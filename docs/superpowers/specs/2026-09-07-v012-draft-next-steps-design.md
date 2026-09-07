# ESAF v0.12-draft Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-09-07

## 1. Purpose

Convert the post-`v0.11-draft` planning gap into a bounded `v0.12-draft`
milestone whose ordered headline deliverables are (1) an ISO/IEC 42001:2023
public-source readiness package that may exit as an evidenced `HOLD` and
(2) a bounded ESAF-1000 / ESAF-1100 normative editorial deepen.

This change shall:

- leave `v0.11-draft` publication identity, annotated-tag evidence, and Draft
  lifecycle states for controls, architectures, profiles, and mappings
  unchanged;
- define measurable `v0.12-draft` entry conditions, workstreams, exit
  criteria, and non-goals;
- record the post-v0.11 engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for hygiene, ISO/IEC 42001
  readiness, ESAF-1000/1100 deepen, and publication workstreams.

## 2. Current state

The annotated tag `v0.11-draft` is published (2026-09-06) at peel commit
`0afbf963a6c11ee1feb65384b8e685461fe2dc85`. Issues `#123`–`#129` are closed.
Open GitHub issues are limited to:

- `#55` — qualified human review of the three UK mapping snapshots; and
- `#60` — HITRUST CSF source and review readiness.

Both remain externally gated and are not `v0.12-draft` blockers.

Phase 6 Draft starters and deepen packs exist under `assessment/` and
`templates/` / `examples/`. ESAF-1500 remains the authoritative shared
evidence, assessment-result, and maturity foundation.

NIST AI RMF readiness remains an evidenced `HOLD` under
`crosswalks/nist-ai-rmf.md` (people gate). PCI DSS readiness remains an
evidenced `HOLD`. No ISO/IEC 42001 readiness package exists yet.

ESAF-1000 remains Working Draft `0.2-alpha`. ESAF-1100 remains control
architecture working draft `0.3-alpha`. Companion manuals ESAF-1300 / 1400 /
1700 remain at Working Draft `0.2.0` with example packs. Toolkit deepen from
`v0.11-draft` is complete and is not reopened by this milestone.

There is no approved `v1.0` redesign. Roadmap Phases 4 and 5 remain long-term
direction. Phase 6 remains long-term direction; this milestone does not add
another toolkit deepen.

## 3. Selected approach

Follow the proven next-steps pattern: planning records and ready-to-file
issues first, then a fail-closed public-source readiness package, then a
bounded normative editorial deepen, with version identity **`v0.12-draft`**.

Ordered themes (owner-approved Approach A):

1. **ISO/IEC 42001:2023 public-source readiness** — pin official public
   source identity, checksums where obtainable, publication-rights boundary,
   provision-inventory feasibility, mechanical readiness matrix, and an
   evidenced `GO` / `HOLD` / `NO_GO` decision without creating unauthorized
   mapping records. Default acceptable exit is evidenced `HOLD` when people,
   rights, or source-access gates fail. A matrix-derived `GO` is permitted
   only when every readiness gate clears.
2. **ESAF-1000 / ESAF-1100 normative deepen** — bounded Working Draft
   editorial and consistency pass: cross-links to current companion and
   toolkit surfaces, terminology consistency, revision-history bumps, and
   ESAF-1100 method/catalog-architecture alignment with ESAF-1500. No new
   control families, objectives, or base controls. No pillar redesign.

Do not open all of roadmap Phases 4–6. Do not redesign `v1.0`. Do not treat
Issues `#55` or `#60` as exit criteria. Do not author ISO/IEC 42001 mapping
records while the readiness decision is `HOLD`.

Execution order:

1. Land durable milestone / backlog / roadmap records and pinned issue bodies.
2. Complete tracker hygiene so GitHub matches repository truth.
3. Complete ISO/IEC 42001 readiness (after hygiene; before publication).
4. Complete ESAF-1000 and ESAF-1100 deepen (after hygiene; may overlap
   readiness; both finish before publication).
5. Close ordinary publication gates on one exact `v0.12-draft` candidate.

## 4. Milestone shape

### Entry state

- `v0.11-draft` is published and its publication evidence is closed.
- ESAF-1300, ESAF-1400, and ESAF-1700 remain at least at Working Draft `0.2.0`
  depth with discoverable example packs.
- ESAF-1500 foundation schemas, examples, and the Phase 6 Draft toolkit packs
  (starters plus `v0.11-draft` deepen) remain Draft and authoritative for
  shared assessment semantics.
- NIST AI RMF readiness remains evidenced `HOLD`; NIST mapping artifact count
  remains `0`.
- No ISO/IEC 42001 readiness package or mapping artifacts exist yet.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.12-draft` blockers.
- ESAF-1000, ESAF-1100, ESAF-1200, ESAF-1600 method artifacts, the UK pilot
  profile, and the three UK mapping snapshots remain Draft.

### Required workstreams

1. **Tracker hygiene.** ESAF shall ensure Issue `#55` is open if and only if
   qualified UK mapping review remains outstanding, close or explicitly
   annotate Issues `#123`–`#129` as historical completed `v0.11-draft` work,
   and align `project/BACKLOG.md` and GitHub milestone state with published
   truth. This workstream does not change normative content.
