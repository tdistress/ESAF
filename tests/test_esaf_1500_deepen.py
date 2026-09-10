"""Contracts for the bounded ESAF-1500 Working Draft deepen (Issue #172)."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ESAF_1500 = ROOT / "assessment" / "ESAF-1500.md"
ASSESSMENT_README = ROOT / "assessment" / "README.md"

COMPANION_LINKS = (
    ("ESAF-1000", "../framework/ESAF-1000.md"),
    ("ESAF-1100", "../controls/ESAF-1100.md"),
    ("ESAF-1600", "../crosswalks/ESAF-1600.md"),
    ("ESAF-1800", "../profiles/ESAF-1800.md"),
)

TOOLKIT_LINKS = (
    "workbook/README.md",
    "evidence-catalog/README.md",
    "audit-checklist/README.md",
)

SCHEMA_LINKS = (
    "schema/evidence-record.schema.json",
    "schema/assessment-result.schema.json",
    "schema/maturity-assessment.schema.json",
)

EXAMPLE_LINKS = (
    "examples/evidence-record.example.json",
    "examples/assessment-result.example.json",
    "examples/maturity-assessment.example.json",
)

MATURITY_LEVELS = ("M0", "M1", "M2", "M3", "M4")


def text() -> str:
    return ESAF_1500.read_text(encoding="utf-8")


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


class Esaf1500DeepenContracts(unittest.TestCase):
    def test_document_is_working_draft_version_0_1_1(self) -> None:
        body = text()
        self.assertRegex(body, r"(?m)^\|\s*Version\s*\|\s*0\.1\.1\s*\|")
        self.assertRegex(body, r"(?m)^\|\s*Status\s*\|\s*Working Draft\s*\|")

    def test_revision_history_records_the_deepen(self) -> None:
        history = section_after("Revision history")
        self.assertIn("0.1.1", history)
        self.assertIn("0.1.0", history)
        self.assertTrue(contains_normalized_phrase(history, "Working Draft"))
        self.assertTrue(
            contains_normalized_phrase(history, "cross-link")
            or contains_normalized_phrase(history, "cross link")
            or contains_normalized_phrase(history, "companion")
        )
        self.assertTrue(
            contains_normalized_phrase(history, "workbook")
            or contains_normalized_phrase(history, "evidence catalog")
            or contains_normalized_phrase(history, "audit checklist")
            or contains_normalized_phrase(history, "toolkit")
        )

    def test_companion_publications_are_linked(self) -> None:
        body = text()
        for label, href in COMPANION_LINKS:
            with self.subTest(label=label):
                self.assertRegex(
                    body,
                    rf"\[[^\]]*{re.escape(label)}[^\]]*\]\({re.escape(href)}\)",
                )

    def test_toolkit_surfaces_are_linked(self) -> None:
        body = text().replace("\\", "/")
        for href in TOOLKIT_LINKS:
            with self.subTest(href=href):
                self.assertRegex(
                    body,
                    rf"\[[^\]]*\]\({re.escape(href)}\)",
                )

    def test_schemas_and_examples_remain_discoverable(self) -> None:
        body = text().replace("\\", "/")
        for href in SCHEMA_LINKS + EXAMPLE_LINKS:
            with self.subTest(href=href):
                self.assertRegex(
                    body,
                    rf"\[[^\]]*\]\({re.escape(href)}\)",
                )

    def test_maturity_scale_remains_m0_through_m4(self) -> None:
        maturity = section_after("Maturity model")
        for level in MATURITY_LEVELS:
            with self.subTest(level=level):
                self.assertIn(f"`{level}`", maturity)
        self.assertNotRegex(maturity, r"`M5`")
        self.assertTrue(
            contains_normalized_phrase(maturity, "shall not rename the levels")
            or contains_normalized_phrase(
                maturity, "shall not rename the levels, weaken"
            )
        )

    def test_schema_version_contract_remains_0_1_0(self) -> None:
        body = text()
        # Document version may be 0.1.1; shared JSON schema_version stays 0.1.0.
        self.assertRegex(
            body,
            r"(?m)^\|\s*`schema_version`\s*\|\s*`0\.1\.0`\s*\.",
        )
        self.assertTrue(
            contains_normalized_phrase(
                body, "schema_version` of `0.1.0`"
            )
            or contains_normalized_phrase(
                body, "`schema_version` of `0.1.0`"
            )
        )

    def test_deepen_does_not_claim_certification_or_compliance(self) -> None:
        body = text()
        self.assertTrue(
            contains_normalized_phrase(body, "does not define a certification scheme")
        )
        self.assertTrue(
            contains_normalized_phrase(body, "establish compliance, certification")
            or contains_normalized_phrase(
                body, "establish compliance, certification, equivalence"
            )
        )
        forbidden = (
            "establishes certification",
            "establishes compliance",
            "provides continuous assurance",
            "accredited certification",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertFalse(contains_normalized_phrase(body, phrase))

    def test_assessment_readme_syncs_version_and_toolkit(self) -> None:
        readme = ASSESSMENT_README.read_text(encoding="utf-8")
        self.assertTrue(
            contains_normalized_phrase(readme, "Working Draft 0.1.1")
            or contains_normalized_phrase(readme, "0.1.1")
        )
        for href in (
            "ESAF-1500.md",
            "workbook/README.md",
            "evidence-catalog/README.md",
            "audit-checklist/README.md",
            "schema/evidence-record.schema.json",
            "examples/evidence-record.example.json",
        ):
            with self.subTest(href=href):
                self.assertIn(href, readme.replace("\\", "/"))


if __name__ == "__main__":
    unittest.main()
