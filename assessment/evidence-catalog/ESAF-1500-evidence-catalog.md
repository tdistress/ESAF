# ESAF-1500 Evidence Catalog

**Status:** Draft deepen
**Authority:** [ESAF-1500](../ESAF-1500.md) evidence-record contract and
[`evidence-record.schema.json`](../schema/evidence-record.schema.json).
**Issues:** [#125](https://github.com/tdistress/ESAF/issues/125) deepen;
[#183](https://github.com/tdistress/ESAF/issues/183) second deepen

## Purpose

Give operators, profile authors, and crosswalk authors a reusable index of
ESAF-1500 evidence types and expectations. Entries stay profile- and
framework-neutral unless marked as examples.

## Required contract fields (every evidence type)

Every evidence record reuses the ESAF-1500 fields without renaming them:

| Field | Expectation |
|---|---|
| `$schema` | Repository-relative schema locator |
| `schema_version` | `0.1.0` |
| `evidence_id` | Stable `^EVD-[A-Z0-9][A-Z0-9-]*$` identifier |
| `title` / `description` | Concise name and supported fact or condition |
| `evidence_type` | One closed type from the table below |
| `source` | Originating identity and locator |
| `custodian` | Accountable evidence owner |
| `collected_at` / `collection_method` | Collection time and method |
| `scope` / `period` / `population` | Assessed boundary, period, and population or sample |
| `quality` | Seven attribute evaluations plus sufficiency |
| `integrity` | Digest pair or protected-record locator and verification method |
| `limitations` | Known gaps, or an explicit empty array |
| `retention` | Retention authority and end condition |
| `traceability` | Requirement, procedure, and result references |

When `evidence_type` is `other`, also complete `other_type_description`.

## Quality attributes

Evaluate every evidence record against these ESAF-1500 attributes; do not invent
parallel quality vocabulary:

| Attribute | Meaning |
|---|---|
| `relevance` | Bears on the assessed use, requirement, scope, and period |
| `reliability` | Source and collection method support dependable use |
| `completeness` | Covers the defined population, sample, and needed facts |
| `timeliness` | Current enough for the recorded assessment period |
| `attribution` | Identifies originating person, role, system, or accountable party |
| `integrity` | Protected from unauthorized alteration and verifiable |
| `traceability` | Linked to requirement, procedure, result, and supported findings |

Record `sufficiency` separately as `sufficient`, `limited`, or `insufficient`.
Do not average attribute ratings into sufficiency.

## Evidence types

| `evidence_type` | Expected attributes (beyond shared fields) | Example uses (neutral) |
|---|---|---|
| `policy` | Approved scope, version, and accountable issuer | Enterprise AI policy excerpt cited for GOV requirements |
| `procedure` | Controlled steps, owners, and applicability | Gate operating procedure used during Examine work |
| `record` | Attributable transactional or decision artifact | Gate decision log entry for a named capability version |
| `configuration` | System or control setting with effective period | Model-gateway allowlist export for a production boundary |
| `log` | Time-bounded event stream with source identity | Access or change log slice for the assessment period |
| `technical_test` | Method, expected result, and observed outcome | Control Test script output for a sampled safeguard |
| `observation` | Observer identity, time, and observed condition | Direct Observe notes from a live approval workflow |
| `interview` | Interviewee role, questions, and recorded answers | Interview notes with a control owner |
| `metric` | Definition, window, and measurement method | Latency or quality metric supporting operating effectiveness |
| `contract` | Parties, obligations, and effective dates | Provider processing terms relevant to data handling |
| `external_assurance` | Issuer, scope, and assurance period | Independent report used only within its stated scope |
| `other` | Mandatory `other_type_description` naming the artifact class | Artifact that fits no closed type; keep rare and specific |

## Per-type quality notes

Use these short Draft deepen notes when judging whether a collected artifact is
good enough for an ESAF-1500 evidence record. Notes are profile-neutral coaching
aids; they do not add normative requirements and do not replace the shared
quality attributes or sufficiency values.

### `policy`

- **Good-enough:** Approved text with version, issuer, and an applicability
  statement that covers the assessed use and period.
- **Common failure:** Draft or undated policy text, missing approval, or a
  scope that does not cover the assessed system or population.

### `procedure`

- **Good-enough:** Controlled steps with owners, entry conditions, and a clear
  applicability boundary for the assessed activity.
- **Common failure:** Informal how-to notes, orphan steps without owners, or a
  procedure that no longer matches the operating system under review.

### `record`

- **Good-enough:** An attributable transactional or decision artifact that
  shows who acted, what was decided, and when it occurred.
- **Common failure:** Editable scratch notes, missing actor identity, or a
  record that cannot be tied to the assessed object or period.

### `configuration`

- **Good-enough:** System or control settings with an effective period and a
  source identity that can be re-exported or verified.
- **Common failure:** Screenshots without provenance, settings from the wrong
  environment, or exports that omit the effective window.

### `log`

- **Good-enough:** A time-bounded event stream with source identity and enough
  fields to reconstruct the sampled activity.
- **Common failure:** Truncated windows, clocks that cannot be trusted, or
  filters that hide the population claimed in the evidence record.

### `technical_test`

- **Good-enough:** Stated method, expected result, observed outcome, and the
  sample or target that was exercised.
- **Common failure:** Pass/fail claims without method detail, unrecorded
  environment, or outcomes that cannot be reproduced from the retained output.

### `observation`

- **Good-enough:** Observer identity, observation time, and a concrete
  condition tied to the assessed workflow.
- **Common failure:** Second-hand summary, undated notes, or observations that
  describe intent rather than what was seen.

### `interview`

- **Good-enough:** Interviewee role, questions asked, and recorded answers that
  can be traced to the assessed requirement.
- **Common failure:** Anonymous paraphrases, leading questions without
  retained prompts, or answers that contradict retained records without a
  limitation note.

### `metric`

- **Good-enough:** Metric definition, measurement window, method, and the
  population or system the metric represents.
- **Common failure:** Dashboard screenshots without definitions, mixed units,
  or windows that do not match the assessment period.

### `contract`

- **Good-enough:** Named parties, obligations relevant to the assessed use, and
  effective dates that cover the period.
- **Common failure:** Marketing summaries, expired terms, or redactions that
  remove the obligation being relied upon.

### `external_assurance`

- **Good-enough:** Issuer identity, stated scope, and assurance period that the
  assessor uses only within those bounds.
- **Common failure:** Treating an out-of-scope report as covering the assessed
  system, or ignoring explicit report limitations.

### `other`

- **Good-enough:** A precise `other_type_description`, plus enough provenance
  and quality narrative to explain why no closed type fits.
- **Common failure:** Using `other` as a dumping ground for ordinary policy,
  log, or record artifacts that already have closed types.

## Filled fictional examples

These Draft deepen examples are keyed to catalog types and validate against the
ESAF-1500 evidence-record schema. They are fictional and non-authoritative:

| Type | Path |
|---|---|
| `policy` | [`examples/catalog-policy.example.json`](examples/catalog-policy.example.json) |
| `interview` | [`examples/catalog-interview.example.json`](examples/catalog-interview.example.json) |
| `technical_test` | [`examples/catalog-technical-test.example.json`](examples/catalog-technical-test.example.json) |
| `procedure` | [`examples/catalog2-procedure.example.json`](examples/catalog2-procedure.example.json) |
| `log` | [`examples/catalog2-log.example.json`](examples/catalog2-log.example.json) |
| `metric` | [`examples/catalog2-metric.example.json`](examples/catalog2-metric.example.json) |

Second-deepen examples use `EVD-CAT2-*` identifiers and illustrate
`procedure`, `log`, and `metric` types not covered by the first deepen set.

## Profile and crosswalk use

Profiles and crosswalks may cite these types when stating evidence expectations.
They should not redefine field names, quality attributes, sufficiency values, or
evidence identifiers. Framework-specific examples belong in the profile or
crosswalk package and must remain labeled as examples.

## Nonclaims

This Draft deepen does not approve certification, compliance, equivalence,
endorsement, assurance, or production readiness. Catalog reuse does not create
mapping completeness, control satisfaction, or lifecycle approval.
