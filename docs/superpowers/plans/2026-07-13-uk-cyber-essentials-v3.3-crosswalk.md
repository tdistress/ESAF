# UK Cyber Essentials v3.3 Crosswalk Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a complete, machine-valid, draft ESAF-1600 mapping set covering all 116 prescriptive provisions in NCSC Cyber Essentials Requirements for IT Infrastructure v3.3.

**Architecture:** Authoritative Markdown records live in one versioned snapshot and resolve only to a release-pinned ESAF control manifest. A separate empty-event lifecycle record tracks the draft snapshot, while deterministic human and JSON catalogs expose derived views. Focused tests lock source identity, inventory completeness, conservative forward-only mappings, negative dispositions, rights, and draft governance boundaries.

**Tech Stack:** Markdown with YAML front matter, JSON Schema 2020-12, Python 3 standard library, PyYAML, jsonschema, `unittest`, Git, and the existing ESAF-1600 validation/catalog modules.

## Global Constraints

- Source PDF: `https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf`.
- Source version/date/digest: `3.3`, `2026-04-27`, `e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923`.
- ESAF baseline: release `0.4-alpha`, commit `5de9ff356ddad1e193444cd7308eff16ed83e811`, 91 draft controls at version `0.1.0`.
- Mapping-set ID: `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`.
- Snapshot status and every provision status remain `draft`; lifecycle `events` remains empty.
- Scope is `complete_publication` at atomic requirement granularity: 116 records grouped `44/12/12/7/29/12`.
- Records contain original ESAF paraphrases and precise locators, not copied requirement text.
- Record identity, atomic meaning, and precise locator shall match the locked 116-row oracle at `docs/superpowers/specs/2026-07-13-uk-cyber-essentials-v3.3-provision-oracle.json`.
- Only `esaf_to_external` relationship legs are permitted in this milestone.
- No percentages, equivalence, certification, legal-sufficiency, endorsement, or implementation-compliance claims.
- Cyber Essentials Plus remains a separate future mapping set.
- Publication-rights reviewer `esaf-project-owner` is distinct from mapper `esaf-crosswalk-editorial-team`.
- Set `PYTHONDONTWRITEBYTECODE=1` for every Python command and remove no user-owned files.

---

## Shared paths and commands

```text
SNAPSHOT=crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0
MAPPING_SET_ID=uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0
REGISTRY=crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md
```

After every task that changes a snapshot file, refresh the draft lifecycle digest with this exact mechanical command before validation:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
@'
from pathlib import Path
import re
from tools.crosswalks.digests import snapshot_digest

root = Path.cwd()
mapping_set_id = "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0"
snapshot = root / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0"
registry = root / "crosswalks/registry" / f"{mapping_set_id}.md"
digest = snapshot_digest(root, snapshot)
text = registry.read_text(encoding="utf-8")
text, count = re.subn(
    r"(?m)^snapshot_digest: [a-f0-9]{64}$",
    f"snapshot_digest: {digest}",
    text,
)
if count != 1:
    raise SystemExit("expected exactly one snapshot_digest field")
registry.write_text(text, encoding="utf-8", newline="\n")
'@ | python -
```

Then run:

```powershell
python tools/validate_crosswalks.py --write
python tools/validate_crosswalks.py --check --baseline-ref 5de9ff356ddad1e193444cd7308eff16ed83e811
```

The exact batch gate referenced by Tasks 3-9 is:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_v33_crosswalk -v
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref 5de9ff356ddad1e193444cd7308eff16ed83e811
git diff --check
```

---

### Task 1: Lock the source, rights, decisions, and landing-page contract

**Files:**
- Create: `tests/test_uk_cyber_essentials_v33_crosswalk.py`
- Modify: `tests/test_esaf_1600_foundation.py`
- Modify: `crosswalks/uk-cyber-essentials.md`
- Modify: `project/DECISION_LOG.md`
- Modify: `project/BACKLOG.md`

**Interfaces:**
- Consumes: the approved design at `docs/superpowers/specs/2026-07-13-uk-cyber-essentials-v3.3-crosswalk-design.md`.
- Consumes: the independently counted semantic/locator oracle at `docs/superpowers/specs/2026-07-13-uk-cyber-essentials-v3.3-provision-oracle.json`.
- Produces: shared constants and helper methods used by every later task's focused tests.

- [ ] **Step 1: Write the failing landing-page and decision tests**

Create a focused test module with these exact constants and first contract:

```python
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.crosswalks.io import parse_front_matter


ROOT = Path(__file__).parents[1]
SOURCE_URL = "https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf"
SOURCE_SHA256 = "e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923"
BASELINE_SHA = "5de9ff356ddad1e193444cd7308eff16ed83e811"
MAPPING_SET_ID = "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0"
SNAPSHOT = ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0"
REGISTRY = ROOT / "crosswalks/registry" / f"{MAPPING_SET_ID}.md"
PROVISION_ORACLE = ROOT / "docs/superpowers/specs/2026-07-13-uk-cyber-essentials-v3.3-provision-oracle.json"


class UkCyberEssentialsV33CrosswalkTests(unittest.TestCase):
    def test_landing_page_freezes_source_rights_and_draft_boundary(self) -> None:
        text = (ROOT / "crosswalks/uk-cyber-essentials.md").read_text(encoding="utf-8")
        for expected in (
            "**Status:** Draft mapping in development",
            "Requirements for IT Infrastructure v3.3",
            SOURCE_URL,
            SOURCE_SHA256,
            "Open Government Licence v3.0",
            "116",
            "Cyber Essentials Plus",
            "does not establish certification",
        ):
            self.assertIn(expected, text)
        self.assertNotRegex(text, r"(?im)^\*\*Status:\*\*\s*(?:Reviewed|Approved|Published)\s*$")

    def test_decisions_lock_core_plus_separation_and_draft_posture(self) -> None:
        text = (ROOT / "project/DECISION_LOG.md").read_text(encoding="utf-8")
        for decision in (
            "Cyber Essentials core and Cyber Essentials Plus use separate mapping sets.",
            "Cyber Essentials v3.3 uses 116 ESAF-assigned atomic provision locators.",
            "The initial Cyber Essentials v3.3 mapping remains draft pending qualified human review.",
        ):
            self.assertIn(decision, text)
```

Remove `uk-cyber-essentials.md` from the exact planned-page fixture loop in `test_esaf_1600_foundation.py`; keep PCI DSS and HITRUST unchanged.
Extend `ESAF_1600_DECISIONS` with the three exact DEC-0026 through DEC-0028 sentences, change `range(1, 26)` to `range(1, 29)`, change `rows[14:25]` to `rows[14:28]`, and change `range(15, 26)` to `range(15, 29)` so the existing contiguous decision-ledger test remains authoritative.

- [ ] **Step 2: Run the test to verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_uk_cyber_essentials_v33_crosswalk tests.test_esaf_1600_foundation -v
```

Expected: FAIL because the landing page remains `Planned` and DEC-0026 through DEC-0028 do not exist.

- [ ] **Step 3: Implement the source and decision contract**

Rewrite `crosswalks/uk-cyber-essentials.md` as a draft landing page with the exact source metadata, OGL attribution/link, 116-record grouped count table, draft-control disclosure, core/Plus separation, and non-certification disclaimer. Add these accepted decisions without renumbering prior rows:

```markdown
| DEC-0026 | 2026-07-13 | Cyber Essentials core and Cyber Essentials Plus use separate mapping sets. | Accepted |
| DEC-0027 | 2026-07-13 | Cyber Essentials v3.3 uses 116 ESAF-assigned atomic provision locators. | Accepted |
| DEC-0028 | 2026-07-13 | The initial Cyber Essentials v3.3 mapping remains draft pending qualified human review. | Accepted |
```

Update `project/BACKLOG.md` so the priority-crosswalk initiative records the core v3.3 draft as active and Cyber Essentials Plus as the next separate UK scheme artifact.

- [ ] **Step 4: Run focused tests and repository diff checks**

Run the Step 2 command and `git diff --check`.

Expected: PASS, with PCI DSS and HITRUST still exactly `Planned`.

- [ ] **Step 5: Commit**

```powershell
git add tests/test_uk_cyber_essentials_v33_crosswalk.py tests/test_esaf_1600_foundation.py crosswalks/uk-cyber-essentials.md project/DECISION_LOG.md project/BACKLOG.md
git commit -m "Lock UK Cyber Essentials v3.3 mapping contract"
```

---

### Task 2: Create the authoritative snapshot scaffold and complete inventory

**Files:**
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/README.md`
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/PROVISION_INVENTORY.md`
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ESAF_CONTROL_MANIFEST.json`
- Create: `crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md`
- Modify: `tests/test_uk_cyber_essentials_v33_crosswalk.py`
- Regenerate: `crosswalks/CATALOG.md`
- Regenerate: `crosswalks/catalog.json`

**Interfaces:**
- Consumes: `build_control_manifest(root, BASELINE_SHA, "0.4-alpha", None)` and `render_manifest(...)` from `tools.crosswalks.manifest`.
- Produces: one valid incomplete draft snapshot with an exact 116-ID inventory and an empty-event lifecycle record.

