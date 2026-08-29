# Phase 2 hosted timing closeout — Issue #90

**Date:** 2026-08-29
**Candidate:** `ea27c5b4d1fee53b2e1e7f68a0ed54a1ad0b0fe2` (PR #97 merge)
**Disposition:** `DEFER` the sealed ≥40% serial full-suite wall-time target

## Sealed criterion

`docs/superpowers/specs/2026-08-01-validation-harness-efficiency-design.md`
requires hosted full-suite wall time for serial
`python -m unittest discover -s tests -v` to decrease by at least 40% relative
to the 751-second eight-run median (≤ ~450.6s), measured over three successful
runs.

## Evidence recorded

| Run | SHA | Role | Metric | Seconds |
|---|---|---|---|---:|
| [33269146568](https://github.com/tdistress/ESAF/actions/runs/33269146568) | `ea27c5b` | post-merge main | parallel shard critical path / sum | 279 / 567 |
| [33268352061](https://github.com/tdistress/ESAF/actions/runs/33268352061) | `35e830e` | PR #97 head | parallel shard critical path / sum | 445 / 805 |
| [30726987363](https://github.com/tdistress/ESAF/actions/runs/30726987363) | `df2d5d6` | pre-shards historical | serial unit-test step | 750 |

Hot-path technical deliverables (inventory, pure boundaries, equivalence PASS)
landed in PR #97. Local ReviewedCandidateAssemblyTests diagnostic wall time
fell from ~34.9s to ~7.3s.

## Why DEFER

1. Current Repository validation CI runs **parallel shards**, not the sealed
   serial discover wall-time metric.
2. Only **two** successful hosted runs contain the bundle hot path; a third
   comparable serial sample could not be dispatched (`workflow_dispatch` /
   rerun unavailable to the agent token).
3. Parallel critical-path timings must not be claimed against the 751s serial
   median.

## Reconsideration triggers

- Restore or add a hosted serial `unittest discover` (or release-evidence
  `full_suite`) measurement step; or
- Explicitly amend the Phase 2 acceptance criterion to a parallel-shard metric
  with a new sealed baseline; and
- Record three successful hosted runs under the chosen comparable metric.

## Nonclaims

This deferral does not claim the ≥40% target is met, change normative content,
close Issue #55, or advance Draft mappings.
