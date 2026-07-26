# PCI DSS publication-rights review

**Reviewer:** Codex PCI DSS Publication Rights Reviewer R1

**Review date:** 2026-07-25

**Reviewer independence:** The reviewer shall not serve as a mapper, mapping reconciler, or substantive mapping reviewer in any future PCI DSS mapping work.

**Authorized public-rights-source access:** Attested. The reviewer was authorized to access the public rights sources listed below. The reviewer did not accept the protected-document agreement or retrieve protected source bytes.

**Publication basis reviewed:** Attested. The reviewer reviewed the public terms, intellectual-property policy and standards license, protected access boundary, and case-specific materials-license request path before making this decision.

**Disposition:** `HOLD`

This is a fail-closed decision. The reviewed sources do not provide affirmative permission for ESAF to publish PCI DSS provision content, a provision inventory, paraphrases, or mapping analysis.

## Reviewed public rights sources

- PCI SSC Terms and Conditions: <https://www.pcisecuritystandards.org/terms_and_conditions/>
- PCI SSC Intellectual Property Rights Policy and Standards License Agreement: <https://www.pcisecuritystandards.org/about_us/policies/>
- Official protected-document access path and license interstitial: <https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf>
- PCI SSC Materials License Agreement Request: <https://programs.pcissc.org/mla_registration.aspx>

## Official-source evidence

The PCI SSC Terms and Conditions limit access, downloading, and printing of Council content to personal, non-commercial review, study, and informational purposes. Unless law requires otherwise or PCI SSC grants rights in a separate written agreement, the terms prohibit publication, distribution, copying, licensing, sublicensing, transfer, sale, preparation of derivative works, and non-personal use.

The PCI SSC Intellectual Property Rights Policy states that PCI SSC owns the copyright in its standards and other work product. Exhibit A grants an internal read-and-copy license for study and a separate implementation license for compliant products. It does not grant a general publication license. The same exhibit prohibits modification and states that it conveys no right to create a derivative work of a standard or any portion of one.

The official protected-document access path presents a license agreement before access to the document. This review did not accept that agreement and did not obtain the protected document. The existence of an access route does not establish a right to republish or derive an ESAF mapping from the protected material.

The PCI SSC Materials License Agreement Request applies when a proposed use falls outside the Standards License Agreement. It states that PCI SSC materials may not be copied or otherwise used without separate permission in each instance and that PCI SSC may grant or refuse a request at its discretion. This is the identified route for seeking permission for a public ESAF artifact.

## ESAF-1600 mapping field-class partition

This table is an exhaustive, disjoint partition of the six ESAF-1600 mapping field classes. A value belongs to exactly one row. Only `official_links` is permitted under the current evidence.

| Mapping field class | Disposition | Boundary |
|---|---|---|
| `identifiers` | Prohibited | PCI DSS provision identifiers are not approved for publication. This class does not include the separate document-level bibliographic metadata listed below. |
| `titles` | Prohibited | PCI DSS provision titles are not approved for publication. This class does not include the publication-family name used as document-level bibliographic metadata. |
| `structural_inventory` | Prohibited | No hierarchy, numbered-requirement population, occurrence ledger, provision count, or comparable source-derived structure may be created or published. |
| `paraphrases` | Prohibited | No summary, close paraphrase, or independently written paraphrase of PCI DSS provision content may be created or published. |
| `derivative_mapping_analysis` | Prohibited | No relationship assessment, mapping rationale, disposition, coverage claim, or other analysis derived from PCI DSS provision content may be created or published. |
| `official_links` | Permitted | ESAF may link to the official public rights, discovery, announcement, and protected access pages without copying the linked content. |

The permitted and prohibited sets are exhaustive over these six classes and do not overlap:

- `permitted_mapping_field_classes`: `official_links`
- `prohibited_mapping_field_classes`: `identifiers`, `titles`, `structural_inventory`, `paraphrases`, `derivative_mapping_analysis`

## Separate bibliographic source-identity allowance

Minimal public bibliographic and source-identity metadata is permitted only to identify the publication and record public discovery state. This allowance is separate from the six ESAF-1600 mapping field classes. It does not permit PCI DSS provision identifiers, provision titles, structural inventory, paraphrases, or derivative mapping analysis.

| Bibliographic metadata class | Disposition | Boundary |
|---|---|---|
| `publisher_name` | Permitted | The publisher's public name. |
| `publication_family_name` | Permitted | The document family name, not a provision title. |
| `document_reference` | Permitted | The public discovery-catalog reference for the document, not a provision identifier. |
| `version_label` | Permitted | The public version label. |
| `language` | Permitted | The public language value. |
| `format` | Permitted | The public media or file-format value. |
| `public_catalog_dates` | Permitted | Dates and timestamps published as discovery metadata. |
| `public_catalog_status_flags` | Permitted | Public archive, protection, and comparable discovery-status values. |
| `announcement_retirement_effective_dates` | Permitted | Public announcement, retirement, and effective dates, kept distinct and labeled with their stated precision. |
| `retrieval_metadata` | Permitted | ESAF's retrieval time plus byte length and digest of public discovery metadata, never of the protected standard. |
| `official_urls` | Permitted | Official source, discovery, announcement, rights, and access URLs. |

This closed allowance does not authorize additional source-derived metadata. Any expansion requires a new publication-rights review supported by affirmative written permission.

## Reconsideration trigger

ESAF may reconsider the prohibited field classes only after PCI SSC grants a case-specific written Materials License Agreement that covers the exact proposed artifact, field classes, publication channels, and redistribution terms. The permission must also identify any required attribution, notices, version limits, and restrictions. Until then, the disposition remains `HOLD`.

## Decision boundaries

This review is not legal advice. It does not decide whether any statutory exception is available, and it does not conclude that statutory exceptions are unavailable. It records a fail-closed absence-of-permission publication-control decision for this repository.

The decision does not claim PCI SSC approval, authorization, validation, endorsement, equivalence, or compliance. It does not assess any PCI DSS provision and does not create a mapping, inventory, registry record, or generated catalog entry.

## Final decision

`HOLD`. Official links and the separately listed minimal bibliographic source-identity metadata may be recorded for readiness. The other five ESAF-1600 mapping field classes remain prohibited until the reconsideration trigger is satisfied and independently reviewed.
