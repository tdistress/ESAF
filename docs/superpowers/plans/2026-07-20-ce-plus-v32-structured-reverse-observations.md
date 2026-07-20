# Cyber Essentials Plus v3.2 structured reverse observations implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the exact CE Plus v3.2 reverse profile’s free-form observation inference with a canonical structured allow-valid contract and migrate its 31 existing positives without changing mapping decisions.

**Architecture:** Add one source-versioned profile module containing the exact eight-field JSON grammar and relationship-leg registry keyed by `(provision_id, control_id)`. The shared validator delegates observation and registry-integrity validation to that module, retains all other reverse-profile contracts, and removes the superseded prose/activity path. Markdown records remain authoritative; records render each leg observation from the allowlist and bind prohibitions to the exact rendered JSON.

**Tech Stack:** Python 3.14 standard library, canonical JSON, Markdown JSON front matter, `unittest`, existing crosswalk validators and generators.

## Global constraints

- Scope is only mapping set `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`.
- Preserve all dispositions, target controls, relationships, coverage, confidence, provenance, condition contracts, and human-readable expected-evidence glosses.
- Do not implement Task 5; document only its registry-extension rule.
- Keep the README Minor deferred to Task 6.
- Treat every semantic field as an outcome-neutral measurement schema and reject answer- or assurance-bearing terms across field boundaries.
- Use `PYTHONDONTWRITEBYTECODE=1` and leave no `__pycache__` directory.
- Use fail-first tests before production code or record migration.

---

### Task 1: Lock the canonical claim contract and registry

**Files:**
- Create: `tools/crosswalks/uk_ce_plus_v32_reverse_profile.py`
- Modify: `tests/test_uk_cyber_essentials_plus_v32_external_to_esaf_mapping.py`

**Interfaces:**
- Produces: `render_observation_claim(provision_id: str, control_id: str) -> str`
- Produces: `validate_observation_claim(claim_text: str, provision_id: object, control_id: object, profiles: Mapping[tuple[str, str], Mapping[str, str]] | None = None) -> list[str]`; `None` resolves the module’s current production lookup, allowing an isolated patched registry in multi-leg tests.
- Produces: `build_observation_profiles(entries: Iterable[tuple[str, str, str, str, str, str]]) -> dict[tuple[str, str], dict[str, str]]`, which rejects duplicate pair declarations.
- Produces: `validate_observation_registry(mapped_pairs: Iterable[tuple[str, str]], entries: Iterable[tuple[str, str, str, str, str, str]] = OBSERVATION_PROFILE_ENTRIES) -> list[str]`.
- Owns: `OBSERVATION_PROFILE_ENTRIES`, an ordered declaration sequence keyed by provision/control pair, and its duplicate-checked `OBSERVATION_PROFILES` lookup.

The registry shall contain these exact profiles:

| Provision | Control | Result kind | Subject | Predicate | Result type |
| --- | --- | --- | --- | --- | --- |
| CEPTS3.2-M-004 | AUD-120 | assessment_scope | declared_assessment_boundary | scope_correspondence_status | recorded_comparison |
| CEPTS3.2-M-010 | AUD-130 | finding_remediation | pre_test_findings | pre_test_resolution_status | recorded_status |
| CEPTS3.2-M-011 | AUD-120 | evidence_retention | pre_test_verification_evidence | retention_duration | recorded_duration |
| CEPTS3.2-S-007 | AUD-120 | sampling_calculation | sample_size | calculation_method_alignment | recorded_calculation |
| CEPTS3.2-S-008 | CMP-110 | evidence_retention | sample_size_calculation_evidence | retention_duration | recorded_duration |
| CEPTS3.2-T1-009 | INF-120 | vulnerability_severity | high_risk_vulnerability | severity_score | recorded_threshold |
| CEPTS3.2-T1-011 | IAM-110 | authentication_requirement | user_authentication | service_access_requirement_status | recorded_boolean |
| CEPTS3.2-T1-012 | IAM-110 | authentication_strength | authentication_factors | factor_count | recorded_count |
| CEPTS3.2-T1-013 | IAM-140 | credential_configuration | default_password | password_change_status | recorded_boolean |
| CEPTS3.2-T1-014 | APP-150 | abuse_resistance | login_attempts | throttling_status | recorded_boolean |
| CEPTS3.2-T1-015 | APP-150 | abuse_resistance | user_account | lockout_attempt_threshold | recorded_count |
| CEPTS3.2-T2-007 | INF-120 | vulnerability_fix_availability | qualifying_vulnerability | vendor_fix_age | recorded_duration |
| CEPTS3.2-T3-005 | INF-110 | host_protection_configuration | anti_malware | activation_and_installation_coverage | recorded_status |
| CEPTS3.2-T3-015 | INF-110 | malware_delivery_control | malware_test_file | delivery_and_access_status | recorded_status |
| CEPTS3.2-T3-016 | INF-110 | execution_control | executable_test_file | delivery_execution_interaction_status | recorded_status |
| CEPTS3.2-T3-017 | INF-110 | malware_delivery_control | defined_malware_delivery_branches | branch_applicability_status | recorded_branch |
| CEPTS3.2-T3-021 | INF-110 | network_access_configuration | test_user | internet_access_status | recorded_boolean |
| CEPTS3.2-T3-022 | INF-110 | download_protection | test_file_download | download_prevention_status | recorded_boolean |
| CEPTS3.2-T3-023 | INF-110 | download_protection | downloaded_test_file | download_access_control_status | recorded_boolean |
| CEPTS3.2-T3-024 | INF-110 | malware_delivery_control | malware_test_file | download_and_access_status | recorded_status |
| CEPTS3.2-T3-025 | INF-110 | execution_control | executable_test_file | download_execution_interaction_status | recorded_status |
| CEPTS3.2-T3-027 | INF-110 | host_protection_configuration | anti_malware_installation | operational_status | recorded_status |
| CEPTS3.2-T3-028 | INF-110 | host_protection_configuration | anti_malware_updates | configuration_alignment | recorded_comparison |
| CEPTS3.2-T3-029 | INF-110 | host_protection_configuration | anti_malware_installation_and_configuration | check_status | recorded_status |
| CEPTS3.2-T3-031 | INF-110 | trust_store_configuration | trusted_roots | root_set_relation | recorded_comparison |
| CEPTS3.2-T3-032 | INF-130 | configuration_change_approval | additional_trusted_roots | applicant_agreement_status | recorded_status |
| CEPTS3.2-T3-033 | INF-110 | execution_control | unsigned_executable | execution_capability | recorded_boolean |
| CEPTS3.2-T3-034 | INF-110 | execution_control | untrusted_chain_executable | execution_capability | recorded_boolean |
| CEPTS3.2-T3-035 | INF-110 | code_signing_configuration | executable_formats | code_signing_coverage | recorded_status |
| CEPTS3.2-T3-036 | INF-110 | allowlisting_configuration | listed_configuration_and_execution_checks | check_status | recorded_status |
| CEPTS3.2-T4-008 | IAM-110 | mfa_challenge | user_or_administrator | pre_access_challenge_status | recorded_boolean |

- [ ] **Step 1: Write fail-first contract tests.** Change the positive fixture to CEPTS3.2-T1-011/IAM-110 and a wished-for rendered claim. Add separate failures for malformed/non-object/duplicate-key JSON, exact-field drift, non-string values, noncanonical serialization, wrong provision/control/date boundaries, tool-as-subject, activity-as-predicate/result-type/kind, and a profile value borrowed from another control. For each of `result_kind`, `subject`, `predicate`, and `result_type`, add cross-field mutations containing pass/fail, true/false, compliance, certification, success/failure, and equivalence variants. Tokenize on identifier boundaries and add `password` as a required substring false-positive guard. Add registry-integrity failures for a duplicate declared pair, missing mapped pair, orphan pair, known negative-provision pair, and unimplemented Task 5 pair. Rebind all nine prohibitions to each mutated claim.
- [ ] **Step 2: Verify RED.** Run the new contract tests and confirm the current free-form validator either accepts invalid claims or rejects the wished-for valid structured claim for the missing behavior.
- [ ] **Step 3: Implement the isolated module.** Render with `json.dumps(claim, separators=(",", ":"), sort_keys=True)`. Parse through an `object_pairs_hook` that rejects duplicate keys. Require exactly the eight design fields, exact boundary literals, record/control equality, outcome-neutral semantic fields, and exact equality with the relationship-leg registry. Build the lookup only through duplicate-pair validation.
- [ ] **Step 4: Verify module GREEN.** Run the new contract tests directly and keep all diagnostics deterministic.

