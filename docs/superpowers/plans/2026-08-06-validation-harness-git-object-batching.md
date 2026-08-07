# Validation harness Git object batching implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace per-file Git subprocesses in qualified-review mapping bundle reads with bounded finite object batches while preserving exact package bytes, fail-closed behavior, and sanitized operator errors.

**Architecture:** `GitReader` will own a frozen child environment, a bounded finite-command transport, up to eight immutable full-tree indexes, and a 128 MiB LRU object cache. Package collection will submit three commit-scoped read phases through `read_many()`, while duck-typed mutation readers keep the existing `read_bytes()` fallback. Deterministic control-manifest regeneration remains a separate measured Git path unless equivalence evidence proves that it must share the reader.

**Tech Stack:** Python 3.13, `unittest`, Git CLI object plumbing, `subprocess`, `tempfile.SpooledTemporaryFile`, `threading`, `hashlib`, `collections.OrderedDict`, GitHub Actions, Mermaid CLI 11.16.0.

## Global constraints

- Follow strict red, green, refactor cycles. Each new behavior needs a test that first fails for the intended reason.
- Keep `resolve_commit()`, `read_bytes()`, and `list_files()` signatures unchanged.
- Add `GitReader.read_many(self, commit: str, paths: Sequence[str]) -> dict[str, bytes]`.
- Do not introduce a persistent child, context manager, finalizer, background process, or public cleanup method.
- Every Git command shall use `shell=False`, binary input and output, a 120-second timeout, the resolved root, the frozen sanitized environment, and `git --no-replace-objects -c core.fsmonitor=false -C <root>`.
- Support only SHA-1 repositories. Require exact lowercase 40-character commit SHAs.
- Limit one reader to eight immutable commit indexes, 100,000 tree records per index, 64 MiB tree output, 4,096 logical paths per `read_many()` call, 32 MiB per blob, 128 MiB logical content per call, and a 128 MiB LRU content cache.
- Cap batch headers at 256 bytes, child stderr at 64 KiB, batch-check stdout at `4_096 * 256` bytes, and batch-content stdout at `128 MiB + 4_096 * 257` bytes.
- Never publish a partial tree index or partial object transaction to a cache.
- Preserve duck-typed mutation readers. They do not gain a required `read_many()` method.
- Keep `tools/crosswalks/manifest.py` unchanged unless Task 5 equivalence evidence proves that the selected package boundary cannot meet its operation-count acceptance criteria without routing regeneration through `GitReader`.
- Use `PYTHONDONTWRITEBYTECODE=1` for every Python command. Run Python test commands serially.

## File map

- Modify `tools/build_mapping_review_bundle.py`: finite Git transport, object-format and commit verification, tree index, batch protocols, object cache, `read_many()`, and three-phase package adoption.
- Modify `tests/test_build_mapping_review_bundle.py`: real-repository behavior, protocol fixtures, limit and cleanup regressions, package equivalence, and deterministic invocation counts.
- Create `tests/fixtures/git-batching-package-equivalence.json`: reviewed pre-change package path, purpose, byte-length, and SHA-256 oracle for all three profiles.
- Modify `tools/v05_beta_release_gates.py`: sanitize `GitObjectReadError` at the retained-campaign validation boundary.
- Modify `tests/test_v05_beta_release_gates.py`: focused release-gate regression for the new `SubprocessError` subtype.
- Modify `tests/test_validate_qualified_review_evidence.py`: replace the obsolete per-file `git show` failure injection with a batch-transport operational failure.
- Verify only, unless Task 5 evidence requires a design-approved change: `tools/crosswalks/manifest.py`.
- Verify consumers without changing their successful contracts: `tools/validate_qualified_review_evidence.py`, `tools/seal_qualified_review_campaign.py`, and `tools/v05_beta_release_evidence.py`.

---

### Task 1: Add the bounded finite-command and repository-binding boundary

**Files:**
- Modify: `tools/build_mapping_review_bundle.py:168-303`
- Test: `tests/test_build_mapping_review_bundle.py:101-303`

