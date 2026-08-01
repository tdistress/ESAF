# Validation Harness Efficiency Design

**Date:** 2026-08-01
**Status:** Approved design
**Scope:** ESAF repository testing, release-evidence validation, and CI defaults

## Purpose

Reduce validation wall time and wasted reruns without weakening ESAF's publication
assurance. The optimized harness shall preserve exact commit and tree binding,
fail-closed GitHub acquisition, complete test coverage, operational validator
execution, pinned Mermaid rendering, independent visual review, and clean-worktree
requirements.

## Evidence and problem statement

Eight recent GitHub Actions runs spent between 507 and 769 seconds in
`python -m unittest discover -s tests -v`, with a median of 751 seconds. In the
latest merge run, the unit-test step consumed 763 seconds while all standalone
validators, Mermaid rendering, and link validation together consumed less than
one minute.

Timestamp analysis of the 1,251 test completions attributed approximately:

- 235 seconds to `test_validate_profiles`;
- 221 seconds to `test_validate_qualified_review_evidence`;
- 151 seconds to `test_build_mapping_review_bundle`;
- 60 seconds to `test_v05_beta_release_gates`; and
- 49 seconds to `test_validate_crosswalks`.

The first three modules account for approximately 79 percent of hosted unit-test
time. Windows release collection is slower still because the tests perform many
small filesystem operations and Git subprocesses.

The taggable evidence controller currently performs a fresh full candidate
validation and a second full merge-head validation even after it has validated
base candidate evidence and proved that the merge tree equals the candidate
tree. This can execute two long suites in one taggable collection.

Two operational defects amplify the cost:

1. clean-status and `__pycache__` checks run after the expensive command set, so
   an invalid precondition can waste a complete suite; and
2. failed commands capture stdout and stderr but discard them, forcing a second
   long run to identify the failing test.

Unit tests also depend unintentionally on ambient repository tags. A legitimate
post-publication `v0.5-beta` tag therefore changes otherwise synthetic collector
tests across every linked worktree.

## Assurance invariants

The efficiency work shall not remove or weaken these controls:

1. Every release command result shall remain bound to an exact 40-character
   commit SHA and its verified tree.
2. Candidate evidence shall retain the canonical command set and successful
   results produced before merge.
3. The merge commit shall remain distinct from the candidate commit, shall have
   the authenticated candidate as an ancestor or parent as required, and shall
   have a tree exactly equal to the approved candidate tree.
4. At least one complete local suite shall execute for every distinct release
   content tree used in a publication transition.
5. Commit- and history-sensitive validators shall execute for each required SHA
   even when two SHAs share a tree.
6. Canonical GitHub Actions checks shall remain required and shall be acquired
   from the authenticated GitHub Actions application and exact workflow run.
7. GitHub resources shall still be reacquired after long-running validation so
   the 15-minute freshness window applies to the final evidence.
8. All 23 Mermaid blocks shall still render with Node 22.23.1 and
   `@mermaid-js/mermaid-cli@11.16.0`; parser success shall not replace visual
   review.
9. Assessment, profile, architecture, control, crosswalk, release, link, and
   generated-artifact validators shall remain default gates.
10. The working tree and generated-cache checks shall pass both before and after
    release validation.
11. Synthetic tests shall control repository and tag state explicitly. Only
    tests of the operational local-tag guard may consult a real local tag.

## Phase 1: Release orchestration and diagnostics

### Preflight and postflight

`LocalValidationRunner` shall execute read-only preflight checks for a clean
worktree and zero `__pycache__` directories before `full_suite`. It shall retain
the existing final `cache_count` and `clean_status` command records so evidence
still proves that validation itself left no generated state.

Preflight failures shall occur before any expensive command and shall identify
the exact offending relative paths without changing or deleting them.

### Actionable failure output

Every subprocess failure shall report:

- the canonical command identifier;
- its exit code; and
- a bounded, UTF-8-safe tail of combined stdout and stderr.

The bounded tail shall be large enough to contain a unittest failure summary but
shall not store unbounded logs in release evidence. Successful evidence shall
continue to record only the stable result contract, not transient command text.

The default full-suite command shall add `--durations 50`. CI shall use the same
option. Timing output is diagnostic only and shall not change pass/fail semantics.

### Taggable candidate replay

Taggable collection shall validate the base candidate command set structurally,
bind it to the exact closure SHA and closure base, and replay those immutable
results while reacquiring candidate GitHub sources. It shall not execute the
candidate full suite a second time.

The merge-head detached validation shall remain mandatory. The controller shall
then reacquire candidate, merge, post-merge rendering, check-run, issue, comment,
and tag resources after merge validation. This preserves current freshness and
TOCTOU defenses while removing one duplicate full suite.

If candidate commands, candidate sources, closure base, merge tree, or merge
identity differ from the authenticated base evidence, collection shall fail
closed rather than fall back to a fresh candidate execution.

