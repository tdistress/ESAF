# v0.5-beta Deferred Mapping Assurance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permit `v0.5-beta` to proceed with all three UK mapping sets included as Draft artifacts when qualified human review is deferred through one coordinated, exact-candidate owner-risk decision, while keeping qualified review open and preserving every other release gate.

**Architecture:** Treat `DEFERRED` only as a human-facing milestone disposition. Reuse the existing `owner_risk_acceptance` release-evidence path and its exact-SHA, uniform-source, Draft-lifecycle, and nonclaim invariants. Enforce the repository policy with metadata regression tests, then synchronize GitHub issues 55 and 59 only after the policy change is merged.

**Tech Stack:** Markdown policy and tracking documents, Python `unittest`, existing release-gate validators, Git, GitHub CLI or the connected GitHub app.

## Global Constraints

- Work from the isolated `agent/v05-deferred-assurance-design` branch and review the complete diff from merge base to branch head.
- Keep the approved design in `docs/superpowers/specs/2026-07-27-v05-beta-deferred-mapping-assurance-design.md` unchanged unless implementation exposes a contradiction.
- Do not add `DEFERRED` to a release-gate enum, ESAF-1600 lifecycle state, mapping schema, or mapping record.
- Do not modify mapping content, reviewer metadata, lifecycle events, approval state, or publication state.
- Do not weaken the existing exact three-identifier requirement, exact-candidate binding, uniform decision basis, authenticated owner source, Draft lifecycle, or required nonclaims.
- Do not let owner-risk acceptance close issue 55 or represent completion of any of the six qualified human role dispositions.
- Preserve the historical `v0.4-alpha` publication evidence and the statement that it cannot approve a later release.
- Preserve the complete `v0.5-beta` technical, editorial, governance, validation, merge, and post-merge gate set.
- Keep HITRUST readiness nonblocking, keep the PCI DSS `HOLD` disposition unchanged, and do not reintroduce architecture-pattern work.
- Set `PYTHONDONTWRITEBYTECODE=1` for Python checks and verify that no generated cache or build output is committed.
- Do not tag or publish `v0.5-beta` under this plan. Release closure is a separate implementation effort after policy and issue synchronization.

---

## Task 1: Add Failing Repository-Policy Regression Tests

**Files:**

- Modify: `tests/test_release_metadata.py:253-380`
- Test: `tests/test_release_metadata.py`

- [ ] **Step 1: Add a helper for bounded Markdown sections**

Add this helper immediately after `markdown_list_items`:

```python
def markdown_section(text: str, heading: str) -> str:
    start_match = re.search(
        rf"^{re.escape(heading)}\s*$",
        text,
        re.MULTILINE,
    )
    if start_match is None:
        raise AssertionError(f"missing Markdown section {heading!r}")
    section_start = start_match.end()
    next_heading = re.search(
        r"^#{1,6}\s+.+$",
        text[section_start:],
        re.MULTILINE,
    )
    section_end = (
        section_start + next_heading.start()
        if next_heading is not None
        else len(text)
    )
    return text[section_start:section_end]
```

- [ ] **Step 2: Extend the release-plan decision-basis test**

Replace `test_release_plan_allows_one_uniform_mapping_decision_basis` with:

```python
    def test_release_plan_allows_one_uniform_mapping_decision_basis(self) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md")
        self.assertIn(
            "exactly one uniform mapping decision basis: `qualified_approval` or "
            "`owner_risk_acceptance`",
            release_plan,
        )
        self.assertTrue(contains_normalized_phrase(
            release_plan,
            "Owner risk acceptance defers qualified review; it does not complete or "
            "qualify that review.",
        ))
        self.assertIn(
            "Steering Committee governance approval remains a separate gate",
            release_plan,
        )

        deferred = markdown_section(
            release_plan,
            "## v0.5-beta deferred mapping assurance",
        )
        for required in (
            "exact `v0.5-beta` release candidate",
            "`mapping_decision_basis: owner_risk_acceptance`",
            "`decision_type: owner_risk_acceptance`",
            "`qualified_review_status: deferred`",
            "one authenticated owner source",
            "remain Draft",
            "issue 55 remains open",
        ):
            with self.subTest(required=required):
                self.assertTrue(contains_normalized_phrase(deferred, required))
        for mapping_set_id in EXPECTED_MAPPING_SET_IDS:
            with self.subTest(mapping_set_id=mapping_set_id):
                self.assertEqual(1, deferred.count(mapping_set_id))
```

- [ ] **Step 3: Replace the backlog assertion with the deferred-follow-up contract**

Replace `test_owner_risk_acceptance_retains_exact_mapping_review_backlog` with:

