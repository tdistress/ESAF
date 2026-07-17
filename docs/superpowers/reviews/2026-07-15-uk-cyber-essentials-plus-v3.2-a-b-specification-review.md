# Cyber Essentials Plus v3.2 `A/B` specification review

review_date: 2026-07-17
reviewer_id: codex-ce-plus-ab-specification-reviewer
reviewer_role: independent specification and task-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: e88e7756d78fa6bc7c94bb7ba8aa6be96e976ca6
reviewed_base_sha: d98581d2a9f8b411f3ad698838f237a082fe20f0
reviewed_range: d98581d2a9f8b411f3ad698838f237a082fe20f0..e88e7756d78fa6bc7c94bb7ba8aa6be96e976ca6
specification_verdict: approved
task_quality_verdict: approved
all_negative_determination: approved
a_authorization_execution_boundary: approved
b_assessment_file_boundary: approved
critical_or_important_findings_remain: false

## Independence and authority

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
rights reviewer `esaf-publication-rights-reviewer`, and A/B overclaiming
reviewer `codex-ce-plus-ab-overclaiming-reviewer`. This review used authorized
access to the pinned public NCSC Cyber Essentials Plus Test Specification
v3.2, its locked provision oracle, and exact normative ESAF `## Requirement`
text at immutable baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. Implementation guidance,
assessment procedures, evidence examples, metrics, topic similarity, and
adjacent capabilities were not accepted as positive mapping bases.

## Scope, method, and evidence

This review covered `.superpowers/sdd/task-12-brief.md`,
`.superpowers/sdd/task-12-report.md`, supplied exact diff package
`.superpowers/sdd/review-d98581d..e88e775.diff`, the complete Git range bound
above, all eighteen A/B records, focused test changes, lifecycle registry,
both generated catalogs, locked oracle, rights boundary, and committed ESAF
manifest. HEAD and the reviewed commit object were independently verified as
exact candidate `e88e7756d78fa6bc7c94bb7ba8aa6be96e976ca6`, with sole parent the
required base and exact commit message `Complete Cyber Essentials Plus
appendix mapping`.

The candidate changes exactly 22 authorized paths: eighteen new A/B records,
one focused test module, one lifecycle registry, and generated
`crosswalks/catalog.json` and `crosswalks/CATALOG.md`. No review report is in
the candidate range. The implementation report is ignored and outside the
candidate.

The oracle SHA-256 was independently verified as
`8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
A separate read-only comparison found zero binding differences across all 18
records for record ID, external provision ID, group, kind, actors, approved
original-paraphrase summary, official URL, rendered locator, schema,
mapping-set ID, status, granularity, paraphrase mode, disposition,
relationships, mapper provenance, source-access attestation, derivative body,
and `Missing outcome:` rationale form.

The complete focused module was rerun with bytecode generation disabled: all
32 tests passed in 13.360 seconds. The exact candidate also passed
`python tools/validate_crosswalks.py --check --baseline-ref
b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, deriving 2 mapping sets, 260
provisions, 49 relationships, and 213 negative dispositions. The exact range
passed `git diff --check`. The implementation report supplies additional
candidate-bound evidence for the per-provision RED/GREEN micro-cycles, link
validation, both crosswalk checks, and a 327-test full suite with three
expected Windows symlink-capability skips; no broad suite was rerun for this
independent review.

## Oracle fidelity and final snapshot completion

The candidate implements exactly `CEPTS3.2-A-001` through
`CEPTS3.2-A-004` and `CEPTS3.2-B-001` through `CEPTS3.2-B-014`, in locked
oracle order, and adds both groups to `COMPLETED_GROUPS`. Actor and kind
bindings are exact: A preserves three Assessor provisions and one Delivery
Partner recommendation; B preserves the Delivery Partner, Certification Body,
and Assessor assignments across procedure steps, prerequisites, decision
rules, applicability entries, and recommendations. Every PDF and printed-page
locator, section, detail, and canonical official URL matches the locked oracle.

All records use schema `1.0.0`, requirement granularity, `draft` status, the
required mapping-set ID, paraphrase mode, approved mapper metadata, and
original oracle-approved summaries. The completed-batch source guard checked
the summaries, negative rationales, and any relationship narratives against
the protected five-word source-window set and passed. The records contain no
copied external requirement or passage text, IASME-derived structure, imagery,
marks, or endorsement language.

The snapshot contains exactly 144 provision records, with group counts
`24/16/11/9/37/9/7/13/4/14` for
`M/T1/S/T2/T3/T4/T5/C/A/B`. The A/B batch contributes exactly 18 negative
dispositions, zero mapped dispositions, zero relationship legs, and zero
distinct referenced ESAF controls.

## Normative-only mapping determination

The all-negative disposition is correct. A candidate-control search across the
pinned 91-control corpus identified the concretely plausible requirements and
their exact `## Requirement` text was inspected, including `APP-140`,
`INF-120`, `INF-110`, `AUD-100`, `AUD-120`, and `DAT-120`. `APP-140` requires
controlled secure-development, testing, vulnerability, and change practices
for AI application artifacts. `INF-120` requires risk-based identification,
assessment, treatment, or acceptance of AI-infrastructure vulnerabilities.
Neither requires authorization of a particular external scanner, execution
over the specified address or port population, delivery of a port list,
scanner output, or an observed result. `INF-110` hardening likewise supplies
no such external procedure or result.

