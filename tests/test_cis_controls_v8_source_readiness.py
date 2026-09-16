import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RIGHTS_REVIEW = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-09-16-cis-controls-v8-publication-rights-review.md"
)
SOURCE_ORACLE = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-16-cis-controls-v8-source-readiness-oracle.json"
)
INVENTORY = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-16-cis-controls-v8-safeguard-inventory.json"
)
MATRIX = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-16-cis-controls-v8-mapping-readiness-matrix.json"
)
TRACEABILITY = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-09-16-cis-controls-v8-mapping-go-no-go-traceability.md"
)
LANDING = ROOT / "crosswalks" / "cis-controls.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "catalog-validation.yml"
CROSSWALK_CATALOG = ROOT / "crosswalks" / "catalog.json"

EXPECTED_INVENTORY_DIGEST = (
    "1a48eb400f3276e4cc6438cf832bf2bdea112512ac8d3c98eea7353df228aad1"
)
EXPECTED_TRACEABILITY_IDS = {
    "I206-D1",
    "I206-D2",
    "I206-D3",
    "I206-D4",
    "I206-D5",
    "I206-A1",
    "I206-A2",
    "I206-A3",
    "I206-A4",
    "I206-A5",
    "I206-A6",
    "I206-B1",
    "I206-B2",
    "I206-B3",
}


class CisControlsV8SourceReadinessTests(unittest.TestCase):
    def test_rights_review_is_hold_with_partition(self) -> None:
        text = RIGHTS_REVIEW.read_text(encoding="utf-8")
        self.assertIn("**Disposition:** `HOLD`", text)
        self.assertIn("## Final decision", text)
        self.assertIn("`HOLD`", text)
        self.assertIn("permitted_mapping_field_classes", text)
        self.assertIn("prohibited_mapping_field_classes", text)
        self.assertIn("derivative_mapping_analysis", text)
        self.assertIn("CC BY-NC-ND", text)

    def test_oracle_pins_v8_identity_without_pdf_bytes(self) -> None:
        oracle = json.loads(SOURCE_ORACLE.read_text(encoding="utf-8"))
        artifact = oracle["source_artifact"]
        self.assertEqual(
            artifact["state"],
            "package_available_via_registration_pdf_bytes_not_retrieved",
        )
        self.assertIsNone(artifact["sha256"])
        self.assertIsNone(artifact["byte_length"])
        self.assertIsNone(artifact["page_count"])
        self.assertEqual(artifact["provision_count"], 153)
        self.assertEqual(artifact["inventory_digest"], EXPECTED_INVENTORY_DIGEST)
        self.assertFalse(oracle["access"]["protected"])
        self.assertEqual(
            oracle["access"]["browser_behavior"],
            "registration_form_before_pdf_package_download",
        )
        self.assertEqual(oracle["publication"]["document_reference"], "CIS Controls Version 8")
        self.assertIn("8", oracle["publication"]["version"])
        self.assertNotIn("8.1", oracle["publication"]["version"])
        retrieved = oracle["discovery"]["retrieved_at_utc"]
        self.assertRegex(retrieved, r"^2026-09-16T\d{2}:\d{2}:\d{2}Z$")

    def test_inventory_matches_oracle_digest_and_count(self) -> None:
        inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual(inventory["count"], 153)
        self.assertEqual(len(inventory["identifiers"]), 153)
        self.assertEqual(inventory["digest_sha256"], EXPECTED_INVENTORY_DIGEST)
        body = "\n".join(inventory["identifiers"]) + "\n"
        self.assertEqual(
            hashlib.sha256(body.encode("utf-8")).hexdigest(),
            EXPECTED_INVENTORY_DIGEST,
        )
        self.assertIn("1.1", inventory["identifiers"])
        self.assertIn("18.5", inventory["identifiers"])
        self.assertEqual(inventory["identifiers"][0], "1.1")

    def test_matrix_derives_hold_with_rights_and_people_blockers(self) -> None:
        matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        self.assertEqual(matrix["recorded_decision"], "HOLD")
        statuses = {gate["gate"]: gate["status"] for gate in matrix["gates"]}
        self.assertEqual(statuses["publication_rights"], "BLOCKED")
        self.assertEqual(statuses["mapper_and_reviewer_readiness"], "BLOCKED")
        for gate, status in statuses.items():
            if gate not in {
                "publication_rights",
                "mapper_and_reviewer_readiness",
            }:
                self.assertEqual(status, "PASS", gate)
        self.assertEqual(
            [blocker["blocker_id"] for blocker in matrix["blockers"]],
            [
                "CIS-CONTROLS-V8-READINESS-B001",
                "CIS-CONTROLS-V8-READINESS-B002",
            ],
        )

    def test_landing_and_traceability_preserve_hold_and_catalog(self) -> None:
        landing = LANDING.read_text(encoding="utf-8")
        trace = TRACEABILITY.read_text(encoding="utf-8")
        self.assertIn("**Status:** Readiness HOLD", landing)
        self.assertIn("CIS Controls mapping artifacts: `0`", landing)
        self.assertIn("3 mapping sets, 404", landing)
        catalog = json.loads(CROSSWALK_CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(catalog["counts"]["mapping_sets"], 3)
        self.assertEqual(catalog["counts"]["provisions"], 404)
        found = set(re.findall(r"`(I206-[A-Z0-9]+)`", trace))
        self.assertTrue(EXPECTED_TRACEABILITY_IDS.issubset(found))
        self.assertIn("Do not close Issue #55", trace)

    def test_ci_and_tools_wire_renderer_check(self) -> None:
        workflow = CI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("tools/render_cis_controls_v8_mapping_go_no_go.py", workflow)
        self.assertIn(
            "python tools/render_cis_controls_v8_mapping_go_no_go.py --check",
            workflow,
        )
        tools_readme = (ROOT / "tools" / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "render_cis_controls_v8_mapping_go_no_go.py --check",
            tools_readme,
        )

    def test_no_cis_controls_mapping_artifacts_under_mappings(self) -> None:
        mappings = ROOT / "crosswalks" / "mappings"
        if mappings.is_dir():
            offenders = [
                path
                for path in mappings.rglob("*")
                if path.is_file()
                and (
                    "cis-controls" in str(path).lower()
                    or "cis_controls" in str(path).lower()
                )
            ]
            self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
