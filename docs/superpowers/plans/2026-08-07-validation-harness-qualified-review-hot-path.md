# Validation harness qualified-review hot path implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move 28 qualified-review policy cases onto ordered pure production boundaries while retaining exact full-validator equivalence, current failure order, complete acquisition coverage, and an auditable proof before migration.

**Architecture:** A frozen inventory will own the 28 selected cases, the 43-method baseline ledger, and a reviewed digest. Ordered policy functions will replace decisions inside the existing role and Draft-reference wrappers without moving I/O. A clean Stage 1 commit will prove full, narrow, and expected equivalence before a later Stage 2 commit changes only selected test call sites and a proof receipt.

**Tech Stack:** Python 3.13, `unittest`, frozen `dataclasses`, `hashlib`, canonical UTF-8 JSON, `argparse`, `unittest.mock`, Git CLI, GitHub CLI, and PowerShell.

## Global constraints

- Implement tasks sequentially. Do not assign overlapping inventory, validator, proof-support, verifier, or migration edits to parallel implementers.
- The approved design commit is `56afd512465a3670c378406d53812487919f6c87`. Bind proof and review evidence to the actual full lowercase 40-character candidate `HEAD`, not to this design SHA or an abbreviated SHA.
- Preserve exactly 28 selected cases across 15 methods: 24 role/readiness cases across 14 methods and four Draft-reference cases in one method.
- Preserve the baseline accounting: 43 tests, 92 detailed-validation entries, 31 selected entries, 61 retained entries, and 108 expanded `copytree` operations. Copy counts are diagnostic. Detail-entry counts and selected case counts are normative.
- Keep the whitespace-only qualification case and both accepted high-severity cases on the complete path. Campaign schema validation owns their first failure. Direct pure-policy tests retain those inputs as intentional defense-in-depth checks outside equivalence.
- Keep accepted-Minor missing-field cases on the full path because they fail schema validation. Keep missing roles in schema validation and duplicate roles or mapping-set identifiers in `_mapping_entries()`.
- Keep candidate acquisition, role-file parsing and binding, source sets, immutable locators, digests, allowlists, archives, seals, CLI behavior, operational errors, and path defenses on the complete path.
- Preserve current first-failure order. Reviewer eligibility stays before each reviewer's role-file binding. Role findings and conclusions stay after that binding. The distinct-candidate reference check stays before Draft recursion. Archive equality stays between manifest-reference and seal-reference checks.
- The alternate-commit description and duplicate-finding cases shall retain their exact candidate facts. Do not reduce them to the ordinary Draft baseline.
- Do not add or widen a process-global, cross-call, path, fixture, mtime, candidate, snapshot, Draft, archive, or seal cache.
- Do not add elapsed-time assertions. Timings remain diagnostic.
- Keep `tools/test-shards.json` and `.github/workflows/catalog-validation.yml` unchanged unless a separate, reviewed completeness defect requires a new design.
- Set `PYTHONDONTWRITEBYTECODE=1` for Python validation. Before an exact-SHA proof, verify a clean worktree and no `__pycache__` directory or build output.
- A change to a proof-critical artifact after Stage 1 invalidates that proof. Restore the selected complete calls, commit the corrected Stage 1 surface, rerun the clean proof, then migrate in a later commit.
- Stage 2 may modify only `tests/test_validate_qualified_review_evidence.py` at selected call sites, its grouping and structural guards, plus the new proof receipt. It shall not modify the inventory, production validator, proof-support module, or verifier.
- Issue 55 stays open. Do not change real campaign evidence, mapping-set state, release status, normative ESAF text, or publication claims.
- Use the humanizer skill in embedded mode for the proof receipt, review summaries, commit messages, and pull-request prose. Those texts shall contain no em dash or en dash.

## File map

- Create `tests/qualified_review_policy_cases.py`: immutable case records, the exact 43-method ledger, canonical digest calculation, strict validation, and the only selected population.
- Create `tests/qualified_review_hot_path_support.py`: deterministic full-fixture reconstruction, immutable narrow-input reconstruction, declarative mutation application, and report projection shared by the test module and verifier.
- Modify `tests/test_validate_qualified_review_evidence.py`: inventory tests, boundary tests, routing tests, verifier tests, retained full-path integrations, final fast matrices, and structural migration guards.
- Modify `tools/validate_qualified_review_evidence.py`: immutable policy types, ordered role/readiness operations, ordered Draft-reference operations, combined narrow adapters, and production wrapper routing.
- Create `tools/verify_qualified_review_hot_path_equivalence.py`: opt-in clean-candidate comparison of full, narrow, and expected results for all 28 cases.
- Create during Stage 2 `docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md`: the clean Stage 1 SHA, inventory digest, exact output, and proof-critical file hashes.
- Review without editing `docs/superpowers/specs/2026-08-07-validation-harness-qualified-review-hot-path-design.md`.
- Verify without editing `tools/test-shards.json`, `.github/workflows/catalog-validation.yml`, and the real qualified-review evidence trees.

## Exact baseline ledger

The ledger below is derived from static control flow at baseline commit `f99e403583877f803576dcad919025e558e5a5f6`. A Final call counts its outer detail entry and any recursive Draft entry reached by that case. Every `CampaignValidationTests` method includes one setup copy. The copy column also expands literal mutation loops and each two-copy `_final_inputs()` call.

| Test method | Detail entries | Selected entries | Retained entries | Expanded copies |
|---|---:|---:|---:|---:|
| `test_linux_acquisition_rejects_swap_restored_before_revalidation` | 0 | 0 | 0 | 0 |
| `test_valid_draft_campaign_is_transition_ready` | 1 | 0 | 1 | 1 |
| `test_rejects_missing_duplicate_and_mismatched_role_keys` | 3 | 0 | 3 | 4 |
| `test_rejects_ineligible_reviewer_evidence` | 5 | 5 | 0 | 6 |
| `test_actor_aliases_and_shared_locator_cannot_bypass_role_rules` | 4 | 4 | 0 | 5 |
| `test_actor_alias_cannot_bypass_mapper_independence` | 1 | 1 | 0 | 1 |
| `test_sha_locators_bind_package_attestation_and_worksheet_bytes` | 3 | 0 | 3 | 4 |
| `test_attestation_source_sets_are_exactly_candidate_bound` | 6 | 0 | 6 | 7 |
| `test_explicitly_resolved_conflict_is_eligible` | 1 | 1 | 0 | 1 |
| `test_duplicate_human_requires_dual_acceptance_and_both_qualifications` | 2 | 1 | 1 | 3 |
| `test_stop_with_open_high_severity_is_valid_but_not_ready` | 2 | 2 | 0 | 3 |
| `test_accepted_critical_or_important_is_evidence_invalid` | 2 | 0 | 2 | 3 |
| `test_accepted_minor_requires_named_acceptance_evidence` | 3 | 0 | 3 | 4 |
| `test_pass_rejects_open_findings` | 1 | 1 | 0 | 1 |
| `test_pass_after_correction_binds_exact_campaign_candidate` | 2 | 2 | 0 | 2 |
| `test_orphan_affected_record_identifier_is_invalid_even_for_stop` | 1 | 1 | 0 | 1 |
| `test_ready_findings_must_equal_authoritative_candidate_findings` | 1 | 1 | 0 | 1 |
| `test_ready_findings_bind_authoritative_description` | 1 | 1 | 0 | 1 |
| `test_duplicate_authoritative_finding_identifiers_are_invalid` | 1 | 1 | 0 | 1 |
| `test_campaign_tree_and_package_bytes_are_exact` | 3 | 0 | 3 | 4 |
| `test_candidate_schema_cannot_retrieve_external_references` | 1 | 0 | 1 | 1 |
| `test_valid_final_campaign_is_recursively_merge_ready` | 2 | 0 | 2 | 3 |
| `test_invalid_report_preserves_parsed_final_campaign_context` | 1 | 0 | 1 | 3 |
| `test_final_campaign_requires_all_preserved_draft_inputs` | 3 | 0 | 3 | 3 |
| `test_final_campaign_binds_every_draft_reference_field` | 7 | 7 | 0 | 9 |
| `test_final_campaign_rejects_archive_seal_or_draft_byte_mutation` | 8 | 0 | 8 | 9 |
| `test_retained_draft_revalidation_rejects_mismatched_archive_urn` | 2 | 0 | 2 | 3 |
| `test_reviewed_candidate_requires_exact_nested_reviewer_objects` | 2 | 2 | 0 | 5 |
| `test_final_pass_after_correction_binds_reviewed_candidate` | 1 | 1 | 0 | 3 |
| `test_validator_cli_emits_canonical_reports_and_exit_codes` | 2 | 0 | 2 | 1 |
| `test_validator_cli_requires_check_and_all_or_none_draft_inputs` | 0 | 0 | 0 | 1 |
| `test_validator_cli_sanitizes_missing_and_permission_failures` | 2 | 0 | 2 | 1 |
| `test_validator_cli_classifies_preopen_permissions_as_operational` | 4 | 0 | 4 | 1 |
| `test_clis_sanitize_git_operational_failures` | 2 | 0 | 2 | 1 |
| `test_validator_cli_keeps_batch_object_failure_operational` | 1 | 0 | 1 | 1 |
| `test_seal_cli_atomically_publishes_exact_archive_and_seal` | 1 | 0 | 1 | 1 |
| `test_seal_cli_accepts_only_the_real_archive_digest_urn` | 2 | 0 | 2 | 1 |
| `test_seal_cli_refuses_invalid_or_nonready_campaign` | 2 | 0 | 2 | 3 |
| `test_seal_cli_refuses_existing_worktree_and_unsafe_destinations` | 0 | 0 | 0 | 1 |
| `test_seal_cli_publishes_nothing_after_execution_state_drift` | 1 | 0 | 1 | 1 |
| `test_seal_cli_preserves_competing_output_and_cleans_partial_staging` | 2 | 0 | 2 | 1 |
| `test_seal_fails_closed_when_parent_or_ancestor_is_swapped` | 2 | 0 | 2 | 1 |
| `test_seal_archives_the_exact_validated_byte_snapshot` | 1 | 0 | 1 | 1 |
| **Total** | **92** | **31** | **61** | **108** |

