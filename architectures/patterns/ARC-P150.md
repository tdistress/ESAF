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

### Figure 1. Context and pattern relationships

```mermaid
flowchart LR
  C["Consumers: applications, workloads, channels"] --> F["ARC-P150 federated integration fabric"]
  F --> P["External providers and managed AI services"]
  F --> T["Enterprise targets, tools, data, and callbacks"]
  F --> G["ARC-P100 gateway, provider policy, and inference routing"]
  F --> R["ARC-P120 retrieval and knowledge handoff"]
  F --> A["ARC-P130 agency and consequential-action handoff"]
  F --> M["ARC-P140 private-model serving handoff"]
  F -. "evidence export" .-> E["ARC-P160 independent evidence and assurance"]
```

ARC-P150 owns stable service contracts, admission, deterministic dispatch, interaction-mode delivery, state, and reconciliation. Consumers retain business-purpose and output-use accountability; providers and enterprise targets retain their native authorization and outcome authority; the named supporting patterns retain their defined responsibilities.

### Figure 2. Federated topology

```mermaid
flowchart TB
  S["Shared control plane: policy administration and signed configuration"]
  B["Global bootstrap and execution-cell discovery"]
  P["Federated policy decision service"]
  C1["Execution cell A: regional or domain runtime"]
  C2["Execution cell B: failover-eligible runtime"]
  U["Consumer"]
  S -- "signed configuration, trust updates, and revocation distribution" --> C1
  S -- "signed configuration, trust updates, and revocation distribution" --> C2
  U --> B
  B -- "short-lived route assertion" --> U
  B -- "route assertion notice" --> C1
  U -- "endpoint authentication then content" --> C1
  C1 -- "federated policy decision" --> P
  C2 -- "federated policy decision" --> P
  C1 -- "contract-authorized state transfer and resumption" --> C2
  C1 -. "runtime posture and failover eligibility" .-> B
  C2 -. "runtime posture and failover eligibility" .-> B
```

The shared control plane is not a mandatory application-content path. Global discovery selects only registered cells from server-derived region, domain, tenant, capability, capacity, locality, continuity, and policy context. The consumer verifies the purpose-, audience-, tenant-, capability-, region-, endpoint-, version-, expiry-, and nonce-bound route assertion and authenticates the selected cell endpoint before releasing credentials or content. Each cell then authenticates the consumer, verifies its own current runtime posture, and performs local admission. Expired, forged, inconsistent, revoked, or nonconformant cells are quarantined and excluded from new work, secret use, and failover.

### Figure 3. Six-plane component view

```mermaid
flowchart TB
  G["Governance and contract plane: registries, schemas, modes, lifecycle"]
  A["Admission and policy plane: identity, purpose, policy-enforcement point"]
  X["Execution and adapter plane: contract validator, dispatch, adapters"]
  D["Durable delivery and state plane: durable state, queues, idempotency"]
  O["Output and delivery plane: output validator and delivery controller"]
  G --> A --> X --> D --> O
  X --> O
  subgraph OPS["Operations, administration, and evidence plane"]
    direction LR
    AD["Operations and administration subplane: privileged interface and trust root"]
    EV["Evidence export subplane: one-way constrained interface and independent trust root"]
  end
  AD -. "configuration, continuity, containment" .-> G
  AD -. "separately protected administration" .-> A
  A -. "minimized event" .-> EV
  X -. "minimized event" .-> EV
  D -. "minimized event" .-> EV
  O -. "minimized event" .-> EV
```

The logical planes may be deployed in different services, but their decisions and retained responsibilities remain distinct. The administration and evidence-export subplanes use different identities, interfaces, trust roots, authorization, stores, administrators, and failure dependencies. Evidence access grants no configuration, secret, replay, suspension, or workload authority, and runtime administrators cannot alter authoritative ARC-P160 evidence.

### Figure 4. Normative flow

