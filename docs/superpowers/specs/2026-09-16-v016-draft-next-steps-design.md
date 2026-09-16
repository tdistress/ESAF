# ESAF v0.16-draft Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-09-16

## 1. Purpose

Convert the post-`v0.15-draft` planning gap into a bounded `v0.16-draft`
milestone whose ordered headline deliverables are (1) tracker hygiene after
`v0.15-draft` publication, (2) NIST SP 800-53 Revision 5 public-source readiness
that may exit as an evidenced `HOLD`, and (3) a bounded United Kingdom
jurisdiction profile deepen from Draft `0.1.0` to Draft `0.2.0`.

This change shall:

- leave `v0.15-draft` publication identity, annotated-tag evidence, and Draft
  lifecycle states for controls, architectures, profiles, and mappings
  unchanged;
- define measurable `v0.16-draft` entry conditions, workstreams, exit
  criteria, and non-goals;
- record the post-v0.15 engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for hygiene, NIST SP 800-53
  readiness, UK profile deepen, and publication workstreams.

Owner direction for this milestone is Approach A (NIST SP 800-53 readiness +
UK profile deepen). Approach C (SOC 2 or CIS Controls readiness + Phase 6
third toolkit deepen) is the preferred subsequent milestone direction after
`v0.16-draft` and is not a `v0.16-draft` workstream.

## 2. Current state

The annotated tag `v0.15-draft` is published (2026-09-11) at peel commit
`f006146dc037538478506d013801f7a357eaefa3`. Issues `#181`–`#185` are closed
completed `v0.15-draft` workstreams to be annotated as historical. Open GitHub
issues are limited to:

- `#55` — qualified human review of the three UK mapping snapshots; and
- `#60` — HITRUST CSF source and review readiness.

Both remain externally gated and are not `v0.16-draft` blockers.

The UK jurisdiction profile remains Draft `0.1.0` under `profiles/uk/0.1.0/`.
ESAF-1500 remains Working Draft `0.1.1`. ESAF-1000 is Working Draft `0.2.1`.
ESAF-1100 is Working Draft `0.3.1`. ESAF-1200 is Working Draft `0.4.1`.
ESAF-1300, ESAF-1400, and ESAF-1700 are Working Draft `0.3.0` with example
packs. Phase 6 toolkit packs have completed the `v0.11-draft` and
`v0.15-draft` deepen passes.

NIST AI RMF, ISO/IEC 42001, NIST CSF 2.0, ISO/IEC 27001, and PCI DSS readiness
remain evidenced `HOLD`; mapping artifact counts for HOLD schemes remain `0`.
No NIST SP 800-53 readiness package or mapping artifacts exist yet.

There is no approved `v1.0` redesign. Roadmap Phases 4, 5, and 6 remain
long-term direction except for the bounded readiness and UK profile deepen
required by this milestone. This milestone does not add a second profile,
clear prior HOLDs, reopen ESAF-1000 / 1100 / 1200 / 1300 / 1400 / 1500 / 1700
or Phase 6 deepen, or authorize mapping authorship under a non-`GO` readiness
decision.

## 3. Selected approach

Follow the proven next-steps pattern: planning records and ready-to-file
issues first, then tracker hygiene, then a fail-closed public-source readiness
package, then bounded deepen work, with version identity **`v0.16-draft`**.

Ordered themes (owner-approved Approach A; Approach C deferred to the next
milestone):

1. **Tracker hygiene (post-v0.15)** — align GitHub with published
   `v0.15-draft` truth; close or annotate Issues `#181`–`#185` as historical;
   close GitHub milestone `v0.15-draft` when empty; open GitHub milestone
   `v0.16-draft`; keep Issue `#55` open when qualified UK review remains
   outstanding.
