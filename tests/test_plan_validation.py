from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.plan_validation import (
    load_manifest,
    main,
    plan_validation,
    render_json,
    render_text,
)


ROOT = Path(__file__).resolve().parents[1]


class PlanValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "tools").mkdir()
        self.write_manifest(self.valid_manifest())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def valid_manifest(self) -> dict[str, object]:
        return {
            "schema": "esaf-validation-plans-v1",
            "commands": [
                {"id": "preflight", "argv": ["git", "diff", "--check"], "tier": "quick", "duration": "under a minute"},
                {"id": "docs", "argv": ["python", "-B", "-m", "unittest", "tests/test_esaf_1600_foundation.py"], "tier": "standard", "duration": "about a minute"},
                {"id": "qualified", "argv": ["python", "tools/validate_qualified_review_evidence.py", "--check"], "tier": "standard", "duration": "several minutes"},
                {"id": "publication", "argv": ["python", "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], "tier": "publication", "duration": "candidate freeze"},
            ],
            "rules": [
                {"id": "documentation", "selectors": [{"prefix": "docs/"}], "quick": ["preflight"], "standard": ["docs"], "reason": "documentation change", "cross_cutting": False},
                {"id": "qualified-review", "selectors": [{"prefix": "crosswalks/qualified-review/"}], "quick": ["preflight"], "standard": ["qualified"], "reason": "qualified-review change", "cross_cutting": False},
                {"id": "workflow", "selectors": [{"prefix": ".github/workflows/"}], "quick": ["preflight"], "standard": [], "reason": "workflow change", "cross_cutting": True},
            ],
        }

    def write_manifest(self, document: object, *, raw: str | None = None) -> None:
        path = self.root / "tools" / "validation-plans.json"
        path.write_text(raw if raw is not None else json.dumps(document), encoding="utf-8")

    def git_diff_for(self, output: bytes, *, resolved: tuple[str, str] = ("a" * 40, "b" * 40)):
        resolves = iter(resolved)
        def runner(argv, **_kwargs):
            if argv[1:3] == ["rev-parse", "--verify"]:
                return subprocess.CompletedProcess(argv, 0, (next(resolves) + "\n").encode(), b"")
            return subprocess.CompletedProcess(argv, 0, output, b"")
        return runner

    def test_documentation_and_qualified_review_route_to_standard(self) -> None:
        plan = plan_validation(self.root, base="base", candidate="candidate", git_runner=self.git_diff_for(b"M\0docs/guide.md\0M\0crosswalks/qualified-review/a.json\0"))
        self.assertEqual(("quick", "standard"), plan.selected_tiers)
        self.assertEqual(("preflight", "docs", "qualified"), tuple(command.identifier for command in plan.commands))

    def test_unknown_path_escalates_to_publication(self) -> None:
        plan = plan_validation(self.root, base="base", candidate="candidate", git_runner=self.git_diff_for(b"M\0new-area/file.md\0"))
        self.assertEqual(("publication",), plan.selected_tiers)
        self.assertIn("unclassified path: new-area/file.md", plan.reasons)

    def test_workflow_deletion_and_rename_escalate_to_publication(self) -> None:
        for output in (b"M\0.github/workflows/check.yml\0", b"D\0docs/guide.md\0", b"R100\0docs/old.md\0docs/new.md\0"):
            with self.subTest(output=output):
                plan = plan_validation(self.root, base="base", candidate="candidate", git_runner=self.git_diff_for(output))
                self.assertEqual(("publication",), plan.selected_tiers)

    def test_manifest_rejects_duplicate_json_keys_and_invalid_rules_before_git(self) -> None:
        self.write_manifest({}, raw='{"schema":"esaf-validation-plans-v1","schema":"esaf-validation-plans-v1"}')
        with self.assertRaisesRegex(ValueError, "duplicate key"):
            load_manifest(self.root)
        for mutate, expected in (
            (lambda d: d["rules"].append(dict(d["rules"][0])), "duplicate rule"),
            (lambda d: d["rules"][0].update({"quick": ["missing"]}), "unknown command"),
            (lambda d: d["rules"][0].update({"selectors": []}), "selectors"),
            (lambda d: d["rules"][0].update({"selectors": [{"exact": "docs/a.md"}, {"exact": "docs/a.md"}]}), "ambiguous exact"),
        ):
            with self.subTest(expected=expected):
                document = self.valid_manifest()
                mutate(document)
                self.write_manifest(document)
                with self.assertRaisesRegex(ValueError, expected):
                    load_manifest(self.root)

    def test_unresolved_reference_and_malformed_diff_fail(self) -> None:
        def unresolved(argv, **_kwargs):
            return subprocess.CompletedProcess(argv, 1, b"", b"bad ref")
        with self.assertRaisesRegex(ValueError, "could not resolve"):
            plan_validation(self.root, base="base", candidate="candidate", git_runner=unresolved)
        with self.assertRaisesRegex(ValueError, "malformed"):
            plan_validation(self.root, base="base", candidate="candidate", git_runner=self.git_diff_for(b"M\0docs/a.md"))

    def test_rendering_is_deterministic_and_tier_filtering_retains_resolved_refs(self) -> None:
        plan = plan_validation(self.root, base="base", candidate="candidate", git_runner=self.git_diff_for(b"M\0docs/a.md\0"))
        self.assertEqual(render_text(plan), render_text(plan))
        rendered = render_json(plan)
        self.assertTrue(rendered.endswith("\n"))
        self.assertEqual(json.loads(rendered)["base"], "a" * 40)
        self.assertEqual(json.loads(rendered)["candidate"], "b" * 40)
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(["--base", "HEAD~1", "--tier", "quick", "--format", "json"], root=self.root, git_runner=self.git_diff_for(b"M\0docs/a.md\0"))
        self.assertEqual(0, result)
        selected = json.loads(stream.getvalue())
        self.assertEqual(["quick"], selected["selected_tiers"])
        self.assertEqual("a" * 40, selected["base"])


if __name__ == "__main__":
    unittest.main()
