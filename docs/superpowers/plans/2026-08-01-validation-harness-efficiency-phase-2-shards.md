# Validation harness efficiency Phase 2 shard implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Divide the complete ESAF unit-test population into four deterministic, completeness-checked shards without changing the canonical release-evidence contract.

**Architecture:** Store the shard assignment in one strict, versioned JSON manifest. A pure Python library validates the manifest against tracked Git files, a thin check command enforces it, and a separate runner executes one shard or all four in independent processes. GitHub Actions runs the four shards in parallel, keeps operational validators in a separate job, and exposes one aggregate check named `Validate ESAF sources`.

**Tech Stack:** Python 3.13, `unittest`, Git subprocesses, JSON, GitHub Actions YAML, Markdown.

## Global constraints

- Preserve the exact four shard identifiers and order: `profile_validation`, `qualified_review_evidence`, `mapping_review_bundle`, and `remaining`.
- Require every tracked `tests/test_*.py` module to appear exactly once.
- Keep the full test population and the input-case populations in the three dominant modules.
- Run every shard in an independent Python process with `PYTHONDONTWRITEBYTECODE=1`. Run local and release aggregate execution sequentially because this increment does not prove that every test is free of transient repository writes. Hosted CI may run one shard per isolated job in parallel.
- Preserve `COMMAND_IDS`, the four-field release command-result schema, exact SHA binding, preflight and postflight hygiene, bounded failure output, candidate replay, and post-merge validation.
- Keep `Validate ESAF sources` as the only GitHub check with that exact name.
- Keep assessment, profile, architecture, control, crosswalk, release, link, generated-artifact, and Mermaid checks as default gates.
- Use `--durations 50` for direct, local aggregate, release, and CI shard execution.
- Do not change normative ESAF content, artifact lifecycle state, mapping relationships, or publication claims.

---

## File structure

- Create `tools/test-shards.json`: authoritative ordered shard assignment.
- Create `tools/test_shards.py`: strict manifest loading, tracked-module discovery, and completeness validation.
- Create `tools/validate_test_shards.py`: thin `--check` command.
- Create `tools/run_test_shards.py`: one-shard and four-shard subprocess execution.
- Create `tests/test_validation_shards.py`: manifest, validator, runner, population, workflow, and release integration tests.
- Modify `tools/v05_beta_release_evidence.py` and its tests: replace monolithic discovery with the aggregate shard runner while preserving `full_suite` evidence.
- Modify `.github/workflows/catalog-validation.yml` and workflow-contract tests: add the shard matrix, operational gate job, and aggregate protected check.
- Modify `tools/README.md`: document direct and aggregate shard commands.

### Task 1: Add the strict shard manifest and completeness validator

**Files:**
- Create: `tools/test-shards.json`
- Create: `tools/test_shards.py`
- Create: `tools/validate_test_shards.py`
- Create: `tests/test_validation_shards.py`

**Interfaces:**
- Produces: `Shard(identifier: str, modules: tuple[str, ...])`.
- Produces: `load_manifest(root: Path) -> tuple[Shard, ...]`.
- Produces: `tracked_test_modules(root: Path, runner: Callable[..., object] | None = None) -> tuple[str, ...]`.
- Produces: `validate_manifest(root: Path, runner: Callable[..., object] | None = None) -> tuple[Shard, ...]`.
- Produces: `python tools/validate_test_shards.py --check`.

- [ ] **Step 1: Write failing schema and completeness tests**

Create `tests/test_validation_shards.py` with temporary-manifest tests that require:

```python
EXPECTED_SHARD_IDS = (
    "profile_validation",
    "qualified_review_evidence",
    "mapping_review_bundle",
    "remaining",
)

def test_repository_manifest_covers_every_tracked_module_once(self) -> None:
    shards = validate_manifest(ROOT)
    self.assertEqual(EXPECTED_SHARD_IDS, tuple(item.identifier for item in shards))
    assigned = [module for shard in shards for module in shard.modules]
    self.assertEqual(list(tracked_test_modules(ROOT)), sorted(assigned))
    self.assertEqual(len(assigned), len(set(assigned)))

def test_manifest_rejects_missing_duplicate_and_untracked_modules(self) -> None:
    # Build one temporary repository manifest for each mutation and assert
    # separate messages containing "missing", "duplicate", and "untracked".
```

