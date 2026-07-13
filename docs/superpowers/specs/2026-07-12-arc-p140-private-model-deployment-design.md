# ARC-P140 Private Model Deployment Design Specification

**Status:** Approved design; pending written-spec review  
**Target:** ESAF-1200 ARC-P140 Draft pattern  
**Release:** 0.4-alpha  
**Date:** 2026-07-12

## 1. Purpose

ARC-P140 defines a vendor-neutral architecture pattern for enterprise-operated model inference and adaptation across on-premises, private-cloud, dedicated-hosted, and isolated edge environments.

The pattern governs acquired, open, commercial, internally developed, fine-tuned, adapter-based, quantized, converted, pruned, or otherwise transformed models. Foundation-model pretraining from scratch is outside this baseline.

## 2. Design decision

Use a **controlled model supply chain and federated serving fabric**.

Acquisition, quarantine, adaptation, validation, release signing, registry administration, trust-anchor custody, deployment, serving, and assurance are distinct trust functions connected by explicit promotion gates. Development and build, model validation, release authority, registry administration, trust-anchor administration, and production deployment have separated duties, governed conflict checks, and narrow, time-bounded emergency exceptions. Governance, artifact identity, release authority, and evidence are centrally governed. Serving may be shared, dedicated, regional, hosted, or edge-based according to tier, data, obligation, and co-residency risk.

ARC-P140 composes with:

- ARC-P100 for shared inference access, admission, policy, and routing;
- ARC-P110 for workforce copilot interaction where applicable;
- ARC-P120 for retrieval and grounding;
- ARC-P130 for agentic or consequential action;
- ARC-P160 for authoritative evidence, monitoring, and assurance.

## 3. Scope and custody boundary

ARC-P140 applies when the enterprise operates or controls the lifecycle of model artifacts and private inference, including through dedicated hosted infrastructure under documented shared responsibility.

“Private” describes custody, deployment, and control boundaries; it does not by itself establish confidentiality, safety, integrity, isolation, or compliance. The threat model includes artifact theft, extraction, replacement, hostile loaders and formats, poisoned adaptation, model inversion and membership inference, shared-accelerator and administrative side channels, supplier and privileged-user abuse, rollback to revoked state, and destructive loss.

Every deployment records who controls and can access:

- source and transformed model artifacts;
- signing and encryption keys;
- training, adaptation, and evaluation data;
- build, validation, registry, deployment, and serving administration;
- compute hardware, accelerators, firmware, drivers, schedulers, networks, and storage;
- backups, telemetry, support tooling, incident evidence, and destruction.

Provider-operated endpoints that do not give the enterprise sufficient control or evidence over artifact identity, runtime integrity, isolation, lifecycle, and destruction remain governed as external services rather than satisfying ARC-P140 by label alone.

Adaptation and build activities, evidence, and CP6–CP7 apply when fine-tuning, adapter creation, quantization, conversion, pruning, packaging, or another material transformation occurs. Inference-only deployments document these activities as not applicable; source, provenance, validation, release, registry, custody, and deployment controls remain mandatory.

Dedicated hosted deployments maintain a field-level shared-responsibility matrix for hardware, hypervisor, firmware, drivers, artifact custody, keys, privileged personnel and subprocessors, support, telemetry, incident timing, substitution and change notice, isolation evidence, backups, destruction, portability, and exit. Minimum qualification requires current evidence for immutable release identity, runtime integrity, tenant isolation, privileged access, incident notification, artifact and key custody, backup and deletion, portability, and exit. Evidence has an approved review cadence and expiry; material provider change or expired, incomplete, or uncorroborated evidence triggers restriction, exit, or reclassification under `API-140`. Provider assertions remain externally asserted unless independently corroborated. Unilateral substitution of model, adapter, precision, runtime, region, or safety configuration is prohibited.

## 4. Intended outcomes

ARC-P140 shall provide:

- attributable artifact provenance, license, ownership, transformation, and validation;
- hostile-artifact containment before model code or data enters trusted environments;
- authorized and reproducible adaptation with governed intermediate artifacts;
- immutable, signed, purpose- and tier-scoped releases;
- protected artifact custody and complete registry history;
- risk-tiered shared or dedicated serving with demonstrated isolation;
- deny-by-default runtime egress and separately governed import/export;
- verified runtime, hardware, configuration, model, adapter, and policy identity;
- capacity, resilience, rollback, revocation, recovery, and destruction;
- authoritative evidence independent of build and serving runtimes.

## 5. Seven-zone architecture

### 5.1 Acquisition and intake zone