```python
    def test_deferred_assurance_followup_keeps_issue_55_open_for_all_three_mapping_sets(
        self,
    ) -> None:
        backlog = read_repository_file("project/BACKLOG.md")
        deferred = markdown_section(backlog, "## Deferred assurance follow-up")
        self.assertIn("https://github.com/tdistress/ESAF/issues/55", deferred)
        self.assertTrue(contains_normalized_phrase(
            deferred,
            "remains open until qualified review is complete",
        ))
        for mapping_set_id in EXPECTED_MAPPING_SET_IDS:
            with self.subTest(mapping_set_id=mapping_set_id):
                self.assertEqual(1, deferred.count(mapping_set_id))
```

- [ ] **Step 4: Add the two-path milestone contract**

Add this test after the existing milestone structure test:

```python
    def test_v05_beta_accepts_qualified_or_coordinated_deferred_mapping_assurance(
        self,
    ) -> None:
        milestones = read_repository_file("project/MILESTONES.md")
        required_workstreams = markdown_section(
            milestones,
            "### Required workstreams",
        )
        exit_criteria = markdown_section(milestones, "### Exit criteria")
        for section in (required_workstreams, exit_criteria):
            with self.subTest(section=section[:40]):
                self.assertTrue(contains_normalized_phrase(
                    section,
                    "completed qualified-review dispositions",
                ))
                self.assertTrue(contains_normalized_phrase(
                    section,
                    "one coordinated owner-risk disposition",
                ))
                self.assertTrue(contains_normalized_phrase(
                    section,
                    "all three",
                ))
                self.assertTrue(contains_normalized_phrase(
                    section,
                    "exact `v0.5-beta` release candidate",
                ))
        self.assertTrue(contains_normalized_phrase(
            milestones,
            "`DEFERRED` is a milestone assurance disposition, not an ESAF-1600 "
            "mapping lifecycle state",
        ))
        self.assertTrue(contains_normalized_phrase(
            milestones,
            "all three mapping sets and their records remain Draft",
        ))
```

- [ ] **Step 5: Enforce that issue 59 retains all other gates**

Extend `test_v05_beta_exit_and_closure_issue_require_complete_gate_set` after its existing historical-plan assertion:

```python
        backlog = read_repository_file("project/BACKLOG.md")
        active = markdown_section(backlog, "## Active release workstreams")
        self.assertIn("https://github.com/tdistress/ESAF/issues/59", active)
        self.assertTrue(contains_normalized_phrase(
            active,
            "completed qualified approval or validated exact-candidate owner-risk "
            "acceptance",
        ))
        self.assertTrue(contains_normalized_phrase(
            active,
            "every other release gate remains required",
        ))
```

- [ ] **Step 6: Assert that active and deferred work are separated**

In `test_backlog_removes_completed_work_and_preserves_remaining_dependencies`, replace the assertion that counts `Complete coordinated qualified review` with:

```python
        active = markdown_section(backlog, "## Active release workstreams")
        deferred = markdown_section(backlog, "## Deferred assurance follow-up")
        self.assertIn("https://github.com/tdistress/ESAF/issues/59", active)
        self.assertNotIn("https://github.com/tdistress/ESAF/issues/55", active)
        self.assertIn("https://github.com/tdistress/ESAF/issues/55", deferred)
        self.assertNotIn("https://github.com/tdistress/ESAF/issues/59", deferred)
```

Retain the existing checks for removed completed work, PCI DSS `HOLD`, HITRUST readiness, and issue 59.

- [ ] **Step 7: Replace the roadmap sequencing assertion**

Replace `test_roadmap_sequences_v05_beta_delivery_before_long_term_phases` with:

```python
    def test_roadmap_keeps_deferred_mapping_assurance_nonblocking_after_beta(
        self,
    ) -> None:
        roadmap = read_repository_file("ROADMAP.md")
        sequence = markdown_section(roadmap, "## 0.5-beta delivery sequence")
        self.assertTrue(contains_normalized_phrase(
            sequence,
            "deferred mapping assurance remains tracked after beta",
        ))
        self.assertTrue(contains_normalized_phrase(
            sequence,
            "does not stop later engineering work",
        ))
        self.assertIn("issue 55", sequence)
        self.assertNotIn("first closes mapping assurance debt", sequence)
```

- [ ] **Step 8: Add the Draft and nonclaim regression**

Add this test after the release-plan decision-basis test:

```python
    def test_deferred_release_preserves_draft_state_and_required_nonclaims(
        self,
    ) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md")
        deferred = markdown_section(
            release_plan,
            "## v0.5-beta deferred mapping assurance",
        )
        self.assertTrue(contains_normalized_phrase(
            deferred,
            "all three mapping sets and their records remain Draft",
        ))
        for nonclaim in (
            "qualified review",
            "approval",
            "assurance",
            "compliance",
            "certification",
            "equivalence",
            "endorsement",
            "external-scheme approval",
            "production readiness",
        ):
            with self.subTest(nonclaim=nonclaim):
                self.assertIn(nonclaim, deferred.casefold())
        self.assertNotIn("qualified review completed", deferred.casefold())
        self.assertNotIn("approved mappings", deferred.casefold())
```

