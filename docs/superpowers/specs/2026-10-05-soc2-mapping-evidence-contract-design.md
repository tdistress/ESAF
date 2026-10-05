# SOC 2 mapping evidence contract design

**Status:** Approved for specification review
**Date:** 2026-10-05

## Purpose

Replace the SOC 2 readiness matrix's boolean feasibility flag and free-form
reviewer contract with machine-readable evidence sufficient for the renderer to
evaluate feasibility and exact-candidate review gates. This is an evidence
contract and validator change only. It does not acquire AICPA materials, change
the current readiness disposition, or authorize source-derived content or
mapping artifacts.

## Scope and decision boundary

The existing SOC 2 matrix remains the sole readiness decision surface. A
versioned evidence manifest will hold structured feasibility and reviewer
records, and the matrix will pin that manifest by repository path and SHA-256.
The renderer will validate the manifest and derive the affected gate states and
decision from evidence, rather than trusting a free-form positive boolean.
Existing source identity, authorized source artifact, publication rights,
inventory, overclaiming, and blocker checks remain mandatory.

All examples and fixtures in this change will be synthetic. They will not
contain AICPA text, criterion identifiers, inferred population counts, or
publication-rights conclusions. The checked-in live SOC 2 matrix remains
`HOLD`, and the crosswalk catalog, mappings, and registry remain unchanged.

## Evidence model

The manifest uses a strict schema version and exact-key validation, following
the SOC 2 renderer's existing closed-matrix convention. It contains:

- A feasibility record with disposition, scope, method, result rationale,
  evidence references, and SHA-256 digests of every input artifact it assessed.
- A six-role B005 participant roster naming the qualified mapper, AICPA TSC
  subject-matter reviewer, ESAF specification/mapping reviewer,
  publication-rights reviewer, security/overclaiming reviewer, and
  owner-authorized approver. Each role records its prescribed qualification,
  qualification evidence reference, authorized source access and its evidence
  reference, independence from the mapper where applicable, and conflict
  disposition. References are repository artifacts with verified SHA-256
  digests or HTTPS URIs with declared SHA-256 digests for exact-candidate
  review; symbolic placeholders are invalid. The AICPA subject-matter reviewer
  and approver also require owner-approval references. Roles must be held by
  distinct people; the mapper
  identity must match the matrix assignment. The mapper's qualification must
  cover the 2017 Trust Services Criteria with Revised Points of Focus – 2022
  and ESAF-1600.
- Two distinct exact-subject review attestations for inventory/specification
  and security/overclaiming. Each attestation names a reviewer that matches
  the corresponding roster role and records qualification basis, independence,
  conflict disposition, authorized source access, review date, findings by
  severity, disposition, and exact review-subject digest.
- A canonical evidence-subject digest computed from the manifest's substantive
  feasibility payload, declared input path/digest pairs, and sorted B005
  participant roster, excluding review attestations. This avoids a
  self-referential digest while ensuring changed inputs, feasibility claims,
  or participant roles invalidate the attestations.

The evidence-subject digest identifies the exact feasibility payload and
assessed inputs reviewed; it is not a substitute for the repository's exact
candidate SHA. An enclosing commit cannot be embedded in a file that is itself
part of that commit without a circular identity. Repository pull-request
reviews and publication gates remain responsible for attesting the final Git
candidate SHA. The manifest's SHA-256, pinned by the matrix, covers the
attestation identities, qualifications, access and independence statements,
findings, and dispositions. The renderer independently verifies that pinned
digest and each declared input digest. Any change to manifest attestations
therefore requires a new pinned manifest digest and is visible in the reviewed
candidate diff. Any substantive feasibility payload, input, or participant
roster change requires new attestations for the resulting evidence-subject
digest.

The manifest digest and roster fields establish integrity and record
attestations; they do not independently prove a person's identity,
qualifications, source access, owner authorization, or the truth of a
feasibility claim. Exact-candidate publication review must verify those claims
against the referenced attributable evidence before relying on a complete
status.

To prevent dependency cycles, feasibility inputs may include only source,
inventory, and probe-evidence artifacts. They shall not include the readiness
matrix, this evidence manifest, or generated readiness review. The renderer
shall reject forbidden paths and duplicate normalized paths before checking
digests. The matrix may pin the manifest digest; the manifest may pin only the
permitted evidence inputs.

The schema will reject unknown fields, missing or duplicate B005 participant
roles, duplicate people, incorrect mapper identity, missing qualifications,
access or independence evidence, absent owner approval, duplicate or forbidden
input paths, malformed or stale digests, unsupported dispositions, unresolved
Critical or Important findings, reviewer identities that differ from their
rostered roles, and an attestation bound to another evidence subject. Exact
final-commit review remains a separate publication gate and must be refreshed
whenever the Git candidate SHA changes.

## Decision flow

1. The renderer verifies the matrix-pinned manifest path and digest.
2. It validates the manifest schema, input paths, input digests, and canonical
   review-subject digest.
3. It derives feasibility and reviewer readiness from positive evidence and
   qualifying attestations; matrix gate labels cannot override missing or
   stale evidence. The resulting readiness status is not proof that the final
   Git candidate passed exact-SHA publication review.
4. It applies the existing source, rights, inventory, blocker, and nonclaim
   requirements. `GO` is possible only when every mandatory gate passes, all
   findings are dispositioned, and no Critical or Important finding remains.
   Otherwise the existing mutually exclusive `HOLD` and `NO_GO` rules apply.
5. The generated review renders concise evidence identifiers and digests, not
   source text or synthetic fixture details.

The production manifest will contain no positive feasibility or reviewer
attestations until actual authorized evidence exists. Consequently this change
must leave the live result at `HOLD`.

## Failure behavior

Invalid, missing, stale, incomplete, contradictory, or unsupported evidence is
a validation error. It cannot be converted to `HOLD` or `GO` by editing a
recorded decision. Existing complete-blocker rules remain the only route to an
evidenced `HOLD`; a terminal blocker remains the only route to `NO_GO`.
Renderer check mode must fail if the generated review is stale.

## Validation

Tests will use temporary files and synthetic digests to cover valid evidence,
input and manifest drift, forbidden dependency cycles, malformed schemas,
duplicate or conflicting reviewers, insufficient
qualifications/access/independence, findings, attestation subject mismatch,
and decision derivation. They will also cover all six B005 participant roles,
mapper identity and qualification, owner approval, and binding review
attestations to the roster. Integration checks will
prove that current SOC 2 data still derives `HOLD`, no source-derived mapping
records are introduced, the catalog remains unchanged, and rendered output is
deterministic. The work will follow repository planner routing, affected
validators, focused tests, full unittest discovery, independent exact-subject
specification/inventory and security/overclaiming review, and exact-candidate
publication checks.

## Alternatives considered

1. **Embed all evidence in the matrix.** This minimizes files but couples
   decision data, probe payloads, and review records, and makes independent
   digest validation difficult to audit.
2. **Create a shared cross-framework evidence schema.** This could reduce
   duplication later, but broadens the current SOC 2 task and risks changing
   existing readiness contracts.
3. **Add a SOC 2-specific evidence manifest pinned by the existing matrix.**
   This keeps the decision surface stable, makes evidence independently
   digest-checkable, and contains scope. This is the selected approach.

## Non-goals

- Obtaining restricted AICPA materials or contacting AICPA.
- Reassessing copyright, permission, or legal sufficiency.
- Creating an AICPA provision inventory, mappings, registry entries, or catalog
  changes.
- Generalizing the evidence model to other frameworks.
- Changing the open issue or representing the present SOC 2 readiness as `GO`.
