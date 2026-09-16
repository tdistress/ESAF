# NIST SP 800-53 Rev. 5 Source Readiness Design

**Status:** Approved for readiness package implementation

**Date:** 2026-09-16

**Issue:** [#194](https://github.com/tdistress/ESAF/issues/194)

## Purpose

Pin NIST Special Publication 800-53 Revision 5 public-source identity,
publication rights, control and enhancement inventory, and a mechanical `GO` /
`HOLD` / `NO_GO` readiness decision without creating unauthorized mapping
artifacts.

## Deliverables

- Publication-rights review (committed first)
- Source-readiness oracle with public PDF digests
- Complete control and enhancement identifier inventory and digest
- Mechanical readiness matrix
- Generated GO/HOLD review via renderer
- Landing page under `crosswalks/nist-sp-800-53.md`
- Issue #194 traceability

## Exact proposed mapping contract

- Direction: `esaf_to_external` only (`external_to_esaf` excluded)
- Granularity: `nist_sp_800_53_rev5_control_or_enhancement_identifier`
- Scope: complete publication when GO is derived
- Positive feasibility probe: public SP 800-53 control and enhancement outcomes
  can be compared to exact ESAF normative control text without inventing
  parallel schemas

## Positive feasibility probe

A sample comparison of ESAF control normative text against a public NIST SP
800-53 Rev. 5 control or enhancement outcome is feasible in principle. No
mapping relationship or negative disposition is recorded while readiness remains
HOLD.

## Mapper and qualified-review contract

Named mapper and independent reviewers are required for GO. Roles include NIST
SP 800-53 subject-matter, ESAF specification and mapping, publication-rights,
and security and overclaiming reviewers, plus an owner-authorized approver.
Exact-SHA dual reviews and findings disposition are required.

## HOLD boundary and reconsideration

Default exit is evidenced HOLD when the people gate is blocked. While HOLD or
NO_GO, create no NIST SP 800-53 mapping relationships, negative dispositions,
snapshots, lifecycle events, registry entries, or catalog increments.
Reconsideration requires named qualified people and attributable exact-SHA
reviews with no open Critical or Important findings.

## Validation and presentation

Renderer `--check` must pass. Catalog counts remain 3 / 404 / 81 / 325. Landing
status shall be exactly `**Status:** Readiness HOLD` when HOLD is derived.