- [ ] **Step 9: Run the focused tests and confirm the intended RED state**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_release_metadata.ReleaseMetadataTests.test_release_plan_allows_one_uniform_mapping_decision_basis `
  tests.test_release_metadata.ReleaseMetadataTests.test_deferred_assurance_followup_keeps_issue_55_open_for_all_three_mapping_sets `
  tests.test_release_metadata.ReleaseMetadataTests.test_v05_beta_accepts_qualified_or_coordinated_deferred_mapping_assurance `
  tests.test_release_metadata.ReleaseMetadataTests.test_v05_beta_exit_and_closure_issue_require_complete_gate_set `
  tests.test_release_metadata.ReleaseMetadataTests.test_roadmap_keeps_deferred_mapping_assurance_nonblocking_after_beta `
  tests.test_release_metadata.ReleaseMetadataTests.test_deferred_release_preserves_draft_state_and_required_nonclaims -v
```

Expected: failures report the missing `v0.5-beta deferred mapping assurance` and `Deferred assurance follow-up` sections and the old roadmap language. Any import, syntax, or helper failure is an invalid RED state and shall be fixed before policy documents are edited.

- [ ] **Step 10: Commit the failing tests**

```powershell
git add tests/test_release_metadata.py
git diff --cached --check
git commit -m "test: define deferred mapping assurance policy"
```

Expected: one test-only commit whose focused tests fail only because the policy documents have not yet been updated.

---

## Task 2: Implement the Repository Policy and Tracking Language

**Files:**

- Modify: `project/MILESTONES.md:15-61`
- Modify: `ROADMAP.md:7-10`
- Modify: `project/BACKLOG.md:7-25`
- Modify: `project/RELEASE_PLAN.md:13`
- Test: `tests/test_release_metadata.py`

- [ ] **Step 1: Replace the qualified-review workstream in `project/MILESTONES.md`**

Replace required workstream 1 with:

```markdown
1. **UK mapping assurance.** ESAF shall record either completed
   qualified-review dispositions for all three UK mapping sets or one
   coordinated owner-risk disposition that defers qualified review for all
   three sets on the exact `v0.5-beta` release candidate. Core and Plus remain
   separate mapping sets. Under the deferred path, `DEFERRED` is a milestone
   assurance disposition, not an ESAF-1600 mapping lifecycle state. All three
   mapping sets and their records remain Draft.
```

- [ ] **Step 2: Replace the first milestone exit criterion**

Replace the first exit-criteria bullet with:

```markdown
- all three UK mapping sets have either completed qualified-review
  dispositions or one coordinated owner-risk disposition that defers
  qualified review for all three sets on the exact `v0.5-beta` release
  candidate;
```

Do not change the remaining exit criteria.

- [ ] **Step 3: Rewrite the roadmap delivery sequence**

Replace the paragraph under `## 0.5-beta delivery sequence` with:

```markdown
`v0.5-beta` records either completed qualified review or one coordinated
exact-candidate owner-risk disposition for the three Draft UK mapping sets,
then completes the minimum shared assessment foundation, one pilot profile,
and the priority-mapping decision. If owner-risk acceptance is used, deferred
mapping assurance remains tracked after beta through issue 55 and does not stop
later engineering work. The Phase 4 and Phase 5 lists remain long-term
direction, not `v0.5-beta` exit criteria.
```

- [ ] **Step 4: Reorganize the backlog**

Replace the current active-workstream block with:

```markdown
## Active release workstreams

- Complete [issue 59](https://github.com/tdistress/ESAF/issues/59), the
  `v0.5-beta` publication gates on one exact candidate after the milestone
  content workstreams are complete. The mapping-assurance prerequisite may be
  met by completed qualified approval or validated exact-candidate owner-risk
  acceptance for all three Draft UK mapping sets. Every other release gate
  remains required.

## Deferred assurance follow-up

- [Issue 55](https://github.com/tdistress/ESAF/issues/55) remains open until
  qualified review is complete for all three exact mapping sets:
  `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`,
  `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`,
  and
  `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`.
  A `v0.5-beta` owner-risk disposition defers this work and does not complete
  qualified review or change a mapping lifecycle state.

## Separately gated future work

- Establish HITRUST CSF source and review readiness only after licensed-source
  access, publication rights, and qualified-review availability are confirmed.
  This work does not block `v0.5-beta`.
```

Keep `## Completed workstreams` and its PCI DSS `HOLD` entry unchanged.

- [ ] **Step 5: Add the v0.5 release-plan section**

Insert this section immediately before `## 0.4-alpha publication`:

```markdown
## v0.5-beta deferred mapping assurance

The `v0.5-beta` mapping-assurance gate shall use either completed qualified
approval or one coordinated owner-risk decision bound to the exact
`v0.5-beta` release candidate. The owner-risk path shall cover each of these
mapping sets exactly once:

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`

The coordinated evidence shall use
`mapping_decision_basis: owner_risk_acceptance`,
`decision_type: owner_risk_acceptance`, and
`qualified_review_status: deferred`. Every mapping decision shall use one
uniform basis and one authenticated owner source, identify the missing
qualified human evidence, preserve the required nonclaims, and bind to the
exact candidate SHA.

`DEFERRED` is a milestone assurance disposition, not an ESAF-1600 mapping
lifecycle state. All three mapping sets and their records remain Draft. No
reviewer metadata, lifecycle event, approval state, or publication state is
added. Issue 55 remains open for the six qualified human role dispositions.
Issue 59 may proceed under validated deferred evidence, but every other
technical, editorial, mapping, governance, validation, merge, and post-merge
release gate remains required.

Owner-risk acceptance defers qualified review; it does not complete or qualify
that review. It does not establish qualified review, approval, assurance,
compliance, certification, equivalence, endorsement, external-scheme approval,
or production readiness. Historical `v0.4-alpha` evidence cannot approve
`v0.5-beta`.
```

- [ ] **Step 6: Run the focused metadata tests and confirm GREEN**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata -v
```

Expected: all release-metadata tests pass.

- [ ] **Step 7: Run focused release-gate regressions**

```powershell
python -m unittest `
  tests.test_release_gates.ReleaseGateTests.test_both_uniform_mapping_decision_bases_pass_closure_and_taggable `
  tests.test_release_gates.ReleaseGateTests.test_mapping_decisions_require_v1_schema_and_uniform_basis `
  tests.test_release_gates.ReleaseGateTests.test_closure_record_and_external_evidence_require_the_same_basis `
  tests.test_release_gates.ReleaseGateTests.test_owner_risk_fields_and_scope_are_strict `
  tests.test_release_gates.ReleaseGateTests.test_owner_risk_rejects_pr_a_head_rebinding_in_both_phases -v
```

Expected: all selected tests pass without modifying `tools/release_gates.py` or any schema.

- [ ] **Step 8: Validate the documentation**

```powershell
python tools/validate_links.py --check
git diff --check
git status --short
```

Expected: link validation passes, no whitespace errors are reported, and only the intended policy/test files plus the already committed design and plan are present.

- [ ] **Step 9: Commit the policy implementation**

```powershell
git add project/MILESTONES.md ROADMAP.md project/BACKLOG.md project/RELEASE_PLAN.md
git diff --cached --check
git commit -m "docs: allow deferred mapping assurance for v0.5-beta"
```

Expected: the focused tests that were RED in Task 1 are GREEN at the new branch head.

---

## Task 3: Independently Review the Exact Policy Candidate

**Files:**

- Review: `docs/superpowers/specs/2026-07-27-v05-beta-deferred-mapping-assurance-design.md`
- Review: `tests/test_release_metadata.py`
- Review: `project/MILESTONES.md`
- Review: `ROADMAP.md`
- Review: `project/BACKLOG.md`
- Review: `project/RELEASE_PLAN.md`

- [ ] **Step 1: Record the exact candidate and merge base**

```powershell
$candidate = git rev-parse HEAD
$mergeBase = git merge-base origin/main HEAD
git diff --check "$mergeBase..$candidate"
git diff --stat "$mergeBase..$candidate"
git status --short
```

Expected: whole-branch diff check passes and the worktree is clean.

- [ ] **Step 2: Dispatch an independent specification review**

Ask a read-only subagent to review the exact `$candidate` against the approved design. Require it to verify:

- both qualified-review and owner-risk paths are explicit alternatives;
- `DEFERRED` is not represented as a lifecycle state;
- all three exact mapping identifiers are present;
- issue 55 remains open;
- issue 59 retains every other release gate;
- historical `v0.4-alpha` evidence cannot approve `v0.5-beta`;
- the implementation did not expand scope.

Record the verdict and findings against the exact candidate SHA.

- [ ] **Step 3: Dispatch an independent release-overclaiming review**

Ask a second read-only subagent to review the same exact `$candidate`. Require it to test for:

- any implication that owner-risk acceptance equals qualified review;
- any approval, assurance, compliance, certification, equivalence,
  endorsement, external-scheme approval, or production-readiness claim;
- any weakened exact-SHA, exact-three-set, uniform-basis, uniform-source,
  Draft-lifecycle, or nonclaim invariant;
- any accidental closure of issue 55 or waiver of issue 59 gates.

Record the verdict and findings against the exact candidate SHA.

- [ ] **Step 4: Resolve findings without stale review evidence**

Resolve every Critical and Important finding. Add a focused regression test before fixing a discovered policy defect when practical. If the branch head changes:

1. rerun the focused tests;
2. record the new candidate SHA; and
3. redispatch both independent reviews on that exact SHA.

Do not reuse a verdict from an earlier branch head.

- [ ] **Step 5: Commit any review fixes**

If changes were required:

```powershell
git add tests/test_release_metadata.py project/MILESTONES.md ROADMAP.md project/BACKLOG.md project/RELEASE_PLAN.md
git diff --cached --check
git commit -m "docs: resolve deferred assurance review findings"
```

Expected: no uncommitted changes and both reviews apply to the final head.

---

## Task 4: Run Publication-Proportional Validation

**Files:**

- Validate: entire branch diff

- [ ] **Step 1: Run the two focused suites**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata tests.test_release_gates -v
```

