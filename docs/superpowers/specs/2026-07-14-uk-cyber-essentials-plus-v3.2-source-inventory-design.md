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
- avoid copied source passages when original concise paraphrases suffice; and
- prohibit any implication of NCSC, IASME, Certification Body, or government endorsement.

A named rights reviewer different from the inventory authors shall verify the exact pinned bytes and recorded permission boundary before the oracle is accepted.

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

Every substantive heading shall appear exactly once in a section ledger as `included` or `context_only`, with printed pages, PDF pages, rationale, and atom count. Context material remains accounted for without becoming artificial `out_of_scope` provision records.

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

Text extraction is not authoritative for completeness. PDF page 9, printed page 8, contains Figure 1 decision logic that ordinary linear extraction does not preserve. Each of its seven independent decisions shall be one decision-rule atom; Yes and No arrows shall remain branches of that atom rather than separate atoms.

Locators for visual provisions shall use both coordinate systems, for example `PDF page 9 / printed page 8, Figure 1, decision 4`. Every PDF page shall be rendered and visually inspected before the oracle count is frozen.

### 7.2 Source anomaly

The public text says that general prerequisites apply to `tests 2 to 7`, while the publication presents Test cases 1 through 5. The source dossier shall record and test this anomaly without silently correcting, interpreting, or expanding it.

## 8. Independent reconciliation and count

No expected provision count is approved by this design. Two inventory authors shall independently inspect the exact canonical bytes, including every rendered page, and produce complete atom lists without sharing a provisional count. They shall then reconcile inclusion decisions, atom boundaries, identifiers, summaries, kinds, and locators.

The reconciled list becomes the locked oracle only after:

1. all differences are dispositioned with rationale;
2. the section-ledger counts, group counts, and total agree;
3. a separate rights reviewer approves publication of every committed element;
4. an independent specification/inventory reviewer finds no unresolved Critical or Important issue; and
5. an independent security/overclaiming reviewer finds no unresolved Critical or Important issue on the same exact candidate SHA.

Any subsequent count, summary, identifier, locator, source, or rights change invalidates both reviews and requires redispatch on the new candidate.

## 9. Identifier and oracle contract

### 9.1 Identifiers

- Record prefix: `cepts32`
- External provision prefix: `CEPTS3.2`
- Groups: `M`, `T1`, `S`, `T2`, `T3`, `T4`, `T5`, `C`, `A`, and `B`

Examples are `cepts32-m-001` / `CEPTS3.2-M-001` and `cepts32-t3-001` / `CEPTS3.2-T3-001`. Source-assigned labels such as `Sub-test 3.1.2` remain in the locator and `source_assigned_label`; they are not treated as globally unique provision identifiers.

Identifiers shall be unique, stable, lowercase for record filenames, uppercase in the external locator form, and ordered by publication flow. They are ESAF-assigned citation locators, not NCSC-issued identifiers.

### 9.2 Machine-readable oracle

The locked oracle will be stored at:

`docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`

Its top-level contract shall include:

- schema version and atomization-rule version;
- source title, authority, version, resource page, canonical URL, legacy URL, dates, media type, byte lengths, page count, and both SHA-256 digests;
- copyright, licence, attribution, permitted and prohibited elements, and rights restrictions;
- known source anomalies and separately sourced operational context;
- included and context-only sections;
- the complete section ledger;
- total and group counts; and
- the ordered provision array.

Each provision shall contain `record_id`, `external_provision_id`, `group`, `kind`, `source_assigned_label`, original `summary`, and precise `locator`.

`kind` shall be one of `applicability`, `prerequisite`, `procedure_step`, `decision_rule`, `result_rule`, `evidence_retention`, or `recommendation`.

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
- never infer certification, equivalence, predictive sufficiency, full-population coverage, or continuous assurance.

The discretionary less-than-five-percent exception is not a 95-percent compliance score or automatic pass threshold. A certificate or test result is point-in-time, sampled assurance and does not by itself prove current ESAF control implementation.

## 11. Implementation deliverables

The source-inventory implementation milestone shall create:

- the locked JSON oracle at the path in section 9.2;
- focused tests for source identity, rights, section coverage, visual decisions, identifiers, counts, kinds, summaries, locators, anomalies, and prohibited claims;
- a concise Cyber Essentials Plus roadmap section in `crosswalks/uk-cyber-essentials.md` linking the oracle and preserving the core/Plus boundary;
- traceability evidence recording the two independent inventories and both exact-SHA final reviews; and
- project backlog wording that moves the next activity from design to independently reconciled inventory implementation.

The milestone shall not create a mapping snapshot directory, lifecycle record, control manifest, provision mapping record, relationship leg, generated crosswalk statistic, or claim of scheme completeness.

## 12. Validation and acceptance

Implementation shall fail closed on source drift, missing section-ledger entries, count disagreement, duplicate or unordered IDs, invalid kinds, empty summaries or locators, omitted visual decisions, missing rights approval, or prohibited claims.

Final acceptance requires:

1. canonical and legacy official source identities are byte-pinned;
2. all 24 pages are rendered and visually inspected;
3. two independent atom lists are reconciled and the count is frozen only afterward;
4. every substantive heading is accounted for exactly once;
5. section, group, and total counts agree exactly;
6. all identifiers, summaries, kinds, and locators satisfy the oracle contract;
7. Figure 1's seven decisions and the `tests 2 to 7` anomaly are locked;
8. NCSC and IASME provenance and rights remain separate;
9. focused and full repository tests, all validators, link checks, cache checks, and whole-branch diff checks pass;
10. exact-SHA inventory/specification and security/overclaiming reviews have no unresolved Critical or Important findings;
11. required GitHub checks pass on the reviewed PR-head SHA and post-merge validation passes on the resulting merged-main SHA; and
12. no mapping, certification, equivalence, endorsement, full-population, continuous-assurance, or current-scheme-completeness claim is introduced.