The retained-method AST oracle uses `ast.dump(method_node, annotate_fields=True, include_attributes=False)` encoded as UTF-8 and hashed with SHA-256. These values bind all 28 baseline methods outside the selected migration, including the three zero-entry security and argument guards:

| Retained method | AST SHA-256 |
|---|---|
| `test_accepted_critical_or_important_is_evidence_invalid` | `8bbbac1520f72932847f347658414654092f2deacbfcc93e37be0de833c6e587` |
| `test_accepted_minor_requires_named_acceptance_evidence` | `23319dd12547114b869fd0815418669c3869e7824e0da17b95b64f76509370b3` |
| `test_attestation_source_sets_are_exactly_candidate_bound` | `7ca3e58598557954724bc325eba4eefe154875151a9d3cf23246b6f24912be24` |
| `test_campaign_tree_and_package_bytes_are_exact` | `c750637c9db1cc6caa16c702b52eec3cae96cfd7cae471977e19a1895f8eecd4` |
| `test_candidate_schema_cannot_retrieve_external_references` | `e9209852b86444d64e0ba63f072353d0be18ad400313450760b903ded8f2ad95` |
| `test_clis_sanitize_git_operational_failures` | `697fa1a28fd0aed65935fdb639543ca966fc85f925b4031e46328c358e96d515` |
| `test_final_campaign_rejects_archive_seal_or_draft_byte_mutation` | `ace8500c85285ccdfe1551710bfdb48a033152010a0342853e2c5db0d60e7c38` |
| `test_final_campaign_requires_all_preserved_draft_inputs` | `dcaf9d0c09653f67b2e12fc700572282349ba9047168d9d9485381ce204d5a2d` |
| `test_invalid_report_preserves_parsed_final_campaign_context` | `285d29a598e49cbfa0f2573f291bbb643f6c685015d2ba6dd148bcafe76d5668` |
| `test_linux_acquisition_rejects_swap_restored_before_revalidation` | `6fb410df11aac17c7c17ec481b061ea0fc92db575b64625713f5af3ab86228db` |
| `test_rejects_missing_duplicate_and_mismatched_role_keys` | `9ee266cb597041d94487abe486f455ab9effe02b339644601932a5c1304a438e` |
| `test_retained_draft_revalidation_rejects_mismatched_archive_urn` | `276c95fd1102d68ecb6a71c3491f2d0224e67bfca6585c95e8add385eef99261` |
| `test_seal_archives_the_exact_validated_byte_snapshot` | `ebbc068dcddf2e0ce61a237acb9522c5b0d7863d1e71f4c2668e18d4fe7b6975` |
| `test_seal_cli_accepts_only_the_real_archive_digest_urn` | `6e8dc8eaa4c6322657a6b80447a51f33353e1bfeb0be7dfde9ece5437f20139f` |
| `test_seal_cli_atomically_publishes_exact_archive_and_seal` | `6952f8478e7bc5a3930337c5ebfd36522e1ab7524e51987f24d18de7241b9563` |
| `test_seal_cli_preserves_competing_output_and_cleans_partial_staging` | `6591b5e3411be8eff4d3cd5011c07ce120eba18ec5470326e1ebdf613bcffe9a` |
| `test_seal_cli_publishes_nothing_after_execution_state_drift` | `ae58a0567c69c7f11ac4b18586f4105198f678ea1038542071dc64b0e02bc49c` |
| `test_seal_cli_refuses_invalid_or_nonready_campaign` | `a9b95acdc8ebf33a0041c0971584c6da299b1e166af309b8224eb75c1848af0e` |
| `test_seal_cli_refuses_existing_worktree_and_unsafe_destinations` | `010cf9b4c1b218de9dfb9204744fe9bf5ab4312b44e4884dc2f2fcfdfa75fc5b` |
| `test_seal_fails_closed_when_parent_or_ancestor_is_swapped` | `cfccdb9ed35deaeb19c72888b1ff9089c60950a2303ceb61bbb034146a665f4c` |
| `test_sha_locators_bind_package_attestation_and_worksheet_bytes` | `a22158545e4a5da79e435e24539243abcc26972e77a0edd58d8d714b6ddeaf94` |
| `test_valid_draft_campaign_is_transition_ready` | `448e7b9e1bbdc69159d887033cd05204afd111e71db6fa493affdc9c2e02ecac` |
| `test_valid_final_campaign_is_recursively_merge_ready` | `6caf1a1f2cc7fd6b2bd255f64a272b02bfef25193d58220c031cd447f8d8c946` |
| `test_validator_cli_classifies_preopen_permissions_as_operational` | `788950d76b07846f2129eba5c2f17daf16407ce76509c52141383045a8d49ceb` |
| `test_validator_cli_emits_canonical_reports_and_exit_codes` | `e40d05ed85181a7aeb8e9b2203e7bfe0df8e28077c3b57fe3cbdf6eee00d1c07` |
| `test_validator_cli_keeps_batch_object_failure_operational` | `2d2c0983d07685de9e1ede5fc90f755712c79a95cd64c2ef8333f66f81216fed` |
| `test_validator_cli_requires_check_and_all_or_none_draft_inputs` | `243bb8120b599e6a838848615b68a8b1db864ffe3d8bf0bda2cd4dba41d8b19e` |
| `test_validator_cli_sanitizes_missing_and_permission_failures` | `573b65c526cd6b51147d1b860459f523b9a35f240295c8a8c644d040cece0d46` |

---

### Task 1: Freeze the case inventory and baseline ledger

**Files:**
- Create: `tests/qualified_review_policy_cases.py`
- Modify: `tests/test_validate_qualified_review_evidence.py:1-38, 1331-2194`
- Test: `tests/test_validate_qualified_review_evidence.py`

**Interfaces:**
- Produces: `BoundaryFamily = Literal["role_readiness", "draft_reference"]`.
- Produces: `FixtureKind = Literal["draft", "reviewed_final", "description_candidate", "duplicate_candidate"]`.
- Produces: `CandidateKey = Literal["draft", "reviewed", "description", "duplicate"]` and frozen `CandidateReference(key: CandidateKey)`.
- Produces: frozen `FieldOperation(path: tuple[str | int, ...], value: FrozenValue | CandidateReference)`.
- Produces: frozen `ExpectedReport(evidence_valid: bool, readiness_name: str, readiness_value: bool, candidate_key: CandidateKey, campaign_id: str, errors: tuple[str, ...])`.
- Produces: frozen `QualifiedReviewPolicyCase(method_name: str, case_id: str, boundary: BoundaryFamily, fixture_kind: FixtureKind, operations: tuple[FieldOperation, ...], expected: ExpectedReport)`.
- Produces: `FullPathRoute = Literal["draft", "final", "recursive_draft", "validator_cli", "seal_cli"]`.
- Produces: frozen `RetainedCaseBaseline(case_id: str, method_name: str, case_label: str, routes: tuple[FullPathRoute, ...], rationale: str)`.
- Produces: frozen `MethodBaseline(method_name: str, detail_entries: int, selected_entries: int, retained_cases: tuple[RetainedCaseBaseline, ...], copytree_operations: int, retained_source_ast_sha256: str)`.
- Produces: frozen `QualifiedReviewPolicyInventory(cases: tuple[QualifiedReviewPolicyCase, ...], methods: tuple[MethodBaseline, ...], retained_cases: tuple[RetainedCaseBaseline, ...], population_sha256: str)` with `cases_for_method(method_name: str) -> tuple[QualifiedReviewPolicyCase, ...]`.
- Produces: `qualified_review_policy_inventory() -> QualifiedReviewPolicyInventory` and `qualified_review_population_sha256(cases: Sequence[QualifiedReviewPolicyCase]) -> str`.

