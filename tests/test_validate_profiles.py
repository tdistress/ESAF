from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tests import profile_fixture
from tools import validate_profiles


class ProfileValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.package = profile_fixture.write_valid_profile_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_population_has_no_errors(self) -> None:
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_duplicate_json_key_is_rejected(self) -> None:
        path = self.package / "profile.json"
        text = path.read_text(encoding="utf-8").replace(
            '"profile_version":',
            '"profile_version": "duplicate",\n"profile_version":',
            1,
        )
        path.write_text(text, encoding="utf-8")
        self.assertTrue(
            any("duplicate JSON key" in error for error in validate_profiles.validate(self.root))
        )

    def test_unlisted_package_file_is_rejected(self) -> None:
        (self.package / "unlisted.json").write_text("{}\n", encoding="utf-8")
        self.assertTrue(
            any("unlisted package file" in error for error in validate_profiles.validate(self.root))
        )

    def test_rogue_package_directory_is_rejected(self) -> None:
        (self.package / "rogue").mkdir()
        self.assertTrue(
            any("unlisted package entry rogue" in error for error in validate_profiles.validate(self.root))
        )

    def test_missing_profile_manifest_is_rejected(self) -> None:
        (self.package / "profile.json").unlink()
        self.assertTrue(
            any("missing package file profile.json" in error for error in validate_profiles.validate(self.root))
        )

    def test_missing_component_is_rejected(self) -> None:
        (self.package / "evidence-expectations.json").unlink()
        self.assertTrue(
            any(
                "missing package file evidence-expectations.json" in error
                for error in validate_profiles.validate(self.root)
            )
        )

    def test_schema_directory_is_not_a_profile_country(self) -> None:
        false_package = self.root / "profiles" / "schema" / "0.1.0"
        false_package.mkdir()
        (false_package / "profile.json").write_text("{}\n", encoding="utf-8")
        self.assertEqual(
            validate_profiles.discover_profile_packages(self.root), (self.package,)
        )

    def test_safe_component_rejects_path_aliases(self) -> None:
        for relative in (
            "nested/./component.json",
            "nested//component.json",
            "nested/../component.json",
            r"nested\component.json",
            "/absolute/component.json",
            "component.json/",
        ):
            with self.subTest(relative=relative):
                self.assertIsNone(validate_profiles.safe_component(self.package, relative))

    def test_diagnostics_are_deterministic_and_repository_relative(self) -> None:
        additional = self.root / "profiles" / "aa" / "0.1.0"
        shutil.copytree(self.package, additional)
        (self.package / "z.txt").write_text("fixture\n", encoding="utf-8")
        (additional / "a.txt").write_text("fixture\n", encoding="utf-8")
        diagnostics = validate_profiles.validate(self.root)
        self.assertEqual(diagnostics, sorted(diagnostics))
        self.assertTrue(all(str(self.root) not in error for error in diagnostics))

    def test_symlinked_country_directory_is_rejected(self) -> None:
        country = self.package.parent
        outside_country = self.root / "outside" / country.name
        outside_country.parent.mkdir()
        shutil.move(str(country), outside_country)
        try:
            os.symlink(outside_country, country, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symlink creation is unavailable: {exc}")
        self.assertTrue(
            any("symlink" in error for error in validate_profiles.validate(self.root))
        )

    def test_symlinked_schema_file_is_rejected(self) -> None:
        schema = self.root / "profiles/schema/profile.schema.json"
        target = self.root / "profile.schema.target.json"
        shutil.move(schema, target)
        try:
            os.symlink(target, schema)
        except OSError as exc:
            self.skipTest(f"symlink creation is unavailable: {exc}")
        self.assertTrue(
            any("schema root or file" in error for error in validate_profiles.validate(self.root))
        )

    def test_symlinked_schema_directory_is_rejected(self) -> None:
        schema_root = self.root / "profiles/schema"
        target = self.root / "schema-target"
        shutil.move(schema_root, target)
        try:
            os.symlink(target, schema_root, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symlink creation is unavailable: {exc}")
        self.assertTrue(
            any("schema root or file" in error for error in validate_profiles.validate(self.root))
        )

    def test_invalid_component_schema_does_not_load_package(self) -> None:
        path = self.package / "risk-overlays.json"
        path.write_text("[]\n", encoding="utf-8")
        diagnostics: list[str] = []
        package = validate_profiles.load_package(self.root, self.package, diagnostics)
        self.assertIsNone(package)
        self.assertTrue(any("risk-overlays.json" in error for error in diagnostics))

    def test_cli_requires_check_and_reports_success(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 0)
        self.assertIn("Successfully validated 1 profile package", output.getvalue())

    def test_cli_requires_check(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = validate_profiles.main([], root=self.root)
        self.assertEqual(result, 2)
        self.assertIn("--check", output.getvalue())

    def test_cli_reports_content_errors_with_exit_one(self) -> None:
        (self.package / "unexpected.txt").write_text("fixture\n", encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 1)
        self.assertIn("unexpected.txt", output.getvalue())

    def test_cli_reports_unresolvable_schema_reference_with_exit_two(self) -> None:
        path = self.root / "profiles/schema/profile.schema.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["allOf"] = [{"$ref": "missing.schema.json"}]
        path.write_text(json.dumps(schema), encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 2)
        self.assertIn("could not run", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
