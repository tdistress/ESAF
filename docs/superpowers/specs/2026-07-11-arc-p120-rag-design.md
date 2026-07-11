# ARC-P120 Retrieval-Augmented Generation Design

**Status:** Approved

**Target release:** 0.4-alpha

**Design date:** 2026-07-11

## 1. Purpose

ARC-P120 defines a vendor-neutral architecture pattern for grounding AI responses in governed knowledge while preserving source authorization, lineage, classification, provenance, tenant isolation, instruction boundaries, citation integrity, operational evidence, and safe failure.

## 2. Decision

Use a dual-pipeline, federated knowledge architecture.

The knowledge-supply pipeline approves and prepares content for retrieval through source admission, quarantine, validation, transformation, chunking, embedding, and controlled index publication. The query-execution pipeline binds identity and purpose, authorizes retrieval, assembles bounded context, invokes an approved model, verifies grounding and citations, and produces evidence.

Domain, regional, or sensitivity-specific indexes may remain federated. Central governance defines metadata, authorization, lineage, evaluation, publication, evidence, and assurance requirements. Query-time content, model output, and user feedback cannot modify authoritative knowledge without an independently authorized publication path.

## 3. Objectives

The pattern shall:

- authorize sources, purposes, owners, licenses, classifications, jurisdictions, and retention before indexing;
- preserve source-to-chunk-to-embedding-to-index lineage and source security attributes;
- enforce identity, tenant, purpose, and source authorization before or during retrieval;
- isolate tenants, domains, indexes, sessions, caches, and retrieval results;
- treat retrieved content as untrusted data rather than authoritative instructions;
- constrain context size, ordering, deduplication, provenance, and instruction authority;
- invoke models through approved ARC-P100 provider and gateway boundaries;
- verify citation resolution, authorization, source version, and support for material claims;
- distinguish sourced, inferred, and unsupported content and abstain when thresholds are not met;
- govern feedback separately from source and index publication;
- detect poisoning, leakage, enumeration, drift, freshness, quality, and authorization failures;
- support quarantine, atomic publication, rollback, reproducible rebuild, deletion, and retirement.

## 4. Non-goals

ARC-P120 does not:

- establish that retrieved information is true or complete;
- guarantee factual output merely because a source was retrieved;
- define model-provider routing already addressed by ARC-P100;
- define agent tool use or consequential action;
- prescribe vector databases, embedding models, rerankers, chunking algorithms, or evaluation products;
- permit broad retrieval followed by post-generation redaction as an authorization model;
- treat citations as valid unless the exact source and version are resolvable and authorized.

## 5. Architecture model

### 5.1 Knowledge-supply pipeline

```text
Sources
  -> Admission and Quarantine
  -> Validation and Classification
  -> Transformation and Chunking
  -> Embedding and Index Build
  -> Controlled Publication
  -> Governed Knowledge Store
```

Supply-pipeline releases are versioned and reproducible. Publication is separate from transformation and uses approved promotion, rollback, and emergency quarantine. Each chunk and embedding retains source identity, version, owner, classification, authorization attributes, transformation, retention, and deletion state.

### 5.2 Query-execution pipeline

```text
User or Workload
  -> Query Admission and Identity Binding
  -> Authorized Retrieval and Reranking
  -> Context Assembly and Instruction Separation
  -> Approved Model Inference through ARC-P100
  -> Grounding and Citation Verification
  -> Response, Feedback, and Evidence
```

Authorization occurs before or during retrieval using server-derived identity, tenant, purpose, and source constraints. The model cannot expand retrieval authority or select unrestricted indexes, filters, sources, tools, or downstream actions.

### 5.3 Governance and operations

Governance defines approved sources, indexes, embedding and retrieval components, metadata contracts, quality thresholds, authorization rules, publication authority, evaluation criteria, operating limits, and review triggers. Operations monitors both pipelines and can quarantine sources, chunks, index generations, models, or configurations.

