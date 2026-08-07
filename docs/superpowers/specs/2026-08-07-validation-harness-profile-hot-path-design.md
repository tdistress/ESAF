# Validation harness profile hot path design

**Date:** 2026-08-07
**Status:** Approved design
**Parent design:** `docs/superpowers/specs/2026-08-01-validation-harness-efficiency-design.md`
**Baseline commit:** `df124e13a7b4a377524c50e73358234425913e72`
**Scope:** Profile claim and source-authority language matrices in `tests/test_validate_profiles.py`

## Purpose

Reduce the cost of the profile validation test module without removing any language case or weakening the complete repository validation path. Exhaustive phrase, voice, aspect, polarity, and framing matrices shall exercise the same production text diagnostics used by `validate()`. Representative integration tests shall continue through package discovery, loading, schema validation, authoritative-source comparison, traceability, source-boundary validation, claim validation, and diagnostic normalization.

This is the profile hot-path increment of validation-harness efficiency Phase 2. It does not change profile policy, accepted language, diagnostic text, or validator behavior.

## Baseline and cost

On current `main` at `df124e13a7b4a377524c50e73358234425913e72`, the complete suite ran 205 tests in 416.717 seconds and reported five Windows symlink privilege skips. The slowest profile language-matrix methods took 5.6 to 9.7 seconds each. Each of those methods issued 28 to 46 calls to the complete `validate()` path.

Most cases change only README prose. A complete call still rediscovers the profile inventory, reads and validates every package component, loads schemas and control records, compares authoritative Markdown and derived JSON, checks traceability, and repeats filesystem defenses. Those operations remain necessary for integration coverage, but they do not need to run once for every grammatical variation.

## Invariants

The implementation shall preserve all of the following:

1. Every existing input phrase and every voice, tense, aspect, polarity, framing, complement, insertion, conjunction, modifier, and dynamic-source combination.
2. The exact accepted or rejected disposition of each case.
3. Existing diagnostic text, repository-relative locations, deduplication, and deterministic sort order.
4. JSON traversal and location reporting for every structured narrative field.
5. README scanning and `PROFILE.md` scanning after authoritative JSON blocks are removed.
6. Dynamic matching against the profile's declared `excluded_sources`.
7. Full validation coverage for inventory, schemas, filesystem boundaries, symlinks and junctions, package identity, authoritative-source integrity, control population, semantic rules, traceability, CLI behavior, exit codes, and sanitized operational errors.
8. The distinction between content diagnostics and operational failures.

The change shall not add a process-global cache, path cache, fixture cache, mtime cache, or any cache whose correctness depends on mutable test files. It shall not add timing assertions.

## Selected design

### Two production text-diagnostic boundaries

`tools/validate_profiles.py` shall expose two narrow deterministic functions:

```python
def claim_text_diagnostics(text: str, location: str) -> list[str]:
    ...


def source_authority_text_diagnostics(
    text: str,
    location: str,
    excluded_sources: list[str],
) -> list[str]:
    ...
```

`location` is the complete repository-relative diagnostic prefix. For Markdown it is the file path. For a JSON string it is the file path followed by the existing document location. The boundary functions shall not read files, discover packages, parse JSON, load schemas, resolve controls, or mutate inputs.

`claim_text_diagnostics()` shall apply the existing `contains_affirmative_weakening()` and `asserted_profile_phrases()` rules. It shall return the current control-weakening and prohibited-assertion messages with the supplied location.

`source_authority_text_diagnostics()` shall apply the existing `contains_affirmative_source_authority()` rule using the supplied excluded-source snapshot. It shall return the current prohibited source-authority message with the supplied location.

Each function shall return a sorted, deduplicated list. This keeps the production wrappers' current externally visible order and gives matrix tests the same diagnostic contract as the complete validator. The lower-level Boolean and phrase helpers remain implementation details. Matrices shall test the diagnostic boundary rather than assembling expected behavior from those helpers.

### Production wrapper adoption

`claim_diagnostics()` shall retain ownership of package traversal, prohibited structured-field checks, UTF-8 handling, Markdown reads, and authoritative JSON block removal. For every narrative string it shall construct the existing location and extend its results with `claim_text_diagnostics()`. Its final sorted, deduplicated return remains unchanged.

`source_boundary_diagnostics()` shall retain ownership of risk `source_basis` resolution, package traversal, excluded-source extraction, UTF-8 handling, Markdown reads, and authoritative JSON block removal. It shall pass every narrative string and its existing location to `source_authority_text_diagnostics()`. Its final sorted, deduplicated return remains unchanged.

`validate()` shall keep its current order of semantic, authoritative-source, traceability, source-boundary, and claim checks. No other validator layer moves into the text functions.

## Test migration

### Equivalence before replacement

Migration shall proceed in two observable stages.

First, every matrix case selected for the hot path shall run through both routes:

1. write the case to the same fixture location and call complete `validate()`;
2. call the applicable production text-diagnostic boundary with the same text, diagnostic location, and excluded-source list; and
3. compare the exact diagnostic lists, including message text and order.

Affirmative cases, direct denials, postposed denials, quotations, rejected-claim frames, metalinguistic discussion, active and passive voice, simple and perfect aspects, bounded adverbs, pronoun and named-source forms, and dynamic excluded-source cases shall all pass this equivalence stage. A mismatch blocks migration.

