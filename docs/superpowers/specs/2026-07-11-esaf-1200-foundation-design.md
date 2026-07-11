# ESAF-1200 Reference Architecture Foundation Design

**Status:** Draft for review

**Milestone:** Phase 3 - Reference Architecture

**Target release:** 0.4-alpha

**Design date:** 2026-07-11

## 1. Purpose

This design defines the breadth-first foundation for ESAF-1200. The foundation establishes a consistent, vendor-neutral method for documenting, selecting, reviewing, implementing, and assessing enterprise AI architecture patterns before individual patterns are authored.

The milestone does not prescribe a single enterprise platform or publish fully implemented deployment patterns. It creates the common architecture contract that every later ESAF pattern must satisfy.

## 2. Design objectives

The foundation shall:

- define the authority, scope, audience, and relationship of ESAF-1200 to ESAF-1000 and ESAF-1100;
- establish architecture principles and a shared vocabulary;
- define reusable trust zones and boundary-crossing rules;
- establish mandatory views, metadata, decisions, control references, and evidence for each pattern;
- define a transparent method for selecting and tailoring patterns;
- distinguish normative architecture requirements from informative implementation guidance;
- remain vendor-neutral and deployment-model-neutral;
- support later automated validation without prematurely creating a complex architecture schema;
- provide a stable index for separately reviewable architecture-pattern PRs.

## 3. Considered approaches

### 3.1 Breadth-first architecture foundation

Define the method, pattern contract, trust zones, decision model, and common overlays before writing individual patterns.

**Advantages:** Consistent pattern structure, smaller reviews, stable terminology, reusable control overlays, and less rework.

**Trade-off:** Delays the first complete deployment pattern by one milestone.

### 3.2 Complete one pattern first

Author the enterprise AI gateway pattern and derive the general method from that implementation.

**Advantages:** Produces an immediately usable artifact and tests assumptions against a concrete case.

**Trade-off:** Gateway-specific assumptions could become accidental framework-wide conventions.

### 3.3 Draft the complete pattern library together

Author the foundation and all initial patterns in one release.

**Advantages:** Provides broad coverage quickly.

**Trade-off:** Creates an oversized review surface, weakens independent technical review, and makes structural corrections expensive.

### 3.4 Decision

Use the breadth-first architecture foundation. Draft each initial pattern in a later focused PR using the approved contract. Validate the contract against the first pattern and revise it only through an explicit architecture decision.

## 4. Publication architecture

The milestone will create the following authoritative files:

```text
architectures/
├── README.md
├── ESAF-1200.md
├── ARCHITECTURE_TEMPLATE.md
├── PRINCIPLES.md
├── TRUST_ZONES.md
├── PATTERN_SELECTION.md
├── overlays/
│   └── README.md
├── patterns/
│   └── README.md
└── decisions/
    ├── README.md
    └── ADR_TEMPLATE.md
```

Responsibilities are separated as follows:

- `ESAF-1200.md` defines the normative architecture method and conformance requirements.
- `PRINCIPLES.md` defines durable, testable architecture principles.
- `TRUST_ZONES.md` defines reusable zones, boundaries, actors, and crossing requirements.
- `PATTERN_SELECTION.md` defines how a capability selects and tailors one or more patterns.
- `ARCHITECTURE_TEMPLATE.md` defines the required pattern record.
- `overlays/README.md` defines how risk, deployment, and regulatory overlays modify a base pattern without duplicating it.
- `patterns/README.md` is the pattern registry and publication queue.
- `decisions/` records significant architecture decisions and their consequences.

Implementation examples, product configurations, and supplier-specific instructions remain outside ESAF-1200 and belong in ESAF-1400.

## 5. Architecture principles

The foundation will define the following principles:

1. **Identity-centered access:** Every actor and workload crossing a trust boundary is attributable and authorized.
2. **Explicit trust boundaries:** Components, data flows, control points, and responsibility changes are documented.
3. **Data authorization before processing:** Data classification, purpose, residency, and source authorization follow data into AI workflows.
4. **Least agency:** Systems receive only the tools, permissions, memory, time, and resources required for an approved purpose.
5. **Policy enforcement at boundaries:** Inspection and enforcement occur where identities, data, instructions, actions, or providers cross boundaries.
6. **Defense in depth:** No single gateway, filter, model, or provider is treated as a complete safeguard.
7. **Observable and attributable operation:** Material requests, decisions, retrievals, tool calls, changes, and failures produce protected evidence.
8. **Safe failure and reversibility:** Designs define fallback, isolation, suspension, rollback, recovery, and retirement behavior.
9. **Portable integration:** Interfaces and dependencies are documented so services can be governed, replaced, or exited.
10. **Human accountability:** Architecture preserves defined human decision rights, intervention mechanisms, and appeal paths.

Each principle will state its intent, required design consequence, and primary ESAF-1100 control families.

## 6. Trust-zone model

The common trust-zone model will use logical zones rather than assuming network topology:

| Zone | Purpose | Typical contents |
|---|---|---|
| Z0 External and untrusted | Sources or actors outside enterprise control | Public users, internet content, external prompts, open data |
| Z1 User and channel | Human or system interaction surfaces | Browser, client, IDE, application, API consumer |
| Z2 Enterprise policy and integration | Central identity, policy, routing, and inspection | AI gateway, API gateway, DLP, policy engine, orchestration boundary |
| Z3 AI application and orchestration | Capability-specific application logic and state | RAG service, agent orchestrator, prompt assembly, session state |
| Z4 Model and inference | Model execution and model-management services | Hosted model API, inference cluster, model router, safety service |
| Z5 Enterprise data and knowledge | Authorized enterprise information sources | Databases, document stores, vector stores, knowledge services |
| Z6 Tools and action targets | Systems on which AI may act | SaaS, business APIs, code repositories, ticketing, operational systems |
| Z7 Security, operations, and assurance | Evidence, monitoring, administration, and recovery | SIEM, observability, registry, vault, CI/CD, backup, assessment store |

Zones express different control and responsibility contexts; they do not imply that every design requires eight separate networks. A component may participate in more than one logical zone only when responsibilities and inherited controls remain explicit.

Every documented boundary crossing must identify:

- initiating and receiving identities;
- data and instruction classifications;
- authentication and authorization;
- validation and policy enforcement;
- encryption and secrets handling;
- logging and correlation;
- failure, retry, timeout, and rate behavior;
- provider and shared-responsibility changes.

## 7. Pattern contract

Every published reference pattern will use a common record containing:

1. Pattern ID, title, status, version, owner, and change history.
2. Purpose, problem statement, intended outcomes, and non-goals.
3. Applicability, assumptions, prerequisites, and prohibited uses.
4. Capability tiers, lifecycle stages, pillars, and deployment models.
5. Context, container, component, data-flow, and trust-boundary views where applicable.
6. Actors, identities, data classes, models, tools, dependencies, and responsibility boundaries.
7. Required control objectives and selected ESAF-1100 controls.
8. Required control points and security, privacy, resilience, and observability overlays.
9. Key architecture decisions and organization-defined parameters.
10. Failure modes, abuse cases, fallback, recovery, and retirement considerations.
11. Required governance artifacts, operational evidence, and assessment questions.
12. Variants, alternatives, anti-patterns, and related patterns.

The initial release uses a Markdown template rather than machine-readable front matter. Schema automation will be introduced only after at least two materially different patterns demonstrate that the metadata contract is stable.

## 8. Pattern identifiers and states

Architecture pattern identifiers will use `ARC-P###`, allocated in increments of ten. Initial reservations are:

| ID | Pattern |
|---|---|
| ARC-P100 | Enterprise AI platform and gateway |
| ARC-P110 | Enterprise copilot |
| ARC-P120 | Retrieval-augmented generation |
| ARC-P130 | Agentic and multi-agent AI |
| ARC-P140 | Private model deployment |
| ARC-P150 | AI integration services |
| ARC-P160 | AI observability |