- [ ] **Step 1: Add failing inventory contract tests**

Add `QualifiedReviewPolicyInventoryTests`. Require 43 ledger rows in the exact source order shown above, totals `(92, 31, 61, 108)`, 28 unique cases, 15 selected methods, a 24/4 boundary split, immutable tuples, valid path tokens, unique case IDs, and a recomputed digest equal to the reviewed constant `f89f118c4d5fe3dfc1a906cebb3f13a7cf5da7b6349c3e3913470c6cd179f50a`.

Freeze every retained baseline case as an explicit record. Use the current subtest label when one exists and `default` for an unlabelled single case. Give each record the identifier `<method-name>:retained:<case-label>`. Its `routes` tuple shall list every detailed-validation entry in order, such as `("final", "recursive_draft")` for a Final case that reaches retained Draft validation. Do not generate records or routes from a count at runtime. Require unique identifiers, nonempty labels and invariant-based rationales, allowed routes, and exactly 61 route elements across all records.

For all 28 methods outside the selected migration, including the three methods with zero detailed-validation entries, store and verify the SHA-256 of the location-free AST dump from baseline commit `f99e403583877f803576dcad919025e558e5a5f6`. This makes a count-preserving loop, label, mutation, route, or zero-entry security-test change fail the ledger contract. Only the 15 methods changed by the approved Stage 2 migration are excluded from this AST binding. The retained accepted-severity method has the exact reviewed AST digest `8bbbac1520f72932847f347658414654092f2deacbfcc93e37be0de833c6e587`.

Use mutation tests that call the lower-level validator with one defect at a time:

```python
def test_inventory_rejects_count_digest_and_mutability_drift(self) -> None:
    inventory = qualified_review_policy_inventory()
    changed = replace(inventory.cases[0], case_id="changed")
    with self.assertRaisesRegex(ValueError, "population digest"):
        validate_qualified_review_policy_inventory(
            (changed, *inventory.cases[1:]),
            inventory.methods,
            inventory.population_sha256,
        )
```

Assert the exact selected per-method distribution: `5, 4, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1` for the 14 role methods in design order, plus four reference cases. Assert the reference detail-entry distribution `2, 1, 2, 2` for campaign ID, candidate commit, manifest digest, and seal-record digest.

- [ ] **Step 2: Run the focused inventory tests and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$redOutput = & python -m unittest tests.test_validate_qualified_review_evidence.QualifiedReviewPolicyInventoryTests -v 2>&1
$redExit = $LASTEXITCODE
$redOutput
if ($redExit -eq 0 -or ($redOutput -join "`n") -notmatch 'ModuleNotFoundError.*qualified_review_policy_cases') {
  throw 'inventory RED run did not fail for the missing inventory module'
}
```

Expected: FAIL with `ModuleNotFoundError` for `tests.qualified_review_policy_cases`.

- [ ] **Step 3: Implement the frozen records, exact ledger, and 28 cases**

Use a recursive immutable value type and canonical serialization:

```python
JsonScalar: TypeAlias = None | bool | int | str
FrozenValue: TypeAlias = JsonScalar | tuple["FrozenValue", ...] | tuple[
    tuple[str, "FrozenValue"], ...
]

@dataclass(frozen=True)
class CandidateReference:
    key: CandidateKey

OperationValue: TypeAlias = FrozenValue | CandidateReference

