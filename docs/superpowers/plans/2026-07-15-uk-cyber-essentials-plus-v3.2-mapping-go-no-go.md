# UK Cyber Essentials Plus v3.2 Mapping Go/No-Go Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce two independently reasoned, machine-validated `GO`, `HOLD`, or `NO_GO` feasibility decisions for mapping ESAF 0.4-alpha and the pinned public Cyber Essentials Plus v3.2 oracle without creating a mapping snapshot.

**Architecture:** Repair and regression-lock the source-inventory digest evidence first, then commit an independent rights re-attestation before any feasibility analysis. Two isolated directional analysts produce temporary probe sets that a reconciler converts into one closed JSON matrix; a deterministic renderer produces the human-readable decision record, and focused tests enforce coverage, disposition mechanics, independence, overclaiming boundaries, and the absence of authoritative mapping artifacts.

**Tech Stack:** Python 3 `unittest`, JSON, Markdown, SHA-256, Git history, existing ESAF validators, GitHub Actions.

## Global Constraints

- The only external decision universe is the locked 144-provision public NCSC Cyber Essentials Plus Test Specification v3.2 oracle.
- The LF-normalized tracked-byte oracle SHA-256 is `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
- Assess `esaf_to_external` and `external_to_esaf` independently and in that order.
- Each direction receives exactly one mechanically derived disposition: `GO`, `HOLD`, or `NO_GO`.
- A `GO` authorizes only a separate direction-specific mapping design, never mapping implementation.
- Current operational changes, core v3.3, Delivery Partner practices, and IASME material are context only and shall not supply missing outcomes or expand the decision universe.
- Positive feasibility requires exact normative ESAF `shall` text through a stable control identifier and requirement locator.
- Conditions may narrow a prospective relationship but shall not create a missing external or ESAF outcome.
- No file beneath `crosswalks/mappings/` or `crosswalks/registry/` may change.
- No mapping snapshot, lifecycle record, provision mapping record, relationship leg, control manifest, generated mapping statistic, or authoritative mapping taxonomy field may be created.
- The NCSC/OGL publication basis and IASME rights partition remain separate; copied source passages remain prohibited.
- The anomaly shall be referenced only by identifier and oracle path; its source literal shall not be copied into new artifacts.
- Python validation shall set `PYTHONDONTWRITEBYTECODE=1` and leave no cache, source-download, rendering, analyst scratch, or generated drift in the repository.
- Any candidate change invalidates prior exact-head reviews and requires all final gates and both reviews to be rerun.

---

### Task 1: Repair and regression-lock source-inventory artifact digests

**Files:**
- Create: `tests/test_uk_cyber_essentials_plus_v32_traceability.py`
- Modify: `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-traceability.md`

**Interfaces:**
- Consumes: the six tracked artifact digest rows in the source-inventory traceability table.
- Produces: `SourceInventoryTraceabilityTests`, `TRACKED_ARTIFACTS`, and one platform-independent LF-normalized digest invariant used as a prerequisite by later tasks.

- [ ] **Step 1: Write the failing digest-table regression**

Create the focused test with this structure and exact tracked labels:

```python
from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACEABILITY = ROOT / "docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-traceability.md"
TRACKED_ARTIFACTS = {
    "Locked oracle": ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json",
    "Tracked reconciliation record": ROOT / "docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-inventory-reconciliation.md",
    "Rights review and R2 re-attestation": ROOT / "docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md",
    "Focused inventory contract test": ROOT / "tests/test_uk_cyber_essentials_plus_v32_inventory.py",
    "Focused link-validator test": ROOT / "tests/test_validate_links.py",
    "Link validator": ROOT / "tools/validate_links.py",
}


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


class SourceInventoryTraceabilityTests(unittest.TestCase):
    def test_tracked_artifact_digests_match_lf_normalized_bytes(self) -> None:
        text = TRACEABILITY.read_text(encoding="utf-8")
        for label, path in TRACKED_ARTIFACTS.items():
            match = re.search(
                rf"\| {re.escape(label)} \| SHA-256 `([0-9a-f]{{64}})` \|",
                text,
            )
            self.assertIsNotNone(match, label)
            self.assertEqual(normalized_sha256(path), match.group(1), label)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_traceability -v
