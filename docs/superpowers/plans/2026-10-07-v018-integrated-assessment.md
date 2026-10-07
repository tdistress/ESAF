# ESAF v0.18-draft Integrated Assessment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish one coherent, fictional Summit Analytics `CAP-140` assessment case across ESAF-1500 workbook, evidence, audit, maturity, and governance examples, and close the `v0.18-draft` publication gates.

**Architecture:** Keep authoritative examples in their existing toolkit directories and add a single overview at `assessment/integrated-assessment.example.md`. Use the existing workbook API-100 evidence/result as canonical, remove the duplicate audit API-100 result, add the missing MOD-100 evidence record, and link all artifacts by existing ESAF-1500 identifier patterns. Record the milestone and exact-candidate publication readiness using the repository's established v0.17 release-gate pattern; do not change normative requirements or schemas.

**Tech Stack:** Markdown, JSON, Python 3.13, `unittest`, JSON Schema, GitHub CLI, repository validation tools.

---

## File map

### Integrated case and indexes

- Create `assessment/integrated-assessment.example.md` as the canonical case entry point and end-to-end artifact map.
- Modify `assessment/README.md` to surface the integrated case.
- Modify `assessment/workbook/engagement3-vignette.example.md` and `assessment/workbook/examples/engagement3-assessment-result.example.json` to describe the full API-100 examination and test work while preserving the open finding and Draft state.
- Modify `assessment/workbook/examples/engagement3-maturity-assessment.example.json` to retain an independent, bounded API-100 maturity scope and consistent evidence/result identifiers.
- Keep `assessment/workbook/examples/engagement3-evidence-record.example.json` as the canonical API-100 configuration evidence record.
- Create `assessment/workbook/examples/engagement3-mod100-evidence-record.example.json` for the model-registry artifact cited by the MOD-100 result.
- Modify `assessment/workbook/README.md` and `assessment/workbook/examples/README.md` to link the integrated overview and both evidence records.
- Modify `assessment/audit-checklist/sampling3-vignette.example.md` and `assessment/audit-checklist/README.md` to cite the canonical workbook API-100 result and the audit-owned MOD-100 result/evidence.
- Delete `assessment/audit-checklist/examples/sampling3-api100-assessment-result.example.json` after all distinct API-100-A1/A2 procedure detail and limitations have been preserved in the canonical workbook result and audit vignette.
- Keep `assessment/audit-checklist/examples/sampling3-mod100-assessment-result.example.json` as the canonical MOD-100 result.
- Modify `assessment/evidence-catalog/README.md` to link the case as an example of configuration and record evidence types without reusing the catalog-demo evidence IDs.
- Modify `templates/examples/governance-thread3.example.md` and `templates/README.md` to link the canonical API-100 evidence/result and MOD-100 result to the risk and retirement follow-up.

### Regression coverage

- Modify `tests/test_assessment_foundation.py` to schema-validate the new evidence record and assert the integrated case's key identity/reference relationships, uniqueness of the API-100 result, explicit Draft/fictitious boundaries, and overview/index discoverability.
- Modify `tests/test_governance_templates_starter.py` only if its current third-thread assertions need to follow changed links or names.
- Create `tests/test_v018_draft_release_gates.py` for candidate-bound release-evidence validation.
- Modify `tools/test-shards.json` to register the new test module in the correct shard.
- Modify `tests/test_plan_validation.py` when the planner gains a v0.18 publication command.

### Milestone and publication records

