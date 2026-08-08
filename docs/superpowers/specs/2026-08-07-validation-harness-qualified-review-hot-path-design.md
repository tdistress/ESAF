# Validation harness qualified-review hot path design

**Date:** 2026-08-07
**Status:** Approved design
**Parent design:** `docs/superpowers/specs/2026-08-01-validation-harness-efficiency-design.md`
**Baseline commit:** `f99e403583877f803576dcad919025e558e5a5f6`
**Scope:** Qualified-review semantic policy, Final-to-Draft reference binding, mutation inventories, tests, and an opt-in equivalence tool

## Purpose

Reduce the cost of `tests/test_validate_qualified_review_evidence.py` without changing qualified-review policy or weakening campaign validation. Repeated semantic mutations shall exercise pure production boundaries over already parsed, immutable data. The complete validator shall retain every campaign, candidate, Draft, archive, and seal acquisition at its current decision point. The pure boundaries shall replace only the policy decisions interleaved with that work.

This is the qualified-review hot-path increment of validation-harness efficiency Phase 2. It does not alter a real review campaign, advance a mapping set from Draft, close Issue 55, or change any publication claim.

## Baseline and cost

The qualified-review shard contains 43 tests: one seal-destination acquisition test and 42 campaign-validation tests. Read-only control-flow analysis at the baseline commit counted 92 entries into the detailed campaign-validation path and 112 `copytree` operations. A copied campaign contains 749 files, so the test code requests about 83,888 file copies before filesystem metadata overhead.

A local validation of one complete valid Draft campaign took 27.234 seconds after fixture setup. The hosted `main` shard at the merged profile candidate completed in 175.741 seconds. These timings identify repeated work, but machine load, antivirus activity, filesystem location, and fixture state can change them. No elapsed-time value is a pass or fail condition.

Each complete campaign call can resolve Git state, validate the candidate schema, load candidate mappings, read six role-file pairs, check package and campaign allowlists, reconstruct packages, and build the deterministic archive. Final campaign validation also revalidates the retained Draft campaign. Those operations remain required when a test concerns acquisition, byte identity, path safety, or archive and seal integrity. They do not need to repeat for every mutation of an already parsed reviewer, finding, conclusion, or reference field.

## Invariants

The implementation shall preserve all of the following:

1. The same campaign inputs shall produce the same `ValidationReport`, including evidence validity, readiness name, readiness value, candidate commit, campaign identifier, error text, and error order.
2. The validator shall keep its current fail-closed distinction between content validation failures and operational evidence failures.
3. Candidate commits, schemas, mapping metadata, records, package bytes, role files, attestations, worksheets, manifests, archives, seals, and immutable locators shall remain bound to their current sources.
4. Actor identity normalization shall retain Unicode NFKC normalization, case folding, and the current letter-and-number comparison rule.
5. Reviewer eligibility, mapper independence, conflict disposition, dual-role acceptance, qualifications, conclusions, post-correction candidates, affected-record identifiers, finding severity and disposition, cross-role finding equality, authoritative finding equality, and reviewed-state reviewer metadata shall retain their current rules.
6. Final campaigns shall continue to require a distinct, valid, transition-ready Draft campaign and exact campaign, candidate, manifest, archive, and seal bindings.
7. Every existing security, acquisition, CLI, and error-classification test shall remain on the complete path.
8. The change shall not introduce a process-global cache, cross-call cache, path cache, fixture cache, mtime cache, or trusted caller-supplied validation result.

## Selected design

### One authoritative mutation inventory

`tests/qualified_review_policy_cases.py` shall be the only authoritative definition of the mutation cases moved to narrow production boundaries. It shall use frozen records and immutable tuples. A case shall contain:

- a stable case identifier and its baseline test-method name;
- the boundary family, either `role_readiness` or `draft_reference`;
- a declarative mutation over a named field in the valid baseline input;
- the exact expected report projection;
- the expected sanitized error tuple; and
- enough provenance to reconstruct the same mutation in a complete campaign fixture.

The expected report projection shall include evidence validity and readiness. It shall include candidate commit and campaign identifier whenever the complete report exposes parsed campaign context. Expected errors shall retain their current text and order.

