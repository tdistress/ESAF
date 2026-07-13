# ARC-P160 AI Observability Design

**Status:** Approved

**Target release:** 0.4-alpha

**Design date:** 2026-07-12

## 1. Purpose

ARC-P160 defines a vendor-neutral observability and assurance architecture for AI identity, input, context, retrieval, model, output, tool, action, policy, configuration, behavior, quality, performance, cost, evidence, and outcome signals.

## 2. Decision

Use an independent, privacy-tiered observability and assurance fabric.

Collection is distributed across material enforcement points, while telemetry contracts, correlation, privacy policy, evidence integrity, evaluation governance, detection policy, and assurance remain centrally governed. Regional, tenant, or high-assurance evidence stores may remain federated under the same contract.

The monitored runtime may emit events but cannot select, rewrite, suppress, or delete authoritative evidence or assurance verdicts. Operational dashboards and aggregated metrics cannot silently replace source evidence.

## 3. Objectives

The pattern shall:

- collect attributable, time-bounded, protected, risk-proportionate signals across complete AI request and action chains;
- authenticate telemetry sources and bind tenant, capability, purpose, version, environment, and region at collection;
- minimize content and use policy-governed capture modes;
- correlate ARC-P100 routes, ARC-P120 retrievals, ARC-P130 agents and actions, provider calls, target outcomes, incidents, and recovery;
- preserve source occurrence time, receipt time, processing time, sequence, clock quality, integrity, and custody;
- separate protected authoritative evidence from operational analytics;
- govern evaluation datasets, rubrics, labels, ground truth, adjudication, confidence, population limits, and uncertainty;
- distinguish data, input, retrieval, model, safety, agent, infrastructure, provider, and business-outcome drift;
- detect threats, policy violations, evidence gaps, provider changes, cost anomalies, and quality degradation;
- route actionable privacy-safe alerts into enterprise case, incident, containment, and recovery processes;
- enforce tenant isolation across collection, storage, queries, dashboards, exports, alerts, and evaluation;
- stop Tier 3 and Tier 4 consequential activity when required evidence or assurance becomes unknown.

## 4. Six-plane architecture

### 4.1 Governance and configuration plane

Maintains telemetry policy, source inventory, event schemas, field classifications, capture modes, sampling, retention, legal holds, alert policy, evaluation definitions, ownership, exceptions, and configuration history. Changes are versioned, independently authorized, tested, reversible, and audited.

### 4.2 Signal collection plane

Collects from channels, gateways, applications, orchestrators, models, retrieval, agents, tools, targets, data stores, providers, and administrative systems. It authenticates sources, validates schema, binds tenant, minimizes content, detects replay, applies rate and capacity controls, buffers locally, and confirms delivery.

### 4.3 Protected evidence plane

Stores authoritative events through independently administered append-only or WORM-capable controls. It preserves attribution, trusted or bounded time, sequence, integrity, receipt, retention, legal hold, access, and loss detection. Ordinary runtime and platform administrators cannot alter evidence.

### 4.4 Evaluation and ground-truth plane

Maintains versioned evaluation datasets, slices, rubrics, expected outcomes, labels, target-native outcomes, adjudication, evaluator identity, confidence, disagreements, effective dates, population limits, and known uncertainty. Model self-evaluation may be a signal but is not sole authority for consequential outcomes.

### 4.5 Detection and response plane

Performs stateful security correlation, policy-violation detection, quality and drift analysis, evidence-gap detection, alert routing, case creation, containment integration, and recovery verification. Critical rules operate independently of the runtime they monitor.

### 4.6 Analytics, service, and cost plane

Provides availability, latency, reliability, token, capacity, provider, cost, budget, quality, adoption, and business-value analysis. Aggregates retain traceability to governed source data and are not authoritative audit records.

### 4.7 Assurance independence

Assurance has organizational and technical independence from the teams operating monitored workloads. Assurance selects its own samples, has direct access to source and gap evidence, records conflicts of interest, and escalates material exceptions outside the monitored management chain. Runtime and platform operators cannot choose tested populations, suppress exceptions, or alter assurance conclusions.

## 5. Required telemetry contract

Authoritative events include, where applicable:

- schema name and version, event ID, event type, and capture mode;
- occurrence time, source clock quality, receipt time, processing time, and maximum uncertainty;
- source identity, attestation, component, version, deployment, environment, and region;
- tenant, capability, tier, lifecycle state, and approved purpose;
- trace, span, parent, session, workflow, transaction, and lineage identifiers;
- initiating principal, runtime identity, agent lineage, model, provider, retrieval, tool, target, policy, approval, and evaluation references;
- input, output, and content references with classification and capture mode;
- decision, reason code, policy version, result, error, latency, resource use, and cost;
- sequence, replay or duplicate status, integrity proof, delivery status, and gap indicator;
- retention class, residency, legal-hold status, and access class.

Stable identifiers correlate records without depending on raw prompts, personal email addresses, or mutable display names.

Externally supplied trace, span, parent, session, workflow, transaction, and lineage identifiers are untrusted. They are issued or validated at trust boundaries, bound to tenant and capability namespaces, collision- and reuse-checked, and regenerated when provenance cannot be established. Correlation identifiers never authorize access or action by themselves.

## 6. Privacy and content treatment

The four capture modes are:

1. **Metadata only:** default when content is unnecessary.
2. **Derived signal:** non-reconstructable classification, verdict, fingerprint, length, score, or feature.
3. **Redacted excerpt:** narrowly scoped diagnostic content under approved policy.
4. **Protected full content:** exceptional capture in a segregated content-evidence vault.

Sampling is purpose-bound, risk-approved, tenant-aware, reproducible where necessary, and documented. It cannot exclude denials, high-risk actions, incidents, evidence gaps, material policy decisions, or Tier 3 and Tier 4 outcome records.

Prompt and response bodies are not copied by default into general logs, traces, analytics, tickets, email, or chat. Debug capture is approved, visible, time-bounded, access-restricted, and automatically expires. Privacy correction and deletion propagate to derived stores where required, subject to valid authorized legal hold.

Fingerprints, embeddings, stable hashes, rare features, and other derived signals receive privacy classification and re-identification or linkability testing. Keyed or scoped transforms, tenant and purpose isolation, retention, deletion, and legal-hold requirements apply whenever derived signals remain identifiable or linkable.

## 7. Time, ordering, lineage, and integrity

The architecture does not assume perfect global ordering. It preserves source occurrence time and collector receipt time separately and records clock source, synchronization state, uncertainty, and sequence.

Causal parentage, source sequence, transaction state, and target-native evidence reconstruct order. The fabric detects duplicates, replay, gaps, late arrival, conflicting events, and clock regression.

Events or batches are signed, hashed, or equivalently integrity-protected at or near collection. Custody is recorded across collectors, queues, transforms, stores, exports, and archives. Transformations preserve source references, transformer identity and version, and before-and-after integrity relationships. Late events amend records explicitly and cannot silently rewrite reported results.

Signing and attestation controls define trust anchors, identity binding, key issuance, non-exportability where supported, rotation, revocation, compromise response, algorithm agility, verifier configuration, and time validity. A valid signature from a compromised or revoked source does not establish trustworthy evidence.

Evidence trust roots and timestamp anchors are administered separately from evidence storage. Periodic end-to-end verification detects privileged rewriting of both events and local proofs. Deletion and cryptographic erasure preserve signed tombstones, custody, and legal-hold proof without retaining prohibited content.

## 8. Evaluation, drift, and ground truth

Evaluation records bind capability, model, prompt, policy, retrieval corpus, tools, components, datasets, slices, rubric, evaluator, ground-truth source, adjudication, confidence, limitations, expected and actual results, threshold, decision, release, deployment, rollback, and incident.

Drift categories remain distinct:

- data-quality drift;
- input and population drift;
- embedding and retrieval drift;
- model behavior and output drift;
- safety and policy drift;
- tool and agent behavior drift;
- infrastructure and provider drift;
- business-outcome drift.

A drift alert is evidence of change, not proof of harm. Thresholds use approved baselines, confidence, minimum sample size, segment analysis, seasonality, and false-positive review. Tier 3 and Tier 4 success uses target-native outcomes or independently governed adjudication.

Ground-truth governance defines target-of-record provenance, outcome-finality windows, correction and version semantics, delayed and censored outcomes, missingness, intervention and confounding review, and separation of training or tuning data from holdout evidence. Transport success or model self-evaluation cannot substitute for causal or semantic outcome evidence.

