from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

import yaml

import tools.build_mapping_review_bundle as bundle_builder
import tools.validate_crosswalks as crosswalk_validator
import tools.crosswalks.catalog as crosswalk_catalog
import tools.crosswalks.manifest as crosswalk_manifest
from tools.build_mapping_review_bundle import (
    PROFILES,
    GitReader,
    MappingProfile,
    PackageFile,
    assemble_package,
    collect_package_files,
    main,
    parse_front_matter_bytes,
    validate_output_directory,
    write_package,
)
from tools.crosswalks.digests import snapshot_digest_from_files


ROOT = Path(__file__).resolve().parents[1]
PLAN = (
    ROOT
    / "docs/superpowers/plans/2026-07-23-uk-qualified-review-preparation.md"
)
CORE_ID = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure"
    "--3.3--esaf-0.4-alpha--0.1.0"
)
PLUS_FORWARD_ID = (
    "uk-ncsc--cyber-essentials-plus-test-specification"
    "--3.2--esaf-0.4-alpha--0.1.0"
)
PLUS_REVERSE_ID = (
    "uk-ncsc--cyber-essentials-plus-test-specification"
    "--3.2--esaf-0.4-alpha--0.2.0"
)
EXPECTED_SOURCE_EVIDENCE = {
    CORE_ID: (
        "e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923",
    ),
    PLUS_FORWARD_ID: (
        "docs/superpowers/specs/"
        "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json",
        "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc",
        "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8",
        "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694",
        "https://www.ncsc.gov.uk/cyberessentials/resources",
        "https://www.ncsc.gov.uk/files/"
        "cyber-essentials-plus-test-specification-v3-2.pdf",
    ),
    PLUS_REVERSE_ID: (
        "docs/superpowers/specs/"
        "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json",
        "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc",
        "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8",
        "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694",
        "https://www.ncsc.gov.uk/cyberessentials/resources",
        "https://www.ncsc.gov.uk/files/"
        "cyber-essentials-plus-test-specification-v3-2.pdf",
    ),
}


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _create_clean_repository(parent: Path) -> tuple[Path, str]:
    repository = parent / "repository"
    repository.mkdir()
    _git(repository, "init")
    _git(repository, "config", "user.name", "ESAF Test")
    _git(repository, "config", "user.email", "esaf-test@example.invalid")
    (repository / "tracked.txt").write_text("baseline\n", encoding="utf-8")
    _git(repository, "add", "tracked.txt")
    _git(repository, "commit", "-m", "test baseline")
    return repository, _git(repository, "rev-parse", "HEAD")


class _FakeReadPipe:
    def __init__(
        self,
        chunks: tuple[bytes | BaseException, ...],
        *,
        close_failure: OSError | None = None,
    ) -> None:
        self._chunks = list(chunks)
        self.closed = False
        self.close_failure = close_failure

    def read(self, _size: int) -> bytes:
        if not self._chunks:
            return b""
        item = self._chunks.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item

    def close(self) -> None:
        self.closed = True
        if self.close_failure is not None:
            raise self.close_failure


class _FakeWritePipe:
    def __init__(
        self,
        *,
        maximum_write: int | None = None,
        failure: BaseException | None = None,
        close_failure: OSError | None = None,
    ) -> None:
        self.maximum_write = maximum_write
        self.failure = failure
        self.close_failure = close_failure
        self.content = bytearray()
        self.closed = False
        self.events: list[str] | None = None

    def write(self, value: bytes | memoryview) -> int:
        if self.events is not None:
            self.events.append("stdin-write")
        if self.failure is not None:
            raise self.failure
        count = len(value)
        if self.maximum_write is not None:
            count = min(count, self.maximum_write)
        self.content.extend(bytes(value[:count]))
        return count

    def flush(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True
        if self.close_failure is not None:
            raise self.close_failure


class _FakeProcess:
    def __init__(
        self,
        stdout: tuple[bytes | BaseException, ...] = (),
        stderr: tuple[bytes | BaseException, ...] = (),
        *,
        returncode: int = 0,
        stdin: _FakeWritePipe | None = None,
        timeout_once: bool = False,
    ) -> None:
        self.stdin = stdin or _FakeWritePipe()
        self.stdout = _FakeReadPipe(stdout)
        self.stderr = _FakeReadPipe(stderr)
        self.returncode = returncode
        self.timeout_once = timeout_once
        self.wait_calls = 0
        self.wait_timeouts: list[float | None] = []
        self.terminated = False
        self.killed = False

    def wait(self, timeout: float | None = None) -> int:
        self.wait_calls += 1
        self.wait_timeouts.append(timeout)
        if self.timeout_once and self.wait_calls == 1:
            raise subprocess.TimeoutExpired(["git"], timeout)
        return self.returncode

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True


class _BlockingWritePipe(_FakeWritePipe):
    def __init__(self, released: threading.Event) -> None:
        super().__init__()
        self.released = released
        self.entered = threading.Event()
        self.exited = threading.Event()
        self.writer: threading.Thread | None = None

    def write(self, value: bytes | memoryview) -> int:
        self.writer = threading.current_thread()
        self.entered.set()
        self.released.wait(timeout=5)
        self.exited.set()
        raise BrokenPipeError("host-secret")


class _BlockingReadPipe(_FakeReadPipe):
    def __init__(self) -> None:
        super().__init__(())
        self.entered = threading.Event()
        self.released = threading.Event()
        self.returned_chunk = False

    def read(self, _size: int) -> bytes:
        self.entered.set()
        self.released.wait(timeout=5)
        if not self.returned_chunk:
            self.returned_chunk = True
            return b"late"
        return b""

    def close(self) -> None:
        self.closed = True
        self.released.set()


class _ScriptedProcess(_FakeProcess):
    def __init__(
        self,
        wait_outcomes: list[int | BaseException],
        *,
        stdin: _FakeWritePipe | None = None,
        stdout: _FakeReadPipe | None = None,
    ) -> None:
        super().__init__(stdin=stdin)
        if stdout is not None:
            self.stdout = stdout
        self.wait_outcomes = list(wait_outcomes)
        self.signal = threading.Event()

    def wait(self, timeout: float | None = None) -> int:
        self.wait_calls += 1
        self.wait_timeouts.append(timeout)
        outcome = self.wait_outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        self.returncode = outcome
        return outcome

    def terminate(self) -> None:
        super().terminate()
        self.signal.set()

    def kill(self) -> None:
        super().kill()
        self.signal.set()


class _ObservedSpool(io.BytesIO):
    def __init__(self, *, close_failure: OSError | None = None) -> None:
        super().__init__()
        self.close_failure = close_failure
        self.close_calls = 0
        self.write_after_close = False

    def write(self, value: bytes) -> int:
        if self.closed:
            self.write_after_close = True
        return super().write(value)

    def close(self) -> None:
        self.close_calls += 1
        super().close()
        if self.close_failure is not None:
            raise self.close_failure


def _popen_sequence(
    processes: list[_FakeProcess],
    calls: list[tuple[tuple[object, ...], dict[str, object]]],
):
    def start(*arguments: object, **keywords: object) -> _FakeProcess:
        calls.append((arguments, keywords))
        return processes.pop(0)

    return start


class FiniteGitCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = GitReader(ROOT)
        self.started_threads: list[threading.Thread] = []

    def _run_with_process(
        self,
        process: _FakeProcess,
        *,
        input_bytes: bytes = b"",
        stdout_limit: int = 1024,
        stderr_limit: int = 1024,
    ):
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        events: list[str] = []
        process.stdin.events = events
        original_start = threading.Thread.start

        def record_start(thread: threading.Thread) -> None:
            events.append("drainer-start")
            self.started_threads.append(thread)
            original_start(thread)

        with mock.patch(
            "tools.build_mapping_review_bundle.subprocess.Popen",
            side_effect=_popen_sequence([process], calls),
        ), mock.patch(
            "tools.build_mapping_review_bundle.threading.Thread.start",
            new=record_start,
        ):
            result = self.reader._run_finite_git(
                ("status", "--porcelain=v1"),
                input_bytes=input_bytes,
                stdout_limit=stdout_limit,
                stderr_limit=stderr_limit,
            )
        return result, calls, events

    def test_success_drains_before_input_and_closes_every_pipe(self) -> None:
        stdin = _FakeWritePipe(maximum_write=2)
        process = _FakeProcess((b"clean",), (), stdin=stdin)

        result, calls, events = self._run_with_process(process, input_bytes=b"abcdef")

        self.assertEqual(result.stdout, b"clean")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(stdin.content, b"abcdef")
        self.assertEqual(events[:2], ["drainer-start", "drainer-start"])
        self.assertGreaterEqual(events.index("stdin-write"), 2)
        self.assertTrue(stdin.closed)
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)
        self.assertTrue(all(not thread.is_alive() for thread in self.started_threads))
        command = calls[0][0][0]
        self.assertEqual(
            command[:5],
            ["git", "--no-replace-objects", "-c", "core.fsmonitor=false", "-C"],
        )
        self.assertEqual(command[5], str(ROOT.resolve()))
        self.assertFalse(calls[0][1]["shell"])
        self.assertIs(calls[0][1]["stdin"], subprocess.PIPE)
        self.assertIs(calls[0][1]["stdout"], subprocess.PIPE)
        self.assertIs(calls[0][1]["stderr"], subprocess.PIPE)

    def test_child_environment_is_sanitized_and_frozen(self) -> None:
        # Mutations caught: leaked GIT_*, omitted fixed environment values, and
        # missing command-prefix options. Other tests below cover non-SHA-1
        # storage and repeated commit resolution.
        ambient = {
            "GIT_DIR": "host-secret-dir",
            "GIT_GRAFT_FILE": "host-secret-graft",
            "git_object_directory": "host-secret-objects",
            "Git_AlternATE_Object_Directories": "host-secret-alternates",
            "ESAF_SENTINEL": "preserved",
        }
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        process = _FakeProcess()
        with mock.patch.dict(os.environ, ambient, clear=False):
            reader = GitReader(ROOT)
            with mock.patch(
                "tools.build_mapping_review_bundle.subprocess.Popen",
                side_effect=_popen_sequence([process], calls),
            ):
                reader._run_finite_git(("status",), stdout_limit=64)
        environment = calls[0][1]["env"]
        self.assertEqual(environment["ESAF_SENTINEL"], "preserved")
        self.assertFalse(
            any(
                name.upper().startswith("GIT_")
                and name not in {
                    "GIT_NO_REPLACE_OBJECTS",
                    "GIT_NO_LAZY_FETCH",
                    "GIT_OPTIONAL_LOCKS",
                    "GIT_TERMINAL_PROMPT",
                }
                for name in environment
            )
        )
        self.assertEqual(
            {
                name: environment[name]
                for name in (
                    "GIT_NO_REPLACE_OBJECTS",
                    "GIT_NO_LAZY_FETCH",
                    "GIT_OPTIONAL_LOCKS",
                    "GIT_TERMINAL_PROMPT",
                    "LC_ALL",
                    "LANG",
                )
            },
            {
                "GIT_NO_REPLACE_OBJECTS": "1",
                "GIT_NO_LAZY_FETCH": "1",
                "GIT_OPTIONAL_LOCKS": "0",
                "GIT_TERMINAL_PROMPT": "0",
                "LC_ALL": "C",
                "LANG": "C",
            },
        )
        self.assertGreater(process.wait_timeouts[0], 0)
        self.assertLessEqual(process.wait_timeouts[0], 120)

    def test_failures_are_sanitized_and_cleanup_is_deterministic(self) -> None:
        cases = (
            ("nonzero", _FakeProcess(returncode=7), 1024, 1024),
            ("stderr", _FakeProcess((), (b"host-secret",)), 1024, 1024),
            ("stdout-overflow", _FakeProcess((b"12345",)), 4, 1024),
            ("stderr-overflow", _FakeProcess((), (b"12345",)), 1024, 4),
            ("read-error", _FakeProcess((OSError("host-secret"),)), 1024, 1024),
            ("timeout", _FakeProcess(timeout_once=True), 1024, 1024),
        )
        for label, process, stdout_limit, stderr_limit in cases:
            with self.subTest(label=label):
                with self.assertRaises(bundle_builder.GitObjectReadError) as raised:
                    self._run_with_process(
                        process,
                        stdout_limit=stdout_limit,
                        stderr_limit=stderr_limit,
                    )
                self.assertEqual(str(raised.exception), "Git object read failed")
                self.assertNotIn("host-secret", str(raised.exception))
                self.assertTrue(process.stdin.closed)
                self.assertTrue(process.stdout.closed)
                self.assertTrue(process.stderr.closed)
                self.assertTrue(all(not thread.is_alive() for thread in self.started_threads))
                self.assertGreaterEqual(process.wait_calls, 1)
                if label in {"stdout-overflow", "stderr-overflow", "timeout"}:
                    self.assertTrue(process.terminated or process.killed)

    def test_input_failures_close_and_reap_the_child(self) -> None:
        for label, failure in (
            ("broken-pipe", BrokenPipeError("host-secret")),
            ("write-error", OSError("host-secret")),
        ):
            with self.subTest(label=label):
                process = _FakeProcess(stdin=_FakeWritePipe(failure=failure))
                with self.assertRaises(bundle_builder.GitObjectReadError):
                    self._run_with_process(process, input_bytes=b"request\n")
                self.assertTrue(process.stdin.closed)
                self.assertTrue(process.stdout.closed)
                self.assertTrue(process.stderr.closed)
                self.assertTrue(all(not thread.is_alive() for thread in self.started_threads))
                self.assertGreaterEqual(process.wait_calls, 1)

    def test_temporary_spools_close_on_success_and_failure(self) -> None:
        for label, process in (
            ("success", _FakeProcess((b"ok",))),
            ("failure", _FakeProcess((), (b"host-secret",))),
        ):
            with self.subTest(label=label):
                spools: list[io.BytesIO] = []

                def make_spool(*_arguments: object, **_keywords: object) -> io.BytesIO:
                    spool = io.BytesIO()
                    spools.append(spool)
                    return spool

                calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
                with mock.patch(
                    "tools.build_mapping_review_bundle.subprocess.Popen",
                    side_effect=_popen_sequence([process], calls),
                ), mock.patch(
                    "tools.build_mapping_review_bundle.tempfile.SpooledTemporaryFile",
                    side_effect=make_spool,
                ):
                    if label == "success":
                        self.reader._run_finite_git(("status",), stdout_limit=64)
                    else:
                        with self.assertRaises(bundle_builder.GitObjectReadError):
                            self.reader._run_finite_git(("status",), stdout_limit=64)
                self.assertEqual(len(spools), 2)
                self.assertTrue(all(spool.closed for spool in spools))

    def test_drainer_start_failure_still_terminates_and_reaps_child(self) -> None:
        process = _FakeProcess()
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        original_start = threading.Thread.start
        starts = 0

        def fail_second_start(thread: threading.Thread) -> None:
            nonlocal starts
            starts += 1
            if starts == 2:
                raise OSError("host-secret")
            original_start(thread)

        with mock.patch(
            "tools.build_mapping_review_bundle.subprocess.Popen",
            side_effect=_popen_sequence([process], calls),
        ), mock.patch(
            "tools.build_mapping_review_bundle.threading.Thread.start",
            new=fail_second_start,
        ):
            with self.assertRaisesRegex(
                bundle_builder.GitObjectReadError,
                "^Git object read failed$",
            ) as raised:
                self.reader._run_finite_git(("status",), stdout_limit=64)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)
        self.assertTrue(process.terminated or process.killed)
        self.assertGreaterEqual(process.wait_calls, 1)
        self.assertTrue(process.stdin.closed)
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)

    def test_deadline_covers_a_blocked_stdin_write_and_joins_writer(self) -> None:
        released = threading.Event()
        stdin = _BlockingWritePipe(released)
        process = _ScriptedProcess(
            [subprocess.TimeoutExpired(["git"], 120), 0],
            stdin=stdin,
        )
        process.signal = released
        errors: list[BaseException] = []
        started: list[threading.Thread] = []
        original_start = threading.Thread.start

        def record_start(thread: threading.Thread) -> None:
            started.append(thread)
            original_start(thread)

        def invoke() -> None:
            try:
                self.reader._run_finite_git(
                    ("hash-object", "--stdin"),
                    input_bytes=b"request\n",
                    stdout_limit=64,
                )
            except BaseException as error:
                errors.append(error)

        caller = threading.Thread(target=invoke)
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        with mock.patch(
            "tools.build_mapping_review_bundle.subprocess.Popen",
            side_effect=_popen_sequence([process], calls),
        ), mock.patch(
            "tools.build_mapping_review_bundle.threading.Thread.start",
            new=record_start,
        ):
            caller.start()
            try:
                self.assertTrue(stdin.entered.wait(timeout=1))
                automatically_released = released.wait(timeout=0.5)
            finally:
                released.set()
                caller.join(timeout=2)

        self.assertTrue(automatically_released)
        self.assertFalse(caller.is_alive())
        self.assertTrue(stdin.exited.is_set())
        self.assertIsNot(stdin.writer, caller)
        self.assertIsInstance(errors[0], bundle_builder.GitObjectReadError)
        self.assertEqual(str(errors[0]), "Git object read failed")
        self.assertFalse(stdin.writer.is_alive())
        self.assertGreaterEqual(len(started), 4)
        self.assertTrue(all(not thread.is_alive() for thread in started))

    def test_second_spool_allocation_failure_closes_first_spool(self) -> None:
        first_spool = _ObservedSpool()
        allocations = [first_spool, OSError("host-secret")]

        def make_spool(*_arguments: object, **_keywords: object) -> _ObservedSpool:
            outcome = allocations.pop(0)
            if isinstance(outcome, OSError):
                raise outcome
            return outcome

        with mock.patch(
            "tools.build_mapping_review_bundle.tempfile.SpooledTemporaryFile",
            side_effect=make_spool,
        ):
            with self.assertRaisesRegex(
                bundle_builder.GitObjectReadError,
                "^Git object read failed$",
            ):
                self.reader._run_finite_git(("status",), stdout_limit=64)
        self.assertTrue(first_spool.closed)
        self.assertGreaterEqual(first_spool.close_calls, 1)

    def test_close_failures_are_sanitized_and_close_remaining_resources(self) -> None:
        for subject in ("stdin", "stdout", "stderr", "stdout-spool", "stderr-spool"):
            with self.subTest(subject=subject):
                stdin = _FakeWritePipe(
                    close_failure=OSError("host-secret") if subject == "stdin" else None
                )
                process = _FakeProcess(stdin=stdin)
                if subject == "stdout":
                    process.stdout.close_failure = OSError("host-secret")
                if subject == "stderr":
                    process.stderr.close_failure = OSError("host-secret")
                spools = [
                    _ObservedSpool(
                        close_failure=(
                            OSError("host-secret") if subject == "stdout-spool" else None
                        )
                    ),
                    _ObservedSpool(
                        close_failure=(
                            OSError("host-secret") if subject == "stderr-spool" else None
                        )
                    ),
                ]
                calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
                with mock.patch(
                    "tools.build_mapping_review_bundle.subprocess.Popen",
                    side_effect=_popen_sequence([process], calls),
                ), mock.patch(
                    "tools.build_mapping_review_bundle.tempfile.SpooledTemporaryFile",
                    side_effect=spools,
                ):
                    with self.assertRaisesRegex(
                        bundle_builder.GitObjectReadError,
                        "^Git object read failed$",
                    ) as raised:
                        self.reader._run_finite_git(("status",), stdout_limit=64)
                self.assertIsNone(raised.exception.__cause__)
                self.assertIsNone(raised.exception.__context__)
                self.assertTrue(stdin.closed)
                self.assertTrue(process.stdout.closed)
                self.assertTrue(process.stderr.closed)
                self.assertTrue(all(spool.closed for spool in spools))
                self.assertTrue(all(spool.close_calls >= 1 for spool in spools))

    def test_terminal_cleanup_kills_retries_reap_and_unblocks_drainer(self) -> None:
        blocked_stdout = _BlockingReadPipe()
        process = _ScriptedProcess(
            [
                subprocess.TimeoutExpired(["git"], 120),
                subprocess.TimeoutExpired(["git"], 5),
                subprocess.TimeoutExpired(["git"], 5),
                0,
            ],
            stdout=blocked_stdout,
        )
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        started: list[threading.Thread] = []
        spools = [_ObservedSpool(), _ObservedSpool()]
        original_start = threading.Thread.start

        def record_start(thread: threading.Thread) -> None:
            started.append(thread)
            original_start(thread)

        started_at = time.monotonic()
        with mock.patch(
            "tools.build_mapping_review_bundle.subprocess.Popen",
            side_effect=_popen_sequence([process], calls),
        ), mock.patch(
            "tools.build_mapping_review_bundle.tempfile.SpooledTemporaryFile",
            side_effect=spools,
        ), mock.patch(
            "tools.build_mapping_review_bundle.threading.Thread.start",
            new=record_start,
        ):
            with self.assertRaisesRegex(
                bundle_builder.GitObjectReadError,
                "^Git object read failed$",
            ):
                self.reader._run_finite_git(("status",), stdout_limit=64)
        elapsed = time.monotonic() - started_at

        self.assertLess(elapsed, 1)
        self.assertTrue(process.terminated)
        self.assertTrue(process.killed)
        self.assertGreaterEqual(process.wait_calls, 4)
        self.assertTrue(blocked_stdout.closed)
        self.assertTrue(blocked_stdout.released.is_set())
        self.assertTrue(all(not thread.is_alive() for thread in started))
        self.assertTrue(all(spool.closed for spool in spools))
        self.assertTrue(all(not spool.write_after_close for spool in spools))


