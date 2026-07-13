# ARC-P120 Retrieval-Augmented Generation

## Metadata

**Pattern ID:** ARC-P120

**Status:** Draft

**Version:** 0.1.0

| Field | Value |
|---|---|
| Owner | Enterprise Architecture |
| Required reviewers | Data Governance, Security Architecture, AI Engineering, Application Engineering, Privacy, Operations |
| Pillars | Protect AI, Utilize AI, Govern AI |
| Lifecycle stages | Data Readiness, Architecture, Development, Validation, Approval, Deployment, Operations, Monitoring, Retirement |
| Capability tiers | Tier 1 through Tier 4; Tier 0 when enterprise information is indexed or retrieved |
| Deployment models | Centralized, federated, regional, sovereign, ephemeral, external managed service |
| Primary pattern role | Primary RAG pattern; supported by ARC-P100 and ARC-P160 |
| Supersedes | None |

## Purpose

Provide governed retrieval-augmented generation that grounds AI responses in authorized enterprise knowledge while preserving source authority, classification, lineage, provenance, tenant isolation, instruction boundaries, citation integrity, evidence, and safe failure.

## Problem statement

RAG combines knowledge ingestion, transformation, embeddings, indexes, retrieval, context assembly, model inference, citations, and feedback. If source security attributes, permissions, lineage, or instruction trust are lost between these stages, the system can expose protected information, amplify poisoned content, fabricate citations, cross tenant boundaries, or present stale and unsupported claims as grounded answers.

Organizations require a consistent pattern that separates knowledge publication from query execution, enforces authorization inside retrieval, and supports centralized governance with federated domain or regional knowledge ownership.

## Intended outcomes

- Only approved, suitable, attributable, and governed sources enter production knowledge.
- Source identity, version, classification, authorization, retention, and deletion state survive transformation and indexing.
- Retrieval authorization occurs before protected content or metadata is exposed.
- Tenant, domain, index, session, cache, and result boundaries remain isolated.
- Retrieved content cannot override higher-authority instructions, identity, policy, tools, routing, or memory.
- Material claims are traceable to exact authorized source versions or handled as unsupported.
- Feedback cannot poison knowledge or training data without independent review and publication.
- Source, index, embedding, retrieval, prompt, model, and configuration changes are versioned, evaluated, reversible, and observable.
- Federated knowledge services use consistent metadata, authorization, citation, evidence, and failure contracts.

## Non-goals

ARC-P120 does not prove that a source or generated claim is objectively true, guarantee factual output, define provider routing already addressed by ARC-P100, authorize agent tools or consequential actions, prescribe vector databases or algorithms, or establish external compliance.

The pattern does not permit broad retrieval followed by post-generation redaction as authorization, and it does not treat a citation as valid unless the exact source and version resolve and the user remains authorized.

## Applicability

Use ARC-P120 when a capability retrieves enterprise or external knowledge to ground model responses, including semantic search, document assistants, question answering, policy assistance, support copilots, and knowledge-grounded workflows.

ARC-P120 may use centralized, domain, regional, sovereign, ephemeral, or externally managed retrieval. It applies whether embeddings and indexes are persistent or created for a bounded session.

Tier 3 and Tier 4 capabilities require independent validation, strict unsupported-claim handling, source and citation authorization, enhanced isolation, tested quarantine and recovery, and risk-authorized degraded modes.

## Assumptions and prerequisites

- The capability, purpose, owners, users, affected parties, tier, and risk classification are approved.
- Source owners can authorize purpose, use, transformation, retrieval, retention, jurisdiction, and deletion.
- Enterprise identity and authorization attributes can be enforced at query time.
- Source classification, access, version, freshness, and deletion state can be represented in retrieval metadata.
- ARC-P100 or equivalent controls govern model access, provider boundaries, common identity, and shared evidence.
- Ingestion, index publication, query execution, and administrative responsibilities are assigned.
- Organization-defined thresholds exist for freshness, relevance, grounding, citations, unsupported claims, abstention, retention, and recovery.