Accepts artifacts only from approved sources through controlled transfer. It records supplier, source, license, permitted uses, original identity, hashes, signatures, trust anchors, bills of materials, security notices, transfer custody, and intake owner.

### 5.2 Quarantine and inspection zone

Isolates untrusted models, tokenizers, templates, loaders, custom code, plugins, dependencies, serialized objects, archives, and metadata. It performs format validation, malware and unsafe-code analysis, dependency and license inspection, signature and provenance verification, resource-bomb testing, and policy evaluation without production credentials or unrestricted network access.

### 5.3 Adaptation and build zone

Performs authorized fine-tuning, adapter creation, quantization, conversion, pruning, packaging, and reproducible build. It binds approved base artifacts, data, purpose, code, parameters, operators, compute, dependencies, intermediate state, outputs, and evidence.

### 5.4 Validation and release zone

Evaluates immutable release candidates for provenance, license, security, privacy, quality, safety, bias, performance, compatibility, resource behavior, and approved purpose. It supports independent review, release decision, signing, expiry, and rollback preparation.

### 5.5 Registry and artifact-custody zone

Maintains authoritative artifact identity, lineage, version, signature, approval, purpose, tier, environment, configuration, retention, legal hold, revocation, rollback, and retirement state. It protects weights, adapters, tokenizers, templates, configurations, and related artifacts from unauthorized access, replacement, extraction, deletion, or duplication.

### 5.6 Deployment and serving zone

Admits only authorized releases and configurations. It performs verified model loading, risk-tiered tenant placement, runtime admission, inference, cache and scheduler isolation, input/output protection, quotas, scaling, safe fallback, draining, rollback, and termination.

### 5.7 Evidence and operations zone

Uses ARC-P160 to provide protected build, validation, release, registry, deployment, inference, integrity, drift, capacity, cost, incident, recovery, revocation, and destruction evidence. Build and serving runtimes cannot select, rewrite, suppress, or delete authoritative evidence or assurance verdicts.

## 6. Artifact identity, provenance, and executable formats

Each artifact has an immutable identity bound to source, supplier, license, hashes, signatures, architecture, format, tokenizer, configuration, dependencies, training lineage, adaptation lineage, transformation history, known limitations, validation, and approved scope.

A release is an immutable closure, not weights alone. Its manifest cryptographically binds all weight shards; tokenizer and vocabulary; chat, system, and prompt templates; adapters; draft or speculative models; loaders; custom and native kernels; libraries and dependencies; runtime image; safety configuration; precision; and approved hardware, firmware, and driver compatibility. Inspection, validation, signing, registry, deployment, load, and attestation verify the same closure and block time-of-check/time-of-use substitution.

Original and derived artifacts remain linked. Conversion, quantization, pruning, adapter merge, tokenizer change, template change, loader change, precision change, or packaging creates a new artifact identity and lineage edge.

Model formats, serialized objects, tokenizers, templates, loaders, custom code, plugins, native extensions, kernels, build scripts, and dependencies are potentially executable and hostile. Quarantine covers parser and decompression attacks, pickle and dynamic loading, remote-code flags, tokenizer or template execution, path traversal and symlinks, oversized tensors and shards, and CPU, accelerator, memory, storage, and time exhaustion. Disposable workers have no enterprise or production credentials, no writable trusted registry, bounded resources, restricted ingress and egress, protected output channels, and sanitization before reuse. Only sanitized outputs cross the quarantine boundary. Unsafe artifacts are converted through an approved non-executing or sandboxed process or rejected.

## 7. Licensing, intellectual property, and permitted use

Before adaptation or deployment, the organization records license text and version, copyright and source, commercial use, hosting, redistribution and modification rights, derivative-work and output terms, use restrictions, attribution and disclosure duties, patent terms, acceptable-use limits, export-control and sanctions obligations, geography, expiration, change and revocation triggers, and downstream obligations.

License or policy compatibility is evaluated transitively for the base model, code, datasets, adapters, dependencies, output use, deployment, distribution, and derivative artifacts. License telemetry or call-home cannot bypass runtime egress policy. Unresolved or incompatible terms prohibit the affected adaptation, release, environment, use, or distribution.

Model artifacts, prompts, outputs, evaluation data, and adaptation results receive intellectual-property classification and protection. Artifact access does not imply authority to copy, export, fine-tune, merge, redistribute, or use for another purpose.

## 8. Adaptation data and build governance

Adaptation jobs use approved datasets, purposes, base artifacts, code, parameters, operators, identities, compute classes, environments, and retention. Data authority, classification, minimization, quality, lineage, privacy rights, consent or legal basis, licensing, and representativeness are established before use.

