# Gate decision record example (informative)

Non-normative worksheet supporting
[ESAF-1300](../../governance/ESAF-1300.md) lifecycle-gate operating detail.
Completing this material does not establish certification, compliance, or
control satisfaction.

This fictional example records a conditional production-readiness gate
decision for capability `CAP-140`. It operationalizes the ESAF-1000 §9.3
record contract without creating a second normative schema.

## Gate decision header

| Field | Fictional entry |
|---|---|
| Gate decision ID | `GATE-SA-2026-014` |
| Capability ID / version | `CAP-140` / `2026.09.1` |
| Gate | Production readiness |
| Decision date | 2026-09-12 |
| Deciding authority | Fictional Summit Analytics AI governance council |
| Disposition | Conditional authorization for limited pilot expansion |

## Required ESAF-1000 §9.3 elements

| Element | Fictional entry |
|---|---|
| Capability and version | `CAP-140` / `2026.09.1` |
| Reviewers | Risk analyst, security architect, data owner, business owner |
| Decision authority | AI governance council chair (fictional) |
| Evidence relied upon | `EVD-ENG2-RSK110-CLASSIFY`, draft result `ASR-ENG2-RSK110`, handling review notes |
| Accepted residual risk | Limited audience expansion with monitoring; dual-review exception `EXC-SA-2026-014` |
| Expiration / next review | 2026-12-12 or upon audience expansion beyond pilot cohort |
| Referenced exception | `EXC-SA-2026-014` (see [governance thread template](../../templates/examples/governance-thread.example.md)) |

## RACI alignment check

| Check | Result |
|---|---|
| Single accountable authority matches RACI production-readiness row | Pass — council chair recorded as deciding authority |
| Security and risk consulted where applicable | Pass — security architect and risk analyst listed as reviewers |
| Open finding blocks unconditional authorization | Pass — draft RSK-110 finding keeps authorization conditional |

## Nonclaims

Names, identifiers, dates, and decisions in this example are fictional. This
worksheet does not replace ESAF-1000 §9.3, GOV controls in ESAF-1100, or an
organization's approved gate records.
