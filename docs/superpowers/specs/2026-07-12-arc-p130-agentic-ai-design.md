# ARC-P130 Agentic and Multi-Agent AI Design

**Status:** Approved

**Target release:** 0.4-alpha

**Design date:** 2026-07-12

## 1. Purpose

ARC-P130 defines a vendor-neutral architecture for agents that plan, delegate, use tools, maintain state, communicate with other agents, or initiate consequential actions. The pattern preserves human and organizational accountability by separating model reasoning from identity, authority, approval, transaction execution, evidence, and containment.

## 2. Decision

Use a policy-mediated agent runtime with bounded authority leases and transactional action execution.

The model may propose plans, tasks, delegation, memory changes, messages, and tool calls. Enforceable identity, authority, approval, execution, and intervention remain outside the model. Every action is independently authorized against current policy and a short-lived lease. Consequential side effects use prepare, approval or commit, and outcome reconciliation stages.

Multi-agent communication is authenticated but treated as untrusted input. A message, plan, memory record, or peer assertion cannot create authority. Child agents receive unique identities and attenuated leases, never inherited bearer credentials or implicit transitive permission.

## 3. Security invariants

1. Every agent instance has a unique managed runtime identity, accountable owner, approved purpose, tier, version, parent lineage, and lifecycle state.
2. An agent cannot create, enlarge, renew, transfer, reinterpret, or approve its own authority.
3. Authority leases are short-lived, integrity-protected, audience-bound, purpose-bound, revocable, and externally issued.
4. Delegated authority is an attenuated subset of both the delegator's current authority and the initiating principal's authority.
5. Plans and model outputs are proposals, never authorization decisions.
6. Tool results, peer messages, retrieved content, memory, and environmental observations remain untrusted data.
7. Consequential side effects use typed, policy-authorized, approval-aware transactional execution with idempotency and outcome reconciliation.
8. Recursive spawning is disabled by default and otherwise bounded by depth, breadth, duration, concurrency, cost, purpose, and aggregate authority.
9. Memory cannot become authoritative policy, identity, approval, entitlement, credential, or transaction state.
10. Pause, containment, lease revocation, and emergency termination remain available outside the agent runtime.
11. Failure, stale authority, lost approval, or uncertain outcome causes abstention, containment, reconciliation, or escalation rather than blind retry or broader fallback.
12. Every material action remains attributable to the initiating principal, agent lineage, policy, lease, approval, execution request, and verified outcome.
13. Effective authority at execution is the intersection of current principal or service authority, agent lease, enterprise policy, target-native authorization, data policy, and valid approval.
14. Consequential commit requires a fresh authorization and revocation check; cached or offline authority is bounded and fails closed outside its approved validity.

## 4. Objectives

The pattern shall:

- register and identify every agent, instance, parent, owner, purpose, version, deployment, and lifecycle state;
- constrain data, tools, targets, operations, resources, time, spend, side effects, persistence, and delegation outside the model;
- separate intent, authority, execution, and evidence flows;
- validate plans, messages, tool parameters, memory, and output according to trust and authority;
- require risk-proportionate human approval, supervision, intervention, challenge, and appeal;
- execute consequential actions with immutable previews, idempotency, concurrency control, compensation, and reconciliation;
- protect agent memory and durable workflow state with explicit ownership, provenance, authorization, reliability, retention, correction, and deletion;
- prevent authority amplification, recursive explosion, orphaned work, approval substitution, and uncontrolled persistence;
- provide end-to-end action traceability without requiring hidden chain-of-thought;
- support out-of-band pause, isolation, termination, descendant shutdown, rollback, recovery, and authorized resumption.

## 5. Non-goals

ARC-P130 does not prescribe agent frameworks, reasoning methods, model providers, orchestration products, or hidden chain-of-thought collection. It does not treat prompts as authorization, guarantee that a planned action is correct, or make every AI workflow autonomous.

The pattern does not replace ARC-P100 provider controls, ARC-P120 retrieval controls, target-system authorization, human accountability, or domain-specific transaction and safety standards.

## 6. Logical architecture

```text
Initiating Principal
  -> Identity and Purpose Binding
  -> Agent Admission and Runtime Identity
  -> Policy and Authority-Lease Service
  -> Planner and Orchestrator
       -> Delegation Broker -> Child or Peer Agents
       -> Memory and State Broker
       -> Tool and Action Gateway
            -> Human Approval Service
            -> Transaction Coordinator
            -> Enterprise Action Targets
            -> Outcome Reconciliation
  -> Evidence, Detection, Containment, and Recovery
```

