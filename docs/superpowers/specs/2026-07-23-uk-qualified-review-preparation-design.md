# UK Mapping Qualified-Review Preparation Design

**Status:** Approved for implementation planning

**Date:** 2026-07-23

## 1. Purpose

Prepare the three Draft UK Cyber Essentials mapping snapshots for qualified,
independent human review under ESAF-1600 without representing preparation,
automation, editorial review, or AI assistance as qualified mapping review.

The in-scope mapping sets are:

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
  (Cyber Essentials Core, 116 provisions);
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
  (ESAF-to-Cyber Essentials Plus forward mapping, 144 provisions); and
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`
  (Cyber Essentials Plus-to-ESAF reverse observation, 144 provisions).

No qualified reviewer has been identified. This work therefore stops at
review readiness. It shall not change a mapping-set or mapping-record status,
add reviewer metadata, record a qualified-review disposition, or close GitHub
issue `#55`.

## 2. Current state and constraints

All three snapshots are `draft`. Each snapshot already contains a pinned
source declaration, publication-rights record, provision inventory, ESAF
control manifest, mapping records, change history, and registry entry.
Existing technical and publication reviews supported Working Draft
publication under repository-owner risk acceptance, but did not satisfy the
qualified scheme-review requirement.

ESAF-1600 and the crosswalk schemas require:

- a `reviewed` mapping set and every `reviewed` record to identify a qualified
  reviewer different from the mapper;
- the reviewer to attest authorized access to the exact official source;
- reviewer qualification, date, and findings disposition to be recorded;
- no open Critical or Important findings at `reviewed`;
- mapping-set and registry lifecycle state to remain synchronized; and
- exact-source, exact-version, scope, rights, inventory, record, and digest
  integrity to remain verifiable.

Core and Plus are distinct schemes and review questions. The two Plus
snapshots also have different directions and purposes and shall not be
collapsed into one review conclusion.

## 3. Selected approach

Use separate, reproducible reviewer packages for Core, Plus forward, and Plus
reverse, generated from an exact Git commit.

The repository change will add:

1. a qualified-review protocol defining reviewer eligibility, review
   disciplines, findings handling, exact-SHA rules, and stop conditions;
2. reviewer attestation and structured review worksheet templates;
3. a deterministic package generator and focused tests; and
4. concise usage documentation.

The generator will produce review packages outside the repository. Generated
packages, completed attestations, and source materials will not be committed
by this preparation change. After the preparation pull request merges, the
three packages will be generated from the exact merged commit and their
manifest digests will be posted to issue `#55` with a reviewer recruitment
notice.

This separation avoids a self-referential candidate SHA and keeps the tracked
preparation change free of invented identities or premature lifecycle claims.

## 4. Repository artifacts

Implementation shall add these tracked artifacts:

- `crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md`
- `crosswalks/reviews/templates/REVIEWER_ATTESTATION.md`
- `crosswalks/reviews/templates/SPECIFICATION_INVENTORY_REVIEW.md`
- `crosswalks/reviews/templates/SECURITY_OVERCLAIMING_REVIEW.md`
- `tools/build_mapping_review_bundle.py`
- focused tests for the generator and review-readiness invariants

The protocol is durable project guidance, not normative ESAF control content.
It shall reference ESAF-1600 and the schemas rather than restating them as a
parallel lifecycle model.

The templates shall contain explicit placeholders and shall be invalid as
completed evidence until a named human supplies the required attestations.
Unresolved placeholders shall never be copied into mapping metadata.

## 5. Exact candidate and package boundaries

The generator shall accept:

- a full 40-character Git commit SHA;
- exactly one of the three in-scope mapping-set identifiers; and
- an output directory outside the repository worktree.

It shall read tracked bytes from the named Git commit, not from an uncommitted
working tree. It shall reject:

- an abbreviated, missing, or non-commit object;
- a mapping-set identifier outside the explicit allowlist;
- a dirty or ambiguous source selection;
- output inside the repository or any attached worktree;
- an existing non-empty destination;
- missing, duplicated, or unexpected required artifacts; and
- any digest or population mismatch discovered while assembling the package.

Each package shall include:

- the snapshot `README.md`;
- `PROVISION_INVENTORY.md`;
- `ESAF_CONTROL_MANIFEST.json`;
- the complete mapping-record population for that snapshot;
- the corresponding registry entry;
- the applicable mapping catalog entries;
- the ESAF controls referenced by the pinned control manifest;
- the ESAF-1600 method and applicable JSON schemas;
- the qualified-review protocol and blank reviewer templates;
- a package index describing every included file and its purpose; and
- a machine-readable manifest containing the mapping-set identifier, candidate
  commit, generator version, file paths, byte sizes, SHA-256 digests, and
  aggregate package-manifest digest.

