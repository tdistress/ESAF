# UK Cyber Essentials Plus v3.2 Public-Source Inventory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and independently reconcile a byte-pinned, complete-publication oracle for every independently actionable or normative provision in the public NCSC Cyber Essentials Plus Test Specification v3.2 without creating ESAF mappings.

**Architecture:** A focused test module locks source identity, rights, section coverage, identifier rules, visual decisions, anomalies, and prohibited claims. Two independent inventory authors work from the same rendered canonical PDF and produce separate scratch atom lists; a reconciler dispositions every difference and commits one ordered JSON oracle plus exact-SHA traceability. The snapshot/mapping tree remains untouched.

**Tech Stack:** Python 3 `unittest`, JSON, Markdown, Poppler PDF rendering, SHA-256, existing ESAF validators, Git, GitHub Actions.

## Global Constraints

- The source is the public NCSC Cyber Essentials Plus Test Specification v3.2, never Plus v3.3.
- `complete_publication` means complete only for the exact pinned public PDF, not the current operational scheme.
- The canonical resource-page target is 424,226 bytes with SHA-256 `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8` as accessed 2026-07-14.
- The legacy official variant is 419,191 bytes with SHA-256 `d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694`.
- No expected provision count may be stated until two independent inventories are reconciled.
- NCSC Crown/OGL rights and IASME copyright/provenance shall remain separate.
- Every PDF page shall be rendered and visually inspected; text extraction alone is insufficient.
- No mapping snapshot, lifecycle record, control manifest, provision mapping record, relationship leg, or generated mapping statistic shall be created.
- No certification, compliance, equivalence, endorsement, predictive-sufficiency, full-population, continuous-assurance, or current-scheme-completeness claim is permitted.
- Python validation shall set `PYTHONDONTWRITEBYTECODE=1` and leave no cache or rendered-page artifact in the repository.

---

### Task 1: Lock the source, rights, and oracle contract in failing tests

**Files:**
- Create: `tests/test_uk_cyber_essentials_plus_v32_inventory.py`
- Expected later: `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`

**Interfaces:**
- Consumes: the approved design, NCSC resource page, canonical and legacy official PDFs.
- Produces: `CyberEssentialsPlusV32InventoryTests`, source constants, section/group contracts, and oracle validation helpers used by later tasks.

- [ ] **Step 1: Write source and absence tests**

Create the focused module with these exact constants and initial tests:

```python
from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RESOURCE_PAGE = "https://www.ncsc.gov.uk/cyberessentials/resources"
CANONICAL_URL = "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf"
CANONICAL_BYTES = 424226
CANONICAL_SHA256 = "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8"
LEGACY_URL = "https://www.ncsc.gov.uk/files/cyber-essentials-plus-test-specification-v3-2.pdf"
LEGACY_BYTES = 419191
LEGACY_SHA256 = "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694"
GROUPS = ("M", "T1", "S", "T2", "T3", "T4", "T5", "C", "A", "B")
KINDS = {
    "applicability", "prerequisite", "procedure_step", "decision_rule",
    "result_rule", "evidence_retention", "recommendation",
}


class CyberEssentialsPlusV32InventoryTests(unittest.TestCase):
    def oracle(self) -> dict:
        return json.loads(ORACLE.read_text(encoding="utf-8"))

    def test_locked_oracle_exists(self) -> None:
        self.assertTrue(ORACLE.is_file())

    def test_source_identity_is_exact(self) -> None:
        oracle = self.oracle()
        self.assertEqual("3.2", oracle["source_version"])
        self.assertEqual(RESOURCE_PAGE, oracle["resource_page_url"])
        self.assertEqual(CANONICAL_URL, oracle["canonical_source_url"])
        self.assertEqual(CANONICAL_BYTES, oracle["canonical_byte_length"])
        self.assertEqual(CANONICAL_SHA256, oracle["canonical_sha256"])
        self.assertEqual(LEGACY_URL, oracle["legacy_source_url"])
        self.assertEqual(LEGACY_BYTES, oracle["legacy_byte_length"])
        self.assertEqual(LEGACY_SHA256, oracle["legacy_sha256"])
        self.assertEqual(24, oracle["pdf_page_count"])
```

