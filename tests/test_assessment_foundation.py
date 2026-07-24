from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


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
                        format_checker=FormatChecker(),
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

    def test_evidence_schema_requires_every_quality_attribute(self) -> None:
        required = set(
            self.schemas["evidence-record"]["properties"]["quality"]["required"]
        )
        self.assertTrue(set(QUALITY_ATTRIBUTES).issubset(required))

    def test_schema_enumerations_match_the_normative_contract(self) -> None:
        evidence = self.schemas["evidence-record"]
        result = self.schemas["assessment-result"]
        maturity = self.schemas["maturity-assessment"]
        self.assertEqual(
            evidence["$defs"]["qualityRating"]["enum"],
            ["adequate", "limited", "inadequate", "not_evaluated"],
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
                self.schemas[name], format_checker=FormatChecker()
            )
            for path in walk(example):
                mutated = json.loads(json.dumps(example))
                target = mutated
                for part in path:
                    target = target[part]
                target["unexpected"] = True
                with self.subTest(name=name, path=path):
                    self.assertTrue(list(validator.iter_errors(mutated)))


if __name__ == "__main__":
    unittest.main()
