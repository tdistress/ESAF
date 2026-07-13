# ARC-P150 AI integration services

## Metadata

**Pattern ID:** ARC-P150

**Status:** Draft

**Version:** 0.1.0

| Field | Value |
|---|---|
| Owner | Enterprise Architecture |
| Required reviewers | Application Architecture, API Architecture, Integration Architecture, Identity and Access Management, Data Governance, Model Governance, Security Architecture, Operations, Business Continuity, Privacy, Legal, Third-Party Risk, Records Management, Assurance |
| Approval date | Not approved (Draft) |
| Review date | Before approval; then at the organization-defined architecture review interval |
| Pillars | Protect AI, Utilize AI, Govern AI |
| Lifecycle stages | Strategy, Architecture, Development, Validation, Approval, Deployment, Operations, Monitoring, Continuous improvement, Retirement |
| Capability tiers | Tier 1 through Tier 4; isolated Tier 0 experimentation |
| Deployment models | Centralized, federated, regional, sovereign, high-assurance, edge, thin synchronous, durable workflow, external-managed |
| Primary pattern role | Primary AI integration services pattern |
| Supersedes | None |

## Purpose

Define a governed, reusable integration boundary for embedding AI capabilities into enterprise applications. The pattern standardizes stable capability-level contracts, identity and policy propagation, deterministic service dispatch, protocol adaptation, delivery semantics, state, compatibility, resilience, evidence, and lifecycle across synchronous, asynchronous, streaming, batch, event or subscription, and callback interactions. It prevents consuming applications from integrating directly and inconsistently with model providers, private inference, enterprise knowledge, tools, targets, or external AI services.

## Problem statement

Enterprise applications otherwise integrate with AI capabilities through inconsistent provider interfaces, identity mappings, schemas, protocols, retry behavior, state models, and evidence paths. Those differences obscure business purpose and authorization, allow adapters to broaden authority or data use, conflate transport success with business outcome, create fragile provider dependencies, and make isolation, recovery, compatibility, and retirement difficult to assess consistently.

## Intended outcomes

- Stable, reusable service contracts replace raw provider-specific interfaces.
- Authoritative identity, tenant, purpose, classification, provenance, policy, and correlation survive every hop.
- All six interaction modes use explicit and consistent delivery semantics.
- Consumer, tenant, job, stream, batch, callback, cache, queue, result, and support state remain isolated.
- Adapters cannot broaden data access, provider choice, target scope, action authority, or credential use.
- Transport, execution, inference, target, and business outcomes remain distinct and reconcilable.
- Regional isolation, data locality, independent scaling, bounded degradation, and controlled recovery are supported.
- Compatibility, portability, deprecation, and retirement are testable.
- Independently assessable evidence is available without unnecessary copying of sensitive content.

## Non-goals

This pattern does not define a universal enterprise service bus, raw provider proxy, generic arbitrary-execution API, business-specific workflow, AI gateway replacement, retrieval ingestion shortcut, agent authorization service, MCP trust proxy, model-management interface, or authoritative observability store. It does not replace conventional API management, service mesh, messaging, workflow, ETL, transaction, software supply-chain, or target-native authorization controls, and it does not claim that delivery success proves output correctness or business completion. Product selection and external-standard mappings remain outside this pattern.

## Applicability

Use this pattern when enterprise applications consume reusable AI services through synchronous requests, asynchronous jobs, streams, batches or files, events or subscriptions, or callbacks. It applies to Tier 1 through Tier 4 capabilities and to isolated Tier 0 experimentation when the experiment cannot connect to production authority or data. It supports centralized, federated, regional, sovereign, high-assurance, edge, thin synchronous, durable-workflow, and externally managed deployments. ARC-P150 may execute deterministic, pre-authorized service workflows; ARC-P130 is mandatory when AI selects a tool, target, operation, or materially consequential parameters, expands delegated authority, or initiates consequential action.

## Assumptions and prerequisites

The consuming capability has an accountable owner, approved business purpose, use-case authorization, human-oversight decision, data classification, capability tier, lifecycle state, and downstream-use rules. Enterprise identity, policy, secrets, contract and schema governance, target-native authorization, records, continuity, supplier-risk, and evidence services are available or their inherited outcomes are explicitly verified. Applicable ARC-P100, ARC-P120, ARC-P130, ARC-P140, and ARC-P160 responsibilities remain authoritative, and the consuming capability retains accountability for output use and downstream effects.

## Prohibited uses

The pattern shall not expose raw provider interfaces or arbitrary execution as an enterprise contract; treat model output, prompt content, transport metadata, an agent lease, or discovery results as authority; let adapters select unapproved providers, targets, operations, or credentials; claim exactly-once business effects from transport behavior; or represent transport, callback, queue, trace, or model success as a verified business outcome. It shall not bypass applicable AI gateway, retrieval, agency, private-model, target-native authorization, or independent-evidence requirements, and it shall not support a deployment that cannot preserve tenant isolation, bounded authority, safe failure, reconciliation, and retirement.

## Architecture views

The architecture shall document the shared governance and control plane, federated regional or domain execution cells, all six logical planes, consumer and dependency context, interaction flows, deployment placement, operational paths, evidence export, state ownership, and responsibility boundaries. The shared plane distributes signed policy and configuration but is not required to carry application content or every request.

## Actors and identities

Human, consumer, workload, execution-cell, service, adapter, provider, broker, callback, target, support, and administrator identities shall be distinct, inventoried, authenticated, scoped, rotated, revoked, and evidenced. Delegation and token exchange cannot expand audience, lifetime, purpose, tenant, provider, model, data, tool, target, or administrative authority, and authorization is re-evaluated at each material durable or consequential step.

## Data and instruction flows

