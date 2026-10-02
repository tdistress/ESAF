---
schema_version: 1.0.0
mapping_set_id: nist--csf--2.0--esaf-0.17-draft--0.1.0
authority:
  id: nist
  name: National Institute of Standards and Technology
publication:
  id: csf
  name: The NIST Cybersecurity Framework (CSF) 2.0
source_version:
  id: '2.0'
  label: '2.0'
esaf_release:
  id: 0.17-draft
  label: ESAF 0.17-draft
  source_commit_sha: 2ae3b6616f50a150aa0959acb58b2d9da48fda6a
  control_catalog_sha256: 70bbd955a65969d2843b60220ad0aad2850f36ec6d189ecd32c40431b848b398
  control_manifest_path: ESAF_CONTROL_MANIFEST.json
mapping_set_version: 0.1.0
status: draft
source:
  official_url: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
  publication_date: '2024-02-26'
  access_class: public
  licensing_note: U.S. government work / NIST technical series; public PDF reused with attribution and no-endorsement constraints.
publication_rights:
  basis: The ESAF publication-rights review records PASS for identifiers, titles, structural inventory, paraphrases, derivative mapping analysis, and official links under U.S. government work and NIST technical-series practice.
  permitted_elements:
  - identifiers
  - titles
  - structural_inventory
  - paraphrases
  - derivative_mapping_analysis
  - official_links
  prohibited_elements: []
  restrictions: Attribute NIST.CSWP.29; do not imply NIST approval, endorsement, certification, or official status; prefer original paraphrases over copied requirement text; do not commit PDF bytes.
  approved: true
  reviewer_id: nist-csf-publication-rights-reviewer
  review_date: '2026-10-02'
  reviewer_authorized_source_access: true
  publication_basis_reviewed: true
scope:
  type: complete_publication
  statement: Every NIST CSF 2.0 subcategory identifier in the pinned public inventory is inventoried.
  inventory_count: 106
  default_granularity: requirement
mapper:
  id: esaf-project-owner
  qualification: ESAF Project Maintainer applying ESAF-1600 under the 2026-10-02 owner-risk people-gate disposition for Draft-only NIST CSF mapping authorship.
  date: '2026-10-02'
  authorized_source_access: true
findings: []
change_history:
- version: 0.1.0
  date: '2026-10-02'
  change: Created the authoritative draft NIST CSF 2.0 complete-publication mapping snapshot.
---
# NIST CSF 2.0 to ESAF 0.17-draft

This authoritative snapshot is a complete machine-validatable draft containing 106 provision records, 162 forward-only relationship legs, and 10 no-direct-mapping dispositions. It does not establish certification, compliance, equivalence, legal sufficiency, NIST endorsement, or official status.

`PROVISION_INVENTORY.md` fixes the complete-publication scope, and `ESAF_CONTROL_MANIFEST.json` pins every referenced control to the stated ESAF baseline. The [NIST CSF landing page](../../../../../../nist-csf.md) provides the repository entry point.

## Source and publication rights

The source is NIST.CSWP.29, *The NIST Cybersecurity Framework (CSF) 2.0*, published 2024-02-26. The uncommitted source PDF had SHA-256 `3c31f46fee98cac0c4323453e5109291a213b4de7fef8c058af9bf67f717433c`. Official PDF bytes are not committed.

## Scope boundary

The complete-publication inventory contains 106 subcategory identifiers across GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, and RECOVER.

## Draft mapping results and gaps

The 106 provision records contain 162 forward-only relationship legs and 10 no-direct-mapping dispositions. Each relationship records its conditions, expected evidence, and known gaps. Multiple relationships are not treated as collectively sufficient.

Prominent gaps retained as negatives include enterprise hardware inventories, physical access and environmental monitoring, cyber threat intelligence integration, hardware maintenance programs, positive-risk opportunity characterization, HR cybersecurity practices, and public incident-recovery messaging where ESAF does not expressly provide those outcomes.

## Draft lifecycle

The ESAF baseline is pinned to commit `2ae3b6616f50a150aa0959acb58b2d9da48fda6a`. All provision records and relationship legs remain draft. Owner-risk readiness GO does not constitute qualified NIST CSF review or lifecycle approval. This mapping set has no schema reviewer or approver and an empty lifecycle event array pending qualified human review.
