# ESAF v0.9-rc1 Next-Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land durable `v0.9-rc1` milestone, backlog, and roadmap records plus ready-to-file issue bodies for post-beta work that currently has no open GitHub issue.

**Architecture:** Keep `v0.5-beta` publication truth and Issues `#55` / `#60` intact. Add a bounded `## v0.9-rc1` milestone section mirroring the `v0.5-beta` structure, a post-beta backlog queue, a roadmap delivery sequence, and pinned issue-body fixtures in this plan for later GitHub filing.

**Tech Stack:** Markdown project records, `unittest` release-metadata invariants.

---

### Task 1: Lock planning invariants with failing tests

**Files:**
- Modify: `tests/test_release_metadata.py`

- [ ] **Step 1: Add tests requiring `## v0.9-rc1` workstreams, exit criteria, non-goals, backlog queue, roadmap sequence, and pinned issue bodies**

- [ ] **Step 2: Run focused tests and confirm they fail before content lands**

---

### Task 2: Update durable project records

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add `## v0.9-rc1` with Entry state, Required workstreams, Exit criteria, and Non-goals from the design**

- [ ] **Step 2: Add `## Post-beta scheduled queue` to the backlog without disturbing deferred, HITRUST, or completed sections**

- [ ] **Step 3: Add `## 0.9-rc1 delivery sequence` to the roadmap after the 0.5-beta sequence**

---

### Task 3: Validate, commit, and open the pull request

- [ ] **Step 1: Run focused release-metadata tests and `git diff --check`**

- [ ] **Step 2: Commit and push the branch**

- [ ] **Step 3: Open a draft PR against `main`**

---

## Task 4: Ready-to-file Issue A - harness closeout

Title: `Close validation-harness Phase 2 performance target`

Labels: `tooling`, `priority:high`

```markdown
## Purpose

Complete the remaining validation-harness efficiency Phase 2 closeout: the
mapping-review bundle mutation-matrix hot path and the hosted full-suite
performance measurement required by the sealed Phase 2 acceptance criteria.

## Dependencies

Depends on the merged `v0.9-rc1` planning records. May proceed in parallel with
ESAF-1300 / ESAF-1400 / ESAF-1700 authorship. Does not depend on Issues #55 or
#60.

## Deliverables

- Land the bundle mutation-matrix hot-path increment with equivalence proof.
- Retain representative end-to-end coverage for the bundle validator.
- Record three successful hosted full-suite runs against the sealed Phase 2
  baseline and decide whether the >=40 percent reduction target is met.
- Update durable harness docs only as needed to close or explicitly defer the
  target with evidence.

## Acceptance criteria

- Equivalence and population proofs pass for the bundle hot path.
- Hosted measurement evidence is recorded for three successful runs.
- Full discovery, shards, standalone validators, Mermaid, and whole-branch
  checks pass on the exact candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue does not change normative ESAF content, close Issue #55, advance
Draft mappings, or claim certification, compliance, equivalence, endorsement,
or assurance.
```

---

## Task 5: Ready-to-file Issue B - ESAF-1300

Title: `Author ESAF-1300 Governance Manual Working Draft`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Author the first Working Draft of ESAF-1300 covering decision rights, lifecycle
gates, exception handling, and RACI materials sufficient for editorial and link
validation.

## Dependencies

Depends on the merged `v0.9-rc1` planning records. May proceed in parallel with
ESAF-1400 and ESAF-1700.

## Deliverables

- Replace the governance stub with a coherent Working Draft.
- Link the draft from applicable indexes and README surfaces.
- Keep requirements aligned to ESAF-1000 without inventing a parallel control
  catalog.

## Acceptance criteria

- ESAF-1300 is internally consistent, linked, and free of drafting placeholders.
- Focused and affected validators pass on the exact candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue publishes a Working Draft only. It does not approve certification,
compliance, equivalence, endorsement, assurance, or production readiness.
```

---

## Task 6: Ready-to-file Issue C - ESAF-1400

Title: `Author ESAF-1400 Implementation Guide Working Draft`

Labels: `documentation`, `priority:high`

```markdown
## Purpose

Author the first Working Draft of ESAF-1400 with practical, non-normative
implementation guidance and adoption roadmaps that reference existing ESAF
controls and architectures.

## Dependencies

Depends on the merged `v0.9-rc1` planning records. May proceed in parallel with
ESAF-1300 and ESAF-1700.

## Deliverables

- Replace the implementation stub with a coherent Working Draft.
- Provide adoption guidance that does not create competing normative
  requirements.
