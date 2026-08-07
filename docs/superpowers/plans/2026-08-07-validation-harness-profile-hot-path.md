# Validation harness profile hot path implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move all 908 profile language cases onto two pure production diagnostic boundaries while retaining exact full-validator equivalence, representative integration coverage, and a clean-candidate equivalence gate.

**Architecture:** A frozen inventory in `tests/profile_language_cases.py` will own the complete migrated population, its baseline ledger, and a reviewed semantic digest. The first stage will keep all 73 selected test methods on `validate()` while production wrappers adopt `claim_text_diagnostics()` and `source_authority_text_diagnostics()` and the opt-in verifier proves exact equivalence. Only that proof permits the second stage, where the 73 methods use the narrow boundaries and two focused integration methods preserve README and structured JSON coverage through the complete validator.

**Tech Stack:** Python 3.13, `unittest`, `dataclasses`, `hashlib`, canonical UTF-8 JSON, `unittest.mock`, `argparse`, Git CLI, PowerShell, and the repository's manifest-defined test shard runner.

## Global Constraints

- Implement the tasks sequentially. Do not assign overlapping inventory, validator, fixture, or test edits to parallel implementers.
- Preserve all 908 exact validation inputs from the 73 selected methods. Do not consolidate, sample, rewrite, or delete a phrase, product dimension, voice, tense, aspect, polarity, frame, complement, insertion, conjunction, modifier, or dynamic-source case.
- Keep the baseline provenance exact: 73 selected methods, 908 `validate()` calls, and 880 successful subtests; 78 repeated-call methods, 923 calls, and 893 successful subtests; five excluded methods, 15 calls, and 13 successful subtests.
- Preserve the excluded-source distribution exactly: `()` has 772 records, `('UK GDPR',)` has 87, `('Acme Code',)` has 28, `('UK GDPR', 'Cyber Essentials')` has 13, and `('UK GDPR', 'NCSC', 'Cyber Essentials')` has 8. Exactly 136 records have a nonempty tuple.
- Every migrated case targets `profiles/uk/0.1.0/README.md` and stores its method name, stable case identifier, exact input text, complete repository-relative location, diagnostic families, immutable excluded-source tuple, and exact sorted diagnostic tuple.
- Preserve current diagnostic text, repository-relative locations, deduplication, deterministic ordering, accepted and rejected dispositions, JSON traversal, `PROFILE.md` authoritative-block stripping, dynamic excluded-source matching, CLI behavior, exit codes, and operational-error sanitization.
- Keep inventory, schema, filesystem boundary, symlink, junction, package identity, authoritative-source, control population, semantic, traceability, risk source-basis, UTF-8, permission, and resolution tests on the complete validation path.
- Do not add a process-global cache, path cache, fixture cache, mtime cache, or any cache whose correctness depends on mutable test files.
- Do not add elapsed-time assertions. Record timings only after deterministic correctness gates pass.
- Keep `tools/test-shards.json` unchanged. Equivalence-tool tests belong in `tests/test_validate_profiles.py`, and the opt-in tool must not enter unittest discovery, the default profile shard, or the ordinary GitHub Actions workflow.
- Set `PYTHONDONTWRITEBYTECODE=1` for Python validation commands. Confirm that no `__pycache__` directories or build outputs remain before every exact-SHA equivalence run and final handoff.
- The approved design baseline is `df124e13a7b4a377524c50e73358234425913e72`. Bind equivalence and final review evidence to the actual full lowercase 40-character candidate `HEAD`, never to the design baseline or an abbreviated SHA.
- A change after an equivalence run invalidates that run. Commit the repair, obtain a clean new candidate SHA, rerun the equivalence tool, rerun every affected gate, and repeat both exact-SHA reviews.
- Use `shall`, `should`, and `may` with their repository meanings in documentation and evidence. This increment changes no profile policy, accepted language, diagnostic string, or normative ESAF content.

## File map

- Create `tests/profile_language_cases.py`: frozen records, compact phrase tables, product builders, the 73-method ledger, five exclusions, canonical digest calculation, validation, grouping, and the only authoritative migrated case population.
- Modify `tests/profile_fixture.py`: shared deterministic writers for README and JSON fixture mutations, including authoritative `PROFILE.md` regeneration after every profile manifest change.
- Modify `tests/test_validate_profiles.py`: inventory contract tests, the full-path inventory stage, narrow-boundary and wrapper tests, equivalence CLI tests, the final fast matrix class, structural consumption guards, and representative full-path integration methods.
- Modify `tools/validate_profiles.py`: two pure text-diagnostic functions and production wrapper adoption without changing `validate()` ordering or error ownership.
- Create `tools/verify_profile_hot_path_equivalence.py`: opt-in clean-candidate comparison of the full path, narrow path, and authoritative expected diagnostics for every record.
- Verify without editing `tools/test-shards.json`: `tests/test_validate_profiles.py` remains the only module in `profile_validation`.

---

### Task 1: Establish the authoritative inventory while every selected method still calls `validate()`

**Files:**
- Create: `tests/profile_language_cases.py`
- Modify: `tests/profile_fixture.py:38-65`
- Modify: `tests/test_validate_profiles.py:1-3769`
- Test: `tests/test_validate_profiles.py`

