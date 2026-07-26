from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import tools.build_mapping_review_bundle as bundle_builder
import tools.validate_crosswalks as crosswalk_validator
import tools.crosswalks.catalog as crosswalk_catalog
from tools.build_mapping_review_bundle import (
    PROFILES,
    GitReader,
    MappingProfile,
    PackageFile,
    assemble_package,
    collect_package_files,
    main,
    parse_front_matter_bytes,
    validate_output_directory,
    write_package,
)
from tools.crosswalks.digests import snapshot_digest_from_files


ROOT = Path(__file__).resolve().parents[1]
PLAN = (
    ROOT
    / "docs/superpowers/plans/2026-07-23-uk-qualified-review-preparation.md"
)
CORE_ID = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure"
    "--3.3--esaf-0.4-alpha--0.1.0"
)
PLUS_FORWARD_ID = (
    "uk-ncsc--cyber-essentials-plus-test-specification"
    "--3.2--esaf-0.4-alpha--0.1.0"
)
PLUS_REVERSE_ID = (
    "uk-ncsc--cyber-essentials-plus-test-specification"
    "--3.2--esaf-0.4-alpha--0.2.0"
)
EXPECTED_SOURCE_EVIDENCE = {
    CORE_ID: (
        "e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923",
    ),
    PLUS_FORWARD_ID: (
        "docs/superpowers/specs/"
        "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json",
        "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc",
        "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8",
        "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694",
        "https://www.ncsc.gov.uk/cyberessentials/resources",
        "https://www.ncsc.gov.uk/files/"
        "cyber-essentials-plus-test-specification-v3-2.pdf",
    ),
    PLUS_REVERSE_ID: (
        "docs/superpowers/specs/"
        "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json",
        "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc",
        "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8",
        "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694",
        "https://www.ncsc.gov.uk/cyberessentials/resources",
        "https://www.ncsc.gov.uk/files/"
        "cyber-essentials-plus-test-specification-v3-2.pdf",
    ),
}


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _create_clean_repository(parent: Path) -> tuple[Path, str]:
    repository = parent / "repository"
    repository.mkdir()
    _git(repository, "init")
    _git(repository, "config", "user.name", "ESAF Test")
    _git(repository, "config", "user.email", "esaf-test@example.invalid")
    (repository / "tracked.txt").write_text("baseline\n", encoding="utf-8")
    _git(repository, "add", "tracked.txt")
    _git(repository, "commit", "-m", "test baseline")
    return repository, _git(repository, "rev-parse", "HEAD")


class GitReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = GitReader(ROOT)
        self.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()

    def test_profiles_are_exact_and_separate(self) -> None:
        self.assertEqual(
            {profile.expected_count for profile in PROFILES.values()},
            {116, 144},
        )
        self.assertEqual(len(PROFILES), 3)
        self.assertEqual(
            {
                mapping_set_id: profile.direction
                for mapping_set_id, profile in PROFILES.items()
            },
            {
                CORE_ID: "esaf_to_external",
                PLUS_FORWARD_ID: "esaf_to_external",
                PLUS_REVERSE_ID: "external_to_esaf",
            },
        )
        self.assertEqual(
            {profile.label for profile in PROFILES.values()},
            {"Core", "Plus forward", "Plus reverse"},
        )

    def test_implementation_plan_uses_authoritative_core_direction(self) -> None:
        self.assertIn(
            '"Core", "esaf_to_external", 116,',
            PLAN.read_text(encoding="utf-8"),
        )

    def test_resolve_commit_requires_full_exact_sha(self) -> None:
        self.assertEqual(self.reader.resolve_commit(self.head), self.head)
        for invalid in ("HEAD", self.head[:12], "g" * 40, "0" * 40):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    self.reader.resolve_commit(invalid)

    def test_reads_blob_and_lists_tree_from_commit(self) -> None:
        data = self.reader.read_bytes(self.head, "crosswalks/ESAF-1600.md")
        self.assertTrue(data.startswith(b"# ESAF-1600 Standards Crosswalk Methodology"))
        paths = self.reader.list_files(self.head, "crosswalks/schema")
        self.assertIn("crosswalks/schema/mapping-set.schema.json", paths)
        self.assertEqual(paths, tuple(sorted(paths)))

    def test_read_bytes_rejects_unsafe_repository_paths(self) -> None:
        for unsafe in (
            "/absolute/path",
            "../parent/path",
            "crosswalks\\schema\\mapping-set.schema.json",
            "C:drive-relative",
        ):
            with self.subTest(path=unsafe):
                with self.assertRaisesRegex(ValueError, "unsafe repository path"):
                    self.reader.read_bytes(self.head, unsafe)

    def test_read_bytes_rejects_non_regular_git_blob_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, _head = _create_clean_repository(Path(directory))
            blob = subprocess.run(
                ["git", "hash-object", "-w", "--stdin"],
                cwd=repository,
                input=b"tracked.txt",
                check=True,
                capture_output=True,
            ).stdout.decode("ascii").strip()
            _git(
                repository,
                "update-index",
                "--add",
                "--cacheinfo",
                f"120000,{blob},fixed-evidence.md",
            )
            _git(repository, "commit", "-m", "add non-regular evidence")
            head = _git(repository, "rev-parse", "HEAD")
            with self.assertRaisesRegex(
                ValueError,
                "unexpected repository entry",
            ):
                GitReader(repository).read_bytes(
                    head,
                    "fixed-evidence.md",
                )

    def test_reports_all_worktree_roots_as_resolved_paths(self) -> None:
        roots = self.reader.worktree_roots()
        self.assertIn(ROOT.resolve(), roots)
        self.assertTrue(all(path.is_absolute() for path in roots))


