# CIS Controls Version 8 mapping readiness decision

**Decision:** `HOLD`

**Review identifier:** `cis-controls--v8--esaf-0.17-draft--mapping-readiness--0.1.0`

**Open findings:** Critical `0`; Important `0`

The decision is derived from the closed readiness matrix. It is not an authorization to create a CIS Controls mapping.

## Exact directional question

> Does exact normative ESAF control requirement text directly support, partially support, or establish a prerequisite for the outcome required by one authorized, publishable CIS Controls Version 8 Safeguard identifier, with each relationship's conditions, expected evidence, and known gaps recorded independently, without implying CIS Controls compliance, assessment, equivalence, certification, authorization, or endorsement?

Direction: `esaf_to_external`.

`external_to_esaf` is excluded and requires a separate approved design.

Scope: `complete_publication`.

Granularity: `cis_controls_v8_safeguard_identifier`.

## Source boundary

- Source-readiness oracle: `docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-oracle.json`
- Source-readiness oracle SHA-256: `82769dc7bf4b39cfe95f6ebeb8023dc70e64246b7f6b2ecc5ae61f934cd79cc1`
- Publication-rights review: `docs/superpowers/reviews/2026-09-16-cis-controls-v8-publication-rights-review.md`
- Publication-rights review commit: `84da951cc171fdc0940648b857ccbb54edd7759c`
- Publication-rights review SHA-256: `0e3aa4a8eaf69b675721a0bc070aff63309fa5eb22c0c6ad2b737786eb4f8e2f`
- Positive feasibility probe available: `true`

The official public CIS Controls Version 8 Safeguard inventory digest and 153-identifier inventory are recorded in the source oracle. CIS Controls PDF and Excel package bytes are not committed to the repository.

## Gate results

| Gate | Status | Rationale | Evidence |
|---|---|---|---|
| `source_identity_and_drift` | `PASS` | Pinned CIS Controls Version 8 (v8) publisher, title, landing URL, free registration download URL, and public Navigator inventory source; Version 8.1 recorded as adjacent unpinned iterative update. | docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-oracle.json#publication; docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-oracle.json#discovery; docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-design.md#edition-pin |
| `authorized_source_artifact` | `PASS` | Official public Navigator lists Safeguard identifiers without a paywall; the PDF/Excel package is freely obtainable after registration. Package bytes and PDF digests were not retrieved or committed; inventory digests are recorded from the public Navigator. | docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-oracle.json#access; docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-oracle.json#source_artifact |
| `publication_rights` | `BLOCKED` | Independent rights review records HOLD under CC BY-NC-ND 4.0: identifiers, titles, structural inventory, and official links are permitted with attribution; paraphrases and derivative mapping analysis are prohibited without CIS commercial-use approval. | docs/superpowers/reviews/2026-09-16-cis-controls-v8-publication-rights-review.md#final-decision; docs/superpowers/reviews/2026-09-16-cis-controls-v8-publication-rights-review.md#esaf-1600-mapping-field-class-partition |
| `provision_inventory` | `PASS` | A complete 153-identifier CIS Controls Version 8 Safeguard inventory is published with a canonical digest derived from the official public CIS Controls Navigator v8. | docs/superpowers/specs/2026-09-16-cis-controls-v8-safeguard-inventory.json; docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-oracle.json#source_artifact |
| `semantic_and_normative_feasibility` | `PASS` | Public CIS Controls Version 8 Safeguard outcomes can be compared with exact ESAF normative text; a positive directional feasibility probe is recorded in the design without creating mapping artifacts. Publication of analysis remains rights-blocked. | docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-design.md#positive-feasibility-probe; docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-design.md#exact-proposed-mapping-contract |
| `esaf_1600_and_schema_fit` | `PASS` | Existing ESAF-1600 direction, relationship, negative-disposition, rights, evidence, and lifecycle controls can represent a future CIS Controls mapping without a parallel schema. | docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-design.md#exact-proposed-mapping-contract; crosswalks/schema/mapping-set.schema.json; crosswalks/schema/mapping-record.schema.json |
| `mapper_and_reviewer_readiness` | `BLOCKED` | Named qualified mapper and independent exact-candidate reviewers are not evidenced. | docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-design.md#mapper-and-qualified-review-contract |
| `overclaiming_controls` | `PASS` | HOLD boundary, explicit nonclaims, exact directional question, rights prohibition on derivative analysis, and future independent security review requirements can be enforced mechanically. | docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-design.md#hold-boundary-and-reconsideration; docs/superpowers/reviews/2026-09-16-cis-controls-v8-publication-rights-review.md#decision-boundaries |

