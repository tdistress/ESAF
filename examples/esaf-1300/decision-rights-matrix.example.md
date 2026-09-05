# ESAF-1300 decision-rights matrix example (informative)

This worksheet is non-normative enablement for
[ESAF-1300](../../governance/ESAF-1300.md) decision-rights assignments.
Completing it does not establish certification, compliance, or control
satisfaction.

All capability names, roles, assignments, and decisions below are fictional.
The example illustrates selected decision domains from ESAF-1000 §5.4; it
does not prescribe an organization's authority model.

## Fictional context

Northstar Services is reviewing `CAP-042`, a customer-support assistant. Its
governance charter delegates routine architecture and production decisions to
named bodies but sends unresolved material risk beyond those delegations to
the executive steering authority.

## Filled matrix

| Decision domain | Deciding authority | Required consultees | Escalation trigger | Separation or compensating oversight | Decision record |
|---|---|---|---|---|---|
| Architecture | Architecture review board | Technical owner, security, data owner, privacy and legal, operations | A proposed pattern falls outside approved architecture or introduces a material shared-service dependency | The technical owner proposes the design but does not approve it | `ADR-042-03` |
| Production authorization | AI governance council | Business owner, technical owner, security, privacy and legal, risk and compliance, operations | An unresolved material risk, a condition outside delegated authority, or required board review | Delivery roles cannot authorize their own release; the council reviews independent validation and open findings | `GATE-042-PROD-01` |
| Risk acceptance | Executive AI steering authority | Business owner, risk and compliance, security, privacy and legal, AI governance council | Residual risk exceeds the council's delegated authority | The business owner may recommend acceptance but cannot be the sole deciding authority | `RISK-042-07` |

## Reader checks

- One deciding authority is named for each decision domain.
- Consultees are identified before the decision.
- Escalation triggers connect delegated decisions to executive or board
  authority.
- Incompatible responsibilities are separated or have documented
  compensating oversight, as required by ESAF-1000 §5.4.
- Each matrix row points to a version-controlled decision record.

This fictional example is informative and is not conformance evidence.
Organizations remain responsible for their own decision-rights assignments
and retained records.
