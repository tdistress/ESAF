# ESAF-1300 / 1400 / 1700 Breadth Deepen Design

**Status:** Approved for implementation planning

**Date:** 2026-08-29

## 1. Purpose

Deepen the first Working Drafts of ESAF-1300 (Governance Manual), ESAF-1400
(Implementation Guide), and ESAF-1700 (Enterprise AI Data Model) in one
coherent breadth pass so each publication is internally usable without
changing normative force or inventing new control outcomes.

This change shall:

- fill thin sections across all three publications with clarifying operational
  detail, short inline examples, and fuller worksheets under `examples/`;
- allow new `shall` / `should` only where they restate or operationalize
  requirements already established in ESAF-1000, ESAF-1100, the GOV family, or
  (for ESAF-1700 reuse) ESAF-1500;
- keep ESAF-1400 informative (no `shall` of its own);
- bump each publication to Working Draft **0.2.0**; and
- leave the published `v0.9-rc1` repository identity and readiness phase
  unchanged.

## 2. Goals and non-goals

### Goals

- Single breadth pass (Approach A) covering 1300, 1400, and 1700 together.
- Hybrid packaging: one short inline example per thin section; fuller
  worksheets and samples under `examples/esaf-{1300,1400,1700}/`.
- Preserve library relationships: 1300 subordinate to 1000/1100; 1400
  non-normative; 1700 conceptual/logical (not a runtime schema).

### Non-goals

- Machine-readable JSON Schema or API contracts for ESAF-1700.
- New control identifiers, assessment procedures, metrics, or architecture
  patterns.
- Advancing `VERSION.md` / publication phase beyond the current `0.9-rc1`
  published identity.
- Closing GitHub issues `#90`–`#95` or reconciling issue `#55`.
- Template packs that substitute for ESAF-1500 schemas or evidence contracts.
- Mermaid diagram campaigns unless an existing section already requires one
  (prefer tables).

## 3. Selected approach

**Approach A — Single breadth pass (0.2.0 across all three).**

One implementation plan and one primary pull request that audits thin
sections, adds clarifying obligations within the force rules below, adds
inline examples plus `examples/` worksheets, updates READMEs and change
histories, and lightly records the deepen work in project trackers and
`CHANGELOG.md`.

Rejected alternatives:

- **B (staged by publication):** smaller diffs, but three review cycles and
  mid-stream version drift.
- **C (core docs only):** incomplete relative to the hybrid packaging
  decision.

## 4. Normative-force rules

- **ESAF-1300 / ESAF-1700:** New `shall` / `should` must cite or clearly bind
  to an existing ESAF-1000, ESAF-1100, GOV-family, or ESAF-1500 (reuse only)
  obligation. No new control IDs, assessment procedures, or metrics.
- **ESAF-1400:** Remains informative. It shall not introduce a `shall` of its
  own. Restatements of external mandatories stay as pointers; local guidance
  stays `should` / `may`.
- **Conflict rule:** Where a deepened passage conflicts with ESAF-1000,
  ESAF-1100, ESAF-1200, or ESAF-1500, the parent publication governs and the
  deepened text is corrected.
- **Examples:** Informative only. Worksheets shall not be readable as creating
  certification, compliance, waiver, or a new control outcome.

## 5. Per-publication content recipe

Shared pattern for every thin section: **clarify → short inline example →
link to fuller example**.

### 5.1 ESAF-1300

Deepen without inventing controls:

| Area | Deepen with |
|---|---|
| Charters | Minimum field checklist tied to GOV-100; edge case where an existing body absorbs AI remit |
| Decision rights | One filled matrix row (for example production authorization); incompatible-rights edge case |
| RACI | Note on extending columns; open-finding gate consults internal audit |
| Lifecycle gates | Record-completeness checklist pointing at ESAF-1000 §9.3 (not a second contract); withhold vs exception routing |
| Exceptions | One worked six-step walkthrough keyed to GOV-140 elements |
| Artifacts / Records | Inventory-navigation example; version-vs-silent-edit edge case |

### 5.2 ESAF-1400

No new `shall`. Deepen with `should` / `may` and pointers:

| Area | Deepen with |
|---|---|
| Adoption sequence | One capability vignette through steps 1–9 |
| Mapping | One filled mapping-row example; stale-mapping failure callout |
| Phased roadmap | Clarify phase ≠ gate; concurrent-capability edge case |
| Vendor-neutral policy | Capability-class vs product-name contrast |
| Evidence handoff | Capture-at-source mini example; draft vs final gap |
| Failure modes | Keep the list; add early-signal / remediation pointer per mode where thin |

### 5.3 ESAF-1700

| Area | Deepen with |
|---|---|
| Thin entities | Attribute clarification where ambiguous; one short instance sketch (IDs and key fields, not JSON Schema) |
| Evidence / Assessment / Finding | Keep ESAF-1500 reuse; cross-link example showing `scope` / `subject` pointing at `CAP-` / `SYS-` / `AST-` |
| Relationship model | Multi-system / shared-asset edge case |
| Exchange guidance | Omit-vs-placeholder restatement; no new exchange mandates beyond existing 1500/1000 meaning |

Out of scope: new entities, JSON Schema files, control IDs.

## 6. Examples layout

Use the existing top-level `examples/` tree (and the `assessment/examples/`
precedent), not a new `companion/` root.

```
examples/
  README.md
  esaf-1300/
    README.md
    charter-worksheet.md
    decision-rights-matrix.example.md
    exception-workflow.example.md
  esaf-1400/
    README.md
    adoption-vignette.example.md
    capability-control-mapping.example.md
  esaf-1700/
    README.md
    entity-instances.example.md
```

Rules:

- Each core-doc thin section that gains an inline example links to the matching
  fuller file with a relative path.
- Prefer Markdown worksheets for this pass. JSON is optional only when copying
  an existing ESAF-1500 example pattern clearly helps a 1700 cross-ref.
- `examples/README.md` indexes the three packs and states they are
  non-normative enablement, not conformance evidence.
- Inline examples stay short (about one paragraph or one compact table row);
  worksheets hold the rest.

## 7. Delivery, versioning, and trackers

- Bump each of `governance/ESAF-1300.md`, `implementation/ESAF-1400.md`, and
  `data-model/ESAF-1700.md` to **Version 0.2.0** / Working Draft and append a
  change-history row summarizing the breadth deepen.
- Update `governance/README.md`, `implementation/README.md`,
  `data-model/README.md`, and root `README.md` only as needed for accurate
  links to example packs.
- Record the deepen in `CHANGELOG.md` under an Unreleased or post-`v0.9-rc1`
  Working Draft note without claiming a new annotated tag or phase change.
- Update `project/BACKLOG.md` / `project/MILESTONES.md` lightly to distinguish
  first Working Draft (done) from this 0.2.0 breadth deepen (in progress or
  done when merged). Do not reopen closed publication gates.
- Leave `VERSION.md`, the `v0.9-rc1` annotated tag, and
  `docs/superpowers/reviews/2026-08-29-v09-rc1-publication-readiness.md`
  (`phase: published`) unchanged.

## 8. Validation

- Focused tests: example pack paths exist; each core doc links to its pack;
  ESAF-1400 still declares informative status and introduces no document-local
  `shall`.
- Run `python tools/plan_validation.py --base origin/main --candidate HEAD`
  and follow the selected route.
- Run `python -m unittest discover -s tests -v` before merge.
- Run `git diff --check` on the branch; do not commit generated caches or
  `__pycache__`.
- No Mermaid renderer campaign is required unless a Mermaid block is added
  (prefer tables; if a Mermaid block is added, render it with the current
  Mermaid CLI before merge).

## 9. Error handling and review posture

- If a proposed clarifying `shall` cannot be tied to an existing parent
  obligation, rewrite it as informative guidance or drop it.
- If an example appears to create a new obligation, demote it to illustration
  language and strengthen the examples nonclaim.
- Critical and Important review findings on normative overclaiming or broken
  parent citations shall be resolved before merge; lower findings may be
  deferred with a recorded reason.

## 10. Success criteria

The pass is complete when:

1. ESAF-1300, ESAF-1400, and ESAF-1700 are each at Working Draft 0.2.0 with
   thin sections deepened per Section 5;
2. the `examples/esaf-{1300,1400,1700}/` packs exist and are linked from the
   core docs;
3. force rules in Section 4 hold under review and focused tests;
4. required validation in Section 8 passes on the candidate SHA; and
5. `v0.9-rc1` published identity remains unchanged.
