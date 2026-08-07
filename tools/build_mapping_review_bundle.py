from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import sys
import tempfile
import threading
import time
from typing import Literal, NamedTuple

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.crosswalks.catalog import build_catalog
from tools.crosswalks.digests import snapshot_digest_from_files
from tools.crosswalks.io import load_yaml_mapping
from tools.crosswalks.manifest import build_control_manifest, render_manifest
from tools.crosswalks.validation import ValidationResult


FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
GENERATOR_VERSION = "1.2.0"
GIT_COMMAND_TIMEOUT_SECONDS = 120
GIT_STDERR_LIMIT = 65_536
GIT_LEGACY_STDOUT_LIMIT = 128 * 1024 * 1024
_SOURCE_EVIDENCE_PATH = re.compile(
    r"(?m)^- (?:Oracle|Specification): `([^`]+)`\s*$"
)
_SOURCE_EVIDENCE_PIN = re.compile(
    r"(?m)^- (?P<label>Oracle|Specification): "
    r"`(?P<path>[^`\r\n]+)`[ \t]*\n"
    r"- (?P=label) SHA-256: "
    r"`(?P<sha256>[0-9a-f]{64})`[ \t]*$"
)


@dataclass(frozen=True)
class MappingProfile:
    mapping_set_id: str
    snapshot_path: str
    label: str
    direction: str
    expected_count: int


_PROFILE_ROWS = (
    (
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0",
        "Core",
        "esaf_to_external",
        116,
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0",
        "Plus forward",
        "esaf_to_external",
        144,
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0",
        "Plus reverse",
        "external_to_esaf",
        144,
    ),
)
PROFILES = {row[0]: MappingProfile(*row) for row in _PROFILE_ROWS}


class GitObjectReadError(subprocess.SubprocessError):
    """A sanitized failure from a bounded Git object command."""


@dataclass(frozen=True)
class _GitCommandResult:
    stdout: bytes
    stderr: bytes


@dataclass(frozen=True)
class PackageFile:
    path: str
    content: bytes
    purpose: str


CandidateState = Literal["draft", "reviewed"]


class PackageAssembly(NamedTuple):
    payloads: tuple[PackageFile, ...]
    manifest: dict[str, object]
    manifest_bytes: bytes


