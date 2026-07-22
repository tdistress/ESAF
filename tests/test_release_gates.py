from copy import deepcopy
from datetime import date, datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

from tools.release_gates import (
    EXPECTED_MAPPING_SETS,
    GATE_IDS,
    load_front_matter,
    validate_external_evidence,
    validate_record,
    validate_transition,
)

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"


def write_release_scope_fixture(root: Path) -> None:
    (root / "crosswalks").mkdir(parents=True)
    (root / "project").mkdir(parents=True)
    shutil.copy2(ROOT / "VERSION.md", root / "VERSION.md")
    shutil.copy2(ROOT / "project/RELEASE_PLAN.md", root / "project/RELEASE_PLAN.md")
    shutil.copy2(ROOT / "crosswalks/catalog.json", root / "crosswalks/catalog.json")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=root, check=True)
    subprocess.run(["git", "add", "VERSION.md", "project/RELEASE_PLAN.md", "crosswalks/catalog.json"], cwd=root, check=True)


def valid_record() -> dict[str, object]:
    return {
        "release": "0.4-alpha",
        "phase": "evidence_candidate",
        "tag": "v0.4-alpha",
        "issue": 39,
        "repository_scope": "complete_git_tracked_repository",
        "publication": {
            "date": None,
            "condition": "remote_annotated_tag_matches_exact_validated_commit",
        },
        "mapping_sets": [
            "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
            "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
            "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
        ],
        "gates": {gate: {"state": "open", "evidence": []} for gate in GATE_IDS},
    }


def closure_record() -> dict[str, object]:
    record = valid_record()
    record["phase"] = "closure_candidate"
    record["publication"] = {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "condition": "remote_annotated_tag_matches_exact_validated_commit",
    }
    record["gates"] = {
        gate: {
            "state": "ready",
            "evidence": ["https://github.com/tdistress/ESAF/issues/39"],
        }
        for gate in GATE_IDS
    }
    return record


def approved_external_evidence(closure: str, merge: str | None = None) -> dict[str, object]:
    date = datetime.now(timezone.utc).date().isoformat()

    def verdict(role: str, suffix: int) -> dict[str, object]:
        return {
            "sha": closure,
            "reviewer": role,
            "date": date,
            "disposition": "approved",
            "url": f"https://github.com/tdistress/ESAF/pull/50#issuecomment-{suffix}",
            "critical": 0,
            "important": 0,
        }

    evidence: dict[str, object] = {
        "closure_head": closure,
        "scope": {
            **verdict("scope-reviewer", 1),
            "approver": "scope-approver",
            "role": "release-scope approver",
        },
        "technical": verdict("technical-reviewer", 2),
        "editorial": verdict("editorial-reviewer", 3),
        "rendering": verdict("rendering-reviewer", 4),
        "governance": {
            **verdict("governance-reviewer", 5),
            "approver": "governance-approver",
            "authority": "Steering Committee",
        },
        "mapping_reviews": [
            {
                "mapping_set_id": mapping_set_id,
                "sha": closure,
                "reviewer": f"qualified-reviewer-{index}",
                "qualification": "documented scheme and ESAF qualification",
                "date": date,
                "disposition": "approved",
                "url": f"https://github.com/tdistress/ESAF/pull/50#issuecomment-{index + 10}",
            }
            for index, mapping_set_id in enumerate(EXPECTED_MAPPING_SETS, start=1)
        ],
        "github_checks": {
            "expected": ["Validate ESAF sources"],
            "observed": [{
                "name": "Validate ESAF sources",
                "sha": closure,
                "conclusion": "success",
                "url": "https://github.com/tdistress/ESAF/actions/runs/1",
            }],
        },
        "merge_state": {"sha": closure, "mergeable": True, "state": "clean"},
    }
    if merge is not None:
        command_names = (
            "full_suite", "controls", "architectures", "migration",
            "crosswalk_current", "crosswalk_baseline", "links", "release_record",
            "mermaid_inventory", "whole_range_diff", "cache_count", "clean_status",
        )
        evidence["merge_head"] = merge
        evidence["post_merge"] = {
            "sha": merge,
            "commands": [
                {"name": name, "exit_code": 0, "result": "passed"}
                for name in command_names
            ],
        }
    return evidence


