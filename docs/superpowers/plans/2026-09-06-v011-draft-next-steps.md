# ESAF v0.11-draft Next-Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land durable `v0.11-draft` milestone, backlog, and roadmap records plus ready-to-file issue bodies for post-v0.10 tracker hygiene, Phase 6 toolkit deepen, NIST AI RMF readiness re-entry (default refreshed `HOLD`), and publication gates.

**Architecture:** Keep `v0.10-draft` publication identity and Draft lifecycle states intact. Add a bounded `## v0.11-draft` milestone section mirroring `v0.10-draft`, a post-v0.10 backlog queue, a roadmap delivery sequence, and pinned issue-body fixtures in this plan for later GitHub filing. Do not deepen toolkit content, refresh NIST package artifacts, reopen/close GitHub issues, or publish a tag in this planning change.

**Tech Stack:** Markdown project records, `unittest` release-metadata invariants.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-06-v011-draft-next-steps-design.md`
- Milestone identity: `v0.11-draft` (Working Draft tag name when later published)
- Sequence: tracker hygiene → toolkit deepen (parallel) → NIST readiness re-entry → publication gates
- Issues `#55` / `#60` are not `v0.11-draft` blockers after hygiene
- Toolkit deepen remains Draft; no parallel ESAF-1500 semantics; no certification claims
- NIST re-entry default exit is refreshed evidenced `HOLD`; no mapping records while `HOLD`
- Do not redesign `v1.0` or open all of roadmap Phases 4–6

---

### Task 1: Lock planning invariants with failing tests

**Files:**
- Modify: `tests/test_release_metadata.py`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: existing helpers `read_repository_file`, `markdown_section`,
  `contains_normalized_phrase`, `fenced_markdown_in_task`, `sha256_text`,
  `milestone_section`
- Produces: constants `V011_NEXT_STEPS_PLAN`, `V011_READY_ISSUE_TASKS`, and
  seven `PINNED_V011_ISSUE_*_BODY_SHA256` digests (compute after bodies are final)

- [ ] **Step 1: Add plan path, digest constants, and ready-issue table**

Near the existing `V010_NEXT_STEPS_PLAN` constants, add a plan-path constant
pointing at this file, seven `PINNED_V011_ISSUE_*_BODY_SHA256` placeholders, and
a `V011_READY_ISSUE_TASKS` tuple that mirrors `V010_READY_ISSUE_TASKS`.

Use the exact Task 4–10 headings and titles already written later in this plan
(do not paste those headings into earlier fenced samples in a way that creates
duplicate first matches). Required phrases per issue:

- Issue A: `reopen Issue #55`, `Issues #114`, `does not change normative`
- Issue B: `ESAF-1500`, `worked fictional`, `Draft`
- Issue C: `evidence catalog`, `ESAF-1500 evidence contract`, `Draft`
- Issue D: `audit checklist`, `assessment-result`, `Draft`
- Issue E: `templates/`, `ESAF-1300`, `ESAF-1400`
- Issue F: `refreshed evidenced`, `HOLD`, `mapping records`
- Issue G: `Issues #55 and #60 may remain open`, `Every \`v0.11-draft\` exit criterion`, `Working Draft`

Also update `test_hitrust_backlog_links_open_issue_60` so the expected phrase
includes `v0.11-draft`.

- [ ] **Step 2: Add failing milestone / backlog / roadmap / digest tests**

Add five tests on `ReleaseMetadataTests` that assert:

1. `project/MILESTONES.md` contains `## v0.11-draft` with headings
   `### Entry state`, `### Required workstreams`, `### Exit criteria`,
   `### Non-goals`, and the workstream / exit phrases listed in Task 2.
2. The `### Non-goals` subsection includes: closing Issue `#55`, substantive
   HITRUST mapping, PCI DSS `HOLD`, NIST AI RMF `HOLD`, all roadmap
   crosswalks, all planned profiles, redesigning `v1.0`.