## 6. Trust-zone mapping

| Zone | ARC-P120 use |
|---|---|
| Z0 | Public sources, external feeds, user uploads, and untrusted retrieved instructions |
| Z1 | Human users, enterprise applications, and workload query channels |
| Z2 | ARC-P100 admission, identity context, policy, provider routing, and common evidence |
| Z3 | RAG application, ingestion pipeline, retriever, reranker, context assembly, grounding, and feedback services |
| Z4 | Embedding, reranking, and generation model endpoints |
| Z5 | Authoritative sources, transformation stores, indexes, vector stores, metadata, and citation resolver |
| Z6 | Excluded unless a supporting agent or integration pattern authorizes tool or action use |
| Z7 | Registry, pipeline CI/CD, secrets, observability, security monitoring, evaluation, backup, evidence, and administration |

ARC-P120 focuses on Z0-Z3-Z5 supply crossings and Z1-Z2-Z3-Z5-Z4 query crossings.

## 7. Control points

| Control point | Required outcome | Primary enforcement and evidence owners |
|---|---|---|
| CP1 Source admission | Authenticate source and owner; authorize purpose, license, classification, residency, retention, and quality; scan and quarantine before publication | Source owner and Data Governance |
| CP2 Transformation and index publication | Use versioned pipelines and components; preserve lineage and security labels; approve atomic publication and rollback | Data Engineering and change authority |
| CP3 Knowledge store | Protect indexes, embeddings, metadata, backups, tenant boundaries, integrity, freshness, deletion, and bulk access | Retrieval platform owner and data owner |
| CP4 Retrieval authorization | Bind identity, tenant, capability, purpose, session, and index; enforce document or chunk authorization inside the retrieval operation before protected information is exposed; constrain query scope and result count | Knowledge owner, IAM, and retrieval engineering |
| CP5 Context assembly | Separate instruction authority; label provenance and trust; deduplicate, sanitize, prioritize, and constrain context | Application engineering |
| CP6 Inference boundary | Send only authorized minimized context through ARC-P100; bind model, prompt-template, index, source, and correlation versions | Platform or gateway owner and capability owner |
| CP7 Grounding and citation verification | Verify source identity, version, user authorization, citation resolution, and claim support; apply approved unsupported-claim treatment | Capability owner and application engineering |
| CP8 Feedback and learning | Classify, rate-limit, moderate, and preserve feedback lineage; require independent review before knowledge or training reuse | Capability owner and Data Governance |
| CP9 Operations and administration | Protect source, pipeline, ACL, index, configuration, promotion, rollback, quarantine, rebuild, and evidence actions | Platform Operations, change authority, and Security Operations |

## 8. Authorization model

Retrieval authorization uses trusted server-derived constraints. It shall be enforced within the retrieval operation before unauthorized content, metadata, source existence, result counts, similarity scores, timing distinctions, or embeddings are exposed to the caller, orchestrator, or model. Broad similarity search followed by application-layer filtering is not authorized retrieval. Application-supplied tenant or source filters cannot be the sole authorization control. Missing, ambiguous, stale, or conflicting authorization metadata results in denial or an explicitly approved safe response.

The pattern supports physical index separation, logical namespaces, attribute-based filtering, document-level enforcement, chunk-level enforcement, or combinations. The selected method shall demonstrate equivalent protection for unauthorized similarity search, metadata exposure, result counts, citation previews, bulk extraction, cache reuse, and cross-tenant nearest-neighbor leakage.

Authorization is rechecked when rendering or opening citations. A citation visible to one user is not automatically visible to another user with access to the same generated response.

Query, retrieval-result, semantic, context, and citation caches shall enforce authorization on every hit and bind entries to tenant, identity or approved sharing scope, purpose, index generation, source version, and security attributes. Cache entries are invalidated upon access change, deletion, quarantine, tenant offboarding, index rollback, or other event that revokes their basis. Retention is bounded, and tests shall confirm that caches cannot resurrect revoked knowledge.