- [ ] **Step 1: Add failing snapshot, inventory, rights, and lifecycle tests**

Add tests that assert:

```python
EXPECTED_GROUPS = {
    "d": 44,
    "e1": 12,
    "e2": 12,
    "e3": 7,
    "e4": 29,
    "e5": 12,
}

def expected_ids() -> list[str]:
    return [
        f"CE3.3-{group.upper()}-{number:03d}"
        for group, count in EXPECTED_GROUPS.items()
        for number in range(1, count + 1)
    ]
```

Add the following test methods inside the existing `UkCyberEssentialsV33CrosswalkTests` class:

```python
    def test_locked_provision_oracle_is_exact(self) -> None:
        oracle = json.loads(PROVISION_ORACLE.read_text(encoding="utf-8"))
        provisions = oracle["provisions"]
        expected_record_ids = [
            f"ce33-{group}-{number:03d}"
            for group, count in EXPECTED_GROUPS.items()
            for number in range(1, count + 1)
        ]
        self.assertEqual(oracle["source_version"], "3.3")
        self.assertEqual(oracle["source_url"], SOURCE_URL)
        self.assertEqual(oracle["source_sha256"], SOURCE_SHA256)
        self.assertEqual(oracle["count"], 116)
        self.assertEqual(oracle["groups"], {key.upper(): value for key, value in EXPECTED_GROUPS.items()})
        self.assertEqual([item["record_id"] for item in provisions], expected_record_ids)
        self.assertEqual([item["external_provision_id"] for item in provisions], expected_ids())
        self.assertEqual(len(set(expected_ids())), 116)
        for item in provisions:
            self.assertEqual(set(item), {"record_id", "external_provision_id", "summary", "locator"})
            self.assertTrue(item["summary"])
            self.assertTrue(item["locator"])

    def test_snapshot_inventory_and_lifecycle_are_exact(self) -> None:
        mapping, body = parse_front_matter(SNAPSHOT / "README.md")
        inventory, _ = parse_front_matter(SNAPSHOT / "PROVISION_INVENTORY.md")
        lifecycle, _ = parse_front_matter(REGISTRY)
        self.assertEqual(
            SNAPSHOT.relative_to(ROOT).as_posix(),
            "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0",
        )
        self.assertEqual(mapping["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(mapping["source_version"], {"id": "3.3", "label": "3.3"})
        self.assertEqual(mapping["mapping_set_version"], "0.1.0")
        self.assertEqual(mapping["status"], "draft")
        self.assertEqual(mapping["source"]["official_url"], SOURCE_URL)
        self.assertEqual(mapping["source"]["publication_date"], "2026-04-27")
        self.assertEqual(mapping["source"]["access_class"], "public")
        self.assertEqual(mapping["esaf_release"]["source_commit_sha"], BASELINE_SHA)
        self.assertEqual(mapping["scope"]["inventory_count"], 116)
        self.assertEqual(mapping["mapper"]["id"], "esaf-crosswalk-editorial-team")
        self.assertTrue(mapping["mapper"]["authorized_source_access"])
        self.assertEqual(inventory["scope_type"], "complete_publication")
        self.assertEqual(inventory["expected_count"], 116)
        self.assertEqual(inventory["provision_ids"], expected_ids())
        self.assertEqual(lifecycle["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(lifecycle["events"], [])
        self.assertIn(SOURCE_SHA256, body)
        self.assertIn("2026-07-13", body)
        self.assertIn("UK National Cyber Security Centre", body)
        self.assertIn("Open Government Licence v3.0", body)
```

Also assert `publication_rights.permitted_elements` is exactly the six-element set `identifiers`, `titles`, `structural_inventory`, `paraphrases`, `derivative_mapping_analysis`, and `official_links`; `prohibited_elements == []`; `reviewer_id == "esaf-project-owner"`; the rights reviewer differs from the mapper; both rights attestations are true; and neither schema `reviewer` nor `approver` exists.

