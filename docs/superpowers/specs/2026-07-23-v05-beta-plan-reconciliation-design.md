# ESAF 0.5-Beta Plan Reconciliation Design

**Status:** Approved for implementation planning

**Date:** 2026-07-23

## 1. Purpose

Reconcile ESAF's durable project records with the completed `v0.4-alpha`
Working Draft publication and convert the broad `v0.5-beta` direction into a
bounded, schedulable milestone.

This change shall:

- preserve the immutable `v0.4-alpha` publication date, tag, evidence, mapping
  decision basis, and Draft lifecycle limitations;
- replace closure-candidate and current-date invariants with durable
  post-publication invariants;
- remove completed work from the backlog;
- define measurable `v0.5-beta` entry conditions, workstreams, exit criteria,
  dependencies, and non-goals; and
- restore GitHub Issues and a GitHub milestone as the authoritative scheduled
  queue.

## 2. Current state

The remote annotated tag `v0.4-alpha` exists and peels to
`8abfe5a85db19d11295a0c3debeb2d58109b0ca7`. GitHub issue `#39` is closed and
contains the publication evidence, including the tag object, exact reviewed and
merged commits, post-merge gates, renderer result, owner-risk basis, separate
governance approval, and Draft limitations.

The tracked planning state has not advanced with that event:

- `project/RELEASE_PLAN.md` still says the gates remain open;
- `project/BACKLOG.md` still lists publication-gate closure;
- the release-readiness record remains a `closure_candidate` with `ready`
  gates;
- release metadata tests require the publication date to equal the current UTC
  date and therefore fail after the publication day; and
- GitHub has no open issues, open pull requests, or milestones even though
  `project/BACKLOG.md` names GitHub Issues as authoritative.

The repository already contains early `v0.5-beta` work: the ESAF-1600 method
and three Draft UK Cyber Essentials mapping snapshots. Those snapshots were
published under repository-owner risk acceptance, not qualified mapping
review.

## 3. Selected approach

Use a bounded `v0.5-beta` redesign rather than a metadata-only correction or a
full roadmap rewrite.

The reconciliation will make the completed `v0.4-alpha` state durable, define
only the next beta milestone in detail, and leave the broader roadmap intact as
long-term direction. This avoids carrying stale release state forward without
prematurely committing every milestone through `v1.0`.

## 4. Post-publication record

The existing publication-readiness record shall become the durable
post-publication record for `v0.4-alpha`.

Its front matter shall:

- set `phase` to `published`;
- retain `release: 0.4-alpha`, `tag: v0.4-alpha`, issue `39`, the exact
  repository scope, the three mapping-set identifiers, and
  `mapping_decision_basis: owner_risk_acceptance`;
- retain `publication.date: 2026-07-23`;
- set `publication.condition` to
  `remote_annotated_tag_matches_exact_validated_commit`;
- add the immutable tag object
  `2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f`;
- add the peeled commit
  `8abfe5a85db19d11295a0c3debeb2d58109b0ca7`;
- add the consolidated evidence locator
  `https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764`; and
- set all eight gate states to `closed`.

The body shall state that the Working Draft was published, that the tag
condition was satisfied, and that the record does not convert Draft controls,
architectures, or mappings into reviewed, approved, certified, compliant,
equivalent, endorsed, assured, or production-ready artifacts.

Exact publication evidence may now be stored because the tag and evidence
already exist. The record shall not depend on the current date or a live
network request to validate.

## 5. Durable release validation

`tools/release_gates.py` shall distinguish an active closure candidate from a
published release record.

For `closure_candidate`:

- the existing exact-head, current-UTC-date, external-evidence, merge-state,
  and taggable-phase rules remain available for future use;
- a baseline reference remains mandatory.

For `published`:

- the publication date shall be a valid fixed date, not today's date;
- every gate shall be `closed` with at least one stable HTTPS evidence
  locator;
- the tag object and peeled commit shall be lowercase 40-character Git SHAs;
- the publication evidence locator shall use GitHub HTTPS and refer to issue
  `#39`;
- external closure or taggable evidence shall not be accepted as a substitute
  for the recorded published state; and
- a baseline reference shall not be required.

Repository tests shall resolve the tracked local annotated tag and require its
tag object and peeled commit to match the recorded values. This verifies the
checked-out repository state without requiring GitHub network access.