**Interfaces:**
- Consumes: resolved repository `Path`, command arguments as `tuple[str, ...]`, frozen process input bytes, and command-specific stdout/stderr limits.
- Produces: `GitObjectReadError`, `_GitCommandResult(stdout: bytes, stderr: bytes)`, `_run_finite_git(arguments: tuple[str, ...], *, input_bytes: bytes = b"", stdout_limit: int, stderr_limit: int = 65_536) -> _GitCommandResult`, `_require_sha1_repository() -> None`, and cached `resolve_commit(revision: str) -> str`.

- [ ] **Step 1: Write failing environment and command-contract tests**

Add tests that construct `GitReader` under a patched environment containing `GIT_DIR`, `GIT_GRAFT_FILE`, `git_object_directory`, `Git_AlternATE_Object_Directories`, and an unrelated `ESAF_SENTINEL`. Inject a complete transport fake at `_run_finite_git` and assert from the fake's received command specification that Git-prefixed variables are absent, `ESAF_SENTINEL` remains, the six fixed variables have exact values, `shell` is false, input and output are binary, the timeout is 120 seconds, and the prefix includes `--no-replace-objects`, `-c core.fsmonitor=false`, and `-C <resolved-root>`.

Add real temporary-repository tests proving that a lowercase 40-character commit resolves exactly once per reader, `HEAD`, uppercase SHA, abbreviated SHA, and a missing all-zero SHA remain `ValueError`, and object-format validation runs before the first commit or tree operation. Create one active replacement ref and prove that a tree read still returns the original exact bytes. Create one active `GIT_GRAFT_FILE`, run an ancestry-sensitive `rev-list --parents -n 1 <commit>` command through the finite transport, and assert the original ungrafted parent identity. These tests shall use literal original identities and bytes.

Add tests for `require_candidate_execution_state()` and `worktree_roots()` at the finite transport seam. Assert that both use the frozen environment, binary response parsing, timeout, prefix, stderr contract, and command-specific output caps. After Task 1, the temporary `_run()` adapter shall delegate only to `_run_finite_git` and shall never call `subprocess.run`.

Name the mutations these tests catch in comments next to the test table: leaked `GIT_*`, omitted fixed environment value, missing command-prefix option, acceptance of non-SHA-1 storage, and repeated commit resolution.

- [ ] **Step 2: Run the new tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle.GitReaderTests -v
```

Expected: FAIL because `GitObjectReadError`, the frozen environment, finite transport seam, storage-format check, and verified-commit cache do not exist. Existing path-validation tests may still pass.

- [ ] **Step 3: Add transport cleanup failure tests before production cleanup code**

Build a small fake child with controllable stdin, stdout, stderr, `wait()`, `terminate()`, `kill()`, and pipe-close observations. Cover success, nonzero exit, nonempty stderr, timeout, stdout overflow, stderr overflow, reader-thread I/O failure, short stdin writes, `BrokenPipeError`, early child exit during input, and failure after termination. Assert that both output drainers start before the first stdin write. For every result, assert deterministic stdin closure. For every failure, also assert that the child is reaped, both drainers are joined, pipes and temporary spools are closed, and the public exception contains no injected `host-secret` stderr or environment value.

Use fixed byte fixtures. Do not derive expected caps from production constants. Include a child that writes beyond its cap before exit so a post-exit-only size check cannot satisfy the test.

- [ ] **Step 4: Run the transport tests and verify RED**

Run the named new test class, for example:

```powershell
python -m unittest tests.test_build_mapping_review_bundle.FiniteGitCommandTests -v
```

Expected: FAIL because no concurrent bounded drainer or cleanup sequence exists.

- [ ] **Step 5: Implement the minimal finite transport and binding**

In `tools/build_mapping_review_bundle.py`:

```python
class GitObjectReadError(subprocess.SubprocessError):
    """Sanitized failure while acquiring immutable Git object bytes."""


@dataclass(frozen=True)
class _GitCommandResult:
    stdout: bytes
    stderr: bytes