The selected population is 31 cases across 16 test methods. Those cases currently cause 34 detailed-validation entries. The role and readiness boundary contains 27 cases and 27 entries across these 15 methods:

- `test_rejects_ineligible_reviewer_evidence`
- `test_actor_aliases_and_shared_locator_cannot_bypass_role_rules`
- `test_actor_alias_cannot_bypass_mapper_independence`
- `test_explicitly_resolved_conflict_is_eligible`
- `test_duplicate_human_requires_dual_acceptance_and_both_qualifications`
- `test_stop_with_open_high_severity_is_valid_but_not_ready`
- `test_accepted_critical_or_important_is_evidence_invalid`
- `test_pass_rejects_open_findings`
- `test_pass_after_correction_binds_exact_campaign_candidate`
- `test_orphan_affected_record_identifier_is_invalid_even_for_stop`
- `test_ready_findings_must_equal_authoritative_candidate_findings`
- `test_ready_findings_bind_authoritative_description`
- `test_duplicate_authoritative_finding_identifiers_are_invalid`
- `test_reviewed_candidate_requires_exact_nested_reviewer_objects`
- `test_final_pass_after_correction_binds_reviewed_candidate`

The Draft-reference inventory shall cover every field case in `test_final_campaign_binds_every_draft_reference_field`: campaign identifier, candidate commit, manifest digest, and seal-record digest. Valid Draft and Final campaigns remain representative full-path controls outside the 31-case inventory. The role and readiness inventory already contains valid narrow controls for resolved conflict and exact post-correction binding.

| Boundary | Selected cases | Current detailed-validation entries |
|---|---:|---:|
| Role and readiness policy | 27 | 27 |
| Final-to-Draft reference binding | 4 | 7 |
| **Selected total** | **31** | **34** |

The four reference cases have different recursive costs. Campaign identifier, manifest digest, and seal-record digest mutations each enter both the Final and retained Draft detail paths, for two entries per case. The candidate-commit mutation fails on the distinct-candidate rule before recursive Draft validation, for one entry. This gives seven detailed-validation entries across the four cases.

The 27 role and readiness records have this reviewed baseline distribution:

| Existing method | Cases |
|---|---:|
| `test_rejects_ineligible_reviewer_evidence` | 5 |
| `test_actor_aliases_and_shared_locator_cannot_bypass_role_rules` | 4 |
| `test_actor_alias_cannot_bypass_mapper_independence` | 1 |
| `test_explicitly_resolved_conflict_is_eligible` | 1 |
| `test_duplicate_human_requires_dual_acceptance_and_both_qualifications` | 2 |
| `test_stop_with_open_high_severity_is_valid_but_not_ready` | 2 |
| `test_accepted_critical_or_important_is_evidence_invalid` | 2 |
| `test_pass_rejects_open_findings` | 1 |
| `test_pass_after_correction_binds_exact_campaign_candidate` | 2 |
| `test_orphan_affected_record_identifier_is_invalid_even_for_stop` | 1 |
| `test_ready_findings_must_equal_authoritative_candidate_findings` | 1 |
| `test_ready_findings_bind_authoritative_description` | 1 |
| `test_duplicate_authoritative_finding_identifiers_are_invalid` | 1 |
| `test_reviewed_candidate_requires_exact_nested_reviewer_objects` | 2 |
| `test_final_pass_after_correction_binds_reviewed_candidate` | 1 |
| **Role and readiness total** | **27** |

The accepted-Minor mutations remain full stack because their missing named-acceptance fields fail the campaign schema before semantic policy runs. The missing-role mutation also remains a schema case. Duplicate role and duplicate mapping-set identifiers remain in the `_mapping_entries` topology path. The authoritative-description and duplicate-finding-identifier cases may use the narrow boundary only if their inventory records retain the alternate-commit authoritative candidate facts used by the complete baseline.

Before implementation replaces any complete validation call, a baseline ledger shall freeze this exact method set, its 31 expanded cases, per-method case counts, and 34 detailed-validation entries. That ledger shall account for all 92 measured detailed-validation entries as 34 selected and 58 retained. Each retained entry shall have a short reason tied to an invariant in this design. The selected population shall not silently absorb schema, topology, role-file parsing, source-set, locator, archive, seal, or CLI cases merely because they are expensive.

