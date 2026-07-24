from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.build_mapping_review_bundle import (
    PROFILES,
    GitReader,
    MappingProfile,
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
