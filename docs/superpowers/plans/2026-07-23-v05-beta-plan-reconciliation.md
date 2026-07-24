# ESAF 0.5-Beta Plan Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile the completed `v0.4-alpha` publication state, define a bounded and testable `v0.5-beta` milestone, and restore GitHub as the authoritative scheduled work queue.

**Architecture:** Extend the release-gate validator with a durable `published` record state while preserving the existing closure-candidate controller. Transition the tracked 0.4-alpha record and release metadata to that state, encode the bounded 0.5-beta milestone in project documents and regression tests, merge the reviewed branch, then create the approved GitHub milestone and issues from the merged plan.

**Tech Stack:** Python 3 standard library, `unittest`, PyYAML front matter, Markdown, Git, GitHub CLI, PowerShell.

## Global Constraints

- The binding design is `docs/superpowers/specs/2026-07-23-v05-beta-plan-reconciliation-design.md`.
- Preserve the immutable publication date `2026-07-23`.
- Preserve annotated tag object `2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f`.
- Preserve peeled commit `8abfe5a85db19d11295a0c3debeb2d58109b0ca7`.
- Preserve consolidated evidence locator `https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764`.
- Preserve `mapping_decision_basis: owner_risk_acceptance` and all Draft lifecycle limitations.
- Do not rewrite the tag, historical decision timestamps, or publication date.
- Do not advance `VERSION.md` or `ROADMAP.md` beyond current version `0.4-alpha`.
- Do not require all roadmap mappings, all nine profiles, a full assessment toolkit, or a substantive HITRUST mapping for `v0.5-beta`.
- Do not create the GitHub milestone or issues until the repository planning changes have merged.
- Set `PYTHONDONTWRITEBYTECODE=1` for Python validation and leave no `__pycache__` directory.
- Resolve every Critical and Important review finding before merge.
- Do not remove unrelated existing worktrees or branches.

---

### Task 1: Add the durable published-release validator contract

**Files:**
- Modify: `tests/test_release_gates.py`
- Modify: `tools/release_gates.py`

**Interfaces:**
- Consumes: the existing `validate_record(root: Path, record: dict[str, object]) -> list[str]` and command-line `--check` mode.
- Produces: validation for `phase: published` with fixed publication evidence, eight closed gates, and no current-date or baseline requirement.
- Preserves: `evidence_candidate` and `closure_candidate` behavior, including current-date validation for an active closure candidate.

- [ ] **Step 1: Add a synthetic published-record fixture**

Add these constants and fixture beside `closure_record` in
`tests/test_release_gates.py`:

```python
PUBLISHED_DATE = "2026-07-23"
PUBLISHED_TAG_OBJECT = "2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f"
PUBLISHED_COMMIT = "8abfe5a85db19d11295a0c3debeb2d58109b0ca7"
PUBLISHED_EVIDENCE = (
    "https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764"
)


def published_record() -> dict[str, object]:
    record = valid_record()
    record["phase"] = "published"
    record["publication"] = {
        "date": PUBLISHED_DATE,
        "condition": "remote_annotated_tag_matches_exact_validated_commit",
        "tag_object": PUBLISHED_TAG_OBJECT,
        "tagged_commit": PUBLISHED_COMMIT,
        "evidence": PUBLISHED_EVIDENCE,
    }
    record["gates"] = {
        gate: {
            "state": "closed",
            "evidence": [PUBLISHED_EVIDENCE],
        }
        for gate in GATE_IDS
    }
    record["mapping_decision_basis"] = "owner_risk_acceptance"
    return record
```

Add a `write_published_scope_fixture(root: Path) -> None` helper that calls
`write_release_scope_fixture(root)` and replaces the copied release plan with:

```markdown
# Release Plan

## 0.4-alpha publication

Publication gates are Closed.

Evidence: https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764

Validated commit: 8abfe5a85db19d11295a0c3debeb2d58109b0ca7
```

Use this temporary fixture for synthetic published-record validation. Do not
make those tests depend on the still-open authoritative release plan before
Task 2.

- [ ] **Step 2: Add failing published-record tests**

Add tests that require:

```python
def test_published_record_accepts_fixed_historical_evidence(self) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        write_published_scope_fixture(root)
        self.assertEqual(validate_record(root, published_record()), [])


def test_published_record_rejects_mutated_publication_evidence(self) -> None:
    cases = (
        ("date", "2026-07-24", "published date shall equal 2026-07-23"),
        ("tag_object", "a" * 40, "published tag object is invalid"),
        ("tagged_commit", "b" * 40, "published tagged commit is invalid"),
        ("evidence", "http://example.test/evidence", "published evidence locator is invalid"),
    )
    for field, value, diagnostic in cases:
        with self.subTest(field=field):
            record = published_record()
            record["publication"][field] = value
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                write_published_scope_fixture(root)
                self.assertIn(diagnostic, validate_record(root, record))


def test_published_record_requires_every_gate_closed(self) -> None:
    record = published_record()
    record["gates"]["technical"]["state"] = "ready"
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        write_published_scope_fixture(root)
        self.assertIn(
            "technical: published gate shall be closed",
            validate_record(root, record),
        )
```