```

Freeze the child environment in `GitReader.__init__`, removing every variable for which `name.upper().startswith("GIT_")`, then set the six values from the design. Implement the finite runner with two drainers that copy fixed-size chunks into capped `SpooledTemporaryFile` instances while the child runs. Start both drainers before writing input, loop until all input is written or the child closes its pipe, and close stdin in `finally`. On overflow, timeout, short write, `BrokenPipeError`, or other I/O failure, terminate, escalate to kill when needed, reap, join, close, and raise `GitObjectReadError("Git object read failed")` without child diagnostics.

Make successful commands require exit zero and empty stderr. Add exact small-output contracts for `rev-parse --show-object-format=storage` and `rev-parse --verify <sha>^{commit}`. Cache only successful SHA-1 and commit verification results.

Migrate `require_candidate_execution_state()` and `worktree_roots()` to the same finite runner. Keep a temporary `_run()` compatibility adapter for `read_bytes()`, `_require_regular_blob()`, and `list_files()`; it shall delegate to the bounded finite transport and shall not call `subprocess.run`. Decode only after each exact binary response contract passes. Task 3 removes the adapter after the final legacy caller is migrated.

- [ ] **Step 6: Run RED tests to verify GREEN, then run the existing reader boundary**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.FiniteGitCommandTests tests.test_build_mapping_review_bundle.GitReaderTests tests.test_build_mapping_review_bundle.CandidateExecutionStateTests -v
```

Expected: PASS. Output contains no warning or leaked fake stderr.

- [ ] **Step 7: Review and commit Task 1**

Run `git diff --check`, inspect the complete staged diff, then commit:

```powershell
git add tools/build_mapping_review_bundle.py tests/test_build_mapping_review_bundle.py
git commit -m "Harden finite Git object commands"
```

Checkpoint: one bounded command helper owns all child lifecycle cleanup; object format and exact commit verification fail closed.

---

### Task 2: Build and validate one immutable complete tree index per commit

**Files:**
- Modify: `tools/build_mapping_review_bundle.py:168-300`
- Test: `tests/test_build_mapping_review_bundle.py:101-228`

**Interfaces:**
- Consumes: `_run_finite_git()`, exact verified commit SHA, complete `ls-tree` bytes.
- Produces: immutable `TreeEntry(path: str, mode: str, object_type: str, object_id: str)`, `_tree_index(commit: str) -> Mapping[str, TreeEntry]`, and compatible `list_files(commit: str, path: str) -> tuple[str, ...]`.

- [ ] **Step 1: Write failing real-tree behavior tests**

Create a real temporary repository containing regular files `foo`, `foobar/item.txt`, `dir/a.txt`, executable `dir/run.sh`, a symlink when supported, and a gitlink fixture made with `git update-index --cacheinfo`. Assert:

- exact file selection returns one path;
- selecting `foo` does not include `foobar/item.txt`;
- an exact tree returns sorted regular descendants;
- a missing path returns `()`;
- selecting a symlink or gitlink raises `ValueError`;
- selecting a tree containing a nonregular descendant raises `ValueError`; and
- repeated operations at the same commit produce one complete-tree acquisition.

Expected values shall be literal tuples, not values computed with `GitReader` helpers.

- [ ] **Step 2: Run the real-tree tests and verify RED**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitTreeIndexTests -v
```

Expected: FAIL because the current code runs path-scoped `ls-tree` commands and does not retain tree entries or enforce complete hierarchy.

- [ ] **Step 3: Write failing parser and index-limit tests**

At the finite transport boundary, feed literal NUL-delimited tree fixtures for:

- missing terminal NUL and empty interior record;
- malformed header or tab separation;
- uppercase or abbreviated object ID;
- invalid UTF-8 or control character in a path;
- unsafe, duplicate, or noncanonical path;
- child without a parent tree;
- parent declared as a blob;
- descendant below a non-tree entry;
- invalid mode/type pair;
- 100,001 records; and
- output crossing 64 MiB while acquisition is still active.

After every failed fixture, repair the fake result and call again. Assert that the successful retry performs a new tree command, proving that failed parsing did not publish a partial index.

- [ ] **Step 4: Run parser tests and verify RED**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitTreeProtocolTests -v
```

