#!/usr/bin/env python3
"""Collect authenticated live GitHub evidence for v0.5-beta publication."""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Callable, Protocol, Sequence
from urllib.parse import parse_qsl, urlencode, urlsplit

from tools.v05_beta_release_gates import (
    ACQUISITION_SCHEMA,
    CLAIMS_NOT_MADE,
    COMMAND_IDS,
    EVIDENCE_SCHEMA,
    MERMAID_BLOCKS,
    MERMAID_RENDERER,
    MISSING_ROLES,
    OWNER_DECISION_SCHEMA,
    OWNER_DISPOSITION,
    QUALIFIED_REVIEW_STATUS,
    REENTRY_TRIGGERS,
    RELEASE,
    REPOSITORY_SCOPE,
    TAG,
)


REPOSITORY = "tdistress/ESAF"
API_ROOT = "https://api.github.com/"
WEB_ROOT = "https://github.com/tdistress/ESAF"
FRESHNESS_SECONDS = 15 * 60
CHECK_NAME = "Validate ESAF sources"
WORKFLOW_NAME = "Repository validation"
WORKFLOW_PATH = ".github/workflows/catalog-validation.yml"
PUBLICATION_ISSUE_NUMBER = 59
ISSUE_55_RESOURCE = f"repos/{REPOSITORY}/issues/55"
TAG_RESOURCE = f"repos/{REPOSITORY}/git/ref/tags/v0.5-beta"
VERDICT_SCHEMA = "esaf-v05-release-verdict-v1"
GOVERNANCE_SCHEMA = "esaf-v05-governance-verdict-v1"
POST_MERGE_SCHEMA = "esaf-v05-post-merge-results-v1"
POST_MERGE_RENDERING_SCHEMA = (
    "esaf-v05-post-merge-rendering-verdict-v1"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
HEADER_NAME_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
REQUEST_RE = re.compile(r"^> ([A-Z]+) (\S+) HTTP/\d(?:\.\d)?$")
RESPONSE_RE = re.compile(r"^< HTTP/\S+ ([0-9]{3})(?: .*)?$")
FENCED_JSON_RE = re.compile(
    r"(?ms)^```json[ \t]*\r?\n(.*?)\r?\n```[ \t]*$"
)
OWNER_KEYS = {
    "schema",
    "release",
    "sha",
    "mapping_decision_basis",
    "decision_type",
    "disposition",
    "qualified_review_status",
    "mapping_set_ids",
    "missing_qualified_roles",
    "accountable_owner",
    "scope_approval",
    "issue_55_status",
    "lifecycle",
    "claims_not_made",
    "reentry_triggers",
}
VERDICT_KEYS = {
    "schema",
    "release",
    "sha",
    "kind",
    "reviewer",
    "role",
    "date",
    "disposition",
    "critical",
    "important",
}
RENDERING_KEYS = {
    "rendered_blocks",
    "renderer",
    "visual_review",
}
GOVERNANCE_KEYS = {
    "schema",
    "release",
    "sha",
    "kind",
    "approver",
    "authority",
    "authority_attestation",
    "authority_verification",
    "authority_basis",
    "date",
    "disposition",
    "critical",
    "important",
}
POST_MERGE_RENDERING_KEYS = {
    "schema",
    "release",
    "sha",
    "tree",
    "kind",
    "reviewer",
    "role",
    "date",
    "disposition",
    "critical",
    "important",
    "rendered_blocks",
    "renderer",
    "visual_review",
}
COMMENT_REQUIRED_KEYS = {
    "url",
    "html_url",
    "issue_url",
    "id",
    "user",
    "created_at",
    "updated_at",
    "author_association",
    "body",
}


@dataclass(frozen=True)
class ApiResponse:
    requested_resource: str
    observed_request_uri: str
    redirect_count: int
    status: int
    headers: tuple[tuple[str, str], ...]
    raw_body: bytes
    retrieved_at: datetime

    def json_object(self) -> dict[str, object]:
        value = json.loads(self.raw_body)
        if not isinstance(value, dict):
            raise ValueError("GitHub API response shall be an object")
        return value


@dataclass(frozen=True)
class ApiPageSet:
    requested_resource: str
    pages: tuple[ApiResponse, ...]
    complete: bool


class ApiClient(Protocol):
    def auth_login(self) -> str:
        raise NotImplementedError

    def get(self, resource: str) -> ApiResponse:
        raise NotImplementedError

    def get_pages(self, resource: str) -> ApiPageSet:
        raise NotImplementedError


class ValidationRunner(Protocol):
    def run(
        self,
        root: Path,
        expected_head: str,
        baseline_head: str,
    ) -> list[dict[str, object]]:
        raise NotImplementedError


class LocalValidationRunner:
    """Execute the canonical candidate gates against the verified local HEAD."""

    def __init__(
        self, runner: Callable[..., object] | None = None
    ) -> None:
        self._runner = runner or subprocess.run

    def run(
        self,
        root: Path,
        expected_head: str,
        baseline_head: str,
    ) -> list[dict[str, object]]:
        if (
            SHA_RE.fullmatch(baseline_head) is None
            or baseline_head == expected_head
        ):
            raise ValueError(
                "closure baseline shall be a distinct 40-character SHA"
            )
        head = self._git_text(root, ["rev-parse", "HEAD"])
        if head != expected_head:
            raise ValueError("local Git HEAD shall equal expected closure head")
        merge_base = self._git_text(
            root,
            ["merge-base", baseline_head, expected_head],
        )
        if merge_base != baseline_head:
            raise ValueError(
                "authenticated pull request base shall be an ancestor "
                "of closure head"
            )
        python = sys.executable
        commands: dict[str, list[str]] = {
            "full_suite": [
                python, "-m", "unittest", "discover", "-s", "tests", "-v"
            ],
            "assessment": [python, "tools/validate_assessment.py", "--check"],
            "profiles": [python, "tools/validate_profiles.py", "--check"],
            "controls": [python, "tools/validate_controls.py", "--check"],
            "architectures": [python, "tools/validate_architectures.py"],
            "migration": [
                python, "tools/migrate_control_mappings.py", "--check"
            ],
            "crosswalk_current": [
                python, "tools/validate_crosswalks.py", "--check"
            ],
            "crosswalk_baseline": [
                python,
                "tools/validate_crosswalks.py",
                "--check",
                "--baseline-ref",
                baseline_head,
            ],
            "pci_readiness": [
                python,
                "tools/render_pci_dss_mapping_go_no_go.py",
                "--check",
            ],
            "links": [python, "tools/validate_links.py", "--check"],
            "release_v04": [python, "tools/release_gates.py", "--check"],
            "release_v05": [
                python,
                "tools/v05_beta_release_gates.py",
                "--check",
                "--baseline-ref",
                baseline_head,
            ],
            "mermaid_inventory": [
                python,
                "tools/mermaid_inventory.py",
                "--check-record",
                (
                    "docs/superpowers/reviews/"
                    "2026-07-27-v05-beta-mermaid-rendering.md"
                ),
            ],
            "whole_range_diff": [
                "git",
                "diff",
                "--check",
                f"{baseline_head}..{expected_head}",
            ],
        }
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        results: list[dict[str, object]] = []
        for name in COMMAND_IDS:
            if name == "mermaid_rendering":
                continue
            if name == "cache_count":
                caches = sorted(
                    path.relative_to(root).as_posix()
                    for path in root.rglob("__pycache__")
                    if path.is_dir()
                )
                if caches:
                    raise ValueError(
                        "cache_count failed: Python cache directories exist"
                    )
                result = "0 __pycache__ directories"
            elif name == "clean_status":
                status = self._git_text(
                    root,
                    ["status", "--porcelain=v1"],
                    allow_empty=True,
                )
                if status:
                    raise ValueError("clean_status failed: working tree is dirty")
                result = "clean"
            else:
                command = commands[name]
                completed = self._runner(
                    command,
                    cwd=root,
                    check=False,
                    capture_output=True,
                    env=environment,
                )
                return_code = getattr(completed, "returncode", None)
                stdout = getattr(completed, "stdout", None)
                stderr = getattr(completed, "stderr", None)
                if not isinstance(stdout, bytes) or not isinstance(stderr, bytes):
                    raise ValueError(f"{name} did not return exact byte output")
                output = stdout + stderr
                if return_code != 0:
                    raise ValueError(
                        f"{name} failed with exit code {return_code}"
                    )
                result = "passed"
            results.append(
                {
                    "name": name,
                    "sha": expected_head,
                    "exit_code": 0,
                    "result": result,
                }
            )
        return results

    def _git_text(
        self,
        root: Path,
        arguments: list[str],
        *,
        allow_empty: bool = False,
    ) -> str:
        completed = self._runner(
            ["git", *arguments],
            cwd=root,
            check=False,
            capture_output=True,
        )
        if getattr(completed, "returncode", None) != 0:
            raise ValueError(f"git {' '.join(arguments)} failed")
        stdout = getattr(completed, "stdout", None)
        if not isinstance(stdout, bytes):
            raise ValueError("Git command did not return exact byte output")
        text = stdout.decode("utf-8", errors="strict").strip()
        if not text and not allow_empty:
            raise ValueError(f"git {' '.join(arguments)} returned no result")
        return text


class DetachedValidationRunner:
    """Run candidate gates in a temporary detached closure-head worktree."""

    def __init__(
        self,
        validation_runner: ValidationRunner | None = None,
        runner: Callable[..., object] | None = None,
    ) -> None:
        self._runner = runner or subprocess.run
        self._validation_runner = (
            validation_runner or LocalValidationRunner()
        )

    def run(
        self,
        root: Path,
        expected_head: str,
        baseline_head: str,
    ) -> list[dict[str, object]]:
        root = root.resolve()
        commit = self._git_text(
            root, ["rev-parse", f"{expected_head}^{{commit}}"]
        )
        tree = self._git_text(
            root, ["rev-parse", f"{expected_head}^{{tree}}"]
        )
        merge_base = self._git_text(
            root,
            ["merge-base", baseline_head, expected_head],
        )
        if (
            commit != expected_head
            or SHA_RE.fullmatch(tree) is None
            or merge_base != baseline_head
        ):
            raise ValueError("closure snapshot could not be verified")
        with tempfile.TemporaryDirectory(
            prefix="esaf-v05-closure-"
        ) as temporary:
            snapshot = Path(temporary).resolve() / "worktree"
            added = False
            try:
                self._git_call(
                    root,
                    [
                        "worktree",
                        "add",
                        "--detach",
                        str(snapshot),
                        expected_head,
                    ],
                )
                added = True
                if (
                    self._git_text(snapshot, ["rev-parse", "HEAD"])
                    != expected_head
                    or self._git_text(
                        snapshot, ["rev-parse", "HEAD^{tree}"]
                    )
                    != tree
                ):
                    raise ValueError(
                        "detached closure snapshot is not immutable"
                    )
                results = self._validation_runner.run(
                    snapshot, expected_head, baseline_head
                )
                _validate_local_results(results, expected_head)
                return results
            finally:
                if added:
                    self._git_call(
                        root,
                        [
                            "worktree",
                            "remove",
                            "--force",
                            str(snapshot),
                        ],
                    )

    def _git_call(self, root: Path, arguments: list[str]) -> object:
        completed = self._runner(
            ["git", *arguments],
            cwd=root,
            check=False,
            capture_output=True,
        )
        if getattr(completed, "returncode", None) != 0:
            raise ValueError(f"git {' '.join(arguments)} failed")
        return completed

    def _git_text(self, root: Path, arguments: list[str]) -> str:
        completed = self._git_call(root, arguments)
        stdout = getattr(completed, "stdout", None)
        if not isinstance(stdout, bytes):
            raise ValueError("Git command did not return exact byte output")
        try:
            text = stdout.decode("utf-8", errors="strict").strip()
        except UnicodeDecodeError as exc:
            raise ValueError(
                "Git command did not return exact byte output"
            ) from exc
        if not text:
            raise ValueError(
                f"git {' '.join(arguments)} returned no result"
            )
        return text


class RecordedValidationRunner:
    """Replay one exact validation result set after fresh acquisition."""

    def __init__(
        self,
        results: list[dict[str, object]],
        expected_head: str,
        baseline_head: str,
    ) -> None:
        _validate_local_results(results, expected_head)
        self._results = deepcopy(results)
        self._expected_head = expected_head
        self._baseline_head = baseline_head

    def run(
        self,
        root: Path,
        expected_head: str,
        baseline_head: str,
    ) -> list[dict[str, object]]:
        if (
            expected_head != self._expected_head
            or baseline_head != self._baseline_head
        ):
            raise ValueError(
                "fresh acquisition shall preserve the validated head and base"
            )
        return deepcopy(self._results)


class GhApiClient:
    """Authenticated GitHub CLI adapter with a fail-closed transport parser."""

    def __init__(
        self,
        runner: Callable[..., object] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._runner = runner or subprocess.run
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._auth_response: ApiResponse | None = None

    def auth_login(self) -> str:
        response = self._get_included_response("user")
        self._auth_response = response
        login = response.json_object().get("login")
        if not _nonblank(login):
            raise ValueError("authenticated GitHub login is required")
        return str(login)

    def get(self, resource: str) -> ApiResponse:
        if resource == "user" and self._auth_response is not None:
            response = self._auth_response
            self._auth_response = None
            return response
        return self._get_included_response(resource)

    def get_pages(self, resource: str) -> ApiPageSet:
        return self._get_all_pages(resource)

    def _get_included_response(self, resource: str) -> ApiResponse:
        environment = os.environ.copy()
        environment["GH_DEBUG"] = "api"
        environment.pop("GH_HOST", None)
        completed = self._runner(
            ["gh", "api", "--hostname", "github.com", resource],
            check=False,
            capture_output=True,
            env=environment,
        )
        stdout = getattr(completed, "stdout", None)
        stderr = getattr(completed, "stderr", None)
        return_code = getattr(completed, "returncode", None)
        if not isinstance(stdout, bytes) or not isinstance(stderr, bytes):
            raise ValueError("GitHub CLI shall return byte streams")
        response = _parse_debug_response(
            resource,
            stdout,
            stderr,
            self._clock(),
        )
        if return_code != 0 and not (
            resource == TAG_RESOURCE and response.status == 404
        ):
            raise ValueError("authenticated GitHub API request failed")
        return response

    def _get_all_pages(self, resource: str) -> ApiPageSet:
        pages: list[ApiResponse] = []
        next_resource = _page_resource(resource, 1)
        expected_page = 1
        while True:
            if expected_page > 100:
                raise ValueError("GitHub pagination is incomplete")
            response = self._get_included_response(next_resource)
            pages.append(response)
            next_link = _next_link(response.headers)
            if next_link is None:
                return ApiPageSet(resource, tuple(pages), True)
            parsed = urlsplit(next_link)
            if parsed.scheme != "https" or parsed.netloc != "api.github.com":
                raise ValueError("GitHub pagination is incomplete")
            next_resource = parsed.path.lstrip("/")
            if parsed.query:
                next_resource += f"?{parsed.query}"
            expected_page += 1
            if not _resource_is_page(
                next_resource, resource, expected_page
            ):
                raise ValueError("GitHub pagination is incomplete")


def _parse_debug_response(
    resource: str,
    raw_body: bytes,
    debug_trace: bytes,
    retrieved_at: datetime,
) -> ApiResponse:
    try:
        lines = debug_trace.decode("utf-8", errors="strict").splitlines()
    except UnicodeDecodeError as exc:
        raise ValueError("GitHub debug transport is malformed") from exc
    requests = [
        (index, match)
        for index, line in enumerate(lines)
        if (match := REQUEST_RE.fullmatch(line)) is not None
    ]
    responses = [
        (index, match)
        for index, line in enumerate(lines)
        if (match := RESPONSE_RE.fullmatch(line)) is not None
    ]
    if not requests:
        raise ValueError("missing request boundary")
    if len(requests) != 1 or len(responses) != 1:
        raise ValueError("multiple transport boundaries")
    request_index, request_match = requests[0]
    response_index, response_match = responses[0]
    if request_index >= response_index or request_match.group(1) != "GET":
        raise ValueError("GitHub debug transport is malformed")
    observed_target = request_match.group(2)
    parsed_target = urlsplit(observed_target)
    if parsed_target.scheme or parsed_target.netloc:
        if (
            parsed_target.scheme != "https"
            or parsed_target.netloc != "api.github.com"
        ):
            raise ValueError("GitHub API host changed")
        observed_uri = parsed_target.path
        if parsed_target.query:
            observed_uri += f"?{parsed_target.query}"
    else:
        observed_uri = observed_target
    request_hosts: list[str] = []
    for line in lines[request_index + 1 : response_index]:
        if not line.startswith("> "):
            continue
        header = line[2:]
        if ":" not in header:
            raise ValueError("GitHub debug transport is malformed")
        name, value = header.split(":", 1)
        if name.casefold() == "host":
            request_hosts.append(value.strip().casefold())
    if request_hosts != ["api.github.com"]:
        raise ValueError("GitHub API host changed")
    if observed_uri != f"/{resource}":
        raise ValueError("GitHub request URI changed")
    status = int(response_match.group(1))
    headers: list[tuple[str, str]] = []
    for line in lines[response_index + 1 :]:
        if not line.startswith("< "):
            break
        header = line[2:]
        if ":" not in header:
            raise ValueError("GitHub response header is malformed")
        name, value = header.split(":", 1)
        value = value.strip()
        if (
            HEADER_NAME_RE.fullmatch(name) is None
            or "\r" in value
            or "\n" in value
        ):
            raise ValueError("GitHub response header is malformed")
        headers.append((name.casefold(), value))
    redirect_count = int(
        300 <= status < 400
        or any(name == "location" for name, _ in headers)
    )
    if redirect_count:
        raise ValueError("GitHub API redirects are forbidden")
    if status != 200 and not (resource == TAG_RESOURCE and status == 404):
        raise ValueError("GitHub API response status shall equal 200")
    return ApiResponse(
        requested_resource=resource,
        observed_request_uri=observed_uri,
        redirect_count=redirect_count,
        status=status,
        headers=tuple(headers),
        raw_body=raw_body,
        retrieved_at=_utc(retrieved_at, "GitHub retrieval timestamp"),
    )


def _page_resource(resource: str, page: int) -> str:
    parsed = urlsplit(resource)
    query = [
        (key, value)
        for key, value in parse_qsl(
            parsed.query, keep_blank_values=True
        )
        if key not in {"per_page", "page"}
    ]
    query.extend((("per_page", "100"), ("page", str(page))))
    encoded = urlencode(query)
    return f"{parsed.path}?{encoded}"


def _resource_is_page(
    candidate: str, base_resource: str, page: int
) -> bool:
    candidate_url = urlsplit(candidate)
    base_url = urlsplit(base_resource)
    if candidate_url.path != base_url.path:
        return False
    candidate_query = parse_qsl(
        candidate_url.query, keep_blank_values=True
    )
    if len(candidate_query) != len({key for key, _ in candidate_query}):
        return False
    values = dict(candidate_query)
    base_values = dict(
        parse_qsl(base_url.query, keep_blank_values=True)
    )
    expected = {
        **{
            key: value
            for key, value in base_values.items()
            if key not in {"per_page", "page"}
        },
        "per_page": "100",
        "page": str(page),
    }
    return values == expected


def _api_link_resource(value: str) -> str | None:
    parsed = urlsplit(value)
    if parsed.scheme != "https" or parsed.netloc != "api.github.com":
        return None
    resource = parsed.path.lstrip("/")
    if parsed.query:
        resource += f"?{parsed.query}"
    return resource


def _next_link(headers: tuple[tuple[str, str], ...]) -> str | None:
    link_values = [value for name, value in headers if name.casefold() == "link"]
    if len(link_values) > 1:
        raise ValueError("GitHub pagination is incomplete")
    if not link_values:
        return None
    next_links: list[str] = []
    for part in link_values[0].split(","):
        match = re.fullmatch(r'\s*<([^>]+)>;\s*rel="([^"]+)"\s*', part)
        if match is None:
            raise ValueError("GitHub pagination is incomplete")
        if "next" in match.group(2).split():
            next_links.append(match.group(1))
    if len(next_links) > 1:
        raise ValueError("GitHub pagination is incomplete")
    return next_links[0] if next_links else None


def parse_fenced_json(body: str) -> dict[str, object]:
    """Parse exactly one fenced JSON object from a GitHub comment body."""
    matches = FENCED_JSON_RE.findall(body)
    if len(matches) != 1:
        raise ValueError("comment shall contain exactly one fenced JSON object")
    try:
        value = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise ValueError(
            "comment shall contain exactly one fenced JSON object"
        ) from exc
    if not isinstance(value, dict):
        raise ValueError("comment shall contain exactly one fenced JSON object")
    return value


def source_record(
    response: ApiResponse,
    payload: dict[str, object],
    *,
    expected_container_type: str,
    expected_container_number: int,
    verified_at: datetime,
) -> dict[str, object]:
    """Derive one immutable comment-source record from exact response bytes."""
    if (
        expected_container_type not in {"pull", "issue"}
        or not _integer(expected_container_number)
        or expected_container_number < 1
    ):
        raise ValueError("expected GitHub comment container is invalid")
    if not COMMENT_REQUIRED_KEYS.issubset(payload):
        raise ValueError("GitHub comment response is incomplete")
    comment_id = payload.get("id")
    user = payload.get("user")
    if (
        not _integer(comment_id)
        or not isinstance(user, dict)
        or not _nonblank(user.get("login"))
        or not _integer(user.get("id"))
        or not _nonblank(payload.get("author_association"))
        or not isinstance(payload.get("body"), str)
    ):
        raise ValueError("GitHub comment response is incomplete")
    resource = f"repos/{REPOSITORY}/issues/comments/{comment_id}"
    expected_api_url = f"{API_ROOT}{resource}"
    html_container = (
        "pull" if expected_container_type == "pull" else "issues"
    )
    expected_html_url = (
        f"{WEB_ROOT}/{html_container}/{expected_container_number}"
        f"#issuecomment-{comment_id}"
    )
    expected_issue_url = (
        f"{API_ROOT}repos/{REPOSITORY}/issues/"
        f"{expected_container_number}"
    )
    if (
        payload.get("url") != expected_api_url
        or payload.get("html_url") != expected_html_url
        or payload.get("issue_url") != expected_issue_url
        or response.requested_resource != resource
    ):
        raise ValueError("GitHub comment canonical URL mismatch")
    created = _parse_rfc3339(payload.get("created_at"), "GitHub comment timestamp")
    updated = _parse_rfc3339(payload.get("updated_at"), "GitHub comment timestamp")
    if created != updated:
        raise ValueError("GitHub comment shall be unedited")
    return {
        "repository": REPOSITORY,
        "resource_path": resource,
        "comment_url": expected_html_url,
        "comment_id": comment_id,
        "author_login": user["login"],
        "author_user_id": user["id"],
        "author_association": payload["author_association"],
        "created_at": _format_utc(created),
        "updated_at": _format_utc(updated),
        "body_sha256": sha256(payload["body"].encode("utf-8")).hexdigest(),
        "response_sha256": sha256(response.raw_body).hexdigest(),
        "acquisition_resource_id": resource,
        "source_verified_at": _format_utc(
            _utc(verified_at, "source verification timestamp")
        ),
    }


def _canonical_pr_side(
    value: object,
    *,
    expected_sha: str | None,
    expected_ref: str | None,
) -> bool:
    if not isinstance(value, dict):
        return False
    sha = value.get("sha")
    ref = value.get("ref")
    repo = value.get("repo")
    if (
        not isinstance(sha, str)
        or SHA_RE.fullmatch(sha) is None
        or (expected_sha is not None and sha != expected_sha)
        or not _nonblank(ref)
        or (expected_ref is not None and ref != expected_ref)
        or value.get("label") != f"tdistress:{ref}"
        or not isinstance(repo, dict)
    ):
        return False
    owner = repo.get("owner")
    return (
        repo.get("full_name") == REPOSITORY
        and repo.get("url") == f"{API_ROOT}repos/{REPOSITORY}"
        and repo.get("html_url") == WEB_ROOT
        and isinstance(owner, dict)
        and owner.get("login") == "tdistress"
    )


def collect_closure_evidence(
    client: ApiClient,
    *,
    root: Path,
    pr_number: int,
    expected_head: str,
    owner_comment_id: int,
    technical_comment_id: int,
    editorial_comment_id: int,
    terminology_comment_id: int,
    rendering_comment_id: int,
    profile_scope_comment_id: int,
    governance_comment_id: int,
    security_overclaiming_comment_id: int,
    whole_range_comment_id: int,
    now: datetime | None = None,
    validation_runner: ValidationRunner | None = None,
    repository_runner: Callable[..., object] | None = None,
    merged_head: str | None = None,
    expected_closure_base: str | None = None,
) -> dict[str, object]:
    """Validate once, then reacquire authenticated evidence for freshness."""
    arguments = {
        "root": root,
        "pr_number": pr_number,
        "expected_head": expected_head,
        "owner_comment_id": owner_comment_id,
        "technical_comment_id": technical_comment_id,
        "editorial_comment_id": editorial_comment_id,
        "terminology_comment_id": terminology_comment_id,
        "rendering_comment_id": rendering_comment_id,
        "profile_scope_comment_id": profile_scope_comment_id,
        "governance_comment_id": governance_comment_id,
        "security_overclaiming_comment_id": security_overclaiming_comment_id,
        "whole_range_comment_id": whole_range_comment_id,
        "now": now,
        "repository_runner": repository_runner,
        "merged_head": merged_head,
        "expected_closure_base": expected_closure_base,
    }
    initial = _collect_closure_evidence_once(
        client,
        validation_runner=validation_runner,
        **arguments,
    )
    closure_base = initial.get("closure_base")
    commands = initial.get("candidate_commands")
    if (
        not isinstance(closure_base, str)
        or not isinstance(commands, list)
    ):
        raise ValueError("initial closure evidence is incomplete")
    recorded = [
        deepcopy(command)
        for command in commands
        if isinstance(command, dict)
        and command.get("name") != "mermaid_rendering"
    ]
    replay = RecordedValidationRunner(
        recorded,
        expected_head,
        closure_base,
    )
    return _collect_closure_evidence_once(
        client,
        validation_runner=replay,
        **arguments,
    )


def _collect_closure_evidence_once(
    client: ApiClient,
    *,
    root: Path,
    pr_number: int,
    expected_head: str,
    owner_comment_id: int,
    technical_comment_id: int,
    editorial_comment_id: int,
    terminology_comment_id: int,
    rendering_comment_id: int,
    profile_scope_comment_id: int,
    governance_comment_id: int,
    security_overclaiming_comment_id: int,
    whole_range_comment_id: int,
    now: datetime | None = None,
    validation_runner: ValidationRunner | None = None,
    repository_runner: Callable[..., object] | None = None,
    merged_head: str | None = None,
    expected_closure_base: str | None = None,
) -> dict[str, object]:
    """Collect closure evidence from authenticated, exact GitHub resources."""
    fixed_now = (
        _utc(now, "source verification timestamp")
        if now is not None
        else None
    )
    if SHA_RE.fullmatch(expected_head) is None:
        raise ValueError("expected closure head shall be a 40-character SHA")
    if not _integer(pr_number) or pr_number < 1:
        raise ValueError("pull request number shall be positive")
    _require_local_tag_absent(
        root, repository_runner or subprocess.run
    )

    login = client.auth_login()
    if not _nonblank(login):
        raise ValueError("authenticated GitHub login is required")
    responses: list[tuple[ApiResponse, str]] = []

    user_response = client.get("user")
    user = _validated_object(
        user_response, _reference_now(fixed_now)
    )
    if user.get("login") != login:
        raise ValueError("authenticated GitHub login does not match /user")
    user_url = user.get("html_url")
    if user_url != f"https://github.com/{login}":
        raise ValueError("authenticated GitHub user canonical URL mismatch")
    responses.append((user_response, str(user_url)))

    commit_resource = f"repos/{REPOSITORY}/commits/{expected_head}"
    commit_response = client.get(commit_resource)
    commit = _validated_object(
        commit_response, _reference_now(fixed_now)
    )
    if commit.get("sha") != expected_head:
        raise ValueError("GitHub closure commit shall equal expected head")
    commit_details = commit.get("commit")
    tree = (
        commit_details.get("tree")
        if isinstance(commit_details, dict)
        else None
    )
    parents = commit.get("parents")
    if (
        not isinstance(tree, dict)
        or SHA_RE.fullmatch(str(tree.get("sha"))) is None
        or not isinstance(commit_details, dict)
        or not isinstance(commit_details.get("committer"), dict)
    ):
        raise ValueError("GitHub closure commit response is incomplete")
    commit_time = _parse_rfc3339(
        commit_details["committer"].get("date"),
        "GitHub closure commit timestamp",
    )
    commit_url = f"{WEB_ROOT}/commit/{expected_head}"
    if commit.get("html_url") != commit_url:
        raise ValueError("GitHub closure commit canonical URL mismatch")
    if not isinstance(parents, list) or not parents:
        raise ValueError(
            "GitHub closure commit parents are invalid"
        )
    for parent in parents:
        if not isinstance(parent, dict):
            raise ValueError(
                "GitHub closure commit parents are invalid"
            )
        parent_sha = parent.get("sha")
        if (
            not isinstance(parent_sha, str)
            or SHA_RE.fullmatch(parent_sha) is None
            or parent_sha == expected_head
            or parent.get("url")
            != f"{API_ROOT}repos/{REPOSITORY}/commits/{parent_sha}"
        ):
            raise ValueError(
                "GitHub closure commit parents are invalid"
            )
    responses.append((commit_response, commit_url))

    pr_resource = f"repos/{REPOSITORY}/pulls/{pr_number}"
    pr_response = client.get(pr_resource)
    pull_request = _validated_object(
        pr_response, _reference_now(fixed_now)
    )
    head = pull_request.get("head")
    base = pull_request.get("base")
    pr_url = f"{WEB_ROOT}/pull/{pr_number}"
    if (
        pull_request.get("number") != pr_number
        or pull_request.get("url") != f"{API_ROOT}{pr_resource}"
        or pull_request.get("html_url") != pr_url
        or not _canonical_pr_side(
            head,
            expected_sha=expected_head,
            expected_ref=None,
        )
    ):
        raise ValueError("GitHub pull request does not match closure head")
    if not _canonical_pr_side(
        base,
        expected_sha=None,
        expected_ref="main",
    ):
        raise ValueError("GitHub pull request base is invalid")
    assert isinstance(base, dict)
    closure_base = str(base["sha"])
    if closure_base == expected_head:
        raise ValueError("GitHub pull request base is invalid")
    if (
        expected_closure_base is not None
        and closure_base != expected_closure_base
    ):
        raise ValueError(
            "authenticated pull request base changed during refresh"
        )
    if merged_head is None:
        if (
            pull_request.get("state") != "open"
            or pull_request.get("mergeable") is not True
            or pull_request.get("mergeable_state") != "clean"
        ):
            raise ValueError(
                "GitHub pull request merge state shall be clean"
            )
    elif (
        pull_request.get("state") != "closed"
        or pull_request.get("merged") is not True
        or pull_request.get("merge_commit_sha") != merged_head
    ):
        raise ValueError(
            "pull request shall be merged to exact merge head"
        )
    responses.append((pr_response, pr_url))

    tag_response = client.get(TAG_RESOURCE)
    _validate_tag_absence(
        tag_response, _reference_now(fixed_now)
    )
    tag_digest = sha256(tag_response.raw_body).hexdigest()
    responses.append((tag_response, f"{API_ROOT}{TAG_RESOURCE}"))

    issue_55_response = client.get(ISSUE_55_RESOURCE)
    issue_55 = _validated_object(
        issue_55_response, _reference_now(fixed_now)
    )
    issue_55_url = f"{WEB_ROOT}/issues/55"
    if (
        issue_55.get("url") != f"{API_ROOT}{ISSUE_55_RESOURCE}"
        or issue_55.get("html_url") != issue_55_url
        or issue_55.get("repository_url")
        != f"{API_ROOT}repos/{REPOSITORY}"
        or issue_55.get("number") != 55
        or issue_55.get("state") != "open"
        or "pull_request" in issue_55
    ):
        raise ValueError(
            "issue 55 shall be the canonical open repository issue"
        )
    issue_55_digest = sha256(
        issue_55_response.raw_body
    ).hexdigest()
    responses.append((issue_55_response, issue_55_url))

    requested_comments = {
        "owner": owner_comment_id,
        "technical": technical_comment_id,
        "editorial": editorial_comment_id,
        "terminology": terminology_comment_id,
        "rendering": rendering_comment_id,
        "profile_scope": profile_scope_comment_id,
        "governance": governance_comment_id,
        "security_overclaiming": security_overclaiming_comment_id,
        "whole_range": whole_range_comment_id,
    }
    if (
        any(not _integer(value) or value < 1 for value in requested_comments.values())
        or len(set(requested_comments.values())) != len(requested_comments)
    ):
        raise ValueError("GitHub comment identifiers shall be distinct positive integers")
    comments: dict[
        str, tuple[dict[str, object], dict[str, object], dict[str, object]]
    ] = {}
    for name, comment_id in requested_comments.items():
        resource = f"repos/{REPOSITORY}/issues/comments/{comment_id}"
        response = client.get(resource)
        response_reference = _reference_now(fixed_now)
        payload = _validated_object(response, response_reference)
        source = source_record(
            response,
            payload,
            expected_container_type="pull",
            expected_container_number=pr_number,
            verified_at=response.retrieved_at,
        )
        if _parse_rfc3339(source["created_at"], "GitHub comment timestamp") <= commit_time:
            raise ValueError("GitHub comment shall postdate closure commit")
        structured = parse_fenced_json(str(payload["body"]))
        comments[name] = (structured, source, payload)
        responses.append((response, str(source["comment_url"])))

    mapping_ids = _tracked_mapping_set_ids(root)
    owner, owner_source, _ = comments["owner"]
    _validate_owner_comment(
        owner,
        owner_source,
        expected_head,
        mapping_ids,
    )
    mapping_ids = list(owner["mapping_set_ids"])
    verdicts: dict[str, dict[str, object]] = {}
    for kind in (
        "technical",
        "editorial",
        "terminology",
        "rendering",
        "profile_scope",
        "security_overclaiming",
        "whole_range",
    ):
        structured, source, _ = comments[kind]
        _validate_release_verdict(
            structured,
            source,
            kind,
            expected_head,
        )
        verdicts[kind] = _release_verdict(structured, source)
    governance, governance_source, _ = comments["governance"]
    _validate_governance_verdict(
        governance,
        governance_source,
        expected_head,
    )

    checks_resource = f"repos/{REPOSITORY}/commits/{expected_head}/check-runs"
    page_set = client.get_pages(checks_resource)
    check_run, page_entry = _validated_check_runs(
        page_set, expected_head, _reference_now(fixed_now)
    )
    run_id = check_run["run_id"]
    run_resource = f"repos/{REPOSITORY}/actions/runs/{run_id}"
    run_response = client.get(run_resource)
    workflow_run = _validated_object(
        run_response, _reference_now(fixed_now)
    )
    run_url = f"{WEB_ROOT}/actions/runs/{run_id}"
    repository = workflow_run.get("repository")
    head_repository = workflow_run.get("head_repository")
    if (
        workflow_run.get("id") != run_id
        or workflow_run.get("name") != WORKFLOW_NAME
        or workflow_run.get("path") != WORKFLOW_PATH
        or workflow_run.get("head_sha") != expected_head
        or workflow_run.get("status") != "completed"
        or workflow_run.get("conclusion") != "success"
        or workflow_run.get("html_url") != run_url
        or not isinstance(repository, dict)
        or repository.get("full_name") != REPOSITORY
        or not isinstance(head_repository, dict)
        or head_repository.get("full_name") != REPOSITORY
    ):
        raise ValueError(
            "check shall bind the canonical GitHub Actions workflow run"
        )
    responses.append((run_response, run_url))

    rendering = comments["rendering"][0]
    executed_results = (
        validation_runner or LocalValidationRunner()
    ).run(root, expected_head, closure_base)
    _validate_local_results(executed_results, expected_head)
    result_by_name = {
        str(item["name"]): deepcopy(item) for item in executed_results
    }
    result_by_name["mermaid_rendering"] = {
        "name": "mermaid_rendering",
        "sha": expected_head,
        "exit_code": 0,
        "result": {
            "rendered_blocks": rendering["rendered_blocks"],
            "renderer": rendering["renderer"],
            "visual_review": rendering["visual_review"],
            "candidate_inventory_equal": True,
            "candidate_review_url": verdicts["rendering"]["url"],
            "candidate_reviewer": verdicts["rendering"]["reviewer"],
            "reviewed_at": comments["rendering"][1]["created_at"],
        },
    }
    candidate_commands = [
        result_by_name[name] for name in COMMAND_IDS
    ]

    scope_approval = owner["scope_approval"]
    assert isinstance(scope_approval, dict)
    scope = {
        "sha": expected_head,
        "reviewer": owner["accountable_owner"],
        "role": "repository owner",
        "date": str(owner_source["created_at"])[:10],
        "disposition": scope_approval["disposition"],
        "url": owner_source["comment_url"],
        "critical": 0,
        "important": 0,
        "source": deepcopy(owner_source),
        "scope": scope_approval["scope"],
        "milestone": scope_approval["milestone"],
    }
    mapping_decisions = [
        {
            "mapping_set_id": mapping_id,
            "mapping_decision_basis": owner["mapping_decision_basis"],
            "decision_type": owner["decision_type"],
            "sha": owner["sha"],
            "disposition": owner["disposition"],
            "qualified_review_status": owner["qualified_review_status"],
            "missing_qualified_roles": deepcopy(owner["missing_qualified_roles"]),
            "accountable_owner": owner["accountable_owner"],
            "issue_55_status": owner["issue_55_status"],
            "lifecycle": owner["lifecycle"],
            "claims_not_made": deepcopy(owner["claims_not_made"]),
            "reentry_triggers": deepcopy(owner["reentry_triggers"]),
            "url": owner_source["comment_url"],
            "source": deepcopy(owner_source),
        }
        for mapping_id in mapping_ids
    ]

    governance_verdict = {
        "sha": expected_head,
        "reviewer": governance["approver"],
        "role": "Steering Committee approver",
        "date": governance["date"],
        "disposition": governance["disposition"],
        "url": governance_source["comment_url"],
        "critical": governance["critical"],
        "important": governance["important"],
        "source": deepcopy(governance_source),
        "authority": governance["authority"],
        "authority_attestation": governance["authority_attestation"],
        "authority_verification": governance["authority_verification"],
        "authority_basis": governance["authority_basis"],
    }
    resource_entries = [
        _acquisition_entry(response, canonical_url)
        for response, canonical_url in responses
    ]
    resource_entries.append(page_entry)
    retrieved_at = max(
        [
            response.retrieved_at
            for response, _ in responses
        ]
        + [page.retrieved_at for page in page_set.pages]
    )
    return {
        "schema": EVIDENCE_SCHEMA,
        "release": RELEASE,
        "closure_base": closure_base,
        "closure_head": expected_head,
        "closure_tree": tree["sha"],
        "scope": scope,
        "technical": verdicts["technical"],
        "editorial": verdicts["editorial"],
        "terminology": verdicts["terminology"],
        "rendering": verdicts["rendering"],
        "profile_scope": verdicts["profile_scope"],
        "security_overclaiming": verdicts["security_overclaiming"],
        "whole_range": verdicts["whole_range"],
        "governance": governance_verdict,
        "candidate_commands": candidate_commands,
        "mapping_decision_schema": OWNER_DECISION_SCHEMA,
        "mapping_decision_basis": "owner_risk_acceptance",
        "mapping_decisions": mapping_decisions,
        "github_checks": {
            "expected": [CHECK_NAME],
            "observed": [
                {
                    "name": CHECK_NAME,
                    "sha": expected_head,
                    "conclusion": "success",
                    "url": run_url,
                    "app_slug": "github-actions",
                    "run_id": run_id,
                    "workflow_name": WORKFLOW_NAME,
                    "workflow_path": WORKFLOW_PATH,
                    "repository": REPOSITORY,
                }
            ],
        },
        "issue_55": {
            "resource": ISSUE_55_RESOURCE,
            "number": 55,
            "state": "open",
            "url": issue_55_url,
            "response_sha256": issue_55_digest,
        },
        "merge_state": {
            "sha": expected_head,
            "mergeable": True,
            "state": "clean",
        },
        "tag_state": {
            "resource": TAG_RESOURCE,
            "exists": False,
            "status": 404,
            "response_sha256": tag_digest,
        },
        "acquisition": {
            "schema": ACQUISITION_SCHEMA,
            "repository": REPOSITORY,
            "authenticated_login": login,
            "retrieved_at": _format_utc(retrieved_at),
            "complete": True,
            "resources": resource_entries,
        },
    }


def refresh_taggable_evidence(
    client: ApiClient,
    *,
    base_evidence: dict[str, object],
    merge_head: str,
    post_merge_rendering_comment_id: int,
    post_merge_validation_runner: ValidationRunner | None = None,
    **collection_arguments: object,
) -> dict[str, object]:
    """Re-fetch closure sources and bind post-merge evidence to an equal tree."""
    expected_head = collection_arguments.get("expected_head")
    if (
        not isinstance(expected_head, str)
        or base_evidence.get("closure_head") != expected_head
    ):
        raise ValueError("base evidence shall match expected closure head")
    closure_base = base_evidence.get("closure_base")
    if (
        not isinstance(closure_base, str)
        or SHA_RE.fullmatch(closure_base) is None
        or closure_base == expected_head
    ):
        raise ValueError(
            "base evidence closure base shall be a distinct "
            "40-character SHA"
        )
    base_commands = _validated_candidate_commands(
        base_evidence.get("candidate_commands"), expected_head
    )
    refresh_arguments = dict(collection_arguments)
    if refresh_arguments.get("validation_runner") is None:
        refresh_arguments["validation_runner"] = DetachedValidationRunner()
    refresh_arguments["merged_head"] = merge_head
    refresh_arguments["expected_closure_base"] = closure_base
    fresh = collect_closure_evidence(client, **refresh_arguments)
    if fresh.get("closure_base") != closure_base:
        raise ValueError(
            "authenticated pull request base changed during refresh"
        )
    _require_unchanged_sources(base_evidence, fresh)
    fresh_commands = _validated_candidate_commands(
        fresh.get("candidate_commands"), expected_head
    )
    nonvisual_names = [
        name for name in COMMAND_IDS if name != "mermaid_rendering"
    ]
    base_by_name = {
        str(item["name"]): item for item in base_commands
    }
    fresh_by_name = {
        str(item["name"]): item for item in fresh_commands
    }
    if [
        base_by_name[name] for name in nonvisual_names
    ] != [
        fresh_by_name[name] for name in nonvisual_names
    ]:
        raise ValueError(
            "base candidate commands shall equal fresh execution"
        )
    fresh["candidate_commands"] = fresh_commands
    fresh["merge_state"] = deepcopy(base_evidence.get("merge_state"))
    if SHA_RE.fullmatch(merge_head) is None or merge_head == fresh["closure_head"]:
        raise ValueError("merge head shall be a distinct 40-character SHA")
    now = collection_arguments.get("now")
    fixed_now = (
        _utc(now, "source verification timestamp")
        if isinstance(now, datetime)
        else None
    )
    merge_resource = f"repos/{REPOSITORY}/commits/{merge_head}"
    merge_response = client.get(merge_resource)
    merge_commit = _validated_object(
        merge_response, _reference_now(fixed_now)
    )
    merge_details = merge_commit.get("commit")
    merge_tree = (
        merge_details.get("tree")
        if isinstance(merge_details, dict)
        else None
    )
    merge_url = f"{WEB_ROOT}/commit/{merge_head}"
    if (
        merge_commit.get("sha") != merge_head
        or merge_commit.get("html_url") != merge_url
        or not isinstance(merge_tree, dict)
        or merge_tree.get("sha") != fresh["closure_tree"]
    ):
        raise ValueError("merged tree shall equal closure tree")

    post_resource = (
        f"repos/{REPOSITORY}/issues/comments/"
        f"{post_merge_rendering_comment_id}"
    )
    post_response = client.get(post_resource)
    post_payload = _validated_object(
        post_response, _reference_now(fixed_now)
    )
    post_source = source_record(
        post_response,
        post_payload,
        expected_container_type="issue",
        expected_container_number=PUBLICATION_ISSUE_NUMBER,
        verified_at=post_response.retrieved_at,
    )
    merge_commit_time = _parse_rfc3339(
        merge_details["committer"].get("date"),
        "GitHub merge commit timestamp",
    )
    if (
        _parse_rfc3339(
            post_source["created_at"],
            "GitHub comment timestamp",
        )
        <= merge_commit_time
    ):
        raise ValueError(
            "post-merge rendering comment shall postdate merge commit"
        )
    merge_results = (
        post_merge_validation_runner or DetachedValidationRunner()
    ).run(
        Path(collection_arguments["root"]),
        merge_head,
        closure_base,
    )
    _validate_local_results(merge_results, merge_head)
    candidate_results = [
        deepcopy(command)
        for command in fresh_commands
        if command.get("name") != "mermaid_rendering"
    ]
    reacquire_arguments = dict(collection_arguments)
    reacquire_arguments.pop("validation_runner", None)
    reacquired = _collect_closure_evidence_once(
        client,
        validation_runner=RecordedValidationRunner(
            candidate_results,
            expected_head,
            closure_base,
        ),
        merged_head=merge_head,
        expected_closure_base=closure_base,
        **reacquire_arguments,
    )
    _require_unchanged_sources(fresh, reacquired)
    fresh = reacquired
    fresh_commands = _validated_candidate_commands(
        fresh.get("candidate_commands"), expected_head
    )
    merge_response = client.get(merge_resource)
    merge_commit = _validated_object(
        merge_response, _reference_now(fixed_now)
    )
    merge_details = merge_commit.get("commit")
    merge_tree = (
        merge_details.get("tree")
        if isinstance(merge_details, dict)
        else None
    )
    if (
        merge_commit.get("sha") != merge_head
        or merge_commit.get("html_url") != merge_url
        or not isinstance(merge_tree, dict)
        or merge_tree.get("sha") != fresh["closure_tree"]
    ):
        raise ValueError("merged tree shall equal closure tree")
    post_response = client.get(post_resource)
    post_payload = _validated_object(
        post_response, _reference_now(fixed_now)
    )
    post_source = source_record(
        post_response,
        post_payload,
        expected_container_type="issue",
        expected_container_number=PUBLICATION_ISSUE_NUMBER,
        verified_at=post_response.retrieved_at,
    )
    merge_commit_time = _parse_rfc3339(
        merge_details["committer"].get("date"),
        "GitHub merge commit timestamp",
    )
    if (
        _parse_rfc3339(
            post_source["created_at"],
            "GitHub comment timestamp",
        )
        <= merge_commit_time
    ):
        raise ValueError(
            "post-merge rendering comment shall postdate merge commit"
        )
    post_rendering = parse_fenced_json(str(post_payload["body"]))
    _validate_post_merge_rendering_verdict(
        post_rendering,
        post_source,
        merge_head,
        str(merge_tree["sha"]),
    )

    merge_by_name = {
        str(item["name"]): deepcopy(item) for item in merge_results
    }
    candidate_rendering = fresh["rendering"]
    assert isinstance(candidate_rendering, dict)
    merge_by_name["mermaid_rendering"] = {
        "name": "mermaid_rendering",
        "sha": merge_head,
        "exit_code": 0,
        "result": {
            "rendered_blocks": post_rendering["rendered_blocks"],
            "renderer": post_rendering["renderer"],
            "visual_review": post_rendering["visual_review"],
            "candidate_inventory_equal": True,
            "merge_tree_equal": True,
            "candidate_review_url": candidate_rendering["url"],
            "candidate_reviewer": candidate_rendering["reviewer"],
            "post_merge_reviewer": post_rendering["reviewer"],
            "post_merge_review_url": post_source["comment_url"],
            "reviewed_at": post_source["created_at"],
        },
    }
    post_commands = []
    for name in COMMAND_IDS:
        command = deepcopy(merge_by_name[name])
        command.pop("sha")
        post_commands.append(command)
    result = deepcopy(fresh)
    result["merge_head"] = merge_head
    result["merge_tree"] = merge_tree["sha"]
    result["post_merge"] = {
        "schema": POST_MERGE_SCHEMA,
        "sha": merge_head,
        "tree": merge_tree["sha"],
        "commands": post_commands,
        "rendering_source": post_source,
    }
    result["acquisition"]["resources"].append(
        _acquisition_entry(merge_response, merge_url)
    )
    result["acquisition"]["resources"].append(
        _acquisition_entry(
            post_response, str(post_source["comment_url"])
        )
    )
    result["acquisition"]["retrieved_at"] = _format_utc(
        max(
            _parse_rfc3339(
                result["acquisition"]["retrieved_at"],
                "acquisition timestamp",
            ),
            merge_response.retrieved_at,
            post_response.retrieved_at,
        )
    )
    return result


def _validated_object(
    response: ApiResponse, now: datetime
) -> dict[str, object]:
    _validate_response(response, now)
    try:
        return response.json_object()
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("GitHub API response body is invalid") from exc


def _require_local_tag_absent(
    root: Path, runner: Callable[..., object]
) -> None:
    command = [
        "git",
        "show-ref",
        "--verify",
        "--quiet",
        f"refs/tags/{TAG}",
    ]
    completed = runner(
        command,
        cwd=root,
        check=False,
        capture_output=True,
    )
    return_code = getattr(completed, "returncode", None)
    if return_code == 0:
        raise ValueError("local v0.5-beta tag already exists")
    if return_code != 1:
        raise ValueError("local v0.5-beta tag state could not be verified")


def _validate_response(response: ApiResponse, now: datetime) -> None:
    if response.observed_request_uri != f"/{response.requested_resource}":
        raise ValueError("GitHub request URI changed")
    if response.redirect_count != 0:
        raise ValueError("GitHub API redirects are forbidden")
    if response.status != 200:
        raise ValueError("GitHub API response status shall equal 200")
    if not isinstance(response.raw_body, bytes):
        raise ValueError("GitHub API response body shall be exact bytes")
    for item in response.headers:
        if (
            not isinstance(item, tuple)
            or len(item) != 2
            or not isinstance(item[0], str)
            or not isinstance(item[1], str)
            or HEADER_NAME_RE.fullmatch(item[0]) is None
            or "\r" in item[1]
            or "\n" in item[1]
        ):
            raise ValueError("GitHub response header is malformed")
        if item[0].casefold() == "location":
            raise ValueError("GitHub API redirects are forbidden")
    retrieved_at = _utc(response.retrieved_at, "GitHub retrieval timestamp")
    if retrieved_at > now or (now - retrieved_at).total_seconds() > FRESHNESS_SECONDS:
        raise ValueError("GitHub acquisition is stale")


def _validate_tag_absence(response: ApiResponse, now: datetime) -> None:
    if response.requested_resource != TAG_RESOURCE:
        raise ValueError("GitHub tag lookup resource is invalid")
    if response.observed_request_uri != f"/{TAG_RESOURCE}":
        raise ValueError("GitHub request URI changed")
    if response.redirect_count != 0:
        raise ValueError("GitHub API redirects are forbidden")
    for name, value in response.headers:
        if (
            HEADER_NAME_RE.fullmatch(name) is None
            or "\r" in value
            or "\n" in value
        ):
            raise ValueError("GitHub response header is malformed")
        if name.casefold() == "location":
            raise ValueError("GitHub API redirects are forbidden")
    retrieved_at = _utc(response.retrieved_at, "GitHub retrieval timestamp")
    if retrieved_at > now or (now - retrieved_at).total_seconds() > FRESHNESS_SECONDS:
        raise ValueError("GitHub acquisition is stale")
    if response.status == 200:
        raise ValueError("remote v0.5-beta tag already exists")
    if response.status != 404:
        raise ValueError("GitHub tag lookup status shall equal 404")
    try:
        body = response.json_object()
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("GitHub tag absence response is invalid") from exc
    if body.get("message") != "Not Found":
        raise ValueError("GitHub tag absence response is invalid")


def _validate_local_results(
    value: object, expected_head: str
) -> None:
    expected = set(COMMAND_IDS) - {"mermaid_rendering"}
    if not isinstance(value, list) or not all(
        isinstance(item, dict) for item in value
    ):
        raise ValueError("local validation command results are invalid")
    names = [item.get("name") for item in value]
    if (
        len(names) != len(expected)
        or len(set(names)) != len(names)
        or set(names) != expected
    ):
        raise ValueError("local validation command results are invalid")
    for item in value:
        if (
            set(item) != {"name", "sha", "exit_code", "result"}
            or item.get("sha") != expected_head
            or item.get("exit_code") != 0
            or not _nonblank(item.get("result"))
        ):
            raise ValueError("local validation command results are invalid")


def _validated_candidate_commands(
    value: object, expected_head: str
) -> list[dict[str, object]]:
    if not isinstance(value, list) or not all(
        isinstance(item, dict) for item in value
    ):
        raise ValueError("base candidate commands are invalid")
    by_name = {item.get("name"): item for item in value}
    if len(value) != len(COMMAND_IDS) or set(by_name) != set(COMMAND_IDS):
        raise ValueError("base candidate commands are invalid")
    nonvisual = [
        deepcopy(by_name[name])
        for name in COMMAND_IDS
        if name != "mermaid_rendering"
    ]
    try:
        _validate_local_results(nonvisual, expected_head)
    except ValueError as exc:
        raise ValueError("base candidate commands are invalid") from exc
    rendering = by_name["mermaid_rendering"]
    if (
        set(rendering) != {"name", "sha", "exit_code", "result"}
        or rendering.get("sha") != expected_head
        or rendering.get("exit_code") != 0
        or not isinstance(rendering.get("result"), dict)
    ):
        raise ValueError("base candidate commands are invalid")
    return [deepcopy(by_name[name]) for name in COMMAND_IDS]


def _validated_check_runs(
    page_set: ApiPageSet,
    expected_head: str,
    now: datetime,
) -> tuple[dict[str, object], dict[str, object]]:
    if not page_set.complete or not page_set.pages:
        raise ValueError("GitHub pagination is incomplete")
    if any(
        not _resource_is_page(
            page.requested_resource,
            page_set.requested_resource,
            index,
        )
        for index, page in enumerate(page_set.pages, start=1)
    ):
        raise ValueError("GitHub pagination is incomplete")
    for index, page in enumerate(page_set.pages):
        _validate_response(page, now)
        next_link = _next_link(page.headers)
        if index < len(page_set.pages) - 1:
            if (
                next_link is None
                or _api_link_resource(next_link)
                != page_set.pages[index + 1].requested_resource
            ):
                raise ValueError("GitHub pagination is incomplete")
        elif next_link is not None:
            raise ValueError("GitHub pagination is incomplete")
    check_runs: list[dict[str, object]] = []
    total_count: int | None = None
    for page in page_set.pages:
        value = page.json_object()
        page_runs = value.get("check_runs")
        if not isinstance(page_runs, list) or not all(
            isinstance(item, dict) for item in page_runs
        ):
            raise ValueError("GitHub check-runs response is incomplete")
        if total_count is None:
            count = value.get("total_count")
            if not _integer(count):
                raise ValueError("GitHub check-runs response is incomplete")
            total_count = count
        check_runs.extend(page_runs)
    if total_count != len(check_runs):
        raise ValueError("GitHub pagination is incomplete")
    matches = [item for item in check_runs if item.get("name") == CHECK_NAME]
    if len(matches) != 1:
        raise ValueError("GitHub required check shall appear exactly once")
    check = matches[0]
    app = check.get("app")
    details_url = check.get("details_url")
    run_match = (
        re.fullmatch(
            (
                r"https://github\.com/tdistress/ESAF/"
                r"actions/runs/([1-9][0-9]*)"
                r"(?:/job/[1-9][0-9]*)?"
            ),
            details_url,
        )
        if isinstance(details_url, str)
        else None
    )
    if (
        check.get("head_sha") != expected_head
        or check.get("status") != "completed"
        or check.get("conclusion") != "success"
        or not isinstance(app, dict)
        or app.get("slug") != "github-actions"
        or app.get("name") != "GitHub Actions"
        or app.get("html_url")
        != "https://github.com/apps/github-actions"
        or run_match is None
    ):
        raise ValueError(
            "check shall bind the canonical GitHub Actions workflow run"
        )
    result = deepcopy(check)
    result["run_id"] = int(run_match.group(1))
    return result, _page_acquisition_entry(
        page_set,
        f"{WEB_ROOT}/actions/runs/{result['run_id']}",
    )


def _validate_owner_comment(
    value: dict[str, object],
    source: dict[str, object],
    expected_head: str,
    mapping_ids: list[str],
) -> None:
    if set(value) != OWNER_KEYS:
        raise ValueError("owner decision keys are invalid")
    if value.get("schema") != OWNER_DECISION_SCHEMA:
        raise ValueError("owner decision schema is invalid")
    if (
        value.get("release") != RELEASE
        or value.get("sha") != expected_head
        or value.get("mapping_decision_basis") != "owner_risk_acceptance"
        or value.get("decision_type") != "owner_risk_acceptance"
        or value.get("disposition") != OWNER_DISPOSITION
        or value.get("qualified_review_status") != QUALIFIED_REVIEW_STATUS
    ):
        raise ValueError("owner decision release disposition is invalid")
    owner_mapping_ids = value.get("mapping_set_ids")
    if (
        not isinstance(owner_mapping_ids, list)
        or len(owner_mapping_ids) != 3
        or not all(isinstance(item, str) for item in owner_mapping_ids)
        or len(set(owner_mapping_ids)) != 3
        or set(owner_mapping_ids) != set(mapping_ids)
    ):
        raise ValueError("owner decision mapping sets are invalid")
    expected_roles = {
        (mapping_id, role)
        for mapping_id in mapping_ids
        for role in MISSING_ROLES
    }
    roles = value.get("missing_qualified_roles")
    if (
        not isinstance(roles, list)
        or len(roles) != 6
        or any(
            not isinstance(item, dict)
            or set(item) != {"mapping_set_id", "role"}
            for item in roles
        )
        or {
            (item["mapping_set_id"], item["role"])
            for item in roles
            if isinstance(item, dict)
        }
        != expected_roles
    ):
        raise ValueError("owner decision missing qualified roles are invalid")
    scope = value.get("scope_approval")
    if (
        not isinstance(scope, dict)
        or set(scope) != {"scope", "milestone", "disposition"}
        or scope.get("scope") != REPOSITORY_SCOPE
        or scope.get("milestone") != TAG
        or scope.get("disposition")
        != "approved_for_working_draft_closure"
    ):
        raise ValueError("owner scope approval is invalid")
    if (
        value.get("accountable_owner") != source.get("author_login")
        or source.get("author_association") != "OWNER"
    ):
        raise ValueError("owner decision shall use authenticated OWNER source")
    if (
        value.get("issue_55_status") != "remains_open"
        or value.get("lifecycle") != "draft"
        or _string_set(value.get("claims_not_made")) != CLAIMS_NOT_MADE
        or _string_set(value.get("reentry_triggers")) != REENTRY_TRIGGERS
    ):
        raise ValueError("owner decision limitations are invalid")


def _validate_release_verdict(
    value: dict[str, object],
    source: dict[str, object],
    expected_kind: str,
    expected_head: str,
) -> None:
    expected_keys = VERDICT_KEYS | (
        RENDERING_KEYS if expected_kind == "rendering" else set()
    )
    if set(value) != expected_keys:
        raise ValueError("release verdict keys are invalid")
    if (
        value.get("schema") != VERDICT_SCHEMA
        or value.get("release") != RELEASE
        or value.get("sha") != expected_head
        or value.get("date") != str(source.get("created_at"))[:10]
        or value.get("disposition") != "approved"
        or value.get("critical") != 0
        or value.get("important") != 0
    ):
        raise ValueError("release verdict disposition is invalid")
    if value.get("kind") != expected_kind:
        raise ValueError("release verdict kind is invalid")
    if (
        value.get("reviewer") != source.get("author_login")
        or not _nonblank(value.get("role"))
    ):
        raise ValueError("release verdict reviewer identity is invalid")
    if expected_kind == "rendering" and (
        value.get("rendered_blocks") != MERMAID_BLOCKS
        or value.get("renderer") != MERMAID_RENDERER
        or value.get("visual_review") != "approved"
    ):
        raise ValueError("rendering verdict is invalid")


def _validate_governance_verdict(
    value: dict[str, object],
    source: dict[str, object],
    expected_head: str,
) -> None:
    if set(value) != GOVERNANCE_KEYS:
        raise ValueError("governance verdict keys are invalid")
    if value.get("schema") != GOVERNANCE_SCHEMA:
        raise ValueError("governance verdict schema is invalid")
    if (
        value.get("release") != RELEASE
        or value.get("sha") != expected_head
        or value.get("kind") != "governance"
        or value.get("approver") != source.get("author_login")
        or value.get("date") != str(source.get("created_at"))[:10]
        or value.get("disposition")
        != "approved_for_working_draft_publication"
        or value.get("critical") != 0
        or value.get("important") != 0
    ):
        raise ValueError("governance verdict disposition is invalid")
    if (
        value.get("authority") != "Steering Committee"
        or value.get("authority_attestation") is not True
        or value.get("authority_verification") != "manual"
        or value.get("authority_basis")
        != "GOVERNANCE.md#21-steering-committee"
    ):
        raise ValueError("governance authority attestation is invalid")


def _validate_post_merge_rendering_verdict(
    value: dict[str, object],
    source: dict[str, object],
    merge_head: str,
    merge_tree: str,
) -> None:
    if set(value) != POST_MERGE_RENDERING_KEYS:
        raise ValueError(
            "post-merge rendering verdict keys are invalid"
        )
    if (
        value.get("schema") != POST_MERGE_RENDERING_SCHEMA
        or value.get("release") != RELEASE
        or value.get("sha") != merge_head
        or value.get("tree") != merge_tree
        or value.get("kind") != "post_merge_rendering"
        or value.get("reviewer") != source.get("author_login")
        or not _nonblank(value.get("role"))
        or value.get("date") != str(source.get("created_at"))[:10]
        or value.get("disposition") != "approved"
        or value.get("critical") != 0
        or value.get("important") != 0
        or value.get("rendered_blocks") != MERMAID_BLOCKS
        or value.get("renderer") != MERMAID_RENDERER
        or value.get("visual_review") != "approved"
    ):
        raise ValueError(
            "post-merge rendering verdict is invalid"
        )


def _release_verdict(
    value: dict[str, object], source: dict[str, object]
) -> dict[str, object]:
    return {
        "sha": value["sha"],
        "reviewer": value["reviewer"],
        "role": value["role"],
        "date": value["date"],
        "disposition": value["disposition"],
        "url": source["comment_url"],
        "critical": value["critical"],
        "important": value["important"],
        "source": deepcopy(source),
    }


def _tracked_mapping_set_ids(root: Path) -> list[str]:
    catalog_path = root / "crosswalks/catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        mapping_sets = catalog["mapping_sets"]
        identifiers = [
            item["metadata"]["mapping_set_id"] for item in mapping_sets
        ]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("tracked mapping-set inventory cannot be read") from exc
    if (
        not isinstance(identifiers, list)
        or len(identifiers) != 3
        or len(set(identifiers)) != 3
        or not all(isinstance(item, str) for item in identifiers)
    ):
        raise ValueError("tracked mapping-set inventory is invalid")
    return identifiers


def _acquisition_entry(
    response: ApiResponse, canonical_url: str
) -> dict[str, object]:
    return {
        "resource_id": response.requested_resource,
        "observed_canonical_url": canonical_url,
        "page_count": 1,
        "response_sha256": sha256(response.raw_body).hexdigest(),
        "retrieved_at": _format_utc(response.retrieved_at),
    }


def _page_acquisition_entry(
    page_set: ApiPageSet, canonical_url: str
) -> dict[str, object]:
    digest = sha256()
    for page in page_set.pages:
        digest.update(len(page.raw_body).to_bytes(8, "big"))
        digest.update(page.raw_body)
    if len(page_set.pages) == 1:
        response_digest = sha256(page_set.pages[0].raw_body).hexdigest()
    else:
        response_digest = digest.hexdigest()
    return {
        "resource_id": page_set.requested_resource,
        "observed_canonical_url": canonical_url,
        "page_count": len(page_set.pages),
        "response_sha256": response_digest,
        "retrieved_at": _format_utc(
            max(page.retrieved_at for page in page_set.pages)
        ),
    }


def _require_unchanged_sources(
    previous: dict[str, object], fresh: dict[str, object]
) -> None:
    stable_fields = {
        "repository",
        "resource_path",
        "comment_url",
        "comment_id",
        "author_login",
        "author_user_id",
        "author_association",
        "created_at",
        "updated_at",
        "body_sha256",
        "response_sha256",
        "acquisition_resource_id",
    }
    names = (
        "scope",
        "technical",
        "editorial",
        "terminology",
        "rendering",
        "profile_scope",
        "security_overclaiming",
        "whole_range",
        "governance",
    )
    for name in names:
        old = previous.get(name)
        new = fresh.get(name)
        if not isinstance(old, dict) or not isinstance(new, dict):
            raise ValueError("GitHub source changed")
        old_source = old.get("source")
        new_source = new.get("source")
        if not isinstance(old_source, dict) or not isinstance(new_source, dict):
            raise ValueError("GitHub source changed")
        if {
            field: old_source.get(field) for field in stable_fields
        } != {
            field: new_source.get(field) for field in stable_fields
        }:
            raise ValueError("GitHub source changed")


def _string_set(value: object) -> set[str]:
    if (
        not isinstance(value, list)
        or not all(isinstance(item, str) for item in value)
        or len(value) != len(set(value))
    ):
        return set()
    return set(value)


def _integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _https(value: object) -> bool:
    return isinstance(value, str) and value.startswith("https://")


def _reference_now(fixed: datetime | None) -> datetime:
    return fixed or datetime.now(timezone.utc)


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError(f"{label} shall be RFC 3339 UTC")
    normalized = value.astimezone(timezone.utc)
    if value.utcoffset() != timezone.utc.utcoffset(value):
        raise ValueError(f"{label} shall be RFC 3339 UTC")
    return normalized


def _parse_rfc3339(value: object, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{label} shall be RFC 3339 UTC")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{label} shall be RFC 3339 UTC") from exc
    return _utc(parsed, label)


def _format_utc(value: datetime) -> str:
    return _utc(value, "timestamp").isoformat().replace("+00:00", "Z")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr-number", type=int, required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--owner-comment-id", type=int, required=True)
    parser.add_argument("--technical-comment-id", type=int, required=True)
    parser.add_argument("--editorial-comment-id", type=int, required=True)
    parser.add_argument("--terminology-comment-id", type=int, required=True)
    parser.add_argument("--rendering-comment-id", type=int, required=True)
    parser.add_argument("--profile-scope-comment-id", type=int, required=True)
    parser.add_argument("--governance-comment-id", type=int, required=True)
    parser.add_argument(
        "--security-overclaiming-comment-id",
        type=int,
        required=True,
    )
    parser.add_argument("--whole-range-comment-id", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-evidence", type=Path)
    parser.add_argument("--merge-head")
    parser.add_argument("--post-merge-rendering-comment-id", type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    root = Path.cwd().resolve()
    output = arguments.output.resolve()
    try:
        forbidden_roots = _git_storage_roots(root, subprocess.run)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(
            f"v0.5-beta evidence collection failed: {exc}",
            file=sys.stderr,
        )
        return 1
    if any(_path_is_within(output, boundary) for boundary in forbidden_roots):
        print(
            "output shall remain outside every Git worktree "
            "and the Git common directory",
            file=sys.stderr,
        )
        return 1
    taggable_values = (
        arguments.base_evidence,
        arguments.merge_head,
        arguments.post_merge_rendering_comment_id,
    )
    taggable_count = sum(value is not None for value in taggable_values)
    if taggable_count not in {0, 3}:
        print(
            "base-evidence, merge-head, and "
            "post-merge-rendering-comment-id "
            "shall be supplied together",
            file=sys.stderr,
        )
        return 1
    collection_arguments = {
        "root": root,
        "pr_number": arguments.pr_number,
        "expected_head": arguments.expected_head,
        "owner_comment_id": arguments.owner_comment_id,
        "technical_comment_id": arguments.technical_comment_id,
        "editorial_comment_id": arguments.editorial_comment_id,
        "terminology_comment_id": arguments.terminology_comment_id,
        "rendering_comment_id": arguments.rendering_comment_id,
        "profile_scope_comment_id": arguments.profile_scope_comment_id,
        "governance_comment_id": arguments.governance_comment_id,
        "security_overclaiming_comment_id": (
            arguments.security_overclaiming_comment_id
        ),
        "whole_range_comment_id": arguments.whole_range_comment_id,
    }
    try:
        client = GhApiClient()
        if taggable_count == 0:
            evidence = collect_closure_evidence(
                client, **collection_arguments
            )
        else:
            base_evidence = _load_json(arguments.base_evidence)
            evidence = refresh_taggable_evidence(
                client,
                base_evidence=base_evidence,
                merge_head=arguments.merge_head,
                post_merge_rendering_comment_id=(
                    arguments.post_merge_rendering_comment_id
                ),
                **collection_arguments,
            )
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(
                evidence,
                stream,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            stream.write("\n")
    except (
        FileExistsError,
        json.JSONDecodeError,
        OSError,
        subprocess.SubprocessError,
        ValueError,
    ) as exc:
        print(f"v0.5-beta evidence collection failed: {exc}", file=sys.stderr)
        return 1
    return 0


def _git_storage_roots(
    root: Path, runner: Callable[..., object]
) -> tuple[Path, ...]:
    worktrees = runner(
        ["git", "worktree", "list", "--porcelain"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    common = runner(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if (
        getattr(worktrees, "returncode", None) != 0
        or getattr(common, "returncode", None) != 0
        or not isinstance(getattr(worktrees, "stdout", None), bytes)
        or not isinstance(getattr(common, "stdout", None), bytes)
    ):
        raise ValueError("Git storage boundaries could not be verified")
    worktree_text = worktrees.stdout.decode(
        "utf-8", errors="strict"
    )
    common_text = common.stdout.decode("utf-8", errors="strict").strip()
    paths = [
        Path(line.removeprefix("worktree ")).resolve()
        for line in worktree_text.splitlines()
        if line.startswith("worktree ")
    ]
    if not paths or not common_text:
        raise ValueError("Git storage boundaries could not be verified")
    common_path = Path(common_text)
    if not common_path.is_absolute():
        common_path = root / common_path
    paths.append(common_path.resolve())
    return tuple(dict.fromkeys(paths))


def _path_is_within(path: Path, boundary: Path) -> bool:
    try:
        path.relative_to(boundary)
    except ValueError:
        return False
    return True


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON object is required")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
