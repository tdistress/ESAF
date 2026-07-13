from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN = ROOT / "architectures" / "patterns" / "ARC-P150.md"
REGISTRY = ROOT / "architectures" / "patterns" / "README.md"
TEMPLATE = ROOT / "architectures" / "ARCHITECTURE_TEMPLATE.md"


def headings(path: Path, level: int) -> list[str]:
    prefix = "#" * level
    return re.findall(rf"^{prefix} (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)


class ArcP150PatternTests(unittest.TestCase):
    def text(self) -> str:
        return PATTERN.read_text(encoding="utf-8")

    def test_registry_links_only_arc_p150_as_draft(self) -> None:
        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("| [ARC-P150](ARC-P150.md) | AI integration services | Draft |", registry)
        self.assertNotIn("| ARC-P150 | AI integration services | Proposed |", registry)

    def test_required_metadata_is_complete(self) -> None:
        text = self.text()
        for value in (
            "**Pattern ID:** ARC-P150",
            "**Status:** Draft",
            "**Version:** 0.1.0",
            "| Owner | Enterprise Architecture |",
            "| Required reviewers |",
            "| Approval date | Not approved (Draft) |",
            "| Review date |",
            "| Pillars | Protect AI, Utilize AI, Govern AI |",
            "| Lifecycle stages |",
            "| Capability tiers |",
            "| Deployment models |",
            "| Primary pattern role |",
            "| Supersedes | None |",
        ):
            self.assertIn(value, text)

    def test_template_headings_are_unique_and_ordered(self) -> None:
        expected = headings(TEMPLATE, 2)
        actual = headings(PATTERN, 2)
        self.assertEqual(expected, actual)

    def test_pattern_has_no_drafting_markers(self) -> None:
        text = self.text().lower()
        markers = ("t" + "bd", "t" + "odo", "place" + "holder", "lorem" + " ipsum")
        for marker in markers:
            self.assertNotIn(marker, text)


if __name__ == "__main__":
    unittest.main()
