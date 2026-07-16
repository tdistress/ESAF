# Cyber Essentials Plus v3.2 `T1` batch specification review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t1-specification-reviewer
reviewer_role: independent specification and code-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 98fce9ea0f71285b2198a17e5d4fa373a8c8d689
reviewed_base_sha: 1ab5375784671b6674e05f51f1802eb91cf9676f
reviewed_range: 1ab5375784671b6674e05f51f1802eb91cf9676f..98fce9ea0f71285b2198a17e5d4fa373a8c8d689
specification_verdict: approved
task_quality_verdict: approved

## Independence and authority

The reviewer is distinct from the mapper, the mapping-rights reviewer, and the independently assigned `T1` security and overclaiming reviewer. This review used authorized access to the pinned official NCSC Cyber Essentials Plus Test Specification v3.2. The reviewed source matched pinned SHA-256 `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`, and the control analysis remained limited to normative `## Requirement` text at immutable ESAF baseline `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`.

## Reviewed artifacts and evidence

The review covered `.superpowers/sdd/task-4-brief.md`, `.superpowers/sdd/task-4-report.md`, the complete 86,020-byte and 20-section package `.superpowers/sdd/review-1ab5375..98fce9e.diff`, the exact Git range, all 16 `T1` records, the focused test, lifecycle registry, both generated catalogs, the locked 144-row provision oracle, the committed 91-control manifest, schema and validator behavior, and rendered official PDF pages 8 through 10. Candidate `98fce9ea0f71285b2198a17e5d4fa373a8c8d689` is the exact reviewed HEAD and contains only the authorized 20-path Task 4 range: 16 new `T1` records, the focused Plus test, lifecycle registry, and two catalogs. The range includes the required initial candidate commit and two focused correction commits; no prohibited artifact changed.

The implementation report's per-record RED-to-GREEN evidence, correction RED/GREEN cycles, exact staged and commit-scope audits, full-suite results, link validation, cache checks, and clean postcommit state were considered. Independent review reran the 12-test focused suite, control validation, both ordinary and pinned-baseline crosswalk checks, and whole-range `git diff --check`; all passed. Derived repository totals are 2 mapping sets, 156 provisions, 45 relationships, and 112 negative dispositions.

## Complete specification assessment

All records appear in locked oracle order as `CEPTS3.2-T1-001` through `CEPTS3.2-T1-016`. Their identifiers, group, kind, actors, independently written summaries, official URL, and rendered dual-coordinate locators match the oracle. Every record remains `draft` and carries the required mapper identity, date, and authorized-source provenance. Fourteen records use `no_direct_mapping`, have empty relationships, and begin a provision-specific rationale with `Missing outcome:`. No record uses `out_of_scope`.

The exact positive set is `CEPTS3.2-T1-011 -> IAM-110` and `CEPTS3.2-T1-013 -> IAM-140`, each with one `partially_supports`, `narrow`, high-confidence, forward-only `esaf_to_external` leg. Their versions, paths, record digests, and requirement locators exactly match the committed manifest.

IAM-110 normatively requires authentication before access to non-public AI assets. T1-011 conditions the contribution on a user accessing such assets through the assessed Internet service. Its rationale and evidence establish only that bounded authentication predicate, while its gaps and prohibited inferences preserve Assessor assignment, Figure 1 execution, every-service coverage, observed state, branch and result assignment, procedure execution, testing completion, certification, compliance, equivalence, and endorsement.

IAM-140 normatively requires the organization to rotate credentials used by AI capabilities through approved secrets-management mechanisms. T1-013 conditions the contribution on the service default password being such a credential. Its corrected rationale expressly binds IAM-140's rotation duty to changing that default-password credential, and expected evidence now requires a secrets-management record demonstrating that the in-scope credential was rotated or changed. The existing gaps remain intact: IAM-140 does not supply the change deadline, coverage of every default password, Assessor assignment, Figure 1 execution, observation, branch or failure result, or Cyber Essentials Plus procedure and test results. The leg therefore contributes to the conditioned credential-change predicate without manufacturing the complete external decision rule.

The remaining records preserve the missing Delivery Partner scanner approval, address enumeration and dynamic-address handling, complete Applicant and IaaS address populations, all-address TCP/UDP scan, discovered-service flow execution, unsupported Figure 1 decisions, and aggregate Test case 1 result. No condition, adjacent capability, implementation guidance, assessment procedure, or aggregate logic supplies a missing outcome.

T1-008 remains the per-discovered-service Figure 1 application step; T1-009 through T1-015 remain seven distinct decision-and-branch records in source order; and T1-016 remains the separate aggregate result rule. The oracle's known-source anomaly remains outside this chain and is neither copied, corrected, duplicated, nor used to expand the frozen provision universe.

## Tests and generated artifacts

The focused completed-batch helper remains fail-closed on oracle order, metadata, locators, provenance, relationship structure, and exact completed-path equality. The exact-positive-set test locks the two positive IDs, two legs, and fourteen negative dispositions. The new T1-013 regression directly requires the rationale to name IAM-140, rotation, and the default-password credential, and requires evidence that this credential was rotated or changed. It reproduces the prior defect and is focused enough to prevent recurrence without coupling to unrelated prose.

The future-safe closure test permits only neither or both independent reports, parses both reviewer IDs, requires both authorized-source attestations, and proves pairwise distinction across mapper, rights reviewer, specification reviewer, and overclaiming reviewer. The candidate passes before reports exist.

The lifecycle remains `draft`, its event array remains empty, and snapshot digest `c8566bed0a196f319d0406b0863541fb83228b3e87083e7565037025134d1dcc` matches the corrected snapshot. The Plus catalog contains 40 completed records, including 16 `T1` records, two `T1` legs, and fourteen `T1` negative dispositions. JSON and Markdown catalog outputs are consistently derived.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

## Verdicts

Specification verdict: **approved**. Exact candidate `98fce9ea0f71285b2198a17e5d4fa373a8c8d689` satisfies the binding Task 4 specification, including oracle fidelity, exact positive and negative dispositions, normative provenance, Figure 1 distinctness, anomaly boundary, lifecycle and catalog derivation, and closure identity behavior.

Task and code-quality verdict: **approved**. The implementation is focused, deterministic, validator-backed, and supported by credible initial and corrective TDD evidence. The T1-013 regression meaningfully locks the corrected normative basis and evidence requirement. No candidate-content change is required before the independent overclaiming report and report-only closure commit.