class GitRepositoryBindingTests(unittest.TestCase):
    def test_exact_commit_resolution_checks_sha1_once_and_caches_success(self) -> None:
        head = "1" * 40
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        processes = [
            _FakeProcess((b"sha1\n",)),
            _FakeProcess((head.encode("ascii") + b"\n",)),
        ]
        reader = GitReader(ROOT)
        with mock.patch(
            "tools.build_mapping_review_bundle.subprocess.Popen",
            side_effect=_popen_sequence(processes, calls),
        ):
            self.assertEqual(reader.resolve_commit(head), head)
            self.assertEqual(reader.resolve_commit(head), head)
        commands = [call[0][0] for call in calls]
        self.assertEqual(commands[0][-2:], ["rev-parse", "--show-object-format=storage"])
        self.assertEqual(
            commands[1][-3:],
            ["rev-parse", "--verify", f"{head}^{{commit}}"],
        )
        self.assertEqual(len(commands), 2)

    def test_non_sha1_storage_fails_closed(self) -> None:
        reader = GitReader(ROOT)
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        with mock.patch(
            "tools.build_mapping_review_bundle.subprocess.Popen",
            side_effect=_popen_sequence([_FakeProcess((b"sha256\n",))], calls),
        ):
            with self.assertRaises(bundle_builder.GitObjectReadError):
                reader.resolve_commit("1" * 40)
        self.assertEqual(len(calls), 1)

    def test_replacement_refs_and_ambient_repository_redirects_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, original = _create_clean_repository(Path(directory))
            (repository / "tracked.txt").write_text("replacement\n", encoding="utf-8")
            _git(repository, "commit", "-am", "replacement")
            replacement = _git(repository, "rev-parse", "HEAD")
            _git(repository, "replace", original, replacement)
            with mock.patch.dict(
                os.environ,
                {
                    "GIT_DIR": str(repository / ".git"),
                    "GIT_WORK_TREE": str(repository),
                    "GIT_REPLACE_REF_BASE": "refs/replace/",
                },
                clear=False,
            ):
                content = GitReader(repository).read_bytes(original, "tracked.txt")
        self.assertEqual(content, b"baseline\n")

    def test_graft_file_cannot_change_ancestry_command(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, parent = _create_clean_repository(Path(directory))
            (repository / "tracked.txt").write_text("second\n", encoding="utf-8")
            _git(repository, "commit", "-am", "second")
            child = _git(repository, "rev-parse", "HEAD")
            graft = Path(directory) / "grafts"
            graft.write_text(f"{child}\n", encoding="ascii")
            with mock.patch.dict(os.environ, {"GIT_GRAFT_FILE": str(graft)}, clear=False):
                result = GitReader(repository)._run_finite_git(
                    ("rev-list", "--parents", "-n", "1", child),
                    stdout_limit=256,
                )
        self.assertEqual(result.stdout, f"{child} {parent}\n".encode("ascii"))

    def test_execution_state_and_worktrees_use_bounded_binary_commands(self) -> None:
        head = "1" * 40
        root_bytes = str(ROOT.resolve()).encode("utf-8")
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        processes = (
            _FakeProcess((b"sha1\n",)),
            _FakeProcess((head.encode("ascii") + b"\n",)),
            _FakeProcess((head.encode("ascii") + b"\n",)),
            _FakeProcess(),
            _FakeProcess((b"worktree " + root_bytes + b"\0",)),
        )
        reader = GitReader(ROOT)
        with mock.patch(
            "tools.build_mapping_review_bundle.subprocess.Popen",
            side_effect=_popen_sequence(list(processes), calls),
        ), mock.patch.object(
            reader,
            "_run_finite_git",
            wraps=reader._run_finite_git,
        ) as finite_git:
            reader.require_candidate_execution_state(head)
            self.assertEqual(reader.worktree_roots(), (ROOT.resolve(),))
        commands = [call[0][0] for call in calls]
        self.assertEqual(commands[2][-2:], ["rev-parse", "HEAD"])
        self.assertEqual(commands[3][-4:], [
            "status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=none",
        ])
        self.assertEqual(commands[4][-4:], ["worktree", "list", "--porcelain", "-z"])
        self.assertTrue(all("text" not in call[1] for call in calls))
        self.assertTrue(all(call[1]["env"] == reader._git_environment for call in calls))
        self.assertTrue(
            all(0 < process.wait_timeouts[0] <= 120 for process in processes)
        )
        self.assertEqual(
            [call.kwargs["stdout_limit"] for call in finite_git.call_args_list],
            [16, 41, 41, 8 * 1024 * 1024, 8 * 1024 * 1024],
        )


def _tree_record(
    path: bytes,
    *,
    mode: bytes = b"100644",
    object_type: bytes = b"blob",
    object_id: bytes = b"1111111111111111111111111111111111111111",
) -> bytes:
    return mode + b" " + object_type + b" " + object_id + b"\t" + path


def _reader_with_verified_commit(commit: str = "a" * 40) -> GitReader:
    reader = GitReader(ROOT)
    reader._sha1_verified = True
    reader._verified_commits.add(commit)
    return reader


def _blob_oid(content: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(content)).encode("ascii") + b"\0" + content
    ).hexdigest()


