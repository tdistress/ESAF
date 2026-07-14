# UK Cyber Essentials Plus v3.2 inventory reconciliation

**Reconciler:** Codex Inventory Reconciler R1

**Inventory authors:** Codex Inventory Author A and Codex Inventory Author B

**Source:** Canonical 24-page PDF, SHA-256 `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`

**Rights record:** `6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6`
**Disposition:** Reconciled with no unresolved difference

## Independence, source, and rights sequence

The two author artifacts were opened only after both independent inventories and their Task 2 review were complete. The reconciler inspected rendered pages 1 through 24 at original detail, traced all seven Figure 1 decisions and branches, and used the text extraction only to locate and compare passages. Neither author's provision count controlled the independently locked occurrence hierarchy.

`git merge-base --is-ancestor 6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6 HEAD` returned success before reconciliation. `git diff-tree --root --no-commit-id --name-status -r 6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6` showed that commit introduced only the approved rights record. Both author reports state that inventory work began after that commit.

The external `task-3-machine-comparison.json` in the verified temporary task root is a semantic comparison, version `2.0.0`. It aligns occurrences by rendered identity and coordinates and aligns provisions by occurrence, dual locator, publication order, and action or criterion meaning. Its 207 stable `DIFF-*` records comprise 62 section rows covering 55 selected occurrences plus seven excluded synthetic Author A occurrences, and 145 provision rows covering 144 selected provisions plus one excluded Author B cross-reference. Every row contains both proposals, the selected result, exact rendered-page and dual-coordinate evidence, atomization rationale, reconciler, resolution, and one or more `TD-*` reverse links into this record.

## Independently locked section-occurrence hierarchy

The rendered publication establishes 55 ordered occurrences. The hierarchy follows visible headings plus Figure 1. An unheaded provision remains in its visible parent occurrence rather than creating a synthetic section. A structural parent is `context_only` when all operative content is in child occurrences; it is `included` when it also carries an unheaded applicability or other provision. The final rights page is a root `M` occurrence, not an Appendix B child.

The exact ordered IDs are frozen in the focused test:

`sec-m-cover`, `sec-m-contents`, `sec-m-whats-new`, `sec-m-audience`, `sec-m-purpose`, `sec-m-before-you-begin`, `sec-m-general-prerequisites`, `sec-m-success-criteria`, `sec-m-test-results`, `sec-m-pass`, `sec-m-fail`, `sec-m-advisory-notes`, `sec-t1-test-case`, `sec-t1-purpose`, `sec-t1-description`, `sec-t1-prerequisites`, `sec-t1-subtest-1-1`, `sec-t1-figure-1`, `sec-t1-interpretation`, `sec-s-sample-testing`, `sec-t2-test-case`, `sec-t2-purpose`, `sec-t2-description`, `sec-t2-prerequisites`, `sec-t2-subtest-2-1`, `sec-t2-interpretation`, `sec-t3-test-case`, `sec-t3-purpose`, `sec-t3-description`, `sec-t3-prerequisites`, `sec-t3-select-subtests`, `sec-t3-subtest-3-1`, `sec-t3-subtest-3-1-1`, `sec-t3-subtest-3-1-2`, `sec-t3-subtest-3-1-3`, `sec-t3-subtest-3-2`, `sec-t3-interpretation`, `sec-t4-test-case`, `sec-t4-purpose`, `sec-t4-description`, `sec-t4-case-4-1`, `sec-t4-interpretation`, `sec-t5-test-case`, `sec-t5-purpose`, `sec-t5-description`, `sec-t5-case-5-1`, `sec-t5-interpretation`, `sec-c-conclude`, `sec-c-note-deferral`, `sec-c-note-exception`, `sec-a-appendix`, `sec-a-note-delivery-partner`, `sec-b-appendix`, `sec-b-note-delivery-partner`, `sec-m-rights-notice`.

The frozen tuple for every occurrence includes its parent, exact heading, group, PDF range, nullable printed range, and decision. Repeated headings remain distinct occurrences: the two conclusion notes have separate IDs, as do the Appendix A and Appendix B notes. Coordinates and parents are asserted as exact ordered equality, not inferred from atom totals.

## Semantic difference contract and linkage

Each machine row is the authoritative per-difference record. A `DIFF-SEC-*` or `DIFF-PROV-*` ID is stable because it is anchored to the selected occurrence or provision, not an array position. Proposal arrays explicitly support one-to-many and many-to-one boundaries. Each row has these exact fields: `difference_id`, `subject_type`, `semantic_anchor`, `difference_classes`, `author_a_proposals`, `author_b_proposals`, `selected_result`, `source_evidence`, `atomization_rationale`, `reconciler`, `resolution`, and `tracked_disposition_ids`.