```mermaid
sequenceDiagram
  participant C as Consumer
  participant B as Global bootstrap
  participant A as Local admission and policy-enforcement point
  participant V as Contract validator
  participant D as Durable state and deterministic dispatcher
  participant S as ARC-P100 / ARC-P120 / ARC-P130 / ARC-P140 handoff
  participant O as Output validator and delivery
  participant E as ARC-P160 evidence export
  C->>B: Bootstrap with non-content routing context
  B-->>C: Signed route assertion
  C->>A: Authenticate selected endpoint and present invocation
  A->>A: Endpoint authentication and local admission
  A->>V: Authorized canonical envelope
  V->>D: Valid contract; durable acceptance when required
  D->>S: Deterministic dispatch and supporting-pattern handoff
  S-->>D: Result or explicit unknown outcome
  D->>D: Conditional reconciliation until claim is supportable
  D->>O: Candidate result and authoritative state
  O-->>C: Validated, authorized, mode-specific delivery
  A-->>E: Admission and authorization evidence
  V-->>E: Validation evidence
  D-->>E: Acceptance, dispatch, transition, failure, and recovery evidence
  O-->>E: Delivery and reconciliation evidence
```

Evidence is cross-cutting from admission through recovery, not a terminal logging step. Authorization is current at every applicable durable, delivery, or consequential step, and no later transport or business result retroactively justifies an earlier decision.

### Figure 5. State and durable-delivery view

```mermaid
flowchart LR
  I["Queue, event, stream, batch, or callback intake"] --> T["Transport authority: accepted, delivered, duplicated, expired"]
  T --> S["Service-execution authority: queued, running, cancelled, failed"]
  S --> R["Result-delivery authority: withheld, partial, released, acknowledged"]
  S --> X["Target-transaction authority: committed, rejected, unknown outcome"]
  X --> B["Business-outcome authority: verified by owning system"]
  T --> D["Durable state: idempotency, deduplication, sequence, checkpoint"]
  S --> D
  R --> D
  X -- "unknown outcome" --> Q["Reconciliation against authoritative target"]
  Q --> X
  D -- "bounded retry only when safe" --> T
```

Transport, service execution, result delivery, target transaction, and business outcome are separate state authorities. At-least-once queue and event delivery, stream resume, batch manifests, and callback retries require tenant-bound idempotency and deduplication. An acknowledgment or successful transport never proves target commit or business outcome; unknown state is recorded and reconciled before a success claim or retry that could duplicate an effect.

### Figure 6. Degraded operation and recovery

```mermaid
flowchart TB
  B["Signed cached bundle: policy, contracts, routes, revocations"] --> V["Trusted time, signature, freshness, and anti-rollback validation"]
  V -- "fresh and applicable" --> L["Bounded local operation"]
  E["Restriction-only emergency path"] --> L
  V -- "expired, revoked, forged, or rollback" --> S["Tier 3/4 stop or consequential commit block"]
  L --> R["Reconnect validation: current identity, posture, policy, dependencies"]
  S --> R
  R --> Q["Reconciliation of queued, partial, failed, and unknown state"]
  Q --> A["Authorized resumption and evidence export"]
```

Disconnected operation cannot add routes, providers, credentials, exceptions, scope, or authority. Emergency changes may only restrict operation. Higher-risk work stops, or blocks immediately before commit, when current trust, required evidence, trusted time, capacity, or reconciliation authority is unavailable. Reconnect does not imply recovery: current validation and reconciliation precede authorized resumption.

### Figure 7. Retirement

```mermaid
flowchart LR
  D["Drain or cancel requests, jobs, streams, batches, and deliveries"] --> U["Resolve unknown state and reconcile external effects"]
  U --> R["Revoke identities, routes, subscriptions, callbacks, and secrets"]
  R --> X["Dispose data, durable state, caches, results, backups, and exports"]
  X --> P["Provider exit: delete copies, revoke access, close obligations"]
  P --> E["Preserve required evidence and legal-hold records"]
  E --> T["Residual-access test across runtime, support, restore, and provider paths"]
```

Retirement is complete only after disposition is recorded for in-flight work and every replica, credential, route, subscription, callback, result, provider copy, support path, and restoration path. Preserved evidence remains protected and attributable without preserving unnecessary workload content.

## Actors and identities

Human users and approvers, consumer applications, workload instances, execution cells, integration services, adapters, providers, brokers, callback senders and receivers, enterprise targets, support personnel, administrators, emergency operators, configuration approvers, signers, trust-root administrators, distributors, and evidence services shall have distinct, inventoried, owned, authenticated, scoped, rotated, revoked, and evidenced identities. Shared integration credentials are prohibited except under a documented legacy exception with equivalent attribution and isolation.