- [ ] **Step 2: Run the focused test to verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_uk_cyber_essentials_v33_crosswalk -v
```

Expected: FAIL because the snapshot does not exist.

- [ ] **Step 3: Create mapping-set and inventory Markdown**

Use the exact metadata contract from the approved design. Set `mapping_set_version: 0.1.0`, `status: draft`, `scope.type: complete_publication`, `scope.inventory_count: 116`, and `scope.default_granularity: requirement`. Record source digest, access date, NCSC attribution, OGL URL, mapper-assigned-ID disclosure, inclusion rules, excluded informative sections, and `44/12/12/7/29/12` group counts in the body.

Inventory IDs shall be exactly and contiguously ordered as independently generated by `expected_ids()` and shall match the locked oracle in the same sequence. Before authoring records, assert the oracle itself has `count == 116`, group counts `44/12/12/7/29/12`, exact independently generated `record_id` and `external_provision_id` sequences, and nonempty `summary` and `locator` values.

- [ ] **Step 4: Generate the pinned control manifest mechanically**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
@'
from pathlib import Path
from tools.crosswalks.manifest import build_control_manifest, render_manifest

root = Path.cwd()
target = root / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ESAF_CONTROL_MANIFEST.json"
manifest = build_control_manifest(root, "5de9ff356ddad1e193444cd7308eff16ed83e811", "0.4-alpha", None)
target.write_text(render_manifest(manifest), encoding="utf-8", newline="\n")
'@ | python -
```

Copy the generated `control_catalog_sha256` into mapping-set metadata exactly.

- [ ] **Step 5: Create and refresh the lifecycle record**

Create the registry record with schema version `1.0.0`, the exact mapping-set ID, `snapshot_digest` set initially to 64 zeroes, and `events: []`. Run the shared digest-refresh command, then `python tools/validate_crosswalks.py --write`.

- [ ] **Step 6: Run focused and crosswalk validation**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_uk_cyber_essentials_v33_crosswalk -v
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref 5de9ff356ddad1e193444cd7308eff16ed83e811
git diff --check
```

Expected: PASS with one incomplete draft mapping set, 116 inventoried provisions, zero records, and current catalogs.

- [ ] **Step 7: Commit**

```powershell
git add -- crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json tests/test_uk_cyber_essentials_v33_crosswalk.py
git commit -m "Create Cyber Essentials v3.3 draft inventory"
```

---

### Task 3: Author the 44 Scope provision records

**Files:**
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ce33-d-001.md` through `ce33-d-044.md` in the same directory
- Modify: `tests/test_uk_cyber_essentials_v33_crosswalk.py`
- Modify: `REGISTRY`
- Regenerate: `crosswalks/CATALOG.md`
- Regenerate: `crosswalks/catalog.json`

**Interfaces:**
- Consumes: inventory IDs `CE3.3-D-001` through `CE3.3-D-044` and pinned controls `ARC-110`, `ARC-140`, `CMP-120`, `AUD-120`, `INF-100`, `GOV-130`, `IAM-100`, and `IAM-150` where exact text supports a leg.
- Produces: 44 draft records covering pages 6-12, including cloud, BYOD, remote work, wireless, third-party, and software scope rules.

- [ ] **Step 1: Add the failing Scope batch test**

Add a helper that parses direct-child records and a test asserting exact filenames, external IDs, draft status, requirement granularity, source URL, locator prefix `Section D`, mapper ID, version `0.1.0`, and either valid forward-only relationships or a specific negative rationale.

```python
def record_paths(prefix: str) -> list[Path]:
    return sorted(SNAPSHOT.glob(f"{prefix}-*.md"))
```

Add the following methods inside the existing `UkCyberEssentialsV33CrosswalkTests` class; do not create a second class declaration:

```python
    def load_record(self, record_id: str) -> dict[str, object]:
        return parse_front_matter(SNAPSHOT / f"{record_id}.md")[0]

    def assert_group(self, group: str, count: int) -> None:
        paths = record_paths(f"ce33-{group}")
        oracle = json.loads(PROVISION_ORACLE.read_text(encoding="utf-8"))
        oracle_by_id = {item["record_id"]: item for item in oracle["provisions"]}
        self.assertEqual(
            [path.stem for path in paths],
            [f"ce33-{group}-{number:03d}" for number in range(1, count + 1)],
        )
        for number, path in enumerate(paths, 1):
            metadata, _ = parse_front_matter(path)
            expected = oracle_by_id[path.stem]
            self.assertEqual(metadata["external_provision_id"], expected["external_provision_id"])
            self.assertEqual(metadata["status"], "draft")
            self.assertEqual(metadata["granularity"], "requirement")
            self.assertEqual(metadata["source_locator"]["official_url"], SOURCE_URL)
            self.assertEqual(metadata["source_locator"]["locator"], expected["locator"])
            self.assertEqual(metadata["mapper"]["id"], "esaf-crosswalk-editorial-team")
            self.assertEqual(metadata["mapping_set_id"], MAPPING_SET_ID)
            self.assertEqual(metadata["change_history"][-1]["version"], "0.1.0")
            self.assertEqual(metadata["context"]["summary"], expected["summary"])
            self.assertEqual(
                {leg["direction"] for leg in metadata["relationships"]},
                {"esaf_to_external"} if metadata["relationships"] else set(),
            )
            if metadata["relationships"]:
                self.assertNotEqual(metadata["disposition"], "no_direct_mapping")
            else:
                self.assertEqual(metadata["disposition"], "no_direct_mapping")
                self.assertTrue(metadata["negative_rationale"])

    def test_scope_records_are_complete_and_conservative(self) -> None:
        self.assert_group("d", 44)
```

