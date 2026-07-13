"""Deterministic ESAF control manifests built from immutable Git objects."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


_RELEASE = re.compile(r"(?m)^Current Version:\s+\*\*(?P<release>[^*]+)\*\*\s*$")


def _git(root: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
    )


def git_bytes(root: Path, revision: str, path: str) -> bytes:
    """Return the exact bytes stored for ``path`` at ``revision``."""
    completed = _git(root, "show", f"{revision}:{path}")
    if completed.returncode:
        raise ValueError(completed.stderr.decode("utf-8", errors="replace").strip())
    return completed.stdout


def _resolve_commit(root: Path, revision: str) -> str:
    completed = _git(root, "rev-parse", "--verify", f"{revision}^{{commit}}")
    if completed.returncode:
        raise ValueError("pinned commit is unreachable")
    resolved = completed.stdout.decode("ascii", errors="replace").strip().lower()
    if resolved != revision.lower():
        raise ValueError("pinned commit is unreachable")
    return resolved


def _release_at(root: Path, commit_sha: str) -> str:
    try:
        text = git_bytes(root, commit_sha, "VERSION.md").decode("utf-8")
    except (UnicodeDecodeError, ValueError) as error:
        raise ValueError(f"cannot read VERSION.md at pinned commit: {error}") from error
    match = _RELEASE.search(text)
    if match is None:
        raise ValueError("VERSION.md release is unavailable at pinned commit")
    return match.group("release")


def build_control_manifest(
    root: Path,
    commit_sha: str,
    esaf_release: str,
    tag_alias: str | None,
) -> dict[str, object]:
    """Regenerate the release manifest from one immutable commit."""
    commit = _resolve_commit(root, commit_sha)
    actual_release = _release_at(root, commit)
    if actual_release != esaf_release:
        raise ValueError(
            f"VERSION.md release mismatch: declared {esaf_release}, pinned commit has {actual_release}"
        )

    if tag_alias is not None:
        completed = _git(root, "rev-parse", "--verify", f"{tag_alias}^{{commit}}")
        resolved_tag = (
            completed.stdout.decode("ascii", errors="replace").strip().lower()
            if completed.returncode == 0
            else None
        )
        if resolved_tag != commit:
            raise ValueError("tag alias does not resolve to pinned commit")

    catalog_bytes = git_bytes(root, commit, "controls/catalog.json")
    try:
        catalog = json.loads(catalog_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid controls/catalog.json at pinned commit: {error}") from error
    catalog_controls = catalog.get("controls") if isinstance(catalog, dict) else None
    if not isinstance(catalog_controls, list):
        raise ValueError("controls/catalog.json controls must be an array")

    controls: list[dict[str, object]] = []
    for item in catalog_controls:
        if not isinstance(item, dict):
            raise ValueError("controls/catalog.json contains a non-object control")
        try:
            control_id = item["id"]
            version = item["version"]
            status = item["status"]
            path = item["path"]
        except KeyError as error:
            raise ValueError(f"catalog control missing {error.args[0]}") from error
        if not all(isinstance(value, str) for value in (control_id, version, status, path)):
            raise ValueError("catalog control id, version, status, and path must be strings")
        record_bytes = git_bytes(root, commit, f"controls/{path}")
        controls.append(
            {
                "id": control_id,
                "version": version,
                "status": status,
                "path": path,
                "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
            }
        )

    manifest: dict[str, object] = {
        "schema_version": "1.0.0",
        "esaf_release": esaf_release,
        "source_commit_sha": commit,
        "control_catalog_sha256": hashlib.sha256(catalog_bytes).hexdigest(),
        "controls": sorted(controls, key=lambda control: str(control["id"])),
    }
    if tag_alias is not None:
        manifest["tag_alias"] = tag_alias
    return manifest


def render_manifest(manifest: dict[str, object]) -> str:
    """Render a manifest in its canonical deterministic JSON form."""
    return json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
