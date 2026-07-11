# ESAF Logical Trust Zones

## 1. Purpose

Trust zones provide a common vocabulary for documenting changes in identity, authority, data handling, control, and responsibility. They are logical security and governance contexts, not prescribed network segments.

## 2. Zone model

| Zone | Name | Purpose | Typical contents |
|---|---|---|---|
| Z0 | External and untrusted | Represent sources and actors outside enterprise control | Public users, internet content, external prompts, open data |
| Z1 | User and channel | Support human or system interaction | Browser, client, IDE, application, API consumer |
| Z2 | Enterprise policy and integration | Centralize identity, routing, inspection, and policy | AI gateway, API gateway, DLP, policy engine, integration boundary |
| Z3 | AI application and orchestration | Execute capability-specific workflow and state | RAG service, agent orchestrator, prompt assembly, session state |
| Z4 | Model and inference | Execute and manage models | Hosted model API, inference cluster, model router, safety service |
| Z5 | Enterprise data and knowledge | Provide authorized enterprise information | Databases, document stores, vector stores, knowledge services |
| Z6 | Tools and action targets | Receive AI-initiated or AI-assisted actions | Business APIs, SaaS, code repositories, ticketing, operational systems |
| Z7 | Security, operations, and assurance | Operate, secure, recover, and assess capabilities | SIEM, observability, registry, vault, CI/CD, backup, evidence store |

## 3. Mapping rules

Every material component shall be mapped to at least one logical zone. A component may participate in multiple zones only when its responsibilities, interfaces, data, identities, and inherited controls remain explicit.

Zone placement shall consider administrative authority, provider control, data handling, execution context, exposure, and operational responsibility. Physical co-location does not eliminate a logical boundary.

## 4. Boundary-crossing record

For each material crossing, the architecture shall record:

| Element | Required description |
|---|---|
| Direction and purpose | Initiator, receiver, business purpose, and permitted direction |
| Identity | Human and non-human identities, authentication, delegation, and impersonation |
| Authorization | Requested operation, scope, least privilege, and policy decision point |
| Information | Data, instructions, context, classifications, provenance, and residency |
| Validation | Input, output, schema, content, instruction, and integrity checks |
| Protection | Encryption, secrets, session, tenant, and state safeguards |
| Evidence | Event source, correlation, decision, outcome, retention, and access |
| Reliability | Timeout, retry, idempotency, rate, capacity, and failure behavior |
| Responsibility | Provider, consumer, subprocessor, and inherited-control boundaries |

## 5. Common boundary risks

Reviews shall consider confused-deputy behavior, instruction injection, unauthorized retrieval, cross-tenant disclosure, credential propagation, excessive agency, replay, duplicate action, policy bypass, untrusted output consumption, provider failover, telemetry leakage, and loss of attribution.

## 6. External providers

Use of an enterprise contract does not place an external service inside an enterprise trust zone. Designs shall preserve the provider boundary and document data use, retention, training use, subprocessors, support access, notification, assurance, continuity, portability, and exit responsibilities.

## 7. Administrative and evidence paths

Administrative interfaces and evidence pipelines shall be represented separately from ordinary user flows when they confer elevated authority or expose sensitive telemetry. Access to Z7 services shall not create an unmonitored path into other zones.
