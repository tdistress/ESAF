# ARC-P150 AI Integration Services Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish ARC-P150 as ESAF's vendor-neutral reference architecture for contract-first, deterministic, reusable AI integration services across synchronous, asynchronous, streaming, batch, event, subscription, and callback interactions.

**Architecture:** ARC-P150 uses a shared policy-administration and configuration plane with federated regional or domain execution cells. Six logical planes, fifteen control points, orthogonal state machines, at-least-once durable delivery, bounded authorization, independent evidence export, and risk-tiered degraded operation connect enterprise consumers to AI, data, providers, and targets without granting hidden agency.

**Tech Stack:** GitHub Markdown, ESAF-1200 architecture template, Mermaid rendered by GitHub, Python `unittest`, `tools/validate_controls.py`, and `tools/validate_architectures.py`.

## Global Constraints

- The approved design at `docs/superpowers/specs/2026-07-12-arc-p150-ai-integration-services-design.md` is authoritative.
- ARC-P150 owns deterministic, pre-authorized reusable integration services. ARC-P130 is mandatory when AI selects a target or operation, expands delegation or scope, or determines a consequential action.
- The baseline supports synchronous request/response, asynchronous jobs and queues, streaming, batch and file processing, events and subscriptions, and callbacks or webhooks.
- The architecture is a contract-first federated fabric. The shared plane administers policy and distributes signed configuration but is not a mandatory workload path; execution cells perform local admission and enforcement.
- The pattern contains exactly six logical planes, seven numbered Mermaid views, and fifteen control points identified `CP1` through `CP15`.
- Global bootstrap and cell discovery use signed, purpose-, audience-, tenant-, capability-, region-, endpoint-, version-, expiry-, and replay-bound assertions. Consumers authenticate selected cell endpoints before releasing credentials or application content.
- Execution cells prove credential-bound, freshness-bounded, clone- and replay-resistant deployment identity or equivalent release closure and posture. Failed posture causes quarantine, secret denial, and failover exclusion.
- ARC-P100 outcomes govern every inference handoff through approved centralized or federated enforcement. ARC-P120 governs semantic retrieval. ARC-P130 governs agency and consequential action. ARC-P140 applies additionally to enterprise-operated model lifecycle and serving. ARC-P160 supplies independent evidence and applicable outcome assurance.
- Durable delivery assumes at-least-once transport with idempotency, deduplication, bounded retry, explicit unknown outcome, compensation where defined, and authoritative reconciliation. The pattern does not claim exactly-once business effects.
- Transport, service execution, result delivery, target transaction, and business outcome remain orthogonal state machines with separate owners and evidence.
- Authorization is current at every consequential or delivery boundary. Streams, subscriptions, jobs, batches, and callbacks use bounded leases with periodic and event-driven revalidation.
- Configuration signing, callback signing, runtime identity, trusted time, emergency containment, operations administration, and evidence export use explicit trust lifecycles and separated authority.
- Control-plane loss permits only bounded signed cached operation without route, privilege, provider, model, data, target, action, tenant, connectivity, or administrative expansion.
- Tier 3 and Tier 4 consequential commit and dependent activity stop when applicable current authorization, required evidence, or outcome assurance is unavailable. Non-consequential inference or retrieval is not stopped solely because target-outcome assurance is inapplicable.
- All control identifiers resolve against `controls/catalog.json`; catalog `owner_role` remains authoritative for control accountability.
- Required, inherited-and-verified, and conditional allocations remain distinct, mutually exclusive, and match approved design section 19: 46 required, 26 inherited-and-verified, and 19 conditional controls.
- Each deployment assigns exactly one accountable owner per control point and records implementation, evidence, consultation, consumption, and assurance contributors separately.
- The pattern follows the exact section order in `architectures/ARCHITECTURE_TEMPLATE.md`, remains supplier-neutral, and contains no drafting placeholders.
- The registry changes only the ARC-P150 row at `architectures/patterns/README.md:12` from Proposed to linked Draft.

---

### Task 0: Create and verify the implementation branch

**Files:**
- Verify: repository worktree and `main`

**Interfaces:**
- Consumes: the merged planning PR on current `main`.
- Produces: a clean `agent/arc-p150-implementation` branch whose merge base is the reviewed planning commit.