def _reader_with_blob_entries(
    entries: tuple[tuple[str, bytes], ...],
    *,
    commit: str = "a" * 40,
) -> tuple[GitReader, dict[str, bytes]]:
    reader = _reader_with_verified_commit(commit)
    contents: dict[str, bytes] = {}
    tree: dict[str, bundle_builder.TreeEntry] = {}
    for path, content in entries:
        object_id = _blob_oid(content)
        contents[object_id] = content
        tree[path] = bundle_builder.TreeEntry(path, "100644", "blob", object_id)
    reader._tree_indexes[commit] = tree
    return reader, contents


def _batch_check_response(
    object_ids: tuple[str, ...], contents: dict[str, bytes]
) -> bytes:
    return b"".join(
        f"{object_id} blob {len(contents[object_id])}\n".encode("ascii")
        for object_id in object_ids
    )


def _batch_content_response(
    object_ids: tuple[str, ...], contents: dict[str, bytes]
) -> bytes:
    return b"".join(
        f"{object_id} blob {len(contents[object_id])}\n".encode("ascii")
        + contents[object_id]
        + b"\n"
        for object_id in object_ids
    )


class GitReadManyInputTests(unittest.TestCase):
    def test_freezes_mutable_sequence_before_tree_lookup(self) -> None:
        commit = "a" * 40
        reader, contents = _reader_with_blob_entries(
            (("one", b"one"),), commit=commit
        )
        paths = ["one"]

        def tree_index(_commit: str):
            paths.append("injected")
            return reader._tree_indexes[commit]

        object_id = next(iter(contents))
        responses = (
            bundle_builder._GitCommandResult(
                _batch_check_response((object_id,), contents), b""
            ),
            bundle_builder._GitCommandResult(
                _batch_content_response((object_id,), contents), b""
            ),
        )
        with mock.patch.object(
            reader, "_tree_index", side_effect=tree_index
        ), mock.patch.object(
            reader, "_run_finite_git", side_effect=responses
        ):
            self.assertEqual(reader.read_many(commit, paths), {"one": b"one"})

    def test_empty_sequence_returns_without_git(self) -> None:
        reader = GitReader(ROOT)
        with mock.patch.object(reader, "_run_finite_git") as finite_git:
            self.assertEqual(reader.read_many("not-a-commit", ()), {})
        finite_git.assert_not_called()

    def test_rejects_non_sequence_and_invalid_path_sets_before_batching(self) -> None:
        commit = "a" * 40
        reader, _contents = _reader_with_blob_entries(
            (("one", b"one"),), commit=commit
        )
        cases = (
            ("one", TypeError),
            (b"one", TypeError),
            (("../one",), ValueError),
            (("one", "one"), ValueError),
            (tuple(f"path-{number}" for number in range(4097)), ValueError),
        )
        for paths, expected_type in cases:
            with self.subTest(paths_type=type(paths), count=len(paths)):
                with mock.patch.object(reader, "_run_finite_git") as finite_git:
                    with self.assertRaises(expected_type) as caught:
                        reader.read_many(commit, paths)  # type: ignore[arg-type]
                self.assertIs(type(caught.exception), expected_type)
                finite_git.assert_not_called()

    def test_rejects_missing_tree_and_nonregular_entries_before_batching(self) -> None:
        commit = "a" * 40
        reader, _contents = _reader_with_blob_entries(
            (("regular", b"ok"),), commit=commit
        )
        reader._tree_indexes[commit].update(
            {
                "directory": bundle_builder.TreeEntry(
                    "directory", "040000", "tree", "1" * 40
                ),
                "link": bundle_builder.TreeEntry(
                    "link", "120000", "blob", "2" * 40
                ),
                "module": bundle_builder.TreeEntry(
                    "module", "160000", "commit", "3" * 40
                ),
            }
        )
        for path in ("missing", "directory", "link", "module"):
            with self.subTest(path=path), mock.patch.object(
                reader, "_run_finite_git"
            ) as finite_git:
                with self.assertRaises(ValueError) as caught:
                    reader.read_many(commit, (path,))
                self.assertIs(type(caught.exception), ValueError)
                finite_git.assert_not_called()


class GitBatchCheckProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.commit = "a" * 40
        self.reader, self.contents = _reader_with_blob_entries(
            (("one", b"first"), ("two", b"second")), commit=self.commit
        )
        self.object_ids = tuple(self.contents)

    def test_uses_direct_oids_in_order_and_exact_preflight_limit(self) -> None:
        responses = (
            bundle_builder._GitCommandResult(
                _batch_check_response(self.object_ids, self.contents), b""
            ),
            bundle_builder._GitCommandResult(
                _batch_content_response(self.object_ids, self.contents), b""
            ),
        )
        with mock.patch.object(
            self.reader, "_run_finite_git", side_effect=responses
        ) as finite_git:
            self.assertEqual(
                self.reader.read_many(self.commit, ("one", "two")),
                {"one": b"first", "two": b"second"},
            )
        expected_input = "".join(
            f"{oid}\n" for oid in self.object_ids
        ).encode("ascii")
        self.assertEqual(
            finite_git.call_args_list[0].args[0],
            (
                "cat-file",
                "--batch-check=%(objectname) %(objecttype) %(objectsize)",
            ),
        )
        self.assertEqual(
            finite_git.call_args_list[0].kwargs["input_bytes"], expected_input
        )
        self.assertEqual(
            finite_git.call_args_list[0].kwargs["stdout_limit"], 4096 * 256
        )

    def test_rejects_each_malformed_preflight_without_content_command(self) -> None:
        first, second = self.object_ids
        valid = _batch_check_response(self.object_ids, self.contents)
        first_size = len(self.contents[first])
        cases = {
            "missing": valid.splitlines(keepends=True)[0],
            "missing terminal newline": valid[:-1],
            "CRLF separators": valid.replace(b"\n", b"\r\n"),
            "bare CR separator": valid.replace(b"\n", b"\r", 1),
            "extra": valid + valid.splitlines(keepends=True)[0],
            "reordered": _batch_check_response((second, first), self.contents),
            "wrong oid": valid.replace(first.encode(), b"f" * 40, 1),
            "wrong type": valid.replace(b" blob ", b" tree ", 1),
            "negative": valid.replace(f" {first_size}\n".encode(), b" -1\n", 1),
            "signed": valid.replace(
                f" {first_size}\n".encode(), f" +{first_size}\n".encode(), 1
            ),
            "zero padded": valid.replace(
                f" {first_size}\n".encode(), f" 0{first_size}\n".encode(), 1
            ),
            "nondecimal": valid.replace(f" {first_size}\n".encode(), b" x\n", 1),
        }
        for label, response in cases.items():
            with self.subTest(label=label):
                reader, _ = _reader_with_blob_entries(
                    (("one", b"first"), ("two", b"second")), commit=self.commit
                )
                with mock.patch.object(
                    reader,
                    "_run_finite_git",
                    return_value=bundle_builder._GitCommandResult(response, b""),
                ) as finite_git:
                    with self.assertRaises(
                        bundle_builder.GitObjectReadError
                    ) as caught:
                        reader.read_many(self.commit, ("one", "two"))
                self.assertIs(
                    type(caught.exception), bundle_builder.GitObjectReadError
                )
                self.assertEqual(str(caught.exception), "Git object read failed")
                self.assertEqual(finite_git.call_count, 1)

    def test_declared_blob_size_limit_remains_a_value_error(self) -> None:
        first = self.object_ids[0]
        valid = _batch_check_response(self.object_ids, self.contents)
        oversized = valid.replace(
            f" {len(self.contents[first])}\n".encode(), b" 33554433\n", 1
        )
        with mock.patch.object(
            self.reader,
            "_run_finite_git",
            return_value=bundle_builder._GitCommandResult(oversized, b""),
        ) as finite_git:
            with self.assertRaisesRegex(ValueError, "blob size limit") as caught:
                self.reader.read_many(self.commit, ("one", "two"))
        self.assertIs(type(caught.exception), ValueError)
        self.assertEqual(finite_git.call_count, 1)

    def test_logical_limit_counts_aliases_and_cache_hits(self) -> None:
        aliases = tuple((f"alias-{number}", b"x") for number in range(5))
        reader, _ = _reader_with_blob_entries(aliases, commit=self.commit)
        oid = _blob_oid(b"x")
        reader._object_cache[(self.commit, oid)] = b"x" * (32 * 1024 * 1024)
        reader._object_cache_size = len(reader._object_cache[(self.commit, oid)])
        with mock.patch.object(reader, "_run_finite_git") as finite_git:
            with self.assertRaisesRegex(ValueError, "logical content") as caught:
                reader.read_many(
                    self.commit, tuple(path for path, _content in aliases)
                )
        self.assertIs(type(caught.exception), ValueError)
        finite_git.assert_not_called()


class GitBatchContentProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.commit = "a" * 40
        self.content = b"\x00line\n\xfftail\n"
        self.reader, self.contents = _reader_with_blob_entries(
            (("binary", self.content),), commit=self.commit
        )
        self.object_id = next(iter(self.contents))

    def test_preserves_binary_payload_and_uses_bounded_content_command(self) -> None:
        responses = (
            bundle_builder._GitCommandResult(
                _batch_check_response((self.object_id,), self.contents), b""
            ),
            bundle_builder._GitCommandResult(
                _batch_content_response((self.object_id,), self.contents), b""
            ),
        )
        with mock.patch.object(
            self.reader, "_run_finite_git", side_effect=responses
        ) as finite_git:
            self.assertEqual(
                self.reader.read_many(self.commit, ("binary",)),
                {"binary": self.content},
            )
        content_call = finite_git.call_args_list[1]
        self.assertEqual(content_call.args[0], ("cat-file", "--batch"))
        self.assertEqual(
            content_call.kwargs["input_bytes"],
            (self.object_id + "\n").encode(),
        )
        self.assertEqual(
            content_call.kwargs["stdout_limit"],
            128 * 1024 * 1024 + 4096 * 257,
        )

    def test_failed_content_transactions_are_atomic_and_retryable(self) -> None:
        valid_check = _batch_check_response((self.object_id,), self.contents)
        valid_content = _batch_content_response((self.object_id,), self.contents)
        malformed = {
            "missing": b"",
            "extra": valid_content + b"extra",
            "wrong identity": valid_content.replace(
                self.object_id.encode(), b"f" * 40, 1
            ),
            "wrong type": valid_content.replace(b" blob ", b" tree ", 1),
            "size disagreement": valid_content.replace(
                f" {len(self.content)}\n".encode(),
                f" {len(self.content) + 1}\n".encode(),
                1,
            ),
            "size disagreement above blob limit": valid_content.replace(
                f" {len(self.content)}\n".encode(), b" 33554433\n", 1
            ),
            "long header": b"x" * 257 + b"\n" + self.content + b"\n",
            "truncated": valid_content[:-2],
            "missing delimiter": valid_content[:-1] + b"x",
            "hash mismatch": valid_content.replace(
                self.content, b"z" * len(self.content), 1
            ),
        }
        for label, bad_content in malformed.items():
            with self.subTest(label=label):
                reader, contents = _reader_with_blob_entries(
                    (("binary", self.content),), commit=self.commit
                )
                responses = (
                    bundle_builder._GitCommandResult(valid_check, b""),
                    bundle_builder._GitCommandResult(bad_content, b""),
                    bundle_builder._GitCommandResult(valid_check, b""),
                    bundle_builder._GitCommandResult(valid_content, b""),
                )
                with mock.patch.object(
                    reader, "_run_finite_git", side_effect=responses
                ) as finite_git:
                    with self.assertRaises(
                        bundle_builder.GitObjectReadError
                    ) as caught:
                        reader.read_many(self.commit, ("binary",))
                    self.assertIs(
                        type(caught.exception), bundle_builder.GitObjectReadError
                    )
                    self.assertEqual(
                        str(caught.exception), "Git object read failed"
                    )
                    self.assertEqual(
                        reader.read_many(self.commit, ("binary",)),
                        {"binary": contents[self.object_id]},
                    )
                self.assertEqual(finite_git.call_count, 4)

    def test_reordered_content_records_are_sanitized(self) -> None:
        reader, contents = _reader_with_blob_entries(
            (("one", b"first"), ("two", b"second")), commit=self.commit
        )
        object_ids = tuple(contents)
        responses = (
            bundle_builder._GitCommandResult(
                _batch_check_response(object_ids, contents), b""
            ),
            bundle_builder._GitCommandResult(
                _batch_content_response(tuple(reversed(object_ids)), contents),
                b"host-secret child detail",
            ),
        )
        with mock.patch.object(
            reader, "_run_finite_git", side_effect=responses
        ):
            with self.assertRaises(
                bundle_builder.GitObjectReadError
            ) as caught:
                reader.read_many(self.commit, ("one", "two"))
        self.assertIs(type(caught.exception), bundle_builder.GitObjectReadError)
        self.assertEqual(str(caught.exception), "Git object read failed")


class GitObjectCacheTests(unittest.TestCase):
    def test_same_commit_deduplicates_aliases_but_other_commit_fetches_again(
        self,
    ) -> None:
        first_commit = "a" * 40
        second_commit = "b" * 40
        reader, contents = _reader_with_blob_entries(
            (("one", b"shared"), ("alias", b"shared")), commit=first_commit
        )
        oid = next(iter(contents))
        reader._verified_commits.add(second_commit)
        reader._tree_indexes[second_commit] = {
            "other": bundle_builder.TreeEntry("other", "100644", "blob", oid)
        }
        response_pair = (
            bundle_builder._GitCommandResult(
                _batch_check_response((oid,), contents), b""
            ),
            bundle_builder._GitCommandResult(
                _batch_content_response((oid,), contents), b""
            ),
        )
        with mock.patch.object(
            reader, "_run_finite_git", side_effect=response_pair + response_pair
        ) as finite_git:
            self.assertEqual(
                reader.read_many(first_commit, ("one", "alias")),
                {"one": b"shared", "alias": b"shared"},
            )
            self.assertEqual(
                reader.read_many(second_commit, ("other",)),
                {"other": b"shared"},
            )
        self.assertEqual(finite_git.call_count, 4)
        self.assertEqual(
            finite_git.call_args_list[0].kwargs["input_bytes"],
            (oid + "\n").encode(),
        )

    def test_lru_touch_controls_eviction_at_128_mib(self) -> None:
        commit = "a" * 40
        reader = _reader_with_verified_commit(commit)
        unit = 32 * 1024 * 1024
        keys = [(commit, character * 40) for character in "12345"]
        reader._object_cache = bundle_builder.OrderedDict(
            (key, bytes([number]) * unit) for number, key in enumerate(keys[:4])
        )
        reader._object_cache_size = 128 * 1024 * 1024
        reader._cache_get(keys[0])
        reader._cache_publish({keys[4]: b"fifth"})
        self.assertNotIn(keys[1], reader._object_cache)
        self.assertIn(keys[0], reader._object_cache)
        self.assertEqual(reader._object_cache_size, unit * 3 + len(b"fifth"))

    def test_requested_cache_hit_is_retained_when_new_object_causes_eviction(
        self,
    ) -> None:
        commit = "a" * 40
        cached_content = b"x" * (32 * 1024 * 1024)
        new_content = b"new"
        cached_oid = _blob_oid(cached_content)
        new_oid = _blob_oid(new_content)
        reader = _reader_with_verified_commit(commit)
        reader._tree_indexes[commit] = {
            "cached": bundle_builder.TreeEntry(
                "cached", "100644", "blob", cached_oid
            ),
            "new": bundle_builder.TreeEntry("new", "100644", "blob", new_oid),
        }
        filler = b"f" * (32 * 1024 * 1024)
        reader._object_cache = bundle_builder.OrderedDict(
            [
                ((commit, cached_oid), cached_content),
                ((commit, "1" * 40), filler),
                ((commit, "2" * 40), filler),
                ((commit, "3" * 40), filler),
            ]
        )
        reader._object_cache_size = 128 * 1024 * 1024
        contents = {new_oid: new_content}
        responses = (
            bundle_builder._GitCommandResult(
                _batch_check_response((new_oid,), contents), b""
            ),
            bundle_builder._GitCommandResult(
                _batch_content_response((new_oid,), contents), b""
            ),
        )
        with mock.patch.object(reader, "_run_finite_git", side_effect=responses):
            self.assertEqual(
                reader.read_many(commit, ("cached", "new")),
                {"cached": cached_content, "new": new_content},
            )
        self.assertIn((commit, cached_oid), reader._object_cache)

    def test_read_bytes_is_singleton_delegation_and_no_legacy_runner_remains(self) -> None:
        reader = GitReader(ROOT)
        with mock.patch.object(
            reader, "read_many", return_value={"file": b"data"}
        ) as read_many:
            self.assertEqual(reader.read_bytes("a" * 40, "file"), b"data")
        read_many.assert_called_once_with("a" * 40, ("file",))
        self.assertNotIn("_run", GitReader.__dict__)
        source = Path(bundle_builder.__file__).read_text(encoding="utf-8")
        reader_start = source.index("class GitReader:")
        reader_end = source.index("\ndef _package_file", reader_start)
        reader_source = source[reader_start:reader_end]
        self.assertNotIn("subprocess.run(", reader_source)


class GitTreeIndexTests(unittest.TestCase):
    def test_real_tree_selection_is_exact_and_reuses_one_complete_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, _initial = _create_clean_repository(Path(directory))
            (repository / "tracked.txt").unlink()
            (repository / "foo").write_text("foo\n", encoding="utf-8")
            (repository / "foobar").mkdir()
            (repository / "foobar" / "item.txt").write_text(
                "item\n", encoding="utf-8"
            )
            (repository / "dir").mkdir()
            (repository / "dir" / "a.txt").write_text("a\n", encoding="utf-8")
            (repository / "dir" / "run.sh").write_text(
                "#!/bin/sh\n", encoding="utf-8"
            )
            (repository / "mixed").mkdir()
            (repository / "mixed" / "regular.txt").write_text(
                "regular\n", encoding="utf-8"
            )
            _git(repository, "add", "-A")
            _git(repository, "update-index", "--chmod=+x", "dir/run.sh")
            link_blob = _git(repository, "hash-object", "-w", "foo")
            _git(
                repository,
                "update-index",
                "--add",
                "--cacheinfo",
                f"120000,{link_blob},mixed/link",
            )
            _git(
                repository,
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{'2' * 40},vendor",
            )
            _git(repository, "commit", "-m", "complete tree fixture")
            head = _git(repository, "rev-parse", "HEAD")
            reader = GitReader(repository)

            with mock.patch.object(
                reader,
                "_run_finite_git",
                wraps=reader._run_finite_git,
            ) as finite_git:
                self.assertEqual(reader.list_files(head, "foo"), ("foo",))
                self.assertEqual(
                    reader.list_files(head, "dir"),
                    ("dir/a.txt", "dir/run.sh"),
                )
                self.assertEqual(reader.list_files(head, "missing"), ())
                with self.assertRaisesRegex(ValueError, "unexpected repository entry"):
                    reader.list_files(head, "mixed/link")
                with self.assertRaisesRegex(ValueError, "unexpected repository entry"):
                    reader.list_files(head, "vendor")
                with self.assertRaisesRegex(ValueError, "unexpected repository entry"):
                    reader.list_files(head, "mixed")
                self.assertEqual(
                    reader.list_files(head, "foobar"),
                    ("foobar/item.txt",),
                )

            tree_calls = [
                call
                for call in finite_git.call_args_list
                if call.args
                and call.args[0][:2] == ("ls-tree", "-r")
            ]
            self.assertEqual(len(tree_calls), 1)
            self.assertEqual(
                tree_calls[0].args[0],
                (
                    "ls-tree",
                    "-r",
                    "-t",
                    "-z",
                    "--full-tree",
                    "--abbrev=40",
                    head,
                ),
            )
            self.assertEqual(tree_calls[0].kwargs["stdout_limit"], 64 * 1024 * 1024)

    def test_published_tree_index_is_immutable(self) -> None:
        commit = "a" * 40
        reader = _reader_with_verified_commit(commit)
        result = bundle_builder._GitCommandResult(
            _tree_record(b"foo") + b"\0",
            b"",
        )
        with mock.patch.object(reader, "_run_finite_git", return_value=result):
            index = reader._tree_index(commit)
        with self.assertRaises(TypeError):
            index["bar"] = index["foo"]  # type: ignore[index]


class GitTreeProtocolTests(unittest.TestCase):
    def test_malformed_tree_transactions_are_not_published(self) -> None:
        commit = "a" * 40
        valid = _tree_record(b"foo") + b"\0"
        too_many = b"".join(
            _tree_record(f"f{number:06d}".encode("ascii")) + b"\0"
            for number in range(100_001)
        )
        malformed_cases = {
            "missing terminal NUL": _tree_record(b"foo"),
            "empty interior record": (
                _tree_record(b"foo") + b"\0\0" + _tree_record(b"bar") + b"\0"
            ),
            "malformed tab": (
                b"100644 blob " + b"1" * 40 + b" foo\0"
            ),
            "malformed header": b"100644  " + b"1" * 40 + b"\tfoo\0",
            "uppercase oid": _tree_record(b"foo", object_id=b"A" * 40) + b"\0",
            "abbreviated oid": _tree_record(b"foo", object_id=b"1" * 39) + b"\0",
            "invalid UTF-8": _tree_record(b"\xff") + b"\0",
            "control path": _tree_record(b"bad\nname") + b"\0",
            "C1 control path": _tree_record(b"bad\xc2\x80name") + b"\0",
            "unsafe path": _tree_record(b"../foo") + b"\0",
            "duplicate path": (
                _tree_record(b"foo") + b"\0" + _tree_record(b"foo") + b"\0"
            ),
            "missing parent tree": _tree_record(b"dir/a.txt") + b"\0",
            "parent is blob": (
                _tree_record(b"dir") + b"\0" + _tree_record(b"dir/a.txt") + b"\0"
            ),
            "descendant below non-tree": (
                _tree_record(b"a", mode=b"040000", object_type=b"tree")
                + b"\0"
                + _tree_record(b"a/b", mode=b"120000")
                + b"\0"
                + _tree_record(b"a/b/c")
                + b"\0"
            ),
            "invalid mode type": (
                _tree_record(b"foo", mode=b"100644", object_type=b"tree") + b"\0"
            ),
            "record limit": too_many,
        }
        for label, malformed in malformed_cases.items():
            with self.subTest(label=label):
                reader = _reader_with_verified_commit(commit)
                responses = [
                    bundle_builder._GitCommandResult(malformed, b""),
                    bundle_builder._GitCommandResult(valid, b""),
                ]
                with mock.patch.object(
                    reader,
                    "_run_finite_git",
                    side_effect=responses,
                ) as finite_git:
                    with self.assertRaises(ValueError):
                        reader._tree_index(commit)
                    self.assertEqual(reader.list_files(commit, "foo"), ("foo",))
                self.assertEqual(finite_git.call_count, 2)

    def test_tree_output_overflow_is_retryable_and_uses_the_hard_cap(self) -> None:
        commit = "a" * 40
        reader = _reader_with_verified_commit(commit)
        valid = bundle_builder._GitCommandResult(_tree_record(b"foo") + b"\0", b"")
        with mock.patch.object(
            reader,
            "_run_finite_git",
            side_effect=[
                bundle_builder.GitObjectReadError("Git object read failed"),
                valid,
            ],
        ) as finite_git:
            with self.assertRaises(bundle_builder.GitObjectReadError):
                reader._tree_index(commit)
            self.assertEqual(reader.list_files(commit, "foo"), ("foo",))
        self.assertEqual(finite_git.call_count, 2)
        self.assertTrue(
            all(
                call.kwargs["stdout_limit"] == 64 * 1024 * 1024
                for call in finite_git.call_args_list
            )
        )


