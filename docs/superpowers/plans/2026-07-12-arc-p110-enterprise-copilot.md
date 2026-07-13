# ARC-P110 Enterprise Copilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish ARC-P110 as ESAF's vendor-neutral enterprise copilot architecture pattern for managed workforce users.

**Architecture:** ARC-P110 is a governed human-interaction shell with federated enforcement. It owns identity-bound sessions, purpose and context transparency, disclosures, attachments, source presentation, responses, optional memory, confirmation, feedback, accessibility, records, and safe failure while composing with ARC-P100, ARC-P120, ARC-P130, and ARC-P160.

**Tech Stack:** GitHub Markdown, ESAF-1200 architecture template, Mermaid, Python `unittest`, `tools/validate_controls.py`, and `tools/validate_architectures.py`.

## Global Constraints

- The approved design at `docs/superpowers/specs/2026-07-12-arc-p110-enterprise-copilot-design.md` is authoritative.
- The baseline serves employees and approved contractors using enterprise-managed identities and channels.
- Context and memory are session-scoped by default; durable memory requires separate explicit opt-in by purpose.
- Enterprise knowledge is a baseline capability whose ARC-P120 and `DAT-150` obligations are inherited and verified.
- Connectors are read-oriented by default; write or consequential action requires ARC-P130 and exact manifest-bound confirmation.
- Live multi-user and public/customer sessions are outside the baseline.
- The architecture contains exactly six logical layers and eighteen control points identified `CP1` through `CP18`.
- Tier 3/4 advisory use stops when identity, authorization, required grounding, integrity, or assurance is unavailable; consequential activity additionally requires confirmation and target-state evidence.
- The pattern remains vendor-neutral and does not select products or prescribe a visual design system.
- All control identifiers resolve against `controls/catalog.json`; catalog `owner_role` remains accountable.
- The pattern follows every required section in `architectures/ARCHITECTURE_TEMPLATE.md` and contains no drafting placeholders.
- The registry links ARC-P110 and changes its state from Proposed to Draft without altering other pattern states.

---

### Task 1: Publish the ARC-P110 pattern and registry record

**Files:**
- Create: `architectures/patterns/ARC-P110.md`
- Modify: `architectures/patterns/README.md`

**Interfaces:**
- Consumes: the approved design, architecture template, trust zones, principles, selection procedure, and conventions in ARC-P100, ARC-P120, ARC-P130, and ARC-P160.
- Produces: a registry-linked Draft pattern that the architecture validator recognizes as a complete pattern record.

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

- [ ] **Step 2: Author the complete pattern record**

Create `architectures/patterns/ARC-P110.md` with metadata followed by every heading from `architectures/ARCHITECTURE_TEMPLATE.md`. Include all approved design requirements, including:

```text
Metadata: ARC-P110; Enterprise copilot; Draft; version 0.1.0; Enterprise Architecture owner;
approval and review dates; Protect/Utilize/Govern pillars; applicable lifecycle stages;
Tier 1 through Tier 4, with isolated Tier 0 experimentation; cloud, hybrid, on-premises,
managed service, endpoint, and high-assurance deployment forms.

Architecture decision: governed interaction shell with federated enforcement.

Layers: experience; session and context; policy and orchestration; knowledge and connector;
model and response; evidence and operations.

Baseline: managed workforce identities; session-scoped context and memory; authorization-aware
enterprise knowledge; read-oriented connectors; exact confirmation for consequential action;
no live multi-user or customer/public use.

Control points: CP1 channel and managed-user admission through CP18 degraded mode, safe stop,
recovery, and retirement, with the exact purposes and implementation/evidence roles in the design.

Controls: required, inherited-and-verified, and conditional allocations exactly as design §17.
```

