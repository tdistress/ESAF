# ESAF v0.14-draft Next-Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land durable `v0.14-draft` milestone, backlog, and roadmap records plus ready-to-file issue bodies for post-v0.13 tracker hygiene, bounded ESAF-1500 Assessment Guide Working Draft deepen (`0.1.0` → `0.1.1`), and publication gates.

**Architecture:** Keep `v0.13-draft` publication identity and Draft lifecycle states intact. Add a bounded `## v0.14-draft` milestone section mirroring `v0.13-draft`, a post-v0.13 backlog queue, a roadmap delivery sequence, and pinned issue-body fixtures in this plan for later GitHub filing. Do not deepen ESAF-1500 content, reopen/close GitHub issues, edit GitHub tracker state, open a readiness/crosswalk workstream, or publish a tag in this planning change.

**Tech Stack:** Markdown project records, `unittest` release-metadata invariants.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-10-v014-draft-next-steps-design.md`
- Milestone identity: `v0.14-draft` (Working Draft tag name when later published)
- Sequence: tracker hygiene → ESAF-1500 deepen → publication gates
- Issues `#55` / `#60` are not `v0.14-draft` blockers after hygiene
- No new readiness or crosswalk workstream
- ESAF-1500 deepen remains Working Draft `0.1.1`; revision history; companion toolkit cross-links (workbook, evidence-catalog, audit-checklist); schemas/examples discoverability; no certification claims; no schema-breaking contract changes; no new maturity levels unless already defined
- Do not redesign `v1.0`, open all of roadmap Phases 4–6, add a second profile, Phase 6 toolkit pack deepen, ISO 27001, or ESAF-1000/1100/1200 re-deepen
- Digests: compute each `PINNED_V014_ISSUE_*_BODY_SHA256` from the final fenced markdown body under the matching line-anchored `^## Task N:` heading via `sha256` of that fenced body (same method as prior next-steps plans)

---

### Task 1: Lock planning invariants with failing tests

**Files:**
- Modify: `tests/test_release_metadata.py`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: existing helpers `read_repository_file`, `markdown_section`,
  `contains_normalized_phrase`, `fenced_markdown_in_task`, `sha256_text`,
  `milestone_section`
- Produces: constants `V014_NEXT_STEPS_PLAN`, `V014_READY_ISSUE_TASKS`, and
  three `PINNED_V014_ISSUE_*_BODY_SHA256` digests (compute after bodies are
  final from fenced markdown under line-anchored `^## Task N:` headings)

- [ ] **Step 1: Add plan path, digest constants, and ready-issue table**

Near the existing `V013_NEXT_STEPS_PLAN` constants, add a plan-path constant
pointing at this file, three `PINNED_V014_ISSUE_*_BODY_SHA256` placeholders, and
a `V014_READY_ISSUE_TASKS` tuple that mirrors `V013_READY_ISSUE_TASKS` with
three entries.

Use the exact Task 4–6 headings and titles already written later in this plan
(do not paste those headings into earlier fenced samples in a way that creates
duplicate first matches). Required phrases per issue:

- Issue A: `reopen Issue #55`, `Issues #158`, `does not change normative`
- Issue B: `ESAF-1500`, `revision history`, `Draft`
- Issue C: `Issues #55 and #60 may remain open`, `Every \`v0.14-draft\` exit criterion`, `Working Draft`

Also update `test_hitrust_backlog_links_open_issue_60` so the expected phrase
includes `v0.14-draft`.

- [ ] **Step 2: Add failing milestone / backlog / roadmap / digest tests**

Add five tests on `ReleaseMetadataTests` that assert:

1. `project/MILESTONES.md` contains `## v0.14-draft` with headings
   `### Entry state`, `### Required workstreams`, `### Exit criteria`,
   `### Non-goals`, and the workstream / exit phrases listed in Task 2.
2. The `### Non-goals` subsection includes: closing Issue `#55`, substantive
   HITRUST mapping, PCI DSS `HOLD`, NIST AI RMF `HOLD`, ISO/IEC 42001 mapping
   records under non-`GO`, authoring NIST CSF mapping records under non-`GO`,
   a new readiness or crosswalk workstream, all roadmap crosswalks, all planned
   profiles, redesigning `v1.0`.
3. `project/BACKLOG.md` section `## Post-v0.13 scheduled queue` lists the three
   initiative titles from Task 2 and says they do not stop later engineering
   work.
4. `ROADMAP.md` section `## 0.14-draft delivery sequence` covers tracker
   hygiene, ESAF-1500, issues 55/60, not exit criteria, and Phases 4/5/6
   long-term direction.