payload = json.dumps(
    semantic_rows,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
return hashlib.sha256(payload).hexdigest()
```

Define the case record directly from those immutable values:

```python
@dataclass(frozen=True)
class QualifiedReviewPolicyCase:
    method_name: str
    case_id: str
    boundary: BoundaryFamily
    fixture_kind: FixtureKind
    operations: tuple[FieldOperation, ...]
    expected: ExpectedReport
```

Give every mutation a stable identifier. Use these prefixes and counts: `ineligible` 5, `actor-alias` 4, `mapper-alias` 1, `resolved-conflict` 1, `duplicate-human` 1, `stop-open` 2, `pass-open` 1, `post-correction` 2, `orphan-record` 1, `finding-set` 1, `finding-description` 1, `duplicate-finding-id` 1, `reviewed-reviewer` 2, `final-post-correction` 1, and `draft-reference` 4.

The whitespace-only duplicate qualification and the accepted Critical and Important severity mutations are schema-owned. Retain those three complete-path entries outside the equivalence population. Keep direct pure-policy tests for the same inputs as explicit defense-in-depth coverage and label them intentionally non-schema-valid. The exact proof must not claim full/narrow equivalence for inputs rejected before the policy layer.

Store final field values or `CandidateReference` records, not lambdas. Canonical serialization shall encode a candidate reference as `{"candidate_reference": "<key>"}` so it cannot collide with an ordinary tuple or string value. Use `fixture_kind="description_candidate"` and `fixture_kind="duplicate_candidate"` for the two alternate-commit cases. Use candidate references and expected `candidate_key` values rather than embedding temporary SHAs in the digest. The shared support module shall resolve every reference from its fixture before applying a mutation or constructing an expected projection, and shall reject an unknown key.

Set the expected errors to the current exact messages. The mapping-set prefix comes from the selected fixture, and the suffixes are:

```text
specification_and_inventory reviewer is not eligible
specification_and_inventory reviewer is also a mapper
specification_and_inventory reviewer has an unresolved conflict
specification_and_inventory reviewer eligibility was rejected
duplicate reviewer lacks complete dual-role acceptance and qualifications
Critical finding cannot be accepted
Important finding cannot be accepted
pass conclusion has an open finding
specification_and_inventory post-correction candidate is not the campaign candidate
finding review-finding-1 references an unknown record
findings do not equal authoritative candidate findings
candidate finding identifiers are duplicated
mapping-set reviewer does not equal the specification review evidence
record reviewer does not equal the security review evidence
```

The four Draft-reference errors are exactly `Draft campaign identifier does not match the reference`, `reviewed and Draft candidate commits must differ`, `Draft manifest digest does not match the reference`, and `Draft seal-record digest does not match the reference`. Valid resolved-conflict and exact post-correction cases have `errors=()` and `readiness_value=True`. Stop cases have valid evidence, `errors=()`, and `readiness_value=False`.

- [ ] **Step 4: Run inventory tests and verify GREEN**

```powershell
python -m unittest tests.test_validate_qualified_review_evidence.QualifiedReviewPolicyInventoryTests -v
if ($LASTEXITCODE -ne 0) { throw "inventory tests exited $LASTEXITCODE" }
git diff --check
if ($LASTEXITCODE -ne 0) { throw "diff check exited $LASTEXITCODE" }
```

Expected: PASS, exact totals match the ledger, and the reviewed digest is a 64-character lowercase SHA-256.

- [ ] **Step 5: Commit the inventory**

```powershell
git add tests/qualified_review_policy_cases.py tests/test_validate_qualified_review_evidence.py
if ($LASTEXITCODE -ne 0) { throw "inventory staging exited $LASTEXITCODE" }
git commit -m "test: freeze qualified-review policy inventory"
if ($LASTEXITCODE -ne 0) { throw "inventory commit exited $LASTEXITCODE" }
```

### Task 2: Add the ordered role and readiness policy boundary

**Files:**
- Modify: `tools/validate_qualified_review_evidence.py:83-118, 696-909`
- Modify: `tests/test_validate_qualified_review_evidence.py:1-38, 676-2194`
- Test: `tests/test_validate_qualified_review_evidence.py`

**Interfaces:**
- Produces: `RolePolicyStage = Literal["reviewer_eligibility", "role_findings", "mapping_set_completion"]`.
- Produces: frozen `ReviewerEligibilityPolicyInput`, `RoleFindingsPolicyInput`, `MappingSetCompletionPolicyInput`, and their union `RolePolicyInput`.
- Produces: frozen `RolePolicyResult(mapping_ready: bool, observed_findings: tuple[tuple[str, tuple[object, ...]], ...])`.
- Produces: `validate_role_readiness_policy(stage: RolePolicyStage, policy_input: RolePolicyInput) -> RolePolicyResult`.
- Produces: frozen `MappingSetPolicyInput` and `evaluate_mapping_set_policy(policy_input: MappingSetPolicyInput) -> bool` for the narrow inventory route.

- [ ] **Step 1: Add failing pure-boundary tests**

Add `QualifiedReviewRolePolicyBoundaryTests`. Build inputs from frozen dataclasses only. Patch `Path.open`, `Path.read_bytes`, `subprocess.run`, `GitReader.read_bytes`, and `build_campaign_archive` to raise if called. Cover eligible and ineligible reviewers, Unicode and punctuation aliases, mapper aliases, conflict states, dual-role rules, stop readiness, accepted severities, open findings, post-correction SHA binding, unknown records, cross-role conflicts, authoritative equality, duplicate authoritative IDs, and reviewed-state reviewer metadata.

```python
with mock.patch.object(Path, "read_bytes", side_effect=AssertionError("I/O")):
    result = evaluate_mapping_set_policy(valid_policy_input)
self.assertTrue(result)
```

Add a multi-defect ordering test for each stage. Require eligibility before finding policy and finding policy before mapping-set completion.

- [ ] **Step 2: Run boundary tests and verify RED**

```powershell
$redOutput = & python -m unittest tests.test_validate_qualified_review_evidence.QualifiedReviewRolePolicyBoundaryTests -v 2>&1
$redExit = $LASTEXITCODE
$redOutput
if ($redExit -eq 0 -or ($redOutput -join "`n") -notmatch 'validate_role_readiness_policy|ReviewerEligibilityPolicyInput') {
  throw 'role-policy RED run did not fail for the absent production boundary'
}
```

Expected: FAIL because the policy dataclasses and functions do not exist.

- [ ] **Step 3: Implement minimal immutable policy operations**

Move `_canonical_actor_identity()`, `_same_actor()` policy use, eligibility rules, conclusion and finding rules, authoritative equality, and reviewed-state metadata equality behind the staged function. Freeze mapper identities with `frozenset`, record IDs with `frozenset`, roles with tuples, and observed findings with a sorted tuple representation at each return boundary.

Dispatch explicitly and reject a mismatched stage/input pair:

```python
def validate_role_readiness_policy(
    stage: RolePolicyStage,
    policy_input: RolePolicyInput,
) -> RolePolicyResult:
    if stage == "reviewer_eligibility" and isinstance(
        policy_input, ReviewerEligibilityPolicyInput
    ):
        return _validate_reviewer_eligibility_policy(policy_input)
    if stage == "role_findings" and isinstance(
        policy_input, RoleFindingsPolicyInput
    ):
        return _validate_role_findings_policy(policy_input)
    if stage == "mapping_set_completion" and isinstance(
        policy_input, MappingSetCompletionPolicyInput
    ):
        return _validate_mapping_set_completion_policy(policy_input)
    raise TypeError("role policy stage and input do not match")
```

`evaluate_mapping_set_policy()` shall call these same three operations in production order. It shall not copy their rules.

- [ ] **Step 4: Run boundary tests and verify GREEN**

```powershell
python -m unittest tests.test_validate_qualified_review_evidence.QualifiedReviewRolePolicyBoundaryTests -v
if ($LASTEXITCODE -ne 0) { throw "role boundary tests exited $LASTEXITCODE" }
git diff --check
if ($LASTEXITCODE -ne 0) { throw "diff check exited $LASTEXITCODE" }
```

Expected: PASS with no filesystem, Git, schema, archive, seal, or fixture dependency in the pure route.

- [ ] **Step 5: Commit the role boundary**

```powershell
git add tools/validate_qualified_review_evidence.py tests/test_validate_qualified_review_evidence.py
if ($LASTEXITCODE -ne 0) { throw "role boundary staging exited $LASTEXITCODE" }
git commit -m "refactor: extract qualified-review role policy"
if ($LASTEXITCODE -ne 0) { throw "role boundary commit exited $LASTEXITCODE" }
```

### Task 3: Add the ordered Draft-reference boundary

**Files:**
- Modify: `tools/validate_qualified_review_evidence.py:111-118, 912-980`
- Modify: `tests/test_validate_qualified_review_evidence.py:1-38, 1936-2194`
- Test: `tests/test_validate_qualified_review_evidence.py`

**Interfaces:**
- Produces: `DraftReferenceStage = Literal["distinct_candidate", "draft_status", "campaign_id", "candidate_commit", "manifest_sha256", "seal_record_sha256"]`.
- Produces: frozen `DistinctCandidateCheck`, `DraftStatusCheck`, `ScalarReferenceCheck`, and union `DraftReferenceCheck`.
- Produces: `validate_draft_reference_binding(check: DraftReferenceCheck) -> None`.
- Produces: frozen `DraftReferencePolicyInput` and `evaluate_draft_reference_policy(policy_input: DraftReferencePolicyInput) -> None` for the narrow inventory route.

- [ ] **Step 1: Add failing ordered-reference tests**

Add `QualifiedReviewDraftReferenceBoundaryTests`. Require the exact four selected errors plus a valid input. Patch all path, Git, JSON, archive, and seal operations to fail if called. Add ordered multi-defect tests that prove distinct candidate comes first, then Draft status, campaign ID, candidate commit, manifest digest, and seal digest.

```python
with self.assertRaisesRegex(
    _ValidationFailure,
    "reviewed and Draft candidate commits must differ",
):
    validate_draft_reference_binding(
        DistinctCandidateCheck(reviewed_candidate=SHA, referenced_candidate=SHA)
    )
```

- [ ] **Step 2: Run reference tests and verify RED**

```powershell
$redOutput = & python -m unittest tests.test_validate_qualified_review_evidence.QualifiedReviewDraftReferenceBoundaryTests -v 2>&1
$redExit = $LASTEXITCODE
$redOutput
if ($redExit -eq 0 -or ($redOutput -join "`n") -notmatch 'validate_draft_reference_binding|DistinctCandidateCheck') {
  throw 'Draft-reference RED run did not fail for the absent production boundary'
}
```

Expected: FAIL because the reference check types and functions do not exist.

- [ ] **Step 3: Implement the staged scalar checks and combined adapter**

`DistinctCandidateCheck` contains the reviewed and referenced candidates. `DraftStatusCheck` contains phase, evidence validity, readiness name, and readiness value. `ScalarReferenceCheck` contains one of the four scalar stages plus expected and actual strings. Reject an incompatible dataclass or scalar stage with `TypeError`.

`evaluate_draft_reference_policy()` shall run the stages in the exact design order over immutable values. It performs no recursion, file read, hashing, JSON parsing, archive comparison, or seal reconstruction.

```python
def validate_draft_reference_binding(check: DraftReferenceCheck) -> None:
    if isinstance(check, DistinctCandidateCheck):
        _validate_distinct_candidate(check)
        return
    if isinstance(check, DraftStatusCheck):
        _validate_draft_status(check)
        return
    if isinstance(check, ScalarReferenceCheck):
        _validate_scalar_reference(check)
        return
    raise TypeError("unknown Draft reference check")
```

- [ ] **Step 4: Run reference tests and verify GREEN**

```powershell
python -m unittest tests.test_validate_qualified_review_evidence.QualifiedReviewDraftReferenceBoundaryTests -v
if ($LASTEXITCODE -ne 0) { throw "Draft reference tests exited $LASTEXITCODE" }
git diff --check
if ($LASTEXITCODE -ne 0) { throw "diff check exited $LASTEXITCODE" }
```

Expected: PASS with exact sanitized messages and no I/O calls.

- [ ] **Step 5: Commit the reference boundary**

```powershell
git add tools/validate_qualified_review_evidence.py tests/test_validate_qualified_review_evidence.py
if ($LASTEXITCODE -ne 0) { throw "Draft reference staging exited $LASTEXITCODE" }
git commit -m "refactor: extract Draft reference policy"
if ($LASTEXITCODE -ne 0) { throw "Draft reference commit exited $LASTEXITCODE" }
```

### Task 4: Route production and extract proof-critical support

**Files:**
- Create: `tests/qualified_review_hot_path_support.py`
- Modify: `tools/validate_qualified_review_evidence.py:726-1089`
- Modify: `tests/test_validate_qualified_review_evidence.py:40-577, 676-1330, 1331-2194`
- Test: `tests/test_validate_qualified_review_evidence.py`

**Interfaces:**
- Produces: `ReportProjection(evidence_valid: bool, readiness_name: str, readiness_value: bool, candidate_commit: str, campaign_id: str, errors: tuple[str, ...])`.
- Produces: `QualifiedReviewHotPathFixture.create(root: Path, repository_root: Path) -> QualifiedReviewHotPathFixture` with the current Draft, reviewed, description, and duplicate candidate facts.
- Produces: `run_full_case(fixture: QualifiedReviewHotPathFixture, case: QualifiedReviewPolicyCase, destination: Path) -> ReportProjection`.
- Produces: `run_narrow_case(fixture: QualifiedReviewHotPathFixture, case: QualifiedReviewPolicyCase) -> ReportProjection`.
- Produces: `expected_projection(fixture: QualifiedReviewHotPathFixture, case: QualifiedReviewPolicyCase) -> ReportProjection`.
- Produces: `resolve_operation_value(fixture: QualifiedReviewHotPathFixture, value: OperationValue) -> FrozenValue`, including strict `CandidateReference` resolution.
- Preserves: every selected test method still uses `_report()`, `_final_report()`, or direct `validate_campaign()` at the end of this task.

- [ ] **Step 1: Add failing production-routing and support tests**

Add `QualifiedReviewPolicyRoutingTests`. Patch each staged function with `wraps` and validate a real Draft fixture. Assert eligibility calls occur before the paired `_validate_role_files()` call, finding calls occur after it, and completion follows both roles. For Final input, assert the distinct-candidate check precedes recursive `_validate_campaign_details()`, the manifest check precedes retained archive comparison, and the seal-digest check precedes seal parsing.

Add support tests that compare projected valid Draft and Final reports with direct validation. Require declarative operations to reject unknown paths, list growth, type mismatch, and mutation of the source case record.

- [ ] **Step 2: Run routing and support tests and verify RED**

```powershell
$tests = @(
  'tests.test_validate_qualified_review_evidence.QualifiedReviewPolicyRoutingTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewHotPathSupportTests'
)
$redOutput = & python -m unittest @tests -v 2>&1
$redExit = $LASTEXITCODE
$redOutput
if ($redExit -eq 0 -or ($redOutput -join "`n") -notmatch 'qualified_review_hot_path_support|production routing') {
  throw 'routing RED run did not fail for the absent support or routing contract'
}
```

Expected: FAIL because wrappers still own the policy and the support module is absent.

- [ ] **Step 3: Extract shared fixture construction without changing selected calls**

Move deterministic fixture construction from `CampaignValidationTests.setUpClass()`, its reviewed-candidate builders, and its finding-candidate builders into `QualifiedReviewHotPathFixture.create()`. Make the test class delegate to this object and expose the same attributes so all existing method bodies remain unchanged.

`run_full_case()` shall create a fresh destination for every case, apply its operations, rewrite role files and manifests through the same helpers used by current tests, then call the complete validator. It shall use alternate readers and SHAs for description and duplicate fixtures. `run_narrow_case()` shall build fresh immutable inputs and call only the combined narrow adapter. Neither route may derive expected results from the other.

```python
@classmethod
def setUpClass(cls) -> None:
    cls.shared_temporary = tempfile.TemporaryDirectory()
    cls.hot_path_fixture = QualifiedReviewHotPathFixture.create(
        Path(cls.shared_temporary.name),
        ROOT,
    )
    cls.hot_path_fixture.attach_to_test_class(cls)
```

- [ ] **Step 4: Route production through ordered operations**

In `_validate_roles_and_readiness()`, replace each policy block with its staged function at the same source position. Keep `_validate_role_files()` between eligibility and findings. In `_validate_draft_reference()`, call `DistinctCandidateCheck` before recursion, call status and scalar checks after Draft validation, keep archive comparison in place, then call the seal scalar check before JSON parsing and deterministic seal reconstruction.

Add `test_policy_boundaries_reach_full_campaign_validation` with five labelled full-path subcases: mapper alias, reviewer ineligibility, stop conclusion, authoritative-finding mismatch, and reviewed-state reviewer mismatch. Add `test_draft_reference_boundary_reaches_full_final_validation` with a manifest-digest reference mismatch that enters the Final and recursive Draft paths. These new integration anchors are outside the baseline ledger and the 28-case inventory. Structural tests shall require their exact names and labels, require complete-validator calls, and keep them unchanged in Stage 2.

```python
validate_role_readiness_policy("reviewer_eligibility", eligibility_input)
findings = _validate_role_files(
    campaign=campaign,
    mapping_set=mapping_set,
    role=role,
    candidate_mapping=candidate_mapping,
    evidence_root=evidence_root,
    worktrees=worktrees,
    allowlist=allowlist,
    snapshot=snapshot,
)
role_result = validate_role_readiness_policy(
    "role_findings",
    findings_input(findings),
)
```

- [ ] **Step 5: Run focused routing, support, and retained-path tests**

```powershell
$tests = @(
  'tests.test_validate_qualified_review_evidence.QualifiedReviewPolicyRoutingTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewHotPathSupportTests'
  'tests.test_validate_qualified_review_evidence.CampaignValidationTests.test_valid_draft_campaign_is_transition_ready'
  'tests.test_validate_qualified_review_evidence.CampaignValidationTests.test_valid_final_campaign_is_recursively_merge_ready'
  'tests.test_validate_qualified_review_evidence.CampaignValidationTests.test_policy_boundaries_reach_full_campaign_validation'
  'tests.test_validate_qualified_review_evidence.CampaignValidationTests.test_draft_reference_boundary_reaches_full_final_validation'
)
python -m unittest @tests -v
if ($LASTEXITCODE -ne 0) { throw "routing and integration run exited $LASTEXITCODE" }
git diff --check
if ($LASTEXITCODE -ne 0) { throw "diff check exited $LASTEXITCODE" }
```

Expected: PASS. Inspect the selected method bodies and confirm they still call the complete path.

- [ ] **Step 6: Commit production routing and shared support**

```powershell
git add tests/qualified_review_hot_path_support.py tests/test_validate_qualified_review_evidence.py tools/validate_qualified_review_evidence.py
if ($LASTEXITCODE -ne 0) { throw "routing staging exited $LASTEXITCODE" }
git commit -m "refactor: route qualified-review policy boundaries"
if ($LASTEXITCODE -ne 0) { throw "routing commit exited $LASTEXITCODE" }
```

### Task 5: Build the verifier and create the observable Stage 1 proof

**Files:**
- Create: `tools/verify_qualified_review_hot_path_equivalence.py`
- Modify: `tests/test_validate_qualified_review_evidence.py:1-38, 676-1330`
- Test: `tests/test_validate_qualified_review_evidence.py`

**Interfaces:**
- Produces: frozen `EquivalenceResult(candidate_sha: str, method_count: int, population_count: int, population_sha256: str, full_comparison_count: int, narrow_comparison_count: int)`.
- Produces: `require_exact_candidate(root: Path, candidate_sha: str, runner: GitRunner = run_git) -> None`.
- Produces: `verify_qualified_review_hot_path_equivalence(root: Path, candidate_sha: str) -> EquivalenceResult`.
- Produces: `main(argv: Sequence[str] | None = None, *, root: Path = ROOT) -> int` and CLI `python -B tools/verify_qualified_review_hot_path_equivalence.py --check --candidate-sha $candidate`.

- [ ] **Step 1: Add failing verifier contract tests**

Test argument rejection, uppercase or abbreviated SHA rejection, HEAD mismatch, dirty status, Git failure sanitization, full/narrow mismatch, full/expected mismatch, narrow/expected mismatch, temporary-path sanitization, post-comparison HEAD drift, and post-comparison dirty state. Require both preflight and postflight checks.

Successful output comes directly from these print statements:

```python
print(f"candidate_sha={result.candidate_sha}")
print("method_count=15")
print("population_count=28")
print(f"population_sha256={result.population_sha256}")
print("full_comparison_count=28")
print("narrow_comparison_count=28")
print("equivalence=PASS")
```

- [ ] **Step 2: Run verifier tests and verify RED**

```powershell
$redOutput = & python -m unittest tests.test_validate_qualified_review_evidence.QualifiedReviewHotPathEquivalenceCommandTests -v 2>&1
$redExit = $LASTEXITCODE
$redOutput
if ($redExit -eq 0 -or ($redOutput -join "`n") -notmatch 'verify_qualified_review_hot_path_equivalence') {
  throw 'verifier RED run did not fail for the missing verifier module'
}
```

Expected: FAIL because the verifier module does not exist.

- [ ] **Step 3: Implement fail-closed candidate checks and comparisons**

Require regex `[0-9a-f]{40}`, exact `git rev-parse HEAD`, and empty `git status --porcelain=v1 --untracked-files=all`. Load the validated inventory once. For every case, allocate a fresh temporary destination, then compute full, narrow, and expected projections independently and compare each pair.

Reject any diagnostic containing the temporary root in native or slash-normalized form. Run the exact-candidate check again after all 28 comparisons. Return `EquivalenceResult` only after postflight. `main()` prints PASS fields only from the returned result.

```python
for case in inventory.cases:
    with tempfile.TemporaryDirectory() as directory:
        destination = Path(directory) / case.case_id
        full = run_full_case(fixture, case, destination)
        narrow = run_narrow_case(fixture, case)
        expected = expected_projection(fixture, case)
        require_equal(case.case_id, "full", full, "narrow", narrow)
        require_equal(case.case_id, "full", full, "expected", expected)
        require_equal(case.case_id, "narrow", narrow, "expected", expected)
require_exact_candidate(root, candidate_sha, runner)
```

- [ ] **Step 4: Run verifier unit tests and focused module tests**

```powershell
$tests = @(
  'tests.test_validate_qualified_review_evidence.QualifiedReviewHotPathEquivalenceCommandTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewPolicyInventoryTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewRolePolicyBoundaryTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewDraftReferenceBoundaryTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewPolicyRoutingTests'
)
python -m unittest @tests -v
if ($LASTEXITCODE -ne 0) { throw "verifier-focused tests exited $LASTEXITCODE" }
python tools/validate_test_shards.py --check
if ($LASTEXITCODE -ne 0) { throw "shard manifest validation exited $LASTEXITCODE" }
git diff --check
if ($LASTEXITCODE -ne 0) { throw "diff check exited $LASTEXITCODE" }
```

Expected: PASS. The shard manifest remains unchanged.

- [ ] **Step 5: Commit the complete pre-migration surface**

```powershell
git add tools/verify_qualified_review_hot_path_equivalence.py tests/test_validate_qualified_review_evidence.py
if ($LASTEXITCODE -ne 0) { throw "verifier staging exited $LASTEXITCODE" }
git commit -m "test: prove qualified-review hot-path equivalence"
if ($LASTEXITCODE -ne 0) { throw "Stage 1 commit exited $LASTEXITCODE" }
```

This commit is the mandatory observable Stage 1 candidate. Do not change a selected test call before this commit exists.

- [ ] **Step 6: Verify clean state and run the exact-SHA Stage 1 proof**

```powershell
$ErrorActionPreference='Stop'
$env:PYTHONDONTWRITEBYTECODE='1'
$stage1 = git rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw "git rev-parse exited $LASTEXITCODE" }
if ($stage1 -notmatch '^[0-9a-f]{40}$') { throw 'invalid Stage 1 SHA' }
$stage1Status = git status --porcelain=v1 --untracked-files=all
if ($LASTEXITCODE -ne 0) { throw "git status exited $LASTEXITCODE" }
if ($stage1Status) { throw 'dirty Stage 1 checkout' }
$caches = Get-ChildItem -Recurse -Directory -Filter __pycache__
if ($caches) { throw 'generated Python cache exists' }
$stage1Output = & python -B tools/verify_qualified_review_hot_path_equivalence.py --check --candidate-sha $stage1 2>&1
$stage1Exit = $LASTEXITCODE
$stage1Output
if ($stage1Exit -ne 0) { throw "Stage 1 equivalence exited $stage1Exit" }
$stage1ProofUtc = [DateTimeOffset]::UtcNow.ToString("yyyy-MM-dd'T'HH:mm:ss'Z'")
Write-Output "proof_timestamp_utc=$stage1ProofUtc"
```

Expected: the seven PASS lines above with `method_count=15`, `population_count=28`, and both comparison counts equal to 28, followed by one RFC 3339 UTC timestamp line. Preserve the complete output, timestamp, Stage 1 SHA, and inventory digest for Task 6. Do not start Task 6 if this command fails.

- [ ] **Step 7: Record proof-critical hashes outside the worktree change set**

```powershell
$critical = @(
  'tests/qualified_review_policy_cases.py',
  'tests/qualified_review_hot_path_support.py',
  'tools/validate_qualified_review_evidence.py',
  'tools/verify_qualified_review_hot_path_equivalence.py'
)
foreach ($path in $critical) {
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()
  Write-Output "critical_sha256[$path]=$hash"
}
```

Expected: four path-bound lowercase SHA-256 records in the receipt format. Keep these values with the Stage 1 output. Task 6 will place them in the receipt and prove they did not change.

### Task 6: Migrate only proven calls in Stage 2

**Files:**
- Modify: `tests/test_validate_qualified_review_evidence.py:1331-2194`
- Create: `docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md`
- Test: `tests/test_validate_qualified_review_evidence.py`
- Must not modify: `tests/qualified_review_policy_cases.py`, `tests/qualified_review_hot_path_support.py`, `tools/validate_qualified_review_evidence.py`, `tools/verify_qualified_review_hot_path_equivalence.py`

**Interfaces:**
- Consumes: `qualified_review_policy_inventory()`, `run_narrow_case()`, and the exact Stage 1 proof output.
- Produces: `_assert_policy_cases_narrow(method_name: str) -> None` in the test class.
- Produces: structural guards that bind the 15 selected methods to the inventory and reject complete-path calls.

- [ ] **Step 1: Add failing migration guards before changing selected calls**

Parse `tests/test_validate_qualified_review_evidence.py` with `ast`. For the 15 exact method names, reject calls named `_report`, `_final_report`, `_final_inputs`, `validate_campaign`, `_validate_campaign_details`, `copytree`, or a test-owned policy predicate. Require each selected method to call `_assert_policy_cases_narrow()` once with its own method name.

Add a consumption test that patches `run_narrow_case` and proves all 28 case IDs are seen exactly once across the 15 methods.

- [ ] **Step 2: Run structural tests and verify RED**

```powershell
$redOutput = & python -m unittest tests.test_validate_qualified_review_evidence.QualifiedReviewHotPathMigrationStructureTests -v 2>&1
$redExit = $LASTEXITCODE
$redOutput
if ($redExit -eq 0 -or ($redOutput -join "`n") -notmatch 'selected methods still call complete validation') {
  throw 'migration RED run did not fail for selected complete-path calls'
}
```

Expected: FAIL because selected methods still contain complete-path calls.

- [ ] **Step 3: Replace only the selected method bodies**

Implement the helper:

```python
def _assert_policy_cases_narrow(self, method_name: str) -> None:
    inventory = qualified_review_policy_inventory()
    cases = inventory.cases_for_method(method_name)
    self.assertGreater(len(cases), 0)
    for case in cases:
        with self.subTest(case_id=case.case_id):
            self.assertEqual(
                run_narrow_case(self.hot_path_fixture, case),
                expected_projection(self.hot_path_fixture, case),
            )
