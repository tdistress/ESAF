from __future__ import annotations

import re
import json
import unittest
from collections import Counter
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import tools.crosswalks.uk_ce_plus_v32_reverse_profile as reverse_profile
import tools.crosswalks.validation as crosswalk_validation
from tools.crosswalks.digests import snapshot_digest
from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.manifest import build_control_manifest, render_manifest
from tools.crosswalks.validation import validate
from tools.crosswalks.uk_ce_plus_v32_reverse_profile import (
    OBSERVATION_PROFILE_ENTRIES,
    OBSERVATION_PROFILES,
    build_observation_profiles,
    render_observation_claim,
    validate_observation_claim,
    validate_observation_registry,
)

ROOT = Path(__file__).parents[1]
MAPPING_SET_ID = "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0"
SNAPSHOT = ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0"
REGISTRY = ROOT / "crosswalks/registry" / f"{MAPPING_SET_ID}.md"
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RIGHTS = ROOT / "docs/superpowers/reviews/2026-07-19-uk-cyber-essentials-plus-v3.2-external-to-esaf-mapping-rights-attestation.md"
ORACLE_SHA256 = "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc"
CANONICAL_PDF_SHA256 = "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8"
LEGACY_PDF_SHA256 = "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694"
FEASIBILITY_RIGHTS_COMMIT = "4207e1c1e8ff9f743274ebb4b626210cca053458"
MAPPER_ID = "esaf-crosswalk-editorial-team"
BASELINE_SHA = "7461d7137e3faf36b2b73a15f71100fa4ce11159"
EXPECTED_GROUP_COUNTS = {"M": 24, "T1": 16, "S": 11, "T2": 9, "T3": 37, "T4": 9, "T5": 7, "C": 13, "A": 4, "B": 14}
CONDITION_ORDER = (
    "actor", "scope", "population", "sample", "assessment_date", "evidence_date",
    "tool", "provenance", "exception", "delivery_partner_discretion", "point_in_time_status",
)
PROHIBITED_INFERENCE_KEYS = (
    "implementation",
    "effectiveness",
    "sufficiency",
    "compliance",
    "certification",
    "equivalence",
    "continuous_assurance",
    "population_wide_coverage",
    "current_scheme_coverage",
)
REVIEW_SEMANTIC_BYPASSES = {
    "unsuccessful_status": "must be outcome-neutral",
    "failures_recorded": "must be outcome-neutral",
    "noncompliance_status": "must be outcome-neutral",
    "certifying_status": "must be outcome-neutral",
    "passes_status": "must be outcome-neutral",
    "critical_risk": "must not encode a threshold classification",
    "medium_risk": "must not encode a threshold classification",
    "nmap_authorization": (
        "must not describe mere tool use or assessment procedure activity"
    ),
    "actor_activity_status": (
        "must not describe mere tool use or assessment procedure activity"
    ),
    "procedure_performance": (
        "must not describe mere tool use or assessment procedure activity"
    ),
    "assessment_performance": (
        "must not describe mere tool use or assessment procedure activity"
    ),
    "continuous_assurance": "must be outcome-neutral",
}
VALID_PROVISION_ID = "CEPTS3.2-T1-011"
VALID_CONTROL_ID = "IAM-110"
VALID_OBSERVATION = render_observation_claim(VALID_PROVISION_ID, VALID_CONTROL_ID)
VALID_SUPPORTED_OUTCOME = (
    "requires identities to be authenticated before access to non-public AI assets "
    "using mechanisms whose strength, context, and resistance are proportionate to risk."
)
TASK3_GROUP_COUNTS = {"M": 24, "T1": 16, "S": 11}
TASK4_GROUP_COUNTS = {"T2": 9, "T3": 37, "T4": 9}
TASK5_GROUP_COUNTS = {"T5": 7, "C": 13, "A": 4, "B": 14}
AUTHORED_GROUP_COUNTS = TASK3_GROUP_COUNTS | TASK4_GROUP_COUNTS | TASK5_GROUP_COUNTS
TASK3_POSITIVE_TARGETS = {
    "CEPTS3.2-M-004": "AUD-120",
    "CEPTS3.2-M-010": "AUD-130",
    "CEPTS3.2-M-011": "AUD-120",
    "CEPTS3.2-T1-009": "INF-120",
    "CEPTS3.2-T1-011": "IAM-110",
    "CEPTS3.2-T1-012": "IAM-110",
    "CEPTS3.2-T1-013": "IAM-140",
    "CEPTS3.2-T1-014": "APP-150",
    "CEPTS3.2-T1-015": "APP-150",
    "CEPTS3.2-S-007": "AUD-120",
    "CEPTS3.2-S-008": "CMP-110",
}
TASK4_POSITIVE_TARGETS = {
    "CEPTS3.2-T2-007": "INF-120",
    "CEPTS3.2-T3-005": "INF-110",
    "CEPTS3.2-T3-015": "INF-110",
    "CEPTS3.2-T3-016": "INF-110",
    "CEPTS3.2-T3-017": "INF-110",
    "CEPTS3.2-T3-021": "INF-110",
    "CEPTS3.2-T3-022": "INF-110",
    "CEPTS3.2-T3-023": "INF-110",
    "CEPTS3.2-T3-024": "INF-110",
    "CEPTS3.2-T3-025": "INF-110",
    "CEPTS3.2-T3-027": "INF-110",
    "CEPTS3.2-T3-028": "INF-110",
    "CEPTS3.2-T3-029": "INF-110",
    "CEPTS3.2-T3-031": "INF-110",
    "CEPTS3.2-T3-032": "INF-130",
    "CEPTS3.2-T3-033": "INF-110",
    "CEPTS3.2-T3-034": "INF-110",
    "CEPTS3.2-T3-035": "INF-110",
    "CEPTS3.2-T3-036": "INF-110",
    "CEPTS3.2-T4-008": "IAM-110",
}
TASK5_POSITIVE_TARGETS = {
    "CEPTS3.2-T5-006": "IAM-130",
}

EXPECTED_OBSERVATION_PROFILE_ENTRIES = (
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
    ("CEPTS3.2-T5-006", "IAM-130", "privileged_access_control", "administrative_process_access", "restriction_and_separate_authentication_status", "recorded_status"),
)


def load_snapshot_records() -> list[dict[str, object]]:
    return [
        parse_front_matter(path)[0]
        for path in sorted(SNAPSHOT.glob("*.md"))
        if path.name not in {"README.md", "PROVISION_INVENTORY.md"}
    ]


def load_task3_records() -> list[dict[str, object]]:
    by_external_id = {
        record["external_provision_id"]: record
        for record in load_snapshot_records()
        if record.get("external_metadata", {}).get("group") in TASK3_GROUP_COUNTS
    }
    oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
    return [
        by_external_id[item["external_provision_id"]]
        for item in oracle["provisions"]
        if item["external_provision_id"] in by_external_id
    ]


def load_task4_records() -> list[dict[str, object]]:
    by_external_id = {
        record["external_provision_id"]: record
        for record in load_snapshot_records()
        if record.get("external_metadata", {}).get("group") in TASK4_GROUP_COUNTS
    }
    oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
    return [
        by_external_id[item["external_provision_id"]]
        for item in oracle["provisions"]
        if item["external_provision_id"] in by_external_id
    ]


def load_task5_records() -> list[dict[str, object]]:
    by_external_id = {
        record["external_provision_id"]: record
        for record in load_snapshot_records()
        if record.get("external_metadata", {}).get("group") in TASK5_GROUP_COUNTS
    }
    oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
    return [
        by_external_id[item["external_provision_id"]]
        for item in oracle["provisions"]
        if item["external_provision_id"] in by_external_id
    ]


