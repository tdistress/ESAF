# Decision Record Example (Draft deepen)

**Status:** Draft deepen example
**Class:** Decision
**Issue:** [#127](https://github.com/tdistress/ESAF/issues/127)
**Informative for:** ESAF-1000 Appendix A architecture decision record;
ESAF-1300 decision rights; ESAF-1400 mapping practice.

This fictional non-normative example records a governed decision to keep human
confirmation before any refund suggestion derived from support summaries. It
does not create new decision rights.

## Decision header

| Field | Entry |
|---|---|
| Decision ID | `ADR-NB-2026-17` |
| Capability ID / version | `CAP-NB-SUPPORT-SUM` / `2026.08.1` |
| Decision domain | Architecture / human-control boundary |
| Date | 2026-08-10 |
| Status (proposed / decided / superseded) | Decided |

## Context and options

| Field | Entry |
|---|---|
| Problem / decision needed | Whether summarization output may auto-populate refund actions |
| Options considered | (A) auto-populate refund draft; (B) summary-only with manual refund entry; (C) block refund language entirely |
| Constraints and assumptions | Support agents remain accountable for refund issuance; no payment API write from the model path |
| Related evidence / risk IDs | `RSK-NB-SUM-2026-08`, `EVD-NB-AGENT-WORKFLOW` |

## Decision

| Field | Entry |
|---|---|
| Chosen option | (B) summary-only with manual refund entry |
| Deciding authority | AI architecture review board (fictional) |
| Required consultees engaged | Support ops, privacy, platform security |
| Rationale | Preserves agent accountability and avoids model-initiated financial side effects |
| Rejected alternatives | (A) too much automation risk; (C) overly restrictive for agent productivity |

## Consequences

| Field | Entry |
|---|---|
| Follow-up actions | Update agent UI to disable auto-fill; add regression Test for refund-action absence |
| Accepted residual risk / conditions | Agents may still misread summaries; mitigated by QA sampling |
| Review or expiry date | 2026-11-10 or on payment-integration change |
| Supersedes / superseded by | Supersedes `ADR-NB-2026-09` draft auto-fill proposal |

## Nonclaims

This Draft deepen fictional example does not establish certification, compliance,
equivalence, endorsement, assurance, or production readiness. Completing it
does not by itself authorize production use or close a lifecycle gate.
