# ARC-P100 Enterprise AI Platform and Gateway

## Metadata

**Pattern ID:** ARC-P100

**Status:** Draft

**Version:** 0.1.0

| Field | Value |
|---|---|
| Owner | Enterprise Architecture |
| Required reviewers | Security Architecture, Platform Engineering, AI Engineering, Data Governance, Operations |
| Pillars | Protect AI, Utilize AI, Govern AI |
| Lifecycle stages | Architecture, Development, Validation, Approval, Deployment, Operations, Monitoring, Retirement |
| Capability tiers | Tier 1 through Tier 4; Tier 0 when connected to enterprise services |
| Deployment models | Cloud, on-premises, edge, hybrid, managed service, private inference |
| Primary pattern role | Shared platform or supporting architecture pattern |
| Supersedes | None |

## Purpose

Provide governed enterprise access to multiple AI models and services through a centralized governance plane with federated enforcement points. The pattern applies consistent identity, routing, data, usage, provider, evidence, resilience, and lifecycle controls without requiring every inference request to traverse one physical gateway.

## Problem statement

Direct and inconsistent integration with AI services creates fragmented identity, data handling, provider credentials, routing, monitoring, cost, resilience, and assurance. A single mandatory gateway can reduce fragmentation but may create capacity bottlenecks, regional constraints, and concentration risk. Enterprises require common governance with enforcement that can be centralized, regional, embedded, or endpoint-adjacent according to risk and operating context.

## Intended outcomes

- AI consumers use approved models, providers, endpoints, regions, and configurations.
- Human and non-human requests remain attributable to a user, workload, tenant, application, and approved purpose.
- Policy is approved centrally and enforced consistently at documented boundaries.
- Data, instructions, outputs, provider credentials, evidence, and administrative actions receive risk-proportionate protection.
- Regional, private, and high-sensitivity workloads can use local enforcement without losing central governance.
- Provider failover, portability, and exit remain controlled and observable.
- Shared platform controls can be inherited by other ESAF architecture patterns.

## Non-goals

This pattern does not select products, prescribe a single gateway topology, guarantee model safety or output correctness, replace capability-specific authorization or human oversight, require centralized storage of content, or fully define retrieval, agent, copilot, private-model, integration, or observability behavior.

## Applicability

Use ARC-P100 when an organization provides shared access to one or more external or private AI services and needs consistent enterprise policy, model routing, provider governance, evidence, or cost allocation.

ARC-P100 may be the primary pattern for a general AI platform. It is commonly a supporting pattern for enterprise copilots, retrieval-augmented generation, agentic AI, private inference, embedded AI services, and observability.

Tier 3 and Tier 4 capabilities require enhanced resilience, independent validation, strict provider fallback constraints, privileged-access protection, and risk-authorized degraded modes.

## Assumptions and prerequisites

- The AI capability, business owner, technical owner, risk classification, and approved purpose are recorded.
- Enterprise identity, secrets management, logging, incident management, and change management services are available.
- Providers, models, endpoints, regions, and processing purposes have an approval status.
- Data classification and handling rules can be evaluated before provider routing.
- Platform and capability teams have documented shared responsibilities.
- Organization-defined parameters exist for limits, retention, policy validity, fallback, and recovery.

## Prohibited uses

The pattern shall not be used to:

- route unidentified or unauthorized requests;
- conceal provider, model, region, data-use, or retention changes;
- treat a gateway filter as the sole safeguard for unsafe or consequential use;
- reuse provider credentials across unrelated tenants or trust contexts;
- fail over to a provider or region that is not authorized for the request data and purpose;
- bypass capability-specific approval, retrieval authorization, tool authorization, or human oversight;
- collect complete prompt and response content by default when less sensitive evidence is sufficient.

## Architecture views

### Context view

```text
AI Consumers
    |
    v
Federated Enforcement Points <---- Central Governance Plane
    |
    +----> External AI Providers
    |
    +----> Private Inference Endpoints
    |
    v
Evidence and Operations Services
```

The central governance plane distributes approved policy and configuration. Enforcement points make request-time decisions within their authorized scope. Providers execute inference. Evidence and operations services receive protected telemetry without creating a request or administrative bypass.

### Plane view

