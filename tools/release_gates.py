#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

import yaml

GATE_IDS = (
    "scope",
    "technical",
    "editorial",
    "cross_reference_rendering",
    "standards_mapping",
    "release_metadata",
    "governance",
    "post_merge",
)
STATES = {"open", "in_review", "ready", "closed"}
ALLOWED_TRANSITIONS = {
    "open": {"open", "in_review", "ready"},
    "in_review": {"open", "in_review", "ready"},
    "ready": {"open", "in_review", "ready", "closed"},
    "closed": {"open", "in_review", "closed"},
}
EXPECTED_MAPPING_SETS = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
)
PUBLICATION_CONDITION = "remote_annotated_tag_matches_exact_validated_commit"
SHA_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", re.IGNORECASE)
POST_MERGE_COMMANDS = (
    "full_suite",
    "controls",
    "architectures",
    "migration",
    "crosswalk_current",
    "crosswalk_baseline",
    "links",
    "release_record",
    "mermaid_inventory",
    "whole_range_diff",
    "cache_count",
    "clean_status",
)
REPOSITORY_SCOPE = "complete_git_tracked_repository"
REQUIRED_SCOPE_INPUTS = (
    "VERSION.md",
    "project/RELEASE_PLAN.md",
    "crosswalks/catalog.json",
)
RELEASE_PLAN_MARKERS = (
    "## 0.4-alpha readiness",
    "Architecture content is complete only at Draft level. Publication gates remain Open.",
    "0.4-alpha shall not be tagged or represented as released.",
)


def load_front_matter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path}: YAML front matter is required")
    payload = text[4:text.index("\n---\n", 4)]
    value = yaml.safe_load(payload)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: front matter shall be a mapping")
    return value