```

Each selected method becomes one call to this helper. Do not change retained methods or the Stage 1 integration methods. Do not edit a proof-critical file.

- [ ] **Step 4: Write the humanized Stage 1 receipt**

Use the humanizer skill in embedded mode. Record the full Stage 1 SHA on exactly one line formatted `stage1_sha=<40 lowercase hexadecimal characters>`. Record the proof time on exactly one `proof_timestamp_utc=<RFC 3339 UTC value>` line. Include the exact inventory digest and all seven verifier output lines. Record each proof-critical hash on exactly one line formatted `critical_sha256[<repository-relative-path>]=<64 lowercase hexadecimal characters>`. Include the statement that selected methods still used the complete path at that SHA. State that Stage 2 changed only selected call sites, grouping, guards, and this receipt.

- [ ] **Step 5: Verify guards, inventory consumption, and proof-critical hashes**

```powershell
$ErrorActionPreference='Stop'
$tests = @(
  'tests.test_validate_qualified_review_evidence.QualifiedReviewHotPathMigrationStructureTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewPolicyInventoryTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewRolePolicyBoundaryTests'
  'tests.test_validate_qualified_review_evidence.QualifiedReviewDraftReferenceBoundaryTests'
)
python -m unittest @tests -v
if ($LASTEXITCODE -ne 0) { throw "migration verification exited $LASTEXITCODE" }
$critical = @(
  'tests/qualified_review_policy_cases.py',
  'tests/qualified_review_hot_path_support.py',
  'tools/validate_qualified_review_evidence.py',
  'tools/verify_qualified_review_hot_path_equivalence.py'
)
$receipt = 'docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md'
$stage1Matches = @(Select-String -Path $receipt -Pattern '^stage1_sha=([0-9a-f]{40})$')
if ($stage1Matches.Count -ne 1) { throw 'receipt shall contain exactly one stage1_sha field' }
$stage1Sha = $stage1Matches[0].Matches[0].Groups[1].Value
foreach ($path in $critical) {
  $escapedPath = [regex]::Escape($path)
  $recorded = @(Select-String -Path $receipt -Pattern "^critical_sha256\[$escapedPath\]=([0-9a-f]{64})$")
  if ($recorded.Count -ne 1) { throw "receipt hash field missing or duplicated for $path" }
  $expectedHash = $recorded[0].Matches[0].Groups[1].Value
  $currentHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()
  if ($currentHash -ne $expectedHash) { throw "proof-critical hash changed for $path" }
}
git diff --quiet HEAD -- @critical
if ($LASTEXITCODE -ne 0) { throw 'proof-critical working-tree content differs from Stage 1 HEAD' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw "diff check exited $LASTEXITCODE" }
```

Expected: PASS, 28 unique case IDs consumed, and all four hashes exactly equal the Stage 1 values.

- [ ] **Step 6: Review the Stage 2 path boundary and commit**

```powershell
$receipt = 'docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md'
$stage1Matches = @(Select-String -Path $receipt -Pattern '^stage1_sha=([0-9a-f]{40})$')
if ($stage1Matches.Count -ne 1) { throw 'receipt shall contain exactly one stage1_sha field' }
$stage1Sha = $stage1Matches[0].Matches[0].Groups[1].Value
$critical = @(
  'tests/qualified_review_policy_cases.py'
  'tests/qualified_review_hot_path_support.py'
  'tools/validate_qualified_review_evidence.py'
  'tools/verify_qualified_review_hot_path_equivalence.py'
)
$expectedPaths = @(
  'docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md'
  'tests/test_validate_qualified_review_evidence.py'
)
$trackedChanged = @(git diff --name-only HEAD)
if ($LASTEXITCODE -ne 0) { throw 'tracked changed-path acquisition failed' }
$untrackedChanged = @(git ls-files --others --exclude-standard)
if ($LASTEXITCODE -ne 0) { throw 'untracked changed-path acquisition failed' }
$changedPaths = @($trackedChanged + $untrackedChanged) | Sort-Object -Unique
$pathDiff = @(Compare-Object ($expectedPaths | Sort-Object) $changedPaths)
if ($pathDiff) { throw "Stage 2 changed-path set is invalid: $($pathDiff | Out-String)" }
git diff -- tests/test_validate_qualified_review_evidence.py docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md
if ($LASTEXITCODE -ne 0) { throw "Stage 2 diff display exited $LASTEXITCODE" }
git add tests/test_validate_qualified_review_evidence.py docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md
if ($LASTEXITCODE -ne 0) { throw "Stage 2 staging exited $LASTEXITCODE" }
git commit -m "test: migrate proven qualified-review matrices"
if ($LASTEXITCODE -ne 0) { throw "Stage 2 commit exited $LASTEXITCODE" }
git diff --quiet "${stage1Sha}..HEAD" -- @critical
if ($LASTEXITCODE -ne 0) { throw 'proof-critical files changed between Stage 1 and Stage 2' }
$committedPaths = @(git diff --name-only "${stage1Sha}..HEAD") | Sort-Object -Unique
if ($LASTEXITCODE -ne 0) { throw "Stage 2 committed-path acquisition exited $LASTEXITCODE" }
$committedPathDiff = @(Compare-Object ($expectedPaths | Sort-Object) $committedPaths)
if ($committedPathDiff) { throw "Stage 2 committed-path set is invalid: $($committedPathDiff | Out-String)" }
```

Expected: before commit, only the test module and receipt appear. If a proof-critical file appears, stop, restore selected full calls in a new commit, and repeat Stage 1 on the corrected surface.

### Task 7: Verify the final candidate and obtain exact-SHA reviews

**Files:**
- Review: complete branch diff from merge base through `HEAD`
- Review: `docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md`
- Do not create generated outputs in the repository

**Interfaces:**
- Produces: clean final equivalence output bound to the final SHA.
- Produces: two independent review results on the same final SHA, one specification and inventory review and one security and overclaiming review.

- [ ] **Step 1: Run the focused module and qualified-review shard**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_qualified_review_evidence -v
if ($LASTEXITCODE -ne 0) { throw "focused module exited $LASTEXITCODE" }
python tools/validate_test_shards.py --check
if ($LASTEXITCODE -ne 0) { throw "shard manifest validation exited $LASTEXITCODE" }
python tools/run_test_shards.py --shard qualified_review_evidence --durations 50
if ($LASTEXITCODE -ne 0) { throw "qualified-review shard exited $LASTEXITCODE" }
```

