# ESAF Architecture Decisions

Architecture decision records preserve the context and consequences of material choices. Use [`ADR_TEMPLATE.md`](ADR_TEMPLATE.md) for decisions affecting reference patterns or capability implementations.

## ADR required conditions

An ADR is required when a team:

- chooses among materially different architecture variants;
- deviates from a required pattern element;
- accepts a provider constraint affecting portability, control, or responsibility;
- combines components across trust zones in an unanticipated way;
- changes a material identity, data, model, tool, action, provider, or evidence boundary;
- resolves a conflict between patterns or overlays;
- supersedes an earlier material decision.

## States

Decision states are proposed, accepted, rejected, superseded, and retired. Accepted decisions identify an owner and review triggers. Superseded records link to the replacement and remain available for historical interpretation.

## Relationship to exceptions

An ADR documents an architecture choice. It does not authorize a control exception or risk acceptance unless the applicable governance process separately records and approves that action.
