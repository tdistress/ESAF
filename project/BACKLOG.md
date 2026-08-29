# Backlog

The authoritative work queue should be maintained in GitHub Issues. This file records only high-level initiatives:

Cyber Essentials core and Cyber Essentials Plus remain separate mapping sets.

## Deferred assurance follow-up

- [Issue 55](https://github.com/tdistress/ESAF/issues/55) remains open until
  qualified review is complete for all three exact mapping sets:
  `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`,
  `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`,
  and
  `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`.
  A `v0.5-beta` owner-risk disposition defers this work and does not complete
  qualified review or change a mapping lifecycle state. Repository Markdown
  continues to treat this work as deferred until an evidenced qualified-review
  campaign is recorded, even if the GitHub issue state drifts.

## Separately gated future work

- [Issue 60](https://github.com/tdistress/ESAF/issues/60) tracks HITRUST CSF
  source and review readiness only after licensed-source access, publication
  rights, and qualified-review availability are confirmed. This work does not
  block `v0.5-beta` or `v0.9-rc1`.

## Post-beta scheduled queue

The `v0.9-rc1` initiatives previously queued here are complete. Deferred
mapping assurance and HITRUST readiness remain tracked separately and do not
stop later engineering work. New post-`v0.9-rc1` initiatives shall be filed
under a later milestone before they re-enter this queue.

## Completed workstreams

- [Issue 95](https://github.com/tdistress/ESAF/issues/95), Close the v0.9-rc1
  publication gates, is completed. The `v0.9-rc1` Working Draft was published
  on 2026-08-29 through annotated tag `v0.9-rc1` (tag object
  `1b5cdead5c56c4f209b5cf091c665ca40e709590`) bound to
  `4136cfdc71a85ea2becd0f23c95424e7580cafa3`. Publication closes repository
  release gates only and does not change any artifact lifecycle state.
- [Issue 94](https://github.com/tdistress/ESAF/issues/94), Complete NIST AI RMF
  public-source readiness and mapping go/no-go, is completed through the
  evidenced `HOLD` path pending named mapper and independent reviewers
  (`crosswalks/nist-ai-rmf.md`).
- [Issue 93](https://github.com/tdistress/ESAF/issues/93), Author ESAF-1700
  Enterprise AI Data Model Working Draft, is completed as a linked Working
  Draft at `data-model/ESAF-1700.md`.
- [Issue 92](https://github.com/tdistress/ESAF/issues/92), Author ESAF-1400
  Implementation Guide Working Draft, is completed as a linked Working Draft
  at `implementation/ESAF-1400.md`.
- [Issue 91](https://github.com/tdistress/ESAF/issues/91), Author ESAF-1300
  Governance Manual Working Draft, is completed as a linked Working Draft at
  `governance/ESAF-1300.md`.
- [Issue 90](https://github.com/tdistress/ESAF/issues/90), Close
  validation-harness Phase 2 performance target, is completed. Hot-path
  delivered in PR #97; hosted serial ≥40% timing criterion recorded as
  `DEFER`
  (`docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md`).

- [Issue 59](https://github.com/tdistress/ESAF/issues/59), the `v0.5-beta`
  publication gates, is closed. The `v0.5-beta` Working Draft was published
  on 2026-08-01 through the annotated tag bound to
  `255f8806917aaf8c6a2441152b4638fc9fd2bfda`. The owner-risk-acceptance basis
  permits only Working Draft publication; it does not change any artifact
  lifecycle state or complete the qualified review tracked in issue 55.

- [Issue 58](https://github.com/tdistress/ESAF/issues/58), PCI DSS source
  readiness and mapping go/no-go, is completed through the evidenced `HOLD`
  path. The decision package records the unavailable protected source checksum
  and provision inventory, publication-rights boundary, qualified-review
  contract, blockers, owners, triggers, re-entry tests, and nonclaims without
  creating a PCI DSS mapping artifact.