class GitTreeIndexLimitTests(unittest.TestCase):
    def test_ninth_commit_is_rejected_without_tree_acquisition_or_eviction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, first = _create_clean_repository(Path(directory))
            commits = [first]
            for number in range(1, 9):
                (repository / "tracked.txt").write_text(
                    f"revision {number}\n", encoding="utf-8"
                )
                _git(repository, "commit", "-am", f"revision {number}")
                commits.append(_git(repository, "rev-parse", "HEAD"))

            reader = GitReader(repository)
            with mock.patch.object(
                reader,
                "_run_finite_git",
                wraps=reader._run_finite_git,
            ) as finite_git:
                for commit in commits[:8]:
                    self.assertEqual(
                        reader.list_files(commit, "tracked.txt"),
                        ("tracked.txt",),
                    )
                calls_after_eight_indexes = finite_git.call_count
                self.assertEqual(
                    reader.list_files(commits[0], "tracked.txt"),
                    ("tracked.txt",),
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "full lowercase 40-character Git SHA",
                ):
                    reader.list_files("HEAD", "tracked.txt")
                self.assertEqual(finite_git.call_count, calls_after_eight_indexes)

                self.assertNotIn(commits[8], reader._verified_commits)
                with self.assertRaisesRegex(ValueError, "tree index limit"):
                    reader.list_files(commits[8], "tracked.txt")
                self.assertEqual(finite_git.call_count, calls_after_eight_indexes)
                self.assertNotIn(commits[8], reader._verified_commits)
                with self.assertRaisesRegex(ValueError, "tree index limit"):
                    reader.read_bytes(commits[8], "tracked.txt")
                self.assertEqual(finite_git.call_count, calls_after_eight_indexes)
                self.assertNotIn(commits[8], reader._verified_commits)

            tree_calls = [
                call
                for call in finite_git.call_args_list
                if call.args and call.args[0][:2] == ("ls-tree", "-r")
            ]
            self.assertEqual(len(tree_calls), 8)


class GitReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = GitReader(ROOT)
        self.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()

    def test_profiles_are_exact_and_separate(self) -> None:
        self.assertEqual(
            {profile.expected_count for profile in PROFILES.values()},
            {116, 144},
        )
        self.assertEqual(len(PROFILES), 3)
        self.assertEqual(
            {
                mapping_set_id: profile.direction
                for mapping_set_id, profile in PROFILES.items()
            },
            {
                CORE_ID: "esaf_to_external",
                PLUS_FORWARD_ID: "esaf_to_external",
                PLUS_REVERSE_ID: "external_to_esaf",
            },
        )
        self.assertEqual(
            {profile.label for profile in PROFILES.values()},
            {"Core", "Plus forward", "Plus reverse"},
        )

    def test_implementation_plan_uses_authoritative_core_direction(self) -> None:
        self.assertIn(
            '"Core", "esaf_to_external", 116,',
            PLAN.read_text(encoding="utf-8"),
        )

    def test_resolve_commit_requires_full_exact_sha(self) -> None:
        self.assertEqual(self.reader.resolve_commit(self.head), self.head)
        for invalid in (
            "HEAD",
            self.head.upper(),
            self.head[:12],
            "g" * 40,
            "0" * 40,
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    self.reader.resolve_commit(invalid)

    def test_reads_blob_and_lists_tree_from_commit(self) -> None:
        data = self.reader.read_bytes(self.head, "crosswalks/ESAF-1600.md")
        self.assertTrue(data.startswith(b"# ESAF-1600 Standards Crosswalk Methodology"))
        paths = self.reader.list_files(self.head, "crosswalks/schema")
        self.assertIn("crosswalks/schema/mapping-set.schema.json", paths)
        self.assertEqual(paths, tuple(sorted(paths)))

    def test_read_bytes_rejects_unsafe_repository_paths(self) -> None:
        for unsafe in (
            "/absolute/path",
            "../parent/path",
            "crosswalks\\schema\\mapping-set.schema.json",
            "C:drive-relative",
        ):
            with self.subTest(path=unsafe):
                with self.assertRaisesRegex(ValueError, "unsafe repository path"):
                    self.reader.read_bytes(self.head, unsafe)

    def test_read_bytes_rejects_non_regular_git_blob_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, _head = _create_clean_repository(Path(directory))
            blob = subprocess.run(
                ["git", "hash-object", "-w", "--stdin"],
                cwd=repository,
                input=b"tracked.txt",
                check=True,
                capture_output=True,
            ).stdout.decode("ascii").strip()
            _git(
                repository,
                "update-index",
                "--add",
                "--cacheinfo",
                f"120000,{blob},fixed-evidence.md",
            )
            _git(repository, "commit", "-m", "add non-regular evidence")
            head = _git(repository, "rev-parse", "HEAD")
            with self.assertRaisesRegex(
                ValueError,
                "unexpected repository entry",
            ):
                GitReader(repository).read_bytes(
                    head,
                    "fixed-evidence.md",
                )

    def test_reports_all_worktree_roots_as_resolved_paths(self) -> None:
        roots = self.reader.worktree_roots()
        self.assertIn(ROOT.resolve(), roots)
        self.assertTrue(all(path.is_absolute() for path in roots))


class CandidateExecutionStateTests(unittest.TestCase):
    def test_accepts_clean_repository_at_candidate_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, head = _create_clean_repository(Path(directory))
            GitReader(repository).require_candidate_execution_state(head)

    def test_rejects_dirty_tracked_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, head = _create_clean_repository(Path(directory))
            (repository / "tracked.txt").write_text("changed\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "repository must be clean"):
                GitReader(repository).require_candidate_execution_state(head)

    def test_rejects_dirty_untracked_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, head = _create_clean_repository(Path(directory))
            (repository / "untracked.txt").write_text("untracked\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "repository must be clean"):
                GitReader(repository).require_candidate_execution_state(head)

    def test_rejects_candidate_that_is_not_current_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository, first = _create_clean_repository(Path(directory))
            (repository / "tracked.txt").write_text("second\n", encoding="utf-8")
            _git(repository, "add", "tracked.txt")
            _git(repository, "commit", "-m", "second")
            with self.assertRaisesRegex(ValueError, "current HEAD must equal candidate"):
                GitReader(repository).require_candidate_execution_state(first)


class GeneratorCheckoutBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.profile = PROFILES[CORE_ID]

    def test_writer_rejects_reader_from_different_checkout(self) -> None:
        module_reader = GitReader(ROOT)
        mapping_set_path = f"{self.profile.snapshot_path}/README.md"
        minimal_files = (
            PackageFile(
                mapping_set_path,
                module_reader.read_bytes(self.head, mapping_set_path),
                "mapping set",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository, foreign_head = _create_clean_repository(root)
            output = root / "package"
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=minimal_files,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "reader root must equal module checkout",
                ):
                    write_package(
                        GitReader(repository),
                        foreign_head,
                        self.profile,
                        output,
                    )

    def test_writer_uses_fresh_module_checkout_for_execution_state(
        self,
    ) -> None:
        caller = GitReader(ROOT)
        caller_check = mock.Mock()
        caller.require_candidate_execution_state = caller_check
        mapping_set_path = f"{self.profile.snapshot_path}/README.md"
        minimal_files = (
            PackageFile(
                mapping_set_path,
                caller.read_bytes(self.head, mapping_set_path),
                "mapping set",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=minimal_files,
            ), mock.patch.object(
                GitReader,
                "require_candidate_execution_state",
                autospec=True,
            ) as module_check:
                write_package(
                    caller,
                    self.head,
                    self.profile,
                    Path(directory) / "package",
                )
        caller_check.assert_not_called()
        self.assertEqual(module_check.call_count, 2)
        for call in module_check.call_args_list:
            checked_reader, checked_commit = call.args
            self.assertIsNot(checked_reader, caller)
            self.assertEqual(checked_reader.root, ROOT)
            self.assertEqual(checked_commit, self.head)


class PackagePopulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reader = GitReader(ROOT)
        cls.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()

    def test_package_file_reads_preserve_mutation_reader_behavior(self) -> None:
        # Catches requiring read_many() on duck-typed mutation readers or
        # collapsing their observable repeated-read behavior.
        class MutatingReader:
            def __init__(self) -> None:
                self.read_count = 0

            def read_bytes(self, commit: str, path: str) -> bytes:
                self.read_count += 1
                return f"{commit}:{path}:{self.read_count}".encode("utf-8")

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return ()

        reader = MutatingReader()
        actual = bundle_builder._read_package_files(
            reader,
            "a" * 40,
            ("first.md", "second.md"),
        )

        self.assertEqual(
            actual,
            {
                "first.md": (f"{'a' * 40}:first.md:1").encode("utf-8"),
                "second.md": (f"{'a' * 40}:second.md:2").encode("utf-8"),
            },
        )
        self.assertEqual(reader.read_count, 2)

    def test_every_profile_collects_exact_population_and_dependencies(self) -> None:
        for profile in PROFILES.values():
            with self.subTest(profile=profile.label):
                files = collect_package_files(self.reader, self.head, profile)
                paths = {item.path for item in files}
                record_prefix = f"{profile.snapshot_path}/"
                record_paths = {
                    path for path in paths
                    if path.startswith(record_prefix)
                    and path.endswith(".md")
                    and not path.endswith("/README.md")
                    and not path.endswith("/PROVISION_INVENTORY.md")
                }
                self.assertEqual(len(record_paths), profile.expected_count)
                for required in (
                    f"{profile.snapshot_path}/README.md",
                    f"{profile.snapshot_path}/PROVISION_INVENTORY.md",
                    f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json",
                    f"crosswalks/registry/{profile.mapping_set_id}.md",
                    "crosswalks/ESAF-1600.md",
                    "crosswalks/schema/mapping-set.schema.json",
                    "crosswalks/schema/mapping-record.schema.json",
                    "crosswalks/schema/qualified-review-evidence.schema.json",
                    "crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md",
                    "crosswalks/reviews/templates/REVIEWER_ATTESTATION.md",
                    "review-metadata/catalog-entry.json",
                ):
                    self.assertIn(required, paths)

    def test_evidence_schema_is_candidate_sourced_with_exact_purpose(
        self,
    ) -> None:
        schema_path = (
            "crosswalks/schema/qualified-review-evidence.schema.json"
        )
        for profile in PROFILES.values():
            with self.subTest(profile=profile.label):
                files = collect_package_files(self.reader, self.head, profile)
                evidence_schema = next(
                    item for item in files if item.path == schema_path
                )
                self.assertEqual(
                    evidence_schema.purpose,
                    "qualified-review evidence schema",
                )
                self.assertEqual(
                    evidence_schema.content,
                    self.reader.read_bytes(self.head, schema_path),
                )

    def test_collected_controls_match_manifest_paths_and_digests(self) -> None:
        for profile in PROFILES.values():
            files = collect_package_files(self.reader, self.head, profile)
            by_path = {item.path: item.content for item in files}
            manifest = json.loads(
                by_path[f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"]
            )
            for control in manifest["controls"]:
                packaged_path = f"controls/{control['path']}"
                self.assertEqual(
                    hashlib.sha256(by_path[packaged_path]).hexdigest(),
                    control["record_sha256"],
                )

    def test_controls_are_read_from_manifest_pinned_historical_commit(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class TrackingReader:
            def __init__(self) -> None:
                self.reads: list[tuple[str, str]] = []

            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                self.reads.append((commit, path))
                return base.read_bytes(commit, path)

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        reader = TrackingReader()
        files = collect_package_files(reader, self.head, profile)
        by_path = {item.path: item.content for item in files}
        manifest = json.loads(
            by_path[f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"]
        )
        source_commit = manifest["source_commit_sha"]
        control_paths = {
            f"controls/{control['path']}" for control in manifest["controls"]
        }
        historical_paths = control_paths | {"controls/catalog.json"}
        self.assertEqual(
            {
                commit
                for commit, path in reader.reads
                if path in historical_paths
            },
            {source_commit},
        )
        self.assertEqual(
            {
                commit
                for commit, path in reader.reads
                if path not in historical_paths
            },
            {self.head},
        )

    def test_collector_accepts_prose_draft_registry(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == f"crosswalks/registry/{profile.mapping_set_id}.md":
                    front_matter, body = content.split(b"---\n", 2)[1:]
                    body = body.replace(b"Draft", b"Pre-review")
                    body = body.replace(b"draft", b"pre-review")
                    return b"---\n" + front_matter + b"---\n" + body
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        files = collect_package_files(MutatingReader(), self.head, profile)
        self.assertIn(
            f"crosswalks/registry/{profile.mapping_set_id}.md",
            {item.path for item in files},
        )

    def test_collector_rejects_unexpected_snapshot_artifact(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader
        unexpected = f"{profile.snapshot_path}/NOTES.txt"

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                return b"unexpected\n" if path == unexpected else base.read_bytes(commit, path)

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return tuple(sorted((*base.list_files(commit, path), unexpected)))

        with self.assertRaisesRegex(ValueError, "unexpected snapshot entry"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_registry_snapshot_digest_drift(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader
        registry_path = f"crosswalks/registry/{profile.mapping_set_id}.md"

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == registry_path:
                    return re.sub(
                        rb"(?m)^snapshot_digest: [0-9a-f]{64}$",
                        b"snapshot_digest: " + b"0" * 64,
                        content,
                        count=1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "snapshot digest mismatch"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_control_catalog_digest_drift(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader
        manifest_path = f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == manifest_path:
                    manifest = json.loads(content)
                    manifest["control_catalog_sha256"] = "0" * 64
                    return (json.dumps(manifest, sort_keys=True) + "\n").encode()
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "control catalog digest mismatch"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_consistently_rehashed_incomplete_manifest(
        self,
    ) -> None:
        profile = PROFILES[CORE_ID]
        base = self.reader
        manifest_path = f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"
        registry_path = f"crosswalks/registry/{profile.mapping_set_id}.md"
        snapshot_contents = {
            path: base.read_bytes(self.head, path)
            for path in base.list_files(self.head, profile.snapshot_path)
        }
        manifest = json.loads(snapshot_contents[manifest_path])
        removed = manifest["controls"].pop()
        self.assertEqual(removed["id"], "STR-130")
        snapshot_contents[manifest_path] = bundle_builder.canonical_json_bytes(
            manifest
        )
        replacement_digest = snapshot_digest_from_files(
            profile.snapshot_path,
            snapshot_contents,
        )
        registry = re.sub(
            rb"(?m)^snapshot_digest: [0-9a-f]{64}$",
            f"snapshot_digest: {replacement_digest}".encode("ascii"),
            base.read_bytes(self.head, registry_path),
            count=1,
        )
        catalog = json.loads(
            base.read_bytes(self.head, "crosswalks/catalog.json")
        )
        catalog_entry = next(
            item
            for item in catalog["mapping_sets"]
            if item["metadata"]["mapping_set_id"] == profile.mapping_set_id
        )
        catalog_entry["lifecycle"]["snapshot_digest"] = replacement_digest
        catalog_bytes = bundle_builder.canonical_json_bytes(catalog)

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                if path == manifest_path:
                    return snapshot_contents[manifest_path]
                if path == registry_path:
                    return registry
                if path == "crosswalks/catalog.json":
                    return catalog_bytes
                return base.read_bytes(commit, path)

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(
            ValueError,
            "control manifest differs from deterministic regeneration",
        ):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_source_evidence_digest_drift(self) -> None:
        profile = PROFILES[PLUS_FORWARD_ID]
        base = self.reader
        oracle_path = (
            "docs/superpowers/specs/"
            "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
        )

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == oracle_path:
                    return content.replace(
                        b'"access_date": "2026-07-14"',
                        b'"access_date": "2026-07-15"',
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(
            ValueError,
            "source evidence digest mismatch",
        ):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_source_evidence_identity_matches_mapping_metadata(self) -> None:
        profile = PROFILES[PLUS_FORWARD_ID]
        readme = self.reader.read_bytes(
            self.head,
            f"{profile.snapshot_path}/README.md",
        )
        metadata, _ = parse_front_matter_bytes(readme)
        oracle_path = (
            "docs/superpowers/specs/"
            "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
        )
        oracle = json.loads(self.reader.read_bytes(self.head, oracle_path))
        oracle["source"]["version"] = "3.1"
        payload = PackageFile(
            oracle_path,
            json.dumps(oracle, sort_keys=True).encode("utf-8"),
            "source evidence pin",
        )
        with self.assertRaisesRegex(
            ValueError,
            "source evidence identity mismatch",
        ):
            bundle_builder._validate_source_evidence_identity(
                payload,
                metadata,
            )

    def test_collector_rejects_same_count_catalog_status_substitution(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == "crosswalks/catalog.json":
                    catalog = json.loads(content)
                    entry = next(
                        item
                        for item in catalog["mapping_sets"]
                        if item["metadata"]["mapping_set_id"]
                        == profile.mapping_set_id
                    )
                    entry["provisions"][0]["metadata"]["status"] = "reviewed"
                    return (json.dumps(catalog, sort_keys=True) + "\n").encode()
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "catalog entry mismatch"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_relationship_direction_drift(self) -> None:
        profile = PROFILES[PLUS_FORWARD_ID]
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if (
                    path.startswith(f"{profile.snapshot_path}/")
                    and path.endswith(".md")
                ):
                    return content.replace(
                        b'"direction": "esaf_to_external"',
                        b'"direction": "external_to_esaf"',
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "relationship direction mismatch"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_nonempty_registry_events(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == f"crosswalks/registry/{profile.mapping_set_id}.md":
                    return content.replace(
                        b"events: []",
                        b"events:\n  - reviewed",
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(
            ValueError,
            "registry lifecycle event array must be empty",
        ):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_population_or_status_drift(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path.endswith("/README.md"):
                    return content.replace(b"status: draft", b"status: reviewed", 1)
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "candidate schema validation"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_reviewer_metadata_on_draft_mapping_set(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path == f"{profile.snapshot_path}/README.md":
                    return content.replace(
                        b"status: draft\n",
                        b"status: draft\nreviewer: Example Reviewer\n",
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "candidate schema validation"):
            collect_package_files(MutatingReader(), self.head, profile)

    def test_collector_rejects_reviewer_metadata_on_draft_mapping_record(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def resolve_commit(self, revision: str) -> str:
                return base.resolve_commit(revision)

            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if (
                    path.startswith(f"{profile.snapshot_path}/")
                    and path.endswith(".md")
                    and not path.endswith("/README.md")
                    and not path.endswith("/PROVISION_INVENTORY.md")
                ):
                    return content.replace(
                        b'  "status": "draft",\n',
                        b'  "status": "draft",\n'
                        b'  "reviewer": {"id": "example-reviewer"},\n',
                        1,
                    )
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "candidate schema validation"):
            collect_package_files(MutatingReader(), self.head, profile)


class PackageEquivalenceTests(unittest.TestCase):
    def test_all_profiles_match_the_reviewed_pre_batching_oracle(self) -> None:
        # Catches any package path, order, purpose, byte-length, or content
        # drift introduced while changing the Git read strategy.
        oracle = json.loads(
            (
                ROOT
                / "tests/fixtures/git-batching-package-equivalence.json"
            ).read_bytes()
        )
        baseline_commit = oracle["baseline_commit"]
        self.assertEqual(set(PROFILES), set(oracle["profiles"]))

        reader = GitReader(ROOT)
        self.assertEqual(
            reader.resolve_commit(baseline_commit),
            baseline_commit,
        )
        for mapping_set_id, profile in PROFILES.items():
            with self.subTest(profile=profile.label):
                assembly = assemble_package(
                    reader,
                    baseline_commit,
                    profile,
                )
                actual = [
                    {
                        "path": item.path,
                        "purpose": item.purpose,
                        "bytes": len(item.content),
                        "sha256": hashlib.sha256(item.content).hexdigest(),
                    }
                    for item in assembly.payloads
                ]
                actual.append(
                    {
                        "path": "PACKAGE_MANIFEST.json",
                        "purpose": "package manifest",
                        "bytes": len(assembly.manifest_bytes),
                        "sha256": hashlib.sha256(
                            assembly.manifest_bytes
                        ).hexdigest(),
                    }
                )
                self.assertEqual(actual, oracle["profiles"][mapping_set_id])


class PackageGitInvocationTests(unittest.TestCase):
    def test_all_profiles_use_three_finite_object_read_phases(self) -> None:
        # Catches a return to singleton Git object reads, mixing candidate and
        # historical objects, or passing revision expressions to cat-file.
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

        for profile in PROFILES.values():
            with self.subTest(profile=profile.label):
                bundle_builder._deterministic_control_manifest_bytes.cache_clear()
                reader = GitReader(ROOT)
                with mock.patch.object(
                    reader,
                    "_run_finite_git",
                    wraps=reader._run_finite_git,
                ) as finite_git, mock.patch.object(
                    crosswalk_manifest,
                    "_git",
                    wraps=crosswalk_manifest._git,
                ) as manifest_git:
                    files = collect_package_files(reader, head, profile)

                commands = [call.args[0] for call in finite_git.call_args_list]
                tree_commands = [
                    arguments for arguments in commands
                    if arguments and arguments[0] == "ls-tree"
                ]
                check_calls = [
                    call for call in finite_git.call_args_list
                    if call.args[0][:2]
                    == (
                        "cat-file",
                        "--batch-check=%(objectname) %(objecttype) %(objectsize)",
                    )
                ]
                content_calls = [
                    call for call in finite_git.call_args_list
                    if call.args[0] == ("cat-file", "--batch")
                ]

                packaged_manifest = json.loads(
                    next(
                        item.content
                        for item in files
                        if item.path
                        == f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"
                    )
                )
                control_count = sum(
                    item.purpose == "referenced ESAF control"
                    for item in files
                )
                self.assertEqual(finite_git.call_count, 11)
                self.assertEqual(len(tree_commands), 2)
                self.assertEqual(
                    {arguments[-1] for arguments in tree_commands},
                    {head, packaged_manifest["source_commit_sha"]},
                )
                self.assertEqual(len(check_calls), 3)
                self.assertEqual(len(content_calls), 3)
                self.assertFalse(
                    any(
                        arguments and arguments[0] == "show"
                        for arguments in commands
                    )
                )
                for check_call, content_call in zip(
                    check_calls,
                    content_calls,
                    strict=True,
                ):
                    request = check_call.kwargs["input_bytes"]
                    self.assertEqual(content_call.kwargs["input_bytes"], request)
                    object_ids = request.decode("ascii").splitlines()
                    self.assertTrue(object_ids)
                    self.assertTrue(
                        all(
                            re.fullmatch(r"[0-9a-f]{40}", item)
                            for item in object_ids
                        )
                    )
                    self.assertNotIn(b":", request)

                manifest_show_count = sum(
                    call.args[1] == "show"
                    for call in manifest_git.call_args_list
                )
                self.assertEqual(manifest_git.call_count, control_count + 4)
                self.assertEqual(manifest_show_count, control_count + 2)


class ReviewedCandidateAssemblyTests(unittest.TestCase):
    """Exercise reviewed candidate content from a real isolated Git repository."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.shared_temporary = tempfile.TemporaryDirectory()
        cls.base_repository = Path(cls.shared_temporary.name) / "reviewed-candidate"
        subprocess.run(
            ["git", "clone", "--no-hardlinks", str(ROOT), str(cls.base_repository)],
            check=True,
            capture_output=True,
            text=True,
        )
        _git(cls.base_repository, "config", "user.name", "ESAF Test")
        _git(cls.base_repository, "config", "user.email", "esaf-test@example.invalid")
        fixture = cls("runTest")
        fixture.repository = cls.base_repository
        fixture.profile = PROFILES[CORE_ID]
        fixture._make_reviewed_candidate()
        cls.base_head = fixture._commit("reviewed candidate")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.shared_temporary.cleanup()

    def setUp(self) -> None:
        self.repository = self.base_repository
        _git(self.repository, "reset", "--hard", self.base_head)
        self.profile = PROFILES[CORE_ID]
        self.head = self.base_head
        self.reader = GitReader(self.repository)

    def _fresh_candidate(self) -> None:
        _git(self.repository, "reset", "--hard", self.base_head)
        self.head = self.base_head
        self.reader = GitReader(self.repository)

    def _commit(self, message: str) -> str:
        _git(self.repository, "add", "--all")
        _git(self.repository, "commit", "-m", message)
        return _git(self.repository, "rev-parse", "HEAD")

    def _front_matter(self, path: Path) -> tuple[dict[str, object], str]:
        return parse_front_matter_bytes(path.read_bytes())

    def _write_front_matter(
        self,
        path: Path,
        metadata: dict[str, object],
        body: str,
    ) -> None:
        rendered = yaml.safe_dump(
            metadata,
            allow_unicode=True,
            sort_keys=False,
        )
        path.write_text(
            f"---\n{rendered}---\n{body}",
            encoding="utf-8",
            newline="\n",
        )

    @staticmethod
    def _reviewer() -> dict[str, object]:
        return {
            "id": "independent-reviewer",
            "qualification": "Qualified independent mapping reviewer",
            "date": "2026-07-25",
            "authorized_source_access": True,
            "findings_disposition": "No Critical or Important findings remain.",
        }

    def _snapshot_paths(self) -> list[Path]:
        return sorted((self.repository / self.profile.snapshot_path).glob("*"))

    def _make_reviewed_candidate(self) -> None:
        snapshot = self.repository / self.profile.snapshot_path
        for path in self._snapshot_paths():
            if path.name in {"PROVISION_INVENTORY.md", "ESAF_CONTROL_MANIFEST.json"}:
                continue
            metadata, body = self._front_matter(path)
            metadata["status"] = "reviewed"
            metadata["reviewer"] = self._reviewer()
            self._write_front_matter(path, metadata, body)
        snapshot_contents = {
            path.relative_to(self.repository).as_posix(): path.read_bytes()
            for path in self._snapshot_paths()
        }
        digest = snapshot_digest_from_files(self.profile.snapshot_path, snapshot_contents)
        registry = self.repository / "crosswalks" / "registry" / f"{CORE_ID}.md"
        metadata, body = self._front_matter(registry)
        metadata["snapshot_digest"] = digest
        self._write_front_matter(registry, metadata, body)
        result = crosswalk_validator.main(["--write"], root=self.repository)
        self.assertEqual(result, 0)

    def _replace_metadata(
        self,
        relative: str,
        update: object,
    ) -> None:
        path = self.repository / relative
        metadata, body = self._front_matter(path)
        update(metadata)
        self._write_front_matter(path, metadata, body)

    def _record_relative(self) -> str:
        for path in self._snapshot_paths():
            if path.name not in {
                "README.md",
                "PROVISION_INVENTORY.md",
                "ESAF_CONTROL_MANIFEST.json",
            }:
                return path.relative_to(self.repository).as_posix()
        self.fail("review fixture has no mapping record")

    def _assemble_after(self, relative: str, update: object) -> None:
        self._replace_metadata(relative, update)
        head = self._commit("mutate reviewed candidate")
        bundle_builder.assemble_package(
            GitReader(self.repository),
            head,
            self.profile,
            "reviewed",
        )

    def test_reviewed_candidate_assembles_and_renders_review_boundary(self) -> None:
        assembly = bundle_builder.assemble_package(
            self.reader,
            self.head,
            self.profile,
            "reviewed",
        )
        self.assertEqual(assembly.manifest["candidate_state"], "reviewed")
        index = next(
            item.content.decode("utf-8")
            for item in assembly.payloads
            if item.path == "PACKAGE_INDEX.md"
        )
        self.assertIn("| Candidate state | `reviewed` |", index)
        self.assertIn("reviewed but is not approved, published", index)

    def test_reviewed_candidate_rejects_mixed_or_approved_states(self) -> None:
        for label, relative, update, message in (
            (
                "mixed-record",
                self._record_relative(),
                lambda metadata: metadata.update(status="draft"),
                "must be reviewed",
            ),
            (
                "approved-snapshot",
                f"{self.profile.snapshot_path}/README.md",
                lambda metadata: metadata.update(status="approved"),
                "candidate schema validation",
            ),
            (
                "approved-record",
                self._record_relative(),
                lambda metadata: metadata.update(status="approved"),
                "candidate schema validation",
            ),
        ):
            with self.subTest(label=label):
                self._fresh_candidate()
                with self.assertRaisesRegex(ValueError, message):
                    self._assemble_after(relative, update)

    def test_reviewed_candidate_rejects_missing_reviewer_metadata(self) -> None:
        for label, relative in (
            ("snapshot", f"{self.profile.snapshot_path}/README.md"),
            ("record", self._record_relative()),
        ):
            with self.subTest(label=label):
                self._fresh_candidate()
                with self.assertRaisesRegex(ValueError, "candidate schema validation"):
                    self._assemble_after(relative, lambda metadata: metadata.pop("reviewer"))

    def test_reviewed_candidate_rejects_mapper_self_review(self) -> None:
        for relative in (f"{self.profile.snapshot_path}/README.md", self._record_relative()):
            with self.subTest(relative=relative):
                self._fresh_candidate()
                def self_review(metadata: dict[str, object]) -> None:
                    reviewer = metadata["reviewer"]
                    mapper = metadata["mapper"]
                    assert isinstance(reviewer, dict) and isinstance(mapper, dict)
                    reviewer["id"] = mapper["id"]
                with self.assertRaisesRegex(ValueError, "reviewer must differ from mapper"):
                    self._assemble_after(relative, self_review)

    def test_reviewed_candidate_rejects_critical_and_important_findings(self) -> None:
        readme = f"{self.profile.snapshot_path}/README.md"
        for severity, status in (
            ("Critical", "open"),
            ("Critical", "accepted"),
            ("Important", "open"),
            ("Important", "accepted"),
        ):
            with self.subTest(severity=severity, status=status):
                self._fresh_candidate()

                def add_finding(metadata: dict[str, object]) -> None:
                    finding: dict[str, object] = {
                        "finding_id": "review-finding",
                        "affected_record_ids": ["ce33-d-001"],
                        "severity": severity,
                        "status": status,
                        "description": "Fixture finding.",
                        "disposition": "Fixture disposition.",
                    }
                    if status == "accepted":
                        finding.update(
                            resolver_or_acceptor="fixture-acceptor",
                            disposition_date="2026-07-25",
                            acceptance_rationale="Fixture rationale.",
                        )
                    metadata["findings"] = [finding]

                with self.assertRaisesRegex(
                    ValueError,
                    f"{severity} finding must be resolved",
                ):
                    self._assemble_after(readme, add_finding)

    def test_reviewed_candidate_rejects_lifecycle_events(self) -> None:
        registry = f"crosswalks/registry/{CORE_ID}.md"
        with self.assertRaisesRegex(ValueError, "event array must be empty"):
            self._assemble_after(
                registry,
                lambda metadata: metadata.update(events=["reviewed"]),
            )

    def test_reviewed_candidate_rejects_each_required_reviewer_field(self) -> None:
        readme = f"{self.profile.snapshot_path}/README.md"
        for field in (
            "id",
            "qualification",
            "date",
            "authorized_source_access",
            "findings_disposition",
        ):
            with self.subTest(field=field):
                self._fresh_candidate()

                def remove_field(metadata: dict[str, object]) -> None:
                    reviewer = metadata["reviewer"]
                    assert isinstance(reviewer, dict)
                    reviewer.pop(field)

                with self.assertRaisesRegex(ValueError, "candidate schema validation"):
                    self._assemble_after(readme, remove_field)

    def test_reviewed_candidate_uses_candidate_sourced_schemas(self) -> None:
        cases = (
            (
                "mapping-set",
                "crosswalks/schema/mapping-set.schema.json",
                "\"reviewed\", \"approved\"",
                "\"approved\"",
                "mapping set candidate schema validation",
            ),
            (
                "mapping-record",
                "crosswalks/schema/mapping-record.schema.json",
                "\"draft\", \"reviewed\"",
                "\"draft\"",
                "record .* candidate schema validation",
            ),
        )
        for label, relative, before, after, message in cases:
            with self.subTest(schema=label):
                self._fresh_candidate()
                path = self.repository / relative
                path.write_text(
                    path.read_text(encoding="utf-8").replace(before, after, 1),
                    encoding="utf-8",
                    newline="\n",
                )
                head = self._commit("tighten candidate schema")
                with self.assertRaisesRegex(ValueError, message):
                    bundle_builder.assemble_package(
                        GitReader(self.repository),
                        head,
                        self.profile,
                        "reviewed",
                    )


class CandidateValidationTests(unittest.TestCase):
    def _metadata(self) -> dict[str, object]:
        return {
            "mapping_set_id": CORE_ID,
            "status": "reviewed",
            "mapper": {"id": "mapper"},
            "reviewer": {"id": "reviewer"},
        }

    def test_reviewed_reviewer_must_differ_from_mapper_for_set_and_record(self) -> None:
        for subject in ("mapping set", "record fixture.md"):
            metadata = self._metadata()
            metadata["reviewer"] = {"id": "mapper"}
            with self.subTest(subject=subject), self.assertRaisesRegex(
                ValueError, "reviewer must differ from mapper"
            ):
                bundle_builder._require_candidate_state(
                    metadata, CORE_ID, subject, "reviewed"
                )

    def test_candidate_schema_decoding_and_definition_errors_are_stable(self) -> None:
        class Reader:
            def __init__(self, content: bytes) -> None:
                self.content = content
            def read_bytes(self, commit: str, path: str) -> bytes:
                return self.content

        for content in (b"\xff", b'{"type": 7}'):
            with self.subTest(content=content), self.assertRaisesRegex(
                ValueError, "invalid candidate schema: crosswalks/schema/mapping-set.schema.json"
            ):
                bundle_builder._validate_candidate_metadata(
                    Reader(content), "0" * 40,
                    "crosswalks/schema/mapping-set.schema.json", {}, "mapping set"
                )

    def test_candidate_schema_can_allow_extension_and_catalog_uses_supplied_validators(self) -> None:
        schema = {"type": "object", "additionalProperties": True}
        class Reader:
            def read_bytes(self, commit: str, path: str) -> bytes:
                return json.dumps(schema).encode("utf-8")
        metadata = self._metadata()
        metadata.update(schema_version="1.0.0", extension="candidate-only")
        bundle_builder._validate_candidate_metadata(
            Reader(), "0" * 40, "crosswalks/schema/mapping-set.schema.json", metadata, "mapping set"
        )
        with mock.patch.object(crosswalk_catalog, "load_schemas", side_effect=AssertionError):
            self.assertEqual(
                crosswalk_catalog._catalog_model_errors(
                    bundle_builder.ValidationResult([], [], []), {}
                ),
                [],
            )


class PackageWriterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reader = GitReader(ROOT)
        cls.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
        cls.profile = PROFILES[
            "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0"
        ]

    def setUp(self) -> None:
        state_patch = mock.patch.object(
            self.reader,
            "require_candidate_execution_state",
        )
        self.require_state = state_patch.start()
        self.addCleanup(state_patch.stop)
        generator_state_patch = mock.patch(
            "tools.build_mapping_review_bundle._require_generator_execution_state",
            create=True,
        )
        self.generator_state = generator_state_patch.start()
        self.addCleanup(generator_state_patch.stop)

    def test_writer_verifies_candidate_state_at_api_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=self._minimal_files(),
            ):
                write_package(
                    self.reader,
                    self.head,
                    self.profile,
                    output,
                )
        self.assertEqual(
            self.generator_state.call_args_list,
            [
                mock.call(self.reader, self.head),
                mock.call(self.reader, self.head),
            ],
        )
        self.require_state.assert_not_called()

    def test_writer_does_not_publish_after_execution_state_changes(self) -> None:
        self.generator_state.side_effect = (
            None,
            ValueError("repository became dirty"),
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=self._minimal_files(),
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "repository became dirty",
                ):
                    write_package(
                        self.reader,
                        self.head,
                        self.profile,
                        output,
                    )
            self.assertFalse(output.exists())

    def test_two_runs_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            first_manifest = write_package(
                self.reader, self.head, self.profile, first
            )
            second_manifest = write_package(
                self.reader, self.head, self.profile, second
            )
            self.assertEqual(first_manifest, second_manifest)
            first_files = {
                path.relative_to(first).as_posix(): path.read_bytes()
                for path in first.rglob("*") if path.is_file()
            }
            second_files = {
                path.relative_to(second).as_posix(): path.read_bytes()
                for path in second.rglob("*") if path.is_file()
            }
            self.assertEqual(first_files, second_files)
            self.assertIn("PACKAGE_INDEX.md", first_files)
            self.assertIn("PACKAGE_MANIFEST.json", first_files)

    def test_manifest_covers_every_payload_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            manifest = write_package(
                self.reader, self.head, self.profile, output
            )
            listed = {item["path"] for item in manifest["files"]}
            actual_payload = {
                path.relative_to(output).as_posix()
                for path in output.rglob("*")
                if path.is_file() and path.name != "PACKAGE_MANIFEST.json"
            }
            self.assertEqual(listed, actual_payload)
            for item in manifest["files"]:
                content = (output / item["path"]).read_bytes()
                self.assertEqual(item["bytes"], len(content))
                self.assertEqual(
                    item["sha256"], hashlib.sha256(content).hexdigest()
                )

    def test_rejects_worktree_and_nonempty_output(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside every Git worktree"):
            validate_output_directory(
                ROOT / "review-output",
                self.reader.worktree_roots(),
            )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "existing"
            output.mkdir()
            (output / "keep.txt").write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty"):
                validate_output_directory(output, ())

    def test_cli_writes_one_allowlisted_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "tools.build_mapping_review_bundle._require_generator_execution_state",
            ) as require_state:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    result = main(
                        [
                            "--commit",
                            self.head,
                            "--mapping-set-id",
                            self.profile.mapping_set_id,
                            "--output",
                            str(output),
                        ]
                    )
            self.assertEqual(result, 0, stderr.getvalue())
            self.assertEqual(require_state.call_count, 2)
            for call in require_state.call_args_list:
                checked_reader, checked_commit = call.args
                self.assertIsInstance(checked_reader, GitReader)
                self.assertEqual(checked_reader.root, ROOT)
                self.assertEqual(checked_commit, self.head)
            report = json.loads(stdout.getvalue())
            self.assertEqual(report["candidate_commit"], self.head)
            self.assertEqual(report["mapping_set_id"], self.profile.mapping_set_id)
            self.assertEqual(len(report["manifest_sha256"]), 64)
            manifest = json.loads(
                (output / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["generator_commit"], self.head)

    def test_cli_defaults_to_draft_and_rejects_unknown_candidate_state(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            default_output = Path(directory) / "default-package"
            default_result = main(
                [
                    "--commit",
                    self.head,
                    "--mapping-set-id",
                    CORE_ID,
                    "--output",
                    str(default_output),
                ]
            )
            self.assertEqual(default_result, 0)
            self.assertEqual(
                json.loads(
                    (default_output / "PACKAGE_MANIFEST.json").read_bytes()
                )["candidate_state"],
                "draft",
            )

            output = Path(directory) / "unknown-state-package"
            parser_result = main(
                [
                    "--commit",
                    self.head,
                    "--mapping-set-id",
                    CORE_ID,
                    "--output",
                    str(output),
                    "--candidate-state",
                    "approved",
                ]
            )
            self.assertEqual(parser_result, 2)
            self.assertFalse(output.exists())

    def test_assembly_is_in_memory_and_manifest_self_excludes(self) -> None:
        assembly = assemble_package(self.reader, self.head, PROFILES[CORE_ID])
        self.assertEqual(assembly.manifest["candidate_state"], "draft")
        self.assertNotIn(
            "PACKAGE_MANIFEST.json",
            {item.path for item in assembly.payloads},
        )

    def test_cli_rejects_unknown_mapping_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main(
                    [
                        "--commit",
                        self.head,
                        "--mapping-set-id",
                        "unknown",
                        "--output",
                        str(Path(directory) / "package"),
                    ]
                )
            self.assertEqual(result, 2)
            self.assertIn("unsupported mapping-set identifier", stderr.getvalue())

    def _minimal_files(
        self,
        *extra: PackageFile,
    ) -> tuple[PackageFile, ...]:
        mapping_set_path = f"{self.profile.snapshot_path}/README.md"
        return (
            PackageFile(
                mapping_set_path,
                self.reader.read_bytes(self.head, mapping_set_path),
                "mapping set",
            ),
            *extra,
        )

    def test_writer_rejects_unsafe_package_paths(self) -> None:
        for index, unsafe in enumerate(
            (
                "/absolute/path",
                "../parent/path",
                "review\\backslash.txt",
                "C:drive-relative",
            )
        ):
            with self.subTest(path=unsafe):
                with tempfile.TemporaryDirectory() as directory:
                    output = Path(directory) / f"package-{index}"
                    files = self._minimal_files(
                        PackageFile(unsafe, b"unsafe\n", "unsafe test"),
                    )
                    with mock.patch(
                        "tools.build_mapping_review_bundle.collect_package_files",
                        return_value=files,
                    ):
                        with self.assertRaisesRegex(
                            ValueError,
                            "unsafe package path",
                        ):
                            write_package(
                                self.reader,
                                self.head,
                                self.profile,
                                output,
                            )

    def test_writer_rejects_case_insensitive_path_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            files = self._minimal_files(
                PackageFile("review-metadata/Evidence.txt", b"one\n", "test"),
                PackageFile("review-metadata/evidence.txt", b"two\n", "test"),
            )
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=files,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "case-insensitive package path collision",
                ):
                    write_package(
                        self.reader,
                        self.head,
                        self.profile,
                        output,
                    )

    def test_writer_rejects_existing_empty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            output.mkdir()
            with self.assertRaisesRegex(ValueError, "must not already exist"):
                write_package(
                    self.reader,
                    self.head,
                    self.profile,
                    output,
                )

    def test_writer_does_not_publish_partial_output_after_write_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            files = self._minimal_files(
                PackageFile("review-metadata/evidence.txt", b"evidence\n", "test"),
            )
            with mock.patch(
                "tools.build_mapping_review_bundle.collect_package_files",
                return_value=files,
            ):
                with mock.patch(
                    "tools.build_mapping_review_bundle._write_file_exclusively",
                    side_effect=OSError("injected write failure"),
                    create=True,
                ):
                    with self.assertRaisesRegex(OSError, "injected write failure"):
                        write_package(
                            self.reader,
                            self.head,
                            self.profile,
                            output,
                        )
            self.assertFalse(output.exists())

    @unittest.skipUnless(
        hasattr(os, "symlink"),
        "symbolic links are not supported",
    )
    def test_output_validation_rejects_existing_directory_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            link = root / "output-link"
            try:
                os.symlink(target, link, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"symbolic-link creation unavailable: {error}")
            with self.assertRaisesRegex(ValueError, "must not already exist"):
                validate_output_directory(link, ())


class PackageIntegrationTests(unittest.TestCase):
    def test_all_packages_are_separate_complete_and_source_safe(self) -> None:
        reader = GitReader(ROOT)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
        with mock.patch(
            "tools.build_mapping_review_bundle._require_generator_execution_state",
        ) as require_state, tempfile.TemporaryDirectory() as directory:
            manifests = {}
            for profile in PROFILES.values():
                with self.subTest(profile=profile.label):
                    output = (
                        Path(directory)
                        / profile.label.replace(" ", "-").lower()
                    )
                    manifests[profile.label] = write_package(
                        reader, head, profile, output
                    )
                    manifest = manifests[profile.label]
                    names = {
                        path.relative_to(output).as_posix()
                        for path in output.rglob("*") if path.is_file()
                    }
                    self.assertFalse(
                        any(
                            name.lower().endswith((".pdf", ".doc", ".docx"))
                            for name in names
                        )
                    )
                    index = (output / "PACKAGE_INDEX.md").read_text(
                        encoding="utf-8"
                    )
                    self.assertIn(profile.label, index)
                    self.assertIn(profile.direction, index)
                    self.assertIn(f"`{profile.mapping_set_id}`", index)
                    self.assertIn(f"| Candidate commit | `{head}` |", index)
                    self.assertIn(
                        f"| Expected provisions | {profile.expected_count} |",
                        index,
                    )
                    mapping_set_path = f"{profile.snapshot_path}/README.md"
                    mapping_set = (output / mapping_set_path).read_bytes()
                    metadata, _ = parse_front_matter_bytes(mapping_set)
                    publication = metadata["publication"]
                    source = metadata["source"]
                    source_version = metadata["source_version"]
                    release = metadata["esaf_release"]
                    rights = metadata["publication_rights"]
                    self.assertIn(
                        f"| Publication | {publication['name']} |",
                        index,
                    )
                    self.assertIn(
                        f"| Source version | `{source_version['id']}` "
                        f"({source_version['label']}) |",
                        index,
                    )
                    self.assertIn(
                        f"| Official URL | {source['official_url']} |",
                        index,
                    )
                    self.assertIn(
                        f"| Access class | `{source['access_class']}` |",
                        index,
                    )
                    self.assertIn(
                        f"| Historical control-source commit | "
                        f"`{release['source_commit_sha']}` |",
                        index,
                    )
                    self.assertIn(
                        f"| Historical control-catalog SHA-256 | "
                        f"`{release['control_catalog_sha256']}` |",
                        index,
                    )
                    self.assertIn(rights["basis"], index)
                    self.assertIn(rights["restrictions"], index)
                    for permitted in rights["permitted_elements"]:
                        self.assertIn(f"`{permitted}`", index)
                    if rights["prohibited_elements"]:
                        for prohibited in rights["prohibited_elements"]:
                            self.assertIn(f"`{prohibited}`", index)
                    else:
                        self.assertIn("None recorded.", index)
                    for evidence in EXPECTED_SOURCE_EVIDENCE[
                        profile.mapping_set_id
                    ]:
                        self.assertIn(evidence, index)
                    self.assertIn("controls/catalog.json", names)
                    self.assertEqual(
                        hashlib.sha256(
                            (output / "controls/catalog.json").read_bytes()
                        ).hexdigest(),
                        release["control_catalog_sha256"],
                    )
                    if profile.mapping_set_id != CORE_ID:
                        self.assertIn(
                            "docs/superpowers/specs/"
                            "2026-07-14-uk-cyber-essentials-plus-v3.2-"
                            "provision-oracle.json",
                            names,
                        )
                    manifest_rows = [
                        f"| `{item['path']}` | {item['purpose']} |"
                        for item in manifest["files"]
                    ]
                    positions = []
                    for row in manifest_rows:
                        self.assertIn(row, index)
                        positions.append(index.index(row))
                    self.assertEqual(positions, sorted(positions))
                    self.assertIn("obtain authorized access", index)
                    self.assertIn("remains Draft", index)
                    for nonclaim in (
                        "certification",
                        "compliance",
                        "equivalence",
                        "endorsement",
                        "approval",
                        "assurance",
                    ):
                        self.assertIn(nonclaim, index)
            self.assertEqual(set(manifests), {"Core", "Plus forward", "Plus reverse"})
            self.assertEqual(
                {item["mapping_set_id"] for item in manifests.values()},
                set(PROFILES),
            )
            self.assertEqual(
                require_state.call_args_list,
                [mock.call(reader, head)] * (2 * len(PROFILES)),
            )

    def test_tools_readme_documents_exact_safe_command(self) -> None:
        text = (ROOT / "tools/README.md").read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        self.assertIn("## Qualified mapping review packages", text)
        self.assertIn("build_mapping_review_bundle.py", text)
        self.assertIn("--commit", text)
        self.assertIn("--mapping-set-id", text)
        self.assertIn("--output", text)
        self.assertIn("outside every Git worktree", normalized)
        self.assertIn(
            "new output path that does not already exist",
            normalized,
        )
        self.assertIn(
            "candidate commit must equal the current clean HEAD",
            normalized,
        )
        self.assertIn(
            "failed assembly can leave an owned hidden sibling staging "
            "directory",
            normalized,
        )
        self.assertIn("does not include the external source document", text)
