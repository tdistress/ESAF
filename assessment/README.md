# ESAF-1500 Assessment Guide

This directory contains the normative assessment guide, its machine-readable
contracts, and fictional examples.

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

Validate the guide, schemas, examples, references, final states, maturity
prerequisites, component roll-ups, and non-claim boundaries with:

```shell
python tools/validate_assessment.py --check
```
