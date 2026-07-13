# ARC-P160 AI Observability Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Protect the existing ARC-P160 AI observability Draft with focused semantic regression tests and a reproducible four-of-four Mermaid publication gate, correcting only defects proven by those gates.

**Architecture:** Add one pattern-specific `unittest` module that reads ARC-P160, its registry row, the architecture template, and the control catalog. The module protects publication, allocation, architecture, assurance, privacy, tenancy, resilience, and recovery semantics; a separate pinned Mermaid CLI command performs renderer validation. Minimal ARC-P160 wording corrections are allowed only for the user-approved ownership and sensitive-evidence clarifications or defects exposed by a failing gate.

**Tech Stack:** GitHub Markdown, Python `unittest`, Python standard library, ESAF architecture validators, PowerShell, pnpm, and `@mermaid-js/mermaid-cli@11.16.0`.

## Global Constraints

- The approved hardening specification at `docs/superpowers/specs/2026-07-13-arc-p160-hardening-design.md` is authoritative and extends, but does not supersede, `docs/superpowers/specs/2026-07-12-arc-p160-observability-design.md`.
- ARC-P160 remains a vendor-neutral Draft; this milestone does not add products, infrastructure code, dashboards, universal thresholds, crosswalks, profiles, or industry retention schedules.
- The control allocation is exactly 47 required, 4 inherited-and-verified, and 17 conditional controls, totaling 68 of the 91 catalog controls. Every allocated identifier shall resolve in `controls/catalog.json`.
- The architecture contains exactly six logical planes, four capture modes, CP1 through CP15, and four numbered Mermaid figures.
- Source patterns retain event semantics and preventive enforcement; target systems remain authoritative for transaction state; capability owners remain accountable for business outcomes; ARC-P160 produces evidence and assurance without authorizing access or action or transferring catalog accountability.
- Monitored runtimes and ordinary administrators cannot select, suppress, rewrite, or delete authoritative evidence or assurance verdicts.
- Tier 3 and Tier 4 consequential activity stops or remains unable to commit when required evidence, approval correlation, target outcome, integrity verification, or assurance is unknown.
- Unit tests verify Mermaid source structure and known hazards. Renderer validation is separate and uses exactly `@mermaid-js/mermaid-cli@11.16.0` against every diagram.
- Set `PYTHONDONTWRITEBYTECODE=1` for Python validation and leave no `__pycache__`, SVG, temporary rendering, or other generated artifacts in the worktree.
- Do not change ARC-P100 through ARC-P150 or the ARC-P160 registry row unless a separate defect is proven and approved.

---

### Task 1: Establish publication, allocation, and architecture characterization

**Files:**
- Create: `tests/test_arc_p160_pattern.py`
- Read: `architectures/patterns/ARC-P160.md`
- Read: `architectures/patterns/README.md`
- Read: `architectures/ARCHITECTURE_TEMPLATE.md`
- Read: `controls/catalog.json`

**Interfaces:**
- Consumes: the existing ARC-P160 Draft, architecture template, registry, and catalog.
- Produces: reusable `section`, `headings`, and `mermaid_blocks` helpers plus publication, allocation, control-point, capture-mode, relationship, and figure-source tests used by later tasks.

- [ ] **Step 1: Record the clean baseline**

Run the following command with a 180-second outer shell timeout so a stalled renderer fails the publication gate instead of blocking the workflow indefinitely:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest discover -s tests -v
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
git status --short
```

Expected: 27 tests pass; 91 controls, 91 objectives, and 16 families validate; 10 foundation files and 7 reserved patterns validate; status is clean except for committed planning files already on the branch.

- [ ] **Step 2: Create the focused characterization module**

Create `tests/test_arc_p160_pattern.py` with:

```python
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN = ROOT / "architectures" / "patterns" / "ARC-P160.md"
REGISTRY = ROOT / "architectures" / "patterns" / "README.md"
TEMPLATE = ROOT / "architectures" / "ARCHITECTURE_TEMPLATE.md"
CATALOG = ROOT / "controls" / "catalog.json"
CONTROL = re.compile(r"`([A-Z]{3}-\d{3})`")

