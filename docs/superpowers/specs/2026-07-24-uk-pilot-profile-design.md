# ESAF-1800 United Kingdom Pilot Profile Design

**Status:** Approved for implementation planning

**Date:** 2026-07-24

## 1. Purpose

Define the reusable ESAF-1800 profile contract and publish one conforming
Draft United Kingdom jurisdiction profile for `v0.5-beta`.

The pilot shall:

- apply to AI systems deployed or operated in the United Kingdom, regardless
  of organizational domicile;
- preserve the meanings of all ESAF controls;
- account for the complete 91-control catalog through explicit profile
  selections;
- define bounded additional risks, overlays, and evidence expectations;
- reuse ESAF-1500 assessment and maturity semantics;
- reference the three existing United Kingdom Cyber Essentials mapping sets
  without importing their relationships or treating them as evidence; and
- prove the contract through strict schemas, deterministic validation, focused
  tests, and exact-candidate review.

The profile is a Draft ESAF tailoring artifact. It is not a statement of
United Kingdom law, regulatory compliance, Cyber Essentials implementation or
certification, equivalence, endorsement, external-scheme approval, or
production readiness.

## 2. Owner decisions

The repository owner selected the United Kingdom jurisdiction profile in
GitHub issue `#57` before profile design began.

The approved design decisions are:

1. **Pilot:** United Kingdom jurisdiction profile.
2. **Applicability:** AI systems deployed or operated in the United Kingdom,
   regardless of organizational domicile.
3. **Source boundary:** ESAF and the three pinned United Kingdom Cyber
   Essentials mapping sets already present in the repository. Other United
   Kingdom laws, regulations, and guidance are out of scope.
4. **Control-selection model:** one explicit profile classification for every
   control in the complete ESAF catalog.
5. **Mapping treatment:** immutable, lifecycle-aware references only. Mapping
   relationships and external outcomes are not copied into the profile.
6. **Package architecture:** modular, contract-first, and machine-readable.

## 3. Current state and dependency boundary

ESAF-1500 now defines the shared evidence record, assessment result, and fixed
five-level maturity contracts required by profiles. `profiles/README.md`
requires profiles to reuse those semantics and prohibits profile-local
replacement maturity scales.

