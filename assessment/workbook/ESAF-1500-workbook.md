# ESAF-1500 Operator Workbook

**Status:** Draft starter  
**Authority:** [ESAF-1500](../ESAF-1500.md) for shared evidence, result, and
maturity semantics; [ESAF-1100](../../controls/ESAF-1100.md) for control
requirements and assessment procedures.

## 1. Engagement scope (fill in)

Record the engagement before collecting evidence. Do not invent parallel
scope vocabulary.

| Field | Operator entry |
|---|---|
| Engagement identifier | |
| Purpose | |
| Subject / system boundary | |
| In-scope ESAF-1100 control IDs | |
| Explicit exclusions | |
| Assessment period (start / end) | |
| Population and sampling approach | |
| Assessor name, role, organization | |
| Independence statement | |
| Known limitations at kickoff | |

## 2. Evidence workflow

1. For each artifact, copy
   [`worksheets/evidence-record.worksheet.json`](worksheets/evidence-record.worksheet.json).
2. Assign a stable `evidence_id` matching `^EVD-[A-Z0-9][A-Z0-9-]*$`.
3. Complete every required ESAF-1500 evidence field, including all seven
   quality attributes and sufficiency.
4. Link `traceability.requirement_refs` to ESAF-1100 control IDs (or approved
   engagement requirement IDs) and `procedure_refs` to the control assessment
   procedures you executed.
5. Keep limitations visible; do not delete known gaps to force sufficiency.

## 3. Procedure steps (ESAF-1100 methods)

For each in-scope control, execute the control’s assessment procedures using
only ESAF-1100 methods:

| Method | Typical use |
|---|---|
| Examine | Policies, configurations, records, logs, designs, samples |
| Interview | Accountable and knowledgeable personnel |
| Test | Exercise, sample, query, or technically verify operation |
| Observe | Directly witness process or control performance |

Record method, object, population or sample, expected result, and work
performed in the assessment-result worksheet `methods` array. Do not create
new method names.

## 4. Findings and dispositions

Capture findings only inside the assessment-result worksheet `findings`
array using ESAF-1500 severity and status values. Tie each finding to
`evidence_refs` and affected requirement IDs. Record disposition action and
rationale when closing a finding.

## 5. Assessment results

1. Copy
   [`worksheets/assessment-result.worksheet.json`](worksheets/assessment-result.worksheet.json).
2. Keep `status` as `draft` until evidence, methods, and rationale are
   complete; promote to `final` only when ESAF-1500 final-state rules are met.
3. Use ESAF-1500 determination and effectiveness enumerations only.
4. Reference evidence solely by `evidence_id` values in `evidence_refs`.

## 6. Maturity (optional axis)

Control conformance and maturity remain independent. If the engagement
includes maturity:

1. Copy
   [`worksheets/maturity-assessment.worksheet.json`](worksheets/maturity-assessment.worksheet.json).
2. Claim only levels substantiated by `basis_refs` to evidence and/or result
   IDs.
3. Do not infer maturity from a single determination, and do not invent
   levels outside `M0`–`M4`.

## 7. Traceability checklist

Before closing an engagement package, confirm:

- [ ] Every evidence record validates against the evidence-record schema
- [ ] Every result validates against the assessment-result schema
- [ ] Every maturity record validates against the maturity-assessment schema
- [ ] Requirement IDs resolve to ESAF-1100 controls or documented engagement
      requirements
- [ ] Procedure references identify the ESAF-1100 assessment procedures used
- [ ] Limitations remain present and accurate
- [ ] No certification or compliance claim appears in operator narrative

## Nonclaims

This Draft starter does not approve certification, compliance, equivalence,
endorsement, assurance, or production readiness. Completing worksheets does
not advance Draft controls, architectures, mappings, or profiles to an
approved lifecycle state.
