# Cyber Essentials Plus v3.2 ESAF-to-external mapping traceability

## Candidate boundary

This record describes the content candidate for mapping set `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`. The snapshot is a complete-publication, unqualified technical draft for the pinned public NCSC v3.2 source. Complete-publication describes inventory coverage only. It is not the current operational scheme and does not claim qualified review, approval, assessment execution, certification, compliance, equivalence, endorsement, current-scheme completeness, full-population assurance, or continuous assurance.

- Direction: forward-only `esaf_to_external`
- Lifecycle: draft, `events: []`
- Immutable ESAF baseline: `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`
- Pinned controls: 91
- Rights ancestry: feasibility rights commit `4207e1c1e8ff9f743274ebb4b626210cca053458`, followed by the committed mapping-rights attestation
- Oracle: `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`
- Oracle SHA-256: `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`
- Canonical PDF SHA-256: `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`

## Inventory and derived totals

The oracle and snapshot contain exactly 144 records across all ten completed groups: M 24, T1 16, S 11, T2 9, T3 37, T4 9, T5 7, C 13, A 4, and B 14. The kind distribution is 43 procedure steps, 21 decision rules, 21 applicability records, 20 result rules, 19 prerequisites, 18 recommendations, and 2 evidence-retention records.

The records contain 8 relationship legs referencing 7 distinct controls and 137 no-direct-mapping dispositions. All relationships are `partially_supports`, use `esaf_to_external`, and retain exact manifest provenance, explicit conditions, expected evidence, known gaps, and prohibited inferences. Conditions narrow exact normative support and do not create a missing outcome.

Repository catalog totals derived from both mapping sets are 2 mapping sets, 260 provisions, 49 relationships, and 213 negative dispositions.

## Batch ancestry and review closure

The candidate consumes the committed M, T1, S, T2, T3-001-019, T3-020-037, T4, T5, C, and A-B batches and both independent batch reviews for each. Every batch report records technical closure with no unresolved Critical or Important finding. The mapper, publication-rights reviewer, and batch reviewers used authorized access to the pinned source boundary. Final candidate-wide specification and security/overclaiming reports are intentionally absent at this stage and remain reviewer-owned artifacts.

The mapping-rights attestation precedes snapshot creation and preserves attribution, the Open Government Licence v3.0 basis, the copied-source prohibition, the IASME partition, source-version separation, and excluded marks, imagery, and third-party material.

## Reconciliation

All 144 records were checked against the oracle and 91-control manifest for identifiers, group and kind metadata, actors, summaries, source locators, record status, relationship provenance, taxonomy, direction, and narrative completeness. The cross-record audit found no non-oracle record, duplicate control/direction leg, empty provenance field, reverse relationship, generic negative rationale, source-copy window, feasibility-text reuse, condition-created outcome, unsupported adjacency, or cross-batch taxonomy contradiction. One exact repeated prohibited-inference sentence occurs in T1-011 and T1-013; it states the same mandatory boundary for two credential-related legs and is retained as applicable control language rather than record rationale boilerplate.

Aggregate reconciliation confirms that the eight narrow legs do not combine into procedure execution, observed results, population or sample coverage, aggregate sufficiency, certification, compliance, equivalence, current-scheme completeness, full-population assurance, or continuous assurance.

## Changed publication artifacts

The content candidate changes the whole-snapshot test contract, the snapshot README, generated lifecycle digest and catalogs, the UK landing page, this traceability record, and the authorized forward-design backlog entry. It does not alter the oracle, inventory, control manifest, source material, schema, validator, separate `external_to_esaf` design item, or final-review reports.

## Precommit verification

The final generated snapshot digest is `284daa76427b88b11a8db0d317ba443061693b52efdb7999a3b928207c0a04b6`.

Pass 1: 35 focused tests passed; 330 full-suite tests passed; 3 skipped. It began with `python tools/validate_crosswalks.py --write` and then passed every required gate. `validate_controls.py --check` reported 91 controls, 91 objectives, and 16 families; `validate_architectures.py` reported 10 foundation files and 7 reserved patterns; `migrate_control_mappings.py --check` reported 91 catalog-derived control mapping sections (0 changed); both `python tools/validate_crosswalks.py --check` and `python tools/validate_crosswalks.py --check --baseline-ref b4529c05c440db2f94ec12db4f21e3d0af57a5fb` reported 2 mapping sets, 260 provisions, 49 relationships, and 213 negative dispositions; `validate_links.py --check` reported 502 tracked Markdown files; and `git diff --check` passed.

Pass 2 reran the check-only bundle against unchanged bytes and passed every gate with the same derived results: Pass 2: 35 focused tests passed; 330 full-suite tests passed; 3 skipped. `validate_controls.py --check` reported 91 controls, 91 objectives, and 16 families; `validate_architectures.py` reported 10 foundation files and 7 reserved patterns; `migrate_control_mappings.py --check` reported 91 catalog-derived control mapping sections (0 changed); both crosswalk checks reported 2 mapping sets, 260 provisions, 49 relationships, and 213 negative dispositions; `validate_links.py --check` reported 502 tracked Markdown files; and `git diff --check: passed`.

The staged candidate scope was the authorized snapshot README prefix, registry digest, catalog, landing page, traceability record, forward-design backlog removal, focused mapping contract, and the owner-authorized necessary `tests/test_release_metadata.py` contract update. No final-review report, source material, oracle, inventory, schema, validator, or separate `external_to_esaf` design item was staged.

During recovery, the full suite exposed an obsolete backlog expectation and historical landing-page assertions. The release-metadata contract was updated because the separately authorized forward design item is complete and removed. The inventory contract and its digest-locked 2026-07-14 traceability evidence were preserved: under one explicit feasibility-time qualifier, the landing page retains both historical statements that no mapping and no mapping snapshot existed, while the immediately preceding paragraph explicitly presents the current draft. No historical checksum or review artifact was changed.

No statement in this traceability record claims qualified review or lifecycle approval.
