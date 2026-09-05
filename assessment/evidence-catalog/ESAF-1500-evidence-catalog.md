# ESAF-1500 Evidence Catalog

**Status:** Draft starter  
**Authority:** [ESAF-1500](../ESAF-1500.md) evidence-record contract and
[`evidence-record.schema.json`](../schema/evidence-record.schema.json).

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

## Profile and crosswalk use

Profiles and crosswalks may cite these types when stating evidence expectations.
They should not redefine field names, quality attributes, sufficiency values, or
evidence identifiers. Framework-specific examples belong in the profile or
crosswalk package and must remain labeled as examples.

## Nonclaims

This Draft starter does not approve certification, compliance, equivalence,
endorsement, assurance, or production readiness. Catalog reuse does not create
mapping completeness, control satisfaction, or lifecycle approval.
