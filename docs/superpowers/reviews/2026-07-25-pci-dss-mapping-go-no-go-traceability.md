# PCI DSS mapping readiness HOLD traceability

**Issue:** [#58 Complete PCI DSS source readiness and mapping go/no-go](https://github.com/tdistress/ESAF/issues/58)

**Status:** `Readiness HOLD`

**Decision basis:** The deterministic readiness matrix derives `HOLD`. This
record traces the issue commitments to the exact repository evidence without
creating or implying a PCI DSS mapping.

## Evidence package

- [Public source-readiness oracle](../specs/2026-07-25-pci-dss-source-readiness-oracle.json)
- [Publication-rights review](2026-07-25-pci-dss-publication-rights-review.md)
- [Mechanical readiness matrix](../specs/2026-07-25-pci-dss-mapping-readiness-matrix.json)
- [Generated GO/HOLD review](2026-07-25-pci-dss-mapping-go-no-go-review.md)
- [ESAF qualified mapping review protocol](../../../crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md)
- [Implementation plan](../plans/2026-07-25-pci-dss-source-readiness.md)

## Issue 58 traceability

| Issue item | Type | Commitment | Evidence and disposition |
|---|---|---|---|
| `I58-D1A` | Deliverable | Pin the official version, URL, and publication date. | The [source-readiness oracle](../specs/2026-07-25-pci-dss-source-readiness-oracle.json) pins PCI DSS `v4.0.1`, the official discovery and protected access URLs, and artifact publication `2024-06` at month precision separately from the `2024-06-11` announcement. |
| `I58-D1B` | Deliverable | Pin the source checksum. | The oracle records that the protected source artifact SHA-256 is `null` and unavailable. Matrix blocker `PCI-READINESS-B001` owns authorized acquisition and independent checksum verification. The mutable discovery-catalog digest is explicitly not the standard digest. |
| `I58-D1C` | Deliverable | Pin the provision inventory. | The oracle records that provision count and inventory digest are `null` and that no inventory exists. Matrix blocker `PCI-READINESS-B003` requires an independently reconciled complete inventory before reconsideration. |
| `I58-D2` | Deliverable | Record publication-rights and public-content boundaries. | The [publication-rights review](2026-07-25-pci-dss-publication-rights-review.md) records the fail-closed field-class partition, permitted bibliographic metadata, reviewed sources, and case-specific written-permission trigger. |
| `I58-D3` | Deliverable | Identify mapper and qualified-review requirements. | The [mapping-readiness matrix](../specs/2026-07-25-pci-dss-mapping-readiness-matrix.json) defines the named mapper, independent PCI, ESAF, rights, and security reviewers, access attestations, exact-SHA evidence, findings disposition, redispatch, and approver contract. |
| `I58-D4` | Deliverable | Define the exact directional mapping question and overclaiming controls. | The [mapping-readiness matrix](../specs/2026-07-25-pci-dss-mapping-readiness-matrix.json) binds `esaf_to_external`, complete-publication scope, authorized publishable granularity, the exact question, excluded reverse direction, and nonclaims. |
| `I58-D5` | Deliverable | Record one GO or HOLD decision. | The deterministic renderer validates the matrix and publishes [the derived `HOLD` review](2026-07-25-pci-dss-mapping-go-no-go-review.md). |
| `I58-GO1` | GO outcome | Complete the approved Draft mapping scope under ESAF-1600. | A future readiness GO only authorizes a separate substantive mapping candidate. It does not close issue 58 until the approved Draft mapping scope is completed under ESAF-1600 with provision records, negative dispositions, lifecycle record, generated catalogs, exact-SHA reviews, and traceability. |
| `I58-HOLD1` | HOLD outcome | Record blockers, owners, triggers, and nonclaims without mapping records. | The matrix and generated review record five blockers, accountable owners, missing evidence, reconsideration triggers, and deterministic re-entry tests. This candidate has zero substantive PCI DSS mapping artifacts. |
| `I58-A1` | Acceptance | Independently verify every pinned source and inventory assertion. | The oracle pins independently retrieved public catalog bytes, length, time, and digest. Protected source checksum and provision inventory are unavailable and therefore are not asserted; `PCI-READINESS-B001` and `PCI-READINESS-B003` fail closed. |
| `I58-A2` | Acceptance | Apply the approved decision method with exact evidence traceability. | The closed matrix, source-oracle digest, rights-review ancestry, renderer validation, generated review, and this record form the exact evidence chain. |
| `I58-A3` | Acceptance | Resolve Critical and Important findings. | The matrix records zero open Critical findings and zero open Important findings. Final exact-SHA reviews remain mandatory publication gates and any candidate change requires redispatch. |
| `I58-A4` | Acceptance | Pass focused tests, full suite, crosswalk validation, link validation, and whole-branch diff checks. | Focused invariants are in `tests/test_pci_dss_source_readiness.py` and `tests/test_render_pci_dss_mapping_go_no_go.py`; the workflow runs the full suite, crosswalk and link validators, and renderer check. Whole-branch diff evidence is required by the implementation plan and final PR record. |
| `I58-B1` | Boundary | Do not assert PCI DSS compliance. | The matrix and generated review explicitly prohibit compliance claims. |
| `I58-B2` | Boundary | Do not assert assessor approval. | The [PCI DSS landing page](../../../crosswalks/pci-dss.md) and this record explicitly prohibit assessor approval claims; the matrix also prohibits PCI SSC approval claims. |
| `I58-B3` | Boundary | Do not assert certification. | The matrix and generated review explicitly prohibit certification claims. |
| `I58-B4` | Boundary | Do not assert equivalence. | The matrix and generated review explicitly prohibit equivalence claims. |
| `I58-B5` | Boundary | Do not assert endorsement. | The matrix and generated review explicitly prohibit endorsement claims. |
| `I58-B6` | Boundary | Do not assert legal sufficiency. | The rights review, matrix, and generated review explicitly prohibit legal-sufficiency claims and do not decide statutory exceptions. |

## Blocking evidence and re-entry

| Blocker | Gate | Accountable owner | Reconsideration trigger |
|---|---|---|---|
| `PCI-READINESS-B001` | Authorized source artifact | ESAF Project Maintainer and authorized PCI source custodian | Authorized acquisition and independent identification of the exact English source artifact, including byte length, SHA-256, metadata, page count, URL, filename, and acquisition time. |
| `PCI-READINESS-B002` | Publication rights | ESAF Project Maintainer and PCI SSC permissions contact | Case-specific written permission covers the exact field classes, repository, website, generated publications, project license, and downstream redistribution. |
| `PCI-READINESS-B003` | Provision inventory | ESAF Project Maintainer and independent inventory authors | Two authorized inventories reconcile to one complete population at the approved granularity, count, and canonical digest. |
| `PCI-READINESS-B004` | Semantic feasibility | ESAF Project Maintainer and qualified mapper | Authorized source, rights, and inventory evidence permit a positive probe of the exact directional question. |
| `PCI-READINESS-B005` | Mapper and reviewer readiness | ESAF Project Maintainer and review coordinator | Named qualified people accept the access, independence, exact-candidate, attestation, and findings-disposition contract. |

The exact missing evidence and deterministic re-entry test for every blocker are
authoritative in the readiness matrix and rendered review.

## Catalog invariance and artifact boundary

The readiness package is outside `crosswalks/mappings/` and
`crosswalks/registry/`. PCI DSS mapping artifacts: `0`.

| Generated catalog measure | Baseline | Current candidate |
|---|---:|---:|
| Mapping sets | 3 | 3 |
| Provisions | 404 | 404 |
| Relationships | 81 | 81 |
| Negative dispositions | 325 | 325 |

No PCI DSS provision record, relationship, negative disposition, snapshot,
lifecycle record, registry record, generated catalog entry, provision count,
inventory digest, or coverage statistic exists.

## Closure rule

The evidenced HOLD package may complete the issue 58 readiness decision because
it records the blocking conditions and fail-closed re-entry path without
publishing a mapping. If the matrix later derives GO, that readiness result does
not close issue 58 by itself. Closure on the GO path requires completion of the
approved Draft mapping scope under ESAF-1600 and all exact-SHA review,
traceability, validation, lifecycle, and generated-catalog evidence.

Neither the current HOLD nor a future GO asserts PCI DSS compliance, assessor
approval, certification, equivalence, endorsement, authorization, coverage, or
legal sufficiency.
