# SOC 2 Mapping Evidence Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make SOC 2 feasibility and reviewer gates derive from a versioned, digest-pinned evidence manifest while preserving the current `HOLD` boundary.

**Architecture:** Keep the existing readiness matrix and renderer as the decision surface. Add a strict evidence-manifest format pinned by path and SHA-256 in the matrix; validate its evidence subject, allowed inputs, six-role B005 participant roster, and two exact-subject attestations before deriving feasibility and reviewer gate status. Leave the live manifest unevidenced and retain all existing source, rights, inventory, blocker, and nonclaim gates.

**Tech Stack:** Python standard library, JSON, `unittest`, GitHub Actions, repository validation planner and shard runner.

---

## File map

- Modify `tests/test_render_soc2_aicpa_tsc_mapping_go_no_go.py` with synthetic evidence fixtures and fail-closed tests.
- Modify `tools/render_soc2_aicpa_tsc_mapping_go_no_go.py` to validate the manifest, bind evidence to its assessed input set, and derive feasibility/reviewer gates.
- Create `docs/superpowers/specs/2026-10-05-soc2-aicpa-tsc-evidence-manifest.json` as a production `not_evidenced` record containing no source-derived or invented evidence.
- Modify `docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-mapping-readiness-matrix.json` to remove the boolean feasibility authority and pin the manifest digest.
- Regenerate `docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-mapping-go-no-go-review.md` with the same derived `HOLD` status and a concise manifest evidence reference.
- Modify `tools/plan_validation.py`, `tools/README.md`, `.github/workflows/catalog-validation.yml`, and `tools/test-shards.json` only if the new manifest or new test module needs explicit catalog, routing, workflow, documentation, or shard registration.
- Do not modify `crosswalks/catalog.json`, `crosswalks/mappings/`, `crosswalks/registry/`, the source oracle, or the rights review.

## Task 1: Specify synthetic evidence fixtures and assertions

**Files:**
- Modify: `tests/test_render_soc2_aicpa_tsc_mapping_go_no_go.py`
- Test: `tests/test_render_soc2_aicpa_tsc_mapping_go_no_go.py`

- [ ] **Step 1: Add a synthetic manifest fixture builder.** Build temporary repository files for an oracle, inventory/probe inputs, a matrix, and a manifest. The helper shall compute real file SHA-256 values and the evidence-subject digest using the design's canonical serialization.
- [ ] **Step 2: Add passing schema tests.** Cover a complete `not_evidenced` live-shaped manifest that remains `HOLD`, and a fully evidenced synthetic manifest whose evidence subject, six B005 participants, and two distinct review roles validate. Negative cases shall omit or duplicate required participant roles, mismatch mapper identity, remove mapper experience or owner approval, and mismatch an attestation identity from its rostered review role. The valid unevidenced state explicitly records `feasibility.status: "not_evidenced"`, `review.status: "not_completed"`, explanatory rationales, empty evidence inputs, participant roster and attestations, and blocker IDs that match the matrix's existing semantic-feasibility and reviewer-readiness blockers.
- [ ] **Step 3: Add failing digest and path tests.** Assert failure for changed input bytes, stale matrix-pinned manifest digest, malformed digest, duplicate normalized input paths, paths outside the repository, and forbidden matrix/manifest/generated-review dependencies.
- [ ] **Step 4: Add failing reviewer contract tests.** Assert failure for missing or duplicate roles, same reviewer identity across roles where independence is required, mapper self-review, absent qualification/access/independence/conflict disposition, stale evidence-subject digest, unsupported disposition, and open Critical or Important findings.
- [ ] **Step 5: Add failing decision tests.** Assert that matrix labels cannot override absent feasibility or reviewer evidence; no `GO` is derived with current source, rights, or inventory evidence; `HOLD` and `NO_GO` retain existing blocker rules; and a synthetic all-positive evidence case derives `GO` only when every existing prerequisite passes.
- [ ] **Step 6: Run the focused tests and confirm the new contract tests fail for the expected missing behavior.**

Run: `python -m unittest tests.test_render_soc2_aicpa_tsc_mapping_go_no_go -v`

