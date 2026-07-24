# ESAF-1500 Minimum Assessment Foundation Design

**Status:** Approved for implementation planning

**Date:** 2026-07-24

## 1. Purpose

Define the minimum shared ESAF-1500 assessment semantics required by ESAF
crosswalks and the `v0.5-beta` pilot profile.

This change shall:

- define a common evidence-record contract and evidence-quality vocabulary;
- define an assessment-result contract for scope, method, time boundary,
  determination, findings, dispositions, limitations, and traceability;
- establish one fixed five-level ESAF maturity scale;
- keep maturity separate from control conformance and external assurance;
- provide machine-readable schemas, examples, validation, and focused
  invariants; and
- link the foundation from applicable assessment, framework, control, profile,
  and project indexes.

The foundation is a reusable contract. It is not an assessment workbook,
certification scheme, audit checklist, governance-template library, or
automated compliance score.

## 2. Current state

`controls/ESAF-1100.md` already defines:

- design and operating effectiveness;
- the assessment methods `Examine`, `Interview`, `Test`, and `Observe`;
- the determinations `satisfied`, `partially satisfied`, `not satisfied`,
  `not applicable`, and `not assessed`; and
- the evidence-quality characteristics relevance, reliability, completeness,
  timeliness, integrity, and traceability.

`AUD-120` additionally requires evidence to be attributable and ties evidence
to each assessment procedure, determination, scope, and period. Control
templates already expect assessment procedures and evidence descriptions.

`assessment/README.md` is only a placeholder. No repository-wide
machine-readable evidence record, assessment-result record, or maturity claim
exists. Profiles therefore have no shared assessment contract to reference.

## 3. Selected approach

Use a contract-first foundation:

1. publish one concise normative ESAF-1500 Markdown document;
2. define closed JSON Schema contracts for evidence records, assessment
   results, and maturity assessments;
3. publish one valid, non-authoritative example of each contract;
4. validate the examples, identifiers, references, cumulative maturity
   prerequisites, and non-claim boundaries with one focused tool; and
5. enforce durable content and validator behavior with focused tests.

A prose-only guide would permit profile-local interpretations of required
fields and scoring. A complete assessment application would exceed the
approved milestone boundary. The selected approach supplies a stable,
enforceable interface without creating a scoring product.

## 4. Normative ESAF-1500 structure

Create `assessment/ESAF-1500.md` as the normative source for the minimum
foundation. It shall use ESAF normative language and contain:

1. purpose and scope;
2. relationship to ESAF-1000, ESAF-1100, ESAF-1600, and ESAF-1800;
3. assessment principles and independence boundaries;
4. evidence-record requirements;
5. evidence-quality evaluation;
6. assessment scope, methods, and time boundaries;
7. assessment-result requirements;
8. findings and dispositions;
9. the five-level maturity model;
10. conformance, maturity, aggregation, and non-claim boundaries;
11. record traceability and change control; and
12. implementation and validation references.

ESAF-1500 shall reuse the ESAF-1100 methods and determination meanings rather
than defining competing vocabularies.

## 5. Evidence-record contract

Create `assessment/schema/evidence-record.schema.json`.

Every evidence record shall contain:

- `$schema`: repository-relative schema locator;
- `schema_version`: `0.1.0`;
- `evidence_id`: stable identifier matching `^EVD-[A-Z0-9][A-Z0-9-]*$`;
- `title`: concise human-readable name;
- `description`: the fact or condition the artifact is intended to support;
- `evidence_type`: a closed value identifying the artifact class;
- `source`: source-system or originating-party identity and source locator;
- `custodian`: accountable evidence owner;
- `collected_at`: RFC 3339 date-time;
- `collection_method`: how the evidence was obtained;
- `scope`: in-scope capability, system, control, requirement, or population;
- `period`: point-in-time date or inclusive start and end dates;
- `population`: defined population and, when sampled, sample and selection
  rationale;
