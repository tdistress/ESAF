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
- A rights reviewer independent of both inventory authors shall approve the exact publication basis before any source-derived inventory, ledger, paraphrase, or oracle enters Git.
- Every PDF page shall be rendered and visually inspected; text extraction alone is insufficient.
- No mapping snapshot, lifecycle record, control manifest, provision mapping record, relationship leg, or generated mapping statistic shall be created.
- No certification, compliance, equivalence, endorsement, predictive-sufficiency, full-population, continuous-assurance, or current-scheme-completeness claim is permitted.
- All PDFs, renderings, independent inventories, page ledgers, and comparison files shall live beneath a verified system-temporary directory outside the repository; `.superpowers` shall not be used for scratch data.
- Python validation shall set `PYTHONDONTWRITEBYTECODE=1` and leave no cache, scratch, source-download, or rendered-page artifact in the repository.

---

### Task 1: Lock the source, rights, and closed oracle contract in failing tests

**Files:**
- Create: `tests/test_uk_cyber_essentials_plus_v32_inventory.py`
- Expected later: `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`

**Interfaces:**
- Consumes: the approved design, NCSC resource page, canonical and legacy official PDFs.
- Produces: `CyberEssentialsPlusV32InventoryTests`, source constants, section/group contracts, and oracle validation helpers used by later tasks.

- [ ] **Step 1: Write source and absence tests**

Create the focused module with the exact source constants below and initial tests. Access source identity through the nested closed contract (`oracle["source"]` and its two ordered `variants`), not legacy top-level aliases:

```python
from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
SOURCE_TITLE = "Cyber Essentials Plus Test Specification"
SOURCE_AUTHORITY = "UK National Cyber Security Centre"
PUBLICATION_IDENTIFIER = "cyber-essentials-plus-test-specification"
DISPLAY_DATE = "April 2025"
RESOURCE_PAGE = "https://www.ncsc.gov.uk/cyberessentials/resources"
RESOURCE_PAGE_DATE = "2025-04-28"
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
RIGHTS_ELEMENTS = (
    "identifiers", "titles", "structural_inventory", "paraphrases",
    "derivative_mapping_analysis", "official_links",
)
PROHIBITED_INFERENCES = (
    "certification", "compliance", "equivalence", "endorsement",
    "predictive_sufficiency", "full_population_assurance",
    "continuous_assurance", "current_scheme_completeness",
)


class CyberEssentialsPlusV32InventoryTests(unittest.TestCase):
    def oracle(self) -> dict:
        return json.loads(ORACLE.read_text(encoding="utf-8"))

    def test_locked_oracle_exists(self) -> None:
        self.assertTrue(ORACLE.is_file())

    def test_source_identity_is_exact(self) -> None:
        oracle = self.oracle()
        source = oracle["source"]
        self.assertEqual(SOURCE_TITLE, source["title"])
        self.assertEqual(SOURCE_AUTHORITY, source["authority"])
        self.assertEqual(PUBLICATION_IDENTIFIER, source["publication_identifier"])
        self.assertEqual("3.2", source["version"])
        self.assertEqual(DISPLAY_DATE, source["display_date"])
        self.assertEqual(RESOURCE_PAGE, source["resource_page_url"])
        self.assertEqual(RESOURCE_PAGE_DATE, source["resource_page_date"])
        self.assertEqual(24, source["pdf_page_count"])
        self.assertEqual(
            [("canonical", CANONICAL_URL, CANONICAL_BYTES, CANONICAL_SHA256),
             ("legacy", LEGACY_URL, LEGACY_BYTES, LEGACY_SHA256)],
            [(v["role"], v["url"], v["byte_length"], v["sha256"])
             for v in source["variants"]],
        )
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

- exact top-level and nested property sets, required types, nullability, formats, and rejection of unknown properties for every object described in design section 9.2;
- exact `schema_version` and `atomization_rule_version` boundaries;
- `scope.type == "complete_publication"` and a scope statement bounded to the public v3.2 PDF;
- exact NCSC/OGL attribution and an explicit separate IASME-rights limitation;
- exact equality with `RIGHTS_ELEMENTS`; permitted/prohibited disjointness and exhaustiveness; `permitted_elements == list(RIGHTS_ELEMENTS)`; `prohibited_elements == []`; and a restriction explicitly prohibiting copied source text;
- the rights reviewer differs from both `inventory_provenance.authors`, the provenance records the committed rights-review SHA, and Git history proves that SHA precedes the first source-derived inventory commit;
- the exact direction boundary: the oracle establishes no mapping direction, future `esaf_to_external` and `external_to_esaf` directions are listed in that order, and they are assessed independently;
- `section_ledger` occurrence entries with hierarchical IDs, parents, repeated-heading-safe identity, group, PDF/printed ranges, decision, rationale, and atom count;
- exact equality with an independently specified ordered section-occurrence ID set added only during reconciliation;
- every provision's required `section_id` referencing one included occurrence, with ledger counts derived from those links;
- ledger, group, and total counts agreeing with `len(provisions)`;
- unique, ordered record and external IDs matching `cepts32-<group>-NNN` and `CEPTS3.2-<GROUP>-NNN`;
- valid controlled `kind`; nonempty controlled `actors` drawn only from `Assessor`, `Applicant`, `Certification Body`, `Certifying Body`, and `Delivery Partner`; multiple actors permitted only with recorded source support; nonempty original summary; and structured dual-coordinate locator;
- structured assurance limits covering scope, population/sample, assessment/evidence dates, tool/provenance, point-in-time status, `discretion_owner == "Delivery Partner"`, one Delivery Partner discretionary exception whose predicate IDs/meanings are exactly `marginal-deviation-under-five-percent` / `a marginal deviation in less than 5% of performed tests` and `no-wider-process-failure-evidence` / `no evidence of wider failure of Applicant cybersecurity processes`, `all_predicates_required is True`, explicit false automatic-pass and 95-percent-score flags, and `prohibited_inferences == list(PROHIBITED_INFERENCES)`;
- the Figure 1 source-label set exactly equal to `Figure 1 decision 1` through `Figure 1 decision 7`;
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
- Create first in repository: `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md`
- Create outside repository beneath one verified system-temporary directory: canonical and legacy PDFs, 24 rendered canonical page images, `inventory-a.json`, `inventory-b.json`, `page-review-a.md`, `page-review-b.md`, and comparison output

**Interfaces:**
- Consumes: exact source constants and atomization rules from the design.
- Produces: an independently approved and committed rights record, followed by two independent atom lists and page-review ledgers; no tracked source-derived oracle before rights approval.

- [ ] **Step 1: Create and verify a system-temporary workspace**

Create a unique child of `[System.IO.Path]::GetTempPath()` (for example with `[System.IO.Path]::GetRandomFileName()`). Resolve both the system temp root and child with `[System.IO.Path]::GetFullPath()`, require the child to start with the temp root plus a directory separator, and require it not to start with the repository root. Stop otherwise. Record the resolved temporary path outside tracked evidence because it is ephemeral. Never use repository-local `.superpowers` scratch.

- [ ] **Step 2: Re-fetch and verify both official variants**

Download both URLs to the verified temporary directory. Verify media type, byte length, SHA-256, PDF page count, title, displayed version, displayed date, copyright, licence, and current resource-page target. Stop if the resource-page target or canonical bytes differ from the design.

- [ ] **Step 3: Obtain and commit independent rights approval**

Before creating any inventory or section ledger, a named reviewer who will be neither inventory author shall verify both exact byte variants, NCSC attribution, OGL applicability and publication basis, the exact six-element ESAF-1600 rights universe, permission for all six elements, an empty prohibited-element set, the copied-source-text prohibition in restrictions, excluded third-party elements, logo/mark and endorsement restrictions, and the separate IASME rights partition. Record reviewer identity, date, both hashes, publication basis, permitted and prohibited elements, restrictions, and an approved/rejected disposition. Commit only the approved rights record:

```powershell
git add docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md
git commit -m "Approve Cyber Essentials Plus inventory rights"
```

Do not continue if the reviewer is an inventory author or the disposition is not unconditionally approved for every planned oracle field class.

- [ ] **Step 4: Render all canonical pages**

Use the bundled Poppler runtime:

```powershell
pdftoppm -png -r 150 $canonicalPdf $temporaryPrefix
```

Expected: 24 nonempty PNG files. Inspect every page for operative tables, figures, branches, footnotes, and layout-dependent conditions. Record PDF and printed page coordinates.

- [ ] **Step 5: Dispatch inventory author A**

Author A reads the approved design and all 24 rendered pages. They create temporary `inventory-a.json` and `page-review-a.md` with a complete hierarchical section-occurrence ledger and ordered atom list, including `section_id`, controlled `actors`, and structured locators. They shall not see Author B's provisional list, ledger, occurrence set, or count.

- [ ] **Step 6: Dispatch inventory author B independently**

Author B receives the same source and rules but no Author A output. They create temporary `inventory-b.json` and `page-review-b.md`. They shall not see Author A's provisional list, ledger, occurrence set, or count.

- [ ] **Step 7: Verify independent deliverables without freezing a count**

Confirm both authors reviewed 24 pages, accounted for every substantive occurrence including repeated headings, produced parent-valid section IDs and provision links, included the exact Figure 1 decision-label set 1 through 7, recorded the `tests 2 to 7` anomaly, and produced internally consistent unique IDs and counts. Confirm both authors differ from the rights reviewer. Do not average, choose, or publish any count or occurrence set at this step.

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

Compare inventories by section occurrence, source location, kind, actors, action/criterion, condition, and outcome. List additions, omissions, section-parent and coordinate differences, boundary differences, ID differences, kind/actor differences, summary differences, and locator differences. Preserve both originals only in the verified temporary directory until reconciliation is accepted.

- [ ] **Step 2: Disposition every difference**

For each difference, record both proposals, the selected result, exact source evidence, atomization-rule rationale, and reconciler. Independently specify and lock the exact ordered hierarchical section-occurrence set, including coordinates, group, and repeated heading occurrences, without deriving it from either author's eventual provision count. Re-open rendered pages whenever text extraction or paragraph context is ambiguous. No unresolved difference may remain.

- [ ] **Step 3: Create the canonical JSON oracle**

Write every required property of the closed contract in design section 9.2 and no others. Record both inventory authors, reconciler, and the actual rights-record commit in `inventory_provenance`; prove that commit is an ancestor before proceeding. Include original concise paraphrases, controlled actors and actor basis, exact section links, structured dual-coordinate locators without a duplicate source label, the exact no-direction boundary, and structured assurance limits. Encode one Delivery Partner discretionary exception with both exact conjunctive predicates, `all_predicates_required: true`, `automatic_pass: false`, and `is_95_percent_score: false`; require the exact eight-value prohibited-inference set. Do not include source text, mappings, dispositions, relationships, or ESAF control references.

- [ ] **Step 4: Freeze exact counts in tests**

Only now set `EXPECTED_COUNT` to the reconciled integer and `EXPECTED_GROUP_COUNTS` to the reconciled group mapping. Set `EXPECTED_SECTION_IDS` to the independently specified exact ordered occurrence set. Add assertions for exact schema/property/type/nullability conformance; exact occurrence-set equality and valid parents; one valid included `section_id` per provision; ledger counts derived from provision links; group and total derivation; controlled actors and evidence for multi-actor atoms; no locator-level source label; exact Figure 1 labels 1 through 7; one conjunctive exception with the exact predicate IDs and meanings; false automatic-pass/95-percent-score flags; the exact eight-value prohibited-inference set; and the exact direction boundary.

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

### Task 4: Re-attest rights coverage and publish the public roadmap boundary

**Files:**
- Modify: `crosswalks/uk-cyber-essentials.md`
- Modify: `project/BACKLOG.md`
- Modify: `tests/test_uk_cyber_essentials_plus_v32_inventory.py`
- Modify: `tests/test_release_metadata.py`
- Modify: `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md`

**Interfaces:**
- Consumes: reconciled oracle and independent rights decision.
- Produces: re-attested source-rights evidence, public navigation, and next-activity metadata without a mapping claim.

- [ ] **Step 1: Re-attest the prior independent rights decision**

The same independent rights reviewer shall compare the reconciled oracle and narrative field classes with the already approved publication basis, confirm that every committed source-derived class is covered, confirm that no IASME-derived structure or text crossed the partition, and record a re-attestation. This is confirmation of the pre-inventory gate, not a retroactive permission decision. Any expanded publication basis requires stopping, removing the unapproved derived material from the candidate, and obtaining a new approval before it re-enters Git.

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
- Create: `tools/validate_links.py`
- Create: `tests/test_validate_links.py`
- Modify only files already in scope if a review proves a defect.

**Interfaces:**
- Consumes: complete branch and exact candidate SHA.
- Produces: a general repository-local Markdown link validator, tracked pending traceability without a self-referential SHA, external exact-head review evidence, and a reviewable pull request; no mapping snapshot.

- [ ] **Step 1: Add a general link validator test-first**

Write failing tests for `tools/validate_links.py` that cover every tracked Markdown file, relative and repository-root paths, directory-index targets, fragments/anchors, URL-decoding, missing targets, missing anchors, repository escapes, and ignored external/network URLs. Implement a deterministic `--check` command that returns nonzero and reports file/line/target for broken repository-local links. Run focused tests RED then GREEN, and use this explicit general command in all candidate gates:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_links -v
python tools/validate_links.py --check
```

