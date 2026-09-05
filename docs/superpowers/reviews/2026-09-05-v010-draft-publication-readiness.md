---
release: 0.10-draft
phase: evidence_candidate
tag: v0.10-draft
issue: 119
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

# v0.10-draft publication readiness

## Scope

This evidence-candidate record covers the complete Git-tracked repository. Its
derived inventory contains 91 controls in 16 families, 7 architecture patterns,
3 mapping sets, and 404 mapping provisions. The mappings contain 81
relationship legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation, the Draft Phase 6
assessment-toolkit starters, and one Draft UK pilot profile under the reusable
profile contract. The PCI DSS readiness record has the approved `HOLD`
disposition, and the NIST AI RMF readiness record has the approved `HOLD`
disposition. Neither disposition establishes a mapping, assessment,
certification, compliance, equivalence, endorsement, or legal conclusion.

## Prerequisite dispositions

Harness Phase 2 hosted-timing reconsideration is `DEFER`, recorded in
`docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md`.
ESAF-1300, ESAF-1400, and ESAF-1700 are linked as Working Drafts at
`governance/ESAF-1300.md`, `implementation/ESAF-1400.md`, and
`data-model/ESAF-1700.md`. The NIST AI RMF crosswalk readiness decision is
`HOLD`, recorded at `crosswalks/nist-ai-rmf.md`.

The Phase 6 Draft starters required for `v0.10-draft` are present at:

- `assessment/workbook/README.md`
- `assessment/evidence-catalog/README.md`
- `assessment/audit-checklist/README.md`
- `templates/README.md`

Issues 55 and 60 may remain open; this publication does not require their
closure.

## Lifecycle boundary

The currently published ESAF version remains `0.9-rc1` until a later
closure-candidate and annotated-tag sequence advances Working Draft surfaces to
`0.10-draft`. This evidence-candidate record does not create tag `v0.10-draft`,
does not change `VERSION.md`, and does not advance any Draft artifact lifecycle
state.

## Nonclaims

This evidence-candidate Working Draft package does not claim certification,
compliance, equivalence, endorsement, assurance, or production readiness. It
does not close Issue 55 or Issue 60, and it does not clear the PCI DSS or
HITRUST blockers.

## Publication evidence

No annotated tag or post-merge publication evidence exists yet for
`v0.10-draft`. Issue [#119](https://github.com/tdistress/ESAF/issues/119)
tracks the publication gates. Exact-SHA technical, editorial, and governance
reviews for this evidence candidate are recorded under
`docs/superpowers/reviews/` with the `2026-09-05-v010-draft-` prefix.
