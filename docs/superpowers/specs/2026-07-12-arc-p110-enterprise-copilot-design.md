# ARC-P110 Enterprise Copilot Design Specification

**Status:** Approved design; pending written-spec review  
**Target:** ESAF-1200 ARC-P110 Draft pattern  
**Release:** 0.4-alpha  
**Date:** 2026-07-12

## 1. Purpose

ARC-P110 defines a vendor-neutral architecture pattern for a general-purpose enterprise copilot used by employees and approved contractors through enterprise-managed identities and channels.

The pattern governs the human-facing interaction boundary: identity, session, purpose, context, disclosure, source presentation, response handling, memory, connector use, confirmation, feedback, accessibility, records, evidence, and safe failure. Supporting patterns govern shared platform, retrieval, agency, and observability behavior.

## 2. Design decision

Use a **governed interaction shell with federated enforcement**.

The interaction shell provides a consistent enterprise contract across web, desktop, mobile, and embedded channels. Enforcement may be centralized, regional, application-adjacent, or channel-adjacent when policy authority, context, identity, evidence, and bypass protection remain explicit.

ARC-P110 composes with:

- ARC-P100 for approved model access, provider routing, and shared policy enforcement;
- ARC-P120 for authorization-aware retrieval, grounding, and citations;
- ARC-P130 for delegated execution and consequential actions;
- ARC-P160 for authoritative evidence, evaluation, monitoring, and assurance.

No supporting pattern may silently broaden the user's data access, authority, purpose, provider, retention, or action scope.

## 3. Scope and audience

The baseline supports managed workforce identities: employees and approved contractors using enterprise-managed accounts, devices or channels according to policy. Guests, partners using unmanaged identities, customers, and public users require a separately tailored trust boundary or another pattern.

Included capabilities are:

- conversational assistance and content generation;
- summarization, transformation, drafting, analysis, and translation;
- user-selected files and session context;
- governed enterprise knowledge and read-oriented connectors;
- source attribution, uncertainty presentation, and feedback;
- optional durable personalization or memory under separate governance;
- human-confirmed actions governed by ARC-P130.

The baseline does not authorize autonomous action, unrestricted enterprise search, covert employee monitoring, model training on enterprise interactions, customer-facing use, or persistent memory by default.

## 4. Intended outcomes

ARC-P110 shall enable:

- attributable use by managed workforce identities for approved purposes;
- clear disclosure of AI operation, limitations, sources, context, and consequential effects;
- session-scoped context and memory by default;
- user visibility and control over material context;
- authorization-aware retrieval and connectors that do not amplify access;
- explicit, action-specific confirmation before consequential effects;
- distinguishable generated, quoted, user-authored, and enterprise-record content;
- accessible interaction, correction, challenge, and feedback;
- privacy-tiered evidence and independent operational assurance;
- unambiguous degraded, failed, refused, partial, and unknown states.

## 5. Six-layer architecture

### 5.1 Experience layer

Provides approved channels, managed user interaction, accessibility, AI disclosure, context indicators, source and citation presentation, previews, confirmations, response status, feedback, challenge, correction, export, and session controls.

### 5.2 Session and context layer

Binds enterprise identity, tenant, role, approved purpose, device and channel state, policy version, conversation, selected files, connected sources, capability tier, context manifest, memory state, and expiry. It isolates sessions, users, tenants, and purposes.

### 5.3 Policy and orchestration layer

Performs admission, authorization, instruction assembly, model and provider routing, context limits, connector policy, content handling, output policy, rate and resource limits, action classification, fallback, and safe-stop decisions.

### 5.4 Knowledge and connector layer

Provides read-oriented access to approved enterprise and external sources under the user's current authority and purpose. It inherits ARC-P120 where retrieval is used and prevents leakage through results, snippets, metadata, embeddings, caches, indexes, counts, errors, or derived outputs.

### 5.5 Model and response layer

Invokes approved models and versions, preserves instruction and context boundaries, validates responses, distinguishes content origin, presents sources and uncertainty, and prevents unsafe or unauthorized consumption.

### 5.6 Evidence and operations layer

Provides privacy-tiered telemetry, authoritative interaction and confirmation evidence, evaluation, quality and safety monitoring, service management, capacity and cost analysis, incidents, records, continuity, recovery, and assurance through ARC-P160.

