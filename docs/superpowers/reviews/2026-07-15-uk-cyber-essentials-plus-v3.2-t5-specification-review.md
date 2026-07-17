# Cyber Essentials Plus v3.2 `T5` specification review

review_date: 2026-07-17
reviewer_id: codex-ce-plus-t5-normative-basis-reviewer
reviewer_role: independent specification, normative-basis, and task-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: f2242473a24e257400ee05224bff8fcecaa7224b
reviewed_base_sha: b3f25025e5f8334ba7a2557db9a8fe6a946cfefb
reviewed_range: b3f25025e5f8334ba7a2557db9a8fe6a946cfefb..f2242473a24e257400ee05224bff8fcecaa7224b
specification_verdict: approved
task_quality_verdict: approved
t5_006_normative_basis_verdict: approved
feasibility_independence_verdict: approved
copy_guard_verdict: approved
prior_important_finding_status: resolved
critical_or_important_findings_remain: false

## Independence and authority

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
rights reviewer `esaf-publication-rights-reviewer`, and the independently
assigned T5 security and overclaiming reviewer. This review used authorized
access to the pinned public NCSC Cyber Essentials Plus Test Specification
v3.2, the locked provision oracle, and exact normative ESAF `## Requirement`
text at immutable baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. Implementation guidance,
assessment procedures, expected-evidence examples, metrics, topic similarity,
and adjacent capabilities were not accepted as positive mapping bases.

## Scope, method, and evidence

This complete re-review covered `.superpowers/sdd/task-10-brief.md`, the
updated `.superpowers/sdd/task-10-report.md`, supplied two-commit package
`.superpowers/sdd/review-b3f2502..f224247.diff`, the exact Git range bound
above, all seven T5 records, focused mapping-test changes, lifecycle registry,
both generated catalogs, locked oracle, committed ESAF manifest, and pinned
IAM-120 and IAM-130 requirements. The feasibility matrix and illustrative
T5-006 plan example were inspected only for independence comparison, not as
normative support. The prior overclaiming report was inspected to verify
resolution of its Important source-copy finding.

HEAD was verified as exact amended candidate
`f2242473a24e257400ee05224bff8fcecaa7224b`. Its range from the required base
contains the original `Map Cyber Essentials Plus administrative-process
tests` commit and the focused `Fix T5 source-copy guard bypass` commit. The
complete candidate still changes exactly 11 authorized paths: seven new T5
records, the focused test, lifecycle registry, and two generated catalogs. The
fix commit changes exactly four paths: the focused test, T5-003 record,
lifecycle registry, and machine catalog. It does not change T5-006 or any
other mapping judgment and does not commit either review report.

