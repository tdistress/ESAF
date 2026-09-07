# ISO/IEC 42001:2023 mapping readiness decision

**Decision:** `HOLD`

**Review identifier:** `iso-iec--42001--2023--esaf-0.11-draft--mapping-readiness--0.1.0`

**Open findings:** Critical `0`; Important `0`

The decision is derived from the closed readiness matrix. It is not an authorization to create an ISO/IEC 42001 mapping.

## Exact directional question

> Does exact normative ESAF control requirement text directly support, partially support, or establish a prerequisite for the outcome required by one authorized, publishable ISO/IEC 42001:2023 clause or control outcome, with each relationship's conditions, expected evidence, and known gaps recorded independently, without implying ISO/IEC 42001 compliance, assessment, equivalence, certification, authorization, or endorsement?

Direction: `esaf_to_external`.

`external_to_esaf` is excluded and requires a separate approved design.

Scope: `complete_publication`.

Granularity: `finest_authorized_publishable_clause_or_control_outcome_identifier`.

## Source boundary

- Source-readiness oracle: `docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-oracle.json`
- Source-readiness oracle SHA-256: `cb172c36272560756c5328d00bc24d791b7a308222294b298c1bd8775f95175c`
- Publication-rights review: `docs/superpowers/reviews/2026-09-07-iso-iec-42001-publication-rights-review.md`
- Publication-rights review commit: `8245a0513979a8e4d4dc28a4f22daa028710bee1`
- Publication-rights review SHA-256: `17b02d0028e996abdc4fd7c3fbfbdfa2972068684ffce237ec42d94444d3df22`
- Positive feasibility probe available: `false`

The protected ISO/IEC 42001:2023 source artifact, its digest, and its provision inventory remain unavailable. Public discovery metadata is not a substitute for source bytes.

## Gate results

| Gate | Status | Rationale | Evidence |
|---|---|---|---|
| `source_identity_and_drift` | `PASS` | Pinned public bibliographic identity identifies ISO/IEC 42001:2023 and records official discovery URLs without retaining protected source bytes. | docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-oracle.json#discovery; docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-oracle.json#publication |
| `authorized_source_artifact` | `BLOCKED` | The protected normative PDF bytes, source SHA-256, page count, and acquisition evidence are unavailable. | docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-oracle.json#access; docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-oracle.json#source_artifact |
| `publication_rights` | `BLOCKED` | The independent rights review records HOLD because no case-specific written permission covers ESAF publication and redistribution. | docs/superpowers/reviews/2026-09-07-iso-iec-42001-publication-rights-review.md#final-decision |
| `provision_inventory` | `BLOCKED` | No authorized exact source or independently reconciled complete provision population exists, and structural inventory remains prohibited. | docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-oracle.json#nonclaims; docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-design.md#source-readiness-oracle |
| `semantic_and_normative_feasibility` | `BLOCKED` | Exact ISO/IEC 42001:2023 outcomes cannot be compared with normative ESAF requirements without authorized source access and a complete approved inventory. | docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-design.md#exact-proposed-mapping-contract; docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-oracle.json#boundary |
| `esaf_1600_and_schema_fit` | `PASS` | Existing ESAF-1600 direction, relationship, negative-disposition, rights, evidence, and lifecycle controls can represent the proposed future mapping without a parallel schema. | docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-design.md#exact-proposed-mapping-contract; crosswalks/schema/mapping-set.schema.json; crosswalks/schema/mapping-record.schema.json |
| `mapper_and_reviewer_readiness` | `BLOCKED` | Named qualified people with authorized source access and the required independent exact-candidate review roles are not evidenced. | docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-design.md#mapper-and-qualified-review-contract |
| `overclaiming_controls` | `PASS` | The HOLD boundary, explicit nonclaims, exact directional question, and future independent security review requirements can be enforced mechanically. | docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-design.md#hold-boundary-and-reconsideration; docs/superpowers/reviews/2026-09-07-iso-iec-42001-publication-rights-review.md#decision-boundaries |

## Blockers