5. Each `V014_READY_ISSUE_TASKS` entry has `Title: \`...\`` in this plan, a
   fenced body matching the pinned digest via `fenced_markdown_in_task` +
   `sha256_text`, required phrases present, and no `closes issue 55` phrase.

Mirror the structure of
`test_planned_v013_issue_bodies_preserve_boundaries_and_digests`.

- [ ] **Step 3: Run focused tests and confirm they fail before content lands**

Run the new tests with:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v014 -v
```

Expected: FAIL (missing `## v0.14-draft` / queue / digests).

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/test_release_metadata.py
git commit -m "test: require v0.14-draft planning invariants"
```

---

### Task 2: Update durable project records

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add `## v0.14-draft` to milestones**

Append after the `v0.13-draft` section (do not rewrite closed publication truth):

```markdown
## v0.14-draft

### Entry state

- `v0.13-draft` is published and its publication evidence is closed.
- ESAF-1300, ESAF-1400, and ESAF-1700 remain at least at Working Draft `0.2.0`
  depth with discoverable example packs.
- ESAF-1500 remains Working Draft `0.1.0`; foundation schemas, examples, and
  the Phase 6 Draft toolkit packs (starters plus `v0.11-draft` deepen) remain
  Draft and authoritative for shared assessment semantics.
- NIST AI RMF readiness remains evidenced `HOLD`; NIST AI RMF mapping artifact
  count remains `0`.
- ISO/IEC 42001 readiness remains evidenced `HOLD`; ISO/IEC 42001 mapping
  artifact count remains `0`.
- NIST CSF 2.0 readiness remains evidenced `HOLD`; NIST CSF mapping artifact
  count remains `0`.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.14-draft` blockers.
- ESAF-1000 remains Working Draft `0.2.1`; ESAF-1100 remains Working Draft
  `0.3.1`; ESAF-1200 remains Working Draft `0.4.1`; ESAF-1600 method artifacts,
  the UK pilot profile, and the three UK mapping snapshots remain Draft.

### Required workstreams

1. **Tracker hygiene.** ESAF shall reopen Issue `#55` if qualified UK mapping
   review remains outstanding, close or explicitly annotate Issues `#158`–`#161`
   as historical completed `v0.13-draft` work, and align backlog and GitHub
   milestone state with published truth. This workstream does not change
   normative content.
2. **ESAF-1500 normative deepen.** ESAF shall complete a bounded Working Draft
   deepen of `assessment/ESAF-1500.md` from `0.1.0` to `0.1.1`: add or update
   revision history; synchronize companion toolkit cross-links to the
   workbook, evidence catalog, and audit checklist; improve schemas/examples
   discoverability; remain Working Draft; introduce no certification claims;
   make no schema-breaking contract changes; and add no new maturity levels
   unless already defined in the guide.
3. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.14-draft` candidate, publish annotated tag `v0.14-draft`, and synchronize
   Working Draft status surfaces.

### Exit criteria

`v0.14-draft` is complete only when:

- tracker hygiene is complete: Issues `#158`–`#161` are closed or explicitly
  annotated as historical, and Issue `#55` is open if and only if qualified UK
  review remains outstanding;
- ESAF-1500 has a bounded deepen to Working Draft `0.1.1` with revision-history
  evidence, companion toolkit cross-links, improved schemas/examples
  discoverability, remains Draft, and does not break schema contracts or invent
  new maturity levels;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.14-draft` is published and Working Draft surfaces are
  synchronized.

### Non-goals

`v0.14-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping;
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` when named mapper and independent reviewers
  remain unavailable;
- authoring ISO/IEC 42001 mapping records, snapshots, or catalog entries under
  a non-`GO` readiness decision;
- authoring NIST CSF mapping records, snapshots, or catalog entries under a
  non-`GO` readiness decision;
- a new readiness or crosswalk workstream;
- a second industry or jurisdiction profile;
- another Phase 6 toolkit pack deepen or a complete assessment library;
- ISO 27001 readiness or mapping work;
- ESAF-1000, ESAF-1100, or ESAF-1200 re-deepen;
- schema-breaking changes to ESAF-1500 contracts or examples;
- new maturity levels beyond those already defined in ESAF-1500;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.
```

- [ ] **Step 2: Add `## Post-v0.13 scheduled queue` to the backlog**

Insert after `## Post-v0.12 scheduled queue` (keep that section as historical
`v0.13-draft` context). New section:

```markdown
## Post-v0.13 scheduled queue

These initiatives are required for `v0.14-draft` and shall be tracked in GitHub
Issues under milestone `v0.14-draft`. Deferred mapping assurance and HITRUST
readiness remain tracked separately and do not stop later engineering work.

- Sync post-v0.13 tracker hygiene
- Deepen ESAF-1500 Assessment Guide Working Draft
- Close the v0.14-draft publication gates
```

Also extend the HITRUST backlog line so it states the work does not block
`v0.5-beta`, `v0.9-rc1`, `v0.10-draft`, `v0.11-draft`, `v0.12-draft`,
`v0.13-draft`, or `v0.14-draft`.

- [ ] **Step 3: Add `## 0.14-draft delivery sequence` to the roadmap**

Insert before `## 0.13-draft delivery sequence`:

```markdown
## 0.14-draft delivery sequence

`v0.14-draft` follows tracker hygiene, then bounded ESAF-1500 Assessment Guide
Working Draft deepen (`0.1.0` to `0.1.1`), then ordinary publication gates on
the exact candidate. Deferred mapping assurance remains tracked through issue
55 and does not stop later engineering work. HITRUST readiness remains
separately gated through issue 60. Issues 55 and 60 are not `v0.14-draft` exit
criteria. No new readiness or crosswalk workstream is required for this
milestone. Publication does not change any control, architecture, profile,
mapping-set, or mapping-record lifecycle state. Phases 4, 5, and 6 remain
long-term direction except for the bounded normative deepen required by this
milestone.
```

- [ ] **Step 4: Run the Task 1 tests again**

Expected: milestone/backlog/roadmap tests PASS; digest test still FAIL until
digests are pinned from the fenced bodies already in this plan (Tasks 4–6).

- [ ] **Step 5: Commit durable records**

```bash
git add project/MILESTONES.md project/BACKLOG.md ROADMAP.md
git commit -m "docs: define v0.14-draft milestone and post-v0.13 queue"
```

---

### Task 3: Pin issue-body digests, validate, and open the pull request

**Files:**
- Modify: `tests/test_release_metadata.py`

- [ ] **Step 1: Compute digests from this plan’s fenced bodies**

Digests shall be computed from the final fenced markdown bodies via sha256,
using line-anchored `^## Task N:` headings (not substring-only matches):

```bash
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
from pathlib import Path
import hashlib, re
plan = Path("docs/superpowers/plans/2026-09-10-v014-draft-next-steps.md").read_text()
for heading in [
    "## Task 4: Ready-to-file Issue A - tracker hygiene",
    "## Task 5: Ready-to-file Issue B - ESAF-1500 deepen",
    "## Task 6: Ready-to-file Issue C - v0.14-draft publication gates",
]:
    heading_match = re.search(rf"^{re.escape(heading)}\s*$", plan, re.MULTILINE)
    assert heading_match is not None, heading
    start = heading_match.start()
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
  tests.test_release_metadata.ReleaseMetadataTests.test_v014_draft_has_bounded_workstreams_and_exit_criteria \
  tests.test_release_metadata.ReleaseMetadataTests.test_v014_draft_preserves_bounded_non_goals \
  tests.test_release_metadata.ReleaseMetadataTests.test_backlog_records_post_v013_v014_draft_initiatives \
  tests.test_release_metadata.ReleaseMetadataTests.test_roadmap_records_v014_draft_delivery_sequence \
  tests.test_release_metadata.ReleaseMetadataTests.test_planned_v014_issue_bodies_preserve_boundaries_and_digests \
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
  docs/superpowers/plans/2026-09-10-v014-draft-next-steps.md \
  docs/superpowers/specs/2026-09-10-v014-draft-next-steps-design.md
git commit -m "docs: plan v0.14-draft next steps and pin issue bodies"
git push -u origin HEAD
```

Open or update a draft PR against `main` describing planning-only scope.
Do not create the three GitHub issues or edit GitHub tracker state in this
planning change; filing happens after the planning PR merges.

---

## Task 4: Ready-to-file Issue A - tracker hygiene

Title: `Sync post-v0.13 tracker hygiene`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Restore GitHub tracker state so it matches post-`v0.13-draft` repository truth
before `v0.14-draft` content work begins.

## Dependencies

Depends on the merged `v0.14-draft` planning records. Blocks filing or starting
the deepen issue only insofar as milestone/`#55` truth must be corrected first.
Does not depend on Issues #60 content work.

## Deliverables

- Reopen Issue #55 if qualified UK mapping review remains outstanding, with a
  short comment stating owner-risk acceptance did not complete qualified review.
