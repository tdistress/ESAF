from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.validate_assessment import validate


REPO = Path(__file__).resolve().parents[1]


class AssessmentValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(
            REPO / "assessment" / "schema",
            self.root / "assessment" / "schema",
        )
        shutil.copytree(
            REPO / "assessment" / "examples",
            self.root / "assessment" / "examples",
        )

    def load(self, name: str) -> dict[str, object]:
        path = self.root / "assessment" / "examples" / f"{name}.example.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def write(self, name: str, value: dict[str, object]) -> None:
        path = self.root / "assessment" / "examples" / f"{name}.example.json"
        path.write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def write_example(self, filename: str, value: dict[str, object]) -> None:
        path = self.root / "assessment" / "examples" / filename
        path.write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def assert_has_error(self, expected: str) -> None:
        errors = validate(self.root)
        self.assertTrue(
            any(expected in error for error in errors),
            f"missing {expected!r} in diagnostics:\n" + "\n".join(errors),
        )

    def component(
        self,
        *,
        maturity_id: str = "MAT-COMPONENT-A",
        level: str = "M0",
    ) -> dict[str, object]:
        component = self.load("maturity-assessment")
        component["maturity_id"] = maturity_id
        component["level"] = level
        level_count = int(level[1]) + 1
        component["criteria"] = component["criteria"][:level_count]
        component["component_results"] = []
        self.write_example("maturity-component.example.json", component)
        return component

    def test_valid_foundation_has_no_errors(self) -> None:
        self.assertEqual(validate(self.root), [])

    def test_duplicate_json_key_is_rejected(self) -> None:
        path = self.root / "assessment/examples/evidence-record.example.json"
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace('"title":', '"title": "duplicate",\n  "title":', 1),
            encoding="utf-8",
        )
        self.assert_has_error("duplicate JSON key 'title'")

    def test_missing_quality_attribute_is_rejected(self) -> None:
        evidence = self.load("evidence-record")
        del evidence["quality"]["relevance"]
        self.write("evidence-record", evidence)
        self.assert_has_error("quality: 'relevance' is a required property")

    def test_unresolved_evidence_result_reference_is_rejected(self) -> None:
        evidence = self.load("evidence-record")
        evidence["traceability"]["result_refs"] = ["ASR-MISSING"]
        self.write("evidence-record", evidence)
        self.assert_has_error("unresolved result reference ASR-MISSING")

    def test_unresolved_evidence_reference_is_rejected(self) -> None:
        result = self.load("assessment-result")
        result["evidence_refs"] = ["EVD-MISSING"]
        self.write("assessment-result", result)
        self.assert_has_error("unresolved evidence reference EVD-MISSING")

    def test_unresolved_finding_evidence_reference_is_rejected(self) -> None:
        result = self.load("assessment-result")
        result["findings"][0]["evidence_refs"] = ["EVD-MISSING"]
        self.write("assessment-result", result)
        self.assert_has_error("finding FND-EXAMPLE-CHANGE-REVIEW unresolved evidence reference EVD-MISSING")

    def test_duplicate_finding_identifiers_are_rejected(self) -> None:
        result = self.load("assessment-result")
        result["findings"].append(
            json.loads(json.dumps(result["findings"][0]))
        )
        self.write("assessment-result", result)
        self.assert_has_error("duplicate finding identifier")

    def test_duplicate_artifact_identifiers_are_rejected_globally(self) -> None:
        evidence = self.load("evidence-record")
        self.write_example("second-evidence.example.json", evidence)
        self.assert_has_error(
            "duplicate evidence identifier EVD-EXAMPLE-CHANGE-LOG"
        )

    def test_final_result_requires_evidence_unless_not_assessed(self) -> None:
        result = self.load("assessment-result")
        result["status"] = "final"
        result["evidence_refs"] = []
        self.write("assessment-result", result)
        self.assert_has_error("final result requires evidence")

    def test_final_result_requires_method_unless_not_assessed(self) -> None:
        result = self.load("assessment-result")
        result["status"] = "final"
        result["methods"] = []
        self.write("assessment-result", result)
        self.assert_has_error("final result requires a method")

    def test_final_not_assessed_is_exempt_from_method_and_evidence_semantics(self) -> None:
        result = self.load("assessment-result")
        result["status"] = "final"
        result["determination"] = "not_assessed"
        result["scope_exclusion_rationale"] = "This capability was excluded."
        result["design_effectiveness"] = "not_assessed"
        result["operating_effectiveness"] = "not_assessed"
        result["methods"] = []
        result["evidence_refs"] = []
        self.write("assessment-result", result)
        self.assertEqual(validate(self.root), [])

    def test_draft_result_may_have_empty_methods_and_evidence(self) -> None:
        result = self.load("assessment-result")
        result["status"] = "draft"
        result["methods"] = []
        result["evidence_refs"] = []
        self.write("assessment-result", result)
        self.assertEqual(validate(self.root), [])

    def test_invalid_not_applicable_result_is_rejected(self) -> None:
        result = self.load("assessment-result")
        result["determination"] = "not_applicable"
        result["design_effectiveness"] = "not_applicable"
        result["operating_effectiveness"] = "not_applicable"
        self.write("assessment-result", result)
        self.assert_has_error("'applicability_rationale' is a required property")

    def test_invalid_not_assessed_result_is_rejected(self) -> None:
        result = self.load("assessment-result")
        result["determination"] = "not_assessed"
        result["design_effectiveness"] = "not_assessed"
        result["operating_effectiveness"] = "not_assessed"
        self.write("assessment-result", result)
        self.assert_has_error("'scope_exclusion_rationale' is a required property")

    def test_final_result_rejects_open_finding(self) -> None:
        result = self.load("assessment-result")
        result["status"] = "final"
        result["findings"][0]["status"] = "open"
        del result["findings"][0]["disposition_at"]
        self.write("assessment-result", result)
        self.assert_has_error("final result contains open finding")

    def test_final_result_retains_accepted_finding(self) -> None:
        result = self.load("assessment-result")
        finding = result["findings"][0]
        finding["status"] = "accepted"
        finding["acceptance_authority"] = "Example risk owner"
        finding["acceptance_rationale"] = "The fictional residual risk is accepted."
        finding["review_at"] = "2026-10-24T16:30:00Z"
        finding["residual_risk"] = "Minor fictional residual risk."
        self.write("assessment-result", result)
        self.assertEqual(validate(self.root), [])

    def test_final_result_rejects_placeholder_language(self) -> None:
        result = self.load("assessment-result")
        result["determination_rationale"] = "TODO: finish this rationale"
        self.write("assessment-result", result)
        self.assert_has_error("unresolved placeholder language")

    def test_final_result_rejects_bracketed_placeholder_language(self) -> None:
        result = self.load("assessment-result")
        result["determination_rationale"] = "Review by [insert approver]."
        self.write("assessment-result", result)
        self.assert_has_error("unresolved placeholder language")

    def test_final_result_rejects_placeholder_inside_brackets(self) -> None:
        result = self.load("assessment-result")
        result["determination_rationale"] = "Review by [reviewer TBD]."
        self.write("assessment-result", result)
        self.assert_has_error("unresolved placeholder language")

    def test_maturity_requires_every_prerequisite_level_in_order(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["level"] = "M2"
        self.write("maturity-assessment", maturity)
        self.assert_has_error("criteria levels must equal M0 through M2")

    def test_maturity_rejects_skipped_level(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["level"] = "M2"
        maturity["criteria"][1]["level"] = "M2"
        maturity["criteria"][1]["criterion_id"] = "M2-CHANGE-MANAGEMENT-DEFINED"
        self.write("maturity-assessment", maturity)
        self.assert_has_error("criteria levels must equal M0 through M2")

    def test_maturity_rejects_duplicate_level(self) -> None:
        maturity = self.load("maturity-assessment")
        duplicate = json.loads(json.dumps(maturity["criteria"][1]))
        duplicate["criterion_id"] = "M1-CHANGE-MANAGEMENT-SECOND"
        maturity["criteria"].append(duplicate)
        self.write("maturity-assessment", maturity)
        self.assert_has_error("criteria levels must equal M0 through M1")

    def test_maturity_rejects_out_of_order_levels(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"].reverse()
        self.write("maturity-assessment", maturity)
        self.assert_has_error("criteria levels must equal M0 through M1")

    def test_maturity_rejects_unmet_prerequisite(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][0]["met"] = False
        self.write("maturity-assessment", maturity)
        self.assert_has_error("unmet prerequisite M0")

    def test_maturity_rejects_empty_criterion_basis(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][0]["basis_refs"] = []
        self.write("maturity-assessment", maturity)
        self.assert_has_error("criterion M0 basis_refs must not be empty")

    def test_maturity_rejects_unresolved_top_level_basis(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["basis_refs"] = ["ASR-MISSING"]
        self.write("maturity-assessment", maturity)
        self.assert_has_error("unresolved basis reference ASR-MISSING")

    def test_maturity_rejects_unresolved_criterion_basis(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][0]["basis_refs"] = ["EVD-MISSING"]
        self.write("maturity-assessment", maturity)
        self.assert_has_error(
            "criterion M0 unresolved basis reference EVD-MISSING"
        )

    def test_maturity_rejects_unresolved_component_reference(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": "MAT-MISSING",
                "level": "M0",
                "applicability": "applicable",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error("unresolved component maturity reference MAT-MISSING")

    def test_maturity_rejects_self_referencing_component(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": maturity["maturity_id"],
                "level": maturity["level"],
                "applicability": "applicable",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error("self-referencing component")

    def test_maturity_rejects_component_level_mismatch(self) -> None:
        self.component(level="M0")
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": "MAT-COMPONENT-A",
                "level": "M1",
                "applicability": "applicable",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error(
            "component MAT-COMPONENT-A declares M1 but resolved record declares M0"
        )

    def test_final_rollup_rejects_draft_component(self) -> None:
        component = self.component(level="M1")
        component["status"] = "draft"
        component["criteria"][0]["met"] = False
        self.write_example("maturity-component.example.json", component)
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": "MAT-COMPONENT-A",
                "level": "M1",
                "applicability": "applicable",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error(
            "applicable component MAT-COMPONENT-A must be final"
        )

    def test_rollup_cannot_exceed_lowest_applicable_component(self) -> None:
        self.component(level="M0")
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": "MAT-COMPONENT-A",
                "level": "M0",
                "applicability": "applicable",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error("exceeds lowest applicable component M0")

    def test_excluded_component_with_rationale_is_ignored_in_rollup(self) -> None:
        self.component(level="M0")
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": "MAT-COMPONENT-A",
                "level": "M0",
                "applicability": "not_applicable",
                "rationale": "The fictional component is outside the stated scope.",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assertEqual(validate(self.root), [])

    def test_excluded_component_must_resolve_to_final_record(self) -> None:
        component = self.component(level="M0")
        component["status"] = "draft"
        self.write_example("maturity-component.example.json", component)
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": "MAT-COMPONENT-A",
                "level": "M0",
                "applicability": "not_applicable",
                "rationale": "The fictional component is outside the stated scope.",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error(
            "component MAT-COMPONENT-A must be final"
        )

    def test_excluded_component_without_rationale_is_rejected(self) -> None:
        self.component(level="M0")
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": "MAT-COMPONENT-A",
                "level": "M0",
                "applicability": "not_applicable",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error("not_applicable component requires rationale")

    def test_not_assessed_component_cannot_support_final_rollup(self) -> None:
        self.component(level="M0")
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {
                "maturity_ref": "MAT-COMPONENT-A",
                "level": "M0",
                "applicability": "not_assessed",
            }
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error("final roll-up contains not_assessed component")

    def test_numeric_average_field_is_rejected(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["average"] = 2.5
        self.write("maturity-assessment", maturity)
        errors = validate(self.root)
        self.assertTrue(
            any("average" in error and "unexpected" in error for error in errors)
        )

    def test_conformance_overclaiming_field_is_rejected(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["compliance_status"] = "compliant"
        self.write("maturity-assessment", maturity)
        errors = validate(self.root)
        self.assertTrue(
            any(
                "compliance_status" in error and "unexpected" in error
                for error in errors
            )
        )

    def test_maturity_rationale_cannot_assert_compliance(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            "This maturity result establishes compliance."
        )
        self.write("maturity-assessment", maturity)
        self.assert_has_error("prohibited conformance assertion")

    def test_maturity_limitation_cannot_assert_continuous_assurance(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["limitations"] = [
            "This maturity result provides continuous assurance."
        ]
        self.write("maturity-assessment", maturity)
        self.assert_has_error("prohibited conformance assertion")

    def test_non_claim_language_is_not_rejected(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            "The review does not establish compliance or certification."
        )
        maturity["limitations"] = [
            "Certification evidence was outside the fictional assessment scope."
        ]
        self.write("maturity-assessment", maturity)
        self.assertEqual(validate(self.root), [])

    def test_explicitly_negated_assertions_are_not_rejected(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            "No maturity result establishes compliance."
        )
        maturity["limitations"] = [
            "Nothing provides continuous assurance."
        ]
        self.write("maturity-assessment", maturity)
        self.assertEqual(validate(self.root), [])

    def test_no_evidence_negates_compliance_assertion(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            "No evidence establishes compliance."
        )
        self.write("maturity-assessment", maturity)
        self.assertEqual(validate(self.root), [])

    def test_no_component_negates_continuous_assurance_assertion(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["limitations"] = [
            "No component provides continuous assurance."
        ]
        self.write("maturity-assessment", maturity)
        self.assertEqual(validate(self.root), [])

    def test_quoted_prohibited_phrase_is_discussion_not_assertion(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            'The phrase "establishes certification" is discussed, not asserted.'
        )
        self.write("maturity-assessment", maturity)
        self.assertEqual(validate(self.root), [])

    def test_denial_before_but_does_not_mask_positive_assertion(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            "No evidence establishes compliance, "
            "but this result establishes compliance."
        )
        self.write("maturity-assessment", maturity)
        errors = [
            error
            for error in validate(self.root)
            if "prohibited conformance assertion" in error
        ]
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("establishes compliance", errors[0])

    def test_unrelated_no_before_and_does_not_negate_assertion(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            "No caveat applies, and this result establishes compliance."
        )
        self.write("maturity-assessment", maturity)
        self.assert_has_error("prohibited conformance assertion")

    def test_without_elsewhere_does_not_negate_assertion(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            "Without qualification, this result establishes compliance."
        )
        self.write("maturity-assessment", maturity)
        self.assert_has_error("prohibited conformance assertion")

    def test_endorsed_quotation_is_rejected(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            'Management concludes, "This maturity result establishes compliance."'
        )
        self.write("maturity-assessment", maturity)
        self.assert_has_error("prohibited conformance assertion")

    def test_unknown_schema_locator_is_rejected(self) -> None:
        evidence = self.load("evidence-record")
        evidence["$schema"] = "../schema/unknown.schema.json"
        self.write("evidence-record", evidence)
        self.assert_has_error("unsupported schema locator")

    def test_invalid_record_does_not_pollute_global_reference_checks(self) -> None:
        result = self.load("assessment-result")
        result["result_id"] = "ASR-INVALID-EXTRA"
        result["unexpected"] = True
        result["evidence_refs"] = ["EVD-MISSING"]
        self.write_example("zzz-invalid-result.example.json", result)
        errors = validate(self.root)
        invalid_errors = [
            error
            for error in errors
            if "zzz-invalid-result.example.json" in error
        ]
        self.assertTrue(any("unexpected" in error for error in invalid_errors))
        self.assertFalse(
            any("unresolved evidence reference" in error for error in errors)
        )
        self.assertFalse(
            any("duplicate finding identifier" in error for error in errors)
        )

    def test_missing_required_schema_is_rejected(self) -> None:
        path = (
            self.root
            / "assessment/schema/maturity-assessment.schema.json"
        )
        path.unlink()
        self.assert_has_error(
            "assessment/schema/maturity-assessment.schema.json: required file is missing"
        )

    def test_missing_required_example_is_rejected(self) -> None:
        path = (
            self.root
            / "assessment/examples/assessment-result.example.json"
        )
        path.unlink()
        self.assert_has_error(
            "assessment/examples/assessment-result.example.json: required file is missing"
        )

    def test_invalid_schema_is_rejected_without_traceback(self) -> None:
        path = (
            self.root
            / "assessment/schema/maturity-assessment.schema.json"
        )
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["type"] = "invalid-type"
        path.write_text(json.dumps(schema), encoding="utf-8")
        self.assert_has_error(
            "assessment/schema/maturity-assessment.schema.json: invalid schema"
        )

    def test_malformed_json_is_rejected_without_traceback(self) -> None:
        path = (
            self.root
            / "assessment/examples/assessment-result.example.json"
        )
        path.write_text("{", encoding="utf-8")
        self.assert_has_error(
            "assessment/examples/assessment-result.example.json: invalid JSON"
        )

    def test_diagnostics_have_stable_repository_relative_order(self) -> None:
        assessment = (
            self.root
            / "assessment/examples/assessment-result.example.json"
        )
        evidence = (
            self.root
            / "assessment/examples/evidence-record.example.json"
        )
        assessment.write_text("{", encoding="utf-8")
        evidence.write_text("{", encoding="utf-8")
        errors = validate(self.root)
        relevant = [error for error in errors if "invalid JSON" in error]
        self.assertEqual(
            relevant,
            [
                "assessment/examples/assessment-result.example.json: invalid JSON",
                "assessment/examples/evidence-record.example.json: invalid JSON",
            ],
        )

    def test_cli_reports_success(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(REPO / "tools/validate_assessment.py"), "--check"],
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            completed.stdout.strip(),
            "Successfully validated 3 assessment schemas and 3 tracked examples.",
        )


if __name__ == "__main__":
    unittest.main()
