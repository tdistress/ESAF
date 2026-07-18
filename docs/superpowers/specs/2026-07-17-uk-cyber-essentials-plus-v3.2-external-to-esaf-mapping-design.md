# UK Cyber Essentials Plus v3.2 External-to-ESAF Mapping Design

**Status:** Approved for implementation planning

**Date:** 2026-07-17

**Target:** ESAF-1600 complete-publication reverse-evidence draft mapping set

## 1. Purpose

This design defines a complete-publication mapping set from the 144 provisions in the pinned public NCSC *Cyber Essentials Plus Test Specification* v3.2 oracle to exact ESAF 0.4-alpha control requirements.

The mapping answers one direction-specific evidence question: can a defined observation or result produced while performing one external provision materially support evaluation of an exact ESAF control outcome, under explicit conditions? A relationship is evidence for an evaluator, not evidence that an ESAF control is implemented, continuously effective, complete, certified, compliant, equivalent, endorsed, current-scheme complete, or fully population-assured.

This is a separate mapping set from the published `esaf_to_external` analysis. Neither set derives relationships, dispositions, evidence, statistics, or assurance from the other.

## 2. Decision and alternatives

The selected approach reuses the existing ESAF-1600 record schema with direction `external_to_esaf` and adds a strict, source-versioned reverse-evidence authoring and validation profile. It creates no new shared relationship type and no schema extension.

Two alternatives are rejected:

- a new evidence-specific relationship taxonomy, because the existing direction, relationship, condition, expected-evidence, known-gap, requirement-locator, and prohibited-inference fields can express the bounded claim while a shared-schema change would add unnecessary migration and review scope; and
- narrative-only guidance, because it would not provide provision-level traceability, a complete inventory, machine validation, derived counts, or auditable negative dispositions.

The existing relationship labels retain their ESAF-1600 meanings. They must never be used to turn an assessment procedure, a sample, a file, a score, an authorization, or an overall scheme result into evidence of an unobserved ESAF outcome.

## 3. Authority and baseline boundary

The external-source authority, version, publication dates, official URLs, source-PDF digests, locked provision oracle, oracle digest, rights record, public-source partition, and known-anomaly handling shall be exactly those established by the forward mapping design at `docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-design.md` sections 3 and 4.

The mapping shall use ESAF release `0.4-alpha` and pin one immutable full source commit before record authoring. `ESAF_CONTROL_MANIFEST.json` shall be deterministically generated from that commit. Every relationship shall resolve to the manifest's exact control ID, version, path, digest, and `## Requirement` locator. A changed ESAF baseline requires a new mapping-set version.

The mapping shall not import private Delivery Partner material, the current operational Cyber Essentials Plus scheme, core Cyber Essentials v3.3 requirements, IASME-authored structure beyond the established public partition, source downloads, or unapproved copied source text.

## 4. Mapping-set identity and layout

The implementation plan shall reserve an independent source-versioned mapping-set identifier and snapshot root beneath:

`crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/`

The final version suffix shall be selected by the implementation plan and must differ from the forward snapshot's `0.1.0` identity. The snapshot shall contain exactly a README, `PROVISION_INVENTORY.md`, `ESAF_CONTROL_MANIFEST.json`, and 144 direct-child provision records. No subdirectories, symbolic links, source downloads, analyst submissions, caches, scratch files, or auxiliary data files are allowed.

The mapping set shall have its own lifecycle registry entry, generated catalog entry, UK landing-page navigation, traceability report, specification/inventory review, and security/overclaiming review. All snapshot records and lifecycle state remain `draft` until qualified human review; Codex review must not populate qualified reviewer or approver fields or advance lifecycle state.

## 5. Complete-publication inventory

The scope is all 144 oracle provisions, in locked oracle order and at the locked atomization granularity. Each provision has exactly one inventory entry and one provision record. Lowercase ESAF record IDs are mechanically derived from punctuation-sensitive oracle identifiers, such as `CEPTS3.2-T5-006` to `cepts32-t5-006`; they are stable ESAF citation identifiers and do not imply NCSC endorsement.

| Group | Count |
|---|---:|
| `M` | 24 |
| `T1` | 16 |
| `S` | 11 |
| `T2` | 9 |
| `T3` | 37 |
| `T4` | 9 |
| `T5` | 7 |
| `C` | 13 |
| `A` | 4 |
| `B` | 14 |
| **Total** | **144** |

Omission is invalid, is never a negative disposition, and shall not be interpreted as an assessment. No non-oracle record may be added. `out_of_scope` is reserved for a demonstrated analytical-scope exclusion and is not a substitute for a missing ESAF outcome; this complete-publication scope expects zero such records unless separately justified.

## 6. Provision record and reverse-evidence contract

Each record shall conform to the current ESAF-1600 mapping-record schema, use status `draft` and granularity `requirement`, bind exactly one oracle provision and its approved original paraphrase, preserve the applicable oracle metadata and official source URL, identify an authorized mapper, and contain one authoring-version change-history entry.

`mapped` requires at least one relationship leg. `no_direct_mapping` and `out_of_scope` require an empty relationship list and a precise rationale naming the missing observable ESAF outcome or genuine scope boundary.

