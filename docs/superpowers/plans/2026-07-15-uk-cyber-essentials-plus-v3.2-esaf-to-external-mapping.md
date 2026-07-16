# UK Cyber Essentials Plus v3.2 ESAF-to-External Mapping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, machine-valid, draft ESAF-1600 mapping set from ESAF 0.4-alpha controls to all 144 provisions in the pinned public Cyber Essentials Plus Test Specification v3.2 oracle.

**Architecture:** A contract-first snapshot fixes source rights, a 144-row provision inventory, an immutable ESAF control manifest, record provenance, and draft lifecycle state before analytical records are authored in stable oracle-group batches. Each provision receives exactly one forward-only disposition, while deterministic catalogs and focused tests expose completeness without implying assessment results or current-scheme coverage.

**Tech Stack:** Markdown with JSON/YAML front matter, JSON Schema 2020-12, Python 3 standard library, PyYAML, jsonschema, `unittest`, Git, and existing `tools.crosswalks` validation, digest, manifest, and catalog modules.

## Global Constraints

- Direction is only `esaf_to_external`; no reverse-direction leg or inference is permitted.
- Mapping-set ID is `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`.
- Snapshot root is `crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0/`.
- External structural source is the locked oracle at `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`, SHA-256 `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
- Canonical PDF digest is `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`; the source PDF is never committed.
- ESAF baseline is release `0.4-alpha`, commit `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, with 91 controls.
- Scope is `complete_publication`: exactly 144 records grouped `24/16/11/9/37/9/7/13/4/14` for `M/T1/S/T2/T3/T4/T5/C/A/B`.
- Snapshot, records, and lifecycle remain `draft`; lifecycle `events` remains empty.
- Records use original paraphrases and approved oracle metadata, never copied requirement or passage text.
- IASME content is limited to bibliographic facts, official links, and independently written high-level context.
- Positive legs require exact normative ESAF requirement text. Conditions narrow support and never create a missing external outcome.
- No mapping leg may imply procedure execution, an observed result, population coverage, certification, compliance, equivalence, endorsement, current-scheme completeness, full-population assurance, or continuous assurance.
- T5-006 with IAM-120/IAM-130 is a candidate seed requiring fresh final-schema assessment, not a preapproved mapping.
- Mapper, rights reviewer, specification reviewer, and security/overclaiming reviewer are distinct roles.
- Set `PYTHONDONTWRITEBYTECODE=1` for every Python command and preserve unrelated user changes.
- This plan does not authorize implementation. Begin Task 1 only after the repository owner separately approves execution of this plan.

---

## Shared paths and mechanical commands

```text
SNAPSHOT=crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0
MAPPING_SET_ID=uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0
REGISTRY=crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0.md
ORACLE=docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json
FOCUSED_TEST=tests.test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping
```

After every snapshot change, refresh the draft lifecycle digest before validation:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
@'
from pathlib import Path
import re
from tools.crosswalks.digests import snapshot_digest

root = Path.cwd()
mapping_set_id = "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0"
snapshot = root / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0"
registry = root / "crosswalks/registry" / f"{mapping_set_id}.md"
digest = snapshot_digest(root, snapshot)
text = registry.read_text(encoding="utf-8")
text, count = re.subn(r"(?m)^snapshot_digest: [a-f0-9]{64}$", f"snapshot_digest: {digest}", text)
if count != 1:
    raise SystemExit("expected exactly one snapshot_digest field")
registry.write_text(text, encoding="utf-8", newline="\n")
'@ | python -
```

Then regenerate and check catalogs:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python tools/validate_crosswalks.py --write
python tools/validate_crosswalks.py --check --baseline-ref b4529c05c440db2f94ec12db4f21e3d0af57a5fb
```

