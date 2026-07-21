---
schema_version: 1.0.0
mapping_set_id: uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0
authority:
  id: uk-ncsc
  name: UK National Cyber Security Centre
publication:
  id: cyber-essentials-plus-test-specification
  name: Cyber Essentials Plus Test Specification
source_version:
  id: "3.2"
  label: "3.2"
esaf_release:
  id: 0.4-alpha
  label: ESAF 0.4-alpha
  source_commit_sha: 7461d7137e3faf36b2b73a15f71100fa4ce11159
  control_catalog_sha256: 70bbd955a65969d2843b60220ad0aad2850f36ec6d189ecd32c40431b848b398
  control_manifest_path: ESAF_CONTROL_MANIFEST.json
mapping_set_version: 0.2.0
status: draft
source:
  official_url: https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf
  publication_date: "2025-04-28"
  access_class: public
  licensing_note: UK National Cyber Security Centre Crown copyright content reused under the Open Government Licence v3.0.
publication_rights:
  basis: The NCSC permits reuse of covered Crown copyright public-sector information under the Open Government Licence v3.0; the committed rights attestation limits this snapshot to approved field classes and original analysis.
  permitted_elements:
    - identifiers
    - titles
    - structural_inventory
    - paraphrases
    - derivative_mapping_analysis
    - official_links
  prohibited_elements: []
  restrictions: Attribute NCSC Crown copyright and the Open Government Licence v3.0; prohibit copied requirement or passage text and IASME-derived structure; exclude marks, imagery, and third-party material; do not imply official status, certification, compliance, equivalence, or endorsement.
  approved: true
  reviewer_id: esaf-reverse-mapping-rights-reviewer
  review_date: "2026-07-19"
  reviewer_authorized_source_access: true
  publication_basis_reviewed: true
scope:
  type: complete_publication
  statement: All 144 atomic provisions in the pinned complete-publication oracle for the public NCSC Cyber Essentials Plus Test Specification v3.2 are inventoried in oracle order.
  inventory_count: 144
  default_granularity: requirement
mapper:
  id: esaf-crosswalk-editorial-team
  qualification: ESAF crosswalk editorial team applying the approved public-v3.2 reverse-evidence design and source-rights boundary.
  date: "2026-07-19"
  authorized_source_access: true
findings: []
change_history:
  - version: 0.2.0
    date: "2026-07-19"
    change: Created the complete draft external-to-ESAF evidence mapping, provision inventory, and release-pinned manifest.
---
# Cyber Essentials Plus Test Specification v3.2 external-to-ESAF mapping

This authoritative snapshot is a complete-publication, unqualified technical draft for the `external_to_esaf` direction. Complete-publication means inventory coverage of the pinned public NCSC v3.2 source only. It is not the current operational scheme and does not establish assessment execution, certification, compliance, equivalence, endorsement, implementation, effectiveness, aggregate sufficiency, population-wide coverage, or continuous assurance.

## Source and immutable pins

- Oracle: `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`
- Oracle SHA-256: `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`
- ESAF baseline: release `0.4-alpha`, commit `7461d7137e3faf36b2b73a15f71100fa4ce11159`, 91 controls

## Rights boundary

NCSC Crown copyright is attributed to the UK National Cyber Security Centre under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Copied requirement or passage text is prohibited. IASME-authored structure remains outside this snapshot. Marks and imagery are excluded, as is third-party material without separate permission.

## Draft mapping results

The snapshot contains 144 records: 32 mapped provisions, 32 relationship legs referencing 10 distinct controls, and 112 no-direct-mapping dispositions. All relationship legs are reverse-only `external_to_esaf` observations with `partially_supports` taxonomy. Each mapped leg binds a dated external observation to one exact normative ESAF requirement and preserves the full 11-condition evidence contract, expected evidence, known gaps, and prohibited inferences. Conditions narrow the supported claim and do not create a missing external result or ESAF outcome.

Every no-direct-mapping record identifies the provision-specific external result and missing ESAF outcome. Administrative artifacts, assessor activity, decision rules, aggregate results, recommendations, and adjacent technical procedures remain negative unless the provision produces a bounded observation of an exact ESAF requirement.

## Assurance and lifecycle boundary

Every mapped observation is point-in-time evidence limited to its assessment date, evidence date, defined population, selected sample, method, provenance, exceptions, and Delivery Partner discretion. A relationship does not establish ongoing state, full-population coverage, control implementation or effectiveness, evidence sufficiency, certification, compliance, equivalence, current-scheme coverage, or continuous assurance.

All 144 records, 32 relationship legs, and lifecycle metadata remain draft. The lifecycle event array is empty. Independent technical reconciliation and review do not qualify or approve the mapping and do not replace future qualified SME review.