2. **ISO/IEC 42001:2023 public-source readiness.** ESAF shall pin the
   applicable official ISO/IEC 42001:2023 source identity, establish
   publication-rights and provision-inventory boundaries, assess mapper and
   qualified-review availability, produce a mechanical readiness matrix, and
   record a `GO` / `HOLD` / `NO_GO` decision. The default acceptable exit is
   an evidenced `HOLD` that restates blockers, owners, reconsideration
   triggers, re-entry tests, and nonclaims. A matrix-derived `GO` is allowed
   only when every readiness gate clears, including named mapper and
   independent reviewer evidence. While the decision remains `HOLD` or
   `NO_GO`, ESAF shall not create ISO/IEC 42001 mapping relationships,
   negative dispositions, snapshots, lifecycle events, registry entries, or
   catalog increments.
3. **ESAF-1000 normative deepen.** ESAF shall complete a bounded Working Draft
   editorial pass on `framework/ESAF-1000.md`: synchronize cross-links to
   current ESAF-1300 / 1400 / 1500 / 1700 and toolkit surfaces, align
   terminology with the glossary and companions, bump revision history, and
   preserve the three pillars and lifecycle model unchanged. No new normative
   pillars, lifecycle stages, or parallel management-system requirements.
4. **ESAF-1100 normative deepen.** ESAF shall complete a bounded Working Draft
   method/catalog-architecture pass on `controls/ESAF-1100.md`: align
   assessment, evidence, and baseline wording with ESAF-1500 shared
   contracts, improve cross-links, and bump revision history. No new control
   families, objectives, base controls, or enhancements.
5. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.12-draft` candidate, publish annotated tag `v0.12-draft`, and
   synchronize Working Draft status surfaces.

### Exit criteria

`v0.12-draft` is complete only when:

- tracker hygiene is complete: Issues `#123`–`#129` are closed or explicitly
  annotated as historical, and Issue `#55` is open if and only if qualified UK
  review remains outstanding;
- ISO/IEC 42001 readiness is recorded as evidenced `GO`, `HOLD`, or `NO_GO`;
  if `HOLD` or `NO_GO`, ISO/IEC 42001 mapping artifact count remains `0` and
  generated crosswalk catalog counts are unchanged by that workstream;
- ESAF-1000 and ESAF-1100 each have a bounded deepen with revision-history
  evidence, remain Draft, and do not invent parallel assessment semantics or
  new control identifiers;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.12-draft` is published and Working Draft status surfaces
  (`VERSION.md`, README badges, changelog, roadmap, backlog, milestones, and
  readiness record) are synchronized.

### Non-goals

`v0.12-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping (Issue `#60`);
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` when named mapper and independent reviewers
  remain unavailable;
- authoring ISO/IEC 42001, NIST AI RMF, or PCI DSS mapping records, snapshots,
  or catalog entries under a non-`GO` readiness decision;
- a second industry or jurisdiction profile;
- another Phase 6 toolkit deepen or a complete assessment library;
- all roadmap crosswalks or all planned industry profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.

## 5. Backlog and roadmap updates

`project/BACKLOG.md` shall add a post-v0.11 queue that lists the five
workstreams above, while retaining:

- deferred assurance follow-up for Issue `#55`;
- separately gated HITRUST readiness for Issue `#60`; and
- completed `v0.11-draft` toolkit-deepen, NIST readiness re-entry, and
  publication workstreams as historical context.

`ROADMAP.md` shall add a `0.12-draft` delivery sequence that states the order
of work (hygiene → ISO/IEC 42001 readiness → ESAF-1000/1100 deepen →
publication) and that Phases 4, 5, and 6 remain long-term direction except for
the bounded readiness and normative deepen required by this milestone.
Deferred mapping assurance and HITRUST readiness remain tracked and do not
stop later engineering work. ISO/IEC 42001 readiness may exit as evidenced
`HOLD`.

`project/MILESTONES.md` shall add a `## v0.12-draft` section mirroring the
`v0.11-draft` structure (entry state, required workstreams, exit criteria,
non-goals).

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Sync post-v0.11 tracker hygiene
2. Complete ISO/IEC 42001:2023 public-source readiness and mapping go/no-go
3. Deepen ESAF-1000 Enterprise Standard Working Draft
4. Deepen ESAF-1100 Control Catalog architecture Working Draft
5. Close the v0.12-draft publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist.

Issues 3–4 may proceed in parallel after hygiene acceptance criteria are met
and may overlap Issue 2, but Issues 2–4 shall finish before Issue 5. Issue 5
depends on Issues 1–4.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS / HITRUST / NIST AI RMF /
ISO/IEC 42001 blockers, authorize ISO/IEC 42001 mapping authorship under
`HOLD` or `NO_GO`, or establish certification, compliance, equivalence,
endorsement, assurance, or production readiness. Normative deepen artifacts
produced under this milestone remain Draft Working Draft material only. An
evidenced ISO/IEC 42001 `HOLD` or `NO_GO` is a readiness disposition, not a
mapping, approval, or assurance claim.
