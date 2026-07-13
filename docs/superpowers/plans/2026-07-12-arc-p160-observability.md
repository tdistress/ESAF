# ARC-P160 AI Observability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish ARC-P160 as ESAF's vendor-neutral architecture pattern for independent, privacy-tiered AI observability and assurance.

**Architecture:** ARC-P160 is a supporting pattern that combines distributed signal collection with centrally governed telemetry contracts, correlation, privacy, protected evidence, evaluation, detection, response, and assurance. The pattern uses six logical planes, four capture modes, fifteen owned control points, explicit safe-failure behavior, and independently administered evidence.

**Tech Stack:** GitHub Markdown, ESAF-1200 architecture template, Python `unittest`, `tools/validate_controls.py`, and `tools/validate_architectures.py`.

## Global Constraints

- The approved design specification at `docs/superpowers/specs/2026-07-12-arc-p160-observability-design.md` is authoritative.
- Pattern content shall remain vendor-neutral and normative; supplier examples and product configuration are out of scope.
- The monitored runtime may emit events but cannot select, rewrite, suppress, or delete authoritative evidence or assurance verdicts.
- Capture modes are exactly: metadata only; derived signal; redacted excerpt; exceptional protected full content.
- The architecture contains exactly six logical planes and fifteen control points identified `CP1` through `CP15`.
- Tier 3 and Tier 4 consequential activity stops or cannot commit when required authoritative evidence, approval correlation, target outcome, integrity verification, or assurance is unavailable.
- All control identifiers shall resolve against `controls/catalog.json`; catalog `owner_role` remains accountable.
- The pattern shall follow every required section in `architectures/ARCHITECTURE_TEMPLATE.md` and contain no instructional placeholders.
- The registry shall link ARC-P160 and change its state from Proposed to Draft.
- Existing ARC-P100, ARC-P120, and ARC-P130 records and registry states shall not change.

---

### Task 1: Publish the ARC-P160 pattern and registry record

**Files:**
- Create: `architectures/patterns/ARC-P160.md`
- Modify: `architectures/patterns/README.md`

**Interfaces:**
- Consumes: the approved ARC-P160 design specification, `architectures/ARCHITECTURE_TEMPLATE.md`, `architectures/TRUST_ZONES.md`, `architectures/PRINCIPLES.md`, `architectures/PATTERN_SELECTION.md`, and existing ARC-P100, ARC-P120, and ARC-P130 pattern conventions.
- Produces: a registry-linked Draft pattern that the architecture validator recognizes as a complete pattern record.

- [ ] **Step 1: Record the clean pre-change validation state**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest discover -s tests -v
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
```

Expected: 10 unit tests pass; 91 controls, 91 objectives, and 16 families validate; 10 foundation files and 7 reserved patterns validate.

- [ ] **Step 2: Author the complete pattern record**

Create `architectures/patterns/ARC-P160.md` with metadata followed by every heading from `architectures/ARCHITECTURE_TEMPLATE.md`. The record shall include all of the following substantive content from the approved specification:

```text
Metadata: ARC-P160; AI observability; Draft; version 0.1; Enterprise Architecture owner;
Protect AI, Utilize AI, Govern AI; applicable lifecycle stages; capability tiers 0-4;
cloud, hybrid, on-premises, edge/disconnected deployment models.

Architecture decision: independent, privacy-tiered observability and assurance fabric.

Planes: governance and configuration; signal collection; protected evidence;
evaluation and ground truth; detection and response; analytics/service/cost.

Capture modes: metadata only; derived signal; redacted excerpt;
exceptional protected full content.

Control points: CP1 telemetry governance and schema registry through CP15 assurance and reporting,
using the exact purposes and implementation/evidence owners approved in the design specification.

Controls: required, inherited/verified, and conditional allocations exactly as approved in design section 17.