Expected: PASS. The shard still contains `tests/test_validate_qualified_review_evidence.py` and executes the migrated population plus retained integration coverage.

- [ ] **Step 2: Run complete unit and standalone validation**

```powershell
python tools/run_test_shards.py --all --durations 50
if ($LASTEXITCODE -ne 0) { throw "aggregate shards exited $LASTEXITCODE" }
python -m unittest discover -s tests -v --durations 50
if ($LASTEXITCODE -ne 0) { throw "full discovery exited $LASTEXITCODE" }
python tools/validate_assessment.py --check
if ($LASTEXITCODE -ne 0) { throw "assessment validation exited $LASTEXITCODE" }
python tools/validate_profiles.py --check
if ($LASTEXITCODE -ne 0) { throw "profile validation exited $LASTEXITCODE" }
python tools/validate_controls.py --check
if ($LASTEXITCODE -ne 0) { throw "control validation exited $LASTEXITCODE" }
python tools/validate_architectures.py
if ($LASTEXITCODE -ne 0) { throw "architecture validation exited $LASTEXITCODE" }
python tools/migrate_control_mappings.py --check
if ($LASTEXITCODE -ne 0) { throw "mapping migration check exited $LASTEXITCODE" }
python tools/validate_crosswalks.py --check
if ($LASTEXITCODE -ne 0) { throw "crosswalk validation exited $LASTEXITCODE" }
python tools/render_pci_dss_mapping_go_no_go.py --check
if ($LASTEXITCODE -ne 0) { throw "PCI DSS renderer check exited $LASTEXITCODE" }
python tools/release_gates.py --check
if ($LASTEXITCODE -ne 0) { throw "release gates exited $LASTEXITCODE" }
python tools/v05_beta_release_gates.py --check --baseline-ref origin/main
if ($LASTEXITCODE -ne 0) { throw "v0.5 beta gates exited $LASTEXITCODE" }
python tools/validate_links.py --check
if ($LASTEXITCODE -ne 0) { throw "link validation exited $LASTEXITCODE" }
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md
if ($LASTEXITCODE -ne 0) { throw "Mermaid inventory check exited $LASTEXITCODE" }
```