- Link the draft from applicable indexes and README surfaces.

## Acceptance criteria

- ESAF-1400 is internally consistent, linked, and free of drafting placeholders.
- Focused and affected validators pass on the exact candidate.
- Critical and Important findings are resolved.

## Boundaries

ESAF-1400 remains non-normative guidance. This issue does not approve
certification, compliance, equivalence, endorsement, assurance, or production
readiness.
```

---

## Task 7: Ready-to-file Issue D - ESAF-1700

Title: `Author ESAF-1700 Enterprise AI Data Model Working Draft`

Labels: `documentation`, `priority:high`

```markdown
## Purpose

Author the first Working Draft of ESAF-1700 defining canonical entities,
attributes, relationships, and exchange guidance for enterprise AI governance.

## Dependencies

Depends on the merged `v0.9-rc1` planning records and shall align exchange
fields to ESAF-1500 assessment contracts where applicable. May proceed in
parallel with ESAF-1300 and ESAF-1400.

## Deliverables

- Replace the data-model stub with a coherent Working Draft.
- Define canonical entities and relationships without claiming a runtime
  product schema mandate.
- Link the draft from applicable indexes and README surfaces.

## Acceptance criteria

- ESAF-1700 is internally consistent, linked, and free of drafting placeholders.
- Focused and affected validators pass on the exact candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue publishes a Working Draft only. It does not approve certification,
compliance, equivalence, endorsement, assurance, or production readiness.
```

---

## Task 8: Ready-to-file Issue E - NIST AI RMF readiness

Title: `Complete NIST AI RMF public-source readiness and mapping go/no-go`

Labels: `crosswalk`, `priority:high`

```markdown
## Purpose

Determine whether ESAF can begin a Draft NIST AI RMF mapping without exceeding
public-source, publication-rights, or review boundaries.

## Dependencies

Depends on the merged `v0.9-rc1` planning records. May proceed in parallel with
ESAF-1300 / ESAF-1400 / ESAF-1700 and the harness closeout. Does not depend on
Issues #55 or #60. No mapping records may be published before the go/no-go
decision.

## Deliverables

- Pin the exact public NIST AI RMF version and official sources.
- Define the public-content and publication-rights boundary.
- Assess provision-inventory feasibility without reproducing restricted text.
- Identify mapper and qualified-review availability.
- Record a `GO`, `HOLD`, or `NO_GO` readiness decision and reconsideration
  triggers.

## Acceptance criteria

- Version, access, rights, inventory feasibility, and review prerequisites are
  evidenced.
- Any permitted public artifact is independently reviewed for rights and
  overclaiming.
- A blocked prerequisite produces a `HOLD` or `NO_GO` record rather than an
  inferred mapping.
- Affected validators pass on the exact candidate.

## Boundaries

This issue does not authorize substantive mapping records beyond an approved
`GO` scope, does not close Issue #55, and makes no NIST AI RMF compliance,
certification, equivalence, endorsement, or assurance claim.
```

---

## Task 9: Ready-to-file Issue F - v0.9-rc1 publication gates

Title: `Close the v0.9-rc1 publication gates`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Close the ordinary `v0.9-rc1` release gates on one exact release candidate after
the required workstreams are complete or formally dispositioned.

## Dependencies

Depends on completion or evidenced disposition of:

- validation-harness Phase 2 closeout;
- ESAF-1300, ESAF-1400, and ESAF-1700 Working Drafts; and
- the NIST AI RMF public-source readiness decision.

Issues #55 and #60 may remain open. They are not `v0.9-rc1` exit criteria.

## Deliverables

- Exact-candidate technical, editorial, and governance reviews.
- Full test suite, control, architecture, assessment, profile, crosswalk, link,
  release, working-tree, and applicable Mermaid-rendering gates.
- Synchronized README, VERSION, changelog, roadmap, release plan, backlog,
  milestones, and readiness record.
- Consolidated publication evidence bound to the exact candidate SHA.

## Acceptance criteria

- Every `v0.9-rc1` exit criterion in `project/MILESTONES.md` is satisfied.
- Critical and Important findings are resolved.
- Post-merge validation passes before any immutable tag or publication
  statement is created.

## Boundaries

Publication remains a Working Draft release candidate. It does not complete
qualified UK mapping review, clear HITRUST or PCI DSS blockers, approve Draft
artifact lifecycle transitions without their own evidence, or establish
certification, compliance, equivalence, endorsement, external-scheme approval,
assurance, or production readiness.
```
