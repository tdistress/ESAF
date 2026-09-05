# Milestones

| Milestone | Scope |
|---|---|
| v0.1-alpha | Project foundation, governance, terminology, lifecycle, and repository conventions |
| v0.2-alpha | ESAF-1000 enterprise standard working draft |
| v0.3-alpha | Initial normative control catalog |
| v0.4-alpha | Initial reference architectures |
| v0.5-beta | Priority crosswalks and industry profiles |
| v0.9-rc1 | Editorially complete release candidate |
| v1.0 | First approved publication |

## v0.5-beta

### Entry state

- `v0.4-alpha` is published and its publication evidence is closed.
- ESAF-1600, its schemas, lifecycle model, and validators are present.
- The three UK mapping snapshots remain Draft and await qualified review.

### Publication state

- The `v0.5-beta` Working Draft was published on 2026-08-01 through annotated
  tag `v0.5-beta` at `255f8806917aaf8c6a2441152b4638fc9fd2bfda`.
- Publication closes the repository release gates only. Controls,
  architectures, profiles, mapping sets, and mapping records remain Draft.
- Issue 55 remains open for qualified review; owner-risk acceptance does not
  approve mappings or change an artifact lifecycle state.

### Required workstreams

1. **UK mapping assurance.** ESAF shall record either completed
   qualified-review dispositions for all three UK mapping sets or one
   coordinated owner-risk disposition that defers qualified review for all
   three sets on the exact `v0.5-beta` release candidate. Core and Plus remain
   separate mapping sets. Under the deferred path, `DEFERRED` is a milestone
   assurance disposition, not an ESAF-1600 mapping lifecycle state. All three
   mapping sets and their records remain Draft.
2. **Minimum assessment foundation.** ESAF shall define the minimum ESAF-1500
   assessment foundation: the common evidence model, assessment-result
   contract, and maturity-scoring semantics needed by crosswalks and profiles.
   This foundation shall be complete before the pilot profile workstream begins.
3. **Pilot profile.** ESAF shall select, design, validate, and publish one
   Draft pilot industry or jurisdiction profile using a reusable profile
   contract. Profile selection is an explicit owner decision; it is not
   hard-coded by this milestone.
4. **PCI DSS readiness and mapping decision.** ESAF shall pin the applicable
   official PCI DSS version and sources, establish publication-rights and
   provision-inventory boundaries, identify qualified-review requirements, and
   record a mapping decision. `GO` means the approved Draft mapping scope is
   completed. `HOLD` permits milestone closure only when the blocking
   condition, reconsideration trigger, and non-claim boundary are recorded.
5. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.5-beta` candidate and record its own counts and review results.

### Exit criteria

`v0.5-beta` is complete only when:

- all three UK mapping sets have either completed qualified-review
  dispositions or one coordinated owner-risk disposition that defers
  qualified review for all three sets on the exact `v0.5-beta` release
  candidate;
- the minimum ESAF-1500 assessment foundation is internally consistent, linked
  from applicable indexes, and validated;
- one Draft pilot profile conforms to the reusable profile contract and uses
  the shared assessment semantics;
- the PCI DSS workstream has reached its approved `GO` deliverable or a
  formally evidenced `HOLD` disposition;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, crosswalk, link, release,
  working-tree, and applicable Mermaid-rendering gates pass on the exact
  candidate;
- Critical and Important review findings are resolved; and
- the exact candidate receives technical, editorial, mapping, and governance
  approval appropriate to its contents.

### Non-goals

`v0.5-beta` does not require:

- all roadmap crosswalks;
- all nine planned profiles;
- a complete assessment workbook, audit checklist, or governance-template
  library;
- substantive HITRUST CSF mapping without licensed-source access,
  publication-rights confirmation, and qualified-review availability;
- advancing Draft controls, architectures, mappings, or profiles to an
  approved lifecycle state without their own evidence; or
- redesigning `v0.9-rc1` and `v1.0`.

## v0.9-rc1

### Entry state

- `v0.5-beta` is published and its publication evidence is closed.
- Issues `#55` and `#60` may remain open; they are not `v0.9-rc1` blockers.
- ESAF-1000, ESAF-1100, ESAF-1200, the ESAF-1500 foundation, ESAF-1600, the UK
  pilot profile, and the three UK mapping snapshots remain Draft.

### Publication state

- The `v0.9-rc1` Working Draft was published on 2026-08-29 through annotated
  tag `v0.9-rc1`.
- The first Working Draft scope for ESAF-1300, ESAF-1400, and ESAF-1700 was
  completed for that publication. The historical requirements and exit
  criteria below remain the record of the closed milestone.

### Required workstreams

1. **Validation-harness Phase 2 closeout.** ESAF shall land the remaining
   mapping-review bundle mutation-matrix hot path with equivalence proof and
   record the hosted full-suite performance measurement against the sealed
   Phase 2 acceptance criteria. This workstream does not change normative
   content.