**Interfaces:**
- Produces: `DiagnosticFamily = Literal["claim", "source_authority"]`.
- Produces: frozen `ProfileLanguageCase(method_name: str, case_id: str, text: str, location: str, diagnostic_families: tuple[DiagnosticFamily, ...], excluded_sources: tuple[str, ...], expected_diagnostics: tuple[str, ...])`.
- Produces: frozen `MethodBaseline(method_name: str, validate_calls: int, successful_subtests: int)` and `ExcludedMethodBaseline(method_name: str, validate_calls: int, successful_subtests: int, rationale: str)`.
- Produces: frozen `ProfileLanguageInventory(cases: tuple[ProfileLanguageCase, ...], methods: tuple[MethodBaseline, ...], exclusions: tuple[ExcludedMethodBaseline, ...], population_sha256: str)` with `cases_for_method(method_name: str) -> tuple[ProfileLanguageCase, ...]`.
- Produces: `validate_profile_language_inventory(cases: Sequence[ProfileLanguageCase], methods: Sequence[MethodBaseline], exclusions: Sequence[ExcludedMethodBaseline], expected_sha256: str) -> ProfileLanguageInventory` for strict validation and focused mutation tests.
- Produces: `profile_language_inventory() -> ProfileLanguageInventory`, the validating accessor used by tests and the later equivalence tool.
- Produces: `profile_language_population_sha256(cases: Sequence[ProfileLanguageCase]) -> str`, which serializes semantic fields as canonical UTF-8 JSON with `sort_keys=True`, `ensure_ascii=False`, and `separators=(",", ":")`.
- Produces: `profile_fixture.write_profile_readme(package: Path, text: str) -> str` and `profile_fixture.write_component(package: Path, filename: str, document: object) -> None`.
- Preserves: all 73 selected unittest method names. At this stage each method delegates to `_assert_language_cases_through_full_validate(method_name: str) -> None` and still invokes `validate_profiles.validate()` once per record.

- [ ] **Step 1: Add failing inventory contract tests**

Add `ProfileLanguageInventoryTests` to `tests/test_validate_profiles.py`. Import `dataclasses.replace` and `tests.profile_language_cases`. Require the validating accessor to return exactly 73 method rows, 908 unique records, the exact method order below, and the exact excluded-source distribution from Global Constraints. Require every `location` to equal `profiles/uk/0.1.0/README.md`, every `excluded_sources` and `expected_diagnostics` value to be a tuple, every expected tuple to equal `tuple(sorted(set(expected)))`, and every family tuple to contain only `claim` or `source_authority`.

The normative method ledger is:

| Method | Calls | Successful subtests |
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

Add mutation tests that call the inventory validator with one defect at a time: a missing and extra method, wrong per-method count, duplicate ledger method, duplicate case identifier, unknown family, list-valued `excluded_sources`, unsorted expected diagnostics, duplicate expected diagnostics, wrong distribution, and a one-character text change with a stale digest. Assert a distinct, deterministic `ValueError` message for each mutation.

Require these five exclusions and totals verbatim:

```python
(
    ExcludedMethodBaseline(
        "test_recommended_selection_rejects_mandatory_synonyms", 3, 3,
        "Tests structured control-selection rationale modality, not a claim, weakening, or source-authority classifier.",
    ),
    ExcludedMethodBaseline(
        "test_risk_source_basis_must_resolve", 2, 2,
        "Tests risk source_basis reference resolution and integrity, which remain in the source-boundary wrapper.",
    ),
    ExcludedMethodBaseline(
        "test_risk_source_basis_accepts_controls_and_permitted_sources", 2, 2,
        "Tests the risk source_basis allowlist and reference behavior, not narrative source-authority language.",
    ),
    ExcludedMethodBaseline(
        "test_malformed_control_catalog_is_a_sanitized_content_failure", 6, 6,
        "Tests malformed catalog parsing, CLI content-failure behavior, and path sanitization.",
    ),
    ExcludedMethodBaseline(
        "test_cli_reports_unresolvable_schema_reference_with_exit_two", 2, 0,
        "Tests schema reference resolution, operational-error sanitization, and CLI exit code 2.",
    ),
)
```

- [ ] **Step 2: Run the inventory tests and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_profiles.ProfileLanguageInventoryTests -v
```

Expected: FAIL because `tests.profile_language_cases`, its frozen records, and its validating accessor do not exist.

- [ ] **Step 3: Add failing fixture synchronization tests**

Test `write_profile_readme()` with `"This profile establishes compliance."` and require the exact returned and written content `"# Synthetic profile\n\nThis profile establishes compliance.\n"`. Test `write_component()` with `profile.json` after assigning `source_boundary.excluded_sources = ["Acme Code"]`; require two-space JSON indentation, one terminal newline, UTF-8 round-trip, and a regenerated `PROFILE.md` block containing the same exclusion. Then assign an empty list through the same helper and prove that neither file retains `Acme Code`.

- [ ] **Step 4: Run the fixture tests and verify RED**

```powershell
python -m unittest tests.test_validate_profiles.ProfileFixtureWriterTests -v
```

Expected: FAIL because the shared README and component writers are absent.

- [ ] **Step 5: Implement the deterministic fixture writers**

Add these functions to `tests/profile_fixture.py` and make the existing test-case methods delegate to them:

```python
def write_profile_readme(package: Path, text: str) -> str:
    content = f"# Synthetic profile\n\n{text}\n"
    (package / "README.md").write_text(content, encoding="utf-8")
    return content


def write_component(package: Path, filename: str, document: object) -> None:
    write_json(package / filename, document)
    write_authoritative_source(package)
```

Do not make either helper cache content. `write_component()` must regenerate `PROFILE.md` even when the incoming excluded-source list is empty.

- [ ] **Step 6: Move the exact case builders and records into the new inventory**

Move the selected methods' phrase constants, exact tuples, and `itertools.product` dimensions out of `tests/test_validate_profiles.py` and into `tests/profile_language_cases.py` without editing string values or loop order. Build stable IDs as `<method-name-without-test_>-<one-based-index-padded-to-three-digits>` after each method's cases have expanded in the original execution order. Store the exact README body text, not the synthetic Markdown header. Store `diagnostic_families` as `("claim",)`, `("source_authority",)`, or `("claim", "source_authority")` in that order.

For each record, encode the exact complete diagnostics, including the location prefix. Empty cases use `()`. Examples that establish the representation are:

```python
ProfileLanguageCase(
    method_name="test_profile_specific_positive_claims_are_rejected",
    case_id="profile_specific_positive_claims_are_rejected-001",
    text="This profile is legally sufficient.",
    location="profiles/uk/0.1.0/README.md",
    diagnostic_families=("claim",),
    excluded_sources=(),
    expected_diagnostics=(
        "profiles/uk/0.1.0/README.md: prohibited assertion 'legal sufficiency'",
    ),
)

