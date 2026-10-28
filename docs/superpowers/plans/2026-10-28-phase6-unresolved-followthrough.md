# Phase 6 Unresolved Follow-through Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one fictional, schema-valid example of inconclusive remediation follow-through and its governance handoff to the Phase 6 toolkit.

**Architecture:** Reuse ESAF-1500's current evidence and assessment-result schemas. Add separate evidence, Draft result, narrative, and governance-thread records; connect them to existing CAP-140 examples with narrative links and index updates. Use only schema-defined `not_assessed` outcomes because the evidence cannot support a control determination.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python unittest, repository assessment/link validators.

---

## File map

- `tests/test_validate_assessment.py`: Add a regression test in this existing registered module for the new follow-up record's `not_assessed` outcome, open finding, historical linkage, and evidence/result reference. No new test module or shard-manifest entry is needed.
- `assessment/examples/api100-inconclusive-follow-up-evidence-record.example.json`: New fictional technical-test evidence record.
- `assessment/examples/api100-inconclusive-follow-up-assessment-result.example.json`: New schema-conforming Draft result with an open finding.
- `assessment/follow-up/api100-inconclusive-follow-up.example.md`: Narrative for the attempted but inconclusive staging test and explicit evidentiary limits.
- `templates/examples/governance-thread4.example.md`: Bounded risk-review handoff linked to the new finding, with no risk acceptance or finding closure.
- `assessment/integrated-assessment.example.md`: Chronology, record ownership, links, and nonclaims for the fourth follow-through example.
- `assessment/README.md`, `assessment/workbook/README.md`, `templates/README.md`: Discovery links to the new records.

## Task 1: Lock the intended record behavior with a regression test

**Files:**
- Modify: `tests/test_validate_assessment.py`

- [ ] Add a focused test that loads the new result and evidence JSON and checks `status == "draft"`, all three outcome fields are `not_assessed`, the result's own finding stays `open`, its finding statement and disposition rationale cite the prior API-100 finding, and evidence/result IDs cross-reference each other.
- [ ] Run `PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_validate_assessment.AssessmentValidationTests.test_inconclusive_api100_followup_preserves_open_finding -v` and confirm it fails because the new records do not yet exist.

## Task 2: Add linked inconclusive follow-up records

**Files:**
- Create: `assessment/examples/api100-inconclusive-follow-up-evidence-record.example.json`
- Create: `assessment/examples/api100-inconclusive-follow-up-assessment-result.example.json`
- Create: `assessment/follow-up/api100-inconclusive-follow-up.example.md`

- [ ] Reuse existing schema fields and identifier patterns. Make the event-trail gap the reason the attempted test is inconclusive, not proof of control failure.
- [ ] Keep the new result Draft with determination, design effectiveness, and operating effectiveness all `not_assessed`; include `scope_exclusion_rationale`, required rationale, limitations, and a distinct open finding.
- [ ] Cite the earlier `ASR-ENG3-API100` and `ASR-ENG4-API100-A3` results and their relevant findings in narrative text without editing those records.
- [ ] Run the focused regression test and assessment validator; correct any schema or cross-reference errors.

## Task 3: Add the governance handoff and integrate discovery

**Files:**
- Create: `templates/examples/governance-thread4.example.md`
- Modify: `assessment/integrated-assessment.example.md`
- Modify: `assessment/README.md`
- Modify: `assessment/workbook/README.md`
- Modify: `assessment/workbook/examples/README.md`
- Modify: `templates/README.md`

- [ ] Record one fictional owner, bounded evidence-capture action, risk-review decision, and explicit next review trigger. Do not record formal risk acceptance or close the assessment finding.
- [ ] Update the CAP-140 record flow to distinguish historical result, v0.19 narrow successful test, and this inconclusive follow-up.
- [ ] Add links from relevant overview and index pages, preserving explicit scope boundaries and nonclaims.
- [ ] Update the workbook examples index and other discovery pages to link to the new narrative and records.
- [ ] Run the focused assessment tests and `PYTHONDONTWRITEBYTECODE=1 python tools/validate_assessment.py --check`.

## Task 4: Validate and review the candidate

**Files:**
- Review: complete branch diff.

- [ ] Run `PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_validate_assessment -v`.
- [ ] Run `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`.
- [ ] Run `PYTHONDONTWRITEBYTECODE=1 python tools/validate_assessment.py --check`, applicable link validation, and the route selected by `python tools/plan_validation.py --base origin/main --candidate HEAD`.
- [ ] Run `git diff --check`, inspect the complete diff for traceability and nonclaim consistency, and obtain independent technical/editorial review on the exact candidate SHA.

## Commit sequence

1. `test: lock inconclusive follow-up record boundaries`
2. `docs: add bounded inconclusive assessment follow-up`

No tag or release status change is part of this implementation plan. Any future publication milestone requires its own approved scope and exact-candidate gates.
