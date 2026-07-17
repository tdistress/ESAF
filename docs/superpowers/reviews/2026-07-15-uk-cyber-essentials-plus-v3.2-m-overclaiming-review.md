# Cyber Essentials Plus v3.2 M-Batch Security and Overclaiming Review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-m-overclaiming-reviewer
authorized_source_access: true
reviewed_candidate_sha: 6eb6691d19c81807f3d1f917fdf225a49096b3b6
reviewed_base_sha: 1ca339c03b24264b03cad0e9debae23c84450d59
review_disposition: approved

## Scope and independence

This independent review covers the exact candidate range
`1ca339c03b24264b03cad0e9debae23c84450d59..6eb6691d19c81807f3d1f917fdf225a49096b3b6`
for the 24 `CEPTS3.2-M-001` through `CEPTS3.2-M-024` methodology
records, their derived lifecycle and catalogs, and the focused regression
contract. The reviewer is distinct from the mapper, the mapping-rights
reviewer, and the independent specification reviewer.

The review used the authorized pinned official NCSC Cyber Essentials Plus
Test Specification v3.2 source, the locked provision oracle, the committed
91-control ESAF manifest, and exact `## Requirement` text from ESAF baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. It also examined the approved
design and implementation plan, the Task 3 brief and implementation report,
and the complete candidate diff
`.superpowers/sdd/review-1ca339c..6eb6691.diff`.

## Security and overclaiming assessment

- All 24 external outcomes were reviewed provision-first. The 22
  `no_direct_mapping` records identify specific missing methodology,
  prerequisite, procedure, decision, or recommendation outcomes. No negative
  disposition overlooks direct normative ESAF support, and no condition,
  implementation guidance, similarity, or adjacent control supplies a missing
  outcome.
- `CEPTS3.2-M-010 -> AUD-130` is a justified
  `partially_supports`, `narrow`, high-confidence leg. AUD-130 directly
  mandates remediation and closure of AI assessment findings. Its condition
  only limits the leg to a preliminary issue already governed as such a
  finding. The gaps and prohibited inferences preserve the absent
  every-issue requirement, pre-test deadline, Assessor assignment, procedure
  execution and results, testing completion, certification, compliance,
  equivalence, and endorsement.
- `CEPTS3.2-M-011 -> AUD-120` is a justified
  `partially_supports`, `narrow`, high-confidence leg. AUD-120 directly
  mandates obtaining and retaining evidence sufficient for each AI assessment
  procedure. Its condition limits applicability to relevant artifacts in an
  ESAF-governed AI assessment. The gaps and prohibited inference preserve the
  absent Certifying Body assignment, complete Plus-artifact population,
  certificate-lifetime duration, verification execution, and certification
  outcome.
- Both legs remain forward-only `esaf_to_external`. Neither leg nor the
  batch implies reverse coverage, procedure execution, observed results,
  population or sample testing, full-population assurance, assessment
  sufficiency, certification, compliance, equivalence, endorsement,
  current-scheme coverage, or continuous assurance.
- Source-version separation and the closed IASME partition remain intact.
  Records use independently written paraphrases and derivative analysis; the
  frozen copied-source guard passes.
- All records and lifecycle metadata remain `draft`, with no reviewer or
  approver identity added to authoritative provision records and no lifecycle
  promotion inferred from this technical review.

The prior Important finding against the original M-010 negative disposition
was resolved in correction commit
`6eb6691d19c81807f3d1f917fdf225a49096b3b6`. This report reviews that new
exact candidate; it does not carry forward approval from the superseded SHA.

## Validation evidence

- Focused Plus mapping suite: 9 tests passed.
- Crosswalk validation: passed in ordinary and pinned-baseline modes; derived
  totals are 2 mapping sets, 140 provisions, 43 relationships, and 98 negative
  dispositions.
- Link validation: 361 tracked Markdown files passed.
- Whole-range `git diff --check`: passed.
- The implementation report records a corrected-candidate full suite of 304
  passing tests with 3 skipped.

## Findings

- Critical: none.
- Important: none.
- Minor: none.

## Disposition

The exact candidate
`6eb6691d19c81807f3d1f917fdf225a49096b3b6` is approved for M-batch technical
closure from the security and overclaiming perspective. This approval does
not promote the draft snapshot, establish Cyber Essentials Plus assessment or
certification, or authorize any compliance, equivalence, endorsement,
current-scheme coverage, full-population, or continuous-assurance claim.
