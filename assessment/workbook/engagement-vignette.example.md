# Workbook engagement vignette (informative)

**Status:** Draft deepen example
**Issue:** [#124](https://github.com/tdistress/ESAF/issues/124)
**Subject control:** `GOV-100` Enterprise AI Governance Authority

This fictional walkthrough shows how an assessor can use the ESAF-1500 workbook
pack for one small engagement. It is informative only. It does not assess a
real organization and does not establish certification, compliance,
equivalence, endorsement, assurance, or production readiness.

## Engagement snapshot

| Field | Fictional entry |
|---|---|
| Engagement ID | `ENG-NB-2026-08-GOV100` |
| Purpose | Examine whether a documented enterprise AI governance authority exists |
| Subject | Fictional Northbridge Enterprises AI governance authority |
| In-scope control | `GOV-100` |
| Explicit exclusions | Operating effectiveness of meeting cadence beyond the sample period |
| Assessment period | 2026-05-01 to 2026-07-31 |
| Population / sample | Complete examination of the fictional approved charter package |
| Assessor | Avery Chen, Independent assessor, Fictional Contour Assurance LLP |
| Independence | Illustrative only; not a real independence attestation |
| Kickoff limitation | Charter extract alone cannot prove meeting attendance or decision execution |

## Narrative

1. **Scope the engagement.** The assessor records the GOV-100 charter
   examination in the workbook scope table and keeps exclusions visible.
2. **Collect evidence.** The assessor obtains a read-only export of the
   fictional AI governance charter and records it as
   [`examples/engagement-evidence-record.example.json`](examples/engagement-evidence-record.example.json)
   (`EVD-ENG-GOV100-CHARTER`).
3. **Execute GOV-100-A1 (Examine).** The assessor checks accountability,
   membership, decision rights, escalation, and cadence language in the
   fictional charter and captures method detail in the draft result.
4. **Record determination and finding.** Authority and membership are present,
   but escalation triggers are underspecified. The draft result
   [`examples/engagement-assessment-result.example.json`](examples/engagement-assessment-result.example.json)
   (`ASR-ENG-GOV100`) stays `draft` with one open minor finding.
5. **Optional maturity axis.** The assessor records a draft maturity view in
   [`examples/engagement-maturity-assessment.example.json`](examples/engagement-maturity-assessment.example.json)
   (`MAT-ENG-GOV100`) at `M1`, citing the same evidence and result IDs. Control
   determination and maturity remain independent.

## Filled worksheet trio

| Record | ID | Status | Path |
|---|---|---|---|
| Evidence | `EVD-ENG-GOV100-CHARTER` | n/a | [engagement-evidence-record.example.json](examples/engagement-evidence-record.example.json) |
| Assessment result | `ASR-ENG-GOV100` | `draft` | [engagement-assessment-result.example.json](examples/engagement-assessment-result.example.json) |
| Maturity assessment | `MAT-ENG-GOV100` | `draft` | [engagement-maturity-assessment.example.json](examples/engagement-maturity-assessment.example.json) |

Blank reusable stubs remain under
[`worksheets/evidence-record.worksheet.json`](worksheets/evidence-record.worksheet.json)
and siblings.

## Reader checks

- [ ] Every filled JSON file validates against the matching ESAF-1500 schema
- [ ] Evidence, result, and maturity IDs cross-reference consistently
- [ ] Result and maturity remain `draft` while the finding is open
- [ ] No certification or compliance claim appears in the narrative

## Nonclaims

Names, dates, organizations, and decisions in this vignette are fictional.
Completing or copying these materials does not advance Draft ESAF artifacts to
an approved lifecycle state and does not replace ESAF-1500, ESAF-1100, or an
organization's approved records.
