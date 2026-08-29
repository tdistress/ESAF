---
release: 0.9-rc1
phase: evidence_candidate
tag: v0.9-rc1
issue: 95
repository_scope: complete_git_tracked_repository
publication:
  date: null
  condition: remote_annotated_tag_matches_exact_validated_commit
  evidence: []
  tag_object: null
  tagged_commit: null
  issue_evidence_url: null
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
  scope: {state: open, evidence: []}
  technical: {state: open, evidence: []}
  editorial: {state: open, evidence: []}
  terminology: {state: open, evidence: []}
  cross_reference_rendering: {state: open, evidence: []}
  standards_mapping: {state: open, evidence: []}
  profile_scope: {state: open, evidence: []}
  release_metadata: {state: open, evidence: []}
  governance: {state: open, evidence: []}
  post_merge: {state: open, evidence: []}
---

# v0.9-rc1 publication readiness

## Scope

This evidence candidate covers the complete Git-tracked repository. Its
derived inventory contains 91 controls in 16 families, 7 architecture
patterns, 3 mapping sets, and 404 mapping provisions. The mappings contain 81
relationship legs and 325 negative dispositions.

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
open; this candidate does not require their closure.

## Lifecycle boundary

The current published ESAF version remains `0.5-beta` until closure. This
candidate is a Working Draft release candidate only; every v0.9 gate is
`open`, no closure candidate exists, and the `v0.9-rc1` tag has not been
created. This record does not advance any Draft artifact, control,
architecture pattern, mapping set, or profile to an approved lifecycle state.

## Nonclaims

This evidence candidate does not claim certification, compliance,
equivalence, endorsement, assurance, or production readiness. It does not
close Issue 55 or Issue 60, and it does not clear the PCI DSS or HITRUST
blockers. It does not approve publication.

## Publication evidence

This is an evidence candidate. The publication `date`, `tag_object`,
`tagged_commit`, and `issue_evidence_url` fields remain `null` and the
`evidence` list remains empty. The publication statement is deferred until
after merge to `main` and creation of the annotated `v0.9-rc1` tag on the
exact validated merged commit.