- [ ] **Step 2: Run focused test to verify RED**

Expected: FAIL with zero Scope record files.

- [ ] **Step 3: Author Scope records with atomic locators and conservative mappings**

Use the approved inventory sequence: general scope/boundaries `001-011`; BYOD `012-015`; remote work `016-020`; wireless `021-023`; cloud responsibility `024-026`; third-party accounts/services/devices `027-042`; web-application scope `043-044`.

Use `no_direct_mapping` for certification-body agreement, general end-user-device inclusion, detailed router/wireless/role ownership rules, and other enterprise-wide outcomes not required by ESAF. Do not treat an AI architecture inventory as a general device inventory. Where mapped, make the AI-system scope limitation explicit in `conditions` and `known_gaps`.

- [ ] **Step 4: Refresh digest/catalog and run gates**

Run the shared digest command, `python tools/validate_crosswalks.py --write`, and the exact shared batch gate.

Expected: PASS with 44 of 116 records represented.

- [ ] **Step 5: Commit**

```powershell
git add -- crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json tests/test_uk_cyber_essentials_v33_crosswalk.py
git commit -m "Map Cyber Essentials v3.3 scope provisions"
```

---

### Task 4: Author the 12 Firewalls provision records

**Files:**
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ce33-e1-001.md` through `ce33-e1-012.md` in the same directory
- Modify: focused test, registry digest, and generated catalogs.

**Interfaces:**
- Consumes: `INF-110`, `INF-130`, `IAM-110`, `IAM-130`, `ARC-110`, and `API-110` only where their exact text contributes.
- Produces: 12 records covering software firewalls, device protection, administrative access, default inbound blocking, rule approval/documentation, rule removal, and untrusted networks.

- [ ] **Step 1: Add a failing exact-range and semantic test for `ce33-e1-001..012`**

Require locators beginning `Section E.1`, forward-only legs, and explicit known gaps whenever a generic hardening or architecture control does not mandate a firewall.

```python
def test_firewall_records_are_complete_and_do_not_infer_firewall_presence(self) -> None:
    self.assert_group("e1", 12)
    universal = self.load_record("ce33-e1-002")
    self.assertEqual(universal["disposition"], "no_direct_mapping")
    self.assertIn("firewall", universal["negative_rationale"].lower())
```

- [ ] **Step 2: Run focused test to verify RED**

Expected: FAIL with no E1 files.

- [ ] **Step 3: Author the 12 records**

Treat universal firewall presence, default-deny inbound traffic, exact internet-admin exceptions, and mandatory software firewalls on untrusted networks as `no_direct_mapping` unless a cited ESAF control contains that outcome. Map rule governance to `INF-130` only to the extent its configuration/change requirements apply; never convert generic hardening into proof of firewall deployment.

- [ ] **Step 4: Run the shared digest command, crosswalk `--write`, and exact batch gate**

Expected: PASS with 56 of 116 records.

- [ ] **Step 5: Commit**

```powershell
git add -- crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json tests/test_uk_cyber_essentials_v33_crosswalk.py
git commit -m "Map Cyber Essentials firewall provisions"
```

---

### Task 5: Author the 12 Secure Configuration provision records

**Files:**
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ce33-e2-001.md` through `ce33-e2-012.md` in the same directory
- Modify: focused test, registry digest, and generated catalogs.

**Interfaces:**
- Consumes: `INF-110`, `INF-130`, `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-150`, `APP-140`, and `OPS-110` where exact text supports a leg.
- Produces: 12 records covering account/software reduction, default credentials, autorun, authentication, device locking, brute-force protection, and unlock credential length.

- [ ] **Step 1: Add a failing exact-range and semantic test for `ce33-e2-001..012`**

Require `Section E.2` locators and explicit negative rationales for exact device-locking thresholds or endpoint configuration outcomes absent from ESAF.

```python
def test_secure_configuration_records_are_complete_and_preserve_threshold_gaps(self) -> None:
    self.assert_group("e2", 12)
    for record_id in ("ce33-e2-009", "ce33-e2-011"):
        record = self.load_record(record_id)
        self.assertEqual(record["disposition"], "no_direct_mapping")
        self.assertTrue(record["negative_rationale"])
```