## 9. Security detection scope

Detection covers, at minimum:

- prompt injection, context injection, and policy bypass;
- sensitive-data exposure and anomalous access;
- identity, tenant, purpose, or authority mismatch;
- model, prompt, policy, index, tool, runtime, or configuration drift;
- retrieval authorization failures and citation anomalies;
- agent authority amplification, recursive growth, loops, budget exhaustion, approval substitution, duplicate action, and unknown outcome;
- provider routing, failover, data-use, retention, and evidence-export change;
- source spoofing, telemetry injection, schema-rejection spikes, sequence gaps, suppression, collector disablement, and evidence deletion;
- anomalous cost, tokens, latency, errors, capacity, and cardinality;
- evaluator manipulation, benchmark contamination, label drift, and unexplained quality improvement.

## 10. Alert and incident integration

Actionable alerts carry severity, confidence, affected tenant, capability, tier, trace and evidence references, detector and rule version, observed and expected condition, privacy-safe summary, recommended containment, owner, route, escalation, response objective, suppression status, and incident, change, risk, or exception linkage.

Alerts enter enterprise case and incident processes. Suppression, tuning, closure, severity change, and containment are attributable and reviewed. Tier 3 and Tier 4 evidence gaps, contradictory target outcomes, integrity failures, and containment failures receive immediate escalation.

Automated response is treated as a consequential action and uses authorization, approval, idempotency, reconciliation, and target-state evidence appropriate to impact.

Automated response also constrains alert and event poisoning, adversarial threshold manipulation, false-positive storms, rate, concurrency, and blast radius. Broad containment requires independent confirmation or human approval according to risk, uses circuit breakers, and validates recovery so an attacker cannot disable many tenants or capabilities by manufacturing signals.

## 11. Multi-tenant isolation

Tenant identity is bound at the source and validated at ingestion. Access, encryption, indexes, searches, caches, dashboards, exports, evaluation datasets, alerts, tickets, retention, and deletion are tenant-scoped.

Cross-tenant analytics require approved aggregation or de-identification. Tenant identity is not trusted solely from user-supplied fields. Negative tests cover cross-tenant query, dashboard join, cache, export, evaluation, alert route, and incident-attachment leakage.

Isolation tests also cover high-cardinality and timing side channels, shared encryption keys and KMS policy, support and break-glass access, detector and evaluator training data, backup and restore, and tenant migration. Exceptional cross-tenant access requires dual authorization, bounded purpose and duration, and tenant-visible audit where appropriate.

## 12. External-provider evidence

Provider telemetry is externally asserted unless independently corroborated. Each integration documents available and missing fields, export delay and completeness, clock and identifier semantics, content and retention, subprocessors, residency, administrative visibility, outage, throttling, backfill, integrity, deletion, portability, and exit.

Enterprise-controlled boundaries compensate for material gaps. Where a gap prevents required assurance, the affected tier, action, or provider use is prohibited rather than represented as observable.

## 13. Safe failure and continuity

Tier 3 and Tier 4 consequential activity stops or cannot commit when authoritative evidence, approval correlation, target outcome, integrity verification, or required assurance is unavailable.

Lower-tier bounded activity may continue only through an approved degraded mode with protected local buffering, explicit duration and volume limits, visible status, and no increase in data, authority, provider, or action scope.

Buffer exhaustion, unverifiable telemetry, missing tenant binding, or inability to honor privacy policy causes fail-safe rejection. Monitoring failure cannot route around policy enforcement.

Recovery requires validated backfill, sequence reconciliation, integrity verification, gap disposition, material incident review, and authorized return to normal mode.

Each capability and action class has an approved observability applicability matrix defining commit-blocking evidence, authoritative source, maximum tolerated delay, degraded state, recovery condition, and change authority. Independent testing verifies that telemetry failure neither causes uncontrolled global halt nor permits bypass by reclassifying required evidence as optional.

## 14. Control points

