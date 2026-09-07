# ESAF v0.13-draft Next-Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land durable `v0.13-draft` milestone, backlog, and roadmap records plus ready-to-file issue bodies for post-v0.12 tracker hygiene, NIST CSF 2.0 public-source readiness (default evidenced `HOLD`), bounded ESAF-1200 normative deepen, and publication gates.

**Architecture:** Keep `v0.12-draft` publication identity and Draft lifecycle states intact. Add a bounded `## v0.13-draft` milestone section mirroring `v0.12-draft`, a post-v0.12 backlog queue, a roadmap delivery sequence, and pinned issue-body fixtures in this plan for later GitHub filing. Do not author NIST CSF readiness artifacts, deepen ESAF-1200 content, reopen/close GitHub issues, or publish a tag in this planning change.

**Tech Stack:** Markdown project records, `unittest` release-metadata invariants.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-07-v013-draft-next-steps-design.md`
- Milestone identity: `v0.13-draft` (Working Draft tag name when later published)
- Sequence: tracker hygiene → NIST CSF 2.0 readiness → ESAF-1200 deepen → publication gates
- Issues `#55` / `#60` are not `v0.13-draft` blockers after hygiene
- NIST CSF 2.0 default exit is evidenced `HOLD`; no mapping records while `HOLD` or `NO_GO`
- ESAF-1200 deepen remains Draft; no new patterns; no certification claims
- Do not redesign `v1.0`, open all of roadmap Phases 4–6, add a second profile, Phase 6 toolkit deepen, ISO 27001, or ESAF-1000/1100 re-deepen

---

### Task 1: Lock planning invariants with failing tests

**Files:**
- Modify: `tests/test_release_metadata.py`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: existing helpers `read_repository_file`, `markdown_section`,
  `contains_normalized_phrase`, `fenced_markdown_in_task`, `sha256_text`,
  `milestone_section`
- Produces: constants `V013_NEXT_STEPS_PLAN`, `V013_READY_ISSUE_TASKS`, and
  four `PINNED_V013_ISSUE_*_BODY_SHA256` digests (compute after bodies are final)

- [ ] **Step 1: Add plan path, digest constants, and ready-issue table**

Near the existing `V012_NEXT_STEPS_PLAN` constants, add a plan-path constant
pointing at this file, four `PINNED_V013_ISSUE_*_BODY_SHA256` placeholders, and
a `V013_READY_ISSUE_TASKS` tuple that mirrors `V012_READY_ISSUE_TASKS`.

Use the exact Task 4–7 headings and titles already written later in this plan
(do not paste those headings into earlier fenced samples in a way that creates
duplicate first matches). Required phrases per issue:

- Issue A: `reopen Issue #55`, `Issues #142`, `does not change normative`
- Issue B: `NIST CSF`, `HOLD`, `mapping records`
- Issue C: `ESAF-1200`, `revision history`, `Draft`
- Issue D: `Issues #55 and #60 may remain open`, `Every \`v0.13-draft\` exit criterion`, `Working Draft`

Also update `test_hitrust_backlog_links_open_issue_60` so the expected phrase
includes `v0.13-draft`.

- [ ] **Step 2: Add failing milestone / backlog / roadmap / digest tests**

Add five tests on `ReleaseMetadataTests` that assert:

1. `project/MILESTONES.md` contains `## v0.13-draft` with headings
   `### Entry state`, `### Required workstreams`, `### Exit criteria`,
   `### Non-goals`, and the workstream / exit phrases listed in Task 2.
2. The `### Non-goals` subsection includes: closing Issue `#55`, substantive
   HITRUST mapping, PCI DSS `HOLD`, NIST AI RMF `HOLD`, ISO/IEC 42001 mapping
   records under non-`GO`, authoring NIST CSF mapping records under non-`GO`,
   all roadmap crosswalks, all planned profiles, redesigning `v1.0`.
3. `project/BACKLOG.md` section `## Post-v0.12 scheduled queue` lists the four
   initiative titles from Task 2 and says they do not stop later engineering
   work.
4. `ROADMAP.md` section `## 0.13-draft delivery sequence` covers tracker
   hygiene, NIST CSF, ESAF-1200, issues 55/60, not exit criteria, evidenced
   `HOLD`, and Phases 4/5/6 long-term direction.
5. Each `V013_READY_ISSUE_TASKS` entry has `Title: \`...\`` in this plan, a
   fenced body matching the pinned digest via `fenced_markdown_in_task` +
   `sha256_text`, required phrases present, and no `closes issue 55` phrase.

Mirror the structure of
`test_planned_v012_issue_bodies_preserve_boundaries_and_digests`.

- [ ] **Step 3: Run focused tests and confirm they fail before content lands**