Each relationship shall use direction `external_to_esaf`, resolve an exact ESAF requirement through the pinned manifest, and record relationship type, coverage, confidence, provision-specific rationale, conditions, expected evidence, known gaps, and prohibited inferences. A relationship may state only that the defined external evidence materially supports evaluation of the cited ESAF requirement under its conditions. It must not assert control operation, sufficiency, effectiveness, certification, compliance, equivalence, or continuous assurance.

Positive legs require both:

1. exact normative ESAF requirement text that defines the outcome being evaluated; and
2. an identified external observation or result that bears on that outcome.

Similarity, an assessment step, an applicability label, evidence retention, complete assessment-file handling, a tool authorization, a decision rule, a score, a sample, a certification outcome, or generic security value is not a positive basis by itself.

## 7. Mandatory evidence conditions

Every positive leg shall contain a closed condition checklist in this exact order:

1. `actor`
2. `scope`
3. `population`
4. `sample`
5. `assessment_date`
6. `evidence_date`
7. `tool`
8. `provenance`
9. `exception`
10. `delivery_partner_discretion`
11. `point_in_time_status`

Each entry shall contain exactly `condition`, `status`, and nonempty `evidence_references`. Status shall be `SATISFIED` or `NOT_APPLICABLE`. `NOT_APPLICABLE` requires evidence explaining why the condition cannot affect the bounded claim. Conditions may narrow a relationship already supported by the external result and exact ESAF requirement; they shall never create a missing result or missing ESAF outcome.

The record contract shall retain all 11 conditions in human-readable relationship content and the implementation validation contract shall make absence, reordering, empty evidence references, unresolved references, or unjustified non-applicability fail closed.

## 8. Provision-first authoring and negative boundaries

For every oracle provision, the mapper shall:

1. load the locked provision metadata, approved paraphrase, source locator, and applicable assurance boundary;
2. identify candidate ESAF controls only through the release-pinned manifest;
3. identify whether the provision can yield a defined observation or result rather than only an administrative, procedural, or scheme-decision artifact;
4. compare that observation or result with exact ESAF normative requirement text;
5. create independently justified relationship legs only where both positive criteria in section 6 are met; otherwise create a specific negative disposition; and
6. run focused validation before the record joins a completed authoring batch.

Candidate-discovery automation may rank candidates, but it shall not write dispositions or relationship legs. The mapper makes every analytical decision; a distinct qualified reviewer with authorized source access later reviews it.

The implementation shall apply adversarial negative review to scope, population and sampling, assessment and evidence dates, tool and provenance, exception handling, Delivery Partner discretion, point-in-time status, evidence retention and files, procedure execution, result aggregation, the known anomaly, core v3.3 separation, and provisions with no exact ESAF outcome.

The feasibility probe involving T5-006 and IAM-130 is a design seed only. It shall be independently reassessed using the final record contract; feasibility does not preapprove a relationship or evidence claim.

## 9. Generated outputs and lifecycle

Implementation shall regenerate `crosswalks/catalog.json` and `crosswalks/CATALOG.md` only through the existing crosswalk generator. The UK Cyber Essentials landing page shall link the distinct reverse snapshot, identify the 144-provision complete-publication inventory target, distinguish draft from reviewed coverage, and preserve the public-v3.2/current-scheme boundary.

Published statistics shall be generated from records and manifests and shall keep separate the pinned provision population, mapped and negative dispositions, relationship-leg total, distinct ESAF controls referenced, and direction-specific totals. Narrative must not aggregate positive legs into a compliance, effectiveness, coverage, certification, or assurance claim.

After every candidate change, affected generated artifacts and exact-head reviews must be rerun. The backlog item remains until a separately authorized implementation has merged; this design and its plan do not authorize mapping-record implementation, publication, or lifecycle promotion.

## 10. Validation, review, and acceptance criteria

Focused tests and validators shall enforce at least:

- exact mapping-set identity, root, source version, oracle digest, and ESAF baseline;
- exactly 144 records and inventory entries with the locked group counts;
- one-to-one record, inventory, and oracle metadata binding with no non-oracle records;
- `draft` lifecycle and no unauthorized lifecycle events;
- reverse-only `external_to_esaf` legs;
- manifest resolution for every cited ESAF requirement;
- the exact ordered 11-condition checklist and condition evidence requirements for every positive;
- provision-specific negative rationales and empty relationships for negative dispositions;
- conditions-only-narrow semantics and prohibited-inference boundaries;
- no copied source, protected material, current-scheme, core-v3.3, compliance, certification, equivalence, full-population, continuous-assurance, or unobserved-implementation claim;
- deterministic catalog generation, valid navigation and links, and absence of unexpected snapshot files; and
- derived-count consistency between records, manifests, catalogs, and narrative.

Required gates include focused tests, the full suite, control and architecture validators, crosswalk validation with a trusted baseline, migration checks where applicable, link validation, Mermaid rendering for any introduced diagrams, generated-artifact check mode, whole-branch diff checks, and clean-worktree/cache checks.

The final immutable candidate shall receive independent exact-SHA reviews for specification/inventory and security/overclaiming. Critical and Important findings must be resolved; any candidate change invalidates both reviews and requires redispatch. Only a qualified Cyber Essentials SME, distinct from the mapper and with authorized source access, may promote records to `reviewed`.

The implementation milestone is acceptable only when all 144 provisions have one draft record, every positive satisfies the reverse-evidence contract, every negative names the missing basis, generated artifacts reproduce from authoritative records, all required gates pass, and both independent final reviews report no unresolved Critical or Important findings.