The record shall contain numbered Mermaid context, layer/component, interaction flow, action-confirmation, and degraded-mode/recovery views. It shall explicitly address identity step-up and continuous authorization; session and cross-channel isolation; machine-readable and user-visible context manifests; instruction classes and integrity; attachment/URL isolation; authorization at discovery, retrieval, presentation, sharing, and export; citation quality and authorization-safe presentation; display/copy/download/share/email/connector output boundaries; opt-in memory item governance; action manifests and confirmation integrity; accessibility and deceptive UX; feedback anti-retaliation; minimized decision records; ARC-P160 evidence of what the user saw; provider and connector gaps; and tiered safe failure.

- [ ] **Step 3: Link and promote the registry entry**

Change only the ARC-P110 row in `architectures/patterns/README.md` from:

```markdown
| ARC-P110 | Enterprise copilot | Proposed |
```

to:

```markdown
| [ARC-P110](ARC-P110.md) | Enterprise copilot | Draft |
```

- [ ] **Step 4: Run focused validation**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest discover -s tests -v
& $py tools/validate_architectures.py
& $py tools/validate_controls.py --check
```

Expected: all 10 tests pass; architecture validation succeeds with ARC-P110 linked as Draft; all control sources validate.

- [ ] **Step 5: Run semantic and repository checks**

Run:

```powershell
git diff --check
rg -n 'TBD|TODO|PLACEHOLDER|lorem ipsum' architectures/patterns/ARC-P110.md
rg -n '^\| CP(?:[1-9]|1[0-8]) ' architectures/patterns/ARC-P110.md
```

Expected: no whitespace or placeholder errors and exactly 18 CP rows. Independently resolve every control ID against `controls/catalog.json`, compare headings to `architectures/ARCHITECTURE_TEMPLATE.md`, and confirm exactly six named layers.

- [ ] **Step 6: Self-review against the approved design**

Verify every design section maps to substantive pattern content; ownership is explicit; required/inherited/conditional controls are not blurred; context visibility does not make mandatory controls user-disableable; read access does not transfer to recipients; protected values need not appear literally in action previews; advisory safe-stop is distinct from action outcome evidence; dashboards are not authoritative evidence; and no supplier-specific guidance appears.

- [ ] **Step 7: Commit the implementation**

```powershell
git add architectures/patterns/ARC-P110.md architectures/patterns/README.md
git commit -m 'Publish ARC-P110 enterprise copilot pattern'
```

Expected: one focused implementation commit containing the pattern and registry promotion.

---

### Task 2: Validate the complete implementation branch

**Files:**
- Verify: `architectures/patterns/ARC-P110.md`
- Verify: `architectures/patterns/README.md`
- Verify: `docs/superpowers/specs/2026-07-12-arc-p110-enterprise-copilot-design.md`

**Interfaces:**
- Consumes: Task 1's committed pattern and registry change.
- Produces: complete validation evidence and a branch ready for final architecture review and PR publication.

- [ ] **Step 1: Verify branch scope**

Run `git status --short`, `git diff --stat main...HEAD`, and `git diff --name-only main...HEAD`.

Expected: implementation changes only ARC-P110 and its registry row; the plan file may appear in a separate planning commit.

- [ ] **Step 2: Run the complete validation suite**

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest discover -s tests -v
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
git diff --check main...HEAD
```

Expected: 10 tests pass, 91 controls validate, architecture validation succeeds, and diff checking is clean.

- [ ] **Step 3: Verify structural and semantic invariants**

Confirm all template headings are present; CP1–CP18 each occur exactly once; six layers are named; managed-workforce scope, session-scoped memory, read-oriented connectors, context manifests, final presentation-time authorization, action manifests, accessibility, records snapshots, ARC-P160 evidence, and distinct advisory/action safe-stop rules are explicit; all control IDs resolve.

- [ ] **Step 4: Record verification evidence**

The implementation report records exact commands, exit status, test and validator counts, referenced-control count, CP and heading counts, changed files, and residual concerns. Do not create a tracked file solely for transient verification output.
