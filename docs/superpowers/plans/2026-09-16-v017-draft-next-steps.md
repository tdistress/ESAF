# ESAF v0.17-draft Next-Steps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land durable `v0.17-draft` milestone, backlog, and roadmap records plus ready-to-file issue bodies for post-v0.16 tracker hygiene, CIS Controls Version 8 public-source readiness (default evidenced `HOLD`), bounded third Phase 6 toolkit deepen, and publication gates.

**Architecture:** Keep `v0.16-draft` publication identity and Draft lifecycle states intact. Add a bounded `## v0.17-draft` milestone section mirroring `v0.16-draft`, a post-v0.16 backlog queue, a roadmap delivery sequence, and pinned issue-body fixtures in this plan for later GitHub filing. Do not author CIS Controls readiness artifacts, deepen Phase 6 packs, reopen/close GitHub issues, or publish a tag in this planning change. SOC 2 readiness remains a separately gated follow-on outside this milestone.

**Tech Stack:** Markdown project records, `unittest` release-metadata invariants.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-16-v017-draft-next-steps-design.md`
- Milestone identity: `v0.17-draft` (Working Draft tag name when later published)
- Sequence: tracker hygiene → CIS Controls readiness → Phase 6 third toolkit deepen → publication gates
- Issues `#55` / `#60` are not `v0.17-draft` blockers after hygiene
- CIS Controls default exit is evidenced `HOLD`; no mapping records while `HOLD` or `NO_GO`
- Clone the NIST public-PDF inventory shape (CSF / AI RMF / SP 800-53), not the ISO copyright-blocked shape
- Phase 6 third deepen remains Draft across workbook, evidence catalog, audit checklist, and governance templates; no complete assessment library
- Do not author a SOC 2 readiness package inside this milestone
- Do not redesign `v1.0` or open all of roadmap Phases 4–6
- Digests: compute each `PINNED_V017_ISSUE_*_BODY_SHA256` from the final fenced markdown body under the matching line-anchored `^## Task N:` heading via `sha256` of that fenced body

---

### Task 1: Lock planning invariants with failing tests

**Files:**
- Modify: `tests/test_release_metadata.py`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: existing helpers `read_repository_file`, `markdown_section`,
  `contains_normalized_phrase`, `fenced_markdown_in_task`, `sha256_text`,
  `milestone_section`
- Produces: constants `V017_NEXT_STEPS_PLAN`, `V017_READY_ISSUE_TASKS`, and
  four `PINNED_V017_ISSUE_*_BODY_SHA256` digests

- [ ] **Step 1: Add plan path, digest constants, and ready-issue table**

Near the existing `V016_NEXT_STEPS_PLAN` constants, add a plan-path constant
pointing at this file, four `PINNED_V017_ISSUE_*_BODY_SHA256` values, and a
`V017_READY_ISSUE_TASKS` tuple that mirrors `V016_READY_ISSUE_TASKS` with four
entries.

Use the exact Task 4–7 headings and titles already written later in this plan.
Required phrases per issue:

- Issue A: `reopen Issue #55`, `Issues #193`, `does not change normative`
- Issue B: `CIS Controls`, `HOLD`, `mapping records`
- Issue C: `Phase 6`, `third`, `Draft`
- Issue D: `Issues #55 and #60 may remain open`, `Every \`v0.17-draft\` exit criterion`, `Working Draft`

Also update `test_hitrust_backlog_links_open_issue_60` so the expected phrase
includes `v0.17-draft`.

- [ ] **Step 2: Add failing milestone / backlog / roadmap / digest tests**

Add five tests on `ReleaseMetadataTests` that assert:

1. `project/MILESTONES.md` contains `## v0.17-draft` with headings
   `### Entry state`, `### Required workstreams`, `### Exit criteria`,
   `### Non-goals`, and the workstream / exit phrases listed in Task 2
   (`Tracker hygiene`, `CIS Controls`, `Phase 6 toolkit deepen`,
   `Release closure`, `Issues \`#193\`–\`#196\``,
   `Critical and Important`).
