from __future__ import annotations

import re
import json
import unittest
from collections import Counter
from copy import deepcopy
from pathlib import Path

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


def assert_reverse_leg_contract(testcase: unittest.TestCase, leg: dict[str, object]) -> None:
    testcase.assertEqual(leg["direction"], "external_to_esaf")
    conditions = leg["conditions"]
    testcase.assertIsInstance(conditions, list)
    assert isinstance(conditions, list)
    testcase.assertEqual([item["condition"] for item in conditions], list(CONDITION_ORDER))
    for item in conditions:
        testcase.assertIn(item["status"], {"SATISFIED", "NOT_APPLICABLE"})
        testcase.assertTrue(item["evidence_references"])
        if item["status"] == "NOT_APPLICABLE":
            testcase.assertGreaterEqual(len(item["evidence_references"]), 2)
    for field in ("esaf_control_sha256", "esaf_control_path", "esaf_requirement_locator"):
        testcase.assertTrue(leg[field])
    testcase.assertNotRegex(str(leg["rationale"]), r"(?i)conditions?\s+(supply|create).*missing")


def assert_negative_contract(testcase: unittest.TestCase, record: dict[str, object]) -> None:
    testcase.assertEqual(record["relationships"], [])
    rationale = str(record["negative_rationale"]).lower()
    testcase.assertTrue(rationale.startswith("missing outcome:"))
    testcase.assertNotIn(rationale, {
        "missing outcome: no direct mapping.",
        "missing outcome: no direct esaf mapping.",
        "missing outcome: the esaf baseline does not directly map.",
    })


class CyberEssentialsPlusExternalToEsafMappingTests(unittest.TestCase):
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
        leg = {
            "direction": "external_to_esaf",
            "esaf_control_sha256": "a" * 64,
            "esaf_control_path": "controls/IAM/IAM-130.md",
            "esaf_requirement_locator": "controls/IAM/IAM-130.md#requirement",
            "rationale": "A defined observation materially supports evaluation of one bounded requirement.",
            "conditions": [
                {"condition": condition, "status": "SATISFIED", "evidence_references": ["oracle", "observation"]}
                for condition in CONDITION_ORDER
            ],
        }
        negative = {"relationships": [], "negative_rationale": "Missing outcome: a defined observation of the exact ESAF requirement."}

        def mutate_leg(label: str) -> dict[str, object]:
            candidate = deepcopy(leg)
            if label == "wrong direction":
                candidate["direction"] = "esaf_to_external"
            elif label == "missing condition":
                candidate["conditions"] = candidate["conditions"][:-1]
            elif label == "reordered condition":
                candidate["conditions"] = list(reversed(candidate["conditions"]))
            elif label == "empty evidence refs":
                candidate["conditions"][0]["evidence_references"] = []
            elif label == "unjustified NA":
                candidate["conditions"][0] = {"condition": "actor", "status": "NOT_APPLICABLE", "evidence_references": ["oracle"]}
            elif label.startswith("missing manifest "):
                field = {
                    "missing manifest digest": "esaf_control_sha256",
                    "missing manifest path": "esaf_control_path",
                    "missing manifest locator": "esaf_requirement_locator",
                }[label]
                candidate[field] = ""
            elif label == "condition-created outcomes":
                candidate["rationale"] = "Conditions supply the missing outcome."
            else:
                self.fail(f"unknown mutation: {label}")
            return candidate

        for label in ("wrong direction", "missing condition", "reordered condition", "empty evidence refs", "unjustified NA", "missing manifest digest", "missing manifest path", "missing manifest locator", "condition-created outcomes"):
            with self.subTest(label=label), self.assertRaises(AssertionError):
                assert_reverse_leg_contract(self, mutate_leg(label))

        for label, candidate in (
            ("duplicate leg", {"relationships": [leg, deepcopy(leg)], "negative_rationale": ""}),
            ("generic negative", {"relationships": [], "negative_rationale": "Missing outcome: no direct mapping."}),
        ):
            with self.subTest(label=label), self.assertRaises(AssertionError):
                if label == "duplicate leg":
                    self.assertEqual(len(candidate["relationships"]), len({item["esaf_requirement_locator"] for item in candidate["relationships"]}))
                else:
                    assert_negative_contract(self, candidate)
