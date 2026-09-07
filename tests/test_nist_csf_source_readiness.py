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
    / "2026-09-07-nist-csf-publication-rights-review.md"
)
SOURCE_ORACLE = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-07-nist-csf-source-readiness-oracle.json"
)
INVENTORY = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-07-nist-csf-2.0-subcategory-inventory.json"
)
MATRIX = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-07-nist-csf-mapping-readiness-matrix.json"
)
TRACEABILITY = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-09-07-nist-csf-2.0-mapping-go-no-go-traceability.md"
)
LANDING = ROOT / "crosswalks" / "nist-csf.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "catalog-validation.yml"
CROSSWALK_CATALOG = ROOT / "crosswalks" / "catalog.json"

EXPECTED_PDF_SHA256 = (
    "3c31f46fee98cac0c4323453e5109291a213b4de7fef8c058af9bf67f717433c"
)
EXPECTED_INVENTORY_DIGEST = (
    "d66bb9694200fb177f0dc89cebf9f6344e48a9c982607320a56af0504e45ff1f"
)
EXPECTED_TRACEABILITY_IDS = {
    "I159-D1",
    "I159-D2",
    "I159-D3",
    "I159-D4",
    "I159-D5",
    "I159-A1",
    "I159-A2",
    "I159-A3",
    "I159-A4",
    "I159-A5",
    "I159-A6",
    "I159-B1",
    "I159-B2",
    "I159-B3",
}


class NistCsfSourceReadinessTests(unittest.TestCase):
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
        self.assertEqual(artifact["byte_length"], 1518858)
        self.assertEqual(artifact["page_count"], 32)
        self.assertEqual(artifact["provision_count"], 106)
        self.assertEqual(artifact["inventory_digest"], EXPECTED_INVENTORY_DIGEST)
        self.assertFalse(oracle["access"]["protected"])
        self.assertEqual(oracle["publication"]["document_reference"], "NIST.CSWP.29")
        self.assertEqual(oracle["publication"]["version"], "2.0")
        retrieved = oracle["discovery"]["retrieved_at_utc"]
        self.assertRegex(retrieved, r"^2026-09-07T\d{2}:\d{2}:\d{2}Z$")

    def test_inventory_matches_oracle_digest_and_count(self) -> None:
        inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual(inventory["count"], 106)
        self.assertEqual(len(inventory["identifiers"]), 106)
        self.assertEqual(inventory["digest_sha256"], EXPECTED_INVENTORY_DIGEST)
        body = "\n".join(inventory["identifiers"]) + "\n"
        self.assertEqual(
            hashlib.sha256(body.encode("utf-8")).hexdigest(),
            EXPECTED_INVENTORY_DIGEST,
        )
        self.assertIn("GV.OC-01", inventory["identifiers"])
        self.assertIn("RC.RP-01", inventory["identifiers"])

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
            ["NIST-CSF-READINESS-B001"],
        )

    def test_landing_and_traceability_preserve_hold_and_catalog(self) -> None:
        landing = LANDING.read_text(encoding="utf-8")
        trace = TRACEABILITY.read_text(encoding="utf-8")
        self.assertIn("**Status:** Readiness HOLD", landing)
        self.assertIn("NIST CSF mapping artifacts: `0`", landing)
        self.assertIn("3 mapping sets, 404", landing)
        catalog = json.loads(CROSSWALK_CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(catalog["counts"]["mapping_sets"], 3)
        self.assertEqual(catalog["counts"]["provisions"], 404)
        found = set(re.findall(r"`(I159-[A-Z0-9]+)`", trace))
        self.assertTrue(EXPECTED_TRACEABILITY_IDS.issubset(found))
        self.assertIn("Do not close Issue #55", trace)

    def test_ci_and_tools_wire_renderer_check(self) -> None:
        workflow = CI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("tools/render_nist_csf_mapping_go_no_go.py", workflow)
        self.assertIn(
            "python tools/render_nist_csf_mapping_go_no_go.py --check",
            workflow,
        )
        tools_readme = (ROOT / "tools" / "README.md").read_text(encoding="utf-8")
        self.assertIn("render_nist_csf_mapping_go_no_go.py --check", tools_readme)

    def test_no_nist_csf_mapping_artifacts_under_mappings(self) -> None:
        mappings = ROOT / "crosswalks" / "mappings"
        if mappings.is_dir():
            offenders = [
                path
                for path in mappings.rglob("*")
                if path.is_file() and "csf" in path.name.lower() and "hitrust" not in str(path).lower()
            ]
            # also catch nist-csf path segments
            offenders += [
                path
                for path in mappings.rglob("*")
                if path.is_file() and "nist-csf" in str(path).lower()
            ]
            self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