## Prohibited uses

The pattern shall not be used to:

- retrieve broadly and filter unauthorized content after retrieval;
- use application-supplied tenant or source filters as the sole authorization mechanism;
- expose source existence, metadata, counts, scores, timing, embeddings, previews, or citations before authorization;
- strip source ACL, classification, owner, provenance, version, retention, or deletion metadata;
- insert retrieved content into authoritative instructions without explicit trust separation;
- allow query-time content, generated output, or feedback to publish directly into authoritative knowledge;
- allow a model or retrieved document to select unrestricted sources, filters, indexes, tools, or actions;
- silently fall back to ungrounded model generation when grounding is mandatory;
- represent grounding or citations as proof of correctness.

## Architecture views

### Dual-pipeline context view

```text
Knowledge-Supply Pipeline
Sources -> Admission/Quarantine -> Transform/Embed -> Index Publication -> Knowledge Stores

Query-Execution Pipeline
User/Workload -> Authorized Retrieval -> Context Assembly -> ARC-P100 Inference
              -> Grounding/Citations -> Response/Feedback/Evidence
```

The supply pipeline produces versioned knowledge releases. The query pipeline consumes authorized releases but cannot modify them. Feedback and generated output return through a separate reviewed path.

### Knowledge-supply view

| Stage | Primary outcome |
|---|---|
| Source admission | Approved owner, authority, purpose, license, classification, residency, retention, quality, integrity, and quarantine decision |
| Transformation | Versioned parsing, normalization, active-content handling, chunking, metadata preservation, and reproducible lineage |
| Embedding and index build | Approved components, tenant and security labels, integrity, quality evaluation, and immutable generation identity |
| Publication | Independent approval, atomic promotion, rollback, emergency quarantine, and evidence |
| Reconciliation | Freshness, ACL, source version, deletion, tenant, and index consistency monitoring |

### Query-execution view

| Stage | Primary outcome |
|---|---|
| Query admission | Bound human or workload identity, tenant, capability, purpose, session, and approved indexes |
| Retrieval | Authorization-enforced search, bounded scope and results, ranking, deduplication, and decision evidence |
| Context assembly | Trust separation, provenance, classification, sanitization, token budget, deterministic priority, and truncation handling |
| Inference | Authorized minimized context sent to an approved model and region through ARC-P100 |
| Grounding and citations | Claim support, source-version resolution, citation reauthorization, unsupported-claim treatment, and abstention |
| Feedback and evidence | Classified feedback, poisoning resistance, correlation, metrics, and independently reviewed reuse |

## Actors and identities

| Actor | Identity and authority expectations |
|---|---|
| Source owner | Named authority for source purpose, classification, access, retention, quality, and retirement |
| Ingestion service | Managed workload identity restricted to approved sources, staging, transformations, and publication inputs |
| Index publisher | Privileged identity separated from transformation, authorized to promote, roll back, and quarantine generations |
| Human user | Enterprise identity with tenant, role, purpose, session, and source entitlements |
| Calling application | Managed workload identity bound to a capability, owner, environment, and approved retrieval scope |
| Retriever or query orchestrator | Managed identity authorized for specific indexes, filters, limits, and evidence export |
| Embedding, reranking, and generation services | Approved endpoints and model identities with recorded versions, regions, and provider responsibilities |
| Citation resolver | Managed service identity that rechecks user authorization and resolves opaque source-version references |
| Administrator | Named privileged identity using approved change, publication, quarantine, rollback, and audit paths |
| Evidence consumer | Security, operations, risk, cost, or audit identity limited to necessary minimized evidence |

Delegated and workload identities shall remain attributable to the initiating user, capability, purpose, and tenant where applicable.

## Data and instruction flows

