# ESAF v0.9-rc1 Publication Gates Design

**Date:** 2026-08-29  
**Issue:** [#95](https://github.com/tdistress/ESAF/issues/95)  
**Status:** Active design for evidence → closure → published

## Intent

Close ordinary `v0.9-rc1` Working Draft release-candidate gates on one exact
candidate after prerequisite workstreams are dispositioned. Mirror the
`v0.5-beta` three-phase record machine without cloning beta-only UK
owner-risk campaign machinery.

## Prerequisites (already on `main`)

| Workstream | Disposition | Evidence |
|---|---|---|
| Harness Phase 2 | Hot path merged; hosted serial ≥40% `DEFER` | PR #97; `docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md` |
| ESAF-1300 / 1400 / 1700 | Working Drafts linked | PR #98 |
| NIST AI RMF readiness | `HOLD` (mapper/reviewer naming) | PR #99 + ancestry fix #100; `crosswalks/nist-ai-rmf.md` |

Issues `#55` and `#60` may remain open.

## Phase machine

Phases: `evidence_candidate` → `closure_candidate` → `published`.

Gate IDs (same vocabulary as beta, without inventing parallel names):

`scope`, `technical`, `editorial`, `terminology`, `cross_reference_rendering`,
`standards_mapping`, `profile_scope`, `release_metadata`, `governance`,
`post_merge`.

| Phase | Gate states |
|---|---|
| `evidence_candidate` | all `open` |
| `closure_candidate` | all `ready` except `post_merge=open` |
| `published` | all `closed` |

## Record

Path: `docs/superpowers/reviews/2026-08-29-v09-rc1-publication-readiness.md`

Front matter shall bind: `release: 0.9-rc1`, `tag: v0.9-rc1`, `issue: 95`,
`repository_scope: complete_git_tracked_repository`, `phase`, `scope` counts
derived from live catalogs, `prerequisite_dispositions`, `gates`, and
`publication` (null fields until published).

Body shall include Scope, Prerequisite dispositions, Lifecycle boundary,
Nonclaims, and Publication evidence sections appropriate to the phase.

## Validator

`tools/v09_rc1_release_gates.py --check` shall:

1. Parse and validate the readiness record contract for the current phase.
2. Require prerequisite paths and dispositions (`phase2_timing: DEFER`,
   `esaf_1300/1400/1700: working_draft`, `nist_ai_rmf: HOLD`).
3. Recompute scope counts from catalogs and fail on drift.
4. Keep `tools/release_gates.py` and `tools/v05_beta_release_gates.py` frozen
   as historical validators.
5. For `closure_candidate`, enforce the metadata-only allowlist:
   `VERSION.md`, `README.md`, `ROADMAP.md`, `CHANGELOG.md`,
   `project/RELEASE_PLAN.md`, readiness record.
6. For `published`, require annotated-tag identity fields and issue evidence URL.

## Closure and publish sequence

1. Land evidence tooling + `evidence_candidate` record; CI green.
2. Independent technical, editorial, and governance reviews on exact SHA.
3. Closure allowlist PR advances to `closure_candidate` and syncs VERSION /
   README / ROADMAP / CHANGELOG / RELEASE_PLAN.
4. Merge; re-validate merged `main` (new candidate SHA).
5. Create annotated `v0.9-rc1` only after post-merge green.
6. Published-record PR closes gates, records tag peel, moves backlog/milestones.

## Nonclaims

Working Draft release candidate only. Does not close `#55`/`#60`, clear PCI or
HITRUST blockers, advance Draft artifacts to approved, or claim certification,
compliance, equivalence, endorsement, assurance, or production readiness.
