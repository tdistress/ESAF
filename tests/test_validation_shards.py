from __future__ import annotations

import json
import io
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Callable

from tools.run_test_shards import (
    FAILURE_SUMMARY_BYTES,
    build_command,
    main,
    run_all,
    run_shard,
)
from tools.test_shards import load_manifest, tracked_test_modules, validate_manifest
from tools.v05_beta_release_evidence import _output_tail


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHARD_IDS = (
    "profile_validation",
    "qualified_review_evidence",
    "mapping_review_bundle",
    "remaining",
)


def flatten_test_ids(suite: unittest.TestSuite) -> list[str]:
    """Return test IDs from a possibly nested unittest suite."""
    test_ids: list[str] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            test_ids.extend(flatten_test_ids(item))
        else:
            test_ids.append(item.id())
    return test_ids


def normalized_test_id(identifier: str) -> str:
    """Normalize discovery and dotted-module test IDs to one namespace."""
    return identifier.removeprefix("tests.")


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

    def test_manifest_modules_match_discovery_test_population(self) -> None:
        shards = load_manifest(ROOT)
        discovered = flatten_test_ids(
            unittest.defaultTestLoader.discover(str(ROOT / "tests"))
        )
        manifest_modules = [
            module.removesuffix(".py").replace("/", ".")
            for shard in shards
            for module in shard.modules
        ]
        manifest_tests = flatten_test_ids(
            unittest.defaultTestLoader.loadTestsFromNames(manifest_modules)
        )

        self.assertEqual(len(discovered), len(manifest_tests))
        self.assertEqual(
            {normalized_test_id(item) for item in discovered},
            {normalized_test_id(item) for item in manifest_tests},
        )


class TestShardRunnerTests(unittest.TestCase):
    def manifest_by_id(self) -> dict[str, object]:
        return {shard.identifier: shard for shard in load_manifest(ROOT)}

    def test_script_starts_from_the_repository_root(self) -> None:
        completed = subprocess.run(
            [sys.executable, "tools/run_test_shards.py", "--help"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )

        self.assertEqual(0, completed.returncode)
        self.assertIn(b"usage:", completed.stdout)

    def test_build_command_uses_the_complete_manifest_module_list(self) -> None:
        manifest_by_id = self.manifest_by_id()
        shard = manifest_by_id["profile_validation"]
        assert hasattr(shard, "modules")

        self.assertEqual(
            [
                sys.executable,
                "-m",
                "unittest",
                *shard.modules,
                "-v",
                "--durations",
                "50",
            ],
            build_command(shard, 50),
        )

    def test_run_shard_captures_bytes_and_elapsed_time(self) -> None:
        shard = self.manifest_by_id()["profile_validation"]
        assert hasattr(shard, "identifier")
        calls: list[tuple[list[str], dict[str, object]]] = []

        def runner(command: list[str], **kwargs: object) -> object:
            calls.append((command, kwargs))
            return subprocess.CompletedProcess(
                command, 0, b"suite output\n", b"suite warnings\n"
            )

        ticks = iter((10.0, 12.5))
        result = run_shard(
            ROOT, shard, 50, runner=runner, clock=lambda: next(ticks)
        )

        self.assertEqual("profile_validation", result.identifier)
        self.assertEqual(shard.modules, result.modules)
        self.assertEqual(2.5, result.elapsed_seconds)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(b"suite output\n", result.stdout)
        self.assertEqual(b"suite warnings\n", result.stderr)
        self.assertEqual([build_command(shard, 50)], [call[0] for call in calls])
        kwargs = calls[0][1]
        self.assertEqual(ROOT, kwargs["cwd"])
        self.assertFalse(kwargs["shell"])
        self.assertTrue(kwargs["capture_output"])
        environment = kwargs["env"]
        self.assertIsInstance(environment, dict)
        self.assertEqual("1", environment["PYTHONDONTWRITEBYTECODE"])
        self.assertEqual(os.environ.get("PATH"), environment.get("PATH"))

    def test_run_all_executes_every_shard_in_manifest_order_after_failure(self) -> None:
        shards = load_manifest(ROOT)
        calls: list[str] = []

        def runner(command: list[str], **kwargs: object) -> object:
            identifier = next(
                shard.identifier
                for shard in shards
                if list(shard.modules) == command[3:-3]
            )
            calls.append(identifier)
            return subprocess.CompletedProcess(
                command,
                1 if identifier == "profile_validation" else 0,
                b"",
                f"{identifier} stderr\n".encode(),
            )

        ticks = iter(float(item) for item in range(16))
        results = run_all(
            ROOT, shards, 50, runner=runner, clock=lambda: next(ticks)
        )

        self.assertEqual([item.identifier for item in shards], calls)
        self.assertEqual([1, 0, 0, 0], [item.exit_code for item in results])
        self.assertEqual([1.0, 1.0, 1.0, 1.0], [item.elapsed_seconds for item in results])

    def test_all_reports_bounded_final_summary_for_every_noisy_failure(self) -> None:
        shards = load_manifest(ROOT)
        stderr = io.StringIO()
        stdout = io.StringIO()

        def runner(command: list[str], **kwargs: object) -> object:
            shard = next(
                item
                for item in shards
                if list(item.modules) == command[3:-3]
            )
            summary = f"{shard.identifier} unittest summary\n".encode()
            return subprocess.CompletedProcess(
                command,
                1,
                (b"x" * 40000) + summary,
                b"ordinary stderr\n",
            )

        ticks = iter(float(item) for item in range(16))
        exit_code = main(
            ["--all", "--durations", "50"],
            root=ROOT,
            runner=runner,
            clock=lambda: next(ticks),
            stdout=stdout,
            stderr=stderr,
            manifest_validator=lambda _root: shards,
        )

        output = stderr.getvalue()
        encoded = output.encode("utf-8")
        self.assertEqual(1, exit_code)
        self.assertLessEqual(len(encoded), FAILURE_SUMMARY_BYTES + 4096)
        self.assertLessEqual(
            len(output[output.rfind("Shard failures:") :].encode("utf-8")),
            FAILURE_SUMMARY_BYTES,
        )
        self.assertLess(output.find("ordinary stderr"), output.rfind("Shard failures:"))
        collector_tail = _output_tail(
            stdout.getvalue().encode("utf-8"),
            stderr.getvalue().encode("utf-8"),
        )
        for shard in shards:
            self.assertIn(shard.identifier, output)
            self.assertIn(f"{shard.identifier} unittest summary", output)
            self.assertIn(shard.identifier, collector_tail)
            self.assertIn(f"{shard.identifier} unittest summary", collector_tail)


if __name__ == "__main__":
    unittest.main()