Adaptation and validation continue to treat imported model components, loaders, kernels, and dependencies as hostile workloads. Jobs use ephemeral isolated workers, short-lived identities, no long-lived or production credentials, governed dependency import, default-deny network access, lateral-movement controls, immutable or read-only input mounts, bounded CPU/accelerator/memory/storage/time, write-only controlled output staging, and no direct write access to a trusted registry. Checkpoints, adapters, logs, metrics, reports, and artifacts pass malware, data-loss, policy, and integrity inspection before promotion.

Training, validation, and holdout sets are separated and versioned. Poisoning, backdoor, trigger, contamination, duplication, leakage, and representativeness risks are assessed. Checkpoints and intermediate adapters undergo admission checks and cannot bypass quarantine, validation, signing, registry, or deployment gates.

Training data, checkpoints, adapters, gradients, optimizer state, caches, logs, samples, and failed outputs receive the highest applicable classification and inherit data, privacy, IP, secondary-use, retention, residency, legal-hold, and deletion obligations. They are tested for secrets, regulated data, and unintended memorization.

Build manifests capture source identities, code and dependency versions, parameters, randomness and determinism controls, environment and hardware class, operators, timestamps, resource use, intermediate artifacts, and outputs. Reproducibility evidence explains and repeats material transformations without requiring unrestricted retention of sensitive data.

Secrets, credentials, personal data, restricted source material, and memorized content are tested before release. Data deletion or correction triggers documented evaluation of whether retraining, adapter replacement, restriction, or other remediation is required.

Deletion and correction propagate to dataset versions and derived artifacts where required. The organization documents the technical limits of unlearning and deletion and does not claim removed influence when it cannot be demonstrated.

## 9. Validation, equivalence, and release

Validation covers intended purpose and populations, security, privacy, quality, safety, harmful bias, robustness, memorization and extraction, prompt abuse, performance, capacity, compatibility, hardware and runtime behavior, observability, rollback, and known limitations.

Release decisions bind an immutable candidate to approved purpose, tier, environment, runtime class, precision, adapters, tokenizer, template, loader, safety settings, hardware/software compatibility, thresholds, expiry, and evidence.

Any post-validation change to weights, adapter, tokenizer, template, loader, precision, quantization, safety configuration, runtime, driver, firmware, serving engine, material dependency, or hardware class invalidates the prior decision unless a documented equivalence rule was approved and tested beforehand.

Release signing is performed by an authorized authority separated from build and deployment administration, with dual or threshold authorization for high-tier releases. Signing keys have governed issuance, non-exportability where supported, identity and purpose binding, rotation, revocation, compromise response, algorithm agility, trusted time, verifier freshness, and independently protected trust anchors. A cryptographically valid signature from an expired, compromised, revoked, wrong-purpose, or untrusted key does not authorize release.

## 10. Registry and artifact custody

The registry is authoritative for artifact identity and release state. Production deployment references immutable release identifiers rather than mutable names or tags.

Artifacts are encrypted in transit and at rest with access scoped by role, purpose, environment, tenant, and lifecycle. Encryption and signing trust roots are separate where appropriate. Key custodianship, recovery, rotation, destruction, and emergency access are documented.

The registry records download, upload, inspection, transformation, validation, approval, signing, promotion, replication, deployment, rollback, revocation, export, backup, restore, legal hold, retirement, and destruction events.

Ordinary build, platform, or serving administrators cannot rewrite authoritative lineage, substitute artifacts, approve their own releases, or erase custody and revocation history.

## 11. Deployment authorization and runtime integrity

An authorized deployment controller verifies release state, signature, hash, purpose, tier, environment, runtime and hardware compatibility, configuration, dependencies, and policy before loading.

Production serving uses separate workload identities, least privilege, protected secrets, immutable or measured configuration, controlled administration, approved images and drivers, verified time, and complete audit evidence. Runtime attestation or equivalent integrity evidence binds the complete release closure, runtime image and configuration, hardware, firmware, driver, tenant, and isolation mode rather than only host boot state. Attestation uses a trusted verifier, challenge or nonce, workload and boot epoch, maximum evidence age, replay detection, current revocation and trust status, and fail behavior. Relevant change, resume, migration, reconfiguration, or trust update triggers re-attestation.

The runtime cannot modify authoritative artifacts, promote a replacement, change registry state, or silently load an unapproved adapter, tokenizer, template, precision, safety setting, or model.

