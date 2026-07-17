# Cyber Essentials Plus v3.2 `C` specification review

review_date: 2026-07-17
reviewer_id: codex-ce-plus-c-specification-reviewer
reviewer_role: independent specification and task-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 39f9dfa3eafe358929dddd63106be502f924a879
reviewed_base_sha: d77768feee5b75bf3a71a5b503729ffe5baf8119
reviewed_range: d77768feee5b75bf3a71a5b503729ffe5baf8119..39f9dfa3eafe358929dddd63106be502f924a879
specification_verdict: approved
task_quality_verdict: approved
all_negative_determination: approved
conjunctive_boundary_determination: approved
critical_or_important_findings_remain: false

## Independence and authority

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
rights reviewer `esaf-publication-rights-reviewer`, and the separately assigned
C overclaiming reviewer. This review used authorized access to the pinned
public NCSC Cyber Essentials Plus Test Specification v3.2, its locked provision
oracle, and exact normative ESAF `## Requirement` text at immutable baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. Implementation guidance,
assessment procedures, expected-evidence examples, metrics, topic similarity,
and adjacent capabilities were not accepted as positive mapping bases.

## Scope, method, and evidence

This review covered `.superpowers/sdd/task-11-brief.md`,
`.superpowers/sdd/task-11-report.md`, supplied exact diff package
`.superpowers/sdd/review-d77768f..39f9dfa.diff`, the exact Git range bound
above, all thirteen C records, focused test changes, lifecycle registry, both
generated catalogs, locked oracle, and committed ESAF manifest. HEAD was
verified as exact candidate `39f9dfa3eafe358929dddd63106be502f924a879`.

The candidate changes exactly 17 authorized paths: thirteen C records, one
focused test module, one lifecycle registry, and generated
`crosswalks/catalog.json` and `crosswalks/CATALOG.md`. The commit message is
`Map Cyber Essentials Plus decision provisions`. No candidate-authored C
review report is present in the reviewed range.

