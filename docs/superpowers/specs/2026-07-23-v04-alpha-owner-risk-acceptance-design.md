# ESAF 0.4-Alpha Owner Risk-Acceptance Design

## Purpose

This amendment allows the ESAF repository owner to accept residual mapping-review risk for publication of the `0.4-alpha` Working Draft when qualified mapping review is not available and the owner determines that the missing review shall not block the milestone.

The amendment does not convert owner acceptance into qualified mapping review. It preserves the deferred review as an explicit limitation and keeps every architecture, control, and mapping artifact in Draft state.

## Decision

The publication evidence model shall support two uniform mapping-decision bases:

1. `qualified_approval`, which preserves the substantive qualified-review checks defined by the original publication-gate design; and
2. `owner_risk_acceptance`, which records the repository owner's decision to accept the absence of qualified review for this Working Draft.

For `0.4-alpha`, all three in-scope mapping decisions shall use the same basis. Mixed bases are outside scope and shall fail validation.

Either basis may satisfy the mapping gate, but published evidence shall identify the basis used. Owner risk acceptance shall never be described as qualified review, scheme approval, assurance, compliance, certification, equivalence, endorsement, or production readiness.

The same owner decision may approve the complete Git-tracked release scope when it explicitly records `scope: complete_git_tracked_repository`.

## Amendment precedence

This amendment supersedes only these requirements:

- Section 5.3 and the mapping-review portions of Sections 6 and 7 of `docs/superpowers/specs/2026-07-21-v04-alpha-publication-gates-design.md` that require qualified approval or digest-backed qualified reaffirmation as the sole mapping-gate disposition.
- Section 9.2 and the qualified-review acceptance criterion in Section 11 of that design that make non-publication the only outcome when qualified review is unavailable.
- Task 4 Step 7, Task 6 Step 3, and the corresponding external-evidence clauses in `docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md` that require three qualified mapping approvals and stop publication when they are unavailable.
- Every other qualified-only mapping clause in that execution plan that conflicts with this amendment, including task interfaces, PR templates, external-evidence construction, final issue evidence, and execution stop conditions.

Those clauses shall instead require one uniform `mapping_decision_basis` and exactly one decision per in-scope mapping set under the schema below.

The execution plan shall be revised throughout before use; a partially updated plan shall fail review.

All non-conflicting requirements remain unchanged, including exact closure-head binding, GitHub checks, clean merge state, Steering Committee governance approval, post-merge validation, current UTC publication date, annotated-tag identity, lifecycle limitations, issue evidence, and cleanup.

## Evidence schema

External closure evidence shall use `mapping_decision_schema: esaf-mapping-decisions-v1`, a top-level `mapping_decision_basis`, and a `mapping_decisions` array containing exactly one decision for each in-scope mapping-set ID.

Every decision shall contain:

- `mapping_set_id`;
- `decision_type`, equal to the top-level basis;
- `sha`, equal to `closure_head`;
- an RFC 3339 `decided_at` timestamp whose UTC date equals the conditional publication date;
- an HTTPS GitHub evidence URL; and
- structured limitations:
  - `lifecycle: draft`;
  - `claims_not_made`, equal as a set to `compliance`, `certification`, `equivalence`, `endorsement`, `external_scheme_approval`, `assurance`, and `production_readiness`.

A `qualified_approval` decision shall additionally contain:

- `reviewer`;
- `qualification`;
- `disposition: approved`; and
- `qualified_review_status: completed`.

An `owner_risk_acceptance` decision shall additionally contain:

- `owner_login`;
- immutable GitHub `owner_user_id`;
- `role: repository_owner`;
- `author_association: OWNER`;
- `disposition: accepted_for_working_draft`; and
- `qualified_review_status: deferred`.

Every owner-risk decision shall contain a `source` object with:

- `repository: tdistress/ESAF`;
- immutable GitHub `comment_url` and numeric `comment_id`;
- `author_login`, numeric `author_user_id`, and `author_association: OWNER`;
- RFC 3339 `created_at` and `updated_at`;
- `body_sha256` of the exact fetched UTF-8 comment body; and
- RFC 3339 `source_verified_at`.

The owner decision's `decided_at` shall equal `source.created_at`, and its UTC date shall equal the conditional publication date.
For every owner mapping or scope object, `owner_login` shall equal `source.author_login`, `owner_user_id` shall equal `source.author_user_id`, and every association field shall equal `OWNER`.

The complete-scope evidence object may use `approval_basis: owner_risk_acceptance` when it contains `sha: closure_head`, the same complete `source` object and owner identity fields, RFC 3339 `decided_at`, `scope: complete_git_tracked_repository`, Draft lifecycle, and exact `claims_not_made` set.

Every mapping decision and scope object shall equal `closure_head` in both `closure` and `taggable` phases. Only `merge_head` and `post_merge.sha` use the merged-main SHA domain; the enclosing `post_merge.sha` binds every command result in `post_merge.commands`. PR-A head evidence shall not satisfy or be rebound to the closure-head domain.

## Owner-source verification

The existing generic owner comment on merged PR A corroborates authenticated owner identity and intent only. It does not contain the structured decision required by this amendment and shall not be used as the substantive mapping or scope decision.

The exact closure PR head shall receive a new owner comment that:

- names all three mapping-set IDs;
- identifies `decision_type: owner_risk_acceptance`;
- names the exact closure SHA;
- records `disposition: accepted_for_working_draft`;
- states `qualified_review_status: deferred`;
- accepts the complete Git-tracked scope when scope approval is intended; and
- states every Draft and prohibited-claim limitation.