ProfileLanguageCase(
    method_name="test_source_boundary_rejects_excluded_authority_claims",
    case_id="source_boundary_rejects_excluded_authority_claims-001",
    text="UK GDPR is the authority for this profile selection.",
    location="profiles/uk/0.1.0/README.md",
    diagnostic_families=("source_authority",),
    excluded_sources=("UK GDPR",),
    expected_diagnostics=(
        "profiles/uk/0.1.0/README.md: prohibited source authority language",
    ),
)
```

Include the complete 73-row ledger and five-row exclusion ledger in this module. Validate record shape, method membership, per-method counts, selected and repeated-call totals, exclusions, distribution, uniqueness, family vocabulary, tuple immutability, expected-order invariants, and the digest every time `profile_language_inventory()` runs.

- [ ] **Step 7: Bind the builders to a reviewed digest**

Start `EXPECTED_POPULATION_SHA256` at `"0" * 64` so the digest test fails. Use this one-off command to print the independently recomputed canonical digest without bypassing any case builder:

```powershell
python -B -c "from tests.profile_language_cases import PROFILE_LANGUAGE_CASES, profile_language_population_sha256; print(profile_language_population_sha256(PROFILE_LANGUAGE_CASES))"
```

Expected: one lowercase 64-character SHA-256. Review the expanded record count, per-method counts, source distribution, representative empty and nonempty expected tuples, first and last stable IDs, and all string diffs against the original 73 method bodies. Copy the printed digest verbatim into `EXPECTED_POPULATION_SHA256`; do not derive the expected constant inside the accessor or test.

- [ ] **Step 8: Route all 73 methods through the shared inventory and complete validator**

Add this test helper to `ProfileValidationTests`:

```python
def _assert_language_cases_through_full_validate(self, method_name: str) -> None:
    inventory = profile_language_cases.profile_language_inventory()
    cases = inventory.cases_for_method(method_name)
    self.assertEqual(
        len(cases),
        next(
            item.validate_calls
            for item in inventory.methods
            if item.method_name == method_name
        ),
    )
    for case in cases:
        with self.subTest(case_id=case.case_id):
            profile_fixture.write_profile_readme(self.package, case.text)
            profile = self.load_component("profile.json")
            profile["source_boundary"]["excluded_sources"] = list(
                case.excluded_sources
            )
            profile_fixture.write_component(
                self.package, "profile.json", profile
            )
            self.assertEqual(
                validate_profiles.validate(self.root),
                list(case.expected_diagnostics),
            )
```

Replace each selected method body with one call that passes its own literal method name. Keep all 73 names and keep them in `ProfileValidationTests` for this stage. Remove each migrated local phrase table only after its final consumer has moved. Do not touch the five excluded methods or any one-call integration, schema, filesystem, CLI, sanitization, or lower-level grammar test.

- [ ] **Step 9: Run the inventory, fixture, and complete full-path population**

```powershell
python -m unittest tests.test_validate_profiles.ProfileLanguageInventoryTests tests.test_validate_profiles.ProfileFixtureWriterTests -v
python -m unittest tests.test_validate_profiles.ProfileValidationTests -v --durations 50
```

Expected: PASS. The second command reports all original `ProfileValidationTests` methods, and the 73 selected methods account for exactly 908 calls to `validate()` through the shared inventory. No narrow text boundary exists yet.

- [ ] **Step 10: Review and commit the observable full-path inventory stage**

```powershell
git diff --check
git add tests/profile_language_cases.py tests/profile_fixture.py tests/test_validate_profiles.py
git diff --cached --stat
git diff --cached
git commit -m "test: centralize profile language cases"
```

Checkpoint: the commit contains one authoritative case population, a reviewed digest, and synchronized excluded-source fixture writes, but all 908 selected records still exercise full `validate()`.

---

### Task 2: Add the two pure production text-diagnostic boundaries

**Files:**
- Modify: `tools/validate_profiles.py:2704-3033`
- Modify: `tests/test_validate_profiles.py`
- Test: `tests/test_validate_profiles.py`

**Interfaces:**
- Consumes: existing `contains_affirmative_weakening(text: str) -> bool`, `asserted_profile_phrases(text: str) -> list[str]`, and `contains_affirmative_source_authority(text: str, excluded_sources: list[str]) -> bool` behavior.
- Produces: `claim_text_diagnostics(text: str, location: str) -> list[str]`.
- Produces: `source_authority_text_diagnostics(text: str, location: str, excluded_sources: Sequence[str]) -> list[str]`.
- Preserves: lower-level Boolean and phrase helpers as implementation details and leaves both package wrappers unchanged until Task 3.

- [ ] **Step 1: Write failing exact-output boundary tests**

Add `ProfileTextDiagnosticBoundaryTests` without a filesystem fixture. Cover an affirmative weakening, one claim that yields multiple assertion labels, denial, quotation, metalinguistic discussion, an affirmative excluded-source authority claim, a direct source denial, and an empty exclusion tuple. Require exact repository-relative lists and exact sorting. Use repeated claim text that would append the same diagnostic twice and require one result.

Add a mutable input test:

```python
def test_source_authority_boundary_snapshots_excluded_sources(self) -> None:
    excluded_sources = ["Acme Code"]
    with mock.patch.object(
        validate_profiles,
        "contains_affirmative_source_authority",
        return_value=True,
    ) as classifier:
        diagnostics = validate_profiles.source_authority_text_diagnostics(
            "Acme Code governs this profile selection.",
            "profiles/uk/0.1.0/README.md",
            excluded_sources,
        )
        excluded_sources.append("Later mutation")
    classifier.assert_called_once_with(
        "Acme Code governs this profile selection.", ("Acme Code",)
    )
    self.assertEqual(
        diagnostics,
        [
            "profiles/uk/0.1.0/README.md: prohibited source authority language"
        ],
    )
