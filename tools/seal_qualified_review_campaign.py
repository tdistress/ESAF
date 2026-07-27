"""Atomically publish a validated qualified-review campaign seal and archive."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import ctypes
from ctypes import wintypes
from dataclasses import dataclass
import errno
import os
from pathlib import Path
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mapping_review_bundle import GitReader
from tools.crosswalks.qualified_review_evidence import (
    EvidenceError,
    EvidenceOperationalError,
    build_seal_record,
    canonical_json_bytes,
)
from tools.validate_qualified_review_evidence import (
    VALIDATOR_VERSION,
    _ValidationFailure,
    _validate_campaign_details,
)


_ARCHIVE_NAME = "CAMPAIGN_ARCHIVE.zip"
_SEAL_NAME = "CAMPAIGN_SEAL.json"


class _OperationalFailure(RuntimeError):
    """A sanitized sealing operation failure."""


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        del message
        raise _OperationalFailure("invalid command arguments")


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _destination(
    output: Path,
    worktrees: tuple[Path, ...],
) -> Path:
    if os.path.lexists(output):
        raise _OperationalFailure("output directory already exists")
    parent = output.parent
    try:
        parent_stat = parent.stat(follow_symlinks=False)
        resolved_parent = parent.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise _OperationalFailure("output parent is unavailable") from error
    if not stat.S_ISDIR(parent_stat.st_mode):
        raise _OperationalFailure("output parent is not a directory")
    if stat.S_ISLNK(parent_stat.st_mode):
        raise _OperationalFailure("output parent must not be an alias")
    destination = resolved_parent / output.name
    if any(_is_within(destination, root) for root in worktrees):
        raise _OperationalFailure("output must be outside every Git worktree")
    return destination


@dataclass
class _DestinationAnchor:
    destination: Path
    worktrees: tuple[Path, ...]
    chain: tuple[tuple[Path, int, int], ...]
    parent_fd: int | None
    windows_handles: tuple[int, ...]

    def revalidate(self) -> None:
        for path, device, inode in self.chain:
            observed = path.stat(follow_symlinks=False)
            if (
                observed.st_dev != device
                or observed.st_ino != inode
                or not stat.S_ISDIR(observed.st_mode)
                or stat.S_ISLNK(observed.st_mode)
                or (
                    getattr(observed, "st_file_attributes", 0)
                    & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
                )
            ):
                raise _OperationalFailure(
                    "output ancestor identity changed"
                )
        resolved_parent = self.destination.parent.resolve(strict=True)
        if resolved_parent != self.destination.parent:
            raise _OperationalFailure("output ancestor became an alias")
        if any(
            _is_within(resolved_parent / self.destination.name, root)
            for root in self.worktrees
        ):
            raise _OperationalFailure("output moved inside a Git worktree")


def _ancestor_chain(parent: Path) -> tuple[Path, ...]:
    resolved = parent.resolve(strict=True)
    return tuple(reversed((resolved, *resolved.parents)))


def _open_windows_directory(path: Path) -> int:
    create_file = ctypes.windll.kernel32.CreateFileW
    create_file.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    create_file.restype = wintypes.HANDLE
    handle = create_file(
        str(path),
        0,
        0x00000001 | 0x00000002,
        None,
        3,
        0x02000000 | 0x00200000,
        None,
    )
    invalid = ctypes.c_void_p(-1).value
    if handle == invalid:
        raise ctypes.WinError(ctypes.get_last_error())
    return int(handle)


@contextmanager
def _anchored_destination(
    output: Path,
    worktrees: tuple[Path, ...],
) -> object:
    destination = _destination(output, worktrees)
    chain_paths = _ancestor_chain(destination.parent)
    identities: list[tuple[Path, int, int]] = []
    windows_handles: list[int] = []
    descriptors: list[int] = []
    parent_fd: int | None = None
    try:
        for path in chain_paths:
            observed = path.stat(follow_symlinks=False)
            if (
                not stat.S_ISDIR(observed.st_mode)
                or stat.S_ISLNK(observed.st_mode)
                or (
                    getattr(observed, "st_file_attributes", 0)
                    & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
                )
            ):
                raise _OperationalFailure(
                    "output ancestor must be an unaliased directory"
                )
            identities.append((path, observed.st_dev, observed.st_ino))
            if os.name == "nt":
                windows_handles.append(_open_windows_directory(path))
        if os.name != "nt":
            if not (
                sys.platform.startswith("linux")
                and os.open in os.supports_dir_fd
                and os.mkdir in os.supports_dir_fd
                and os.stat in os.supports_dir_fd
            ):
                raise _OperationalFailure(
                    "atomic anchored publication is unavailable"
                )
            flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            current = os.open(chain_paths[0], flags)
            descriptors.append(current)
            for path in chain_paths[1:]:
                current = os.open(
                    path.name,
                    flags,
                    dir_fd=current,
                )
                descriptors.append(current)
            parent_fd = descriptors[-1]
        anchor = _DestinationAnchor(
            destination=destination,
            worktrees=worktrees,
            chain=tuple(identities),
            parent_fd=parent_fd,
            windows_handles=tuple(windows_handles),
        )
        anchor.revalidate()
        yield anchor
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)
        if os.name == "nt":
            close_handle = ctypes.windll.kernel32.CloseHandle
            for handle in reversed(windows_handles):
                close_handle(wintypes.HANDLE(handle))


def _validate_archive_locator(candidate: str, locator: str) -> None:
    try:
        build_seal_record(
            manifest_bytes=b"",
            archive_bytes=b"",
            archive_locator=locator,
            campaign_id="locator-check",
            candidate_commit=candidate,
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            validator_version=VALIDATOR_VERSION,
        )
    except EvidenceError as error:
        raise _OperationalFailure("archive locator is invalid") from error


def _write_exclusive_fsync(path: Path, content: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_BINARY", 0)
    descriptor: int | None = None
    try:
        descriptor = os.open(path, flags, 0o600)
        view = memoryview(content)
        written = 0
        while written < len(view):
            count = os.write(descriptor, view[written:])
            if count <= 0:
                raise OSError("short write")
            written += count
        os.fsync(descriptor)
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _write_exclusive_fsync_at(
    directory_fd: int,
    name: str,
    content: bytes,
) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(name, flags, 0o600, dir_fd=directory_fd)
    try:
        view = memoryview(content)
        written = 0
        while written < len(view):
            count = os.write(descriptor, view[written:])
            if count <= 0:
                raise OSError("short write")
            written += count
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fsync_directory_when_supported(path: Path) -> None:
    if os.name == "nt":
        return
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor: int | None = None
    try:
        descriptor = os.open(path, flags)
        os.fsync(descriptor)
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _remove_owned_staging(staging: Path, parent: Path) -> None:
    try:
        exact_parent = staging.parent.resolve(strict=True)
        expected_parent = parent.resolve(strict=True)
    except (OSError, RuntimeError):
        return
    if exact_parent != expected_parent:
        return
    if not staging.name.startswith(".") or ".staging-" not in staging.name:
        return
    if os.path.lexists(staging):
        try:
            shutil.rmtree(staging)
        except OSError:
            pass


def _rename_directory_no_replace(
    source: Path,
    destination: Path,
    source_dir_fd: int | None = None,
    destination_dir_fd: int | None = None,
) -> None:
    if os.name == "nt":
        os.rename(source, destination)
        return
    if sys.platform.startswith("linux"):
        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = getattr(libc, "renameat2", None)
        if renameat2 is None:
            raise _OperationalFailure(
                "atomic no-replace rename is unavailable"
            )
        renameat2.argtypes = (
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        )
        renameat2.restype = ctypes.c_int
        result = renameat2(
            source_dir_fd if source_dir_fd is not None else -100,
            os.fsencode(source.name if source_dir_fd is not None else source),
            (
                destination_dir_fd
                if destination_dir_fd is not None
                else -100
            ),
            os.fsencode(
                destination.name
                if destination_dir_fd is not None
                else destination
            ),
            1,
        )
        if result != 0:
            error_number = ctypes.get_errno()
            raise OSError(
                error_number or errno.EIO,
                "atomic directory publication failed",
            )
        return
    if sys.platform == "darwin":
        libc = ctypes.CDLL(None, use_errno=True)
        renamex_np = getattr(libc, "renamex_np", None)
        if renamex_np is None:
            raise _OperationalFailure(
                "atomic no-replace rename is unavailable"
            )
        renamex_np.argtypes = (
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_uint,
        )
        renamex_np.restype = ctypes.c_int
        result = renamex_np(
            os.fsencode(source),
            os.fsencode(destination),
            0x00000004,
        )
        if result != 0:
            error_number = ctypes.get_errno()
            raise OSError(
                error_number or errno.EIO,
                "atomic directory publication failed",
            )
        return
    raise _OperationalFailure("atomic no-replace rename is unavailable")


def _publish(
    *,
    reader: GitReader,
    candidate: str,
    evidence_root: Path,
    output_directory: Path,
    archive_locator: str,
    draft_evidence_root: Path | None,
    draft_seal_record: Path | None,
    draft_archive: Path | None,
) -> tuple[dict[str, object], bytes]:
    resolved_candidate = reader.resolve_commit(candidate)
    worktrees = reader.worktree_roots()
    with _anchored_destination(output_directory, worktrees) as anchor_value:
        assert isinstance(anchor_value, _DestinationAnchor)
        anchor = anchor_value
        destination = anchor.destination
        _validate_archive_locator(resolved_candidate, archive_locator)
        try:
            reader.require_candidate_execution_state(resolved_candidate)
        except ValueError as error:
            raise _OperationalFailure(
                "candidate execution state is invalid"
            ) from error
        try:
            details = _validate_campaign_details(
                reader,
                resolved_candidate,
                evidence_root,
                draft_evidence_root,
                draft_seal_record,
                draft_archive,
            )
        except (_ValidationFailure, EvidenceError, ValueError):
            raise
        if (
            not details.report.evidence_valid
            or not details.report.readiness_value
        ):
            raise _ValidationFailure("campaign is not ready to seal")
        seal_record, seal_bytes = build_seal_record(
            manifest_bytes=details.manifest_bytes,
            archive_bytes=details.archive_bytes,
            archive_locator=archive_locator,
            campaign_id=details.campaign.campaign_id,
            candidate_commit=resolved_candidate,
            evidence_valid=details.report.evidence_valid,
            readiness_name=details.report.readiness_name,
            readiness_value=details.report.readiness_value,
            validator_version=VALIDATOR_VERSION,
        )
        staging_name = (
            f".{destination.name}.staging-{secrets.token_hex(12)}"
        )
        staging = destination.parent / staging_name
        staging_fd: int | None = None
        published = False
        try:
            if anchor.parent_fd is None:
                staging = Path(
                    tempfile.mkdtemp(
                        prefix=f".{destination.name}.staging-",
                        dir=destination.parent,
                    )
                )
                if staging.stat().st_dev != destination.parent.stat().st_dev:
                    raise _OperationalFailure(
                        "staging filesystem does not match output"
                    )
                _write_exclusive_fsync(
                    staging / _ARCHIVE_NAME,
                    details.archive_bytes,
                )
                _write_exclusive_fsync(staging / _SEAL_NAME, seal_bytes)
                _fsync_directory_when_supported(staging)
            else:
                os.mkdir(staging_name, 0o700, dir_fd=anchor.parent_fd)
                flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
                staging_fd = os.open(
                    staging_name,
                    flags,
                    dir_fd=anchor.parent_fd,
                )
                _write_exclusive_fsync_at(
                    staging_fd,
                    _ARCHIVE_NAME,
                    details.archive_bytes,
                )
                _write_exclusive_fsync_at(
                    staging_fd,
                    _SEAL_NAME,
                    seal_bytes,
                )
                os.fsync(staging_fd)
            try:
                reader.require_candidate_execution_state(resolved_candidate)
            except ValueError as error:
                raise _OperationalFailure(
                    "candidate execution state changed"
                ) from error
            anchor.revalidate()
            if os.path.lexists(destination):
                raise _OperationalFailure(
                    "output directory appeared during sealing"
                )
            _rename_directory_no_replace(
                staging,
                destination,
                anchor.parent_fd,
                anchor.parent_fd,
            )
            if anchor.parent_fd is None:
                _fsync_directory_when_supported(destination.parent)
            else:
                os.fsync(anchor.parent_fd)
            published = True
        finally:
            if staging_fd is not None:
                if not published:
                    for name in (_ARCHIVE_NAME, _SEAL_NAME):
                        try:
                            os.unlink(name, dir_fd=staging_fd)
                        except FileNotFoundError:
                            pass
                os.close(staging_fd)
                if not published:
                    try:
                        os.rmdir(staging_name, dir_fd=anchor.parent_fd)
                    except OSError:
                        pass
            elif not published:
                _remove_owned_staging(staging, destination.parent)
        return seal_record, seal_bytes


def main(
    argv: list[str] | None = None,
    *,
    root: Path = ROOT,
) -> int:
    parser = _ArgumentParser(add_help=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--archive-locator", required=True)
    parser.add_argument("--draft-evidence-root", type=Path)
    parser.add_argument("--draft-seal-record", type=Path)
    parser.add_argument("--draft-archive", type=Path)
    try:
        args = parser.parse_args(argv)
        draft_inputs = (
            args.draft_evidence_root,
            args.draft_seal_record,
            args.draft_archive,
        )
        if sum(item is not None for item in draft_inputs) not in {0, 3}:
            raise _OperationalFailure(
                "preserved Draft inputs must be supplied together"
            )
        reader = GitReader(root)
        try:
            record, _seal_bytes = _publish(
                reader=reader,
                candidate=args.candidate,
                evidence_root=args.evidence_root,
                output_directory=args.output_directory,
                archive_locator=args.archive_locator,
                draft_evidence_root=args.draft_evidence_root,
                draft_seal_record=args.draft_seal_record,
                draft_archive=args.draft_archive,
            )
        except EvidenceOperationalError:
            raise
        except (_ValidationFailure, EvidenceError):
            return 1
        print(canonical_json_bytes(record).decode("utf-8"), end="")
        return 0
    except (
        _OperationalFailure,
        OSError,
        subprocess.SubprocessError,
        ValueError,
    ):
        print("qualified-review campaign sealing failed", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