3. `project/BACKLOG.md` section `## Post-v0.10 scheduled queue` lists the seven
   initiative titles from Task 2 and says they do not stop later engineering
   work.
4. `ROADMAP.md` section `## 0.11-draft delivery sequence` covers tracker
   hygiene, toolkit deepen, NIST readiness re-entry, issues 55/60, not exit
   criteria, Phase 6, and refreshed `HOLD`.
5. Each `V011_READY_ISSUE_TASKS` entry has `Title: \`...\`` in this plan, a
   fenced body matching the pinned digest via `fenced_markdown_in_task` +
   `sha256_text`, required phrases present, and no `closes issue 55` phrase.

Mirror the structure of
`test_planned_v010_issue_bodies_preserve_boundaries_and_digests`.

- [ ] **Step 3: Run focused tests and confirm they fail before content lands**

Run the new tests with:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v011 -v
```

Expected: FAIL (missing `## v0.11-draft` / queue / digests).

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/test_release_metadata.py
git commit -m "test: require v0.11-draft planning invariants"
```

---

### Task 2: Update durable project records

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add `## v0.11-draft` to milestones**

Append after the `v0.10-draft` section (do not rewrite closed publication truth):

```markdown
## v0.11-draft

### Entry state

- `v0.10-draft` is published and its publication evidence is closed.
- ESAF-1300, ESAF-1400, and ESAF-1700 remain at least at Working Draft `0.2.0`
  depth with discoverable example packs.
- ESAF-1500 foundation schemas, examples, and the four Phase 6 Draft starters
  remain Draft and authoritative for shared assessment semantics.
- NIST AI RMF readiness remains evidenced `HOLD`; mapping artifact count remains
  `0`.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.11-draft` blockers.
- ESAF-1000, ESAF-1100, ESAF-1200, ESAF-1600 method artifacts, the UK pilot
  profile, and the three UK mapping snapshots remain Draft.

### Required workstreams

1. **Tracker hygiene.** ESAF shall reopen Issue `#55` if qualified UK mapping
   review remains outstanding, close or explicitly annotate Issues `#114`–`#119`
   as historical completed `v0.10-draft` work, and align backlog and GitHub
   milestone state with published truth. This workstream does not change
   normative content.
2. **Assessment workbook Draft deepen.** ESAF shall add one worked fictional
   engagement with scope narrative and a filled worksheet trio bound to
   ESAF-1500 schemas and ESAF-1100 procedures, keeping pack status Draft and
   worksheets schema-valid.
3. **Evidence catalog Draft deepen.** ESAF shall add short per-type quality
   notes and a small set of fictional filled evidence records keyed to catalog
   types, remaining profile-neutral and bound to the ESAF-1500 evidence
   contract.
4. **Audit checklist Draft deepen.** ESAF shall add one small sampling vignette
   with procedure IDs, methods, evidence references, and determinations against
   the shared assessment-result vocabulary, without authoring a full
   control-family library.
5. **Governance templates Draft deepen.** ESAF shall add one filled informative
   instance per template class under `examples/` or an adjacent informative
   path, linked from `templates/` and ESAF-1300 / ESAF-1400 without adding new
   normative `shall` requirements.
6. **NIST AI RMF readiness re-entry.** ESAF shall refresh the NIST AI RMF
   readiness package. The default acceptable exit is a refreshed evidenced
   `HOLD` that restates blockers, owners, reconsideration triggers, re-entry
   tests, and nonclaims. A matrix-derived `GO` is allowed only when named
   mapper and independent reviewer evidence fully clears the people gate.
   While the decision remains `HOLD`, ESAF shall not create NIST mapping
   records or catalog increments.
7. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.11-draft` candidate, publish annotated tag `v0.11-draft`, and synchronize
   Working Draft status surfaces.

### Exit criteria

`v0.11-draft` is complete only when:

- tracker hygiene is complete: Issues `#114`–`#119` are closed or explicitly
  annotated as historical, and Issue `#55` is open if and only if qualified UK
  review remains outstanding;
