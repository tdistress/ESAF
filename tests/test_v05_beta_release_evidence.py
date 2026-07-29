from __future__ import annotations

from copy import deepcopy
from contextlib import redirect_stderr
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tests.test_v05_beta_release_gates import (
    CLOSURE_BASE,
    CLOSURE_SHA,
    CLOSURE_TREE,
    COMMAND_IDS,
    MERGE_SHA,
    MAPPING_SETS,
    CLAIMS_NOT_MADE,
    REENTRY_TRIGGERS,
    command_results,
    missing_roles,
    record_fixture,
)
from tools.v05_beta_release_evidence import (
    ApiClient,
    ApiPageSet,
    ApiResponse,
    DetachedValidationRunner,
    GhApiClient,
    LocalValidationRunner,
    ValidationRunner,
    build_parser,
    collect_closure_evidence,
    main,
    parse_fenced_json,
    refresh_taggable_evidence,
    source_record,
)
from tools.v05_beta_release_gates import validate_external_evidence


ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 7, 27, 12, 10, tzinfo=timezone.utc)
COMMIT_TIME = "2026-07-27T11:00:00Z"
PUBLICATION_DATE = "2026-07-27"
PR_NUMBER = 73
PUBLICATION_ISSUE_NUMBER = 59
OWNER_ID = 20
TECHNICAL_ID = 11
EDITORIAL_ID = 12
TERMINOLOGY_ID = 13
RENDERING_ID = 14
PROFILE_SCOPE_ID = 15
GOVERNANCE_ID = 16
SECURITY_OVERCLAIMING_ID = 17
WHOLE_RANGE_ID = 18
POST_MERGE_RENDERING_ID = 19
COMMIT_RESOURCE = f"repos/tdistress/ESAF/commits/{CLOSURE_SHA}"
MERGE_COMMIT_RESOURCE = f"repos/tdistress/ESAF/commits/{MERGE_SHA}"
PR_RESOURCE = f"repos/tdistress/ESAF/pulls/{PR_NUMBER}"
CHECKS_RESOURCE = f"repos/tdistress/ESAF/commits/{CLOSURE_SHA}/check-runs"
CHECKS_PAGE_ONE = f"{CHECKS_RESOURCE}?per_page=100&page=1"
ACTIONS_RUN_RESOURCE = "repos/tdistress/ESAF/actions/runs/9001"
ISSUE_55_RESOURCE = "repos/tdistress/ESAF/issues/55"
USER_RESOURCE = "user"
TAG_RESOURCE = "repos/tdistress/ESAF/git/ref/tags/v0.5-beta"
CLOSURE_PARENT = "a" * 40
HEAD_REF = "agent/v05-beta-publication-closure"


def comment_resource(comment_id: int) -> str:
    return f"repos/tdistress/ESAF/issues/comments/{comment_id}"


OWNER_RESOURCE = comment_resource(OWNER_ID)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def fenced(value: dict[str, object]) -> str:
    return "Decision evidence follows.\n\n```json\n" + json.dumps(
        value, indent=2, sort_keys=True
    ) + "\n```\n"


def owner_payload() -> dict[str, object]:
    return {
        "schema": "esaf-v05-owner-decision-v1",
        "release": "0.5-beta",
        "sha": CLOSURE_SHA,
        "mapping_decision_basis": "owner_risk_acceptance",
        "decision_type": "owner_risk_acceptance",
        "disposition": "accepted_for_working_draft",
        "qualified_review_status": "deferred",
        "mapping_set_ids": list(MAPPING_SETS),
        "missing_qualified_roles": missing_roles(),
        "accountable_owner": "tdistress",
        "scope_approval": {
            "scope": "complete_git_tracked_repository",
            "milestone": "v0.5-beta",
            "disposition": "approved_for_working_draft_closure",
        },
        "issue_55_status": "remains_open",
        "lifecycle": "draft",
        "claims_not_made": sorted(CLAIMS_NOT_MADE),
        "reentry_triggers": sorted(REENTRY_TRIGGERS),
    }


def verdict_payload(
    kind: str, reviewer: str | None = None
) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema": "esaf-v05-release-verdict-v1",
        "release": "0.5-beta",
        "sha": CLOSURE_SHA,
        "kind": kind,
        "reviewer": reviewer or f"{kind}-reviewer",
        "role": f"{kind.replace('_', ' ')} reviewer",
        "date": PUBLICATION_DATE,
        "disposition": "approved",
        "critical": 0,
        "important": 0,
    }
    if kind == "rendering":
        payload.update(
            {
                "rendered_blocks": 23,
                "renderer": "@mermaid-js/mermaid-cli@11.16.0",
                "visual_review": "approved",
            }
        )
    return payload


def governance_payload() -> dict[str, object]:
    return {
        "schema": "esaf-v05-governance-verdict-v1",
        "release": "0.5-beta",
        "sha": CLOSURE_SHA,
        "kind": "governance",
        "approver": "governance-approver",
        "authority": "Steering Committee",
        "authority_attestation": True,
        "authority_verification": "manual",
        "authority_basis": "GOVERNANCE.md#21-steering-committee",
        "date": PUBLICATION_DATE,
        "disposition": "approved_for_working_draft_publication",
        "critical": 0,
        "important": 0,
    }


def post_merge_rendering_payload() -> dict[str, object]:
    return {
        "schema": "esaf-v05-post-merge-rendering-verdict-v1",
        "release": "0.5-beta",
        "sha": MERGE_SHA,
        "tree": CLOSURE_TREE,
        "kind": "post_merge_rendering",
        "reviewer": "post-merge-rendering-reviewer",
        "role": "post-merge rendering reviewer",
        "date": PUBLICATION_DATE,
        "disposition": "approved",
        "critical": 0,
        "important": 0,
        "rendered_blocks": 23,
        "renderer": "@mermaid-js/mermaid-cli@11.16.0",
        "visual_review": "approved",
    }


def api_response(
    resource: str,
    payload: dict[str, object],
    *,
    retrieved_at: datetime = NOW,
    headers: tuple[tuple[str, str], ...] = (("content-type", "application/json"),),
    raw_body: bytes | None = None,
    status: int = 200,
) -> ApiResponse:
    return ApiResponse(
        requested_resource=resource,
        observed_request_uri=f"/{resource}",
        redirect_count=0,
        status=status,
        headers=headers,
        raw_body=raw_body if raw_body is not None else canonical_bytes(payload),
        retrieved_at=retrieved_at,
    )


def comment_payload(
    comment_id: int,
    author: str,
    body: dict[str, object],
    association: str = "COLLABORATOR",
    *,
    container_type: str = "pull",
    container_number: int = PR_NUMBER,
) -> dict[str, object]:
    resource = comment_resource(comment_id)
    html_container = (
        "pull" if container_type == "pull" else "issues"
    )
    return {
        "url": f"https://api.github.com/{resource}",
        "html_url": (
            f"https://github.com/tdistress/ESAF/{html_container}/"
            f"{container_number}"
            f"#issuecomment-{comment_id}"
        ),
        "issue_url": (
            "https://api.github.com/repos/tdistress/ESAF/issues/"
            f"{container_number}"
        ),
        "id": comment_id,
        "user": {
            "login": author,
            "id": 1000 + comment_id,
            "type": "User",
            "site_admin": False,
        },
        "created_at": "2026-07-27T12:00:00Z",
        "updated_at": "2026-07-27T12:00:00Z",
        "author_association": association,
        "body": fenced(body),
    }


class FakeClient(ApiClient):
    def __init__(
        self,
        login: str,
        responses: dict[str, ApiResponse],
        page_sets: dict[str, ApiPageSet],
    ) -> None:
        self.login = login
        self.responses = responses
        self.page_sets = page_sets

    def auth_login(self) -> str:
        return self.login

    def get(self, resource: str) -> ApiResponse:
        return self.responses[resource]

    def get_pages(self, resource: str) -> ApiPageSet:
        return self.page_sets[resource]


class LiveTimestampFakeClient(FakeClient):
    def get(self, resource: str) -> ApiResponse:
        return replace(
            super().get(resource),
            retrieved_at=datetime.now(timezone.utc),
        )

    def get_pages(self, resource: str) -> ApiPageSet:
        page_set = super().get_pages(resource)
        return replace(
            page_set,
            pages=tuple(
                replace(
                    page,
                    retrieved_at=datetime.now(timezone.utc),
                )
                for page in page_set.pages
            ),
        )


class FakeValidationRunner(ValidationRunner):
    def __init__(self) -> None:
        self.calls: list[tuple[Path, str, str]] = []
        self.results = [
            {
                "name": name,
                "sha": CLOSURE_SHA,
                "exit_code": 0,
                "result": f"executed:{name}",
            }
            for name in COMMAND_IDS
            if name != "mermaid_rendering"
        ]

    def run(
        self,
        root: Path,
        expected_head: str,
        baseline_head: str,
    ) -> list[dict[str, object]]:
        self.calls.append((root, expected_head, baseline_head))
        results = deepcopy(self.results)
        for result in results:
            if result.get("sha") == CLOSURE_SHA:
                result["sha"] = expected_head
        return results


