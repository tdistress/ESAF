# UK Cyber Essentials Plus v3.2 source-inventory rights review

**Reviewer:** Codex Rights Reviewer R1

**Review date:** 2026-07-14

**Reviewed design:** `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-source-inventory-design.md`

**Independence:** The reviewer is not inventory author A or inventory author B and shall not serve in either role.

**Disposition:** **Approved unconditionally for every planned oracle field class listed in this record.**

The approval is bounded to the exact NCSC byte variants, source contract, rights universe, field classes, and restrictions below. The stated restrictions are the approved publication boundary, not unresolved conditions. No source-derived inventory, ledger, paraphrase, oracle, rendering, or provision count was created during this review.

## Exact source verification

| Role | Official URL | Bytes | SHA-256 | Media type | PDF pages |
|---|---|---:|---|---|---:|
| Canonical | `https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf` | 424,226 | `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8` | `application/pdf` | 24 |
| Legacy | `https://www.ncsc.gov.uk/files/cyber-essentials-plus-test-specification-v3-2.pdf` | 419,191 | `d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694` | `application/pdf` | 24 |

Independent byte hashing and length checks matched every pinned value. Both files are unencrypted A4 PDFs with the following common embedded metadata: title `Cyber Essentials Plus Test Specification v3.2`, author `National Cyber Security Centre`, and subject `Cyber Essentials Plus`. Their creation metadata is the same; their modification metadata differs, consistent with distinct official byte variants. Both display version 3.2 and April 2025, and their independently supplied text extractions are byte-identical.

The acquired NCSC resource page contains the exact relative target:

`/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf`

Resolving that target against `https://www.ncsc.gov.uk` yields the canonical URL and bytes above.

## Copyright, licence, and attribution basis

The exact PDFs identify their material as UK Crown copyright. Their publication notice identifies Crown copyright 2024, makes text content available for reuse under the Open Government Licence v3.0, and excludes photographs and infographics that may contain third-party material.

