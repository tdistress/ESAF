# UK Cyber Essentials Plus v3.2 External-to-ESAF Mapping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, machine-valid, draft ESAF-1600 reverse-evidence mapping from all 144 pinned Cyber Essentials Plus v3.2 provisions to exact ESAF 0.4-alpha requirements.

**Architecture:** Create an independent `0.2.0` snapshot beside forward `0.1.0`, using the existing `external_to_esaf` schema direction. Provision-first authoring records bounded evidence relationships or specific negatives; deterministic artifacts and independent reviews prevent assessment artifacts from being represented as control implementation.

**Tech Stack:** Markdown with JSON/YAML front matter, JSON Schema 2020-12, Python 3, PyYAML, jsonschema, `unittest`, Git, and existing `tools.crosswalks` modules.

## Global Constraints

- ID: `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`; root: `crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0/`.
- Use all 144 locked oracle provisions in oracle order: M=24, T1=16, S=11, T2=9, T3=37, T4=9, T5=7, C=13, A=4, B=14.
- Every positive is `external_to_esaf`, resolves exact manifest provenance, and has ordered conditions: actor, scope, population, sample, assessment_date, evidence_date, tool, provenance, exception, delivery_partner_discretion, point_in_time_status.
- Condition status is `SATISFIED` or `NOT_APPLICABLE`, with nonempty evidence references; conditions only narrow an already-supported claim.
- A positive is bounded evaluator evidence, never implementation, effectiveness, sufficiency, compliance, certification, equivalence, continuous assurance, or population/current-scheme coverage.
- Procedures, files, retention, tools, samples, scores, decisions, and certification remain negative unless they independently yield a defined observation/result and exact ESAF outcome.
- Use approved original paraphrases only. No copied source, private Delivery Partner material, core v3.3/current-scheme material, downloads, caches, or scratch files. All records stay `draft`.

### Task 1: Commit reverse mapping rights and contract tests

**Files:** Create `tests/test_uk_cyber_essentials_plus_v32_external_to_esaf_mapping.py`; create `docs/superpowers/reviews/2026-07-19-uk-cyber-essentials-plus-v3.2-external-to-esaf-mapping-rights-attestation.md`.

- [ ] **Step 1: Write failing tests** for the exact ID/root/oracle, rights reviewer distinction, and an attestation containing `direction: external_to_esaf`, `authorized_source_access: true`, and `disposition: approved`.
- [ ] **Step 2: Run** `python -m unittest tests.test_uk_cyber_essentials_plus_v32_external_to_esaf_mapping -v`; expect failure because the attestation does not exist.
- [ ] **Step 3: Add the attestation** binding NCSC/Crown and OGL v3.0, both PDF digests, oracle digest, feasibility rights commit `4207e1c1e8ff9f743274ebb4b626210cca053458`, allowed field classes, copied-text prohibition, IASME partition, source-version boundary, and unconditional approval.
- [ ] **Step 4: Rerun and commit:** `git add -- tests/test_uk_cyber_essentials_plus_v32_external_to_esaf_mapping.py docs/superpowers/reviews/2026-07-19-uk-cyber-essentials-plus-v3.2-external-to-esaf-mapping-rights-attestation.md && git commit -m "Approve CE Plus reverse mapping rights"`.

### Task 2: Scaffold snapshot and fail-closed contract

**Files:** Modify the focused test; create snapshot `README.md`, `PROVISION_INVENTORY.md`, `ESAF_CONTROL_MANIFEST.json`, lifecycle registry `crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0.md`; modify catalogs.

- [ ] **Step 1: Write failing scaffold tests** for draft state, 144 ordered inventory rows, group counts, deterministic manifest from pinned ESAF commit, empty lifecycle events, and zero records.
- [ ] **Step 2: Add mutations** for wrong direction, missing/reordered conditions, empty evidence references, unjustified NA, missing manifest digest/path/locator, duplicate legs, generic negatives, and condition-created outcomes.
- [ ] **Step 3: Implement minimal scaffold,** render inventory from oracle order, generate manifest with `build_control_manifest`, refresh lifecycle digest, and run `python tools/validate_crosswalks.py --write`.
- [ ] **Step 4: Verify** focused/schema/validator tests, `validate_crosswalks.py --check`, and commit `Scaffold CE Plus reverse mapping`.