| Plane | Primary functions | Synchronous request dependency |
|---|---|---|
| Governance | Registry, policy, routing constraints, identity integration, limits, provider lifecycle, assurance | Not required when a valid protected policy bundle is available |
| Enforcement | Admission, authorization, validation, routing, limits, transformation, response handling | Required at each designated control boundary |
| Provider | Model inference, provider safety services, endpoint health, service notifications | Required for selected inference unless an approved fallback is used |
| Evidence and operations | Events, metrics, traces, cost, detection, incident, administration, recovery | Evidence delivery may be asynchronous within approved loss and delay bounds |

### Deployment view

Enforcement points may be shared, regional, embedded, sidecar, service-mesh, application, or endpoint-adjacent components. Multiple forms may coexist when policy authority, scope, identity, evidence, bypass protection, and control ownership remain explicit.

## Actors and identities

| Actor | Identity and authority expectations |
|---|---|
| Human user | Enterprise identity, tenant, role, purpose, session, and applicable consent or notice context |
| Calling application | Managed workload identity bound to an approved capability, environment, owner, and deployment |
| AI agent | Unique managed identity with bounded delegation, tools, data, resources, and lifetime |
| Enforcement point | Managed platform identity authorized for policy retrieval, provider invocation, and evidence export within scope |
| Governance administrator | Privileged named identity using separate administrative paths, approval, and complete audit evidence |
| Provider endpoint | Authenticated and authorized service endpoint with approved model, region, contract, and assurance state |
| Evidence consumer | Managed security, operations, risk, cost, or audit identity limited to necessary telemetry |

Identity context shall not be accepted solely from caller-supplied headers. Delegation and impersonation shall be explicit, integrity-protected, time-bounded, and traceable.

## Data and instruction flows

| Flow | Contents | Required properties |
|---|---|---|
| Management | Policy, registry, routes, provider status, limits, deployments, exceptions | Privileged access, approval, integrity, versioning, rollback, administrative evidence |
| Request | User instructions, system instructions, context, attachments, model parameters, response | Attribution, authorization, classification, confidentiality, validation, limits, correlation, safe retry |
| Evidence | Decisions, events, metrics, traces, errors, cost, health, selected content samples | Minimization, integrity, access control, retention, correlation, delivery monitoring |
| Provider | Model request and response, credentials, endpoint metadata, health, notification | Endpoint authorization, credential isolation, encryption, residency, purpose, failover constraints |

Management, request, evidence, and provider credentials shall remain separated. Transformations shall preserve necessary classification, provenance, authorization, and correlation metadata.

## Trust boundaries

| Crossing | Key requirements |
|---|---|
| Z0 to Z1 | Treat public users, content, and external instructions as untrusted; apply channel and capability controls |
| Z1 to Z2 | Bind caller, workload, tenant, capability, purpose, classification, and requested operation |
| Z2 to Z3 | Preserve authorized context while preventing applications from bypassing platform policy |
| Z2 to Z4 | Use approved endpoint, model, version, region, credentials, transport, limits, and provider terms |
| Z3 to Z5 | Defer knowledge authorization and retrieval decisions to the applicable data and RAG pattern |
| Z3 to Z6 | Defer tool and consequential-action authorization to the applicable agentic or integration pattern |
| Z2 to Z7 | Export minimized correlated evidence and receive policy through protected, independently authorized paths |
| Z7 to Z2 | Restrict administrative changes, policy distribution, rollback, and emergency suspension to privileged workflows |

Private connectivity does not remove an external provider boundary. Physical co-location does not remove logical separation among planes.

## Components and responsibilities

| Component | Required responsibility |
|---|---|
| Provider and model registry | Record owner, approval, model and endpoint identity, version, region, data terms, limits, assurance, status, and exit information |
| Policy management | Author, review, approve, sign, distribute, expire, revoke, and roll back policy |
| Identity integration | Resolve and validate enterprise identity, role, tenant, workload, capability, and delegation context |
| Routing service | Select only approved providers and models using purpose, data, region, health, risk, cost, and fallback constraints |
| Enforcement point | Apply admission, policy, validation, routing, limits, transformation, response, and evidence controls within assigned scope |
| Secrets service | Issue, store, rotate, revoke, and monitor provider and platform credentials |
| Evidence pipeline | Receive, protect, correlate, retain, route, and monitor delivery of events, metrics, traces, and decisions |
| Operations service | Monitor health, capacity, latency, cost, provider state, policy currency, and control effectiveness |
| Capability application | Retain responsibility for use-case logic, capability authorization, user experience, output use, and downstream effects |
| AI provider | Perform contracted service functions and provide agreed security, availability, notification, evidence, portability, and exit support |

