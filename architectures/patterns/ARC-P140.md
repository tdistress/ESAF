# ARC-P140 Private model deployment

## Metadata

**Pattern ID:** ARC-P140

**Status:** Draft

**Version:** 0.1.0

| Field | Value |
|---|---|
| Owner | Enterprise Architecture |
| Required reviewers | Security Architecture, Model Validation, Data Governance, Legal, Privacy, AI Platform Engineering, Operations, Business Continuity, Records Management, Assurance |
| Approval date | Not approved (Draft) |
| Review date | Before approval; then at the organization-defined architecture review interval |
| Pillars | Protect AI, Utilize AI, Govern AI |
| Lifecycle stages | Model selection, Data readiness, Architecture, Development, Validation, Approval, Deployment, Operations, Monitoring, Continuous improvement, Retirement |
| Capability tiers | Tier 1 through Tier 4; isolated Tier 0 experimentation |
| Deployment models | On-premises, private cloud, dedicated hosted, hybrid, regional, confidential computing, disconnected or edge |
| Primary pattern role | Primary private-model lifecycle and serving pattern |
| Supersedes | None |

## Purpose

Provide a vendor-neutral controlled model supply chain and federated serving fabric for enterprise-controlled acquisition, adaptation, release, custody, deployment, private inference, revocation, and retirement. Private denotes custody and control boundaries; network placement or a private label is not evidence of confidentiality, integrity, safety, isolation, or compliance.

## Problem statement

Model weights are only one part of an executable release. Tokenizers, templates, loaders, adapters, kernels, dependencies, runtimes, drivers, firmware, safety settings, and hardware compatibility can change behavior or introduce hostile code. Without one immutable release identity and separated lifecycle gates, inspection can be bypassed between download and load, suppliers or administrators can silently substitute components, derived artifacts lose license and data obligations, and shared serving leaks tenant state. Distributed deployments also make revocation, recovery, evidence, and destruction difficult to prove.

## Intended outcomes

- Attributable source, supplier, license, lineage, transformation, ownership, and custody.
- Hostile-artifact containment and sanitized promotion before any trusted use.
- Authorized, reproducible adaptation with classified intermediate artifacts and deletion propagation.
- Independently validated, purpose- and tier-scoped, immutable signed release closures.
- Authoritative registry history, governed trust anchors, encrypted custody, and immutable runtime admission identity.
- Empirically demonstrated tenant, adapter, scheduler, cache, accelerator, telemetry, backup, support, and administrative isolation.
- Deny-by-default inference egress, governed import and export, extraction resistance, fair capacity, and safe failure.
- Independent ARC-P160 evidence for fleet impact, incidents, recovery, revocation, retirement, and verifiable destruction.

## Non-goals

This pattern does not define foundation-model pretraining from scratch, select model or accelerator products, prescribe universal performance, safety, or side-channel thresholds, implement a data-engineering platform, configure a particular cloud service, claim confidential computing eliminates infrastructure risk, or assert mappings to external standards.

## Applicability

Use ARC-P140 when the enterprise operates or controls model artifacts and private inference, including acquired, open, commercial, internally developed, fine-tuned, adapter-based, quantized, converted, pruned, or packaged models. Apply it across on-premises, private-cloud, dedicated-hosted, hybrid, regional, confidential-computing, and disconnected or edge forms. Tier 1 through Tier 4 use risk-proportionate controls; Tier 4, incompatible legal or data domains, untrusted adapters, or unbounded side-channel risk require dedicated boundaries. Tier 0 is limited to governed, isolated experimentation without production data, authority, or promotion paths.

Adaptation and build activities, evidence, CP6 and CP7 apply when fine-tuning, adapter creation, quantization, conversion, pruning, packaging, or another material transformation occurs. An inference-only deployment records CP6 and CP7 as not applicable with rationale; CP1 through CP5 and CP8 through CP21 remain applicable. Provider-operated endpoints lacking sufficient enterprise control and evidence over artifact identity, runtime integrity, isolation, lifecycle, and destruction remain external services.

## Assumptions and prerequisites

- Enterprise identity, classification, privacy, legal, procurement, key management, change, incident, continuity, records, and assurance services exist.
- Capability purpose, tier, owners, approved uses, data authority, residency, recovery objectives, and evidence retention are decided before promotion.
- Organization-defined limits exist for evidence and attestation freshness, trusted-time skew, isolation leakage, extraction, capacity, offline duration, revocation latency, and recovery.
- ARC-P160 supplies independently administered, append-only or WORM-capable authoritative evidence with trusted time and gap detection.
- Source and provider assertions are classified by assurance strength; contracts or physical placement do not erase supplier boundaries.

## Prohibited uses

Do not use this pattern to justify direct production downloads, mutable tags as identity, unrestricted runtime internet access, self-approval across build or release boundaries, silent component or provider substitution, shared serving without empirical isolation evidence, restoration of ineligible artifacts, or unverifiable retirement. It cannot support acceptable risk when immutable release identity, current authorization, license compatibility, independent validation, trust-anchor integrity, required isolation, revocation, evidence, or destruction cannot be established.

## Architecture views

### Figure 1. Context and custody view

```mermaid
flowchart LR
  S["Approved suppliers and enterprise sources"] --> L["Controlled model supply chain"]
  D["Authorized adaptation data and build inputs"] --> L
  L --> R["Immutable signed release and registry custody"]
  R --> F["Federated private serving fabric"]
  C["Authorized capabilities and tenants"] --> F
  F --> C
  L -. "independent evidence" .-> E["ARC-P160 evidence, operations, and assurance"]
  R -. "custody and state" .-> E
  F -. "runtime and outcome evidence" .-> E
```

Custody is recorded for artifacts, keys, data, compute, firmware, administration, backups, telemetry, support, and destruction. Shared responsibility remains explicit across hosted and regional boundaries.

### Figure 2. Seven-zone component view

```mermaid
flowchart LR
  Z1["1 Acquisition and intake"] --> Z2["2 Quarantine and inspection"]
  Z2 --> Z3["3 Adaptation and build"]
  Z2 --> Z4["4 Validation and release"]
  Z3 --> Z4
  Z4 --> Z5["5 Registry and artifact custody"]
  Z5 --> Z6["6 Deployment and serving"]
  Z7["7 Evidence and operations"] -. "observe, assure, contain" .-> Z1
  Z7 -.-> Z2
  Z7 -.-> Z3
  Z7 -.-> Z4
  Z7 -.-> Z5
  Z7 -.-> Z6
```

The zones are logical responsibility and authority boundaries, not proof supplied by subnets or physical co-location.

### Figure 3. Artifact-promotion view

```mermaid
flowchart LR
  A["Original artifact plus source record"] --> Q{"Hostile-format quarantine"}
  Q -- "reject" --> X["Isolate, investigate, dispose"]
  Q -- "sanitized immutable output" --> B["Authorized adaptation or release candidate"]
  B --> V{"Independent validation"}
  V -- "fail" --> X
  V -- "pass" --> S{"Separated release authority; threshold sign at higher tiers"}
  S --> G["Immutable registry identity and complete closure"]
```

Only sanitized outputs cross quarantine. A transformation creates a new identity and lineage edge; build workers cannot write the trusted registry.

### Figure 4. Deployment and admission view