def parse_front_matter_bytes(content: bytes) -> tuple[dict[str, object], str]:
    if content.startswith(b"\xef\xbb\xbf") or b"\r" in content:
        raise ValueError("package Markdown must be canonical UTF-8/LF")
    text = content.decode("utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("malformed YAML front matter")
    return load_yaml_mapping(parts[1]), parts[2]


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


@lru_cache(maxsize=None)
def _deterministic_control_manifest_bytes(
    root: Path,
    commit: str,
    release: str,
    tag_alias: str | None,
) -> bytes:
    manifest = build_control_manifest(root, commit, release, tag_alias)
    return render_manifest(manifest).encode("utf-8")


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _canonical_relative_path(value: str, subject: str) -> PurePosixPath:
    path = PurePosixPath(value)
    windows_path = PureWindowsPath(value)
    if (
        not value
        or "\\" in value
        or path.is_absolute()
        or windows_path.is_absolute()
        or bool(windows_path.drive)
        or any(part in {".", ".."} for part in path.parts)
        or path.as_posix() != value
    ):
        raise ValueError(f"unsafe {subject} path: {value}")
    return path


def validate_output_directory(
    output: Path, worktrees: tuple[Path, ...]
) -> Path:
    if os.path.lexists(output):
        raise ValueError(
            "output must not already exist; choose a new empty destination"
        )
    resolved = output.resolve()
    if any(_is_within(resolved, root) for root in worktrees):
        raise ValueError("output must be outside every Git worktree")
    return resolved


class GitReader:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self._git_environment = {
            name: value
            for name, value in os.environ.items()
            if not name.upper().startswith("GIT_")
        }
        self._git_environment.update(
            {
                "GIT_NO_REPLACE_OBJECTS": "1",
                "GIT_NO_LAZY_FETCH": "1",
                "GIT_OPTIONAL_LOCKS": "0",
                "GIT_TERMINAL_PROMPT": "0",
                "LC_ALL": "C",
                "LANG": "C",
            }
        )
        self._sha1_verified = False
        self._verified_commits: set[str] = set()
        self._regular_blobs: set[tuple[str, str]] = set()
        self._contents: dict[tuple[str, str], bytes] = {}

    def _run_finite_git(
        self,
        arguments: tuple[str, ...],
        *,
        input_bytes: bytes = b"",
        stdout_limit: int,
        stderr_limit: int = GIT_STDERR_LIMIT,
    ) -> _GitCommandResult:
        command = [
            "git",
            "--no-replace-objects",
            "-c",
            "core.fsmonitor=false",
            "-C",
            str(self.root),
            *arguments,
        ]
        process: subprocess.Popen[bytes] | None = None
        deadline: float | None = None
        spools: list[object] = []
        stdout_spool: object | None = None
        stderr_spool: object | None = None
        drainer_threads: list[threading.Thread] = []
        started_threads: list[threading.Thread] = []
        reaped = False
        failures: list[Exception] = []
        failure_lock = threading.Lock()

        def add_failure(error: Exception) -> None:
            with failure_lock:
                failures.append(error)

        def terminate_child() -> None:
            if process is None:
                return
            try:
                process.terminate()
            except Exception as error:
                add_failure(error)

        def kill_child() -> None:
            if process is None:
                return
            try:
                process.kill()
            except Exception as error:
                add_failure(error)

        def record_failure(error: Exception) -> None:
            add_failure(error)
            terminate_child()

        def close_resource(resource: object | None) -> None:
            if resource is None:
                return
            try:
                resource.close()  # type: ignore[attr-defined]
            except Exception as error:
                add_failure(error)

        def wait_for_child(timeout: float) -> bool:
            if process is None:
                return False
            try:
                process.wait(timeout=max(0.0, timeout))
                return True
            except Exception as error:
                add_failure(error)
                return False

        def join_thread(thread: threading.Thread, timeout: float) -> None:
            try:
                thread.join(timeout=max(0.0, timeout))
            except Exception as error:
                add_failure(error)

        def remaining_deadline() -> float:
            if deadline is None:
                return 0.0
            return max(0.0, deadline - time.monotonic())

        def write_input() -> None:
            if process is None or process.stdin is None:
                record_failure(OSError("missing Git stdin pipe"))
                return
            try:
                view = memoryview(input_bytes)
                offset = 0
                while offset < len(view):
                    written = process.stdin.write(view[offset:])
                    if written is None or written <= 0:
                        raise OSError("short write to Git command")
                    offset += written
                process.stdin.flush()
            except Exception as error:
                record_failure(error)
            finally:
                close_resource(process.stdin)

        def drain(
            stream: object,
            spool: object,
            limit: int,
            subject: str,
        ) -> None:
            total = 0
            try:
                while True:
                    chunk = stream.read(65_536)  # type: ignore[attr-defined]
                    if not chunk:
                        return
                    total += len(chunk)
                    if total > limit:
                        record_failure(OverflowError(f"{subject} limit exceeded"))
                        return
                    spool.write(chunk)  # type: ignore[attr-defined]
            except Exception as error:
                record_failure(error)
            finally:
                close_resource(stream)

        stdout = b""
        stderr = b""
        try:
            stdout_spool = tempfile.SpooledTemporaryFile(
                max_size=1024 * 1024,
                mode="w+b",
            )
            spools.append(stdout_spool)
            stderr_spool = tempfile.SpooledTemporaryFile(
                max_size=1024 * 1024,
                mode="w+b",
            )
            spools.append(stderr_spool)
            process = subprocess.Popen(
                command,
                shell=False,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self._git_environment,
            )
            deadline = time.monotonic() + GIT_COMMAND_TIMEOUT_SECONDS
            if process.stdin is None or process.stdout is None or process.stderr is None:
                raise OSError("missing Git command pipe")

            drainer_threads = [
                threading.Thread(
                    target=drain,
                    args=(process.stdout, stdout_spool, stdout_limit, "stdout"),
                    daemon=True,
                ),
                threading.Thread(
                    target=drain,
                    args=(process.stderr, stderr_spool, stderr_limit, "stderr"),
                    daemon=True,
                ),
            ]
            writer_thread = threading.Thread(target=write_input, daemon=True)
            for thread in (*drainer_threads, writer_thread):
                thread.start()
                started_threads.append(thread)

            reaped = wait_for_child(remaining_deadline())
            if not reaped:
                terminate_child()
                reaped = wait_for_child(5)
            if not reaped:
                kill_child()
                for _attempt in range(2):
                    if wait_for_child(5):
                        reaped = True
                        break

            terminal_failure = bool(failures) or not reaped
            if terminal_failure:
                close_resource(process.stdin)
                close_resource(process.stdout)
                close_resource(process.stderr)
                for thread in started_threads:
                    join_thread(thread, 5)
            else:
                for thread in started_threads:
                    join_thread(thread, remaining_deadline())
                if any(thread.is_alive() for thread in started_threads):
                    add_failure(TimeoutError("Git command I/O thread did not finish"))
                    close_resource(process.stdin)
                    close_resource(process.stdout)
                    close_resource(process.stderr)
                    for thread in started_threads:
                        join_thread(thread, 5)

            if any(thread.is_alive() for thread in started_threads):
                kill_child()
                close_resource(process.stdin)
                close_resource(process.stdout)
                close_resource(process.stderr)
                for thread in started_threads:
                    join_thread(thread, 5)
            if any(thread.is_alive() for thread in started_threads):
                add_failure(TimeoutError("Git command I/O thread did not stop"))

            close_resource(process.stdin)
            close_resource(process.stdout)
            close_resource(process.stderr)
            if not any(thread.is_alive() for thread in drainer_threads):
                try:
                    stdout_spool.seek(0)  # type: ignore[attr-defined]
                    stderr_spool.seek(0)  # type: ignore[attr-defined]
                    stdout = stdout_spool.read()  # type: ignore[attr-defined]
                    stderr = stderr_spool.read()  # type: ignore[attr-defined]
                except Exception as error:
                    add_failure(error)
        except Exception as error:
            add_failure(error)
        finally:
            if process is not None:
                if not reaped:
                    terminate_child()
                    reaped = wait_for_child(5)
                if not reaped:
                    kill_child()
                    for _attempt in range(2):
                        if wait_for_child(5):
                            reaped = True
                            break
                for stream in (process.stdin, process.stdout, process.stderr):
                    close_resource(stream)
                for thread in started_threads:
                    join_thread(thread, 5)
                if any(thread.is_alive() for thread in started_threads):
                    add_failure(TimeoutError("Git command I/O thread did not stop"))
            if not any(thread.is_alive() for thread in drainer_threads):
                for spool in spools:
                    close_resource(spool)

        if (
            failures
            or not reaped
            or process is None
            or process.returncode != 0
            or stderr
            or any(thread.is_alive() for thread in started_threads)
        ):
            raise GitObjectReadError("Git object read failed")
        return _GitCommandResult(stdout=stdout, stderr=stderr)

    def _require_sha1_repository(self) -> None:
        if self._sha1_verified:
            return
        result = self._run_finite_git(
            ("rev-parse", "--show-object-format=storage"),
            stdout_limit=16,
        )
        if result.stdout != b"sha1\n":
            raise GitObjectReadError("Git object read failed")
        self._sha1_verified = True

    def _run(
        self,
        *arguments: str,
        text: bool = False,
    ) -> subprocess.CompletedProcess:
        self._require_sha1_repository()
        result = self._run_finite_git(
            tuple(arguments),
            stdout_limit=GIT_LEGACY_STDOUT_LIMIT,
        )
        stdout: bytes | str = result.stdout
        stderr: bytes | str = result.stderr
        if text:
            stdout = result.stdout.decode("utf-8")
            stderr = result.stderr.decode("utf-8")
        return subprocess.CompletedProcess(arguments, 0, stdout, stderr)

    def resolve_commit(self, revision: str) -> str:
        if not FULL_SHA.fullmatch(revision):
            raise ValueError(
                "candidate must be a full lowercase 40-character Git SHA"
            )
        if revision in self._verified_commits:
            return revision
        self._require_sha1_repository()
        try:
            result = self._run_finite_git(
                ("rev-parse", "--verify", f"{revision}^{{commit}}"),
                stdout_limit=41,
            )
        except GitObjectReadError as error:
            raise ValueError("candidate is not an available commit") from error
        if result.stdout != revision.encode("ascii") + b"\n":
            raise ValueError("candidate does not resolve to the exact commit")
        self._verified_commits.add(revision)
        return revision

    def read_bytes(self, commit: str, path: str) -> bytes:
        _canonical_relative_path(path, "repository")
        commit = self.resolve_commit(commit)
        self._require_regular_blob(commit, path)
        key = (commit, path)
        cached = self._contents.get(key)
        if cached is not None:
            return cached
        content = self._run("show", f"{commit}:{path}").stdout
        self._contents[key] = content
        return content

    def _require_regular_blob(self, commit: str, path: str) -> None:
        key = (commit, path)
        if key in self._regular_blobs:
            return
        result = self._run(
            "ls-tree",
            "-z",
            commit,
            "--",
            path,
        ).stdout
        entries = [item for item in result.split(b"\0") if item]
        if not entries:
            raise ValueError(f"missing tracked file at candidate: {path}")
        if len(entries) != 1:
            raise ValueError(f"unexpected repository entry: {path}")
        try:
            header, raw_name = entries[0].split(b"\t", 1)
            mode, object_type, _object_id = header.split(b" ", 2)
            name = raw_name.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as error:
            raise ValueError("malformed Git tree entry") from error
        if (
            name != path
            or object_type != b"blob"
            or mode not in {b"100644", b"100755"}
        ):
            raise ValueError(f"unexpected repository entry: {name}")
        self._regular_blobs.add(key)

    def list_files(self, commit: str, path: str) -> tuple[str, ...]:
        _canonical_relative_path(path, "repository")
        commit = self.resolve_commit(commit)
        result = self._run(
            "ls-tree",
            "-r",
            "-z",
            commit,
            "--",
            path,
        ).stdout
        names: list[str] = []
        for item in result.split(b"\0"):
            if not item:
                continue
            try:
                header, raw_name = item.split(b"\t", 1)
                mode, object_type, _object_id = header.split(b" ", 2)
                name = raw_name.decode("utf-8")
            except (UnicodeDecodeError, ValueError) as error:
                raise ValueError("malformed Git tree entry") from error
            if object_type != b"blob" or mode not in {b"100644", b"100755"}:
                raise ValueError(f"unexpected repository entry: {name}")
            _canonical_relative_path(name, "repository")
            names.append(name)
            self._regular_blobs.add((commit, name))
        return tuple(sorted(names))

    def require_candidate_execution_state(self, commit: str) -> None:
        """Bind executing working-tree bytes to one clean candidate HEAD."""
        commit = self.resolve_commit(commit)
        head = self._run_finite_git(
            ("rev-parse", "HEAD"),
            stdout_limit=41,
        ).stdout
        if head != commit.encode("ascii") + b"\n":
            raise ValueError("current HEAD must equal candidate commit")
        status = self._run_finite_git(
            (
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--ignore-submodules=none",
            ),
            stdout_limit=8 * 1024 * 1024,
        ).stdout
        if status:
            raise ValueError(
                "repository must be clean, including non-ignored untracked files"
            )

    def worktree_roots(self) -> tuple[Path, ...]:
        output = self._run_finite_git(
            ("worktree", "list", "--porcelain", "-z"),
            stdout_limit=8 * 1024 * 1024,
        ).stdout
        roots = []
        for field in output.split(b"\0"):
            if field.startswith(b"worktree "):
                roots.append(Path(field[9:].decode("utf-8")).resolve())
        return tuple(roots)


def _package_file(
    reader: GitReader,
    commit: str,
    path: str,
    purpose: str,
) -> PackageFile:
    return PackageFile(path, reader.read_bytes(commit, path), purpose)


def _validate_candidate_metadata(
    reader: GitReader,
    commit: str,
    schema_path: str,
    metadata: dict[str, object],
    subject: str,
) -> None:
    try:
        schema = json.loads(reader.read_bytes(commit, schema_path))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, SchemaError, ValueError) as error:
        raise ValueError(f"invalid candidate schema: {schema_path}") from error
    errors = sorted(
        validator.iter_errors(metadata),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        raise ValueError(
            f"{subject} candidate schema validation failed: {errors[0].message}"
        )


def _candidate_validators(reader: GitReader, commit: str) -> dict[str, object]:
    validators: dict[str, object] = {}
    for name in (
        "mapping-set",
        "mapping-record",
        "provision-inventory",
        "lifecycle-record",
    ):
        path = f"crosswalks/schema/{name}.schema.json"
        try:
            schema = json.loads(reader.read_bytes(commit, path))
            Draft202012Validator.check_schema(schema)
            validators[name] = Draft202012Validator(schema, format_checker=FormatChecker())
        except (UnicodeDecodeError, json.JSONDecodeError, SchemaError, ValueError) as error:
            raise ValueError(f"invalid candidate schema: {path}") from error
    return validators


def _require_candidate_state(
    metadata: dict[str, object],
    mapping_set_id: str,
    subject: str,
    candidate_state: CandidateState,
) -> None:
    if metadata.get("mapping_set_id") != mapping_set_id:
        raise ValueError(f"{subject} mapping-set identifier mismatch")
    if metadata.get("status") != candidate_state:
        raise ValueError(f"{subject} must be {candidate_state}")
    reviewer = metadata.get("reviewer")
    if candidate_state == "draft" and reviewer is not None:
        raise ValueError(f"{subject} Draft content cannot contain reviewer metadata")
    if candidate_state == "reviewed" and not isinstance(reviewer, dict):
        raise ValueError(f"{subject} reviewed content requires reviewer metadata")
    if candidate_state == "reviewed":
        mapper = metadata.get("mapper")
        if isinstance(mapper, dict) and reviewer.get("id") == mapper.get("id"):
            raise ValueError(f"{subject} reviewer must differ from mapper")


def _require_reviewed_findings(metadata: dict[str, object]) -> None:
    findings = metadata.get("findings")
    if not isinstance(findings, list):
        raise ValueError("mapping set findings must be an array")
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("mapping set finding must be an object")
        severity = finding.get("severity")
        if severity in {"Critical", "Important"} and finding.get("status") != "resolved":
            raise ValueError(f"{severity} finding must be resolved")


def _source_evidence_pins(body: str) -> tuple[tuple[str, str], ...]:
    named_paths = _SOURCE_EVIDENCE_PATH.findall(body)
    matches = tuple(
        (match.group("path"), match.group("sha256"))
        for match in _SOURCE_EVIDENCE_PIN.finditer(body)
    )
    matched_paths = [path for path, _digest in matches]
    if (
        len(named_paths) != len(matches)
        or matched_paths != named_paths
        or len(set(matched_paths)) != len(matched_paths)
    ):
        raise ValueError(
            "every named source evidence file requires one adjacent checksum pin"
        )
    return matches


def _load_source_evidence(payload: PackageFile) -> dict[str, object]:
    try:
        evidence = json.loads(payload.content)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"invalid source evidence JSON: {payload.path}"
        ) from exc
    if not isinstance(evidence, dict):
        raise ValueError(f"invalid source evidence object: {payload.path}")
    return evidence