The repository currently has no normative ESAF-1800 contract, profile schemas,
profile validator, or published pilot. It does have three separate Draft
United Kingdom mapping sets:

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`;
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`; and
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`.

Those mapping sets remain Draft and await qualified review. The pilot may
identify their existence and lifecycle state, but shall not depend on their
relationships being approved. Profile publication therefore remains
independent from the qualified-review workstream.

## 4. Selected architecture

Use a modular contract-first package.

Create `profiles/ESAF-1800.md` as the concise normative profile contract.
Create strict JSON Schema Draft 2020-12 contracts in `profiles/schema/`.
Publish the pilot at `profiles/uk/0.1.0/` using the canonical profile
identifier `uk--jurisdiction-profile--0.1.0`.

The initial schema version and profile version shall both be `0.1.0`. The
profile lifecycle status shall be `draft`, and the target ESAF release shall
be recorded separately as `v0.5-beta`. A profile version is not an ESAF
release version and does not inherit an ESAF lifecycle status.

The pilot package shall contain:

| Artifact | Responsibility |
|---|---|
| `README.md` | Human-readable purpose, applicability, use, source boundary, Draft status, and limitations. |
| `profile.json` | Identity, version, lifecycle, scope, applicability conditions, source boundary, component paths, and change history. |
| `control-selections.json` | Complete 91-control applicability ledger. |
| `risk-overlays.json` | Additional-risk records and their strengthening overlays. |
| `evidence-expectations.json` | Profile-specific expectations that reuse ESAF-1500. |
| `external-references.json` | Immutable references to the three Draft mapping sets and their lifecycle states. |

This structure separates stable contract concerns from pilot content and keeps
future profiles from inheriting United Kingdom-specific material. A monolithic
manifest would make review and diagnostics harder. A record-per-control
package would create unnecessary file and tooling overhead for the first
pilot.

## 5. Normative ESAF-1800 contract

`profiles/ESAF-1800.md` shall define:

1. purpose and scope;
2. relationship to ESAF-1000, ESAF-1100, ESAF-1500, and ESAF-1600;
3. profile identity, versioning, lifecycle, and change control;
4. applicability and system-boundary requirements;
5. source and authority boundaries;
6. control-selection semantics;
7. additional-risk and overlay semantics;
8. evidence-expectation and assessment semantics;
9. external-reference semantics;
10. traceability and validation requirements; and
11. conformance and non-claim boundaries.

The normative contract shall use `shall`, `should`, and `may` according to
repository conventions. It shall distinguish an ESAF profile requirement from
an assertion about law or an external scheme.

Profiles shall not:

- alter a core control identifier, objective, normative requirement, owner
  role, evidence meaning, or assessment meaning;
- weaken an ESAF requirement;
- treat profile maturity as control conformance or external assurance;
- define a profile-local replacement maturity scale;
- infer an external outcome from an ESAF control or profile overlay;
- claim compliance, certification, equivalence, endorsement, legal
  sufficiency, external approval, or production readiness; or
- advance a referenced artifact beyond its recorded lifecycle state.

## 6. Schema contracts

Create these strict Draft 2020-12 schemas:

- `profile.schema.json`;
- `control-selections.schema.json`;
- `risk-overlays.schema.json`;
- `evidence-expectations.schema.json`; and
- `external-references.schema.json`.

Every object boundary shall reject additional properties. Every component
shall carry the profile identifier, profile version, schema version, and its
repository-relative schema locator. Identifiers shall use closed patterns and
be unique within their namespace.

The reusable schemas shall accept any profile identifier matching the
ESAF-1800 identifier pattern. They shall not pin the United Kingdom pilot
identifier. The reusable lifecycle vocabulary is `proposed`, `draft`,
`approved`, `published`, `deprecated`, and `retired`; the United Kingdom pilot
itself shall remain `draft`.

`profile.json` shall identify all required component paths. Paths shall be
repository-relative, normalized POSIX paths inside the same versioned profile
package. The validator shall reject path traversal, absolute paths, alternate
separators, symlinks, missing components, and unlisted profile artifacts.
The manifest shall list `README.md` as its human document in addition to the
four machine-readable component manifests.

The root manifest shall define a closed applicability-condition catalog.
Each condition shall have:

- a stable condition identifier;
- a concise factual question about the assessed system or its operating
  context;
- the answer type `boolean`;
- `activates_when`, set to either `true` or `false`; and
- the evidence needed to resolve it.

Conditional selections and overlays shall reference these condition
identifiers rather than embed unstructured trigger prose. This makes
applicability resolution machine-readable without creating a general-purpose
policy language.

## 7. Applicability and system boundary

The profile applies when an AI system is deployed or operated in the United
Kingdom. Organizational incorporation, headquarters, or domicile alone does
not determine applicability.

The assessed system boundary shall include supporting infrastructure,
services, suppliers, and operational dependencies when they support or affect
the in-scope AI system. The profile shall require users to record:

- the AI system and business purpose;
- United Kingdom deployment or operating basis;
- included and excluded components;
- supporting infrastructure and services;
- supplier and shared-responsibility boundaries;
- applicable condition answers and supporting evidence; and
- limitations, assumptions, and unresolved scope questions.

The profile does not define the scope of Cyber Essentials or any legal or
regulatory regime.

## 8. Control-selection semantics

`control-selections.json` shall contain exactly one record for every control in
the authoritative ESAF catalog. The validator shall derive the population
from the catalog rather than pin a manually maintained list.

The closed selection vocabulary is:

| Status | Meaning |
|---|---|
| `required` | Selected by this Draft profile for every in-scope system. |
| `conditional` | Selected when one or more referenced applicability conditions resolve to their activating values. |
| `recommended` | Profile guidance expressed with `should`; it does not affect ESAF conformance. |
| `not_selected` | The profile adds no selection for the control; this does not declare the underlying ESAF control inapplicable. |

Every selection shall contain a profile rationale. A `conditional` record
shall reference at least one applicability condition. Other statuses shall not
carry activation conditions.

The classification rules are:

- use `required` only when universal relevance to the approved United Kingdom
  operating scope is justified;
- use `conditional` when system capability, data, exposure, supplier, or
  deployment facts determine selection;
- use `recommended` only for useful strengthening that is not a profile
  requirement; and
- use `not_selected` when the pilot adds no profile-level selection.

No classification may be justified as a legal obligation or as a Cyber
Essentials certification requirement.

## 9. Additional risks and overlays

The pilot may define technical risk lenses supported by ESAF and the pinned
Cyber Essentials source boundary, including:

- exposed AI infrastructure and boundary protection;
- insecure configuration and privileged access;
- vulnerable or unsupported components;
- malware and untrusted software paths;
- cloud and third-party responsibility gaps; and
- incomplete scope, asset, and evidence coverage.

Each risk record shall identify:

- a stable risk identifier;
- a bounded risk statement;
- the in-scope circumstances;
- source-basis references;
- affected ESAF controls; and
- one or more mitigating overlay identifiers.

Each overlay shall identify:

- a stable overlay identifier;
- the profile requirement or recommendation;
- whether it is universal or condition-activated;
- affected controls;
- related risk identifiers;
- related evidence-expectation identifiers; and
- an explanation of how it strengthens implementation without changing core
  control meaning.

All risk and overlay language shall be original ESAF synthesis. The package
shall not reproduce external requirement text or describe these lenses as
United Kingdom law.

## 10. Evidence and assessment semantics

Evidence expectations shall reuse the ESAF-1500 evidence-quality attributes,
assessment methods, determinations, time-boundary rules, finding semantics,
and maturity levels.

Each expectation shall:

- have a stable identifier;
- reference at least one ESAF control or profile overlay;
- describe the evidence purpose and expected artifact class;
- identify applicable ESAF-1500 quality attributes;
- identify any condition that activates the expectation;
- state freshness, scope, or independence strengthening where applicable; and
- preserve the distinction between collected evidence and an assessment
  determination.

A profile may strengthen evidence expectations or maturity criteria. It shall
not weaken cumulative maturity prerequisites, calculate an average maturity
score, replace the five-level scale, or treat a maturity result as conformance.

## 11. External-reference semantics

`external-references.json` shall contain exactly the three approved mapping-set
identifiers listed in Section 3.

Each reference shall record:

- the exact mapping-set identifier;
- its registry path;
- expected lifecycle status `draft`;
- reference use `lifecycle_reference_only`;
- `qualified_review_required: true`; and
- an explicit statement that relationships, external outcomes, and evidence
  are not imported into the profile.

The validator shall resolve each identifier against the actual mapping
registry and reject identifier, path, or lifecycle drift. A later mapping
lifecycle transition requires an explicit profile update. It does not
silently change the profile or advance the profile lifecycle.

## 12. Traceability and application flow

Traceability shall form a closed graph:

1. each additional risk resolves to one or more overlays;
2. each overlay resolves to affected controls and evidence expectations;
3. each evidence expectation resolves to controls or overlays;
4. each conditional selection or overlay resolves to defined applicability
   conditions;
5. each control identifier resolves to the authoritative catalog; and
6. each external reference resolves to its registry record.

The intended application flow is:

1. establish that the AI system is deployed or operated in the United
   Kingdom;
2. define the assessed system boundary;
3. answer the applicability conditions with evidence;
4. resolve the required and conditional control selection;
5. apply applicable overlays and evidence expectations;
6. gather evidence under ESAF-1500;
7. record assessment results and limitations; and
8. report the profile version and Draft status with every result.

The flow does not produce or imply legal compliance, certification, external
assurance, or mapping equivalence.

## 13. Validator and failure behavior

Create `tools/validate_profiles.py`. It shall validate the normative package
structure, schemas, catalog population, reference graph, lifecycle state, and
non-claim boundaries.

Validation shall fail closed and return:

- exit `0` for a valid profile population;
- exit `1` for content or semantic validation failures; and
- exit `2` for operational failures that prevent validation.

Diagnostics shall be deterministic, deduplicated, stably ordered, and use
repository-relative paths. Malformed or schema-invalid data shall produce
diagnostics without a traceback and shall not pollute later global-reference
checks.

The validator shall reject:

- missing, extra, malformed, or duplicate components;
- duplicate or unknown identifiers;
- any missing or duplicate catalog control;
- invalid selection status or condition usage;
- unresolved references or asymmetric reciprocal traceability links;
- component path escape, symlink, or package-boundary violations;
- mapping identifier, path, or lifecycle drift;
- fields or statuses that replace, waive, narrow, or mark a core control
  inapplicable;
- external outcomes presented as profile facts; and
- affirmative claims of compliance, certification, equivalence, endorsement,
  legal sufficiency, external approval, or production readiness.

Machine validation can prohibit replacement and waiver structures, invalid
selection meanings, and known weakening language. It cannot prove the absence
of every semantic weakening in prose. Exact-SHA technical, editorial, and
profile-scope review remains the publication gate for that judgment.

Prohibited-claim checks shall use assertion-aware behavior equivalent to the
ESAF-1500 validator so explicit denials, quotations, and discussion are not
misclassified as positive assertions. Shared logic should be factored into a
small common helper when that can be done without changing existing
assessment-validator behavior. Regression tests shall pin both consumers
before any refactor.

## 14. Testing strategy

Implementation shall use test-driven development.

Focused foundation tests shall verify:

- the normative ESAF-1800 structure and vocabulary;
- repository and profile index integration;
- strict Draft 2020-12 schema construction;
- complete package composition;
- the exact three external references;
- complete and unique coverage of the authoritative control population;
- status-specific selection invariants;
- source and non-claim boundaries; and
- reuse of ESAF-1500 semantics.

Validator tests shall cover:

- one valid profile population;
- every schema and semantic failure class;
- malformed JSON and duplicate JSON keys;
- missing, rogue, and symlinked artifacts;
- path traversal and package escape;
- missing and duplicate controls;
- applicability-condition resolution;
- unresolved and invalid traceability;
- mapping lifecycle drift;
- external-outcome import attempts;
- maturity and control-meaning substitution;
- positive, negated, quoted, and discussed prohibited claims;
- stable diagnostic ordering; and
- direct CLI execution from the repository root.

CI shall run profile validation whenever profile contracts, profile packages,
referenced control metadata, referenced mapping registries, assessment
semantics, the validator, or focused tests change.

## 15. Publication and review gates

The implementation shall update applicable framework, profile, tool,
contribution, backlog, and release metadata. Exactly one Draft pilot profile
shall be published for `v0.5-beta`.

Before publication, run:

- focused profile and validator tests;
- `python -m unittest discover -s tests -v`;
- `python tools/validate_profiles.py --check`;
- `python tools/validate_assessment.py --check`;
- `python tools/validate_controls.py --check`;
- `python tools/validate_architectures.py`;
- crosswalk and generated-catalog validation;
- link validation;
- release gates;
- working-tree and whole-branch `git diff --check`; and
- Mermaid CLI rendering for every changed or added Mermaid block.

Independent technical, editorial, profile-scope, and overclaiming reviews
shall inspect the complete branch diff at the exact final SHA. Critical and
Important findings shall be resolved before publication. Lower-severity
findings shall be resolved or have an explicit disposition.

The pull request shall record:

- the exact reviewed head SHA and merge base;
- the owner selection and source boundary;
- control-selection counts derived from the manifest;
- exact validation results;
- review findings and dispositions; and
- the Draft and non-claim boundaries.

## 16. Explicit non-goals

This work does not:

- interpret United Kingdom law or regulation;
- incorporate UK GDPR, sector regulation, or additional guidance;
- define the scope of Cyber Essentials;
- complete qualified review of any mapping set;
- copy mapping relationships into the profile;
- establish Cyber Essentials or ESAF compliance;
- create an assessment workbook or automated policy engine;
- define all planned ESAF profiles; or
- advance any profile, control, mapping, or architecture beyond its recorded
  lifecycle state.

## 17. Completion criteria

The design is complete when:

- the reusable ESAF-1800 contract is normative and internally consistent;
- the strict component schemas are published;
- exactly one Draft United Kingdom pilot package validates;
- all 91 controls appear exactly once in the selection ledger;
- risks, overlays, evidence expectations, conditions, controls, and mapping
  references form a closed traceability graph;
- ESAF-1500 semantics are reused without replacement;
- the three Draft mappings remain reference-only and separately gated;
- focused and repository-wide validation passes on the exact candidate; and
- the required independent reviews are complete with all Critical and
  Important findings resolved.
