import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RIGHTS_REVIEW = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-08-29-nist-ai-rmf-publication-rights-review.md"
)
SOURCE_ORACLE = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-08-29-nist-ai-rmf-source-readiness-oracle.json"
)
INVENTORY = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-08-29-nist-ai-rmf-1.0-subcategory-inventory.json"
)
MATRIX = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-08-29-nist-ai-rmf-mapping-readiness-matrix.json"
)
TRACEABILITY = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-08-29-nist-ai-rmf-1.0-mapping-go-no-go-traceability.md"
)
LANDING = ROOT / "crosswalks" / "nist-ai-rmf.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "catalog-validation.yml"
CROSSWALK_CATALOG = ROOT / "crosswalks" / "catalog.json"

EXPECTED_PDF_SHA256 = (
    "7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1"
)
EXPECTED_INVENTORY_DIGEST = (
    "4bc3922a9a6ff5ea6c6cd714559ed480b396ee847af854bfe3e8068d693043b2"
)
EXPECTED_TRACEABILITY_IDS = {
    "I94-D1",
    "I94-D2",
    "I94-D3",
    "I94-D4",
    "I94-D5",
    "I94-A1",
    "I94-A2",
    "I94-A3",
    "I94-A4",
    "I94-B1",
    "I94-B2",
    "I94-B3",
}


class NistAiRmfSourceReadinessTests(unittest.TestCase):
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
        self.assertEqual(artifact["byte_length"], 1946127)
        self.assertEqual(artifact["page_count"], 48)
        self.assertEqual(artifact["provision_count"], 72)
        self.assertEqual(artifact["inventory_digest"], EXPECTED_INVENTORY_DIGEST)
        self.assertFalse(oracle["access"]["protected"])
        self.assertEqual(oracle["publication"]["document_reference"], "NIST.AI.100-1")
        self.assertEqual(oracle["publication"]["version"], "1.0")

    def test_inventory_matches_oracle_digest_and_count(self) -> None:
        inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual(inventory["count"], 72)
        self.assertEqual(len(inventory["identifiers"]), 72)
        self.assertEqual(inventory["digest_sha256"], EXPECTED_INVENTORY_DIGEST)
        body = "\n".join(inventory["identifiers"]) + "\n"
        self.assertEqual(
            hashlib.sha256(body.encode("utf-8")).hexdigest(),
            EXPECTED_INVENTORY_DIGEST,
        )
        self.assertIn("GOVERN-1.1", inventory["identifiers"])
        self.assertIn("MEASURE-2.13", inventory["identifiers"])

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
            ["NIST-AI-RMF-READINESS-B001"],
        )

    def test_landing_and_traceability_preserve_hold_and_catalog(self) -> None:
        landing = LANDING.read_text(encoding="utf-8")
        trace = TRACEABILITY.read_text(encoding="utf-8")
        self.assertIn("**Status:** Readiness HOLD", landing)
        self.assertIn("NIST AI RMF mapping artifacts: `0`", landing)
        self.assertIn("3 mapping sets, 404", landing)
        catalog = json.loads(CROSSWALK_CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(catalog["counts"]["mapping_sets"], 3)
        self.assertEqual(catalog["counts"]["provisions"], 404)
        found = set(re.findall(r"`(I94-[A-Z0-9]+)`", trace))
        self.assertTrue(EXPECTED_TRACEABILITY_IDS.issubset(found))
        self.assertIn("Do not close Issue #55", trace)

    def test_ci_and_tools_wire_renderer_check(self) -> None:
        workflow = CI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("tools/render_nist_ai_rmf_mapping_go_no_go.py", workflow)
        self.assertIn(
            "python tools/render_nist_ai_rmf_mapping_go_no_go.py --check",
            workflow,
        )
        tools_readme = (ROOT / "tools" / "README.md").read_text(encoding="utf-8")
        self.assertIn("render_nist_ai_rmf_mapping_go_no_go.py --check", tools_readme)

    def test_no_nist_mapping_artifacts_under_mappings(self) -> None:
        mappings = ROOT / "crosswalks" / "mappings"
        if mappings.is_dir():
            offenders = [
                path
                for path in mappings.rglob("*")
                if path.is_file() and "nist" in path.name.lower()
            ]
            self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
