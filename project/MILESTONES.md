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

### Required workstreams

1. **Qualified UK mapping review.** ESAF shall complete independent, qualified
   human review of all three UK mapping snapshots as one coordinated initiative.
   Core and Plus remain separate mapping sets.
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

- all three UK mapping snapshots have qualified-review dispositions recorded
  under ESAF-1600;
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
