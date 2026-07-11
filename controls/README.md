# ESAF-1100 Control Catalog

This directory contains the control architecture and, after approval, individual control records.

- [`ESAF-1100.md`](ESAF-1100.md) defines the normative control architecture.
- [`OBJECTIVES.md`](OBJECTIVES.md) defines family-level control objectives.
- [`CONTROL_TEMPLATE.md`](CONTROL_TEMPLATE.md) is the authoring template.
- [`schema/control.schema.json`](schema/control.schema.json) validates machine-readable control metadata.
- Family directories contain approved controls for that family.

No example or template is an approved control. Approved controls will be identified by catalog status and release version.

## Current control tranches

| Tranche | Families | Base controls | Status |
|---|---|---:|---|
| Foundational governance and risk | [GOV](GOV/README.md), [STR](STR/README.md), [RSK](RSK/README.md) | 14 | Draft |
| Identity and data protection | [IAM](IAM/README.md), [DAT](DAT/README.md) | 13 | Draft |
| Model, application, and integration security | [MOD](MOD/README.md), [APP](APP/README.md), [API](API/README.md) | 18 | Draft |
