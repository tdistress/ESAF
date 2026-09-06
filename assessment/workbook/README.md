# ESAF-1500 Assessment Workbook (Draft)

**Status:** Draft deepen  
**Issues:** [#115](https://github.com/tdistress/ESAF/issues/115) starter;
[#124](https://github.com/tdistress/ESAF/issues/124) deepen

This directory is a non-normative operator workbook for recording assessments
against existing ESAF-1500 contracts and ESAF-1100 control assessment
procedures. It does not replace [ESAF-1500](../ESAF-1500.md).

## Contents

| Path | Role |
|---|---|
| [ESAF-1500-workbook.md](ESAF-1500-workbook.md) | Draft operator guide |
| [engagement-vignette.example.md](engagement-vignette.example.md) | Fictional worked engagement narrative |
| [worksheets/evidence-record.worksheet.json](worksheets/evidence-record.worksheet.json) | Blank evidence-record worksheet |
| [worksheets/assessment-result.worksheet.json](worksheets/assessment-result.worksheet.json) | Blank assessment-result worksheet |
| [worksheets/maturity-assessment.worksheet.json](worksheets/maturity-assessment.worksheet.json) | Blank maturity-assessment worksheet |
| [examples/engagement-evidence-record.example.json](examples/engagement-evidence-record.example.json) | Filled fictional evidence record |
| [examples/engagement-assessment-result.example.json](examples/engagement-assessment-result.example.json) | Filled fictional draft assessment result |
| [examples/engagement-maturity-assessment.example.json](examples/engagement-maturity-assessment.example.json) | Filled fictional draft maturity assessment |

## How to use

1. Copy the worksheet JSON files into your working engagement folder.
2. Replace every `WORKSHEET` placeholder value before treating a record as
   final.
3. Keep field names and enumerations aligned to the schemas under
   [`../schema/evidence-record.schema.json`](../schema/evidence-record.schema.json),
   [`../schema/assessment-result.schema.json`](../schema/assessment-result.schema.json),
   and
   [`../schema/maturity-assessment.schema.json`](../schema/maturity-assessment.schema.json).
4. Validate blank worksheets and filled engagement examples with the workbook
   unit tests, or validate finalized tracked examples under
   `assessment/examples/` with `python tools/validate_assessment.py --check`.

## Worked example

See [engagement-vignette.example.md](engagement-vignette.example.md) for one
fictional GOV-100 walkthrough with a filled worksheet trio under
[`examples/`](examples/). Blank stubs under [`worksheets/`](worksheets/) remain
the reusable starting point.

## Nonclaims

This workbook is Draft material only. Completing worksheets does not establish
certification, compliance, equivalence, endorsement, assurance, production
readiness, or lifecycle approval for any Draft ESAF artifact.
