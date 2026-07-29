# v0.5-beta publication closure design

## Purpose

This design closes issue 59 by publishing `v0.5-beta` as a Working Draft on
one exact candidate. It preserves the Draft lifecycle state of controls,
architectures, profiles, and mappings. It also keeps issue 55 open when the
release uses owner-risk acceptance instead of completed qualified review.

The release shall use evidence created for `v0.5-beta`. Historical
`v0.4-alpha` approvals, reviews, validation results, and owner-risk evidence
shall not approve this release.

## Verified starting state

The release starts from merged `main` commit
`b9a6e63993bf9cf546e5d716d41c037c3eeb26db`.

The milestone content dependencies are complete:

- issue 56 completed the ESAF-1500 assessment foundation through merge commit
  `9715ddcd59eac0a92c72cf748db869e50f39359b`;
- issue 57 completed the Draft UK pilot profile through merge commit
  `30708a4337d8aff1dfbf30f9b7b9cf9d0a857edf`; and
- issue 58 recorded the approved PCI DSS `HOLD` decision through merge commit
  `f61edcad85bb32f64328484ee973e6f64203597e`.

Issue 55 remains open. No qualified-review campaign has completed all six
human roles, and no live `v0.5-beta` owner-risk decision exists. `VERSION.md`
still identifies `0.4-alpha`, and no `v0.5-beta` tag exists.

## Chosen architecture

The published `v0.4-alpha` validator and readiness record are historical
evidence. They shall remain intact.

The implementation shall add a release-specific `v0.5-beta` controller and
live evidence collector:

- `tools/v05_beta_release_gates.py`
- `tools/v05_beta_release_evidence.py`
- `tests/test_v05_beta_release_gates.py`
- `tests/test_v05_beta_release_evidence.py`
- `docs/superpowers/reviews/2026-07-27-v05-beta-publication-readiness.md`
- `docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md`

The new tools may reuse stable parsing, identifier, and evidence vocabulary
from the v0.4 modules. They shall not retarget the v0.4 record, tag, issue,
fixed publication values, or historical validation behavior.

The repository workflow shall run both release validators. A change that
breaks the frozen v0.4 publication record or the active v0.5 contract shall
fail CI.

## Alternatives considered

### Retarget the v0.4 validator

Changing `tools/release_gates.py` to validate only `v0.5-beta` would remove
durable validation of the published `v0.4-alpha` evidence. This approach is
rejected.

### Build a generic multi-release framework

A data-driven release framework could support future releases, but it would
refactor the most security-sensitive publication code during an active
release. The repository has only one historical record and one active
candidate. This approach is deferred until another release requires it.

### Add a v0.5-specific controller

This is the selected approach. It keeps the historical contract stable,
allows stronger v0.5 requirements, and limits the change to the current
milestone.

## Release sequence

### Stage 1: evidence and tooling

The first pull request shall:

- add the v0.5 release controller, live evidence collector, and mutation tests;
- add a v0.5 readiness record in `evidence_candidate` phase;
- add a baseline renderer-capability and Mermaid inventory record that makes no
  candidate-approval claim;
- wire both v0.4 and v0.5 validators into CI;
- document the module invocation
  `python -m tools.v05_beta_release_evidence`;
- add an unreleased `v0.5-beta` changelog section; and
- leave the current release metadata and issue state unchanged.

This stage proves that the repository can construct and reject v0.5 release
evidence. It does not create an exact closure candidate, acquire owner or
governance approval, approve candidate rendering, publish, tag, or close issue
59.

### Stage 2: exact closure candidate

After Stage 1 merges and post-merge validation passes, a fresh closure branch
shall update only release metadata and evidence-bound publication files:

- `VERSION.md`
- `README.md`
- `ROADMAP.md`
- `CHANGELOG.md`
- `project/RELEASE_PLAN.md`
- the v0.5 readiness record

