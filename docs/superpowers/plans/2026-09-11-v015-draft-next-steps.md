# ESAF v0.15-draft Next-Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land durable `v0.15-draft` milestone, backlog, and roadmap records plus ready-to-file issue bodies for post-v0.14 tracker hygiene, ISO/IEC 27001:2022 public-source readiness (default evidenced `HOLD`), bounded Phase 6 toolkit deepen, ESAF-1300/1400/1700 deepen to `0.3.0`, and publication gates.

**Architecture:** Keep `v0.14-draft` publication identity and Draft lifecycle states intact. Add a bounded `## v0.15-draft` milestone section mirroring `v0.14-draft`, a post-v0.14 backlog queue, a roadmap delivery sequence, and pinned issue-body fixtures in this plan for later GitHub filing. Do not author ISO/IEC 27001 readiness artifacts, deepen toolkit or companion manuals, reopen/close GitHub issues, or publish a tag in this planning change.

**Tech Stack:** Markdown project records, `unittest` release-metadata invariants.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-11-v015-draft-next-steps-design.md`
- Milestone identity: `v0.15-draft` (Working Draft tag name when later published)
- Sequence: tracker hygiene → ISO/IEC 27001 readiness → Phase 6 toolkit deepen and ESAF-1300/1400/1700 deepen → publication gates
- Issues `#55` / `#60` are not `v0.15-draft` blockers after hygiene
- ISO/IEC 27001 default exit is evidenced `HOLD`; no mapping records while `HOLD` or `NO_GO`
- Phase 6 toolkit deepen remains Draft and bound to ESAF-1500; not a complete library
- ESAF-1300/1400/1700 deepen remains Working Draft `0.3.0`; ESAF-1400 stays informative
- Do not redesign `v1.0` or open all of roadmap Phases 4–6
- Digests: compute each `PINNED_V015_ISSUE_*_BODY_SHA256` from the final fenced markdown body under the matching line-anchored `^## Task N:` heading via `sha256` of that fenced body

---

### Task 1: Lock planning invariants with failing tests

**Files:**
- Modify: `tests/test_release_metadata.py`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: existing helpers `read_repository_file`, `markdown_section`,
  `contains_normalized_phrase`, `fenced_markdown_in_task`, `sha256_text`,
  `milestone_section`
- Produces: constants `V015_NEXT_STEPS_PLAN`, `V015_READY_ISSUE_TASKS`, and
  five `PINNED_V015_ISSUE_*_BODY_SHA256` digests

- [ ] **Step 1: Add plan path, digest constants, and ready-issue table**

Near the existing `V014_NEXT_STEPS_PLAN` constants, add a plan-path constant
pointing at this file, five `PINNED_V015_ISSUE_*_BODY_SHA256` values, and a
`V015_READY_ISSUE_TASKS` tuple that mirrors `V014_READY_ISSUE_TASKS` with five
entries.

Use the exact Task 4–8 headings and titles already written later in this plan.
Required phrases per issue:

- Issue A: `reopen Issue #55`, `Issues #171`, `does not change normative`
- Issue B: `ISO/IEC 27001`, `HOLD`, `mapping records`
- Issue C: `workbook`, `evidence catalog`, `Draft`
- Issue D: `ESAF-1300`, `0.3.0`, `Draft`
- Issue E: `Issues #55 and #60 may remain open`, `Every \`v0.15-draft\` exit criterion`, `Working Draft`

Also update `test_hitrust_backlog_links_open_issue_60` so the expected phrase
includes `v0.15-draft`.

- [ ] **Step 2: Add failing milestone / backlog / roadmap / digest tests**

Add five tests on `ReleaseMetadataTests` that assert:

1. `project/MILESTONES.md` contains `## v0.15-draft` with headings
   `### Entry state`, `### Required workstreams`, `### Exit criteria`,
   `### Non-goals`, and the workstream / exit phrases listed in Task 2
   (`Tracker hygiene`, `ISO/IEC 27001`, `Phase 6 toolkit deepen`,
   `ESAF-1300`, `Release closure`, `Issues \`#171\`–\`#173\``,
   `Critical and Important`).
2. The `### Non-goals` subsection includes: closing Issue `#55`, substantive
   HITRUST mapping, PCI DSS `HOLD`, NIST AI RMF `HOLD`, ISO/IEC 42001 `HOLD`,
   NIST CSF `HOLD`, a second industry or jurisdiction profile, all roadmap
   crosswalks, all planned profiles, redesigning `v1.0`.
