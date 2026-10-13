from __future__ import annotations

from copy import deepcopy
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.v019_draft_release_gates import (
    GATE_IDS,
    PHASE_GATE_STATES,
    RECORD_RELATIVE,
    validate_candidate_binding,
    validate_record,
    validate_baseline_from_record,
    validate_evidence_candidate_baseline,
    main,
    validate_transition,
)


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


TEMP_DIRS: list[tempfile.TemporaryDirectory] = []


def init_repo() -> Path:
    temp = tempfile.TemporaryDirectory()
    TEMP_DIRS.append(temp)
    repo = Path(temp.name)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    git(repo, "config", "user.email", "release-test@example.invalid")
    git(repo, "config", "user.name", "Release Test")
    return repo


def readiness(phase: str, base_sha: str) -> dict:
    return {
        "release": "v0.19-draft",
        "phase": phase,
        "tag": "v0.19-draft",
        "milestone": "v0.19-draft",
        "issue": 228,
        "version_advanced": False,
        "deliverable": "one_fictional_api100_assessment_follow_up_cycle",
        "qualified_crosswalk_review_required": False,
        "base_sha": base_sha,
        "publication": {
            "condition": "annotated_tag_targets_validated_closure_candidate",
            "tag_object": None,
            "tagged_commit": None,
            "date": None,
            "evidence": [],
        },
        "gates": {
            gate: {
                "state": state,
                "evidence": [] if gate in {"post_merge", "standards_mapping"} else ["https://example.invalid/evidence"],
            }
            for gate, state in PHASE_GATE_STATES[phase].items()
        },
    }


def save_commit(repo: Path, record: dict, message: str) -> str:
    path = repo / RECORD_RELATIVE
    path.parent.mkdir(parents=True, exist_ok=True)
    import yaml
    body = "\n# v0.19-draft publication readiness\n\n## Scope\n\n## Mandatory gates\n\n## Lifecycle boundary\n\n## Publication evidence\n"
    path.write_text("---\n" + yaml.safe_dump(record, sort_keys=False) + "---\n" + body, encoding="utf-8")
    git(repo, "add", RECORD_RELATIVE)
    subprocess.run(["git", "commit", "-qm", message], cwd=repo, check=True)
    return git(repo, "rev-parse", "HEAD^{commit}")