Delegation and token exchange cannot increase scope, audience, lifetime, impersonation, purpose, tenant, provider, model, data, tool, target, operation, or administrative authority. Authorization is re-evaluated at admission, durable acceptance, dequeue, dispatch, batch and per-item execution or delivery, stream frame or partial-result release, event publication, subscription and callback delivery, result release, replay or backfill, and immediately before consequential commit as applicable. Long-lived work uses bounded authorization leases with periodic and event-driven revalidation.

Provider and target credentials remain outside requests, prompts, events, files, logs, traces, dead-letter records, and model context. They are scoped to provider or target, capability, tenant or approved sharing context, environment, purpose, operation, and lifetime. Policy approval, configuration signing, trust-root administration, distribution, runtime administration, evidence custody, and emergency action are separated; higher tiers use dual or threshold control where required. Administrative and emergency credentials use separate privileged workflows, automatic expiry, and review.

## Data and instruction flows

Every interaction shall use a versioned canonical contract that binds authoritative identity, tenant, capability, purpose, operation, classification, provenance, residency, retention, correlation, causation, deadlines, budgets, and mode-specific state. Data, instructions, provider responses, callback content, metadata, and model output remain untrusted and cannot become policy, route, target, command, credential reference, or authorization.

## Trust boundaries

Each material crossing records the following minimum allocation. Deployment records add concrete endpoints, owners, data classes, residency, retention, thresholds, and approved exceptions.

