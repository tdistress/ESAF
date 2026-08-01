# Validation Harness Efficiency Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make ESAF release validation fail fast, expose actionable failure output, avoid duplicate candidate-suite execution during taggable evidence collection, and make synthetic tests independent of ambient repository tags.

**Architecture:** Keep the canonical command-result schema and all existing release gates intact. Add preflight and diagnostic behavior inside `LocalValidationRunner`, replay candidate results already authenticated by closure evidence during taggable collection, and explicitly inject synthetic local-tag state in collector fixtures. Phase 2 sharding and hot-path refactors are intentionally excluded so this phase remains independently reviewable and measurable.

**Tech Stack:** Python 3.13, `unittest`, Git subprocesses, GitHub Actions YAML, Markdown.

## Global Constraints

- Preserve exact 40-character commit SHA and verified tree binding.
- Execute one complete local suite for every distinct release content tree.
- Continue executing commit- and history-sensitive validators for every required SHA.
- Keep authenticated GitHub Actions acquisition and the 15-minute final-evidence freshness window.
- Render all 23 Mermaid blocks with Node 22.23.1 and `@mermaid-js/mermaid-cli@11.16.0`.
- Keep assessment, profile, architecture, control, crosswalk, release, link, generated-artifact, preflight-clean, and postflight-clean checks as default gates.
- Do not delete or ignore a real local `v0.5-beta` tag in operational code.
- Set `PYTHONDONTWRITEBYTECODE=1` for every Python validation command.

---

## File Structure

- Modify `tools/v05_beta_release_evidence.py`: implement preflight checks, bounded subprocess diagnostics, duration reporting, and authenticated candidate-result replay.
- Modify `tests/test_v05_beta_release_evidence.py`: add regression coverage for ordering, output bounds, duration reporting, replay count, and controlled tag state.
- Modify `.github/workflows/catalog-validation.yml`: publish the 50 slowest tests by default without changing pass/fail semantics.
- Modify `tools/README.md`: document the default diagnostic behavior and preserved release assurances.

### Task 1: Isolate synthetic collector tests from ambient local tags

**Files:**
- Modify: `tests/test_v05_beta_release_evidence.py:554-572`
- Test: `tests/test_v05_beta_release_evidence.py:1385-2130`

**Interfaces:**
- Consumes: existing `collect_closure_evidence(..., repository_runner: Callable[..., object] | None)` injection point.
- Produces: `absent_local_tag_runner(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]` and a default `repository_runner` entry in `valid_collection_args()`.
- Preserves: the dedicated preexisting-tag test overrides the controlled default and proves the operational rejection remains active.

- [ ] **Step 1: Write the failing ambient-tag isolation test**

Add a helper and an explicit fixture-contract test:

```python
def absent_local_tag_runner(
    args: list[str], **kwargs: object
) -> subprocess.CompletedProcess[bytes]:
    del kwargs
    if args != [
        "git", "show-ref", "--verify", "--quiet",
        "refs/tags/v0.5-beta",
    ]:
        raise AssertionError(args)
    return subprocess.CompletedProcess(args, 1, b"", b"")


def test_synthetic_collection_controls_local_tag_absence(self) -> None:
    arguments = valid_collection_args()
    self.assertIs(arguments["repository_runner"], absent_local_tag_runner)
    evidence = collect_closure_evidence(valid_fake_client(), **arguments)
    self.assertEqual(CLOSURE_SHA, evidence["closure_head"])
```

- [ ] **Step 2: Run the isolation test and verify the ambient tag currently breaks it**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_v05_beta_release_evidence.V05AcquisitionTests.test_synthetic_collection_controls_local_tag_absence -v
```

Expected: FAIL because `valid_collection_args()` has no controlled `repository_runner`, or because collection reaches the real local `v0.5-beta` tag.

- [ ] **Step 3: Make controlled absence the synthetic fixture default**

Add this exact entry to `valid_collection_args()`:

```python
"repository_runner": absent_local_tag_runner,
```

Keep `_require_local_tag_absent()` unchanged. Keep `test_collector_rejects_preexisting_local_v05_tag` overriding `arguments["repository_runner"]` with a return-code-zero runner.

- [ ] **Step 4: Run focused collector tests with the real tag present**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
git show-ref --verify refs/tags/v0.5-beta
python -m unittest tests.test_v05_beta_release_evidence.V05AcquisitionTests -v
```

