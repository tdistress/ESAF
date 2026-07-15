# Cyber Essentials Plus v3.2 Source Inventory Traceability

**Status:** Pending exact-head reviews

**Scope:** Public-source inventory and locked provision oracle for the NCSC *Cyber Essentials Plus Test Specification* v3.2. This record contains no mapping snapshot, relationship leg, certification claim, or current-operational-scheme completeness claim.

## Pinned source and derived-record identity

| Artifact | Identity |
|---|---|
| Canonical NCSC PDF | 424,226 bytes; 24 PDF pages; SHA-256 `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8` |
| Legacy official NCSC PDF | 419,191 bytes; 24 PDF pages; SHA-256 `d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694` |
| Locked oracle | SHA-256 `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc` |
| Tracked reconciliation record | SHA-256 `6563dfaeac62fd505edf49661ab0b826b00a67778af7de9b29029af16f0fd284` |
| Rights review and R2 re-attestation | SHA-256 `dd4e380087d5ae487f432dc08843e5c9d9dd57711cd7904403955359fb701ab1` |
| Focused inventory contract test | SHA-256 `3663fc611416eefcdda7dba924761fb72a7feb67edc66df214060bab33e8acf2` |
| Focused link-validator test | SHA-256 `72fec52a30208e6a82c4cd0bc5cc5434dcb4717bddca01d9f978d9d6782b04b4` |
| Link validator | SHA-256 `bdca046054d16ad18877d2ca3343acfd751b3a09be53c488fc2a605b7f4fd87e` |
| Independent Author A inventory | SHA-256 `54b288ac07e9a3acf33ecc1db187f8410c1a9502a5bd9ecf4e5820fddd0a1559` |
| Independent Author B inventory | SHA-256 `8c62f87697d9bb8965363924c26c25ec08a20bd07ac537c76b7191ae17c37604` |
| External semantic comparison | SHA-256 `ec77e0b12b2b5ddc59fabbfeb59a77a518bb1ea060850974d863dd2c150f29b1` |

The canonical acquisition source is the NCSC resource-page target dated 2025-04-28 and accessed 2026-07-14. The legacy URL is retained as a known official byte variant. The source version remains 3.2 and the displayed publication date remains April 2025.

## Rights sequencing and re-attestation

Codex Rights Reviewer R1 approved the publication boundary before inventory work in commit `6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6`. That commit changes only the rights-review record. Both inventory authors attest that they began after verifying this approval, and the oracle records `inventories_started_after_rights_commit: true`.

The approved boundary attributes the NCSC, applies OGL v3.0 to the covered NCSC material, permits the exact six-element rights universe, excludes marks, imagery, third-party material, copied passages, and endorsement implications, and keeps IASME material in a separate closed partition. Copied requirement or passage text is prohibited except for `known_anomalies[0].source_literal`, whose exact value occurs once as `tests 2 to 7`.

On 2026-07-14, the same independent rights reviewer re-attested the exact R2 correction without reservation. The review covered all 509 original-free-text instances, all 36 prior reparaphrases, the B-001 complete required-file outcome, the T4-008 prompt criterion, the 3,055-digest containment guard, all 55 ledger rationales, all 144 actor bases, summaries, and locator details, and all six assurance-boundary statements. It confirmed the oracle, semantic-comparison, reconciliation, and focused-inventory-test hashes above, found no unapproved copied narrative window or IASME-derived inventory content, and did not expand or retroactively alter the pre-inventory publication basis.

Codex Rights Reviewer R1 is distinct from Codex Inventory Author A, Codex Inventory Author B, and Codex Inventory Reconciler R1.

## Independent source review and reconciliation

Both authors independently inspected `page-01.png` through `page-24.png` at original detail and used the canonical text extraction only as supporting evidence. All 24 rendered pages were accounted for. Figure 1 on PDF page 9 / printed page 8 was visually traced into exactly seven decision-rule atoms, one for each numbered decision, with Yes and No retained as branches rather than atoms. PDF page 24 was independently confirmed as a standalone publication-wide rights page.

| Independent inventory | Author | Occurrences | Provisions | Group counts in publication order |
|---|---|---:|---:|---|
| Author A | Codex Inventory Author A | 62 | 126 | `M=21, T1=15, S=7, T2=10, T3=30, T4=9, T5=7, C=10, A=4, B=13` |
| Author B | Codex Inventory Author B | 55 | 142 | `M=24, T1=16, S=11, T2=9, T3=38, T4=9, T5=7, C=10, A=4, B=14` |

Neither author accessed, searched for, compared with, or inferred the other author's file, occurrence set, atom list, or provisional count before reconciliation. Codex Inventory Reconciler R1 selected the rendered occurrence hierarchy before deriving the final atom count.

The external semantic comparison contains 207 stable difference rows: 62 occurrence rows and 145 provision rows. Every row records both author proposals, the selected result, source evidence, rationale, reconciler, resolution, and one or more links into the 23-entry tracked disposition universe. Validation found zero unresolved or unlinked rows, duplicate difference identifiers, unknown or unused disposition links, or uncovered Author A, Author B, or selected records.