The inventory shall serialize its semantic fields as UTF-8 canonical JSON with sorted keys and separators `(',', ':')`, then check a reviewed SHA-256 digest stored beside the records. Validation shall fail for a missing or extra method, count drift, a duplicate identifier, an unknown boundary family, mutable case data, an unsupported mutation target, or a digest mismatch. Both the fast tests and the equivalence tool shall consume the same validating accessor. No generated copy or second expected-case table is permitted.

### Pure role and readiness policy boundary

`tools/validate_qualified_review_evidence.py` shall expose a narrow deterministic policy component over immutable, already parsed policy inputs. The production types may be private frozen dataclasses, but their responsibilities shall be explicit. The component shall provide pure staged operations for reviewer eligibility, role findings and conclusions, and mapping-set readiness and reviewed-state metadata.

```python
def validate_role_readiness_policy(
    stage: RolePolicyStage,
    policy_input: RolePolicyInput,
) -> RolePolicyResult:
    ...
```

Each mapping-set input shall contain only the data used by the current policy checks: reviewer identities and verification locators, eligibility flags, qualifications, conflict data, dual-role acceptance, conclusions, post-correction candidates, normalized findings, authoritative candidate findings, candidate mapper identities, candidate record identifiers, and reviewed-state reviewer metadata.

The function shall not accept paths, readers, open files, mutable mappings, package assemblies, raw Markdown, raw JSON bytes, or caller assertions that external evidence has been checked. A stage shall return only the immutable state needed by the next policy stage or raise the same sanitized `_ValidationFailure` at the same rule boundary as the current implementation. The combined narrow test adapter may run all stages over one complete immutable input, but it shall not reimplement any rule.

The complete validator shall retain ownership of campaign and schema parsing, candidate acquisition, role-key checks, role-file loading, attestation and worksheet equality, source-set binding, digest and locator checks, snapshot collection, and allowlist construction. It shall call the pure stages at the same points where the current rules run. Reviewer eligibility remains before that reviewer's role-file binding. Finding and conclusion policy remains after those files bind. Authoritative finding equality and reviewed-state reviewer metadata remain after both roles. This staged routing preserves first-failure order when one campaign contains more than one defect.

### Pure Final-to-Draft reference boundary

The second production boundary shall compare a parsed Final reference with immutable facts obtained from Draft validation. It shall support named stages so the wrapper can preserve the current order of reference checks, archive comparison, seal reading, and seal reconstruction:

```python
def validate_draft_reference_binding(
    check: DraftReferenceCheck,
) -> None:
    ...
```

Each `DraftReferenceCheck` shall be a frozen record for one named stage and the values available at that point. After recursive validation, the validated Draft facts include phase, readiness result, campaign identifier, candidate commit, and manifest SHA-256. The seal stage adds the digest computed from the retained seal bytes. The boundary shall enforce the current distinct-candidate rule, the Draft phase and transition-readiness requirements, and exact equality for all four reference fields. The narrow test adapter may run all applicable stages over immutable facts without reading external files.

The boundary shall not locate a Draft worktree, recursively validate a campaign, read retained artifacts, hash external paths, parse a seal, reconstruct an archive, or build expected seal bytes. The production wrapper shall call the distinct-candidate stage before recursive Draft validation. After recursive validation, it shall run the Draft phase, readiness, campaign, candidate, and manifest stages in their current order. It shall then compare the retained archive with deterministic reconstruction on the complete path. After reading the seal bytes, it shall pass the computed digest to the seal-reference stage before parsing and reconstructing the seal. Canonical seal JSON, archive locator, validator version, seal contents, and deterministic reconstruction remain full stack. This ordering preserves the current first failure when a campaign has multiple defects.

### Production routing before migration

The first implementation stage shall make the complete validator use both new boundaries while every existing test still follows its current route. `_validate_roles_and_readiness()` may become an acquisition-and-binding wrapper, but it shall no longer contain a second implementation of semantic policy. `_validate_draft_reference()` may become a retained-artifact wrapper, but it shall delegate the reference comparisons to the pure binding function.

Tests shall enforce this routing structurally. Production wrappers shall import or call the narrow functions, and the inventory and fast matrix modules shall not contain copied policy logic. The pure functions shall not import filesystem, subprocess, Git, archive, seal, schema, or test-fixture modules.

