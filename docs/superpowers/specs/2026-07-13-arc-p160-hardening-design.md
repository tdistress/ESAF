# ARC-P160 AI Observability Hardening Design

**Status:** Pending written-spec review

**Target release:** 0.4-alpha

**Design date:** 2026-07-13

**Extends:** `docs/superpowers/specs/2026-07-12-arc-p160-observability-design.md`

## 1. Purpose

This milestone hardens the existing ARC-P160 AI observability Draft through focused semantic regression tests and renderer validation. It does not redesign or supersede the approved ARC-P160 architecture.

The hardening work shall detect drift in publication structure, control allocation, architecture semantics, assurance independence, sensitive-telemetry handling, tenant isolation, safe failure, and recovery. Narrowly scoped corrections are permitted only when a failing gate demonstrates a defect in the current pattern.

## 2. Context

ARC-P160 was designed and published as a substantive Draft before this milestone. The general architecture validator already checks repository-wide structure, registry linkage, metadata, local links, required headings, and control-reference resolution. It does not prove that ARC-P160 continues to express its deeper observability and assurance contract.

ARC-P150 established a useful model: a pattern-specific test module can protect exact allocations and durable normative concepts while the shared validator remains broadly reusable. ARC-P160 needs equivalent coverage plus explicit Mermaid rendering because fenced-block counting cannot detect parser failures.

## 3. Decision

Add a dedicated `tests/test_arc_p160_pattern.py` module and retain the existing shared architecture validator unchanged.

The focused suite shall protect six groups of invariants:

1. publication and metadata contract;
2. exact control allocation;
3. architecture structure and relationships;
4. evidence independence and privacy contract;
5. resilience, safe-stop, and recovery contract;
6. Mermaid source validity and a separate renderer publication gate.

Tests shall prefer durable semantic assertions over complete paragraph snapshots. Exact strings are appropriate only where wording represents a required normative invariant or an allocation that must not drift silently.

## 4. Scope

### 4.1 In scope

- Add the focused ARC-P160 regression module.
- Verify registry linkage, Draft status, required metadata, template heading order, and absence of drafting markers.
- Verify exact and disjoint required, inherited-and-verified, and conditional control sets against `controls/catalog.json`.
- Verify the six logical planes, four governed capture modes, CP1 through CP15, and the four numbered Mermaid figures.
- Verify ARC-P160 relationships to ARC-P100 through ARC-P150 and the ownership boundary between source-pattern semantics, authoritative evidence, target transaction truth, and business outcomes.
- Verify untrusted correlation identifiers, authoritative source binding, independent evidence administration, privacy-tiered capture, derived-signal treatment, tenant isolation, provider evidence gaps, governed evaluation, and non-authoritative dashboard semantics.
- Verify Tier 3 and Tier 4 safe-stop behavior, bounded lower-tier degraded operation, buffer exhaustion, backfill, reconciliation, integrity verification, gap disposition, and authorized recovery.
- Render every Mermaid block with the current Mermaid CLI.
- Correct narrowly scoped ARC-P160 defects exposed by these gates and retain regression coverage for each correction.

### 4.2 Out of scope

- New observability architecture features or a rewrite of ARC-P160.
- Vendor selection, product configuration, infrastructure code, or production dashboard design.
- Universal thresholds, retention schedules, or industry-specific requirements.
- External-standard crosswalks, industry profiles, or compliance claims.
- Changes to ARC-P100 through ARC-P150 except where a separately approved defect is proven.
- Promotion of ARC-P160 beyond Draft.

## 5. Test architecture

The focused test module shall use the pattern, registry, architecture template, and control catalog as its authoritative inputs.

### 5.1 Publication contract

Tests shall verify:

- the registry contains exactly one ARC-P160 row with the title AI observability, a link to `ARC-P160.md`, and Draft status;
- required metadata is populated and consistent with the filename and registry;
- level-two headings match the architecture template exactly, uniquely, and in order;
- no drafting markers remain; and
- figure headings are numbered consecutively.

### 5.2 Control-allocation contract

The required set shall contain exactly the 47 monitoring, governance, risk, assurance, operations, data, identity, compliance, platform, integration, architecture, application, and model controls allocated in the current pattern.

The inherited-and-verified set shall be exactly `ARC-120`, `ARC-150`, `OPS-150`, and `MOD-140`.

