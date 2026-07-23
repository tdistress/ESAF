from __future__ import annotations

from copy import deepcopy
from contextlib import redirect_stderr
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from tools.owner_risk_evidence import (
    build_external_evidence,
    main,
    parse_owner_decision,
    refresh_taggable_evidence,
    verify_owner_comment,
)
from tools.release_gates import CLAIMS_NOT_MADE, EXPECTED_MAPPING_SETS, POST_MERGE_COMMANDS


HEAD = "d" * 40
MERGE = "f" * 40
PUBLICATION_DATE = datetime.now(timezone.utc).date().isoformat()
TIMESTAMP = f"{PUBLICATION_DATE}T12:00:00Z"


def decision() -> dict[str, object]:
    return {
        "decision_type": "owner_risk_acceptance",
        "sha": HEAD,
        "mapping_set_ids": list(EXPECTED_MAPPING_SETS),
        "disposition": "accepted_for_working_draft",
        "qualified_review_status": "deferred",
        "scope": "complete_git_tracked_repository",
        "lifecycle": "draft",
        "claims_not_made": sorted(CLAIMS_NOT_MADE),
    }


def owner_comment(body: str | None = None) -> dict[str, object]:
    payload = body or "```json\n" + json.dumps(decision()) + "\n```\n\nThis is an owner risk acceptance for the working draft."
    return {
        "repository_url": "https://api.github.com/repos/tdistress/ESAF",
        "html_url": "https://github.com/tdistress/ESAF/pull/51#issuecomment-1001",
        "id": 1001,
        "user": {"login": "tdistress", "id": 2001},
        "author_association": "OWNER",
        "created_at": TIMESTAMP,
        "updated_at": TIMESTAMP,
        "body": payload,
    }


def verdicts() -> dict[str, dict[str, object]]:
    date = PUBLICATION_DATE
    def review(name: str, number: int) -> dict[str, object]:
        return {
            "sha": HEAD,
            "reviewer": f"{name}-reviewer",
            "date": date,
            "disposition": "approved",
            "url": f"https://github.com/tdistress/ESAF/pull/51#issuecomment-{number}",
            "critical": 0,
            "important": 0,
            "method": "independent review",
            "result": "passed",
        }
    return {
        "technical": review("technical", 2),
        "editorial": review("editorial", 3),
        "rendering": review("rendering", 4),
        "governance": {
            **review("governance", 5),
            "approver": "governance-approver",
            "authority": "Steering Committee",
        },
    }


def pr_state() -> dict[str, object]:
    return {
        "headRefOid": HEAD,
        "mergeable": "MERGEABLE",
        "mergeStateStatus": "CLEAN",
        "statusCheckRollup": [{
            "name": "Validate ESAF sources",
            "conclusion": "SUCCESS",
            "detailsUrl": "https://github.com/tdistress/ESAF/actions/runs/1",
        }],
    }


def post_merge() -> dict[str, object]:
    return {
        "sha": MERGE,
        "commands": [
            {"name": name, "exit_code": 0, "result": "passed"}
            for name in POST_MERGE_COMMANDS
        ],
    }


def verdict_comment(name: str, number: int) -> dict[str, object]:
    body = deepcopy(verdicts()[name])
    body.pop("url")
    return {
        "html_url": f"https://github.com/tdistress/ESAF/pull/51#issuecomment-{number}",
        "body": "```json\n" + json.dumps(body) + "\n```\n",
    }


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