- [ ] **Step 2: Run the focused suite and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_inventory -v
```

Expected: failure because the oracle file is absent. Syntax, import, or path errors are not valid RED evidence.

- [ ] **Step 3: Add structural and semantic helper tests while still RED**

Add tests that, once the oracle exists, will require:

- `scope_type == "complete_publication"` and a scope statement bounded to the public v3.2 PDF;
- exact NCSC/OGL attribution and an explicit separate IASME-rights limitation;
- `section_ledger` entries with heading, PDF/printed pages, decision, rationale, and atom count;
- every substantive heading accounted for exactly once;
- ledger, group, and total counts agreeing with `len(provisions)`;
- unique, ordered record and external IDs matching `cepts32-<group>-NNN` and `CEPTS3.2-<GROUP>-NNN`;
- valid controlled `kind`, nonempty original summary, and dual-coordinate locator;
- exactly seven Figure 1 decision atoms;
- the literal source anomaly `tests 2 to 7` recorded without correction;
- no mapping disposition, relationship, ESAF control, or compliance statistic fields; and
- no prohibited claim phrases in the serialized oracle or landing-page update.

Use helper assertions over the loaded JSON rather than duplicating oracle content in test code. After the count is independently reconciled in Task 3, add one literal `EXPECTED_COUNT` and exact group-count mapping to lock the accepted result.

- [ ] **Step 4: Commit the failing contract**

```powershell
git add tests/test_uk_cyber_essentials_plus_v32_inventory.py
git commit -m "Test Cyber Essentials Plus source inventory contract"
```

---

### Task 2: Acquire, render, and independently inventory the canonical PDF

**Files:**
- Create outside repository: system-temporary canonical and legacy PDFs
- Create outside repository: 24 rendered canonical page images
- Create ignored scratch: `.superpowers/ce-plus/inventory-a.json`
- Create ignored scratch: `.superpowers/ce-plus/inventory-b.json`
- Create ignored scratch: `.superpowers/ce-plus/page-review-a.md`
- Create ignored scratch: `.superpowers/ce-plus/page-review-b.md`

**Interfaces:**
- Consumes: exact source constants and atomization rules from the design.
- Produces: two independent atom lists and page-review ledgers; no tracked oracle yet.

- [ ] **Step 1: Re-fetch and verify both official variants**

Download both URLs to a system-temporary directory. Verify media type, byte length, SHA-256, PDF page count, title, displayed version, displayed date, copyright, and licence. Stop if the resource-page target or canonical bytes differ from the design.

- [ ] **Step 2: Render all canonical pages**

Use the bundled Poppler runtime:

```powershell
pdftoppm -png -r 150 $canonicalPdf $temporaryPrefix
```

Expected: 24 nonempty PNG files. Inspect every page for operative tables, figures, branches, footnotes, and layout-dependent conditions. Record PDF and printed page coordinates.

- [ ] **Step 3: Dispatch inventory author A**

Author A reads the approved design and all 24 rendered pages. They create `inventory-a.json` and `page-review-a.md` with a complete section ledger and ordered atom list. They shall not see Author B's provisional list or count.

- [ ] **Step 4: Dispatch inventory author B independently**

Author B receives the same source and rules but no Author A output. They create `inventory-b.json` and `page-review-b.md`. They shall not see Author A's provisional list or count.

- [ ] **Step 5: Verify independent deliverables**

Confirm both authors reviewed 24 pages, accounted for every substantive heading, included Figure 1's seven decisions, recorded the `tests 2 to 7` anomaly, and produced internally consistent unique IDs and counts. Do not average or choose a count at this step.

---

### Task 3: Reconcile and lock the provision oracle

**Files:**
- Create: `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`
- Modify: `tests/test_uk_cyber_essentials_plus_v32_inventory.py`
- Create: `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-inventory-reconciliation.md`

**Interfaces:**
- Consumes: independent inventories A and B plus exact rendered source.
- Produces: one reconciled oracle, fixed accepted count, and difference-disposition record.

- [ ] **Step 1: Generate a machine comparison**

Compare inventories by source location, kind, actor, action/criterion, condition, and outcome. List additions, omissions, boundary differences, ID differences, kind differences, summary differences, and locator differences. Preserve both originals in ignored scratch until reconciliation is accepted.

- [ ] **Step 2: Disposition every difference**

For each difference, record both proposals, the selected result, exact source evidence, atomization-rule rationale, and reconciler. Re-open rendered pages whenever text extraction or paragraph context is ambiguous. No unresolved difference may remain.

- [ ] **Step 3: Create the canonical JSON oracle**

Write the top-level source, rights, scope, anomaly, section-ledger, group, count, and ordered provision fields exactly as defined by the design. Include original concise paraphrases and precise dual-coordinate locators. Do not include source text, mappings, dispositions, relationships, or ESAF control references.

- [ ] **Step 4: Freeze exact counts in tests**

Set `EXPECTED_COUNT` to the reconciled integer and `EXPECTED_GROUP_COUNTS` to the reconciled group mapping. Add assertions that the oracle count, provision-array length, ledger atom sum, and group sum all equal that integer and that the group dictionary equals the accepted mapping.

- [ ] **Step 5: Run focused tests and verify GREEN**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_inventory -v
```