Before constructing external evidence, the controller shall fetch the live comment through GitHub and verify every `source` field, body digest, structured body content, and exact closure SHA. It shall re-fetch and compare the immutable source immediately before closure merge and again immediately before tag creation, update `source_verified_at` to the new verification time, and run the corresponding offline validation against that refreshed evidence. Any edit, deletion, author mismatch, association change, body-digest change, or structured-content mismatch shall invalidate the evidence. The live GitHub preflight and the offline structural validator are both required.

Steering Committee governance approval shall use a separate comment and evidence object.

## Publication and lifecycle behavior

Owner risk acceptance permits the closure workflow to continue; it does not close the deferred qualified-review work.

When `mapping_decision_basis` is `owner_risk_acceptance`, the readiness record, closure PR, final issue evidence, and tag message shall state:

- qualified mapping review was deferred;
- repository-owner risk acceptance was the publication basis;
- all mapping snapshots remain Draft; and
- publication makes no compliance, certification, equivalence, endorsement, external-scheme approval, assurance, production-readiness, or qualified-review claim.

For owner risk acceptance, the backlog shall retain qualified-review coverage for all three exact mapping-set IDs after `v0.4-alpha` publication, either as three items or one aggregate item enumerating all three. A later qualified review may replace the risk acceptance in a subsequent release, but shall not retroactively rewrite the evidence basis for `v0.4-alpha`.

When `mapping_decision_basis` is `qualified_approval`, the same artifacts shall state that qualified review was completed and shall reject owner-risk, deferred-review, or repository-owner-publication-basis claims. Backlog items may close only when their exact mapping-set coverage is completed.

Governance approval remains separate. This amendment does not change the requirement that publication approval under `GOVERNANCE.md` comes from the Steering Committee.

## Implementation boundaries

The implementation shall:

- extend `tools/release_gates.py` without weakening qualified-approval validation;
- add fail-first tests for both uniform decision bases;
- update the publication readiness record, release plan, backlog, and execution plan to distinguish deferred review from completed review;
- obtain the new exact-closure-head owner comment before constructing owner-risk evidence;
- preserve exact-SHA, check, merge-state, post-merge, governance, publication-date, and tag gates; and
- keep external evidence JSON outside the repository.

It shall not:

- treat the existing generic PR-A comment as substantive mapping or scope evidence;
- mark the mappings Reviewed or Approved;
- claim that the owner is a qualified Cyber Essentials reviewer;
- remove qualified-review backlog coverage when `mapping_decision_basis` is `owner_risk_acceptance`;
- change authoritative external-source or mapping-record content;
- weaken Steering Committee governance approval; or
- authorize a release or tag before every remaining gate passes.

## Testing and review

Tests shall run both uniform decision bases through the same closure and taggable mutation matrix.

They shall prove:

- qualified approval preserves its substantive reviewer, qualification, exact-SHA, disposition, source, and limitation checks under the v1 schema;
- exactly one owner risk-acceptance decision per expected mapping set passes for a Working Draft;
- mixed, missing, duplicate, or extra mapping decisions fail;
- owner acceptance fails for a non-owner identity, wrong association, wrong disposition, or completed qualified-review status;
- qualified approval fails when owner-risk, deferred-review, or repository-owner-basis language is present;
- owner risk acceptance fails when completed-qualified-review language is present;
- PR-A head evidence fails during closure and taggable validation;
- exact closure SHA, RFC 3339 timestamp, immutable HTTPS comment source, Draft lifecycle, and exact prohibited-claims set are mandatory;
- stale decision timestamps fail for both bases, and owner `decided_at` shall match the fetched comment `created_at`;
- scope acceptance covers only `complete_git_tracked_repository`;
- both bases fail for missing or failed GitHub checks, dirty or unmergeable PR state, wrong closure or merge SHA, missing or wrong governance authority, failed or missing post-merge commands, stale publication date, and head changes after approval;
- closure and taggable SHA domains remain distinct;
- governance remains Steering Committee-only;
- owner risk acceptance retains backlog coverage enumerating all three exact mapping-set IDs, while qualified approval permits those items to close or be removed only after evidence proves exact three-set completion and all deferred-review wording is removed; and
- final issue evidence and tag-message tests require the owner-risk basis, deferred-review statement, and complete prohibited-claims language when that basis is used, and reject that wording for qualified approval.

The closure candidate shall receive independent technical and editorial review on its exact head. For owner risk acceptance, reviewers shall verify that every publication statement identifies that basis accurately and does not imply qualified review or external assurance. For qualified approval, reviewers shall verify completed-review wording and the absence of owner-risk or deferred-review claims.

## Acceptance criteria

This amendment is complete when:

- the validator and tests implement both uniform decision bases without weakening any global gate;
- the tracked readiness, plan, backlog, and release language consistently follow the selected decision basis without cross-basis claims;
- when the selected basis is `owner_risk_acceptance`, a live verified owner comment on the exact closure head supplies the structured mapping and scope decision;
- when the selected basis is `qualified_approval`, exact-closure-head qualified evidence supplies all three mapping decisions and no owner-risk decision is required;
- exact-head technical and editorial reviews report zero unresolved Critical or Important findings;
- the closure PR, final issue evidence, and annotated tag message identify the selected basis, use its corresponding completed/deferred review wording, and state every applicable limitation; and
- all remaining governance, CI, merge, post-merge, publication-date, tag, and cleanup gates pass.
