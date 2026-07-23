# ESAF 0.4-Alpha Publication-Gate Closure Design

**Status:** Approved design

**Target release:** 0.4-alpha

**Design date:** 2026-07-21

## 1. Purpose

Close GitHub issue #39 and publish the repository's current 0.4-alpha
working-draft milestone without promoting any Draft architecture, control, or
mapping artifact beyond its existing lifecycle state. Publication shall mean
that an exact repository snapshot has completed the release gates. It shall not
mean that every artifact is approved, conformant, certified, equivalent to an
external standard, or ready for production adoption.

## 2. Current state

`main` identifies version 0.4-alpha as an unreleased Working Draft at the
Initial Reference Architecture Draft Library stage. It contains the complete
seven-pattern Draft architecture library, 91 Draft controls across 16 families,
and three Draft mapping snapshots: Cyber Essentials v3.3, Cyber Essentials Plus
v3.2 `esaf_to_external`, and Cyber Essentials Plus v3.2 `external_to_esaf`.

The repository has deterministic control, architecture, migration, crosswalk,
and link validators. It does not yet have one release-scope record, an
exhaustive exact-SHA Mermaid-rendering record, consolidated editorial and
terminology review, qualified review of every in-scope mapping snapshot,
governance approval of an exact release candidate, or post-merge evidence tied
to the commit that would be tagged. All readiness rows in
`project/RELEASE_PLAN.md` therefore remain Open.

## 3. Decision

Use a two-pull-request release sequence followed by external post-merge
evidence and an annotated tag.

1. **Evidence candidate PR.** Freeze the complete release scope, synchronize
   candidate metadata, create a durable gate ledger, render and inspect every
   Mermaid block, and complete technical, normative, editorial, terminology,
   cross-reference, link, and mapping reviews on one exact PR-head SHA.
2. **Closure PR.** After the evidence candidate merges and its resulting
   `main` commit passes post-merge validation, create an evidence-only closure
   candidate. Reconcile the release ledger and readiness states, perform all
   affected exact-head gates and reviews again, obtain explicit governance
   approval on the exact closure PR head, and merge without changing the
   approved release content.
3. **Publication action.** Validate the resulting closure merge commit, record
   the exact post-merge evidence in GitHub issue #39 and the annotated tag,
   create tag `v0.4-alpha` on that exact commit, verify the remote tag, and
   close issue #39. No tracked change may occur between the final validation
   and tag creation.

The GitHub issue, pull-request reviews and comments, checks, and annotated tag
are the authoritative non-self-referential evidence for exact candidate,
merge, and tag SHAs. Tracked records shall describe the evidence contract,
review identities, commands, results, counts, and stable GitHub locators, but
shall not claim a commit contains its own hash.

## 4. Release scope and lifecycle boundary

The evidence candidate shall include the complete tracked repository at its
frozen head. The release scope is not limited to files added since the prior
planning reconciliation. It includes the three strategic pillars, normative
standards content, controls, architecture library, all three mapping snapshots,
assessment and implementation material, templates, governance documents,
generated catalogs, validators, and repository automation present at that
head.

Publication shall preserve these boundaries:

- `VERSION.md` remains `0.4-alpha` and `Working Draft`.
- Architecture patterns remain `Draft`.
- Controls and mapping snapshots retain their existing Draft states and
  lifecycle histories.
- No mapping relationship becomes an equivalence, compliance, certification,
  endorsement, assurance, or scheme-outcome claim.
- Cyber Essentials core and Cyber Essentials Plus remain separate,
  source-versioned mapping sets.
- The release is an immutable working-draft snapshot, not promotion to
  `0.5-beta`, `0.9-rc`, or `1.0`.

## 5. Evidence candidate

### 5.1 Candidate-owned artifacts

The first PR shall add a release-scope and gate-traceability record under
`docs/superpowers/reviews/` and update only metadata necessary to make the
candidate internally coherent. At minimum, the record shall identify:

- the version, stage, release scope, and explicit exclusions;
- the merge base and the rule for recording the reviewed PR head externally;
- every applicable gate and its evidence owner;
- all in-scope mapping-set identifiers, source versions, lifecycle states, and
  derived counts;
- the complete Mermaid inventory and renderer/readability evidence method;
- the exact validation commands and result-recording format;
- independent reviewer roles, qualifications, and independence constraints;
- Critical and Important finding closure rules; and
- the rule that any candidate-byte change invalidates prior exact-head review
  and requires affected gates to be rerun.

