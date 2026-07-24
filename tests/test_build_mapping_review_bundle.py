from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.build_mapping_review_bundle import (
    PROFILES,
    GitReader,
    MappingProfile,
    collect_package_files,
)


ROOT = Path(__file__).resolve().parents[1]


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
            {profile.direction for profile in PROFILES.values()},
            {"external_to_esaf", "esaf_to_external"},
        )
        self.assertEqual(
            {profile.label for profile in PROFILES.values()},
            {"Core", "Plus forward", "Plus reverse"},
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

    def test_reports_all_worktree_roots_as_resolved_paths(self) -> None:
        roots = self.reader.worktree_roots()
        self.assertIn(ROOT.resolve(), roots)
        self.assertTrue(all(path.is_absolute() for path in roots))


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
        self.assertEqual(
            {
                commit
                for commit, path in reader.reads
                if path in control_paths
            },
            {source_commit},
        )
        self.assertEqual(
            {
                commit
                for commit, path in reader.reads
                if path not in control_paths
            },
            {self.head},
        )

    def test_collector_accepts_prose_draft_registry(self) -> None:
        profile = next(iter(PROFILES.values()))
        files = collect_package_files(self.reader, self.head, profile)
        self.assertIn(
            f"crosswalks/registry/{profile.mapping_set_id}.md",
            {item.path for item in files},
        )

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

        with self.assertRaisesRegex(ValueError, "must remain draft"):
            collect_package_files(MutatingReader(), self.head, profile)