| Blocker | Gate | Owner | Missing evidence | Reconsideration trigger | Re-entry test |
|---|---|---|---|---|---|
| `ISO-IEC-42001-READINESS-B001` | `authorized_source_artifact` | ESAF Project Maintainer and authorized ISO/IEC 42001 source custodian | Authorized acquisition evidence for the exact English ISO/IEC 42001:2023 PDF, including final URL, filename, byte length, SHA-256, PDF metadata, page count, and acquisition time. | An authorized person acquires the exact artifact through the intended ISO/IEC commercial flow without placing protected bytes in the repository. | The source oracle records the authorized artifact as available and every required identity, byte, digest, metadata, page-count, and acquisition field is non-null and independently verified. |
| `ISO-IEC-42001-READINESS-B002` | `publication_rights` | ESAF Project Maintainer and ISO/IEC permissions contact | Case-specific written ISO/IEC permission, or equivalent licensing, for the exact ESAF field classes, repository, website, generated publications, project license, and downstream redistribution model. | ISO/IEC grants written permission covering the complete proposed publication use. | An independent rights reviewer verifies the executed permission against every proposed field class and publication channel and records an attributable PASS disposition. |
| `ISO-IEC-42001-READINESS-B003` | `provision_inventory` | ESAF Project Maintainer and independent inventory authors | An independently reconciled complete inventory of the authorized publishable ISO/IEC 42001:2023 clauses or control outcomes, with count and digest. | Authorized source access and publication permission allow two independent inventories at the approved granularity. | Independent inventories reconcile to one complete population, and tests reproduce the exact provision count and canonical inventory digest. |
| `ISO-IEC-42001-READINESS-B004` | `semantic_and_normative_feasibility` | ESAF Project Maintainer and qualified mapper | A positive feasibility probe for the exact directional question using authorized ISO/IEC 42001:2023 outcomes and exact normative ESAF requirements. | The authorized source artifact, publication rights, and complete reconciled provision inventory are available. | A qualified mapper and independent reviewers record at least one evidence-backed positive probe for the exact question while preserving all ESAF-1600 negative and overclaiming rules. |
| `ISO-IEC-42001-READINESS-B005` | `mapper_and_reviewer_readiness` | ESAF Project Maintainer and review coordinator | Named qualified people with authorized source access for the mapper, ISO/IEC 42001 subject-matter, ESAF specification and mapping, publication-rights, security and overclaiming, and owner-authorized approval roles. | Qualified named people accept the closed role, independence, access-attestation, exact-candidate, and findings-disposition contract. | The readiness evidence names every required person, verifies qualifications and independence, and proves attributable exact-SHA inventory/specification and security/overclaiming reviews with no open Critical or Important findings. |

## Future mapper and reviewer requirements

A future GO requires a named mapper with authorized source access and experience in ISO/IEC 42001:2023 and ESAF-1600. The mapper may not review their own work.

| Role | Independence | Qualification | Authorized source access |
|---|---|---|---|
| `iso_iec_42001_subject_matter` | Independent from mapper | owner-approved ISO/IEC 42001:2023 subject-matter reviewer | Required |
| `esaf_specification_and_mapping` | Independent from mapper | independent ESAF specification and mapping reviewer | Required |
| `publication_rights` | Independent from mapper | independent publication-rights reviewer | Required |
| `security_and_overclaiming` | Independent from mapper | independent security and overclaiming reviewer | Required |

Each review record requires: `identity`, `role`, `qualification_or_relevant_experience`, `authorized_source_access_attestation`, `attributable_attestation`, `review_date`, `exact_candidate_sha`, `artifact_digests`, `findings`, `findings_disposition`.

The inventory/specification and security/overclaiming reviews shall be separate reviews of the same exact candidate SHA and artifact digests. Any candidate change requires redispatch of both reviews.

Approver: An approver authorized by the ESAF project owner.

## Reconsideration sequence

1. Obtain case-specific written ISO/IEC permission, or equivalent licensing, for the exact publication and redistribution model.
2. Have an authorized person acquire and independently identify the exact English ISO/IEC 42001:2023 source artifact.
3. Create and reconcile a complete provision inventory at the authorized publishable granularity.
4. Name the qualified mapper, independent reviewers, review coordinator, and owner-authorized approver with required access attestations.
5. Refresh source identity and drift evidence, run the exact feasibility probe, and derive GO only if every gate passes with no blockers or open Critical or Important findings.

## Nonclaims

- No protected ISO/IEC 42001:2023 source bytes were downloaded, accepted, or committed by this workstream.
- No ISO/IEC 42001:2023 clause or control identifier, title, source text, close paraphrase, or structural inventory is published.
- No ISO/IEC 42001:2023 provision inventory, provision count, or inventory digest exists.
- No ISO/IEC 42001 mapping relationship, negative disposition, snapshot, lifecycle record, registry record, or generated catalog entry exists.
- No ISO or IEC authorization, validation, approval, endorsement, or certification is claimed.
- No ISO/IEC 42001 assessment, compliance, equivalence, coverage, or legal sufficiency is claimed.
- No coverage statistic or percentage is calculated.
- No decision is made for the excluded external_to_esaf direction.

## Final decision

`HOLD`. The blocked gates and their complete blocker records control re-entry. No mapping artifact may be created while this decision remains HOLD.
