#!/usr/bin/env python3
"""Validate the exact-candidate v0.18-draft publication readiness record."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import subprocess
import sys
from typing import Sequence

import yaml

RELEASE = "v0.18-draft"
TAG = "v0.18-draft"
MILESTONE = "v0.18-draft"
ISSUE = 224
RECORD_RELATIVE = "docs/superpowers/reviews/2026-10-07-v018-draft-publication-readiness.md"
GATE_IDS = ("scope", "integrated_case", "technical", "editorial", "terminology", "cross_reference_rendering", "standards_mapping", "repository_validation", "governance", "post_merge")
PHASE_GATE_STATES = {
    "evidence_candidate": {**{gate: "open" for gate in GATE_IDS}, "standards_mapping": "not_applicable"},
    "closure_candidate": {**{gate: "ready" for gate in GATE_IDS if gate not in {"post_merge", "standards_mapping"}}, "standards_mapping": "not_applicable", "post_merge": "open"},
    "published": {**{gate: "closed" for gate in GATE_IDS}, "standards_mapping": "not_applicable"},
}
PREVIOUS_PHASE = {"closure_candidate": "evidence_candidate", "published": "closure_candidate"}
HEADINGS = ("# v0.18-draft publication readiness", "## Scope", "## Mandatory gates", "## Lifecycle boundary", "## Publication evidence")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def load_readiness_document(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("YAML front matter is required")
    end = text.index("\n---\n", 4)
    value = yaml.safe_load(text[4:end])
    if not isinstance(value, dict):
        raise ValueError("front matter shall be a mapping")
    return value, text[end + 5:]


def validate_record(root: Path, record: dict) -> list[str]:
    errors: list[str] = []
    allowed = {"release", "phase", "tag", "milestone", "issue", "version_advanced", "deliverable", "qualified_crosswalk_review_required", "base_sha", "publication", "gates"}
    for key in sorted(set(record) - allowed): errors.append(f"unknown top-level key {key}")
    if record.get("release") != RELEASE: errors.append("release shall equal v0.18-draft")
    if record.get("tag") != TAG: errors.append("tag shall equal v0.18-draft")
    if record.get("milestone") != MILESTONE: errors.append("milestone shall equal v0.18-draft")
    if record.get("issue") != ISSUE: errors.append(f"issue shall equal {ISSUE}")
    if record.get("version_advanced") is not False: errors.append("version_advanced shall remain false until publication")
    if record.get("deliverable") != "one_fictional_summit_analytics_cap140_integrated_assessment_case": errors.append("deliverable shall identify the single integrated assessment case")
    if record.get("qualified_crosswalk_review_required") is not False: errors.append("qualified crosswalk review shall not be required")
    phase = record.get("phase")
    if not isinstance(phase, str) or phase not in PHASE_GATE_STATES:
        errors.append("phase shall be evidence_candidate, closure_candidate, or published")
    gates = record.get("gates")
    if not isinstance(gates, dict) or set(gates) != set(GATE_IDS):
        errors.append("gates shall contain the exact mandatory gate identifiers")
        return errors
    states = PHASE_GATE_STATES.get(phase, {}) if isinstance(phase, str) else {}
    for gate in GATE_IDS:
        item = gates[gate]
        if not isinstance(item, dict) or item.get("state") != states.get(gate):
            errors.append(f"{phase} phase shall set {gate} gate to {states.get(gate)!r}")
            continue
        evidence = item.get("evidence")
        if not isinstance(evidence, list): errors.append(f"{gate} evidence shall be a list")
        elif states[gate] in {"ready", "closed"} and gate != "standards_mapping" and not evidence:
            errors.append(f"{gate} evidence is required")
        elif any(not isinstance(url, str) or not url.startswith("https://") for url in evidence):
            errors.append(f"{gate} evidence shall use HTTPS locators")
    standards_mapping = gates.get("standards_mapping")
    if isinstance(standards_mapping, dict) and standards_mapping.get("state") != "not_applicable":
        errors.append("standards_mapping shall be explicitly not_applicable for this mapping-neutral milestone")
    publication = record.get("publication")
    if not isinstance(publication, dict): errors.append("publication shall be a mapping")
    else:
        if publication.get("condition") != "annotated_tag_targets_validated_closure_candidate": errors.append("publication condition is invalid")
        for key in ("tag_object", "tagged_commit", "date", "evidence"):
            value = publication.get(key)
            if phase != "published" and value not in (None, []): errors.append(f"candidate publication {key} shall be unset")
        if phase == "published":
            if not isinstance(publication.get("tag_object"), str) or not SHA_RE.fullmatch(publication["tag_object"]): errors.append("published tag_object shall be a 40-character SHA")
            if not isinstance(publication.get("tagged_commit"), str) or not SHA_RE.fullmatch(publication["tagged_commit"]): errors.append("published tagged_commit shall be a 40-character SHA")
            if not isinstance(publication.get("date"), str): errors.append("published date is required")
            else:
                try: date.fromisoformat(publication["date"])
                except ValueError: errors.append("published date shall be YYYY-MM-DD")
            publication_evidence = publication.get("evidence")
            if not isinstance(publication_evidence, list):
                errors.append("published publication evidence shall be a list")
            elif not publication_evidence:
                errors.append("published publication evidence is required")
            elif any(not isinstance(url, str) or not url.startswith("https://") for url in publication_evidence):
                errors.append("published publication evidence shall use HTTPS locators")
    return errors


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def validate_candidate_binding(root: Path, working_text: str) -> list[str]:
    """Bind readiness content to HEAD; unrelated dirty files are permitted."""
    try:
        result = subprocess.run(
            ["git", "show", f"HEAD:{RECORD_RELATIVE}"], cwd=root,
            capture_output=True, check=True,
        )
        committed = result.stdout.decode("utf-8")
        candidate_sha = _git(root, "rev-parse", "--verify", "HEAD^{commit}")
    except subprocess.CalledProcessError as exc:
        return [f"candidate HEAD readiness record could not be resolved: {exc}"]
    if not SHA_RE.fullmatch(candidate_sha):
        return ["candidate HEAD shall resolve to an exact commit SHA"]
    if committed != working_text:
        return ["working-tree readiness record differs from committed HEAD; commit it before validation"]
    return []


def validate_baseline_anchor(root: Path, baseline_ref: str) -> list[str]:
    """Verify the evidence-candidate base is an exact existing ancestor SHA."""
    try:
        resolved = _git(root, "rev-parse", "--verify", f"{baseline_ref}^{{commit}}")
        head = _git(root, "rev-parse", "--verify", "HEAD^{commit}")
    except subprocess.CalledProcessError as exc:
        return [f"baseline/candidate SHA could not be resolved: {exc}"]
    errors = []
    if not SHA_RE.fullmatch(baseline_ref) or resolved != baseline_ref:
        errors.append("base_sha shall resolve to the exact recorded 40-character SHA")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", baseline_ref, head],
        cwd=root, capture_output=True,
    )
    if ancestry.returncode != 0:
        errors.append("base_sha shall be an ancestor of candidate HEAD")
    return errors


def validate_baseline_from_record(root: Path, record: dict) -> list[str]:
    """Validate the record's bound baseline for its current release phase."""
    phase = record.get("phase")
    if not isinstance(phase, str):
        return ["phase shall be a string before record-bound baseline validation"]
    baseline_ref = record.get("base_sha")
    if not isinstance(baseline_ref, str) or not SHA_RE.fullmatch(baseline_ref):
        return ["readiness record base_sha shall be an exact 40-character SHA"]
    if phase in PREVIOUS_PHASE:
        return validate_transition(root, baseline_ref, record)
    return validate_baseline_anchor(root, baseline_ref)


