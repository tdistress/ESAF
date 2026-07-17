# Cyber Essentials Plus v3.2 S Security and Overclaiming Review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-s-overclaiming-reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 1a6886a93737a865624512a8a24f457be20dcf7f
reviewed_base_sha: c3275328fcbd2c97dc48afba98de19ff1f1f27ae
review_disposition: approved

## Scope and independence

This independent review covers the exact candidate range
`c3275328fcbd2c97dc48afba98de19ff1f1f27ae..1a6886a93737a865624512a8a24f457be20dcf7f`
for `CEPTS3.2-S-001` through `CEPTS3.2-S-011`, the focused regression
contract, lifecycle digest, and generated catalogs. The reviewer is distinct
from the mapper, mapping-rights reviewer, and S specification reviewer.

The review used the authorized pinned official NCSC Cyber Essentials Plus
Test Specification v3.2 source, whose canonical SHA-256 is
`2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`,
the locked 144-provision oracle, the committed 91-control ESAF manifest, and
exact `## Requirement` text from ESAF baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. Reviewed artifacts also include
`.superpowers/sdd/task-5-brief.md`, `.superpowers/sdd/task-5-report.md`, and the
complete candidate package `.superpowers/sdd/review-c327532..1a6886a.diff`.
HEAD was verified as the exact reviewed candidate before analysis and again
before report creation.

## Security and overclaiming assessment

- All 11 dispositions were reviewed provision-first. The ten
  `no_direct_mapping` records preserve the missing remaining-test population,
  device and cloud-service inclusion, device-sample selection,
  representativeness, population confidence, sample-size calculation
  verification, cloud-account test selection, minimum account composition,
  and cross-service user-reuse outcomes.
- The negative review specifically considered narrower normative duties in
  AUD-100, IAM-100, IAM-120, IAM-130, INF-100, and related scope and inventory
  controls. Those duties define AI assessment sampling, identify or govern AI
  identities and infrastructure, or establish AI boundaries. They do not put
  the stated device, server, cloud-service, or account populations into the
  external methodology; select or execute the samples; establish
  representativeness; verify the Delivery Partner calculation; prescribe the
  account mix; or authorize cross-service reuse. No narrower direct support
  was omitted.
- `CEPTS3.2-S-008 -> CMP-110` is a justified `partially_supports`, `narrow`,
  high-confidence leg. CMP-110 directly mandates retention of governed AI
  records and evidence according to applicable retention requirements. The
  condition only limits the relationship to calculation evidence already
  governed as an AI record and to a certificate-lifetime period already
  applicable to that record. It does not manufacture the calculation or its
  existence, correctness, method, actor, selection, representativeness,
  procedure execution, sample coverage, population coverage, or sufficiency.
  The expected evidence, known gaps, and prohibited inferences maintain those
  boundaries.
- All records remain original paraphrases and derivative analysis within the
  authorized public-source boundary. The frozen source-copy guard passes, the
  public v3.2 source is not represented as the current operational scheme,
  and no IASME-only structure or outcome is inferred.
- The mapping remains forward-only `esaf_to_external` and draft. Neither the
  positive leg nor the batch implies reverse coverage, an observed result,
  procedure execution, sample or population sufficiency, full-population or
  continuous assurance, assessment success, certification, compliance,
  equivalence, endorsement, or current-scheme completeness.

## Validation evidence

- Focused Plus mapping suite: 14 tests passed in 11.396 seconds, including the
  frozen source-copy guard, exact S positive set and counts, baseline-manifest
  binding, draft catalog assertions, and fails-closed closure behavior.
- Crosswalk validation passed in ordinary and pinned-baseline modes with 2
  mapping sets, 167 provisions, 46 relationships, and 122 negative
  dispositions.
- Link validation passed for 392 tracked Markdown files.
- Whole-range `git diff --check` passed for the exact reviewed base and
  candidate; the candidate worktree was clean before report creation and had
  no Python cache directories.
- The implementation report records a full repository suite of 309 passing
  tests with 3 skipped, control validation of 91 controls and 91 objectives,
  exact candidate scope, and clean postcommit validation.

## Findings

- Critical: none.
- Important: none.
- Minor: none.

## Disposition

Approved. Exact candidate
`1a6886a93737a865624512a8a24f457be20dcf7f` is approved for Task 5 S-batch
technical closure from the security and overclaiming perspective. This
approval does not promote the draft snapshot or establish sample or
population coverage, procedure execution, assessment success, certification,
compliance, equivalence, endorsement, current-scheme coverage,
full-population assurance, or continuous assurance.