Expected: FAIL because complete-tree framing, hierarchy validation, and atomic index publication do not exist.

- [ ] **Step 5: Write the eight-commit hard-bound test and verify RED**

Create nine commits in one temporary repository. Index the first eight, then request the ninth. Assert `ValueError` before the fake transport records any ninth tree command. Re-read the first commit and assert that it was not evicted or rebuilt.

Run:

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitTreeIndexLimitTests -v
```

Expected: FAIL because the current reader has no complete-index limit.

- [ ] **Step 6: Implement the immutable index and compatible list semantics**

Use exactly:

```text
git ls-tree -r -t -z --full-tree --abbrev=40 <commit>
```

Parse and validate all records in local temporary structures. Validate canonical paths with the repository path helper plus a control-character check. Validate parent trees and descendant structure after parsing all records. Publish an immutable mapping only after the entire output passes. Enforce the eight-commit limit before starting Git for a ninth commit.

Update `list_files()` to consult the complete index. Do not make a valid prohibited entry elsewhere poison an unrelated selected subtree.

- [ ] **Step 7: Run all tree tests and the existing reader tests**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitTreeIndexTests tests.test_build_mapping_review_bundle.GitTreeProtocolTests tests.test_build_mapping_review_bundle.GitTreeIndexLimitTests tests.test_build_mapping_review_bundle.GitReaderTests -v
```

Expected: PASS.

- [ ] **Step 8: Commit Task 2**

```powershell
git add tools/build_mapping_review_bundle.py tests/test_build_mapping_review_bundle.py
git commit -m "Index immutable Git trees once"
```

Checkpoint: every exact commit has at most one validated tree acquisition, and request-scoped regular-file behavior matches the approved design.

---

### Task 3: Add atomic metadata and content batch transactions

**Files:**
- Modify: `tools/build_mapping_review_bundle.py:168-300`
- Test: `tests/test_build_mapping_review_bundle.py:101-228`

**Interfaces:**
- Consumes: verified `TreeEntry` objects and `_run_finite_git()`.
- Produces: `read_many(commit: str, paths: Sequence[str]) -> dict[str, bytes]`, compatible singleton `read_bytes()`, and an LRU cache keyed by `(exact_commit, object_id)`.

- [ ] **Step 1: Write failing public input and immutable-snapshot tests**

Add a custom adversarial `Sequence[str]` whose iterator mutates its backing values after the first traversal. Assert that `read_many()` freezes it once and returns results in the original order. Add literal cases for empty input, `str`, `bytes`, unsafe paths, duplicates, 4,097 paths, missing entries, trees, symlinks, and gitlinks. Assert that empty input starts no Git command and that logical limits count cache hits and same-OID aliases.

- [ ] **Step 2: Run input tests and verify RED**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitReadManyInputTests -v
```

Expected: FAIL with missing `read_many` or incorrect validation behavior.

- [ ] **Step 3: Write failing batch-check protocol tests**

Use hand-built complete responses for `git cat-file --batch-check=%(objectname) %(objecttype) %(objectsize)`. Cover exact success and each failure independently: missing record, extra record, reordered OID, wrong OID, non-blob type, negative, signed, zero-padded, or nondecimal size, size over 32 MiB, logical total over 128 MiB, nonempty stderr, nonzero exit, timeout, and output overflow. Assert that the content command is never started after a preflight failure.

- [ ] **Step 4: Run preflight tests and verify RED**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitBatchCheckProtocolTests -v
```

Expected: FAIL because batch metadata validation does not exist.

- [ ] **Step 5: Write failing content parser and identity tests**

Create literal binary fixtures containing NULs, embedded newlines, non-UTF-8 bytes, empty content, and payloads ending in newline. Compute fixture OIDs in test setup from independently supplied fixture bytes using Git's documented blob identity rule. Test missing and extra records, reordered identity, wrong type, size disagreement, header over 256 bytes, truncated content, missing payload delimiter, trailing stdout, nonempty stderr, nonzero exit, timeout, and local SHA-1 mismatch.

