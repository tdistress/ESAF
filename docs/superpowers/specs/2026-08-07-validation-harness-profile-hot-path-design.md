# Validation harness profile hot path design

**Date:** 2026-08-07
**Status:** Approved design
**Parent design:** `docs/superpowers/specs/2026-08-01-validation-harness-efficiency-design.md`
**Baseline commit:** `df124e13a7b4a377524c50e73358234425913e72`
**Scope:** Profile language cases, tests, diagnostic boundaries, and the opt-in equivalence tool

## Purpose

Reduce the cost of the profile validation test module without removing any language case or weakening the complete repository validation path. Exhaustive phrase, voice, aspect, polarity, and framing matrices shall exercise the same production text diagnostics used by `validate()`. Representative integration tests shall continue through package discovery, loading, schema validation, authoritative-source comparison, traceability, source-boundary validation, claim validation, and diagnostic normalization.

This is the profile hot-path increment of validation-harness efficiency Phase 2. It does not change profile policy, accepted language, diagnostic text, or validator behavior.

## Baseline and cost

On current `main` at `df124e13a7b4a377524c50e73358234425913e72`, the complete suite ran 205 tests in 416.717 seconds and reported five Windows symlink privilege skips. The slowest profile language-matrix methods took 5.6 to 9.7 seconds each. Each of those methods issued 28 to 46 calls to the complete `validate()` path.

