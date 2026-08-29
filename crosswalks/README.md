# ESAF-1600 Standards Crosswalk

Crosswalks provide traceability between ESAF controls and external requirements. A mapping does not establish certification, compliance, equivalence, or legal sufficiency.

Priority mappings include NIST AI RMF, ISO/IEC 42001, PCI DSS, HITRUST CSF, UK Cyber Essentials, NIST CSF, ISO/IEC 27001, CIS Controls, OWASP guidance, and MITRE ATLAS.

Current readiness packages:

- [NIST AI RMF](nist-ai-rmf.md) — readiness `HOLD` (mapper/reviewer naming)
- [PCI DSS](pci-dss.md) — readiness `HOLD` (protected source and rights)

The [ESAF-1600 standard](ESAF-1600.md) defines the authoritative method. Each mapping shall identify the exact external source version, rationale, relationship, direction, coverage, confidence, mapper, independent reviewer, and review date. These dimensions remain separate and do not assert outcome sufficiency.

## Authoring resources

- [Mapping-set template](MAPPING_SET_TEMPLATE.md)
- [Provision-inventory template](PROVISION_INVENTORY_TEMPLATE.md)
- [Provision mapping template](CROSSWALK_TEMPLATE.md)
- [Lifecycle-record template](LIFECYCLE_RECORD_TEMPLATE.md)

## Generated catalogs and validation

The [human-readable catalog](CATALOG.md) and [machine-readable catalog](catalog.json) are deterministic generated views; authoritative Markdown records shall be edited instead.

Validate authoritative records and rewrite generated catalogs after an intentional source change:

```shell
python tools/validate_crosswalks.py --write
```

Check records and generated-catalog currency without rewriting files:

```shell
python tools/validate_crosswalks.py --check
```

See the [tooling guide](../tools/README.md) for trusted-baseline validation and full-history requirements.