- [ ] **Step 1: Create the isolated implementation branch**

Use `superpowers:using-git-worktrees` when executing in an isolated worktree. Otherwise run:

```powershell
git switch main
git pull --ff-only origin main
if (git status --porcelain) { throw "Main worktree is not clean" }
git switch -c agent/arc-p150-implementation
```

- [ ] **Step 2: Verify branch identity and base**

```powershell
$branch = git branch --show-current
if ($branch -ne 'agent/arc-p150-implementation') { throw "Unexpected branch: $branch" }
$main = git rev-parse main
$base = git merge-base HEAD main
if ($base -ne $main) { throw "Implementation branch is not based on current main" }
git status -sb
```

Expected: current branch is `agent/arc-p150-implementation`, its merge base equals current `main`, and the worktree is clean.

---

### Task 1: Establish the pattern foundation and executable contract tests

**Files:**
- Create: `tests/test_arc_p150_pattern.py`
- Create: `architectures/patterns/ARC-P150.md`
- Modify: `architectures/patterns/README.md:12`

**Interfaces:**
- Consumes: `architectures/ARCHITECTURE_TEMPLATE.md`, `controls/catalog.json`, the pattern registry, and approved design metadata and scope.
- Produces: a template-complete Draft record and focused regression tests that later tasks extend before adding each substantive section.

- [ ] **Step 1: Record the clean baseline**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest discover -s tests -v
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
```

Expected: 10 tests pass; 91 controls, 91 objectives, and 16 families validate; 10 foundation files and 7 reserved patterns validate.

- [ ] **Step 2: Write the foundation tests**

Create `tests/test_arc_p150_pattern.py` with:

```python
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN = ROOT / "architectures" / "patterns" / "ARC-P150.md"
REGISTRY = ROOT / "architectures" / "patterns" / "README.md"
TEMPLATE = ROOT / "architectures" / "ARCHITECTURE_TEMPLATE.md"


