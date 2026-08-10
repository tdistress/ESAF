# Validation time-budgeted workflow implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let contributors select conservative validation work that fits a short session while preserving complete CI and publication assurance.

**Architecture:** A strict JSON manifest maps changed repository paths to named commands from a fixed catalog. `tools/plan_validation.py` resolves a Git base and candidate, parses the tracked-path diff, and emits deterministic quick, standard, and publication plans. The shard runner gains an opt-in parallel mode, and the workflow cancels only obsolete runs for the same PR or branch.

**Tech Stack:** Python 3.13 standard library, `unittest`, JSON, Git, GitHub Actions YAML, Markdown.

## Global constraints

- Preserve `tools/test-shards.json` as the authoritative complete, exactly-once test partition.
- Keep GitHub Actions matrix `fail-fast: false` and the `Validate ESAF sources` aggregate job unchanged.
- Treat unknown, renamed, deleted, cross-cutting, workflow, and validation-tool changes as publication-tier routes.
- Do not reuse a quick or standard result after the candidate SHA changes.
- Use fixed command identifiers in the routing manifest. Never execute shell text from manifest data.
- Keep `tools/run_test_shards.py --all` sequential. Parallel execution is explicit and returns diagnostics for every selected shard.
- Use `PYTHONDONTWRITEBYTECODE=1` for Python validation and verify no cache directories before publication.

---

## File map

| File | Responsibility |
|---|---|
| `tools/validation-plans.json` | Versioned routing manifest and named command catalog |
| `tools/plan_validation.py` | Strict manifest loading, Git diff classification, plan selection, and CLI rendering |
| `tests/test_plan_validation.py` | Fail-closed manifest, Git, routing, and output tests |
| `tools/run_test_shards.py` | Opt-in local parallel all-shards execution |
| `tests/test_validation_shards.py` | Parallel runner and workflow contract tests |
| `.github/workflows/catalog-validation.yml` | Concurrency cancellation and planner-path CI triggers |
| `tests/test_esaf_1600_foundation.py` | Expected workflow trigger paths |
| `tools/README.md` and `AGENTS.md` | Contributor commands, escalation rules, and result-expiry guidance |

## Task 1: Add the fail-closed routing manifest and planner

**Files:**

- Create: `tools/validation-plans.json`
- Create: `tools/plan_validation.py`
- Create: `tests/test_plan_validation.py`

**Interfaces:**

- Consumes: `git diff --name-status -z <base> <candidate>` and fixed command identifiers.
- Produces: `load_manifest(root) -> ValidationManifest` and `plan_validation(root, *, base, candidate, git_runner=None) -> ValidationPlan`.

- [ ] **Step 1: Write failing planner tests**

Create temporary manifests with schema `esaf-validation-plans-v1`. Test known documentation and qualified-review routing, unknown-path escalation, cross-cutting workflow escalation, deletion, rename, duplicate JSON keys, duplicate rule IDs, unknown command IDs, empty selectors, ambiguous exact selectors, unresolved references, malformed NUL diff output, deterministic text and JSON rendering, tier filtering, and resolved base/candidate reporting.

```python
def test_unknown_path_escalates_to_publication(self) -> None:
    plan = plan_validation(
        ROOT,
        base="base",
        candidate="candidate",
        git_runner=self.git_diff_for(b"M\\0new-area/file.md\\0"),
    )
    self.assertEqual(("publication",), plan.selected_tiers)
    self.assertIn("unclassified path", plan.reasons)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -B -m unittest tests/test_plan_validation.py -v`

Expected: FAIL because the planner and manifest do not exist.

- [ ] **Step 3: Add the declarative manifest**

Add a root `commands` catalog containing only fixed identifiers. Each command records its argv tuple, available tier, and duration label. Add ordered path rules for documentation, architecture, assessment, controls, crosswalks, profiles, qualified review, mapping review, and broad workflow/tool paths. Mark workflow and broad tool rules cross-cutting. Do not include executable shell text in rules.

- [ ] **Step 4: Implement strict loading and immutable plan types**

Reuse the duplicate-key JSON pattern from `tools/test_shards.py`. Define frozen records:

```python
@dataclass(frozen=True)
class ValidationCommand:
    identifier: str
    argv: tuple[str, ...]
    tier: str
    duration: str

@dataclass(frozen=True)
class ValidationPlan:
    base: str
    candidate: str
    changed_paths: tuple[str, ...]
    selected_tiers: tuple[str, ...]
    commands: tuple[ValidationCommand, ...]
    reasons: tuple[str, ...]
```

Reject malformed schema, duplicate identifiers, invalid selectors, unknown commands, empty argv values, and ambiguous exact selectors before Git execution.

- [ ] **Step 5: Implement conservative Git routing and the CLI**

Resolve both refs with `git rev-parse --verify <ref>^{commit}`. Parse name-status NUL records for `A`, `M`, `D`, and `R`. An unclassified, malformed, renamed, deleted, or cross-cutting path selects publication with a reason. Add `--base REF`, optional `--candidate REF` defaulting to `HEAD`, `--tier`, and `--format text|json`. Text includes resolved refs, reasons, commands, and duration labels. JSON has sorted keys and a trailing newline.

- [ ] **Step 6: Run focused planner tests**

Run: `python -B -m unittest tests/test_plan_validation.py -v`

Expected: PASS, including fail-closed error handling.

- [ ] **Step 7: Commit**

```powershell
git add tools/validation-plans.json tools/plan_validation.py tests/test_plan_validation.py
git commit -m "feat: plan validation by time budget"
```

## Task 2: Add explicit local parallel shard execution

**Files:**

- Modify: `tools/run_test_shards.py:91-216`
- Modify: `tests/test_validation_shards.py:379-565`

**Interfaces:**

