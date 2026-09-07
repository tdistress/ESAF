# ESAF v0.13-draft Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-09-07

## 1. Purpose

Convert the post-`v0.12-draft` planning gap into a bounded `v0.13-draft`
milestone whose ordered headline deliverables are (1) an NIST Cybersecurity
Framework (CSF) 2.0 public-source readiness package that may exit as an
evidenced `HOLD` and (2) a bounded ESAF-1200 Reference Architecture Working
Draft deepen.

This change shall:

- leave `v0.12-draft` publication identity, annotated-tag evidence, and Draft
  lifecycle states for controls, architectures, profiles, and mappings
  unchanged;
- define measurable `v0.13-draft` entry conditions, workstreams, exit
  criteria, and non-goals;
- record the post-v0.12 engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for hygiene, NIST CSF 2.0
  readiness, ESAF-1200 deepen, and publication workstreams.

## 2. Current state

The annotated tag `v0.12-draft` is published (2026-09-07) at peel commit
`6546f2cacbbfaa89c7828991768e623b42a8081d`. Issues `#142`–`#146` are closed or
are the completed `v0.12-draft` workstreams to be annotated as historical.
Open GitHub issues are limited to:

- `#55` — qualified human review of the three UK mapping snapshots; and
- `#60` — HITRUST CSF source and review readiness.

Both remain externally gated and are not `v0.13-draft` blockers.

Phase 6 Draft starters and deepen packs exist under `assessment/` and
`templates/` / `examples/`. ESAF-1500 remains the authoritative shared
evidence, assessment-result, and maturity foundation.

NIST AI RMF readiness remains an evidenced `HOLD` under
`crosswalks/nist-ai-rmf.md` (people gate). PCI DSS readiness remains an
evidenced `HOLD`. ISO/IEC 42001 readiness is now an evidenced `HOLD` under
`crosswalks/iso-iec-42001.md`. No NIST CSF 2.0 readiness package exists yet.

ESAF-1000 is Working Draft `0.2.1`. ESAF-1100 is Working Draft `0.3.1`.
ESAF-1200 remains Version `0.4-alpha`. Companion manuals ESAF-1300 / 1400 /
1700 remain at Working Draft `0.2.0` with example packs. Toolkit deepen from
`v0.11-draft` and the ESAF-1000 / ESAF-1100 deepen from `v0.12-draft` are
complete and are not reopened by this milestone.

There is no approved `v1.0` redesign. Roadmap Phases 4 and 5 remain long-term
direction. Phase 6 remains long-term direction; this milestone does not add
another toolkit deepen, a second profile, ISO 27001 readiness, or ESAF-1000 /
ESAF-1100 re-deepen.

## 3. Selected approach

Follow the proven next-steps pattern: planning records and ready-to-file
issues first, then a fail-closed public-source readiness package, then a
bounded normative editorial deepen, with version identity **`v0.13-draft`**.

Ordered themes (owner-approved Approach A):

1. **Tracker hygiene (post-v0.12)** — align GitHub with published
   `v0.12-draft` truth; close or annotate Issues `#142`–`#146` as historical;
   keep Issue `#55` open when qualified UK review remains outstanding.
2. **NIST Cybersecurity Framework (CSF) 2.0 public-source readiness** — pin
   official public source identity, checksums where obtainable,
   publication-rights boundary, provision-inventory feasibility, mechanical
   readiness matrix, and an evidenced `GO` / `HOLD` / `NO_GO` decision without
   creating unauthorized mapping records. Default acceptable exit is evidenced
   `HOLD` when people, rights, or source-access gates fail. A matrix-derived
   `GO` is permitted only when every readiness gate clears.
3. **Bounded ESAF-1200 Reference Architecture Working Draft deepen** —
   method and cross-links to patterns, trust zones, and selection surfaces;
   revision-history bump; remain Draft; no new patterns.
4. **Ordinary publication gates** on one exact `v0.13-draft` candidate.

Do not open all of roadmap Phases 4–6. Do not redesign `v1.0`. Do not treat
Issues `#55` or `#60` as exit criteria. Do not author NIST CSF mapping
records while the readiness decision is `HOLD` or `NO_GO`. Do not include a
second profile, Phase 6 toolkit deepen, ISO 27001 readiness, or ESAF-1000 /
ESAF-1100 re-deepen.

Execution order:

1. Land durable milestone / backlog / roadmap records and pinned issue bodies.
2. Complete tracker hygiene so GitHub matches repository truth.
3. Complete NIST CSF 2.0 readiness (after hygiene; before publication).
4. Complete ESAF-1200 deepen (after hygiene; may overlap readiness; finish
   before publication).
5. Close ordinary publication gates on one exact `v0.13-draft` candidate.

## 4. Milestone shape

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

1. **Tracker hygiene.** ESAF shall ensure Issue `#55` is open if and only if
   qualified UK mapping review remains outstanding, close or explicitly
   annotate Issues `#142`–`#146` as historical completed `v0.12-draft` work,
   and align `project/BACKLOG.md` and GitHub milestone state with published
   truth. This workstream does not change normative content.
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
   `v0.13-draft` candidate, publish annotated tag `v0.13-draft`, and
   synchronize Working Draft status surfaces.

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
- annotated tag `v0.13-draft` is published and Working Draft status surfaces
  (`VERSION.md`, README badges, changelog, roadmap, backlog, milestones, and
  readiness record) are synchronized.

### Non-goals

`v0.13-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping (Issue `#60`);
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
- all roadmap crosswalks or all planned industry profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.

## 5. Backlog and roadmap updates

`project/BACKLOG.md` shall add a post-v0.12 queue that lists the four
workstreams above, while retaining:

- deferred assurance follow-up for Issue `#55`;
- separately gated HITRUST readiness for Issue `#60`; and
- completed `v0.12-draft` ISO/IEC 42001 readiness, ESAF-1000/1100 deepen, and
  publication workstreams as historical context.

`ROADMAP.md` shall add a `0.13-draft` delivery sequence that states the order
of work (hygiene → NIST CSF 2.0 readiness → ESAF-1200 deepen → publication)
and that Phases 4, 5, and 6 remain long-term direction except for the bounded
readiness and normative deepen required by this milestone. Deferred mapping
assurance and HITRUST readiness remain tracked and do not stop later
engineering work. NIST CSF 2.0 readiness may exit as evidenced `HOLD`.

`project/MILESTONES.md` shall add a `## v0.13-draft` section mirroring the
`v0.12-draft` structure (entry state, required workstreams, exit criteria,
non-goals).

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Sync post-v0.12 tracker hygiene
2. Complete NIST CSF 2.0 public-source readiness and mapping go/no-go
3. Deepen ESAF-1200 Reference Architecture Working Draft
4. Close the v0.13-draft publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist.

Issue 3 may proceed in parallel after hygiene acceptance criteria are met and
may overlap Issue 2, but Issues 2–3 shall finish before Issue 4. Issue 4
depends on Issues 1–3.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS / HITRUST / NIST AI RMF /
ISO/IEC 42001 / NIST CSF blockers, authorize NIST CSF mapping authorship under
`HOLD` or `NO_GO`, or establish certification, compliance, equivalence,
endorsement, assurance, or production readiness. Normative deepen artifacts
produced under this milestone remain Draft Working Draft material only. An
evidenced NIST CSF `HOLD` or `NO_GO` is a readiness disposition, not a
mapping, approval, or assurance claim.