Privileged operations across build, validation, signing, registry, trust anchors, deployment, runtime, KMS, backup, support, and destruction use distinct named identities, just-in-time or break-glass access, bounded purpose and duration, dual authorization for high-impact actions, session and evidence capture, conflict-of-interest checks, and independent review. Builders cannot validate or promote their own candidates; validators cannot self-sign; signers cannot change registry approval; registry administrators cannot alter trust roots; and build or runtime administrators cannot self-promote, weaken egress, alter trust stores, or suppress authoritative evidence.

## 12. Tenancy and accelerator isolation

Shared serving is permitted only when isolation is demonstrated across request queues and dynamic batching, schedulers and preemption, accelerator HBM and residual pages, host and shared memory, IPC, peer-to-peer, DMA and RDMA, key-value, prefix, prompt, and response caches, adapters and LoRA routing, tokenizer and template state, speculative-decoding draft models, temporary files, storage, network, model routing, response delivery, device plugins, logs, traces, metrics, profiling, crash dumps, debugging, backups, support paths, quotas, priorities, and administration.

Tenant and capability identity is bound at admission and preserved through batching, inference, caching, evidence, and response. User-supplied tenant fields are not authoritative.

Accelerator controls address residual memory, direct memory access, peer-to-peer access, device plugins, firmware, drivers, partitioning, virtualization, scheduler behavior, error handling, thermal and power exhaustion, and sanitization before reassignment, repair, return, or retirement. Hardware partitioning and confidential-computing claims require empirical verification for the selected workload and do not by themselves establish tenant isolation.

Isolation tests cover content and state leakage plus timing, latency, cache occupancy, error and cardinality behavior, utilization, power and thermal signals, and covert channels. Approved leakage thresholds are tested repeatedly with representative adversarial co-tenants on the exact hardware, firmware, driver, scheduler, and partition configuration. Tier 4 workloads, incompatible legal or data domains, untrusted adapters, or configurations that exceed thresholds or cannot bound co-residency and side-channel risk use dedicated runtime boundaries.

## 13. Inference protection and model extraction

Admission authenticates and authorizes callers, capability, tenant, purpose, model, adapter, tier, limits, and data handling. Inputs and outputs are classified, validated, bounded, and protected according to the consuming pattern.

The service enforces per-principal, capability, and tenant budgets; concurrency, token and sequence limits; batch limits; timeouts; cancellation; memory and compute ceilings; cache controls; distributed and low-and-slow abuse detection; and fair scheduling. Resource failure cannot cross tenant boundaries or expose prior content.

Model-extraction, membership-inference, memorization, inversion, evasion, and probing risks are assessed. Bulk, high-entropy, near-boundary, multi-identity, and cross-tenant query campaigns are correlated. Rate, query-pattern, response-detail, confidence, logit, embedding, adapter, error, debug, and diagnostic exposure are limited according to purpose and risk. Extraction alerts integrate with incident response. Safeguards do not claim to eliminate extraction where the interface necessarily exposes model behavior.

## 14. Network and import/export separation

Production inference runtimes use deny-by-default external egress across IPv4, IPv6, DNS, metadata and identity endpoints, service mesh and control planes, package and model registries, telemetry, crash dumps, support tunnels, approved data sinks, and direct host or accelerator paths. They do not directly acquire models, packages, updates, licenses, or unrestricted external content.

Artifact import, dependency resolution, license activation, update, support, telemetry export, and model export use separately authenticated, authorized, inspected, logged, and approved channels with signed manifests, malware and data-loss inspection, destination authorization, bounded queues, reconciliation, and one-way controls where justified. Export includes purpose, recipient, destination, classification, license, integrity, encryption, residency, and custody validation.

Exceptions are narrowly allowlisted, time-bounded, monitored, reviewed, and incapable of bypassing artifact promotion or evidence controls. Emergency support requires dual authorization, recording, automatic expiry, and verification that no tunnel or credential persists. DNS, metadata services, management networks, registries, approved sinks, and telemetry endpoints are protected from confused-deputy, credential-exfiltration, and covert-export paths.

## 15. Monitoring, drift, and response

ARC-P160 correlates source, build, validation, release, registry, deployment, runtime, model, adapter, tokenizer, template, configuration, hardware, input/output policy, integrity, performance, capacity, tenant, and incident evidence.

Monitoring detects unauthorized artifact or configuration change, signature or attestation failure, unknown version, drift, extraction attempts, memorization indicators, isolation failure, cache contamination, abnormal resource use, scheduler abuse, egress attempts, evidence gaps, and revocation failures.