```mermaid
sequenceDiagram
  participant C as Deployment controller
  participant G as Authoritative registry
  participant T as Trust and attestation verifier
  participant R as Serving runtime
  C->>G: Resolve immutable release identity and current state
  C->>T: Verify signature, purpose, time, trust and revocation
  C->>R: Challenge with nonce and requested tenant/isolation mode
  R-->>T: Fresh closure, runtime, hardware, firmware and driver evidence
  T-->>C: Non-replayed admission verdict
  C->>R: Load exact approved closure or fail closed
```

Registry, signature, deployment, load, and attestation use the same immutable release closure, preventing time-of-check/time-of-use substitution.

Attestation is renewed after every relevant release or configuration change, resume, migration, reconfiguration, or trust update. Until the new nonce-bound evidence passes freshness, replay, revocation, workload, tenant, hardware, firmware, driver, and closure checks, the controller does not load or resume the runtime.

### Figure 5. Serving view

```mermaid
flowchart LR
  I["Authenticated caller, tenant, purpose and capability"] --> P["Admission, policy, quota and extraction controls"]
  P --> S["Isolated queue, batch and scheduler"]
  S --> M["Attested model, adapter and safety closure"]
  M --> K["Tenant-scoped cache and protected response"]
  K --> O["Authorized consumer"]
  M -. "denied external egress" .-> N["External networks"]
  P -.-> E["Independent evidence"]
  S -.-> E
  M -.-> E
```

Tenant identity is authoritative at admission and preserved through batching, cache, inference, telemetry, backup, support, and response.

### Figure 6. Online and offline revocation view

```mermaid
flowchart TB
  A["Signed revocation and fleet-impact decision"] --> O["Online registries, trust stores, controllers, routes and replicas"]
  A --> B["Signed offline release, policy and revocation bundle"]
  B --> E["Edge node: monotonic time, anti-rollback, expiry"]
  E -- "fresh and authorized" --> L["Bounded local operation and evidence"]
  E -- "expired, rolled back or unknown" --> S["Safe stop"]
  L --> R["Reconnect reconciliation and re-enrollment"]
  O --> V["Acknowledgment, escalation and verified propagation"]
  R --> V
```

Revocation covers active sessions, adapters, caches, mirrors, credentials, backups and restore eligibility; a missed maximum propagation bound causes escalation or safe stop.

### Figure 7. Retirement and destruction view

```mermaid
flowchart LR
  D["Drain and remove serving authority"] --> R["Revoke releases, identities, keys and routes"]
  R --> I["Inventory originals, derivatives, memory, media, backups and provider copies"]
  I --> H{"Legal hold or retention duty?"}
  H -- "yes" --> P["Protected retained evidence and documented exception"]
  H -- "no" --> S["Media-specific sanitization or qualified cryptographic erasure"]
  P --> T["Signed tombstone and residual-risk disposition"]
  S --> T
  T --> A["Independent residual-artifact search and assurance"]
```

Destruction is verifiable only when replica coverage, key-destruction prerequisites, provider copies, device memory, and residual searches are evidenced.

## Actors and identities

Model Owner, Data Owner, AI Capability Business Owner, AI Capability Technical Owner, AI Platform Owner, Application Owner, supplier, Procurement, Legal, Privacy, Model Validation Lead, build and ML operations, Release Authority, registry and artifact custodians, trust-anchor and cryptographic services, deployment controller, runtime operations, backup and records custodians, support personnel, Incident Response, Security Operations, Assurance, and Internal Audit use distinct named identities. Workload identities are short-lived and bound to purpose, tier, tenant, environment, and release.

Build, validation, signing, registry administration, trust-anchor administration, deployment, runtime, KMS, backup, support, destruction, and assurance are separated privileged functions. Builders cannot validate or promote their candidate; validators cannot sign it; signers cannot change registry approval; registry administrators cannot alter trust roots; deployment or runtime administrators cannot promote artifacts, weaken egress, change trust stores, or suppress evidence. Just-in-time and break-glass access is purpose- and time-bounded, independently approved for high-impact work, recorded, automatically expired, and reviewed for conflicts and orphaned credentials.

## Data and instruction flows

Intake records original hashes, signatures, supplier, copyright and source, license text and version, commercial use and hosting rights, redistribution and modification rights, derivative-work and output terms, use restrictions, attribution and disclosure duties, patent terms, acceptable-use limits, export-control and sanctions obligations, permitted geography, expiration, and change and revocation triggers, together with bills of materials, notices, classification, and custody. Quarantine treats model formats, pickle and serialized objects, archives, tokenizers, templates, loaders, plugins, native extensions, kernels, scripts, and dependencies as hostile; it tests parser and decompression attacks, remote-code behavior, path traversal, symlinks, oversized shards, and resource bombs in disposable workers without enterprise credentials, writable registry access, or unrestricted egress.

Adaptation binds approved base identity; versioned training, validation, and holdout datasets; dataset authority, classification, minimization, consent or legal basis, licensing, quality, lineage and representativeness; code and dependency versions; parameters; randomness and determinism controls; operator and workload identities; timestamps; hardware and environment class; resource use; intermediate inventory; and output identities. Separated training, validation, and holdout sets are checked for duplication, poisoning, backdoors, triggers, contamination, leakage, secrets, regulated data, and memorization. Checkpoints, gradients, optimizer state, adapters, caches, logs, metrics, reports, samples, and failures receive the highest applicable data, privacy, intellectual-property, secondary-use, retention, residency, legal-hold, and deletion obligations inherited from their inputs. Correction and deletion propagate to dataset versions and derived artifacts where required; retraining, adapter replacement, restriction, or other remediation is evaluated, and unlearning is never claimed beyond demonstrated limits. Reproducibility evidence must repeat material transformations using the recorded manifest without requiring unrestricted retention of sensitive inputs.

License and acceptable-use compatibility is evaluated transitively across base model, code, data, adapters, dependencies, output use, deployment, distribution, and derivatives. Changed or revoked terms trigger lineage-based fleet impact and may prohibit adaptation, release, use, or distribution. Artifact access never implies permission to copy, export, adapt, merge, redistribute, or repurpose.

Model artifacts, prompts, outputs, evaluation data, and adaptation results receive intellectual-property classification and protection consistent with ownership, confidentiality, use, disclosure, retention, residency, legal-hold, and deletion obligations.

A release manifest binds every weight shard, tokenizer, vocabulary, prompt and chat template, adapter, speculative model, loader, kernel, dependency, runtime image, safety configuration, precision, and approved hardware, firmware, and driver class. Import, dependency resolution, activation, support, telemetry export, and artifact export use authenticated, authorized, inspected, logged channels with destination, license, classification, encryption, residency, DLP, bounded queues, and reconciliation.

Independent release validation tests the immutable candidate for intended purpose and populations; security; privacy; quality; safety; harmful bias; robustness; memorization and extraction; prompt abuse; performance and capacity; compatibility; hardware and runtime behavior; observability; rollback; and known limitations. Results, populations, configurations, thresholds, failures, limitations, and reviewer independence are bound to the release decision.