### Task 2: Replace the shared validator path

**Files:**
- Modify: `tools/crosswalks/validation.py`
- Modify: `tests/test_uk_cyber_essentials_plus_v32_external_to_esaf_mapping.py`

**Interfaces:**
- Consumes: `validate_observation_claim` from Task 1.
- Preserves: existing supported-outcome, conditions-only-narrow, manifest, condition-evidence, population, and prohibited-inference validation.

- [ ] **Step 1: Add fail-first integration tests.** Include every reviewer synonym (`scanner performed the scan`, `Assessor employed a scanning tool`, `utility completed execution`, `permission to run Nmap granted`, `Nmap authorized to run`) plus all earlier active/passive/nominal variants. Add a valid structured authentication result whose tool name appears only in `tool evidence`. Add a valid two-leg fixture by patching the profile module with two pair keys for one provision, then duplicate-pair and incompatible-pair mutations; both legs shall pass through the production record validator.
- [ ] **Step 2: Verify RED with exact prohibition rebinding.** Confirm failures are observation-contract failures, not stale prohibition diagnostics.
- [ ] **Step 3: Integrate the closed validator.** Isolate the exact JSON text between rationale markers, require one terminal period, delegate each leg to the pair-keyed profile module, and delete `_reverse_observation_has_independent_result`, its activity/synonym helpers, and `_reverse_observation_is_date_bound`. At snapshot scope, compare authoritative mapped leg pairs to the registry and diagnose duplicates, missing pairs, orphans, and negative/unimplemented-provision keys.
- [ ] **Step 4: Run focused GREEN.** Run the structured-contract mutations, valid tool-produced result, full focused reverse-profile module, and persisted-profile validator test.

### Task 3: Migrate the 31 positive records mechanically

**Files:**
- Modify: the 31 existing mapped records in `crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0/`
- Modify: `crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0.md`
- Regenerate: `crosswalks/catalog.json`

- [ ] **Step 1: Verify migration RED.** Run the persisted-profile test against the new validator and confirm all 31 legacy prose observations fail the canonical contract.
- [ ] **Step 2: Perform a bounded mechanical rewrite.** For exactly the registry’s 31 relationship-leg pairs, render JSON by `(provision_id, control_id)`, replace only that leg’s observation segment and nine prohibited-inference observation bindings, and assert before writing that disposition, target, relationship, coverage, confidence, provenance, conditions, expected evidence, and known gaps are unchanged.
- [ ] **Step 3: Audit the diff.** Compare every current record to the pre-migration commit and require changed relationship fields to equal `{rationale, prohibited_inferences}`. Report before any unexpected mapping-decision change and stop rather than write it.
- [ ] **Step 4: Regenerate derived state.** Refresh the lifecycle snapshot digest, then run `python tools/validate_crosswalks.py --write --baseline-ref 93e1034d8ea4bfcacab4d6a16426db1d2df39e77` and verify only the expected registry/catalog output changes.
- [ ] **Step 5: Run migration GREEN.** Prove registry keys exactly equal the Markdown mapped-leg set, all 31 persisted positives validate, no negative or unimplemented provision owns a registry key, and the exact Task 3/Task 4 disposition and target sets remain unchanged. Task 5 later extends the registry once per independently justified new leg, including an additional leg for a provision already present.

### Task 4: Verify and hand off the corrective candidate

**Files:**
- Append: `.superpowers/sdd/task-4-report.md` (gitignored task evidence)

- [ ] **Step 1: Append RED/GREEN and scope evidence.** Record the structured-contract design, exact migration count, record-diff audit, disposition/target invariance, and Task 5 extension rule.
- [ ] **Step 2: Run focused and repository gates.** Run the focused reverse module, relevant persisted-profile validator test, `validate_crosswalks.py --check`, `validate_controls.py --check`, `git diff --check`, and cache audit.
- [ ] **Step 3: Commit the corrective implementation.** Stage only the profile module, validator, focused tests, 31 migrated positives, lifecycle digest, and generated catalog; commit with an outcome-focused message.
- [ ] **Step 4: Run exact-head verification.** Run `python -m unittest discover -s tests -v` once on the final committed bytes, rerun affected focused/crosswalk/control gates, run `git diff --check 3f56726..HEAD`, verify a clean worktree and zero `__pycache__` directories, and record the exact candidate SHA.
