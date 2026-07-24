from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "profiles" / "ESAF-1800.md"

REQUIRED_HEADINGS = (
    "Purpose and scope",
    "Profile identity and lifecycle",
    "Applicability and system boundary",
    "Control selections",
    "Additional risks and overlays",
    "Evidence and assessment",
    "External references",
    "Traceability and validation",
    "Non-claim boundaries",
)
SELECTION_STATUSES = (
    "required",
    "conditional",
    "recommended",
    "not_selected",
)


def text() -> str:
    return STANDARD.read_text(encoding="utf-8")


class ProfileFoundationTests(unittest.TestCase):
    def test_normative_contract_exists_with_required_sections(self) -> None:
        document = text()
        for heading in REQUIRED_HEADINGS:
            with self.subTest(heading=heading):
                self.assertRegex(document, rf"(?m)^## {re.escape(heading)}$")

    def test_control_selection_vocabulary_is_closed(self) -> None:
        document = text()
        selection_section = document.split("## Control selections", 1)[1].split(
            "\n## ", 1
        )[0]
        for status in SELECTION_STATUSES:
            with self.subTest(status=status):
                self.assertIn(f"`{status}`", selection_section)

    def test_non_selection_preserves_control_applicability(self) -> None:
        self.assertIn(
            "does not declare the underlying ESAF control inapplicable", text()
        )

    def test_assessment_reuses_esaf_1500(self) -> None:
        self.assertIn("[ESAF-1500](../assessment/ESAF-1500.md)", text())

    def test_profiles_cannot_replace_maturity_or_weaken_controls(self) -> None:
        document = text()
        self.assertIn(
            "shall not define a profile-local replacement maturity scale", document
        )
        self.assertIn("shall not alter or weaken a core control", document)


if __name__ == "__main__":
    unittest.main()