def _validate_source_evidence_identity(
    payload: PackageFile,
    mapping_metadata: dict[str, object],
) -> None:
    evidence = _load_source_evidence(payload)
    evidence_source = evidence.get("source")
    publication = mapping_metadata.get("publication")
    source_version = mapping_metadata.get("source_version")
    mapping_source = mapping_metadata.get("source")
    authority = mapping_metadata.get("authority")
    if not all(
        isinstance(item, dict)
        for item in (
            evidence_source,
            publication,
            source_version,
            mapping_source,
            authority,
        )
    ):
        raise ValueError(f"source evidence identity mismatch: {payload.path}")
    assert isinstance(evidence_source, dict)
    assert isinstance(publication, dict)
    assert isinstance(source_version, dict)
    assert isinstance(mapping_source, dict)
    assert isinstance(authority, dict)
    variants = evidence_source.get("variants")
    variant_urls = (
        {
            variant.get("url")
            for variant in variants
            if isinstance(variant, dict)
            and isinstance(variant.get("url"), str)
        }
        if isinstance(variants, list)
        else set()
    )
    expected_pairs = (
        (evidence_source.get("title"), publication.get("name")),
        (
            evidence_source.get("publication_identifier"),
            publication.get("id"),
        ),
        (evidence_source.get("version"), source_version.get("id")),
        (evidence_source.get("authority"), authority.get("name")),
    )
    if (
        any(
            not isinstance(actual, str)
            or not isinstance(expected, str)
            or actual != expected
            for actual, expected in expected_pairs
        )
        or mapping_source.get("official_url") not in variant_urls
    ):
        raise ValueError(f"source evidence identity mismatch: {payload.path}")


