from __future__ import annotations

import contextlib
import io
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


if __name__ == "__main__":
    unittest.main()
