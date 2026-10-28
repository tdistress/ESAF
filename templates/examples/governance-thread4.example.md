# Governance Thread Example 4 (Draft deepen)

**Status:** Draft deepen example
**Informative for:** ESAF-1000 Appendix A risk treatment; ESAF-1300 governance follow-up; ESAF-1400 evidence handoff.

This fictional thread links an inconclusive assessment follow-up to a risk
review and a bounded next action. The risk review does not close or accept the
assessment finding, and it does not change either historical assessment result.
No production-use decision is made.

## Scenario

During one fictional CAP-140 staging exercise, the harness did not retain a
complete event trail for the API-100-A3 emergency restriction. The assessor
could not determine whether the expected event and subsequent restricted state
were both observed. The separate Draft result remains `not_assessed`, and its
finding stays open. This record flow is described in the
[integrated assessment overview](../../assessment/integrated-assessment.example.md)
and the [inconclusive follow-up narrative](../../assessment/follow-up/api100-inconclusive-follow-up.example.md).

## Thread map

| Step | Record | Fictional entry | Relationship |
|---|---|---|---|
| 1 | Evidence | `EVD-ENG5-API100-RESTRICTION` | Partial event trail from one staging exercise |
| 2 | Assessment | `ASR-ENG5-API100-A3-INCONCLUSIVE` | Draft `not_assessed` result; finding `FND-ENG5-API100-A3-INCONCLUSIVE` remains open |
| 3 | Risk review | `RSK-SA-2026-052` | Records unresolved exposure and next evidence-capture action |

## Risk review excerpt

| Field | Entry |
|---|---|
| Risk ID | `RSK-SA-2026-052` |
| Capability ID / version | `CAP-140` / `2026.09.2` |
| Risk statement | Incomplete staging event retention prevents a determination about the tested emergency-restriction path; this sample does not establish that a request was allowed or blocked. |
| Inherent rating | Medium, fictional and provisional pending complete evidence |
| Treatment | Update the staging harness to retain correlated request, restriction, and event records; repeat the bounded API-100-A3 exercise and request independent review of the complete record. |
| Owner | Jordan Hale, fictional AI platform engineer |
| Status | Planned; no treatment-completion evidence exists in this example |
| Linked assessment | `ASR-ENG5-API100-A3-INCONCLUSIVE`; open finding `FND-ENG5-API100-A3-INCONCLUSIVE` |
| Residual-risk statement | The evidence gap remains open until a complete record supports a separately documented follow-up assessment. |
| Acceptance authority | None recorded; this example does not accept the risk. |
| Next review trigger | Review after the harness update and independent examination of a complete staging event trail, or sooner if a related staging event cannot be reconstructed. |

Risk review tracks the exposure and treatment decision. It does not determine
whether API-100 is satisfied, resolve the open finding, revise
`ASR-ENG3-API100` or `ASR-ENG4-API100-A3`, or authorize production use. Any
future assessment result would be a separate record using the existing
ESAF-1500 contract.

## Nonclaims

All people, organizations, identifiers, evidence, dates, ratings, and actions
are fictional. The example remains Draft and does not establish certification,
compliance, equivalence, endorsement, assurance, production readiness, or
lifecycle approval. A risk review is not a formal risk acceptance.
