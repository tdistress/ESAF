# ARC-P150 AI Integration Services Design

**Status:** Approved design draft

**Date:** 2026-07-12

## 1. Purpose

ARC-P150 defines a governed, reusable integration boundary for embedding AI capabilities into enterprise applications. It standardizes stable capability-level contracts, identity and policy propagation, deterministic service dispatch, protocol adaptation, delivery semantics, state, compatibility, resilience, evidence, and lifecycle across synchronous, asynchronous, streaming, batch, event or subscription, and callback interactions.

The pattern prevents consuming applications from integrating directly and inconsistently with model providers, private inference, enterprise knowledge, tools, targets, or external AI services.

## 2. Design decision

ARC-P150 uses a **contract-first federated integration fabric**:

- a shared governance and control plane maintains service and consumer registrations, schemas and contracts, policy metadata, execution-cell conformance, compatibility, callback and subscription registrations, lifecycle state, and signed configuration; and
- regional or domain execution cells enforce those contracts and provide protocol, delivery, state, isolation, resilience, and evidence functions without creating one mandatory enterprise data path.

The central-hub and durable-workflow-backbone models remain approved variants. The baseline does not centralize all application traffic or make a workflow engine authoritative for business purpose or permission.

Durable work assumes at-least-once transport with idempotency, deduplication, bounded retry, explicit unknown outcomes, and authoritative reconciliation. ARC-P150 never claims exactly-once business effects from transport behavior.

## 3. Scope and responsibility boundary

ARC-P150 owns:

- reusable, versioned AI service and consumer contracts;
- synchronous, asynchronous job, streaming, batch, event or subscription, and callback semantics;
- canonical envelopes, protocol adaptation, schema validation, correlation, causation, ordering, idempotency, cancellation, result delivery, and reconciliation;
- consumer, producer, execution-cell, adapter, provider, and target responsibility boundaries;
- bounded integration state, compatibility, deprecation, portability, suspension, and retirement; and
- integration evidence emitted to ARC-P160.

Adjacent patterns retain their authority:

- `ARC-P100` owns shared model and provider registry, inference routing, credentials, provider policy, and gateway enforcement.
- `ARC-P110` owns the managed workforce interaction shell, disclosure, session experience, confirmation, feedback, and accessibility.
- `ARC-P120` owns source admission, retrieval authorization, indexing, grounding, citation, and knowledge lifecycle.
- `ARC-P130` owns AI-selected tools or targets, delegated or expanded authority, autonomous planning, consequential action, approval, transaction, containment, and outcome assurance.
- `ARC-P140` owns private model acquisition, adaptation, release, custody, serving, and revocation.
- `ARC-P160` owns authoritative evidence custody, evaluation, detection, response, and independent assurance.

ARC-P150 may execute deterministic, pre-authorized service workflows. ARC-P130 becomes mandatory when AI selects a tool, target, operation, or action parameters that determine material effect; delegates or expands authority; or initiates consequential action. A transport or adapter cannot convert model output, prompt content, an agent lease, or an MCP discovery result into authority.

The consuming capability remains accountable for business purpose, use-case authorization, human oversight, output use, and downstream effects.

## 4. Intended outcomes

ARC-P150 shall:

- expose stable service contracts instead of raw provider-specific interfaces;
- preserve authoritative identity, tenant, purpose, classification, provenance, policy, and correlation across every hop;
- provide consistent delivery semantics for all six interaction modes;
- isolate consumer, tenant, job, stream, batch, callback, cache, queue, result, and support state;
- prevent adapters from broadening data access, provider choice, target scope, action authority, or credential use;
- distinguish transport, execution, inference, target, and business outcomes;
- support regional isolation, data locality, independent scaling, bounded degradation, and controlled recovery;
- make compatibility, portability, deprecation, and retirement testable; and
- provide independently assessable evidence without copying sensitive content unnecessarily.

## 5. Non-goals

ARC-P150 does not define a universal enterprise service bus, raw provider proxy, generic arbitrary-execution API, business-specific workflow, AI gateway replacement, RAG ingestion shortcut, agent authorization service, MCP trust proxy, model-management interface, or authoritative observability store.

It does not replace conventional API management, service mesh, messaging, workflow, ETL, transaction, software supply-chain, or target-native authorization controls. It does not assert that delivery success proves output correctness or business completion.

## 6. Architecture model

The pattern contains six logical planes.

### 6.1 Governance and contract plane

Maintains service and consumer registries; ownership and purpose; contract, schema, canonicalization, and event definitions; allowed interaction modes; data classes and residency; dependencies; SLOs; quotas; compatibility and deprecation policy; provider and target responsibility; cell conformance; callback and subscription registrations; exceptions; review state; and signed configuration history.

### 6.2 Admission and policy plane

Authenticates consumers and workloads, derives authoritative identity and tenant context, validates delegation, binds purpose and capability, resolves the approved service and contract version, evaluates policy, applies limits, validates classification and provenance, rejects replay, and selects an approved execution cell.

### 6.3 Execution and adapter plane

Runs bounded deterministic service logic and approved protocol adapters. Inference access implements ARC-P100 outcomes through an approved centralized or federated enforcement point for shared admission, policy, routing, and provider controls; ARC-P140 applies additionally when the model lifecycle or serving runtime is enterprise-operated. It invokes ARC-P120 for semantic retrieval and ARC-P130 when agency or consequential action is present. Adapters preserve identity, purpose, classification, provenance, expiry, policy version, and correlation and cannot contain hidden provider routing, business authorization, agent planning, or target authority.

### 6.4 Durable delivery and state plane

Provides job state, queues and event adapters, stream relays, batch coordination, callback and subscription delivery, immutable manifests, idempotency, deduplication, sequencing, checkpointing, cancellation, result expiry, dead-letter quarantine, unknown-outcome handling, and reconciliation.

