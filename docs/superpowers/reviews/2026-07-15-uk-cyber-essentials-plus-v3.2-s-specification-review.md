# Cyber Essentials Plus v3.2 `S` batch specification review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-s-specification-reviewer
reviewer_role: independent specification and code-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 1a6886a93737a865624512a8a24f457be20dcf7f
reviewed_base_sha: c3275328fcbd2c97dc48afba98de19ff1f1f27ae
reviewed_range: c3275328fcbd2c97dc48afba98de19ff1f1f27ae..1a6886a93737a865624512a8a24f457be20dcf7f
specification_verdict: approved
task_quality_verdict: approved_with_minor_finding

## Independence and authority

The reviewer is distinct from the mapper, the mapping-rights reviewer, and the independently assigned `S` security and overclaiming reviewer. This review used authorized access to the pinned official NCSC Cyber Essentials Plus Test Specification v3.2. The reviewed source boundary is bound to canonical SHA-256 `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`, the locked oracle is bound to SHA-256 `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`, and ESAF control analysis remained limited to normative `## Requirement` text at immutable baseline `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`.

## Reviewed artifacts and evidence

The review covered `.superpowers/sdd/task-5-brief.md`, `.superpowers/sdd/task-5-report.md`, the complete 64,069-byte and 15-section package `.superpowers/sdd/review-c327532..1a6886a.diff`, the exact Git range, all 11 `S` records, the focused Plus test, lifecycle registry, both generated catalogs, the locked 144-row provision oracle, the committed 91-control manifest, mapping schema and validator behavior, and the pinned official source. The package reverse-applies cleanly to the candidate. Candidate `1a6886a93737a865624512a8a24f457be20dcf7f` was verified as the exact reviewed HEAD with parent `c3275328fcbd2c97dc48afba98de19ff1f1f27ae` and commit message `Map Cyber Essentials Plus sampling provisions`.

The candidate range contains exactly the 15 authorized paths: 11 new records, `cepts32-s-001.md` through `cepts32-s-011.md`, the focused test, the Plus lifecycle registry, and the two generated catalogs. No M or T1 record, oracle, inventory, manifest, schema, validator, design, plan, rights artifact, README, landing page, backlog, or review report is in the candidate range.

The implementation report's initial and per-record RED-to-GREEN history, frozen-source-copy correction, exact staged-path audit, postcommit checks, and clean candidate state were considered. Independent review reran the 14-test focused suite, all 309 repository tests, control validation, both ordinary and pinned-baseline crosswalk checks, link validation, exact-range `git diff --check`, exact package reverse-application, and cache inspection. All substantive gates passed; 3 platform-dependent tests were skipped because Windows symlink privileges were unavailable. No `__pycache__` directory was present.

## Complete specification assessment

All records appear in locked oracle order as `CEPTS3.2-S-001` through `CEPTS3.2-S-011`. Their identifiers, group, kind, actors, original summaries, official URL, and rendered dual-coordinate locators match the oracle exactly. Every record remains `draft` and carries the required mapper identity, date, and authorized-source provenance. Ten records use `no_direct_mapping`, have empty relationship arrays, and begin a provision-specific rationale with `Missing outcome:`. No record uses `out_of_scope`.

The ten negative dispositions correctly preserve the outcomes absent from ESAF: application of remaining tests to the agreed computing-device population; inclusion of end-user devices, every internal server, and all cloud-service types; representative-device selection when full testing is impractical; confidence in population representation across configuration and provisioning variation; verification of the Delivery Partner sample-size calculation; representative per-service cloud-account testing; the required ordinary and administrative account mix; and reuse of sampled users across services. General inventory, boundary, identity-governance, and assessment-sampling duties do not establish those external populations or mechanics. The records do not use conditions, adjacent capabilities, implementation guidance, or assessment procedures to manufacture selection, representativeness, sample construction, execution, or coverage.

The exact positive set is solely `CEPTS3.2-S-008 -> CMP-110`, with one `partially_supports`, `narrow`, high-confidence, forward-only `esaf_to_external` leg. Its control version, path, digest, and requirement locator match the committed manifest. CMP-110 normatively requires the organization to retain governed AI records and evidence according to applicable retention requirements. The condition limits the relationship to calculation evidence already governed as an AI record and to a certificate-lifetime period already applicable to that record. It does not create the calculation, make it correct, supply the Delivery Partner method, assign the Certifying Body, select or test a sample, establish representativeness, or assert sample or population coverage. The rationale, expected evidence, known gaps, and prohibited inferences keep the contribution limited to retention and expressly reject procedure execution, observed results, certification, compliance, equivalence, endorsement, and aggregate assurance.

## Tests, lifecycle, and generated artifacts

The completed-batch helper remains oracle-ordered and fail-closed for exact path equality, metadata, locators, provenance, record structure, source-copy boundaries, and manifest-bound relationship provenance. The S-batch assertion locks the exact positive ID set to S-008, the relationship count to one, and the negative count to ten without importing a feasibility conclusion. The closure test permits only neither or both S reports, requires authorized-source attestations, parses reviewer IDs, and proves pairwise distinction among mapper, rights reviewer, specification reviewer, and overclaiming reviewer.

The lifecycle remains `draft`, its event array remains empty, and snapshot digest `bc9dffa101bffd59efec168b67786f0b32ec217290e7af328a98c1c45bf2b9fb` matches the candidate snapshot. Generated JSON and Markdown catalogs consistently contain 51 completed Plus provisions and repository totals of 2 mapping sets, 167 provisions, 46 relationships, and 122 negative dispositions.

Fresh independent validation produced these results on the exact candidate before report creation:

- Focused Plus mapping suite: 14 tests passed.
- Full repository suite: 309 tests passed, 3 skipped.
- Control validation: 91 controls, 91 objectives, and 16 families passed.
- Crosswalk validation in ordinary and pinned-baseline modes: passed with 2 mapping sets, 167 provisions, 46 relationships, and 122 negative dispositions.
- Link validation: passed for 392 tracked Markdown files.
- Exact-range `git diff --check`, package reverse-application, and zero-cache inspection: passed.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: the implementation report records link validation against 381 tracked Markdown files, while a fresh run on the exact candidate validates 392. The 11-file difference is exactly the new S record population. The fresh complete gate passes, so this is a stale evidence count in the implementation report rather than a candidate or validator defect.

## Verdicts

Specification verdict: **approved**. Exact candidate `1a6886a93737a865624512a8a24f457be20dcf7f` satisfies the binding Task 5 specification: exact S scope and oracle fidelity, draft/schema/provenance requirements, normative-only ESAF citation, one correctly bounded S-008/CMP-110 retention leg, ten provision-specific negative dispositions, exact count and closure-identity tests, and deterministic lifecycle and catalog derivation. No condition manufactures device or account selection, representativeness, sampling, testing execution, or coverage.

Task and code-quality verdict: **approved with one minor evidence finding**. The implementation is focused, deterministic, validator-backed, and supported by credible per-record TDD evidence. The stale link-validation file count should be corrected when the implementation report is next maintained, but fresh full-scope validation establishes the gate result and no candidate-content change is required before the report-only closure commit.
