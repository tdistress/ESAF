from __future__ import annotations

import re
import unittest
from pathlib import Path

from tools.crosswalks.io import parse_front_matter


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md"
TEMPLATES = ROOT / "crosswalks/reviews/templates"
SET_IDS = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
)
SNAPSHOTS = (
    ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0",
    ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0",
    ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0",
)


class MappingReviewProtocolTests(unittest.TestCase):
    def test_protocol_defines_roles_exact_sha_and_stop_boundary(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        for phrase in (
            "Specification and inventory review",
            "Security and overclaiming review",
            "full 40-character Git commit SHA",
            "authorized source access",
            "different from the mapper",
            "Critical",
            "Important",
            "remains `draft`",
            "AI-produced review",
        ):
            self.assertIn(phrase, text)
        scope = text.split("## In-scope snapshots\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(
            tuple(re.findall(r"^- `([^`]+)`$", scope, flags=re.MULTILINE)),
            SET_IDS,
        )
        for population in (
            "Core, 116 provisions.",
            "Plus forward, 144 provisions.",
            "Plus reverse, 144 provisions.",
        ):
            self.assertIn(population, text)
        self.assertIn(
            "Every repository-sourced payload byte shall be read from either "
            "the exact candidate commit or an exact historical commit SHA "
            "pinned by candidate-commit metadata; working-tree bytes shall "
            "never be used.",
            text,
        )
        self.assertIn(
            "Generated metadata shall be deterministic from those inputs.",
            text,
        )

    def test_attestation_requires_identity_eligibility_and_nonclaims(self) -> None:
        text = (TEMPLATES / "REVIEWER_ATTESTATION.md").read_text(encoding="utf-8")
        for field in (
            "Reviewer identity",
            "Organization",
            "Verification locator",
            "Mapping-set identifier",
            "Candidate commit SHA",
            "Review role",
            "Scheme qualification",
            "ESAF or mapping qualification",
            "Authorized source access",
            "Independence from mapper",
            "Conflicts of interest",
            "certification",
            "equivalence",
            "Signature",
            "Date",
        ):
            self.assertIn(field, text)

    def test_review_worksheets_have_separate_scopes_and_findings(self) -> None:
        specification = (
            TEMPLATES / "SPECIFICATION_INVENTORY_REVIEW.md"
        ).read_text(encoding="utf-8")
        security = (
            TEMPLATES / "SECURITY_OVERCLAIMING_REVIEW.md"
        ).read_text(encoding="utf-8")
        for text in (specification, security):
            for field in (
                "Mapping-set identifier",
                "Candidate commit SHA",
                "Attestation locator",
                "Coverage",
                "Finding ID",
                "Affected record IDs",
                "Severity",
                "Evidence",
                "Required action",
                "Disposition",
                "Overall conclusion",
                "`pass`",
                "`pass_after_correction`",
                "`stop`",
            ):
                self.assertIn(field, text)
        self.assertIn("Provision population", specification)
        self.assertIn("Publication rights", specification)
        self.assertIn("no_direct_mapping", security)
        self.assertIn("prerequisite", security)
        self.assertIn("partially_supports", security)

    def test_preparation_does_not_transition_snapshots(self) -> None:
        for snapshot in SNAPSHOTS:
            set_metadata, _ = parse_front_matter(snapshot / "README.md")
            self.assertEqual(set_metadata["status"], "draft")
            self.assertNotIn("reviewer", set_metadata)
            records = [
                path for path in snapshot.glob("*.md")
                if path.name not in {"README.md", "PROVISION_INVENTORY.md"}
            ]
            for record in records:
                metadata, _ = parse_front_matter(record)
                self.assertEqual(metadata["status"], "draft")
                self.assertNotIn("reviewer", metadata)


if __name__ == "__main__":
    unittest.main()