Also require rejection of duplicate JSON keys, unknown fields, the wrong schema, the wrong shard order, unsorted modules, backslashes, absolute paths, `.` or `..` segments, and entries outside `tests/test_*.py`.

- [ ] **Step 2: Run the new test module and verify it fails**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validation_shards -v
```

Expected: FAIL because the manifest and validator modules do not exist.

- [ ] **Step 3: Add the exact manifest assignment**

Create `tools/test-shards.json` with schema `esaf-test-shards-v1`. Assign only `tests/test_validate_profiles.py` to `profile_validation`, only `tests/test_validate_qualified_review_evidence.py` to `qualified_review_evidence`, and only `tests/test_build_mapping_review_bundle.py` to `mapping_review_bundle`. Assign every other tracked test module, including `tests/test_validation_shards.py`, to `remaining`. Sort every module list lexically.

- [ ] **Step 4: Implement strict loading and Git-backed validation**

In `tools/test_shards.py`, parse JSON with an `object_pairs_hook` that rejects duplicate keys. Require the exact top-level keys `schema` and `shards`, exact shard keys `id` and `modules`, and the exact ordered identifiers. Validate every module as a canonical POSIX relative path matching `tests/test_*.py`.

Discover the source population without shell expansion:

```python
completed = command_runner(
    ["git", "ls-files", "-z", "--", "tests/test_*.py"],
    cwd=root,
    check=False,
    capture_output=True,
)
```

Require exit code zero and strict UTF-8 decoding. Compare the flattened manifest with the tracked set and report missing, duplicate, and untracked entries in one deterministic `ValueError`.

- [ ] **Step 5: Add the thin check command**

`tools/validate_test_shards.py --check` shall call `validate_manifest(ROOT)`, print the four shard counts and total tracked count, and return 0. A validation error shall print one concise message to stderr and return 1. Any invocation without `--check` shall be rejected by `argparse`.

- [ ] **Step 6: Stage the new tracked population, then run focused tests and the operational check**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
git add tools/test-shards.json tools/test_shards.py tools/validate_test_shards.py tests/test_validation_shards.py
python -m unittest tests.test_validation_shards -v
python tools/validate_test_shards.py --check
```

Expected: PASS. Staging makes the new test visible to `git ls-files`. The validator reports 33 tracked test modules, partitioned 1, 1, 1, and 30.

- [ ] **Step 7: Commit the manifest boundary**

```powershell
git add tools/test-shards.json tools/test_shards.py tools/validate_test_shards.py tests/test_validation_shards.py
git commit -m "test: define complete unit test shards"
```

### Task 2: Execute shards locally and through release validation

**Files:**
- Create: `tools/run_test_shards.py`
- Modify: `tests/test_validation_shards.py`
- Modify: `tools/v05_beta_release_evidence.py`
- Modify: `tests/test_v05_beta_release_evidence.py`

**Interfaces:**
- Consumes: `validate_manifest(root)` from Task 1.
- Produces: `python tools/run_test_shards.py --shard <id> --durations 50`.
- Produces: `python tools/run_test_shards.py --all --durations 50`.
- Produces: `ShardResult(identifier: str, modules: tuple[str, ...], elapsed_seconds: float, exit_code: int, stdout: bytes, stderr: bytes)`.
- Produces: `build_command(shard: Shard, durations: int) -> list[str]`.
- Produces: `run_shard(root: Path, shard: Shard, durations: int, runner: Callable[..., object] | None = None, clock: Callable[[], float] | None = None) -> ShardResult`.
- Produces: `run_all(root: Path, shards: tuple[Shard, ...], durations: int, runner: Callable[..., object] | None = None, clock: Callable[[], float] | None = None) -> tuple[ShardResult, ...]`.
- Preserves: one canonical release result named `full_suite` with `result: passed`.

- [ ] **Step 1: Add failing runner tests**

Add tests with an injected subprocess runner and clock that require:

```python
expected = [
    sys.executable,
    "-m",
    "unittest",
    *manifest_by_id["profile_validation"].modules,
    "-v",
    "--durations",
    "50",
]
```