Expected: the tag exists, synthetic acquisition tests PASS, and the dedicated preexisting-local-tag test PASS by rejecting its injected return code zero.

- [ ] **Step 5: Commit the isolated fixture contract**

```powershell
git add tests/test_v05_beta_release_evidence.py
git commit -m "test: isolate release evidence from ambient tags"
```

### Task 2: Add preflight ordering, bounded diagnostics, and duration visibility

**Files:**
- Modify: `tools/v05_beta_release_evidence.py:185-349`
- Test: `tests/test_v05_beta_release_evidence.py:604-635`
- Test: `tests/test_v05_beta_release_evidence.py:1101-1384`

**Interfaces:**
- Consumes: `LocalValidationRunner(runner=...)`, `COMMAND_IDS`, and the existing stable command-result dictionaries.
- Produces: `_output_tail(stdout: bytes, stderr: bytes, limit: int = 32768) -> str`, `_preflight(root: Path) -> None`, and optional constructor injections `clock: Callable[[], float]` and `reporter: Callable[[str], None]`.
- Preserves: successful evidence records contain only `name`, `sha`, `exit_code`, and `result`; elapsed time and command text are operator diagnostics, not evidence fields.

- [ ] **Step 1: Add failing tests for cache and dirty-worktree preflight ordering**

Add a configurable executor that records calls, returns valid HEAD and merge-base values, and can return a dirty porcelain status. Add these assertions:

```python
def test_runner_rejects_dirty_worktree_before_full_suite(self) -> None:
    executor = RecordingCommandExecutor(status=b" M README.md\n")
    with self.assertRaisesRegex(
        ValueError, "preflight clean_status failed: README.md"
    ):
        LocalValidationRunner(executor).run(
            ROOT, CLOSURE_SHA, CLOSURE_BASE
        )
    self.assertFalse(any(
        args[1:4] == ["-m", "unittest", "discover"]
        for args, _kwargs in executor.calls
    ))

def test_runner_rejects_cache_before_full_suite(self) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "tests" / "__pycache__").mkdir(parents=True)
        executor = RecordingCommandExecutor()
        with self.assertRaisesRegex(
            ValueError,
            "preflight cache_count failed: tests/__pycache__",
        ):
            LocalValidationRunner(executor).run(
                root, CLOSURE_SHA, CLOSURE_BASE
            )
        self.assertFalse(any(
            args[1:4] == ["-m", "unittest", "discover"]
            for args, _kwargs in executor.calls
        ))
```

Update `RecordingCommandExecutor.__init__` to accept `status: bytes = b""` and return it for `git status --porcelain=v1`.

- [ ] **Step 2: Run the preflight tests and verify they fail**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_v05_beta_release_evidence.V05LocalValidationRunnerTests.test_runner_rejects_dirty_worktree_before_full_suite `
  tests.test_v05_beta_release_evidence.V05LocalValidationRunnerTests.test_runner_rejects_cache_before_full_suite -v
```

Expected: FAIL because cache and clean checks still occur at the end of `COMMAND_IDS`.

- [ ] **Step 3: Implement read-only preflight while retaining postflight evidence**

Add a `_cache_paths(root)` helper returning sorted POSIX-relative paths. In `run()`, after HEAD and merge-base verification and before constructing or executing the command loop:

```python
caches = self._cache_paths(root)
if caches:
    raise ValueError(
        "preflight cache_count failed: " + ", ".join(caches)
    )
status = self._git_text(
    root, ["status", "--porcelain=v1"], allow_empty=True
)
if status:
    paths = sorted(
        line[3:] if len(line) > 3 else line
        for line in status.splitlines()
    )
    raise ValueError(
        "preflight clean_status failed: " + ", ".join(paths)
    )
```

Retain the existing `cache_count` and `clean_status` branches inside the final loop unchanged in meaning so the recorded evidence proves validation did not generate repository state.

- [ ] **Step 4: Add failing tests for duration arguments and bounded failure output**

Add tests that require the exact full-suite command and a deterministic failure tail:

```python
def test_runner_enables_slowest_test_durations(self) -> None:
    executor = RecordingCommandExecutor()
    LocalValidationRunner(executor).run(
        ROOT, CLOSURE_SHA, CLOSURE_BASE
    )
    self.assertIn([
        os.fsdecode(Path(os.sys.executable)), "-m", "unittest",
        "discover", "-s", "tests", "-v", "--durations", "50",
    ], [args for args, _kwargs in executor.calls])

def test_runner_failure_contains_bounded_utf8_safe_output_tail(self) -> None:
    executor = FailingSuiteExecutor(
        stdout=(b"x" * 40000) + "\u2713 summary\n".encode(),
        stderr=b"FAILED (failures=1)\n",
    )
    with self.assertRaises(ValueError) as raised:
        LocalValidationRunner(executor).run(
            ROOT, CLOSURE_SHA, CLOSURE_BASE
        )
    message = str(raised.exception)
    self.assertIn("full_suite failed with exit code 1", message)
    self.assertIn("FAILED (failures=1)", message)
    self.assertIn("\u2713 summary", message)
    self.assertLessEqual(len(message.encode("utf-8")), 33024)
```

Add this executor beside `RecordingCommandExecutor`:

```python
class FailingSuiteExecutor:
    def __init__(self, *, stdout: bytes, stderr: bytes) -> None:
        self.delegate = RecordingCommandExecutor()
        self.stdout = stdout
        self.stderr = stderr

    def __call__(
        self, args: list[str], **kwargs: object
    ) -> subprocess.CompletedProcess[bytes]:
        if "unittest" in args:
            return subprocess.CompletedProcess(
                args, 1, self.stdout, self.stderr
            )
        return self.delegate(args, **kwargs)
```

- [ ] **Step 5: Run the diagnostic tests and verify they fail**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_v05_beta_release_evidence.V05LocalValidationRunnerTests.test_runner_enables_slowest_test_durations `
  tests.test_v05_beta_release_evidence.V05LocalValidationRunnerTests.test_runner_failure_contains_bounded_utf8_safe_output_tail -v
```

Expected: FAIL because `--durations 50` is absent and subprocess output is discarded.

- [ ] **Step 6: Implement the exact duration option and bounded UTF-8-safe tail**

Change the full-suite command to:

```python
[
    python, "-m", "unittest", "discover", "-s", "tests", "-v",
    "--durations", "50",
]
```

Add this module-level helper and use it in the nonzero-return branch:

```python
FAILURE_TAIL_BYTES = 32768


def _output_tail(stdout: bytes, stderr: bytes) -> str:
    combined = stdout + stderr
    tail = combined[-FAILURE_TAIL_BYTES:]
    text = tail.decode("utf-8", errors="replace")
    low, high = 0, len(text)
    while low < high:
        middle = (low + high) // 2
        if len(text[middle:].encode("utf-8")) <= FAILURE_TAIL_BYTES:
            high = middle
        else:
            low = middle + 1
    return text[low:].strip()
```

Raise:

```python
detail = _output_tail(stdout, stderr)
suffix = f"\n--- output tail ---\n{detail}" if detail else ""
raise ValueError(
    f"{name} failed with exit code {return_code}{suffix}"
)
```

- [ ] **Step 7: Add failing tests for start/completion/elapsed operator events**

Use a clock iterator and list reporter:

```python
events: list[str] = []
ticks = iter(float(value) for value in range(1000))
LocalValidationRunner(
    RecordingCommandExecutor(),
    clock=lambda: next(ticks),
    reporter=events.append,
).run(ROOT, CLOSURE_SHA, CLOSURE_BASE)
self.assertIn("full_suite: start", events)
self.assertIn("full_suite: passed in 1.000s", events)
self.assertIn("clean_status: passed in 1.000s", events)
```

- [ ] **Step 8: Implement operator-only timing events**

Extend the constructor without changing existing call sites:

```python
def __init__(
    self,
    runner: Callable[..., object] | None = None,
    *,
    clock: Callable[[], float] | None = None,
    reporter: Callable[[str], None] | None = None,
) -> None:
    self._runner = runner or subprocess.run
    self._clock = clock or time.monotonic
    self._reporter = reporter or print
```

For every `COMMAND_IDS` entry except `mermaid_rendering`, report `"{name}: start"`, capture the clock immediately before work, and report `"{name}: passed in {elapsed:.3f}s"` after its result is known. Do not add elapsed time to the stable evidence dictionary.

- [ ] **Step 9: Preserve detached-worktree context through failure cleanup**

Add a validation runner that asserts its supplied root exists and raises `ValueError("synthetic suite failure")`. Assert that `DetachedValidationRunner.run()` raises a message containing both the original failure and `detached worktree:`, and that the recorded `git worktree remove --force` call occurs after the failing runner call.

Inside `DetachedValidationRunner.run()`, wrap validation failures while the snapshot path still exists:

```python
try:
    results = self._validation_runner.run(
        snapshot, expected_head, baseline_head
    )
    _validate_local_results(results, expected_head)
    return results
except ValueError as error:
    raise ValueError(
        f"{error}\ndetached worktree: {snapshot}"
    ) from error
```

Retain the existing `finally` block so the worktree is removed only after the contextual exception has been constructed.

- [ ] **Step 10: Run the complete local-runner test class**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_v05_beta_release_evidence.V05LocalValidationRunnerTests -v
```

Expected: PASS, including exact command coverage, preflight ordering, postflight records, bounded diagnostics, and timing events.

- [ ] **Step 11: Commit the runner changes**

```powershell
git add tools/v05_beta_release_evidence.py tests/test_v05_beta_release_evidence.py
git commit -m "perf: fail fast in release validation"
```

### Task 3: Replay authenticated candidate results during taggable refresh

**Files:**
- Modify: `tools/v05_beta_release_evidence.py:1361-1450`
- Test: `tests/test_v05_beta_release_evidence.py:1690-1785`
- Test: `tests/test_v05_beta_release_evidence.py:2280-2525`

**Interfaces:**
- Consumes: `_validated_candidate_commands`, `RecordedValidationRunner`, `_require_unchanged_sources`, closure `candidate_commands`, and closure `closure_base`.
- Produces: taggable refresh that invokes no candidate validation runner and invokes the post-merge validation runner exactly once.
- Preserves: two fresh candidate-source acquisitions around the merge-head validation, exact command equality, exact tree equality, and final GitHub source reacquisition.

- [ ] **Step 1: Strengthen the refresh execution-count regression test**

Replace the candidate runner in the taggable test with a sentinel and assert exact counts:

```python
candidate_runner = FakeValidationRunner()
arguments = valid_collection_args()
arguments["validation_runner"] = candidate_runner
taggable = refresh_taggable_evidence(
    client,
    base_evidence=closure,
    merge_head=MERGE_SHA,
    post_merge_rendering_comment_id=POST_MERGE_RENDERING_ID,
    post_merge_validation_runner=merge_runner,
    **arguments,
)
self.assertEqual([], candidate_runner.calls)
self.assertEqual([(ROOT, MERGE_SHA, CLOSURE_BASE)], merge_runner.calls)
self.assertEqual(
    _validated_candidate_commands(
        closure["candidate_commands"], CLOSURE_SHA
    ),
    _validated_candidate_commands(
        taggable["candidate_commands"], CLOSURE_SHA
    ),
)
```

Add a drift test that mutates one authenticated base command result and expects the existing local-result validator to fail closed before acquisition.

- [ ] **Step 2: Run the taggable tests and verify duplicate candidate execution**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_v05_beta_release_evidence.V05AcquisitionTests.test_taggable_refresh_executes_merge_head_and_fetches_visual_review `
  tests.test_v05_beta_release_evidence.V05AcquisitionTests.test_taggable_refresh_reacquires_after_postmerge_validation -v
```

Expected: execution-count assertion FAIL because `refresh_taggable_evidence()` currently installs `DetachedValidationRunner()` and runs the candidate command set.

- [ ] **Step 3: Replace candidate re-execution with validated replay**

Immediately after `base_commands` validation, build the nonvisual immutable results:

```python
candidate_results = [
    deepcopy(command)
    for command in base_commands
    if command.get("name") != "mermaid_rendering"
]
candidate_replay = RecordedValidationRunner(
    candidate_results, expected_head, closure_base
)
refresh_arguments = dict(collection_arguments)
refresh_arguments["validation_runner"] = candidate_replay
```

Remove the `DetachedValidationRunner()` candidate default. Keep `collect_closure_evidence()` as the acquisition mechanism so it still performs the initial and post-validation acquisitions, but both calls receive the authenticated replay. Keep the existing `_require_unchanged_sources()` comparison and exact `base_commands` versus `fresh_commands` comparison.

Keep this merge-head execution unchanged:

```python
merge_results = (
    post_merge_validation_runner or DetachedValidationRunner()
).run(Path(collection_arguments["root"]), merge_head, closure_base)
```

Keep the final `_collect_closure_evidence_once()` reacquisition after merge validation, using a `RecordedValidationRunner` bound to the candidate SHA and closure base.

- [ ] **Step 4: Run all acquisition and taggable mutation tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_v05_beta_release_evidence.V05AcquisitionTests -v
```