After the complete moved population passes, the exhaustive language matrices shall call only the applicable text-diagnostic boundary. Their case tables and product dimensions shall remain byte-for-byte unchanged except for the assertion route. The implementation shall not consolidate, delete, sample, or rewrite cases to obtain the speedup.

The final tests shall enforce the migration structurally. Exhaustive matrix helpers shall fail if they invoke `validate()`, and each case shall invoke its production text boundary exactly once. These are deterministic call-count assertions, not elapsed-time assertions.

### Full-path coverage retained

Complete `validate()` tests shall remain for representative examples of:

- affirmative, negative, and metalinguistic claim language in README content;
- affirmative, negative, and metalinguistic excluded-source authority language;
- a generic authority named dynamically in `excluded_sources`;
- `PROFILE.md` prose scanning with authoritative JSON blocks stripped before text diagnostics;
- narrative strings and prohibited keys nested in structured JSON components;
- exact diagnostic ordering and deduplication when semantic and language errors coexist;
- risk source-basis resolution and permitted-source behavior;
- malformed and duplicate JSON, schema failures, missing or unexpected package entries, unsafe paths, files replaced by directories, symlinks, junctions, and repository-boundary checks;
- package inventory, identity, authoritative control population, mapping references, lifecycle semantics, and traceability; and
- CLI success, content-error exit one, operational-error exit two, UTF-8 failures, permission failures, resolution failures, and host-path sanitization.

Existing focused tests that already call `claim_diagnostics()` or another narrow helper may remain when they test structured traversal or a lower-level grammar rule. Only exhaustive language matrices that repeatedly call the complete validator are candidates for replacement.

## Error handling and compatibility

The text boundaries are pure classification and formatting functions. They shall not catch or translate filesystem, decoding, schema, inventory, or operational errors because they perform none of those operations. The package wrappers retain the current error behavior.

The excluded-source list shall be treated as a call input. The source-authority function shall not retain it after return or derive it from ambient repository state. Tests may reuse one immutable value snapshot across matrix cases, but production shall continue to read the list from each loaded profile.

No public CLI or evidence format changes. `python tools/validate_profiles.py --check` shall produce the same output and exit status for the same repository tree before and after the refactor.

## Alternatives considered

### Reusable fixture template

A prebuilt valid profile tree could be copied or cloned for each test. This may reduce setup work for tests that construct a fresh package, but the slow matrices already reuse one fixture inside a method. Their dominant cost is the repeated complete validation call after each one-line mutation. A template also creates a new fixture-integrity boundary around copied files, links, permissions, and mutable state. It is secondary to removing work that is unrelated to the rule under test.

### Validation-call-scoped parsing caches

A cache limited to one `validate()` call could avoid a few repeated reads or parses without creating cross-call stale-state risk. It would not help the dominant pattern because each matrix case starts a new validation call. The validator already needs most package data once per complete call, so the available saving is smaller and touches broader production code. Call-scoped parsing may be considered separately if later profiling identifies repeated work within one invocation.

Cross-call and process-global caches are rejected. The tests deliberately mutate files between calls, and any cache keyed by path, timestamp, or ambient repository state would create a stale-validation risk.

## Verification

Development shall use a red, green, refactor sequence:

1. Add focused tests for the two diagnostic boundaries and their exact output order.
2. Route production wrappers through the new boundaries while all existing tests still use their current paths.
3. Run every candidate matrix through both the narrow and complete paths and prove exact equivalence.
4. Replace complete calls only in the proven exhaustive matrices and add deterministic guards against regression to full validation.
5. Run the focused profile module, the profile shard, complete discovery, standalone validators affected by profiles or references, and whole-branch hygiene checks.

The implementation review shall compare the complete branch diff and verify that matrix inputs and product dimensions have not changed. Any behavior change requires a separate design and is outside this increment.

## Acceptance criteria

This increment is accepted when:

1. Production claim and source-authority wrappers use the same two text-diagnostic functions exercised by the migrated matrices.
2. Every moved case has first produced an exact narrow-path and full-path equivalence result.
3. The final exhaustive matrices preserve every existing case and issue no complete `validate()` calls.
4. Representative full-path tests cover README, stripped `PROFILE.md`, structured JSON, dynamic excluded sources, affirmative, negative, and metalinguistic language.
5. Filesystem, security, schema, inventory, authoritative-source, traceability, CLI, ordering, and error-sanitization tests remain on the complete path and pass.
6. Focused and complete validation passes on the exact candidate SHA with no new generated cache or build output.
7. Independent review finds no unresolved Critical or Important issue.

Timing data may be reported after the deterministic gates pass, but it is diagnostic only. The hosted Phase 2 target of at least a 40 percent reduction from the 751-second median remains open until the qualified-review and bundle mutation-matrix increments have landed. The final decision shall use three successful hosted full-suite runs after all Phase 2 increments are present.

## Non-goals

- Changing claim, weakening, source-authority, or metalinguistic recognition.
- Changing any diagnostic string, location, ordering, or exit code.
- Reducing the language population or replacing exhaustive matrices with samples.
- Moving structural JSON-field or risk source-basis rules into text diagnostics.
- Caching mutable repository or fixture state across validation calls.
- Optimizing the qualified-review or bundle mutation matrices in this increment.
- Declaring the Phase 2 performance target complete from a local run or this increment alone.