Inherited controls shall identify provider or platform evidence, consumer configuration, verification frequency, limitations, and failure dependencies.

## Required controls

| Control | Applicability | Primary enforcement or evidence owner |
|---|---|---|
| `API-100` | Required | Platform owner and enforcement-point owner |
| `API-110` | Required | API and platform engineering |
| `API-140` | Required for external services | Third-party risk, platform owner, and provider |
| `API-150` | Required | Enterprise architecture and platform owner |
| `IAM-100` | Required | Identity governance |
| `IAM-110` | Required | Identity and platform engineering |
| `IAM-120` | Required | Capability owner and platform owner |
| `IAM-130` | Required | Privileged access management |
| `IAM-140` | Required | Secrets-management owner |
| `DAT-100` | Required | Data owner and capability owner |
| `DAT-110` | Required | Data governance and enforcement-point owner |
| `APP-120` | Conditional on downstream output use | Capability application owner |
| `INF-140` | Required | Infrastructure and platform engineering |
| `INF-150` | Required | Platform operations |
| `MON-100` | Required | Observability owner |
| `MON-110` | Required | Security operations |
| `MON-140` | Required | Security and platform operations |
| `MON-150` | Required | Platform owner and assurance |
| `OPS-110` | Required | Platform engineering and change authority |
| `OPS-120` | Required | Incident-response owner |
| `OPS-130` | Required | Service owner and continuity owner |
| `OPS-140` | Required | Platform operations and financial owner |
| `ARC-110` | Required | Solution architect |
| `ARC-130` | Required | Solution architect and service owner |
| `ARC-140` | Required | Enterprise architecture and provider owner |

Additional controls apply according to capability behavior, data, provider, tier, deployment, and overlays.

## Control points and overlays

| Control point | Required outcome |
|---|---|
| CP1 Channel admission | Authenticate the caller and bind identity, tenant, workload, capability, purpose, and risk context |
| CP2 Policy decision | Determine whether the requested model, provider, data, operation, region, and configuration are authorized |
| CP3 Request enforcement | Apply validation, classification, limits, approved transformations, routing, and correlation |
| CP4 Provider boundary | Protect credentials, endpoint authorization, transport, residency, failover, and shared responsibility |
| CP5 Response enforcement | Apply schema, classification, policy, attribution, and downstream handling decisions |
| CP6 Evidence export | Emit minimized, protected, attributable, and time-correlated evidence and monitor delivery |
| CP7 Administrative control | Protect registry, policy, configuration, deployment, exception, suspension, and rollback actions |

Apply overlays for Tier 3 and Tier 4 risk, regulated or confidential data, public exposure, regional residency, private inference, and consequential or agentic use. Each control-point outcome shall have one accountable owner even when multiple components contribute.

## Architecture decisions and parameters

Required decisions include:

- centralized, regional, embedded, direct-connect, private-inference, or combined enforcement;
- synchronous and asynchronous policy dependencies;
- policy bundle signing, validity, refresh, revocation, and disconnected behavior;
- identity claims and delegation accepted at each boundary;
- approved provider, model, version, region, purpose, and fallback constraints;
- request and response transformation authority;
- content logging, sampling, redaction, retention, and evidence access;
- rate, token, concurrency, size, latency, cost, and circuit-breaker limits;
- error disclosure, retry, idempotency, fallback, safe-state, and recovery;
- provider exit, credential revocation, endpoint retirement, and evidence preservation.

Organization-defined parameters shall record exact values, owner, approval authority, environment, review frequency, monitoring, and change method.

## Failure modes and abuse cases

| Condition | Required treatment |
|---|---|
| Governance plane unavailable | Use only valid protected policy within approved age; fail safely when authority or classification is uncertain |
| Stale or corrupted policy | Reject invalid policy, report version and health, quarantine affected enforcement, and restore an approved version |
| Enforcement bypass | Block unauthorized provider paths using identity, network, endpoint, secrets, procurement, and detection controls |
| Identity-context loss | Reject or restrict the request; do not infer tenant, purpose, or authority |
| Route manipulation or downgrade | Authorize routing from protected policy and record the selected model, provider, region, and reason |
| Provider degradation | Use bounded retry and circuit breaking; apply only authorized fallback chains |
| Duplicate consequential request | Require idempotency or capability-specific confirmation before retry |
| Credential compromise | Revoke and rotate credentials, isolate affected routes, preserve evidence, and invoke incident response |
| Evidence delivery failure | Buffer within approved limits, alert, reconcile, and fail safely where evidence is mandatory |
| Capacity or cost abuse | Apply quotas, rate and concurrency limits, anomaly detection, budget controls, and owner escalation |
| Administrative abuse | Require privileged access, separation of duties, approval, alerting, and complete audit records |
| Provider or model compromise | Suspend the endpoint or model, block routing, assess affected requests, and activate approved recovery or exit |