- Modify `project/MILESTONES.md` to define `v0.18-draft` entry, workstreams, exit criteria, and non-goals.
- Modify `project/BACKLOG.md` to add the new GitHub work items and preserve the separate status of issues #60 and #219.
- Modify `ROADMAP.md` with the approved v0.18 sequence while keeping the published version at 0.17 until release closure.
- Modify `project/RELEASE_PLAN.md` to add the v0.18 publication evidence section without changing the closed v0.17 record.
- Create `docs/superpowers/reviews/2026-10-07-v018-draft-publication-readiness.md` as the candidate-bound evidence record.
- Create `tools/v018_draft_release_gates.py` and `tests/test_v018_draft_release_gates.py` following the phase-aware `v0.17` validator pattern, adapted to this bounded example-only scope.
- Modify `tools/test-shards.json` to register the new release-gate test module in its correct shard, with lexicographically sorted module names.
- Modify `tools/README.md` and `.github/workflows/catalog-validation.yml` to document and run the v0.18 release gate and its tests.
- In the closure-candidate PR, modify `README.md`, `VERSION.md`, `CHANGELOG.md`, and the top of `ROADMAP.md` to identify v0.18 as the candidate without claiming publication. After the annotated tag exists, update these surfaces and the readiness record with publication date and exact tag-object/tagged-commit evidence.

## Task 1: Add regression coverage for the integrated artifact graph

**Files:**
- Modify: `tests/test_assessment_foundation.py`
- Modify: `tests/test_governance_templates_starter.py` if existing third-thread assertions require it
- Run: focused unittest discovery for both modified modules

- [ ] **Step 1: Add a failing integrated-case test.** Assert that the overview, workbook vignette, audit vignette, and governance thread share one canonical API-100 result ID and evidence ID; that the audit result set contains no second API-100 JSON record; that MOD-100's cited evidence ID resolves to a filled evidence-record JSON; and that linked result/evidence/maturity JSON documents validate against their existing schemas.
- [ ] **Step 2: Add discoverability and nonclaim assertions.** Assert the overview is linked from `assessment/README.md`, the workbook and audit indexes, the evidence catalog index, and the governance-template index; assert the integrated records and narrative stay fictional and Draft and do not introduce an external compliance claim or normative `shall`.
- [ ] **Step 3: Run the focused tests and confirm the intended failure.**

Run:

```shell
python -m unittest discover -s tests -p 'test_assessment_foundation.py' -v
python -m unittest discover -s tests -p 'test_governance_templates_starter.py' -v
```

Expected: the new integrated-case checks fail because there is no overview or MOD-100 evidence record yet and the API-100 audit result is duplicated.

## Task 2: Reconcile the Summit Analytics assessment records

**Files:**
- Create: `assessment/integrated-assessment.example.md`
- Create: `assessment/workbook/examples/engagement3-mod100-evidence-record.example.json`
- Modify: `assessment/workbook/engagement3-vignette.example.md`
- Modify: `assessment/workbook/examples/engagement3-assessment-result.example.json`
- Modify: `assessment/workbook/examples/engagement3-maturity-assessment.example.json`
- Modify: `assessment/audit-checklist/sampling3-vignette.example.md`
- Modify: `assessment/audit-checklist/examples/sampling3-mod100-assessment-result.example.json`
- Modify: `templates/examples/governance-thread3.example.md`
- Delete: `assessment/audit-checklist/examples/sampling3-api100-assessment-result.example.json`

- [ ] **Step 1: Define one stable engagement identity in the overview.** Use the existing Summit Analytics `CAP-140` scenario, scope the sample to `API-100` and `MOD-100`, and state the period, population/sample boundary, assessor independence, exclusions, limitations, and explicit nonclaims.
- [ ] **Step 2: Make the workbook API-100 evidence and result canonical.** Retain `EVD-ENG3-API100-GATEWAY` and `ASR-ENG3-API100`; fold the distinct API-100-A1 examination and API-100-A2 staging test work into that single result; retain the open emergency-restriction finding and staging limitation; keep `MAT-ENG3-API100` separate and bounded to API-100.
- [ ] **Step 3: Add the MOD-100 evidence record and reconcile the result.** Create a schema-conforming fictional record for the model-registry artifact using the current `EVD-SAMP3-MOD100-REGISTRY` reference; preserve the MOD-100-A1/A2/A3 examination, deployment reconciliation, and interview details in `ASR-SAMP3-MOD100` and the audit vignette. Keep MOD-100 result Draft because the sample is bounded to one alias.
- [ ] **Step 4: Remove the duplicated API-100 audit result file.** Update the audit vignette to cite `ASR-ENG3-API100` and `EVD-ENG3-API100-GATEWAY` from the workbook location while retaining the audit checklist's two-control selection and procedure-level test notes. Preserve `ASR-SAMP3-MOD100` as the audit-owned MOD-100 result.
- [ ] **Step 5: Link governance follow-up to the canonical assessment.** Update the governance thread so its risk/retirement excerpt references the canonical API-100 evidence/result and the integrated assessment overview; clearly distinguish assessment findings, residual risk, governance decisions, and retirement verification.
- [ ] **Step 6: Run the focused tests and check the new JSON records.**

