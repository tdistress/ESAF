# Validation harness Git object batching design

**Date:** 2026-08-06
**Status:** Approved design
**Parent design:** `docs/superpowers/specs/2026-08-01-validation-harness-efficiency-design.md`
**Scope:** The `GitReader` used to build qualified-review mapping bundles

## Purpose

Replace hundreds of per-file Git subprocesses with bounded, exact-object batch reads while preserving the current package bytes and fail-closed evidence boundary.

This is the second reviewable increment of validation-harness efficiency Phase 2. Test sharding is already complete. Profile, qualified-review, and bundle mutation-matrix hot paths remain separate later increments.

## Current cost

`GitReader.read_bytes()` currently runs `git ls-tree` to validate each uncached path and `git show <commit>:<path>` to read it. A cold package collection starts roughly 330 to 360 Git subprocesses before deterministic control-manifest regeneration. The mapping-bundle test module took 415.091 seconds for 57 tests on the pre-change Windows baseline.

## Selected approach

`GitReader` shall use a finite two-step object transaction:

1. `git cat-file --batch-check` verifies every requested object identity, type, and size.
2. A separate finite `git cat-file --batch` invocation returns the approved blob contents.

The reader shall validate each complete child result before adding any returned bytes to its cache. This avoids persistent-process ownership, finalizers, background stderr draining, and Windows pipe cleanup across current callers.

### Alternatives considered

A persistent `cat-file --batch` session would minimize changes to demand-driven reads, but it cannot prove a successful child exit before returning bytes. It would also add explicit close propagation, timeout recovery, stderr draining, and deterministic process cleanup to every caller and long-lived test fixture.

A single content batch without metadata preflight cannot enforce per-object and aggregate limits before fetching content.

An in-process Git object library would add a dependency and a new compatibility boundary for object stores, alternates, replacement refs, corruption, and repository formats. Git remains the authoritative object reader.

## Public interface and compatibility

`GitReader` shall add:

```python
def read_many(
    self,
    commit: str,
    paths: Sequence[str],
) -> dict[str, bytes]:
    ...
```

The method shall first freeze `paths` as a tuple and use only that snapshot for validation, limit accounting, lookup, retrieval, and result construction. The returned dictionary shall preserve snapshot order. An empty snapshot shall return an empty dictionary without starting Git. The method shall reject `str` and `bytes` in place of a sequence, unsafe paths, duplicate paths, and requests larger than 4,096 paths.

`resolve_commit()`, `read_bytes()`, and `list_files()` shall keep their signatures. `read_bytes()` shall delegate to a singleton `read_many()` request. A private collection helper shall use `read_many()` for an exact `GitReader` and shall fall back to repeated `read_bytes()` calls for existing duck-typed mutation readers. Existing test doubles do not need a new method.

No persistent child process, context manager, finalizer, or public cleanup method shall be introduced.

## Repository and process binding

`GitReader.__init__` shall freeze a sanitized child environment. It shall remove inherited variables whose names satisfy `name.upper().startswith("GIT_")`, which also covers case-insensitive Windows environment handling, then set only:

- `GIT_NO_REPLACE_OBJECTS=1`;
- `GIT_NO_LAZY_FETCH=1`;
- `GIT_OPTIONAL_LOCKS=0`;
- `GIT_TERMINAL_PROMPT=0`;
- `LC_ALL=C`; and
- `LANG=C`.

Every Git command shall use `shell=False`, binary input and output, a 120-second timeout, the resolved repository root, and this command prefix:

```text
git --no-replace-objects -c core.fsmonitor=false -C <root>
```

Before its first commit resolution or tree operation, the reader shall require `git rev-parse --show-object-format=storage` to return exactly `sha1\n`, with exit zero and empty stderr. It shall cache that successful storage-format check for the reader lifetime. Other object formats shall fail closed until deliberately designed and tested.

Every public commit argument shall be a full lowercase 40-character SHA. `resolve_commit()` shall require `git rev-parse --verify <sha>^{commit}` to return exactly the same SHA followed by one newline. Verified SHAs may be cached within one reader.

## Complete tree index

The reader shall build one complete immutable index per verified commit with:

```text
git ls-tree -r -t -z --full-tree --abbrev=40 <commit>
```

No caller pathspec shall restrict the index. The reader shall validate the complete output before publishing it to the cache. Each record shall have exactly this form:

```text
<mode> SP <type> SP <lowercase-40-character-object-id> TAB <UTF-8-path> NUL
```

The index shall retain canonical path, mode, object type, and object ID in an immutable `TreeEntry`. Parsing shall require:

- a terminal NUL with no empty interior record;
- no more than 100,000 records or 64 MiB of output;
- valid UTF-8 canonical repository-relative paths without control characters;
- no duplicate paths;
- valid parent-tree structure, meaning that every slash-delimited parent exists exactly once as a `040000 tree` entry and no non-tree entry has descendants; and
- only these mode and type pairs: `040000 tree`, `100644 blob`, `100755 blob`, `120000 blob`, and `160000 commit`.

Valid but prohibited entries elsewhere in the commit shall not poison unrelated reads. `read_many()` shall reject a requested tree, symlink, gitlink, missing path, or nonregular mode. For `list_files()`, an exact regular-file path shall return that one path, an exact tree shall return sorted regular descendants, and an exact symlink or gitlink shall fail. A missing path shall preserve the established empty-list result. A selected tree containing a nonregular descendant shall fail. Prefix matching shall distinguish `foo` from `foobar`.

The reader shall retain at most eight complete commit indexes without eviction. A request for a ninth distinct commit shall fail before Git runs. This hard reader-lifetime bound guarantees that a successfully indexed exact commit is never rebuilt. A failed parse shall publish no partial index.

## Finite object transaction

`read_many()` shall resolve every requested path through the verified tree index and send only direct object IDs to Git. It shall never send `commit:path`, filters, mailmap options, text conversions, or caller-controlled revision expressions.

Duplicate object IDs within one call may be fetched once. The logical request limits still count every requested path, including cache hits and paths sharing one object ID.

The metadata preflight command shall be:

```text
git cat-file --batch-check=%(objectname) %(objecttype) %(objectsize)
```

The reader shall require the exact response count and request order. Every record shall contain the requested lowercase object ID, the type `blob`, and a canonical decimal size.

Only after all preflight records pass shall the reader invoke:

```text
git cat-file --batch
```

The content parser shall read the binary response as:

```text
<expected-object-id> SP blob SP <expected-size> LF
<exactly expected-size bytes> LF
```

Each header shall be no larger than 256 bytes. The parser shall reject missing or extra records, reordering, wrong identities or types, noncanonical sizes, preflight size disagreement, oversized objects, truncated payloads, missing delimiters, and trailing stdout.

Before accepting a payload, the reader shall verify its SHA-1 Git object identity locally:

```python
sha1(
    b"blob " + str(size).encode("ascii") + b"\0" + content
).hexdigest() == expected_object_id
```

The transaction limits are:

- 4,096 requested paths;
- 32 MiB per blob;
- 128 MiB of logical requested content per call;
- 128 MiB total content cache;
- 256 bytes per batch header;
- 64 KiB of child stderr; and
- 120 seconds per Git subprocess.

The content cache shall use least-recently-used eviction and keys of `(exact_commit, object_id)`. This permits same-commit object deduplication without cross-commit reuse.

## Process output and failure handling

Object-format, commit-resolution, complete-tree, batch-check, and batch-content commands shall use one bounded finite-command helper. Concurrent drainers shall copy stdout and stderr in fixed-size chunks into capped temporary spools while the child runs. Crossing either command-specific cap shall signal overflow, terminate the child, escalate to kill if needed, reap it, join both drainers, and fail without parsing partial output. Timeout handling shall use the same cleanup sequence. The helper shall close every pipe and temporary resource on every path.

The complete-tree stdout cap is 64 MiB. Batch-check stdout is capped at `4_096 * 256` bytes. Batch-content stdout is capped at the 128 MiB logical content limit plus `4_096 * 257` bytes of framing. Object-format and commit-resolution commands use small fixed caps appropriate to their exact response contracts. Every command has a 64 KiB stderr cap. These are active acquisition limits, not post-exit observations.

