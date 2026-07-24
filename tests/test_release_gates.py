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
    CLAIMS_NOT_MADE,
    EXPECTED_MAPPING_SETS,
    GATE_IDS,
    load_front_matter,
    validate_external_evidence,
    validate_record,
    validate_transition,
)

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
PUBLISHED_DATE = "2026-07-23"
PUBLISHED_TAG_OBJECT = "2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f"
PUBLISHED_COMMIT = "8abfe5a85db19d11295a0c3debeb2d58109b0ca7"
PUBLISHED_EVIDENCE = (
    "https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764"
)


def write_release_scope_fixture(root: Path) -> None:
    (root / "crosswalks").mkdir(parents=True)
    (root / "project").mkdir(parents=True)
    shutil.copy2(ROOT / "VERSION.md", root / "VERSION.md")
    shutil.copy2(ROOT / "project/RELEASE_PLAN.md", root / "project/RELEASE_PLAN.md")
    shutil.copy2(ROOT / "crosswalks/catalog.json", root / "crosswalks/catalog.json")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=root, check=True)
    subprocess.run(["git", "add", "VERSION.md", "project/RELEASE_PLAN.md", "crosswalks/catalog.json"], cwd=root, check=True)


def write_published_scope_fixture(root: Path) -> None:
    write_release_scope_fixture(root)
    (root / "project/RELEASE_PLAN.md").write_text(
        """# Release Plan

## 0.4-alpha publication

Publication gates are Closed.

Evidence: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764

Validated commit: 8abfe5a85db19d11295a0c3debeb2d58109b0ca7
""",
        encoding="utf-8",
    )


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


def closure_record(basis: str = "qualified_approval") -> dict[str, object]:
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
    record["mapping_decision_basis"] = basis
    return record


def published_record() -> dict[str, object]:
    record = valid_record()
    record["phase"] = "published"
    record["publication"] = {
        "date": PUBLISHED_DATE,
        "condition": "remote_annotated_tag_matches_exact_validated_commit",
        "tag_object": PUBLISHED_TAG_OBJECT,
        "tagged_commit": PUBLISHED_COMMIT,
        "evidence": PUBLISHED_EVIDENCE,
    }
    record["gates"] = {
        gate: {
            "state": "closed",
            "evidence": [PUBLISHED_EVIDENCE],
        }
        for gate in GATE_IDS
    }
    record["mapping_decision_basis"] = "owner_risk_acceptance"
    return record


def publication_timestamp() -> str:
    return f"{datetime.now(timezone.utc).date().isoformat()}T12:00:00Z"


def owner_source(created_at: str) -> dict[str, object]:
    return {
        "repository": "tdistress/ESAF",
        "comment_url": "https://github.com/tdistress/ESAF/pull/51#issuecomment-1001",
        "comment_id": 1001,
        "author_login": "tdistress",
        "author_user_id": 2001,
        "author_association": "OWNER",
        "created_at": created_at,
        "updated_at": created_at,
        "body_sha256": "a" * 64,
        "source_verified_at": publication_timestamp(),
    }


def limitations() -> dict[str, object]:
    return {"lifecycle": "draft", "claims_not_made": sorted(CLAIMS_NOT_MADE)}


def mapping_decisions(closure: str, basis: str) -> list[dict[str, object]]:
    decided_at = publication_timestamp()
    if basis == "qualified_approval":
        return [
            {
                "mapping_set_id": mapping_set_id,
                "decision_type": basis,
                "sha": closure,
                "decided_at": decided_at,
                "url": f"https://github.com/tdistress/ESAF/pull/51#issuecomment-{1100 + index}",
                "reviewer": f"qualified-reviewer-{index}",
                "qualification": "documented scheme and ESAF qualification",
                "disposition": "approved",
                "qualified_review_status": "completed",
                "limitations": limitations(),
            }
            for index, mapping_set_id in enumerate(EXPECTED_MAPPING_SETS, start=1)
        ]
    source = owner_source(decided_at)
    return [
        {
            "mapping_set_id": mapping_set_id,
            "decision_type": basis,
            "sha": closure,
            "decided_at": decided_at,
            "url": source["comment_url"],
            "owner_login": source["author_login"],
            "owner_user_id": source["author_user_id"],
            "role": "repository_owner",
            "author_association": "OWNER",
            "disposition": "accepted_for_working_draft",
            "qualified_review_status": "deferred",
            "limitations": limitations(),
            "source": deepcopy(source),
        }
        for mapping_set_id in EXPECTED_MAPPING_SETS
    ]