### 6.5 Output and delivery plane

Validates, classifies, labels, minimizes, and authorizes outputs before synchronous response, stream release, persistence, event publication, batch export, callback delivery, or downstream machine use. It preserves per-item and partial-result status and blocks unsafe or unauthorized delivery.

### 6.6 Operations, administration, and evidence plane

Contains two explicitly isolated subplanes. The **operations and administration subplane** provides configuration, secrets, privileged administration, capacity, continuity, emergency suspension, recovery, conformance testing, compatibility testing, and provider gap handling. The **evidence-export subplane** accepts one-way or equivalently constrained runtime events and exports minimized events to ARC-P160. The subplanes use distinct identities, interfaces, trust roots, authorization, stores, administrators, and failure dependencies. Evidence access cannot confer configuration, secret, replay, suspension, or workload authority; cell and control-plane administrators cannot alter authoritative ARC-P160 evidence. Operational dashboards and transport logs are not authoritative business-outcome evidence.

## 7. Shared control plane and federated execution cells

The shared control plane is a policy-administration and configuration-distribution plane, not a mandatory request path. It distributes signed, versioned, bounded-lifetime contracts, policy, routes, callback registrations, compatibility state, revocations, and emergency restrictions. Every execution cell has a unique workload identity, accountable owner, region or domain, approved protocol profile, software and configuration identity, current conformance evidence, capacity limits, and lifecycle state.

Cells host the runtime ingress, policy-enforcement points, contract validation, dispatch, delivery, and output enforcement needed for their approved modes. An approved global bootstrap and cell-discovery service uses signed routing metadata and server-derived region, domain, tenant, and capability context to direct the consumer to a cell without carrying application content through the shared control plane. The routing assertion is purpose-bound, audience-bound, tenant-bound, capability-bound, region-bound, endpoint-bound, versioned, short-lived, and replay-resistant. The consumer verifies the assertion and the selected cell's authenticated endpoint identity before releasing credentials or application content. The selected cell authenticates the consumer and performs local policy enforcement using current signed policy or an approved federated policy-decision service. Failover ownership, eligible cells, health inputs, policy constraints, state transfer, and resumption authority are defined by the service contract and enforced at the cell boundary.

Cells shall verify configuration identity, signature, purpose, version, freshness, revocation, and applicability before use. Each cell also proves an approved deployment and workload identity through runtime attestation or an equivalent release-closure and posture mechanism bound to its workload credentials. Trust is freshness-bounded and clone- and replay-resistant; a cell with expired, forged, inconsistent, or revoked posture is quarantined, loses new-work and secret-use authority, and cannot be selected for failover. Cells preserve regional, tenant, classification, and provider constraints and emit common evidence. They cannot create local service or consumer registrations, weaken a contract, silently select an unapproved version, or invent an exception.

Configuration-signing trust is governed separately from configuration storage and distribution. Requirements cover authorized issuers and signers; HSM or equivalent key custody; purpose-bound keys; separation of policy approval, signing, trust-root administration, distribution, and runtime administration; threshold or dual control for higher tiers; algorithm agility; trusted-time evidence; rotation overlap; signer and trust-root revocation; compromise response; emergency re-signing; and rejection of artifacts signed before or after a compromise according to the approved revocation epoch. Cells detect forged, wrong-purpose, stale-trust, downgraded-algorithm, replayed, split-brain, and rollback configurations.

Cell routing is separate from ARC-P100 model routing. A service may select an approved cell based on region, locality, capacity, continuity, and contract, but provider or model selection remains governed by the applicable inference pattern.

### 7.1 Minimum logical components and flow

The shared plane contains the service and consumer registry; contract, schema, event, callback, and subscription registry; policy administration; signed configuration publisher; cell registry and conformance service; compatibility and deprecation service; and emergency-control authority.

Each cell contains an approved ingress and cell-local service or capability discovery endpoint; authentication and delegation verifier; policy-enforcement point; contract and canonicalization validator; dispatcher; deterministic service runtime; protocol adapters; durable job and idempotency store; queue and event adapter; stream relay; batch coordinator and manifest store; callback and subscription broker; output validator and delivery controller; secrets client; administrative endpoint; and evidence exporter. Cell-local discovery does not replace the global bootstrap and cell-discovery service and cannot select an unregistered cell or expand a routing assertion.

The normative execution path is: global bootstrap and cell selection; mutual endpoint and consumer authentication; cell-local admission; contract and envelope validation; durable acceptance when required; deterministic dispatch; applicable ARC-P100, ARC-P120, ARC-P130, ARC-P140, provider, or target handoff; output validation; conditional or iterative reconciliation whenever a target, provider, unknown state, or evidence gap can affect the claimed result; and mode-specific delivery. A result cannot be represented or delivered as successful until every reconciliation on which that claim depends is complete. Independent evidence export is a cross-cutting path at admission, authorization, validation, acceptance, dispatch, transition, failure, delivery, reconciliation, configuration change, and recovery rather than a terminal flow step. No step may use a later transport or business result to retroactively justify an earlier authorization decision.

## 8. Canonical invocation envelope

Every invocation has a typed **base envelope** containing:

- server-validated consumer and workload identity;
- user identity and explicit delegation where applicable;
- tenant, capability, purpose, operation, service version, contract version, and interaction mode;
- data and instruction classification, provenance, residency, retention, and permitted-use attributes;
- correlation ID, causation ID, server-issued request ID, deadline or explicit no-deadline prohibition, expiry, budgets, limits, requested response contract, and trace context.

Mode extensions are versioned parts of the same contract. Durable submission requires job ID and idempotency key; streaming requires stream ID, sequence scope, frame identity, and resume policy; batch requires manifest and item identity; events require immutable event ID, deduplication scope, producer-stream or partition sequence, subject, and retention policy; and callbacks or subscriptions require a registered destination or subscription reference and allowed event types. The contract marks each field required, optional, prohibited, server-issued, consumer-supplied, or derived for each operation and mode.

