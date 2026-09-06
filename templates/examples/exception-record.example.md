# Exception Record Example (Draft deepen)

**Status:** Draft deepen example
**Class:** Exception
**Issue:** [#127](https://github.com/tdistress/ESAF/issues/127)
**Informative for:** ESAF-1300 exception workflow; GOV-140 field coverage.

This fictional non-normative example records a time-bounded exception for delayed
dual-review coverage on a low-volume support-summarization hotfix path. It does
not replace an authorized exception workflow.

## Request

| Field | Entry |
|---|---|
| Exception ID | `EXC-NB-2026-014` |
| Capability ID / version | `CAP-NB-SUPPORT-SUM` / `2026.08.1` |
| Scope (component, control, or process) | Hotfix prompt edits for locale typo fixes only |
| Justification | Dual reviewers unavailable for a 72-hour holiday window; typos block agent usability |
| Requested duration | 2026-08-29 through 2026-09-01 |
| Accountable owner | Morgan Ellis, fictional platform owner |

## Risk review

| Field | Entry |
|---|---|
| Residual risk | Limited — typo-only edits; no retrieval or tool-policy changes |
| Compensating measures | Single senior reviewer plus automated prompt-diff lint; post-window retrospective |
| Reviewer | Avery Chen, fictional independent risk reviewer |
| Recommendation | Approve with monitoring and forced retrospective |

## Approval

| Field | Entry |
|---|---|
| Approval authority | Northbridge AI governance board chair (fictional) |
| Decision (approve / modify / reject) | Approve |
| Conditions | Locale typo fixes only; no retrieval, tool, or data-handling changes |
| Expiration | 2026-09-01T23:59:59Z |
| Review triggers | Any non-typo change; security alert; customer complaint spike |
| Decision date | 2026-08-28 |

## Monitoring and closure

| Field | Entry |
|---|---|
| Monitoring cadence and owner | Daily diff review by platform on-call |
| Register entry locator | `REG-NB-EXC#014` |
| Remediation commitment | Restore dual-review before 2026-09-02 |
| Closure or renewal decision | Closed after dual-review restored; no renewal |
| Closure date | 2026-09-02 |

## Nonclaims

This Draft deepen fictional example does not establish certification, compliance,
equivalence, endorsement, assurance, or production readiness. An approved
template instance does not waive controls outside the recorded scope and
duration.
