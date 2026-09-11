# Workbook engagement vignette 2 (informative)

**Status:** Draft deepen example
**Issue:** [#183](https://github.com/tdistress/ESAF/issues/183)
**Subject control:** `RSK-110` AI Capability Risk Classification

This fictional second walkthrough shows how an assessor can use the ESAF-1500
workbook pack for a non-GOV control engagement. It is informative only. It
does not assess a real organization and does not establish certification,
compliance, equivalence, endorsement, assurance, or production readiness.

## Engagement snapshot

| Field | Fictional entry |
|---|---|
| Engagement ID | `ENG-SA-2026-09-RSK110` |
| Purpose | Examine whether a fictional workforce-research assistant has a current, documented risk classification |
| Subject | Fictional Summit Analytics workforce-research assistant (`CAP-140`) |
| In-scope control | `RSK-110` |
| Explicit exclusions | Supplier-risk controls (`RSK-120`) and impact-assessment depth (`RSK-130`) |
| Assessment period | 2026-06-01 to 2026-08-31 |
| Population / sample | Complete examination of the fictional classification package for `CAP-140` |
| Assessor | Morgan Ellis, Independent assessor, Fictional Contour Assurance LLP |
| Independence | Illustrative only; not a real independence attestation |
| Kickoff limitation | Classification procedure alone cannot prove operating adherence without corroborating logs |

## Narrative

1. **Scope the engagement.** The assessor records the RSK-110 classification
   examination in the workbook scope table and keeps supplier-risk exclusions
   visible.
2. **Collect evidence.** The assessor obtains the fictional controlled
   classification procedure and the completed classification record, recording
   them as
   [`examples/engagement2-evidence-record.example.json`](examples/engagement2-evidence-record.example.json)
   (`EVD-ENG2-RSK110-CLASSIFY`).
3. **Execute RSK-110-A1 (Examine).** The assessor checks that the fictional
   classification addresses impact, likelihood, autonomy, data sensitivity,
   affected parties, and applicable obligations, capturing method detail in
   the draft result.
4. **Record determination and finding.** Required factors are documented, but
   the fictional reclassification trigger for new audiences is underspecified.
   The draft result
   [`examples/engagement2-assessment-result.example.json`](examples/engagement2-assessment-result.example.json)
   (`ASR-ENG2-RSK110`) stays `draft` with one open minor finding.
5. **Optional maturity axis.** The assessor records a draft maturity view in
   [`examples/engagement2-maturity-assessment.example.json`](examples/engagement2-maturity-assessment.example.json)
   (`MAT-ENG2-RSK110`) at `M1`, citing the same evidence and result IDs.
   Control determination and maturity remain independent.

## Filled worksheet trio

| Record | ID | Status | Path |
|---|---|---|---|
| Evidence | `EVD-ENG2-RSK110-CLASSIFY` | n/a | [engagement2-evidence-record.example.json](examples/engagement2-evidence-record.example.json) |
| Assessment result | `ASR-ENG2-RSK110` | `draft` | [engagement2-assessment-result.example.json](examples/engagement2-assessment-result.example.json) |
| Maturity assessment | `MAT-ENG2-RSK110` | `draft` | [engagement2-maturity-assessment.example.json](examples/engagement2-maturity-assessment.example.json) |

The first workbook vignette for `GOV-100` remains at
[engagement-vignette.example.md](engagement-vignette.example.md). Blank
reusable stubs remain under
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
