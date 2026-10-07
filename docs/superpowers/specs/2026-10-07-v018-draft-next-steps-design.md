# ESAF v0.18-draft Next-Steps Design

**Status:** Approved by the project owner for implementation planning

**Date:** 2026-10-07

## 1. Purpose

Define a bounded `v0.18-draft` milestone centered on one integrated, fictional
ESAF-1500 assessment case. The case will make the existing Summit Analytics
`CAP-140` workbook, audit-sampling, evidence, and governance examples read as
one coherent engagement from scoping through governance follow-up.

The milestone will:

- establish the project scope, delivery sequence, entry state, exit criteria,
  and non-goals for `v0.18-draft`;
- reconcile the overlapping API-100 workbook and audit-sampling examples and
  complete missing evidence links for the sampled MOD-100 control;
- connect evidence capture, assessment results, maturity, limitations, risks,
  and governance actions through one discoverable case overview;
- keep all assessment content fictional, non-normative, and Draft; and
- close ordinary publication gates and synchronize Working Draft status
  surfaces on the exact candidate.

This milestone does not depend on qualified external crosswalk reviewers.
Technical, editorial, governance, validation, and publication gates remain
applicable.

## 2. Current state

The `v0.17-draft` Working Draft was published on 2026-09-16. Its tracker
hygiene, CIS Controls Version 8 readiness decision, Phase 6 third deepen, and
publication work are complete. CIS Controls readiness remains `HOLD`; no
mapping records were authorized by that decision.

PR #222 merged on 2026-10-07 as commit
`04f7b6c058dd776d51d5cba37a808dda555a4511`. It strengthened SOC 2 readiness
evidence and left the SOC 2 decision at `HOLD`. The SOC 2 and HITRUST readiness
workstreams remain separately gated. They are not prerequisites or exit
criteria for `v0.18-draft`.

The assessment toolkit already contains:

- a third workbook vignette and a filled evidence/result/maturity trio for
  Summit Analytics `CAP-140` and `API-100`;
- a third audit-sampling vignette and filled results for `API-100` and
  `MOD-100` under the same capability and fictional organization;
- a `MOD-100` result that references registry evidence, but no corresponding
  filled ESAF-1500 evidence-record example for that registry artifact;
- evidence-catalog examples for configuration and record evidence; and
- a third governance thread linking CAP-140 risk, sidecar retirement, and one
  workbook evidence record.

The existing third workbook and audit examples use different engagement,
API-100 evidence, and API-100 result identifiers for overlapping work. The
governance thread uses the workbook identifiers but does not connect the
MOD-100 sample. This leaves readers to infer whether the examples form one
engagement and how the artifacts relate.

## 3. Selected approach

Use the existing Summit Analytics `CAP-140` examples as the canonical case.
Do not create a parallel organization or a second set of competing third-pass
vignettes. Preserve the first and second standalone workbook, catalog,
sampling, and template examples.

The integrated case will have one authoritative identity and consistent
cross-references for its scope, evidence, assessment results, maturity view,
limitations, risk, and governance follow-up. Where multiple existing records
describe the same API-100 artifact or determination, reconcile them to one
canonical record and preserve the distinct procedures, sampling work, and
limitations that each example contributes. A single result may be referenced
from both the workbook narrative and audit checklist; duplicated result
records shall not imply separate determinations for the same work.

Add one overview document at
`assessment/integrated-assessment.example.md`. It will serve as the reader's
entry point and explain the fictional engagement, artifact flow, and links to
the existing records in their established locations. Update the third
workbook vignette and records, third audit-sampling vignette and records, and
third governance thread as needed to make them consistent with that overview.
Add a filled evidence-record example for the MOD-100 registry artifact so the
referenced evidence has a complete ESAF-1500 record. Retain evidence-catalog
examples as catalog demonstrations; link to their type-specific guidance
without treating standalone catalog-demo identifiers as engagement evidence.

The assessment scope remains one fictional Summit Analytics capability,
`CAP-140`, with the existing sampled controls `API-100` and `MOD-100`. The case
will not imply coverage of the entire capability, control family, enterprise,
or any external framework. Existing procedures and ESAF-1500 schemas remain
authoritative.

## 4. Integrated case flow

The overview and linked artifacts will let a reader follow this sequence:

1. **Define engagement scope.** Identify purpose, capability, assessment
   period, selected controls, population and sample, assessor independence,
   exclusions, and scope limitations.
2. **Capture evidence.** Record the API-100 gateway configuration and the
   MOD-100 model-registry artifact under the shared evidence-record schema.
   Procedure-level test and interview work remains explicitly described in
   the corresponding assessment results and audit checklist.