Every provision-batch task ends with this exact gate:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping -v
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref b4529c05c440db2f94ec12db4f21e3d0af57a5fb
python tools/validate_links.py --check
git diff --check
```

This T5-006 example uses exact pinned oracle and manifest values. Its relationship analysis is illustrative only: Task 10 must reassess each candidate leg from the exact baseline requirement before retaining, changing, or removing it.

```json
{
  "schema_version": "1.0.0",
  "record_id": "cepts32-t5-006",
  "mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
  "status": "draft",
  "external_provision_id": "CEPTS3.2-T5-006",
  "granularity": "requirement",
  "external_metadata": {"group": "T5", "kind": "result_rule", "actors": ["Assessor"]},
  "context": {"mode": "paraphrase", "summary": "Pass only if another login is requested and ordinary user credentials cannot run the process; otherwise fail."},
  "source_locator": {"official_url": "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf", "locator": "PDF page 19; printed page 18; Test case 5; conjunctive process result"},
  "disposition": "mapped",
  "relationships": [{
    "esaf_control_id": "IAM-130",
    "esaf_control_version": "0.1.0",
    "esaf_control_path": "IAM/IAM-130.md",
    "esaf_control_sha256": "4bc87d20659c2c794c4268f02a2c2699802b2d079c48803601a962853c4c6576",
    "esaf_requirement_locator": "controls/IAM/IAM-130.md#requirement",
    "relationship": "partially_supports",
    "direction": "esaf_to_external",
    "coverage": "narrow",
    "confidence": "high",
    "rationale": "Provision-specific direct normative contribution.",
    "conditions": ["Explicit condition that narrows an already-supported outcome."],
    "expected_evidence": ["Implementation evidence expected from an ESAF adopter."],
    "known_gaps": ["External outcome not provided by this ESAF requirement."],
    "prohibited_inferences": ["No inference that the external procedure ran or produced a result."]
  }],
  "mapper": {"id": "esaf-crosswalk-editorial-team", "date": "2026-07-15", "authorized_source_access": true},
  "change_history": [{"version": "0.1.0", "date": "2026-07-15", "change": "Created the draft Cyber Essentials Plus v3.2 mapping record."}]
}
```

`no_direct_mapping` records use `relationships: []` and a `negative_rationale` beginning with `Missing outcome:` followed by the exact provision outcome absent from normative ESAF text. An `out_of_scope` record would instead require a precise `Scope boundary:` rationale, but the complete-publication contract rejects `out_of_scope` unless a separately approved design amendment changes the declared analytical scope.

---

### Task 1: Commit the mapping-specific rights gate

**Files:**
- Create: `tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py`
- Create: `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-rights-attestation.md`

**Interfaces:**
- Consumes: locked oracle rights, feasibility rights commit `4207e1c1e8ff9f743274ebb4b626210cca053458`, and the approved mapping design.
- Produces: constants `MAPPING_SET_ID`, `SNAPSHOT`, `REGISTRY`, `ORACLE`, `RIGHTS`, `BASELINE_SHA`, `EXPECTED_GROUP_COUNTS`, and a committed unconditional rights decision that Task 2 requires as an ancestor.

- [ ] **Step 1: Write the failing rights contract**

Create the focused test module with imports and constants, then add:

```python
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from tools.crosswalks.io import parse_front_matter
from tests.test_uk_cyber_essentials_plus_v32_inventory import (
    PERMITTED_SOURCE_IDENTITY_PROSE,
    SOURCE_FIVE_WORD_DIGESTS,
)

ROOT = Path(__file__).parents[1]
MAPPING_SET_ID = "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0"
SNAPSHOT = ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0"
REGISTRY = ROOT / "crosswalks/registry" / f"{MAPPING_SET_ID}.md"
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RIGHTS = ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-rights-attestation.md"
BASELINE_SHA = "b4529c05c440db2f94ec12db4f21e3d0af57a5fb"
ORACLE_SHA256 = "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc"
CANONICAL_PDF_SHA256 = "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8"
LEGACY_PDF_SHA256 = "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694"
FEASIBILITY_RIGHTS_COMMIT = "4207e1c1e8ff9f743274ebb4b626210cca053458"
EXPECTED_GROUP_COUNTS = {"M": 24, "T1": 16, "S": 11, "T2": 9, "T3": 37, "T4": 9, "T5": 7, "C": 13, "A": 4, "B": 14}
COMPLETED_GROUPS: tuple[str, ...] = ()


class CyberEssentialsPlusEsafToExternalMappingTests(unittest.TestCase):
    def test_mapping_rights_gate_is_exact_and_precedes_snapshot(self) -> None:
        self.assertTrue(RIGHTS.is_file())
        text = RIGHTS.read_text(encoding="utf-8")
        for value in (
            ORACLE_SHA256,
            CANONICAL_PDF_SHA256,
            LEGACY_PDF_SHA256,
            f"feasibility_rights_commit: {FEASIBILITY_RIGHTS_COMMIT}",
            "attribution: National Cyber Security Centre; Crown copyright",
            "Open Government Licence v3.0",
            "ogl_v3_url: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            "copied requirement or passage text: prohibited",
            "IASME source-derived structure: prohibited",
            "marks and imagery: excluded",
            "source_version_boundary: public NCSC v3.2 only; current operational scheme not inferred",
            "direction: esaf_to_external",
            "reviewer_authorized_source_access: true",
            "field_classes: identifiers | titles where used | structural inventory | original paraphrases | derivative mapping analysis | ESAF normative citations | assurance analysis | official links",
            "disposition: approved",
        ):
            self.assertIn(value, text)
        self.assertNotIn("conditional approval", text.lower())
        reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", text)
        self.assertIsNotNone(reviewer)
        self.assertNotEqual(reviewer.group(1), "esaf-crosswalk-editorial-team")

        rights_commit = subprocess.check_output(
            ["git", "log", "-1", "--format=%H", "--", str(RIGHTS.relative_to(ROOT))],
            cwd=ROOT,
            text=True,
        ).strip()
        if not rights_commit:
            self.assertFalse(SNAPSHOT.exists(), "snapshot creation is blocked until rights are committed")
            return
        self.assertRegex(rights_commit, r"^[0-9a-f]{40}$")
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", FEASIBILITY_RIGHTS_COMMIT, rights_commit],
            cwd=ROOT,
            check=True,
        )
        rights_files = set(subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", rights_commit],
            cwd=ROOT,
            text=True,
        ).splitlines())
        self.assertEqual(rights_files, {
            str(RIGHTS.relative_to(ROOT)).replace("\\", "/"),
            "tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py",
        })
        first_snapshot_commit = subprocess.check_output(
            ["git", "log", "--diff-filter=A", "--format=%H", "--", str((SNAPSHOT / "README.md").relative_to(ROOT))],
            cwd=ROOT,
            text=True,
        ).splitlines()
        if first_snapshot_commit:
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", rights_commit, first_snapshot_commit[-1]],
                cwd=ROOT,
                check=True,
            )
        else:
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
            self.assertEqual(head, rights_commit, "rights commit must be HEAD before snapshot creation")
