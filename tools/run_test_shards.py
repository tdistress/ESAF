#!/usr/bin/env python3
"""Run the complete unit-test population in validated sequential shards."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import TextIO

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.test_shards import Shard, validate_manifest


FAILURE_SUMMARY_BYTES = 32768
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ShardResult:
    """The captured result from one independently executed test shard."""

    identifier: str
    modules: tuple[str, ...]
    elapsed_seconds: float
    exit_code: int
    stdout: bytes
    stderr: bytes


def build_command(shard: Shard, durations: int) -> list[str]:
    """Build the canonical unittest command for one shard."""
    return [
        sys.executable,
        "-m",
        "unittest",
        *shard.modules,
        "-v",
        "--durations",
        str(durations),
    ]


def run_shard(
    root: Path,
    shard: Shard,
    durations: int,
    runner: Callable[..., object] | None = None,
    clock: Callable[[], float] | None = None,
) -> ShardResult:
    """Run one shard as an independent process and capture its byte output."""
    command_runner = runner or subprocess.run
    elapsed_clock = clock or time.monotonic
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = build_command(shard, durations)
    started = elapsed_clock()
    completed = command_runner(
        command,
        cwd=root,
        shell=False,
        check=False,
        capture_output=True,
        env=environment,
    )
    elapsed_seconds = elapsed_clock() - started
    exit_code = getattr(completed, "returncode", None)
    stdout = getattr(completed, "stdout", None)
    stderr = getattr(completed, "stderr", None)
    if not isinstance(exit_code, int):
        raise ValueError(f"shard {shard.identifier} did not return an exit code")
    if not isinstance(stdout, bytes) or not isinstance(stderr, bytes):
        raise ValueError(f"shard {shard.identifier} did not return byte output")
    return ShardResult(
        shard.identifier,
        shard.modules,
        elapsed_seconds,
        exit_code,
        stdout,
        stderr,
    )


def run_all(
    root: Path,
    shards: tuple[Shard, ...],
    durations: int,
    runner: Callable[..., object] | None = None,
    clock: Callable[[], float] | None = None,
) -> tuple[ShardResult, ...]:
    """Run all shards sequentially, retaining results after failures."""
    return tuple(
        run_shard(root, shard, durations, runner=runner, clock=clock)
        for shard in shards
    )


def _worker_failure(shard: Shard, error: BaseException) -> ShardResult:
    """Represent an unexpected worker exception as a failed shard result."""
    message = (
        f"unexpected runner failure for shard {shard.identifier}: "
        f"{type(error).__name__}: {error}\n"
    )
    return ShardResult(
        shard.identifier,
        shard.modules,
        0.0,
        1,
        b"",
        message.encode("utf-8", errors="replace"),
    )


def run_all_parallel(
    root: Path,
    shards: tuple[Shard, ...],
    durations: int,
    runner: Callable[..., object] | None = None,
    clock: Callable[[], float] | None = None,
) -> tuple[ShardResult, ...]:
    """Run every shard concurrently and return results in manifest order."""
    if not shards:
        return ()
    with ThreadPoolExecutor(max_workers=len(shards)) as executor:
        futures = tuple(
            (
                shard,
                executor.submit(
                    run_shard, root, shard, durations, runner=runner, clock=clock
                ),
            )
            for shard in shards
        )
        results = []
        for shard, future in futures:
            try:
                results.append(future.result())
            except Exception as error:
                results.append(_worker_failure(shard, error))
    return tuple(results)


def _byte_tail(value: bytes, limit: int) -> str:
    """Return an UTF-8-safe tail whose encoded length fits *limit* bytes."""
    text = value.decode("utf-8", errors="replace")
    if len(text.encode("utf-8")) <= limit:
        return text
    low, high = 0, len(text)
    while low < high:
        middle = (low + high) // 2
        if len(text[middle:].encode("utf-8")) <= limit:
            high = middle
        else:
            low = middle + 1
    return text[low:]


def _failure_summary(results: tuple[ShardResult, ...]) -> str:
    """Build the bounded final diagnostic block for every failed shard."""
    failed = tuple(result for result in results if result.exit_code != 0)
    if not failed:
        return ""
    prefix = "Shard failures:\n"
    headings = tuple(
        f"[{result.identifier}] exit code {result.exit_code}\n"
        for result in failed
    )
    reserved = (
        len(prefix.encode("utf-8"))
        + sum(len(heading.encode("utf-8")) for heading in headings)
        + len(failed)
    )
    if reserved > FAILURE_SUMMARY_BYTES:
        raise ValueError("failed-shard headings exceed the diagnostic byte limit")
    allocation = (FAILURE_SUMMARY_BYTES - reserved) // len(failed)
    blocks = [prefix]
    for result, heading in zip(failed, headings, strict=True):
        blocks.append(heading)
        blocks.append(_byte_tail(result.stdout + result.stderr, allocation))
        blocks.append("\n")
    summary = "".join(blocks)
    if len(summary.encode("utf-8")) > FAILURE_SUMMARY_BYTES:
        raise AssertionError("failed-shard diagnostic exceeds the byte limit")
    return summary


def _write_result(result: ShardResult, stdout: TextIO, stderr: TextIO) -> None:
    """Write one shard's complete, ordinary diagnostic record."""
    print(f"Shard: {result.identifier}", file=stdout)
    print("Modules:", file=stdout)
    for module in result.modules:
        print(module, file=stdout)
    print(f"Elapsed seconds: {result.elapsed_seconds:.3f}", file=stdout)
    print(f"Exit code: {result.exit_code}", file=stdout)
    print("stdout:", file=stdout)
    print(result.stdout.decode("utf-8", errors="replace"), end="", file=stdout)
    if result.stdout and not result.stdout.endswith(b"\n"):
        print(file=stdout)
    print(f"Shard: {result.identifier} stderr:", file=stderr)
    print(result.stderr.decode("utf-8", errors="replace"), end="", file=stderr)
    if result.stderr and not result.stderr.endswith(b"\n"):
        print(file=stderr)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for local shard execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--shard", metavar="ID")
    selection.add_argument("--all", action="store_true")
    parser.add_argument("--parallel", action="store_true")
    parser.add_argument("--durations", type=int, default=50)
    return parser


