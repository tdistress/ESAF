# v0.19 Assessment Follow-Through Design

## Status and scope

This design proposes the bounded `v0.19-draft` effort: extend the existing
fictional Summit Analytics `CAP-140` integrated assessment with one example of
finding remediation and follow-up assessment. The work is an ESAF-internal
assessment-use example and an exact-candidate Working Draft publication. It
does not depend on an external framework source, licensed material, or a
qualified external crosswalk verifier.

The gated SOC 2 and HITRUST readiness issues remain unchanged and outside this
scope. No external mapping, source-readiness decision, normative control,
assessment schema, maturity meaning, or lifecycle status change is proposed.

## Context and problem

The published `v0.18-draft` case demonstrates evidence capture, assessment
results, a minor open finding, maturity separation, and governance follow-up.
It does not yet show how an owner records a corrective action, how an assessor
tests the claimed correction, or how the follow-up result relates to the prior
finding and its evidence. A focused continuation can make the existing records
more useful without widening the standard or building a complete assessment
library.

The existing ESAF-1500 contracts already support a new Draft assessment result,
evidence record, finding status and disposition, and change history. ESAF-1100
remains authoritative for the assessment procedure and determination. The
example must not invent schema fields to create links; it can make linkage
explicit in the existing narrative fields, evidence references, finding ID,
requirement/procedure references, and stable artifact links.

## Approaches considered

1. **Extend the current CAP-140 case with one follow-up cycle (recommended).**
   Add a fictional owner action record and one focused reassessment package for
   the existing API-100 emergency-restriction finding. This provides a
   concrete end-to-end learning path while keeping the scope narrow and
   reusing existing contracts.
2. **Create a second integrated case.** This could show a different control or
   organizational context, but it would repeat the integration work and would
   not directly close the current case's open finding.
3. **Add a general remediation workflow or new record contract.** This could
   formalize reusable corrective-action semantics, but it would broaden the
   normative and schema surface and require a separate design and review.

## Recommended design

Keep the initial `ASR-ENG3-API100` result as the original assessment record.
Add an informative fictional follow-up package that:

- links to the original result and `FND-ENG3-API100-EMERGENCY`;
- records a fictional owner, action, completion point, and closure evidence in
  a clearly labeled companion Markdown record, without claiming that this is a
  new ESAF machine contract;
- adds one schema-conforming evidence record for a later emergency-restriction
  exercise, with its own evidence ID, collection period, limitations, and
  traceability to API-100, API-100-A3, and the follow-up assessment result;
- adds a distinct Draft follow-up assessment result using API-100-A3 and the
  new evidence, resolving only the underlying condition associated with the
  original finding while leaving the original result unchanged, retaining the
  original scope boundary, and stating what the follow-up does not retest;
- records a distinct follow-up finding ID as resolved in the follow-up result,
  with a dated disposition identifying the action and verification basis; the
  companion narrative explicitly links it to the original finding because
  findings are nested in exactly one result and identifiers cannot be reused
  across result files;
- gives the follow-up result its own determination and effectiveness judgments
  supported only by the follow-up procedure and evidence; it does not rewrite
  the original result or imply that the original period was reassessed; and
- updates assessment indexes and the integrated-case overview so readers can
  navigate the original finding, action, evidence, and follow-up result.

The package remains fictional, informative, and Draft. It makes no claim of
real-world assurance, certification, compliance, or control effectiveness
beyond the limited illustrated scope. No changes are made to the ESAF-1500 or
ESAF-1100 normative text or machine contracts.

The v0.19 publication uses a dedicated readiness record and executable gate
validator wired into the validation planner and CI. The gate enforces the
`evidence_candidate` to `closure_candidate` to `published` sequence, exact base
and candidate binding, annotated tag identity, and immutable published-to-
published status maintenance. Candidate publication surfaces and readiness
evidence are validated before tagging; a published-status commit records the
tag identity and synchronizes public status surfaces without moving the tag.

## Validation and review

Validate every new assessment and evidence JSON record with the existing
assessment validator. Update focused content-level regression coverage for
the package's links, explicit original-to-follow-up finding cross-reference,
bounded follow-up, and non-claim language. Add deterministic fixture tests for
the readiness validator's phase transitions, candidate/base binding,
annotated-tag binding, and published-to-published immutability. Register the
test module in the shard manifest and wire the validator into the planner and
CI. Run the full unittest suite and every affected assessment,
control, architecture, link, rendering, and release validation selected by the
repository planner. Review the complete branch diff and obtain exact-candidate
technical, editorial, and governance review before publication.

The ordinary Working Draft publication gate applies to the exact candidate.
No qualified external crosswalk reviewer is part of this effort because it
creates no crosswalk records or claims.

## Out of scope

- SOC 2 readiness or mapping (Issue #219) and HITRUST readiness or mapping
  (Issue #60);
- any external framework source, mapping inventory, or compliance claim;
- changing or replacing the original assessment result;
- new machine schemas, identifier types or contracts, normative requirements,
  or maturity semantics;
- a complete remediation program, assessment library, or generalized
  corrective-action model; and
- advancing any artifact lifecycle state beyond repository Working Draft
  publication.
