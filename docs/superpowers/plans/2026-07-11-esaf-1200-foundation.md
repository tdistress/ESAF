# ESAF-1200 Reference Architecture Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish and automatically validate the vendor-neutral ESAF-1200 architecture method, trust-zone model, pattern contract, registry, selection process, overlays, and decision records.

**Architecture:** ESAF-1200 is decomposed into focused Markdown sources with a deterministic Python validator. The validator checks the stable structural contract and links while leaving architectural judgment to technical review. Existing control-catalog validation remains independent and runs alongside architecture validation in CI.

**Tech Stack:** Markdown, Python 3.13 standard library, GitHub Actions, Git.

## Global Constraints

- Markdown remains the authoritative source.
- ESAF-1200 remains vendor-neutral and does not duplicate ESAF-1100 control requirements.
- Pattern identifiers use `ARC-P###` in increments of ten and are never reassigned after publication.
- The foundation reserves ARC-P100 through ARC-P160.
- Architecture views use logical trust zones and do not prescribe network topology.
- The architecture validator may inspect structure and links but may not infer diagram semantics.

---

### Task 1: Foundation validation contract

**Files:**
- Create: `tests/test_validate_architectures.py`
- Create: `tools/validate_architectures.py`

**Interfaces:**
- Consumes: repository root and authoritative files under `architectures/`
- Produces: `validate(root: Path) -> list[str]` and CLI exit status 0 for valid architecture sources, 1 for validation errors

- [ ] **Step 1: Write failing unit tests**

Create isolated temporary repositories that demonstrate missing required files, duplicate pattern identifiers, missing template sections, broken local links, and a valid minimal foundation.

- [ ] **Step 2: Verify the tests fail because the module is absent**

Run: `python -m unittest tests.test_validate_architectures -v`

Expected: FAIL because `tools.validate_architectures` cannot be imported.

- [ ] **Step 3: Implement the minimal validator**

Implement constants for required foundation files, reserved pattern identifiers, required template headings, permitted pattern states, control-family prefixes, placeholder markers, and Markdown link resolution. Return deterministic error messages and expose `main()`.

- [ ] **Step 4: Verify the validator tests pass**

Run: `python -m unittest tests.test_validate_architectures -v`

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```shell
git add tests/test_validate_architectures.py tools/validate_architectures.py
git commit -m "Add architecture foundation validator"
```

### Task 2: Normative architecture foundation

**Files:**
- Modify: `architectures/README.md`
- Create: `architectures/ESAF-1200.md`
- Create: `architectures/PRINCIPLES.md`
- Create: `architectures/TRUST_ZONES.md`
- Create: `architectures/PATTERN_SELECTION.md`

**Interfaces:**
- Consumes: ESAF-1000 requirements, ESAF-1100 control families, and the approved design
- Produces: normative architecture method, ten architecture principles, eight trust zones, and pattern-selection procedure

- [ ] **Step 1: Run the validator against the incomplete foundation**

Run: `python tools/validate_architectures.py`

Expected: FAIL listing missing foundation files.

- [ ] **Step 2: Author ESAF-1200 and supporting normative sources**

Define purpose, scope, relationship to other ESAF publications, architecture governance, views, pattern conformance, principles, trust zones, boundary crossings, selection inputs, tailoring, inherited controls, and exceptions.

- [ ] **Step 3: Run structural and control validation**

Run: `python tools/validate_architectures.py` and `python tools/validate_controls.py --check`

Expected: architecture validation may still report files intentionally deferred to Task 3; control validation PASS.

- [ ] **Step 4: Commit**

```shell
git add architectures/README.md architectures/ESAF-1200.md architectures/PRINCIPLES.md architectures/TRUST_ZONES.md architectures/PATTERN_SELECTION.md
git commit -m "Define ESAF-1200 architecture method"
```

### Task 3: Pattern and decision contracts

**Files:**
- Create: `architectures/ARCHITECTURE_TEMPLATE.md`
- Create: `architectures/patterns/README.md`
- Create: `architectures/overlays/README.md`
- Create: `architectures/decisions/README.md`
- Create: `architectures/decisions/ADR_TEMPLATE.md`

**Interfaces:**
- Consumes: pattern contract, reserved identifiers, selection method, and trust zones
- Produces: authoring template, seven-entry pattern registry, overlay method, and ADR process

- [ ] **Step 1: Author the pattern template and registries**

Include every required template heading, reserve ARC-P100 through ARC-P160 exactly once, define pattern states, document overlays, and provide the ADR record.

- [ ] **Step 2: Run architecture validation**

Run: `python tools/validate_architectures.py`

Expected: PASS with seven reserved patterns and all required foundation files.

- [ ] **Step 3: Run all unit and control checks**

Run: `python -m unittest discover -s tests -v` and `python tools/validate_controls.py --check`

Expected: all tests and catalog checks PASS.

- [ ] **Step 4: Commit**

```shell
git add architectures/ARCHITECTURE_TEMPLATE.md architectures/patterns architectures/overlays architectures/decisions
git commit -m "Add architecture pattern contracts"
```

### Task 4: Continuous integration and release metadata

**Files:**
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tools/README.md`
- Modify: `ROADMAP.md`
- Modify: `project/BACKLOG.md`
- Modify: `project/DECISION_LOG.md`
- Modify: `CHANGELOG.md`
- Modify: `VERSION.md`

**Interfaces:**
- Consumes: both repository validators and Phase 3 release requirements
- Produces: CI enforcement and 0.4-alpha release-state metadata

- [ ] **Step 1: Extend CI and tooling documentation**

Rename the workflow and job to repository validation, add architecture and test paths to triggers, and run unit tests, architecture validation, and control validation as separate steps.

- [ ] **Step 2: Update project metadata**

Record DEC-0011 for the architecture method, mark the foundation initiative complete, set the current version to 0.4-alpha, and describe the next pattern tranche.

- [ ] **Step 3: Run final verification**

Run:

```shell
python -m unittest discover -s tests -v
python tools/validate_architectures.py
python tools/validate_controls.py --check
git diff --check
```

Expected: every command exits 0 with no failures.

- [ ] **Step 4: Commit and publish**

```shell
git add .github/workflows/catalog-validation.yml tools/README.md ROADMAP.md project/BACKLOG.md project/DECISION_LOG.md CHANGELOG.md VERSION.md docs/superpowers
git commit -m "Complete ESAF-1200 architecture foundation"
git push
```

- [ ] **Step 5: Complete PR #13**

Mark PR #13 ready for review, update its title and body to describe the implemented milestone, wait for required checks, then merge and delete the branch. Confirm the post-merge `main` workflow succeeds.
