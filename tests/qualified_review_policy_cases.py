"""Frozen qualified-review policy cases and the baseline validation ledger.

The records in this module are deliberately data, rather than executable
mutations.  The narrow test support reconstructs fixture-specific values and
then applies these operations without changing this reviewed population.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Literal, Sequence, TypeAlias


BoundaryFamily: TypeAlias = Literal["role_readiness", "draft_reference"]
FixtureKind: TypeAlias = Literal[
    "draft", "reviewed_final", "description_candidate", "duplicate_candidate"
]
CandidateKey: TypeAlias = Literal["draft", "reviewed", "description", "duplicate"]
FullPathRoute: TypeAlias = Literal[
    "draft", "final", "recursive_draft", "validator_cli", "seal_cli"
]
JsonScalar: TypeAlias = None | bool | int | str
FrozenValue: TypeAlias = (
    JsonScalar | tuple["FrozenValue", ...] | tuple[tuple[str, "FrozenValue"], ...]
)

BASELINE_COMMIT = "f99e403583877f803576dcad919025e558e5a5f6"
MAPPING_SET_ID = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3"
    "--esaf-0.4-alpha--0.1.0"
)
ALLOWED_PATH_TOKENS = frozenset(
    {
        "mapping_sets", "roles", "reviewer", "identity", "authorized_source_access",
        "conflicts", "conflict_disposition", "owner_eligibility_accepted",
        "dual_role_accepted", "qualification", "conclusion", "findings",
        "findings_disposition", "post_correction_candidate_sha", "affected_record_ids",
        "severity", "status", "draft_campaign_reference", "campaign_id",
        "candidate_commit", "manifest_sha256", "seal_record_sha256", "reviewer",
        "mapping_metadata", "record_metadata", "description", "finding_id",
        "verification_locator",
        0, 1,
    }
)


@dataclass(frozen=True)
class CandidateReference:
    key: CandidateKey


OperationValue: TypeAlias = FrozenValue | CandidateReference


@dataclass(frozen=True)
class FieldOperation:
    path: tuple[str | int, ...]
    value: OperationValue


@dataclass(frozen=True)
class ExpectedReport:
    evidence_valid: bool
    readiness_name: str
    readiness_value: bool
    candidate_key: CandidateKey
    campaign_id: str
    errors: tuple[str, ...]


@dataclass(frozen=True)
class QualifiedReviewPolicyCase:
    method_name: str
    case_id: str
    boundary: BoundaryFamily
    fixture_kind: FixtureKind
    operations: tuple[FieldOperation, ...]
    expected: ExpectedReport


@dataclass(frozen=True)
class RetainedCaseBaseline:
    case_id: str
    method_name: str
    case_label: str
    routes: tuple[FullPathRoute, ...]
    rationale: str


@dataclass(frozen=True)
class MethodBaseline:
    method_name: str
    detail_entries: int
    selected_entries: int
    retained_cases: tuple[RetainedCaseBaseline, ...]
    copytree_operations: int
    retained_source_ast_sha256: str


@dataclass(frozen=True)
class QualifiedReviewPolicyInventory:
    cases: tuple[QualifiedReviewPolicyCase, ...]
    methods: tuple[MethodBaseline, ...]
    retained_cases: tuple[RetainedCaseBaseline, ...]
    population_sha256: str

    def cases_for_method(self, method_name: str) -> tuple[QualifiedReviewPolicyCase, ...]:
        return tuple(case for case in self.cases if case.method_name == method_name)


def _obj(*items: tuple[str, FrozenValue]) -> tuple[tuple[str, FrozenValue], ...]:
    return items


def _operation(path: tuple[str | int, ...], value: OperationValue) -> FieldOperation:
    return FieldOperation(path, value)


def _report(
    valid: bool,
    ready: bool,
    candidate: CandidateKey = "draft",
    campaign_id: str = "issue-55-draft-review",
    errors: tuple[str, ...] = (),
    readiness_name: str = "transition_ready",
) -> ExpectedReport:
    return ExpectedReport(valid, readiness_name, ready, candidate, campaign_id, errors)


def _error(suffix: str) -> tuple[str, ...]:
    return (f"{MAPPING_SET_ID} {suffix}",)


_FINDING_COMMON = (
    ("finding_id", "review-finding-1"),
    ("affected_record_ids", ("ce33-d-001",)),
    ("disposition", "Resolved in candidate"),
    ("resolver_or_acceptor", "Project Owner"),
    ("disposition_date", "2026-07-25"),
    ("acceptance_rationale", "Not applicable"),
)
_OPEN_CRITICAL = _obj(
    *_FINDING_COMMON[:2],
    ("severity", "Critical"),
    ("status", "open"),
    *_FINDING_COMMON[2:],
)
_OPEN_IMPORTANT = _obj(
    *_FINDING_COMMON[:2],
    ("severity", "Important"),
    ("status", "open"),
    *_FINDING_COMMON[2:],
)
_OPEN_MINOR = _obj(
    *_FINDING_COMMON[:2],
    ("severity", "Minor"),
    ("status", "open"),
    *_FINDING_COMMON[2:],
)
_ACCEPTED_CRITICAL = _obj(
    *_FINDING_COMMON[:2],
    ("severity", "Critical"),
    ("status", "accepted"),
    ("disposition", "Accepted for this release"),
    *_FINDING_COMMON[3:],
)
_ACCEPTED_IMPORTANT = _obj(
    *_FINDING_COMMON[:2],
    ("severity", "Important"),
    ("status", "accepted"),
    ("disposition", "Accepted for this release"),
    *_FINDING_COMMON[3:],
)
_RESOLVED_MINOR = _obj(
    *_FINDING_COMMON[:2],
    ("severity", "Minor"),
    ("status", "resolved"),
    *_FINDING_COMMON[2:],
)
_ORPHAN_OPEN_MINOR = _obj(
    ("finding_id", "review-finding-1"),
    ("affected_record_ids", ("orphan-record",)),
    ("severity", "Minor"),
    ("status", "open"),
    ("disposition", "Resolved in candidate"),
    ("resolver_or_acceptor", "Project Owner"),
    ("disposition_date", "2026-07-25"),
    ("acceptance_rationale", "Not applicable"),
)

_ROLE_CASES: tuple[QualifiedReviewPolicyCase, ...] = (
    QualifiedReviewPolicyCase("test_rejects_ineligible_reviewer_evidence", "ineligible:unauthorized-source-access", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "reviewer", "authorized_source_access"), False),), _report(False, False, errors=_error("specification_and_inventory reviewer is not eligible"))),
    QualifiedReviewPolicyCase("test_rejects_ineligible_reviewer_evidence", "ineligible:mapper-self-review", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "reviewer", "identity"), "esaf-crosswalk-editorial-team"),), _report(False, False, errors=_error("specification_and_inventory reviewer is also a mapper"))),
    QualifiedReviewPolicyCase("test_rejects_ineligible_reviewer_evidence", "ineligible:unresolved-conflict", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "reviewer", "conflicts"), True), _operation(("mapping_sets", 0, "roles", 0, "reviewer", "conflict_disposition"), "Unresolved")), _report(False, False, errors=_error("specification_and_inventory reviewer has an unresolved conflict"))),
    QualifiedReviewPolicyCase("test_rejects_ineligible_reviewer_evidence", "ineligible:pending-conflict-variant", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "reviewer", "conflicts"), True), _operation(("mapping_sets", 0, "roles", 0, "reviewer", "conflict_disposition"), "Resolution pending")), _report(False, False, errors=_error("specification_and_inventory reviewer has an unresolved conflict"))),
    QualifiedReviewPolicyCase("test_rejects_ineligible_reviewer_evidence", "ineligible:rejected-owner-eligibility", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "owner_eligibility_accepted"), False),), _report(False, False, errors=_error("specification_and_inventory reviewer eligibility was rejected"))),
    QualifiedReviewPolicyCase("test_actor_aliases_and_shared_locator_cannot_bypass_role_rules", "actor-alias:case", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 1, "reviewer", "identity"), "UK-NCSC--CYBER-ESSENTIALS-REQUIREMENTS-FOR-IT-INFRASTRUCTURE--3.3--ESAF-0.4-ALPHA--0.1.0 INVENTORY REVIEWER"),), _report(False, False, errors=_error("duplicate reviewer lacks complete dual-role acceptance and qualifications"))),
    QualifiedReviewPolicyCase("test_actor_aliases_and_shared_locator_cannot_bypass_role_rules", "actor-alias:punctuation", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 1, "reviewer", "identity"), "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0-inventory-reviewer"),), _report(False, False, errors=_error("duplicate reviewer lacks complete dual-role acceptance and qualifications"))),
    QualifiedReviewPolicyCase("test_actor_aliases_and_shared_locator_cannot_bypass_role_rules", "actor-alias:unicode", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "reviewer", "identity"), "Jos\u00e9 Reviewer"), _operation(("mapping_sets", 0, "roles", 1, "reviewer", "identity"), "Jose\u0301 Reviewer")), _report(False, False, errors=_error("duplicate reviewer lacks complete dual-role acceptance and qualifications"))),
    QualifiedReviewPolicyCase("test_actor_aliases_and_shared_locator_cannot_bypass_role_rules", "actor-alias:shared-locator", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 1, "reviewer", "identity"), "Different Display Name"), _operation(("mapping_sets", 0, "roles", 1, "reviewer", "verification_locator"), "https://identity.example.invalid/reviewer?version=uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0-inventory")), _report(False, False, errors=_error("duplicate reviewer lacks complete dual-role acceptance and qualifications"))),
    QualifiedReviewPolicyCase("test_actor_alias_cannot_bypass_mapper_independence", "mapper-alias:case", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "reviewer", "identity"), "ESAF-CROSSWALK-EDITORIAL-TEAM"),), _report(False, False, errors=_error("specification_and_inventory reviewer is also a mapper"))),
    QualifiedReviewPolicyCase("test_explicitly_resolved_conflict_is_eligible", "resolved-conflict:recused", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "reviewer", "conflicts"), True), _operation(("mapping_sets", 0, "roles", 0, "reviewer", "conflict_disposition"), "Resolved: reviewer recused from all mapping decisions")), _report(True, True)),
    QualifiedReviewPolicyCase("test_duplicate_human_requires_dual_acceptance_and_both_qualifications", "duplicate-human:without-acceptance", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 1, "reviewer", "identity"), "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0 inventory reviewer"),), _report(False, False, errors=_error("duplicate reviewer lacks complete dual-role acceptance and qualifications"))),
    QualifiedReviewPolicyCase("test_duplicate_human_requires_dual_acceptance_and_both_qualifications", "duplicate-human:incomplete-qualifications", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 1, "reviewer", "identity"), "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0 inventory reviewer"), _operation(("mapping_sets", 0, "roles", 0, "dual_role_accepted"), True), _operation(("mapping_sets", 0, "roles", 1, "dual_role_accepted"), True), _operation(("mapping_sets", 0, "roles", 1, "reviewer", "qualification"), " ")), _report(False, False, errors=_error("duplicate reviewer lacks complete dual-role acceptance and qualifications"))),
    QualifiedReviewPolicyCase("test_stop_with_open_high_severity_is_valid_but_not_ready", "stop-open:critical", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "conclusion"), "stop"), _operation(("mapping_sets", 0, "roles", 0, "findings"), (_OPEN_CRITICAL,))), _report(True, False)),
    QualifiedReviewPolicyCase("test_stop_with_open_high_severity_is_valid_but_not_ready", "stop-open:important", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "conclusion"), "stop"), _operation(("mapping_sets", 0, "roles", 0, "findings"), (_OPEN_IMPORTANT,))), _report(True, False)),
    QualifiedReviewPolicyCase("test_accepted_critical_or_important_is_evidence_invalid", "accepted-severity:critical", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "findings"), (_ACCEPTED_CRITICAL,)),), _report(False, False, errors=_error("Critical finding cannot be accepted"))),
    QualifiedReviewPolicyCase("test_accepted_critical_or_important_is_evidence_invalid", "accepted-severity:important", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "findings"), (_ACCEPTED_IMPORTANT,)),), _report(False, False, errors=_error("Important finding cannot be accepted"))),
    QualifiedReviewPolicyCase("test_pass_rejects_open_findings", "pass-open:minor", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "findings"), (_OPEN_MINOR,)),), _report(False, False, errors=_error("pass conclusion has an open finding"))),
    QualifiedReviewPolicyCase("test_pass_after_correction_binds_exact_campaign_candidate", "post-correction:mismatched", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "conclusion"), "pass_after_correction"), _operation(("mapping_sets", 0, "roles", 0, "post_correction_candidate_sha"), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")), _report(False, False, errors=_error("specification_and_inventory post-correction candidate is not the campaign candidate"))),
    QualifiedReviewPolicyCase("test_pass_after_correction_binds_exact_campaign_candidate", "post-correction:exact", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "conclusion"), "pass_after_correction"), _operation(("mapping_sets", 0, "roles", 0, "post_correction_candidate_sha"), CandidateReference("draft"))), _report(True, True)),
    QualifiedReviewPolicyCase("test_orphan_affected_record_identifier_is_invalid_even_for_stop", "orphan-record:stop", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "conclusion"), "stop"), _operation(("mapping_sets", 0, "roles", 0, "findings"), (_ORPHAN_OPEN_MINOR,))), _report(False, False, errors=_error("finding review-finding-1 references an unknown record"))),
    QualifiedReviewPolicyCase("test_ready_findings_must_equal_authoritative_candidate_findings", "finding-set:mismatch", "role_readiness", "draft", (_operation(("mapping_sets", 0, "roles", 0, "findings"), (_RESOLVED_MINOR,)),), _report(False, False, errors=_error("findings do not equal authoritative candidate findings"))),
    QualifiedReviewPolicyCase("test_ready_findings_bind_authoritative_description", "finding-description:authoritative", "role_readiness", "description_candidate", (), _report(False, False, "description", errors=_error("findings do not equal authoritative candidate findings"))),
    QualifiedReviewPolicyCase("test_duplicate_authoritative_finding_identifiers_are_invalid", "duplicate-finding-id:authoritative", "role_readiness", "duplicate_candidate", (), _report(False, False, "duplicate", errors=_error("candidate finding identifiers are duplicated"))),
    QualifiedReviewPolicyCase("test_reviewed_candidate_requires_exact_nested_reviewer_objects", "reviewed-reviewer:specification", "role_readiness", "reviewed_final", (_operation(("mapping_sets", 0, "roles", 0, "reviewer", "qualification"), "Different signed qualification"),), _report(False, False, "reviewed", "issue-55-final-confirmation", _error("mapping-set reviewer does not equal the specification review evidence"), "merge_ready")),
    QualifiedReviewPolicyCase("test_reviewed_candidate_requires_exact_nested_reviewer_objects", "reviewed-reviewer:security", "role_readiness", "reviewed_final", (_operation(("mapping_sets", 0, "roles", 1, "reviewer", "qualification"), "Different signed qualification"),), _report(False, False, "reviewed", "issue-55-final-confirmation", _error("record reviewer does not equal the security review evidence"), "merge_ready")),
    QualifiedReviewPolicyCase("test_final_pass_after_correction_binds_reviewed_candidate", "final-post-correction:mismatched", "role_readiness", "reviewed_final", (_operation(("mapping_sets", 0, "roles", 0, "conclusion"), "pass_after_correction"), _operation(("mapping_sets", 0, "roles", 0, "post_correction_candidate_sha"), CandidateReference("draft"))), _report(False, False, "reviewed", "issue-55-final-confirmation", _error("specification_and_inventory post-correction candidate is not the campaign candidate"), "merge_ready")),
)

_REFERENCE_CASES: tuple[QualifiedReviewPolicyCase, ...] = (
    QualifiedReviewPolicyCase("test_final_campaign_binds_every_draft_reference_field", "draft-reference:campaign-id", "draft_reference", "reviewed_final", (_operation(("draft_campaign_reference", "campaign_id"), "another-draft-campaign"),), _report(False, False, "reviewed", "issue-55-final-confirmation", ("Draft campaign identifier does not match the reference",), "merge_ready")),
    QualifiedReviewPolicyCase("test_final_campaign_binds_every_draft_reference_field", "draft-reference:candidate-commit", "draft_reference", "reviewed_final", (_operation(("draft_campaign_reference", "candidate_commit"), CandidateReference("reviewed")),), _report(False, False, "reviewed", "issue-55-final-confirmation", ("reviewed and Draft candidate commits must differ",), "merge_ready")),
    QualifiedReviewPolicyCase("test_final_campaign_binds_every_draft_reference_field", "draft-reference:manifest-digest", "draft_reference", "reviewed_final", (_operation(("draft_campaign_reference", "manifest_sha256"), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),), _report(False, False, "reviewed", "issue-55-final-confirmation", ("Draft manifest digest does not match the reference",), "merge_ready")),
    QualifiedReviewPolicyCase("test_final_campaign_binds_every_draft_reference_field", "draft-reference:seal-record-digest", "draft_reference", "reviewed_final", (_operation(("draft_campaign_reference", "seal_record_sha256"), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),), _report(False, False, "reviewed", "issue-55-final-confirmation", ("Draft seal-record digest does not match the reference",), "merge_ready")),
)

CASES = _ROLE_CASES + _REFERENCE_CASES


RETAINED_AST_SHA256 = {
    "test_accepted_minor_requires_named_acceptance_evidence": "23319dd12547114b869fd0815418669c3869e7824e0da17b95b64f76509370b3",
    "test_attestation_source_sets_are_exactly_candidate_bound": "7ca3e58598557954724bc325eba4eefe154875151a9d3cf23246b6f24912be24",
    "test_campaign_tree_and_package_bytes_are_exact": "c750637c9db1cc6caa16c702b52eec3cae96cfd7cae471977e19a1895f8eecd4",
    "test_candidate_schema_cannot_retrieve_external_references": "e9209852b86444d64e0ba63f072353d0be18ad400313450760b903ded8f2ad95",
    "test_clis_sanitize_git_operational_failures": "697fa1a28fd0aed65935fdb639543ca966fc85f925b4031e46328c358e96d515",
    "test_final_campaign_rejects_archive_seal_or_draft_byte_mutation": "ace8500c85285ccdfe1551710bfdb48a033152010a0342853e2c5db0d60e7c38",
    "test_final_campaign_requires_all_preserved_draft_inputs": "dcaf9d0c09653f67b2e12fc700572282349ba9047168d9d9485381ce204d5a2d",
    "test_invalid_report_preserves_parsed_final_campaign_context": "285d29a598e49cbfa0f2573f291bbb643f6c685015d2ba6dd148bcafe76d5668",
    "test_linux_acquisition_rejects_swap_restored_before_revalidation": "6fb410df11aac17c7c17ec481b061ea0fc92db575b64625713f5af3ab86228db",
    "test_rejects_missing_duplicate_and_mismatched_role_keys": "9ee266cb597041d94487abe486f455ab9effe02b339644601932a5c1304a438e",
    "test_retained_draft_revalidation_rejects_mismatched_archive_urn": "276c95fd1102d68ecb6a71c3491f2d0224e67bfca6585c95e8add385eef99261",
    "test_seal_archives_the_exact_validated_byte_snapshot": "ebbc068dcddf2e0ce61a237acb9522c5b0d7863d1e71f4c2668e18d4fe7b6975",
    "test_seal_cli_accepts_only_the_real_archive_digest_urn": "6e8dc8eaa4c6322657a6b80447a51f33353e1bfeb0be7dfde9ece5437f20139f",
    "test_seal_cli_atomically_publishes_exact_archive_and_seal": "6952f8478e7bc5a3930337c5ebfd36522e1ab7524e51987f24d18de7241b9563",
    "test_seal_cli_preserves_competing_output_and_cleans_partial_staging": "6591b5e3411be8eff4d3cd5011c07ce120eba18ec5470326e1ebdf613bcffe9a",
    "test_seal_cli_publishes_nothing_after_execution_state_drift": "ae58a0567c69c7f11ac4b18586f4105198f678ea1038542071dc64b0e02bc49c",
    "test_seal_cli_refuses_invalid_or_nonready_campaign": "a9b95acdc8ebf33a0041c0971584c6da299b1e166af309b8224eb75c1848af0e",
    "test_seal_cli_refuses_existing_worktree_and_unsafe_destinations": "010cf9b4c1b218de9dfb9204744fe9bf5ab4312b44e4884dc2f2fcfdfa75fc5b",
    "test_seal_fails_closed_when_parent_or_ancestor_is_swapped": "cfccdb9ed35deaeb19c72888b1ff9089c60950a2303ceb61bbb034146a665f4c",
    "test_sha_locators_bind_package_attestation_and_worksheet_bytes": "a22158545e4a5da79e435e24539243abcc26972e77a0edd58d8d714b6ddeaf94",
    "test_valid_draft_campaign_is_transition_ready": "448e7b9e1bbdc69159d887033cd05204afd111e71db6fa493affdc9c2e02ecac",
    "test_valid_final_campaign_is_recursively_merge_ready": "6caf1a1f2cc7fd6b2bd255f64a272b02bfef25193d58220c031cd447f8d8c946",
    "test_validator_cli_classifies_preopen_permissions_as_operational": "788950d76b07846f2129eba5c2f17daf16407ce76509c52141383045a8d49ceb",
    "test_validator_cli_emits_canonical_reports_and_exit_codes": "e40d05ed85181a7aeb8e9b2203e7bfe0df8e28077c3b57fe3cbdf6eee00d1c07",
    "test_validator_cli_keeps_batch_object_failure_operational": "2d2c0983d07685de9e1ede5fc90f755712c79a95cd64c2ef8333f66f81216fed",
    "test_validator_cli_requires_check_and_all_or_none_draft_inputs": "243bb8120b599e6a838848615b68a8b1db864ffe3d8bf0bda2cd4dba41d8b19e",
    "test_validator_cli_sanitizes_missing_and_permission_failures": "573b65c526cd6b51147d1b860459f523b9a35f240295c8a8c644d040cece0d46",
}


RETAINED_CASES: tuple[RetainedCaseBaseline, ...] = (
    RetainedCaseBaseline("test_valid_draft_campaign_is_transition_ready:retained:default", "test_valid_draft_campaign_is_transition_ready", "default", ("draft",), "A valid Draft campaign remains the complete acquisition control."),
    RetainedCaseBaseline("test_rejects_missing_duplicate_and_mismatched_role_keys:retained:missing-role", "test_rejects_missing_duplicate_and_mismatched_role_keys", "missing-role", ("draft",), "Campaign schema must reject a missing review role."),
    RetainedCaseBaseline("test_rejects_missing_duplicate_and_mismatched_role_keys:retained:duplicate-role", "test_rejects_missing_duplicate_and_mismatched_role_keys", "duplicate-role", ("draft",), "Role topology must reject a duplicate review role."),
    RetainedCaseBaseline("test_rejects_missing_duplicate_and_mismatched_role_keys:retained:duplicate-mapping-set", "test_rejects_missing_duplicate_and_mismatched_role_keys", "duplicate-mapping-set", ("draft",), "Mapping-set topology must reject duplicate identifiers."),
    RetainedCaseBaseline("test_sha_locators_bind_package_attestation_and_worksheet_bytes:retained:package", "test_sha_locators_bind_package_attestation_and_worksheet_bytes", "package", ("draft",), "Package locator binding remains a complete-path integrity check."),
    RetainedCaseBaseline("test_sha_locators_bind_package_attestation_and_worksheet_bytes:retained:attestation", "test_sha_locators_bind_package_attestation_and_worksheet_bytes", "attestation", ("draft",), "Attestation locator binding remains a complete-path integrity check."),
    RetainedCaseBaseline("test_sha_locators_bind_package_attestation_and_worksheet_bytes:retained:worksheet", "test_sha_locators_bind_package_attestation_and_worksheet_bytes", "worksheet", ("draft",), "Worksheet locator binding remains a complete-path integrity check."),
    RetainedCaseBaseline("test_attestation_source_sets_are_exactly_candidate_bound:retained:0", "test_attestation_source_sets_are_exactly_candidate_bound", "0", ("draft",), "Source checksums must match the candidate package."),
    RetainedCaseBaseline("test_attestation_source_sets_are_exactly_candidate_bound:retained:1", "test_attestation_source_sets_are_exactly_candidate_bound", "1", ("draft",), "Source checksum multiplicity must match the candidate package."),
    RetainedCaseBaseline("test_attestation_source_sets_are_exactly_candidate_bound:retained:2", "test_attestation_source_sets_are_exactly_candidate_bound", "2", ("draft",), "Source checksum completeness must match the candidate package."),
    RetainedCaseBaseline("test_attestation_source_sets_are_exactly_candidate_bound:retained:3", "test_attestation_source_sets_are_exactly_candidate_bound", "3", ("draft",), "Source locators must match the candidate package."),
    RetainedCaseBaseline("test_attestation_source_sets_are_exactly_candidate_bound:retained:4", "test_attestation_source_sets_are_exactly_candidate_bound", "4", ("draft",), "Source locator completeness must match the candidate package."),
    RetainedCaseBaseline("test_attestation_source_sets_are_exactly_candidate_bound:retained:5", "test_attestation_source_sets_are_exactly_candidate_bound", "5", ("draft",), "The source version must match the candidate package."),
    RetainedCaseBaseline("test_accepted_minor_requires_named_acceptance_evidence:retained:resolver_or_acceptor", "test_accepted_minor_requires_named_acceptance_evidence", "resolver_or_acceptor", ("draft",), "Schema validation requires a named acceptance actor."),
    RetainedCaseBaseline("test_accepted_minor_requires_named_acceptance_evidence:retained:acceptance_rationale", "test_accepted_minor_requires_named_acceptance_evidence", "acceptance_rationale", ("draft",), "Schema validation requires an acceptance rationale."),
    RetainedCaseBaseline("test_accepted_minor_requires_named_acceptance_evidence:retained:disposition_date", "test_accepted_minor_requires_named_acceptance_evidence", "disposition_date", ("draft",), "Schema validation requires an acceptance date."),
    RetainedCaseBaseline("test_campaign_tree_and_package_bytes_are_exact:retained:extra-source", "test_campaign_tree_and_package_bytes_are_exact", "extra-source", ("draft",), "The campaign tree must contain only allowlisted source files."),
    RetainedCaseBaseline("test_campaign_tree_and_package_bytes_are_exact:retained:manifest-byte", "test_campaign_tree_and_package_bytes_are_exact", "manifest-byte", ("draft",), "The packaged manifest bytes must remain immutable."),
    RetainedCaseBaseline("test_campaign_tree_and_package_bytes_are_exact:retained:payload-byte", "test_campaign_tree_and_package_bytes_are_exact", "payload-byte", ("draft",), "The packaged payload bytes must remain immutable."),
    RetainedCaseBaseline("test_candidate_schema_cannot_retrieve_external_references:retained:default", "test_candidate_schema_cannot_retrieve_external_references", "default", ("draft",), "Candidate schema handling must not retrieve external references."),
    RetainedCaseBaseline("test_valid_final_campaign_is_recursively_merge_ready:retained:default", "test_valid_final_campaign_is_recursively_merge_ready", "default", ("final", "recursive_draft"), "A valid Final campaign must revalidate its retained Draft evidence."),
    RetainedCaseBaseline("test_invalid_report_preserves_parsed_final_campaign_context:retained:default", "test_invalid_report_preserves_parsed_final_campaign_context", "default", ("final",), "Final reports must preserve parsed campaign context after package failure."),
    RetainedCaseBaseline("test_final_campaign_requires_all_preserved_draft_inputs:retained:no-draft-root", "test_final_campaign_requires_all_preserved_draft_inputs", "no-draft-root", ("final",), "Final validation requires the retained Draft evidence root."),
    RetainedCaseBaseline("test_final_campaign_requires_all_preserved_draft_inputs:retained:no-seal", "test_final_campaign_requires_all_preserved_draft_inputs", "no-seal", ("final",), "Final validation requires the retained Draft seal."),
    RetainedCaseBaseline("test_final_campaign_requires_all_preserved_draft_inputs:retained:no-archive", "test_final_campaign_requires_all_preserved_draft_inputs", "no-archive", ("final",), "Final validation requires the retained Draft archive."),
    RetainedCaseBaseline("test_final_campaign_rejects_archive_seal_or_draft_byte_mutation:retained:archive", "test_final_campaign_rejects_archive_seal_or_draft_byte_mutation", "archive", ("final", "recursive_draft"), "Final validation must reject changed retained archive bytes."),
    RetainedCaseBaseline("test_final_campaign_rejects_archive_seal_or_draft_byte_mutation:retained:seal-version", "test_final_campaign_rejects_archive_seal_or_draft_byte_mutation", "seal-version", ("final", "recursive_draft"), "Final validation must bind the retained seal version."),
    RetainedCaseBaseline("test_final_campaign_rejects_archive_seal_or_draft_byte_mutation:retained:seal-field", "test_final_campaign_rejects_archive_seal_or_draft_byte_mutation", "seal-field", ("final", "recursive_draft"), "Final validation must bind retained seal content."),
    RetainedCaseBaseline("test_final_campaign_rejects_archive_seal_or_draft_byte_mutation:retained:draft", "test_final_campaign_rejects_archive_seal_or_draft_byte_mutation", "draft", ("final", "recursive_draft"), "Final validation must reject Draft evidence changed after sealing."),
    RetainedCaseBaseline("test_retained_draft_revalidation_rejects_mismatched_archive_urn:retained:default", "test_retained_draft_revalidation_rejects_mismatched_archive_urn", "default", ("final", "recursive_draft"), "The retained seal archive locator must bind the reconstructed archive."),
    RetainedCaseBaseline("test_validator_cli_emits_canonical_reports_and_exit_codes:retained:valid", "test_validator_cli_emits_canonical_reports_and_exit_codes", "valid", ("validator_cli",), "The validator CLI must emit the canonical valid report."),
    RetainedCaseBaseline("test_validator_cli_emits_canonical_reports_and_exit_codes:retained:malformed", "test_validator_cli_emits_canonical_reports_and_exit_codes", "malformed", ("validator_cli",), "The validator CLI must emit a canonical invalid report for malformed evidence."),
    RetainedCaseBaseline("test_validator_cli_sanitizes_missing_and_permission_failures:retained:missing", "test_validator_cli_sanitizes_missing_and_permission_failures", "missing", ("validator_cli",), "The validator CLI must sanitize missing-evidence failures."),
    RetainedCaseBaseline("test_validator_cli_sanitizes_missing_and_permission_failures:retained:permission", "test_validator_cli_sanitizes_missing_and_permission_failures", "permission", ("validator_cli",), "The validator CLI must sanitize permission failures."),
    RetainedCaseBaseline("test_validator_cli_classifies_preopen_permissions_as_operational:retained:lstat", "test_validator_cli_classifies_preopen_permissions_as_operational", "lstat", ("validator_cli",), "The validator CLI must classify lstat denial as operational."),
    RetainedCaseBaseline("test_validator_cli_classifies_preopen_permissions_as_operational:retained:iterdir", "test_validator_cli_classifies_preopen_permissions_as_operational", "iterdir", ("validator_cli",), "The validator CLI must classify directory-read denial as operational."),
    RetainedCaseBaseline("test_validator_cli_classifies_preopen_permissions_as_operational:retained:resolve", "test_validator_cli_classifies_preopen_permissions_as_operational", "resolve", ("validator_cli",), "The validator CLI must classify path-resolution denial as operational."),
    RetainedCaseBaseline("test_validator_cli_classifies_preopen_permissions_as_operational:retained:stat", "test_validator_cli_classifies_preopen_permissions_as_operational", "stat", ("validator_cli",), "The validator CLI must classify manifest-stat denial as operational."),
    RetainedCaseBaseline("test_clis_sanitize_git_operational_failures:retained:git", "test_clis_sanitize_git_operational_failures", "git", ("validator_cli",), "The validator CLI must sanitize Git operational failures."),
    RetainedCaseBaseline("test_clis_sanitize_git_operational_failures:retained:decode", "test_clis_sanitize_git_operational_failures", "decode", ("validator_cli",), "The validator CLI must sanitize Git decode failures."),
    RetainedCaseBaseline("test_validator_cli_keeps_batch_object_failure_operational:retained:default", "test_validator_cli_keeps_batch_object_failure_operational", "default", ("validator_cli",), "The validator CLI must keep batch object failures operational."),
    RetainedCaseBaseline("test_seal_cli_atomically_publishes_exact_archive_and_seal:retained:default", "test_seal_cli_atomically_publishes_exact_archive_and_seal", "default", ("seal_cli",), "The seal CLI must publish the exact validated archive and seal."),
    RetainedCaseBaseline("test_seal_cli_accepts_only_the_real_archive_digest_urn:retained:accepted", "test_seal_cli_accepts_only_the_real_archive_digest_urn", "accepted", ("seal_cli",), "The seal CLI must accept the actual archive digest locator."),
    RetainedCaseBaseline("test_seal_cli_accepts_only_the_real_archive_digest_urn:retained:rejected", "test_seal_cli_accepts_only_the_real_archive_digest_urn", "rejected", ("seal_cli",), "The seal CLI must reject a false archive digest locator."),
    RetainedCaseBaseline("test_seal_cli_refuses_invalid_or_nonready_campaign:retained:invalid", "test_seal_cli_refuses_invalid_or_nonready_campaign", "invalid", ("seal_cli",), "The seal CLI must refuse invalid campaign evidence."),
    RetainedCaseBaseline("test_seal_cli_refuses_invalid_or_nonready_campaign:retained:stop", "test_seal_cli_refuses_invalid_or_nonready_campaign", "stop", ("seal_cli",), "The seal CLI must refuse a valid but nonready campaign."),
    RetainedCaseBaseline("test_seal_cli_publishes_nothing_after_execution_state_drift:retained:default", "test_seal_cli_publishes_nothing_after_execution_state_drift", "default", ("seal_cli",), "The seal CLI must not publish after execution-state drift."),
    RetainedCaseBaseline("test_seal_cli_preserves_competing_output_and_cleans_partial_staging:retained:existing-output", "test_seal_cli_preserves_competing_output_and_cleans_partial_staging", "existing-output", ("seal_cli",), "The seal CLI must preserve a competing output directory."),
    RetainedCaseBaseline("test_seal_cli_preserves_competing_output_and_cleans_partial_staging:retained:partial-staging", "test_seal_cli_preserves_competing_output_and_cleans_partial_staging", "partial-staging", ("seal_cli",), "The seal CLI must clean partial staging after failure."),
    RetainedCaseBaseline("test_seal_fails_closed_when_parent_or_ancestor_is_swapped:retained:parent", "test_seal_fails_closed_when_parent_or_ancestor_is_swapped", "parent", ("seal_cli",), "The seal CLI must fail closed when its parent changes."),
    RetainedCaseBaseline("test_seal_fails_closed_when_parent_or_ancestor_is_swapped:retained:ancestor", "test_seal_fails_closed_when_parent_or_ancestor_is_swapped", "ancestor", ("seal_cli",), "The seal CLI must fail closed when an ancestor changes."),
    RetainedCaseBaseline("test_seal_archives_the_exact_validated_byte_snapshot:retained:default", "test_seal_archives_the_exact_validated_byte_snapshot", "default", ("seal_cli",), "The seal archive must match the validated byte snapshot."),
)


_METHOD_ROWS: tuple[tuple[str, int, int, int], ...] = (
    ("test_linux_acquisition_rejects_swap_restored_before_revalidation", 0, 0, 0),
    ("test_valid_draft_campaign_is_transition_ready", 1, 0, 1),
    ("test_rejects_missing_duplicate_and_mismatched_role_keys", 3, 0, 4),
    ("test_rejects_ineligible_reviewer_evidence", 5, 5, 6),
    ("test_actor_aliases_and_shared_locator_cannot_bypass_role_rules", 4, 4, 5),
    ("test_actor_alias_cannot_bypass_mapper_independence", 1, 1, 1),
    ("test_sha_locators_bind_package_attestation_and_worksheet_bytes", 3, 0, 4),
    ("test_attestation_source_sets_are_exactly_candidate_bound", 6, 0, 7),
    ("test_explicitly_resolved_conflict_is_eligible", 1, 1, 1),
    ("test_duplicate_human_requires_dual_acceptance_and_both_qualifications", 2, 2, 3),
    ("test_stop_with_open_high_severity_is_valid_but_not_ready", 2, 2, 3),
    ("test_accepted_critical_or_important_is_evidence_invalid", 2, 2, 3),
    ("test_accepted_minor_requires_named_acceptance_evidence", 3, 0, 4),
    ("test_pass_rejects_open_findings", 1, 1, 1),
    ("test_pass_after_correction_binds_exact_campaign_candidate", 2, 2, 2),
    ("test_orphan_affected_record_identifier_is_invalid_even_for_stop", 1, 1, 1),
    ("test_ready_findings_must_equal_authoritative_candidate_findings", 1, 1, 1),
    ("test_ready_findings_bind_authoritative_description", 1, 1, 1),
    ("test_duplicate_authoritative_finding_identifiers_are_invalid", 1, 1, 1),
    ("test_campaign_tree_and_package_bytes_are_exact", 3, 0, 4),
    ("test_candidate_schema_cannot_retrieve_external_references", 1, 0, 1),
    ("test_valid_final_campaign_is_recursively_merge_ready", 2, 0, 3),
    ("test_invalid_report_preserves_parsed_final_campaign_context", 1, 0, 3),
    ("test_final_campaign_requires_all_preserved_draft_inputs", 3, 0, 3),
    ("test_final_campaign_binds_every_draft_reference_field", 7, 7, 9),
    ("test_final_campaign_rejects_archive_seal_or_draft_byte_mutation", 8, 0, 9),
    ("test_retained_draft_revalidation_rejects_mismatched_archive_urn", 2, 0, 3),
    ("test_reviewed_candidate_requires_exact_nested_reviewer_objects", 2, 2, 5),
    ("test_final_pass_after_correction_binds_reviewed_candidate", 1, 1, 3),
    ("test_validator_cli_emits_canonical_reports_and_exit_codes", 2, 0, 1),
    ("test_validator_cli_requires_check_and_all_or_none_draft_inputs", 0, 0, 1),
    ("test_validator_cli_sanitizes_missing_and_permission_failures", 2, 0, 1),
    ("test_validator_cli_classifies_preopen_permissions_as_operational", 4, 0, 1),
    ("test_clis_sanitize_git_operational_failures", 2, 0, 1),
    ("test_validator_cli_keeps_batch_object_failure_operational", 1, 0, 1),
    ("test_seal_cli_atomically_publishes_exact_archive_and_seal", 1, 0, 1),
    ("test_seal_cli_accepts_only_the_real_archive_digest_urn", 2, 0, 1),
    ("test_seal_cli_refuses_invalid_or_nonready_campaign", 2, 0, 3),
    ("test_seal_cli_refuses_existing_worktree_and_unsafe_destinations", 0, 0, 1),
    ("test_seal_cli_publishes_nothing_after_execution_state_drift", 1, 0, 1),
    ("test_seal_cli_preserves_competing_output_and_cleans_partial_staging", 2, 0, 1),
    ("test_seal_fails_closed_when_parent_or_ancestor_is_swapped", 2, 0, 1),
    ("test_seal_archives_the_exact_validated_byte_snapshot", 1, 0, 1),
)


METHODS = tuple(
    MethodBaseline(
        method_name,
        detail_entries,
        selected_entries,
        tuple(
            retained_case
            for retained_case in RETAINED_CASES
            if retained_case.method_name == method_name
        ),
        copytree_operations,
        RETAINED_AST_SHA256.get(method_name, ""),
    )
    for method_name, detail_entries, selected_entries, copytree_operations in _METHOD_ROWS
)


def _semantic_value(value: OperationValue) -> object:
    if isinstance(value, CandidateReference):
        return {"candidate_reference": value.key}
    if isinstance(value, tuple):
        if all(
            isinstance(item, tuple)
            and len(item) == 2
            and isinstance(item[0], str)
            for item in value
        ):
            return {key: _semantic_value(item_value) for key, item_value in value}
        return [_semantic_value(item) for item in value]
    return value


def qualified_review_population_sha256(
    cases: Sequence[QualifiedReviewPolicyCase],
) -> str:
    semantic_rows = [
        {
            "method_name": case.method_name,
            "case_id": case.case_id,
            "boundary": case.boundary,
            "fixture_kind": case.fixture_kind,
            "operations": [
                {
                    "path": list(operation.path),
                    "value": _semantic_value(operation.value),
                }
                for operation in case.operations
            ],
            "expected": {
                "evidence_valid": case.expected.evidence_valid,
                "readiness_name": case.expected.readiness_name,
                "readiness_value": case.expected.readiness_value,
                "candidate_key": case.expected.candidate_key,
                "campaign_id": case.expected.campaign_id,
                "errors": list(case.expected.errors),
            },
        }
        for case in cases
    ]
    payload = json.dumps(
        semantic_rows,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _retained_method_ast_sha256(source: str) -> dict[str, str]:
    tree = ast.parse(source)
    methods = {
        node.name: hashlib.sha256(
            ast.dump(
                node,
                annotate_fields=True,
                include_attributes=False,
            ).encode("utf-8")
        ).hexdigest()
        for class_node in tree.body
        if isinstance(class_node, ast.ClassDef)
        for node in class_node.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in RETAINED_AST_SHA256
    }
    if set(methods) != set(RETAINED_AST_SHA256):
        raise ValueError("AST source does not contain every retained method")
    return methods


def retained_method_ast_sha256_from_baseline() -> dict[str, str]:
    """Return location-free AST hashes for retained methods at the pinned commit."""
    result = subprocess.run(
        [
            "git",
            "show",
            f"{BASELINE_COMMIT}:tests/test_validate_qualified_review_evidence.py",
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return _retained_method_ast_sha256(result.stdout)


def retained_method_ast_sha256_from_current_source() -> dict[str, str]:
    """Return location-free AST hashes for retained methods in this candidate."""
    source_path = Path(__file__).with_name(
        "test_validate_qualified_review_evidence.py"
    )
    return _retained_method_ast_sha256(source_path.read_text(encoding="utf-8"))


REVIEWED_POPULATION_SHA256 = "d55df00837cd8be7b93cc24177e85cc158aec0f8faae7a7d8dde41710d97ab0a"


def _is_frozen_value(value: object) -> bool:
    if value is None or isinstance(value, (bool, int, str)):
        return True
    if not isinstance(value, tuple):
        return False
    if all(
        isinstance(item, tuple)
        and len(item) == 2
        and isinstance(item[0], str)
        for item in value
    ):
        return all(_is_frozen_value(item[1]) for item in value)
    return all(_is_frozen_value(item) for item in value)


def validate_qualified_review_policy_inventory(
    cases: Sequence[QualifiedReviewPolicyCase],
    methods: Sequence[MethodBaseline],
    population_sha256: str,
) -> None:
    if not isinstance(cases, tuple) or not isinstance(methods, tuple):
        raise ValueError("inventory collections must be immutable tuples")
    if len(methods) != 43:
        raise ValueError("method count must remain 43")
    if len(cases) != 31:
        raise ValueError("case count must remain 31")
    if len({case.case_id for case in cases}) != len(cases):
        raise ValueError("case identifiers must be unique")
    if len({method.method_name for method in methods}) != len(methods):
        raise ValueError("method names must be unique")
    if sum(method.detail_entries for method in methods) != 92:
        raise ValueError("detail-entry total must remain 92")
    if sum(method.selected_entries for method in methods) != 34:
        raise ValueError("selected-entry total must remain 34")
    if sum(method.copytree_operations for method in methods) != 108:
        raise ValueError("copytree total must remain 108")
    if sum(case.boundary == "role_readiness" for case in cases) != 27:
        raise ValueError("role-readiness case count must remain 27")
    if sum(case.boundary == "draft_reference" for case in cases) != 4:
        raise ValueError("Draft-reference case count must remain 4")
    for case in cases:
        if case.boundary not in {"role_readiness", "draft_reference"}:
            raise ValueError("unknown boundary family")
        if case.fixture_kind not in {
            "draft", "reviewed_final", "description_candidate", "duplicate_candidate",
        }:
            raise ValueError("unknown fixture kind")
        if not isinstance(case.operations, tuple) or not isinstance(case.expected.errors, tuple):
            raise ValueError("case values must be immutable tuples")
        if case.expected.candidate_key not in {
            "draft", "reviewed", "description", "duplicate",
        }:
            raise ValueError("unknown expected candidate key")
        for operation in case.operations:
            if not isinstance(operation.path, tuple) or not operation.path:
                raise ValueError("operation paths must be nonempty tuples")
            if any(
                not isinstance(token, (str, int)) or token not in ALLOWED_PATH_TOKENS
                for token in operation.path
            ):
                raise ValueError("operation path has an unsupported token")
            if isinstance(operation.value, CandidateReference):
                if operation.value.key not in {
                    "draft", "reviewed", "description", "duplicate",
                }:
                    raise ValueError("unknown candidate reference")
            elif not _is_frozen_value(operation.value):
                raise ValueError("operation values must be recursively immutable")
    retained_cases = tuple(
        retained_case
        for method in methods
        for retained_case in method.retained_cases
    )
    if len({case.case_id for case in retained_cases}) != len(retained_cases):
        raise ValueError("retained case identifiers must be unique")
    if sum(len(case.routes) for case in retained_cases) != 58:
        raise ValueError("retained route total must remain 58")
    if sum(method.detail_entries - method.selected_entries for method in methods) != 58:
        raise ValueError("retained entry total must remain 58")
    for method in methods:
        if method.retained_cases != tuple(
            retained_case
            for retained_case in retained_cases
            if retained_case.method_name == method.method_name
        ):
            raise ValueError("method retained cases must be ordered")
        if sum(len(case.routes) for case in method.retained_cases) != (
            method.detail_entries - method.selected_entries
        ):
            raise ValueError("retained routes must match the baseline ledger")
        expected_ast = RETAINED_AST_SHA256.get(method.method_name, "")
        if method.retained_source_ast_sha256 != expected_ast:
            raise ValueError("retained source AST oracle changed")
    for retained_case in retained_cases:
        if retained_case.case_id != (
            f"{retained_case.method_name}:retained:{retained_case.case_label}"
        ):
            raise ValueError("retained case identifier is invalid")
        if not retained_case.case_label or not retained_case.rationale:
            raise ValueError("retained cases require invariant rationales")
        if not isinstance(retained_case.routes, tuple) or not retained_case.routes:
            raise ValueError("retained routes must be nonempty tuples")
        if any(
            route not in {"draft", "final", "recursive_draft", "validator_cli", "seal_cli"}
            for route in retained_case.routes
        ):
            raise ValueError("retained route is invalid")
    if qualified_review_population_sha256(cases) != population_sha256:
        raise ValueError("population digest does not match the reviewed inventory")


def qualified_review_policy_inventory() -> QualifiedReviewPolicyInventory:
    inventory = QualifiedReviewPolicyInventory(
        CASES,
        METHODS,
        RETAINED_CASES,
        REVIEWED_POPULATION_SHA256,
    )
    validate_qualified_review_policy_inventory(
        inventory.cases,
        inventory.methods,
        inventory.population_sha256,
    )
    return inventory
