# ESAF v0.16-draft Next-Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land durable `v0.16-draft` milestone, backlog, and roadmap records plus ready-to-file issue bodies for post-v0.15 tracker hygiene, NIST SP 800-53 Revision 5 public-source readiness (default evidenced `HOLD`), bounded UK jurisdiction profile deepen to Draft `0.2.0`, and publication gates.

**Architecture:** Keep `v0.15-draft` publication identity and Draft lifecycle states intact. Add a bounded `## v0.16-draft` milestone section mirroring `v0.15-draft`, a post-v0.15 backlog queue, a roadmap delivery sequence, and pinned issue-body fixtures in this plan for later GitHub filing. Do not author NIST SP 800-53 readiness artifacts, deepen the UK profile, reopen/close GitHub issues, or publish a tag in this planning change. Approach C (SOC 2 / CIS Controls + Phase 6 third deepen) is deferred to the next milestone.

**Tech Stack:** Markdown project records, `unittest` release-metadata invariants.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-16-v016-draft-next-steps-design.md`
- Milestone identity: `v0.16-draft` (Working Draft tag name when later published)
- Sequence: tracker hygiene → NIST SP 800-53 readiness → UK profile deepen → publication gates
- Issues `#55` / `#60` are not `v0.16-draft` blockers after hygiene
- NIST SP 800-53 default exit is evidenced `HOLD`; no mapping records while `HOLD` or `NO_GO`
- Clone the NIST public-PDF inventory shape (CSF / AI RMF), not the ISO copyright-blocked shape
- UK profile deepen remains Draft `0.2.0` under ESAF-1800; no second profile; no imported mapping outcomes
- Do not execute Approach C inside this milestone
- Do not redesign `v1.0` or open all of roadmap Phases 4–6
- Digests: compute each `PINNED_V016_ISSUE_*_BODY_SHA256` from the final fenced markdown body under the matching line-anchored `^## Task N:` heading via `sha256` of that fenced body

---

### Task 1: Lock planning invariants with failing tests

**Files:**
- Modify: `tests/test_release_metadata.py`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: existing helpers `read_repository_file`, `markdown_section`,
  `contains_normalized_phrase`, `fenced_markdown_in_task`, `sha256_text`,
  `milestone_section`
- Produces: constants `V016_NEXT_STEPS_PLAN`, `V016_READY_ISSUE_TASKS`, and
  four `PINNED_V016_ISSUE_*_BODY_SHA256` digests

- [ ] **Step 1: Add plan path, digest constants, and ready-issue table**

Near the existing `V015_NEXT_STEPS_PLAN` constants, add a plan-path constant
pointing at this file, four `PINNED_V016_ISSUE_*_BODY_SHA256` values, and a
`V016_READY_ISSUE_TASKS` tuple that mirrors `V015_READY_ISSUE_TASKS` with four
entries.

Use the exact Task 4–7 headings and titles already written later in this plan.
Required phrases per issue:

- Issue A: `reopen Issue #55`, `Issues #181`, `does not change normative`
- Issue B: `NIST SP 800-53`, `HOLD`, `mapping records`
- Issue C: `United Kingdom`, `0.2.0`, `Draft`
- Issue D: `Issues #55 and #60 may remain open`, `Every \`v0.16-draft\` exit criterion`, `Working Draft`

Also update `test_hitrust_backlog_links_open_issue_60` so the expected phrase
includes `v0.16-draft`.

- [ ] **Step 2: Add failing milestone / backlog / roadmap / digest tests**

Add five tests on `ReleaseMetadataTests` that assert:

1. `project/MILESTONES.md` contains `## v0.16-draft` with headings
   `### Entry state`, `### Required workstreams`, `### Exit criteria`,
   `### Non-goals`, and the workstream / exit phrases listed in Task 2
   (`Tracker hygiene`, `NIST SP 800-53`, `United Kingdom jurisdiction profile deepen`,
   `Release closure`, `Issues \`#181\`–\`#185\``,
   `Critical and Important`).
