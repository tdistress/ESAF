# Changelog

All notable changes to ESAF are documented in this file.

Versions 0.2-alpha and 0.3-alpha remain unreleased working-draft stages.
Version 0.4-alpha is a tagged Working Draft. Version 0.5-beta is a tagged
Working Draft. Version 0.9-rc1 is a tagged Working Draft. Version 0.10-draft
is an unreleased Working Draft closure candidate.

## 0.10-draft - Unreleased

### Added

- Added non-normative worksheet and worked-example packs for ESAF-1300,
  ESAF-1400, and ESAF-1700 under
  [`examples/esaf-1300/`](examples/esaf-1300/),
  [`examples/esaf-1400/`](examples/esaf-1400/), and
  [`examples/esaf-1700/`](examples/esaf-1700/).
- Added a Draft ESAF-1500 assessment workbook starter under
  [`assessment/workbook/`](assessment/workbook/) with operator guidance and
  schema-conforming worksheet stubs.
- Added a Draft ESAF-1500 evidence catalog starter under
  [`assessment/evidence-catalog/`](assessment/evidence-catalog/).
- Added a Draft ESAF-1500 audit checklist starter under
  [`assessment/audit-checklist/`](assessment/audit-checklist/).
- Added a Draft governance template starter pack under
  [`templates/`](templates/) for risk, exception, decision, and retirement
  records.
- Added the Issue #119 `v0.10-draft` publication-readiness evidence candidate,
  release-gate validator, and exact-SHA review records, starting at
  [`docs/superpowers/reviews/2026-09-05-v010-draft-publication-readiness.md`](docs/superpowers/reviews/2026-09-05-v010-draft-publication-readiness.md).

### Changed

- Advanced Working Draft status surfaces to `0.10-draft` for the exact
  metadata-only closure candidate. Publication remains conditional on the
  remote annotated `v0.10-draft` tag resolving to the exact validated merged
  commit. The tag has not been created, and the post-merge gate remains open.
- Completed the ESAF-1300 0.2.0 breadth deepen with expanded governance
  charters, decision rights, lifecycle-gate operation, RACI, exceptions, and
  governance records.
- Completed the ESAF-1400 0.2.0 breadth deepen with an expanded adoption
  sequence, control and architecture mappings, roadmap guidance, evidence
  handoff, vendor-neutral policy, and failure modes.
- Completed the ESAF-1700 0.2.0 breadth deepen with expanded canonical
  entities, relationships, identifier conventions, exchange guidance, and
  alignment to ESAF-1500 assessment records.

## 0.9-rc1 - 2026-08-29

### Added

- Added the v0.9-rc1 evidence-candidate readiness record and release-gate
  validator, including prerequisite dispositions for Phase 2 hosted-timing
  `DEFER`, ESAF-1300/1400/1700 Working Drafts, and the NIST AI RMF readiness
  `HOLD`.
- Recorded independent technical, editorial, and governance reviews of the
  exact evidence candidate and the immutable published readiness record,
  including the annotated tag object, tagged commit, UTC publication date,
  and issue 95 evidence locators.
- Carried forward the seven Draft architecture patterns in the current
  Working Draft: ARC-P100, Enterprise AI platform and gateway; ARC-P110,
  Enterprise copilot; ARC-P120, Retrieval-augmented generation; ARC-P130,
  Agentic and multi-agent AI; ARC-P140, Private model deployment; ARC-P150,
  AI integration services; and ARC-P160, AI observability.
- Carried forward the Draft Cyber Essentials v3.3 mapping snapshot.
- Carried forward the Draft Cyber Essentials Plus v3.2 `esaf_to_external`
  mapping snapshot.
- Carried forward the Draft Cyber Essentials Plus v3.2 `external_to_esaf`
  mapping snapshot.

### Changed

- Published the `v0.9-rc1` Working Draft through the annotated `v0.9-rc1`
  tag. Prerequisite dispositions remain Phase 2 timing `DEFER`,
  ESAF-1300/1400/1700 Working Drafts, and NIST AI RMF `HOLD`. Issues 55 and
  60 remain open.
- Clarified that publication does not establish certification, compliance,
  equivalence, endorsement, assurance, legal sufficiency, implementation
  assessment, production readiness, or replacement of qualified professional
  judgment.

## 0.5-beta - 2026-08-01

### Added

- Added the ESAF-1500 assessment foundation and one Draft UK pilot profile.
- Recorded the PCI DSS mapping-readiness decision as `HOLD`.
- Added v0.5 release validation and authenticated evidence-collection tooling.
- Added the immutable published readiness record, including the annotated tag
  object, tagged commit, UTC publication date, and issue 59 evidence URL.
- Carried forward the seven Draft architecture patterns in the current
  Working Draft: ARC-P100, Enterprise AI platform and gateway; ARC-P110,
  Enterprise copilot; ARC-P120, Retrieval-augmented generation; ARC-P130,
  Agentic and multi-agent AI; ARC-P140, Private model deployment; ARC-P150,
  AI integration services; and ARC-P160, AI observability.