```

- [ ] **Step 2: Run RED**

Run `python -m unittest tests.test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping -v` with bytecode disabled.

Expected: FAIL because the mapping-specific rights attestation does not exist.

- [ ] **Step 3: Write the rights attestation**

Create a concise record naming a rights reviewer distinct from `esaf-crosswalk-editorial-team`; bind the feasibility rights commit, exact oracle, and both PDF digests; enumerate the eight mapping field classes; preserve NCSC/Crown attribution, the official OGL v3.0 link, copied-text prohibition, IASME partition, marks/imagery exclusions, source-version boundary, and `esaf_to_external` direction; state `disposition: approved` without conditions. Use the exact machine-readable lines asserted by the test for upstream rights basis, reviewer ID, authorized access, field classes, source boundary, direction, and disposition.

- [ ] **Step 4: Run GREEN and commit**

Run the focused test and `git diff --check`, then commit:

```powershell
git add tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-rights-attestation.md
git commit -m "Approve Cyber Essentials Plus mapping publication rights"
```

Rerun the focused test after committing. Expected: rights commit contains exactly the test and attestation, the exact-files branch passes, and no snapshot exists. Record its SHA for ancestry checks.

---

### Task 2: Extend provenance fields and create the snapshot scaffold

**Files:**
- Modify: `crosswalks/schema/mapping-record.schema.json`
- Modify: `tools/crosswalks/validation.py`
- Modify: `tests/test_crosswalk_schemas.py`
- Modify: `tests/test_validate_crosswalks.py`
- Modify: `tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py`
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0/README.md`
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0/PROVISION_INVENTORY.md`
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0/ESAF_CONTROL_MANIFEST.json`
- Create: `crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0.md`
- Modify: `crosswalks/catalog.json`
- Modify: `crosswalks/CATALOG.md`

**Interfaces:**
- Consumes: Task 1 constants and rights decision.
- Produces: optional backward-compatible record field `external_metadata`; optional backward-compatible mapper attestation `authorized_source_access`; optional backward-compatible relationship fields `esaf_control_path`, `esaf_control_sha256`, `esaf_requirement_locator`, and `prohibited_inferences`; new mapping tests require all of them.
- Produces: complete inventory and deterministic manifest used by every batch.

- [ ] **Step 1: Add failing schema and provenance tests**

Add schema fixtures proving the new fields accept only this shape:

```json
"external_metadata": {
  "type": "object",
  "additionalProperties": false,
  "required": ["group", "kind", "actors"],
  "properties": {
    "group": {"type": "string", "minLength": 1},
    "kind": {"type": "string", "minLength": 1},
    "actors": {"type": "array", "minItems": 1, "uniqueItems": true, "items": {"type": "string", "minLength": 1}}
  }
}
```

The mapper addition is `"authorized_source_access": {"const": true}`. Relationship additions are strings with nonempty path/locator, a lowercase 64-hex digest, and a nonempty unique string array for `prohibited_inferences`. Add validator mutation tests asserting path, digest, and locator mismatch against the manifest each fail closed. Existing Cyber Essentials v3.3 fixtures without the optional fields must remain valid.

Add scaffold tests asserting exact mapping identity, source metadata, rights reviewer distinction, `complete_publication`, count 144, group counts, oracle-order IDs, deterministic manifest regeneration at `BASELINE_SHA`, draft states, empty lifecycle events, and zero provision records initially.

- [ ] **Step 2: Run RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_crosswalk_schemas tests.test_validate_crosswalks tests.test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping -v
```

Expected: FAIL for unknown schema fields, missing mismatch diagnostics, and absent snapshot files.

- [ ] **Step 3: Implement the backward-compatible schema extension**

Add `external_metadata` to mapping-record properties, add `authorized_source_access` to the mapper definition, and add the four relationship properties without adding them to global `required`. The Plus-focused tests require the mapper attestation and all provenance fields on this snapshot. In `_validate_control_manifest`, when any provenance field is present require all three and compare them to the resolved manifest control:

```python
expected_path = control.get("path")
expected_digest = control.get("record_sha256")
expected_locator = f"controls/{expected_path}#requirement"
for field, expected in (
    ("esaf_control_path", expected_path),
    ("esaf_control_sha256", expected_digest),
    ("esaf_requirement_locator", expected_locator),
):
    if relationship.get(field) != expected:
        errors.append(f"{record_path}: {field} mismatch for {control_id}")