The pinned ESAF baseline has no normative requirement that supplies B-005's
specific anti-malware detection-and-access-prevention criterion or B-006's
warning-and-user-choice criterion. `AUD-100` governs an internal risk-based AI
assessment program and `AUD-120` governs sufficient assessment evidence;
neither creates the external assessment-file delivery, hosting, subset,
tailoring, or file-format outcomes. `DAT-120` governs data fitness for an AI
capability, not the composition of this external test-file set. Conditions
could narrow an otherwise supported relationship but could not supply these
missing outcomes.

All-negative determination: **approved**. No missed direct support was found,
and no positive leg is justified by exact normative ESAF requirement text.

## A authorization, execution, and result boundary

A-001 correctly treats Delivery Partner authorization of scanner tools as a
prerequisite only; it does not infer that a scanner ran, produced output, or
established a result. A-002 correctly preserves the instruction to scan every
Applicant-associated address while declining to infer execution, output, or
implementation evidence. A-003 preserves the limited-port alternative and
Delivery Partner scoping without converting port coverage into an observation.
A-004 preserves delivery of the TCP/UDP port inventory as procedure setup,
not scanner execution or a control result.

Each A rationale names its precise missing outcome, and together they preserve
authorization, address population, port population, procedure setup, execution,
output, and observation as separate concepts. None implies procedure
completion, population assurance, vulnerability remediation, compliance, or
certification.

A authorization/execution boundary: **approved**.

## B assessment-file, tailoring, and evidence boundary

B-001 preserves the Delivery Partner's duty to supply every required
assessment file, while B-007 separately preserves advance delivery of a
representative set. B-010 through B-012 preserve the three mandatory
full-set format categories. These records establish file availability or
complete-file assembly only; they do not establish that testing occurred or
that a normative ESAF safeguard was implemented.

B-002 and B-003 separately preserve Certification Body subset definition and
hosting. B-004 preserves the Assessor's prospective correct-file confirmation.
B-008 and B-009 preserve encouragement of Applicant-specific tailoring and the
resulting relevance of the subset. None converts definition, hosting,
confirmation, or tailoring into a performed technical check or observation.

B-005 and B-006 correctly preserve external expected-behavior decision rules
without representing those expectations as observed detection, access
prevention, warning, user choice, or ESAF implementation evidence. B-013
preserves design of a conspicuously observable executable artifact without
claiming it was executed. B-014 preserves selection of a generally detectable
inert sample without claiming detection. Their missing-outcome rationales are
specific to the distinct expectation, artifact-design, selection, execution,
and observation boundaries.

B assessment-file boundary: **approved**. File availability, complete-set
coverage, representative-set selection, subset definition, hosting, tailoring,
file categories, expected behavior, artifact design, and observed
implementation evidence remain distinct.

## Lifecycle, catalogs, provenance, and regression quality

The lifecycle remains `draft`, its `events` array remains empty, and its
independently validated snapshot digest is
`7fd8388923c3ac0e05cbfa7e448ca25161ef2213563d48198288b0f3c9a560dc`.
Both generated catalogs consistently derive the final 144-record mapping-set
population and repository totals of 260 provisions, 49 directional
relationships, and 213 negative dispositions.

The focused regressions are proportionate and candidate-bound. The completed-
batch test enforces exact oracle membership, metadata, approved summaries,
locators, mapper provenance, source-copy protection, manifest bindings, and
mapping direction. The new A test preserves authorization versus execution,
scanner output, observed result, address coverage, and port coverage. The new
B test preserves complete-file assembly, representative-set, subset,
hosting, and tailoring boundaries. The final count test enforces the exact
144-record population, every group count, the 18-record A/B universe, zero
legs, and 18 negative dispositions. Existing snapshot tests enforce schema,
draft lifecycle, empty events, deterministic baseline manifest, digest, and
catalog freshness.

The implementation report records an initial 18-file RED and the required
oracle-ordered single-record RED/GREEN cycle for each A/B provision, followed
by final focused and full validation. Its claimed candidate scope agrees with
the independently inspected exact range.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

No Critical or Important finding remains unresolved.

## Verdicts

Specification verdict: **approved**. Exact candidate
`e88e7756d78fa6bc7c94bb7ba8aa6be96e976ca6` satisfies the binding Task 12
contract: exact 18-row oracle fidelity, correct all-negative dispositions,
specific missing outcomes, preserved A authorization/execution/result and B
assessment-file/tailoring/evidence boundaries, normative-only mapping
judgment, original paraphrases and source protection, correct schema and
provenance, final 144-record completion, draft lifecycle with empty events,
and deterministic catalog derivation.

Task-quality verdict: **approved**. The implementation is tightly scoped,
test-first, and supported by credible candidate-bound evidence. Focused
regressions directly enforce the appendix boundaries and final population,
and the exact candidate contains no unrelated or reviewer-authored change.
