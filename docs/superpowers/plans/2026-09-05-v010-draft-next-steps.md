# ESAF v0.10-draft Next-Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land durable `v0.10-draft` milestone, backlog, and roadmap records plus ready-to-file issue bodies for post-rc1 tracker hygiene and the Phase 6 assessment-toolkit starter.

**Architecture:** Keep `v0.9-rc1` publication identity and Draft lifecycle states intact. Add a bounded `## v0.10-draft` milestone section mirroring `v0.9-rc1`, a post-rc1 backlog queue, a roadmap delivery sequence, and pinned issue-body fixtures in this plan for later GitHub filing. Do not author toolkit content, reopen/close GitHub issues, or publish a tag in this planning change.

**Tech Stack:** Markdown project records, `unittest` release-metadata invariants.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-05-v010-draft-next-steps-design.md`
- Milestone identity: `v0.10-draft` (Working Draft tag name when later published)
- Sequence: tracker hygiene → four toolkit starters (parallel) → publication gates
- Issues `#55` / `#60` are not `v0.10-draft` blockers after hygiene
- Toolkit packs remain Draft; no parallel ESAF-1500 semantics; no certification claims
- Do not redesign `v1.0` or open all of roadmap Phases 4–6

---

### Task 1: Lock planning invariants with failing tests

**Files:**
- Modify: `tests/test_release_metadata.py`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: existing helpers `read_repository_file`, `markdown_section`,
  `contains_normalized_phrase`, `fenced_markdown_in_task`, `sha256_text`
- Produces: constants `V010_NEXT_STEPS_PLAN`, `V010_READY_ISSUE_TASKS`, and
  six `PINNED_V010_ISSUE_*_BODY_SHA256` digests (compute after bodies are final)

- [ ] **Step 1: Add plan path, digest constants, and ready-issue table**

Near the existing `V09_NEXT_STEPS_PLAN` constants, add a plan-path constant
pointing at this file, six `PINNED_V010_ISSUE_*_BODY_SHA256` placeholders, and
a `V010_READY_ISSUE_TASKS` tuple that mirrors `V09_READY_ISSUE_TASKS`.

Use the exact Task 4–9 headings and titles already written later in this plan
(do not paste those headings into earlier fenced samples in a way that creates
duplicate first matches). Required phrases per issue:

- Issue A: `reopen Issue #55`, `Issues #90`, `does not change normative`
- Issue B: `ESAF-1500`, `ESAF-1100`, `Draft starter`
- Issue C: `evidence catalog`, `ESAF-1500 evidence contract`, `Draft starter`
- Issue D: `audit checklist`, `assessment-result`, `Draft starter`
- Issue E: `templates/`, `ESAF-1300`, `ESAF-1400`
- Issue F: `Issues #55 and #60 may remain open`, `Every \`v0.10-draft\` exit criterion`, `Working Draft`

- [ ] **Step 2: Add failing milestone / backlog / roadmap / digest tests**

Add five tests on `ReleaseMetadataTests` that assert:

1. `project/MILESTONES.md` contains `## v0.10-draft` with headings
   `### Entry state`, `### Required workstreams`, `### Exit criteria`,
   `### Non-goals`, and the workstream / exit phrases listed in Task 2.
2. The `### Non-goals` subsection includes: closing Issue `#55`, substantive
   HITRUST mapping, PCI DSS `HOLD`, NIST AI RMF `HOLD`, all roadmap
   crosswalks, all planned profiles, redesigning `v1.0`.
3. `project/BACKLOG.md` section `## Post-rc1 scheduled queue` lists the six
   initiative titles from Task 2 and says they do not stop later engineering
   work.
4. `ROADMAP.md` section `## 0.10-draft delivery sequence` covers tracker
   hygiene, the four toolkit packs, issues 55/60, not exit criteria, and
   Phase 6.
5. Each `V010_READY_ISSUE_TASKS` entry has `Title: \`...\`` in this plan, a
   fenced body matching the pinned digest via `fenced_markdown_in_task` +
   `sha256_text`, required phrases present, and no `closes issue 55` phrase.

Mirror the structure of
`test_planned_v09_issue_bodies_preserve_boundaries_and_digests`.

- [ ] **Step 3: Run focused tests and confirm they fail before content lands**