## 6. Identity, session, and purpose

Every session binds a managed workforce identity, tenant, approved purpose, capability and tier, identity assurance level, policy version, channel, and managed device or approved access posture. Caller-supplied identity and tenant fields are untrusted until validated at an enterprise trust boundary.

Session identifiers are opaque, unpredictable, scoped, time-bounded, and rotated after authentication or privilege change. Conversation history, files, retrievals, caches, exports, feedback, memory, and support tooling remain isolated by user, tenant, purpose, and environment. Channel transfer, device change, synchronization, or session resume revalidates identity, device posture, context, source authorization, and policy before restoring state. Live multi-user or link-based shared sessions are outside the baseline; shared artifacts create recipient-specific authorization and evidence boundaries.

Privilege elevation, impersonation, shared accounts, support access, and break-glass access use separate managed identities, approval, bounded duration and purpose, session recording where appropriate, and review. Privileged recording follows ARC-P160 capture modes, records privileged actions and necessary interface state with the least interaction content required, and uses separately authorized protected storage; it is not a general-purpose path for copying user content. Routine productivity sessions do not inherit privileged administrative authority.

The capability reauthenticates or requires step-up authentication for sensitive context, privilege changes, protected exports, durable-memory changes, and consequential actions according to risk. It reevaluates authorization during long sessions and after account, contractor, group, device, risk, source ACL, or policy changes. Stale group membership, silent impersonation, and shared-account ambiguity cannot establish authority.

## 7. Context transparency and instruction integrity

The capability maintains an integrity-protected, machine-readable context manifest containing selected files, retrieved sources, conversation state, connected applications, memory, inferred attributes, policy context, versions, classification, purpose, and expiry. The user can see and control a comprehensible representation of user-selectable material context supplied to the copilot. Mandatory legal, policy, safety, and security context may be presented at an appropriate abstraction but is not user-disableable. The interface identifies when context is added, changed, unavailable, stale, or excluded and makes the final material context available after consequential use.

Sensitive attributes are not inferred, added to transient context, or used to shape responses unless explicitly authorized, necessary for the approved purpose, classified, protected, disclosed where required, and subject to impact and rights review. Transient processing does not bypass the restrictions that apply to durable memory or workforce analytics.

Hidden context is limited to approved system, safety, and security instructions. Hidden instructions are inventoried, classified, versioned, integrity-protected, tested, attributable to an owner, and available to authorized assessment without disclosure that would weaken security.

The normative instruction classes are enterprise policy, platform instruction, capability instruction, user instruction, and untrusted content. Enterprise policy has highest authority; platform and capability instructions operate only within it; user instructions operate within approved capability authority; retrieved content, attachments, connector results, external material, and model-generated text are untrusted content unless an explicit governed transformation changes their class. Provider-specific instruction roles map to these classes. Untrusted content cannot redefine identity, policy, authority, confirmation, evidence, or precedence. Material instruction conflicts are rejected, isolated, or disclosed according to risk.

User context controls cannot disable mandatory security instructions, conceal required evidence, or weaken policy precedence. Material context changes after an action preview invalidate the confirmation.

## 8. Attachments and imported content

Attachments, pasted content, links, images, archives, code, office documents, imported conversations, and connector responses are untrusted.

Before use, the capability validates declared and actual type, size, nested archives, compression ratio, macros, scripts, active content, links, OCR content, embedded objects, metadata, classification, ownership, version, provenance, inspection result, data-loss policy, and approved purpose. Scanning, extraction, rendering, and preview occur in an isolated environment and never execute active content. Unsupported, encrypted, malformed, polyglot, or high-risk content is rejected or routed to an approved protected process.

Parsing and extraction services run with least privilege, bounded resources, restricted network access, and no implicit authority to follow embedded links, macros, instructions, credentials, or external references.

URL retrieval and browsing resist server-side request forgery, unsafe downloads, redirect manipulation, credential leakage, tracking, and unauthorized data egress. Tests cover archive bombs, malicious documents, hidden text, image-based injection, poisoned repositories, and externally hosted content.

## 9. Retrieval and connector authorization