The registry lineage graph drives continuous monitoring of model, code, dependency, driver, firmware, supplier, security-advisory, CVE, license-term, acceptable-use, export-control, and sanctions changes. The organization performs fleet impact analysis across derived artifacts and deployments, reconciles supplier notices, and defines emergency quarantine, release suspension, routing block, patch, rebuild, revalidation, and propagation deadlines according to severity and tier.

Operational dashboards and aggregate metrics are not authoritative release, custody, or incident evidence. Runtimes and ordinary administrators cannot suppress authoritative model identity, loading, inference, or failure evidence.

## 16. Continuity, rollback, and recovery

Capacity planning addresses accelerator availability, quotas, queues, batch behavior, model load time, cold start, scaling, storage, network, power, cooling, and dependency failure.

Rollback is a new deployment decision, not an unconditional safety mechanism. The target remains authorized, unexpired, without unresolved vulnerabilities that exceed approved deployment criteria, license-valid, data-compatible, policy-compatible, and free of revoked weights, restricted training-derived material, stale keys, weaker safety settings, or incompatible precision and runtime. When no safe rollback exists, the service uses an approved forward-recovery or safe-stop path. It never silently falls back to a different model, adapter, precision, provider, region, safety setting, or retention behavior.

Lower-tier service may use a preapproved degraded configuration with visible limitations, bounded duration and scope, preserved evidence, and no increase in data, authority, tenancy, or external connectivity. Tier 3 and Tier 4 inference stops when model identity, integrity, isolation, required validation, authorization, policy, or assurance becomes unknown.

An approved safe-failure matrix for each tier and deployment variant defines conditions that block promotion, new model load, new inference, or continued inference; permitted grace periods; identity, revocation, policy, and evidence freshness; capacity behavior; approved degraded substitutes; and resumption authority. It prevents either enterprise-wide denial from a local evidence outage or silent bypass of required assurance.

Recovery verifies artifact and configuration identity, isolation, data and cache state, evidence reconciliation, target capacity, and affected releases before return to service.

## 17. Backup, revocation, retirement, and destruction

Backups atomically and consistently preserve the complete artifact closure, registry metadata, approvals, lineage, signatures and trust state, policies, adapters, evidence, encryption, access, custody, retention, residency, legal hold, and revocation status. Keys are separately protected or recoverable through approved wrapping and separation of duties. Restore occurs into an isolated verification path before production use and cannot reactivate a revoked, expired, vulnerable, license-invalid, or wrong-region artifact without new authorization. Recovery tests cover ransomware, privileged-admin compromise, partial restore, stale trust state, residency violation, and KMS failure.

Revocation has defined maximum propagation latency and reaches registries, trust stores, credentials, caches, mirrors, deployment controllers, routing, active replicas, running instances, adapters, edge nodes, backups and restore eligibility, export destinations under enterprise control, and consuming capability records. Disconnected deployments use signed release, policy, and revocation bundles; trusted or monotonic time; anti-rollback; freshness and expiry; maximum offline operation; bounded local evidence; reconnect reconciliation; and safe stop after authority or evidence expiry. Lost edge nodes assume remote wipe may fail and trigger credential, artifact, and trust revocation accordingly.

Edge and disconnected deployments use risk-tiered hardware-bound storage encryption, secure or measured boot, sealed keys, debug-port and removable-media controls, local export restrictions, and tamper response where justified. Capture, loss, recovery, repair, or custody change requires revocation and governed re-enrollment before renewed trust. Physical-capture testing includes cold storage, removable media, debug interfaces, boot rollback, key extraction, and offline artifact access.

Retirement removes serving authorization, drains traffic, revokes credentials and releases, updates consumers, preserves required evidence, and disposes of weights, adapters, tokenizers, checkpoints, intermediate state, caches, temporary files, media, and device memory.

Destruction covers active replicas, registry objects and versions, staging and quarantine, checkpoints, adapters, optimizer state, converted and quantized derivatives, local and edge copies, snapshots, backups, temporary disks, crash dumps, RAM, shared memory, accelerator HBM, support copies, and provider or subprocessor copies. It uses media-specific sanitization or cryptographic erasure only when key-destruction prerequisites and replica coverage are demonstrated. Verification records exceptions, legal holds, residual-risk disposition, provider attestations, and signed tombstones that preserve custody without retaining prohibited content.

## 18. Control points