class ReleaseGateTests(unittest.TestCase):
    def test_authoritative_record_is_valid(self) -> None:
        self.assertEqual(validate_record(ROOT, load_front_matter(RECORD)), [])

    def test_record_requires_complete_release_scope_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_release_scope_fixture(root)
            cases = (
                (
                    "version",
                    lambda record: (root / "VERSION.md").write_text("# ESAF Version\n\nCurrent Version: **0.5-alpha**\n", encoding="utf-8"),
                    "VERSION.md current version shall equal 0.4-alpha",
                ),
                (
                    "plan",
                    lambda record: (root / "project/RELEASE_PLAN.md").write_text("# Release Plan\n", encoding="utf-8"),
                    "project/RELEASE_PLAN.md shall preserve the 0.4-alpha Draft release plan",
                ),
                (
                    "scope",
                    lambda record: record.__setitem__("repository_scope", "mapping_sets_only"),
                    "repository scope shall equal complete_git_tracked_repository",
                ),
            )
            for name, mutate, diagnostic in cases:
                with self.subTest(name=name):
                    record = valid_record()
                    shutil.copy2(ROOT / "VERSION.md", root / "VERSION.md")
                    shutil.copy2(ROOT / "project/RELEASE_PLAN.md", root / "project/RELEASE_PLAN.md")
                    mutate(record)
                    self.assertIn(diagnostic, validate_record(root, record))

    def test_unquoted_yaml_closure_date_is_normalized_for_record_and_evidence(self) -> None:
        record = closure_record()
        date_text = datetime.now(timezone.utc).date().isoformat()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "record.md"
            path.write_text(
                "---\n" + yaml.safe_dump(record, sort_keys=False).replace(f"'{date_text}'", date_text) + "---\n",
                encoding="utf-8",
            )
            loaded = load_front_matter(path)
        self.assertIsInstance(loaded["publication"]["date"], date)
        self.assertEqual(validate_record(ROOT, loaded), [])
        self.assertEqual(
            validate_external_evidence(loaded, approved_external_evidence("d" * 40), "d" * 40, "closure"),
            [],
        )

    def test_closure_cli_requires_baseline_ref(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_release_scope_fixture(root)
            (root / "tools").mkdir()
            (root / "docs/superpowers/reviews").mkdir(parents=True)
            shutil.copy2(ROOT / "tools/release_gates.py", root / "tools/release_gates.py")
            record_path = root / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
            record_path.write_text("---\n" + yaml.safe_dump(closure_record(), sort_keys=False) + "---\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(root / "tools/release_gates.py"), "--check"],
                cwd=root,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("baseline-ref is required for closure candidate", result.stdout)

    def test_record_rejects_self_referential_sha_fields_and_values(self) -> None:
        for key, value in (
            ("candidate_sha", "a" * 40),
            ("reviewed_commit", "b" * 40),
            ("evidence", ["c" * 40]),
        ):
            with self.subTest(key=key):
                record = valid_record()
                record[key] = value
                self.assertTrue(validate_record(ROOT, record))

    def test_closed_gate_requires_nonempty_stable_evidence_locator(self) -> None:
        record = valid_record()
        record["gates"]["technical"] = {"state": "closed", "evidence": []}
        self.assertIn("technical: closed gate requires evidence", validate_record(ROOT, record))

    def test_ready_gate_requires_https_evidence_locators(self) -> None:
        record = valid_record()
        record["gates"]["technical"] = {"state": "ready", "evidence": ["review complete"]}
        self.assertIn("technical: evidence shall contain HTTPS locators", validate_record(ROOT, record))

    def test_transition_rejects_open_directly_to_closed(self) -> None:
        previous = valid_record()
        candidate = deepcopy(previous)
        candidate["gates"]["technical"]["state"] = "closed"
        candidate["gates"]["technical"]["evidence"] = ["https://github.com/tdistress/ESAF/issues/39"]
        self.assertIn("technical: illegal transition open -> closed", validate_transition(previous, candidate))

    def test_transition_rejects_malformed_gate_records(self) -> None:
        previous = valid_record()
        del previous["gates"]["scope"]
        self.assertIn("scope: transition requires valid gate records", validate_transition(previous, valid_record()))

    def test_repository_scope_locks_three_draft_mapping_sets(self) -> None:
        record = load_front_matter(RECORD)
        self.assertEqual(validate_record(ROOT, record), [])
        self.assertEqual(len(record["mapping_sets"]), 3)

    def test_taggable_phase_rejects_missing_or_wrong_sha_approval(self) -> None:
        record = closure_record()
        closure = "d" * 40
        expected_merge = "f" * 40
        evidence = approved_external_evidence(closure, expected_merge)
        evidence["governance"]["sha"] = "e" * 40
        evidence["mapping_reviews"] = []
        errors = validate_external_evidence(record, evidence, expected_merge, "taggable")
        self.assertIn("governance approval is not bound to closure head", errors)
        self.assertIn("three qualified mapping reviews are required", errors)

    def test_scope_and_governance_require_named_approvers(self) -> None:
        closure = "d" * 40
        for name, mutate, diagnostic in (
            ("scope", lambda evidence: evidence["scope"].__setitem__("approver", ""), "scope approver shall be named"),
            ("governance", lambda evidence: evidence["governance"].pop("approver"), "governance approver shall be named"),
        ):
            with self.subTest(name=name):
                evidence = approved_external_evidence(closure)
                mutate(evidence)
                self.assertIn(diagnostic, validate_external_evidence(closure_record(), evidence, closure, "closure"))

    def test_governance_rejects_undocumented_delegate_authority(self) -> None:
        closure = "d" * 40
        evidence = approved_external_evidence(closure)
        evidence["governance"]["authority"] = "documented delegate"
        evidence["governance"]["delegation_url"] = (
            "https://github.com/tdistress/ESAF/blob/main/GOVERNANCE.md"
        )
        self.assertIn(
            "governance authority is not authorized",
            validate_external_evidence(closure_record(), evidence, closure, "closure"),
        )

    def test_taggable_phase_preserves_distinct_candidate_and_merge_domains(self) -> None:
        record = closure_record()
        closure = "d" * 40
        merge = "f" * 40
        evidence = approved_external_evidence(closure, merge)
        self.assertEqual(validate_external_evidence(record, evidence, merge, "taggable"), [])

    def test_taggable_phase_requires_sha_shaped_merge_domain(self) -> None:
        closure = "d" * 40
        merge = "not-a-git-sha"
        evidence = approved_external_evidence(closure, merge)
        errors = validate_external_evidence(closure_record(), evidence, merge, "taggable")
        self.assertIn("expected head shall be a 40-character SHA", errors)
        self.assertIn("merge head shall be a 40-character SHA", errors)
        self.assertIn("post-merge head shall be a 40-character SHA", errors)

    def test_taggable_commands_are_order_independent(self) -> None:
        closure = "d" * 40
        merge = "f" * 40
        evidence = approved_external_evidence(closure, merge)
        evidence["post_merge"]["commands"].reverse()
        self.assertEqual(validate_external_evidence(closure_record(), evidence, merge, "taggable"), [])

    def test_closure_phase_requires_every_approval_check_and_clean_merge_state(self) -> None:
        closure = "d" * 40
        record = closure_record()
        for key in ("scope", "technical", "editorial", "rendering", "governance", "github_checks", "merge_state"):
            with self.subTest(key=key):
                evidence = approved_external_evidence(closure)
                del evidence[key]
                self.assertTrue(validate_external_evidence(record, evidence, closure, "closure"))

    def test_external_validation_requires_true_ready_closure_record(self) -> None:
        closure = "d" * 40
        for name, mutate, diagnostic in (
            ("phase", lambda r: r.__setitem__("phase", "evidence_candidate"), "record phase shall be closure_candidate"),
            ("altered_condition", lambda r: r["publication"].__setitem__("condition", "tag_exists"), "publication condition is invalid"),
            ("missing_condition", lambda r: r["publication"].pop("condition"), "publication condition is invalid"),
            ("missing_date", lambda r: r["publication"].__setitem__("date", None), "conditional publication date shall equal current UTC date"),
            ("open", lambda r: r["gates"]["technical"].__setitem__("state", "open"), "technical gate is not ready for closure"),
            ("in_review", lambda r: r["gates"]["editorial"].__setitem__("state", "in_review"), "editorial gate is not ready for closure"),
        ):
            with self.subTest(name=name):
                record = closure_record()
                mutate(record)
                self.assertIn(diagnostic, validate_external_evidence(record, approved_external_evidence(closure), closure, "closure"))

    def test_taggable_evidence_mutation_matrix(self) -> None:
        closure = "d" * 40
        merge = "f" * 40
        mutations = (
            ("disposition", lambda e: e["technical"].__setitem__("disposition", "rejected"), "technical disposition shall be approved"),
            ("url", lambda e: e["editorial"].__setitem__("url", "http://example.invalid"), "editorial URL shall use HTTPS"),
            ("findings", lambda e: e["rendering"].__setitem__("important", 1), "rendering Important findings shall be zero"),
            ("duplicate_mapping", lambda e: e["mapping_reviews"].append(deepcopy(e["mapping_reviews"][0])), "mapping reviews shall contain each expected mapping set exactly once"),
            ("duplicate_check", lambda e: e["github_checks"]["observed"].append(deepcopy(e["github_checks"]["observed"][0])), "observed GitHub checks shall exactly match expected checks"),
            ("exit_code", lambda e: e["post_merge"]["commands"][0].__setitem__("exit_code", 1), "full_suite command failed"),
            ("authority", lambda e: e["governance"].__setitem__("authority", "repository owner"), "governance authority is not authorized"),
            ("merge_state", lambda e: e["merge_state"].__setitem__("state", "dirty"), "merge state shall be clean"),
            ("candidate_sha", lambda e: e["scope"].__setitem__("sha", "a" * 40), "scope approval is not bound to closure head"),
            ("merge_sha", lambda e: e["post_merge"].__setitem__("sha", "a" * 40), "post-merge evidence is not bound to merge head"),
        )
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                evidence = approved_external_evidence(closure, merge)
                mutate(evidence)
                self.assertIn(diagnostic, validate_external_evidence(closure_record(), evidence, merge, "taggable"))
