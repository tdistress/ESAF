---
release: 0.4-alpha
phase: closure_candidate
tag: v0.4-alpha
issue: 39
repository_scope: complete_git_tracked_repository
publication:
  date: 2026-07-23
  condition: remote_annotated_tag_matches_exact_validated_commit
mapping_sets:
  - uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0
mapping_decision_basis: owner_risk_acceptance
gates:
  scope: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/39]}
  technical: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/51]}
  editorial: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/main/docs/superpowers/reviews/2026-07-21-v04-alpha-editorial-review.md]}
  cross_reference_rendering: {state: ready, evidence: [https://github.com/tdistress/ESAF/blob/main/docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md]}
  standards_mapping: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/39]}
  release_metadata: {state: ready, evidence: [https://github.com/tdistress/ESAF/pull/51]}
  governance: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/39]}
  post_merge: {state: ready, evidence: [https://github.com/tdistress/ESAF/issues/39]}
---

# 0.4-alpha publication readiness

## Scope

This readiness record covers 91 controls in 16 families, 7 Draft architecture
patterns, and 3 Draft mapping sets. The mapping inventory contains 404
provisions, 81 relationship legs, and 325 negative dispositions.
It applies to the complete Git-tracked ESAF repository, not a selected subset.

## Lifecycle limitations

The mapping sets remain Draft snapshots. This record does not assert assurance,
certification, compliance, equivalence, endorsement, external-scheme approval,
production readiness, or qualified review.

## Evidence ownership

Gate evidence is owned by the responsible reviewers and release governance.
Exact candidate, reviewed, merge, and tag identifiers remain in external
GitHub evidence rather than this tracked record.

## Invalidation

Changes to the candidate, review findings, release scope, or merge state
invalidate the corresponding evidence and require the applicable gate to be
reassessed.

## Current state

The record is a conditional closure candidate. Repository-owner risk acceptance
is the selected Working Draft mapping-decision basis. Qualified mapping review is deferred,
does not complete or qualify that review, and all mapping snapshots remain Draft.
Exact-head technical, editorial, rendering, owner, and separate
Steering Committee evidence remain external and must validate before merge.

The conditional date is not a release assertion. A remote annotated tag may be
created only after post-merge validation confirms that it resolves to the exact
validated merged-main commit.