| CP | Control point | Required outcome | Primary implementation and evidence roles |
|---|---|---|---|
| CP1 | Model-source and supplier approval | Sources, suppliers, ownership, assurance, and permitted acquisition are approved | Model Owner; Procurement, Third-Party Risk, and Legal |
| CP2 | License and permitted-use validation | License, IP, use, modification, distribution, and downstream obligations are resolved | Legal; Model Owner and Procurement |
| CP3 | Secure artifact intake and transfer | Original identity, integrity, custody, classification, and transfer are preserved | Model Owner; Transfer Custodian and Security Engineering |
| CP4 | Quarantine and hostile-format inspection | Executable, malicious, unsafe, malformed, and resource-abusive artifacts are contained or rejected | Model Owner; Application Security and Vulnerability Management |
| CP5 | Provenance and lineage verification | Source, training, adaptation, transformation, dependency, and limitation lineage is attributable | Model Owner and Data Governance; Supplier and Build Engineering |
| CP6 | Training and adaptation data authorization | Data authority, purpose, quality, privacy, license, and retention are established | Data Owner; Privacy, Data Governance, and ML Operations |
| CP7 | Reproducible adaptation and build | Approved inputs, code, parameters, identities, compute, intermediate state, and outputs are reproducible and evidenced | Model Owner; ML Operations and Build Engineering |
| CP8 | Release-candidate security and quality validation | Immutable candidates meet approved security, privacy, safety, quality, bias, compatibility, and performance criteria | Model Validation Lead; Security, Privacy, Safety, and Performance Testers |
| CP9 | Artifact signing and trust-anchor governance | Only authorized releases are signed and verifiable through governed key lifecycle and trust anchors | Cryptographic Services and Model Owner; Release Authority, PKI/HSM, and Assurance |
| CP10 | Registry identity, metadata, and approval state | Immutable identities, lineage, scope, status, expiry, revocation, and history are authoritative | Model Owner; Registry Custodian and Release Management |
| CP11 | Encrypted artifact custody and access | Artifacts and keys resist unauthorized access, extraction, replacement, deletion, and duplication | Model Owner; Cryptographic Services, Artifact Custodian, and Storage Operations |
| CP12 | Deployment authorization and admission | Only approved releases, configurations, environments, runtimes, and hardware classes are admitted | AI Capability Technical Owner; Change Management and Platform Engineering |
| CP13 | Runtime identity and configuration integrity | Workload, runtime, image, driver, firmware, configuration, model, and adapter identity are verified | Platform Engineering; IAM, Cryptographic Services, and Runtime Operations |
| CP14 | Tenant, adapter, cache, scheduler, and accelerator isolation | Shared serving prevents cross-tenant state, authority, resource, telemetry, and side-channel compromise | AI Platform Owner and Application Owner; Platform, Accelerator, Scheduler, and Security Engineering |
| CP15 | Inference input, output, and resource protection | Callers, data, behavior, diagnostics, resources, and extraction exposure are bounded | Application Owner; Application Security, Model Validation, and SRE |
| CP16 | Deny-by-default egress and governed import/export | Runtime egress is denied and all external movement uses approved inspected channels | Platform Engineering and API Owner; Network Security and Import/Export Custodian |
| CP17 | Model integrity, drift, and behavioral monitoring | Unauthorized change, drift, abuse, extraction, isolation failure, and evidence gaps are detected | Model Owner and Security Operations; ML Operations and ARC-P160 Platform |
| CP18 | Capacity, continuity, rollback, and recovery | Capacity is governed and only approved known releases and states support fallback and recovery | Business Continuity and AI Service Owner; SRE, Model Owner, and Assurance |
| CP19 | Backup, retention, legal hold, and destruction | Copies remain governed and restoration or destruction preserves identity, obligations, and evidence | Data Owner and Compliance; Records, Privacy, and Backup Custodians |
| CP20 | Retirement, revocation, and residual-artifact removal | Authorization and every material artifact residue are removed or preserved only as required | Model Owner and AI Capability Business Owner; Registry, Platform, and Data Custodians |
| CP21 | Evidence, incident response, and independent assurance | Protected evidence supports investigation, assessment, accountability, and management review | Incident Response and Assurance; Security Operations, Internal Audit, and Evidence Custodian |

Catalog `owner_role` remains authoritative; these pattern roles assign implementation and evidence duties without transferring accountability.

## 19. Control alignment

Required controls are:

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

`GOV-100`, `GOV-110`, `GOV-120`, `RSK-100`, `STR-100`, `STR-130`, `API-100`, `ARC-120`, `ARC-150`, `EDU-100`, and `EDU-120` are normally inherited from enterprise governance, strategy, ARC-P100, architecture lifecycle, and workforce programs and must be verified at each hosted, regional, and edge boundary.

