# ARC-P130 Agentic and Multi-Agent AI

## Metadata

**Pattern ID:** ARC-P130

**Status:** Draft

**Version:** 0.1.0

| Field | Value |
|---|---|
| Owner | Enterprise Architecture |
| Required reviewers | Agent Owner, Security Architecture, AI Platform, Application Engineering, IAM, Risk, Operations, target-system owners |
| Pillars | Protect AI, Utilize AI, Govern AI |
| Lifecycle stages | Risk Classification, Architecture, Development, Validation, Approval, Deployment, Operations, Monitoring, Retirement |
| Capability tiers | Tier 1 through Tier 4; Tier 0 when tools, persistent state, or enterprise services are available |
| Deployment models | Single agent, supervisor-worker, peer collaboration, human-led actions, persistent agent, high-assurance transaction, research swarm, managed agent platform |
| Primary pattern role | Primary agentic and multi-agent pattern; supported by ARC-P100 and ARC-P160 |
| Supersedes | None |

## Purpose

Provide governed architecture for agents that plan, delegate, use tools, maintain state, communicate with other agents, or initiate consequential actions. The pattern separates model reasoning from enforceable identity, authority, approval, execution, evidence, containment, and recovery.

## Problem statement

Agents convert model output into continuing activity and external side effects. Without enforceable boundaries, they can amplify authority, misuse tools, propagate credentials, retain malicious memory, create unbounded descendants, substitute actions after denial, duplicate transactions, obscure accountability, or continue after an attempted stop.

Prompt instructions cannot reliably govern identity, permission, delegation, human approval, target authorization, transaction state, evidence, or emergency intervention. Enterprises need an external policy and execution architecture that keeps autonomy bounded and accountable.

## Intended outcomes

- Every agent and runtime instance is uniquely identified, owned, approved, attested, and traceable to its initiating principal and lineage.
- Models propose plans and actions but cannot authorize them.
- Authority is minimal, short-lived, purpose-bound, revocable, externally issued, and attenuated upon delegation.
- Tools and targets enforce current authority outside the model.
- Human approval is informed, eligible, independent where required, single-use, and bound to an immutable exact action.
- Consequential side effects are prepared, committed, reconciled, deduplicated, and recovered safely.
- Memory, messages, plans, and tool output remain untrusted and cannot become authoritative identity, policy, approval, or transaction state.
- Recursive spawning, persistence, runtime resources, cost, duration, fan-out, and aggregate side effects remain bounded.
- Evidence reconstructs material action from principal through descendants to verified target outcome.
- Out-of-band pause, lease revocation, containment, descendant termination, reconciliation, recovery, and authorized resumption remain effective.

## Non-goals

ARC-P130 does not prescribe agent frameworks, models, reasoning methods, orchestration products, or hidden chain-of-thought collection. It does not make every workflow autonomous, treat prompts as authorization, guarantee plan correctness, or replace target-system controls and domain safety standards.

The pattern does not replace ARC-P100 model-provider controls, ARC-P120 retrieval controls, human accountability, legal authority, or independent assurance.

## Applicability

Use ARC-P130 when an AI capability can initiate tool calls, maintain operational memory, continue beyond a single response, schedule or retry work, delegate, create child agents, communicate with peer agents, or produce external side effects.

Tier 1 and Tier 2 should prefer a single bounded agent or human-led action model. Tier 3 and Tier 4 should use deterministic workflow orchestration around bounded agent steps, enhanced approval, transactional execution, out-of-band containment, and independent outcome assurance.

## Assumptions and prerequisites

- The capability, Agent Owner, business owner, technical owner, purpose, tier, risk, and prohibited outcomes are approved.
- Human and non-human identity, secrets, policy, logging, incident, change, and continuity services are available.
- Tools, target operations, data, side effects, failure semantics, and owners are inventoried.
- Target systems can enforce authorization independent of model output.
- Organization-defined limits exist for runtime, cost, steps, calls, tokens, data, fan-out, delegation, transactions, approvals, evidence, and recovery.
- ARC-P100 or equivalent governs models, providers, routing, and common platform controls.

## Prohibited uses

The pattern shall not be used to:

- let a model issue, enlarge, renew, transfer, interpret, or approve authority;
- pass parent bearer credentials to child or peer agents;
- infer authority from prompts, plans, messages, memory, tool output, or claimed role;
- allow unrestricted tools, targets, operations, data, spawning, persistence, or retries;
- approve vague intent rather than an exact immutable action;
- retry consequential unknown-result actions without reconciliation;
- represent best-effort compensation as atomic rollback;
- store credentials, leases, or approvals in agent memory;
- implement kill and containment solely inside the agent being stopped;
- allow agents to alter or delete authoritative evidence.

## Architecture views

### Policy-mediated runtime

```text
Initiating Principal
  -> Identity and Purpose Binding
  -> Agent Admission and Runtime Identity
  -> Policy and Authority-Lease Service
  -> Planner and Orchestrator
       -> Delegation Broker -> Child and Peer Agents
       -> Memory and State Broker
       -> Tool and Action Gateway
            -> Human Approval
            -> Transaction Coordinator
            -> Enterprise Targets
            -> Outcome Reconciliation
  -> Evidence, Detection, Containment, and Recovery
```

The authoritative agent definition, lineage, policy, lease, approval, transaction, and intervention state remain outside model context.

### Flow separation

| Flow | Contents | Rule |
|---|---|---|
| Intent | User objective, constraints, context, and approved purpose | Influences planning but cannot create authority |
| Authority | Identity, policy, lease, delegation, approval, revocation, emergency control | Integrity-protected and evaluated outside the model |
| Execution | Plans, messages, tool requests, preparation, commit, compensation, result | Typed, authorized, bounded, approval-aware, and reconciled |
| Evidence | Decisions, lineage, messages, actions, approvals, outcomes, alerts, containment, recovery | Attributable, independently protected, minimized, and immutable according to policy |

Authority metadata shall not be inferred from intent or execution content.

## Actors and identities

| Actor | Identity and accountability requirements |
|---|---|
| Initiating principal | Authenticated human or managed service identity with approved purpose and current authority |
| Agent definition | Registered owner, purpose, tier, versions, tools, data, memory, delegation, limits, and lifecycle state |
| Runtime instance | Unique attested identity bound to approved definition, tenant, versions, deployment, environment, and parent lineage |
| Child or peer agent | Independent identity with authenticated communication and attenuated authority |
| Policy and lease issuer | Separately controlled service authorized to evaluate policy, issue leases, revoke authority, and preserve decisions |
| Tool and target | Registered identity and owner that independently validates operation, arguments, target, authority, and transaction state |
| Human approver | Strongly authenticated, eligible, sufficiently informed, and independent where policy requires |
| Transaction coordinator | Managed service that prepares, commits, deduplicates, reconciles, and records side effects |
| Outcome assurance service | Separately controlled verifier using target-native authoritative evidence |
| Containment authority | Out-of-band incident or operations identity authorized to pause, revoke, isolate, terminate, and recover |

Runtime credentials are non-exportable where supported. Cloned, altered, unattested, or unapproved runtimes cannot use agent identity or leases.

## Data and instruction flows

| Flow | Contents | Required properties |
|---|---|---|
| Agent admission | Principal, tenant, purpose, tier, definition, versions, deployment, parent lineage | Authentication, approval, attestation, lifecycle validation, correlation |
| Authority lease | Principal, agent, purpose, tools, targets, data, budgets, delegation, approval, expiry | Integrity, audience, nonce, policy version, revocation, fail-closed semantics |
| Plan and replan | Objective, steps, dependencies, expected effects, approval gates, termination | Untrusted proposal, schema, limits, policy evaluation, no hidden authorization |
| Delegation | Parent and child identity, task, attenuated lease, lineage, budgets, expiry | Eligibility, depth, breadth, aggregate limits, revocation propagation |
| Agent message | Sender, receiver, task, purpose, content, provenance, classification | Authentication, typed envelope, replay protection, trust label, correlation |
| Memory and state | Session, preference, workflow, durable record, shared state, checkpoint | Authorization, provenance, reliability, tenant isolation, version, retention, deletion |
| Tool request | Operation, arguments, target, data, lease, approval, idempotency, expected state | Schema, current effective authority, target authorization, limits, policy |
| Transaction | Prepared state, canonical digest, approval, commit, compensation, reconciliation | TOCTOU protection, concurrency, duplicate suppression, authoritative outcome |
| Evidence | Policy, lease, plan, message, tool, approval, action, result, memory, containment | Correlation, trusted time, integrity, ordering, access, retention, loss detection |

