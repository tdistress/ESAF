# ESAF-1700 entity instances example (informative)

This sample is non-normative enablement for
[ESAF-1700](../../data-model/ESAF-1700.md) entity contracts. Using it does
not establish certification, compliance, or control satisfaction.

The records below are fictional, selected-field instance sketches. They are
not JSON Schema, a serialization format, or complete ESAF-1500 evidence and
assessment records. Local `OWNER-` labels exist only to connect the sketches;
ESAF-1700 does not define an Accountable Owner identifier pattern.

## Scenario and relationship map

Northstar Benefits uses one AI capability to summarize claims and route
ambiguous cases for human review. An API and a reviewer workbench both depend
on the same policy-language model.

| From | Relationship | To |
|---|---|---|
| `CAP-CLAIMS-01` | `system_refs` | `SYS-CLAIMS-API`, `SYS-CLAIMS-REVIEW` |
| `SYS-CLAIMS-API` | `asset_refs` | `AST-POLICY-MODEL-01` |
| `SYS-CLAIMS-REVIEW` | `asset_refs` | `AST-POLICY-MODEL-01` |
| `CAP-CLAIMS-01` | `risk_classification_ref` | `RSK-CLAIMS-2026-01` |
| `GATE-CLAIMS-PROD-01` | `capability_ref` | `CAP-CLAIMS-01` |
| `EXC-CLAIMS-LOG-01` | `scope_ref` | `SYS-CLAIMS-REVIEW` |

## AI Capability

| Attribute | Example value |
|---|---|
| `capability_id` | `CAP-CLAIMS-01` |
| `name` | Claims summary and review routing |
| `approved_purpose` | Summarize submitted claim material and route uncertain cases to an authorized reviewer; no autonomous coverage decision |
| `business_owner_ref` | `OWNER-CLAIMS-BUSINESS` |
| `technical_owner_ref` | `OWNER-CLAIMS-TECHNICAL` |
| `deployment_status` | Operations |
| `risk_classification_ref` | `RSK-CLAIMS-2026-01` |
| `system_refs` | `SYS-CLAIMS-API`, `SYS-CLAIMS-REVIEW` |
| `review_date` | 2026-11-30 |

## AI Systems

| Attribute | Claims API | Reviewer workbench |
|---|---|---|
| `system_id` | `SYS-CLAIMS-API` | `SYS-CLAIMS-REVIEW` |
| `capability_refs` | `CAP-CLAIMS-01` | `CAP-CLAIMS-01` |
| `asset_refs` | `AST-POLICY-MODEL-01` | `AST-POLICY-MODEL-01` |
| `provider` | Northstar Benefits | Northstar Benefits |
| `hosting` | Private cloud service | Managed workstation application |
| `data_categories` | Claim narrative, policy reference | Claim summary, reviewer disposition |
| `technical_owner_ref` | `OWNER-CLAIMS-TECHNICAL` | `OWNER-CLAIMS-TECHNICAL` |

## Shared AI Asset

| Attribute | Example value |
|---|---|
| `asset_id` | `AST-POLICY-MODEL-01` |
| `asset_type` | Model |
| `system_refs` | `SYS-CLAIMS-API`, `SYS-CLAIMS-REVIEW` |
| `provenance` | Internally fine-tuned fictional base model |
| `version` | `2026.08.1` |
| `license` | Internal evaluation license |
| `integrity_ref` | Protected model-registry digest record |
| `retirement_status` | Active |

Because this is one shared asset, a model-version or integrity change is
recorded once and propagated to both system relationships. Impact analysis
therefore follows both paths back to `CAP-CLAIMS-01`.

## Accountable Owners

| Worksheet label | `name` | `role` | `organization` | `owner_type` | `accountability_scope` |
|---|---|---|---|---|---|
| `OWNER-CLAIMS-BUSINESS` | Jordan Lee | VP, Claims Operations | Northstar Benefits | Business owner | `CAP-CLAIMS-01` |
| `OWNER-CLAIMS-TECHNICAL` | Casey Morgan | Director, AI Platforms | Northstar Benefits | Technical or service owner | `CAP-CLAIMS-01`, `SYS-CLAIMS-API`, `SYS-CLAIMS-REVIEW`, `AST-POLICY-MODEL-01` |

