from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import unittest

from tools.owner_risk_evidence import (
    build_external_evidence,
    parse_owner_decision,
    refresh_taggable_evidence,
    verify_owner_comment,
)
from tools.release_gates import CLAIMS_NOT_MADE, EXPECTED_MAPPING_SETS


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
        post_merge = {"sha": MERGE, "commands": [{"name": "full_suite", "exit_code": 0, "result": "passed"}]}
        evidence = refresh_taggable_evidence(base, refreshed, MERGE, post_merge)
        self.assertEqual(evidence["closure_head"], HEAD)
        self.assertEqual(evidence["technical"], base["technical"])
        self.assertEqual(evidence["mapping_decisions"][0]["source"], refreshed)
        self.assertEqual(evidence["scope"]["source"], refreshed)
        self.assertEqual(evidence["merge_head"], MERGE)
        self.assertEqual(evidence["post_merge"], post_merge)
