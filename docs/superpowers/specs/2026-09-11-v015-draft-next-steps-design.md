# ESAF v0.15-draft Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-09-11

## 1. Purpose

Convert the post-`v0.14-draft` planning gap into a bounded `v0.15-draft`
milestone whose ordered headline deliverables are (1) tracker hygiene after
`v0.14-draft` publication, (2) ISO/IEC 27001:2022 public-source readiness that
may exit as an evidenced `HOLD`, (3) a second bounded Phase 6 assessment-toolkit
deepen, and (4) a bounded ESAF-1300 / ESAF-1400 / ESAF-1700 Working Draft deepen
from `0.2.0` to `0.3.0`.

This change shall:

- leave `v0.14-draft` publication identity, annotated-tag evidence, and Draft
  lifecycle states for controls, architectures, profiles, and mappings
  unchanged;
- define measurable `v0.15-draft` entry conditions, workstreams, exit
  criteria, and non-goals;
- record the post-v0.14 engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for hygiene, ISO/IEC 27001
  readiness, Phase 6 toolkit deepen, companion-manual deepen, and publication
  workstreams.

## 2. Current state

The annotated tag `v0.14-draft` is published (2026-09-10) at peel commit
`7727d6f2bcf020ddf453374c95ed37f51e6e41ff`. Issues `#171`–`#173` are closed
completed `v0.14-draft` workstreams to be annotated as historical. Open GitHub
issues are limited to:

- `#55` — qualified human review of the three UK mapping snapshots; and
- `#60` — HITRUST CSF source and review readiness.

Both remain externally gated and are not `v0.15-draft` blockers.

Phase 6 Draft starters and the `v0.11-draft` deepen packs exist under
`assessment/` and `templates/`. ESAF-1500 remains the authoritative shared
evidence, assessment-result, and maturity foundation at Working Draft
`0.1.1`.

NIST AI RMF readiness remains an evidenced `HOLD` under
`crosswalks/nist-ai-rmf.md` (people gate). PCI DSS readiness remains an
evidenced `HOLD`. ISO/IEC 42001 readiness remains an evidenced `HOLD` under
`crosswalks/iso-iec-42001.md`. NIST CSF 2.0 readiness remains an evidenced
`HOLD` under `crosswalks/nist-csf.md` (people gate). No ISO/IEC 27001
readiness package exists yet.

ESAF-1000 is Working Draft `0.2.1`. ESAF-1100 is Working Draft `0.3.1`.
ESAF-1200 is Working Draft `0.4.1`. Companion manuals ESAF-1300 / 1400 /
1700 remain at Working Draft `0.2.0` with example packs. Toolkit deepen from
`v0.11-draft`, the ESAF-1000 / ESAF-1100 deepen from `v0.12-draft`, the
ESAF-1200 deepen from `v0.13-draft`, and the ESAF-1500 deepen from
`v0.14-draft` are complete and are not reopened by this milestone except for
the explicit second Phase 6 toolkit deepen defined below.

There is no approved `v1.0` redesign. Roadmap Phases 4 and 5 remain long-term
direction. Phase 6 remains long-term direction except for the bounded second
toolkit deepen required by this milestone. This milestone does not add a
second profile, clear prior HOLDs, reopen ESAF-1000 / 1100 / 1200 / 1500
deepen, or authorize mapping authorship under a non-`GO` readiness decision.

## 3. Selected approach

Follow the proven next-steps pattern: planning records and ready-to-file
issues first, then tracker hygiene, then a fail-closed public-source readiness
package, then bounded deepen workstreams, with version identity
**`v0.15-draft`**.

Ordered themes (owner-approved Approach A covering prior candidates 1–3):

1. **Tracker hygiene (post-v0.14)** — align GitHub with published
   `v0.14-draft` truth; close or annotate Issues `#171`–`#173` as historical;
   close GitHub milestone `v0.14-draft` when empty; open GitHub milestone
   `v0.15-draft`; keep Issue `#55` open when qualified UK review remains
   outstanding.
2. **ISO/IEC 27001:2022 public-source readiness** — pin official public source
   identity, checksums where obtainable, publication-rights boundary,
   provision-inventory feasibility, mechanical readiness matrix, and an
   evidenced `GO` / `HOLD` / `NO_GO` decision without creating unauthorized
   mapping records. Default acceptable exit is evidenced `HOLD` when people,
   rights, or source-access gates fail. Clone the ISO/IEC 42001 / PCI-shaped
   package (not the NIST public-PDF inventory shape) because ISO copyright
   typically blocks public provision inventories. While `HOLD` or `NO_GO`, no
   ISO/IEC 27001 mapping records, snapshots, or catalog increments.
