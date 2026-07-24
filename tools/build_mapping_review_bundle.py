from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from tools.crosswalks.io import load_yaml_mapping


FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
GENERATOR_VERSION = "1.0.0"


@dataclass(frozen=True)
class MappingProfile:
    mapping_set_id: str
    snapshot_path: str
    label: str
    direction: str
    expected_count: int


_PROFILE_ROWS = (
    (
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0",
        "Core",
        "external_to_esaf",
        116,
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0",
        "Plus forward",
        "esaf_to_external",
        144,
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0",
        "Plus reverse",
        "external_to_esaf",
        144,
    ),
)
PROFILES = {row[0]: MappingProfile(*row) for row in _PROFILE_ROWS}


@dataclass(frozen=True)
class PackageFile:
    path: str
    content: bytes
    purpose: str


def parse_front_matter_bytes(content: bytes) -> tuple[dict[str, object], str]:
    if content.startswith(b"\xef\xbb\xbf") or b"\r" in content:
        raise ValueError("package Markdown must be canonical UTF-8/LF")
    text = content.decode("utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("malformed YAML front matter")
    return load_yaml_mapping(parts[1]), parts[2]


class GitReader:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def _run(
        self,
        *arguments: str,
        text: bool = False,
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=text,
        )

    def resolve_commit(self, revision: str) -> str:
        if not FULL_SHA.fullmatch(revision):
            raise ValueError(
                "candidate must be a full lowercase 40-character Git SHA"
            )
        try:
            resolved = self._run(
                "rev-parse",
                "--verify",
                f"{revision}^{{commit}}",
                text=True,
            ).stdout.strip()
        except subprocess.CalledProcessError as error:
            raise ValueError("candidate is not an available commit") from error
        if resolved != revision:
            raise ValueError("candidate does not resolve to the exact commit")
        return resolved

    def read_bytes(self, commit: str, path: str) -> bytes:
        if path.startswith("/") or ".." in Path(path).parts or "\\" in path:
            raise ValueError(f"unsafe repository path: {path}")
        try:
            return self._run("show", f"{commit}:{path}").stdout
        except subprocess.CalledProcessError as error:
            raise ValueError(
                f"missing tracked file at candidate: {path}"
            ) from error

    def list_files(self, commit: str, path: str) -> tuple[str, ...]:
        result = self._run(
            "ls-tree",
            "-r",
            "--name-only",
            "-z",
            commit,
            "--",
            path,
        ).stdout
        names = tuple(item.decode("utf-8") for item in result.split(b"\0") if item)
        return tuple(sorted(names))

    def worktree_roots(self) -> tuple[Path, ...]:
        output = self._run("worktree", "list", "--porcelain", "-z").stdout
        roots = []
        for field in output.split(b"\0"):
            if field.startswith(b"worktree "):
                roots.append(Path(field[9:].decode("utf-8")).resolve())
        return tuple(roots)


def _package_file(
    reader: GitReader,
    commit: str,
    path: str,
    purpose: str,
) -> PackageFile:
    return PackageFile(path, reader.read_bytes(commit, path), purpose)


def _require_draft(
    metadata: dict[str, object],
    mapping_set_id: str,
    subject: str,
) -> None:
    if metadata.get("mapping_set_id") != mapping_set_id:
        raise ValueError(f"{subject} mapping-set identifier mismatch")
    if metadata.get("status") != "draft" or "reviewer" in metadata:
        raise ValueError(f"{subject} must remain draft without reviewer metadata")


def collect_package_files(
    reader: GitReader,
    commit: str,
    profile: MappingProfile,
) -> tuple[PackageFile, ...]:
    snapshot_paths = reader.list_files(commit, profile.snapshot_path)
    required = {
        f"{profile.snapshot_path}/README.md",
        f"{profile.snapshot_path}/PROVISION_INVENTORY.md",
        f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json",
    }
    if not required.issubset(snapshot_paths):
        raise ValueError("snapshot is missing required artifacts")
    record_paths = tuple(
        path for path in snapshot_paths
        if path.endswith(".md") and path not in required
    )
    if len(record_paths) != profile.expected_count:
        raise ValueError("mapping-record population mismatch")

    files: list[PackageFile] = []
    readme_path = f"{profile.snapshot_path}/README.md"
    readme = _package_file(reader, commit, readme_path, "mapping set")
    set_metadata, _ = parse_front_matter_bytes(readme.content)
    _require_draft(set_metadata, profile.mapping_set_id, "mapping set")
    scope = set_metadata.get("scope")
    if not isinstance(scope, dict) or scope.get("inventory_count") != profile.expected_count:
        raise ValueError("mapping-set inventory count mismatch")
    files.append(readme)

    inventory_path = f"{profile.snapshot_path}/PROVISION_INVENTORY.md"
    inventory = _package_file(
        reader, commit, inventory_path, "provision inventory"
    )
    inventory_metadata, _ = parse_front_matter_bytes(inventory.content)
    if inventory_metadata.get("mapping_set_id") != profile.mapping_set_id:
        raise ValueError("inventory mapping-set identifier mismatch")
    provision_ids = inventory_metadata.get("provision_ids")
    if (
        inventory_metadata.get("expected_count") != profile.expected_count
        or not isinstance(provision_ids, list)
        or len(provision_ids) != profile.expected_count
        or len(set(provision_ids)) != profile.expected_count
    ):
        raise ValueError("provision inventory population mismatch")
    files.append(inventory)

    record_ids: set[str] = set()
    record_provisions: set[str] = set()
    for path in record_paths:
        record = _package_file(reader, commit, path, "mapping record")
        metadata, _ = parse_front_matter_bytes(record.content)
        _require_draft(metadata, profile.mapping_set_id, f"record {path}")
        record_id = metadata.get("record_id")
        provision_id = metadata.get("external_provision_id")
        if not isinstance(record_id, str) or record_id in record_ids:
            raise ValueError("duplicate or invalid mapping-record identifier")
        if not isinstance(provision_id, str) or provision_id in record_provisions:
            raise ValueError("duplicate or invalid external provision identifier")
        record_ids.add(record_id)
        record_provisions.add(provision_id)
        files.append(record)
    if record_provisions != set(provision_ids):
        raise ValueError("mapping records do not match provision inventory")

    manifest_path = f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"
    manifest_file = _package_file(
        reader, commit, manifest_path, "control manifest"
    )
    manifest = json.loads(manifest_file.content)
    if manifest.get("esaf_release") != set_metadata["esaf_release"]["id"]:
        raise ValueError("control manifest ESAF release mismatch")
    control_source = manifest.get("source_commit_sha")
    if not isinstance(control_source, str):
        raise ValueError("control manifest source commit is missing")
    control_source = reader.resolve_commit(control_source)
    if control_source != set_metadata["esaf_release"]["source_commit_sha"]:
        raise ValueError("control manifest source commit mismatch")
    controls = manifest.get("controls")
    if not isinstance(controls, list) or not controls:
        raise ValueError("control manifest has no controls")
    files.append(manifest_file)
    seen_controls: set[str] = set()
    for control in controls:
        control_path = f"controls/{control['path']}"
        if control_path in seen_controls:
            raise ValueError("duplicate control manifest path")
        seen_controls.add(control_path)
        control_file = _package_file(
            reader, control_source, control_path, "referenced ESAF control"
        )
        if hashlib.sha256(control_file.content).hexdigest() != control["record_sha256"]:
            raise ValueError(f"control digest mismatch: {control_path}")
        files.append(control_file)

    registry_path = f"crosswalks/registry/{profile.mapping_set_id}.md"
    registry = _package_file(
        reader, commit, registry_path, "lifecycle registry"
    )
    registry_metadata, registry_body = parse_front_matter_bytes(registry.content)
    if registry_metadata.get("mapping_set_id") != profile.mapping_set_id:
        raise ValueError("registry mapping-set identifier mismatch")
    if registry_metadata.get("events") != []:
        raise ValueError("registry lifecycle event array must be empty")
    if re.search(r"\bdraft\b", registry_body, re.IGNORECASE) is None:
        raise ValueError("registry body must identify Draft state")
    files.append(registry)

    catalog = json.loads(reader.read_bytes(commit, "crosswalks/catalog.json"))
    matches = [
        item for item in catalog["mapping_sets"]
        if item["metadata"]["mapping_set_id"] == profile.mapping_set_id
    ]
    if len(matches) != 1 or len(matches[0]["provisions"]) != profile.expected_count:
        raise ValueError("catalog entry population mismatch")
    catalog_bytes = (
        json.dumps(
            {
                "schema_version": catalog["schema_version"],
                "generated_from": catalog["generated_from"],
                "mapping_set": matches[0],
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    files.append(
        PackageFile(
            "review-metadata/catalog-entry.json",
            catalog_bytes,
            "catalog entry",
        )
    )

    fixed_paths = {
        "crosswalks/ESAF-1600.md": "ESAF-1600 method",
        "crosswalks/schema/esaf-control-manifest.schema.json": "crosswalk schema",
        "crosswalks/schema/lifecycle-record.schema.json": "crosswalk schema",
        "crosswalks/schema/mapping-record.schema.json": "crosswalk schema",
        "crosswalks/schema/mapping-set.schema.json": "crosswalk schema",
        "crosswalks/schema/provision-inventory.schema.json": "crosswalk schema",
        "crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md": "review protocol",
        "crosswalks/reviews/templates/REVIEWER_ATTESTATION.md": "blank review template",
        "crosswalks/reviews/templates/SPECIFICATION_INVENTORY_REVIEW.md": "blank review template",
        "crosswalks/reviews/templates/SECURITY_OVERCLAIMING_REVIEW.md": "blank review template",
    }
    files.extend(
        _package_file(reader, commit, path, purpose)
        for path, purpose in fixed_paths.items()
    )
    paths = [item.path for item in files]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate package path")
    return tuple(sorted(files, key=lambda item: item.path))
