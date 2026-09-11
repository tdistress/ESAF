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

    def test_template_deepen_filled_instances_exist(self) -> None:
        readme = (TEMPLATE_ROOT / "README.md").read_text(encoding="utf-8")
        example_root = TEMPLATE_ROOT / "examples"
        filled = {
            "risk": example_root / "risk-assessment.example.md",
            "exception": example_root / "exception-record.example.md",
            "decision": example_root / "decision-record.example.md",
            "retirement": example_root / "retirement-record.example.md",
        }
        self.assertRegex(readme, r"(?im)\bDraft deepen\b")
        self.assertIn("#127", readme)
        for template_name in TEMPLATE_FILES:
            with self.subTest(template=template_name):
                text = (TEMPLATE_ROOT / template_name).read_text(encoding="utf-8")
                self.assertRegex(text, r"(?im)\bDraft deepen\b")
        for class_name, path in filled.items():
            with self.subTest(filled=class_name):
                self.assertTrue(path.is_file(), msg=f"missing {path}")
                self.assertIn(path.name, readme)
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text, r"(?im)\bDraft deepen\b")
                self.assertRegex(text, r"(?im)fictional")
                self.assertRegex(text, r"(?im)certification")
                self.assertRegex(text, r"(?im)compliance")
                self.assertIsNone(
                    SHALL_RE.search(text),
                    msg=f"{path.name} introduces normative shall language",
                )
                # Filled tables should not leave blank entry cells in the first
                # data row after each section header table.
                self.assertNotRegex(
                    text,
                    r"(?m)^\| [^|]+\| \|$",
                    msg=f"{path.name} still has blank template entry cells",
                )
        for document_path, needle in (
            (ROOT / "governance" / "ESAF-1300.md", "templates/examples/risk-assessment.example.md"),
            (ROOT / "implementation" / "ESAF-1400.md", "templates/examples/risk-assessment.example.md"),
            (ROOT / "governance" / "README.md", "templates/examples/risk-assessment.example.md"),
            (ROOT / "implementation" / "README.md", "templates/examples/risk-assessment.example.md"),
        ):
            with self.subTest(document=str(document_path)):
                text = document_path.read_text(encoding="utf-8")
                self.assertIn(needle, text)

    def test_template_second_deepen_governance_thread_exists(self) -> None:
        readme = (TEMPLATE_ROOT / "README.md").read_text(encoding="utf-8")
        thread = TEMPLATE_ROOT / "examples" / "governance-thread.example.md"
        self.assertTrue(thread.is_file(), msg=f"missing {thread}")
        self.assertIn("governance-thread.example.md", readme)
        self.assertIn("#183", readme)
        text = thread.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?im)\bDraft deepen\b")
        self.assertRegex(text, r"(?im)fictional")
        self.assertRegex(text, r"(?im)certification")
        self.assertRegex(text, r"(?im)compliance")
        self.assertIsNone(
            SHALL_RE.search(text),
            msg="governance-thread.example.md introduces normative shall language",
        )
        self.assertIn("decision-record.example.md", text)
        self.assertIn("exception-record.example.md", text)
        self.assertIn("engagement2-vignette.example.md", text)


if __name__ == "__main__":
    unittest.main()
