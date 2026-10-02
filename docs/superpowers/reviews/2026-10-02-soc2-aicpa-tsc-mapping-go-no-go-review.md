# SOC 2 AICPA TSC mapping readiness decision

**Decision:** `HOLD`

**Review identifier:** `aicpa--2017-trust-services-criteria--revised-pof-2022--esaf-0.17-draft--mapping-readiness--0.1.0`

The decision is mechanically derived from the closed readiness matrix.

## Directional question

> Does exact normative ESAF control requirement text directly support, partially support, or establish a prerequisite for the outcome required by one authorized, publishable AICPA Trust Services Criteria outcome, with each relationship's conditions, expected evidence, and known gaps recorded independently, without implying AICPA approval, SOC 2 compliance, assessment, equivalence, certification, authorization, or endorsement?

## Gate results

| Gate | Status | Rationale | Evidence |
|---|---|---|---|
| `source_identity_and_drift` | `PASS` | The official AICPA resource page identifies the candidate 2017 Trust Services Criteria with revised 2022 Points of Focus and gives a resource-page date. Currentness is explicitly not asserted; drift must be rechecked before any later mapping candidate. | docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-oracle.json#publication; docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-oracle.json#access |
| `authorized_source_artifact` | `BLOCKED` | The official download is account-gated. The exact PDF bytes and document-specific copyright notice have not been retrieved or inspected. | docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-oracle.json#access; docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-oracle.json#source_artifact |
| `publication_rights` | `BLOCKED` | No document-specific license or written AICPA permission for public ESAF source-derived analysis is evidenced. The site terms do not establish the exact rights attached to the separately downloadable criteria. | docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md#evidence-boundary; docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md#reconsideration-trigger |
| `provision_inventory` | `BLOCKED` | No authorized source artifact or permission boundary supports a complete public criterion-identifier inventory; no source-derived inventory has been created. | docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-oracle.json#inventory; docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md#esaf-1600-mapping-field-class-partition |
| `semantic_and_normative_feasibility` | `BLOCKED` | A positive feasibility probe cannot be performed without authorized criteria outcomes and an approved publishable granularity. | docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-design.md#scope-and-source-identity; docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-oracle.json#boundary |
| `esaf_1600_and_schema_fit` | `PASS` | Existing ESAF-1600 direction, relationship, rights, evidence, and lifecycle contracts can represent a future crosswalk without a parallel schema, subject to a later approved mapping design. | docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-design.md#evidence-model-and-rights-boundary; crosswalks/schema/mapping-set.schema.json; crosswalks/schema/mapping-record.schema.json |
| `mapper_and_reviewer_readiness` | `BLOCKED` | No named qualified mapper, AICPA TSC subject-matter reviewer, independent specification reviewer, publication-rights reviewer, security and overclaiming reviewer, or owner-authorized approver is evidenced. | docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-design.md#mechanical-readiness-decision; docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md#decision-boundaries |
| `overclaiming_controls` | `PASS` | The readiness-only boundary, explicit nonclaims, excluded mapping direction, and prohibition on source-derived public artifacts while rights remain unresolved are recorded and testable. | docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-design.md#nonclaims-and-reconsideration; docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md#decision-boundaries |

## Blockers

| Blocker | Category | Gate | Owner | Missing evidence | Remediation | Trigger | Re-entry test |
|---|---|---|---|---|---|---|---|
| SOC2-TSC-READINESS-B001 | authorized_source | authorized_source_artifact | ESAF Project Maintainer and authorized AICPA source custodian | Authorized acquisition of the exact Trust Services Criteria PDF and inspection of its document-specific copyright notice or license, with verified file identity and digest. | reconsiderable | An authorized source custodian obtains the exact English source through the intended AICPA account flow and confirms the terms permit the proposed review. | The oracle records verified title, edition, access state, byte length, SHA-256, document-specific notice, and any source updates; an independent reviewer confirms the source identity. |
| SOC2-TSC-READINESS-B002 | publication_permission | publication_rights | ESAF Project Maintainer and AICPA permissions contact | An independent rights determination and any needed written AICPA permission covering the exact proposed field classes, repository, generated publications, and downstream redistribution model. | reconsiderable | Document-specific terms or written AICPA permission affirmatively address the proposed source-derived analysis and each publication channel. | An independent rights reviewer verifies the exact source notice or executed permission against every field class and channel and records an attributable PASS disposition. |
| SOC2-TSC-READINESS-B003 | provision_population | provision_inventory | ESAF Project Maintainer and independent inventory reviewers | A complete and independently reconciled inventory at an expressly authorized and publishable Trust Services Criteria identifier granularity. | reconsiderable | Authorized source access and publication rights allow the complete criteria population to be inventoried at a defined granularity. | Two independent inventories reconcile exactly and reproduce the approved population count and canonical inventory digest without copying unauthorized source expression. |
| SOC2-TSC-READINESS-B004 | semantic_feasibility | semantic_and_normative_feasibility | Named qualified mapper and independent specification reviewers | A positive feasibility probe using authorized Trust Services Criteria outcomes and exact normative ESAF control requirement text. | reconsiderable | Authorized source access, positive publication rights, and a reconciled publishable population permit a bounded probe. | A qualified mapper and independent reviewers record an attributable positive exact-SHA probe while applying the ESAF-1600 outcome, prerequisite, evidence, and nonclaim rules. |
| SOC2-TSC-READINESS-B005 | qualified_people | mapper_and_reviewer_readiness | ESAF Project Maintainer and review coordinator | Named qualified people for mapping, AICPA TSC subject matter, ESAF specification, publication rights, security and overclaiming, and owner-authorized approval, with independence and source-access attestations. | reconsiderable | Qualified named people accept their defined roles, independence requirements, access attestations, and exact-candidate review contract. | The evidence names and qualifies each person, documents independence and authorized access, and requires separate exact-SHA specification/inventory and security/overclaiming reviews with no open Critical or Important findings. |

## Reconsideration sequence

1. Have an authorized source custodian obtain the exact Trust Services Criteria PDF through the intended AICPA access flow and document the specific notice, version, and file digest without committing protected bytes.
2. Obtain an independent rights determination and written AICPA permission where needed for each proposed field class and publication channel, then refresh the rights review.
3. Define the expressly authorized publishable criterion granularity and create two independent inventories that reconcile to the same population and digest.
4. Name the qualified mapper, independent reviewers, review coordinator, and owner-authorized approver with required source-access attestations.
5. Run the positive feasibility probe and derive GO only if every gate passes, all blockers are cleared, and no Critical or Important findings remain.

## Nonclaims

- No criterion text, criterion identifier, criterion title, paraphrase, structural inventory, or source-derived mapping analysis is published.
- No SOC 2 mapping relationship, negative disposition, snapshot, lifecycle event, registry record, or generated catalog entry exists.
- No mapping artifact or inventory count is asserted.
- No AICPA approval, authorization, validation, endorsement, certification, SOC 2 compliance, equivalence, coverage, assurance, or legal sufficiency is claimed.
- The decision does not assess a SOC 2 report or substitute for a qualified CPA examination.

**Final decision:** `HOLD`