2. **NIST SP 800-53 Revision 5 public-source readiness** — pin official public
   source identity, checksums where obtainable, publication-rights boundary,
   provision-inventory feasibility, mechanical readiness matrix, and an
   evidenced `GO` / `HOLD` / `NO_GO` decision without creating unauthorized
   mapping records. Default acceptable exit is evidenced `HOLD` when people,
   rights, or source-access gates fail. Clone the NIST CSF / NIST AI RMF
   public-PDF inventory shape (not the ISO copyright-blocked inventory shape)
   because NIST SP 800-53 Rev 5 is publicly downloadable. While `HOLD` or
   `NO_GO`, no NIST SP 800-53 mapping records, snapshots, or catalog
   increments.
3. **United Kingdom jurisdiction profile deepen** — bounded Draft deepen of
   `profiles/uk/` from `0.1.0` to `0.2.0` under ESAF-1800; retain Draft
   lifecycle; preserve control meanings; do not import mapping outcomes; do
   not add a second industry or jurisdiction profile.
4. **Ordinary publication gates** on one exact `v0.16-draft` candidate.

Do not open all of roadmap Phases 4–6. Do not redesign `v1.0`. Do not treat
Issues `#55` or `#60` as exit criteria. Do not author NIST SP 800-53 mapping
records while the readiness decision is `HOLD` or `NO_GO`. Do not clear prior
HOLDs without their recorded reconsideration triggers and named people. Do not
execute Approach C (SOC 2 / CIS Controls readiness or a third Phase 6 toolkit
deepen) inside this milestone.

Execution order:

1. Land durable milestone / backlog / roadmap records and pinned issue bodies.
2. Complete tracker hygiene so GitHub matches repository truth.
3. Complete NIST SP 800-53 readiness (after hygiene; before publication).
4. Complete UK profile deepen (after hygiene; may overlap readiness; finish
   before publication).
5. Close ordinary publication gates on one exact `v0.16-draft` candidate.

## 4. Milestone shape

### Entry state

- `v0.15-draft` is published and its publication evidence is closed.
- ESAF-1500 remains Working Draft `0.1.1` with schemas, examples, and Phase 6
  Draft toolkit packs under `assessment/` and `templates/`.
- ESAF-1200 remains Working Draft `0.4.1`; ESAF-1000 remains Working Draft
  `0.2.1`; ESAF-1100 remains Working Draft `0.3.1`; ESAF-1300, ESAF-1400, and
  ESAF-1700 remain at Working Draft `0.3.0` depth with discoverable example
  packs.
- The UK jurisdiction profile remains Draft `0.1.0`.
- NIST AI RMF, ISO/IEC 42001, NIST CSF 2.0, ISO/IEC 27001, and PCI DSS
  readiness remain evidenced `HOLD`; mapping artifact counts for HOLD schemes
  remain `0`.
- No NIST SP 800-53 readiness package or mapping artifacts exist yet.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.16-draft` blockers.

### Required workstreams

1. **Tracker hygiene.** ESAF shall ensure Issue `#55` is open if and only if
   qualified UK mapping review remains outstanding, close or explicitly
   annotate Issues `#181`–`#185` as historical completed `v0.15-draft` work,
   close GitHub milestone `v0.15-draft` when it has no open issues, open
   GitHub milestone `v0.16-draft`, and align `project/BACKLOG.md` with
   published truth. This workstream does not change normative content.
2. **NIST SP 800-53 Revision 5 public-source readiness.** ESAF shall pin the
   applicable official NIST SP 800-53 Revision 5 source identity, establish
   publication-rights and provision-inventory boundaries, assess mapper and
   qualified-review availability, produce a mechanical readiness matrix, and
   record a `GO` / `HOLD` / `NO_GO` decision. The default acceptable exit is
   an evidenced `HOLD` that restates blockers, owners, reconsideration
   triggers, re-entry tests, and nonclaims. A matrix-derived `GO` is allowed
   only when every readiness gate clears, including named mapper and
   independent reviewer evidence. While the decision remains `HOLD` or
   `NO_GO`, ESAF shall not create NIST SP 800-53 mapping relationships,
   negative dispositions, snapshots, lifecycle events, registry entries, or
   catalog increments.