- [ ] **Step 2: Run preliminary gates and create pending traceability**

Run the complete commands below, then create traceability with status `Pending exact-head reviews`. It shall contain source hashes, rights approval and re-attestation, 24-page rendering evidence, independent author identities and independence from the rights reviewer, independent pre-reconciliation counts, the exact reconciled occurrence set, difference dispositions, final counts derived from provision links, changed files, and command/result evidence. It shall not contain or reserve a field for its own commit SHA, candidate SHA, reviewed SHA, or merged SHA. Commit the validator, tests, and pending traceability before final gates:

```powershell
git add tools/validate_links.py tests/test_validate_links.py docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-traceability.md
git commit -m "Record Cyber Essentials Plus inventory traceability"
```

- [ ] **Step 3: Run the complete final gates on the immutable candidate head**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_plus_v32_inventory -v
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
$base = git merge-base HEAD origin/main
python tools/validate_crosswalks.py --check --baseline-ref $base
python tools/validate_links.py --check
git diff --check "$base..HEAD"
Get-ChildItem -Recurse -Directory -Filter __pycache__
git status --short
```

Expected: all tests and validators pass, no generated drift, no caches, temporary files, source downloads, or rendered artifacts in the repository, and a clean tracked worktree. Record the resulting `git rev-parse HEAD` only in external dispatch and PR/check evidence; do not edit tracked traceability after this point.

Before dispatch, read `inventory_provenance.rights_record_commit` into `$rightsSha`, set `$reviewedPrHead = git rev-parse HEAD`, and run `git merge-base --is-ancestor $rightsSha $reviewedPrHead`; throw if the exit code is nonzero. Record that pre-review ancestry result externally with `$reviewedPrHead`.

- [ ] **Step 4: Dispatch exact-SHA specification/inventory review**

The reviewer shall verify source identity, section completeness, visual decisions, atom boundaries, IDs, kinds, summaries, locators, count derivation, and absence of mapping content. Resolve all Critical and Important findings.

- [ ] **Step 5: Dispatch exact-SHA security/overclaiming review independently**

The reviewer shall verify rights-review sequencing and independence, the exact six-element rights partition and copied-source-text restriction, version skew, controlled actor and direction boundaries, scope/population/sample/date/tool/provenance/point-in-time limits, the Delivery Partner's one discretionary exception with both required conjunctive predicates and no automatic-pass/95-percent-score interpretation, excluded Pathways work, and the exact eight prohibited inferences. Resolve all Critical and Important findings.

- [ ] **Step 6: Redispatch after every candidate change**

Any correction changes the candidate. Add focused regression coverage where practical, replace superseded tracked traceability evidence rather than appending contradictions, commit, rerun every final gate, and redispatch both reviews on the new exact SHA. Once both reviews pass on one immutable head, make no further tracked change. Record the reviewed PR-head SHA, review identities/dispositions, final command results, and GitHub check results only in the PR body, PR comments, or check evidence.

- [ ] **Step 7: Publish, merge, validate, and clean temporary material**

Push the short-lived branch and open or update a pull request referencing the design and implementation issue. Confirm the PR head exactly equals `$reviewedPrHead` and rerun `git merge-base --is-ancestor $rightsSha $reviewedPrHead` before integration. Merge using a true merge commit only; squash and rebase integration are prohibited because they discard the committed rights-review ancestry. Merge only when both exact-head reviews pass, GitHub checks pass on that same head, the ancestry check passes, and the merge state is clean. Then update `main` and run:

```powershell
$mergedMainSha = git rev-parse HEAD
$parents = (git rev-list --parents -n 1 $mergedMainSha).Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries)
if ($parents.Count -lt 3) { throw "Merged main is not a merge commit" }
git merge-base --is-ancestor $rightsSha $mergedMainSha
if ($LASTEXITCODE -ne 0) { throw "Rights-review commit ancestry was not preserved" }
```

Record the resulting main SHA, merge-commit verification, and post-merge rights ancestry externally in the PR/issue evidence. Rerun focused tests, all three domain validators, and `python tools/validate_links.py --check` on that merged-main SHA; verify a clean checkout; verify the temporary workspace still resolves beneath the system temp root and outside the repository; remove that exact temporary child; and remove the temporary branch and worktree. Never recursively remove an unverified computed path.
