# Release Plan

Each release shall complete the following gates:

1. Scope and milestone approved.
2. Normative and technical review completed.
3. Editorial conventions and terminology validated.
4. Internal links and cross-references validated.
5. Required standards mappings reviewed by qualified contributors.
6. Changelog and version metadata updated.
7. Release approved under `GOVERNANCE.md`.

## 0.4-alpha readiness

Architecture content is complete only at Draft level. Publication gates remain Open.

| Gate | Current state | Required closure evidence |
|---|---|---|
| Scope and milestone approval | Open | Approved scope and milestone for the exact candidate SHA. |
| Normative and technical review | Open | Full test suite and all three validators pass on the exact candidate SHA; architecture content remains Draft. |
| Editorial and terminology review | Open | Global link and terminology review completes without unresolved release-blocking findings. |
| Cross-reference and rendering review | Open | Internal cross-references are validated, and every Mermaid diagram is rendered and reviewed for readability. |
| Standards mapping review | Open | When mappings are in scope, qualified mapping review is completed by qualified contributors. |
| Release metadata synchronization | Open | Changelog, version, roadmap, architecture registry, backlog, and release-plan metadata are synchronized on the exact candidate SHA. |
| Governance approval | Open | Required governance approval is recorded under `GOVERNANCE.md`; GitHub checks pass and the candidate has a clean merge state. |
| Post-merge validation | Open | After merge, the full suite, all three validators, repository cleanliness, and published metadata are revalidated. |

Structural validators do not replace renderer, qualified-review, or governance evidence.

Until every applicable gate is closed on one exact candidate SHA, 0.4-alpha must not be tagged or represented as released.
