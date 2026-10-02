# SOC 2 AICPA TSC Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record an evidence-pinned, mechanically derived SOC 2 Trust Services Criteria readiness decision without publishing unauthorized source-derived content or creating mapping artifacts.

**Architecture:** Follow the repository's PCI DSS/CIS readiness pattern: immutable source and rights evidence feed a closed JSON matrix; a deterministic renderer derives the decision; a landing page and issue traceability record expose the result. Focused tests, CI, validation planner, and test-shard manifest wiring enforce the hold boundary.

**Tech Stack:** Markdown, JSON, Python standard library, `unittest`, repository validation tools and GitHub Actions.

---

## Files to create or modify

- Create the source-readiness design, oracle, matrix, rights review, decision review, traceability review, and focused tests under `docs/superpowers/` and `tests/`.
- Create `crosswalks/soc-2.md` as the readiness status surface; do not create mapping or registry records.
- Create `tools/render_soc2_aicpa_tsc_mapping_go_no_go.py` as a deterministic matrix validator and Markdown renderer.
- Modify `.github/workflows/catalog-validation.yml`, `tools/README.md`, `tools/plan_validation.py`, `tests/test_plan_validation.py`, and `tools/test-shards.json` to validate and route the new work.
- Modify `project/BACKLOG.md` to link unmilestoned Issue #219 and state the completed readiness disposition.
- Do not modify `crosswalks/catalog.json`, `crosswalks/registry/`, or `crosswalks/mappings/` under `HOLD`.

## Task 1: Pin rights evidence and source oracle

- [ ] Record reviewed official AICPA source URLs, source title/edition and dates, access state, and limits of observed evidence. Do not retrieve restricted source bytes, scrape, or include criterion text.
- [ ] Write and independently review the rights review first. Partition identifiers, titles, structural inventory, paraphrases, derivative mapping analysis, and official links; distinguish minimal source metadata from mapping field classes; do not infer a PDF-specific license from the website terms. A later re-entry reviewer must verify every proposed metadata and mapping field class, publication channel, and written permission.
- [ ] Commit the rights review before authoring the source oracle or matrix.
- [ ] Add the source oracle with retrieval date, source identity, access behavior, rights references, and explicit nulls for unobtained bytes, digest, counts, and inventory.

## Task 2: Add the mechanically derived HOLD decision

- [ ] Write tests first for a valid HOLD matrix, blocked-gate coverage, fail-closed rights boundary, no mapping artifacts, and deterministic rendering. Cover all eight ordered gates; GO conditions; HOLD requiring reconsiderable blockers; NO_GO requiring a terminal blocker; and rejection of a HOLD with a terminal blocker or a NO_GO without one.
- [ ] Implement the renderer from the PCI DSS/CIS patterns with strict key/status/reference validation, terminal-blocker exclusivity, design-conformant GO/HOLD/NO_GO derivation, and `--check` support.
- [ ] Add a matrix with blockers for source artifact, rights, inventory, semantic probe, and named qualified people; preserve PASS only for schema fit and enforceable overclaiming controls.
- [ ] Generate the decision review and traceability report for Issue #219.
- [ ] Add the crosswalk landing page with decision, zero artifact counts, blockers, reconsideration triggers, and nonclaims.

## Task 3: Enforce project validation and tracker wiring

- [ ] Register the test module in the correct test shard with a lexicographically sorted module list.
- [ ] Add the renderer check to `tools/plan_validation.py`, its catalog command group, and GitHub Actions catalog validation; document the command in `tools/README.md`.
- [ ] Add Issue #219 to the high-level backlog; do not rewrite the published v0.17 milestone record.
- [ ] Run focused tests and the renderer check; run crosswalk validation to confirm the catalog and mapping populations are unchanged.

## Task 4: Review and validate exact candidate

- [ ] Run the planner against `origin/main` and follow its publication route.
- [ ] Run focused tests, full unittest discovery, all affected validators, Mermaid record validation, qualified-review equivalence, and whole-branch `git diff --check` as required by repository policy.
- [ ] Have independent rights, specification/inventory, and security/overclaiming reviewers review the exact candidate SHA; rights review shall verify every proposed metadata and mapping field class, publication channel, and any written permission. Redispatch all reviews after any candidate change.
- [ ] Verify clean worktree, no `__pycache__`, no mapping snapshots, no registry entries, and no crosswalk catalog delta.

## Task 5: Publish and close the issue

- [ ] Commit without attribution trailers, fetch `origin/main`, and revalidate base/head freshness before opening a PR.
- [ ] Open a reviewable PR with the exact reviewed head SHA and validation evidence.
- [ ] Merge only after required checks pass, verify the merge commit on `main`, rerun the merge-SHA crosswalk check, then update local `main` and clean the temporary branch/worktree.
- [ ] Close Issue #219 only after the readiness package has landed and its acceptance criteria are satisfied.
