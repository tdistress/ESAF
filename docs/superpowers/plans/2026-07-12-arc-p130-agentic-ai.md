# ARC-P130 Agentic and Multi-Agent AI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish ARC-P130 as a complete, validated architecture pattern for bounded-authority agentic and multi-agent systems.

**Architecture:** Author ARC-P130 against the approved pattern contract and design, using external authority leases, attenuated delegation, transactional action execution, brokered memory, authenticated multi-agent messaging, independent evidence, and out-of-band containment. Reuse the pattern-aware validator and obtain independent control and threat reviews before release.

**Tech Stack:** Markdown, Python 3.13 standard library, Python unittest, GitHub Actions, Git.

## Global Constraints

- Models may propose plans and actions but cannot authorize them.
- Effective authority is the intersection of current principal or service authority, agent lease, policy, target authorization, data policy, and valid approval.
- Every consequential commit receives a fresh authorization and revocation check.
- Delegation always attenuates authority and creates a new identity.
- Consequential actions use prepare, commit, and reconcile where feasible.
- Tier 3 and Tier 4 success requires independent outcome assurance.
- Kill controls remain outside the agent and cannot retract already committed external effects.
- All referenced controls resolve to authoritative ESAF control records.

---

### Task 1: Registry red state and normative pattern

**Files:**
- Modify: `architectures/patterns/README.md`
- Create: `architectures/patterns/ARC-P130.md`

**Interfaces:**
- Consumes: approved ARC-P130 design, pattern template, trust zones, ARC-P100, ARC-P120, and ESAF controls
- Produces: complete ARC-P130 Draft record and linked registry entry

- [ ] **Step 1: Link ARC-P130 before creating the record**

Change the registry entry to a Draft link, then run `python tools/validate_architectures.py` and confirm it fails with a broken `ARC-P130.md` link.

- [ ] **Step 2: Author the complete pattern**

Populate every required section with security invariants, logical views, identities, authority leases, delegation, messages, memory, tools, approvals, transactions, control points, safe failure, containment, variants, controls, evidence, and assessment.

- [ ] **Step 3: Verify and commit**

Run architecture, unit, and control validation. Commit the pattern and registry as `Publish ARC-P130 agentic AI pattern`.

### Task 2: Independent technical review

**Files:**
- Modify if findings require correction: `architectures/patterns/ARC-P130.md`

**Interfaces:**
- Consumes: completed ARC-P130 record
- Produces: resolved control-traceability and security review findings

- [ ] **Step 1: Request two reviews**

One subagent verifies exact controls, classifications, owners, evidence, and assessments. A second reviews leases, effective authority, delegation, approvals, transactions, durable work, memory, messages, evidence, containment, and outcome assurance.

- [ ] **Step 2: Resolve findings and verify**

Apply material corrections, rerun all validation, and commit review corrections separately when present.

### Task 3: Release records and publication

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `project/BACKLOG.md`
- Modify: `project/DECISION_LOG.md`
- Create: `docs/superpowers/plans/2026-07-12-arc-p130-agentic-ai.md`

**Interfaces:**
- Consumes: reviewed ARC-P130 pattern
- Produces: release traceability, updated queue, and merged implementation PR

- [ ] **Step 1: Update release records**

Record ARC-P130 publication, remove it from the active backlog, make ARC-P160 the next pattern, and record the bounded-authority transactional design as DEC-0014.

- [ ] **Step 2: Run final verification**

Run `python -m unittest discover -s tests -v`, `python tools/validate_architectures.py`, `python tools/validate_controls.py --check`, and `git diff --check`; expect all commands to exit 0.

- [ ] **Step 3: Publish and merge**

Commit release records, push the branch, open a ready PR, wait for repository validation, merge, synchronize `main`, and confirm the post-merge workflow passes.
