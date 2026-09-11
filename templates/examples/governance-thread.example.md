# Governance Thread Example (Draft deepen)

**Status:** Draft deepen example
**Issue:** [#183](https://github.com/tdistress/ESAF/issues/183)
**Informative for:** ESAF-1300 lifecycle gates and exceptions; ESAF-1400 evidence handoff.

This fictional cross-template thread links a gate decision and a related
exception for the same fictional capability. It is informative only and does
not establish certification, compliance, equivalence, endorsement, assurance,
or production readiness.

## Scenario

Fictional Summit Analytics is preparing `CAP-140` (workforce-research assistant)
for a limited pilot expansion. The governance council records a conditional
production-readiness decision while a time-bounded exception covers delayed
dual-review on prompt edits.

## Thread map

| Step | Template | Fictional record | Linked control / gate |
|---|---|---|---|
| 1 | [Decision record](decision-record.example.md) | `DEC-SA-2026-014` conditional production authorization | ESAF-1000 §9.3 production-readiness gate |
| 2 | [Exception record](exception-record.example.md) | `EXC-SA-2026-014` dual-review coverage gap | GOV-140 exception governance |
| 3 | Workbook evidence (informative) | `EVD-ENG2-RSK110-CLASSIFY` classification record | RSK-110 evidence cited in gate package |

## Decision record excerpt

| Field | Entry |
|---|---|
| Decision ID | `DEC-SA-2026-014` |
| Capability ID / version | `CAP-140` / `2026.09.1` |
| Gate | Production readiness (conditional) |
| Decision authority | Fictional AI governance council |
| Disposition | Authorize limited pilot expansion with monitoring conditions |
| Referenced exception | `EXC-SA-2026-014` |
| Referenced evidence | `EVD-ENG2-RSK110-CLASSIFY`, draft workbook result `ASR-ENG2-RSK110` |
| Decision date | 2026-09-12 |

See the filled [decision-record.example.md](decision-record.example.md) for
field coverage on a separate fictional decision.

## Exception record excerpt

| Field | Entry |
|---|---|
| Exception ID | `EXC-SA-2026-014` |
| Capability ID / version | `CAP-140` / `2026.09.1` |
| Scope | Prompt-edit dual-review coverage during holiday window |
| Linked gate decision | `DEC-SA-2026-014` |
| Expiration | 2026-09-20T23:59:59Z |

See the filled [exception-record.example.md](exception-record.example.md) for
the complete fictional exception lifecycle on a related hotfix path.

## Evidence handoff note

Implementation teams should capture classification and handling evidence close
to the gate decision, using ESAF-1500 identifier patterns such as
`EVD-ENG2-RSK110-CLASSIFY`. The second workbook vignette at
[`assessment/workbook/engagement2-vignette.example.md`](../../assessment/workbook/engagement2-vignette.example.md)
shows how assessors record such evidence without treating draft results as
final determinations.

## Nonclaims

Names, identifiers, dates, and decisions in this thread are fictional.
Completing or copying these materials does not advance Draft ESAF artifacts to
an approved lifecycle state and does not replace ESAF-1300, ESAF-1400, ESAF-1500,
or an organization's approved records.
