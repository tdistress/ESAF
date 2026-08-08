#!/usr/bin/env python3
"""Compare qualified-review full, narrow, and expected policy results."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.qualified_review_hot_path_support import (  # noqa: E402
    QualifiedReviewHotPathFixture,
    ReportProjection,
    expected_projection,
    run_full_case,
    run_narrow_case,
)
from tests.qualified_review_policy_cases import (  # noqa: E402
    qualified_review_policy_inventory,
)


GitRunner = Callable[..., subprocess.CompletedProcess[bytes]]
run_git: GitRunner = subprocess.run


@dataclass(frozen=True)
class EquivalenceResult:
    candidate_sha: str
    method_count: int
    population_count: int
    population_sha256: str
    full_comparison_count: int
    narrow_comparison_count: int


class QualifiedReviewHotPathEquivalenceError(RuntimeError):
    """Report a verifier failure without exposing checkout or fixture paths."""


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise QualifiedReviewHotPathEquivalenceError(
            "command arguments are invalid"
        )


def _inspect_git(
    root: Path,
    arguments: list[str],
    *,
    runner: GitRunner,
) -> subprocess.CompletedProcess[bytes]:
    try:
        result = runner(
            arguments,
            cwd=root,
            shell=False,
            capture_output=True,
        )
    except Exception as error:
        raise QualifiedReviewHotPathEquivalenceError(
            "Git could not inspect the candidate checkout"
        ) from error
    if result.returncode != 0:
        raise QualifiedReviewHotPathEquivalenceError(
            "Git could not inspect the candidate checkout"
        )
    if result.stderr != b"":
        raise QualifiedReviewHotPathEquivalenceError(
            "Git returned an unexpected candidate-check error"
        )
    if not isinstance(result.stdout, bytes):
        raise QualifiedReviewHotPathEquivalenceError(
            "Git returned an invalid candidate-check response"
        )
    return result


def require_exact_candidate(
    root: Path,
    candidate_sha: str,
    runner: GitRunner = run_git,
) -> None:
    """Require a clean checkout whose HEAD is the exact supplied commit."""
    if re.fullmatch(r"[0-9a-f]{40}", candidate_sha) is None:
        raise QualifiedReviewHotPathEquivalenceError(
            "candidate SHA must contain 40 lowercase hexadecimal characters"
        )

    head = _inspect_git(
        root,
        ["git", "rev-parse", "HEAD"],
        runner=runner,
    )
    if head.stdout != (candidate_sha + "\n").encode("ascii"):
        raise QualifiedReviewHotPathEquivalenceError(
            "candidate SHA does not match the checkout HEAD"
        )

    status = _inspect_git(
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
        raise QualifiedReviewHotPathEquivalenceError(
            "candidate checkout contains uncommitted files"
        )


def _safe_case_id(case_id: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_.:-]+", case_id) is None:
        return "unknown_case"
    return case_id


def _reject_temporary_paths(
    projection: ReportProjection,
    temporary_roots: Sequence[Path],
    case_id: str,
) -> None:
    if not isinstance(projection, ReportProjection):
        raise QualifiedReviewHotPathEquivalenceError(
            f"{case_id}: a comparison returned an invalid projection"
        )
    values = (
        projection.readiness_name,
        projection.candidate_commit,
        projection.campaign_id,
        *projection.errors,
    )
    for value in values:
        if not isinstance(value, str):
            raise QualifiedReviewHotPathEquivalenceError(
                f"{case_id}: a comparison returned a non-text diagnostic"
            )
        folded = value.casefold()
        normalized = folded.replace("\\", "/")
        for root in temporary_roots:
            native_root = str(root.resolve()).casefold()
            slash_root = native_root.replace("\\", "/")
            if native_root in folded or slash_root in normalized:
                raise QualifiedReviewHotPathEquivalenceError(
                    f"{case_id}: a diagnostic contains a temporary path"
                )


def _require_pairwise_equivalence(
    case_id: str,
    full: ReportProjection,
    narrow: ReportProjection,
    expected: ReportProjection,
) -> None:
    pairs = (
        ("full", full, "narrow", narrow),
        ("full", full, "expected", expected),
        ("narrow", narrow, "expected", expected),
    )
    mismatches = [
        f"{left_name}/{right_name}"
        for left_name, left, right_name, right in pairs
        if left != right
    ]
    if mismatches:
        raise QualifiedReviewHotPathEquivalenceError(
            f"{case_id}: {', '.join(mismatches)} outputs differ; "
            f"full={full!r}; narrow={narrow!r}; expected={expected!r}"
        )


def verify_qualified_review_hot_path_equivalence(
    root: Path,
    candidate_sha: str,
    *,
    runner: GitRunner = run_git,
) -> EquivalenceResult:
    """Compare the frozen population and reject candidate state drift."""
    require_exact_candidate(root, candidate_sha, runner=runner)
    try:
        inventory = qualified_review_policy_inventory()
    except Exception as error:
        raise QualifiedReviewHotPathEquivalenceError(
            "the qualified-review policy inventory could not be loaded"
        ) from error

    full_comparison_count = 0
    narrow_comparison_count = 0
    try:
        with tempfile.TemporaryDirectory() as fixture_directory:
            fixture_root = Path(fixture_directory)
            fixture = QualifiedReviewHotPathFixture.create(fixture_root, root)
            for case in inventory.cases:
                case_id = _safe_case_id(case.case_id)
                with tempfile.TemporaryDirectory() as case_directory:
                    case_root = Path(case_directory)
                    destination = case_root / case_id
                    full = run_full_case(fixture, case, destination)
                    full_comparison_count += 1
                    narrow = run_narrow_case(fixture, case)
                    narrow_comparison_count += 1
                    expected = expected_projection(fixture, case)
                    temporary_roots = (fixture_root, case_root)
                    for projection in (full, narrow, expected):
                        _reject_temporary_paths(
                            projection,
                            temporary_roots,
                            case_id,
                        )
                    _require_pairwise_equivalence(
                        case_id,
                        full,
                        narrow,
                        expected,
                    )
    except QualifiedReviewHotPathEquivalenceError:
        raise
    except Exception as error:
        raise QualifiedReviewHotPathEquivalenceError(
            "qualified-review comparison could not complete"
        ) from error

    result = EquivalenceResult(
        candidate_sha=candidate_sha,
        method_count=len({case.method_name for case in inventory.cases}),
        population_count=len(inventory.cases),
        population_sha256=inventory.population_sha256,
        full_comparison_count=full_comparison_count,
        narrow_comparison_count=narrow_comparison_count,
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
            raise QualifiedReviewHotPathEquivalenceError(
                "use --check with a full candidate SHA"
            )
        result = verify_qualified_review_hot_path_equivalence(
            root,
            arguments.candidate_sha,
        )
        if (
            result.method_count != 16
            or result.population_count != 31
            or result.full_comparison_count != 31
            or result.narrow_comparison_count != 31
            or re.fullmatch(r"[0-9a-f]{64}", result.population_sha256) is None
        ):
            raise QualifiedReviewHotPathEquivalenceError(
                "verification returned an invalid equivalence result"
            )
    except QualifiedReviewHotPathEquivalenceError as error:
        print(f"qualified-review equivalence failed: {error}", file=sys.stderr)
        return 1
    except Exception:
        print(
            "qualified-review equivalence failed: verification could not complete",
            file=sys.stderr,
        )
        return 1

    print(f"candidate_sha={result.candidate_sha}")
    print("method_count=16")
    print("population_count=31")
    print(f"population_sha256={result.population_sha256}")
    print("full_comparison_count=31")
    print("narrow_comparison_count=31")
    print("equivalence=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