The authoritative agent definition, lineage graph, policy, lease, approval, transaction, and intervention state exist outside model context.

Agent admission binds workload identity cryptographically, or through an equivalent attestation mechanism, to the approved agent definition, tenant, model and orchestrator versions, deployment, environment, and runtime instance. Credentials are non-exportable where supported. Cloned, altered, unattested, or unapproved runtimes cannot use the agent identity or its leases.

## 7. Flow separation

| Flow | Contents | Rule |
|---|---|---|
| Intent | User objective, constraints, context, and approved purpose | May influence planning but cannot create authority |
| Authority | Identity, policy, lease, delegation, approval, revocation, and emergency control | Integrity-protected and evaluated outside the model |
| Execution | Plans, messages, tool requests, transaction preparation, commit, compensation, and result | Typed, authorized, bounded, idempotent where required, and reconciled |
| Evidence | Decisions, lineage, messages, actions, approvals, outcomes, alerts, containment, and recovery | Attributable, correlated, minimized, protected, and independent from agent modification |

Authority metadata shall not be inferred from intent or execution content.

## 8. Authority lease contract

Each lease records:

- lease ID, issuer, subject agent, initiating principal, tenant, capability, purpose, and audience;
- parent lease and complete delegation lineage;
- permitted tools, operations, targets, data classes, jurisdictions, and environments;
- prohibited actions and non-delegable permissions;
- maximum delegation depth, child count, concurrency, duration, cost, steps, calls, and side effects;
- human-approval requirements and maximum transaction values;
- issue, not-before, expiration, policy version, nonce, and revocation reference;
- fail-closed behavior and external renewal authority.

Leases are single-purpose and short-lived by default. Renewal requires external policy evaluation. Material changes to identity, purpose, target, tool, risk, policy, or approval invalidate or narrow the lease. The design specifies maximum clock skew, cache age, revocation propagation latency, offline enforcement behavior, and acknowledgment from each enforcement point.

Immediately before a consequential commit, the execution boundary recomputes effective authority as the intersection of current initiating-principal or service authority, agent lease, enterprise policy, target-native authorization, data policy, and valid approval. Scheduled, event-driven, and service-initiated agents use an accountable managed service principal with an approved purpose and authority baseline; absence of an interactive human does not create ambient authority.

## 9. Planning and delegation

Plans identify intended actions, dependencies, constraints, side effects, approval gates, rollback or compensation, evidence, and termination conditions. A planner cannot authorize its own proposal.

Replanning after denial, failure, changed input, expired approval, or uncertain outcome shall not silently substitute a new tool, target, transaction, provider, or data source. The replacement is re-evaluated and reapproved where required.

Each child receives a new identity and attenuated lease. Parent termination or revocation propagates to descendants unless a documented independent-ownership transfer is approved. The orchestrator maintains an authoritative lineage graph, detects cycles and orphaned work, and prevents peers from granting authority by instruction.

Scheduled jobs, callbacks, broker messages, external workflow tokens, target-side jobs, and delayed retries carry lineage and lease references. They support cancellation or tombstoning and are inventoried and reconciled during containment so durable work cannot escape descendant shutdown.

Dynamic or recursive spawning is prohibited for Tier 3 and Tier 4 unless specifically risk-approved and deterministically bounded.

## 10. Human oversight and approval

The oversight model classifies actions by impact, reversibility, uncertainty, affected parties, legal duties, safety, financial value, data disclosure, production effect, and exception status.

An approval request presents:

- action, business purpose, exact tool, operation, target, and material parameters;
- expected side effects, affected parties, data disclosure or change, and limitations;
- initiating identity, agent lineage, lease, policy decision, and exceptions;
- reversibility, rollback, compensation, and unknown-outcome risks;
- expiration, single-use status, and approver authority.

Approval binds to an immutable action digest. Changes to parameters, target, tool, lease, data, or risk require reapproval. Silence, timeout, prior similar approval, or agent self-evaluation is not approval.

Approval policy defines authentication strength, eligible roles, conflicts of interest, self-approval prohibitions, quorum or dual approval, and emergency authority. Where independence is required, the initiating principal, agent owner, tool owner, transaction beneficiary, and operator cannot approve their own action. Emergency approval is time-bounded and receives independent reconciliation.

## 11. Tool and action execution

Every tool is registered with owner, purpose, schema, identity, permissions, targets, data, side effects, limits, approval requirements, failure behavior, monitoring, change history, and retirement state.

Consequential actions use three stages where feasible:

1. **Prepare:** validate and reserve without external effect; produce an immutable preview and action digest.
2. **Approve and commit:** bind current policy, lease, target authorization, human approval, and idempotency key to the prepared transaction.
3. **Reconcile:** independently confirm target state and classify the outcome as committed, failed, compensated, or unknown.

Unknown outcomes enter reconciliation and block contradictory follow-on actions. Non-idempotent or unknown-result actions are never blindly retried. Compensation is distinguished from atomic rollback and its limitations are disclosed.

The action digest uses a canonical representation and binds exact parameters, target identity and version, source-data versions, prepared target state, policy and lease versions, approval, idempotency key, reservation expiry, and expected preconditions. Target state and authority are revalidated atomically at commit; any mismatch aborts and requires re-prepare and reapproval.

A Tier 3 or Tier 4 tool that cannot support transactional execution requires documented risk acceptance and stronger immutable preview, approval, duplicate suppression, constrained scope, post-action verification, outcome reconciliation, and domain recovery.

## 12. Memory and durable state

The pattern separates ephemeral reasoning state, session memory, user-approved preferences, workflow state, durable enterprise records, and shared multi-agent state.

Memory records include owner, subject, tenant, purpose, provenance, writer, source, timestamp, reliability, classification, version, retention, and correction or deletion state. Reads and writes are authorized independently. Untrusted memory is validated and cannot expand authority.

Authoritative workflow and transaction state live outside model context. Summaries do not replace source records. Persistent agents reauthenticate and reacquire authority after restart; credentials, leases, and approvals are not restored from memory.

## 13. Multi-agent communication

Inter-agent channels authenticate sender and receiver, constrain permitted conversation purpose, validate typed envelopes, preserve provenance and classification, prevent replay, enforce rate and size limits, and correlate messages to lineage and task.

Messages and peer claims remain untrusted. Agents cannot delegate by message alone, and no receiver may infer authority from a claimed role, plan, instruction, or parent relationship. Shared state uses brokered authorization, versioning, conflict resolution, and isolation.

## 14. Trust-zone mapping

| Crossing | Required treatment |
|---|---|
| Z1 to Z3 agent admission | Bind principal, tenant, capability, purpose, tier, session, risk, and budget; create runtime identity |
| Z2 to Z3 authority lease | Issue integrity-protected, short-lived, audience-bound, revocable authority with explicit limits |
| Z3 planner to executor | Treat plan as untrusted proposal; validate schema, policy, lease, limits, and current context |
| Z3 agent to agent | Authenticate parties; validate envelope, purpose, provenance, classification, replay, correlation, and limits |
| Z3 to Z5 memory | Broker read and write by identity, tenant, purpose, provenance, reliability, retention, version, and conflict policy |
| Z3 to Z6 tool or target | Validate identity, lease, arguments, target, data, risk, approval, idempotency, and transaction state |
| Z3 or Z6 to Z7 approval | Bind human decision to immutable action digest, scope, agent, lease, approver, and expiration |
| Z6 to Z3 outcome | Return authenticated typed result with target transaction ID and committed, failed, compensated, or unknown state |
| Z7 to Z3 containment | Apply out-of-band pause, isolation, revocation, termination, restoration, and authorized resumption |
| Z3 or Z6 to Z7 evidence | Emit attributable policy, lease, plan, message, tool, approval, transaction, result, memory, and lineage events |

## 15. Control points

