"""Canonical digest algorithms for crosswalk snapshots and lifecycle events."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Mapping
from pathlib import Path, PurePosixPath


EVENT_FIELDS = (
    "event_id",
    "state",
    "date",
    "actor",
    "reason",
    "predecessor_id",
    "successor_id",
    "approval_reference",
    "previous_event_digest",
)

_FIXED_FILES = {"README.md", "PROVISION_INVENTORY.md", "ESAF_CONTROL_MANIFEST.json"}
_RECORD_FILE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def event_bytes(event: Mapping[str, str]) -> bytes:
    """Serialize one lifecycle event using the frozen canonical framing."""
    output = bytearray()
    for field in EVENT_FIELDS:
        value = unicodedata.normalize("NFC", event.get(field, "")).encode("utf-8")
        output.extend(f"{field}:{len(value)}:".encode("ascii"))
        output.extend(value)
        output.extend(b"\n")
    return bytes(output)


def event_digest(event: Mapping[str, str]) -> str:
    """Return the lowercase SHA-256 digest of a canonical lifecycle event."""
    return hashlib.sha256(event_bytes(event)).hexdigest()


def snapshot_digest_from_files(
    snapshot_path: str,
    files: Mapping[str, bytes],
) -> str:
    """Hash one canonical snapshot represented by repository-relative bytes."""
    snapshot = PurePosixPath(snapshot_path)
    if (
        not snapshot_path
        or "\\" in snapshot_path
        or snapshot.is_absolute()
        or snapshot.as_posix() != snapshot_path
        or any(part in {".", ".."} for part in snapshot.parts)
    ):
        raise ValueError("snapshot path must be canonical repository-relative POSIX")

    manifest: list[tuple[str, str]] = []
    names: set[str] = set()
    for relative, raw in files.items():
        path = PurePosixPath(relative)
        if (
            "\\" in relative
            or path.is_absolute()
            or path.as_posix() != relative
            or path.parent != snapshot
        ):
            raise ValueError(f"unexpected snapshot entry {relative}")
        if path.name not in _FIXED_FILES and not _RECORD_FILE.fullmatch(path.name):
            raise ValueError(f"unexpected snapshot entry {path.name}")
        if not isinstance(raw, bytes):
            raise ValueError(f"snapshot entry {path.name} must be bytes")
        names.add(path.name)
        manifest.append((relative, hashlib.sha256(raw).hexdigest()))

    required = _FIXED_FILES - names
    if required:
        raise ValueError(f"missing snapshot entry {sorted(required)[0]}")
    serialized = b"".join(
        f"{digest}  {relative}\n".encode("utf-8")
        for relative, digest in sorted(manifest)
    )
    return hashlib.sha256(serialized).hexdigest()


def snapshot_digest(root: Path, snapshot: Path) -> str:
    """Hash the complete, direct-child regular-file set of a snapshot."""
    try:
        snapshot_relative = snapshot.relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError("snapshot is outside repository root") from error

    files: dict[str, bytes] = {}
    try:
        entries = list(snapshot.iterdir())
    except OSError as error:
        raise ValueError(f"cannot inspect snapshot: {error}") from error
    for entry in entries:
        if entry.is_symlink() or not entry.is_file():
            raise ValueError(f"unexpected snapshot entry {entry.name}")
        if entry.name not in _FIXED_FILES and not _RECORD_FILE.fullmatch(entry.name):
            raise ValueError(f"unexpected snapshot entry {entry.name}")
        try:
            raw = entry.read_bytes()
        except OSError as error:
            raise ValueError(f"cannot read snapshot entry {entry.name}: {error}") from error
        relative = entry.relative_to(root).as_posix()
        files[relative] = raw
    return snapshot_digest_from_files(snapshot_relative, files)