- `quality`: the seven attribute evaluations and an overall sufficiency
  decision;
- `integrity`: digest algorithm and lowercase hexadecimal digest, or a
  documented protected-record locator and verification method;
- `limitations`: non-empty known limitations, or an explicit empty array;
- `retention`: retention authority and end condition; and
- `traceability`: stable references to the assessed requirement, procedure,
  and result that consume the evidence.

The closed `evidence_type` values shall be:

- `policy`;
- `procedure`;
- `record`;
- `configuration`;
- `log`;
- `technical_test`;
- `observation`;
- `interview`;
- `metric`;
- `contract`;
- `external_assurance`; and
- `other`.

`other` shall require a specific type description.

### 5.1 Evidence quality

The seven required quality attributes are:

1. relevance;
2. reliability;
3. completeness;
4. timeliness;
5. attribution;
6. integrity; and
7. traceability.

Each attribute shall contain:

- `rating`: `adequate`, `limited`, `inadequate`, or `not_evaluated`; and
- `rationale`: a non-empty explanation tied to the assessed use.

The evidence record shall also contain:

- `sufficiency`: `sufficient`, `limited`, or `insufficient`;
- `evaluated_by`: named individual or accountable role;
- `evaluated_at`: RFC 3339 date-time; and
- `sufficiency_rationale`: non-empty explanation.

Sufficiency shall be explicit. It shall not be calculated by averaging
attribute ratings. `limited`, `inadequate`, or `not_evaluated` attributes shall
remain visible even when the evaluator concludes that the evidence is
sufficient for a narrowly stated use.

## 6. Assessment-result contract

Create `assessment/schema/assessment-result.schema.json`.

Every assessment result shall contain:

- `$schema`: repository-relative schema locator;
- `schema_version`: `0.1.0`;
- `result_id`: stable identifier matching
  `^ASR-[A-Z0-9][A-Z0-9-]*$`;
- `status`: `draft` or `final`;
- `title`;
- `assessor`: identity, role, organization, and independence statement;
- `assessment_scope`: assessed capability or system, requirements, boundary,
  exclusions, population, and sample;
- `methods`: one or more method records using `examine`, `interview`, `test`,
  or `observe`, with procedure, object, expected result, and actual work
  performed;
- `time_boundary`: assessment start, assessment end, and result date;
- `evidence_refs`: one or more stable evidence identifiers;
- `determination`: one of `satisfied`, `partially_satisfied`,
  `not_satisfied`, `not_applicable`, or `not_assessed`;
- `determination_rationale`;
- `design_effectiveness`: `effective`, `partially_effective`, `ineffective`,
  `not_applicable`, or `not_assessed`;
- `operating_effectiveness`: the same closed values;
- `findings`: finding records with stable identifiers, or an empty array;
- `limitations`: explicit limitations, or an empty array;
- `traceability`: assessed ESAF control or requirement identifiers and any
  applicable external or profile identifiers; and
- `change_history`: version, date, author, and change description.

`not_applicable` shall require an approved applicability rationale and
approver. `not_assessed` shall require a scope-exclusion rationale.

A `final` result shall prohibit unresolved placeholder language, require at
least one method and evidence reference except where `not_assessed` is
justified, and require every included finding to have a valid disposition
state. A `draft` result may record incomplete work but shall not be represented
as final, approved, or sufficient for a conformance claim.

## 7. Finding and disposition contract

Findings are nested within the assessment-result schema as a reusable
definition and exposed through the result's `findings` array.

Each finding shall contain:

- `finding_id`, matching `^FND-[A-Z0-9][A-Z0-9-]*$`;
- `severity`: `critical`, `important`, or `minor`;
- `status`: `open`, `resolved`, or `accepted`;
- `affected_requirement_ids`;
- `statement`;
- `evidence_refs`;
- `owner`;
- `disposition`;
- `identified_at`; and
- `disposition_at`, required when status is `resolved` or `accepted`.