Run the five new tests with:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v010 -v
```

Expected: FAIL (missing `## v0.10-draft` / queue / digests).

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/test_release_metadata.py
git commit -m "test: require v0.10-draft planning invariants"
```

---

### Task 2: Update durable project records

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add `## v0.10-draft` to milestones**

Append after the `v0.9-rc1` section (do not rewrite closed publication truth):

```markdown
## v0.10-draft

### Entry state

- `v0.9-rc1` is published and its publication evidence is closed.
- ESAF-1300, ESAF-1400, and ESAF-1700 are at least at post-rc1 Working Draft
  `0.2.0` depth with discoverable example packs.
- ESAF-1500 foundation schemas and examples remain Draft and authoritative for
  shared assessment semantics.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.10-draft` blockers.
- ESAF-1000, ESAF-1100, ESAF-1200, ESAF-1600 method artifacts, the UK pilot
  profile, and the three UK mapping snapshots remain Draft.

### Required workstreams

1. **Tracker hygiene.** ESAF shall reopen Issue `#55` if qualified UK mapping
   review remains outstanding, close or explicitly annotate Issues `#90`–`#95`
   as historical completed `v0.9-rc1` work, and align backlog and GitHub
   milestone state with published truth. This workstream does not change
   normative content.
2. **Assessment workbook Draft starter.** ESAF shall author a Draft assessor
   workbook skeleton bound to ESAF-1500 shared contracts and ESAF-1100 control
   assessment procedures without inventing parallel evidence, result, or
   maturity semantics.
3. **Evidence catalog Draft starter.** ESAF shall author a Draft starter catalog
   of evidence types and expectations reusable by profiles and crosswalks,
   aligned to the ESAF-1500 evidence contract.
4. **Audit checklist Draft starter.** ESAF shall author a Draft checklist for
   control/capability sampling against the shared assessment-result contract.
5. **Governance templates Draft starter.** ESAF shall author a Draft starter pack
   under `templates/` covering risk, exception, decision, and retirement-class
   artifacts, linked from ESAF-1300 / ESAF-1400 without adding new normative
   requirements.
6. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.10-draft` candidate, publish annotated tag `v0.10-draft`, and synchronize
   Working Draft status surfaces.

### Exit criteria

`v0.10-draft` is complete only when:

- tracker hygiene is complete: Issues `#90`–`#95` are closed or explicitly
  annotated as historical, and Issue `#55` is open if and only if qualified UK
  review remains outstanding;
- the assessment workbook, evidence catalog, audit checklist, and governance
  template starter each exist as Draft and are linked from applicable indexes;
- each toolkit pack reuses ESAF-1500 shared semantics and does not invent
  parallel maturity, evidence, or result contracts;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.10-draft` is published and Working Draft surfaces are
  synchronized.

### Non-goals

`v0.10-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping;
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` or authoring NIST mapping records;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.
```

- [ ] **Step 2: Add `## Post-rc1 scheduled queue` to the backlog**

Insert after `## Post-beta scheduled queue` (keep that section as historical
`v0.9-rc1` context). New section:

```markdown
## Post-rc1 scheduled queue

These initiatives are required for `v0.10-draft` and shall be tracked in GitHub
Issues under milestone `v0.10-draft`. Deferred mapping assurance and HITRUST
readiness remain tracked separately and do not stop later engineering work.

- Sync post-rc1 tracker hygiene
- Author assessment workbook Draft starter
- Author evidence catalog Draft starter
- Author audit checklist Draft starter
- Author governance templates Draft starter
- Close the v0.10-draft publication gates
```

Also extend the HITRUST backlog line so it states the work does not block
`v0.5-beta`, `v0.9-rc1`, or `v0.10-draft`.

- [ ] **Step 3: Add `## 0.10-draft delivery sequence` to the roadmap**

Insert before `## 0.9-rc1 delivery sequence`:

```markdown
## 0.10-draft delivery sequence

`v0.10-draft` follows tracker hygiene, then the Phase 6 assessment-toolkit
starter (assessment workbook, evidence catalog, audit checklist, and
governance templates), then ordinary publication gates on the exact candidate.
Deferred mapping assurance remains tracked through issue 55 and does not stop
later engineering work. HITRUST readiness remains separately gated through
issue 60. Issues 55 and 60 are not `v0.10-draft` exit criteria. Publication
does not change any control, architecture, profile, mapping-set, or
mapping-record lifecycle state. Phases 4 and 5 remain long-term direction.
Phase 6 remains long-term direction except for the bounded starter packs
required by this milestone.
```

