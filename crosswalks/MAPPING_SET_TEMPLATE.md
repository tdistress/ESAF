---
schema_version: 1.0.0
mapping_set_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.0.0
authority:
  id: example-authority
  name: Example Authority
publication:
  id: example-standard
  name: Example Standard
source_version:
  id: "2026.1"
  label: "2026.1"
esaf_release:
  id: 0.5-beta
  label: ESAF 0.5-beta
  source_commit_sha: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
  tag_alias: v0.5-beta
  control_catalog_sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  control_manifest_path: ESAF_CONTROL_MANIFEST.json
mapping_set_version: 1.0.0
status: draft
source:
  official_url: https://example.com/example-standard
  publication_date: "2026-01-15"
  access_class: public
  licensing_note: Non-authoritative example source used only to demonstrate metadata.
publication_rights:
  basis: Example publication-rights review approved use of identifiers and original analysis.
  permitted_elements:
    - identifiers
    - structural_inventory
    - paraphrases
    - derivative_mapping_analysis
    - official_links
  prohibited_elements:
    - titles
  restrictions: Do not reproduce source requirement text.
  approved: true
  reviewer_id: rights-reviewer-1
  review_date: "2026-07-13"
  reviewer_authorized_source_access: true
  publication_basis_reviewed: true
scope:
  type: complete_publication
  statement: Every provision in the non-authoritative example publication.
  inventory_count: 4
  default_granularity: requirement
mapper:
  id: mapper-1
  qualification: Example mapper qualification statement.
  date: "2026-07-13"
  authorized_source_access: true
reviewer:
  id: reviewer-1
  qualification: Independent example subject-matter reviewer.
  date: "2026-07-14"
  authorized_source_access: true
  findings_disposition: All Critical and Important findings are resolved.
approver:
  id: approver-1
  date: "2026-07-15"
predecessor_id: example-authority--example-standard--2026.1--esaf-0.5-beta--0.9.0
findings:
  - finding_id: example-finding-resolved
    affected_record_ids:
      - ex-1-1
    severity: Important
    status: resolved
    description: The directional rationale required clarification.
    disposition: The mapper revised the rationale and the reviewer verified the correction.
    resolver_or_acceptor: reviewer-1
    disposition_date: "2026-07-14"
change_history:
  - version: 1.0.0
    date: "2026-07-13"
    change: Created the non-authoritative example mapping set.
---
# Mapping-set authoring template

This file is a non-authoritative example. Copy its structure into a versioned snapshot and replace every example value before review.

## Scope boundary

Describe the exact publication or declared subset represented by the provision inventory.

## Source and publication rights

Record the authoritative source, access basis, permission boundary, restrictions, and completed independent rights review.

## Mapping and review method

Describe mapper qualifications, analytical method, independent review, and findings disposition without asserting outcome sufficiency.

### Accepted Minor finding shape

Use `accepted` only for a Minor finding and record the named acceptor, date, and rationale. This fenced example is parsed explicitly by the foundation tests and remains outside mapping discovery.

```yaml
finding_id: example-finding-accepted
affected_record_ids:
  - ex-1-2
severity: Minor
status: accepted
description: A minor editorial ambiguity remains.
disposition: The approval authority accepted the documented limitation.
resolver_or_acceptor: approver-1
disposition_date: "2026-07-15"
acceptance_rationale: The ambiguity does not alter the mapping analysis and is documented for the next revision.
```

## Change rationale

Explain this mapping-set version and identify a predecessor when applicable.