Expected: all tests pass.

- [ ] **Step 2: Run the full unit suite**

```powershell
python -m unittest discover -s tests -v
```

Expected: the complete suite passes.

- [ ] **Step 3: Run repository validators**

```powershell
python tools/validate_assessment.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/validate_links.py --check
```

Expected: all validators pass. Mapping artifacts are unchanged, so no crosswalk snapshot regeneration is expected. If a crosswalk reference changes unexpectedly, stop and run the repository's trusted-baseline crosswalk validation before continuing.

- [ ] **Step 4: Run final hygiene checks**

```powershell
$candidate = git rev-parse HEAD
$mergeBase = git merge-base origin/main HEAD
git diff --check "$mergeBase..$candidate"
git status --short
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Select-Object -ExpandProperty FullName
```

Expected: whole-branch diff check passes, the worktree is clean, and no `__pycache__` directories exist. Remove only generated caches inside this isolated worktree if any appear, then repeat the checks.

---

## Task 5: Publish and Merge the Repository Policy Change

**Files:**

- Publish: complete `agent/v05-deferred-assurance-design` branch
- GitHub: create a ready pull request against `main`

- [ ] **Step 1: Push the exact reviewed head**

```powershell
$candidate = git rev-parse HEAD
git push -u origin agent/v05-deferred-assurance-design
```

Expected: the remote branch resolves to `$candidate`.

- [ ] **Step 2: Open a ready pull request**

Create a ready PR whose body:

- summarizes the two-path `v0.5-beta` policy;
- names the exact three Draft mapping sets;
- states that issue 55 remains open;
- states that issue 59 retains all other gates;
- records the exact reviewed head SHA from Task 3;
- records both independent review verdicts;
- records the focused, full-suite, validator, link, and diff-check results;
- links issues 55 and 59 without using a closing keyword;
- states that the PR does not publish or tag `v0.5-beta`.

- [ ] **Step 3: Verify the PR head and checks**

```powershell
$pr = gh pr view --repo tdistress/ESAF --json number,state,isDraft,headRefOid,mergeStateStatus,statusCheckRollup,url | ConvertFrom-Json
if ($pr.headRefOid -ne $candidate) { throw "PR head does not match reviewed candidate" }
$pr | ConvertTo-Json -Depth 8
```

Expected: the PR is open, ready, points to `$candidate`, and all required checks reach a passing terminal state.

- [ ] **Step 4: Recheck merge readiness immediately before merge**

```powershell
gh pr view $pr.number --repo tdistress/ESAF `
  --json state,isDraft,headRefOid,mergeStateStatus,statusCheckRollup
```

Expected: state is open, the PR is not a draft, `headRefOid` still equals the exact reviewed SHA, required checks pass, and merge state is clean.

- [ ] **Step 5: Merge without closing either tracking issue**

Merge the PR using the repository's normal merge strategy. If branch deletion reports a local worktree conflict after the merge, verify the PR state before any retry and clean the worktree separately.

- [ ] **Step 6: Verify merged main**

```powershell
git fetch origin
$mergedPr = gh pr view $pr.number --repo tdistress/ESAF `
  --json state,mergedAt,mergeCommit,statusCheckRollup,url | ConvertFrom-Json
$mergeSha = $mergedPr.mergeCommit.oid
git merge-base --is-ancestor $mergeSha origin/main
if ($LASTEXITCODE -ne 0) { throw "policy merge is not on origin/main" }
$mergedPr | ConvertTo-Json -Depth 8
```

Expected: PR state is merged, `$mergeSha` is an ancestor of `origin/main`, and checks are passing.

- [ ] **Step 7: Run post-merge proportional validation**

Use the clean main worktree:

```powershell
git switch main
git pull --ff-only origin main
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata tests.test_release_gates -v
python tools/validate_links.py --check
git status --short
```

Expected: validation passes and main is clean.

---

## Task 6: Synchronize GitHub Issue 55

**Files:**

- GitHub issue: `https://github.com/tdistress/ESAF/issues/55`
- Read-only reference: merged policy files at `$mergeSha`

