# Task 7 report: planner candidate and publication contract

## Result

The validation planner now binds preflight and qualified-review equivalence
commands to the resolved candidate SHA, requires that SHA to equal a clean
checked-out `HEAD`, and rejects a base that is not its ancestor. It ignores
untracked files while checking tracked checkout cleanliness.

The manifest now uses `python tools/validate_links.py --check`, includes link
validation for ordinary documentation at standard, routes publication evidence
and `VERSION.md` changes to publication, and retains only the executable
`qualified-review-shard` for qualified-review paths. Generic human-evidence
validation is no longer emitted as a planner command.

`tools/README.md` documents the clean checked-out candidate contract and the
fact that unrelated untracked artifacts are left alone.

## Test-driven development record

1. Added contract tests for exact preflight, links, and equivalence argv;
   qualification route command identity; publication routes; checkout-candidate
   mismatch; tracked dirtiness; and non-ancestor bases.
2. Ran `python -m unittest tests.test_plan_validation -v` before implementation.
   It failed with six expected failures: stale catalog content, missing
   publication routing, and absent state guards.
3. Added only the required manifest bindings/routes and planner Git checks.
4. Re-ran the focused suite successfully: 12 tests passed.

## Preserved workspace state

Existing untracked cache directories under `tests/`, `tools/`, and
`tools/crosswalks/` were preserved. No untracked installation artifact was
inspected or removed.

## Validation evidence

- `python -B -m unittest tests.test_plan_validation -v`
  - Passed: 12 tests.
- `python -B tools/validate_test_shards.py --check`
  - Passed: 34 tracked tests across all four manifest shards.
- `python -B tools/plan_validation.py --base HEAD~1 --candidate HEAD`
  - Passed: emitted a publication route for the validation-tool change,
    including SHA-bound preflight and equivalence argv.
- `python -B tools/plan_validation.py --base HEAD~1 --candidate HEAD --format json`
  - Passed: emitted the same resolved base/candidate bindings in JSON.
- `git diff --check HEAD~1..HEAD`
  - Passed.

## Concern

The repository-wide discovery command was additionally attempted with bytecode
generation disabled, but exceeded the interactive 60-second execution limit
without a test result. This corrective task therefore claims only the focused
planner and manifest evidence above, not a complete discovery pass.

## Round 1 follow-up: committed-manifest route coverage

Added `test_committed_catalog_routes_ordinary_docs_and_qualified_review_to_standard`.
Unlike the temporary-manifest fixture test, it invokes `plan_validation` with
the committed manifest at `ROOT`. It asserts an ordinary `docs/` path selects
the standard route containing `links`, and a
`crosswalks/qualified-review/` path selects the standard route containing
`qualified-review-shard`. Each assertion fixes the complete selected command
sequence, so removing either command from its committed rule fails the test.

This is coverage-only work: the committed manifest already had the required
behavior, so the new focused test passed on its first run (1 test).

- `python -B -m unittest tests.test_plan_validation -v`
  - Passed: 13 tests.
- `git diff --check`
  - Passed.