- each of the four toolkit packs has a Draft deepen deliverable linked from
  applicable indexes and still reuses ESAF-1500 shared semantics without
  inventing parallel maturity, evidence, or result contracts;
- NIST AI RMF readiness re-entry is recorded as either a refreshed evidenced
  `HOLD` or a matrix-derived `GO` with zero blockers; if `HOLD`, NIST mapping
  artifact count remains `0` and generated crosswalk catalog counts are
  unchanged by this workstream;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.11-draft` is published and Working Draft surfaces are
  synchronized.

### Non-goals

`v0.11-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping;
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` when named mapper and independent reviewers
  remain unavailable;
- authoring NIST AI RMF mapping records, snapshots, or catalog entries;
- a complete Phase 6 workbook, evidence library, audit-checklist library, or
  template library;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.
```

- [ ] **Step 2: Add `## Post-v0.10 scheduled queue` to the backlog**

Insert after `## Post-rc1 scheduled queue` (keep that section as historical
`v0.10-draft` context). New section:

```markdown
## Post-v0.10 scheduled queue

These initiatives are required for `v0.11-draft` and shall be tracked in GitHub
Issues under milestone `v0.11-draft`. Deferred mapping assurance and HITRUST
readiness remain tracked separately and do not stop later engineering work.

- Sync post-v0.10 tracker hygiene
- Deepen assessment workbook Draft pack
- Deepen evidence catalog Draft pack
- Deepen audit checklist Draft pack
- Deepen governance templates Draft pack
- Refresh NIST AI RMF readiness package
- Close the v0.11-draft publication gates
```

Also extend the HITRUST backlog line so it states the work does not block
`v0.5-beta`, `v0.9-rc1`, `v0.10-draft`, or `v0.11-draft`.

- [ ] **Step 3: Add `## 0.11-draft delivery sequence` to the roadmap**

Insert before `## 0.10-draft delivery sequence`:

```markdown
## 0.11-draft delivery sequence

`v0.11-draft` follows tracker hygiene, then the Phase 6 assessment-toolkit
deepen (assessment workbook, evidence catalog, audit checklist, and
governance templates), then NIST AI RMF readiness re-entry, then ordinary
publication gates on the exact candidate. Deferred mapping assurance remains
tracked through issue 55 and does not stop later engineering work. HITRUST
readiness remains separately gated through issue 60. Issues 55 and 60 are not
`v0.11-draft` exit criteria. NIST readiness re-entry may exit as a refreshed
evidenced `HOLD` when named mapper and independent reviewers remain
unavailable; while `HOLD`, no NIST mapping records are authored. Publication
does not change any control, architecture, profile, mapping-set, or
mapping-record lifecycle state. Phases 4 and 5 remain long-term direction.
Phase 6 remains long-term direction except for the bounded deepen required by
this milestone.
```

- [ ] **Step 4: Run the Task 1 tests again**

Expected: milestone/backlog/roadmap tests PASS; digest test still FAIL until
digests are pinned from the fenced bodies already in this plan (Tasks 4–10).

- [ ] **Step 5: Commit durable records**

```bash
git add project/MILESTONES.md project/BACKLOG.md ROADMAP.md
git commit -m "docs: define v0.11-draft milestone and post-v0.10 queue"
```

---

### Task 3: Pin issue-body digests, validate, and open the pull request

**Files:**
- Modify: `tests/test_release_metadata.py`

- [ ] **Step 1: Compute digests from this plan’s fenced bodies**

