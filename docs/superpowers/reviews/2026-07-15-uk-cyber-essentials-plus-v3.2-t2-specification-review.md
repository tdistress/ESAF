# Cyber Essentials Plus v3.2 `T2` batch specification review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t2-specification-reviewer
reviewer_role: independent specification and code-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 95d5420ec42d0242e17109d31081a49320e13537
reviewed_base_sha: 6f326f68fafe14ad1834edf2ace9e60ffb9e4c73
reviewed_range: 6f326f68fafe14ad1834edf2ace9e60ffb9e4c73..95d5420ec42d0242e17109d31081a49320e13537
specification_verdict: approved
task_quality_verdict: approved_with_minor_evidence_finding

## Independence and authority

The reviewer is distinct from the mapper, the mapping-rights reviewer, and
the independently assigned `T2` security and overclaiming reviewer. This
review used authorized access to the pinned official NCSC Cyber Essentials
Plus Test Specification v3.2 and the locked 144-row provision oracle. ESAF
analysis was independently checked against normative `## Requirement` text at
immutable baseline `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`; mutable
working-tree prose, implementation guidance, assessment procedures,
similarity, and adjacency were not used as positive bases.

## Reviewed artifacts and scope

The review covered `.superpowers/sdd/task-6-brief.md`,
`.superpowers/sdd/task-6-report.md`, the complete package
`.superpowers/sdd/review-6f326f6..95d5420.diff`, the exact Git candidate
range, all nine `T2` records, the focused test, lifecycle registry, both
generated catalogs, the locked oracle, the committed 91-control manifest,
and schema and validator behavior. HEAD was verified as exact candidate
`95d5420ec42d0242e17109d31081a49320e13537` before review and immediately
before report creation.

The candidate range contains exactly the 13 authorized paths: nine new
records `cepts32-t2-001.md` through `cepts32-t2-009.md`, the focused Plus
test, the Plus lifecycle registry, and the JSON and Markdown catalogs. No
prior record, oracle, inventory, manifest, schema, validator, design, plan,
rights artifact, README, landing page, backlog, or review report changed in
the candidate range.

## Complete specification assessment

The nine records follow the locked oracle sequence. Record and external
identifiers, group, kind, actors, original paraphrase, official URL, and
rendered dual-coordinate locator match each oracle row exactly. Every record
uses schema version `1.0.0`, requirement granularity, `draft` status, the
authorized mapper identity and date, an empty relationship array, and a
provision-specific `no_direct_mapping` rationale beginning `Missing outcome:`.
No record uses `out_of_scope`, and the exact batch totals are zero positive
records, zero relationship legs, and nine negative dispositions.

The dispositions preserve all missing external outcomes separately:
assessment-population applicability, Delivery Partner scanner approval,
scanner execution against each selected device, vendor-rating and CVSS
interpretation criteria, missing-vendor-detail interpretation, the observed
age-based sub-test result, the unsupported-legacy-system virtual-patching
exclusion, and the aggregate Test case 2 result. Pinned INF-120 requires
risk-based vulnerability identification, assessment, prioritization, and
disposition for AI infrastructure and dependencies. It does not require the
external Assessor workflow, scanner authorization or execution, sampled-device
coverage, an observed vulnerability state, the source-specific thresholds or
exclusion, or either pass/fail outcome. The candidate therefore correctly
declines to manufacture a positive relationship from vulnerability-management
adjacency.

No record or relationship implies procedure execution, an observed result,
sample or population coverage, certification, compliance, equivalence,
endorsement, current-scheme completeness, full-population assurance, or
continuous assurance.

## Anomaly, tests, and generated artifacts

The known anomaly remains solely oracle identifier `cepts32-anomaly-001` at
`PDF page 6; printed page 5; General prerequisites for testing; introductory
applicability line`. It is not converted into a provision or relationship,
does not expand the exact nine-record `T2` universe, and is not reproduced in
the records. The focused assertion verifies its frozen no-correction and
no-expansion treatment by oracle fields without embedding its source literal.

The focused tests lock the exact nine oracle and record IDs, empty positive
set, zero relationships, nine negatives, anomaly identity and locator,
non-expansion, and non-reproduction. The completed-batch helper checks oracle
metadata, summaries, locators, mapper provenance, draft status, source-copy
boundaries, and exact completed-path equality. The future-safe closure test
accepts neither report, rejects a one-report-only state, and, when both reports
exist, requires authorized-source attestations and pairwise-distinct mapper,
rights reviewer, `T2` specification reviewer, and `T2` overclaiming reviewer
IDs. The specification and overclaiming reviewer IDs present at report
creation are distinct from each other and from the mapper and rights reviewer.

The lifecycle remains `draft`, its events remain empty, and snapshot digest
`1a62d143efecae0e9f1f372e1061cad485638f820d56e5a72f8859c5c54abe52`
matches the snapshot. Catalog derivation is consistent: the Plus snapshot has
60 completed records, and repository totals are 2 mapping sets, 176
provisions, 46 directional relationships, and 131 negative dispositions.

## Independent validation evidence

Fresh review commands on the exact candidate produced these results:

- Focused Plus mapping suite: 17 tests passed.
- Full repository suite: 312 tests passed, 3 skipped.
- Control validation: 91 controls, 91 objectives, and 16 families passed.
- Crosswalk validation in ordinary and pinned-baseline modes: passed with 2
  mapping sets, 176 provisions, 46 relationships, and 131 negative
  dispositions.
- Link validation: all 403 tracked Markdown files passed.
- Exact-range `git diff --check`: passed; the candidate range contains exactly
  13 authorized paths, and no Python cache directory was present.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: `.superpowers/sdd/task-6-report.md` records link validation against
  394 tracked Markdown files, while a fresh run on the exact candidate
  validates 403. The nine-file difference is exactly the new `T2` record
  population. The complete fresh gate passes, so this is stale implementation
  evidence rather than a candidate or validator defect.

## Verdicts

Specification verdict: **approved**. Exact candidate
`95d5420ec42d0242e17109d31081a49320e13537` satisfies the binding Task 6
specification: exact nine-row oracle fidelity, source/anomaly boundary,
normative-only disposition analysis, zero positive relationships, nine
provision-specific negative dispositions, draft/schema/provenance requirements,
closure identity behavior, and deterministic lifecycle and catalog derivation.

Task and code-quality verdict: **approved with one minor evidence finding**.
The implementation is focused, deterministic, validator-backed, and supported
by credible per-record RED-to-GREEN evidence. The stale link-validation file
count should be corrected when the implementation report is next maintained,
but fresh full-scope validation establishes the gate result and no candidate
content change is required before the report-only closure commit.
