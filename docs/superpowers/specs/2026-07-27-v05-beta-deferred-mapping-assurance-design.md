# v0.5-beta deferred mapping assurance design

**Status:** Approved

**Date:** 2026-07-27

## Purpose

Qualified review of the three UK mapping sets may take weeks or months. ESAF
shall continue toward `v0.5-beta` without treating the missing reviewers as
completed assurance or removing the mappings from the release.

This design permits one coordinated deferred-assurance disposition for the
three mapping sets. The mappings remain Draft and issue 55 remains open until
qualified human review is complete.

## Decisions

### Release policy

`DEFERRED` is a milestone assurance disposition. It is not an ESAF-1600
mapping lifecycle state.

The `v0.5-beta` exit criteria shall accept either:

1. completed qualified-review dispositions for all three UK mapping sets; or
2. one coordinated owner-risk disposition that defers qualified review for all
   three exact mapping sets on the exact release candidate.

The deferred path shall not add reviewer metadata, lifecycle events, approval
state, or publication state to a mapping artifact. All three mapping sets and
their records remain `draft`.

### Included release scope

The following mapping sets remain included in `v0.5-beta`:

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`

Release evidence shall identify them as Draft artifacts whose qualified review
is deferred.

## Evidence model

The release gate already supports the required machine-readable basis. This
change shall reuse:

- `mapping_decision_basis: owner_risk_acceptance`;
- `decision_type: owner_risk_acceptance`; and
- `qualified_review_status: deferred`.

The human-facing milestone and tracking language may call this the
`DEFERRED` qualified-review disposition. No new release-gate enum or mapping
schema value is required.

One authenticated owner decision shall:

- cover each of the three exact mapping-set identifiers once;
- bind every decision to the exact `v0.5-beta` release candidate;
- use one uniform decision basis and one owner source;
- identify the missing qualified human evidence;
- retain Draft lifecycle limitations;
- name the accountable owner and re-entry triggers; and
- preserve the required nonclaims.

The release gate shall reject mixed decision bases, stale candidate SHAs,
missing or duplicate mapping decisions, nonuniform owner sources, changed
lifecycle state, or weakened nonclaims.

## Human-review boundary

Owner-risk acceptance permits Working Draft publication. It does not complete
qualified review and cannot substitute for the six human role dispositions:

- specification and inventory review for Core;
- security and overclaiming review for Core;
- specification and inventory review for Plus forward;
- security and overclaiming review for Plus forward;
- specification and inventory review for Plus reverse; and
- security and overclaiming review for Plus reverse.

Issue 55 shall remain open. A later transition requires the existing
qualified-review evidence process, owner acceptance of reviewer eligibility
and any dual-role arrangement, exact-SHA validation, resolution of every
Critical and Important finding, and signed final confirmation.

The deferred release shall not claim qualified review, approval,
certification, compliance, equivalence, endorsement, external-scheme approval,
or assurance beyond the recorded Working Draft basis.

## Repository tracking

The implementation shall update:

- `project/MILESTONES.md` to add the coordinated deferred path to the
  `v0.5-beta` workstream and exit criteria;
- `ROADMAP.md` to state that deferred mapping assurance remains tracked after
  beta and does not stop later engineering work;
- `project/BACKLOG.md` to separate active release closure from deferred
  assurance follow-up;
- `project/RELEASE_PLAN.md` to describe the exact-candidate owner-risk basis
  for the deferred path; and
- release-metadata regression tests to enforce these boundaries.

GitHub tracking shall be synchronized:

- issue 55 remains open as the deferred assurance follow-up;
- issue 59 becomes executable under either qualified approval or validated
  exact-candidate owner-risk acceptance; and
- issue 59 still requires every other technical, editorial, governance,
  validation, and post-merge release gate.

Historical `v0.4-alpha` evidence shall not approve `v0.5-beta`.

## Validation

Development shall begin with failing release-metadata tests. The tests shall
prove that:

- the milestone accepts completed qualified review or the coordinated deferred
  owner-risk path;
- all three exact mapping sets remain in the qualified-review follow-up;
- issue 55 remains open in the documented workflow;
- issue 59 no longer requires completed human review when valid deferred
  evidence exists;
- the mappings remain Draft;
- the required nonclaims remain explicit;
- HITRUST readiness remains nonblocking; and
- no architecture-pattern work is reintroduced into the active backlog.

The implementation shall run the focused release-metadata and release-gate
tests, standalone validators affected by the documentation, the full unit
suite, link validation, and whole-branch diff checks.

## Execution sequence

1. Update the repository policy and tracking documents with regression tests.
2. Review and merge the policy change.
3. Update issues 55 and 59 to match the merged repository policy.
4. Begin issue 59 release closure from a clean, exact candidate.
5. Acquire and validate a live owner-risk decision for the three mappings
   during release closure unless qualified review has completed by then.
6. Complete the remaining `v0.5-beta` gates and post-merge validation.
7. Continue later engineering work while issue 55 remains open.
8. Process qualified review later through the existing evidence and lifecycle
   transition controls.

## Non-goals

This change does not:

- alter mapping content;
- create a new mapping lifecycle state;
- weaken the qualified-review evidence contract;
- close issue 55;
- treat AI or ordinary pull-request review as qualified human review;
- change the PCI DSS `HOLD` disposition;
- begin substantive HITRUST mapping; or
- publish or tag `v0.5-beta`.
