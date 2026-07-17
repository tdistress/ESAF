# Cyber Essentials Plus v3.2 `T3-020` through `T3-037` specification review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t3-020-037-specification-reviewer
reviewer_role: independent specification and task-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: fa3c8c8bef60b0f779849797f348701e900a22fd
reviewed_base_sha: e35ae8f49172139890aea83224a5cec1f16a0616
reviewed_range: e35ae8f49172139890aea83224a5cec1f16a0616..fa3c8c8bef60b0f779849797f348701e900a22fd
specification_verdict: approved
task_quality_verdict: approved_with_minor_evidence_finding
full_t3_consistency_verdict: approved
critical_or_important_findings_remain: false

## Independence and authority

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
rights reviewer `esaf-publication-rights-reviewer`, and independently assigned
overclaiming reviewer `codex-ce-plus-t3-020-037-overclaiming-reviewer`. This
review used authorized access to the pinned public NCSC Cyber Essentials Plus
Test Specification v3.2, the locked 144-row provision oracle, and exact
normative ESAF `## Requirement` text at immutable baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. Implementation guidance,
assessment procedures, evidence examples, topic similarity, and adjacency
were not accepted as positive mapping bases.

## Scope, method, and evidence

The review covered `.superpowers/sdd/task-8-brief.md`,
`.superpowers/sdd/task-8-report.md`, the supplied package
`.superpowers/sdd/review-e35ae8f..fa3c8c8.diff`, and the exact Git range bound
above. HEAD was verified as exact candidate
`fa3c8c8bef60b0f779849797f348701e900a22fd`, whose sole parent is the required
base and whose commit subject is `Complete Cyber Essentials Plus configuration
mapping`. The package header binds the same range, and its embedded diff
matches the exact Git range using ten context lines.

The candidate contains exactly 22 authorized paths: 18 new records
`cepts32-t3-020.md` through `cepts32-t3-037.md`, the focused Plus mapping test,
the Plus lifecycle registry, and the JSON and Markdown catalogs. It does not
modify `T3-001` through `T3-019`, the locked oracle, committed ESAF manifest,
inventory, schema, validators, rights artifacts, or other publication content,
and it does not create either Task 8 review report.