The tag, historical decision timestamps, and publication date shall never be
rewritten to make time-sensitive tests pass.

## 6. Release and changelog reconciliation

`project/RELEASE_PLAN.md` shall retain the generic seven release gates. Its
`0.4-alpha` section shall be rewritten as a closed publication record:

- all eight tracked readiness rows are `Closed`;
- the exact tag, peeled commit, and issue evidence are named;
- owner risk acceptance and deferred qualified review remain explicit;
- the separate Steering Committee approval remains explicit; and
- the section states that closure is historical and not a reusable approval
  for later releases.

`CHANGELOG.md` shall change the `0.4-alpha` heading from conditional to
published on `2026-07-23`. Its preamble shall distinguish the unreleased
`0.2-alpha` and `0.3-alpha` stages from the tagged `0.4-alpha` Working Draft.
The section shall record that the conditional tag requirement was satisfied.
Working Draft publication shall not be described as a stable release,
qualified mapping review, or external assurance.

`VERSION.md` and `ROADMAP.md` shall continue to identify `0.4-alpha` as the
current Working Draft until a later version is actually published. Planning
`v0.5-beta` does not advance current-version metadata.

## 7. Bounded 0.5-beta milestone

`project/MILESTONES.md` shall retain the high-level milestone table and add a
normative project-management subsection for `v0.5-beta`.

### 7.1 Entry state

- `v0.4-alpha` is published and its publication evidence is closed.
- ESAF-1600, its schemas, lifecycle model, and validators are present.
- The three UK mapping snapshots remain Draft and awaiting qualified review.

### 7.2 Required workstreams

1. **Qualified UK mapping review.** Complete independent, qualified human
   review of all three exact mapping-set snapshots. Core and Plus remain
   separate mapping sets, but the deferred assurance work is scheduled as one
   coordinated initiative.
2. **Minimum assessment foundation.** Define the common ESAF-1500 evidence
   model, assessment-result contract, and maturity scoring semantics needed by
   crosswalks and profiles. A workbook and full template library are not
   required for this milestone.
3. **Pilot profile.** Select, design, validate, and publish one Draft pilot
   industry or jurisdiction profile using a reusable profile contract. Profile
   selection is an explicit owner decision in the profile issue; it is not
   hard-coded by this reconciliation.
4. **PCI DSS readiness and mapping decision.** Pin the applicable official
   version and sources, establish publication-rights and provision-inventory
   boundaries, identify qualified review requirements, and record a mapping
   go/no-go decision. If the decision is `GO`, complete the approved Draft
   mapping scope. If it is `HOLD`, the milestone may close only when the
   blocking condition, reconsideration trigger, and non-claim boundary are
   recorded.
5. **Release closure.** Complete the ordinary release gates on the exact
   `v0.5-beta` candidate and record all counts and review results from the
   candidate rather than copying `v0.4-alpha` evidence.

### 7.3 Exit criteria

`v0.5-beta` is complete only when:

- all three UK mapping snapshots have qualified-review dispositions recorded
  under ESAF-1600;
- the minimum ESAF-1500 assessment foundation is internally consistent,
  linked from the applicable project and content indexes, and validated;
- one Draft pilot profile conforms to the reusable profile contract and uses
  the shared assessment semantics;
- the PCI DSS workstream has reached its approved `GO` deliverable or a
  formally evidenced `HOLD` disposition;
- generated catalogs and all affected traceability records are current;
- the full test suite, control, architecture, crosswalk, link, release,
  working-tree, and applicable Mermaid-rendering gates pass on the exact
  candidate;
- Critical and Important review findings are resolved; and
- the exact candidate receives technical, editorial, mapping, and governance
  approval appropriate to its contents.

### 7.4 Non-goals

`v0.5-beta` does not require:

- all roadmap crosswalks;
- all nine planned profiles;
- a complete assessment workbook, audit checklist, or governance-template
  library;
- a substantive HITRUST CSF mapping without licensed-source access,
  publication-rights confirmation, and qualified-review availability;
- advancing Draft controls, architectures, mappings, or profiles to an
  approved lifecycle state without their own evidence; or
- redesigning milestones `v0.9-rc1` and `v1.0`.

