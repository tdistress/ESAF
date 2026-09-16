# NIST SP 800-53 Rev. 5 publication-rights review

**Reviewer:** ESAF Publication Rights Reviewer (automated readiness package)

**Review date:** 2026-09-16

**Reviewer independence:** The reviewer shall not serve as a mapper, mapping
reconciler, or substantive mapping reviewer in any future NIST SP 800-53
mapping work under this readiness package.

**Authorized public-rights-source access:** Attested. The reviewer accessed the
public NIST CSRC publication landing page, DOI record, freely downloadable PDF
identity metadata, and the public NIST OSCAL catalog distribution. Protected-
paywall acceptance was not required.

**Publication basis reviewed:** Attested. The reviewer reviewed U.S. government
work status under 17 U.S.C. § 105, NIST technical-series publication practice,
and the official SP 800-53 Rev. 5 public distribution URLs before making this
decision.

**Disposition:** `PASS`

This is an affirmative public-source publication-control decision for the field
classes listed below. It is not legal advice and does not waive attribution or
trademark constraints.

## Reviewed public rights sources

- NIST SP 800-53 Rev. 5 CSRC publication record (includes updates as of
  Dec. 10, 2020; planning note for Release 5.2.0):
  <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- DOI / NVLPubs identity: <https://doi.org/10.6028/NIST.SP.800-53r5>
- Official PDF:
  <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf>
- Official OSCAL catalog (identifier inventory source):
  <https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json>
- NIST disclaimer and copyright practice for technical series publications
  (U.S. government work; royalty-free use with attribution)

## Official-source evidence

NIST Special Publication 800-53 Revision 5, *Security and Privacy Controls for
Information Systems and Organizations* (NIST.SP.800-53r5; dated September 2020
with updates as of December 10, 2020, and subsequent public Release 5.2.0
control catalog updates) is a NIST Special Publication distributed as a freely
downloadable PDF. Works of the United States government are not subject to
domestic copyright under 17 U.S.C. § 105. NIST technical series practice grants
royalty-free worldwide permission to copy, distribute, and prepare derivative
works with appropriate attribution to NIST and without implying NIST endorsement
of a third-party product or mapping.

No PCI-style protected interstitial or materials-license agreement gates access
to the normative PDF or the public OSCAL catalog. ESAF may therefore publish
mapping field classes derived from the public SP 800-53 Rev. 5 text and
identifiers, subject to attribution and the nonclaim boundaries below.

## ESAF-1600 mapping field-class partition

This table is an exhaustive, disjoint partition of the six ESAF-1600 mapping
field classes. A value belongs to exactly one row.

| Mapping field class | Disposition | Boundary |
|---|---|---|
| `identifiers` | Permitted | SP 800-53 control and control-enhancement identifiers (for example `AC-2` and `AC-2(1)`) may be published with attribution. |
| `titles` | Permitted | Official control and enhancement titles may be published with attribution. |
| `structural_inventory` | Permitted | A complete inventory of publishable control and enhancement identifiers, counts, and digests may be published. |
| `paraphrases` | Permitted | Independent paraphrases and summaries of public SP 800-53 outcomes may be published with attribution and without NIST endorsement claims. |
| `derivative_mapping_analysis` | Permitted | ESAF-to-external relationship analysis may be published under ESAF-1600 once a readiness GO authorizes Draft mapping work. |
| `official_links` | Permitted | ESAF may link to official NIST landing, DOI, CSRC, PDF, and OSCAL URLs. |

The permitted set is exhaustive over these six classes:

- `permitted_mapping_field_classes`: `identifiers`, `titles`, `structural_inventory`, `paraphrases`, `derivative_mapping_analysis`, `official_links`
- `prohibited_mapping_field_classes`: _(none under this PASS disposition)_

## Separate bibliographic source-identity allowance

| Bibliographic metadata class | Disposition | Boundary |
|---|---|---|
| `publisher_name` | Permitted | National Institute of Standards and Technology (NIST). |
| `publication_family_name` | Permitted | NIST Special Publication (SP) 800-53. |
| `document_reference` | Permitted | NIST.SP.800-53r5. |
| `version_label` | Permitted | Revision 5 (with updates; OSCAL catalog Release 5.2.0 for identifier inventory). |
| `language` | Permitted | English. |
| `format` | Permitted | PDF (normative publication) and JSON (OSCAL catalog inventory source). |
| `publication_dates` | Permitted | September 2020 / 2020-12-10 current-final history date (day precision for the Dec. 10, 2020 update). |
| `retrieval_metadata` | Permitted | ESAF retrieval time, byte length, SHA-256, and page count of the official PDF; OSCAL catalog digest used for inventory derivation. |
| `official_urls` | Permitted | Landing, DOI, CSRC, PDF, and OSCAL URLs. |

## Attribution and endorsement boundary

Any ESAF publication that reproduces or derives from SP 800-53 Rev. 5 shall
attribute NIST as the source, identify NIST.SP.800-53r5 / SP 800-53 Rev. 5, and
shall not imply NIST approval, endorsement, certification, or assessment of ESAF
or of any mapped organization.

## Reconsideration trigger

Revisit this PASS only if NIST revises redistribution terms, withdraws the
public PDF or OSCAL catalog, or substitutes a rights regime that withdraws
derivative-work permission. A later rights FAIL or HOLD shall block mapping
publication until resolved.

## Decision boundaries

This review is not legal advice. It does not claim NIST approval, endorsement,
equivalence, compliance, certification, or assurance. It does not authorize
substantive mapping records while the readiness matrix remains `HOLD` for other
gates. It does not close Issues #55 or #60.

## Final decision

`PASS`. All six ESAF-1600 mapping field classes are permitted for public NIST SP 800-53 Rev. 5 content with attribution and without NIST endorsement claims.