| CP | Control point | Required outcome | Primary implementation and evidence owners |
|---|---|---|---|
| CP1 | Agent registration and admission | Verify definition, owner, purpose, tier, model and orchestrator versions, deployment, attested runtime identity, parent lineage, and lifecycle state | Agent Owner, IAM, and Platform Engineering |
| CP2 | Authority lease issuance | Issue minimal external authority bound to principal, agent, tenant, purpose, audience, tools, targets, actions, budgets, delegation, expiry, policy, and revocation | Agent Owner, IAM, and policy-service owner |
| CP3 | Planning and task decomposition | Constrain objective, horizon, iteration, resources, termination, prohibited outcomes, and replanning; validate plan as proposal | Agent Owner and Application Engineering |
| CP4 | Delegation and spawn broker | Enforce attenuation, attribution, recipient eligibility, depth, breadth, concurrency, cost, expiry, revocation propagation, and orphan handling | Agent Owner and orchestration-platform owner |
| CP5 | Inter-agent message gateway | Authenticate agents and validate typed contracts, purpose, provenance, classification, replay, rate, size, and instruction trust | AI Platform Owner and Agent Owner |
| CP6 | Memory and state broker | Enforce scoped reads and writes, isolation, provenance, reliability, conflict control, retention, correction, deletion, and poisoning defense | Agent Owner, Data Owner, and state-platform owner |
| CP7 | Tool registry and invocation gateway | Permit only registered operations; validate schema, arguments, target, data, secrets, rate, output, and current authority | AI Platform Owner, tool owner, and target-system owner |
| CP8 | Human approval service | Bind eligible and independent approval to exact action digest, target, parameters, agent, lease, expiry, and approver authority | Business or risk approval authority and approval-service owner |
| CP9 | Transaction and side-effect coordinator | Separate prepare, commit, and reconcile; enforce canonical digest, idempotency, concurrency, duplicate suppression, retry, and compensation | Target-system or transaction owner and Platform Engineering |
| CP10 | Runtime supervision and budgets | Enforce time, steps, tokens, cost, calls, fan-out, data, resource, and side-effect budgets; detect loops, deadlocks, and escalation | AI Platform Owner and Platform Operations |
| CP11 | Evidence and detection | Correlate principal, lineage, messages, plans, policy, leases, approvals, tools, transactions, outcomes, memory, and administration | AI Service Owner, Security Operations, and assurance |
| CP12 | Containment, kill, and recovery | Revoke leases, block tools, stop dispatch, isolate state, terminate descendants, reconcile durable and in-flight actions, restore state, and require authorized resumption | Incident Response, Platform Operations, and Agent Owner |
| CP13 | Outcome assurance | For Tier 3 and Tier 4, independently compare approved intent with authoritative target state before reporting success | Independent validation or assurance owner and target-system owner |

## 16. Safe failure

| Failure | Required treatment |
|---|---|
| Policy service unavailable | No new consequential authority; bounded read-only behavior only if preapproved |
| Lease expired or unverifiable | Stop affected work, preserve state, revoke dependent work, and request reauthorization |
| Approval unavailable or expired | Queue safely or abstain; never reinterpret silence as approval |
| Tool timeout or unknown result | Reconcile before retry and block contradictory dependent actions |
| Memory inconsistency or poisoning | Quarantine state and continue only through an approved stateless or known-good mode |
| Peer conflict | Stop conflicting actions and use deterministic arbitration or human review |
| Budget exceeded or loop detected | Halt, summarize attributable state, stop descendants as needed, and release resources |
| Evidence failure | Stop Tier 3 and Tier 4 consequential actions; lower tiers use only approved bounded buffering |
| Kill signal | Stop dispatch, revoke leases, require acknowledgment from every reachable enforcement point, terminate descendants, enumerate unreachable targets, classify and reconcile in-flight or queued actions, preserve evidence, and require authorized recovery; committed effects require compensation or domain recovery |
| Provider or model degradation | Do not fail over to broader data use, authority, tools, providers, or action semantics without prior approval |

Tier 3 and Tier 4 outcome assurance is separately controlled from the planner and executor. It uses target-native state, transaction records, or other authoritative evidence to verify semantic outcome rather than transport success. Verification is time-bounded and includes affected-party or downstream-state checks where applicable. Success remains unknown while evidence is unavailable, stale, contradictory, or incomplete.

## 17. Variants

- **Single bounded agent:** one agent, limited tools, no delegation; preferred default.
- **Supervisor-worker:** supervisor decomposes tasks and issues attenuated child leases; workers cannot spawn by default.
- **Peer collaboration:** typed messages and deterministic conflict policy; no implicit shared authority.
- **Human-led action copilot:** human initiates and approves consequential steps; lower autonomy.
- **Event-driven persistent agent:** durable workflow state is external; identity and authority are reacquired per event or step.
- **High-assurance transaction agent:** deterministic workflow shell, prepare or commit or reconcile, enhanced approval, and outcome assurance.
- **Sandboxed research swarm:** isolated ephemeral state, no production data or side-effecting tools, strict aggregate budgets.
- **External managed agent platform:** enterprise-controlled identity, tool gateway, policy, evidence, containment, portability, and exit remain mandatory.

Tier 3 and Tier 4 should prefer deterministic workflows around bounded agent steps rather than open-ended loops.

## 18. Anti-patterns

