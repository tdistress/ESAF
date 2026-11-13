# Fictional API-100 evidence-complete follow-up

This fictional example continues the Summit Analytics CAP-140 sequence after
the [inconclusive follow-up](api100-inconclusive-follow-up.example.md). It
records one later staging exercise with a complete event trail and a separate
Draft reassessment. The earlier results remain unchanged.

| Record | Identifier | Purpose |
|---|---|---|
| Prior inconclusive result | [`ASR-ENG5-API100-A3-INCONCLUSIVE`](../examples/api100-inconclusive-follow-up-assessment-result.example.json) | Records the incomplete event trail and its distinct open finding |
| New evidence | [`EVD-ENG6-API100-RESTRICTION`](../examples/api100-evidence-complete-follow-up-evidence-record.example.json) | Captures one later API-100-A3 staging exercise with ordered event entries |
| New result | [`ASR-ENG6-API100-A3-FOLLOWUP`](../examples/api100-evidence-complete-follow-up-assessment-result.example.json) | Records the bounded reassessment and its distinct finding |

The complete fictional event trail is retained by the owner and reviewed by
the assessor:

| Time (UTC) | Event | Recorded outcome |
|---|---|---|
| 2026-10-30 14:30:00 | Test operator `op-test-01` sends baseline request `req-6301` to staging alias `summit-test-7` | Test route responds before restriction |
| 2026-10-30 14:34:00 | Operator issues restriction command `cmd-6302` for `summit-test-7` | Staging gateway accepts the command |
| 2026-10-30 14:34:01 | Gateway records `restriction_applied` event `evt-6303` for command `cmd-6302` | Event includes the alias, actor, and timestamp |
| 2026-10-30 14:34:06 | Operator sends request `req-6304` to `summit-test-7` | Gateway blocks the request under the active restriction |
| 2026-10-30 14:34:07 | Gateway records `request_blocked` event `evt-6305` for `req-6304` | Event includes the alias, restriction state, and timestamp |
| 2026-10-30 14:35:00 | Owner exports the ordered staging events for assessor review | Export is linked to evidence `EVD-ENG6-API100-RESTRICTION` |

The assessor records `partially_satisfied` and `partially_effective` for this
one API-100-A3 staging exercise. Operating effectiveness remains
`not_assessed`. The new result's finding is distinct because findings are
nested within assessment results; it resolves only the evidence-capture gap
within this follow-up and references the open finding
`FND-ENG5-API100-A3-INCONCLUSIVE`. It does not change that historical result
or rewrite its open status as recorded at that earlier assessment date; the
separate later result records the bounded resolution disposition.

This example does not establish production or recovery behavior, repeated or
sustained operation, capability-wide effectiveness, or results for API-100-A1
or API-100-A2. It makes no compliance, certification, equivalence,
endorsement, or assurance claim. All people, events, evidence, and judgments
are fictional, and the result remains Draft.