Inference protection assesses model extraction, membership inference, memorization, inversion, evasion, and probing. Detection correlates bulk, high-entropy, near-boundary, multi-identity, and cross-tenant campaigns, including distributed and low-and-slow behavior. Purpose- and risk-based controls limit rate, query pattern, response detail, confidence, logit, embedding, adapter, error, debug, and diagnostic exposure. Alerts preserve attributable evidence and invoke incident response. These controls reduce but do not eliminate extraction risk where an interface necessarily exposes model behavior; the accepted residual risk, monitoring limits, and response thresholds are documented.

Registry artifacts and metadata are encrypted in transit and at rest. Access is scoped by named role, purpose, environment, tenant, and lifecycle state. Encryption roots and release-signing trust roots are separated where appropriate; key issuance, custodianship, recovery, rotation, destruction, and emergency access are documented and independently evidenced. The immutable registry history records download, upload, inspection, transformation, validation, approval, signing, promotion, replication, deployment, rollback, revocation, export, backup, restore, legal hold, retirement, and destruction events. Ordinary build, platform, and serving administrators cannot rewrite that history, replace artifacts, or erase custody and revocation state.

## Trust boundaries

| Named lifecycle zone | ESAF logical mapping | Material crossings and custody requirements |
|---|---|---|
| Acquisition and intake | Z0 External and untrusted; Z7 Security, operations, and assurance | Controlled transfer authenticates source, preserves original identity, classification, license, custody, direction, evidence, and failure state. |
| Quarantine and inspection | Z7 Security, operations, and assurance | Disposable hostile-workload isolation accepts only bounded input and emits sanitized, integrity-bound output; no production identity, lateral path, or registry write exists. |
| Adaptation and build | Z4 Model and inference; Z5 Enterprise data and knowledge; Z7 Security, operations, and assurance | Data and artifact authority, read-only inputs, short-lived identity, default-deny egress, bounded resources, controlled output staging, and evidence are enforced. |
| Validation and release | Z4 Model and inference; Z7 Security, operations, and assurance | Independent evaluators receive an immutable candidate; release authority signs the same closure only after current purpose, tier, license, evidence, and conflict checks. |
| Registry and artifact custody | Z7 Security, operations, and assurance | Immutable identity, encrypted artifacts, approval state, trust history, revocation, backup, legal hold, and ordinary-admin immutability are authoritative. |
| Deployment and serving | Z1 User and channel; Z2 Enterprise policy and integration; Z3 AI application and orchestration; Z4 Model and inference | Admission binds caller, tenant, purpose, release, runtime, hardware, policy, isolation, and evidence; response and diagnostic exposure is bounded. |
| Evidence and operations | Z7 Security, operations, and assurance | Separately administered evidence receives attributable events from every zone and returns containment or assurance decisions without becoming an unmonitored admin path. |

Every crossing records direction, identity, authorization, information and classification, validation, protection, evidence, reliability, and provider-consumer responsibility. A hosted service remains outside enterprise control where applicable even when contractually dedicated.

The following records apply crossing by crossing. For each row, the architecture record names the concrete human and workload identities, authentication method, any delegation or impersonation, requested operation and least-privilege scope, and the policy decision point (PDP). It also instantiates the listed payload with provenance, classification and residency; input, output, schema, content, instruction and integrity validation; encryption, secret, session, tenant and state protection; event source, correlation, decision, outcome, retention and evidence access; timeout, retry, idempotency, rate, capacity and failure behavior; and provider, consumer, subprocessor and inherited-control allocation.