3. **Phase 6 toolkit deepen (second pass)** — bounded Draft deepen of the
   assessment workbook, evidence catalog, audit checklist, and governance
   templates beyond the `v0.11-draft` packs; remain Draft; stay bound to
   ESAF-1500 contracts; no certification claims; not a complete Phase 6
   library.
4. **ESAF-1300 / ESAF-1400 / ESAF-1700 Working Draft deepen** — bounded deepen
   from `0.2.0` to `0.3.0`; clarifying `shall`/`should` in 1300/1700 must cite
   parent ESAF-1000 / 1100 / GOV / 1500 obligations; ESAF-1400 remains
   informative with no local `shall`; examples remain informative; no new
   control IDs, procedures, or metrics.
5. **Ordinary publication gates** on one exact `v0.15-draft` candidate.

Do not open all of roadmap Phases 4–6. Do not redesign `v1.0`. Do not treat
Issues `#55` or `#60` as exit criteria. Do not author ISO/IEC 27001 mapping
records while the readiness decision is `HOLD` or `NO_GO`. Do not clear prior
HOLDs without their recorded reconsideration triggers and named people.

Execution order:

1. Land durable milestone / backlog / roadmap records and pinned issue bodies.
2. Complete tracker hygiene so GitHub matches repository truth.
3. Complete ISO/IEC 27001 readiness (after hygiene; before publication).
4. Complete Phase 6 toolkit deepen and ESAF-1300/1400/1700 deepen (after
   hygiene; may overlap readiness and each other; both finish before
   publication).
5. Close ordinary publication gates on one exact `v0.15-draft` candidate.

## 4. Milestone shape

### Entry state

- `v0.14-draft` is published and its publication evidence is closed.
- ESAF-1500 remains Working Draft `0.1.1` with schemas, examples, and Phase 6
  Draft toolkit packs under `assessment/` and `templates/`.
- ESAF-1200 remains Working Draft `0.4.1`; ESAF-1000 remains Working Draft
  `0.2.1`; ESAF-1100 remains Working Draft `0.3.1`; ESAF-1300, ESAF-1400, and
  ESAF-1700 remain at Working Draft `0.2.0` depth with discoverable example
  packs.
- NIST AI RMF, ISO/IEC 42001, NIST CSF 2.0, and PCI DSS readiness remain
  evidenced `HOLD`; mapping artifact counts for HOLD schemes remain `0`.
- No ISO/IEC 27001 readiness package or mapping artifacts exist yet.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.15-draft` blockers.

### Required workstreams

1. **Tracker hygiene.** ESAF shall ensure Issue `#55` is open if and only if
   qualified UK mapping review remains outstanding, close or explicitly
   annotate Issues `#171`–`#173` as historical completed `v0.14-draft` work,
   close GitHub milestone `v0.14-draft` when it has no open issues, open
   GitHub milestone `v0.15-draft`, and align `project/BACKLOG.md` with
   published truth. This workstream does not change normative content.
2. **ISO/IEC 27001:2022 public-source readiness.** ESAF shall pin the
   applicable official ISO/IEC 27001:2022 source identity, establish
   publication-rights and provision-inventory boundaries, assess mapper and
   qualified-review availability, produce a mechanical readiness matrix, and
   record a `GO` / `HOLD` / `NO_GO` decision. The default acceptable exit is
   an evidenced `HOLD` that restates blockers, owners, reconsideration
   triggers, re-entry tests, and nonclaims. A matrix-derived `GO` is allowed
   only when every readiness gate clears, including named mapper and
   independent reviewer evidence. While the decision remains `HOLD` or
   `NO_GO`, ESAF shall not create ISO/IEC 27001 mapping relationships,
   negative dispositions, snapshots, lifecycle events, registry entries, or
   catalog increments.
3. **Phase 6 toolkit deepen.** ESAF shall complete a bounded second Working
   Draft deepen of the assessment workbook, evidence catalog, audit checklist,
   and governance templates: add operator-facing examples or vignettes beyond
   the `v0.11-draft` packs, keep ESAF-1500 contract alignment, remain Draft,
   and avoid certification claims or a complete assessment library.