Every interaction shall use a versioned canonical contract that binds authoritative identity, tenant, capability, purpose, operation, classification, provenance, residency, retention, correlation, causation, deadlines, budgets, and mode-specific state. Data, instructions, provider responses, callback content, metadata, and model output remain untrusted and cannot become policy, route, target, command, credential reference, or authorization.

## Trust boundaries

Every material crossing among Z0 through Z7 shall have a boundary-crossing record covering direction, purpose, identities, authentication, delegation, authorization, data and instruction semantics, validation, encryption, secrets, state, tenant isolation, evidence, timeout, retry, ordering, capacity, failure behavior, and retained responsibility. Queue storage remains a logical boundary when co-located, external services remain external when contracted, and Z7 cannot create an unmonitored workload or replay path.

## Components and responsibilities

The pattern comprises governance and contract; admission and policy; execution and adapter; durable delivery and state; output and delivery; and operations, administration, and evidence planes. Regional or domain execution cells implement approved runtime functions under signed, freshness-bounded configuration. Operations and administration remain isolated from evidence export, and adjacent patterns retain their defined model, retrieval, agency, private-model, consumer-experience, and assurance responsibilities.

## Required controls

Each implementation shall allocate all applicable ESAF-1100 controls as required, inherited-and-verified, or conditional without overlap. The control record identifies implementation location, the catalog-accountable owner, evidence owner, inheritance source and limitations, conditional trigger, freshness, failure dependency, retained responsibility, exception state, and assessment result.

## Control points and overlays

Deployments shall implement and evidence the approved CP1 through CP15 control points for governance, registration, admission, contract validation, context binding, isolation, dispatch, durable state, inference, data and retrieval, tool and target handoff, output delivery, external boundaries, evidence export, recovery, compatibility, and retirement. Applicable security, privacy, resilience, deployment, risk, jurisdiction, supplier, records, and assurance overlays shall strengthen rather than weaken the baseline.

## Architecture decisions and parameters

The baseline is a contract-first federated integration fabric with a shared policy-administration and configuration plane and conformant regional or domain execution cells. Durable work assumes at-least-once transport, idempotency, deduplication, bounded retry, explicit unknown outcomes, and authoritative reconciliation; transport behavior never establishes exactly-once business effects. Deployments define limits, deadlines, leases, freshness, retention, compatibility windows, recovery objectives, review cadence, and accountable approval authorities.

## Failure modes and abuse cases

Each deployment shall maintain a failure-and-abuse treatment record for identity and delegation abuse, cross-tenant access, contract or semantic drift, injection, forged or stale configuration, provider and target failure, duplicate or replayed work, cancellation races, unknown or contradictory state, callback and event abuse, capacity exhaustion, evidence loss or forgery, degraded operation, and incomplete retirement. Each treatment states detection bounds, containment and safe state, recovery authority, reconciliation source, evidence, residual risk, tier applicability, and retest trigger.

## Fallback recovery and retirement

Timeouts and dependency failures move work to an explicit failed, stopped, quarantined, or unknown state according to contract. Retries are bounded and limited to proven idempotent operations or target-native idempotency with reconciliation. Degraded operation cannot expand authority, higher-risk work stops when current trust or required evidence is unavailable, and recovery requires current authorization and dependency validation. Retirement resolves unknown outcomes, drains or cancels work, revokes routes and credentials, removes callbacks and subscriptions, disposes state and provider-held data, preserves required evidence, and tests for residual access.

## Evidence and assessment

The implementation shall retain inventories, architecture and boundary records, versioned contracts, identity and delegation matrices, data lifecycle mappings, signed configuration history, delivery and reconciliation matrices, state records, compatibility and recovery tests, provider-gap records, and a CP1 through CP15 assurance matrix. Minimized, attributable runtime evidence is exported through an independently protected path to ARC-P160. Acceptance tests define objective, precondition, exact evidence, thresholds, safe state, accountable reviewer, and retest trigger.

## Variants and alternatives

Approved variants are a central multi-protocol hub, durable workflow and event backbone, regional or sovereign cells, a high-assurance dedicated cell, an edge or intermittently connected cell, a thin synchronous service, and an external managed integration service. Variants may combine or externally supply components only when responsibility, evidence, failure dependency, accountability, control-point outcomes, safe-state behavior, and changed flows remain explicit. Another primary pattern is preferred when the dominant capability is a managed copilot, retrieval, agency, private-model lifecycle, shared gateway, or independent assurance rather than reusable deterministic integration.

## Anti-patterns

Anti-patterns include raw provider proxies, generic execute-anything endpoints, hidden adapter authority, caller- or model-selected destinations, silent schema downgrade, cross-tenant shared state, unbounded queues or retries, blind retry after unknown outcomes, transport success represented as business success, observability used as an action interface, and retirement that leaves credentials, routes, jobs, callbacks, subscriptions, results, exports, or provider data active.

## Related patterns

- `ARC-P100` owns shared model and provider registry, inference routing, credentials, provider policy, and gateway enforcement.
- `ARC-P110` owns managed workforce interaction, disclosure, confirmation, feedback, and accessibility.
- `ARC-P120` owns source admission, retrieval authorization, indexing, grounding, citation, and knowledge lifecycle.
- `ARC-P130` owns AI-selected tools or targets, expanded authority, autonomous planning, consequential action, approval, containment, and outcome assurance.
- `ARC-P140` owns private model acquisition, adaptation, release, custody, serving, and revocation.
- `ARC-P160` owns authoritative evidence custody, evaluation, detection, response, and independent assurance.

## Change history

| Pattern version | ESAF release | Date | Change |
|---|---|---|---|
| 0.1.0 | 0.4-alpha | 2026-07-11 | Initial draft |