- Close or explicitly annotate Issues #158–#161 as historical completed
  `v0.13-draft` work, linking the published tag evidence where useful.
- Align GitHub milestone `v0.13-draft` / `v0.14-draft` membership and
  `project/BACKLOG.md` wording with the durable records.
- Record the resulting open/closed matrix in the issue comments.

## Acceptance criteria

- Repository policy and GitHub agree on Issue #55 open/closed state.
- Issues #158–#161 are closed or clearly marked historical completed work.
- `project/BACKLOG.md` deferred-assurance and post-v0.13 queue text remain
  consistent with GitHub.
- No normative ESAF Markdown, schemas, or mappings change in this issue.

## Boundaries

This issue does not change normative ESAF content, complete qualified UK
review, close Issue #55 by owner-risk acceptance, clear HITRUST/PCI/NIST/
ISO/IEC 42001 blockers, open a readiness or crosswalk workstream, or claim
certification, compliance, equivalence, endorsement, or assurance.
```

---

## Task 5: Ready-to-file Issue B - ESAF-1500 deepen

Title: `Deepen ESAF-1500 Assessment Guide Working Draft`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Complete a bounded Working Draft deepen of ESAF-1500 from `0.1.0` to `0.1.1`
so revision history, companion toolkit cross-links, and schemas/examples
discoverability stay aligned after `v0.13-draft`.

## Dependencies

Depends on merged `v0.14-draft` planning records and tracker hygiene. Must
finish before publication gates.

## Deliverables

- Bump `assessment/ESAF-1500.md` Working Draft version from `0.1.0` to `0.1.1`
  and add or update revision history recording the deepen.
- Synchronize companion toolkit cross-links from ESAF-1500 to the Draft
  workbook (`assessment/workbook/`), evidence catalog
  (`assessment/evidence-catalog/`), and audit checklist
  (`assessment/audit-checklist/`).
- Improve discoverability of schemas under `assessment/schema/` and examples
  under `assessment/examples/` without changing contract meaning.
- Keep status Working Draft; introduce no certification claims.
- Make no schema-breaking contract changes to evidence-record,
  assessment-result, or maturity-assessment schemas or examples.
- Add no new maturity levels unless already defined in ESAF-1500.

## Acceptance criteria

- ESAF-1500 deepen is Working Draft `0.1.1` with revision-history evidence.
- Companion toolkit cross-links to workbook, evidence-catalog, and
  audit-checklist are present and accurate.
- Schemas and examples remain discoverable from the guide and assessment index.
- No schema-breaking contract changes; `python tools/validate_assessment.py
  --check` passes on the exact candidate.
- No new maturity levels beyond those already defined.
- Critical and Important findings are resolved.

## Boundaries

This issue does not redesign `v1.0`, invent certification or accreditation
requirements, advance lifecycle states, break ESAF-1500 schema contracts, add
new maturity levels, open a readiness or crosswalk workstream, or claim
compliance, equivalence, endorsement, or assurance.
```

---

## Task 6: Ready-to-file Issue C - v0.14-draft publication gates

Title: `Close the v0.14-draft publication gates`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Close the ordinary `v0.14-draft` release gates on one exact release candidate
after tracker hygiene and ESAF-1500 deepen are complete.

## Dependencies

Depends on completion of:

- Sync post-v0.13 tracker hygiene; and
- Deepen ESAF-1500 Assessment Guide Working Draft.

Issues #55 and #60 may remain open. They are not `v0.14-draft` exit criteria.

## Deliverables

- Exact-candidate technical, editorial, and governance reviews.
- Full test suite, control, architecture, assessment, profile, crosswalk, link,
  release, working-tree, and applicable Mermaid-rendering gates.
- Synchronized README, VERSION, changelog, roadmap, release plan, backlog,
  milestones, and readiness record.
- Annotated tag `v0.14-draft` and consolidated publication evidence bound to
  the exact candidate SHA.

## Acceptance criteria

- Every `v0.14-draft` exit criterion in `project/MILESTONES.md` is satisfied.
- Critical and Important findings are resolved.
- Post-merge validation passes before any immutable tag or publication
  statement is created.

## Boundaries

Publication remains a Working Draft. It does not complete qualified UK mapping
review, clear HITRUST / PCI DSS / NIST AI RMF / ISO/IEC 42001 / NIST CSF
blockers, open a readiness or crosswalk workstream, approve Draft artifact
lifecycle transitions without their own evidence, or establish certification,
compliance, equivalence, endorsement, external-scheme approval, assurance, or
production readiness.
```
