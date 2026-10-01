# NIST AI RMF 1.0 source-readiness design

**Date:** 2026-08-29
**Issue:** [#94](https://github.com/tdistress/ESAF/issues/94)
**Disposition target:** mechanical `GO` after the 2026-10-01 owner-risk
people-gate disposition for Draft-only mapping authorship; independent
qualified reviewers remain deferred

## Exact proposed mapping contract

Direction: `esaf_to_external` only. Excluded: `external_to_esaf`.

Directional question:

> Does exact normative ESAF control requirement text directly support,
> partially support, or establish a prerequisite for the outcome required by
> one authorized, publishable NIST AI RMF 1.0 Core subcategory identifier,
> with each relationship's conditions, expected evidence, and known gaps
> recorded independently, without implying NIST AI RMF compliance, assessment,
> equivalence, certification, authorization, or endorsement?

Scope: `complete_publication`.
Granularity: `ai_rmf_core_subcategory_identifier`.

## Source-readiness oracle

The oracle pins NIST.AI.100-1 / AI RMF 1.0, the official PDF digest
(`7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1`), page
count 48, byte length 1946127, and a 72-subcategory inventory digest
(`4bc3922a9a6ff5ea6c6cd714559ed480b396ee847af854bfe3e8068d693043b2`). PDF
bytes are not committed.

## Publication-rights boundary

The independent rights review records `PASS` for all six ESAF-1600 mapping
field classes under U.S. government work / NIST technical-series practice,
with attribution and no-endorsement constraints.

## Positive feasibility probe

At least one directional probe is feasible using public subcategory outcomes
and exact ESAF normative text (example probe subject: ESAF `GOV-100` against
AI RMF `GOVERN-1.1`). The probe authorizes readiness analysis only; it does
not create a mapping-set, registry, or catalog entry while the matrix is HOLD.

## Mapper and qualified-review contract

Draft-only GO under owner risk names mapper `esaf-project-owner` and defers
independent reviewers for: `nist_ai_rmf_subject_matter`,
`esaf_specification_and_mapping`, `publication_rights`, and
`security_and_overclaiming`. Self-review remains prohibited for any advance to
`reviewed` or `approved`. Inventory/specification and security/overclaiming
reviews must be separate exact-SHA reviews before those lifecycle states.

## GO boundary and reconsideration

Overall `GO` authorizes a separate Draft mapping candidate under ESAF-1600.
Owner-risk people-gate clearance does not complete qualified review and does
not advance Draft artifacts. Lifecycle advance beyond Draft requires naming
independent reviewers, attributable exact-SHA reviews with no open Critical or
Important findings, and continued matrix `GO`.
