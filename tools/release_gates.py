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
MAPPING_DECISION_SCHEMA = "esaf-mapping-decisions-v1"
MAPPING_DECISION_BASES = {"qualified_approval", "owner_risk_acceptance"}
CLAIMS_NOT_MADE = {
    "compliance",
    "certification",
    "equivalence",
    "endorsement",
    "external_scheme_approval",
    "assurance",
    "production_readiness",
}
OWNER_REPOSITORY = "tdistress/ESAF"
OWNER_LOGIN = "tdistress"
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
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
PUBLISHED_DATE = "2026-07-23"
PUBLISHED_TAG_OBJECT = "2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f"
PUBLISHED_COMMIT = "8abfe5a85db19d11295a0c3debeb2d58109b0ca7"
PUBLISHED_EVIDENCE = (
    "https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764"
)
PUBLISHED_SHA_PATHS = {
    "publication.tag_object": PUBLISHED_TAG_OBJECT,
    "publication.tagged_commit": PUBLISHED_COMMIT,
}
PUBLISHED_RELEASE_PLAN_MARKERS = (
    "## 0.4-alpha publication",
    "Publication gates are Closed.",
    PUBLISHED_EVIDENCE,
    PUBLISHED_COMMIT,
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


def _rfc3339(value: object) -> datetime | None:
    if not isinstance(value, str) or not RFC3339_RE.fullmatch(value):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _publication_date(record: dict[str, object]) -> str | None:
    publication = record.get("publication")
    return _date_text(publication.get("date")) if isinstance(publication, dict) else None


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
    phase = record.get("phase")
    if phase not in {"evidence_candidate", "closure_candidate", "published"}:
        errors.append(
            "phase shall be evidence_candidate, closure_candidate, or published"
        )
    publication = record.get("publication")
    if not isinstance(publication, dict) or publication.get("condition") != PUBLICATION_CONDITION:
        errors.append("publication condition is invalid")
    elif phase == "evidence_candidate" and publication.get("date") is not None:
        errors.append("evidence candidate shall not have a publication date")
    elif phase == "closure_candidate" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", _date_text(publication.get("date")) or ""):
        errors.append("closure candidate shall have an ISO publication date")
    elif phase == "published":
        if _date_text(publication.get("date")) != PUBLISHED_DATE:
            errors.append("published date shall equal 2026-07-23")
        if publication.get("tag_object") != PUBLISHED_TAG_OBJECT:
            errors.append("published tag object is invalid")
        if publication.get("tagged_commit") != PUBLISHED_COMMIT:
            errors.append("published tagged commit is invalid")
        if publication.get("evidence") != PUBLISHED_EVIDENCE:
            errors.append("published evidence locator is invalid")
    if phase == "closure_candidate" and record.get("mapping_decision_basis") not in MAPPING_DECISION_BASES:
        errors.append("closure candidate mapping_decision_basis shall be supported")
    if phase == "published" and record.get("mapping_decision_basis") != "owner_risk_acceptance":
        errors.append(
            "published mapping_decision_basis shall equal owner_risk_acceptance"
        )
    version = (root / "VERSION.md").read_text(encoding="utf-8")
    if "Current Version: **0.4-alpha**" not in version or "Status: **Working Draft**" not in version:
        errors.append("VERSION.md current version shall equal 0.4-alpha")
    release_plan = (root / "project/RELEASE_PLAN.md").read_text(encoding="utf-8")
    release_plan_markers = (
        PUBLISHED_RELEASE_PLAN_MARKERS if phase == "published" else RELEASE_PLAN_MARKERS
    )
    if not all(marker in release_plan for marker in release_plan_markers):
        if phase == "published":
            errors.append("project/RELEASE_PLAN.md shall preserve the 0.4-alpha published release plan")
        else:
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
            if phase == "published" and gate["state"] != "closed":
                errors.append(f"{gate_id}: published gate shall be closed")
    for path, value in flattened_items(record):
        if phase == "published" and path in PUBLISHED_SHA_PATHS:
            if value != PUBLISHED_SHA_PATHS[path]:
                errors.append(f"{path}: published identifier is invalid")
            continue
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


def _owner_comment_url(value: object, comment_id: object) -> bool:
    return (
        isinstance(value, str)
        and isinstance(comment_id, int)
        and not isinstance(comment_id, bool)
        and re.fullmatch(
            rf"https://github\.com/{re.escape(OWNER_REPOSITORY)}/(?:issues|pull)/\d+#issuecomment-{comment_id}",
            value,
        ) is not None
    )


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


def _validate_limitations(errors: list[str], value: object, prefix: str) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix} limitations are required")
        return
    if value.get("lifecycle") != "draft":
        errors.append(f"{prefix} lifecycle shall equal draft")
    claims = value.get("claims_not_made")
    if (
        not isinstance(claims, list)
        or len(claims) != len(CLAIMS_NOT_MADE)
        or any(not isinstance(claim, str) for claim in claims)
        or len(set(claims)) != len(claims)
        or set(claims) != CLAIMS_NOT_MADE
    ):
        errors.append(f"{prefix} prohibited claims shall equal the required set")