```bash
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
from pathlib import Path
import hashlib, re
plan = Path("docs/superpowers/plans/2026-09-06-v011-draft-next-steps.md").read_text()
for heading in [
    "## Task 4: Ready-to-file Issue A - tracker hygiene",
    "## Task 5: Ready-to-file Issue B - assessment workbook deepen",
    "## Task 6: Ready-to-file Issue C - evidence catalog deepen",
    "## Task 7: Ready-to-file Issue D - audit checklist deepen",
    "## Task 8: Ready-to-file Issue E - governance templates deepen",
    "## Task 9: Ready-to-file Issue F - NIST AI RMF readiness re-entry",
    "## Task 10: Ready-to-file Issue G - v0.11-draft publication gates",
]:
    start = plan.rfind(heading)
    nxt = re.search(r"^## Task \d+:", plan[start+1:], re.M)
    end = start + 1 + nxt.start() if nxt else len(plan)
    task = plan[start:end]
    fence_start = task.index("```markdown\n") + len("```markdown\n")
    fence_end = task.index("\n```", fence_start)
    body = task[fence_start:fence_end]
    print(heading.split(" - ",1)[1], hashlib.sha256(body.encode()).hexdigest())
PY
```

Replace each placeholder digest constant with the printed digest.

- [ ] **Step 2: Run focused tests and `git diff --check`**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest \
  tests.test_release_metadata.ReleaseMetadataTests.test_v011_draft_has_bounded_workstreams_and_exit_criteria \
  tests.test_release_metadata.ReleaseMetadataTests.test_v011_draft_preserves_bounded_non_goals \
  tests.test_release_metadata.ReleaseMetadataTests.test_backlog_records_post_v010_v011_draft_initiatives \
  tests.test_release_metadata.ReleaseMetadataTests.test_roadmap_records_v011_draft_delivery_sequence \
  tests.test_release_metadata.ReleaseMetadataTests.test_planned_v011_issue_bodies_preserve_boundaries_and_digests \
  tests.test_release_metadata.ReleaseMetadataTests.test_hitrust_backlog_links_open_issue_60 \
  -v
git diff --check
```

Expected: all PASS; no whitespace errors.

- [ ] **Step 3: Confirm no `__pycache__` leftovers**

```bash
find . -type d -name '__pycache__' -print
```

Expected: empty (or only outside the repo). Remove any created under the tree.

- [ ] **Step 4: Commit, push, and open/update the draft PR**

```bash
git add tests/test_release_metadata.py \
  project/MILESTONES.md project/BACKLOG.md ROADMAP.md \
  docs/superpowers/plans/2026-09-06-v011-draft-next-steps.md \
  docs/superpowers/specs/2026-09-06-v011-draft-next-steps-design.md
git commit -m "docs: plan v0.11-draft next steps and pin issue bodies"
git push -u origin HEAD
```

Open or update a draft PR against `main` describing planning-only scope.

---

## Task 4: Ready-to-file Issue A - tracker hygiene

Title: `Sync post-v0.10 tracker hygiene`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Restore GitHub tracker state so it matches post-`v0.10-draft` repository truth
before `v0.11-draft` content work begins.

## Dependencies

Depends on the merged `v0.11-draft` planning records. Blocks filing or starting
the toolkit and NIST issues only insofar as milestone/`#55` truth must be
corrected first. Does not depend on Issues #60 content work.

## Deliverables

- Reopen Issue #55 if qualified UK mapping review remains outstanding, with a
  short comment stating owner-risk acceptance did not complete qualified review.
- Close or explicitly annotate Issues #114–#119 as historical completed
  `v0.10-draft` work, linking the published tag evidence where useful.
- Align GitHub milestone `v0.10-draft` / `v0.11-draft` membership and
  `project/BACKLOG.md` wording with the durable records.
- Record the resulting open/closed matrix in the issue comments.

## Acceptance criteria

- Repository policy and GitHub agree on Issue #55 open/closed state.
- Issues #114–#119 are closed or clearly marked historical completed work.
- `project/BACKLOG.md` deferred-assurance and post-v0.10 queue text remain
  consistent with GitHub.
- No normative ESAF Markdown, schemas, or mappings change in this issue.

## Boundaries

