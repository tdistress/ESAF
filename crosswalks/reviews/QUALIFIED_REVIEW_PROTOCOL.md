# Qualified Review Protocol for UK Mapping Snapshots

## Status and boundary

This protocol prepares Draft mappings for qualified independent human review
under ESAF-1600. Preparation, automation, mapper self-review, and AI-produced
review are not qualified review. This preparation shall not perform a
lifecycle transition, populate reviewer identities, or create completed
evidence. Until every applicable condition is met, the affected mapping set
remains `draft`.

The completed attestations, completed worksheets, campaign manifests, archives,
seal records, and source documents remain external and uncommitted. Blank
forms and the evidence schema are repository content. The external evidence
records hashes and durable locators; it shall not copy licensed source
documents into Git or a generated review package.

## Authoritative method and schemas

The authoritative review and lifecycle rules remain in:

- `crosswalks/ESAF-1600.md`;
- `crosswalks/schema/mapping-set.schema.json`;
- `crosswalks/schema/mapping-record.schema.json`;
- `crosswalks/schema/provision-inventory.schema.json`;
- `crosswalks/schema/esaf-control-manifest.schema.json`;
- `crosswalks/schema/lifecycle-record.schema.json`; and
- `crosswalks/schema/qualified-review-evidence.schema.json`.

This protocol supplies a review procedure and evidence forms. It does not
replace or restate those normative and machine-enforced requirements as a
parallel lifecycle model.