def _source_value(errors: list[str], source: object, record: dict[str, object], prefix: str) -> dict[str, object] | None:
    if not isinstance(source, dict):
        errors.append(f"{prefix} source is required")
        return None
    if source.get("repository") != OWNER_REPOSITORY:
        errors.append(f"{prefix} source repository shall equal tdistress/ESAF")
    for field, message in (("comment_id", "comment ID"), ("author_user_id", "user ID")):
        value = source.get(field)
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{prefix} source {message} shall be numeric")
    if not _owner_comment_url(source.get("comment_url"), source.get("comment_id")):
        errors.append(f"{prefix} source comment URL shall use GitHub HTTPS")
    if source.get("author_login") != OWNER_LOGIN:
        errors.append(f"{prefix} source login shall equal {OWNER_LOGIN}")
    if source.get("author_association") != "OWNER":
        errors.append(f"{prefix} source author association shall be OWNER")
    for field in ("created_at", "updated_at", "source_verified_at"):
        timestamp = _rfc3339(source.get(field))
        if timestamp is None:
            errors.append(f"{prefix} source {field} shall be RFC 3339")
        elif timestamp.astimezone(timezone.utc).date().isoformat() != _publication_date(record):
            errors.append(f"{prefix} source {field} UTC date shall equal conditional publication date")
    digest = source.get("body_sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        errors.append(f"{prefix} source body digest shall be a SHA-256")
    return source


def _validate_timestamp(errors: list[str], record: dict[str, object], value: object) -> None:
    timestamp = _rfc3339(value)
    if timestamp is None:
        errors.append("mapping decision timestamp shall be RFC 3339")
    elif timestamp.astimezone(timezone.utc).date().isoformat() != _publication_date(record):
        errors.append("mapping decision UTC date shall equal conditional publication date")


def _validate_qualified_decision(
    errors: list[str], record: dict[str, object], value: dict[str, object], closure_head: object,
) -> None:
    if value.get("sha") != closure_head:
        errors.append("mapping decision is not bound to closure head")
    _validate_timestamp(errors, record, value.get("decided_at"))
    if not isinstance(value.get("reviewer"), str) or not value["reviewer"].strip():
        errors.append("qualified mapping reviewer shall be named")
    if not isinstance(value.get("qualification"), str) or not value["qualification"].strip():
        errors.append("qualified mapping reviewer shall be qualified")
    if value.get("disposition") != "approved":
        errors.append("qualified mapping disposition shall be approved")
    if value.get("qualified_review_status") != "completed":
        errors.append("qualified review status shall be completed")
    if not _https(value.get("url")):
        errors.append("mapping decision URL shall use HTTPS")
    _validate_limitations(errors, value.get("limitations"), "mapping decision")
    wording = json.dumps(value, sort_keys=True).casefold()
    if any(term in wording for term in ("owner_risk_acceptance", "repository owner", "repository_owner", "deferred")):
        errors.append("qualified mapping decision shall not contain owner-risk wording")


def _validate_owner_decision(
    errors: list[str], record: dict[str, object], value: dict[str, object], closure_head: object,
) -> dict[str, object] | None:
    if value.get("sha") != closure_head:
        errors.append("mapping decision is not bound to closure head")
    _validate_timestamp(errors, record, value.get("decided_at"))
    if not isinstance(value.get("owner_login"), str) or not value["owner_login"].strip():
        errors.append("owner mapping login shall be named")
    owner_id = value.get("owner_user_id")
    if not isinstance(owner_id, int) or isinstance(owner_id, bool):
        errors.append("owner mapping user ID shall be numeric")
    if value.get("role") != "repository_owner":
        errors.append("owner mapping role shall equal repository_owner")
    if value.get("author_association") != "OWNER":
        errors.append("owner mapping author association shall be OWNER")
    if value.get("disposition") != "accepted_for_working_draft":
        errors.append("owner mapping disposition shall be accepted_for_working_draft")
    if value.get("qualified_review_status") != "deferred":
        errors.append("owner mapping qualified review status shall be deferred")
    if not _https(value.get("url")):
        errors.append("mapping decision URL shall use HTTPS")
    _validate_limitations(errors, value.get("limitations"), "mapping decision")
    source = _source_value(errors, value.get("source"), record, "owner mapping")
    if source is not None:
        if value.get("url") != source.get("comment_url"):
            errors.append("owner mapping decision URL shall equal source comment URL")
        if value.get("owner_login") != source.get("author_login") or value.get("owner_user_id") != source.get("author_user_id") or value.get("author_association") != source.get("author_association"):
            errors.append("owner mapping identity shall match source")
        if value.get("decided_at") != source.get("created_at"):
            errors.append("owner mapping timestamp shall match source creation time")
    wording = json.dumps(value, sort_keys=True).casefold()
    if "completed" in wording and "qualified" in wording:
        errors.append("owner mapping decision shall not claim completed qualified review")
    return source


def _validate_owner_scope(
    errors: list[str], record: dict[str, object], value: dict[str, object], closure_head: object, basis: object,
) -> dict[str, object] | None:
    if basis != "owner_risk_acceptance" or value.get("approval_basis") != "owner_risk_acceptance":
        errors.append("owner scope approval basis shall equal owner_risk_acceptance")
    if value.get("sha") != closure_head:
        errors.append("scope approval is not bound to closure head")
    if value.get("role") != "repository_owner":
        errors.append("owner scope role shall equal repository_owner")
    if value.get("author_association") != "OWNER":
        errors.append("owner scope author association shall be OWNER")
    if value.get("scope") != REPOSITORY_SCOPE:
        errors.append("owner scope shall equal complete_git_tracked_repository")
    _validate_limitations(errors, value.get("limitations"), "scope")
    source = _source_value(errors, value.get("source"), record, "owner scope")
    if source is not None:
        if value.get("owner_login") != source.get("author_login") or value.get("owner_user_id") != source.get("author_user_id"):
            errors.append("owner scope identity shall match source")
        if value.get("decided_at") != source.get("created_at"):
            errors.append("owner scope timestamp shall match source creation time")
    return source


def _validate_scope_decision(
    errors: list[str], record: dict[str, object], value: object, closure_head: object, basis: object,
) -> None:
    if isinstance(value, dict) and value.get("approval_basis") == "owner_risk_acceptance":
        _validate_owner_scope(errors, record, value, closure_head, basis)
    else:
        if basis == "owner_risk_acceptance":
            errors.append("owner-risk mapping basis requires owner scope approval")
        _candidate_verdict(errors, "scope", value, closure_head, scope=True)


def _validate_mapping_decisions(
    errors: list[str], record: dict[str, object], evidence: dict[str, object], closure_head: object,
) -> None:
    if evidence.get("mapping_decision_schema") != MAPPING_DECISION_SCHEMA:
        errors.append("mapping decision schema shall equal esaf-mapping-decisions-v1")
    basis = evidence.get("mapping_decision_basis")
    if basis not in MAPPING_DECISION_BASES:
        errors.append("mapping decision basis shall be supported")
    if basis != record.get("mapping_decision_basis"):
        errors.append("external mapping decision basis shall match the closure record")
    if "mapping_reviews" in evidence:
        errors.append("legacy mapping_reviews are not accepted")
    decisions = evidence.get("mapping_decisions")
    if not isinstance(decisions, list) or len(decisions) != len(EXPECTED_MAPPING_SETS):
        errors.append("mapping decisions shall contain each expected mapping set exactly once")
        return
    identifiers = [item.get("mapping_set_id") for item in decisions if isinstance(item, dict)]
    if (
        not all(isinstance(identifier, str) for identifier in identifiers)
        or sorted(identifier for identifier in identifiers if isinstance(identifier, str))
        != sorted(EXPECTED_MAPPING_SETS)
    ):
        errors.append("mapping decisions shall contain each expected mapping set exactly once")
    sources: list[dict[str, object]] = []
    for decision in decisions:
        if not isinstance(decision, dict):
            errors.append("mapping decision shall be an object")
            continue
        if decision.get("decision_type") != basis:
            errors.append("mapping decisions shall uniformly match mapping_decision_basis")
            continue
        if basis == "qualified_approval":
            _validate_qualified_decision(errors, record, decision, closure_head)
        elif basis == "owner_risk_acceptance":
            source = _validate_owner_decision(errors, record, decision, closure_head)
            if source is not None:
                sources.append(source)
    if basis == "owner_risk_acceptance" and sources and any(source != sources[0] for source in sources[1:]):
        errors.append("owner mapping decisions shall use the same source")


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

    _validate_scope_decision(
        errors, record, evidence.get("scope"), closure_head, evidence.get("mapping_decision_basis")
    )
    for name in ("technical", "editorial", "rendering"):
        _candidate_verdict(errors, name, evidence.get(name), closure_head)
    _candidate_verdict(errors, "governance", evidence.get("governance"), closure_head, governance=True)
    governance = evidence.get("governance")
    if isinstance(governance, dict):
        if governance.get("authority") != "Steering Committee":
            errors.append("governance authority is not authorized")

    _validate_mapping_decisions(errors, record, evidence, closure_head)
    if evidence.get("mapping_decision_basis") == "owner_risk_acceptance":
        scope = evidence.get("scope")
        decisions = evidence.get("mapping_decisions")
        if isinstance(scope, dict) and isinstance(decisions, list) and decisions and isinstance(decisions[0], dict):
            if scope.get("source") != decisions[0].get("source"):
                errors.append("owner scope source shall match mapping decision source")

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
        if record.get("phase") == "published":
            errors.append("external evidence is not accepted for a published record")
        else:
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