## Trust boundaries

| Crossing | Required treatment |
|---|---|
| Z1 to Z3 admission | Bind principal, tenant, capability, purpose, tier, risk, session, and budget; create attested runtime identity |
| Z2 to Z3 lease | Issue integrity-protected, short-lived, audience-bound, revocable authority with explicit limits |
| Z3 planner to executor | Treat plan as untrusted proposal; validate schema, current policy, lease, limits, and preconditions |
| Z3 agent to agent | Authenticate sender and receiver; validate purpose, envelope, provenance, classification, replay, rate, and correlation |
| Z3 to Z5 memory | Broker reads and writes by identity, tenant, purpose, provenance, reliability, retention, version, and conflict policy |
| Z3 to Z6 tool or target | Recompute effective authority and validate arguments, target, data, risk, approval, idempotency, and transaction state |
| Z3 or Z6 to Z7 approval | Bind eligible human decision to canonical action digest, scope, agent, lease, target, expiry, and approver |
| Z6 to Z3 outcome | Return authenticated typed target result with transaction ID and committed, failed, compensated, or unknown state |
| Z7 to Z3 containment | Apply out-of-band pause, isolation, revocation, termination, restoration, and authorized resumption |
| Z3 or Z6 to Z7 evidence | Emit attributable policy, lease, plan, message, tool, approval, transaction, result, memory, and lineage events |

## Components and responsibilities

| Component | Required responsibility |
|---|---|
| Agent registry and admission | Record definition, owner, purpose, tier, versions, deployment, identity, attestation, lineage, and lifecycle |
| Policy and lease service | Evaluate current effective authority, issue and revoke bounded leases, enforce validity, and preserve evidence |
| Planner and orchestrator | Constrain planning, maintain lineage, dispatch bounded tasks, detect cycles, and obey external policy |
| Delegation broker | Create child identity and attenuated lease; enforce eligibility, depth, breadth, budgets, cancellation, and orphan handling |
| Message gateway | Authenticate agents; validate typed messages, purpose, provenance, classification, replay, limits, and trust |
| Memory and state broker | Separate state types; authorize reads and writes; preserve provenance, reliability, retention, correction, and deletion |
| Tool registry and gateway | Register tools and operations; validate schema, target, credentials, authority, output, limits, and retirement |
| Approval service | Present immutable preview, enforce eligibility and separation of duties, bind decision, and prevent reuse |
| Transaction coordinator | Prepare, canonicalize, commit, deduplicate, control concurrency, compensate, and reconcile outcomes |
| Runtime supervisor | Enforce time, steps, tokens, cost, calls, fan-out, resources, data, and side-effect budgets |
| Evidence and detection | Correlate events in independently protected storage and detect abuse, loops, escalation, gaps, and anomalies |
| Containment and recovery | Revoke leases, stop dispatch, terminate descendants, cancel durable work, reconcile effects, restore, and authorize resumption |
| Outcome assurance | Independently compare approved intent with authoritative target state before Tier 3 or Tier 4 success |

## Required controls