## In-scope snapshots

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
  — Core, 116 provisions.
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
  — Plus forward, 144 provisions.
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`
  — Plus reverse, 144 provisions.

Core, Plus forward, and Plus reverse require separate packages, findings, and
conclusions.

## Two-stage campaign

Each campaign uses `REVIEW_EVIDENCE.json` with schema version `1.0.0` and
exactly three mapping-set entries. Each entry has exactly two separate role
records: `specification_and_inventory` and
`security_and_overclaiming`.

The two preserved campaign phases are:

1. `draft_review`, which records substantive human review of one exact
   `draft` candidate; and
2. `final_reviewed_confirmation`, which records both disciplines'
   confirmation of the exact transitioned `reviewed` candidate proposed for
   merge.

A final confirmation shall reference the preserved Draft campaign by campaign
identifier, Draft candidate commit, manifest SHA-256, and seal-record SHA-256.
It shall use a different exact reviewed candidate SHA. It shall not overwrite
the Draft campaign or store host-local paths to that campaign.

## Candidate and path integrity

Every review names one full 40-character Git commit SHA and one package
manifest digest. Every repository-sourced payload byte shall be read from either the exact candidate commit or an exact historical commit SHA pinned by candidate-commit metadata; working-tree bytes shall never be used. Generated metadata shall be deterministic from those inputs. A changed candidate invalidates final review evidence.

Campaign paths shall be canonical relative paths beneath the external
campaign root. They shall not be URLs, absolute paths, aliases, traversal
paths, symbolic links, junctions, or files inside any Git worktree. Immutable
locators and reviewer verification locators shall be immutable HTTPS
object/version URLs or `urn:sha256:<lowercase-digest>` values. Every campaign,
package, attestation, and worksheet retention owner shall accept preservation
responsibility under the recorded campaign retention commitment.

## Reviewer eligibility and field binding

A named human records qualification, authorized source access, organization,
verification locator, independence from the mapper, and conflicts of interest.
The project owner accepts or rejects eligibility per mapping set and review
role. The reviewer must be different from the mapper.

Prefer different qualified humans for the two review disciplines. If one
human performs both disciplines, the project owner must explicitly accept
that arrangement. `dual_role_accepted` shall be false for unique reviewers
and true on both role records when the same identity performs both roles.
That reviewer shall demonstrate qualifications for both roles, and the
attestations, worksheets, findings, signatures, and conclusions remain
separate.

The reviewed mapping-set and provision-record reviewer object uses exactly
`id` from `reviewer.identity`, `date` from `worksheet.review_date`,
`qualification` and `authorized_source_access` from the reviewer evidence, and
`findings_disposition` from the signed worksheet field
`Reviewer metadata findings disposition`. The specification and inventory
role binds the mapping-set reviewer object. The security and overclaiming role
binds every applicable provision-record reviewer object. Those fields shall
be semantically identical on the exact reviewed candidate.

## Specification and inventory review

Verify official source identity/version/checksum/locators, publication rights,
registry/catalog consistency, and change-history integrity. The reviewer shall
make and record explicit determinations for:

- provision population;
- provision identifiers;
- provision hierarchy;
- provision granularity;
- provision coverage;
- predecessor integrity; and
- absence of omitted, duplicated, invented, or wrong-version provisions.

## Security and overclaiming review

Verify each relationship and `no_direct_mapping` rationale against exact
normative source and ESAF text. Check direction, coverage, confidence,
conditions, evidence, gaps, `prerequisite` versus `partially_supports`, and
all certification, compliance, equivalence, endorsement, and assurance
nonclaims. The review shall also confirm:

- conditions cannot create a missing external outcome; and
- implementation guidance or adjacent capabilities cannot replace normative
  requirements.

## Findings, validity, and readiness

Use Critical, Important, and Minor. Accepted Critical or Important findings
make the campaign evidence-invalid. Only Minor findings may be accepted, with
a named acceptor, acceptance rationale, and disposition date. Record separate
signed worksheets for both review disciplines.

The validator derives `evidence_valid` for both phases. A Draft campaign also
derives `transition_ready`; a final confirmation derives `merge_ready`.
Valid `stop` evidence has `evidence_valid: true` and the applicable readiness
result false. A `stop` conclusion may preserve open Critical or Important
findings without misrepresenting the evidence as ready. Only complete `pass`
or `pass_after_correction` evidence with reconciled findings may be ready.
A `pass_after_correction` worksheet shall name the exact campaign candidate
SHA reviewed after correction.

## Closed Markdown grammar

Completed forms shall retain the exact template heading order, table names,
ordered row labels, and fixed findings header. Every value shall be
single-line UTF-8 text without an unescaped pipe. Rows and sections shall not
be added, removed, duplicated, or reordered. A findings table may contain a
literal `NONE` row or finding rows, but never both. All template markers shall
be replaced, and the attestation's free-text Yes/No answers shall agree with
its table.

## Signed worksheet digest procedure

The signed worksheet digest shall be reproducible and shall not hash its own
value. First encode the completed worksheet as UTF-8 without BOM and LF line
endings. Ensure all other fields, including the reviewer signature and
signature date, are final. For the digest calculation, remove the entire
`| Signed worksheet SHA-256 |` table row, including its terminating LF, and
hash every remaining byte with SHA-256. Record the resulting lowercase
hexadecimal digest in that row. Verification repeats the same row exclusion.
No non-excluded byte may change after the digest is recorded.

## External sealing sequence

After evidence completion, validate the completed campaign, hash the canonical
manifest, create and hash the deterministic archive, upload the archive to its
immutable locator, then write `CAMPAIGN_SEAL.json` outside the sealed campaign
root. The seal is canonical one-line UTF-8/LF JSON with sorted keys, no
insignificant whitespace, and schema version `1.0.0`.

The seal has exactly these keys:

- `archive_byte_length`;
- `archive_format`, with value `zip`;
- `archive_locator`;
- `archive_media_type`, with value `application/zip`;
- `archive_sha256`;
- `campaign_id`;
- `candidate_commit`;
- `evidence_valid`;
- `manifest_sha256`;
- `readiness_name`;
- `readiness_value`;
- `schema_version`; and
- `validator_version`.

The archive contains the validated campaign allowlist, but not its own seal.
Publish the seal-record SHA-256 and locator in the external issue or pull
request evidence record. No campaign byte may change after sealing.

## Automation and human judgment boundary

Automation checks schema, bytes, hashes, paths, field consistency, campaign
linkage, and readiness rules. Automation cannot establish human identity,
qualification, source authorization, signature effect, the truth of human
review conclusions, or non-infringement of human-authored prose. An automated
pass therefore validates the evidence contract; it does not create qualified
review or substitute for the named humans' judgments.

## Lifecycle transition

This preparation shall not perform a lifecycle transition. It does not add
reviewer metadata or change lifecycle state. A later transition updates every
mapping record, mapping-set metadata, registry state, catalogs, and digests
together on the exact human-reviewed head. The separate
`final_reviewed_confirmation` campaign then confirms that exact transitioned
head. `reviewed` is not `approved`.

## Stop conditions

Stop for missing eligibility, independence, source access, source/version or
digest mismatch, changed SHA, invalid campaign linkage, combined Core/Plus
conclusions, external-source redistribution, unresolved template markers,
unsealed mutation, or an AI-produced review. Accepted Critical or Important
findings are evidence-invalid. Open Critical or Important findings require a
valid `stop` conclusion and make readiness false. The affected mapping remains
`draft` until valid Draft evidence supports a later authorized transition.
