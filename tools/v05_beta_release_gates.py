#!/usr/bin/env python3
"""Validate the v0.5-beta release-record contract."""

from __future__ import annotations

import argparse
from datetime import date
from functools import lru_cache
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Sequence

import yaml


RELEASE = "0.5-beta"
TAG = "v0.5-beta"
ISSUE = 59
RECORD_RELATIVE = (
    "docs/superpowers/reviews/"
    "2026-07-27-v05-beta-publication-readiness.md"
)
REPOSITORY_SCOPE = "complete_git_tracked_repository"
PUBLICATION_CONDITION = "remote_annotated_tag_matches_exact_validated_commit"
MAPPING_DECISION_BASES = {"qualified_approval", "owner_risk_acceptance"}
GATE_IDS = (
    "scope",
    "technical",
    "editorial",
    "terminology",
    "cross_reference_rendering",
    "standards_mapping",
    "profile_scope",
    "release_metadata",
    "governance",
    "post_merge",
)
PHASE_GATE_STATES = {
    "evidence_candidate": {gate: "open" for gate in GATE_IDS},
    "closure_candidate": {
        **{gate: "ready" for gate in GATE_IDS if gate != "post_merge"},
        "post_merge": "open",
    },
    "published": {gate: "closed" for gate in GATE_IDS},
}
REQUIRED_SCOPE_INPUTS = (
    "controls/catalog.json",
    "architectures/patterns",
    "crosswalks/catalog.json",
    "assessment/ESAF-1500.md",
    "profiles/uk/0.1.0/profile.json",
    "docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json",
)
ALLOWED_TOP_LEVEL_KEYS = {
    "release",
    "tag",
    "issue",
    "repository_scope",
    "phase",
    "mapping_decision_basis",
    "mapping_sets",
    "scope",
    "scope_inputs",
    "publication",
    "gates",
}
SHA_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", re.IGNORECASE)
PATTERN_FILE_RE = re.compile(r"ARC-P[1-9][0-9]{2}\.md$")
PROFILE_PATH_RE = re.compile(r"profiles/[^/]+/[^/]+/profile\.json$")
ALLOWED_PUBLICATION_KEYS = {"condition", "date", "evidence"}
ALLOWED_GATE_KEYS = {"state", "evidence"}
PREVIOUS_PHASE = {
    "closure_candidate": "evidence_candidate",
    "published": "closure_candidate",
}