### Ambient-state isolation

Collector unit-test fixtures shall provide an explicit repository runner whose
local-tag result is controlled by the test. The existing operational CLI and
dedicated local-tag tests shall continue to use the real repository guard.

This makes the suite valid both before and after publication without permitting
the operational collector to ignore a real local tag.

## Phase 2: Test and Git hot-path optimization

### Completeness-checked test shards

The repository shall define four deterministic unit-test shards:

1. profile validation;
2. qualified-review evidence;
3. mapping-review bundle construction; and
4. all remaining test modules.

A manifest validator shall discover every tracked `tests/test_*.py` file and
require each file to appear in exactly one shard. Missing, duplicate, renamed,
or untracked shard entries shall fail the harness.

GitHub Actions shall run the four shards in parallel and expose one aggregate
required check. Local validation may run shards in parallel only when each shard
uses an independent process and its tests do not write into the repository.
Release evidence shall require all shard results before recording `full_suite`
as passed.

### Git object batching

`GitReader` shall build one verified tree index per exact commit. The index shall
retain canonical path, mode, object type, and object ID. Blob contents shall be
read through a bounded `git --no-replace-objects cat-file --batch` session or an
equivalent exact-object batch interface instead of starting `ls-tree` and
`git show` for every file.

The implementation shall preserve:

- full lowercase SHA resolution;
- canonical relative-path checks;
- rejection of symlinks, submodules, trees, missing paths, duplicates, and
  non-regular modes;
- exact blob bytes; and
- fail-closed behavior when the batch process, object identity, or output framing
  is invalid.

### Focused exhaustive matrices

Exhaustive language and evidence mutation matrices shall call the smallest pure
diagnostic boundary that implements the rule. Each rule family shall retain
representative end-to-end tests through the complete repository validator.

The refactor shall not reduce the number of tested phrase combinations,
severities, dispositions, mapping sets, roles, archive mutations, or source
identity cases. It shall reduce repeated fixture copying, JSON/YAML parsing,
repository traversal, archive construction, and full-campaign validation when
those operations are not the subject of the case.

## Data flow

The optimized publication flow is:

1. preflight the exact candidate checkout;
2. execute the complete candidate suite and canonical validators once;
3. reacquire fresh candidate GitHub evidence and persist closure evidence;
4. merge only after exact-head reviews, decisions, CI, and clean merge state;
5. prove merge-tree equality and record authenticated post-merge rendering;
6. replay the immutable candidate command results while reacquiring candidate
   sources;
7. execute the complete suite and commit-sensitive validators for the merge
   head;
8. reacquire all GitHub and tag resources;
9. validate taggable evidence; and
10. create the annotated tag only after every gate passes.

## Error handling and observability

- Each command shall emit start, completion, elapsed time, and result to the
  operator stream while preserving stable evidence fields.
- Failure diagnostics shall include a bounded output tail and the temporary
  detached-worktree path while that path still exists.
- Detached-worktree cleanup shall run after diagnostics are captured.
- Parallel shards shall report their individual module lists and durations.
- CI shall publish the 50 slowest test durations for performance regression
  review.
- Harness tests shall enforce command completeness, preflight ordering, bounded
  diagnostics, candidate replay, post-merge execution, and shard completeness.

## Performance acceptance criteria

Phase 1 is accepted when:

1. a dirty worktree or generated cache fails before `full_suite` is invoked;
2. a synthetic failing suite exposes its unittest failure summary without a
   diagnostic rerun;
3. taggable collection executes zero candidate validation commands and exactly
   one merge-head validation command set;
4. closure and taggable evidence remain valid under the official gates; and
5. the collector tests pass with a real local `v0.5-beta` tag present.

Phase 2 is accepted when:

1. the shard manifest covers every test module exactly once;
2. all shards together execute the same test population as discovery;
3. the three dominant modules retain their full input-case populations;
4. batched Git reads return byte-identical packages and reject every existing
   adversarial path/object case; and
5. hosted full-suite wall time decreases by at least 40 percent relative to the
   751-second eight-run median, measured over three successful runs.

## Non-goals

- Removing tests, mutation cases, operational validators, Mermaid renders, or
  exact-SHA review requirements.
- Treating a cache hit as proof that a command passed.
- Trusting caller-supplied validation results that are not already bound by
  validated closure evidence.
- Disabling antivirus, filesystem security, Git object checks, or fail-closed
  behavior for speed.
- Changing ESAF normative content, control inventories, mapping relationships,
  or publication claims.

## Rollout

Phase 1 shall land first because it removes the largest duplicate operation and
improves failure diagnosis with a small assurance surface. Phase 2 shall land in
separate reviewable commits: shard completeness, Git batching, profile hot-path
tests, qualified-review hot-path tests, and bundle hot-path tests. Each commit
shall retain the old path until focused equivalence tests pass, then remove only
the superseded implementation.
