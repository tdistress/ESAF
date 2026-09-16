# ESAF v0.17-draft Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-09-16

## 1. Purpose

Convert the post-`v0.16-draft` planning gap into a bounded `v0.17-draft`
milestone whose ordered headline deliverables are (1) tracker hygiene after
`v0.16-draft` publication, (2) CIS Controls Version 8 public-source readiness
that may exit as an evidenced `HOLD`, and (3) a bounded third Phase 6
assessment-toolkit deepen across the workbook, evidence catalog, audit
checklist, and governance templates.

This change shall:

- leave `v0.16-draft` publication identity, annotated-tag evidence, and Draft
  lifecycle states for controls, architectures, profiles, and mappings
  unchanged;
- define measurable `v0.17-draft` entry conditions, workstreams, exit
  criteria, and non-goals;
- record the post-v0.16 engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for hygiene, CIS Controls
  readiness, Phase 6 third deepen, and publication workstreams.

Owner direction for this milestone is Approach C (readiness for SOC 2 or CIS
Controls + third Phase 6 toolkit deepen). Within that approved direction,
this design selects **CIS Controls Version 8** as the readiness scheme and
queues **SOC 2 (AICPA TSC)** as separately gated follow-on work, because CIS
Controls are publicly downloadable in a NIST-like inventory shape while SOC 2
source text is typically copyright-restricted.

## 2. Current state

The annotated tag `v0.16-draft` is published (2026-09-16) at peel commit
`b6a7547662720a0ea643f4a7766a75ff73af9a15` (tag object
`c4d41670de99b956ea1e41d7ce06ad427dce3bc0`). Published-truth surfaces land at
`ebe09e0265dd3ee39fb54f973853c66148ca9e10`. Issues `#193`–`#196` are closed
completed `v0.16-draft` workstreams to be annotated as historical. GitHub
milestone `v0.16-draft` is closed empty. Open GitHub issues remain limited to:

- `#55` — qualified human review of the three UK mapping snapshots; and
- `#60` — HITRUST CSF source and review readiness.

Both remain externally gated and are not `v0.17-draft` blockers.

The UK jurisdiction profile is Draft `0.2.0` under `profiles/uk/0.2.0/`.
ESAF-1500 remains Working Draft `0.1.1`. ESAF-1000 is Working Draft `0.2.1`.
ESAF-1100 is Working Draft `0.3.1`. ESAF-1200 is Working Draft `0.4.1`.
ESAF-1300, ESAF-1400, and ESAF-1700 are Working Draft `0.3.0` with example
packs. Phase 6 toolkit packs have completed the `v0.11-draft` (first deepen)
and `v0.15-draft` (second deepen) passes.

NIST AI RMF, ISO/IEC 42001, NIST CSF 2.0, ISO/IEC 27001, PCI DSS, and NIST SP
800-53 readiness remain evidenced `HOLD`; mapping artifact counts for HOLD
schemes remain `0`. No CIS Controls or SOC 2 readiness package or mapping
artifacts exist yet.

There is no approved `v1.0` redesign. Roadmap Phases 4, 5, and 6 remain
long-term direction except for the bounded CIS Controls readiness and third
Phase 6 toolkit deepen required by this milestone. This milestone does not
add a second profile, clear prior HOLDs, reopen ESAF-1000 / 1100 / 1200 /
1300 / 1400 / 1500 / 1700 normative deepen, author SOC 2 readiness inside
this milestone, or authorize mapping authorship under a non-`GO` readiness
decision.

## 3. Selected approach

Follow the proven next-steps pattern: planning records and ready-to-file
issues first, then tracker hygiene, then a fail-closed public-source readiness
package, then bounded deepen work, with version identity **`v0.17-draft`**.

Ordered themes (owner-approved Approach C; CIS Controls selected over SOC 2
for this milestone):

1. **Tracker hygiene (post-v0.16)** — align GitHub with published
   `v0.16-draft` truth; close or annotate Issues `#193`–`#196` as historical;
   confirm GitHub milestone `v0.16-draft` is closed when empty; open GitHub
   milestone `v0.17-draft`; keep Issue `#55` open when qualified UK review
   remains outstanding.
