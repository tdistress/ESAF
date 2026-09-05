# ESAF-1500 Assessment Guide

This directory contains the normative assessment guide, its machine-readable
contracts, fictional examples, and Draft operator toolkit starters.

- [ESAF-1500](ESAF-1500.md) defines shared assessment methodology, evidence
  expectations, assessment results, and maturity semantics.
- [Evidence-record schema](schema/evidence-record.schema.json),
  [assessment-result schema](schema/assessment-result.schema.json), and
  [maturity-assessment schema](schema/maturity-assessment.schema.json) define
  the supported JSON contracts.
- [Fictional evidence-record example](examples/evidence-record.example.json),
  [fictional assessment-result example](examples/assessment-result.example.json),
  and [fictional maturity-assessment example](examples/maturity-assessment.example.json)
  demonstrate the contracts without assessing an organization or control.
- [Draft assessment workbook starter](workbook/README.md) provides operator
  guidance and schema-conforming worksheet stubs bound to ESAF-1500 and
  ESAF-1100 assessment procedures. Completing worksheets does not establish
  certification, compliance, equivalence, endorsement, or assurance.
- [Draft evidence catalog starter](evidence-catalog/README.md) indexes ESAF-1500
  evidence types, shared contract fields, and quality attributes for reuse by
  operators, profiles, and crosswalks.
- [Draft audit checklist starter](audit-checklist/README.md) supports control or
  capability sampling against the shared ESAF-1500 assessment-result contract.

Validate the guide, schemas, examples, references, final states, maturity
prerequisites, component roll-ups, and non-claim boundaries with:

```shell
python tools/validate_assessment.py --check
```