For every failed content transaction, issue the same request with a valid fixture and assert a new batch-check and batch-content pair. This proves the failed call left no content-cache entry.

- [ ] **Step 6: Run content tests and verify RED**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitBatchContentProtocolTests -v
```

Expected: FAIL because finite content framing, local object verification, and transaction atomicity do not exist.

- [ ] **Step 7: Write failing deduplication and LRU tests**

Use two paths at one commit that share one blob OID. Assert one requested OID in each batch command but two ordered dictionary results. Repeat at another commit with the same OID and assert a separate fetch because cache keys include the exact commit. Fill the cache with literal object sizes, touch an older entry, cross 128 MiB, and assert least-recently-used eviction. Assert that a single object larger than the cache or blob limit fails before content acquisition.

- [ ] **Step 8: Run cache tests and verify RED**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitObjectCacheTests -v
```

Expected: FAIL because transport deduplication and the bounded LRU content cache do not exist.

- [ ] **Step 9: Implement minimal `read_many()` and cache behavior**

Resolve paths through the validated tree. Deduplicate only transport OIDs. Send newline-delimited direct OIDs, never `commit:path` or caller-controlled revision expressions. Validate the complete preflight before starting content acquisition. Validate and hash every content record into local storage, then publish all successful objects to the LRU cache in one final step. Return a normal insertion-ordered dictionary constructed from the frozen path snapshot.

Make `read_bytes()` exactly delegate to `read_many(commit, (path,))[path]`.

Remove the temporary `_run()` compatibility adapter after `read_many()`, the complete tree index, and `list_files()` own every former caller. Add a source regression asserting that no direct `subprocess.run` call and no `_run()` method remain in `GitReader`.

