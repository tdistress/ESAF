---
release: 0.15-draft
phase: evidence_candidate
tag: v0.15-draft
issue: 185
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
  esaf_1300: working_draft_deepen
  esaf_1300_path: governance/ESAF-1300.md
  esaf_1400: working_draft_deepen
  esaf_1400_path: implementation/ESAF-1400.md
  esaf_1700: working_draft_deepen
  esaf_1700_path: data-model/ESAF-1700.md
  nist_ai_rmf: HOLD
  nist_ai_rmf_path: crosswalks/nist-ai-rmf.md
  iso_iec_42001: HOLD
  iso_iec_42001_path: crosswalks/iso-iec-42001.md
  nist_csf: HOLD
  nist_csf_path: crosswalks/nist-csf.md
  iso_iec_27001: HOLD
  iso_iec_27001_path: crosswalks/iso-iec-27001.md
  esaf_1500: working_draft
  esaf_1500_path: assessment/ESAF-1500.md
  phase6_toolkit: working_draft_second_deepen
  phase6_toolkit_path: assessment/workbook/README.md
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
  iso_iec_27001_disposition: HOLD
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

# v0.15-draft publication readiness

## Scope

This evidence-candidate record covers the complete Git-tracked repository. Its
derived inventory contains 91 controls in 16 families, 7 architecture patterns,
3 mapping sets, and 404 mapping provisions. The mappings contain 81 relationship
legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation and one Draft UK pilot
profile under the reusable profile contract. The PCI DSS readiness record has
the approved `HOLD` disposition, the NIST AI RMF readiness record has the
approved `HOLD` disposition, the ISO/IEC 42001 readiness record has the
approved `HOLD` disposition, the NIST CSF 2.0 readiness record has the
approved `HOLD` disposition, and the ISO/IEC 27001:2022 readiness record has
the approved `HOLD` disposition. None of those dispositions establish a mapping,
assessment, certification, compliance, equivalence, endorsement, or legal
conclusion.

## Prerequisite dispositions

Harness Phase 2 hosted-timing reconsideration is `DEFER`, recorded in
`docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md`.
ESAF-1300, ESAF-1400, and ESAF-1700 are linked as Working Draft deepen packs at
Working Draft `0.3.0` in `governance/ESAF-1300.md`,
`implementation/ESAF-1400.md`, and `data-model/ESAF-1700.md`. ESAF-1500
remains a Working Draft carry-forward at `assessment/ESAF-1500.md` (Working
Draft `0.1.1`) from the `v0.14-draft` deepen; it is not the milestone deepen
target for `v0.15-draft`. The NIST AI RMF crosswalk readiness decision is
`HOLD`, recorded at `crosswalks/nist-ai-rmf.md`. The ISO/IEC 42001 crosswalk
readiness decision is `HOLD`, recorded at `crosswalks/iso-iec-42001.md`. The
NIST CSF 2.0 crosswalk readiness decision is `HOLD`, recorded at
`crosswalks/nist-csf.md`. The ISO/IEC 27001:2022 crosswalk readiness decision
is `HOLD`, recorded at `crosswalks/iso-iec-27001.md`.

The bounded Phase 6 assessment toolkit second deepen required for
`v0.15-draft` is present at:

- `assessment/workbook/README.md` (second deepen marker)

Issues 55 and 60 may remain open; this publication does not require their
closure.

## Lifecycle boundary

The current ESAF version is still `0.14-draft` until the later
`closure_candidate` metadata sync. The `v0.15-draft` Working Draft is an
evidence candidate and is not yet published. Publication, when completed, is
limited to the repository Working Draft and does not change any artifact
lifecycle state.

This record does not advance any Draft artifact, control, architecture
pattern, mapping set, or profile to an approved lifecycle state.

## Nonclaims

This evidence-candidate Working Draft package does not claim certification,
compliance, equivalence, endorsement, assurance, or production readiness. It
does not close Issue 55 or Issue 60, and it does not clear the PCI DSS,
HITRUST, NIST AI RMF, ISO/IEC 42001, NIST CSF, or ISO/IEC 27001 blockers.
While NIST AI RMF, ISO/IEC 42001, NIST CSF, or ISO/IEC 27001 readiness remains
`HOLD`, this package does not authorize mapping authorship for those schemes.

## Publication evidence

Publication evidence is not yet bound in the `evidence_candidate` phase.
Annotated tag identity, tagged commit, and post-merge validation evidence
remain unset until the published phase. Issue
[#185](https://github.com/tdistress/ESAF/issues/185) tracks the publication
gates.