3. **Perform control assessment.** Reconcile the API-100 workbook result with
   the API-100 audit result and preserve the API-100-A1 examination and
   API-100-A2 test details. Retain the MOD-100 examination, deployment
   reconciliation, and interview procedure references in one linked result.
4. **Record outcomes and limitations.** Keep the results `draft` where the
   fictional finding, evidence gap, sample limit, or staging limitation
   remains unresolved. Do not turn one satisfied sampled control into a
   capability-wide or enterprise-wide conclusion.
5. **Record maturity separately.** Retain a maturity assessment only for its
   defined scope and cite its evidence and assessment-result IDs. Do not
   derive maturity mechanically from control determinations or roll it up to
   the entire CAP-140 capability.
6. **Connect governance follow-up.** Link the relevant residual risk, decision
   or exception as applicable, and sidecar retirement record to the assessment
   evidence and result. Preserve the distinction between a control finding,
   risk acceptance, implementation action, and retirement verification.

The case remains illustrative. Fictional people, organizations, evidence,
dates, decisions, records, and results shall be labeled as such.

## 5. Workstreams and sequence

### Workstream 1 — v0.18-draft planning and tracker alignment

Record the approved scope, entry conditions, bounded deliverable, exit
criteria, and non-goals in the project milestone, roadmap, backlog, and
release-planning surfaces. Track implementation and publication work in
GitHub under milestone `v0.18-draft`. Keep the open SOC 2 and HITRUST issues
separately gated and unassigned as prerequisites.

### Workstream 2 — Integrated Summit Analytics assessment case

Create the overview and reconcile the existing third workbook, evidence,
audit-sampling, and governance artifacts to one canonical case. Add the
MOD-100 evidence record required to complete the chain. Update all relevant
indexes and cross-references. Do not add a new standard, methodology, schema,
control, or external mapping.

### Workstream 3 — Ordinary validation and publication

Run the applicable assessment and control validators, focused artifact
validation, full test suite, link checks, release checks, and whole-branch
review. Complete technical, editorial, and governance review on the exact
candidate. Resolve Critical and Important findings before publication, publish
the annotated `v0.18-draft` tag only after required gates pass, and synchronize
Working Draft status surfaces.

The delivery sequence is planning and tracker alignment, integrated case
implementation, validation and review, then publication closure.

## 6. Entry conditions

`v0.18-draft` may begin when:

- `v0.17-draft` publication and its exact-candidate evidence remain recorded;
- PR #222 is merged on `main` and its SOC 2 readiness outcome remains `HOLD`;
- existing assessment schemas and ESAF-1100 procedures are the source of
  truth for the example records; and
- the integrated case remains bounded to the existing fictional Summit
  Analytics `CAP-140` scope and sampled `API-100` and `MOD-100` controls.

## 7. Exit criteria

`v0.18-draft` is complete only when:

- the project planning files and GitHub milestone/issues describe the same
  approved, bounded scope;
- a discoverable integrated-case overview links to the workbook, evidence,
  audit, maturity, and governance artifacts in their established locations;
- the API-100 workbook and audit materials share one canonical evidence and
  assessment-result identity for the same examination/test work, with all
  distinct procedures and limitations retained;
- MOD-100 has a filled evidence record matching the evidence cited by its
  assessment result, and its procedures, result, checklist, and case overview
  agree;
- all cross-artifact identifiers and links are consistent, every JSON example
  conforms to its existing schema, and the case remains explicitly fictional
  and Draft;
- maturity remains a separate axis and the case makes no capability-wide,
  enterprise-wide, external-framework, compliance, certification, equivalence,
  endorsement, or assurance claim;
- applicable validation gates, full tests, technical/editorial/governance
  reviews, and publication checks pass on the exact candidate, with no
  unresolved Critical or Important findings; and
- the annotated `v0.18-draft` publication and all applicable Working Draft
  status surfaces are synchronized.

## 8. Non-goals and boundaries

`v0.18-draft` does not require:

- a qualified external crosswalk verifier, independent standards mapper, or
  external framework reviewer;
- SOC 2, HITRUST, CIS Controls, or other external framework readiness,
  inventory, mapping, or publication work;
- clearing or changing any existing crosswalk `HOLD` or `GO` decision;
- new normative requirements, maturity semantics, assessment criteria,
  control procedures, schemas, identifier prefixes or schemes, or lifecycle
  states. Example record IDs shall follow the existing ESAF-1500 patterns;
- a complete assessment-library or all-controls implementation;
- final assessment results, approved lifecycle states, or claims about a real
  organization; or
- another general Phase 6 breadth-deepen pass beyond what is needed to make
  this single integrated case coherent and discoverable.

Ordinary technical, editorial, governance, and repository validation gates
remain required. The absence of a qualified external verifier does not waive
those gates or permit claims beyond the Draft fictional example.
