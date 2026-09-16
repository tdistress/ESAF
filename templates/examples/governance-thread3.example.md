# Governance Thread Example 3 (Draft deepen)

**Status:** Draft deepen example
**Issue:** [#207](https://github.com/tdistress/ESAF/issues/207)
**Informative for:** ESAF-1300 lifecycle gates and retirement; ESAF-1400
evidence handoff.

This fictional third cross-template thread links a risk entry and a related
retirement path for the same fictional capability family, with an assessment
workbook handoff. It is informative only and does not establish certification,
compliance, equivalence, endorsement, assurance, or production readiness.

## Scenario

Fictional Summit Analytics is closing the legacy prompt-routing sidecar that
preceded the CAP-140 gateway cutover. The risk register records residual
exposure during dual-run, while retirement verification waits on gateway
evidence captured in the third workbook vignette.

## Thread map

| Step | Template | Fictional record | Linked control / gate |
|---|---|---|---|
| 1 | [Risk assessment](risk-assessment.example.md) | `RSK-SA-2026-041` dual-run routing residual risk | ESAF-1000 §9 risk treatment; RSK family practice |
| 2 | [Retirement record](retirement-record.example.md) | `RET-SA-2026-041` legacy sidecar retirement | ESAF-1300 retirement gate; OPS-150 |
| 3 | Workbook evidence (informative) | `EVD-ENG3-API100-GATEWAY` gateway configuration | API-100 evidence cited in retirement verification |

## Risk assessment excerpt

| Field | Entry |
|---|---|
| Risk ID | `RSK-SA-2026-041` |
| Capability ID / version | `CAP-140` / `2026.09.2` |
| Risk statement | Dual-run legacy sidecar may accept unapproved direct provider calls during cutover |
| Inherent rating | Medium |
| Treatment | Retire sidecar after gateway allowlist verification |
| Linked evidence | `EVD-ENG3-API100-GATEWAY`, draft workbook result `ASR-ENG3-API100` |
| Review date | 2026-09-20 |

See the filled [risk-assessment.example.md](risk-assessment.example.md) for
field coverage on a separate fictional risk entry.

## Retirement record excerpt

| Field | Entry |
|---|---|
| Retirement ID | `RET-SA-2026-041` |
| Capability ID / version | `CAP-140-SIDECAR` / `legacy-route-v1` |
| Retirement trigger | Gateway cutover complete; dual-run window expired |
| Linked risk | `RSK-SA-2026-041` |
| Verification evidence | `EVD-ENG3-API100-GATEWAY` traffic-zero and route-revoke checks |
| Planned retirement date | 2026-09-22 |

See the filled [retirement-record.example.md](retirement-record.example.md) for
the complete fictional retirement lifecycle on a related summarizer path.

## Evidence handoff note

Implementation teams should capture gateway configuration and routing evidence
close to retirement verification, using ESAF-1500 identifier patterns such as
`EVD-ENG3-API100-GATEWAY`. The third workbook vignette at
[`assessment/workbook/engagement3-vignette.example.md`](../../assessment/workbook/engagement3-vignette.example.md)
shows how assessors record such evidence without treating draft results as
final determinations.

The second cross-template thread remains at
[governance-thread.example.md](governance-thread.example.md).

## Nonclaims

Names, identifiers, dates, and decisions in this thread are fictional.
Completing or copying these materials does not advance Draft ESAF artifacts to
an approved lifecycle state and does not replace ESAF-1300, ESAF-1400, ESAF-1500,
or an organization's approved records.
