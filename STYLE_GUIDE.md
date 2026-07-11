# ESAF-0001 Editorial and Style Guide

**Document ID:** ESAF-0001  
**Status:** Working Draft  
**Version:** 0.1-alpha  

---

## 1. Purpose

This guide defines editorial, numbering, formatting, and terminology conventions for ESAF publications.

---

## 2. Normative Language

| Term | Meaning |
|------|---------|
| Shall | Mandatory requirement |
| Should | Strong recommendation |
| May | Optional capability |

---

## 3. Document Numbering

| Document | Purpose |
|----------|---------|
| ESAF-0000 | Project Charter |
| ESAF-0001 | Editorial and Style Guide |
| ESAF-0002 | Governance and Publication Guide |
| ESAF-1000 | Enterprise Standard |
| ESAF-1100 | Control Catalog |
| ESAF-1200 | Reference Architecture |
| ESAF-1300 | Governance Manual |
| ESAF-1400 | Implementation Guide |
| ESAF-1500 | Assessment Guide |
| ESAF-1600 | Standards Crosswalk |
| ESAF-1700 | Enterprise AI Data Model |
| ESAF-1800 | Industry Profiles |

---

## 4. Control Numbering

Control objectives shall use a family prefix and two-digit number. Base controls shall use a family prefix and three-digit number allocated in increments of ten.

Example:

```text
IAM-01 Identity Governance
IAM-100 Enterprise Authentication
IAM-110 Machine Identity
IAM-120 Privileged Access
```

Control enhancements shall use parenthetical numbering.

```text
IAM-100(1) Federated Authentication
IAM-100(2) Adaptive Authentication
```

---

## 5. Control Template

Each control shall include schema-valid YAML metadata and the following content:

- Control ID
- Title
- Family
- Objective
- Status and version
- Requirement
- Intent
- Applicability
- Implementation Guidance
- Organization-defined parameters, when used
- Evidence
- Assessment Procedures
- Metrics
- Lifecycle stages and pillars
- Control Owner
- Baseline selections
- Related controls
- Framework Crosswalk
- Change history

The authoritative authoring template is `controls/CONTROL_TEMPLATE.md`. The metadata schema is `controls/schema/control.schema.json`.

---

## 6. Figure and Table Numbering

Figures shall be numbered by section.

Example:

```text
Figure 4-1. Enterprise AI Lifecycle
```

Tables shall be numbered by section.

Example:

```text
Table 5-2. Control Families
```
