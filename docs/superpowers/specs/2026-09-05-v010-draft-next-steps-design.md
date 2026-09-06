# ESAF v0.10-draft Next-Steps Design

**Status:** Approved for implementation planning

**Date:** 2026-09-05

## 1. Purpose

Convert the post-`v0.9-rc1` planning gap into a bounded `v0.10-draft`
milestone whose headline deliverable is a Phase 6 assessment-toolkit starter,
preceded by tracker hygiene so repository truth matches GitHub.

This change shall:

- leave `v0.9-rc1` publication identity, annotated-tag evidence, and Draft
  lifecycle states for controls, architectures, profiles, and mappings
  unchanged;
- define measurable `v0.10-draft` entry conditions, workstreams, exit
  criteria, and non-goals;
- record the post-rc1 engineering and publication queue in durable project
  files; and
- supply ready-to-file GitHub issue bodies for the hygiene, toolkit, and
  publication workstreams.

## 2. Current state

The annotated tag `v0.9-rc1` is published (2026-08-29) at peel commit
`4136cfdc71a85ea2becd0f23c95424e7580cafa3`. Post-publication, ESAF-1300,
ESAF-1400, and ESAF-1700 were deepened to Working Draft `0.2.0` with example
packs; that deepen did not create a new tagged release.

ESAF-1500 remains the authoritative shared evidence, assessment-result, and
maturity foundation. `templates/` is still a placeholder. Roadmap Phase 6
(assessment toolkit) has no bounded milestone beyond long-term direction.

Tracker drift exists relative to durable policy:

- Issues `#90`–`#95` remain open though `v0.9-rc1` workstreams and publication
  gates are complete in repository records.
- Issue `#55` was closed by automation even though project files and
  release-metadata tests still require it to remain open until qualified UK
  mapping review completes.
- Issue `#60` (HITRUST readiness) remains open and externally gated.

There is no approved `v1.0` redesign.

## 3. Selected approach

Follow the proven `v0.9-rc1` pattern: planning records and ready-to-file
issues first (**D**), then a bounded usability content theme (**B**), with
version identity **`v0.10-draft`**.

Do not open all of roadmap Phases 4–6. Do not redesign `v1.0`. Take only a
Phase 6 *starter*: assessment workbook, evidence catalog, audit checklist,
and governance templates — all Draft, non-certified — after tracker hygiene.

Execution order:

1. Land durable milestone / backlog / roadmap records and pinned issue bodies.
2. Complete tracker hygiene so GitHub matches repository truth.
3. Author the four toolkit starters (parallelizable).
4. Close ordinary publication gates on one exact `v0.10-draft` candidate.

## 4. Milestone shape

### Entry state

- `v0.9-rc1` is published and its publication evidence is closed.
- ESAF-1300, ESAF-1400, and ESAF-1700 are at least at post-rc1 Working Draft
  `0.2.0` depth with discoverable example packs.
- ESAF-1500 foundation schemas and examples remain Draft and authoritative
  for shared assessment semantics.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.10-draft` blockers.
- ESAF-1000, ESAF-1100, ESAF-1200, ESAF-1600 method artifacts, the UK pilot
  profile, and the three UK mapping snapshots remain Draft.

### Required workstreams

1. **Tracker hygiene.** Reopen Issue `#55` if qualified UK mapping review is
   still outstanding. Close or explicitly annotate Issues `#90`–`#95` as
   historical completed `v0.9-rc1` work. Align `project/BACKLOG.md` and
   GitHub milestone state with published truth. This workstream does not
   change normative content.
2. **Assessment workbook Draft starter.** Author a Draft assessor workbook
   skeleton bound to ESAF-1500 shared contracts and ESAF-1100 control
   assessment procedures. The workbook shall not invent parallel evidence,
   result, or maturity semantics.
3. **Evidence catalog Draft starter.** Author a Draft starter catalog of
   evidence types and expectations reusable by profiles and crosswalks,
   aligned to the ESAF-1500 evidence contract.
4. **Audit checklist Draft starter.** Author a Draft checklist for
   control/capability sampling against the shared assessment-result
   contract.
5. **Governance templates Draft starter.** Author a Draft starter pack under
   `templates/` (risk, exception, decision, and retirement-class artifacts)
   linked from ESAF-1300 / ESAF-1400 without adding new normative
   requirements.
6. **Release closure.** Complete ordinary release gates on the exact
   `v0.10-draft` candidate, record counts and review results, publish the
   annotated tag, and synchronize Working Draft status surfaces.

### Exit criteria

`v0.10-draft` is complete only when:

- tracker hygiene is complete: Issues `#90`–`#95` are closed or explicitly
  annotated as historical, and Issue `#55` is open if and only if qualified
  UK review remains outstanding (repository truth matches GitHub);
- the assessment workbook, evidence catalog, audit checklist, and governance
  template starter each exist as Draft and are linked from applicable
  indexes;
- each toolkit pack reuses ESAF-1500 shared semantics and does not invent
  parallel maturity, evidence, or result contracts;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile,
  crosswalk, link, release, working-tree, and applicable Mermaid-rendering
  gates pass on the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.10-draft` is published and Working Draft surfaces
  (`VERSION.md`, README badges, changelog, roadmap, backlog, milestones, and
  readiness record) are synchronized.

### Non-goals

`v0.10-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six
  qualified UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping (Issue `#60`);
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` or authoring NIST mapping records;
- all roadmap crosswalks or all planned industry profiles;
- advancing Draft controls, architectures, mappings, or profiles to an
  approved lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.

## 5. Backlog and roadmap updates

`project/BACKLOG.md` shall add a post-rc1 queue that lists the six workstreams
above, while retaining:

- deferred assurance follow-up for Issue `#55` (after hygiene restores
  correct open state if still required);
- separately gated HITRUST readiness for Issue `#60`; and
- completed `v0.9-rc1` and ESAF-1300/1400/1700 0.2.0 workstreams as
  historical context.

`ROADMAP.md` shall add a `0.10-draft` delivery sequence that states the order
of work and that Phases 4 and 5 remain long-term direction. Phase 6 remains
long-term direction except for the bounded starter packs required by this
milestone. Deferred mapping assurance and HITRUST readiness remain tracked
and do not stop later engineering work.

`project/MILESTONES.md` shall add a `## v0.10-draft` section mirroring the
`v0.9-rc1` structure (entry state, required workstreams, exit criteria,
non-goals).

## 6. Ready-to-file issues

The implementation plan shall include issue titles, labels, and bodies for:

1. Sync post-rc1 tracker hygiene
2. Author assessment workbook Draft starter
3. Author evidence catalog Draft starter
4. Author audit checklist Draft starter
5. Author governance templates Draft starter
6. Close the v0.10-draft publication gates

Issue creation in GitHub may occur after the planning PR merges. The durable
repository records remain authoritative until those issues exist.

Issues 2–5 may proceed in parallel after hygiene acceptance criteria are met.
Issue 6 depends on Issues 2–5.

## 7. Nonclaims

This planning change does not publish a release, change artifact lifecycle
states, complete qualified review, clear PCI DSS / HITRUST / NIST AI RMF
blockers, or establish certification, compliance, equivalence, endorsement,
assurance, or production readiness. Toolkit artifacts produced under this
milestone remain Draft Working Draft material only.