Require `cwd=ROOT`, `shell=False`, `os.environ.copy()` with `PYTHONDONTWRITEBYTECODE=1`, captured byte output, complete module-list reporting, elapsed-time reporting, all four sequential calls under `--all`, and a nonzero aggregate result when any shard fails. Require a final failure-summary block written to stderr after all ordinary stderr. The complete encoded block, including every failed-shard heading, shall not exceed 32 KiB. Divide the remaining byte budget fairly among failed shards and retain the tail of each diagnostic. Add multiple noisy failures, including an early failure, and pass the runner's stdout and stderr through the collector's `stdout + stderr` tail behavior. Prove the final 32 KiB contains every failed shard identifier and each retained unittest summary.

- [ ] **Step 2: Add a failing population-equivalence test**

Load discovery with `unittest.defaultTestLoader.discover(ROOT / "tests")`. Load every manifest module with `unittest.defaultTestLoader.loadTestsFromNames()` after converting its path to a dotted module name. Flatten both suites to test IDs, remove an optional leading `tests.`, and require exact set equality and equal cardinality. This test shall prove that the manifest population matches discovery, not just that file counts match.

- [ ] **Step 3: Add failing release-runner expectations**

Change the expected `full_suite` command in `tests/test_v05_beta_release_evidence.py` to:

```python
[
    os.fsdecode(Path(os.sys.executable)),
    "tools/run_test_shards.py",
    "--all",
    "--durations",
    "50",
]
```

Update `FailingSuiteExecutor` and preflight-order assertions to recognize `tools/run_test_shards.py`. Keep the failure-tail, elapsed-time, exact command set, and stable evidence assertions unchanged.

- [ ] **Step 4: Run focused tests and verify the runner is absent**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validation_shards tests.test_v05_beta_release_evidence.V05LocalValidationRunnerTests -v
```

Expected: FAIL because `tools/run_test_shards.py` does not exist and `LocalValidationRunner` still invokes discovery.

- [ ] **Step 5: Implement independent subprocess execution**

In `tools/run_test_shards.py`, validate the manifest before starting tests. Each shard command shall use `sys.executable`, `shell=False`, repository-root `cwd`, captured bytes, and `os.environ.copy()` with `PYTHONDONTWRITEBYTECODE=1` set. The injected runner and clock shall default to `subprocess.run` and `time.monotonic`.

Use an `argparse` mutually exclusive required group for `--shard` and `--all`. Print the shard identifier, complete ordered module list, elapsed time, exit code, stdout, and stderr. For `--all`, execute each independent process sequentially in manifest order and continue after failures. After all ordinary output, write one final summary to stderr. Define `FAILURE_SUMMARY_BYTES = 32768`, reserve space for every failed-shard heading, divide the remaining bytes among failures, and append one tail excerpt per shard. Reject a heading set that alone exceeds the limit. Assert the final encoded summary is no larger than the limit before writing it. Exit nonzero if any shard failed. Reject `durations` below 1.

- [ ] **Step 6: Replace only the release full-suite command**

In `LocalValidationRunner`, replace the discovery arguments with the aggregate runner arguments from Step 3. Do not change `COMMAND_IDS`, evidence fields, result values, or any other command.

- [ ] **Step 7: Run the three dominant shards and focused integration tests**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python tools/run_test_shards.py --shard profile_validation --durations 50
python tools/run_test_shards.py --shard qualified_review_evidence --durations 50
python tools/run_test_shards.py --shard mapping_review_bundle --durations 50
python -m unittest tests.test_validation_shards tests.test_v05_beta_release_evidence.V05LocalValidationRunnerTests -v
```

Expected: PASS. The three dominant shards retain their complete case populations, and release evidence still returns one passing `full_suite` record.

- [ ] **Step 8: Commit local and release execution**

```powershell
git add tools/run_test_shards.py tools/v05_beta_release_evidence.py tests/test_validation_shards.py tests/test_v05_beta_release_evidence.py
git commit -m "perf: run release tests in complete shards"
```

### Task 3: Parallelize CI behind one aggregate protected check

