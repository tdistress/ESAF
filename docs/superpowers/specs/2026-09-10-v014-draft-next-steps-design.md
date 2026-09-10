# ESAF v0.14-draft Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-09-10

## 1. Purpose

Convert the post-`v0.13-draft` planning gap into a bounded `v0.14-draft`
milestone whose ordered headline deliverables are (1) tracker hygiene after
`v0.13-draft` publication and (2) a bounded ESAF-1500 Assessment Guide Working
Draft deepen from `0.1.0` to `0.1.1`.

This change shall:

- leave `v0.13-draft` publication identity, annotated-tag evidence, and Draft
  lifecycle states for controls, architectures, profiles, and mappings
  unchanged;
- define measurable `v0.14-draft` entry conditions, workstreams, exit
  criteria, and non-goals;
- record the post-v0.13 engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for hygiene, ESAF-1500 deepen, and
  publication workstreams.

## 2. Current state

The annotated tag `v0.13-draft` is published (2026-09-07) at peel commit
`ea2af64bc6fc2fe377a07d70bfbda777520dde70`. Issues `#158`–`#161` are closed
completed `v0.13-draft` workstreams to be annotated as historical. Open GitHub
issues are limited to:

- `#55` — qualified human review of the three UK mapping snapshots; and
- `#60` — HITRUST CSF source and review readiness.

Both remain externally gated and are not `v0.14-draft` blockers.

Phase 6 Draft starters and deepen packs exist under `assessment/` and
`templates/` / `examples/`. ESAF-1500 remains the authoritative shared
evidence, assessment-result, and maturity foundation at Working Draft
`0.1.0`, with companion Draft toolkit packs (workbook, evidence catalog, and
audit checklist) under `assessment/`.

NIST AI RMF readiness remains an evidenced `HOLD` under
`crosswalks/nist-ai-rmf.md` (people gate). PCI DSS readiness remains an
evidenced `HOLD`. ISO/IEC 42001 readiness remains an evidenced `HOLD` under
`crosswalks/iso-iec-42001.md`. NIST CSF 2.0 readiness remains an evidenced
`HOLD` under `crosswalks/nist-csf.md` (people gate). No new readiness or
crosswalk workstream is opened by this milestone.

ESAF-1000 is Working Draft `0.2.1`. ESAF-1100 is Working Draft `0.3.1`.
ESAF-1200 is Working Draft `0.4.1`. Companion manuals ESAF-1300 / 1400 /
1700 remain at Working Draft `0.2.0` with example packs. Toolkit deepen from
`v0.11-draft`, the ESAF-1000 / ESAF-1100 deepen from `v0.12-draft`, and the
ESAF-1200 deepen from `v0.13-draft` are complete and are not reopened by this
milestone.

There is no approved `v1.0` redesign. Roadmap Phases 4 and 5 remain long-term
direction. Phase 6 remains long-term direction; this milestone does not add
another toolkit pack deepen, a second profile, ISO 27001 readiness, ESAF-1000 /
ESAF-1100 / ESAF-1200 re-deepen, or any new public-source readiness workstream.

## 3. Selected approach

Follow the proven next-steps pattern: planning records and ready-to-file
issues first, then tracker hygiene, then a bounded normative editorial deepen,
with version identity **`v0.14-draft`**.

Ordered themes (owner-approved Approach A):

1. **Tracker hygiene (post-v0.13)** — align GitHub with published
   `v0.13-draft` truth; close or annotate Issues `#158`–`#161` as historical;
   close GitHub milestone `v0.13-draft` when empty; open GitHub milestone
   `v0.14-draft`; keep Issue `#55` open when qualified UK review remains
   outstanding.
2. **Bounded ESAF-1500 Assessment Guide Working Draft deepen** — revision
   history bump to `0.1.1`; companion toolkit cross-links (workbook,
   evidence-catalog, audit-checklist); schemas/examples discoverability via
   the guide and `assessment/README.md`; remain Working Draft; no
   certification claims; no schema-breaking contract changes; no new maturity
   levels unless already defined.
3. **Ordinary publication gates** on one exact `v0.14-draft` candidate.

Do not open all of roadmap Phases 4–6. Do not redesign `v1.0`. Do not treat
Issues `#55` or `#60` as exit criteria. Do not open a new readiness or
crosswalk workstream. Do not include a second profile, Phase 6 toolkit pack
deepen, ISO 27001 readiness, or ESAF-1000 / ESAF-1100 / ESAF-1200 re-deepen.

Execution order:

1. Land durable milestone / backlog / roadmap records and pinned issue bodies.
2. Complete tracker hygiene so GitHub matches repository truth.
3. Complete ESAF-1500 deepen (after hygiene; finish before publication).
4. Close ordinary publication gates on one exact `v0.14-draft` candidate.

## 4. Milestone shape

### Entry state