2. The `### Non-goals` subsection includes: closing Issue `#55`, substantive
   HITRUST mapping, PCI DSS `HOLD`, NIST AI RMF `HOLD`, ISO/IEC 42001 `HOLD`,
   NIST CSF `HOLD`, ISO/IEC 27001 `HOLD`, SOC 2 or CIS Controls readiness,
   third Phase 6 toolkit deepen, second industry or jurisdiction profile,
   all roadmap crosswalks, all planned profiles, redesigning `v1.0`.
3. `project/BACKLOG.md` section `## Post-v0.15 scheduled queue` lists the four
   initiative titles from Task 2 and says they do not stop later engineering
   work.
4. `ROADMAP.md` section `## 0.16-draft delivery sequence` covers tracker
   hygiene, NIST SP 800-53, United Kingdom, issues 55/60, not exit
   criteria, evidenced `HOLD`, and Phases 4/5/6 long-term direction.
5. Each `V016_READY_ISSUE_TASKS` entry has `Title: \`...\`` in this plan, a
   fenced body matching the pinned digest via `fenced_markdown_in_task` +
   `sha256_text`, required phrases present, and no `closes issue 55` phrase.

- [ ] **Step 3: Run focused tests and confirm they fail before content lands**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v016 -v
```

Expected: FAIL (missing `## v0.16-draft` / queue / digests) when run before
Tasks 2–3 land; after Task 2, digest pin may still fail until Task 3.

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/test_release_metadata.py
git commit -m "test: require v0.16-draft planning invariants"
```

---

### Task 2: Update durable project records

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add `## v0.16-draft` to milestones**

Append after the `v0.15-draft` section (do not rewrite closed publication truth).

- [ ] **Step 2: Add `## Post-v0.15 scheduled queue` to the backlog**

Insert after `## Post-v0.14 scheduled queue`. List:

- Sync post-v0.15 tracker hygiene
- Complete NIST SP 800-53 Revision 5 public-source readiness and mapping go/no-go
- Deepen United Kingdom jurisdiction profile to Draft 0.2.0
- Close the v0.16-draft publication gates

Also extend the HITRUST backlog line so it states the work does not block
through `v0.16-draft`.

- [ ] **Step 3: Add `## 0.16-draft delivery sequence` to the roadmap**

Insert before `## 0.15-draft delivery sequence`.

- [ ] **Step 4: Commit durable records**

```bash
git add project/MILESTONES.md project/BACKLOG.md ROADMAP.md
git commit -m "docs: define v0.16-draft milestone and post-v0.15 queue"
```

---

### Task 3: Pin issue-body digests, validate, and open the pull request

**Files:**
- Modify: `tests/test_release_metadata.py`

- [ ] **Step 1: Compute digests from this plan's fenced bodies**

Pinned digests for the bodies in this plan:

- Issue A: `c5893b6e74b97a00cb8442ae1f5b880628ff97a0e4285312694048a8ec04a78d`
- Issue B: `f9f86fcb0e6585c34d22fc44922fdc3035ab49024195983a1013711418b4e66e`
- Issue C: `fa60a3ef92c57ba48dad5e1c65fed6fb667db1feab425e3d550b72f271b73dbf`
- Issue D: `cbb539392cfa83dde9951cc4c98c5f695ab7d86d37b63d74882f0e41a171f925`

These digests are the exact `sha256_text` of each fenced markdown body
under Tasks 4–7.

- [ ] **Step 2: Run focused tests and `git diff --check`**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v016 -v
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
  docs/superpowers/plans/2026-09-16-v016-draft-next-steps.md \
  docs/superpowers/specs/2026-09-16-v016-draft-next-steps-design.md