The changelog shall describe all material content included in 0.4-alpha,
including both Cyber Essentials Plus direction-specific Draft snapshots. It
shall remain `Unreleased` in the evidence candidate. The backlog shall continue
to name only work that remains after publication closure.

### 5.2 Mermaid rendering

Every tracked Markdown Mermaid block shall be inventoried by source path,
one-based block index, source digest, diagram type, render result, and
readability disposition. Rendering shall use the repository-selected Mermaid
CLI version pinned for the candidate. Rendered files shall be created in a
temporary directory and shall not be committed unless a separate publication
artifact requirement is approved.

Successful parsing alone is insufficient. A reviewer shall inspect every
render for clipped labels, unreadable density, missing nodes or edges, unsafe
contrast, and correspondence with its numbered figure and surrounding prose.
Any source correction changes the candidate and resets the affected technical,
editorial, rendering, and whole-branch review evidence.

### 5.3 Reviews

The frozen evidence candidate shall receive separate reviews for:

- normative and technical integrity;
- editorial conventions, terminology, and internal consistency;
- global links, cross-references, and generated-content coherence;
- architecture diagrams and Mermaid readability; and
- all three mapping snapshots by qualified contributors with authority to
  evaluate the mapped external schemes and the ESAF requirements.

Automated validators and Codex reviewers may supply technical evidence but do
not manufacture human qualifications or governance authority. Qualified
mapping and governance approvals shall identify the approving person or role,
the exact SHA, scope, date, disposition, and any limitations in GitHub evidence.

## 6. Closure candidate and publication

After the first PR merges, the resulting `main` SHA shall pass the full suite,
all validators, renderer inventory comparison, cache check, and clean-worktree
check. Those results shall be posted to the evidence PR or issue #39 before the
closure branch is created.

The closure PR shall be evidence-only. It may update the gate ledger,
`project/RELEASE_PLAN.md`, the changelog's release-state convention and
0.4-alpha heading, and focused release-metadata tests. The heading shall record
the intended UTC publication date and state that publication is effective only
when remote annotated tag `v0.4-alpha` resolves to the exact commit containing
that statement. The changelog introduction shall define this conditional form
as not released until the tag condition is satisfied. Before the tag exists the
candidate therefore makes no publication claim; after the verified tag exists
the immutable tagged snapshot describes its state accurately. The closure PR
shall not change normative requirements, controls, architecture content,
mapping records, diagram sources, schemas, validators, or generated catalogs.
If a substantive defect is discovered, closure stops and the work returns to a
new evidence candidate.

The tag shall be created on the recorded intended UTC publication date. If the
post-merge gates cannot complete on that date, publication stops, the date is
updated in a new closure candidate, and every invalidated exact-head approval
and check is rerun before another merge attempt.

The closure candidate shall identify pre-merge gates as closed only when their
exact evidence exists. Its post-merge gate shall remain an explicit release
condition whose authoritative completion is recorded outside the commit in
issue #39 and the annotated tag. A person authorized to grant publication
approval under `GOVERNANCE.md` shall approve the exact closure PR-head SHA for
scope and governance after all other applicable gates pass. Repository
ownership alone shall not be treated as proof of that governance role. Any
subsequent tracked change invalidates the approval.

Qualified mapping reviewers shall also approve or explicitly reaffirm the
exact closure PR-head SHA. When the closure diff changes no mapping-controlled
bytes, the reaffirmation may rely on verified digests that prove the three
mapping snapshots, their sources, lifecycle registries, manifests, schemas,
validators, and generated catalogs are byte-identical to the substantively
reviewed evidence candidate. The approval shall still name the closure SHA,
reviewer qualification, scope, date, and disposition. Any tracked change after
that reaffirmation invalidates it.

After the closure PR merges:

1. fetch and verify the exact merge commit on local `main` and `origin/main`;
2. rerun the full suite and every required validator with bytecode caches
   disabled;
3. render the complete Mermaid inventory again or prove digest identity with
   the reviewed inventory and rerender any changed block;
4. verify repository cleanliness, zero generated caches, and no unexpected
   output;
5. post the commands, counts, exact merge SHA, and dispositions to issue #39;
6. create annotated tag `v0.4-alpha` on that exact SHA with the evidence
   locator and lifecycle limitations;
7. push and independently resolve the remote tag target; and
8. close issue #39 only after the remote tag and evidence agree.