```

Patch `Path.read_text`, package discovery, JSON loading, and schema loading to raise if called, then invoke both boundaries and prove that they perform no I/O or ambient repository lookup.

- [ ] **Step 2: Run the boundary tests and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_profiles.ProfileTextDiagnosticBoundaryTests -v
```

Expected: FAIL because both public text-diagnostic functions are absent.

- [ ] **Step 3: Implement only classification and diagnostic formatting**

Add the exact signatures from the approved design. Build claim results from the existing weakening Boolean and asserted phrase list. Freeze source inputs before classification. Return `sorted(set(diagnostics))` from each function.

```python
def claim_text_diagnostics(text: str, location: str) -> list[str]:
    diagnostics: list[str] = []
    if contains_affirmative_weakening(text):
        diagnostics.append(
            f"{location}: prohibited control weakening language"
        )
    for phrase in asserted_profile_phrases(text):
        diagnostics.append(
            f"{location}: prohibited assertion {phrase!r}"
        )
    return sorted(set(diagnostics))


def source_authority_text_diagnostics(
    text: str,
    location: str,
    excluded_sources: Sequence[str],
) -> list[str]:
    frozen_sources = tuple(excluded_sources)
    diagnostics: list[str] = []
    if contains_affirmative_source_authority(text, frozen_sources):
        diagnostics.append(
            f"{location}: prohibited source authority language"
        )
    return sorted(set(diagnostics))
```

Update only the lower helper's type annotations needed to accept the frozen sequence. Do not move file reads, traversal, source-basis checks, decoding behavior, schema work, or error translation into either function.

- [ ] **Step 4: Run focused tests and the still-full-path inventory**

```powershell
python -m unittest tests.test_validate_profiles.ProfileTextDiagnosticBoundaryTests tests.test_validate_profiles.ProfileLanguageInventoryTests -v
python -m unittest tests.test_validate_profiles.ProfileValidationTests -v --durations 50
```

Expected: PASS. The new functions have exact isolated behavior, while all 908 selected records still run through `validate()` and do not call the new functions through production wrappers yet.

- [ ] **Step 5: Commit the pure boundaries**

```powershell
git diff --check
git add tools/validate_profiles.py tests/test_validate_profiles.py
git diff --cached
git commit -m "refactor: expose profile text diagnostics"
```

---

### Task 3: Route production wrappers through the new boundaries

**Files:**
- Modify: `tools/validate_profiles.py:3034-3155`
- Modify: `tests/test_validate_profiles.py`
- Test: `tests/test_validate_profiles.py`

**Interfaces:**
- Consumes: both Task 2 boundary functions.
- Preserves: `source_boundary_diagnostics(package: ProfilePackage, controls: set[str]) -> list[str]`, `claim_diagnostics(package: ProfilePackage) -> list[str]`, and `validate(root: Path = ROOT) -> list[str]` signatures.
- Preserves: `validate()` check order: semantic, authoritative source, traceability, source boundary, then claims.

- [ ] **Step 1: Add failing wrapper-routing tests**

Use a loaded synthetic package and insert unique marker strings into `profile.json`, `risk-overlays.json`, README, and prose outside the authoritative JSON blocks in `PROFILE.md`. Patch each Task 2 boundary with a wrapper and assert calls with the complete existing location:

```python
mock.call("README marker", "profiles/uk/0.1.0/README.md")
mock.call(
    "Structured marker",
    "profiles/uk/0.1.0/profile.json: document.scope",
)
```

For the source wrapper, assert the third argument is the exact tuple declared in the loaded profile. Assert the `PROFILE.md` call excludes authoritative JSON block contents. Return duplicate sentinel diagnostics from the patched boundary and require each wrapper's final result to remain sorted and deduplicated.

Keep separate focused tests proving that `source_boundary_diagnostics()` still owns unresolved risk `source_basis` errors and that `claim_diagnostics()` still owns prohibited structural fields. Keep the existing malformed UTF-8 tests on their current package wrappers.

