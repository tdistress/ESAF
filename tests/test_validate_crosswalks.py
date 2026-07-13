import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from tests.crosswalk_fixtures import MAPPING_SET_ID, CrosswalkFixture, valid_event
from tools.crosswalks.digests import event_bytes, event_digest, snapshot_digest
from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.manifest import build_control_manifest, git_bytes, render_manifest
from tools.crosswalks.catalog import (
    build_catalog,
    check_outputs,
    render_json,
    render_markdown,
)
from tools.crosswalks.validation import _validate_mappings_tree, validate, validate_record
from tools.validate_crosswalks import main as crosswalk_cli


class CrosswalkValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.fixture = CrosswalkFixture(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_empty_catalog_is_explicit_and_deterministic(self) -> None:
        catalog = build_catalog(validate(self.root))
        self.assertEqual(catalog["counts"]["mapping_sets"], 0)
        self.assertEqual(catalog["counts"]["provisions"], 0)
        self.assertEqual(catalog["counts"]["relationships"], 0)
        self.assertEqual(catalog["counts"]["negative_dispositions"], 0)
        markdown = render_markdown(catalog)
        self.assertIn("No mapping sets have been assessed", markdown)
        self.assertNotIn("unmapped", markdown.lower())
        self.assertEqual(render_json(catalog), render_json(catalog))
        self.assertEqual(markdown, render_markdown(catalog))

    def test_catalog_rejects_malformed_mapping_set_components(self) -> None:
        self.fixture.create_valid_snapshot(status="draft", complete=True)
        cases = (
            ("non-mapping model", lambda result: result.mapping_sets.__setitem__(0, [])),
            ("missing metadata", lambda result: result.mapping_sets[0].pop("metadata")),
            (
                "non-mapping metadata",
                lambda result: result.mapping_sets[0].__setitem__("metadata", []),
            ),
            (
                "schema-invalid metadata",
                lambda result: result.mapping_sets[0]["metadata"].pop("authority"),
            ),
            ("missing inventory", lambda result: result.mapping_sets[0].pop("inventory")),
            (
                "non-mapping inventory",
                lambda result: result.mapping_sets[0].__setitem__("inventory", []),
            ),
            (
                "missing inventory metadata",
                lambda result: result.mapping_sets[0]["inventory"].pop("metadata"),
            ),
            ("missing lifecycle", lambda result: result.mapping_sets[0].pop("lifecycle")),
            (
                "non-mapping lifecycle",
                lambda result: result.mapping_sets[0].__setitem__("lifecycle", []),
            ),
            (
                "lifecycle differs from registry",
                lambda result: result.mapping_sets[0].__setitem__(
                    "lifecycle",
                    {
                        **result.mapping_sets[0]["lifecycle"],
                        "snapshot_digest": "0" * 64,
                    },
                ),
            ),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                result = copy.deepcopy(validate(self.root))
                mutation(result)
                with self.assertRaisesRegex(ValueError, "^invalid catalog model:") as first:
                    build_catalog(result)
                with self.assertRaisesRegex(ValueError, "^invalid catalog model:") as second:
                    build_catalog(result)
                self.assertEqual(str(first.exception), str(second.exception))

    def test_catalog_rejects_malformed_provisions_and_relationships(self) -> None:
        self.fixture.create_valid_snapshot(status="draft", complete=True)
        cases = (
            (
                "non-array provisions",
                lambda result: result.mapping_sets[0].__setitem__("provisions", {}),
            ),
            (
                "non-mapping provision",
                lambda result: result.mapping_sets[0]["provisions"].__setitem__(0, []),
            ),
            (
                "missing provision metadata",
                lambda result: result.mapping_sets[0]["provisions"][0].pop("metadata"),
            ),
            (
                "non-array relationships",
                lambda result: result.mapping_sets[0]["provisions"][0]["metadata"].__setitem__(
                    "relationships", {}
                ),
            ),
            (
                "non-mapping relationship",
                lambda result: result.mapping_sets[0]["provisions"][0]["metadata"][
                    "relationships"
                ].__setitem__(0, []),
            ),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                result = copy.deepcopy(validate(self.root))
                mutation(result)
                with self.assertRaisesRegex(ValueError, "^invalid catalog model:"):
                    build_catalog(result)

    def test_catalog_rejects_every_missing_relationship_field(self) -> None:
        self.fixture.create_valid_snapshot(status="draft", complete=True)
        required_fields = (
            "esaf_control_id",
            "esaf_control_version",
            "relationship",
            "direction",
            "coverage",
            "confidence",
            "rationale",
            "conditions",
            "expected_evidence",
            "known_gaps",
        )
        for field in required_fields:
            with self.subTest(field=field):
                result = copy.deepcopy(validate(self.root))
                result.mapping_sets[0]["provisions"][0]["metadata"]["relationships"][
                    0
                ].pop(field)
                with self.assertRaisesRegex(ValueError, "^invalid catalog model:"):
                    build_catalog(result)

    def test_catalog_rejects_non_posix_or_out_of_scope_paths(self) -> None:
        self.fixture.create_valid_snapshot(status="draft", complete=True)
        cases = (
            (
                "mapping Windows path",
                lambda result: result.mapping_sets[0].__setitem__(
                    "path", "crosswalks\\mappings\\nist\\README.md"
                ),
            ),
            (
                "mapping absolute path",
                lambda result: result.mapping_sets[0].__setitem__(
                    "path", "/crosswalks/mappings/nist/README.md"
                ),
            ),
            (
                "mapping traversal",
                lambda result: result.mapping_sets[0].__setitem__(
                    "path", "crosswalks/mappings/../registry/record.md"
                ),
            ),
            (
                "mapping wrong scope",
                lambda result: result.mapping_sets[0].__setitem__(
                    "path", "controls/README.md"
                ),
            ),
            (
                "inventory wrong scope",
                lambda result: result.mapping_sets[0]["inventory"].__setitem__(
                    "path", "crosswalks/registry/PROVISION_INVENTORY.md"
                ),
            ),
            (
                "provision wrong snapshot",
                lambda result: result.mapping_sets[0]["provisions"][0].__setitem__(
                    "path", "crosswalks/mappings/other/record.md"
                ),
            ),
            (
                "registry Windows path",
                lambda result: result.lifecycle_records[0].__setitem__(
                    "path", "crosswalks\\registry\\record.md"
                ),
            ),
            (
                "registry wrong scope",
                lambda result: result.lifecycle_records[0].__setitem__(
                    "path", "crosswalks/mappings/record.md"
                ),
            ),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                result = copy.deepcopy(validate(self.root))
                mutation(result)
                with self.assertRaisesRegex(ValueError, "^invalid catalog model:"):
                    build_catalog(result)

    def test_check_reports_stale_generated_output_exactly(self) -> None:
        self.fixture.write_generated_catalogs("stale\n", "{}\n")
        catalog = build_catalog(validate(self.root))
        errors = check_outputs(self.root, catalog)
        self.assertEqual(errors, sorted(errors))
        self.assertEqual(len(errors), 2)
        self.assertTrue(
            all("generated output is missing or stale" in error for error in errors)
        )
        self.fixture.write_generated_catalogs(
            render_markdown(catalog), render_json(catalog)
        )
        self.assertEqual(check_outputs(self.root, catalog), [])

    def test_nonempty_catalog_preserves_data_counts_links_and_semantic_order(self) -> None:
        self.fixture.create_mixed_catalog_fixture(
            mapping_set_versions=("0.10.0", "0.2.0"),
            lifecycle_states=("deprecated", "published"),
            dispositions=("mapped", "no_direct_mapping", "out_of_scope"),
            include_both_directions=True,
        )
        result = validate(self.root)
        self.assertEqual(result.errors, [])
        catalog = build_catalog(result)
        self.assertEqual(catalog["schema_version"], "1.0.0")
        self.assertEqual(
            catalog["generated_from"],
            "crosswalks/mappings/** and crosswalks/registry/*.md",
        )
        self.assertEqual(catalog["counts"]["mapping_sets"], 2)
        self.assertEqual(catalog["counts"]["provisions"], 6)
        self.assertEqual(catalog["counts"]["relationships"], 4)
        self.assertEqual(catalog["counts"]["negative_dispositions"], 4)
        self.assertEqual(
            catalog["counts"]["by_direction"],
            {"esaf_to_external": 2, "external_to_esaf": 2},
        )
        self.assertEqual(
            catalog["counts"]["by_disposition"],
            {"mapped": 2, "no_direct_mapping": 2, "out_of_scope": 2},
        )
        for dimension in (
            "by_snapshot_status",
            "by_lifecycle_state",
            "by_provision_status",
            "by_authority",
            "by_publication",
            "by_source_version",
            "by_esaf_release",
            "by_disposition",
            "by_relationship",
            "by_direction",
            "by_coverage",
            "by_confidence",
        ):
            self.assertEqual(
                list(catalog["counts"][dimension]),
                sorted(catalog["counts"][dimension]),
            )
        self.assertEqual(
            [item["metadata"]["mapping_set_version"] for item in catalog["mapping_sets"]],
            ["0.2.0", "0.10.0"],
        )
        for mapping_set in catalog["mapping_sets"]:
            self.assertIn(
                mapping_set["lifecycle"]["events"][-1]["state"],
                {"published", "deprecated"},
            )
            self.assertEqual(
                mapping_set["inventory"]["mapping_set_id"],
                mapping_set["metadata"]["mapping_set_id"],
            )
            mapped = next(
                item
                for item in mapping_set["provisions"]
                if item["metadata"]["disposition"] == "mapped"
            )
            self.assertEqual(
                {leg["direction"] for leg in mapped["metadata"]["relationships"]},
                {"esaf_to_external", "external_to_esaf"},
            )
            self.assertTrue(
                mapped["path"].endswith(f"{mapped['metadata']['record_id']}.md")
            )
        markdown = render_markdown(catalog)
        headings = (
            "## Active published mapping sets",
            "## Reviewed and draft work",
            "## Deprecated and retired history",
            "## Coverage and gaps",
        )
        positions = [markdown.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        for mapping_set in catalog["mapping_sets"]:
            self.assertIn(
                f"({mapping_set['path'].removeprefix('crosswalks/')})", markdown
            )
            for provision in mapping_set["provisions"]:
                self.assertIn(
                    f"({provision['path'].removeprefix('crosswalks/')})", markdown
                )

    def test_cli_requires_exactly_one_mode(self) -> None:
        for arguments in ([], ["--check", "--write"]):
            with self.subTest(arguments=arguments):
                with redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        crosswalk_cli(arguments, root=self.root)
                self.assertEqual(raised.exception.code, 2)

    def test_cli_is_directly_executable_from_repository_root(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [sys.executable, "tools/validate_crosswalks.py", "--help"],
            cwd=repository,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--baseline-ref", completed.stdout)

    def test_cli_write_occurs_only_after_successful_validation(self) -> None:
        self.fixture.write_generated_catalogs("markdown sentinel\n", "json sentinel\n")
        self.fixture.create_valid_snapshot(status="reviewed", complete=False)
        output = io.StringIO()
        with redirect_stdout(output):
            return_code = crosswalk_cli(["--write"], root=self.root)
        self.assertEqual(return_code, 1)
        self.assertEqual(
            (self.root / "crosswalks" / "CATALOG.md").read_text(encoding="utf-8"),
            "markdown sentinel\n",
        )
        self.assertEqual(
            (self.root / "crosswalks" / "catalog.json").read_text(encoding="utf-8"),
            "json sentinel\n",
        )
        diagnostics = [
            line for line in output.getvalue().splitlines() if line.startswith("- ")
        ]
        self.assertEqual(diagnostics, sorted(diagnostics))

    def test_cli_write_check_and_optional_baseline_ref(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(crosswalk_cli(["--write"], root=self.root), 0)
            self.assertEqual(crosswalk_cli(["--check"], root=self.root), 0)
            self.assertEqual(
                crosswalk_cli(["--check", "--baseline-ref", "HEAD"], root=self.root),
                0,
            )
        self.assertIn("0 mapping sets, 0 provisions, 0 relationships", output.getvalue())

    def test_valid_incomplete_draft_is_accepted(self) -> None:
        self.fixture.create_valid_snapshot(status="draft", complete=False)
        self.assertEqual(validate(self.root).errors, [])

    def test_event_digest_uses_fixed_length_prefixed_utf8(self) -> None:
        event = valid_event(
            event_id="evt-001",
            state="approved",
            date="2026-07-13",
            actor="reviewer-1",
            reason="Cafe\u0301",
            predecessor_id="",
            successor_id="",
            approval_reference="APR-001",
            previous_event_digest="0" * 64,
        )
        expected = (
            b"event_id:7:evt-001\n"
            b"state:8:approved\n"
            b"date:10:2026-07-13\n"
            b"actor:10:reviewer-1\n"
            b"reason:5:Caf\xc3\xa9\n"
            b"predecessor_id:0:\n"
            b"successor_id:0:\n"
            b"approval_reference:7:APR-001\n"
            b"previous_event_digest:64:"
            + (b"0" * 64)
            + b"\n"
        )
        self.assertEqual(event_bytes(event), expected)
        self.assertEqual(
            event_digest(event),
            "dce6853af1e45395304b66d057807375f8c0d61e7393a725f4776e9fba00b811",
        )

    def test_approved_snapshot_mutation_against_baseline_is_rejected(self) -> None:
        baseline = self.fixture.commit_approved_snapshot()
        self.fixture.mutate_approved_record()
        errors = validate(self.root, baseline_ref=baseline).errors
        self.assertIn("approved snapshot differs from trusted baseline", "\n".join(errors))

    def test_positive_lifecycle_states_are_accepted(self) -> None:
        for state in ("approved", "published", "deprecated", "retired"):
            with self.subTest(state=state):
                self.fixture.reset_crosswalks()
                self.fixture.create_approved_snapshot_with_lifecycle(final_state=state)
                self.assertEqual(validate(self.root).errors, [])

    def test_empty_registry_placeholder_is_accepted(self) -> None:
        registry = self.root / "crosswalks" / "registry"
        registry.mkdir(parents=True)
        (registry / ".gitkeep").write_bytes(b"")
        self.assertEqual(validate(self.root).errors, [])

    def test_lifecycle_and_baseline_mutation_matrix(self) -> None:
        cases = (
            (
                "rewrite_snapshot_and_registry_digest",
                "approved snapshot differs from trusted baseline",
            ),
            (
                "rewrite_prior_event_and_rehash_chain",
                "baseline lifecycle events are not an exact prefix",
            ),
            ("reorder_lifecycle_events", "invalid lifecycle transition"),
            ("duplicate_lifecycle_event", "duplicate lifecycle event"),
            ("skip_published_transition", "invalid lifecycle transition"),
            ("publish_unapproved_snapshot", "published lifecycle requires approved snapshot"),
            ("publish_second_active_version", "multiple active published mapping sets"),
            (
                "deprecate_without_successor_or_explanation",
                "deprecated lifecycle requires successor or explanation",
            ),
            ("set_stale_snapshot_digest", "lifecycle snapshot digest mismatch"),
        )
        for mutation, expected in cases:
            with self.subTest(mutation=mutation):
                self.fixture.reset_repository()
                baseline = self.fixture.commit_approved_snapshot_with_lifecycle()
                getattr(self.fixture, mutation)()
                self.assertIn(
                    expected,
                    "\n".join(validate(self.root, baseline_ref=baseline).errors),
                )

    def test_schema_invalid_lifecycle_identifiers_fail_closed(self) -> None:
        cases = (
            ("set_unhashable_lifecycle_event_id", "events.0.event_id"),
            ("set_unhashable_lifecycle_mapping_set_id", "mapping_set_id"),
        )
        for mutation, expected in cases:
            with self.subTest(mutation=mutation):
                self.fixture.reset_crosswalks()
                self.fixture.create_approved_snapshot_with_lifecycle("approved")
                getattr(self.fixture, mutation)()
                errors = validate(self.root).errors
                self.assertEqual(errors, sorted(set(errors)))
                self.assertIn(expected, "\n".join(errors))

    def test_schema_invalid_baseline_lifecycle_identifier_fails_closed(self) -> None:
        baseline = self.fixture.commit_unhashable_lifecycle_mapping_set_id()
        errors = validate(self.root, baseline_ref=baseline).errors
        self.assertEqual(errors, sorted(set(errors)))
        self.assertIn(
            "trusted baseline lifecycle metadata is malformed",
            "\n".join(errors),
        )

    def test_unparseable_baseline_lifecycle_metadata_fails_closed(self) -> None:
        baseline = self.fixture.commit_malformed_lifecycle_yaml()
        errors = validate(self.root, baseline_ref=baseline).errors
        self.assertEqual(errors, sorted(set(errors)))
        self.assertIn(
            "crosswalks/registry/"
            + MAPPING_SET_ID
            + ".md: trusted baseline lifecycle metadata is malformed",
            "\n".join(errors),
        )

    def test_unparseable_baseline_snapshot_metadata_fails_closed(self) -> None:
        for mutation in ("invalid_utf8", "bom", "crlf", "missing_front_matter"):
            with self.subTest(mutation=mutation):
                self.fixture.reset_repository()
                baseline = self.fixture.commit_malformed_snapshot_readme(mutation)
                errors = validate(self.root, baseline_ref=baseline).errors
                self.assertEqual(errors, sorted(set(errors)))
                self.assertIn(
                    "crosswalks/mappings/nist/1.0/0.4-alpha/1.0.0/README.md: "
                    "trusted baseline snapshot metadata is malformed",
                    "\n".join(errors),
                )

    def test_baseline_lifecycle_requires_closing_front_matter_delimiter(self) -> None:
        baseline = self.fixture.commit_lifecycle_missing_closing_delimiter()
        errors = validate(self.root, baseline_ref=baseline).errors
        self.assertIn(
            "crosswalks/registry/"
            + MAPPING_SET_ID
            + ".md: trusted baseline lifecycle metadata is malformed",
            "\n".join(errors),
        )

    def test_baseline_snapshot_requires_closing_front_matter_delimiter(self) -> None:
        baseline = self.fixture.commit_snapshot_readme_missing_closing_delimiter()
        errors = validate(self.root, baseline_ref=baseline).errors
        self.assertIn(
            "crosswalks/mappings/nist/1.0/0.4-alpha/1.0.0/README.md: "
            "trusted baseline snapshot metadata is malformed",
            "\n".join(errors),
        )

    def test_baseline_lifecycle_schema_rejects_empty_event_prefix(self) -> None:
        baseline = self.fixture.commit_lifecycle_with_empty_events()
        errors = validate(self.root, baseline_ref=baseline).errors
        self.assertIn(
            "crosswalks/registry/"
            + MAPPING_SET_ID
            + ".md: trusted baseline lifecycle metadata is malformed",
            "\n".join(errors),
        )

    def test_baseline_snapshot_schema_rejects_type_safe_invalid_metadata(self) -> None:
        baseline = self.fixture.commit_schema_invalid_snapshot_readme()
        errors = validate(self.root, baseline_ref=baseline).errors
        self.assertIn(
            "crosswalks/mappings/nist/1.0/0.4-alpha/1.0.0/README.md: "
            "trusted baseline snapshot metadata is malformed",
            "\n".join(errors),
        )

    def test_incomplete_reviewed_snapshot_is_rejected(self) -> None:
        self.fixture.create_valid_snapshot(status="reviewed", complete=False)
        errors = validate(self.root).errors
        self.assertIn("missing provision record for inventory identifier EXT-2", "\n".join(errors))

    def test_reviewed_snapshot_rejects_open_or_accepted_critical_and_important_findings(self) -> None:
        for status in ("open", "accepted"):
            for severity in ("Critical", "Important"):
                with self.subTest(status=status, severity=severity):
                    self.fixture.reset_crosswalks()
                    self.fixture.create_valid_snapshot(status="reviewed", complete=True)
                    if status == "open":
                        self.fixture.add_open_snapshot_finding(severity)
                    else:
                        self.fixture.accept_snapshot_finding(severity)
                    self.fixture.refresh_lifecycle_snapshot_digest()
                    errors = "\n".join(validate(self.root).errors)
                    self.assertIn(
                        f"{status} {severity} review finding blocks reviewed content",
                        errors,
                    )
                    self.assertIn("/1.0.0:", errors)

    def test_reviewed_record_in_draft_snapshot_rejects_targeted_open_or_accepted_high_findings(self) -> None:
        for status in ("open", "accepted"):
            for severity in ("Critical", "Important"):
                with self.subTest(status=status, severity=severity):
                    self.fixture.reset_crosswalks()
                    self.fixture.create_valid_snapshot(status="draft", complete=True)
                    self.fixture.make_record_reviewed()
                    if status == "open":
                        self.fixture.set_finding(severity, status)
                    else:
                        self.fixture.accept_record_finding(severity)
                    self.fixture.refresh_lifecycle_snapshot_digest()
                    errors = "\n".join(validate(self.root).errors)
                    self.assertIn(
                        f"{status} {severity} review finding blocks reviewed content",
                        errors,
                    )
                    self.assertIn("/ext-1.md:", errors)

    def test_draft_snapshot_and_draft_record_allow_open_high_findings(self) -> None:
        for target in ("snapshot", "record"):
            with self.subTest(target=target):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="draft", complete=True)
                if target == "snapshot":
                    self.fixture.add_open_snapshot_finding("Important")
                else:
                    self.fixture.add_open_finding()
                self.fixture.refresh_lifecycle_snapshot_digest()
                self.assertEqual(validate(self.root).errors, [])

    def test_reviewed_entities_allow_open_or_accepted_minor_and_resolved_high_findings(self) -> None:
        cases = (
            ("snapshot", "open", "Minor"),
            ("snapshot", "accepted", "Minor"),
            ("snapshot", "resolved", "Critical"),
            ("record", "open", "Minor"),
            ("record", "accepted", "Minor"),
            ("record", "resolved", "Important"),
        )
        for target, status, severity in cases:
            with self.subTest(target=target, status=status, severity=severity):
                self.fixture.reset_crosswalks()
                parent_status = "reviewed" if target == "snapshot" else "draft"
                self.fixture.create_valid_snapshot(status=parent_status, complete=True)
                if target == "record":
                    self.fixture.make_record_reviewed()
                affected = [] if target == "snapshot" else None
                self.fixture.set_finding(severity, status, affected_record_ids=affected)
                self.fixture.refresh_lifecycle_snapshot_digest()
                self.assertEqual(validate(self.root).errors, [])

    def test_schema_invalid_finding_fields_return_diagnostics_without_crashing(self) -> None:
        cases = (
            ("severity", ["Critical"], "is not one of"),
            ("affected_record_ids", {"ext-1": True}, "is not of type 'array'"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="reviewed", complete=True)
                self.fixture.add_open_finding()
                self.fixture.set_malformed_finding_field(field, value)
                self.fixture.refresh_lifecycle_snapshot_digest()
                self.assertIn(expected, "\n".join(validate(self.root).errors))

        for field, value, expected in (
            ("status", {"state": "open"}, "is not one of"),
            ("disposition", ["invalid"], "is not of type 'string'"),
        ):
            with self.subTest(field=field, status="approved"):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="approved", complete=True)
                self.fixture.add_open_minor_finding()
                self.fixture.set_malformed_finding_field(field, value)
                self.fixture.refresh_lifecycle_snapshot_digest()
                self.assertIn(expected, "\n".join(validate(self.root).errors))

    def test_reviewed_snapshot_allows_resolved_high_severity_findings(self) -> None:
        for severity in ("Critical", "Important"):
            with self.subTest(severity=severity):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="reviewed", complete=True)
                self.fixture.add_resolved_snapshot_finding(severity)
                self.fixture.refresh_lifecycle_snapshot_digest()
                self.assertEqual(validate(self.root).errors, [])

    def test_record_outside_inventory_is_always_rejected(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        self.fixture.add_record(snapshot, external_provision_id="EXT-99", record_id="ext-99")
        self.assertIn("not present in provision inventory", "\n".join(validate(self.root).errors))

    def test_complete_positive_snapshot_states_are_accepted(self) -> None:
        for status in ("draft", "reviewed", "approved"):
            with self.subTest(status=status):
                self.fixture.reset_crosswalks()
                if status == "approved":
                    self.fixture.create_approved_snapshot_with_lifecycle("approved")
                else:
                    self.fixture.create_valid_snapshot(status=status, complete=True)
                self.assertEqual(validate(self.root).errors, [])

    def test_every_snapshot_state_requires_lifecycle_record(self) -> None:
        for status in ("draft", "reviewed", "approved"):
            with self.subTest(status=status):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(
                    status=status, complete=True, with_lifecycle=False
                )
                self.assertIn(
                    "mapping set requires lifecycle record",
                    "\n".join(validate(self.root).errors),
                )

    def test_declared_subset_and_all_dispositions_are_accepted(self) -> None:
        self.fixture.create_valid_snapshot(
            status="reviewed",
            complete=True,
            scope_type="declared_subset",
            dispositions=("mapped", "no_direct_mapping", "out_of_scope"),
        )
        self.assertEqual(validate(self.root).errors, [])

    def test_validation_result_exposes_loaded_snapshot_model(self) -> None:
        self.fixture.create_valid_snapshot(status="draft", complete=True)
        result = validate(self.root)
        self.assertEqual(len(result.mapping_sets), 1)
        model = result.mapping_sets[0]
        self.assertTrue(model["path"].endswith("/README.md"))
        self.assertEqual(
            model["metadata"]["mapping_set_id"],
            "nist--ai-rmf--1.0--esaf-0.4-alpha--1.0.0",
        )
        self.assertEqual(model["inventory"]["metadata"]["provision_ids"], ["EXT-1"])
        self.assertEqual(model["provisions"][0]["metadata"]["record_id"], "ext-1")
        self.assertTrue(model["provisions"][0]["path"].endswith("/ext-1.md"))

    def test_validate_record_exposes_unqualified_semantic_diagnostics(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        mapping_set, _ = parse_front_matter(snapshot / "README.md")
        record, _ = parse_front_matter(snapshot / "ext-1.md")
        record["relationships"] = []
        self.assertIn(
            "mapped record requires at least one relationship",
            validate_record(record, mapping_set),
        )

    def test_schema_invalid_inventory_is_reported_without_validator_crash(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        inventory_path = snapshot / "PROVISION_INVENTORY.md"
        inventory, body = parse_front_matter(inventory_path)
        inventory["provision_ids"] = [{"invalid": "identifier"}]
        self.fixture.write_front_matter(
            inventory_path.relative_to(self.root).as_posix(), inventory, body
        )
        self.assertIn("is not of type 'string'", "\n".join(validate(self.root).errors))

    def test_schema_invalid_manifest_is_reported_without_validator_crash(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        manifest_path = snapshot / "ESAF_CONTROL_MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["controls"] = None
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        self.assertIn("is not of type 'array'", "\n".join(validate(self.root).errors))

    def test_malformed_yaml_is_reported_for_snapshot_and_record(self) -> None:
        for target in ("README.md", "ext-1.md"):
            with self.subTest(target=target):
                self.fixture.reset_crosswalks()
                snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
                (snapshot / target).write_text(
                    "---\ninvalid: [\n---\n# Broken\n", encoding="utf-8", newline="\n"
                )
                self.assertIn("invalid YAML", "\n".join(validate(self.root).errors))

    def test_non_string_status_is_reported_for_snapshot_and_record(self) -> None:
        for target in ("README.md", "ext-1.md"):
            with self.subTest(target=target):
                self.fixture.reset_crosswalks()
                snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
                path = snapshot / target
                metadata, body = parse_front_matter(path)
                metadata["status"] = {"invalid": "status"}
                self.fixture.write_front_matter(
                    path.relative_to(self.root).as_posix(), metadata, body
                )
                self.assertIn("is not one of", "\n".join(validate(self.root).errors))

    def test_reviewed_text_diagnostics_use_repository_relative_paths(self) -> None:
        self.fixture.create_valid_snapshot(status="approved", complete=True)
        self.fixture.break_local_link()
        errors = [error for error in validate(self.root).errors if "broken local link" in error]
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("crosswalks/mappings/"))
        self.assertNotIn(self.root.as_posix(), errors[0])

    def test_reviewed_inventory_body_mutation_matrix(self) -> None:
        cases = (
            ("break_inventory_local_link", "broken local link"),
            ("add_inventory_drafting_marker", "unresolved drafting marker"),
            (
                "write_inventory_encoding_corruption_signature",
                "possible text-encoding corruption",
            ),
        )
        for mutation, expected in cases:
            with self.subTest(mutation=mutation):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="approved", complete=True)
                getattr(self.fixture, mutation)()
                self.assertIn(expected, "\n".join(validate(self.root).errors))

    def test_identifier_only_context_is_accepted_when_identifiers_are_permitted(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        mapping_path = snapshot / "README.md"
        mapping_set, mapping_body = parse_front_matter(mapping_path)
        mapping_set["publication_rights"]["permitted_elements"] = [
            "identifiers", "structural_inventory", "derivative_mapping_analysis", "official_links"
        ]
        mapping_set["publication_rights"]["prohibited_elements"] = ["titles", "paraphrases"]
        self.fixture.write_front_matter(
            mapping_path.relative_to(self.root).as_posix(), mapping_set, mapping_body
        )
        record_path = snapshot / "ext-1.md"
        record, record_body = parse_front_matter(record_path)
        record["context"] = {
            "mode": "identifier_only",
            "omission_rationale": "Publication rights prohibit a summary.",
        }
        self.fixture.write_front_matter(
            record_path.relative_to(self.root).as_posix(), record, record_body
        )
        self.fixture.refresh_lifecycle_snapshot_digest()
        self.assertEqual(validate(self.root).errors, [])

    def test_record_reviewer_must_differ_from_record_mapper(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="approved", complete=True)
        record_path = snapshot / "ext-1.md"
        record, body = parse_front_matter(record_path)
        record["reviewer"]["id"] = record["mapper"]["id"]
        self.fixture.write_front_matter(record_path.relative_to(self.root).as_posix(), record, body)
        self.assertIn("reviewer must differ from mapper", "\n".join(validate(self.root).errors))

    def test_git_bytes_returns_exact_pinned_object_bytes(self) -> None:
        commit = self.fixture.control_commit
        self.assertIsNotNone(commit)
        expected = subprocess.run(
            ["git", "-C", str(self.root), "show", f"{commit}:controls/IAM/IAM-100.md"],
            check=True,
            capture_output=True,
        ).stdout
        self.assertEqual(git_bytes(self.root, commit, "controls/IAM/IAM-100.md"), expected)

    def test_manifest_regenerates_from_pinned_commit(self) -> None:
        commit = self.fixture.control_commit
        self.assertIsNotNone(commit)
        manifest = build_control_manifest(self.root, commit, "0.4-alpha", None)
        catalog = json.loads(git_bytes(self.root, commit, "controls/catalog.json"))
        self.assertEqual(manifest["source_commit_sha"], commit)
        self.assertEqual(manifest["controls"][0]["id"], "IAM-100")
        self.assertEqual(len(manifest["controls"]), len(catalog["controls"]))
        self.assertEqual(
            [control["id"] for control in manifest["controls"]],
            sorted(control["id"] for control in catalog["controls"]),
        )
        iam_bytes = git_bytes(self.root, commit, "controls/IAM/IAM-100.md")
        self.assertFalse(iam_bytes.endswith(b"\n"))
        self.assertIn("café".encode(), iam_bytes)
        iam = next(control for control in manifest["controls"] if control["id"] == "IAM-100")
        self.assertEqual(iam["record_sha256"], hashlib.sha256(iam_bytes).hexdigest())

    def test_manifest_rejects_dangling_commit_object(self) -> None:
        dangling = self.fixture.dangling_control_commit()
        with self.assertRaisesRegex(ValueError, "pinned commit is unreachable"):
            build_control_manifest(self.root, dangling, "0.4-alpha", None)

    def test_manifest_rejects_branch_as_tag_alias(self) -> None:
        commit = self.fixture.control_commit
        self.assertIsNotNone(commit)
        self.fixture._git("branch", "fixture-release", commit)
        with self.assertRaisesRegex(
            ValueError, "tag alias does not resolve to pinned commit"
        ):
            build_control_manifest(self.root, commit, "0.4-alpha", "fixture-release")

    def test_manifest_rejects_revision_expression_as_tag_alias(self) -> None:
        commit = self.fixture.control_commit
        self.assertIsNotNone(commit)
        self.fixture._git("tag", "fixture-release", commit)
        with self.assertRaisesRegex(ValueError, "tag alias is invalid"):
            build_control_manifest(
                self.root, commit, "0.4-alpha", "fixture-release^{commit}"
            )

    def test_manifest_rejects_ambiguous_version_declarations(self) -> None:
        commit = self.fixture.commit_version_document(
            "# ESAF Version\n\nCurrent Version: **0.4-alpha**\n"
            "Current Version: **9.9**\n"
        )
        with self.assertRaisesRegex(ValueError, "VERSION.md release declaration is ambiguous"):
            build_control_manifest(self.root, commit, "0.4-alpha", None)

    def test_manifest_rejects_malformed_version_declaration(self) -> None:
        commit = self.fixture.commit_version_document(
            "# ESAF Version\n\nCurrent Version: 0.4-alpha\n"
        )
        with self.assertRaisesRegex(ValueError, "VERSION.md release declaration is invalid"):
            build_control_manifest(self.root, commit, "0.4-alpha", None)

    def test_manifest_rendering_is_deterministic_and_matches_fixture_bytes(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        mapping_set, _ = parse_front_matter(snapshot / "README.md")
        release = mapping_set["esaf_release"]
        manifest = build_control_manifest(
            self.root,
            release["source_commit_sha"],
            release["id"],
            release.get("tag_alias"),
        )
        self.assertEqual(
            (snapshot / "ESAF_CONTROL_MANIFEST.json").read_bytes(),
            render_manifest(manifest).encode("utf-8"),
        )

    def test_manifest_rejects_current_tree_substitution(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        self.fixture.mutate_control_after_snapshot(snapshot)
        self.assertIn(
            "manifest differs from regeneration at pinned commit",
            "\n".join(validate(self.root).errors),
        )

    def test_manifest_accepts_tag_alias_resolving_to_pinned_commit(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        commit = self.fixture.control_commit
        self.fixture._git("tag", "fixture-release", commit)
        mapping_path = snapshot / "README.md"
        mapping_set, body = parse_front_matter(mapping_path)
        mapping_set["esaf_release"]["tag_alias"] = "fixture-release"
        self.fixture.write_front_matter(
            mapping_path.relative_to(self.root).as_posix(), mapping_set, body
        )
        manifest_path = snapshot / "ESAF_CONTROL_MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["tag_alias"] = "fixture-release"
        manifest_path.write_text(
            render_manifest(manifest), encoding="utf-8", newline="\n"
        )
        self.fixture.refresh_lifecycle_snapshot_digest()
        self.assertEqual(validate(self.root).errors, [])

    def test_manifest_mutation_matrix(self) -> None:
        cases = (
            ("set_unreachable_commit", "pinned commit is unreachable"),
            ("set_wrong_esaf_release", "VERSION.md release mismatch"),
            ("point_tag_to_other_commit", "tag alias does not resolve to pinned commit"),
            ("alter_catalog_digest", "control catalog digest mismatch"),
            ("alter_control_record_digest", "control record digest mismatch"),
            ("reference_unknown_control", "unresolved ESAF control identifier"),
            ("set_wrong_control_version", "ESAF control version mismatch"),
            ("omit_manifest_control", "manifest differs from regeneration at pinned commit"),
        )
        for mutation, expected in cases:
            with self.subTest(mutation=mutation):
                self.fixture.reset_repository()
                self.fixture.create_valid_snapshot(status="draft", complete=True)
                getattr(self.fixture, mutation)()
                self.assertIn(expected, "\n".join(validate(self.root).errors))

    def test_control_resolution_does_not_trust_injected_manifest_entries(self) -> None:
        self.fixture.create_valid_snapshot(status="draft", complete=True)
        self.fixture.inject_and_reference_unknown_control()
        self.assertIn(
            "unresolved ESAF control identifier IAM-999",
            "\n".join(validate(self.root).errors),
        )

    def test_control_resolution_diagnostic_names_record_path(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        self.fixture.reference_unknown_control()
        expected = f"{(snapshot / 'ext-1.md').relative_to(self.root).as_posix()}: "
        error = next(
            error
            for error in validate(self.root).errors
            if "unresolved ESAF control identifier" in error
        )
        self.assertTrue(error.startswith(expected), error)

    def test_snapshot_and_record_mutation_matrix(self) -> None:
        cases = (
            ("duplicate_mapping_set_id", "duplicate mapping-set id"),
            ("duplicate_record_id", "duplicate record id"),
            ("duplicate_external_provision_id", "duplicate external provision identifier"),
            ("mismatch_snapshot_path", "snapshot path disagrees with metadata"),
            ("mismatch_inventory_scope_type", "mapping-set scope type disagrees with provision inventory"),
            ("mismatch_inventory_scope_statement", "mapping-set scope statement disagrees with provision inventory"),
            ("mismatch_mapping_set_inventory_count", "mapping-set inventory count disagrees with provision inventory"),
            ("mismatch_inventory_expected_count", "inventory expected count disagrees with provision identifiers"),
            ("add_auxiliary_file", "unexpected snapshot entry"),
            ("add_nested_directory", "unexpected snapshot entry"),
            ("add_symbolic_link", "unexpected snapshot entry"),
            ("remove_granularity_exception", "non-requirement granularity requires granularity_exception"),
            ("remove_mapped_relationships", "mapped record requires at least one relationship"),
            ("add_relationship_to_negative", "must not contain relationships"),
            ("remove_negative_rationale", "negative disposition requires negative_rationale"),
            ("duplicate_control_direction_leg", "duplicate relationship leg"),
            ("make_mapper_reviewer_identical", "reviewer must differ from mapper"),
            ("remove_review_metadata", "reviewed content requires review metadata"),
            ("set_unsafe_child_status", "invalid snapshot/provision status combination"),
            ("make_approved_snapshot_empty", "approved snapshot requires at least one provision"),
            ("add_open_finding", "open review finding blocks approval"),
            ("accept_important_finding", "Important findings must be resolved"),
            ("remove_rights_approval", "publication-rights approval is required"),
            ("add_unpermitted_paraphrase", "context exceeds permitted publication elements"),
            ("break_local_link", "broken local link"),
            ("add_reviewed_drafting_marker", "unresolved drafting marker"),
            ("write_utf8_bom", "UTF-8 byte-order mark is prohibited"),
            ("write_crlf", "CR or CRLF line endings are prohibited"),
            ("write_encoding_corruption_signature", "possible text-encoding corruption"),
        )
        for mutation, expected in cases:
            with self.subTest(mutation=mutation):
                self.fixture.reset_crosswalks()
                status = "reviewed" if mutation == "set_unsafe_child_status" else "approved"
                self.fixture.create_valid_snapshot(status=status, complete=True)
                if mutation == "add_symbolic_link" and not self.fixture.symlinks_supported():
                    continue
                getattr(self.fixture, mutation)()
                self.assertIn(expected, "\n".join(validate(self.root).errors))

    def test_mappings_tree_discovery_rejects_every_rogue_entry(self) -> None:
        cases = ("rogue_file", "orphan_directory", "incomplete_snapshot", "nested_directory")
        for case in cases:
            with self.subTest(case=case):
                self.fixture.reset_crosswalks()
                base = self.root / "crosswalks" / "mappings"
                if case == "rogue_file":
                    base.mkdir(parents=True)
                    (base / "source.txt").write_text("restricted source", encoding="utf-8")
                elif case == "orphan_directory":
                    (base / "orphan").mkdir(parents=True)
                elif case == "incomplete_snapshot":
                    (base / "nist" / "1.0" / "0.4-alpha" / "1.0.0").mkdir(parents=True)
                else:
                    snapshot = self.fixture.create_valid_snapshot(status="draft")
                    (snapshot / "nested").mkdir()
                self.assertIn("unexpected mappings-tree entry", "\n".join(validate(self.root).errors))

    def test_mappings_tree_discovery_rejects_symlink_when_supported(self) -> None:
        self.fixture.reset_crosswalks()
        base = self.root / "crosswalks" / "mappings"
        base.mkdir(parents=True)
        target = self.root / "outside"
        target.mkdir()
        link = base / "linked"
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest("directory symlinks unavailable")
        self.assertIn("unexpected mappings-tree entry", "\n".join(validate(self.root).errors))

    def test_duplicate_yaml_keys_fail_closed_for_all_authoritative_documents(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="approved")
        paths_and_needles = (
            (snapshot / "README.md", "status: approved\n", "status: approved\nstatus: draft\n"),
            (snapshot / "PROVISION_INVENTORY.md", "expected_count: 1\n", "expected_count: 1\nexpected_count: 2\n"),
            (snapshot / "ext-1.md", "  mode: paraphrase\n", "  mode: paraphrase\n  mode: identifier_only\n"),
            (self.root / "crosswalks" / "registry" / f"{MAPPING_SET_ID}.md", "snapshot_digest:", "snapshot_digest:"),
        )
        for path, needle, replacement in paths_and_needles:
            with self.subTest(path=path.name):
                original = path.read_text(encoding="utf-8")
                if path.parent.name == "registry":
                    line = next(item for item in original.splitlines() if item.startswith("snapshot_digest:"))
                    replacement = line + "\n" + line
                    needle = line
                path.write_text(original.replace(needle, replacement, 1), encoding="utf-8", newline="\n")
                errors = "\n".join(validate(self.root).errors)
                self.assertIn(path.relative_to(self.root).as_posix(), errors)
                self.assertIn("duplicate YAML key", errors)
                path.write_text(original, encoding="utf-8", newline="\n")

    def test_trusted_baseline_duplicate_yaml_key_fails_closed(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="approved")
        readme = snapshot / "README.md"
        text = readme.read_text(encoding="utf-8")
        readme.write_text(text.replace("status: approved\n", "status: approved\nstatus: draft\n", 1), encoding="utf-8", newline="\n")
        self.fixture._git("add", "crosswalks")
        self.fixture._git("commit", "--quiet", "-m", "Duplicate baseline key")
        baseline = self.fixture._git("rev-parse", "HEAD")
        self.fixture.reset_crosswalks()
        errors = "\n".join(validate(self.root, baseline_ref=baseline).errors)
        self.assertIn("trusted baseline snapshot metadata is malformed", errors)
        self.assertIn("duplicate YAML key", errors)

    def test_trusted_baseline_duplicate_lifecycle_key_fails_closed(self) -> None:
        self.fixture.create_valid_snapshot(status="approved")
        path = self.root / "crosswalks" / "registry" / f"{MAPPING_SET_ID}.md"
        text = path.read_text(encoding="utf-8")
        line = next(item for item in text.splitlines() if item.startswith("snapshot_digest:"))
        path.write_text(text.replace(line, line + "\n" + line, 1), encoding="utf-8", newline="\n")
        self.fixture._git("add", "crosswalks")
        self.fixture._git("commit", "--quiet", "-m", "Duplicate lifecycle baseline key")
        baseline = self.fixture._git("rev-parse", "HEAD")
        self.fixture.reset_crosswalks()
        errors = "\n".join(validate(self.root, baseline_ref=baseline).errors)
        self.assertIn("trusted baseline lifecycle metadata is malformed", errors)
        self.assertIn("duplicate YAML key", errors)

    def test_finding_targets_must_resolve_even_for_drafts(self) -> None:
        self.fixture.create_valid_snapshot(status="draft")
        self.fixture.set_finding("Important", "open", ["missing-record"])
        self.assertIn("finding target missing-record does not resolve", "\n".join(validate(self.root).errors))

    def test_orphan_finding_target_cannot_bypass_review_gate(self) -> None:
        self.fixture.create_valid_snapshot(status="reviewed")
        self.fixture.set_finding("Important", "open", ["missing-record"])
        errors = "\n".join(validate(self.root).errors)
        self.assertIn("finding target missing-record does not resolve", errors)

    def test_lifecycle_events_align_with_snapshot_editorial_state(self) -> None:
        for status in ("draft", "reviewed"):
            with self.subTest(status=status):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status=status)
                self.assertEqual(validate(self.root).errors, [])
                lifecycle = self.fixture._lifecycle()
                event = valid_event()
                self.fixture._omit_empty_optional_event_fields(event)
                event["event_digest"] = event_digest(event)
                lifecycle["events"] = [event]
                self.fixture._write_lifecycle_metadata(lifecycle)
                self.assertIn(f"{status} mapping set requires empty lifecycle events", "\n".join(validate(self.root).errors))
        self.fixture.reset_crosswalks()
        self.fixture.create_valid_snapshot(status="approved")
        lifecycle = self.fixture._lifecycle()
        lifecycle["events"] = []
        self.fixture._write_lifecycle_metadata(lifecycle)
        self.assertIn("approved mapping set requires an approval lifecycle event", "\n".join(validate(self.root).errors))

    def test_lifecycle_links_reject_missing_self_and_nonreciprocal_successors(self) -> None:
        self.fixture.create_approved_snapshot_with_lifecycle("published")
        self.fixture._append_lifecycle_state("deprecated", successor_id="nist--ai-rmf--1.0--esaf-0.4-alpha--1.0.1")
        self.assertIn("successor mapping set does not exist", "\n".join(validate(self.root).errors))
        lifecycle = self.fixture._lifecycle()
        lifecycle["events"][-1]["successor_id"] = MAPPING_SET_ID
        lifecycle["events"][-1]["event_digest"] = event_digest(lifecycle["events"][-1])
        self.fixture._write_lifecycle_metadata(lifecycle)
        self.assertIn("lifecycle link must not reference itself", "\n".join(validate(self.root).errors))

    def test_lifecycle_supersession_links_are_reciprocal_and_consistent(self) -> None:
        self.fixture.create_mixed_catalog_fixture(
            mapping_set_versions=("0.10.0", "0.2.0"),
            lifecycle_states=("deprecated", "published"),
            dispositions=("mapped",),
            include_both_directions=False,
        )
        source_id = "nist--ai-rmf--1.0--esaf-0.4-alpha--0.10.0"
        target_id = "nist--ai-rmf--1.0--esaf-0.4-alpha--0.2.0"
        source_path = self.root / "crosswalks" / "registry" / f"{source_id}.md"
        target_path = self.root / "crosswalks" / "mappings" / "nist" / "1.0" / "0.4-alpha" / "0.2.0" / "README.md"
        source, body = parse_front_matter(source_path)
        source["events"][-1]["successor_id"] = target_id
        source["events"][-1]["event_digest"] = event_digest(source["events"][-1])
        self.fixture.write_front_matter(source_path.relative_to(self.root).as_posix(), source, body)
        self.assertIn("successor link is not reciprocated", "\n".join(validate(self.root).errors))

        target, target_body = parse_front_matter(target_path)
        target["predecessor_id"] = source_id
        self.fixture.write_front_matter(target_path.relative_to(self.root).as_posix(), target, target_body)
        target_registry = self.root / "crosswalks" / "registry" / f"{target_id}.md"
        target_lifecycle, lifecycle_body = parse_front_matter(target_registry)
        target_lifecycle["snapshot_digest"] = snapshot_digest(self.root, target_path.parent)
        self.fixture.write_front_matter(target_registry.relative_to(self.root).as_posix(), target_lifecycle, lifecycle_body)
        self.assertEqual(validate(self.root).errors, [])

        source, body = parse_front_matter(source_path)
        source["events"][0]["successor_id"] = MAPPING_SET_ID
        source["events"][0]["event_digest"] = event_digest(source["events"][0])
        for index in range(1, len(source["events"])):
            source["events"][index]["previous_event_digest"] = source["events"][index - 1]["event_digest"]
            source["events"][index]["event_digest"] = event_digest(source["events"][index])
        self.fixture.write_front_matter(source_path.relative_to(self.root).as_posix(), source, body)
        self.assertIn("conflicting successor mapping-set links", "\n".join(validate(self.root).errors))

    def test_publication_rights_are_partitioned_and_cover_committed_content(self) -> None:
        mutations = (
            ("overlap", lambda rights: rights["prohibited_elements"].append("identifiers"), "must be disjoint"),
            ("omission", lambda rights: rights["prohibited_elements"].remove("titles"), "must exhaustively partition"),
            ("content", lambda rights: (rights["permitted_elements"].remove("paraphrases"), rights["prohibited_elements"].append("paraphrases")), "committed element paraphrases is not permitted"),
        )
        for name, mutation, expected in mutations:
            with self.subTest(name=name):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="draft")
                self.fixture._mutate_mapping_set(lambda value: mutation(value["publication_rights"]))
                self.assertIn(expected, "\n".join(validate(self.root).errors))

    def test_publication_rights_require_explicit_reviewer_attestations(self) -> None:
        self.fixture.create_valid_snapshot(status="draft")
        self.fixture._mutate_mapping_set(
            lambda value: value["publication_rights"].pop("reviewer_authorized_source_access", None)
        )
        self.assertIn("reviewer_authorized_source_access", "\n".join(validate(self.root).errors))

    def test_publication_rights_cover_each_committed_element(self) -> None:
        for element in ("identifiers", "structural_inventory", "official_links", "derivative_mapping_analysis", "paraphrases"):
            with self.subTest(element=element):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="draft")
                def prohibit(value: dict[str, object]) -> None:
                    rights = value["publication_rights"]
                    rights["permitted_elements"].remove(element)
                    rights["prohibited_elements"].append(element)
                self.fixture._mutate_mapping_set(prohibit)
                self.assertIn(f"committed element {element} is not permitted", "\n".join(validate(self.root).errors))
        self.fixture.reset_crosswalks()
        snapshot = self.fixture.create_valid_snapshot(status="draft")
        record, body = parse_front_matter(snapshot / "ext-1.md")
        record["title"] = "Permitted title required"
        self.fixture.write_front_matter((snapshot / "ext-1.md").relative_to(self.root).as_posix(), record, body)
        self.assertIn("committed element titles is not permitted", "\n".join(validate(self.root).errors))

    def test_draft_text_rejects_broken_links_and_encoding_corruption(self) -> None:
        for mutation, expected in (("break_local_link", "broken local link"), ("write_encoding_corruption_signature", "possible text-encoding corruption")):
            with self.subTest(mutation=mutation):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="draft")
                getattr(self.fixture, mutation)()
                self.assertIn(expected, "\n".join(validate(self.root).errors))

    def test_impossible_dates_and_decreasing_lifecycle_dates_are_rejected(self) -> None:
        for target in ("mapping-set", "record", "lifecycle"):
            with self.subTest(target=target):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status="approved" if target == "lifecycle" else "draft")
                if target == "mapping-set":
                    self.fixture._mutate_mapping_set(lambda value: value["mapper"].__setitem__("date", "2026-02-30"))
                elif target == "record":
                    self.fixture._mutate_record(lambda value: value["mapper"].__setitem__("date", "2026-02-30"))
                else:
                    lifecycle = self.fixture._lifecycle()
                    lifecycle["events"][0]["date"] = "2026-02-30"
                    lifecycle["events"][0]["event_digest"] = event_digest(lifecycle["events"][0])
                    self.fixture._write_lifecycle_metadata(lifecycle)
                self.assertIn("2026-02-30", "\n".join(validate(self.root).errors))
        self.fixture.reset_crosswalks()
        self.fixture.create_approved_snapshot_with_lifecycle("published")
        lifecycle = self.fixture._lifecycle()
        lifecycle["events"][1]["date"] = "2026-07-12"
        lifecycle["events"][1]["event_digest"] = event_digest(lifecycle["events"][1])
        self.fixture._write_lifecycle_metadata(lifecycle)
        self.assertIn("lifecycle event dates must be nondecreasing", "\n".join(validate(self.root).errors))

    def test_mappings_root_symlink_is_rejected_before_exists_or_traversal(self) -> None:
        with mock.patch.object(Path, "is_symlink", return_value=True), mock.patch.object(
            Path, "exists", side_effect=AssertionError("exists must not be queried")
        ):
            errors = _validate_mappings_tree(self.root)
        self.assertIn("crosswalks/mappings: unexpected mappings-tree entry", errors)

    def test_actual_mappings_root_symlink_is_rejected_when_supported(self) -> None:
        crosswalks = self.root / "crosswalks"
        crosswalks.mkdir()
        external = self.root / "external"
        external.mkdir()
        try:
            (crosswalks / "mappings").symlink_to(external, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"directory symlinks unavailable: {error}")
        self.assertIn(
            "crosswalks/mappings: unexpected mappings-tree entry",
            _validate_mappings_tree(self.root),
        )

    def test_local_markdown_links_must_remain_inside_repository(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        record_path = snapshot / "ext-1.md"
        metadata, body = parse_front_matter(record_path)
        outside = self.root.parent / f"{self.root.name}-outside.md"
        outside.write_text("outside", encoding="utf-8")
        try:
            for label, target in (
                ("parent escape", os.path.relpath(outside, record_path.parent).replace("\\", "/")),
                ("absolute", outside.as_posix()),
            ):
                with self.subTest(label=label):
                    self.fixture.write_front_matter(
                        record_path.relative_to(self.root).as_posix(), metadata, body + f"\n[x]({target})\n"
                    )
                    self.fixture.refresh_lifecycle_snapshot_digest()
                    self.assertIn("local link escapes repository", "\n".join(validate(self.root).errors))
        finally:
            outside.unlink(missing_ok=True)

    def test_local_markdown_links_accept_repository_anchor_and_external_targets(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        record_path = snapshot / "ext-1.md"
        target = self.root / "docs" / "target.md"
        target.parent.mkdir()
        target.write_text("target", encoding="utf-8")
        relative_target = os.path.relpath(target, record_path.parent).replace("\\", "/")
        metadata, body = parse_front_matter(record_path)
        self.fixture.write_front_matter(
            record_path.relative_to(self.root).as_posix(),
            metadata,
            body + f"\n[in repo]({relative_target}) [anchor](#heading) [web](https://example.com/x)\n",
        )
        self.fixture.refresh_lifecycle_snapshot_digest()
        errors = "\n".join(validate(self.root).errors)
        self.assertNotIn("broken local link", errors)
        self.assertNotIn("local link escapes repository", errors)

    def test_local_markdown_link_rejects_symlink_escape_when_supported(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        record_path = snapshot / "ext-1.md"
        outside = self.root.parent / f"{self.root.name}-outside.md"
        outside.write_text("outside", encoding="utf-8")
        link = self.root / "linked-outside.md"
        try:
            try:
                link.symlink_to(outside)
            except OSError as error:
                self.skipTest(f"file symlinks unavailable: {error}")
            metadata, body = parse_front_matter(record_path)
            target = os.path.relpath(link, record_path.parent).replace("\\", "/")
            self.fixture.write_front_matter(
                record_path.relative_to(self.root).as_posix(), metadata, body + f"\n[x]({target})\n"
            )
            self.fixture.refresh_lifecycle_snapshot_digest()
            self.assertIn("local link escapes repository", "\n".join(validate(self.root).errors))
        finally:
            link.unlink(missing_ok=True)
            outside.unlink(missing_ok=True)

    def test_complex_yaml_keys_fail_closed_with_deterministic_diagnostic(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        paths = (
            snapshot / "README.md",
            snapshot / "ext-1.md",
            snapshot / "PROVISION_INVENTORY.md",
            self.root / "crosswalks" / "registry" / f"{MAPPING_SET_ID}.md",
        )
        for index, path in enumerate(paths):
            with self.subTest(path=path.name):
                raw = path.read_text(encoding="utf-8")
                key = "? [a, b]\n: value\n" if index % 2 == 0 else "? {a: b}\n: value\n"
                path.write_text(raw.replace("---\n", "---\n" + key, 1), encoding="utf-8", newline="\n")
                self.assertIn("YAML mapping keys must be scalar and hashable", "\n".join(validate(self.root).errors))
                self.fixture.reset_crosswalks()
                snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)

    def test_trusted_baseline_complex_yaml_key_fails_closed(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="approved", complete=True)
        readme = snapshot / "README.md"
        raw = readme.read_text(encoding="utf-8")
        readme.write_text(
            raw.replace("---\n", "---\n? {a: b}\n: value\n", 1),
            encoding="utf-8",
            newline="\n",
        )
        self.fixture._git("add", "crosswalks")
        self.fixture._git("commit", "--quiet", "-m", "Complex baseline key")
        baseline = self.fixture._git("rev-parse", "HEAD")
        self.fixture.reset_crosswalks()
        errors = "\n".join(validate(self.root, baseline_ref=baseline).errors)
        self.assertIn("trusted baseline snapshot metadata is malformed", errors)
        self.assertIn("YAML mapping keys must be scalar and hashable", errors)

    def test_duplicate_finding_ids_are_rejected_and_malformed_ids_do_not_crash(self) -> None:
        self.fixture.create_valid_snapshot(status="draft", complete=True)
        self.fixture.set_finding("Minor", "resolved")
        def duplicate(value: dict[str, object]) -> None:
            finding = copy.deepcopy(value["findings"][0])
            value["findings"].append(finding)
        self.fixture._mutate_mapping_set(duplicate)
        self.assertIn("duplicate finding id", "\n".join(validate(self.root).errors))
        self.fixture._mutate_mapping_set(lambda value: value["findings"][0].__setitem__("finding_id", []))
        self.assertIsInstance(validate(self.root).errors, list)

    def test_mojibake_detection_is_precise(self) -> None:
        for text in ("\u00c2ge et s\u00e9curit\u00e9", "\u00c3", "\u00c2"):
            with self.subTest(text=text):
                self.fixture.reset_crosswalks()
                snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
                path = snapshot / "ext-1.md"
                metadata, body = parse_front_matter(path)
                self.fixture.write_front_matter(path.relative_to(self.root).as_posix(), metadata, body + "\n" + text)
                self.fixture.refresh_lifecycle_snapshot_digest()
                self.assertNotIn("possible text-encoding corruption", "\n".join(validate(self.root).errors))
        for text in (
            "caf\u00c3\u0192\u00c2\u00a9",
            "Fran\u00c3\u00a7ais",
            "Espa\u00c3\u00b1a",
            "\u00e2\u20ac\u02dc",
            "\u00e2\u20ac\u00a6",
            "\u00e2\u20ac\u2122",
            "\ufffd",
        ):
            with self.subTest(text=text):
                self.fixture.reset_crosswalks()
                snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
                path = snapshot / "ext-1.md"
                metadata, body = parse_front_matter(path)
                self.fixture.write_front_matter(path.relative_to(self.root).as_posix(), metadata, body + "\n" + text)
                self.assertIn("possible text-encoding corruption", "\n".join(validate(self.root).errors))


if __name__ == "__main__":
    unittest.main()