def load_front_matter(path: Path) -> dict[str, object]:
    """Load the YAML front matter from one readiness record."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path}: YAML front matter is required")
    value = yaml.safe_load(text[4:text.index("\n---\n", 4)])
    if not isinstance(value, dict):
        raise ValueError(f"{path}: front matter shall be a mapping")
    return value


def derive_scope(root: Path) -> dict[str, object]:
    """Derive release scope directly from authoritative tracked artifacts."""
    tracked = _tracked_paths(root)
    controls = _load_json(root / "controls/catalog.json")
    crosswalks = _load_json(root / "crosswalks/catalog.json")
    matrix = _load_json(
        root / "docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json"
    )
    profiles = 0
    for profile_path in _tracked_profile_paths(root, tracked):
        profile = _load_json(profile_path)
        if (
            profile.get("status") == "draft"
            and profile.get("target_esaf_release") == TAG
        ):
            profiles += 1
    return {
        "controls": _integer(controls, "control_count"),
        "control_families": len(_mapping(controls, "families")),
        "architecture_patterns": len(_tracked_pattern_paths(root, tracked)),
        "mapping_sets": _integer(_mapping(crosswalks, "counts"), "mapping_sets"),
        "mapping_provisions": _integer(_mapping(crosswalks, "counts"), "provisions"),
        "relationship_legs": _integer(_mapping(crosswalks, "counts"), "relationships"),
        "negative_dispositions": _integer(
            _mapping(crosswalks, "counts"), "negative_dispositions"
        ),
        "assessment_foundation": _assessment_foundation(root),
        "draft_profiles": profiles,
        "pci_dss_disposition": matrix.get("recorded_decision"),
    }


def validate_record(root: Path, record: dict[str, object]) -> list[str]:
    """Return deterministic diagnostics for an in-memory v0.5-beta record."""
    errors: list[str] = []
    for key in record:
        if key not in ALLOWED_TOP_LEVEL_KEYS:
            errors.append(f"unknown top-level key {key}")
    if record.get("release") != RELEASE:
        errors.append("release shall equal 0.5-beta")
    if record.get("tag") != TAG:
        errors.append("tag shall equal v0.5-beta")
    if record.get("issue") != ISSUE:
        errors.append("issue shall equal 59")
    if record.get("repository_scope") != REPOSITORY_SCOPE:
        errors.append("repository scope shall equal complete_git_tracked_repository")

    phase = record.get("phase")
    if phase not in PHASE_GATE_STATES:
        errors.append("phase shall be evidence_candidate, closure_candidate, or published")
    if record.get("mapping_decision_basis") not in MAPPING_DECISION_BASES:
        errors.append("mapping_decision_basis shall be supported")
    _validate_publication(errors, phase, record.get("publication"))
    _validate_mapping_sets(errors, root, record.get("mapping_sets"))
    _validate_scope(errors, root, record.get("scope"))
    _validate_scope_inputs(errors, root, record.get("scope_inputs"))
    _validate_gates(errors, phase, record.get("gates"))
    if phase in {"evidence_candidate", "closure_candidate"}:
        _validate_candidate_sha_fields(errors, record)
    return errors


def validate_transition(previous: dict[str, object], candidate: dict[str, object]) -> list[str]:
    """Validate the fixed v0.5-beta release-phase transition sequence."""
    errors: list[str] = []
    if previous.get("release") != RELEASE:
        errors.append("baseline release shall equal 0.5-beta")
    if previous.get("tag") != TAG:
        errors.append("baseline tag shall equal v0.5-beta")
    if previous.get("issue") != ISSUE:
        errors.append("baseline issue shall equal 59")
    if previous.get("repository_scope") != REPOSITORY_SCOPE:
        errors.append(
            "baseline repository scope shall equal complete_git_tracked_repository"
        )
    candidate_phase = candidate.get("phase")
    expected_previous = PREVIOUS_PHASE.get(candidate_phase)
    if expected_previous is not None and previous.get("phase") != expected_previous:
        errors.append(
            f"{candidate_phase} shall transition only from {expected_previous}"
        )
    if (
        previous.get("phase") == "published"
        and candidate_phase in {"evidence_candidate", "closure_candidate"}
    ):
        errors.append("published record shall not transition to a candidate phase")
    return errors


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON object is required")
    return value


def _mapping(value: dict[str, Any], key: str) -> dict[str, Any]:
    child = value.get(key)
    if not isinstance(child, dict):
        raise ValueError(f"{key}: mapping is required")
    return child


def _integer(value: dict[str, Any], key: str) -> int:
    child = value.get(key)
    if not isinstance(child, int) or isinstance(child, bool):
        raise ValueError(f"{key}: integer is required")
    return child


def _assessment_foundation(root: Path) -> bool:
    text = (root / "assessment/ESAF-1500.md").read_text(encoding="utf-8")
    return text.startswith("# ESAF-1500 Assessment Guide\n") and "**Status:** Working Draft" in text


def _validate_publication(errors: list[str], phase: object, publication: object) -> None:
    if not isinstance(publication, dict):
        errors.append("publication is required")
        return
    for key in publication:
        if key not in ALLOWED_PUBLICATION_KEYS:
            errors.append(f"unknown publication key {key}")
    if publication.get("condition") != PUBLICATION_CONDITION:
        errors.append("publication condition is invalid")
    publication_date = publication.get("date")
    if phase in {"evidence_candidate", "closure_candidate"} and publication_date is not None:
        errors.append("candidate publication date shall be null")
    elif phase == "published" and not _iso_date(publication_date):
        errors.append("published publication date shall be an ISO date")
    evidence = publication.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("publication evidence is required")
    elif any(not _https(locator) for locator in evidence):
        errors.append("publication evidence shall use HTTPS locators")


def _validate_mapping_sets(errors: list[str], root: Path, value: object) -> None:
    try:
        catalog = _load_json(root / "crosswalks/catalog.json")
    except (OSError, ValueError, json.JSONDecodeError):
        errors.append("crosswalk catalog cannot be parsed")
        return
    mapping_sets = catalog.get("mapping_sets")
    if not isinstance(mapping_sets, list):
        errors.append("crosswalk catalog cannot be parsed")
        return
    expected: list[str] = []
    draft = True
    source_paths: list[str] = []
    try:
        for item in mapping_sets:
            metadata = item["metadata"]
            identifier = metadata["mapping_set_id"]
            if not isinstance(identifier, str):
                raise ValueError("mapping set identifier is invalid")
            expected.append(identifier)
            draft = draft and metadata.get("status") == "draft"
            source_paths.append(item["path"])
            for provision in item["provisions"]:
                provision_metadata = provision["metadata"]
                draft = draft and provision_metadata.get("status") == "draft"
                source_paths.append(provision["path"])
    except (KeyError, TypeError, OSError, ValueError):
        errors.append("crosswalk catalog cannot be parsed")
        return
    try:
        draft = draft and _mapping_sources_are_draft(root, tuple(source_paths))
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError):
        errors.append("crosswalk catalog cannot be parsed")
        return
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append("mapping_sets shall equal the tracked catalog mapping sets")
        return
    if len(value) != len(set(value)):
        errors.append("mapping_sets shall not contain duplicates")
    if sorted(value) != sorted(expected):
        errors.append("mapping_sets shall equal the tracked catalog mapping sets")
    if not draft:
        errors.append("tracked mapping sets shall remain draft")


def _validate_scope(errors: list[str], root: Path, value: object) -> None:
    try:
        expected = derive_scope(root)
    except (OSError, ValueError, json.JSONDecodeError):
        errors.append("repository scope cannot be derived")
        return
    if value != expected:
        errors.append("scope shall equal the derived repository scope")


def _validate_scope_inputs(errors: list[str], root: Path, value: object) -> None:
    if value is not None and (
        not isinstance(value, list | tuple)
        or tuple(value) != REQUIRED_SCOPE_INPUTS
    ):
        errors.append("scope_inputs shall not override fixed authoritative scope inputs")
    inputs = REQUIRED_SCOPE_INPUTS
    try:
        tracked = _tracked_paths(root)
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        errors.append("repository scope cannot be verified from Git-tracked files")
        return
    if any(input_path not in tracked and not any(path.startswith(f"{input_path}/") for path in tracked) for input_path in inputs):
        errors.append("required scope inputs shall be Git-tracked")
    if _untracked_scope_population(root, tracked):
        errors.append("scope inputs shall not contain untracked files")


def _tracked_paths(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
    )
    return {path for path in result.stdout.decode("utf-8").split("\0") if path}


def _validate_gates(errors: list[str], phase: object, gates: object) -> None:
    if not isinstance(gates, dict):
        errors.append("gates shall contain the exact gate identifiers")
        return
    for gate in gates:
        if gate not in GATE_IDS:
            errors.append(f"unknown gate {gate}")
    for gate in GATE_IDS:
        item = gates.get(gate)
        if not isinstance(item, dict):
            errors.append(f"missing gate {gate}")
            continue
        for key in item:
            if key not in ALLOWED_GATE_KEYS:
                errors.append(f"{gate}: unknown gate key {key}")
        expected = PHASE_GATE_STATES.get(phase, {}).get(gate)
        if item.get("state") != expected:
            errors.append(f"{phase} phase shall set {gate} gate to {expected}")
        evidence = item.get("evidence")
        if not isinstance(evidence, list):
            errors.append(f"{gate}: evidence shall be a list")
        elif item.get("state") in {"ready", "closed"} and not evidence:
            errors.append(f"{gate}: evidence is required")
        elif any(not _https(locator) for locator in evidence):
            errors.append(f"{gate}: evidence shall use HTTPS locators")


def _validate_candidate_sha_fields(errors: list[str], value: object) -> None:
    if _contains_candidate_sha(value):
        errors.append("candidate phases shall not contain SHA fields")


def _contains_candidate_sha(value: object, key: str = "") -> bool:
    if "sha" in key.casefold() or "commit" in key.casefold():
        return True
    if isinstance(value, dict):
        return any(_contains_candidate_sha(child, str(child_key)) for child_key, child in value.items())
    if isinstance(value, list):
        return any(_contains_candidate_sha(child, key) for child in value)
    return isinstance(value, str) and SHA_RE.search(value) is not None


def _iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _mapping_sources_are_draft(root: Path, source_paths: tuple[str, ...]) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", "crosswalks/mappings"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return _cached_mapping_sources_are_draft(root, source_paths, result.stdout)


@lru_cache
def _cached_mapping_sources_are_draft(
    root: Path, source_paths: tuple[str, ...], _working_tree_state: bytes
) -> bool:
    for relative in source_paths:
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if text.lstrip().startswith("{"):
            value = json.loads(text)
        else:
            value = load_front_matter(path)
        if not isinstance(value, dict) or value.get("status") != "draft":
            return False
    return True


def _tracked_pattern_paths(root: Path, tracked: set[str]) -> list[Path]:
    return [
        root / relative
        for relative in sorted(tracked)
        if relative.startswith("architectures/patterns/")
        and PATTERN_FILE_RE.fullmatch(Path(relative).name)
    ]


def _tracked_profile_paths(root: Path, tracked: set[str]) -> list[Path]:
    return [root / relative for relative in sorted(tracked) if PROFILE_PATH_RE.fullmatch(relative)]


def _untracked_scope_population(root: Path, tracked: set[str]) -> bool:
    patterns = root / "architectures/patterns"
    if patterns.exists():
        for path in patterns.iterdir():
            if PATTERN_FILE_RE.fullmatch(path.name) and path.relative_to(root).as_posix() not in tracked:
                return True
    profiles = root / "profiles"
    if profiles.exists():
        for path in profiles.glob("*/*/profile.json"):
            if path.relative_to(root).as_posix() not in tracked:
                return True
    return False


def _https(value: object) -> bool:
    return isinstance(value, str) and value.startswith("https://")


def _load_baseline(root: Path, ref: str) -> dict[str, object]:
    result = subprocess.run(
        ["git", "show", f"{ref}:{RECORD_RELATIVE}"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    text = result.stdout
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("baseline record: YAML front matter is required")
    value = yaml.safe_load(text[4:text.index("\n---\n", 4)])
    if not isinstance(value, dict):
        raise ValueError("baseline record: front matter shall be a mapping")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("--baseline-ref")
    arguments = parser.parse_args(argv)
    root = Path.cwd().resolve()
    try:
        record = load_front_matter(root / RECORD_RELATIVE)
        errors = validate_record(root, record)
        phase = record.get("phase")
        if phase in PREVIOUS_PHASE and not arguments.baseline_ref:
            label = "closure candidate" if phase == "closure_candidate" else "published"
            errors.append(f"baseline-ref is required for {label}")
        elif arguments.baseline_ref:
            baseline = _load_baseline(root, arguments.baseline_ref)
            errors.extend(
                f"baseline record: {error}"
                for error in validate_record(root, baseline)
            )
            errors.extend(validate_transition(baseline, record))
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        errors = [f"release record could not be validated: {exc}"]
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