```

- [ ] **Step 4: Create the authoritative scaffold**

Write README metadata using the exact mapping ID, canonical PDF URL/digest, OGL rights, mapping-rights reviewer, baseline SHA, complete scope, mapper `esaf-crosswalk-editorial-team`, and draft status. Render `PROVISION_INVENTORY.md` directly from oracle order with `expected_count: 144`. Generate the manifest with:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
@'
from pathlib import Path
from tools.crosswalks.manifest import build_control_manifest, render_manifest
root = Path.cwd()
target = root / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0/ESAF_CONTROL_MANIFEST.json"
target.write_text(render_manifest(build_control_manifest(root, "b4529c05c440db2f94ec12db4f21e3d0af57a5fb", "0.4-alpha", None)), encoding="utf-8", newline="\n")
'@ | python -
```

Create the empty-event lifecycle record, refresh its snapshot digest, then run `validate_crosswalks.py --write`.

- [ ] **Step 5: Run GREEN and commit**

Run Step 2 tests, both crosswalk validation modes, link validation, and `git diff --check`. Commit all listed files with:

```powershell
git add -- crosswalks/schema/mapping-record.schema.json tools/crosswalks/validation.py tests/test_crosswalk_schemas.py tests/test_validate_crosswalks.py tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0.md crosswalks/catalog.json crosswalks/CATALOG.md
git diff --cached --check
git commit -m "Scaffold Cyber Essentials Plus forward mapping"
```

- [ ] **Step 6: Prove postcommit rights ancestry**

Rerun the focused test after the scaffold commit. It must take the committed-snapshot branch and prove that the rights-only commit is an ancestor of the first commit that added the snapshot README. Do not begin Task 3 unless this postcommit test passes.

---

## Provision-batch authoring contract

Tasks 3-12 use the same test-first mechanism but cover disjoint oracle rows. Before authoring, extend `COMPLETED_GROUPS` or the T3 completed-range constant and add a failing assertion that every assigned record exists and matches its oracle metadata. Each task's mapper shall inspect exact ESAF `## Requirement` text from the pinned baseline, not mutable working-tree prose or implementation guidance. Every task receives an independent specification and overclaiming review before the next task begins.

For each candidate manifest path, read the immutable control with Git and extract its `## Requirement` section; for example:

```powershell
$controlPath = 'IAM/IAM-130.md'
git show "b4529c05c440db2f94ec12db4f21e3d0af57a5fb`:controls/$controlPath"
```

Never substitute `Get-Content controls/$controlPath`, because later working-tree changes are not the pinned analytical basis.

For every batch, add or extend these assertions:

```python
def record_id(external_id: str) -> str:
    return external_id.lower().replace(".", "")

def oracle_locator(locator: dict[str, object]) -> str:
    return (
        f"PDF page {locator['pdf_page']}; printed page {locator['printed_page']}; "
        f"{locator['section']}; {locator['detail']}"
    )