| Material interface and purpose | Initiator and receiver | Authorization and PDP | Information, classification, provenance, residency | Validation and protection | Evidence and reliability | Responsibility boundary |
|---|---|---|---|---|---|---|
| Approved source to acquisition intake: acquire an original artifact | Approved supplier or enterprise source to intake custodian | Approved supplier, artifact, transfer and purpose; acquisition PDP | Artifact, license, notices and source identity; source provenance; assigned classification and permitted region | Signature, hash, schema, archive and transfer validation; encrypted authenticated channel and bounded staging | Transfer/custody decision and outcome; timeout, no blind retry, idempotent source identity, intake rate/capacity, quarantine on failure | Source provides authentic material; enterprise intake verifies; subprocessors and inherited transfer controls are recorded |
| Authorized data owner to adaptation input: stage governed datasets | Data Owner and data service to adaptation staging identity | Approved dataset version, purpose and job; data-policy PDP | Versioned data, labels and lineage; highest applicable classification, rights and residency | Schema, quality, duplication, trigger, DLP and integrity checks; encrypted read-only mounts and tenant/job isolation | Dataset decision, version and outcome; bounded transfer, idempotent version, capacity limit, fail closed | Data Owner authorizes; build consumes; storage/provider duties and inherited data controls remain explicit |
| Intake to quarantine: submit untrusted package | Intake workload to disposable quarantine worker | One artifact identity and inspection profile; quarantine admission PDP | Original artifact and intake manifest; untrusted classification and source provenance | Size, archive, path, format and integrity checks; no production secrets, default-deny egress and bounded resources | Submission, scan and disposition; timeout, no unsafe retry, idempotent hash, resource ceiling, isolate on failure | Intake preserves custody; quarantine contains; execution provider cannot promote output |
| Quarantine to adaptation staging: promote sanitized build input | Sanitization service to build staging custodian | Approved sanitized identity and build purpose; promotion PDP | Sanitized artifact and inspection evidence; classified derivative and retained lineage | Complete-closure hash, malware/DLP and policy checks; signed transfer and write-only staging | Promotion decision and receipt; bounded queue, idempotent identity, reject incomplete output | Quarantine produces; build verifies and consumes; neither can write the registry |
| Quarantine to validation staging: promote sanitized inference-only candidate | Sanitization service to validation custodian | Approved sanitized identity, purpose and test plan; validation-admission PDP | Sanitized candidate and evidence; classified artifact, source lineage and region | Closure, signature, malware, license and integrity checks; encrypted immutable staging | Admission and rejection evidence; bounded queue, idempotent identity, fail closed | Quarantine produces; independent validation consumes; inference-only CP6/CP7 status is recorded |
| Adaptation to validation: submit derived immutable candidate | Ephemeral build workload to validation custodian | Approved job output and test purpose; candidate-admission PDP | Candidate closure, manifest, datasets and transformation lineage; derived classification/residency | Output staging, malware, DLP, reproducibility and closure-integrity checks; build cannot modify after receipt | Build/candidate correlation and decision; timeout, no self-approval, idempotent candidate ID, quarantine failure | Build produces evidence; independent validation owns verdict; provider compute has no promotion authority |
| Validation to release authority: request release decision and signing | Independent validator to separated release signer | Passed candidate, purpose, tier, environment, expiry and signer quorum; release PDP | Immutable closure, findings, limitations and approval evidence; controlled classification and residency | Evidence completeness, conflict, trusted time, scope and closure verification; protected signer session and keys | Validator/signature correlation and outcome; signature timeout, no automatic approval retry, fail closed | Validator supplies verdict; Release Authority decides/signs; higher tiers require dual or threshold approval |
| Release authority to registry: register signed release | Release service to registry custodian | Exact signed closure and approved metadata; registry-promotion PDP | Signed release, lineage, scope, tier, expiry and rollback; protected artifact classification/residency | Signature, trust, purpose, metadata schema and immutable-identity checks; encrypted custody | Append-only promotion and receipt; idempotent release ID, bounded replication, reject conflicts | Release produces; registry verifies/custodies; registry admin cannot alter trust or approval |
| Deployment controller to registry: resolve current release state | Deployment identity to authoritative registry | Immutable ID, target environment, tier and purpose; deployment PDP | Release state, closure, revocation, expiry and compatibility; authoritative provenance and residency | Authenticated query, current-state and response-integrity checks; protected session and scoped metadata | Query, decision and version; timeout, bounded retry, no mutable-tag fallback, block load | Registry is authoritative provider; controller consumes; replicas preserve state and responsibility |
| Deployment controller to trust verifier: verify signature and attestation | Controller workload to independent verifier | Release, runtime, tenant and isolation request; trust/admission PDP | Closure, signature, nonce, boot epoch, runtime/hardware evidence; sensitive integrity classification | Trust, time, purpose, revocation, freshness, replay and cross-tenant checks; encrypted nonce-bound session | Challenge, verdict and correlation; expiry, bounded retry, anti-replay, fail closed | Controller requests; verifier decides independently; attestation providers remain identified external assertions where applicable |
| Deployment controller to serving runtime: load or re-attest exact closure | Controller to workload identity | Approved release, tenant, environment and isolation mode; runtime-admission PDP | Complete closure and measured configuration; restricted artifact and regional placement | Signature/hash, image, driver, firmware, policy and configuration checks; encrypted artifact transfer and sealed secrets | Load/re-attestation outcome; timeout, idempotent release ID, capacity gate, drain or stop on failure | Controller authorizes; runtime loads but cannot promote; infrastructure/provider controls remain field-assigned |
| Capability caller to serving admission: request inference | Human or workload caller through enterprise policy boundary to serving identity | Principal, capability, tenant, purpose, model, adapter, tier and budgets; inference PDP | Prompt/context and request metadata; classified, provenance-bound and region-checked | Authentication, schema/content/instruction, size and policy validation; encryption, session and tenant isolation | Admission, denial, quota and correlation; timeout, bounded retry/idempotency where applicable, fair capacity | Caller supplies authorized input; application and platform enforce; consuming pattern owns business use |
| Serving admission to queue, batch and scheduler: dispatch authorized work | Admission workload to isolated scheduler identity | Immutable decision, tenant, model/adapter, tier, deadline and resource budget; scheduling PDP | Validated request plus authoritative tenant/capability identity; request classification and regional placement | Decision integrity, expiry and tenant checks; encrypted internal channel, queue and batch isolation | Dispatch and scheduling outcome; timeout, cancellation, fair rate/capacity and no cross-tenant retry | Admission authorizes; scheduler allocates but cannot broaden purpose, authority or placement |
| Scheduler to attested model runtime: execute bounded inference | Isolated scheduler to admitted runtime identity | Exact release, adapter, tenant, batch and resource scope; runtime PDP | Bounded tokenized input and execution metadata; classified tenant state and region | Closure/attestation freshness, batch, adapter and tenant validation; HBM, DMA, cache and state isolation | Start, cancellation, completion and resource evidence; timeout, idempotent request ID where safe, bounded capacity/failure | Scheduler dispatches; runtime executes; accelerator/provider responsibilities remain explicit |
| Model runtime to tenant-scoped cache and response protection: stage output | Attested runtime to cache/response service identity | Original request, tenant, purpose, retention and diagnostic policy; output PDP | Output, cache key/state and limitations; classified provenance-bound result | Tenant, adapter, schema/content, DLP, retention and integrity checks; encrypted cache and response state | Cache/write decision, response and eviction; bounded retry, expiry, quota, purge on failure | Runtime produces; cache/response service isolates and releases only to the authorized consumer |
| Serving runtime to authorized consumer: return protected output | Attested runtime to initiating application or user channel | Original request, tenant, purpose and response scope; output-policy PDP | Output, citations/limitations and correlation; classified for approved recipient/residency | Output schema/content, DLP, safety, tenant binding and integrity checks; encrypted response and cache isolation | Response/denial and outcome; timeout, no cross-tenant retry, bounded detail and capacity | Runtime produces; application consumes and governs use; downstream provider boundaries persist |
| Every lifecycle zone to ARC-P160: emit authoritative evidence | Named zone workload or administrator to independent evidence collector | Registered source, event type, tenant and purpose; telemetry/evidence PDP | Identity, decision, artifact, operation, cost, outcome and integrity events; minimized classification/residency | Source authentication, schema, sequence, trusted-time, gap and integrity checks; encrypted append-only or WORM custody | Correlation, receipt and gap alert; bounded buffer, backpressure, loss behavior and safe-stop matrix | Source emits but cannot select/delete; ARC-P160 custodies; assurance independently assesses |
| ARC-P160 operations to lifecycle enforcement: assure, alert or contain | Independent assurance, Security Operations or Incident Response identity to the named zone enforcement owner | Signed finding, incident, revocation or resumption scope; assurance/containment PDP | Verdict, evidence reference, affected identity, deadline and action; protected incident classification/residency | Authority, signature, scope, freshness, conflict and acknowledgment checks; separate administrative channel | Decision, delivery, acknowledgment and outcome; timed retry, idempotent action ID, escalation and safe stop | Independent function directs; zone owner enforces and cannot rewrite the source evidence or verdict |
| Revocation authority to online and offline enforcement: withdraw authority | Authorized incident/release authority to registries, trust stores, controllers, routes, runtimes and edge bundle custodians | Signed release/credential/policy scope and deadline; revocation PDP | Revocation identity, reason, effective time and fleet lineage; protected classification and region | Signature, purpose, trusted/monotonic time, anti-rollback, freshness and completeness checks | Acknowledgment and timed propagation; idempotent revocation, retry until deadline, safe stop/escalate missed nodes | Authority decides; each enforcement owner acknowledges; disconnected/provider obligations and unreachable targets stay visible |
| Retirement authority to custodians and destruction services: remove or retain artifacts | Model Owner and business owner to registry, platform, backup, edge and provider custodians | Approved retirement, legal hold, media and destruction plan; retirement PDP | Full replica inventory, keys, holds, tombstones and residual risk; classification/residency retained | Inventory completeness, media method, key/replica coverage and residual search; protected evidence | Per-copy outcome and signed tombstone; bounded retry, exception tracking, escalation until reconciled | Enterprise retains accountability; each custodian/provider proves action; assessor verifies independently |

## Components and responsibilities

