import re
import unittest
from pathlib import Path

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

    def test_required_foundation_files_exist(self) -> None:
        missing = [relative for relative in REQUIRED_CROSSWALK_FILES if not (ROOT / relative).is_file()]
        self.assertEqual(missing, [], f"missing foundation files: {missing}")

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


if __name__ == "__main__":
    unittest.main()
