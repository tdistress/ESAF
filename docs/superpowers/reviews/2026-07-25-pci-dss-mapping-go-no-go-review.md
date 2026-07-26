# PCI DSS mapping readiness decision

**Decision:** `HOLD`

**Review identifier:** `pci-ssc--pci-dss--4.0.1--esaf-0.4-alpha--mapping-readiness--0.1.0`

**Open findings:** Critical `0`; Important `0`

The decision is derived from the closed readiness matrix. It is not an authorization to create a PCI DSS mapping.

## Exact directional question

> Does exact normative ESAF control requirement text directly support, partially support, or establish a prerequisite for the outcome required by one authorized, publishable PCI DSS v4.0.1 numbered requirement or sub-requirement, with each relationship's conditions, expected evidence, and known gaps recorded independently, without implying PCI DSS compliance, assessment, equivalence, certification, authorization, or endorsement?

Direction: `esaf_to_external`.

`external_to_esaf` is excluded and requires a separate approved design.

Scope: `complete_publication`.

Granularity: `finest_authorized_publishable_numbered_requirement_or_sub_requirement_identifier`.

## Source boundary

- Source-readiness oracle: `docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json`
- Source-readiness oracle SHA-256: `fc513985138689085a9ceb8794edc12313a0a5a1f7e47c936d988bbeac294904`
- Publication-rights review: `docs/superpowers/reviews/2026-07-25-pci-dss-publication-rights-review.md`
- Publication-rights review commit: `5bc0d8235a49b3a08bffb14c1fc500c547199e81`
- Positive feasibility probe available: `false`

The protected PCI DSS source artifact, its digest, and its provision inventory remain unavailable. Public discovery metadata is not a substitute for source bytes.

## Gate results

| Gate | Status | Rationale | Evidence |
|---|---|---|---|
| `source_identity_and_drift` | `PASS` | Pinned public PCI SSC discovery metadata identifies the active PCI DSS v4.0.1 publication and records a reproducible retrieval digest for mutable discovery metadata. | docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json#discovery; docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json#publication |
| `authorized_source_artifact` | `BLOCKED` | The protected normative PDF bytes, source SHA-256, page count, and acquisition evidence are unavailable. | docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json#access; docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json#source_artifact |
| `publication_rights` | `BLOCKED` | The independent rights review records HOLD because no case-specific written permission covers ESAF publication and redistribution. | docs/superpowers/reviews/2026-07-25-pci-dss-publication-rights-review.md#final-decision |
| `provision_inventory` | `BLOCKED` | No authorized exact source or independently reconciled complete provision population exists. | docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json#nonclaims; docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-design.md#source-readiness-oracle |
| `semantic_and_normative_feasibility` | `BLOCKED` | Exact PCI DSS outcomes cannot be compared with normative ESAF requirements without authorized source access and a complete approved inventory. | docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-design.md#exact-proposed-mapping-contract; docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json#boundary |
| `esaf_1600_and_schema_fit` | `PASS` | Existing ESAF-1600 direction, relationship, negative-disposition, rights, evidence, and lifecycle controls can represent the proposed future mapping without a parallel schema. | docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-design.md#exact-proposed-mapping-contract; schemas/crosswalk-mapping-set.schema.json; schemas/crosswalk-mapping.schema.json |
| `mapper_and_reviewer_readiness` | `BLOCKED` | Named qualified people with authorized source access and the required independent exact-candidate review roles are not evidenced. | docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-design.md#mapper-and-qualified-review-contract |
| `overclaiming_controls` | `PASS` | The HOLD boundary, explicit nonclaims, exact directional question, and future independent security review requirements can be enforced mechanically. | docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-design.md#hold-boundary-and-reconsideration; docs/superpowers/reviews/2026-07-25-pci-dss-publication-rights-review.md#decision-boundaries |

## Blockers