| Component | Required responsibility |
|---|---|
| Intake and transfer service | Approve source and transfer; preserve original identity, custody, classification, supplier, license, and notices. |
| Quarantine and sanitization service | Execute hostile parsing and inspection in disposable bounded workers; reject or emit sanitized immutable artifacts. |
| Adaptation and build service | Use authorized data and inputs in ephemeral isolation; create reproducible manifests and staged derivatives without registry write. |
| Independent validation service | Test immutable candidates for intended purpose and populations, security, privacy, quality, safety, harmful bias, robustness, memorization and extraction, prompt abuse, performance, capacity, compatibility, hardware and runtime behavior, observability, rollback, and known limitations. |
| Release and signing authority | Bind scope, tier, environment, expiry and evidence; enforce separation and dual or threshold signing for higher tiers. |
| Trust-anchor service | Govern issuance, non-exportability, identity and purpose binding, rotation, revocation, compromise, algorithm agility, trusted time, recovery, and verifier freshness. |
| Registry and artifact custodian | Maintain immutable identity, lineage, state and history; encrypt and authorize custody; prevent ordinary-admin rewrite or substitution. |
| Deployment controller and verifier | Resolve current immutable state, verify closure and trust, demand fresh nonce-bound attestation at initial admission and after change, resume, migration, reconfiguration, or trust update, and admit only an exact authorized deployment. |
| Serving fabric | Preserve tenant and capability identity; isolate queues, adapters, scheduler, accelerator, cache, telemetry, backups and support; deny egress. |
| Import/export custodian | Operate separately governed inspection, authorization, signing, DLP, destination, and reconciliation channels. |
| Continuity and revocation service | Maintain safe-failure matrices, atomic backup, isolated restore, online and offline revocation, reconciliation, and authorized resumption. |
| ARC-P160 evidence and assurance | Independently preserve source evidence, correlate fleet identity, incidents, capacity and cost, detect gaps, and support assessment and management review. Dashboards and aggregate metrics are operational aids, not authoritative release, custody, incident, or assurance evidence. |

Dedicated hosted infrastructure requires a field-level shared-responsibility matrix for hardware, hypervisor, firmware, drivers, artifact and key custody, privileged personnel and subprocessors, support, telemetry, incident timing, substitution notice, isolation, backups, destruction, portability, and exit. Qualification evidence for immutable identity, runtime integrity, tenant isolation, privileged access, incident notification, custody, backup and deletion, portability, and exit has a cadence and expiry. Provider claims remain externally asserted unless corroborated. Material change, missing or expired evidence, provider-admin access, or silent model, adapter, precision, runtime, region, safety, or subprocessor substitution triggers restriction, reclassification under API-140, or exit.

## Required controls

Required allocation:

- Governance and risk: `GOV-130`, `GOV-140`, `RSK-110`, `RSK-120`, `RSK-140`.
- Identity and access: `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-140`, `IAM-150`.
- Data: `DAT-100`, `DAT-110`, `DAT-120`, `DAT-130`.
- Model: `MOD-100`, `MOD-110`, `MOD-120`, `MOD-130`, `MOD-140`, `MOD-150`.
- Application: `APP-100`, `APP-110`, `APP-120`, `APP-130`, `APP-140`, `APP-150`.
- Infrastructure: `INF-100`, `INF-110`, `INF-120`, `INF-130`, `INF-140`, `INF-150`.
- Platform and API: `API-110`, `API-150`.
- Architecture: `ARC-100`, `ARC-110`, `ARC-130`, `ARC-140`.
- Operations: `OPS-100`, `OPS-110`, `OPS-120`, `OPS-130`, `OPS-140`, `OPS-150`.
- Monitoring: `MON-100`, `MON-110`, `MON-120`, `MON-140`, `MON-150`.
- Compliance and assurance: `CMP-100`, `CMP-110`, `CMP-140`, `AUD-100`, `AUD-110`, `AUD-120`, `AUD-130`, `AUD-140`.
- Workforce: `EDU-110`, `EDU-130`.

Inherited-and-verified allocation: `GOV-100`, `GOV-110`, `GOV-120`, `RSK-100`, `STR-100`, `STR-130`, `API-100`, `ARC-120`, `ARC-150`, `EDU-100`, `EDU-120`. Each is verified at hosted, regional, and edge boundaries with configuration, responsibility, limitation, evidence, and failure tests.

Conditional allocation: `RSK-130` for individual, group, safety, environmental, or societal impact; `DAT-140` for personal data and rights; `DAT-150` for retrieval or embedding; `DAT-160` when outputs or feedback are retained, evaluated, shared, or reused; `CMP-120` for an external model, host, or supplier; `CMP-130` for jurisdiction, residency, or transfer; `API-120` and `API-130` for plugins, tools, MCP, or orchestration; `API-140` for dedicated hosted or external services; `AGT-100`, `AGT-110`, `AGT-120`, `AGT-130`, `AGT-140`, `AGT-150`, and `AGT-160`, plus `MON-130`, for agentic operation; `STR-110` for value claims; `STR-120` for experimentation; and `EDU-140` for governance personnel.

Catalog owner roles remain accountable. Pattern roles identify primary implementation and evidence production without transferring accountability.

## Control points and overlays

| CP | Control point | Required outcome | Primary implementation and evidence roles |
|---|---|---|---|
| CP1 | Model-source and supplier approval | Sources, suppliers, ownership, assurance, and permitted acquisition are approved | Model Owner; Procurement, Third-Party Risk, Legal |
| CP2 | License and permitted-use validation | License, IP, use, modification, distribution, and downstream obligations are resolved | Legal; Model Owner, Procurement |
| CP3 | Secure artifact intake and transfer | Original identity, integrity, custody, classification, and transfer are preserved | Model Owner; Transfer Custodian, Security Engineering |
| CP4 | Quarantine and hostile-format inspection | Executable, malicious, malformed, unsafe, and resource-abusive artifacts are contained or rejected | Model Owner; Application Security, Vulnerability Management |
| CP5 | Provenance and lineage verification | Source, training, adaptation, transformation, dependency, and limitation lineage is attributable | Model Owner, Data Governance; Supplier, Build Engineering |
| CP6 | Training and adaptation data authorization | Data authority, purpose, quality, privacy, license, and retention are established when adaptation occurs; otherwise documented not applicable | Data Owner; Privacy, Data Governance, ML Operations |
| CP7 | Reproducible adaptation and build | Material transformations bind approved inputs, code, parameters, identities, compute, intermediate state, outputs, and evidence; inference-only use records not applicable | Model Owner; ML Operations, Build Engineering |
| CP8 | Release-candidate security and quality validation | Immutable candidates meet approved intended-purpose and population, security, privacy, safety, quality, harmful-bias, robustness, memorization, extraction, prompt-abuse, compatibility, hardware/runtime, observability, performance, capacity, rollback, and limitation criteria | Model Validation Lead; Security, Privacy, Safety, Performance testers |
| CP9 | Artifact signing and trust-anchor governance | Only authorized releases are signed and verifiable through governed key and trust-anchor lifecycle | Cryptographic Services, Model Owner; Release Authority, PKI/HSM, Assurance |
| CP10 | Registry identity, metadata, and approval state | Immutable identity, lineage, scope, status, expiry, revocation, and history are authoritative | Model Owner; Registry Custodian, Release Management |
| CP11 | Encrypted artifact custody and access | Artifacts and keys resist unauthorized access, extraction, replacement, deletion, and duplication | Model Owner; Cryptographic Services, Artifact Custodian, Storage Operations |
| CP12 | Deployment authorization and admission | Only approved releases, configurations, environments, runtimes, and hardware classes are admitted | AI Capability Technical Owner; Change Management, Platform Engineering |
| CP13 | Runtime identity and configuration integrity | Workload, runtime, image, driver, firmware, configuration, model, and adapter identity are freshly verified | Platform Engineering; IAM, Cryptographic Services, Runtime Operations |
| CP14 | Tenant, adapter, cache, scheduler, and accelerator isolation | Shared serving prevents cross-tenant state, authority, resource, telemetry, and side-channel compromise | AI Platform Owner, Application Owner; Platform, Accelerator, Scheduler, Security Engineering |
| CP15 | Inference input, output, and resource protection | Callers, data, behavior, diagnostics, resources, and extraction exposure are bounded | Application Owner; Application Security, Model Validation, SRE |
| CP16 | Deny-by-default egress and governed import/export | Runtime egress is denied and external movement uses approved inspected channels | Platform Engineering, API Owner; Network Security, Import/Export Custodian |
| CP17 | Model integrity, drift, and behavioral monitoring | Change, drift, abuse, extraction, isolation failure, advisory impact, and evidence gaps are detected | Model Owner, Security Operations; ML Operations, ARC-P160 Platform |
| CP18 | Capacity, continuity, rollback, and recovery | Capacity is governed; only eligible known states support fallback and isolated recovery | Business Continuity, AI Service Owner; SRE, Model Owner, Assurance |
| CP19 | Backup, retention, legal hold, and destruction | Atomic copies and isolated restoration or destruction preserve identity, obligations, and evidence | Data Owner, Compliance; Records, Privacy, Backup Custodians |
| CP20 | Retirement, revocation, and residual-artifact removal | Authorization and material residue are removed or preserved only as required | Model Owner, AI Capability Business Owner; Registry, Platform, Data Custodians |
| CP21 | Evidence, incident response, and independent assurance | Protected evidence supports response, investigation, assessment, accountability, and review | Incident Response, Assurance; Security Operations, Internal Audit, Evidence Custodian |