- [ ] **Step 2: Run wrapper tests and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_profiles.ProfileDiagnosticWrapperRoutingTests -v
```

Expected: FAIL because the wrappers still invoke the lower-level classifiers directly, so the boundary spies receive no calls.

- [ ] **Step 3: Adopt the boundaries without moving wrapper responsibilities**

In each JSON traversal, build the current location first and extend the wrapper list with the relevant boundary output. For Markdown, read UTF-8 exactly as before, strip authoritative JSON blocks only for `source`, and call the boundary with the existing path-only location. Leave risk basis checks, prohibited-key checks, decode handling, and final `sorted(set(diagnostics))` in their current wrappers.

Do not alter `validate()` or the order in which it extends diagnostic groups.

- [ ] **Step 4: Run focused routing, error, CLI, and all 908 full-path cases**

```powershell
python -m unittest tests.test_validate_profiles.ProfileDiagnosticWrapperRoutingTests -v
python -m unittest tests.test_validate_profiles.ProfileValidationTests.test_malformed_readme_encoding_is_a_content_failure tests.test_validate_profiles.ProfileValidationTests.test_component_permission_error_is_operational_and_sanitized tests.test_validate_profiles.ProfileValidationTests.test_component_resolution_error_is_operational_and_sanitized tests.test_validate_profiles.ProfileValidationTests.test_inventory_permission_error_is_operational_and_sanitized tests.test_validate_profiles.ProfileValidationTests.test_cli_reports_unresolvable_schema_reference_with_exit_two -v
python -m unittest tests.test_validate_profiles.ProfileValidationTests -v --durations 50
```

Expected: PASS. The selected population now reaches the two new boundaries through `validate()`, and operational failures remain sanitized with their existing exit status.

- [ ] **Step 5: Commit wrapper adoption**

```powershell
git diff --check
git add tools/validate_profiles.py tests/test_validate_profiles.py
git diff --cached
git commit -m "refactor: route profile wrappers through text diagnostics"
```

Checkpoint: production and matrix paths share the same text functions, but the 73 selected methods still invoke complete validation.

---

### Task 4: Build and run the retained exact-candidate equivalence tool

**Files:**
- Create: `tools/verify_profile_hot_path_equivalence.py`
- Modify: `tests/test_validate_profiles.py`
- Verify only: `tools/test-shards.json`
- Test: `tests/test_validate_profiles.py`

**Interfaces:**
- Consumes: `profile_language_cases.profile_language_inventory()`, `profile_fixture.write_valid_profile_fixture()`, `profile_fixture.write_profile_readme()`, `profile_fixture.write_component()`, both production text boundaries, and complete `validate()`.
- Produces: frozen `EquivalenceResult(candidate_sha: str, method_count: int, population_count: int, population_sha256: str)`.
- Produces: sanitized `ProfileHotPathEquivalenceError`.
- Produces: `require_exact_candidate(root: Path, candidate_sha: str, runner: Callable[..., subprocess.CompletedProcess[bytes]] = subprocess.run) -> None`.
- Produces: `verify_profile_hot_path_equivalence(root: Path, candidate_sha: str) -> EquivalenceResult`.
- Produces: `main(argv: Sequence[str] | None = None, *, root: Path = ROOT) -> int` and CLI `python -B tools/verify_profile_hot_path_equivalence.py --check --candidate-sha <full-sha>`.

- [ ] **Step 1: Write failing candidate-binding and CLI tests**

Add `ProfileHotPathEquivalenceCommandTests` to `tests/test_validate_profiles.py`; do not add a new test module. With an injected binary subprocess runner, require these exact Git calls with `cwd=root`, `shell=False`, `capture_output=True`, and no text decoding by the child:

```python
["git", "rev-parse", "--verify", "HEAD"]
["git", "status", "--porcelain=v1", "--untracked-files=all"]
```

Test an uppercase SHA, abbreviated SHA, all-zero unavailable SHA, HEAD mismatch, nonzero Git result, nonempty stderr, dirty tracked state, and an untracked file. Every failure must be nonzero and omit injected absolute paths and child stderr. Test a clean detached checkout response with matching HEAD and require acceptance.

Test `main()` success with a patched verification result and require these exact five lines in this order:

```text
candidate_sha=1111111111111111111111111111111111111111
method_count=73
population_count=908
population_sha256=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
equivalence=PASS
```

- [ ] **Step 2: Run candidate and CLI tests and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_profiles.ProfileHotPathEquivalenceCommandTests -v
```

Expected: FAIL because the tool module and interfaces do not exist.

- [ ] **Step 3: Write failing comparison and fixture-reset tests**

Use a small injected inventory containing one empty exclusion, one `("Acme Code",)` exclusion, and one following empty exclusion under two method names. Patch the fixture constructor, full validator, and text boundaries so the test can record operations without running the full repository validator. Require:

- one fresh `TemporaryDirectory` and valid fixture per method;
- README reset before every record;
- a fresh `profile.json` read before every record;
- assignment from `list(case.excluded_sources)` for every record, including both empty records;
- `write_component()` and authoritative-source regeneration before every full validation;
- one full validation call per record;
- one call to each applicable boundary per record and no call to an inapplicable boundary;
- independent equality of full output, sorted narrow union, and expected tuple; and
- stable method and case identifiers in a mismatch without the temporary root.

Add separate mismatches for full versus narrow, full versus expected, narrow versus expected, wrong order, duplicate diagnostics, and a leaked absolute temporary path. Each mismatch must exit nonzero and print sanitized repository-relative evidence only.

- [ ] **Step 4: Run comparison tests and verify RED**

```powershell
python -m unittest tests.test_validate_profiles.ProfileHotPathEquivalenceComparisonTests -v
```

Expected: FAIL because per-method fresh fixtures, per-case state reset, and three-way exact comparison are absent.

- [ ] **Step 5: Implement the opt-in verifier**

Validate the candidate syntax with `re.fullmatch(r"[0-9a-f]{40}", candidate_sha)`. Require exact `HEAD` bytes and an empty porcelain status before creating any fixture. Call the inventory's validating accessor once.

For each method ledger row, create a new temporary root and valid package. For every case in that method, execute this order:

```python
readme = profile_fixture.write_profile_readme(package, case.text)
profile_path = package / "profile.json"
profile = json.loads(profile_path.read_text(encoding="utf-8"))
profile["source_boundary"]["excluded_sources"] = list(
    case.excluded_sources
)
profile_fixture.write_component(package, "profile.json", profile)
full = validate_profiles.validate(fixture_root)
narrow: list[str] = []
if "claim" in case.diagnostic_families:
    narrow.extend(
        validate_profiles.claim_text_diagnostics(readme, case.location)
    )
if "source_authority" in case.diagnostic_families:
    narrow.extend(
        validate_profiles.source_authority_text_diagnostics(
            readme, case.location, case.excluded_sources
        )
    )
narrow = sorted(set(narrow))
expected = list(case.expected_diagnostics)
```

Compare `full`, `narrow`, and `expected` independently. Before reporting any list, reject diagnostics containing the resolved temporary root or its slash-normalized form. Catch inventory, fixture, Git, JSON, operational validator, and unexpected failures at `main()` and print one concise sanitized error with exit 1. Do not print a traceback, child stderr, environment value, or host path.

- [ ] **Step 6: Run tool unit tests, the profile module, and the shard manifest check**

```powershell
python -m unittest tests.test_validate_profiles.ProfileHotPathEquivalenceCommandTests tests.test_validate_profiles.ProfileHotPathEquivalenceComparisonTests -v
python -m unittest tests.test_validate_profiles -v --durations 50
python tools/validate_test_shards.py --check
git diff -- tools/test-shards.json
```

Expected: PASS; the manifest still assigns only `tests/test_validate_profiles.py` to `profile_validation`, and the final Git diff command prints nothing.

- [ ] **Step 7: Commit the verifier, then run it on the clean full-path stage**