Connectors are read-oriented by default. Retrieval and connector calls execute under delegated authority that is no broader than the current user's authority, approved purpose, tenant, source, operation, and session.

Authorization is enforced at the source or an equivalently authoritative boundary at query time. Indexes, embeddings, caches, previews, snippets, counts, citations, error messages, and model inference cannot reveal inaccessible content or resource existence.

Authorization is reevaluated when source ACLs, group membership, purpose, tenant, or session posture changes. Shared conversations, copied citations, and exported or published results create a new authorization boundary; the originating user's access does not transfer to recipients.

A final authoritative access decision occurs before displaying or exporting cached answers, citations, previews, snippets, retrieved content, or derived output. When current authorization cannot be established, protected material and existence signals are withheld and the capability enters an explicit insufficient-authorization or unavailable-source state.

Connector identity, scope, credentials, provider, endpoint, version, data use, retention, residency, administrative visibility, evidence, throttling, outage, backfill, deletion, portability, and exit are documented. Material evidence or authorization gaps prohibit the affected source, tier, or operation.

## 10. Source attribution and response integrity

The interface distinguishes:

- model-generated content;
- user-authored content;
- quoted or transformed source content;
- retrieved source summaries;
- connector data;
- confirmed actions and target-native results;
- approved enterprise records.

Citations bind claims to accessible source versions, locations, retrieval times, authorization context, and transformation lineage. User-facing citations reveal only authorization-safe source information; protected evidence retains the complete authorization decision context. The capability detects missing, fabricated, substituted, stale, inaccessible, contradictory, or unsupported citations and does not imply stronger support than the evidence provides.

Evaluation measures citation correctness, claim coverage, freshness, contradiction, and unsupported-claim rates separately. The presence or number of citations is not treated as proof of truth.

Output validation addresses sensitive-data exposure, unsafe content, unsupported claims, malformed citations, executable content, policy violations, and downstream format or command risks. Classification, data-loss, attribution, and executable-content controls apply at display, copy, download, share, email, export, and connector boundaries. Generated advice, drafts, code, formulas, commands, links, and files remain untrusted and are labeled so they cannot be mistaken for approved policy, completed work, or authoritative records. High-impact advice requires risk-appropriate grounding, limitations, independent validation, and human accountability; unsupported numeric confidence scores are not used as a substitute for evidence-based limitations and verification paths.

## 11. Memory and personalization

Context and memory are session-scoped by default. Session closure expires or disposes of context according to the approved record and retention policy.

Durable memory or personalization is optional, separately approved, and explicitly opted into by purpose; ambiguous conversation cannot create durable memory. It is purpose-bound, data-minimized, user-visible, and clearly distinguishable from session context and authoritative enterprise records. Each memory item records provenance, creation method, confidence, purpose, expiry, correction history, and governing policy. Users can inspect, correct, restrict, and delete durable memory where policy and law permit.

Durable memory is isolated by identity, tenant, purpose, environment, and capability. It has defined retention, residency, access, legal hold, correction, deletion, export, revocation, and retirement behavior across primary and derived stores. The copilot does not silently infer or retain sensitive attributes. Feedback does not automatically become memory or training data. Memory is excluded from model training, unrelated evaluation, advertising, or secondary use unless separately authorized and disclosed. Where deletion conflicts with legal hold or record duties, the user receives an accurate restriction or correction workflow rather than a false deletion promise.

The pattern tests memory poisoning, cross-user contamination, stale or conflicting memory, unauthorized inference, feedback loops, re-identification, support access, backup and restore, migration, and deletion propagation.

## 12. Action preview and confirmation

Read-oriented retrieval does not require per-request confirmation when it remains within approved authority and purpose. Any action that writes, sends, submits, publishes, approves, purchases, changes access, modifies a system of record, executes code, or causes another consequential effect requires ARC-P130.

Before execution, the copilot creates an integrity-protected action manifest containing actor, delegated identity, target, recipients, operation, exact data or protected integrity-bound references, material parameters, expected effect, risk, reversibility, cost where material, expiry, and idempotency key. It presents an accessible, human-readable semantic preview that explains material changes without unnecessarily exposing secrets, credentials, regulated fields, or large payloads and provides a safe inspection path where detail is required. Confirmation is explicit, informed, time-bounded, and cryptographically or transactionally bound to that exact manifest.