Run the new tests with:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v013 -v
```

Expected: FAIL (missing `## v0.13-draft` / queue / digests).

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/test_release_metadata.py
git commit -m "test: require v0.13-draft planning invariants"
```

---

### Task 2: Update durable project records

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add `## v0.13-draft` to milestones**

Append after the `v0.12-draft` section (do not rewrite closed publication truth):

```markdown
## v0.13-draft

### Entry state

- `v0.12-draft` is published and its publication evidence is closed.
- ESAF-1300, ESAF-1400, and ESAF-1700 remain at least at Working Draft `0.2.0`
  depth with discoverable example packs.
- ESAF-1500 foundation schemas, examples, and the Phase 6 Draft toolkit packs
  (starters plus `v0.11-draft` deepen) remain Draft and authoritative for
  shared assessment semantics.
- NIST AI RMF readiness remains evidenced `HOLD`; NIST AI RMF mapping artifact
  count remains `0`.
- ISO/IEC 42001 readiness remains evidenced `HOLD`; ISO/IEC 42001 mapping
  artifact count remains `0`.
- No NIST CSF 2.0 readiness package or mapping artifacts exist yet.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.13-draft` blockers.
- ESAF-1000 remains Working Draft `0.2.1`; ESAF-1100 remains Working Draft
  `0.3.1`; ESAF-1200 remains Version `0.4-alpha`; ESAF-1600 method artifacts,
  the UK pilot profile, and the three UK mapping snapshots remain Draft.

### Required workstreams

1. **Tracker hygiene.** ESAF shall reopen Issue `#55` if qualified UK mapping
   review remains outstanding, close or explicitly annotate Issues `#142`–`#146`
   as historical completed `v0.12-draft` work, and align backlog and GitHub
   milestone state with published truth. This workstream does not change
   normative content.
2. **NIST CSF 2.0 public-source readiness.** ESAF shall pin the applicable
   official NIST Cybersecurity Framework (CSF) 2.0 source identity, establish
   publication-rights and provision-inventory boundaries, assess mapper and
   qualified-review availability, produce a mechanical readiness matrix, and
   record a `GO` / `HOLD` / `NO_GO` decision. The default acceptable exit is
   an evidenced `HOLD` that restates blockers, owners, reconsideration
   triggers, re-entry tests, and nonclaims. A matrix-derived `GO` is allowed
   only when every readiness gate clears, including named mapper and
   independent reviewer evidence. While the decision remains `HOLD` or
   `NO_GO`, ESAF shall not create NIST CSF mapping relationships, negative
   dispositions, snapshots, lifecycle events, registry entries, or catalog
   increments.
3. **ESAF-1200 normative deepen.** ESAF shall complete a bounded Working Draft
   method and cross-link pass on `architectures/ESAF-1200.md`: synchronize
   cross-links to patterns, trust zones, and pattern-selection surfaces,
   align method wording for consistency, bump revision history, and remain
   Draft. No new architecture patterns. No pattern-population expansion.
4. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.13-draft` candidate, publish annotated tag `v0.13-draft`, and synchronize
   Working Draft status surfaces.

### Exit criteria

`v0.13-draft` is complete only when:

- tracker hygiene is complete: Issues `#142`–`#146` are closed or explicitly
  annotated as historical, and Issue `#55` is open if and only if qualified UK
  review remains outstanding;
- NIST CSF 2.0 readiness is recorded as evidenced `GO`, `HOLD`, or `NO_GO`;
  if `HOLD` or `NO_GO`, NIST CSF mapping artifact count remains `0` and
  generated crosswalk catalog counts are unchanged by that workstream;
- ESAF-1200 has a bounded deepen with revision-history evidence, remains Draft,
  and does not add new patterns or invent parallel architecture semantics;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.13-draft` is published and Working Draft surfaces are
  synchronized.

### Non-goals

`v0.13-draft` does not require:

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
- a second industry or jurisdiction profile;
- another Phase 6 toolkit deepen or a complete assessment library;
- ISO 27001 readiness or mapping work;
- ESAF-1000 or ESAF-1100 re-deepen;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.
```

- [ ] **Step 2: Add `## Post-v0.12 scheduled queue` to the backlog**

Insert after `## Post-v0.11 scheduled queue` (keep that section as historical
`v0.12-draft` context). New section:

```markdown
## Post-v0.12 scheduled queue

These initiatives are required for `v0.13-draft` and shall be tracked in GitHub
Issues under milestone `v0.13-draft`. Deferred mapping assurance and HITRUST
readiness remain tracked separately and do not stop later engineering work.

- Sync post-v0.12 tracker hygiene
- Complete NIST CSF 2.0 public-source readiness and mapping go/no-go
- Deepen ESAF-1200 Reference Architecture Working Draft
- Close the v0.13-draft publication gates
```

