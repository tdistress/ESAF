# Cyber Essentials Plus v3.2 external-to-ESAF mapping traceability

## Candidate boundary

This record covers mapping set `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`. The snapshot is a complete-publication, unqualified technical draft for the pinned public NCSC v3.2 source. Complete-publication means inventory coverage only. It is not the current operational scheme and does not establish assessment execution, certification, compliance, equivalence, endorsement, implementation, effectiveness, aggregate sufficiency, full-population assurance, current-scheme completeness, or continuous assurance.

- Direction: reverse-only `external_to_esaf`
- Lifecycle: draft, `events: []`
- Immutable ESAF baseline: `7461d7137e3faf36b2b73a15f71100fa4ce11159`
- Pinned controls: 91
- Snapshot digest: `460b14fafb2dd8b2ac041cba5a2ec5216cb6fec4fae14ec7b6e3ee89416c2599`
- Oracle: `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`
- Oracle SHA-256: `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`
- Canonical PDF SHA-256: `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`
- Legacy PDF SHA-256: `d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694`
- Rights ancestry: feasibility rights commit `4207e1c1e8ff9f743274ebb4b626210cca053458` and the committed 2026-07-19 external-to-ESAF mapping-rights attestation

## Inventory and derived totals

The oracle and snapshot contain exactly 144 records across M 24, T1 16, S 11, T2 9, T3 37, T4 9, T5 7, C 13, A 4, and B 14. The records contain 32 mapped provisions, 32 relationship legs referencing 10 distinct controls, and 112 no-direct-mapping dispositions. Every relationship is `partially_supports` and `external_to_esaf`; there is no forward or bidirectional leg in this snapshot.

Repository totals derived from all three mapping sets are 3 mapping sets, 404 provisions, 81 relationships, and 325 negative dispositions.

## Reconciliation

All 144 records were checked against the locked oracle and 91-control manifest for identifiers, record uniqueness, group and kind taxonomy, actors, summaries, source locators, draft status, disposition, relationship direction and taxonomy, positive control targets, control version, path, digest, requirement locator, conditions, expected evidence, known gaps, prohibited inferences, and negative specificity.

The complete audit found no omitted, extra, or duplicate provision; no taxonomy drift; no unsupported adjacent-control target; no copied five-word source window; no stale manifest binding; no forward or bidirectional leg; no duplicate relationship; no generic or repeated negative rationale; no condition-created external or ESAF outcome; and no contradiction between disposition and relationship presence. All 32 positive legs have the ordered 11-condition contract with nonempty evidence references. All 112 negatives are provision-specific, unique, and relationship-free.

The structured observation profiles remain outcome-neutral measurements. They do not convert tool or assessor activity, administrative artifacts, recommendations, aggregate rules, or adjacent procedures into ESAF evidence. In particular, T5-006 remains a bounded privileged-access observation and T1-009 records a dated severity measurement without supplying an implementation, effectiveness, risk-verdict, certification, compliance, or equivalence claim.

## Publication metadata

The snapshot README, lifecycle registry, generated catalog, UK landing page, and backlog now use the record-derived totals above. The landing page preserves the go/no-go statements as feasibility-time history while separately identifying both implemented draft directions. Only the completed external-to-ESAF design item was removed from `project/BACKLOG.md`; unrelated initiatives remain.

The snapshot, all records and relationships, and lifecycle remain draft. Every mapped observation is point-in-time evidence limited by its dated population, sample, method, provenance, exception, and Delivery Partner conditions. Qualified SME review and any lifecycle transition remain future work.

## Test-driven reconciliation evidence

The whole-snapshot tests were added before publication metadata changed. The initial run passed the 144-record reconciliation and failed because the reverse README still said that no records or relationship legs had been authored. A separate backlog regression failed while the completed `external_to_esaf` item remained. Both passed after the metadata changes. A later regression exposed current-tense feasibility text saying the reverse mapping remained unimplemented; the landing page was corrected to explicit feasibility-time history. Finally, independent review identified that this candidate-owned traceability record was missing; a focused test failed on that absence before this file was added.

The contract now derives and locks the record, mapped, negative, relationship-leg, and distinct-control counts; exact positive target set; reverse-only direction; oracle metadata; source locators; manifest provenance; relationship taxonomy; ordered condition completeness; expected evidence and gap presence; prohibited-inference completeness; negative specificity and uniqueness; copied-source windows; prohibited affirmative assurance language; lifecycle/catalog equality; generated repository totals; navigation; historical feasibility context; backlog scope; and independent reviewer identity closure when review reports are present.

## Pre-review verification

The mapping content immediately before this candidate-owned traceability record was commit `46af68e1ed262fb8ad9bfedac2280b9eaf656e08`, over merge-base `e4de0a5d3801431d96e49a746069834fa0b4d370`. Both first-pass independent reviewers inspected that exact content commit and reported no mapping-content finding. They stopped report authoring after the specification/inventory reviewer identified the missing traceability record as Important I-1.

The following commands and results were recorded on that unchanged content commit with `PYTHONDONTWRITEBYTECODE=1` for Python commands:

- `python -m unittest tests.test_uk_cyber_essentials_plus_v32_external_to_esaf_mapping -v` — 63 tests passed.
- `python tools/validate_crosswalks.py --check` — valid; 3 mapping sets, 404 provisions, 81 relationships, and 325 negative dispositions.
- `python tools/validate_crosswalks.py --check --baseline-ref e4de0a5d3801431d96e49a746069834fa0b4d370` — valid with the same derived totals.
- `git diff --check e4de0a5d3801431d96e49a746069834fa0b4d370..46af68e1ed262fb8ad9bfedac2280b9eaf656e08` — passed with no output.

No Mermaid diagram was introduced or affected by this task. Final report-inclusive exact-head gates and both exact-head reviewer verdicts are recorded outside this non-self-referential file in the draft pull-request description and ignored task evidence. Any report-inclusive byte change invalidates that evidence and requires both reviewers and affected gates to run again.

## Review boundary

This record documents technical traceability only. It does not claim qualified SME review, lifecycle approval, certification, compliance, equivalence, current-scheme completeness, implementation, effectiveness, aggregate sufficiency, population-wide coverage, or continuous assurance.
