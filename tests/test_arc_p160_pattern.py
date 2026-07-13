from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN = ROOT / "architectures" / "patterns" / "ARC-P160.md"
REGISTRY = ROOT / "architectures" / "patterns" / "README.md"
TEMPLATE = ROOT / "architectures" / "ARCHITECTURE_TEMPLATE.md"
CATALOG = ROOT / "controls" / "catalog.json"
CONTROL = re.compile(r"`([A-Z]{3}-\d{3})`")

REQUIRED = {
    "API-110",
    "APP-100", "APP-110", "APP-120", "APP-130", "APP-140", "APP-150",
    "ARC-100", "ARC-110", "ARC-130", "ARC-140",
    "AUD-100", "AUD-110", "AUD-120", "AUD-130", "AUD-140",
    "CMP-100", "CMP-110",
    "DAT-100", "DAT-110", "DAT-120", "DAT-130",
    "GOV-130",
    "IAM-100", "IAM-110", "IAM-120", "IAM-130", "IAM-140", "IAM-150",
    "INF-140", "INF-150",
    "MOD-100", "MOD-120", "MOD-130",
    "MON-100", "MON-110", "MON-120", "MON-140", "MON-150",
    "OPS-100", "OPS-110", "OPS-120", "OPS-130", "OPS-140",
    "RSK-110", "RSK-120", "RSK-140",
}
INHERITED = {"ARC-120", "ARC-150", "OPS-150", "MOD-140"}
CONDITIONAL = {
    "MON-130",
    "DAT-140", "DAT-150", "DAT-160",
    "CMP-120", "CMP-130", "CMP-140",
    "MOD-110", "MOD-150",
    "API-140",
    "AGT-100", "AGT-110", "AGT-120", "AGT-130", "AGT-140", "AGT-150", "AGT-160",
}


def section(text: str, title: str) -> str:
    match = re.search(
        rf"^## {re.escape(title)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Missing section: {title}")
    return match.group(1)


