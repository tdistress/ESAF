# UK Cyber Essentials Plus v3.2 ESAF-to-External Mapping Design

**Status:** Approved for implementation planning

**Date:** 2026-07-15

**Target:** ESAF-1600 complete-publication draft mapping set

## 1. Purpose

This design defines a complete-publication mapping set from ESAF 0.4-alpha controls to the 144 provisions in the pinned public NCSC *Cyber Essentials Plus Test Specification* v3.2 oracle.

The mapping answers one direction-specific analytical question: how does exact normative ESAF control text contribute to an individual public Cyber Essentials Plus v3.2 provision? It does not assess an adopter, establish that a Plus procedure was performed, calculate a compliance percentage, demonstrate a testing result, or establish certification, compliance, equivalence, endorsement, current-scheme completeness, full-population assurance, or continuous assurance.

The reverse `external_to_esaf` direction is excluded. It remains a separate authorized design activity and shall not be inferred from this mapping set.

## 2. Decision and alternatives

The selected approach is contract-first, staged authoring of one complete-publication snapshot. The complete identity, inventory, record contract, review roles, provenance, and fail-closed gates are fixed before provision records are authored. Records may then be implemented in stable provision-group batches while the snapshot remains `draft`.

Two alternatives were rejected:

- sequential provision authoring without a closed snapshot contract, because cross-batch inconsistencies and completeness defects would surface late; and
- control-led candidate generation as the authoritative workflow, because similarity and adjacency can overstate coverage and leave negative dispositions implicit.

Candidate discovery may be automated, but the authoritative workflow remains provision-first and every result requires human-readable analytical justification.

## 3. Source and authority boundary

### 3.1 External source

- Authority: UK National Cyber Security Centre
- Authority identifier: `uk-ncsc`
- Publication: *Cyber Essentials Plus Test Specification*
- Publication identifier: `cyber-essentials-plus-test-specification`
- Source version: `3.2`
- Display date: April 2025
- Resource-page date: 2025-04-28
- Source access date: 2026-07-14
- Official resource page: `https://www.ncsc.gov.uk/cyberessentials/resources`
- Canonical PDF SHA-256: `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`
- Legacy PDF SHA-256: `d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694`
- Locked oracle: `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`
- Locked oracle SHA-256: `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`

The source PDFs are not committed. The oracle is the sole structural source for identifiers, groups, kinds, actors, locators, approved original summaries, source-version boundaries, and the recorded anomaly. The mapping shall not import private Delivery Partner material, the current operational scheme, core Cyber Essentials v3.3 requirements, or IASME-authored structure.

The known source anomaly may be referenced only by its oracle identifier and locator. It shall not be duplicated, expanded into additional provisions, or used to create a relationship.

### 3.2 ESAF baseline

- ESAF release identifier: `0.4-alpha`
- ESAF label: `ESAF 0.4-alpha`
- Initial design baseline: `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`
- Control count: 91

Implementation shall pin one immutable full source commit and deterministically generate `ESAF_CONTROL_MANIFEST.json` from that Git object. Each relationship shall resolve to the pinned control version, path, digest, and exact `## Requirement` locator in the manifest. A later change to the control baseline requires a new mapping-set version rather than silent rebinding.

## 4. Publication rights

The source is Crown copyright material available under the Open Government Licence v3.0, subject to the oracle's recorded restrictions. The design binds to the locked oracle rights record and the mapping-feasibility re-attestation at commit `4207e1c1e8ff9f743274ebb4b626210cca053458`.

Before provision authoring, an independent mapping-rights gate shall confirm that the exact snapshot fields are covered, including identifiers, titles where used, structural inventory, original paraphrases, derivative mapping analysis, ESAF normative citations, assurance analysis, and official links. The gate shall preserve:

- source attribution and the OGL v3.0 link;
- the prohibition on copied requirement or passage text;
- exclusion of third-party material, imagery, logos, marks, and endorsement implications;
- the closed IASME partition, allowing only bibliographic facts, official links, and independently written high-level context; and
- reviewer independence and authorized source access.

The rights decision shall be committed before authoritative provision records. A failed, conditional, stale, or incomplete rights decision blocks authoring.

## 5. Mapping-set identity and layout

The mapping-set identifier is:

`uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`

The authoritative snapshot root is:

`crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0/`

It shall contain exactly:

- `README.md`;
- `PROVISION_INVENTORY.md`;
- `ESAF_CONTROL_MANIFEST.json`; and
- 144 direct-child provision records.

No subdirectory, symbolic link, source download, analyst output, scratch file, or auxiliary data file is permitted beneath the snapshot root.

The lifecycle record is:

`crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0.md`

The snapshot, provision records, and lifecycle remain `draft`; the lifecycle event array remains empty. Codex review shall not populate schema reviewer or approver fields or advance editorial state.

## 6. Complete-publication inventory

The inventory contains all 144 locked oracle provisions in oracle order:

| Group | Record identity | Count |
|---|---|---:|
| `M` | `cepts32-m-*` | 24 |
| `T1` | `cepts32-t1-*` | 16 |
| `S` | `cepts32-s-*` | 11 |
| `T2` | `cepts32-t2-*` | 9 |
| `T3` | `cepts32-t3-*` | 37 |
| `T4` | `cepts32-t4-*` | 9 |
| `T5` | `cepts32-t5-*` | 7 |
| `C` | `cepts32-c-*` | 13 |
| `A` | `cepts32-a-*` | 4 |
| `B` | `cepts32-b-*` | 14 |
| **Total** |  | **144** |

Each lowercase `record_id` is derived mechanically from the corresponding punctuation-sensitive oracle identifier, for example `CEPTS3.2-T5-006` becomes `cepts32-t5-006`. These are ESAF-assigned stable citation identifiers and do not imply NCSC endorsement.

Every oracle provision shall have exactly one inventory entry and exactly one provision record. Omission is invalid and shall not be interpreted as a negative assessment. No record may be added outside the oracle. The inventory scope is `complete_publication` at the oracle's locked atomization granularity.

## 7. Provision record contract

Each provision record shall:

- conform to the current ESAF-1600 provision-record schema;
- use status `draft` and granularity `requirement`;
- match exactly one inventory identifier and oracle record;
- preserve the external identifier, group, kind, actors, locator, and official source URL;
- use only an approved original paraphrase, never copied source text;
- identify the mapper and attest authorized source access;
- contain one authoring-version change-history entry;
- declare exactly one disposition: `mapped`, `no_direct_mapping`, or `out_of_scope`;
- use `out_of_scope` only when the oracle provision is demonstrably outside the declared analytical scope, never as a substitute for missing ESAF coverage; the present complete-publication scope expects zero such records unless separately justified; and
- omit qualified reviewer and approver identities until those actors actually review the record.

`mapped` requires at least one relationship leg and prohibits a negative rationale. `no_direct_mapping` and `out_of_scope` require no relationship legs and a precise rationale naming the missing outcome or scope boundary.

## 8. Provision-first analytical workflow

For each oracle provision, the mapper shall:

1. load the locked identifier, structural metadata, locator, approved summary, and applicable source and assurance limits;
2. identify candidate controls only from the release-pinned ESAF manifest;
3. compare the provision-specific external outcome with exact normative ESAF requirement text;
4. reject similarity, adjacency, implementation guidance, or generic security value as a positive basis;
5. create independently justified relationship legs when direct normative support exists; otherwise record a specific negative disposition; and
6. run focused validation before the record enters a completed authoring batch.

Candidate-discovery automation may rank possible controls but shall not write authoritative dispositions or relationship legs. A mapper shall make every analytical decision, and a separate qualified reviewer with authorized source access shall review it before later promotion.

## 9. Direction and relationship semantics

Every relationship leg shall use direction `esaf_to_external`. Bidirectional or reverse-direction inference is prohibited.

Relationship, coverage, and confidence remain independent:

- `supports`: direct contribution without independent sufficiency;
- `partially_supports`: direct contribution to a defined subset;
- `complements`: adjacent useful outcome that does not provide the provision outcome;
- `prerequisite`: direct condition required before the provision outcome can occur; and
- `informs`: interpretive context without claimed coverage.

Positive relationships require exact normative ESAF text. `complements` and `informs` shall be used sparingly and never to avoid a negative disposition. Multiple partial legs shall not be aggregated into sufficiency. Conditions may narrow a relationship already supported by normative text but shall not create a missing external outcome.

Each leg shall independently record:

- ESAF control ID, version, immutable source path, digest, and requirement locator;
- relationship type, coverage, and confidence;
- provision-specific rationale;
- explicit conditions;
- expected implementation evidence;
- known gaps; and
- prohibited inferences where the relationship could otherwise be overstated.

## 10. Seed and adversarial boundaries

The accepted feasibility result identifies T5-006 with IAM-120 and IAM-130 as a design seed. Implementation shall reassess that candidate using the final schema, pinned manifest, exact provision record, and mapping review process. The feasibility result is process evidence, not an authoritative mapping decision, and does not preapprove either leg.

The design requires adversarial negative testing across:

- assessment scope, population, sample, and dates;
- evidence retention and complete assessment files;
- procedure execution, tools, and provenance;
- decision chains and result aggregation;
- Delivery Partner discretion and both exception predicates;
- the known source anomaly;
- point-in-time versus continuous assurance;
- core v3.3 versus Plus v3.2 source separation; and
- provisions with no exact normative ESAF outcome.

No relationship may imply that a Plus procedure ran, an observation occurred, a population was tested, a result was achieved, or an overall assessment decision followed.

## 11. Batch model

Implementation may proceed by stable oracle group, with one or more groups in a milestone. Each completed batch shall contain an explicit disposition for every provision assigned to that batch, focused tests, and an independent batch review.

Batch completion does not change snapshot completeness or editorial status. Until all 144 records exist and whole-snapshot gates pass, the snapshot remains an incomplete `draft` and shall not be described as publication-wide assessed coverage.