- Carried forward the Draft Cyber Essentials v3.3 mapping snapshot.
- Carried forward the Draft Cyber Essentials Plus v3.2 `esaf_to_external`
  mapping snapshot.
- Carried forward the Draft Cyber Essentials Plus v3.2 `external_to_esaf`
  mapping snapshot.

### Changed

- Published the `v0.5-beta` Working Draft through the annotated
  `v0.5-beta` tag. Owner-risk acceptance is the uniform basis for the three
  Draft UK mapping sets; qualified review remains deferred, all mapping sets
  and records remain Draft, and issue 55 remains open.
- Clarified that publication does not establish qualified review, mapping
  approval, artifact lifecycle approval, certification, compliance,
  equivalence, endorsement, external scheme approval, assurance, legal
  sufficiency, implementation assessment, production readiness, or
  replacement of qualified professional judgment.

## 0.4-alpha - 2026-07-23

### Added

- Defined the normative ESAF-1200 architecture method.
- Added ten architecture principles and eight reusable logical trust zones.
- Added pattern selection, tailoring, overlay, and architecture decision methods.
- Added the canonical architecture pattern template and seven-pattern registry.
- Added deterministic architecture validation, unit tests, and continuous integration enforcement.
- Added ARC-P100, Enterprise AI platform and gateway, defining centrally governed and federated enforcement.
- Added ARC-P110, Enterprise copilot, defining governed employee-facing AI assistance.
- Extended architecture validation to enforce pattern metadata, registry linkage, required sections, and control-reference integrity.
- Added ARC-P120, Retrieval-augmented generation, defining governed dual-pipeline retrieval with federated knowledge, authorization-before-exposure, grounding, and citation controls.
- Added ARC-P130, Agentic and multi-agent AI, defining bounded-authority systems with transactional action execution, attenuated delegation, and independent outcome assurance.
- Added ARC-P140, Private model deployment, defining governed private model hosting and operation.
- Added ARC-P150, AI integration services, defining governed integration boundaries and service controls.
- Added ARC-P160, AI observability, defining lifecycle-aligned telemetry and assurance.
- Hardened ARC-P160 through focused review and validation changes.
- Added the machine-validated draft Cyber Essentials v3.3 crosswalk with 116 atomic provision records, 41 forward-only relationship legs, and 76 specific no-direct-mapping dispositions.
- Added source-rights evidence, deterministic catalogs, focused semantic tests, and acceptance traceability for the Cyber Essentials v3.3 validated draft.
- Recorded the Cyber Essentials snapshot as early Draft 0.5-beta work; it does not complete that milestone.
- Added the Draft Cyber Essentials Plus v3.2 `esaf_to_external` snapshot with 144 records and 8 forward-only relationship legs.
- Added the separate Draft Cyber Essentials Plus v3.2 `external_to_esaf` snapshot with 144 records, 32 reverse-only relationship legs, and 112 specific no-direct-mapping dispositions.

### Changed

- Advanced release metadata to the Initial Reference Architecture Draft Library stage.
- Recorded that the remote annotated-tag condition was satisfied for the
  0.4-alpha Working Draft on 2026-07-23.
- Recorded repository-owner risk acceptance as the Working Draft publication
  basis while qualified mapping review remains deferred and all mapping
  snapshots remain Draft.

## 0.3-alpha - Unreleased

### Added

- Defined the ESAF-1100 control architecture, identifiers, lifecycle, baselines, assessment methods, and evidence model.
- Defined objectives for all sixteen control families.
- Added the canonical control authoring template and machine-validatable metadata schema.
- Defined control inheritance, organization-defined parameters, and external mapping semantics.
- Added the first fourteen normative base-control drafts across the GOV, STR, and RSK families.
- Added thirteen normative base-control drafts across the IAM and DAT families.
- Added eighteen normative base-control drafts across the MOD, APP, and API families.
- Added thirteen normative base-control drafts across the INF and AGT families.
- Added twelve normative base-control drafts across the OPS and MON families.
- Added ten normative base-control drafts across the CMP and AUD families.
- Added eleven normative base-control drafts across the EDU and ARC families, completing initial coverage of all sixteen families.
- Added deterministic control validation and generated human- and machine-readable catalogs.
- Added continuous integration checks for control schema, structure, linkage, coverage, indexing, and generated-output drift.

### Changed

- Updated the editorial style guide with approved control-numbering and metadata conventions.

## 0.2-alpha - Unreleased

### Added

- Expanded ESAF-1000 into a substantive normative enterprise standard.
- Defined scope, conformance, governance, risk planning, portfolio, lifecycle, and assurance requirements.
- Established Protect AI, Utilize AI, and Govern AI requirements.
- Defined minimum governance artifacts, illustrative capability tiers, roles, references, and maintenance triggers.

## 0.1-alpha - Foundation Draft

### Added

- Established the initial repository and publication structure.
- Added the project charter, governance guide, roadmap, editorial style guide, glossary, and contribution guide.
- Added GitHub contribution templates and repository hygiene configuration.
- Initialized all control-family directories.
- Added priority crosswalk placeholders for PCI DSS, HITRUST CSF, and UK Cyber Essentials.

### Corrected

- Corrected encoding corruption in foundational documents.