2. The `### Non-goals` subsection includes: closing Issue `#55`, substantive
   HITRUST mapping, PCI DSS `HOLD`, NIST AI RMF `HOLD`, ISO/IEC 42001 `HOLD`,
   NIST CSF `HOLD`, ISO/IEC 27001 `HOLD`, NIST SP 800-53 `HOLD`, SOC 2
   readiness package, second industry or jurisdiction profile, all roadmap
   crosswalks, all planned profiles, redesigning `v1.0`.
3. `project/BACKLOG.md` section `## Post-v0.16 scheduled queue` lists the four
   initiative titles from Task 2 and says they do not stop later engineering
   work.
4. `ROADMAP.md` section `## 0.17-draft delivery sequence` covers tracker
   hygiene, CIS Controls, Phase 6, issues 55/60, not exit criteria, evidenced
   `HOLD`, and Phases 4/5/6 long-term direction.
5. Each `V017_READY_ISSUE_TASKS` entry has `Title: \`...\`` in this plan, a
   fenced body matching the pinned digest via `fenced_markdown_in_task` +
   `sha256_text`, required phrases present, and no `closes issue 55` phrase.

- [ ] **Step 3: Run focused tests and confirm they fail before content lands**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v017 -v
```

Expected: FAIL (missing `## v0.17-draft` / queue / digests) when run before
Tasks 2–3 land; after Task 2, digest pin may still fail until Task 3.

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/test_release_metadata.py
git commit -m "test: require v0.17-draft planning invariants"
```

---

### Task 2: Update durable project records

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add `## v0.17-draft` to milestones**

Append after the `v0.16-draft` section (do not rewrite closed publication truth).

- [ ] **Step 2: Add `## Post-v0.16 scheduled queue` to the backlog**

Insert after `## Post-v0.15 scheduled queue`. List:

- Sync post-v0.16 tracker hygiene
- Complete CIS Controls Version 8 public-source readiness and mapping go/no-go
- Deepen Phase 6 assessment toolkit Draft packs (third pass)
- Close the v0.17-draft publication gates

Also extend the HITRUST backlog line so it states the work does not block
`v0.17-draft`, and add a separately gated SOC 2 follow-on note under
`## Separately gated future work`.

- [ ] **Step 3: Add `## 0.17-draft delivery sequence` to the roadmap**

Insert before the `0.16-draft` delivery sequence. State hygiene → CIS Controls
readiness → Phase 6 third toolkit deepen → publication; Issues 55/60 are not
exit criteria; CIS Controls may exit evidenced `HOLD`; Phases 4/5/6 remain
long-term direction except for this milestone's bounded work; SOC 2 remains
outside this milestone.

- [ ] **Step 4: Commit project records**

```bash
git add project/MILESTONES.md project/BACKLOG.md ROADMAP.md
git commit -m "docs: record v0.17-draft milestone queue and roadmap"
```

---

### Task 3: Pin ready-to-file issue digests

**Files:**
- Modify: `tests/test_release_metadata.py` (digest constants only, if needed)
- This plan file already contains Task 4–7 bodies

- [ ] **Step 1: Compute digests from the Task 4–7 fenced bodies**

```bash
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
from pathlib import Path
import hashlib, re
plan = Path("docs/superpowers/plans/2026-09-16-v017-draft-next-steps.md").read_text()
for heading in (
    "## Task 4: Ready-to-file Issue A - tracker hygiene",
    "## Task 5: Ready-to-file Issue B - CIS Controls readiness",
    "## Task 6: Ready-to-file Issue C - Phase 6 third deepen",
    "## Task 7: Ready-to-file Issue D - v0.17-draft publication gates",
):
    m = re.search(rf"(?m)^{re.escape(heading)}\n", plan)
    assert m, heading
    rest = plan[m.end():]
    fence = re.search(r"```markdown\n(.*?)```", rest, re.S)
    body = fence.group(1)
    print(heading, hashlib.sha256(body.encode()).hexdigest())
PY
```