Run:

```shell
python -m unittest discover -s tests -p 'test_assessment_foundation.py' -v
python -m unittest discover -s tests -p 'test_governance_templates_starter.py' -v
```

Expected: all focused tests pass; each integrated JSON record conforms to its existing ESAF-1500 schema; no duplicated API-100 result remains.

## Task 3: Make the case discoverable from each toolkit

**Files:**
- Modify: `assessment/README.md`
- Modify: `assessment/workbook/README.md`
- Modify: `assessment/workbook/examples/README.md`
- Modify: `assessment/audit-checklist/README.md`
- Modify: `assessment/evidence-catalog/README.md`
- Modify: `templates/README.md`

- [ ] **Step 1: Add the overview to the assessment index.** Describe the case as an informative fictional example and link the entry point.
- [ ] **Step 2: Update workbook and audit indexes.** Show which shared records belong to the integrated engagement and distinguish the canonical API-100 result from the audit-owned MOD-100 result.
- [ ] **Step 3: Update the evidence catalog index.** Link the integrated case as an example of using the configuration and record evidence types; retain the catalog examples' separate demo identities.
- [ ] **Step 4: Update the governance-template index.** Link the governance thread and integrated overview without implying that a risk acceptance or retirement action changes the assessment result.
- [ ] **Step 5: Run focused tests and repository-local link validation.**

Run:

```shell
python -m unittest discover -s tests -p 'test_assessment_foundation.py' -v
python -m unittest discover -s tests -p 'test_governance_templates_starter.py' -v
python tools/validate_links.py --check
```

Expected: focused tests pass and every new relative link resolves.

## Task 4: Establish the v0.18 milestone and GitHub work queue

**Files:**
- Modify: `project/MILESTONES.md`
- Modify: `project/BACKLOG.md`
- Modify: `ROADMAP.md`
- Create/update through GitHub CLI: milestone `v0.18-draft` and its work issues

- [ ] **Step 1: Add the v0.18 milestone definition.** Record the entry state, one integrated-case workstream, publication workstream, explicit no-crosswalk-verifier boundary, exit criteria, and non-goals from the approved spec. Keep all prior milestone text intact.
- [ ] **Step 2: Add the post-v0.17 sequence to the roadmap and backlog.** Keep v0.17 published metadata intact. Mark issues #60 and #219 as separately gated and not v0.18 exit criteria.
- [ ] **Step 3: Create the GitHub `v0.18-draft` milestone.** Use the approved scope as its description and due date only if an owner-approved date is present; otherwise omit a due date.
- [ ] **Step 4: Create two milestone issues.** One issue tracks the integrated assessment case (including IDs, schemas, indexes, and content review); the other tracks exact-candidate publication gates and status synchronization. Apply existing project labels and avoid inventing new labels.
- [ ] **Step 5: Replace planning placeholders with actual issue URLs/numbers and compare repository/GitHub scope.** Ensure every issue acceptance criterion is consistent with the approved spec and no additional verifier is listed as a prerequisite.
- [ ] **Step 6: Run the release-metadata planning tests.**

Run:

```shell
python -m unittest discover -s tests -p 'test_release_metadata.py' -v
```

Expected: all planning and prior published-status consistency tests pass.

## Task 5: Add exact-candidate v0.18 publication readiness gates

**Files:**
- Create: `docs/superpowers/reviews/2026-10-07-v018-draft-publication-readiness.md`
- Create: `tools/v018_draft_release_gates.py`
- Create: `tests/test_v018_draft_release_gates.py`
- Modify: `tools/test-shards.json`
- Modify: `tools/plan_validation.py`
- Modify: `tests/test_plan_validation.py`
- Modify: `tools/README.md`
- Modify: `.github/workflows/catalog-validation.yml`

