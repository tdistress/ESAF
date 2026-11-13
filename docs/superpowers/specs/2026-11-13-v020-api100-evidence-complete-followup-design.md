# v0.20 API-100 evidence-complete follow-up

## Purpose

Extend the fictional Summit Analytics CAP-140 case with one later API-100-A3
staging exercise that has a complete event trail. Add a separate assessment
result that resolves only the scoped open finding created by the inconclusive
follow-up. This demonstrates how a later, reviewable evidence package can
support a bounded reassessment without replacing prior records.

## Chosen approach

Add one fictional evidence record for a single staging exercise, a new Draft
assessment result, and a concise narrative that links the evidence to
`ASR-ENG5-API100-A3-INCONCLUSIVE` and
`FND-ENG5-API100-A3-INCONCLUSIVE`. Reuse existing ESAF-1500 schemas and
identifier patterns. The result may record `partially_satisfied` and
`partially_effective` for the single API-100-A3 exercise, with
`operating_effectiveness` remaining `not_assessed`. It will own a distinct
finding ID and resolve only that finding's bounded evidence-capture gap. It
will not revise any earlier result.

## Scope

- Add one fictional technical-test evidence record with a complete,
  attributable, time-bounded staging event trail and linked result ID.
- Add one Draft assessment result consuming only that evidence for one
  API-100-A3 follow-up. Link to the prior inconclusive result and finding in
  the rationale, and resolve a distinct finding for the scoped follow-up.
- Add a short follow-up narrative explaining the chronology, evidence, result,
  finding ownership, and explicit limits.
- Link the narrative and records from the integrated assessment and the
  relevant assessment and workbook indexes.
- Define the bounded v0.20-draft milestone and publication gates in the
  project milestone, backlog, and release-plan records. Track the work in
  GitHub milestone 14 and Issues #234 and #235.

## Boundaries

- Preserve `ASR-ENG3-API100`, `ASR-ENG4-API100-A3`, and
  `ASR-ENG5-API100-A3-INCONCLUSIVE` unchanged.
- Assess only one fictional staging exercise under API-100-A3. Do not imply
  that one exercise establishes production behavior, recovery behavior,
  repeated or sustained effectiveness, or API-100-A1/A2 outcomes.
- Do not change normative requirements, controls, procedures, schemas,
  maturity semantics, identifier rules, or lifecycle states.
- Do not add external framework mappings or claims of compliance,
  certification, equivalence, endorsement, or assurance. SOC 2 (#219) and
  HITRUST (#60) remain outside scope.

## Acceptance criteria

- The evidence and result validate against the existing schemas and their
  cross-references resolve.
- The new result remains Draft, is linked to the evidence and prior
  inconclusive result, uses bounded outcome fields, and resolves only its own
  distinct follow-up finding.
- The prior inconclusive result and all earlier records remain unchanged.
- The narrative and indexes make record chronology and limits clear.
- Milestone and release-plan text match the GitHub milestone and issues.
- Focused tests and all applicable exact-candidate validation and independent
  review gates pass with no unresolved Critical or Important findings.
