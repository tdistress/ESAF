---
release: 0.17-draft
phase: closure_candidate
tag: v0.17-draft
issue: 208
repository_scope: complete_git_tracked_repository
publication:
  date: null
  condition: remote_annotated_tag_matches_exact_validated_commit
  evidence:
    - https://github.com/tdistress/ESAF/issues/208
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
  nist_sp_800_53: HOLD
  nist_sp_800_53_path: crosswalks/nist-sp-800-53.md
  cis_controls: HOLD
  cis_controls_path: crosswalks/cis-controls.md
  esaf_1500: working_draft
  esaf_1500_path: assessment/ESAF-1500.md
  phase6_toolkit: working_draft_third_deepen
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
  nist_sp_800_53_disposition: HOLD
  cis_controls_disposition: HOLD
gates:
  scope: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/212]}
  technical: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/170410c42d9f4cc3d40a02f7147e6cbc06a852e6/docs/superpowers/reviews/2026-09-16-v017-draft-technical-review.md]}
  editorial: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/170410c42d9f4cc3d40a02f7147e6cbc06a852e6/docs/superpowers/reviews/2026-09-16-v017-draft-editorial-review.md]}
  terminology: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/170410c42d9f4cc3d40a02f7147e6cbc06a852e6/docs/superpowers/reviews/2026-09-16-v017-draft-editorial-review.md]}
  cross_reference_rendering: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/212]}
  standards_mapping: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/212]}
  profile_scope: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/212]}
  release_metadata: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/212]}
  governance: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/170410c42d9f4cc3d40a02f7147e6cbc06a852e6/docs/superpowers/reviews/2026-09-16-v017-draft-governance-review.md]}
  post_merge: {state: open, evidence: []}
---

# v0.17-draft publication readiness

## Scope

This closure-candidate record covers the complete Git-tracked repository. Its
derived inventory contains 91 controls in 16 families, 7 architecture patterns,
3 mapping sets, and 404 mapping provisions. The mappings contain 81 relationship
legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation and one Draft UK pilot
profile (Draft `0.2.0`) under the reusable profile contract. The PCI DSS
readiness record has the approved `HOLD` disposition, the NIST AI RMF readiness
record has the approved `HOLD` disposition, the ISO/IEC 42001 readiness record
has the approved `HOLD` disposition, the NIST CSF 2.0 readiness record has the
approved `HOLD` disposition, the ISO/IEC 27001:2022 readiness record has the
approved `HOLD` disposition, the NIST SP 800-53 Revision 5 readiness record has
the approved `HOLD` disposition, and the CIS Controls Version 8 readiness
record has the approved `HOLD` disposition. None of those dispositions
establish a mapping, assessment, certification, compliance, equivalence,
endorsement, or legal conclusion.

## Prerequisite dispositions

Harness Phase 2 hosted-timing reconsideration is `DEFER`, recorded in
`docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md`.
ESAF-1300, ESAF-1400, and ESAF-1700 are linked as Working Draft deepen packs at
Working Draft `0.3.0` in `governance/ESAF-1300.md`,
`implementation/ESAF-1400.md`, and `data-model/ESAF-1700.md`. ESAF-1500
remains a Working Draft carry-forward at `assessment/ESAF-1500.md` (Working
Draft `0.1.1`) from the `v0.14-draft` deepen; it is not the milestone deepen
target for `v0.17-draft`. The NIST AI RMF crosswalk readiness decision is
`HOLD`, recorded at `crosswalks/nist-ai-rmf.md`. The ISO/IEC 42001 crosswalk
readiness decision is `HOLD`, recorded at `crosswalks/iso-iec-42001.md`. The
NIST CSF 2.0 crosswalk readiness decision is `HOLD`, recorded at
`crosswalks/nist-csf.md`. The ISO/IEC 27001:2022 crosswalk readiness decision
is `HOLD`, recorded at `crosswalks/iso-iec-27001.md`. The NIST SP 800-53
Revision 5 crosswalk readiness decision is `HOLD`, recorded at
`crosswalks/nist-sp-800-53.md`. The CIS Controls Version 8 crosswalk readiness
decision is `HOLD`, recorded at `crosswalks/cis-controls.md`.

The bounded Phase 6 assessment toolkit third deepen for `v0.17-draft` is
present at:

- `assessment/workbook/README.md` (third deepen marker)

Issues 55 and 60 may remain open; this publication does not require their
closure. Tracker hygiene, CIS Controls Version 8 readiness `HOLD`, and the
Phase 6 third deepen are completed workstreams for this milestone.

## Lifecycle boundary

The current ESAF version is `0.17-draft` for the exact metadata-only closure
candidate. The `v0.17-draft` Working Draft is not yet published. Publication
remains conditional on the remote annotated `v0.17-draft` tag resolving to the
exact validated merged commit. Publication, when completed, is limited to the
repository Working Draft and does not change any artifact lifecycle state.

This record does not advance any Draft artifact, control, architecture
pattern, mapping set, or profile to an approved lifecycle state.

## Nonclaims

This closure-candidate Working Draft package does not claim certification,
compliance, equivalence, endorsement, assurance, or production readiness. It
does not close Issue 55 or Issue 60, and it does not clear the PCI DSS,
HITRUST, NIST AI RMF, ISO/IEC 42001, NIST CSF, ISO/IEC 27001, NIST SP 800-53,
or CIS Controls blockers. While NIST AI RMF, ISO/IEC 42001, NIST CSF,
ISO/IEC 27001, NIST SP 800-53, or CIS Controls readiness remains `HOLD`, this
package does not authorize mapping authorship for those schemes. It does not
author a SOC 2 readiness package.

## Publication evidence

Publication evidence for the closure candidate binds Issue
[#208](https://github.com/tdistress/ESAF/issues/208). Annotated tag identity,
tagged commit, and post-merge validation evidence remain unset until the
published phase.