| CP | Control point | Required outcome | Primary implementation and evidence owners |
|---|---|---|---|
| CP1 | Telemetry governance and schema registry | Versioned contracts, field classification, ownership, compatibility, and change control | AI Service Owner, Data Governance, Platform Engineering |
| CP2 | Source instrumentation and identity | Attributable signals from every material decision and enforcement point | Workload Owner, Observability Platform, Identity and Access Management |
| CP3 | Edge minimization and content policy | Apply approved capture mode before general telemetry distribution | Data Owner, Privacy, Ingestion Engineering |
| CP4 | Secure ingestion and tenant binding | Authenticate source, validate schema, bind tenant, reject replay, quarantine invalid events, and enforce limits | Observability Platform, Identity and Access Management, Tenant Owner |
| CP5 | Correlation and lineage service | Reconstruct principal-to-model-to-retrieval-to-agent-to-tool-to-outcome paths | AI Service Owner, Source and Workload Owners |
| CP6 | Time, sequence, and integrity service | Preserve causal order, uncertainty, duplicates, gaps, signatures, transformation lineage, and custody | AI Service Owner, Evidence Custodian, Platform Engineering |
| CP7 | Protected evidence store | Maintain independently controlled append-only authoritative evidence with scoped access | AI Service Owner accountable; Evidence Custodian and Platform Engineering implement |
| CP8 | Evaluation and ground-truth registry | Govern datasets, labels, rubrics, evaluators, adjudication, outcome provenance, confidence, and limitations | Model Validation Lead, Data Owner, Assurance |
| CP9 | Drift and quality analytics | Detect material change by slice with confidence and approved thresholds | Model Owner, Evaluation and ML Operations |
| CP10 | Security detection and correlation | Detect abuse, policy bypass, authority misuse, evidence tampering, and provider gaps | Security Operations, Detection Engineering |
| CP11 | Alert, case, and incident broker | Route privacy-safe actionable alerts and preserve response decisions | Security Operations, Service Operations, Incident Response |
| CP12 | Cost, capacity, and service monitoring | Attribute usage and detect exhaustion, runaway behavior, and degradation | AI Service Owner, Site Reliability Engineering, Financial Operations |
| CP13 | Retention, residency, deletion, and legal hold | Enforce lifecycle obligations across raw, derived, archived, ticketed, and exported telemetry | Data Owner, Privacy, Compliance, Records Management |
| CP14 | Evidence continuity and degraded-mode controller | Detect loss, bound buffering, stop unsafe activity, reconcile backfill, and authorize recovery | Business Continuity, AI Service Owner, Site Reliability Engineering; Assurance verifies |
| CP15 | Assurance and reporting | Independently verify completeness, control operation, outcomes, and executive reporting | Executive Leadership accountable for management review; Internal Audit and Assurance independently assess |

## 15. Variants

- **Central assurance fabric:** shared platform and evidence store where residency and tenant requirements permit.
- **Federated regional fabric:** regional collection and evidence with centrally governed schemas and aggregated assurance.
- **High-assurance enclave:** isolated evidence, evaluation, and detection for Tier 4 or regulated workloads.
- **Provider-assisted observability:** provider signals supplement enterprise-controlled boundary telemetry.
- **Edge or disconnected:** signed local journal with bounded offline operation and verified reconciliation.
- **Privacy-maximized:** metadata and derived signals by default with exceptional protected-content capture.
- **Research and experimentation:** broader diagnostic sampling in isolated non-production environments, never silently promoted to production.

## 16. Anti-patterns

- Logging only final prompts and responses.
- Treating application logs, dashboards, provider consoles, or aggregate metrics as authoritative evidence.
- Collecting all content just in case.
- Sampling that omits denials, incidents, evidence gaps, or consequential actions.
- Correlating through raw content or personal identifiers.
- Letting monitored runtimes or ordinary administrators delete evidence or select assurance results.
- Assuming timestamps alone establish global order.
- Using average quality without population slices, confidence, or limitations.
- Letting a model grade itself as sole quality or safety authority.
- Alerting raw sensitive content into tickets, email, or chat.
- Sharing telemetry indexes, query roles, exports, or caches across tenants without isolation.
- Silently dropping events under load.
- Continuing Tier 3 or Tier 4 actions when evidence is incomplete.
- Retaining excerpts, embeddings, exports, tickets, or derived data outside governing lifecycle policy.
- Changing telemetry configuration without versioning, testing, approval, and audit.

## 17. Control alignment

`MON-100`, `MON-110`, `MON-120`, `MON-140`, and `MON-150` are required. `MON-130` is conditionally applicable when agent workloads are monitored; the fabric nevertheless supports the schemas and correlation needed to onboard agents without redesign.