Apply overlays for Tier 3 and Tier 4, personal or regulated data, external suppliers, dedicated hosting, regional or transfer restrictions, shared serving, untrusted adapters, confidential computing, agentic operation, offline or edge use, legal hold, and high-impact recovery or destruction.

## Architecture decisions and parameters

Record the selected tier and variant; custody and shared-responsibility fields; artifact formats; release-closure schema; immutable identity and equivalence rules; validation thresholds and populations; signer quorum; trust-anchor algorithms, time, rotation and recovery; registry retention and replication; attestation nonce, maximum age, boot epoch and replay policy; role-conflict and emergency-access rules; isolation test configuration and leakage thresholds; tenant placement; extraction budgets and correlation; complete IPv4, IPv6, DNS, metadata, mesh, registry, telemetry, crash, support and approved-sink egress policy; advisory severity and fleet deadlines; capacity and safe-failure matrix; backup atomicity and restore eligibility; maximum revocation latency; maximum offline operation; capture response; destruction technique; evidence retention; recovery objectives; and resumption authority.

## Failure modes and abuse cases

| Failure or abuse | Required detection and safe treatment |
|---|---|
| Hostile, malformed, or resource-abusive input | Quarantine in ephemeral bounded workers; reject or promote only sanitized immutable output. |
| Candidate or closure substitution | Compare the complete immutable identity at inspection, validation, signing, registry, admission, load, and attestation; fail promotion or load. |
| License, acceptable-use, advisory, supplier, driver, firmware, code, or model change | Traverse lineage, identify fleet and derivatives, suspend or route-block affected releases, set remediation deadlines, rebuild and revalidate. |
| Signature, key, time, purpose, tenant, trust, algorithm, or attestation failure | Treat cryptographic validity alone as insufficient; block load or inference, revoke affected trust, and investigate replay or compromise. |
| Shared-serving or accelerator leakage | Compare repeated adversarial tests against approved empirical content, timing, occupancy, cardinality, utilization, power and thermal thresholds; dedicate or stop. |
| Extraction, membership inference, memorization, inversion, evasion, probing, or distributed abuse | Correlate bulk, high-entropy, near-boundary, multi-identity, cross-tenant and low-and-slow campaigns; limit confidence, logit, embedding, adapter, error, debug, diagnostic and response detail; throttle or deny, preserve evidence, and invoke incident response while recognizing that controls reduce but cannot eliminate extraction risk. |
| Egress or support bypass | Deny every network plane by default, terminate exceptions and emergency credentials automatically, contain and investigate any attempted path. |
| Capacity exhaustion or starvation | Apply tenant quotas and fair scheduling; shed or queue bounded work without exposing state or silently broadening model, authority, provider, or data use. |
| Evidence unavailable or suppressible | Higher tiers stop affected inference; lower tiers use only an approved bounded buffer or grace rule, never runtime-selected evidence. |
| Rollback or restore is revoked, expired, vulnerable, license-invalid, wrong-region, partial, compromised, or keyless | Keep it isolated and ineligible; use authorized forward recovery or safe stop. |
| Online revocation misses its bound | Block new loads and inference as defined, escalate failed acknowledgments, contain reachable enforcement points, and track unreconciled targets. |
| Offline bundle stale, replayed, clock-rolled-back, or expired | Use monotonic time and anti-rollback; safe stop and require reconciled re-enrollment. |
| Edge capture, loss, repair, or custody change | Assume remote wipe can fail; revoke credentials, artifacts and trust, preserve evidence, and require governed re-enrollment. |

The safe-failure matrix distinguishes promotion, new model load, new inference, continued inference, and resumption. It records permitted grace, evidence and policy freshness, capacity behavior, approved degraded substitutes, and authority. Tier 3 and Tier 4 stop when identity, integrity, isolation, required validation, authorization, revocation, policy, or assurance is unknown. Lower tiers may use a visible, time-bounded degraded configuration only when it increases neither data use, authority, tenancy, connectivity, provider scope, nor action scope.

## Fallback recovery and retirement

Rollback is a new deployment decision. The target must remain authorized, unexpired, license- and policy-compatible, data-compatible, free of disqualifying vulnerabilities, stale keys, revoked material, weaker safety, and incompatible runtime or precision. No model, adapter, precision, provider, region, safety, retention, or connectivity substitution is silent.

Backups atomically preserve the complete closure, registry identity and state, approvals, lineage, signatures and trust, policies, adapters, evidence, encryption, access, residency, retention, legal hold, and revocation. Keys are separately protected. Restore occurs in an isolated verification path and tests partial restore, ransomware, compromised administrators, stale trust, wrong region, KMS failure, and revoked or license-invalid contents before new authorization.

Revocation reaches registries, trust stores, credentials, caches, mirrors, controllers, routing, active replicas and sessions, adapters, edge nodes, backup restore eligibility, controlled export destinations, and consuming records within a declared maximum. Offline nodes use signed bundles, trusted or monotonic time, anti-rollback, expiry, bounded evidence, maximum offline duration, safe stop, and reconnect reconciliation.

Retirement drains traffic, removes authorization, revokes identities, releases and keys, updates consumers, preserves required evidence, and inventories weights, adapters, tokenizers, checkpoints, optimizer state, derivatives, caches, staging, snapshots, backups, temporary disks, crash dumps, RAM, shared memory, accelerator HBM, removable media, support, supplier and subprocessor copies. Media-specific sanitization or cryptographic erasure is accepted only with demonstrated key and replica coverage. Signed tombstones, legal-hold exceptions, provider attestations, residual-risk disposition, and independent post-retirement searches verify destruction.

## Evidence and assessment