The `source_evidence` object pins the canonical digest and exact rendered file. Occurrence rows also record PDF and printed ranges, visible heading, and group. Provision rows record PDF page, printed page, section, detail, and nullable source-assigned label. Thus each broad tracked disposition below reverse-maps to complete proposal, selection, evidence, rationale, and resolution data without reproducing 207 machine rows in Markdown.

`DIFF-PROV-CEPTS32-T4-008` preserves the rendered Test case 4.1 result criterion as an observable MFA prompt or challenge before access. Its selected summary does not strengthen that evidence into the user or administrator completing or providing MFA. The row remains linked to `TD-PROV-SUMMARY` for the evidence-faithful paraphrase and `TD-PROV-LOCATOR` for its exact page, section, label, and detail dependencies.

All tracked dispositions are reconciled by Codex Inventory Reconciler R1 and have status `resolved`.

| Tracked ID | Class and linked machine rows | Author A proposal | Author B proposal | Selected result | Exact source evidence and atomization rationale |
|---|---|---|---|---|---|
| `TD-SEC-IDENTITY` | Occurrence identifiers; 15 rows | Alternate hierarchical IDs | IDs matching the visible hierarchy | Frozen selected IDs | Linked rows pin the exact rendered heading and ranges. Identity follows occurrence, not heading text alone. |
| `TD-SEC-BOUNDARY` | Synthetic occurrence additions/omissions; 7 rows | Seven extra unheaded continuation or procedure occurrences | No separate occurrences | Merge each into its visible parent | PDF pages 7 and 21-23 contain no separate headings at those boundaries. |
| `TD-SEC-PARENT` | Occurrence parents; 21 rows | Parent IDs based on Author A hierarchy | Parent IDs based on Author B hierarchy | Frozen rendered hierarchy | Linked rendered headings and indentation establish the parent; repeated notes retain occurrence-specific parents. |
| `TD-SEC-COORDINATES` | Occurrence range differences; 3 rows | Broader Test results, Fail, and Test 1 description ranges | Narrower rendered ranges | Exact frozen PDF and printed ranges | Pages 6-10 show where each visible heading's content begins and ends; coordinates do not expand merely because a later child or continuation exists. |
| `TD-SEC-HEADING` | Heading wording; 3 rows | Curly-apostrophe, short Figure 1, and alternate rights-page wording | Rendered-normalized wording | Frozen selected headings | Pages 4, 9, and 24 provide the exact visible occurrence identity; Figure 1 retains its caption. |
| `TD-SEC-DECISION` | Included/context-only; 5 rows | Several structural parents included | Structural-only parents context-only | Link-bearing occurrence controls | Pages 6-16 show whether an occurrence itself contains an unheaded atom; operative children do not make a structural parent included. |
| `TD-SEC-RATIONALE` | Original occurrence rationales; 55 rows | Author A original explanations | Author B original explanations | Selected concise rationale | Every linked row pins its rendered heading and ranges; rationale describes the selected occurrence decision without source copying. |
| `TD-COUNT-DERIVATION` | Ledger atom counts; 14 rows | Counts from Author A boundaries | Counts from Author B boundaries | Counts derived from 144 selected links | Linked section rows identify the exact occurrence; no proposed free-standing count overrides provision links. |
| `TD-ATOM-M` | Group M boundaries; 9 rows | 21 atoms; combines sampling/time, report ownership, access, and advisory uses but splits global fail restatement | 24 atoms; separates those elements and combines the fail restatement | 24 atoms | PDF pages 5-7: separate actions, timing, ownership, conditional access, and advisory uses where fulfillment differs; keep the duplicated failure clarification in one rule. |
| `TD-ATOM-T1` | Test 1 boundaries; 2 rows | 15 atoms; IaaS coverage combined with discovery | 16 atoms; separate IaaS applicability | 16 atoms | PDF page 8 / printed page 7, Sub-test 1.1 step 1: population coverage can differ from address discovery. |
| `TD-ATOM-S` | Sampling boundaries; 6 rows | 7 atoms; combines device populations and account reuse | 11 atoms; separates populations and reuse | 11 atoms | PDF page 10 / printed page 9, Sample testing: EUD, server, cloud, account-composition, and reuse applicability can differ. |
| `TD-ATOM-T2` | Test 2 result boundary; 1 row | Failure condition and residual pass split | Paired outcomes kept together | 9 atoms | PDF page 12 / printed page 11, Sub-test 2.1: a condition and its required fail or residual-pass outcomes form one decision rule. |
| `TD-ATOM-T3` | Test 3 boundaries; 13 rows | 30 atoms; combines applicability, compound numbered actions, and executable checks | 38 atoms including one cross-reference atom | 37 atoms after excluding navigation | PDF pages 13-16 / printed pages 12-15: separate populations, actions, observations, recorded evidence, and independently checkable executable properties. |
| `TD-ATOM-T3-XREF` | Navigation-only omission; 1 row | No atom | One prerequisite atom for the internal cross-reference | Excluded | PDF page 13 / printed page 12, Prerequisites: the reference to general prerequisites and Appendix B adds no independent action, condition, evidence duty, decision, result, or recommendation. |
| `TD-ATOM-C` | Conclusion boundaries; 10 rows | 10 atoms; combines deferral actors and predicate logic but splits certificate clauses | 10 atoms; separates deferral and predicates but combines three outcome/certificate clauses | 13 atoms | PDF page 20 / printed page 19: separate Assessor and Delivery Partner actions, assessment outcomes, certificate actions, and both numbered predicates. |
| `TD-ATOM-B` | Appendix B boundaries; 2 rows | 13 atoms; combines Certification Body definition and hosting | 14 atoms; separates definition and hosting | 14 atoms | PDF page 22 / printed page 21: subset definition and hosting are separately fulfillable responsibilities. |
| `TD-PROV-IDENTITY` | Provision identifiers; 100 rows | Sequential IDs under Author A boundaries | Sequential IDs under Author B boundaries | Re-numbered selected publication order | Per-row dual locators anchor semantics; IDs follow rather than determine the reconciled boundary. |
| `TD-PROV-SECTION-LINK` | Occurrence links; 51 rows | Links to Author A occurrence IDs | Links to Author B occurrence IDs | Link to one selected included occurrence | Per-row section and coordinates identify the exact occurrence; all selected links agree in group and derive ledger counts. |
| `TD-PROV-KIND` | Kind differences; 27 rows | Alternate applicability, procedure, recommendation, or rule classifications | Alternate classifications | Source-grammar-controlled kind | Per-row detail identifies the source clause: population is applicability, precondition is prerequisite, action is procedure, guidance is recommendation, and condition/outcome is decision or result. |
| `TD-PROV-ACTORS` | Actor differences; 11 rows | Some counterparties included or omitted | Some owners or counterparties treated as co-actors | Only directly assigned actors | Per-row actor basis and locator control. Ownership, consultation, or receipt alone does not create a co-duty. |
| `TD-PROV-SUMMARY` | Original summary wording; 137 rows | Author A concise paraphrase | Author B concise paraphrase | Selected original concise paraphrase, including the T4-008 prompt criterion | Each row pins the exact source element; selection preserves meaning without copied passages, modal source wording, or stronger evidence claims. |
| `TD-PROV-LABEL` | Source-assigned labels; 28 rows | Parent sub-test labels | Some composite step or predicate labels | Only publication-assigned labels | Per-row label and detail distinguish a true source label from locator detail; Figure 1 decisions remain exactly 1 through 7. |
| `TD-PROV-LOCATOR` | Locator wording/coordinates; 142 rows | Author A dual coordinates and details | Author B dual coordinates and details | Selected dual locator with no label duplication | Every row records exact PDF page, printed page, section, and detail against the rendered file. |