- [ ] **Step 1: Write failing release-gate contract tests.** Start from `tests/test_v017_draft_release_gates.py` and define tests for `evidence_candidate`, `closure_candidate`, and `published`; exact milestone scope; the one integrated-case deliverable; zero need for qualified crosswalk review; no premature version advancement; and all mandatory ordinary gates.
- [ ] **Step 2: Run the focused release-gate tests and verify the expected failure.**

Run:

```shell
python -m unittest discover -s tests -p 'test_v018_draft_release_gates.py' -v
```

Expected: import or contract failures because the v0.18 validator and record do not exist.

- [ ] **Step 3: Create the evidence-candidate readiness record and minimal validator.** Follow `tools/v017_draft_release_gates.py` and its record. Bind scope and gate state to the exact candidate; enforce the standard `evidence_candidate` → `closure_candidate` → `published` progression, candidate/base SHA, publication tag identity, evidence locators, and no stale/open gate at publication. The initial record has all gates open and no version advancement; keep v0.17 validators and evidence frozen.
- [ ] **Step 4: Complete the release-gate contract tests.** Include deterministic temporary Git fixtures for candidate/base/tag states, positive transitions, malformed records, mismatched SHA/tag, missing ordinary review evidence, and a published record committed after its tag target. Require the standards-mapping gate to be explicitly `not_applicable` because v0.18 changes no mapping artifacts; do not require a qualified external crosswalk reviewer.
- [ ] **Step 5: Register the new test module in the correct shard.** Keep the module list lexicographically sorted and verify shard-manifest validation.
- [ ] **Step 6: Add the planner command and test its exact command vector.** Add `v018-draft-release-gates` to `tools/plan_validation.py` as a publication-tier command with `--baseline-ref {base}`, and update `tests/test_plan_validation.py` expected catalog data.
- [ ] **Step 7: Wire local documentation and CI.** Add the v0.18 check to `tools/README.md` and `.github/workflows/catalog-validation.yml`; ensure pull-request and protected-branch invocations pass the correct baseline reference.
- [ ] **Step 8: Run focused release-gate, planner, and shard-manifest checks.**

Run:

```shell
python -m unittest discover -s tests -p 'test_v018_draft_release_gates.py' -v
python -m unittest discover -s tests -p 'test_plan_validation.py' -v
python tools/validate_test_shards.py --check
```

Expected: release-gate tests pass and the new module is registered once in the intended shard.

## Task 6: Freeze and validate the publication candidate

**Files:**
- Modify as required: `docs/superpowers/reviews/2026-10-07-v018-draft-publication-readiness.md`
- Modify as required: `project/RELEASE_PLAN.md`
- Modify as required: `README.md`
- Modify as required: `VERSION.md`
- Modify as required: `CHANGELOG.md`
- Modify as required: `ROADMAP.md`
- Review: complete branch diff

- [ ] **Step 1: Run applicable focused artifact validation.**

Run:

```shell
python tools/validate_assessment.py --check
python tools/validate_controls.py --check
python tools/validate_links.py --check
python -m unittest discover -s tests -p 'test_assessment_foundation.py' -v
python -m unittest discover -s tests -p 'test_governance_templates_starter.py' -v
python -m unittest discover -s tests -p 'test_v018_draft_release_gates.py' -v
```

Expected: all commands pass. There are no Mermaid changes in this scope.

- [ ] **Step 2: Prepare candidate version surfaces.** Update the README badge/status, `VERSION.md`, changelog history/entry, and roadmap version to identify `v0.18-draft` as the closure candidate and state that publication is conditional on the annotated tag. Keep the readiness record in `closure_candidate` with tag object and publication date unset.
- [ ] **Step 3: Run the full required test suite and release gates on the frozen SHA.** Use `--baseline-ref <evidence-candidate-sha>` for the v0.18 closure-candidate transition.

Run:

```shell
python -m unittest discover -s tests -v
python tools/release_gates.py --check
python tools/v017_draft_release_gates.py --check
python tools/v018_draft_release_gates.py --check --baseline-ref <evidence-candidate-sha>
git diff --check origin/main...HEAD
```