def main(
    arguments: list[str] | None = None,
    *,
    root: Path = REPOSITORY_ROOT,
    runner: Callable[..., object] | None = None,
    clock: Callable[[], float] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    manifest_validator: Callable[[Path], tuple[Shard, ...]] = validate_manifest,
) -> int:
    """Validate the manifest, run the selected shards, and return an exit code."""
    parser = build_parser()
    options = parser.parse_args(arguments)
    if options.durations < 1:
        parser.error("--durations shall be at least 1")
    if options.parallel and not options.all:
        parser.error("--parallel shall be used only with --all")
    output = stdout or sys.stdout
    errors = stderr or sys.stderr
    shards = manifest_validator(root)
    execution_started = (clock or time.monotonic)()
    if options.all:
        if options.parallel:
            results = run_all_parallel(
                root, shards, options.durations, runner=runner, clock=clock
            )
        else:
            results = run_all(
                root, shards, options.durations, runner=runner, clock=clock
            )
    else:
        selected = next(
            (shard for shard in shards if shard.identifier == options.shard),
            None,
        )
        if selected is None:
            parser.error(f"unknown shard: {options.shard}")
        results = (
            run_shard(
                root, selected, options.durations, runner=runner, clock=clock
            ),
        )
    overall_elapsed_seconds = (clock or time.monotonic)() - execution_started
    print(f"Mode: {'parallel' if options.parallel else 'sequential'}", file=output)
    print(f"Overall elapsed seconds: {overall_elapsed_seconds:.3f}", file=output)
    for result in results:
        _write_result(result, output, errors)
    summary = _failure_summary(results)
    if summary:
        print(summary, end="", file=errors)
    return 1 if any(result.exit_code != 0 for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