class CandidateExecutionStateTests(unittest.TestCase):
    def test_accepts_clean_repository_at_candidate_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, head = _create_clean_repository(Path(directory))
            GitReader(repository).require_candidate_execution_state(head)

    def test_rejects_dirty_tracked_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, head = _create_clean_repository(Path(directory))
            (repository / "tracked.txt").write_text("changed\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "repository must be clean"):
                GitReader(repository).require_candidate_execution_state(head)

    def test_rejects_dirty_untracked_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, head = _create_clean_repository(Path(directory))
            (repository / "untracked.txt").write_text("untracked\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "repository must be clean"):
                GitReader(repository).require_candidate_execution_state(head)

    def test_rejects_candidate_that_is_not_current_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, first = _create_clean_repository(Path(directory))
            (repository / "tracked.txt").write_text("second\n", encoding="utf-8")
            _git(repository, "add", "tracked.txt")
            _git(repository, "commit", "-m", "second")
            with self.assertRaisesRegex(ValueError, "current HEAD must equal candidate"):
                GitReader(repository).require_candidate_execution_state(first)


class GeneratorCheckoutBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.profile = PROFILES[CORE_ID]

    def test_writer_rejects_reader_from_different_checkout(self) -> None:
        module_reader = GitReader(ROOT)
        mapping_set_path = f"{self.profile.snapshot_path}/README.md"
        minimal_files = (
            PackageFile(
                mapping_set_path,
                module_reader.read_bytes(self.head, mapping_set_path),
                "mapping set",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository, foreign_head = _create_clean_repository(root)
            output = root / "package"
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=minimal_files,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "reader root must equal module checkout",
                ):
                    write_package(
                        GitReader(repository),
                        foreign_head,
                        self.profile,
                        output,
                    )

    def test_writer_uses_fresh_module_checkout_for_execution_state(
        self,
    ) -> None:
        caller = GitReader(ROOT)
        caller_check = mock.Mock()
        caller.require_candidate_execution_state = caller_check
        mapping_set_path = f"{self.profile.snapshot_path}/README.md"
        minimal_files = (
            PackageFile(
                mapping_set_path,
                caller.read_bytes(self.head, mapping_set_path),
                "mapping set",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=minimal_files,
            ), mock.patch.object(
                GitReader,
                "require_candidate_execution_state",
                autospec=True,
            ) as module_check:
                write_package(
                    caller,
                    self.head,
                    self.profile,
                    Path(directory) / "package",
                )
        caller_check.assert_not_called()
        self.assertEqual(module_check.call_count, 2)
        for call in module_check.call_args_list:
            checked_reader, checked_commit = call.args
            self.assertIsNot(checked_reader, caller)
            self.assertEqual(checked_reader.root, ROOT)
            self.assertEqual(checked_commit, self.head)


class PackagePopulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reader = GitReader(ROOT)
        cls.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()

    def test_every_profile_collects_exact_population_and_dependencies(self) -> None:
        for profile in PROFILES.values():
            with self.subTest(profile=profile.label):
                files = collect_package_files(self.reader, self.head, profile)
                paths = {item.path for item in files}
                record_prefix = f"{profile.snapshot_path}/"
                record_paths = {
                    path for path in paths
                    if path.startswith(record_prefix)
                    and path.endswith(".md")
                    and not path.endswith("/README.md")
                    and not path.endswith("/PROVISION_INVENTORY.md")
                }
                self.assertEqual(len(record_paths), profile.expected_count)
                for required in (
                    f"{profile.snapshot_path}/README.md",
                    f"{profile.snapshot_path}/PROVISION_INVENTORY.md",
                    f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json",
                    f"crosswalks/registry/{profile.mapping_set_id}.md",
                    "crosswalks/ESAF-1600.md",
                    "crosswalks/schema/mapping-set.schema.json",
                    "crosswalks/schema/mapping-record.schema.json",
                    "crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md",
                    "crosswalks/reviews/templates/REVIEWER_ATTESTATION.md",
                    "review-metadata/catalog-entry.json",
                ):
                    self.assertIn(required, paths)

    def test_collected_controls_match_manifest_paths_and_digests(self) -> None:
        for profile in PROFILES.values():
            files = collect_package_files(self.reader, self.head, profile)
            by_path = {item.path: item.content for item in files}
            manifest = json.loads(
                by_path[f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"]
            )
            for control in manifest["controls"]:
                packaged_path = f"controls/{control['path']}"
                self.assertEqual(
                    hashlib.sha256(by_path[packaged_path]).hexdigest(),
                    control["record_sha256"],
                )

    def test_controls_are_read_from_manifest_pinned_historical_commit(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class TrackingReader:
            def __init__(self) -> None:
                self.reads: list[tuple[str, str]] = []

            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                self.reads.append((commit, path))
                return base.read_bytes(commit, path)

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        reader = TrackingReader()
        files = collect_package_files(reader, self.head, profile)
        by_path = {item.path: item.content for item in files}
        manifest = json.loads(
            by_path[f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"]
        )
        source_commit = manifest["source_commit_sha"]
        control_paths = {
            f"controls/{control['path']}" for control in manifest["controls"]
        }
        historical_paths = control_paths | {"controls/catalog.json"}
        self.assertEqual(
            {
                commit
                for commit, path in reader.reads
                if path in historical_paths
            },
            {source_commit},
        )
        self.assertEqual(
            {
                commit
                for commit, path in reader.reads
                if path not in historical_paths
            },
            {self.head},
        )

    def test_collector_accepts_prose_draft_registry(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == f"crosswalks/registry/{profile.mapping_set_id}.md":
                    front_matter, body = content.split(b"---\n", 2)[1:]
                    body = body.replace(b"Draft", b"Pre-review")
                    body = body.replace(b"draft", b"pre-review")
                    return b"---\n" + front_matter + b"---\n" + body
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        files = collect_package_files(MutatingReader(), self.head, profile)
        self.assertIn(
            f"crosswalks/registry/{profile.mapping_set_id}.md",
            {item.path for item in files},
        )

    def test_collector_rejects_unexpected_snapshot_artifact(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader
        unexpected = f"{profile.snapshot_path}/NOTES.txt"

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                return b"unexpected\n" if path == unexpected else base.read_bytes(commit, path)

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return tuple(sorted((*base.list_files(commit, path), unexpected)))

        with self.assertRaisesRegex(ValueError, "unexpected snapshot entry"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_registry_snapshot_digest_drift(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader
        registry_path = f"crosswalks/registry/{profile.mapping_set_id}.md"

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == registry_path:
                    return re.sub(
                        rb"(?m)^snapshot_digest: [0-9a-f]{64}$",
                        b"snapshot_digest: " + b"0" * 64,
                        content,
                        count=1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "snapshot digest mismatch"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_control_catalog_digest_drift(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader
        manifest_path = f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == manifest_path:
                    manifest = json.loads(content)
                    manifest["control_catalog_sha256"] = "0" * 64
                    return (json.dumps(manifest, sort_keys=True) + "\n").encode()
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "control catalog digest mismatch"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_consistently_rehashed_incomplete_manifest(
        self,
    ) -> None:
        profile = PROFILES[CORE_ID]
        base = self.reader
        manifest_path = f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"
        registry_path = f"crosswalks/registry/{profile.mapping_set_id}.md"
        snapshot_contents = {
            path: base.read_bytes(self.head, path)
            for path in base.list_files(self.head, profile.snapshot_path)
        }
        manifest = json.loads(snapshot_contents[manifest_path])
        removed = manifest["controls"].pop()
        self.assertEqual(removed["id"], "STR-130")
        snapshot_contents[manifest_path] = bundle_builder.canonical_json_bytes(
            manifest
        )
        replacement_digest = snapshot_digest_from_files(
            profile.snapshot_path,
            snapshot_contents,
        )
        registry = re.sub(
            rb"(?m)^snapshot_digest: [0-9a-f]{64}$",
            f"snapshot_digest: {replacement_digest}".encode("ascii"),
            base.read_bytes(self.head, registry_path),
            count=1,
        )
        catalog = json.loads(
            base.read_bytes(self.head, "crosswalks/catalog.json")
        )
        catalog_entry = next(
            item
            for item in catalog["mapping_sets"]
            if item["metadata"]["mapping_set_id"] == profile.mapping_set_id
        )
        catalog_entry["lifecycle"]["snapshot_digest"] = replacement_digest
        catalog_bytes = bundle_builder.canonical_json_bytes(catalog)

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                if path == manifest_path:
                    return snapshot_contents[manifest_path]
                if path == registry_path:
                    return registry
                if path == "crosswalks/catalog.json":
                    return catalog_bytes
                return base.read_bytes(commit, path)

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(
            ValueError,
            "control manifest differs from deterministic regeneration",
        ):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_source_evidence_digest_drift(self) -> None:
        profile = PROFILES[PLUS_FORWARD_ID]
        base = self.reader
        oracle_path = (
            "docs/superpowers/specs/"
            "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
        )

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == oracle_path:
                    return content.replace(
                        b'"access_date": "2026-07-14"',
                        b'"access_date": "2026-07-15"',
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(
            ValueError,
            "source evidence digest mismatch",
        ):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_source_evidence_identity_matches_mapping_metadata(self) -> None:
        profile = PROFILES[PLUS_FORWARD_ID]
        readme = self.reader.read_bytes(
            self.head,
            f"{profile.snapshot_path}/README.md",
        )
        metadata, _ = parse_front_matter_bytes(readme)
        oracle_path = (
            "docs/superpowers/specs/"
            "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
        )
        oracle = json.loads(self.reader.read_bytes(self.head, oracle_path))
        oracle["source"]["version"] = "3.1"
        payload = PackageFile(
            oracle_path,
            json.dumps(oracle, sort_keys=True).encode("utf-8"),
            "source evidence pin",
        )
        with self.assertRaisesRegex(
            ValueError,
            "source evidence identity mismatch",
        ):
            bundle_builder._validate_source_evidence_identity(
                payload,
                metadata,
            )

    def test_collector_rejects_same_count_catalog_status_substitution(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == "crosswalks/catalog.json":
                    catalog = json.loads(content)
                    entry = next(
                        item
                        for item in catalog["mapping_sets"]
                        if item["metadata"]["mapping_set_id"]
                        == profile.mapping_set_id
                    )
                    entry["provisions"][0]["metadata"]["status"] = "reviewed"
                    return (json.dumps(catalog, sort_keys=True) + "\n").encode()
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "catalog entry mismatch"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_relationship_direction_drift(self) -> None:
        profile = PROFILES[PLUS_FORWARD_ID]
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if (
                    path.startswith(f"{profile.snapshot_path}/")
                    and path.endswith(".md")
                ):
                    return content.replace(
                        b'"direction": "esaf_to_external"',
                        b'"direction": "external_to_esaf"',
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "relationship direction mismatch"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_nonempty_registry_events(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == f"crosswalks/registry/{profile.mapping_set_id}.md":
                    return content.replace(
                        b"events: []",
                        b"events:\n  - reviewed",
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(
            ValueError,
            "registry lifecycle event array must be empty",
        ):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_population_or_status_drift(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path.endswith("/README.md"):
                    return content.replace(b"status: draft", b"status: reviewed", 1)
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "candidate schema validation"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_reviewer_metadata_on_draft_mapping_set(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == f"{profile.snapshot_path}/README.md":
                    return content.replace(
                        b"status: draft\n",
                        b"status: draft\nreviewer: Example Reviewer\n",
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "candidate schema validation"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_reviewer_metadata_on_draft_mapping_record(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if (
                    path.startswith(f"{profile.snapshot_path}/")
                    and path.endswith(".md")
                    and not path.endswith("/README.md")
                    and not path.endswith("/PROVISION_INVENTORY.md")
                ):
                    return content.replace(
                        b'  "status": "draft",\n',
                        b'  "status": "draft",\n'
                        b'  "reviewer": {"id": "example-reviewer"},\n',
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "candidate schema validation"):
            collect_package_files(MutatingReader(), self.head, profile)


class ReviewedCandidateAssemblyTests(unittest.TestCase):
    """Exercise reviewed candidate content from a real isolated Git repository."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.shared_temporary = tempfile.TemporaryDirectory()
        cls.base_repository = Path(cls.shared_temporary.name) / "reviewed-candidate"
        subprocess.run(
            ["git", "clone", "--no-hardlinks", str(ROOT), str(cls.base_repository)],
            check=True,
            capture_output=True,
            text=True,
        )
        _git(cls.base_repository, "config", "user.name", "ESAF Test")
        _git(cls.base_repository, "config", "user.email", "esaf-test@example.invalid")
        fixture = cls("runTest")
        fixture.repository = cls.base_repository
        fixture.profile = PROFILES[CORE_ID]
        fixture._make_reviewed_candidate()
        cls.base_head = fixture._commit("reviewed candidate")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.shared_temporary.cleanup()

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repository = Path(self.temporary.name) / "reviewed-candidate"
        subprocess.run(
            ["git", "clone", "--no-hardlinks", str(self.base_repository), str(self.repository)],
            check=True,
            capture_output=True,
            text=True,
        )
        _git(self.repository, "config", "user.name", "ESAF Test")
        _git(self.repository, "config", "user.email", "esaf-test@example.invalid")
        self.profile = PROFILES[CORE_ID]
        self.head = self.base_head
        self.reader = GitReader(self.repository)
        self._candidate_index = 0

    def _fresh_candidate(self) -> None:
        self._candidate_index += 1
        self.repository = (
            Path(self.temporary.name) / f"reviewed-candidate-{self._candidate_index}"
        )
        subprocess.run(
            ["git", "clone", "--no-hardlinks", str(self.base_repository), str(self.repository)],
            check=True,
            capture_output=True,
            text=True,
        )
        _git(self.repository, "config", "user.name", "ESAF Test")
        _git(self.repository, "config", "user.email", "esaf-test@example.invalid")
        self.head = _git(self.repository, "rev-parse", "HEAD")
        self.reader = GitReader(self.repository)

    def _commit(self, message: str) -> str:
        _git(self.repository, "add", "--all")
        _git(self.repository, "commit", "-m", message)
        return _git(self.repository, "rev-parse", "HEAD")

    def _front_matter(self, path: Path) -> tuple[dict[str, object], str]:
        return parse_front_matter_bytes(path.read_bytes())

    def _write_front_matter(
        self,
        path: Path,
        metadata: dict[str, object],
        body: str,
    ) -> None:
        rendered = yaml.safe_dump(
            metadata,
            allow_unicode=True,
            sort_keys=False,
        )
        path.write_text(
            f"---\n{rendered}---\n{body}",
            encoding="utf-8",
            newline="\n",
        )

    @staticmethod
    def _reviewer() -> dict[str, object]:
        return {
            "id": "independent-reviewer",
            "qualification": "Qualified independent mapping reviewer",
            "date": "2026-07-25",
            "authorized_source_access": True,
            "findings_disposition": "No Critical or Important findings remain.",
        }

    def _snapshot_paths(self) -> list[Path]:
        return sorted((self.repository / self.profile.snapshot_path).glob("*"))

    def _make_reviewed_candidate(self) -> None:
        snapshot = self.repository / self.profile.snapshot_path
        for path in self._snapshot_paths():
            if path.name in {"PROVISION_INVENTORY.md", "ESAF_CONTROL_MANIFEST.json"}:
                continue
            metadata, body = self._front_matter(path)
            metadata["status"] = "reviewed"
            metadata["reviewer"] = self._reviewer()
            self._write_front_matter(path, metadata, body)
        snapshot_contents = {
            path.relative_to(self.repository).as_posix(): path.read_bytes()
            for path in self._snapshot_paths()
        }
        digest = snapshot_digest_from_files(self.profile.snapshot_path, snapshot_contents)
        registry = self.repository / "crosswalks" / "registry" / f"{CORE_ID}.md"
        metadata, body = self._front_matter(registry)
        metadata["snapshot_digest"] = digest
        self._write_front_matter(registry, metadata, body)
        result = crosswalk_validator.main(["--write"], root=self.repository)
        self.assertEqual(result, 0)

    def _replace_metadata(
        self,
        relative: str,
        update: object,
    ) -> None:
        path = self.repository / relative
        metadata, body = self._front_matter(path)
        update(metadata)
        self._write_front_matter(path, metadata, body)

    def _record_relative(self) -> str:
        for path in self._snapshot_paths():
            if path.name not in {
                "README.md",
                "PROVISION_INVENTORY.md",
                "ESAF_CONTROL_MANIFEST.json",
            }:
                return path.relative_to(self.repository).as_posix()
        self.fail("review fixture has no mapping record")

    def _assemble_after(self, relative: str, update: object) -> None:
        self._replace_metadata(relative, update)
        head = self._commit("mutate reviewed candidate")
        bundle_builder.assemble_package(
            GitReader(self.repository),
            head,
            self.profile,
            "reviewed",
        )

    def test_reviewed_candidate_assembles_and_renders_review_boundary(self) -> None:
        assembly = bundle_builder.assemble_package(
            self.reader,
            self.head,
            self.profile,
            "reviewed",
        )
        self.assertEqual(assembly.manifest["candidate_state"], "reviewed")
        index = next(
            item.content.decode("utf-8")
            for item in assembly.payloads
            if item.path == "PACKAGE_INDEX.md"
        )
        self.assertIn("| Candidate state | `reviewed` |", index)
        self.assertIn("reviewed but is not approved, published", index)

    def test_reviewed_candidate_rejects_mixed_or_approved_states(self) -> None:
        for label, relative, update, message in (
            (
                "mixed-record",
                self._record_relative(),
                lambda metadata: metadata.update(status="draft"),
                "must be reviewed",
            ),
            (
                "approved-snapshot",
                f"{self.profile.snapshot_path}/README.md",
                lambda metadata: metadata.update(status="approved"),
                "candidate schema validation",
            ),
            (
                "approved-record",
                self._record_relative(),
                lambda metadata: metadata.update(status="approved"),
                "candidate schema validation",
            ),
        ):
            with self.subTest(label=label):
                self._fresh_candidate()
                with self.assertRaisesRegex(ValueError, message):
                    self._assemble_after(relative, update)

    def _test_reviewed_candidate_rejects_missing_reviewer_metadata(self) -> None:
        for label, relative in (
            ("snapshot", f"{self.profile.snapshot_path}/README.md"),
            ("record", self._record_relative()),
        ):
            with self.subTest(label=label):
                self._fresh_candidate()
                with self.assertRaisesRegex(ValueError, "candidate schema validation"):
                    self._assemble_after(relative, lambda metadata: metadata.pop("reviewer"))

    def _test_reviewed_candidate_rejects_mapper_self_review(self) -> None:
        for relative in (f"{self.profile.snapshot_path}/README.md", self._record_relative()):
            with self.subTest(relative=relative):
                self._fresh_candidate()
                def self_review(metadata: dict[str, object]) -> None:
                    reviewer = metadata["reviewer"]
                    mapper = metadata["mapper"]
                    assert isinstance(reviewer, dict) and isinstance(mapper, dict)
                    reviewer["id"] = mapper["id"]
                with self.assertRaisesRegex(ValueError, "reviewer must differ from mapper"):
                    self._assemble_after(relative, self_review)

    def _test_reviewed_candidate_rejects_critical_and_important_findings(self) -> None:
        readme = f"{self.profile.snapshot_path}/README.md"
        for severity, status in (
            ("Critical", "open"),
            ("Critical", "accepted"),
            ("Important", "open"),
            ("Important", "accepted"),
        ):
            with self.subTest(severity=severity, status=status):
                self._fresh_candidate()

                def add_finding(metadata: dict[str, object]) -> None:
                    finding: dict[str, object] = {
                        "finding_id": "review-finding",
                        "affected_record_ids": ["ce33-d-001"],
                        "severity": severity,
                        "status": status,
                        "description": "Fixture finding.",
                        "disposition": "Fixture disposition.",
                    }
                    if status == "accepted":
                        finding.update(
                            resolver_or_acceptor="fixture-acceptor",
                            disposition_date="2026-07-25",
                            acceptance_rationale="Fixture rationale.",
                        )
                    metadata["findings"] = [finding]

                with self.assertRaisesRegex(
                    ValueError,
                    f"{severity} finding must be resolved",
                ):
                    self._assemble_after(readme, add_finding)

    def _test_reviewed_candidate_rejects_lifecycle_events(self) -> None:
        registry = f"crosswalks/registry/{CORE_ID}.md"
        with self.assertRaisesRegex(ValueError, "event array must be empty"):
            self._assemble_after(
                registry,
                lambda metadata: metadata.update(events=["reviewed"]),
            )

    def _test_reviewed_candidate_rejects_each_required_reviewer_field(self) -> None:
        readme = f"{self.profile.snapshot_path}/README.md"
        for field in (
            "id",
            "qualification",
            "date",
            "authorized_source_access",
            "findings_disposition",
        ):
            with self.subTest(field=field):
                self._fresh_candidate()

                def remove_field(metadata: dict[str, object]) -> None:
                    reviewer = metadata["reviewer"]
                    assert isinstance(reviewer, dict)
                    reviewer.pop(field)

                with self.assertRaisesRegex(ValueError, "candidate schema validation"):
                    self._assemble_after(readme, remove_field)

    def test_reviewed_candidate_uses_candidate_sourced_schemas(self) -> None:
        cases = (
            (
                "mapping-set",
                "crosswalks/schema/mapping-set.schema.json",
                "\"reviewed\", \"approved\"",
                "\"approved\"",
                "mapping set candidate schema validation",
            ),
            (
                "mapping-record",
                "crosswalks/schema/mapping-record.schema.json",
                "\"draft\", \"reviewed\"",
                "\"draft\"",
                "record .* candidate schema validation",
            ),
        )
        for label, relative, before, after, message in cases:
            with self.subTest(schema=label):
                self._fresh_candidate()
                path = self.repository / relative
                path.write_text(
                    path.read_text(encoding="utf-8").replace(before, after, 1),
                    encoding="utf-8",
                    newline="\n",
                )
                head = self._commit("tighten candidate schema")
                with self.assertRaisesRegex(ValueError, message):
                    bundle_builder.assemble_package(
                        GitReader(self.repository),
                        head,
                        self.profile,
                        "reviewed",
                    )


class CandidateValidationTests(unittest.TestCase):
    def _metadata(self) -> dict[str, object]:
        return {
            "mapping_set_id": CORE_ID,
            "status": "reviewed",
            "mapper": {"id": "mapper"},
            "reviewer": {"id": "reviewer"},
        }

    def test_reviewed_reviewer_must_differ_from_mapper_for_set_and_record(self) -> None:
        for subject in ("mapping set", "record fixture.md"):
            metadata = self._metadata()
            metadata["reviewer"] = {"id": "mapper"}
            with self.subTest(subject=subject), self.assertRaisesRegex(
                ValueError, "reviewer must differ from mapper"
            ):
                bundle_builder._require_candidate_state(
                    metadata, CORE_ID, subject, "reviewed"
                )

    def test_candidate_schema_decoding_and_definition_errors_are_stable(self) -> None:
        class Reader:
            def __init__(self, content: bytes) -> None:
                self.content = content
            def read_bytes(self, commit: str, path: str) -> bytes:
                return self.content

        for content in (b"\xff", b'{"type": 7}'):
            with self.subTest(content=content), self.assertRaisesRegex(
                ValueError, "invalid candidate schema: crosswalks/schema/mapping-set.schema.json"
            ):
                bundle_builder._validate_candidate_metadata(
                    Reader(content), "0" * 40,
                    "crosswalks/schema/mapping-set.schema.json", {}, "mapping set"
                )

    def test_candidate_schema_can_allow_extension_and_catalog_uses_supplied_validators(self) -> None:
        schema = {"type": "object", "additionalProperties": True}
        class Reader:
            def read_bytes(self, commit: str, path: str) -> bytes:
                return json.dumps(schema).encode("utf-8")
        metadata = self._metadata()
        metadata.update(schema_version="1.0.0", extension="candidate-only")
        bundle_builder._validate_candidate_metadata(
            Reader(), "0" * 40, "crosswalks/schema/mapping-set.schema.json", metadata, "mapping set"
        )
        with mock.patch.object(crosswalk_catalog, "load_schemas", side_effect=AssertionError):
            self.assertEqual(
                crosswalk_catalog._catalog_model_errors(
                    bundle_builder.ValidationResult([], [], []), {}
                ),
                [],
            )


class PackageWriterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reader = GitReader(ROOT)
        cls.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
        cls.profile = PROFILES[
            "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0"
        ]

    def setUp(self) -> None:
        state_patch = mock.patch.object(
            self.reader,
            "require_candidate_execution_state",
        )
        self.require_state = state_patch.start()
        self.addCleanup(state_patch.stop)
        generator_state_patch = mock.patch(
            "tools.build_mapping_review_bundle._require_generator_execution_state",
            create=True,
        )
        self.generator_state = generator_state_patch.start()
        self.addCleanup(generator_state_patch.stop)

    def test_writer_verifies_candidate_state_at_api_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=self._minimal_files(),
            ):
                write_package(
                    self.reader,
                    self.head,
                    self.profile,
                    output,
                )
        self.assertEqual(
            self.generator_state.call_args_list,
            [
                mock.call(self.reader, self.head),
                mock.call(self.reader, self.head),
            ],
        )
        self.require_state.assert_not_called()

    def test_writer_does_not_publish_after_execution_state_changes(self) -> None:
        self.generator_state.side_effect = (
            None,
            ValueError("repository became dirty"),
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=self._minimal_files(),
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "repository became dirty",
                ):
                    write_package(
                        self.reader,
                        self.head,
                        self.profile,
                        output,
                    )
            self.assertFalse(output.exists())

    def test_two_runs_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            first_manifest = write_package(
                self.reader, self.head, self.profile, first
            )
            second_manifest = write_package(
                self.reader, self.head, self.profile, second
            )
            self.assertEqual(first_manifest, second_manifest)
            first_files = {
                path.relative_to(first).as_posix(): path.read_bytes()
                for path in first.rglob("*") if path.is_file()
            }
            second_files = {
                path.relative_to(second).as_posix(): path.read_bytes()
                for path in second.rglob("*") if path.is_file()
            }
            self.assertEqual(first_files, second_files)
            self.assertIn("PACKAGE_INDEX.md", first_files)
            self.assertIn("PACKAGE_MANIFEST.json", first_files)

    def test_manifest_covers_every_payload_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            manifest = write_package(
                self.reader, self.head, self.profile, output
            )
            listed = {item["path"] for item in manifest["files"]}
            actual_payload = {
                path.relative_to(output).as_posix()
                for path in output.rglob("*")
                if path.is_file() and path.name != "PACKAGE_MANIFEST.json"
            }
            self.assertEqual(listed, actual_payload)
            for item in manifest["files"]:
                content = (output / item["path"]).read_bytes()
                self.assertEqual(item["bytes"], len(content))
                self.assertEqual(
                    item["sha256"], hashlib.sha256(content).hexdigest()
                )

    def test_rejects_worktree_and_nonempty_output(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside every Git worktree"):
            validate_output_directory(
                ROOT / "review-output",
                self.reader.worktree_roots(),
            )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "existing"
            output.mkdir()
            (output / "keep.txt").write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty"):
                validate_output_directory(output, ())

    def test_cli_writes_one_allowlisted_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "tools.build_mapping_review_bundle._require_generator_execution_state",
            ) as require_state:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    result = main(
                        [
                            "--commit",
                            self.head,
                            "--mapping-set-id",
                            self.profile.mapping_set_id,
                            "--output",
                            str(output),
                        ]
                    )
            self.assertEqual(result, 0, stderr.getvalue())
            self.assertEqual(require_state.call_count, 2)
            for call in require_state.call_args_list:
                checked_reader, checked_commit = call.args
                self.assertIsInstance(checked_reader, GitReader)
                self.assertEqual(checked_reader.root, ROOT)
                self.assertEqual(checked_commit, self.head)
            report = json.loads(stdout.getvalue())
            self.assertEqual(report["candidate_commit"], self.head)
            self.assertEqual(report["mapping_set_id"], self.profile.mapping_set_id)
            self.assertEqual(len(report["manifest_sha256"]), 64)
            manifest = json.loads(
                (output / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["generator_commit"], self.head)

    def test_cli_defaults_to_draft_and_rejects_unknown_candidate_state(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            default_output = Path(directory) / "default-package"
            default_result = main(
                [
                    "--commit",
                    self.head,
                    "--mapping-set-id",
                    CORE_ID,
                    "--output",
                    str(default_output),
                ]
            )
            self.assertEqual(default_result, 0)
            self.assertEqual(
                json.loads(
                    (default_output / "PACKAGE_MANIFEST.json").read_bytes()
                )["candidate_state"],
                "draft",
            )

            output = Path(directory) / "unknown-state-package"
            parser_result = main(
                [
                    "--commit",
                    self.head,
                    "--mapping-set-id",
                    CORE_ID,
                    "--output",
                    str(output),
                    "--candidate-state",
                    "approved",
                ]
            )
            self.assertEqual(parser_result, 2)
            self.assertFalse(output.exists())

    def test_assembly_is_in_memory_and_manifest_self_excludes(self) -> None:
        assembly = assemble_package(self.reader, self.head, PROFILES[CORE_ID])
        self.assertEqual(assembly.manifest["candidate_state"], "draft")
        self.assertNotIn(
            "PACKAGE_MANIFEST.json",
            {item.path for item in assembly.payloads},
        )

    def test_cli_rejects_unknown_mapping_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main(
                    [
                        "--commit",
                        self.head,
                        "--mapping-set-id",
                        "unknown",
                        "--output",
                        str(Path(directory) / "package"),
                    ]
                )
            self.assertEqual(result, 2)
            self.assertIn("unsupported mapping-set identifier", stderr.getvalue())

    def _minimal_files(
        self,
        *extra: PackageFile,
    ) -> tuple[PackageFile, ...]:
        mapping_set_path = f"{self.profile.snapshot_path}/README.md"
        return (
            PackageFile(
                mapping_set_path,
                self.reader.read_bytes(self.head, mapping_set_path),
                "mapping set",
            ),
            *extra,
        )

    def test_writer_rejects_unsafe_package_paths(self) -> None:
        for index, unsafe in enumerate(
            (
                "/absolute/path",
                "../parent/path",
                "review\\backslash.txt",
                "C:drive-relative",
            )
        ):
            with self.subTest(path=unsafe):
                with tempfile.TemporaryDirectory() as directory:
                    output = Path(directory) / f"package-{index}"
                    files = self._minimal_files(
                        PackageFile(unsafe, b"unsafe\n", "unsafe test"),
                    )
                    with mock.patch(
                        "tools.build_mapping_review_bundle.collect_package_files",
                        return_value=files,
                    ):
                        with self.assertRaisesRegex(
                            ValueError,
                            "unsafe package path",
                        ):
                            write_package(
                                self.reader,
                                self.head,
                                self.profile,
                                output,
                            )

    def test_writer_rejects_case_insensitive_path_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            files = self._minimal_files(
                PackageFile("review-metadata/Evidence.txt", b"one\n", "test"),
                PackageFile("review-metadata/evidence.txt", b"two\n", "test"),
            )
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=files,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "case-insensitive package path collision",
                ):
                    write_package(
                        self.reader,
                        self.head,
                        self.profile,
                        output,
                    )

    def test_writer_rejects_existing_empty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            output.mkdir()
            with self.assertRaisesRegex(ValueError, "must not already exist"):
                write_package(
                    self.reader,
                    self.head,
                    self.profile,
                    output,
                )

    def test_writer_does_not_publish_partial_output_after_write_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            files = self._minimal_files(
                PackageFile("review-metadata/evidence.txt", b"evidence\n", "test"),
            )
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=files,
            ):
                with mock.patch(
                    "tools.build_mapping_review_bundle._write_file_exclusively",
                    side_effect=OSError("injected write failure"),
                    create=True,
                ):
                    with self.assertRaisesRegex(OSError, "injected write failure"):
                        write_package(
                            self.reader,
                            self.head,
                            self.profile,
                            output,
                        )
            self.assertFalse(output.exists())

    @unittest.skipUnless(
        hasattr(os, "symlink"),
        "symbolic links are not supported",
    )
    def test_output_validation_rejects_existing_directory_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            link = root / "output-link"
            try:
                os.symlink(target, link, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"symbolic-link creation unavailable: {error}")
            with self.assertRaisesRegex(ValueError, "must not already exist"):
                validate_output_directory(link, ())


class PackageIntegrationTests(unittest.TestCase):
    def test_all_packages_are_separate_complete_and_source_safe(self) -> None:
        reader = GitReader(ROOT)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
        with mock.patch(
            "tools.build_mapping_review_bundle._require_generator_execution_state",
        ) as require_state, tempfile.TemporaryDirectory() as directory:
            manifests = {}
            for profile in PROFILES.values():
                with self.subTest(profile=profile.label):
                    output = (
                        Path(directory)
                        / profile.label.replace(" ", "-").lower()
                    )
                    manifests[profile.label] = write_package(
                        reader, head, profile, output
                    )
                    manifest = manifests[profile.label]
                    names = {
                        path.relative_to(output).as_posix()
                        for path in output.rglob("*") if path.is_file()
                    }
                    self.assertFalse(
                        any(
                            name.lower().endswith((".pdf", ".doc", ".docx"))
                            for name in names
                        )
                    )
                    index = (output / "PACKAGE_INDEX.md").read_text(
                        encoding="utf-8"
                    )
                    self.assertIn(profile.label, index)
                    self.assertIn(profile.direction, index)
                    self.assertIn(f"`{profile.mapping_set_id}`", index)
                    self.assertIn(f"| Candidate commit | `{head}` |", index)
                    self.assertIn(
                        f"| Expected provisions | {profile.expected_count} |",
                        index,
                    )
                    mapping_set_path = f"{profile.snapshot_path}/README.md"
                    mapping_set = (output / mapping_set_path).read_bytes()
                    metadata, _ = parse_front_matter_bytes(mapping_set)
                    publication = metadata["publication"]
                    source = metadata["source"]
                    source_version = metadata["source_version"]
                    release = metadata["esaf_release"]
                    rights = metadata["publication_rights"]
                    self.assertIn(
                        f"| Publication | {publication['name']} |",
                        index,
                    )
                    self.assertIn(
                        f"| Source version | `{source_version['id']}` "
                        f"({source_version['label']}) |",
                        index,
                    )
                    self.assertIn(
                        f"| Official URL | {source['official_url']} |",
                        index,
                    )
                    self.assertIn(
                        f"| Access class | `{source['access_class']}` |",
                        index,
                    )
                    self.assertIn(
                        f"| Historical control-source commit | "
                        f"`{release['source_commit_sha']}` |",
                        index,
                    )
                    self.assertIn(
                        f"| Historical control-catalog SHA-256 | "
                        f"`{release['control_catalog_sha256']}` |",
                        index,
                    )
                    self.assertIn(rights["basis"], index)
                    self.assertIn(rights["restrictions"], index)
                    for permitted in rights["permitted_elements"]:
                        self.assertIn(f"`{permitted}`", index)
                    if rights["prohibited_elements"]:
                        for prohibited in rights["prohibited_elements"]:
                            self.assertIn(f"`{prohibited}`", index)
                    else:
                        self.assertIn("None recorded.", index)
                    for evidence in EXPECTED_SOURCE_EVIDENCE[
                        profile.mapping_set_id
                    ]:
                        self.assertIn(evidence, index)
                    self.assertIn("controls/catalog.json", names)
                    self.assertEqual(
                        hashlib.sha256(
                            (output / "controls/catalog.json").read_bytes()
                        ).hexdigest(),
                        release["control_catalog_sha256"],
                    )
                    if profile.mapping_set_id != CORE_ID:
                        self.assertIn(
                            "docs/superpowers/specs/"
                            "2026-07-14-uk-cyber-essentials-plus-v3.2-"
                            "provision-oracle.json",
                            names,
                        )
                    manifest_rows = [
                        f"| `{item['path']}` | {item['purpose']} |"
                        for item in manifest["files"]
                    ]
                    positions = []
                    for row in manifest_rows:
                        self.assertIn(row, index)
                        positions.append(index.index(row))
                    self.assertEqual(positions, sorted(positions))
                    self.assertIn("obtain authorized access", index)
                    self.assertIn("remains Draft", index)
                    for nonclaim in (
                        "certification",
                        "compliance",
                        "equivalence",
                        "endorsement",
                        "approval",
                        "assurance",
                    ):
                        self.assertIn(nonclaim, index)
            self.assertEqual(set(manifests), {"Core", "Plus forward", "Plus reverse"})
            self.assertEqual(
                {item["mapping_set_id"] for item in manifests.values()},
                set(PROFILES),
            )
            self.assertEqual(
                require_state.call_args_list,
                [mock.call(reader, head)] * (2 * len(PROFILES)),
            )

    def test_tools_readme_documents_exact_safe_command(self) -> None:
        text = (ROOT / "tools/README.md").read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        self.assertIn("## Qualified mapping review packages", text)
        self.assertIn("build_mapping_review_bundle.py", text)
        self.assertIn("--commit", text)
        self.assertIn("--mapping-set-id", text)
        self.assertIn("--output", text)
        self.assertIn("outside every Git worktree", normalized)
        self.assertIn(
            "new output path that does not already exist",
            normalized,
        )
        self.assertIn(
            "candidate commit must equal the current clean HEAD",
            normalized,
        )
        self.assertIn(
            "failed assembly can leave an owned hidden sibling staging "
            "directory",
            normalized,
        )
        self.assertIn("does not include the external source document", text)