- [ ] **Step 2: Run focused test to verify RED**

- [ ] **Step 3: Author the 12 records**

Use strong direct legs for identity lifecycle/authentication only where the ESAF control applies to the relevant AI system identity. Preserve gaps for default-password replacement, unnecessary general software/services, autorun, ten-attempt/five-minute thresholds, and six-character unlock credentials. Do not broaden `IAM-140` from secrets into human password policy.

- [ ] **Step 4: Run the shared digest command, crosswalk `--write`, and exact batch gate**

Expected: PASS with 68 of 116 records.

- [ ] **Step 5: Commit**

```powershell
git add -- crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json tests/test_uk_cyber_essentials_v33_crosswalk.py
git commit -m "Map Cyber Essentials secure configuration provisions"
```

---

### Task 6: Author the 7 Security Update Management provision records

**Files:**
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ce33-e3-001.md` through `ce33-e3-007.md` in the same directory
- Modify: focused test, registry digest, and generated catalogs.

**Interfaces:**
- Consumes: `INF-120`, `ARC-150`, `OPS-110`, `INF-130`, and `APP-140` where exact text supports a leg.
- Produces: 7 records for supported software, unsupported-software treatment, automatic updates, and three independently applicable 14-day triggers.

- [ ] **Step 1: Add a failing exact-range and threshold-preservation test**

Assert `CE3.3-E3-005`, `006`, and `007` remain distinct and that their summaries preserve the 14-day trigger without claiming ESAF contains that deadline.

```python
def test_update_records_are_complete_and_keep_three_fixed_deadline_triggers(self) -> None:
    self.assert_group("e3", 7)
    for record_id in ("ce33-e3-005", "ce33-e3-006", "ce33-e3-007"):
        record = self.load_record(record_id)
        self.assertIn("14 days", record["context"]["summary"])
        for leg in record["relationships"]:
            self.assertTrue(any("14-day" in gap or "14 day" in gap for gap in leg["known_gaps"]))
```

- [ ] **Step 2: Run focused test to verify RED**

- [ ] **Step 3: Author the 7 records**

Map ESAF's risk-based vulnerability and lifecycle controls as partial contributions. Use explicit known gaps for universal software licensing/support, automatic-update enablement, internet-isolated unsupported software, the fixed 14-day deadline, CVSS v3 score 7, and vendor severity/no-severity triggers. Never describe a risk-based remediation process as satisfying the fixed deadline.

- [ ] **Step 4: Run the shared digest command, crosswalk `--write`, and exact batch gate**

Expected: PASS with 75 of 116 records.

- [ ] **Step 5: Commit**

```powershell
git add -- crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json tests/test_uk_cyber_essentials_v33_crosswalk.py
git commit -m "Map Cyber Essentials update provisions"
```

---

### Task 7: Author User Access Control records 001-015

**Files:**
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ce33-e4-001.md` through `ce33-e4-015.md` in the same directory
- Modify: focused test, registry digest, and generated catalogs.

**Interfaces:**
- Consumes: `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-150`, and `MON-150`.
- Produces: 15 records covering account/privilege governance, unique credentials, account removal, MFA, administrative separation, and MFA account populations.

- [ ] **Step 1: Add a failing exact-range and identity-scope test**

Require `Section E.4` locators, distinct records for MFA-where-available and mandatory cloud MFA, and known gaps that disclose ESAF's AI-asset scope.

```python
def test_user_access_first_batch_is_complete_and_separates_mfa_outcomes(self) -> None:
    self.assertEqual(
        [path.stem for path in record_paths("ce33-e4")],
        [f"ce33-e4-{number:03d}" for number in range(1, 16)],
    )
    available = self.load_record("ce33-e4-009")
    cloud = self.load_record("ce33-e4-010")
    self.assertNotEqual(available["context"]["summary"], cloud["context"]["summary"])
    self.assertIn("cloud", cloud["context"]["summary"].lower())
```

- [ ] **Step 2: Run focused test to verify RED**

- [ ] **Step 3: Author records 001-015**

Use direct IAM legs only where control text supports the outcome. Keep cloud-service MFA and population-wide requirements partial or negative when ESAF does not mandate them universally. Separate account creation from approval and administrative-account existence from activity restriction.

- [ ] **Step 4: Run the shared digest command, crosswalk `--write`, and exact batch gate**

Expected: PASS with 90 of 116 records.

- [ ] **Step 5: Commit**

