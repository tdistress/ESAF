# Qualified Review Protocol for UK Mapping Snapshots

## Status and boundary

This protocol prepares Draft mappings for qualified independent human review
under ESAF-1600. Preparation, automation, mapper self-review, and AI-produced
review are not qualified review. Until every applicable condition is met, the
affected mapping set remains `draft`.

## Authoritative method and schemas

The authoritative review and lifecycle rules remain in:

- `crosswalks/ESAF-1600.md`;
- `crosswalks/schema/mapping-set.schema.json`;
- `crosswalks/schema/mapping-record.schema.json`;
- `crosswalks/schema/provision-inventory.schema.json`;
- `crosswalks/schema/esaf-control-manifest.schema.json`; and
- `crosswalks/schema/lifecycle-record.schema.json`.

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

## Candidate integrity

Every review names one full 40-character Git commit SHA and one package manifest digest. Every repository-sourced payload byte shall be read from either the exact candidate commit or an exact historical commit SHA pinned by candidate-commit metadata; working-tree bytes shall never be used. Generated metadata shall be deterministic from those inputs. A changed candidate invalidates final review evidence.

## Reviewer eligibility

A named human records scheme qualification, ESAF or mapping qualification,
authorized source access, organization, verification locator, independence
from the mapper, and conflicts of interest. The project owner accepts or
rejects eligibility per mapping set and review role. The reviewer must be
different from the mapper.

Prefer different qualified humans for the two review disciplines. If one
human performs both disciplines, the project owner must explicitly accept
that arrangement. The reviewer must demonstrate qualifications for both
roles, and the attestations, worksheets, findings, signatures, and conclusions
remain separate.

## Specification and inventory review

Verify official source identity/version/checksum/locators, publication rights,
provision population and hierarchy, record coverage, registry/catalog
consistency, and predecessor/change-history integrity.

## Security and overclaiming review

Verify each relationship and `no_direct_mapping` rationale against exact
normative source and ESAF text. Check direction, coverage, confidence,
conditions, evidence, gaps, `prerequisite` versus `partially_supports`, and
all certification, compliance, equivalence, endorsement, and assurance
nonclaims. The review shall also confirm:

- conditions cannot create a missing external outcome; and
- implementation guidance or adjacent capabilities cannot replace normative
  requirements.

## Findings

Use Critical, Important, and Minor. Critical and Important findings cannot be
accepted and shall be resolved before `reviewed`. Only Minor findings may be
accepted, with a named acceptor, acceptance rationale, and disposition date.
Record separate signed worksheets for both review disciplines.

## Signed worksheet digest procedure

The signed worksheet digest shall be reproducible and shall not hash its own
value. First encode the completed worksheet as UTF-8 without BOM and LF line
endings. Ensure all other fields, including the reviewer signature and
signature date, are final. For the digest calculation, remove the entire
`| Signed worksheet SHA-256 |` table row, including its terminating LF, and
hash every remaining byte with SHA-256. Record the resulting lowercase
hexadecimal digest in that row. Verification repeats the same row exclusion.
No non-excluded byte may change after the digest is recorded.

## Lifecycle transition

This preparation does not add reviewer metadata or change lifecycle state.
A later transition updates every mapping record, mapping-set metadata,
registry state, catalogs, and digests together on an exact human-reviewed
head. `reviewed` is not `approved`.

## Stop conditions

Stop for missing eligibility, independence, source access, source/version or
digest mismatch, changed SHA, combined Core/Plus conclusions, external-source
redistribution, open Critical or Important findings, unresolved template
markers, or an AI-produced review. The affected mapping remains `draft`.
