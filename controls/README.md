# ESAF-1100 Control Catalog

This directory contains the Working Draft control architecture and individual
control records.

- [`ESAF-1100.md`](ESAF-1100.md) defines the normative control architecture,
  assessment methods, determination meanings, and design and operating
  effectiveness definitions.
- Parent standard: [`ESAF-1000`](../framework/ESAF-1000.md).
- Shared evidence-record, assessment-result, and maturity semantics:
  [`ESAF-1500`](../assessment/ESAF-1500.md).
- [`OBJECTIVES.md`](OBJECTIVES.md) defines family-level control objectives.
- [`CONTROL_TEMPLATE.md`](CONTROL_TEMPLATE.md) is the authoring template.
- [`schema/control.schema.json`](schema/control.schema.json) validates
  machine-readable control metadata.
- [`CATALOG.md`](CATALOG.md) is the generated human-readable catalog and
  coverage summary.
- [`catalog.json`](catalog.json) is the generated machine-readable catalog.
- Family directories contain approved controls for that family.
- Draft assessment toolkit indexes under
  [`assessment/`](../assessment/README.md) illustrate ESAF-1500 record shapes
  used with ESAF-1100 procedures.

No example or template is an approved control. Approved controls will be
identified by catalog status and release version. This Working Draft does not
approve baseline selections or establish certification, compliance,
equivalence, endorsement, or assurance.

## Current control tranches

| Tranche | Families | Base controls | Status |
|---|---|---:|---|
| Foundational governance and risk | [GOV](GOV/README.md), [STR](STR/README.md), [RSK](RSK/README.md) | 14 | Draft |
| Identity and data protection | [IAM](IAM/README.md), [DAT](DAT/README.md) | 13 | Draft |
| Model, application, and integration security | [MOD](MOD/README.md), [APP](APP/README.md), [API](API/README.md) | 18 | Draft |
| Infrastructure and agentic AI | [INF](INF/README.md), [AGT](AGT/README.md) | 13 | Draft |
| Operations and monitoring | [OPS](OPS/README.md), [MON](MON/README.md) | 12 | Draft |
| Compliance and assurance | [CMP](CMP/README.md), [AUD](AUD/README.md) | 10 | Draft |
| Workforce and architecture | [EDU](EDU/README.md), [ARC](ARC/README.md) | 11 | Draft |