```powershell
git diff --check
git add tools/verify_profile_hot_path_equivalence.py tests/test_validate_profiles.py
git diff --cached
git commit -m "test: retain profile hot path equivalence gate"
$candidate = git rev-parse HEAD
if ($candidate -notmatch '^[0-9a-f]{40}$') { throw "Invalid candidate SHA: $candidate" }
$status = git status --porcelain=v1 --untracked-files=all
if ($status) { throw "Dirty full-path candidate: $($status -join ', ')" }
$elapsed = Measure-Command {
  python -B tools/verify_profile_hot_path_equivalence.py --check --candidate-sha $candidate
  if ($LASTEXITCODE -ne 0) { throw "Full-path equivalence failed" }
}
$elapsed.TotalSeconds
```

Expected: the command prints the exact committed candidate SHA, `method_count=73`, `population_count=908`, the reviewed inventory digest, and `equivalence=PASS`. Record the elapsed seconds as diagnostic evidence. Do not start Task 5 if any comparison fails.

Checkpoint: this clean commit is the required first observable equivalence stage. All 908 matrix cases still use `validate()` in unittest, and the retained tool has independently compared full, narrow, and expected lists.

---

### Task 5: Switch the proven matrices to narrow boundaries and retain representative integration

**Files:**
- Modify: `tests/test_validate_profiles.py`
- Test: `tests/test_validate_profiles.py`

**Interfaces:**
- Consumes: `ProfileLanguageInventory.cases_for_method()`, `claim_text_diagnostics()`, and `source_authority_text_diagnostics()`.
- Produces: `ProfileLanguageMatrixTests._assert_profile_language_cases(method_name: str) -> None`.
- Produces: `profile_fixture.profile_readme_content(text: str) -> str`, the shared pure formatter used by the file writer, fast matrices, and equivalence tool.
- Produces: exactly 73 methods on `ProfileLanguageMatrixTests`, each requesting inventory records by its own literal method name.
- Produces: `ProfileValidationTests.test_text_diagnostics_reach_full_validate_for_readme()` and `ProfileValidationTests.test_text_diagnostics_reach_full_validate_for_structured_json()` outside the inventory.
- Preserves: `test_authoritative_markdown_prose_is_claim_scanned()` and `test_authoritative_markdown_prose_respects_source_boundary()` on full `validate()`.

- [ ] **Step 1: Add failing structural guards before changing the matrix helper**

Add `ProfileLanguageMatrixStructureTests` that compares the selected inventory method tuple with the exact `test_*` methods defined directly on `ProfileLanguageMatrixTests`. Parse each method's source with `ast` and require one call to `_assert_profile_language_cases()` whose sole argument is the method's own literal name. Reject direct or indirect references to `_assert_language_cases_through_full_validate`, `validate_profiles.validate`, fixture paths, README writes, JSON writes, or lower-level Boolean and phrase helpers.

Add a call-count guard that runs the inventory through `_assert_profile_language_cases()` with `validate_profiles.validate` patched to raise `AssertionError("fast language matrices shall not call validate")`, and both text boundaries wrapped with mocks. For each method, require:

```python
claim_calls = sum(
    "claim" in case.diagnostic_families for case in cases
)
source_calls = sum(
    "source_authority" in case.diagnostic_families for case in cases
)
```

Assert exact mock counts and an exact once-only sequence of consumed case IDs. Do not use timing in these tests.

- [ ] **Step 2: Run structural guards and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_profiles.ProfileLanguageMatrixStructureTests -v
```

Expected: FAIL because the selected methods still live on the fixture-backed full-validator class and call `_assert_language_cases_through_full_validate()`.

- [ ] **Step 3: Add the two representative full-path integration methods**

In `ProfileValidationTests`, add `test_text_diagnostics_reach_full_validate_for_readme` with exact cases for:

- affirmative claim: `This profile establishes compliance.`;
- direct claim denial: `This profile does not establish compliance.`;
- metalinguistic claim discussion: `The phrase "This profile establishes compliance" is prohibited.`;
- affirmative UK GDPR authority;
- direct UK GDPR authority denial;
- metalinguistic UK GDPR authority discussion; and
- affirmative `Acme Code` authority with `excluded_sources` set to only `Acme Code`.

For every subcase, use both shared fixture writers and reset the excluded-source list, including empty lists. Call complete `validate()` and compare the full exact diagnostic list.

Add `test_text_diagnostics_reach_full_validate_for_structured_json`. Write exact claim and source-authority strings into schema-valid narrative fields, regenerate `PROFILE.md`, and assert complete diagnostics with existing document locations such as `profiles/uk/0.1.0/profile.json: document.scope`. Include an allowed denial for each family. The method must call only complete `validate()` and must not consume inventory records.

- [ ] **Step 4: Run the integration methods on the complete path**

```powershell
python -m unittest tests.test_validate_profiles.ProfileValidationTests.test_text_diagnostics_reach_full_validate_for_readme tests.test_validate_profiles.ProfileValidationTests.test_text_diagnostics_reach_full_validate_for_structured_json tests.test_validate_profiles.ProfileValidationTests.test_authoritative_markdown_prose_is_claim_scanned tests.test_validate_profiles.ProfileValidationTests.test_authoritative_markdown_prose_respects_source_boundary -v
```

Expected: PASS with README, structured JSON, stripped `PROFILE.md`, dynamic exclusions, both diagnostic families, and affirmative, negative, and metalinguistic forms reaching complete validation.

- [ ] **Step 5: Implement the narrow matrix helper and move all 73 methods**

Create `ProfileLanguageMatrixTests(unittest.TestCase)` with no `setUp()`, temporary directory, package fixture, or file mutation. Its helper shall obtain only the named method's cases, process each record once, call each applicable production text boundary exactly once, sort and deduplicate the union, and compare it with `list(case.expected_diagnostics)`.

```python
def _assert_profile_language_cases(self, method_name: str) -> None:
    cases = profile_language_cases.profile_language_inventory().cases_for_method(
        method_name
    )
    consumed: list[str] = []
    with mock.patch.object(
        validate_profiles,
        "validate",
        side_effect=AssertionError(
            "fast language matrices shall not call validate"
        ),
    ):
        for case in cases:
            with self.subTest(case_id=case.case_id):
                diagnostics: list[str] = []
                if "claim" in case.diagnostic_families:
                    diagnostics.extend(
                        validate_profiles.claim_text_diagnostics(
                            profile_fixture.profile_readme_content(case.text),
                            case.location,
                        )
                    )
                if "source_authority" in case.diagnostic_families:
                    diagnostics.extend(
                        validate_profiles.source_authority_text_diagnostics(
                            profile_fixture.profile_readme_content(case.text),
                            case.location,
                            case.excluded_sources,
                        )
                    )
                self.assertEqual(
                    sorted(set(diagnostics)),
                    list(case.expected_diagnostics),
                )
                consumed.append(case.case_id)
    self.assertEqual(consumed, [case.case_id for case in cases])
