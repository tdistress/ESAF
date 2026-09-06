# ESAF v0.11-draft Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-09-06

## 1. Purpose

Convert the post-`v0.10-draft` planning gap into a bounded `v0.11-draft`
milestone whose ordered headline deliverables are (1) a Phase 6 assessment
toolkit deepen of the existing Draft starters and (2) a NIST AI RMF readiness
re-entry that may exit as a refreshed evidenced `HOLD`.

This change shall:

- leave `v0.10-draft` publication identity, annotated-tag evidence, and Draft
  lifecycle states for controls, architectures, profiles, and mappings
  unchanged;
- define measurable `v0.11-draft` entry conditions, workstreams, exit
  criteria, and non-goals;
- record the post-v0.10 engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for hygiene, toolkit deepen, NIST
  readiness re-entry, and publication workstreams.

## 2. Current state

The annotated tag `v0.10-draft` is published (2026-09-05) at peel commit
`05b7ebdd588d9959412fce1d2d4d9bdf663e998e`. Issues `#114`–`#119` are closed.
Open GitHub issues are limited to:

- `#55` — qualified human review of the three UK mapping snapshots; and
- `#60` — HITRUST CSF source and review readiness.

Both remain externally gated and are not `v0.11-draft` blockers.

Phase 6 Draft starters exist and remain thin by design:

- `assessment/workbook/` — operator guide plus blank schema-valid worksheets;
- `assessment/evidence-catalog/` — type index and quality attributes without
  per-type worked samples;
- `assessment/audit-checklist/` — blank sampling grids without a vignette; and
- `templates/` — blank risk, exception, decision, and retirement forms.

ESAF-1500 remains the authoritative shared evidence, assessment-result, and
maturity foundation. Toolkit packs must not invent parallel contracts.

NIST AI RMF readiness remains an evidenced `HOLD` under
`crosswalks/nist-ai-rmf.md`, with mechanical package artifacts under
`docs/superpowers/specs/` and `docs/superpowers/reviews/`. The sole recorded
blocker is named qualified mapper and independent exact-candidate reviewer
evidence (`NIST-AI-RMF-READINESS-B001`). Source identity, public PDF digests,
publication rights, the 72-subcategory inventory, semantic feasibility,
ESAF-1600 schema fit, and overclaiming controls already pass. Issue `#94` was
closed through the evidenced-`HOLD` path; a readiness re-entry does not reopen
that historical disposition as incomplete.

There is no approved `v1.0` redesign. Roadmap Phases 4 and 5 remain long-term
direction. Phase 6 remains long-term direction except for the bounded deepen
required by this milestone.

## 3. Selected approach

Follow the proven next-steps pattern: planning records and ready-to-file
issues first, then a bounded usability content theme, then a fail-closed
readiness refresh, with version identity **`v0.11-draft`**.

Ordered themes:

1. **Toolkit deepen** — make the four Draft starters usable through worked
   fictional examples and filled informative instances, without expanding into
   a certification program or full Phase 6 library.
2. **NIST AI RMF readiness re-entry** — refresh the readiness package; default
   exit is a refreshed evidenced `HOLD` because named mapper and independent
   reviewers are not available. A matrix-derived `GO` is permitted only if
   complete people evidence appears before publication. Mapping records remain
   out of scope while the decision is `HOLD`.

Do not open all of roadmap Phases 4–6. Do not redesign `v1.0`. Do not treat
Issues `#55` or `#60` as exit criteria.

Execution order:

1. Land durable milestone / backlog / roadmap records and pinned issue bodies.
2. Complete tracker hygiene so GitHub matches repository truth.
3. Deepen the four toolkit packs (parallelizable after hygiene).
4. Complete NIST AI RMF readiness re-entry (after or overlapping toolkit deepen;
   must finish before publication gates).
5. Close ordinary publication gates on one exact `v0.11-draft` candidate.

## 4. Milestone shape

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

1. **Tracker hygiene.** ESAF shall ensure Issue `#55` is open if and only if
   qualified UK mapping review remains outstanding, close or explicitly
   annotate Issues `#114`–`#119` as historical completed `v0.10-draft` work,
   and align `project/BACKLOG.md` and GitHub milestone state with published
   truth. This workstream does not change normative content.