Conditional controls include `RSK-130` for individual, group, safety, environmental, or societal impact; `DAT-140` for personal data and rights; `DAT-150` for retrieval or embedding services; `DAT-160` when outputs or feedback are retained, evaluated, shared, or reused; `CMP-120` for external model, host, or supplier; `CMP-130` for jurisdiction, residency, or transfer; `API-120` and `API-130` for plugins, tools, MCP, or orchestration; `API-140` for dedicated hosted or external services; `AGT-100` through `AGT-160` and `MON-130` for agentic operation; `STR-110` for value claims; `STR-120` for experimentation; and `EDU-140` for governance personnel.

Catalog `owner_role` remains accountable. Pattern roles identify implementation and evidence responsibility without transferring accountability.

## 20. Evidence and assessment

Required evidence includes:

- source, supplier, license, permitted-use, transfer, and custody records;
- original and transformed hashes, signatures, trust-anchor history, model and dependency bills of materials, security advisories, and provenance;
- quarantine topology, hostile-format tests, malware and dependency scans, sandbox escape and resource-exhaustion tests, and sanitization evidence;
- adaptation data authority, classification, lineage, quality, privacy, license, retention, deletion, and representativeness evidence;
- build manifests, code and parameters, operator and workload identities, environment and hardware, intermediate-state inventory, reproducibility, and output identity; adaptation and validation isolation, egress, read-only input, output staging, DLP, malware, lateral-movement, metadata-service, and log/metric/checkpoint exfiltration tests;
- security, privacy, safety, bias, robustness, extraction, memorization, performance, compatibility, capacity, and rollback validation;
- release decision, approved scope, equivalence rules, signature, expiry, rollback, and separation-of-duties evidence;
- registry history, access reviews, encryption, key lifecycle, replication, export, backup, restore, revocation, and legal-hold evidence;
- runtime image, driver, firmware, hardware, workload identity, configuration, fresh nonce-bound attestation, replay and migration tests, model-load, and deployment evidence;
- tenant, batching, scheduler, accelerator memory, cache, adapter, storage, network, telemetry, debug, quota, timing, latency, occupancy, cardinality, power, thermal, utilization, covert-channel, and side-channel isolation thresholds and tests;
- input/output, abuse, extraction, inference, diagnostic, quota, capacity, cancellation, and denial-of-service tests;
- egress-denial, import/export, registry, license, telemetry, metadata-service, DNS, credential-exfiltration, and exception tests;
- model identity, integrity, drift, behavior, capacity, incident, rollback, recovery, and assurance evidence through ARC-P160;
- continuous advisory, vulnerability, license, supplier-notice, fleet-impact, emergency-block, patch, rebuild, revalidation, and propagation evidence, including an injected model, code, driver, firmware, license, or acceptable-use change that exercises lineage-based fleet and derived-artifact discovery, emergency quarantine or routing block, remediation deadlines, rebuild, revalidation, and propagation;
- field-level provider shared-responsibility matrices, independent corroboration, qualification expiry, substitution notices, provider-admin access tests, deletion/export corroboration, privileged-support evidence, incident timing, portability, exit, and destruction rights;
- per-tier and per-variant safe-failure matrices covering promotion, load, inference, grace, freshness, degraded substitutes, evidence, and resumption authority;
- backup atomicity, partial and wrong-region restore, ransomware and administrator compromise, KMS recovery, disconnected revocation, clock anti-rollback, offline expiry, reconciliation, edge physical capture, boot and key protection, debug and removable media, draining, destruction, residual-memory, media, supplier, and retirement tests; and
- timed end-to-end revocation exercises across online and intermittently connected registries, trust stores, credentials, caches, mirrors, controllers, routing, active replicas, running instances, adapters, edge nodes, backup restore eligibility, export destinations, and consumers, including stale caches, active sessions, failed acknowledgments, enforcement within the declared maximum, and escalation or safe stop when the bound is missed;
- a CP1-CP21 assurance matrix mapping controls, accountable and evidence-producing roles, artifacts, procedures, and objectives.

