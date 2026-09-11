# v0.15-draft Independent Governance Review

## Review identity and scope

- Reviewer: `Codex ESAF Governance Publication Reviewer`
- Review date: 2026-09-11
- Exact candidate SHA: `1ef1164f39d686ba03253e6f5858266cd49703d9`
- Exact candidate branch: `main` (merge of PR #188)
- Scope: Issue #185 evidence-candidate boundaries, milestone non-goals,
  retained readiness `HOLD` boundaries, ISO/IEC 27001 readiness package
  non-expansion, Phase 6 / ESAF-1300/1400/1700 deepen non-expansion relative
  to existing normative contracts, and post-v0.14 backlog hygiene required
  before allowlist-bound closure.
- Independence: the reviewer did not author the deepen Markdown under review.

The review covered:

- `project/MILESTONES.md` `v0.15-draft` non-goals for Issues #55 and #60, PCI
  DSS HOLD, NIST AI RMF HOLD, ISO/IEC 42001 HOLD, NIST CSF HOLD, ISO/IEC
  27001 HOLD without mapping authorship, and Draft lifecycle non-advancement;
- deepen packs introducing no schema-breaking ESAF-1300/1400/1700/1500
  contract changes;
- publication-readiness record nonclaims and lifecycle-boundary wording that
  keeps `VERSION.md` at `0.14-draft` until closure;
- confirmation that NIST CSF, NIST AI RMF, ISO/IEC 42001, and ISO/IEC 27001
  mapping authorship remain unauthorized under `HOLD`;
- `tools/v015_draft_release_gates.py` closure allowlist discipline that binds
  only the `closure_candidate` transition.

## Findings

The evidence-candidate package preserves the approved milestone boundaries.
Prerequisite dispositions correctly keep Phase 2 timing as `DEFER`, NIST AI
RMF, ISO/IEC 42001, NIST CSF, and ISO/IEC 27001 as `HOLD`, ESAF-1300/1400/1700
as Working Draft deepen outcomes at `0.3.0`, Phase 6 as a second deepen, and
ESAF-1500 as a Working Draft carry-forward at `0.1.1`. Issues #55 and #60 are
explicitly allowed to remain open.

One Important finding on the evidence candidate required remediation before
allowlist-bound closure: the Post-v0.14 scheduled queue in
`project/BACKLOG.md` lacked Issue `#181`–`#185` links. That hygiene gap is
outside `CLOSURE_ALLOWLIST` and is remediated in the same review-binding
change set.

Open Critical: 0  
Open Important: 0 (after backlog Issue `#181`–`#185` link remediation)  
Verdict: Approve for advancing toward `closure_candidate` after technical and
editorial reviews and full exact-SHA validation.

## Nonclaims

This governance review does not close Issue [#55](https://github.com/tdistress/ESAF/issues/55)
or Issue [#60](https://github.com/tdistress/ESAF/issues/60). It does not clear
PCI DSS, HITRUST, NIST AI RMF, ISO/IEC 42001, NIST CSF, or ISO/IEC 27001
blockers, authorize mapping authorship under `HOLD`, create tag
`v0.15-draft`, or establish certification, compliance, equivalence,
endorsement, assurance, or production readiness.

## Limitations

Closure still requires synchronized Working Draft surfaces, post-merge
validation, and annotated-tag evidence before any published-phase claim.
