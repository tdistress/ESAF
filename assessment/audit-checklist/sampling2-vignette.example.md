# ESAF-1500 Audit Checklist Sampling Vignette 2

**Status:** Draft deepen example
**Issue:** [#183](https://github.com/tdistress/ESAF/issues/183)
**Authority:** [ESAF-1500](../ESAF-1500.md) assessment-result contract;
[ESAF-1100](../../controls/ESAF-1100.md) assessment procedures.

This fictional second Draft deepen example fills the audit-checklist tables for
a risk-and-data sampling engagement on non-GOV controls. It does not assess a
real organization and does not establish certification, compliance, equivalence,
endorsement, or assurance.

## Engagement header

| Field | Operator entry |
|---|---|
| Engagement identifier | `ENG-SAMP2-SUMMIT-2026Q3` |
| Assessed subject / capability | Fictional Summit Analytics workforce-research assistant (`CAP-140`) |
| In-scope requirement IDs | `RSK-110`, `DAT-110` |
| Boundary and exclusions | Production research-assistant data path; vendor contracts excluded |
| Assessment period | 2026-06-01 through 2026-08-31 |
| Assessor / independence | Contour Assurance LLP fictional assessor; no operational ownership |

## Sampling intent

| Checkpoint | Complete? | Notes |
|---|---|---|
| Population of controls, capabilities, or artifacts is defined | [x] | Population is the fictional CAP-140 risk and data-handling control set (`RSK-*` and `DAT-*` controls assigned to the capability). |
| Sample size and selection rationale are recorded | [x] | Sample of two controls: `RSK-110` (classification) and `DAT-110` (data handling). Selected for highest data-exposure concentration. |
| Exclusions and non-sampled items are explicit | [x] | Supplier contracts and embedding-store controls remain out of sample for this vignette. |
| Sampling approach matches engagement risk and purpose | [x] | Risk-based judgmental sample for a second Draft deepen demonstration; not a statistical sample. |

## Procedure references

| Requirement ID | Procedure ID(s) | Method(s) | Object / population | Work performed | Complete? |
|---|---|---|---|---|---|
| `RSK-110` | `RSK-110-A1`, `RSK-110-A2` | `Examine`, `Test` | CAP-140 classification record and independent criteria application | Examined record `EVD-SAMP2-RSK110-CLASSIFY`; independently applied criteria to the fictional sample | [x] |
| `DAT-110` | `DAT-110-A1`, `DAT-110-A2` | `Examine`, `Test` | Data-handling rules and traced prompt/response path for CAP-140 | Examined handling standard `EVD-SAMP2-DAT110-HANDLING`; traced one fictional prompt/response through storage and logs | [x] |

## Evidence pointers

| Evidence ID | Type | Requirement ID(s) | Sufficiency | Limitations noted? | Complete? |
|---|---|---|---|---|---|
| `EVD-SAMP2-RSK110-CLASSIFY` | `record` | `RSK-110` | limited | [x] | [x] |
| `EVD-SAMP2-DAT110-HANDLING` | `procedure` / `configuration` package | `DAT-110` | limited | [x] | [x] |

## Determination capture

| Result ID | Requirement ID(s) | Determination | Design effectiveness | Operating effectiveness | Rationale summary | Status (`draft`/`final`) | Complete? |
|---|---|---|---|---|---|---|---|
| `ASR-SAMP2-RSK110` | `RSK-110` | `partially_satisfied` | `effective` | `partially_effective` | Classification record exists and addresses required factors, but audience-expansion trigger criteria remain incomplete in this fictional sample. | `draft` | [x] |
| `ASR-SAMP2-DAT110` | `DAT-110` | `satisfied` | `effective` | `effective` | Handling rules cover prompt and response paths; traced sample showed classification metadata propagated to storage and logs. | `draft` | [x] |

Filled Draft assessment-result records:

- [`examples/sampling2-rsk110-assessment-result.example.json`](examples/sampling2-rsk110-assessment-result.example.json)
- [`examples/sampling2-dat110-assessment-result.example.json`](examples/sampling2-dat110-assessment-result.example.json)

The first sampling vignette for `GOV-100` and `SYS-220` remains at
[sampling-vignette.example.md](sampling-vignette.example.md).

## Limitation notes

| Limitation | Impact on determination | Residual action | Complete? |
|---|---|---|---|
| Independent criteria Test for `RSK-110` used only one fictional capability | Limits generalization beyond CAP-140 | Expand sample before any portfolio-level claim | [x] |
| `DAT-110` trace used a staging environment, not live production | Limits external reuse of the `satisfied` determination | Re-run trace against production path or accept as Draft-only | [x] |
| Sample covers two controls only | No capability-wide conclusion is supportable | Expand sample before any broader claim | [x] |

## Nonclaims

This Draft deepen vignette is fictional. Completing or copying these tables does
not establish certification, compliance, equivalence, endorsement, assurance,
production readiness, or lifecycle approval for any Draft ESAF artifact.