2. **ESAF-1300 first Working Draft.** ESAF shall author the Governance Manual
   foundation covering decision rights, lifecycle gates, exception handling,
   and RACI sufficient for editorial and link validation.
3. **ESAF-1400 first Working Draft.** ESAF shall author the Implementation
   Guide foundation with practical, non-normative adoption guidance that
   references existing controls and architectures without inventing parallel
   requirements.
4. **ESAF-1700 first Working Draft.** ESAF shall author the Enterprise AI Data
   Model foundation defining canonical entities, attributes, relationships,
   and exchange guidance aligned to ESAF-1500 assessment records where
   applicable.
5. **Next public-source crosswalk readiness.** ESAF shall pin one public
   external framework—default NIST AI RMF 1.0 unless the owner selects another
   public source—and complete source inventory, publication-rights boundary,
   provision-inventory feasibility, and a `GO` / `HOLD` / `NO_GO` readiness
   decision without creating unauthorized mapping records.
6. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.9-rc1` candidate and record its own counts and review results.

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

### Post-publication breadth deepen

- The ESAF-1300, ESAF-1400, and ESAF-1700 0.2.0 breadth deepen is complete.
- Each publication now has a discoverable non-normative example pack under
  `examples/esaf-1300/`, `examples/esaf-1400/`, or `examples/esaf-1700/`.
- This follow-up does not alter the closed `v0.9-rc1` publication state or
  create a new tagged release.

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

## v0.10-draft

### Entry state

- `v0.9-rc1` is published and its publication evidence is closed.
- ESAF-1300, ESAF-1400, and ESAF-1700 are at least at post-rc1 Working Draft
  `0.2.0` depth with discoverable example packs.
- ESAF-1500 foundation schemas and examples remain Draft and authoritative for
  shared assessment semantics.
- Issues `#55` and `#60` may remain open after hygiene; they are not
  `v0.10-draft` blockers.
- ESAF-1000, ESAF-1100, ESAF-1200, ESAF-1600 method artifacts, the UK pilot
  profile, and the three UK mapping snapshots remain Draft.

### Required workstreams

1. **Tracker hygiene.** ESAF shall reopen Issue `#55` if qualified UK mapping
   review remains outstanding, close or explicitly annotate Issues `#90`–`#95`
   as historical completed `v0.9-rc1` work, and align backlog and GitHub
   milestone state with published truth. This workstream does not change
   normative content.
2. **Assessment workbook Draft starter.** ESAF shall author a Draft assessor
   workbook skeleton bound to ESAF-1500 shared contracts and ESAF-1100 control
   assessment procedures without inventing parallel evidence, result, or
   maturity semantics.
3. **Evidence catalog Draft starter.** ESAF shall author a Draft starter catalog
   of evidence types and expectations reusable by profiles and crosswalks,
   aligned to the ESAF-1500 evidence contract.
4. **Audit checklist Draft starter.** ESAF shall author a Draft checklist for
   control/capability sampling against the shared assessment-result contract.
5. **Governance templates Draft starter.** ESAF shall author a Draft starter pack
   under `templates/` covering risk, exception, decision, and retirement-class
   artifacts, linked from ESAF-1300 / ESAF-1400 without adding new normative
   requirements.
6. **Release closure.** ESAF shall complete ordinary release gates on the exact
   `v0.10-draft` candidate, publish annotated tag `v0.10-draft`, and synchronize
   Working Draft status surfaces.

### Exit criteria

`v0.10-draft` is complete only when:

- tracker hygiene is complete: Issues `#90`–`#95` are closed or explicitly
  annotated as historical, and Issue `#55` is open if and only if qualified UK
  review remains outstanding;
- the assessment workbook, evidence catalog, audit checklist, and governance
  template starter each exist as Draft and are linked from applicable indexes;
- each toolkit pack reuses ESAF-1500 shared semantics and does not invent
  parallel maturity, evidence, or result contracts;
- generated catalogs and affected traceability records are current;
- the full test suite, control, architecture, assessment, profile, crosswalk,
  link, release, working-tree, and applicable Mermaid-rendering gates pass on
  the exact candidate;
- Critical and Important review findings are resolved;
- the exact candidate receives technical, editorial, and governance approval
  appropriate to its contents; and
- annotated tag `v0.10-draft` is published and Working Draft surfaces are
  synchronized.

### Non-goals

`v0.10-draft` does not require:

- closing Issue `#55` via owner-risk acceptance or completing the six qualified
  UK mapping role dispositions;
- licensed HITRUST CSF access or substantive HITRUST mapping;
- clearing the PCI DSS `HOLD` without its recorded reconsideration triggers;
- clearing the NIST AI RMF `HOLD` or authoring NIST mapping records;
- all roadmap crosswalks or all planned profiles;
- advancing Draft controls, architectures, mappings, or profiles to an approved
  lifecycle state without their own evidence;
- a certification or accreditation scheme; or
- redesigning `v1.0`.