git commit -m "docs: plan v0.16-draft next steps and pin issue bodies"
git push -u origin HEAD
```

Open or update a draft PR against `main` describing planning-only scope.
Do not create the four GitHub issues or edit GitHub tracker state in this
planning change; filing happens after the planning PR merges.

---

## Task 4: Ready-to-file Issue A - tracker hygiene

Title: `Sync post-v0.15 tracker hygiene`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Restore GitHub tracker state so it matches post-`v0.15-draft` repository truth
before `v0.16-draft` content work begins.

## Dependencies

Depends on the merged `v0.16-draft` planning records. Blocks filing or starting
content issues only insofar as milestone/`#55` truth must be corrected first.
Does not depend on Issue #60 content work.

## Deliverables

- Reopen Issue #55 if qualified UK mapping review remains outstanding, with a
  short comment stating owner-risk acceptance did not complete qualified review.
- Close or explicitly annotate Issues #181–#185 as historical completed
  `v0.15-draft` work, linking the published tag evidence where useful.
- Close GitHub milestone `v0.15-draft` when it has no open issues; open GitHub
  milestone `v0.16-draft`.
- Align GitHub milestone membership and `project/BACKLOG.md` wording with the
  durable records.
- Record the resulting open/closed matrix in the issue comments.

## Acceptance criteria

- Repository policy and GitHub agree on Issue #55 open/closed state.
- Issues #181–#185 are closed or clearly marked historical completed work.
- GitHub milestone `v0.15-draft` is closed when empty; milestone `v0.16-draft`
  exists.
- `project/BACKLOG.md` deferred-assurance and post-v0.15 queue text remain
  consistent with GitHub.
- No normative ESAF Markdown, schemas, or mappings change in this issue.

## Boundaries

This issue does not change normative ESAF content, complete qualified UK
review, close Issue #55 by owner-risk acceptance, clear HITRUST/PCI/NIST/
ISO/IEC 42001/NIST CSF/ISO/IEC 27001 blockers, open unauthorized mapping
authorship, or claim certification, compliance, equivalence, endorsement, or
assurance. Tracker hygiene does not change normative content.
```

---

## Task 5: Ready-to-file Issue B - NIST SP 800-53 readiness

Title: `Complete NIST SP 800-53 Revision 5 public-source readiness and mapping go/no-go`

Labels: `crosswalk`, `priority:high`

```markdown
## Purpose

Complete NIST SP 800-53 Revision 5 public-source readiness and a mapping
go/no-go decision for ESAF without creating unauthorized mapping records.

## Dependencies

Depends on merged `v0.16-draft` planning records and tracker hygiene. May
overlap UK profile deepen. Must finish before publication gates.

## Deliverables

- Pin the official NIST SP 800-53 Revision 5 source identity (title, edition,
  publisher, locator) and checksums where obtainable.
- Record the publication-rights boundary and provision-inventory feasibility
  using the NIST public-PDF inventory shape (clone CSF / AI RMF packaging).
- Assess named mapper and independent qualified-reviewer availability.
- Produce a mechanical readiness matrix and an evidenced `GO` / `HOLD` /
  `NO_GO` decision package under `docs/superpowers/` plus landing page
  `crosswalks/nist-sp-800-53.md`.
- Default acceptable exit is evidenced `HOLD` when people, rights, or
  source-access gates remain blocked.

## Acceptance criteria

- NIST SP 800-53 readiness decision is recorded as `GO`, `HOLD`, or `NO_GO`
  with blockers, owners, reconsideration triggers, re-entry tests, and
  nonclaims.
- While the decision is `HOLD` or `NO_GO`, NIST SP 800-53 mapping records,
  snapshots, lifecycle events, registry entries, and catalog increments remain
  absent (`0` mapping artifacts for the scheme).
- Focused readiness tests and renderers pass; whole-branch release-metadata
  invariants remain green.
- No certification, compliance, equivalence, endorsement, or assurance claim.

## Boundaries