After all group batches, a whole-snapshot reconciliation shall check for:

- duplicated or templated rationales that fail to name the provision outcome;
- inconsistent relationships for materially similar provisions;
- taxonomy, coverage, or confidence drift;
- missing controls or stale manifest bindings;
- conditions that manufacture support;
- cross-batch contradictions; and
- aggregate language that implies sufficiency or assessment results.

## 12. Generated and narrative outputs

Implementation shall update deterministically generated `crosswalks/catalog.json` and `crosswalks/CATALOG.md` only through the existing crosswalk generator. The UK Cyber Essentials landing page shall link the authoritative draft snapshot, identify the 144-provision complete-publication target, distinguish authored from reviewed coverage, and retain the public-v3.2/current-scheme boundary.

The backlog shall remove the completed `esaf_to_external` design item only after the design is merged. It shall not queue implementation unless the repository owner separately approves the implementation plan, mark the mapping as implemented, or collapse the separate `external_to_esaf` activity. This design and its implementation plan do not themselves authorize implementation.

Published narrative shall state that all referenced ESAF controls and mapping records are draft and that the mapping does not establish implementation, certification, compliance, equivalence, endorsement, legal sufficiency, testing success, or current operational scheme coverage.

## 13. Validation and failure behavior

Focused tests shall enforce:

- the exact mapping-set ID, repository path, source version, oracle digest, and ESAF source commit;
- the rights decision's identity, ancestry, independence, and field coverage;
- exactly 144 inventory entries and records with group counts `24/16/11/9/37/9/7/13/4/14`;
- deterministic record IDs and exact inventory-to-record agreement;
- complete oracle metadata binding and absence of non-oracle records;
- draft-only snapshot, record, and lifecycle states with no lifecycle events;
- forward-only `esaf_to_external` legs;
- manifest resolution for every control, version, path, digest, and requirement locator;
- specific negative rationales that name missing outcomes;
- nonempty rationale, conditions, expected evidence, and known gaps for every leg;
- conditions-only-narrow semantics;
- T5-006 seed reassessment without preapproval;
- copied-source and protected-language prohibitions;
- no authoritative reverse-direction, compliance, equivalence, certification, testing-result, full-population, or continuous-assurance claim;
- current generated catalogs and valid links; and
- no source downloads, caches, scratch, analyst outputs, or unexpected snapshot files.

Validation shall fail closed on malformed schemas, duplicate YAML keys, count drift, omissions, orphan records, unknown controls, stale manifests, unauthorized source content, broken links, catalog drift, unresolved high-severity findings, changed reviewed content, or protected claims.

Required candidate gates include focused tests, the full repository suite, controls and architecture validation, crosswalk validation with a trusted baseline, migration checks where mappings affect control metadata, link validation, deterministic catalog regeneration and check mode, whole-branch diff checks, and clean-worktree checks.

## 14. Review and publication

The mapper shall be distinct from both the specification reviewer and security/overclaiming reviewer. The complete immutable candidate receives two independent exact-SHA reviews:

1. specification/methodology review for inventory completeness, record contract, taxonomy, normative citations, manifest provenance, lifecycle state, and catalog derivation; and
2. security/overclaiming review for copied-source protection, IASME partition, source-version separation, directionality, conditions, assurance limits, prohibited inferences, and negative-disposition integrity.

Every Critical and Important finding shall be resolved. Any candidate change invalidates both exact-head reviews and requires redispatch. Only the exact reviewed SHA may be pushed for integration, and required GitHub checks and clean merge state are mandatory.

Independent Codex review establishes technical closure only. Promotion to `reviewed` requires a qualified Cyber Essentials SME who is different from the mapper and has authorized source access. Promotion to `approved` requires a separate approver, complete reviewed records, no disallowed findings, and a valid lifecycle transition.

## 15. Acceptance criteria

The implementation milestone is complete when:

1. The mapping-specific rights gate is committed before provision authoring.
2. The snapshot identity, oracle, source version, and immutable ESAF manifest are exact.
3. All 144 oracle provisions have exactly one authoritative draft record.
4. Every positive leg has exact normative support, independent semantics, explicit conditions, expected evidence, known gaps, and prohibited inference boundaries.
5. Every negative record names the missing outcome or genuine scope boundary.
6. T5-006 is reassessed under the final record contract rather than copied from feasibility analysis.
7. Whole-snapshot reconciliation finds no unresolved contradiction, omission, or overclaiming defect.
8. Generated catalogs and landing-page metadata reproduce from authoritative records.
9. Focused, full-suite, crosswalk, manifest, migration, control, architecture, link, encoding, baseline, diff, cache, scratch, and clean-status gates pass.
10. Two independent exact-head reviewers report no unresolved Critical or Important findings.
11. The merged result remains `draft` pending qualified human review.
12. No reverse-direction mapping, assessment result, implementation claim, or current-scheme completeness claim is created.
