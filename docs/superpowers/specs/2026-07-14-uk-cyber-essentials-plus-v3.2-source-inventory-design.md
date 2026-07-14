# UK Cyber Essentials Plus v3.2 Public-Source Inventory Design

**Status:** Approved for implementation planning

**Design date:** 2026-07-14

**Target:** ESAF-1600 source dossier and atomic provision oracle

**Tracks:** GitHub issue #40

## 1. Purpose

This design defines the source-acquisition and atomization milestone for the public NCSC *Cyber Essentials Plus Test Specification v3.2*. The milestone will produce an independently reconciled, machine-readable oracle of every independently actionable or normative provision in the pinned public PDF.

The milestone does not create a mapping-set snapshot, provision mapping records, ESAF relationship legs, certification claims, or lifecycle events. A later mapping milestone may consume the locked oracle only after the source, rights, completeness, and overclaiming gates in this design pass.

Cyber Essentials core and Cyber Essentials Plus remain separate artifacts. The 116-provision Cyber Essentials core v3.3 inventory defines protection requirements. The Plus v3.2 public specification primarily defines technical assessment procedures, actor duties, sampling, evidence retention, decision rules, and result interpretation. Neither inventory supplies or supersedes the other.

## 2. Decision

Create a `complete_publication` oracle for the exact pinned public v3.2 PDF, supported by a full section ledger and two independently produced atom lists. Completeness means complete for that public document under the stated atomization rule. It does not mean complete for the current operational Cyber Essentials Plus scheme.

Three approaches were considered:

1. **Complete public-document inventory with a section ledger — selected.** This accounts for all operative provisions and all excluded context while keeping the completeness claim bounded to one pinned public source.
2. **Declared subset containing only Test cases 1 through 5 — rejected.** It would omit scope verification, global result rules, sampling, evidence retention, conclusion duties, and operative appendices that materially define the public assurance procedure.
3. **Composite inventory of v3.2 plus current operational notices — rejected.** ESAF-1600 currently models one authoritative publication and one rights basis per mapping set. NCSC and IASME sources have different ownership, rights, dates, and operational roles. Combining them would misrepresent provenance and completeness.

## 3. Pinned public source

### 3.1 Source identity

- Authority: UK National Cyber Security Centre
- Publication: *Cyber Essentials Plus Test Specification*
- Publication identifier: `cyber-essentials-plus-test-specification`
- Source version: `3.2`
- Display date: April 2025
- NCSC resource-page date: 2025-04-28
- Resource page: `https://www.ncsc.gov.uk/cyberessentials/resources`
- Page count: 24 PDF pages
- Access date: 2026-07-14

The source version shall remain `3.2`. The design, oracle, later snapshot, and generated outputs shall not call it Cyber Essentials Plus v3.3.

### 3.2 Official byte variants

On the access date, the NCSC resource page linked to:

`https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf`

- Byte length: 424,226
- SHA-256: `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`

An older official URL remained live:

`https://www.ncsc.gov.uk/files/cyber-essentials-plus-test-specification-v3-2.pdf`

- Byte length: 419,191
- SHA-256: `d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694`

The two 24-page files have byte and metadata differences but yielded identical extracted publication text during acquisition review. The resource-page target is the canonical acquisition source for this milestone. The legacy official URL and digest remain recorded as a known byte variant. The oracle shall not identify the source by version alone.

Implementation shall re-fetch the resource page and canonical PDF. If the target URL, bytes, page count, displayed version, publication date, or substantive rendered content differs, implementation shall stop for source-drift review rather than silently updating the oracle.

## 4. Public-document and current-scheme boundary

NCSC currently publishes Cyber Essentials core requirements v3.3, effective 2026-04-27, while the public Plus test specification remains v3.2. IASME also published operational changes effective for assessment accounts created after 2026-04-26. Those changes include update-management retest sampling and verified self-assessment lifecycle rules not consolidated into the public v3.2 PDF.