Expected: existing readiness tests pass; new manifest-contract tests fail because manifest validation and digest-bound derivation are not implemented.

## Task 2: Implement manifest validation and evidence-derived gates

**Files:**
- Modify: `tools/render_soc2_aicpa_tsc_mapping_go_no_go.py`
- Test: `tests/test_render_soc2_aicpa_tsc_mapping_go_no_go.py`

- [ ] **Step 1: Add strict manifest constants and schema validation.** Define exact keys, schema version, feasibility states (`not_evidenced`, `positive`), review states (`not_completed`, `complete`), required reviewer roles, and permitted evidence-input categories. `not_evidenced` plus `not_completed` is a complete, valid negative record only when both have nonempty rationales, empty evidence/attestation arrays, and blocker IDs that exactly match the corresponding blocked matrix gates. Reject unknown keys and unsupported enum values; missing required fields are validation errors.
- [ ] **Step 2: Implement canonical evidence-subject digest calculation.** Serialize the substantive feasibility payload, normalized path/digest pairs, and sorted participant roster as UTF-8 JSON with sorted keys and compact separators; exclude review attestations, then calculate SHA-256. Compare every attestation's subject digest to this value.
- [ ] **Step 3: Implement safe input-path validation.** Require repository-relative POSIX paths, reject absolute paths, `.`/`..`, duplicate normalized paths, symlinks escaping the repository, matrix/manifest/generated-review paths, and paths outside the declared input-category allowlists. Verify each repository input's digest before consuming its content.
- [ ] **Step 4: Validate B005 people and attestations.** When `review.status` is `complete`, require six distinct people for mapper, AICPA TSC subject matter, ESAF specification/mapping, publication rights, security/overclaiming, and owner-authorized approver; validate role-specific qualifications, qualification/access evidence references, independence, conflict disposition, owner approval evidence, mapper identity, and mapper experience. Evidence references shall be either repository files with verified SHA-256 or HTTPS URIs with declared SHA-256 for external exact-SHA review; reject symbolic placeholders, credential-bearing URLs, and token query strings. Require two distinct exact-subject attestations whose identities match the rostered specification and security roles, valid dates/dispositions, and zero open Critical/Important findings. When `review.status` is `not_completed`, require empty participant and attestation arrays and exact blocker coverage as defined in Step 1.
- [ ] **Step 5: Integrate matrix pinning.** Replace `mapping_contract.positive_feasibility_probe` as decision authority with an exact `{path, sha256}` evidence-manifest reference. Verify the path is the canonical SOC 2 manifest and its bytes match the matrix digest. Keep the static reviewer requirements closed and structured if needed for renderer comparison.
- [ ] **Step 6: Derive feasibility and reviewer gate state from the manifest.** A valid `not_evidenced`/`not_completed` record keeps the corresponding matrix gates blocked and must reference their complete reconsiderable blockers. A positive feasibility record and both qualifying attestations are necessary but not sufficient for `GO`; existing oracle retrieval, rights `PASS`, inventory digest, blocker, finding, and overclaiming checks remain required.
- [ ] **Step 7: Add focused tests for every validation helper and decision branch.** Run the focused test module and make every new test pass.

Run: `python -m unittest tests.test_render_soc2_aicpa_tsc_mapping_go_no_go -v`

Expected: all focused SOC 2 renderer tests pass, including synthetic all-positive mechanics and current live `HOLD` derivation.

## Task 3: Pin the live unevidenced manifest and regenerate the review

**Files:**
- Create: `docs/superpowers/specs/2026-10-05-soc2-aicpa-tsc-evidence-manifest.json`
- Modify: `docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-mapping-readiness-matrix.json`
- Regenerate: `docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-mapping-go-no-go-review.md`
- Test: `tests/test_render_soc2_aicpa_tsc_mapping_go_no_go.py`