2. **CIS Controls Version 8 public-source readiness** — pin official public
   source identity, checksums where obtainable, publication-rights boundary,
   provision-inventory feasibility, mechanical readiness matrix, and an
   evidenced `GO` / `HOLD` / `NO_GO` decision without creating unauthorized
   mapping records. Default acceptable exit is evidenced `HOLD` when people,
   rights, or source-access gates fail. Clone the NIST CSF / NIST AI RMF /
   NIST SP 800-53 public-PDF inventory shape (not the ISO copyright-blocked
   inventory shape) because CIS Controls Version 8 is publicly downloadable.
   While `HOLD` or `NO_GO`, no CIS Controls mapping records, snapshots, or
   catalog increments. SOC 2 readiness is out of scope for this milestone and
   remains a separately gated follow-on initiative.
3. **Phase 6 toolkit deepen (third pass)** — bounded Draft deepen of the
   assessment workbook, evidence catalog, audit checklist, and governance
   templates beyond the `v0.11-draft` and `v0.15-draft` packs; remain Draft;
   stay bound to ESAF-1500 contracts; no certification claims; not a complete
   Phase 6 library. Prefer covering remaining closed evidence types lacking
   filled catalog examples (`record`, `configuration`, `observation`,
   `contract`, `external_assurance`, and optionally `other`) plus one
   additional workbook engagement vignette, one additional audit sampling
   vignette, and one additional governance-template filled example or
   cross-template thread.
4. **Ordinary publication gates** on one exact `v0.17-draft` candidate.

Do not open all of roadmap Phases 4–6. Do not redesign `v1.0`. Do not treat
Issues `#55` or `#60` as exit criteria. Do not author CIS Controls mapping
records while the readiness decision is `HOLD` or `NO_GO`. Do not clear prior
HOLDs without their recorded reconsideration triggers and named people. Do not
author a SOC 2 readiness package inside this milestone. Do not deepen UK
profile beyond `0.2.0` or add a second industry or jurisdiction profile.

Execution order:

1. Land durable milestone / backlog / roadmap records and pinned issue bodies.
2. Complete tracker hygiene so GitHub matches repository truth.
3. Complete CIS Controls readiness (after hygiene; before publication).
4. Complete Phase 6 third toolkit deepen (after hygiene; may overlap readiness;
   finish before publication).
5. Close ordinary publication gates on one exact `v0.17-draft` candidate.

## 4. Milestone shape

### Entry state

- `v0.16-draft` is published and its publication evidence is closed.
- ESAF-1500 remains Working Draft `0.1.1` with schemas, examples, and Phase 6
  Draft toolkit packs under `assessment/` and `templates/` after the first and
  second deepen passes.
- ESAF-1200 remains Working Draft `0.4.1`; ESAF-1000 remains Working Draft
  `0.2.1`; ESAF-1100 remains Working Draft `0.3.1`; ESAF-1300, ESAF-1400, and
  ESAF-1700 remain at Working Draft `0.3.0` depth with discoverable example
  packs.
- The UK jurisdiction profile remains Draft `0.2.0`.
- NIST AI RMF, ISO/IEC 42001, NIST CSF 2.0, ISO/IEC 27001, PCI DSS, and NIST
  SP 800-53 readiness remain evidenced `HOLD`; mapping artifact counts for
  HOLD schemes remain `0`.
- No CIS Controls or SOC 2 readiness package or mapping artifacts exist yet.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.17-draft` blockers.

### Required workstreams

1. **Tracker hygiene.** ESAF shall ensure Issue `#55` is open if and only if
   qualified UK mapping review remains outstanding, close or explicitly
   annotate Issues `#193`–`#196` as historical completed `v0.16-draft` work,
   close GitHub milestone `v0.16-draft` when it has no open issues, open
   GitHub milestone `v0.17-draft`, and align `project/BACKLOG.md` with
   published truth. This workstream does not change normative content.
2. **CIS Controls Version 8 public-source readiness.** ESAF shall pin the
   applicable official CIS Controls Version 8 source identity, establish
   publication-rights and provision-inventory boundaries, assess mapper and
   qualified-review availability, produce a mechanical readiness matrix, and
   record a `GO` / `HOLD` / `NO_GO` decision. The default acceptable exit is
   an evidenced `HOLD` that restates blockers, owners, reconsideration
   triggers, re-entry tests, and nonclaims. A matrix-derived `GO` is allowed
   only when every readiness gate clears, including named mapper and
   independent reviewer evidence. While the decision remains `HOLD` or
   `NO_GO`, ESAF shall not create CIS Controls mapping relationships,
   negative dispositions, snapshots, lifecycle events, registry entries, or
   catalog increments.