The oracle SHA-256 was independently verified as
`8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
The committed manifest remains ESAF release `0.4-alpha`, source commit
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, with 91 controls. A read-only
candidate audit compared all seven records in oracle order for IDs, group,
kind, actors, approved original-paraphrase summary, official URL, and rendered
locator; checked dispositions, relationship provenance, lifecycle, and
catalog state; and passed at seven records, one mapped disposition, six
negatives, two legs, and repository totals 229/49/182.

Two focused tests were rerun at the amended SHA:
`test_source_copy_guard_rejects_t5_003_derivative_window` and
`test_completed_batches_match_oracle_and_manifest`. Both passed in 0.202
seconds. The implementation report additionally supplies candidate-bound
evidence for 27 focused tests, both crosswalk checks, link validation,
exact-range checks, and a 322-test full suite with three expected skips. No
broad suite was rerun for this review.

## Specification assessment

The candidate implements exactly `CEPTS3.2-T5-001` through
`CEPTS3.2-T5-007`, adds `T5` to `COMPLETED_GROUPS`, and enforces the exact T5
universe and counts. Each record uses schema `1.0.0`, requirement granularity,
`draft` status, the required mapping-set ID, paraphrase mode, approved mapper
metadata, and exact oracle-derived metadata and locator.

T5-001 through T5-005 and T5-007 correctly use `no_direct_mapping`. Their
specific `Missing outcome:` rationales preserve external population and test
execution, the signed-in standard-account exercise, complete sampled-device
coverage, the observed operating-system-specific attempt, sample-wide
repetition, and complete sub-test/population aggregation. Exact ESAF
requirements do not supply those Assessor procedures or result mechanics.

T5-003 retains exact locked oracle binding, including the four-word approved
summary `Test every sampled device.` Its revised rationale remains specific:
ESAF does not require the Assessor to execute the external assessment
throughout the selected device sample and does not define or complete that
assessment population. It no longer reproduces the protected five-word source
window that triggered the prior finding.

T5-006 correctly remains `mapped` with two and only two separately justified
legs. Both use direction `esaf_to_external`, relationship
`partially_supports`, `narrow` coverage, and `high` confidence. High confidence
describes confidence in each bounded analytical claim, not implementation
effectiveness or completion of the external provision. No reverse leg,
equivalence, compliance, procedure execution, or result assertion appears.

## Separate T5-006 normative determinations

### IAM-120

The IAM-120 leg remains justified. Its exact pinned requirement mandates
authorization of AI assets and actions according to approved purpose, role,
attributes, context, and least privilege, explicitly including limits on
administration. Under the stated condition that the process is an IAM-120 AI
action and the ordinary-user role is not approved, that text directly
contributes only the restriction predicate in T5-006.

`partially_supports` and `narrow` remain correct because IAM-120 does not
define ordinary credentials, require a separate authentication request,
select or launch the external process, establish device or population scope,
observe an attempt or result, or assign a sub-test or aggregate verdict. The
record states these gaps and prohibited inferences. No stronger relationship
or additional IAM-120 leg is warranted.

### IAM-130

The IAM-130 leg remains independently justified. Its exact pinned requirement
mandates restriction and separate authentication of privileged access capable
of changing enumerated AI models, data, instructions, controls, tools,
configuration, logs, or authorization policy. Under the stated condition that
the process uses such privileged access, that text directly contributes the
restriction and abstract separate-authentication predicates.

`partially_supports` and `narrow` remain correct because IAM-130 does not
define ordinary-user credentials, prescribe the exact additional login prompt
an Assessor must see, execute the external process on a device, establish
tested-population coverage or observation, or assign the sub-test or aggregate
verdict. The record preserves every such gap. The IAM-130 leg neither depends
on nor combines with IAM-120 to manufacture a missing outcome.

The two legs correctly remain separate. Their T5-006 record is byte-identical
between the original and amended candidates, confirmed by identical Git blob
`b3add5d458eae6c2f1d2ece3410295c1eca694bf`. IAM-110's exact requirement
only requires risk-proportionate authentication before access to non-public AI
assets; it does not add direct support for separate-login or ordinary-
credential-rejection predicates. No other plausible pinned requirement
supplies an omitted direct T5-006 leg.

## Feasibility-independence assessment

The T5-006 analysis remains independently sourced for final-schema purposes.
Its two legs have separate requirement-specific rationales, conditions,
expected evidence, known gaps, and prohibited inferences grounded in the
pinned IAM-120 and IAM-130 requirements. The prose is not copied from the
feasibility probe's combined analysis or the plan's illustrative example, and
the record contains none of the feasibility metadata markers.

The focused independence regression requires both normative bases,
requirement-specific markers, the named gap set, and absence of feasibility
markers. A test cannot prove mental independence alone, but direct comparison
of the exact requirements, feasibility text, and final record confirms it.

## Copy-guard fix and regression

The prior Important finding is resolved. The superseded candidate incorrectly
treated `test on every sampled device` as an unavoidable exact-oracle-summary
collision even though the locked summary has only four words. The five-word
window occurred in derivative T5-003 rationale, and the global digest skip
could exempt the same protected source window in any narrative field.

The amended candidate removes `PERMITTED_ORACLE_SUMMARY_WINDOW_DIGESTS` and
the corresponding `if digest in ...: continue` path completely. Candidate-
bound search confirms the targeted exception code is absent. T5-003's
derivative rationale is rephrased while its exact approved four-word oracle
summary and specific missing-outcome analysis remain intact. No oracle field
or protected-source fixture was weakened.

The new regression is meaningful. It supplies precisely the protected digest,
places the formerly exempted five-word window inside surrounded derivative
prose, and requires `assert_no_copied_source_windows` to raise. The reported
RED failed with `AssertionError not raised` on the vulnerable implementation,
demonstrating that the global skip caused the bypass. After removal, the test
passes, and the completed-batch guard also passes on all candidate narratives.
This directly exercises the defect rather than merely searching for a constant
or asserting the revised T5-003 text.

Copy-guard verdict: **approved**. No exception is needed or retained, and the
prior Important finding has no residual bypass or replacement defect.

## Lifecycle, catalog, provenance, and tests

The lifecycle remains `draft`, its `events` array remains empty, and the
refreshed snapshot digest is
`25d0adac7d3e2fe8058681783b53a7372957dd38652383654253f46ad9081039`.
Generated catalogs consistently derive 2 mapping sets, 229 provisions, 49
directional relationships, and 182 negative dispositions. T5 contributes
exactly seven provisions, two relationship legs, two distinct referenced
controls, and six negative dispositions.

The focused tests enforce complete T5 oracle membership and metadata,
manifest provenance, fail-closed source-copy protection including the T5-003
regression, exact T5 disposition and leg counts, independent T5-006 normative
markers and gaps, draft lifecycle, catalog freshness, and paired closure
reports with authorized and pairwise-distinct identities. Candidate scope and
validation evidence are proportionate to the batch.

Across the records, no condition creates a missing external outcome and no
text implies procedure execution, observed result, device or population
coverage, certification, compliance, equivalence, endorsement, current-scheme
completeness, full-population assurance, or continuous assurance.

## Findings by severity

- Critical: none.
- Important: none. The prior source-copy-guard bypass finding is resolved in
  `f2242473a24e257400ee05224bff8fcecaa7224b`.
- Minor: none.

No Critical or Important finding remains unresolved.

## Verdicts

Specification verdict: **approved**. Exact amended candidate
`f2242473a24e257400ee05224bff8fcecaa7224b` satisfies the binding Task 10
contract: exact seven-row oracle fidelity, six correct negative dispositions,
two independently justified and separately bounded T5-006 legs, normative-
only support, correct taxonomy and provenance, original paraphrases,
fail-closed copy protection, draft lifecycle with empty events, and
deterministic catalog derivation.

Task-quality verdict: **approved**. The implementation is tightly scoped,
test-first, and supported by credible amended-candidate evidence. The focused
fix removes the bypass rather than broadening an exception, includes a true
RED/GREEN regression for the defect, preserves T5-003 oracle fidelity and
missing-outcome specificity, and leaves all T5-006 judgments unchanged.