Expected: every command exits zero. Any defect found after `HEAD` changes requires affected gates to run again.

- [ ] **Step 3: Check whole-branch hygiene and run final exact-SHA equivalence**

```powershell
$mergeBase = git merge-base origin/main HEAD
if ($LASTEXITCODE -ne 0) { throw "merge-base resolution exited $LASTEXITCODE" }
git diff --check "$mergeBase..HEAD"
if ($LASTEXITCODE -ne 0) { throw "whole-branch diff check exited $LASTEXITCODE" }
$shortStatus = git status --short
if ($LASTEXITCODE -ne 0) { throw "git status exited $LASTEXITCODE" }
if ($shortStatus) { throw "final checkout is dirty: $shortStatus" }
$caches = Get-ChildItem -Recurse -Directory -Filter __pycache__
if ($caches) { throw 'generated Python cache exists' }
$candidate = git rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw "candidate resolution exited $LASTEXITCODE" }
$porcelain = git status --porcelain=v1 --untracked-files=all
if ($LASTEXITCODE -ne 0) { throw "porcelain status exited $LASTEXITCODE" }
if ($porcelain) { throw 'dirty final checkout' }
python -B tools/verify_qualified_review_hot_path_equivalence.py --check --candidate-sha $candidate
if ($LASTEXITCODE -ne 0) { throw "final equivalence exited $LASTEXITCODE" }
```

Expected: clean status and exact PASS output for 15 methods and 28 cases. Confirm the final inventory digest equals the Stage 1 receipt.

- [ ] **Step 4: Dispatch two independent reviews on the exact final SHA**

Use separate subagents. Give each the full SHA and merge base. The specification reviewer checks the 28-case inventory, 43-method ledger, digest, Stage 1 chronology, Stage 2 path boundary, and full/narrow/expected equality. The security reviewer checks first-failure order, acquisition ownership, alternate-commit facts, path and seal defenses, sanitization, structural guards, and absence of new caches or trusted snapshots.

Expected: both reviews name the same final SHA and report no unresolved Critical or Important finding. If a fix changes `HEAD`, commit it, rerun every affected gate and exact-SHA equivalence, then redispatch both reviews.

- [ ] **Step 5: Commit review repairs separately when needed**

```powershell
git add tests/qualified_review_policy_cases.py tests/qualified_review_hot_path_support.py tests/test_validate_qualified_review_evidence.py tools/validate_qualified_review_evidence.py tools/verify_qualified_review_hot_path_equivalence.py docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md
if ($LASTEXITCODE -ne 0) { throw "review repair staging exited $LASTEXITCODE" }
git commit -m "fix: address qualified-review hot-path review"
if ($LASTEXITCODE -ne 0) { throw "review repair commit exited $LASTEXITCODE" }
```

Expected: each repair is isolated and followed by fresh evidence. Do not amend the Stage 1 proof commit or the Stage 2 migration commit.

If a repair changes a proof-critical artifact, this ordinary repair step is not sufficient. Restore every selected complete call, commit and prove a new Stage 1 surface, then migrate again in a later Stage 2 commit before returning to final verification.

