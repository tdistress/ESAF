#!/usr/bin/env python3
"""Build offline, versioned owner-risk evidence for the ESAF release gate."""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from tools.release_gates import (
    CLAIMS_NOT_MADE,
    EXPECTED_MAPPING_SETS,
    MAPPING_DECISION_SCHEMA,
    OWNER_REPOSITORY,
    POST_MERGE_COMMANDS,
    REPOSITORY_SCOPE,
    SHA_RE,
    _rfc3339,
)


JSON_FENCE_RE = re.compile(r"(?ms)^```json[ \t]*\r?\n(.*?)^```[ \t]*$")
OWNER_API_URL = "https://api.github.com/repos/tdistress/ESAF"


def _numeric(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_owner_decision(body: str) -> dict[str, object]:
    """Extract exactly one JSON object from a GitHub comment body."""
    _require(isinstance(body, str), "comment body is required")
    blocks = JSON_FENCE_RE.findall(body)
    _require(len(blocks) == 1, "comment body shall contain exactly one fenced JSON object")
    try:
        value = json.loads(blocks[0])
    except json.JSONDecodeError as exc:
        raise ValueError("comment JSON block shall be valid JSON") from exc
    _require(isinstance(value, dict), "comment JSON block shall be an object")
    return value


def _validate_decision(value: dict[str, object], expected_head: str) -> None:
    _require(value.get("decision_type") == "owner_risk_acceptance", "owner decision type shall be owner_risk_acceptance")
    _require(value.get("sha") == expected_head and bool(SHA_RE.fullmatch(expected_head)), "owner decision SHA shall equal expected head")
    mapping_ids = value.get("mapping_set_ids")
    _require(
        isinstance(mapping_ids, list)
        and len(mapping_ids) == len(EXPECTED_MAPPING_SETS)
        and all(isinstance(item, str) for item in mapping_ids)
        and len(set(mapping_ids)) == len(mapping_ids)
        and set(mapping_ids) == set(EXPECTED_MAPPING_SETS),
        "owner decision mapping-set IDs shall equal the expected set",
    )
    _require(value.get("disposition") == "accepted_for_working_draft", "owner decision disposition shall be accepted_for_working_draft")
    _require(value.get("qualified_review_status") == "deferred", "owner decision qualified review status shall be deferred")
    _require(value.get("scope") == REPOSITORY_SCOPE, "owner decision scope shall equal complete_git_tracked_repository")
    _require(value.get("lifecycle") == "draft", "owner decision lifecycle shall equal draft")
    claims = value.get("claims_not_made")
    _require(
        isinstance(claims, list)
        and len(claims) == len(CLAIMS_NOT_MADE)
        and all(isinstance(item, str) for item in claims)
        and len(set(claims)) == len(claims)
        and set(claims) == CLAIMS_NOT_MADE,
        "owner decision prohibited claims shall equal the required set",
    )


def _timestamp_for_date(value: object, publication_date: str, name: str) -> str:
    timestamp = _rfc3339(value)
    _require(timestamp is not None, f"{name} shall be RFC 3339")
    _require(
        timestamp.astimezone(timezone.utc).date().isoformat() == publication_date,
        f"{name} UTC date shall equal publication date",
    )
    return str(value)


def verify_owner_comment(
    comment: dict[str, object], expected_head: str, publication_date: str, verified_at: str,
) -> dict[str, object]:
    """Validate fetched GitHub data and derive the source record from it."""
    _require(isinstance(comment, dict), "fetched owner comment shall be an object")
    _require(bool(SHA_RE.fullmatch(expected_head)), "expected head shall be a 40-character SHA")
    _require(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", publication_date)), "publication date shall be ISO formatted")
    _timestamp_for_date(verified_at, publication_date, "verification timestamp")
    _require(comment.get("repository_url") == OWNER_API_URL, "owner comment repository URL shall equal tdistress/ESAF")
    body = comment.get("body")
    _require(isinstance(body, str) and body.strip(), "owner comment body is required")
    decision = parse_owner_decision(body)
    _validate_decision(decision, expected_head)
    comment_url = comment.get("html_url")
    _require(isinstance(comment_url, str) and comment_url.startswith("https://github.com/tdistress/ESAF/"), "owner comment URL shall use GitHub HTTPS")
    _require(_numeric(comment.get("id")), "owner comment ID shall be numeric")
    user = comment.get("user")
    _require(isinstance(user, dict), "owner comment author is required")
    _require(user.get("login") == "tdistress", "owner comment login shall equal tdistress")
    _require(_numeric(user.get("id")), "owner comment user ID shall be numeric")
    _require(comment.get("author_association") == "OWNER", "owner comment association shall be OWNER")
    created_at = _timestamp_for_date(comment.get("created_at"), publication_date, "owner comment creation timestamp")
    updated_at = _timestamp_for_date(comment.get("updated_at"), publication_date, "owner comment update timestamp")
    return {
        "repository": OWNER_REPOSITORY,
        "comment_url": comment_url,
        "comment_id": comment["id"],
        "author_login": user["login"],
        "author_user_id": user["id"],
        "author_association": "OWNER",
        "created_at": created_at,
        "updated_at": updated_at,
        "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "source_verified_at": verified_at,
    }


def _source_is_valid(source: dict[str, object], closure_head: str) -> None:
    _require(isinstance(source, dict), "owner source is required")
    _require(source.get("repository") == OWNER_REPOSITORY, "owner source repository shall equal tdistress/ESAF")
    _require(isinstance(source.get("comment_url"), str) and str(source["comment_url"]).startswith("https://"), "owner source comment URL shall use HTTPS")
    _require(_numeric(source.get("comment_id")), "owner source comment ID shall be numeric")
    _require(source.get("author_login") == "tdistress", "owner source login shall equal tdistress")
    _require(_numeric(source.get("author_user_id")), "owner source user ID shall be numeric")
    _require(source.get("author_association") == "OWNER", "owner source association shall be OWNER")
    for field in ("created_at", "updated_at", "source_verified_at"):
        _require(_rfc3339(source.get(field)) is not None, f"owner source {field} shall be RFC 3339")
    _require(isinstance(source.get("body_sha256"), str) and bool(re.fullmatch(r"[0-9a-f]{64}", str(source["body_sha256"]))), "owner source body digest shall be a SHA-256")
    _require(bool(SHA_RE.fullmatch(closure_head)), "closure head shall be a 40-character SHA")


def _owner_decisions(source: dict[str, object], closure_head: str) -> list[dict[str, object]]:
    limitations = {"lifecycle": "draft", "claims_not_made": sorted(CLAIMS_NOT_MADE)}
    return [
        {
            "mapping_set_id": mapping_set_id,
            "decision_type": "owner_risk_acceptance",
            "sha": closure_head,
            "decided_at": source["created_at"],
            "url": source["comment_url"],
            "owner_login": source["author_login"],
            "owner_user_id": source["author_user_id"],
            "role": "repository_owner",
            "author_association": "OWNER",
            "disposition": "accepted_for_working_draft",
            "qualified_review_status": "deferred",
            "limitations": deepcopy(limitations),
            "source": deepcopy(source),
        }
        for mapping_set_id in EXPECTED_MAPPING_SETS
    ]


def _owner_scope(source: dict[str, object], closure_head: str) -> dict[str, object]:
    return {
        "approval_basis": "owner_risk_acceptance",
        "sha": closure_head,
        "owner_login": source["author_login"],
        "owner_user_id": source["author_user_id"],
        "role": "repository_owner",
        "author_association": "OWNER",
        "decided_at": source["created_at"],
        "scope": REPOSITORY_SCOPE,
        "limitations": {"lifecycle": "draft", "claims_not_made": sorted(CLAIMS_NOT_MADE)},
        "source": deepcopy(source),
    }


def _validate_verdicts(verdict_comments: dict[str, dict[str, object]], closure_head: str) -> None:
    _require(isinstance(verdict_comments, dict), "verdict comments are required")
    for name in ("technical", "editorial", "rendering", "governance"):
        value = verdict_comments.get(name)
        _require(isinstance(value, dict), f"{name} verdict is required")
        _require(value.get("sha") == closure_head, f"{name} verdict shall be bound to closure head")
        _require(value.get("disposition") == "approved", f"{name} verdict disposition shall be approved")
        _require(isinstance(value.get("url"), str) and value["url"].startswith("https://"), f"{name} verdict URL shall use HTTPS")
        _require(isinstance(value.get("reviewer"), str) and value["reviewer"].strip(), f"{name} verdict reviewer shall be named")
        _require(isinstance(value.get("method"), str) and value["method"].strip(), f"{name} verdict method shall be named")
        _require(isinstance(value.get("result"), str) and value["result"].strip(), f"{name} verdict result shall be nonempty")
        if name == "governance":
            _require(isinstance(value.get("approver"), str) and value["approver"].strip(), "governance approver shall be named")
            _require(value.get("authority") == "Steering Committee", "governance authority shall be Steering Committee")
        else:
            _require(value.get("critical") == 0 and value.get("important") == 0, f"{name} verdict findings shall be zero")


def _checks_and_merge_state(pr_state: dict[str, object], closure_head: str) -> tuple[dict[str, object], dict[str, object]]:
    _require(isinstance(pr_state, dict), "PR state is required")
    _require(pr_state.get("headRefOid") == closure_head, "PR state head shall equal closure head")
    _require(pr_state.get("mergeable") == "MERGEABLE", "PR state shall be mergeable")
    _require(pr_state.get("mergeStateStatus") == "CLEAN", "PR state shall be clean")
    rollup = pr_state.get("statusCheckRollup")
    _require(isinstance(rollup, list) and len(rollup) == 1 and isinstance(rollup[0], dict), "PR state shall contain the required check")
    check = rollup[0]
    _require(check.get("name") == "Validate ESAF sources", "PR check shall be Validate ESAF sources")
    _require(check.get("conclusion") == "SUCCESS", "PR check conclusion shall be SUCCESS")
    url = check.get("detailsUrl")
    _require(isinstance(url, str) and url.startswith("https://"), "PR check URL shall use HTTPS")
    return (
        {"expected": ["Validate ESAF sources"], "observed": [{"name": "Validate ESAF sources", "sha": closure_head, "conclusion": "success", "url": url}]},
        {"sha": closure_head, "mergeable": True, "state": "clean"},
    )


def build_external_evidence(
    owner_source: dict[str, object], closure_head: str, verdict_comments: dict[str, dict[str, object]], pr_state: dict[str, object],
) -> dict[str, object]:
    _source_is_valid(owner_source, closure_head)
    _validate_verdicts(verdict_comments, closure_head)
    checks, merge_state = _checks_and_merge_state(pr_state, closure_head)
    return {
        "closure_head": closure_head,
        "mapping_decision_schema": MAPPING_DECISION_SCHEMA,
        "mapping_decision_basis": "owner_risk_acceptance",
        "mapping_decisions": _owner_decisions(owner_source, closure_head),
        "scope": _owner_scope(owner_source, closure_head),
        "technical": deepcopy(verdict_comments["technical"]),
        "editorial": deepcopy(verdict_comments["editorial"]),
        "rendering": deepcopy(verdict_comments["rendering"]),
        "governance": deepcopy(verdict_comments["governance"]),
        "github_checks": checks,
        "merge_state": merge_state,
    }


def _validate_owner_decision_base(value: object, closure_head: str) -> dict[str, object]:
    _require(isinstance(value, dict), "base mapping decision shall be an object")
    _require(value.get("decision_type") == "owner_risk_acceptance", "base mapping decision shall use owner_risk_acceptance")
    _require(value.get("sha") == closure_head, "base mapping decision shall be bound to closure head")
    _require(value.get("role") == "repository_owner", "base mapping decision role shall be repository_owner")
    _require(value.get("author_association") == "OWNER", "base mapping decision association shall be OWNER")
    _require(value.get("disposition") == "accepted_for_working_draft", "base mapping decision disposition shall be accepted_for_working_draft")
    _require(value.get("qualified_review_status") == "deferred", "base mapping decision review status shall be deferred")
    source = value.get("source")
    _require(isinstance(source, dict), "base mapping decision source is required")
    _source_is_valid(source, closure_head)
    _require(value.get("url") == source.get("comment_url"), "base mapping decision URL shall match source")
    _require(value.get("owner_login") == source.get("author_login") and value.get("owner_user_id") == source.get("author_user_id"), "base mapping decision identity shall match source")
    _require(value.get("decided_at") == source.get("created_at"), "base mapping decision timestamp shall match source")
    return source


def _validate_closure_base(base_evidence: dict[str, object], closure_head: str) -> None:
    _require(base_evidence.get("mapping_decision_schema") == MAPPING_DECISION_SCHEMA, "base evidence shall use the v1 mapping decision schema")
    _require("merge_head" not in base_evidence and "post_merge" not in base_evidence, "base evidence shall not contain merge evidence")
    decisions = base_evidence.get("mapping_decisions")
    _require(isinstance(decisions, list) and len(decisions) == len(EXPECTED_MAPPING_SETS), "base evidence shall contain exactly three mapping decisions")
    decision_ids = [item.get("mapping_set_id") for item in decisions if isinstance(item, dict)]
    _require(
        len(decision_ids) == len(EXPECTED_MAPPING_SETS)
        and all(isinstance(identifier, str) for identifier in decision_ids)
        and sorted(decision_ids) == sorted(EXPECTED_MAPPING_SETS),
        "base mapping decisions shall contain each expected mapping set exactly once",
    )
    sources = [_validate_owner_decision_base(item, closure_head) for item in decisions]
    _require(all(source == sources[0] for source in sources[1:]), "base mapping decisions shall use the same source")
    scope = base_evidence.get("scope")
    _require(isinstance(scope, dict), "base owner scope is required")
    _require(scope.get("approval_basis") == "owner_risk_acceptance", "base owner scope shall use owner_risk_acceptance")
    _require(scope.get("sha") == closure_head, "base owner scope shall be bound to closure head")
    _require(scope.get("scope") == REPOSITORY_SCOPE, "base owner scope shall be complete")
    _require(scope.get("role") == "repository_owner" and scope.get("author_association") == "OWNER", "base owner scope identity is invalid")
    scope_source = scope.get("source")
    _require(isinstance(scope_source, dict), "base owner scope source is required")
    _source_is_valid(scope_source, closure_head)
    _require(scope_source == sources[0], "base owner scope source shall match mapping decisions")
    _require(scope.get("owner_login") == scope_source.get("author_login") and scope.get("owner_user_id") == scope_source.get("author_user_id"), "base owner scope identity shall match source")
    _require(scope.get("decided_at") == scope_source.get("created_at"), "base owner scope timestamp shall match source")
    verdicts = {name: base_evidence.get(name) for name in ("technical", "editorial", "rendering", "governance")}
    _validate_verdicts(verdicts, closure_head)
    checks = base_evidence.get("github_checks")
    _require(isinstance(checks, dict), "base GitHub checks are required")
    observed = checks.get("observed")
    _require(checks.get("expected") == ["Validate ESAF sources"], "base GitHub expected checks are invalid")
    _require(isinstance(observed, list) and len(observed) == 1 and isinstance(observed[0], dict), "base GitHub observed checks are invalid")
    check = observed[0]
    _require(check.get("name") == "Validate ESAF sources" and check.get("sha") == closure_head and check.get("conclusion") == "success", "base GitHub check shall be a successful closure-head check")
    _require(isinstance(check.get("url"), str) and check["url"].startswith("https://"), "base GitHub check URL shall use HTTPS")
    merge_state = base_evidence.get("merge_state")
    _require(isinstance(merge_state, dict), "base merge state is required")
    _require(merge_state.get("sha") == closure_head and merge_state.get("mergeable") is True and merge_state.get("state") == "clean", "base merge state shall be a clean closure-head state")


def _validate_post_merge(post_merge: object, merge_head: str) -> None:
    _require(isinstance(post_merge, dict) and post_merge.get("sha") == merge_head, "post-merge evidence shall be bound to merge head")
    commands = post_merge.get("commands")
    _require(isinstance(commands, list) and len(commands) == len(POST_MERGE_COMMANDS) and all(isinstance(command, dict) for command in commands), "post-merge commands shall contain each required command exactly once")
    names = [command.get("name") for command in commands]
    _require(all(isinstance(name, str) for name in names) and sorted(names) == sorted(POST_MERGE_COMMANDS), "post-merge commands shall contain each required command exactly once")
    for command in commands:
        _require(command.get("exit_code") == 0, f"{command['name']} command failed")
        _require(isinstance(command.get("result"), str) and command["result"].strip(), f"{command['name']} command result shall be nonempty")


def refresh_taggable_evidence(
    base_evidence: dict[str, object], owner_source: dict[str, object], merge_head: str, post_merge: dict[str, object],
) -> dict[str, object]:
    _require(isinstance(base_evidence, dict), "base evidence is required")
    closure_head = base_evidence.get("closure_head")
    _require(isinstance(closure_head, str) and bool(SHA_RE.fullmatch(closure_head)), "base evidence closure head shall be a 40-character SHA")
    _require(base_evidence.get("mapping_decision_basis") == "owner_risk_acceptance", "base evidence shall use owner_risk_acceptance")
    _require(isinstance(merge_head, str) and bool(SHA_RE.fullmatch(merge_head)), "merge head shall be a 40-character SHA")
    _validate_closure_base(base_evidence, closure_head)
    _source_is_valid(owner_source, closure_head)
    _validate_post_merge(post_merge, merge_head)
    evidence = deepcopy(base_evidence)
    evidence["mapping_decisions"] = _owner_decisions(owner_source, closure_head)
    evidence["scope"] = _owner_scope(owner_source, closure_head)
    evidence["merge_head"] = merge_head
    evidence["post_merge"] = deepcopy(post_merge)
    return evidence


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"{path} shall contain a JSON object")
    return value


def _verdict_from_comment(comment: dict[str, object], name: str, expected_head: str, publication_date: str) -> dict[str, object]:
    body = comment.get("body")
    _require(isinstance(body, str), f"{name} comment body is required")
    value = parse_owner_decision(body)
    _require(value.get("sha") == expected_head, f"{name} verdict SHA shall equal expected head")
    _require(value.get("date") == publication_date, f"{name} verdict date shall equal publication date")
    _require(value.get("disposition") == "approved", f"{name} verdict disposition shall be approved")
    url = comment.get("html_url")
    _require(isinstance(url, str) and url.startswith("https://"), f"{name} verdict comment URL shall use HTTPS")
    value["url"] = url
    return value


def _write_output(path: Path, evidence: dict[str, object]) -> None:
    root = Path(__file__).resolve().parents[1]
    resolved = path.resolve()
    _require(not resolved.is_relative_to(root), "external evidence output shall be outside the repository")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build offline owner-risk evidence.")
    parser.add_argument("--comment-json", type=Path, required=True)
    parser.add_argument("--technical-comment-json", type=Path)
    parser.add_argument("--editorial-comment-json", type=Path)
    parser.add_argument("--rendering-comment-json", type=Path)
    parser.add_argument("--governance-comment-json", type=Path)
    parser.add_argument("--pr-state-json", type=Path)
    parser.add_argument("--expected-head")
    parser.add_argument("--publication-date")
    parser.add_argument("--verified-at")
    parser.add_argument("--base-evidence", type=Path)
    parser.add_argument("--merge-head")
    parser.add_argument("--post-merge-json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.base_evidence:
            _require(args.merge_head is not None and args.post_merge_json is not None, "taggable refresh requires --merge-head and --post-merge-json")
            base = _load_json(args.base_evidence)
            source = verify_owner_comment(_load_json(args.comment_json), str(base.get("closure_head")), str(args.publication_date), str(args.verified_at))
            evidence = refresh_taggable_evidence(base, source, args.merge_head, _load_json(args.post_merge_json))
        else:
            inputs = (args.technical_comment_json, args.editorial_comment_json, args.rendering_comment_json, args.governance_comment_json, args.pr_state_json, args.expected_head, args.publication_date, args.verified_at)
            _require(all(inputs), "build mode requires verdict comments, PR state, expected head, publication date, and verification timestamp")
            source = verify_owner_comment(_load_json(args.comment_json), args.expected_head, args.publication_date, args.verified_at)
            verdicts = {
                name: _verdict_from_comment(_load_json(getattr(args, f"{name}_comment_json")), name, args.expected_head, args.publication_date)
                for name in ("technical", "editorial", "rendering", "governance")
            }
            evidence = build_external_evidence(source, args.expected_head, verdicts, _load_json(args.pr_state_json))
        _write_output(args.output, evidence)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
