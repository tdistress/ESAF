# UK qualified-review evidence gate design

**Issue:** [#55 Complete qualified review of the three UK mapping snapshots](https://github.com/tdistress/ESAF/issues/55)

**Status:** Approved for implementation

## Purpose

Issue 55 requires two separately recorded qualified human review disciplines
for each of three Draft UK mapping sets. The repository can generate
deterministic review packages, but it cannot yet validate completed external
attestations and worksheets or package a transitioned `reviewed` candidate for
final exact-SHA review.

This work shall add those two capabilities. It shall not perform qualified
review, decide whether a person is qualified, sign evidence, populate reviewer
metadata, or change any mapping lifecycle state.

## Current state

The three mapping sets are:

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`;
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`; and
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`.

They contain 404 Draft provision records in total. Core, Plus forward, and Plus
reverse remain separate mapping sets with separate packages, evidence, findings,
and conclusions.

The qualified-review protocol requires a specification and inventory review and
a security and overclaiming review for each mapping set. A single human may fill
both roles only when the project owner accepts the dual role and the person
demonstrates both qualifications. AI output, automation, mapper self-review, and
ordinary pull-request review do not satisfy either role.

## Selected approach

The repository shall define a closed machine-readable campaign manifest and a
validator that consumes the manifest together with completed external Markdown
attestations, worksheets, and review packages. The signed human evidence shall
stay outside Git at access-appropriate immutable locators. The manifest shall
contain hashes, durable locators, and local verification paths, not licensed
source material.

`crosswalks/schema/qualified-review-evidence.schema.json`, with schema identifier
`https://esaf-standard.org/schemas/qualified-review-evidence.schema.json`, shall
define the campaign manifest. Repository tests shall keep the schema, validator,
templates, and protocol consistent.

The existing package generator shall gain an explicit reviewed-candidate mode.
Draft behavior remains the default. Reviewed mode shall accept only a complete,
uniformly reviewed candidate with valid reviewer metadata and empty lifecycle
events.

Two alternatives were rejected:

1. Refreshing Draft packages without an evidence validator leaves worksheet
   digests, role coverage, dual-role acceptance, and finding dispositions
   unenforced.
2. Automating the 404-record lifecycle transition before real signed evidence
   exists would force the project to guess at reviewer identifiers, evidence
   locators, and finding reconciliation.

## External evidence model

Two campaign phases shall be preserved separately:

1. `draft_review` records the substantive review of one exact Draft candidate;
2. `final_reviewed_confirmation` records both disciplines' confirmation of the
   exact transitioned `reviewed` candidate that will be merged.

A final confirmation shall reference, not overwrite, the applicable Draft
campaign. One campaign directory shall contain:

- `REVIEW_EVIDENCE.json`;
- one completed reviewer attestation for each assigned human and mapping-set
  role;
- one completed specification and inventory worksheet for each mapping set; and
- one completed security and overclaiming worksheet for each mapping set; and
- three complete package directories, one per mapping set.

The campaign manifest shall use canonical UTF-8/LF JSON with exact key sets. It
shall record:

- schema version, campaign identifier, and campaign phase;
- `candidate_state` with the exact value `draft` or `reviewed` required by the
  phase;
- one full 40-character candidate SHA;
- the campaign retention owner and retention commitment;
- the referenced Draft campaign identifier, candidate SHA, manifest SHA-256,
  and seal-record SHA-256 for final confirmation;
- the exact three mapping-set identifiers;
- one package root, package-manifest SHA-256, package-manifest path, immutable
  locator, and retention owner per mapping set;
- exactly two role records per mapping set;
- reviewer identity, organization, verification locator, qualifications,
  authorized-source-access attestation, independence, conflicts and their
  disposition;
- project-owner eligibility acceptance and any dual-role acceptance;
- attestation path, immutable locator, retention owner, and SHA-256;
- worksheet path, immutable locator, retention owner, full-file SHA-256,
  signed-worksheet SHA-256, review date, and conclusion; and
- finding identifiers and dispositions needed to reconcile the worksheet with
  authoritative mapping findings.

Campaign-internal paths shall be canonical relative paths beneath the current
`--evidence-root`. They shall not be URLs, absolute paths, aliases, traversal
paths, symbolic links, junctions, or files inside any Git worktree. The final
manifest shall not store host-local paths to a preserved Draft campaign or its
seal record. The separately supplied `--draft-evidence-root` and
`--draft-seal-record` inputs shall be validated as external roots and bound by
campaign identifier, candidate SHA, manifest SHA-256, and seal-record SHA-256.

Immutable locators are separate from local paths and reviewer
identity-verification locators. Each shall be an HTTPS URL with an immutable
object or version identifier, or a `urn:sha256:<lowercase-digest>` value. The
recorded SHA-256 binds the locator to the verified local bytes. The retention
owner shall accept responsibility for preserving access according to the
recorded retention commitment. The validator checks locator syntax and hash
agreement but does not claim that a remote object is available.

The campaign manifest shall not contain its own archive locator. After local
validation, the operator shall hash the final canonical manifest and sealed
campaign archive, upload the archive to its immutable destination, and create
`CAMPAIGN_SEAL.json` outside the sealed campaign root. The seal shall be
canonical one-line UTF-8/LF JSON with sorted keys, no insignificant whitespace,
schema version `1.0.0`, and this exact key set:

- `archive_byte_length`;
- `archive_format`, with the exact value `zip`;
- `archive_locator`;
- `archive_media_type`, with the exact value `application/zip`;
- `archive_sha256`;
- `campaign_id`;
- `candidate_commit`;
- `evidence_valid`;
- `manifest_sha256`;
- `readiness_name`;
- `readiness_value`;
- `schema_version`; and
- `validator_version`.

The sealing operation shall create deterministic ZIP bytes. Entries shall use
sorted canonical POSIX paths, implicit directories, stored compression, fixed
`1980-01-01 00:00:00` timestamps, and regular-file mode `0644`. The archive
shall contain exactly the validated campaign allowlist. It shall reject
duplicate or unexpected entries, absolute or traversal paths, symbolic links,
junction metadata, other special file modes, and path aliases.

The seal record shall contain the archive locator, manifest SHA-256, archive
byte length and SHA-256, candidate SHA, campaign identifier, validator version,
and validation results. Revalidation shall reconstruct the deterministic ZIP
from the preserved local campaign and compare exact archive bytes, byte length,
and digest with the downloaded or retained archive and seal. The operator shall
publish the seal-record SHA-256 and locator in an external GitHub issue or
pull-request evidence record. No campaign byte changes after sealing. The seal
record is not part of the archive it identifies, which avoids a self-referential
manifest or archive digest.

The sealing CLI shall publish `CAMPAIGN_ARCHIVE.zip` and
`CAMPAIGN_SEAL.json` together in one new external output directory. It shall
write both files in a sibling staging directory on the destination filesystem,
repeat candidate execution-state checks, and atomically rename that directory.
It shall not accept split archive and seal destinations.

The manifest and local evidence files are verification inputs. They are not
authoritative mapping records and shall not enter generated crosswalk catalogs.

## Evidence validation

`tools/validate_qualified_review_evidence.py` shall provide:

```text
python tools/validate_qualified_review_evidence.py \
  --candidate <full-sha> \
  --evidence-root <external-directory> \
  --check
```

Final confirmation shall also require:

```text
--draft-evidence-root <preserved-draft-campaign-directory>
--draft-seal-record <preserved-draft-campaign-seal.json>
--draft-archive <preserved-draft-campaign-archive.zip>
```

The separate archive input lets revalidation compare the retained or downloaded
archive byte-for-byte with deterministic reconstruction and the seal record.

The validator shall read repository bytes from the exact candidate commit and
shall fail closed unless:

- the supplied candidate exists, equals the campaign candidate, and contains
  the exact three mapping sets in the campaign's required state;
- a final confirmation recursively validates the locally preserved Draft
  campaign, validates the external canonical seal record, matches the manifest
  and seal-record digests to the final campaign reference, and uses a different
  exact reviewed candidate SHA;
- every package manifest names the same candidate, mapping set, and state,
  matches the recorded SHA-256, and self-excludes
  `PACKAGE_MANIFEST.json` from its payload list;
- package manifests use canonical paths and record each payload's exact
  purpose, byte length, and SHA-256;
- every package contains only allowlisted regular files, has no reparse-point
  ancestor or hard-link alias, and contains no unlisted file;
- deterministic package reconstruction from the exact candidate produces the
  same manifest and identical payload bytes;
- all six required mapping-set and role pairs occur exactly once;
- every attestation and worksheet exists as a regular file beneath the external
  root and matches its recorded digest;
- each completed Markdown file follows the closed grammar and contains no
  template marker;
- the signed-worksheet digest matches the protocol's row-exclusion procedure;
- each reviewer has affirmative authorized source access and independence;
- project-owner eligibility acceptance is affirmative;
- duplicate reviewer identities across the two disciplines have affirmative
  owner dual-role acceptance and both qualifications;
- each conclusion is `pass`, `pass_after_correction`, or `stop`;
- `pass_after_correction` names the exact post-correction candidate reviewed by
  the signer;
- `stop` may contain open Critical or Important findings but is never
  transition-ready;
- `pass` and `pass_after_correction` contain no open or accepted Critical or
  Important finding;
- only Minor findings may be accepted, with a named acceptor, rationale, and
  disposition date;
- finding identifiers and affected record identifiers are valid;
- transition-ready evidence reconciles every worksheet finding with the
  authoritative candidate findings;
- reviewed-state campaigns derive the exact mapping-set reviewer object from
  the specification and inventory role and require semantic equality for
  reviewer identity, review date, qualification, authorized source access, and
  findings disposition;
- reviewed-state campaigns derive the exact provision-record reviewer object
  from the security and overclaiming role and require the same semantic equality
  on every applicable record;
- the complete campaign tree contains only manifest-listed Markdown and JSON
  evidence and package files; and
- source documents, binary extensions, licensed source text fields, and
  unsupported lifecycle claims are absent from the complete campaign tree.

The validator shall derive `evidence_valid` for both phases. A Draft campaign
also derives `transition_ready`; a final confirmation derives `merge_ready`.
Valid `stop` evidence has `evidence_valid: true` and the phase readiness result
set to false. Only a complete `pass` or `pass_after_correction` campaign with
reconciled findings may be transition-ready or merge-ready.

The reviewer object is derived deterministically from nested role evidence:
`id` from `reviewer.identity`, `date` from `worksheet.review_date`,
`qualification` and `authorized_source_access` from the reviewer evidence, and
`findings_disposition` from a fixed signed worksheet field. Accepted Critical
or Important findings make the campaign evidence-invalid; they are not merely a
readiness stop. A `pass_after_correction` conclusion names the exact
post-correction campaign candidate SHA in either campaign phase.

The validator checks evidence completeness, file and field boundaries, and
internal consistency. It shall state that it does not prove identity,
qualifications, source authorization, a signature's legal effect, the truth of
a human review conclusion, or that human-authored prose is non-infringing.

Operational failures shall use concise sanitized diagnostics. Content failures
shall identify the campaign field or relative evidence path without exposing
unrelated host paths.

Every evidence and package file shall have a link count of exactly one. The
validator shall fail closed when the platform cannot report link count
reliably. Tests shall cover hard links separately from symbolic links,
junctions, and lexical traversal.

## Completed Markdown grammar

Attestations and worksheets shall retain the exact template heading order and
table names. Identification and signature tables shall use the exact ordered
row labels from the templates, with each row occurring once. Values shall be
single-line UTF-8 text without unescaped pipe characters. Enumerated values,
dates, SHAs, and Yes/No answers shall use their exact declared spelling.

The free-text attestation answers shall all be `Yes` and shall agree with their
corresponding table values. Duplicate rows, reordered or unknown sections,
additional fields, multiline cells, escaped ambiguity, and conflicting table
and body answers shall fail validation.

Findings tables may contain zero or more data rows after the fixed header and
separator. Each row shall contain the exact eleven cells defined by the
template. A literal `NONE` row represents no findings and shall not coexist
with a finding row.

## Reviewed-candidate package mode

`tools/build_mapping_review_bundle.py` shall retain the current Draft-only
default and add:

```text
--candidate-state reviewed
```

Reviewed mode shall require:

- snapshot status `reviewed`;
- exactly one provision record for every inventory identifier;
- every provision record status `reviewed`;
- complete snapshot and record reviewer metadata accepted by existing schemas;
- no open or accepted Critical or Important findings;
- mapping-set and registry agreement;
- an empty lifecycle event array; and
- current snapshot, registry, manifest, and catalog digests.

The generated package shall identify the candidate state in
`PACKAGE_MANIFEST.json` and `PACKAGE_INDEX.md`. It shall retain the same source
protection and deterministic-byte guarantees as Draft packages. External
attestations, completed worksheets, and source documents shall not be copied
into the package.

The package shall include
`crosswalks/schema/qualified-review-evidence.schema.json` with the existing
protocol and blank forms so reviewers receive the candidate-pinned evidence
contract.

Mixed Draft and reviewed content, `approved` content, missing reviewer metadata,
or nonempty lifecycle events shall stop package generation.

## Lifecycle boundary

This work shall leave all three mapping sets and all 404 records in `draft`.
Lifecycle registry events shall remain empty. The project shall not record a
reviewer, `reviewed` state, approval, publication, certification, compliance,
equivalence, endorsement, or scheme assurance.

A later transition may begin only after:

1. named humans submit complete Draft-review evidence for all six role
   assignments;
2. the project owner accepts reviewer eligibility and any dual role;
3. the validator passes on one exact Draft candidate;
4. all Critical and Important findings are resolved; and
5. any content correction is committed, repackaged, and reviewed again;
6. the transition produces one exact reviewed candidate and three reviewed
   packages; and
7. both disciplines sign a separate final-reviewed-confirmation campaign for
   that exact head.

The transition mechanism will be designed against real validated evidence. It
is outside this implementation.

## Testing

Development shall use test-driven development. Focused tests shall begin red
and cover:

- canonical campaign manifest structure;
- path containment, file type, and worktree exclusion;
- exact candidate, mapping-set, package, and digest bindings;
- Draft-review and final-reviewed-confirmation campaign linkage;
- recursive local Draft-campaign revalidation;
- campaign sealing without self-reference;
- exact seal schema and deterministic archive reconstruction;
- immutable locator syntax, retention fields, and local-byte hash binding;
- complete six-role coverage and duplicate-role rejection;
- reviewer eligibility fields, conflicts, independence, and dual-role rules;
- completed Markdown field extraction and template-marker rejection;
- signed-worksheet digest calculation;
- valid `stop` evidence versus transition readiness;
- finding severity, status, acceptance, correction-candidate, and
  affected-record reconciliation;
- exact reviewed-state reviewer-metadata agreement for both disciplines;
- complete campaign and package allowlists, deterministic reconstruction, and
  binary/source-document rejection;
- hard-link, symbolic-link, junction, and path-alias rejection;
- sanitized operational errors;
- Draft package behavior remaining unchanged;
- successful reviewed-candidate package generation from a complete fixture; and
- rejection of mixed, incomplete, approved, or lifecycle-event-bearing
  candidates.

Final validation shall include focused tests, the full unit suite, ordinary and
trusted-baseline crosswalk validation, link validation, and whole-branch diff
checks.

## Delivery and issue handoff

After the capability is merged, the project shall generate three new Draft
review packages from one clean exact `main` SHA outside every worktree. It shall
post the candidate SHA, mapping-set identifiers, package-manifest digests,
directions, payload counts, and validation results to issue 55.

Issue 55 shall remain open until named qualified humans complete the required
reviews and every acceptance criterion is met.