Expected: PASS with zero candidate execution, one merge execution, immutable candidate commands, equal merge tree, and fresh post-validation acquisitions. All taggable mutation cases are members of `V05AcquisitionTests`.

- [ ] **Step 5: Commit candidate replay**

```powershell
git add tools/v05_beta_release_evidence.py tests/test_v05_beta_release_evidence.py
git commit -m "perf: replay validated candidate release results"
```

### Task 4: Make duration diagnostics the repository default

**Files:**
- Modify: `.github/workflows/catalog-validation.yml:126-130`
- Modify: `tools/README.md:86-105`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: the existing `Run repository unit tests` workflow step.
- Produces: the canonical CI command `python -m unittest discover -s tests -v --durations 50` and documentation matching the local release runner.
- Preserves: one discovery-based complete suite in Phase 1; sharding belongs to Phase 2.

- [ ] **Step 1: Add a failing workflow-contract test**

In `tests/test_release_metadata.py`, add this exact test:

```python
def test_repository_unit_tests_publish_slowest_durations(self) -> None:
    workflow = read_repository_file(
        ".github/workflows/catalog-validation.yml"
    )
    unit_step = workflow.split(
        "- name: Run repository unit tests\n", 1
    )[1].split("      - name:", 1)[0]
    self.assertIn(
        "run: python -m unittest discover -s tests -v "
        "--durations 50",
        unit_step,
    )
```

- [ ] **Step 2: Run the workflow-contract test and verify it fails**

Run the exact new test with:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata.ReleaseMetadataTests.test_repository_unit_tests_publish_slowest_durations -v
```

Expected: FAIL because the workflow command lacks `--durations 50`.

- [ ] **Step 3: Update CI and operator documentation**

Change the workflow step to:

```yaml
- name: Run repository unit tests
  run: python -m unittest discover -s tests -v --durations 50
```

Update the unit-test command in `tools/README.md` to the same command. Add a concise paragraph stating that release collection performs read-only clean/cache preflight, reports command durations and bounded failure output, retains postflight clean/cache evidence, and reuses only candidate results already authenticated by valid closure evidence.

- [ ] **Step 4: Run metadata and focused release-evidence tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata tests.test_v05_beta_release_evidence -v
```

Expected: PASS.

- [ ] **Step 5: Commit default diagnostics**

```powershell
git add .github/workflows/catalog-validation.yml tools/README.md tests/test_release_metadata.py
git commit -m "ci: publish slowest unit test durations"
```

### Task 5: Verify the complete Phase 1 assurance boundary

**Files:**
- Verify: all files changed since `origin/main`
- Record: command output in the pull-request description during publication, not in generated repository files.

**Interfaces:**
- Consumes: Tasks 1-4 and the approved design specification.
- Produces: a clean, fully validated Phase 1 branch ready for independent review and measurement.

- [ ] **Step 1: Run focused release tests**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_v05_beta_release_evidence `
  tests.test_v05_beta_release_gates `
  tests.test_release_metadata -v --durations 50
```

Expected: PASS with the real local `v0.5-beta` tag still present.

- [ ] **Step 2: Run all standalone operational validators**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python tools/validate_assessment.py --check
python tools/validate_profiles.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/render_pci_dss_mapping_go_no_go.py --check
python tools/release_gates.py --check
python tools/v05_beta_release_gates.py --check --baseline-ref origin/main
python tools/validate_links.py --check
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md
```

Expected: every command exits 0 and all 23 Mermaid blocks render under the pinned renderer configuration.

- [ ] **Step 3: Run the complete suite once and retain duration evidence**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -v --durations 50
```

Expected: all discovered tests PASS. Record total wall time and the 50 slowest tests for the Phase 2 baseline.

- [ ] **Step 4: Review the whole branch and repository cleanliness**

```powershell
git diff --check origin/main..HEAD
git diff --stat origin/main..HEAD
git diff origin/main..HEAD
git status --short
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Select-Object -ExpandProperty FullName
```

Expected: no whitespace errors, only approved Phase 1 files changed, clean status, and no `__pycache__` directories.

- [ ] **Step 5: Commit any verification-only corrections and record exact head**

If verification exposed a defect, first add a focused regression test, make the minimal fix, rerun every affected gate, and commit only those correction files. Then run:

```powershell
git rev-parse HEAD
git status --short
```

Expected: a 40-character reviewed head SHA and no status output. Do not claim prior test evidence after changing that SHA; rerun the affected gates.