Material changes to target, scope, data, cost, authority, provider, operation, or expected effect invalidate prior confirmation and require a new preview and confirmation. Silence, continued conversation, prior confirmation, ambiguous language, preselected controls, interface timing, or confirmation fatigue do not constitute approval.

Bundled approval, coercive wording, hidden recipients, deceptive defaults, and confirmation before the final action is known are prohibited. Step-up authentication, separation of duties, or two-person approval applies when required by risk or source-system policy.

Execution records initiating identity, delegated identity, preview, confirmation, policy, target, request, target-native result, timestamps, and final state. The interface distinguishes success, failure, partial completion, rollback, and unknown outcome. Unknown outcomes block blind retry until target state is reconciled.

## 13. Human factors, accessibility, and deceptive interaction

The experience persistently discloses AI interaction and material changes in model, provider, grounding, memory, connector, or degraded state. It supports applicable accessibility requirements, keyboard navigation, screen readers, logical focus order, semantic labels, zoom and reflow, color-independent status, localization, understandable reading level, manageable cognitive load and timeouts, and equivalent access to disclosures, citations, context, previews, confirmations, errors, and feedback.

The interface shall not make deceptive claims of human identity, emotion, consciousness, authority, or relationship, or use fabricated certainty, hidden advertising, dark patterns, manufactured urgency, emotional manipulation, or misleading controls to induce disclosure, reliance, confirmation, or continued use.

Users can challenge outputs, report harm, correct context or memory, withdraw optional consent, and reach a human or authoritative process where required. Feedback collection is minimized, purpose-limited, disclosed, access-restricted, protected from retaliation, and separated from employee performance management. Sensitive content and attribution are handled according to policy. Feedback is validated for poisoning and quality before it enters evaluation or improvement datasets and does not silently change enterprise records, policy, memory, model behavior, training data, or user rights.

## 14. Records, privacy, and employee monitoring

Prompts, responses, files, context, retrievals, memory, feedback, exports, and telemetry are classified and purpose-bound. The interface provides required notices about processing, retention, human review, provider use, monitoring, and records status.

General interaction content is not collected into ordinary logs, tickets, alerts, analytics, or support tools by default. ARC-P160 capture modes and access controls apply. Content sampling, support access, investigations, quality review, and legal hold are approved, minimized, visible where required, attributable, and time-bounded.

ARC-P110 shall not be used for hidden employee surveillance, emotion inference, protected-trait inference, undisclosed performance scoring, or secondary employment decisions. Any separately approved workforce analytics require an explicit purpose, legal and employee-relations review, necessity and proportionality assessment, notice, access controls, contestability, and independent governance.

Business-record classification is determined by content, purpose, transaction, and obligation rather than by the fact that AI generated or transmitted the material. Records, exports, deletion, correction, legal hold, eDiscovery, and retirement apply consistently across source and derived stores.

For material decisions and actions, the record preserves an integrity-protected, minimized snapshot of relevant user input, context manifest, sources, model and policy versions, output, confirmation presentation, action manifest, and target-native outcome. Sharing, exporting, or publishing a conversation creates a new authorization, privacy, and records boundary. Obligations propagate through history, memory, feedback, caches, citations, tickets, backups, and derived data.

## 15. Failure and degraded modes

The copilot presents distinct states for no answer, insufficient evidence, incomplete or stale sources, policy refusal, unavailable model or connector, degraded functionality, partial completion, failed action, rollback, and unknown action outcome.

An approved capability matrix defines which functions remain available for each failure condition and capability tier, including permitted data, providers, sources, memory, connectors, actions, duration, evidence, and recovery authority.

It never represents a timeout, missing evidence, inferred target state, or uncertain transaction as success. Lower-risk conversational assistance may continue only under an approved, visible degraded mode with reduced data, sources, functions, and duration. Degraded mode cannot broaden provider, data, authority, retention, memory, connector, or action scope.

The capability never silently changes model, provider, region, grounding source, retention, memory behavior, or action capability. Material change invalidates stale context, evaluation assumptions, and action confirmations and requires renewed disclosure or confirmation as applicable.