class V019ReleaseGateContractTests(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        for temp in TEMP_DIRS:
            temp.cleanup()
        TEMP_DIRS.clear()

    def test_valid_phase_records_and_scope_identity(self):
        repo = init_repo()
        base = save_commit(repo, readiness("evidence_candidate", "0" * 40), "candidate")
        for phase in ("evidence_candidate", "closure_candidate", "published"):
            record = readiness(phase, base)
            if phase == "published":
                record["gates"] = {gate: {"state": state, "evidence": [] if gate == "standards_mapping" else ["https://example.invalid/closed"]} for gate, state in PHASE_GATE_STATES["published"].items()}
                record["publication"].update({"tag_object": "a" * 40, "tagged_commit": "b" * 40, "date": "2026-10-13", "evidence": ["https://example.invalid/publication"]})
            self.assertEqual([], validate_record(repo, record))
        wrong = readiness("evidence_candidate", base)
        wrong["deliverable"] = "two_assessment_cases"
        self.assertTrue(any("deliverable" in error for error in validate_record(repo, wrong)))
        wrong_gate = readiness("closure_candidate", base)
        wrong_gate["gates"]["technical"]["state"] = "open"
        self.assertTrue(any("technical" in error for error in validate_record(repo, wrong_gate)))

    def test_candidate_readiness_must_match_committed_head(self):
        repo = init_repo()
        base = save_commit(repo, readiness("evidence_candidate", "0" * 40), "candidate")
        committed = (repo / RECORD_RELATIVE).read_text(encoding="utf-8")
        self.assertEqual([], validate_candidate_binding(repo, committed))
        (repo / "unrelated.tmp").write_text("allowed", encoding="utf-8")
        self.assertEqual([], validate_candidate_binding(repo, committed))
        edited = committed + "uncommitted\n"
        self.assertTrue(any("differs from committed HEAD" in error for error in validate_candidate_binding(repo, edited)))

    def test_transition_requires_exact_ancestor_baseline_and_correct_phase(self):
        repo = init_repo()
        base = save_commit(repo, readiness("evidence_candidate", "0" * 40), "evidence candidate")
        candidate = readiness("closure_candidate", base)
        save_commit(repo, candidate, "closure candidate")
        self.assertEqual([], validate_transition(repo, base, candidate))
        self.assertTrue(any("transition only from evidence_candidate" in error for error in validate_transition(repo, git(repo, "rev-parse", "HEAD"), candidate)))
        mismatched = deepcopy(candidate)
        mismatched["base_sha"] = "f" * 40
        self.assertTrue(any("base_sha shall equal the exact baseline" in error for error in validate_transition(repo, base, mismatched)))
        subprocess.run(["git", "checkout", "--orphan", "unrelated"], cwd=repo, check=True, capture_output=True)
        (repo / "unrelated.txt").write_text("unrelated history\n", encoding="utf-8")
        git(repo, "add", "unrelated.txt")
        subprocess.run(["git", "commit", "-qm", "unrelated root"], cwd=repo, check=True)
        self.assertTrue(any("exact baseline SHA shall be an ancestor" in error for error in validate_transition(repo, base, candidate)))

    def test_published_requires_annotated_tag_targeting_closure_candidate_and_immutable_maintenance(self):
        repo = init_repo()
        base = save_commit(repo, readiness("evidence_candidate", "0" * 40), "evidence candidate")
        closure = readiness("closure_candidate", base)
        closure_sha = save_commit(repo, closure, "closure candidate")
        git(repo, "tag", "-a", "v0.19-draft", "-m", "v0.19-draft")
        tag_object = git(repo, "rev-parse", "refs/tags/v0.19-draft")
        published = readiness("published", closure_sha)
        published["gates"] = {gate: {"state": state, "evidence": [] if gate == "standards_mapping" else ["https://example.invalid/closed"]} for gate, state in PHASE_GATE_STATES["published"].items()}
        published["publication"].update({"tag_object": tag_object, "tagged_commit": closure_sha, "date": "2026-10-13", "evidence": ["https://example.invalid/publication"]})
        published_sha = save_commit(repo, published, "published status")
        self.assertEqual([], validate_transition(repo, closure_sha, published))
        bad_target = deepcopy(published)
        bad_target["publication"]["tagged_commit"] = "f" * 40
        self.assertTrue(any("tagged commit is stale or mismatched" in error or "equal the exact closure_candidate baseline SHA" in error for error in validate_transition(repo, closure_sha, bad_target)))
        maintenance = deepcopy(published)
        maintenance["base_sha"] = published_sha
        save_commit(repo, maintenance, "maintenance")
        self.assertEqual([], validate_transition(repo, published_sha, maintenance))
        mutated = deepcopy(maintenance)
        mutated["publication"]["date"] = "2026-10-14"
        self.assertTrue(any("identity and closed gate truth" in error for error in validate_transition(repo, published_sha, mutated)))
        mutated_gate = deepcopy(maintenance)
        mutated_gate["gates"]["technical"]["evidence"] = ["https://example.invalid/changed"]
        self.assertTrue(any("identity and closed gate truth" in error for error in validate_transition(repo, published_sha, mutated_gate)))
        git(repo, "tag", "-d", "v0.19-draft")
        subprocess.run(["git", "tag", "v0.19-draft", closure_sha], cwd=repo, check=True)
        self.assertTrue(any("shall be annotated" in error for error in validate_transition(repo, closure_sha, published)))

    def test_evidence_candidate_cannot_regress_published_baseline(self):
        repo = init_repo()
        base = save_commit(repo, readiness("evidence_candidate", "0" * 40), "evidence candidate")
        closure = readiness("closure_candidate", base)
        closure_sha = save_commit(repo, closure, "closure candidate")
        git(repo, "tag", "-a", "v0.19-draft", "-m", "v0.19-draft")
        tag_object = git(repo, "rev-parse", "refs/tags/v0.19-draft")
        published = readiness("published", closure_sha)
        published["gates"] = {gate: {"state": state, "evidence": [] if gate == "standards_mapping" else ["https://example.invalid/closed"]} for gate, state in PHASE_GATE_STATES["published"].items()}
        published["publication"].update({"tag_object": tag_object, "tagged_commit": closure_sha, "date": "2026-10-13", "evidence": ["https://example.invalid/publication"]})
        published_sha = save_commit(repo, published, "published status")
        regression = readiness("evidence_candidate", published_sha)
        save_commit(repo, regression, "invalid regression")
        errors = validate_baseline_from_record(repo, regression)
        self.assertTrue(any("shall not reopen a prior v0.19 readiness phase" in error for error in errors))
        old_base_regression = readiness("evidence_candidate", base)
        save_commit(repo, old_base_regression, "invalid old-base regression")
        errors = validate_baseline_from_record(repo, old_base_regression)
        self.assertTrue(any("shall not reopen a prior v0.19 readiness phase" in error for error in errors))
        explicit_errors = validate_evidence_candidate_baseline(repo, base)
        self.assertTrue(any("shall not reopen a prior v0.19 readiness phase" in error for error in explicit_errors))
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = main(["--check", "--baseline-ref", base], root=repo)
        self.assertEqual(1, result)
        self.assertIn("shall not reopen a prior v0.19 readiness phase", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