## 9. Instruction and context model

System and developer instructions, user input, retrieved content, metadata, tool output, memory, and feedback retain explicit authority and trust labels. Retrieved text remains untrusted even when the source is approved.

Context assembly shall:

- reserve protected capacity for authoritative instructions and evidence metadata;
- prevent retrieved content from redefining identity, policy, tools, routing, memory, or output handling;
- sanitize active content and constrain formats and size;
- preserve exact source, version, classification, and authorization references;
- apply deterministic prioritization, diversity, deduplication, and per-source limits;
- report truncation and abstain when required evidence is lost.

## 10. Grounding and citation model

Grounding measures whether material output claims are supported by authorized retrieved evidence. It does not prove that the source or claim is objectively true.

The pattern shall define organization-approved thresholds for retrieval relevance, evidence coverage, citation validity, source freshness, unsupported claims, and abstention. Citation verification shall resolve an opaque citation identifier to the exact source and version, confirm user authorization, and prevent disclosure through titles, previews, metadata, URLs, or access errors.

Responses distinguish sourced statements, model inference, uncertainty, and unsupported content according to use-case risk. Unsupported content may remain labeled only when the approved use case permits that treatment. Otherwise the affected claim is withheld, regenerated from authorized evidence, escalated for human review, or causes abstention. Tier 3 and Tier 4 material claims shall not remain solely because a failed citation was removed; those capabilities require independent evaluation and human-review or safe-abstention rules.

## 11. Index lifecycle

Index generations are immutable or otherwise integrity-verifiable releases. Publication records the source set, transformations, chunking configuration, embedding model and version, retrieval configuration, security metadata, quality results, approvers, and release identifier.

Source changes, access changes, deletion, tenant offboarding, embedding changes, and material pipeline changes trigger reconciliation or rebuild. Tombstones alone are insufficient unless testing confirms that deleted or restricted content cannot be retrieved, inferred through metadata, cited, cached, or restored through an unauthorized backup.

Emergency quarantine can remove a source, chunk set, tenant partition, or complete generation without waiting for a full rebuild. Rollback shall not reintroduce revoked authorization or deleted content.

## 12. Federated knowledge

Federation permits knowledge stores to remain under domain, region, or sensitivity ownership. The federation contract shall standardize:

- source and owner identity;
- classification and authorization attributes;
- lineage and version identifiers;
- query and filter schemas;
- citation resolution;
- freshness and deletion status;
- quality and availability indicators;
- evidence and incident interfaces.

The query orchestrator routes only to authorized indexes and shall not reveal the existence, size, labels, or result counts of unauthorized domains. Cross-domain ranking and deduplication preserve source authority and do not erase access decisions.

## 13. Variants

### Central enterprise index

Approved content is consolidated into one managed platform. This simplifies common operations but requires strong tenant and domain isolation, concentration-risk treatment, and strict prevention of security-attribute loss.

### Federated domain indexes

Domains retain knowledge ownership and expose standardized retrieval interfaces. This preserves autonomy and jurisdictional control but requires consistent metadata, authorization, evaluation, evidence, and failure semantics.

### Regional or sovereign RAG

Sources, embeddings, indexes, and inference remain within approved regions. Cross-region routing, evidence, operations, support, backup, and recovery require explicit authorization.

### Ephemeral retrieval

Authorized sources are retrieved or transformed for a bounded session without persistent embeddings. This reduces index retention but still requires source authorization, context separation, evidence, and session deletion.

### External managed retrieval

An external provider hosts embeddings, indexes, retrieval, or knowledge connectors. Shared responsibility, provider data terms, tenant isolation, access propagation, portability, deletion, incident notification, and exit controls become mandatory.

## 14. Failure behavior

