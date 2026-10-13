# v0.19 Assessment Follow-Through Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a bounded fictional API-100 assessment follow-through case showing an owner action and a separately recorded reassessment of the existing open finding, without changing normative requirements or assessment contracts.

**Architecture:** Add a small assessment follow-up example package with a Markdown action narrative and schema-conforming evidence and assessment-result JSON. Keep the v0.18 result immutable and connect the new result using the original finding reference, distinct follow-up finding ID, existing evidence traceability fields, procedure references, and index links. Update v0.19 planning and publication metadata only after content and validation are complete.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python `unittest`, repository assessment validator and release-validation tools.

---

## Files and responsibilities

- Modify `tests/test_assessment_foundation.py` to lock the follow-up package's cross-links, distinct finding identity, scope limits, and non-claim boundary.
- Create `assessment/follow-up/api100-remediation.example.md` for the fictional owner action, evidence of completion, and explicit relation to the original and follow-up findings.
- Create `assessment/examples/api100-follow-up-evidence-record.example.json` as the later API-100-A3 exercise evidence record in the validator's canonical example set.
- Create `assessment/examples/api100-follow-up-assessment-result.example.json` as the distinct Draft reassessment result and resolved follow-up finding in the validator's canonical example set.
- Modify `assessment/integrated-assessment.example.md`, `assessment/README.md`, and `assessment/workbook/examples/README.md` as needed to make the follow-up discoverable without altering the historical v0.18 result.
- Modify `README.md`, `CHANGELOG.md`, `VERSION.md`, `project/ROADMAP.md`, `project/BACKLOG.md`, `project/MILESTONES.md`, and `project/RELEASE_PLAN.md` to define and synchronize the bounded v0.19-draft effort and, after publication, its exact evidence.
- Register the touched or new test module in `tools/test-shards.json` if a new test module is added. Prefer extending the existing assessment-foundation module to avoid unnecessary shard changes.

### Task 1: Add focused regression coverage

**Files:**
- Modify: `tests/test_assessment_foundation.py`
- Test: `tests/test_assessment_foundation.py`

- [ ] **Step 1: Add assertions for the follow-up package contract**

Assert that the action narrative points to the original `ASR-ENG3-API100` and
`FND-ENG3-API100-EMERGENCY`, that the follow-up result uses a distinct finding
ID and explicitly cross-references the original, that the JSON records use the
existing schemas, that the follow-up scope remains API-100 and API-100-A3, and
that the package states its fictional/non-claim limitations.

- [ ] **Step 2: Run the focused test and confirm it fails**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_assessment_foundation.py' -v`

Expected: FAIL because the follow-up package has not yet been added.

### Task 2: Add follow-up evidence and assessment result

**Files:**
- Create: `assessment/examples/api100-follow-up-evidence-record.example.json`
- Create: `assessment/examples/api100-follow-up-assessment-result.example.json`

- [ ] **Step 1: Add the later emergency-restriction exercise evidence**

Use a new `EVD-` identifier, fictional source and custodian, an explicit
collection period and sample, all seven quality attributes, a bounded
sufficiency rationale, illustrative integrity value, limitations, and
traceability to `API-100`, `API-100-A3`, and the follow-up `ASR-` identifier.

- [ ] **Step 2: Add a distinct Draft follow-up assessment result**

Use a new `ASR-` identifier and a distinct `FND-` identifier. Reuse only the
API-100-A3 procedure and new evidence for the follow-up determination. State
the follow-up boundary, excluded retests, independent assessor statement,
limited effectiveness basis, dated resolved disposition, cross-reference to
the original finding, and fictional notice. Do not alter
`ASR-ENG3-API100`.

- [ ] **Step 3: Run the existing assessment validator**

Run: `PYTHONDONTWRITEBYTECODE=1 python tools/validate_assessment.py --check`

Expected: PASS with both new records schema-valid and all references
resolvable.

### Task 3: Add action narrative and discoverability links

**Files:**
- Create: `assessment/follow-up/api100-remediation.example.md`
- Modify: `assessment/integrated-assessment.example.md`
- Modify: `assessment/README.md`
- Modify: `assessment/workbook/examples/README.md` if the index includes this workbook-owned API-100 lineage.

- [ ] **Step 1: Write the action narrative**

Record the fictional finding owner, action, completion point, verification
method, and links to the original result, original finding, new evidence, and
follow-up result. State that the follow-up finding ID is distinct because
findings are nested within one result, and the original result remains
historical and unchanged.

- [ ] **Step 2: Link the follow-up from the integrated case and assessment index**

Add a follow-up section that explains the original partial result remains
historical, the new API-100-A3 check supports only the bounded follow-up
disposition, and no other API-100 procedure or production population is
reassessed. Link all artifacts from the assessment index.

- [ ] **Step 3: Run focused test and validation**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_assessment_foundation.py' -v`

Expected: PASS.

### Task 4: Define v0.19 scope and publication state

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `VERSION.md`
- Modify: `project/ROADMAP.md`
- Modify: `project/BACKLOG.md`
- Modify: `project/MILESTONES.md`
- Modify: `project/RELEASE_PLAN.md`
- Create: `tools/v019_draft_release_gates.py`
- Create: `tests/test_v019_draft_release_gates.py`
- Modify: `tools/plan_validation.py`, `tools/test-shards.json`, `.github/workflows/catalog-validation.yml`, and `tools/README.md` for release-gate wiring.
- Create: `docs/superpowers/reviews/2026-10-13-v019-draft-publication-readiness.md`

