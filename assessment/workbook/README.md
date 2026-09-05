# ESAF-1500 Assessment Workbook (Draft starter)

**Status:** Draft starter  
**Issue:** [#115](https://github.com/tdistress/ESAF/issues/115)

This directory is a non-normative operator workbook for recording assessments
against existing ESAF-1500 contracts and ESAF-1100 control assessment
procedures. It does not replace [ESAF-1500](../ESAF-1500.md).

## Contents

| Path | Role |
|---|---|
| [ESAF-1500-workbook.md](ESAF-1500-workbook.md) | Draft operator guide |
| [worksheets/evidence-record.worksheet.json](worksheets/evidence-record.worksheet.json) | Blank evidence-record worksheet |
| [worksheets/assessment-result.worksheet.json](worksheets/assessment-result.worksheet.json) | Blank assessment-result worksheet |
| [worksheets/maturity-assessment.worksheet.json](worksheets/maturity-assessment.worksheet.json) | Blank maturity-assessment worksheet |

## How to use

1. Copy the worksheet JSON files into your working engagement folder.
2. Replace every `WORKSHEET` placeholder value before treating a record as
   final.
3. Keep field names and enumerations aligned to the schemas under
   [`../schema/evidence-record.schema.json`](../schema/evidence-record.schema.json),
   [`../schema/assessment-result.schema.json`](../schema/assessment-result.schema.json),
   and
   [`../schema/maturity-assessment.schema.json`](../schema/maturity-assessment.schema.json).
4. Validate filled records with `python tools/validate_assessment.py --check`
   after placing finalized examples under `assessment/examples/` or by running
   the workbook worksheet tests.

## Nonclaims

This workbook is Draft starter material only. Completing worksheets does not
establish certification, compliance, equivalence, endorsement, assurance,
production readiness, or lifecycle approval for any Draft ESAF artifact.