The oracle SHA-256 was independently verified as
`8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
The committed manifest remains ESAF release `0.4-alpha`, source commit
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, with 91 controls. All 18 new
records were compared in oracle order for record and external IDs, group,
kind, actors, original-paraphrase summary, canonical official URL, and
rendered dual-coordinate locator; no mismatch was found. All 37 T3 records
were then inspected together for cross-half contradictions and templated
rationales. The implementer supplied per-record RED/GREEN evidence, a passing
21-test focused suite, a passing 316-test full suite with 3 skipped, ordinary
and pinned-baseline crosswalk validation, link validation, and clean diff
checks. No broad suite was rerun for this task-scoped review.

## Specification assessment

The candidate implements exactly `CEPTS3.2-T3-020` through
`CEPTS3.2-T3-037`. It removes `COMPLETED_T3_IDS`, adds `T3` to
`COMPLETED_GROUPS`, and makes the shared fidelity assertion require all 37
oracle-defined T3 paths. The focused batch test fixes the new range at zero
mapped records, zero relationship legs, and 18 `no_direct_mapping` records.

Every new record uses schema version `1.0.0`, requirement granularity,
`draft` status, the required mapping-set ID, paraphrase mode, the authorized
mapper identity and date, exact oracle-derived metadata and locator, and an
empty relationship array. Every negative rationale begins `Missing outcome:`
and specifically preserves the absent applicability population, Assessor
procedure, product-specific check, observed device outcome, coverage rule,
decision branch, or aggregate verdict. The candidate does not infer a
procedure from a control, use a condition to create a missing outcome, or
promote implementation guidance and adjacent capabilities into normative
support.

The all-negative result is correct. In particular, exact pinned requirements
for `INF-110`, `INF-120`, `INF-140`, `APP-140`, `MON-100`, `AUD-100`, and
`AUD-120` do not require the T3-027 through T3-035 external outcomes. They do
not assign an Assessor to confirm anti-malware operation from logs, verify
vendor-specific anti-malware update configuration, issue the conjunctive
manual-check verdict, execute certificate-allowlisting checks across every
sampled device, compare roots with an operating-system manufacturer's set,
verify Applicant agreement per additional root, observe unsigned or
untrusted-chain executable blocking, or verify every-format operating-system
code-signing policy. Exact controls for telemetry, evidence, baselines,
vulnerability treatment, cryptographic protection, and secure development
are adjacent but do not supply those actor, object, procedure, population,
observation, coverage, or verdict outcomes.

No new record implies procedure execution, an observed result, population
coverage, pass/fail status, certification, compliance, equivalence,
endorsement, current-scheme completeness, full-population assurance, or
continuous assurance.

## Full-T3 consistency result

The complete 37-record T3 group is internally consistent. Applicability rows
`T3-001`, `T3-004`, `T3-007`, `T3-018`, `T3-026`, and `T3-030` consistently
decline to convert ESAF scope, sampling, hardening, or cryptographic duties
into external assessment populations. Email failure rules `T3-015` and
`T3-016` receive the same negative treatment as parallel browser failure rules
`T3-024` and `T3-025`. Aggregate rules `T3-017`, `T3-029`, `T3-036`, and
`T3-037` consistently remain negative. Recommendation `T3-019` remains
negative and is not promoted into a mandatory ESAF outcome. The rationales
share a controlled form but are provision-specific rather than templated in a
way that obscures different missing outcomes.

`T3-014 -> AUD-120` remains the sole justified positive T3 relationship. The
exact normative AUD-120 duty to obtain and retain attributable,
integrity-protected evidence sufficient to support each AI assessment
procedure and determination directly contributes to recording an attempted
attachment-opening outcome when that attempt is an ESAF-governed assessment
procedure and its outcome is necessary evidence. Its condition narrows the
existing evidence duty; it does not create the attempt, procedure, Assessor
assignment, observed result, or per-attachment coverage. T3-027 instead
requires a particular evidence source and product-specific confirmation, and
T3-029 requires a scheme-specific aggregate verdict, so their negative
dispositions do not contradict T3-014.

## Lifecycle, catalog, provenance, and tests

The lifecycle remains `draft`, its `events` array remains empty, and its
snapshot digest is
`9aad4168d67369e067e71737119b0081c6afbafb40ced9161128b9e2019b3266`.
The generated catalogs consistently derive a 97-record Plus snapshot and
repository totals of 2 mapping sets, 213 provisions, 47 forward-only
relationships, and 167 negative dispositions. Complete T3 totals are 37
records, one relationship leg (`T3-014 -> AUD-120`), and 36 negatives.

The focused tests enforce exact full-group path equality, oracle and manifest
fidelity, original-paraphrase source-copy protection, draft provenance, exact
batch disposition counts, lifecycle and catalog totals, and paired closure
reports with authorized and pairwise-distinct mapper, rights, specification,
and overclaiming reviewer identities. Removing the temporary range constant
and adding T3 to the completed-group tuple correctly replaces the Task 7
exception with full-group completeness.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: `.superpowers/sdd/task-8-report.md` says link validation covered 426
  tracked Markdown files. Exact base `e35ae8f49172139890aea83224a5cec1f16a0616`
  contains 426 tracked Markdown files, while candidate
  `fa3c8c8bef60b0f779849797f348701e900a22fd` contains 444 after the 18 new T3
  records. The reported link gate passed, so this is stale result-count
  evidence rather than a candidate content or validator defect.

No Critical or Important finding remains unresolved.

## Verdicts

Specification verdict: **approved**. Exact candidate
`fa3c8c8bef60b0f779849797f348701e900a22fd` satisfies the binding Task 8
contract: exact 18-row oracle fidelity, complete T3 group enforcement,
normative-only disposition analysis, 18 provision-specific negative
dispositions, no new relationship leg, draft lifecycle and empty events,
correct provenance, and deterministic catalog derivation. The required
full-T3 consistency review is also approved; no cross-half contradiction or
defective templated rationale was found, and T3-014 remains the sole justified
positive.

Task-quality verdict: **approved with one Minor evidence finding**. The
implementation is focused, test-first, full-group complete, and supported by
credible candidate-bound validation evidence. The stale link-validation file
count should be corrected if the implementation report is next maintained,
but it requires no candidate content change before the report-only closure
commit.
