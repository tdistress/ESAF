"""Load and validate the complete partition of tracked unit-test modules."""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess


MANIFEST_PATH = Path("tools/test-shards.json")
SCHEMA = "esaf-test-shards-v1"
SHARD_IDS = (
    "profile_validation",
    "qualified_review_evidence",
    "mapping_review_bundle",
    "remaining",
)
MODULE_PATH = re.compile(r"^tests/test_[^/]+\.py$")


@dataclass(frozen=True)
class Shard:
    """One named, ordered collection of unit-test modules."""

    identifier: str
    modules: tuple[str, ...]


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build a JSON object while rejecting repeated keys."""
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"manifest has duplicate key {key!r}")
        value[key] = item
    return value


def validate_module_path(value: object) -> str:
    """Return one canonical test-module path or raise ValueError."""
    if not isinstance(value, str):
        raise ValueError("manifest module entry must be a string")
    if "\\" in value or not MODULE_PATH.fullmatch(value):
        raise ValueError(f"manifest module path is invalid: {value!r}")
    parts = value.split("/")
    if "." in parts or ".." in parts:
        raise ValueError(f"manifest module path is invalid: {value!r}")
    return value


def load_manifest(root: Path) -> tuple[Shard, ...]:
    """Load the strict shard manifest rooted at *root*."""
    path = root / MANIFEST_PATH
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except json.JSONDecodeError as error:
        raise ValueError("test shard manifest is not valid JSON") from error
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError("test shard manifest could not be read") from error

    if not isinstance(value, dict) or set(value) != {"schema", "shards"}:
        raise ValueError("manifest top-level keys must be schema and shards")
    if value["schema"] != SCHEMA:
        raise ValueError(f"manifest schema must be {SCHEMA!r}")
    raw_shards = value["shards"]
    if not isinstance(raw_shards, list):
        raise ValueError("manifest shards must be a list")

    shards: list[Shard] = []
    for raw_shard in raw_shards:
        if not isinstance(raw_shard, dict) or set(raw_shard) != {"id", "modules"}:
            raise ValueError("manifest shard keys must be id and modules")
        identifier = raw_shard["id"]
        modules = raw_shard["modules"]
        if not isinstance(identifier, str):
            raise ValueError("manifest shard id must be a string")
        if not isinstance(modules, list):
            raise ValueError(f"manifest shard {identifier!r} modules must be a list")
        validated_modules = tuple(validate_module_path(item) for item in modules)
        if list(validated_modules) != sorted(validated_modules):
            raise ValueError(f"manifest shard {identifier!r} modules must be sorted")
        shards.append(Shard(identifier, validated_modules))

    identifiers = tuple(shard.identifier for shard in shards)
    if identifiers != SHARD_IDS:
        raise ValueError("manifest shard identifiers have the wrong order")
    return tuple(shards)


def tracked_test_modules(
    root: Path, runner: Callable[..., object] | None = None
) -> tuple[str, ...]:
    """Return tracked test-module paths using Git's NUL-delimited output."""
    command_runner = runner if runner is not None else subprocess.run
    completed = command_runner(
        ["git", "ls-files", "-z", "--", "tests/test_*.py"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if getattr(completed, "returncode", None) != 0:
        raise ValueError("could not discover tracked test modules")
    output = getattr(completed, "stdout", None)
    if not isinstance(output, bytes):
        raise ValueError("tracked test-module discovery did not return bytes")
    try:
        decoded = output.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ValueError("tracked test-module discovery is not valid UTF-8") from error
    entries = decoded.split("\0")
    if entries and entries[-1] == "":
        entries.pop()
    if not entries or any(not entry for entry in entries):
        if entries:
            raise ValueError("tracked test-module discovery returned an empty path")
        return ()
    return tuple(sorted(entries))


def validate_manifest(
    root: Path, runner: Callable[..., object] | None = None
) -> tuple[Shard, ...]:
    """Validate that the manifest partitions every tracked test module once."""
    shards = load_manifest(root)
    assigned = [module for shard in shards for module in shard.modules]
    tracked = tracked_test_modules(root, runner)
    counts = Counter(assigned)
    assigned_set = set(assigned)
    tracked_set = set(tracked)
    missing = sorted(tracked_set - assigned_set)
    duplicate = sorted(module for module, count in counts.items() if count > 1)
    untracked = sorted(assigned_set - tracked_set)
    if missing or duplicate or untracked:
        findings = []
        if missing:
            findings.append("missing: " + ", ".join(missing))
        if duplicate:
            findings.append("duplicate: " + ", ".join(duplicate))
        if untracked:
            findings.append("untracked: " + ", ".join(untracked))
        raise ValueError("manifest test modules are invalid: " + "; ".join(findings))
    return shards
