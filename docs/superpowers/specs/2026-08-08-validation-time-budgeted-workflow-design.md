# Validation time-budgeted workflow design

**Date:** 2026-08-08
**Status:** Approved design
**Baseline commit:** `a8f6885a1b7d504d8ad0b90bae65f9866811815c`
**Scope:** Validation planning, local shard execution, GitHub Actions run cancellation, and contributor guidance

## Purpose

Give contributors useful validation work that fits short sessions without weakening the repository's complete merge and publication gates. The workflow shall show which checks apply to a change, group them by time budget, and default to the complete route whenever it cannot classify a changed path safely.

The design responds to the practical difference between a short local work window and a publication candidate. It does not redefine the meaning of a passing release, reuse results after the branch head changes, or allow a quick check to stand in for a required complete gate.

## Current state

The repository has a complete, fixed test-shard partition in `tools/test-shards.json`. It assigns 33 tracked test modules to four shards: `profile_validation`, `qualified_review_evidence`, `mapping_review_bundle`, and `remaining`. `tools/test_shards.py` and `tools/validate_test_shards.py` enforce complete, single assignment.

GitHub Actions runs the four shards in parallel. The latest successful runs took about 7.5 minutes end to end, with the qualified-review shard setting the critical path at about 7 minutes 20 seconds. The profile shard took less than a minute, and the mapping and remaining shards each took about three minutes. The operational validation-gates job took about one minute.

Local `tools/run_test_shards.py --all` runs shards sequentially. The SHA-bound qualified-review equivalence verifier also runs its locked 28 cases serially. Full local discovery and release-evidence acquisition remain intentionally more expensive because they validate the complete candidate.

## Goals

1. A contributor with 15 minutes shall be able to run a conservative preflight and directly affected checks.
2. A contributor with 30 minutes shall be able to run the affected domain gate or a selected shard.
3. A contributor with one or two hours shall be able to schedule the standard complete local work, exact-SHA proof when needed, and independent review before publication.
4. The complete GitHub Actions matrix and operational gates shall remain the authoritative merge requirement for this increment.
5. An unknown, cross-cutting, generated, workflow, or validation-tool change shall escalate to the complete tier.

## Non-goals

- Reducing the required test population or weakening any existing merge, publication, release, renderer, link, or exact-SHA gate.
- Making the 28-case equivalence verifier resumable in this increment.
- Changing GitHub's required-check policy or its `fail-fast: false` diagnostic behavior.
- Treating elapsed time as a pass or fail condition.

## Selected design

### A fail-closed validation planner

Add a versioned path-to-validation manifest and a `tools/plan_validation.py` command. Given a comparison base and candidate, the command shall inspect changed tracked paths and print three command groups: `quick`, `standard`, and `publication`. It shall also print the routing reasons and documented, approximate durations.

The manifest shall map each supported path family to the smallest relevant preflight, validator, and test selection. Its rules shall be explicit and testable. A path with no rule, a deleted or renamed path the planner cannot classify, a tool or workflow change, generated-review evidence, or a path family marked cross-cutting shall select the complete route. The planner shall not suppress a required validator merely because no direct test module appears to cover the changed file.

The command shall have a machine-readable output mode for future automation, but its normal output shall be a short human-readable work plan. The output is advisory. It does not change which checks GitHub requires.

### Time tiers

The planner shall define these tiers.

| Tier | Intended window | Contents | Use |
|---|---|---|---|
| `quick` | About 5 to 15 minutes | `git diff --check`, shard-manifest validation, changed-path routing, and directly affected validators or test modules | Start of a short session and immediate feedback |
| `standard` | About 15 to 30 minutes | Selected complete shard or directly affected domain bundle, plus gates selected by the manifest | Before handoff or when there is time to investigate a domain change |
| `publication` | Candidate freeze | Every existing required local gate that applies, full test discovery where required, renderer and external-evidence gates, exact-SHA proof, and independent review | Pull-request publication, merge, and release work |

The documented durations are planning aids based on observed runs. They shall use ranges and shall not promise a completion time. The planner shall describe the qualified-review shard as a long domain gate and the exact equivalence verifier as a publication proof, not as a quick feedback command.

### Local parallel shard execution

Extend `tools/run_test_shards.py` with an explicit parallel all-shards mode. It shall preserve the current isolated subprocess model, shard-manifest validation, bounded failure diagnostics, exit semantics, and `PYTHONDONTWRITEBYTECODE=1` behavior. It shall collect a result for every selected shard rather than cancelling sibling shards after the first failure.

The existing sequential `--all` behavior shall remain available for deterministic diagnosis. The parallel mode shall be opt-in and shall not change the commands used by GitHub Actions. Its output shall state the selected mode, each shard's elapsed time, and the overall result.

