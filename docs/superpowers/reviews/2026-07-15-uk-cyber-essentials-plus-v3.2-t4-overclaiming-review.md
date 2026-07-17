# Cyber Essentials Plus v3.2 T4 Security and Overclaiming Review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t4-overclaiming-reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: ce5a88e94a6a505a2f27c25a4967e57db4860cf2
reviewed_base_sha: 6458359e7b9fdc10bd57b695c220a1d24d816cf2
review_disposition: approved

## Scope and independence

This independent security and overclaiming review covers the exact candidate
range
`6458359e7b9fdc10bd57b695c220a1d24d816cf2..ce5a88e94a6a505a2f27c25a4967e57db4860cf2`
for `CEPTS3.2-T4-001` through `CEPTS3.2-T4-009`. It reviews source and
version boundaries, actor separation, procedure and result separation,
population and repetition boundaries, negative-outcome specificity,
copied-source protection, internal consistency, and the correctness of all
nine `no_direct_mapping` dispositions.

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
mapping-rights reviewer `esaf-publication-rights-reviewer`, and the separately
assigned T4 specification reviewer. The review used authorized access within
the approved public-source boundary and did not modify the candidate, index,
HEAD, or any artifact other than this designated report.

## Method and evidence

- Verified HEAD as exact candidate
  `ce5a88e94a6a505a2f27c25a4967e57db4860cf2` before analysis and reviewed the
  complete supplied diff package `.superpowers/sdd/review-6458359..ce5a88e.diff`,
  not a later working-tree diff.
- Reviewed `.superpowers/sdd/task-9-brief.md`, the implementation evidence in
  `.superpowers/sdd/task-9-report.md`, all nine T4 records, the mapping-set
  source and rights metadata, lifecycle change, generated catalog effects,
  and focused regression changes.
- Reconciled every record against the locked nine-row T4 oracle. The locally
  verified oracle SHA-256 is
  `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
  The source remains the public NCSC Cyber Essentials Plus Test Specification
  v3.2, not a later operational scheme or an IASME-derived structure.
- Inspected exact normative `## Requirement` text from immutable ESAF baseline
  `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, including `IAM-110`, `IAM-120`,
  `IAM-130`, `ARC-140`, and `AUD-120`. Concrete alternatives considered
  included `IAM-100`, `IAM-140`, `IAM-150`, `ARC-110`, and `AUD-100` through
  `AUD-140`. None supplies a narrower direct mapping omitted by the candidate.
- Relied on the fixed-candidate validation evidence in the implementation
  report as directed: 23 focused tests passed; ordinary and pinned-baseline
  crosswalk validation reported 222 provisions, 47 relationships, and 176
  negative dispositions; link validation passed; whole-range `git diff
  --check` passed; and the full suite passed 318 tests with 3 expected skips.
  No broad suite was rerun for this review.

## Security and overclaiming assessment

- All nine records correctly use the forward-only `esaf_to_external`
  direction, `no_direct_mapping`, and zero relationship legs. Each negative
  begins with `Missing outcome:` and identifies the absent external procedure,
  population, repetition, observation, fallback method, individual result, or
  aggregate result rather than relying on a generic scope mismatch.
- T4-001 through T4-004 set external Assessor procedure, role-population, and
  repetition boundaries. Authentication, authorization, administrative-path,
  cloud-responsibility, and assessment-program requirements do not require an
  Assessor to perform Test case 4 across every cloud service, direct sampled
  users to use organization-issued accounts, cover both ordinary and
  administrator roles for every service, or deduplicate execution by distinct
  authentication service.
- T4-005 through T4-007 prescribe Assessor observation, a fallback
  private-browser method on an Assessor device, and repetition across every
  authentication service. No ESAF implementation, evidence, or assessment
  requirement assigns these actions or proves that they occurred. The
  recommendation in T4-006 also remains correctly negative because no ESAF
  normative requirement recommends that specific fallback method.
- `AUD-100`, `AUD-110`, and `AUD-120` establish an AI assessment program,
  competent and independent personnel, and sufficient evidence. They do not
  incorporate this external procedure, define its cloud-service population,
  require its test accounts or authentication attempts, or create its result
  rules. `AUD-130` governs findings after an assessment and likewise cannot
  manufacture execution or a pass/fail outcome.
- The records use only approved oracle metadata and original paraphrases.
  They do not copy source requirement or passage text, recreate prohibited
  IASME-derived structure, or expand beyond the locked public-v3.2 oracle.
  The implementation evidence records passing source-copy guard and exact
  oracle-fidelity assertions.
- No record or rationale implies execution, observed results, coverage,
  pass/fail satisfaction, certification, compliance, equivalence,
  endorsement, current-scheme completeness, full-population assurance, or
  continuous assurance. Draft snapshot status and empty lifecycle events are
  preserved.

## T4-008 MFA-observation determination

T4-008 correctly remains `no_direct_mapping`. Its external outcome combines
an Assessor-observed authentication event, a prescribed MFA form before user
or administrator cloud access, and an Assessor-issued pass/fail verdict.
`IAM-110` normatively requires risk-proportionate authentication before access
to non-public AI assets, but it does not require MFA in every covered case, the
specified observed prompt form, the T4 ordinary-user and administrator cloud
population, or this external verdict. MFA appears only in IAM-110
implementation guidance for privileged or high-impact human access and cannot
support a positive leg.

`IAM-130` requires separate authentication for privileged access capable of
changing enumerated AI assets. It neither requires MFA nor reaches every
administrator access path or ordinary-user cloud access. `IAM-120` governs
authorization after authentication and supplies no MFA outcome. Combining or
conditioning these adjacent duties would still manufacture the missing form,
population, observation, and result mechanics. The record's negative
rationale identifies those missing outcomes without denying the narrower ESAF
authentication duties.

## T4-009 aggregation determination

T4-009 correctly remains `no_direct_mapping`. It requires the Assessor to
derive the complete Test case 4 result from every sub-test result. ESAF
authentication, privileged-access, assessment-program, evidence, and findings
requirements do not define those sub-tests, require their execution or
results, or establish this all-sub-tests-pass aggregation chain. Adjacent
control duties cannot be composed into the scheme-specific decision rule.

## Actor-boundary determination

Every T4 record preserves `actors: ["Assessor"]` exactly as locked by the
oracle. The summaries and rationales do not transfer the Assessor's direction,
execution, observation, population selection, repetition, or verdict duties
to the implementing organization. Conversely, the records do not misstate
organization-scoped ESAF implementation controls as proof of Assessor action
or observed outcomes. Actor separation is therefore sound across all nine
records.

## Findings

- Critical: none.
- Important: none.
- Minor: none.

No Critical or Important findings remain unresolved.

## Overclaiming verdict and disposition

Approved. Exact candidate
`ce5a88e94a6a505a2f27c25a4967e57db4860cf2` is approved for Task 9 T4-batch
technical closure from the security and overclaiming perspective. The
all-negative disposition is conservative and correct against the exact pinned
ESAF requirements and concrete alternatives reviewed. This approval does not
promote the draft snapshot or establish procedure execution, observed MFA,
population or repetition coverage, an individual or aggregate pass,
certification, compliance, equivalence, endorsement, current-scheme coverage,
full-population assurance, or continuous assurance.