### Task 8: Publish, merge, and clean up

**Files:**
- Update: pull-request description only
- Remove after merge: temporary worktree and local feature branch

**Interfaces:**
- Consumes: the final reviewed SHA, Stage 1 proof SHA and digest, exact verifier outputs, validation results, and review dispositions.
- Produces: a merged pull request with passing required checks and a clean local `main`.

- [ ] **Step 1: Push the branch and open a reviewable pull request**

Use the humanizer skill in embedded mode for the title and body. Include scope, the 28-case and 31/61/92 detail-entry ledger, Stage 1 SHA and digest, final reviewed SHA, exact verifier outputs, retained full-path coverage, validation commands, review results, and the statement that Issue 55 remains open.

```powershell
$ErrorActionPreference='Stop'
$branch = git branch --show-current
if ($LASTEXITCODE -ne 0 -or -not $branch) { throw 'current branch resolution failed' }
$prBody = Join-Path ([System.IO.Path]::GetTempPath()) ("esaf-qualified-review-hot-path-$([guid]::NewGuid()).md")
$receipt = 'docs/superpowers/reviews/2026-08-07-qualified-review-hot-path-pre-migration-equivalence.md'
$stage1Matches = @(Select-String -Path $receipt -Pattern '^stage1_sha=([0-9a-f]{40})$')
if ($stage1Matches.Count -ne 1) { throw 'receipt shall contain exactly one stage1_sha field' }
$stage1Sha = $stage1Matches[0].Matches[0].Groups[1].Value
$candidate = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $candidate -notmatch '^[0-9a-f]{40}$') { throw 'candidate SHA resolution failed' }
$prText = @"
## Summary

- Moves all 28 selected qualified-review cases onto ordered production policy operations.
- Retains 61 baseline detail entries for schema, acquisition, role files, archives, seals, CLI behavior, and security defenses.
- Preserves Issue 55 and the real Draft campaign state.

## Proof

Stage 1 proof SHA: $stage1Sha

Final reviewed SHA: $candidate

The clean Stage 1 verifier compared the full, narrow, and expected projections for 28 cases before migration. The final verifier repeated those comparisons on the reviewed head with the same inventory digest. Focused, shard, discovery, standalone, Mermaid, and link gates passed on the final head. Independent specification and security reviews reported no unresolved Critical or Important finding.
"@
[System.IO.File]::WriteAllText(
  $prBody,
  $prText,
  [System.Text.UTF8Encoding]::new($false)
)
try {
  git push -u origin $branch
  if ($LASTEXITCODE -ne 0) { throw "git push exited $LASTEXITCODE" }
  $prUrl = gh pr create --base main --head $branch --title "Optimize qualified-review validation matrices" --body-file $prBody
  if ($LASTEXITCODE -ne 0) { throw "PR creation exited $LASTEXITCODE" }
  if ($prUrl -notmatch '^https://github\.com/') { throw 'PR creation returned no GitHub URL' }
  $prUrl
}
finally {
  if (Test-Path -LiteralPath $prBody) { Remove-Item -LiteralPath $prBody -Force }
}
```

Expected: the branch pushes and the PR is ready for review. Use a temporary file outside the repository for the body and remove it after creation.

- [ ] **Step 2: Wait for CI and verify the PR head**

```powershell
gh pr checks --watch
if ($LASTEXITCODE -ne 0) { throw "PR checks exited $LASTEXITCODE" }
$candidate = git rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw "candidate resolution exited $LASTEXITCODE" }
$prJson = gh pr view --json headRefOid,mergeable,reviewDecision,statusCheckRollup
if ($LASTEXITCODE -ne 0) { throw "PR inspection exited $LASTEXITCODE" }
$pr = $prJson | ConvertFrom-Json
if ($pr.headRefOid -ne $candidate) { throw "PR head $($pr.headRefOid) differs from reviewed $candidate" }
if ($pr.mergeable -ne 'MERGEABLE') { throw "PR mergeable state is $($pr.mergeable)" }
```

Expected: `headRefOid` equals the reviewed candidate, required checks pass, and the PR is mergeable. A changed head requires fresh affected validation, equivalence, and both reviews.

- [ ] **Step 3: Merge only the passing reviewed head**

```powershell
$candidate = git rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw "pre-merge candidate resolution exited $LASTEXITCODE" }
gh pr checks
if ($LASTEXITCODE -ne 0) { throw "pre-merge PR checks exited $LASTEXITCODE" }
$preMergeJson = gh pr view --json headRefOid,mergeable,statusCheckRollup
if ($LASTEXITCODE -ne 0) { throw "pre-merge PR inspection exited $LASTEXITCODE" }
$preMerge = $preMergeJson | ConvertFrom-Json
if ($preMerge.headRefOid -ne $candidate) { throw "pre-merge PR head $($preMerge.headRefOid) differs from reviewed $candidate" }
if ($preMerge.mergeable -ne 'MERGEABLE') { throw "pre-merge state is $($preMerge.mergeable)" }
gh pr merge --merge --delete-branch
$mergeExit = $LASTEXITCODE
$mergedJson = gh pr view --json state,mergedAt,mergeCommit
if ($LASTEXITCODE -ne 0) { throw "merged PR inspection exited $LASTEXITCODE" }
$merged = $mergedJson | ConvertFrom-Json
if ($merged.state -ne 'MERGED' -or -not $merged.mergedAt -or -not $merged.mergeCommit.oid) {
  throw "PR did not reach a verified merged state; merge exit was $mergeExit"
}
if ($mergeExit -ne 0) { Write-Warning "merge succeeded but branch cleanup exited $mergeExit" }
```

Expected: state is `MERGED` and a merge commit is present. If branch deletion warns because another worktree owns a branch, verify merge state before cleaning branches separately.

- [ ] **Step 4: Update local main and rerun proportional post-merge checks**

Run from `C:\Users\phrea\OneDrive\Documents\ESAF`:

```powershell
git switch main
if ($LASTEXITCODE -ne 0) { throw "switch to main exited $LASTEXITCODE" }
git pull --ff-only origin main
if ($LASTEXITCODE -ne 0) { throw "main fast-forward exited $LASTEXITCODE" }
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_qualified_review_evidence -v
if ($LASTEXITCODE -ne 0) { throw "post-merge focused module exited $LASTEXITCODE" }
python tools/validate_test_shards.py --check
if ($LASTEXITCODE -ne 0) { throw "post-merge shard validation exited $LASTEXITCODE" }
python tools/validate_qualified_review_evidence.py --help
if ($LASTEXITCODE -ne 0) { throw "qualified-review validator import exited $LASTEXITCODE" }
$mainStatus = git status --short
if ($LASTEXITCODE -ne 0) { throw "post-merge status exited $LASTEXITCODE" }
if ($mainStatus) { throw "main is dirty after merge: $mainStatus" }
```

Expected: PASS and a clean main worktree. The help command confirms the operational validator still imports without changing real evidence.

- [ ] **Step 5: Remove the temporary worktree and feature branch**

Resolve and verify the exact paths before removal:

```powershell
$ErrorActionPreference='Stop'
$repo = 'C:\Users\phrea\OneDrive\Documents\ESAF'
$worktree = 'C:\Users\phrea\OneDrive\Documents\ESAF\.worktrees\agent-validation-qualified-review-hot-path'
$repoFull = (Resolve-Path -LiteralPath $repo).Path
$worktreeFull = (Resolve-Path -LiteralPath $worktree).Path
$repoPrefix = $repoFull.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
if (-not $worktreeFull.StartsWith($repoPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Refusing to remove worktree outside repository: $worktreeFull"
}
Set-Location -LiteralPath $repoFull
git -C $repoFull worktree remove $worktreeFull
if ($LASTEXITCODE -ne 0) { throw "worktree removal exited $LASTEXITCODE" }
$localBranches = @(git -C $repoFull branch --format='%(refname:short)')
if ($LASTEXITCODE -ne 0) { throw "local branch listing exited $LASTEXITCODE" }
if ($localBranches -contains 'agent/validation-qualified-review-hot-path') {
  git -C $repoFull branch -d agent/validation-qualified-review-hot-path
  if ($LASTEXITCODE -ne 0) { throw "local branch deletion exited $LASTEXITCODE" }
}
git -C $repo worktree prune
if ($LASTEXITCODE -ne 0) { throw "worktree prune exited $LASTEXITCODE" }
$cleanupStatus = git -C $repo status --short
if ($LASTEXITCODE -ne 0) { throw "cleanup status exited $LASTEXITCODE" }
if ($cleanupStatus) { throw "main is dirty after cleanup: $cleanupStatus" }
```

Expected: the path guard passes, the temporary worktree and local branch are removed, and `main` remains clean.