Expected: all required tests and gates pass; v0.17 remains valid; v0.18 is in the `closure_candidate` phase; candidate version surfaces are synchronized without claiming publication; branch diff has no whitespace errors.

- [ ] **Step 4: Review the entire branch diff.** Confirm no normative/schema changes, no unintended edits to earlier examples/releases, complete traceability among all integrated artifacts, and no generated caches/build outputs.
- [ ] **Step 5: Obtain exact-SHA technical, editorial, and governance review.** Resolve Critical and Important findings; refresh all affected gates and reviews after any candidate change.
- [ ] **Step 6: Fetch `origin/main` immediately before PR creation.** Integrate any base changes and rerun every affected gate and exact-head review if the merge base advances.
- [ ] **Step 7: Open a reviewable PR with validation merge base and reviewed head SHA in the description.** Attach the PR to this Codex task.
- [ ] **Step 8: Merge only after required GitHub checks pass and the merge state is clean.** Verify the PR is `MERGED` and the merge commit is on `origin/main` before proceeding.

## Task 7: Publish v0.18-draft and synchronize public status

**Files:**
- Modify: `project/RELEASE_PLAN.md`
- Modify: `docs/superpowers/reviews/2026-10-07-v018-draft-publication-readiness.md`
- Modify: `README.md`
- Modify: `VERSION.md`
- Modify: `CHANGELOG.md`
- Modify: `ROADMAP.md`
- Update: GitHub tag and publication issue/milestone

- [ ] **Step 1: Validate the merged closure candidate before tagging.** Fetch `origin/main`, record the exact merge commit, run post-merge validation and the v0.18 closure-candidate gate on that commit, and collect the CI run, PR merge, and post-merge evidence needed to close the post-merge gate.
- [ ] **Step 2: Create the annotated `v0.18-draft` tag on the exact merged closure-candidate commit.** Do this only after required checks pass; do not put tag-object data into a commit before the tag exists.
- [ ] **Step 3: Verify the remote annotated tag.** Record the tag object SHA and peeled commit SHA; require the peeled commit to equal the validated closure-candidate merge commit.
- [ ] **Step 4: Record published truth in a post-tag commit.** Set the readiness record to `published`, recording the tag object, tagged closure-candidate commit, publication date, and issue evidence URL. State explicitly that the annotated tag intentionally targets the validated closure-candidate commit and that this later commit records published status without changing the tag target. Update the release plan, README, VERSION, changelog, and roadmap with published status while preserving v0.17 history.
- [ ] **Step 5: Validate the post-tag published record.** Run `python tools/v018_draft_release_gates.py --check --baseline-ref <closure-candidate-merge-sha>` and require it to verify the existing remote tag identity, closed gates, and `tagged_commit` without incorrectly requiring the post-tag record commit itself to be the tag target. Preserve immutable publication identity on later `published`-to-`published` maintenance.
- [ ] **Step 6: Close the GitHub publication issue and milestone only after tag, post-merge validation, and all required evidence are recorded.** Leave #60 and #219 open in their separately gated state.
- [ ] **Step 7: Confirm the final `main` checkout is clean and recoverable.** Preserve the spec and implementation plan commits and archive the worktree only after the branch has been integrated and no further task work needs it.

## Constraints for implementation

- Follow `docs/superpowers/specs/2026-10-07-v018-draft-next-steps-design.md` as the approved scope.
- Use exact existing ESAF-1500 record shapes and identifier patterns; do not modify schemas or normative semantics.
- Keep all example names, organizations, evidence, dates, judgments, and findings explicitly fictional.
- Retain API-100-A1/A2 procedures and all existing limitations when removing the duplicate result record.
- Do not use a risk acceptance or retirement record to convert a Draft result to final or to imply control satisfaction.
- Do not make qualified external crosswalk review a v0.18 exit criterion.
- Set `PYTHONDONTWRITEBYTECODE=1` during Python validation and confirm there are no `__pycache__` directories before declaring the final checkout clean.
