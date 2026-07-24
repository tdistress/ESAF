from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "assessment" / "ESAF-1500.md"

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


if __name__ == "__main__":
    unittest.main()
