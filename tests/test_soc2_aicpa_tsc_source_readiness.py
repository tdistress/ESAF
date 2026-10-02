from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-oracle.json"
MATRIX = ROOT / "docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-mapping-readiness-matrix.json"
RIGHTS_REVIEW = ROOT / "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md"
DECISION_REVIEW = ROOT / "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-mapping-go-no-go-review.md"
TRACEABILITY = ROOT / "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-mapping-go-no-go-traceability.md"
LANDING = ROOT / "crosswalks/soc-2.md"


class Soc2AicpaTscSourceReadinessTests(unittest.TestCase):
    def test_source_oracle_pins_candidate_edition_without_claiming_currentness(self):
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))

        self.assertEqual(
            oracle["publication"]["document_title"],
            "2017 Trust Services Criteria (With Revised Points of Focus – 2022)",
        )
        self.assertEqual(oracle["publication"]["edition"], "2017")
        self.assertEqual(oracle["publication"]["revised_points_of_focus"], "2022")
        self.assertEqual(oracle["publication"]["currentness"], "not_asserted")
        self.assertEqual(
            oracle["publication"]["official_url"],
            "https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022",
        )

    def test_source_access_and_inventory_fail_closed(self):
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        artifact = oracle["source_artifact"]

        self.assertEqual(oracle["access"]["account_required"], "free_account")
        self.assertFalse(oracle["access"]["account_used"])
        self.assertEqual(artifact["state"], "not_retrieved")
        for key in ("byte_length", "sha256", "page_count", "criterion_count", "inventory_sha256"):
            self.assertIsNone(artifact[key], key)
        self.assertFalse(oracle["inventory"]["created"])
        self.assertEqual(oracle["inventory"]["criterion_count"], None)

    def test_matrix_and_rights_review_keep_aicpa_reuse_permission_blocked(self):
        matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        rights = RIGHTS_REVIEW.read_text(encoding="utf-8")

        self.assertEqual(matrix["recorded_decision"], "HOLD")
        self.assertIn("AICPA", rights)
        self.assertIn("not been verified", rights)
        self.assertIn("derivative_mapping_analysis", rights)
        self.assertIn("statutory exception", rights)
        self.assertFalse(matrix["mapping_contract"]["positive_feasibility_probe"])

    def test_public_status_has_zero_mapping_artifacts_and_no_catalog_registration(self):
        landing = LANDING.read_text(encoding="utf-8")
        index = (ROOT / "crosswalks/README.md").read_text(encoding="utf-8")
        catalog = json.loads((ROOT / "crosswalks/catalog.json").read_text(encoding="utf-8"))

        self.assertIn("`HOLD`", landing)
        self.assertRegex(landing, r"mapping artifacts:\s*`0`")
        self.assertIn("[SOC 2](soc-2.md) — readiness `HOLD`", index)
        catalog_text = json.dumps(catalog)
        self.assertNotIn("aicpa", catalog_text.casefold())
        self.assertNotIn("soc-2", catalog_text.casefold())
        self.assertFalse(list((ROOT / "crosswalks/mappings").rglob("*soc*")))
        self.assertFalse(list((ROOT / "crosswalks/registry").glob("*soc*")))

    def test_decision_review_and_issue_traceability_are_rendered(self):
        review = DECISION_REVIEW.read_text(encoding="utf-8")
        traceability = TRACEABILITY.read_text(encoding="utf-8")

        self.assertIn("`HOLD`", review)
        self.assertIn("Issue #219", traceability)
        for trace_id in ("I219-D1", "I219-D2", "I219-D3", "I219-GO1", "I219-HOLD1"):
            self.assertRegex(traceability, rf"(?m)^\| {re.escape(trace_id)} \|")

    def test_planner_ci_and_tool_documentation_validate_the_hold_decision(self):
        planner = (ROOT / "tools/plan_validation.py").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/catalog-validation.yml").read_text(encoding="utf-8")
        readme = (ROOT / "tools/README.md").read_text(encoding="utf-8")

        self.assertIn("soc2-aicpa-tsc-mapping-go-no-go", planner)
        self.assertIn("python tools/render_soc2_aicpa_tsc_mapping_go_no_go.py --check", workflow)
        self.assertIn("tools/render_soc2_aicpa_tsc_mapping_go_no_go.py", workflow)
        self.assertIn("python tools/render_soc2_aicpa_tsc_mapping_go_no_go.py --check", readme)


if __name__ == "__main__":
    unittest.main()