| Direction and purpose | Identities | Authorization | Information | Validation | Protection | Evidence | Reliability | Retained responsibility |
|---|---|---|---|---|---|---|---|---|
| Consumer -> global bootstrap: cell discovery | Consumer workload; bootstrap service | Registered tenant, capability, purpose, and allowed region; no content authority | Non-content tenant, capability, locality, continuity context | Authenticate caller; derive server-side context; reject replay | TLS; minimized metadata; no provider credentials | Request, decision, eligible-set version | Short deadline; no silent fallback | Consumer retains invocation purpose; bootstrap owns registered-cell selection only |
| Bootstrap -> consumer and selected cell: signed routing | Bootstrap signer; consumer; cell | Purpose-, audience-, tenant-, capability-, region-, endpoint-bound route | Route assertion, version, expiry, nonce, selected endpoint | Verify issuer, signature, time, replay defense, consumer verification, endpoint identity | Purpose-bound signing keys; short lifetime | Assertion, issuer, verification, endpoint | Expiry and retry bounds; fail closed | Consumer authenticates selected cell; cell repeats local admission |
| Shared control plane -> cell: distribution | Publisher; distributor; execution-cell workload | Approved signer, artifact purpose, cell applicability, revocation epoch | Signed contracts, policy, routes, trust updates, revocations, restrictions | Signature, configuration identity, version, freshness, revocation, anti-rollback, split-brain | HSM-equivalent custody; encrypted channel and store; separation of duties | Approval, signature, receipt, activation, rejection | Bounded propagation; stale or conflicting state quarantines cell | Shared plane owns approved artifacts; cell owns verify-before-use |
| Cell -> federated PDP: policy decision | Cell workload; PDP service | Registered cell may request only contract-defined decisions | Bound identity, tenant, purpose, capability, operation, classification, policy version | Mutual authentication; schema, freshness, context, decision integrity | Encrypted channel; minimized attributes; no credential forwarding | Request correlation, policy version, decision, expiry | Deadline; cached decisions only when explicitly permitted | Cell retains enforcement and safe-state responsibility |
| Source cell -> destination cell: failover or resumption | Source and destination cell workloads; transfer controller | Contract-defined eligible cells, state classes, and resumption authority | Tenant-bound state, manifest, checkpoint, idempotency and reconciliation status | Both cell postures, route assertion, integrity, freshness, completeness, unknown-state check | Encrypted transfer; tenant isolation; immutable manifest | Initiator, approvals, state hash, acceptance, outcome | Ordered checkpoint; no resumption on partial transfer | Source owns transfer truth; destination reauthorizes and reconciles before execution |
| Z1 consumer -> Z2 cell: admission | Consumer and workload; cell ingress | Current identity, delegation, purpose, capability, contract, limits | Canonical invocation envelope and untrusted content | Endpoint and consumer authentication; delegation, schema, provenance, classification, replay | TLS; tenant isolation; bounded buffers; secret exclusion | Admission, policy, validation, denial | Deadline, quota, rate and capacity bounds | Consumer retains input and use accountability; cell owns admission |
| Z2 admission -> Z3 execution: dispatch | Policy-enforcement point; service runtime; adapter | Explicit operation, contract, policy, provider or target constraints | Canonical envelope, decision, expiry, correlation, budgets | Decision freshness, contract version, adapter allowlist, cell posture | Workload identity; scoped secrets client; isolated state | Decision, dispatcher, adapter, transition | Bounded queue, retry, cancellation and expiry | Dispatcher cannot broaden authorization; runtime owns deterministic execution |
| Z2/Z3 -> Z4 inference | Cell service or adapter; ARC-P100 enforcement point; provider | Approved model/provider route, data class, purpose and budget | Minimized inference request, policy context, correlation | Contract and content checks; ARC-P100 routing and provider controls | Scoped provider credential outside content; encryption and tenant isolation | Request lineage, route, model, provider, result status | Timeout, rate, retry only when safe; unknown status explicit | ARC-P100 owns inference routing; cell owns service contract and outcome interpretation |
| Z2/Z3 -> Z5 retrieval | Cell service; ARC-P120 retrieval service | Approved sources, tenant, purpose, query and result scope | Query, classification, provenance requirements, correlation | Source admission, retrieval authorization, grounding and citation checks | Scoped workload identity; minimized query; residency enforcement | Query lineage, sources, policy, retrieval result | Timeout, freshness and partial-result policy | ARC-P120 owns knowledge lifecycle; cell owns service delivery |
| Z2/Z3 -> Z6 tool or target | Cell service or ARC-P130 agent; target identity | Pre-authorized deterministic operation, or ARC-P130 lease and approval | Typed command, bounded parameters, idempotency key, correlation | Target-native authorization; schema; current commit authorization; output validation | Target-scoped credential; encrypted channel; no model-derived authority | Request, target decision, transaction state, reconciliation | Bounded retry; unknown outcomes block blind replay | Target owns transaction truth; ARC-P130 owns AI-selected action; consumer owns business outcome |
| Z0 callback/event -> Z2 cell | Provider, callback sender, event source; cell broker | Registered source, event type, tenant, subscription, window | Untrusted callback or event, source ID, sequence, signature | Source authentication, signature, schema, freshness, replay, tenant binding | Dedicated ingress; rate limits; quarantine; secret-safe dead letter | Source, receipt, duplicate, disposition | At-least-once handling; deduplicate and order per contract | Sender owns event assertion; cell owns admission and processing |
| Z2/Z3 -> Z0 callback destination | Delivery controller; registered callback receiver | Current registration, tenant, event type, destination and delivery lease | Validated minimized result, labels, correlation, delivery ID | Destination authentication; output policy; registration and lease freshness | Destination-scoped credential; encryption; no sensitive query-string data | Attempt, receipt, retry, expiry, terminal status | Bounded retry, idempotency, dead-letter quarantine | Receiver owns business processing; cell owns delivery state only |
| Execution cell -> broker/queue | Cell workload; broker identity; worker | Tenant, topic or queue, operation, retention, producer and consumer scope | Canonical job/event, state reference, sequence, expiry | Broker ACL, schema, integrity, tenant, duplicate and poison-message checks | Encryption; isolated topics and stores; scoped credentials | Publish, durable receipt, dequeue, ack, quarantine | At-least-once; capacity, ordering, timeout, retry and expiry bounds | Broker owns transport state; cell owns service and reconciliation state |
| Z2/Z3 -> Z7 evidence | Runtime component; evidence exporter; ARC-P160 collector | One-way or equivalently constrained event submission only | Minimized attributable events, decisions, gaps, outcomes, timestamps | Source identity, schema, correlation, tenant, integrity, occurrence and receipt time | Separate trust root, interface, store, identity and failure dependency | Durable receipt, sequence, gap and backfill status | Bounded buffer/backfill; Tier 3/4 safe stop on required-evidence loss | ARC-P160 owns authoritative custody; runtime cannot alter accepted evidence |
| Z7 -> Z2/Z3 administration and containment | Named administrator or containment service; cell admin endpoint | Separate privileged workflow, approved change, bounded scope and expiry | Signed configuration command, suspension, recovery or restriction | Strong authentication; dual control where required; target and change validation | Separate administration path, credentials, trust root and audit store | Request, approval, command, acknowledgment, effect, rollback | Restriction-first failure; timeout and recovery procedure | Administrators cannot rewrite evidence or create unmonitored replay/workload paths |

