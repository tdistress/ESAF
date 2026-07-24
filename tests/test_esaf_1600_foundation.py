import json
import re
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import yaml

from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.schemas import load_schemas, schema_errors
from tools.crosswalks.validation import validate, validate_lifecycle


ROOT = Path(__file__).parents[1]
REQUIRED_CROSSWALK_FILES = (
    "crosswalks/ESAF-1600.md",
    "crosswalks/MAPPING_SET_TEMPLATE.md",
    "crosswalks/PROVISION_INVENTORY_TEMPLATE.md",
    "crosswalks/CROSSWALK_TEMPLATE.md",
    "crosswalks/LIFECYCLE_RECORD_TEMPLATE.md",
)
YAML_BLOCK = re.compile(r"```yaml\n(.*?)```", re.DOTALL)
CANONICAL_EXTERNAL_MAPPING_LINK = (
    "Authoritative external mappings are maintained in the "
    "[ESAF-1600 generated catalog](../../crosswalks/CATALOG.md)."
)
README_LINK_TARGETS = {
    "ESAF-1600.md",
    "MAPPING_SET_TEMPLATE.md",
    "PROVISION_INVENTORY_TEMPLATE.md",
    "CROSSWALK_TEMPLATE.md",
    "LIFECYCLE_RECORD_TEMPLATE.md",
    "CATALOG.md",
    "catalog.json",
    "../tools/README.md",
}
ESAF_1600_DECISIONS = (
    "Provision Markdown is the authoritative crosswalk source.",
    "Generated crosswalk catalogs are deterministic derivative outputs.",
    "Relationship, direction, coverage, and confidence are independent dimensions.",
    "Negative dispositions are explicit records.",
    "Independent review is required before approval.",
    "Approved mapping snapshots are immutable and version-bound, while draft snapshots remain mutable working sets.",
    "Lifecycle changes use an external append-only registry.",
    "Assessment completeness is bounded by an authoritative provision inventory.",
    "Historical mappings resolve against a release-pinned ESAF control manifest.",
    "ESAF-1600 supersedes the prior ESAF-1100 mapping taxonomy.",
    "Restricted external requirement text is excluded and publication rights are recorded.",
    "Cyber Essentials core and Cyber Essentials Plus use separate mapping sets.",
    "Cyber Essentials v3.3 uses 116 ESAF-assigned atomic provision locators.",
    "The initial Cyber Essentials v3.3 mapping remains draft pending qualified human review.",
)
PLANNED_LANDING_PAGE_CONTENT = {
    "pci-dss.md": """# PCI DSS Crosswalk

**Status:** Planned

This crosswalk will map applicable ESAF controls to a versioned PCI DSS release. Payment-account-data scope and compliance conclusions remain the responsibility of the adopting organization and its qualified assessor.

No substantive mapping is approved. Future mapping work shall follow [ESAF-1600](ESAF-1600.md) and identify the exact approved source version before any mapping-set snapshot is created.
""",
    "hitrust-csf.md": """# HITRUST CSF Crosswalk

**Status:** Planned

This crosswalk will map applicable ESAF controls to a licensed, versioned HITRUST CSF release. Public project content shall not reproduce proprietary source material beyond permitted citation and identifiers.

No substantive mapping is approved. Future mapping work shall follow [ESAF-1600](ESAF-1600.md) and identify the exact approved source version and publication-rights boundary before any mapping-set snapshot is created.
""",
}


def control_record_paths(root: Path) -> list[Path]:
    return sorted(
        path
        for path in (root / "controls").glob("*/*.md")
        if re.fullmatch(r"[A-Z]{3}-[1-9][0-9]{2}", path.stem)
    )


def markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def extract_yaml_blocks(path: Path) -> list[dict[str, object]]:
    documents: list[dict[str, object]] = []
    for block in YAML_BLOCK.findall(path.read_text(encoding="utf-8")):
        value = yaml.safe_load(block)
        if not isinstance(value, dict):
            raise AssertionError(f"{path}: YAML example must be a mapping")
        documents.append(value)
    return documents


def normalize_markdown_contract(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in normalized.split("\n")).strip("\n")
    return re.sub(r"\n{2,}", "\n\n", normalized)