Caller-provided identity, tenant, purpose, role, classification, correlation, callback, or authorization fields are untrusted claims until bound to authenticated context and policy. Canonicalization rules cover duplicate keys, ambiguous encodings, polymorphism, numeric limits, unknown fields, content types, normalization, signatures, and hash calculation.

## 9. Interaction-mode contracts

### 9.1 Synchronous request and response

The contract defines bounded payload, deadline budget across every hop, cancellation intent, resource and cost limits, idempotency classification, retry eligibility, response schema, secure error behavior, and terminal status. A timeout is unknown unless authoritative service or target state proves failure or success. Failover preserves provider, model, region, residency, retention, training-use, safety, behavior, and assurance constraints.

### 9.2 Asynchronous jobs and queues

Durable acceptance atomically records a server-issued job ID, immutable request or digest, identity, tenant, purpose, contract and policy version, authorization basis, idempotency key, expiry, budgets, input references, callback and result policy, and correlation. Authorization to submit, execute, cancel, inspect status, read results, replay, or administer is distinct and re-evaluated at the applicable step.

Job execution states include accepted, queued, running, succeeded, failed, canceled, expired, and unknown. They do not contain target-transaction or business-outcome claims. Dequeue and redispatch require current authorization and revocation checks. Dead-letter replay is a new governed operation rather than an automatic continuation.

### 9.3 Streaming

Streams authenticate the session and validate every frame or chunk. Each frame binds stream, sequence, tenant, capability, contract, and classification. Controls bound buffers, backpressure, idle and total duration, frame and message size, rate, cost, fair use, cancellation, reconnect, and resume-token use.

A disconnect does not prove cancellation or failure. Partial output is labeled and cannot cross a delivery boundary before the validation required by its structure, content, sensitivity, and downstream use. The service detects truncation, injection, replay, reordering, cross-stream mixing, slow-consumer exhaustion, and resume-token theft.

Stream authorization uses a bounded lease. It is revalidated periodically and upon identity, tenant, purpose, classification, policy, contract, route, provider, model, revocation, risk, or destination change and before release of a frame whose authorization basis changed. Expired or revoked leases stop new execution and delivery, quarantine or discard queued frames according to contract, invalidate resume authorization, and require a new authenticated admission. The stop, redaction, queued-frame disposition, reconnect decision, and evidence are explicit.

### 9.4 Batch and file processing

A versioned batch manifest binds input snapshot or digest, source, item count, per-item identity, tenant, classification, schema, region, expiry, output destination, and partial-success policy. Every item is authorized and validated; batch-envelope authorization is insufficient.

Mixed-tenant or mixed-classification batches are prohibited unless isolation and evidence are independently demonstrated. Controls cover archive, formula, path, active-content, parser, decompression, malformed-item, temporary-file, staging, checkpoint, restart, export, and deletion risks. Aggregate success cannot hide unauthorized, quarantined, failed, or unknown items.

Long-running batches use bounded authorization leases at batch and item scope. Authorization is revalidated periodically, on material identity, tenant, purpose, classification, policy, contract, route, provider, model, target, region, destination, or revocation change, and before item execution and result delivery. Expired or revoked authority stops or quarantines affected items according to contract and cannot be hidden by aggregate batch status.

### 9.5 Events and subscriptions

Every event uses a versioned envelope with immutable event ID and deduplication scope; authenticated producer; purpose, provenance, classification, schema, tenant, correlation, causation, trusted or bounded time, expiry, and integrity; and sequence scoped explicitly to a producer stream, partition, subject, or subscription rather than a global order. Contracts define gap detection, wait, skip, quarantine, backfill, and reconciliation behavior. Duplicate, replayed, out-of-order, late, conflicting, expired, and poison events are detected and dispositioned. Event content, topic, headers, queue metadata, and correlation identifiers never confer authority.

Authorization is distinct for publish, topic discovery, subscribe, consume, acknowledge, checkpoint, replay, backfill, consumer-group membership, retained-event access, wildcard or pattern subscription, and topic or subscription administration. Subscriptions use bounded authorization leases with periodic and event-driven revalidation. Revocation stops new delivery, prevents backlog and retained-event access, invalidates replay and checkpoint authority, governs queued events, and records consumer-group and wildcard changes.

### 9.6 Callbacks and webhooks

Callback destinations and event types are pre-registered, ownership-verified, tenant-bound, purpose-bound, classification-approved, and assigned an internal or external destination class. Request-selected or model-generated callback URLs are prohibited. Arbitrary and private-address destinations are denied by default. Registered internal enterprise destinations may use approved private addressing only through controlled name resolution, egress, routing, network policy, destination identity, and change monitoring. All delivery prevents SSRF, open redirect, DNS rebinding, credential forwarding, and unapproved cross-border or data-class transfer.

Inbound callbacks require authenticated transport and message-level signature, trusted-time window, nonce and replay cache, audience, content digest, provider and job binding, schema, expected state transition, and key-rotation handling. Callback-signing trust uses an approved key source, purpose- and algorithm-restricted keys scoped to provider and tenant, rotation overlap, compromise epochs, revocation, and explicit safe behavior when key-status or replay-cache services are unavailable. A callback signed before compromise but received after the applicable revocation epoch is rejected or quarantined under the approved incident rule. Retries and backoff are bounded. Callback acknowledgment is delivery evidence only; the authoritative job or target status governs business outcome.

## 10. Identity, authorization, and secrets

Human, service, workload, execution-cell, adapter, provider, broker, callback, target, and administrator identities are distinct, inventoried, owned, authenticated, scoped, rotated, revoked, and evidenced. Shared integration credentials are prohibited unless a documented legacy exception provides equivalent attribution and isolation.