- [ ] **Step 1: Add a v0.19-draft milestone and bounded exit criteria**

Describe the follow-up package, artifact traceability, review and validation
gates, and publication closure. Explicitly exclude SOC 2 and HITRUST readiness,
all external mapping work, new normative requirements, schema changes, and a
general remediation model. Keep gated issues outside the milestone.

- [ ] **Step 2: Add the v0.19 readiness record and candidate scope surfaces**

Create a v0.19 exact-candidate readiness record with the deliverable, required
gates, gate evidence, and phase transitions required by the dedicated
validator in Task 5. Add the v0.19 effort and candidate publication plan to
roadmap, backlog, milestones, and release plan. Keep README and VERSION
describing v0.18 as the current published release, and do not claim v0.19 is
published.

### Task 5: Add the executable v0.19 publication readiness gate

**Files:**
- Create: `tools/v019_draft_release_gates.py`
- Create: `tests/test_v019_draft_release_gates.py`
- Modify: `tools/plan_validation.py`
- Modify: `tools/test-shards.json`
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tools/README.md`
- Modify: `docs/superpowers/reviews/2026-10-13-v019-draft-publication-readiness.md`

- [ ] **Step 1: Add deterministic release-gate fixture tests**

Cover valid `evidence_candidate`, `closure_candidate`, and `published`
readiness states; reject invalid transitions and mismatched deliverable/gate
states; bind the readiness record to committed HEAD and an exact ancestor
baseline; require annotated `v0.19-draft` to target the validated closure
candidate; and permit published-to-published status maintenance only when tag
identity and closed gate truth remain immutable. Use isolated temporary Git
repositories and deterministic refs, never the ambient absence of a tag.

- [ ] **Step 2: Run the new gate tests and confirm they fail**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_v019_draft_release_gates.py' -v`

Expected: FAIL because the v0.19 gate module is not implemented.

- [ ] **Step 3: Implement the release-specific readiness validator**

Follow the v0.18 gate interface while binding only the v0.19 readiness record,
milestone, issue, deliverable, gate IDs, publication state, and tag. Validate
phase-specific evidence, exact-candidate record commitment, baseline ancestry,
phase transition truth, annotated-tag identity and target, and immutable
published-to-published metadata.

- [ ] **Step 4: Wire the gate into reviewed policy, tests, CI, and documentation**

Add the v0.19 command to the static validation catalog and publication route,
bind `{v019_base}` from the committed readiness record, add it to relevant
workflow path filters, register the new test module in the correct sorted
shard, and document its candidate and baseline invocation in `tools/README.md`.

- [ ] **Step 5: Run focused gate and planner tests**

Run `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_v019_draft_release_gates.py' -v` and `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_plan_validation.py' -v`.

Expected: PASS with deterministic candidate and baseline behavior.

### Task 6: Validate and review the exact candidate

**Files:**
- Review the complete branch diff, readiness record, and all release status surfaces.

- [ ] **Step 1: Fetch the base and check route and exact candidate state**

Run: `git fetch origin main`, then
`PYTHONDONTWRITEBYTECODE=1 python tools/plan_validation.py --base origin/main --candidate HEAD`.

Follow the route selected for the current candidate. Immediately before
opening the PR, fetch `origin/main` again and record the validation merge
base. If the base advanced, integrate it, rerun affected validation, and
redispatch exact-head reviews. If any commit changes the candidate SHA after
validation, rerun every affected gate.

- [ ] **Step 2: Run required validations**

Run `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`,
`PYTHONDONTWRITEBYTECODE=1 python tools/validate_assessment.py --check`,
`PYTHONDONTWRITEBYTECODE=1 python tools/validate_controls.py --check`,
`PYTHONDONTWRITEBYTECODE=1 python tools/validate_architectures.py`,
`git diff --check <merge-base>..HEAD`, relevant link/release checks, and render every Mermaid
diagram if any Mermaid content changes.

- [ ] **Step 3: Complete independent technical, editorial, and governance review**

Resolve Critical and Important findings. Record lower-severity dispositions
and the exact reviewed head SHA. No external crosswalk verifier is required
because this effort contains no external mapping records.

- [ ] **Step 4: Merge, validate merged main, and tag the closure candidate**

Merge the reviewed PR only after required GitHub checks pass and the merge
state is clean. Update local `main` and rerun SHA-bound validation and
applicable required post-merge gates against the merge commit; the PR head is
a different candidate. If the merged candidate passes, create the annotated
`v0.19-draft` tag against that exact validated closure-candidate commit.

- [ ] **Step 5: Record publication and synchronize published status**

After tag creation, update the readiness record with immutable tag object,
tagged commit, publication date, and evidence; synchronize README, VERSION,
CHANGELOG, roadmap, release plan, backlog, and milestones. Keep the tag target
unchanged. Validate the `published` to `published` readiness transition and
rerun any SHA-bound checks required on the status commit. Verify the final
worktree is clean and the readiness record points to the verified tag.