The package index shall identify Core, Plus forward, or Plus reverse and shall
state the direction and non-claim boundary in plain language.

The generator shall preserve repository-relative paths within the package,
use stable lexical ordering, normalize generated metadata deterministically,
and produce identical manifests and content for repeated runs with the same
inputs. Archive-container timestamps are out of scope; the authoritative
integrity object is the deterministic package directory and manifest.

## 6. Source-rights boundary

The package shall contain only material already tracked in ESAF and generated
review metadata. It shall not download, copy, embed, or redistribute external
source documents.

The package index and attestation shall identify the official source URLs,
versions, checksums, locators, publication-rights basis, prohibited elements,
and access restrictions already recorded by the mapping set. Reviewers must
obtain authorized source access independently and attest to it. A URL,
checksum, or package manifest is not evidence that a reviewer had authorized
access.

If a reviewer cannot access the exact source version, review stops. A
substitute version, secondary summary, adjacent assurance scheme, or another
reviewer's access shall not satisfy the requirement.

## 7. Reviewer eligibility and independence

Eligibility is evaluated per mapping set and review role. Before reviewing, a
named human shall attest:

- legal name or stable professional identity;
- organizational affiliation and contact or verification locator;
- relevant Cyber Essentials or Cyber Essentials Plus scheme knowledge;
- relevant ESAF, control-mapping, assurance, or security-review experience;
- the exact mapping set and candidate SHA being reviewed;
- authorized access to the exact official source;
- independence from the mapper and mapping decisions under review;
- conflicts of interest and their disposition; and
- agreement that the review does not assert certification, compliance,
  equivalence, endorsement, or assurance beyond the recorded relationships.

The project owner shall determine whether the documented qualifications and
independence are sufficient before accepting review evidence. Codex, an AI
system, the original mapper, or an unnamed group cannot serve as the qualified
reviewer.

The same human may cover more than one mapping set only when eligibility,
source access, independence, and findings are documented separately for each
set. Core qualification shall not be presumed to establish Plus qualification.

## 8. Required independent review disciplines

Every mapping set requires two separately recorded review disciplines on the
same exact candidate SHA.

### 8.1 Specification and inventory review

This review shall verify:

- official publication identity, version, checksum, and source locators;
- publication-rights statements and restrictions;
- provision population, identifiers, hierarchy, granularity, and coverage;
- correspondence among the inventory, mapping records, scope count, registry,
  and generated catalogs;
- change-history and predecessor integrity where applicable; and
- the absence of omitted, duplicated, invented, or wrong-version provisions.

### 8.2 Security and overclaiming review

This review shall verify:

- each relationship against exact external normative text and exact ESAF
  normative control text;
- direction, relationship type, coverage, confidence, conditions, expected
  evidence, and known gaps;
- every `no_direct_mapping` disposition and negative rationale;
- the distinction between `prerequisite` and `partially_supports`;
- that conditions qualify an existing relationship rather than create a
  missing external outcome;
- that implementation guidance or adjacent capabilities are not used as
  substitutes for normative requirements; and
- that the snapshot makes no compliance, certification, equivalence,
  endorsement, or assurance claim.

The two worksheets shall be completed and signed separately. Prefer distinct
qualified humans for the two roles. If one human performs both disciplines,
the project owner must explicitly accept that arrangement and the reviewer
must demonstrate qualifications for both; the reviews and findings remain
separate.

## 9. Findings and candidate changes

Each worksheet shall record:

- the exact mapping set and candidate SHA;
- reviewer identity and attestation locator;
- review role, date, scope, and method;
- provision and record coverage;
- finding identifier, affected record identifiers, severity, description,
  evidence, required action, and disposition; and
- an explicit overall conclusion of `pass`, `pass_after_correction`, or
  `stop`.

Severities shall use the ESAF-1600 values `Critical`, `Important`, and `Minor`.
Critical and Important findings must be resolved before a `reviewed`
transition. Only Minor findings may be accepted, with a named acceptor,
rationale, and date.

Any content or metadata correction changes the candidate. Both review
disciplines shall be redispatched on the new exact SHA. Earlier results may
inform the new review but shall not be represented as final approval of the
changed candidate.

## 10. Later lifecycle transition