Delegated token exchange cannot increase scope, audience, lifetime, impersonation, provider, model, data, tool, target, or administrative authority. Current authorization is evaluated at admission, durable acceptance, dequeue, dispatch, batch and per-item execution or delivery, stream frame or partial-result release, event publication and subscription delivery, callback delivery, result release, replay or backfill, and immediately before consequential commit as applicable. Long-lived streams, subscriptions, jobs, batches, and callbacks use bounded authorization leases with periodic and event-driven revalidation.

Provider and target credentials are stored outside requests, prompts, events, files, logs, traces, dead-letter records, and model context. They are scoped by provider or target, capability, tenant or approved sharing context, environment, purpose, operation, and lifetime. Administrative and emergency credentials use separate privileged workflows with automatic expiry and review.

## 11. Data, instruction, state, and tenant isolation

The fabric preserves data and instruction classification, provenance, purpose, authorization, residency, retention, deletion, legal hold, and output-use constraints across transformations. Untrusted data, callback text, tool errors, provider status, file contents, URLs, metadata, and model output cannot become system instruction, policy, route, target, query, command, credential reference, or authorization.

Isolation applies to request buffers, sessions, caches, idempotency records, job stores, queues, topics, streams, resume tokens, batch manifests, staging, temporary files, callbacks, result stores, dead-letter queues, exports, metrics, traces, tickets, backups, support access, and administrative tooling. Cache and coalescing keys bind tenant, identity or approved sharing scope, purpose, contract and policy version, classification, provider or target constraints, and lifecycle state.

Deletion, revocation, tenant offboarding, contract withdrawal, policy change, and retirement propagate to active streams, in-flight requests, queued work, batches, event backlogs, subscriptions, callbacks, caches, results, exports, backups, and provider-held copies according to documented obligations. The contract defines whether affected in-flight data is stopped, redacted, quarantined, discarded, reconciled, or preserved under legal hold and records the disposition.

## 12. Boundary-crossing records

Each material crossing records direction and purpose; initiating and receiving identity; authentication and delegation; requested operation and policy decision point; data, instructions, provenance, classification, and residency; schema, content, integrity, input, and output validation; encryption, secrets, session, tenant, and state safeguards; event source, correlation, decision, outcome, retention, and access; timeout, retry, idempotency, order, rate, capacity, and failure behavior; and provider, consumer, subprocessor, and inherited-control responsibility.

Required crossings include consumer to global bootstrap; bootstrap to consumer and selected cell for signed routing; shared control plane to cells for configuration, revocation, emergency restriction, and trust updates; cell to federated policy-decision service when used; source cell to destination cell for failover, resumption, or state transfer; Z1 to Z2 consumer admission; Z2 to Z3 dispatch; Z2 or Z3 to Z4 inference; Z2 or Z3 to Z5 data and retrieval; Z2 or Z3 to Z6 tools and targets; Z0 to Z2 provider callbacks or external events; Z2 or Z3 to Z0 callback destinations; execution cells to brokers and queues; Z2 or Z3 to Z7 evidence; and Z7 to Z2 or Z3 administration and containment. Bootstrap records include routing-assertion issuer, audience, tenant, capability, region, endpoint, version, expiry, nonce or equivalent replay defense, consumer verification, and selected-cell endpoint identity.

Queue storage and delivery remain a logical boundary even when physically co-located. External services remain external even when contracted. Z7 access cannot create an unmonitored replay or workload path.

## 13. Contract, schema, adapter, and dependency lifecycle

Services define owners, consumers, operations, side effects, interaction modes, schemas, examples, canonicalization, classifications, dependencies, providers, targets, limits, SLOs, support dates, compatibility, deprecation, migration, suspension, and retirement.

Breaking and non-breaking change rules are explicit and tested in both producer and consumer directions. Unknown fields, version fallback, schema downgrade, content-type change, SDK or connector behavior change, and provider response drift cannot be accepted silently. Signed configuration, staged rollout, rollback, consumer notification, compatibility windows, and emergency blocking are required.

Adapters and dependencies have approved identity, source, version, integrity, vulnerability, license, support, configuration, credential, endpoint, serialization, logging, retry, and retirement records. A connector or SDK update that changes endpoints, retention, training use, residency, authentication, serialization, retry, logging, output, or error behavior triggers review and compatibility testing.

Each protocol transformation defines a field-level semantic map and loss policy. An adapter cannot drop, truncate, default, duplicate, reinterpret, or synthesize authoritative identity, tenant, purpose, classification, provenance, expiry, delegation, policy version, cancellation, sequence, idempotency, or unknown-state information without an explicit approved transformation and downstream representation. Unsupported semantics block the path or invoke a documented compensating contract; they are not silently approximated.

## 14. Output and downstream-use protection

AI output is untrusted data. Before presentation, execution, persistence, publication, callback, export, or machine consumption, the service validates structure, type, size, encoding, classification, sensitivity, provenance, destination, permitted use, uncertainty, and action implications.

When AI-selected output is used to invoke, execute, persist, route, or otherwise determine material effect through an endpoint, method, tool, query, command, file path, callback URL, credential reference, or business object, it requires independent allowlisting, authorization, validation, and the applicable ARC-P130 control. Merely presenting non-executed content to an authorized human does not by itself invoke ARC-P130, although output validation, disclosure, and downstream-use controls still apply. Structured output is validated in full before machine use; partial streams are not represented as complete or safe.

Result access is reauthorized and bound to job, consumer, tenant, purpose, destination, contract, and retention. Errors do not disclose secrets, internal topology, provider configuration, job existence, tenant metadata, inaccessible objects, or sensitive model diagnostics.

## 15. Reliability, state, and reconciliation

The service maintains orthogonal state machines with named owners and authoritative evidence:

- **transport delivery:** pending, accepted, delivered, acknowledged, expired, dead-lettered, or unknown, owned by the integration transport;
- **service execution:** accepted, queued, running, succeeded, failed, canceled, expired, or unknown, owned by the reusable AI service;
- **result delivery:** pending, available, partially delivered, delivered, revoked, expired, or unknown, owned by the delivery controller;
- **target transaction:** not applicable, prepared, committed, rejected, compensated, or unknown, owned by the target and governed by ARC-P130 when applicable; and
- **business outcome:** not assessed, achieved, partially achieved, not achieved, or unknown, owned by the consuming capability or accountable business process.

State names cannot be projected across machines without authoritative evidence. Contracts define allowed transitions, terminal states, transition guards, writer and reader authority, cancellation races, restart behavior, contradictory-state precedence, correction, and reconciliation. Stateful modes add bounded projections: streams use created, open, draining, closed, canceled, expired, and unknown, authored by the stream relay; batches record batch and per-item execution and delivery, authored by the batch coordinator and delivery controller respectively; events record publication and per-subscription delivery or checkpoint, authored by the event adapter and subscription broker respectively; and callbacks record pending, attempted, acknowledged, exhausted, canceled, and unknown, authored by the callback broker. None of these states proves target transaction or business outcome.

At-least-once delivery is assumed for durable operations. Idempotency keys bind authoritative caller, tenant, purpose, operation, contract and policy or authorization version, classification, normalized request or digest, output destination, approved provider, model, target and region constraints, lifecycle state, and expiry. Concurrent key use, changed payload, cross-tenant reuse, expired replay, or key-store failure is rejected or reconciled safely. A material change to any bound basis invalidates the record or requires explicit reauthorization and reconciliation before an earlier result may be released.

Retries are limited to operations proven idempotent or protected by target-native idempotency and reconciliation. A timeout, disconnect, lost broker acknowledgment, worker crash, missing callback, contradictory provider response, or evidence gap results in unknown state until authoritative evidence resolves it. Non-idempotent unknown work is not blindly retried.

Capacity controls cover request and item size, tokens, sequence, concurrent requests, connections, stream buffers, queue depth, batch size, fan-out, retry budgets, callback backoff, worker capacity, result retention, cost, and downstream rate. Circuit breakers, admission control, fair scheduling, per-tenant quotas, backpressure, load shedding, and dependency isolation prevent retry storms and cascading failure.

## 16. Disconnected and degraded operation

When the shared control plane is unavailable, a cell may continue only with signed contract and policy bundles that remain within approved freshness, revocation, tier, region, service, consumer, provider, target, and evidence limits.

Freshness and replay decisions use a governed time model with maximum clock uncertainty, monotonic counters or equivalent anti-rollback state, approved time sources, trusted or signed time evidence where required, and explicit behavior for skew, rollback, leap, source disagreement, or time-source loss. An unavailable or untrusted clock cannot extend contract, policy, authorization, callback, replay, credential, or result lifetime. Higher-tier work stops when time uncertainty exceeds its approved bound.

Disconnected cells cannot register services or consumers, expand privileges, enable routes, accept new callbacks or subscriptions, weaken validation, select unapproved versions, create exceptions, or increase provider, model, data, target, action, tenancy, connectivity, or administrative scope.

Tier 3 and Tier 4 activity stops or cannot commit when current identity, tenant binding, authorization, contract integrity, revocation, or required evidence is unavailable. When authoritative outcome assurance applies to the capability or action class under ARC-P130 or ARC-P160, consequential commit and dependent activity are blocked until that assurance is available; non-consequential inference or retrieval is not stopped solely because target-outcome assurance is inapplicable. Lower tiers may use approved degraded modes only when scope does not expand, the state is visible and evidenced, and duration and recovery authority are bounded.

Emergency stop and revocation use a separately protected out-of-band path or a cell-local containment authority whose permissions are limited to restriction and shutdown. Where neither is feasible, the approved risk record defines a maximum isolation window no longer than the shortest relevant bundle, credential, route, provider, tenant, or authorization lifetime. Conflicting emergency commands fail toward the more restrictive state, are independently evidenced, and require governed recovery.

Reconnection verifies bundle sequence and time, rejects rollback and replay, reconciles registrations, revocations, jobs, callbacks, results, evidence, and exceptions, and prevents divergent local state from silently becoming authoritative.

## 17. Lifecycle, recovery, and retirement

Service publication requires owner, purpose, consumers, operations, protocol modes, schemas, data, dependencies, providers and targets, limits, SLOs, evidence, compatibility, support, recovery, and retirement approval. Material change triggers architecture, risk, security, privacy, legal, supplier, and operational review as applicable.

Recovery tests worker failure before and after effects; broker acknowledgment loss; callback loss; duplicate and reordered work; queue and result corruption; partial stream and batch; policy outage; cell loss; regional failover; provider failure; stale configuration; KMS and credential recovery; backup restoration; and reconciliation against target-native state.

Emergency suspension revokes routes, credentials, registrations, subscriptions, callbacks, queued work, replays, provider access, and privileged sessions according to risk. Resumption requires current authorization, contract, dependency, provider, target, evidence, and recovery validation.

Retirement drains or cancels work, resolves unknown outcomes, disposes results and temporary state, removes routes and registrations, revokes credentials and subscriptions, disables callbacks and scheduled work, migrates consumers, completes provider exit and deletion, preserves required evidence, and tests former endpoints, identities, queues, exports, replicas, backups, and support paths for residual access.

## 18. Control points

