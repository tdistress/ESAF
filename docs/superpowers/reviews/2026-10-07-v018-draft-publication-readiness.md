---
release: v0.18-draft
phase: closure_candidate
tag: v0.18-draft
milestone: v0.18-draft
issue: 224
base_sha: 836659e97a4b7d1deb01f164407f59dd6e240b15
version_advanced: false
deliverable: one_fictional_summit_analytics_cap140_integrated_assessment_case
qualified_crosswalk_review_required: false
publication:
  condition: annotated_tag_targets_validated_closure_candidate
  tag_object: null
  tagged_commit: null
  date: null
  evidence: []
gates:
  scope: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/224]}
  integrated_case: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/224]}
  technical: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/224]}
  editorial: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/224]}
  terminology: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/224]}
  cross_reference_rendering: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/224]}
  standards_mapping: {state: not_applicable, evidence: []}
  repository_validation: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/224]}
  governance: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/224]}
  post_merge: {state: open, evidence: []}
---

# v0.18-draft publication readiness

## Scope

This record governs milestone [v0.18-draft](https://github.com/tdistress/ESAF/milestone/12)
and its publication work tracked by [Issue #224](https://github.com/tdistress/ESAF/issues/224).
The sole deliverable is one fictional Summit Analytics `CAP-140` integrated
assessment case connecting the existing `API-100` and `MOD-100` records. Scope
and gate evidence shall bind to the exact candidate and its base commit.

## Mandatory gates

Scope, integrated-case coherence, technical validation, editorial review,
terminology, cross-reference/rendering, repository validation, governance, and
post-merge validation remain required. The standards-mapping gate is explicitly
`not_applicable`: this milestone changes no mapping artifacts. A qualified
external crosswalk reviewer is not required. That boundary does not waive any
ordinary gate above. All gate evidence shall use durable HTTPS locators when a
gate is ready or closed.

## Lifecycle boundary

The evidence phase is `evidence_candidate`; progression is `evidence_candidate`
to `closure_candidate` to `published`. In the closure-candidate phase, `ready`
means the candidate and evidence package are prepared for exact-SHA review; it
does not claim that technical, editorial, terminology, cross-reference/rendering,
or governance review has already occurred. Those reviews must be completed on
the final exact candidate before merge. Issue #224 is the HTTPS tracker for
those pending reviews and candidate evidence. Publication is recorded only
after the annotated `v0.18-draft` tag exists and all post-merge checks pass.

## Publication evidence

The annotated tag shall target the exact validated closure-candidate commit.
The later published-record commit records the tag object, tagged commit,
publication date, and evidence; it is not required to be the tag target.
Published-to-published maintenance shall preserve immutable tag identity and
closed gate truth. No Draft artifact lifecycle state or standard version is
advanced by this repository Working Draft publication.
