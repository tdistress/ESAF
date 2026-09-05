---
release: 0.10-draft
phase: closure_candidate
tag: v0.10-draft
issue: 119
repository_scope: complete_git_tracked_repository
publication:
  date: null
  condition: remote_annotated_tag_matches_exact_validated_commit
  evidence:
    - https://github.com/tdistress/ESAF/issues/119
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
  assessment_workbook: draft_starter
  assessment_workbook_path: assessment/workbook/README.md
  evidence_catalog: draft_starter
  evidence_catalog_path: assessment/evidence-catalog/README.md
  audit_checklist: draft_starter
  audit_checklist_path: assessment/audit-checklist/README.md
  governance_templates: draft_starter
  governance_templates_path: templates/README.md
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
  scope: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/112]}
  technical: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/ebdac7d2b1a55e63712d9146162b9bf7fa81ba4d/docs/superpowers/reviews/2026-09-05-v010-draft-technical-review.md]}
  editorial: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/ebdac7d2b1a55e63712d9146162b9bf7fa81ba4d/docs/superpowers/reviews/2026-09-05-v010-draft-editorial-review.md]}
  terminology: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/ebdac7d2b1a55e63712d9146162b9bf7fa81ba4d/docs/superpowers/reviews/2026-09-05-v010-draft-editorial-review.md]}
  cross_reference_rendering: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/112]}
  standards_mapping: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/112]}
  profile_scope: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/112]}
  release_metadata: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/112]}
  governance: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/ebdac7d2b1a55e63712d9146162b9bf7fa81ba4d/docs/superpowers/reviews/2026-09-05-v010-draft-governance-review.md]}
  post_merge: {state: open, evidence: []}
---

# v0.10-draft publication readiness


## Scope

This closure candidate covers the complete Git-tracked repository. Its
derived inventory contains 91 controls in 16 families, 7 architecture
patterns, 3 mapping sets, and 404 mapping provisions. The mappings contain 81
relationship legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation, the Draft Phase 6
assessment-toolkit starters, and one Draft UK pilot profile under the reusable
profile contract. The PCI DSS readiness record has the approved 
disposition, and the NIST AI RMF readiness record has the approved 
disposition. Neither disposition establishes a mapping, assessment,
certification, compliance, equivalence, endorsement, or legal conclusion.

## Prerequisite dispositions

Harness Phase 2 hosted-timing reconsideration is , recorded in
.
ESAF-1300, ESAF-1400, and ESAF-1700 are linked as Working Drafts at
, , and
. The NIST AI RMF crosswalk readiness decision is
, recorded at .

The Phase 6 Draft starters required for  are present at:

- 
- 
- 
- 

Issues 55 and 60 may remain open; this candidate does not require their
closure.

## Lifecycle boundary

The current ESAF version is . The non-post-merge v0.10 gates are
, the post-merge gate is xdg-open - opens a file or URL in the user's preferred application

Synopsis

xdg-open { file | URL }

xdg-open { --help | --manual | --version }

Use 'man xdg-open' or 'xdg-open --manual' for additional info., and the  tag has not been
created. The  release status is Working Draft. This closure
candidate does not approve publication.

This record does not advance any Draft artifact, control, architecture
pattern, mapping set, or profile to an approved lifecycle state.

## Nonclaims

This closure candidate does not claim certification, compliance,
equivalence, endorsement, assurance, or production readiness. It does not
close Issue 55 or Issue 60, and it does not clear the PCI DSS or HITRUST
blockers. It does not approve publication.

## Publication evidence

Publication remains conditional on the remote annotated  tag
resolving to the exact validated merged commit. The tag has not been
created. The publication Sat Sep  5 04:13:10 PM UTC 2026, , , and
 fields remain  until after merge to  and
creation of the annotated tag on the exact validated merged commit. Issue
[#119](https://github.com/tdistress/ESAF/issues/119) tracks the publication
gates.