Tier 3 and Tier 4 advisory use stops when identity, authorization, required grounding, integrity, or required assurance is unavailable. Consequential actions and workflows also stop when required confirmation or target-state evidence is unavailable. Recovery requires cause resolution, state reconciliation, evidence validation, renewed confirmation where context or parameters changed, affected-user notification where appropriate, and authorized return to normal service.

Authoritative evidence correlates the session, context manifest, source retrieval, active instruction and policy versions, model and provider version, output checks, citations, memory changes, feedback, confirmation interface actually presented, action manifest, target outcome, and degraded-state decision. Evidence records what the user was shown, not only what backend services intended to show. The runtime and ordinary administrators cannot selectively suppress, rewrite, or omit authoritative evidence.

## 16. Control points

| CP | Control point | Required outcome | Primary implementation and evidence roles |
|---|---|---|---|
| CP1 | Channel and managed-user admission | Only approved channels, identities, tenants, devices, purposes, and capability states enter a session | Application Owner; IAM and Channel Owner produce evidence |
| CP2 | Session, tenant, and purpose binding | All context and operations remain bound to validated identity, tenant, purpose, tier, policy, and expiry | Application Owner; IAM and Application Engineering |
| CP3 | User notice and AI disclosure | Users understand AI operation, material limitations, processing, records, and monitoring | Compliance; Product, UX, Legal, and Accessibility |
| CP4 | Context selection and minimization | Material context is visible, controllable, necessary, classified, and purpose-bound | Data Owner; Application Engineering and Privacy |
| CP5 | Attachment and imported-content inspection | Untrusted content is validated, isolated, bounded, and prevented from changing authority or policy | Application Owner; Security Engineering |
| CP6 | System-instruction and policy integrity | Hidden instructions and policy are owned, versioned, protected, tested, and precedence-enforced | Application Owner; Platform Engineering and Change Authority |
| CP7 | Retrieval and connector authorization | Read access remains within current user, source, tenant, purpose, and session authority | Technical Owner; IAM, Knowledge Owner, and API Owner |
| CP8 | Prompt-injection and instruction-conflict handling | Untrusted instructions cannot override identity, policy, authorization, confirmation, or evidence | Application Owner; Application Security and Retrieval Engineering |
| CP9 | Model and provider routing | Only approved models, providers, regions, versions, and processing conditions are selected | AI Platform Owner; Model Owner and Gateway Operations |
| CP10 | Output validation and sensitive-data protection | Unsafe, unauthorized, unsupported, or executable outputs are blocked, transformed, or disclosed | Application Owner; Privacy, DLP, and Application Engineering |
| CP11 | Citation, provenance, and uncertainty presentation | Claims, sources, transformations, freshness, limitations, and uncertainty are accurately represented | Data Governance and Business Owner; Application and Retrieval Engineering |
| CP12 | Memory and personalization governance | Durable state is optional, visible, purpose-bound, isolated, correctable, deletable, and lifecycle-governed | Data Owner; Privacy and Application Engineering |
| CP13 | Action preview, confirmation, and reauthorization | Consequential actions execute only after exact informed confirmation under ARC-P130 | Business Owner; Application Owner, Agent Owner when applicable, and UX |
| CP14 | Feedback, challenge, correction, and appeal | Users can contest outputs and correct state without creating uncontrolled secondary effects | Business Owner; Product Operations, Data Governance, and Compliance |
| CP15 | Records, export, retention, and deletion | Source and derived interaction records follow classification, rights, hold, and disposition rules | Compliance; Data Owner, Privacy, and Records Management |
| CP16 | Session termination and context disposal | Session context, delegated credentials, temporary files, caches, and authority expire or are retained only as approved | Application Owner; Application and Platform Engineering |
| CP17 | Evidence, evaluation, monitoring, and incident integration | Privacy-tiered authoritative evidence supports quality, security, operations, incidents, and assurance | AI Service Owner; Security Operations, Model Validation, Assurance, and Incident Response |
| CP18 | Degraded mode, safe stop, recovery, and retirement | Failure is explicit, authority never expands, consequential use stops safely, and recovery is verified | Business Continuity and Business Owner; AI Service Owner, SRE, and Assurance |

Catalog `owner_role` remains authoritative; these pattern roles assign implementation and evidence duties without transferring accountability.