| ID | Control point | Outcome | Primary implementation and evidence roles |
|---|---|---|---|
| CP1 | Service registration and approval | Every service has accountable ownership, purpose, contracts, dependencies, limits, lifecycle, and approved state | AI Service Owner; Enterprise Architecture, Risk, Security, Privacy, Legal, and Operations |
| CP2 | Consumer registration and admission | Only approved consumers invoke allowed operations for an authorized tenant, purpose, tier, and context | Application Owner; IAM, API Owner, and Policy Administration |
| CP3 | Contract, schema, version, and canonicalization | Requests, events, files, frames, callbacks, and responses conform to an approved unambiguous contract | API Owner; Application Security and Contract Registry Custodian |
| CP4 | Identity, tenant, purpose, classification, and delegation binding | Authoritative context survives every hop without caller-controlled expansion | IAM and API Owner; Policy Administration and Data Governance |
| CP5 | Integration state and tenant isolation | Jobs, queues, streams, batches, callbacks, caches, results, evidence, and support state remain isolated | AI Platform Owner; Platform Engineering, Data Owner, and Security Engineering |
| CP6 | Deterministic dispatch and cell selection | Only approved service, operation, version, region, and execution cell receive work | AI Platform Owner and API Owner; Platform Operations and Enterprise Architecture |
| CP7 | Durable acceptance and delivery state | Job identity, request digest, idempotency, order, expiry, policy, cancellation, and correlation are atomic and attributable | Integration Platform Owner; Messaging, Workflow, and SRE teams |
| CP8 | Inference handoff | Model access preserves context and implements ARC-P100 admission, policy, routing, and provider-control outcomes through an approved centralized or federated enforcement point, with ARC-P140 additionally applied for enterprise-operated model lifecycle and serving | AI Service Owner; AI Platform Owner and, when applicable, Model Owner |
| CP9 | Data and retrieval handoff | Data access preserves authorization, provenance, classification, lifecycle, and ARC-P120 semantics where applicable | Data Owner; Data Governance and Retrieval Service Owner |
| CP10 | Tool and target handoff | Deterministic target calls are allowlisted and authorized; AI-selected or consequential action invokes ARC-P130 | Application Owner; Target Owner, IAM, and Agent Governance |
| CP11 | Output validation and delivery | Only authorized, validated, classified, and correctly labeled results reach each destination | Application Owner; Application Security, Data Governance, and Records Management |
| CP12 | External provider, event, and callback boundary | External responsibilities, sender and destination identity, message integrity, data use, failure, and exit are governed | AI Capability Technical Owner; Third-Party Risk, Security, Privacy, and API Owner |
| CP13 | Evidence export and assurance gaps | Attributable minimized evidence reaches ARC-P160 and material gaps block unsupported assurance claims | AI Service Owner and Observability Platform; Security Operations consumes detections and Assurance independently verifies completeness and gaps |
| CP14 | Capacity, retry, reconciliation, recovery, and degradation | Resource use and failure are bounded; unknown outcomes reconcile; degraded modes never expand scope | AI Service Owner and SRE; Platform Operations, Business Continuity, and Incident Response |
| CP15 | Compatibility, migration, deprecation, portability, and retirement | Consumers and providers change or exit without silent contract drift or residual access | Enterprise Architecture and AI Service Owner; API Owner, Procurement, Records, and Operations |

Catalog `owner_role` remains accountable. Pattern roles identify implementation and evidence responsibilities without transferring control accountability. Every deployment assigns exactly one accountable owner to each control point; when a row lists multiple primary roles, one is selected as accountable and the others are implementation, consultation, consumption, or evidence contributors. Every deployment maintains a CP1-CP15 assurance matrix mapping controls, the single accountable owner, evidence-producing roles, artifacts, procedures, objectives, review state, exceptions, findings, and remediation.

## 19. Control alignment

Required controls are:

- Governance and risk: `GOV-130`, `RSK-110`, `RSK-120`, `RSK-140`.
- Identity: `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-140`, `IAM-150`.
- Data: `DAT-100`, `DAT-110`, `DAT-120`, `DAT-130`, `DAT-160`.
- Model and application: `MOD-120`, `APP-100`, `APP-110`, `APP-120`, `APP-130`, `APP-140`, `APP-150`.
- Platform and integration: `API-110`, `API-150`, `INF-140`, `INF-150`.
- Operations: `OPS-100`, `OPS-110`, `OPS-120`, `OPS-130`, `OPS-140`, `OPS-150`.
- Monitoring: `MON-100`, `MON-110`, `MON-120`, `MON-140`, `MON-150`.
- Compliance and assurance: `CMP-100`, `CMP-110`, `AUD-110`, `AUD-120`.
- Workforce and architecture: `EDU-130`, `ARC-100`, `ARC-110`, `ARC-130`, `ARC-140`.

Inherited controls that shall be verified at each applicable dependency and boundary are `GOV-100`, `GOV-110`, `GOV-120`, `GOV-140`, `STR-100`, `STR-130`, `RSK-100`, `MOD-100`, `MOD-110`, `MOD-130`, `MOD-140`, `MOD-150`, `API-100`, `INF-100`, `INF-110`, `INF-120`, `INF-130`, `AUD-100`, `AUD-130`, `AUD-140`, `EDU-100`, `EDU-110`, `EDU-120`, `EDU-140`, `ARC-120`, and `ARC-150`. The inheritance record identifies the source, applicable component or crossing, supplied outcome, consumer configuration, limitations, evidence, freshness, failure dependency, and retained responsibility; it does not require an unrelated broker or target to implement enterprise-level or model-specific controls.

Conditional controls are `STR-110` for value claims; `STR-120` for experimentation; `RSK-130` for material individual, group, safety, environmental, or societal impact; `DAT-140` for personal data and rights; `DAT-150` for retrieval, embeddings, or vector data; `API-120` for tools, plugins, or connectors; `API-130` for MCP or any qualifying context-exchange or orchestration mechanism, whether deterministic or dynamic; `API-140` for external AI services, APIs, tool providers, data processors, evaluation services, or subcontracted operations participating in the integration path; `AGT-100`, `AGT-110`, `AGT-120`, `AGT-130`, `AGT-140`, `AGT-150`, `AGT-160`, and `MON-130` for agentic operation; and `CMP-120`, `CMP-130`, and `CMP-140` for suppliers, jurisdiction or transfer, and intellectual-property or licensing obligations.