def collect_package_files(
    reader: GitReader,
    commit: str,
    profile: MappingProfile,
    candidate_state: CandidateState = "draft",
) -> tuple[PackageFile, ...]:
    snapshot_paths = reader.list_files(commit, profile.snapshot_path)
    snapshot_contents = {
        path: reader.read_bytes(commit, path)
        for path in snapshot_paths
    }
    try:
        expected_snapshot_digest = snapshot_digest_from_files(
            profile.snapshot_path,
            snapshot_contents,
        )
    except ValueError as error:
        raise ValueError(str(error)) from error
    fixed_names = {
        "README.md",
        "PROVISION_INVENTORY.md",
        "ESAF_CONTROL_MANIFEST.json",
    }
    record_paths = tuple(
        path
        for path in snapshot_paths
        if PurePosixPath(path).name not in fixed_names
    )
    if len(record_paths) != profile.expected_count:
        raise ValueError("mapping-record population mismatch")

    files: list[PackageFile] = []
    readme_path = f"{profile.snapshot_path}/README.md"
    readme = PackageFile(
        readme_path,
        snapshot_contents[readme_path],
        "mapping set",
    )
    set_metadata, set_body = parse_front_matter_bytes(readme.content)
    _validate_candidate_metadata(
        reader,
        commit,
        "crosswalks/schema/mapping-set.schema.json",
        set_metadata,
        "mapping set",
    )
    _require_candidate_state(
        set_metadata,
        profile.mapping_set_id,
        "mapping set",
        candidate_state,
    )
    if candidate_state == "reviewed":
        _require_reviewed_findings(set_metadata)
    scope = set_metadata.get("scope")
    if not isinstance(scope, dict) or scope.get("inventory_count") != profile.expected_count:
        raise ValueError("mapping-set inventory count mismatch")
    files.append(readme)

    inventory_path = f"{profile.snapshot_path}/PROVISION_INVENTORY.md"
    inventory = PackageFile(
        inventory_path,
        snapshot_contents[inventory_path],
        "provision inventory",
    )
    inventory_metadata, _ = parse_front_matter_bytes(inventory.content)
    if inventory_metadata.get("mapping_set_id") != profile.mapping_set_id:
        raise ValueError("inventory mapping-set identifier mismatch")
    provision_ids = inventory_metadata.get("provision_ids")
    if (
        inventory_metadata.get("expected_count") != profile.expected_count
        or not isinstance(provision_ids, list)
        or len(provision_ids) != profile.expected_count
        or len(set(provision_ids)) != profile.expected_count
    ):
        raise ValueError("provision inventory population mismatch")
    files.append(inventory)

    record_ids: set[str] = set()
    record_provisions: set[str] = set()
    provision_models: list[dict[str, object]] = []
    for path in record_paths:
        record = PackageFile(path, snapshot_contents[path], "mapping record")
        metadata, body = parse_front_matter_bytes(record.content)
        _validate_candidate_metadata(
            reader,
            commit,
            "crosswalks/schema/mapping-record.schema.json",
            metadata,
            f"record {path}",
        )
        _require_candidate_state(
            metadata,
            profile.mapping_set_id,
            f"record {path}",
            candidate_state,
        )
        record_id = metadata.get("record_id")
        provision_id = metadata.get("external_provision_id")
        if not isinstance(record_id, str) or record_id in record_ids:
            raise ValueError("duplicate or invalid mapping-record identifier")
        if not isinstance(provision_id, str) or provision_id in record_provisions:
            raise ValueError("duplicate or invalid external provision identifier")
        record_ids.add(record_id)
        record_provisions.add(provision_id)
        relationships = metadata.get("relationships")
        if not isinstance(relationships, list):
            raise ValueError(f"record {path} relationships must be an array")
        for relationship in relationships:
            if (
                not isinstance(relationship, dict)
                or relationship.get("direction") != profile.direction
            ):
                raise ValueError(
                    f"relationship direction mismatch: {path}"
                )
        provision_models.append(
            {
                "path": path,
                "metadata": metadata,
                "body": body,
            }
        )
        files.append(record)
    if record_provisions != set(provision_ids):
        raise ValueError("mapping records do not match provision inventory")

    manifest_path = f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"
    manifest_file = PackageFile(
        manifest_path,
        snapshot_contents[manifest_path],
        "control manifest",
    )
    manifest = json.loads(manifest_file.content)
    release = set_metadata.get("esaf_release")
    if not isinstance(release, dict):
        raise ValueError("mapping set ESAF release pin is missing")
    if manifest.get("esaf_release") != release.get("id"):
        raise ValueError("control manifest ESAF release mismatch")
    control_source = manifest.get("source_commit_sha")
    if not isinstance(control_source, str):
        raise ValueError("control manifest source commit is missing")
    control_source = reader.resolve_commit(control_source)
    if control_source != release.get("source_commit_sha"):
        raise ValueError("control manifest source commit mismatch")
    pinned_catalog_digest = release.get("control_catalog_sha256")
    control_catalog = reader.read_bytes(
        control_source,
        "controls/catalog.json",
    )
    actual_catalog_digest = hashlib.sha256(control_catalog).hexdigest()
    if (
        not isinstance(pinned_catalog_digest, str)
        or manifest.get("control_catalog_sha256") != pinned_catalog_digest
        or actual_catalog_digest != pinned_catalog_digest
    ):
        raise ValueError("control catalog digest mismatch")
    release_id = release.get("id")
    tag_alias = release.get("tag_alias")
    if not isinstance(release_id, str) or (
        tag_alias is not None and not isinstance(tag_alias, str)
    ):
        raise ValueError("mapping set ESAF release pin is invalid")
    expected_manifest = _deterministic_control_manifest_bytes(
        reader.root if isinstance(reader, GitReader) else ROOT,
        control_source,
        release_id,
        tag_alias,
    )
    if manifest_file.content != expected_manifest:
        raise ValueError(
            "control manifest differs from deterministic regeneration"
        )
    controls = manifest.get("controls")
    if not isinstance(controls, list) or not controls:
        raise ValueError("control manifest has no controls")
    files.append(manifest_file)
    files.append(
        PackageFile(
            "controls/catalog.json",
            control_catalog,
            "pinned ESAF control catalog",
        )
    )
    seen_controls: set[str] = set()
    for control in controls:
        if not isinstance(control, dict) or not isinstance(
            control.get("path"),
            str,
        ):
            raise ValueError("control manifest contains an invalid control")
        control_path = f"controls/{control['path']}"
        if control_path in seen_controls:
            raise ValueError("duplicate control manifest path")
        seen_controls.add(control_path)
        control_file = _package_file(
            reader, control_source, control_path, "referenced ESAF control"
        )
        if hashlib.sha256(control_file.content).hexdigest() != control["record_sha256"]:
            raise ValueError(f"control digest mismatch: {control_path}")
        files.append(control_file)

    registry_path = f"crosswalks/registry/{profile.mapping_set_id}.md"
    registry = _package_file(
        reader, commit, registry_path, "lifecycle registry"
    )
    registry_metadata, registry_body = parse_front_matter_bytes(registry.content)
    if registry_metadata.get("mapping_set_id") != profile.mapping_set_id:
        raise ValueError("registry mapping-set identifier mismatch")
    if registry_metadata.get("events") != []:
        raise ValueError("registry lifecycle event array must be empty")
    if registry_metadata.get("snapshot_digest") != expected_snapshot_digest:
        raise ValueError("registry snapshot digest mismatch")
    files.append(registry)

    catalog = json.loads(reader.read_bytes(commit, "crosswalks/catalog.json"))
    mapping_model: dict[str, object] = {
        "path": readme_path,
        "metadata": set_metadata,
        "inventory": {
            "path": inventory_path,
            "metadata": inventory_metadata,
        },
        "control_manifest": {
            "path": manifest_path,
            "metadata": manifest,
        },
        "provisions": provision_models,
        "lifecycle": registry_metadata,
    }
    lifecycle_model: dict[str, object] = {
        "path": registry_path,
        "metadata": registry_metadata,
        "body": registry_body,
    }
    expected_catalog = build_catalog(
        ValidationResult(
            [],
            [mapping_model],
            [lifecycle_model],
        ),
        _candidate_validators(reader, commit),
    )
    matches = [
        item
        for item in catalog.get("mapping_sets", [])
        if (
            isinstance(item, dict)
            and isinstance(item.get("metadata"), dict)
            and item["metadata"].get("mapping_set_id")
            == profile.mapping_set_id
        )
    ]
    expected_entries = expected_catalog["mapping_sets"]
    if (
        catalog.get("schema_version") != expected_catalog["schema_version"]
        or catalog.get("generated_from") != expected_catalog["generated_from"]
        or len(matches) != 1
        or not isinstance(expected_entries, list)
        or len(expected_entries) != 1
        or matches[0] != expected_entries[0]
    ):
        raise ValueError("catalog entry mismatch")
    catalog_bytes = canonical_json_bytes(
        {
            "schema_version": catalog["schema_version"],
            "generated_from": catalog["generated_from"],
            "mapping_set": matches[0],
        }
    )
    files.append(
        PackageFile(
            "review-metadata/catalog-entry.json",
            catalog_bytes,
            "catalog entry",
        )
    )

    fixed_paths = {
        "crosswalks/ESAF-1600.md": "ESAF-1600 method",
        "crosswalks/schema/esaf-control-manifest.schema.json": "crosswalk schema",
        "crosswalks/schema/lifecycle-record.schema.json": "crosswalk schema",
        "crosswalks/schema/mapping-record.schema.json": "crosswalk schema",
        "crosswalks/schema/mapping-set.schema.json": "crosswalk schema",
        "crosswalks/schema/provision-inventory.schema.json": "crosswalk schema",
        "crosswalks/schema/qualified-review-evidence.schema.json": (
            "qualified-review evidence schema"
        ),
        "crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md": "review protocol",
        "crosswalks/reviews/templates/REVIEWER_ATTESTATION.md": "blank review template",
        "crosswalks/reviews/templates/SPECIFICATION_INVENTORY_REVIEW.md": "blank review template",
        "crosswalks/reviews/templates/SECURITY_OVERCLAIMING_REVIEW.md": "blank review template",
    }
    files.extend(
        _package_file(reader, commit, path, purpose)
        for path, purpose in fixed_paths.items()
    )
    for path, pinned_digest in _source_evidence_pins(set_body):
        source_evidence = _package_file(
            reader,
            commit,
            path,
            "source evidence pin",
        )
        if hashlib.sha256(source_evidence.content).hexdigest() != pinned_digest:
            raise ValueError(f"source evidence digest mismatch: {path}")
        _validate_source_evidence_identity(source_evidence, set_metadata)
        files.append(source_evidence)
    paths = [item.path for item in files]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate package path")
    return tuple(sorted(files, key=lambda item: item.path))


