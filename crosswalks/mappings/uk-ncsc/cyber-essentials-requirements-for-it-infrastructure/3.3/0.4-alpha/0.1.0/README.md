---
schema_version: 1.0.0
mapping_set_id: uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0
authority:
  id: uk-ncsc
  name: UK National Cyber Security Centre
publication:
  id: cyber-essentials-requirements-for-it-infrastructure
  name: "Cyber Essentials: Requirements for IT Infrastructure"
source_version:
  id: "3.3"
  label: "3.3"
esaf_release:
  id: 0.4-alpha
  label: ESAF 0.4-alpha
  source_commit_sha: 5de9ff356ddad1e193444cd7308eff16ed83e811
  control_catalog_sha256: 70bbd955a65969d2843b60220ad0aad2850f36ec6d189ecd32c40431b848b398
  control_manifest_path: ESAF_CONTROL_MANIFEST.json
mapping_set_version: 0.1.0
status: draft
source:
  official_url: https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf
  publication_date: "2026-04-27"
  access_class: public
  licensing_note: UK National Cyber Security Centre Crown copyright content reused under the Open Government Licence v3.0.
publication_rights:
  basis: The NCSC permits reuse of its Crown copyright website content under the Open Government Licence v3.0 unless otherwise indicated; this snapshot contains identifiers, titles, structural inventory, original paraphrases, original mapping analysis, and official links.
  permitted_elements:
    - identifiers
    - titles
    - structural_inventory
    - paraphrases
    - derivative_mapping_analysis
    - official_links
  prohibited_elements: []
  restrictions: Acknowledge NCSC Crown copyright and the Open Government Licence v3.0; do not use NCSC or government logos, reproduce third-party material, or imply endorsement, certification, or official status; prefer original paraphrases over copied requirement text.
  approved: true
  reviewer_id: esaf-project-owner
  review_date: "2026-07-13"
  reviewer_authorized_source_access: true
  publication_basis_reviewed: true
scope:
  type: complete_publication
  statement: Every independently testable prescriptive provision in sections D and E of Cyber Essentials Requirements for IT Infrastructure v3.3 is inventoried.
  inventory_count: 116
  default_granularity: requirement
mapper:
  id: esaf-crosswalk-editorial-team
  qualification: ESAF crosswalk editorial team applying the approved ESAF-1600 Cyber Essentials v3.3 atomization and mapping design.
  date: "2026-07-13"
  authorized_source_access: true
findings: []
change_history:
  - version: 0.1.0
    date: "2026-07-13"
    change: Created the authoritative draft scaffold and complete provision inventory.
---
# Cyber Essentials v3.3 to ESAF 0.4-alpha

This authoritative snapshot is an incomplete draft. It inventories the source publication but contains no provision mapping records yet. It does not establish certification, compliance, equivalence, legal sufficiency, NCSC endorsement, or official status.

## Source and publication rights

The source is the UK National Cyber Security Centre publication *Cyber Essentials: Requirements for IT Infrastructure v3.3*, published 2026-04-27 and accessed 2026-07-13 at the official URL recorded above. The uncommitted source PDF had SHA-256 `e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923`.

NCSC Crown copyright material is attributed to the UK National Cyber Security Centre and reused under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). The source PDF, logos, and third-party material are not committed. Original paraphrases and derivative mapping analysis will be used instead of copied requirement text.

The IDs `CE3.3-D-001` through `CE3.3-E5-012` are ESAF-assigned citation identifiers. They are not identifiers printed, issued, or endorsed by the NCSC.

## Scope boundary

The complete-publication inventory contains 116 independently testable prescriptive provisions:

| Source group | Count |
|---|---:|
| D. Scope | 44 |
| E.1 Firewalls | 12 |
| E.2 Secure Configuration | 12 |
| E.3 Security Update Management | 7 |
| E.4 User Access Control | 29 |
| E.5 Malware Protection | 12 |
| **Total** | **116** |

Included material comprises explicit must statements, imperatives, need-to statements, independently testable prescriptive should statements, declarative scope classifications, independently testable conjunctive outcomes, independently applicable triggers, and meaningful scope-table classifications.

Excluded informative material comprises definitions, aims, examples, explanatory introductions, information boxes, section C backup guidance, section F zero-trust guidance, statements expressly identified as non-mandatory guidance, N/A table cells, repeated clarifications, and umbrella statements fully operationalized by following provisions. Cyber Essentials Plus is outside this mapping set and requires a separate source-versioned mapping set.

## Draft lifecycle

The ESAF baseline is pinned to commit `5de9ff356ddad1e193444cd7308eff16ed83e811`. All 91 manifest controls are draft version 0.1.0. This mapping set remains draft with no schema reviewer or approver and an empty lifecycle event array pending qualified human review.