## Fallback recovery and retirement

Fallback chains shall be pre-approved for data classification, purpose, model suitability, provider, region, retention, and contractual terms. Failover shall preserve identity, policy, correlation, and evidence and shall not silently change the risk basis.

Recovery procedures shall test policy rollback, enforcement isolation, provider suspension, credential rotation, evidence reconciliation, configuration restoration, and controlled service reintroduction.

Retirement shall remove routes, endpoints, credentials, policies, exceptions, integrations, provider access, cached content, and administrative privileges; preserve required evidence; update the registry; notify dependent capabilities; and execute provider exit and data-disposition obligations.

## Evidence and assessment

Required evidence includes:

- provider, model, endpoint, enforcement-point, and dependent-capability inventories;
- policy, route, limit, and configuration versions with approval, distribution, expiry, and rollback records;
- sampled admission, authorization, routing, transformation, denial, error, and response decisions;
- provider credentials, issuance, use, rotation, and revocation evidence;
- provider assurance, contract, incident-notification, continuity, portability, and exit records;
- correlated request, provider, response, error, retry, failover, and evidence-delivery events;
- availability, latency, capacity, cost, abuse, policy-currency, denial, and exception metrics;
- exercise results for provider suspension, fallback, rollback, recovery, direct connection, and retirement.

Assessment shall examine representative providers, models, regions, enforcement forms, tenants, capability tiers, and failure paths. Testing shall confirm that unauthorized direct access, provider fallback, stale policy, missing identity, excessive use, and evidence failure produce the approved outcome.

## Variants and alternatives

### Central gateway

All requests traverse a shared enforcement service. This simplifies consistency but requires strong isolation, horizontal capacity, regional design, and concentration-risk treatment.

### Regional gateways

Regional enforcement uses centrally governed policy to support latency, residency, sovereignty, and continuity. Policy synchronization, evidence correlation, and regional divergence require explicit control.

### Embedded enforcement

Application libraries, sidecars, service-mesh components, or endpoint-adjacent proxies enforce policy. This reduces central bottlenecks but requires version governance, attestation, consistent evidence, and bypass prevention.

### Controlled direct connection

An application connects directly to an approved provider and demonstrates equivalent identity, authorization, data, secrets, limits, evidence, monitoring, cost, provider, and exit controls. Direct connection is not a policy exemption.

### Private inference

The provider boundary terminates at an enterprise-operated endpoint. Gateway controls remain applicable while model, infrastructure, capacity, and lifecycle responsibilities shift to the enterprise.

## Anti-patterns

- One provider credential shared across applications, tenants, environments, or users.
- Caller-controlled headers accepted as authoritative identity, classification, or policy context.
- A gateway content filter represented as complete AI security.
- Unapproved direct endpoints or embedded SDKs that bypass registry, policy, or evidence.
- Failover based only on availability or cost without data, region, model, and contract authorization.
- Complete content logging by default without purpose, minimization, access, and retention controls.
- Governance policy required synchronously without a resilient, integrity-protected, fail-safe design.
- Evidence or administrative channels that provide an alternate request path.
- Central enforcement without tenant isolation, capacity planning, or regional failure treatment.
- Distributed enforcement without policy currency, attestation, inventory, and correlation.

## Related patterns

- `ARC-P110` Enterprise copilot uses ARC-P100 for shared model access and policy.
- `ARC-P120` Retrieval-augmented generation adds governed knowledge retrieval and grounding.
- `ARC-P130` Agentic and multi-agent AI adds delegation, tools, memory, and action controls.
- `ARC-P140` Private model deployment defines enterprise-operated inference responsibilities.
- `ARC-P150` AI integration services defines reusable application integration boundaries.
- `ARC-P160` AI observability defines shared evaluation, monitoring, and assurance services.

## Change history

| Pattern version | ESAF release | Date | Change |
|---|---|---|---|
| 0.1.0 | 0.4-alpha | 2026-07-11 | Initial draft |