An accepted finding shall also require an acceptance authority, rationale,
expiry or review date, and residual-risk statement. Acceptance records a
governed disposition; it shall not change the underlying determination or
establish control satisfaction.

## 8. Fixed five-level maturity model

Create `assessment/schema/maturity-assessment.schema.json`.

The ESAF maturity scale shall be:

| Level | Name | Meaning |
|---|---|---|
| `M0` | Ad hoc | The capability is absent, materially incomplete, unknown, or performed inconsistently without dependable management. |
| `M1` | Managed | The capability has accountable ownership, planned execution, and repeatable basic operation within the stated scope. |
| `M2` | Defined | The capability uses approved, standardized, documented practices integrated with applicable lifecycle and governance processes. |
| `M3` | Measured | The capability is measured against defined outcomes and thresholds using trustworthy evidence, with exceptions and trends governed. |
| `M4` | Adaptive | The capability uses measured results, change signals, incidents, and lessons to improve predictably while preserving control and evidence integrity. |

The levels are cumulative. A maturity assessment shall contain:

- `$schema`;
- `schema_version`: `0.1.0`;
- `maturity_id`, matching `^MAT-[A-Z0-9][A-Z0-9-]*$`;
- `status`: `draft` or `final`;
- `scope`: the exact assessed unit and exclusions;
- `assessor`: identity, role, organization, and independence statement;
- `assessed_at`;
- `level`;
- `criteria`: one entry for every level from `M0` through the claimed level,
  in ascending order;
- `basis_refs`: evidence and assessment-result identifiers;
- `limitations`;
- `component_results`: optional component maturity references used for a
  roll-up; and
- `change_history`.

Each criterion entry shall contain its level, criterion identifier, statement,
`met` boolean, rationale, and basis references. A final claim above `M0` is
invalid when:

- any prerequisite level is missing;
- any prerequisite criterion is not met;
- a required basis reference is missing or unresolved; or
- the claimed level exceeds the lowest substantiated applicable component
  result.

An organization may define more demanding criteria or dimensions, but shall
not rename the levels, weaken cumulative prerequisites, infer an unassessed
level, or publish a profile-local replacement scale as ESAF maturity.

## 9. Conformance and aggregation boundaries

Control conformance and maturity are independent axes:

- an assessment determination states what the available evidence supports for
  an assessed requirement, scope, and period;
- a maturity level states the substantiated institutionalization of a
  capability within its declared scope; and
- neither result supplies missing evidence for the other.

No maturity level shall:

- convert `not_assessed`, `not_satisfied`, or `partially_satisfied` into
  `satisfied`;
- establish compliance, certification, equivalence, endorsement, or external
  approval;
- establish evidence sufficiency outside the recorded scope and period; or
- imply continuous assurance from point-in-time evidence.

Numeric averaging of ordinal maturity levels is prohibited. A roll-up shall
use the lowest substantiated applicable component level and disclose excluded
or not-assessed components. An organization may publish distributions and
counts, but shall not convert them into an unsupported composite score.

## 10. Examples and validation

Create:

- `assessment/examples/evidence-record.example.json`;
- `assessment/examples/assessment-result.example.json`; and
- `assessment/examples/maturity-assessment.example.json`.

Examples shall be valid, clearly marked non-authoritative, use fictional
identities and systems, and cross-reference one another. They shall not imply
that an ESAF control, profile, external framework, or organization has been
assessed.

Create `tools/validate_assessment.py` with a `--check` interface. The validator
shall:

1. load each assessment schema with strict duplicate-key rejection;
2. validate the three tracked examples;
3. reject duplicate evidence, result, finding, or maturity identifiers;
4. resolve every example reference within the tracked example set;
5. enforce final-result conditions not expressible cleanly in JSON Schema;
6. enforce cumulative maturity prerequisites and lowest-component roll-ups;
7. reject numeric maturity score or average fields;
8. reject final maturity claims whose basis is unresolved;
9. reject conformance-overclaiming fields or assertions; and
10. produce stable, repository-relative diagnostics and a non-zero exit code
    on failure.