This issue does not change normative ESAF content, complete qualified UK
review, close Issue #55 by owner-risk acceptance, clear HITRUST/PCI/NIST
blockers, or claim certification, compliance, equivalence, endorsement, or
assurance.
```

---

## Task 5: Ready-to-file Issue B - assessment workbook deepen

Title: `Deepen assessment workbook Draft pack`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Deepen the Draft assessment workbook starter with one worked fictional
engagement operators can follow while remaining bound to ESAF-1500 shared
contracts and ESAF-1100 control assessment procedures.

## Dependencies

Depends on merged `v0.11-draft` planning records and completion (or explicit
waiver note) of tracker hygiene. May proceed in parallel with the evidence
catalog, audit checklist, governance-template, and NIST readiness issues.

## Deliverables

- One worked fictional engagement narrative under `assessment/` or `examples/`
  covering scope, evidence references, procedure steps, findings, and result
  recording.
- A filled worksheet trio that remains schema-valid against ESAF-1500 evidence /
  assessment-result / maturity contracts.
- Links from applicable assessment indexes and README surfaces.
- Pack status remains Draft.

## Acceptance criteria

- Workbook deepen is internally consistent, Draft-labeled, and free of
  certification claims.
- No parallel evidence, result, or maturity semantics are introduced.
- Focused assessment validators and affected link checks pass on the exact
  candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue publishes a Draft deepen only. It does not approve certification,
compliance, equivalence, endorsement, assurance, or production readiness, and
it does not advance control or mapping lifecycle states.
```

---

## Task 6: Ready-to-file Issue C - evidence catalog deepen

Title: `Deepen evidence catalog Draft pack`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Deepen the Draft evidence catalog with per-type quality notes and a small set
of fictional filled evidence records, aligned to the ESAF-1500 evidence
contract.

## Dependencies

Depends on merged `v0.11-draft` planning records and tracker hygiene. May
proceed in parallel with the workbook, audit checklist, governance-template,
and NIST readiness issues.

## Deliverables

- Short per-type good-enough versus common-failure notes for catalog types.
- A small set of fictional filled evidence records keyed to catalog types and
  bound to the ESAF-1500 evidence contract.
- Keep catalog entries profile- and framework-neutral unless explicitly marked
  as examples.
- Link the deepen from applicable assessment indexes.

## Acceptance criteria

- Catalog deepen is Draft-labeled and reuses ESAF-1500 evidence semantics.
- No parallel evidence contract is introduced.
- Focused assessment validators and affected link checks pass on the exact
  candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue does not create framework-specific mapping evidence claims, close
Issue #55, or establish certification, compliance, equivalence, endorsement,
or assurance.
```

---

## Task 7: Ready-to-file Issue D - audit checklist deepen

Title: `Deepen audit checklist Draft pack`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Deepen the Draft audit checklist with one small sampling vignette against the
shared ESAF-1500 assessment-result contract.

## Dependencies

Depends on merged `v0.11-draft` planning records and tracker hygiene. May
proceed in parallel with the workbook, evidence catalog, governance-template,
and NIST readiness issues.

## Deliverables

- One small sampling vignette (approximately two to three controls) covering
  sampling intent, procedure references, evidence pointers, determination
  capture, and limitation notes.
- Bind determinations to the shared assessment-result vocabulary.
- Link the deepen from applicable assessment indexes.

## Acceptance criteria

- Checklist deepen is Draft-labeled and consistent with ESAF-1500 result
  semantics.
- No parallel determination vocabulary is introduced.
- Focused assessment validators and affected link checks pass on the exact
  candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue does not create a certification audit program, complete qualified
mapping review, or claim compliance, equivalence, endorsement, or assurance.
```

---

## Task 8: Ready-to-file Issue E - governance templates deepen

Title: `Deepen governance templates Draft pack`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Deepen the Draft governance template starter pack under `templates/` with one
filled informative instance per class (risk, exception, decision, retirement),
linked from ESAF-1300 and ESAF-1400 without adding new normative requirements.

## Dependencies

Depends on merged `v0.11-draft` planning records and tracker hygiene. May
proceed in parallel with the workbook, evidence catalog, audit-checklist, and
NIST readiness issues.

## Deliverables

- One filled informative instance per template class under `examples/` or an
  adjacent informative path.
