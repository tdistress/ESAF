# v0.20 API-100 Evidence-Complete Follow-up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one fictional, schema-valid API-100-A3 follow-up whose complete staging evidence resolves only the distinct open finding from the inconclusive follow-up, and define the v0.20-draft milestone.

**Architecture:** Reuse existing evidence and assessment-result contracts. Add a separate evidence/result/narrative package, link it into the integrated CAP-140 case and indexes, and keep all prior results unchanged. Record the bounded scope in project trackers and the existing GitHub milestone/issues.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python unittest, assessment and repository validators, GitHub CLI/API.

---

## File map

- `tests/test_validate_assessment.py`: Assert result status and bounded outcome, cross-references, prior result identity, and distinct resolved finding.
- `assessment/examples/api100-evidence-complete-follow-up-evidence-record.example.json`: Complete fictional event evidence for one staging exercise.
- `assessment/examples/api100-evidence-complete-follow-up-assessment-result.example.json`: Separate Draft reassessment and distinct resolved finding.
- `assessment/follow-up/api100-evidence-complete-follow-up.example.md`: Chronology, evidence limits, and links to prior and new records.
- `assessment/integrated-assessment.example.md`, `assessment/README.md`, `assessment/workbook/README.md`, `assessment/workbook/examples/README.md`: Discovery links and concise record-flow explanation.
- `project/MILESTONES.md`, `project/BACKLOG.md`, `project/RELEASE_PLAN.md`: Planned v0.20 scope, issues, gates, and exclusions.
- `docs/superpowers/specs/2026-11-13-v020-api100-evidence-complete-followup-design.md`: Approved design and boundaries.

## Task 1: Lock the new record contract with a test

**Files:** `tests/test_validate_assessment.py`

- [ ] Add a focused test checking Draft status, bounded determination and effectiveness fields, an own resolved finding, the prior finding's preserved historical open status, and evidence/result cross-references.
- [ ] Run `PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_validate_assessment.AssessmentValidationTests.test_evidence_complete_api100_followup_resolves_only_scoped_finding -v` and confirm it fails because the new records do not exist.

## Task 2: Add evidence and reassessment records

**Files:** the two new JSON examples under `assessment/examples/`.

- [ ] Reuse the existing schemas and identifier patterns. Use one complete staging event trail with timestamps, test alias, restriction action, blocked request, retained events, custodian, and bounded collection period.
- [ ] Keep the result Draft, scoped to API-100-A3, and limited to one staging exercise; record one distinct resolved finding for the evidence gap, with operating effectiveness `not_assessed`.
- [ ] Link the evidence and result bidirectionally and cite the prior inconclusive result and finding without modifying prior JSON files.
- [ ] Run the focused regression and `PYTHONDONTWRITEBYTECODE=1 python tools/validate_assessment.py --check`.

## Task 3: Integrate the narrative and discovery links

**Files:** new narrative plus assessment overview and index files listed above.

- [ ] Explain that the later complete event trail supports only the bounded follow-up result; retain all production, recovery, sustained-effectiveness, A1/A2, and non-claim boundaries.
- [ ] Show the sequence of the historical result, v0.19 narrow successful exercise, inconclusive follow-up, and this later reassessment.
- [ ] Link the narrative and records from all relevant indexes without changing historic records.
- [ ] Run focused assessment tests, the assessment validator, and link validation.

## Task 4: Define and synchronize v0.20 tracking

**Files:** `project/MILESTONES.md`, `project/BACKLOG.md`, `project/RELEASE_PLAN.md`.

- [ ] Add v0.20 entry state, bounded required work, exit criteria, non-goals, and references to GitHub milestone 14 / Issues #234 and #235.
- [ ] Keep `README.md`, `VERSION.md`, and `CHANGELOG.md` describing v0.19 as the current published release; no tag or publication status change is part of this candidate.
- [ ] Run repository link and project-metadata validations.

## Task 5: Review and validate the candidate

- [ ] Run the route selected by `PYTHONDONTWRITEBYTECODE=1 python tools/plan_validation.py --base origin/main --candidate HEAD`.
- [ ] Run focused assessment tests, `PYTHONDONTWRITEBYTECODE=1 python tools/validate_assessment.py --check`, the full unittest suite, applicable control/architecture/profile/crosswalk/Markdown/Mermaid gates, and `git diff --check`.
- [ ] Review the full branch diff and obtain independent exact-candidate technical/editorial review. Fix Critical and Important findings, then rerun affected gates and reviews.

## Completion boundary

This branch defines and implements the v0.20-draft work but does not publish a
v0.20 tag, update current published status surfaces, or close milestone issues.
Those actions belong to Issue #235 after its gates pass.