| Flow | Contents | Required properties |
|---|---|---|
| Source | Documents, records, metadata, ACLs, classification, owner, license, version, retention, deletion | Authenticated source, authorized purpose, integrity, quarantine, lineage |
| Transformation | Parsed content, chunks, extracted metadata, active-content findings, security labels | Versioned pipeline, deterministic lineage, no attribute loss |
| Embedding and index | Embeddings, sparse terms, index metadata, namespaces, ranking features, generation manifests | Classification-equivalent protection, isolation, integrity, reproducibility |
| Query | User input, identity, tenant, purpose, session, approved indexes, server-derived constraints | Authentication, authorization, schema, limits, injection resistance, correlation |
| Retrieval | Candidate and selected chunks, scores, source and security metadata, index generation | Authorization before exposure, bounded scope, evidence, no security-label loss |
| Context | System and developer instructions, user input, retrieved text, provenance, classification | Explicit authority, separation, sanitization, prioritization, token limits |
| Inference and response | Authorized context, model parameters, response, claim and citation metadata | ARC-P100 controls, minimized data, schema, output and grounding validation |
| Feedback | Ratings, corrections, reports, identities, response and source references | Classification, rate limits, moderation, lineage, no automatic publication |
| Evidence | Decisions, versions, denials, metrics, traces, alerts, administrative actions | Minimization, integrity, access, retention, correlation, delivery monitoring |

## Trust boundaries

| Crossing | Key requirements |
|---|---|
| Z0 or Z5 to Z3 supply pipeline | Authenticate and authorize source; scan, validate, classify, quarantine, hash, and preserve source identity and version |
| Z3 to Z4 embedding or reranking | Use approved model and version, minimize authorized content, protect transport, and record provider and lineage |
| Z3 to Z5 index publication | Preserve tenant and security labels, approve promotion, use atomic generation change, and support rollback |
| Z1 or Z2 to Z3 query admission | Bind trusted user or workload identity, tenant, capability, purpose, session, limits, and index scope |
| Z3 retrieval to Z5 knowledge | Enforce server-derived authorization inside retrieval before content or metadata exposure |
| Z5 to Z3 context assembly | Treat retrieved text as untrusted instructions; preserve provenance, authorization, classification, and version |
| Z3 to Z4 generation | Send only authorized minimized context through ARC-P100 and record model, prompt, index, and source versions |
| Z3 to Z1 response and citation | Validate output and claim support; reauthorize citation rendering and source opening |
| Z1 or Z3 to Z7 feedback and evidence | Minimize, classify, protect, rate-limit, correlate, and separate operational feedback from publication |
| Z7 to Z3 or Z5 administration | Require privileged access, separation of duties, approved change, alerting, and complete evidence |

## Components and responsibilities

| Component | Required responsibility |
|---|---|
| Source registry | Record owner, authority, purpose, classification, jurisdiction, retention, quality, version, and status |
| Admission and quarantine | Verify source, scan active content and malware, evaluate policy and quality, and prevent unapproved publication |
| Transformation pipeline | Apply versioned parsing, normalization, chunking, metadata preservation, and lineage |
| Embedding and index builder | Use approved components, preserve security labels, create generation manifests, and produce evaluation evidence |
| Knowledge store | Protect content, embeddings, indexes, metadata, namespaces, backups, integrity, freshness, deletion, and bulk access |
| Retrieval authorization | Derive trusted tenant, purpose, source, and document or chunk constraints and enforce them inside search |
| Retriever and reranker | Apply bounded query, ranking, diversity, deduplication, per-source limits, and quality evidence |
| Context assembler | Preserve authority, provenance, classification, token budgets, deterministic priority, and truncation behavior |
| Model boundary | Use ARC-P100 to authorize model, provider, region, context, limits, and evidence |
| Grounding and citation service | Verify material claim support, resolve exact source versions, reauthorize citations, and enforce unsupported-claim policy |
| Cache services | Reauthorize every hit, bind entries to security context and versions, apply bounded retention, and invalidate revoked knowledge |
| Feedback service | Classify, rate-limit, moderate, quarantine, and preserve lineage before approved reuse |
| Evaluation and observability | Measure quality, freshness, grounding, citations, unsupported claims, drift, leakage, abuse, latency, and cost |
| Operations and administration | Govern change, promotion, rollback, quarantine, rebuild, recovery, deletion, and retirement |

