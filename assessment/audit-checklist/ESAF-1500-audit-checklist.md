# ESAF-1500 Audit Checklist

**Status:** Draft starter  
**Authority:** [ESAF-1500](../ESAF-1500.md) assessment-result contract;
[ESAF-1100](../../controls/ESAF-1100.md) assessment procedures and methods.

## Purpose

Support control or capability sampling engagements that capture determinations
in the shared ESAF-1500 assessment-result vocabulary. Do not invent parallel
determination, effectiveness, or method names.

## Engagement header

| Field | Operator entry |
|---|---|
| Engagement identifier | |
| Assessed subject / capability | |
| In-scope requirement IDs | |
| Boundary and exclusions | |
| Assessment period | |
| Assessor / independence | |

## Sampling intent

Define the population and sample before collecting evidence.

| Checkpoint | Complete? | Notes |
|---|---|---|
| Population of controls, capabilities, or artifacts is defined | [ ] | |
| Sample size and selection rationale are recorded | [ ] | |
| Exclusions and non-sampled items are explicit | [ ] | |
| Sampling approach matches engagement risk and purpose | [ ] | |

## Procedure references

For each sampled requirement, reference the ESAF-1100 assessment procedures and
authorized methods only: `Examine`, `Interview`, `Test`, and `Observe`.

| Requirement ID | Procedure ID(s) | Method(s) | Object / population | Work performed | Complete? |
|---|---|---|---|---|---|
| | | | | | [ ] |
| | | | | | [ ] |
| | | | | | [ ] |

## Evidence pointers

Point to ESAF-1500 evidence records by `evidence_id`. Prefer catalog types from
[`../evidence-catalog/`](../evidence-catalog/).

| Evidence ID | Type | Requirement ID(s) | Sufficiency | Limitations noted? | Complete? |
|---|---|---|---|---|---|
| | | | | [ ] | [ ] |
| | | | | [ ] | [ ] |
| | | | | [ ] | [ ] |

## Determination capture

Record one ESAF-1500 determination per assessed requirement set. Allowed values
are `satisfied`, `partially_satisfied`, `not_satisfied`, `not_applicable`, and
`not_assessed`. Pair design and operating effectiveness using only
`effective`, `partially_effective`, `ineffective`, `not_applicable`, or
`not_assessed`.

| Result ID | Requirement ID(s) | Determination | Design effectiveness | Operating effectiveness | Rationale summary | Status (`draft`/`final`) | Complete? |
|---|---|---|---|---|---|---|---|
| | | | | | | `draft` | [ ] |
| | | | | | | `draft` | [ ] |

Rules of use:

- Keep `status` as `draft` until methods, evidence, and rationale are complete.
- A `not_applicable` determination also needs an approved applicability rationale
  and approver in the assessment-result record.
- A `not_assessed` determination also needs a scope-exclusion rationale.
- Findings, if any, stay nested in the assessment-result `findings` array.

## Limitation notes

| Limitation | Impact on determination | Residual action | Complete? |
|---|---|---|---|
| | | | [ ] |
| | | | [ ] |

Before promoting any result to `final`, confirm limitations remain accurate and
visible.

## Nonclaims

This Draft starter does not create a certification audit program and does not
approve certification, compliance, equivalence, endorsement, assurance, or
production readiness. Checklist completion does not satisfy controls by itself.