This issue does not author NIST SP 800-53 mapping records under `HOLD` or
`NO_GO`, clear prior NIST AI RMF / NIST CSF / ISO/IEC 42001 / ISO/IEC 27001 /
PCI DSS HOLDs, close Issue #55, perform HITRUST work, execute SOC 2 or CIS
Controls readiness, or establish certification. Clone the NIST public-PDF
inventory shape; do not invent restricted provision text.
```

---

## Task 6: Ready-to-file Issue C - UK profile deepen

Title: `Deepen United Kingdom jurisdiction profile to Draft 0.2.0`

Labels: `profile`, `priority:high`

```markdown
## Purpose

Complete a bounded Draft deepen of the United Kingdom jurisdiction profile
from `0.1.0` to `0.2.0` under ESAF-1800 while remaining Draft.

## Dependencies

Depends on merged `v0.16-draft` planning records and tracker hygiene. May
overlap NIST SP 800-53 readiness. Must finish before publication gates.

## Deliverables

- Author versioned package `profiles/uk/0.2.0/` with authoritative `PROFILE.md`,
  README, and derived JSON components synchronized exactly.
- Update `profiles/README.md` index to discover Draft `0.2.0` while retaining
  historical `0.1.0` package truth as required by ESAF-1800 versioning.
- Keep lifecycle Draft; preserve ESAF control meanings; retain ESAF-1500 shared
  assessment semantics.
- Keep ESAF-1600 composition limited to pinned UK mapping identity without
  importing mapping outcomes, relationships, or external interpretations.
- Extend focused profile validation tests for the `0.2.0` deepen invariants.

## Acceptance criteria

- UK jurisdiction profile reports Draft `0.2.0` with change-history evidence
  and remains Draft.
- Control meanings are preserved; no imported mapping outcomes; no
  external-scheme compliance or certification claims.
- Profile validators and focused tests pass; Critical and Important findings
  are resolved.
- No second industry or jurisdiction profile is introduced.

## Boundaries

This issue does not redesign `v1.0`, invent certification requirements, advance
lifecycle states beyond Draft, open a second profile, clear readiness HOLDs,
author crosswalk mapping records, break ESAF-1500 or ESAF-1800 contracts, or
claim compliance, equivalence, endorsement, or assurance.
```

---

## Task 7: Ready-to-file Issue D - v0.16-draft publication gates

Title: `Close the v0.16-draft publication gates`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Close the ordinary `v0.16-draft` release gates on one exact release candidate
after tracker hygiene, NIST SP 800-53 readiness, and UK profile deepen are
complete.

## Dependencies

Depends on completion of:

- Sync post-v0.15 tracker hygiene;
- Complete NIST SP 800-53 Revision 5 public-source readiness and mapping go/no-go; and
- Deepen United Kingdom jurisdiction profile to Draft 0.2.0.

Issues #55 and #60 may remain open. They are not `v0.16-draft` exit criteria.

## Deliverables

- Exact-candidate technical, editorial, and governance reviews.
- Full test suite, control, architecture, assessment, profile, crosswalk, link,
  release, working-tree, and applicable Mermaid-rendering gates.
- Synchronized README, VERSION, changelog, roadmap, release plan, backlog,
  milestones, and readiness record.
- Annotated tag `v0.16-draft` and consolidated publication evidence bound to
  the exact candidate SHA.

## Acceptance criteria

- Every `v0.16-draft` exit criterion in `project/MILESTONES.md` is satisfied.
- Critical and Important findings are resolved.
- Post-merge validation passes before any immutable tag or publication
  statement is created.
- Publication remains a Working Draft.

## Boundaries

Publication remains a Working Draft. It does not complete qualified UK mapping
review, clear HITRUST / PCI DSS / NIST AI RMF / ISO/IEC 42001 / NIST CSF /
ISO/IEC 27001 blockers, authorize NIST SP 800-53 mapping authorship under
`HOLD` or `NO_GO`, execute Approach C (SOC 2 / CIS Controls or third Phase 6
toolkit deepen), approve Draft artifact lifecycle transitions without their
own evidence, or establish certification, compliance, equivalence, endorsement,
external-scheme approval, assurance, or production readiness.
```