## Risk Classification

| Attribute | Example value |
|---|---|
| `classification_id` | `RSK-CLAIMS-2026-01` |
| `capability_ref` | `CAP-CLAIMS-01` |
| `tier` or `level` | High |
| `criteria_refs` | Material financial effect, sensitive personal data, human-review dependency |
| `determined_by` | `OWNER-CLAIMS-BUSINESS` with Enterprise Risk Committee |
| `determined_at` | 2026-08-15 |
| `required_gates` | Security and risk, production readiness, periodic recertification, material change |
| `required_controls` | Applicable Protect AI and Govern AI controls recorded in the capability inventory |
| `required_evidence` | Initial risk assessment, architecture decision, validation report, production authorization, and monitoring reviews |
| `approval_authority` | Enterprise Risk Committee |
| `monitoring` | Unsupported-summary rate, uncertain-case routing, access failures, policy-model changes, and reviewer overrides |
| `review_frequency` | Quarterly and upon a material change |
| `review_date` | 2026-11-30 |
| `independent_assurance` | Annual independent review of control design and operating effectiveness |
| `human_oversight` | Authorized reviewer decides every uncertain case and may stop use of the capability |

## Lifecycle Gate Decision

| Attribute | Example value |
|---|---|
| `gate_decision_id` | `GATE-CLAIMS-PROD-01` |
| `capability_ref` | `CAP-CLAIMS-01`, version `2026.08.1` |
| `gate` | Production readiness |
| `decision` | Conditional approval |
| `conditions` | Preserve mandatory human review for uncertain cases and close `FND-CLAIMS-01` by the next review |
| `accepted_residual_risk` | Temporary reviewer-workbench log gap accepted through 2026-10-31 |
| `reviewers` | Security lead, privacy lead, claims operations lead |
| `decision_authority` | Enterprise Risk Committee |
| `evidence_refs` | `EVD-CLAIMS-LOG-01` |
| `next_review_or_trigger` | 2026-10-31 or any change to `AST-POLICY-MODEL-01`, whichever occurs first |

## Exception

| Attribute | Example value |
|---|---|
| `exception_id` | `EXC-CLAIMS-LOG-01` |
| `requirement_ref` | Fictional internal control `LOG-07` |
| `scope_ref` | `SYS-CLAIMS-REVIEW` |
| `justification` | Legacy reviewer module does not yet emit the required structured event |
| `risk` | Reduced ability to reconstruct reviewer actions |
| `compensating_measures` | Restricted access, daily export reconciliation, and supervisory review |
| `owner` | `OWNER-CLAIMS-TECHNICAL` |
| `approver` | Enterprise Risk Committee |
| `acceptance_authority` | Enterprise Risk Committee |
| `expiration` | 2026-10-31 |
| `monitoring` | Daily reconciliation exceptions reviewed by Claims Security |
| `remediation_plan` | Deploy structured event logging before expiration |

## ESAF-1500 cross-references

These are identifier and subject sketches only. The Evidence Record,
Assessment Result, and nested Finding retain every required field and meaning
from [ESAF-1500](../../assessment/ESAF-1500.md) unchanged.

| ESAF-1500 record | Selected cross-references |
|---|---|
| Evidence Record `EVD-CLAIMS-LOG-01` | `scope.description`: `CAP-CLAIMS-01`, `SYS-CLAIMS-API`, `SYS-CLAIMS-REVIEW`, and `AST-POLICY-MODEL-01`; `traceability.result_refs`: `ASR-CLAIMS-01` |
| Assessment Result `ASR-CLAIMS-01` | `assessment_scope.subject`: `CAP-CLAIMS-01`; `evidence_refs`: `EVD-CLAIMS-LOG-01`; `findings`: nested `FND-CLAIMS-01` |
| Finding `FND-CLAIMS-01` | `statement`: reviewer-workbench structured logging is incomplete; `evidence_refs`: `EVD-CLAIMS-LOG-01`; `owner`: `OWNER-CLAIMS-TECHNICAL`; `status`: `open` |

The assessment subject identifies the capability, while its boundary and
evidence scope identify both systems and the shared asset. This preserves one
ESAF-1500 record chain while making every affected ESAF-1700 entity
discoverable.