- [ ] **Step 4: Run the Task 1 tests again**

Expected: milestone/backlog/roadmap tests PASS; digest test still FAIL until
digests are pinned from the fenced bodies already in this plan (Tasks 4–9).

- [ ] **Step 5: Commit durable records**

```bash
git add project/MILESTONES.md project/BACKLOG.md ROADMAP.md
git commit -m "docs: define v0.10-draft milestone and post-rc1 queue"
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
plan = Path("docs/superpowers/plans/2026-09-05-v010-draft-next-steps.md").read_text()
# Use rfind so this script's own heading strings are not matched first.
for heading in [
    "## Task 4: Ready-to-file Issue A - tracker hygiene",
    "## Task 5: Ready-to-file Issue B - assessment workbook",
    "## Task 6: Ready-to-file Issue C - evidence catalog",
    "## Task 7: Ready-to-file Issue D - audit checklist",
    "## Task 8: Ready-to-file Issue E - governance templates",
    "## Task 9: Ready-to-file Issue F - v0.10-draft publication gates",
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
  tests.test_release_metadata.ReleaseMetadataTests.test_v010_draft_has_bounded_workstreams_and_exit_criteria \
  tests.test_release_metadata.ReleaseMetadataTests.test_v010_draft_preserves_bounded_non_goals \
  tests.test_release_metadata.ReleaseMetadataTests.test_backlog_records_post_rc1_v010_draft_initiatives \
  tests.test_release_metadata.ReleaseMetadataTests.test_roadmap_records_v010_draft_delivery_sequence \
  tests.test_release_metadata.ReleaseMetadataTests.test_planned_v010_issue_bodies_preserve_boundaries_and_digests \
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
  docs/superpowers/plans/2026-09-05-v010-draft-next-steps.md \
  docs/superpowers/specs/2026-09-05-v010-draft-next-steps-design.md
git commit -m "docs: plan v0.10-draft next steps and pin issue bodies"
git push -u origin HEAD
```

Open or update a draft PR against `main` describing planning-only scope.

---

## Task 4: Ready-to-file Issue A - tracker hygiene

Title: `Sync post-rc1 tracker hygiene`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Restore GitHub tracker state so it matches post-`v0.9-rc1` repository truth
before `v0.10-draft` content work begins.

## Dependencies

Depends on the merged `v0.10-draft` planning records. Blocks filing or starting
the toolkit issues only insofar as milestone/`#55` truth must be corrected
first. Does not depend on Issues #60 content work.

## Deliverables

- Reopen Issue #55 if qualified UK mapping review remains outstanding, with a
  short comment stating owner-risk acceptance did not complete qualified review.
- Close or explicitly annotate Issues #90–#95 as historical completed
  `v0.9-rc1` work, linking the published tag evidence where useful.
- Align GitHub milestone `v0.9-rc1` / `v0.10-draft` membership and
  `project/BACKLOG.md` wording with the durable records.
- Record the resulting open/closed matrix in the issue comments.

## Acceptance criteria

- Repository policy and GitHub agree on Issue #55 open/closed state.
- Issues #90–#95 are closed or clearly marked historical completed work.
- `project/BACKLOG.md` deferred-assurance and post-rc1 queue text remain
  consistent with GitHub.
- No normative ESAF Markdown, schemas, or mappings change in this issue.

## Boundaries

This issue does not change normative ESAF content, complete qualified UK
review, close Issue #55 by owner-risk acceptance, clear HITRUST/PCI/NIST
blockers, or claim certification, compliance, equivalence, endorsement, or
assurance.
```

---

## Task 5: Ready-to-file Issue B - assessment workbook

Title: `Author assessment workbook Draft starter`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Author a Draft assessor workbook starter that operators can use with existing
ESAF-1500 shared contracts and ESAF-1100 control assessment procedures.

## Dependencies

Depends on merged `v0.10-draft` planning records and completion (or explicit
waiver note) of tracker hygiene. May proceed in parallel with the evidence
catalog, audit checklist, and governance-template issues.

## Deliverables

- Draft workbook skeleton under `assessment/` (or linked companion path) covering
  scope, evidence references, procedure steps, findings, and result recording.
- Bind fields to ESAF-1500 evidence / assessment-result / maturity contracts.
- Reference ESAF-1100 assessment procedures without inventing parallel controls.
- Link the workbook from applicable assessment indexes and README surfaces.

## Acceptance criteria

- Workbook is internally consistent, Draft-labeled, and free of certification
  claims.
- No parallel evidence, result, or maturity semantics are introduced.
- Focused assessment validators and affected link checks pass on the exact
  candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue publishes a Draft starter only. It does not approve certification,
compliance, equivalence, endorsement, assurance, or production readiness, and
it does not advance control or mapping lifecycle states.
```