3. `project/BACKLOG.md` section `## Post-v0.14 scheduled queue` lists the five
   initiative titles from Task 2 and says they do not stop later engineering
   work.
4. `ROADMAP.md` section `## 0.15-draft delivery sequence` covers tracker
   hygiene, ISO/IEC 27001, Phase 6, ESAF-1300, issues 55/60, not exit
   criteria, evidenced `HOLD`, and Phases 4/5/6 long-term direction.
5. Each `V015_READY_ISSUE_TASKS` entry has `Title: \`...\`` in this plan, a
   fenced body matching the pinned digest via `fenced_markdown_in_task` +
   `sha256_text`, required phrases present, and no `closes issue 55` phrase.

- [ ] **Step 3: Run focused tests and confirm they fail before content lands**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v015 -v
```

Expected: FAIL (missing `## v0.15-draft` / queue / digests) when run before
Tasks 2–3 land; after Task 2, digest pin may still fail until Task 3.

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/test_release_metadata.py
git commit -m "test: require v0.15-draft planning invariants"
```

---

### Task 2: Update durable project records

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add `## v0.15-draft` to milestones**

Append after the `v0.14-draft` section (do not rewrite closed publication truth).

- [ ] **Step 2: Add `## Post-v0.14 scheduled queue` to the backlog**

Insert after `## Post-v0.13 scheduled queue`. List:

- Sync post-v0.14 tracker hygiene
- Complete ISO/IEC 27001:2022 public-source readiness and mapping go/no-go
- Deepen Phase 6 assessment toolkit Draft packs
- Deepen ESAF-1300/1400/1700 Working Drafts to 0.3.0
- Close the v0.15-draft publication gates

Also extend the HITRUST backlog line so it states the work does not block
through `v0.15-draft`.

- [ ] **Step 3: Add `## 0.15-draft delivery sequence` to the roadmap**

Insert before `## 0.14-draft delivery sequence`.

- [ ] **Step 4: Commit durable records**

```bash
git add project/MILESTONES.md project/BACKLOG.md ROADMAP.md
git commit -m "docs: define v0.15-draft milestone and post-v0.14 queue"
```

---

### Task 3: Pin issue-body digests, validate, and open the pull request

**Files:**
- Modify: `tests/test_release_metadata.py`

- [ ] **Step 1: Compute digests from this plan's fenced bodies**

Pinned digests for the bodies in this plan:

- Issue A: `054c611745d96aa90d3b9979a9c764aed5c30a032538cad1cd2c7edc784a65c6`
- Issue B: `d9d9e2960fb3d8387b64d7ce53ffbf283fcd7932ee29844737be2bfb46a84dcf`
- Issue C: `76044258ade8c10ce02341bd59fbc25dc90a7b90c4b7608db2f1aad3b3df50d5`
- Issue D: `82202492e545423d708f0d2b0dc34b9947a9a0b75f5cd6be9f328351b13c1a47`
- Issue E: `f07299eed8346109cef73d8000aa0a87b72d8d3af60aab2aa7941557e16360fb`

- [ ] **Step 2: Run focused tests and `git diff --check`**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v015 -v
git diff --check
```

- [ ] **Step 3: Confirm no `__pycache__` leftovers**

```bash
find . -type d -name '__pycache__' -print
```

- [ ] **Step 4: Commit, push, and open/update the draft PR**

```bash
git add tests/test_release_metadata.py \
  project/MILESTONES.md project/BACKLOG.md ROADMAP.md \
  docs/superpowers/plans/2026-09-11-v015-draft-next-steps.md \
  docs/superpowers/specs/2026-09-11-v015-draft-next-steps-design.md
git commit -m "docs: plan v0.15-draft next steps and pin issue bodies"
git push -u origin HEAD
```

Open or update a draft PR against `main` describing planning-only scope.
Do not create the five GitHub issues or edit GitHub tracker state in this
planning change; filing happens after the planning PR merges.

---

## Task 4: Ready-to-file Issue A - tracker hygiene

Title: `Sync post-v0.14 tracker hygiene`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Restore GitHub tracker state so it matches post-`v0.14-draft` repository truth
before `v0.15-draft` content work begins.

## Dependencies

Depends on the merged `v0.15-draft` planning records. Blocks filing or starting
content issues only insofar as milestone/`#55` truth must be corrected first.
Does not depend on Issue #60 content work.

## Deliverables

- Reopen Issue #55 if qualified UK mapping review remains outstanding, with a
  short comment stating owner-risk acceptance did not complete qualified review.
- Close or explicitly annotate Issues #171–#173 as historical completed
  `v0.14-draft` work, linking the published tag evidence where useful.