Tests shall enforce this allowlist. The closure branch shall not change
normative content, assessment content, profile content, crosswalk records,
schemas, validators, generated catalogs, or Mermaid source.

The branch head after these changes is the closure candidate. Candidate-bound
Mermaid inventory and visual-review evidence shall be acquired externally
after this head exists. The reviewer may rely on the Stage 1 baseline only
after proving that every Mermaid source path and digest is identical on the
closure head, rendering every block again, and recording a fresh exact-head
visual disposition.

Any later commit
invalidates candidate-bound reviews, decisions, GitHub checks, rendering
evidence, and inventories. Changed evidence shall be reacquired against the
new head.

### Stage 3: merge, tag, and durable publication evidence

After every non-post-merge closure gate is `ready`, the post-merge gate is
`open`, and all required pre-merge evidence validates:

1. fetch all external evidence again and compare source identities, timestamps,
   bodies, and digests;
2. merge the clean closure pull request;
3. require the merged tree to equal the reviewed closure-head tree;
4. run the full post-merge command set on merged `main`;
5. rebuild taggable evidence from freshly fetched sources;
6. verify that no local or remote `v0.5-beta` tag exists;
7. generate the canonical UTF-8/LF tag message outside Git storage, create an
   annotated `v0.5-beta` tag that peels to the validated merge commit, and
   validate the actual tag object message before push;
8. verify the remote tag object and peeled commit;
9. post one consolidated evidence comment to issue 59; and
10. close issue 59 only after the tag and evidence comment are verified.

A later publication-record pull request shall record the fixed tag object,
peeled commit, evidence locator, and closed gate states. Backlog and milestone
text may move issue 59 to completed only after publication truth exists.

## v0.5 readiness record

The authoritative Markdown front matter shall identify:

- release `0.5-beta`;
- tag `v0.5-beta`;
- issue `59`;
- repository scope `complete_git_tracked_repository`;
- phase `evidence_candidate`, `closure_candidate`, or `published`;
- the conditional annotated-tag publication rule;
- the exact three UK mapping-set identifiers;
- the selected uniform mapping-decision basis;
- all required gates and their evidence locators; and
- fixed publication data only after the remote tag exists.

Candidate records shall keep the publication date null and shall omit tag
identity. Published records shall record the UTC tag-operation date, annotated
tag object, peeled tagged commit, and issue 59 evidence-comment URL. The local
annotated tag object, peel, and UTC tagger date shall match those published
fields. Its message shall exactly match the production-owned canonical
contract: Working Draft, owner-risk permission for Working Draft publication
only, deferred qualified review, issue 55 open, all mappings Draft, no artifact
lifecycle approval, and the complete required nonclaim set. A later
`published`-phase edit may use the published record as its baseline only when
the immutable publication identity and closed-gate truth are unchanged.

Gate states shall follow these exact phase rules:

- `evidence_candidate`: every gate is `open`;
- `closure_candidate`: every gate except `post_merge` is `ready`, and
  `post_merge` is `open`; and
- `published`: every gate is `closed`.

Taggable external evidence may satisfy the operational post-merge gate while
the tracked closure record remains conditional. The later durable publication
record changes the tracked gate to `closed` only after tag verification.

The body shall record exact candidate-derived counts. At the starting commit,
the repository contains 91 controls in 16 families, 7 architecture patterns,
3 Draft mapping sets, 404 mapping provisions, 81 relationship legs, and 325
negative dispositions. The implementation shall recompute these values from
the candidate and shall fail if the record contains stale totals.

The scope contract shall also prove:

- the ESAF-1500 foundation is present and validates;
- exactly one Draft pilot profile is published under the reusable profile
  contract; and
- the PCI DSS readiness artifact records the approved `HOLD` decision and its
  nonclaim boundary.

## Candidate gates

The v0.5 controller shall require these candidate-bound gates:

- scope and milestone;
- technical;
- editorial;
- terminology;
- cross-reference and rendering;
- standards mapping;
- profile scope;
- release metadata;
- governance; and
- post-merge.

The external closure evidence shall contain exact keys for:

- `closure_head` and `closure_tree`;
- derived scope inventory and counts;
- technical, editorial, terminology, rendering, profile-scope, and governance
  verdicts;
- security/overclaiming and whole-range verdicts;
- candidate validation commands;
- mapping decision schema, basis, and decisions;
- the required GitHub check; and
- clean merge state.

Every verdict shall include its exact SHA, reviewer or approver identity,
role or authority, disposition, date, stable HTTPS locator, source comment
identifier, immutable author identifier, association, timestamps, body
SHA-256, and source-verification timestamp. Critical and Important findings
shall both equal zero.

The governance verdict shall name the Steering Committee authority. Repository
ownership alone shall not satisfy governance. The repository has no
machine-readable Steering Committee membership registry, so the controller
shall treat institutional authority as a manual gate. The approver shall
expressly attest that they are authorized to approve this publication under
`GOVERNANCE.md`. The live evidence collector shall verify the exact comment
source and immutable identity but shall not claim to prove institutional
membership. Publication shall stop unless the release operator records the
manual authority determination in the closure evidence.

Taggable evidence shall retain the closure-head evidence and add:

- `merge_head` and `merge_tree`;
- proof that `merge_tree` equals `closure_tree`; and
- the complete post-merge command results constructed from canonical execution
  in a detached, tree-verified `merge_head` worktree; and
- a separately fetched authenticated post-merge rendering verdict bound to the
  exact merge head and tree.

A merge tree difference invalidates the candidate. The release shall return to
Stage 2 with fresh reviews, decisions, checks, and evidence.

## Mapping assurance

The release shall select exactly one mapping basis for all three mapping sets.
Mixed bases shall fail.

### Qualified approval

The qualified path shall require the existing campaign validator to report:

- `evidence_valid: true`;
- `readiness_name: transition_ready`;
- candidate state `draft`;
- the exact closure candidate;
- all three mapping sets; and
- both `specification_and_inventory` and `security_and_overclaiming` roles for
  each set.

`transition_ready` records completed qualified review of the exact Draft
candidate without performing a lifecycle transition. `merge_ready` applies
only to the separate final confirmation of an already transitioned `reviewed`
candidate and is outside this Working Draft release. Synthetic approval
objects without the validated six-role Draft campaign shall fail.

### Owner-risk acceptance

The deferred path requires an authenticated repository-owner decision created
after the exact closure candidate exists. Standing authorization to perform
repository work shall not be treated as this substantive risk decision.

The owner decision shall contain:

- `mapping_decision_basis: owner_risk_acceptance`;
- `decision_type: owner_risk_acceptance`;
- `qualified_review_status: deferred`;
- the exact closure candidate SHA;
- each exact mapping-set identifier once;
- the six missing qualified-human role entries, consisting of both required
  roles for each mapping set;
- the accountable owner, matching the authenticated GitHub author;
- the required limitations and nonclaims;
- issue 55 as the continuing qualified-review work item; and
- the complete re-entry and invalidation triggers.

All three decisions shall use one unchanged owner source. Edited comments,
changed source digests, duplicate or missing mapping sets, stale SHAs,
non-owner associations, or inconsistent identities shall fail.

The mapping-risk decision does not supply scope approval. Scope and milestone
approval shall be an express, separately typed decision, even if the same
authenticated owner records both in one comment.

The owner decision cannot be inferred or drafted into effect by automation.
Automation may prepare exact text, fetch the resulting GitHub source, compare
its digest, and construct evidence only after the owner expressly accepts it
for the named candidate.

## Deferred-path limitations

All three mapping sets and all mapping records shall remain `draft`. Their
review-event arrays, reviewer metadata, approval fields, and lifecycle state
shall remain unchanged.

