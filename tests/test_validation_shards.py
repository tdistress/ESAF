from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

from tools.test_shards import load_manifest, tracked_test_modules, validate_manifest


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHARD_IDS = (
    "profile_validation",
    "qualified_review_evidence",
    "mapping_review_bundle",
    "remaining",
)


class ValidationShardTests(unittest.TestCase):
    def manifest(self, modules: list[str]) -> dict[str, object]:
        return {
            "schema": "esaf-test-shards-v1",
            "shards": [
                {
                    "id": "profile_validation",
                    "modules": ["tests/test_validate_profiles.py"],
                },
                {
                    "id": "qualified_review_evidence",
                    "modules": [
                        "tests/test_validate_qualified_review_evidence.py"
                    ],
                },
                {
                    "id": "mapping_review_bundle",
                    "modules": [
                        "tests/test_build_mapping_review_bundle.py"
                    ],
                },
                {"id": "remaining", "modules": modules},
            ],
        }

    def write_manifest(self, root: Path, document: object) -> None:
        tools = root / "tools"
        tools.mkdir()
        (tools / "test-shards.json").write_text(
            json.dumps(document, indent=2) + "\n", encoding="utf-8"
        )

    def runner_for(self, modules: tuple[str, ...]) -> Callable[..., object]:
        def runner(command: list[str], **kwargs: Any) -> object:
            self.assertEqual(
                command, ["git", "ls-files", "-z", "--", "tests/test_*.py"]
            )
            self.assertFalse(kwargs["check"])
            self.assertTrue(kwargs["capture_output"])
            return subprocess.CompletedProcess(
                command, 0, "\0".join(modules).encode("utf-8") + b"\0"
            )

        return runner

    def validate_temporary_manifest(
        self, document: object, modules: tuple[str, ...]
    ) -> tuple[object, ...]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_manifest(root, document)
            return validate_manifest(root, self.runner_for(modules))

    def assert_manifest_error(
        self, document: object, modules: tuple[str, ...], expected: str
    ) -> None:
        with self.assertRaisesRegex(ValueError, expected):
            self.validate_temporary_manifest(document, modules)

    def test_repository_manifest_covers_every_tracked_module_once(self) -> None:
        shards = validate_manifest(ROOT)
        self.assertEqual(EXPECTED_SHARD_IDS, tuple(item.identifier for item in shards))
        assigned = [module for shard in shards for module in shard.modules]
        self.assertEqual(list(tracked_test_modules(ROOT)), sorted(assigned))
        self.assertEqual(len(assigned), len(set(assigned)))

    def test_manifest_rejects_missing_duplicate_and_untracked_modules(self) -> None:
        population = (
            "tests/test_build_mapping_review_bundle.py",
            "tests/test_validate_profiles.py",
            "tests/test_validate_qualified_review_evidence.py",
            "tests/test_zeta.py",
        )
        self.assert_manifest_error(
            self.manifest([]), population, "missing"
        )
        self.assert_manifest_error(
            self.manifest(["tests/test_zeta.py", "tests/test_zeta.py"]),
            population,
            "duplicate",
        )
        self.assert_manifest_error(
            self.manifest(["tests/test_untracked.py", "tests/test_zeta.py"]),
            population,
            "untracked",
        )

    def test_manifest_rejects_invalid_structure_and_paths(self) -> None:
        population = (
            "tests/test_build_mapping_review_bundle.py",
            "tests/test_validate_profiles.py",
            "tests/test_validate_qualified_review_evidence.py",
            "tests/test_zeta.py",
        )
        self.assert_manifest_error(
            {"schema": "wrong", "shards": []}, population, "schema"
        )
        self.assert_manifest_error(
            {"schema": "esaf-test-shards-v1", "extra": [], "shards": []},
            population,
            "top-level",
        )
        wrong_order = self.manifest(["tests/test_zeta.py"])
        shards = wrong_order["shards"]
        assert isinstance(shards, list)
        shards[0], shards[1] = shards[1], shards[0]
        self.assert_manifest_error(wrong_order, population, "order")

        unknown_field = self.manifest(["tests/test_zeta.py"])
        unknown_field["shards"][0]["extra"] = True  # type: ignore[index]
        self.assert_manifest_error(unknown_field, population, "shard")

        for invalid_module in (
            "tests\\test_zeta.py",
            "/tests/test_zeta.py",
            "tests/./test_zeta.py",
            "tests/../tests/test_zeta.py",
            "tools/test_zeta.py",
            "tests/zeta.py",
        ):
            with self.subTest(module=invalid_module):
                self.assert_manifest_error(
                    self.manifest([invalid_module]), population, "module"
                )

    def test_manifest_rejects_duplicate_json_keys_and_unsorted_modules(self) -> None:
        population = (
            "tests/test_build_mapping_review_bundle.py",
            "tests/test_validate_profiles.py",
            "tests/test_validate_qualified_review_evidence.py",
            "tests/test_alpha.py",
            "tests/test_zeta.py",
        )
        duplicate_key_manifest = (
            '{"schema":"esaf-test-shards-v1","schema":"esaf-test-shards-v1",'
            '"shards":[]}'
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            (root / "tools" / "test-shards.json").write_text(
                duplicate_key_manifest, encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "duplicate key"):
                load_manifest(root)

        self.assert_manifest_error(
            self.manifest(["tests/test_zeta.py", "tests/test_alpha.py"]),
            population,
            "sorted",
        )


if __name__ == "__main__":
    unittest.main()