- Close GitHub milestone `v0.14-draft` when it has no open issues; open GitHub
  milestone `v0.15-draft`.
- Align GitHub milestone membership and `project/BACKLOG.md` wording with the
  durable records.
- Record the resulting open/closed matrix in the issue comments.

## Acceptance criteria

- Repository policy and GitHub agree on Issue #55 open/closed state.
- Issues #171–#173 are closed or clearly marked historical completed work.
- GitHub milestone `v0.14-draft` is closed when empty; milestone `v0.15-draft`
  exists.
- `project/BACKLOG.md` deferred-assurance and post-v0.14 queue text remain
  consistent with GitHub.
- No normative ESAF Markdown, schemas, or mappings change in this issue.

## Boundaries

This issue does not change normative ESAF content, complete qualified UK
review, close Issue #55 by owner-risk acceptance, clear HITRUST/PCI/NIST/
ISO/IEC 42001/NIST CSF blockers, open unauthorized mapping authorship, or claim
certification, compliance, equivalence, endorsement, or assurance. Tracker
hygiene does not change normative content.
```

---

## Task 5: Ready-to-file Issue B - ISO/IEC 27001 readiness

Title: `Complete ISO/IEC 27001:2022 public-source readiness and mapping go/no-go`

Labels: `crosswalk`, `priority:high`

```markdown
## Purpose

Complete ISO/IEC 27001:2022 public-source readiness and a mapping go/no-go
decision for ESAF without creating unauthorized mapping records.

## Dependencies

Depends on merged `v0.15-draft` planning records and tracker hygiene. May
overlap Phase 6 toolkit deepen and ESAF-1300/1400/1700 deepen. Must finish
before publication gates.

## Deliverables

- Pin the official ISO/IEC 27001:2022 source identity (title, edition, publisher,
  locator) and checksums where obtainable.
- Record the publication-rights boundary and provision-inventory feasibility
  without reproducing restricted ISO text.
- Assess named mapper and independent qualified-reviewer availability.
- Produce a mechanical readiness matrix and an evidenced `GO` / `HOLD` /
  `NO_GO` decision package under `docs/superpowers/` plus landing page
  `crosswalks/iso-iec-27001.md`.
- Default acceptable exit is evidenced `HOLD` when people, rights, or
  source-access gates remain blocked.

## Acceptance criteria

- ISO/IEC 27001 readiness decision is recorded as `GO`, `HOLD`, or `NO_GO`
  with blockers, owners, reconsideration triggers, re-entry tests, and
  nonclaims.
- While the decision is `HOLD` or `NO_GO`, ISO/IEC 27001 mapping records,
  snapshots, lifecycle events, registry entries, and catalog increments remain
  absent (`0` mapping artifacts for the scheme).
- Focused readiness tests and renderers pass; whole-branch release-metadata
  invariants remain green.
- No certification, compliance, equivalence, endorsement, or assurance claim.

## Boundaries

This issue does not author ISO/IEC 27001 mapping records under `HOLD` or
`NO_GO`, clear prior NIST AI RMF / ISO/IEC 42001 / NIST CSF / PCI DSS HOLDs,
close Issue #55, perform HITRUST work, or establish certification. Clone the
ISO/IEC 42001 / PCI-shaped package; do not invent a public provision inventory
when rights forbid it.
```

---

## Task 6: Ready-to-file Issue C - Phase 6 toolkit deepen

Title: `Deepen Phase 6 assessment toolkit Draft packs`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Complete a bounded second Working Draft deepen of the Phase 6 assessment
toolkit packs beyond the `v0.11-draft` deepen, while remaining Draft and bound
to ESAF-1500 contracts.

## Dependencies

Depends on merged `v0.15-draft` planning records and tracker hygiene. May
overlap ISO/IEC 27001 readiness and ESAF-1300/1400/1700 deepen. Must finish
before publication gates.

## Deliverables

- Deepen the assessment workbook under `assessment/workbook/` with at least one
  additional operator-facing vignette or worked example beyond the existing
  Draft pack.
- Deepen the evidence catalog under `assessment/evidence-catalog/` with
  additional filled examples or quality notes while preserving ESAF-1500
  evidence contracts.
- Deepen the audit checklist under `assessment/audit-checklist/` with
  additional sampling or result examples without inventing parallel result
  semantics.
- Deepen governance templates under `templates/` with additional informative
  examples linked from ESAF-1300 / ESAF-1400 where appropriate.
- Keep all packs Draft; update indexes/READMEs for discoverability; add or
  extend focused tests.

## Acceptance criteria

- Workbook, evidence catalog, audit checklist, and governance template packs
  each show a bounded second deepen with Draft evidence.
- Packs remain bound to ESAF-1500 shared contracts; no schema-breaking contract
  changes; no certification claims.
- Focused assessment/toolkit tests pass; Critical and Important findings are
  resolved.
- The deepen does not claim a complete Phase 6 assessment library.

## Boundaries

This issue does not redesign `v1.0`, invent certification or accreditation
requirements, advance lifecycle states, break ESAF-1500 schema contracts, open
a second profile, clear readiness HOLDs, or claim compliance, equivalence,
endorsement, or assurance.
```