def headings(path: Path, level: int) -> list[str]:
    prefix = "#" * level
    return re.findall(rf"^{prefix} (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)


class ArcP150PatternTests(unittest.TestCase):
    def text(self) -> str:
        return PATTERN.read_text(encoding="utf-8")

    def test_registry_links_only_arc_p150_as_draft(self) -> None:
        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("| [ARC-P150](ARC-P150.md) | AI integration services | Draft |", registry)
        self.assertNotIn("| ARC-P150 | AI integration services | Proposed |", registry)

    def test_required_metadata_is_complete(self) -> None:
        text = self.text()
        for value in (
            "**Pattern ID:** ARC-P150",
            "**Status:** Draft",
            "**Version:** 0.1.0",
            "| Owner | Enterprise Architecture |",
            "| Required reviewers |",
            "| Approval date | Not approved (Draft) |",
            "| Review date |",
            "| Pillars | Protect AI, Utilize AI, Govern AI |",
            "| Lifecycle stages |",
            "| Capability tiers |",
            "| Deployment models |",
            "| Primary pattern role |",
            "| Supersedes | None |",
        ):
            self.assertIn(value, text)

    def test_template_headings_are_unique_and_ordered(self) -> None:
        expected = headings(TEMPLATE, 2)
        actual = headings(PATTERN, 2)
        self.assertEqual(expected, actual)

    def test_pattern_has_no_drafting_markers(self) -> None:
        text = self.text().lower()
        markers = ("t" + "bd", "t" + "odo", "place" + "holder", "lorem" + " ipsum")
        for marker in markers:
            self.assertNotIn(marker, text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the new test to verify the red phase**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest tests.test_arc_p150_pattern -v
```

Expected: ERROR because `architectures/patterns/ARC-P150.md` does not exist and FAIL because the registry still lists ARC-P150 as Proposed.

- [ ] **Step 4: Create the template-complete foundation**

Create `architectures/patterns/ARC-P150.md` with title `# ARC-P150 AI integration services`, complete metadata, and all 23 template headings in exact order. Fully author `Purpose`, `Problem statement`, `Intended outcomes`, `Non-goals`, `Applicability`, `Assumptions and prerequisites`, and `Prohibited uses` from approved design sections 1 through 5. Each remaining template section receives its approved governing statement rather than a drafting marker; Tasks 2 through 5 expand those sections.

Metadata shall include Enterprise Architecture ownership; application, API, integration, identity, data, model, security, operations, continuity, privacy, legal, supplier-risk, records, and assurance reviewers; Draft approval and review dates; all three pillars; Strategy through Retirement lifecycle stages; Tier 1 through Tier 4 with isolated Tier 0 experimentation; centralized, federated, regional, sovereign, high-assurance, edge, thin synchronous, durable workflow, and external-managed deployment forms; primary AI integration pattern role; and no superseded pattern.

Change only the ARC-P150 registry row to:

```markdown
| [ARC-P150](ARC-P150.md) | AI integration services | Draft |
```

- [ ] **Step 5: Run foundation tests and validators**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest tests.test_arc_p150_pattern -v
& $py tools/validate_architectures.py
```

Expected: 4 focused tests pass; architecture validation recognizes ARC-P150 as a linked Draft record.

- [ ] **Step 6: Commit the foundation**

```powershell
git add tests/test_arc_p150_pattern.py architectures/patterns/ARC-P150.md architectures/patterns/README.md
git commit -m 'Establish ARC-P150 pattern foundation'
```

Expected: one green commit containing the regression test, complete template structure, and registry promotion.

---

### Task 2: Define the federated architecture, boundaries, and views

**Files:**
- Modify: `tests/test_arc_p150_pattern.py`
- Modify: `architectures/patterns/ARC-P150.md`

**Interfaces:**
- Consumes: Task 1's pattern skeleton, ESAF trust zones, and design sections 6, 7, and 12.
- Produces: seven renderable architecture views plus complete actors, trust boundaries, components, shared-plane, cell, bootstrap, administration, and evidence responsibilities.

- [ ] **Step 1: Add failing architecture-view tests**

Add these methods to `ArcP150PatternTests`:

```python
    def test_seven_numbered_mermaid_views_cover_required_components(self) -> None:
        text = self.text()
        self.assertEqual([str(number) for number in range(1, 8)], re.findall(r"^### Figure (\d+)\.", text, re.MULTILINE))
        diagrams = re.findall(r"```mermaid\n(.*?)\n```", text, re.DOTALL)
        self.assertEqual(7, len(diagrams))
        rendered_source = "\n".join(diagrams).lower()
        for label in (
            "shared control plane",
            "global bootstrap",
            "execution cell",
            "policy-enforcement point",
            "contract validator",
            "durable state",
            "output validator",
            "administration",
            "evidence export",
            "arc-p100",
            "arc-p120",
            "arc-p130",
            "arc-p140",
            "arc-p160",
        ):
            self.assertIn(label, rendered_source)

    def test_six_plane_outcomes_are_explicit(self) -> None:
        text = self.text().lower()
        for plane in (
            "governance and contract plane",
            "admission and policy plane",
            "execution and adapter plane",
            "durable delivery and state plane",
            "output and delivery plane",
            "operations, administration, and evidence plane",
        ):
            self.assertIn(plane, text)
```

Run `python -m unittest tests.test_arc_p150_pattern -v` and expect both new tests to fail because the views and plane definitions are not complete.

- [ ] **Step 2: Author the seven required views**

Expand `Architecture views` with these minimum nodes and crossings:

1. **Context and pattern relationships:** consumers, ARC-P150 fabric, external providers, enterprise targets, and ARC-P100/P120/P130/P140/P160 handoffs.
2. **Federated topology:** shared control plane, global bootstrap, at least two execution cells, signed configuration and revocation distribution, federated policy decision, route assertion, failover eligibility, and state transfer.
3. **Six-plane component view:** every named plane; operations-administration and evidence-export shown as isolated subplanes with distinct interfaces and trust.
4. **Normative flow:** bootstrap, endpoint authentication, local admission, contract validation, durable acceptance, deterministic dispatch, supporting-pattern handoff, output validation, conditional reconciliation, delivery, and cross-cutting evidence at admission through recovery.
5. **State and durable-delivery view:** transport, service execution, result delivery, target transaction, and business outcome as separate state authorities; queue, event, stream, batch, callback, idempotency, unknown outcome, and reconciliation.
6. **Degraded operation and recovery:** signed cached bundle, trusted time and anti-rollback, restriction-only emergency path, Tier 3/4 stop or commit block, reconnect validation, and reconciliation.
7. **Retirement:** drain or cancel, resolve unknown state, revoke identities/routes/subscriptions/callbacks, dispose data and results, provider exit, preserve evidence, and residual-access test.

- [ ] **Step 3: Author actors, trust boundaries, and components**

Expand `Actors and identities`, `Trust boundaries`, and `Components and responsibilities` with all identities and separation rules from design sections 7, 10, and 12. The boundary table shall explicitly include consumer-to-bootstrap, bootstrap-to-consumer-and-cell, shared-plane-to-cell distribution, cell-to-federated-PDP, source-cell-to-destination-cell failover, Z1-to-Z2 admission, Z2-to-Z3 dispatch, inference, retrieval, tool/target, callback/event, broker/queue, evidence, administration, and containment crossings. Each row records direction, identities, authorization, information, validation, protection, evidence, reliability, and retained responsibility.

Distinguish global cell discovery from cell-local capability discovery. Require route-assertion verification, selected-cell endpoint authentication, runtime cell posture, failover exclusion, and separately protected operations and evidence paths.

- [ ] **Step 4: Run architecture tests and validators**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest tests.test_arc_p150_pattern -v
& $py tools/validate_architectures.py
```

Expected: 6 focused tests pass and architecture validation remains clean.

- [ ] **Step 5: Commit the federated architecture**

```powershell
git add tests/test_arc_p150_pattern.py architectures/patterns/ARC-P150.md
git commit -m 'Define ARC-P150 federated architecture'
```

---

### Task 3: Define interaction contracts, authorization, and state semantics

**Files:**
- Modify: `tests/test_arc_p150_pattern.py`
- Modify: `architectures/patterns/ARC-P150.md`

**Interfaces:**
- Consumes: Task 2's components and crossings and design sections 8 through 15.
- Produces: complete mode contracts, identity and data rules, adapter semantics, output controls, and state and reliability behavior.

- [ ] **Step 1: Add failing interaction and state tests**

Add:

```python
    def test_all_interaction_modes_and_state_authorities_are_explicit(self) -> None:
        text = self.text().lower()
        for mode in (
            "synchronous request and response",
            "asynchronous jobs and queues",
            "streaming",
            "batch and file processing",
            "events and subscriptions",
            "callbacks and webhooks",
        ):
            self.assertIn(mode, text)
        for state in (
            "transport delivery",
            "service execution",
            "result delivery",
            "target transaction",
            "business outcome",
        ):
            self.assertIn(state, text)

    def test_durable_and_authorization_invariants_are_explicit(self) -> None:
        text = self.text().lower()
        for requirement in (
            "at-least-once",
            "unknown outcome",
            "idempotency",
            "bounded authorization lease",
            "current authorization",
            "authoritative reconciliation",
            "semantic map",
            "granular event permissions",
            "registered internal enterprise destinations",
        ):
            self.assertIn(requirement, text)
```

Run the focused test and expect the two new methods to fail.

- [ ] **Step 2: Author base and mode-specific contracts**

Expand `Data and instruction flows` and `Architecture decisions and parameters` with the base envelope and explicit required/optional/prohibited/server-issued/consumer-supplied/derived field rules. Cover identity, delegation, tenant, capability, purpose, operation, service and contract version, mode, classification, provenance, residency, retention, use, correlation, causation, request, deadline, expiry, budget, limit, response, and trace fields.

Add six named mode subsections. Preserve every mode-specific requirement from design section 9, including atomic job acceptance; frame and resume authorization; batch and per-item leases; immutable event ID, deduplication scope, sequence scope, gap policy, and separate publish/discover/subscribe/consume/acknowledge/checkpoint/replay/backfill/group/retained/wildcard/admin permissions; and registered callback destination classes with controlled internal private addressing.

- [ ] **Step 3: Author identity, data, adapter, output, and state rules**

Require distinct human, service, workload, cell, adapter, provider, broker, callback, target, and administrator identities. Define bounded lease and revocation behavior for queued jobs, streams, batches, subscriptions, callbacks, results, replay, and consequential commit. Preserve data/instruction classification, tenant isolation, deletion propagation, secrets handling, cache and idempotency scope, and in-flight disposition.

Require a field-level adapter semantic map and block unsupported or lossy identity, tenant, purpose, classification, provenance, expiry, delegation, policy, cancellation, sequence, idempotency, and unknown-state transformations. Treat AI output as untrusted. Invoke ARC-P130 only when AI-selected output is used to invoke, execute, persist, route, or determine material effect; human display alone does not invoke that pattern.

Define the five orthogonal state machines with approved states, owners, transition authority, contradiction handling, and reconciliation. Add stream, batch, event/subscription, and callback projections with their authoritative writers. Bind idempotency to caller, tenant, purpose, operation, contract, policy/authorization version, classification, normalized input, output destination, provider, model, target, region, lifecycle, and expiry.

- [ ] **Step 4: Run interaction tests and commit**

Run the focused tests, architecture validator, and control validator. Expect 8 focused tests to pass and both validators to succeed.

```powershell
git add tests/test_arc_p150_pattern.py architectures/patterns/ARC-P150.md
git commit -m 'Define ARC-P150 interaction and state semantics'
```

---

### Task 4: Define trust, degraded operation, failure treatment, and recovery

**Files:**
- Modify: `tests/test_arc_p150_pattern.py`
- Modify: `architectures/patterns/ARC-P150.md`

**Interfaces:**
- Consumes: Task 3's protocol and state model and design sections 13, 16, 17, and 20.1.
- Produces: assessable trust lifecycles, safe degradation, emergency containment, failure treatment, recovery, and retirement.

- [ ] **Step 1: Add failing trust and recovery tests**

Add:

```python
    def test_trust_degraded_operation_and_failure_treatment_are_explicit(self) -> None:
        text = self.text().lower()
        for requirement in (
            "configuration-signing trust",
            "callback-signing trust",
            "trusted time",
            "anti-rollback",
            "maximum isolation window",
            "more restrictive state",
            "out-of-band",
            "failure-and-abuse treatment record",
            "affected boundary and state machines",
            "reconciliation source",
            "tier applicability",
            "residual-access",
        ):
            self.assertIn(requirement, text)
```

Run the focused test and expect the new method to fail.

- [ ] **Step 2: Author trust and degraded-operation decisions**

Expand `Architecture decisions and parameters` and `Fallback recovery and retirement`. Define signing issuer, custody, purpose, approval/signing/trust/distribution/runtime separation, higher-tier threshold control, algorithm agility, rotation, compromise epoch, revocation, re-signing, and pre-compromise artifact disposition. Apply an equivalent lifecycle to callback signing.

Define trusted time, maximum uncertainty, monotonic or equivalent anti-rollback state, source loss, skew, and rollback. Require a separately protected out-of-band restriction path or restriction-only cell-local authority. If unavailable, the approved maximum isolation window cannot exceed the shortest relevant bundle, credential, route, provider, tenant, or authorization lifetime. Conflicting emergency commands resolve to the more restrictive state, emit independent evidence, and require governed recovery.

Define cached-operation constraints, applicable Tier 3/4 blocking, reconnection validation, state reconciliation, recovery tests, emergency suspension, provider exit, deletion, and residual-access retirement search.

- [ ] **Step 3: Author the complete failure-and-abuse treatment**

Expand `Failure modes and abuse cases` with a required record containing: initiating condition or adversary capability; affected boundary and state machines; detection signal and maximum interval; containment and safe state; recovery and resumption authority; authoritative reconciliation source; required evidence; residual risk; tier applicability; and retest trigger.

The inventory shall literally cover all negative-test categories in approved design section 20, including forged identity, delegation, audience, scope, purpose, tenant, and classification; authorization or revocation change during every durable mode; model-generated endpoints, methods, tools, queries, commands, paths, credentials, and targets; bootstrap, route, cell identity, release-closure, lateral-secret, and forged-evidence attacks; event permission abuse; partial-stream disclosure and exhaustion; callback audience, digest, job binding, signer, key-status, replay, redirect, resolution, destination, and error attacks; connector or SDK compromise and rollback; trust, time, containment, telemetry, evidence, Z7, lifecycle, provider, transport, state, capacity, and retirement failures.

- [ ] **Step 4: Run trust tests and commit**

Run the focused tests and both validators. Expect 9 focused tests to pass.

```powershell
git add tests/test_arc_p150_pattern.py architectures/patterns/ARC-P150.md
git commit -m 'Define ARC-P150 trust and recovery requirements'
```

---

### Task 5: Complete controls, evidence, variants, and acceptance

**Files:**
- Modify: `tests/test_arc_p150_pattern.py`
- Modify: `architectures/patterns/ARC-P150.md`

**Interfaces:**
- Consumes: Tasks 1 through 4 and approved design sections 18 through 24.
- Produces: the complete control allocation, control points, coverage matrix, evidence model, variants, anti-patterns, related patterns, and acceptance record.

- [ ] **Step 1: Add failing control-allocation and completion tests**

Add imports `json` and these helpers above the class:

```python
CATALOG = ROOT / "controls" / "catalog.json"
CONTROL = re.compile(r"`([A-Z]{3}-\d{3})`")


def subsection(text: str, title: str) -> str:
    match = re.search(rf"^### {re.escape(title)}\s*$\n(.*?)(?=^### |^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"Missing subsection: {title}")
    return match.group(1)
```

Add methods:

```python
    def test_control_partition_matches_catalog_exactly(self) -> None:
        text = self.text()
        required = set(CONTROL.findall(subsection(text, "Required catalog controls")))
        inherited = set(CONTROL.findall(subsection(text, "Inherited and verified catalog controls")))
        conditional = set(CONTROL.findall(subsection(text, "Conditional catalog controls")))
        catalog = {item["id"] for item in json.loads(CATALOG.read_text(encoding="utf-8"))["controls"]}
        self.assertEqual((46, 26, 19), (len(required), len(inherited), len(conditional)))
        self.assertFalse(required & inherited)
        self.assertFalse(required & conditional)
        self.assertFalse(inherited & conditional)
        self.assertEqual(catalog, required | inherited | conditional)

    def test_control_points_are_exact_and_singly_accountable(self) -> None:
        text = self.text()
        ids = re.findall(r"^\| (CP\d+) \|", text, re.MULTILINE)
        self.assertEqual([f"CP{number}" for number in range(1, 16)], ids)
        self.assertIn("exactly one accountable owner", text.lower())

    def test_design_coverage_and_variants_are_complete(self) -> None:
        text = self.text().lower()
        for coverage in ("| 1-5 |", "| 6-7 |", "| 8-9 |", "| 10-14 |", "| 15-17 |", "| 18-20 |", "| 21-24 |"):
            self.assertIn(coverage, text)
        for variant in (
            "central multi-protocol hub",
            "durable workflow and event backbone",
            "regional or sovereign cells",
            "high-assurance dedicated cell",
            "edge or intermittently connected cell",
            "thin synchronous service",
            "external managed integration service",
        ):
            self.assertIn(variant, text)
```

Run the focused test and expect the three new methods to fail.

- [ ] **Step 2: Author controls and control points**

Under `Required controls`, add exact subsections `Required catalog controls`, `Inherited and verified catalog controls`, and `Conditional catalog controls`. Copy the literal allocations from approved design section 19. For inherited controls, require a record of source, component or crossing, supplied outcome, consumer configuration, limitations, evidence, freshness, failure dependency, and retained responsibility. Preserve every conditional trigger, including broad API-140 external-service participation.

Under `Control points and overlays`, reproduce CP1 through CP15 in order with approved outcome and roles. State that each tailored deployment assigns exactly one accountable owner per CP and treats all other listed roles as implementation, consultation, consumption, evidence, or assurance contributors. Map security, privacy, resilience, deployment, risk, and obligation overlays.

- [ ] **Step 3: Author evidence, coverage, variants, and closure**

Expand `Evidence and assessment` with every artifact and test class in design section 20. Require event occurrence, receipt, and processing times; time quality and uncertainty; scoped source sequence; duplicate/gap/reorder/late disposition; transformation lineage; delivery state; and source attestation. Preserve independent administration/evidence identities, interfaces, trust roots, and authority.

Add `### Design coverage matrix` with rows for design sections `1-5`, `6-7`, `8-9`, `10-14`, `15-17`, `18-20`, and `21-24`. Each row maps design obligations to pattern sections, figures, CPs, evidence, assessment cases, and reviewer discipline. This matrix is retained in the pattern and summarized in the PR.

Complete `Variants and alternatives` with all seven variants and explicit component combination or external-supply rules, changed flows, evidence and failure dependencies, retained enterprise accountability, and invariant CP1-CP15, six-plane, supporting-pattern, safe-state, and control-allocation outcomes. Complete every anti-pattern, related-pattern boundary, acceptance criterion, and change-history row from the design.

- [ ] **Step 4: Run completion tests and commit**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest tests.test_arc_p150_pattern -v
& $py -m unittest discover -s tests -v
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
git diff --check
```

Expected: 12 focused ARC-P150 tests and 22 total tests pass; 91 controls, 91 objectives, and 16 families validate; architecture validation succeeds; and diff checking is clean.

```powershell
git add tests/test_arc_p150_pattern.py architectures/patterns/ARC-P150.md
git commit -m 'Complete ARC-P150 assurance requirements'
```

---

### Task 6: Validate, independently review, and publish

**Files:**
- Verify: `tests/test_arc_p150_pattern.py`
- Verify: `architectures/patterns/ARC-P150.md`
- Verify: `architectures/patterns/README.md`
- Verify: `docs/superpowers/specs/2026-07-12-arc-p150-ai-integration-services-design.md`
- Verify: `docs/superpowers/plans/2026-07-12-arc-p150-ai-integration-services.md`

**Interfaces:**
- Consumes: all green implementation commits.
- Produces: fresh validation evidence, independent review closure, a merged implementation PR, and verified `main`.

- [ ] **Step 1: Verify branch and commit scope**

Run:

```powershell
git status --short
git log --oneline main..HEAD
git diff --name-only main...HEAD
git show --name-only --format= HEAD
```

Expected: `main..HEAD` contains only implementation commits and the branch diff is limited to the pattern, registry, and focused test. The already-merged planning commit contains only the plan. The final implementation commit shown by `git show` changes only `tests/test_arc_p150_pattern.py` and `architectures/patterns/ARC-P150.md`.

- [ ] **Step 2: Run the complete fresh validation suite**

Run the exact commands from Task 5 Step 4. Expected: 12 focused and 22 total tests pass; both validators succeed; 46/26/19 control allocation passes; CP1-CP15, seven figures, six planes, six modes, metadata, heading order, coverage rows, and variants pass; and the diff is clean.

- [ ] **Step 3: Request independent reviews and record the reviewed commit**

Request three read-only reviews:

1. architecture and boundary review against ARC-P100 through ARC-P160;
2. threat and abuse-case review across bootstrap, cells, protocols, state, trust, degraded operation, evidence, and retirement; and
3. control partition, CP accountability, template, coverage-matrix, and assessment-evidence review.

Resolve every Critical or Important finding. Re-run targeted verification by the originating reviewer after remediation. Record accepted Minor findings and rationale in the PR.

After remediation and a fresh Task 5 Step 4 validation, record the exact reviewed commit:

```powershell
$reviewedSha = git rev-parse HEAD
if (git status --porcelain) { throw "Reviewed worktree is not clean" }
Write-Output "Reviewed commit: $reviewedSha"
```

- [ ] **Step 4: Push and open the draft PR**

Run:

```powershell
git push -u origin agent/arc-p150-implementation
$reviewedSha = git rev-parse HEAD
$body = @'
## Summary

- publishes ARC-P150 as the Draft AI integration services reference architecture
- adds focused ARC-P150 structure, allocation, and coverage regression tests
- promotes only the ARC-P150 registry row from Proposed to linked Draft

## Design coverage

- retains the approved design-section coverage matrix for sections 1-5, 6-7, 8-9, 10-14, 15-17, 18-20, and 21-24
- preserves mandatory ARC-P100 inference outcomes and the ARC-P120, ARC-P130, ARC-P140, and ARC-P160 applicability boundaries

## Validation

- 12 ARC-P150 focused tests and 22 total tests passed
- architecture and control validators passed; 91 controls, 91 objectives, and 16 families validated
- control partition is 46 required, 26 inherited-and-verified, and 19 conditional controls with exact catalog equality
- CP1-CP15, seven figures, six planes, six interaction modes, metadata, template order, coverage rows, and variants passed
- all Critical and Important independent-review findings were resolved and reverified
- Mermaid rendering is pending on this draft PR and blocks promotion until 7/7 figures render

## Reviewed commit

Reviewed commit: `$reviewedSha`
'@
$body = $body.Replace('$reviewedSha', $reviewedSha)
$prUrl = gh pr create --draft --base main --head agent/arc-p150-implementation --title "Publish ARC-P150 AI integration services pattern" --body $body
$prNumber = [int]($prUrl.TrimEnd('/') -split '/')[-1]
gh pr edit $prNumber --add-label architecture --add-label documentation --add-label draft
```

Expected: one draft PR against `main` containing the implementation commits and a body with design coverage, exact validation results, reviewer closure, the reviewed 40-character commit ID, and an explicit pending Mermaid gate.

- [ ] **Step 5: Verify Mermaid rendering and update the PR evidence**

Open the rendered `architectures/patterns/ARC-P150.md` file from the draft PR's **Files changed** tab. Inspect Figures 1 through 7 at desktop width and confirm that GitHub renders each without a Mermaid syntax error, truncated label, missing node, or ambiguous edge. A rendering failure blocks publication and requires a new review and reviewed commit after correction.

After 7/7 render, update the PR body:

```powershell
$prNumber = gh pr view --json number --jq '.number'
$body = gh pr view $prNumber --json body --jq '.body'
$body = $body.Replace('- Mermaid rendering is pending on this draft PR and blocks promotion until 7/7 figures render', '- GitHub rendered all seven Mermaid figures without error (7/7)')
gh pr edit $prNumber --body $body
```

- [ ] **Step 6: Promote only the reviewed commit after all gates pass**

Run:

```powershell
$prNumber = gh pr view --json number --jq '.number'
$body = gh pr view $prNumber --json body --jq '.body'
if ($body -notmatch 'Reviewed commit: `([0-9a-f]{40})`') { throw "PR body lacks a reviewed commit" }
$reviewedSha = $Matches[1]
$headOid = gh pr view $prNumber --json headRefOid --jq '.headRefOid'
if ($headOid -ne $reviewedSha) { throw "PR head differs from reviewed commit" }
if ($body -notmatch 'rendered all seven Mermaid figures.*7/7') { throw "Mermaid render gate is incomplete" }
gh pr ready $prNumber
gh pr edit $prNumber --remove-label draft --add-label review
$expectsChecks = Test-Path -LiteralPath '.github/workflows/catalog-validation.yml'
$deadline = [DateTime]::UtcNow.AddMinutes(2)
do {
    $checkCount = [int](gh pr view $prNumber --json statusCheckRollup --jq '.statusCheckRollup | length')
    if ($checkCount -gt 0) { break }
    if ([DateTime]::UtcNow -ge $deadline) { break }
    Start-Sleep -Seconds 5
} while ($true)
if ($expectsChecks -and $checkCount -eq 0) { throw "Expected repository validation checks did not register" }
if ($checkCount -gt 0) {
    gh pr checks $prNumber --watch
    if ($LASTEXITCODE -ne 0) { throw "PR checks did not pass" }
}
$state = gh pr view $prNumber --json mergeStateStatus,reviewDecision,headRefOid
$stateObject = $state | ConvertFrom-Json
$reviewDecision = [string]$stateObject.reviewDecision
if ($stateObject.headRefOid -ne $reviewedSha) { throw "PR head changed after review" }
if ($reviewDecision -in @('CHANGES_REQUESTED', 'REVIEW_REQUIRED')) { throw "Required review is incomplete: $reviewDecision" }
if ($reviewDecision -notin @('APPROVED', '')) { throw "Unexpected review state: $reviewDecision" }
if ($stateObject.mergeStateStatus -ne 'CLEAN') { throw "PR is not cleanly mergeable: $($stateObject.mergeStateStatus)" }
if ($reviewDecision -eq '') { Write-Output 'No approving review is enforced by repository policy; proceeding under the repository owner standing authorization recorded for this project.' }
gh pr merge $prNumber --merge --delete-branch
```

Stop if any check is failing or pending, a Critical or Important review finding remains, Mermaid rendering is not 7/7, or the branch differs from the reviewed commit.

- [ ] **Step 7: Verify merged `main`**

Run:

```powershell
git switch main
git pull --ff-only origin main
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest discover -s tests -v
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
git status --short
```

Expected: 22 total tests pass; both validators succeed; and merged `main` is clean.