Queue storage and delivery remain logical boundaries even when physically co-located, and contracted external services remain external. Global cell discovery is distinct from cell-local capability discovery: the latter may resolve only services allowed by the verified routing assertion and cannot register or select a cell, weaken a contract, or expand authority. Operations and evidence paths are separately protected from workload paths and from each other.

## Components and responsibilities

The **governance and contract plane** maintains service and consumer registries; ownership and purpose; versioned contracts, canonicalization, schemas, events, callbacks, and subscriptions; allowed interaction modes; classifications, residency, dependencies, SLOs, quotas, compatibility, deprecation, exceptions, review state, cell conformance, and signed configuration history.

The **admission and policy plane** provides global bootstrap and registered-cell discovery, cell ingress, endpoint and consumer authentication, delegation verification, identity and tenant derivation, purpose and capability binding, policy enforcement, limit and replay control, classification and provenance checks, approved contract resolution, route-assertion verification, selected-cell endpoint authentication, runtime cell-posture verification, and failover exclusion. Global discovery does not carry application content; cell-local capability discovery cannot expand the global routing assertion.

The **execution and adapter plane** contains the contract validator and canonicalizer, dispatcher, bounded deterministic service runtime, protocol adapters, and secrets client. Adapters preserve identity, purpose, tenant, classification, provenance, expiry, policy version, and correlation and cannot hide provider routing, business authorization, agent planning, target authority, or credential selection. ARC-P100 governs shared inference admission, routing, provider policy, and credentials; ARC-P120 governs retrieval; ARC-P130 governs AI-selected tools, targets, parameters, and consequential action; ARC-P140 governs enterprise-operated model lifecycle and serving.

The **durable delivery and state plane** provides durable job and idempotency stores, queue and event adapters, stream relays, batch coordinators and immutable manifests, callback and subscription brokers, deduplication, sequencing, checkpointing, cancellation, result expiry, dead-letter quarantine, explicit unknown-outcome handling, and authoritative reconciliation. It keeps transport, service execution, result delivery, target transaction, and business outcome separate and never claims exactly-once business effects from transport behavior.

The **output and delivery plane** contains the output validator and delivery controller. It validates, classifies, labels, minimizes, and authorizes outputs before synchronous response, stream or partial-result release, persistence, event publication, batch export, callback delivery, or downstream machine use. It preserves per-item and partial status and blocks delivery until every reconciliation required by the claimed result is complete.

The **operations, administration, and evidence plane** contains explicitly isolated operations-and-administration and evidence-export subplanes. Operations provides separately protected configuration, secrets, privileged administration, capacity, continuity, emergency suspension, recovery, compatibility and conformance testing, and provider-gap handling. Evidence export uses a one-way or equivalently constrained path to send minimized attributable admission-through-recovery events to ARC-P160. The two subplanes have distinct identities, interfaces, trust roots, authorization, stores, administrators, and failure dependencies; evidence access cannot confer configuration, secret, replay, suspension, or workload authority, and operations administrators cannot alter authoritative evidence.

Each regional or domain execution cell has a unique workload identity, accountable owner, region or domain, approved protocol profile, software and configuration identity, current conformance evidence, capacity limits, lifecycle state, and freshness-bounded runtime attestation or equivalent release-closure posture. The shared control plane distributes signed, versioned, bounded-lifetime configuration and restrictions but need not process application content. Cells verify identity, signature, purpose, version, freshness, revocation epoch, applicability, trusted time, and anti-rollback state before use and cannot create registrations, invent exceptions, silently downgrade versions, or retain failover eligibility after posture becomes invalid.

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