Required evidence includes source and supplier approval; the complete license, intellectual-property and acceptable-use record and changes; original and derived hashes and lineage; dependency and model bills of materials; quarantine topology, hostile-format, escape, malware, dependency, DLP, sanitization and resource tests; data authority, versioning, privacy, quality, duplication, triggers, deletion and representativeness; build manifests with dependency versions, determinism, timestamps, resource use and intermediate inventory; independent validation of intended purpose and populations, security, privacy, quality, safety, harmful bias, robustness, memorization, extraction, prompt abuse, performance, capacity, compatibility, hardware/runtime behavior, observability, rollback and known limitations; release scope, equivalence, signature, expiry and role conflicts; trust-anchor history; immutable registry event history; access, in-transit and at-rest encryption, separate roots, key lifecycle, export, backup and legal hold; fresh attestation and replay tests for admission, change, resume, migration, reconfiguration and trust update; empirical tenant and accelerator isolation thresholds; model-extraction, membership-inference, memorization, inversion, evasion, probing, campaign-correlation, exposure-control, capacity and cost evidence; deny-by-default egress; ARC-P160 identity, drift, incident, fleet, cost and assurance records; provider qualification; safe-failure matrices; atomic backup and isolated restore; online and offline revocation; edge capture; retirement and destruction. Dashboards, provider consoles and aggregate operational metrics are not authoritative release, custody, incident, cost-allocation, or assurance evidence; authoritative conclusions trace to protected source records.

Each assessment exercise below has a control objective, evidence source, pass/fail basis, and safe-stop or escalation behavior.

| Exercise | Control objective | Evidence source | Pass/fail basis | Safe stop or escalation |
|---|---|---|---|---|
| Hostile artifact and quarantine escape | Contain executable formats and promote only sanitized output | Sandbox, scan, escape, resource and transfer records | Pass only when no trusted credential, registry write, lateral path, or unsanitized output is reachable | Reject, isolate, investigate |
| Adaptation or validation exfiltration | Prevent data and artifact escape from ephemeral hostile workloads | Network, metadata, log, metric, checkpoint, adapter, storage and lateral-movement tests | Pass when every unapproved path is denied and recorded | Terminate job, quarantine outputs, incident escalation |
| Artifact substitution between inspection and load | Preserve one release-closure identity across every gate | Manifest, signature, registry, admission, load and attestation comparisons | Any shard, adapter, draft model, safety, precision, runtime, driver or firmware mismatch fails | Block promotion or load and investigate |
| Incomplete release validation | Test every approved release dimension on the immutable candidate | Intended-purpose and population, security, privacy, quality, safety, harmful-bias, robustness, memorization, extraction, prompt-abuse, performance, capacity, compatibility, hardware/runtime, observability, rollback and limitation evidence | Every applicable dimension meets its approved threshold and limitations are accepted by an independent reviewer; omitted, stale or mismatched evidence fails | Block signing and promotion; remediate and repeat validation |
| Stale or replayed attestation | Require fresh tenant- and workload-bound integrity | Nonce, boot epoch, age, migration and replay evidence | Stale, replayed, cross-host or cross-tenant evidence is rejected | Block load or inference; re-attest |
| Signature, trust, time, and purpose failure | Accept only current, correctly scoped trust | Signature, key, purpose, tenant, trusted-time, algorithm and revocation records | Expired, revoked, compromised, wrong-purpose, stale-trust, bad-time or downgraded signatures fail | Revoke, block, invoke compromise response |
| Poisoned or contaminated adaptation | Prevent poisoned, backdoored, leaking or invalid derived artifacts | Dataset lineage, contamination, trigger, memorization and holdout tests | Candidate meets approved contamination, privacy and quality thresholds with independent data separation | Quarantine candidate and data; remediate or abandon |
| Unreproducible build or equivalence-rule abuse | Require repeatable material transformation and preapproved bounded equivalence | Versioned dataset, code/dependency, parameter, randomness/determinism, timestamp, environment, resource, output and equivalence records | Material output is reproduced within approved bounds; no post-validation change is waived by an untested or retrospective rule | Block candidate and require corrected build or full revalidation |
| Direct intermediate-artifact promotion | Keep checkpoints, adapters and other intermediate state behind every quarantine, validation, signing and registry gate | Intermediate inventory, staging ACL, promotion decision and negative authorization tests | No intermediate identity can write the registry or reach deployment without the complete approved gate chain | Block and quarantine artifact; revoke path and investigate |
| License or acceptable-use change | Enforce transitive rights continuously | License versions, lineage graph, supplier notice and fleet-impact record | All affected bases, data, adapters, derivatives, uses and deployments are resolved before deadline | Suspend promotion/use/export; legal escalation |
| Separation-of-duties violation | Prevent self-approval and privileged collusion | Identity, conflict, approval, session and break-glass records | Builder, validator, signer, registry, trust, deployment and assurance conflicts are denied | Freeze release, revoke access, independent review |
| Shared-serving and accelerator side-channel leakage, including P2P, DMA, RDMA and profiler paths | Demonstrate tenant and hardware isolation empirically | Repeated adversarial content, HBM, residual page, P2P, DMA, RDMA, profiler, timing, cache, occupancy, utilization, power and thermal tests | Exact hardware, firmware, driver, scheduler, device plugin, profiler and partition stay within approved thresholds | Dedicate affected tiers or stop shared serving |
| Model extraction, membership inference, memorization, inversion, evasion, probing, and distributed campaigns | Reduce inference privacy and model-disclosure risk without claiming elimination | Bulk, high-entropy, near-boundary, multi-identity, cross-tenant and low-and-slow correlation; rate, query-pattern, confidence, logit, embedding, adapter, error, debug, diagnostic and response-detail evidence | Each campaign and exposure channel is detected or bounded within approved thresholds, residual risk is recorded, and no control is represented as eliminating unavoidable behavioral exposure | Throttle, reduce detail, deny, revoke and escalate to incident response |
| Resource starvation | Preserve fair service and tenant isolation | Queue, quota, batch, memory, compute, thermal and power load tests | Resource exhaustion remains bounded to authorized budgets and does not expose prior state | Shed or queue load; safe degraded mode or stop |
| IPv4, IPv6, DNS, metadata, mesh, registry, telemetry, crash, support, and approved-sink egress bypass | Enforce comprehensive default deny | Network-plane tests, policy decisions, flow and exception records | Every unapproved route and covert credential or data path is denied and detected | Terminate path and credentials; contain and investigate |
| Provider-admin access or silent substitution | Preserve enterprise custody and approved hosted configuration | Shared-responsibility fields, support sessions, corroboration, change notices and load identity | Unapproved access or provider, model, precision, safety, region or subprocessor change fails | Restrict, reclassify or exit provider |
| Provider deletion or export corroboration failure | Require independently supportable hosted custody, portability and destruction claims | Provider deletion/export records, enterprise destination receipt, residual search, key/copy inventory and independent corroboration | Export is complete and attributable and deletion covers every obligated copy; unsupported assertions fail | Restrict new use, preserve claims and evidence, escalate, reclassify or exit |
| Failed rollback and recovery | Recover only to a complete eligible state | Rollback decision, closure, cache, trust, recovery and validation evidence | No partial, corrupt, revoked, weaker, incompatible or silently substituted state becomes active | Forward recover or safe stop |
| Edge capture and clock rollback | Resist offline theft and stale authority | Boot, sealed-key, media, debug, bundle, monotonic-time and custody tests | Captured media and rollback cannot yield usable artifacts, keys, or extended authority | Revoke and require governed re-enrollment |
| Evidence-buffer exhaustion or divergent reconnect | Preserve bounded offline evidence and reconcile one authoritative history | Buffer capacity, overflow, sequence, signed bundle, local/central state and reconnect-conflict tests | Buffer exhaustion invokes the approved safe state; divergence is detected and resolved without discarding contradictory evidence or extending authority | Safe stop, quarantine node state and escalate reconciliation |
| Compromised or ineligible restore | Prevent backup from bypassing current authorization | Atomic backup, isolated restore, admin, region, license, key and revocation evidence | Partial, compromised-admin, wrong-region, keyless, revoked or expired restore stays isolated | Reject restore; incident and recovery escalation |
| Evidence suppression | Keep authoritative evidence independent | ARC-P160 integrity, gap, access and negative-admin tests | Build, runtime, provider and ordinary administrators cannot alter, select, suppress, or delete evidence | Stop required assurance; investigate |
| Expired or orphaned emergency credentials | Bound exceptional privilege | Issuance, purpose, session, tunnel, expiry, revocation and orphan scans | Every credential and tunnel expires automatically and is absent after use | Revoke, contain and review all affected paths |
| Timed fleet-wide revocation | Meet declared propagation latency online and offline | Signed decision, acknowledgments, stale caches, sessions, edge reconciliation and timer | Every reachable enforcement point meets the bound; failures remain visible | Safe stop affected use and escalate missed acknowledgments |
| Injected advisory response | Discover and remediate fleet and derivatives | Injected model, code, driver, firmware, license or acceptable-use notice; lineage and deadline evidence | Fleet impact, emergency block, rebuild, revalidation and propagation complete within tier deadlines | Quarantine or route-block affected releases |
| Post-retirement residual-artifact search | Demonstrate complete retirement and destruction | Searches of registry, staging, checkpoints, adapters, snapshots, backups, disks, dumps, RAM, HBM, support/provider copies, wrapped keys, HSM, escrow and holds | No unauthorized residue remains; retained exceptions have legal basis, protection and tombstone | Revoke access, sanitize residue, escalate exceptions |

