---
release: 0.12-draft
phase: published
tag: v0.12-draft
issue: 146
repository_scope: complete_git_tracked_repository
publication:
  date: "2026-09-07"
  condition: remote_annotated_tag_matches_exact_validated_commit
  evidence:
    - https://github.com/tdistress/ESAF/issues/146
    - https://github.com/tdistress/ESAF/actions/runs/34094275390
    - https://github.com/tdistress/ESAF/commit/6546f2cacbbfaa89c7828991768e623b42a8081d
    - https://github.com/tdistress/ESAF/releases/tag/v0.12-draft
  tag_object: 3c11c7a0261314ce9519a4e3f4cad9357a3fcbe6
  tagged_commit: 6546f2cacbbfaa89c7828991768e623b42a8081d
  issue_evidence_url: https://github.com/tdistress/ESAF/issues/146
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
  esaf_1000: working_draft_deepen
  esaf_1000_path: framework/ESAF-1000.md
  esaf_1100: working_draft_deepen
  esaf_1100_path: controls/ESAF-1100.md
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
gates:
  scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  technical: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  editorial: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  terminology: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  cross_reference_rendering: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  standards_mapping: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  profile_scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  release_metadata: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  governance: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/146]}
  post_merge: {state: closed, evidence: [https://github.com/tdistress/ESAF/actions/runs/34094275390]}
---

# v0.12-draft publication readiness

## Scope

This published record covers the complete Git-tracked repository. Its derived
inventory contains 91 controls in 16 families, 7 architecture patterns, 3
mapping sets, and 404 mapping provisions. The mappings contain 81 relationship
legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation and one Draft UK pilot
profile under the reusable profile contract. The PCI DSS readiness record has
the approved `HOLD` disposition, the NIST AI RMF readiness record has the
approved `HOLD` disposition, and the ISO/IEC 42001 readiness record has the
approved `HOLD` disposition. None of those dispositions establish a mapping,
assessment, certification, compliance, equivalence, endorsement, or legal
conclusion.

## Prerequisite dispositions

Harness Phase 2 hosted-timing reconsideration is `DEFER`, recorded in
`docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md`.
ESAF-1300, ESAF-1400, and ESAF-1700 are linked as Working Drafts at
`governance/ESAF-1300.md`, `implementation/ESAF-1400.md`, and
`data-model/ESAF-1700.md`. The NIST AI RMF crosswalk readiness decision is
`HOLD`, recorded at `crosswalks/nist-ai-rmf.md`. The ISO/IEC 42001 crosswalk
readiness decision is `HOLD`, recorded at `crosswalks/iso-iec-42001.md`.

The bounded Working Draft deepen packs required for `v0.12-draft` are present
at:

- `framework/ESAF-1000.md` (Working Draft `0.2.1`)
- `controls/ESAF-1100.md` (Working Draft `0.3.1`)

A second Phase 6 toolkit deepen is not a `v0.12-draft` exit criterion. Issues
55 and 60 may remain open; this publication does not require their closure.

## Lifecycle boundary

The current ESAF version is `0.12-draft`. The `v0.12-draft` Working Draft is
published. Publication is limited to the repository Working Draft and does not
change any artifact lifecycle state.

This record does not advance any Draft artifact, control, architecture
pattern, mapping set, or profile to an approved lifecycle state.

## Nonclaims

This published Working Draft does not claim certification, compliance,
equivalence, endorsement, assurance, or production readiness. It does not
close Issue 55 or Issue 60, and it does not clear the PCI DSS, HITRUST,
NIST AI RMF, or ISO/IEC 42001 blockers. While NIST AI RMF or ISO/IEC 42001
readiness remains `HOLD`, this package does not authorize mapping authorship
for those schemes.

## Publication evidence

The annotated `v0.12-draft` tag object is
`3c11c7a0261314ce9519a4e3f4cad9357a3fcbe6` and peels to validated commit
`6546f2cacbbfaa89c7828991768e623b42a8081d`. Post-merge validation evidence is
https://github.com/tdistress/ESAF/actions/runs/34094275390. Issue
[#146](https://github.com/tdistress/ESAF/issues/146) tracks the publication
gates. A consolidating issue comment may be added by the repository owner when
desired; it is not required to close the published record.