## Required controls

| Control group | Controls | Primary implementation and evidence owners |
|---|---|---|
| Data authority, quality, lineage, retrieval, and output | `DAT-100`, `DAT-110`, `DAT-120`, `DAT-130`, `DAT-150`, `DAT-160` | Data owner, Data Governance, knowledge owner, Data Engineering |
| Application threat, context, output, isolation, release, and abuse resistance | `APP-100`, `APP-110`, `APP-120`, `APP-130`, `APP-140`, `APP-150` | Solution or security architect, application engineering, capability owner |
| Retrieval identity and API | `IAM-120`, `API-110` | IAM, knowledge owner, API engineering, retrieval engineering |
| End-to-end model and RAG validation | `MOD-120` | Model validation lead, capability owner |
| Telemetry, detection, quality, alerting, and audit | `MON-100`, `MON-110`, `MON-120`, `MON-140`, `MON-150` | Observability owner, Security Operations, AI Operations, assurance |
| Service, change, incident, recovery, and capacity | `OPS-100`, `OPS-110`, `OPS-120`, `OPS-130`, `OPS-140` | Service owner, change authority, incident response, Platform Operations |
| Architecture governance, boundaries, failure, and responsibility | `ARC-100`, `ARC-110`, `ARC-130`, `ARC-140` | Solution Architecture, Enterprise Architecture |

Shared controls normally inherited through ARC-P100 or enterprise services include `API-100`, `IAM-100`, `IAM-110`, `IAM-130`, `IAM-140`, `IAM-150`, `MOD-100`, `MOD-110`, `MOD-130`, `ARC-120`, and `ARC-150`. The RAG owner retains responsibility to register and verify provenance for embedding and reranking models and to govern compatibility, version coupling, evaluation, release, and rollback across embeddings, index generations, retriever and reranker configuration, prompt templates, and generation models.

Conditional controls include `DAT-140` for personal data or rights; `API-120` for tools, plugins, or connectors; `API-130` for MCP or orchestration-based retrieval; `API-140` for external retrieval services; `API-150` for portability or concentration risk; `MOD-140` for protected enterprise-held model artifacts; `MON-130` when an agent controls retrieval or memory; and `MOD-150` plus `OPS-150` for retirement.

## Control points and overlays

| Control point | Required outcome | Primary enforcement and evidence owners |
|---|---|---|
| CP1 Source admission | Authenticate source and owner; authorize purpose, license, classification, residency, retention, quality, and integrity; quarantine before publication | Source owner and Data Governance |
| CP2 Transformation and index publication | Use versioned pipelines and models; preserve lineage and security labels; approve atomic publication and rollback | Data Engineering and change authority |
| CP3 Knowledge store | Protect indexes, embeddings, metadata, backups, tenant boundaries, integrity, freshness, deletion, and bulk access | Retrieval platform owner and data owner |
| CP4 Retrieval authorization | Bind identity, tenant, capability, purpose, session, and index; authorize inside retrieval before exposure; constrain scope and results | Knowledge owner, IAM, and retrieval engineering |
| CP5 Context assembly | Separate instruction authority; label provenance and trust; deduplicate, sanitize, prioritize, and constrain context | Application engineering |
| CP6 Inference boundary | Send only authorized minimized context through ARC-P100; bind model, prompt, index, source, and correlation versions | Platform or gateway owner and capability owner |
| CP7 Grounding and citation verification | Verify source identity, version, user authorization, citation resolution, and claim support; apply unsupported-claim policy | Capability owner and application engineering |
| CP8 Feedback and learning | Classify, rate-limit, moderate, and preserve feedback lineage; require independent review before reuse | Capability owner and Data Governance |
| CP9 Operations and administration | Protect source, pipeline, ACL, index, configuration, promotion, rollback, quarantine, rebuild, and evidence actions | Platform Operations, change authority, Security Operations |

