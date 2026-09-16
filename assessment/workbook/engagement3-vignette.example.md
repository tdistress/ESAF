# Workbook engagement vignette 3 (informative)

**Status:** Draft deepen example
**Issue:** [#207](https://github.com/tdistress/ESAF/issues/207)
**Subject control:** `API-100` Enterprise AI Gateway

This fictional third walkthrough shows how an assessor can use the ESAF-1500
workbook pack for a gateway-control engagement. It is informative only. It
does not assess a real organization and does not establish certification,
compliance, equivalence, endorsement, assurance, or production readiness.

## Engagement snapshot

| Field | Fictional entry |
|---|---|
| Engagement ID | `ENG-SA-2026-09-API100` |
| Purpose | Examine whether fictional CAP-140 production traffic routes through an approved AI gateway with required policy-enforcement capabilities |
| Subject | Fictional Summit Analytics workforce-research assistant (`CAP-140`) |
| In-scope control | `API-100` |
| Explicit exclusions | Emergency restriction Test depth (`API-100-A3`) and external-provider contract depth (`API-140`) |
| Assessment period | 2026-09-01 to 2026-09-15 |
| Population / sample | Complete examination of the fictional gateway configuration package for `CAP-140` |
| Assessor | Morgan Ellis, Independent assessor, Fictional Contour Assurance LLP |
| Independence | Illustrative only; not a real independence attestation |
| Kickoff limitation | Configuration export alone cannot prove runtime enforcement without corroborating Test evidence |

## Narrative

1. **Scope the engagement.** The assessor records the API-100 gateway
   examination in the workbook scope table and keeps emergency-restriction and
   vendor-contract exclusions visible.
2. **Collect evidence.** The assessor obtains the fictional effective gateway
   routing and allowlist package, recording it as
   [`examples/engagement3-evidence-record.example.json`](examples/engagement3-evidence-record.example.json)
   (`EVD-ENG3-API100-GATEWAY`).
3. **Execute API-100-A1 (Examine).** The assessor checks that fictional CAP-140
   traffic routes through approved control points with identity, authorization,
   model routing, logging, and limits, capturing method detail in the draft
   result.
4. **Record determination and finding.** Required routing capabilities are
   present, but the fictional emergency model-restriction switch lacks an
   executable Test harness in this sample. The draft result
   [`examples/engagement3-assessment-result.example.json`](examples/engagement3-assessment-result.example.json)
   (`ASR-ENG3-API100`) stays `draft` with one open minor finding.
5. **Optional maturity axis.** The assessor records a draft maturity view in
   [`examples/engagement3-maturity-assessment.example.json`](examples/engagement3-maturity-assessment.example.json)
   (`MAT-ENG3-API100`) at `M1`, citing the same evidence and result IDs.
   Control determination and maturity remain independent.

## Filled worksheet trio

| Record | ID | Status | Path |
|---|---|---|---|
| Evidence | `EVD-ENG3-API100-GATEWAY` | n/a | [engagement3-evidence-record.example.json](examples/engagement3-evidence-record.example.json) |
| Assessment result | `ASR-ENG3-API100` | `draft` | [engagement3-assessment-result.example.json](examples/engagement3-assessment-result.example.json) |
| Maturity assessment | `MAT-ENG3-API100` | `draft` | [engagement3-maturity-assessment.example.json](examples/engagement3-maturity-assessment.example.json) |

Earlier workbook vignettes remain at
[engagement-vignette.example.md](engagement-vignette.example.md) (`GOV-100`)
and [engagement2-vignette.example.md](engagement2-vignette.example.md)
(`RSK-110`). Blank reusable stubs remain under
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