- [ ] **Step 1: Reverify the merged policy and capture live issue state**

```powershell
git show "${mergeSha}:project/MILESTONES.md"
git show "${mergeSha}:project/BACKLOG.md"
git show "${mergeSha}:project/RELEASE_PLAN.md"
$issue55Before = gh api repos/tdistress/ESAF/issues/55 | ConvertFrom-Json
$issue55CommentsBefore = @(gh api repos/tdistress/ESAF/issues/55/comments --paginate | ConvertFrom-Json)
$issue55Before | Select-Object number,state,title,updated_at,body
```

Expected: issue 55 is open, remains in milestone `v0.5-beta`, and historical comments `5071834997` and `5096716394` are present. Stop if its body changed materially after the planning snapshot; reconcile the new information before writing.

- [ ] **Step 2: Build the exact replacement body**

Use a PowerShell literal here-string for this body:

```markdown
## Purpose

Complete coordinated independent qualified human review for these exact Draft mapping snapshots:

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`

Core and Plus remain separate mapping sets. This issue coordinates their deferred assurance work and does not merge their sources, scopes, or conclusions.

This issue remains open if `v0.5-beta` proceeds under the coordinated owner-risk deferred-assurance path. `DEFERRED` is a milestone assurance disposition, not an ESAF-1600 mapping lifecycle state.

## Release relationship

For `v0.5-beta`, qualified-review assurance may be satisfied by either:

1. completed qualified-review dispositions for all six required human roles; or
2. one validated, exact-candidate owner-risk decision covering all three mapping sets.

The second path permits Working Draft publication only. It does not complete this issue, complete qualified review, or change any mapping lifecycle state. All three mapping sets and all records remain `draft`.

Historical `v0.4-alpha` evidence cannot approve `v0.5-beta`.

## Qualified-review deliverables

Complete all six separately recorded human role dispositions:

- specification and inventory review for Core;
- security and overclaiming review for Core;
- specification and inventory review for Plus forward;
- security and overclaiming review for Plus forward;
- specification and inventory review for Plus reverse; and
- security and overclaiming review for Plus reverse.

For each applicable mapping set and role:

- pin the exact final snapshot SHA, source inventory, manifest, and generated-catalog state;
- record the named human reviewer, relevant qualifications, date, evidence locator, source access, independence, affiliation, and conflicts disposition;
- obtain owner acceptance of reviewer eligibility and any dual-role arrangement;
- record every finding and resolve all Critical and Important findings; and
- obtain signed final confirmation bound to the exact reviewed SHA.

Update reviewer metadata, lifecycle events, approval state, or publication state only when every ESAF-1600 transition condition is satisfied.

## Re-entry triggers

Qualified-review work shall be re-entered or rebaselined when:

- an eligible qualified reviewer becomes available;
- a mapping record, pinned source, inventory, manifest, catalog, or reviewed candidate changes;
- a deferred owner-risk decision expires, is withdrawn, or is superseded; or
- the accountable owner requires earlier completion.

## Acceptance criteria

- All six qualified human role dispositions are complete for the three exact mapping-set identifiers.
- Reviewer identities, qualifications, dates, evidence locators, exact reviewed SHA, eligibility decisions, and any accepted dual-role arrangement are recorded.
- Every Critical and Important finding is resolved.
- Catalogs and traceability records are regenerated and validated.
- Focused tests, the full suite, crosswalk validation with the trusted baseline, link validation, and whole-branch diff checks pass.
- Any lifecycle transition is supported by the complete qualified-review evidence contract.

## Boundaries

Owner-risk acceptance cannot substitute for qualified human review and cannot close this issue.

AI review and ordinary pull-request review are not qualified human review.