class OwnerRiskEvidenceTests(unittest.TestCase):
    def test_parse_owner_decision_accepts_exactly_one_json_fence(self) -> None:
        self.assertEqual(parse_owner_decision(owner_comment()["body"]), decision())
        for body in ("no decision", "```json\n{}\n```\n```json\n{}\n```", "```json\n{\n```"):
            with self.subTest(body=body):
                with self.assertRaises(ValueError):
                    parse_owner_decision(body)

    def test_verify_owner_comment_derives_source_from_fetched_comment(self) -> None:
        source = verify_owner_comment(owner_comment(), HEAD, PUBLICATION_DATE, TIMESTAMP)
        self.assertEqual(source["repository"], "tdistress/ESAF")
        self.assertEqual(source["comment_id"], 1001)
        self.assertEqual(source["body_sha256"], hashlib.sha256(owner_comment()["body"].encode()).hexdigest())
        self.assertEqual(source["source_verified_at"], TIMESTAMP)

    def test_verify_owner_comment_rejects_each_owner_invariant(self) -> None:
        cases = (
            ("missing", lambda c: c.pop("body")),
            ("sha", lambda c: c.__setitem__("body", c["body"].replace(HEAD, "a" * 40))),
            ("duplicate", lambda c: c.__setitem__("body", c["body"] + "\n```json\n{}\n```")),
            ("mapping", lambda c: c.__setitem__("body", "```json\n" + json.dumps({**decision(), "mapping_set_ids": []}) + "\n```")),
            ("repository", lambda c: c.__setitem__("repository_url", "https://api.github.com/repos/example/ESAF")),
            ("comment_id", lambda c: c.__setitem__("id", True)),
            ("user_id", lambda c: c["user"].__setitem__("id", "2001")),
            ("login", lambda c: c["user"].__setitem__("login", "other")),
            ("association", lambda c: c.__setitem__("author_association", "MEMBER")),
            ("timestamp", lambda c: c.__setitem__("created_at", "today")),
            ("date", lambda c: c.__setitem__("created_at", "2000-01-01T00:00:00Z")),
        )
        for name, mutate in cases:
            with self.subTest(name=name):
                comment = owner_comment()
                mutate(comment)
                with self.assertRaises(ValueError):
                    verify_owner_comment(comment, HEAD, PUBLICATION_DATE, TIMESTAMP)

    def test_verify_owner_comment_rejects_every_structured_decision_mutation(self) -> None:
        def set_decision(comment: dict[str, object], **changes: object) -> None:
            comment["body"] = "```json\n" + json.dumps({**decision(), **changes}) + "\n```"

        cases = (
            ("missing_mapping", lambda c: set_decision(c, mapping_set_ids=list(EXPECTED_MAPPING_SETS[:-1]))),
            ("duplicate_mapping", lambda c: set_decision(c, mapping_set_ids=[EXPECTED_MAPPING_SETS[0]] * 3)),
            ("extra_mapping", lambda c: set_decision(c, mapping_set_ids=[*EXPECTED_MAPPING_SETS[:2], "extra"])),
            ("scope", lambda c: set_decision(c, scope="mapping_sets_only")),
            ("lifecycle", lambda c: set_decision(c, lifecycle="released")),
            ("incomplete_claims", lambda c: set_decision(c, claims_not_made=sorted(CLAIMS_NOT_MADE)[:-1])),
            ("extra_claim", lambda c: set_decision(c, claims_not_made=[*sorted(CLAIMS_NOT_MADE)[:-1], "extra"])),
            ("type", lambda c: set_decision(c, decision_type="qualified_approval")),
            ("disposition", lambda c: set_decision(c, disposition="approved")),
            ("review_status", lambda c: set_decision(c, qualified_review_status="completed")),
        )
        for name, mutate in cases:
            with self.subTest(name=name):
                comment = owner_comment()
                mutate(comment)
                with self.assertRaises(ValueError):
                    verify_owner_comment(comment, HEAD, PUBLICATION_DATE, TIMESTAMP)

    def test_verify_owner_comment_tracks_updated_and_edited_body_digest(self) -> None:
        original = verify_owner_comment(owner_comment(), HEAD, PUBLICATION_DATE, TIMESTAMP)
        edited = owner_comment()
        edited["updated_at"] = f"{PUBLICATION_DATE}T13:00:00Z"
        edited["body"] += "\nEditorial clarification."
        refreshed = verify_owner_comment(edited, HEAD, PUBLICATION_DATE, f"{PUBLICATION_DATE}T13:00:00Z")
        self.assertEqual(refreshed["updated_at"], edited["updated_at"])
        self.assertEqual(refreshed["source_verified_at"], f"{PUBLICATION_DATE}T13:00:00Z")
        self.assertNotEqual(refreshed["body_sha256"], original["body_sha256"])
        for field in ("updated_at", "source_verified_at"):
            with self.subTest(field=field):
                comment = owner_comment()
                if field == "updated_at":
                    comment[field] = "not-a-timestamp"
                    verified_at = TIMESTAMP
                else:
                    verified_at = "not-a-timestamp"
                with self.assertRaises(ValueError):
                    verify_owner_comment(comment, HEAD, PUBLICATION_DATE, verified_at)

    def test_build_external_evidence_assembles_complete_v1_contract(self) -> None:
        source = verify_owner_comment(owner_comment(), HEAD, PUBLICATION_DATE, TIMESTAMP)
        evidence = build_external_evidence(source, HEAD, verdicts(), pr_state())
        self.assertEqual(evidence["mapping_decision_schema"], "esaf-mapping-decisions-v1")
        self.assertEqual(evidence["mapping_decision_basis"], "owner_risk_acceptance")
        self.assertEqual(len(evidence["mapping_decisions"]), 3)
        self.assertEqual(evidence["scope"]["source"], source)
        self.assertTrue(all(item["source"] == source for item in evidence["mapping_decisions"]))
        self.assertEqual(evidence["technical"], verdicts()["technical"])
        self.assertEqual(evidence["github_checks"]["observed"][0]["conclusion"], "success")
        self.assertEqual(evidence["merge_state"], {"sha": HEAD, "mergeable": True, "state": "clean"})

    def test_build_external_evidence_rejects_missing_verdict_or_pr_state_field(self) -> None:
        source = verify_owner_comment(owner_comment(), HEAD, PUBLICATION_DATE, TIMESTAMP)
        for name in ("technical", "editorial", "rendering", "governance"):
            with self.subTest(name=name):
                supplied = verdicts()
                supplied.pop(name)
                with self.assertRaises(ValueError):
                    build_external_evidence(source, HEAD, supplied, pr_state())
        for field in ("headRefOid", "mergeable", "mergeStateStatus", "statusCheckRollup"):
            with self.subTest(field=field):
                state = pr_state()
                state.pop(field)
                with self.assertRaises(ValueError):
                    build_external_evidence(source, HEAD, verdicts(), state)

    def test_refresh_taggable_evidence_preserves_closure_objects(self) -> None:
        source = verify_owner_comment(owner_comment(), HEAD, PUBLICATION_DATE, TIMESTAMP)
        base = build_external_evidence(source, HEAD, verdicts(), pr_state())
        refreshed_comment = owner_comment()
        refreshed_comment["updated_at"] = f"{PUBLICATION_DATE}T13:00:00Z"
        refreshed = verify_owner_comment(refreshed_comment, HEAD, PUBLICATION_DATE, f"{PUBLICATION_DATE}T13:00:00Z")
        results = post_merge()
        evidence = refresh_taggable_evidence(base, refreshed, MERGE, results)
        self.assertEqual(evidence["closure_head"], HEAD)
        for name in ("technical", "editorial", "rendering", "governance", "github_checks", "merge_state"):
            with self.subTest(name=name):
                self.assertEqual(evidence[name], base[name])
        self.assertTrue(all(item["source"] == refreshed for item in evidence["mapping_decisions"]))
        self.assertEqual(evidence["scope"]["source"], refreshed)
        self.assertEqual(evidence["merge_head"], MERGE)
        self.assertEqual(evidence["post_merge"], results)

    def test_refresh_taggable_evidence_rejects_incomplete_or_invalid_closure_base(self) -> None:
        source = verify_owner_comment(owner_comment(), HEAD, PUBLICATION_DATE, TIMESTAMP)
        base = build_external_evidence(source, HEAD, verdicts(), pr_state())
        cases = (
            ("schema", lambda e: e.pop("mapping_decision_schema")),
            ("mapping_decisions", lambda e: e.__setitem__("mapping_decisions", [])),
            ("mapping_binding", lambda e: e["mapping_decisions"][0].__setitem__("sha", "a" * 40)),
            ("mapping_missing_lifecycle", lambda e: e["mapping_decisions"][0]["limitations"].pop("lifecycle")),
            ("mapping_wrong_lifecycle", lambda e: e["mapping_decisions"][0]["limitations"].__setitem__("lifecycle", "released")),
            ("mapping_missing_claims", lambda e: e["mapping_decisions"][0]["limitations"].pop("claims_not_made")),
            ("mapping_extra_claim", lambda e: e["mapping_decisions"][0]["limitations"]["claims_not_made"].append("extra")),
            ("mapping_duplicate_claim", lambda e: e["mapping_decisions"][0]["limitations"]["claims_not_made"].__setitem__(-1, e["mapping_decisions"][0]["limitations"]["claims_not_made"][0])),
            ("scope", lambda e: e.pop("scope")),
            ("scope_binding", lambda e: e["scope"].__setitem__("sha", "a" * 40)),
            ("scope_missing_lifecycle", lambda e: e["scope"]["limitations"].pop("lifecycle")),
            ("scope_wrong_lifecycle", lambda e: e["scope"]["limitations"].__setitem__("lifecycle", "released")),
            ("scope_missing_claims", lambda e: e["scope"]["limitations"].pop("claims_not_made")),
            ("scope_extra_claim", lambda e: e["scope"]["limitations"]["claims_not_made"].append("extra")),
            ("scope_duplicate_claim", lambda e: e["scope"]["limitations"]["claims_not_made"].__setitem__(-1, e["scope"]["limitations"]["claims_not_made"][0])),
            ("technical", lambda e: e.pop("technical")),
            ("technical_binding", lambda e: e["technical"].__setitem__("sha", "a" * 40)),
            ("editorial", lambda e: e.pop("editorial")),
            ("rendering", lambda e: e.pop("rendering")),
            ("governance", lambda e: e.pop("governance")),
            ("checks", lambda e: e.pop("github_checks")),
            ("check_binding", lambda e: e["github_checks"]["observed"][0].__setitem__("sha", "a" * 40)),
            ("merge_state", lambda e: e.pop("merge_state")),
            ("merge_binding", lambda e: e["merge_state"].__setitem__("sha", "a" * 40)),
            ("merge_evidence", lambda e: e.__setitem__("merge_head", MERGE)),
            ("legacy_mapping_reviews", lambda e: e.__setitem__("mapping_reviews", [])),
        )
        for name, mutate in cases:
            with self.subTest(name=name):
                candidate = deepcopy(base)
                mutate(candidate)
                with self.assertRaises(ValueError):
                    refresh_taggable_evidence(candidate, source, MERGE, post_merge())

    def test_refresh_taggable_evidence_rejects_every_preserved_verdict_date_mutation(self) -> None:
        source = verify_owner_comment(owner_comment(), HEAD, PUBLICATION_DATE, TIMESTAMP)
        base = build_external_evidence(source, HEAD, verdicts(), pr_state())
        for verdict in ("technical", "editorial", "rendering", "governance"):
            for name, value in (("missing", None), ("stale", "2000-01-01"), ("malformed", "today")):
                with self.subTest(verdict=verdict, name=name):
                    candidate = deepcopy(base)
                    if value is None:
                        candidate[verdict].pop("date")
                    else:
                        candidate[verdict]["date"] = value
                    with self.assertRaises(ValueError):
                        refresh_taggable_evidence(candidate, source, MERGE, post_merge())

    def test_refresh_taggable_evidence_rejects_invalid_post_merge_commands(self) -> None:
        source = verify_owner_comment(owner_comment(), HEAD, PUBLICATION_DATE, TIMESTAMP)
        base = build_external_evidence(source, HEAD, verdicts(), pr_state())
        cases = (
            ("missing", lambda p: p["commands"].pop()),
            ("duplicate", lambda p: p["commands"].append(deepcopy(p["commands"][0]))),
            ("extra", lambda p: p["commands"].append({"name": "extra", "exit_code": 0, "result": "passed"})),
            ("failed", lambda p: p["commands"][0].__setitem__("exit_code", 1)),
            ("empty_result", lambda p: p["commands"][0].__setitem__("result", "")),
        )
        for name, mutate in cases:
            with self.subTest(name=name):
                results = post_merge()
                mutate(results)
                with self.assertRaises(ValueError):
                    refresh_taggable_evidence(base, source, MERGE, results)

    def test_cli_build_and_taggable_refresh_modes_write_external_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            owner_path = directory / "owner.json"
            write_json(owner_path, owner_comment())
            for name, number in (("technical", 2), ("editorial", 3), ("rendering", 4), ("governance", 5)):
                write_json(directory / f"{name}.json", verdict_comment(name, number))
            pr_path = directory / "pr.json"
            write_json(pr_path, pr_state())
            closure_path = directory / "closure.json"
            build_args = [
                "--comment-json", str(owner_path),
                "--technical-comment-json", str(directory / "technical.json"),
                "--editorial-comment-json", str(directory / "editorial.json"),
                "--rendering-comment-json", str(directory / "rendering.json"),
                "--governance-comment-json", str(directory / "governance.json"),
                "--pr-state-json", str(pr_path),
                "--expected-head", HEAD,
                "--publication-date", PUBLICATION_DATE,
                "--verified-at", TIMESTAMP,
                "--output", str(closure_path),
            ]
            self.assertEqual(main(build_args), 0)
            closure = json.loads(closure_path.read_text(encoding="utf-8"))
            self.assertEqual(closure["closure_head"], HEAD)
            post_merge_path = directory / "post-merge.json"
            write_json(post_merge_path, post_merge())
            taggable_path = directory / "taggable.json"
            refresh_args = [
                "--comment-json", str(owner_path),
                "--base-evidence", str(closure_path),
                "--merge-head", MERGE,
                "--post-merge-json", str(post_merge_path),
                "--publication-date", PUBLICATION_DATE,
                "--verified-at", TIMESTAMP,
                "--output", str(taggable_path),
            ]
            self.assertEqual(main(refresh_args), 0)
            self.assertEqual(json.loads(taggable_path.read_text(encoding="utf-8"))["merge_head"], MERGE)

    def test_cli_refuses_repository_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            owner_path = directory / "owner.json"
            write_json(owner_path, owner_comment())
            for name, number in (("technical", 2), ("editorial", 3), ("rendering", 4), ("governance", 5)):
                comment = verdict_comment(name, number)
                write_json(directory / f"{name}.json", comment)
            pr_path = directory / "pr.json"
            write_json(pr_path, pr_state())
            arguments = [
                "--comment-json", str(owner_path),
                "--technical-comment-json", str(directory / "technical.json"),
                "--editorial-comment-json", str(directory / "editorial.json"),
                "--rendering-comment-json", str(directory / "rendering.json"),
                "--governance-comment-json", str(directory / "governance.json"),
                "--pr-state-json", str(pr_path),
                "--expected-head", HEAD,
                "--publication-date", PUBLICATION_DATE,
                "--verified-at", TIMESTAMP,
                "--output", str(Path(__file__).resolve().parents[1] / "evidence.json"),
            ]
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(main(arguments), 1)
            self.assertIn("external evidence output shall be outside the repository", stderr.getvalue())

    def test_cli_build_rejects_incomplete_verdict_body(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            owner_path = directory / "owner.json"
            write_json(owner_path, owner_comment())
            for name, number in (("technical", 2), ("editorial", 3), ("rendering", 4), ("governance", 5)):
                comment = verdict_comment(name, number)
                if name == "technical":
                    payload = json.loads(comment["body"].split("\n", 1)[1].rsplit("\n```", 1)[0])
                    payload.pop("method")
                    comment["body"] = "```json\n" + json.dumps(payload) + "\n```"
                write_json(directory / f"{name}.json", comment)
            pr_path = directory / "pr.json"
            write_json(pr_path, pr_state())
            arguments = [
                "--comment-json", str(owner_path),
                "--technical-comment-json", str(directory / "technical.json"),
                "--editorial-comment-json", str(directory / "editorial.json"),
                "--rendering-comment-json", str(directory / "rendering.json"),
                "--governance-comment-json", str(directory / "governance.json"),
                "--pr-state-json", str(pr_path),
                "--expected-head", HEAD,
                "--publication-date", PUBLICATION_DATE,
                "--verified-at", TIMESTAMP,
                "--output", str(directory / "external-evidence.json"),
            ]
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(main(arguments), 1)
            self.assertIn("technical verdict method shall be named", stderr.getvalue())