The v3.2 PDF states that it helps the Delivery Partner develop its own test specifications. Public material does not fully define approved scanners, port sets, the sample-size method, report templates, test-file sets, or every exercise of Delivery Partner discretion. The oracle therefore shall state:

> This complete-publication oracle inventories the public NCSC Cyber Essentials Plus Test Specification v3.2. It is not a complete inventory of the current operational Cyber Essentials Plus scheme, Delivery Partner methodology, or certification process.

The IASME April 2026 notice is related operational context, not part of the v3.2 provision universe. Its URL, owner, publication date, access date, and high-level relevance may be recorded as factual context. IASME-authored text, structure, and derived inventory shall not enter the oracle without a separate rights decision and a separately designed source model.

NCSC's July 2026 Cyber Essentials Pathways work is outside the v3.2 publication and this milestone. It shall not be treated as general permission to assert alternative-control equivalence.

## 5. Publication rights

The NCSC PDF is Crown copyright. The NCSC terms apply the Open Government Licence v3.0 unless otherwise indicated. The implementation shall:

- attribute the NCSC and link the OGL v3.0;
- permit identifiers, structural inventory, official links, original paraphrases, and original derivative analysis;
- exclude NCSC and government logos, certification marks, photographs, infographics, and third-party material;
- prohibit copied requirement text and source passages, except for the sole minimal anomaly fragment `tests 2 to 7`; and
- prohibit any implication of NCSC, IASME, Certification Body, or government endorsement.

A named rights reviewer different from both inventory authors shall verify the exact pinned bytes, publication basis, attribution, permitted derivative elements, excluded elements, and restrictions **before either source-derived scratch inventory, ledger, paraphrase, or oracle enters Git**. The rights record itself may be committed first because it contains only source identity, bibliographic facts, the reviewer's decision, and the approved publication boundary. Inventory work shall stop if that decision is absent, conditional, or does not cover the intended committed fields.

IASME pages display separate IASME copyright, and no open reuse licence was identified. OGL permissions shall not be extended to IASME material. Until a distinct rights basis is approved, only bibliographic facts, official links, and independently written high-level context may be committed about IASME notices.

## 6. Assessment universe

The `complete_publication` universe contains every independently actionable or normative provision directed to an Assessor, Applicant, Certification Body, Certifying Body, or Delivery Partner in the public v3.2 PDF.

### 6.1 Included publication material

- the independently operative scope-boundary rule in Purpose;
- Before you begin, including permission, scope, segregation, sampling, reporting, remediation-before-testing, and evidence-retention duties;
- General prerequisites for testing;
- global test-result, pass, fail, completion, exception, and advisory rules;
- Test cases 1 through 5, including applicability, prerequisites, steps, sub-tests, conditions, decision criteria, result rules, and aggregate interpretation;
- every independent decision in Figure 1's remote-vulnerability flow;
- Sample testing, including population, representativeness, calculation, account coverage, and evidence-retention rules;
- Conclude the assessment, including deferral and discretionary exception rules; and
- independently operative or recommended content in Appendices A and B.

### 6.2 Context-only publication material

- cover, contents, What is new, and audience description;
- descriptive purpose, background, rationale, examples, and definitions that do not independently prescribe an action or outcome;
- navigation, branding, headers, footers, page numbers, and rights-only material; and
- references to the separately published Cyber Essentials requirements, which are dependencies rather than incorporated provisions.

Every substantive section occurrence shall appear exactly once in a section ledger as `included` or `context_only`, with a unique hierarchical `section_id`, `parent_section_id`, heading text, group, printed-page coordinates, PDF-page coordinates, rationale, and atom count. Occurrence identity, rather than heading text, controls uniqueness so repeated headings remain separate and auditable. Every provision shall reference exactly one included occurrence through `section_id`. Context material remains accounted for without becoming artificial `out_of_scope` provision records.

## 7. Atomization rule

One atom represents one independently assessable action, applicability constraint, prerequisite, evidence-retention duty, decision criterion, result rule, or recommendation whose fulfillment or future ESAF relationship could differ from adjacent text.

Apply these rules consistently:

- split numbered steps and independently testable bullets;
- split compound clauses when actors, evidence, conditions, outcomes, or potential relationships differ;
- keep a condition and its required result together as one decision-rule atom;
- attach examples and explanatory notes to the atom they clarify rather than creating separate atoms;
- preserve applicability statements separately when they define device, service, account, or sampling populations;
- preserve recommendations as provisions even when a later mapping may use `no_direct_mapping`;
- treat aggregate pass or fail interpretation separately from the underlying procedures;
- do not assign mapping dispositions or ESAF relationships during atomization; and
- do not duplicate core v3.3 implementation requirements as Plus provisions.

### 7.1 Visual provisions

Text extraction is not authoritative for completeness. PDF page 9, printed page 8, contains Figure 1 decision logic that ordinary linear extraction does not preserve. Each of its seven independent decisions shall be one decision-rule atom with `source_assigned_label` values forming the exact set `Figure 1 decision 1` through `Figure 1 decision 7`; Yes and No arrows shall remain branches of that atom rather than separate atoms.

Locators for visual provisions shall use both coordinate systems, for example `PDF page 9 / printed page 8, Figure 1, decision 4`. Every PDF page shall be rendered and visually inspected before the oracle count is frozen.

### 7.2 Source anomaly

The public text says that general prerequisites apply to `tests 2 to 7`, while the publication presents Test cases 1 through 5. The source dossier shall record and test this anomaly without silently correcting, interpreting, or expanding it.

## 8. Independent reconciliation and count

No expected provision count is approved by this design. After the independent rights gate passes, two inventory authors shall independently inspect the exact canonical bytes, including every rendered page, and produce complete atom lists and complete section-occurrence ledgers without sharing a provisional count or occurrence set. They shall then reconcile inclusion decisions, atom boundaries, identifiers, summaries, kinds, actors, locators, and occurrence links.

The reconciled list becomes the locked oracle only after:

1. all differences are dispositioned with rationale;
2. an independent reconciler locks the exact expected set of hierarchical section occurrences from the source before deriving any atom count, and tests assert exact set equality rather than heading-count equality;
3. every provision links to one included ledger occurrence, and section-ledger counts derived from those links, group counts, and total agree;
4. the prior rights decision is re-attested against every class of committed source-derived element without changing its publication basis;
5. an independent specification/inventory reviewer finds no unresolved Critical or Important issue; and
6. an independent security/overclaiming reviewer finds no unresolved Critical or Important issue on the same exact candidate SHA.

Any subsequent count, summary, identifier, locator, source, or rights change invalidates both reviews and requires redispatch on the new candidate.

## 9. Identifier and oracle contract

### 9.1 Identifiers

- Record prefix: `cepts32`
- External provision prefix: `CEPTS3.2`
- Groups: `M`, `T1`, `S`, `T2`, `T3`, `T4`, `T5`, `C`, `A`, and `B`

Examples are `cepts32-m-001` / `CEPTS3.2-M-001` and `cepts32-t3-001` / `CEPTS3.2-T3-001`. Source-assigned labels such as `Sub-test 3.1.2` remain only in the provision-level `source_assigned_label`; they are not treated as globally unique provision identifiers.

Identifiers shall be unique, stable, lowercase for record filenames, uppercase in the external locator form, and ordered by publication flow. They are ESAF-assigned citation locators, not NCSC-issued identifiers.

### 9.2 Machine-readable oracle

The locked oracle will be stored at:

`docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`

Tests shall enforce the following closed contract as an exact JSON Schema equivalent: every object has `additionalProperties: false`; every listed property is required unless explicitly described as nullable; arrays retain publication order and contain no duplicate values where a set is intended. Strings are nonempty after trimming. Date fields use `YYYY-MM-DD` except the exact human-readable `source.display_date`, SHA-256 values use 64 lowercase hexadecimal characters, byte/page/count fields are nonnegative integers, and no numeric count is fixed until reconciliation.

The top-level object has exactly these required properties:

- `schema_version`: string, initially `1.0.0`;
- `atomization_rule_version`: string, initially `1.0.0`;
- `scope`: object with exactly `type` (`complete_publication`) and `statement` (string bounded to the pinned public PDF);
- `source`: source object defined below;
- `rights`: rights object defined below;
- `inventory_provenance`: inventory-provenance object defined below;
- `direction_boundary`: direction-boundary object defined below;
- `operational_context`: array of context objects defined below;
- `known_anomalies`: array of anomaly objects defined below;
- `groups`: array equal in order to `M`, `T1`, `S`, `T2`, `T3`, `T4`, `T5`, `C`, `A`, `B`;
- `section_ledger`: ordered array of section-occurrence objects defined below;
- `counts`: counts object defined below;
- `assurance_limits`: assurance-limits object defined below; and
- `provisions`: ordered array of provision objects defined below.

The `source` object has exactly these required properties and values: `title` (`Cyber Essentials Plus Test Specification`), `authority` (`UK National Cyber Security Centre`), `publication_identifier` (`cyber-essentials-plus-test-specification`), `version` (`3.2`), `display_date` (`April 2025`), `resource_page_url` (the pinned URI in section 3), `resource_page_date` (`2025-04-28`), `access_date` (`2026-07-14`), `media_type` (`application/pdf`), `pdf_page_count` (`24`), and `variants` (array). `variants` contains exactly two objects, ordered canonical then legacy, each with exactly `role` (`canonical` or `legacy`), `url` (the corresponding pinned URI), `byte_length` (the corresponding pinned positive integer), and `sha256` (the corresponding pinned digest).

The `rights` object has exactly these required properties: `copyright` (string), `licence_name` (string), `licence_url` (URI string), `attribution` (string), `publication_basis` (string), `permitted_elements` (array), `prohibited_elements` (array), `copied_requirement_or_passage_text_prohibited` (boolean required true), `allowed_verbatim_fragments` (array exactly equal to `["tests 2 to 7"]`), `restrictions` (nonempty array of unique strings), `iasme_partition` (object), and `review` (object). ESAF-1600 defines the exact six-element rights universe `identifiers`, `titles`, `structural_inventory`, `paraphrases`, `derivative_mapping_analysis`, and `official_links`. `permitted_elements` and `prohibited_elements` shall be disjoint and exhaustive over that universe. Because all six rights elements are committed in the oracle's rights declaration, `permitted_elements` shall equal all six in that order and `prohibited_elements` shall be empty. Copied requirement text and source passages remain prohibited everywhere except the one minimal allowed anomaly fragment; `restrictions` also covers excluded marks, imagery, third-party material, and endorsement implications. `iasme_partition` has exactly `owner` (string), `licence` (nullable string; null until a separate licence is approved), `permitted_facts` (nonempty unique string array), and `prohibited_source_derived_elements` (nonempty unique string array). `review` has exactly `reviewer` (string), `review_date` (date), `independent_of_inventory_authors` (boolean required true), `canonical_sha256` (digest), `legacy_sha256` (digest), `publication_basis_verified` (boolean required true), and `disposition` (string equal to `approved`).

The `inventory_provenance` object has exactly `authors` (array of exactly two unique nonempty strings), `reconciler` (nonempty string), `rights_record_commit` (40-character lowercase Git SHA string), and `inventories_started_after_rights_commit` (boolean required true). Tests shall require `rights.review.reviewer` to differ from both authors and shall use Git history during repository validation to prove `rights_record_commit` is an ancestor of the first commit containing any source-derived inventory artifact.

The `direction_boundary` object has exactly `oracle_establishes_mapping_direction` (boolean required false), `future_directions` (array exactly equal in order to `esaf_to_external`, `external_to_esaf`), and `assessed_independently` (boolean required true). The source oracle establishes no mapping direction; any future mapping assesses those two directions independently.

Each `operational_context` item has exactly `owner` (string), `title` (string), `url` (URI string), `publication_date` (date), `access_date` (date), `relevance` (original high-level string), and `rights_partition` (string equal to `bibliographic_facts_and_original_context_only`). `known_anomalies` contains exactly one item with exactly `anomaly_id` (unique string), `source_literal` (string exactly equal to the sole allowed verbatim fragment `tests 2 to 7`), `locator` (locator object), and `treatment` (string that records without correction or expansion). The fragment shall occur verbatim nowhere else in the oracle.

