# ESAF-1500 Evidence Catalog (Draft deepen)

**Status:** Draft deepen
**Issues:** [#116](https://github.com/tdistress/ESAF/issues/116) starter;
[#125](https://github.com/tdistress/ESAF/issues/125) deepen

This directory is a non-normative Draft catalog of ESAF-1500 evidence types,
shared contract fields, quality attributes, per-type good-enough versus common
failure notes, and a small set of fictional filled evidence records. It reuses
the shared evidence contract; it does not define a parallel evidence model.

- [ESAF-1500 evidence catalog](ESAF-1500-evidence-catalog.md) lists the closed
  `evidence_type` values, required contract fields, quality attributes,
  per-type quality notes, and profile-neutral example uses.
- Filled fictional examples:
  - [`examples/catalog-policy.example.json`](examples/catalog-policy.example.json)
  - [`examples/catalog-interview.example.json`](examples/catalog-interview.example.json)
  - [`examples/catalog-technical-test.example.json`](examples/catalog-technical-test.example.json)
- Authoritative semantics remain in [ESAF-1500](../ESAF-1500.md) and
  [`../schema/evidence-record.schema.json`](../schema/evidence-record.schema.json).

## Nonclaims

This catalog is Draft deepen material only. Using catalog entries does not
establish certification, compliance, equivalence, endorsement, assurance,
production readiness, or lifecycle approval for any Draft ESAF artifact.
