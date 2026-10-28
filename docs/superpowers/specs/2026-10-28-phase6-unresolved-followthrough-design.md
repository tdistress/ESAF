# Phase 6 unresolved follow-through: bounded fourth deepen

## Purpose

Extend the Phase 6 assessment toolkit with one fictional example of an
inconclusive remediation follow-up. The example will show how an assessor
records an attempted test whose evidence is incomplete, preserves the prior
result, keeps the underlying concern open, and hands the unresolved exposure
to a governance risk review. The evidence establishes neither successful nor
failed control operation.

This is the next bounded deepen after the three toolkit deepens already
delivered and the integrated CAP-140 examples published in v0.18 and v0.19.
The v0.19 follow-up demonstrates a narrowly successful staging exercise. This
pass demonstrates the complementary outcome in which a test cannot establish
the intended restriction.

## Chosen approach

Add one inconclusive API-100-A3 follow-up to the existing fictional Summit
Analytics CAP-140 case. A staging test produces an inconclusive result because
the harness fails to capture a complete event trail. The new evidence record
and assessment result will use existing ESAF-1500 schemas. Because the
available evidence cannot support a determination, the result will use
`not_assessed` for determination, design effectiveness, and operating
effectiveness, with the required `scope_exclusion_rationale`, determination
rationale, and limitations explaining what could not be established. The
result will keep a new finding open. It will link to the prior results and
finding in narrative text, following the existing API-100 follow-up pattern;
this link will not alter any historical record. A governance thread will hand
the unresolved concern to a fictional risk review and record a next review
trigger without asserting formal risk acceptance or closure.

The result will be deliberately bounded to one staging exercise. It will not
claim that the control is ineffective in all contexts, establish production or
sustained effectiveness, or imply a final assessment outcome.

## Scope

- Add one technical-test evidence record and one Draft assessment-result
  example for the inconclusive follow-up, conforming to the existing
  `assessment/schema/evidence-record.schema.json` and
  `assessment/schema/assessment-result.schema.json` contracts.
- Add one short follow-up narrative explaining the test, the incomplete event
  trail, the open finding, the narrative relationship to the earlier API-100
  findings, and the limits of what could be concluded.
- Extend the integrated CAP-140 overview with links and a concise record-flow
  explanation that distinguishes the historical assessment, v0.19 successful
  scoped exercise, and this inconclusive exercise.
- Extend or add one governance-thread example linking the open finding to a
  risk review, an accountable owner, a bounded next action, and a review
  trigger. Do not record formal risk acceptance.
- Update the relevant assessment, workbook, and template indexes so the
  example is discoverable.

## Out of scope

- Changes to normative standards, controls, procedures, assessment criteria,
  schemas, identifier rules, lifecycle states, or maturity semantics.
- A generalized remediation workflow, a new reusable remediation template,
  production testing, repeated sampling, or a complete assessment library.
- External framework sources, mappings, readiness decisions, or assurance
  claims.
- Rewriting or replacing any historical CAP-140 record.

## Design constraints

- Reuse established record contracts and identifier/nesting patterns without
  inventing fields or identifier prefixes.
- Preserve the immutability of earlier fictional assessment results. The new
  result owns its own finding identifier and cites the prior finding in its
  narrative and disposition rationale.
- Distinguish an inconclusive test from a successful test and from a
  generalized conclusion that the control is ineffective. Encode the
  indeterminate result using only schema-supported `not_assessed` values and
  explain the evidence boundary in the rationale and limitations.
- Keep the governance risk review distinct from the assessment result and do
  not let it close, accept, or alter the assessment finding.
- Label all people, organizations, actions, dates, evidence, and judgments as
  fictional; retain Draft status and explicit nonclaims.

## Validation

- Validate the new evidence and result records with
  `python tools/validate_assessment.py --check`.
- Run focused assessment validation tests and the repository's full unittest
  suite, plus applicable link, control, architecture, release, and publication
  checks selected by `tools/plan_validation.py` for the candidate.
- Review the entire branch diff and obtain independent technical/editorial
  review on the exact candidate before publication.

## Acceptance criteria

- The new records validate against the existing schemas and have resolvable
  evidence/result references.
- The follow-up result is distinct, Draft, uses `not_assessed` for the
  determination and both effectiveness fields, explains the inconclusive
  evidence in its rationale and limitations, links to the prior finding
  through narrative text, and leaves its own finding open.
- The integrated overview makes the chronological and record ownership
  relationships clear without revising historic results.
- The governance handoff records a risk review and concrete future trigger
  without treating risk review as finding closure or formal risk acceptance.
- All touched indexes link to the new material, and nonclaims are explicit.
- Applicable exact-candidate validations and independent reviews pass with no
  unresolved Critical or Important findings.
