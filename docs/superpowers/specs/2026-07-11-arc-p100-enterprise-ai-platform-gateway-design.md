# ARC-P100 Enterprise AI Platform and Gateway Design

**Status:** Approved

**Target release:** 0.4-alpha

**Design date:** 2026-07-11

## 1. Purpose

ARC-P100 defines a vendor-neutral pattern for enterprise access to AI models and services through centrally governed policy with federated enforcement. It supports multiple providers, regional and private deployments, diverse application channels, and risk-proportionate control without requiring every request to traverse one physical gateway.

## 2. Decision

Use a centralized governance plane with federated enforcement points.

The governance plane maintains authoritative policy, approved providers and models, routing constraints, identity integration, configuration, cost allocation, assurance status, and lifecycle decisions. Enforcement points apply approved policy near interaction channels, applications, model endpoints, sensitive environments, or regional boundaries.

Direct provider connections are permitted only as a documented variant when they implement equivalent required controls, remain visible to governance and assurance, and receive architecture approval.

## 3. Objectives

The pattern shall:

- provide consistent enterprise policy across heterogeneous AI services;
- preserve user, workload, tenant, application, and agent attribution;
- route requests only to approved models, providers, regions, and configurations;
- enforce data, instruction, output, rate, cost, and usage policy at appropriate boundaries;
- separate management, request, evidence, and provider flows;
- support private and externally hosted model endpoints;
- avoid a mandatory single enforcement bottleneck and single point of failure;
- produce protected, correlated evidence for operations, incident response, audit, and cost management;
- document provider-consumer responsibilities, failure behavior, portability, and exit;
- enable later ARC-P110 through ARC-P160 patterns to inherit shared platform controls.

## 4. Non-goals

ARC-P100 does not:

- define a product selection or procurement recommendation;
- define retrieval, agent, copilot, private-model, or observability behavior in full;
- guarantee model safety or output correctness;
- replace capability-specific authorization, validation, or human oversight;
- require centralized storage of prompt or response content;
- establish compliance with ESAF or an external framework.

## 5. Architecture model

### 5.1 Governance plane

The governance plane contains:

- provider, model, endpoint, and capability registry;
- policy authoring, approval, distribution, versioning, and rollback;
- identity, role, tenant, and workload integration;
- routing constraints and approved fallback chains;
- provider and model lifecycle, assurance, and health status;
- organization-defined limits, budgets, quotas, and allocation rules;
- configuration evidence and architecture decision records.

The governance plane is authoritative for policy but is not required to participate synchronously in every inference request. Enforcement points use signed or otherwise integrity-protected policy bundles with defined validity and fail-safe behavior.

### 5.2 Enforcement plane

Enforcement points may be centralized, regional, embedded, sidecar, service-mesh, application, or endpoint-adjacent. Each point shall have a managed identity, approved scope, current policy, protected configuration, health reporting, and attributable evidence.

Enforcement responsibilities include, as applicable:

- authentication and authorization context validation;
- provider, model, version, region, and purpose routing;
- data classification, instruction, content, schema, and output policy;
- prompt, context, tool, and response size limits;
- token, request, concurrency, latency, cost, and abuse controls;
- request and response correlation without unnecessary content retention;
- provider credential isolation and rotation;
- bounded retry, circuit breaking, fallback, and safe failure.

### 5.3 Provider plane

The provider plane includes external model APIs, managed enterprise AI services, private inference endpoints, model routers, and supporting safety services. Provider boundaries remain explicit regardless of contract, private connectivity, or hosting arrangement.

### 5.4 Evidence and operations plane

The evidence and operations plane receives protected events, metrics, traces, policy decisions, configuration changes, provider health, usage, cost, and incident signals. Content collection is minimized and controlled according to sensitivity, purpose, privacy, and retention obligations.

## 6. Flow separation

The pattern distinguishes four flow classes:

| Flow | Purpose | Required properties |
|---|---|---|
| Management | Configure policy, registry, routing, identities, providers, and enforcement points | Privileged access, approval, integrity, versioning, rollback, complete administrative evidence |
| Request | Carry user or workload instructions, context, model calls, and responses | Attribution, authorization, validation, confidentiality, limits, correlation, safe retry |
| Evidence | Export events, metrics, traces, decisions, cost, and health | Minimization, integrity, access control, retention, correlation, delivery monitoring |
| Provider | Exchange calls, credentials, metadata, health, and service notifications with model providers | Explicit responsibility, endpoint authorization, encryption, credential isolation, residency and failover constraints |

Mixing flow privileges or credentials is prohibited. Evidence transport shall not provide an administrative or request bypass.

## 7. Trust-zone mapping

| Zone | ARC-P100 use |
|---|---|
| Z0 | Public users, internet content, untrusted clients, and external data |
| Z1 | Enterprise users, applications, developer tools, and API consumers |
| Z2 | Governance services, AI gateways, regional enforcement points, and policy distribution |
| Z3 | Capability applications, prompt assembly, orchestration, and session state |
| Z4 | External and private model inference endpoints and safety services |
| Z5 | Enterprise data and knowledge services referenced by capability-specific patterns |
| Z6 | Tools and action targets referenced by agentic or integration patterns |
| Z7 | Registry, vault, CI/CD, observability, SIEM, evidence, backup, and administration |

ARC-P100 focuses on Z1-Z2-Z4-Z7 crossings while preserving interfaces for Z3, Z5, and Z6 patterns.

## 8. Required control points