Successful Git operations require exit zero and empty stderr. Treating even a benign Git warning as failure is intentional at this evidence boundary. Generic operator errors shall not expose child stderr or environment details.

`GitObjectReadError`, derived from `subprocess.SubprocessError`, shall represent object-format failures, batch-process failures, nonzero exits, nonempty stderr, protocol faults, identity mismatches, timeouts, and I/O failures. Unsafe paths, missing paths, nonregular requested entries, duplicate requests, and declared caller limits shall remain `ValueError` validation failures. `resolve_commit()` shall preserve its current translation of invalid or unresolved commit input to `ValueError`. Every production `GitReader` consumer shall be audited so `GitObjectReadError` reaches an existing sanitized operator-error boundary; the release gate shall receive a focused regression test because its current outer boundary catches `CalledProcessError`, not general `SubprocessError`.

Fetched objects shall remain private until the complete preflight and content operations pass, every child has exited cleanly, all framing is consumed, and every local object hash matches. A failed object transaction shall not modify the content cache. A fully validated tree index is independent successful state and may remain cached when a later object transaction fails.

## Package collection adoption

Package collection shall group reads into three commit-scoped phases:

1. all files in the candidate mapping snapshot;
2. candidate schemas, registry, catalog, fixed review files, and source-evidence files derived from the candidate README; and
3. the historical `controls/catalog.json` and all manifest-derived controls from the historical `control_source` commit.

Later singleton reads may reuse the validated cache. Historical controls shall not be included in a candidate-commit request.

Deterministic control-manifest regeneration currently uses a separate Git path. This increment shall measure and report those subprocesses separately. It shall not refactor `tools/crosswalks/manifest.py` unless an equivalence test proves that routing it through `GitReader` is necessary for the selected package boundary.

## Testing

Development shall follow strict red, green, refactor cycles. Tests shall cover:

- SHA-1 repository detection and exact lowercase commit resolution;
- sanitized child environments, including lowercase and mixed-case Git variables on Windows, replacement refs, grafts, and ambient repository redirection;
- one complete tree index per exact commit, immutable caching, the eight-commit hard limit, and commit isolation;
- malformed tree records, duplicates, invalid hierarchy, control characters, unsafe paths, and request-scoped tree, symlink, and gitlink rejection;
- exact prefix behavior for similarly named paths;
- multi-blob binary responses containing NULs, newlines, non-UTF-8 bytes, and payloads ending in a newline;
- preflight and content count, order, identity, type, size, framing, hash, stderr, exit, timeout, and cleanup failures;
- immutable path snapshots under adversarial sequence mutation;
- logical request, blob, aggregate, tree-output, entry-count, header, stderr, and cache limits, including termination of a child that overproduces output before unrestricted growth;
- atomic cache behavior and valid retry after a failed transaction;
- same-OID deduplication within one commit without cross-commit cache sharing;
- byte-for-byte package assembly and written-package equivalence for all three profiles; and
- deterministic Git invocation counts with one tree index per used commit, a bounded number of batch pairs, and zero per-file `git show` calls.

Tests shall assert observable behavior through real temporary repositories where practical. Protocol fakes shall inject complete binary process results at the Git transport boundary rather than asserting mock existence.

## Acceptance criteria

This increment is accepted when:

1. `GitReader` builds no more than one verified complete tree index per exact commit in a reader.
2. A cold package assembly uses a bounded number of batch-check and batch-content operations and no per-file `git show` calls.
3. Batched packages and manifests are byte-for-byte identical to the current implementation for all three profiles.
4. Existing and new adversarial path, object, framing, environment, consumer-boundary, and cache cases fail closed without partial output or content-cache contamination.
5. Focused bundle and qualified-review tests, the mapping-review shard, the complete shard suite, discovery, standalone publication validators, Mermaid rendering, link validation, and whole-branch hygiene pass on the exact candidate SHA.
6. Independent architecture and security reviews have no unresolved Critical or Important findings.

Performance evidence shall report Git operation counts and observed wall times. Timing is diagnostic and shall not replace deterministic equivalence and operation-count gates. The Phase 2 hosted 40 percent target remains open until Git batching and the three later hot-path increments have all landed.