### Task 3: Author M, T1, and S records

**Files:** Modify focused test; create 24 `cepts32-m-*.md`, 16 `cepts32-t1-*.md`, 11 `cepts32-s-*.md`; modify lifecycle/catalogs.

- [ ] **Step 1: Write failing batch tests** with record loader, positive-condition assertion, specific `Missing outcome:` negative assertion, and manifest-resolution assertion.
- [ ] **Step 2: Confirm failure, then author provision-first.** Default to negative; positives name exact observed state, exact ESAF requirement, and all 11 conditions.
- [ ] **Step 3: Refresh digest/catalogs, run focused and crosswalk checks, inspect `git diff --check`, and commit** `Map CE Plus reverse scope and selection evidence`.

### Task 4: Author T2, T3, and T4 configuration records

**Files:** Modify focused test; create 9 T2, 37 T3, and 9 T4 records; modify lifecycle/catalogs.

- [ ] **Step 1: Write failing tests** proving a tool name alone, sample without population boundary, and date-free observation cannot be positive.
- [ ] **Step 2: Author records** with exact observation/result, requirement, scope/population/sample, date/tool/provenance, and point-in-time boundary; recommendations remain negative.
- [ ] **Step 3: Regenerate, validate, inspect, and commit** `Map CE Plus reverse configuration evidence`.

### Task 5: Reassess T5 and author C, A, B

**Files:** Modify focused test; create 7 T5, 13 C, 4 A, and 14 B records; modify lifecycle/catalogs.

- [ ] **Step 1: Write failing adversarial tests** proving T5-006 is not copied feasibility text and that discretion, aggregate decisions, scanner authorization, file supply, and retention cannot become positives.
- [ ] **Step 2: Author and independently reassess all T5 records.** Keep C/A/B negative unless their own observation/result—not administrative role—supports exact ESAF outcome.
- [ ] **Step 3: Regenerate, validate, inspect, and commit** `Complete CE Plus reverse evidence inventory`.

### Task 6: Reconcile, review, and publish draft metadata

**Files:** Modify focused test, snapshot README, lifecycle, catalogs, `crosswalks/uk-cyber-essentials.md`, and `project/BACKLOG.md`; create traceability, specification, and overclaiming reviews dated 2026-07-19.

- [ ] **Step 1: Write whole-snapshot failing tests** for 144 records, all derived counts, reverse-only legs, condition completeness, negative specificity, current catalogs/navigation, and prohibited assurance language.
- [ ] **Step 2: Reconcile** boilerplate, taxonomy drift, unsupported adjacency, condition-created support, copied-source windows, stale manifests, and contradictions; add regression tests before each material correction.
- [ ] **Step 3: Update narrative using derived totals only,** retain draft/point-in-time boundaries, and remove only the completed design backlog item.
- [ ] **Step 4: Dispatch independent exact-SHA specification/inventory and security/overclaiming reviews.** Resolve Critical/Important findings with regressions; redispatch both reviews after every candidate change.
- [ ] **Step 5: Run final gates:** focused suite, full `python -m unittest discover -s tests -v`, controls, architectures, migration, baseline crosswalk, links, whole-branch diff check, and clean status. Commit reviews as `Review CE Plus reverse mapping draft`, then push and open a PR recording the reviewed SHA and actual gate results. Do not promote lifecycle beyond draft.

## Plan self-review

- **Spec coverage:** Tasks 1–2 establish rights, identity, inventory, lifecycle, manifest, and strict conditions. Tasks 3–5 implement complete provision-first authoring and adversarial limits. Task 6 reconciles, independently reviews, and validates the final draft.
- **Placeholder scan:** No TBD/TODO markers or unspecified validation steps remain; analytical outcomes are intentionally not pre-decided.
- **Type consistency:** Every task uses snapshot version `0.2.0`, the same mapping-set ID, locked oracle, manifest, and 11-condition contract.