The validator shall validate contracts and examples only. It shall not score
an organization, infer determinations, or author findings.

Add the validator to `tools/README.md` and the ordinary repository validation
instructions.

## 11. Repository integration

Update:

- `assessment/README.md` to identify ESAF-1500, schemas, examples, and
  validation;
- `README.md` to link directly to the normative assessment guide;
- `framework/ESAF-1000.md` to link its ESAF-1500 reference;
- `controls/ESAF-1100.md` to delegate shared record and maturity semantics to
  ESAF-1500 without duplicating them;
- `profiles/README.md` to require profiles to reuse ESAF-1500 determinations,
  evidence semantics, and maturity levels;
- `project/MILESTONES.md` and `project/BACKLOG.md` only as necessary to record
  completion after the implementation is merged; and
- applicable link or validation indexes following existing repository
  conventions.

Normative requirements shall remain in `assessment/ESAF-1500.md`. Examples
and implementation notes shall not silently add requirements.

## 12. Test strategy

Create focused tests in:

- `tests/test_assessment_foundation.py`; and
- `tests/test_validate_assessment.py`.

Content tests shall verify:

- required normative sections and terms;
- exact evidence-quality attributes and ratings;
- exact assessment methods and determinations;
- exact maturity levels, names, order, and cumulative rule;
- separation of maturity from conformance;
- the lowest-substantiated-level roll-up rule;
- prohibited averaging and non-claims;
- schema and example links; and
- profile reuse of the shared semantics.

Validator tests shall start with valid temporary fixtures and independently
mutate:

- every required evidence-quality attribute;
- evidence sufficiency;
- result scope, method, time boundary, determination, and traceability;
- `not_applicable` approval and `not_assessed` rationale;
- final-result evidence and finding disposition requirements;
- duplicate and unresolved identifiers;
- each maturity prerequisite;
- basis references and component roll-ups;
- numeric score and averaging fields; and
- conformance-overclaiming fields.

The complete validation set shall be:

```text
python -m unittest tests.test_assessment_foundation -v
python -m unittest tests.test_validate_assessment -v
python -m unittest discover -s tests -v
python tools/validate_assessment.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
git diff --check <merge-base>..HEAD
```

Set `PYTHONDONTWRITEBYTECODE=1`, verify no `__pycache__` directories remain,
and ensure generated caches or temporary assessment output are not committed.
No Mermaid diagram is required. If implementation adds or changes Mermaid,
every affected block shall be rendered with the current Mermaid CLI.

## 13. Review and publication workflow

Implementation shall use the isolated branch and worktree workflow. The
complete branch shall receive:

- independent technical review of the contracts, validator, and maturity
  logic;
- independent editorial review of terminology, normative language, and
  internal consistency;
- independent overclaiming review of conformance, maturity, aggregation, and
  external-assurance boundaries;
- resolution of every Critical and Important finding;
- the complete validation set on the exact reviewed head;
- a reviewable pull request recording the reviewed head SHA and exact gate
  results; and
- verification that the reviewed head remains the pull-request head before
  merge.

After merge, update local `main`, rerun proportional validation, verify issue
`#56` acceptance criteria against the merged commit, close the issue with exact
evidence, and remove only the owned branch and worktree.

## 14. Explicit non-goals

This change shall not:

- create a complete assessment workbook or workpaper system;
- create an audit checklist or governance-template library;
- automate control determinations, finding authorship, or risk acceptance;
- calculate a compliance percentage or composite maturity score;
- define a certification or accreditation method;
- claim compatibility, equivalence, or approval by an external scheme;
- publish a pilot industry profile; or
- advance any existing Draft artifact to a reviewed or approved lifecycle
  state.