Each `section_ledger` occurrence has exactly `section_id` (unique hierarchical identifier such as `sec-t3-figure-1`), `parent_section_id` (nullable string referencing another ledger occurrence), `heading` (string; repeated values permitted), `group` (one controlled group), `pdf_pages` (page-range object), `printed_pages` (nullable page-range object), `decision` (`included` or `context_only`), `rationale` (string), and `atom_count` (nonnegative integer). A page-range object has exactly `start` and `end` positive integers with `start <= end`. The reconciler shall independently specify and freeze the exact ordered `section_id` set; tests shall assert exact equality, valid parent references, coordinates, and group values. Ledger atom counts shall be computed from provision `section_id` links, including zero for context-only occurrences, rather than trusted as free-standing declarations.

The `counts` object has exactly `total` (nonnegative integer) and `by_group` (object with exactly the ten group names as nonnegative integer properties). Tests shall derive both from `provisions`, require their sums to agree, and compare them with the link-derived ledger counts. Count literals enter tests only after both independent inventories and the independently specified occurrence set are reconciled.

Each provision has exactly these required properties: `record_id` (string), `external_provision_id` (string), `section_id` (string referencing one `included` ledger occurrence), `group` (controlled group matching that occurrence), `kind` (controlled kind), `actors` (nonempty array of unique controlled actor strings), `actor_basis` (original concise string identifying the source grammar that assigns the actor or actors), `source_assigned_label` (nullable string), `summary` (original concise string), and `locator` (locator object). `actors` values are limited to `Assessor`, `Applicant`, `Certification Body`, `Certifying Body`, and `Delivery Partner`; multiple actors are allowed only when `actor_basis` and the locator demonstrate that the source expressly assigns the same atom to each. A locator has exactly `pdf_page` (positive integer), `printed_page` (nullable positive integer), `section` (string), and `detail` (string); it does not duplicate `source_assigned_label`. `kind` is one of `applicability`, `prerequisite`, `procedure_step`, `decision_rule`, `result_rule`, `evidence_retention`, or `recommendation`.

The `assurance_limits` object has exactly these required properties, all expressed as original bounded statements rather than source quotation: `scope_boundary`, `population_and_sample_boundary`, `assessment_date_boundary`, `evidence_date_boundary`, `tool_and_provenance_boundary`, and `point_in_time_boundary` (strings); `discretion_owner` (string equal to `Delivery Partner`); `discretionary_exception` (object); and `prohibited_inferences` (array). `discretionary_exception` models one exception and has exactly `owner` (`Delivery Partner`), `predicates` (array), `all_predicates_required` (boolean required true), `locator` (locator object), `automatic_pass` (boolean required false), and `is_95_percent_score` (boolean required false). `predicates` contains exactly two objects in order: `marginal-deviation-under-five-percent`, meaning a marginal deviation in less than 5% of performed tests; and `no-wider-process-failure-evidence`, meaning no evidence of wider failure of Applicant cybersecurity processes. Each predicate object has exactly `predicate_id` (the stated identifier) and `meaning` (the stated meaning). `prohibited_inferences` shall equal the exact controlled set `certification`, `compliance`, `equivalence`, `endorsement`, `predictive_sufficiency`, `full_population_assurance`, `continuous_assurance`, and `current_scheme_completeness`.

## 10. Future mapping boundary

The future snapshot path will use:

`crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/<esaf-release>/<mapping-set-version>/`

The exact ESAF release, source commit, and mapping-set version shall be chosen and pinned when mapping implementation begins. They are not fixed by this source-inventory milestone.

Most Plus provisions prescribe assessment actors or assurance procedures rather than applicant implementation outcomes. A future mapping shall therefore:

- assess `esaf_to_external` and `external_to_esaf` independently;
- use `prerequisite` only where exact ESAF normative text establishes a condition required by the test procedure;
- avoid `supports` merely because a procedure tests a similar topic;
- condition any reverse assurance leg on actor, scope, population, sample, date, tool, exceptions, and evidence provenance;
- default to `no_direct_mapping` where ESAF does not expressly supply the external outcome; and
- never infer certification, compliance, equivalence, endorsement, predictive sufficiency, full-population assurance, continuous assurance, or current-scheme completeness.

The discretionary less-than-five-percent exception is not a 95-percent compliance score or automatic pass threshold. A certificate or test result is point-in-time, sampled assurance and does not by itself prove current ESAF control implementation.

## 11. Implementation deliverables

The source-inventory implementation milestone shall create:

- an independently approved rights record committed before any source-derived inventory content;
- the locked JSON oracle at the path in section 9.2;
- focused tests for source identity, rights, section coverage, visual decisions, identifiers, counts, kinds, summaries, locators, anomalies, and prohibited claims;
- a concise Cyber Essentials Plus roadmap section in `crosswalks/uk-cyber-essentials.md` linking the oracle and preserving the core/Plus boundary;
- traceability evidence recording the two independent inventories, independently specified occurrence set, derived counts, and gate results, while exact reviewed PR-head SHA evidence remains external to the reviewed commit; and
- project backlog wording that moves the next activity from design to independently reconciled inventory implementation.

The milestone shall not create a mapping snapshot directory, lifecycle record, control manifest, provision mapping record, relationship leg, generated crosswalk statistic, or claim of scheme completeness.

## 12. Validation and acceptance

Implementation shall fail closed on source drift; source-identity mismatch; missing section-ledger entries; count disagreement; duplicate or unordered IDs; invalid kinds; empty summaries or locators; duplicate source labels in locators; omitted visual decisions; missing or late rights approval; invalid rights partition; invalid direction boundary; malformed discretionary exception; incomplete prohibited-inference set; or prohibited claims.

Final acceptance requires:

1. canonical and legacy official source identities are byte-pinned;
2. all 24 pages are rendered and visually inspected;
3. rights approval precedes any source-derived inventory content entering Git, and the reviewer is independent of both inventory authors;
4. two independent atom lists and ledgers are reconciled and the count is frozen only afterward;
5. the independently specified exact section-occurrence set is locked, including repeated headings, and every provision links to one included occurrence;
6. section counts derived from provision links, group counts, and total counts agree exactly;
7. the closed JSON contract rejects missing, mistyped, nullable-when-nonnullable, and unknown fields; all exact source constants, identifiers, actors, summaries, kinds, and nonduplicative locators satisfy it;
8. Figure 1's decision-label set is exactly decisions 1 through 7, and the `tests 2 to 7` anomaly is locked;
9. NCSC and IASME provenance and rights remain separate; the ESAF-1600 six-element rights universe is disjointly and exhaustively partitioned with all six permitted and none prohibited; copied requirement text and source passages are prohibited except for the exact singleton anomaly fragment `tests 2 to 7`, which appears only as `known_anomalies[0].source_literal`;
10. assurance limits encode actor, scope, population/sample, dates, tool/provenance, point-in-time, one Delivery Partner discretionary exception with both exact conjunctive predicates, no automatic pass or 95-percent score, and the exact eight prohibited inferences;
11. the direction boundary states that the oracle establishes no mapping direction and any future `esaf_to_external` and `external_to_esaf` directions are assessed independently;
12. focused and full repository tests, all validators, an explicit general link validator, cache checks, and whole-branch diff checks pass;
13. exact-SHA inventory/specification and security/overclaiming reviews have no unresolved Critical or Important findings;
14. the rights-review commit is an ancestor of both the reviewed PR head and resulting merged-main SHA, integration uses a merge commit rather than squash or rebase, required GitHub checks pass on the externally recorded reviewed PR-head SHA, and post-merge validation passes on the resulting merged-main SHA; and
15. no mapping, certification, equivalence, endorsement, full-population, continuous-assurance, or current-scheme-completeness claim is introduced.
