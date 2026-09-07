"""Contracts for the bounded ESAF-1100 Working Draft deepen (Issue #145)."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ESAF_1100 = ROOT / "controls" / "ESAF-1100.md"
CONTROLS_README = ROOT / "controls" / "README.md"

METHODS = ("Examine", "Interview", "Test", "Observe")
DETERMINATIONS = (
    "satisfied",
    "partially_satisfied",
    "not_satisfied",
    "not_applicable",
    "not_assessed",
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
BASELINES = ("E0", "E1", "E2", "E3", "E4")
CONTROL_INDEX_LINKS = (
    "OBJECTIVES.md",
    "CATALOG.md",
    "catalog.json",
    "CONTROL_TEMPLATE.md",
    "schema/control.schema.json",
)
COMPANION_LINKS = (
    ("ESAF-1000", "../framework/ESAF-1000.md"),
    ("ESAF-1500", "../assessment/ESAF-1500.md"),
    ("ESAF-1600", "../crosswalks/ESAF-1600.md"),
    ("ESAF-1800", "../profiles/ESAF-1800.md"),
)
TOOLKIT_LINKS = (
    "../assessment/README.md",
    "../assessment/workbook/README.md",
    "../assessment/evidence-catalog/README.md",
    "../assessment/audit-checklist/README.md",
)
# Sixteen families already published in the architecture; deepen shall not add more.
EXPECTED_FAMILIES = (
    "GOV",
    "STR",
    "RSK",
    "IAM",
    "DAT",
    "MOD",
    "APP",
    "API",
    "INF",
    "AGT",
    "OPS",
    "MON",
    "CMP",
    "AUD",
    "EDU",
    "ARC",
)


def text() -> str:
    return ESAF_1100.read_text(encoding="utf-8")


def section_after(heading: str) -> str:
    """Return body after a ## or ### heading until the next heading of equal or higher rank."""
    body = text()
    match = re.search(
        rf"(?m)^(#+)\s+{re.escape(heading)}\s*$",
        body,
    )
    if match is None:
        raise AssertionError(f"missing heading {heading!r}")
    level = len(match.group(1))
    remainder = body[match.end() :]
    next_heading = re.search(rf"(?m)^#{{1,{level}}}\s+", remainder)
    if next_heading is None:
        return remainder
    return remainder[: next_heading.start()]


def contains_normalized_phrase(haystack: str, needle: str) -> bool:
    compact = re.sub(r"\s+", " ", haystack).casefold()
    return re.sub(r"\s+", " ", needle).casefold() in compact