Acceptance requires every template section to be substantive; all seven named zones and CP1-CP21 to be represented; all 91 catalog controls to resolve under required, inherited-and-verified, or conditional allocation; the same immutable release identity at registry and admission; unambiguous inference-only CP6/CP7 treatment; role independence; testable supply-chain, licensing, adaptation, validation, trust, serving, isolation, egress, monitoring, continuity, revocation, destruction and hosted-boundary requirements; current evidence; and successful architecture, control, unit, pull-request and post-merge validation.

Every assessment package shall include a CP1-CP21 assurance matrix with exactly one row for each of CP1, CP2, CP3, CP4, CP5, CP6, CP7, CP8, CP9, CP10, CP11, CP12, CP13, CP14, CP15, CP16, CP17, CP18, CP19, CP20, and CP21. The matrix resolves inference-only not-applicable decisions but never omits a row, and uses this required schema:

| Assurance-matrix field | Required content |
|---|---|
| Control point and objective | CP identifier and the required outcome from the control-point table, expressed as a testable objective |
| Applicable controls | Every required, inherited-and-verified, and conditionally triggered catalog control supporting the objective |
| Accountable role | Catalog `owner_role` for each mapped control and the accountable capability or data owner where applicable |
| Evidence-producing roles | Named implementation, provider, custodian, operations, security and assurance roles that generate source evidence |
| Artifacts and source evidence | Immutable identities, records, configurations, manifests, logs, attestations, tests, approvals, receipts and outcomes used for assessment |
| Procedures and frequency | Operating and assessment procedure, trigger, cadence, sample, negative case, independence and escalation path |
| Pass/fail and disposition | Objective-specific acceptance basis, finding owner, remediation deadline, exception authority, safe stop and resumption evidence |

## Variants and alternatives

- **Shared private inference platform:** maximizes utilization; requires risk-tiered placement and empirical isolation and is not preferred for incompatible Tier 4 or legal domains.
- **Dedicated high-assurance enclave:** separates runtime, keys, administration, and evidence when co-residency is unacceptable, with higher cost and complexity.
- **Regional private serving:** constrains artifacts, inference, administration, support, replication, evidence, and recovery to approved regions while preserving consistent revocation.
- **Disconnected or edge deployment:** uses signed bundles, monotonic time, anti-rollback, maximum offline periods, capture resistance, local evidence, reconciliation, and safe stop.
- **Adapter-based multi-tenant serving:** shares a base only when adapters, routing, batching, caches, scheduler, artifacts, telemetry, and evidence are isolated and independently tested.
- **Confidential-computing deployment:** adds measured or protected execution against selected threats but does not replace supply-chain, administrator, runtime, side-channel, evidence, recovery, or destruction controls.
- **Dedicated hosted infrastructure:** assigns documented fields to a supplier while enterprise lifecycle accountability, qualification, corroboration, change control, portability, exit, and destruction rights remain.

## Anti-patterns

- Downloading model artifacts directly into production.
- Treating model formats, tokenizers, templates, loaders, or dependencies as inert data.
- Using mutable model names or tags as release identity.
- Allowing builders, validators, signers, registry administrators, trust custodians, or deployers to approve their own changes.
- Treating a hash check as proof of provenance, safety, license, purpose, or current authorization.
- Reusing adaptation data, checkpoints, adapters, gradients, logs, or outputs beyond approved purpose.
- Changing quantization, conversion, adapter, tokenizer, template, safety, runtime, driver, firmware, or hardware without revalidation or a preapproved tested equivalence rule.
- Allowing production runtimes unrestricted internet access, package installation, telemetry export, support tunnels, or direct model acquisition.
- Sharing infrastructure without queue, batch, scheduler, memory, cache, adapter, accelerator, telemetry, backup, support, quota, and administrative isolation.
- Assuming accelerator partitioning or confidential computing eliminates side channels, residual state, or administrator risk.
- Exposing logits, embeddings, errors, debug data, or diagnostics without extraction, privacy, and purpose analysis.
- Silently failing over to another model, adapter, precision, provider, region, safety setting, data use, or retention behavior.
- Restoring a backup that reactivates a revoked, expired, vulnerable, license-invalid, wrong-region, or incomplete model.
- Declaring retirement complete while weights, adapters, caches, snapshots, backups, device memory, keys, exports, support, provider, or subprocessor copies remain usable.

## Related patterns

- `ARC-P100` supplies shared inference access, admission, policy, routing, and provider controls; ARC-P140 owns enterprise-operated model supply, runtime, and artifact custody.
- `ARC-P110` governs workforce-copilot interaction and consumes approved private inference.
- `ARC-P120` governs retrieval, grounding, citations, vector and knowledge custody; ARC-P140 governs the privately served embedding, reranking, or generation release.
- `ARC-P130` governs agent identity, authority, tools, actions, and outcomes; ARC-P140 governs the underlying model and runtime infrastructure.
- `ARC-P160` supplies independent monitoring, protected evidence, detection, response, assessment, and assurance; ARC-P140 supplies model, build, registry, serving, revocation, and destruction events.

## Change history

| Pattern version | ESAF release | Date | Change |
|---|---|---|---|
| 0.1.0 | 0.4-alpha | 2026-07-12 | Initial draft |
