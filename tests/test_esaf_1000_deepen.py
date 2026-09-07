"""Contracts for the bounded ESAF-1000 Working Draft deepen (Issue #144)."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ESAF_1000 = ROOT / "framework" / "ESAF-1000.md"
FRAMEWORK_README = ROOT / "framework" / "README.md"
GLOSSARY = ROOT / "GLOSSARY.md"

LIFECYCLE_STAGES = (
    "Strategy",
    "Ideation",
    "Business Case",
    "Risk Classification",
    "Architecture",
    "Data Readiness",
    "Model Selection",
    "Development",
    "Validation",
    "Approval",
    "Deployment",
    "Operations",
    "Monitoring",
    "Continuous Improvement",
    "Retirement",
)

PILLARS = ("Protect AI", "Utilize AI", "Govern AI")

COMPANION_LINKS = (
    ("ESAF-1100", "../controls/ESAF-1100.md"),
    ("ESAF-1200", "../architectures/ESAF-1200.md"),
    ("ESAF-1300", "../governance/ESAF-1300.md"),
    ("ESAF-1400", "../implementation/ESAF-1400.md"),
    ("ESAF-1500", "../assessment/ESAF-1500.md"),
    ("ESAF-1600", "../crosswalks/ESAF-1600.md"),
    ("ESAF-1700", "../data-model/ESAF-1700.md"),
    ("ESAF-1800", "../profiles/ESAF-1800.md"),
)

TOOLKIT_LINKS = (
    "../assessment/README.md",
    "../assessment/workbook/README.md",
    "../assessment/evidence-catalog/README.md",
    "../assessment/audit-checklist/README.md",
    "../templates/README.md",
)


def text() -> str:
    return ESAF_1000.read_text(encoding="utf-8")


class Esaf1000DeepenContracts(unittest.TestCase):
    def test_document_is_working_draft_version_0_2_1(self) -> None:
        body = text()
        self.assertRegex(
            body,
            r"(?m)^\|\s*Version\s*\|\s*0\.2\.1\s*\|",
        )
        self.assertRegex(
            body,
            r"(?m)^\|\s*Status\s*\|\s*Working Draft\s*\|",
        )

    def test_revision_history_records_the_deepen(self) -> None:
        body = text()
        history = body.split("## Revision history", 1)[1].split("\n## ", 1)[0]
        self.assertIn("0.2.1", history)
        self.assertTrue(
            contains_normalized_phrase(history, "Working Draft"),
        )
        self.assertTrue(
            contains_normalized_phrase(history, "cross-link")
            or contains_normalized_phrase(history, "cross link")
            or contains_normalized_phrase(history, "companion"),
        )
        self.assertTrue(
            contains_normalized_phrase(history, "toolkit")
            or contains_normalized_phrase(history, "terminology")
            or contains_normalized_phrase(history, "glossary"),
        )

    def test_companion_publications_are_fully_linked(self) -> None:
        body = text()
        for label, href in COMPANION_LINKS:
            with self.subTest(label=label):
                self.assertRegex(
                    body,
                    rf"\[[^\]]*{re.escape(label)}[^\]]*\]\({re.escape(href)}\)",
                )

    def test_toolkit_index_surfaces_are_linked(self) -> None:
        body = text().replace("\\", "/")
        for href in TOOLKIT_LINKS:
            with self.subTest(href=href):
                self.assertIn(href, body)

    def test_terms_section_links_glossary_and_aligns_key_definitions(self) -> None:
        body = text()
        self.assertRegex(
            body,
            r"\[[^\]]*GLOSSARY[^\]]*\]\(\.\./GLOSSARY\.md\)",
        )
        terms = body.split("## 3. Terms and definitions", 1)[1].split(
            "\n## 4. ", 1
        )[0]
        glossary = GLOSSARY.read_text(encoding="utf-8")
        for term in (
            "Accountable Owner",
            "Human Oversight",
            "Residual Risk",
            "AI Management System",
            "AI Bill of Materials",
            "Model Registry",
        ):
            with self.subTest(term=term):
                self.assertTrue(
                    contains_normalized_phrase(terms, term)
                    or contains_normalized_phrase(terms, term.replace(" ", "")),
                    msg=f"ESAF-1000 terms shall reference {term}",
                )
                self.assertTrue(
                    contains_normalized_phrase(glossary, term),
                    msg=f"GLOSSARY.md shall define {term}",
                )
        # Material Change uses glossary-aligned "obligations" wording.
        self.assertIn("obligations", terms.lower())
        self.assertRegex(
            terms,
            r"(?is)material change.*?obligations",
        )

    def test_three_pillars_and_lifecycle_stages_are_preserved(self) -> None:
        body = text()
        for pillar in PILLARS:
            with self.subTest(pillar=pillar):
                self.assertIn(f"**{pillar}**", body)
                self.assertRegex(body, rf"(?m)^## \d+\. {re.escape(pillar)}$")
        lifecycle = body.split("## 9. Enterprise AI lifecycle", 1)[1].split(
            "\n## 10. ", 1
        )[0]
        for stage in LIFECYCLE_STAGES:
            with self.subTest(stage=stage):
                self.assertIn(f"| {stage} |", lifecycle)

    def test_deepen_does_not_invent_certification_or_new_lifecycle_stages(self) -> None:
        body = text().lower()
        # Preserve existing nonclaim language; forbid inventing a scheme.
        self.assertIn("shall not imply independent certification", body)
        forbidden = (
            "esaf certification scheme",
            "certified against esaf-1000",
            "accredited certification body shall",
            "new lifecycle stage",
            "fourth pillar",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, body)

    def test_framework_readme_points_to_companions_and_toolkit(self) -> None:
        readme = FRAMEWORK_README.read_text(encoding="utf-8").replace("\\", "/")
        for needle in (
            "ESAF-1100",
            "ESAF-1200",
            "ESAF-1300",
            "ESAF-1400",
            "ESAF-1500",
            "ESAF-1600",
            "ESAF-1700",
            "ESAF-1800",
            "../assessment/README.md",
            "../templates/README.md",
            "Working Draft",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, readme)

    def test_appendix_a_links_available_templates(self) -> None:
        appendix = text().split("## Appendix A. Required governance artifacts", 1)[
            1
        ].split("\n## Appendix B.", 1)[0]
        normalized = appendix.replace("\\", "/")
        for href in (
            "../templates/risk-assessment.md",
            "../templates/exception-record.md",
            "../templates/decision-record.md",
            "../templates/retirement-record.md",
            "../templates/README.md",
        ):
            with self.subTest(href=href):
                self.assertIn(href, normalized)


def contains_normalized_phrase(haystack: str, needle: str) -> bool:
    compact = re.sub(r"\s+", " ", haystack).casefold()
    return re.sub(r"\s+", " ", needle).casefold() in compact


if __name__ == "__main__":
    unittest.main()