| Control group | Controls | Catalog accountability and primary evidence roles |
|---|---|---|
| Agent identity, authority, oversight, memory, traceability, intervention, multi-agent | `AGT-100`, `AGT-110`, `AGT-120`, `AGT-130`, `AGT-140`, `AGT-150`, `AGT-160` | Agent Owner remains accountable; IAM, platform, application, operations, and assurance produce evidence |
| Governance and risk | `GOV-130`, `RSK-110` | Capability accountability and Enterprise Risk Management |
| APIs, tools, orchestration | `API-110`, `API-120`, `API-130` | API Owner and AI Platform Owner |
| Human and non-human identity | `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-140`, `IAM-150` | IAM and AI Capability Technical Owner according to catalog |
| Application security and abuse resistance | `APP-100`, `APP-110`, `APP-120`, `APP-130`, `APP-140`, `APP-150` | Application Owner or Application Engineering according to catalog |
| Data, lineage, output, and feedback | `DAT-100`, `DAT-110`, `DAT-120`, `DAT-130`, `DAT-160` | Data Owner, Data Governance, and AI Capability Business Owner |
| Model validation and resource safeguards | `MOD-120`, `INF-150` | Model Validation Lead and AI Platform Owner |
| Monitoring and detection | `MON-100`, `MON-110`, `MON-120`, `MON-130`, `MON-140`, `MON-150` | AI Service Owner, Security Operations, Model Owner, and Agent Owner according to catalog |
| Service, change, incident, recovery, capacity | `OPS-100`, `OPS-110`, `OPS-120`, `OPS-130`, `OPS-140` | Technical Owner, Incident Response, Business Continuity, and AI Service Owner |
| Architecture governance, boundaries, failure, responsibility | `ARC-100`, `ARC-110`, `ARC-130`, `ARC-140` | Enterprise Architecture and Solution Architecture |

`API-100`, `ARC-120`, `ARC-150`, `MOD-100`, `INF-100`, and `INF-130` are normally inherited and require configuration evidence, sample traces, limitation analysis, and failure tests. Conditional controls include `API-140`, `API-150`, `DAT-140`, `DAT-150`, and `OPS-150` according to external services, concentration, personal data, semantic memory, and retirement.

Catalog `owner_role` remains accountable. Pattern roles identify implementation and evidence responsibility without transferring accountability.

## Control points and overlays

| CP | Control point | Required outcome | Primary implementation and evidence owners |
|---|---|---|---|
| CP1 | Agent registration and admission | Verify definition, owner, purpose, tier, versions, deployment, attested identity, lineage, and lifecycle | Agent Owner, IAM, Platform Engineering |
| CP2 | Authority lease issuance | Issue minimal authority bound to principal, agent, tenant, purpose, audience, tools, targets, actions, budgets, delegation, expiry, policy, and revocation | Agent Owner, IAM, policy-service owner |
| CP3 | Planning and task decomposition | Constrain objective, horizon, iteration, resources, termination, prohibited outcomes, and replanning; validate proposals | Agent Owner, Application Engineering |
| CP4 | Delegation and spawn broker | Enforce attenuation, attribution, eligibility, depth, breadth, concurrency, cost, expiry, revocation, and orphan handling | Agent Owner, orchestration-platform owner |
| CP5 | Inter-agent message gateway | Authenticate agents and validate contracts, purpose, provenance, classification, replay, rate, size, and instruction trust | AI Platform Owner, Agent Owner |
| CP6 | Memory and state broker | Enforce scoped reads and writes, isolation, provenance, reliability, conflict, retention, correction, deletion, and poisoning defense | Agent Owner, Data Owner, state-platform owner |
| CP7 | Tool registry and invocation gateway | Permit registered operations; validate schema, arguments, target, data, secrets, output, limits, and current authority | AI Platform Owner, tool owner, target-system owner |
| CP8 | Human approval service | Bind eligible independent approval to canonical action digest, target, parameters, agent, lease, expiry, and approver | Business or risk approval authority, approval-service owner |
| CP9 | Transaction and side-effect coordinator | Separate prepare, commit, and reconcile; enforce canonical digest, freshness, idempotency, concurrency, retry, and compensation | Target-system or transaction owner, Platform Engineering |
| CP10 | Runtime supervision and budgets | Enforce time, steps, tokens, cost, calls, fan-out, data, resources, and side effects; detect loops and escalation | AI Platform Owner, Platform Operations |
| CP11 | Evidence and detection | Correlate principal, lineage, messages, plans, policy, leases, approvals, tools, transactions, outcomes, memory, and administration | AI Service Owner, Security Operations, assurance |
| CP12 | Containment, kill, and recovery | Revoke leases, block tools, stop dispatch, terminate descendants, cancel durable work, reconcile actions, restore, and authorize resumption | Incident Response, Platform Operations, Agent Owner |
| CP13 | Outcome assurance | Independently compare approved intent with authoritative target state before Tier 3 or Tier 4 success | Independent validation or assurance owner, target-system owner |

