# ESAF v0.9-rc1 Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-08-29

## 1. Purpose

Convert the post-`v0.5-beta` planning gap into a bounded `v0.9-rc1` milestone
and a schedulable queue for work that is not already covered by open GitHub
issues `#55` and `#60`.

This change shall:

- leave `v0.5-beta` publication truth, Draft lifecycle states, owner-risk
  mapping basis, and Issues `#55` / `#60` unchanged;
- define measurable `v0.9-rc1` entry conditions, workstreams, exit criteria,
  and non-goals;
- record the post-beta engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for work that currently has no open
  issue.

## 2. Current state

The annotated tag `v0.5-beta` is published. Open issues are limited to:

- `#55` — qualified human review of the three UK mapping snapshots; and
- `#60` — HITRUST CSF source and review readiness.

Both remain externally gated. Roadmap Phases 4 through 6, the charter stubs for
ESAF-1300 / ESAF-1400 / ESAF-1700, and the unfinished validation-harness Phase 2
closeout have no open issues and no milestone definition beyond a one-line
`v0.9-rc1` table row.

## 3. Selected approach

Use a bounded `v0.9-rc1` redesign rather than opening the entire remaining
roadmap or redesigning `v1.0`.

`v0.9-rc1` shall mean an editorially complete Working Draft release candidate
for the current publication set: fill the empty charter packages, finish the
in-flight validation-harness efficiency closeout, add one additional
public-source crosswalk readiness package, and keep external-gated work
outside the exit criteria.

## 4. Milestone shape

### Entry state

- `v0.5-beta` is published and its publication evidence is closed.
- Issues `#55` and `#60` may remain open.
- ESAF-1000, ESAF-1100, ESAF-1200, ESAF-1500 foundation, ESAF-1600 method, the
  UK pilot profile, and the three UK mapping snapshots remain Draft.

### Required workstreams

1. **Validation-harness Phase 2 closeout.** Land the remaining mapping-review
   bundle mutation-matrix hot path, retain equivalence proofs, and record the
   hosted full-suite performance measurement against the sealed Phase 2
   acceptance criteria. This workstream does not change normative content.
2. **ESAF-1300 first Working Draft.** Author the Governance Manual foundation
   covering decision rights, lifecycle gates, exception handling, and RACI
   sufficient for editorial and link validation.
3. **ESAF-1400 first Working Draft.** Author the Implementation Guide
   foundation with practical, non-normative adoption guidance that references
   existing controls and architectures without inventing parallel requirements.
4. **ESAF-1700 first Working Draft.** Author the Enterprise AI Data Model
   foundation defining canonical entities, attributes, relationships, and
   exchange guidance aligned to ESAF-1500 assessment records where applicable.
5. **Next public-source crosswalk readiness.** Pin one public external
   framework—default NIST AI RMF 1.0 unless the owner selects another public
   source—and complete source inventory, publication-rights boundary,
   provision-inventory feasibility, and a `GO` / `HOLD` / `NO_GO` readiness
   decision without creating unauthorized mapping records.
6. **Release closure.** Complete ordinary release gates on the exact
   `v0.9-rc1` candidate and record counts and review results.

### Exit criteria

`v0.9-rc1` is complete only when:

- the validation-harness Phase 2 closeout is merged and its hosted measurement
  evidence is recorded;
- ESAF-1300, ESAF-1400, and ESAF-1700 each have an internally consistent
  Working Draft linked from applicable indexes and validated;
- the selected public-source crosswalk readiness package has an evidenced
  `GO`, `HOLD`, or `NO_GO` disposition;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved; and
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents.

### Non-goals

`v0.9-rc1` does not require:

- closing Issue `#55` or completing qualified UK mapping review;
- licensed HITRUST CSF access or substantive HITRUST mapping;
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an
  approved lifecycle state without their own evidence;
- a complete assessment workbook, audit-checklist library, or every template
  named in `templates/README.md`; or
- redesigning `v1.0`.

## 5. Backlog and roadmap updates

`project/BACKLOG.md` shall add a post-beta queue that lists the six workstreams
above as initiatives awaiting GitHub Issues, while retaining:

- deferred assurance follow-up for Issue `#55`;
- separately gated HITRUST readiness for Issue `#60`; and
- completed `v0.5-beta` workstreams.

`ROADMAP.md` shall add a `0.9-rc1` delivery sequence that states the order of
work and that Phases 4 through 6 remain long-term direction rather than
`v0.9-rc1` exit criteria. Deferred mapping assurance and HITRUST readiness
remain tracked and do not stop later engineering work.

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Close validation-harness Phase 2 performance target
2. Author ESAF-1300 Governance Manual Working Draft
3. Author ESAF-1400 Implementation Guide Working Draft
4. Author ESAF-1700 Enterprise AI Data Model Working Draft
5. Complete NIST AI RMF public-source readiness and mapping go/no-go
6. Close the v0.9-rc1 publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS or HITRUST blockers, or
establish certification, compliance, equivalence, endorsement, assurance, or
production readiness.
