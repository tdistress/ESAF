# ESAF Architecture Pattern Template

Remove instructional text when authoring a pattern. Pattern content shall remain vendor-neutral; supplier examples are informative and belong in ESAF-1400.

## Metadata

Record pattern ID, title, status, version, owner, reviewers, approval date, review date, pillars, lifecycle stages, capability tiers, deployment models, and supersession.

## Purpose

State the reusable architectural outcome supplied by the pattern.

## Problem statement

Describe the recurring enterprise problem and the consequences of inconsistent design.

## Intended outcomes

List observable security, governance, operational, and business outcomes.

## Non-goals

Identify adjacent problems and implementation choices the pattern does not address.

## Applicability

Define use cases, tiers, risks, deployment contexts, and conditions for using the pattern.

## Assumptions and prerequisites

State required enterprise services, governance decisions, data conditions, competencies, and inherited controls.

## Prohibited uses

Identify conditions in which the pattern cannot support acceptable risk without redesign.

## Architecture views

Provide context, component, flow, deployment, operations, and responsibility views needed to understand the pattern. Number figures according to the ESAF style guide.

## Actors and identities

Identify human and non-human actors, authentication, authorization, privileged roles, delegated authority, and lifecycle responsibilities.

## Data and instruction flows

Identify prompts, instructions, context, enterprise data, retrievals, model artifacts, outputs, memory, feedback, telemetry, classifications, and permitted purposes.

## Trust boundaries

Map components to Z0 through Z7 and document each material crossing according to the boundary-crossing record.

## Components and responsibilities

Define component responsibilities, interfaces, provider-consumer boundaries, dependencies, and control inheritance.

## Required controls

List applicable ESAF-1100 objectives and base controls, including where each control is implemented and who owns evidence.

## Control points and overlays

Define required enforcement points and applicable security, privacy, resilience, deployment, risk, and obligation overlays.

## Architecture decisions and parameters

Record mandatory decisions and organization-defined parameters such as limits, thresholds, review frequency, retention, approval authority, and recovery objectives.

## Failure modes and abuse cases

Analyze foreseeable technical, human, supplier, data, model, and adversarial failures and their detection and containment.

## Fallback recovery and retirement

Define timeout, bounded retry, safe state, fallback, rollback, emergency suspension, recovery, evidence preservation, and decommissioning.

## Evidence and assessment

List required architecture records, operational evidence, assessment questions, and acceptance criteria.

## Variants and alternatives

Describe approved variants, material trade-offs, and when another pattern is preferred.

## Anti-patterns

Describe recurring unsafe or ungovernable designs and why they fail the pattern's objectives.

## Related patterns

Identify primary, supporting, superseding, or incompatible ESAF patterns.

## Change history

| Pattern version | ESAF release | Date | Change |
|---|---|---|---|
| 0.1.0 | 0.4-alpha | 2026-07-11 | Initial draft |