def validate_transition(root: Path, baseline_ref: str, record: dict) -> list[str]:
    errors: list[str] = []
    phase = record.get("phase")
    if not isinstance(phase, str):
        return ["phase shall be a string before baseline transition validation"]
    expected = PREVIOUS_PHASE.get(phase)
    if not expected and phase != "published": return [f"phase {phase!r} does not support baseline-ref"]
    try:
        base_sha = _git(root, "rev-parse", "--verify", f"{baseline_ref}^{{commit}}")
        baseline_text = _git(root, "show", f"{base_sha}:{RECORD_RELATIVE}")
        baseline, _ = _frontmatter(baseline_text)
        head_sha = _git(root, "rev-parse", "--verify", "HEAD^{commit}")
    except (subprocess.CalledProcessError, ValueError) as exc:
        return [f"baseline/candidate SHA could not be resolved: {exc}"]
    if not SHA_RE.fullmatch(base_sha) or not SHA_RE.fullmatch(head_sha): errors.append("baseline and candidate shall be exact commit SHAs")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", base_sha, head_sha],
        cwd=root, capture_output=True,
    )
    if ancestry.returncode != 0:
        errors.append("exact baseline SHA shall be an ancestor of candidate HEAD")
    if phase == "published":
        if baseline.get("phase") not in {"closure_candidate", "published"}:
            errors.append("published shall transition only from closure_candidate or published")
    elif expected and baseline.get("phase") != expected:
        errors.append(f"{phase} shall transition only from {expected}")
    if record.get("base_sha") != base_sha: errors.append("base_sha shall equal the exact baseline commit SHA")
    if phase == "published" and baseline.get("phase") == "published":
        if baseline.get("publication") != record.get("publication") or baseline.get("gates") != record.get("gates"):
            errors.append("published publication identity and closed gate truth shall remain unchanged")
    if phase == "published" and baseline.get("phase") == "closure_candidate":
        publication = record.get("publication")
        if isinstance(publication, dict) and publication.get("tagged_commit") != base_sha:
            errors.append("first published tagged_commit shall equal the exact closure_candidate baseline SHA")
    if phase == "published":
        publication = record.get("publication", {})
        if not isinstance(publication, dict):
            return errors + ["publication shall be a mapping"]
        try:
            tag_object = _git(root, "rev-parse", "--verify", f"refs/tags/{TAG}")
            tagged_commit = _git(root, "rev-parse", "--verify", f"refs/tags/{TAG}^{{commit}}")
            tag_type = _git(root, "cat-file", "-t", tag_object)
            closure_text = _git(root, "show", f"{tagged_commit}:{RECORD_RELATIVE}")
            closure, _ = _frontmatter(closure_text)
            if tag_type != "tag": errors.append("publication tag shall be annotated")
            if tag_object != publication.get("tag_object"): errors.append("publication tag object is stale or mismatched")
            if tagged_commit != publication.get("tagged_commit"): errors.append("publication tagged commit is stale or mismatched")
            if closure.get("phase") != "closure_candidate": errors.append("annotated tag shall target the validated closure_candidate commit")
        except (subprocess.CalledProcessError, ValueError) as exc:
            errors.append(f"publication tag evidence cannot be verified: {exc}")
    return errors