The conditional set shall contain exactly 17 controls: `MON-130`; `DAT-140` through `DAT-160`; `CMP-120` through `CMP-140`; `MOD-110`; `MOD-150`; `API-140`; and `AGT-100` through `AGT-160`.

The three sets shall be disjoint, their union shall contain exactly 68 of the catalog's 91 controls, and every allocated identifier shall resolve in the current catalog. For this milestone, the approved phrase "collectively match the catalog" means exact equality to ARC-P160's approved allocation plus catalog resolution; it does not mean assigning all catalog controls to ARC-P160. Classifying the other 23 controls merely to force catalog-wide equality would expand scope and create false applicability. Any ARC-P160 allocation change must produce a deliberate test failure and review decision rather than silent drift.

### 5.3 Architecture contract

Tests shall verify:

- exactly six named planes: governance and configuration; signal collection; protected evidence; evaluation and ground truth; detection and response; and analytics, service, and cost;
- exactly four capture modes: metadata only, derived signal, redacted excerpt, and exceptional protected full content;
- CP1 through CP15 appear once, in order, with explicit implementation and evidence responsibility;
- source patterns retain event semantics and enforcement responsibility;
- target systems remain authoritative for transaction state;
- capability owners remain accountable for business outcomes; and
- observability produces evidence without becoming an authorization source or transferring catalog accountability.

### 5.4 Requirement traceability

New tests shall protect approved or existing requirements; they shall not manufacture a document defect by asserting an unapproved clarification. The implementation plan shall trace each semantic test to the sources below.

| Invariant | Approved or existing source |
|---|---|
| Six planes, four capture modes, and CP1-CP15 | Approved 2026-07-12 design sections 4, 6, and 14; current pattern Architecture views, Data and instruction flows, and Control points and overlays |
| ARC-P100 through ARC-P150 evidence relationships | Current pattern Applicability and Related patterns |
| Observability does not replace authorization, preventive controls, or business accountability | Current pattern Non-goals and Prohibited uses |
| Source-pattern enforcement ownership, target transaction truth, and capability outcome accountability | User-approved 2026-07-13 hardening clarification; current pattern Assumptions and prerequisites, Non-goals, Architecture decisions and parameters, and Related patterns |
| Untrusted correlation identifiers never authorize | Current pattern Data and instruction flows |
| Evidence and assurance independence | Approved 2026-07-12 design sections 2, 4.3, and 4.7; current pattern Problem statement, Intended outcomes, Assumptions and prerequisites, Actors and identities, and Evidence and assessment |
| Sampling exclusions and sensitive-content treatment | Approved 2026-07-12 design section 6; current pattern Data and instruction flows |
| Privacy-safe evidence handling in alerts and response channels | Approved 2026-07-12 design sections 6 and 10; current pattern Data and instruction flows and Anti-patterns |
| Tenant isolation and privileged access | Approved 2026-07-12 design section 11; current pattern Trust boundaries and Evidence and assessment |
| Provider gap register and prohibition semantics | Approved 2026-07-12 design section 12; current pattern Prohibited uses, Trust boundaries, and Evidence and assessment |
| Dashboards and self-evaluation are non-authoritative | Approved 2026-07-12 design sections 2, 4.6, and 8; current pattern Problem statement, Non-goals, Prohibited uses, Components and responsibilities, and Evidence and assessment |
| Tier 3/4 safe stop, bounded degraded mode, and governed recovery | Approved 2026-07-12 design section 13; current pattern Failure modes and abuse cases and Fallback recovery and retirement |

Any proposed assertion that cannot be traced to an approved source shall be treated as a candidate clarification and shall require separate approval before it can justify normative pattern changes.

### 5.5 Assurance and sensitive-telemetry contract

Tests shall require explicit language that:

- externally supplied trace and correlation identifiers are untrusted and never authorize access or action;
- monitored runtimes and ordinary administrators cannot select, suppress, rewrite, or delete authoritative evidence or assurance verdicts;
- sampling cannot omit denials, incidents, evidence gaps, material policy decisions, consequential outcomes, or required Tier 3 and Tier 4 records;
- actionable alerts reference protected evidence;
- alerts, cases, tickets, email, and chat do not duplicate raw or sensitive source content;
- prompts, context, retrieval content, outputs, tool data, agent state, hashes, embeddings, and rare features receive appropriate classification, minimization, isolation, retention, correction, deletion, and legal-hold treatment;
- tenant binding is established or independently validated at ingestion and tested across stores, encryption, indexes, queries, joins, caches, exports, evaluations, alerts, incidents, backups, migrations, privileged access, timing, and high-cardinality surfaces;
- provider telemetry is externally asserted, gaps are registered, and a material assurance gap prohibits the affected tier, action, or provider use; and
- dashboards, aggregates, transport receipts, provider consoles, and model self-evaluation cannot silently replace authoritative evidence or governed ground truth.