REQUIRED = {
    "API-110",
    "APP-100", "APP-110", "APP-120", "APP-130", "APP-140", "APP-150",
    "ARC-100", "ARC-110", "ARC-130", "ARC-140",
    "AUD-100", "AUD-110", "AUD-120", "AUD-130", "AUD-140",
    "CMP-100", "CMP-110",
    "DAT-100", "DAT-110", "DAT-120", "DAT-130",
    "GOV-130",
    "IAM-100", "IAM-110", "IAM-120", "IAM-130", "IAM-140", "IAM-150",
    "INF-140", "INF-150",
    "MOD-100", "MOD-120", "MOD-130",
    "MON-100", "MON-110", "MON-120", "MON-140", "MON-150",
    "OPS-100", "OPS-110", "OPS-120", "OPS-130", "OPS-140",
    "RSK-110", "RSK-120", "RSK-140",
}
INHERITED = {"ARC-120", "ARC-150", "OPS-150", "MOD-140"}
CONDITIONAL = {
    "MON-130",
    "DAT-140", "DAT-150", "DAT-160",
    "CMP-120", "CMP-130", "CMP-140",
    "MOD-110", "MOD-150",
    "API-140",
    "AGT-100", "AGT-110", "AGT-120", "AGT-130", "AGT-140", "AGT-150", "AGT-160",
}


def section(text: str, title: str) -> str:
    match = re.search(
        rf"^## {re.escape(title)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Missing section: {title}")
    return match.group(1)


