# Cyber Essentials Plus v3.2 `M` batch specification review

## Review identity and authority

- Review date: `2026-07-16`
- Reviewer ID: `codex-ce-plus-m-specification-reviewer`
- Review role: independent specification and code-quality reviewer
- Authorized source access: `true`
- Candidate SHA: `6eb6691d19c81807f3d1f917fdf225a49096b3b6`
- Reviewed base: `1ca339c03b24264b03cad0e9debae23c84450d59`
- Reviewed range: `1ca339c03b24264b03cad0e9debae23c84450d59..6eb6691d19c81807f3d1f917fdf225a49096b3b6`

The reviewer is distinct from the mapper, the mapping-rights reviewer, and the independently assigned security/overclaiming reviewer. The review used authorized access to the pinned Cyber Essentials Plus v3.2 source boundary and the immutable ESAF baseline at `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`.

## Reviewed artifacts and scope

The review covered the approved design and implementation plan, `.superpowers/sdd/task-3-brief.md`, the corrected Task 3 implementation report, the complete 122,229-byte candidate diff package with 30 file sections, and the exact Git candidate range. The candidate contains exactly 24 new records, `cepts32-m-001.md` through `cepts32-m-024.md`; the focused-test, lifecycle, and generated-catalog changes; and the two authorized integration-test repairs. No oracle, inventory, manifest, schema, validator, README, rights artifact, design, plan, landing-page, backlog, non-`M` record, or review-report change is present in the candidate commit range.

The record review verified oracle order and exact external identifiers, metadata, actors, summaries, and rendered locators; draft lifecycle and mapper provenance; manifest-bound ESAF relationship provenance; disposition structure; original narrative boundaries; generated counts; and the absence of reverse-direction, `out_of_scope`, or record-level reviewer fields. All 24 records are provision-specific. Twenty-two records use `no_direct_mapping` with a specific `Missing outcome:` rationale. The exact positive set is `CEPTS3.2-M-010` and `CEPTS3.2-M-011`, with one relationship leg each.

## Positive relationship review

`CEPTS3.2-M-010` maps to `AUD-130` as `partially_supports`, with narrow coverage and high confidence. The exact pinned `AUD-130` requirement mandates remediation and closure of AI assessment findings, directly contributing to resolution of a preliminary issue when that issue is formally governed as such a finding. The condition establishes that applicability and does not supply the missing external outcome. Its separate gaps preserve the absence of an every-issue clearance duty, closure before the external test sequence, assignment to the Assessor, and Cyber Essentials Plus procedure execution or results. Its prohibited inferences also reject testing completion, certification, compliance, equivalence, and endorsement. The control path, version, SHA-256 digest, and requirement locator match the committed 91-control manifest.

`CEPTS3.2-M-011` maps to `AUD-120` as `partially_supports`, with narrow coverage and high confidence. The exact pinned `AUD-120` requirement mandates retention of sufficient evidence for each AI assessment procedure, determination, scope, and period. The leg limits applicability to an ESAF-governed AI assessment and preserves the absent Certifying Body assignment, all-artifact requirement, certificate-lifetime duration, procedure execution, population completeness, and certification outcome. Its manifest provenance is exact.

No positive leg treats implementation guidance, adjacency, procedure execution, observed results, sampling, aggregate sufficiency, certification, compliance, equivalence, endorsement, current-scheme coverage, or continuous assurance as a supported outcome.

## Test and generated-artifact review

The focused test remains fail-closed and readable. The completed-batch helper validates present records during the TDD authoring cycle and still requires exact final path equality. The added exact-positive-set test locks M-010 and M-011, two M-batch relationships, and 22 negative dispositions. Catalog assertions match the regenerated totals of 2 mapping sets, 140 provisions, 43 relationships, and 98 negative dispositions. The lifecycle digest matches the corrected snapshot and lifecycle events remain empty.

The two integration fixes remain within their authorization. The feasibility regression evaluates the accepted PR #46 parent-to-parent range rather than later authorized mapping work. The v3.3 regression retains exact snapshot-local counts while deriving repository-wide totals from all mapping-set entries, eliminating the stale single-snapshot assumption without weakening the v3.3 invariant.

## Validation evidence

Independent review commands produced the following results on exact candidate `6eb6691d19c81807f3d1f917fdf225a49096b3b6`:

- Focused Cyber Essentials Plus mapping suite: 9 tests passed.
- Authorized feasibility-history and v3.3 catalog regressions: 2 tests passed.
- Crosswalk validation in ordinary mode: passed with 2 mapping sets, 140 provisions, 43 relationships, and 98 negative dispositions.
- Crosswalk validation against baseline `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`: passed with the same counts.
- `git diff --check 1ca339c03b24264b03cad0e9debae23c84450d59..6eb6691d19c81807f3d1f917fdf225a49096b3b6`: passed.
- Exact candidate audit: 24 `M` records, 2 mapped records, 22 negative dispositions, 2 relationship legs, and positive IDs exactly M-010 and M-011.

The corrected implementation report additionally records a full-suite gate of 304 passing tests with 3 skips, 361-file link validation, TDD RED-to-GREEN evidence for the M-010 correction, exact staged-path review, postcommit gates, no Python cache artifacts, and a clean candidate worktree. These report-backed results are consistent with the independently rerun focused and domain gates.

## Findings

- Critical: none.
- Important: none.
- Minor: none.

## Disposition

Approved. Candidate `6eb6691d19c81807f3d1f917fdf225a49096b3b6` satisfies the Task 3 `M`-batch specification and code-quality requirements. No Critical or Important finding remains, and no candidate-content change is required before the separate overclaiming review and report-only batch-closure commit.