The three allocations are mutually exclusive and cover all 91 controls.

## 20. Evidence and assessment

Required evidence includes:

- service, consumer, provider, target, adapter, broker, cell, callback, subscription, route, owner, purpose, protocol, tier, region, environment, version, support, and retirement inventories;
- context, component, sequence, deployment, state-machine, administration, evidence, and recovery diagrams;
- complete boundary-crossing records for every material path;
- versioned API, event, file, stream, batch, and callback contracts; schema hashes; canonicalization rules; examples; compatibility matrices; and deprecation schedules;
- identity and delegation matrices covering submit, execute, cancel, status, result, replay, administer, support, and target commit;
- field-level classification, provenance, transformation, retention, residency, encryption, deletion, legal-hold, and secret-handling mappings;
- signed configuration, contract, route, cell-conformance, callback-registration, subscription, exception, and emergency-restriction history;
- timeout, deadline, retry, idempotency, sequence, order, cancellation, expiry, unknown-outcome, compensation, and reconciliation matrices by operation;
- job ledgers, event and queue records, stream state, callback receipts, replay decisions, dead-letter and quarantine records, batch manifests, per-item dispositions, result releases, and target-native evidence;
- event evidence that records occurrence, receipt, and processing time; time quality and uncertainty; source sequence and its scope; duplicate, gap, reorder, and late-arrival disposition; transformation lineage; delivery and acknowledgment state; and source attestation;
- provider and protocol gap registers covering identifiers, semantics, retention, training use, subprocessors, residency, callback and backfill, outage, throttling, integrity, deletion, portability, and exit;
- load, quota, cost, capacity, backpressure, retry-storm, fan-out, failover, chaos, recovery, portability, compatibility, migration, deprecation, and retirement tests;
- independently protected ARC-P160 evidence for admission, authorization, transformation, dispatch, inference, retrieval, target call, callback, retry, cancellation, result release, side effect, reconciliation, policy or configuration change, gap, and recovery, exported through identities, interfaces, trust roots, and authorization distinct from operations and administration; and
- the CP1-CP15 assurance matrix.

Negative testing includes forged user, workload, tenant, purpose, classification, delegation, token audience, and scope; cross-tenant request, object, job, callback, resume-token, cache, queue, batch-item, result, dead-letter, export, backup, and support access; malicious or unavailable bootstrap, wrong-cell substitution, redirect and host confusion, routing-assertion forgery, wrong audience, tenant, capability, region, endpoint, version, or expiry, replayed route, downgrade, failover to an ineligible cell, and selected-cell endpoint-identity mismatch; cloned or compromised cell, stolen cell identity, stale or forged runtime attestation, release-closure mismatch, lateral secret use from an unapproved runtime, forged cell evidence, and selection of a quarantined cell; duplicate keys, unknown fields, alternate encodings, ambiguous types, numeric overflow, schema downgrade, canonicalization mismatch, wrong content type, and oversized nesting; direct and indirect prompt injection in structured fields, files, URLs, headers, event metadata, provider status, callbacks, errors, and target responses; model-generated endpoint, method, tool, query, command, file path, callback URL, credential reference, or target object; duplicate submit, concurrent idempotency, changed payload, replay after expiry, timeout retry, reorder, late callback, cancellation race, and eventual completion after caller timeout; authorization or revocation change while queued, streaming, batched, retrying, or awaiting callback; worker crash before and after effect, broker acknowledgment loss, callback loss, poison message, dead-letter replay, partial batch or stream, and contradictory provider or target state; event topic enumeration, wildcard escalation, consumer-group takeover, unauthorized subscribe, consume, acknowledge, checkpoint, replay, backfill, or retained-backlog access after revocation; callback signature, timestamp, nonce, audience, digest, job binding, compromised callback signer, pre-compromise signature received after revocation, key-status or replay-cache outage, key rotation, redirect, DNS rebinding, unregistered private address, response size, and error disclosure; provider or model failover that changes region, retention, training, safety, schema, behavior, or assurance; frame injection, truncation, cross-stream mixing, resume-token theft, slow consumer, connection exhaustion, and sensitive partial-output release; mixed-tenant batching, cache-key omission, count or timing leakage, unauthorized item hidden in an authorized batch, and aggregate success masking failures; retry storms, fan-out explosion, quota evasion, expensive-payload amplification, and backpressure propagation; forged, wrong-purpose, stale, downgraded, rollback, or split-brain signed configuration, compromised signer, key rotation or revocation failure, and continued trust in pre-compromise artifacts; control-plane compromise, partition during emergency containment, conflicting emergency commands, out-of-band containment failure, and unsafe recovery from containment; clock skew, clock rollback, time-source loss, excessive time uncertainty, and acceptance of expired policy, authorization, callback, lease, or replay windows; semantic-loss and differential tests across gateway, broker, adapter, SDK, callback, and target hops for dropped, truncated, defaulted, duplicated, reinterpreted, or synthesized identity, tenant, purpose, classification, provenance, expiry, delegation, policy, cancellation, and unknown-outcome metadata; observability outage, forged trace IDs, telemetry injection, raw-content leakage, evidence tampering, and attempted replay or action through Z7; connector or SDK rollback, compromised dependency, expired certificate, revoked secret, unsupported protocol, stale policy, silent contract drift, and cell configuration rollback; and retirement with surviving credentials, routes, jobs, schedules, callbacks, subscriptions, replicas, caches, results, exports, backups, or provider-held data.

