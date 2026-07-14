import os
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


VALIDATOR = Path(__file__).resolve().parents[1] / "tools" / "validate_links.py"
SPEC = importlib.util.spec_from_file_location("validate_links", VALIDATOR)
assert SPEC is not None and SPEC.loader is not None
VALIDATE_LINKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATE_LINKS)


class LinkValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self.run_git("init", "--quiet")
        self.run_git("config", "user.email", "tests@example.invalid")
        self.run_git("config", "user.name", "Link Validator Tests")

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_git(self, *args):
        return subprocess.run(
            ["git", *args],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

    def write(self, relative_path, content):
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def track(self, *relative_paths):
        self.run_git("add", "--", *relative_paths)

    def validate(self):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--check"],
            cwd=self.repo,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def test_accepts_tracked_relative_root_directory_fragment_and_decoded_links(self):
        self.write(
            "README.md",
            "# Repository Home\n\n"
            "[relative](docs/guide.md#repeated-heading-1)\n"
            "[root](/docs/guide.md#repeated-heading)\n"
            "[directory](handbook/)\n"
            "[decoded](docs/file%20name.md#encoded-heading)\n"
            "[same file](#repository-home)\n"
            "[external](https://example.com/missing.md)\n"
            "[mail](mailto:owner@example.com)\n"
            "[network](//example.com/also-missing.md)\n",
        )
        self.write(
            "docs/guide.md",
            "# Repeated heading\n\n## Repeated heading\n",
        )
        self.write("docs/file name.md", "# Encoded heading\n")
        self.write("handbook/README.md", "# Handbook\n")
        self.write("untracked.md", "[broken](missing.md)\n")
        self.track("README.md", "docs/guide.md", "docs/file name.md", "handbook/README.md")

        result = self.validate()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("validated 4 tracked Markdown files", result.stdout)
        self.assertNotIn("untracked.md", result.stdout + result.stderr)

    def test_reports_missing_target_with_source_line_and_original_target(self):
        self.write("README.md", "# Home\n\ntext\n\n[missing](docs/absent.md)\n")
        self.track("README.md")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        self.assertIn("README.md:5: docs/absent.md: target does not exist", result.stdout)

    def test_reports_missing_anchor_with_source_line_and_original_target(self):
        self.write("README.md", "[section](docs/guide.md#not-present)\n")
        self.write("docs/guide.md", "# Present\n")
        self.track("README.md", "docs/guide.md")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "README.md:1: docs/guide.md#not-present: anchor does not exist",
            result.stdout,
        )

    def test_rejects_decoded_repository_escape_even_when_external_file_exists(self):
        outside = self.repo.parent / "outside.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        self.addCleanup(outside.unlink, missing_ok=True)
        self.write("README.md", "[plain](../outside.md)\n[encoded](%2e%2e/outside.md)\n")
        self.track("README.md")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        self.assertIn("README.md:1: ../outside.md: target escapes repository", result.stdout)
        self.assertIn("README.md:2: %2e%2e/outside.md: target escapes repository", result.stdout)

    def test_checks_every_tracked_markdown_file_and_orders_diagnostics(self):
        self.write("z-last.md", "[missing](z.md)\n")
        self.write("a-first.md", "first\n\n[missing](a.md)\n")
        self.write("ignored.txt", "[missing](not-markdown.md)\n")
        self.track("z-last.md", "a-first.md", "ignored.txt")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        first = result.stdout.index("a-first.md:3: a.md")
        last = result.stdout.index("z-last.md:1: z.md")
        self.assertLess(first, last)
        self.assertIn("2 broken repository-local links", result.stdout)

    def test_validates_reference_style_definitions_and_reports_definition_line(self):
        self.write(
            "README.md",
            "# Home\n\n"
            "[valid guide][guide]\n"
            "[missing guide][missing]\n\n"
            "[guide]: docs/guide.md#reference-heading\n"
            "[missing]: docs/missing_(draft).md \"optional title\"\n",
        )
        self.write("docs/guide.md", "# Reference heading\n")
        self.track("README.md", "docs/guide.md")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "README.md:7: docs/missing_(draft).md: target does not exist",
            result.stdout,
        )
        self.assertNotIn("docs/guide.md#reference-heading: ", result.stdout)

    def test_reports_full_and_collapsed_references_without_definitions(self):
        self.write(
            "README.md",
            "[full reference][missing-full]\n[missing-collapsed][]\n",
        )
        self.track("README.md")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "README.md:1: [missing-full]: reference definition does not exist",
            result.stdout,
        )
        self.assertIn(
            "README.md:2: [missing-collapsed]: reference definition does not exist",
            result.stdout,
        )

    def test_shortcut_reference_usage_recognizes_only_defined_text_and_images(self):
        line = "[guide] ![diagram]"

        usages = list(VALIDATE_LINKS.reference_usages(line))

        self.assertEqual(["guide", "diagram"], usages)

    def test_validates_defined_shortcut_text_and_image_destinations(self):
        self.write(
            "README.md",
            "[guide] ![diagram]\n\n"
            "[guide]: docs/missing-guide.md\n"
            "[diagram]: images/missing-diagram.png\n",
        )
        self.track("README.md")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "README.md:3: docs/missing-guide.md: target does not exist",
            result.stdout,
        )
        self.assertIn(
            "README.md:4: images/missing-diagram.png: target does not exist",
            result.stdout,
        )

    def test_undefined_shortcuts_and_ordinary_bracket_text_are_not_links(self):
        self.write(
            "README.md",
            "[undefined text] ![undefined image] ordinary [bracket text]\n",
        )
        self.track("README.md")

        result = self.validate()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_balanced_parenthesis_destination_preserves_complete_original_target(self):
        target = "docs/missing_(draft(v2)).md#not-(present)"
        self.write("README.md", f"[draft]({target})\n")
        self.track("README.md")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            f"README.md:1: {target}: target does not exist",
            result.stdout,
        )

    def test_inline_code_heading_content_and_url_decoded_fragment_form_anchor(self):
        self.write(
            "README.md",
            "# Commands\n\n[check](docs/guide.md#run-%2D%2Dcheck-now)\n",
        )
        self.write("docs/guide.md", "# Run `--check` now\n")
        self.track("README.md", "docs/guide.md")

        result = self.validate()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_directory_index_symlink_escape_when_supported(self):
        outside = self.repo.parent / "outside-index"
        outside.mkdir()
        self.addCleanup(outside.rmdir)
        handbook = self.repo / "handbook"
        handbook.mkdir()
        try:
            (handbook / "README.md").symlink_to(outside, target_is_directory=True)
        except OSError as error:
            if os.name != "nt":
                self.skipTest(f"directory symlinks unavailable: {error}")
            junction = subprocess.run(
                [
                    "cmd", "/c", "mklink", "/J",
                    str(handbook / "README.md"), str(outside),
                ],
                capture_output=True,
                text=True,
            )
            if junction.returncode != 0:
                self.skipTest(f"directory links unavailable: {error}; {junction.stderr}")
        self.write("README.md", "[handbook](handbook/)\n")
        self.track("README.md")

        result = self.validate()

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "README.md:1: handbook/: target escapes repository",
            result.stdout,
        )

    def test_operational_failure_returns_two(self):
        outside_git = tempfile.TemporaryDirectory()
        self.addCleanup(outside_git.cleanup)

        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--check"],
            cwd=outside_git.name,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("link validation failed:", result.stdout)


if __name__ == "__main__":
    unittest.main()