## 17. Control alignment

Required controls are:

- Governance and risk: `GOV-130`, `RSK-110`, `RSK-120`, `RSK-130`, `RSK-140`; impact-assessment depth remains proportional to capability tier and deployment.
- Identity: `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-140`, `IAM-150`.
- Data and privacy: `DAT-100`, `DAT-110`, `DAT-120`, `DAT-130`, `DAT-140`, `DAT-160`.
- Application: `APP-100`, `APP-110`, `APP-120`, `APP-130`, `APP-140`, `APP-150`.
- API boundary and resource safeguards: `API-110`, `INF-150`.
- Model validation: `MOD-120`.
- Architecture: `ARC-100`, `ARC-110`, `ARC-130`, `ARC-140`.
- Operations and monitoring: `OPS-100`, `OPS-110`, `OPS-120`, `OPS-130`, `OPS-140`, `MON-100`, `MON-110`, `MON-120`, `MON-140`, `MON-150`.
- Assurance and compliance: `AUD-110`, `AUD-120`, `CMP-100`, `CMP-110`.
- Workforce: `EDU-100`, `EDU-120`.

`GOV-100`, `GOV-110`, `GOV-120`, `GOV-140`, `RSK-100`, `API-100`, `INF-100`, `INF-110`, `INF-120`, `INF-130`, `INF-140`, `MOD-100`, `MOD-110`, `MOD-130`, `MOD-140`, `DAT-150`, `ARC-120`, `ARC-150`, `AUD-100`, `AUD-130`, and `AUD-140` are normally inherited from enterprise governance, ARC-P100, ARC-P120, approved model services, the architecture lifecycle, and the assurance program and must be verified in the copilot context. ARC-P120 pattern obligations are inherited and verified for the baseline enterprise-knowledge capability.

Conditional controls include `API-120` for plugins or connectors; `API-130` for MCP or orchestration; `API-140` for external AI or connector services; `API-150` for portability or concentration risk; `AGT-100` through `AGT-160`, `MON-130`, and ARC-P130 pattern obligations for action or agent behavior; `CMP-120`, `CMP-130`, and `CMP-140` according to third parties, jurisdiction, residency, intellectual property, and licensing; `MOD-150` and `OPS-150` for retirement; `EDU-130` for developer copilots; `EDU-110` and `EDU-140` for specialized operators and governors; and `STR-110` for measured productivity or value claims.

Catalog `owner_role` remains accountable. Pattern roles identify implementation and evidence responsibility without transferring catalog accountability.

## 18. Evidence and assessment

Required evidence includes:

- approved audience, channels, purposes, capability tiers, models, providers, connectors, and sources;
- identity, session, purpose, context, instruction, retrieval, connector, model, response, memory, action, evidence, and records data-flow diagrams;
- session fixation, step-up authentication, continuous authorization, expiry, revocation, tenant isolation, shared-device, privileged search, impersonation, export, backup-restore, and support-access tests;
- machine-readable and user-presented context manifests, context-change invalidation, user controls, hidden-instruction inventory, policy history, precedence, and integrity tests;
- attachment scanning, actual-type validation, polyglot, archive-bomb, OCR and image injection, parser isolation, decompression, active-content, embedded-link, redirect, SSRF, unsafe-download, credential-leakage, data-egress, and resource-exhaustion tests;
- prompt-injection, indirect-injection, instruction-conflict, policy-bypass, and cross-context contamination tests;
- authorization-aware discovery, retrieval, generation, cache, citation, export, ACL-change, recipient-access, inaccessible-source inference, citation correctness, claim coverage, provenance, freshness, substitution, and contradiction tests;
- output safety at display, copy, download, share, email, export, and connector boundaries; sensitive-data, executable-content, downstream-consumption, labeling, and unsupported-claim tests;
- memory creation, visibility, correction, deletion, isolation, poisoning, retention, backup, migration, and retirement tests;
- action-manifest integrity, accessible semantic preview, step-up and dual approval, confirmation binding, changed-parameter reauthorization, idempotency, duplicate execution, partial completion, rollback, and unknown-outcome reconciliation tests;
- accessibility across keyboard, screen reader, focus, labels, zoom, color, localization, reading level, cognitive load, timeouts, and confirmation; comprehension, reliance, confirmation fatigue, deceptive-interface, feedback, challenge, and human-escalation tests;
- persistent notices, material-change disclosure, minimized decision snapshots, records, sharing, export, privacy rights, legal hold, eDiscovery, deletion, and employee-monitoring controls;
- provider and connector gap registers, approved degraded-capability matrix, failover disclosure, safe-stop tests, recovery and re-confirmation validation, and retirement evidence;
- ARC-P160 coverage correlating what the user was shown with context, sources, policy, model, citations, memory, confirmation, action, outcome, and degraded state; evaluation results, incidents, control-point evidence matrix, and independent assurance.