The tracked semantic dispositions cover occurrence identity, boundaries, parents, coordinates, headings, inclusion decisions, rationales, and link-derived counts; group-specific atom boundaries for M, T1, S, T2, T3, C, and B; the navigation-only Test 3 cross-reference omission; and provision identity, occurrence links, kinds, actors, summaries, source labels, and locators. The principal selections separate independently fulfillable actions, evidence, populations, actors, outcomes, and conjunctive predicates; keep each condition with its required result; exclude navigation-only text; and retain only publication-assigned labels.

## Exact reconciled occurrence set

The selected occurrence set is the following ordered set. Atom counts are derived from provision links; context-only occurrences therefore have zero atoms.

| Section ID | Decision | Group | Atoms | Heading |
|---|---|---:|---:|---|
| `sec-m-cover` | context_only | M | 0 | Cover |
| `sec-m-contents` | context_only | M | 0 | Contents |
| `sec-m-whats-new` | context_only | M | 0 | What's new |
| `sec-m-audience` | context_only | M | 0 | Audience |
| `sec-m-purpose` | included | M | 1 | Purpose |
| `sec-m-before-you-begin` | included | M | 10 | Before you begin |
| `sec-m-general-prerequisites` | included | M | 5 | General prerequisites for testing |
| `sec-m-success-criteria` | context_only | M | 0 | Success criteria |
| `sec-m-test-results` | included | M | 1 | Test results |
| `sec-m-pass` | included | M | 2 | Pass |
| `sec-m-fail` | included | M | 2 | Fail |
| `sec-m-advisory-notes` | included | M | 3 | Advisory notes |
| `sec-t1-test-case` | context_only | T1 | 0 | Test case 1: Remote vulnerability assessment |
| `sec-t1-purpose` | context_only | T1 | 0 | Test purpose |
| `sec-t1-description` | context_only | T1 | 0 | Test description |
| `sec-t1-prerequisites` | included | T1 | 4 | Prerequisites |
| `sec-t1-subtest-1-1` | included | T1 | 4 | Sub-test 1.1 |
| `sec-t1-figure-1` | included | T1 | 7 | Figure 1: Sub-test flow diagram for assessing services accessible through the firewall |
| `sec-t1-interpretation` | included | T1 | 1 | Interpreting the test case results |
| `sec-s-sample-testing` | included | S | 11 | Sample testing |
| `sec-t2-test-case` | included | T2 | 1 | Test case 2: Check patching, by authenticated vulnerability scan of devices |
| `sec-t2-purpose` | context_only | T2 | 0 | Test purpose |
| `sec-t2-description` | context_only | T2 | 0 | Test description |
| `sec-t2-prerequisites` | included | T2 | 1 | Prerequisites |
| `sec-t2-subtest-2-1` | included | T2 | 6 | Sub-test 2.1 |
| `sec-t2-interpretation` | included | T2 | 1 | Interpreting the test case results |
| `sec-t3-test-case` | included | T3 | 1 | Test case 3: Check malware protection |
| `sec-t3-purpose` | context_only | T3 | 0 | Test purpose |
| `sec-t3-description` | context_only | T3 | 0 | Test description |
| `sec-t3-prerequisites` | included | T3 | 1 | Prerequisites |
| `sec-t3-select-subtests` | included | T3 | 1 | Selecting appropriate sub-tests |
| `sec-t3-subtest-3-1` | included | T3 | 3 | Sub-test 3.1 (for devices that use anti-malware software) |
| `sec-t3-subtest-3-1-1` | included | T3 | 11 | Sub-test 3.1.1 (Check effectiveness of defences against malware delivered by email) |
| `sec-t3-subtest-3-1-2` | included | T3 | 8 | Sub-test 3.1.2 (Check effectiveness of defences against malware delivered by browser) |
| `sec-t3-subtest-3-1-3` | included | T3 | 4 | Sub-test 3.1.3 (Manual Checks for devices that use anti-malware software) |
| `sec-t3-subtest-3-2` | included | T3 | 7 | Sub-test 3.2 (for devices that use certificate-based application allow listing) |
| `sec-t3-interpretation` | included | T3 | 1 | Interpreting the test case results |
| `sec-t4-test-case` | included | T4 | 1 | Test case 4: Check multi-factor authentication configuration |
| `sec-t4-purpose` | context_only | T4 | 0 | Test purpose |
| `sec-t4-description` | included | T4 | 3 | Test description |
| `sec-t4-case-4-1` | included | T4 | 4 | Test case 4.1 |
| `sec-t4-interpretation` | included | T4 | 1 | Interpreting the test case results |
| `sec-t5-test-case` | included | T5 | 1 | Test case 5: Check account separation |
| `sec-t5-purpose` | context_only | T5 | 0 | Test purpose |
| `sec-t5-description` | included | T5 | 2 | Test description |
| `sec-t5-case-5-1` | included | T5 | 3 | Test case 5.1 |
| `sec-t5-interpretation` | included | T5 | 1 | Interpreting the test case results |
| `sec-c-conclude` | included | C | 10 | Conclude the assessment |
| `sec-c-note-deferral` | included | C | 1 | Note for Delivery Partner |
| `sec-c-note-exception` | included | C | 2 | Note for Delivery Partner |
| `sec-a-appendix` | included | A | 3 | Appendix A: Vulnerability scanning |
| `sec-a-note-delivery-partner` | included | A | 1 | Note for Delivery Partner |
| `sec-b-appendix` | included | B | 11 | Appendix B: Types of test file |
| `sec-b-note-delivery-partner` | included | B | 3 | Note for Delivery Partner |
| `sec-m-rights-notice` | context_only | M | 0 | Rights and attribution notice |