```

Refactor `write_profile_readme()` to call a pure `profile_readme_content(text: str) -> str` formatter so the fast path and file writer classify identical bytes without touching disk. Move all 73 selected method definitions from `ProfileValidationTests` to `ProfileLanguageMatrixTests`; each method body must contain only its own helper call. Delete `_assert_language_cases_through_full_validate()` after the final method moves. Keep the five excluded repeated-call methods and every retained full-path test in `ProfileValidationTests`.

- [ ] **Step 6: Run the guards, integrations, and full profile module**

```powershell
python -m unittest tests.test_validate_profiles.ProfileLanguageMatrixStructureTests -v
python -m unittest tests.test_validate_profiles.ProfileLanguageMatrixTests -v --durations 50
python -m unittest tests.test_validate_profiles.ProfileValidationTests -v --durations 50
python -m unittest tests.test_validate_profiles -v --durations 50
```

Expected: PASS. The matrix class executes exactly 73 methods and consumes 908 records without calling `validate()`. The fixture-backed class retains the two new integration methods, the existing `PROFILE.md` tests, the five explicit exclusions, and all security, schema, CLI, ordering, and sanitization coverage.

- [ ] **Step 7: Commit the narrow migration**

```powershell
git diff --check
git add tests/profile_fixture.py tests/test_validate_profiles.py
git diff --cached --stat
git diff --cached
git commit -m "perf: move profile language matrices to text diagnostics"
```

Checkpoint: unittest uses the narrow path for all 908 cases, while representative integration and the retained opt-in tool keep the full path observable.

---

### Task 6: Prove the final candidate and collect timing diagnostics

**Files:**
- Verify: `tests/profile_language_cases.py`
- Verify: `tests/profile_fixture.py`
- Verify: `tests/test_validate_profiles.py`
- Verify: `tools/validate_profiles.py`
- Verify: `tools/verify_profile_hot_path_equivalence.py`
- Verify only: `tools/test-shards.json`

**Interfaces:**
- Consumes: the committed Task 5 candidate.
- Produces: exact-SHA equivalence evidence and non-gating before/after timing records.

- [ ] **Step 1: Require a clean exact candidate and rerun all 908 three-way comparisons**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$candidate = git rev-parse HEAD
if ($candidate -notmatch '^[0-9a-f]{40}$') { throw "Invalid candidate SHA: $candidate" }
$status = git status --porcelain=v1 --untracked-files=all
if ($status) { throw "Dirty candidate: $($status -join ', ')" }
$caches = Get-ChildItem -Recurse -Directory -Filter __pycache__
if ($caches) { throw "Generated Python caches: $($caches.FullName -join ', ')" }
$equivalenceElapsed = Measure-Command {
  python -B tools/verify_profile_hot_path_equivalence.py --check --candidate-sha $candidate
  if ($LASTEXITCODE -ne 0) { throw "Final equivalence failed" }
}
$equivalenceElapsed.TotalSeconds
```

Expected: the tool reports this exact candidate, 73 methods, 908 cases, the reviewed digest, and `equivalence=PASS`. Duration is recorded but does not affect the result.

- [ ] **Step 2: Run three focused timing samples without thresholds**

```powershell
1..3 | ForEach-Object {
  $run = $_
  $elapsed = Measure-Command {
    python -m unittest tests.test_validate_profiles -v --durations 50
    if ($LASTEXITCODE -ne 0) { throw "Profile timing run $run failed" }
  }
  "profile_module_run_$run=$($elapsed.TotalSeconds)"
}
1..3 | ForEach-Object {
  $run = $_
  $elapsed = Measure-Command {
    python tools/run_test_shards.py --shard profile_validation --durations 50
    if ($LASTEXITCODE -ne 0) { throw "Profile shard timing run $run failed" }
  }
  "profile_shard_run_$run=$($elapsed.TotalSeconds)"
}
```

Expected: all six runs pass and print durations. Compare them with the design's diagnostic baseline of 235 seconds for the hosted module and 5.6 to 9.7 seconds for the slowest matrix methods, but do not claim the parent Phase 2 target from local results.

- [ ] **Step 3: Handle any defect as a new candidate**

If equivalence or focused testing finds a defect, first add a focused failing regression to `tests/test_validate_profiles.py`, make the smallest production, inventory, or fixture repair, run the focused red and green cycle, commit with a specific message, and restart Task 6 at Step 1. Do not amend a previously reviewed commit or reuse its SHA evidence.

---

### Task 7: Run complete repository validation and exact-SHA reviews

**Files:**
- Review: complete branch diff from `git merge-base origin/main HEAD` through the final candidate.
- Record externally: exact commands, exit codes, test counts, skips, durations, population digest, equivalence output, reviewer findings, and reviewed head in the pull-request description.

**Interfaces:**
- Consumes: the exact candidate that passed Task 6.
- Produces: complete local validation, two independent reviews of the same SHA, and humanized review evidence.