- [ ] **Step 2: Set `PINNED_V017_ISSUE_*_BODY_SHA256` to those digests**

- [ ] **Step 3: Run focused tests green**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_release_metadata -k v017 -v
```

- [ ] **Step 4: Commit digest pins**

```bash
git add tests/test_release_metadata.py
git commit -m "test: pin v0.17-draft ready-issue body digests"
```

---

## Task 4: Ready-to-file Issue A - tracker hygiene

Title: `Sync post-v0.16 tracker hygiene`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Align GitHub Issues and milestones with published `v0.16-draft` truth without
changing normative ESAF content.

## Dependencies

Depends on merged `v0.17-draft` planning records on `main`. Must finish before
CIS Controls readiness, Phase 6 third deepen, and publication gates.

## Deliverables

- Confirm Issue #55 remains open if and only if qualified UK mapping review is
  still outstanding; reopen Issue #55 only when that review remains incomplete
  and the issue was closed incorrectly.
- Close or explicitly annotate Issues #193–#196 as historical completed
  `v0.16-draft` workstreams.
- Confirm GitHub milestone `v0.16-draft` is closed when it has no open issues.
- Open GitHub milestone `v0.17-draft` and assign the filed `v0.17-draft`
  workstream issues.
- Align `project/BACKLOG.md` issue links with published tracker truth.

## Acceptance criteria

- Issue #55 state matches qualified UK review reality.
- Issues #193–#196 are closed or explicitly annotated as historical.
- Milestone `v0.16-draft` is closed when empty; milestone `v0.17-draft` exists.
- Backlog links and labels match repository truth.
- This workstream does not change normative content.

## Boundaries

This issue does not author readiness packages, deepen Phase 6 packs, clear
HOLDs, close Issue #55 via owner-risk acceptance, perform HITRUST work, or
establish certification, compliance, equivalence, endorsement, or assurance.
```

---

## Task 5: Ready-to-file Issue B - CIS Controls readiness

Title: `Complete CIS Controls Version 8 public-source readiness and mapping go/no-go`

Labels: `crosswalk`, `priority:high`

```markdown
## Purpose

Complete CIS Controls Version 8 public-source readiness and a mapping go/no-go
decision for ESAF without creating unauthorized mapping records.

## Dependencies

Depends on merged `v0.17-draft` planning records and tracker hygiene. May
overlap Phase 6 third deepen. Must finish before publication gates.

## Deliverables

- Pin the official CIS Controls Version 8 source identity (title, edition,
  publisher, locator) and checksums where obtainable.
- Record the publication-rights boundary and provision-inventory feasibility
  using the NIST public-PDF inventory shape (clone CSF / AI RMF / SP 800-53
  packaging).
- Assess named mapper and independent qualified-reviewer availability.
- Produce a mechanical readiness matrix and an evidenced `GO` / `HOLD` /
  `NO_GO` decision package under `docs/superpowers/` plus landing page
  `crosswalks/cis-controls.md`.
- Default acceptable exit is evidenced `HOLD` when people, rights, or
  source-access gates remain blocked.

## Acceptance criteria

- CIS Controls readiness decision is recorded as `GO`, `HOLD`, or `NO_GO`
  with blockers, owners, reconsideration triggers, re-entry tests, and
  nonclaims.
- While the decision is `HOLD` or `NO_GO`, CIS Controls mapping records,
  snapshots, lifecycle events, registry entries, and catalog increments remain
  absent (`0` mapping artifacts for the scheme).
- Focused readiness tests and renderers pass; whole-branch release-metadata
  invariants remain green.
- No certification, compliance, equivalence, endorsement, or assurance claim.

## Boundaries

This issue does not author CIS Controls mapping records under `HOLD` or
`NO_GO`, clear prior NIST AI RMF / NIST CSF / NIST SP 800-53 / ISO/IEC 42001 /
ISO/IEC 27001 / PCI DSS HOLDs, close Issue #55, perform HITRUST work, author a
SOC 2 readiness package, or establish certification. Clone the NIST public-PDF
inventory shape; do not invent restricted provision text.
```