```

Expected: one failure for `Locked oracle`, with actual digest `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc` and recorded digest `096a5c1238b92250b1497e76ef175b6b8e99f05a65a21ed66263f8b1cf68578a`.

- [ ] **Step 3: Correct only the stale oracle digest**

Replace the `Locked oracle` table value with:

```text
8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc
```

Do not change the oracle or any other recorded digest.

- [ ] **Step 4: Run focused and source-inventory tests and verify GREEN**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_traceability tests.test_uk_cyber_essentials_plus_v32_inventory -v
git diff --check
```

Expected: 21 tests pass, no digest mismatch, and no whitespace errors.

- [ ] **Step 5: Commit the traceability repair**

```powershell
git add tests/test_uk_cyber_essentials_plus_v32_traceability.py docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-traceability.md
git commit -m "Repair Cyber Essentials Plus oracle traceability"
```

---

### Task 2: Lock and commit the pre-analysis rights gate

**Files:**
- Create first: `tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py`
- Create in a later, rights-only commit: `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-rights-re-attestation.md`
- Expected later: `docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json`

**Interfaces:**
- Consumes: prior rights commit `6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6`, oracle digest, and approved field classes from the design.
- Produces: `MappingGoNoGoTests`, rights-record constants, and an independently approved rights-only ancestor commit required by Task 4.

- [ ] **Step 1: Write the failing rights-sequencing contract**

Start the test module with:

```python
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RIGHTS = ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-rights-re-attestation.md"
MATRIX = ROOT / "docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json"
REVIEW = ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md"
ORACLE_SHA256 = "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc"
PRIOR_RIGHTS_COMMIT = "6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6"
FIELD_CLASSES = (
    "source_oracle_identity",
    "provision_identifiers_and_structural_classifications",
    "original_probe_selection_rationales",
    "derivative_mapping_analysis",
    "esaf_normative_citations",
    "assurance_and_overclaiming_analysis",
    "official_links",
    "directional_gate_and_decision_metadata",
)


class MappingGoNoGoTests(unittest.TestCase):
    def test_rights_re_attestation_exists_before_analysis(self) -> None:
        self.assertTrue(RIGHTS.is_file())

    def test_rights_re_attestation_contract_is_exact(self) -> None:
        text = RIGHTS.read_text(encoding="utf-8")
        self.assertIn(f"`{ORACLE_SHA256}`", text)
        self.assertIn(f"`{PRIOR_RIGHTS_COMMIT}`", text)
        self.assertIn("**Disposition:** Approved", text)
        for field_class in FIELD_CLASSES:
            self.assertIn(f"`{field_class}`", text)
        self.assertIn("**IASME partition preserved:** yes", text)
        self.assertIn("**Copied-source prohibition preserved:** yes", text)
```

Add a helper that computes the LF-normalized oracle digest and a test requiring exact equality with `ORACLE_SHA256`.

- [ ] **Step 2: Run the focused module and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go -v
```

Expected: failure because the rights re-attestation file does not exist. Import, syntax, and path errors are not valid RED evidence.

- [ ] **Step 3: Commit the failing non-source-derived contract**

```powershell
git add tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py
git commit -m "Test Cyber Essentials Plus mapping feasibility rights gate"
```

- [ ] **Step 4: Obtain independent rights re-attestation**

Dispatch a rights reviewer who is not either future directional analyst. The reviewer shall verify the exact oracle digest, prior rights commit, all eight field classes, OGL coverage, original-paraphrase boundary, anomaly non-duplication, IASME partition, marks and third-party exclusions, and absence of endorsement implications.

The re-attestation shall use these exact headings and fields:

```markdown
# Cyber Essentials Plus v3.2 Mapping Feasibility Rights Re-attestation

