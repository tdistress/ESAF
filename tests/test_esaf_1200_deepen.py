"""Contracts for the bounded ESAF-1200 Working Draft deepen (Issue #160)."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ESAF_1200 = ROOT / "architectures" / "ESAF-1200.md"
ARCHITECTURES_README = ROOT / "architectures" / "README.md"
PATTERNS_README = ROOT / "architectures" / "patterns" / "README.md"

EXPECTED_PATTERNS = (
    "ARC-P100",
    "ARC-P110",
    "ARC-P120",
    "ARC-P130",
    "ARC-P140",
    "ARC-P150",
    "ARC-P160",
)

COMPANION_LINKS = (
    ("ESAF-1000", "../framework/ESAF-1000.md"),
    ("ESAF-1100", "../controls/ESAF-1100.md"),
    ("ESAF-1400", "../implementation/ESAF-1400.md"),
    ("ESAF-1500", "../assessment/ESAF-1500.md"),
    ("ESAF-1600", "../crosswalks/ESAF-1600.md"),
)

FOUNDATION_LINKS = (
    "PATTERN_SELECTION.md",
    "TRUST_ZONES.md",
    "patterns/README.md",
    "PRINCIPLES.md",
    "ARCHITECTURE_TEMPLATE.md",
    "overlays/README.md",
    "decisions/README.md",
)


def text() -> str:
    return ESAF_1200.read_text(encoding="utf-8")


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


class Esaf1200DeepenContracts(unittest.TestCase):
    def test_document_is_working_draft_version_0_4_1(self) -> None:
        body = text()
        self.assertRegex(body, r"(?m)^\|\s*Version\s*\|\s*0\.4\.1\s*\|")
        self.assertRegex(body, r"(?m)^\|\s*Status\s*\|\s*Working Draft\s*\|")

    def test_revision_history_records_the_deepen(self) -> None:
        history = section_after("Revision history")
        self.assertIn("0.4.1", history)
        self.assertIn("0.4-alpha", history)
        self.assertTrue(contains_normalized_phrase(history, "Working Draft"))
        self.assertTrue(
            contains_normalized_phrase(history, "cross-link")
            or contains_normalized_phrase(history, "cross link")
            or contains_normalized_phrase(history, "companion")
        )
        self.assertTrue(
            contains_normalized_phrase(history, "pattern")
            or contains_normalized_phrase(history, "trust zone")
            or contains_normalized_phrase(history, "selection")
        )

    def test_companion_publications_are_linked(self) -> None:
        body = text()
        for label, href in COMPANION_LINKS:
            with self.subTest(label=label):
                self.assertRegex(
                    body,
                    rf"\[[^\]]*{re.escape(label)}[^\]]*\]\({re.escape(href)}\)",
                )

    def test_foundation_surfaces_are_linked(self) -> None:
        body = text().replace("\\", "/")
        for href in FOUNDATION_LINKS:
            with self.subTest(href=href):
                self.assertIn(href, body)

    def test_pattern_population_remains_seven_draft_patterns(self) -> None:
        patterns = PATTERNS_README.read_text(encoding="utf-8")
        for pattern_id in EXPECTED_PATTERNS:
            with self.subTest(pattern_id=pattern_id):
                self.assertRegex(
                    patterns,
                    rf"(?m)^\|\s*\[{re.escape(pattern_id)}\]",
                )
        draft_rows = re.findall(r"(?m)^\|\s*\[ARC-P\d+\]", patterns)
        self.assertEqual(len(draft_rows), 7)
        # Deepen shall not invent a new pattern identifier in ESAF-1200.
        body = text()
        invented = re.findall(r"ARC-P(?:1[7-9]\d|[2-9]\d{2})", body)
        self.assertEqual(invented, [])

    def test_deepen_does_not_claim_certification_or_compliance(self) -> None:
        body = text().casefold()
        self.assertIn("does not establish", body)
        self.assertIn("certification", body)
        for phrase in (
            "esaf certification scheme",
            "certified against esaf-1200",
            "accredited certification body shall",
            "establishes compliance with",
            "equivalence to external frameworks",
            "assures fitness for purpose",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, body)

    def test_architectures_readme_syncs_version_and_foundation(self) -> None:
        readme = ARCHITECTURES_README.read_text(encoding="utf-8").replace("\\", "/")
        for needle in (
            "ESAF-1200.md",
            "0.4.1",
            "Working Draft",
            "PATTERN_SELECTION.md",
            "TRUST_ZONES.md",
            "patterns/README.md",
            "PRINCIPLES.md",
            "ARCHITECTURE_TEMPLATE.md",
            "overlays/README.md",
            "decisions/README.md",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, readme)


if __name__ == "__main__":
    unittest.main()