Also extend the HITRUST backlog line so it states the work does not block
`v0.5-beta`, `v0.9-rc1`, `v0.10-draft`, `v0.11-draft`, `v0.12-draft`, or
`v0.13-draft`.

- [ ] **Step 3: Add `## 0.13-draft delivery sequence` to the roadmap**

Insert before `## 0.12-draft delivery sequence`:

```markdown
## 0.13-draft delivery sequence

`v0.13-draft` follows tracker hygiene, then NIST CSF 2.0 public-source
readiness, then bounded ESAF-1200 normative deepen, then ordinary publication
gates on the exact candidate. Deferred mapping assurance remains tracked
through issue 55 and does not stop later engineering work. HITRUST readiness
remains separately gated through issue 60. Issues 55 and 60 are not
`v0.13-draft` exit criteria. NIST CSF 2.0 readiness may exit as an evidenced
`HOLD` when people, rights, or source-access gates remain blocked; while
`HOLD` or `NO_GO`, no NIST CSF mapping records are authored. Publication does
not change any control, architecture, profile, mapping-set, or mapping-record
lifecycle state. Phases 4, 5, and 6 remain long-term direction except for the
bounded readiness and normative deepen required by this milestone.
```

- [ ] **Step 4: Run the Task 1 tests again**

Expected: milestone/backlog/roadmap tests PASS; digest test still FAIL until
digests are pinned from the fenced bodies already in this plan (Tasks 4–7).

- [ ] **Step 5: Commit durable records**

```bash
git add project/MILESTONES.md project/BACKLOG.md ROADMAP.md
git commit -m "docs: define v0.13-draft milestone and post-v0.12 queue"
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
plan = Path("docs/superpowers/plans/2026-09-07-v013-draft-next-steps.md").read_text()
for heading in [
    "## Task 4: Ready-to-file Issue A - tracker hygiene",
    "## Task 5: Ready-to-file Issue B - NIST CSF 2.0 readiness",
    "## Task 6: Ready-to-file Issue C - ESAF-1200 deepen",
    "## Task 7: Ready-to-file Issue D - v0.13-draft publication gates",
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
  tests.test_release_metadata.ReleaseMetadataTests.test_v013_draft_has_bounded_workstreams_and_exit_criteria \
  tests.test_release_metadata.ReleaseMetadataTests.test_v013_draft_preserves_bounded_non_goals \
  tests.test_release_metadata.ReleaseMetadataTests.test_backlog_records_post_v012_v013_draft_initiatives \
  tests.test_release_metadata.ReleaseMetadataTests.test_roadmap_records_v013_draft_delivery_sequence \
  tests.test_release_metadata.ReleaseMetadataTests.test_planned_v013_issue_bodies_preserve_boundaries_and_digests \
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
  docs/superpowers/plans/2026-09-07-v013-draft-next-steps.md \
  docs/superpowers/specs/2026-09-07-v013-draft-next-steps-design.md
git commit -m "docs: plan v0.13-draft next steps and pin issue bodies"
git push -u origin HEAD
```

Open or update a draft PR against `main` describing planning-only scope.

---

## Task 4: Ready-to-file Issue A - tracker hygiene

Title: `Sync post-v0.12 tracker hygiene`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Restore GitHub tracker state so it matches post-`v0.12-draft` repository truth
before `v0.13-draft` content work begins.

## Dependencies

Depends on the merged `v0.13-draft` planning records. Blocks filing or starting
the readiness and deepen issues only insofar as milestone/`#55` truth must be
corrected first. Does not depend on Issues #60 content work.

## Deliverables

- Reopen Issue #55 if qualified UK mapping review remains outstanding, with a
  short comment stating owner-risk acceptance did not complete qualified review.
- Close or explicitly annotate Issues #142–#146 as historical completed
  `v0.12-draft` work, linking the published tag evidence where useful.
- Align GitHub milestone `v0.12-draft` / `v0.13-draft` membership and
  `project/BACKLOG.md` wording with the durable records.
- Record the resulting open/closed matrix in the issue comments.

## Acceptance criteria

- Repository policy and GitHub agree on Issue #55 open/closed state.
- Issues #142–#146 are closed or clearly marked historical completed work.
- `project/BACKLOG.md` deferred-assurance and post-v0.12 queue text remain
  consistent with GitHub.
- No normative ESAF Markdown, schemas, or mappings change in this issue.

## Boundaries

This issue does not change normative ESAF content, complete qualified UK
review, close Issue #55 by owner-risk acceptance, clear HITRUST/PCI/NIST/
ISO/IEC 42001 blockers, or claim certification, compliance, equivalence,
endorsement, or assurance.
```

---

## Task 5: Ready-to-file Issue B - NIST CSF 2.0 readiness

Title: `Complete NIST CSF 2.0 public-source readiness and mapping go/no-go`

Labels: `crosswalk`, `priority:high`

```markdown
## Purpose