## Blockers

| Blocker | Gate | Owner | Missing evidence | Reconsideration trigger | Re-entry test |
|---|---|---|---|---|---|
| `CIS-CONTROLS-V8-READINESS-B001` | `publication_rights` | ESAF Project Maintainer and CIS permissions contact | Case-specific written CIS commercial-use and derivative-distribution permission, or an equivalent affirmative rights regime, covering ESAF paraphrases and derivative mapping analysis across the repository, website, generated publications, project license, and downstream redistribution model. | CIS grants written permission covering the complete proposed publication use, or publishes rights that affirmatively permit distributed derivative mapping analysis under ESAF's model. | An independent rights reviewer verifies the executed permission against every proposed field class and publication channel and records an attributable PASS disposition that includes derivative_mapping_analysis. |
| `CIS-CONTROLS-V8-READINESS-B002` | `mapper_and_reviewer_readiness` | ESAF Project Maintainer and review coordinator | Named qualified people for the mapper, CIS Controls Version 8 subject-matter, ESAF specification and mapping, publication-rights, security and overclaiming, and owner-authorized approval roles, with independence and attributable exact-SHA review evidence. | Qualified named people accept the closed role, independence, access-attestation, exact-candidate, and findings-disposition contract. | The readiness evidence names every required person, verifies qualifications and independence, and proves attributable exact-SHA inventory/specification and security/overclaiming reviews with no open Critical or Important findings. |

## Future mapper and reviewer requirements

A future GO requires a named mapper with authorized source access and experience in CIS Controls Version 8 and ESAF-1600. The mapper may not review their own work.

| Role | Independence | Qualification | Authorized source access |
|---|---|---|---|
| `cis_controls_subject_matter` | Independent from mapper | owner-approved CIS Controls Version 8 subject-matter reviewer | Required |
| `esaf_specification_and_mapping` | Independent from mapper | independent ESAF specification and mapping reviewer | Required |
| `publication_rights` | Independent from mapper | independent publication-rights reviewer | Required |
| `security_and_overclaiming` | Independent from mapper | independent security and overclaiming reviewer | Required |

Each review record requires: `identity`, `role`, `qualification_or_relevant_experience`, `authorized_source_access_attestation`, `attributable_attestation`, `review_date`, `exact_candidate_sha`, `artifact_digests`, `findings`, `findings_disposition`.

The inventory/specification and security/overclaiming reviews shall be separate reviews of the same exact candidate SHA and artifact digests. Any candidate change requires redispatch of both reviews.

Approver: An approver authorized by the ESAF project owner.

## Reconsideration sequence

1. Obtain CIS commercial-use and derivative-distribution permission covering ESAF paraphrases and mapping analysis, then refresh the publication-rights review to PASS for derivative_mapping_analysis.
2. Name the qualified mapper, independent reviewers, review coordinator, and owner-authorized approver with required access attestations.
3. Complete attributable exact-SHA inventory/specification and security/overclaiming reviews with no open Critical or Important findings.
4. Optionally retrieve official CIS Controls Version 8 PDF package digests without committing package bytes, refresh source identity if CIS revises the publication, and derive GO only if every gate passes with no blockers.

## Nonclaims

- No CIS Controls mapping relationship, negative disposition, snapshot, lifecycle record, registry record, or generated catalog entry exists.
- No CIS approval, endorsement, certification, assessment, equivalence, compliance, or assurance is claimed.
- No coverage statistic or percentage is calculated.
- No decision is made for the excluded external_to_esaf direction.
- This HOLD does not close Issues #55 or #60.
- CIS Controls PDF and Excel package bytes were not retrieved or committed to the repository.
- This package pins CIS Controls Version 8 (v8) and does not claim identity with CIS Controls Version 8.1.

## Final decision

`HOLD`. The blocked gates and their complete blocker records control re-entry. No mapping artifact may be created while this decision remains HOLD.