Evidence: the control-point assurance matrix, telemetry coverage and contracts, end-to-end traces,
privacy and tenant tests, integrity and custody tests, provider gap assessment, evaluation and drift evidence,
detection/response evidence, lifecycle tests, continuity exercises, and independent assurance.
```

The architecture views shall include numbered Mermaid context, component/plane, event-flow, and evidence-continuity diagrams. The pattern shall explicitly cover correlation identifiers as untrusted inputs, signing and attestation key lifecycle, separate evidence trust roots, causal ordering and clock uncertainty, derived-signal privacy, ground-truth finality and correction, containment abuse resistance, privileged tenant access, assurance independence, provider evidence gaps, and governed degraded-mode recovery.

- [ ] **Step 3: Link and promote the registry entry**

Change only the ARC-P160 row in `architectures/patterns/README.md` from:

```markdown
| ARC-P160 | AI observability | Proposed |
```

to:

```markdown
| [ARC-P160](ARC-P160.md) | AI observability | Draft |
```

- [ ] **Step 4: Run focused architecture validation**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest discover -s tests -v
& $py tools/validate_architectures.py
```

Expected: all 10 tests pass and architecture validation reports 10 foundation files and 7 reserved patterns with ARC-P160 linked as Draft.

- [ ] **Step 5: Run full semantic and repository checks**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py tools/validate_controls.py --check
git diff --check
rg -n 'TBD|TODO|PLACEHOLDER|lorem ipsum' architectures/patterns/ARC-P160.md
```

Expected: control validation succeeds; `git diff --check` emits no output; placeholder search returns no matches. Independently compare every control ID in ARC-P160 to `controls/catalog.json` and verify all resolve.

- [ ] **Step 6: Self-review against the approved design**

Verify every design section maps to pattern content, all six planes and four capture modes appear, CP1-CP15 appear once in the control-point table, owners are explicit, Tier 3/4 failure semantics are unambiguous, no dashboard is treated as authoritative evidence, and the pattern does not introduce supplier-specific guidance.

- [ ] **Step 7: Commit the implementation**

```powershell
git add architectures/patterns/ARC-P160.md architectures/patterns/README.md
git commit -m 'Publish ARC-P160 AI observability pattern'
```

Expected: one focused commit containing the pattern and registry promotion.

---

### Task 2: Validate the complete implementation branch

**Files:**
- Verify: `architectures/patterns/ARC-P160.md`
- Verify: `architectures/patterns/README.md`
- Verify: `docs/superpowers/specs/2026-07-12-arc-p160-observability-design.md`

**Interfaces:**
- Consumes: Task 1's committed pattern and registry change.
- Produces: complete validation evidence and a branch ready for final architecture review and publication through a pull request.

- [ ] **Step 1: Verify branch scope**

Run:

```powershell
git status --short
git diff --stat main...HEAD
git diff --name-only main...HEAD
```

Expected: the implementation commit changes only `architectures/patterns/ARC-P160.md` and `architectures/patterns/README.md`; the plan file may appear in a separate planning commit.

- [ ] **Step 2: Run the complete validation suite**

Run:

```powershell
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
& $py -m unittest discover -s tests -v
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
git diff --check main...HEAD
```

Expected: 10 unit tests pass, all 91 controls validate, architecture validation succeeds, and the diff check emits no errors.

- [ ] **Step 3: Verify structural invariants**

Run focused searches and confirm:

```powershell
rg -n '^## ' architectures/patterns/ARC-P160.md
rg -n '^\| CP(?:[1-9]|1[0-5]) ' architectures/patterns/ARC-P160.md
rg -n 'metadata only|derived signal|redacted excerpt|exceptional protected full content' architectures/patterns/ARC-P160.md
rg -n 'Tier 3|Tier 4|authoritative evidence|assurance' architectures/patterns/ARC-P160.md
```

Expected: all template headings are present, CP1-CP15 are present, all capture modes are defined, and safe-failure and assurance language is explicit.

- [ ] **Step 4: Record verification evidence**

The implementation report shall record exact commands, exit status, test counts, validator counts, control-ID resolution count, changed files, and any residual concerns. Do not create a repository file solely for transient verification output.