---

## Task 6: Ready-to-file Issue C - evidence catalog

Title: `Author evidence catalog Draft starter`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Author a Draft starter evidence catalog of evidence types and expectations
reusable by profiles and crosswalks, aligned to the ESAF-1500 evidence
contract.

## Dependencies

Depends on merged `v0.10-draft` planning records and tracker hygiene. May
proceed in parallel with the workbook, audit checklist, and governance-template
issues.

## Deliverables

- Draft evidence catalog listing evidence types, expected attributes, and
  example uses bound to the ESAF-1500 evidence contract.
- Keep catalog entries profile- and framework-neutral unless explicitly marked
  as examples.
- Link the catalog from applicable assessment indexes.

## Acceptance criteria

- Catalog is Draft-labeled and reuses ESAF-1500 evidence semantics.
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

## Task 7: Ready-to-file Issue D - audit checklist

Title: `Author audit checklist Draft starter`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Author a Draft starter audit checklist for control/capability sampling against
the shared ESAF-1500 assessment-result contract.

## Dependencies

Depends on merged `v0.10-draft` planning records and tracker hygiene. May
proceed in parallel with the workbook, evidence catalog, and governance-template
issues.

## Deliverables

- Draft checklist covering sampling intent, procedure references, evidence
  pointers, determination capture, and limitation notes.
- Bind determinations to the shared assessment-result vocabulary.
- Link the checklist from applicable assessment indexes.

## Acceptance criteria

- Checklist is Draft-labeled and consistent with ESAF-1500 result semantics.
- No parallel determination vocabulary is introduced.
- Focused assessment validators and affected link checks pass on the exact
  candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue does not create a certification audit program, complete qualified
mapping review, or claim compliance, equivalence, endorsement, or assurance.
```

---

## Task 8: Ready-to-file Issue E - governance templates

Title: `Author governance templates Draft starter`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Author a Draft governance template starter pack under `templates/` covering
risk, exception, decision, and retirement-class artifacts, linked from
ESAF-1300 and ESAF-1400 without adding new normative requirements.

## Dependencies

Depends on merged `v0.10-draft` planning records and tracker hygiene. May
proceed in parallel with the workbook, evidence catalog, and audit-checklist
issues.

## Deliverables

- Replace or extend the `templates/` placeholder with Draft starters for risk,
  exception, decision, and retirement-class records.
- Link templates from ESAF-1300 / ESAF-1400 and `templates/` indexes.
- Keep templates non-normative; do not invent requirements beyond existing
  publications.

## Acceptance criteria

- Template pack is Draft-labeled and discoverable from governance and
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

## Task 9: Ready-to-file Issue F - v0.10-draft publication gates

Title: `Close the v0.10-draft publication gates`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Close the ordinary `v0.10-draft` release gates on one exact release candidate
after tracker hygiene and the four toolkit starters are complete.

## Dependencies

Depends on completion of:

- Sync post-rc1 tracker hygiene;
- Author assessment workbook Draft starter;
- Author evidence catalog Draft starter;
- Author audit checklist Draft starter; and
- Author governance templates Draft starter.

Issues #55 and #60 may remain open. They are not `v0.10-draft` exit criteria.

## Deliverables

- Exact-candidate technical, editorial, and governance reviews.
- Full test suite, control, architecture, assessment, profile, crosswalk, link,
  release, working-tree, and applicable Mermaid-rendering gates.
- Synchronized README, VERSION, changelog, roadmap, release plan, backlog,
  milestones, and readiness record.
- Annotated tag `v0.10-draft` and consolidated publication evidence bound to
  the exact candidate SHA.

## Acceptance criteria

- Every `v0.10-draft` exit criterion in `project/MILESTONES.md` is satisfied.
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