Expected: all focused tests pass with no warnings or cache files.

- [ ] **Step 6: Commit the reconciled oracle**

```powershell
git add docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-inventory-reconciliation.md tests/test_uk_cyber_essentials_plus_v32_inventory.py
git commit -m "Lock Cyber Essentials Plus v3.2 provision oracle"
```

---

### Task 4: Record rights approval and public roadmap boundary

**Files:**
- Modify: `crosswalks/uk-cyber-essentials.md`
- Modify: `project/BACKLOG.md`
- Modify: `tests/test_uk_cyber_essentials_plus_v32_inventory.py`
- Modify: `tests/test_release_metadata.py`
- Create: `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md`

**Interfaces:**
- Consumes: reconciled oracle and independent rights decision.
- Produces: source-rights evidence, public navigation, and next-activity metadata without a mapping claim.

- [ ] **Step 1: Obtain independent rights review**

The reviewer shall verify both official byte variants, NCSC attribution, OGL applicability, excluded third-party elements, logo and endorsement restrictions, and the separate IASME rights boundary. Record reviewer identity, date, source access authorization, permitted elements, prohibited elements, restrictions, and disposition.

- [ ] **Step 2: Add failing landing/backlog assertions**

Require the UK landing page to link the oracle, state public-v3.2-only completeness, identify core v3.3 and Plus v3.2 separately, disclose 2026 operational-context skew, and prohibit scheme-completeness/certification inference. Require the backlog's next activity to be mapping go/no-go review, not source-inventory design or implementation.

Run the two focused modules and verify the new assertions fail before changing the Markdown.

- [ ] **Step 3: Update narrative and queue**

Add a concise Plus source-inventory section to `crosswalks/uk-cyber-essentials.md`. Link the oracle and official sources, record both byte variants, state the rights and current-scheme boundary, publish the reconciled count derived from the oracle, and state that no mapping snapshot exists. Update the backlog to the exact next approved activity.

- [ ] **Step 4: Run focused tests and commit**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_inventory tests.test_release_metadata -v
git diff --check
git add crosswalks/uk-cyber-essentials.md project/BACKLOG.md tests/test_uk_cyber_essentials_plus_v32_inventory.py tests/test_release_metadata.py docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md
git commit -m "Publish Cyber Essentials Plus source inventory boundary"
```

---

### Task 5: Validate and independently review the exact candidate

**Files:**
- Create: `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-traceability.md`
- Modify only files already in scope if a review proves a defect.

**Interfaces:**
- Consumes: complete branch and exact candidate SHA.
- Produces: final gate evidence and a reviewable pull request; no mapping snapshot.

- [ ] **Step 1: Run the complete candidate gates**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_inventory -v
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
$base = git merge-base HEAD origin/main
python tools/validate_crosswalks.py --check --baseline-ref $base
git diff --check "$base..HEAD"
Get-ChildItem -Recurse -Directory -Filter __pycache__
git status --short
```

Expected: all tests and validators pass, no generated drift, no caches or rendered artifacts, and a clean tracked worktree.

- [ ] **Step 2: Record traceability on the candidate SHA**

Record source hashes, 24-page rendering evidence, independent author identities, independent counts before reconciliation, every difference disposition, final counts derived from the oracle, rights approval, changed files, exact commands/results, and the candidate SHA. Replace superseded evidence rather than appending contradictory totals.

- [ ] **Step 3: Dispatch exact-SHA specification/inventory review**

The reviewer shall verify source identity, section completeness, visual decisions, atom boundaries, IDs, kinds, summaries, locators, count derivation, and absence of mapping content. Resolve all Critical and Important findings.

- [ ] **Step 4: Dispatch exact-SHA security/overclaiming review independently**

The reviewer shall verify rights separation, version skew, actor/direction boundaries, sampling and point-in-time limits, the discretionary-exception interpretation, excluded Pathways work, and prohibited claims. Resolve all Critical and Important findings.

- [ ] **Step 5: Redispatch after every candidate change**

Any correction changes the candidate. Add focused regression coverage where practical, rerun all gates, replace superseded traceability totals, and redispatch both final reviews on the new exact SHA.

- [ ] **Step 6: Publish, merge, and validate merged main**

Push a short-lived branch and open a pull request referencing the design and implementation issue. Record the exact reviewed PR-head SHA and final results. Merge only when GitHub checks pass and the merge state is clean. Then update `main`, rerun focused tests and all three validators on the resulting merged-main SHA, verify a clean checkout, and remove the temporary branch, worktree, rendered pages, and source downloads.