```powershell
git add -- crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json tests/test_uk_cyber_essentials_v33_crosswalk.py
git commit -m "Map Cyber Essentials account control provisions"
```

---

### Task 8: Author User Access Control records 016-029

**Files:**
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ce33-e4-016.md` through `ce33-e4-029.md` in the same directory
- Modify: focused test, registry digest, and generated catalogs.

**Interfaces:**
- Consumes: the same IAM/MON controls as Task 7 plus `EDU-100` or `EDU-110` only where exact workforce language supports password education.
- Produces: 14 records covering MFA password length, usable/accessibile factors, brute-force protection, password-quality alternatives, education, password storage, expiry/complexity behavior, and compromise response.

- [ ] **Step 1: Add a failing exact-range and numeric-threshold test**

Assert the summaries preserve `8`, `12`, `10`, `5 minutes`, and `three words` where applicable, while every mapped leg states that ESAF does not itself impose the source-specific threshold unless the exact control text does.

```python
def test_user_access_second_batch_preserves_source_thresholds(self) -> None:
    self.assert_group("e4", 29)
    checks = {
        "ce33-e4-016": "8",
        "ce33-e4-021": "10",
        "ce33-e4-022": "12",
        "ce33-e4-024": "three",
    }
    for record_id, token in checks.items():
        self.assertIn(token, self.load_record(record_id)["context"]["summary"])
```

- [ ] **Step 2: Run focused test to verify RED**

- [ ] **Step 3: Author records 016-029**

Prefer negative dispositions over generic identity mappings for numeric password and lockout rules. Map workforce education only when the ESAF control directly requires applicable training. Preserve separate outcomes for usable storage and usage guidance, no routine expiry, no complexity rules, and prompt response to suspected compromise.

- [ ] **Step 4: Run the shared digest command, crosswalk `--write`, and exact batch gate**

Expected: PASS with 104 of 116 records.

- [ ] **Step 5: Commit**

```powershell
git add -- crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json tests/test_uk_cyber_essentials_v33_crosswalk.py
git commit -m "Map Cyber Essentials authentication provisions"
```

---

### Task 9: Author the 12 Malware Protection provision records

**Files:**
- Create: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/ce33-e5-001.md` through `ce33-e5-012.md` in the same directory
- Modify: focused test, registry digest, and generated catalogs.

**Interfaces:**
- Consumes: `INF-110`, `APP-140`, and `API-120` only as their exact text permits.
- Produces: 12 records covering active malware protection, anti-malware behavior, malicious-site blocking, code-signing allowlists, application approval, and unsigned-application prevention.

- [ ] **Step 1: Add a failing exact-range and gap-visibility test**

Require all 12 records, `Section E.5` locators, and at least one explicit negative disposition for the absence of a universal endpoint-malware control. Do not require a fabricated mapped leg.

```python
def test_malware_records_are_complete_and_expose_endpoint_gap(self) -> None:
    self.assert_group("e5", 12)
    records = [self.load_record(f"ce33-e5-{number:03d}") for number in range(1, 13)]
    negatives = [record for record in records if record["disposition"] == "no_direct_mapping"]
    self.assertTrue(negatives)
    self.assertTrue(any("malware" in record["negative_rationale"].lower() for record in negatives))
```

- [ ] **Step 2: Run focused test to verify RED**

- [ ] **Step 3: Author the 12 records**

Use `no_direct_mapping` for outcomes not expressly required by ESAF. Contextual controls may be mapped only when they materially contribute; application-security, plugin, or hardening language shall not be described as endpoint anti-malware, malicious-site blocking, or application allowlisting.

- [ ] **Step 4: Run the shared digest command, crosswalk `--write`, and exact batch gate**

Expected: PASS with all 116 records represented.

- [ ] **Step 5: Commit**

```powershell
git add -- crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json tests/test_uk_cyber_essentials_v33_crosswalk.py
git commit -m "Map Cyber Essentials malware provisions"
```

---

### Task 10: Enforce whole-snapshot semantics and publish draft evidence

**Files:**
- Modify: `tests/test_uk_cyber_essentials_v33_crosswalk.py`
- Modify: `crosswalks/uk-cyber-essentials.md`
- Modify: `crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/README.md`
- Modify: `CHANGELOG.md`
- Modify: `project/BACKLOG.md`
- Create: `docs/superpowers/reviews/2026-07-13-uk-cyber-essentials-v3.3-traceability.md`
- Modify: registry digest and generated catalogs.

**Interfaces:**
- Consumes: the complete 116-record draft and all task-level review findings.
- Produces: one independently reviewable branch with line-by-line acceptance evidence and no unresolved Critical or Important findings.

