# ESAF 0.4-Alpha Closure and Planning Reconciliation Design

**Status:** Approved

**Target release:** 0.4-alpha

**Design date:** 2026-07-14

## 1. Purpose

Reconcile ESAF's planning and release metadata with the repository's actual state after completion of the seven-pattern reference-architecture draft library and the early ESAF-1600 crosswalk work. The milestone will make the next work queue trustworthy without representing 0.4-alpha as formally released or its Draft artifacts as approved.

## 2. Current state

The repository is on 0.4-alpha and contains Draft records for ARC-P100 through ARC-P160. The version badge, roadmap version, release stage, changelog, architecture narrative, and backlog do not consistently reflect that state. GitHub Issues, designated as the authoritative queue, has no open items.

The Cyber Essentials v3.3 snapshot is an early Draft crosswalk against the 0.4-alpha control baseline. Its presence does not complete the priority-crosswalk scope assigned to 0.5-beta, and it remains subject to qualified human review.

No Git tag, consolidated exact-SHA release-gate record, or documented governance approval establishes a formal 0.4-alpha publication. All architecture patterns remain Draft. The milestone therefore closes planning drift and records open release gates; it does not publish or approve the release.

## 3. Decision

Use a conservative reconciliation with enforceable document invariants.

1. Advertise 0.4-alpha consistently in `README.md`, `ROADMAP.md`, and `VERSION.md`.
2. Describe the current stage as the initial reference-architecture Draft library, not merely its foundation.
3. Record all seven delivered architecture patterns in the 0.4-alpha changelog.
4. Clarify that the 0.2-alpha through 0.4-alpha sections are unreleased working-draft stages and that the Cyber Essentials work is an early Draft artifact, not completion of the 0.5-beta milestone.
5. Replace completed backlog items with the actual next queue: 0.4-alpha publication closure, qualified review of the Cyber Essentials core snapshot, Cyber Essentials Plus public-source acquisition and atomization design, remaining priority crosswalks, assessment work, and industry profiles.
6. Update architecture narrative from a prospective queue to the completed initial Draft library while preserving every pattern's Draft status.
7. Add a release-readiness record that distinguishes completed content from open publication gates and requires exact candidate-SHA evidence before release.
8. Add focused tests that prevent version, architecture-inventory, changelog, backlog, and unreleased-state drift.

## 4. Release-readiness boundary

`project/RELEASE_PLAN.md` will remain the durable release policy and will gain a 0.4-alpha readiness section. The section will record the architecture milestone as content-complete while leaving publication gates open. It will not hard-code a candidate SHA before a release candidate exists, fabricate reviewer identities, or convert absence of evidence into a pass.

The open gates shall include:

- approved release scope and exact candidate SHA;
- normative, technical, editorial, terminology, and global-link review;
- rendering and readability review of every Mermaid diagram;
- qualified review of mappings required for the release scope;
- synchronized changelog and version metadata;
- governance approval;
- passing GitHub checks and clean merge state; and
- post-merge validation before tagging or publication.

The record will state that structural validators do not substitute for renderer validation, qualified mapping review, or governance approval.

## 5. Enforceable invariants

A new `tests/test_release_metadata.py` module will require:

- the README badge and roadmap version to match `VERSION.md`;
- the current release to remain a Working Draft and the changelog heading to remain Unreleased until a deliberate test update accompanies a lifecycle change;
- every registered architecture pattern identifier and title to appear in the 0.4-alpha changelog;
- the backlog not to queue architecture records that already exist in the registry;
- the backlog to identify Cyber Essentials Plus public-source acquisition and atomization as the next substantive crosswalk design activity; and
- release-readiness text to preserve the exact-SHA, Mermaid-rendering, qualified-review, and governance-approval boundaries.

Tests will be written and observed failing against the current repository before metadata is changed.

## 6. Scope

### 6.1 In scope

- `README.md`, `ROADMAP.md`, `VERSION.md`, and `CHANGELOG.md` reconciliation.
- `project/BACKLOG.md` and `project/RELEASE_PLAN.md` reconciliation.
- Prospective-to-current wording corrections in architecture overview and registry pages.
- Focused release-metadata regression tests.
- Design and implementation-plan records for this milestone.
- Full repository validation, whole-branch diff review, independent review, pull request publication, merge, and cleanup.

### 6.2 Out of scope

- Promoting any architecture pattern beyond Draft.
- Declaring, tagging, or publishing 0.4-alpha.
- Claiming governance approval or qualified crosswalk review.
- Adding a reusable Mermaid renderer or changing diagrams solely to satisfy this reconciliation.
- Creating the Cyber Essentials Plus inventory or mapping records.
- Substantive changes to ESAF normative controls, architecture requirements, or crosswalk relationships.

## 7. Alternatives considered

### 7.1 Declare 0.4-alpha released

Rejected because the repository has no tag, exact-SHA gate record, governance approval, qualified mapping review, or complete renderer evidence, and all architecture records remain Draft.

### 7.2 Skip reconciliation and begin Cyber Essentials Plus immediately

Rejected because the authoritative work queue is empty and local planning files contain completed work. Starting another substantial mapping would compound unreliable sequencing and release metadata.

### 7.3 Reconcile metadata while keeping the release unreleased

Selected because it corrects factual drift, adds durable enforcement, and exposes the real publication work without overstating assurance or approval.

## 8. Validation and review

The candidate shall complete:

- focused release-metadata tests with a recorded red-green cycle;
- `python -m unittest discover -s tests -v`;
- `python tools/validate_controls.py --check`;
- `python tools/validate_architectures.py`;
- `python tools/validate_crosswalks.py --check --baseline-ref <merge-base>`;
- `git diff --check <merge-base>..HEAD`;
- placeholder, generated-cache, and worktree-cleanliness checks; and
- independent whole-branch review against this design and the implementation plan.

Critical and Important findings shall be resolved before merge. The pull-request description shall record the reviewed head SHA and exact validation results. GitHub checks and mergeability shall be verified on that same head.

## 9. Follow-on milestone

After this reconciliation merges, the next substantive design milestone is Cyber Essentials Plus public-source acquisition and atomization. It will pin the public NCSC Cyber Essentials Plus Test Specification independently from the Cyber Essentials core snapshot, record version and byte-level source identity, distinguish public test procedures from non-public operational scheme material, resolve rights for every source, and prohibit certification or assurance inference.

## 10. Acceptance criteria

The milestone is complete when:

- release and planning metadata describe the repository consistently;
- all seven architecture Drafts are represented in the changelog and architecture narrative;
- completed architecture work is absent from the backlog;
- 0.4-alpha remains explicitly unreleased with open publication gates;
- the next substantive crosswalk activity is unambiguous;
- focused and full validation pass on the final candidate;
- independent review reports no unresolved Critical or Important findings;
- the pull request merges with passing checks; and
- updated `main` is validated and the temporary branch and worktree are removed.
