# ESAF 0.4-Alpha Closure and Planning Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile ESAF's 0.4-alpha planning and release metadata with the completed seven-pattern Draft architecture library while preserving every open publication and approval gate.

**Architecture:** Add one focused document-invariant test module, then make the smallest authoritative Markdown changes needed to satisfy those invariants. Keep release policy in `project/RELEASE_PLAN.md`, work sequencing in `project/BACKLOG.md`, publication history in `CHANGELOG.md`, and descriptive status in the existing overview files.

**Tech Stack:** Python 3 `unittest`, Markdown, Git, existing ESAF validators, GitHub CLI.

## Global Constraints

- 0.4-alpha remains a Working Draft and Unreleased.
- ARC-P100 through ARC-P160 remain Draft; this milestone does not approve or publish them.
- No pre-merge release gate may be marked complete without evidence tied to the exact reviewed candidate SHA, and no post-merge gate may be marked complete without evidence tied to the exact resulting merged-main SHA.
- Structural validation does not substitute for Mermaid rendering, qualified mapping review, or governance approval.
- Cyber Essentials core and Cyber Essentials Plus remain independently sourced artifacts.
- Markdown remains authoritative; no generated catalog changes are expected.
- Set `PYTHONDONTWRITEBYTECODE=1` for Python validation and leave no cache artifacts.

---

### Task 1: Add failing release-metadata invariants

**Files:**
- Create: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: `VERSION.md`, `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `project/BACKLOG.md`, `project/RELEASE_PLAN.md`, and `architectures/patterns/README.md`.
- Produces: `ReleaseMetadataTests`, a focused suite that locks version, stage, architecture inventory, backlog, and release-gate boundaries.

- [ ] **Step 1: Create the focused test module**

Implement helpers that read repository text, extract `Current Version` from `VERSION.md`, parse architecture registry rows, and isolate the current changelog section. Add tests that require:

```python
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def current_version() -> str:
    match = re.search(r"^Current Version: \*\*([^*]+)\*\*$", read("VERSION.md"), re.MULTILINE)
    if not match:
        raise AssertionError("VERSION.md does not declare Current Version")
    return match.group(1)


def architecture_rows() -> list[tuple[str, str]]:
    return re.findall(
        r"^\| \[(ARC-P\d{3})\]\([^)]*\) \| ([^|]+?) \| Draft \|$",
        read("architectures/patterns/README.md"),
        re.MULTILINE,
    )


class ReleaseMetadataTests(unittest.TestCase):
    def test_advertised_version_is_consistent(self) -> None:
        version = current_version()
        self.assertIn(f"version-{version.replace('-', '--')}-orange", read("README.md"))
        self.assertIn(f"**Version:** {version}", read("ROADMAP.md"))

    def test_current_stage_remains_unreleased_working_draft(self) -> None:
        version = current_version()
        self.assertIn("Status: **Working Draft**", read("VERSION.md"))
        self.assertIn(f"## {version} - Unreleased", read("CHANGELOG.md"))
        self.assertIn("Initial Reference Architecture Draft Library", read("VERSION.md"))

    def test_changelog_covers_every_registered_architecture(self) -> None:
        changelog = read("CHANGELOG.md")
        rows = architecture_rows()
        self.assertEqual(7, len(rows))
        for pattern_id, title in rows:
            with self.subTest(pattern_id=pattern_id):
                self.assertIn(pattern_id, changelog)
                self.assertIn(title.lower(), changelog.lower())

    def test_backlog_does_not_queue_existing_architecture_drafts(self) -> None:
        backlog = read("project/BACKLOG.md")
        for pattern_id, title in architecture_rows():
            with self.subTest(pattern_id=pattern_id):
                self.assertNotRegex(backlog.lower(), rf"draft[^\n]*(?:{pattern_id.lower()}|{re.escape(title.lower())})")

    def test_backlog_names_next_crosswalk_design_activity(self) -> None:
        backlog = read("project/BACKLOG.md")
        self.assertIn("Cyber Essentials Plus public-source acquisition and atomization design", backlog)
        self.assertIn("separate, source-versioned", backlog)

    def test_release_readiness_preserves_open_gate_boundaries(self) -> None:
        release = read("project/RELEASE_PLAN.md")
        for requirement in (
            "reviewed candidate SHA",
            "resulting merged-main SHA",
            "every Mermaid diagram",
            "qualified contributors",
            "governance approval",
            "must not be tagged or represented as released",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, release)
```

- [ ] **Step 2: Run the focused suite and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata -v
```

Expected: failures for the README badge, roadmap version, release stage, omitted changelog patterns, completed backlog work, missing next-activity wording, and missing readiness boundaries.

- [ ] **Step 3: Commit the failing invariants**

```powershell
git add tests/test_release_metadata.py
git commit -m "Test 0.4-alpha release metadata invariants"
```

---

### Task 2: Reconcile authoritative release and planning records

**Files:**
- Modify: `README.md`
- Modify: `ROADMAP.md`
- Modify: `VERSION.md`
- Modify: `CHANGELOG.md`
- Modify: `project/BACKLOG.md`
- Modify: `project/RELEASE_PLAN.md`
- Modify: `architectures/README.md`
- Modify: `architectures/patterns/README.md`
- Test: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: the failing invariants from Task 1 and the accepted closure design.
- Produces: internally consistent 0.4-alpha status, architecture history, active work queue, and explicit open release gates.