def reverse_profile_inputs() -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    mapping_set, _ = parse_front_matter(SNAPSHOT / "README.md")
    manifest = json.loads(
        (SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").read_text(encoding="utf-8")
    )
    controls = {item["id"]: item for item in manifest["controls"]}
    return mapping_set, controls


def condition_entry(
    condition: str,
    status: str = "SATISFIED",
    evidence_references: list[str] | None = None,
) -> str:
    return json.dumps(
        {
            "condition": condition,
            "status": status,
            "evidence_references": (
                evidence_references
                if evidence_references is not None
                else ["record:source_locator", "manifest:IAM-130#requirement"]
            ),
        },
        separators=(",", ":"),
        sort_keys=True,
    )


def required_prohibited_inferences(
    external_id: str,
    observation: str = VALID_OBSERVATION,
    control_id: str = VALID_CONTROL_ID,
) -> list[str]:
    explanations = {
        "implementation": "does not establish control implementation",
        "effectiveness": "does not establish control effectiveness",
        "sufficiency": "is not sufficient evidence",
        "compliance": "does not establish ESAF compliance",
        "certification": "does not authorize or establish certification",
        "equivalence": "is not equivalent",
        "continuous_assurance": "does not provide continuous assurance",
        "population_wide_coverage": "does not establish population-wide coverage",
        "current_scheme_coverage": "does not establish current-scheme coverage",
    }
    return [
        f'{external_id} | prohibit {key}: The observed result "{observation}" '
        f"{explanations[key]} for the cited {control_id} outcome."
        for key in PROHIBITED_INFERENCE_KEYS
    ]


def condition_evidence(external_id: str) -> list[str]:
    return [
        f"actor evidence: {external_id} identifies the Assessor responsible for the observed result.",
        f"scope evidence: {external_id} identifies the in-scope AI service and privileged authentication path.",
        f"population evidence: {external_id} defines the applicable authentication population for the in-scope path.",
        f"sample evidence: {external_id} identifies the sample selected from that defined population and the selection basis.",
        f"assessment_date evidence: {external_id} records the assessment date and timezone for the observed result.",
        f"evidence_date evidence: {external_id} records the evidence-collection date and timezone separately from the assessment date.",
        f"tool evidence: {external_id} names the approved tool and version or the documented manual observation method.",
        f"provenance evidence: {external_id} links the source artifacts, source locator, and cited ESAF requirement.",
        f"exception evidence: {external_id} records that no exception affected the result or identifies its approval and disposition.",
        f"delivery_partner_discretion evidence: {external_id} records the applicable Delivery Partner choice, method, or approval, or the basis for no discretion affecting the result.",
        f"point_in_time_status evidence: {external_id} limits the result to the assessment and evidence dates, defined population, and sample; later state is excluded.",
    ]


def condition_references(control_id: str) -> dict[str, list[str]]:
    return {
        "actor": ["relationship:expected_evidence:0", "record:external_metadata"],
        "scope": [
            "relationship:expected_evidence:1",
            "record:context",
            f"manifest:{control_id}#requirement",
        ],
        "population": ["relationship:expected_evidence:2"],
        "sample": ["relationship:expected_evidence:3"],
        "assessment_date": ["relationship:expected_evidence:4"],
        "evidence_date": ["relationship:expected_evidence:5"],
        "tool": ["relationship:expected_evidence:6"],
        "provenance": [
            "relationship:expected_evidence:7",
            "record:source_locator",
            f"manifest:{control_id}#requirement",
        ],
        "exception": ["relationship:expected_evidence:8"],
        "delivery_partner_discretion": ["relationship:expected_evidence:9"],
        "point_in_time_status": [
            "relationship:expected_evidence:10",
            "relationship:known_gaps:0",
        ],
    }


def set_profile_observation(record: dict[str, object], observation: str) -> None:
    normalized_observation = observation.rstrip(". ")
    leg = record["relationships"][0]
    control_id = leg["esaf_control_id"]
    leg["rationale"] = (
        f"External observation: {normalized_observation}. Supported ESAF outcome: "
        f"{control_id} {VALID_SUPPORTED_OUTCOME} Conditions only "
        "narrow this supported claim; they do not create either outcome."
    )
    leg["prohibited_inferences"] = required_prohibited_inferences(
        record["external_provision_id"],
        normalized_observation,
        control_id,
    )


def valid_profile_record() -> dict[str, object]:
    _, controls = reverse_profile_inputs()
    control = controls[VALID_CONTROL_ID]
    return {
        "external_provision_id": VALID_PROVISION_ID,
        "disposition": "mapped",
        "context": {
            "mode": "paraphrase",
            "summary": "Observe a bounded authentication result.",
        },
        "source_locator": {"official_url": "https://example.com/source", "locator": "M-001"},
        "external_metadata": {
            "group": "M",
            "kind": "procedure_step",
            "actors": ["Assessor"],
        },
        "relationships": [
            {
                "esaf_control_id": VALID_CONTROL_ID,
                "esaf_control_version": control["version"],
                "esaf_control_path": control["path"],
                "esaf_control_sha256": control["record_sha256"],
                "esaf_requirement_locator": f"controls/{control['path']}#requirement",
                "direction": "external_to_esaf",
                "rationale": (
                    f"External observation: {VALID_OBSERVATION}. "
                    f"Supported ESAF outcome: {VALID_CONTROL_ID} "
                    f"{VALID_SUPPORTED_OUTCOME} "
                    "Conditions only narrow this supported claim; they do not create either outcome."
                ),
                "conditions": [
                    condition_entry(
                        condition,
                        evidence_references=condition_references(VALID_CONTROL_ID)[condition],
                    )
                    for condition in CONDITION_ORDER
                ],
                "expected_evidence": condition_evidence(VALID_PROVISION_ID),
                "known_gaps": ["Population-wide and continuous operation are not established."],
                "prohibited_inferences": required_prohibited_inferences(
                    VALID_PROVISION_ID
                ),
            }
        ],
    }


class CyberEssentialsPlusExternalToEsafMappingTests(unittest.TestCase):
    def test_production_validator_exposes_reverse_evidence_profile(self) -> None:
        self.assertTrue(
            hasattr(crosswalk_validation, "validate_reverse_evidence_record")
        )

    def test_all_32_persisted_positives_satisfy_the_structured_contract(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        records = load_snapshot_records()
        positives = [record for record in records if record.get("disposition") == "mapped"]
        negatives = [record for record in records if record.get("disposition") != "mapped"]
        self.assertEqual(len(positives), 32)
        for record in positives:
            with self.subTest(external_id=record["external_provision_id"]):
                self.assertEqual(
                    crosswalk_validation.validate_reverse_evidence_record(
                        record, mapping_set, controls
                    ),
                    [],
                )
        self.assertEqual(
            [
                message
                for record in negatives
                for message in crosswalk_validation.validate_reverse_evidence_record(
                    record, mapping_set, controls
                )
            ],
            [],
        )

    def test_mapping_identity_root_and_oracle_are_locked(self) -> None:
        self.assertEqual(
            MAPPING_SET_ID,
            "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
        )
        self.assertEqual(
            SNAPSHOT.relative_to(ROOT).as_posix(),
            "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0",
        )
        self.assertTrue(ORACLE.is_file())

    def test_rights_attestation_is_independent_and_exact(self) -> None:
        self.assertTrue(RIGHTS.is_file())
        text = RIGHTS.read_text(encoding="utf-8")
        lines = text.splitlines()

        for value in (
            f"oracle: {ORACLE.relative_to(ROOT).as_posix()}",
            f"oracle_sha256: {ORACLE_SHA256}",
            f"canonical_pdf_sha256: {CANONICAL_PDF_SHA256}",
            f"legacy_pdf_sha256: {LEGACY_PDF_SHA256}",
            f"feasibility_rights_commit: {FEASIBILITY_RIGHTS_COMMIT}",
            "attribution: National Cyber Security Centre; Crown copyright",
            "licence: Open Government Licence v3.0",
            "ogl_v3_url: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            "copied requirement or passage text: prohibited",
            "IASME source-derived structure: prohibited",
            "marks and imagery: excluded",
            "source_version_boundary: public NCSC v3.2 only; current operational scheme not inferred",
            "direction: external_to_esaf",
            "reviewer_authorized_source_access: true",
            "field_classes: identifiers | titles where used | structural inventory | original paraphrases | derivative mapping analysis | ESAF normative citations | assurance analysis | official links",
            "disposition: approved",
        ):
            self.assertIn(value, lines)

        reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", text)
        self.assertIsNotNone(reviewer)
        self.assertNotEqual(reviewer.group(1), MAPPER_ID)
        self.assertNotIn("conditional approval", text.lower())

    def test_draft_scaffold_has_locked_complete_publication_shape(self) -> None:
        self.assertTrue((SNAPSHOT / "README.md").is_file())
        self.assertTrue((SNAPSHOT / "PROVISION_INVENTORY.md").is_file())
        self.assertTrue((SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").is_file())
        self.assertTrue(REGISTRY.is_file())
        mapping, _ = parse_front_matter(SNAPSHOT / "README.md")
        inventory, _ = parse_front_matter(SNAPSHOT / "PROVISION_INVENTORY.md")
        lifecycle, lifecycle_body = parse_front_matter(REGISTRY)
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        provision_ids = [item["external_provision_id"] for item in oracle["provisions"]]

        self.assertEqual(mapping["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(mapping["mapping_set_version"], "0.2.0")
        self.assertEqual(mapping["status"], "draft")
        self.assertEqual(mapping["esaf_release"]["source_commit_sha"], BASELINE_SHA)
        self.assertEqual(oracle["counts"], {"total": 144, "by_group": EXPECTED_GROUP_COUNTS})
        self.assertEqual(Counter(item["group"] for item in oracle["provisions"]), Counter(EXPECTED_GROUP_COUNTS))
        self.assertEqual(inventory["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(inventory["expected_count"], 144)
        self.assertEqual(inventory["provision_ids"], provision_ids)
        self.assertEqual(lifecycle["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(lifecycle["events"], [])
        self.assertIn("state: draft", lifecycle_body)
        self.assertEqual(lifecycle["snapshot_digest"], snapshot_digest(ROOT, SNAPSHOT))
        records = load_snapshot_records()
        self.assertEqual(
            Counter(record["external_metadata"]["group"] for record in records),
            Counter(AUTHORED_GROUP_COUNTS),
        )
        self.assertEqual(validate(ROOT).errors, [])

    def test_manifest_is_deterministic_at_pinned_esaf_commit(self) -> None:
        expected = build_control_manifest(ROOT, BASELINE_SHA, "0.4-alpha", None)
        self.assertEqual(len(expected["controls"]), 91)
        self.assertEqual(
            (SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").read_text(encoding="utf-8"),
            render_manifest(expected),
        )

    def test_draft_catalog_entry_contains_authored_records(self) -> None:
        catalog = json.loads((ROOT / "crosswalks/catalog.json").read_text(encoding="utf-8"))
        entry = next(item for item in catalog["mapping_sets"] if item["metadata"]["mapping_set_id"] == MAPPING_SET_ID)
        self.assertEqual(entry["metadata"]["status"], "draft")
        self.assertEqual(entry["inventory"]["expected_count"], 144)
        self.assertEqual(len(entry["provisions"]), sum(AUTHORED_GROUP_COUNTS.values()))
        self.assertEqual(entry["lifecycle"]["events"], [])

    def test_task3_records_are_loaded_once_in_locked_oracle_order(self) -> None:
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        expected = [
            item["external_provision_id"]
            for item in oracle["provisions"]
            if item["group"] in TASK3_GROUP_COUNTS
        ]
        records = load_task3_records()
        self.assertEqual(len(records), sum(TASK3_GROUP_COUNTS.values()))
        self.assertEqual(
            [record["external_provision_id"] for record in records], expected
        )

    def test_task3_positives_have_exact_targets_and_condition_contract(self) -> None:
        records = load_task3_records()
        positives = {
            record["external_provision_id"]: record["relationships"]
            for record in records
            if record["disposition"] == "mapped"
        }
        self.assertEqual(set(positives), set(TASK3_POSITIVE_TARGETS))
        for external_id, relationships in positives.items():
            with self.subTest(external_id=external_id):
                self.assertEqual(len(relationships), 1)
                leg = relationships[0]
                self.assertEqual(
                    leg["esaf_control_id"], TASK3_POSITIVE_TARGETS[external_id]
                )
                self.assertEqual(leg["direction"], "external_to_esaf")
                parsed = [json.loads(item) for item in leg["conditions"]]
                self.assertEqual(
                    [item["condition"] for item in parsed], list(CONDITION_ORDER)
                )
                self.assertTrue(
                    all(item["evidence_references"] for item in parsed)
                )

    def test_task3_negatives_use_exact_provision_specific_missing_outcomes(self) -> None:
        records = load_task3_records()
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        expected_task3_ids = {
            item["external_provision_id"]
            for item in oracle["provisions"]
            if item["group"] in TASK3_GROUP_COUNTS
        }
        negatives = {
            record["external_provision_id"]: record
            for record in records
            if record["disposition"] == "no_direct_mapping"
        }
        self.assertEqual(
            set(negatives),
            expected_task3_ids - set(TASK3_POSITIVE_TARGETS),
        )
        self.assertEqual(
            negatives["CEPTS3.2-M-001"]["negative_rationale"],
            "Missing outcome: CEPTS3.2-M-001 - external result 'assessment "
            "boundary' does not evidence ESAF outcome 'risk-based AI assessment "
            "program scope'.",
        )
        for external_id, record in negatives.items():
            with self.subTest(external_id=external_id):
                self.assertTrue(
                    record["negative_rationale"].startswith(
                        f"Missing outcome: {external_id} - external result '"
                    )
                )
                self.assertEqual(record["relationships"], [])

    def test_task3_positive_manifest_provenance_resolves_exactly(self) -> None:
        _, controls = reverse_profile_inputs()
        records = load_task3_records()
        self.assertEqual(
            sum(len(record["relationships"]) for record in records),
            len(TASK3_POSITIVE_TARGETS),
        )
        for record in records:
            for leg in record["relationships"]:
                with self.subTest(
                    external_id=record["external_provision_id"],
                    control_id=leg["esaf_control_id"],
                ):
                    control = controls[leg["esaf_control_id"]]
                    self.assertEqual(leg["esaf_control_version"], control["version"])
                    self.assertEqual(leg["esaf_control_path"], control["path"])
                    self.assertEqual(
                        leg["esaf_control_sha256"], control["record_sha256"]
                    )
                    self.assertEqual(
                        leg["esaf_requirement_locator"],
                        f"controls/{control['path']}#requirement",
                    )

    def test_task4_records_are_loaded_once_in_locked_oracle_order(self) -> None:
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        expected = [
            item["external_provision_id"]
            for item in oracle["provisions"]
            if item["group"] in TASK4_GROUP_COUNTS
        ]
        records = load_task4_records()
        self.assertEqual(len(records), sum(TASK4_GROUP_COUNTS.values()))
        self.assertEqual(
            [record["external_provision_id"] for record in records], expected
        )

    def test_task4_positives_have_exact_targets_and_bounded_evidence(self) -> None:
        records = load_task4_records()
        positives = {
            record["external_provision_id"]: record["relationships"]
            for record in records
            if record["disposition"] == "mapped"
        }
        self.assertEqual(set(positives), set(TASK4_POSITIVE_TARGETS))
        for external_id, relationships in positives.items():
            with self.subTest(external_id=external_id):
                self.assertEqual(len(relationships), 1)
                leg = relationships[0]
                self.assertEqual(
                    leg["esaf_control_id"], TASK4_POSITIVE_TARGETS[external_id]
                )
                self.assertEqual(leg["direction"], "external_to_esaf")
                parsed = [json.loads(item) for item in leg["conditions"]]
                self.assertEqual(
                    [item["condition"] for item in parsed], list(CONDITION_ORDER)
                )
                evidence = " ".join(leg["expected_evidence"]).lower()
                self.assertIn("dated", evidence)
                self.assertIn("population", evidence)
                self.assertIn("sample", evidence)
                self.assertRegex(evidence, r"\b(?:tool|method)\b")
                self.assertIn("provenance", evidence)
                self.assertRegex(
                    " ".join(leg["known_gaps"]).lower(),
                    r"\b(?:later|point-in-time)\b",
                )

    def test_task4_negatives_are_specific_and_recommendations_stay_negative(self) -> None:
        records = load_task4_records()
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        expected_ids = {
            item["external_provision_id"]
            for item in oracle["provisions"]
            if item["group"] in TASK4_GROUP_COUNTS
        }
        negatives = {
            record["external_provision_id"]: record
            for record in records
            if record["disposition"] == "no_direct_mapping"
        }
        self.assertEqual(
            set(negatives), expected_ids - set(TASK4_POSITIVE_TARGETS)
        )
        self.assertEqual(
            negatives["CEPTS3.2-T2-002"]["negative_rationale"],
            "Missing outcome: CEPTS3.2-T2-002 - external result 'Delivery "
            "Partner-approved vulnerability scanner' does not evidence ESAF "
            "outcome 'identified vulnerability affecting AI infrastructure and "
            "its risk-based disposition'.",
        )
        for external_id, record in negatives.items():
            with self.subTest(external_id=external_id):
                self.assertTrue(
                    record["negative_rationale"].startswith(
                        f"Missing outcome: {external_id} - external result '"
                    )
                )
                self.assertEqual(record["relationships"], [])
        recommendation_ids = {
            item["external_provision_id"]
            for item in oracle["provisions"]
            if item["group"] in TASK4_GROUP_COUNTS
            and item["kind"] == "recommendation"
        }
        self.assertTrue(recommendation_ids)
        self.assertTrue(recommendation_ids <= set(negatives))

    def test_task4_positive_manifest_provenance_resolves_exactly(self) -> None:
        _, controls = reverse_profile_inputs()
        records = load_task4_records()
        self.assertEqual(
            sum(len(record["relationships"]) for record in records),
            len(TASK4_POSITIVE_TARGETS),
        )
        for record in records:
            for leg in record["relationships"]:
                with self.subTest(
                    external_id=record["external_provision_id"],
                    control_id=leg["esaf_control_id"],
                ):
                    control = controls[leg["esaf_control_id"]]
                    self.assertEqual(leg["esaf_control_version"], control["version"])
                    self.assertEqual(leg["esaf_control_path"], control["path"])
                    self.assertEqual(
                        leg["esaf_control_sha256"], control["record_sha256"]
                    )
                    self.assertEqual(
                        leg["esaf_requirement_locator"],
                        f"controls/{control['path']}#requirement",
                    )

    def test_task5_records_are_loaded_once_in_locked_oracle_order(self) -> None:
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        expected = [
            item["external_provision_id"]
            for item in oracle["provisions"]
            if item["group"] in TASK5_GROUP_COUNTS
        ]
        records = load_task5_records()
        self.assertEqual(len(records), sum(TASK5_GROUP_COUNTS.values()))
        self.assertEqual(
            [record["external_provision_id"] for record in records], expected
        )

    def test_task5_independent_reassessment_has_one_exact_t5_006_leg(self) -> None:
        records = load_task5_records()
        positives = {
            record["external_provision_id"]: record["relationships"]
            for record in records
            if record["disposition"] == "mapped"
        }
        self.assertEqual(set(positives), set(TASK5_POSITIVE_TARGETS))
        relationships = positives["CEPTS3.2-T5-006"]
        self.assertEqual(len(relationships), 1)
        leg = relationships[0]
        self.assertEqual(leg["esaf_control_id"], "IAM-130")
        self.assertEqual(leg["direction"], "external_to_esaf")
        self.assertEqual(
            render_observation_claim("CEPTS3.2-T5-006", "IAM-130"),
            '{"assessment_date_boundary":"assessment_date_required","control_id":"IAM-130","evidence_date_boundary":"evidence_date_required","predicate":"restriction_and_separate_authentication_status","provision_id":"CEPTS3.2-T5-006","result_kind":"privileged_access_control","result_type":"recorded_status","subject":"administrative_process_access"}',
        )
        parsed = [json.loads(item) for item in leg["conditions"]]
        self.assertEqual(
            [item["condition"] for item in parsed], list(CONDITION_ORDER)
        )
        self.assertTrue(all(item["evidence_references"] for item in parsed))

    def test_t5_006_analysis_does_not_copy_feasibility_probe_text(self) -> None:
        record = next(
            record
            for record in load_task5_records()
            if record["external_provision_id"] == "CEPTS3.2-T5-006"
        )
        matrix = json.loads(
            (
                ROOT
                / "docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json"
            ).read_text(encoding="utf-8")
        )
        probe = next(
            item
            for item in matrix["probes"]
            if item["direction"] == "external_to_esaf"
            and item["provision_ids"] == ["CEPTS3.2-T5-006"]
        )
        authored = json.dumps(record, sort_keys=True)
        for field in (
            "rationale",
            "selection_basis",
            "semantic_fit_analysis",
        ):
            with self.subTest(field=field):
                self.assertNotIn(probe[field], authored)
        self.assertNotIn(probe["esaf_normative_bases"][0]["relevance_analysis"], authored)
        self.assertNotIn("two observed T5-006 facts materially support", authored)

    def test_task5_administrative_artifacts_and_decisions_stay_negative(self) -> None:
        records = {
            record["external_provision_id"]: record
            for record in load_task5_records()
        }
        categories = {
            "discretion": {
                "CEPTS3.2-C-003", "CEPTS3.2-C-008", "CEPTS3.2-C-010",
                "CEPTS3.2-C-011",
            },
            "aggregate decisions": {
                "CEPTS3.2-T5-007", "CEPTS3.2-C-005", "CEPTS3.2-C-008",
                "CEPTS3.2-C-012",
            },
            "scanner authorization": {"CEPTS3.2-A-001"},
            "file supply": {"CEPTS3.2-B-001", "CEPTS3.2-B-004", "CEPTS3.2-B-007"},
            "file retention": {"CEPTS3.2-B-003"},
        }
        for category, provision_ids in categories.items():
            for provision_id in provision_ids:
                with self.subTest(category=category, provision_id=provision_id):
                    record = records[provision_id]
                    self.assertEqual(record["disposition"], "no_direct_mapping")
                    self.assertEqual(record["relationships"], [])
                    self.assertTrue(
                        record["negative_rationale"].startswith(
                            f"Missing outcome: {provision_id} - external result '"
                        )
                    )
                    self.assertFalse(
                        any(pair[0] == provision_id for pair in OBSERVATION_PROFILES)
                    )

    def test_task5_c_a_and_b_records_are_all_specific_negatives(self) -> None:
        records = load_task5_records()
        for record in records:
            if record["external_metadata"]["group"] not in {"C", "A", "B"}:
                continue
            with self.subTest(external_id=record["external_provision_id"]):
                self.assertEqual(record["disposition"], "no_direct_mapping")
                self.assertEqual(record["relationships"], [])
                self.assertTrue(
                    record["negative_rationale"].startswith(
                        f"Missing outcome: {record['external_provision_id']} - external result '"
                    )
                )

    def test_task5_positive_manifest_provenance_resolves_exactly(self) -> None:
        _, controls = reverse_profile_inputs()
        relationships = [
            leg
            for record in load_task5_records()
            for leg in record["relationships"]
        ]
        self.assertEqual(len(relationships), 1)
        leg = relationships[0]
        control = controls["IAM-130"]
        self.assertEqual(leg["esaf_control_version"], control["version"])
        self.assertEqual(leg["esaf_control_path"], control["path"])
        self.assertEqual(leg["esaf_control_sha256"], control["record_sha256"])
        self.assertEqual(
            leg["esaf_requirement_locator"],
            f"controls/{control['path']}#requirement",
        )

    def test_reverse_contract_mutations_fail_closed(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        valid = valid_profile_record()
        self.assertEqual(
            crosswalk_validation.validate_reverse_evidence_record(
                valid, mapping_set, controls
            ),
            [],
        )

        def mutate(label: str) -> dict[str, object]:
            candidate = deepcopy(valid)
            leg = candidate["relationships"][0]
            if label == "wrong direction":
                leg["direction"] = "esaf_to_external"
            elif label == "missing condition":
                leg["conditions"] = leg["conditions"][:-1]
            elif label == "reordered condition":
                leg["conditions"] = list(reversed(leg["conditions"]))
            elif label == "empty evidence refs":
                leg["conditions"][0] = condition_entry("actor", evidence_references=[])
            elif label == "unresolved evidence ref":
                leg["conditions"][0] = condition_entry(
                    "actor", evidence_references=["record:not-a-field"]
                )
            elif label == "malformed condition":
                leg["conditions"][0] = "actor | SATISFIED | source"
            elif label == "noncanonical condition":
                leg["conditions"][0] = json.dumps(
                    json.loads(leg["conditions"][0]), indent=2
                )
            elif label == "unjustified NA":
                leg["conditions"][0] = condition_entry(
                    "actor",
                    "NOT_APPLICABLE",
                    ["record:source_locator", f"manifest:{VALID_CONTROL_ID}#requirement"],
                )
            elif label.startswith("wrong manifest "):
                field = {
                    "wrong manifest id": "esaf_control_id",
                    "wrong manifest version": "esaf_control_version",
                    "wrong manifest digest": "esaf_control_sha256",
                    "wrong manifest path": "esaf_control_path",
                    "wrong manifest locator": "esaf_requirement_locator",
                }[label]
                leg[field] = "0" * 64 if field == "esaf_control_sha256" else "wrong-nonempty"
            elif label == "duplicate leg":
                candidate["relationships"].append(deepcopy(leg))
            elif label == "condition-created outcomes":
                leg["rationale"] = "Conditions supply the missing observation and ESAF outcome."
            else:
                self.fail(f"unknown mutation: {label}")
            return candidate

        expected_errors = {
            "wrong direction": "must use direction external_to_esaf",
            "missing condition": "exact ordered checklist",
            "reordered condition": "exact ordered checklist",
            "empty evidence refs": "requires evidence references",
            "unresolved evidence ref": "unresolved evidence reference",
            "malformed condition": "canonical condition/status/evidence_references",
            "noncanonical condition": "canonical condition/status/evidence_references",
            "unjustified NA": "condition-specific known-gap justification",
            "wrong manifest id": "references unresolved manifest control",
            "wrong manifest version": "esaf_control_version must exactly match",
            "wrong manifest digest": "esaf_control_sha256 must exactly match",
            "wrong manifest path": "esaf_control_path must exactly match",
            "wrong manifest locator": "esaf_requirement_locator must exactly match",
            "duplicate leg": "duplicate reverse-evidence relationship leg",
            "condition-created outcomes": "must state an external observation",
        }
        for label, expected in expected_errors.items():
            with self.subTest(label=label):
                errors = crosswalk_validation.validate_reverse_evidence_record(
                    mutate(label), mapping_set, controls
                )
                self.assertIn(expected, "\n".join(errors))

        justified_na = deepcopy(valid)
        justified_leg = justified_na["relationships"][0]
        justified_leg["known_gaps"][0] = (
            "actor not applicable because the bounded result was produced automatically."
        )
        justified_leg["conditions"][0] = condition_entry(
            "actor",
            "NOT_APPLICABLE",
            ["relationship:known_gaps:0", "record:source_locator"],
        )
        self.assertEqual(
            crosswalk_validation.validate_reverse_evidence_record(
                justified_na, mapping_set, controls
            ),
            [],
        )

        duplicate_na_evidence = deepcopy(justified_na)
        duplicate_na_leg = duplicate_na_evidence["relationships"][0]
        duplicate_na_leg["conditions"][0] = condition_entry(
            "actor",
            "NOT_APPLICABLE",
            ["relationship:known_gaps:0", "relationship:known_gaps:0"],
        )
        self.assertIn(
            "distinct evidence references and a separate corroborating reference",
            "\n".join(
                crosswalk_validation.validate_reverse_evidence_record(
                    duplicate_na_evidence, mapping_set, controls
                )
            ),
        )

    def test_reverse_negative_rationale_is_provision_specific(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        valid = {
            "external_provision_id": "CEPTS3.2-M-001",
            "disposition": "no_direct_mapping",
            "relationships": [],
            "context": {
                "mode": "paraphrase",
                "summary": (
                    "The provision produces an administrative sampling plan for "
                    "the assessment."
                ),
            },
            "negative_rationale": (
                "Missing outcome: CEPTS3.2-M-001 - external result 'administrative "
                "sampling plan' does not evidence ESAF outcome 'separate "
                "authentication of privileged access'."
            ),
        }
        self.assertEqual(
            crosswalk_validation.validate_reverse_evidence_record(
                valid, mapping_set, controls
            ),
            [],
        )
        for rationale in (
            "Missing outcome: no direct mapping.",
            "Missing outcome: CEPTS3.2-M-001 - no direct mapping is available.",
            (
                "Missing outcome: CEPTS3.2-M-001 - external result 'generic external "
                "result' does not evidence ESAF outcome 'generic ESAF outcome'."
            ),
            "Missing outcome: a defined observation is absent.",
            "Anything may be used as a justification.",
        ):
            with self.subTest(rationale=rationale):
                candidate = deepcopy(valid)
                candidate["negative_rationale"] = rationale
                self.assertTrue(
                    crosswalk_validation.validate_reverse_evidence_record(
                        candidate, mapping_set, controls
                    )
                )

        with self.subTest(rationale="negative with relationship"):
            candidate = deepcopy(valid)
            candidate["relationships"] = valid_profile_record()["relationships"]
            self.assertIn(
                "negative reverse-evidence record must have no relationships",
                crosswalk_validation.validate_reverse_evidence_record(
                    candidate, mapping_set, controls
                ),
            )

    def test_reverse_negative_rejects_semantic_esaf_outcome_placeholders(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        record = {
            "external_provision_id": "CEPTS3.2-M-001",
            "disposition": "no_direct_mapping",
            "relationships": [],
            "context": {
                "mode": "paraphrase",
                "summary": (
                    "The provision produces an administrative sampling plan for "
                    "the assessment."
                ),
            },
        }
        placeholders = (
            "observed state of an exact normative AI safeguard",
            "verified condition of a specific ESAF control requirement",
            "evidence for a defined normative AI control outcome",
            "technical state of a named ESAF safeguard",
            "AUD-120 exact normative AI safeguard",
            "IAM 110 specific ESAF control requirement",
        )
        for placeholder in placeholders:
            with self.subTest(placeholder=placeholder):
                candidate = deepcopy(record)
                candidate["negative_rationale"] = (
                    "Missing outcome: CEPTS3.2-M-001 - external result "
                    "'administrative sampling plan' does not evidence ESAF outcome "
                    f"'{placeholder}'."
                )
                self.assertIn(
                    "specific ESAF outcome",
                    "\n".join(
                        crosswalk_validation.validate_reverse_evidence_record(
                            candidate, mapping_set, controls
                        )
                    ),
                )

    def test_reverse_positive_rejects_prohibited_assurance_claims(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        claims = (
            "This proves implementation.",
            "This proves effectiveness.",
            "This is sufficient evidence.",
            "This demonstrates compliance.",
            "This supports certification.",
            "This establishes equivalence.",
            "This provides continuous assurance.",
            "This proves population-wide coverage.",
            "This proves current-scheme coverage.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                candidate = valid_profile_record()
                candidate["relationships"][0]["rationale"] += f" {claim}"
                self.assertIn(
                    "rationale contains prohibited assurance claim",
                    "\n".join(
                        crosswalk_validation.validate_reverse_evidence_record(
                            candidate, mapping_set, controls
                        )
                    ),
                )

    def test_reverse_positive_requires_the_exact_canonical_rationale_template(
        self,
    ) -> None:
        mapping_set, controls = reverse_profile_inputs()
        canonical = valid_profile_record()["relationships"][0]["rationale"]
        mutations = {
            "supported outcome drift": canonical.replace(
                VALID_SUPPORTED_OUTCOME,
                "generally relates to privileged access.",
            ),
            "contradictory proof suffix": (
                f"{canonical} This proves the cited control is met."
            ),
            "contradictory guarantee suffix": (
                f"{canonical} This guarantees secure control operation."
            ),
            "contradictory conformity suffix": (
                f"{canonical} This assures conformity with the cited control."
            ),
        }
        for label, rationale in mutations.items():
            with self.subTest(label=label):
                candidate = valid_profile_record()
                candidate["relationships"][0]["rationale"] = rationale
                self.assertIn(
                    "rationale must equal the exact canonical reverse-evidence template",
                    "\n".join(
                        crosswalk_validation.validate_reverse_evidence_record(
                            candidate, mapping_set, controls
                        )
                    ),
                )

    def test_supported_outcome_registry_exactly_binds_all_persisted_rationales(
        self,
    ) -> None:
        supported_outcomes = getattr(
            crosswalk_validation,
            "_UK_CE_PLUS_V32_SUPPORTED_OUTCOME_TEXTS",
            {},
        )
        expected_pairs = {
            (record["external_provision_id"], leg["esaf_control_id"])
            for record in load_snapshot_records()
            if record.get("disposition") == "mapped"
            for leg in record["relationships"]
        }
        self.assertEqual(set(supported_outcomes), expected_pairs)
        self.assertEqual(len(supported_outcomes), 32)
        self.assertEqual(len(set(supported_outcomes.values())), 13)
        narrowing = (
            "Conditions only narrow this supported claim; "
            "they do not create either outcome."
        )
        for record in load_snapshot_records():
            if record.get("disposition") != "mapped":
                continue
            provision_id = record["external_provision_id"]
            for leg in record["relationships"]:
                control_id = leg["esaf_control_id"]
                observation = render_observation_claim(provision_id, control_id)
                expected = (
                    f"External observation: {observation}. Supported ESAF outcome: "
                    f"{control_id} {supported_outcomes[(provision_id, control_id)]} "
                    f"{narrowing}"
                )
                self.assertEqual(leg["rationale"], expected)

    def test_reverse_prohibitions_reject_positive_prefix_smuggling_in_each_entry(
        self,
    ) -> None:
        mapping_set, controls = reverse_profile_inputs()
        for index, category in enumerate(PROHIBITED_INFERENCE_KEYS):
            with self.subTest(category=category):
                candidate = valid_profile_record()
                entry = candidate["relationships"][0]["prohibited_inferences"][index]
                candidate["relationships"][0]["prohibited_inferences"][index] = (
                    entry.replace(
                        ": The observed result ",
                        ": The observation proves ESAF compliance and equivalence; "
                        "The observed result ",
                        1,
                    )
                )
                self.assertIn(
                    "must bind every prohibited inference to the observed result and "
                    "cited ESAF outcome",
                    "\n".join(
                        crosswalk_validation.validate_reverse_evidence_record(
                            candidate, mapping_set, controls
                        )
                    ),
                )

    def test_reverse_prohibitions_reject_suffix_and_synonym_smuggling(
        self,
    ) -> None:
        mapping_set, controls = reverse_profile_inputs()
        mutations = {
            "suffix": lambda entry: f"{entry} This assures conformity.",
            "synonym drift": lambda entry: entry.replace(
                "The observed result ", "The documented observation ", 1
            ),
        }
        for label, mutate in mutations.items():
            for index, category in enumerate(PROHIBITED_INFERENCE_KEYS):
                with self.subTest(label=label, category=category):
                    candidate = valid_profile_record()
                    entry = candidate["relationships"][0]["prohibited_inferences"][index]
                    candidate["relationships"][0]["prohibited_inferences"][index] = (
                        mutate(entry)
                    )
                    self.assertIn(
                        "must bind every prohibited inference to the observed result and "
                        "cited ESAF outcome",
                        "\n".join(
                            crosswalk_validation.validate_reverse_evidence_record(
                                candidate, mapping_set, controls
                            )
                        ),
                    )

    def test_reverse_prohibitions_require_control_binding_outside_observation_json(
        self,
    ) -> None:
        mapping_set, controls = reverse_profile_inputs()
        for index, category in enumerate(PROHIBITED_INFERENCE_KEYS):
            with self.subTest(category=category):
                candidate = valid_profile_record()
                entry = candidate["relationships"][0]["prohibited_inferences"][index]
                candidate["relationships"][0]["prohibited_inferences"][index] = (
                    entry.replace(
                        f" for the cited {VALID_CONTROL_ID} outcome.",
                        " for the cited control outcome.",
                    )
                )
                self.assertIn(
                    "must bind every prohibited inference to the observed result and "
                    "cited ESAF outcome",
                    "\n".join(
                        crosswalk_validation.validate_reverse_evidence_record(
                            candidate, mapping_set, controls
                        )
                    ),
                )

    def test_reverse_positive_requires_binding_prohibited_inferences(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        arbitrary_prohibition = required_prohibited_inferences(VALID_PROVISION_ID)
        arbitrary_prohibition[0] = (
            f"{VALID_PROVISION_ID} | prohibit implementation: This is not a meaningful "
            "binding prohibition for the authored record."
        )
        mutations = {
            "missing field": (
                None,
                "requires provision-specific prohibited_inferences",
            ),
            "missing category": (
                required_prohibited_inferences(VALID_PROVISION_ID)[:-1],
                "requires provision-specific prohibited_inferences",
            ),
            "wrong provision": (
                required_prohibited_inferences("CEPTS3.2-M-999"),
                "requires provision-specific prohibited_inferences",
            ),
            "generic entry": (
                ["Do not infer implementation, effectiveness, compliance, or assurance."],
                "requires provision-specific prohibited_inferences",
            ),
            "arbitrary prohibition": (
                arbitrary_prohibition,
                "must bind every prohibited inference to the observed result and "
                "cited ESAF outcome",
            ),
        }
        for label, (prohibited_inferences, expected_message) in mutations.items():
            with self.subTest(label=label):
                candidate = valid_profile_record()
                leg = candidate["relationships"][0]
                if prohibited_inferences is None:
                    leg.pop("prohibited_inferences")
                else:
                    leg["prohibited_inferences"] = prohibited_inferences
                self.assertIn(
                    expected_message,
                    "\n".join(
                        crosswalk_validation.validate_reverse_evidence_record(
                            candidate, mapping_set, controls
                        )
                    ),
                )

    def test_reverse_positive_rejects_generic_condition_boilerplate(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        candidate = valid_profile_record()
        leg = candidate["relationships"][0]
        leg["expected_evidence"] = [
            "A dated attributable workpaper identifies actor, scope, population, "
            "sample, dates, tool, provenance, exception, discretion, and status."
        ]
        leg["conditions"] = [
            condition_entry(
                condition,
                evidence_references=[
                    "relationship:expected_evidence",
                    "record:source_locator",
                ],
            )
            for condition in CONDITION_ORDER
        ]
        self.assertIn(
            "condition actor requires provision-specific evidence for actor",
            "\n".join(
                crosswalk_validation.validate_reverse_evidence_record(
                    candidate, mapping_set, controls
                )
            ),
        )

    def test_reverse_positive_rejects_mismatched_condition_evidence(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        mutations = {
            "exception evidence substituted": ["relationship:expected_evidence:8"],
            "unrelated generic reference added": [
                "relationship:expected_evidence:9",
                "record:source_locator",
            ],
        }
        for label, references in mutations.items():
            with self.subTest(label=label):
                candidate = valid_profile_record()
                leg = candidate["relationships"][0]
                leg["conditions"][9] = condition_entry(
                    "delivery_partner_discretion",
                    evidence_references=references,
                )
                self.assertIn(
                    "condition delivery_partner_discretion requires provision-specific "
                    "evidence for delivery_partner_discretion",
                    "\n".join(
                        crosswalk_validation.validate_reverse_evidence_record(
                            candidate, mapping_set, controls
                        )
                    ),
                )

    def test_reverse_positive_rejects_generic_prohibited_inference_wording(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        candidate = valid_profile_record()
        candidate["relationships"][0]["prohibited_inferences"] = [
            f"{candidate['external_provision_id']} | prohibit {key}: The observation "
            "does not establish the generic assurance category."
            for key in PROHIBITED_INFERENCE_KEYS
        ]
        self.assertIn(
            "must bind every prohibited inference to the observed result and cited "
            "ESAF outcome",
            "\n".join(
                crosswalk_validation.validate_reverse_evidence_record(
                    candidate, mapping_set, controls
                )
            ),
        )

    def test_reverse_positive_rejects_tool_activity_without_observed_result(
        self,
    ) -> None:
        mapping_set, controls = reverse_profile_inputs()
        for observation in (
            "Nmap.",
            "the Assessor ran Nmap.",
            "Nmap was used.",
            "the dated assessment result records that Nmap was used.",
            "the dated assessment result records that the Assessor ran Nmap.",
            "the dated assessment result records that the Assessor executed a "
            "generic vulnerability scanner.",
            "the dated assessment result records that a generic vulnerability "
            "scanner was executed by the Assessor.",
            "the dated assessment result records that an active scanning tool was "
            "used.",
            "the dated assessment result records that a passive scanning tool was "
            "used.",
            "the dated assessment result records that the Assessor authorized a "
            "scanning tool.",
            "the dated assessment result records that a scanning tool was authorized.",
            "the dated assessment result records that use of Nmap was authorized.",
            "the dated assessment result records that execution of a generic scanner "
            "was approved.",
            "scanner performed the scan",
            "Assessor employed a scanning tool",
            "utility completed execution",
            "permission to run Nmap granted",
            "Nmap authorized to run",
        ):
            with self.subTest(observation=observation):
                candidate = valid_profile_record()
                set_profile_observation(candidate, observation)
                errors = crosswalk_validation.validate_reverse_evidence_record(
                    candidate, mapping_set, controls
                )
                diagnostics = "\n".join(errors)
                self.assertIn("observation contract", diagnostics)
                self.assertNotIn("must bind every prohibited inference", diagnostics)

    def test_reverse_positive_accepts_tool_produced_concrete_state(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        candidate = valid_profile_record()
        leg = candidate["relationships"][0]
        leg["expected_evidence"][6] = (
            f"tool evidence: {VALID_PROVISION_ID} names Nmap version 7.94 and its approved "
            "authentication-test configuration."
        )
        self.assertNotIn("Nmap", leg["rationale"])
        self.assertIn("Nmap", leg["expected_evidence"][6])
        self.assertEqual(
            crosswalk_validation.validate_reverse_evidence_record(
                candidate, mapping_set, controls
            ),
            [],
        )

    def test_reverse_positive_rejects_sample_without_population_boundary(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        candidate = valid_profile_record()
        candidate["relationships"][0]["expected_evidence"] = [
            "A dated attributable assessment workpaper identifies the Assessor, AI "
            "service scope, selected devices, approved tool and method, result, "
            "provenance, and any exception."
        ]
        self.assertIn(
            "selection or sampling evidence requires an explicit population boundary",
            "\n".join(
                crosswalk_validation.validate_reverse_evidence_record(
                    candidate, mapping_set, controls
                )
            ),
        )

    def test_reverse_positive_requires_exact_json_isolation_and_one_terminal_period(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        mutations = {
            "missing terminal period": f"{VALID_OBSERVATION} ",
            "double terminal period": f"{VALID_OBSERVATION}.. ",
            "leading prose": f"claim {VALID_OBSERVATION}. ",
            "trailing prose": f"{VALID_OBSERVATION} extra. ",
        }
        for label, observation_segment in mutations.items():
            with self.subTest(label=label):
                candidate = valid_profile_record()
                leg = candidate["relationships"][0]
                leg["rationale"] = (
                    f"External observation: {observation_segment}Supported ESAF outcome: "
                    f"{VALID_CONTROL_ID} separately authenticates privileged access. "
                    "Conditions only narrow this supported claim; they do not create either outcome."
                )
                normalized = observation_segment.strip().rstrip(".")
                leg["prohibited_inferences"] = required_prohibited_inferences(
                    VALID_PROVISION_ID, normalized, VALID_CONTROL_ID
                )
                errors = crosswalk_validation.validate_reverse_evidence_record(
                    candidate, mapping_set, controls
                )
                diagnostics = "\n".join(errors)
                self.assertIn("observation contract", diagnostics)
                self.assertNotIn("must bind every prohibited inference", diagnostics)

    def test_reverse_positive_validates_each_pair_of_a_two_leg_record(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        provision_id = "CEPTS3.2-X-001"
        profiles = {
            (provision_id, "IAM-110"): {
                "result_kind": "authentication_requirement",
                "subject": "user_authentication",
                "predicate": "service_access_requirement_status",
                "result_type": "recorded_boolean",
            },
            (provision_id, "IAM-140"): {
                "result_kind": "credential_configuration",
                "subject": "default_password",
                "predicate": "password_change_status",
                "result_type": "recorded_boolean",
            },
        }
        supported_outcomes = {
            (provision_id, "IAM-110"): "states its independently supported outcome.",
            (provision_id, "IAM-140"): "states its independently supported outcome.",
        }
        candidate = valid_profile_record()
        candidate["external_provision_id"] = provision_id
        legs = []
        with patch.object(
            reverse_profile, "OBSERVATION_PROFILES", profiles
        ), patch.object(
            crosswalk_validation,
            "_UK_CE_PLUS_V32_SUPPORTED_OUTCOME_TEXTS",
            supported_outcomes,
            create=True,
        ):
            for control_id in ("IAM-110", "IAM-140"):
                leg = deepcopy(candidate["relationships"][0])
                control = controls[control_id]
                leg.update(
                    esaf_control_id=control_id,
                    esaf_control_version=control["version"],
                    esaf_control_path=control["path"],
                    esaf_control_sha256=control["record_sha256"],
                    esaf_requirement_locator=f"controls/{control['path']}#requirement",
                )
                observation = reverse_profile.render_observation_claim(
                    provision_id, control_id
                )
                leg["rationale"] = (
                    f"External observation: {observation}. Supported ESAF outcome: "
                    f"{control_id} states its independently supported outcome. "
                    "Conditions only narrow this supported claim; they do not create either outcome."
                )
                leg["conditions"] = [
                    condition_entry(
                        condition,
                        evidence_references=condition_references(control_id)[condition],
                    )
                    for condition in CONDITION_ORDER
                ]
                leg["expected_evidence"] = condition_evidence(provision_id)
                leg["prohibited_inferences"] = required_prohibited_inferences(
                    provision_id, observation, control_id
                )
                legs.append(leg)
            candidate["relationships"] = legs
            with patch.object(
                reverse_profile,
                "validate_observation_claim",
                wraps=reverse_profile.validate_observation_claim,
            ) as validator:
                self.assertEqual(
                    crosswalk_validation.validate_reverse_evidence_record(
                        candidate, mapping_set, controls
                    ),
                    [],
                )
                self.assertEqual(
                    [call.args[1:] for call in validator.call_args_list],
                    [(provision_id, "IAM-110"), (provision_id, "IAM-140")],
                )

            duplicate = deepcopy(candidate)
            duplicate["relationships"].append(deepcopy(legs[1]))
            self.assertIn(
                "duplicate reverse-evidence relationship leg for IAM-140",
                crosswalk_validation.validate_reverse_evidence_record(
                    duplicate, mapping_set, controls
                ),
            )

            incompatible = deepcopy(candidate)
            first_claim = reverse_profile.render_observation_claim(
                provision_id, "IAM-110"
            )
            incompatible_leg = incompatible["relationships"][1]
            incompatible_leg["rationale"] = (
                f"External observation: {first_claim}. Supported ESAF outcome: IAM-140 "
                "states its independently supported outcome. Conditions only narrow this "
                "supported claim; they do not create either outcome."
            )
            incompatible_leg["prohibited_inferences"] = (
                required_prohibited_inferences(provision_id, first_claim, "IAM-140")
            )
            self.assertIn(
                "relationship 2 observation contract: observation control_id must equal "
                "the relationship control ID",
                crosswalk_validation.validate_reverse_evidence_record(
                    incompatible, mapping_set, controls
                ),
            )

    def test_snapshot_validation_audits_authoritative_mapped_leg_pairs(self) -> None:
        expected_pairs = {
            (record["external_provision_id"], leg["esaf_control_id"])
            for record in load_snapshot_records()
            if record.get("disposition") == "mapped"
            for leg in record["relationships"]
        }
        with patch.object(
            reverse_profile,
            "validate_observation_registry",
            wraps=reverse_profile.validate_observation_registry,
        ) as validator:
            validate(ROOT)
        validator.assert_called_once()
        self.assertEqual(set(validator.call_args.args[0]), expected_pairs)
        self.assertIs(
            validator.call_args.args[1], reverse_profile.OBSERVATION_PROFILE_ENTRIES
        )

    def test_snapshot_validation_rejects_supported_outcome_registry_key_drift(
        self,
    ) -> None:
        supported_outcomes = {}
        narrowing = (
            " Conditions only narrow this supported claim; "
            "they do not create either outcome."
        )
        for record in load_snapshot_records():
            if record.get("disposition") != "mapped":
                continue
            provision_id = record["external_provision_id"]
            for leg in record["relationships"]:
                control_id = leg["esaf_control_id"]
                marker = f"Supported ESAF outcome: {control_id} "
                supported_outcomes[(provision_id, control_id)] = (
                    leg["rationale"].split(marker, 1)[1].removesuffix(narrowing)
                )
        missing_pair = ("CEPTS3.2-M-004", "AUD-120")
        cases = {
            "missing": (
                {
                    pair: text
                    for pair, text in supported_outcomes.items()
                    if pair != missing_pair
                },
                "missing supported-outcome text for observation profile pair: "
                "CEPTS3.2-M-004/AUD-120",
            ),
            "orphan": (
                supported_outcomes
                | {
                    ("CEPTS3.2-X-001", "IAM-110"): (
                        "states an unsupported outcome registry entry."
                    )
                },
                "orphan supported-outcome text pair: CEPTS3.2-X-001/IAM-110",
            ),
        }
        for label, (candidate, diagnostic) in cases.items():
            with self.subTest(label=label), patch.object(
                crosswalk_validation,
                "_UK_CE_PLUS_V32_SUPPORTED_OUTCOME_TEXTS",
                candidate,
                create=True,
            ):
                self.assertIn(diagnostic, "\n".join(validate(ROOT).errors))

    def test_reverse_mapped_record_requires_a_relationship(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        record = valid_profile_record()
        record["relationships"] = []
        self.assertIn(
            "mapped reverse-evidence record requires at least one relationship",
            crosswalk_validation.validate_reverse_evidence_record(
                record, mapping_set, controls
            ),
        )


class CyberEssentialsPlusStructuredObservationProfileTests(unittest.TestCase):
    provision_id = "CEPTS3.2-T1-011"
    control_id = "IAM-110"

    def valid_claim(self) -> str:
        return render_observation_claim(self.provision_id, self.control_id)

    def mutated_claim(self, **changes: object) -> str:
        claim = json.loads(self.valid_claim())
        claim.update(changes)
        return json.dumps(claim, separators=(",", ":"), sort_keys=True)

    def assert_rejected(
        self,
        claim: str,
        message: str = "",
        profiles: dict[tuple[str, str], dict[str, str]] | None = None,
    ) -> None:
        errors = validate_observation_claim(
            claim, self.provision_id, self.control_id, profiles
        )
        self.assertTrue(errors, message or claim)
        if message:
            self.assertIn(message, errors)

    def semantic_mutation(self, field: str, value: str) -> tuple[str, dict[tuple[str, str], dict[str, str]]]:
        profile = dict(OBSERVATION_PROFILES[(self.provision_id, self.control_id)])
        profile[field] = value
        return self.mutated_claim(**{field: value}), {
            (self.provision_id, self.control_id): profile
        }

    def test_registry_declares_the_exact_ordered_32_pair_profiles(self) -> None:
        self.assertEqual(OBSERVATION_PROFILE_ENTRIES, EXPECTED_OBSERVATION_PROFILE_ENTRIES)
        self.assertEqual(
            OBSERVATION_PROFILES,
            build_observation_profiles(EXPECTED_OBSERVATION_PROFILE_ENTRIES),
        )

    def test_renderer_produces_the_wished_for_canonical_claim(self) -> None:
        self.assertEqual(
            self.valid_claim(),
            '{"assessment_date_boundary":"assessment_date_required","control_id":"IAM-110","evidence_date_boundary":"evidence_date_required","predicate":"service_access_requirement_status","provision_id":"CEPTS3.2-T1-011","result_kind":"authentication_requirement","result_type":"recorded_boolean","subject":"user_authentication"}',
        )
        self.assertEqual(
            validate_observation_claim(
                self.valid_claim(), self.provision_id, self.control_id
            ),
            [],
        )

    def test_claim_requires_a_canonical_json_object_with_exact_string_fields(self) -> None:
        valid = self.valid_claim()
        duplicate = valid.replace(
            '"subject":"user_authentication"',
            '"subject":"user_authentication","subject":"another_subject"',
        )
        cases = {
            "malformed": "{not json}",
            "non-object": "[]",
            "duplicate key": duplicate,
            "extra field": self.mutated_claim(extra="field"),
            "missing field": self.mutated_claim(subject=None).replace(',"subject":null', ""),
            "non-string": self.mutated_claim(subject=7),
            "noncanonical": json.dumps(json.loads(valid), indent=2, sort_keys=True),
        }
        for label, claim in cases.items():
            with self.subTest(label=label):
                self.assert_rejected(claim)

    def test_claim_requires_exact_pair_and_date_boundaries(self) -> None:
        cases = {
            "wrong provision": self.mutated_claim(provision_id="CEPTS3.2-T1-012"),
            "wrong control": self.mutated_claim(control_id="IAM-140"),
            "assessment boundary": self.mutated_claim(assessment_date_boundary="optional"),
            "evidence boundary": self.mutated_claim(evidence_date_boundary="optional"),
        }
        for label, claim in cases.items():
            with self.subTest(label=label):
                self.assert_rejected(claim)

    def test_claim_rejects_tool_or_assessment_activity_in_every_semantic_field(self) -> None:
        for field in ("result_kind", "subject", "predicate", "result_type"):
            for activity in (
                "scanner_use",
                "tool_authorization",
                "assessor_procedure",
                "assessment_execution",
                "activity",
                "procedure",
                "execution",
            ):
                with self.subTest(field=field, activity=activity):
                    claim, profiles = self.semantic_mutation(field, activity)
                    self.assert_rejected(
                        claim,
                        f"{field} must not describe mere tool use or assessment procedure activity",
                        profiles,
                    )

    def test_claim_rejects_outcome_bearing_terms_in_every_semantic_field(self) -> None:
        values = (
            "pass", "fail", "true", "false", "compliance", "certification",
            "success", "failure", "equivalence", "non_compliant", "certified",
            "equivalent", "passed", "failing",
        )
        for field in ("result_kind", "subject", "predicate", "result_type"):
            for value in values:
                with self.subTest(field=field, value=value):
                    claim, profiles = self.semantic_mutation(field, value)
                    self.assert_rejected(
                        claim, f"{field} must be outcome-neutral", profiles
                    )

    def test_claim_rejects_matching_profiles_for_the_complete_review_bypass_list(
        self,
    ) -> None:
        for field in ("result_kind", "subject", "predicate", "result_type"):
            for value, diagnostic in REVIEW_SEMANTIC_BYPASSES.items():
                with self.subTest(field=field, value=value):
                    claim, profiles = self.semantic_mutation(field, value)
                    self.assert_rejected(
                        claim,
                        f"{field} {diagnostic}",
                        profiles,
                    )

    def test_claim_rejects_novel_neutral_values_even_when_the_profile_matches(
        self,
    ) -> None:
        for field in ("result_kind", "subject", "predicate", "result_type"):
            with self.subTest(field=field):
                value = f"novel_{field}_measurement"
                claim, profiles = self.semantic_mutation(field, value)
                self.assert_rejected(
                    claim,
                    f"{field} must use the closed source-versioned vocabulary",
                    profiles,
                )

    def test_claim_rejects_a_profile_value_borrowed_from_another_pair(self) -> None:
        self.assert_rejected(
            self.mutated_claim(predicate="factor_count"),
            "observation predicate must exactly match the registered pair profile",
        )

    def test_identifier_boundary_audit_keeps_password_valid(self) -> None:
        claim = render_observation_claim("CEPTS3.2-T1-013", "IAM-140")
        self.assertIn('"subject":"default_password"', claim)
        self.assertEqual(
            validate_observation_claim(claim, "CEPTS3.2-T1-013", "IAM-140"), []
        )

    def test_registry_audit_rejects_threshold_result_classifications_in_every_field(self) -> None:
        threshold = list(EXPECTED_OBSERVATION_PROFILE_ENTRIES[5])
        for position, field in enumerate(
            ("result_kind", "subject", "predicate", "result_type"), start=2
        ):
            for value in ("high_risk", "low_risk", "high-risk", "low-risk"):
                entries = list(EXPECTED_OBSERVATION_PROFILE_ENTRIES)
                candidate = threshold.copy()
                candidate[position] = value
                entries[5] = tuple(candidate)
                with self.subTest(field=field, value=value):
                    self.assertTrue(validate_observation_registry(
                        [(row[0], row[1]) for row in EXPECTED_OBSERVATION_PROFILE_ENTRIES],
                        entries,
                    ))

    def test_registry_builder_rejects_mere_tool_or_procedure_profiles(self) -> None:
        for position, field in enumerate(
            ("result_kind", "subject", "predicate", "result_type"), start=2
        ):
            for value in ("activity", "procedure", "execution"):
                entry = [
                    "CEPTS3.2-X-001", "IAM-110", "measurement_kind",
                    "configuration_subject", "measurement_predicate", "recorded_status",
                ]
                entry[position] = value
                with self.subTest(field=field, value=value):
                    with self.assertRaisesRegex(
                        ValueError,
                        f"{field} must not describe mere tool use or assessment procedure activity",
                    ):
                        build_observation_profiles([tuple(entry)])

    def test_registry_builder_rejects_the_complete_review_bypass_list(self) -> None:
        original = list(EXPECTED_OBSERVATION_PROFILE_ENTRIES[6])
        for position, field in enumerate(
            ("result_kind", "subject", "predicate", "result_type"), start=2
        ):
            for value, diagnostic in REVIEW_SEMANTIC_BYPASSES.items():
                with self.subTest(field=field, value=value):
                    entry = original.copy()
                    entry[position] = value
                    with self.assertRaisesRegex(
                        ValueError,
                        f"{field} {diagnostic}",
                    ):
                        build_observation_profiles([tuple(entry)])

    def test_registry_audit_rejects_the_complete_review_bypass_list(self) -> None:
        original = list(EXPECTED_OBSERVATION_PROFILE_ENTRIES[6])
        pair = (original[0], original[1])
        for position, field in enumerate(
            ("result_kind", "subject", "predicate", "result_type"), start=2
        ):
            for value, diagnostic in REVIEW_SEMANTIC_BYPASSES.items():
                with self.subTest(field=field, value=value):
                    entry = original.copy()
                    entry[position] = value
                    self.assertIn(
                        f"{field} {diagnostic}",
                        validate_observation_registry([pair], [tuple(entry)]),
                    )

    def test_registry_builder_and_audit_reject_novel_neutral_values(self) -> None:
        original = list(EXPECTED_OBSERVATION_PROFILE_ENTRIES[6])
        pair = (original[0], original[1])
        for position, field in enumerate(
            ("result_kind", "subject", "predicate", "result_type"), start=2
        ):
            with self.subTest(field=field):
                entry = original.copy()
                entry[position] = f"novel_{field}_measurement"
                with self.assertRaisesRegex(
                    ValueError,
                    f"{field} must use the closed source-versioned vocabulary",
                ):
                    build_observation_profiles([tuple(entry)])
                self.assertIn(
                    f"{field} must use the closed source-versioned vocabulary",
                    validate_observation_registry([pair], [tuple(entry)]),
                )

    def test_registry_accepts_configuration_change_approval_measurement(self) -> None:
        claim = render_observation_claim("CEPTS3.2-T3-032", "INF-130")
        self.assertEqual(
            validate_observation_claim(claim, "CEPTS3.2-T3-032", "INF-130"), []
        )

    def test_closed_vocabularies_preserve_approved_assessment_and_execution_terms(
        self,
    ) -> None:
        for provision_id, control_id in (
            ("CEPTS3.2-M-004", "AUD-120"),
            ("CEPTS3.2-T3-033", "INF-110"),
            ("CEPTS3.2-T3-034", "INF-110"),
        ):
            with self.subTest(provision_id=provision_id, control_id=control_id):
                claim = render_observation_claim(provision_id, control_id)
                self.assertEqual(
                    validate_observation_claim(claim, provision_id, control_id), []
                )

    def test_registry_integrity_rejects_duplicate_missing_orphan_and_negative_pairs(self) -> None:
        pairs = [(row[0], row[1]) for row in EXPECTED_OBSERVATION_PROFILE_ENTRIES]
        negative = ("CEPTS3.2-M-001", "IAM-110", "authentication_requirement", "user_authentication", "service_access_requirement_status", "recorded_boolean")
        task5_negative = ("CEPTS3.2-T5-001", "IAM-110", "authentication_requirement", "user_authentication", "service_access_requirement_status", "recorded_boolean")
        orphan = ("CEPTS3.2-X-001", "IAM-110", "authentication_requirement", "user_authentication", "service_access_requirement_status", "recorded_boolean")
        cases = {
            "duplicate declared pair": (
                pairs, list(EXPECTED_OBSERVATION_PROFILE_ENTRIES) + [EXPECTED_OBSERVATION_PROFILE_ENTRIES[0]],
                "duplicate observation profile pair: CEPTS3.2-M-004/AUD-120",
            ),
            "missing mapped pair": (
                pairs,
                list(EXPECTED_OBSERVATION_PROFILE_ENTRIES[1:]),
                "missing observation profile for mapped pair: CEPTS3.2-M-004/AUD-120",
            ),
            "orphan pair": (
                pairs,
                list(EXPECTED_OBSERVATION_PROFILE_ENTRIES) + [orphan],
                "orphan observation profile pair: CEPTS3.2-X-001/IAM-110",
            ),
            "known negative provision": (
                pairs + [(negative[0], negative[1])],
                list(EXPECTED_OBSERVATION_PROFILE_ENTRIES) + [negative],
                "observation profile must not target a known negative provision",
            ),
            "known negative task 5 provision": (
                pairs + [(task5_negative[0], task5_negative[1])],
                list(EXPECTED_OBSERVATION_PROFILE_ENTRIES) + [task5_negative],
                "observation profile must not target a known negative provision",
            ),
        }
        for label, (mapped_pairs, entries, diagnostic) in cases.items():
            with self.subTest(label=label):
                self.assertEqual(
                    validate_observation_registry(mapped_pairs, entries), [diagnostic]
                )