- [ ] **Step 1: Add failing aggregate semantic tests**

Add tests that load all 116 records and assert:

```python
def test_complete_snapshot_has_exact_records_and_allowed_semantics(self) -> None:
    records = [parse_front_matter(path)[0] for path in sorted(SNAPSHOT.glob("ce33-*.md"))]
    inventory = parse_front_matter(SNAPSHOT / "PROVISION_INVENTORY.md")[0]
    manifest = json.loads((SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").read_text(encoding="utf-8"))
    manifest_versions = {control["id"]: control["version"] for control in manifest["controls"]}
    self.assertEqual(len(records), 116)
    self.assertEqual(
        [record["external_provision_id"] for record in records],
        inventory["provision_ids"],
    )
    self.assertEqual({record["status"] for record in records}, {"draft"})
    self.assertEqual({record["granularity"] for record in records}, {"requirement"})
    self.assertNotIn("out_of_scope", {record["disposition"] for record in records})
    for record in records:
        self.assertTrue(record["source_locator"]["locator"])
        for leg in record["relationships"]:
            self.assertEqual(leg["direction"], "esaf_to_external")
            self.assertEqual(manifest_versions[leg["esaf_control_id"]], leg["esaf_control_version"])
            self.assertTrue(leg["conditions"])
            self.assertTrue(leg["expected_evidence"])
            self.assertTrue(leg["known_gaps"])
        if not record["relationships"]:
            self.assertEqual(record["disposition"], "no_direct_mapping")
            self.assertGreater(len(record["negative_rationale"].split()), 8)
```

Add claim-language scans for `equivalent`, `certified by`, `ensures compliance`, `compliance percentage`, and NCSC endorsement across the landing page, snapshot bodies, and provision summaries. Add a local-link test and a grouped-count/catalog agreement test.

- [ ] **Step 2: Run focused and full suites to verify any RED gaps**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_uk_cyber_essentials_v33_crosswalk -v
python -m unittest discover -s tests -v
```

Expected: any remaining semantic, wording, link, or catalog gaps fail with record-specific diagnostics.

- [ ] **Step 3: Correct only evidenced gaps and finalize narrative outputs**

Update the landing page and mapping-set narrative with actual mapped/negative counts derived from the catalog, prominent firewall/password/update/malware gaps, draft-control disclosure, OGL attribution, and the separate Plus roadmap. Do not add marketing language or a percentage.

Update the changelog and backlog with the validated-draft milestone. Create a traceability matrix covering every design acceptance criterion, relevant file/test evidence, status, and the independent-review procedure. Final review closure is recorded on the pull request so the reviewed head can remain immutable.

- [ ] **Step 4: Refresh digest and generated catalogs**

Run the shared digest-refresh command followed by `python tools/validate_crosswalks.py --write`.

- [ ] **Step 5: Run final local gates**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_v33_crosswalk -v
python -m unittest discover -s tests -v
python tools/validate_crosswalks.py --write
python tools/migrate_control_mappings.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref 5de9ff356ddad1e193444cd7308eff16ed83e811
git diff --check
```

Expected: all commands exit 0, catalogs remain unchanged after `--write`, the worktree has no caches, and status contains only intended committed changes.

- [ ] **Step 6: Commit the complete review candidate**

```powershell
git add -- tests/test_uk_cyber_essentials_v33_crosswalk.py crosswalks/uk-cyber-essentials.md crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0 crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md crosswalks/CATALOG.md crosswalks/catalog.json CHANGELOG.md project/BACKLOG.md docs/superpowers/reviews/2026-07-13-uk-cyber-essentials-v3.3-traceability.md
git commit -m "Complete Cyber Essentials v3.3 draft crosswalk"
```

- [ ] **Step 7: Conduct independent reviews on the immutable candidate**

Dispatch one specification/inventory reviewer and one security/overclaiming reviewer against the complete merge-base-to-head diff at the exact current commit. Resolve every Critical and Important finding. Fix lower-severity defects or record an explicit acceptance rationale. After any head change, rerun all affected gates, commit only the explicit affected paths, and dispatch both reviews again against the new head. When both reviewers approve, make no further repository changes; record the exact reviewed SHA and review closure in pull-request comments or check artifacts.

- [ ] **Step 8: Publish and integrate**

Push the branch, open a draft pull request, verify the PR head equals the independently reviewed SHA, wait for required checks, mark ready, merge only with `mergeable: MERGEABLE` and `mergeStateStatus: CLEAN`, then verify the protected-branch workflow passes on the merge commit. Keep the snapshot status `draft`.
