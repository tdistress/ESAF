# Integrated assessment example: Summit Analytics CAP-140

**Status:** Informative fictional Draft example  
**Engagement ID:** `ENG-SA-2026-09-API100`  
**Assessment period:** 2026-09-01 through 2026-09-18

This overview connects the existing Summit Analytics workbook, audit-sampling,
evidence, maturity, and governance examples into one bounded fictional case.
The sample covers `API-100` and `MOD-100` for one fictional workforce-research
assistant capability, `CAP-140`. The linked records remain Draft and do not
establish a real assessment, certification, compliance, equivalence,
endorsement, or assurance outcome.

## Engagement boundary

| Field | Fictional engagement entry |
|---|---|
| Purpose | Illustrate evidence capture, assessment recording, sampling limitations, separate maturity recording, and governance follow-up for one capability. |
| Organization and subject | Fictional Summit Analytics workforce-research assistant (`CAP-140`). |
| Assessment period | 2026-09-01 through 2026-09-18. |
| Selected controls | `API-100` Enterprise AI Gateway and `MOD-100` Model Registry. |
| Population | The fictional CAP-140 gateway and model-control set (`API-*` and `MOD-*` controls assigned to the capability), with the evidence population for each control described in its record. |
| Sample | Risk-based judgmental selection of two controls. API-100 includes the complete gateway configuration package and one staging bypass attempt. MOD-100 includes one model-registry alias. This is not a statistical sample. |
| Assessor independence | Morgan Ellis of fictional Contour Assurance LLP is presented as having no operational ownership of CAP-140. The statement is illustrative, not a real independence attestation. |
| Exclusions | API-100 emergency-restriction exercise depth (`API-100-A3`), production bypass testing, external-provider contract depth (`API-140`), model-validation depth (`MOD-120`), and model retirement (`MOD-150`). |
| Scope limitation | Two controls and one MOD-100 alias do not support a capability-wide, portfolio-wide, or enterprise-wide conclusion. |

## Artifact flow

1. **Capture evidence.** The canonical API-100 configuration evidence is
   [`EVD-ENG3-API100-GATEWAY`](workbook/examples/engagement3-evidence-record.example.json).
   The MOD-100 registry artifact is
   [`EVD-SAMP3-MOD100-REGISTRY`](workbook/examples/engagement3-mod100-evidence-record.example.json).
   Procedure-level Test and Interview work is described in the results; the
   staging Test has no separate evidence-record example.
2. **Record API-100 work once.** The workbook's
   [`ASR-ENG3-API100`](workbook/examples/engagement3-assessment-result.example.json)
   is the single canonical API-100 result, combining API-100-A1 examination
   with one API-100-A2 staging bypass Test. The audit checklist retains its
   selection and procedure notes and points to this same result and evidence.
3. **Record MOD-100 work.** The audit-owned
   [`ASR-SAMP3-MOD100`](audit-checklist/examples/sampling3-mod100-assessment-result.example.json)
   records MOD-100-A1 examination, MOD-100-A2 reconciliation of one deployed
   alias, and MOD-100-A3 owner interview. Its result is Draft and bounded to
   that one alias.
4. **Keep maturity separate.** The workbook's
   [`MAT-ENG3-API100`](workbook/examples/engagement3-maturity-assessment.example.json)
   is a separate Draft maturity view scoped to API-100 for CAP-140. It does not
   assess MOD-100 or roll up the capability.
5. **Connect governance follow-up.** The
   [governance thread](../templates/examples/governance-thread3.example.md)
   links the residual risk and sidecar retirement verification to the
   canonical API-100 evidence and result. Governance action does not change the
   result's Draft status or determination.

## Outcome and limitations

The API-100 result is `partially_satisfied` and remains Draft. The fictional
gateway routes through approved control points, and one staging bypass call
was blocked and logged. The minor emergency-restriction finding remains open;
no production bypass Test or emergency-restriction exercise is included.
Configuration and staging observations do not establish production operating
effectiveness.

The MOD-100 result records a `satisfied` determination for the sampled alias,
but remains Draft. Its single-alias reconciliation and owner interview do not
support generalization to other models or a broader capability conclusion.
Maturity is a separate API-100-only view and does not replace either control
determination.

All people, organizations, evidence, dates, judgments, decisions, and records
are fictional. The examples make no external-framework mapping, compliance,
certification, equivalence, endorsement, or assurance claim. Copying or
completing them does not advance any Draft artifact to an approved lifecycle
state.
