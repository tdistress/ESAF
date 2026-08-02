---
release: 0.5-beta
phase: published
tag: v0.5-beta
issue: 59
repository_scope: complete_git_tracked_repository
publication:
  date: "2026-08-01"
  condition: remote_annotated_tag_matches_exact_validated_commit
  evidence:
    - https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331
  tag_object: fc2876cf52791edba6e923a25e0cdb8dec981e1c
  tagged_commit: 255f8806917aaf8c6a2441152b4638fc9fd2bfda
  issue_evidence_url: https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331
mapping_sets:
  - uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0
mapping_decision_basis: owner_risk_acceptance
scope:
  controls: 91
  control_families: 16
  architecture_patterns: 7
  mapping_sets: 3
  mapping_provisions: 404
  relationship_legs: 81
  negative_dispositions: 325
  assessment_foundation: true
  draft_profiles: 1
  pci_dss_disposition: HOLD
gates:
  scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  technical: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  editorial: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  terminology: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  cross_reference_rendering: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  standards_mapping: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  profile_scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  release_metadata: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  governance: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
  post_merge: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/59#issuecomment-5153256331]}
---

# v0.5-beta publication readiness

## Scope

This published record covers the complete Git-tracked repository. Its derived
inventory contains 91 controls in 16 families, 7 architecture patterns, 3
mapping sets, and 404 mapping provisions. The mappings contain 81 relationship
legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation and one Draft UK pilot
profile under the reusable profile contract. The PCI DSS readiness record has
the approved `HOLD` disposition. That disposition does not establish a PCI DSS
mapping, assessment, certification, compliance, equivalence, endorsement, or
legal conclusion.

## Lifecycle boundary

The current ESAF version is `0.5-beta`. The `v0.5-beta` Working Draft is
published. Publication is limited to the repository Working Draft and does not
change any artifact lifecycle state.

All controls, architecture patterns, the pilot profile, mapping sets, and
mapping records remain Draft. The three mapping lifecycle records have empty
event arrays. This publication does not add reviewer metadata, approval
metadata, or lifecycle events to those artifacts.

## Mapping assurance

This published Working Draft uses the owner-risk-acceptance mapping basis
recorded in front matter. Qualified approval remains deferred and requires a
validated six-role Draft campaign bound to the exact published commit. The
owner-risk decision permits only Working Draft publication; it does not
approve mappings or change artifact lifecycle state.

Issue 55 remains open for qualified review. Owner-risk acceptance does not
complete qualified review or approve the mappings. It does not establish
qualified mapping approval, artifact lifecycle approval,
certification, compliance, equivalence, endorsement, external scheme approval,
production readiness, assurance, implementation assessment, legal
sufficiency, or replacement of qualified professional judgment.

## Publication evidence

The exact annotated `v0.5-beta` tag object, tagged commit, publication date,
and issue 59 evidence URL are recorded in this record's front matter. This
body does not independently identify or replace that durable publication
evidence.
