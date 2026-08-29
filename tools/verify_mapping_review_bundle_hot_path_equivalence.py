#!/usr/bin/env python3
"""Compare mapping-review bundle narrow and expected policy results.

Stage 1 of the mapping-review bundle hot-path (see
`docs/superpowers/specs/2026-08-29-validation-harness-bundle-hot-path-design.md`)
seals the narrow-boundary proof before matrix migration. Every selected
inventory case is a pure-boundary reject: `_require_candidate_state`,
`_require_reviewed_findings`, or `validate_metadata_against_schema` raises a
`ValueError` before package-completeness work is the subject of the
assertion. For Stage 1, the "full" path and the "narrow" path both invoke
the same pure production boundary over the same reconstructed metadata
(full == narrow for policy helpers is documented as acceptable for Stage 1);
the comparison this tool performs is between that boundary result and the
frozen expected-error-regex oracle recorded in
`tests/mapping_review_bundle_policy_cases.py`.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.mapping_review_bundle_hot_path_support import (  # noqa: E402
    run_narrow_case,
)
from tests.mapping_review_bundle_policy_cases import (  # noqa: E402
    mapping_review_bundle_policy_inventory,
)


GitRunner = Callable[..., subprocess.CompletedProcess[bytes]]
run_git: GitRunner = subprocess.run


@dataclass(frozen=True)
class EquivalenceResult:
    candidate_sha: str
    method_count: int
    population_count: int
    population_sha256: str
    narrow_comparison_count: int


class MappingReviewBundleHotPathEquivalenceError(RuntimeError):
    """Report a verifier failure without exposing checkout details."""


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise MappingReviewBundleHotPathEquivalenceError(
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
        raise MappingReviewBundleHotPathEquivalenceError(
            "Git could not inspect the candidate checkout"
        ) from error
    if result.returncode != 0:
        raise MappingReviewBundleHotPathEquivalenceError(
            "Git could not inspect the candidate checkout"
        )
    if result.stderr != b"":
        raise MappingReviewBundleHotPathEquivalenceError(
            "Git returned an unexpected candidate-check error"
        )
    if not isinstance(result.stdout, bytes):
        raise MappingReviewBundleHotPathEquivalenceError(
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
        raise MappingReviewBundleHotPathEquivalenceError(
            "candidate SHA must contain 40 lowercase hexadecimal characters"
        )

    head = _inspect_git(
        root,
        ["git", "rev-parse", "HEAD"],
        runner=runner,
    )
    if head.stdout != (candidate_sha + "\n").encode("ascii"):
        raise MappingReviewBundleHotPathEquivalenceError(
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
        raise MappingReviewBundleHotPathEquivalenceError(
            "candidate checkout contains uncommitted files"
        )


def verify_mapping_review_bundle_hot_path_equivalence(
    root: Path,
    candidate_sha: str,
    *,
    runner: GitRunner = run_git,
) -> EquivalenceResult:
    """Compare the frozen population against the pure narrow boundaries."""
    require_exact_candidate(root, candidate_sha, runner=runner)
    try:
        inventory = mapping_review_bundle_policy_inventory()
    except Exception as error:
        raise MappingReviewBundleHotPathEquivalenceError(
            "the mapping-review bundle policy inventory could not be loaded"
        ) from error

    narrow_comparison_count = 0
    try:
        for case in inventory.cases:
            try:
                run_narrow_case(case)
            except ValueError as error:
                message = str(error)
            else:
                raise MappingReviewBundleHotPathEquivalenceError(
                    f"{case.case_id}: narrow boundary did not reject"
                )
            if re.search(case.expected_error_regex, message) is None:
                raise MappingReviewBundleHotPathEquivalenceError(
                    f"{case.case_id}: narrow error does not match the "
                    f"expected pattern; narrow={message!r}"
                )
            narrow_comparison_count += 1
    except MappingReviewBundleHotPathEquivalenceError:
        raise
    except Exception as error:
        raise MappingReviewBundleHotPathEquivalenceError(
            "mapping-review bundle comparison could not complete"
        ) from error

    result = EquivalenceResult(
        candidate_sha=candidate_sha,
        method_count=len({case.method_name for case in inventory.cases}),
        population_count=len(inventory.cases),
        population_sha256=inventory.population_sha256,
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
            raise MappingReviewBundleHotPathEquivalenceError(
                "use --check with a full candidate SHA"
            )
        result = verify_mapping_review_bundle_hot_path_equivalence(
            root,
            arguments.candidate_sha,
        )
        if (
            result.method_count != 5
            or result.population_count != 16
            or result.narrow_comparison_count != 16
            or re.fullmatch(r"[0-9a-f]{64}", result.population_sha256) is None
        ):
            raise MappingReviewBundleHotPathEquivalenceError(
                "verification returned an invalid equivalence result"
            )
    except MappingReviewBundleHotPathEquivalenceError as error:
        print(
            f"mapping-review bundle equivalence failed: {error}",
            file=sys.stderr,
        )
        return 1
    except Exception:
        print(
            "mapping-review bundle equivalence failed: "
            "verification could not complete",
            file=sys.stderr,
        )
        return 1

    print(f"candidate_sha={result.candidate_sha}")
    print("method_count=5")
    print("population_count=16")
    print(f"population_sha256={result.population_sha256}")
    print("narrow_comparison_count=16")
    print("equivalence=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