class Esaf1100DeepenContracts(unittest.TestCase):
    def test_document_is_working_draft_version_0_3_1(self) -> None:
        body = text()
        self.assertRegex(body, r"(?m)^\|\s*Version\s*\|\s*0\.3\.1\s*\|")
        self.assertRegex(body, r"(?m)^\|\s*Status\s*\|\s*Working Draft\s*\|")

    def test_revision_history_records_the_deepen(self) -> None:
        history = section_after("Revision history")
        self.assertIn("0.3.1", history)
        self.assertTrue(contains_normalized_phrase(history, "Working Draft"))
        self.assertTrue(
            contains_normalized_phrase(history, "ESAF-1500")
            or contains_normalized_phrase(history, "assessment")
            or contains_normalized_phrase(history, "evidence")
        )
        self.assertTrue(
            contains_normalized_phrase(history, "baseline")
            or contains_normalized_phrase(history, "cross-link")
            or contains_normalized_phrase(history, "cross link")
        )

    def test_parent_and_shared_contract_links_are_present(self) -> None:
        body = text()
        for label, href in COMPANION_LINKS:
            with self.subTest(label=label):
                self.assertRegex(
                    body,
                    rf"\[[^\]]*{re.escape(label)}[^\]]*\]\({re.escape(href)}\)",
                )

    def test_control_and_assessment_indexes_are_linked(self) -> None:
        body = text().replace("\\", "/")
        for href in CONTROL_INDEX_LINKS:
            with self.subTest(href=href):
                self.assertIn(href, body)
        for href in TOOLKIT_LINKS:
            with self.subTest(href=href):
                self.assertIn(href, body)

    def test_determination_vocabulary_matches_esaf_1500_machine_values(self) -> None:
        determinations = section_after("10.3 Determination values")
        for value in DETERMINATIONS:
            with self.subTest(value=value):
                self.assertIn(f"`{value}`", determinations)
        # Reject parallel space-separated determination identifiers.
        for banned in (
            "| partially satisfied |",
            "| not satisfied |",
            "| not applicable |",
            "| not assessed |",
        ):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, determinations)

    def test_assessment_methods_remain_exact(self) -> None:
        methods = section_after("10.2 Assessment methods")
        for method in METHODS:
            with self.subTest(method=method):
                self.assertRegex(methods, rf"(?m)^\|\s*{re.escape(method)}\s*\|")

    def test_evidence_quality_aligns_with_esaf_1500_seven_attributes(self) -> None:
        evidence = section_after("11. Evidence model")
        for attribute in QUALITY_ATTRIBUTES:
            with self.subTest(attribute=attribute):
                self.assertIn(f"**{attribute}:**", evidence)
        self.assertIn("../assessment/ESAF-1500.md", evidence.replace("\\", "/"))
        self.assertTrue(
            contains_normalized_phrase(evidence, "authoritative for shared")
            or contains_normalized_phrase(evidence, "shared evidence-record")
            or contains_normalized_phrase(evidence, "evidence-record")
        )
        self.assertTrue(
            contains_normalized_phrase(evidence, "maturity")
            and (
                contains_normalized_phrase(evidence, "ESAF-1500")
                or contains_normalized_phrase(evidence, "shall not define")
            )
        )

    def test_assessment_model_defers_shared_records_without_parallel_maturity(self) -> None:
        assessment = section_after("10. Assessment model")
        self.assertIn("../assessment/ESAF-1500.md", assessment.replace("\\", "/"))
        self.assertTrue(
            contains_normalized_phrase(assessment, "design effectiveness")
        )
        self.assertTrue(
            contains_normalized_phrase(assessment, "operating effectiveness")
        )
        # Forbid inventing an ESAF-1100 maturity table; allow deferral wording.
        for banned in (
            "| `M0` |",
            "| `M1` |",
            "| `M2` |",
            "| `M3` |",
            "| `M4` |",
            "| M0 |",
            "| M1 |",
            "| M2 |",
            "| M3 |",
            "| M4 |",
        ):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, assessment)
        self.assertTrue(
            contains_normalized_phrase(assessment, "shall not define a maturity")
            or contains_normalized_phrase(assessment, "maturity fields")
        )

    def test_baseline_model_aligns_with_esaf_1000_tiers_and_remains_unselected(self) -> None:
        baseline = section_after("9. Baseline model")
        for value in BASELINES:
            with self.subTest(value=value):
                self.assertIn(f"| {value} |", baseline)
        self.assertIn("../framework/ESAF-1000.md", baseline.replace("\\", "/"))
        self.assertTrue(
            contains_normalized_phrase(baseline, "capability tier")
            or contains_normalized_phrase(baseline, "capability tiers")
        )
        self.assertTrue(
            contains_normalized_phrase(baseline, "after sufficient controls")
            or contains_normalized_phrase(baseline, "not yet approved")
            or contains_normalized_phrase(baseline, "will be defined only after")
        )
        # Baselines must not invent M0-M4 maturity rows.
        for banned in ("| M0 |", "| M1 |", "| M2 |", "| M3 |", "| M4 |"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, baseline)
        self.assertTrue(
            contains_normalized_phrase(baseline, "does not establish a maturity")
            or contains_normalized_phrase(baseline, "not a maturity")
        )

    def test_family_population_is_unchanged(self) -> None:
        families = section_after("4. Control families")
        for family in EXPECTED_FAMILIES:
            with self.subTest(family=family):
                self.assertRegex(families, rf"(?m)^\|\s*{family}\s*\|")
        # Exactly sixteen family rows in the architecture table.
        family_rows = re.findall(r"(?m)^\|\s*[A-Z]{3}\s*\|", families)
        self.assertEqual(len(family_rows), 16)

    def test_deepen_does_not_claim_certification_or_baseline_approval(self) -> None:
        body = text().casefold()
        for phrase in (
            "esaf certification scheme",
            "certified against esaf-1100",
            "baseline selections are approved",
            "approved complete control baseline",
            "equivalence to external frameworks",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, body)

    def test_controls_readme_points_to_parent_shared_contracts_and_indexes(self) -> None:
        readme = CONTROLS_README.read_text(encoding="utf-8").replace("\\", "/")
        for needle in (
            "ESAF-1100.md",
            "Working Draft",
            "../framework/ESAF-1000.md",
            "../assessment/ESAF-1500.md",
            "OBJECTIVES.md",
            "CATALOG.md",
            "../assessment/README.md",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, readme)


if __name__ == "__main__":
    unittest.main()