The suite baseline came from a clean Windows worktree at that commit with bytecode generation disabled:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest discover -s tests -v
```

The method counts below come from an instrumented run of `python -m unittest -v tests.test_validate_profiles` at the same commit. The measurement counted calls to `validate_profiles.validate()` and successful unittest subtests without changing case inputs or validator behavior. The authoritative measurement inventory has SHA-256 `eea29c38bb90f4837d41674512e4dd001047d76c2de7d1d89445c831a58d0486`.

Most cases change only README prose. A complete call still rediscovers the profile inventory, reads and validates every package component, loads schemas and control records, compares authoritative Markdown and derived JSON, checks traceability, and repeats filesystem defenses. Those operations remain necessary for integration coverage, but they do not need to run once for every grammatical variation.

## Migration population

The selected population is exactly 73 test methods. At the baseline commit, they made 995 complete `validate()` calls and completed 1,564 successful subtests.

| Method | `validate()` calls | Successful subtests |
|---|---:|---:|
| `test_additional_assurance_claim_forms_are_rejected` | 5 | 5 |
| `test_additional_assurance_denials_and_discussion_are_allowed` | 6 | 6 |
| `test_additional_control_weakening_forms_are_rejected` | 6 | 6 |
| `test_additional_weakening_denials_and_discussion_are_allowed` | 5 | 5 |
| `test_affirmative_claim_after_denied_clause_is_rejected` | 2 | 2 |
| `test_affirmative_weakening_after_denial_is_rejected` | 2 | 2 |
| `test_approval_subject_voice_and_aspect_cross_product` | 24 | 24 |
| `test_assurance_voice_tense_and_aspect_grammar_matrix` | 20 | 20 |
| `test_bounded_adverb_slots_cross_product` | 35 | 35 |
| `test_common_affirmative_control_weakening_is_rejected` | 16 | 16 |
| `test_common_affirmative_profile_claim_variants_are_rejected` | 30 | 30 |
| `test_contrast_clause_boundaries_do_not_mask_prohibited_language` | 18 | 18 |
| `test_declared_generic_authority_passive_aspect_cross_product` | 9 | 8 |
| `test_direct_weakening_object_and_complement_are_bounded` | 2 | 2 |
| `test_dynamic_authority_bounded_adverb_cross_product` | 19 | 19 |
| `test_establishes_profile_claim_denials_are_allowed` | 3 | 3 |
| `test_establishes_profile_claim_quotations_are_allowed` | 3 | 3 |
| `test_establishes_profile_claim_variants_are_rejected` | 3 | 3 |
| `test_excluded_source_supply_and_derivation_are_rejected` | 8 | 8 |
| `test_excluded_source_supply_and_derivation_polarity_pairs` | 20 | 20 |
| `test_explicit_control_weakening_denials_are_allowed` | 18 | 18 |
| `test_extended_polarity_and_metalinguistic_matrix` | 11 | 11 |
| `test_final_review_claim_assertions_are_rejected` | 9 | 9 |
| `test_final_review_claim_polarity_and_clause_pairs` | 28 | 28 |
| `test_identified_excluded_source_supply_forms_are_rejected` | 2 | 2 |
| `test_identified_excluded_source_supply_polarity_pairs` | 8 | 8 |
| `test_later_metalinguistic_discussion_does_not_mask_assertions` | 3 | 3 |
| `test_mapping_direction_and_authority_grammar_matrix` | 13 | 13 |
| `test_mapping_direction_form_and_aspect_cross_product` | 38 | 38 |
| `test_metalinguistic_context_is_bounded_to_the_assertion` | 4 | 4 |
| `test_natural_perfect_mandatory_denial_and_discussion_pairs` | 18 | 18 |
| `test_natural_perfect_mandatory_placement_cross_product` | 4 | 4 |
| `test_negated_rejection_head_cross_product` | 12 | 12 |
| `test_negation_binding_complement_and_insertion_cross_product` | 7 | 7 |
| `test_negative_modifiers_remain_polarity_cross_product` | 9 | 9 |
| `test_new_control_weakening_quotations_are_allowed` | 12 | 12 |
| `test_new_profile_claim_denials_are_allowed` | 18 | 18 |
| `test_new_profile_claim_quotations_and_discussion_are_allowed` | 44 | 22 |
| `test_omit_skip_and_reduce_control_forms_are_rejected` | 11 | 11 |
| `test_omit_skip_and_reduce_polarity_pairs` | 15 | 15 |
| `test_passive_affirmative_control_weakening_is_rejected` | 8 | 8 |
| `test_passive_control_weakening_denials_are_allowed` | 8 | 8 |
| `test_passive_control_weakening_quotations_are_allowed` | 8 | 8 |
| `test_polarity_is_bound_to_the_assertion_head` | 2 | 0 |
| `test_postposed_denial_agent_vs_rhetorical_cross_product` | 9 | 9 |
| `test_postposed_denial_and_rejection_polarity_cross_product` | 17 | 17 |
| `test_postposed_denial_complement_boundary_cross_product` | 30 | 30 |
| `test_postposed_possessive_rhetorical_suffix_cross_product` | 16 | 16 |
| `test_postposed_terminal_and_qualified_denial_cross_product` | 12 | 12 |
| `test_profile_specific_claim_denials_are_allowed` | 7 | 7 |
| `test_profile_specific_claim_quotations_are_allowed` | 8 | 8 |
| `test_profile_specific_positive_claims_are_rejected` | 4 | 4 |
| `test_readiness_confirmation_requires_positive_establishment` | 2 | 2 |
| `test_reordered_mapping_and_general_authority_are_rejected` | 4 | 4 |
| `test_reordered_mapping_and_general_authority_denials_are_allowed` | 4 | 4 |
| `test_second_review_claim_word_order_polarity_pairs` | 16 | 16 |
| `test_second_review_claim_word_orders_are_rejected` | 4 | 4 |
| `test_second_review_direct_weakening_forms_are_rejected` | 2 | 2 |
| `test_second_review_direct_weakening_polarity_pairs` | 8 | 8 |
| `test_source_authority_after_denied_clause_is_rejected` | 2 | 0 |
| `test_source_authority_denials_and_discussion_are_allowed` | 4 | 4 |
| `test_source_boundary_rejects_excluded_authority_claims` | 2 | 2 |
| `test_third_review_bounded_nonweakening_semantic_variations` | 4 | 4 |
| `test_third_review_excluded_source_supply_aspect_and_voice` | 20 | 20 |
| `test_third_review_passive_aspect_claim_families` | 30 | 30 |
| `test_third_review_progressive_direct_weakening_forms` | 20 | 20 |
| `test_third_review_readiness_explicit_denial_family` | 11 | 10 |
| `test_unrelated_denial_does_not_mask_later_control_weakening` | 2 | 2 |
| `test_weakening_aspect_and_state_cross_product` | 24 | 24 |
| `test_weakening_aspect_denial_and_metalinguistic_pairs` | 13 | 13 |
| `test_weakening_cross_product_denials_and_claim_frames` | 17 | 17 |
| `test_weakening_state_grammar_matrix` | 24 | 24 |
| `test_weakening_subject_modal_and_state_cross_product` | 46 | 46 |
| **Selected total** | **995** | **1,564** |

The readiness methods belong in the selected population because they test prohibited-claim polarity. The mapping, approval, and assurance methods test prohibited-claim or source-authority prose. `test_polarity_is_bound_to_the_assertion_head` and `test_source_authority_after_denied_clause_is_rejected` each exercise two independent cases without using `subTest`, which explains their zero successful-subtest counts.

The original measured population contained 78 methods, 1,010 `validate()` calls, and 1,577 successful subtests. These five exclusions account for the remaining 15 calls and 13 successful subtests:

| Excluded method | `validate()` calls | Successful subtests | Rationale |
|---|---:|---:|---|
| `test_recommended_selection_rejects_mandatory_synonyms` | 3 | 3 | Tests structured control-selection rationale modality, not a claim, weakening, or source-authority classifier. |
| `test_risk_source_basis_must_resolve` | 2 | 2 | Tests risk `source_basis` reference resolution and integrity, which remain in the source-boundary wrapper. |
| `test_risk_source_basis_accepts_controls_and_permitted_sources` | 2 | 2 | Tests the risk `source_basis` allowlist and reference behavior, not narrative source-authority language. |
| `test_malformed_control_catalog_is_a_sanitized_content_failure` | 6 | 6 | Tests malformed catalog parsing, CLI content-failure behavior, and path sanitization. |
| `test_cli_reports_unresolvable_schema_reference_with_exit_two` | 2 | 0 | Tests schema reference resolution, operational-error sanitization, and CLI exit code 2. |
| **Excluded total** | **15** | **13** | |

## Invariants

The implementation shall preserve all of the following:

1. Every existing input phrase and every voice, tense, aspect, polarity, framing, complement, insertion, conjunction, modifier, and dynamic-source combination.
2. The exact accepted or rejected disposition of each case.
3. Existing diagnostic text, repository-relative locations, deduplication, and deterministic sort order.
4. JSON traversal and location reporting for every structured narrative field.
5. README scanning and `PROFILE.md` scanning after authoritative JSON blocks are removed.
6. Dynamic matching against the profile's declared `excluded_sources`.
7. Full validation coverage for inventory, schemas, filesystem boundaries, symlinks and junctions, package identity, authoritative-source integrity, control population, semantic rules, traceability, CLI behavior, exit codes, and sanitized operational errors.
8. The distinction between content diagnostics and operational failures.

The change shall not add a process-global cache, path cache, fixture cache, mtime cache, or any cache whose correctness depends on mutable test files. It shall not add timing assertions.

## Selected design

### Authoritative case inventory

`tests/profile_language_cases.py` shall be the only authoritative definition of the migrated language population. It shall contain frozen case records and the compact phrase tables and product builders needed to expand all 995 baseline validation inputs. Each expanded `ProfileLanguageCase` shall contain:

- the exact selected test-method name and a unique stable case identifier;
- the input text and complete repository-relative diagnostic location;
- the applicable diagnostic family, either claim, source authority, or both;
- an immutable tuple of excluded sources; and
- the exact expected sorted diagnostic tuple.

The module shall also contain the 73-method baseline ledger from this design, including each method's `validate()` call count and successful-subtest count, the five exclusions and their counts, and the selected and original totals. It shall expand to exactly 995 unique case records grouped under exactly the 73 selected method names. Per-method expanded case counts shall equal the baseline `validate()` call counts.

The module shall serialize the expanded semantic case fields as UTF-8 canonical JSON with sorted object keys and separators `(',', ':')`, then compute their SHA-256 digest. A reviewed expected digest constant in the same module shall bind the compact builders to the expanded population. Inventory validation shall fail on a digest mismatch, a missing or extra method, a count mismatch, a duplicate method and case identifier, an unknown diagnostic family, mutable excluded-source data, or unsorted or duplicate expected diagnostics.

Both `tests/test_validate_profiles.py` and the retained equivalence harness shall import this module and call its validating accessor. The fast tests shall request cases by their own method name and consume every returned case once. No second case table, generated checked-in copy, or independently maintained digest is permitted. An intentional population change requires a separately reviewed update to the case definitions, baseline ledger, expected digest, and this design's population record.

### Two production text-diagnostic boundaries

`tools/validate_profiles.py` shall expose two narrow deterministic functions:

```python
from collections.abc import Sequence