2. **Assessment workbook deepen.** ESAF shall add one worked fictional
   engagement under `assessment/` or `examples/` with scope narrative and a
   filled worksheet trio bound to ESAF-1500 schemas and ESAF-1100 procedures,
   while keeping pack status Draft and worksheets schema-valid.
3. **Evidence catalog deepen.** ESAF shall add short per-type quality notes
   (good-enough versus common-failure) and a small set of fictional filled
   evidence records keyed to catalog types, remaining profile-neutral and
   bound to the ESAF-1500 evidence contract.
4. **Audit checklist deepen.** ESAF shall add one small sampling vignette
   (approximately two to three controls) with procedure IDs, methods,
   evidence references, and determinations against the shared
   assessment-result vocabulary, without authoring a full control-family
   library.
5. **Governance templates deepen.** ESAF shall add one filled informative
   instance per template class (risk, exception, decision, retirement) under
   `examples/` or an adjacent informative path, linked from `templates/` and
   ESAF-1300 / ESAF-1400 without adding new normative `shall` requirements.
6. **NIST AI RMF readiness re-entry.** ESAF shall refresh the NIST AI RMF
   readiness package (oracle, rights boundary, inventory, matrix, generated
   decision, landing page, and issue traceability as applicable). The default
   acceptable exit is a refreshed evidenced `HOLD` that restates blockers,
   owners, reconsideration triggers, re-entry tests, and nonclaims. A
   matrix-derived `GO` is allowed only when named mapper and independent
   reviewer evidence fully clears the people gate. While the decision remains
   `HOLD`, ESAF shall not create NIST mapping relationships, negative
   dispositions, snapshots, lifecycle events, registry entries, or catalog
   increments.
7. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.11-draft` candidate, publish annotated tag `v0.11-draft`, and
   synchronize Working Draft status surfaces.

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
  artifact count remains `0` and the generated crosswalk catalog counts are
  unchanged by this workstream;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.11-draft` is published and Working Draft surfaces
  (`VERSION.md`, README badges, changelog, roadmap, backlog, milestones, and
  readiness record) are synchronized.

### Non-goals

`v0.11-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping (Issue `#60`);
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` when named mapper and independent reviewers
  remain unavailable;
- authoring NIST AI RMF mapping records, snapshots, or catalog entries;
- a complete Phase 6 workbook, evidence library, audit-checklist library, or
  template library;
- all roadmap crosswalks or all planned industry profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.

## 5. Backlog and roadmap updates

`project/BACKLOG.md` shall add a post-v0.10 queue that lists the seven
workstreams above, while retaining:

- deferred assurance follow-up for Issue `#55`;
- separately gated HITRUST readiness for Issue `#60`; and
- completed `v0.10-draft` toolkit-starter and publication workstreams as
  historical context.

`ROADMAP.md` shall add a `0.11-draft` delivery sequence that states the order
of work (hygiene → toolkit deepen → NIST readiness re-entry → publication) and
that Phases 4 and 5 remain long-term direction. Phase 6 remains long-term
direction except for the bounded deepen required by this milestone. Deferred
mapping assurance and HITRUST readiness remain tracked and do not stop later
engineering work. NIST readiness re-entry may exit as refreshed `HOLD`.

`project/MILESTONES.md` shall add a `## v0.11-draft` section mirroring the
`v0.10-draft` structure (entry state, required workstreams, exit criteria,
non-goals).

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Sync post-v0.10 tracker hygiene
2. Deepen assessment workbook Draft pack
3. Deepen evidence catalog Draft pack
4. Deepen audit checklist Draft pack
5. Deepen governance templates Draft pack
6. Refresh NIST AI RMF readiness package
7. Close the v0.11-draft publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist.

Issues 2–5 may proceed in parallel after hygiene acceptance criteria are met.
Issue 6 may proceed after hygiene and may overlap Issues 2–5, but shall finish
before Issue 7. Issue 7 depends on Issues 2–6.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS / HITRUST / NIST AI RMF
blockers, authorize NIST mapping authorship under `HOLD`, or establish
certification, compliance, equivalence, endorsement, assurance, or production
readiness. Toolkit deepen artifacts produced under this milestone remain Draft
Working Draft material only. A refreshed NIST `HOLD` is an evidenced readiness
disposition, not a mapping, approval, or assurance claim.
