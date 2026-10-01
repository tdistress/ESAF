---
schema_version: 1.0.0
mapping_set_id: nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0
authority:
  id: nist
  name: National Institute of Standards and Technology
publication:
  id: ai-rmf
  name: "Artificial Intelligence Risk Management Framework (AI RMF 1.0)"
source_version:
  id: "1.0"
  label: "1.0"
esaf_release:
  id: 0.17-draft
  label: ESAF 0.17-draft
  source_commit_sha: 31995e73f8fcab1348c0fafed185debfd544951a
  control_catalog_sha256: 70bbd955a65969d2843b60220ad0aad2850f36ec6d189ecd32c40431b848b398
  control_manifest_path: ESAF_CONTROL_MANIFEST.json
mapping_set_version: 0.1.0
status: draft
source:
  official_url: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
  publication_date: "2023-01-26"
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
  restrictions: Attribute NIST.AI.100-1; do not imply NIST approval, endorsement, certification, or official status; prefer original paraphrases over copied requirement text; do not commit PDF bytes.
  approved: true
  reviewer_id: nist-ai-rmf-publication-rights-reviewer
  review_date: "2026-10-01"
  reviewer_authorized_source_access: true
  publication_basis_reviewed: true
scope:
  type: complete_publication
  statement: Every NIST AI RMF 1.0 Core subcategory identifier in the pinned public inventory is inventoried.
  inventory_count: 72
  default_granularity: requirement
mapper:
  id: esaf-project-owner
  qualification: ESAF Project Maintainer applying ESAF-1600 under the 2026-10-01 owner-risk people-gate disposition for Draft-only NIST AI RMF mapping authorship.
  date: "2026-10-01"
  authorized_source_access: true
findings: []
change_history:
  - version: 0.1.0
    date: "2026-10-01"
    change: Created the authoritative draft NIST AI RMF 1.0 complete-publication mapping snapshot.
---
# NIST AI RMF 1.0 to ESAF 0.17-draft

This authoritative snapshot is a complete machine-validatable draft containing 72 provision records, 163 forward-only relationship legs, and 8 no-direct-mapping dispositions. It does not establish certification, compliance, equivalence, legal sufficiency, NIST endorsement, or official status.

`PROVISION_INVENTORY.md` fixes the complete-publication scope, and `ESAF_CONTROL_MANIFEST.json` pins every referenced control to the stated ESAF baseline. The [NIST AI RMF landing page](../../../../../../nist-ai-rmf.md) provides the repository entry point.

## Source and publication rights

The source is NIST.AI.100-1, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, published 2023-01-26. The uncommitted source PDF had SHA-256 `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1`. Official PDF bytes are not committed.

## Scope boundary

The complete-publication inventory contains 72 Core subcategory identifiers across GOVERN, MAP, MEASURE, and MANAGE.

## Draft mapping results and gaps

The 72 provision records contain 163 forward-only relationship legs and 8 no-direct-mapping dispositions. Each relationship records its conditions, expected evidence, and known gaps. Multiple relationships are not treated as collectively sufficient.

Prominent gaps retained as negatives include human-subject protection evaluations, environmental sustainability of model training, and regular engagement with potentially impacted communities of practice where ESAF does not expressly provide those outcomes.

## Draft lifecycle

The ESAF baseline is pinned to commit `31995e73f8fcab1348c0fafed185debfd544951a`. All provision records and relationship legs remain draft. Owner-risk readiness GO does not constitute qualified NIST AI RMF review or lifecycle approval. This mapping set has no schema reviewer or approver and an empty lifecycle event array pending qualified human review.
