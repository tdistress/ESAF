# ESAF-1100 Control Objectives

**Status:** Working Draft

**Version:** 0.3-alpha

Control objectives define intended outcomes. They do not create independently assessable obligations until implemented through approved controls.

## GOV - Governance

- **GOV-01 Governance authority:** Establish accountable enterprise authority and decision rights for AI.
- **GOV-02 Policy:** Maintain approved, communicated, and enforced AI policy.
- **GOV-03 Portfolio oversight:** Govern AI capabilities, investment, risk, and lifecycle as a portfolio.
- **GOV-04 Accountability:** Assign owners, responsibilities, escalation, and separation of duties.
- **GOV-05 Exceptions:** Govern deviations, compensating measures, risk acceptance, and expiration.

## STR - Strategy

- **STR-01 Strategic alignment:** Align AI objectives and investments with organizational strategy.
- **STR-02 Value realization:** Define and measure intended value and outcomes.
- **STR-03 Responsible innovation:** Enable bounded experimentation and controlled scaling.
- **STR-04 Resource planning:** Plan funding, capacity, skills, platforms, and dependencies.

## RSK - Risk Management

- **RSK-01 Risk methodology:** Maintain a consistent AI risk-management method.
- **RSK-02 Risk classification:** Classify capabilities and select risk-proportionate governance.
- **RSK-03 Risk treatment:** Select, approve, implement, and monitor risk responses.
- **RSK-04 Impact assessment:** Evaluate effects on organizations, individuals, society, and the environment where relevant.
- **RSK-05 Change risk:** Reassess risk when material changes or triggers occur.

## IAM - Identity and Access Management

- **IAM-01 Identity governance:** Govern human, service, workload, API, and agent identities.
- **IAM-02 Authentication:** Verify identities using risk-appropriate mechanisms.
- **IAM-03 Authorization:** Enforce least privilege, separation of duties, and delegated authority.
- **IAM-04 Privileged access:** Control and monitor administrative and high-impact access.
- **IAM-05 Secrets:** Protect credentials, tokens, keys, and other authentication material.
- **IAM-06 Access review:** Periodically validate and revoke access.

## DAT - Data Protection and Governance

- **DAT-01 Data authority:** Establish ownership, lawful authority, purpose, and permitted use.
- **DAT-02 Classification and handling:** Apply protection according to sensitivity and obligation.
- **DAT-03 Quality and suitability:** Validate data quality, representativeness, relevance, and limitations.
- **DAT-04 Lineage and provenance:** Trace material data sources, transformations, and derived assets.
- **DAT-05 Privacy:** Apply minimization, rights, retention, and privacy safeguards.
- **DAT-06 Retrieval and embeddings:** Protect knowledge sources, vector stores, embeddings, and authorization context.
- **DAT-07 Output and feedback:** Govern generated content, feedback, labels, and downstream use.

## MOD - Model Security and Management

- **MOD-01 Model governance:** Assign ownership, purpose, approval, status, and lifecycle.
- **MOD-02 Provenance and supply chain:** Establish origin, licensing, dependencies, and integrity.
- **MOD-03 Validation:** Evaluate performance, safety, security, fairness, robustness, and limitations.
- **MOD-04 Change and version control:** Control updates, fine-tuning, configuration, release, and rollback.
- **MOD-05 Protection:** Protect models from unauthorized access, extraction, replacement, or modification.
- **MOD-06 Retirement:** Safely withdraw models and preserve required records.

## APP - AI Application Security

- **APP-01 Secure design:** Integrate threat modeling and secure design through the lifecycle.
- **APP-02 Input and context protection:** Validate and separate instructions, content, context, and untrusted input.
- **APP-03 Output handling:** Validate, constrain, label, and safely consume AI output.
- **APP-04 Session and state isolation:** Protect user, tenant, conversation, and memory boundaries.
- **APP-05 Software assurance:** Secure code, dependencies, testing, deployment, and AI-generated artifacts.
- **APP-06 Abuse resistance:** Detect and mitigate misuse, adversarial behavior, and resource exhaustion.

## API - AI Platforms and Integrations

- **API-01 AI gateway:** Centralize policy enforcement, routing, inspection, and accountability where appropriate.
- **API-02 API security:** Authenticate, authorize, validate, limit, and monitor interfaces.
- **API-03 Tools and plugins:** Govern tool registration, permissions, input, output, and change.
- **API-04 MCP and orchestration:** Secure protocol servers, clients, context exchange, and orchestration.
- **API-05 External services:** Control data exchange, dependencies, failures, and supplier boundaries.
- **API-06 Interoperability:** Use controlled, documented, and replaceable integration patterns.