The preparation pull request shall not perform a lifecycle transition.

After eligible reviewers complete both disciplines for all three packages:

1. findings are triaged and required corrections are implemented;
2. affected validations and package generation are rerun;
3. both reviews are completed on the exact proposed transition head;
4. mapping-set and mapping-record reviewer metadata is added from verified
   human evidence;
5. mapping-set and record statuses move from `draft` to `reviewed`;
6. registry state and digests are regenerated and synchronized;
7. the Draft-to-reviewed transition is validated under ESAF-1600; and
8. issue `#55` is updated with identities, qualifications, dates, evidence
   locators, exact SHA, findings disposition, and validation results.

The target for issue `#55` is a qualified-review disposition at `reviewed`,
not `approved`. Approval would require a separately authorized approver and
the additional ESAF-1600 approval conditions.

No files may change after the final exact-head human attestations. If the pull
request head changes, affected review gates are stale and must be repeated.

## 11. Recruitment and issue update

After the preparation change merges, issue `#55` shall receive one concise
comment containing:

- the exact merged candidate SHA used for packaging;
- all three mapping-set identifiers and their separate package-manifest
  digests;
- the generator command and repository protocol locator;
- the two required review roles;
- reviewer eligibility, independence, and source-access requirements;
- instructions for expressing interest without posting sensitive personal or
  licensed material publicly; and
- the explicit statement that the mappings remain Draft and the issue remains
  open until qualified human review is completed.

The comment shall recruit reviewers; it shall not name, assign, approve, or
pre-qualify anyone who has not provided evidence.

## 12. Stop conditions

Review preparation or review shall stop when:

- no eligible named human reviewer is available;
- qualification, independence, conflict, or source-access evidence is absent;
- a source version, checksum, inventory, record population, or digest differs
  from the package manifest;
- Core and Plus conclusions are combined or a directional conclusion is
  reused without separate review;
- the candidate SHA changes;
- external licensed or restricted material would need to be redistributed;
- a Critical or Important finding remains open;
- a required field contains a placeholder or drafting marker; or
- the only available review is automated, AI-produced, mapper self-review, or
  otherwise not qualified under ESAF-1600.

In every stop state, the affected mapping set remains `draft`.

## 13. Test and validation strategy

Use test-driven development for the package generator and enforceable
review-readiness invariants.

Focused tests shall cover:

- exact allowlisted mapping-set selection and expected populations of 116,
  144, and 144 provisions;
- extraction from the named Git commit rather than working-tree bytes;
- complete record, inventory, manifest, registry, catalog, control, method,
  schema, protocol, and template inclusion;
- deterministic file ordering and SHA-256 manifest generation;
- rejection of abbreviated or invalid SHAs, unexpected mapping sets,
  population or digest mismatches, path traversal, non-empty output, and
  output inside any worktree;
- exclusion of downloaded or untracked external source material;
- separate Core, Plus forward, and Plus reverse package labels;
- required attestation, findings, exact-SHA, non-claim, and stop-condition
  fields in the templates; and
- preservation of `draft` status and absence of reviewer metadata in all three
  repository snapshots during preparation.

The complete validation set is:

```text
python -m unittest <focused review-package tests> -v
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
git diff --check <merge-base>..HEAD
```

The implementation shall generate all three packages twice in separate
temporary directories from the exact candidate and compare their manifests
and file digests. Temporary packages shall be removed after validation and
shall not appear in the Git diff.

Set `PYTHONDONTWRITEBYTECODE=1`, verify no `__pycache__` directories remain,
and verify a clean worktree after commits.

No Mermaid source is expected to change. If implementation adds or changes a
Mermaid block, every affected block shall be rendered with the current Mermaid
CLI and reviewed for readability.

## 14. Review and delivery workflow

Implementation shall remain on the isolated
`agent/uk-qualified-review-preparation` branch and worktree. Before merge it
shall receive:

- independent specification review against this design;
- independent security and overclaiming review of the complete branch;
- final whole-branch review on the exact candidate SHA;
- the complete validation set;
- a reviewable pull request whose description records the reviewed head SHA
  and exact gate results; and
- confirmation that the reviewed SHA still matches the pull-request head and
  that GitHub checks pass with a clean merge state.

After merge, update local `main`, rerun proportional validation, generate the
three packages from the merged SHA, post the recruitment comment to issue
`#55`, verify the mappings remain `draft`, and remove only the owned branch,
worktree, and temporary package outputs. Unrelated branches and worktrees
shall not be changed.
