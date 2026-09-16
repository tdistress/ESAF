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
    / "2026-09-16-nist-sp-800-53-publication-rights-review.md"
)
SOURCE_ORACLE = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-16-nist-sp-800-53-source-readiness-oracle.json"
)
INVENTORY = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-16-nist-sp-800-53-rev5-control-inventory.json"
)
MATRIX = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-16-nist-sp-800-53-mapping-readiness-matrix.json"
)
TRACEABILITY = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-09-16-nist-sp-800-53-rev5-mapping-go-no-go-traceability.md"
)
LANDING = ROOT / "crosswalks" / "nist-sp-800-53.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "catalog-validation.yml"
CROSSWALK_CATALOG = ROOT / "crosswalks" / "catalog.json"

EXPECTED_PDF_SHA256 = (
    "fc63bcd61715d0181dd8e85998b1e6201ae3515fc6626102101cab1841e11ec6"
)
EXPECTED_INVENTORY_DIGEST = (
    "bba55bf6a5a3390f349237c1eabf0a851bfc7e7a9914be1ba1eded19aa36067b"
)
EXPECTED_TRACEABILITY_IDS = {
    "I194-D1",
    "I194-D2",
    "I194-D3",
    "I194-D4",
    "I194-D5",
    "I194-A1",
    "I194-A2",
    "I194-A3",
    "I194-A4",
    "I194-A5",
    "I194-A6",
    "I194-B1",
    "I194-B2",
    "I194-B3",
}


class NistSp80053SourceReadinessTests(unittest.TestCase):
    def test_rights_review_is_pass(self) -> None:
        text = RIGHTS_REVIEW.read_text(encoding="utf-8")
        self.assertIn("**Disposition:** `PASS`", text)
        self.assertIn("## Final decision", text)
        self.assertIn("`PASS`", text)
        self.assertIn("permitted_mapping_field_classes", text)

    def test_oracle_pins_public_pdf_identity(self) -> None:
        oracle = json.loads(SOURCE_ORACLE.read_text(encoding="utf-8"))
        artifact = oracle["source_artifact"]
        self.assertEqual(artifact["state"], "available")
        self.assertEqual(artifact["sha256"], EXPECTED_PDF_SHA256)
        self.assertEqual(artifact["byte_length"], 6073678)
        self.assertEqual(artifact["page_count"], 492)
        self.assertEqual(artifact["provision_count"], 1196)
        self.assertEqual(artifact["inventory_digest"], EXPECTED_INVENTORY_DIGEST)
        self.assertFalse(oracle["access"]["protected"])
        self.assertEqual(oracle["publication"]["document_reference"], "NIST.SP.800-53r5")
        self.assertIn("Rev. 5", oracle["publication"]["version"])
        retrieved = oracle["discovery"]["retrieved_at_utc"]
        self.assertRegex(retrieved, r"^2026-09-16T\d{2}:\d{2}:\d{2}Z$")

    def test_inventory_matches_oracle_digest_and_count(self) -> None:
        inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual(inventory["count"], 1196)
        self.assertEqual(len(inventory["identifiers"]), 1196)
        self.assertEqual(inventory["digest_sha256"], EXPECTED_INVENTORY_DIGEST)
        body = "\n".join(inventory["identifiers"]) + "\n"
        self.assertEqual(
            hashlib.sha256(body.encode("utf-8")).hexdigest(),
            EXPECTED_INVENTORY_DIGEST,
        )
        self.assertIn("AC-2", inventory["identifiers"])
        self.assertIn("AC-2(1)", inventory["identifiers"])
        self.assertIn("SI-7(15)", inventory["identifiers"])

    def test_matrix_derives_hold_with_only_mapper_blocker(self) -> None:
        matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        self.assertEqual(matrix["recorded_decision"], "HOLD")
        statuses = {gate["gate"]: gate["status"] for gate in matrix["gates"]}
        self.assertEqual(statuses["mapper_and_reviewer_readiness"], "BLOCKED")
        for gate, status in statuses.items():
            if gate != "mapper_and_reviewer_readiness":
                self.assertEqual(status, "PASS", gate)
        self.assertEqual(
            [blocker["blocker_id"] for blocker in matrix["blockers"]],
            ["NIST-SP-800-53-READINESS-B001"],
        )

    def test_landing_and_traceability_preserve_hold_and_catalog(self) -> None:
        landing = LANDING.read_text(encoding="utf-8")
        trace = TRACEABILITY.read_text(encoding="utf-8")
        self.assertIn("**Status:** Readiness HOLD", landing)
        self.assertIn("NIST SP 800-53 mapping artifacts: `0`", landing)
        self.assertIn("3 mapping sets, 404", landing)
        catalog = json.loads(CROSSWALK_CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(catalog["counts"]["mapping_sets"], 3)
        self.assertEqual(catalog["counts"]["provisions"], 404)
        found = set(re.findall(r"`(I194-[A-Z0-9]+)`", trace))
        self.assertTrue(EXPECTED_TRACEABILITY_IDS.issubset(found))
        self.assertIn("Do not close Issue #55", trace)

    def test_ci_and_tools_wire_renderer_check(self) -> None:
        workflow = CI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("tools/render_nist_sp_800_53_mapping_go_no_go.py", workflow)
        self.assertIn(
            "python tools/render_nist_sp_800_53_mapping_go_no_go.py --check",
            workflow,
        )
        tools_readme = (ROOT / "tools" / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "render_nist_sp_800_53_mapping_go_no_go.py --check",
            tools_readme,
        )

    def test_no_nist_sp_800_53_mapping_artifacts_under_mappings(self) -> None:
        mappings = ROOT / "crosswalks" / "mappings"
        if mappings.is_dir():
            offenders = [
                path
                for path in mappings.rglob("*")
                if path.is_file()
                and (
                    "sp-800-53" in str(path).lower()
                    or "sp_800_53" in str(path).lower()
                    or "800-53" in path.name.lower()
                )
            ]
            self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
