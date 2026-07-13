# ARC-P140 Private Model Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish ARC-P140 as ESAF's vendor-neutral architecture pattern for enterprise-controlled model acquisition, adaptation, release, custody, deployment, operation, revocation, and retirement.

**Architecture:** ARC-P140 uses a controlled model supply chain and federated serving architecture. It separates acquisition, hostile quarantine, adaptation, validation and release, immutable registry custody, deployment and serving, and independent evidence and operations into seven logical zones joined by explicit promotion gates and 21 control points.

**Tech Stack:** GitHub Markdown, ESAF-1200 architecture template, Mermaid, Python `unittest`, `tools/validate_controls.py`, and `tools/validate_architectures.py`.

## Global Constraints

- The approved design at `docs/superpowers/specs/2026-07-12-arc-p140-private-model-deployment-design.md` is authoritative.
- Scope includes enterprise-operated inference and material adaptation of acquired, open, commercial, or internally developed model weights; it excludes foundation-model pretraining from scratch.
- Enterprise-controlled custody may be implemented on-premises, in private cloud, on dedicated hosted infrastructure, or at isolated edge locations under an explicit field-level shared-responsibility model.
- The architecture contains exactly seven logical zones and 21 control points identified `CP1` through `CP21`.
- Model identity is an immutable release closure that covers every material shard, manifest, tokenizer, vocabulary, template, adapter, draft model, loader, kernel, library, runtime image, safety configuration, precision choice, and hardware, driver, or firmware dependency.
- Model acquisition and transformation use hostile-workload isolation, immutable provenance, transitive license analysis, separated duties, signed promotion, and independently governed trust anchors.
- Inference-only deployments may mark adaptation-specific CP6 and CP7 activities not applicable only when no material transformation occurs; provenance, validation, release, registry, custody, and deployment remain mandatory.
- Runtime egress is denied by default; imports, exports, telemetry, support access, and exceptions use separately governed inspected paths.
- Shared serving is permitted only when risk-tiered isolation, including accelerator and empirical side-channel isolation, is demonstrated; incompatible Tier 4 or legal obligations require dedicated serving.
- Tier 3 and Tier 4 deployments do not silently continue or fail over when model identity, integrity, isolation, validation, authorization, revocation, or required assurance is unknown.
- Rollback is a new deployment decision and may use only a compatible approved target without unresolved vulnerabilities or obligations exceeding approved deployment criteria.
- All control identifiers resolve against `controls/catalog.json`; the catalog `owner_role` remains authoritative for accountability.
- Required, inherited-and-verified, and conditional control allocations remain distinct and match approved design section 19; the conditional range `AGT-100` through `AGT-160` is enumerated as `AGT-100`, `AGT-110`, `AGT-120`, `AGT-130`, `AGT-140`, `AGT-150`, and `AGT-160` so every catalog control resolves literally.
- The pattern follows every required section in `architectures/ARCHITECTURE_TEMPLATE.md`, remains supplier-neutral, and contains no drafting placeholders.
- The registry links ARC-P140 and changes only its state from Proposed to Draft.

---

### Task 1: Publish the ARC-P140 pattern and registry record

**Files:**
- Create: `architectures/patterns/ARC-P140.md`
- Modify: `architectures/patterns/README.md`

**Interfaces:**
- Consumes: the approved ARC-P140 design, architecture template, trust zones, principles, pattern-selection method, and conventions established by ARC-P100, ARC-P110, ARC-P120, ARC-P130, and ARC-P160.
- Produces: a registry-linked Draft architecture pattern that the architecture validator recognizes as a complete record and that future private-model capability designs can select and tailor.

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

Create `architectures/patterns/ARC-P140.md` with metadata followed by every heading from `architectures/ARCHITECTURE_TEMPLATE.md`. Include the approved design requirements below:

```text
Metadata: ARC-P140; Private model deployment; Draft; version 0.1.0; Enterprise Architecture owner;
required security, model, data, legal, privacy, platform, operations, continuity, records, and assurance reviewers;
Protect AI, Utilize AI, and Govern AI pillars; applicable lifecycle stages; capability tiers 1-4,
with isolated Tier 0 experimentation; on-premises, private-cloud, dedicated-hosted, hybrid,
regional, confidential-computing, and disconnected or edge deployment forms.

Architecture decision: controlled model supply chain and federated serving.

Zones: acquisition and intake; quarantine and inspection; adaptation and build;
validation and release; registry and artifact custody; deployment and serving;
evidence and operations.

Control points: CP1 model-source and supplier approval through CP21 evidence,
incident response, and independent assurance, using the approved purpose and
primary implementation/evidence roles in the design.

Controls: required, inherited-and-verified, and conditional allocations exactly as design section 19,
with AGT-100, AGT-110, AGT-120, AGT-130, AGT-140, AGT-150, and AGT-160
enumerated individually rather than represented by a prose range.
```

The record shall include numbered Mermaid context, zone/component, artifact-promotion, deployment/admission, serving, revocation, and retirement views. Prose accompanying the views shall explain custody and shared responsibility rather than treating network placement as proof of privacy or security.

The record shall substantively cover hostile artifact formats and sanitized promotion; release-closure identity and time-of-check/time-of-use protection; transitive licensing and acceptable-use change; adaptation data authority, intermediate-artifact classification, deletion propagation, and unlearning limits; ephemeral hostile-workload isolation for adaptation and validation; independent validation; dual or threshold signing for higher tiers; trust-anchor lifecycle; registry immutability; attestation freshness and anti-replay; privileged-role separation; tenant, adapter, scheduler, cache, accelerator, telemetry, backup, and support isolation; empirical side-channel acceptance thresholds; extraction and distributed-abuse protection; comprehensive deny-by-default egress; independent ARC-P160 evidence; advisory and fleet-impact response; safe-failure matrices; atomic backup and isolated restore; online and offline revocation; edge capture resistance; and verifiable destruction. It shall also include the approved shared, high-assurance, regional, disconnected or edge, adapter-based, confidential-computing, and dedicated-hosted variants; every approved anti-pattern; explicit acceptance criteria; related-pattern responsibilities; and the approved out-of-scope boundary.

- [ ] **Step 3: Link and promote the registry entry**

Change only the ARC-P140 row in `architectures/patterns/README.md` from:

```markdown
| ARC-P140 | Private model deployment | Proposed |
```

to:

```markdown
| [ARC-P140](ARC-P140.md) | Private model deployment | Draft |
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

Expected: all 10 tests pass; architecture validation succeeds with ARC-P140 linked as Draft; 91 controls, 91 objectives, and 16 families validate.

- [ ] **Step 5: Run structural and repository checks**

Run:

```powershell
git diff --check
rg -n 'TBD|TODO|PLACEHOLDER|lorem ipsum' architectures/patterns/ARC-P140.md
$cpLines = @(rg '^\| CP[0-9]+ \|' architectures/patterns/ARC-P140.md)
$cpIds = @($cpLines | ForEach-Object { if ($_ -match '^\| (CP\d+) \|') { $Matches[1] } })
if ($cpIds.Count -ne 21 -or ($cpIds | Sort-Object -Unique).Count -ne 21) {
    throw "Expected 21 unique control points; found $($cpIds.Count) rows and $(($cpIds | Sort-Object -Unique).Count) unique IDs"
}
$templateHeadings = @(Select-String -Path architectures/ARCHITECTURE_TEMPLATE.md -Pattern '^## (.+)$' | ForEach-Object { $_.Matches[0].Groups[1].Value })
$patternHeadings = @(Select-String -Path architectures/patterns/ARC-P140.md -Pattern '^## (.+)$' | ForEach-Object { $_.Matches[0].Groups[1].Value })
$missingHeadings = @($templateHeadings | Where-Object { $_ -notin $patternHeadings })
if ($missingHeadings.Count) { throw "Missing template headings: $($missingHeadings -join ', ')" }
$controlIds = @((Select-String -Path architectures/patterns/ARC-P140.md -Pattern '\b(?:GOV|STR|RSK|IAM|DAT|MOD|APP|API|INF|AGT|OPS|MON|CMP|AUD|EDU|ARC)-\d{3}\b' -AllMatches).Matches.Value | Sort-Object -Unique)
if ($controlIds.Count -ne 91) { throw "Expected 91 unique control references; found $($controlIds.Count)" }
```

Expected: no whitespace or placeholder errors; exactly 21 unique CP rows; every heading required by `architectures/ARCHITECTURE_TEMPLATE.md`; and 91 literal control references. Independently resolve every reference against `controls/catalog.json` and confirm exactly seven named zones.

- [ ] **Step 6: Exercise the approved assessment cases**

Confirm the pattern's evidence and assessment section requires each of these concrete exercises:

```text
hostile artifact and quarantine escape; adaptation or validation exfiltration;
artifact substitution between inspection and load; stale or replayed attestation;
signature, trust, time, and purpose failure; poisoned or contaminated adaptation;
license or acceptable-use change; separation-of-duties violation; shared-serving and
accelerator side-channel leakage; distributed extraction; resource starvation;
IPv4, IPv6, DNS, metadata, mesh, registry, telemetry, crash, support, and approved-sink
egress bypass; provider-admin access or silent substitution; failed rollback and recovery;
edge capture and clock rollback; compromised or ineligible restore; evidence suppression;
expired or orphaned emergency credentials; timed fleet-wide revocation; injected advisory
response; and post-retirement residual-artifact search.
```

Expected: each case has a stated control objective, evidence source, pass/fail basis, and safe-stop or escalation behavior where applicable.

- [ ] **Step 7: Self-review against the approved design**

Verify every design section maps to substantive pattern content; CP6 and CP7 applicability is unambiguous for inference-only deployments; the build, validation, signing, registry, trust-anchor, and deployment roles cannot self-approve across boundaries; the registry record and runtime admission use the same immutable release identity; dedicated hosted deployments have field-level qualification and no silent supplier substitution; risk-tiered shared serving uses empirical isolation evidence; safe failure distinguishes promotion, new load, new inference, continued inference, and resumption; and no product-specific guidance appears.

- [ ] **Step 8: Commit the implementation**

```powershell
git add architectures/patterns/ARC-P140.md architectures/patterns/README.md
git commit -m 'Publish ARC-P140 private model deployment pattern'
```

Expected: one focused implementation commit containing the pattern and registry promotion.

---

### Task 2: Validate the complete implementation branch

**Files:**
- Verify: `architectures/patterns/ARC-P140.md`
- Verify: `architectures/patterns/README.md`
- Verify: `docs/superpowers/specs/2026-07-12-arc-p140-private-model-deployment-design.md`

**Interfaces:**
- Consumes: Task 1's committed pattern and registry change.
- Produces: complete validation evidence and a branch ready for independent architecture and security review and PR publication.

- [ ] **Step 1: Verify branch scope**

Run:

```powershell
git status --short
git diff --stat main...HEAD
git diff --name-only main...HEAD
```

Expected: the implementation commit changes only `architectures/patterns/ARC-P140.md` and `architectures/patterns/README.md`; the plan file may appear in a separate planning commit.

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

Confirm all template headings are present; CP1 through CP21 each appear exactly once; seven zones are named; all 91 catalog controls are referenced literally and retain required, inherited, or conditional status; immutable closure identity, hostile workload isolation, separation of duties, fresh attestation, side-channel testing, deny-by-default egress, fleet advisory response, safe-failure matrices, timed revocation, edge capture, and destruction requirements are explicit; registry status is Draft; and all other pattern states remain unchanged.

- [ ] **Step 4: Request independent reviews**

Request one reviewer to compare the implementation against all approved design sections and control allocations, and a second reviewer to assess trust boundaries, failure semantics, negative tests, and evidence sufficiency. Resolve every Critical or Important finding before publication and document any accepted Minor finding in the PR.

- [ ] **Step 5: Record verification evidence**

The implementation report records exact commands, exit status, test and validator counts, referenced-control count, CP and heading counts, changed files, independent-review results, and residual concerns. Do not create a tracked file solely for transient verification output.
