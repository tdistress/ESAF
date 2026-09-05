from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "templates"
TEMPLATE_FILES = (
    "risk-assessment.md",
    "exception-record.md",
    "decision-record.md",
    "retirement-record.md",
)
SHALL_RE = re.compile(r"(?i)\bshall\b")


class GovernanceTemplatesStarterTests(unittest.TestCase):
    def test_templates_readme_is_draft_and_indexes_starters(self) -> None:
        readme = (TEMPLATE_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertRegex(readme, r"(?im)\bDraft\b")
        self.assertRegex(readme, r"(?im)certification")
        self.assertRegex(readme, r"(?im)compliance")
        for name in TEMPLATE_FILES:
            with self.subTest(name=name):
                self.assertIn(name, readme)

    def test_template_files_are_non_normative_draft_starters(self) -> None:
        for name in TEMPLATE_FILES:
            path = TEMPLATE_ROOT / name
            with self.subTest(name=name):
                self.assertTrue(path.is_file(), msg=f"missing {path}")
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text, r"(?im)\bDraft\b")
                self.assertRegex(text, r"(?im)non-normative|informative")
                self.assertRegex(text, r"(?im)certification")
                self.assertIsNone(
                    SHALL_RE.search(text),
                    msg=f"{name} introduces normative shall language",
                )

    def test_governance_and_implementation_indexes_link_templates(self) -> None:
        governance_readme = (ROOT / "governance" / "README.md").read_text(
            encoding="utf-8"
        )
        implementation_readme = (ROOT / "implementation" / "README.md").read_text(
            encoding="utf-8"
        )
        governance_manual = (ROOT / "governance" / "ESAF-1300.md").read_text(
            encoding="utf-8"
        )
        implementation_guide = (ROOT / "implementation" / "ESAF-1400.md").read_text(
            encoding="utf-8"
        )
        for document, needle in (
            (governance_readme, "../templates/"),
            (implementation_readme, "../templates/"),
            (governance_manual, "../templates/"),
            (implementation_guide, "../templates/"),
        ):
            with self.subTest(needle=needle, sample=document[:32]):
                self.assertIn(needle, document)


if __name__ == "__main__":
    unittest.main()
