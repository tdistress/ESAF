# CIS Controls Version 8 Source Readiness Design

**Status:** Approved for readiness package implementation

**Date:** 2026-09-16

**Issue:** [#206](https://github.com/tdistress/ESAF/issues/206)

## Purpose

Pin CIS Critical Security Controls Version 8 (CIS Controls v8) public-source
identity, publication rights under CC BY-NC-ND 4.0, Safeguard identifier
inventory, and a mechanical `GO` / `HOLD` / `NO_GO` readiness decision without
creating unauthorized mapping artifacts.

## Deliverables

- Publication-rights review (committed first)
- Source-readiness oracle with official discovery URLs and inventory digest
- Complete Safeguard identifier inventory and digest
- Mechanical readiness matrix
- Generated GO/HOLD review via renderer
- Landing page under `crosswalks/cis-controls.md`
- Issue #206 traceability

## Exact proposed mapping contract

- Direction: `esaf_to_external` only (`external_to_esaf` excluded)
- Granularity: `cis_controls_v8_safeguard_identifier`
- Scope: complete publication when GO is derived
- Positive feasibility probe: public CIS Controls Version 8 Safeguard outcomes
  can be compared to exact ESAF normative control text without inventing
  parallel schemas

## Edition pin

This package pins **CIS Controls Version 8 (v8)**, which remains officially
published and obtainable via the CIS Version 8 landing and free registration
download pages and the public CIS Controls Navigator for v8. CIS also publishes
**Version 8.1** as an iterative update to v8 (same 153-Safeguard population with
revised descriptions and NIST CSF 2.0 Govern alignment). Retargeting to v8.1
requires a separate readiness refresh and is out of scope for Issue #206.

## Positive feasibility probe

A sample comparison of ESAF control normative text against a public CIS Controls
Version 8 Safeguard outcome is feasible in principle from public Navigator and
framework materials. No mapping relationship or negative disposition is recorded
while readiness remains HOLD. Publication of paraphrases or derivative mapping
analysis remains prohibited under the rights HOLD until CIS approval is
evidenced.

## Mapper and qualified-review contract

Named mapper and independent reviewers are required for GO. Roles include CIS
Controls Version 8 subject-matter, ESAF specification and mapping,
publication-rights, and security and overclaiming reviewers, plus an
owner-authorized approver. Exact-SHA dual reviews and findings disposition are
required.

## HOLD boundary and reconsideration

Default exit is evidenced HOLD when people, rights, or source-access gates are
blocked. While HOLD or NO_GO, create no CIS Controls mapping relationships,
negative dispositions, snapshots, lifecycle events, registry entries, or catalog
increments. Reconsideration requires rights clearance for derivative mapping
analysis where applicable, named qualified people, and attributable exact-SHA
reviews with no open Critical or Important findings.

## Validation and presentation

Renderer `--check` must pass. Catalog counts remain 3 / 404 / 81 / 325. Landing
status shall be exactly `**Status:** Readiness HOLD` when HOLD is derived.