def _source_evidence_references(
    payloads: tuple[PackageFile, ...],
) -> list[str]:
    references: list[str] = []
    for payload in payloads:
        if payload.purpose != "source evidence pin":
            continue
        evidence = _load_source_evidence(payload)
        source = evidence.get("source")
        if not isinstance(source, dict):
            raise ValueError(
                f"source evidence lacks source metadata: {payload.path}"
            )
        resource_page_url = source.get("resource_page_url")
        variants = source.get("variants")
        if not isinstance(resource_page_url, str) or not resource_page_url:
            raise ValueError(
                f"source evidence lacks resource-page URL: {payload.path}"
            )
        if not isinstance(variants, list) or not variants:
            raise ValueError(
                f"source evidence lacks source variants: {payload.path}"
            )
        references.append(f"Resource page: {resource_page_url}")
        for variant in variants:
            if not isinstance(variant, dict):
                raise ValueError(
                    f"invalid source variant in {payload.path}"
                )
            role = variant.get("role")
            url = variant.get("url")
            sha256 = variant.get("sha256")
            byte_length = variant.get("byte_length")
            if (
                not isinstance(role, str)
                or not role
                or not isinstance(url, str)
                or not url
                or not isinstance(sha256, str)
                or re.fullmatch(r"[0-9a-f]{64}", sha256) is None
                or not isinstance(byte_length, int)
                or isinstance(byte_length, bool)
                or byte_length < 0
            ):
                raise ValueError(
                    f"invalid source variant metadata in {payload.path}"
                )
            references.append(
                f"{role.capitalize()} source variant: {url}; "
                f"SHA-256 `{sha256}`; {byte_length:,} bytes"
            )
    return references


