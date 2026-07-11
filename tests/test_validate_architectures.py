from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_architectures import validate


REQUIRED_TEMPLATE_HEADINGS = (
    "Metadata",
    "Purpose",
    "Problem statement",
    "Intended outcomes",
    "Non-goals",
    "Applicability",
    "Assumptions and prerequisites",
    "Prohibited uses",
    "Architecture views",
    "Actors and identities",
    "Data and instruction flows",
    "Trust boundaries",
    "Components and responsibilities",
    "Required controls",
    "Control points and overlays",
    "Architecture decisions and parameters",
    "Failure modes and abuse cases",
    "Fallback recovery and retirement",
    "Evidence and assessment",
    "Variants and alternatives",
    "Anti-patterns",
    "Related patterns",
    "Change history",
)

PATTERNS = (
    ("ARC-P100", "Enterprise AI platform and gateway"),
    ("ARC-P110", "Enterprise copilot"),
    ("ARC-P120", "Retrieval-augmented generation"),
    ("ARC-P130", "Agentic and multi-agent AI"),
    ("ARC-P140", "Private model deployment"),
    ("ARC-P150", "AI integration services"),
    ("ARC-P160", "AI observability"),
)


class ArchitectureValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def create_valid_foundation(self) -> None:
        self.write("controls/schema/control.schema.json", '{"properties":{"family":{"enum":["ARC","IAM"]}}}')
        linked_files = {
            "architectures/README.md": "# Reference Architecture\n\n[Standard](ESAF-1200.md)\n",
            "architectures/ESAF-1200.md": "# ESAF-1200\n\nArchitecture method using `ARC` and `IAM`.\n",
            "architectures/PRINCIPLES.md": "# Principles\n\nArchitecture principles using `ARC`.\n",
            "architectures/TRUST_ZONES.md": "# Trust Zones\n\nEight logical zones.\n",
            "architectures/PATTERN_SELECTION.md": "# Pattern Selection\n\nSelection and tailoring.\n",
            "architectures/overlays/README.md": "# Overlays\n\nOverlay method.\n",
            "architectures/decisions/README.md": "# Decisions\n\n[Template](ADR_TEMPLATE.md)\n",
            "architectures/decisions/ADR_TEMPLATE.md": "# Architecture Decision Record\n\nDecision record.\n",
        }
        for relative, content in linked_files.items():
            self.write(relative, content)
        template = ["# Architecture Pattern Template", ""]
        for heading in REQUIRED_TEMPLATE_HEADINGS:
            template.extend([f"## {heading}", "", "Required content.", ""])
        self.write("architectures/ARCHITECTURE_TEMPLATE.md", "\n".join(template))
        registry = ["# Pattern Registry", "", "| ID | Pattern | Status |", "|---|---|---|"]
        registry.extend(f"| {identifier} | {title} | Proposed |" for identifier, title in PATTERNS)
        self.write("architectures/patterns/README.md", "\n".join(registry) + "\n")

    def test_valid_foundation_has_no_errors(self) -> None:
        self.create_valid_foundation()

        self.assertEqual(validate(self.root), [])

    def test_missing_required_file_is_reported(self) -> None:
        self.create_valid_foundation()
        (self.root / "architectures/TRUST_ZONES.md").unlink()

        errors = validate(self.root)

        self.assertIn("architectures/TRUST_ZONES.md: required foundation file is missing", errors)

    def test_duplicate_reserved_pattern_is_reported(self) -> None:
        self.create_valid_foundation()
        registry = self.root / "architectures/patterns/README.md"
        registry.write_text(registry.read_text(encoding="utf-8") + "| ARC-P100 | Duplicate | Proposed |\n", encoding="utf-8")

        errors = validate(self.root)

        self.assertIn("architectures/patterns/README.md: ARC-P100 occurs 2 times; expected 1", errors)

    def test_missing_template_heading_is_reported(self) -> None:
        self.create_valid_foundation()
        template = self.root / "architectures/ARCHITECTURE_TEMPLATE.md"
        template.write_text(template.read_text(encoding="utf-8").replace("## Anti-patterns\n", ""), encoding="utf-8")

        errors = validate(self.root)

        self.assertIn("architectures/ARCHITECTURE_TEMPLATE.md: missing heading '## Anti-patterns'", errors)

    def test_broken_local_markdown_link_is_reported(self) -> None:
        self.create_valid_foundation()
        self.write("architectures/README.md", "# Reference Architecture\n\n[Missing](NOT-HERE.md)\n")

        errors = validate(self.root)

        self.assertIn("architectures/README.md: broken local link 'NOT-HERE.md'", errors)


if __name__ == "__main__":
    unittest.main()
