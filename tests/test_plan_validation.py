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
EXPECTED_PUBLICATION_CATALOG = (
    "preflight",
    "test-shard-manifest",
    "profile-shard",
    "qualified-review-shard",
    "mapping-review-shard",
    "remaining-shard",
    "architectures",
    "assessment",
    "controls",
    "crosswalks",
    "profiles",
    "full-discovery",
    "mermaid-record",
    "links",
    "qualified-review-equivalence",
    "release-gates",
    "release-evidence",
    "pci-dss-mapping-go-no-go",
)


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
                {"id": "preflight", "argv": ["git", "diff", "--check", "{base}", "{candidate}"], "tier": "quick", "duration": "under a minute"},
                {"id": "docs", "argv": ["python", "-B", "-m", "unittest", "tests/test_esaf_1600_foundation.py"], "tier": "standard", "duration": "about a minute"},
                {"id": "links", "argv": ["python", "tools/validate_links.py", "--check"], "tier": "standard", "duration": "about a minute"},
                {"id": "qualified-review-shard", "argv": ["python", "tools/run_test_shards.py", "--shard", "qualified_review_evidence"], "tier": "standard", "duration": "several minutes"},
                {"id": "publication", "argv": ["python", "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], "tier": "publication", "duration": "candidate freeze"},
            ],
            "rules": [
                {"id": "documentation", "selectors": [{"prefix": "docs/"}], "quick": ["preflight"], "standard": ["docs", "links"], "reason": "documentation change", "cross_cutting": False},
                {"id": "qualified-review", "selectors": [{"prefix": "crosswalks/qualified-review/"}], "quick": ["preflight"], "standard": ["qualified-review-shard"], "reason": "qualified-review change", "cross_cutting": False},
                {"id": "workflow", "selectors": [{"prefix": ".github/workflows/"}], "quick": ["preflight"], "standard": [], "reason": "workflow change", "cross_cutting": True},
            ],
        }

    def write_manifest(self, document: object, *, raw: str | None = None) -> None:
        path = self.root / "tools" / "validation-plans.json"
        path.write_text(raw if raw is not None else json.dumps(document), encoding="utf-8")

    def git_diff_for(self, output: bytes, *, resolved: tuple[str, str] = ("a" * 40, "b" * 40)):
        resolves = iter(resolved)
        def runner(argv, **_kwargs):
            if argv == ["git", "rev-parse", "--verify", "HEAD^{commit}"]:
                return subprocess.CompletedProcess(argv, 0, (resolved[1] + "\n").encode(), b"")
            if argv[1:3] == ["rev-parse", "--verify"]:
                return subprocess.CompletedProcess(argv, 0, (next(resolves) + "\n").encode(), b"")
            if argv == ["git", "status", "--porcelain=v1", "--untracked-files=no"]:
                return subprocess.CompletedProcess(argv, 0, b"", b"")
            if argv == ["git", "merge-base", "--is-ancestor", resolved[0], resolved[1]]:
                return subprocess.CompletedProcess(argv, 0, b"", b"")
            return subprocess.CompletedProcess(argv, 0, output, b"")
        return runner

    def test_documentation_and_qualified_review_route_to_standard(self) -> None:
        plan = plan_validation(self.root, base="base", candidate="candidate", git_runner=self.git_diff_for(b"M\0docs/guide.md\0M\0crosswalks/qualified-review/a.json\0"))
        self.assertEqual(("quick", "standard"), plan.selected_tiers)
        self.assertEqual(("preflight", "docs", "links", "qualified-review-shard"), tuple(command.identifier for command in plan.commands))

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

    def test_publication_request_selects_complete_route(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(
                ["--base", "HEAD~1", "--tier", "publication", "--format", "json"],
                root=self.root,
                git_runner=self.git_diff_for(b"M\0docs/a.md\0"),
            )
        self.assertEqual(0, result)
        selected = json.loads(stream.getvalue())
        self.assertEqual(
            ["preflight", "docs", "links", "qualified-review-shard", "publication"],
            [command["id"] for command in selected["commands"]],
        )
        self.assertEqual(["publication"], selected["selected_tiers"])

    def test_committed_catalog_publication_route_includes_all_gates_and_base(self) -> None:
        plan = plan_validation(
            ROOT,
            base="base",
            candidate="candidate",
            git_runner=self.git_diff_for(b"M\0.github/workflows/check.yml\0"),
        )
        self.assertEqual(
            EXPECTED_PUBLICATION_CATALOG,
            tuple(command.identifier for command in plan.commands),
        )
        commands = {command.identifier: command.argv for command in plan.commands}
        self.assertEqual(
            ("git", "diff", "--check", "a" * 40, "b" * 40),
            commands["preflight"],
        )
        self.assertEqual(
            ("python", "tools/validate_links.py", "--check"),
            commands["links"],
        )
        self.assertEqual(
            (
                "python",
                "tools/verify_qualified_review_hot_path_equivalence.py",
                "--check",
                "--candidate-sha",
                "b" * 40,
            ),
            commands["qualified-review-equivalence"],
        )
        self.assertNotIn("qualified-review", commands)
        self.assertIn("qualified-review-shard", commands)
        self.assertEqual(
            ("python", "tools/release_gates.py", "--check", "--baseline-ref", "a" * 40),
            commands["release-gates"],
        )
        self.assertEqual(
            ("python", "tools/render_pci_dss_mapping_go_no_go.py", "--check"),
            commands["pci-dss-mapping-go-no-go"],
        )
        self.assertEqual(
            ("python", "tools/mermaid_inventory.py", "--check-record", "docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md"),
            commands["mermaid-record"],
        )
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(
                ["--base", "base", "--candidate", "candidate", "--tier", "publication", "--format", "json"],
                root=ROOT,
                git_runner=self.git_diff_for(b"M\0docs/guide.md\0"),
            )
        self.assertEqual(0, result)
        cli_commands = {command["id"]: tuple(command["argv"]) for command in json.loads(stream.getvalue())["commands"]}
        self.assertEqual(set(commands), set(cli_commands))
        self.assertEqual(commands["release-gates"], cli_commands["release-gates"])

    def test_committed_catalog_routes_ordinary_docs_and_qualified_review_to_standard(self) -> None:
        ordinary_docs = plan_validation(
            ROOT,
            base="base",
            candidate="candidate",
            git_runner=self.git_diff_for(b"M\0docs/ordinary-guide.md\0"),
        )
        self.assertEqual(("quick", "standard"), ordinary_docs.selected_tiers)
        self.assertEqual(
            ("preflight", "test-shard-manifest", "remaining-shard", "links"),
            tuple(command.identifier for command in ordinary_docs.commands),
        )

        qualified_review = plan_validation(
            ROOT,
            base="base",
            candidate="candidate",
            git_runner=self.git_diff_for(
                b"M\0crosswalks/qualified-review/campaign/manifest.json\0"
            ),
        )
        self.assertEqual(("quick", "standard"), qualified_review.selected_tiers)
        self.assertEqual(
            (
                "preflight",
                "test-shard-manifest",
                "qualified-review-shard",
                "mapping-review-shard",
                "crosswalks",
            ),
            tuple(command.identifier for command in qualified_review.commands),
        )

    def test_publication_evidence_and_version_changes_take_publication_route(self) -> None:
        for changed_path in (b"M\0docs/superpowers/reviews/record.md\0", b"M\0VERSION.md\0"):
            with self.subTest(changed_path=changed_path):
                plan = plan_validation(
                    ROOT,
                    base="base",
                    candidate="candidate",
                    git_runner=self.git_diff_for(changed_path),
                )
                self.assertEqual(("publication",), plan.selected_tiers)

    def test_candidate_mismatch_dirty_checkout_and_nonancestor_base_fail_closed(self) -> None:
        base, candidate = "a" * 40, "b" * 40

        def runner_for(*, head: str = candidate, status: bytes = b"", ancestry: int = 0):
            resolves = iter((base, candidate))

            def runner(argv, **_kwargs):
                if argv == ["git", "rev-parse", "--verify", "HEAD^{commit}"]:
                    return subprocess.CompletedProcess(argv, 0, (head + "\n").encode(), b"")
                if argv[1:3] == ["rev-parse", "--verify"]:
                    return subprocess.CompletedProcess(argv, 0, (next(resolves) + "\n").encode(), b"")
                if argv == ["git", "status", "--porcelain=v1", "--untracked-files=no"]:
                    return subprocess.CompletedProcess(argv, 0, status, b"")
                if argv == ["git", "merge-base", "--is-ancestor", base, candidate]:
                    return subprocess.CompletedProcess(argv, ancestry, b"", b"")
                return subprocess.CompletedProcess(argv, 0, b"M\0docs/a.md\0", b"")

            return runner

        for runner, message in (
            (runner_for(head="c" * 40), "does not match checkout HEAD"),
            (runner_for(status=b" M tools/plan_validation.py\0"), "tracked changes"),
            (runner_for(ancestry=1), "not an ancestor"),
        ):
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    plan_validation(self.root, base="base", candidate="candidate", git_runner=runner)

    def test_mapping_review_routes_to_supported_validation_without_stateful_package_builder(self) -> None:
        plan = plan_validation(
            ROOT,
            base="base",
            candidate="candidate",
            git_runner=self.git_diff_for(b"M\0crosswalks/mapping-review/manifest.json\0"),
        )
        self.assertEqual(("quick", "standard"), plan.selected_tiers)
        self.assertEqual(
            ("preflight", "test-shard-manifest", "mapping-review-shard", "crosswalks"),
            tuple(command.identifier for command in plan.commands),
        )
        self.assertNotIn("mapping-review", {command.identifier for command in plan.commands})

        deleted_plan = plan_validation(
            ROOT,
            base="base",
            candidate="candidate",
            git_runner=self.git_diff_for(b"D\0crosswalks/mapping-review/manifest.json\0"),
        )
        self.assertEqual(("publication",), deleted_plan.selected_tiers)
        self.assertNotIn("mapping-review", {command.identifier for command in deleted_plan.commands})

    def test_mermaid_publication_gate_uses_only_the_recorded_renderer_command(self) -> None:
        plan = plan_validation(
            ROOT,
            base="base",
            candidate="candidate",
            git_runner=self.git_diff_for(b"M\0.github/workflows/check.yml\0"),
        )
        renderer_commands = tuple(
            command for command in plan.commands if "mermaid" in command.identifier
        )
        self.assertEqual(("mermaid-record",), tuple(command.identifier for command in renderer_commands))
        self.assertEqual(
            (
                "python",
                "tools/mermaid_inventory.py",
                "--check-record",
                "docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md",
            ),
            renderer_commands[0].argv,
        )


if __name__ == "__main__":
    unittest.main()