def _frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]: raise ValueError("YAML front matter is required")
    end = text.index("\n---\n", 4)
    value = yaml.safe_load(text[4:end])
    if not isinstance(value, dict): raise ValueError("front matter shall be a mapping")
    return value, text[end + 5:]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    baseline = parser.add_mutually_exclusive_group()
    baseline.add_argument("--baseline-ref")
    baseline.add_argument("--baseline-ref-from-record", action="store_true")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        record, body = load_readiness_document(root / RECORD_RELATIVE)
        working_text = (root / RECORD_RELATIVE).read_text(encoding="utf-8")
        errors = [*validate_candidate_binding(root, working_text), *validate_record(root, record)]
        baseline_ref = args.baseline_ref
        if args.baseline_ref_from_record:
            errors.extend(validate_baseline_from_record(root, record))
            baseline_ref = None
        phase = record.get("phase")
        phase_requires_baseline = isinstance(phase, str) and phase in PREVIOUS_PHASE
        cursor = 0
        for heading in HEADINGS:
            pos = body.find(heading, cursor)
            if pos < 0: errors.append(f"readiness body is missing required heading: {heading}")
            else: cursor = pos + len(heading)
        if phase_requires_baseline and not baseline_ref and not args.baseline_ref_from_record:
            errors.append("baseline-ref is required for a phase transition")
        elif baseline_ref and phase_requires_baseline:
            errors.extend(validate_transition(root, baseline_ref, record))
        elif baseline_ref and isinstance(phase, str):
            errors.extend(validate_baseline_anchor(root, baseline_ref))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors = [f"release record could not be validated: {exc}"]
    for error in errors: print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__": raise SystemExit(main())