- [ ] **Step 1: Verify tracked-file readability and the shard manifest**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$missing = git ls-files | Where-Object { -not (Test-Path -LiteralPath $_) }
if ($LASTEXITCODE -ne 0) { throw "git ls-files failed" }
if ($missing) { throw "Unreadable tracked paths: $($missing -join ', ')" }
python tools/validate_test_shards.py --check
if ($LASTEXITCODE -ne 0) { throw "Shard manifest validation failed" }
```

Expected: every tracked path is readable and the manifest reports complete, unique shard coverage without an edit to `tools/test-shards.json`.

- [ ] **Step 2: Run the profile shard, aggregate shards, and discovery**

```powershell
python tools/run_test_shards.py --shard profile_validation --durations 50
if ($LASTEXITCODE -ne 0) { throw "Profile shard failed" }
python tools/run_test_shards.py --all --durations 50
if ($LASTEXITCODE -ne 0) { throw "Aggregate shards failed" }
python -m unittest discover -s tests -v --durations 50
if ($LASTEXITCODE -ne 0) { throw "Discovery failed" }
```

Expected: all commands pass, shard and discovery populations agree, and only documented platform-dependent skips remain.

- [ ] **Step 3: Run every repository validator required by this change**

```powershell
python tools/validate_assessment.py --check
if ($LASTEXITCODE -ne 0) { throw "Assessment validation failed" }
python tools/validate_profiles.py --check
if ($LASTEXITCODE -ne 0) { throw "Profile validation failed" }
python tools/validate_controls.py --check
if ($LASTEXITCODE -ne 0) { throw "Control validation failed" }
python tools/validate_architectures.py
if ($LASTEXITCODE -ne 0) { throw "Architecture validation failed" }
python tools/migrate_control_mappings.py --check
if ($LASTEXITCODE -ne 0) { throw "Control mapping migration check failed" }
python tools/validate_crosswalks.py --check
if ($LASTEXITCODE -ne 0) { throw "Crosswalk validation failed" }
python tools/render_pci_dss_mapping_go_no_go.py --check
if ($LASTEXITCODE -ne 0) { throw "PCI DSS readiness rendering failed" }
python tools/release_gates.py --check
if ($LASTEXITCODE -ne 0) { throw "Historical release validation failed" }
python tools/v05_beta_release_gates.py --check --baseline-ref origin/main
if ($LASTEXITCODE -ne 0) { throw "v0.5-beta release validation failed" }
python tools/validate_links.py --check
if ($LASTEXITCODE -ne 0) { throw "Link validation failed" }
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md
if ($LASTEXITCODE -ne 0) { throw "Mermaid rendering validation failed" }
```

Expected: every command exits 0, all Mermaid blocks render with the repository-pinned toolchain, and profile CLI output and status remain unchanged.

- [ ] **Step 4: Review whole-branch hygiene and bind the review candidate**

```powershell
$mergeBase = git merge-base origin/main HEAD
if ($LASTEXITCODE -ne 0 -or $mergeBase -notmatch '^[0-9a-f]{40}$') {
  throw "Invalid merge base: $mergeBase"
}
git diff --check "$mergeBase..HEAD"
if ($LASTEXITCODE -ne 0) { throw "Whole-branch whitespace check failed" }
git diff --stat "$mergeBase..HEAD"
git diff "$mergeBase..HEAD" -- tests/profile_language_cases.py tests/profile_fixture.py tests/test_validate_profiles.py tools/validate_profiles.py tools/verify_profile_hot_path_equivalence.py
$reviewedHead = git rev-parse HEAD
if ($reviewedHead -notmatch '^[0-9a-f]{40}$') { throw "Invalid reviewed head" }
$status = git status --porcelain=v1 --untracked-files=all
if ($status) { throw "Dirty reviewed candidate: $($status -join ', ')" }
$caches = Get-ChildItem -Recurse -Directory -Filter __pycache__
if ($caches) { throw "Generated Python caches: $($caches.FullName -join ', ')" }
$reviewedHead
```

Expected: only the five planned implementation files and their tests changed, the branch has no whitespace defects, the worktree is clean, and no generated cache remains.

- [ ] **Step 5: Obtain two independent reviews of the exact same SHA**

Dispatch reviews sequentially so no reviewer edits the candidate:

1. Specification and inventory review: verify all approved-design requirements, the exact 73-method ledger, 908-case expansion, digest construction, expected diagnostics, product dimensions, excluded-source distribution, full-path stage evidence, and final matrix consumption.
2. Security and compatibility review: verify clean-SHA binding, dirty-state rejection, subprocess failure handling, temporary-path sanitization, fixture reset, immutable excluded-source snapshots, wrapper ownership, CLI exit behavior, and retention of filesystem, schema, traceability, and operational tests.

Give each reviewer `$reviewedHead` and the complete `$mergeBase..$reviewedHead` diff. Require explicit Critical, Important, and lower-severity findings. Resolve every Critical and Important finding. Record the reason for accepting or deferring each lower-severity finding.

- [ ] **Step 6: Revalidate after any review change**

For each accepted finding, add a focused failing regression before the fix when practical, commit the repair, and treat the new `HEAD` as a fresh candidate. Rerun the equivalence command from Task 6, all affected focused and complete gates, whole-branch hygiene, and both independent reviews. Continue until both reviews cover the same unchanged SHA with no unresolved Critical or Important issue.

- [ ] **Step 7: Prepare humanized pull-request evidence**

Use the `humanizer` skill in embedded mode on the pull-request prose. State concrete results without promotional language. Include:

- the exact reviewed head and merge base;
- the full-path-stage equivalence SHA and output;
- the final-candidate equivalence SHA and output;
- the inventory count, method count, excluded-source distribution, and population digest;
- focused module, profile shard, aggregate shard, discovery, standalone validator, and Mermaid results;
- the three profile-module and three profile-shard timing samples, labeled diagnostic only;
- both exact-SHA review conclusions and any accepted lower-severity findings; and
- the statement that the hosted 40 percent Phase 2 target remains open until all Phase 2 increments have landed and three successful hosted full-suite runs exist.

Before opening or updating the reviewable pull request, confirm that the recorded reviewed head still equals both `git rev-parse HEAD` and the PR head. If it differs, discard the stale evidence and restart Task 6.

Final checkpoint: the final clean candidate has passed retained equivalence, focused and complete testing, all required validators, whole-branch review, and two independent reviews at the exact recorded SHA.