| Blocker | Gate | Owner | Missing evidence | Reconsideration trigger | Re-entry test |
|---|---|---|---|---|---|
| `PCI-READINESS-B001` | `authorized_source_artifact` | ESAF Project Maintainer and authorized PCI source custodian | Authorized acquisition evidence for the exact English PCI DSS v4.0.1 PDF, including final URL, filename, byte length, SHA-256, PDF metadata, page count, and acquisition time. | An authorized person acquires the exact artifact through the intended PCI SSC flow without placing protected bytes in the repository. | The source oracle records the authorized artifact as available and every required identity, byte, digest, metadata, page-count, and acquisition field is non-null and independently verified. |
| `PCI-READINESS-B002` | `publication_rights` | ESAF Project Maintainer and PCI SSC permissions contact | Case-specific written PCI SSC permission for the exact ESAF field classes, repository, website, generated publications, project license, and downstream redistribution model. | PCI SSC grants a written Materials License Agreement covering the complete proposed publication use. | An independent rights reviewer verifies the executed permission against every proposed field class and publication channel and records an attributable PASS disposition. |
| `PCI-READINESS-B003` | `provision_inventory` | ESAF Project Maintainer and independent inventory authors | An independently reconciled complete inventory of the authorized publishable numbered PCI DSS v4.0.1 requirements or sub-requirements, with count and digest. | Authorized source access and publication permission allow two independent inventories at the approved granularity. | Independent inventories reconcile to one complete population, and tests reproduce the exact provision count and canonical inventory digest. |
| `PCI-READINESS-B004` | `semantic_and_normative_feasibility` | ESAF Project Maintainer and qualified mapper | A positive feasibility probe for the exact directional question using authorized PCI DSS outcomes and exact normative ESAF requirements. | The authorized source artifact, publication rights, and complete reconciled provision inventory are available. | A qualified mapper and independent reviewers record at least one evidence-backed positive probe for the exact question while preserving all ESAF-1600 negative and overclaiming rules. |
| `PCI-READINESS-B005` | `mapper_and_reviewer_readiness` | ESAF Project Maintainer and review coordinator | Named qualified people with authorized source access for the mapper, PCI subject-matter, ESAF specification and mapping, publication-rights, security and overclaiming, and owner-authorized approval roles. | Qualified named people accept the closed role, independence, access-attestation, exact-candidate, and findings-disposition contract. | The readiness evidence names every required person, verifies qualifications and independence, and proves attributable exact-SHA inventory/specification and security/overclaiming reviews with no open Critical or Important findings. |

## Future mapper and reviewer requirements

A future GO requires a named mapper with authorized source access and experience in PCI DSS v4.0.1 and ESAF-1600. The mapper may not review their own work.

| Role | Independence | Qualification | Authorized source access |
|---|---|---|---|
| `pci_subject_matter` | Independent from mapper | current QSA or owner-approved equivalent PCI reviewer | Required |
| `esaf_specification_and_mapping` | Independent from mapper | independent ESAF specification and mapping reviewer | Required |
| `publication_rights` | Independent from mapper | independent publication-rights reviewer | Required |
| `security_and_overclaiming` | Independent from mapper | independent security and overclaiming reviewer | Required |

Each review record requires: `identity`, `role`, `qualification_or_relevant_experience`, `authorized_source_access_attestation`, `attributable_attestation`, `review_date`, `exact_candidate_sha`, `artifact_digests`, `findings`, `findings_disposition`.

The inventory/specification and security/overclaiming reviews shall be separate reviews of the same exact candidate SHA and artifact digests. Any candidate change requires redispatch of both reviews.

Approver: An approver authorized by the ESAF project owner.

## Reconsideration sequence

1. Obtain case-specific written PCI SSC permission for the exact publication and redistribution model.
2. Have an authorized person acquire and independently identify the exact English PCI DSS v4.0.1 source artifact.
3. Create and reconcile a complete provision inventory at the authorized publishable granularity.
4. Name the qualified mapper, independent reviewers, review coordinator, and owner-authorized approver with required access attestations.
5. Refresh source identity and drift evidence, run the exact feasibility probe, and derive GO only if every gate passes with no blockers or open Critical or Important findings.

## Nonclaims

- No protected PCI DSS source bytes were downloaded, accepted, or committed by this workstream.
- No PCI DSS provision identifier, provision title, source text, close paraphrase, or structural inventory is published.
- No PCI DSS provision inventory, provision count, or inventory digest exists.
- No PCI DSS mapping relationship, negative disposition, snapshot, lifecycle record, registry record, or generated catalog entry exists.
- No PCI SSC authorization, validation, approval, endorsement, or certification is claimed.
- No PCI DSS assessment, compliance, equivalence, coverage, or legal sufficiency is claimed.
- No coverage statistic or percentage is calculated.
- No decision is made for the excluded external_to_esaf direction.

## Final decision

`HOLD`. The blocked gates and their complete blocker records control re-entry. No mapping artifact may be created while this decision remains HOLD.
