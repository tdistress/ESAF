# ESAF-1300 exception workflow example (informative)

This worksheet is non-normative enablement for the
[ESAF-1300](../../governance/ESAF-1300.md) exception workflow. Completing it
does not establish certification, compliance, or control satisfaction.

The organization, capability, exception, dates, and decisions below are
fictional. [GOV-140](../../controls/GOV/GOV-140.md) remains authoritative for
exception requirements.

## Fictional scenario

Northstar Services identifies that `CAP-042`, its customer-support assistant,
uses an unsupported gateway component. Replacement is scheduled, but the
capability owner requests a temporary deviation while network restrictions
and enhanced log review reduce exposure.

## Walkthrough

| Stage | Fictional record |
|---|---|
| **1. Request** | Exception `EX-042-01` covers only gateway component `GW-7` in production capability `CAP-042` version 2.3. The justification is continuity during replacement. The business owner is accountable. Proposed compensating measures are network allowlisting, removal of administrative access from the gateway, and enhanced log review. |
| **2. Risk review** | Security and risk reviewers document the unsupported-component threat, affected service boundary, remaining residual risk, and the condition that the capability stays within its approved purpose. They recommend approval only through 2026-10-15. |
| **3. Approval** | The fictional AI governance council, acting within its documented authority, approves the exception on 2026-09-01. The decision identifies the accountable owner, scope, compensating measures, remediation commitment, expiration, and review conditions. Any control-measure failure or material scope change triggers immediate review. |
| **4. Register entry** | The central exception register records `EX-042-01`, links `CAP-042` and `GW-7`, identifies the council as approval authority, and links the risk review, approval record, and replacement work item. |
| **5. Monitoring** | The security owner reviews allowlist configuration and gateway logs weekly. The exception owner reports status to the council. A failed restriction, material incident, delayed replacement, or approach of expiration triggers escalation. |
| **6. Closure or renewal** | The replacement is deployed and validated on 2026-10-03. The owner submits remediation evidence, the council records closure on 2026-10-05, and monitoring confirms removal of the temporary measures. If remediation had not completed, a separately reviewed renewal decision would have been required before 2026-10-15. |

## GOV-140 field coverage

| GOV-140 field | Where represented in the fictional record |
|---|---|
| Scope | `CAP-042` version 2.3 and gateway component `GW-7` |
| Justification | Service continuity during component replacement |
| Risk | Unsupported-component threat, service boundary, and documented residual risk |
| Compensating measures | Network allowlisting, administrative-access removal, and enhanced log review |
| Accountable owner | Capability business owner |
| Approval authority | AI governance council acting within documented authority |
| Monitoring | Weekly restriction and log review with status reporting |
| Remediation | Replace and validate the unsupported component |
| Expiration | 2026-10-15 |
| Review conditions | Measure failure, incident, scope change, delay, or approaching expiration |

This example is informative and is not conformance evidence. A real exception
record must use the organization's authorized workflow and retain the
evidence required by GOV-140.
