# Cyber Essentials v3.3 Draft Crosswalk Traceability

**Candidate baseline:** `5de9ff356ddad1e193444cd7308eff16ed83e811`

**Mapping set:** `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`

**Status:** Draft acceptance evidence; independent candidate review and pull-request integration remain separate gates.

## Acceptance evidence

| Criterion | Acceptance requirement | Repository evidence | Status before candidate review |
|---:|---|---|---|
| 1 | Source and publication-rights evidence are fixed and attributed. | Snapshot `README.md`; `crosswalks/uk-cyber-essentials.md`; focused source, digest, rights, and OGL tests. | Enforced locally. |
| 2 | All 116 prescriptive provisions appear exactly once. | `PROVISION_INVENTORY.md`; locked provision oracle; 116 direct-child records; exact inventory/order/group tests. | Enforced locally. |
| 3 | Every provision has defensible forward legs or a specific negative rationale. | Provision records; whole-snapshot semantics test; 41 relationship legs and 76 negative dispositions in generated catalog. | Enforced locally. |
| 4 | Every relationship resolves to the pinned ESAF manifest. | `ESAF_CONTROL_MANIFEST.json`; whole-snapshot version-resolution test; crosswalk validator. | Enforced locally. |
| 5 | Landing page and catalogs expose draft status, counts, and prominent gaps. | `crosswalks/uk-cyber-essentials.md`; snapshot `README.md`; `crosswalks/CATALOG.md`; `crosswalks/catalog.json`; narrative and catalog-agreement tests. | Enforced locally. |
| 6 | Focused, full-suite, crosswalk, migration, control, architecture, baseline, link, and diff checks pass. | Task 10 final-gate command set and task report. | Passed on the replacement candidate content before commit. |
| 7 | Two independent reviewers report no unresolved Critical or Important findings. | Exact-SHA specification/inventory review and security/overclaiming review. | Pending immutable candidate review. |
| 8 | The protected-branch workflow passes after merge. | Pull-request checks and post-merge protected-branch workflow. | Pending pull request and merge. |
| 9 | Snapshot remains draft pending qualified human review. | Snapshot and all records use `status: draft`; registry has `events: []`; draft-state tests. | Enforced locally. |

## Independent-review procedure

1. Create the candidate commit only after every local gate passes and generated outputs are stable.
2. Record the exact candidate SHA and generate the complete merge-base-to-candidate diff.
3. Dispatch one independent specification/inventory review and one independent security/overclaiming review against that exact immutable SHA.
4. Resolve every Critical and Important finding. Fix lower-severity defects or record an explicit acceptance rationale.
5. If the candidate changes, rerun affected and final gates, create a new candidate SHA, and repeat both independent reviews.
6. After both reviews approve the same exact SHA, make no repository changes. Record review closure in pull-request comments or check artifacts so the reviewed head remains immutable.
7. Merge only after required checks pass and the pull request reports a clean merge state. Verify the protected-branch workflow on the merge commit.

Independent technical review does not populate schema reviewer or approver fields and does not advance the snapshot beyond draft. A qualified Cyber Essentials subject-matter review and a separate governance decision are required for later lifecycle transitions.
