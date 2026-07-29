---
release: 0.5-beta
phase: closure_candidate
tag: v0.5-beta
issue: 59
repository_scope: complete_git_tracked_repository
publication:
  date: null
  condition: remote_annotated_tag_matches_exact_validated_commit
  evidence:
    - https://github.com/tdistress/ESAF/issues/59
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
  scope: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  technical: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  editorial: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  terminology: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  cross_reference_rendering: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  standards_mapping: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  profile_scope: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  release_metadata: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  governance: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/69]}
  post_merge: {state: open, evidence: []}
---

# v0.5-beta publication readiness

## Scope

This closure candidate covers the complete Git-tracked repository. Its derived
inventory contains 91 controls in 16 families, 7 architecture patterns, 3
mapping sets, and 404 mapping provisions. The mappings contain 81 relationship
legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation and one Draft UK pilot
profile under the reusable profile contract. The PCI DSS readiness record has
the approved `HOLD` disposition. That disposition does not establish a PCI DSS
mapping, assessment, certification, compliance, equivalence, endorsement, or
legal conclusion.

## Lifecycle boundary

The current ESAF version is `0.5-beta`. The non-post-merge v0.5 gates are ready,
the post-merge gate is open, and the `v0.5-beta` tag has not been created. The
`v0.5-beta` release status is Working Draft. This closure candidate does not
approve publication.

All controls, architecture patterns, the pilot profile, mapping sets, and
mapping records remain Draft. The three mapping lifecycle records have empty
event arrays. This release work does not add reviewer metadata, approval
metadata, or lifecycle events to those artifacts.

## Mapping assurance

The release design permits one uniform mapping basis for all three mapping
sets. Qualified approval requires a validated six-role Draft campaign bound
to the exact closure candidate. Owner-risk acceptance requires a separate,
authenticated repository-owner decision created after that exact candidate
exists. No such v0.5 decision is recorded here.

Issue 55 remains open for qualified review. Owner-risk acceptance, if later
given for the exact candidate, would permit only Working Draft publication. It
would not complete qualified review or approve the mappings. It would not
establish qualified mapping approval, artifact lifecycle approval,
certification, compliance, equivalence, endorsement, external scheme approval,
production readiness, assurance, implementation assessment, legal
sufficiency, or replacement of qualified professional judgment.

## Conditional publication

Publication remains conditional on the remote annotated `v0.5-beta` tag
resolving to the exact validated merged commit. This closure candidate requires
its own exact-head reviews, rendering evidence, owner and scope decision,
governance decision, successful checks, and clean merge state. The post-merge
gate remains open until merged-main validation and remote tag verification are
complete.