**Reviewer:** Codex Mapping Feasibility Rights Reviewer R1
**Review date:** 2026-07-15
**Prior rights commit:** `6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6`
**Oracle SHA-256:** `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`
**IASME partition preserved:** yes
**Copied-source prohibition preserved:** yes
**Disposition:** Approved

## Approved field classes
```

List all eight `FIELD_CLASSES` values exactly. Record evidence for every confirmation and reject the work if approval is conditional.

- [ ] **Step 5: Commit only the approved rights record**

Verify the staged set contains one file, then commit:

```powershell
git add docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-rights-re-attestation.md
$staged = @(git diff --cached --name-only)
if ($staged.Count -ne 1) { throw "Rights commit contains unexpected files" }
git commit -m "Approve Cyber Essentials Plus mapping feasibility rights"
```

- [ ] **Step 6: Run the rights contract and verify GREEN**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go -v
```

Expected: the initial rights and digest tests pass while no matrix or review artifact exists.

---

### Task 3: Lock the matrix, renderer, and decision mechanics in failing tests

**Files:**
- Modify: `tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py`
- Create: `tools/render_ce_plus_mapping_go_no_go.py`
- Create: `tests/test_render_ce_plus_mapping_go_no_go.py`
- Expected later: matrix and review paths from Task 2

**Interfaces:**
- Consumes: the approved rights record and the locked oracle.
- Produces: closed-contract helpers, deterministic `render(matrix: dict) -> str`, and validation expectations used by Task 4.

- [ ] **Step 1: Add closed-contract constants**

Add these exact constants to the go/no-go test module:

```python
DIRECTIONS = ("esaf_to_external", "external_to_esaf")
DISPOSITIONS = {"GO", "HOLD", "NO_GO"}
GATES = ("source", "rights", "semantic", "normative_basis", "schema", "overclaiming", "utility")
GATE_STATUSES = {"PASS", "BLOCKED", "FAIL"}
GROUPS = ("M", "T1", "S", "T2", "T3", "T4", "T5", "C", "A", "B")
KINDS = (
    "applicability", "prerequisite", "procedure_step", "decision_rule",
    "result_rule", "evidence_retention", "recommendation",
)
ACTORS = ("Assessor", "Applicant", "Certification Body", "Certifying Body", "Delivery Partner")
SCENARIOS = (
    "figure-1-decision-logic",
    "sampling-and-population-limits",
    "evidence-retention",
    "complete-assessment-file-coverage",
    "delivery-partner-discretionary-exception",
    "known-source-anomaly",
    "point-in-time-versus-continuous-assurance",
    "core-v3.3-versus-plus-v3.2-separation",
    "expected-no-direct-esaf-basis",
)
PROBE_CONCLUSIONS = {"POSITIVE_FEASIBILITY", "NO_POSITIVE_BASIS", "INDETERMINATE"}
CONDITION_STATUSES = {"SATISFIED", "NOT_APPLICABLE"}
EXTERNAL_TO_ESAF_CONDITIONS = (
    "actor", "scope", "population", "sample", "assessment_date", "evidence_date",
    "tool", "provenance", "exception", "delivery_partner_discretion",
    "point_in_time_status",
)
PROHIBITED_KEYS = {
    "relationship", "relationships", "coverage", "confidence", "mapping_disposition",
    "snapshot_digest", "lifecycle", "mapper", "approver",
}
```

- [ ] **Step 2: Add matrix-absence RED and complete semantic tests**

Add tests that require:

- exact top-level keys and schema/review identifier values from design section 10.1;
- exact nested key sets for source, rights, roles, coverage, analysis provenance, immutable submissions, assessments, prerequisites, reconsideration triggers, gates, probes, scenario bindings, condition entries, and normative bases;
- exact direction order, unique role identities, rights reviewer independence, and direction-ordered analyst submission identities;
- the rights record commit to change only the rights file and precede the first probe commit;
- four true closed isolation attestations, two unique immutable submission digests/timestamps/references, and reconciliation evidence that references both submission digest references;
- exact gate, group, kind, actor, scenario, status, disposition, and conclusion sets;
- valid provision IDs and derived group/kind/actor values from the oracle;
- valid control IDs and normative requirement locators resolved from the pinned ESAF control files;
- every group, kind, and actor derived from direction-local probes and every special scenario derived from a valid same-probe binding, independently per direction;
- each scenario binding to use exactly its probe's scenario identifier, nonempty provision IDs, and resolving oracle paths; assert every direction against every row of the closed binding oracle in design section 8.2, including `known-source-anomaly` at `known_anomalies[0]` / `cepts32-anomaly-001` and the exact named `assurance_limits` fields, never label unions;
- `POSITIVE_FEASIBILITY` to have at least one normative basis;
- every `external_to_esaf` positive probe to have the exact ordered 11-condition checklist, accepted status, and nonempty resolving evidence references, while every other probe has an empty checklist;
- `NO_POSITIVE_BASIS` to name the missing outcome;
- `INDETERMINATE` to link a nonempty prerequisite;
- `positive_probe_identifiers` to equal the ordered positive probe IDs derived directly for that direction, and exact disposition/prerequisite/reconsideration-trigger mechanics from design section 7, including `BLOCKED` for every unresolved disagreement;
- recursive absence of `PROHIBITED_KEYS` and prohibited claim phrases;
- no anomaly source literal in the matrix or review;
- no changed path beneath mapping or registry roots relative to the implementation merge base; and
- review headings, gate values, dispositions, and totals to equal values derived from the matrix.

Use helper functions with these signatures:

```python
def assert_exact_keys(
    test: unittest.TestCase,
    obj: dict,
    expected: set[str],
    context: str,
) -> None:
    test.assertEqual(expected, set(obj), context)


def recursive_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            key
            for child in value.values()
            for key in recursive_keys(child)
        }
    if isinstance(value, list):
        return {
            key
            for child in value
            for key in recursive_keys(child)
        }
    return set()


def derive_coverage(matrix: dict, direction: str) -> dict[str, set[str]]:
    selected = [probe for probe in matrix["probes"] if probe["direction"] == direction]
    return {
        "groups": {value for probe in selected for value in probe["groups"]},
        "kinds": {value for probe in selected for value in probe["kinds"]},
        "actors": {value for probe in selected for value in probe["actors"]},
        "special_scenarios": {
            binding["scenario_id"]
            for probe in selected
            for binding in probe["special_scenario_bindings"]
        },
    }


def expected_disposition(
    assessment: dict,
    probes_by_id: dict[str, dict],
) -> str:
    statuses = {gate["status"] for gate in assessment["gate_results"]}
    derived_positive = [
        probe_id
        for probe_id, probe in probes_by_id.items()
        if probe["direction"] == assessment["direction"]
        and probe["conclusion"] == "POSITIVE_FEASIBILITY"
    ]
    if derived_positive != assessment["positive_probe_identifiers"]:
        raise ValueError("positive_probe_identifiers do not equal derived positive probes")
    if "FAIL" in statuses:
        return "NO_GO"
    if "BLOCKED" in statuses:
        return "HOLD"
    return "GO" if derived_positive else "NO_GO"
```

Also assert: `GO` has empty prerequisites and triggers; `HOLD` has nonempty externally resolvable prerequisites and empty triggers; `NO_GO` has empty prerequisites and nonempty reconsideration triggers.

- [ ] **Step 3: Run the focused suite and verify matrix RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go -v
```

Expected: rights tests pass and matrix-dependent tests fail only because the matrix and rendered review are absent.

- [ ] **Step 4: Write renderer tests RED**

Create renderer tests with a minimal valid fixture containing both directions. Require:

```python
from tools.render_ce_plus_mapping_go_no_go import render