- [ ] **Step 1: Align version and stage descriptions**

Apply these exact outcomes:

- README badge advertises `0.4-alpha`.
- ROADMAP declares `**Version:** 0.4-alpha` and includes AI integration services in Phase 3.
- VERSION uses `Release Stage: **Initial Reference Architecture Draft Library**`.
- Architecture overview heading becomes `Initial pattern library` and states that the seven Draft patterns have been delivered through independently reviewable changes.
- Registry heading becomes `Initial drafting sequence` and uses past tense without changing registry statuses.

- [ ] **Step 2: Complete the 0.4-alpha changelog**

Add a short preamble stating that 0.2-alpha through 0.4-alpha are unreleased working-draft stages unless a section records a release date. Add precise 0.4-alpha bullets for ARC-P110, ARC-P140, ARC-P150, and ARC-P160, including ARC-P160 focused hardening. State that the Cyber Essentials snapshot is early Draft 0.5-beta work and does not complete the priority-crosswalk milestone. Change the release-stage bullet to `Initial Reference Architecture Draft Library`.

- [ ] **Step 3: Replace stale backlog items**

Retain the statement that GitHub Issues is authoritative, then list only active initiatives:

1. Complete the 0.4-alpha publication gates without promoting Draft artifacts prematurely.
2. Obtain qualified human review for the Cyber Essentials core v3.3 snapshot.
3. Complete Cyber Essentials Plus public-source acquisition and atomization design as a separate, source-versioned scheme artifact.
4. Establish substantive PCI DSS and HITRUST CSF mapping sets under ESAF-1600.
5. Define assessment evidence and maturity scoring.
6. Establish the planned industry profiles.

- [ ] **Step 4: Add the 0.4-alpha readiness record**

Keep the seven durable gates, then add a table with columns `Gate`, `Current state`, and `Required closure evidence`. Record architecture content as complete at Draft level, but every publication gate as Open. Tie pre-merge scope, review, full tests and three validators, global links and terminology review, rendering and readability review of every Mermaid diagram, qualified mapping review where mappings are in scope, synchronized metadata, governance approval, passing GitHub checks, and clean merge state to the exact reviewed PR-head/candidate SHA. Tie post-merge validation to the exact resulting merged-main SHA. End with:

> Until every applicable pre-merge gate is closed on the exact reviewed candidate SHA and post-merge validation passes on the exact resulting merged-main SHA, 0.4-alpha must not be tagged or represented as released.

- [ ] **Step 5: Run focused tests and verify GREEN**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata -v
python tools/validate_architectures.py
python tools/validate_controls.py --check
python tools/validate_crosswalks.py --check --baseline-ref (git merge-base HEAD main)
```

Expected: focused tests and all validators pass with no generated drift.

- [ ] **Step 6: Review and commit the reconciliation**

```powershell
rg -n 'TBD|TODO|PLACEHOLDER|lorem ipsum' README.md ROADMAP.md VERSION.md CHANGELOG.md project architectures tests/test_release_metadata.py
git diff --check
git diff -- README.md ROADMAP.md VERSION.md CHANGELOG.md project/BACKLOG.md project/RELEASE_PLAN.md architectures/README.md architectures/patterns/README.md tests/test_release_metadata.py
git add README.md ROADMAP.md VERSION.md CHANGELOG.md project/BACKLOG.md project/RELEASE_PLAN.md architectures/README.md architectures/patterns/README.md
git commit -m "Reconcile 0.4-alpha release planning"
```

---

### Task 3: Verify, review, and publish the candidate

**Files:**
- Modify only if review proves a defect in a file already in scope.

**Interfaces:**
- Consumes: the complete branch relative to `origin/main`.
- Produces: exact reviewed-candidate and resulting-merged-main validation evidence, independent review closure, a merged pull request, and a clean updated `main`.

- [ ] **Step 1: Run the complete local gate set**

Use a short drive alias for the worktree and run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
$base = git merge-base HEAD origin/main
python tools/validate_crosswalks.py --check --baseline-ref $base
git diff --check "$base..HEAD"
Get-ChildItem -Recurse -Directory -Filter __pycache__
git status --short
```

Expected: zero test failures, all validators pass, no whitespace errors, no cache directories, and no uncommitted changes.

- [ ] **Step 2: Dispatch independent whole-branch review**

Provide the reviewer the design, plan, base SHA, head SHA, and complete diff. Require classification as Critical, Important, or Minor. Resolve Critical and Important findings, add a focused regression test for any discovered document invariant when practical, commit corrections, and rerun Step 1 after every candidate change.

- [ ] **Step 3: Publish the pull request**

Push `agent/v04-alpha-closure` and open a pull request against `main`. The body shall record scope, non-release boundary, exact reviewed candidate SHA, exact test and validator results, review findings, and residual open publication gates.

- [ ] **Step 4: Verify GitHub state and merge**

Wait for all required checks, verify the PR head still equals the exact reviewed candidate SHA and the merge state is clean, then merge without bypassing checks. Verify merge completion before attempting local branch cleanup.

- [ ] **Step 5: Verify merged main and clean up**

Update local `main`, record the exact resulting merged-main SHA, rerun the focused release-metadata tests and all three validators on it, confirm a clean worktree and no caches, remove the temporary worktree, prune worktree metadata, and delete the local and remote feature branch.
