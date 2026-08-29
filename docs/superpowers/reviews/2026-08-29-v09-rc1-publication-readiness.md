---
release: 0.9-rc1
phase: published
tag: v0.9-rc1
issue: 95
repository_scope: complete_git_tracked_repository
publication:
  date: "2026-08-29"
  condition: remote_annotated_tag_matches_exact_validated_commit
  evidence:
    - https://github.com/tdistress/ESAF/issues/95
    - https://github.com/tdistress/ESAF/actions/runs/33277455030
    - https://github.com/tdistress/ESAF/commit/4136cfdc71a85ea2becd0f23c95424e7580cafa3
    - https://github.com/tdistress/ESAF/releases/tag/v0.9-rc1
  tag_object: 1b5cdead5c56c4f209b5cf091c665ca40e709590
  tagged_commit: 4136cfdc71a85ea2becd0f23c95424e7580cafa3
  issue_evidence_url: https://github.com/tdistress/ESAF/issues/95
prerequisite_dispositions:
  phase2_timing: DEFER
  phase2_evidence: docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md
  esaf_1300: working_draft
  esaf_1300_path: governance/ESAF-1300.md
  esaf_1400: working_draft
  esaf_1400_path: implementation/ESAF-1400.md
  esaf_1700: working_draft
  esaf_1700_path: data-model/ESAF-1700.md
  nist_ai_rmf: HOLD
  nist_ai_rmf_path: crosswalks/nist-ai-rmf.md
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
  nist_ai_rmf_disposition: HOLD
gates:
  scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  technical: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  editorial: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  terminology: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  cross_reference_rendering: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  standards_mapping: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  profile_scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  release_metadata: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  governance: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/95]}
  post_merge: {state: closed, evidence: [https://github.com/tdistress/ESAF/actions/runs/33277455030]}
---

# v0.9-rc1 publication readiness

## Scope

This published record covers the complete Git-tracked repository. Its derived
inventory contains 91 controls in 16 families, 7 architecture patterns, 3
mapping sets, and 404 mapping provisions. The mappings contain 81 relationship
legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation and one Draft UK pilot
profile under the reusable profile contract. The PCI DSS readiness record has
the approved `HOLD` disposition, and the NIST AI RMF readiness record has the
approved `HOLD` disposition. Neither disposition establishes a mapping,
assessment, certification, compliance, equivalence, endorsement, or legal
conclusion.

## Prerequisite dispositions

Harness Phase 2 hosted-timing reconsideration is `DEFER`, recorded in
`docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md`.
ESAF-1300, ESAF-1400, and ESAF-1700 are linked as Working Drafts at
`governance/ESAF-1300.md`, `implementation/ESAF-1400.md`, and
`data-model/ESAF-1700.md`. The NIST AI RMF crosswalk readiness decision is
`HOLD`, recorded at `crosswalks/nist-ai-rmf.md`. Issues 55 and 60 may remain
open; this publication does not require their closure.

## Lifecycle boundary

The current ESAF version is `0.9-rc1`. The `v0.9-rc1` Working Draft is
published. Publication is limited to the repository Working Draft and does not
change any artifact lifecycle state.

This record does not advance any Draft artifact, control, architecture
pattern, mapping set, or profile to an approved lifecycle state.

## Nonclaims

This published Working Draft does not claim certification, compliance,
equivalence, endorsement, assurance, or production readiness. It does not
close Issue 55 or Issue 60, and it does not clear the PCI DSS or HITRUST
blockers.

## Publication evidence

The annotated `v0.9-rc1` tag object is
`1b5cdead5c56c4f209b5cf091c665ca40e709590` and peels to validated commit
`4136cfdc71a85ea2becd0f23c95424e7580cafa3`. Post-merge validation evidence is
https://github.com/tdistress/ESAF/actions/runs/33277455030. Issue
[#95](https://github.com/tdistress/ESAF/issues/95) tracks the publication
gates. A consolidating issue comment may be added by the repository owner when
write access to issues is available.