- [ ] **Step 10: Run the complete object transaction boundary**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.GitReadManyInputTests tests.test_build_mapping_review_bundle.GitBatchCheckProtocolTests tests.test_build_mapping_review_bundle.GitBatchContentProtocolTests tests.test_build_mapping_review_bundle.GitObjectCacheTests tests.test_build_mapping_review_bundle.GitReaderTests -v
```

Expected: PASS with no warning, leaked stderr, or orphaned process.

- [ ] **Step 11: Commit Task 3**

```powershell
git add tools/build_mapping_review_bundle.py tests/test_build_mapping_review_bundle.py
git commit -m "Read Git blobs in atomic batches"
```

Checkpoint: one `read_many()` call is all-or-nothing, validates local Git object identity, and cannot grow acquisition buffers or caches beyond the fixed limits.

---

### Task 4: Adopt three package read phases without breaking mutation readers

**Files:**
- Modify: `tools/build_mapping_review_bundle.py:303-789`
- Test: `tests/test_build_mapping_review_bundle.py:304-1132`

**Interfaces:**
- Consumes: `GitReader.read_many()`, existing `read_bytes()` duck readers, parsed candidate README and control manifest.
- Produces: private `_read_package_files(reader: object, commit: str, paths: Sequence[str]) -> dict[str, bytes]` and three commit-scoped collection phases.

- [ ] **Step 1: Write the failing package-read helper test**

Add a test that calls the wished-for `_read_package_files()` with a mutation reader that implements only `read_bytes()` and `list_files()`. Assert the literal ordered result and the mutation reader's observable changed byte. Assert returned package behavior, not whether a mock method exists.

Run:

```powershell
python -m unittest tests.test_build_mapping_review_bundle.PackagePopulationTests -v
```

Expected: FAIL with `AttributeError` because `_read_package_files` does not exist. Implement the minimal helper with exact-`GitReader` batching and repeated `read_bytes()` fallback before changing `collect_package_files()`.

- [ ] **Step 2: Capture and pass the pre-change equivalence oracle**

Before changing `collect_package_files()`, run the current writer for all three profiles and create `tests/fixtures/git-batching-package-equivalence.json` with the exact baseline commit, ordered path, purpose, byte length, and SHA-256 for every payload plus `PACKAGE_MANIFEST.json` and `PACKAGE_INDEX.md`. Review the fixture against the generated directories. Add the characterization test and run it against the unchanged collector. It shall pass before the batching refactor; it is a safety harness, not the RED for batching.

- [ ] **Step 3: Write failing phase-boundary and invocation-count tests**

Use a real temporary Git repository or a complete transport recorder below `GitReader`. Assemble each profile and assert observable operation records:

- exactly one full-tree command for each used exact commit;
- exactly three logical package read phases: candidate snapshot, remaining candidate dependencies, and historical controls;
- a bounded batch-check and batch-content pair per uncached phase;
- direct object IDs only in batch input;
- no per-file `git show` call from `GitReader`; and
- deterministic control-manifest regeneration subprocesses counted separately under the existing manifest helper.

Do not assert a wall-clock threshold. Do not count calls on a mocked `read_many()` method. The recorder shall observe commands at the finite transport boundary while the real reader performs validation and package assembly.

- [ ] **Step 4: Run invocation tests and verify RED**

```powershell
python -m unittest tests.test_build_mapping_review_bundle.PackageGitInvocationTests -v
```

Expected: FAIL because collection still performs singleton reads and per-file `git show` operations.

- [ ] **Step 5: Implement the private collection helper and phases**

Freeze every helper path sequence. When `type(reader) is GitReader`, call `read_many()` once for that phase. Otherwise, preserve the existing ordered repeated `read_bytes()` behavior.

Phase 1 reads every path returned for `profile.snapshot_path`. After parsing the candidate README, Phase 2 reads candidate schemas, registry, catalog, fixed review files, and README-derived source-evidence paths. After parsing the manifest and resolving `control_source`, Phase 3 reads `controls/catalog.json` and every manifest-derived control at the historical commit. Do not mix candidate and historical paths.

- [ ] **Step 6: Prove byte-for-byte equivalence for all profiles**

Using the oracle captured in Step 2, assemble and write all profiles after batching and assert:

- identical ordered `PackageFile` paths, purposes, and bytes;
- identical `PACKAGE_MANIFEST.json` bytes;
- identical `PACKAGE_INDEX.md` bytes; and
- identical complete output trees.

Run:

```powershell
python -m unittest tests.test_build_mapping_review_bundle.PackageEquivalenceTests tests.test_build_mapping_review_bundle.PackagePopulationTests tests.test_build_mapping_review_bundle.PackageWriterTests tests.test_build_mapping_review_bundle.PackageIntegrationTests -v
```

Expected: PASS for Core, Plus forward, and Plus reverse.

- [ ] **Step 7: Decide the manifest boundary from evidence**

Inspect the invocation report. If package acceptance already shows bounded `GitReader` batch pairs and separately reports manifest regeneration, leave `tools/crosswalks/manifest.py` unchanged as required. If manifest subprocesses prevent the selected package boundary from meeting an explicit approved count, stop and obtain a design amendment before modifying that file. Do not broaden scope on timing evidence alone.

- [ ] **Step 8: Commit Task 4**

```powershell
git add tools/build_mapping_review_bundle.py tests/test_build_mapping_review_bundle.py tests/fixtures/git-batching-package-equivalence.json
git commit -m "Batch mapping package object reads"
```

Checkpoint: all package bytes match the trusted baseline, mutation readers still work, and deterministic command evidence replaces timing assertions.

---

### Task 5: Audit and harden every production consumer boundary

**Files:**
- Modify: `tools/v05_beta_release_gates.py:1793-1811`
- Modify: `tests/test_v05_beta_release_gates.py:763-2297`
- Modify: `tests/test_validate_qualified_review_evidence.py:2388-2467`
- Verify: `tools/validate_qualified_review_evidence.py:1232-1269`
- Verify: `tools/seal_qualified_review_campaign.py:591-628`
- Verify: `tools/v05_beta_release_evidence.py`

**Interfaces:**
- Consumes: `GitObjectReadError`, a `subprocess.SubprocessError` subtype.
- Produces: existing sanitized operator result at each CLI or release-gate boundary, with no new public error text.

- [ ] **Step 1: Write the failing v0.5 release-gate regression**

Patch the retained-campaign validation path so a real `GitObjectReadError("host-secret")` reaches `_validate_qualified_basis`. Call `validate_external_evidence()` with the existing qualified fixture. Assert that it returns the established `qualified campaign shall pass the tracked official validator` diagnostic and does not raise or include `host-secret`.

Run:

```powershell
python -m unittest tests.test_v05_beta_release_gates.V05ExternalEvidenceTests.test_git_object_read_failure_is_sanitized -v
```

Expected: ERROR because the current boundary catches `OSError`, `RuntimeError`, `UnicodeError`, and `ValueError`, but not `subprocess.SubprocessError`.

- [ ] **Step 2: Implement the minimal release-gate catch**

Add `subprocess.SubprocessError` to only the retained-campaign validation boundary at `tools/v05_beta_release_gates.py:1807`. Preserve the existing diagnostic and return path.

- [ ] **Step 3: Replace the obsolete `git show` operational regression**

In `tests/test_validate_qualified_review_evidence.py`, replace `test_validator_cli_keeps_post_blob_git_show_failure_operational` with a batch-transport failure test. Inject `GitObjectReadError("host-secret object failure")` at the finite transport boundary after an earlier successful read. Assert CLI exit 2, empty stdout, exactly one sanitized stderr line, no traceback, and no secret.

- [ ] **Step 4: Run consumer-boundary GREEN tests**

```powershell
python -m unittest tests.test_v05_beta_release_gates.V05ExternalEvidenceTests.test_git_object_read_failure_is_sanitized tests.test_validate_qualified_review_evidence.CampaignValidationTests.test_validator_cli_keeps_batch_object_failure_operational -v
```

Expected: PASS. Existing CLI messages remain byte-for-byte unchanged.

- [ ] **Step 5: Complete the consumer audit**

Use `rg -n "GitReader|CalledProcessError|SubprocessError" tools tests` and inspect every production `GitReader` constructor. Record each consumer and its sanitized boundary in the task report. `validate_qualified_review_evidence.py` and `seal_qualified_review_campaign.py` already catch `subprocess.SubprocessError`; prove those paths with focused tests. Confirm `v05_beta_release_evidence.py` does the same. Any uncovered consumer is a blocking finding and gets its own failing regression before a catch is changed.

- [ ] **Step 6: Run focused consumer suites**

```powershell
python -m unittest tests.test_validate_qualified_review_evidence -v
python -m unittest tests.test_v05_beta_release_gates.V05ExternalEvidenceTests -v
```

Expected: PASS.

- [ ] **Step 7: Commit Task 5**

```powershell
git add tools/v05_beta_release_gates.py tests/test_v05_beta_release_gates.py tests/test_validate_qualified_review_evidence.py
git commit -m "Sanitize batched Git read failures"
```

Checkpoint: every production consumer converts acquisition failures to its existing operator-safe result.

---

### Task 6: Produce exact equivalence, performance, and publication evidence

**Files:**
- Modify only if required by existing repository conventions: `tools/README.md`
- Verify: `.github/workflows/catalog-validation.yml`
- Verify: `tools/test-shards.json`
- Record in the implementation task report and pull-request description: exact commands, counts, wall times, and reviewed SHA.

**Interfaces:**
- Consumes: Tasks 1 through 5 at one exact candidate SHA.
- Produces: focused evidence, deterministic Git operation counts, hosted timing evidence, complete publication gates, and independent reviews.

- [ ] **Step 1: Run the focused bundle boundary**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle -v --durations 50
python tools/validate_test_shards.py --check
```