Add a CLI test that writes `published_record()` to the authoritative record
path in a temporary fixture and runs:

```python
[sys.executable, str(root / "tools/release_gates.py"), "--check"]
```

Require exit code `0` without `--baseline-ref`. Add a second assertion invoking
the same command with `--external-evidence`, `--expected-head`, and `--phase`;
require a nonzero result containing:

```text
external evidence is not accepted for a published record
```

- [ ] **Step 3: Run the focused tests and verify the new tests fail**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_gates -v
```

Expected: the new published-state tests fail because `published` is not an
accepted phase, SHA fields are prohibited, the closed-state contract is absent,
and the CLI has no published-record branch.

- [ ] **Step 4: Implement phase-specific release validation**

In `tools/release_gates.py`, add:

```python
PUBLISHED_DATE = "2026-07-23"
PUBLISHED_TAG_OBJECT = "2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f"
PUBLISHED_COMMIT = "8abfe5a85db19d11295a0c3debeb2d58109b0ca7"
PUBLISHED_EVIDENCE = (
    "https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764"
)
PUBLISHED_SHA_PATHS = {
    "publication.tag_object": PUBLISHED_TAG_OBJECT,
    "publication.tagged_commit": PUBLISHED_COMMIT,
}
```

Replace the phase check with:

```python
phase = record.get("phase")
if phase not in {"evidence_candidate", "closure_candidate", "published"}:
    errors.append(
        "phase shall be evidence_candidate, closure_candidate, or published"
    )
```

Retain existing candidate validation. Add a published branch requiring the
exact date, condition, tag object, tagged commit, and evidence locator. Validate
that every published gate is `closed`. Use these exact diagnostics:

```text
published date shall equal 2026-07-23
published tag object is invalid
published tagged commit is invalid
published evidence locator is invalid
<gate>: published gate shall be closed
```

Change the SHA prohibition loop so only the two exact published SHA paths are
allowed:

```python
for path, value in flattened_items(record):
    if path in PUBLISHED_SHA_PATHS:
        if value != PUBLISHED_SHA_PATHS[path]:
            errors.append(f"{path}: published identifier is invalid")
        continue
    if "sha" in path.casefold() or "commit" in path.casefold():
        errors.append(f"{path}: tracked record shall not contain SHA fields")
    if isinstance(value, str) and SHA_RE.search(value):
        errors.append(f"{path}: tracked record shall not contain a 40-character SHA")
```

Split release-plan markers by phase. Candidate validation shall retain the
historical open-gate markers. Published validation shall require:

```python
PUBLISHED_RELEASE_PLAN_MARKERS = (
    "## 0.4-alpha publication",
    "Publication gates are Closed.",
    PUBLISHED_EVIDENCE,
    PUBLISHED_COMMIT,
)
```

Update the two existing tests that call `validate_record(ROOT, closure_record())`
or `validate_record(ROOT, valid_record())` after the authoritative release plan
becomes published. Run those synthetic candidate records against temporary
fixtures containing `RELEASE_PLAN_MARKERS`; keep the authoritative-record test
against `ROOT`. This preserves coverage for both state machines without
requiring the current repository to be simultaneously candidate and
published.

In `main`, preserve the baseline requirement only for
`phase == "closure_candidate"`. If external evidence arguments are supplied for
a published record, add:

```text
external evidence is not accepted for a published record
```

Do not call `validate_external_evidence` for a published record.

- [ ] **Step 5: Run focused tests and make them pass**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_gates -v
```

Expected: all release-gate tests pass. Existing closure-candidate mutation
tests continue to use today's UTC date and remain unchanged.

- [ ] **Step 6: Commit the validator contract**

```powershell
git add -- tests/test_release_gates.py tools/release_gates.py
git diff --cached --check
git commit -m "Support durable published release records"
```

---

### Task 2: Transition 0.4-alpha from candidate to published

