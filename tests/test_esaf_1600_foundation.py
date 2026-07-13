import json
import re
import unittest
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
)


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


class Esaf1600FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validators = load_schemas(ROOT)

    def assert_planned_landing_page(self, text: str) -> None:
        statuses = re.findall(r"(?m)^\*\*Status:\*\*\s*(\S.*?)\s*$", text)
        self.assertEqual(statuses, ["Planned"])
        self.assertNotRegex(
            text,
            r"(?im)^\*\*Status:\*\*\s*(?:Approved|Reviewed|Published)\s*$",
        )
        self.assertEqual(len(re.findall(r"(?m)^# ", text)), 1)
        self.assertNotRegex(text, r"(?m)^---\s*$")
        self.assertNotRegex(text, r"(?m)^\|")
        blocks = re.split(r"\n{2,}", text.strip())
        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[1], "**Status:** Planned")
        self.assertTrue(blocks[2].startswith("This crosswalk will map"))
        self.assertTrue(blocks[3].startswith("No substantive mapping is approved."))
        self.assertIn("[ESAF-1600](ESAF-1600.md)", blocks[3])

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

    def test_templates_are_outside_mapping_discovery(self) -> None:
        result = validate(ROOT)
        self.assertEqual(result.mapping_sets, [])
        self.assertEqual(result.lifecycle_records, [])

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
        for name in ("pci-dss.md", "hitrust-csf.md", "uk-cyber-essentials.md"):
            text = (ROOT / "crosswalks" / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assert_planned_landing_page(text)

    def test_landing_page_contract_rejects_status_and_mapping_content_mutations(self) -> None:
        text = (ROOT / "crosswalks/pci-dss.md").read_text(encoding="utf-8")
        mutations = (
            text.replace("**Status:** Planned", "**Status:** Approved"),
            text.replace("**Status:** Planned", "**Status:** Planned\n\n**Status:** Reviewed"),
            text + "\n| External provision | ESAF control |\n|---|---|\n| 1.1 | IAM-100 |\n",
            text + "\n## Approved mappings\n\nNo rows yet.\n",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation[-80:]):
                with self.assertRaises(AssertionError):
                    self.assert_planned_landing_page(mutation)

    def test_contributing_requires_rights_provenance(self) -> None:
        text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        for phrase in (
            "exact source identity and version",
            "publication-rights basis",
            "permitted and prohibited elements",
            "authorized source access",
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
        expected_ids = [f"DEC-{number:04d}" for number in range(1, 26)]
        self.assertEqual(ids, expected_ids)
        self.assertEqual(len(ids), len(set(ids)))

        esaf_rows = rows[14:25]
        self.assertEqual(
            [(row[0], row[2], row[3]) for row in esaf_rows],
            [
                (f"DEC-{number:04d}", decision, "Accepted")
                for number, decision in zip(range(15, 26), ESAF_1600_DECISIONS)
            ],
        )

    def test_tools_readme_documents_crosswalk_validation_modes(self) -> None:
        text = (ROOT / "tools/README.md").read_text(encoding="utf-8")
        self.assertIn("python tools/validate_crosswalks.py --write", text)
        self.assertIn("python tools/validate_crosswalks.py --check", text)
        self.assertIn("python tools/validate_crosswalks.py --check --baseline-ref", text)
        self.assertIn("full Git history", text)


if __name__ == "__main__":
    unittest.main()