### 5.6 Resilience and recovery contract

Tests shall require explicit treatment for missing, late, duplicate, out-of-order, replayed, spoofed, injected, conflicting, or corrupted telemetry; clock uncertainty; source or signing-key compromise; provider outage; export delay; backpressure; suppression abuse; containment abuse; and evidence-integrity failure.

Tier 3 and Tier 4 consequential activity shall stop or remain unable to commit when required evidence, approval correlation, target outcome, integrity verification, or assurance is unknown.

Lower-tier degraded operation shall be preapproved, visible, bounded by duration and volume, protected by local buffering, and prohibited from increasing data, authority, provider, or action scope. Expiry, buffer exhaustion, missing tenant binding, unverifiable telemetry, or privacy-policy failure shall cause the approved safe stop.

Recovery shall require signed or otherwise verified backfill, sequence reconciliation, integrity and custody verification, gap disposition, privacy-obligation handling, material incident review, and authorized return to normal operation.

## 6. Mermaid publication gate

The focused unit-test module shall count and extract the four consecutively numbered Mermaid figures and shall reject known source hazards such as semicolon-delimited sequence messages. Unit tests do not invoke a browser or claim renderer validity.

Renderer validation is a separate publication command. For this milestone it shall use `pnpm dlx @mermaid-js/mermaid-cli@11.16.0`, extract each block to standard input, render to a system-temporary SVG with a bounded command timeout, verify exit status zero and a nonempty artifact, and remove all artifacts after the gate. The gate passes only when all four renders succeed. CI integration or a reusable repository renderer tool is outside this hardening milestone unless separately approved.

Local renderer verification shall be reported accurately. It shall not be described as GitHub visual verification unless an authenticated GitHub-rendered view was actually inspected.

## 7. Defect handling

Hardening begins by adding tests against the unchanged Draft. A failing gate shall be classified as one of:

- test defect or brittle assertion;
- missing normative requirement;
- ambiguous or contradictory language;
- control-allocation mismatch; or
- Mermaid parser or rendering defect.

Only confirmed ARC-P160 defects may change pattern content. Each correction shall be minimal, shall preserve the approved architecture, and shall retain focused regression coverage. Unrelated restructuring or scope expansion is prohibited.

## 8. Review and validation

The implementation shall complete:

- focused ARC-P160 tests;
- the full `unittest` discovery suite;
- `tools/validate_controls.py --check`;
- `tools/validate_architectures.py`;
- `git diff --check`;
- placeholder and generated-cache checks;
- Mermaid CLI rendering for every figure; and
- independent whole-branch review.

Critical and Important findings shall be resolved before publication. The pull-request description shall record the reviewed head SHA, exact test and validator counts, renderer results, changed files, and any residual concerns. The reviewed SHA shall still equal the PR head before merge.

## 9. Deliverables

Expected implementation changes are:

- create `tests/test_arc_p160_pattern.py`;
- modify `architectures/patterns/ARC-P160.md` only if hardening gates prove a defect; and
- leave `architectures/patterns/README.md` unchanged unless a current inconsistency is proven.

The design specification and implementation plan are separate planning commits and do not alter the normative standard.

## 10. Acceptance criteria

The milestone is complete when:

- focused tests protect publication, allocation, architecture, assurance, privacy, tenancy, resilience, and recovery contracts;
- required, inherited-and-verified, and conditional controls are exact, disjoint, total 68, and all resolve in the catalog;
- all ARC-P160 Mermaid figures render successfully;
- every confirmed defect has focused regression coverage;
- focused and full tests, both validators, and diff checks pass;
- no generated caches or rendering artifacts remain;
- independent review reports no unresolved Critical or Important findings;
- GitHub checks pass and the PR has a clean merge state;
- post-merge validation passes on `main`; and
- the temporary implementation branch and worktree are removed.
