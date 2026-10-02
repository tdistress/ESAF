# NIST CSF Owner-Risk Draft Mapping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clear NIST CSF people-gate HOLD under owner disposition, derive readiness GO, and publish a complete Draft 106-subcategory ESAF→CSF 2.0 mapping set.

**Architecture:** Owner-risk amendment to the existing readiness matrix (Draft-only), then UK-style ESAF-1600 snapshot under `crosswalks/mappings/nist/csf/2.0/0.17-draft/0.1.0/`, regenerating catalogs and synchronizing live release-gate surfaces.

**Tech Stack:** Python validators (`validate_crosswalks`, `render_nist_csf_mapping_go_no_go`, release gates), Markdown/YAML ESAF-1600 snapshots, unittest.

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
- Create: `docs/superpowers/reviews/2026-10-02-nist-csf-owner-risk-people-gate-disposition.md`
- Create: `docs/superpowers/specs/2026-10-02-nist-csf-owner-risk-draft-mapping-design.md`
- Modify: `docs/superpowers/specs/2026-09-07-nist-csf-mapping-readiness-matrix.json`
- Modify: `docs/superpowers/specs/2026-09-07-nist-csf-source-readiness-design.md`
- Regenerate: `docs/superpowers/reviews/2026-09-07-nist-csf-2.0-mapping-go-no-go-review.md`
- Modify: `crosswalks/nist-csf.md`
- Modify: `docs/superpowers/reviews/2026-09-07-nist-csf-2.0-mapping-go-no-go-traceability.md`
- Modify: focused readiness and foundation landing tests

- [ ] Write owner disposition review citing Approach 1 approval and deferred qualified review
- [ ] Clear matrix blockers; set `mapper_and_reviewer_readiness` to PASS; set `recorded_decision` to GO
- [ ] Run `python tools/render_nist_csf_mapping_go_no_go.py` and `--check`
- [ ] Update landing/traceability/design reconsideration text for GO + deferred review
- [ ] Update focused readiness tests for GO
- [ ] Commit

### Task 2: Author Draft NIST CSF mapping snapshot

**Files:**
- Create: `docs/superpowers/specs/2026-10-02-nist-csf-2.0-draft-mapping-oracle.json`
- Create snapshot under `crosswalks/mappings/nist/csf/2.0/0.17-draft/0.1.0/`
- Create: `crosswalks/registry/nist--csf--2.0--esaf-0.17-draft--0.1.0.md`
- Update: `crosswalks/nist-csf.md` counts and Draft mapping links
- Regenerate: `crosswalks/catalog.json`, `crosswalks/CATALOG.md`
- Create: `tests/test_nist_csf_v20_crosswalk.py` + shard registration

- [ ] Pin `source_commit_sha` to the Task 1 commit
- [ ] Build manifest via `tools.crosswalks.manifest.build_control_manifest`
- [ ] Generate 106 records from the curated oracle; validate with `validate_crosswalks.py`
- [ ] Add focused snapshot tests
- [ ] Commit

### Task 3: Synchronize release surfaces and gate expectations

**Files:**
- Modify: live readiness records that pin NIST CSF path / derived scope
- Modify: `tools/v0*_draft_release_gates.py` NIST CSF prerequisite expectations HOLD→GO
- Modify: matching release-gate tests
- Modify: tracker surfaces as needed for current truth

- [ ] Update live prerequisite expectations and derived scope counts
- [ ] Preserve immutable publication identity fields and closed gate truth
- [ ] Run affected release-gate `--check` commands
- [ ] Commit

### Task 4: Validate, push, open PR, merge if green

- [ ] Focused tests + full suite with signing disabled for fixtures
- [ ] `python tools/plan_validation.py --base origin/main --candidate HEAD` and selected route
- [ ] `git diff --check origin/main..HEAD`; confirm no `__pycache__`
- [ ] Push; open PR; merge when green