## 8. Backlog and roadmap

`project/BACKLOG.md` shall:

- remove the completed `0.4-alpha` gate item;
- replace the duplicate core and aggregate qualified-review bullets with one
  coordinated initiative containing all three exact mapping-set identifiers;
- list the assessment foundation, pilot profile, and PCI DSS decision in
  dependency order; and
- retain HITRUST CSF as a separately gated later initiative whose entry
  conditions are licensed-source access, publication rights, and qualified
  review availability.

`ROADMAP.md` shall remain the long-term capability roadmap. It shall add a short
delivery-sequence note explaining that the `v0.5-beta` tranche closes existing
mapping assurance debt, establishes minimum shared assessment semantics,
validates one pilot profile, and then expands priority mappings. The full
crosswalk and profile lists remain future direction, not `v0.5-beta` exit
criteria.

## 9. Authoritative GitHub queue

After the planning changes merge, create a GitHub milestone named
`v0.5-beta`. Do not assign a due date without an owner-approved schedule.

Create these milestone issues:

1. `Complete qualified review of the three UK mapping snapshots`
   - label: `crosswalk`
   - priority: `priority:critical`
2. `Define the minimum ESAF-1500 assessment foundation`
   - label: `assessment`
   - priority: `priority:high`
3. `Select and publish one Draft pilot ESAF industry profile`
   - label: `profile`
   - priority: `priority:high`
4. `Complete PCI DSS source readiness and mapping go/no-go`
   - label: `crosswalk`
   - priority: `priority:high`
5. `Close the v0.5-beta publication gates`
   - label: `governance`
   - priority: `priority:high`

Create one unmilestoned backlog issue:

6. `Establish HITRUST CSF source and review readiness`
   - label: `crosswalk`
   - priority: `priority:medium`

Each issue shall state its dependencies, exact deliverables, acceptance
criteria, required review disciplines, lifecycle limitations, and applicable
validation gates. The release-closure issue depends on the four milestone
content issues. The profile issue depends on the minimum assessment
foundation. The PCI DSS issue may proceed through source inventory in parallel
but shall not publish mapping records before its go/no-go decision.

The milestone and issues shall be created only after the repository planning
records merge, so GitHub links can reference the authoritative merged text.

## 10. Test strategy

Use test-driven development for changed invariants.

Focused release-metadata tests shall first fail for the current stale state and
then verify:

- the fixed published date rather than the current date;
- an unconditional dated changelog heading for `0.4-alpha`;
- a published phase with eight closed gates;
- the exact tag object, peeled commit, and evidence URL;
- local tag resolution to the recorded values;
- the closed release-plan wording;
- removal of completed backlog work;
- one coordinated qualified-review backlog item with all three identifiers;
- bounded `v0.5-beta` entry state, workstreams, exit criteria, and non-goals;
- the assessment-before-profile dependency;
- the conditional PCI DSS `GO` or evidenced `HOLD` boundary; and
- the HITRUST readiness gate.

Focused release-gate tests shall verify both valid and invalid published
records, including wrong dates, tag identifiers, evidence locators, open gates,
and inappropriate baseline or external-evidence requirements.

The complete validation set is:

```text
python -m unittest tests.test_release_metadata -v
python -m unittest tests.test_release_gates -v
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
git diff --check <merge-base>..HEAD
```

Set `PYTHONDONTWRITEBYTECODE=1`, verify no `__pycache__` directories remain,
and verify a clean worktree after commits.

No Mermaid source is expected to change. If implementation changes or adds a
Mermaid block, every affected block shall be rendered with the current Mermaid
CLI and reviewed for readability.

## 11. Review and publication workflow

Implementation shall use the existing isolated branch and worktree workflow.
The completed branch shall receive:

- independent specification review against this design;
- independent whole-branch review for planning consistency, overclaiming, and
  lifecycle boundaries;
- the full repository validation set;
- a reviewable pull request whose description records the reviewed head SHA
  and exact gate results; and
- verification that the reviewed head remains the PR head before merge.

After merge, update local `main`, rerun proportional validation, create the
GitHub milestone and issues from the merged plan, verify their labels and
milestone assignments, and remove only the owned planning branch and worktree.
Unrelated existing worktrees and branches shall not be removed.