## Migration chronology and equivalence proof

The branch history shall preserve two separate, observable stages.

### Stage 1: pre-migration equivalence commit

The first stage shall add the final digest-bound inventory, both production boundaries, production routing, focused boundary tests, and the opt-in equivalence tool. Existing exhaustive methods shall still call the complete validator. This stage shall be committed before any of those calls are replaced.

On that clean commit, `tools/verify_qualified_review_hot_path_equivalence.py` shall run every selected inventory case through three independent routes:

1. apply the declarative mutation to a fresh complete fixture and call the production campaign validator;
2. apply the same mutation to a fresh immutable baseline input and call the applicable narrow production boundary; and
3. load the expected report projection from the inventory.

The full, narrow, and expected projections shall be exactly equal. Equality includes validity, readiness, campaign context where applicable, sanitized message text, and message order. Empty error tuples and the role-policy positive controls are part of the proof.

The verifier shall accept only a full lowercase 40-character candidate SHA. It shall require the supplied SHA to equal `HEAD` and require `git status --porcelain=v1 --untracked-files=all` to be empty. Successful output shall report the candidate SHA, method count, population count, population digest, full comparison count, narrow comparison count, and `equivalence=PASS`.

The pull-request record shall identify this pre-migration commit, preserve the successful verifier output, and show that the inventory digest at that commit equals the digest used by the later fast tests. A later edit to the inventory or either boundary invalidates the proof and requires a new pre-migration proof commit before migration continues.

### Stage 2: matrix migration commit

Only after Stage 1 passes may a later commit replace the selected complete validation calls with narrow policy evaluation. The fast tests shall consume every inventory record exactly once. Each record shall run each applicable ordered operation once through a shared production adapter. The tests shall fail if they call `validate_campaign()`, `_validate_campaign_details()`, the recursive Final wrapper, or a test-owned policy implementation.

The opt-in verifier shall remain after migration and shall run again on the clean final candidate. The final run checks that the inventory, production routing, fixture adapter, and narrow tests still describe the same behavior after test replacement. The branch diff and commit order shall prove that equivalence preceded migration rather than being reconstructed after the old path was removed.

## Full-path coverage retained

The complete campaign path shall remain mandatory for:

- manifest structure, missing or duplicate roles, duplicate mapping-set keys, and schema behavior;
- candidate commit resolution, candidate schema validation, network-reference rejection, Git object failures, and worktree boundaries;
- package, attestation, worksheet, and immutable-locator digest bindings;
- attestation source sets, exact source versions, Markdown parsing, JSON parsing, and source-file equality;
- package and campaign allowlists, extension rules, case-insensitive collisions, extra files, payload mutations, and deterministic snapshots;
- valid Draft transition readiness and valid recursive Final merge readiness;
- retained Draft archive equality, archive mutation, Draft byte mutation, seal mutation, archive locator checks, canonical seal JSON, and deterministic seal reconstruction;
- all CLI argument, output, exit-code, sanitization, permission, operational-error, and content-error cases;
- seal publication atomicity, destination anchoring, unsafe paths, execution-state drift, competing output, cleanup, ancestor swaps, and exact byte snapshots.

At least one full-path integration test shall exercise each pure boundary with a valid Draft campaign. Final integration shall also exercise a valid recursively checked Final campaign. Representative invalid integrations shall cover mapper aliasing, reviewer ineligibility, a stop conclusion, an authoritative-finding mismatch, a reviewed-state reviewer mismatch, and one Final-to-Draft reference mismatch. The retained opt-in verifier covers all four reference fields through the complete path. These integration tests may overlap existing retained methods. They shall not use test-only shortcuts to claim that acquisition occurred.

## Error handling and compatibility

The pure boundaries shall operate only on immutable values and shall not catch operational exceptions because they perform no I/O. Their policy failures shall use the existing sanitized messages. The surrounding wrappers shall retain current parsing, acquisition, normalization, and operational-error translation.

The validator CLI, report schema, seal format, deterministic archive, evidence manifest, and campaign schema do not change. The qualified-review shard manifest and GitHub Actions workflow do not need edits unless implementation reveals a completeness defect unrelated to timing.

