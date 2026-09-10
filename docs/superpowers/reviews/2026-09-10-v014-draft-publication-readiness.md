---
release: 0.14-draft
phase: published
tag: v0.14-draft
issue: 173
repository_scope: complete_git_tracked_repository
publication:
  date: "2026-09-10"
  condition: remote_annotated_tag_matches_exact_validated_commit
  evidence:
    - https://github.com/tdistress/ESAF/issues/173
    - https://github.com/tdistress/ESAF/actions/runs/34521088413
    - https://github.com/tdistress/ESAF/commit/7727d6f2bcf020ddf453374c95ed37f51e6e41ff
    - https://github.com/tdistress/ESAF/releases/tag/v0.14-draft
  tag_object: 0e3602c82b9898e2af575fd563042df9cce27675
  tagged_commit: 7727d6f2bcf020ddf453374c95ed37f51e6e41ff
  issue_evidence_url: https://github.com/tdistress/ESAF/issues/173
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
  iso_iec_42001: HOLD
  iso_iec_42001_path: crosswalks/iso-iec-42001.md
  nist_csf: HOLD
  nist_csf_path: crosswalks/nist-csf.md
  esaf_1500: working_draft_deepen
  esaf_1500_path: assessment/ESAF-1500.md
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
  iso_iec_42001_disposition: HOLD
  nist_csf_disposition: HOLD
gates:
  scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  technical: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  editorial: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  terminology: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  cross_reference_rendering: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  standards_mapping: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  profile_scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  release_metadata: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  governance: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/173]}
  post_merge: {state: closed, evidence: [https://github.com/tdistress/ESAF/actions/runs/34521088413]}
---

# v0.14-draft publication readiness

## Scope

This published record covers the complete Git-tracked repository. Its derived
inventory contains 91 controls in 16 families, 7 architecture patterns, 3
mapping sets, and 404 mapping provisions. The mappings contain 81 relationship
legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation and one Draft UK pilot
profile under the reusable profile contract. The PCI DSS readiness record has
the approved `HOLD` disposition, the NIST AI RMF readiness record has the
approved `HOLD` disposition, the ISO/IEC 42001 readiness record has the
approved `HOLD` disposition, and the NIST CSF 2.0 readiness record has the
approved `HOLD` disposition. None of those dispositions establish a mapping,
assessment, certification, compliance, equivalence, endorsement, or legal
conclusion.

## Prerequisite dispositions

Harness Phase 2 hosted-timing reconsideration is `DEFER`, recorded in
`docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md`.
ESAF-1300, ESAF-1400, and ESAF-1700 are linked as Working Drafts at
`governance/ESAF-1300.md`, `implementation/ESAF-1400.md`, and
`data-model/ESAF-1700.md`. ESAF-1200 remains a Working Draft at
`architectures/ESAF-1200.md`, but the milestone deepen disposition for
`v0.14-draft` is ESAF-1500. The NIST AI RMF crosswalk readiness decision is
`HOLD`, recorded at `crosswalks/nist-ai-rmf.md`. The ISO/IEC 42001 crosswalk
readiness decision is `HOLD`, recorded at `crosswalks/iso-iec-42001.md`. The
NIST CSF 2.0 crosswalk readiness decision is `HOLD`, recorded at
`crosswalks/nist-csf.md`.

The bounded Working Draft deepen pack required for `v0.14-draft` is present at:

- `assessment/ESAF-1500.md` (Working Draft `0.1.1`)

Issues 55 and 60 may remain open; this publication does not require their
closure.

## Lifecycle boundary

The current ESAF version is `0.14-draft`. The `v0.14-draft` Working Draft is
published. Publication is limited to the repository Working Draft and does not
change any artifact lifecycle state.

This record does not advance any Draft artifact, control, architecture
pattern, mapping set, or profile to an approved lifecycle state.

## Nonclaims

This published Working Draft does not claim certification, compliance,
equivalence, endorsement, assurance, or production readiness. It does not
close Issue 55 or Issue 60, and it does not clear the PCI DSS, HITRUST,
NIST AI RMF, ISO/IEC 42001, or NIST CSF blockers. While NIST AI RMF,
ISO/IEC 42001, or NIST CSF readiness remains `HOLD`, this package does not
authorize mapping authorship for those schemes.

## Publication evidence

The annotated `v0.14-draft` tag object is
`0e3602c82b9898e2af575fd563042df9cce27675` and peels to validated commit
`7727d6f2bcf020ddf453374c95ed37f51e6e41ff`. Post-merge validation evidence is
https://github.com/tdistress/ESAF/actions/runs/34521088413. Issue
[#173](https://github.com/tdistress/ESAF/issues/173) tracks the publication
gates. A consolidating issue comment may be added by the repository owner when
desired; it is not required to close the published record.