Machine validation proves semantic completeness: 207 unique difference IDs; zero unresolved rows; zero unlinked rows; zero unknown reverse links; zero unused tracked dispositions; and complete coverage of all 62 Author A occurrences, 55 Author B occurrences, 55 selected occurrences, 126 Author A provisions, 142 Author B provisions, and 144 selected provisions. The input and selected-oracle digests are pinned in the comparison. No substantive difference remains unresolved or unlinked.

## Locked result and safeguards

The reconciled oracle contains 144 provisions: `M` 24, `T1` 16, `S` 11, `T2` 9, `T3` 37, `T4` 9, `T5` 7, `C` 13, `A` 4, and `B` 14. Ledger counts are derived from provision links and sum to the same total.

The oracle contains no mapping, relationship, disposition, compliance statistic, or ESAF control reference. Mapping direction remains unset; future `esaf_to_external` and `external_to_esaf` work is explicitly independent. The exact eight prohibited inferences are locked. The Delivery Partner exception requires both numbered predicates and is neither an automatic pass nor a 95-percent score.

Normalized source passages and list/numbered items were extracted from the verified canonical text. The focused test freezes complete SHA-256 digests for all 3,055 distinct five-word windows and checks every five-word window in every controlled original-free-text value. This self-contained containment guard detects a copied source subpassage even when surrounding words are added, while separately allowing the approved source identity, title, and licence name. The source text remains outside Git. The sole permitted literal remains exactly once at `known_anomalies[0].source_literal`.