| Failure | Required treatment |
|---|---|
| Source validation failure | Quarantine and prevent publication; notify the accountable source owner |
| Poisoned or malicious source | Revoke source or chunks, quarantine affected generation, investigate retrievals, rebuild, and preserve evidence |
| Missing or stale ACL metadata | Deny retrieval for affected content and alert; do not retrieve broadly and redact later |
| Cross-tenant result | Block response, suspend affected partition or index, invoke incident response, and test related tenants |
| Index unavailable | Use an explicitly approved degraded mode, normally abstention; model-only generation is prohibited where grounding or attribution is mandatory and is disabled by default for Tier 3 or Tier 4 material decisions unless specifically risk-authorized with equivalent safeguards |
| Retrieval quality below threshold | Retry only within bounded approved alternatives; otherwise abstain or escalate |
| Citation resolution failure | Remove unsupported citation, label the claim unsupported, or abstain according to policy |
| Context saturation or truncation | Preserve instruction and evidence budgets; report truncation and fail safely when material support is lost |
| Embedding or retriever change | Evaluate compatibility, canary or shadow test, publish a new generation, and preserve rollback |
| Deletion propagation failure | Block affected content or index, alert, correct, retest, and record nonconformity |
| Evidence delivery failure | Buffer within approved bounds, alert, reconcile, and restrict operation where evidence is mandatory |
| Feedback abuse or poisoning | Rate-limit, quarantine, moderate, and prevent automatic publication or training use |

## 15. Threat and abuse focus

The pattern addresses source poisoning, indirect prompt injection, unauthorized retrieval, ACL drift, cross-tenant leakage, metadata and filter injection, embedding inversion, membership inference, bulk extraction, ranking manipulation, duplicate amplification, stale knowledge, orphaned embeddings, context saturation, fabricated citations, citation authorization leaks, provider changes, telemetry leakage, feedback poisoning, and privileged administration abuse.

## 16. Anti-patterns

- One shared vector index with caller-supplied tenant filters as the only isolation.
- Retrieve broadly and redact unauthorized chunks after retrieval.
- Treat private networking, vector-store possession, or similarity score as authorization.
- Strip source ACL, classification, provenance, owner, version, or deletion metadata during transformation.
- Mix retrieved content into authoritative instructions without explicit boundaries.
- Automatically ingest public content, user uploads, generated output, or feedback into production knowledge.
- Let the model or retrieved document select unrestricted sources, filters, indexes, tools, or actions.
- Log complete queries, chunks, and answers by default.
- Display citations without verifying source version, support, and user authorization.
- Reuse embeddings indefinitely after deletion, access change, embedding change, or tenant offboarding.
- Silently fall back from governed RAG to ungrounded model generation.
- Represent grounding as a guarantee of factual correctness.

## 17. Required controls

Core RAG controls are:

| Control group | Controls | Primary implementation and evidence owners |
|---|---|---|
| Data authority, quality, lineage, retrieval, and output | `DAT-100`, `DAT-110`, `DAT-120`, `DAT-130`, `DAT-150`, `DAT-160` | Data owner, Data Governance, knowledge owner, and Data Engineering |
| Application threat, context, output, isolation, release, and abuse resistance | `APP-100`, `APP-110`, `APP-120`, `APP-130`, `APP-140`, `APP-150` | Solution or security architect, application engineering, and capability owner |
| Retrieval identity and API | `IAM-120`, `API-110` | IAM, knowledge owner, API engineering, and retrieval engineering |
| End-to-end model and RAG validation | `MOD-120` | Model validation lead and capability owner |
| Telemetry, detection, quality, alerting, and audit | `MON-100`, `MON-110`, `MON-120`, `MON-140`, `MON-150` | Observability owner, Security Operations, AI Operations, and assurance |
| Service, change, incident, recovery, and capacity | `OPS-100`, `OPS-110`, `OPS-120`, `OPS-130`, `OPS-140` | Service owner, change authority, incident response, and Platform Operations |
| Architecture governance, boundaries, failure, and responsibility | `ARC-100`, `ARC-110`, `ARC-130`, `ARC-140` | Solution Architecture and Enterprise Architecture |