Negative testing includes cross-user, cross-session, cross-tenant, shared-device, and stale-group leakage; authorization revocation during a session; restricted-fact inference; malicious metadata, images, email signatures, code comments, files, URLs, and retrieved instructions; citation substitution and fabricated sources; memory and feedback poisoning; hidden, bundled, preselected, or ambiguous actions; inaccessible confirmations; time-of-check/time-of-use changes; duplicate and partial actions; target timeout with eventual completion and unknown outcomes; provider or connector failover that changes residency, retention, safety, or behavior; policy rollback; raw content copied into alerts or support systems; evidence loss; privileged export and silent impersonation; recipient access loss after sharing; and unsafe degraded continuation.

## 19. Variants

- **General productivity copilot:** broad drafting and analysis with limited enterprise context; prefer when no specialized domain or action authority is required.
- **Knowledge-grounded copilot:** composes ARC-P120 for enterprise sources; improves factual grounding but increases authorization, freshness, citation, and index-governance obligations.
- **Developer copilot:** handles code, repositories, build context, and executable outputs; requires stronger source, secret, license, dependency, sandbox, and software-assurance controls.
- **Role-specialized copilot:** adds domain vocabulary, data, workflows, and validation; appropriate where a bounded function can own risk and outcome criteria.
- **Embedded application copilot:** runs inside an enterprise application; improves context and workflow fit but requires explicit separation between host authority and copilot authority.
- **Offline or high-assurance enclave:** limits providers, connectors, and collaboration to protect sensitive work; trades convenience and freshness for isolation and control.
- **Accessibility-focused interaction mode:** provides equivalent multimodal access and support; never weakens disclosure, context visibility, confirmation, or privacy.

## 20. Anti-patterns

- Treating login as authorization to all enterprise information.
- Hiding material context, memory, providers, sources, or actions from the user.
- Persisting conversation content or personalization by default without separate governance.
- Using retrieved documents, attachments, links, or connector output as trusted instructions.
- Presenting model-generated citations or confidence as authoritative without validation.
- Allowing a copilot to write, send, submit, approve, purchase, or change access without exact confirmation.
- Treating silence, prior approval, continued conversation, or inaccessible controls as consent.
- Retrying an action with unknown outcome before reconciling target state.
- Copying prompts, responses, files, or sensitive context into general logs, tickets, or support tools.
- Using a copilot for hidden workforce monitoring or employment decisions.
- Allowing support, administrators, or providers to inspect user content without governed access and evidence.
- Continuing consequential assistance after authorization, grounding, confirmation, or assurance becomes unknown.
- Claiming productivity, quality, or safety benefit without defined measures and limitations.

## 21. Acceptance criteria

ARC-P110 is complete when:

- every architecture-template section is substantively populated;
- all six layers and eighteen control points are represented;
- managed-workforce scope, session-scoped default memory, read-oriented connectors, and exact action confirmation are explicit;
- identity, context, attachment, instruction, retrieval, source, output, memory, action, accessibility, privacy, records, evidence, and safe-failure requirements are testable;
- control accountability and evidence producers are assigned;
- all required, inherited, and conditional control IDs resolve;
- the pattern registry links ARC-P110 and changes its state to Draft;
- unit, architecture, control, PR, and post-merge validation pass.

## 22. Out of scope

This milestone does not select products, define a visual design system, configure specific productivity suites, set universal content-safety thresholds, authorize customer-facing use, establish industry-specific employment rules, create a general autonomous agent pattern, or claim external-standard compliance mappings.
