# ESAF Architecture Pattern Selection and Tailoring

## 1. Purpose

This procedure selects and tailors architecture patterns for an approved AI capability. Selection begins after purpose, ownership, and initial risk classification are established and is revisited upon material change.

## 2. Required inputs

The selecting team shall document:

- approved use case, intended users, affected parties, and outcomes;
- capability tier and risk classification;
- data classifications, purposes, sources, jurisdictions, and retention;
- model source, deployment model, adaptation, and provider relationship;
- external exposure, integrations, tools, actions, memory, and autonomy;
- availability, latency, recovery, safe-state, and retirement needs;
- applicable legal, regulatory, contractual, privacy, security, and accessibility obligations.

## 3. Selection procedure

1. Select the pattern that best represents the capability's principal execution and responsibility model.
2. Select supporting patterns for shared platform, integration, observability, retrieval, action, or deployment functions.
3. Select applicable risk, deployment, data, and obligation overlays.
4. Identify required ESAF-1100 controls, inherited controls, and capability-specific controls.
5. Set organization-defined parameters, including review frequency, thresholds, limits, retention, and approval authority.
6. Document variants, unresolved gaps, and material decisions.
7. Submit the design, decisions, control allocation, and evidence plan for architecture review.

## 4. Primary-pattern decision guide

| Dominant capability characteristic | Primary pattern |
|---|---|
| Shared enterprise access to multiple models with centralized policy | ARC-P100 Enterprise AI platform and gateway |
| General employee assistance in an approved enterprise channel | ARC-P110 Enterprise copilot |
| Responses grounded in governed enterprise knowledge | ARC-P120 Retrieval-augmented generation |
| Planning, delegation, tool use, or consequential action | ARC-P130 Agentic and multi-agent AI |
| Enterprise-operated model inference and lifecycle | ARC-P140 Private model deployment |
| Reusable AI services embedded across applications | ARC-P150 AI integration services |
| Shared evidence, monitoring, evaluation, and operational assurance | ARC-P160 AI observability |

ARC-P160 normally supports another primary pattern. ARC-P100 or ARC-P150 may be a supporting pattern when the capability's primary distinguishing behavior is retrieval or agency.

## 5. Tailoring

Tailoring may add safeguards, narrow applicability, select an approved variant, or set organization-defined parameters. Tailoring shall not remove a required element without a documented decision and governed exception where required.

The tailored record shall identify:

- pattern identifier and version;
- selected variants and overlays;
- included, inherited, modified, and additional controls;
- parameters and assumptions;
- deviations, rationale, approver, conditions, and expiration;
- review triggers and evidence owner.

## 6. Combining patterns

When patterns are combined, the capability design shall identify one primary pattern and describe the responsibility of each supporting pattern. Overlapping control points shall have one accountable owner. Conflicting assumptions or requirements shall be resolved through an architecture decision.

## 7. Reassessment triggers

Selection and tailoring shall be reassessed when the capability changes purpose, users, affected parties, data, model, provider, deployment, jurisdiction, integration, tool, autonomy, scale, exposure, or risk classification, or when a material incident or obligation changes the approved basis.

## 8. Approval and evidence

Architecture approval shall record the selected patterns, versions, overlays, decisions, controls, evidence plan, conditions, and reviewers. The selection record shall remain linked to the capability inventory and production authorization.
