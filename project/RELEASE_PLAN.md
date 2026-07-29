# Release Plan

Each release shall complete the following gates:

1. Scope and milestone approved.
2. Normative and technical review completed.
3. Editorial conventions and terminology validated.
4. Internal links and cross-references validated.
5. Required standards mappings use exactly one uniform mapping decision basis: `qualified_approval` or `owner_risk_acceptance`.
6. Changelog and version metadata updated.
7. Release approved under `GOVERNANCE.md`.

## v0.5-beta deferred mapping assurance

The `v0.5-beta` mapping-assurance gate shall use either completed qualified
approval or one coordinated owner-risk decision bound to the exact
`v0.5-beta` release candidate. The owner-risk path shall cover each of these
mapping sets exactly once:

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`

The coordinated evidence shall use
`mapping_decision_basis: owner_risk_acceptance`,
`decision_type: owner_risk_acceptance`, and
`qualified_review_status: deferred`. Every mapping decision shall use one
uniform basis and one authenticated owner source, identify the missing
qualified human evidence, preserve the required nonclaims, and bind to the
exact candidate SHA.

`DEFERRED` is a milestone assurance disposition, not an ESAF-1600 mapping
lifecycle state. All three mapping sets and their records remain Draft. No
reviewer metadata, lifecycle event, approval state, or publication state is
added. Issue 55 remains open for the six qualified human role dispositions.
Issue 59 may proceed under validated deferred evidence, but every other
technical, editorial, mapping, governance, validation, merge, and post-merge
release gate remains required.

Owner-risk acceptance defers qualified review; it does not complete or qualify
that review. It does not establish qualified review, approval, assurance,
compliance, certification, equivalence, endorsement, external-scheme approval,
or production readiness. Historical `v0.4-alpha` evidence cannot approve
`v0.5-beta`.

## 0.5-beta closure candidate

The exact metadata-only closure candidate sets every non-post-merge gate to
Ready and leaves the post-merge gate Open. It does not record owner-risk,
scope, or Steering Committee approval and does not approve publication.

Publication remains conditional on the remote annotated `v0.5-beta` tag
resolving to the exact validated merged commit. The tag has not been created.
Exact-head reviews, non-delegable decisions, successful checks, clean merge
state, merged-main validation, and remote tag verification remain required.

## 0.4-alpha publication

Publication gates are Closed.

The v0.4-alpha Working Draft was published through annotated tag `v0.4-alpha`
on 2026-07-23. The tag object is
`2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f` and its peeled commit is
`8abfe5a85db19d11295a0c3debeb2d58109b0ca7`. Issue
[#39](https://github.com/tdistress/ESAF/issues/39) records the publication
evidence at https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764.

Architecture content and all mapping sets remain Draft. The uniform Working
Draft mapping decision basis is `owner_risk_acceptance`. Owner risk acceptance
defers qualified review; it does not complete or qualify that review.
The closed evidence records that every Mermaid diagram was rendered and reviewed. It does
not represent qualified review by qualified contributors. Steering Committee governance approval remains a separate gate and was recorded independently of
the repository-owner risk decision.

| Gate | Current state | Final evidence |
|---|---|---|
| Scope and milestone approval | Closed | Owner mapping and scope decision: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764 |
| Normative and technical review | Closed | Technical verdict and validation evidence: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764 |
| Editorial and terminology review | Closed | Editorial review evidence: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764 |
| Cross-reference and rendering review | Closed | Mermaid rendering evidence: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764 |
| Standards mapping review | Closed | Owner-risk Working Draft basis; qualified review remains deferred: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764 |
| Release metadata synchronization | Closed | Published metadata and annotated-tag evidence: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764 |
| Governance approval | Closed | Separate Steering Committee approval: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764 |
| Post-merge validation | Closed | Validated merged-main commit and tag resolution: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764 |

Structural validators do not replace renderer, mapping-decision, or governance
evidence. Owner risk acceptance is a Working Draft publication basis, not a
qualified mapping review or external-scheme approval. It makes no assurance,
compliance, certification, equivalence, endorsement, or production-readiness
claim.

This evidence closes only `v0.4-alpha` and cannot approve a later release.
