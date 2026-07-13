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

    def assert_control_points_complete(self, text: str) -> None:
        control_points = section(text, "Control points and overlays")
        table_lines = [
            line for line in control_points.splitlines() if line.startswith("|")
        ]
        self.assertGreaterEqual(len(table_lines), 2)
        self.assertEqual(
            [
                "CP",
                "Control point",
                "Required outcome",
                "Primary implementation and evidence owners",
            ],
            [cell.strip() for cell in table_lines[0].strip("|").split("|")],
        )
        self.assertTrue(all(re.fullmatch(r"[-: ]+", cell) for cell in table_lines[1].strip("|").split("|")))

        rows = [
            [cell.strip() for cell in line.strip("|").split("|")]
            for line in table_lines[2:]
        ]
        self.assertEqual(15, len(rows))
        self.assertTrue(all(len(row) == 4 for row in rows))
        self.assertEqual([f"CP{number}" for number in range(1, 16)], [row[0] for row in rows])
        for row in rows:
            self.assertTrue(row[1], f"{row[0]} has no control-point name")
            self.assertTrue(row[2], f"{row[0]} has no required outcome")
            self.assertTrue(row[3], f"{row[0]} has no implementation/evidence owner")

    def assert_related_pattern_evidence_relationships(self, text: str) -> None:
        related = section(text, "Related patterns")
        relationships = {
            "ARC-P100": "supplies shared gateway, model, provider, policy, identity, routing, and enforcement evidence.",
            "ARC-P110": "supplies human-facing copilot interaction, feedback, and oversight signals.",
            "ARC-P120": "supplies retrieval, context, grounding, citation, corpus, and semantic-memory evidence.",
            "ARC-P130": "supplies agent identity, lineage, delegation, tool, action, transaction, outcome, and containment evidence.",
            "ARC-P140": "supplies private model, runtime, infrastructure, adaptation, and deployment evidence.",
            "ARC-P150": "supplies reusable service, API, integration, target, and provider-boundary evidence.",
        }
        bullets = dict(re.findall(r"^- `([^`]+)` (.+)$", related, re.MULTILINE))
        self.assertEqual(relationships, bullets)

    def assert_sensitive_telemetry_contract_complete(self, text: str) -> None:
        intended_outcomes = section(text, "Intended outcomes").lower()
        assumptions = section(text, "Assumptions and prerequisites").lower()
        purpose = section(text, "Purpose").lower()
        flows = section(text, "Data and instruction flows").lower()
        components = section(text, "Components and responsibilities").lower()
        trust = section(text, "Trust boundaries").lower()
        evidence = section(text, "Evidence and assessment").lower()
        anti_patterns = section(text, "Anti-patterns").lower()

        sensitive_class_traces = {
            "prompts": ("logging only final prompts and responses", anti_patterns),
            "context": ("input, context, retrieval", purpose),
            "retrieval content": ("provider, retrieval, tool, target", flows),
            "outputs": ("model, output, tool, action", purpose),
            "tool data": ("retrieval, tool, target, policy", flows),
            "agent state": ("tier, lifecycle state", assumptions),
        }
        for sensitive_class, (trace, scoped_text) in sensitive_class_traces.items():
            self.assertIn(trace, scoped_text, f"Missing handling trace for {sensitive_class}")
        self.assertIn("principal, runtime, agent, model, provider", flows)
        self.assertIn("classified content references", flows)

        self.assertIn(
            "content minimization through four governed capture modes and tenant-scoped lifecycle controls",
            intended_outcomes,
        )
        self.assertIn("capture modes are:", flows)
        for capture_rule in (
            "metadata only:** the default when content is unnecessary",
            "redacted excerpt:** narrowly approved diagnostic content",
            "exceptional protected full content:** segregated content-evidence vault capture under explicit authorization",
        ):
            self.assertIn(capture_rule, flows)
        self.assertIn(
            "authenticate, attest, minimize, validate, tenant-bind",
            components,
        )
        self.assertIn("capture approvals", evidence)
        self.assertIn(
            "lifecycle tests for retention, deletion, residency, export, tickets and legal hold",
            evidence,
        )
        self.assertIn("embeddings, stable hashes and rare features", flows)
        self.assertIn(
            "purpose and tenant isolation, scoped or keyed transforms, retention, correction, deletion, and legal hold extend to derived stores",
            flows,
        )

        tenant_surfaces = (
            "encryption and key-management policy",
            "indexes, search, and query authorization",
            "dashboards and joins",
            "caches",
            "exports",
            "evaluation datasets and detector or evaluator training data",
            "alert routing",
            "incident attachments",
            "backup and restore",
            "tenant migration",
            "support or break-glass access",
            "timing",
            "high-cardinality",
        )
        self.assertIn("tenant identity shall be bound at the source and independently validated at ingestion", trust)
        for surface in tenant_surfaces:
            self.assertIn(surface, trust)

        for requirement in (
            "every external-provider integration shall maintain a governed gap register",
            "available and missing fields",
            "compensating enterprise-boundary evidence for each material gap",
            "provider evidence remains externally asserted unless independently corroborated",
            "the affected tier, action, or provider use is prohibited rather than represented as observable",
        ):
            self.assertIn(requirement, trust)
        self.assertIn("per-provider integration gap registers", evidence)

        self.assertIn(
            "treating application logs, dashboards, provider consoles, aggregates, transport success, or model self-evaluation as authoritative evidence",
            anti_patterns,
        )
        self.assertIn("ground-truth provenance", evidence)

    def assert_resilience_contract_complete(self, text: str) -> None:
        actors = section(text, "Actors and identities").lower()
        flows = section(text, "Data and instruction flows").lower()
        trust = section(text, "Trust boundaries").lower()
        components = section(text, "Components and responsibilities").lower()
        failures = section(text, "Failure modes and abuse cases").lower()
        evidence = section(text, "Evidence and assessment").lower()

        for requirement in (
            "spoofed source",
            "correlation collision",
            "replay",
            "schema drift",
            "telemetry injection",
            "clock regression",
            "late, duplicate, missing, or out-of-order event",
            "signing key compromise",
            "privileged evidence alteration",
            "alert poisoning",
            "provider export delay, incompleteness, changed semantics, or outage",
            "suppression abuse",
            "containment abuse",
        ):
            self.assertIn(requirement, failures)
        self.assertIn("clock quality and uncertainty", flows)
        self.assertIn("record conflicts", components)
        self.assertIn("schema and integrity validation", trust)
        self.assertIn("compromise response", actors)
        for requirement in (
            "routing and backpressure failure",
            "provider outage",
            "evidence integrity failure",
        ):
            self.assertIn(requirement, evidence)

        table_lines = [line for line in failures.splitlines() if line.startswith("|")]
        self.assertGreaterEqual(len(table_lines), 2)
        self.assertEqual(
            ["failure or abuse", "required treatment"],
            [cell.strip() for cell in table_lines[0].strip("|").split("|")],
        )
        treatment_rows = {
            cells[0]: cells[1]
            for cells in (
                [cell.strip() for cell in line.strip("|").split("|")]
                for line in table_lines[2:]
            )
            if len(cells) == 2
        }
        safe_treatments = {
            "spoofed source, correlation collision, replay, schema drift, or telemetry injection": (
                "reject or quarantine",
                "record gap",
                "regenerate untrusted identifiers",
                "investigate source and verifier state",
            ),
            "signing key compromise or privileged evidence alteration": (
                "revoke trust",
                "preserve custody",
                "verify against separate trust roots and timestamp anchors",
                "reassess affected evidence",
            ),
            "provider export delay, incompleteness, changed semantics, or outage": (
                "record the gap",
                "use enterprise boundary evidence",
                "prohibit use where assurance cannot be met",
                "execute portability or exit plans",
            ),
            "evidence, correlation, outcome, integrity, or assurance unavailable": (
                "stop tier 3 and tier 4 consequential commit and dependent activity",
                "do not report success",
            ),
        }
        for failure, requirements in safe_treatments.items():
            self.assertIn(failure, treatment_rows)
            for requirement in requirements:
                self.assertIn(requirement, treatment_rows[failure])

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
        self.assert_control_points_complete(self.text())
        self.assert_related_pattern_evidence_relationships(self.text())

    def test_control_point_completeness_rejects_blank_outcome_or_owner(self) -> None:
        text = self.text()
        mutants = {
            "blank outcome": re.sub(r"^(\| CP7 \|[^|]+\|)[^|]+(\|[^|]+\|)$", r"\1 \2", text, count=1, flags=re.MULTILINE),
            "blank owner": re.sub(r"^(\| CP7 \|[^|]+\|[^|]+\|)[^|]+\|$", r"\1 |", text, count=1, flags=re.MULTILINE),
        }
        for name, mutant in mutants.items():
            with self.subTest(mutant=name):
                with self.assertRaises(AssertionError):
                    self.assert_control_points_complete(mutant)

    def test_related_pattern_relationships_reject_semantic_erasure(self) -> None:
        mutant = self.text().replace(
            "`ARC-P120` supplies retrieval, context, grounding, citation, corpus, and semantic-memory evidence.",
            "`ARC-P120` is mentioned here.",
            1,
        )
        with self.assertRaises(AssertionError):
            self.assert_related_pattern_evidence_relationships(mutant)

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
        self.assert_sensitive_telemetry_contract_complete(self.text())

    def test_sensitive_telemetry_contract_rejects_polarity_inversion_and_removal(self) -> None:
        text = self.text()
        mutants = {
            "affirmative self-evaluation": text.replace(
                "Treating application logs, dashboards, provider consoles, aggregates, transport success, or model self-evaluation as authoritative evidence.",
                "Treating model self-evaluation as authoritative evidence is approved.",
                1,
            ),
            "removed lifecycle duty": text.replace(", correction, deletion, and legal hold extend to derived stores", " extend to derived stores", 1),
            "removed tenant surface": text.replace("; tenant migration;", ";", 1),
            "removed provider gap register": text.replace("a governed gap register", "an informal note", 1),
            "removed governed ground truth": text.replace("ground-truth provenance", "label provenance", 1),
        }
        for name, mutant in mutants.items():
            with self.subTest(mutant=name):
                with self.assertRaises(AssertionError):
                    self.assert_sensitive_telemetry_contract_complete(mutant)

    def test_sensitive_telemetry_contract_rejects_broken_governed_handling(self) -> None:
        text = self.text()
        mutants = {
            "all minimization removed": text.replace("minimization", "handling").replace("minimize", "process"),
            "governed capture relationship removed": text.replace(
                "Content minimization through four governed capture modes and tenant-scoped lifecycle controls.",
                "Sensitive classes are listed without a governed handling relationship.",
                1,
            ),
            "collector minimization removed": text.replace(
                "Authenticate, attest, minimize, validate, tenant-bind",
                "Authenticate, attest, process, validate, tenant-bind",
                1,
            ),
            "classified handling relationship removed": text.replace(
                "classified content references",
                "unclassified references",
                1,
            ),
        }
        for name, mutant in mutants.items():
            with self.subTest(mutant=name):
                with self.assertRaises(AssertionError):
                    self.assert_sensitive_telemetry_contract_complete(mutant)

    def test_failure_and_abuse_treatment_is_complete(self) -> None:
        self.assert_resilience_contract_complete(self.text())

    def test_resilience_contract_rejects_missing_failure_treatments(self) -> None:
        text = self.text()
        mutants = {
            "conflicting telemetry": text.replace("record conflicts", "record findings", 1),
            "corrupted telemetry": text.replace("schema and integrity validation", "schema validation", 1),
            "clock uncertainty": text.replace("clock quality and uncertainty", "clock quality", 1),
            "source compromise": text.replace("Spoofed source", "Unknown source", 1),
            "signing-key compromise": text.replace("compromise response", "incident response", 1),
            "provider outage": text.replace("changed semantics, or outage", "changed semantics", 1),
        }
        for name, mutant in mutants.items():
            with self.subTest(mutant=name):
                with self.assertRaises(AssertionError):
                    self.assert_resilience_contract_complete(mutant)

    def test_resilience_contract_rejects_unsafe_treatment_polarity(self) -> None:
        text = self.text()
        mutants = {
            "spoofed source accepted": text.replace(
                "Reject or quarantine; record gap; regenerate untrusted identifiers; investigate source and verifier state",
                "Accept and continue; trust supplied identifiers",
                1,
            ),
            "provider gap ignored": text.replace(
                "Record the gap, use enterprise boundary evidence, prohibit use where assurance cannot be met, and execute portability or exit plans",
                "Ignore the gap, trust provider claims, and continue use",
                1,
            ),
            "integrity failure continued": text.replace(
                "Stop Tier 3 and Tier 4 consequential commit and dependent activity; do not report success",
                "Continue Tier 3 and Tier 4 consequential commit and report success",
                1,
            ),
        }
        for name, mutant in mutants.items():
            with self.subTest(mutant=name):
                with self.assertRaises(AssertionError):
                    self.assert_resilience_contract_complete(mutant)

    def test_tier_three_and_four_safe_stop_is_explicit(self) -> None:
        text = self.text()
        for requirement in (
            "Stop Tier 3 and Tier 4 consequential commit and dependent activity; do not report success",
            "Missing tenant binding, unverifiable telemetry, privacy-policy failure, expiry, or buffer exhaustion causes fail-safe rejection.",
            "Monitoring failure cannot bypass enforcement.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_degraded_operation_and_recovery_are_bounded(self) -> None:
        text = self.text()
        for requirement in (
            "Lower-tier operation may enter only a preapproved degraded mode with protected local buffering, explicit duration and volume, visible status, and no increase in data, authority, provider, or action scope.",
            "Recovery validates signed backfill, sequence reconciliation, integrity and custody, gap disposition, privacy obligations, material incident review, and authorized return to normal.",
            "Applicability matrices define commit-blocking evidence, source, tolerated delay, degraded state, recovery condition, and change authority for each capability and action class.",
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