### Obsolete CI run cancellation

Add workflow-level GitHub Actions concurrency keyed to the pull request or branch reference, with `cancel-in-progress: true`. A newer commit shall cancel only older runs for the same key. Runs for different pull requests and the protected `main` branch shall not cancel one another.

The unit-test matrix shall keep `fail-fast: false`. That setting preserves independent failure diagnostics inside the current run. Workflow-level concurrency saves time and capacity only when a newer candidate supersedes an older one.

### Contributor guidance

Update `tools/README.md` and the development workflow in `AGENTS.md` with the tier commands, escalation rules, and short-session examples. The guidance shall state that a passing quick or standard tier never carries forward after `HEAD` changes and never replaces the full pull-request or publication gate.

## Interfaces

### Validation routing manifest

The manifest shall be a JSON file under `tools/` with a versioned schema. Every rule shall declare:

- a stable identifier;
- one or more repository-relative path prefixes or exact paths;
- the quick commands;
- the standard commands;
- whether the rule is cross-cutting and therefore escalates to publication; and
- a plain-language reason shown by the planner.

The schema shall reject duplicate identifiers, unsupported command identifiers, empty path selectors, overlapping ambiguous exact selectors, and an unrecognized schema version. The planner shall sort output deterministically.

Commands shall be named from a fixed internal catalog rather than accepted as arbitrary shell text. The catalog shall define the executable command, tier availability, approximate duration label, and whether it needs a comparison base. This keeps the manifest declarative and prevents a changed path from injecting a command.

### Planner command

`tools/plan_validation.py` shall accept an explicit base reference and candidate reference. It shall refuse to plan when either cannot resolve to a Git commit or when the comparison cannot produce a tracked-path diff. It shall accept a `--format text|json` option and a tier selector for callers that want one tier only.

When invoked without an explicit candidate, it may use `HEAD`. It shall print the resolved base and candidate so contributors can see whether the plan applies to their current work.

## Error handling

The planner shall fail closed. It shall return a nonzero exit code for an invalid manifest, unresolved Git reference, malformed machine-readable request, or path classification ambiguity. For an otherwise valid diff containing an unknown or intentionally cross-cutting path, it shall return a successful plan that selects the complete route and names the escalation reason.

The parallel runner shall return nonzero if any selected shard fails or cannot start. It shall preserve enough per-shard output to identify the failure without relying on interleaved terminal output.

## Verification

Implementation shall follow test-driven development.

1. Add failing tests for valid routing, unknown-path escalation, cross-cutting escalation, renamed and deleted paths, invalid manifests, deterministic text and JSON output, and candidate/base reporting.
2. Add failing tests for parallel shard selection, per-shard result accounting, mixed success and failure behavior, and preservation of sequential mode.
3. Implement the manifest validator, planner, and parallel runner until the focused tests pass.
4. Add workflow tests or static assertions for the concurrency group and `cancel-in-progress` setting while preserving matrix `fail-fast: false`.
5. Run the planner against representative documentation, architecture, crosswalk, qualified-review, workflow, and unknown-path changes.
6. Run the existing shard-manifest validation, selected shard tests, full test discovery, affected standalone validators, Mermaid rendering when the guidance changes, link validation, and whole-branch hygiene checks.
7. Have an independent reviewer confirm that every unknown or cross-cutting change escalates and that no quick or standard route makes a publication claim.

## Acceptance criteria

This increment is accepted when:

1. Contributors can request a deterministic quick, standard, or publication validation plan for a base and candidate.
2. The planner routes known paths to documented commands and escalates any unclassified or cross-cutting path to publication.
3. The manifest and planner are covered by focused fail-closed tests.
4. Local all-shard parallel mode reports every selected shard and preserves the current sequential diagnostic mode.
5. A newer run cancels only obsolete workflow runs with the same concurrency key.
6. GitHub's matrix still collects independent failures with `fail-fast: false`, and the complete GitHub gate remains required.
7. The documentation explains time tiers without presenting duration estimates as guarantees or allowing earlier results to survive a new candidate SHA.

## Alternatives considered

### Change GitHub matrix fail-fast to true

This would stop sibling shards after the first failure. It would not shorten a successful run, and it would remove useful independent diagnostics. The existing `fail-fast: false` behavior stays.

### Skip expensive GitHub checks from a path filter

Path-based skipping would weaken the current merge policy unless the routing rules have already been proven fail-closed and accepted as a governance change. This increment keeps the complete GitHub check intact and uses routing first for local planning.

### Split or resume the exact equivalence verifier now

Case-level diagnostics would be useful later, but the verifier binds all 28 cases to one exact candidate SHA and population digest. The first increment should deliver conservative planning and local shard parallelism without changing that proof boundary.