- `v0.13-draft` is published and its publication evidence is closed.
- ESAF-1500 remains Working Draft `0.1.0` with schemas, examples, and Phase 6
  Draft toolkit packs under `assessment/`.
- ESAF-1200 remains Working Draft `0.4.1`; ESAF-1000 remains Working Draft
  `0.2.1`; ESAF-1100 remains Working Draft `0.3.1`; ESAF-1300, ESAF-1400, and
  ESAF-1700 remain at least at Working Draft `0.2.0` depth with discoverable
  example packs.
- NIST AI RMF, ISO/IEC 42001, NIST CSF 2.0, and PCI DSS readiness remain
  evidenced `HOLD`; mapping artifact counts for HOLD schemes remain `0`.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.14-draft` blockers.

### Required workstreams

1. **Tracker hygiene.** ESAF shall ensure Issue `#55` is open if and only if
   qualified UK mapping review remains outstanding, close or explicitly
   annotate Issues `#158`–`#161` as historical completed `v0.13-draft` work,
   close GitHub milestone `v0.13-draft` when it has no open issues, open
   GitHub milestone `v0.14-draft`, and align `project/BACKLOG.md` with
   published truth. This workstream does not change normative content.
2. **ESAF-1500 normative deepen.** ESAF shall complete a bounded Working Draft
   method and cross-link pass on `assessment/ESAF-1500.md`: synchronize
   cross-links to schemas, examples, workbook, evidence-catalog, and audit
   checklist surfaces; align discoverability in `assessment/README.md`; bump
   revision history to `0.1.1`; and remain Draft. No schema-breaking contract
   changes. No new maturity levels. No certification claims.
3. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.14-draft` candidate, publish annotated tag `v0.14-draft`, and
   synchronize Working Draft status surfaces.

### Exit criteria

`v0.14-draft` is complete only when:

- tracker hygiene is complete: Issues `#158`–`#161` are closed or explicitly
  annotated as historical, GitHub milestone `v0.13-draft` is closed when empty,
  GitHub milestone `v0.14-draft` exists, and Issue `#55` is open if and only if
  qualified UK review remains outstanding;
- ESAF-1500 has a bounded deepen with revision-history evidence at Working
  Draft `0.1.1`, remains Draft, and does not break assessment schemas or invent
  certification semantics;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.14-draft` is published and Working Draft status surfaces
  (`VERSION.md`, README badges, changelog, roadmap, backlog, milestones, and
  readiness record) are synchronized.

### Non-goals

`v0.14-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping (Issue `#60`);
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` when named mapper and independent reviewers
  remain unavailable;
- clearing the ISO/IEC 42001 `HOLD` or NIST CSF `HOLD` without recorded
  reconsideration triggers and named people;
- authoring mapping records, snapshots, or catalog entries under a non-`GO`
  readiness decision for any HOLD scheme;
- a new public-source readiness workstream (including ISO 27001);
- a second industry or jurisdiction profile;
- ESAF-1000, ESAF-1100, or ESAF-1200 re-deepen;
- schema-breaking changes to ESAF-1500 machine contracts;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.

## 5. Backlog and roadmap updates

`project/BACKLOG.md` shall add a post-v0.13 queue that lists the three
workstreams above, while retaining:

- deferred assurance follow-up for Issue `#55`;
- separately gated HITRUST readiness for Issue `#60`; and
- completed `v0.13-draft` NIST CSF readiness, ESAF-1200 deepen, and
  publication workstreams as historical context.

`ROADMAP.md` shall add a `0.14-draft` delivery sequence that states the order
of work (hygiene → ESAF-1500 deepen → publication) and that Phases 4, 5, and 6
remain long-term direction except for the bounded normative deepen required by
this milestone. Deferred mapping assurance and HITRUST readiness remain
tracked and do not stop later engineering work. No new readiness or crosswalk
workstream is required for this milestone.

`project/MILESTONES.md` shall add a `## v0.14-draft` section mirroring the
`v0.13-draft` structure (entry state, required workstreams, exit criteria,
non-goals).

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Sync post-v0.13 tracker hygiene
2. Deepen ESAF-1500 Assessment Guide Working Draft
3. Close the v0.14-draft publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist. This planning
change does not create GitHub issues or edit GitHub tracker state.

Issue 2 depends on hygiene acceptance criteria being met and shall finish
before Issue 3. Issue 3 depends on Issues 1–2.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS / HITRUST / NIST AI RMF /
ISO/IEC 42001 / NIST CSF blockers, open a new readiness or crosswalk
workstream, authorize mapping authorship under `HOLD` or `NO_GO`, or establish
certification, compliance, equivalence, endorsement, assurance, or production
readiness. Normative deepen artifacts produced under this milestone remain
Draft Working Draft material only. ESAF-1500 `0.1.1` remains a Working Draft
editorial deepen, not a certification, accreditation, or schema-breaking
contract change.