No optimization may reuse a prior secure snapshot, validated Draft result, candidate mapping, archive, or seal across mutable test calls. Existing caches are outside this increment and shall not be widened. This design removes irrelevant repetitions from semantic matrices; it does not make secure acquisition cheaper.

## Alternatives considered

### Invocation-scoped acquisition caches

A cache limited to one top-level Final validation could reuse candidate or Draft data during recursive checks. The validator's correctness depends on exact worktree, object, and retained-artifact state at the time of each acquisition. A new cache would broaden the proof surface and would not address repeated fixture copies between independent test cases. This increment does not add one.

### Test-only fixture memoization

Tests could memoize a valid report or reuse one mutable campaign tree. That would make the suite faster, but it would test the memoization layer rather than the production policy. It would also make case isolation and mutation cleanup harder to audit. The selected design keeps fresh immutable policy inputs and preserves fresh complete fixtures wherever acquisition is under test.

### Broad campaign-validator rewrite

The complete validator could be split into many stages at once. That would touch schema loading, candidate acquisition, file binding, archive construction, and error translation in one increment. Two narrow policy seams provide the useful test boundary without redesigning the evidence pipeline.

## Verification

Implementation shall follow a red, green, refactor sequence:

1. Add tests for the baseline ledger, selected and retained accounting, expanded inventory, uniqueness, immutability, and digest.
2. Add focused tests for the role/readiness and Draft-reference boundaries, including exact messages and readiness results.
3. Route complete production validation through both boundaries while existing campaign tests remain unchanged.
4. Commit the complete Stage 1 state and run the equivalence tool on that clean exact SHA.
5. Record the Stage 1 SHA, inventory digest, counts, and successful output in the pull-request evidence.
6. Replace only the proven semantic and reference matrix calls, then add structural guards against full validation and copied policy logic.
7. Run the equivalence tool again on the clean final candidate SHA.
8. Run the focused module, qualified-review shard, shard-manifest tests, complete discovery, affected standalone validators, Mermaid rendering, link validation, and whole-branch hygiene checks.

Independent review shall inspect the complete branch diff and its commit order. It shall verify that the selected case population did not shrink, the final inventory digest matches the pre-migration proof, every retained full-path case still reaches production acquisition, and no mutable cache or trusted snapshot shortcut was added.

## Acceptance criteria

This increment is accepted when:

1. The baseline ledger accounts for all 43 tests, all 92 detailed-validation calls, and every selected or retained mutation case at the baseline commit.
2. One validated, digest-bound inventory is the source for the pre-migration proof, final fast tests, and retained equivalence tool.
3. Complete production validation routes policy decisions through both pure boundary families at the current ordered decision points, while acquisition and binding stay in the surrounding wrappers.
4. A clean pre-migration commit proves exact full, narrow, and expected equivalence for the final inventory digest before a later commit replaces any complete matrix call.
5. The final fast tests consume every selected record once, evaluate only the applicable narrow production operations, and preserve all expected report and error behavior.
6. The retained equivalence tool passes again on the clean final candidate and reports the exact SHA, population counts, digest, and comparison totals.
7. Path, link, digest, role-file, source-set, package, allowlist, archive, seal, CLI, operational, and security cases remain full stack and pass.
8. The valid Draft and recursively validated Final campaigns still report transition readiness and merge readiness exactly as before.
9. Complete validation passes on the exact candidate with no new generated cache or build output.
10. Independent review finds no unresolved Critical or Important issue.

Timing may be reported after deterministic gates pass, but it is diagnostic only. The hosted Phase 2 target remains open until the bundle mutation-matrix increment lands and three successful hosted full-suite runs provide the final measurement.

## Non-goals

- Changing reviewer eligibility, independence, conflict, dual-role, finding, conclusion, readiness, or Final-to-Draft reference policy.
- Changing diagnostic strings, report fields, deterministic ordering, CLI output, or exit codes.
- Reducing the mutation population or replacing exhaustive cases with samples.
- Moving acquisition, parsing, byte binding, path defense, archive reconstruction, seal reconstruction, or operational-error handling into a pure seam.
- Reusing a mutable validation result, secure snapshot, candidate object, Draft validation, archive, or seal across calls.
- Optimizing mapping-review bundle mutation matrices in this increment.
- Closing Issue 55, advancing Draft mapping sets, or declaring the Phase 2 performance target complete.