def claim_text_diagnostics(text: str, location: str) -> list[str]:
    ...


def source_authority_text_diagnostics(
    text: str,
    location: str,
    excluded_sources: Sequence[str],
) -> list[str]:
    ...
```

`location` is the complete repository-relative diagnostic prefix. For Markdown it is the file path. For a JSON string it is the file path followed by the existing document location. The boundary functions shall not read files, discover packages, parse JSON, load schemas, resolve controls, or mutate inputs.

`claim_text_diagnostics()` shall apply the existing `contains_affirmative_weakening()` and `asserted_profile_phrases()` rules. It shall return the current control-weakening and prohibited-assertion messages with the supplied location.

`source_authority_text_diagnostics()` shall freeze the supplied sequence as an unmodified tuple, then apply the existing `contains_affirmative_source_authority()` rule to that snapshot. It shall return the current prohibited source-authority message with the supplied location.

Each function shall return a sorted, deduplicated list. This keeps the production wrappers' current externally visible order and gives matrix tests the same diagnostic contract as the complete validator. The lower-level Boolean and phrase helpers remain implementation details. Matrices shall test the diagnostic boundary rather than assembling expected behavior from those helpers.

### Production wrapper adoption

`claim_diagnostics()` shall retain ownership of package traversal, prohibited structured-field checks, UTF-8 handling, Markdown reads, and authoritative JSON block removal. For every narrative string it shall construct the existing location and extend its results with `claim_text_diagnostics()`. Its final sorted, deduplicated return remains unchanged.

`source_boundary_diagnostics()` shall retain ownership of risk `source_basis` resolution, package traversal, excluded-source extraction, UTF-8 handling, Markdown reads, and authoritative JSON block removal. It shall pass every narrative string and its existing location to `source_authority_text_diagnostics()`. Its final sorted, deduplicated return remains unchanged.

`validate()` shall keep its current order of semantic, authoritative-source, traceability, source-boundary, and claim checks. No other validator layer moves into the text functions.

## Test migration

### Equivalence before replacement

Migration shall proceed in two observable stages.

First, every matrix case selected for the hot path shall run through both routes:

1. write the case to the same fixture location and call complete `validate()`;
2. call the applicable production text-diagnostic boundary with the same text, diagnostic location, and excluded-source list; and
3. compare the exact diagnostic lists, including message text and order.

Affirmative cases, direct denials, postposed denials, quotations, rejected-claim frames, metalinguistic discussion, active and passive voice, simple and perfect aspects, bounded adverbs, pronoun and named-source forms, and dynamic excluded-source cases shall all pass this equivalence stage. A mismatch blocks migration.

After the complete moved population passes, the exhaustive language matrices shall call only the applicable text-diagnostic boundaries. The compact phrase tables may move into the authoritative inventory, but their values and product dimensions shall not change. The expanded semantic case records shall remain identical. The implementation shall not consolidate, delete, sample, or rewrite cases to obtain the speedup.

The final tests shall enforce the migration structurally. Exhaustive matrix helpers shall fail if they invoke `validate()`, and each case shall invoke each applicable production text boundary exactly once. These are deterministic call-count assertions, not elapsed-time assertions.

### Retained exact-candidate equivalence harness

`tools/verify_profile_hot_path_equivalence.py` shall retain the full comparison after migration. It is an opt-in candidate gate, not part of unittest discovery, the default profile shard, or the ordinary GitHub Actions shard workflow. Run it explicitly on the final review candidate:

```powershell
$candidate = git rev-parse HEAD
python -B tools/verify_profile_hot_path_equivalence.py --check --candidate-sha $candidate
```

The command shall accept only a full lowercase 40-character SHA. It shall require that SHA to equal the verified `HEAD` commit and shall require `git status --porcelain=v1 --untracked-files=all` to be empty. A detached checkout is allowed when it is clean and its `HEAD` equals the supplied SHA. These checks bind the result to committed files at one exact candidate rather than to a mutable working tree.

The harness shall load the validated inventory from `tests/profile_language_cases.py`. For each of its 995 records, it shall create the specified valid fixture state, apply the record's README text and excluded-source tuple, and compare three exact lists: complete `validate()` output, the sorted union of the applicable production text-diagnostic outputs, and the case record's expected diagnostics. This includes empty results, repository-relative locations, message text, deduplication, and order. It shall not use a separately encoded expected-case table.

Successful output shall report these stable fields:

```text
candidate_sha=<40-character-lowercase-SHA>
method_count=73
population_count=995
population_sha256=<64-character-lowercase-SHA-256>
equivalence=PASS
```

The population digest is the digest recomputed and checked by the authoritative inventory module. Missing cases, inventory drift, dirty state, candidate mismatch, fixture setup failure, full-validator failure, narrow-boundary failure, or any exact comparison mismatch shall exit nonzero. A comparison failure shall identify the stable method and case identifiers and show the differing repository-relative diagnostic lists without exposing a temporary host path.

This command shall run once after the implementation reaches its final SHA and again after any candidate change that can affect the validator, case inventory, fixture, or test migration. Its elapsed time may be recorded for diagnosis, but duration never determines pass or fail.

### Full-path coverage retained

Complete `validate()` tests shall remain for representative examples of:

- affirmative, negative, and metalinguistic claim language in README content;
- affirmative, negative, and metalinguistic excluded-source authority language;
- a generic authority named dynamically in `excluded_sources`;
- `PROFILE.md` prose scanning with authoritative JSON blocks stripped before text diagnostics;
- narrative strings and prohibited keys nested in structured JSON components;
- exact diagnostic ordering and deduplication when semantic and language errors coexist;
- risk source-basis resolution and permitted-source behavior;
- malformed and duplicate JSON, schema failures, missing or unexpected package entries, unsafe paths, files replaced by directories, symlinks, junctions, and repository-boundary checks;
- package inventory, identity, authoritative control population, mapping references, lifecycle semantics, and traceability; and
- CLI success, content-error exit one, operational-error exit two, UTF-8 failures, permission failures, resolution failures, and host-path sanitization.

Two small integration methods outside the 73-method migration inventory shall make README and structured-JSON coverage explicit. `test_text_diagnostics_reach_full_validate_for_readme` shall cover affirmative, negative, and metalinguistic claim and source-authority text, including a dynamically declared generic exclusion. `test_text_diagnostics_reach_full_validate_for_structured_json` shall cover both diagnostic families with existing JSON document locations. The existing `test_authoritative_markdown_prose_is_claim_scanned` and `test_authoritative_markdown_prose_respects_source_boundary` shall retain the `PROFILE.md` source-stripping path. These integration methods shall use complete `validate()` and shall not be consumed by the fast case inventory.

Existing focused tests that already call `claim_diagnostics()` or another narrow helper may remain when they test structured traversal or a lower-level grammar rule. Only exhaustive language matrices that repeatedly call the complete validator are candidates for replacement.

## Error handling and compatibility

The text boundaries are pure classification and formatting functions. They shall not catch or translate filesystem, decoding, schema, inventory, or operational errors because they perform none of those operations. The package wrappers retain the current error behavior.

The excluded-source sequence shall be snapshotted at function entry and shall not be mutated or retained after return. The source-authority function shall not derive exclusions from ambient repository state. Tests may reuse an immutable tuple across matrix cases, but production shall continue to read the sequence from each loaded profile.

The existing profile validator CLI and evidence format do not change. `python tools/validate_profiles.py --check` shall produce the same output and exit status for the same repository tree before and after the refactor. The new equivalence command is a development and review tool, not a profile validation mode.

## Alternatives considered

### Reusable fixture template

A prebuilt valid profile tree could be copied or cloned for each test. This may reduce setup work for tests that construct a fresh package, but the slow matrices already reuse one fixture inside a method. Their dominant cost is the repeated complete validation call after each one-line mutation. A template also creates a new fixture-integrity boundary around copied files, links, permissions, and mutable state. It is secondary to removing work that is unrelated to the rule under test.

### Validation-call-scoped parsing caches

A cache limited to one `validate()` call could avoid a few repeated reads or parses without creating cross-call stale-state risk. It would not help the dominant pattern because each matrix case starts a new validation call. The validator already needs most package data once per complete call, so the available saving is smaller and touches broader production code. Call-scoped parsing may be considered separately if later profiling identifies repeated work within one invocation.

Cross-call and process-global caches are rejected. The tests deliberately mutate files between calls, and any cache keyed by path, timestamp, or ambient repository state would create a stale-validation risk.

## Verification

Development shall use a red, green, refactor sequence:

1. Add the authoritative case inventory and focused tests for its exact method set, counts, expansion, uniqueness, and digest.
2. Add focused tests for the two diagnostic boundaries and their exact output order.
3. Route production wrappers through the new boundaries while all existing tests still use their current paths.
4. Run every selected case through both the narrow and complete paths and prove exact equivalence.
5. Replace complete calls only in the proven methods, consume the shared inventory from the fast matrices, and add deterministic guards against regression to full validation.
6. Run the retained equivalence command on the clean exact candidate SHA.
7. Run the focused profile module, the profile shard, complete discovery, standalone validators affected by profiles or references, and whole-branch hygiene checks.

The implementation review shall compare the complete branch diff and verify that matrix inputs and product dimensions have not changed. Any behavior change requires a separate design and is outside this increment.

## Acceptance criteria

This increment is accepted when:

1. `tests/profile_language_cases.py` validates exactly 73 selected methods, 995 expanded cases, the reviewed population digest, the recorded per-method baseline counts, and the five exclusions.
2. Production claim and source-authority wrappers use the same two text-diagnostic functions exercised by the migrated matrices.
3. Every moved case has first produced an exact narrow-path and full-path equivalence result.
4. The final exhaustive matrices consume the authoritative case inventory once, preserve every existing case, and issue no complete `validate()` calls.
5. The retained opt-in equivalence command passes on the clean exact candidate SHA and reports that SHA, method count, population count, population digest, and `equivalence=PASS`.
6. Representative full-path tests cover README, stripped `PROFILE.md`, structured JSON, dynamic excluded sources, affirmative, negative, and metalinguistic language.
7. Filesystem, security, schema, inventory, authoritative-source, traceability, CLI, ordering, and error-sanitization tests remain on the complete path and pass.
8. Focused and complete validation passes on the exact candidate SHA with no new generated cache or build output.
9. Independent review finds no unresolved Critical or Important issue.

Timing data may be reported after the deterministic gates pass, but it is diagnostic only. The hosted Phase 2 target of at least a 40 percent reduction from the 751-second median remains open until the qualified-review and bundle mutation-matrix increments have landed. The final decision shall use three successful hosted full-suite runs after all Phase 2 increments are present.

## Non-goals

- Changing claim, weakening, source-authority, or metalinguistic recognition.
- Changing any diagnostic string, location, ordering, or exit code.
- Reducing the language population or replacing exhaustive matrices with samples.
- Moving structural JSON-field or risk source-basis rules into text diagnostics.
- Caching mutable repository or fixture state across validation calls.
- Optimizing the qualified-review or bundle mutation matrices in this increment.
- Declaring the Phase 2 performance target complete from a local run or this increment alone.
