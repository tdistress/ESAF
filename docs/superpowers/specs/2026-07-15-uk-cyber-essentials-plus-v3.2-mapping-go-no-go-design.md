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

The directional disposition shall be derived mechanically:

- `GO` requires all seven gates to be `PASS`, at least one defensible positive feasibility probe, no unresolved analyst disagreement, and empty prerequisites.
- `HOLD` requires no `FAIL` gate and at least one `BLOCKED` gate or unresolved analyst disagreement. It shall record one or more specific, externally resolvable prerequisites and the evidence required for re-entry.
- `NO_GO` requires at least one `FAIL` gate or no defensible positive feasibility probe after the complete adversarial probe set. It shall record the structural reason and a source, methodology, or framework change that could justify reconsideration.

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

### 8.3 Probe conclusions

Each probe receives exactly one conclusion:

- `POSITIVE_FEASIBILITY`: exact normative evidence supports a prospective, bounded relationship in the stated direction;
- `NO_POSITIVE_BASIS`: the reviewed material does not supply a direct normative basis; or
- `INDETERMINATE`: a named resolvable prerequisite prevents a defensible conclusion.

These values are feasibility conclusions, not ESAF-1600 mapping dispositions. The artifacts shall not encode relationship, coverage, or confidence values.

## 9. Roles and independence

The milestone shall identify:

- one `esaf_to_external` analyst;
- one different `external_to_esaf` analyst;
- one reconciler different from both analysts;
- one rights reviewer different from both analysts; and
- two exact-head reviewers: specification/methodology and security/overclaiming.

Each directional analyst shall receive the approved design, locked oracle, ESAF controls, and ESAF-1600 method. Neither analyst shall see the other direction's provisional disposition, gate statuses, probe conclusions, or counts before submitting their own result.

The reconciler shall disposition every disagreement, missing coverage axis, unsupported citation, and conclusion difference. An unresolved disagreement produces `HOLD` for the affected direction.

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
- `direction_assessments`: array; and
- `probes`: array.

`source_oracle` shall contain exactly the repository-relative path, SHA-256, source version, expected provision count, atomization-rule version, and public-document-only scope statement.

`rights_re_attestation` shall contain exactly record path, record commit, reviewer, review date, prior rights commit, oracle SHA-256, publication basis covered, IASME partition preserved, copied-source prohibition preserved, field classes reviewed, and disposition. Its disposition shall be `approved`. Tests shall prove that the record commit changed only the re-attestation record and is an ancestor of the first commit containing any probe, directional gate result, or provisional disposition.

`roles` shall contain exactly the two directional analysts and reconciler. Tests shall enforce the independence rules in section 9.

`coverage_contract` shall contain exactly the ordered groups, kinds, actors, and special scenarios in section 8.

`direction_assessments` shall contain exactly two objects in the direction order in section 3.2. Each contains exactly direction, analyst, question, gate results, positive-probe identifiers, disposition, decision rationale, prerequisites, and reconsideration triggers.

Each gate-result object contains exactly gate identifier, status, rationale, and evidence references. Evidence references shall resolve to probe identifiers, repository-relative source paths with stable locators, or official URLs already approved as bibliographic facts.

Each probe contains exactly:

- `probe_id`;
- `direction`;
- `provision_ids`;
- `selection_basis`;
- `groups`;
- `kinds`;
- `actors`;
- `special_scenarios`;
- `esaf_normative_bases`;
- `semantic_fit_analysis`;
- `assurance_and_overclaiming_risks`;
- `source_rights_and_operational_limits`;
- `conclusion`; and
- `rationale`.

An ESAF normative-basis entry contains exactly control identifier, requirement locator, and original concise relevance analysis. `POSITIVE_FEASIBILITY` requires at least one normative-basis entry. `NO_POSITIVE_BASIS` may use an empty array and shall state the missing outcome. `INDETERMINATE` shall state the blocking prerequisite in the corresponding directional assessment.

Unknown properties, unknown enum values, duplicate identifiers, empty required strings, invalid references, and unrecognized coverage values are invalid.