## INF - Infrastructure Security

- **INF-01 Approved hosting:** Operate workloads only in authorized and classified environments.
- **INF-02 Hardening:** Secure compute, accelerators, containers, orchestration, storage, and networks.
- **INF-03 Vulnerability management:** Identify, prioritize, remediate, and accept infrastructure risk.
- **INF-04 Configuration and change:** Manage infrastructure through controlled, reproducible configuration.
- **INF-05 Cryptographic protection:** Protect data and administrative paths in transit and at rest.
- **INF-06 Capacity and resource safeguards:** Prevent exhaustion, abuse, and uncontrolled consumption.

## AGT - Autonomous and Agentic AI

- **AGT-01 Agent accountability:** Assign identity, owner, purpose, authority, and lifecycle state.
- **AGT-02 Permission boundaries:** Constrain tools, data, actions, resources, and delegation.
- **AGT-03 Human oversight:** Establish approval, supervision, intervention, and appeal appropriate to risk.
- **AGT-04 Memory and state:** Protect, limit, validate, retain, and delete agent memory and state.
- **AGT-05 Action traceability:** Record plans, tool calls, approvals, outcomes, and material decisions.
- **AGT-06 Intervention and recovery:** Provide tested suspension, containment, rollback, and recovery.
- **AGT-07 Multi-agent control:** Govern delegation, identity propagation, communication, and emergent behavior.

## OPS - Operations and Resilience

- **OPS-01 Service ownership:** Define service objectives, support, accountability, and operating boundaries.
- **OPS-02 Change and release:** Authorize, test, deploy, and reverse changes.
- **OPS-03 Incident management:** Prepare for, detect, respond to, recover from, and learn from AI incidents.
- **OPS-04 Continuity and recovery:** Maintain fallback, safe-state, recovery, and dependency plans.
- **OPS-05 Capacity and performance:** Manage availability, latency, quality, cost, and demand.
- **OPS-06 Retirement:** Decommission capabilities, access, data, integrations, and contracts safely.

## MON - Monitoring and Detection

- **MON-01 Telemetry:** Collect attributable, protected, and sufficient AI telemetry.
- **MON-02 Security detection:** Detect threats, misuse, unauthorized change, and policy violations.
- **MON-03 Behavior and drift:** Monitor performance, quality, drift, unsafe behavior, and emerging limitations.
- **MON-04 Agent monitoring:** Observe actions, tools, permissions, resource use, and anomalies.
- **MON-05 Alert response:** Define thresholds, ownership, triage, escalation, and tuning.
- **MON-06 Audit trails:** Preserve evidence for investigation, assurance, and accountability.

## CMP - Compliance and Obligations

- **CMP-01 Obligation management:** Identify, interpret, assign, and monitor applicable obligations.
- **CMP-02 Records and reporting:** Maintain required evidence, notices, disclosures, and reports.
- **CMP-03 Third-party compliance:** Establish contractual, assurance, notification, and exit requirements.
- **CMP-04 Jurisdiction and residency:** Govern geographic scope, transfers, localization, and applicable law.
- **CMP-05 Intellectual property:** Govern licensing, ownership, attribution, and protected content.

## AUD - Audit and Assurance

- **AUD-01 Assessment program:** Plan risk-based control and capability assessments.
- **AUD-02 Assessor competence and independence:** Ensure credible and objective evaluation.
- **AUD-03 Evidence:** Obtain relevant, reliable, complete, timely, and traceable evidence.
- **AUD-04 Findings and remediation:** Classify, assign, correct, and verify deficiencies.
- **AUD-05 Management review:** Provide leadership with assurance and improvement decisions.

## EDU - Workforce and Competency

- **EDU-01 AI literacy:** Establish baseline awareness for the workforce.
- **EDU-02 Role competence:** Define and maintain competency for specialized roles.
- **EDU-03 Acceptable use:** Educate users on approved tools, data, verification, and escalation.
- **EDU-04 Secure development:** Train personnel who design, build, test, and operate AI.
- **EDU-05 Governance education:** Prepare executives, owners, reviewers, and assessors for their duties.

## ARC - Architecture

- **ARC-01 Architecture governance:** Approve patterns, standards, exceptions, and decisions.
- **ARC-02 Trust boundaries and data flows:** Document components, actors, flows, and boundaries.
- **ARC-03 Reference patterns:** Establish reusable patterns for common AI architectures.
- **ARC-04 Resilience and failure design:** Design fallback, isolation, reversibility, and safe states.
- **ARC-05 Shared responsibility:** Define inherited controls and provider-consumer boundaries.
- **ARC-06 Technical lifecycle:** Manage technology approval, currency, debt, and retirement.