class RenderMappingGoNoGoTests(unittest.TestCase):
    def test_render_is_deterministic_and_derived(self) -> None:
        first = render(self.fixture())
        second = render(self.fixture())
        self.assertEqual(first, second)
        self.assertIn("No mapping snapshot exists", first)
        self.assertIn("design only", first)
        for label in ("Groups", "Kinds", "Actors", "Special scenarios"):
            self.assertIn(label, first)
        for direction in DIRECTIONS:
            selected = [p for p in self.fixture()["probes"] if p["direction"] == direction]
            expected = {
                "Groups": len({v for p in selected for v in p["groups"]}),
                "Kinds": len({v for p in selected for v in p["kinds"]}),
                "Actors": len({v for p in selected for v in p["actors"]}),
                "Special scenarios": len({
                    b["scenario_id"] for p in selected
                    for b in p["special_scenario_bindings"]
                }),
            }
            section = first.split(f"## {direction}", 1)[1].split("## ", 1)[0]
            for label, total in expected.items():
                self.assertIn(f"| {label} | {total} |", section)

    def test_render_rejects_unknown_direction(self) -> None:
        fixture = self.fixture()
        fixture["direction_assessments"][0]["direction"] = "bidirectional"
        with self.assertRaisesRegex(ValueError, "unexpected direction order"):
            render(fixture)
```

Run and expect import failure because the renderer does not exist.

- [ ] **Step 5: Implement the minimal deterministic renderer**

Create:

```python
from __future__ import annotations

from collections import Counter

DIRECTIONS = ("esaf_to_external", "external_to_esaf")


