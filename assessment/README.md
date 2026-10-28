# ESAF-1500 Assessment Guide

This directory contains the normative assessment guide (Working Draft `0.1.1`),
its machine-readable contracts, fictional examples, and Draft operator toolkit
starters.

- [ESAF-1500](ESAF-1500.md) Working Draft `0.1.1` defines shared assessment
  methodology, evidence expectations, assessment results, and maturity
  semantics.
- [Evidence-record schema](schema/evidence-record.schema.json),
  [assessment-result schema](schema/assessment-result.schema.json), and
  [maturity-assessment schema](schema/maturity-assessment.schema.json) define
  the supported JSON contracts.
- [Fictional evidence-record example](examples/evidence-record.example.json),
  [fictional assessment-result example](examples/assessment-result.example.json),
  and [fictional maturity-assessment example](examples/maturity-assessment.example.json)
  demonstrate the contracts without assessing an organization or control.
- [Integrated Summit Analytics assessment](integrated-assessment.example.md) is
  the shared fictional CAP-140 case connecting the workbook, audit checklist,
  evidence catalog, and governance thread. Its API-100 result is workbook-owned;
  its MOD-100 result is audit-owned.
- [API-100 remediation follow-up](follow-up/api100-remediation.example.md)
  adds one fictional owner action and one bounded API-100-A3 staging exercise.
  Its separate Draft result links to the original open finding without
  changing the historical assessment result.
- [API-100 inconclusive follow-up](follow-up/api100-inconclusive-follow-up.example.md)
  shows one attempted staging exercise whose incomplete event trail supports
  no control determination. Its distinct Draft result remains `not_assessed`
  with an open finding, and a separate governance risk review records the next
  evidence-capture action without accepting the risk or closing the finding.
- [Draft assessment workbook](workbook/README.md) provides operator guidance,
  schema-conforming worksheet stubs, and fictional worked engagement vignettes
  with filled worksheet trios bound to ESAF-1500 and ESAF-1100 assessment
  procedures. Completing worksheets does not establish certification,
  compliance, equivalence, endorsement, or assurance.
- [Draft evidence catalog deepen](evidence-catalog/README.md) indexes ESAF-1500
  evidence types, shared contract fields, quality attributes, per-type
  good-enough versus common-failure notes, and a growing set of fictional
  filled evidence examples for reuse by operators, profiles, and crosswalks.
- [Draft audit checklist deepen](audit-checklist/README.md) supports control or
  capability sampling against the shared ESAF-1500 assessment-result contract,
  including fictional two-control sampling vignettes with Draft filled
  assessment-result examples.

Validate the guide, schemas, examples, references, final states, maturity
prerequisites, component roll-ups, and non-claim boundaries with:

```shell
python tools/validate_assessment.py --check
```