- Link filled instances from ESAF-1300 / ESAF-1400 and `templates/` indexes.
- Keep templates non-normative; do not invent requirements beyond existing
  publications.

## Acceptance criteria

- Template deepen is Draft-labeled and discoverable from governance and
  implementation indexes.
- No new normative `shall` requirements are introduced in template files.
- Affected link checks and release-metadata expectations pass on the exact
  candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue does not amend ESAF-1300 / ESAF-1400 normative scope, approve
lifecycle transitions, or claim certification, compliance, equivalence,
endorsement, or assurance.
```

---

## Task 9: Ready-to-file Issue F - NIST AI RMF readiness re-entry

Title: `Refresh NIST AI RMF readiness package`

Labels: `crosswalk`, `priority:high`

```markdown
## Purpose

Refresh the NIST AI RMF readiness package after `v0.10-draft`. The default
acceptable exit is a refreshed evidenced `HOLD` because named mapper and
independent reviewers are not available. A matrix-derived `GO` is permitted
only if complete people evidence appears before publication.

## Dependencies

Depends on merged `v0.11-draft` planning records and tracker hygiene. May
overlap toolkit deepen issues, but must finish before publication gates.

## Deliverables

- Refresh oracle, rights boundary, inventory, matrix, generated decision,
  landing page, and issue traceability as applicable.
- If people evidence remains unavailable, record a refreshed evidenced `HOLD`
  that restates blockers (including `NIST-AI-RMF-READINESS-B001`), owners,
  reconsideration triggers, re-entry tests, and nonclaims.
- If people evidence fully clears the people gate, record a matrix-derived
  `GO` with zero blockers.
- While the decision remains `HOLD`, create no NIST mapping records, negative
  dispositions, snapshots, lifecycle events, registry entries, or catalog
  increments.

## Acceptance criteria

- Readiness re-entry is recorded as either refreshed evidenced `HOLD` or
  matrix-derived `GO`.
- If `HOLD`, NIST mapping artifact count remains `0` and generated crosswalk
  catalog counts are unchanged by this issue.
- Focused crosswalk/readiness validators and affected link checks pass on the
  exact candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue does not authorize NIST mapping authorship under `HOLD`, clear
HITRUST or PCI DSS blockers, close Issue #55, or claim certification,
compliance, equivalence, endorsement, assurance, or production readiness.
```

---

## Task 10: Ready-to-file Issue G - v0.11-draft publication gates

Title: `Close the v0.11-draft publication gates`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Close the ordinary `v0.11-draft` release gates on one exact release candidate
after tracker hygiene, the four toolkit deepen packs, and NIST AI RMF
readiness re-entry are complete.

## Dependencies

Depends on completion of:

- Sync post-v0.10 tracker hygiene;
- Deepen assessment workbook Draft pack;
- Deepen evidence catalog Draft pack;
- Deepen audit checklist Draft pack;
- Deepen governance templates Draft pack; and
- Refresh NIST AI RMF readiness package.

Issues #55 and #60 may remain open. They are not `v0.11-draft` exit criteria.

## Deliverables

- Exact-candidate technical, editorial, and governance reviews.
- Full test suite, control, architecture, assessment, profile, crosswalk, link,
  release, working-tree, and applicable Mermaid-rendering gates.
- Synchronized README, VERSION, changelog, roadmap, release plan, backlog,
  milestones, and readiness record.
- Annotated tag `v0.11-draft` and consolidated publication evidence bound to
  the exact candidate SHA.

## Acceptance criteria

- Every `v0.11-draft` exit criterion in `project/MILESTONES.md` is satisfied.
- Critical and Important findings are resolved.
- Post-merge validation passes before any immutable tag or publication
  statement is created.

## Boundaries

Publication remains a Working Draft. It does not complete qualified UK mapping
review, clear HITRUST / PCI DSS / NIST AI RMF blockers, approve Draft artifact
lifecycle transitions without their own evidence, or establish certification,
compliance, equivalence, endorsement, external-scheme approval, assurance, or
production readiness.
```
