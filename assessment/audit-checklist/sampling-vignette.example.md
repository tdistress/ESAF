# ESAF-1500 Audit Checklist Sampling Vignette

**Status:** Draft deepen example
**Issue:** [#126](https://github.com/tdistress/ESAF/issues/126)
**Authority:** [ESAF-1500](../ESAF-1500.md) assessment-result contract;
[ESAF-1100](../../controls/ESAF-1100.md) assessment procedures.

This fictional Draft deepen example fills the audit-checklist tables for a small
two-control sampling engagement. It does not assess a real organization and
does not establish certification, compliance, equivalence, endorsement, or
assurance.

## Engagement header

| Field | Operator entry |
|---|---|
| Engagement identifier | `ENG-SAMP-NORTHBRIDGE-2026Q2` |
| Assessed subject / capability | Fictional Northbridge AI intake and model-gateway controls |
| In-scope requirement IDs | `GOV-100`, `SYS-220` |
| Boundary and exclusions | Production AI intake for customer-support summarization; training-pipeline controls excluded |
| Assessment period | 2026-05-01 through 2026-07-31 |
| Assessor / independence | Contour Assurance LLP fictional assessor; no operational ownership |

## Sampling intent

| Checkpoint | Complete? | Notes |
|---|---|---|
| Population of controls, capabilities, or artifacts is defined | [x] | Population is the fictional production AI intake control set (`GOV-*` and `SYS-*` controls assigned to the support-summarization capability). |
| Sample size and selection rationale are recorded | [x] | Sample of two controls: `GOV-100` (authority) and `SYS-220` (gateway allowlist). Selected for highest intake risk concentration. |
| Exclusions and non-sampled items are explicit | [x] | Training-data retention and vendor-risk controls remain out of sample for this vignette. |
| Sampling approach matches engagement risk and purpose | [x] | Risk-based judgmental sample for a Draft deepen demonstration; not a statistical sample. |

## Procedure references

| Requirement ID | Procedure ID(s) | Method(s) | Object / population | Work performed | Complete? |
|---|---|---|---|---|---|
| `GOV-100` | `GOV-100-A1`, `GOV-100-A2` | `Examine`, `Interview` | Approved AI governance charter and governance-owner interview | Examined charter package `EVD-SAMP-GOV100-CHARTER`; interviewed fictional governance owner | [x] |
| `SYS-220` | `SYS-220-T1` | `Test`, `Examine` | Model-gateway allowlist enforcement for blocked model IDs | Executed harness run `EVD-SAMP-SYS220-ALLOWLIST`; examined export metadata | [x] |

## Evidence pointers

| Evidence ID | Type | Requirement ID(s) | Sufficiency | Limitations noted? | Complete? |
|---|---|---|---|---|---|
| `EVD-SAMP-GOV100-CHARTER` | `policy` / `record` package | `GOV-100` | limited | [x] | [x] |
| `EVD-SAMP-GOV100-INTERVIEW` | `interview` | `GOV-100` | limited | [x] | [x] |
| `EVD-SAMP-SYS220-ALLOWLIST` | `technical_test` | `SYS-220` | limited | [x] | [x] |

## Determination capture

| Result ID | Requirement ID(s) | Determination | Design effectiveness | Operating effectiveness | Rationale summary | Status (`draft`/`final`) | Complete? |
|---|---|---|---|---|---|---|---|
| `ASR-SAMP-GOV100` | `GOV-100` | `partially_satisfied` | `effective` | `partially_effective` | Charter exists and is approved, but escalation evidence for exceptions remains incomplete in this fictional sample. | `draft` | [x] |
| `ASR-SAMP-SYS220` | `SYS-220` | `satisfied` | `effective` | `effective` | Allowlist Test blocked the sampled forbidden model IDs and permitted the control case in the fictional harness. | `draft` | [x] |

Filled Draft assessment-result records:

- [`examples/sampling-gov100-assessment-result.example.json`](examples/sampling-gov100-assessment-result.example.json)
- [`examples/sampling-sys220-assessment-result.example.json`](examples/sampling-sys220-assessment-result.example.json)

## Limitation notes

| Limitation | Impact on determination | Residual action | Complete? |
|---|---|---|---|
| Interview answers for `GOV-100` were not corroborated against exception tickets | Keeps `GOV-100` at `partially_satisfied` / `draft` | Request exception-ticket extract before any finalization | [x] |
| `SYS-220` harness is labeled production-like, not live production | Limits external reuse of the `satisfied` determination | Re-run against the production gateway or accept as Draft-only | [x] |
| Sample covers two controls only | No portfolio-level conclusion is supportable | Expand sample before any broader claim | [x] |

## Nonclaims

This Draft deepen vignette is fictional. Completing or copying these tables does
not establish certification, compliance, equivalence, endorsement, assurance,
production readiness, or lifecycle approval for any Draft ESAF artifact.