def valid_fake_client() -> FakeClient:
    responses = {
        USER_RESOURCE: api_response(
            USER_RESOURCE,
            {
                "login": "tdistress",
                "id": 1,
                "html_url": "https://github.com/tdistress",
                "type": "User",
            },
        ),
        COMMIT_RESOURCE: api_response(
            COMMIT_RESOURCE,
            {
                "sha": CLOSURE_SHA,
                "html_url": (
                    "https://github.com/tdistress/ESAF/commit/"
                    f"{CLOSURE_SHA}"
                ),
                "commit": {
                    "author": {"date": COMMIT_TIME},
                    "committer": {"date": COMMIT_TIME},
                    "tree": {"sha": CLOSURE_TREE},
                },
                "parents": [
                    {
                        "sha": CLOSURE_PARENT,
                        "url": (
                            "https://api.github.com/repos/tdistress/ESAF/"
                            f"commits/{CLOSURE_PARENT}"
                        ),
                    }
                ],
            },
        ),
        MERGE_COMMIT_RESOURCE: api_response(
            MERGE_COMMIT_RESOURCE,
            {
                "sha": MERGE_SHA,
                "html_url": (
                    "https://github.com/tdistress/ESAF/commit/"
                    f"{MERGE_SHA}"
                ),
                "commit": {
                    "author": {"date": "2026-07-27T12:06:00Z"},
                    "committer": {"date": "2026-07-27T12:06:00Z"},
                    "tree": {"sha": CLOSURE_TREE},
                },
            },
        ),
        PR_RESOURCE: api_response(
            PR_RESOURCE,
            {
                "url": f"https://api.github.com/{PR_RESOURCE}",
                "html_url": f"https://github.com/tdistress/ESAF/pull/{PR_NUMBER}",
                "number": PR_NUMBER,
                "state": "open",
                "head": {
                    "sha": CLOSURE_SHA,
                    "ref": HEAD_REF,
                    "label": f"tdistress:{HEAD_REF}",
                    "repo": {
                        "full_name": "tdistress/ESAF",
                        "url": "https://api.github.com/repos/tdistress/ESAF",
                        "html_url": "https://github.com/tdistress/ESAF",
                        "owner": {"login": "tdistress"},
                    },
                },
                "base": {
                    "sha": CLOSURE_BASE,
                    "ref": "main",
                    "label": "tdistress:main",
                    "repo": {
                        "full_name": "tdistress/ESAF",
                        "url": "https://api.github.com/repos/tdistress/ESAF",
                        "html_url": "https://github.com/tdistress/ESAF",
                        "owner": {"login": "tdistress"},
                    },
                },
                "mergeable": True,
                "mergeable_state": "clean",
            },
        ),
        TAG_RESOURCE: api_response(
            TAG_RESOURCE,
            {
                "message": "Not Found",
                "documentation_url": (
                    "https://docs.github.com/rest/git/refs#get-a-reference"
                ),
                "status": "404",
            },
            status=404,
        ),
        ISSUE_55_RESOURCE: api_response(
            ISSUE_55_RESOURCE,
            {
                "url": f"https://api.github.com/{ISSUE_55_RESOURCE}",
                "html_url": "https://github.com/tdistress/ESAF/issues/55",
                "repository_url": (
                    "https://api.github.com/repos/tdistress/ESAF"
                ),
                "number": 55,
                "state": "open",
                "title": "Complete qualified review",
            },
        ),
        ACTIONS_RUN_RESOURCE: api_response(
            ACTIONS_RUN_RESOURCE,
            {
                "id": 9001,
                "name": "Repository validation",
                "path": ".github/workflows/catalog-validation.yml",
                "head_sha": CLOSURE_SHA,
                "status": "completed",
                "conclusion": "success",
                "html_url": (
                    "https://github.com/tdistress/ESAF/actions/runs/9001"
                ),
                "repository": {"full_name": "tdistress/ESAF"},
                "head_repository": {"full_name": "tdistress/ESAF"},
            },
        ),
    }
    comment_specs = (
        (OWNER_ID, "tdistress", owner_payload(), "OWNER"),
        (TECHNICAL_ID, "technical-reviewer", verdict_payload("technical"), "MEMBER"),
        (EDITORIAL_ID, "editorial-reviewer", verdict_payload("editorial"), "MEMBER"),
        (
            TERMINOLOGY_ID,
            "terminology-reviewer",
            verdict_payload("terminology"),
            "MEMBER",
        ),
        (RENDERING_ID, "rendering-reviewer", verdict_payload("rendering"), "MEMBER"),
        (
            PROFILE_SCOPE_ID,
            "profile_scope-reviewer",
            verdict_payload("profile_scope"),
            "MEMBER",
        ),
        (GOVERNANCE_ID, "governance-approver", governance_payload(), "MEMBER"),
        (
            SECURITY_OVERCLAIMING_ID,
            "security_overclaiming-reviewer",
            verdict_payload("security_overclaiming"),
            "MEMBER",
        ),
        (
            WHOLE_RANGE_ID,
            "whole_range-reviewer",
            verdict_payload("whole_range"),
            "MEMBER",
        ),
        (
            POST_MERGE_RENDERING_ID,
            "post-merge-rendering-reviewer",
            post_merge_rendering_payload(),
            "MEMBER",
        ),
    )
    for comment_id, author, body, association in comment_specs:
        resource = comment_resource(comment_id)
        payload = comment_payload(
            comment_id,
            author,
            body,
            association,
            **(
                {
                    "container_type": "issue",
                    "container_number": PUBLICATION_ISSUE_NUMBER,
                }
                if comment_id == POST_MERGE_RENDERING_ID
                else {}
            ),
        )
        if comment_id == POST_MERGE_RENDERING_ID:
            payload["created_at"] = "2026-07-27T12:07:00Z"
            payload["updated_at"] = "2026-07-27T12:07:00Z"
        responses[resource] = api_response(
            resource,
            payload,
        )
    checks_payload = {
        "total_count": 1,
        "check_runs": [
            {
                "id": 9001,
                "name": "Validate ESAF sources",
                "head_sha": CLOSURE_SHA,
                "status": "completed",
                "conclusion": "success",
                "html_url": "https://github.com/tdistress/ESAF/actions/runs/9001",
                "details_url": "https://github.com/tdistress/ESAF/actions/runs/9001",
                "app": {
                    "id": 15368,
                    "slug": "github-actions",
                    "name": "GitHub Actions",
                    "html_url": "https://github.com/apps/github-actions",
                },
            }
        ],
    }
    checks_page = api_response(CHECKS_PAGE_ONE, checks_payload)
    return FakeClient(
        "tdistress",
        responses,
        {
            CHECKS_RESOURCE: ApiPageSet(
                requested_resource=CHECKS_RESOURCE,
                pages=(checks_page,),
                complete=True,
            )
        },
    )


def valid_collection_args() -> dict[str, object]:
    return {
        "root": ROOT,
        "pr_number": PR_NUMBER,
        "expected_head": CLOSURE_SHA,
        "owner_comment_id": OWNER_ID,
        "technical_comment_id": TECHNICAL_ID,
        "editorial_comment_id": EDITORIAL_ID,
        "terminology_comment_id": TERMINOLOGY_ID,
        "rendering_comment_id": RENDERING_ID,
        "profile_scope_comment_id": PROFILE_SCOPE_ID,
        "governance_comment_id": GOVERNANCE_ID,
        "security_overclaiming_comment_id": SECURITY_OVERCLAIMING_ID,
        "whole_range_comment_id": WHOLE_RANGE_ID,
        "now": NOW,
        "validation_runner": FakeValidationRunner(),
    }


def mark_pull_request_merged(
    client: FakeClient, merge_head: str = MERGE_SHA
) -> None:
    response = client.responses[PR_RESOURCE]
    payload = response.json_object()
    payload.update(
        {
            "state": "closed",
            "merged": True,
            "merge_commit_sha": merge_head,
            "mergeable": None,
            "mergeable_state": "unknown",
        }
    )
    client.responses[PR_RESOURCE] = api_response(
        PR_RESOURCE, payload
    )