Required supporting controls are:

- Governance and risk: `GOV-130`, `RSK-110`, `RSK-120`, `RSK-140`.
- Assurance: `AUD-100`, `AUD-110`, `AUD-120`, `AUD-130`, `AUD-140`.
- Operations: `OPS-100`, `OPS-110`, `OPS-120`, `OPS-130`, `OPS-140`.
- Data: `DAT-100`, `DAT-110`, `DAT-120`, `DAT-130`.
- Identity: `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-140`, `IAM-150`.
- Compliance: `CMP-100`, `CMP-110`.
- Platform and integration: `INF-140`, `INF-150`, `API-110`.
- Architecture: `ARC-100`, `ARC-110`, `ARC-130`, `ARC-140`.
- Application: `APP-100`, `APP-110`, `APP-120`, `APP-130`, `APP-140`, `APP-150`.
- Model: `MOD-100`, `MOD-120`, `MOD-130`.

`ARC-120`, `ARC-150`, `OPS-150`, and `MOD-140` are normally inherited or consumed and must be verified. Conditional controls include `DAT-140`, `DAT-150`, `DAT-160`, `CMP-120`, `CMP-130`, `CMP-140`, `MOD-110`, `MOD-150`, `API-140` for provider-assisted observability, and `AGT-100` through `AGT-160` according to data, providers, jurisdiction, intellectual property, models, and agent workloads.

Catalog `owner_role` remains accountable. Pattern roles identify implementation and evidence responsibility without transferring accountability.

## 18. Evidence model

Required evidence includes:

- a control-point assurance matrix mapping every control point to applicable catalog controls, accountable and evidence-producing roles, evidence artifacts, assessment procedures, and the objective being demonstrated;

- telemetry inventory, source owners, source-to-schema coverage, and gap register;
- event contracts, compatibility tests, field classifications, capture modes, and version history;
- representative end-to-end traces for applicable patterns and tiers;
- tenant isolation and access tests;
- sampling, minimization, redaction, debug, and protected-content approvals;
- integrity, sequence-gap, late-event, replay, clock-skew, transformation-lineage, and custody tests;
- provider gap and compensating-control assessments;
- evaluation datasets, slices, rubrics, ground-truth provenance, adjudication, confidence, and contamination controls;
- drift baselines, thresholds, segment results, uncertainty, and tuning decisions;
- detection rules, alerts, cases, incidents, suppression approvals, and response exercises;
- cost, capacity, cardinality, budget, and runaway-workload evidence;
- retention, deletion, residency, archive, export, ticket, and legal-hold tests;
- collector outage, buffering, exhaustion, backfill, safe-stop, reconciliation, and recovery exercises;
- independent assurance that runtimes and ordinary administrators cannot suppress evidence or alter verdicts.

Negative tests include missing, late, duplicate, out-of-order, replayed, and spoofed events; clock skew; schema drift; telemetry injection; cross-tenant access; privileged alteration; secret and personal-data leakage; retention and legal hold; unauthorized rule change; suppression abuse; routing failure; backpressure; provider outage; evidence integrity failure; and unsafe automated response.

Assessment explicitly verifies that monitored runtimes and ordinary administrators cannot suppress, alter, or select authoritative evidence or assurance verdicts; that Tier 3 and Tier 4 consequential commits fail safely when required evidence, correlation, or outcome capture is unavailable; and that degraded-mode expiry or buffer exhaustion causes the approved safe stop rather than silent continuation.

## 19. Acceptance criteria

ARC-P160 is complete when:

- every pattern-template section is substantively populated;
- all six planes, four capture modes, and fifteen control points are represented;
- telemetry contract, correlation, time, integrity, privacy, evaluation, drift, detection, alerting, tenancy, provider gaps, and safe failure are explicit;
- control owners and evidence producers are assigned;
- required, inherited, and conditional controls resolve;
- evidence and negative assessment scenarios are testable;
- the registry links ARC-P160 and changes its state to Draft;
- unit, architecture, control, PR, and post-merge validation pass.

## 20. Out of scope

This milestone does not include vendor configuration, observability product selection, infrastructure code, universal quality thresholds, production dashboards, external-standard crosswalk claims, or industry-specific retention schedules.
