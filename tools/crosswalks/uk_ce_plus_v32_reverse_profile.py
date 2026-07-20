"""Closed observation-claim registry for Cyber Essentials Plus v3.2 reverse evidence."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping


_SEMANTIC_FIELDS = ("result_kind", "subject", "predicate", "result_type")
_CLAIM_FIELDS = (
    "assessment_date_boundary",
    "control_id",
    "evidence_date_boundary",
    "predicate",
    "provision_id",
    "result_kind",
    "result_type",
    "subject",
)
_ASSESSMENT_DATE_BOUNDARY = "assessment_date_required"
_EVIDENCE_DATE_BOUNDARY = "evidence_date_required"


# The tuple form deliberately preserves the source declaration order so duplicate
# pair declarations cannot be hidden while a lookup is constructed.
OBSERVATION_PROFILE_ENTRIES = (
    ("CEPTS3.2-M-004", "AUD-120", "assessment_scope", "declared_assessment_boundary", "scope_correspondence_status", "recorded_comparison"),
    ("CEPTS3.2-M-010", "AUD-130", "finding_remediation", "pre_test_findings", "pre_test_resolution_status", "recorded_status"),
    ("CEPTS3.2-M-011", "AUD-120", "evidence_retention", "pre_test_verification_evidence", "retention_duration", "recorded_duration"),
    ("CEPTS3.2-S-007", "AUD-120", "sampling_calculation", "sample_size", "calculation_method_alignment", "recorded_calculation"),
    ("CEPTS3.2-S-008", "CMP-110", "evidence_retention", "sample_size_calculation_evidence", "retention_duration", "recorded_duration"),
    ("CEPTS3.2-T1-009", "INF-120", "vulnerability_severity", "assessed_service_vulnerability", "severity_score", "recorded_threshold"),
    ("CEPTS3.2-T1-011", "IAM-110", "authentication_requirement", "user_authentication", "service_access_requirement_status", "recorded_boolean"),
    ("CEPTS3.2-T1-012", "IAM-110", "authentication_strength", "authentication_factors", "factor_count", "recorded_count"),
    ("CEPTS3.2-T1-013", "IAM-140", "credential_configuration", "default_password", "password_change_status", "recorded_boolean"),
    ("CEPTS3.2-T1-014", "APP-150", "abuse_resistance", "login_attempts", "throttling_status", "recorded_boolean"),
    ("CEPTS3.2-T1-015", "APP-150", "abuse_resistance", "user_account", "lockout_attempt_threshold", "recorded_count"),
    ("CEPTS3.2-T2-007", "INF-120", "vulnerability_fix_availability", "qualifying_vulnerability", "vendor_fix_age", "recorded_duration"),
    ("CEPTS3.2-T3-005", "INF-110", "host_protection_configuration", "anti_malware", "activation_and_installation_coverage", "recorded_status"),
    ("CEPTS3.2-T3-015", "INF-110", "malware_delivery_control", "malware_test_file", "delivery_and_access_status", "recorded_status"),
    ("CEPTS3.2-T3-016", "INF-110", "execution_control", "executable_test_file", "delivery_execution_interaction_status", "recorded_status"),
    ("CEPTS3.2-T3-017", "INF-110", "malware_delivery_control", "defined_malware_delivery_branches", "branch_applicability_status", "recorded_branch"),
    ("CEPTS3.2-T3-021", "INF-110", "network_access_configuration", "test_user", "internet_access_status", "recorded_boolean"),
    ("CEPTS3.2-T3-022", "INF-110", "download_protection", "test_file_download", "download_prevention_status", "recorded_boolean"),
    ("CEPTS3.2-T3-023", "INF-110", "download_protection", "downloaded_test_file", "download_access_control_status", "recorded_boolean"),
    ("CEPTS3.2-T3-024", "INF-110", "malware_delivery_control", "malware_test_file", "download_and_access_status", "recorded_status"),
    ("CEPTS3.2-T3-025", "INF-110", "execution_control", "executable_test_file", "download_execution_interaction_status", "recorded_status"),
    ("CEPTS3.2-T3-027", "INF-110", "host_protection_configuration", "anti_malware_installation", "operational_status", "recorded_status"),
    ("CEPTS3.2-T3-028", "INF-110", "host_protection_configuration", "anti_malware_updates", "configuration_alignment", "recorded_comparison"),
    ("CEPTS3.2-T3-029", "INF-110", "host_protection_configuration", "anti_malware_installation_and_configuration", "check_status", "recorded_status"),
    ("CEPTS3.2-T3-031", "INF-110", "trust_store_configuration", "trusted_roots", "root_set_relation", "recorded_comparison"),
    ("CEPTS3.2-T3-032", "INF-130", "configuration_change_approval", "additional_trusted_roots", "applicant_agreement_status", "recorded_status"),
    ("CEPTS3.2-T3-033", "INF-110", "execution_control", "unsigned_executable", "execution_capability", "recorded_boolean"),
    ("CEPTS3.2-T3-034", "INF-110", "execution_control", "untrusted_chain_executable", "execution_capability", "recorded_boolean"),
    ("CEPTS3.2-T3-035", "INF-110", "code_signing_configuration", "executable_formats", "code_signing_coverage", "recorded_status"),
    ("CEPTS3.2-T3-036", "INF-110", "allowlisting_configuration", "listed_configuration_and_execution_checks", "check_status", "recorded_status"),
    ("CEPTS3.2-T4-008", "IAM-110", "mfa_challenge", "user_or_administrator", "pre_access_challenge_status", "recorded_boolean"),
)


class _DuplicateKey(ValueError):
    """Raised by the JSON parser when an object repeats a member name."""


def _parse_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _semantic_tokens(value: str) -> tuple[str, ...]:
    return tuple(token for token in re.split(r"[^a-z0-9]+", value.casefold()) if token)


def _semantic_value_errors(field: str, value: object) -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{field} must be a nonempty string"]
    tokens = _semantic_tokens(value)
    forbidden = {
        "true", "false", "compliance", "compliant", "noncompliant", "certification",
        "certified", "uncertified", "success", "successful", "failure", "equivalence",
        "equivalent", "nonequivalent", "inequivalent",
    }
    if any(token in forbidden or re.fullmatch(r"pass(?:ed|ing)?", token)
           or re.fullmatch(r"fail(?:ed|ing|ure)?", token) for token in tokens):
        return [f"{field} must be outcome-neutral"]
    if any(tokens[index:index + 2] in (("high", "risk"), ("low", "risk"))
           for index in range(len(tokens) - 1)):
        return [f"{field} must not encode a threshold classification"]
    if any(token in {"tool", "scanner", "utility", "assessor", "invocation"}
           for token in tokens) or (
        "assessment" in tokens
        and any(token in {"procedure", "execution", "activity"} for token in tokens)
    ):
        return [f"{field} must not describe mere tool use or assessment procedure activity"]
    return []


def build_observation_profiles(
    entries: Iterable[tuple[str, str, str, str, str, str]],
) -> dict[tuple[str, str], dict[str, str]]:
    """Build the pair-keyed lookup, rejecting duplicate or answer-bearing declarations."""
    profiles: dict[tuple[str, str], dict[str, str]] = {}
    for entry in entries:
        if len(entry) != 6:
            raise ValueError("observation profile entry must contain six strings")
        provision_id, control_id, result_kind, subject, predicate, result_type = entry
        if not all(isinstance(value, str) and value for value in entry):
            raise ValueError("observation profile entry values must be nonempty strings")
        pair = (provision_id, control_id)
        if pair in profiles:
            raise ValueError(f"duplicate observation profile pair: {provision_id}/{control_id}")
        semantic = {
            "result_kind": result_kind,
            "subject": subject,
            "predicate": predicate,
            "result_type": result_type,
        }
        semantic_errors = [
            error for field, value in semantic.items()
            for error in _semantic_value_errors(field, value)
        ]
        if semantic_errors:
            raise ValueError("; ".join(semantic_errors))
        profiles[pair] = semantic
    return profiles


OBSERVATION_PROFILES = build_observation_profiles(OBSERVATION_PROFILE_ENTRIES)


def render_observation_claim(provision_id: str, control_id: str) -> str:
    """Render the one canonical JSON observation allowed for an exact leg pair."""
    profile = OBSERVATION_PROFILES[(provision_id, control_id)]
    claim = {
        "assessment_date_boundary": _ASSESSMENT_DATE_BOUNDARY,
        "control_id": control_id,
        "evidence_date_boundary": _EVIDENCE_DATE_BOUNDARY,
        "provision_id": provision_id,
        **profile,
    }
    return json.dumps(claim, separators=(",", ":"), sort_keys=True)


def validate_observation_claim(
    claim_text: str,
    provision_id: object,
    control_id: object,
    profiles: Mapping[tuple[str, str], Mapping[str, str]] | None = None,
) -> list[str]:
    """Fail closed unless *claim_text* is the canonical registered pair claim."""
    if not isinstance(claim_text, str):
        return ["observation claim must be a canonical JSON object string"]
    try:
        claim = json.loads(claim_text, object_pairs_hook=_parse_object_pairs)
    except _DuplicateKey:
        return ["observation claim must not contain duplicate keys"]
    except json.JSONDecodeError:
        return ["observation claim must be valid JSON"]
    if not isinstance(claim, dict):
        return ["observation claim must be a JSON object"]
    if set(claim) != set(_CLAIM_FIELDS):
        return ["observation claim must contain exactly the eight design fields"]
    if any(not isinstance(claim[field], str) or not claim[field] for field in _CLAIM_FIELDS):
        return ["observation claim fields must be nonempty strings"]
    if json.dumps(claim, separators=(",", ":"), sort_keys=True) != claim_text:
        return ["observation claim must use canonical compact JSON serialization"]
    errors: list[str] = []
    if claim["assessment_date_boundary"] != _ASSESSMENT_DATE_BOUNDARY:
        errors.append("assessment_date_boundary must equal assessment_date_required")
    if claim["evidence_date_boundary"] != _EVIDENCE_DATE_BOUNDARY:
        errors.append("evidence_date_boundary must equal evidence_date_required")
    if claim["provision_id"] != provision_id:
        errors.append("observation provision_id must equal the record provision ID")
    if claim["control_id"] != control_id:
        errors.append("observation control_id must equal the relationship control ID")
    for field in _SEMANTIC_FIELDS:
        errors.extend(_semantic_value_errors(field, claim[field]))
    active_profiles = OBSERVATION_PROFILES if profiles is None else profiles
    pair = (claim["provision_id"], claim["control_id"])
    profile = active_profiles.get(pair)
    if profile is None:
        errors.append("observation pair is not declared in the source-versioned registry")
    else:
        for field in _SEMANTIC_FIELDS:
            if claim[field] != profile.get(field):
                errors.append(f"observation {field} must exactly match the registered pair profile")
    return errors


def validate_observation_registry(
    mapped_pairs: Iterable[tuple[str, str]],
    entries: Iterable[tuple[str, str, str, str, str, str]] = OBSERVATION_PROFILE_ENTRIES,
) -> list[str]:
    """Check that declarations are neutral, unique, and exactly cover mapped legs."""
    declared_entries = list(entries)
    errors: list[str] = []
    declared_pairs: set[tuple[str, str]] = set()
    for entry in declared_entries:
        if len(entry) != 6:
            errors.append("observation profile entry must contain six strings")
            continue
        provision_id, control_id, result_kind, subject, predicate, result_type = entry
        pair = (provision_id, control_id)
        if pair in declared_pairs:
            errors.append(f"duplicate observation profile pair: {provision_id}/{control_id}")
        declared_pairs.add(pair)
        for field, value in zip(
            _SEMANTIC_FIELDS, (result_kind, subject, predicate, result_type), strict=True
        ):
            errors.extend(_semantic_value_errors(field, value))
        if provision_id == "CEPTS3.2-M-001":
            errors.append("observation profile must not target a known negative provision")
        if provision_id.startswith("CEPTS3.2-T5-"):
            errors.append("observation profile must not target an unimplemented Task 5 provision")
    mapped_pair_set = set(mapped_pairs)
    for pair in sorted(mapped_pair_set - declared_pairs):
        errors.append(f"missing observation profile for mapped pair: {pair[0]}/{pair[1]}")
    for pair in sorted(declared_pairs - mapped_pair_set):
        errors.append(f"orphan observation profile pair: {pair[0]}/{pair[1]}")
    return errors