The annotated tag and issue evidence are the publication event. Immediately
before tag creation, the changelog's explicit tag condition remains false and
the snapshot remains unpublished. Once the remote annotated tag is independently
resolved to the exact validated commit, the condition becomes true and the
tagged snapshot's intended UTC publication date becomes effective. No later
tracked reconciliation is required to make the immutable tagged commit
internally accurate, and the tag shall never be moved or recreated.

## 7. State and evidence model

Each gate has one of four states:

- **Open:** required evidence does not yet exist.
- **In review:** a frozen candidate exists, but one or more required verdicts
  are pending.
- **Ready:** all preconditions exist for the next irreversible action, but that
  action has not occurred.
- **Closed:** the required evidence exists for the exact relevant SHA and no
  invalidating change has occurred.

No gate may transition directly from Open to Closed without its required
evidence. A failed command, missing reviewer qualification, unresolved Critical
or Important finding, changed candidate SHA, failed or pending GitHub check,
unclean merge state, mismatched remote ref, or Mermaid parse/readability defect
returns the affected gate to Open or In review. Lower-severity findings may be
accepted only with a recorded rationale and owner.

## 8. Testing and validation

Release-metadata tests shall be developed test-first and shall enforce:

- exact version, stage, changelog, roadmap, and backlog synchronization;
- the conditional changelog form, intended UTC date, exact tag name, and rule
  that publication is false until the remote tag resolves to the tagged commit;
- the complete release-scope inventory and three mapping-set boundary;
- the four-state gate vocabulary and legal transitions;
- required evidence fields for each Closed gate;
- preservation of Draft lifecycle states and prohibited mapping inferences;
- prohibition on tagging or release representation while a required gate is
  Open, In review, or Ready;
- the evidence-only path allowlist for the closure PR; and
- the non-self-referential exact-SHA evidence boundary.

Each candidate shall run, at minimum:

- focused release tests;
- `python -m unittest discover -s tests -v`;
- `python tools/validate_controls.py --check`;
- `python tools/validate_architectures.py`;
- `python tools/migrate_control_mappings.py --check`;
- `python tools/validate_crosswalks.py --check` and its required baseline mode;
- `python tools/validate_links.py --check`;
- every Mermaid render and readability review;
- `git diff --check <merge-base>..HEAD`;
- placeholder, cache, unexpected-output, and worktree-cleanliness checks; and
- independent review of the complete branch range, not only the latest commit.

The PR description shall record the reviewed head, exact results, reviewer
identities and dispositions, and GitHub check/merge state. Prior results shall
not be reused after candidate bytes change.

## 9. Alternatives considered

### 9.1 Single PR with GitHub-only evidence

Rejected because it combines content synchronization, gate-state transition,
and publication approval before post-merge evidence exists. It is simpler but
makes premature closure and stale exact-head claims easier.

### 9.2 Evidence package without publication

Rejected as the terminal design because it would improve readiness while
leaving issue #39 and the documented release gates open. It remains the safe
fallback if qualified review or governance approval is withheld.

### 9.3 Two PRs plus external post-merge evidence

Selected because it separates substantive candidate bytes from evidence-only
closure, preserves exact-SHA review, and records the necessarily
non-self-referential merge and tag facts in GitHub and the annotated tag.

## 10. Out of scope

- Promotion of any Draft artifact.
- New normative requirements, controls, architecture patterns, mappings,
  profiles, assessment methods, or implementation guidance.
- Rewriting diagrams for cosmetic preference when they already render and are
  readable.
- Claiming external certification, compliance, equivalence, endorsement, or
  official scheme approval.
- Beginning 0.5-beta content work before publication closure is complete.
- Publishing generated PDF, Word, spreadsheet, or website artifacts unless
  separately authorized.

## 11. Acceptance criteria

The milestone is complete only when:

- both PRs are merged from independently reviewed exact heads;
- all applicable gate evidence is complete and contains no unresolved Critical
  or Important finding;
- every Mermaid block renders and has a recorded readability disposition;
- all three mapping snapshots have qualified approval or digest-backed
  reaffirmation on the exact closure head without a lifecycle or assurance
  overclaim;
- an authorized governance approver records publication approval for the exact
  closure head under `GOVERNANCE.md`;
- the closure merge commit passes post-merge validation with a clean checkout;
- remote annotated tag `v0.4-alpha` resolves to that exact validated commit;
- the tagged changelog condition is thereby true for the recorded UTC
  publication date;
- issue #39 records the candidate, merge, tag, commands, counts, reviews, and
  lifecycle limitations and is closed; and
- temporary branches and owned worktrees are removed without disturbing
  unrelated work.