## Derived final counts

Every provision links to exactly one included occurrence in the same group. Summing those links yields 144 provisions and the exact group counts `M=24, T1=16, S=11, T2=9, T3=37, T4=9, T5=7, C=13, A=4, B=14`. The same link derivation reproduces every occurrence atom count above. No free-standing proposed count overrides the locked provisions.

## Validator TDD and preliminary command evidence

Focused tests cover every Git-tracked Markdown file; relative and repository-root paths; directory indexes; inline and reference-style destinations; balanced nested parentheses; same-file and target fragments; inline-code and duplicate heading anchors; URL-decoded paths and fragment boundaries; missing targets and anchors; decoded and plain repository escapes; ignored external/network URLs; complete file, line, and original-target diagnostics; deterministic diagnostic order; exclusion of untracked Markdown; and the exact exit contract of 0 for success, 1 for broken links, and 2 for operational failure.

For the consolidated parser correction, nine focused tests ran before the implementation change. Three failed for the intended reasons: a broken reference definition was ignored with exit 0, a nested balanced-parenthesis target was truncated in the diagnostic, and a URL-decoded fragment could not match a heading containing inline code. The strengthened broken-link exit-1 and operational-failure exit-2 assertions already passed. After replacing the flat parsing layer, all nine focused tests passed. Self-review then exposed that the reference destination was checked without proving full and collapsed usage lookup; one added focused test failed because both undefined usages returned exit 0. Normalized definition lookup resolved that gap, and the final ten-test suite passed. The complete preliminary rerun below is the authoritative GREEN evidence.

The exact-head final review then found four Important gaps. Test-first regressions proved that shortcut text/image references were not recognized, the final directory-index candidate could escape through a link, a copied five-word source window with surrounding words bypassed the durable gate, and T4-008 strengthened an observable MFA prompt into providing MFA. The directory-index RED reproduced against the prior implementation through a Windows junction: expected `target escapes repository`, observed `target does not exist`. The completed fixes recognize CommonMark shortcuts only when defined, resolve and recheck the final directory index, freeze all 3,055 source-window SHA-256 digests without source text, reparaphrase all exposed copies, and preserve the T4-008 prompt/challenge criterion. Rights Reviewer R1 re-attested the exact hashes above before this record and the complete gates were refreshed.

R2 review then found that B-001's `broad collection` wording could be incomplete. Its focused regression failed against that wording and now locks the original five-word-safe summary `Supply each Certification Body with every assessment file needed for testing.` The correction preserves the comprehensive all-required outcome without changing the actor, kind, section link, locator, counts, or structure. R2 also corrected the digest-method description: numbered items are split into 91 passages, while the mojibake bullet marker is conservatively not treated as a boundary. The 3,055-window frozen set contains all 2,878 bullet-split windows plus exactly 177 cross-bullet windows and loses none of the bullet-split coverage. Rights Reviewer R1 independently reproduced these results and re-attested the exact R2 hashes before traceability finalization.

Preliminary command results on the completed working-tree content were:

| Command | Result |
|---|---|
| `python -m unittest tests.test_validate_links -v` | 14 tests passed in 6.959 seconds; the Windows directory-junction containment regression executed without a skip |
| `python -m unittest tests.test_uk_cyber_essentials_plus_v32_inventory -v` | 20 tests passed in 0.272 seconds |
| `python -m unittest discover -s tests -v` | 240 tests passed in 168.055 seconds; 3 expected Windows symlink-capability skips |
| `python tools/validate_controls.py --check` | 91 controls, 91 objectives, and 16 families validated |
| `python tools/validate_architectures.py` | 10 foundation files and 7 reserved patterns validated |
| `python tools/validate_crosswalks.py --check --baseline-ref $base` | 1 mapping set, 116 provisions, 41 relationships, and 76 negative dispositions validated |
| `python tools/validate_links.py --check` | 326 tracked Markdown files validated with all repository-local links resolving |
| `git diff --check` | exited 0 for the complete working-tree correction |

## Changed files

This R2 correction changes exactly these tracked files:

- `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-inventory-reconciliation.md`
- `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md`
- `docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-traceability.md`
- `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`
- `tests/test_uk_cyber_essentials_plus_v32_inventory.py`

Independent specification/inventory review and independent security/overclaiming review remain required on one immutable exact head. Their identities, dispositions, ancestry evidence, integration checks, and protected-branch results belong in external pull-request or check evidence so this tracked record remains non-self-referential.
