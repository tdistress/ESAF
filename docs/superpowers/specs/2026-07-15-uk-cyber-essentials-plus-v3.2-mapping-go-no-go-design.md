# UK Cyber Essentials Plus v3.2 Mapping Go/No-Go Review Design

**Status:** Approved design

**Date:** 2026-07-15

**Issue:** [#44](https://github.com/tdistress/ESAF/issues/44)

## 1. Purpose

This design defines an evidence-gated feasibility review for mapping the Enterprise Secure AI Framework (ESAF) 0.4-alpha and the public NCSC *Cyber Essentials Plus Test Specification* v3.2. The review decides whether each mapping direction is suitable for a separate mapping-design milestone. It does not create or authorize a mapping snapshot.

The review shall preserve the distinction between security-control implementation, assessment procedure, assessment evidence, and assurance conclusion. It shall not infer certification, compliance, equivalence, endorsement, predictive sufficiency, full-population assurance, continuous assurance, current-scheme completeness, or any Cyber Essentials Plus testing outcome.

## 2. Decision and alternatives

Use a representative, adversarial feasibility matrix with predeclared gates and stress cases. The matrix shall test the hardest semantic, source, rights, evidence, and assurance boundaries without performing a full 144-provision dry run.

Three approaches were considered:

1. **Evidence-gated feasibility review — selected.** Test representative stress cases across every group, kind, actor, and special assurance boundary. This produces reproducible directional decisions without creating a shadow mapping set.
2. **Full 144-provision dry run — rejected.** This would provide broad evidence but would effectively perform mapping implementation before its design and duplicate later work.
3. **Qualitative expert memorandum — rejected.** This would be faster but insufficiently reproducible, machine-checkable, and resistant to overclaiming.

## 3. Scope and non-goals

### 3.1 Decision universe

The decision universe is the locked 144-provision oracle at `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`, whose LF-normalized tracked-byte SHA-256 is `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc` at the approved source-inventory head.

The oracle is complete only for the pinned public v3.2 PDF under atomization rule version `1.0.0`. It is not a complete inventory of the current operational Cyber Essentials Plus scheme, Delivery Partner methodology, or certification process.

Current operational changes, NCSC core v3.3, Delivery Partner practices, and IASME material may explain limitations. They shall not supply missing outcomes, expand the assessment universe, or establish a positive feasibility result.

### 3.2 Authorized outcome

The review shall assess these directions independently and in this order:

1. `esaf_to_external`
2. `external_to_esaf`

Each direction receives exactly one disposition: `GO`, `HOLD`, or `NO_GO`.

A `GO` authorizes only a separate direction-specific mapping design. It does not authorize immediate mapping implementation.

### 3.3 Prohibited outputs

This milestone shall not create or modify:

- any path beneath `crosswalks/mappings/`;
- any path beneath `crosswalks/registry/`;
- a mapping-set snapshot, provision inventory, provision mapping record, lifecycle record, relationship leg, control manifest, or generated mapping statistic;
- authoritative relationship, coverage, confidence, mapping disposition, reviewer, or approver fields; or
- any claim that a feasibility probe is an ESAF-1600 mapping record.

The existing core v3.3 mapping set and its generated statistics shall remain unchanged.

### 3.4 Source-inventory traceability prerequisite

The merged source-inventory traceability table records stale oracle digest `096a5c1238b92250b1497e76ef175b6b8e99f05a65a21ed66263f8b1cf68578a`. The actual LF-normalized tracked bytes at source-inventory head `2a5428ad50d3121f16fc39ccb9c7ff116426ec26` hash to `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`. The stale value arose because the table was refreshed before the final B-001 oracle summary edit in the same commit, and the repository has no test that validates the recorded artifact-digest table.

Before the feasibility rights re-attestation or any probe work, implementation shall add a failing regression test that compares every tracked artifact digest in the source-inventory traceability table with the corresponding LF-normalized tracked bytes. It shall then correct the stale oracle digest and prove every recorded tracked-artifact digest is current. This is a traceability repair only; it shall not change the oracle, its 144-provision content, or any mapping artifact.

## 4. Source and rights boundary

The review shall consume only:

- the locked public v3.2 oracle and its committed source, rights, reconciliation, and traceability evidence;
- exact normative ESAF 0.4-alpha control text and the pinned control population recorded by the repository;
- ESAF-1600 and its schemas, templates, validators, and taxonomy; and
- independently written operational context that remains outside the decision universe.

The rights approval commit `6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6` approved the exact six-element ESAF-1600 rights universe, including `derivative_mapping_analysis`. Before any source-derived feasibility matrix enters Git, the same rights reviewer or another qualified independent rights reviewer shall re-attest that the planned matrix and review field classes remain within that approval. The re-attestation shall be recorded and committed by itself before any probe, directional gate result, or provisional disposition is created or committed.

The re-attestation shall confirm:

- the exact oracle digest and source variants;
- original paraphrases rather than copied source passages;
- the sole existing allowed verbatim location remains `known_anomalies[0].source_literal` in the oracle and is not duplicated in the feasibility artifacts;
- NCSC/OGL and IASME rights remain separate;
- no IASME-derived structure or text enters the decision evidence; and
- no logo, mark, third-party material, or endorsement implication is used.

The re-attestation confirms the existing publication basis; it shall not retroactively approve expanded content. A required expansion produces `HOLD` until a separate rights basis is approved.

## 5. Directional questions

### 5.1 ESAF to external

The `esaf_to_external` question is:

> Does exact normative ESAF control text directly provide or require an outcome, action, condition, or prerequisite that materially contributes to a specific public Cyber Essentials Plus v3.2 provision, without implying that the assessment procedure has been performed or passed?

The analysis shall reject thematic similarity, implementation guidance, architectural adjacency, and generic security benefit as positive normative bases.

### 5.2 External to ESAF

The `external_to_esaf` question is:

> Can evidence or a result produced by performing a specific public Cyber Essentials Plus v3.2 provision materially support evaluation of an exact normative ESAF control outcome under explicit actor, scope, population, sample, date, tool, exception, and provenance conditions?

The analysis shall not treat a procedure, pass result, certificate, sample, or assessment file as proof of current or continuous ESAF control implementation.

The two questions are asymmetric. A result in one direction shall not establish, strengthen, or weaken the other direction automatically.

## 6. Mandatory gates

Each direction shall record all seven gates in this exact order:

1. `source`
2. `rights`
3. `semantic`
4. `normative_basis`
5. `schema`
6. `overclaiming`
7. `utility`

Each gate has `PASS`, `BLOCKED`, or `FAIL` status and a specific evidence-based rationale.

### 6.1 Source gate

The pinned oracle shall provide sufficient identifiers, original summaries, actors, locators, kinds, section links, anomalies, and assurance limits for the directional question. Missing current-scheme detail shall remain a limitation and shall not be inferred.

### 6.2 Rights gate

The approved publication basis shall cover every planned field and analytical use. A separately licensed or unapproved source shall not be required to understand a positive result.

### 6.3 Semantic gate

The directional question shall keep implementation, procedure, evidence, result, and assurance distinct. Conditions may narrow a result but shall not supply a missing external or ESAF outcome.

### 6.4 Normative-basis gate

Every positive feasibility result shall cite exact ESAF `shall` text through a stable control identifier and requirement locator. Guidance, examples, architecture patterns, control objectives, or adjacent capabilities are insufficient by themselves.

### 6.5 Schema gate

The existing ESAF-1600 taxonomy and schema shall be capable of expressing the prospective direction, rationale, conditions, evidence, known gaps, and negative outcomes without a schema extension or semantic overload.

### 6.6 Overclaiming gate

The direction shall remain useful after preserving actor, scope, population, sample, assessment and evidence dates, tool and provenance, Delivery Partner discretion, exception predicates, and point-in-time limits.

### 6.7 Utility gate

The prospective mapping shall provide material traceability value even if most provisions later receive `no_direct_mapping`. A single positive feasibility probe may satisfy this gate only when its stakeholder value is stated specifically and survives adversarial review.

## 7. Disposition mechanics

For each direction, validators shall derive `positive_probe_identifiers` as the ordered `probe_id` values of that direction's probes whose conclusion is `POSITIVE_FEASIBILITY`. The recorded array shall equal that derived array exactly; a declared identifier cannot make a probe positive and an omitted positive probe is invalid.

The directional disposition shall then be derived mechanically:

- `GO` requires all seven gates to be `PASS`, a nonempty derived positive-probe array, and empty `prerequisites` and `reconsideration_triggers` arrays.
- `HOLD` requires no `FAIL` gate and at least one `BLOCKED` gate within that sealed directional submission. `HOLD` shall have one or more externally resolvable `prerequisites`, each naming the missing evidence and re-entry test, and an empty `reconsideration_triggers` array.
- `NO_GO` requires at least one `FAIL` gate or, when all seven gates are `PASS`, an empty derived positive-probe array after the complete adversarial probe set. It shall have empty `prerequisites` and one or more `reconsideration_triggers`, each naming a source, methodology, or framework change and evidence that would justify reconsideration.

A reviewer shall be able to reproduce the disposition from the gate statuses and probe conclusions without relying on unstated judgment.

## 8. Feasibility probes

### 8.1 Coverage contract

For each direction independently, the selected probes shall collectively cover:

- all groups in oracle order: `M`, `T1`, `S`, `T2`, `T3`, `T4`, `T5`, `C`, `A`, `B`;
- all kinds: `applicability`, `prerequisite`, `procedure_step`, `decision_rule`, `result_rule`, `evidence_retention`, `recommendation`;
- all actors: `Assessor`, `Applicant`, `Certification Body`, `Certifying Body`, `Delivery Partner`; and
- every special scenario below.

One probe may cover multiple provisions and multiple coverage axes when one coherent feasibility question justifies the grouping. Every selected provision shall resolve to the oracle and its recorded group, kind, actors, section, and locator.

### 8.2 Required special scenarios

Each direction shall cover these scenario identifiers exactly:

1. `figure-1-decision-logic`
2. `sampling-and-population-limits`
3. `evidence-retention`
4. `complete-assessment-file-coverage`
5. `delivery-partner-discretionary-exception`
6. `known-source-anomaly`
7. `point-in-time-versus-continuous-assurance`
8. `core-v3.3-versus-plus-v3.2-separation`
9. `expected-no-direct-esaf-basis`

The known anomaly shall be referenced only by anomaly identifier and oracle path. Its source literal shall not be copied into the feasibility matrix or review record.

Scenario coverage shall be evidence-bound rather than label-counted. Every scenario claimed by a probe shall have one same-probe `special_scenario_binding` with the same identifier, one or more provision IDs where the scenario concerns provisions, and one or more exact oracle JSON paths. Paths shall resolve only to the bound provision records, `scope`, `known_anomalies[0]`, or named fields beneath `assurance_limits`. The `known-source-anomaly` binding shall resolve to anomaly identifier `cepts32-anomaly-001` at `known_anomalies[0]`; assurance scenarios shall resolve to their specific `assurance_limits` fields. A scenario is covered for a direction only when a probe in that direction has a valid binding; unions of unbound labels are invalid.

Validators shall apply this closed binding oracle in each direction:

| Scenario | Required provision/path evidence |
|---|---|
| `figure-1-decision-logic` | At least `CEPTS3.2-T1-008` plus the applicable decision/result records from `CEPTS3.2-T1-009` through `CEPTS3.2-T1-016`; provision paths shall resolve by `external_provision_id`. |
| `sampling-and-population-limits` | At least one sampling provision among `CEPTS3.2-M-006`, `CEPTS3.2-S-005`, `CEPTS3.2-S-007`, or `CEPTS3.2-S-009`, plus `assurance_limits.population_and_sample_boundary`. |
| `evidence-retention` | `CEPTS3.2-M-011` or `CEPTS3.2-S-008`, plus `assurance_limits.evidence_date_boundary`. |
| `complete-assessment-file-coverage` | `CEPTS3.2-B-001` and at least one of `CEPTS3.2-B-007`, `CEPTS3.2-B-010`, `CEPTS3.2-B-011`, or `CEPTS3.2-B-012`. |
| `delivery-partner-discretionary-exception` | `CEPTS3.2-C-008`, `CEPTS3.2-C-010`, and `CEPTS3.2-C-011`, plus `assurance_limits.discretion_owner` and `assurance_limits.discretionary_exception`. |
| `known-source-anomaly` | At least one bound provision used to test the anomaly's consequence, plus `known_anomalies[0].anomaly_id` resolving to `cepts32-anomaly-001` and `known_anomalies[0].locator`; never the literal. |
| `point-in-time-versus-continuous-assurance` | At least one bound assessment provision, plus `assurance_limits.assessment_date_boundary`, `assurance_limits.evidence_date_boundary`, and `assurance_limits.point_in_time_boundary`. |
| `core-v3.3-versus-plus-v3.2-separation` | At least one bound v3.2 provision, plus `scope` and `assurance_limits.scope_boundary`; no core v3.3 provision may be introduced. |
| `expected-no-direct-esaf-basis` | At least one bound provision whose probe conclusion is `NO_POSITIVE_BASIS`, plus that provision's summary and locator paths. |

### 8.3 Probe conclusions

Each probe receives exactly one conclusion:

- `POSITIVE_FEASIBILITY`: exact normative evidence supports a prospective, bounded relationship in the stated direction;
- `NO_POSITIVE_BASIS`: the reviewed material does not supply a direct normative basis; or
- `INDETERMINATE`: a named resolvable prerequisite prevents a defensible conclusion.

These values are feasibility conclusions, not ESAF-1600 mapping dispositions. The artifacts shall not encode relationship, coverage, or confidence values.

### 8.4 External-to-ESAF positive-probe conditions

Every `external_to_esaf` `POSITIVE_FEASIBILITY` probe shall contain a closed `condition_checklist` with these entries in this exact order: `actor`, `scope`, `population`, `sample`, `assessment_date`, `evidence_date`, `tool`, `provenance`, `exception`, `delivery_partner_discretion`, and `point_in_time_status`. Each entry shall contain exactly `condition`, `status`, and `evidence_references`; status shall be `SATISFIED` or `NOT_APPLICABLE`, and evidence references shall be nonempty and resolve under the same rules as gate evidence. `NOT_APPLICABLE` requires explicit evidence showing why that condition cannot affect the bounded claim. Other probes shall have an empty checklist. Conditions may narrow a supported outcome but shall not create a missing ESAF outcome.

## 9. Roles and independence

The milestone shall identify:

- one `esaf_to_external` analyst;
- one different `external_to_esaf` analyst;
- one reconciler different from both analysts;
- one rights reviewer different from both analysts; and
- two exact-head reviewers: specification/methodology and security/overclaiming.

The controller shall dispatch both directional analysts concurrently as sibling Codex agents with `fork_turns="none"`. Each receives an independently hashed direction-specific prompt and the same hashed common-input manifest: approved design, locked oracle, ESAF controls, ESAF-1600 method, and closed contract. Analysts shall write no output file and shall return exactly one canonical JSON payload only as their final response through the controller mailbox. Sibling agents cannot access the controller mailbox. The controller shall not persist outside that mailbox, quote, summarize, or reveal either payload until both final messages have been received. Neither analyst shall see the other direction's provisional disposition, gate statuses, probe conclusions, counts, or payload.

This brokered-private-submission protocol is mandatory for Codex collaboration. If the runtime cannot prove private controller-mailbox semantics, the implementation shall use analysts running under separate principals or containers with equivalent private return channels; if neither mechanism is available, analysis stops. Shared-filesystem output, prompt-only secrecy, sequential dispatch, and `fork_turns` values other than `none` are invalid.

Receipt seals each payload permanently. The controller shall record the prompt and common-input digests, UTC receipt time, SHA-256 of the exact canonical payload bytes, a unique digest reference, and the analyst's no-file/no-sibling-content attestations. Correction, mutation, and supersession after sealing are prohibited. If either member of the pair is missing, malformed, noncanonical, or fails any contract validation, the controller shall discard both payloads and redispatch two fresh analysts without disclosing either prior payload. No invalid or discarded submission may enter the matrix or provenance.

Each final-response payload shall contain exactly `direction`, `analyst`, `direction_assessment`, `probes`, `no_output_file_attestation`, and `no_sibling_content_attestation`. Direction, analyst, assessment, and probes shall agree internally; both attestations shall be `true`. The direction-specific prompt envelope and common-input manifest shall also be JSON values hashed with the canonical serialization below, so their recorded digests identify the complete dispatched instructions and shared source set rather than a prose description.

The reconciler is a validation-and-packaging role, not an analyst. It shall validate each sealed payload independently and may not alter either payload, resolve differences between the asymmetric questions, add gates, change conclusions, or manufacture prerequisites. The committed direction assessment and direction-local probes shall be byte-semantically identical to the accepted payload content after canonical parsing. `HOLD` can arise only from `BLOCKED` gates and prerequisites already present in that direction's sealed submission.

Canonical JSON bytes for payload and content hashing shall be UTF-8 bytes of Python `json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)`. Inputs shall contain only JSON types; object keys are sorted, array order is preserved, and no trailing newline is included. Each direction-content digest shall hash exactly `{"direction_assessment": <that assessment>, "probes": <that direction's probes in matrix order>}` under this serialization. Tests shall recompute both digests from committed matrix content.

The exact-head reviewers shall be independent of the analysts and reconciler. Independent Codex review establishes technical closure only; it does not qualify a future mapping snapshot as reviewed or approved under ESAF-1600.

## 10. Artifacts and closed contracts

### 10.1 Feasibility matrix

First create and commit only `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-rights-re-attestation.md`. That record shall contain the review evidence and confirmations in section 4, the approved field classes, the reviewer identity and date, and an unconditional `approved` or `rejected` disposition. A rejected or conditional disposition stops the analysis.

After the approved re-attestation commit exists, create `docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json`.

The top-level object shall contain exactly:

- `schema_version`: `1.0.0`;
- `review_identifier`: `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--mapping-feasibility--0.1.0`;
- `source_oracle`: object;
- `rights_re_attestation`: object;
- `roles`: object;
- `coverage_contract`: object;
- `analysis_provenance`: object;
- `direction_assessments`: array; and
- `probes`: array.

`source_oracle` shall contain exactly `path`, `sha256`, `source_version`, `expected_provision_count`, `atomization_rule_version`, and `scope_statement`.

`rights_re_attestation` shall contain exactly `record_path`, `record_commit`, `reviewer`, `review_date`, `prior_rights_commit`, `oracle_sha256`, `publication_basis_covered`, `iasme_partition_preserved`, `copied_source_prohibition_preserved`, `field_classes_reviewed`, and `disposition`. Its disposition shall be `approved`. Tests shall prove that the record commit changed only the re-attestation record and is an ancestor of the first commit containing any probe, directional gate result, or provisional disposition.

`roles` shall contain exactly `esaf_to_external_analyst`, `external_to_esaf_analyst`, and `reconciler`. Tests shall enforce the independence rules in section 9.

`coverage_contract` shall contain exactly `groups`, `kinds`, `actors`, and `special_scenarios`, using the ordered values in section 8.

`analysis_provenance` shall contain exactly `broker_protocol`, `prompt_digests`, `common_input_sha256`, `submissions`, `direction_content_digests`, and `reconciliation`.

`broker_protocol` shall contain exactly `dispatch_mode`, `fork_turns`, `concurrent`, `analyst_output_channel`, `no_output_files`, `controller_withholding_attestation`, `sibling_mailbox_inaccessible_attestation`, and `fail_closed_fallback`. Values shall be `codex_sibling_agents`, `none`, `true`, `controller_mailbox_final_response`, `true`, `true`, `true`, and `separate_principals_or_containers_else_stop`, respectively. `prompt_digests` shall contain exactly two direction-ordered objects with exactly `direction` and lowercase hexadecimal `sha256`. `common_input_sha256` shall be lowercase hexadecimal.

`submissions` shall contain exactly two direction-ordered objects, each containing exactly `direction`, `analyst`, `received_at_utc`, `payload_sha256`, `digest_reference`, `no_output_file_attestation`, and `no_sibling_content_attestation`. Each analyst shall equal the matching role and direction-assessment analyst. Digests and references shall be unique; receipt timestamps shall be UTC ISO 8601 values; both attestations shall be `true`. Tests shall reconstruct the exact payload object from the matching committed assessment, direction-local probes, analyst, direction, and two true attestations, then require its canonical SHA-256 to equal `payload_sha256`. There is no correction or supersession field.

`direction_content_digests` shall contain exactly two direction-ordered objects with exactly `direction` and `sha256`. Each digest shall equal the recomputation defined in section 9. `reconciliation` shall contain exactly `reconciler`, `submission_digest_references`, `direction_validations`, `post_seal_changes_prohibited`, and `packaging_disposition`. Its `reconciler` shall equal `roles.reconciler`; its digest references shall equal the two submission references in direction order; `post_seal_changes_prohibited` shall be `true`; and `packaging_disposition` shall be `accepted`. `direction_validations` shall contain exactly two direction-ordered objects, each with exactly `direction`, `status`, and `evidence_references`; committed status shall be `ACCEPTED` and evidence references shall be nonempty. A matrix with a rejected, changed, discarded, or incomplete payload is invalid and shall not be committed.

`direction_assessments` shall contain exactly two objects in the direction order in section 3.2. Each contains exactly `direction`, `analyst`, `question`, `gate_results`, `positive_probe_identifiers`, `disposition`, `decision_rationale`, `prerequisites`, and `reconsideration_triggers`.

Each prerequisite entry shall contain exactly `prerequisite`, `required_evidence`, and `reentry_test`, all nonempty strings that describe an action available outside the completed analysis and an objectively checkable return condition. Each reconsideration-trigger entry shall contain exactly `change` and `required_evidence`, both nonempty strings. Narrative wishes, restatements of analyst opinion, and analyst-only reconsideration are not externally resolvable.

Each gate-result object contains exactly `gate`, `status`, `rationale`, and `evidence_references`. Evidence references shall resolve to probe identifiers, repository-relative source paths with stable locators, or official URLs already approved as bibliographic facts.

Each probe contains exactly:

- `probe_id`;
- `direction`;
- `provision_ids`;
- `selection_basis`;
- `groups`;
- `kinds`;
- `actors`;
- `special_scenarios`;
- `special_scenario_bindings`;
- `condition_checklist`;
- `esaf_normative_bases`;
- `semantic_fit_analysis`;
- `assurance_and_overclaiming_risks`;
- `source_rights_and_operational_limits`;
- `conclusion`; and
- `rationale`.

An ESAF normative-basis entry contains exactly `control_id`, `requirement_locator`, and `relevance_analysis`. `POSITIVE_FEASIBILITY` requires at least one normative-basis entry. `NO_POSITIVE_BASIS` may use an empty array and shall state the missing outcome. `INDETERMINATE` shall state the blocking prerequisite in the corresponding directional assessment.

A special-scenario binding contains exactly `scenario_id`, `provision_ids`, and `oracle_paths`. Its identifier shall occur exactly once in the probe's `special_scenarios`; its provision IDs shall be a nonempty subset of the probe's provision IDs; and every oracle path shall resolve to the deterministic evidence described in section 8.2. A condition-checklist entry contains exactly `condition`, `status`, and `evidence_references` and follows section 8.4.

Unknown properties, unknown enum values, duplicate identifiers, empty required strings, invalid references, and unrecognized coverage values are invalid.

### 10.2 Review record

Create `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md` as the human-readable decision record. It shall derive its directional dispositions, gate results, coverage totals, and probe totals from the matrix rather than restating independent hand-maintained values.

The record shall state prominently that a `GO` authorizes design only and that no mapping snapshot exists.

### 10.3 Traceability and tests

Create:

- `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-traceability.md`; and
- `tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py`.

Tracked traceability shall remain non-self-referential. Exact candidate SHA, reviewer dispositions, GitHub check results, and merged-main SHA belong in pull-request or check evidence.

Tracked traceability shall record the broker protocol and fallback, direction-ordered prompt digests, common-input digest, analyst identities and attestations, receipt timestamps, accepted payload digest references, recomputed direction-content digests, and the closed accepted reconciliation. It shall not contain discarded payload content or digests, correction/supersession fields, controller-mailbox contents, or filesystem paths for analyst output because analyst output files are prohibited.

### 10.4 Navigation and queue

Modify only as required:

- `crosswalks/uk-cyber-essentials.md` to publish the two directional decisions and link the review artifacts without implying a mapping exists; and
- `project/BACKLOG.md` to queue direction-specific mapping design only for a `GO`, explicit evidence acquisition for a `HOLD`, or no mapping design for a `NO_GO`.

## 11. Validation and failure handling

Tests shall fail closed on:

- oracle path, digest, version, count, or atomization-rule drift;
- disagreement between the source-inventory traceability digest table and LF-normalized tracked artifact bytes;
- source-derived analysis committed before rights re-attestation;
- role-identity collisions, nonconcurrent dispatch, non-`none` forks, filesystem analyst output, unavailable private mailbox semantics without the fail-closed fallback, controller disclosure before both receipts, or analysts seeing sibling content;
- missing prompt/common-input/receipt provenance, noncanonical payloads, invalid submission or direction-content digests, any correction or supersession mechanism, post-seal changes, an invalid pair retained instead of discarded together, or reconciliation that is not fully `ACCEPTED`;
- missing or extra directions, gates, groups, kinds, actors, or special scenarios;
- special-scenario claims without direction-local provision/anomaly/assurance-limit bindings;
- invalid provision, control, probe, evidence, or cross-reference identifiers;
- a positive result without exact ESAF normative basis;
- a condition that supplies a missing outcome;
- a `GO`, `HOLD`, or `NO_GO` inconsistent with section 7;
- copied source passages or duplication of the anomaly literal;
- IASME-derived structure or text without a separately approved basis;
- prohibited inference or affirmative overclaiming language;
- any changed path beneath `crosswalks/mappings/` or `crosswalks/registry/` relative to the branch base;
- prohibited mapping fields in feasibility artifacts;
- incomplete external-to-ESAF positive condition checklists or checklist evidence that does not resolve;
- hand-maintained review totals, including per-direction group, kind, actor, or special-scenario totals, that disagree with values derived from valid probe bindings; or
- broken links, encoding corruption, cache files, source downloads, renderings, or scratch artifacts in the repository.

Source identity or oracle drift stops the review. A direction-local rights conflict or resolvable evidence gap encoded as a `BLOCKED` gate and prerequisite in the sealed submission produces `HOLD`; it shall not be guessed through. A structural semantic failure or absence of every defensible positive probe produces `NO_GO`. A new source version requires a new source-versioned review.

## 12. Review, integration, and publication gates

Before publication, run:

- the focused go/no-go contract tests;
- the complete test suite;
- controls, architectures, crosswalk, and repository-local link validators;
- whole-branch `git diff --check`;
- cache, scratch, source-download, and rendered-artifact checks; and
- a clean-worktree check.

Dispatch two independent reviews on one immutable exact head:

1. specification/methodology review of decision mechanics, oracle coverage, ESAF normative citations, schema fit, and absence of mapping artifacts; and
2. security/overclaiming review of rights sequencing, copied-source protection, IASME partition, asymmetric direction semantics, assurance limits, and prohibited claims.

Resolve all Critical and Important findings. Any candidate change invalidates both exact-head reviews and requires full gate reruns and both redispatches.

The pull-request head shall equal the reviewed SHA, required GitHub checks shall pass on that SHA, and merge state shall be clean. Integration shall use a true merge commit; squash and rebase integration are prohibited. Immediately before merge, automation shall verify the configured merge method, rights-record ancestry to the reviewed head, and that the resulting integration commit will preserve the feature history. After merge it shall require exactly the expected first-parent/base parent and feature-head parent ancestry before post-merge validation. Post-merge validation shall run on the resulting `main` SHA before temporary branches, worktrees, and verified external scratch material are removed.

## 13. Acceptance criteria

The milestone is complete when:

1. the exact locked public v3.2 oracle is the only external decision universe;
2. the source-inventory traceability digest table matches every LF-normalized tracked artifact and is protected by regression coverage;
3. `esaf_to_external` and `external_to_esaf` have concurrently authored broker-private submissions with `fork_turns="none"`, no output files, both-receipt withholding, prompt/common-input/receipt digests and timestamps, and a fail-closed isolation fallback;
4. each direction records all seven gates and one mechanically derived `GO`, `HOLD`, or `NO_GO` disposition;
5. each direction covers all ten groups, seven kinds, five actors, and nine special scenarios through valid direction-local evidence bindings, and the renderer derives and displays each per-axis total;
6. every positive probe cites exact normative ESAF control text through stable locators;
7. conditions do not create missing outcomes;
8. rights re-attestation precedes committed source-derived feasibility analysis and preserves the IASME partition;
9. no mapping snapshot, lifecycle record, mapping record, relationship leg, generated mapping statistic, or authoritative mapping field is created;
10. a `GO` authorizes only a separate direction-specific mapping design;
11. positive identifiers and dispositions are derived from each immutable sealed direction; `GO`, `HOLD`, and `NO_GO` enforce their exact prerequisite and trigger invariants, and no cross-direction disagreement rule exists;
12. narrative and backlog outputs are derived from the matrix and preserve all prohibited-inference boundaries;
13. focused and full tests, all validators, diff checks, artifact checks, and clean-worktree checks pass;
14. exact-SHA specification/methodology and security/overclaiming reviews have no unresolved Critical or Important findings; and
15. the reconciler only validates and packages two accepted sealed payloads, both committed direction-content digests recompute exactly, and invalid pairs are discarded and freshly redispatched; and
16. PR-head, GitHub-check, merge-state, integration, and post-merge evidence are recorded externally without making tracked traceability self-referential.
