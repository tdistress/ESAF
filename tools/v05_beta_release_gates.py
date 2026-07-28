#!/usr/bin/env python3
"""Validate the v0.5-beta release-record contract."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
from functools import lru_cache
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import tempfile
from typing import Any, Sequence

import yaml


RELEASE = "0.5-beta"
TAG = "v0.5-beta"
ISSUE = 59
RECORD_RELATIVE = (
    "docs/superpowers/reviews/"
    "2026-07-27-v05-beta-publication-readiness.md"
)
CLOSURE_ALLOWLIST = (
    "VERSION.md",
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "project/RELEASE_PLAN.md",
    RECORD_RELATIVE,
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
COMMAND_IDS = (
    "full_suite",
    "assessment",
    "profiles",
    "controls",
    "architectures",
    "migration",
    "crosswalk_current",
    "crosswalk_baseline",
    "pci_readiness",
    "links",
    "release_v04",
    "release_v05",
    "mermaid_inventory",
    "mermaid_rendering",
    "whole_range_diff",
    "cache_count",
    "clean_status",
)
OWNER_DECISION_SCHEMA = "esaf-v05-owner-decision-v1"
QUALIFIED_REVIEW_STATUS = "deferred"
OWNER_DISPOSITION = "accepted_for_working_draft"
MISSING_ROLES = (
    "specification_and_inventory",
    "security_and_overclaiming",
)
REENTRY_TRIGGERS = {
    "eligible_qualified_reviewer_available",
    "mapping_or_source_inventory_changes",
    "owner_decision_expires_withdrawn_edited_or_superseded",
    "accountable_owner_requires_earlier_completion",
    "closure_candidate_or_merged_tree_changes",
}
CLAIMS_NOT_MADE = {
    "qualified_review",
    "qualified_mapping_approval",
    "artifact_lifecycle_approval",
    "certification",
    "compliance",
    "equivalence",
    "endorsement",
    "external_scheme_approval",
    "production_readiness",
    "assurance",
    "implementation_assessment",
    "legal_sufficiency",
    "replacement_of_qualified_professional_judgment",
}
EVIDENCE_SCHEMA = "esaf-v05-release-evidence-v1"
POST_MERGE_SCHEMA = "esaf-v05-post-merge-results-v1"
ACQUISITION_SCHEMA = "esaf-v05-acquisition-v1"
MERMAID_RENDERER = "@mermaid-js/mermaid-cli@11.16.0"
MERMAID_BLOCKS = 23
EVIDENCE_KEYS = {
    "schema",
    "release",
    "closure_base",
    "closure_head",
    "closure_tree",
    "scope",
    "technical",
    "editorial",
    "terminology",
    "rendering",
    "profile_scope",
    "governance",
    "candidate_commands",
    "mapping_decision_schema",
    "mapping_decision_basis",
    "mapping_decisions",
    "github_checks",
    "merge_state",
    "tag_state",
    "acquisition",
}
TAGGABLE_KEYS = EVIDENCE_KEYS | {"merge_head", "merge_tree", "post_merge"}
VERDICT_KEYS = {
    "sha",
    "reviewer",
    "role",
    "date",
    "disposition",
    "url",
    "critical",
    "important",
    "source",
}
SOURCE_KEYS = {
    "repository",
    "resource_path",
    "comment_url",
    "comment_id",
    "author_login",
    "author_user_id",
    "author_association",
    "created_at",
    "updated_at",
    "body_sha256",
    "response_sha256",
    "acquisition_resource_id",
    "source_verified_at",
}
GOVERNANCE_KEYS = {
    "authority",
    "authority_attestation",
    "authority_verification",
    "authority_basis",
}
SCOPE_KEYS = {"scope", "milestone"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
QUALIFIED_SCHEMA = (
    "https://esaf-standard.org/schemas/"
    "qualified-review-evidence.schema.json"
)
QUALIFIED_WRAPPER_KEYS = {
    "retained_root",
    "campaign_path",
    "archive_path",
    "seal_path",
    "source",
}
OWNER_DECISION_KEYS = {
    "mapping_set_id",
    "mapping_decision_basis",
    "decision_type",
    "sha",
    "disposition",
    "qualified_review_status",
    "missing_qualified_roles",
    "accountable_owner",
    "issue_55_status",
    "lifecycle",
    "claims_not_made",
    "reentry_triggers",
    "url",
    "source",
}
MISSING_ROLE_KEYS = {"mapping_set_id", "role"}
ACQUISITION_RESOURCE_KEYS = {
    "resource_id",
    "observed_canonical_url",
    "page_count",
    "response_sha256",
}
TAG_STATE_KEYS = {
    "resource",
    "exists",
    "status",
    "response_sha256",
}
TAG_RESOURCE = "repos/tdistress/ESAF/git/ref/tags/v0.5-beta"


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
    if candidate_phase == "evidence_candidate":
        errors.append("evidence_candidate shall not have a predecessor")
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


def validate_external_evidence(
    root: Path,
    record: dict[str, object],
    evidence: dict[str, object],
    expected_head: str,
    phase: str,
    now: datetime | None = None,
) -> list[str]:
    """Validate exact-candidate closure or taggable external evidence."""
    errors: list[str] = []
    if record.get("phase") != "closure_candidate":
        errors.append("external evidence requires a closure_candidate record")
    if phase not in {"closure", "taggable"}:
        return [*errors, "external evidence phase shall be closure or taggable"]
    if not isinstance(evidence, dict):
        return [*errors, f"{phase} evidence shall be an object"]

    expected_keys = TAGGABLE_KEYS if phase == "taggable" else EVIDENCE_KEYS
    missing = sorted(expected_keys - set(evidence))
    unknown = sorted(set(evidence) - expected_keys)
    if missing:
        errors.append(f"{phase} evidence is missing keys: {', '.join(missing)}")
    if unknown:
        errors.append(f"{phase} evidence has unknown keys: {', '.join(unknown)}")
    if missing:
        return errors

    if evidence.get("schema") != EVIDENCE_SCHEMA:
        errors.append("external evidence schema is invalid")
    if evidence.get("release") != RELEASE:
        errors.append("external evidence release shall equal 0.5-beta")
    closure_head = evidence.get("closure_head")
    closure_base = evidence.get("closure_base")
    closure_tree = evidence.get("closure_tree")
    if not _sha(closure_base) or closure_base == closure_head:
        errors.append(
            "closure base shall be a distinct 40-character SHA"
        )
    if not _sha(closure_head):
        errors.append("closure head shall be a 40-character SHA")
    if not _sha(closure_tree):
        errors.append("closure tree shall be a 40-character SHA")
    if phase == "closure" and closure_head != expected_head:
        errors.append("closure head shall equal expected head")

    merge_head: object = None
    merge_tree: object = None
    if phase == "taggable":
        merge_head = evidence.get("merge_head")
        merge_tree = evidence.get("merge_tree")
        if not _sha(merge_head):
            errors.append("merge head shall be a 40-character SHA")
        if not _sha(merge_tree):
            errors.append("merge tree shall be a 40-character SHA")
        if merge_head != expected_head:
            errors.append("merge head shall equal expected head")
        if merge_head == closure_head:
            errors.append("merge head shall differ from closure head")
        if merge_tree != closure_tree:
            errors.append("merged tree shall equal closure tree")

    acquired_resources = _validate_acquisition(
        errors, evidence.get("acquisition"), now
    )
    _validate_tag_state(
        errors, evidence.get("tag_state"), acquired_resources
    )
    _validate_acquisition_coverage(
        errors, evidence, acquired_resources, phase
    )
    for name in (
        "scope",
        "technical",
        "editorial",
        "terminology",
        "rendering",
        "profile_scope",
        "governance",
    ):
        _validate_sourced_verdict(
            errors,
            name,
            evidence.get(name),
            closure_head,
            acquired_resources,
        )
    _validate_human_authorities(errors, evidence)

    _validate_commands(
        errors,
        evidence.get("candidate_commands"),
        closure_head,
        "candidate",
    )
    _validate_mapping_basis(
        errors, root, record, evidence, closure_head, acquired_resources
    )
    _validate_github_checks(errors, evidence.get("github_checks"), closure_head)
    _validate_merge_state(errors, evidence.get("merge_state"), closure_head)
    if phase == "taggable":
        _validate_post_merge(
            errors, evidence.get("post_merge"), merge_head, merge_tree
        )
    return errors


def _sha(value: object) -> bool:
    return isinstance(value, str) and SHA_RE.fullmatch(value) is not None


def _nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _numeric(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _rfc3339_utc(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None
    return parsed if parsed.tzinfo == timezone.utc else None


def _validate_acquisition(
    errors: list[str], value: object, now: datetime | None
) -> dict[str, dict[str, object]]:
    if not isinstance(value, dict):
        errors.append("acquisition manifest is required")
        return {}
    required = {
        "schema",
        "repository",
        "authenticated_login",
        "retrieved_at",
        "complete",
        "resources",
    }
    if set(value) != required:
        errors.append("acquisition manifest keys are invalid")
    if value.get("schema") != ACQUISITION_SCHEMA:
        errors.append("acquisition manifest schema is invalid")
    if value.get("repository") != "tdistress/ESAF":
        errors.append("acquisition repository shall equal tdistress/ESAF")
    if not _nonblank(value.get("authenticated_login")):
        errors.append("acquisition authenticated login is required")
    if value.get("complete") is not True:
        errors.append("acquisition manifest shall be complete")
    resources = value.get("resources")
    if (
        not isinstance(resources, list)
        or not all(
            isinstance(item, dict)
            and set(item) == ACQUISITION_RESOURCE_KEYS
            and _nonblank(item.get("resource_id"))
            and _https(item.get("observed_canonical_url"))
            and _numeric(item.get("page_count"))
            and item.get("page_count", 0) > 0
            and isinstance(item.get("response_sha256"), str)
            and SHA256_RE.fullmatch(item["response_sha256"]) is not None
            for item in resources
        )
    ):
        errors.append("acquisition resource identifiers are invalid")
        result: dict[str, dict[str, object]] = {}
    else:
        identifiers = [str(item["resource_id"]) for item in resources]
        if len(identifiers) != len(set(identifiers)):
            errors.append("acquisition resource identifiers are invalid")
            result = {}
        else:
            result = {
                str(item["resource_id"]): item
                for item in resources
            }
    retrieved_at = _rfc3339_utc(value.get("retrieved_at"))
    reference = now or datetime.now(timezone.utc)
    if retrieved_at is None:
        errors.append("acquisition retrieval timestamp shall be RFC 3339 UTC")
    elif retrieved_at > reference or (reference - retrieved_at).total_seconds() > 900:
        errors.append("acquisition manifest shall be no more than 15 minutes old")
    return result


def _validate_tag_state(
    errors: list[str],
    value: object,
    acquired_resources: dict[str, dict[str, object]],
) -> None:
    if (
        not isinstance(value, dict)
        or set(value) != TAG_STATE_KEYS
        or value.get("resource") != TAG_RESOURCE
        or value.get("exists") is not False
        or value.get("status") != 404
        or not isinstance(value.get("response_sha256"), str)
        or SHA256_RE.fullmatch(value["response_sha256"]) is None
    ):
        errors.append(
            "remote tag state shall prove exact v0.5-beta absence"
        )
        return
    acquired = acquired_resources.get(TAG_RESOURCE)
    if (
        not isinstance(acquired, dict)
        or acquired.get("page_count") != 1
        or acquired.get("observed_canonical_url")
        != f"https://api.github.com/{TAG_RESOURCE}"
        or acquired.get("response_sha256")
        != value.get("response_sha256")
    ):
        errors.append(
            "remote tag state shall bind the acquired tag response"
        )


def _validate_acquisition_coverage(
    errors: list[str],
    evidence: dict[str, object],
    acquired_resources: dict[str, dict[str, object]],
    phase: str,
) -> None:
    closure_head = evidence.get("closure_head")
    expected = {
        "user",
        TAG_RESOURCE,
        f"repos/tdistress/ESAF/commits/{closure_head}",
        f"repos/tdistress/ESAF/commits/{closure_head}/check-runs",
    }
    scope = evidence.get("scope")
    source = scope.get("source") if isinstance(scope, dict) else None
    comment_url = (
        source.get("comment_url")
        if isinstance(source, dict)
        else None
    )
    pull_match = (
        re.fullmatch(
            (
                r"https://github\.com/tdistress/ESAF/"
                r"(?:issues|pull)/([1-9][0-9]*)"
                r"#issuecomment-[1-9][0-9]*"
            ),
            comment_url,
        )
        if isinstance(comment_url, str)
        else None
    )
    if pull_match is not None:
        expected.add(
            f"repos/tdistress/ESAF/pulls/{pull_match.group(1)}"
        )
    if phase == "taggable":
        expected.add(
            f"repos/tdistress/ESAF/commits/{evidence.get('merge_head')}"
        )
    if expected - set(acquired_resources):
        errors.append(
            "acquisition manifest is missing required resources"
        )
        return
    acquisition = evidence.get("acquisition")
    login = (
        acquisition.get("authenticated_login")
        if isinstance(acquisition, dict)
        else None
    )
    if acquired_resources["user"].get(
        "observed_canonical_url"
    ) != f"https://github.com/{login}":
        errors.append(
            "acquisition authenticated user resource is inconsistent"
        )


def _validate_source(
    errors: list[str],
    name: str,
    value: object,
    acquired_resources: dict[str, dict[str, object]],
) -> None:
    if not isinstance(value, dict) or set(value) != SOURCE_KEYS:
        errors.append(f"{name} source keys are invalid")
        return
    if value.get("repository") != "tdistress/ESAF":
        errors.append(f"{name} source repository shall equal tdistress/ESAF")
    if not _nonblank(value.get("resource_path")):
        errors.append(f"{name} source resource path is required")
    if not _https(value.get("comment_url")):
        errors.append(f"{name} source comment URL shall use HTTPS")
    if not _numeric(value.get("comment_id")):
        errors.append(f"{name} source comment ID shall be numeric")
    for field in ("author_login", "author_association"):
        if not _nonblank(value.get(field)):
            errors.append(f"{name} source {field} is required")
    if not _numeric(value.get("author_user_id")):
        errors.append(f"{name} source author user ID shall be numeric")
    for field in ("created_at", "updated_at", "source_verified_at"):
        if _rfc3339_utc(value.get(field)) is None:
            errors.append(f"{name} source {field} shall be RFC 3339 UTC")
    for field in ("body_sha256", "response_sha256"):
        if not isinstance(value.get(field), str) or SHA256_RE.fullmatch(
            value[field]
        ) is None:
            errors.append(f"{name} source {field} shall be a SHA-256")
    resource_id = value.get("acquisition_resource_id")
    if resource_id not in acquired_resources:
        errors.append(f"{name} source shall bind an acquired resource")
    else:
        acquired = acquired_resources[resource_id]
        if value.get("comment_url") != acquired.get(
            "observed_canonical_url"
        ):
            errors.append(
                f"{name} source canonical URL shall equal acquired response"
            )
        if (
            acquired.get("page_count") != 1
            or value.get("response_sha256")
            != acquired.get("response_sha256")
        ):
            errors.append(
                f"{name} source response digest shall equal acquired response"
            )
    comment_id = value.get("comment_id")
    resource_path = value.get("resource_path")
    comment_url = value.get("comment_url")
    if (
        not _numeric(comment_id)
        or resource_path
        != f"repos/tdistress/ESAF/issues/comments/{comment_id}"
        or resource_id != resource_path
        or not isinstance(comment_url, str)
        or re.fullmatch(
            (
                r"https://github\.com/tdistress/ESAF/(?:issues|pull)/"
                rf"[1-9][0-9]*#issuecomment-{comment_id}"
            ),
            comment_url,
        )
        is None
    ):
        errors.append(f"{name} source identity is inconsistent")


def _validate_sourced_verdict(
    errors: list[str],
    name: str,
    value: object,
    closure_head: object,
    acquired_resources: dict[str, dict[str, object]],
) -> None:
    additional = GOVERNANCE_KEYS if name == "governance" else (
        SCOPE_KEYS if name == "scope" else set()
    )
    if not isinstance(value, dict) or set(value) != VERDICT_KEYS | additional:
        errors.append(f"{name} verdict keys are invalid")
        return
    if value.get("sha") != closure_head:
        errors.append(f"{name} verdict shall be bound to closure head")
    if not _nonblank(value.get("reviewer")):
        errors.append(f"{name} reviewer shall be named")
    if not _nonblank(value.get("role")):
        errors.append(f"{name} verdict role shall be named")
    if not _iso_date(value.get("date")):
        errors.append(f"{name} verdict date shall be YYYY-MM-DD")
    expected_disposition = {
        "scope": "approved_for_working_draft_closure",
        "governance": "approved_for_working_draft_publication",
    }.get(name, "approved")
    if value.get("disposition") != expected_disposition:
        errors.append(f"{name} verdict disposition is invalid")
    if not _https(value.get("url")):
        errors.append(f"{name} verdict URL shall use HTTPS")
    if value.get("critical") != 0 or value.get("important") != 0:
        errors.append(f"{name} verdict findings shall be zero")
    source = value.get("source")
    _validate_source(errors, name, source, acquired_resources)
    if (
        isinstance(source, dict)
        and value.get("url") != source.get("comment_url")
    ):
        errors.append(
            f"{name} verdict URL shall equal source comment URL"
        )
    if name == "scope":
        if (
            value.get("scope") != REPOSITORY_SCOPE
            or value.get("milestone") != TAG
        ):
            errors.append("scope verdict shall approve the complete v0.5-beta scope")
    if name == "governance":
        if (
            value.get("authority") != "Steering Committee"
            or value.get("authority_attestation") is not True
            or value.get("authority_verification") != "manual"
            or value.get("authority_basis")
            != "GOVERNANCE.md#21-steering-committee"
        ):
            errors.append(
                "governance shall contain an express manual authority attestation"
            )


def _validate_human_authorities(
    errors: list[str], evidence: dict[str, object]
) -> None:
    scope = evidence.get("scope")
    governance = evidence.get("governance")
    if not isinstance(scope, dict) or not isinstance(governance, dict):
        return
    scope_source = scope.get("source")
    governance_source = governance.get("source")
    if not isinstance(scope_source, dict):
        return
    if (
        scope_source.get("author_association") != "OWNER"
        or scope.get("reviewer") != scope_source.get("author_login")
        or scope.get("role") != "repository owner"
        or scope.get("url") != scope_source.get("comment_url")
    ):
        errors.append(
            "scope approval shall use its authenticated OWNER source"
        )
    if isinstance(governance_source, dict):
        if (
            governance.get("reviewer")
            != governance_source.get("author_login")
            or governance.get("role") != "Steering Committee approver"
            or governance.get("url") != governance_source.get("comment_url")
        ):
            errors.append(
                "governance approver shall match its authenticated source author"
            )
        if _source_identity(governance_source) == _source_identity(scope_source):
            errors.append(
                "governance source shall be distinct from owner and scope source"
            )


def _source_identity(value: dict[str, object]) -> tuple[object, ...]:
    return (
        value.get("repository"),
        value.get("resource_path"),
        value.get("comment_id"),
        value.get("comment_url"),
        value.get("body_sha256"),
    )


def _validate_commands(
    errors: list[str],
    value: object,
    sha: object,
    label: str,
) -> None:
    diagnostic = (
        f"{label} commands shall contain each required command exactly once"
    )
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        errors.append(diagnostic)
        return
    names = [item.get("name") for item in value]
    if (
        len(names) != len(COMMAND_IDS)
        or len(set(names)) != len(names)
        or set(names) != set(COMMAND_IDS)
    ):
        errors.append(diagnostic)
        return
    for command in value:
        name = str(command["name"])
        expected_keys = (
            {"name", "sha", "exit_code", "result"}
            if label == "candidate"
            else {"name", "exit_code", "result"}
        )
        if set(command) != expected_keys:
            errors.append(f"{label} command keys are invalid")
            continue
        if command.get("exit_code") != 0:
            errors.append(f"{name} {label} command shall succeed")
        if label == "candidate" and command.get("sha") != sha:
            errors.append(
                f"{name} candidate command shall be bound to closure head"
            )
        result = command.get("result")
        if name == "mermaid_rendering":
            _validate_mermaid_result(errors, result, label)
        elif not _nonblank(result):
            errors.append(f"{name} {label} command result shall be nonempty")


def _validate_mermaid_result(
    errors: list[str], value: object, label: str
) -> None:
    candidate_keys = {
        "rendered_blocks",
        "renderer",
        "visual_review",
        "candidate_inventory_equal",
        "candidate_review_url",
        "candidate_reviewer",
        "reviewed_at",
    }
    keys = (
        candidate_keys | {"merge_tree_equal", "post_merge_reviewer"}
        if label == "post-merge"
        else candidate_keys
    )
    if not isinstance(value, dict) or set(value) != keys:
        errors.append(
            "mermaid_rendering result shall be a structured visual review"
        )
        return
    if value.get("rendered_blocks") != MERMAID_BLOCKS:
        errors.append("mermaid_rendering shall cover exactly 23 blocks")
    if value.get("renderer") != MERMAID_RENDERER:
        errors.append("mermaid_rendering renderer is invalid")
    if value.get("visual_review") != "approved":
        errors.append("mermaid_rendering visual review shall be approved")
    if value.get("candidate_inventory_equal") is not True or (
        label == "post-merge" and value.get("merge_tree_equal") is not True
    ):
        errors.append("mermaid_rendering equality flags shall be true")
    if not _https(value.get("candidate_review_url")):
        errors.append("mermaid_rendering candidate review URL shall use HTTPS")
    if not _nonblank(value.get("candidate_reviewer")) or (
        label == "post-merge"
        and not _nonblank(value.get("post_merge_reviewer"))
    ):
        errors.append("mermaid_rendering reviewer identities shall be named")
    if _rfc3339_utc(value.get("reviewed_at")) is None:
        errors.append("mermaid_rendering review timestamp shall be RFC 3339 UTC")


def _mapping_set_ids(record: dict[str, object]) -> list[str]:
    value = record.get("mapping_sets")
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _validate_mapping_basis(
    errors: list[str],
    root: Path,
    record: dict[str, object],
    evidence: dict[str, object],
    closure_head: object,
    acquired_resources: dict[str, dict[str, object]],
) -> None:
    basis = evidence.get("mapping_decision_basis")
    decisions = evidence.get("mapping_decisions")
    if basis != record.get("mapping_decision_basis"):
        errors.append("external mapping basis shall match the release record")
    if basis == "owner_risk_acceptance":
        _validate_owner_risk(
            errors,
            record,
            evidence.get("mapping_decision_schema"),
            decisions,
            closure_head,
            acquired_resources,
        )
        if (
            isinstance(decisions, list)
            and decisions
            and isinstance(decisions[0], dict)
            and isinstance(evidence.get("scope"), dict)
            and evidence["scope"].get("source")
            != decisions[0].get("source")
        ):
            errors.append(
                "scope approval source shall match owner-risk decision source"
            )
    elif basis == "qualified_approval":
        _validate_qualified_campaign(
            errors,
            root,
            record,
            evidence.get("mapping_decision_schema"),
            decisions,
            closure_head,
            acquired_resources,
        )
    else:
        errors.append("external mapping decision basis is invalid")


def _validate_owner_risk(
    errors: list[str],
    record: dict[str, object],
    schema: object,
    value: object,
    closure_head: object,
    acquired_resources: dict[str, dict[str, object]],
) -> None:
    if schema != OWNER_DECISION_SCHEMA:
        errors.append("owner-risk evidence shall use esaf-v05-owner-decision-v1")
    if not isinstance(value, list):
        errors.append("owner-risk evidence shall contain exactly three decisions")
        return
    if len(value) != 3 or not all(isinstance(item, dict) for item in value):
        errors.append("owner-risk evidence shall contain exactly three decisions")
    decisions = [item for item in value if isinstance(item, dict)]
    expected_ids = _mapping_set_ids(record)
    observed_ids = [item.get("mapping_set_id") for item in decisions]
    if (
        len(observed_ids) != len(expected_ids)
        or len(set(observed_ids)) != len(observed_ids)
        or set(observed_ids) != set(expected_ids)
    ):
        errors.append(
            "owner-risk decisions shall contain each mapping set exactly once"
        )
    sources: list[object] = []
    for decision in decisions:
        if set(decision) != OWNER_DECISION_KEYS:
            errors.append("owner-risk decision keys are invalid")
        if decision.get("mapping_decision_basis") != "owner_risk_acceptance":
            errors.append("mapping decisions shall use one uniform basis")
        if (
            decision.get("decision_type") != "owner_risk_acceptance"
            or decision.get("disposition") != OWNER_DISPOSITION
            or decision.get("qualified_review_status") != QUALIFIED_REVIEW_STATUS
        ):
            errors.append("owner-risk decision disposition is invalid")
        if decision.get("sha") != closure_head:
            errors.append("owner-risk decision shall be bound to closure head")
        roles = decision.get("missing_qualified_roles")
        expected_roles = {
            (mapping_set_id, role)
            for mapping_set_id in expected_ids
            for role in MISSING_ROLES
        }
        observed_roles: set[tuple[object, object]] = set()
        if isinstance(roles, list):
            if any(
                not isinstance(item, dict)
                or set(item) != MISSING_ROLE_KEYS
                for item in roles
            ):
                errors.append("owner-risk missing-role keys are invalid")
            observed_roles = {
                (item.get("mapping_set_id"), item.get("role"))
                for item in roles
                if isinstance(item, dict)
            }
        if (
            not isinstance(roles, list)
            or len(roles) != 6
            or len(observed_roles) != 6
            or observed_roles != expected_roles
        ):
            errors.append(
                "owner-risk decision shall contain exactly six missing roles"
            )
        source = decision.get("source")
        sources.append(source)
        _validate_source(errors, "owner-risk", source, acquired_resources)
        if not isinstance(source, dict):
            errors.append("owner-risk decision source is required")
            continue
        if decision.get("accountable_owner") != source.get("author_login"):
            errors.append(
                "owner-risk accountable owner shall match authenticated author"
            )
        if source.get("author_association") != "OWNER":
            errors.append("owner-risk source association shall be OWNER")
        if decision.get("url") != source.get("comment_url"):
            errors.append("owner-risk decision URL shall match source")
        if decision.get("issue_55_status") != "remains_open":
            errors.append("owner-risk decision shall leave issue 55 open")
        if decision.get("lifecycle") != "draft":
            errors.append("owner-risk decision lifecycle shall remain draft")
        if _string_set(decision.get("claims_not_made")) != CLAIMS_NOT_MADE:
            errors.append("owner-risk nonclaims shall equal the required set")
        if _string_set(decision.get("reentry_triggers")) != REENTRY_TRIGGERS:
            errors.append(
                "owner-risk re-entry triggers shall equal the required set"
            )
    if sources and any(source != sources[0] for source in sources[1:]):
        errors.append("owner-risk decisions shall use one unchanged source")


def _string_set(value: object) -> set[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return set()
    if len(value) != len(set(value)):
        return set()
    return set(value)


def _validate_qualified_campaign(
    errors: list[str],
    root: Path,
    record: dict[str, object],
    schema: object,
    value: object,
    closure_head: object,
    acquired_resources: dict[str, dict[str, object]],
) -> None:
    del record
    if (
        schema != QUALIFIED_SCHEMA
        or not isinstance(value, list)
        or len(value) != 1
        or not isinstance(value[0], dict)
        or set(value[0]) != QUALIFIED_WRAPPER_KEYS
    ):
        errors.append(
            "qualified approval requires recognized immutable campaign evidence"
        )
        errors.append(
            "qualified approval requires a valid exact-candidate six-role Draft campaign"
        )
        return
    decision = value[0]
    source_errors: list[str] = []
    _validate_source(
        source_errors,
        "qualified",
        decision.get("source"),
        acquired_resources,
    )
    if source_errors:
        errors.extend(source_errors)
        errors.append(
            "qualified approval requires recognized immutable campaign evidence"
        )
        return
    paths = _qualified_retained_paths(decision)
    if paths is None or not isinstance(closure_head, str):
        errors.append(
            "qualified retained evidence locators shall remain within one external root"
        )
        errors.append(
            "qualified approval requires a valid exact-candidate six-role Draft campaign"
        )
        return
    campaign_root, archive_path, seal_path = paths
    try:
        from tools.build_mapping_review_bundle import GitReader
        from tools.validate_qualified_review_evidence import (
            validate_retained_campaign,
        )

        report = validate_retained_campaign(
            GitReader(root),
            closure_head,
            campaign_root,
            seal_path,
            archive_path,
        )
    except (OSError, RuntimeError, UnicodeError, ValueError):
        errors.append(
            "qualified campaign shall pass the tracked official validator"
        )
        return
    if report.evidence_valid is not True:
        if any(
            message.startswith("retained archive")
            or message.startswith("retained seal")
            for message in report.errors
        ):
            errors.append(
                "qualified retained archive and seal shall match exact campaign bytes"
            )
        else:
            errors.append(
                "qualified campaign shall pass the tracked official validator"
            )
        return
    if (
        report.candidate_commit != closure_head
        or report.readiness_name != "transition_ready"
        or report.readiness_value is not True
        or not _nonblank(report.campaign_id)
    ):
        errors.append(
            "qualified approval requires a valid exact-candidate six-role Draft campaign"
        )


def _qualified_retained_paths(
    decision: dict[str, object],
) -> tuple[Path, Path, Path] | None:
    retained_root_value = decision.get("retained_root")
    if not isinstance(retained_root_value, str):
        return None
    retained_root = Path(retained_root_value)
    if not retained_root.is_absolute():
        return None
    try:
        resolved_root = retained_root.resolve(strict=True)
    except OSError:
        return None
    if not resolved_root.is_dir():
        return None

    resolved: list[Path] = []
    for field in ("campaign_path", "archive_path", "seal_path"):
        relative = decision.get(field)
        if not isinstance(relative, str) or "\\" in relative:
            return None
        pure = PurePosixPath(relative)
        if (
            pure.is_absolute()
            or not pure.parts
            or any(part in {"", ".", ".."} for part in pure.parts)
        ):
            return None
        try:
            candidate = resolved_root.joinpath(*pure.parts).resolve(strict=True)
            candidate.relative_to(resolved_root)
        except (OSError, ValueError):
            return None
        resolved.append(candidate)
    campaign_root, archive_path, seal_path = resolved
    if (
        not campaign_root.is_dir()
        or not archive_path.is_file()
        or not seal_path.is_file()
    ):
        return None
    return campaign_root, archive_path, seal_path


def _validate_github_checks(
    errors: list[str], value: object, closure_head: object
) -> None:
    if not isinstance(value, dict):
        errors.append("GitHub checks are required")
        return
    if set(value) != {"expected", "observed"}:
        errors.append("GitHub checks keys are invalid")
    observed = value.get("observed")
    if (
        value.get("expected") != ["Validate ESAF sources"]
        or not isinstance(observed, list)
        or len(observed) != 1
        or not isinstance(observed[0], dict)
        or observed[0].get("name") != "Validate ESAF sources"
    ):
        errors.append("GitHub checks shall contain the required check exactly once")
        return
    check = observed[0]
    if set(check) != {"name", "sha", "conclusion", "url"}:
        errors.append("GitHub check keys are invalid")
    if check.get("sha") != closure_head:
        errors.append("GitHub check shall be bound to closure head")
    if check.get("conclusion") != "success":
        errors.append("GitHub check shall be successful")
    if not _https(check.get("url")):
        errors.append("GitHub check URL shall use HTTPS")


def _validate_merge_state(
    errors: list[str], value: object, closure_head: object
) -> None:
    if not isinstance(value, dict):
        errors.append("merge state is required")
        return
    if set(value) != {"sha", "mergeable", "state"}:
        errors.append("merge state keys are invalid")
    if value.get("sha") != closure_head:
        errors.append("merge state shall be bound to closure head")
    if value.get("mergeable") is not True or value.get("state") != "clean":
        errors.append("merge state shall be clean")


def _validate_post_merge(
    errors: list[str], value: object, merge_head: object, merge_tree: object
) -> None:
    if not isinstance(value, dict):
        errors.append("post-merge evidence is required")
        return
    if set(value) != {"schema", "sha", "tree", "commands"}:
        errors.append("post-merge evidence keys are invalid")
    if value.get("schema") != POST_MERGE_SCHEMA:
        errors.append("post-merge evidence schema is invalid")
    if value.get("sha") != merge_head:
        errors.append("post-merge evidence shall be bound to merge head")
    if value.get("tree") != merge_tree:
        errors.append("post-merge tree shall equal merged tree")
    _validate_commands(errors, value.get("commands"), merge_head, "post-merge")


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
        sources_draft, missing_sources, untracked_sources = _mapping_sources_are_draft(
            root, tuple(source_paths)
        )
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError):
        errors.append("crosswalk catalog cannot be parsed")
        return
    if missing_sources:
        errors.append("catalog-declared mapping source is missing")
    if untracked_sources:
        errors.append("catalog-declared mapping source shall be Git-tracked")
    draft = draft and sources_draft
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


def _mapping_sources_are_draft(
    root: Path, source_paths: tuple[str, ...]
) -> tuple[bool, bool, bool]:
    tracked = _tracked_paths(root)
    missing = any(not (root / relative).is_file() for relative in source_paths)
    untracked = any(
        (root / relative).is_file() and relative not in tracked
        for relative in source_paths
    )
    if missing or untracked:
        return False, missing, untracked
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", "crosswalks/mappings"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return _cached_mapping_sources_are_draft(root, source_paths, result.stdout), False, False


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


def _validate_baseline_at_ref(
    root: Path, ref: str, record: dict[str, object]
) -> list[str]:
    archive = subprocess.run(
        ["git", "archive", "--format=tar", ref],
        cwd=root,
        check=True,
        capture_output=True,
    )
    with tempfile.TemporaryDirectory() as temporary:
        snapshot = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as bundle:
            bundle.extractall(snapshot, filter="data")
        subprocess.run(["git", "init", "--quiet"], cwd=snapshot, check=True)
        subprocess.run(
            ["git", "-c", "core.autocrlf=false", "add", "."],
            cwd=snapshot,
            check=True,
            capture_output=True,
        )
        return validate_record(snapshot, record)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("--baseline-ref")
    parser.add_argument("--external-evidence", type=Path)
    parser.add_argument("--expected-head")
    parser.add_argument("--phase", choices=("closure", "taggable"))
    arguments = parser.parse_args(argv)
    root = Path.cwd().resolve()
    try:
        record = load_front_matter(root / RECORD_RELATIVE)
        errors = validate_record(root, record)
        external_arguments = (
            arguments.external_evidence,
            arguments.expected_head,
            arguments.phase,
        )
        external_count = sum(value is not None for value in external_arguments)
        if external_count not in {0, 3}:
            errors.append(
                "external-evidence, expected-head, and phase shall be supplied together"
            )
        elif external_count == 3:
            external_evidence = _load_json(arguments.external_evidence)
            errors.extend(
                validate_external_evidence(
                    root,
                    record,
                    external_evidence,
                    arguments.expected_head,
                    arguments.phase,
                )
            )
        phase = record.get("phase")
        if phase in PREVIOUS_PHASE and not arguments.baseline_ref:
            label = "closure candidate" if phase == "closure_candidate" else "published"
            errors.append(f"baseline-ref is required for {label}")
        elif arguments.baseline_ref:
            baseline = _load_baseline(root, arguments.baseline_ref)
            errors.extend(
                f"baseline record: {error}"
                for error in _validate_baseline_at_ref(
                    root, arguments.baseline_ref, baseline
                )
            )
            errors.extend(validate_transition(baseline, record))
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        errors = [f"release record could not be validated: {exc}"]
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