Neither deferred assurance nor later qualified review establishes compliance, certification, equivalence, endorsement, external-scheme approval, production readiness, or assurance beyond the expressly recorded scope.
```

- [ ] **Step 3: Update only the issue body**

Before writing, re-read `updated_at` and body. Stop on divergence. Skip the write if the desired body is already identical. Otherwise update only the body, leaving title, state, milestone, labels, and assignees unchanged.

- [ ] **Step 4: Verify the body byte-for-byte**

Re-fetch issue 55 and compare its body with the desired body. Also verify:

- state is still `open`;
- title, milestone, labels, and assignees match `$issue55Before`;
- all three mapping IDs occur once;
- all six human roles are present;
- historical comments `5071834997` and `5096716394` are unchanged.

- [ ] **Step 5: Add one idempotent synchronization comment**

Use the marker `<!-- v05-beta-deferred-assurance-sync:$mergeSha -->`. Search all paginated comments for that exact marker. Build the exact comment from verified runtime values:

```powershell
$issue55Sync = @(
  "<!-- v05-beta-deferred-assurance-sync:$mergeSha -->"
  "Repository policy synchronization is complete at merged commit ``$mergeSha`` through PR #$($pr.number)."
  "The ``v0.5-beta`` release gate now permits either completed qualified review or one validated exact-candidate owner-risk disposition covering all three exact Draft mapping sets. This changes milestone release sequencing only: ``DEFERRED`` is not an ESAF-1600 lifecycle state."
  "Issue #55 remains open at the human boundary. Named qualified humans must still complete all six separately recorded role dispositions, with owner acceptance of reviewer eligibility and any dual-role arrangement, signed evidence bound to the exact reviewed SHA, and resolution of every Critical and Important finding before any later lifecycle transition."
  "No reviewer metadata, lifecycle event, approval state, or publication state has been added. This synchronization does not establish qualified review, approval, certification, compliance, equivalence, endorsement, external-scheme approval, production readiness, or assurance."
) -join "`n`n"
```

Add `$issue55Sync` only if the marker is absent.

- [ ] **Step 6: Verify issue 55 synchronization**

Re-fetch the issue and all comments. Assert exactly one marker for `$mergeSha`, issue state remains open, and the historical evidence comments remain present.

---

## Task 7: Synchronize GitHub Issue 59

**Files:**

- GitHub issue: `https://github.com/tdistress/ESAF/issues/59`
- Read-only reference: merged policy files at `$mergeSha`

- [ ] **Step 1: Capture current issue state**

```powershell
$issue59Before = gh api repos/tdistress/ESAF/issues/59 | ConvertFrom-Json
$issue59CommentsBefore = @(gh api repos/tdistress/ESAF/issues/59/comments --paginate | ConvertFrom-Json)
$issue59Before | Select-Object number,state,title,updated_at,body
```

Expected: issue 59 is open in milestone `v0.5-beta`. Stop if its body changed materially after the planning snapshot; reconcile before writing.

- [ ] **Step 2: Build the exact replacement body**

Use a PowerShell literal here-string for this body:

```markdown
## Purpose

Close the `v0.5-beta` publication gates on one exact candidate after the milestone content workstreams are complete and the UK mapping assurance requirement has either completed qualified review or a validated coordinated deferred disposition.

## Dependencies

- Define the minimum ESAF-1500 assessment foundation.
- Select and publish one Draft pilot ESAF industry profile.
- Complete PCI DSS source readiness and mapping go/no-go.
- Satisfy the UK mapping assurance gate through one of the two paths below.

HITRUST readiness remains nonblocking for `v0.5-beta`.

## UK mapping assurance paths

The release candidate shall have either:

1. completed qualified-review dispositions for all six human roles tracked in #55; or
2. one authenticated owner-risk decision that defers qualified review for all three exact mapping sets:

   - `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
   - `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
   - `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`

A deferred decision shall:

- use `mapping_decision_basis: owner_risk_acceptance`;
- use `decision_type: owner_risk_acceptance`;
- use `qualified_review_status: deferred`;
- cover each exact mapping-set identifier once;
- bind every decision to the exact `v0.5-beta` release candidate SHA;
- use one uniform decision basis and one authenticated owner source;
- identify the missing qualified human evidence;
- name the accountable owner and re-entry triggers;
- retain Draft lifecycle limitations; and
- preserve the required nonclaims.

The release gate shall reject mixed decision bases, stale candidate SHAs, missing or duplicate mapping decisions, nonuniform owner sources, changed lifecycle state, or weakened nonclaims.

`DEFERRED` is a milestone assurance disposition, not an ESAF-1600 mapping lifecycle state. Under the deferred path, all three mapping sets and their records remain `draft`, no reviewer metadata or lifecycle event is added, and #55 remains open.

## Acceptance criteria

- Scope and milestone approval is recorded on the exact candidate.
- The UK mapping assurance path is validated on the exact candidate.
- Technical, editorial, terminology, mapping, profile-scope, and governance reviews are complete.
- Critical and Important findings are resolved.
- Generated catalogs and traceability records are current.
- The full test suite, control, architecture, crosswalk, assessment, link, release, working-tree, and applicable Mermaid-rendering gates pass on the exact candidate.
- The complete branch diff is reviewed, GitHub checks pass, and merge state is clean.
- Post-merge validation passes before an immutable tag or publication statement is created.
- Final evidence records the exact candidate, merge, tag, counts, reviews, mapping assurance basis, and lifecycle limitations.

## Human-review boundary

Owner-risk acceptance permits Working Draft publication only. It does not complete qualified review and cannot substitute for the six human role dispositions tracked in #55.

A later lifecycle transition requires the existing qualified-review evidence process, owner acceptance of reviewer eligibility and any dual-role arrangement, exact-SHA validation, resolution of every Critical and Important finding, and signed final confirmation.

## Boundaries

Evidence from `v0.4-alpha` is historical and cannot approve `v0.5-beta`.

Publication does not change an artifact lifecycle state without its own evidence.

The deferred path does not claim qualified review, approval, certification, compliance, equivalence, endorsement, external-scheme approval, production readiness, or assurance beyond the recorded Working Draft basis.

This issue does not begin substantive HITRUST mapping, change the PCI DSS `HOLD` disposition, or reintroduce architecture-pattern work into the active backlog.
```