---

## Task 6: Ready-to-file Issue C - Phase 6 third deepen

Title: `Deepen Phase 6 assessment toolkit Draft packs (third pass)`

Labels: `assessment`, `priority:high`

```markdown
## Purpose

Complete a bounded third Draft deepen of the Phase 6 assessment toolkit packs
beyond the `v0.11-draft` and `v0.15-draft` deepen passes while remaining Draft
and bound to ESAF-1500 contracts.

## Dependencies

Depends on merged `v0.17-draft` planning records and tracker hygiene. May
overlap CIS Controls readiness. Must finish before publication gates.

## Deliverables

- Add operator-facing Draft examples or vignettes across assessment workbook,
  evidence catalog, audit checklist, and governance templates.
- Prefer covering remaining closed evidence types that lack filled catalog
  examples (`record`, `configuration`, `observation`, `contract`,
  `external_assurance`, and optionally `other`), plus one additional workbook
  engagement vignette, one additional audit sampling vignette, and one
  additional governance-template filled example or cross-template thread.
- Keep ESAF-1500 schema and field contracts unchanged; remain Draft; avoid
  certification claims.
- Extend focused assessment and template validation tests for the third-deepen
  invariants.

## Acceptance criteria

- Each of the four Phase 6 packs shows a bounded third deepen with Draft
  evidence beyond the second-deepen artifacts.
- Packs remain Draft and bound to ESAF-1500 contracts without certification,
  compliance, equivalence, endorsement, or assurance claims.
- Assessment validators and focused tests pass; Critical and Important findings
  are resolved.
- No complete Phase 6 assessment library is claimed or delivered.

## Boundaries

This issue does not redesign `v1.0`, invent certification requirements, advance
lifecycle states beyond Draft, break ESAF-1500 machine contracts, reopen
ESAF-1000 / 1100 / 1200 / 1300 / 1400 / 1500 / 1700 normative deepen, clear
readiness HOLDs, author crosswalk mapping records, or claim compliance,
equivalence, endorsement, or assurance.
```

---

## Task 7: Ready-to-file Issue D - v0.17-draft publication gates

Title: `Close the v0.17-draft publication gates`

Labels: `governance`, `priority:high`

```markdown
## Purpose

Close the ordinary `v0.17-draft` release gates on one exact release candidate
after tracker hygiene, CIS Controls readiness, and Phase 6 third deepen are
complete.

## Dependencies

Depends on completion of:

- Sync post-v0.16 tracker hygiene;
- Complete CIS Controls Version 8 public-source readiness and mapping go/no-go; and
- Deepen Phase 6 assessment toolkit Draft packs (third pass).

Issues #55 and #60 may remain open. They are not `v0.17-draft` exit criteria.

## Deliverables

- Exact-candidate technical, editorial, and governance reviews.
- Full test suite, control, architecture, assessment, profile, crosswalk, link,
  release, working-tree, and applicable Mermaid-rendering gates.
- Synchronized README, VERSION, changelog, roadmap, release plan, backlog,
  milestones, and readiness record.
- Annotated tag `v0.17-draft` and consolidated publication evidence bound to
  the exact candidate SHA.

## Acceptance criteria

- Every `v0.17-draft` exit criterion in `project/MILESTONES.md` is satisfied.
- Critical and Important findings are resolved.
- Post-merge validation passes before any immutable tag or publication
  statement is created.
- Publication remains a Working Draft.

## Boundaries

Publication remains a Working Draft. It does not complete qualified UK mapping
review, clear HITRUST / PCI DSS / NIST AI RMF / ISO/IEC 42001 / NIST CSF /
ISO/IEC 27001 / NIST SP 800-53 blockers, authorize CIS Controls mapping
authorship under `HOLD` or `NO_GO`, author a SOC 2 readiness package, approve
Draft artifact lifecycle transitions without their own evidence, or establish
certification, compliance, equivalence, endorsement, external-scheme approval,
assurance, or production readiness.
```