Negative testing includes a substituted model shard, malicious tokenizer or template, path traversal, pickle or native extension, dependency confusion, archive and decompression bombs, oversized tensors, and quarantine escape; adaptation or validation exfiltration through network, metadata, logs, metrics, checkpoints, adapters, shared storage, or lateral movement; artifact, adapter, draft-model, safety, precision, runtime, driver, or firmware substitution between inspection and load; stale, replayed, cross-host, or cross-tenant attestation; expired, revoked, compromised, wrong-purpose, wrong-tenant, stale-trust, bad-time, or downgraded-algorithm signatures; poisoned and backdoored data or checkpoints, secret and personal-data memorization, validation contamination, and direct intermediate-artifact promotion; license mismatch and changed or revoked rights; unreproducible builds and equivalence-rule abuse; builder self-validation, validator self-signing, signer registry change, registry-admin trust-root change, collusion, and unauthorized promotion; expired, orphaned, or unrevoked break-glass or support credentials and tunnels across build, registry, runtime, KMS, backup, and provider-support paths; cross-tenant batch, cache, adapter, speculative-model, scheduler, HBM, P2P, DMA, RDMA, timing, occupancy, power, thermal, telemetry, profiler, crash-dump, backup, and support leakage; distributed low-and-slow model extraction and membership inference; quota, queue, memory, thermal, power, and starvation exhaustion; IPv6, DNS, metadata, mesh, registry, crash-dump, support-tunnel, and approved-sink egress bypass; provider-admin artifact access, unverifiable deletion or export, and silent provider, model, precision, safety, region, or subprocessor change; incomplete loading, corrupt cache, failed rollback, and forward recovery; stale or replayed edge bundles, clock rollback, evidence-buffer exhaustion, stolen nodes, debug-port access, and divergent reconnect; partial, revoked, license-expired, wrong-region, compromised-admin, or keyless backup restore; runtime or build administrator evidence suppression and trust-store change; and post-retirement search across registry versions, caches, staging, checkpoints, adapters, snapshots, backups, temporary disks, crash dumps, RAM, HBM, support copies, provider copies, wrapped keys, HSM copies, escrow, and legal holds.

## 21. Variants

- **Shared private inference platform:** maximizes utilization and centralized operations; requires demonstrated isolation and is not preferred for incompatible Tier 4 or legal domains.
- **Dedicated high-assurance enclave:** isolates runtime, keys, administration, and evidence; preferred when co-residency or shared control is unacceptable, at higher cost and operational complexity.
- **Regional private serving:** keeps artifacts, inference, and evidence within regional boundaries; requires controlled replication and consistent revocation.
- **Disconnected or edge deployment:** supports limited connectivity and local inference; requires signed bundles, maximum offline periods, local evidence, revocation reconciliation, and safe stop.
- **Adapter-based multi-tenant serving:** shares a base model while isolating adapters, caches, batching, and evidence; prohibited when adapter or tenant isolation cannot be demonstrated.
- **Confidential-computing deployment:** adds measured or protected execution; useful against selected infrastructure threats but does not replace supply-chain, runtime, administrator, side-channel, or destruction controls.
- **Dedicated hosted infrastructure:** assigns defined controls to a supplier while retaining enterprise lifecycle accountability; requires evidence, key, support, incident, portability, and destruction rights.

## 22. Anti-patterns

- Downloading model artifacts directly into production.
- Treating model formats, tokenizers, templates, or loaders as inert data.
- Using mutable model names or tags as release identity.
- Allowing builders, validators, signers, and deployers to approve their own changes.
- Treating a successful hash check as proof of provenance, safety, or license compliance.
- Reusing adaptation data, checkpoints, adapters, or logs outside their approved purpose.
- Applying quantization, conversion, adapter, tokenizer, template, or runtime changes without revalidation or approved equivalence.
- Allowing production runtimes unrestricted internet access or package installation.
- Sharing serving infrastructure without cache, batch, scheduler, memory, adapter, telemetry, and administrative isolation.
- Assuming accelerator partitioning eliminates side channels or residual state.
- Exposing logits, embeddings, errors, or diagnostics without extraction and privacy analysis.
- Silently failing over to another model, adapter, precision, provider, region, or safety configuration.
- Restoring a backup that reactivates a revoked or expired model.
- Declaring retirement complete while weights, adapters, caches, snapshots, backups, device memory, or export copies remain active.

## 23. Acceptance criteria

ARC-P140 is complete when:

- every architecture-template section is substantively populated;
- all seven zones and twenty-one control points are represented;
- enterprise-operated inference and adaptation, multi-host custody, risk-tiered tenancy, and deny-by-default runtime egress are explicit;
- supply chain, hostile formats, licensing, data, build, validation, signing, registry, custody, serving, accelerator, extraction, network, monitoring, continuity, revocation, and destruction requirements are testable;
- control accountability and evidence producers are assigned;
- all required, inherited, and conditional control IDs resolve;
- the registry links ARC-P140 and changes its state to Draft;
- unit, architecture, control, PR, and post-merge validation pass.

## 24. Out of scope

This milestone does not define foundation-model pretraining from scratch, select model or accelerator products, prescribe universal performance or safety thresholds, implement a full data-engineering platform, configure specific cloud services, claim confidential computing eliminates all infrastructure risk, or assert external-standard compliance mappings.
