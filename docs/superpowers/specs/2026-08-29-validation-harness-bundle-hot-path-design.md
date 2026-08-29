# Validation harness bundle hot-path design

**Date:** 2026-08-29
**Status:** Approved for implementation
**Parent design:** `docs/superpowers/specs/2026-08-01-validation-harness-efficiency-design.md`
**Issue:** [#90](https://github.com/tdistress/ESAF/issues/90)
**Scope:** Mapping-review bundle reviewed-candidate mutation matrices, pure
candidate-state / findings / schema boundaries, equivalence proof, and Phase 2
hosted measurement closeout

## Purpose

Reduce the cost of `tests/test_build_mapping_review_bundle.py` reviewed-candidate
reject matrices without changing package collection semantics or weakening
Git/writer/security coverage. Selected mutations shall exercise pure production
boundaries over already parsed metadata. Full `assemble_package` /
`collect_package_files` paths shall remain for collector integrity, Git batching,
writer safety, lifecycle/registry rules, and representative reviewed success.

This is the final validation-harness efficiency Phase 2 hot-path increment. It
does not change normative ESAF content, close Issue 55, or advance Draft
mappings.

## Baseline and cost

The `mapping_review_bundle` shard is the single module
`tests/test_build_mapping_review_bundle.py`. The Phase 2 parent design recorded
about 151 seconds for this module before earlier increments. Today,
`ReviewedCandidateAssemblyTests` clones the repository once, builds a reviewed
Core candidate, and then pays a Git commit plus full `assemble_package` for each
reject mutation.

Selected reject mutations fail inside:

- `_require_candidate_state`
- `_require_reviewed_findings`
- `_validate_candidate_metadata` / schema validation

before package completeness work is the subject of the assertion. Those cases
shall move to pure boundaries.

## Invariants

1. Identical metadata inputs shall produce identical `ValueError` text and
   success/failure disposition through full and narrow paths.
2. Package population, Git batching, writer, security, and CLI tests remain on
   the complete path.
3. Case population shall not shrink. Digests shall bind the selected inventory.
4. No process-global, cross-call, path, fixture, or mtime cache is introduced.
5. Issue 55 and Draft mapping lifecycle states remain unchanged.

## Selected population

`tests/mapping_review_bundle_policy_cases.py` is the authoritative inventory.

| Case family | Count | Boundary |
|---|---:|---|
| Mixed draft status on record | 1 | `candidate_state` |
| Approved status on snapshot / record | 2 | `schema` |
| Missing reviewer on snapshot / record | 2 | `schema` |
| Mapper self-review on snapshot / record | 2 | `candidate_state` |
| Critical/Important × open/accepted findings | 4 | `reviewed_findings` |
| Required reviewer field removals | 5 | `schema` |
| **Selected total** | **16** | |

Retained full path (non-exhaustive): reviewed success assembly, lifecycle event
rejection, candidate-sourced schema tightening, MutatingReader collector suite,
Git/writer/security/CLI suites, and one representative reviewed reject through
`assemble_package`.

## Pure boundaries

`tools/build_mapping_review_bundle.py` shall expose:

```python
def validate_metadata_against_schema(
    schema: object,
    metadata: dict[str, object],
    subject: str,
) -> None: ...
```

Production `_validate_candidate_metadata` shall load the schema then call that
pure checker. `_require_candidate_state` and `_require_reviewed_findings` remain
the candidate-state and findings boundaries; matrices shall call them directly.

## Equivalence

`tools/verify_mapping_review_bundle_hot_path_equivalence.py` shall compare, for
every inventory case on a clean exact candidate:

1. full path — mutate reviewed fixture metadata and invoke `assemble_package`
   (or the smallest full collector entry that surfaces the same error); and
2. narrow path — apply the same metadata mutation and invoke the pure boundary;

then require identical success/error projections and print
`candidate_sha`, counts, population digest, and `equivalence=PASS`.

Stage 1 seals the proof before matrix migration. Stage 2 migrates only selected
call sites and adds structural guards forbidding `assemble_package` /
`_assemble_after` in the fast matrix class.

## Hosted Phase 2 measurement

After the hot path lands, record three successful hosted full-suite runs against
the sealed 751-second eight-run median. Target is at least a 40 percent
reduction (≤ ~450.6s). Timing remains diagnostic for intermediate commits; the
final Issue #90 closeout shall either meet the target or explicitly defer with
evidence.

## Non-goals

- Changing package bytes, directions, or review protocol semantics
- Closing Issue 55 or advancing Draft mappings
- Narrowing MutatingReader collector integrity cases
- Claiming the 40 percent target from local timings alone
