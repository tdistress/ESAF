# Cyber Essentials Plus v3.2 T1 Security and Overclaiming Review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t1-overclaiming-reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 98fce9ea0f71285b2198a17e5d4fa373a8c8d689
reviewed_base_sha: 1ab5375784671b6674e05f51f1802eb91cf9676f
review_disposition: approved

## Scope and independence

This independent review covers the exact candidate range
`1ab5375784671b6674e05f51f1802eb91cf9676f..98fce9ea0f71285b2198a17e5d4fa373a8c8d689`
for `CEPTS3.2-T1-001` through `CEPTS3.2-T1-016`, the focused regression
contract, lifecycle digest, and generated catalogs. The reviewer is distinct
from the mapper, mapping-rights reviewer, and T1 specification reviewer.

The review used the authorized pinned official NCSC Cyber Essentials Plus
Test Specification v3.2 source, whose canonical SHA-256 is
`2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`,
the locked 144-provision oracle, the committed 91-control ESAF manifest, and
exact `## Requirement` text from ESAF baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. Reviewed artifacts also include
the approved mapping design and plan, `.superpowers/sdd/task-4-brief.md`, the
corrected Task 4 implementation report, and the complete candidate package
`.superpowers/sdd/review-1ab5375..98fce9e.diff`.

## Security and overclaiming assessment

- All 16 dispositions were reviewed provision-first. The fourteen
  `no_direct_mapping` records preserve the missing scanner approval and
  execution, IP/DNS/IaaS population, prescribed port set, Figure application,
  score threshold, public-read-only pass, two-factor, throttling, lockout, and
  aggregate-result outcomes. No implementation guidance, assessment
  procedure, adjacent capability, condition, discovered-service state, or
  chain aggregation supplies those outcomes.
- `CEPTS3.2-T1-011 -> IAM-110` is a justified `partially_supports`, `narrow`,
  high-confidence leg. IAM-110 directly requires authentication before access
  to non-public AI assets. The condition limits the relationship to a user
  accessing such assets through the assessed Internet service. The gaps and
  prohibited inferences preserve the absent Assessor assignment, universal
  Internet-service coverage, Figure execution, branch and result assignment,
  procedure or test execution, certification, compliance, equivalence, and
  endorsement.
- `CEPTS3.2-T1-013 -> IAM-140` is a justified `partially_supports`, `narrow`,
  high-confidence leg. IAM-140 directly requires rotation of credentials used
  by AI capabilities. The condition identifies the service default password as
  that governed credential, and expected evidence requires a record that the
  credential was rotated or changed. The gaps preserve the absent timing,
  every-default-password coverage, Assessor assignment, Figure execution,
  branch and failure assignment, procedure or test execution, certification,
  compliance, equivalence, and endorsement.
- `CEPTS3.2-T1-008` through `CEPTS3.2-T1-016` remain nine separate records for
  the per-service flow action, seven decisions, and aggregate result rule. The
  two narrow positive legs do not imply that a service was discovered,
  observed, evaluated, passed, or failed, and they do not contribute to the
  aggregate Test case 1 result.
- The recorded source anomaly is neither expanded nor duplicated and supplies
  no mapping outcome. The public v3.2 source boundary remains distinct from the
  current operational scheme. Original paraphrases and the frozen source-copy
  boundary are preserved.
- The candidate remains forward-only `esaf_to_external` and draft. It makes no
  claim of population coverage, predictive sufficiency, full-population or
  continuous assurance, current-scheme completeness, certification,
  compliance, equivalence, or endorsement.

## Validation evidence

- Focused Plus mapping suite: 12 tests passed in 12.223 seconds.
- Crosswalk validation passed in ordinary and pinned-baseline modes with 2
  mapping sets, 156 provisions, 45 relationships, and 112 negative
  dispositions.
- Whole-range `git diff --check` passed for the reviewed base and candidate.
- Candidate audit confirmed exactly 16 T1 records, 2 mapped records, 14
  negative dispositions, 2 relationship legs, and positive IDs exactly
  T1-011 and T1-013.
- The corrected implementation report records a full repository suite of 307
  passing tests with 3 skipped, control validation of 91 controls and 91
  objectives, link validation of 379 tracked Markdown files, exact commit
  scope, no Python cache artifacts, and a clean candidate worktree.

## Findings

- Critical: none.
- Important: none.
- Minor: none.

## Disposition

Approved. Exact candidate
`98fce9ea0f71285b2198a17e5d4fa373a8c8d689` is approved for Task 4 T1-batch
technical closure from the security and overclaiming perspective. This
approval does not promote the draft snapshot or establish assessment
execution, testing success, certification, compliance, equivalence,
endorsement, current-scheme coverage, full-population assurance, or
continuous assurance.