The oracle SHA-256 was independently verified as
`8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
The committed manifest remains ESAF release `0.4-alpha`, source commit
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, with the pinned 91-control
population. A read-only audit compared all thirteen records in oracle order
for record and provision identifiers, group, kind, actors, approved
original-paraphrase summary, official URL, rendered locator, draft status,
taxonomy, disposition, relationships, mapper provenance, and specific negative
rationale.

Three focused candidate-bound tests were rerun:
`test_completed_batches_match_oracle_and_manifest`,
`test_c_discretionary_exception_preserves_owner_and_conjunction`, and
`test_c_batch_universe_and_counts_are_exact`. All passed in 0.238 seconds. The
exact range also passed `git diff --check`. The implementation report supplies
additional candidate-bound evidence for 29 focused tests, both crosswalk
checks, link validation, and a 324-test full suite with three expected Windows
symlink-capability skips. No broad suite was rerun for this independent review.

## Specification assessment

The candidate implements exactly `CEPTS3.2-C-001` through
`CEPTS3.2-C-013`, adds `C` to `COMPLETED_GROUPS`, and enforces the exact C
universe and counts. Every record uses schema `1.0.0`, requirement
granularity, `draft` status, the required mapping-set ID, paraphrase mode,
approved mapper metadata, and exact oracle-derived structural metadata and
locator. All thirteen records use `no_direct_mapping` and contain no
relationship leg, so the only mapping direction remains `esaf_to_external`.

The records preserve the oracle's actor ownership and provision taxonomy:
Assessor-owned reporting, consultation, aggregate-result, and certificate
actions remain separate from Delivery Partner-owned deferral and exception
decisions. Each negative rationale begins with `Missing outcome:` and names
the precise absent scheme outcome rather than relying on generic subject-matter
difference.

C-001 and C-002 correctly remain negative because ESAF evidence, reporting,
and escalation duties do not require the Assessor to compile this external
assessment report after all prescribed tests or conduct the scheme-specific
Delivery Partner consultation when the appointed-day assessment is
unfinished. C-003 and C-004 correctly remain negative because no ESAF
requirement assigns the Delivery Partner authority to defer these tests or
recommends the external one-month deferral interval.

C-005 and C-012 correctly remain negative because no ESAF requirement directs
the Assessor to calculate or record the named aggregate pass or residual-fail
result across performed external test cases and decision branches. C-006,
C-009, and C-013 correctly remain negative because ESAF does not authorize the
Assessor to award or withhold a Cyber Essentials Plus certificate after the
corresponding aggregate result. C-007 correctly remains negative because ESAF
does not require the Assessor to classify a few external case failures as
minor and then consult the Delivery Partner.

The candidate does not imply external procedure execution, an observed result,
test-population coverage, certification, compliance, equivalence, endorsement,
current-scheme completeness, full-population assurance, or continuous
assurance. No condition is used to manufacture a missing outcome.

## All-negative normative determination

The all-negative disposition is correct. Concretely plausible normative
controls were independently checked, including `AUD-100`, `AUD-120`,
`AUD-130`, `AUD-140`, `CMP-110`, `GOV-140`, `RSK-130`, and `MOD-120`.
Their exact requirements govern internal assessment programs and evidence,
finding treatment, management review, applicable reporting duties, ESAF
exceptions, impact assessment, and model validation. None requires the named
external actor to perform a C provision, supplies an observed external test
result or population conjunction, grants Delivery Partner discretion, fixes
the two exception predicates, assigns an aggregate Cyber Essentials Plus
verdict, or authorizes a certificate action.

In particular, `CMP-110` does not create the C-001 report procedure merely
because it covers reports according to applicable requirements; `AUD-130` and
`GOV-140` do not create the C-003/C-004 or C-008 exception outcomes merely
because they govern findings or ESAF exceptions; and `AUD-100`, `AUD-120`,
and `MOD-120` do not establish performed-test coverage, observations, or
aggregate scheme results. A positive leg to any of these controls would rely
on adjacency or a narrowing condition to supply a missing external outcome.

All-negative determination: **approved**. No missed direct support was found
for reporting, deferral, consultation, aggregate outcome, exception, or
certificate-action records.

## C-008/C-010/C-011 conjunctive boundary

The locked oracle and records preserve a three-record external decision chain.
C-008 assigns the discretionary exceptional overall-pass decision exclusively
to the Delivery Partner. C-010 separately expresses the first predicate:
marginal deviations in less than five percent of performed tests. C-011
separately expresses the second predicate: no evidence of a broader failure in
the Applicant's cybersecurity processes. The C-008 rationale expressly
requires both predicates, and the C-010/C-011 rationales each prohibit waiver
of the other predicate.

All three records retain `actors: ["Delivery Partner"]`,
`no_direct_mapping`, and empty relationships. Their rationales also prohibit
ESAF controls from counting external results, revising an observation,
establishing both predicates, or supplying the overall pass. The wording does
not turn either predicate into an automatic pass rule: even when both external
predicates hold, C-008 remains the Delivery Partner's discretionary decision.
Nor does C-008 revise or waive any underlying observed case failure.

Conjunctive-boundary determination: **approved**. Actor ownership, the precise
under-five-percent predicate, the distinct no-broader-process-failure
predicate, their conjunction, observation integrity, and the separation from
aggregate pass/fail are all preserved.

## Lifecycle, catalogs, provenance, and tests

The lifecycle remains `draft`, its `events` array remains empty, and the
refreshed snapshot digest is
`82710639b09157052392c3eb1ec8e7195a78d9cb420d917146b8dec1d4388057`.
The generated catalogs consistently derive 2 mapping sets, 242 provisions, 49
directional relationships, and 195 negative dispositions. The C batch
contributes exactly 13 provisions, zero mapped dispositions, 13 negative
dispositions, zero relationship legs, and zero distinct referenced controls.

The focused tests enforce full C oracle membership, exact metadata and manifest
provenance, source-copy protection for derivative narrative, exact all-negative
counts, the Delivery Partner owner/conjunction boundary, draft lifecycle with
empty events, and generated catalog totals. The candidate scope and reported
validation evidence are proportionate to the batch.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

No Critical or Important finding remains unresolved.

## Verdicts

Specification verdict: **approved**. Exact candidate
`39f9dfa3eafe358929dddd63106be502f924a879` satisfies the binding Task 11
contract: complete 13-row oracle fidelity, correct all-negative dispositions,
specific missing-outcome rationales, preserved C-008/C-010/C-011 ownership and
conjunction, normative-only mapping judgment, original paraphrases, correct
taxonomy and provenance, draft lifecycle with empty events, and deterministic
catalog derivation.

Task-quality verdict: **approved**. The implementation is tightly scoped,
test-first, and supported by credible candidate-bound evidence. The focused
regressions directly enforce the exact C population and discretionary boundary,
and the complete candidate contains no unrelated or reviewer-authored change.
