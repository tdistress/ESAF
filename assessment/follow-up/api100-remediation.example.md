# API-100 follow-up example: Summit Analytics CAP-140

**Status:** Informative fictional Draft example

This example extends the fictional Summit Analytics `CAP-140` case in the
[integrated assessment](../integrated-assessment.example.md). It records one
owner action and one focused follow-up of the emergency-restriction condition
documented in the original
[`ASR-ENG3-API100`](../workbook/examples/engagement3-assessment-result.example.json)
as [`FND-ENG3-API100-EMERGENCY`](../workbook/examples/engagement3-assessment-result.example.json).
The original result remains unchanged and continues to describe its original
assessment period.

## Fictional owner action

| Field | Example entry |
|---|---|
| Finding owner | Jordan Hale, AI platform engineer, fictional Summit Analytics |
| Action | Add a staging harness that exercises the API-100-A3 emergency restriction, retains the event record, and checks that the restricted alias remains blocked. |
| Completed | 2026-10-12, before the follow-up assessment |
| Verification | Morgan Ellis performed one controlled API-100-A3 Test against the fictional staging mirror. |
| Scope boundary | One staging alias and one exercise; production, recovery timing, bypass paths, API-100-A1, and API-100-A2 remain outside this follow-up. |

The new exercise record is
[`EVD-ENG4-API100-RESTRICTION`](../examples/api100-follow-up-evidence-record.example.json).
The follow-up result is
[`ASR-ENG4-API100-A3`](../examples/api100-follow-up-assessment-result.example.json).
Its resolved finding,
`FND-ENG4-API100-A3-VERIFICATION`, is a distinct identifier because each
finding is nested in one assessment result. The narrative and result link it
to the earlier `FND-ENG3-API100-EMERGENCY`; they do not replace or rewrite that
historical finding.

## Outcome and limitations

The fictional exercise blocked the selected staging alias and recorded the
restriction event. The follow-up disposition resolves only the specific
exercise gap associated with the original finding within this limited staging
sample. The follow-up determination remains `partially_satisfied`, and
operating effectiveness remains `not_assessed`: one staging exercise does not
reassess the whole API-100 control or establish sustained or production
operation.

All people, organizations, actions, evidence, dates, and judgments are
fictional. This example makes no compliance, certification, equivalence,
endorsement, or assurance claim. Completing it does not advance any control or
assessment record beyond Draft.
