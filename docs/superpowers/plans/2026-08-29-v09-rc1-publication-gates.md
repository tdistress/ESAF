# ESAF v0.9-rc1 Publication Gates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Enforce Issue #95 with a three-phase readiness record and
`tools/v09_rc1_release_gates.py`, starting at `evidence_candidate`.

**Architecture:** Freeze historical `release_gates` / `v05_beta_release_gates`.
Add a lean v09 validator that checks phase, prerequisites, scope drift, gate
states, allowlist transitions, and published tag fields. Status surfaces
advance only on the closure allowlist.

**Tech Stack:** Python 3, PyYAML, unittest, GitHub Actions catalog-validation.

---

### Task 1: Failing contract tests

**Files:**
- Create: `tests/test_v09_rc1_release_gates.py`

- [ ] Assert missing readiness record fails `--check`
- [ ] Assert wrong phase gate-state matrix fails
- [ ] Assert prerequisite disposition drift fails
- [ ] Assert scope count drift fails
- [ ] Assert happy-path `evidence_candidate` passes

### Task 2: Evidence record + validator

**Files:**
- Create: `docs/superpowers/reviews/2026-08-29-v09-rc1-publication-readiness.md`
- Create: `tools/v09_rc1_release_gates.py`
- Modify: `tools/plan_validation.py`, `.github/workflows/catalog-validation.yml`,
  `tools/README.md`, `tools/test-shards.json`

- [ ] Author `evidence_candidate` readiness record with live scope counts
- [ ] Implement `--check` validator
- [ ] Wire CI + publication planner command
- [ ] Add modules to remaining shard

### Task 3: Validate and open PR

- [ ] Focused tests + `render`/`validate_links` as needed
- [ ] `python tools/plan_validation.py --base origin/main --candidate HEAD`
- [ ] Commit, push, draft PR for evidence phase (VERSION stays `0.5-beta`)

### Task 4 (later PR): Closure allowlist

- Advance to `closure_candidate`; sync VERSION/README/ROADMAP/CHANGELOG/RELEASE_PLAN
- Exact-SHA reviews; merge; post-merge re-check

### Task 5 (later): Tag + published

- Annotated `v0.9-rc1` after post-merge green
- Published-record PR; close #95