**Files:**
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tests/test_validation_shards.py`
- Modify: `tests/test_esaf_1600_foundation.py`
- Modify: `tests/test_pci_dss_source_readiness.py`
- Modify: `tests/test_release_metadata.py`
- Modify: `tests/test_profile_foundation.py`
- Modify: `tools/README.md`

**Interfaces:**
- Consumes: `run_test_shards.py --shard` from Task 2.
- Produces: four-entry `unit_tests` matrix with `fail-fast: false`.
- Produces: `validation_gates` for the existing operational validators.
- Produces: always-run `validate` aggregate job named exactly `Validate ESAF sources`.

- [ ] **Step 1: Add failing workflow-contract tests**

Require exact matrix identifiers, `fail-fast: false`, and this command:

```yaml
run: python tools/run_test_shards.py --shard "${{ matrix.shard }}" --durations 50
```

Require the existing operational validator steps to remain in `validation_gates`. Require `validate` to use `if: ${{ always() }}`, need both `unit_tests` and `validation_gates`, and fail unless both job results are `success`. Require exactly one occurrence of `name: Validate ESAF sources`.

Update existing workflow tests to inspect their owning job instead of assuming every step is under one job. Replace the Phase 1 discovery-command assertion with four matrix entries and one shard-runner command template.

- [ ] **Step 2: Run workflow tests and verify they fail**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validation_shards tests.test_esaf_1600_foundation tests.test_pci_dss_source_readiness tests.test_release_metadata tests.test_profile_foundation -v
```

Expected: FAIL because the workflow still has one monolithic job.

- [ ] **Step 3: Split the workflow without duplicating the required check**

Create `unit_tests` with checkout, Python 3.13, dependency installation, and the four-entry matrix. Move the current non-unit-test steps unchanged into `validation_gates`, including full-history checkout, Python and Node setup, dependencies, all validators, event-specific baselines, Mermaid rendering, and link validation.

Keep job ID `validate` for the aggregate job. Give only that job the display name `Validate ESAF sources`. Use `if: ${{ always() }}` and environment variables sourced from `needs.unit_tests.result` and `needs.validation_gates.result`; exit 1 unless both equal `success`.

Add `tools/test-shards.json`, `tools/test_shards.py`, `tools/validate_test_shards.py`, and `tools/run_test_shards.py` to both workflow path filters. Add `python tools/validate_test_shards.py --check` to `validation_gates` so a manifest defect fails both local release collection and hosted validation.

- [ ] **Step 4: Update operator documentation**

In `tools/README.md`, replace the discovery command with:

```shell
python tools/validate_test_shards.py --check
python tools/run_test_shards.py --all --durations 50
```

State plainly that CI runs the same four manifest-defined shards in separate jobs and publishes one aggregate required check. Keep the existing release assurance and diagnostics statements.