def approved_external_evidence(
    closure: str, merge: str | None = None, basis: str = "qualified_approval",
) -> dict[str, object]:
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
        "mapping_decision_schema": "esaf-mapping-decisions-v1",
        "mapping_decision_basis": basis,
        "mapping_decisions": mapping_decisions(closure, basis),
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
    if basis == "owner_risk_acceptance":
        source = owner_source(publication_timestamp())
        evidence["scope"] = {
            "approval_basis": basis,
            "sha": closure,
            "owner_login": source["author_login"],
            "owner_user_id": source["author_user_id"],
            "role": "repository_owner",
            "author_association": "OWNER",
            "decided_at": source["created_at"],
            "scope": "complete_git_tracked_repository",
            "limitations": limitations(),
            "source": deepcopy(source),
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
    def test_tracked_closure_record_has_ready_https_gates_and_owner_risk_basis(self) -> None:
        record = load_front_matter(RECORD)
        self.assertEqual("closure_candidate", record["phase"])
        self.assertEqual("owner_risk_acceptance", record["mapping_decision_basis"])
        self.assertEqual(datetime.now(timezone.utc).date(), record["publication"]["date"])
        self.assertEqual(validate_record(ROOT, record), [])
        for gate, value in record["gates"].items():
            with self.subTest(gate=gate):
                self.assertEqual("ready", value["state"])
                self.assertTrue(value["evidence"])
                self.assertTrue(all(locator.startswith("https://") for locator in value["evidence"]))

    def test_authoritative_record_is_valid(self) -> None:
        self.assertEqual(validate_record(ROOT, load_front_matter(RECORD)), [])

    def test_published_record_accepts_fixed_historical_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_published_scope_fixture(root)
            self.assertEqual(validate_record(root, published_record()), [])

    def test_published_record_rejects_mutated_publication_evidence(self) -> None:
        cases = (
            ("date", "2026-07-24", "published date shall equal 2026-07-23"),
            ("tag_object", "a" * 40, "published tag object is invalid"),
            ("tagged_commit", "b" * 40, "published tagged commit is invalid"),
            ("evidence", "http://example.test/evidence", "published evidence locator is invalid"),
        )
        for field, value, diagnostic in cases:
            with self.subTest(field=field):
                record = published_record()
                record["publication"][field] = value
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    write_published_scope_fixture(root)
                    self.assertIn(diagnostic, validate_record(root, record))

    def test_published_record_requires_every_gate_closed(self) -> None:
        record = published_record()
        record["gates"]["technical"]["state"] = "ready"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_published_scope_fixture(root)
            self.assertIn(
                "technical: published gate shall be closed",
                validate_record(root, record),
            )

    def test_published_cli_requires_no_baseline_and_rejects_external_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_published_scope_fixture(root)
            (root / "tools").mkdir()
            (root / "docs/superpowers/reviews").mkdir(parents=True)
            shutil.copy2(ROOT / "tools/release_gates.py", root / "tools/release_gates.py")
            record_path = root / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
            record_path.write_text("---\n" + yaml.safe_dump(published_record(), sort_keys=False) + "---\n", encoding="utf-8")
            evidence_path = root / "external-evidence.json"
            evidence_path.write_text("{}\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(root / "tools/release_gates.py"), "--check"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            external_result = subprocess.run(
                [
                    sys.executable,
                    str(root / "tools/release_gates.py"),
                    "--check",
                    "--external-evidence",
                    str(evidence_path),
                    "--expected-head",
                    "a" * 40,
                    "--phase",
                    "closure",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0)
        self.assertNotEqual(external_result.returncode, 0)
        self.assertIn(
            "external evidence is not accepted for a published record",
            external_result.stdout,
        )

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

    def test_candidate_records_reject_published_sha_fields(self) -> None:
        for phase, record in (
            ("evidence_candidate", valid_record()),
            ("closure_candidate", closure_record()),
        ):
            with self.subTest(phase=phase):
                record["publication"]["tag_object"] = PUBLISHED_TAG_OBJECT
                record["publication"]["tagged_commit"] = PUBLISHED_COMMIT
                errors = validate_record(ROOT, record)
                self.assertIn(
                    "publication.tag_object: tracked record shall not contain a 40-character SHA",
                    errors,
                )
                self.assertIn(
                    "publication.tagged_commit: tracked record shall not contain SHA fields",
                    errors,
                )

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
        evidence["mapping_decisions"] = []
        errors = validate_external_evidence(record, evidence, expected_merge, "taggable")
        self.assertIn("governance approval is not bound to closure head", errors)
        self.assertIn("mapping decisions shall contain each expected mapping set exactly once", errors)

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
            ("duplicate_mapping", lambda e: e["mapping_decisions"].append(deepcopy(e["mapping_decisions"][0])), "mapping decisions shall contain each expected mapping set exactly once"),
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

    def test_closure_record_requires_supported_mapping_decision_basis(self) -> None:
        for value in (None, "legacy"):
            with self.subTest(value=value):
                record = closure_record()
                if value is None:
                    record.pop("mapping_decision_basis")
                else:
                    record["mapping_decision_basis"] = value
                self.assertIn(
                    "closure candidate mapping_decision_basis shall be supported",
                    validate_record(ROOT, record),
                )
        self.assertEqual(validate_record(ROOT, valid_record()), [])

    def test_both_uniform_mapping_decision_bases_pass_closure_and_taggable(self) -> None:
        closure = "d" * 40
        merge = "f" * 40
        for basis in ("qualified_approval", "owner_risk_acceptance"):
            with self.subTest(basis=basis, phase="closure"):
                self.assertEqual(
                    validate_external_evidence(
                        closure_record(basis), approved_external_evidence(closure, basis=basis), closure, "closure"
                    ), [],
                )
            with self.subTest(basis=basis, phase="taggable"):
                self.assertEqual(
                    validate_external_evidence(
                        closure_record(basis), approved_external_evidence(closure, merge, basis), merge, "taggable"
                    ), [],
                )

    def test_mapping_decisions_require_v1_schema_and_uniform_basis(self) -> None:
        closure = "d" * 40
        cases = (
            ("schema", lambda e: e.__setitem__("mapping_decision_schema", "legacy"), "mapping decision schema shall equal esaf-mapping-decisions-v1"),
            ("mixed", lambda e: e["mapping_decisions"][0].__setitem__("decision_type", "owner_risk_acceptance"), "mapping decisions shall uniformly match mapping_decision_basis"),
            ("duplicate", lambda e: e["mapping_decisions"].append(deepcopy(e["mapping_decisions"][0])), "mapping decisions shall contain each expected mapping set exactly once"),
        )
        for name, mutate, diagnostic in cases:
            with self.subTest(name=name):
                evidence = approved_external_evidence(closure)
                mutate(evidence)
                self.assertIn(diagnostic, validate_external_evidence(closure_record(), evidence, closure, "closure"))

    def test_legacy_mapping_reviews_are_rejected(self) -> None:
        closure = "d" * 40
        evidence = approved_external_evidence(closure)
        evidence["mapping_reviews"] = []
        self.assertIn(
            "legacy mapping_reviews are not accepted",
            validate_external_evidence(closure_record(), evidence, closure, "closure"),
        )

    def test_closure_record_and_external_evidence_require_the_same_basis(self) -> None:
        closure = "d" * 40
        self.assertIn(
            "external mapping decision basis shall match the closure record",
            validate_external_evidence(
                closure_record("owner_risk_acceptance"), approved_external_evidence(closure), closure, "closure"
            ),
        )

    def test_global_mutations_apply_to_both_bases_and_phases(self) -> None:
        closure, merge = "d" * 40, "f" * 40
        mutations = (
            ("missing_check", lambda e: e.pop("github_checks"), "GitHub checks are required"),
            ("failed_check", lambda e: e["github_checks"]["observed"][0].__setitem__("conclusion", "failure"), "GitHub check conclusion shall be success"),
            ("dirty_merge", lambda e: e["merge_state"].__setitem__("state", "dirty"), "merge state shall be clean"),
            ("unmergeable", lambda e: e["merge_state"].__setitem__("mergeable", False), "merge state shall be mergeable"),
            ("governance_authority", lambda e: e["governance"].__setitem__("authority", "repository owner"), "governance authority is not authorized"),
            ("stale_closure_sha", lambda e: e["mapping_decisions"][0].__setitem__("sha", "a" * 40), "mapping decision is not bound to closure head"),
        )
        for basis in ("qualified_approval", "owner_risk_acceptance"):
            for phase, expected, merged in (("closure", closure, None), ("taggable", merge, merge)):
                for name, mutate, diagnostic in mutations:
                    with self.subTest(basis=basis, phase=phase, name=name):
                        evidence = approved_external_evidence(closure, merged, basis)
                        mutate(evidence)
                        self.assertIn(diagnostic, validate_external_evidence(closure_record(basis), evidence, expected, phase))

    def test_qualified_mapping_decision_fields_are_strict(self) -> None:
        closure = "d" * 40
        mutations = (
            (lambda d: d.__setitem__("reviewer", ""), "qualified mapping reviewer shall be named"),
            (lambda d: d.__setitem__("qualification", ""), "qualified mapping reviewer shall be qualified"),
            (lambda d: d.__setitem__("disposition", "deferred"), "qualified mapping disposition shall be approved"),
            (lambda d: d.__setitem__("qualified_review_status", "deferred"), "qualified review status shall be completed"),
            (lambda d: d.__setitem__("decided_at", "today"), "mapping decision timestamp shall be RFC 3339"),
            (lambda d: d.__setitem__("url", "http://example.invalid"), "mapping decision URL shall use HTTPS"),
            (lambda d: d["limitations"].__setitem__("lifecycle", "released"), "mapping decision lifecycle shall equal draft"),
            (lambda d: d["limitations"].__setitem__("claims_not_made", []), "mapping decision prohibited claims shall equal the required set"),
            (lambda d: d.__setitem__("owner_risk_wording", "owner_risk_acceptance deferred repository owner publication basis"), "qualified mapping decision shall not contain owner-risk wording"),
        )
        for mutate, diagnostic in mutations:
            evidence = approved_external_evidence(closure)
            mutate(evidence["mapping_decisions"][0])
            self.assertIn(diagnostic, validate_external_evidence(closure_record(), evidence, closure, "closure"))

    def test_mapping_timestamp_uses_utc_publication_date(self) -> None:
        closure = "d" * 40
        record = closure_record()
        record["publication"]["date"] = "2026-07-24"
        evidence = approved_external_evidence(closure)
        for item in evidence["mapping_decisions"]:
            item["decided_at"] = "2026-07-23T23:30:00-02:00"
        self.assertNotIn(
            "mapping decision UTC date shall equal conditional publication date",
            validate_external_evidence(record, evidence, closure, "closure"),
        )

    def test_owner_risk_fields_and_scope_are_strict(self) -> None:
        closure = "d" * 40
        mutations = (
            (lambda e: e["mapping_decisions"][0].__setitem__("author_association", "MEMBER"), "owner mapping author association shall be OWNER"),
            (lambda e: e["mapping_decisions"][0].__setitem__("owner_login", ""), "owner mapping login shall be named"),
            (lambda e: e["mapping_decisions"][0].__setitem__("owner_user_id", True), "owner mapping user ID shall be numeric"),
            (lambda e: e["mapping_decisions"][0].__setitem__("role", "reviewer"), "owner mapping role shall equal repository_owner"),
            (lambda e: e["mapping_decisions"][0].__setitem__("disposition", "approved"), "owner mapping disposition shall be accepted_for_working_draft"),
            (lambda e: e["mapping_decisions"][0].__setitem__("qualified_review_status", "completed"), "owner mapping qualified review status shall be deferred"),
            (lambda e: e["mapping_decisions"][0]["source"].__setitem__("body_sha256", "edited"), "owner mapping source body digest shall be a SHA-256"),
            (lambda e: [source.__setitem__("author_login", "attacker") for source in [*(item["source"] for item in e["mapping_decisions"]), e["scope"]["source"]]], "owner mapping source login shall equal tdistress"),
            (lambda e: [source.__setitem__("comment_url", "https://example.invalid/not-a-github-comment") for source in [*(item["source"] for item in e["mapping_decisions"]), e["scope"]["source"]]], "owner mapping source comment URL shall use GitHub HTTPS"),
            (lambda e: e["scope"].__setitem__("scope", "mapping_sets_only"), "owner scope shall equal complete_git_tracked_repository"),
            (lambda e: e["scope"]["limitations"].__setitem__("claims_not_made", []), "scope prohibited claims shall equal the required set"),
        )
        for mutate, diagnostic in mutations:
            evidence = approved_external_evidence(closure, basis="owner_risk_acceptance")
            mutate(evidence)
            self.assertIn(diagnostic, validate_external_evidence(closure_record("owner_risk_acceptance"), evidence, closure, "closure"))

    def test_owner_risk_rejects_pr_a_head_rebinding_in_both_phases(self) -> None:
        closure, merge, old_pr_a_head = "d" * 40, "f" * 40, "a" * 40
        for phase, expected in (("closure", closure), ("taggable", merge)):
            with self.subTest(phase=phase):
                evidence = approved_external_evidence(closure, merge if phase == "taggable" else None, "owner_risk_acceptance")
                evidence["scope"]["sha"] = old_pr_a_head
                for decision in evidence["mapping_decisions"]:
                    decision["sha"] = old_pr_a_head
                errors = validate_external_evidence(closure_record("owner_risk_acceptance"), evidence, expected, phase)
                self.assertIn("scope approval is not bound to closure head", errors)
                self.assertIn("mapping decision is not bound to closure head", errors)