def record_narratives(record: dict[str, object]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    context = record["context"]
    if "summary" in context:
        values.append(("context.summary", context["summary"]))
    if "negative_rationale" in record:
        values.append(("negative_rationale", record["negative_rationale"]))
    for index, relationship in enumerate(record["relationships"]):
        values.append((f"relationships[{index}].rationale", relationship["rationale"]))
        for field in ("conditions", "expected_evidence", "known_gaps", "prohibited_inferences"):
            values.extend(
                (f"relationships[{index}].{field}[{item_index}]", item)
                for item_index, item in enumerate(relationship[field])
            )
    return values

def assert_no_copied_source_windows(
    testcase: unittest.TestCase,
    record: dict[str, object],
    source_digests: frozenset[bytes] = SOURCE_FIVE_WORD_DIGESTS,
) -> None:
    for path, value in record_narratives(record):
        words = re.findall(r"[a-z0-9%]+", value.lower())
        for index in range(len(words) - 4):
            window = " ".join(words[index:index + 5])
            if any(window in phrase for phrase in PERMITTED_SOURCE_IDENTITY_PROSE):
                continue
            testcase.assertNotIn(
                hashlib.sha256(window.encode("utf-8")).digest(),
                source_digests,
                f"normalized five-word source window reproduced at {path}",
            )

def test_completed_batches_match_oracle_and_manifest(self) -> None:
    oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
    manifest = json.loads((SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").read_text(encoding="utf-8"))
    controls = {item["id"]: item for item in manifest["controls"]}
    for provision in oracle["provisions"]:
        if provision["group"] not in COMPLETED_GROUPS:
            continue
        path = SNAPSHOT / f"{record_id(provision['external_provision_id'])}.md"
        self.assertTrue(path.is_file(), provision["external_provision_id"])
        record, _ = parse_front_matter(path)
        self.assertEqual(record["external_provision_id"], provision["external_provision_id"])
        self.assertEqual(record["external_metadata"], {key: provision[key] for key in ("group", "kind", "actors")})
        self.assertEqual(record["source_locator"]["locator"], oracle_locator(provision["locator"]))
        self.assertEqual(record["context"]["summary"], provision["summary"])
        self.assertIs(record["mapper"]["authorized_source_access"], True)
        assert_no_copied_source_windows(self, record)
        for leg in record["relationships"]:
            control = controls[leg["esaf_control_id"]]
            self.assertEqual(leg["direction"], "esaf_to_external")
            self.assertEqual(leg["esaf_control_version"], control["version"])
            self.assertEqual(leg["esaf_control_path"], control["path"])
            self.assertEqual(leg["esaf_control_sha256"], control["record_sha256"])
            self.assertEqual(leg["esaf_requirement_locator"], f"controls/{control['path']}#requirement")
            for field in ("rationale", "conditions", "expected_evidence", "known_gaps", "prohibited_inferences"):
                self.assertTrue(leg[field])
        self.assertNotEqual(record["disposition"], "out_of_scope")
        if record["disposition"] == "no_direct_mapping":
            self.assertRegex(record["negative_rationale"], r"^Missing outcome: \S")

def test_source_copy_guard_rejects_a_surrounded_five_word_window(self) -> None:
    copied = "assessor observes distinct authentication challenge"
    record = {
        "context": {"summary": f"During review the {copied} before access"},
        "relationships": [],
    }
    digest = hashlib.sha256(copied.encode("utf-8")).digest()
    with self.assertRaisesRegex(AssertionError, r"context\.summary"):
        assert_no_copied_source_windows(self, record, frozenset({digest}))
```

T3 range tasks additionally filter their exact external-ID interval until the group is complete.

The source-copy mutation test is added in Task 2 and remains active for every batch. It scans all authored record narratives before the candidate commit using the frozen 3,055-window digest corpus; the final whole-snapshot mutation remains defense in depth.

Within every batch, repeat this test-first micro-cycle for each provision in oracle order:

1. Add the provision ID to the batch's expected-ID tuple and run the focused test to observe the single missing-record failure.
2. Load its exact oracle row and all candidate controls from the pinned manifest; inspect only each candidate control's baseline `## Requirement` section.
3. Write one complete record in a single patch, using either independently justified positive legs or a specific `Missing outcome:` negative rationale.
4. Run the focused test immediately. Correct the record before adding the next expected ID.
5. After the batch's last record, refresh generated artifacts and run the batch gate. Stage only the focused test, snapshot, lifecycle registry, and two generated catalogs with the common candidate command below, inspect the staged diff, and commit the record candidate with the task-specific message.
6. Dispatch both reviewers on that exact candidate SHA. Resolve findings with a new candidate commit and repeat the gate and reviews until both reports are clean.
7. Commit only the two review reports as the batch-closure commit; its parent is the exact reviewed content SHA.

This loop makes each record an independently testable change while leaving the analytical result open to evidence; no record disposition or relationship leg is predetermined by this plan.

Use this exact staging command for every batch candidate:

```powershell
git add -- tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0.md crosswalks/catalog.json crosswalks/CATALOG.md
git diff --cached --check
git diff --cached --stat
```

Each batch creates the following two immutable review reports and closure commit:

| Batch | Specification review | Overclaiming review | Closure commit message |
| --- | --- | --- | --- |
| M | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-m-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-m-overclaiming-review.md` | `Document Cyber Essentials Plus M batch reviews` |
| T1 | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t1-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t1-overclaiming-review.md` | `Document Cyber Essentials Plus T1 batch reviews` |
| S | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-s-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-s-overclaiming-review.md` | `Document Cyber Essentials Plus S batch reviews` |
| T2 | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t2-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t2-overclaiming-review.md` | `Document Cyber Essentials Plus T2 batch reviews` |
| T3-001-019 | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t3-001-019-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t3-001-019-overclaiming-review.md` | `Document Cyber Essentials Plus T3-001-019 batch reviews` |
| T3-020-037 | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t3-020-037-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t3-020-037-overclaiming-review.md` | `Document Cyber Essentials Plus T3-020-037 batch reviews` |
| T4 | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t4-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t4-overclaiming-review.md` | `Document Cyber Essentials Plus T4 batch reviews` |
| T5 | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t5-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t5-overclaiming-review.md` | `Document Cyber Essentials Plus T5 batch reviews` |
| C | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-c-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-c-overclaiming-review.md` | `Document Cyber Essentials Plus C batch reviews` |
| A-B | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-a-b-specification-review.md` | `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-a-b-overclaiming-review.md` | `Document Cyber Essentials Plus A-B batch reviews` |

For every batch, the mapper, mapping-rights reviewer, specification reviewer, and security/overclaiming reviewer shall be pairwise distinct. The two batch reports identify the exact reviewed candidate commit, record reviewer IDs and authorized-source access, list findings by severity, and report no unresolved Critical or Important finding. Extend the focused test to parse the mapping-rights reviewer ID and both batch report reviewer IDs and assert the four-value identity set has length four before closure. If review changes a record, rerun the batch gate and both reviews on the new candidate SHA. For closure, stage the exact two report paths listed in the batch's table row, run `git diff --cached --check` and `git diff --cached --stat`, confirm no other path is staged, and commit with that row's exact message.

---

### Task 3: Author the 24 `M` records

**Files:** Create `cepts32-m-001.md` through `cepts32-m-024.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `m` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Consumes Task 2 scaffold and produces explicit dispositions for methodology, scope, sampling, and evidence-retention provisions.

- [ ] Add `"M"` to `COMPLETED_GROUPS` and run the focused test; expect 24 missing-record failures.
- [ ] Author all 24 records provision-first. Treat assessment scope, populations, samples, dates, and retained evidence conservatively; ESAF implementation controls do not establish that external assessment mechanics occurred.
- [ ] Refresh lifecycle digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Map Cyber Essentials Plus methodology provisions"`.
- [ ] Review all M records for specific negative outcomes, source-version limits, and absence of full-population or continuous-assurance claims; then commit the two clean `m` review reports using the closure procedure.

---

### Task 4: Author the 16 `T1` records

**Files:** Create `cepts32-t1-001.md` through `cepts32-t1-016.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `t1` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Produces complete scanner-discovery and Figure 1 decision-flow dispositions without treating procedure logic as implementation evidence.

- [ ] Add `"T1"` to `COMPLETED_GROUPS`; run RED and require 16 missing records.
- [ ] Author each record from exact provision outcome. Preserve the full T1-008 through T1-016 chain as distinct records; do not infer aggregate success, scanner execution, or discovered-service state from adjacent ESAF controls.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Map Cyber Essentials Plus external-service tests"`.
- [ ] Independently review the complete Figure 1 chain and anomaly boundary; then commit the two clean `t1` review reports using the closure procedure.

---

### Task 5: Author the 11 `S` records

**Files:** Create `cepts32-s-001.md` through `cepts32-s-011.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `s` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Produces representative-device and sampling dispositions bounded to the external methodology.

- [ ] Add `"S"` to `COMPLETED_GROUPS`; run RED and require 11 missing records.
- [ ] Author all records, distinguishing exact ESAF inventory or scope duties from external selection, representativeness, and sample mechanics.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Map Cyber Essentials Plus sampling provisions"`.
- [ ] Review population/sample boundaries and reject conditions that manufacture coverage; then commit the two clean `s` review reports using the closure procedure.

---

### Task 6: Author the 9 `T2` records

**Files:** Create `cepts32-t2-001.md` through `cepts32-t2-009.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `t2` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Produces complete authorized vulnerability-scanner workflow and result-rule dispositions and the authoritative handling of the known source anomaly.

- [ ] Add `"T2"` to `COMPLETED_GROUPS`; run RED and require 9 missing records.
- [ ] Author all records from the locked IDs and locators. Reference the anomaly only by oracle identifier and locator; do not duplicate its literal or expand the provision universe.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Map Cyber Essentials Plus vulnerability scanning tests"`.
- [ ] Review anomaly nonduplication, applicability, and source boundary; then commit the two clean `t2` review reports using the closure procedure.

---

### Task 7: Author `T3` records 001-019

**Files:** Create `cepts32-t3-001.md` through `cepts32-t3-019.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `t3-001-019` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Produces the first immutable half of T3 without marking the group complete.

- [ ] Add `COMPLETED_T3_IDS = tuple(f"CEPTS3.2-T3-{number:03d}" for number in range(1, 20))` and make the shared assertion include those IDs; run RED for 19 records.
- [ ] Author each record using exact normative support or a named missing outcome. Configuration recommendations and external test steps do not become direct ESAF outcomes by subject similarity.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Map first Cyber Essentials Plus configuration batch"`.
- [ ] Review all 19 records as a sealed batch for consistent taxonomy and gaps; then commit the two clean `t3-001-019` review reports using the closure procedure.

---

### Task 8: Complete `T3` records 020-037

**Files:** Create `cepts32-t3-020.md` through `cepts32-t3-037.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `t3-020-037` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Completes T3 and replaces the range exception with group-level completeness.

- [ ] Remove `COMPLETED_T3_IDS`, add `"T3"` to `COMPLETED_GROUPS`, and run RED for the remaining 18 records.
- [ ] Author the remaining records, retaining exact recommendation strength and explicit negative outcomes.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Complete Cyber Essentials Plus configuration mapping"`.
- [ ] Review all 37 T3 records together for cross-half contradictions or templated rationales; then commit the two clean `t3-020-037` review reports using the closure procedure.

---

### Task 9: Author the 9 `T4` records

**Files:** Create `cepts32-t4-001.md` through `cepts32-t4-009.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `t4` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Produces complete user-access procedure dispositions without confusing procedure actions with implemented access controls.

- [ ] Add `"T4"` to `COMPLETED_GROUPS`; run RED for 9 records.
- [ ] Author all records and require direct normative ESAF support for every positive. Tool execution, account use during testing, or observed behavior remains outside a forward implementation claim.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Map Cyber Essentials Plus user-access tests"`.
- [ ] Review procedure/result separation and actor boundaries; then commit the two clean `t4` review reports using the closure procedure.

---

### Task 10: Author the 7 `T5` records and reassess the seed

**Files:** Create `cepts32-t5-001.md` through `cepts32-t5-007.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `t5` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Produces fresh final-schema analysis of T5, including the non-preapproved T5-006 candidate.

- [ ] Add `"T5"` to `COMPLETED_GROUPS` and a test asserting T5-006 is independently sourced from the pinned IAM requirements rather than copied from the feasibility matrix; run RED for 7 records.
- [ ] Assess every record. For T5-006, compare the exact provision outcome separately with IAM-120 and IAM-130, record a leg only where exact text directly contributes, and preserve ordinary-credential, separate-authentication, procedure-execution, device, population, and aggregate-result gaps.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Map Cyber Essentials Plus administrative-process tests"`.
- [ ] Dispatch independent normative-basis and overclaiming reviews for T5-006 and the whole group; then commit the two clean `t5` review reports using the closure procedure.

---

### Task 11: Author the 13 `C` records

**Files:** Create `cepts32-c-001.md` through `cepts32-c-013.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `c` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Produces aggregate decision and Delivery Partner discretion dispositions.

- [ ] Add `"C"` to `COMPLETED_GROUPS`; run RED for 13 records.
- [ ] Author all records. Treat C-008, C-010, and C-011 as a conjunctive discretionary external decision boundary; no ESAF implementation duty may establish that decision or revise an underlying observation.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Map Cyber Essentials Plus decision provisions"`.
- [ ] Review exception ownership, predicate conjunction, and aggregate-result overclaiming; then commit the two clean `c` review reports using the closure procedure.

---

### Task 12: Author the 4 `A` and 14 `B` records

**Files:** Create `cepts32-a-001.md` through `cepts32-a-004.md` and `cepts32-b-001.md` through `cepts32-b-014.md`; modify focused tests, lifecycle registry, and generated catalogs.

Create the `a-b` specification and overclaiming review reports defined by the batch contract.

**Interfaces:** Completes the 144-record snapshot with tool-authorization and assessment-file dispositions.

- [ ] Add `"A"` and `"B"` to `COMPLETED_GROUPS`; run RED for 18 records.
- [ ] Author A records without treating scanner authorization as scanner execution or an observed result. Author B records without treating file availability, subset definition, tailoring, or complete-file assembly as implementation evidence.
- [ ] Refresh digest, regenerate catalogs, and run the exact batch gate.
- [ ] Commit the candidate with `git commit -m "Complete Cyber Essentials Plus appendix mapping"`.
- [ ] Review complete-file coverage, protected source boundaries, and final 144-record count; then commit the two clean `a-b` review reports using the closure procedure.

---

### Task 13: Reconcile, publish draft metadata, review, and integrate

**Files:**
- Modify: `tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py`
- Modify: `crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0/README.md`
- Modify: `crosswalks/uk-cyber-essentials.md`
- Modify: `project/BACKLOG.md`
- Create: `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-traceability.md`
- Create: `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-specification-review.md`
- Create: `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-overclaiming-review.md`
- Modify: lifecycle registry, `crosswalks/catalog.json`, and `crosswalks/CATALOG.md`

**Interfaces:**
- Consumes: all 144 records and every batch review.
- Produces: one immutable reviewed technical candidate that remains schema `draft` pending qualified human review.

- [ ] **Step 1: Add failing whole-snapshot tests**

Add assertions for exact 144-record and inventory agreement; group and kind counts; zero non-oracle records; all groups completed; forward-only directions; zero missing relationship provenance fields; no generic negative rationale; no duplicate control/direction leg; no unreviewed batch finding; pairwise-distinct mapper, mapping-rights reviewer, final specification reviewer, and final security/overclaiming reviewer identities with authorized source access; exact catalog counts; landing-page synchronization; design-only/current-scheme disclaimers; and absence of copied-source windows and prohibited outcome claims.

Add a mutation matrix proving that each of these defects fails: missing record, extra record, changed oracle metadata, stale control digest, wrong requirement locator, reverse direction, empty gap, condition-created outcome, generic negative rationale, copied source window, T5-006 feasibility-text reuse, and stale catalog.

- [ ] **Step 2: Run RED**

Run the focused test and expect failures for incomplete final narratives, traceability, backlog state, and any reconciliation defects discovered by the new assertions.

- [ ] **Step 3: Reconcile the snapshot**

Review all 144 records for repeated boilerplate, cross-batch contradictions, inconsistent relationship taxonomy, unsupported adjacency, condition-created support, and aggregate sufficiency. Fix each defect with a focused regression. Recompute the lifecycle digest and catalogs after the final record change.

- [ ] **Step 4: Publish draft navigation and traceability**

Update the snapshot README and UK landing page with derived counts only. State that the snapshot is complete-publication in inventory but remains an unqualified technical draft. Preserve public-v3.2/current-operational-scheme separation and all prohibited-claim disclaimers.

Remove the completed design backlog item only because the repository owner separately approved execution of this plan; neither design nor plan merge supplies that authority. Do not remove or alter the separate `external_to_esaf` design item. Traceability records rights ancestry, immutable baseline, batch commits/reviews, derived counts, changed files, and precommit command results without claiming qualified review or approval. The PR body records rerun results and the exact final reviewed head.

- [ ] **Step 5: Run complete precommit gates**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python tools/validate_crosswalks.py --write
python -m unittest tests.test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping -v
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref b4529c05c440db2f94ec12db4f21e3d0af57a5fb
python tools/validate_links.py --check
git diff --check
```

Require no cache, scratch, analyst-output, or source-download artifacts. Capture the results in traceability, then repeat every command above except `validate_crosswalks.py --write` against the resulting bytes. If any recorded count or outcome differs, correct traceability and repeat the complete check-only gate until its statements match the candidate exactly.

- [ ] **Step 6: Commit the complete content candidate**

```powershell
git add -- tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0.md crosswalks/catalog.json crosswalks/CATALOG.md crosswalks/uk-cyber-essentials.md docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-traceability.md project/BACKLOG.md
$snapshotPrefix = 'crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0/'
$allowedFiles = @(
  'tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py',
  'crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0.md',
  'crosswalks/catalog.json',
  'crosswalks/CATALOG.md',
  'crosswalks/uk-cyber-essentials.md',
  'docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-traceability.md',
  'project/BACKLOG.md'
)
$staged = @(git diff --cached --name-only)
$unexpected = @($staged | Where-Object { $_ -notin $allowedFiles -and -not $_.StartsWith($snapshotPrefix) })
if ($unexpected) { throw "Unexpected staged paths: $($unexpected -join ', ')" }
git diff --cached --check
git diff --cached --stat
git commit -m "Publish draft Cyber Essentials Plus forward mapping"
$branchBase = git merge-base b4529c05c440db2f94ec12db4f21e3d0af57a5fb HEAD
git diff --check "$branchBase..HEAD"
if (git status --porcelain) { throw 'Content-candidate worktree is not clean' }
```

- [ ] **Step 7: Dispatch two independent candidate-SHA reviews**

The final specification and security/overclaiming reviewers shall each be distinct from the mapper, the mapping-rights reviewer, and one another, and shall attest authorized source access. The specification reviewer verifies all 144 oracle bindings, inventory/record agreement, schema extension, normative citations, relationship taxonomy, manifest provenance, lifecycle digest, catalog derivation, and draft governance. The security/overclaiming reviewer verifies copied-source protection, IASME partition, source versions, negative dispositions, conditions, T5-006 reassessment, procedure/result separation, Delivery Partner discretion, and every prohibited inference.

Resolve every Critical and Important finding. Any record or metadata change requires a new content-candidate commit, rerunning all gates, and redispatching both reviewers on the new SHA. When both reviews are clean, write the two final review reports with their reviewed content-candidate SHA and findings.

- [ ] **Step 8: Commit review reports, then prove the final exact head**

```powershell
git add -- docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-specification-review.md docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-overclaiming-review.md
git diff --cached --check
git diff --cached --stat
git commit -m "Document Cyber Essentials Plus final reviews"
```

Rerun the complete gate suite on this report-only head, using `validate_crosswalks.py --check` rather than `--write`. Redispatch both reviewers on the exact new head to verify that the only delta is faithful review documentation and that all prior conclusions still hold. Make no tracked change after these exact-head attestations.

Before exact-head redispatch, run:

```powershell
$branchBase = git merge-base b4529c05c440db2f94ec12db4f21e3d0af57a5fb HEAD
git diff --check "$branchBase..HEAD"
if (git status --porcelain) { throw 'Final reviewed worktree is not clean' }
```

- [ ] **Step 9: Push, open a draft PR, and merge only the reviewed head**

Record the reviewed SHA, both reviewer identities and dispositions, rights ancestry, all gate results, derived counts, and explicit draft/no-assessment boundaries in the PR body. Confirm the PR head equals the reviewed SHA, then mark the draft PR ready for review. Merge only after the PR is no longer draft, GitHub checks pass, required approvals are present, merge state is clean, and merge-commit integration is enabled. Use a true merge commit; squash and rebase are prohibited.

- [ ] **Step 10: Validate merged main and clean temporary state**

Verify the merge has two parents with the prior base first and reviewed feature head second, prove rights and reviewed-head ancestry, rerun focused tests and all domain validators, confirm `main == origin/main`, then remove only the verified project-owned worktree and merged local/remote feature branches.
