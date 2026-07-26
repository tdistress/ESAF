"""Atomically publish a validated qualified-review campaign seal and archive."""

from __future__ import annotations

import argparse
import ctypes
import errno
import os
from pathlib import Path
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


def _rename_directory_no_replace(source: Path, destination: Path) -> None:
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
            -100,
            os.fsencode(source),
            -100,
            os.fsencode(destination),
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
    destination = _destination(output_directory, worktrees)
    _validate_archive_locator(resolved_candidate, archive_locator)
    try:
        reader.require_candidate_execution_state(resolved_candidate)
    except ValueError as error:
        raise _OperationalFailure("candidate execution state is invalid") from error
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

    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.staging-",
            dir=destination.parent,
        )
    )
    published = False
    try:
        if staging.stat().st_dev != destination.parent.stat().st_dev:
            raise _OperationalFailure("staging filesystem does not match output")
        _write_exclusive_fsync(
            staging / _ARCHIVE_NAME,
            details.archive_bytes,
        )
        _write_exclusive_fsync(staging / _SEAL_NAME, seal_bytes)
        _fsync_directory_when_supported(staging)
        try:
            reader.require_candidate_execution_state(resolved_candidate)
        except ValueError as error:
            raise _OperationalFailure(
                "candidate execution state changed"
            ) from error
        if os.path.lexists(destination):
            raise _OperationalFailure("output directory appeared during sealing")
        _rename_directory_no_replace(staging, destination)
        _fsync_directory_when_supported(destination.parent)
        published = True
    finally:
        if not published:
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