Shared controls normally inherited through ARC-P100 or enterprise services include `API-100`, `IAM-100`, `IAM-110`, `IAM-130`, `IAM-140`, `IAM-150`, `MOD-100`, `MOD-110`, `MOD-130`, `ARC-120`, and `ARC-150`. The implementation records provider, configuration, verification, limitations, and evidence for each inherited outcome. The RAG owner retains responsibility to register and verify provenance for material embedding and reranking models and to govern compatibility, version coupling, evaluation, release, and rollback across embeddings, index generations, retriever and reranker configuration, prompt templates, and generation models.

Conditional controls include:

- `DAT-140` for personal data, profiling, rights, or cross-border processing;
- `API-120` for tool, plugin, or connector invocation;
- `API-130` for MCP or orchestration-based retrieval;
- `API-140` for external embedding, vector, reranking, model, or knowledge services;
- `API-150` for material portability, concentration, or continuity risk;
- `MOD-140` for protected enterprise-held model artifacts or endpoints;
- `MON-130` when an agent controls retrieval, memory, planning, or tools;
- `MOD-150` and `OPS-150` for retirement.

## 18. Evidence model

Required evidence includes:

- approved source, corpus, index, owner, authority, purpose, classification, jurisdiction, and retention inventory;
- source approvals, versions, integrity records, and quarantine decisions;
- source-to-transformation-to-chunk-to-embedding-to-index lineage;
- pipeline, parser, chunking, embedding, retriever, reranker, prompt, model, index, and configuration versions;
- ACL and classification synchronization, reconciliation, and denial records;
- index promotion, rollback, quarantine, deletion, rebuild, backup, and restore records;
- sampled authorized and denied retrieval decisions;
- tenant isolation, leakage, enumeration, poisoning, and indirect-injection tests;
- golden-query and adversarial evaluation sets and results;
- retrieval relevance, coverage, freshness, grounding, citation, unsupported-claim, abstention, latency, cost, and drift metrics;
- minimized correlated query, retrieval, context, model, output, citation, feedback, and policy evidence;
- incident, quarantine, rebuild, recovery, deletion, and retirement exercises;
- shared-responsibility and inherited-control matrix.

When external retrieval, embedding, reranking, vector, model, or knowledge services are used, evidence also includes provider data-use, retention, training-use, residency, tenant-isolation, incident-notification, export, rebuild, migration, exit, and deletion assurance and test results.

Assessment shall include negative and failure-path testing for unauthorized cross-tenant and cross-domain retrieval, missing or stale ACL denial, citation reauthorization, cache invalidation, source and index quarantine, deletion propagation through caches and backups, poisoned-source containment, index rebuild and rollback, and the approved degraded mode.

## 19. Validation changes

The pattern-aware validator already enforces metadata, status, headings, registry linkage, local links, encoding, and control references. ARC-P120 implementation will add no speculative schema. Tests will prove that the registry transition and ARC-P120 control references are valid using the existing contract.

## 20. Acceptance criteria

ARC-P120 is complete when:

- every architecture-template section is substantively populated;
- knowledge-supply and query-execution pipelines are distinct;
- all nine control points and their owners are defined;
- retrieval authorization occurs before or during retrieval;
- context authority, grounding, citation, feedback, federation, lifecycle, failure, and anti-pattern rules are explicit;
- required, inherited, and conditional controls are mapped and resolve;
- evidence and assessment expectations are testable;
- the registry links ARC-P120 and changes its state to Draft;
- unit tests, architecture validation, control-catalog validation, PR CI, and post-merge CI pass.

## 21. Out of scope

This milestone does not include product configurations, infrastructure code, external-standard crosswalk claims, publication-quality graphics, benchmark datasets, quantitative universal grounding thresholds, agent tool-use design, or production implementation guidance.