Acceptance requires each exercise to define objective, input and precondition, exact evidence, pass and fail thresholds, safe-state or escalation, accountable reviewer, and retest trigger. A successful transport response is never evidence of authorization, correct model behavior, completed side effect, or verified business outcome.

### 20.1 Failure modes and abuse-case treatment

Each deployment maintains a failure-and-abuse treatment record covering every material mode identified in Sections 7 through 17 and the negative tests above. Each record identifies the initiating condition or adversary capability, affected boundary and state machines, detection signal and maximum detection interval, containment action and safe state, recovery and resumption authority, reconciliation source, required evidence, residual risk, tier applicability, and retest trigger. At minimum, the record covers identity or delegation abuse; cross-tenant access; bootstrap, route, cell, signer, clock, policy, and emergency-channel compromise; contract or semantic drift; prompt or instruction injection; provider, model, data, target, broker, callback, stream, batch, and event failure; duplication, replay, cancellation, timeout, unknown outcome, and contradictory state; capacity or cost exhaustion; evidence loss or forgery; and incomplete retirement.

## 21. Variants

- **Central multi-protocol hub:** simplifies governance and onboarding but increases concentration, latency, residency, and blast-radius risk.
- **Durable workflow and event backbone:** favors long-running, event-heavy, callback-heavy, and failure-prone work; deterministic workflow state does not grant agent authority.
- **Regional or sovereign cells:** restrict contracts, data, providers, targets, and evidence to approved jurisdictions and require controlled cross-region failover.
- **High-assurance dedicated cell:** isolates runtime, state, secrets, administration, queues, results, and evidence for incompatible Tier 4 or legal domains.
- **Edge or intermittently connected cell:** uses bounded signed bundles, local evidence, offline revocation and expiry, constrained operation, and governed reconciliation.
- **Thin synchronous service:** minimizes durable state for low-latency bounded requests while retaining identity, contract, deadline, output, and evidence controls.
- **External managed integration service:** retains enterprise contract, identity, data, evidence, continuity, portability, deletion, and exit accountability across the provider boundary.

Variants may combine or externally supply baseline components only when the responsibility, evidence, failure dependency, and retained enterprise accountability are explicit. A central hub may co-locate bootstrap, ingress, policy enforcement, and runtime components but remains subject to cell-identity, isolation, blast-radius, and continuity outcomes. A durable workflow backbone may supply job, event, callback, and reconciliation components but cannot supply authorization or business-outcome truth by transport status alone. Regional, high-assurance, and edge cells alter placement and connectivity but retain signed configuration, local admission, bounded authority, evidence export, and governed reconciliation. A thin synchronous service may omit unused durable-mode components only when its contract prohibits those modes. An external managed service may supply runtime components but cannot inherit enterprise approval, risk acceptance, data accountability, or independent assurance. In every variant, CP1 through CP15, the six plane outcomes, ARC-P100 through ARC-P160 handoffs, single accountable owners, boundary records, safe-state behavior, and the 91-control allocation remain mandatory where applicable; any changed flow is recorded in the architecture and assurance matrix.

## 22. Anti-patterns

- Exposing raw provider APIs or a generic execute-anything endpoint as an enterprise service.
- Treating queue, transport, callback, HTTP, trace, or model success as verified business outcome.
- Claiming exactly-once business effects from broker or workflow guarantees.
- Using event content, queue metadata, callback URLs, correlation IDs, or trace IDs as authorization.
- Retrying non-idempotent work after an unknown outcome without reconciliation.
- Allowing adapters to contain hidden provider routing, model selection, agent planning, business authorization, or target authority.
- Sharing credentials, queues, caches, results, callbacks, dead letters, support access, or administrative paths across tenants without demonstrated isolation.
- Accepting silent schema downgrade, unknown-field smuggling, content-type confusion, provider drift, or fallback to an unapproved version.
- Accepting caller-selected or model-generated callback destinations, endpoints, methods, queries, tools, files, or target objects.
- Unbounded streams, queues, batches, retries, callbacks, fan-out, result retention, or cost.
- Describing all integrations as tools and collapsing deterministic service integration into ARC-P130.
- Using ARC-P150 to bypass ARC-P100, ARC-P120, ARC-P130, ARC-P140, target-native authorization, or ARC-P160 evidence requirements.
- Using Z7 observability or support access as a replay, request, or action interface.
- Retaining orphaned jobs, routes, credentials, subscriptions, callbacks, results, exports, or provider data after retirement.

## 23. Acceptance criteria

The implemented pattern shall:

- contain every required architecture-template section;
- define the contract-first federated fabric, six planes, all six interaction modes, and CP1 through CP15;
- maintain the approved boundary with ARC-P100, ARC-P110, ARC-P120, ARC-P130, ARC-P140, and ARC-P160;
- enumerate and correctly allocate all 91 catalog controls;
- require complete boundary-crossing records and protocol-specific state, security, failure, and evidence semantics;
- define orthogonal transport, service-execution, result-delivery, target-transaction, and business-outcome state machines with accountable owners and contradiction handling;
- make at-least-once delivery, unknown outcomes, idempotency, current authorization, reconciliation, and transport-versus-business outcome explicit;
- include risk-tiered signed cached operation without authority expansion;
- define signing-trust governance, trusted-time behavior, bounded authorization leases, granular event permissions, and adapter semantic-preservation tests;
- define the required evidence, assurance matrix, negative tests, variants, anti-patterns, safe failure, and retirement behavior;
- remain vendor-neutral and avoid implementation-product selection; and
- pass architecture, control, link, placeholder, structure, and repository validation.

## 24. Out of scope

This design does not choose API gateways, brokers, workflow engines, service meshes, integration platforms, SDKs, serialization formats, databases, providers, models, or observability products. Product configuration belongs in ESAF-1400. External-standard mappings belong in ESAF-1600. Business-specific service contracts and capability designs are implementations of this pattern, not part of ARC-P150 itself.