- [ ] **Step 5: Run focused workflow and release tests**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validation_shards tests.test_esaf_1600_foundation tests.test_pci_dss_source_readiness tests.test_release_metadata tests.test_profile_foundation tests.test_v05_beta_release_evidence -v
python tools/validate_test_shards.py --check
```

Expected: PASS with one aggregate protected-check name and no lost operational gate.

- [ ] **Step 6: Commit CI aggregation and documentation**

```powershell
git add .github/workflows/catalog-validation.yml tools/README.md tests/test_validation_shards.py tests/test_esaf_1600_foundation.py tests/test_pci_dss_source_readiness.py tests/test_release_metadata.py tests/test_profile_foundation.py
git commit -m "ci: parallelize complete unit test shards"
```

### Task 4: Verify the Phase 2 shard boundary

**Files:**
- Verify: every file changed from the branch merge base through `HEAD`.
- Record: exact commands, counts, durations, and reviewed head in the pull-request description.

**Interfaces:**
- Consumes: Tasks 1 through 3.
- Produces: a clean branch with exact population equivalence and publication gates preserved.

- [ ] **Step 1: Create a short drive alias and verify tracked-path readability**

Define this wrapper and execute all Task 4 steps in the same PowerShell session:

```powershell
function Invoke-InShortWorktree {
  param([Parameter(Mandatory=$true)][scriptblock]$Action)
  $worktree = (Resolve-Path .).Path
  $aliasDrive = 'S:'
  if (Test-Path "$aliasDrive\") { throw "$aliasDrive is already in use" }
  subst $aliasDrive $worktree
  if ($LASTEXITCODE -ne 0) { throw "subst failed with exit code $LASTEXITCODE" }
  $locationPushed = $false
  try {
    Push-Location "$aliasDrive\"
    $locationPushed = $true
    & $Action
  } finally {
    if ($locationPushed) { Pop-Location }
    subst $aliasDrive /D
    if ($LASTEXITCODE -ne 0) { throw "subst cleanup failed with exit code $LASTEXITCODE" }
  }
}

function Assert-NativeSuccess {
  param([Parameter(Mandatory=$true)][string]$Label)
  if ($LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE"
  }
}

Invoke-InShortWorktree {
  $missing = git ls-files | Where-Object { -not (Test-Path -LiteralPath $_) }
  Assert-NativeSuccess 'git ls-files'
  if ($missing) { throw "Unreadable tracked paths: $($missing -join ', ')" }
}
```

Expected: the wrapper maps the short drive only for the supplied action, every tracked file is readable through it, and `S:` is removed on success or failure. Wrap each command block in Steps 2 through 6 with `Invoke-InShortWorktree { ... }`.

- [ ] **Step 2: Run the aggregate shard suite three times**

```powershell
Invoke-InShortWorktree {
$env:PYTHONDONTWRITEBYTECODE='1'
1..3 | ForEach-Object {
  python tools/run_test_shards.py --all --durations 50
  Assert-NativeSuccess "Shard run $_"
}
}
```

Expected: all three runs PASS. Record each wall time. These sequential local runs prove stability. Hosted CI supplies the parallel timing evidence. This increment does not claim the full Phase 2 40 percent target before Git batching and hot-path work lands.

- [ ] **Step 3: Run all standalone validators**

```powershell
Invoke-InShortWorktree {
$env:PYTHONDONTWRITEBYTECODE='1'
python tools/validate_test_shards.py --check
Assert-NativeSuccess 'Shard manifest validation'
python tools/validate_assessment.py --check
Assert-NativeSuccess 'Assessment validation'
python tools/validate_profiles.py --check
Assert-NativeSuccess 'Profile validation'
python tools/validate_controls.py --check
Assert-NativeSuccess 'Control validation'
python tools/validate_architectures.py
Assert-NativeSuccess 'Architecture validation'
python tools/migrate_control_mappings.py --check
Assert-NativeSuccess 'Control mapping migration check'
python tools/validate_crosswalks.py --check
Assert-NativeSuccess 'Crosswalk validation'
python tools/render_pci_dss_mapping_go_no_go.py --check
Assert-NativeSuccess 'PCI DSS readiness rendering check'
python tools/release_gates.py --check
Assert-NativeSuccess 'Historical release validation'
python tools/v05_beta_release_gates.py --check --baseline-ref origin/main
Assert-NativeSuccess 'v0.5-beta release validation'
python tools/validate_links.py --check
Assert-NativeSuccess 'Link validation'
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md
Assert-NativeSuccess 'Mermaid rendering validation'
}
```

Expected: every command exits 0 and all 23 Mermaid blocks render with the pinned configuration.

- [ ] **Step 4: Run discovery once as an independent equivalence gate**

```powershell
Invoke-InShortWorktree {
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -v --durations 50
Assert-NativeSuccess 'Discovery verification'
}
```

Expected: PASS with the same population proven by `tests/test_validation_shards.py`. This command remains a verification oracle, not the operational CI or release path.

- [ ] **Step 5: Review the complete branch and repository hygiene**

```powershell
Invoke-InShortWorktree {
$mergeBase = git merge-base origin/main HEAD
Assert-NativeSuccess 'git merge-base'
if ($mergeBase -notmatch '^[0-9a-f]{40}$') { throw "Invalid merge base: $mergeBase" }
git diff --check "$mergeBase..HEAD"
Assert-NativeSuccess 'git diff --check'
git diff --stat "$mergeBase..HEAD"
Assert-NativeSuccess 'git diff --stat'
$status = git status --porcelain=v1
Assert-NativeSuccess 'git status'
if ($status) { throw "Dirty worktree: $($status -join ', ')" }
$caches = Get-ChildItem -Recurse -Directory -Filter __pycache__
if ($caches) { throw "Generated Python caches: $($caches.FullName -join ', ')" }
}
```

Expected: no whitespace errors, only approved shard files changed, clean status, and no `__pycache__` directories.

- [ ] **Step 6: Record the exact reviewed head**

```powershell
Invoke-InShortWorktree {
$reviewedHead = git rev-parse HEAD
Assert-NativeSuccess 'git rev-parse HEAD'
if ($reviewedHead -notmatch '^[0-9a-f]{40}$') { throw "Invalid reviewed head: $reviewedHead" }
$status = git status --porcelain=v1
Assert-NativeSuccess 'git status'
if ($status) { throw "Dirty worktree: $($status -join ', ')" }
Write-Output $reviewedHead
}
```

Expected: one 40-character head SHA and no status output. If the head changes after any gate, rerun every affected validation and redispatch the required reviews.
