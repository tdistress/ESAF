# API-100 inconclusive follow-up example: Summit Analytics CAP-140

**Status:** Informative fictional Draft example

This example adds one bounded follow-up to the fictional Summit Analytics
`CAP-140` case. Historical context includes the original
[`ASR-ENG3-API100`](../workbook/examples/engagement3-assessment-result.example.json)
and its open finding `FND-ENG3-API100-EMERGENCY`, plus the v0.19 follow-up
`ASR-ENG4-API100-A3`. Those historical records remain unchanged.

## Attempted follow-up

| Field | Example entry |
|---|---|
| Finding owner | Jordan Hale, AI platform engineer, fictional Summit Analytics |
| Attempt | Review one API-100-A3 emergency-restriction exercise on the fictional staging gateway. |
| Evidence | [`EVD-ENG5-API100-RESTRICTION`](../examples/api100-inconclusive-follow-up-evidence-record.example.json) |
| Result | [`ASR-ENG5-API100-A3-INCONCLUSIVE`](../examples/api100-inconclusive-follow-up-assessment-result.example.json) |
| Finding | `FND-ENG5-API100-A3-INCONCLUSIVE`, a distinct open finding nested in this result. |

The staging event trail is incomplete, so the attempted test is inconclusive.
The available record does not show whether the restriction succeeded or failed.
The assessment therefore sets determination, design effectiveness, and
operating effectiveness to `not_assessed`, and keeps the new finding open.
This result neither declares control failure nor claims successful operation.

## Scope and limitations

The follow-up covers one attempted staging exercise only. Production restriction
and recovery, bypass paths, repeated operation, API-100-A1, and API-100-A2 were
not assessed. A future follow-up would need complete, reviewable event records
before reaching a conclusion about the attempted test.

All people, organizations, actions, evidence, dates, and judgments are
fictional. This example makes no compliance, certification, equivalence,
endorsement, or assurance claim. It remains Draft and does not revise any
historical assessment result.
