"""Shared fixtures and narrow-boundary runner for mapping-review bundle
hot-path tests.

The baseline fixtures here are minimal valid metadata dicts, sufficient to
pass `crosswalks/schema/mapping-set.schema.json` /
`crosswalks/schema/mapping-record.schema.json` schema validation, the
`_require_candidate_state` reviewed-candidate check, and the
`_require_reviewed_findings` check, before a single declarative mutation
from `tests/mapping_review_bundle_policy_cases.py` is applied.
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from tests.mapping_review_bundle_policy_cases import (
    CORE_MAPPING_SET_ID,
    FrozenValue,
    MappingReviewBundlePolicyCase,
    MutationOp,
)
from tools.build_mapping_review_bundle import (
    _require_candidate_state,
    _require_reviewed_findings,
    validate_metadata_against_schema,
)


ROOT = Path(__file__).resolve().parents[1]

MAPPING_SET_SCHEMA_PATH = "crosswalks/schema/mapping-set.schema.json"
MAPPING_RECORD_SCHEMA_PATH = "crosswalks/schema/mapping-record.schema.json"

_SCHEMA_PATHS = {
    "mapping_set": MAPPING_SET_SCHEMA_PATH,
    "record": MAPPING_RECORD_SCHEMA_PATH,
}
_SUBJECTS = {
    "mapping_set": "mapping set",
    "record": "record fixture.md",
}

MAPPER_ID = "fixture-mapper"
REVIEWER_ID = "independent-reviewer"


def baseline_mapping_set_metadata() -> dict[str, object]:
    """Return a minimal valid reviewed Core mapping-set metadata dict."""
    return {
        "schema_version": "1.0.0",
        "mapping_set_id": CORE_MAPPING_SET_ID,
        "authority": {"id": "uk-ncsc", "name": "UK NCSC"},
        "publication": {"id": "cyber-essentials", "name": "Cyber Essentials"},
        "source_version": {"id": "3.3", "label": "Version 3.3"},
        "esaf_release": {
            "id": "0.4-alpha",
            "label": "ESAF 0.4 Alpha",
            "source_commit_sha": "0" * 40,
            "control_catalog_sha256": "0" * 64,
            "control_manifest_path": "ESAF_CONTROL_MANIFEST.json",
        },
        "mapping_set_version": "0.1.0",
        "status": "reviewed",
        "source": {
            "official_url": "https://example.invalid/source",
            "access_class": "public",
            "licensing_note": "Fixture licensing note.",
        },
        "publication_rights": {
            "basis": "Fixture basis.",
            "permitted_elements": ["identifiers"],
            "prohibited_elements": [],
            "restrictions": "None.",
            "approved": True,
            "reviewer_id": REVIEWER_ID,
            "review_date": "2026-07-25",
            "reviewer_authorized_source_access": True,
            "publication_basis_reviewed": True,
        },
        "scope": {
            "type": "declared_subset",
            "statement": "Fixture scope statement.",
            "inventory_count": 1,
            "default_granularity": "requirement",
        },
        "mapper": {
            "id": MAPPER_ID,
            "qualification": "Fixture mapper qualification.",
            "date": "2026-07-20",
            "authorized_source_access": True,
        },
        "reviewer": {
            "id": REVIEWER_ID,
            "qualification": "Fixture reviewer qualification.",
            "date": "2026-07-25",
            "authorized_source_access": True,
            "findings_disposition": "No Critical or Important findings remain.",
        },
        "findings": [],
        "change_history": [
            {
                "version": "0.1.0",
                "date": "2026-07-20",
                "change": "Initial fixture.",
            }
        ],
    }


def baseline_mapping_record_metadata() -> dict[str, object]:
    """Return a minimal valid reviewed Core mapping-record metadata dict."""
    return {
        "schema_version": "1.0.0",
        "record_id": "fixture-record-1",
        "mapping_set_id": CORE_MAPPING_SET_ID,
        "status": "reviewed",
        "external_provision_id": "fixture-provision-1",
        "granularity": "requirement",
        "context": {
            "mode": "identifier_only",
            "omission_rationale": "Fixture omission rationale.",
        },
        "source_locator": {
            "official_url": "https://example.invalid/source",
            "locator": "Fixture locator.",
        },
        "disposition": "no_direct_mapping",
        "relationships": [],
        "negative_rationale": "Fixture negative rationale.",
        "mapper": {"id": MAPPER_ID, "date": "2026-07-20"},
        "reviewer": {
            "id": REVIEWER_ID,
            "qualification": "Fixture reviewer qualification.",
            "date": "2026-07-25",
            "authorized_source_access": True,
            "findings_disposition": "No Critical or Important findings remain.",
        },
        "change_history": [
            {
                "version": "0.1.0",
                "date": "2026-07-20",
                "change": "Initial fixture.",
            }
        ],
    }


_BASELINE_METADATA = {
    "mapping_set": baseline_mapping_set_metadata,
    "record": baseline_mapping_record_metadata,
}


def _thaw(value: FrozenValue) -> object:
    if isinstance(value, tuple):
        if all(
            isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str)
            for item in value
        ):
            return {key: _thaw(item_value) for key, item_value in value}
        return [_thaw(item) for item in value]
    return value


def _apply_mutation(metadata: dict[str, object], operation: MutationOp) -> None:
    target: Any = metadata
    for token in operation.path[:-1]:
        if not isinstance(target, dict) or token not in target:
            raise ValueError(f"unknown mutation path: {operation.path}")
        target = target[token]
    if not isinstance(target, dict):
        raise ValueError(f"mutation path does not address an object: {operation.path}")
    final = operation.path[-1]
    if operation.kind == "remove":
        if final not in target:
            raise ValueError(f"cannot remove missing field: {operation.path}")
        del target[final]
    elif operation.kind == "set":
        target[final] = _thaw(operation.value)
    else:
        raise ValueError(f"unknown mutation kind: {operation.kind}")


def build_case_metadata(
    case: MappingReviewBundlePolicyCase,
) -> dict[str, object]:
    """Reconstruct the mutated metadata dict for one frozen inventory case."""
    metadata = deepcopy(_BASELINE_METADATA[case.subject_kind]())
    for operation in case.mutations:
        _apply_mutation(metadata, operation)
    return metadata


def load_schema(subject_kind: str) -> object:
    """Load the real candidate-sourced schema for one subject kind."""
    path = ROOT / _SCHEMA_PATHS[subject_kind]
    return json.loads(path.read_bytes())


def run_narrow_case(case: MappingReviewBundlePolicyCase) -> None:
    """Apply one case's mutation and invoke the matching pure boundary.

    Every case in the frozen inventory is a reject case, so a successful
    call here (one that does not raise) indicates the narrow path diverged
    from the reviewed population and the caller should treat that as a
    failure.
    """
    metadata = build_case_metadata(case)
    subject = _SUBJECTS[case.subject_kind]
    if case.boundary == "schema":
        schema = load_schema(case.subject_kind)
        validate_metadata_against_schema(schema, metadata, subject)
    elif case.boundary == "candidate_state":
        _require_candidate_state(metadata, case.mapping_set_id, subject, "reviewed")
    elif case.boundary == "reviewed_findings":
        _require_reviewed_findings(metadata)
    else:
        raise ValueError(f"unknown policy boundary: {case.boundary}")
