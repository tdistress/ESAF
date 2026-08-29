#!/usr/bin/env python3
"""Validate the v0.9-rc1 publication-readiness record contract (Issue #95).

Supports ``evidence_candidate``, ``closure_candidate``, and ``published``
phases, including ``--baseline-ref`` previous-phase and closure-allowlist
checks. ``tools/release_gates.py`` and ``tools/v05_beta_release_gates.py``
remain frozen historical validators.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Sequence

import yaml

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


RELEASE = "0.9-rc1"
TAG = "v0.9-rc1"
ISSUE = 95
RECORD_RELATIVE = (
    "docs/superpowers/reviews/2026-08-29-v09-rc1-publication-readiness.md"
)
REPOSITORY_SCOPE = "complete_git_tracked_repository"
PUBLICATION_CONDITION = "remote_annotated_tag_matches_exact_validated_commit"

CLOSURE_ALLOWLIST = (
    "VERSION.md",
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "project/RELEASE_PLAN.md",
    RECORD_RELATIVE,
)

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
PREVIOUS_PHASE = {
    "closure_candidate": "evidence_candidate",
    "published": "closure_candidate",
}

ALLOWED_TOP_LEVEL_KEYS = {
    "release",
    "phase",
    "tag",
    "issue",
    "repository_scope",
    "publication",
    "prerequisite_dispositions",
    "scope",
    "gates",
}
ALLOWED_PUBLICATION_KEYS = {
    "date",
    "condition",
    "evidence",
    "tag_object",
    "tagged_commit",
    "issue_evidence_url",
}
ALLOWED_GATE_KEYS = {"state", "evidence"}

# (disposition key, expected disposition value, evidence-path key, accepted markers)
PREREQUISITE_SPECS = (
    ("phase2_timing", "DEFER", "phase2_evidence", ("DEFER",)),
    ("esaf_1300", "working_draft", "esaf_1300_path", ("Working Draft",)),
    ("esaf_1400", "working_draft", "esaf_1400_path", ("Working Draft",)),
    ("esaf_1700", "working_draft", "esaf_1700_path", ("Working Draft",)),
    ("nist_ai_rmf", "HOLD", "nist_ai_rmf_path", ("Readiness HOLD", "`HOLD`")),
)
PREREQUISITE_KEYS = frozenset(
    key for spec in PREREQUISITE_SPECS for key in (spec[0], spec[2])
)

CONTROLS_CATALOG_RELATIVE = "controls/catalog.json"
CROSSWALKS_CATALOG_RELATIVE = "crosswalks/catalog.json"
ASSESSMENT_FOUNDATION_RELATIVE = "assessment/ESAF-1500.md"
DRAFT_PROFILE_RELATIVE = "profiles/uk/0.1.0/profile.json"
PCI_DSS_MATRIX_RELATIVE = (
    "docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json"
)
NIST_AI_RMF_MATRIX_RELATIVE = (
    "docs/superpowers/specs/2026-08-29-nist-ai-rmf-mapping-readiness-matrix.json"
)
ARCHITECTURE_PATTERNS_PREFIX = "architectures/patterns/"
ARCHITECTURE_PATTERN_FILE_RE = re.compile(r"ARC-P[1-9][0-9]{2}\.md$")

REQUIRED_HEADINGS = (
    "# v0.9-rc1 publication readiness",
    "## Scope",
    "## Prerequisite dispositions",
    "## Lifecycle boundary",
    "## Nonclaims",
    "## Publication evidence",
)


def _front_matter_parts(text: str, label: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{label}: YAML front matter is required")
    boundary = text.index("\n---\n", 4)
    value = yaml.safe_load(text[4:boundary])
    if not isinstance(value, dict):
        raise ValueError(f"{label}: front matter shall be a mapping")
    return value, text[boundary + len("\n---\n") :]


def load_front_matter(path: Path) -> dict[str, object]:
    """Load the YAML front matter from one readiness record."""
    text = path.read_text(encoding="utf-8")
    value, _ = _front_matter_parts(text, str(path))
    return value


def load_readiness_document(path: Path) -> tuple[dict[str, object], str]:
    """Load the readiness record front matter and normative Markdown body."""
    return _front_matter_parts(path.read_text(encoding="utf-8"), str(path))


def _tracked_paths(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
    )
    return {path for path in result.stdout.decode("utf-8").split("\0") if path}


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON object is required")
    return value


def _assessment_foundation(root: Path, tracked: set[str]) -> bool:
    if ASSESSMENT_FOUNDATION_RELATIVE not in tracked:
        return False
    return (root / ASSESSMENT_FOUNDATION_RELATIVE).is_file()


def _draft_profile_count(root: Path, tracked: set[str]) -> int:
    if DRAFT_PROFILE_RELATIVE not in tracked:
        return 0
    return 1 if (root / DRAFT_PROFILE_RELATIVE).is_file() else 0


def derive_scope(root: Path) -> dict[str, object]:
    """Derive the v0.9-rc1 release scope from live, Git-tracked catalogs."""
    tracked = _tracked_paths(root)
    controls = _load_json(root / CONTROLS_CATALOG_RELATIVE)
    crosswalks = _load_json(root / CROSSWALKS_CATALOG_RELATIVE)
    counts = crosswalks.get("counts")
    if not isinstance(counts, dict):
        raise ValueError("crosswalk catalog counts are missing")
    families = controls.get("families")
    if not isinstance(families, dict):
        raise ValueError("control catalog families are missing")
    pattern_files = [
        path
        for path in tracked
        if path.startswith(ARCHITECTURE_PATTERNS_PREFIX)
        and ARCHITECTURE_PATTERN_FILE_RE.search(path)
    ]
    pci_matrix = _load_json(root / PCI_DSS_MATRIX_RELATIVE)
    nist_matrix = _load_json(root / NIST_AI_RMF_MATRIX_RELATIVE)
    return {
        "controls": controls.get("control_count"),
        "control_families": len(families),
        "architecture_patterns": len(pattern_files),
        "mapping_sets": counts.get("mapping_sets"),
        "mapping_provisions": counts.get("provisions"),
        "relationship_legs": counts.get("relationships"),
        "negative_dispositions": counts.get("negative_dispositions"),
        "assessment_foundation": _assessment_foundation(root, tracked),
        "draft_profiles": _draft_profile_count(root, tracked),
        "pci_dss_disposition": pci_matrix.get("recorded_decision"),
        "nist_ai_rmf_disposition": nist_matrix.get("recorded_decision"),
    }


def _https(value: object) -> bool:
    return isinstance(value, str) and value.startswith("https://")


def _sha(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdefABCDEF" for character in value)
    )


def _validate_publication(errors: list[str], phase: object, publication: object) -> None:
    if not isinstance(publication, dict) or set(publication) != ALLOWED_PUBLICATION_KEYS:
        errors.append("publication keys are invalid")
        return
    if publication.get("condition") != PUBLICATION_CONDITION:
        errors.append("publication condition is invalid")
    if phase in {"evidence_candidate", "closure_candidate"}:
        for field in ("tag_object", "tagged_commit", "issue_evidence_url"):
            if publication.get(field) is not None:
                errors.append(f"candidate publication {field} shall be null")
        if phase == "evidence_candidate":
            if publication.get("date") is not None:
                errors.append("evidence candidate publication date shall be null")
            if publication.get("evidence") != []:
                errors.append("evidence candidate publication evidence shall be empty")
        elif phase == "closure_candidate":
            date_value = publication.get("date")
            if date_value is not None and (
                not isinstance(date_value, str) or not DATE_RE.fullmatch(date_value)
            ):
                errors.append(
                    "closure candidate publication date shall be YYYY-MM-DD or null"
                )
            evidence = publication.get("evidence")
            if not isinstance(evidence, list):
                errors.append("closure candidate publication evidence shall be a list")
            elif any(not _https(locator) for locator in evidence):
                errors.append(
                    "closure candidate publication evidence shall use HTTPS locators"
                )
    elif phase == "published":
        date_value = publication.get("date")
        if not isinstance(date_value, str) or not DATE_RE.fullmatch(date_value):
            errors.append("published publication date shall be YYYY-MM-DD")
        if not _sha(publication.get("tag_object")):
            errors.append("published tag object shall be a 40-character SHA")
        if not _sha(publication.get("tagged_commit")):
            errors.append("published tagged commit shall be a 40-character SHA")
        if not _https(publication.get("issue_evidence_url")):
            errors.append("published issue evidence URL shall be an HTTPS locator")
        evidence = publication.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append("published publication evidence is required")
        elif any(not _https(locator) for locator in evidence):
            errors.append("published publication evidence shall use HTTPS locators")


def _validate_prerequisites(errors: list[str], root: Path, value: object) -> None:
    if not isinstance(value, dict) or set(value) != PREREQUISITE_KEYS:
        errors.append("prerequisite_dispositions keys are invalid")
        return
    for disposition_key, expected_value, path_key, markers in PREREQUISITE_SPECS:
        if value.get(disposition_key) != expected_value:
            errors.append(
                f"prerequisite_dispositions.{disposition_key} shall equal "
                f"{expected_value!r}"
            )
        relative_path = value.get(path_key)
        if not isinstance(relative_path, str) or not relative_path:
            errors.append(f"prerequisite_dispositions.{path_key} is required")
            continue
        evidence_path = root / relative_path
        if not evidence_path.is_file():
            errors.append(
                f"prerequisite_dispositions.{path_key} does not exist: "
                f"{relative_path}"
            )
            continue
        text = evidence_path.read_text(encoding="utf-8")
        if not any(marker in text for marker in markers):
            errors.append(
                f"prerequisite_dispositions.{path_key} is missing a required "
                f"disposition marker: {' or '.join(markers)}"
            )


def _validate_scope(errors: list[str], root: Path, value: object) -> None:
    try:
        expected = derive_scope(root)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors.append(f"repository scope cannot be derived: {exc}")
        return
    if value != expected:
        errors.append("scope shall equal the derived repository scope")


def _validate_gates(errors: list[str], phase: object, gates: object) -> None:
    if not isinstance(gates, dict):
        errors.append("gates shall contain the exact gate identifiers")
        return
    unknown = sorted(set(gates) - set(GATE_IDS))
    for gate in unknown:
        errors.append(f"unknown gate {gate}")
    expected_states = PHASE_GATE_STATES.get(phase, {})
    for gate in GATE_IDS:
        item = gates.get(gate)
        if not isinstance(item, dict):
            errors.append(f"missing gate {gate}")
            continue
        unknown_keys = sorted(set(item) - ALLOWED_GATE_KEYS)
        for key in unknown_keys:
            errors.append(f"{gate}: unknown gate key {key}")
        expected = expected_states.get(gate)
        if item.get("state") != expected:
            errors.append(f"{phase} phase shall set {gate} gate to {expected!r}")
        evidence = item.get("evidence")
        if not isinstance(evidence, list):
            errors.append(f"{gate}: evidence shall be a list")
        elif item.get("state") in {"ready", "closed"} and not evidence:
            errors.append(f"{gate}: evidence is required")
        elif any(not _https(locator) for locator in evidence):
            errors.append(f"{gate}: evidence shall use HTTPS locators")


def validate_record(root: Path, record: dict[str, object]) -> list[str]:
    """Return deterministic diagnostics for an in-memory v0.9-rc1 record."""
    errors: list[str] = []
    unknown = sorted(set(record) - ALLOWED_TOP_LEVEL_KEYS)
    for key in unknown:
        errors.append(f"unknown top-level key {key}")
    if record.get("release") != RELEASE:
        errors.append(f"release shall equal {RELEASE}")
    if record.get("tag") != TAG:
        errors.append(f"tag shall equal {TAG}")
    if record.get("issue") != ISSUE:
        errors.append(f"issue shall equal {ISSUE}")
    if record.get("repository_scope") != REPOSITORY_SCOPE:
        errors.append(
            "repository scope shall equal complete_git_tracked_repository"
        )

    phase = record.get("phase")
    if phase not in PHASE_GATE_STATES:
        errors.append(
            "phase shall be evidence_candidate, closure_candidate, or published"
        )
    _validate_publication(errors, phase, record.get("publication"))
    _validate_prerequisites(errors, root, record.get("prerequisite_dispositions"))
    _validate_scope(errors, root, record.get("scope"))
    _validate_gates(errors, phase, record.get("gates"))
    return errors


def validate_readiness_body(body: str) -> list[str]:
    """Require the required v0.9-rc1 readiness body headings in order."""
    errors: list[str] = []
    cursor = 0
    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        index = body.find(heading, cursor)
        if index == -1:
            errors.append(f"readiness body is missing required heading: {heading}")
            continue
        positions.append(index)
        cursor = index + len(heading)
    if positions != sorted(positions):
        errors.append("readiness body headings shall appear in the required order")
    return errors


def _git_show_text(root: Path, ref: str, relative_path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{relative_path}"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return result.stdout.decode("utf-8")


def changed_paths_since(root: Path, baseline_ref: str) -> set[str]:
    """Return path names changed between baseline_ref and HEAD."""
    result = subprocess.run(
        ["git", "diff", "--name-only", baseline_ref, "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return {
        path
        for path in result.stdout.decode("utf-8").splitlines()
        if path.strip()
    }


def validate_baseline_transition(
    root: Path,
    *,
    baseline_ref: str,
    candidate_phase: object,
    candidate_record: dict[str, object],
) -> list[str]:
    """Validate previous-phase ancestry and the closure allowlist."""
    errors: list[str] = []
    expected_previous = PREVIOUS_PHASE.get(candidate_phase)  # type: ignore[arg-type]
    if expected_previous is None:
        errors.append(f"phase {candidate_phase!r} does not support baseline-ref")
        return errors
    try:
        baseline_text = _git_show_text(root, baseline_ref, RECORD_RELATIVE)
        baseline_record, _ = _front_matter_parts(
            baseline_text, f"{baseline_ref}:{RECORD_RELATIVE}"
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        return [f"baseline readiness record could not be loaded: {exc}"]
    if baseline_record.get("phase") != expected_previous:
        errors.append(
            f"{candidate_phase} shall transition only from {expected_previous}"
        )
    if candidate_phase in {"closure_candidate", "published"}:
        changed = changed_paths_since(root, baseline_ref)
        disallowed = sorted(changed - set(CLOSURE_ALLOWLIST))
        for path in disallowed:
            errors.append(
                f"{candidate_phase} baseline diff includes non-allowlist path: {path}"
            )
    # Keep candidate identity fields stable across the transition.
    for field in ("release", "tag", "issue", "repository_scope"):
        if baseline_record.get(field) != candidate_record.get(field):
            errors.append(
                f"{candidate_phase} shall preserve {field} from the baseline record"
            )
    return errors


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument(
        "--baseline-ref",
        help=(
            "previous-phase readiness baseline for closure_candidate/published "
            "transition and allowlist checks; ignored for evidence_candidate"
        ),
    )
    arguments = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        record, body = load_readiness_document(root / RECORD_RELATIVE)
        errors = [*validate_record(root, record), *validate_readiness_body(body)]
        phase = record.get("phase")
        if phase in PREVIOUS_PHASE and not arguments.baseline_ref:
            label = (
                "closure candidate"
                if phase == "closure_candidate"
                else "published"
            )
            errors.append(f"baseline-ref is required for {label}")
        elif arguments.baseline_ref and phase in PREVIOUS_PHASE:
            errors.extend(
                validate_baseline_transition(
                    root,
                    baseline_ref=arguments.baseline_ref,
                    candidate_phase=phase,
                    candidate_record=record,
                )
            )
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        errors = [f"release record could not be validated: {exc}"]
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
