from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from tools.validate_assessment import ASSESSMENT_FORMAT_CHECKER


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "assessment" / "ESAF-1500.md"
SCHEMA_ROOT = ROOT / "assessment" / "schema"
EXAMPLE_ROOT = ROOT / "assessment" / "examples"
SCHEMA_NAMES = (
    "evidence-record",
    "assessment-result",
    "maturity-assessment",
)

REQUIRED_HEADINGS = (
    "Purpose",
    "Scope",
    "Relationship to the ESAF library",
    "Assessment principles",
    "Evidence records",
    "Evidence quality",
    "Assessment scope and methods",
    "Assessment results",
    "Findings and dispositions",
    "Maturity model",
    "Conformance and maturity",
    "Aggregation",
    "Traceability and change control",
    "Implementation and validation",
)
QUALITY_ATTRIBUTES = (
    "relevance",
    "reliability",
    "completeness",
    "timeliness",
    "attribution",
    "integrity",
    "traceability",
)
QUALITY_FIELDS = QUALITY_ATTRIBUTES + (
    "sufficiency",
    "evaluated_by",
    "evaluated_at",
    "sufficiency_rationale",
)
METHODS = ("Examine", "Interview", "Test", "Observe")
DETERMINATIONS = (
    "satisfied",
    "partially_satisfied",
    "not_satisfied",
    "not_applicable",
    "not_assessed",
)
MATURITY_LEVELS = (
    ("M0", "Ad hoc"),
    ("M1", "Managed"),
    ("M2", "Defined"),
    ("M3", "Measured"),
    ("M4", "Adaptive"),
)


def text() -> str:
    return STANDARD.read_text(encoding="utf-8")


class AssessmentFoundationTests(unittest.TestCase):
    def test_normative_standard_exists_with_required_sections(self) -> None:
        document = text()
        for heading in REQUIRED_HEADINGS:
            with self.subTest(heading=heading):
                self.assertRegex(document, rf"(?m)^## {re.escape(heading)}$")

    def test_evidence_quality_vocabulary_is_exact(self) -> None:
        section = text().split("## Evidence quality", 1)[1].split("\n## ", 1)[0]
        for attribute in QUALITY_ATTRIBUTES:
            self.assertEqual(section.count(f"**{attribute}:**"), 1)
        for rating in ("adequate", "limited", "inadequate", "not_evaluated"):
            self.assertIn(f"`{rating}`", section)
        self.assertIn("shall not be calculated by averaging", section)

    def test_methods_and_determinations_reuse_esaf_1100(self) -> None:
        document = text()
        for method in METHODS:
            self.assertIn(f"`{method}`", document)
        for determination in DETERMINATIONS:
            self.assertIn(f"`{determination}`", document)
        self.assertIn("ESAF-1100", document)

    def test_maturity_levels_are_exact_ordered_and_cumulative(self) -> None:
        section = text().split("## Maturity model", 1)[1].split("\n## ", 1)[0]
        positions = []
        for level, name in MATURITY_LEVELS:
            marker = f"`{level}` | {name}"
            self.assertEqual(section.count(marker), 1)
            positions.append(section.index(marker))
        self.assertEqual(positions, sorted(positions))
        self.assertIn("levels are cumulative", section)

    def test_maturity_cannot_replace_conformance(self) -> None:
        document = text()
        for determination in ("not_assessed", "not_satisfied", "partially_satisfied"):
            self.assertIn(determination, document)
        for prohibited in (
            "compliance",
            "certification",
            "equivalence",
            "endorsement",
            "continuous assurance",
        ):
            self.assertIn(prohibited, document.casefold())

    def test_rollup_is_lowest_substantiated_level_without_averaging(self) -> None:
        section = text().split("## Aggregation", 1)[1].split("\n## ", 1)[0]
        self.assertIn("lowest substantiated applicable component level", section)
        self.assertIn("Numeric averaging", section)
        self.assertIn("not-assessed components", section)

    def test_repository_indexes_link_the_normative_guide(self) -> None:
        expected = {
            "README.md": "[ESAF-1500](assessment/ESAF-1500.md)",
            "assessment/README.md": "[ESAF-1500](ESAF-1500.md)",
            "framework/ESAF-1000.md": "[ESAF-1500](../assessment/ESAF-1500.md)",
            "controls/ESAF-1100.md": "[ESAF-1500](../assessment/ESAF-1500.md)",
            "profiles/README.md": "[ESAF-1500](../assessment/ESAF-1500.md)",
        }
        for relative, marker in expected.items():
            with self.subTest(relative=relative):
                self.assertIn(marker, (ROOT / relative).read_text(encoding="utf-8"))

    def test_tools_and_contributing_document_the_validator(self) -> None:
        for relative in ("tools/README.md", "CONTRIBUTING.md", "AGENTS.md"):
            with self.subTest(relative=relative):
                self.assertIn(
                    "python tools/validate_assessment.py --check",
                    (ROOT / relative).read_text(encoding="utf-8"),
                )

    def test_ci_runs_assessment_validation_for_assessment_changes(self) -> None:
        workflow = (
            ROOT / ".github/workflows/catalog-validation.yml"
        ).read_text(encoding="utf-8")
        self.assertEqual(workflow.count('- "assessment/**"'), 2)
        self.assertEqual(workflow.count('- "tools/validate_assessment.py"'), 2)
        self.assertIn("run: python tools/validate_assessment.py --check", workflow)

    def test_profile_contract_cannot_define_local_maturity_scale(self) -> None:
        profile = (ROOT / "profiles/README.md").read_text(encoding="utf-8")
        self.assertIn("shall reuse", profile)
        self.assertIn(
            "shall not define a profile-local replacement maturity scale", profile
        )

    def test_completed_foundation_is_removed_from_backlog(self) -> None:
        backlog = (ROOT / "project/BACKLOG.md").read_text(encoding="utf-8")
        self.assertNotIn("Define the minimum ESAF-1500 assessment foundation", backlog)


class AssessmentSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = {
            name: json.loads(
                (SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8")
            )
            for name in SCHEMA_NAMES
        }
        self.examples = {
            name: json.loads(
                (EXAMPLE_ROOT / f"{name}.example.json").read_text(encoding="utf-8")
            )
            for name in SCHEMA_NAMES
        }

    def test_schemas_are_strict_draft_2020_12_documents(self) -> None:
        for name, schema in self.schemas.items():
            with self.subTest(name=name):
                self.assertEqual(
                    schema["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )
                Draft202012Validator.check_schema(schema)
                self.assertFalse(schema["additionalProperties"])

    def test_examples_validate_against_their_schemas(self) -> None:
        for name in SCHEMA_NAMES:
            with self.subTest(name=name):
                errors = list(
                    Draft202012Validator(
                        self.schemas[name],
                        format_checker=ASSESSMENT_FORMAT_CHECKER,
                    ).iter_errors(self.examples[name])
                )
                self.assertEqual(errors, [])

    def test_examples_are_explicitly_fictional_and_non_authoritative(self) -> None:
        notice = (
            "Fictional non-authoritative example; no organization, ESAF control, "
            "profile, or external framework has been assessed."
        )
        for name, example in self.examples.items():
            with self.subTest(name=name):
                self.assertEqual(example["example_notice"], notice)

    def test_exported_rfc3339_checker_rejects_malformed_values(self) -> None:
        for value in (
            "0000-02-29T00:00:00Z",
            "1991-06-30T23:59:60.123Z",
            "1990-12-31T23:59:60Z",
            "1991-01-01T08:59:60+09:00",
            "2026-07-24t15:00:00z",
            "2026-07-24T15:00:00+07:30",
        ):
            with self.subTest(value=value):
                self.assertTrue(
                    ASSESSMENT_FORMAT_CHECKER.conforms(value, "date-time")
                )
        for value in (
            "not-a-date-time",
            "0000-02-30T00:00:00Z",
            "\u0662\u0660\u0662\u0664-\u0660\u0666-\u0663\u0660T\u0662\u0663:\u0665\u0669:\u0665\u0669Z",
            "2026-02-29T15:00:00Z",
            "2024-02-29T23:59:60Z",
            "1991-01-01T09:00:60+09:00",
            "2026-07-24 15:00:00Z",
            "2026-07-24T24:00:00Z",
            "2026-07-24T15:00:00",
            "2026-07-24T15:00:00+07:60",
        ):
            with self.subTest(value=value):
                self.assertFalse(
                    ASSESSMENT_FORMAT_CHECKER.conforms(value, "date-time")
                )

    def test_assessment_schemas_reject_malformed_datetime_fields(self) -> None:
        fixtures = (
            ("evidence-record", ("collected_at",), "2026-02-29T15:00:00Z"),
            (
                "assessment-result",
                ("time_boundary", "assessment_start"),
                "2026-07-24 15:00:00Z",
            ),
            ("maturity-assessment", ("assessed_at",), "2026-07-24T15:00:00"),
        )
        for name, path, invalid_value in fixtures:
            with self.subTest(name=name, path=path):
                value = json.loads(json.dumps(self.examples[name]))
                target = value
                for part in path[:-1]:
                    target = target[part]
                target[path[-1]] = invalid_value
                validator = Draft202012Validator(
                    self.schemas[name], format_checker=ASSESSMENT_FORMAT_CHECKER
                )
                self.assertTrue(list(validator.iter_errors(value)))

    def test_evidence_schema_requires_every_quality_attribute(self) -> None:
        quality = self.schemas["evidence-record"]["properties"]["quality"]
        self.assertCountEqual(quality["required"], QUALITY_FIELDS)
        self.assertCountEqual(quality["properties"], QUALITY_FIELDS)

    def test_evidence_schema_has_no_unused_quality_definition(self) -> None:
        self.assertNotIn("quality", self.schemas["evidence-record"]["$defs"])

    def test_evidence_schema_accepts_each_period_and_integrity_alternative(self) -> None:
        validator = Draft202012Validator(
            self.schemas["evidence-record"],
            format_checker=ASSESSMENT_FORMAT_CHECKER,
        )
        fixtures = (
            (
                "point-in-time period with digest integrity",
                {"point_in_time": "2026-06-30T23:59:59Z"},
                {
                    "digest_algorithm": "sha-256",
                    "digest": "0123456789abcdef" * 4,
                },
            ),
            (
                "inclusive range with protected-record integrity",
                {
                    "start": "2026-04-01T00:00:00Z",
                    "end": "2026-06-30T23:59:59Z",
                },
                {
                    "protected_record_locator": "example://protected/evidence-record",
                    "verification_method": "Verify the immutable record's access log.",
                },
            ),
        )
        for name, period, integrity in fixtures:
            with self.subTest(name=name):
                evidence = json.loads(json.dumps(self.examples["evidence-record"]))
                evidence["period"] = period
                evidence["integrity"] = integrity
                self.assertEqual(list(validator.iter_errors(evidence)), [])

    def test_evidence_schema_rejects_invalid_period_and_integrity_alternatives(self) -> None:
        validator = Draft202012Validator(
            self.schemas["evidence-record"],
            format_checker=ASSESSMENT_FORMAT_CHECKER,
        )
        fixtures = (
            (
                "invalid point-in-time period",
                {"point_in_time": "not-a-date-time"},
                {
                    "digest_algorithm": "sha-256",
                    "digest": "0123456789abcdef" * 4,
                },
            ),
            (
                "point-in-time period with range member",
                {
                    "point_in_time": "2026-06-30T23:59:59Z",
                    "start": "2026-04-01T00:00:00Z",
                },
                {
                    "digest_algorithm": "sha-256",
                    "digest": "0123456789abcdef" * 4,
                },
            ),
            (
                "invalid inclusive range",
                {
                    "start": "2026-04-01T00:00:00Z",
                    "end": "not-a-date-time",
                },
                {
                    "protected_record_locator": "example://protected/evidence-record",
                    "verification_method": "Verify the immutable record's access log.",
                },
            ),
            (
                "inclusive range without end",
                {
                    "start": "2026-04-01T00:00:00Z",
                },
                {
                    "protected_record_locator": "example://protected/evidence-record",
                    "verification_method": "Verify the immutable record's access log.",
                },
            ),
            (
                "invalid digest integrity",
                {"point_in_time": "2026-06-30T23:59:59Z"},
                {"digest_algorithm": "sha-256", "digest": "not-a-digest"},
            ),
            (
                "invalid protected-record integrity",
                {
                    "start": "2026-04-01T00:00:00Z",
                    "end": "2026-06-30T23:59:59Z",
                },
                {"protected_record_locator": "example://protected/evidence-record"},
            ),
        )
        for name, period, integrity in fixtures:
            with self.subTest(name=name):
                evidence = json.loads(json.dumps(self.examples["evidence-record"]))
                evidence["period"] = period
                evidence["integrity"] = integrity
                self.assertTrue(list(validator.iter_errors(evidence)))

    def test_schema_enumerations_match_the_normative_contract(self) -> None:
        evidence = self.schemas["evidence-record"]
        result = self.schemas["assessment-result"]
        maturity = self.schemas["maturity-assessment"]
        self.assertEqual(
            evidence["$defs"]["qualityRating"]["enum"],
            ["adequate", "limited", "inadequate", "not_evaluated"],
        )
        self.assertEqual(
            evidence["properties"]["evidence_type"]["enum"],
            [
                "policy", "procedure", "record", "configuration", "log",
                "technical_test", "observation", "interview", "metric", "contract",
                "external_assurance", "other",
            ],
        )
        self.assertEqual(
            evidence["properties"]["quality"]["properties"]["sufficiency"]["enum"],
            ["sufficient", "limited", "insufficient"],
        )
        self.assertEqual(
            result["$defs"]["method"]["properties"]["method"]["enum"],
            list(METHODS),
        )
        self.assertEqual(
            result["properties"]["determination"]["enum"],
            list(DETERMINATIONS),
        )
        self.assertEqual(
            maturity["properties"]["level"]["enum"],
            [level for level, _name in MATURITY_LEVELS],
        )

    def test_every_object_boundary_rejects_extra_properties(self) -> None:
        def walk(value: object, path: tuple[object, ...] = ()):
            if isinstance(value, dict):
                yield path
                for key, child in value.items():
                    yield from walk(child, (*path, key))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    yield from walk(child, (*path, index))

        for name, example in self.examples.items():
            validator = Draft202012Validator(
                self.schemas[name], format_checker=ASSESSMENT_FORMAT_CHECKER
            )
            for path in walk(example):
                mutated = json.loads(json.dumps(example))
                target = mutated
                for part in path:
                    target = target[part]
                target["unexpected"] = True
                with self.subTest(name=name, path=path):
                    self.assertTrue(list(validator.iter_errors(mutated)))


class AssessmentWorkbookStarterTests(unittest.TestCase):
    workbook_root = ROOT / "assessment" / "workbook"
    worksheet_root = workbook_root / "worksheets"
    worksheet_files = {
        "evidence-record": worksheet_root / "evidence-record.worksheet.json",
        "assessment-result": worksheet_root / "assessment-result.worksheet.json",
        "maturity-assessment": worksheet_root
        / "maturity-assessment.worksheet.json",
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            name: json.loads(
                (SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8")
            )
            for name in SCHEMA_NAMES
        }

    def test_workbook_guide_is_draft_and_nonclaiming(self) -> None:
        guide = (self.workbook_root / "ESAF-1500-workbook.md").read_text(
            encoding="utf-8"
        )
        readme = (self.workbook_root / "README.md").read_text(encoding="utf-8")
        for document in (guide, readme):
            with self.subTest(document=document[:40]):
                self.assertRegex(document, r"(?im)\bDraft\b")
                self.assertRegex(document, r"(?im)certification")
                self.assertRegex(document, r"(?im)compliance")
                self.assertIn("ESAF-1500", document)
                self.assertIn("ESAF-1100", document)

    def test_workbook_worksheets_validate_against_esaf_1500_schemas(self) -> None:
        for name, path in self.worksheet_files.items():
            with self.subTest(name=name):
                self.assertTrue(path.is_file(), msg=f"missing {path}")
                document = json.loads(path.read_text(encoding="utf-8"))
                validator = Draft202012Validator(
                    self.schemas[name],
                    format_checker=ASSESSMENT_FORMAT_CHECKER,
                )
                errors = list(validator.iter_errors(document))
                self.assertEqual(
                    errors,
                    [],
                    msg="; ".join(error.message for error in errors),
                )
                if name != "evidence-record":
                    self.assertEqual(document.get("status"), "draft")


if __name__ == "__main__":
    unittest.main()