Owner-risk acceptance permits Working Draft publication only. It shall state
that it:

- does not complete qualified review;
- does not approve or transition the mappings;
- does not establish qualified mapping approval, artifact-lifecycle approval,
  certification, compliance, equivalence, endorsement, external-scheme
  approval, production readiness, or assurance;
- does not establish implementation assessment or legal sufficiency;
- does not replace qualified professional judgment; and
- leaves issue 55 open.

Separate governance approval authorizes publication of the Working Draft. It
shall not be described as mapping approval or artifact-lifecycle approval.

## Re-entry and invalidation

The deferred decision shall expire or require re-entry when:

- an eligible qualified reviewer becomes available;
- a mapping record, pinned source, inventory, manifest, catalog, or reviewed
  candidate changes;
- the owner decision expires, is withdrawn, is edited, or is superseded;
- the accountable owner requires earlier completion; or
- the closure candidate or merged tree changes.

A later mapping lifecycle transition still requires the existing two-stage
qualified-review campaign, signed exact-SHA evidence, owner acceptance of
reviewer eligibility and any dual-role arrangement, resolution of all Critical
and Important findings, metadata and catalog regeneration, and every ESAF-1600
transition condition.

## Validation command contract

Candidate and post-merge validation shall run with
`PYTHONDONTWRITEBYTECODE=1` and record nonempty successful results for:

- the full unit-test suite;
- assessment validation;
- profile validation;
- control validation;
- architecture validation;
- control-mapping migration validation;
- current crosswalk validation;
- baseline crosswalk validation;
- PCI DSS decision rendering validation;
- link validation;
- frozen v0.4 release validation;
- v0.5 release validation;
- Mermaid inventory validation;
- rendering and visual review of every Mermaid block;
- whole-range `git diff --check`;
- zero generated Python caches; and
- clean working-tree status.

The command vocabulary shall be exact. Missing, duplicate, unknown, pending,
or failed commands shall fail.

All Mermaid blocks shall render with the pinned current Mermaid CLI. Inventory
equality cannot substitute for visual review.

## GitHub and source handling

CI, pull-request head, review comments, merge state, owner decisions,
governance decisions, merged commit, and tag state shall be fetched live.
Plausible local JSON does not establish external state.

`tools/v05_beta_release_evidence.py` shall own the online acquisition boundary.
It shall invoke authenticated `gh api` requests for the fixed repository
`tdistress/ESAF` and exact configured issue, pull request, comment, Actions,
and Git-reference identifiers. It shall reject a different repository,
redirected item, missing authentication, incomplete pagination, pending check,
or API failure.

The live collector shall parse structured decisions and verdicts only from
the exact fetched comment bodies. It shall derive body digests, identities,
timestamps, findings, dispositions, SHAs, roles, and authority attestations
itself. Caller-supplied derived verdicts, checks, merge state, identities,
digests, or tag state shall not be accepted by the operational CLI.

The implementation shall separate an injectable fetch adapter used by unit
tests from the production `gh api` adapter. Tests may supply fixtures through
that internal interface. The release command shall have no option that
converts arbitrary local snapshots into live closure evidence.

Every acquisition shall record the fixed repository, API resource identifiers,
retrieval timestamp, authenticated login, complete page count, and the exact
response-body digest used to derive evidence. The release gates shall require
the acquisition manifest and bind every derived object to one of its resources.

Each acquired resource shall carry its own retrieval timestamp and shall be
fresh for no more than 15 minutes at final evidence construction. A newer
manifest timestamp shall not mask an older resource. Every source-verification
timestamp shall equal its bound resource's retrieval timestamp. Taggable
construction shall re-fetch the complete closure source set rather than reuse a
closure manifest. Decision and verdict comments may have older creation dates
when they remain unchanged, but each shall have been created after the fetched
closure commit and shall bind the exact closure SHA. Each verdict date shall
equal its own authenticated comment creation date. Candidate records have no
publication date; the publication date is derived immediately from the UTC tag
operation. All timestamps shall be RFC 3339 UTC values.

