# v0.17-draft Independent Governance Review

## Review identity and scope

- Reviewer: `Codex ESAF Governance Publication Reviewer`
- Review date: 2026-09-16
- Exact candidate SHA: `40646efdeada24675ac9e198c53b84cffd113784`
- Exact candidate branch: `cursor/v017-evidence-candidate-0e44`
- Scope: Issue #208 evidence-candidate boundaries, milestone non-goals,
  retained readiness `HOLD` boundaries, CIS Controls Version 8 readiness
  package non-expansion, Phase 6 third deepen non-expansion relative to
  ESAF-1500, SOC 2 non-goal, UK profile non-deepen beyond Draft `0.2.0`, and
  post-v0.16 backlog hygiene required before allowlist-bound closure.
- Independence: the reviewer did not author the CIS Controls readiness
  Markdown under review.

The review covered:

- `project/MILESTONES.md` `v0.17-draft` non-goals for Issues #55 and #60, PCI
  DSS HOLD, NIST AI RMF HOLD, ISO/IEC 42001 HOLD, NIST CSF HOLD, ISO/IEC
  27001 HOLD, NIST SP 800-53 HOLD, CIS Controls HOLD without mapping
  authorship, SOC 2 readiness package, second industry profile, and Draft
  lifecycle non-advancement;
- Phase 6 third deepen introducing no schema-breaking ESAF-1500 / ESAF-1800
  contract changes and no certification claims;
- publication-readiness record nonclaims and lifecycle-boundary wording that
  keeps `VERSION.md` at `0.16-draft` until closure;
- confirmation that CIS Controls and prior HOLD-scheme mapping authorship
  remain unauthorized under `HOLD`;
- `tools/v017_draft_release_gates.py` closure allowlist discipline that binds
  only the `closure_candidate` transition;
- confirmation that Issues `#205`–`#208` are linked in
  `project/BACKLOG.md` under the Post-v0.16 scheduled queue and that
  milestone `v0.17-draft` exists with hygiene, CIS Controls HOLD, and Phase 6
  third deepen complete as prerequisites for this package.

## Findings

The evidence-candidate package preserves the approved milestone boundaries.
Prerequisite dispositions correctly keep Phase 2 timing as `DEFER`, NIST AI
RMF, ISO/IEC 42001, NIST CSF, ISO/IEC 27001, NIST SP 800-53, and CIS Controls
as `HOLD`, ESAF-1300/1400/1700 as Working Draft deepen outcomes at `0.3.0`,
Phase 6 as a third deepen, ESAF-1500 as a Working Draft carry-forward at
`0.1.1`, and the UK profile as Draft `0.2.0`. Issues #55 and #60 are
explicitly allowed to remain open. SOC 2 readiness remains a recorded
non-goal for this milestone.

Open Critical: 0
Open Important: 0
Verdict: Approve for advancing toward `closure_candidate` after technical and
editorial reviews and full exact-SHA validation.

## Nonclaims

This governance review does not close Issue [#55](https://github.com/tdistress/ESAF/issues/55)
or Issue [#60](https://github.com/tdistress/ESAF/issues/60). It does not clear
PCI DSS, HITRUST, NIST AI RMF, ISO/IEC 42001, NIST CSF, ISO/IEC 27001, NIST
SP 800-53, or CIS Controls blockers, authorize mapping authorship under
`HOLD`, author a SOC 2 readiness package, create tag `v0.17-draft`, or
establish certification, compliance, equivalence, endorsement, assurance, or
production readiness.

## Limitations

Closure still requires synchronized Working Draft surfaces, post-merge
validation, and annotated-tag evidence before any published-phase claim.
Any change to the evidence-candidate head after this review requires SHA
retarget and redispatched exact-SHA review before closure.
