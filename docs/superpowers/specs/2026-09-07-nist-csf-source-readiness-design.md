# NIST CSF 2.0 Source Readiness Design

**Status:** Approved for readiness package implementation

**Date:** 2026-09-07

**Issue:** [#159](https://github.com/tdistress/ESAF/issues/159)

## Purpose

Pin NIST Cybersecurity Framework (CSF) 2.0 public-source identity, publication
rights, provision inventory, and a mechanical `GO` / `HOLD` / `NO_GO` readiness
decision without creating unauthorized mapping artifacts.

## Deliverables

- Publication-rights review (committed first)
- Source-readiness oracle with public PDF digests
- Complete subcategory identifier inventory and digest
- Mechanical readiness matrix
- Generated GO/HOLD review via renderer
- Landing page under `crosswalks/nist-csf.md`
- Issue #159 traceability

## Exact proposed mapping contract

- Direction: `esaf_to_external` only (`external_to_esaf` excluded)
- Granularity: `nist_csf_2_0_subcategory_identifier`
- Scope: complete publication when GO is derived
- Positive feasibility probe: public CSF subcategory outcomes can be compared
  to exact ESAF normative control text without inventing parallel schemas

## Positive feasibility probe

A sample comparison of ESAF control normative text against a public CSF
subcategory outcome is feasible in principle. No mapping relationship or
negative disposition is recorded while readiness remains HOLD.

## Mapper and qualified-review contract

Named mapper and independent reviewers are required for GO. Roles include NIST
CSF subject-matter, ESAF specification and mapping, publication-rights, and
security and overclaiming reviewers, plus an owner-authorized approver.
Exact-SHA dual reviews and findings disposition are required.

## HOLD boundary and reconsideration

Default exit is evidenced HOLD when the people gate is blocked. While HOLD or
NO_GO, create no NIST CSF mapping relationships, negative dispositions,
snapshots, lifecycle events, registry entries, or catalog increments.
Reconsideration requires named qualified people and attributable exact-SHA
reviews with no open Critical or Important findings.

## Validation and presentation

Renderer `--check` must pass. Catalog counts remain 3 / 404 / 81 / 325. Landing
status shall be exactly `**Status:** Readiness HOLD` when HOLD is derived.