3. **Phase 6 toolkit deepen.** ESAF shall complete a bounded third Working
   Draft deepen of the assessment workbook, evidence catalog, audit checklist,
   and governance templates beyond the `v0.11-draft` and `v0.15-draft` packs;
   remain Draft; stay bound to ESAF-1500 contracts; and avoid certification
   claims or a complete assessment library.
4. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.17-draft` candidate, publish annotated tag `v0.17-draft`, and
   synchronize Working Draft status surfaces.

### Exit criteria

`v0.17-draft` is complete only when:

- tracker hygiene is complete: Issues `#193`–`#196` are closed or explicitly
  annotated as historical, GitHub milestone `v0.16-draft` is closed when empty,
  GitHub milestone `v0.17-draft` exists, and Issue `#55` is open if and only if
  qualified UK review remains outstanding;
- CIS Controls readiness is recorded as evidenced `GO`, `HOLD`, or `NO_GO`;
  if `HOLD` or `NO_GO`, CIS Controls mapping artifact count remains `0` and
  generated crosswalk catalog counts are unchanged by that workstream;
- Phase 6 toolkit packs have a bounded third deepen with Draft evidence and
  remain bound to ESAF-1500 contracts without certification claims;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.17-draft` is published and Working Draft status surfaces
  (`VERSION.md`, README badges, changelog, roadmap, backlog, milestones, and
  readiness record) are synchronized.

### Non-goals

`v0.17-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping (Issue `#60`);
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` when named mapper and independent reviewers
  remain unavailable;
- clearing the ISO/IEC 42001 `HOLD`, NIST CSF `HOLD`, ISO/IEC 27001 `HOLD`, or
  NIST SP 800-53 `HOLD` without recorded reconsideration triggers and named
  people;
- authoring CIS Controls, SOC 2, NIST SP 800-53, ISO/IEC 27001, ISO/IEC 42001,
  NIST AI RMF, NIST CSF, or PCI DSS mapping records, snapshots, or catalog
  entries under a non-`GO` readiness decision;
- a SOC 2 (AICPA TSC) readiness package (separately gated follow-on);
- a second industry or jurisdiction profile or UK profile deepen beyond
  `0.2.0`;
- a complete Phase 6 assessment library;
- ESAF-1000, ESAF-1100, ESAF-1200, ESAF-1300, ESAF-1400, ESAF-1500, or
  ESAF-1700 re-deepen;
- schema-breaking changes to ESAF-1500 or ESAF-1800 machine contracts;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.

## 5. Backlog and roadmap updates

`project/BACKLOG.md` shall add a post-v0.16 queue that lists the four
workstreams above, while retaining:

- deferred assurance follow-up for Issue `#55`;
- separately gated HITRUST readiness for Issue `#60`;
- a separately gated SOC 2 readiness follow-on note; and
- completed `v0.16-draft` hygiene, readiness, deepen, and publication
  workstreams as historical context.

`ROADMAP.md` shall add a `0.17-draft` delivery sequence that states the order
of work (hygiene → CIS Controls readiness → Phase 6 third toolkit deepen →
publication) and that Phases 4, 5, and 6 remain long-term direction except for
the bounded readiness and deepen work required by this milestone. Deferred
mapping assurance and HITRUST readiness remain tracked and do not stop later
engineering work. CIS Controls readiness may exit as evidenced `HOLD`. SOC 2
readiness remains Phase 4 long-term direction outside this milestone.

`project/MILESTONES.md` shall add a `## v0.17-draft` section mirroring the
`v0.16-draft` structure (entry state, required workstreams, exit criteria,
non-goals).

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Sync post-v0.16 tracker hygiene
2. Complete CIS Controls Version 8 public-source readiness and mapping go/no-go
3. Deepen Phase 6 assessment toolkit Draft packs (third pass)
4. Close the v0.17-draft publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist. This planning
change does not create GitHub issues or edit GitHub tracker state.

Issue 3 may proceed in parallel with Issue 2 after hygiene acceptance criteria
are met, but Issues 2–3 shall finish before Issue 4. Issue 4 depends on
Issues 1–3.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS / HITRUST / NIST AI RMF /
ISO/IEC 42001 / NIST CSF / ISO/IEC 27001 / NIST SP 800-53 blockers, open
unauthorized mapping authorship under `HOLD` or `NO_GO`, author a SOC 2
readiness package, or establish certification, compliance, equivalence,
endorsement, assurance, or production readiness. Readiness and Phase 6 deepen
artifacts produced under this milestone remain Draft Working Draft material
only. An evidenced CIS Controls `HOLD` is an acceptable milestone exit and
does not authorize mapping records.