Complete NIST CSF 2.0 public-source readiness and record a mapping go/no-go
decision after `v0.12-draft`. The default acceptable exit is an evidenced
`HOLD` when people, rights, or source-access gates remain blocked. A
matrix-derived `GO` is permitted only if every readiness gate clears before
publication.

## Dependencies

Depends on merged `v0.13-draft` planning records and tracker hygiene. May
overlap ESAF-1200 deepen, but must finish before publication gates.

## Deliverables

- Pin official NIST CSF 2.0 source identity, version, publication date, and
  obtainable checksums.
- Record publication-rights boundary and provision-inventory feasibility
  without reproducing restricted requirement text.
- Assess named mapper and independent qualified-review availability.
- Produce mechanical readiness matrix and generated GO/HOLD/NO_GO review.
- Landing page under `crosswalks/` plus issue traceability.
- If any readiness gate fails, record evidenced `HOLD` or `NO_GO` that restates
  blockers, owners, reconsideration triggers, re-entry tests, and nonclaims.
- While the decision remains `HOLD` or `NO_GO`, create no NIST CSF mapping
  records, negative dispositions, snapshots, lifecycle events, registry
  entries, or catalog increments.

## Acceptance criteria

- Readiness decision is recorded as evidenced `GO`, `HOLD`, or `NO_GO`.
- If `HOLD` or `NO_GO`, NIST CSF mapping artifact count remains `0` and
  generated crosswalk catalog counts are unchanged by this issue.
- Focused crosswalk/readiness validators and affected link checks pass on the
  exact candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue does not authorize NIST CSF mapping authorship under `HOLD` or
`NO_GO`, clear HITRUST / PCI DSS / NIST AI RMF / ISO/IEC 42001 blockers,
close Issue #55, or claim certification, compliance, equivalence, endorsement,
assurance, or production readiness.
```

---

## Task 6: Ready-to-file Issue C - ESAF-1200 deepen

Title: `Deepen ESAF-1200 Reference Architecture Working Draft`

Labels: `architecture`, `priority:high`

```markdown
## Purpose

Complete a bounded Working Draft deepen of ESAF-1200 so method text,
cross-links to patterns / trust zones / selection, and revision history stay
aligned after `v0.12-draft`.

## Dependencies

Depends on merged `v0.13-draft` planning records and tracker hygiene. May
proceed in parallel with NIST CSF 2.0 readiness.

## Deliverables

- Synchronize cross-links from `architectures/ESAF-1200.md` to patterns, trust
  zones, and pattern-selection surfaces.
- Align architecture-method wording for consistency with related architecture
  indexes.
- Bump revision history to record the deepen; keep status Working Draft.
- Do not add new architecture patterns or expand the pattern population.

## Acceptance criteria

- ESAF-1200 deepen is Draft-labeled with revision-history evidence.
- No new architecture patterns are introduced.
- Focused architecture validators and affected link checks pass on the exact
  candidate.
- Critical and Important findings are resolved.

## Boundaries

This issue does not redesign `v1.0`, invent certification requirements, advance
lifecycle states, add new patterns, or claim compliance, equivalence,
endorsement, or assurance.
```

---

## Task 7: Ready-to-file Issue D - v0.13-draft publication gates

Title: `Close the v0.13-draft publication gates`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Close the ordinary `v0.13-draft` release gates on one exact release candidate
after tracker hygiene, NIST CSF 2.0 readiness, and ESAF-1200 deepen are
complete.

## Dependencies

Depends on completion of:

- Sync post-v0.12 tracker hygiene;
- Complete NIST CSF 2.0 public-source readiness and mapping go/no-go; and
- Deepen ESAF-1200 Reference Architecture Working Draft.

Issues #55 and #60 may remain open. They are not `v0.13-draft` exit criteria.

## Deliverables

- Exact-candidate technical, editorial, and governance reviews.
- Full test suite, control, architecture, assessment, profile, crosswalk, link,
  release, working-tree, and applicable Mermaid-rendering gates.
- Synchronized README, VERSION, changelog, roadmap, release plan, backlog,
  milestones, and readiness record.
- Annotated tag `v0.13-draft` and consolidated publication evidence bound to
  the exact candidate SHA.

## Acceptance criteria

- Every `v0.13-draft` exit criterion in `project/MILESTONES.md` is satisfied.
- Critical and Important findings are resolved.
- Post-merge validation passes before any immutable tag or publication
  statement is created.

## Boundaries

Publication remains a Working Draft. It does not complete qualified UK mapping
review, clear HITRUST / PCI DSS / NIST AI RMF / ISO/IEC 42001 / NIST CSF
blockers, approve Draft artifact lifecycle transitions without their own
evidence, or establish certification, compliance, equivalence, endorsement,
external-scheme approval, assurance, or production readiness.
```
