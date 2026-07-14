# AGENTS.md Durable Lessons Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add reusable whole-branch, Windows-worktree, and crosswalk-development lessons to ESAF's `AGENTS.md` without duplicating detailed procedures or preserving session-specific facts.

**Architecture:** Make one focused guidance-file change. Strengthen existing workflow and validation bullets, add a dedicated crosswalk-development section, and generalize the durable-lessons heading so the Windows path and report-coherence rules have an appropriate home.

**Tech Stack:** Markdown, Git, Python `unittest`, PowerShell, Git for Windows.

## Global Constraints

- Preserve all existing project-intent, editorial, authorization, and pause-handling guidance.
- Keep rules repository-wide or reusable across multiple crosswalks; do not add task-specific SHAs, counts, branch names, reviewer names, or Cyber Essentials procedures.
- Treat Markdown as the authoritative source.
- Run the full repository suite through a short Windows drive alias when the worktree path is deep.
- Run the final whitespace gate across the complete branch diff with `git diff --check <merge-base>..HEAD`.

---

### Task 1: Update durable repository guidance

**Files:**
- Modify: `AGENTS.md`
- Test: `AGENTS.md` through content assertions and repository validation commands

**Interfaces:**
- Consumes: the approved design in `docs/superpowers/specs/2026-07-14-agents-memory-lessons-design.md` and the existing `AGENTS.md` conventions.
- Produces: future-session guidance for whole-branch validation, deep Windows worktrees, coherent evidence, and conservative crosswalk development.

- [ ] **Step 1: Run a content assertion to verify the new rules are absent**

```powershell
@'
from pathlib import Path

text = Path("AGENTS.md").read_text(encoding="utf-8")
required = [
    "git diff --check <merge-base>..HEAD",
    "## Crosswalk development lessons",
    "must not supply a missing external outcome",
    "distinct referenced-control count",
    "short drive alias",
]
missing = [item for item in required if item not in text]
assert not missing, f"missing durable rules: {missing}"
'@ | python -
```

Expected: FAIL with all five durable rules reported missing.

- [ ] **Step 2: Strengthen the final whole-branch and evidence rules**

In `AGENTS.md`:

1. Replace the existing validation bullet `Run git diff --check` with language requiring ordinary working-tree checks during development and `git diff --check <merge-base>..HEAD` for final branch review.
2. Add review-discipline bullets requiring traceability statements to match the exact candidate SHA and actual gate results, and requiring task reports to replace superseded totals rather than retain contradictory earlier statements.

- [ ] **Step 3: Add the crosswalk-development section**

Add this section before `## Collaboration preferences`:

```markdown
## Crosswalk development lessons

- Pin authoritative external sources by official URL, version, publication date, and checksum. Lock provision identifiers, summaries, and locators in a machine-readable oracle when feasible.
- Default to `no_direct_mapping` when ESAF does not expressly provide the external outcome. Conditions may narrow or qualify an existing relationship, but they must not supply a missing external outcome.
- Distinguish `prerequisite` from `partially_supports` using exact normative control text; implementation guidance and adjacent capabilities are insufficient by themselves.
- Treat whitespace-only mapping-record edits as snapshot changes when registries or catalogs use content digests. Regenerate and validate every dependent artifact.
- Derive published statistics from records and manifests. Keep the pinned control population, relationship-leg count, distinct referenced-control count, and negative-disposition count separate.
- Keep adjacent assurance schemes independently sourced and mapped; do not infer one scheme's requirements or assurance from another.
- For substantial crosswalks, require separate specification/inventory and security/overclaiming reviews on the exact final SHA. Redispatch both reviews after any candidate change.
```

- [ ] **Step 4: Generalize and extend durable implementation lessons**

Rename `## Durable lessons from ARC-P150` to `## Durable implementation lessons`, retain its existing bullets, and append:

```markdown
- On Windows, deeply nested project-local worktrees can make tracked files unreadable to Python or PowerShell even when Git reports a clean checkout. Use a short drive alias, run tests and tools through it, and verify the longest tracked paths before diagnosing missing repository content.
- Keep implementation and review reports internally coherent. Replace superseded totals or conclusions instead of appending corrections that leave contradictory earlier evidence.
```

- [ ] **Step 5: Run the focused content assertion**

Run the Step 1 command again.

Expected: PASS with exit code 0.

- [ ] **Step 6: Review the complete guidance diff**

```powershell
git diff -- AGENTS.md
rg -n "T[B]D|T[O]DO|implement lat[e]r|fill in deta[i]ls" AGENTS.md
git diff --check
```

Expected: the diff contains only approved durable guidance; the placeholder scan returns no matches; the working-tree whitespace check exits 0.

- [ ] **Step 7: Run the repository suite from the short drive alias**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -q
```

Expected: 197 tests pass with only the 3 environment-dependent Windows symlink skips.

- [ ] **Step 8: Commit the implementation**

```powershell
git add -- AGENTS.md
git commit -m "Record durable crosswalk development lessons"
```

- [ ] **Step 9: Run the final branch-wide whitespace gate**

```powershell
git diff --check origin/main..HEAD
git status --short
```

Expected: the branch-wide whitespace check exits 0 and the worktree is clean.
