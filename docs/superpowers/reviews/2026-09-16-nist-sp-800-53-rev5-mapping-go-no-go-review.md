# NIST SP 800-53 Rev. 5 mapping readiness decision

**Decision:** `HOLD`

**Review identifier:** `nist--sp-800-53--rev5--esaf-0.16-draft--mapping-readiness--0.1.0`

**Open findings:** Critical `0`; Important `0`

The decision is derived from the closed readiness matrix. It is not an authorization to create a NIST SP 800-53 mapping.

## Exact directional question

> Does exact normative ESAF control requirement text directly support, partially support, or establish a prerequisite for the outcome required by one authorized, publishable NIST SP 800-53 Revision 5 control or control-enhancement identifier, with each relationship's conditions, expected evidence, and known gaps recorded independently, without implying NIST SP 800-53 compliance, assessment, equivalence, certification, authorization, or endorsement?

Direction: `esaf_to_external`.

`external_to_esaf` is excluded and requires a separate approved design.

Scope: `complete_publication`.

Granularity: `nist_sp_800_53_rev5_control_or_enhancement_identifier`.

## Source boundary

- Source-readiness oracle: `docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-oracle.json`
- Source-readiness oracle SHA-256: `0b9f0f8fad53c28be8379c02a71441f62748bb291ef70d7086a4f6fe80faf495`
- Publication-rights review: `docs/superpowers/reviews/2026-09-16-nist-sp-800-53-publication-rights-review.md`
- Publication-rights review commit: `c25399222e8f9e5f3e84a48f0335cf5eb144b545`
- Publication-rights review SHA-256: `23f4eb393d0169105d19108ee2ed3575e6570def24d64db53168f420a565031f`
- Positive feasibility probe available: `true`

The official public NIST SP 800-53 Rev. 5 PDF digest, page count, and 1196-identifier control/enhancement inventory are recorded in the source oracle. PDF and OSCAL catalog bytes are not committed to the repository.

## Gate results

| Gate | Status | Rationale | Evidence |
|---|---|---|---|
| `source_identity_and_drift` | `PASS` | Pinned NIST.SP.800-53r5 / SP 800-53 Rev. 5 public PDF identity, DOI, landing URL, publication date, byte length, SHA-256, and page count, plus OSCAL catalog 5.2.0 inventory digest. | docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-oracle.json#publication; docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-oracle.json#discovery; docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-oracle.json#source_artifact |
| `authorized_source_artifact` | `PASS` | The official English SP 800-53 Rev. 5 PDF and public OSCAL catalog are available without a protected interstitial; digests and page count are recorded without committing PDF or OSCAL bytes. | docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-oracle.json#access; docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-oracle.json#source_artifact |
| `publication_rights` | `PASS` | Independent rights review records PASS for all six ESAF-1600 mapping field classes under U.S. government work and NIST technical-series practice. | docs/superpowers/reviews/2026-09-16-nist-sp-800-53-publication-rights-review.md#final-decision; docs/superpowers/reviews/2026-09-16-nist-sp-800-53-publication-rights-review.md#esaf-1600-mapping-field-class-partition |
| `provision_inventory` | `PASS` | A complete 1196-identifier control and enhancement inventory is published with a canonical digest derived from the official NIST OSCAL SP 800-53 Rev 5.2.0 catalog. | docs/superpowers/specs/2026-09-16-nist-sp-800-53-rev5-control-inventory.json; docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-oracle.json#source_artifact |
| `semantic_and_normative_feasibility` | `PASS` | Public control and enhancement outcomes can be compared with exact ESAF normative text; a positive directional feasibility probe is recorded in the design without creating mapping artifacts. | docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-design.md#positive-feasibility-probe; docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-design.md#exact-proposed-mapping-contract |
| `esaf_1600_and_schema_fit` | `PASS` | Existing ESAF-1600 direction, relationship, negative-disposition, rights, evidence, and lifecycle controls can represent a future NIST SP 800-53 mapping without a parallel schema. | docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-design.md#exact-proposed-mapping-contract; crosswalks/schema/mapping-set.schema.json; crosswalks/schema/mapping-record.schema.json |
| `mapper_and_reviewer_readiness` | `BLOCKED` | Named qualified mapper and independent exact-candidate reviewers are not evidenced. | docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-design.md#mapper-and-qualified-review-contract |
| `overclaiming_controls` | `PASS` | HOLD boundary, explicit nonclaims, exact directional question, and future independent security review requirements can be enforced mechanically. | docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-design.md#hold-boundary-and-reconsideration; docs/superpowers/reviews/2026-09-16-nist-sp-800-53-publication-rights-review.md#decision-boundaries |

## Blockers

| Blocker | Gate | Owner | Missing evidence | Reconsideration trigger | Re-entry test |
|---|---|---|---|---|---|
| `NIST-SP-800-53-READINESS-B001` | `mapper_and_reviewer_readiness` | ESAF Project Maintainer and review coordinator | Named qualified people for the mapper, NIST SP 800-53 subject-matter, ESAF specification and mapping, publication-rights, security and overclaiming, and owner-authorized approval roles, with independence and attributable exact-SHA review evidence. | Qualified named people accept the closed role, independence, access-attestation, exact-candidate, and findings-disposition contract. | The readiness evidence names every required person, verifies qualifications and independence, and proves attributable exact-SHA inventory/specification and security/overclaiming reviews with no open Critical or Important findings. |

## Future mapper and reviewer requirements

A future GO requires a named mapper with authorized source access and experience in NIST SP 800-53 Rev. 5 and ESAF-1600. The mapper may not review their own work.

| Role | Independence | Qualification | Authorized source access |
|---|---|---|---|
| `nist_sp_800_53_subject_matter` | Independent from mapper | owner-approved NIST SP 800-53 subject-matter reviewer | Required |
| `esaf_specification_and_mapping` | Independent from mapper | independent ESAF specification and mapping reviewer | Required |
| `publication_rights` | Independent from mapper | independent publication-rights reviewer | Required |
| `security_and_overclaiming` | Independent from mapper | independent security and overclaiming reviewer | Required |

Each review record requires: `identity`, `role`, `qualification_or_relevant_experience`, `authorized_source_access_attestation`, `attributable_attestation`, `review_date`, `exact_candidate_sha`, `artifact_digests`, `findings`, `findings_disposition`.

The inventory/specification and security/overclaiming reviews shall be separate reviews of the same exact candidate SHA and artifact digests. Any candidate change requires redispatch of both reviews.

Approver: An approver authorized by the ESAF project owner.

## Reconsideration sequence

1. Name the qualified mapper, independent reviewers, review coordinator, and owner-authorized approver with required access attestations.
2. Complete attributable exact-SHA inventory/specification and security/overclaiming reviews with no open Critical or Important findings.
3. Refresh source identity and rights evidence if NIST revises the publication, and derive GO only if every gate passes with no blockers.

## Nonclaims

- No NIST SP 800-53 mapping relationship, negative disposition, snapshot, lifecycle record, registry record, or generated catalog entry exists.
- No NIST approval, endorsement, certification, assessment, equivalence, compliance, or assurance is claimed.
- No coverage statistic or percentage is calculated.
- No decision is made for the excluded external_to_esaf direction.
- This HOLD does not close Issues #55 or #60.
- Official PDF and OSCAL catalog bytes were retrieved for digest verification and inventory derivation only and are not committed to the repository.

## Final decision

`HOLD`. The blocked gates and their complete blocker records control re-entry. No mapping artifact may be created while this decision remains HOLD.