3. **United Kingdom jurisdiction profile deepen.** ESAF shall complete a
   bounded Draft deepen of the UK jurisdiction profile from `0.1.0` to
   `0.2.0` under ESAF-1800: publish a versioned `profiles/uk/0.2.0/` package,
   update the profile index, retain Draft lifecycle, preserve ESAF control
   meanings, keep composition with ESAF-1600 limited to pinned mapping
   identity without importing mapping outcomes, and avoid certification or
   external-scheme compliance claims.
4. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.16-draft` candidate, publish annotated tag `v0.16-draft`, and
   synchronize Working Draft status surfaces.

### Exit criteria

`v0.16-draft` is complete only when:

- tracker hygiene is complete: Issues `#181`–`#185` are closed or explicitly
  annotated as historical, GitHub milestone `v0.15-draft` is closed when empty,
  GitHub milestone `v0.16-draft` exists, and Issue `#55` is open if and only if
  qualified UK review remains outstanding;
- NIST SP 800-53 readiness is recorded as evidenced `GO`, `HOLD`, or `NO_GO`;
  if `HOLD` or `NO_GO`, NIST SP 800-53 mapping artifact count remains `0` and
  generated crosswalk catalog counts are unchanged by that workstream;
- the UK jurisdiction profile has a bounded deepen with Draft evidence at
  `0.2.0`, remains Draft, preserves control meanings, and does not import
  mapping outcomes or claim external-scheme compliance;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.16-draft` is published and Working Draft status surfaces
  (`VERSION.md`, README badges, changelog, roadmap, backlog, milestones, and
  readiness record) are synchronized.

### Non-goals

`v0.16-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping (Issue `#60`);
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` when named mapper and independent reviewers
  remain unavailable;
- clearing the ISO/IEC 42001 `HOLD`, NIST CSF `HOLD`, or ISO/IEC 27001 `HOLD`
  without recorded reconsideration triggers and named people;
- authoring NIST SP 800-53, ISO/IEC 27001, ISO/IEC 42001, NIST AI RMF, NIST
  CSF, or PCI DSS mapping records, snapshots, or catalog entries under a
  non-`GO` readiness decision;
- SOC 2 or CIS Controls readiness packages (preferred subsequent Approach C);
- a third Phase 6 toolkit deepen (preferred subsequent Approach C);
- a second industry or jurisdiction profile;
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

`project/BACKLOG.md` shall add a post-v0.15 queue that lists the four
workstreams above, while retaining:

- deferred assurance follow-up for Issue `#55`;
- separately gated HITRUST readiness for Issue `#60`; and
- completed `v0.15-draft` hygiene, readiness, deepen, and publication
  workstreams as historical context.

`ROADMAP.md` shall add a `0.16-draft` delivery sequence that states the order
of work (hygiene → NIST SP 800-53 readiness → UK profile deepen → publication)
and that Phases 4, 5, and 6 remain long-term direction except for the bounded
readiness and deepen work required by this milestone. Deferred mapping
assurance and HITRUST readiness remain tracked and do not stop later
engineering work. NIST SP 800-53 readiness may exit as evidenced `HOLD`.

`project/MILESTONES.md` shall add a `## v0.16-draft` section mirroring the
`v0.15-draft` structure (entry state, required workstreams, exit criteria,
non-goals).

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Sync post-v0.15 tracker hygiene
2. Complete NIST SP 800-53 Revision 5 public-source readiness and mapping go/no-go
3. Deepen United Kingdom jurisdiction profile to Draft 0.2.0
4. Close the v0.16-draft publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist. This planning
change does not create GitHub issues or edit GitHub tracker state.

Issue 3 may proceed in parallel with Issue 2 after hygiene acceptance criteria
are met, but Issues 2–3 shall finish before Issue 4. Issue 4 depends on
Issues 1–3.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS / HITRUST / NIST AI RMF /
ISO/IEC 42001 / NIST CSF / ISO/IEC 27001 blockers, open unauthorized mapping
authorship under `HOLD` or `NO_GO`, or establish certification, compliance,
equivalence, endorsement, assurance, or production readiness. Readiness and
profile deepen artifacts produced under this milestone remain Draft Working
Draft material only. An evidenced NIST SP 800-53 `HOLD` is an acceptable
milestone exit and does not authorize mapping records.
