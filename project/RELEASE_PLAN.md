# Release Plan

Each release shall complete the following gates:

1. Scope and milestone approved.
2. Normative and technical review completed.
3. Editorial conventions and terminology validated.
4. Internal links and cross-references validated.
5. Required standards mappings use exactly one uniform mapping decision basis: `qualified_approval` or `owner_risk_acceptance`.
6. Changelog and version metadata updated.
7. Release approved under `GOVERNANCE.md`.

## 0.4-alpha readiness

Architecture content is complete only at Draft level. Publication gates remain Open.
For this conditional closure candidate, all eight tracked readiness entries are
Ready, while the release gates remain open until exact-head external evidence,
post-merge validation, and the conditional tag rule are satisfied. The closure
evidence shall confirm that every Mermaid diagram was rendered and reviewed and
that `qualified_approval`, when selected, is completed by qualified contributors.
Owner risk acceptance defers qualified review; it does not complete or qualify that review.

Pre-merge evidence shall be tied to the exact reviewed PR-head/candidate SHA. Post-merge evidence shall be tied to the exact resulting merged-main SHA; these are successive repository states and are not required to have the same SHA.

| Gate | Current state | Required closure evidence |
|---|---|---|
| Scope and milestone approval | Ready | Owner mapping/scope decision on the exact closure candidate: https://github.com/tdistress/ESAF/issues/39 |
| Normative and technical review | Ready | Exact-head technical verdict and validation evidence: https://github.com/tdistress/ESAF/pull/51 |
| Editorial and terminology review | Ready | Exact-head editorial review evidence: https://github.com/tdistress/ESAF/blob/main/docs/superpowers/reviews/2026-07-21-v04-alpha-editorial-review.md |
| Cross-reference and rendering review | Ready | Exact-head 23-block Mermaid inventory and rendering review: https://github.com/tdistress/ESAF/blob/main/docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md |
| Standards mapping review | Ready | `owner_risk_acceptance` is the one uniform Working Draft basis; qualified mapping review is deferred, does not complete or qualify that review, and all mapping snapshots remain Draft: https://github.com/tdistress/ESAF/issues/39 |
| Release metadata synchronization | Ready | Conditional closure metadata and exact-head review record: https://github.com/tdistress/ESAF/pull/51 |
| Governance approval | Ready | Separate Steering Committee approval, successful checks, and clean merge state will be bound to the exact closure candidate: https://github.com/tdistress/ESAF/issues/39 |
| Post-merge validation | Ready | Post-merge validation remains a condition of the remote annotated tag: https://github.com/tdistress/ESAF/issues/39 |

Structural validators do not replace renderer, mapping-decision, or governance evidence. Steering Committee governance approval remains a separate gate and repository-owner risk acceptance does not supply it.

Owner risk acceptance is a conditional Working Draft publication basis, not a
qualified mapping review or external-scheme approval. It makes no assurance,
compliance, certification, equivalence, endorsement, or production-readiness
claim. Until every applicable pre-merge gate is externally evidenced on the
exact reviewed candidate SHA and post-merge validation passes on the exact
resulting merged-main SHA, 0.4-alpha shall not be tagged or represented as
released.

Until that condition is met, 0.4-alpha shall not be tagged or represented as released.
