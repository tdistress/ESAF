from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN = ROOT / "architectures" / "patterns" / "ARC-P150.md"
REGISTRY = ROOT / "architectures" / "patterns" / "README.md"
TEMPLATE = ROOT / "architectures" / "ARCHITECTURE_TEMPLATE.md"
CATALOG = ROOT / "controls" / "catalog.json"
CONTROL = re.compile(r"`([A-Z]{3}-\d{3})`")


def subsection(text: str, title: str) -> str:
    match = re.search(rf"^### {re.escape(title)}\s*$\n(.*?)(?=^### |^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"Missing subsection: {title}")
    return match.group(1)


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

    def test_control_partition_matches_catalog_exactly(self) -> None:
        text = self.text()
        required = set(CONTROL.findall(subsection(text, "Required catalog controls")))
        inherited = set(CONTROL.findall(subsection(text, "Inherited and verified catalog controls")))
        conditional = set(CONTROL.findall(subsection(text, "Conditional catalog controls")))
        catalog = {item["id"] for item in json.loads(CATALOG.read_text(encoding="utf-8"))["controls"]}
        self.assertEqual((46, 26, 19), (len(required), len(inherited), len(conditional)))
        self.assertFalse(required & inherited)
        self.assertFalse(required & conditional)
        self.assertFalse(inherited & conditional)
        self.assertEqual(catalog, required | inherited | conditional)

    def test_control_points_are_exact_and_singly_accountable(self) -> None:
        text = self.text()
        ids = re.findall(r"^\| (CP\d+) \|", text, re.MULTILINE)
        self.assertEqual([f"CP{number}" for number in range(1, 16)], ids)
        self.assertIn("exactly one accountable owner", text.lower())

    def test_design_coverage_and_variants_are_complete(self) -> None:
        text = self.text().lower()
        for coverage in ("| 1-5 |", "| 6-7 |", "| 8-9 |", "| 10-14 |", "| 15-17 |", "| 18-20 |", "| 21-24 |"):
            self.assertIn(coverage, text)
        for variant in (
            "central multi-protocol hub",
            "durable workflow and event backbone",
            "regional or sovereign cells",
            "high-assurance dedicated cell",
            "edge or intermittently connected cell",
            "thin synchronous service",
            "external managed integration service",
        ):
            self.assertIn(variant, text)

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

    def test_sequence_diagram_messages_avoid_mermaid_statement_delimiters(self) -> None:
        diagrams = re.findall(r"```mermaid\n(.*?)\n```", self.text(), re.DOTALL)
        sequence_diagrams = [diagram for diagram in diagrams if diagram.startswith("sequenceDiagram")]
        self.assertGreater(len(sequence_diagrams), 0)
        for diagram in sequence_diagrams:
            for line in diagram.splitlines():
                if ":" in line:
                    with self.subTest(line=line):
                        self.assertNotIn(";", line.split(":", 1)[1])

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

    def test_contract_adapter_and_dependency_lifecycle_records_are_complete(self) -> None:
        text = self.text()
        for requirement in (
            "Services define owners, consumers, operations, side effects, interaction modes, schemas, examples, canonicalization, classifications, dependencies, providers, targets, limits, SLOs, support dates, compatibility, deprecation, migration, suspension, and retirement.",
            "Breaking and non-breaking change rules are explicit and tested in both producer and consumer directions.",
            "Unknown fields, version fallback, schema downgrade, content-type change, SDK or connector behavior change, and provider response drift cannot be accepted silently.",
            "Signed configuration, staged rollout, rollback, consumer notification, compatibility windows, and emergency blocking are required.",
            "Adapters and dependencies have approved identity, source, version, integrity, vulnerability, license, support, configuration, credential, endpoint, serialization, logging, retry, and retirement records.",
            "A connector or SDK update that changes endpoints, retention, training use, residency, authentication, serialization, retry, logging, output, or error behavior triggers review and compatibility testing.",
            "Service publication requires owner, purpose, consumers, operations, protocol modes, schemas, data, dependencies, providers and targets, limits, SLOs, evidence, compatibility, support, recovery, and retirement approval.",
            "Material change triggers architecture, risk, security, privacy, legal, supplier, and operational review as applicable.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_material_effect_outputs_and_errors_use_independent_controls(self) -> None:
        text = self.text()
        for requirement in (
            "When AI-selected output is used to invoke, execute, persist, route, or otherwise determine material effect through an endpoint, method, tool, query, command, file path, callback URL, credential reference, or business object, it requires independent allowlisting, authorization, validation, and the applicable ARC-P130 control.",
            "Errors do not disclose secrets, internal topology, provider configuration, job existence, tenant metadata, inaccessible objects, or sensitive model diagnostics.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_capacity_and_cascading_failure_controls_are_complete(self) -> None:
        text = self.text()
        for requirement in (
            "Capacity controls cover request and item size, tokens, sequence, concurrent requests, connections, stream buffers, queue depth, batch size, fan-out, retry budgets, callback backoff, worker capacity, result retention, cost, and downstream rate.",
            "Circuit breakers, admission control, fair scheduling, per-tenant quotas, backpressure, load shedding, and dependency isolation prevent retry storms and cascading failure.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_approved_editorial_invariants_are_exact(self) -> None:
        text = self.text()
        for requirement in (
            "Contracts define gap detection, wait, skip, quarantine, backfill, and reconciliation behavior.",
            "Duplicate, replayed, out-of-order, late, conflicting, expired, and poison events are detected and dispositioned.",
            "deadline or explicit no-deadline prohibition",
            "| 0.1.0 | 0.4-alpha | 2026-07-12 | Initial draft |",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)
        self.assertNotIn("deadline (or an explicit prohibition on no deadline)", text)
        self.assertNotIn("| 0.1.0 | 0.4-alpha | 2026-07-11 | Initial draft |", text)


if __name__ == "__main__":
    unittest.main()
