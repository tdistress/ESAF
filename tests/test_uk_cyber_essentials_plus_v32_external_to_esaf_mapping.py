from __future__ import annotations

import re
import json
import unittest
from collections import Counter
from copy import deepcopy
from pathlib import Path

import tools.crosswalks.validation as crosswalk_validation
from tools.crosswalks.digests import snapshot_digest
from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.manifest import build_control_manifest, render_manifest
from tools.crosswalks.validation import validate

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


def load_snapshot_records() -> list[dict[str, object]]:
    return [
        parse_front_matter(path)[0]
        for path in sorted(SNAPSHOT.glob("*.md"))
        if path.name not in {"README.md", "PROVISION_INVENTORY.md"}
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


def required_prohibited_inferences(external_id: str) -> list[str]:
    explanations = {
        "implementation": "The observation does not establish control implementation.",
        "effectiveness": "The observation does not establish control effectiveness.",
        "sufficiency": "The observation is not sufficient evidence of the control outcome.",
        "compliance": "The observation does not establish ESAF compliance.",
        "certification": "The observation does not authorize or establish certification.",
        "equivalence": "The external provision is not equivalent to the ESAF control.",
        "continuous_assurance": "The point-in-time observation is not continuous assurance.",
        "population_wide_coverage": "The sampled observation is not population-wide coverage.",
        "current_scheme_coverage": "The public v3.2 evidence is not current-scheme coverage.",
    }
    return [
        f"{external_id} | prohibit {key}: {explanations[key]}"
        for key in PROHIBITED_INFERENCE_KEYS
    ]


def valid_profile_record() -> dict[str, object]:
    _, controls = reverse_profile_inputs()
    control = controls["IAM-130"]
    return {
        "external_provision_id": "CEPTS3.2-M-001",
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
                "esaf_control_id": "IAM-130",
                "esaf_control_version": control["version"],
                "esaf_control_path": control["path"],
                "esaf_control_sha256": control["record_sha256"],
                "esaf_requirement_locator": f"controls/{control['path']}#requirement",
                "direction": "external_to_esaf",
                "rationale": (
                    "External observation: the assessment produced a bounded authentication result. "
                    "Supported ESAF outcome: IAM-130 separately authenticates privileged access. "
                    "Conditions only narrow this supported claim; they do not create either outcome."
                ),
                "conditions": [condition_entry(condition) for condition in CONDITION_ORDER],
                "expected_evidence": ["Recorded authentication observation."],
                "known_gaps": ["Population-wide and continuous operation are not established."],
                "prohibited_inferences": required_prohibited_inferences(
                    "CEPTS3.2-M-001"
                ),
            }
        ],
    }


class CyberEssentialsPlusExternalToEsafMappingTests(unittest.TestCase):
    def test_production_validator_exposes_reverse_evidence_profile(self) -> None:
        self.assertTrue(
            hasattr(crosswalk_validation, "validate_reverse_evidence_record")
        )

    def test_authored_records_are_loaded_and_checked_by_production_profile(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        errors = [
            f"{record.get('external_provision_id')}: {message}"
            for record in load_snapshot_records()
            for message in crosswalk_validation.validate_reverse_evidence_record(
                record, mapping_set, controls
            )
        ]
        self.assertEqual(errors, [])

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

    def test_draft_scaffold_has_locked_empty_complete_publication_shape(self) -> None:
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
        records = [path for path in SNAPSHOT.glob("*.md") if path.name not in {"README.md", "PROVISION_INVENTORY.md"}]
        self.assertEqual(records, [])
        self.assertEqual(validate(ROOT).errors, [])

    def test_manifest_is_deterministic_at_pinned_esaf_commit(self) -> None:
        expected = build_control_manifest(ROOT, BASELINE_SHA, "0.4-alpha", None)
        self.assertEqual(len(expected["controls"]), 91)
        self.assertEqual(
            (SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").read_text(encoding="utf-8"),
            render_manifest(expected),
        )

    def test_draft_catalog_entry_is_generated_with_zero_records(self) -> None:
        catalog = json.loads((ROOT / "crosswalks/catalog.json").read_text(encoding="utf-8"))
        entry = next(item for item in catalog["mapping_sets"] if item["metadata"]["mapping_set_id"] == MAPPING_SET_ID)
        self.assertEqual(entry["metadata"]["status"], "draft")
        self.assertEqual(entry["inventory"]["expected_count"], 144)
        self.assertEqual(entry["provisions"], [])
        self.assertEqual(entry["lifecycle"]["events"], [])

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
                    ["record:source_locator", "manifest:IAM-130#requirement"],
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

    def test_reverse_positive_requires_binding_prohibited_inferences(self) -> None:
        mapping_set, controls = reverse_profile_inputs()
        arbitrary_prohibition = required_prohibited_inferences("CEPTS3.2-M-001")
        arbitrary_prohibition[0] = (
            "CEPTS3.2-M-001 | prohibit implementation: This is not a meaningful "
            "binding prohibition for the authored record."
        )
        mutations = {
            "missing field": None,
            "missing category": required_prohibited_inferences("CEPTS3.2-M-001")[:-1],
            "wrong provision": required_prohibited_inferences("CEPTS3.2-M-999"),
            "generic entry": [
                "Do not infer implementation, effectiveness, compliance, or assurance."
            ],
            "arbitrary prohibition": arbitrary_prohibition,
        }
        for label, prohibited_inferences in mutations.items():
            with self.subTest(label=label):
                candidate = valid_profile_record()
                leg = candidate["relationships"][0]
                if prohibited_inferences is None:
                    leg.pop("prohibited_inferences")
                else:
                    leg["prohibited_inferences"] = prohibited_inferences
                self.assertIn(
                    "requires provision-specific prohibited_inferences",
                    "\n".join(
                        crosswalk_validation.validate_reverse_evidence_record(
                            candidate, mapping_set, controls
                        )
                    ),
                )

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