Pattern states are `proposed`, `draft`, `approved`, `published`, `deprecated`, and `retired`. Published identifiers are never reassigned. Substantial alternatives use pattern variants rather than silently changing architectural meaning.

## 9. Pattern selection and tailoring

Selection begins with the approved AI use case, risk classification, capability tier, data classification, autonomy, external exposure, deployment model, and applicable obligations.

The selection method will:

1. identify one primary pattern;
2. identify supporting patterns, such as observability or integration services;
3. select applicable risk, deployment, and regulatory overlays;
4. record organization-defined parameters and deviations;
5. map required ESAF-1100 controls and inherited controls;
6. document unresolved gaps through an architecture decision or governed exception.

Conformance to a reference pattern does not establish conformance to ESAF-1000 or any external standard. It demonstrates that the design uses the specified pattern structure and accounts for its required decisions and controls.

## 10. Architecture decision records

An ADR is required when a team:

- chooses among materially different architecture variants;
- deviates from a required pattern element;
- accepts a provider-specific constraint that affects portability or responsibility;
- combines components across trust zones in a way not anticipated by the pattern;
- changes a material identity, data, model, tool, or observability boundary.

The ADR template will record context, decision, alternatives, consequences, controls affected, evidence, owner, status, and supersession.

## 11. Validation and quality gates

This milestone will be validated through deterministic repository checks rather than visual rendering. Validation shall confirm:

- all required foundation files exist;
- the pattern registry contains each reserved identifier exactly once;
- the template contains every required pattern-contract section;
- internal Markdown links resolve;
- referenced ESAF control families exist;
- no unresolved placeholder markers remain in normative content;
- text encoding and `git diff --check` are clean;
- the existing 91-control catalog validation remains successful.

A lightweight `tools/validate_architectures.py` check will enforce these structural rules without attempting to parse diagram semantics.

## 12. Error and ambiguity handling

- A missing architectural decision is reported as a pattern gap, not silently inferred.
- Conflicting patterns require an ADR that identifies the controlling decision.
- An unresolved control mapping blocks pattern approval but may remain explicit while the pattern is in `draft` state.
- Vendor examples must be labeled informative and cannot redefine the vendor-neutral pattern.
- Diagrams and prose must agree; prose is authoritative when rendering limitations create ambiguity.

## 13. Delivery sequence

The implementation will use one focused foundation PR containing:

1. ESAF-1200 normative foundation.
2. Architecture principles and trust-zone model.
3. Pattern template, registry, selection method, overlay method, and ADR template.
4. Structural validation and CI integration.
5. Version, roadmap, changelog, and decision-log updates for 0.4-alpha.

After foundation approval, individual pattern PRs will be delivered in this order:

1. ARC-P100 Enterprise AI platform and gateway.
2. ARC-P120 Retrieval-augmented generation.
3. ARC-P130 Agentic and multi-agent AI.
4. ARC-P160 AI observability.
5. ARC-P110 Enterprise copilot.
6. ARC-P140 Private model deployment.
7. ARC-P150 AI integration services.

The order establishes shared platform, data, agency, and evidence concepts before consumer-facing and specialized deployment patterns.

## 14. Acceptance criteria

The foundation milestone is complete when:

- every file in Section 4 exists and has an explicit responsibility;
- ESAF-1200 defines assessable architecture-method requirements without duplicating ESAF-1100 controls;
- all ten principles and all eight trust zones are defined consistently;
- the pattern template covers every item in Section 7;
- the registry reserves ARC-P100 through ARC-P160 as specified;
- selection, tailoring, overlays, ADRs, and conformance boundaries are documented;
- architecture validation and existing catalog validation pass in CI;
- release metadata records Phase 3 and version 0.4-alpha;
- the PR is merged to `main` with a clean working tree.

## 15. Out of scope

The foundation milestone does not include:

- completed deployment-pattern content;
- supplier-specific configurations or product recommendations;
- production infrastructure code;
- formal external-standard mappings;
- publication-quality graphical diagrams;
- assessment workbooks or certification claims;
- industry-specific architecture profiles.