def headings(path: Path, level: int) -> list[str]:
    prefix = "#" * level
    return re.findall(rf"^{prefix} (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)


def mermaid_blocks(text: str) -> list[str]:
    return re.findall(r"```mermaid\n(.*?)\n```", text, re.DOTALL)


def figure_mermaid_pairs(text: str) -> list[tuple[str, str]]:
    architecture = section(text, "Architecture views")
    return re.findall(
        r"^### Figure (\d+)\.[^\n]*\n\n```mermaid\n(.*?)\n```",
        architecture,
        re.MULTILINE | re.DOTALL,
    )


class ArcP160PatternTests(unittest.TestCase):
    def text(self) -> str:
        return PATTERN.read_text(encoding="utf-8")

    def assert_required_metadata_complete(self, text: str) -> None:
        for value in (
            "**Pattern ID:** ARC-P160",
            "**Status:** Draft",
            "**Version:** 0.1.0",
            "| Owner | Enterprise Architecture |",
            "| Required reviewers |",
            "| Approval date | Not approved (Draft) |",
            "| Review date |",
            "| Pillars | Protect AI, Utilize AI, Govern AI |",
            "| Lifecycle stages |",
            "| Capability tiers | Tier 0 through Tier 4 |",
            "| Deployment models |",
            "| Primary pattern role |",
            "| Supersedes | None |",
        ):
            with self.subTest(value=value):
                self.assertIn(value, text)

        metadata = section(text, "Metadata")
        rows = {
            field.strip(): value.strip()
            for field, value in re.findall(r"^\| ([^|]+) \|([^|]*)\|$", metadata, re.MULTILINE)
        }
        for field in (
            "Owner",
            "Required reviewers",
            "Approval date",
            "Review date",
            "Pillars",
            "Lifecycle stages",
            "Capability tiers",
            "Deployment models",
            "Primary pattern role",
            "Supersedes",
        ):
            self.assertTrue(rows.get(field), f"Metadata field is missing or empty: {field}")

    def assert_capture_modes_and_planes_preserved(self, text: str) -> None:
        expected_modes = (
            "Metadata only",
            "Derived signal",
            "Redacted excerpt",
            "Exceptional protected full content",
        )
        flow = section(text, "Data and instruction flows")
        capture_list = re.search(
            r"^Capture modes are:\s*$\n\n((?:^\d+\. \*\*.+$\n?)+)",
            flow,
            re.MULTILINE,
        )
        self.assertIsNotNone(capture_list)
        actual_modes = tuple(
            re.findall(r"^\d+\. \*\*(.+?):\*\*", capture_list.group(1), re.MULTILINE)
        )
        self.assertEqual(expected_modes, actual_modes)

        lower = text.lower()
        for mode in expected_modes:
            self.assertIn(mode.lower(), lower)

        expected_planes = (
            "1 governance and configuration",
            "2 signal collection",
            "3 protected evidence",
            "4 evaluation and ground truth",
            "5 detection and response",
            "6 analytics, service, and cost",
        )
        pairs = dict(figure_mermaid_pairs(text))
        self.assertIn("2", pairs)
        actual_planes = tuple(
            label.lower()
            for label in re.findall(r'^\s+\w+\["(\d+ [^":]+):', pairs["2"], re.MULTILINE)
        )
        self.assertEqual(expected_planes, actual_planes)

        rendered_source = "\n".join(mermaid_blocks(text)).lower()
        for plane in expected_planes:
            self.assertIn(plane, rendered_source)

    def assert_figures_pair_with_mermaid_blocks(self, text: str) -> None:
        architecture = section(text, "Architecture views")
        expected = [str(number) for number in range(1, 5)]
        self.assertEqual(
            expected,
            re.findall(r"^### Figure (\d+)\.", architecture, re.MULTILINE),
        )
        self.assertEqual(expected, [number for number, _ in figure_mermaid_pairs(text)])
        self.assertEqual(4, len(mermaid_blocks(architecture)))

    def test_registry_has_one_exact_arc_p160_draft_row(self) -> None:
        registry = REGISTRY.read_text(encoding="utf-8")
        expected = "| [ARC-P160](ARC-P160.md) | AI observability | Draft |"
        self.assertEqual(1, registry.count(expected))
        self.assertEqual(1, len(re.findall(r"^\| (?:\[)?ARC-P160", registry, re.MULTILINE)))

    def test_required_metadata_is_complete(self) -> None:
        self.assert_required_metadata_complete(self.text())

    def test_metadata_completeness_rejects_empty_required_value(self) -> None:
        mutant = re.sub(
            r"^\| Required reviewers \|.*$",
            "| Required reviewers | |",
            self.text(),
            count=1,
            flags=re.MULTILINE,
        )
        with self.assertRaises(AssertionError):
            self.assert_required_metadata_complete(mutant)

    def test_template_headings_are_unique_and_ordered(self) -> None:
        expected = headings(TEMPLATE, 2)
        actual = headings(PATTERN, 2)
        self.assertEqual(expected, actual)
        self.assertEqual(len(actual), len(set(actual)))

    def test_pattern_has_no_drafting_markers(self) -> None:
        text = self.text().lower()
        markers = ("t" + "bd", "t" + "odo", "place" + "holder", "lorem" + " ipsum")
        for marker in markers:
            self.assertNotIn(marker, text)

    def test_control_allocation_is_exact_disjoint_and_resolved(self) -> None:
        allocation = section(self.text(), "Required controls")
        required_table, allocation_notes = allocation.split("\n\n", 1)
        inherited_text, conditional_text = allocation_notes.split("Conditional controls are", 1)
        conditional_text = conditional_text.split("Catalog `owner_role`", 1)[0]

        required = set(CONTROL.findall(required_table))
        inherited = set(CONTROL.findall(inherited_text))
        conditional = set(CONTROL.findall(conditional_text))
        catalog = {
            item["id"]
            for item in json.loads(CATALOG.read_text(encoding="utf-8"))["controls"]
        }

        self.assertEqual((47, 4, 17), (len(required), len(inherited), len(conditional)))
        self.assertEqual(REQUIRED, required)
        self.assertEqual(INHERITED, inherited)
        self.assertEqual(CONDITIONAL, conditional)
        self.assertFalse(required & inherited)
        self.assertFalse(required & conditional)
        self.assertFalse(inherited & conditional)
        self.assertEqual(68, len(required | inherited | conditional))
        self.assertTrue((required | inherited | conditional) <= catalog)
        self.assertEqual(91, len(catalog))

    def test_architecture_structure_and_relationships_are_complete(self) -> None:
        text = self.text()
        lower = text.lower()
        ids = re.findall(r"^\| (CP\d+) \|", text, re.MULTILINE)
        self.assertEqual([f"CP{number}" for number in range(1, 16)], ids)
        self.assertIn("implementation and evidence owners", lower)

        for pattern_id in ("ARC-P100", "ARC-P110", "ARC-P120", "ARC-P130", "ARC-P140", "ARC-P150"):
            self.assertIn(f"`{pattern_id}`", section(text, "Related patterns"))

    def test_observability_preserves_enforcement_and_accountability_boundaries(self) -> None:
        text = self.text()
        for requirement in (
            "Source patterns remain responsible for their event semantics and preventive enforcement.",
            "Target systems remain authoritative for transaction state.",
            "Capability owners remain accountable for business outcomes.",
            "ARC-P160 produces evidence and assurance; it does not authorize access or action and does not transfer catalog accountability.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_assurance_independence_and_correlation_boundaries_are_explicit(self) -> None:
        text = self.text()
        lower = text.lower()
        for requirement in (
            "Externally supplied correlation identifiers are untrusted inputs.",
            "They never authorize access or action.",
            "Monitored workloads cannot administer authoritative evidence or assurance verdicts.",
            "cannot select, suppress, rewrite or delete authoritative evidence or verdicts",
            "ordinary administrative privilege does not imply cross-tenant evidence access",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement.lower(), lower)

    def test_sensitive_evidence_and_sampling_rules_are_explicit(self) -> None:
        text = self.text()
        for requirement in (
            "Sampling cannot omit denials, incidents, gaps, material decisions, consequential outcomes, or required Tier 3 and Tier 4 outcome records.",
            "Alert payloads reference protected evidence rather than copying sensitive source content.",
            "Alerts, cases, tickets, email, and chat shall not duplicate raw or sensitive source content.",
            "Derived signals, including embeddings, stable hashes and rare features, are classified and tested for re-identification and linkability.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_tenant_provider_and_ground_truth_boundaries_are_explicit(self) -> None:
        text = self.text().lower()
        for requirement in (
            "tenant identity shall be bound at the source and independently validated at ingestion",
            "cross-tenant support or break-glass access requires dual authorization",
            "provider evidence remains externally asserted unless independently corroborated",
            "the affected tier, action, or provider use is prohibited rather than represented as observable",
            "operational dashboards and aggregates remain traceable conveniences, never authoritative evidence",
            "model self-evaluation as authoritative evidence",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_capture_modes_and_six_logical_planes_are_preserved(self) -> None:
        self.assert_capture_modes_and_planes_preserved(self.text())

    def test_capture_mode_and_logical_plane_exactness_rejects_extras(self) -> None:
        extra_mode = self.text().replace(
            "4. **Exceptional protected full content:** segregated content-evidence vault capture under explicit authorization.",
            "4. **Exceptional protected full content:** segregated content-evidence vault capture under explicit authorization.\n"
            "5. **Unapproved extra mode:** synthetic.",
            1,
        )
        extra_plane = self.text().replace(
            '  A["6 Analytics, service, and cost: reliability, capacity, value"]',
            '  A["6 Analytics, service, and cost: reliability, capacity, value"]\n'
            '  X["7 Unapproved extra plane: synthetic"]',
            1,
        )
        for name, mutant in (("extra mode", extra_mode), ("extra plane", extra_plane)):
            with self.subTest(mutant=name):
                with self.assertRaises(AssertionError):
                    self.assert_capture_modes_and_planes_preserved(mutant)

    def test_four_numbered_figures_pair_with_mermaid_blocks(self) -> None:
        self.assert_figures_pair_with_mermaid_blocks(self.text())

    def test_figure_mermaid_pairing_rejects_misalignment(self) -> None:
        mutant = self.text().replace(
            "### Figure 1. Context view\n\n```mermaid",
            "### Figure 1. Context view\n\nDisplaced block.\n\n```mermaid",
            1,
        )
        with self.assertRaises(AssertionError):
            self.assert_figures_pair_with_mermaid_blocks(mutant)

    def test_mermaid_source_avoids_known_sequence_hazards(self) -> None:
        diagrams = mermaid_blocks(self.text())
        sequence_diagrams = [diagram for diagram in diagrams if diagram.startswith("sequenceDiagram")]
        self.assertGreater(len(sequence_diagrams), 0)
        for diagram in sequence_diagrams:
            for line in diagram.splitlines():
                if ":" in line:
                    with self.subTest(line=line):
                        self.assertNotIn(";", line.split(":", 1)[1])


if __name__ == "__main__":
    unittest.main()
