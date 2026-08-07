#!/usr/bin/env python3
"""Compare the retained profile language paths on one clean commit."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import profile_fixture, profile_language_cases  # noqa: E402
from tools import validate_profiles  # noqa: E402


Runner = Callable[..., subprocess.CompletedProcess[bytes]]


@dataclass(frozen=True)
class EquivalenceResult:
    candidate_sha: str
    method_count: int
    population_count: int
    population_sha256: str


class ProfileHotPathEquivalenceError(RuntimeError):
    """Report a verification failure without exposing checkout details."""


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ProfileHotPathEquivalenceError("command arguments are invalid")


def _run_git(
    root: Path,
    arguments: list[str],
    *,
    runner: Runner,
) -> subprocess.CompletedProcess[bytes]:
    try:
        result = runner(
            arguments,
            cwd=root,
            shell=False,
            capture_output=True,
        )
    except Exception as exc:
        raise ProfileHotPathEquivalenceError(
            "Git could not inspect the candidate checkout"
        ) from exc
    if result.returncode != 0:
        raise ProfileHotPathEquivalenceError(
            "Git could not inspect the candidate checkout"
        )
    if result.stderr != b"":
        raise ProfileHotPathEquivalenceError(
            "Git returned an unexpected candidate-check error"
        )
    if not isinstance(result.stdout, bytes):
        raise ProfileHotPathEquivalenceError(
            "Git returned an invalid candidate-check response"
        )
    return result


def require_exact_candidate(
    root: Path,
    candidate_sha: str,
    runner: Runner = subprocess.run,
) -> None:
    """Require one clean checkout at the supplied full lowercase HEAD."""
    if re.fullmatch(r"[0-9a-f]{40}", candidate_sha) is None:
        raise ProfileHotPathEquivalenceError(
            "candidate SHA must contain 40 lowercase hexadecimal characters"
        )
    if candidate_sha == "0" * 40:
        raise ProfileHotPathEquivalenceError("candidate SHA is unavailable")

    head = _run_git(
        root,
        ["git", "rev-parse", "--verify", "HEAD"],
        runner=runner,
    )
    if head.stdout != (candidate_sha + "\n").encode("ascii"):
        raise ProfileHotPathEquivalenceError(
            "candidate SHA does not match the checkout HEAD"
        )

    status = _run_git(
        root,
        [
            "git",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        runner=runner,
    )
    if status.stdout != b"":
        raise ProfileHotPathEquivalenceError(
            "candidate checkout contains uncommitted files"
        )


def _safe_case_label(method_name: str, case_id: str) -> str:
    allowed = r"[A-Za-z0-9_.:-]+"
    safe_method = (
        method_name
        if re.fullmatch(allowed, method_name)
        else "unknown_method"
    )
    safe_case = case_id if re.fullmatch(allowed, case_id) else "unknown_case"
    return f"{safe_method}/{safe_case}"


def _reject_temporary_paths(
    diagnostics: Sequence[str], fixture_root: Path, case_label: str
) -> None:
    resolved = str(fixture_root.resolve()).casefold()
    normalized = resolved.replace("\\", "/")
    for diagnostic in diagnostics:
        if not isinstance(diagnostic, str):
            raise ProfileHotPathEquivalenceError(
                f"{case_label}: a validator returned a non-text diagnostic"
            )
        candidate = diagnostic.casefold()
        if resolved in candidate or normalized in candidate.replace("\\", "/"):
            raise ProfileHotPathEquivalenceError(
                f"{case_label}: a diagnostic contains a temporary fixture path"
            )


def _compare_case(
    *,
    fixture_root: Path,
    package: Path,
    case: profile_language_cases.ProfileLanguageCase,
) -> None:
    readme = profile_fixture.write_profile_readme(package, case.text)
    profile_path = package / "profile.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile["source_boundary"]["excluded_sources"] = list(
        case.excluded_sources
    )
    profile_fixture.write_component(package, "profile.json", profile)
    full = validate_profiles.validate(fixture_root)
    narrow: list[str] = []
    if "claim" in case.diagnostic_families:
        narrow.extend(
            validate_profiles.claim_text_diagnostics(readme, case.location)
        )
    if "source_authority" in case.diagnostic_families:
        narrow.extend(
            validate_profiles.source_authority_text_diagnostics(
                readme, case.location, case.excluded_sources
            )
        )
    narrow = sorted(set(narrow))
    expected = list(case.expected_diagnostics)

    case_label = _safe_case_label(case.method_name, case.case_id)
    for diagnostics in (full, narrow, expected):
        _reject_temporary_paths(diagnostics, fixture_root, case_label)

    mismatches: list[str] = []
    if full != narrow:
        mismatches.append("complete/narrow")
    if full != expected:
        mismatches.append("complete/expected")
    if narrow != expected:
        mismatches.append("narrow/expected")
    if mismatches:
        raise ProfileHotPathEquivalenceError(
            f"{case_label}: {', '.join(mismatches)} outputs differ"
        )


def verify_profile_hot_path_equivalence(
    root: Path,
    candidate_sha: str,
    *,
    runner: Runner = subprocess.run,
) -> EquivalenceResult:
    """Verify every frozen case and reject candidate state drift."""
    require_exact_candidate(root, candidate_sha, runner=runner)
    try:
        inventory = profile_language_cases.profile_language_inventory()
    except Exception as exc:
        raise ProfileHotPathEquivalenceError(
            "the profile language inventory could not be loaded"
        ) from exc

    try:
        for method in inventory.methods:
            with tempfile.TemporaryDirectory() as directory:
                fixture_root = Path(directory)
                package = profile_fixture.write_valid_profile_fixture(
                    fixture_root
                )
                for case in inventory.cases_for_method(method.method_name):
                    _compare_case(
                        fixture_root=fixture_root,
                        package=package,
                        case=case,
                    )
    except ProfileHotPathEquivalenceError:
        raise
    except Exception as exc:
        raise ProfileHotPathEquivalenceError(
            "profile comparison could not complete"
        ) from exc

    result = EquivalenceResult(
        candidate_sha=candidate_sha,
        method_count=len(inventory.methods),
        population_count=len(inventory.cases),
        population_sha256=inventory.population_sha256,
    )
    require_exact_candidate(root, candidate_sha, runner=runner)
    return result


def _parser() -> argparse.ArgumentParser:
    parser = _SafeArgumentParser(add_help=False)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--candidate-sha")
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    root: Path = ROOT,
) -> int:
    try:
        arguments = _parser().parse_args(argv)
        if not arguments.check or arguments.candidate_sha is None:
            raise ProfileHotPathEquivalenceError(
                "use --check with a full candidate SHA"
            )
        result = verify_profile_hot_path_equivalence(
            root, arguments.candidate_sha
        )
    except ProfileHotPathEquivalenceError as exc:
        print(f"profile equivalence failed: {exc}", file=sys.stderr)
        return 1
    except Exception:
        print(
            "profile equivalence failed: verification could not complete",
            file=sys.stderr,
        )
        return 1

    print(f"candidate_sha={result.candidate_sha}")
    print(f"method_count={result.method_count}")
    print(f"population_count={result.population_count}")
    print(f"population_sha256={result.population_sha256}")
    print("equivalence=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