def render_package_index(
    profile: MappingProfile,
    commit: str,
    mapping_set_content: bytes,
    payloads: tuple[PackageFile, ...],
    candidate_state: CandidateState = "draft",
) -> bytes:
    metadata, body = parse_front_matter_bytes(mapping_set_content)
    publication = metadata["publication"]
    source = metadata["source"]
    rights = metadata["publication_rights"]
    source_version = metadata["source_version"]
    release = metadata["esaf_release"]
    source_references = []
    for line in body.splitlines():
        stripped = line.strip()
        if (
            "SHA-256" not in stripped
            and not stripped.startswith("- Oracle:")
            and not stripped.startswith("- Resource page:")
        ):
            continue
        reference = stripped.removeprefix("- ")
        if reference not in source_references:
            source_references.append(reference)
    for reference in _source_evidence_references(payloads):
        if reference not in source_references:
            source_references.append(reference)
    source_reference_lines = (
        "\n".join(f"- {item}" for item in source_references)
        if source_references
        else "- None recorded."
    )
    permitted = rights["permitted_elements"]
    prohibited = rights["prohibited_elements"]
    permitted_lines = "\n".join(f"- `{item}`" for item in permitted)
    prohibited_lines = (
        "\n".join(f"- `{item}`" for item in prohibited)
        if prohibited
        else "- None recorded."
    )
    payload_lines = "\n".join(
        f"| `{item.path}` | {item.purpose} |"
        for item in payloads
    )
    text = f"""# {profile.label} Qualified-Review Package

| Field | Value |
|---|---|
| Mapping-set identifier | `{profile.mapping_set_id}` |
| Direction | `{profile.direction}` |
| Candidate commit | `{commit}` |
| Candidate state | `{candidate_state}` |
| Expected provisions | {profile.expected_count} |
| Publication | {publication["name"]} |
| Source version | `{source_version["id"]}` ({source_version["label"]}) |
| Official URL | {source["official_url"]} |
| Access class | `{source["access_class"]}` |
| Historical control-source commit | `{release["source_commit_sha"]}` |
| Historical control-catalog SHA-256 | `{release["control_catalog_sha256"]}` |

## Recorded source checksums and additional locators

{source_reference_lines}

## Publication-rights boundary

**Basis:** {rights["basis"]}

**Permitted elements:**

{permitted_lines}

**Prohibited elements:**

{prohibited_lines}

**Restrictions:** {rights["restrictions"]}

External source documents are not included. The reviewer must independently
obtain authorized access to the exact source and attest to that access.

## Lifecycle and assurance boundary

{_lifecycle_boundary(candidate_state)}

## Payload inventory

| Path | Purpose |
|---|---|
{payload_lines}
"""
    return text.encode("utf-8")