Issue 55 shall be fetched as the canonical `tdistress/ESAF` issue during both
closure and taggable construction. It shall remain open and shall not be a pull
request. `Validate ESAF sources` shall be produced by the GitHub Actions app
and bind a fetched canonical Actions run for
`.github/workflows/catalog-validation.yml`, workflow name
`Repository validation`, the exact closure head, successful conclusion, and
the fixed repository.

Each fetched comment shall preserve:

- repository;
- comment URL and numeric identifier;
- author login and immutable numeric user identifier;
- author association;
- creation and update timestamps;
- exact body SHA-256; and
- verification timestamp.

Comment acquisition shall bind both `html_url` and `issue_url` to an explicit
container type and number. Closure owner, review, and governance comments shall
belong to the closure pull request. The post-merge rendering verdict shall
belong to issue 59; a pull-request comment with the same comment identifier
shall not substitute for it.

Independent of collector checks, release-gate validation shall derive exactly
one closure pull-request number from the canonical acquired pull resource and
require every closure decision and verdict source to use that pull container.
Taggable validation shall require the post-merge rendering source and command
review URL to use issue 59 exactly. Missing, multiple, cross-container, or
internally consistent substitute resources shall fail closed.

Sources shall be fetched immediately before evidence construction, immediately
before merge, and immediately before tag creation. A changed field stops the
release.

External validation shall bind the evidence to local Git: `HEAD` shall equal
the phase's expected head, the expected-head tree shall equal the recorded
closure tree, the recorded closure base shall exactly equal the supplied
baseline SHA, and that baseline shall be the exact merge base. In taggable
phase the expected head is the merge head and merge-tree equality preserves the
reviewed closure tree.

The current v0.4 owner-risk helper works when invoked as a module but fails as
a direct script in this checkout because its package import cannot resolve.
The v0.5 documentation and automation shall use module invocation and test it.

## Testing

Implementation shall follow test-driven development. Mutation tests shall
cover:

- v0.4 historical behavior remaining unchanged;
- wrong release, tag, issue, phase, or record path;
- stale or self-referential candidate SHAs;
- closure and merge tree mismatch;
- missing, extra, duplicate, pending, or failed commands;
- missing assessment, profile, PCI, or renderer gates;
- incomplete scope inventory or stale derived counts;
- missing terminology or profile-scope verdicts;
- absent source identity or body-digest fields on any verdict;
- missing, redirected, incomplete, stale, unauthenticated, or caller-derived
  live-source acquisition;
- owner source edits or identity changes;
- mixed mapping bases;
- missing or duplicate mapping-set decisions;
- fewer or more than six missing human-role entries;
- owner-risk wording that implies qualified review or approval;
- qualified approval without a valid six-role campaign;
- changed Draft lifecycle state or mapping metadata;
- missing nonclaims or re-entry triggers;
- pre-existing local or remote tag state; and
- publication wording that exceeds the Working Draft boundary.

Focused tests, the full suite, all repository validators, exact Mermaid
rendering, whole-branch diff review, and clean-worktree checks shall pass on
the exact reviewed head. Any candidate-head change requires rerunning the
affected gates and exact-SHA reviews.

## Human boundary

Automation can complete the tooling, readiness record, candidate construction,
validation, review coordination, evidence templates, and source verification.
It cannot originate the owner-risk decision or Steering Committee approval.

When the exact closure candidate exists, the release pauses until the owner
expressly records both the owner-risk disposition and scope approval, and the
authorized governance approver records the separate publication disposition.
No tag or publication statement may precede those decisions.

The governance approver's institutional authority remains a disclosed manual
determination because this repository has no authoritative membership
registry. The automated evidence shall preserve the attestation and source
identity without representing that limitation as machine-verified authority.
