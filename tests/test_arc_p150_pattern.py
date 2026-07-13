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

    def test_seven_numbered_mermaid_views_cover_required_components(self) -> None:
        text = self.text()
        self.assertEqual([str(number) for number in range(1, 8)], re.findall(r"^### Figure (\d+)\.", text, re.MULTILINE))
        diagrams = re.findall(r"```mermaid\n(.*?)\n```", text, re.DOTALL)
        self.assertEqual(7, len(diagrams))
        rendered_source = "\n".join(diagrams).lower()
        for label in (
            "shared control plane",
            "global bootstrap",
            "execution cell",
            "policy-enforcement point",
            "contract validator",
            "durable state",
            "output validator",
            "administration",
            "evidence export",
            "arc-p100",
            "arc-p120",
            "arc-p130",
            "arc-p140",
            "arc-p160",
        ):
            self.assertIn(label, rendered_source)

    def test_six_plane_outcomes_are_explicit(self) -> None:
        text = self.text().lower()
        for plane in (
            "governance and contract plane",
            "admission and policy plane",
            "execution and adapter plane",
            "durable delivery and state plane",
            "output and delivery plane",
            "operations, administration, and evidence plane",
        ):
            self.assertIn(plane, text)

    def test_all_interaction_modes_and_state_authorities_are_explicit(self) -> None:
        text = self.text().lower()
        for mode in (
            "synchronous request and response",
            "asynchronous jobs and queues",
            "streaming",
            "batch and file processing",
            "events and subscriptions",
            "callbacks and webhooks",
        ):
            self.assertIn(mode, text)
        for state in (
            "transport delivery",
            "service execution",
            "result delivery",
            "target transaction",
            "business outcome",
        ):
            self.assertIn(state, text)

    def test_durable_and_authorization_invariants_are_explicit(self) -> None:
        text = self.text().lower()
        for requirement in (
            "at-least-once",
            "unknown outcome",
            "idempotency",
            "bounded authorization lease",
            "current authorization",
            "authoritative reconciliation",
            "semantic map",
            "granular event permissions",
            "registered internal enterprise destinations",
        ):
            self.assertIn(requirement, text)

    def test_trust_degraded_operation_and_failure_treatment_are_explicit(self) -> None:
        text = self.text().lower()
        for requirement in (
            "configuration-signing trust",
            "callback-signing trust",
            "trusted time",
            "anti-rollback",
            "maximum isolation window",
            "more restrictive state",
            "out-of-band",
            "failure-and-abuse treatment record",
            "affected boundary and state machines",
            "reconciliation source",
            "tier applicability",
            "residual-access",
        ):
            self.assertIn(requirement, text)
        for requirement in (
            "non-consequential inference or retrieval",
            "data failure",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)


if __name__ == "__main__":
    unittest.main()
