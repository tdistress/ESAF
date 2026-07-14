# UK Cyber Essentials Plus v3.2 inventory reconciliation

**Reconciler:** Codex Inventory Reconciler R1

**Inventory authors:** Codex Inventory Author A and Codex Inventory Author B

**Source:** Canonical 24-page PDF, SHA-256 `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`

**Rights record:** `6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6`
**Disposition:** Reconciled with no unresolved difference

## Independence, source, and rights sequence

The two author artifacts were opened only after both independent inventories and their Task 2 review were complete. The reconciler inspected rendered pages 1 through 24 at original detail, traced all seven Figure 1 decisions and branches, and used the text extraction only to locate and compare passages. Neither author's provision count controlled the independently locked occurrence hierarchy.

`git merge-base --is-ancestor 6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6 HEAD` returned success before reconciliation. `git diff-tree --root --no-commit-id --name-status -r 6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6` showed that commit introduced only the approved rights record. Both author reports state that inventory work began after that commit.

An external exhaustive leaf comparison is retained as `task-3-machine-comparison.json` in the verified temporary task root. It pins both input digests, records 1,906 differing leaf paths, retains both proposed values, and assigns each path to one of the disposition classes below. It is evidence, not a source artifact, and is intentionally not tracked.

## Independently locked section-occurrence hierarchy

The rendered publication establishes 55 ordered occurrences. The hierarchy follows visible headings plus Figure 1. An unheaded provision remains in its visible parent occurrence rather than creating a synthetic section. A structural parent is `context_only` when all operative content is in child occurrences; it is `included` when it also carries an unheaded applicability or other provision. The final rights page is a root `M` occurrence, not an Appendix B child.

The exact ordered IDs are frozen in the focused test:

`sec-m-cover`, `sec-m-contents`, `sec-m-whats-new`, `sec-m-audience`, `sec-m-purpose`, `sec-m-before-you-begin`, `sec-m-general-prerequisites`, `sec-m-success-criteria`, `sec-m-test-results`, `sec-m-pass`, `sec-m-fail`, `sec-m-advisory-notes`, `sec-t1-test-case`, `sec-t1-purpose`, `sec-t1-description`, `sec-t1-prerequisites`, `sec-t1-subtest-1-1`, `sec-t1-figure-1`, `sec-t1-interpretation`, `sec-s-sample-testing`, `sec-t2-test-case`, `sec-t2-purpose`, `sec-t2-description`, `sec-t2-prerequisites`, `sec-t2-subtest-2-1`, `sec-t2-interpretation`, `sec-t3-test-case`, `sec-t3-purpose`, `sec-t3-description`, `sec-t3-prerequisites`, `sec-t3-select-subtests`, `sec-t3-subtest-3-1`, `sec-t3-subtest-3-1-1`, `sec-t3-subtest-3-1-2`, `sec-t3-subtest-3-1-3`, `sec-t3-subtest-3-2`, `sec-t3-interpretation`, `sec-t4-test-case`, `sec-t4-purpose`, `sec-t4-description`, `sec-t4-case-4-1`, `sec-t4-interpretation`, `sec-t5-test-case`, `sec-t5-purpose`, `sec-t5-description`, `sec-t5-case-5-1`, `sec-t5-interpretation`, `sec-c-conclude`, `sec-c-note-deferral`, `sec-c-note-exception`, `sec-a-appendix`, `sec-a-note-delivery-partner`, `sec-b-appendix`, `sec-b-note-delivery-partner`, `sec-m-rights-notice`.

The frozen tuple for every occurrence includes its parent, exact heading, group, PDF range, nullable printed range, and decision. Repeated headings remain distinct occurrences: the two conclusion notes have separate IDs, as do the Appendix A and Appendix B notes. Coordinates and parents are asserted as exact ordered equality, not inferred from atom totals.

## Difference dispositions