**Files:**
- Modify: `tests/test_release_metadata.py`
- Modify: `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md`
- Modify: `project/RELEASE_PLAN.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the published-record validator from Task 1.
- Produces: the authoritative `v0.4-alpha` published record and durable human-readable release history.
- Preserves: current version `0.4-alpha`, Working Draft status, owner-risk basis, separate governance approval, and all Draft non-claims.

- [ ] **Step 1: Replace date-sensitive metadata tests with published-state tests**

Change `current_changelog_section` so a current heading accepts either
`Unreleased` or a fixed ISO date, without requiring `(conditional)`:

```python
rf"^## {re.escape(version)} - (?:Unreleased|\d{{4}}-\d{{2}}-\d{{2}})$"
```

Replace `test_current_changelog_section_is_conditionally_dated` with:

```python
def test_current_changelog_section_records_published_working_draft(self) -> None:
    changelog = read_repository_file("CHANGELOG.md")
    self.assertEqual(
        1,
        len(re.findall(
            r"^## 0\.4-alpha - 2026-07-23$",
            changelog,
            re.MULTILINE,
        )),
    )
    self.assertNotIn("0.4-alpha - 2026-07-23 (conditional)", changelog)
```

Replace the closure-candidate test with assertions for:

```python
self.assertEqual("published", record["phase"])
self.assertEqual(date(2026, 7, 23), record["publication"]["date"])
self.assertEqual(PUBLISHED_TAG_OBJECT, record["publication"]["tag_object"])
self.assertEqual(PUBLISHED_COMMIT, record["publication"]["tagged_commit"])
self.assertEqual(PUBLISHED_EVIDENCE, record["publication"]["evidence"])
self.assertTrue(all(value["state"] == "closed" for value in record["gates"].values()))
```

Import `date` from `datetime` and define the three publication constants in
the test module.

Add a local tag-resolution test:

```python
def test_recorded_annotated_tag_matches_local_repository(self) -> None:
    tag_object = subprocess.run(
        ["git", "rev-parse", "v0.4-alpha"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    peeled_commit = subprocess.run(
        ["git", "rev-parse", "v0.4-alpha^{commit}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    self.assertEqual(PUBLISHED_TAG_OBJECT, tag_object)
    self.assertEqual(PUBLISHED_COMMIT, peeled_commit)
```

Add `import subprocess`.

- [ ] **Step 2: Run focused metadata tests and verify failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata -v
```

Expected: failures show that the record is still a closure candidate, the
gates are `ready`, the changelog is conditional, and the release plan remains
open.

- [ ] **Step 3: Update the authoritative publication record**

In
`docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md`:

- set `phase: published`;
- add the exact `tag_object`, `tagged_commit`, and `evidence` fields under
  `publication`;
- change all eight gate states from `ready` to `closed`;
- preserve their stable HTTPS evidence;
- replace candidate and future-tense wording with satisfied, historical
  publication wording; and
- preserve owner-risk, deferred-qualified-review, and Draft limitations.

The current-state section shall explicitly state:

```text
The v0.4-alpha Working Draft was published through the remote annotated tag
v0.4-alpha. The tag condition was satisfied on 2026-07-23 and the tag peels to
the exact validated merged-main commit recorded in front matter.
```

- [ ] **Step 4: Reconcile the release plan**

Rename the section to:

```markdown
## 0.4-alpha publication
```

State `Publication gates are Closed.` Replace every table state with `Closed`
and use stable final evidence locators. Record the tag object, peeled commit,
issue `#39`, owner-risk basis, deferred qualified review, and separate Steering
Committee approval.

Remove future-tense statements that the release shall not be tagged. Replace
them with a historical boundary stating that this evidence closes only
`v0.4-alpha` and cannot approve a later release.

- [ ] **Step 5: Reconcile the changelog**

Change:

```markdown
## 0.4-alpha - 2026-07-23 (conditional)
```

to:

```markdown
## 0.4-alpha - 2026-07-23
```

Change the preamble to say `0.2-alpha` and `0.3-alpha` remain unreleased
working-draft stages, while `0.4-alpha` is a tagged Working Draft. Replace the
conditional-candidate bullets with a statement that the annotated-tag
condition was satisfied. Preserve every limitation and do not call it stable,
qualified, compliant, certified, equivalent, endorsed, assured, or
production-ready.

- [ ] **Step 6: Run focused release tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata -v
python -m unittest tests.test_release_gates -v
python tools/release_gates.py --check
```

Expected: all commands exit `0`.

- [ ] **Step 7: Commit the published-state transition**

```powershell
git add -- tests/test_release_metadata.py `
  docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md `
  project/RELEASE_PLAN.md CHANGELOG.md
git diff --cached --check
git commit -m "Record published 0.4-alpha state"
```

---

### Task 3: Define the bounded 0.5-beta milestone

**Files:**
- Modify: `tests/test_release_metadata.py`
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`

**Interfaces:**
- Consumes: the approved design's entry state, five workstreams, exit criteria, and non-goals.
- Produces: a testable repository plan that GitHub issues can implement without broadening `v0.5-beta`.
- Preserves: the long-term crosswalk and profile lists as roadmap direction.

- [ ] **Step 1: Add failing milestone and backlog invariants**

Add tests that require:

```python
def test_v05_beta_has_bounded_workstreams_and_exit_criteria(self) -> None:
    milestones = read_repository_file("project/MILESTONES.md")
    for heading in (
        "### Entry state",
        "### Required workstreams",
        "### Exit criteria",
        "### Non-goals",
    ):
        self.assertIn(heading, milestones)
    for required in (
        "all three UK mapping snapshots",
        "minimum ESAF-1500 assessment foundation",
        "one Draft pilot",
        "PCI DSS",
        "`GO`",
        "`HOLD`",
        "Critical and Important",
    ):
        self.assertIn(required, milestones)


def test_v05_beta_preserves_bounded_non_goals(self) -> None:
    milestones = read_repository_file("project/MILESTONES.md")
    for non_goal in (
        "all roadmap crosswalks",
        "all nine planned profiles",
        "complete assessment workbook",
        "substantive HITRUST CSF mapping",
        "redesigning `v0.9-rc1` and `v1.0`",
    ):
        self.assertIn(non_goal, milestones)


def test_backlog_removes_completed_release_work_and_orders_dependencies(self) -> None:
    backlog = read_repository_file("project/BACKLOG.md")
    self.assertNotIn("Complete open 0.4-alpha publication gates", backlog)
    self.assertEqual(
        1,
        backlog.count("Complete coordinated qualified review"),
    )
    review = backlog.index("Complete coordinated qualified review")
    assessment = backlog.index("Define the minimum ESAF-1500 assessment foundation")
    profile = backlog.index("Select and publish one Draft pilot")
    pci = backlog.index("Complete PCI DSS source readiness")
    self.assertLess(review, assessment)
    self.assertLess(assessment, profile)
    self.assertLess(profile, pci)


def test_hitrust_is_readiness_gated_and_not_a_v05_blocker(self) -> None:
    backlog = read_repository_file("project/BACKLOG.md")
    for required in (
        "licensed-source access",
        "publication rights",
        "qualified-review availability",
        "does not block `v0.5-beta`",
    ):
        self.assertIn(required, backlog)
```

Retain the existing exact-mapping-set assertion, but make it locate the single
coordinated qualified-review item.

Add a roadmap test requiring a `## 0.5-beta delivery sequence` section with the
ordered phrases:

```text
mapping assurance debt
minimum shared assessment semantics
one pilot profile
priority mappings
```

- [ ] **Step 2: Run the focused tests and verify failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata -v
```

Expected: new milestone, backlog, and roadmap tests fail against the broad
existing plan.

- [ ] **Step 3: Expand `project/MILESTONES.md`**

Retain the milestone table. Add `## v0.5-beta` with the exact four subsections
and requirements from design sections 7.1 through 7.4.

The PCI DSS workstream shall define two valid milestone outcomes:

- `GO`: the approved Draft mapping scope is completed;
- `HOLD`: the blocking condition, reconsideration trigger, and non-claim
  boundary are recorded.

The minimum assessment foundation shall be required before the pilot profile.
The full toolkit and all profile/crosswalk lists remain non-goals.

- [ ] **Step 4: Reconcile `project/BACKLOG.md`**

Remove the completed publication item and the duplicate core-only review item.
Create one coordinated qualified-review item containing all three exact
mapping-set identifiers.

Order the remaining initiatives:

1. coordinated qualified review;
2. minimum ESAF-1500 assessment foundation;
3. one Draft pilot profile;
4. PCI DSS source readiness and mapping go/no-go;
5. `v0.5-beta` release closure;
6. separately gated HITRUST readiness that does not block `v0.5-beta`.

- [ ] **Step 5: Add the roadmap delivery sequence**

Add `## 0.5-beta delivery sequence` after the version header and before the
long-term phases. State the four-stage order from the design and say explicitly
that the Phase 4 and Phase 5 lists remain long-term direction rather than beta
exit criteria.

- [ ] **Step 6: Run focused tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata -v
python -m unittest tests.test_release_gates -v
```

Expected: both focused modules pass.

- [ ] **Step 7: Commit the bounded milestone**

```powershell
git add -- tests/test_release_metadata.py project/MILESTONES.md `
  project/BACKLOG.md ROADMAP.md
git diff --cached --check
git commit -m "Define bounded 0.5-beta milestone"
```

---

### Task 4: Review and validate the complete branch

**Files:**
- Review: all files changed from `origin/main`
- Modify only if required by accepted review findings.

**Interfaces:**
- Consumes: Tasks 1 through 3 at one exact branch head.
- Produces: a review-approved, fully validated pull-request candidate.

- [ ] **Step 1: Inspect the complete branch diff**

```powershell
git fetch origin main
$base=(git merge-base origin/main HEAD).Trim()
git diff --stat "$base..HEAD"
git diff --check "$base..HEAD"
git diff "$base..HEAD"
```

Confirm the branch contains only the approved design, plan, release-state
transition, tests, validator, milestones, backlog, and roadmap changes.

- [ ] **Step 2: Dispatch independent specification review**

Give the reviewer:

- approved design path;
- implementation plan path;
- `$base`;
- exact `HEAD`;
- complete diff;
- request to identify missing requirements, contradictions, stale candidate
  language, and incorrect `v0.5-beta` scope.

Resolve every Critical and Important finding. Record accepted Minor findings
with owner and rationale.

- [ ] **Step 3: Dispatch independent whole-branch assurance review**

Request a separate reviewer to inspect:

- owner-risk and qualified-review wording;
- Draft lifecycle and non-claim boundaries;
- PCI DSS `GO`/`HOLD` semantics;
- HITRUST licensing and publication-rights gate;
- dependency order;
- exact tag and evidence identity; and
- whether any text implies compliance, equivalence, certification,
  endorsement, assurance, or production readiness.

Resolve every Critical and Important finding. If the branch head changes,
redispatch both reviews on the new exact head.

- [ ] **Step 4: Run the complete validation set**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
$base=(git merge-base origin/main HEAD).Trim()
git diff --check "$base..HEAD"
$cacheDirs=@(Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue)
if($cacheDirs.Count -ne 0){throw "Cache directories found: $($cacheDirs.Count)"}
if(@(git status --porcelain).Count -ne 0){throw 'Candidate worktree is not clean'}
```

Expected:

- 477 or more tests pass with only the three Windows symlink skips;
- controls report 91 controls, 91 objectives, and 16 families;
- architectures report 10 foundation files and 7 reserved patterns;
- mapping migration reports 91 unchanged sections;
- crosswalks report 3 mapping sets, 404 provisions, 81 relationships, and 325
  negative dispositions;
- links resolve for every tracked Markdown file;
- release record passes;
- whole-branch diff check passes;
- zero cache directories; and
- clean worktree.

No Mermaid source is expected to change. If the diff contains a Mermaid block,
stop and render every affected block before continuing.

- [ ] **Step 5: Record the reviewed head**

```powershell
$reviewedHead=(git rev-parse HEAD).Trim()
$base=(git merge-base origin/main HEAD).Trim()
"Reviewed head: $reviewedHead"
"Merge base: $base"
```

Do not amend or add commits after this point without rerunning affected
validation and both exact-head reviews.

---

### Task 5: Publish and merge the planning reconciliation

**Files:**
- No new repository files unless PR review requires a correction.

**Interfaces:**
- Consumes: the exact reviewed head and validation evidence from Task 4.
- Produces: a merged PR on `main` with traceable review and gate results.

- [ ] **Step 1: Push the branch**

```powershell
$branch=(git branch --show-current).Trim()
if($branch -ne 'agent/v05-plan-reconciliation'){throw "Unexpected branch: $branch"}
git push -u origin $branch
```

- [ ] **Step 2: Open a draft pull request**

Use the GitHub app when available. The title shall be:

```text
Reconcile 0.4 publication and bound 0.5-beta
```

The body shall include:

- approved design and plan paths;
- reviewed head SHA;
- baseline failure evidence: 477 tests, three date-sensitive failures before
  implementation;
- final focused and full-suite results;
- all validator counts;
- exact tag object and peeled commit;
- independent review verdicts;
- Critical and Important finding counts;
- `v0.5-beta` workstreams and non-goals;
- statement that GitHub milestone/issues will be created only after merge.

- [ ] **Step 3: Verify checks and exact-head identity**

```powershell
$pr=(gh pr view --json number --jq '.number').Trim()
$localHead=(git rev-parse HEAD).Trim()
$remoteHead=(gh pr view $pr --json headRefOid --jq '.headRefOid').Trim()
if($localHead -ne $remoteHead){throw 'Local and PR heads differ'}
gh pr checks $pr --watch
gh pr view $pr --json mergeable,mergeStateStatus,reviewDecision,statusCheckRollup
```

Require successful checks, a clean merge state, and the PR head equal to the
reviewed head.

- [ ] **Step 4: Mark the PR ready and merge**

```powershell
gh pr ready $pr
gh pr merge $pr --merge
```

If `gh pr merge` reports a local branch cleanup error after a successful merge,
inspect PR state before retrying. Do not issue a second merge.

- [ ] **Step 5: Update and validate main**

From the main worktree:

```powershell
git pull --ff-only origin main
$mergeHead=(git rev-parse HEAD).Trim()
$remoteMain=(git rev-parse origin/main).Trim()
if($mergeHead -ne $remoteMain){throw 'Local and remote main differ'}
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata -v
python -m unittest tests.test_release_gates -v
python tools/release_gates.py --check
git status --short --branch
```

Expected: focused release tests and release record pass on merged `main`, and
the main worktree is clean.

---

### Task 6: Create and verify the authoritative GitHub queue

**Files:**
- No repository file changes.

**Interfaces:**
- Consumes: merged `project/MILESTONES.md` and `project/BACKLOG.md`.
- Produces: GitHub milestone `v0.5-beta`, five milestone issues, and one
  unmilestoned HITRUST readiness issue.

- [ ] **Step 1: Create the milestone without a due date**

Verify it does not already exist:

```powershell
$existing=@(gh api 'repos/tdistress/ESAF/milestones?state=all&per_page=100' |
  ConvertFrom-Json | Where-Object {$_.title -eq 'v0.5-beta'})
if($existing.Count -ne 0){throw 'v0.5-beta milestone already exists'}
```

Create it:

```powershell
$milestone=gh api repos/tdistress/ESAF/milestones -X POST `
  -f title='v0.5-beta' `
  -f description='Qualified UK mappings, minimum ESAF-1500 assessment foundation, one Draft pilot profile, PCI DSS readiness and mapping decision, and exact-candidate release closure.'
$milestoneNumber=($milestone | ConvertFrom-Json).number
```

Load existing issue titles once and define a fail-closed duplicate guard:

```powershell
$existingIssueTitles=@(gh issue list --repo tdistress/ESAF --state all --limit 500 `
  --json title | ConvertFrom-Json | ForEach-Object {$_.title})
function Assert-IssueTitleAbsent([string]$title){
  if($existingIssueTitles -contains $title){throw "Issue title already exists: $title"}
}
```

- [ ] **Step 2: Create the qualified-review issue**

Run:

```powershell
$qualifiedBody=@'
## Purpose

Complete coordinated independent qualified human review for these exact Draft mapping snapshots:

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`

Core and Plus remain separate mapping sets. This issue coordinates their deferred assurance work and does not merge their sources, scopes, or conclusions.

## Deliverables

- Pin the exact final snapshot SHA, source inventory, manifest, and generated-catalog state for each mapping set.
- Obtain independent qualified human review with documented scheme and ESAF qualifications.
- Complete separate specification/inventory and security/overclaiming reviews on the exact final SHA.
- Record every finding and resolve all Critical and Important findings.
- Update lifecycle records only when every ESAF-1600 transition condition is satisfied.

## Acceptance criteria

- All three exact mapping-set identifiers have a qualified-review disposition.
- Reviewer identities, qualifications, dates, evidence locators, and exact reviewed SHA are recorded.
- Catalogs and traceability records are regenerated and validated.
- Focused tests, the full suite, crosswalk validation with the trusted baseline, link validation, and whole-branch diff checks pass.

## Boundaries

Review does not establish compliance, certification, equivalence, endorsement, external-scheme approval, assurance beyond the reviewed scope, or production readiness.
'@
Assert-IssueTitleAbsent 'Complete qualified review of the three UK mapping snapshots'
$qualifiedUrl=gh issue create --repo tdistress/ESAF `
  --title 'Complete qualified review of the three UK mapping snapshots' `
  --body $qualifiedBody --label crosswalk --label 'priority:critical' `
  --milestone 'v0.5-beta'
```

- [ ] **Step 3: Create the assessment-foundation issue**

Run:

```powershell
$assessmentBody=@'
## Purpose

Define the minimum shared ESAF-1500 assessment semantics required by crosswalks and the v0.5-beta pilot profile.

## Deliverables

- Define the common evidence model and evidence-quality attributes.
- Define the assessment-result contract, including scope, method, time boundary, finding, disposition, and traceability.
- Define maturity scoring semantics without allowing maturity to substitute for control conformance.
- Link the foundation from applicable assessment, control, profile, and project indexes.
- Add focused invariant tests and validation.

## Acceptance criteria

- The evidence, result, and maturity concepts are internally consistent and use ESAF normative terminology.
- The pilot-profile contract can reference the shared semantics without inventing profile-local scoring.
- Independent technical and editorial review is complete.
- Focused tests, the full suite, link validation, and whole-branch diff checks pass.

## Boundaries

This issue does not require the complete assessment workbook, audit checklist, governance-template library, certification method, or automated compliance score.
'@
Assert-IssueTitleAbsent 'Define the minimum ESAF-1500 assessment foundation'
$assessmentUrl=gh issue create --repo tdistress/ESAF `
  --title 'Define the minimum ESAF-1500 assessment foundation' `
  --body $assessmentBody --label assessment --label 'priority:high' `
  --milestone 'v0.5-beta'
```

- [ ] **Step 4: Create the pilot-profile issue**

Run:

```powershell
$profileBody=@'
## Purpose

Select, design, validate, and publish one Draft pilot industry or jurisdiction profile that proves the reusable ESAF profile contract.

## Dependency

Profile implementation begins only after the minimum ESAF-1500 assessment foundation is merged. The repository owner records the pilot selection in this issue before profile design starts.

## Deliverables

- Record the selected pilot and selection rationale.
- Define a reusable profile contract that preserves core control meanings.
- Define the pilot scope, additional risks, control selections, overlays, evidence expectations, and external mappings.
- Add focused validation and link the profile from applicable indexes.

## Acceptance criteria

- Exactly one Draft pilot profile conforms to the reusable contract.
- Assessment and evidence references use the shared ESAF-1500 semantics.
- Technical, editorial, profile-scope, and overclaiming reviews are complete on the exact final SHA.
- Focused tests, the full suite, affected validators, link validation, and every applicable Mermaid render pass.

## Boundaries

The profile remains Draft and does not establish compliance, certification, equivalence, endorsement, external-scheme approval, or production readiness.
'@
Assert-IssueTitleAbsent 'Select and publish one Draft pilot ESAF industry profile'
$profileUrl=gh issue create --repo tdistress/ESAF `
  --title 'Select and publish one Draft pilot ESAF industry profile' `
  --body $profileBody --label profile --label 'priority:high' `
  --milestone 'v0.5-beta'
```

- [ ] **Step 5: Create the PCI DSS issue**

Run:

```powershell
$pciBody=@'
## Purpose

Establish the authoritative PCI DSS source boundary and decide whether a substantive ESAF mapping is ready to proceed.

## Deliverables

- Pin the official PCI DSS version, URL, publication date, source checksum, and provision inventory.
- Record publication-rights and public-content boundaries.
- Identify mapper and qualified-review requirements.
- Define the exact directional mapping questions and overclaiming controls.
- Record one decision: `GO` or `HOLD`.

## GO outcome

Complete the approved Draft mapping scope under ESAF-1600, including provision records, negative dispositions, lifecycle record, generated catalogs, exact-SHA reviews, and traceability.

## HOLD outcome

Record the blocking condition, owner, reconsideration trigger, and non-claim boundary. Do not create substantive mapping records.

## Acceptance criteria

- Every pinned source and inventory assertion is independently verified.
- The decision follows the approved go/no-go method and is traceable to exact evidence.
- Critical and Important findings are resolved.
- Focused tests, the full suite, crosswalk validation, link validation, and whole-branch diff checks pass.

## Boundaries

Neither outcome asserts PCI DSS compliance, assessor approval, certification, equivalence, endorsement, or legal sufficiency.
'@
Assert-IssueTitleAbsent 'Complete PCI DSS source readiness and mapping go/no-go'
$pciUrl=gh issue create --repo tdistress/ESAF `
  --title 'Complete PCI DSS source readiness and mapping go/no-go' `
  --body $pciBody --label crosswalk --label 'priority:high' `
  --milestone 'v0.5-beta'
```

- [ ] **Step 6: Create the release-closure issue**

Run:

```powershell
$closureBody=@'
## Purpose

Close the v0.5-beta publication gates on one exact candidate after the four milestone content workstreams are complete.

## Dependencies

- Complete qualified review of the three UK mapping snapshots.
- Define the minimum ESAF-1500 assessment foundation.
- Select and publish one Draft pilot ESAF industry profile.
- Complete PCI DSS source readiness and mapping go/no-go.

## Acceptance criteria

- Scope and milestone approval is recorded on the exact candidate.
- Technical, editorial, terminology, mapping, profile-scope, and governance reviews are complete.
- Critical and Important findings are resolved.
- Generated catalogs and traceability records are current.
- The full suite and every affected control, architecture, crosswalk, link, release, and working-tree gate pass.
- Every changed Mermaid block is rendered and reviewed.
- The complete branch diff is reviewed, GitHub checks pass, and merge state is clean.
- Post-merge validation passes before an immutable tag or publication statement is created.
- Final evidence records exact candidate, merge, tag, counts, reviews, and lifecycle limitations.

## Boundaries

Evidence from v0.4-alpha is historical and cannot approve v0.5-beta. Publication does not change an artifact lifecycle state without its own evidence.
'@
Assert-IssueTitleAbsent 'Close the v0.5-beta publication gates'
$closureUrl=gh issue create --repo tdistress/ESAF `
  --title 'Close the v0.5-beta publication gates' `
  --body $closureBody --label governance --label 'priority:high' `
  --milestone 'v0.5-beta'
```

- [ ] **Step 7: Create the unmilestoned HITRUST readiness issue**

Run:

```powershell
$hitrustBody=@'
## Purpose

Determine whether ESAF can begin a future HITRUST CSF mapping without exceeding licensed-source, publication-rights, or review boundaries.

## Deliverables

- Confirm authorized access to the exact licensed HITRUST CSF version.
- Define the public-content and publication-rights boundary.
- Assess provision-inventory feasibility without reproducing restricted text.
- Identify mapper and qualified-review availability.
- Record a readiness decision and reconsideration triggers.

## Acceptance criteria

- Version, access, rights, inventory, and review prerequisites are evidenced.
- Any permitted public artifact is independently reviewed for rights and overclaiming.
- A blocked prerequisite produces a `HOLD` record rather than an inferred mapping.

## Boundaries

This issue does not authorize substantive mapping records and does not block v0.5-beta. It makes no HITRUST certification, compliance, equivalence, endorsement, or assurance claim.
'@
Assert-IssueTitleAbsent 'Establish HITRUST CSF source and review readiness'
$hitrustUrl=gh issue create --repo tdistress/ESAF `
  --title 'Establish HITRUST CSF source and review readiness' `
  --body $hitrustBody --label crosswalk --label 'priority:medium'
```

- [ ] **Step 8: Verify the queue**

```powershell
$milestones=gh api 'repos/tdistress/ESAF/milestones?state=open&per_page=100' |
  ConvertFrom-Json
$v05=$milestones | Where-Object {$_.title -eq 'v0.5-beta'}
if(@($v05).Count -ne 1){throw 'Expected exactly one v0.5-beta milestone'}
if($null -ne $v05.due_on){throw 'v0.5-beta shall not have a due date'}
if($v05.open_issues -ne 5){throw "Expected five milestone issues, found $($v05.open_issues)"}
gh issue list --repo tdistress/ESAF --state open --limit 100 `
  --json number,title,labels,milestone,url
```

Verify:

- exactly five issues use `v0.5-beta`;
- exactly one approved HITRUST issue has no milestone;
- every issue has the designed labels;
- dependency text and lifecycle limitations are present; and
- no duplicate issue was created.

- [ ] **Step 9: Clean only the owned branch and worktree**

After GitHub verification, resolve the exact worktree path and ensure it lies
under the project `.worktrees` directory before removal:

```powershell
$mainRoot=(git rev-parse --show-toplevel).Trim()
$owned=Join-Path $mainRoot '.worktrees\agent-v05-plan-reconciliation'
$worktreeRoot=[IO.Path]::GetFullPath((Join-Path $mainRoot '.worktrees')) +
  [IO.Path]::DirectorySeparatorChar
$resolved=[IO.Path]::GetFullPath($owned)
if(-not $resolved.StartsWith($worktreeRoot,[StringComparison]::OrdinalIgnoreCase)){
  throw "Refusing to remove out-of-scope worktree: $resolved"
}
git worktree list --porcelain
if(Test-Path -LiteralPath $resolved){git worktree remove $resolved}
git worktree prune
git branch -d agent/v05-plan-reconciliation
if(git ls-remote --heads origin agent/v05-plan-reconciliation){
  git push origin --delete agent/v05-plan-reconciliation
}
git status --short --branch
```

Do not remove `agent/task2-mapping-set-counts`,
`agent/task2-validation`, the pre-existing publication-design worktree, or any
other unrelated branch/worktree in this task.

## Execution stop conditions

Stop and preserve a clean, recoverable state if:

- the annotated tag object or peeled commit differs from the approved values;
- the tracked publication evidence differs from issue `#39`;
- a current-date requirement remains on the published record;
- a Critical or Important review finding remains unresolved;
- the branch head changes after review without affected re-review;
- any focused test, full-suite test, validator, link check, diff check, cache
  check, or cleanliness check fails;
- the PR head differs from the reviewed head;
- GitHub checks fail or the PR is not cleanly mergeable;
- the milestone already exists unexpectedly;
- an issue with the same title already exists; or
- a cleanup target cannot be proven to be the owned planning worktree.

Do not weaken validation, rewrite history, move the tag, broaden `v0.5-beta`,
or delete unrelated state to bypass a stop condition.