### 10.2 Review record

Create `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md` as the human-readable decision record. It shall derive its directional dispositions, gate results, coverage totals, and probe totals from the matrix rather than restating independent hand-maintained values.

The record shall state prominently that a `GO` authorizes design only and that no mapping snapshot exists.

### 10.3 Traceability and tests

Create:

- `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-traceability.md`; and
- `tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py`.

Tracked traceability shall remain non-self-referential. Exact candidate SHA, reviewer dispositions, GitHub check results, and merged-main SHA belong in pull-request or check evidence.

### 10.4 Navigation and queue

Modify only as required:

- `crosswalks/uk-cyber-essentials.md` to publish the two directional decisions and link the review artifacts without implying a mapping exists; and
- `project/BACKLOG.md` to queue direction-specific mapping design only for a `GO`, explicit evidence acquisition for a `HOLD`, or no mapping design for a `NO_GO`.

## 11. Validation and failure handling

Tests shall fail closed on:

- oracle path, digest, version, count, or atomization-rule drift;
- disagreement between the source-inventory traceability digest table and LF-normalized tracked artifact bytes;
- source-derived analysis committed before rights re-attestation;
- role-identity collisions or analysts seeing the other provisional result before submission;
- missing or extra directions, gates, groups, kinds, actors, or special scenarios;
- invalid provision, control, probe, evidence, or cross-reference identifiers;
- a positive result without exact ESAF normative basis;
- a condition that supplies a missing outcome;
- a `GO`, `HOLD`, or `NO_GO` inconsistent with section 7;
- copied source passages or duplication of the anomaly literal;
- IASME-derived structure or text without a separately approved basis;
- prohibited inference or affirmative overclaiming language;
- any changed path beneath `crosswalks/mappings/` or `crosswalks/registry/` relative to the branch base;
- prohibited mapping fields in feasibility artifacts;
- hand-maintained review totals that disagree with the matrix; or
- broken links, encoding corruption, cache files, source downloads, renderings, or scratch artifacts in the repository.

Source identity or oracle drift stops the review. A rights conflict, unresolved analyst disagreement, or resolvable evidence gap produces `HOLD`; it shall not be guessed through. A structural semantic failure or absence of every defensible positive probe produces `NO_GO`. A new source version requires a new source-versioned review.

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

The pull-request head shall equal the reviewed SHA, required GitHub checks shall pass on that SHA, and merge state shall be clean. Integration shall preserve any rights re-attestation sequencing required by the implementation plan. Post-merge validation shall run on the resulting `main` SHA before temporary branches, worktrees, and verified external scratch material are removed.

## 13. Acceptance criteria

The milestone is complete when:

1. the exact locked public v3.2 oracle is the only external decision universe;
2. the source-inventory traceability digest table matches every LF-normalized tracked artifact and is protected by regression coverage;
3. `esaf_to_external` and `external_to_esaf` have separate, independently authored assessments;
4. each direction records all seven gates and one mechanically derived `GO`, `HOLD`, or `NO_GO` disposition;
5. each direction covers all ten groups, seven kinds, five actors, and nine special scenarios;
6. every positive probe cites exact normative ESAF control text through stable locators;
7. conditions do not create missing outcomes;
8. rights re-attestation precedes committed source-derived feasibility analysis and preserves the IASME partition;
9. no mapping snapshot, lifecycle record, mapping record, relationship leg, generated mapping statistic, or authoritative mapping field is created;
10. a `GO` authorizes only a separate direction-specific mapping design;
11. `HOLD` and `NO_GO` outcomes record explicit re-entry or reconsideration evidence;
12. narrative and backlog outputs are derived from the matrix and preserve all prohibited-inference boundaries;
13. focused and full tests, all validators, diff checks, artifact checks, and clean-worktree checks pass;
14. exact-SHA specification/methodology and security/overclaiming reviews have no unresolved Critical or Important findings; and
15. PR-head, GitHub-check, merge-state, integration, and post-merge evidence are recorded externally without making tracked traceability self-referential.
