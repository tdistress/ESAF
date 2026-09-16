# ESAF-1500 Audit Checklist Sampling Vignette 3

**Status:** Draft deepen example
**Issue:** [#207](https://github.com/tdistress/ESAF/issues/207)
**Authority:** [ESAF-1500](../ESAF-1500.md) assessment-result contract;
[ESAF-1100](../../controls/ESAF-1100.md) assessment procedures.

This fictional third Draft deepen example fills the audit-checklist tables for
a gateway-and-model sampling engagement on non-GOV controls. It does not assess
a real organization and does not establish certification, compliance,
equivalence, endorsement, or assurance.

## Engagement header

| Field | Operator entry |
|---|---|
| Engagement identifier | `ENG-SAMP3-SUMMIT-2026Q3` |
| Assessed subject / capability | Fictional Summit Analytics workforce-research assistant (`CAP-140`) |
| In-scope requirement IDs | `API-100`, `MOD-100` |
| Boundary and exclusions | Production gateway and model-registry path; vendor contracts and model-validation depth excluded |
| Assessment period | 2026-09-01 through 2026-09-15 |
| Assessor / independence | Contour Assurance LLP fictional assessor; no operational ownership |

## Sampling intent

| Checkpoint | Complete? | Notes |
|---|---|---|
| Population of controls, capabilities, or artifacts is defined | [x] | Population is the fictional CAP-140 gateway and model-control set (`API-*` and `MOD-*` controls assigned to the capability). |
| Sample size and selection rationale are recorded | [x] | Sample of two controls: `API-100` (gateway) and `MOD-100` (model registry). Selected for highest production-path concentration. |
| Exclusions and non-sampled items are explicit | [x] | Vendor contracts (`API-140`) and model-validation depth (`MOD-120`) remain out of sample for this vignette. |
| Sampling approach matches engagement risk and purpose | [x] | Risk-based judgmental sample for a third Draft deepen demonstration; not a statistical sample. |

## Procedure references

| Requirement ID | Procedure ID(s) | Method(s) | Object / population | Work performed | Complete? |
|---|---|---|---|---|---|
| `API-100` | `API-100-A1`, `API-100-A2` | `Examine`, `Test` | CAP-140 gateway configuration and staging bypass harness | Examined export `EVD-SAMP3-API100-GATEWAY`; executed one fictional bypass attempt | [x] |
| `MOD-100` | `MOD-100-A1`, `MOD-100-A2`, `MOD-100-A3` | `Examine`, `Test`, `Interview` | CAP-140 model registry record and deployed alias | Examined registry `EVD-SAMP3-MOD100-REGISTRY`; reconciled deployed hash; interviewed model owner | [x] |

## Evidence pointers

| Evidence ID | Type | Requirement ID(s) | Sufficiency | Limitations noted? | Complete? |
|---|---|---|---|---|---|
| `EVD-SAMP3-API100-GATEWAY` | `configuration` | `API-100` | limited | [x] | [x] |
| `EVD-SAMP3-MOD100-REGISTRY` | `record` | `MOD-100` | limited | [x] | [x] |

## Determination capture

| Result ID | Requirement ID(s) | Determination | Design effectiveness | Operating effectiveness | Rationale summary | Status (`draft`/`final`) | Complete? |
|---|---|---|---|---|---|---|---|
| `ASR-SAMP3-API100` | `API-100` | `partially_satisfied` | `effective` | `partially_effective` | Gateway routes CAP-140 through approved control points and blocked the sampled bypass, but emergency-restriction exercise evidence remains incomplete in this fictional sample. | `draft` | [x] |
| `ASR-SAMP3-MOD100` | `MOD-100` | `satisfied` | `effective` | `effective` | Registry record was complete and approved; deployed identifier matched; owner confirmed update triggers. | `draft` | [x] |

Filled Draft assessment-result records:

- [`examples/sampling3-api100-assessment-result.example.json`](examples/sampling3-api100-assessment-result.example.json)
- [`examples/sampling3-mod100-assessment-result.example.json`](examples/sampling3-mod100-assessment-result.example.json)

Earlier sampling vignettes remain at
[sampling-vignette.example.md](sampling-vignette.example.md) (`GOV-100`,
`SYS-220`) and [sampling2-vignette.example.md](sampling2-vignette.example.md)
(`RSK-110`, `DAT-110`).

## Limitation notes

| Limitation | Impact on determination | Residual action | Complete? |
|---|---|---|---|
| Bypass Test for `API-100` used a staging harness | Limits external reuse of operating-effectiveness conclusions | Re-run against production or accept as Draft-only | [x] |
| Registry reconciliation covered one fictional model alias | Limits generalization beyond CAP-140 | Expand sample before any portfolio-level claim | [x] |
| Sample covers two controls only | No capability-wide conclusion is supportable | Expand sample before any broader claim | [x] |

## Nonclaims

This Draft deepen vignette is fictional. Completing or copying these tables does
not establish certification, compliance, equivalence, endorsement, assurance,
production readiness, or lifecycle approval for any Draft ESAF artifact.