Apply overlays for Tier 3 and Tier 4 risk, personal or regulated data, regional residency, public or user-provided sources, external managed retrieval, agent-controlled retrieval, and consequential downstream use.

## Architecture decisions and parameters

Required decisions include:

- centralized, federated, regional, sovereign, ephemeral, external, or combined retrieval;
- authoritative source systems and source-admission authority;
- security metadata contract and behavior for missing or stale attributes;
- physical and logical tenant, domain, index, cache, and backup separation;
- parser, chunking, embedding, retrieval, reranking, prompt, model, and index versions;
- source, chunk, result, and context limits and deterministic prioritization;
- retrieval relevance, evidence coverage, freshness, grounding, citation, unsupported-claim, and abstention thresholds;
- source, ACL, deletion, quarantine, feedback, and rebuild service levels;
- query, retrieval, context, response, citation, and evidence retention and sampling;
- degraded mode, fallback, safe state, recovery, rollback, and retirement.

Organization-defined parameters shall identify exact values, scope, owner, approval authority, monitoring, evaluation set, and change method.

## Failure modes and abuse cases

| Condition | Required treatment |
|---|---|
| Source validation failure | Quarantine and prevent publication; notify the source owner |
| Poisoned or malicious source | Revoke source or chunks, quarantine affected generation, investigate retrievals, rebuild, and preserve evidence |
| Missing or stale ACL metadata | Deny affected retrieval and alert; do not search broadly and filter later |
| Cross-tenant or cross-domain result | Block response, suspend affected partition or index, invoke incident response, and test related boundaries |
| Index unavailable | Use an approved degraded mode, normally abstention; prohibit model-only fallback where grounding is mandatory |
| Retrieval quality below threshold | Use bounded approved alternatives, then abstain or escalate |
| Citation resolution or authorization failure | Withhold or regenerate the affected claim, escalate, or abstain; label unsupported content only where the use case permits |
| Context saturation or truncation | Preserve instruction and evidence budgets, report truncation, and fail safely when material support is lost |
| Embedding, retriever, or model change | Evaluate compatibility, canary or shadow test, publish a new generation, and preserve rollback |
| Deletion propagation failure | Block affected content or index, alert, correct, retest, and record nonconformity |
| Cache retains revoked knowledge | Invalidate and isolate cache, block affected scope, investigate exposure, correct event propagation, and retest |
| Evidence delivery failure | Buffer within approved limits, alert, reconcile, and restrict operation where evidence is mandatory |
| Feedback abuse or poisoning | Rate-limit, quarantine, moderate, and prevent automatic publication or training use |
| Privileged administration compromise | Suspend publication and administration, preserve evidence, rotate access, verify integrity, and invoke incident response |

## Fallback recovery and retirement

Retrieval failure shall not silently change a grounded capability into ungrounded generation. Model-only output is prohibited when grounding or attribution is a mandatory safety, legal, contractual, or business requirement and is disabled by default for Tier 3 and Tier 4 material decisions unless specifically risk-authorized with equivalent safeguards.

Recovery shall support source and chunk quarantine, atomic index promotion and rollback, reproducible rebuild, ACL reconciliation, cache invalidation, deletion verification, backup and restore, component version rollback, evidence reconciliation, and controlled service reintroduction. Rollback shall not restore revoked access or deleted content.

Retirement shall remove source access, connectors, transformations, indexes, embeddings, caches, credentials, routes, configurations, backups according to retention, and administrative access; preserve required evidence; notify dependent capabilities; and verify provider deletion and exit obligations.

## Evidence and assessment

Required evidence includes:

- approved source, corpus, index, owner, authority, purpose, classification, jurisdiction, and retention inventory;
- source approvals, versions, hashes or integrity records, quarantine, and rejection decisions;
- source-to-transformation-to-chunk-to-embedding-to-index lineage and generation manifests;
- parser, chunking, embedding, retriever, reranker, prompt, model, index, cache, and configuration versions;
- ACL and classification synchronization, reconciliation, denial, and freshness reports;
- index promotion, rollback, quarantine, deletion, rebuild, backup, restore, and retirement records;
- sampled authorized and denied retrieval decisions with identity, tenant, purpose, index, source, and version correlation;
- tenant isolation, leakage, enumeration, poisoning, indirect-injection, cache, and authorization tests;
- golden-query and adversarial evaluation sets and results;
- retrieval relevance, coverage, freshness, grounding, citation, unsupported-claim, abstention, latency, cost, and drift metrics;
- minimized correlated query, retrieval, context, model, output, citation, feedback, policy, and administrative evidence;
- incident, quarantine, rebuild, recovery, deletion, degraded-mode, and retirement exercises;
- shared-responsibility and inherited-control matrix.

External service evidence also includes provider data-use, retention, training-use, residency, tenant-isolation, incident-notification, export, rebuild, migration, exit, and deletion assurance and tests.

Assessment shall include negative and failure-path testing for unauthorized cross-tenant and cross-domain retrieval, source existence and metadata leakage, missing or stale ACL denial, citation reauthorization, cache invalidation, source and index quarantine, deletion propagation through caches and backups, poisoned-source containment, index rebuild and rollback, instruction injection, fabricated citations, and approved degraded modes.

## Variants and alternatives

### Central enterprise index

Approved content is consolidated into one managed platform. This simplifies common operations but requires strong tenant and domain isolation, concentration-risk treatment, and strict prevention of security-attribute loss.

### Federated domain indexes

Domains retain ownership and expose standardized retrieval interfaces. This preserves autonomy and jurisdictional control but requires consistent metadata, authorization, evaluation, evidence, and failure semantics.

### Regional or sovereign RAG

Sources, embeddings, indexes, and inference remain within approved regions. Cross-region routing, evidence, operations, support, backup, and recovery require explicit authorization.

### Ephemeral retrieval

Authorized sources are retrieved or transformed for a bounded session without persistent embeddings. Source authorization, context separation, evidence, cache controls, and session deletion still apply.

### External managed retrieval

An external provider hosts embeddings, indexes, retrieval, or connectors. Shared responsibility, provider terms, tenant isolation, access propagation, portability, deletion, incident notification, and exit controls become mandatory.

## Anti-patterns

- One shared vector index with caller-supplied tenant filters as the only isolation.
- Broad similarity search followed by application-layer authorization or redaction.
- Private networking, vector-store possession, or similarity score treated as authorization.
- Source ACL, classification, provenance, owner, version, or deletion metadata stripped during transformation.
- Retrieved content mixed into authoritative instructions without explicit boundaries.
- Public content, user uploads, generated output, or feedback automatically published into production knowledge.
- A model or retrieved document allowed to choose unrestricted sources, filters, indexes, tools, or actions.
- Full queries, chunks, answers, and ACL metadata logged by default.
- Citations displayed without source-version resolution, claim support, and user reauthorization.
- Embeddings or caches reused indefinitely after deletion, access change, model change, or tenant offboarding.
- Silent fallback from governed RAG to ungrounded generation.
- Grounding represented as a guarantee of factual correctness.

## Related patterns

- `ARC-P100` supplies shared model access, provider governance, identity, policy, and evidence controls.
- `ARC-P110` uses ARC-P120 for governed enterprise knowledge in employee-facing assistance.
- `ARC-P130` adds agent-controlled retrieval, memory, planning, tools, and actions.
- `ARC-P140` defines enterprise-operated embedding, reranking, and generation model responsibilities.
- `ARC-P150` defines reusable retrieval and knowledge integration services.
- `ARC-P160` defines shared evaluation, monitoring, drift, and assurance services.

## Change history

| Pattern version | ESAF release | Date | Change |
|---|---|---|---|
| 0.1.0 | 0.4-alpha | 2026-07-12 | Initial draft |