- [ ] **Step 3: Update and verify the issue body**

Before writing, re-read `updated_at` and body. Stop on divergence. Skip an identical body. Otherwise update only the body. Re-fetch and verify:

- state remains `open`;
- title, milestone, labels, and assignees match `$issue59Before`;
- both assurance alternatives are present;
- all three mapping IDs occur once;
- the complete release gate set and nonclaims are present.

- [ ] **Step 4: Add one idempotent synchronization comment**

Search all paginated comments for `<!-- v05-beta-deferred-assurance-sync:$mergeSha -->`. Build the exact comment from verified runtime values:

```powershell
$issue59Sync = @(
  "<!-- v05-beta-deferred-assurance-sync:$mergeSha -->"
  "Repository policy synchronization is complete at merged commit ``$mergeSha`` through PR #$($pr.number)."
  "Issue #59 is now executable under either completed qualified review or validated exact-candidate owner-risk acceptance for all three exact Draft UK mapping sets. No live owner-risk decision is recorded by this comment; that evidence must be acquired and validated against the exact release candidate during release closure unless qualified review completes first."
  "Every other technical, editorial, terminology, mapping, profile-scope, governance, validation, GitHub-check, clean-merge, and post-merge publication gate remains required. Issue #55 remains open under the deferred path."
  "This synchronization does not publish or tag ``v0.5-beta``, change a mapping lifecycle state, or establish qualified review, approval, certification, compliance, equivalence, endorsement, external-scheme approval, production readiness, or assurance."
) -join "`n`n"
```

Add `$issue59Sync` only if the marker is absent.

- [ ] **Step 5: Verify both issues as one coordinated state**

Re-fetch issues 55 and 59 and all comments. Verify:

- both issues remain open;
- each issue has exactly one synchronization marker for `$mergeSha`;
- issue 55 retains the six-role human-review boundary;
- issue 59 is executable under either assurance path;
- titles, labels, milestones, and assignees are unchanged;
- issue 55 historical comments remain unchanged;
- neither body or comment claims that a live owner-risk decision has already been acquired;
- neither issue closes or publishes `v0.5-beta`.

- [ ] **Step 6: Handle partial-write failure safely**

The two issue updates are not transactional. If issue 55 updates and issue 59 fails:

1. re-read both live issues;
2. complete issue 59 from the same verified inputs if safe; or
3. restore issue 55's captured body before retrying.

Prefer preserving a posted synchronization comment with a correction over deleting audit history. Delete only an immediately posted, exact duplicate or malformed comment during the same verified rollback. Never roll back by closing issue 55, changing lifecycle metadata, or altering historical evidence comments.

---

## Task 8: Close the Policy-Implementation Workstream

**Files:**

- Verify: main worktree and temporary worktree
- Do not begin: issue 59 release-candidate construction

- [ ] **Step 1: Record final synchronized evidence**

Capture:

- merged policy PR URL and merge SHA;
- post-merge focused validation result;
- issue 55 and 59 URLs;
- synchronization comment URLs;
- confirmation that both issues remain open;
- confirmation that no tag or publication action occurred.

- [ ] **Step 2: Verify main is clean**

```powershell
git -C C:\Users\phrea\OneDrive\Documents\ESAF status --short
git -C C:\Users\phrea\OneDrive\Documents\ESAF rev-parse HEAD
git -C C:\Users\phrea\OneDrive\Documents\ESAF rev-parse origin/main
```

Expected: the main worktree is clean and local main equals `origin/main`.

- [ ] **Step 3: Remove the temporary branch and worktree**

Resolve and verify the exact temporary worktree path before removal:

```powershell
git -C C:\Users\phrea\OneDrive\Documents\ESAF worktree list --porcelain
git -C C:\Users\phrea\OneDrive\Documents\ESAF worktree remove `
  'C:\Users\phrea\OneDrive\Documents\ESAF\.worktrees\agent-v05-deferred-assurance-design'
git -C C:\Users\phrea\OneDrive\Documents\ESAF branch -d agent/v05-deferred-assurance-design
```

Expected: the merged temporary worktree and local branch are removed. Delete the remote branch only if it was not already removed by the PR merge.

- [ ] **Step 4: Stop before release closure**

Report that repository policy and issue tracking are synchronized. The next separate implementation effort is issue 59 release closure, including creation of a clean exact candidate and acquisition of a live exact-candidate owner-risk decision unless qualified review completes first.

Do not create a release candidate, owner decision, tag, or publication record under this plan.