Expected: PASS. Record test count, skipped count, wall time, tree-command count, batch-check count, batch-content count, per-file `git show` count of zero, and separately counted control-manifest Git commands.

- [ ] **Step 2: Run focused qualified-review and release boundaries**

```powershell
python tools/run_test_shards.py --shard mapping_review_bundle --durations 50
python tools/run_test_shards.py --shard qualified_review_evidence --durations 50
python -m unittest tests.test_v05_beta_release_gates.V05ExternalEvidenceTests -v --durations 50
```

Expected: PASS. Run serially. Record each wall time as diagnostic evidence only.

- [ ] **Step 3: Review complete branch equivalence and consumer scope**

At the exact candidate SHA, review `git diff <merge-base>..HEAD` and confirm:

- packages for all three profiles match the trusted baseline byte for byte;
- no `GitReader` per-file `git show` remains;
- complete-tree indexing occurs once per used commit per reader;
- no persistent process or cleanup API was added;
- `tools/crosswalks/manifest.py` is unchanged unless a reviewed design amendment authorized it; and
- every `GitReader` consumer has a tested sanitized acquisition-failure boundary.

- [ ] **Step 4: Run the complete shard and discovery gates**

Use the repository's short-drive wrapper on Windows. Ensure no Python command overlaps another.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python tools/run_test_shards.py --all --durations 50
python -m unittest discover -s tests -v --durations 50
```

Expected: both PASS with the same population proven by `tests/test_validation_shards.py`.

- [ ] **Step 5: Run standalone publication validators in repository order**

```powershell
python tools/validate_test_shards.py --check
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

