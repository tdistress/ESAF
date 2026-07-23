---
release: 0.4-alpha
phase: evidence_candidate
tag: v0.4-alpha
issue: 39
repository_scope: complete_git_tracked_repository
publication:
  date: null
  condition: remote_annotated_tag_matches_exact_validated_commit
mapping_sets:
  - uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0
gates:
  scope: {state: in_review, evidence: []}
  technical: {state: in_review, evidence: []}
  editorial: {state: in_review, evidence: []}
  cross_reference_rendering: {state: in_review, evidence: []}
  standards_mapping: {state: open, evidence: []}
  release_metadata: {state: in_review, evidence: []}
  governance: {state: open, evidence: []}
  post_merge: {state: open, evidence: []}
---

# 0.4-alpha publication readiness

## Scope

This readiness record covers 91 controls in 16 families, 7 Draft architecture
patterns, and 3 Draft mapping sets. The mapping inventory contains 404
provisions, 81 relationship legs, and 325 negative dispositions.
It applies to the complete Git-tracked ESAF repository, not a selected subset.

## Lifecycle limitations

The mapping sets remain Draft snapshots. This record does not assert
certification, compliance, equivalence, endorsement, or publication.

## Evidence ownership

Gate evidence is owned by the responsible reviewers and release governance.
Exact candidate, reviewed, merge, and tag identifiers remain in external
GitHub evidence rather than this tracked record.

## Invalidation

Changes to the candidate, review findings, release scope, or merge state
invalidate the corresponding evidence and require the applicable gate to be
reassessed.

## Current state

The record is an evidence candidate. It remains open until every required gate
is ready or closed and independently evidenced for a closure candidate.

Candidate-content technical, editorial, and rendering reviews are complete.
Their gates remain `in_review` until exact-head external evidence is bound to a
closure candidate. Qualified mapping, authorized scope, governance, post-merge,
publication, and tag conditions remain outstanding.
