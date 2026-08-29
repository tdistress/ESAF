"""Frozen mapping-review bundle reviewed-candidate reject policy cases.

The records in this module are deliberately data, rather than executable
mutations, mirroring the qualified-review hot-path inventory in
`tests/qualified_review_policy_cases.py`.  The narrow test support in
`tests/mapping_review_bundle_hot_path_support.py` reconstructs baseline
reviewed mapping-set and mapping-record metadata and then applies these
mutation operations before invoking one pure production boundary from
`tools/build_mapping_review_bundle.py`.

This inventory intentionally selects only the reviewed-candidate reject
mutations that fail inside a pure boundary (`_require_candidate_state`,
`_require_reviewed_findings`, or `validate_metadata_against_schema`) before
package-completeness work becomes the subject of the assertion. Case
population is frozen at 16 and bound by a population digest; see
`docs/superpowers/specs/2026-08-29-validation-harness-bundle-hot-path-design.md`.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Literal, Sequence, TypeAlias


Boundary: TypeAlias = Literal["candidate_state", "schema", "reviewed_findings"]
SubjectKind: TypeAlias = Literal["mapping_set", "record"]
MutationKind: TypeAlias = Literal["set", "remove"]
JsonScalar: TypeAlias = None | bool | int | str
FrozenValue: TypeAlias = (
    JsonScalar | tuple["FrozenValue", ...] | tuple[tuple[str, "FrozenValue"], ...]
)

CORE_MAPPING_SET_ID = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure"
    "--3.3--esaf-0.4-alpha--0.1.0"
)


@dataclass(frozen=True)
class MutationOp:
    kind: MutationKind
    path: tuple[str, ...]
    value: FrozenValue | None = None


@dataclass(frozen=True)
class MappingReviewBundlePolicyCase:
    case_id: str
    method_name: str
    boundary: Boundary
    subject_kind: SubjectKind
    mutations: tuple[MutationOp, ...]
    expected_error_regex: str
    mapping_set_id: str


@dataclass(frozen=True)
class MappingReviewBundlePolicyInventory:
    cases: tuple[MappingReviewBundlePolicyCase, ...]
    population_sha256: str

    def cases_for_method(
        self, method_name: str
    ) -> tuple[MappingReviewBundlePolicyCase, ...]:
        return tuple(
            case for case in self.cases if case.method_name == method_name
        )


def _obj(*items: tuple[str, FrozenValue]) -> tuple[tuple[str, FrozenValue], ...]:
    return items


def _set(path: tuple[str, ...], value: FrozenValue) -> MutationOp:
    return MutationOp("set", path, value)


def _remove(path: tuple[str, ...]) -> MutationOp:
    return MutationOp("remove", path)


def _case(
    case_id: str,
    method_name: str,
    boundary: Boundary,
    subject_kind: SubjectKind,
    mutations: tuple[MutationOp, ...],
    expected_error_regex: str,
) -> MappingReviewBundlePolicyCase:
    return MappingReviewBundlePolicyCase(
        case_id=case_id,
        method_name=method_name,
        boundary=boundary,
        subject_kind=subject_kind,
        mutations=mutations,
        expected_error_regex=expected_error_regex,
        mapping_set_id=CORE_MAPPING_SET_ID,
    )


def _finding(severity: str, status: str) -> tuple[tuple[str, FrozenValue], ...]:
    fields: list[tuple[str, FrozenValue]] = [
        ("finding_id", "review-finding"),
        ("affected_record_ids", ("fixture-record-1",)),
        ("severity", severity),
        ("status", status),
        ("description", "Fixture finding."),
        ("disposition", "Fixture disposition."),
    ]
    if status == "accepted":
        fields.extend(
            [
                ("resolver_or_acceptor", "fixture-acceptor"),
                ("disposition_date", "2026-07-25"),
                ("acceptance_rationale", "Fixture rationale."),
            ]
        )
    return _obj(*fields)


_MIXED_STATUS_CASES: tuple[MappingReviewBundlePolicyCase, ...] = (
    _case(
        "mixed-status:record",
        "test_reviewed_candidate_rejects_mixed_or_approved_states",
        "candidate_state",
        "record",
        (_set(("status",), "draft"),),
        "must be reviewed",
    ),
)

_APPROVED_STATUS_CASES: tuple[MappingReviewBundlePolicyCase, ...] = (
    _case(
        "approved-status:snapshot",
        "test_reviewed_candidate_rejects_mixed_or_approved_states",
        "schema",
        "mapping_set",
        (_set(("status",), "approved"),),
        "candidate schema validation",
    ),
    _case(
        "approved-status:record",
        "test_reviewed_candidate_rejects_mixed_or_approved_states",
        "schema",
        "record",
        (_set(("status",), "approved"),),
        "candidate schema validation",
    ),
)

_MISSING_REVIEWER_CASES: tuple[MappingReviewBundlePolicyCase, ...] = (
    _case(
        "missing-reviewer:snapshot",
        "test_reviewed_candidate_rejects_missing_reviewer_metadata",
        "schema",
        "mapping_set",
        (_remove(("reviewer",)),),
        "candidate schema validation",
    ),
    _case(
        "missing-reviewer:record",
        "test_reviewed_candidate_rejects_missing_reviewer_metadata",
        "schema",
        "record",
        (_remove(("reviewer",)),),
        "candidate schema validation",
    ),
)

_MAPPER_SELF_REVIEW_CASES: tuple[MappingReviewBundlePolicyCase, ...] = (
    _case(
        "mapper-self-review:snapshot",
        "test_reviewed_candidate_rejects_mapper_self_review",
        "candidate_state",
        "mapping_set",
        (_set(("reviewer", "id"), "fixture-mapper"),),
        "reviewer must differ from mapper",
    ),
    _case(
        "mapper-self-review:record",
        "test_reviewed_candidate_rejects_mapper_self_review",
        "candidate_state",
        "record",
        (_set(("reviewer", "id"), "fixture-mapper"),),
        "reviewer must differ from mapper",
    ),
)

_FINDINGS_CASES: tuple[MappingReviewBundlePolicyCase, ...] = (
    _case(
        "findings:critical-open",
        "test_reviewed_candidate_rejects_critical_and_important_findings",
        "reviewed_findings",
        "mapping_set",
        (_set(("findings",), (_finding("Critical", "open"),)),),
        "Critical finding must be resolved",
    ),
    _case(
        "findings:critical-accepted",
        "test_reviewed_candidate_rejects_critical_and_important_findings",
        "reviewed_findings",
        "mapping_set",
        (_set(("findings",), (_finding("Critical", "accepted"),)),),
        "Critical finding must be resolved",
    ),
    _case(
        "findings:important-open",
        "test_reviewed_candidate_rejects_critical_and_important_findings",
        "reviewed_findings",
        "mapping_set",
        (_set(("findings",), (_finding("Important", "open"),)),),
        "Important finding must be resolved",
    ),
    _case(
        "findings:important-accepted",
        "test_reviewed_candidate_rejects_critical_and_important_findings",
        "reviewed_findings",
        "mapping_set",
        (_set(("findings",), (_finding("Important", "accepted"),)),),
        "Important finding must be resolved",
    ),
)

_REQUIRED_REVIEWER_FIELD_CASES: tuple[MappingReviewBundlePolicyCase, ...] = tuple(
    _case(
        f"reviewer-field:{field}",
        "test_reviewed_candidate_rejects_each_required_reviewer_field",
        "schema",
        "mapping_set",
        (_remove(("reviewer", field)),),
        "candidate schema validation",
    )
    for field in (
        "id",
        "qualification",
        "date",
        "authorized_source_access",
        "findings_disposition",
    )
)

CASES: tuple[MappingReviewBundlePolicyCase, ...] = (
    _MIXED_STATUS_CASES
    + _APPROVED_STATUS_CASES
    + _MISSING_REVIEWER_CASES
    + _MAPPER_SELF_REVIEW_CASES
    + _FINDINGS_CASES
    + _REQUIRED_REVIEWER_FIELD_CASES
)


def _semantic_value(value: FrozenValue) -> object:
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


def mapping_review_bundle_population_sha256(
    cases: Sequence[MappingReviewBundlePolicyCase],
) -> str:
    semantic_rows = [
        {
            "case_id": case.case_id,
            "method_name": case.method_name,
            "boundary": case.boundary,
            "subject_kind": case.subject_kind,
            "mapping_set_id": case.mapping_set_id,
            "mutations": [
                {
                    "kind": mutation.kind,
                    "path": list(mutation.path),
                    "value": _semantic_value(mutation.value)
                    if mutation.value is not None
                    else None,
                }
                for mutation in case.mutations
            ],
            "expected_error_regex": case.expected_error_regex,
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


POPULATION_SHA256 = (
    "e424ad26f9dba7cda0663194acc10990d73caa4ce0ead486a52b44fb60302aa1"
)


def _is_frozen_value(value: object) -> bool:
    if value is None or isinstance(value, (bool, int, str)):
        return True
    if not isinstance(value, tuple):
        return False
    if all(
        isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str)
        for item in value
    ):
        return all(_is_frozen_value(item[1]) for item in value)
    return all(_is_frozen_value(item) for item in value)


def validate_mapping_review_bundle_policy_inventory(
    cases: Sequence[MappingReviewBundlePolicyCase],
    population_sha256: str,
) -> None:
    if not isinstance(cases, tuple):
        raise ValueError("inventory collection must be an immutable tuple")
    if len(cases) != 16:
        raise ValueError("case count must remain 16")
    if len({case.case_id for case in cases}) != len(cases):
        raise ValueError("case identifiers must be unique")
    boundary_counts = {"candidate_state": 0, "schema": 0, "reviewed_findings": 0}
    subject_counts = {"mapping_set": 0, "record": 0}
    for case in cases:
        if case.boundary not in boundary_counts:
            raise ValueError("unknown policy boundary")
        boundary_counts[case.boundary] += 1
        if case.subject_kind not in subject_counts:
            raise ValueError("unknown subject kind")
        subject_counts[case.subject_kind] += 1
        if case.mapping_set_id != CORE_MAPPING_SET_ID:
            raise ValueError("case must be bound to the Core mapping set")
        if not case.expected_error_regex:
            raise ValueError("case requires a nonempty expected error regex")
        if not isinstance(case.mutations, tuple) or not case.mutations:
            raise ValueError("case mutations must be a nonempty immutable tuple")
        for mutation in case.mutations:
            if not isinstance(mutation.path, tuple) or not mutation.path:
                raise ValueError("mutation paths must be nonempty tuples")
            if any(not isinstance(token, str) for token in mutation.path):
                raise ValueError("mutation path tokens must be strings")
            if mutation.kind not in ("set", "remove"):
                raise ValueError("unknown mutation kind")
            if mutation.kind == "remove" and mutation.value is not None:
                raise ValueError("remove mutations must not carry a value")
            if mutation.kind == "set" and not _is_frozen_value(mutation.value):
                raise ValueError("mutation values must be recursively immutable")
    if boundary_counts != {
        "candidate_state": 3,
        "schema": 9,
        "reviewed_findings": 4,
    }:
        raise ValueError("boundary distribution must match the reviewed design table")
    if mapping_review_bundle_population_sha256(cases) != population_sha256:
        raise ValueError("population digest does not match the reviewed inventory")


def mapping_review_bundle_policy_inventory() -> MappingReviewBundlePolicyInventory:
    inventory = MappingReviewBundlePolicyInventory(CASES, POPULATION_SHA256)
    validate_mapping_review_bundle_policy_inventory(
        inventory.cases, inventory.population_sha256
    )
    return inventory
