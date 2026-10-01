# NIST AI RMF Owner-Risk Draft Mapping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clear NIST AI RMF people-gate HOLD under owner disposition, derive readiness GO, and publish a complete Draft 72-subcategory ESAF→AI RMF mapping set.

**Architecture:** Owner-risk amendment to the existing readiness matrix (Draft-only), then UK-style ESAF-1600 snapshot under `crosswalks/mappings/nist/ai-rmf/1.0/0.17-draft/0.1.0/`, regenerating catalogs and synchronizing live release-gate surfaces.

**Tech Stack:** Python validators (`validate_crosswalks`, `render_nist_ai_rmf_mapping_go_no_go`, release gates), Markdown/YAML ESAF-1600 snapshots, unittest.

## Global Constraints

- Lifecycle remains `draft`; `events: []`; no reviewer/approver metadata on the mapping set.
- Direction `esaf_to_external` only; default `no_direct_mapping` when ESAF does not expressly provide the outcome.
- No NIST endorsement/compliance/equivalence claims.
- Keep `PYTHONDONTWRITEBYTECODE=1`; do not commit `__pycache__`.
- Register any new `tests/test_*.py` in `tools/test-shards.json`.
- Never add Cursor attribution trailers.

---

### Task 1: Record owner disposition and flip readiness to GO

**Files:**
- Create: `docs/superpowers/reviews/2026-10-01-nist-ai-rmf-owner-risk-people-gate-disposition.md`
- Modify: `docs/superpowers/specs/2026-08-29-nist-ai-rmf-mapping-readiness-matrix.json`
- Modify: `docs/superpowers/specs/2026-08-29-nist-ai-rmf-source-readiness-design.md`
- Regenerate: `docs/superpowers/reviews/2026-08-29-nist-ai-rmf-1.0-mapping-go-no-go-review.md`
- Modify: `crosswalks/nist-ai-rmf.md` (temporary GO-without-artifacts text until Task 2)
- Modify: `docs/superpowers/reviews/2026-08-29-nist-ai-rmf-1.0-mapping-go-no-go-traceability.md`
- Modify: `tests/test_nist_ai_rmf_source_readiness.py`, `tests/test_render_nist_ai_rmf_mapping_go_no_go.py`, `tests/test_esaf_1600_foundation.py` (NIST landing assertions)

- [ ] Write owner disposition review citing Approach 1 approval and deferred qualified review
- [ ] Clear matrix blockers; set `mapper_and_reviewer_readiness` to PASS with owner-disposition evidence; set `recorded_decision` to GO
- [ ] Run `python tools/render_nist_ai_rmf_mapping_go_no_go.py` and `--check`
- [ ] Update landing/traceability/design reconsideration text for GO + deferred review
- [ ] Update focused readiness tests for GO (still forbid mappings until Task 2 lands in same PR, or relax artifact-zero asserts once mappings exist)
- [ ] Commit

### Task 2: Author Draft NIST AI RMF mapping snapshot

**Files:**
- Create: `docs/superpowers/specs/2026-10-01-nist-ai-rmf-1.0-draft-mapping-oracle.json` (per-subcategory dispositions)
- Create snapshot under `crosswalks/mappings/nist/ai-rmf/1.0/0.17-draft/0.1.0/` (`README.md`, `PROVISION_INVENTORY.md`, `ESAF_CONTROL_MANIFEST.json`, 72 records)
- Create: `crosswalks/registry/nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0.md`
- Update: `crosswalks/nist-ai-rmf.md` counts and Draft mapping links
- Regenerate: `crosswalks/catalog.json`, `crosswalks/CATALOG.md`
- Create: `tests/test_nist_ai_rmf_v10_crosswalk.py` + shard registration

- [ ] Pin `source_commit_sha` to the Task 1 commit (control catalog unchanged)
- [ ] Build manifest via `tools.crosswalks.manifest.build_control_manifest`
- [ ] Generate 72 records from the curated oracle; validate with `python tools/validate_crosswalks.py --write` then `--check`
- [ ] Add focused snapshot tests
- [ ] Commit

### Task 3: Synchronize release surfaces and gate expectations

**Files:**
- Modify: `docs/superpowers/reviews/2026-09-16-v017-draft-publication-readiness.md` (and earlier published readiness records that pin live NIST path / derived scope)
- Modify: `tools/v017_draft_release_gates.py` and earlier `tools/v0*_draft_release_gates.py` / `tools/v09_rc1_release_gates.py` NIST prerequisite expectations from HOLD→GO markers
- Modify: matching `tests/test_v0*_draft_release_gates.py` negative tests that assert HOLD
- Modify: `project/BACKLOG.md`, `project/RELEASE_PLAN.md`, `project/MILESTONES.md` as needed for current truth
- Modify: `crosswalks/README.md`, `tests/test_release_metadata.py` if they hardcode NIST HOLD

- [ ] Update live prerequisite expectations and derived scope counts
- [ ] Preserve immutable publication identity fields and closed gate truth
- [ ] Run affected release-gate `--check` commands against `origin/main`
- [ ] Commit

### Task 4: Validate, push, open PR, merge if green

- [ ] `PYTHONDONTWRITEBYTECODE=1` focused tests + `python -m unittest discover -s tests -v` (with git signing disabled for fixture speed)
- [ ] `python tools/plan_validation.py --base origin/main --candidate HEAD` and execute selected route
- [ ] `git diff --check origin/main..HEAD`; confirm no `__pycache__`
- [ ] Push branch; open draft PR via ManagePullRequest; address CI; merge when authorized and green