Apply overlays for Tier 3 and Tier 4, external managed agent platforms, persistent agents, personal or regulated data, production actions, financial or legal transactions, safety impact, code execution, and research swarms.

## Architecture decisions and parameters

Required decisions include:

- single agent, supervisor-worker, peer, persistent, high-assurance, research, external, or combined model;
- agent definition, attestation, runtime identity, initiating principal, and service-initiated authority;
- lease fields, maximum lifetime, clock skew, cache age, revocation latency, offline behavior, and renewal authority;
- effective-authority inputs, target-native authorization, data policy, and commit-time recheck;
- tool, target, operation, data, side-effect, transaction, and approval classes;
- planning horizon, iteration, replan, termination, spawning, fan-out, and aggregate budgets;
- message schemas, allowed purposes, provenance, replay, rate, and conflict policy;
- memory types, write authority, reliability, retention, correction, deletion, and persistence;
- canonical action representation, idempotency, concurrency, preconditions, reservation, retry, compensation, and reconciliation;
- human approver eligibility, independence, quorum, emergency authority, expiration, and appeal;
- evidence content, trusted time, ordering, integrity, retention, access, gap handling, and WORM capability;
- containment acknowledgment, unreachable targets, durable work, in-flight effects, recovery, and resumption.

## Failure modes and abuse cases

| Failure | Required treatment |
|---|---|
| Policy service unavailable | Issue no new consequential authority; allow bounded read-only behavior only when preapproved |
| Lease expired, revoked, stale, or unverifiable | Stop affected work, preserve state, cancel dependent work, and request reauthorization |
| Approval unavailable, expired, or changed | Queue safely or abstain; never infer approval from silence or prior action |
| Target state changes after preparation | Abort commit, reprepare canonical transaction, and obtain reapproval where material |
| Tool timeout or unknown result | Reconcile target state before retry and block contradictory dependent work |
| Memory inconsistency or poisoning | Quarantine affected state and continue only through approved stateless or known-good mode |
| Peer conflict or authority claim | Stop conflicting work and use deterministic arbitration or human review |
| Budget exceeded, loop, deadlock, or recursive explosion | Halt, stop descendants as needed, summarize attributable state, and release resources |
| Evidence failure | Stop Tier 3 and Tier 4 consequential actions; lower tiers use only approved bounded buffering |
| Kill signal | Stop dispatch, revoke leases, require enforcement acknowledgment, terminate descendants, inventory unreachable targets, reconcile durable and in-flight work, preserve evidence, and require recovery approval |
| Provider or model degradation | Do not fail over to broader data use, tools, authority, provider, or action semantics without approval |
| Outcome assurance unavailable or contradictory | Keep outcome unknown, block success reporting and dependent action, and escalate or reconcile |

Kill and revocation cannot retract committed external effects. Such effects require compensation or domain recovery, and unreachable or unmanaged targets are explicitly disclosed.

## Fallback recovery and retirement

Containment shall revoke leases, block tools, stop new dispatch, terminate descendants, cancel or tombstone scheduled jobs, callbacks, broker messages, workflow tokens, target-side jobs, and delayed retries, isolate memory, and reconcile all in-flight or unknown actions.

Each reachable enforcement point acknowledges containment. Unreachable targets and unconfirmed actions remain visible until reconciled. Automatic restart is prohibited after emergency stop.

Recovery verifies identity, policy, lease state, tool configuration, memory integrity, target transactions, evidence continuity, and known-good runtime versions before authorized resumption. Retirement removes agent identities, leases, schedules, queues, tools, credentials, memory, state, routes, deployments, and privileges; preserves required evidence; and verifies dependent and descendant termination.

## Evidence and assessment

Required evidence includes:

- agent inventories, owners, purposes, tiers, versions, deployments, identities, attestations, and lineage;
- architecture and intent, authority, execution, evidence, memory, delegation, tool, and transaction flows;
- risk classification, baseline, identity, lease, policy, revocation, permission, limit, delegation, and denial records;
- tool registry, schemas, targets, side effects, approvals, tests, monitoring, change, and retirement;
- plan and replan records sufficient for assurance without hidden chain-of-thought;
- message envelopes, provenance, replay, validation, delivery, and conflict outcomes;
- memory read, write, correction, deletion, provenance, reliability, and conflict records;
- approval preview, canonical digest, eligible approver, authority, decision, expiration, quorum, and use;
- prepare, precondition, idempotency, commit, compensation, reconciliation, and target-state evidence;
- principal-to-descendant-to-action traces with trusted timestamps and integrity;
- loop, budget, escalation, denial, approval, unknown-outcome, evidence-gap, and containment alerts;
- lease revocation, kill, tool blocking, descendant termination, durable-work cancellation, reconciliation, recovery, and authorized-resumption exercises;
- adversarial tests for injection, confused deputy, authority amplification, replay, forged messages, memory poisoning, duplicate actions, approval substitution, recursive explosion, workload cloning, stale lease, TOCTOU, and evidence loss;
- service, change, incident, continuity, capacity, cost, provider, and retirement records.

Authoritative evidence is stored through separately administered append-only or WORM-capable controls with trusted time, ordering or sequence integrity, verification, access control, retention, and loss detection.

Assessment shall recompute tier, risk, and baseline for representative agents and verify that authority, oversight, assurance, and failure behavior change accordingly. Tier 3 and Tier 4 testing independently compares the canonical approved action with authoritative target state across committed, failed, unknown, duplicate, partial, compensated, stale-approval, mismatched-target, and unavailable-assurance outcomes.

## Variants and alternatives

### Single bounded agent

One agent uses limited tools and cannot delegate. This is the preferred default for straightforward automation.

### Supervisor-worker

A supervisor decomposes work and issues attenuated child leases. Workers cannot spawn by default, and supervisor authority does not transfer automatically.

### Peer collaboration

Agents communicate through typed authenticated messages and deterministic conflict policy. They share neither implicit authority nor unrestricted mutable memory.

### Human-led action copilot

A human initiates and approves consequential steps. The agent prepares and explains actions but operates with lower autonomy.

### Event-driven persistent agent

An external workflow engine owns durable state. Identity and authority are reacquired for each event or step, and queued work remains cancelable and attributable.

### High-assurance transaction agent

Deterministic workflow surrounds bounded agent decisions, enhanced approval, prepare or commit or reconcile, and independent target-state assurance.

### Sandboxed research swarm

Agents use isolated ephemeral state, no production data or side-effecting tools, and strict aggregate time, cost, concurrency, and fan-out budgets.

### External managed agent platform

Enterprise-controlled identity, policy, tool gateway, evidence export, containment, portability, and exit remain mandatory across the provider boundary.

## Anti-patterns

- Shared API keys or service accounts across agents.
- Model-generated permissions, policy, approval, or credentials.
- Parent bearer credentials passed to children.
- Unlimited recursive spawning or spawning until solved.
- Tool access embedded directly in prompts or model runtime.
- Free-form inter-agent messages carrying executable instructions without provenance or schema.
- Global mutable memory across users, tenants, agents, or purposes.
- Memory, plans, tool text, or peer assertions treated as authoritative records.
- Approval of vague intent rather than a canonical exact action.
- Silent action substitution after denial or approval expiration.
- Retrying unknown consequential results without reconciliation.
- Best-effort compensation described as rollback.
- Kill switches implemented only inside the agent.
- Logging only final output rather than policy, approvals, actions, and effects.
- Persisting credentials, leases, or approval in memory.
- Allowing an agent or ordinary runtime administrator to alter authoritative evidence.
- Reporting tool transport success as proof of intended target outcome.

## Related patterns

- `ARC-P100` supplies shared model, provider, gateway, policy, identity, and evidence controls.
- `ARC-P110` uses bounded agents for human-facing enterprise assistance where approved.
- `ARC-P120` governs retrieval, context, grounding, citations, and semantic memory.
- `ARC-P140` defines enterprise-operated model and runtime infrastructure responsibilities.
- `ARC-P150` defines reusable tool and integration boundaries.
- `ARC-P160` defines shared agent evaluation, monitoring, detection, and assurance.

## Change history

| Pattern version | ESAF release | Date | Change |
|---|---|---|---|
| 0.1.0 | 0.4-alpha | 2026-07-12 | Initial draft |