4. **ESAF-1300 / ESAF-1400 / ESAF-1700 normative deepen.** ESAF shall complete
   a bounded Working Draft deepen of `governance/ESAF-1300.md`,
   `implementation/ESAF-1400.md`, and `data-model/ESAF-1700.md` from `0.2.0`
   to `0.3.0`, update revision histories, extend discoverable example packs as
   needed, keep ESAF-1400 informative, and require parent-obligation citations
   for any clarifying `shall`/`should` in ESAF-1300 or ESAF-1700. No new
   control identifiers, procedures, or metrics.
5. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.15-draft` candidate, publish annotated tag `v0.15-draft`, and
   synchronize Working Draft status surfaces.

### Exit criteria

`v0.15-draft` is complete only when:

- tracker hygiene is complete: Issues `#171`–`#173` are closed or explicitly
  annotated as historical, GitHub milestone `v0.14-draft` is closed when empty,
  GitHub milestone `v0.15-draft` exists, and Issue `#55` is open if and only if
  qualified UK review remains outstanding;
- ISO/IEC 27001 readiness is recorded as evidenced `GO`, `HOLD`, or `NO_GO`;
  if `HOLD` or `NO_GO`, ISO/IEC 27001 mapping artifact count remains `0` and
  generated crosswalk catalog counts are unchanged by that workstream;
- Phase 6 toolkit packs have a bounded second deepen with Draft evidence and
  remain bound to ESAF-1500 contracts without certification claims;
- ESAF-1300, ESAF-1400, and ESAF-1700 each have a bounded deepen with
  revision-history evidence at Working Draft `0.3.0`, remain Draft, and do not
  invent new control identifiers or local ESAF-1400 `shall` statements;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.15-draft` is published and Working Draft status surfaces
  (`VERSION.md`, README badges, changelog, roadmap, backlog, milestones, and
  readiness record) are synchronized.

### Non-goals

`v0.15-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping (Issue `#60`);
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` when named mapper and independent reviewers
  remain unavailable;
- clearing the ISO/IEC 42001 `HOLD` or NIST CSF `HOLD` without recorded
  reconsideration triggers and named people;
- authoring ISO/IEC 27001, ISO/IEC 42001, NIST AI RMF, NIST CSF, or PCI DSS
  mapping records, snapshots, or catalog entries under a non-`GO` readiness
  decision;
- a second industry or jurisdiction profile;
- a complete Phase 6 assessment library;
- ESAF-1000, ESAF-1100, ESAF-1200, or ESAF-1500 re-deepen;
- schema-breaking changes to ESAF-1500 machine contracts;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.

## 5. Backlog and roadmap updates

`project/BACKLOG.md` shall add a post-v0.14 queue that lists the five
workstreams above, while retaining:

- deferred assurance follow-up for Issue `#55`;
- separately gated HITRUST readiness for Issue `#60`; and
- completed `v0.14-draft` hygiene, ESAF-1500 deepen, and publication
  workstreams as historical context.

`ROADMAP.md` shall add a `0.15-draft` delivery sequence that states the order
of work (hygiene → ISO/IEC 27001 readiness → Phase 6 toolkit deepen and
ESAF-1300/1400/1700 deepen → publication) and that Phases 4, 5, and 6 remain
long-term direction except for the bounded readiness and deepen work required
by this milestone. Deferred mapping assurance and HITRUST readiness remain
tracked and do not stop later engineering work. ISO/IEC 27001 readiness may
exit as evidenced `HOLD`.

`project/MILESTONES.md` shall add a `## v0.15-draft` section mirroring the
`v0.14-draft` structure (entry state, required workstreams, exit criteria,
non-goals).

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Sync post-v0.14 tracker hygiene
2. Complete ISO/IEC 27001:2022 public-source readiness and mapping go/no-go
3. Deepen Phase 6 assessment toolkit Draft packs
4. Deepen ESAF-1300/1400/1700 Working Drafts to 0.3.0
5. Close the v0.15-draft publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist. This planning
change does not create GitHub issues or edit GitHub tracker state.

Issues 3–4 may proceed in parallel after hygiene acceptance criteria are met
and may overlap Issue 2, but Issues 2–4 shall finish before Issue 5. Issue 5
depends on Issues 1–4.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS / HITRUST / NIST AI RMF /
ISO/IEC 42001 / NIST CSF blockers, open unauthorized mapping authorship under
`HOLD` or `NO_GO`, or establish certification, compliance, equivalence,
endorsement, assurance, or production readiness. Readiness, toolkit, and
companion deepen artifacts produced under this milestone remain Draft Working
Draft material only. An evidenced ISO/IEC 27001 `HOLD` is an acceptable
milestone exit and does not authorize mapping records.