Expected: every command exits 0 and all Mermaid rows render with the pinned configuration. Set up the repository-pinned Node and Mermaid versions before the final command.

- [ ] **Step 6: Measure hosted improvement without a flaky gate**

Use the mapping-review shard duration already printed by `tools/run_test_shards.py` on the GitHub Actions runner. Compare at least three completed runs from the baseline SHA and at least three from the exact batching SHA on the same runner image and Python version. Report median, minimum, maximum, and percentage change alongside deterministic Git operation counts. Do not add an elapsed-time assertion to unit tests or required CI.

Keep the Phase 2 hosted 40 percent target open. This increment reports its contribution; the profile, qualified-review, and mutation-matrix hot-path increments still remain.

- [ ] **Step 7: Run final hygiene and exact-SHA checks**

```powershell
$mergeBase = git merge-base origin/main HEAD
git diff --check "$mergeBase..HEAD"
git diff --stat "$mergeBase..HEAD"
git status --porcelain=v1
git rev-parse HEAD
Get-ChildItem -Recurse -Directory -Filter __pycache__
```

Expected: no whitespace errors, only approved files changed, clean status, one lowercase 40-character SHA, and no caches.

- [ ] **Step 8: Dispatch exact-SHA reviews**

Request independent architecture and security reviews on the exact final SHA. Architecture review covers finite-process ownership, interface compatibility, and package-phase boundaries. Security review covers environment isolation, tree and batch parsers, acquisition limits, atomic caches, object identity, error sanitization, and adversarial cleanup. Resolve every Critical and Important finding. Any candidate change invalidates affected evidence and requires redispatch.

- [ ] **Step 9: Commit documentation only if Task 6 changed it**

If `tools/README.md` required an operator-visible update, run its focused documentation tests and commit only that file:

```powershell
git add tools/README.md
git commit -m "Document batched Git package reads"
```

If no documentation changed, make no Task 6 commit.

Checkpoint: the exact candidate has deterministic equivalence and operation-count proof, proportional timing evidence, passing publication gates, and clean independent reviews.

## Plan self-review

- Spec coverage: every approved requirement maps to Tasks 1 through 6, including limits, child cleanup, SHA-1 binding, tree hierarchy, batch framing, local object hashes, atomic caching, package phases, duck-reader compatibility, consumer sanitization, equivalence, operation counts, hosted timing, publication gates, and exact-SHA reviews.
- Placeholder scan: the plan contains no deferred implementation step. Conditional manifest work requires an explicit design amendment rather than an implicit scope expansion.
- Type consistency: `GitObjectReadError`, `_GitCommandResult`, `TreeEntry`, `_run_finite_git`, `_tree_index`, `read_many`, and `_read_package_files` have one spelling and one signature throughout.
- Test integrity: expectations use literal fixtures or trusted parent-commit package bytes. Protocol fakes sit below the real parser and cache. No acceptance test asserts that a mock exists.
