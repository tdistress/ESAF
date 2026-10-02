# NIST CSF 2.0 owner-risk Draft mapping design

**Date:** 2026-10-02
**Approach:** Owner-risk Draft path (Approach 1)
**Owner authorization:** Repository owner directed that independent
qualified reviewers are not required for this item, selected Approach 1,
and authorized commit, push, and merge.

## Purpose

Clear the NIST CSF readiness people-gate blocker under explicit owner
disposition, derive matrix `GO`, and author a complete Draft
`esaf_to_external` mapping set for all 106 CSF 2.0 subcategory
identifiers. Qualified review remains deferred. Lifecycle remains Draft.

## Non-goals

- Do not advance mapping-set or record status to `reviewed` or `approved`.
- Do not claim NIST approval, endorsement, certification, equivalence,
  compliance, assessment, assurance, or legal sufficiency.
- Do not permanently remove the people gate for other frameworks.
- Do not author `external_to_esaf` relationships.
- Do not close Issues #55 or #60.

## Owner disposition for the people gate

The readiness matrix currently derives `HOLD` solely because
`mapper_and_reviewer_readiness` is `BLOCKED` (`NIST-CSF-READINESS-B001`).
Source identity, authorized artifact, publication rights, inventory,
semantic feasibility, ESAF-1600 fit, and overclaiming controls already
`PASS`.

Under this design:

1. The ESAF Project Maintainer / repository owner is the named mapper.
2. Independent qualified-review seats remain unfilled.
3. The owner accepts residual readiness risk for **Draft-only** mapping
   authorship, with `qualified_review_status: deferred`.
4. The people gate becomes `PASS` with evidence pointing to this design and
   the recorded owner disposition review, blockers are cleared, and
   `recorded_decision` becomes `GO`.
5. Owner risk acceptance never represents completed qualified review.

This mirrors the NIST AI RMF and UK Working Draft `owner_risk_acceptance`
pattern at the readiness layer for one public framework, without rewriting
ESAF-1600 reviewed/approved rules.

## Mapping contract

Unchanged from the readiness design:

- Direction: `esaf_to_external` only
- Scope: `complete_publication`
- Granularity: `nist_csf_2_0_subcategory_identifier`
- Population: the pinned 106-identifier inventory
- Default when ESAF does not expressly provide the subcategory outcome:
  `no_direct_mapping`
- Positive relationships use exact normative control text and record
  independent `conditions`, `expected_evidence`, and `known_gaps`
- Relationship vocabulary: `supports`, `partially_supports`, `prerequisite`

## Snapshot identity

- Authority: `nist`
- Publication: `csf`
- Source version: `2.0`
- ESAF release pin: `0.17-draft` at the exact control-catalog commit used
  for the manifest
- Mapping-set version: `0.1.0`
- Mapping-set ID:
  `nist--csf--2.0--esaf-0.17-draft--0.1.0`
- Path:
  `crosswalks/mappings/nist/csf/2.0/0.17-draft/0.1.0/`
- Registry:
  `crosswalks/registry/nist--csf--2.0--esaf-0.17-draft--0.1.0.md`
  with `events: []`

Publication rights reuse the existing PASS rights review. Mapper identity
uses `esaf-project-owner`. No schema `reviewer` or `approver` fields on
the Draft mapping set.

## Repository surface updates

- Landing `crosswalks/nist-csf.md` becomes Readiness GO with Draft
  mapping present and nonclaims retained.
- Regenerated go/no-go review matches the matrix.
- Traceability records the owner disposition and Draft authorship.
- `crosswalks/catalog.json` / `CATALOG.md` regenerate.
- Current and historical Working Draft readiness records update
  `nist_csf` disposition to `GO` where they pin the live landing path,
  and update derived `scope` mapping counts so live gate checks remain
  coherent. Publication identity and closed gate truth for published
  records remain immutable.
- Matching release-gate prerequisite expectations and focused readiness
  tests update from HOLD to GO for NIST CSF only.

## Success criteria

- Matrix derives `GO`; renderer `--check` passes.
- Snapshot validates under `validate_crosswalks.py --check`.
- Catalog counts reflect one additional mapping set and 106 provisions.
- Mapping remains Draft; no lifecycle events.
- Focused NIST CSF readiness, crosswalk, and release-gate tests pass.
- Full unit suite and proportional publication validation pass on the
  candidate SHA.