def _lifecycle_boundary(candidate_state: CandidateState) -> str:
    if candidate_state == "draft":
        return (
            "This package does not establish qualified review, certification, "
            "compliance, equivalence, endorsement, approval, or assurance. "
            "The mapping remains Draft."
        )
    return (
        "This package records mapping content that is reviewed but is not "
        "approved, published, certified, compliant, equivalent, endorsed, "
        "or assured."
    )


def _validate_package_files(files: tuple[PackageFile, ...]) -> None:
    seen: set[str] = set()
    seen_casefolded: set[str] = set()
    for item in files:
        _canonical_relative_path(item.path, "package")
        if item.path in seen:
            raise ValueError(f"duplicate package path: {item.path}")
        seen.add(item.path)
        folded = item.path.casefold()
        if folded in seen_casefolded:
            raise ValueError(
                f"case-insensitive package path collision: {item.path}"
            )
        seen_casefolded.add(folded)


def _write_file_exclusively(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(content)


def _require_generator_execution_state(
    reader: GitReader,
    commit: str,
) -> None:
    if not isinstance(reader, GitReader) or reader.root != ROOT:
        raise ValueError("reader root must equal module checkout")
    GitReader(ROOT).require_candidate_execution_state(commit)


def assemble_package(
    reader: GitReader,
    commit: str,
    profile: MappingProfile,
    candidate_state: CandidateState = "draft",
) -> PackageAssembly:
    collected = list(
        collect_package_files(reader, commit, profile, candidate_state)
    )
    mapping_set_path = f"{profile.snapshot_path}/README.md"
    mapping_set_content = next(
        item.content for item in collected
        if item.path == mapping_set_path
    )
    collected.append(
        PackageFile(
            "PACKAGE_INDEX.md",
            b"",
            "package index",
        )
    )
    collected.sort(key=lambda item: item.path)
    _validate_package_files(tuple(collected))
    index_content = render_package_index(
        profile,
        commit,
        mapping_set_content,
        tuple(collected),
        candidate_state,
    )
    collected = [
        (
            PackageFile(item.path, index_content, item.purpose)
            if item.path == "PACKAGE_INDEX.md"
            else item
        )
        for item in collected
    ]
    manifest_files: list[dict[str, object]] = []
    for item in collected:
        manifest_files.append(
            {
                "path": item.path,
                "purpose": item.purpose,
                "bytes": len(item.content),
                "sha256": hashlib.sha256(item.content).hexdigest(),
            }
        )
    manifest: dict[str, object] = {
        "schema_version": "1.1.0",
        "generator_version": GENERATOR_VERSION,
        "mapping_set_id": profile.mapping_set_id,
        "package_label": profile.label,
        "direction": profile.direction,
        "expected_provision_count": profile.expected_count,
        "candidate_commit": commit,
        "candidate_state": candidate_state,
        "generator_commit": commit,
        "files": manifest_files,
    }
    manifest_content = canonical_json_bytes(manifest)
    return PackageAssembly(tuple(collected), manifest, manifest_content)


def write_package(
    reader: GitReader,
    commit: str,
    profile: MappingProfile,
    output: Path,
    candidate_state: CandidateState = "draft",
) -> dict[str, object]:
    _require_generator_execution_state(reader, commit)
    destination = validate_output_directory(output, reader.worktree_roots())
    assembly = assemble_package(reader, commit, profile, candidate_state)

    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.staging-",
            dir=destination.parent,
        )
    )
    for item in assembly.payloads:
        relative = _canonical_relative_path(item.path, "package")
        target = staging.joinpath(*relative.parts)
        if not _is_within(target.resolve(), staging.resolve()):
            raise ValueError(f"unsafe package path: {item.path}")
        _write_file_exclusively(target, item.content)
    _write_file_exclusively(
        staging / "PACKAGE_MANIFEST.json",
        assembly.manifest_bytes,
    )
    _require_generator_execution_state(reader, commit)
    if os.path.lexists(destination):
        raise ValueError("output appeared while package was being assembled")
    staging.rename(destination)
    return assembly.manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True)
    parser.add_argument("--mapping-set-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--candidate-state",
        choices=("draft", "reviewed"),
        default="draft",
    )
    try:
        args = parser.parse_args(argv)
    except SystemExit as error:
        return int(error.code)
    try:
        reader = GitReader(ROOT)
        commit = reader.resolve_commit(args.commit)
        try:
            profile = PROFILES[args.mapping_set_id]
        except KeyError as error:
            raise ValueError("unsupported mapping-set identifier") from error
        output = validate_output_directory(
            args.output, reader.worktree_roots()
        )
        write_package(reader, commit, profile, output, args.candidate_state)
        report = {
            "candidate_commit": commit,
            "mapping_set_id": profile.mapping_set_id,
            "output": str(output),
            "manifest_sha256": hashlib.sha256(
                (output / "PACKAGE_MANIFEST.json").read_bytes()
            ).hexdigest(),
        }
        print(json.dumps(report, sort_keys=True))
        return 0
    except Exception as error:
        print(error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
