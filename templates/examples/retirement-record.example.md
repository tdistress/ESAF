# Retirement Record Example (Draft deepen)

**Status:** Draft deepen example
**Class:** Retirement
**Issue:** [#127](https://github.com/tdistress/ESAF/issues/127)
**Informative for:** ESAF-1000 Appendix A retirement record; ESAF-1300
retirement gate; ESAF-1400 optimize-phase retirement practice.

This fictional non-normative example records retirement of the legacy
`support-summarizer-v1` endpoint after cutover to `2026.08.1`. It does not
redefine retirement-gate evidence requirements.

## Retirement header

| Field | Entry |
|---|---|
| Retirement record ID | `RET-NB-SUM-V1-2026` |
| Capability ID / version | `CAP-NB-SUPPORT-SUM` / `support-summarizer-v1` |
| Retirement trigger | Cutover complete; v1 error budget exhausted and unsupported |
| Decision authority | AI lifecycle board (fictional) |
| Planned retirement date | 2026-08-15 |
| Actual retirement date | 2026-08-15 |

## Scope of retirement

| Field | Entry |
|---|---|
| Systems / models / endpoints removed | `https://ai.northbridge.example/summarizer/v1` and model alias `sum-v1` |
| Data stores and retention disposition | Prompt caches purged; ticket mirrors retained per privacy schedule |
| Access and credentials revoked | Service account `sa-sum-v1` and gateway route revoked |
| Dependent capabilities impacted | None after cutover verification |
| External notices completed | Internal support ops bulletin 2026-08-14 |

## Verification

| Checkpoint | Complete? | Evidence pointer |
|---|---|---|
| Traffic or invocation stopped | [x] | `EVD-NB-SUM-V1-TRAFFIC-ZERO` |
| Secrets and keys revoked | [x] | `EVD-NB-SUM-V1-KEY-REVOKE` |
| Data deleted, archived, or retained per authority | [x] | `EVD-NB-SUM-V1-DATA-DISPOSITION` |
| Inventory and AIBOM updated | [x] | `INV-NB-AI-042` revision 18 |
| Monitoring and support runbooks closed | [x] | `RUN-NB-SUM-V1` archived |
| Residual risk after retirement accepted or closed | [x] | Lifecycle board minutes 2026-08-15 |

## Post-retirement

| Field | Entry |
|---|---|
| Lessons learned | Keep dual-run metrics for a full week before endpoint removal |
| Records retention locator | `REC-NB-RETIRE/2026/SUM-V1` |
| Follow-up owner | Platform reliability lead |

## Nonclaims

This Draft deepen fictional example does not establish certification, compliance,
equivalence, endorsement, assurance, or production readiness. Completing it
does not by itself prove secure decommissioning or regulatory disposal.
