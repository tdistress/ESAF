# Contributing to ESAF

Thank you for your interest in contributing to the Enterprise Secure AI Framework.

ESAF is intended to evolve as a collaborative, vendor-neutral standards initiative.

---

## Contribution Areas

Contributions may include:

- Framework language
- Control statements
- Reference architectures
- Governance processes
- Assessment procedures
- Standards mappings
- Industry profiles
- Templates
- Diagrams
- Glossary terms

---

## Contribution Principles

Contributions should be:

- Vendor-neutral
- Technology-agnostic
- Risk-based
- Auditable
- Implementable
- Traceable to recognized standards where practical

---

## External Mapping Contributions

An external mapping contribution shall follow [ESAF-1600](crosswalks/ESAF-1600.md) and record:

- the official source URL and exact source identity and version;
- the approved publication-rights basis, access class, licensing note, and rights-review date;
- the permitted and prohibited elements, including any restrictions on titles, identifiers, paraphrases, or derivative analysis;
- explicit `reviewer_authorized_source_access: true` and `publication_basis_reviewed: true` attestations, in addition to attestations that the mapper and technical reviewer had authorized source access;
- mapper and reviewer qualifications, dates, and findings dispositions; and
- an intellectual-property attestation confirming that no restricted or licensed external requirement text is included and that contributed summaries and analysis are original and within the recorded rights.

The mapper and reviewer shall be different people. The rights reviewer shall also be different from the mapper. Restricted or licensed requirement text shall not be committed; use identifier-only records with a rights-based omission rationale when a summary is not permitted.

---

## Assessment Contributions

Assessment-guide, schema, or example changes shall include:

```shell
python tools/validate_assessment.py --check
```

---

## Profile Contributions

Profile contract changes shall follow [ESAF-1800](profiles/ESAF-1800.md).
Create or edit a versioned package only under
`profiles/<profile-domain>/<version>/`, where the profile domain identifies
the jurisdiction, industry, sector, or risk context. Preserve the required
package components and keep profile-specific requirements separate from the
meanings of core ESAF controls and ESAF-1500 assessment semantics. Manifest
component values are package-relative component paths; component `$schema`
values are document-relative schema locators.

`proposed` remains a valid earlier lifecycle state. A profile shall not advance
beyond Draft until the applicable technical, editorial, scope, and
overclaiming reviews and publication gates are complete. Profiles shall not
claim compliance, certification, equivalence, endorsement, legal sufficiency,
external approval, or production readiness.

Profile contract, schema, package, index, or validator changes shall include:

```shell
python -m unittest tests.test_profile_foundation tests.test_validate_profiles -v
python tools/validate_profiles.py --check
```

---

## Review Process

Proposed changes should move through:

```text
Draft
    ↓
Technical Review
    ↓
Editorial Review
    ↓
Approval
    ↓
Publication
```

---

## Normative Language

Use:

- **Shall** for mandatory requirements
- **Should** for strong recommendations
- **May** for optional capabilities
