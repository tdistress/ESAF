---
release: 0.4-alpha
phase: published
tag: v0.4-alpha
issue: 39
repository_scope: complete_git_tracked_repository
publication:
  date: 2026-07-23
  condition: remote_annotated_tag_matches_exact_validated_commit
  tag_object: 2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f
  tagged_commit: 8abfe5a85db19d11295a0c3debeb2d58109b0ca7
  evidence: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764
mapping_sets:
  - uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0
mapping_decision_basis: owner_risk_acceptance
gates:
  scope: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/39, https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764]}
  technical: {state: closed, evidence: [https://github.com/tdistress/ESAF/pull/51, https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764]}
  editorial: {state: closed, evidence: [https://github.com/tdistress/ESAF/blob/main/docs/superpowers/reviews/2026-07-21-v04-alpha-editorial-review.md, https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764]}
  cross_reference_rendering: {state: closed, evidence: [https://github.com/tdistress/ESAF/blob/main/docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md, https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764]}
  standards_mapping: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/39, https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764]}
  release_metadata: {state: closed, evidence: [https://github.com/tdistress/ESAF/pull/51, https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764]}
  governance: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/39, https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764]}
  post_merge: {state: closed, evidence: [https://github.com/tdistress/ESAF/issues/39, https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764]}
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
The fixed annotated-tag object, peeled merged-main commit, and final issue
evidence are recorded in this durable publication record.

## Invalidation

This closed evidence applies only to the recorded v0.4-alpha tag object and
peeled commit. Changes for a later release require their own evidence and gate
assessment.

## Current state

The v0.4-alpha Working Draft was published through the remote annotated tag
v0.4-alpha. The tag condition was satisfied on 2026-07-23 and the tag peels to
the exact validated merged-main commit recorded in front matter.

Repository-owner risk acceptance is the selected Working Draft mapping-decision
basis. Qualified mapping review is deferred, does not complete or qualify that
review, and all mapping snapshots remain Draft. The separate Steering Committee
approval was recorded as an independently closed governance gate.
