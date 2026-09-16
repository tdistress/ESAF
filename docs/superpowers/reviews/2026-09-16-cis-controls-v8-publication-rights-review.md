# CIS Controls Version 8 publication-rights review

**Reviewer:** ESAF Publication Rights Reviewer (automated readiness package)

**Review date:** 2026-09-16

**Reviewer independence:** The reviewer shall not serve as a mapper, mapping
reconciler, or substantive mapping reviewer in any future CIS Controls mapping
work under this readiness package.

**Authorized public-rights-source access:** Attested. The reviewer accessed the
official CIS Controls Version 8 landing page, the free registration download
page, the public CIS Controls Navigator for v8, CIS public license clarification
pages, and the Creative Commons BY-NC-ND 4.0 legal code. The reviewer did not
complete the download registration form, did not retrieve CIS Controls PDF or
Excel package bytes, and did not obtain case-specific written CIS commercial-use
approval for ESAF.

**Publication basis reviewed:** Attested. The reviewer reviewed the CIS Controls
Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
(CC BY-NC-ND 4.0) statement and CIS clarification that commercial use of the CIS
Controls requires prior CIS approval, before making this decision.

**Disposition:** `HOLD`

This is a fail-closed publication-control decision. CC BY-NC-ND 4.0 and the CIS
commercial-use clarification do not affirmatively authorize ESAF to publish
derivative mapping analysis or distributed paraphrases under ESAF's open
repository and downstream redistribution model without prior CIS approval.

## Reviewed public rights sources

- CIS Controls Version 8 landing:
  <https://www.cisecurity.org/controls/v8>
- CIS Controls Version 8 free download (registration form):
  <https://learn.cisecurity.org/cis-controls-download-v8>
- CIS Controls Navigator (v8):
  <https://www.cisecurity.org/controls/cis-controls-navigator/v8>
- CIS Controls public list / overview:
  <https://www.cisecurity.org/controls/cis-controls-list>
- CIS Assessment Specification terms-of-use license clarification:
  <https://cas.docs.cisecurity.org/en/latest/source/terms-of-use/>
- Creative Commons BY-NC-ND 4.0 legal code:
  <https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode>
- Adjacent discovery (not the pinned edition): CIS Controls Version 8.1 landing
  <https://www.cisecurity.org/controls/v8-1> (iterative update to v8; out of
  scope for this pinned readiness package)

## Official-source evidence

CIS Critical Security Controls Version 8 (CIS Controls v8) is published by the
Center for Internet Security, Inc. (CIS). Official CIS materials state that the
work is licensed under CC BY-NC-ND 4.0. CIS further clarifies that users may
copy and redistribute the content as a framework for non-commercial purposes
with appropriate credit to CIS and a link to the license, and that if users
remix, transform, or build upon the CIS Controls they may not distribute the
modified materials. Commercial use of the CIS Controls is subject to prior CIS
approval.

The normative PDF/Excel package is obtainable without payment after a marketing
registration form on the official learn.cisecurity.org download page. That
registration gate is not a PCI-style materials-license interstitial and is not
treated as a commercial paywall. This review nevertheless did not retrieve or
retain CIS PDF/Excel package bytes.

No case-specific written CIS commercial-use approval covering ESAF's repository,
website, generated publications, project license, and downstream redistribution
model is evidenced. Absence of affirmative permission for distributed derivative
mapping analysis is treated as a publication HOLD for the field classes below.

## ESAF-1600 mapping field-class partition

This table is an exhaustive, disjoint partition of the six ESAF-1600 mapping
field classes. A value belongs to exactly one row.

| Mapping field class | Disposition | Boundary |
|---|---|---|
| `identifiers` | Permitted | CIS Controls Version 8 Control and Safeguard identifiers (for example `1.1`) may be published with CIS attribution and a CC BY-NC-ND 4.0 license link, under the non-commercial framework-redistribution clarification. |
| `titles` | Permitted | Official Control and Safeguard titles may be published with attribution and a license link under the same non-commercial framework-redistribution clarification. |
| `structural_inventory` | Permitted | A complete inventory of publishable Safeguard identifiers, counts, and digests may be published with attribution and a license link. CIS PDF/Excel package bytes shall not be committed. |
| `paraphrases` | Prohibited | Distributed summaries or paraphrases of CIS Controls Version 8 Safeguard text are treated as transformations that may not be distributed under CC BY-NC-ND without CIS approval. |
| `derivative_mapping_analysis` | Prohibited | ESAF-to-external relationship analysis builds upon the CIS Controls. Distributing such modified materials requires CIS commercial-use / derivative-distribution approval that is not evidenced. |
| `official_links` | Permitted | ESAF may link to official CIS Controls landing, download, Navigator, license, and related discovery URLs without copying linked package bytes. |

The permitted and prohibited sets are exhaustive over these six classes and do
not overlap:

- `permitted_mapping_field_classes`: `identifiers`, `titles`, `structural_inventory`, `official_links`
- `prohibited_mapping_field_classes`: `paraphrases`, `derivative_mapping_analysis`

## Separate bibliographic source-identity allowance

| Bibliographic metadata class | Disposition | Boundary |
|---|---|---|
| `publisher_name` | Permitted | Center for Internet Security, Inc. (CIS). |
| `publication_family_name` | Permitted | CIS Critical Security Controls (CIS Controls). |
| `document_reference` | Permitted | CIS Controls Version 8 / CIS Controls v8. |
| `version_label` | Permitted | Version 8 (v8). CIS also publishes Version 8.1 as an iterative update; this package pins v8. |
| `language` | Permitted | English. |
| `format` | Permitted | PDF and Excel package (download), plus public HTML Navigator inventory source. |
| `publication_dates` | Permitted | Public Version 8 release identity as stated on official CIS pages (day-precision PDF publication date not claimed without retrieved PDF metadata). |
| `retrieval_metadata` | Permitted | ESAF retrieval time for public discovery pages; inventory digest of Safeguard identifiers; PDF/Excel byte length and SHA-256 only when independently retrieved and not committed. |
| `official_urls` | Permitted | Official landing, download, Navigator, list, and license URLs. |

## Attribution and endorsement boundary

Any ESAF publication that redistributes permitted CIS Controls Version 8
framework identifiers, titles, or structural inventory shall attribute CIS,
identify CIS Controls Version 8, provide a link to CC BY-NC-ND 4.0, and shall
not imply CIS approval, endorsement, certification, or assessment of ESAF or of
any mapped organization.

## Reconsideration trigger

Revisit this HOLD when CIS grants case-specific written commercial-use and
derivative-distribution permission covering ESAF's exact artifact classes,
publication channels, project license, and downstream redistribution model, or
when CIS publishes a rights regime that affirmatively permits distributed
derivative mapping analysis under ESAF's model. A later rights PASS for
`derivative_mapping_analysis` is required before a readiness GO may authorize
Draft mapping publication.

## Decision boundaries

This review is not legal advice. It does not decide whether any statutory
exception is available. It records a fail-closed publication-control decision
for this repository.

The decision does not claim CIS approval, endorsement, equivalence, compliance,
certification, or assurance. It does not authorize substantive mapping records
while the readiness matrix remains `HOLD`. It does not close Issues #55 or #60.
It does not retarget this package to CIS Controls Version 8.1.

## Final decision

`HOLD`. Identifiers, titles, structural inventory, and official links may be
recorded for readiness under non-commercial framework redistribution with
attribution and a license link. Paraphrases and derivative mapping analysis
remain prohibited until the reconsideration trigger is satisfied and
independently reviewed.