def flattened_items(value: object, prefix: str = ""):
    if prefix:
        yield prefix, value
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            yield from flattened_items(child, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from flattened_items(child, f"{prefix}[{index}]")


def _date_text(value: object) -> str | None:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value if isinstance(value, str) else None


def _tracked_paths(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True,
        capture_output=True,
    )
    return {path for path in result.stdout.decode("utf-8").split("\0") if path}


def validate_record(root: Path, record: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if record.get("release") != "0.4-alpha":
        errors.append("release shall equal 0.4-alpha")
    if record.get("tag") != "v0.4-alpha":
        errors.append("tag shall equal v0.4-alpha")
    if record.get("issue") != 39:
        errors.append("issue shall equal 39")
    if record.get("repository_scope") != REPOSITORY_SCOPE:
        errors.append("repository scope shall equal complete_git_tracked_repository")
    if record.get("phase") not in {"evidence_candidate", "closure_candidate"}:
        errors.append("phase shall be evidence_candidate or closure_candidate")
    publication = record.get("publication")
    if not isinstance(publication, dict) or publication.get("condition") != PUBLICATION_CONDITION:
        errors.append("publication condition is invalid")
    elif record.get("phase") == "evidence_candidate" and publication.get("date") is not None:
        errors.append("evidence candidate shall not have a publication date")
    elif record.get("phase") == "closure_candidate" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", _date_text(publication.get("date")) or ""):
        errors.append("closure candidate shall have an ISO publication date")
    version = (root / "VERSION.md").read_text(encoding="utf-8")
    if "Current Version: **0.4-alpha**" not in version or "Status: **Working Draft**" not in version:
        errors.append("VERSION.md current version shall equal 0.4-alpha")
    release_plan = (root / "project/RELEASE_PLAN.md").read_text(encoding="utf-8")
    if not all(marker in release_plan for marker in RELEASE_PLAN_MARKERS):
        errors.append("project/RELEASE_PLAN.md shall preserve the 0.4-alpha Draft release plan")
    try:
        if not set(REQUIRED_SCOPE_INPUTS).issubset(_tracked_paths(root)):
            errors.append("required release-scope inputs shall be Git-tracked")
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        errors.append("repository scope cannot be verified from Git-tracked files")
    if tuple(sorted(record.get("mapping_sets", []))) != tuple(sorted(EXPECTED_MAPPING_SETS)):
        errors.append("mapping_sets shall equal the three unique Draft snapshots")
    gates = record.get("gates")
    if not isinstance(gates, dict) or tuple(gates) != GATE_IDS:
        errors.append("gates shall contain the exact ordered gate identifiers")
    else:
        for gate_id, gate in gates.items():
            if not isinstance(gate, dict) or gate.get("state") not in STATES:
                errors.append(f"{gate_id}: invalid gate state")
                continue
            evidence = gate.get("evidence")
            if not isinstance(evidence, list):
                errors.append(f"{gate_id}: evidence shall be a list")
            elif gate["state"] in {"ready", "closed"} and not evidence:
                errors.append(f"{gate_id}: {gate['state']} gate requires evidence")
            elif gate["state"] in {"ready", "closed"} and any(not _https(locator) for locator in evidence):
                errors.append(f"{gate_id}: evidence shall contain HTTPS locators")
    for path, value in flattened_items(record):
        if "sha" in path.casefold() or "commit" in path.casefold():
            errors.append(f"{path}: tracked record shall not contain SHA fields")
        if isinstance(value, str) and SHA_RE.search(value):
            errors.append(f"{path}: tracked record shall not contain a 40-character SHA")
    catalog = json.loads((root / "crosswalks/catalog.json").read_text(encoding="utf-8"))
    identifiers = tuple(item["metadata"]["mapping_set_id"] for item in catalog["mapping_sets"])
    if tuple(sorted(identifiers)) != tuple(sorted(EXPECTED_MAPPING_SETS)):
        errors.append("catalog mapping sets differ from the release scope")
    if any(item["metadata"]["status"] != "draft" for item in catalog["mapping_sets"]):
        errors.append("every in-scope mapping set shall remain draft")
    return errors


def validate_transition(previous: dict[str, object], candidate: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for gate_id in GATE_IDS:
        previous_gates = previous.get("gates")
        candidate_gates = candidate.get("gates")
        before_gate = previous_gates.get(gate_id) if isinstance(previous_gates, dict) else None
        after_gate = candidate_gates.get(gate_id) if isinstance(candidate_gates, dict) else None
        if not isinstance(before_gate, dict) or not isinstance(after_gate, dict):
            errors.append(f"{gate_id}: transition requires valid gate records")
            continue
        before = before_gate.get("state")
        after = after_gate.get("state")
        if before not in ALLOWED_TRANSITIONS or after not in STATES:
            errors.append(f"{gate_id}: transition requires valid gate states")
        elif after not in ALLOWED_TRANSITIONS[before]:
            errors.append(f"{gate_id}: illegal transition {before} -> {after}")
    return errors


def _https(value: object) -> bool:
    return isinstance(value, str) and value.startswith("https://")


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _candidate_verdict(
    errors: list[str], name: str, value: object, closure_head: object, *, scope: bool = False,
    governance: bool = False,
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{name} approval is required")
        return
    if value.get("sha") != closure_head:
        errors.append(f"{name} approval is not bound to closure head")
    identity_field = "approver" if scope or governance else "reviewer"
    identity = value.get(identity_field)
    if not isinstance(identity, str) or not identity.strip():
        errors.append(f"{name} {identity_field} shall be named")
    if scope:
        role = value.get("role")
        if not isinstance(role, str) or not role.strip():
            errors.append("scope role shall be named")
    if value.get("date") != _today():
        errors.append(f"{name} approval date shall equal current UTC date")
    if value.get("disposition") != "approved":
        errors.append(f"{name} disposition shall be approved")
    if not _https(value.get("url")):
        errors.append(f"{name} URL shall use HTTPS")
    if not scope and not governance:
        if value.get("critical") != 0:
            errors.append(f"{name} Critical findings shall be zero")
        if value.get("important") != 0:
            errors.append(f"{name} Important findings shall be zero")


def validate_external_evidence(
    record: dict[str, object], evidence: dict[str, object], expected_head: str, phase: str,
) -> list[str]:
    errors: list[str] = []
    if phase not in {"closure", "taggable"}:
        return ["phase shall be closure or taggable"]
    if record.get("phase") != "closure_candidate":
        errors.append("record phase shall be closure_candidate")
    publication = record.get("publication")
    if not isinstance(publication, dict) or publication.get("condition") != PUBLICATION_CONDITION:
        errors.append("publication condition is invalid")
    elif _date_text(publication.get("date")) != _today():
        errors.append("conditional publication date shall equal current UTC date")
    gates = record.get("gates")
    if not isinstance(gates, dict):
        errors.append("record gates are invalid")
    else:
        for gate_id in GATE_IDS:
            gate = gates.get(gate_id)
            if not isinstance(gate, dict) or gate.get("state") not in {"ready", "closed"}:
                errors.append(f"{gate_id} gate is not ready for closure")

    closure_head = evidence.get("closure_head")
    if not isinstance(closure_head, str) or not SHA_RE.fullmatch(closure_head):
        errors.append("closure head shall be a 40-character SHA")
    if not isinstance(expected_head, str) or not SHA_RE.fullmatch(expected_head):
        errors.append("expected head shall be a 40-character SHA")
    if phase == "closure" and expected_head != closure_head:
        errors.append("expected head is not bound to closure head")
    if phase == "closure" and ("merge_head" in evidence or "post_merge" in evidence):
        errors.append("closure evidence shall not contain merge evidence")
    if phase == "taggable":
        if not isinstance(evidence.get("merge_head"), str) or not SHA_RE.fullmatch(evidence["merge_head"]):
            errors.append("merge head shall be a 40-character SHA")
        if evidence.get("merge_head") != expected_head:
            errors.append("merge head is not bound to expected head")

    _candidate_verdict(errors, "scope", evidence.get("scope"), closure_head, scope=True)
    for name in ("technical", "editorial", "rendering"):
        _candidate_verdict(errors, name, evidence.get(name), closure_head)
    _candidate_verdict(errors, "governance", evidence.get("governance"), closure_head, governance=True)
    governance = evidence.get("governance")
    if isinstance(governance, dict):
        if governance.get("authority") != "Steering Committee":
            errors.append("governance authority is not authorized")

    mapping_reviews = evidence.get("mapping_reviews")
    if not isinstance(mapping_reviews, list):
        errors.append("three qualified mapping reviews are required")
    else:
        if len(mapping_reviews) != len(EXPECTED_MAPPING_SETS):
            errors.append("three qualified mapping reviews are required")
        identifiers = [review.get("mapping_set_id") for review in mapping_reviews if isinstance(review, dict)]
        if sorted(identifiers) != sorted(EXPECTED_MAPPING_SETS):
            errors.append("mapping reviews shall contain each expected mapping set exactly once")
        for review in mapping_reviews:
            if not isinstance(review, dict):
                errors.append("mapping review shall be an object")
                continue
            if review.get("sha") != closure_head:
                errors.append("mapping review is not bound to closure head")
            if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
                errors.append("mapping reviewer shall be named")
            if not isinstance(review.get("qualification"), str) or not review["qualification"].strip():
                errors.append("mapping reviewer shall be qualified")
            if review.get("date") != _today():
                errors.append("mapping review date shall equal current UTC date")
            if review.get("disposition") != "approved":
                errors.append("mapping review disposition shall be approved")
            if not _https(review.get("url")):
                errors.append("mapping review URL shall use HTTPS")

    checks = evidence.get("github_checks")
    if not isinstance(checks, dict):
        errors.append("GitHub checks are required")
    else:
        expected = checks.get("expected")
        observed = checks.get("observed")
        if expected != ["Validate ESAF sources"]:
            errors.append("expected GitHub checks shall equal required checks")
        if not isinstance(observed, list) or len(observed) != 1 or not all(isinstance(item, dict) for item in observed) or [item.get("name") for item in observed] != ["Validate ESAF sources"]:
            errors.append("observed GitHub checks shall exactly match expected checks")
        else:
            check = observed[0]
            if check.get("sha") != closure_head:
                errors.append("GitHub check is not bound to closure head")
            if check.get("conclusion") != "success":
                errors.append("GitHub check conclusion shall be success")
            if not _https(check.get("url")):
                errors.append("GitHub check URL shall use HTTPS")

    merge_state = evidence.get("merge_state")
    if not isinstance(merge_state, dict):
        errors.append("merge state is required")
    else:
        if merge_state.get("sha") != closure_head:
            errors.append("merge state is not bound to closure head")
        if merge_state.get("mergeable") is not True:
            errors.append("merge state shall be mergeable")
        if merge_state.get("state") != "clean":
            errors.append("merge state shall be clean")

    if phase == "taggable":
        post_merge = evidence.get("post_merge")
        if not isinstance(post_merge, dict):
            errors.append("post-merge evidence is required")
        else:
            if not isinstance(post_merge.get("sha"), str) or not SHA_RE.fullmatch(post_merge["sha"]):
                errors.append("post-merge head shall be a 40-character SHA")
            if post_merge.get("sha") != expected_head:
                errors.append("post-merge evidence is not bound to merge head")
            commands = post_merge.get("commands")
            command_names = [command.get("name") for command in commands] if isinstance(commands, list) and all(isinstance(command, dict) for command in commands) else []
            if not isinstance(commands, list) or len(commands) != len(POST_MERGE_COMMANDS) or set(command_names) != set(POST_MERGE_COMMANDS):
                errors.append("post-merge commands shall contain each required command exactly once")
            else:
                for command in commands:
                    name = command["name"]
                    if command.get("exit_code") != 0:
                        errors.append(f"{name} command failed")
                    if not isinstance(command.get("result"), str) or not command["result"].strip():
                        errors.append(f"{name} command result shall be nonempty")
    return errors


def _load_baseline(root: Path, ref: str) -> dict[str, object]:
    relative = "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
    result = subprocess.run(
        ["git", "show", f"{ref}:{relative}"], cwd=root, check=True,
        capture_output=True, text=True,
    )
    text = result.stdout
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("baseline record: YAML front matter is required")
    value = yaml.safe_load(text[4:text.index("\n---\n", 4)])
    if not isinstance(value, dict):
        raise ValueError("baseline record: front matter shall be a mapping")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the 0.4-alpha release-gate contract.")
    parser.add_argument("--check", action="store_true", help="validate without changing files")
    parser.add_argument("--baseline-ref")
    parser.add_argument("--external-evidence", type=Path)
    parser.add_argument("--expected-head")
    parser.add_argument("--phase", choices=("closure", "taggable"))
    args = parser.parse_args(argv)
    if not args.check:
        parser.error("--check is required")
    if args.external_evidence and (not args.expected_head or not args.phase):
        parser.error("--external-evidence requires --expected-head and --phase")
    if (args.expected_head or args.phase) and not args.external_evidence:
        parser.error("--expected-head and --phase require --external-evidence")

    root = Path(__file__).resolve().parents[1]
    record_path = root / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
    record = load_front_matter(record_path)
    errors = validate_record(root, record)
    if record.get("phase") == "closure_candidate" and not args.baseline_ref:
        errors.append("baseline-ref is required for closure candidate")
    if args.baseline_ref:
        try:
            errors.extend(validate_transition(_load_baseline(root, args.baseline_ref), record))
        except (OSError, subprocess.CalledProcessError, ValueError) as exc:
            if record.get("phase") != "evidence_candidate" or args.phase in {"closure", "taggable"}:
                errors.append(f"baseline record could not be loaded: {exc}")
    if args.external_evidence:
        try:
            evidence = json.loads(args.external_evidence.read_text(encoding="utf-8"))
            if not isinstance(evidence, dict):
                raise ValueError("external evidence shall be a JSON object")
            errors.extend(validate_external_evidence(record, evidence, args.expected_head, args.phase))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"external evidence could not be loaded: {exc}")
    for error in errors:
        print(error)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