- [ ] **Step 1: Create the production manifest in the valid unevidenced state.** Record feasibility as `not_evidenced`, reviews as `not_completed`, include rationales and the matching existing blocker IDs, and use empty evidence-input, participant, and attestation arrays. Do not omit schema-required fields or present the state as a validator error. Add no AICPA-derived content, identifiers, counts, or synthetic results.
- [ ] **Step 2: Pin the manifest's exact path and SHA-256 in the matrix.** Remove the old boolean feasibility property and ensure no matrix field can override manifest state.
- [ ] **Step 3: Regenerate the readiness Markdown with the renderer.** Render only summary status and digests; do not print restricted or synthetic fixture details.
- [ ] **Step 4: Assert the live matrix still derives `HOLD`.** Assert all existing readiness blockers remain intact and no `GO` can be derived while source access, publication rights, inventory, or people gates are blocked.
- [ ] **Step 5: Run renderer check mode and focused tests.**

Run: `python tools/render_soc2_aicpa_tsc_mapping_go_no_go.py --check`

Expected: exit 0; generated review is current and reports `HOLD`.

## Task 4: Wire repository validation and shard metadata

**Files:**
- Modify if required: `tools/plan_validation.py`
- Modify if required: `.github/workflows/catalog-validation.yml`
- Modify if required: `tools/README.md`
- Modify if required: `tools/test-shards.json`
- Test: `tests/test_plan_validation.py` if planner routing changes

- [ ] **Step 1: Check existing renderer routing and CI invocation.** Retain existing checks where they already cover the new manifest through the renderer; add manifest path routing only if the planner currently classifies it outside the publication tier.
- [ ] **Step 2: Check test-shard registration.** Keep the existing SOC 2 test module registered; update its shard only if the new test module is split or the current module's shard membership needs modification.
- [ ] **Step 3: Update documentation only if the invocation or evidence contract changes the documented command.** Preserve concise tool usage documentation.
- [ ] **Step 4: Run planner and shard-manifest focused tests if wiring changes.**

Run: `python tools/plan_validation.py --base origin/main --candidate HEAD`

Expected: the changed manifest, matrix, renderer, generated review, and tests receive the publication validation route; no weaker route is selected.

## Task 5: Review the exact candidate and validate publication boundaries

**Files:**
- Review the complete branch diff and every changed file.
- No unrelated source, mapping, or catalog files.

- [ ] **Step 1: Run focused SOC 2 tests and renderer check.**
- [ ] **Step 2: Run `python -m unittest discover -s tests -v` and the planner-selected route.** Apply repository-prescribed local Git signing overrides only to test subprocesses if fixture commits make the run impractically slow.
- [ ] **Step 3: Run applicable crosswalk, assessment, controls, architecture, Markdown/link, test-shard, and qualified-review validators selected by changed paths.**
- [ ] **Step 4: Verify catalog populations and no mapping/registry files changed.** Compare catalog counts to `origin/main`; confirm there are no source-derived SOC 2 records.
- [ ] **Step 5: Have independent specification/inventory and security/overclaiming reviewers review the exact candidate SHA.** Record no attribution trailers or tooling attribution in commits, pull request text, or review comments. Redispatch both reviewers if the candidate changes.
- [ ] **Step 6: Run `git diff --check origin/main...HEAD`, confirm clean tracked state and no `__pycache__`, and capture the exact reviewed head SHA and gate results.**
- [ ] **Step 7: Fetch `origin/main`; if it advanced, integrate it and rerun affected validation and both exact-head reviews.**
- [ ] **Step 8: Open a reviewable pull request only after validation and exact-SHA reviews are complete. Merge only after all required hosted checks pass and the merge state is clean.**
- [ ] **Step 9: After merge, update local `main`, rerun the renderer and candidate-bound checks on the merge commit, verify clean state, and remove the temporary branch/worktree.**

## Acceptance criteria

- The live SOC 2 readiness decision remains `HOLD` and its published review is deterministic and current.
- The matrix cannot claim feasibility or reviewer readiness without a valid, matrix-pinned manifest.
- Stale inputs, stale manifests, invalid paths, dependency cycles, missing roles, contradictory reviewer identities, and unresolved major findings fail closed.
- Synthetic all-positive fixtures demonstrate that the renderer can derive `GO` only when every independent existing readiness gate also passes.
- No AICPA source-derived content, inventory, mappings, registry records, or catalog changes are introduced.
- All required repository checks pass on the exact PR head and merged `main` commit, with no coauthor or tooling attribution added.
