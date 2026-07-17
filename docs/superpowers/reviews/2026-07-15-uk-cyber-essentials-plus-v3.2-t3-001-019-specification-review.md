# Cyber Essentials Plus v3.2 `T3-001` through `T3-019` specification review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t3-001-019-specification-reviewer
reviewer_role: independent specification and task-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 7f3f48f5c1a289bcfda0c6849963784ac529a858
reviewed_base_sha: 3c79aad3fe9d437f725f2134cda51665f16cfe93
reviewed_range: 3c79aad3fe9d437f725f2134cda51665f16cfe93..7f3f48f5c1a289bcfda0c6849963784ac529a858
specification_verdict: approved
task_quality_verdict: approved_with_minor_evidence_finding
critical_or_important_findings_remain: false

## Independence and authority

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
the mapping-rights reviewer, and the independently assigned security and
overclaiming reviewer. This review used authorized access to the pinned
official NCSC Cyber Essentials Plus Test Specification v3.2, the locked
144-row provision oracle, and exact normative ESAF `## Requirement` text at
immutable baseline `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`.
Implementation guidance, assessment procedures, topic similarity, and subject
adjacency were not accepted as positive mapping bases.

## Scope, method, and evidence

The review covered `.superpowers/sdd/task-7-brief.md`,
`.superpowers/sdd/task-7-report.md`, the supplied exact diff package
`.superpowers/sdd/review-3c79aad..7f3f48f.diff`, and the exact Git range bound
above. HEAD was verified as candidate
`7f3f48f5c1a289bcfda0c6849963784ac529a858`, whose sole parent is the required
base and whose commit subject is `Map first Cyber Essentials Plus configuration
batch`.

The candidate range contains exactly 23 authorized paths: the focused Plus
mapping test, 19 new records `cepts32-t3-001.md` through
`cepts32-t3-019.md`, the Plus lifecycle registry, and the JSON and Markdown
catalogs. It does not modify the locked oracle, committed ESAF manifest,
inventory, schema, validators, prior records, rights artifacts, or other
publication content, and it does not create either batch review report.

Oracle SHA-256 was independently verified as
`8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
All 19 records were compared in oracle order for record and external IDs,
group, kind, actors, summary, official URL, and rendered dual-coordinate
locator. A fresh read-only execution of the single completed-batch fidelity
test passed on the exact candidate. The implementer supplied per-provision
RED/GREEN evidence, the exact batch-gate result, a passing 314-test full suite,
pinned and ordinary crosswalk validation, link validation, and clean diff
evidence; broad suites were not rerun for this review.

## Specification assessment

The candidate implements exactly the first immutable T3 range, IDs
`CEPTS3.2-T3-001` through `CEPTS3.2-T3-019`. `COMPLETED_GROUPS` still excludes
T3, while `COMPLETED_T3_IDS` enumerates only 001 through 019 and feeds the
shared exact-set assertion. Thus the range is complete without marking T3's
37-row group complete or admitting later T3 rows. The helper now requires
exact path equality, preventing both missing and premature records.

Each record uses schema version `1.0.0`, requirement granularity, `draft`
status, the required mapping-set ID, original paraphrase mode, the authorized
mapper identity and date, and approved oracle-derived metadata and locator.
No source passage or requirement text is copied into a record. The exact
batch disposition is one mapped record with one relationship leg and 18
`no_direct_mapping` records. Every negative rationale begins with a specific
`Missing outcome:` and separately preserves the absent applicability,
selection, procedure, observation, population, result-rule, or recommendation
outcome. It does not promote configuration recommendations, implementation
guidance, or neighboring ESAF capabilities into direct support.

## Independent scrutiny of `T3-014 -> AUD-120`

The sole positive relationship is justified and is not merely subject
adjacency. The pinned normative AUD-120 requirement states that the
organization shall obtain and retain relevant, reliable, complete, timely,
attributable, integrity-protected evidence sufficient to support each AI
assessment procedure and determination. That mandatory obtain-and-retain duty
directly contributes to the external outcome of recording an attempted
attachment-opening outcome when the attempt is an ESAF-governed AI assessment
procedure and its outcome is necessary evidence for the determination.

The condition narrows the class of attempts to which the already-existing
AUD-120 evidence duty applies; it does not create the attachment-opening
attempt, the external assessment procedure, or an observed result. Therefore
`partially_supports`, `narrow`, and high confidence are appropriate. The exact
control version `0.1.0`, path `AUD/AUD-120.md`, record SHA-256
`f6aa7dda8b73ee22586eb9728e59d5ec19f357a5c10187cd6c6a1d2c28f34ac0`,
and requirement locator match the pinned 91-control manifest.

The rationale, condition, evidence, gaps, and prohibited-inference fields
preserve what AUD-120 does not provide: Assessor assignment, the Cyber
Essentials Plus attachment-opening procedure, a record for every selected
attachment type, procedure execution, an observed opening or blocking result,
complete test-population coverage, testing success, certification, compliance,
equivalence, or endorsement. No record implies current-scheme completeness,
full-population assurance, or continuous assurance.

## Lifecycle, catalog, provenance, and tests

The lifecycle registry remains `draft`, its `events` array remains empty, and
its refreshed snapshot digest is
`a653931bdf379a8f8617a0cc4f0a62d9e6874125188022e2e461ea3bbcfc45ca`.
The generated catalogs consistently derive a 79-record Plus snapshot and
repository totals of 2 mapping sets, 195 provisions, 47 forward-only
relationships, and 149 negative dispositions. The T3 rows appear in oracle
order with T3-014 as the sole mapped row.

The focused tests lock the 001-019 range, exact completed-record equality,
oracle and manifest fidelity, draft provenance, original-paraphrase copy
guard, the exact positive set, one relationship, 18 negatives, lifecycle
digest, generated counts, and paired-report closure behavior. The closure test
allows neither report or both reports, rejects a one-report state, requires
authorized-source declarations, and enforces distinct mapper, rights,
specification-reviewer, and overclaiming-reviewer identities.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: `.superpowers/sdd/task-7-report.md` says link validation covered 405
  tracked Markdown files. The exact base contains 405 tracked Markdown files,
  while candidate `7f3f48f5c1a289bcfda0c6849963784ac529a858` contains 424 after the 19 new
  T3 records. The reported link gate passed, so this is stale result-count
  evidence rather than a candidate content or validator defect.

No Critical or Important finding remains unresolved.

## Verdicts

Specification verdict: **approved**. Exact candidate
`7f3f48f5c1a289bcfda0c6849963784ac529a858` satisfies the binding Task 7
contract for the first immutable T3 half: exact 001-019 oracle fidelity,
normative-only relationship analysis, one justified narrow AUD-120 leg, 18
provision-specific negative dispositions, forward-only direction, draft
lifecycle state, empty events, correct provenance, and deterministic catalog
derivation without marking T3 complete.

Task-quality verdict: **approved with one Minor evidence finding**. The
implementation is focused, test-first, range-complete, and supported by
credible candidate-bound validation evidence. The stale link-validation file
count should be corrected when the implementation report is next maintained,
but it requires no candidate content change before the report-only closure
commit.