class QueueRunner:
    def __init__(self, results: list[subprocess.CompletedProcess[bytes]]) -> None:
        self.results = results
        self.calls: list[tuple[list[str], dict[str, str]]] = []

    def __call__(self, args: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        environment = kwargs["env"]
        assert isinstance(environment, dict)
        self.calls.append((args, environment))
        return self.results.pop(0)


class RecordingCommandExecutor:
    def __init__(self) -> None:
        self.calls: list[tuple[list[str], dict[str, object]]] = []

    def __call__(
        self, args: list[str], **kwargs: object
    ) -> subprocess.CompletedProcess[bytes]:
        self.calls.append((args, kwargs))
        if args == ["git", "rev-parse", "HEAD"]:
            stdout = f"{CLOSURE_SHA}\n".encode("ascii")
        elif args == [
            "git", "merge-base", CLOSURE_BASE, CLOSURE_SHA
        ]:
            stdout = f"{CLOSURE_BASE}\n".encode("ascii")
        elif args == ["git", "status", "--porcelain=v1"]:
            stdout = b""
        else:
            stdout = f"executed {' '.join(args)}\n".encode("utf-8")
        return subprocess.CompletedProcess(args, 0, stdout, b"")


def debug_trace(
    resource: str,
    *,
    status: int = 200,
    headers: tuple[tuple[str, str], ...] = (
        ("Content-Type", "application/json; charset=utf-8"),
    ),
) -> bytes:
    header_lines = b"".join(
        f"< {name}: {value}\n".encode("ascii") for name, value in headers
    )
    return (
        b"* Request at 2026-07-27 12:10:00 +0000 UTC\n"
        + f"> GET /{resource} HTTP/1.1\n".encode("ascii")
        + b"> Host: api.github.com\n"
        + f"< HTTP/2.0 {status} Example\n".encode("ascii")
        + header_lines
        + b"* Request took 42ms\n"
    )


def completed(
    resource: str,
    payload: dict[str, object],
    *,
    status: int = 200,
    headers: tuple[tuple[str, str], ...] = (
        ("Content-Type", "application/json; charset=utf-8"),
    ),
    trace: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.CompletedProcess(
        ["gh", "api", resource],
        0 if status == 200 else 1,
        canonical_bytes(payload),
        trace if trace is not None else debug_trace(
            resource, status=status, headers=headers
        ),
    )


class V05GhApiTransportTests(unittest.TestCase):
    def test_gh_client_pins_github_com_and_rejects_host_drift(self) -> None:
        runner = QueueRunner(
            [completed(USER_RESOURCE, {"login": "tdistress"})]
        )
        with patch.dict(os.environ, {"GH_HOST": "enterprise.example"}, clear=False):
            GhApiClient(runner=runner, clock=lambda: NOW).get(USER_RESOURCE)
        self.assertEqual(
            ["gh", "api", "--hostname", "github.com", USER_RESOURCE],
            runner.calls[0][0],
        )
        self.assertNotIn("GH_HOST", runner.calls[0][1])

        drift_trace = debug_trace(USER_RESOURCE).replace(
            b"> Host: api.github.com\n",
            b"> Host: enterprise.example\n",
        )
        with self.assertRaisesRegex(
            ValueError, "GitHub API host changed"
        ):
            GhApiClient(
                runner=QueueRunner(
                    [
                        completed(
                            USER_RESOURCE,
                            {"login": "tdistress"},
                            trace=drift_trace,
                        )
                    ]
                ),
                clock=lambda: NOW,
            ).get(USER_RESOURCE)

    def test_captured_secret_free_debug_fixtures_parse_each_resource_kind(self) -> None:
        resources = (
            "user",
            "repos/tdistress/ESAF/issues/comments/20",
            f"repos/tdistress/ESAF/pulls/{PR_NUMBER}",
            CHECKS_PAGE_ONE,
            f"repos/tdistress/ESAF/commits/{CLOSURE_SHA}",
            "repos/tdistress/ESAF/git/ref/tags/v0.5-beta",
        )
        for resource in resources:
            with self.subTest(resource=resource):
                raw_body = b'{"fixture":"secret-free"}'
                runner = QueueRunner(
                    [
                        subprocess.CompletedProcess(
                            ["gh", "api", resource],
                            0,
                            raw_body,
                            debug_trace(resource),
                        )
                    ]
                )
                response = GhApiClient(runner=runner, clock=lambda: NOW).get(resource)
                self.assertEqual(resource, response.requested_resource)
                self.assertEqual(f"/{resource}", response.observed_request_uri)
                self.assertEqual(raw_body, response.raw_body)
                self.assertEqual(200, response.status)
                self.assertEqual(0, response.redirect_count)
                self.assertEqual("api", runner.calls[0][1]["GH_DEBUG"])
                self.assertNotIn("Authorization", repr(response))

    def test_request_authorization_header_is_never_retained(self) -> None:
        trace = debug_trace(USER_RESOURCE).replace(
            b"> Host: api.github.com\n",
            (
                b"> Host: api.github.com\n"
                b"> Authorization: token fixture-secret\n"
            ),
        )
        response = GhApiClient(
            runner=QueueRunner(
                [
                    completed(
                        USER_RESOURCE,
                        {"login": "tdistress"},
                        trace=trace,
                    )
                ]
            ),
            clock=lambda: NOW,
        ).get(USER_RESOURCE)
        self.assertNotIn("fixture-secret", repr(response))
        self.assertNotIn("authorization", {
            name.casefold() for name, _ in response.headers
        })

    def test_transport_rejects_missing_or_multiple_boundaries(self) -> None:
        resource = USER_RESOURCE
        good = debug_trace(resource)
        traces = {
            "missing request boundary": good.replace(
                b"> GET /user HTTP/1.1\n", b""
            ),
            "multiple transport boundaries": good + good,
        }
        for diagnostic, trace in traces.items():
            with self.subTest(diagnostic=diagnostic):
                client = GhApiClient(
                    runner=QueueRunner(
                        [completed(resource, {"login": "tdistress"}, trace=trace)]
                    ),
                    clock=lambda: NOW,
                )
                with self.assertRaisesRegex(ValueError, diagnostic):
                    client.get(resource)

    def test_transport_rejects_redirect_location_uri_drift_status_and_headers(self) -> None:
        cases = (
            (
                "redirect",
                debug_trace(USER_RESOURCE, status=302),
                302,
                "GitHub API redirects are forbidden",
            ),
            (
                "location",
                debug_trace(
                    USER_RESOURCE,
                    headers=(("Location", "https://api.github.com/elsewhere"),),
                ),
                200,
                "GitHub API redirects are forbidden",
            ),
            (
                "uri",
                debug_trace("repos/other/project/issues/comments/7"),
                200,
                "GitHub request URI changed",
            ),
            (
                "status",
                debug_trace(USER_RESOURCE, status=500),
                500,
                "GitHub API response status shall equal 200",
            ),
            (
                "header",
                debug_trace(USER_RESOURCE).replace(
                    b"< Content-Type: application/json; charset=utf-8\n",
                    b"< malformed-header\n",
                ),
                200,
                "GitHub response header is malformed",
            ),
        )
        for label, trace, status, diagnostic in cases:
            with self.subTest(label=label):
                client = GhApiClient(
                    runner=QueueRunner(
                        [
                            completed(
                                USER_RESOURCE,
                                {"login": "tdistress"},
                                status=status,
                                trace=trace,
                            )
                        ]
                    ),
                    clock=lambda: NOW,
                )
                with self.assertRaisesRegex(ValueError, diagnostic):
                    client.get(USER_RESOURCE)

    def test_only_exact_tag_ref_accepts_canonical_404_transport(self) -> None:
        absent = completed(
            TAG_RESOURCE,
            {"message": "Not Found", "status": "404"},
            status=404,
        )
        response = GhApiClient(
            runner=QueueRunner([absent]), clock=lambda: NOW
        ).get(TAG_RESOURCE)
        self.assertEqual(404, response.status)
        other = completed(
            USER_RESOURCE,
            {"message": "Not Found", "status": "404"},
            status=404,
        )
        with self.assertRaisesRegex(
            ValueError, "GitHub API response status shall equal 200"
        ):
            GhApiClient(
                runner=QueueRunner([other]), clock=lambda: NOW
            ).get(USER_RESOURCE)

    def test_get_pages_requests_each_link_explicitly_and_proves_terminal_page(self) -> None:
        resource = "repos/tdistress/ESAF/issues/59/comments"
        page_one = f"{resource}?per_page=100&page=1"
        page_two = f"{resource}?per_page=100&page=2"
        next_link = f'<https://api.github.com/{page_two}>; rel="next"'
        runner = QueueRunner(
            [
                completed(page_one, {"items": []}, headers=(("Link", next_link),)),
                completed(page_two, {"items": []}),
            ]
        )
        pages = GhApiClient(runner=runner, clock=lambda: NOW).get_pages(resource)
        self.assertTrue(pages.complete)
        self.assertEqual((page_one, page_two), tuple(
            page.requested_resource for page in pages.pages
        ))
        self.assertEqual(
            [
                ["gh", "api", "--hostname", "github.com", page_one],
                ["gh", "api", "--hostname", "github.com", page_two],
            ],
            [call[0] for call in runner.calls],
        )

    def test_get_pages_rejects_nonsequential_or_missing_final_page(self) -> None:
        resource = "repos/tdistress/ESAF/issues/59/comments"
        page_one = f"{resource}?per_page=100&page=1"
        bad_next = f'<https://api.github.com/{resource}?per_page=100&page=3>; rel="next"'
        client = GhApiClient(
            runner=QueueRunner(
                [completed(page_one, {"items": []}, headers=(("Link", bad_next),))]
            ),
            clock=lambda: NOW,
        )
        with self.assertRaisesRegex(ValueError, "GitHub pagination is incomplete"):
            client.get_pages(resource)

    def test_get_pages_follows_canonical_link_query_order_exactly(self) -> None:
        resource = "repos/tdistress/ESAF/issues/59/comments"
        page_one = f"{resource}?per_page=100&page=1"
        linked_page_two = f"{resource}?page=2&per_page=100"
        next_link = (
            f'<https://api.github.com/{linked_page_two}>; rel="next"'
        )
        runner = QueueRunner(
            [
                completed(
                    page_one,
                    {"items": []},
                    headers=(("Link", next_link),),
                ),
                completed(linked_page_two, {"items": []}),
            ]
        )
        pages = GhApiClient(
            runner=runner, clock=lambda: NOW
        ).get_pages(resource)
        self.assertEqual(
            (page_one, linked_page_two),
            tuple(page.requested_resource for page in pages.pages),
        )


class V05StructuredCommentTests(unittest.TestCase):
    def test_parse_fenced_json_requires_exactly_one_object(self) -> None:
        expected = {"schema": "example", "approved": True}
        self.assertEqual(expected, parse_fenced_json(fenced(expected)))
        for body in (
            "no structured decision",
            "```json\n[]\n```",
            "```json\n{}\n```\n```json\n{}\n```",
            "```json\n{not json}\n```",
        ):
            with self.subTest(body=body):
                with self.assertRaisesRegex(
                    ValueError, "exactly one fenced JSON object"
                ):
                    parse_fenced_json(body)

    def test_source_record_derives_exact_body_and_response_digests(self) -> None:
        response = valid_fake_client().responses[OWNER_RESOURCE]
        payload = response.json_object()
        record = source_record(
            response,
            payload,
            expected_container_type="pull",
            expected_container_number=PR_NUMBER,
            verified_at=NOW,
        )
        self.assertEqual(
            sha256(str(payload["body"]).encode("utf-8")).hexdigest(),
            record["body_sha256"],
        )
        self.assertEqual(
            sha256(response.raw_body).hexdigest(),
            record["response_sha256"],
        )
        self.assertNotIn("headers", record)

    def test_source_record_binds_distinct_pr_and_issue_containers(self) -> None:
        client = valid_fake_client()
        post_response = client.responses[
            comment_resource(POST_MERGE_RENDERING_ID)
        ]
        post_source = source_record(
            post_response,
            post_response.json_object(),
            expected_container_type="issue",
            expected_container_number=PUBLICATION_ISSUE_NUMBER,
            verified_at=NOW,
        )
        self.assertEqual(
            (
                "https://github.com/tdistress/ESAF/issues/59"
                f"#issuecomment-{POST_MERGE_RENDERING_ID}"
            ),
            post_source["comment_url"],
        )
        cases = (
            (
                "closure verdict on issue 59",
                OWNER_RESOURCE,
                "pull",
                PR_NUMBER,
                {
                    "html_url": (
                        "https://github.com/tdistress/ESAF/issues/59"
                        f"#issuecomment-{OWNER_ID}"
                    ),
                    "issue_url": (
                        "https://api.github.com/repos/tdistress/ESAF/"
                        "issues/59"
                    ),
                },
            ),
            (
                "post-merge review on PR",
                comment_resource(POST_MERGE_RENDERING_ID),
                "issue",
                PUBLICATION_ISSUE_NUMBER,
                {
                    "html_url": (
                        f"https://github.com/tdistress/ESAF/pull/{PR_NUMBER}"
                        f"#issuecomment-{POST_MERGE_RENDERING_ID}"
                    ),
                    "issue_url": (
                        "https://api.github.com/repos/tdistress/ESAF/issues/"
                        f"{PR_NUMBER}"
                    ),
                },
            ),
            (
                "wrong issue number",
                comment_resource(POST_MERGE_RENDERING_ID),
                "issue",
                PUBLICATION_ISSUE_NUMBER,
                {
                    "html_url": (
                        "https://github.com/tdistress/ESAF/issues/60"
                        f"#issuecomment-{POST_MERGE_RENDERING_ID}"
                    ),
                    "issue_url": (
                        "https://api.github.com/repos/tdistress/ESAF/"
                        "issues/60"
                    ),
                },
            ),
            (
                "mismatched issue and HTML URLs",
                comment_resource(POST_MERGE_RENDERING_ID),
                "issue",
                PUBLICATION_ISSUE_NUMBER,
                {
                    "issue_url": (
                        "https://api.github.com/repos/tdistress/ESAF/"
                        "issues/60"
                    ),
                },
            ),
        )
        for label, resource, container_type, number, mutation in cases:
            with self.subTest(label=label):
                response = client.responses[resource]
                payload = response.json_object()
                payload.update(mutation)
                mutated = api_response(resource, payload)
                with self.assertRaisesRegex(
                    ValueError, "GitHub comment canonical URL mismatch"
                ):
                    source_record(
                        mutated,
                        payload,
                        expected_container_type=container_type,
                        expected_container_number=number,
                        verified_at=NOW,
                    )

    def test_owner_verdict_and_governance_schemas_reject_unknown_or_wrong_fields(self) -> None:
        cases = (
            (OWNER_RESOURCE, "schema", "wrong", "owner decision schema is invalid"),
            (
                comment_resource(TECHNICAL_ID),
                "kind",
                "security",
                "release verdict kind is invalid",
            ),
            (
                comment_resource(GOVERNANCE_ID),
                "authority_attestation",
                False,
                "governance authority attestation is invalid",
            ),
        )
        for resource, field, value, diagnostic in cases:
            with self.subTest(field=field):
                client = valid_fake_client()
                response = client.responses[resource]
                payload = response.json_object()
                structured = parse_fenced_json(str(payload["body"]))
                structured[field] = value
                payload["body"] = fenced(structured)
                client.responses[resource] = api_response(resource, payload)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )


class V05LocalValidationRunnerTests(unittest.TestCase):
    def test_detached_runner_validates_entire_multi_commit_pr_range_from_authenticated_base(
        self,
    ) -> None:
        class RealGitTopologyExecutor:
            def __init__(self) -> None:
                self.calls: list[tuple[list[str], Path]] = []

            def __call__(
                executor_self, args: list[str], **kwargs: object
            ) -> subprocess.CompletedProcess[bytes]:
                cwd = Path(kwargs["cwd"])
                executor_self.calls.append((args, cwd))
                if args[0] == "git":
                    return subprocess.run(args, **kwargs)
                return subprocess.CompletedProcess(
                    args, 0, b"validated\n", b""
                )

        with tempfile.TemporaryDirectory(
            prefix="esaf-v05-real-topology-"
        ) as temporary:
            repository = Path(temporary).resolve() / "repository"
            repository.mkdir()
            for command in (
                ["git", "init", "--quiet"],
                ["git", "config", "user.name", "ESAF Test"],
                ["git", "config", "user.email", "esaf@example.invalid"],
                ["git", "commit", "--allow-empty", "-m", "base"],
            ):
                subprocess.run(
                    command,
                    cwd=repository,
                    check=True,
                    capture_output=True,
                )
            closure_base = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repository,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            for message in ("first PR commit", "closure head"):
                subprocess.run(
                    ["git", "commit", "--allow-empty", "-m", message],
                    cwd=repository,
                    check=True,
                    capture_output=True,
                )
            closure_head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repository,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            immediate_parent = subprocess.run(
                ["git", "rev-parse", f"{closure_head}^"],
                cwd=repository,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            self.assertNotEqual(closure_base, immediate_parent)

            executor = RealGitTopologyExecutor()
            results = DetachedValidationRunner(
                validation_runner=LocalValidationRunner(executor),
                runner=executor,
            ).run(repository, closure_head, closure_base)
            called = [args for args, _ in executor.calls]
            self.assertIn(
                [
                    "git",
                    "diff",
                    "--check",
                    f"{closure_base}..{closure_head}",
                ],
                called,
            )
            self.assertNotIn(
                [
                    "git",
                    "diff",
                    "--check",
                    f"{immediate_parent}..{closure_head}",
                ],
                called,
            )
            self.assertEqual(
                set(COMMAND_IDS) - {"mermaid_rendering"},
                {item["name"] for item in results},
            )

    def test_detached_runner_reexecutes_after_main_contains_closure_head_using_original_closure_base(
        self,
    ) -> None:
        class PostMergeTopologyExecutor:
            def __init__(self) -> None:
                self.calls: list[tuple[list[str], Path]] = []

            def __call__(
                executor_self, args: list[str], **kwargs: object
            ) -> subprocess.CompletedProcess[bytes]:
                cwd = Path(kwargs["cwd"])
                executor_self.calls.append((args, cwd))
                if args == [
                    "git", "rev-parse", f"{CLOSURE_SHA}^{{commit}}"
                ]:
                    stdout = f"{CLOSURE_SHA}\n".encode("ascii")
                elif args == [
                    "git", "rev-parse", f"{CLOSURE_SHA}^{{tree}}"
                ]:
                    stdout = f"{CLOSURE_TREE}\n".encode("ascii")
                elif args == [
                    "git",
                    "merge-base",
                    CLOSURE_BASE,
                    CLOSURE_SHA,
                ]:
                    stdout = f"{CLOSURE_BASE}\n".encode("ascii")
                elif args[:4] == [
                    "git", "worktree", "add", "--detach"
                ]:
                    Path(args[4]).mkdir()
                    stdout = b""
                elif args == ["git", "rev-parse", "HEAD"]:
                    stdout = f"{CLOSURE_SHA}\n".encode("ascii")
                elif args == ["git", "rev-parse", "HEAD^{tree}"]:
                    stdout = f"{CLOSURE_TREE}\n".encode("ascii")
                elif args == [
                    "git", "merge-base", CLOSURE_SHA, "main"
                ]:
                    stdout = f"{CLOSURE_SHA}\n".encode("ascii")
                elif args == ["git", "status", "--porcelain=v1"]:
                    stdout = b""
                elif args[:4] == [
                    "git", "worktree", "remove", "--force"
                ]:
                    stdout = b""
                else:
                    stdout = f"executed {' '.join(args)}\n".encode()
                return subprocess.CompletedProcess(
                    args, 0, stdout, b""
                )

        executor = PostMergeTopologyExecutor()
        results = DetachedValidationRunner(
            validation_runner=LocalValidationRunner(executor),
            runner=executor,
        ).run(ROOT, CLOSURE_SHA, CLOSURE_BASE)
        called = [args for args, _ in executor.calls]
        self.assertNotIn(
            ["git", "merge-base", CLOSURE_SHA, "main"], called
        )
        self.assertIn(
            [
                os.fsdecode(Path(os.sys.executable)),
                "tools/validate_crosswalks.py",
                "--check",
                "--baseline-ref",
                CLOSURE_BASE,
            ],
            called,
        )
        self.assertIn(
            [
                "git",
                "diff",
                "--check",
                f"{CLOSURE_BASE}..{CLOSURE_SHA}",
            ],
            called,
        )
        self.assertEqual(
            set(COMMAND_IDS) - {"mermaid_rendering"},
            {item["name"] for item in results},
        )

    def test_detached_runner_executes_at_verified_immutable_closure_head(
        self,
    ) -> None:
        inner = FakeValidationRunner()

        def git_runner(
            args: list[str], **kwargs: object
        ) -> subprocess.CompletedProcess[bytes]:
            cwd = Path(kwargs["cwd"])
            if args == [
                "git", "rev-parse", f"{CLOSURE_SHA}^{{commit}}"
            ]:
                stdout = f"{CLOSURE_SHA}\n".encode("ascii")
            elif args == [
                "git", "rev-parse", f"{CLOSURE_SHA}^{{tree}}"
            ]:
                stdout = f"{CLOSURE_TREE}\n".encode("ascii")
            elif args == [
                "git", "merge-base", CLOSURE_BASE, CLOSURE_SHA
            ]:
                stdout = f"{CLOSURE_BASE}\n".encode("ascii")
            elif args[:4] == ["git", "worktree", "add", "--detach"]:
                Path(args[4]).mkdir()
                stdout = b""
            elif args == ["git", "rev-parse", "HEAD"]:
                self.assertNotEqual(ROOT, cwd)
                stdout = f"{CLOSURE_SHA}\n".encode("ascii")
            elif args == ["git", "rev-parse", "HEAD^{tree}"]:
                self.assertNotEqual(ROOT, cwd)
                stdout = f"{CLOSURE_TREE}\n".encode("ascii")
            elif args[:4] == ["git", "worktree", "remove", "--force"]:
                stdout = b""
            else:
                raise AssertionError(args)
            return subprocess.CompletedProcess(args, 0, stdout, b"")

        results = DetachedValidationRunner(
            validation_runner=inner,
            runner=git_runner,
        ).run(ROOT, CLOSURE_SHA, CLOSURE_BASE)
        self.assertEqual(1, len(inner.calls))
        self.assertNotEqual(ROOT, inner.calls[0][0])
        self.assertEqual(
            (CLOSURE_SHA, CLOSURE_BASE),
            inner.calls[0][1:],
        )
        self.assertEqual(
            set(COMMAND_IDS) - {"mermaid_rendering"},
            {item["name"] for item in results},
        )

    def test_runner_executes_exact_canonical_nonvisual_commands(self) -> None:
        executor = RecordingCommandExecutor()
        results = LocalValidationRunner(executor).run(
            ROOT, CLOSURE_SHA, CLOSURE_BASE
        )
        self.assertEqual(
            set(COMMAND_IDS) - {"mermaid_rendering"},
            {item["name"] for item in results},
        )
        called = [call[0] for call in executor.calls]
        self.assertIn(
            [
                os.fsdecode(Path(os.sys.executable)),
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-v",
            ],
            called,
        )
        self.assertIn(
            [
                os.fsdecode(Path(os.sys.executable)),
                "tools/validate_crosswalks.py",
                "--check",
                "--baseline-ref",
                "b" * 40,
            ],
            called,
        )
        self.assertIn(
            [
                "git",
                "diff",
                "--check",
                f"{'b' * 40}..{CLOSURE_SHA}",
            ],
            called,
        )
        validation_calls = [
            kwargs
            for args, kwargs in executor.calls
            if args and args[0] != "git"
        ]
        self.assertTrue(validation_calls)
        self.assertTrue(all(
            kwargs["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
            for kwargs in validation_calls
        ))


class V05AcquisitionTests(unittest.TestCase):
    def test_operational_cli_removes_caller_dates_and_postmerge_results(
        self,
    ) -> None:
        required = [
            "--pr-number", str(PR_NUMBER),
            "--expected-head", CLOSURE_SHA,
            "--owner-comment-id", str(OWNER_ID),
            "--technical-comment-id", str(TECHNICAL_ID),
            "--editorial-comment-id", str(EDITORIAL_ID),
            "--terminology-comment-id", str(TERMINOLOGY_ID),
            "--rendering-comment-id", str(RENDERING_ID),
            "--profile-scope-comment-id", str(PROFILE_SCOPE_ID),
            "--governance-comment-id", str(GOVERNANCE_ID),
            "--security-overclaiming-comment-id",
            str(SECURITY_OVERCLAIMING_ID),
            "--whole-range-comment-id", str(WHOLE_RANGE_ID),
            "--output", str(ROOT.parent / "evidence.json"),
        ]
        parsed = build_parser().parse_args(required)
        self.assertFalse(hasattr(parsed, "publication_date"))
        self.assertFalse(hasattr(parsed, "post_merge_results"))
        for removed in ("--publication-date", "--post-merge-results"):
            with self.subTest(removed=removed):
                with redirect_stderr(io.StringIO()), self.assertRaises(
                    SystemExit
                ):
                    build_parser().parse_args(
                        [*required, removed, "fabricated.json"]
                    )

    def test_collector_requires_live_open_canonical_issue_55(self) -> None:
        evidence = collect_closure_evidence(
            valid_fake_client(), **valid_collection_args()
        )
        self.assertEqual(
            {
                "resource": ISSUE_55_RESOURCE,
                "number": 55,
                "state": "open",
                "url": "https://github.com/tdistress/ESAF/issues/55",
                "response_sha256": sha256(
                    valid_fake_client().responses[
                        ISSUE_55_RESOURCE
                    ].raw_body
                ).hexdigest(),
            },
            evidence["issue_55"],
        )
        for label, mutation in (
            ("closed", {"state": "closed"}),
            ("pull request", {"pull_request": {"url": "https://example.test"}}),
            ("foreign number", {"number": 56}),
        ):
            with self.subTest(label=label):
                client = valid_fake_client()
                response = client.responses[ISSUE_55_RESOURCE]
                payload = response.json_object()
                payload.update(mutation)
                client.responses[ISSUE_55_RESOURCE] = api_response(
                    ISSUE_55_RESOURCE, payload
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "issue 55 shall be the canonical open repository issue",
                ):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_collector_binds_github_actions_app_and_canonical_workflow_run(
        self,
    ) -> None:
        evidence = collect_closure_evidence(
            valid_fake_client(), **valid_collection_args()
        )
        check = evidence["github_checks"]["observed"][0]
        self.assertEqual("github-actions", check["app_slug"])
        self.assertEqual(9001, check["run_id"])
        self.assertEqual(
            ".github/workflows/catalog-validation.yml",
            check["workflow_path"],
        )
        self.assertEqual("Repository validation", check["workflow_name"])
        self.assertEqual("tdistress/ESAF", check["repository"])

        mutations = (
            (
                "foreign app",
                lambda client: client.page_sets[
                    CHECKS_RESOURCE
                ].pages[0].json_object()["check_runs"][0]["app"].update(
                    slug="attacker-app"
                ),
            ),
            (
                "foreign workflow",
                lambda client: client.responses[
                    ACTIONS_RUN_RESOURCE
                ].json_object().__setitem__(
                    "path", ".github/workflows/attacker.yml"
                ),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                client = valid_fake_client()
                if label == "foreign app":
                    page = client.page_sets[CHECKS_RESOURCE].pages[0]
                    payload = page.json_object()
                    payload["check_runs"][0]["app"]["slug"] = "attacker-app"
                    client.page_sets[CHECKS_RESOURCE] = replace(
                        client.page_sets[CHECKS_RESOURCE],
                        pages=(
                            api_response(
                                CHECKS_PAGE_ONE,
                                payload,
                            ),
                        ),
                    )
                else:
                    response = client.responses[ACTIONS_RUN_RESOURCE]
                    payload = response.json_object()
                    payload["path"] = ".github/workflows/attacker.yml"
                    client.responses[ACTIONS_RUN_RESOURCE] = api_response(
                        ACTIONS_RUN_RESOURCE, payload
                    )
                with self.assertRaisesRegex(
                    ValueError,
                    "canonical GitHub Actions workflow run",
                ):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_every_resource_records_its_own_retrieval_time(self) -> None:
        evidence = collect_closure_evidence(
            valid_fake_client(), **valid_collection_args()
        )
        resources = {
            item["resource_id"]: item
            for item in evidence["acquisition"]["resources"]
        }
        self.assertTrue(resources)
        self.assertTrue(
            all(
                item["retrieved_at"] == "2026-07-27T12:10:00Z"
                for item in resources.values()
            )
        )
        for verdict in (
            "scope",
            "technical",
            "editorial",
            "terminology",
            "rendering",
            "profile_scope",
            "security_overclaiming",
            "whole_range",
            "governance",
        ):
            resource = resources[
                evidence[verdict]["source"]["acquisition_resource_id"]
            ]
            self.assertEqual(
                resource["retrieved_at"],
                evidence[verdict]["source"]["source_verified_at"],
            )

    def test_review_dates_follow_independent_comment_dates_not_tag_day(
        self,
    ) -> None:
        client = valid_fake_client()
        dates = {
            TECHNICAL_ID: "2026-07-27T20:00:00Z",
            EDITORIAL_ID: "2026-07-28T20:00:00Z",
            GOVERNANCE_ID: "2026-07-29T20:00:00Z",
        }
        acquired_at = datetime(
            2026, 7, 30, 12, 10, tzinfo=timezone.utc
        )
        client.responses = {
            resource: replace(response, retrieved_at=acquired_at)
            for resource, response in client.responses.items()
        }
        client.page_sets = {
            resource: replace(
                page_set,
                pages=tuple(
                    replace(page, retrieved_at=acquired_at)
                    for page in page_set.pages
                ),
            )
            for resource, page_set in client.page_sets.items()
        }
        for comment_id, created_at in dates.items():
            resource = comment_resource(comment_id)
            response = client.responses[resource]
            payload = response.json_object()
            body = parse_fenced_json(payload["body"])
            body["date"] = created_at[:10]
            payload["body"] = fenced(body)
            payload["created_at"] = created_at
            payload["updated_at"] = created_at
            client.responses[resource] = api_response(
                resource, payload, retrieved_at=acquired_at
            )
        arguments = valid_collection_args()
        arguments["now"] = acquired_at
        evidence = collect_closure_evidence(client, **arguments)
        self.assertEqual("2026-07-27", evidence["technical"]["date"])
        self.assertEqual("2026-07-28", evidence["editorial"]["date"])
        self.assertEqual("2026-07-29", evidence["governance"]["date"])

    def test_taggable_refresh_executes_merge_head_and_fetches_visual_review(
        self,
    ) -> None:
        client = valid_fake_client()
        closure = collect_closure_evidence(
            client, **valid_collection_args()
        )
        mark_pull_request_merged(client)
        merge_runner = FakeValidationRunner()
        taggable = refresh_taggable_evidence(
            client,
            base_evidence=closure,
            merge_head=MERGE_SHA,
            post_merge_rendering_comment_id=POST_MERGE_RENDERING_ID,
            post_merge_validation_runner=merge_runner,
            **valid_collection_args(),
        )
        self.assertEqual(
            [(ROOT, MERGE_SHA, CLOSURE_BASE)],
            merge_runner.calls,
        )
        self.assertEqual(
            MERGE_SHA, taggable["post_merge"]["sha"]
        )
        self.assertEqual(
            comment_resource(POST_MERGE_RENDERING_ID),
            taggable["post_merge"]["rendering_source"][
                "acquisition_resource_id"
            ],
        )

    def test_collector_requires_pr_base_sha_to_equal_authenticated_closure_base(
        self,
    ) -> None:
        evidence = collect_closure_evidence(
            valid_fake_client(), **valid_collection_args()
        )
        self.assertEqual(CLOSURE_BASE, evidence["closure_base"])
        cases = (
            (
                "missing",
                lambda pull: pull.pop("base"),
            ),
            (
                "substituted",
                lambda pull: pull["base"].__setitem__(
                    "sha", CLOSURE_SHA
                ),
            ),
            (
                "non-main",
                lambda pull: pull["base"].__setitem__(
                    "ref", "release"
                ),
            ),
            (
                "wrong-repo",
                lambda pull: pull["base"]["repo"].__setitem__(
                    "full_name", "other/ESAF"
                ),
            ),
            (
                "wrong-owner",
                lambda pull: pull["base"]["repo"]["owner"].__setitem__(
                    "login", "other"
                ),
            ),
            (
                "wrong-url",
                lambda pull: pull["base"]["repo"].__setitem__(
                    "url", "https://api.github.com/repos/other/ESAF"
                ),
            ),
        )
        for label, mutate in cases:
            with self.subTest(label=label):
                client = valid_fake_client()
                response = client.responses[PR_RESOURCE]
                payload = response.json_object()
                mutate(payload)
                client.responses[PR_RESOURCE] = api_response(
                    PR_RESOURCE, payload
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "GitHub pull request base is invalid",
                ):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_collector_requires_canonical_authenticated_pr_head(
        self,
    ) -> None:
        cases = (
            (
                "sha",
                lambda head: head.__setitem__("sha", "f" * 40),
            ),
            (
                "ref",
                lambda head: head.__setitem__("ref", ""),
            ),
            (
                "label",
                lambda head: head.__setitem__(
                    "label", "other:branch"
                ),
            ),
            (
                "repo",
                lambda head: head["repo"].__setitem__(
                    "full_name", "other/ESAF"
                ),
            ),
        )
        for label, mutate in cases:
            with self.subTest(label=label):
                client = valid_fake_client()
                response = client.responses[PR_RESOURCE]
                payload = response.json_object()
                mutate(payload["head"])
                client.responses[PR_RESOURCE] = api_response(
                    PR_RESOURCE, payload
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "GitHub pull request does not match closure head",
                ):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_collector_requires_nonempty_canonical_closure_parents(
        self,
    ) -> None:
        multiple = valid_fake_client()
        response = multiple.responses[COMMIT_RESOURCE]
        payload = response.json_object()
        payload["parents"].append(
            {
                "sha": "f" * 40,
                "url": (
                    "https://api.github.com/repos/tdistress/ESAF/"
                    f"commits/{'f' * 40}"
                ),
            }
        )
        multiple.responses[COMMIT_RESOURCE] = api_response(
            COMMIT_RESOURCE, payload
        )
        evidence = collect_closure_evidence(
            multiple, **valid_collection_args()
        )
        self.assertEqual(CLOSURE_BASE, evidence["closure_base"])
        for parents in (
            [],
            [
                {
                    "sha": "not-a-sha",
                    "url": "https://api.github.com/repos/tdistress/ESAF/commits/not-a-sha",
                }
            ],
            [
                {
                    "sha": CLOSURE_PARENT,
                    "url": "https://api.github.com/repos/other/ESAF/commits/"
                    f"{CLOSURE_PARENT}",
                }
            ],
        ):
            with self.subTest(parent_count=len(parents)):
                client = valid_fake_client()
                response = client.responses[COMMIT_RESOURCE]
                payload = response.json_object()
                payload["parents"] = parents
                client.responses[COMMIT_RESOURCE] = api_response(
                    COMMIT_RESOURCE, payload
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "GitHub closure commit parents are invalid",
                ):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_collector_uses_real_github_commit_tree_shape_for_closure_and_merge(
        self,
    ) -> None:
        client = valid_fake_client()
        closure = collect_closure_evidence(
            client, **valid_collection_args()
        )
        self.assertEqual(CLOSURE_TREE, closure["closure_tree"])
        mark_pull_request_merged(client)
        taggable = refresh_taggable_evidence(
            client,
            base_evidence=closure,
            merge_head=MERGE_SHA,
            post_merge_rendering_comment_id=POST_MERGE_RENDERING_ID,
            post_merge_validation_runner=FakeValidationRunner(),
            **valid_collection_args(),
        )
        self.assertEqual(CLOSURE_TREE, taggable["merge_tree"])

    def test_collector_builds_gate_valid_evidence_from_live_envelopes(self) -> None:
        evidence = collect_closure_evidence(
            valid_fake_client(), **valid_collection_args()
        )
        record = record_fixture("closure_candidate")
        record["mapping_decision_basis"] = "owner_risk_acceptance"
        self.assertEqual(
            [],
            validate_external_evidence(
                ROOT, record, evidence, CLOSURE_SHA, "closure", NOW
            ),
        )
        self.assertEqual(set(COMMAND_IDS), {
            item["name"] for item in evidence["candidate_commands"]
        })
        self.assertEqual(
            {
                f"executed:{name}"
                for name in COMMAND_IDS
                if name != "mermaid_rendering"
            },
            {
                item["result"]
                for item in evidence["candidate_commands"]
                if item["name"] != "mermaid_rendering"
            },
        )

    def test_collector_executes_every_nonvisual_canonical_gate(self) -> None:
        runner = FakeValidationRunner()
        arguments = valid_collection_args()
        arguments["validation_runner"] = runner
        evidence = collect_closure_evidence(
            valid_fake_client(), **arguments
        )
        self.assertEqual(
            [(ROOT, CLOSURE_SHA, CLOSURE_BASE)], runner.calls
        )
        self.assertEqual(
            set(COMMAND_IDS) - {"mermaid_rendering"},
            {
                item["name"]
                for item in evidence["candidate_commands"]
                if item["name"] != "mermaid_rendering"
            },
        )
        check_url = evidence["github_checks"]["observed"][0]["url"]
        self.assertNotIn(
            check_url,
            {
                item["result"]
                for item in evidence["candidate_commands"]
                if item["name"] != "mermaid_rendering"
            },
        )

    def test_live_retrieval_timestamps_are_validated_after_each_fetch(
        self,
    ) -> None:
        fixture = valid_fake_client()
        client = LiveTimestampFakeClient(
            fixture.login,
            fixture.responses,
            fixture.page_sets,
        )
        arguments = valid_collection_args()
        del arguments["now"]
        evidence = collect_closure_evidence(client, **arguments)
        self.assertEqual(
            "tdistress", evidence["acquisition"]["authenticated_login"]
        )

    def test_collector_rejects_missing_or_failed_local_gate_result(self) -> None:
        cases = ("missing", "failed")
        for case in cases:
            with self.subTest(case=case):
                runner = FakeValidationRunner()
                if case == "missing":
                    runner.results.pop()
                else:
                    runner.results[0]["exit_code"] = 1
                arguments = valid_collection_args()
                arguments["validation_runner"] = runner
                with self.assertRaisesRegex(
                    ValueError, "local validation command results are invalid"
                ):
                    collect_closure_evidence(
                        valid_fake_client(), **arguments
                    )

    def test_collector_proves_exact_remote_tag_absence(self) -> None:
        evidence = collect_closure_evidence(
            valid_fake_client(), **valid_collection_args()
        )
        self.assertEqual(
            {
                "resource": TAG_RESOURCE,
                "exists": False,
                "status": 404,
                "response_sha256": sha256(
                    valid_fake_client().responses[TAG_RESOURCE].raw_body
                ).hexdigest(),
            },
            evidence["tag_state"],
        )
        for label, mutate, diagnostic in (
            (
                "existing",
                lambda response: replace(response, status=200),
                "remote v0.5-beta tag already exists",
            ),
            (
                "drift",
                lambda response: replace(
                    response,
                    observed_request_uri=(
                        "/repos/other/project/git/ref/tags/v0.5-beta"
                    ),
                ),
                "GitHub request URI changed",
            ),
            (
                "failure",
                lambda response: replace(response, status=500),
                "GitHub tag lookup status shall equal 404",
            ),
        ):
            with self.subTest(label=label):
                client = valid_fake_client()
                client.responses[TAG_RESOURCE] = mutate(
                    client.responses[TAG_RESOURCE]
                )
                with self.assertRaisesRegex(ValueError, diagnostic):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_collector_rejects_preexisting_local_v05_tag(self) -> None:
        def local_tag_runner(
            args: list[str], **kwargs: object
        ) -> subprocess.CompletedProcess[bytes]:
            del kwargs
            self.assertEqual(
                [
                    "git",
                    "show-ref",
                    "--verify",
                    "--quiet",
                    "refs/tags/v0.5-beta",
                ],
                args,
            )
            return subprocess.CompletedProcess(args, 0, b"", b"")

        arguments = valid_collection_args()
        arguments["repository_runner"] = local_tag_runner
        with self.assertRaisesRegex(
            ValueError, "local v0.5-beta tag already exists"
        ):
            collect_closure_evidence(
                valid_fake_client(), **arguments
            )

    def test_collector_rejects_redirected_resource(self) -> None:
        client = valid_fake_client()
        response = client.responses[OWNER_RESOURCE]
        client.responses[OWNER_RESOURCE] = replace(
            response,
            observed_request_uri="/repos/other/project/issues/comments/7",
        )
        with self.assertRaisesRegex(ValueError, "GitHub request URI changed"):
            collect_closure_evidence(client, **valid_collection_args())

    def test_collector_rejects_incomplete_pagination(self) -> None:
        client = valid_fake_client()
        client.page_sets[CHECKS_RESOURCE] = replace(
            client.page_sets[CHECKS_RESOURCE], complete=False
        )
        with self.assertRaisesRegex(
            ValueError, "GitHub pagination is incomplete"
        ):
            collect_closure_evidence(client, **valid_collection_args())

    def test_collector_rejects_page_set_with_unfollowed_next_link(self) -> None:
        client = valid_fake_client()
        page_set = client.page_sets[CHECKS_RESOURCE]
        page = replace(
            page_set.pages[0],
            headers=(
                (
                    "link",
                    (
                        f'<https://api.github.com/{CHECKS_RESOURCE}'
                        '?per_page=100&page=2>; rel="next"'
                    ),
                ),
            ),
        )
        client.page_sets[CHECKS_RESOURCE] = replace(
            page_set, pages=(page,)
        )
        with self.assertRaisesRegex(
            ValueError, "GitHub pagination is incomplete"
        ):
            collect_closure_evidence(client, **valid_collection_args())

    def test_source_digest_uses_exact_raw_body(self) -> None:
        client = valid_fake_client()
        response = client.responses[OWNER_RESOURCE]
        payload = response.json_object()
        raw_body = json.dumps(payload, indent=3).encode("utf-8")
        client.responses[OWNER_RESOURCE] = replace(
            response, raw_body=raw_body
        )
        evidence = collect_closure_evidence(
            client, **valid_collection_args()
        )
        expected = sha256(raw_body).hexdigest()
        self.assertEqual(
            expected,
            evidence["mapping_decisions"][0]["source"]["response_sha256"],
        )
        acquisition = {
            item["resource_id"]: item
            for item in evidence["acquisition"]["resources"]
        }
        self.assertEqual(expected, acquisition[OWNER_RESOURCE]["response_sha256"])

    def test_collector_rejects_wrong_login_status_headers_and_stale_acquisition(self) -> None:
        cases: list[tuple[str, callable, str]] = [
            (
                "login",
                lambda client: setattr(client, "login", ""),
                "authenticated GitHub login is required",
            ),
            (
                "status",
                lambda client: client.responses.__setitem__(
                    OWNER_RESOURCE,
                    replace(client.responses[OWNER_RESOURCE], status=500),
                ),
                "GitHub API response status shall equal 200",
            ),
            (
                "headers",
                lambda client: client.responses.__setitem__(
                    OWNER_RESOURCE,
                    replace(
                        client.responses[OWNER_RESOURCE],
                        headers=(("bad header", "value"),),
                    ),
                ),
                "GitHub response header is malformed",
            ),
            (
                "stale",
                lambda client: client.responses.__setitem__(
                    OWNER_RESOURCE,
                    replace(
                        client.responses[OWNER_RESOURCE],
                        retrieved_at=NOW - timedelta(minutes=16),
                    ),
                ),
                "GitHub acquisition is stale",
            ),
        ]
        for label, mutate, diagnostic in cases:
            with self.subTest(label=label):
                client = valid_fake_client()
                mutate(client)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_collector_rejects_edited_or_pre_candidate_comment(self) -> None:
        cases = (
            (
                "edited",
                "updated_at",
                "2026-07-27T12:01:00Z",
                "GitHub comment shall be unedited",
            ),
            (
                "pre-candidate",
                "created_at",
                "2026-07-27T10:59:59Z",
                "GitHub comment shall postdate closure commit",
            ),
        )
        for label, field, value, diagnostic in cases:
            with self.subTest(label=label):
                client = valid_fake_client()
                response = client.responses[OWNER_RESOURCE]
                payload = response.json_object()
                payload[field] = value
                if field == "created_at":
                    payload["updated_at"] = value
                client.responses[OWNER_RESOURCE] = api_response(
                    OWNER_RESOURCE, payload
                )
                with self.assertRaisesRegex(ValueError, diagnostic):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_collector_rejects_mismatched_canonical_html_or_api_url(self) -> None:
        for field, value in (
            ("url", "https://api.github.com/repos/other/project/issues/comments/20"),
            ("html_url", "https://github.com/other/project/issues/1#issuecomment-20"),
        ):
            with self.subTest(field=field):
                client = valid_fake_client()
                response = client.responses[OWNER_RESOURCE]
                payload = response.json_object()
                payload[field] = value
                client.responses[OWNER_RESOURCE] = api_response(
                    OWNER_RESOURCE, payload
                )
                with self.assertRaisesRegex(
                    ValueError, "GitHub comment canonical URL mismatch"
                ):
                    collect_closure_evidence(
                        client, **valid_collection_args()
                    )

    def test_collector_rejects_raw_body_that_does_not_match_decoded_payload(self) -> None:
        client = valid_fake_client()
        response = client.responses[OWNER_RESOURCE]
        client.responses[OWNER_RESOURCE] = replace(
            response, raw_body=b'{"body":"truncated mutation"}'
        )
        with self.assertRaisesRegex(
            ValueError, "GitHub comment response is incomplete"
        ):
            collect_closure_evidence(client, **valid_collection_args())

    def test_refresh_reacquires_sources_and_binds_equal_merge_tree(self) -> None:
        client = valid_fake_client()
        closure = collect_closure_evidence(
            client, **valid_collection_args()
        )
        mark_pull_request_merged(client)
        taggable = refresh_taggable_evidence(
            client,
            base_evidence=closure,
            merge_head=MERGE_SHA,
            post_merge_rendering_comment_id=POST_MERGE_RENDERING_ID,
            post_merge_validation_runner=FakeValidationRunner(),
            **valid_collection_args(),
        )
        record = record_fixture("closure_candidate")
        record["mapping_decision_basis"] = "owner_risk_acceptance"
        self.assertEqual(
            [],
            validate_external_evidence(
                ROOT, record, taggable, MERGE_SHA, "taggable", NOW
            ),
        )

    def test_refresh_rejects_check_inferred_or_tampered_base_commands(
        self,
    ) -> None:
        client = valid_fake_client()
        closure = collect_closure_evidence(
            client, **valid_collection_args()
        )
        mark_pull_request_merged(client)
        check_url = closure["github_checks"]["observed"][0]["url"]
        for replacement in ("tampered", check_url):
            with self.subTest(replacement=replacement):
                changed = deepcopy(closure)
                changed["candidate_commands"][0]["result"] = replacement
                runner = FakeValidationRunner()
                arguments = valid_collection_args()
                arguments["validation_runner"] = runner
                with self.assertRaisesRegex(
                    ValueError,
                    "base candidate commands shall equal fresh execution",
                ):
                    refresh_taggable_evidence(
                        client,
                        base_evidence=changed,
                        merge_head=MERGE_SHA,
                        post_merge_rendering_comment_id=(
                            POST_MERGE_RENDERING_ID
                        ),
                        **arguments,
                    )
                self.assertEqual(
                    [(ROOT, CLOSURE_SHA, CLOSURE_BASE)],
                    runner.calls,
                )

    def test_collector_binds_verdict_date_to_comment_creation_date(
        self,
    ) -> None:
        client = valid_fake_client()
        response = client.responses[comment_resource(TECHNICAL_ID)]
        payload = response.json_object()
        body = parse_fenced_json(payload["body"])
        body["date"] = "2026-07-26"
        payload["body"] = fenced(body)
        client.responses[comment_resource(TECHNICAL_ID)] = api_response(
            comment_resource(TECHNICAL_ID), payload
        )
        with self.assertRaisesRegex(
            ValueError, "release verdict disposition is invalid"
        ):
            collect_closure_evidence(
                client, **valid_collection_args()
            )

    def test_refresh_rejects_postmerge_visual_review_for_wrong_tree(
        self,
    ) -> None:
        client = valid_fake_client()
        closure = collect_closure_evidence(
            client, **valid_collection_args()
        )
        mark_pull_request_merged(client)
        response = client.responses[
            comment_resource(POST_MERGE_RENDERING_ID)
        ]
        payload = response.json_object()
        body = parse_fenced_json(payload["body"])
        body["tree"] = "f" * 40
        payload["body"] = fenced(body)
        client.responses[
            comment_resource(POST_MERGE_RENDERING_ID)
        ] = api_response(
            comment_resource(POST_MERGE_RENDERING_ID),
            payload,
        )
        with self.assertRaisesRegex(
            ValueError, "post-merge rendering verdict is invalid"
        ):
            refresh_taggable_evidence(
                client,
                base_evidence=closure,
                merge_head=MERGE_SHA,
                post_merge_rendering_comment_id=(
                    POST_MERGE_RENDERING_ID
                ),
                post_merge_validation_runner=FakeValidationRunner(),
                **valid_collection_args(),
            )


    def test_refresh_requires_pr_merged_to_exact_merge_head(self) -> None:
        initial = valid_fake_client()
        closure = collect_closure_evidence(
            initial, **valid_collection_args()
        )
        merged = valid_fake_client()
        mark_pull_request_merged(merged)
        taggable = refresh_taggable_evidence(
            merged,
            base_evidence=closure,
            merge_head=MERGE_SHA,
            post_merge_rendering_comment_id=POST_MERGE_RENDERING_ID,
            post_merge_validation_runner=FakeValidationRunner(),
            **valid_collection_args(),
        )
        self.assertEqual(closure["merge_state"], taggable["merge_state"])
        wrong_merge = valid_fake_client()
        mark_pull_request_merged(wrong_merge, "f" * 40)
        with self.assertRaisesRegex(
            ValueError, "pull request shall be merged to exact merge head"
        ):
            refresh_taggable_evidence(
                wrong_merge,
                base_evidence=closure,
                merge_head=MERGE_SHA,
                post_merge_rendering_comment_id=(
                    POST_MERGE_RENDERING_ID
                ),
                **valid_collection_args(),
            )

    def test_refresh_rejects_changed_source_and_merge_tree(self) -> None:
        client = valid_fake_client()
        closure = collect_closure_evidence(
            client, **valid_collection_args()
        )
        mark_pull_request_merged(client)
        changed = deepcopy(closure)
        changed["technical"]["source"]["body_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "GitHub source changed"):
            refresh_taggable_evidence(
                client,
                base_evidence=changed,
                merge_head=MERGE_SHA,
                post_merge_rendering_comment_id=(
                    POST_MERGE_RENDERING_ID
                ),
                **valid_collection_args(),
            )
        client = valid_fake_client()
        mark_pull_request_merged(client)
        merge = client.responses[MERGE_COMMIT_RESOURCE]
        payload = merge.json_object()
        payload["commit"]["tree"]["sha"] = "f" * 40
        client.responses[MERGE_COMMIT_RESOURCE] = api_response(
            MERGE_COMMIT_RESOURCE, payload
        )
        with self.assertRaisesRegex(
            ValueError, "merged tree shall equal closure tree"
        ):
            refresh_taggable_evidence(
                client,
                base_evidence=closure,
                merge_head=MERGE_SHA,
                post_merge_rendering_comment_id=(
                    POST_MERGE_RENDERING_ID
                ),
                **valid_collection_args(),
            )

    def test_refresh_rejects_changed_authenticated_pr_base_before_reexecution(
        self,
    ) -> None:
        initial = valid_fake_client()
        closure = collect_closure_evidence(
            initial, **valid_collection_args()
        )
        changed = valid_fake_client()
        mark_pull_request_merged(changed)
        response = changed.responses[PR_RESOURCE]
        payload = response.json_object()
        payload["base"]["sha"] = "f" * 40
        changed.responses[PR_RESOURCE] = api_response(
            PR_RESOURCE, payload
        )
        runner = FakeValidationRunner()
        arguments = valid_collection_args()
        arguments["validation_runner"] = runner
        with self.assertRaisesRegex(
            ValueError,
            "authenticated pull request base changed during refresh",
        ):
            refresh_taggable_evidence(
                changed,
                base_evidence=closure,
                merge_head=MERGE_SHA,
                post_merge_rendering_comment_id=(
                    POST_MERGE_RENDERING_ID
                ),
                **arguments,
            )
        self.assertEqual([], runner.calls)

    def test_refresh_rejects_immediate_parent_as_base_before_runner(
        self,
    ) -> None:
        client = valid_fake_client()
        closure = collect_closure_evidence(
            client, **valid_collection_args()
        )
        changed = deepcopy(closure)
        changed["closure_base"] = CLOSURE_PARENT
        mark_pull_request_merged(client)
        runner = FakeValidationRunner()
        arguments = valid_collection_args()
        arguments["validation_runner"] = runner
        with self.assertRaisesRegex(
            ValueError,
            "authenticated pull request base changed during refresh",
        ):
            refresh_taggable_evidence(
                client,
                base_evidence=changed,
                merge_head=MERGE_SHA,
                post_merge_rendering_comment_id=(
                    POST_MERGE_RENDERING_ID
                ),
                **arguments,
            )
        self.assertEqual([], runner.calls)

    def test_operational_cli_rejects_local_snapshot_switches(self) -> None:
        parser = build_parser()
        required = [
            "--pr-number", str(PR_NUMBER),
            "--expected-head", CLOSURE_SHA,
            "--owner-comment-id", str(OWNER_ID),
            "--technical-comment-id", str(TECHNICAL_ID),
            "--editorial-comment-id", str(EDITORIAL_ID),
            "--terminology-comment-id", str(TERMINOLOGY_ID),
            "--rendering-comment-id", str(RENDERING_ID),
            "--profile-scope-comment-id", str(PROFILE_SCOPE_ID),
            "--governance-comment-id", str(GOVERNANCE_ID),
            "--security-overclaiming-comment-id",
            str(SECURITY_OVERCLAIMING_ID),
            "--whole-range-comment-id", str(WHOLE_RANGE_ID),
            "--output", str(ROOT.parent / "evidence.json"),
        ]
        for option in (
            "--comment-json",
            "--pr-json",
            "--check-json",
            "--merge-state-json",
            "--author-identity",
            "--body-digest",
            "--verdict-json",
        ):
            with self.subTest(option=option):
                error = io.StringIO()
                with redirect_stderr(error), self.assertRaises(SystemExit):
                    parser.parse_args(
                        [*required, option, "fabricated.json"]
                    )
                self.assertIn(
                    f"unrecognized arguments: {option} fabricated.json",
                    error.getvalue(),
                )

    def test_cli_rejects_output_in_any_registered_worktree_or_git_common_dir(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            other_worktree = base / "registered worktree"
            common_dir = base / "repository.git"
            other_worktree.mkdir()
            common_dir.mkdir()

            def git_runner(
                args: list[str], **kwargs: object
            ) -> subprocess.CompletedProcess[bytes]:
                del kwargs
                if args == ["git", "worktree", "list", "--porcelain"]:
                    body = (
                        f"worktree {ROOT}\nHEAD {CLOSURE_SHA}\n"
                        "branch refs/heads/main\n\n"
                        f"worktree {other_worktree}\nHEAD {CLOSURE_SHA}\n"
                        "detached\n\n"
                    )
                    return subprocess.CompletedProcess(
                        args, 0, body.encode("utf-8"), b""
                    )
                if args == ["git", "rev-parse", "--git-common-dir"]:
                    return subprocess.CompletedProcess(
                        args, 0, f"{common_dir}\n".encode("utf-8"), b""
                    )
                raise AssertionError(args)

            required = [
                "--pr-number", str(PR_NUMBER),
                "--expected-head", CLOSURE_SHA,
                "--owner-comment-id", str(OWNER_ID),
                "--technical-comment-id", str(TECHNICAL_ID),
                "--editorial-comment-id", str(EDITORIAL_ID),
                "--terminology-comment-id", str(TERMINOLOGY_ID),
                "--rendering-comment-id", str(RENDERING_ID),
                "--profile-scope-comment-id", str(PROFILE_SCOPE_ID),
                "--governance-comment-id", str(GOVERNANCE_ID),
                "--security-overclaiming-comment-id",
                str(SECURITY_OVERCLAIMING_ID),
                "--whole-range-comment-id", str(WHOLE_RANGE_ID),
            ]
            for forbidden in (
                other_worktree / "evidence.json",
                common_dir / "artifacts" / "evidence.json",
            ):
                with self.subTest(forbidden=forbidden):
                    error = io.StringIO()
                    with (
                        patch(
                            "tools.v05_beta_release_evidence.subprocess.run",
                            side_effect=git_runner,
                        ),
                        patch(
                            "tools.v05_beta_release_evidence.GhApiClient"
                        ) as client_class,
                        redirect_stderr(error),
                    ):
                        self.assertEqual(
                            1,
                            main([*required, "--output", str(forbidden)]),
                        )
                    client_class.assert_not_called()
                    self.assertIn(
                        "output shall remain outside every Git worktree "
                        "and the Git common directory",
                        error.getvalue(),
                    )