---

## Task 7: Ready-to-file Issue D - ESAF-1300/1400/1700 deepen

Title: `Deepen ESAF-1300/1400/1700 Working Drafts to 0.3.0`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Complete a bounded Working Draft deepen of ESAF-1300, ESAF-1400, and ESAF-1700
from `0.2.0` to `0.3.0`.

## Dependencies

Depends on merged `v0.15-draft` planning records and tracker hygiene. May
overlap ISO/IEC 27001 readiness and Phase 6 toolkit deepen. Must finish before
publication gates.

## Deliverables

- Deepen `governance/ESAF-1300.md` to Working Draft `0.3.0` with revision
  history; any clarifying `shall`/`should` shall cite a parent ESAF-1000 /
  GOV / related obligation that already establishes the outcome.
- Deepen `implementation/ESAF-1400.md` to Working Draft `0.3.0` while remaining
  informative; add no local `shall`.
- Deepen `data-model/ESAF-1700.md` to Working Draft `0.3.0` with revision
  history; clarifying normative language shall cite parent ESAF-1000 / 1100 /
  1500 obligations and shall not invent new assessment-record identifier
  prefixes.
- Extend discoverable example packs under `examples/esaf-1300/`,
  `examples/esaf-1400/`, and `examples/esaf-1700/` as needed (informative only).
- Extend companion breadth tests for the `0.3.0` deepen invariants.

## Acceptance criteria

- ESAF-1300, ESAF-1400, and ESAF-1700 each report Working Draft `0.3.0` with
  revision-history evidence and remain Draft.
- ESAF-1400 remains informative with no local `shall`.
- No new control identifiers, procedures, or metrics are introduced.
- Focused companion tests pass; Critical and Important findings are resolved.

## Boundaries

This issue does not redesign `v1.0`, invent certification requirements, advance
lifecycle states, reopen ESAF-1000/1100/1200/1500 deepen, author crosswalk
mapping records, or claim compliance, equivalence, endorsement, or assurance.
```

---

## Task 8: Ready-to-file Issue E - v0.15-draft publication gates

Title: `Close the v0.15-draft publication gates`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Close the ordinary `v0.15-draft` release gates on one exact release candidate
after tracker hygiene, ISO/IEC 27001 readiness, Phase 6 toolkit deepen, and
ESAF-1300/1400/1700 deepen are complete.

## Dependencies

Depends on completion of:

- Sync post-v0.14 tracker hygiene;
- Complete ISO/IEC 27001:2022 public-source readiness and mapping go/no-go;
- Deepen Phase 6 assessment toolkit Draft packs; and
- Deepen ESAF-1300/1400/1700 Working Drafts to 0.3.0.

Issues #55 and #60 may remain open. They are not `v0.15-draft` exit criteria.

## Deliverables

- Exact-candidate technical, editorial, and governance reviews.
- Full test suite, control, architecture, assessment, profile, crosswalk, link,
  release, working-tree, and applicable Mermaid-rendering gates.
- Synchronized README, VERSION, changelog, roadmap, release plan, backlog,
  milestones, and readiness record.
- Annotated tag `v0.15-draft` and consolidated publication evidence bound to
  the exact candidate SHA.

## Acceptance criteria

- Every `v0.15-draft` exit criterion in `project/MILESTONES.md` is satisfied.
- Critical and Important findings are resolved.
- Post-merge validation passes before any immutable tag or publication
  statement is created.
- Publication remains a Working Draft.

## Boundaries

Publication remains a Working Draft. It does not complete qualified UK mapping
review, clear HITRUST / PCI DSS / NIST AI RMF / ISO/IEC 42001 / NIST CSF
blockers, authorize ISO/IEC 27001 mapping authorship under `HOLD` or `NO_GO`,
approve Draft artifact lifecycle transitions without their own evidence, or
establish certification, compliance, equivalence, endorsement, external-scheme
approval, assurance, or production readiness.
```