The [NCSC terms and conditions](https://www.ncsc.gov.uk/section/about-this-website/terms-and-conditions) state that website content is Crown copyright unless otherwise indicated and may be reused under OGL v3.0 with source acknowledgement and, where possible, an OGL link. They separately exclude third-party copyright material, third-party images, and logos from that permission. The [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) permits copying, publication, distribution, adaptation, and commercial or non-commercial exploitation of covered information, subject to attribution. It excludes third-party rights, logos, crests, trade marks, design rights, and other listed rights, and forbids uses that imply official status or endorsement.

The approved oracle attribution is:

> Contains public sector information from the UK National Cyber Security Centre, licensed under the Open Government Licence v3.0.

The oracle shall identify the NCSC as the source and link to the OGL v3.0 URL above.

## ESAF-1600 rights universe

The exact six-element universe is exhaustively and disjointly partitioned as follows. All six elements are permitted in the planned oracle, in this exact order; none is prohibited.

| Rights element | Disposition | Approved use |
|---|---|---|
| `identifiers` | Approved unconditionally | ESAF-assigned record, provision, group, section, anomaly, and predicate identifiers, plus source-assigned labels used for source identification. |
| `titles` | Approved unconditionally | The publication title and source headings needed for identification and navigation. |
| `structural_inventory` | Approved unconditionally | Original section-occurrence accounting, hierarchy, coordinates, actors, provision kinds, decision labels, and derived counts. |
| `paraphrases` | Approved unconditionally | Concise, independently written summaries, rationales, actor bases, anomaly treatment, scope statements, and assurance limits. |
| `derivative_mapping_analysis` | Approved unconditionally | Original ESAF analysis, including direction boundaries, future mapping analysis, restrictions, and prohibited inferences. |
| `official_links` | Approved unconditionally | Official NCSC, OGL, and separately partitioned IASME links. |

Accordingly:

- `permitted_elements` shall equal `identifiers`, `titles`, `structural_inventory`, `paraphrases`, `derivative_mapping_analysis`, and `official_links`, in that order.
- `prohibited_elements` shall be empty.
- The two arrays are disjoint and exhaustive over the six-element universe.

## Verbatim-text boundary

`copied_requirement_or_passage_text_prohibited` is approved with the required value `true`.

`allowed_verbatim_locations` is approved only as the exact singleton array:

`["known_anomalies[0].source_literal"]`

The required value at that sole location is `tests 2 to 7`. The oracle shall contain that source literal exactly once at that path and nowhere else. No other copied requirement text or source passage is approved. Titles, identifiers, and minimal source-assigned labels used within their approved field classes are not a licence to reproduce passages.

## Exclusions and restrictions

The approved `restrictions` field shall state all of the following boundaries:

- exclude photographs, infographics, and all other third-party material unless separately licensed;
- exclude NCSC, UK government, IASME, Certification Body, and Certifying Body logos, certification marks, trade marks, crests, and other protected branding;
- do not imply official status, affiliation, approval, certification, or endorsement by the NCSC, IASME, a Certification Body, a Certifying Body, the UK government, or any other source party;
- do not extend OGL permission to content identified as third-party or subject to another arrangement; and
- preserve the attribution and OGL link stated above wherever covered information is reused.

## Separate IASME partition

IASME material is not part of the NCSC OGL permission. The reviewed IASME operational-update page identifies IASME Consortium Limited copyright, and no open reuse licence was identified for its authored content. The planned `iasme_partition` is approved only with this boundary:

- `owner`: `IASME Consortium Limited`;
- `licence`: `null` until a separate licence is approved;
- `permitted_facts`: bibliographic facts, official links, and independently written high-level context; and
- `prohibited_source_derived_elements`: copied IASME text or passages, IASME-authored structure, derived IASME inventory or atomization, IASME imagery, logos, marks, and any implication of IASME endorsement.

The IASME notice may appear only in `operational_context` under `rights_partition: bibliographic_facts_and_original_context_only`. It shall not contribute provisions, section-ledger occurrences, counts, assurance rules, or other source-derived inventory to this NCSC oracle.

## Planned oracle field-class dispositions

Every planned top-level field class and its nested fields have the following unconditional disposition under the boundaries already fixed in this record.

| Planned field class | Rights classification | Disposition |
|---|---|---|
| `schema_version`, `atomization_rule_version` | Original ESAF identifiers and metadata | Approved unconditionally |
| `scope` | Original bounded statement and identifier | Approved unconditionally |
| `source` | Bibliographic facts, title, identifiers, metadata, digests, and official links | Approved unconditionally |
| `rights` | Original rights declaration, attribution, restrictions, IASME partition, and this review decision | Approved unconditionally |
| `inventory_provenance` | Original authorship, reconciliation, commit, and sequencing facts | Approved unconditionally |
| `direction_boundary` | Original ESAF derivative analysis and controlled identifiers | Approved unconditionally |
| `operational_context` | IASME bibliographic facts, official links, and independently written high-level context only | Approved unconditionally |
| `known_anomalies` | Original identifier, locator, and treatment plus the sole permitted literal at the exact singleton path | Approved unconditionally |
| `groups` | ESAF-assigned structural identifiers | Approved unconditionally |
| `section_ledger` | Titles, structural inventory, coordinates, original rationales, and derived atom counts | Approved unconditionally |
| `counts` | Facts derived from the permitted structural inventory | Approved unconditionally |
| `assurance_limits` | Original paraphrases, locators, predicates, and derivative analysis | Approved unconditionally |
| `provisions` | ESAF identifiers, source-assigned labels, structural inventory, actors, original summaries and actor bases, kinds, and locators | Approved unconditionally |

This approval covers the complete closed oracle contract planned by the reviewed design. Any added field class, additional verbatim location, different source bytes, different rights owner or licence, expansion of the IASME partition, or use of excluded material requires a new rights decision before that change enters Git.

## Final decision

**APPROVED.** Codex Rights Reviewer R1 unconditionally approves all planned oracle field classes for the exact canonical and legacy NCSC byte variants recorded above. The publication basis, attribution, exhaustive six-element permitted set, empty prohibited set, copied-text prohibition, exact singleton anomaly exception, excluded material and marks, non-endorsement rule, and separate IASME partition are all verified and approved. Inventory authors A and B may begin only after this rights record is committed, and neither author may be Codex Rights Reviewer R1.

## Post-reconciliation rights re-attestation

**Re-attesting reviewer:** Codex Rights Reviewer R1

**Re-attestation date:** 2026-07-14

**Reviewed candidate:** `c723d3eba723ac3107dba2e0eccbf6de4f42f70a`

**Reviewed oracle SHA-256:** `6c152f07be832a749f5b6ffe41f3a7d0002b21c650ed6564ed3d9da6399d73be`

**Reviewed reconciliation SHA-256:** `229d45fa682edb2b019c71112fe05a6124537ed9dc392637997323692980b791`

**Nature of decision:** This re-attestation confirms that the reconciled oracle remains within the publication basis approved before inventory work in commit `6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6`. It does not grant retroactive permission and does not expand that basis.

The same independent reviewer compared every committed source-derived and narrative field class with the prior approval:

| Reconciled field class | Observed content and prior basis | Re-attestation |
|---|---|---|
| `schema_version`, `atomization_rule_version` | Original ESAF identifiers and metadata only | Confirmed within prior approval |
| `scope` | One original bounded complete-publication statement | Confirmed within prior approval |
| `source` | Approved title, bibliographic facts, exact byte identities, metadata, and official NCSC links | Confirmed within prior approval |
| `rights` | Exact six-element permitted set, empty prohibited set, attribution, OGL link, restrictions, review, and closed IASME partition | Confirmed within prior approval |
| `inventory_provenance` | Original authorship, reconciliation, commit, and sequencing facts | Confirmed within prior approval |
| `direction_boundary` | Original ESAF governance analysis and controlled identifiers | Confirmed within prior approval |
| `operational_context` | Empty; no IASME notice content was committed | Confirmed within prior approval |
| `known_anomalies` | Original identifier, locator, and treatment with the sole approved literal exception | Confirmed within prior approval |
| `groups` | ESAF-assigned structural identifiers | Confirmed within prior approval |
| `section_ledger` | 55 NCSC-PDF occurrences containing approved titles, structural inventory, coordinates, original rationales, and derived counts | Confirmed within prior approval |
| `counts` | Facts derived from the approved structural inventory | Confirmed within prior approval |
| `assurance_limits` | Original paraphrases, locators, controlled predicates, and derivative analysis | Confirmed within prior approval |
| `provisions` | 144 records containing approved ESAF identifiers, source-assigned labels, structure, actors, original actor bases and summaries, kinds, and locators | Confirmed within prior approval |

The narrative review covered all 509 instances in the planned original-free-text classes: the scope statement; rights publication basis, restrictions, and IASME partition terms; anomaly treatment; all 55 ledger rationales; all 144 actor bases, summaries, and locator details; and all six assurance-boundary statements. The focused source-copy controls passed, and an additional normalized comparison found no narrative value of five or more words reproduced contiguously from the canonical source.

The IASME partition remains closed. The only IASME-named oracle value is `rights.iasme_partition.owner`; `operational_context` is empty; and no IASME-derived text, heading hierarchy, occurrence, provision, count, assurance rule, imagery, logo, mark, or endorsement implication appears in the ledger, provisions, or assurance limits. The NCSC OGL basis has not been extended to IASME material.

The copied-text boundary also remains exact. `copied_requirement_or_passage_text_prohibited` is `true`; `allowed_verbatim_locations` remains the singleton `["known_anomalies[0].source_literal"]`; and a recursive value walk finds `tests 2 to 7` exactly once, at that approved path and nowhere else.

**RE-ATTESTED WITHOUT RESERVATION.** Codex Rights Reviewer R1 confirms that every reconciled source-derived and narrative field class is covered by the prior pre-inventory approval. No expanded publication basis or new permission is required for the reviewed oracle and reconciliation candidate.