| Difference class | Author A proposal | Author B proposal | Selected result and source evidence | Atomization rationale |
|---|---|---|---|---|
| Occurrence set | 62 occurrences, including synthetic unheaded continuation/procedure occurrences | 55 visible heading/figure occurrences | 55 rendered occurrences | Visible publication hierarchy controls; unheaded text belongs to its visible parent. |
| Structural parent decision | Several parent headings marked included merely because operative children follow | Structural-only parents marked context-only | Author B convention | A provision links to the occurrence containing it; a parent is not included solely because a child is operative. |
| Test 1 parent | Root and description included | Root and description context-only | Author B | Page 8 places operative provisions under Prerequisites and Sub-test 1.1. |
| Tests 2-5 parents | Roots included; description parents included | Roots included for their unheaded population lines; descriptions context-only | Author B | The population line is directly under each case heading, while description content is assigned to children except where the description itself contains unheaded provisions. |
| Appendices | Synthetic unheaded child occurrences | Operative unheaded content linked to appendix root, note kept as child | Author B | Pages 21-23 show appendix and note headings only. |
| Final page | Root `M` occurrence with alternate ID | Root `M` occurrence | `sec-m-rights-notice` | Page 24 is publication-wide rights material with no appendix heading or printed page. |
| Before-you-begin sampling | One atom combines sample identification and schedule | Two atoms | Author B | Sample selection and timing can be fulfilled and evidenced separately. |
| Report-template bullet | One Assessor atom combines possession and Delivery Partner format assignment | Separate Assessor and Delivery Partner atoms | Author B | Actors and actions differ within the bullet. |
| General test-file prerequisite | One atom combines host-site condition and conditional access | Separate host-site prerequisite and access recommendation | Author B, with Assessor as sole actor on hosting | The conditional access action can differ; Certification Body ownership is a condition, not a co-duty. |
| Global fail text | Two atoms for propagation and a clarifying restatement | One atom | Author B | The second bullet restates the same overall-failure rule and exception rather than adding independent fulfillment. |
| Advisory notes | Two atoms, combining both uses | Three atoms | Author B | Optional attachment, improvement advice, and decision rationale can differ. |
| Test 1 address discovery | One action includes IaaS coverage | Action plus separate IaaS applicability atom | Author B | Population coverage can differ from the discovery action. |
| Sample testing population | One combined population atom | Separate boundary, EUD, server, and cloud population atoms | Author B | The listed populations can differ in applicability and later relationship. |
| Cloud account reuse | Combined with minimum account composition | Separate recommendation | Author B | Minimum composition and optional reuse are independent. |
| Test 2 pass/fail branch | Failure condition and residual pass split | One decision rule | Author B | The condition and its paired outcomes form one decision rule. |
| Test 3 cross-reference | Excluded | Separate prerequisite atom | Excluded | Page 13 points to already inventoried general prerequisites and Appendix B; navigation adds no new action or outcome. |
| Test 3.1 applicability | Combined with installed/running check | Separate population and check atoms | Author B | Applicability is preserved separately when it defines the device population. |
| Email numbered steps | Three compound step atoms | Seven atoms separating send, observe, select, prepare, record | Author B | Actions and evidence can be fulfilled or related independently. |
| Allow-list executable bullet | One atom combines unsigned and untrusted-chain executables | Two atoms | Author B | The two executable properties are independently checkable. |
| Conclusion deferral | One multi-actor decision atom | Assessor consultation and Delivery Partner discretion split | Author B | Actors and actions differ. |
| Normal overall pass | Result and certificate action split by A, combined by B | Both proposals considered | Split into result and certificate action | Assessment outcome and certificate issuance are distinct actions with different future relationships. |
| Discretionary pass | Pass and certificate action split by A, combined by B | Both proposals considered | Split into Delivery Partner outcome and Assessor certificate action | Actors and effects differ. |
| Exception predicates | One combined conjunctive atom | Two numbered predicate atoms | Author B | Each numbered predicate is independently assessable; the structured exception separately requires both. |
| Residual failure | Result and no-award action split by A, combined by B | Both proposals considered | Split into result and certificate action | Failure determination and withholding a certificate can differ. |
| Appendix B responsibilities | Certification Body definition and hosting combined | Definition and hosting split | Author B | The two actions can be evidenced separately. |
| Appendix B criteria | Delivery Partner design recommendations | Assessor decision criteria | Author B | The paragraph expressly introduces result criteria; expected behavior is evaluated by the Assessor. |
| Applicant-specific subset | Certification Body only | Delivery Partner and Certification Body | Certification Body only | The prior sentence assigns the Certification Body responsibility for defining the subset; the Delivery Partner's separate encouragement is already its own atom. |
| Identifiers | Sequential within Author A boundaries | Sequential within Author B boundaries | Re-numbered after reconciliation | IDs follow the final publication-ordered group sequence and do not decide boundaries. |
| Source-assigned labels | Parent sub-test labels | Composite labels that added step text | Only publication-assigned sub-test/case labels; Figure 1 decisions 1-7 exact | Locator details identify step portions without inventing source labels or duplicating labels. |
| Kinds | Several permissive statements classified as applicability or procedure | Mostly recommendation/decision classifications | Source grammar controls per record | `may`/`should` guidance is recommendation; population is applicability; condition/outcome is decision or result rule. |
| Actors | Some counterparties treated as co-actors | Some ownership/counterparty references treated as co-actors | Only grammatically assigned actors | Ownership, consultation, or receipt alone does not create a co-duty; every multi-actor atom names each actor in `actor_basis`. |
| Summary and locator wording | Original Author A paraphrases/details | Original Author B paraphrases/details | Author B paraphrases retained for selected atoms; Author A wording retained where its split controlled; new original wording only for reconciled conclusion splits | No source passage is copied; locators use both coordinate systems and no locator-level source label. |
| Scratch metadata | Author-specific inventory envelope | Different author-specific envelope | Replaced by the closed oracle contract | Scratch provenance is preserved through named authors and reconciler, not copied as parallel schema. |

All additions, omissions, boundary differences, ID shifts, kind/actor differences, summary differences, locator differences, parent differences, coordinates, and scratch-envelope differences fall within the table above and the path-complete machine comparison. No difference remains unresolved.

## Locked result and safeguards

The reconciled oracle contains 144 provisions: `M` 24, `T1` 16, `S` 11, `T2` 9, `T3` 37, `T4` 9, `T5` 7, `C` 13, `A` 4, and `B` 14. Ledger counts are derived from provision links and sum to the same total.

The oracle contains no mapping, relationship, disposition, compliance statistic, or ESAF control reference. Mapping direction remains unset; future `esaf_to_external` and `external_to_esaf` work is explicitly independent. The exact eight prohibited inferences are locked. The Delivery Partner exception requires both numbered predicates and is neither an automatic pass nor a 95-percent score.

Normalized source passages and list/numbered items were extracted from the verified canonical text. Their 235 SHA-256 digests are frozen in the focused test, so source-copy validation is self-contained after deletion of the temporary task root. The sole permitted literal remains exactly once at `known_anomalies[0].source_literal`.
