from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.catalog import build_catalog
from tools.crosswalks.validation import validate


ROOT = Path(__file__).parents[1]
SOURCE_URL = "https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf"
SOURCE_SHA256 = "e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923"
BASELINE_SHA = "5de9ff356ddad1e193444cd7308eff16ed83e811"
MAPPING_SET_ID = "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0"
SNAPSHOT = ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0"
REGISTRY = ROOT / "crosswalks/registry" / f"{MAPPING_SET_ID}.md"
PROVISION_ORACLE = ROOT / "docs/superpowers/specs/2026-07-13-uk-cyber-essentials-v3.3-provision-oracle.json"
EXPECTED_GROUPS = {
    "d": 44,
    "e1": 12,
    "e2": 12,
    "e3": 7,
    "e4": 29,
    "e5": 12,
}


def expected_ids() -> list[str]:
    return [
        f"CE3.3-{group.upper()}-{number:03d}"
        for group, count in EXPECTED_GROUPS.items()
        for number in range(1, count + 1)
    ]


def record_paths(prefix: str) -> list[Path]:
    return sorted(SNAPSHOT.glob(f"{prefix}-*.md"))


class UkCyberEssentialsV33CrosswalkTests(unittest.TestCase):
    def load_record(self, record_id: str) -> dict[str, object]:
        return parse_front_matter(SNAPSHOT / f"{record_id}.md")[0]

    def assert_group(self, group: str, count: int) -> None:
        paths = record_paths(f"ce33-{group}")
        oracle = json.loads(PROVISION_ORACLE.read_text(encoding="utf-8"))
        oracle_by_id = {item["record_id"]: item for item in oracle["provisions"]}
        self.assertEqual(
            [path.stem for path in paths],
            [f"ce33-{group}-{number:03d}" for number in range(1, count + 1)],
        )
        for number, path in enumerate(paths, 1):
            metadata, _ = parse_front_matter(path)
            expected = oracle_by_id[path.stem]
            self.assertEqual(metadata["external_provision_id"], expected["external_provision_id"])
            self.assertEqual(metadata["status"], "draft")
            self.assertEqual(metadata["granularity"], "requirement")
            self.assertEqual(metadata["source_locator"]["official_url"], SOURCE_URL)
            self.assertEqual(metadata["source_locator"]["locator"], expected["locator"])
            self.assertEqual(metadata["mapper"]["id"], "esaf-crosswalk-editorial-team")
            self.assertEqual(metadata["mapping_set_id"], MAPPING_SET_ID)
            self.assertEqual(metadata["change_history"][-1]["version"], "0.1.0")
            self.assertEqual(metadata["context"]["summary"], expected["summary"])
            self.assertEqual(
                {leg["direction"] for leg in metadata["relationships"]},
                {"esaf_to_external"} if metadata["relationships"] else set(),
            )
            if metadata["relationships"]:
                self.assertNotEqual(metadata["disposition"], "no_direct_mapping")
            else:
                self.assertEqual(metadata["disposition"], "no_direct_mapping")
                self.assertTrue(metadata["negative_rationale"])

    def test_scope_records_are_complete_and_conservative(self) -> None:
        self.assert_group("d", 44)

    def test_scope_relationship_semantics_remain_conservative(self) -> None:
        for record_id in ("ce33-d-007", "ce33-d-008", "ce33-d-009"):
            metadata = self.load_record(record_id)
            self.assertEqual(metadata["disposition"], "no_direct_mapping")
            self.assertEqual(metadata["relationships"], [])
            rationale = metadata["negative_rationale"]
            self.assertIn("ARC-110 identifies", rationale)
            self.assertIn("AI", rationale)
            self.assertIn(
                "does not require Cyber Essentials controls to be applied",
                rationale,
            )

        managed_service = self.load_record("ce33-d-028")
        self.assertEqual(len(managed_service["relationships"]), 1)
        relationship = managed_service["relationships"][0]
        self.assertEqual(relationship["esaf_control_id"], "CMP-120")
        self.assertEqual(relationship["confidence"], "medium")
        gap = " ".join(relationship["known_gaps"])
        self.assertIn(
            "does not itself establish every Cyber Essentials technical control is implemented or effective",
            gap,
        )
        self.assertIn("including for in-scope AI services", gap)
        self.assertIn("Cyber Essentials-specific technical verification remains separate", gap)

    def test_firewall_records_are_complete_and_do_not_infer_firewall_presence(self) -> None:
        self.assert_group("e1", 12)

        for number in range(1, 13):
            metadata = self.load_record(f"ce33-e1-{number:03d}")
            self.assertTrue(metadata["source_locator"]["locator"].startswith("Section E.1"))
            for relationship in metadata["relationships"]:
                self.assertEqual(relationship["direction"], "esaf_to_external")
                self.assertTrue(relationship["rationale"])
                self.assertTrue(relationship["conditions"])
                self.assertTrue(relationship["expected_evidence"])
                self.assertTrue(relationship["known_gaps"])

        for record_id in (
            "ce33-e1-001",
            "ce33-e1-002",
            "ce33-e1-003",
            "ce33-e1-004",
            "ce33-e1-005",
            "ce33-e1-006",
            "ce33-e1-007",
            "ce33-e1-010",
            "ce33-e1-012",
        ):
            metadata = self.load_record(record_id)
            self.assertEqual(metadata["disposition"], "no_direct_mapping")
            self.assertEqual(metadata["relationships"], [])
            self.assertIn("firewall", metadata["negative_rationale"].lower())

        for record_id in ("ce33-e1-008", "ce33-e1-009", "ce33-e1-011"):
            metadata = self.load_record(record_id)
            self.assertEqual(
                {relationship["esaf_control_id"] for relationship in metadata["relationships"]},
                {"INF-130"},
            )
            gap = " ".join(metadata["relationships"][0]["known_gaps"]).lower()
            self.assertIn("firewall", gap)

    def test_firewall_rule_approval_mapping_preserves_authorised_person_gap(self) -> None:
        approval = self.load_record("ce33-e1-008")
        self.assertEqual(len(approval["relationships"]), 1)
        relationship = approval["relationships"][0]
        self.assertEqual(relationship["esaf_control_id"], "INF-130")
        self.assertEqual(relationship["confidence"], "medium")
        gap = " ".join(relationship["known_gaps"]).lower()
        self.assertIn("does not itself require approval by an authorised person", gap)

    def test_secure_configuration_records_are_complete_and_preserve_threshold_gaps(self) -> None:
        self.assert_group("e2", 12)

        for number in range(1, 13):
            metadata = self.load_record(f"ce33-e2-{number:03d}")
            self.assertTrue(metadata["source_locator"]["locator"].startswith("Section E.2"))
            for relationship in metadata["relationships"]:
                self.assertEqual(relationship["direction"], "esaf_to_external")
                self.assertTrue(relationship["rationale"])
                self.assertTrue(relationship["conditions"])
                self.assertTrue(relationship["expected_evidence"])
                self.assertTrue(relationship["known_gaps"])
                if relationship["esaf_control_id"].startswith("IAM-"):
                    conditions = " ".join(relationship["conditions"]).lower()
                    self.assertIn("in-scope ai asset", conditions)

        account_reduction = self.load_record("ce33-e2-001")
        self.assertEqual(
            {relationship["esaf_control_id"] for relationship in account_reduction["relationships"]},
            {"IAM-100"},
        )

        for record_id in (
            "ce33-e2-002",
            "ce33-e2-003",
            "ce33-e2-004",
            "ce33-e2-006",
            "ce33-e2-009",
            "ce33-e2-010",
            "ce33-e2-011",
        ):
            metadata = self.load_record(record_id)
            self.assertEqual(metadata["disposition"], "no_direct_mapping")
            self.assertEqual(metadata["relationships"], [])
            self.assertTrue(metadata["negative_rationale"])

        threshold = self.load_record("ce33-e2-009")["negative_rationale"].lower()
        self.assertIn("10", threshold)
        self.assertIn("five minutes", threshold)
        unlock_length = self.load_record("ce33-e2-011")["negative_rationale"].lower()
        self.assertIn("six-character", unlock_length)

    def test_update_records_are_complete_and_keep_three_fixed_deadline_triggers(self) -> None:
        self.assert_group("e3", 7)

        unsupported = self.load_record("ce33-e3-003")
        self.assertEqual(
            {leg["esaf_control_id"] for leg in unsupported["relationships"]},
            {"ARC-150"},
        )

        automatic = self.load_record("ce33-e3-004")
        self.assertEqual(automatic["disposition"], "no_direct_mapping")
        self.assertEqual(automatic["relationships"], [])
        automatic_rationale = automatic["negative_rationale"].lower()
        self.assertIn("automated changes", automatic_rationale)
        self.assertIn("configuration", automatic_rationale)
        self.assertIn("does not require automatic-update enablement", automatic_rationale)

        trigger_terms = {
            "ce33-e3-005": ("vendor", "critical", "high risk"),
            "ce33-e3-006": ("cvss v3", "7 or above"),
            "ce33-e3-007": ("vendor", "severity"),
        }
        for record_id, terms in trigger_terms.items():
            record = self.load_record(record_id)
            self.assertTrue(record["relationships"])
            self.assertEqual(
                {leg["esaf_control_id"] for leg in record["relationships"]},
                {"INF-120"},
            )
            self.assertIn("14 days", record["context"]["summary"])
            for leg in record["relationships"]:
                gaps = " ".join(leg["known_gaps"]).lower()
                self.assertRegex(gaps, r"14[- ]day")
                for term in terms:
                    self.assertIn(term, gaps)
                if record_id == "ce33-e3-007":
                    self.assertRegex(gaps, r"omission|omitted|no severity")

    def test_locked_provision_oracle_is_exact(self) -> None:
        oracle = json.loads(PROVISION_ORACLE.read_text(encoding="utf-8"))
        provisions = oracle["provisions"]
        expected_record_ids = [
            f"ce33-{group}-{number:03d}"
            for group, count in EXPECTED_GROUPS.items()
            for number in range(1, count + 1)
        ]
        self.assertEqual(oracle["source_version"], "3.3")
        self.assertEqual(oracle["source_url"], SOURCE_URL)
        self.assertEqual(oracle["source_sha256"], SOURCE_SHA256)
        self.assertEqual(oracle["count"], 116)
        self.assertEqual(oracle["groups"], {key.upper(): value for key, value in EXPECTED_GROUPS.items()})
        self.assertEqual([item["record_id"] for item in provisions], expected_record_ids)
        self.assertEqual([item["external_provision_id"] for item in provisions], expected_ids())
        self.assertEqual(len(set(expected_ids())), 116)
        for item in provisions:
            self.assertEqual(set(item), {"record_id", "external_provision_id", "summary", "locator"})
            self.assertTrue(item["summary"])
            self.assertTrue(item["locator"])

    def test_snapshot_inventory_and_lifecycle_are_exact(self) -> None:
        mapping, body = parse_front_matter(SNAPSHOT / "README.md")
        inventory, _ = parse_front_matter(SNAPSHOT / "PROVISION_INVENTORY.md")
        lifecycle, _ = parse_front_matter(REGISTRY)
        self.assertEqual(
            SNAPSHOT.relative_to(ROOT).as_posix(),
            "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0",
        )
        self.assertEqual(mapping["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(mapping["source_version"], {"id": "3.3", "label": "3.3"})
        self.assertEqual(mapping["mapping_set_version"], "0.1.0")
        self.assertEqual(mapping["status"], "draft")
        self.assertEqual(mapping["source"]["official_url"], SOURCE_URL)
        self.assertEqual(mapping["source"]["publication_date"], "2026-04-27")
        self.assertEqual(mapping["source"]["access_class"], "public")
        self.assertEqual(mapping["esaf_release"]["source_commit_sha"], BASELINE_SHA)
        self.assertEqual(mapping["scope"]["inventory_count"], 116)
        self.assertEqual(mapping["mapper"]["id"], "esaf-crosswalk-editorial-team")
        self.assertTrue(mapping["mapper"]["authorized_source_access"])
        rights = mapping["publication_rights"]
        self.assertEqual(
            set(rights["permitted_elements"]),
            {
                "identifiers",
                "titles",
                "structural_inventory",
                "paraphrases",
                "derivative_mapping_analysis",
                "official_links",
            },
        )
        self.assertEqual(rights["prohibited_elements"], [])
        self.assertEqual(rights["reviewer_id"], "esaf-project-owner")
        self.assertNotEqual(rights["reviewer_id"], mapping["mapper"]["id"])
        self.assertTrue(rights["reviewer_authorized_source_access"])
        self.assertTrue(rights["publication_basis_reviewed"])
        self.assertNotIn("reviewer", mapping)
        self.assertNotIn("approver", mapping)
        self.assertEqual(inventory["scope_type"], "complete_publication")
        self.assertEqual(inventory["expected_count"], 116)
        self.assertEqual(inventory["provision_ids"], expected_ids())
        self.assertEqual(lifecycle["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(lifecycle["events"], [])
        self.assertIn(SOURCE_SHA256, body)
        self.assertIn("2026-07-13", body)
        self.assertIn("UK National Cyber Security Centre", body)
        self.assertIn("Open Government Licence v3.0", body)

    def test_publication_qualified_snapshot_path_is_valid(self) -> None:
        result = validate(ROOT)
        path_errors = [
            error
            for error in result.errors
            if "unexpected mappings-tree entry" in error
            or "snapshot path disagrees with metadata" in error
        ]
        self.assertEqual(path_errors, [])
        self.assertEqual(build_catalog(result)["counts"]["mapping_sets"], 1)

    def test_landing_page_freezes_source_rights_and_draft_boundary(self) -> None:
        text = (ROOT / "crosswalks/uk-cyber-essentials.md").read_text(encoding="utf-8")
        for expected in (
            "**Status:** Draft mapping in development",
            "Requirements for IT Infrastructure v3.3",
            SOURCE_URL,
            SOURCE_SHA256,
            "Open Government Licence v3.0",
            "116",
            "Cyber Essentials Plus",
            "does not establish certification",
        ):
            self.assertIn(expected, text)
        self.assertNotRegex(text, r"(?im)^\*\*Status:\*\*\s*(?:Reviewed|Approved|Published)\s*$")

    def test_decisions_lock_core_plus_separation_and_draft_posture(self) -> None:
        text = (ROOT / "project/DECISION_LOG.md").read_text(encoding="utf-8")
        for decision in (
            "Cyber Essentials core and Cyber Essentials Plus use separate mapping sets.",
            "Cyber Essentials v3.3 uses 116 ESAF-assigned atomic provision locators.",
            "The initial Cyber Essentials v3.3 mapping remains draft pending qualified human review.",
        ):
            self.assertIn(decision, text)
