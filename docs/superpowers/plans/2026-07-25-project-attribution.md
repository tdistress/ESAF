# Project Attribution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record Eric Amos (Hearst) as ESAF's author, project maintainer, and lead contributor in the canonical repository files.

**Architecture:** Keep attribution in the existing author, contributor, and charter files. Treat Hearst only as Eric Amos's affiliation, leave repository ownership enforcement in `.github/CODEOWNERS`, and do not add attribution to normative publications.

**Tech Stack:** Markdown and Git validation commands.

## Global Constraints

- Use the exact name and affiliation `Eric Amos (Hearst)`.
- Do not imply that Hearst owns, sponsors, or endorses ESAF.
- Do not modify `.github/CODEOWNERS`, `README.md`, or normative ESAF publications.
- Preserve unrelated repository content.

---

### Task 1: Add canonical project attribution

**Files:**
- Modify: `AUTHORS.md`
- Modify: `CONTRIBUTORS.md`
- Modify: `PROJECT_CHARTER.md`

**Interfaces:**
- Consumes: Existing Markdown attribution placeholders and the project charter owner field.
- Produces: Canonical human-readable attribution for the repository.

- [ ] **Step 1: Confirm the expected placeholders and owner field**

Run:

```powershell
Get-Content -Raw AUTHORS.md
Get-Content -Raw CONTRIBUTORS.md
Select-String -Path PROJECT_CHARTER.md -Pattern '^\*\*Owner:\*\*'
```

Expected: the author and contributor files contain placeholder prose, and the charter owner is `ESAF Project Maintainers`.

- [ ] **Step 2: Replace the placeholders with exact role entries**

Set `AUTHORS.md` to:

```markdown
# Authors

- Eric Amos (Hearst), Author and Project Maintainer
```

Set `CONTRIBUTORS.md` to:

```markdown
# Contributors

- Eric Amos (Hearst), Lead Contributor
```

Set the `PROJECT_CHARTER.md` owner field to:

```markdown
**Owner:** Eric Amos (Hearst), Project Maintainer
```

- [ ] **Step 3: Verify exact attribution and excluded files**

Run:

```powershell
rg -n -F "Eric Amos (Hearst)" AUTHORS.md CONTRIBUTORS.md PROJECT_CHARTER.md
git diff -- .github/CODEOWNERS README.md framework controls architectures governance implementation assessment crosswalks data-model profiles
```

Expected: exactly one match appears in each of the three intended files, and the excluded-file diff is empty.

- [ ] **Step 4: Run repository validation**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
git diff --check
python -m unittest discover -s tests -v
git status --short
```

Expected: no whitespace errors, the full test suite passes, and status lists only the attribution files and this implementation plan.

- [ ] **Step 5: Commit the implementation**

Run:

```powershell
git add AUTHORS.md CONTRIBUTORS.md PROJECT_CHARTER.md docs/superpowers/plans/2026-07-25-project-attribution.md
git commit -m "docs: credit project author and maintainer"
```

Expected: Git creates one commit containing the plan and the three attribution changes.
