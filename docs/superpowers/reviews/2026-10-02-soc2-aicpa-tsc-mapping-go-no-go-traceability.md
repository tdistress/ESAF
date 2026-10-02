# SOC 2 AICPA Trust Services Criteria readiness traceability

**Issue:** [#219](https://github.com/tdistress/ESAF/issues/219)

This table traces Issue #219 acceptance criteria to the evidence package and
the status derived by its readiness matrix. It does not authorize substantive
mapping.

| Traceability ID | Issue requirement | Evidence | Status |
|---|---|---|---|
| I219-D1 | Pin the AICPA Trust Services Criteria source identity and exact candidate edition. | Source oracle `publication`; official AICPA resource page. | Complete; latest-version status not asserted. |
| I219-D2 | Record whether authorized source bytes and document-specific terms were obtained. | Source oracle `access` and `source_artifact`. | Complete; bytes and document-specific notice not obtained. |
| I219-D3 | Review public rights evidence before derivative decision analysis. | Publication-rights review committed at `358fb4d8823c7050c2543b5589d4f36fec6f2c9a`; matrix rights-review digest. | Complete; disposition `HOLD`. |
| I219-D4 | Partition ESAF-1600 field classes and state the rights boundary. | Publication-rights review, “ESAF-1600 mapping field-class partition”. | Complete; source-derived classes remain prohibited pending permission. |
| I219-D5 | Assess inventory feasibility without reproducing restricted source text. | Source oracle `inventory`; readiness matrix `provision_inventory` gate. | Complete; no inventory created or count asserted. |
| I219-D6 | Assess ESAF-1600 schema fit and reviewer readiness. | Readiness matrix gates `esaf_1600_and_schema_fit` and `mapper_and_reviewer_readiness`. | Schema fit passes; named mapping and independent review roles remain blocked. |
| I219-D7 | Record evidence, blockers, owners, triggers, re-entry tests, and nonclaims. | Readiness matrix, generated decision review, and `crosswalks/soc-2.md`. | Complete; five reconsiderable blockers remain. |
| I219-GO1 | Derive `GO` only after all gates pass, positive feasibility is evidenced, blockers are cleared, and no Critical or Important findings remain. | Readiness renderer and matrix decision rule. | Not met. |
| I219-HOLD1 | Derive `HOLD` when one or more blocked gates have complete reconsiderable blockers and no terminal blocker exists. | Readiness matrix and generated decision review. | Met; decision is `HOLD`. |
| I219-A1 | Keep mapping artifacts, provision inventories, snapshots, registry entries, and catalog increments at zero under `HOLD`. | Source oracle, crosswalk landing page, renderer tests, catalog validation. | Met; no SOC 2 mapping artifacts or catalog entry exists. |
| I219-A2 | Avoid claims of AICPA authorization, SOC 2 compliance, equivalence, certification, endorsement, or assurance. | Rights review, matrix nonclaims, generated review, and crosswalk landing page. | Met. |

## Decision boundary

This traceability record confirms readiness evidence and project boundaries
only. A future `GO` would authorize a separate mapping candidate and its
independent exact-SHA reviews; it would not establish an AICPA-approved
mapping, SOC 2 compliance, or assurance.