- Consumes: existing `Shard`, `ShardResult`, `run_shard`, and validated shard tuple.
- Produces: `run_all_parallel(root, shards, durations, ...) -> tuple[ShardResult, ...]` and a CLI mode valid only with `--all`.

- [ ] **Step 1: Write failing parallel tests**

Add injected-runner tests that verify every selected shard starts, every result remains available if one fails, emitted records use manifest order even when workers finish out of order, and sequential `run_all` remains unchanged. Require `--parallel` without `--all` to be rejected. Require the runner to print selected mode and overall elapsed time.

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -B -m unittest tests/test_validation_shards.py -v`

Expected: FAIL because the parallel API and CLI option are absent.

- [ ] **Step 3: Implement the parallel API**

Add `run_all_parallel` using `concurrent.futures.ThreadPoolExecutor`, one `run_shard` call per selected shard. Collect every future and preserve each failure. Reorder results to manifest order before using existing result and bounded-summary rendering. Convert an unexpected worker exception into a clear runner failure without cancelling sibling futures.

- [ ] **Step 4: Add the explicit CLI mode**

Add a `--parallel` boolean. Retain sequential behavior for `--all` without it, reject the option for `--shard`, and preserve all existing subprocess isolation, `PYTHONDONTWRITEBYTECODE`, and exit behavior. Print `Mode: sequential` or `Mode: parallel` and `Overall elapsed seconds: ...`.

- [ ] **Step 5: Run focused shard tests**

Run: `python -B -m unittest tests/test_validation_shards.py -v`

Expected: PASS, including the existing bounded diagnostic test.

- [ ] **Step 6: Commit**

```powershell
git add tools/run_test_shards.py tests/test_validation_shards.py
git commit -m "feat: run local test shards in parallel"
```

## Task 3: Cancel obsolete CI runs without losing diagnostics

**Files:**

- Modify: `.github/workflows/catalog-validation.yml:1-225`
- Modify: `tests/test_validation_shards.py:252-376`
- Modify: `tests/test_esaf_1600_foundation.py:436-491`

**Interfaces:**

- Consumes: the current four-shard matrix and aggregate job.
- Produces: a concurrency group that separates pull requests and branch refs.

- [ ] **Step 1: Write failing workflow contract tests**

Require this exact top-level workflow object:

```python
{
    "group": "${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}",
    "cancel-in-progress": "true",
}
```

Extend expected pull-request and push path arrays with the two planner files. Continue asserting the four-shard matrix with `fail-fast: false` and the unchanged aggregate job.

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -B -m unittest tests/test_validation_shards.py tests/test_esaf_1600_foundation.py -v`

Expected: FAIL because concurrency and planner trigger paths are absent.

- [ ] **Step 3: Update the workflow**

Add top-level concurrency after `permissions`. Add each planner file exactly once to each existing pull-request and push path list. Do not alter matrix content, `fail-fast`, operational gates, aggregate-job dependencies, or check names.

- [ ] **Step 4: Run workflow contract tests**

Run: `python -B -m unittest tests/test_validation_shards.py tests/test_esaf_1600_foundation.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add .github/workflows/catalog-validation.yml tests/test_validation_shards.py tests/test_esaf_1600_foundation.py
git commit -m "ci: cancel superseded validation runs"
```

## Task 4: Document the tiers and validate end to end

**Files:**

- Modify: `tools/README.md:91-104`
- Modify: `AGENTS.md:33-43`
- Test: `tests/test_plan_validation.py`

**Interfaces:**

- Consumes: final planner CLI and parallel runner.
- Produces: guidance that matches the tested commands and does not overstate assurance.

- [ ] **Step 1: Add a narrow executable-interface assertion if useful**

If the repository's documentation tests support it, assert only that the planner help and examples remain executable. Do not freeze prose line by line. The examples must be:

```powershell
python tools/plan_validation.py --base origin/main --candidate HEAD
python tools/run_test_shards.py --all --parallel --durations 50
```

- [ ] **Step 2: Run new focused tests to verify failure**

Run: `python -B -m unittest tests/test_plan_validation.py -v`

Expected: FAIL only when a new executable-interface assertion was added.

- [ ] **Step 3: Update the human-facing guidance**

Document quick, standard, and publication use in `tools/README.md`. State that estimates are planning aids, unknown and cross-cutting paths escalate, and a new candidate SHA invalidates earlier results. Add the matching durable workflow rule to `AGENTS.md`.

- [ ] **Step 4: Run focused checks and representative commands**

```powershell
python -B -m unittest tests/test_plan_validation.py tests/test_validation_shards.py tests/test_esaf_1600_foundation.py -v
python tools/validate_test_shards.py --check
python tools/plan_validation.py --base HEAD~1 --candidate HEAD
python tools/run_test_shards.py --all --parallel --durations 50
```

Expected: tests pass, the manifest remains complete, the planner prints a conservative plan, and all shard records appear.

- [ ] **Step 5: Run publication validation**

Run full test discovery and every affected standalone validator. Render Mermaid and validate links because workflow and contributor guidance changed. Run `git diff --check <merge-base>..HEAD`, verify no Python cache directories, and confirm the tested candidate still equals the final branch head.

- [ ] **Step 6: Commit**

```powershell
git add tools/README.md AGENTS.md
git commit -m "docs: explain time-budgeted validation"
```

## Plan self-review

- Spec coverage: Tasks 1 through 4 implement the planner, parallel execution, concurrency cancellation, guidance, and final validation. Required CI policy stays unchanged.
- Placeholder scan: Every task identifies files, contracts, tests, commands, and expected results.
- Type consistency: Task 1 owns `ValidationCommand` and `ValidationPlan`. Task 2 adds `run_all_parallel` without changing the sequential `run_all` contract.
