# ESAF-0002 Governance and Publication Guide

**Document ID:** ESAF-0002  
**Status:** Working Draft  
**Version:** 0.1-alpha

## 1. Purpose

This document defines how ESAF is governed, reviewed, versioned, maintained, and published. ESAF is maintained as a living standards project.

## 2. Governance bodies

### 2.1 Steering Committee

Sets strategic direction, approves scope and major releases, and resolves material governance matters.

### 2.2 Editorial Board

Maintains terminology, normative language, numbering, structure, references, and publication consistency.

### 2.3 Technical Review Board

Reviews architecture, security, engineering, control design, implementation feasibility, and technical accuracy.

### 2.4 Compliance Review Board

Reviews mappings to external standards, including NIST, ISO, PCI DSS, HITRUST, UK Cyber Essentials, SOC 2, HIPAA, GDPR, OWASP, MITRE, and CIS Controls.

Initially, one maintainer may perform more than one role. Conflicts of interest and dissenting technical views shall be recorded in the decision log.

## 3. Publication lifecycle

```text
Proposed -> Draft -> Technical Review -> Editorial Review
         -> Approved -> Published -> Revised -> Deprecated -> Retired
```

## 4. Decision process

Changes enter through an issue or pull request. Normative changes require technical and editorial review. Major structural changes require Steering Committee approval. Decisions that affect scope, taxonomy, numbering, or compatibility shall be recorded in [`project/DECISION_LOG.md`](project/DECISION_LOG.md).

## 5. Versioning

ESAF uses semantic versioning:

| Version type | Meaning |
|---|---|
| Major | Breaking structural or normative changes |
| Minor | New controls, guidance, mappings, architectures, or profiles |
| Patch | Editorial corrections, clarifications, and errata |

## 6. Release stages

| Stage | Description |
|---|---|
| 0.1-alpha | Foundation draft |
| 0.5-beta | Integrated review draft |
| 0.9-rc | Release candidate |
| 1.0 | First stable release |

## 7. Exceptions

Exceptions to ESAF requirements shall document the requirement or control ID, business justification, risk assessment, compensating controls, approval authority, expiration date, and review schedule.

## 8. Intellectual property and conduct

Contributions are made under the repository license and contribution terms. Participants shall follow the [Code of Conduct](CODE_OF_CONDUCT.md).