def render(matrix: dict) -> str:
    assessments = matrix["direction_assessments"]
    if tuple(item["direction"] for item in assessments) != DIRECTIONS:
        raise ValueError("unexpected direction order")
    probes = matrix["probes"]
    lines = [
        "# Cyber Essentials Plus v3.2 Mapping Go/No-Go Review",
        "",
        "**Boundary:** No mapping snapshot exists. A GO authorizes design only.",
        "",
    ]
    for assessment in assessments:
        direction = assessment["direction"]
        selected = [probe for probe in probes if probe["direction"] == direction]
        counts = Counter(probe["conclusion"] for probe in selected)
        coverage = {
            "Groups": {value for probe in selected for value in probe["groups"]},
            "Kinds": {value for probe in selected for value in probe["kinds"]},
            "Actors": {value for probe in selected for value in probe["actors"]},
            "Special scenarios": {
                binding["scenario_id"]
                for probe in selected
                for binding in probe["special_scenario_bindings"]
            },
        }
        lines.extend([
            f"## {direction}",
            "",
            f"**Disposition:** {assessment['disposition']}",
            "",
            assessment["decision_rationale"],
            "",
            "| Gate | Status |",
            "|---|---|",
            *[f"| `{gate['gate']}` | `{gate['status']}` |" for gate in assessment["gate_results"]],
            "",
            f"Probes: {len(selected)}; positive: {counts['POSITIVE_FEASIBILITY']}; "
            f"no positive basis: {counts['NO_POSITIVE_BASIS']}; indeterminate: {counts['INDETERMINATE']}.",
            "",
            "| Coverage axis | Derived total |",
            "|---|---:|",
            *[f"| {label} | {len(values)} |" for label, values in coverage.items()],
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"
```

Add a CLI accepting `--matrix`, `--output`, and mutually exclusive `--check` / `--write`. `--check` shall compare exact UTF-8 bytes and exit 1 on drift; operational errors exit 2.

- [ ] **Step 6: Run renderer tests GREEN and commit the contract**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_render_ce_plus_mapping_go_no_go -v
python -m unittest tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go -v
```

Expected: renderer tests pass; matrix tests remain RED only for absent implementation artifacts.

Commit:

```powershell
git add tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py tests/test_render_ce_plus_mapping_go_no_go.py tools/render_ce_plus_mapping_go_no_go.py
git commit -m "Test Cyber Essentials Plus mapping feasibility contract"
```

---

### Task 4: Independently analyze both directions and reconcile the matrix

**Files:**
- Create: `docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json`
- Create by renderer: `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md`
- Create outside repository in isolated system-temp children: `esaf-to-external-analysis.json`, `external-to-esaf-analysis.json`, immutable submission attestations, analyst ledgers, and reconciliation comparison

**Interfaces:**
- Consumes: locked contract, rights-only ancestor commit, oracle, ESAF controls, and ESAF-1600.
- Produces: the canonical closed matrix and byte-derived review record used by Task 5.

- [ ] **Step 1: Create and verify isolated system-temporary workspaces**

Create a unique coordination child of `[System.IO.Path]::GetTempPath()` and two distinct analyst output children that are not readable or listable by the other analyst process. Resolve the temp root, all children, and repository root with `GetFullPath`; require every child prefix to be beneath temp and outside the repository. Verify the process or permission boundary with an attempted cross-child read from each analyst context and require both attempts to fail. Record resolved paths and command evidence only outside the repository; the matrix records the four closed boolean isolation attestations, not paths.

- [ ] **Step 2: Prove rights ancestry before analysis**

Read the rights-record commit, require it to change only the rights file, and run:

```powershell
git merge-base --is-ancestor $rightsCommit HEAD
if ($LASTEXITCODE -ne 0) { throw "Rights re-attestation is not an ancestor" }
```

Stop if the record is conditional, rejected, or missing any field class.

- [ ] **Step 3: Dispatch the ESAF-to-external analyst**

The analyst receives the design, oracle, controls, methodology, closed contract, and only their verified temporary output child. They shall answer only the section 5.1 question, cover every group/kind/actor/scenario for their direction, create deterministic provision/anomaly/assurance-limit bindings for every scenario, and produce provisional gates and probes. They shall not see or list the other analyst's output or conclusion.

- [ ] **Step 4: Dispatch the external-to-ESAF analyst independently**

The second analyst receives the same common inputs but only the section 5.2 question and their separately protected temporary output child. They shall not see or list the first analyst's output, conclusion, probe count, or gate statuses. Each positive probe shall include the exact ordered condition checklist for actor, scope, population, sample, assessment date, evidence date, tool, provenance, exception, Delivery Partner discretion, and point-in-time status, with a status and resolving evidence for every entry.

- [ ] **Step 5: Seal and attest both submissions before comparison**

In each isolated analyst context, serialize the final submission deterministically, compute SHA-256 over the exact bytes, record UTC submission time and the no-other-output-visible attestation, then remove analyst write permission or copy the bytes to a reconciler-owned immutable location. Assign a unique digest reference. Verify the sealed digest immediately before reconciliation. Any correction creates a new timestamped submission with `supersedes_digest_reference`; never overwrite submitted bytes.

- [ ] **Step 6: Validate both temporary analyses before comparison**

For each sealed file, verify its recorded digest, exact direction, seven ordered gates, complete direction-local coverage axes, valid deterministic special-scenario bindings, valid oracle provisions, valid ESAF control locators, external-to-ESAF positive condition checklists, conclusion preconditions, absence of prohibited keys and claims, and analyst identity distinctness. Derive its positive IDs from its probes. Do not average or select a conclusion yet.

- [ ] **Step 7: Reconcile every issue into the canonical matrix**

Only after both submissions are sealed, give the reconciler read access to both immutable copies. Generate a comparison by submission digest reference, provision selection, coverage axes, normative basis, semantic conclusion, assurance risk, gate status, prerequisite, and disposition. Record every correction and its source evidence in temporary reconciliation output. Any unresolved disagreement shall set the affected canonical gate to `BLOCKED`, create an externally resolvable prerequisite, and therefore derive `HOLD`.

The reconciler shall create the top-level matrix with exact key sets from the design. `rights_re_attestation.record_commit` shall be the actual 40-character rights commit. The matrix shall record the two analyst identities, a distinct reconciler, the four isolation attestations, both immutable submission records, and reconciliation evidence references to both submission digests. Derive `positive_probe_identifiers`, disposition, prerequisite emptiness/nonemptiness, and trigger emptiness/nonemptiness mechanically; do not copy provisional declarations.

- [ ] **Step 8: Render the review record**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python tools/render_ce_plus_mapping_go_no_go.py --matrix docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json --output docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md --write
```

- [ ] **Step 9: Run all focused tests GREEN**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_traceability tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go tests.test_render_ce_plus_mapping_go_no_go -v
python tools/render_ce_plus_mapping_go_no_go.py --matrix docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json --output docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md --check
```

Expected: all focused tests pass and the rendered record is current.

- [ ] **Step 10: Commit the reconciled decision artifacts**

```powershell
git add docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md
git commit -m "Decide Cyber Essentials Plus mapping feasibility"
```

---

### Task 5: Publish traceability and queue only authorized next work

**Files:**
- Create: `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-traceability.md`
- Modify: `crosswalks/uk-cyber-essentials.md`
- Modify: `project/BACKLOG.md`
- Modify: `tests/test_release_metadata.py`
- Modify: `tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py`

**Interfaces:**
- Consumes: canonical matrix and rendered decision record.
- Produces: public navigation, exact next-activity metadata, and non-self-referential traceability.

- [ ] **Step 1: Add failing narrative and queue assertions**

Require the landing page to link both new artifacts, publish both exact directional dispositions from the matrix, state that no mapping exists, state that `GO` means design only, and preserve the public-v3.2/current-scheme boundary.

Require backlog behavior by disposition:

```python
if disposition == "GO":
    expected = f"Design the Cyber Essentials Plus v3.2 {direction} mapping"
elif disposition == "HOLD":
    expected = f"Resolve the Cyber Essentials Plus v3.2 {direction} feasibility prerequisites"
else:
    expected = None
```

Assert that `NO_GO` does not queue mapping design and that no generic immediate mapping-implementation item appears.

- [ ] **Step 2: Run focused tests and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go tests.test_release_metadata -v
```

Expected: failures for missing landing-page and backlog updates only.

- [ ] **Step 3: Update landing page and backlog from matrix outcomes**

Add one concise go/no-go subsection. Do not restate probe-level details or create compliance percentages. Update the backlog with only the outcome-authorized next activity for each direction.

- [ ] **Step 4: Create pending traceability**

Record:

- repaired source-inventory digest evidence;
- rights record identity and ancestry;
- analyst identities and independence;
- temporary analysis artifact digests without temporary paths;
- reconciler identity and difference dispositions;
- per-direction coverage derived from probes;
- directional gates and dispositions derived from the matrix;
- changed files and command results; and
- status `Pending exact-head reviews`.

Do not include or reserve fields for the traceability file's own commit, candidate SHA, reviewed SHA, PR head, merge SHA, or GitHub check result.

- [ ] **Step 5: Run focused tests and commit publication metadata**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_traceability tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go tests.test_render_ce_plus_mapping_go_no_go tests.test_release_metadata -v
python tools/render_ce_plus_mapping_go_no_go.py --matrix docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json --output docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md --check
git diff --check
```

Commit:

```powershell
git add docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-traceability.md crosswalks/uk-cyber-essentials.md project/BACKLOG.md tests/test_release_metadata.py tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py
git commit -m "Publish Cyber Essentials Plus mapping feasibility decisions"
```

---

### Task 6: Validate, independently review, publish, merge, and clean

**Files:**
- Modify only already in-scope files if a review proves a defect.
- Store exact-head review and integration evidence externally in the pull request or checks.

**Interfaces:**
- Consumes: complete immutable candidate.
- Produces: exact-head approvals, merged design-authorized decisions, post-merge evidence, and cleaned temporary state.

- [ ] **Step 1: Run the complete candidate gates**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_traceability -v
python -m unittest tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go -v
python -m unittest tests.test_render_ce_plus_mapping_go_no_go -v
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
$base = git merge-base HEAD origin/main
python tools/validate_crosswalks.py --check --baseline-ref $base
python tools/validate_links.py --check
python tools/render_ce_plus_mapping_go_no_go.py --matrix docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json --output docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md --check
git diff --check "$base..HEAD"
$prohibitedChanges = @(git diff --name-only "$base..HEAD" -- crosswalks/mappings crosswalks/registry)
if ($LASTEXITCODE -ne 0 -or $prohibitedChanges.Count -ne 0) { throw "Prohibited mapping/registry path changed: $($prohibitedChanges -join ', ')" }
$caches = @(Get-ChildItem -Recurse -Force | Where-Object { $_.Name -eq '__pycache__' -or $_.Extension -in '.pyc', '.pyo' })
if ($caches.Count -ne 0) { throw "Python cache artifacts remain: $($caches.FullName -join ', ')" }
$scratch = @(Get-ChildItem -Recurse -Force | Where-Object { $_.Name -match '(?i)(scratch|analyst-output|source-download)' })
if ($scratch.Count -ne 0) { throw "Scratch/source-download artifacts remain: $($scratch.FullName -join ', ')" }
python tools/render_ce_plus_mapping_go_no_go.py --matrix docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json --output docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md --check
if ($LASTEXITCODE -ne 0) { throw "Generated review drift detected" }
$dirty = @(git status --porcelain=v1)
if ($LASTEXITCODE -ne 0 -or $dirty.Count -ne 0) { throw "Worktree is dirty: $($dirty -join '; ')" }
```

Require no changed path under `crosswalks/mappings/` or `crosswalks/registry/`, no caches or scratch, current renderer output, and a clean worktree. Record `git rev-parse HEAD` only in external dispatch evidence.

- [ ] **Step 2: Dispatch exact-SHA specification/methodology review**

The reviewer shall verify source and traceability repair, rights sequencing, closed contracts, direction independence, coverage completeness, normative citations, gate mechanics, renderer derivation, schema fit, and absence of mapping artifacts. Resolve every Critical and Important finding.

- [ ] **Step 3: Dispatch exact-SHA security/overclaiming review independently**

The reviewer shall verify copied-source protection, anomaly non-duplication, IASME partition, source-version boundary, actor/scope/sample/date/tool/provenance/point-in-time limits, Delivery Partner discretion, direction asymmetry, condition semantics, all prohibited inferences, and design-only meaning of `GO`. Resolve every Critical and Important finding.

- [ ] **Step 4: Redispatch both reviews after any change**

Add focused regression coverage where practical, replace superseded tracked evidence rather than appending contradictions, commit, rerun every candidate gate, and redispatch both reviewers on the new exact SHA. Once both reviews approve one immutable head, make no tracked change.

- [ ] **Step 5: Push and open the reviewable pull request**

Record in the PR body the design and issue links, exact reviewed head, both reviewer identities and dispositions, rights ancestry, all gate results, and explicit absence of mapping artifacts. Confirm the PR head equals the reviewed SHA and required GitHub checks pass on it.

- [ ] **Step 6: Merge only a clean, passing exact head**

Use a true merge commit unconditionally. Squash and rebase integration are prohibited. Before merge, recheck the PR head, successful checks, clean merge state, and repository/host configuration proving merge-commit integration is enabled; abort if the selected method is not `merge`. Record the base head before integration, then run:

```powershell
git merge-base --is-ancestor $rightsCommit $reviewedPrHead
if ($LASTEXITCODE -ne 0) { throw "Rights ancestry failed" }
git merge-base --is-ancestor $baseHead $reviewedPrHead
if ($LASTEXITCODE -ne 0) { throw "Reviewed head is not based on the expected base" }
```

- [ ] **Step 7: Validate merged main and clean verified temporary state**

Update local `main`; require `git rev-list --parents -n 1 HEAD` to contain exactly the merge commit plus two parents, require the first parent to equal the recorded base head and the reviewed feature head to be the second parent (or an ancestor of that second parent if the host created an equivalent merge parent), and prove rights-record and reviewed-head ancestry to the merge. A one-parent squash/rebase result is a publication failure. Rerun focused tests, all domain validators, link validation, renderer check, and the throwing cache, scratch, prohibited-path, generated-drift, and dirty-status checks. Verify a clean checkout.

Resolve the system-temp root, exact scratch child, repository root, and worktree path before recursive removal. Remove only the verified scratch child beneath system temp and the verified project-owned worktree beneath `.worktrees/`. Then remove the merged local and remote feature branches and confirm `main == origin/main`.