- Shared API keys or service accounts across agents.
- Model-generated permissions, policy decisions, approvals, or credentials.
- Parent bearer credentials passed to child agents.
- Unlimited recursive spawning or spawning until a result appears.
- Tool access embedded directly in prompts or model runtime.
- Free-form agent messages carrying executable instructions without provenance or schema.
- One global mutable memory store across users, tenants, agents, or purposes.
- Memory, plans, tool text, or peer assertions treated as authoritative records.
- Approval of vague intent rather than an immutable exact action.
- Silent substitution after denial, changed conditions, or approval expiration.
- Retrying timed-out consequential actions without reconciliation.
- Claiming rollback where only best-effort compensation exists.
- Kill switches implemented solely inside the agent being stopped.
- Logging only final answers rather than decisions, approvals, and side effects.
- Persisting credentials, leases, or approval in agent memory.
- Allowing agents to alter or delete their evidence.

## 19. Control alignment

All agent controls `AGT-100` through `AGT-160` are required.

Required supporting groups are:

- Governance and risk: `GOV-130`, `RSK-110`.
- Identity: `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-140`, `IAM-150`.
- APIs and tools: `API-110`, `API-120`, `API-130`.
- Applications: `APP-100`, `APP-110`, `APP-120`, `APP-130`, `APP-140`, `APP-150`.
- Data: `DAT-100`, `DAT-110`, `DAT-120`, `DAT-130`, `DAT-160`.
- Monitoring: `MON-100`, `MON-110`, `MON-120`, `MON-130`, `MON-140`, `MON-150`.
- Operations: `OPS-100`, `OPS-110`, `OPS-120`, `OPS-130`, `OPS-140`.
- Architecture: `ARC-100`, `ARC-110`, `ARC-130`, `ARC-140`.
- Model and infrastructure: `MOD-120`, `INF-150`.

`API-100`, `ARC-120`, `ARC-150`, `MOD-100`, `INF-100`, and `INF-130` are normally inherited and must be verified through configuration, sample traces, limitations, and failure tests. Conditional controls include `API-140`, `API-150`, `DAT-140`, `DAT-150`, and `OPS-150` according to external services, concentration, personal data, semantic memory, and retirement.

Catalog `owner_role` remains accountable. Pattern roles identify implementation and evidence responsibility without transferring accountability.

## 20. Evidence model

Required evidence includes:

- agent and system inventories, owners, purposes, tiers, versions, deployments, identities, and lineage;
- architecture, data, authority, execution, evidence, memory, delegation, tool, and transaction flows;
- identity, lease issuance, policy, revocation, permissions, limits, delegation, and denial records;
- tool registry, schemas, targets, side effects, approvals, tests, monitoring, changes, and retirement;
- plan and replan records at an assurance-appropriate level without requiring hidden chain-of-thought;
- inter-agent message envelopes, provenance, replay, validation, and delivery outcomes;
- memory read, write, correction, deletion, provenance, and conflict records;
- approval preview, exact action digest, approver, authority, decision, expiration, and use;
- prepare, idempotency, commit, compensation, reconciliation, and target-state evidence;
- principal-to-descendant-to-action correlated traces;
- behavior, loop, budget, escalation, denial, approval, unknown-outcome, and evidence alerts;
- containment, lease revocation, tool blocking, kill, descendant termination, reconciliation, recovery, and authorized-resumption exercises;
- adversarial tests for injection, confused deputy, authority amplification, replay, forged messages, memory poisoning, duplicate actions, approval substitution, recursive explosion, and evidence loss;
- service, change, incident, continuity, capacity, cost, and retirement records.

Evidence is exported to a separately administered append-only or WORM-capable store with trusted timestamps, ordering or sequence integrity, access control, retention, verification, and evidence-loss detection. Agents and ordinary runtime administrators cannot alter or delete authoritative evidence.

Assessment shall recompute tier, risk, and baseline for representative agents and confirm that authority, oversight, assurance, and failure behavior change accordingly. Tier 3 and Tier 4 outcome assurance shall independently compare the canonical approved action digest with authoritative target state and test committed, failed, unknown, duplicate, partial, compensated, stale-approval, and mismatched-target outcomes. Success is not reported while assurance is unavailable, contradictory, or unknown.

## 21. Acceptance criteria

ARC-P130 is complete when:

- every pattern-template section is substantively populated;
- all fourteen invariants and thirteen control points are represented;
- identity, lease, planning, delegation, messaging, memory, tools, approval, transactions, supervision, evidence, containment, and outcome assurance are explicit;
- required, inherited, and conditional controls resolve and owners are assigned;
- safe failure, variants, anti-patterns, and evidence are testable;
- the registry links ARC-P130 and changes its state to Draft;
- unit, architecture, control, PR, and post-merge validation pass.

## 22. Out of scope

This milestone does not include product configuration, infrastructure code, universal autonomy thresholds, hidden chain-of-thought collection, external-standard crosswalk claims, or domain-specific transaction and safety rules.
