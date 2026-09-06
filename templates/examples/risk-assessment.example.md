# Risk Assessment Example (Draft deepen)

**Status:** Draft deepen example
**Class:** Risk
**Issue:** [#127](https://github.com/tdistress/ESAF/issues/127)
**Informative for:** ESAF-1000 Appendix A AI risk assessment; ESAF-1300 and
ESAF-1400 operating practice.

This fictional non-normative example shows a filled risk-assessment record for
the Northbridge support-summarization intake capability. It does not redefine
ESAF risk tiers or control baselines.

## Record header

| Field | Entry |
|---|---|
| Record ID | `RSK-NB-SUM-2026-08` |
| Capability ID / name | `CAP-NB-SUPPORT-SUM` / Northbridge support summarization |
| Version / release | `2026.08.1` |
| Assessor | Priya Nair, fictional risk lead |
| Date | 2026-08-12 |
| Related inventory / ADR IDs | `INV-NB-AI-042`, `ADR-NB-2026-17` |

## Context

| Field | Entry |
|---|---|
| Purpose and users | Summarize customer-support tickets for internal agents |
| Data classes and sensitivity | Customer ticket text; personal data possible; no payment data |
| Deployment boundary | Production VPC region `us-east-1`; no customer-facing autonomous actions |
| Applicable ESAF tier / baseline | Tier 2 operating baseline for assisted decision support |
| External obligations in scope | Fictional internal privacy schedule only; no external framework claim |

## Inherent risk

| Factor | Rating / note |
|---|---|
| Impact if misused or failed | Moderate — incorrect summaries could mislead agents but not auto-execute refunds |
| Likelihood without treatment | Moderate — prompts and retrieval can drift without review |
| Affected parties | Customers (indirect), support agents, privacy office |
| Inherent-risk summary | Moderate inherent risk concentrated in prompt integrity and data minimization |

## Treatment

| Treatment | Owner | Status | Evidence pointer |
|---|---|---|---|
| Prompt and retrieval change gate with dual review | Platform eng lead | Operating | `EVD-NB-PROMPT-GATE-LOG` |
| Ticket-field redaction before model intake | Data steward | Operating | `EVD-NB-REDACTION-CONFIG` |
| Weekly sample review of summarization quality | Support QA | Operating | `EVD-NB-QA-SAMPLE-2026W32` |

## Residual risk and acceptance

| Field | Entry |
|---|---|
| Residual-risk statement | Residual risk remains limited after redaction and change-gate treatments |
| Acceptance authority | Northbridge AI governance board (fictional) |
| Conditions / expiry | Accept while dual-review gate remains enforced; revisit on model change |
| Monitoring expectations | Weekly QA sample and monthly gate metrics |
| Next review date | 2026-11-12 |

## Nonclaims

This Draft deepen fictional example does not establish certification, compliance,
equivalence, endorsement, assurance, or production readiness. Completing or
copying it does not authorize production use or risk acceptance by itself.
