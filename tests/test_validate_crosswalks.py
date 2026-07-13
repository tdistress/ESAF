import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.crosswalk_fixtures import CrosswalkFixture, valid_event
from tools.crosswalks.digests import event_bytes, event_digest
from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.manifest import build_control_manifest, git_bytes, render_manifest
from tools.crosswalks.validation import validate, validate_record


class CrosswalkValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.fixture = CrosswalkFixture(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

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

    def test_incomplete_reviewed_snapshot_is_rejected(self) -> None:
        self.fixture.create_valid_snapshot(status="reviewed", complete=False)
        errors = validate(self.root).errors
        self.assertIn("missing provision record for inventory identifier EXT-2", "\n".join(errors))

    def test_record_outside_inventory_is_always_rejected(self) -> None:
        snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
        self.fixture.add_record(snapshot, external_provision_id="EXT-99", record_id="ext-99")
        self.assertIn("not present in provision inventory", "\n".join(validate(self.root).errors))

    def test_complete_positive_snapshot_states_are_accepted(self) -> None:
        for status in ("draft", "reviewed", "approved"):
            with self.subTest(status=status):
                self.fixture.reset_crosswalks()
                self.fixture.create_valid_snapshot(status=status, complete=True)
                self.assertEqual(validate(self.root).errors, [])

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
        mapping_set["publication_rights"]["permitted_elements"] = ["identifiers"]
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


if __name__ == "__main__":
    unittest.main()