def headings(path: Path, level: int) -> list[str]:
    prefix = "#" * level
    return re.findall(rf"^{prefix} (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)


def mermaid_blocks(text: str) -> list[str]:
    return re.findall(r"```mermaid\n(.*?)\n```", text, re.DOTALL)


class ArcP160PatternTests(unittest.TestCase):
    def text(self) -> str:
        return PATTERN.read_text(encoding="utf-8")

    def test_registry_has_one_exact_arc_p160_draft_row(self) -> None:
        registry = REGISTRY.read_text(encoding="utf-8")
        expected = "| [ARC-P160](ARC-P160.md) | AI observability | Draft |"
        self.assertEqual(1, registry.count(expected))
        self.assertEqual(1, len(re.findall(r"^\| (?:\[)?ARC-P160", registry, re.MULTILINE)))

    def test_required_metadata_is_complete(self) -> None:
        text = self.text()
        for value in (
            "**Pattern ID:** ARC-P160",
            "**Status:** Draft",
            "**Version:** 0.1.0",
            "| Owner | Enterprise Architecture |",
            "| Required reviewers |",
            "| Approval date | Not approved (Draft) |",
            "| Review date |",
            "| Pillars | Protect AI, Utilize AI, Govern AI |",
            "| Lifecycle stages |",
            "| Capability tiers | Tier 0 through Tier 4 |",
            "| Deployment models |",
            "| Primary pattern role |",
            "| Supersedes | None |",
        ):
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_template_headings_are_unique_and_ordered(self) -> None:
        expected = headings(TEMPLATE, 2)
        actual = headings(PATTERN, 2)
        self.assertEqual(expected, actual)
        self.assertEqual(len(actual), len(set(actual)))

    def test_pattern_has_no_drafting_markers(self) -> None:
        text = self.text().lower()
        markers = ("t" + "bd", "t" + "odo", "place" + "holder", "lorem" + " ipsum")
        for marker in markers:
            self.assertNotIn(marker, text)

    def test_control_allocation_is_exact_disjoint_and_resolved(self) -> None:
        allocation = section(self.text(), "Required controls")
        required_table, allocation_notes = allocation.split("\n\n", 1)
        inherited_text, conditional_text = allocation_notes.split("Conditional controls are", 1)
        conditional_text = conditional_text.split("Catalog `owner_role`", 1)[0]

        required = set(CONTROL.findall(required_table))
        inherited = set(CONTROL.findall(inherited_text))
        conditional = set(CONTROL.findall(conditional_text))
        catalog = {
            item["id"]
            for item in json.loads(CATALOG.read_text(encoding="utf-8"))["controls"]
        }

        self.assertEqual((47, 4, 17), (len(required), len(inherited), len(conditional)))
        self.assertEqual(REQUIRED, required)
        self.assertEqual(INHERITED, inherited)
        self.assertEqual(CONDITIONAL, conditional)
        self.assertFalse(required & inherited)
        self.assertFalse(required & conditional)
        self.assertFalse(inherited & conditional)
        self.assertEqual(68, len(required | inherited | conditional))
        self.assertTrue((required | inherited | conditional) <= catalog)
        self.assertEqual(91, len(catalog))

    def test_architecture_structure_and_relationships_are_complete(self) -> None:
        text = self.text()
        lower = text.lower()
        ids = re.findall(r"^\| (CP\d+) \|", text, re.MULTILINE)
        self.assertEqual([f"CP{number}" for number in range(1, 16)], ids)
        self.assertIn("implementation and evidence owners", lower)

        for mode in (
            "metadata only",
            "derived signal",
            "redacted excerpt",
            "exceptional protected full content",
        ):
            self.assertIn(mode, lower)

        diagrams = mermaid_blocks(text)
        self.assertEqual([str(number) for number in range(1, 5)], re.findall(r"^### Figure (\d+)\.", text, re.MULTILINE))
        self.assertEqual(4, len(diagrams))
        rendered_source = "\n".join(diagrams).lower()
        for plane in (
            "1 governance and configuration",
            "2 signal collection",
            "3 protected evidence",
            "4 evaluation and ground truth",
            "5 detection and response",
            "6 analytics, service, and cost",
        ):
            self.assertIn(plane, rendered_source)

        for pattern_id in ("ARC-P100", "ARC-P110", "ARC-P120", "ARC-P130", "ARC-P140", "ARC-P150"):
            self.assertIn(f"`{pattern_id}`", section(text, "Related patterns"))

    def test_mermaid_source_avoids_known_sequence_hazards(self) -> None:
        diagrams = mermaid_blocks(self.text())
        sequence_diagrams = [diagram for diagram in diagrams if diagram.startswith("sequenceDiagram")]
        self.assertGreater(len(sequence_diagrams), 0)
        for diagram in sequence_diagrams:
            for line in diagram.splitlines():
                if ":" in line:
                    with self.subTest(line=line):
                        self.assertNotIn(";", line.split(":", 1)[1])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the focused characterization tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest tests.test_arc_p160_pattern -v
```

Expected: 7 tests pass. If a test fails, classify the failure against design section 7 before changing either the test or pattern.

- [ ] **Step 4: Run architecture and control validators**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
git diff --check
```

Expected: 91 controls, 91 objectives, and 16 families validate; 10 foundation files and 7 reserved patterns validate; diff check emits no output.

- [ ] **Step 5: Commit the characterization suite**

```powershell
git add tests/test_arc_p160_pattern.py
git commit -m "Add ARC-P160 structural regression tests"
```

Expected: one commit containing only the new focused test module.

---

### Task 2: Protect and clarify accountability boundaries

**Files:**
- Modify: `tests/test_arc_p160_pattern.py`
- Modify: `architectures/patterns/ARC-P160.md` in `Related patterns`

**Interfaces:**
- Consumes: Task 1 helpers and the user-approved ownership clarification in hardening design section 5.4.
- Produces: an explicit, test-protected boundary between source-pattern enforcement, target transaction truth, capability accountability, and ARC-P160 evidence production.

- [ ] **Step 1: Add the failing ownership-boundary test**

Add this method to `ArcP160PatternTests`:

```python
    def test_observability_preserves_enforcement_and_accountability_boundaries(self) -> None:
        text = self.text()
        for requirement in (
            "Source patterns remain responsible for their event semantics and preventive enforcement.",
            "Target systems remain authoritative for transaction state.",
            "Capability owners remain accountable for business outcomes.",
            "ARC-P160 produces evidence and assurance; it does not authorize access or action and does not transfer catalog accountability.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)
```

- [ ] **Step 2: Run the focused test and confirm the approved clarification is absent**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest tests.test_arc_p160_pattern.ArcP160PatternTests.test_observability_preserves_enforcement_and_accountability_boundaries -v
```

Expected: FAIL because the four approved sentences are not yet explicit in ARC-P160.

- [ ] **Step 3: Add the minimal normative clarification**

After the ARC-P100 through ARC-P150 bullets in `## Related patterns`, add exactly:

```markdown
Source patterns remain responsible for their event semantics and preventive enforcement. Target systems remain authoritative for transaction state. Capability owners remain accountable for business outcomes. ARC-P160 produces evidence and assurance; it does not authorize access or action and does not transfer catalog accountability.
```

- [ ] **Step 4: Run the focused module**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest tests.test_arc_p160_pattern -v
```

Expected: 8 tests pass.

- [ ] **Step 5: Commit the accountability clarification**

```powershell
git add tests/test_arc_p160_pattern.py architectures/patterns/ARC-P160.md
git commit -m "Clarify ARC-P160 accountability boundaries"
```

Expected: one commit containing the new test and one related-pattern paragraph.

---

### Task 3: Protect assurance independence and sensitive-evidence handling

**Files:**
- Modify: `tests/test_arc_p160_pattern.py`
- Modify: `architectures/patterns/ARC-P160.md` in `Data and instruction flows`

**Interfaces:**
- Consumes: Task 1 helpers and the approved assurance, privacy, tenancy, provider-gap, and ground-truth requirements.
- Produces: tests for authoritative evidence and privacy boundaries plus two narrow wording corrections for Tier 3/4 sampling and response-channel duplication.

- [ ] **Step 1: Add the assurance and privacy tests**

Add these methods to `ArcP160PatternTests`:

```python
    def test_assurance_independence_and_correlation_boundaries_are_explicit(self) -> None:
        text = self.text()
        lower = text.lower()
        for requirement in (
            "Externally supplied correlation identifiers are untrusted inputs.",
            "They never authorize access or action.",
            "Monitored workloads cannot administer authoritative evidence or assurance verdicts.",
            "cannot select, suppress, rewrite or delete authoritative evidence or verdicts",
            "ordinary administrative privilege does not imply cross-tenant evidence access",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement.lower(), lower)

    def test_sensitive_evidence_and_sampling_rules_are_explicit(self) -> None:
        text = self.text()
        for requirement in (
            "Sampling cannot omit denials, incidents, gaps, material decisions, consequential outcomes, or required Tier 3 and Tier 4 outcome records.",
            "Alert payloads reference protected evidence rather than copying sensitive source content.",
            "Alerts, cases, tickets, email, and chat shall not duplicate raw or sensitive source content.",
            "Derived signals, including embeddings, stable hashes and rare features, are classified and tested for re-identification and linkability.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_tenant_provider_and_ground_truth_boundaries_are_explicit(self) -> None:
        text = self.text().lower()
        for requirement in (
            "tenant identity shall be bound at the source and independently validated at ingestion",
            "cross-tenant support or break-glass access requires dual authorization",
            "provider evidence remains externally asserted unless independently corroborated",
            "the affected tier, action, or provider use is prohibited rather than represented as observable",
            "operational dashboards and aggregates remain traceable conveniences, never authoritative evidence",
            "model self-evaluation as authoritative evidence",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)
```

- [ ] **Step 2: Run the two tests containing approved wording corrections**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest tests.test_arc_p160_pattern.ArcP160PatternTests.test_sensitive_evidence_and_sampling_rules_are_explicit -v
```

Expected: FAIL on the Tier 3/4 sampling sentence and the response-channel duplication sentence; existing derived-signal and alert-reference assertions pass.

- [ ] **Step 3: Correct the sampling sentence**

In `## Data and instruction flows`, replace:

```markdown
Sampling cannot omit denials, incidents, gaps, material decisions, or consequential outcomes.
```

with:

```markdown
Sampling cannot omit denials, incidents, gaps, material decisions, consequential outcomes, or required Tier 3 and Tier 4 outcome records.
```

- [ ] **Step 4: Add the response-channel minimization sentence**

Immediately after the sentence `Alert payloads reference protected evidence rather than copying sensitive source content.`, add:

```markdown
Alerts, cases, tickets, email, and chat shall not duplicate raw or sensitive source content.
```

- [ ] **Step 5: Run the focused module**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest tests.test_arc_p160_pattern -v
```

Expected: 11 tests pass.

- [ ] **Step 6: Commit the assurance and privacy hardening**

```powershell
git add tests/test_arc_p160_pattern.py architectures/patterns/ARC-P160.md
git commit -m "Harden ARC-P160 evidence handling requirements"
```

Expected: one commit containing three semantic tests and two narrow pattern corrections.

---

### Task 4: Protect resilience, safe-stop, and recovery semantics

**Files:**
- Modify: `tests/test_arc_p160_pattern.py`
- Modify if a confirmed defect is found: `architectures/patterns/ARC-P160.md`

**Interfaces:**
- Consumes: Task 1 helpers and the existing ARC-P160 failure, degraded-mode, and recovery requirements.
- Produces: characterization tests for failure treatment, Tier 3/4 safe stop, bounded lower-tier operation, and governed recovery.

- [ ] **Step 1: Add the resilience and recovery tests**

Add these methods to `ArcP160PatternTests`:

```python
    def test_failure_and_abuse_treatment_is_complete(self) -> None:
        text = self.text().lower()
        for requirement in (
            "spoofed source",
            "correlation collision",
            "replay",
            "schema drift",
            "telemetry injection",
            "clock regression",
            "late, duplicate, missing, or out-of-order event",
            "signing key compromise",
            "privileged evidence alteration",
            "provider export delay",
            "alert poisoning",
            "suppression abuse",
            "containment abuse",
            "evidence integrity failure",
            "routing and backpressure failure",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_tier_three_and_four_safe_stop_is_explicit(self) -> None:
        text = self.text()
        for requirement in (
            "Stop Tier 3 and Tier 4 consequential commit and dependent activity; do not report success",
            "Missing tenant binding, unverifiable telemetry, privacy-policy failure, expiry, or buffer exhaustion causes fail-safe rejection.",
            "Monitoring failure cannot bypass enforcement.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_degraded_operation_and_recovery_are_bounded(self) -> None:
        text = self.text()
        for requirement in (
            "Lower-tier operation may enter only a preapproved degraded mode with protected local buffering, explicit duration and volume, visible status, and no increase in data, authority, provider, or action scope.",
            "Recovery validates signed backfill, sequence reconciliation, integrity and custody, gap disposition, privacy obligations, material incident review, and authorized return to normal.",
            "Applicability matrices define commit-blocking evidence, source, tolerated delay, degraded state, recovery condition, and change authority for each capability and action class.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)
```

- [ ] **Step 2: Run the new resilience tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest `
  tests.test_arc_p160_pattern.ArcP160PatternTests.test_failure_and_abuse_treatment_is_complete `
  tests.test_arc_p160_pattern.ArcP160PatternTests.test_tier_three_and_four_safe_stop_is_explicit `
  tests.test_arc_p160_pattern.ArcP160PatternTests.test_degraded_operation_and_recovery_are_bounded -v
```

Expected: all 3 tests pass against the current ARC-P160 Draft. Any failure is unexpected and must be classified before modifying the pattern.

- [ ] **Step 3: Run the complete focused module**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest tests.test_arc_p160_pattern -v
```

Expected: 14 tests pass.

- [ ] **Step 4: Commit the resilience characterization**

```powershell
git add tests/test_arc_p160_pattern.py
git commit -m "Protect ARC-P160 resilience requirements"
```

Expected: one commit containing only the three resilience and recovery tests unless a separately classified defect required a minimal pattern correction.

---

### Task 5: Execute the renderer and repository publication gates

**Files:**
- Verify: `architectures/patterns/ARC-P160.md`
- Verify: `tests/test_arc_p160_pattern.py`
- Verify: `docs/superpowers/specs/2026-07-13-arc-p160-hardening-design.md`
- Verify: `docs/superpowers/plans/2026-07-13-arc-p160-hardening.md`

**Interfaces:**
- Consumes: Tasks 1 through 4 and the pinned Mermaid publication contract.
- Produces: exact validation evidence for whole-branch review and the pull-request description.

- [ ] **Step 1: Render all four Mermaid figures with the pinned CLI**

Run:

```powershell
$env:PATH = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin;' + $env:PATH
$text = Get-Content -LiteralPath 'architectures\patterns\ARC-P160.md' -Raw
$matches = [regex]::Matches($text, '(?s)```mermaid\r?\n(.*?)\r?\n```')
if ($matches.Count -ne 4) { throw "Expected 4 Mermaid diagrams, found $($matches.Count)" }

$outDir = Join-Path $env:TEMP 'esaf-arc-p160-mermaid'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$results = @()
try {
  for ($i = 0; $i -lt $matches.Count; $i++) {
    $out = Join-Path $outDir ("figure-{0}.svg" -f ($i + 1))
    if (Test-Path -LiteralPath $out) { Remove-Item -LiteralPath $out -Force }
    $matches[$i].Groups[1].Value | & 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd' dlx @mermaid-js/mermaid-cli@11.16.0 -i - -o $out 2>&1 | Out-Null
    $results += [pscustomobject]@{
      Figure = $i + 1
      Exit = $LASTEXITCODE
      Rendered = Test-Path -LiteralPath $out
      Bytes = if (Test-Path -LiteralPath $out) { (Get-Item -LiteralPath $out).Length } else { 0 }
    }
  }
  $results | ConvertTo-Json -Compress
  $failed = @($results | Where-Object { $_.Exit -ne 0 -or -not $_.Rendered -or $_.Bytes -le 0 })
  if ($failed.Count -gt 0) { throw "Mermaid rendering failed: $($failed | ConvertTo-Json -Compress)" }
}
finally {
  if (Test-Path -LiteralPath $outDir) { Remove-Item -LiteralPath $outDir -Recurse -Force }
}
```

Expected: four result objects report `Exit: 0`, `Rendered: true`, and `Bytes` greater than zero; the temporary directory is removed.

- [ ] **Step 2: Run all focused and repository validation**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'C:\Users\phrea\Documents\Codex\2026-07-11\referenced-chatgpt-conversation-this-is-untrusted\work\.validation-deps'
$py = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py -m unittest tests.test_arc_p160_pattern -v
& $py -m unittest discover -s tests -v
& $py tools/validate_controls.py --check
& $py tools/validate_architectures.py
git diff --check main...HEAD
```

Expected: 14 ARC-P160 tests and 41 total tests pass; 91 controls, 91 objectives, and 16 families validate; 10 foundation files and 7 reserved patterns validate; diff check emits no output.

- [ ] **Step 3: Verify branch scope and cleanliness**

Run:

```powershell
git diff --name-only main...HEAD
git status --short
$cacheDirs = @(Get-ChildItem -Path . -Directory -Recurse -Filter '__pycache__')
if ($cacheDirs.Count -gt 0) { throw "Unexpected Python caches: $($cacheDirs.FullName -join ', ')" }
```

Expected implementation files: `architectures/patterns/ARC-P160.md` and `tests/test_arc_p160_pattern.py`; the approved design and plan appear as planning commits. Status is clean and no cache directories exist.

- [ ] **Step 4: Complete independent whole-branch review**

The reviewer shall compare `main...HEAD` to both ARC-P160 design specifications and this implementation plan, inspect every test assertion for traceability, verify that only approved clarifications changed normative content, and classify findings as Critical, Important, or Minor.

Expected: no unresolved Critical or Important findings. Any fix changes the reviewed head SHA and requires proportional reruns plus final re-review.

- [ ] **Step 5: Prepare the pull-request evidence**

Record in the PR body:

```text
- 14 ARC-P160 focused tests and 41 total tests passed
- 91 controls, 91 objectives, and 16 families validated
- 10 architecture foundation files and 7 reserved patterns validated
- Mermaid CLI 11.16.0 rendered all four ARC-P160 figures successfully (4/4)
- no unresolved Critical or Important findings
```

Record and verify the reviewed SHA with:

```powershell
$reviewedSha = git rev-parse HEAD
$prNumber = gh pr view --json number --jq .number
$headSha = gh pr view $prNumber --json headRefOid --jq .headRefOid
Write-Output "- reviewed commit: $reviewedSha"
if ($reviewedSha -ne $headSha) { throw "Reviewed SHA $reviewedSha does not match PR head $headSha" }
```

Before merge, also verify GitHub checks pass, review is not blocked, and merge state is `CLEAN`.

- [ ] **Step 6: Merge and validate `main`**

After merge, update local `main` and rerun the full suite, both validators, Mermaid 4/4 rendering, cache check, and `git status --short`. Remove the temporary implementation branch and worktree only after post-merge validation passes.
