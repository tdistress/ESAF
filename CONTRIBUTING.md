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

## Contribution licensing

Unless the contributor and the ESAF Project Maintainers agree otherwise in writing, each contribution is submitted under the license applicable to the target path in [LICENSE_SCOPE.md](LICENSE_SCOPE.md). A contribution to an Apache-licensed path is submitted under Apache 2.0. A contribution to a CC BY 4.0 path is submitted under CC BY 4.0.

By submitting a contribution, the contributor confirms that they have authority to submit the contribution under the applicable license. This submission does not transfer copyright ownership.

Material conspicuously marked `Not a Contribution` is excluded from submission under these terms. Contributors shall identify third-party material and shall not submit it unless its terms permit inclusion and the project accepts it through the applicable rights-review process.

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
