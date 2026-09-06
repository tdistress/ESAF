# Assessment Workbook Draft Starter Design

**Status:** Approved for implementation (#115)

**Date:** 2026-09-05

## Purpose

Provide a Draft ESAF-1500 operator workbook under `assessment/workbook/` with
Markdown guidance and schema-conforming JSON worksheet stubs. Operators copy
and fill worksheets without inventing parallel evidence, result, or maturity
semantics.

## Shape

```text
assessment/workbook/
  README.md
  ESAF-1500-workbook.md
  worksheets/
    evidence-record.worksheet.json
    assessment-result.worksheet.json
    maturity-assessment.worksheet.json
```

Engagement metadata (purpose, boundary, period, assessor independence) lives in
the Markdown guide as fill-in sections, not a separate non-schema JSON file.

## Constraints

- Status remains **Draft**; no certification or assurance claims.
- Field names and enumerations bind only to ESAF-1500 schemas and ESAF-1100
  assessment methods/procedures.
- Worksheets shall validate against existing schemas with `status: draft` where
  applicable and explicit placeholder identifiers.
- Link from `assessment/README.md` (and root publication table only if already
  listing companion assessment material).

## Validation

Add focused tests that every `*.worksheet.json` under
`assessment/workbook/worksheets/` validates against its ESAF-1500 schema and
that the workbook Markdown carries Draft and nonclaim language.
