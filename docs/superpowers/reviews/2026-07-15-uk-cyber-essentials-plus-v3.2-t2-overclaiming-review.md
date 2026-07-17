# Cyber Essentials Plus v3.2 T2 Security and Overclaiming Review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t2-overclaiming-reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 95d5420ec42d0242e17109d31081a49320e13537
reviewed_base_sha: 6f326f68fafe14ad1834edf2ace9e60ffb9e4c73
review_disposition: approved

## Scope and independence

This independent review covers the exact candidate range
`6f326f68fafe14ad1834edf2ace9e60ffb9e4c73..95d5420ec42d0242e17109d31081a49320e13537`
for `CEPTS3.2-T2-001` through `CEPTS3.2-T2-009`, the focused regression
contract, lifecycle digest, and generated catalogs. The reviewer is distinct
from the mapper, mapping-rights reviewer, and T2 specification reviewer.

The review used authorized access to the pinned official NCSC Cyber Essentials
Plus Test Specification v3.2 source, whose canonical SHA-256 is
`2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`,
the locked 144-provision oracle, the committed 91-control ESAF manifest, and
exact normative `## Requirement` text from immutable ESAF baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. Reviewed artifacts also include
`.superpowers/sdd/task-6-brief.md`, `.superpowers/sdd/task-6-report.md`, and the
complete candidate package `.superpowers/sdd/review-6f326f6..95d5420.diff`.
HEAD was verified as the exact reviewed candidate before analysis and before
report creation.

## Security and overclaiming assessment

- All nine dispositions were reviewed independently and provision-first.
  Every record correctly uses `no_direct_mapping`, has no relationship leg,
  and identifies the specific external outcome absent from ESAF.
- The review specifically considered INF-120 together with narrower duties in
  AUD-100, AUD-110, AUD-120, AUD-130, APP-140, ARC-150, GOV-140, RSK-100,
  RSK-120, and the surrounding INF control family. INF-120 requires
  vulnerability identification, assessment, prioritization, remediation,
  mitigation, or acceptance according to risk factors. Those duties do not
  require this external test, its sampled device and infrastructure
  population, a Delivery Partner-approved scanner, or Assessor execution of
  that scanner against every selected device. Assessment-program, evidence,
  testing, authorization, technology-currency, exception, and risk-treatment
  duties likewise do not supply those missing scheme-specific outcomes.
- No ESAF normative requirement supplies the external vendor high-risk or
  critical interpretation, the CVSS version 3 base-score threshold, the rule
  for updates without vendor severity detail, an observed qualifying
  vulnerability, its vendor-fixable age, the 14-day threshold, the sub-test
  pass/fail result, the unsupported-legacy-system virtual-patching exclusion,
  or the aggregate Test case 2 result. No narrower direct support was omitted.
- No implementation guidance, assessment procedure, expected-evidence item,
  adjacent capability, condition, or chain of controls is used to manufacture
  Assessor workflow, scanner availability or execution, target or sample
  coverage, vendor or CVSS interpretation, observed vulnerability state or
  age, an exclusion rule, or individual or aggregate results.
- The known anomaly remains outside the locked nine-provision T2 universe. It
  is not copied, corrected, converted into a provision, duplicated, or used to
  expand the source. Its identifier and locator are handled only by the
  fail-closed regression assertion, and it supplies no mapping outcome.
- The records preserve original paraphrases within the authorized public v3.2
  source boundary. They do not represent the public source as the current
  operational scheme or infer later-scheme, IASME-only, or adjacent-assurance
  requirements.
- The snapshot remains draft and forward-only `esaf_to_external`. The batch
  implies no procedure execution, observed result, sample or population
  coverage, testing success, certification, compliance, equivalence,
  endorsement, current-scheme completeness, full-population assurance, or
  continuous assurance.

## Validation evidence

- Focused Plus mapping suite: 17 tests passed in 11.624 seconds, including the
  exact nine-record universe, zero positive relationships, nine negative
  dispositions, anomaly non-expansion, source-copy guard, baseline-manifest
  binding, catalog assertions, and fail-closed closure behavior.
- Control validation passed for 91 controls, 91 objectives, and 16 families.
- Crosswalk validation passed in ordinary and pinned-baseline modes with 2
  mapping sets, 176 provisions, 46 relationships, and 131 negative
  dispositions.
- Link validation passed for 403 tracked Markdown files.
- Whole-range `git diff --check` passed for the exact reviewed base and
  candidate. The implementation report records a full repository suite of 312
  passing tests with 3 skipped, exact 13-path candidate scope, zero Python
  cache artifacts, and a clean postcommit worktree.

## Findings

- Critical: none.
- Important: none.
- Minor: none.

## Disposition

Approved. Exact candidate
`95d5420ec42d0242e17109d31081a49320e13537` is approved for Task 6 T2-batch
technical closure from the security and overclaiming perspective. This
approval does not promote the draft snapshot or establish scanner approval or
execution, sample or population coverage, observed vulnerability state,
interpretation-rule satisfaction, assessment success, certification,
compliance, equivalence, endorsement, current-scheme coverage,
full-population assurance, or continuous assurance.