class Esaf1600FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validators = load_schemas(ROOT)

    def assert_planned_landing_page(self, name: str, text: str) -> None:
        statuses = re.findall(r"(?m)^\*\*Status:\*\*\s*(\S.*?)\s*$", text)
        self.assertEqual(statuses, ["Planned"])
        self.assertNotRegex(
            text,
            r"(?im)^\*\*Status:\*\*\s*(?:Approved|Reviewed|Published)\s*$",
        )
        self.assertIn("[ESAF-1600](ESAF-1600.md)", text)
        self.assertEqual(
            normalize_markdown_contract(text),
            normalize_markdown_contract(PLANNED_LANDING_PAGE_CONTENT[name]),
        )

    def test_required_foundation_files_exist(self) -> None:
        missing = [relative for relative in REQUIRED_CROSSWALK_FILES if not (ROOT / relative).is_file()]
        self.assertEqual(missing, [], f"missing foundation files: {missing}")

    def test_every_control_delegates_external_mapping_authority(self) -> None:
        records = control_record_paths(ROOT)
        catalog = json.loads((ROOT / "controls/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(len(records), len(catalog["controls"]))
        self.assertEqual(
            {path.relative_to(ROOT / "controls").as_posix() for path in records},
            {record["path"] for record in catalog["controls"]},
        )
        for path in records:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                section = markdown_section(path.read_text(encoding="utf-8"), "External mappings")
                self.assertEqual(section, CANONICAL_EXTERNAL_MAPPING_LINK)

    def test_esaf_1100_defers_taxonomy_to_esaf_1600(self) -> None:
        text = (ROOT / "controls/ESAF-1100.md").read_text(encoding="utf-8")
        self.assertNotIn("| equivalent |", text)
        self.assertIn("ESAF-1600 is authoritative", text)

    def test_mapping_migration_preserves_every_byte_outside_section(self) -> None:
        from tools.migrate_control_mappings import replace_external_mapping, split_external_mapping

        before = (
            "# IAM-100 Example\n\n## External mappings\n\nOld text.\n\n"
            "## Change history\n\nHistory.\n"
        )
        prefix, _old, suffix = split_external_mapping(before)
        after = replace_external_mapping(before, CANONICAL_EXTERNAL_MAPPING_LINK)
        new_prefix, new_section, new_suffix = split_external_mapping(after)
        self.assertEqual((new_prefix, new_suffix), (prefix, suffix))
        self.assertEqual(new_section, CANONICAL_EXTERNAL_MAPPING_LINK)

    def test_control_validator_rejects_duplicate_external_mapping_sections(self) -> None:
        from tools import validate_controls

        original_parse_control = validate_controls.parse_control

        def parse_with_duplicate(path: Path) -> tuple[dict, str]:
            metadata, body = original_parse_control(path)
            if path.name == "GOV-100.md":
                body += (
                    "\n## External mappings\n\n"
                    "| Authority | Publication | Provision |\n"
                    "|---|---|---|\n"
                    "| Example | Example Standard | EX-1 |\n"
                )
            return metadata, body

        with patch.object(validate_controls, "parse_control", side_effect=parse_with_duplicate):
            errors, _records, _objectives, _families = validate_controls.validate()

        self.assertIn(
            "controls/GOV/GOV-100.md: expected exactly one '## External mappings' heading; found 2",
            errors,
        )

    def test_methodology_contains_required_normative_sections(self) -> None:
        text = (ROOT / "crosswalks/ESAF-1600.md").read_text(encoding="utf-8")
        required_headings = (
            "Purpose and scope",
            "Authority boundaries",
            "Record model and repository paths",
            "Canonical identifiers",
            "Completeness",
            "Mapping taxonomy",
            "Negative dispositions",
            "Review and findings",
            "Publication rights",
            "Manifest provenance",
            "Snapshot and event digests",
            "Lifecycle",
            "Validation",
            "Generated catalogs",
            "Adoption disclaimers",
        )
        for heading in required_headings:
            with self.subTest(heading=heading):
                self.assertRegex(text, rf"(?m)^## \d+\. {re.escape(heading)}$")

    def test_methodology_prohibits_compliance_equivalence(self) -> None:
        text = (ROOT / "crosswalks/ESAF-1600.md").read_text(encoding="utf-8")
        self.assertIn(
            "shall not establish certification, compliance, equivalence, or legal sufficiency",
            text,
        )

    def test_methodology_requires_one_lifecycle_record_for_every_mapping_set(self) -> None:
        text = (ROOT / "crosswalks/ESAF-1600.md").read_text(encoding="utf-8")
        self.assertIn(
            "Every mapping set, whether draft, reviewed, or approved, shall have exactly one lifecycle record",
            text,
        )

    def test_methodology_defines_lifecycle_as_a_valid_prefix(self) -> None:
        text = (ROOT / "crosswalks/ESAF-1600.md").read_text(encoding="utf-8")
        self.assertIn(
            "shall be an append-only valid prefix of `approved`, `published`, `deprecated`, `retired`",
            text,
        )
        self.assertIn("The current terminal state may be any state in that ordered sequence", text)
        self.assertNotIn("without omission, duplication, or reordering", text)

    def test_methodology_states_reviewed_finding_gate_exactly(self) -> None:
        text = (ROOT / "crosswalks/ESAF-1600.md").read_text(encoding="utf-8")
        self.assertIn(
            "Reviewed provision records and reviewed or approved snapshots shall have no open Critical or Important findings",
            text,
        )

    def test_methodology_does_not_require_terminal_lf_for_snapshot_digest(self) -> None:
        text = (ROOT / "crosswalks/ESAF-1600.md").read_text(encoding="utf-8")
        self.assertNotIn("LF-terminated bytes", text)
        self.assertIn("hash each permitted file's exact bytes", text)

    def test_templates_are_outside_authoritative_mapping_discovery(self) -> None:
        result = validate(ROOT)
        self.assertEqual(len(result.mapping_sets), 3)
        self.assertEqual(len(result.lifecycle_records), 3)
        self.assertTrue(all("TEMPLATE" not in item["path"] for item in result.mapping_sets))
        self.assertTrue(all("TEMPLATE" not in item["path"] for item in result.lifecycle_records))

    def test_lifecycle_template_contains_complete_valid_chain(self) -> None:
        metadata, _ = parse_front_matter(ROOT / "crosswalks/LIFECYCLE_RECORD_TEMPLATE.md")
        self.assertEqual(
            [event["state"] for event in metadata["events"]],
            ["approved", "published", "deprecated", "retired"],
        )
        self.assertEqual(
            schema_errors(self.validators["lifecycle-record"], metadata, "template"),
            [],
        )
        self.assertEqual(validate_lifecycle([metadata]), [])

    def test_mapping_set_template_is_schema_valid(self) -> None:
        metadata, _ = parse_front_matter(ROOT / "crosswalks/MAPPING_SET_TEMPLATE.md")
        self.assertEqual(schema_errors(self.validators["mapping-set"], metadata, "template"), [])

    def test_mapping_set_template_demonstrates_review_approval_and_history_shapes(self) -> None:
        metadata, _ = parse_front_matter(ROOT / "crosswalks/MAPPING_SET_TEMPLATE.md")
        self.assertEqual(
            set(metadata["reviewer"]),
            {"id", "qualification", "date", "authorized_source_access", "findings_disposition"},
        )
        self.assertEqual(set(metadata["approver"]), {"id", "date"})
        self.assertRegex(metadata["predecessor_id"], r"--\d+\.\d+\.\d+$")
        resolved = metadata["findings"][0]
        self.assertEqual(resolved["status"], "resolved")
        self.assertTrue(resolved["resolver_or_acceptor"])
        self.assertTrue(resolved["disposition_date"])

        examples = extract_yaml_blocks(ROOT / "crosswalks/MAPPING_SET_TEMPLATE.md")
        self.assertEqual(len(examples), 1)
        accepted = examples[0]
        self.assertEqual(accepted["severity"], "Minor")
        self.assertEqual(accepted["status"], "accepted")
        self.assertTrue(accepted["resolver_or_acceptor"])
        self.assertTrue(accepted["disposition_date"])
        self.assertTrue(accepted["acceptance_rationale"])
        variant = dict(metadata)
        variant["findings"] = [accepted]
        self.assertEqual(schema_errors(self.validators["mapping-set"], variant, "template"), [])

    def test_inventory_template_demonstrates_both_scope_types(self) -> None:
        examples = extract_yaml_blocks(ROOT / "crosswalks/PROVISION_INVENTORY_TEMPLATE.md")
        self.assertEqual(len(examples), 2)
        self.assertEqual(
            {item["scope_type"] for item in examples},
            {"complete_publication", "declared_subset"},
        )
        for item in examples:
            self.assertEqual(
                schema_errors(self.validators["provision-inventory"], item, "template"),
                [],
            )

    def test_crosswalk_template_examples_are_schema_valid_and_complete(self) -> None:
        examples = extract_yaml_blocks(ROOT / "crosswalks/CROSSWALK_TEMPLATE.md")
        for item in examples:
            self.assertEqual(schema_errors(self.validators["mapping-record"], item, "template"), [])
        mapped = next(
            item
            for item in examples
            if item["disposition"] == "mapped" and item["granularity"] == "requirement"
        )
        self.assertEqual(
            {leg["direction"] for leg in mapped["relationships"]},
            {"esaf_to_external", "external_to_esaf"},
        )
        self.assertNotEqual(
            mapped["relationships"][0]["relationship"],
            mapped["relationships"][1]["relationship"],
        )
        clause = next(item for item in examples if item["granularity"] == "clause")
        self.assertTrue(clause["granularity_exception"])
        self.assertEqual(
            {item["disposition"] for item in examples},
            {"mapped", "no_direct_mapping", "out_of_scope"},
        )

    def test_crosswalk_readme_documents_taxonomy_and_operational_links(self) -> None:
        path = ROOT / "crosswalks/README.md"
        text = path.read_text(encoding="utf-8")
        for dimension in ("relationship", "direction", "coverage", "confidence"):
            self.assertIn(dimension, text)
        self.assertNotIn("strength", text.lower())
        local_targets = {
            target.split("#", 1)[0]
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
            if "://" not in target and not target.startswith("#")
        }
        self.assertEqual(local_targets, README_LINK_TARGETS)
        for target in local_targets:
            with self.subTest(target=target):
                self.assertTrue((path.parent / target).resolve().is_file())
        self.assertIn("python tools/validate_crosswalks.py --write", text)
        self.assertIn("python tools/validate_crosswalks.py --check", text)

    def test_landing_pages_remain_planned_and_link_methodology(self) -> None:
        for name in ("pci-dss.md", "hitrust-csf.md"):
            text = (ROOT / "crosswalks" / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assert_planned_landing_page(name, text)

    def test_landing_page_contract_rejects_status_and_mapping_content_mutations(self) -> None:
        text = (ROOT / "crosswalks/pci-dss.md").read_text(encoding="utf-8")
        mutations = (
            text.replace("**Status:** Planned", "**Status:** Approved"),
            text.replace("**Status:** Planned", "**Status:** Planned\n\n**Status:** Reviewed"),
            text.replace(
                "Payment-account-data scope",
                "PCI DSS 1.1 maps directly to IAM-100. Payment-account-data scope",
            ),
            text + "\n| External provision | ESAF control |\n|---|---|\n| 1.1 | IAM-100 |\n",
            text + "\n## Approved mappings\n\nNo rows yet.\n",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation[-80:]):
                with self.assertRaises(AssertionError):
                    self.assert_planned_landing_page("pci-dss.md", mutation)

        whitespace_variant = text.replace("\n", "  \r\n\r\n")
        self.assert_planned_landing_page("pci-dss.md", whitespace_variant)

    def test_contributing_requires_rights_provenance(self) -> None:
        text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        for phrase in (
            "exact source identity and version",
            "publication-rights basis",
            "permitted and prohibited elements",
            "authorized source access",
            "reviewer_authorized_source_access: true",
            "publication_basis_reviewed: true",
            "mapper and reviewer shall be different people",
            "intellectual-property attestation",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no restricted or licensed external requirement text", text)
        self.assertNotIn("restricted or unlicensed", text)

    def test_decision_log_records_esaf_1600_decisions_without_renumbering(self) -> None:
        text = (ROOT / "project/DECISION_LOG.md").read_text(encoding="utf-8")
        decision_lines = [line for line in text.splitlines() if line.startswith("| DEC-")]
        row_pattern = re.compile(
            r"^\| (DEC-\d{4}) \| (\d{4}-\d{2}-\d{2}) \| (.+) \| ([A-Za-z]+) \|$"
        )
        rows = []
        for line in decision_lines:
            match = row_pattern.fullmatch(line)
            self.assertIsNotNone(match, f"malformed decision row: {line}")
            rows.append(match.groups())

        ids = [row[0] for row in rows]
        expected_ids = [f"DEC-{number:04d}" for number in range(1, 29)]
        self.assertEqual(ids, expected_ids)
        self.assertEqual(len(ids), len(set(ids)))

        esaf_rows = rows[14:28]
        self.assertEqual(
            [(row[0], row[2], row[3]) for row in esaf_rows],
            [
                (f"DEC-{number:04d}", decision, "Accepted")
                for number, decision in zip(range(15, 29), ESAF_1600_DECISIONS)
            ],
        )

    def test_tools_readme_documents_crosswalk_validation_modes(self) -> None:
        text = (ROOT / "tools/README.md").read_text(encoding="utf-8")
        self.assertIn("python tools/validate_crosswalks.py --write", text)
        self.assertIn("python tools/validate_crosswalks.py --check", text)
        self.assertIn("python tools/validate_crosswalks.py --check --baseline-ref", text)
        self.assertIn("full Git history", text)

    def assert_ci_workflow_contract(self, workflow: dict[str, object]) -> None:
        triggers = workflow["on"]
        self.assertEqual(set(triggers), {"pull_request", "push", "workflow_dispatch"})
        expected_paths = [
            ".github/workflows/catalog-validation.yml",
            "CHANGELOG.md",
            "VERSION.md",
            "ROADMAP.md",
            "project/**",
            "docs/superpowers/reviews/**",
            "architectures/**",
            "assessment/**",
            "controls/**",
            "crosswalks/**",
            "tests/**",
            "tools/crosswalks/**",
            "tools/release_gates.py",
            "tools/mermaid_inventory.py",
            "tools/validate_links.py",
            "tools/validate_architectures.py",
            "tools/validate_assessment.py",
            "tools/validate_controls.py",
            "tools/validate_crosswalks.py",
            "requirements-dev.txt",
        ]
        for event in ("pull_request", "push"):
            self.assertEqual(triggers[event]["paths"], expected_paths)
        self.assertEqual(triggers["push"]["branches"], ["main"])

        steps = workflow["jobs"]["validate"]["steps"]

        def unique_step(name: str) -> dict[str, object]:
            matches = [step for step in steps if step.get("name") == name]
            self.assertEqual(len(matches), 1, f"expected one active {name!r} step")
            return matches[0]

        checkout = unique_step("Check out repository")
        self.assertEqual(checkout["uses"], "actions/checkout@v5")
        self.assertIn("with", checkout)
        self.assertEqual(checkout["with"]["fetch-depth"], "0")

        current = unique_step("Validate crosswalk catalog")
        self.assertEqual(current, {
            "name": "Validate crosswalk catalog",
            "run": "python tools/validate_crosswalks.py --check",
        })

        pull_request = unique_step("Validate crosswalk history on pull request")
        self.assertEqual(pull_request["if"], "github.event_name == 'pull_request'")
        self.assertEqual(
            pull_request["run"],
            'python tools/validate_crosswalks.py --check --baseline-ref "${{ github.event.pull_request.base.sha }}"',
        )

        push = unique_step("Validate crosswalk history on protected-branch push")
        self.assertEqual(
            push["if"],
            "github.event_name == 'push' && "
            "github.event.before != '0000000000000000000000000000000000000000'",
        )
        self.assertEqual(
            push["run"],
            'python tools/validate_crosswalks.py --check --baseline-ref "${{ github.event.before }}"',
        )

        release_gate_on_pull_request = unique_step(
            "Validate release gate record on pull request"
        )
        self.assertEqual(release_gate_on_pull_request, {
            "name": "Validate release gate record on pull request",
            "if": "github.event_name == 'pull_request'",
            "run": (
                "python tools/release_gates.py --check --baseline-ref "
                '\"${{ github.event.pull_request.base.sha }}\"'
            ),
        })

        release_gate_on_protected_push = unique_step(
            "Validate release gate record on protected-branch push"
        )
        self.assertEqual(release_gate_on_protected_push, {
            "name": "Validate release gate record on protected-branch push",
            "if": (
                "github.event_name == 'push' && "
                "github.event.before != '0000000000000000000000000000000000000000'"
            ),
            "run": (
                "python tools/release_gates.py --check --baseline-ref "
                '\"${{ github.event.before }}\"'
            ),
        })

        release_gate_on_workflow_dispatch = unique_step(
            "Validate release gate record on workflow dispatch"
        )
        self.assertEqual(release_gate_on_workflow_dispatch, {
            "name": "Validate release gate record on workflow dispatch",
            "if": "github.event_name == 'workflow_dispatch'",
            "run": 'python tools/release_gates.py --check --baseline-ref "HEAD^"',
        })

        release_gate_runs = [
            (step["run"], step.get("if", ""))
            for step in steps
            if "release_gates.py" in step.get("run", "")
        ]
        self.assertEqual(
            release_gate_runs,
            [
                (
                    "python tools/release_gates.py --check --baseline-ref "
                    '"${{ github.event.pull_request.base.sha }}"',
                    "github.event_name == 'pull_request'",
                ),
                (
                    "python tools/release_gates.py --check --baseline-ref "
                    '"${{ github.event.before }}"',
                    "github.event_name == 'push' && "
                    "github.event.before != '0000000000000000000000000000000000000000'",
                ),
                (
                    'python tools/release_gates.py --check --baseline-ref "HEAD^"',
                    "github.event_name == 'workflow_dispatch'",
                ),
            ],
        )

        links = unique_step("Validate repository-local links")
        self.assertEqual(links, {
            "name": "Validate repository-local links",
            "run": "python tools/validate_links.py --check",
        })

        active_runs = [step.get("run") for step in steps]
        self.assertEqual(active_runs.count("python tools/validate_architectures.py"), 1)
        self.assertEqual(
            active_runs.count("python tools/validate_assessment.py --check"), 1
        )
        self.assertEqual(active_runs.count("python tools/validate_controls.py --check"), 1)
        crosswalk_runs = [
            (step["run"], step.get("if", ""))
            for step in steps
            if "validate_crosswalks.py" in step.get("run", "")
        ]
        self.assertEqual(
            crosswalk_runs,
            [
                ("python tools/validate_crosswalks.py --check", ""),
                (
                    "python tools/validate_crosswalks.py --check --baseline-ref "
                    '"${{ github.event.pull_request.base.sha }}"',
                    "github.event_name == 'pull_request'",
                ),
                (
                    "python tools/validate_crosswalks.py --check --baseline-ref "
                    '"${{ github.event.before }}"',
                    "github.event_name == 'push' && "
                    "github.event.before != '0000000000000000000000000000000000000000'",
                ),
            ],
        )

    def test_ci_fetches_history_and_runs_crosswalk_validation(self) -> None:
        workflow_path = ROOT / ".github/workflows/catalog-validation.yml"
        workflow = yaml.load(
            workflow_path.read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        self.assertIsInstance(workflow, dict)
        self.assert_ci_workflow_contract(workflow)

    def test_ci_contract_rejects_duplicate_steps_and_path_entries(self) -> None:
        workflow_path = ROOT / ".github/workflows/catalog-validation.yml"
        workflow = yaml.load(
            workflow_path.read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        self.assertIsInstance(workflow, dict)

        mutations = []
        steps = workflow["jobs"]["validate"]["steps"]
        for name in (
            "Validate crosswalk catalog",
            "Validate crosswalk history on pull request",
            "Validate crosswalk history on protected-branch push",
        ):
            mutation = deepcopy(workflow)
            original = next(step for step in steps if step["name"] == name)
            duplicate = deepcopy(original)
            duplicate["name"] = f"Duplicate {name}"
            mutation["jobs"]["validate"]["steps"].append(duplicate)
            mutations.append((f"duplicate step: {name}", mutation))

        for event in ("pull_request", "push"):
            duplicate_path = deepcopy(workflow)
            duplicate_path["on"][event]["paths"].append("crosswalks/**")
            mutations.append((f"duplicate path: {event}", duplicate_path))

            extra_path = deepcopy(workflow)
            extra_path["on"][event]["paths"].append("docs/**")
            mutations.append((f"extra path: {event}", extra_path))

        generic_release_gate = deepcopy(workflow)
        generic_release_gate["jobs"]["validate"]["steps"].append({
            "name": "Prohibited generic release gate validation",
            "run": "python tools/release_gates.py --check",
        })
        mutations.append(("generic release gate validation", generic_release_gate))

        for name, mutation in mutations:
            with self.subTest(mutation=name):
                with self.assertRaises(AssertionError):
                    self.assert_ci_workflow_contract(mutation)


if __name__ == "__main__":
    unittest.main()