| Control point | Outcome |
|---|---|
| CP1 Channel admission | Authenticate the caller and bind user, tenant, workload, application, purpose, and risk context |
| CP2 Policy decision | Determine whether the requested model, provider, data, operation, and configuration are authorized |
| CP3 Request enforcement | Apply validation, classification, limits, transformations, routing, and correlation |
| CP4 Provider boundary | Protect credentials, endpoints, transport, residency, failover, and shared responsibility |
| CP5 Response enforcement | Validate schema, classification, policy, attribution, and downstream handling requirements |
| CP6 Evidence export | Emit minimized, protected, attributable, and time-correlated evidence |
| CP7 Administrative control | Protect policy, registry, configuration, deployment, exception, and rollback actions |

Capabilities may distribute these control points across components, but each outcome shall have one accountable owner.

## 9. Required ESAF controls

ARC-P100 requires or strongly depends on:

- `API-100` Enterprise AI Gateway;
- `API-110` AI API Security;
- `API-140` External AI Service Integration;
- `API-150` AI Interoperability and Portability;
- `IAM-100` AI Identity Governance;
- `IAM-110` AI Authentication;
- `IAM-120` AI Authorization and Least Privilege;
- `IAM-130` Privileged AI Access;
- `IAM-140` AI Secrets Management;
- `DAT-100` AI Data Authority and Purpose;
- `DAT-110` AI Data Classification and Handling;
- `APP-120` AI Output Handling;
- `INF-140` AI Cryptographic Protection;
- `INF-150` AI Resource and Capacity Safeguards;
- `MON-100` AI Telemetry;
- `MON-110` AI Security Detection;
- `MON-140` AI Alert Response;
- `MON-150` AI Audit Trails;
- `OPS-110` AI Change and Release Management;
- `OPS-120` AI Incident Management;
- `OPS-130` AI Continuity and Recovery;
- `OPS-140` AI Capacity and Performance Management;
- `ARC-110` AI Trust Boundaries and Data Flows;
- `ARC-130` AI Resilience and Failure Design;
- `ARC-140` AI Shared Responsibility Architecture.

The final pattern will distinguish required, conditional, and inherited controls and identify enforcement and evidence ownership.

## 10. Variants

### 10.1 Central gateway

All requests traverse a shared enforcement service. This is appropriate for simpler environments but requires capacity, resilience, isolation, and concentration-risk treatment.

### 10.2 Regional gateways

Regional enforcement points use centrally governed policy. This supports residency, latency, sovereignty, and regional continuity while requiring policy synchronization and evidence correlation.

### 10.3 Embedded enforcement

Application libraries, sidecars, service-mesh components, or endpoint-adjacent proxies enforce policy. This reduces central bottlenecks but requires attestation, version governance, consistent evidence, and bypass prevention.

### 10.4 Controlled direct connection

An application connects directly to an approved provider. The design shall demonstrate equivalent identity, authorization, data, secrets, limits, evidence, monitoring, cost, provider, and exit controls. Direct connection is not a policy exemption.

### 10.5 Private inference

The provider boundary terminates at an enterprise-operated model endpoint. Shared gateway controls still apply, while infrastructure and model lifecycle responsibilities shift to the enterprise.

## 11. Failure behavior

The pattern shall define:

- behavior when governance policy is unavailable or stale;
- enforcement-point health and policy-version reporting;
- fail-closed conditions for unauthorized, unclassified, or high-impact requests;
- explicitly approved degraded modes for low-risk use;
- bounded and idempotent retry;
- circuit breaking and provider health quarantine;
- fallback chains constrained by data, region, model, risk, and contract;
- preservation of correlation and decision evidence across failover;
- emergency suspension of a provider, model, capability, tenant, or enforcement point;
- recovery and reconciliation after disconnected operation.

Failover shall not silently send data to a new provider, model, region, or retention regime.

## 12. Threat and abuse focus

The pattern will address policy bypass, direct unauthorized model access, credential theft, tenant confusion, identity-context loss, route manipulation, downgrade, shadow endpoints, prompt or response leakage, logging leakage, unsafe transformation, excessive resource use, denial of service, provider compromise, stale policy, unapproved failover, evidence gaps, and administrative abuse.

## 13. Evidence and assessment

Required evidence will include:

- provider and model registry exports;
- policy and routing versions, approvals, distribution status, and rollback records;
- enforcement-point inventory, identity, health, and policy currency;
- sampled authorization, routing, limit, transformation, and denial decisions;
- secrets-management and provider credential records;
- provider assurance, contract, notification, continuity, and exit records;
- correlated request, response, error, retry, failover, and evidence-delivery records;
- capacity, latency, availability, cost, abuse, and exception metrics;
- tested suspension, failover, rollback, recovery, and direct-connect controls.

Assessment shall verify both design and operating effectiveness across representative enforcement points and providers.

## 14. Validation changes

The architecture validator will evolve from foundation-only checks to pattern-aware validation. It will verify that:

- `architectures/patterns/ARC-P100.md` exists;
- the record contains every required pattern heading;
- the pattern ID, title, status, and version are present;
- the registry links to the pattern and marks it Draft;
- referenced ESAF controls resolve to real control files;
- local links and text encoding are valid;
- the record contains no unresolved placeholder markers.

Unit tests will be written before validator changes.

## 15. Acceptance criteria

ARC-P100 is complete when:

- every architecture-template section is substantively populated;
- management, request, evidence, and provider flows are distinct;
- centralized governance and federated enforcement responsibilities are explicit;
- seven control points, five variants, trust-zone crossings, and failure behavior are defined;
- required, conditional, and inherited ESAF controls are mapped;
- evidence and assessment expectations are testable;
- the pattern registry links ARC-P100 and changes its state to Draft;
- pattern-aware unit tests, architecture validation, and control-catalog validation pass;
- CI passes on the PR and post-merge `main`.

## 16. Out of scope

This milestone does not include product configurations, infrastructure code, completed external-standard mappings, publication-quality graphics, quantitative performance benchmarks, or the supporting ARC-P160 observability pattern.
