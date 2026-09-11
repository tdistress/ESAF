# Assessment record links example (informative)

Non-normative example supporting
[ESAF-1700](../../data-model/ESAF-1700.md) exchange guidance and ESAF-1500
record reuse. Completing this material does not establish certification,
compliance, or control satisfaction.

This fictional example extends the
[entity instances example](entity-instances.example.md) scenario with
ESAF-1500 evidence and assessment-result links for capability `CAP-140`.

## Linked record set

| Record | Identifier | Subject entity | Role |
|---|---|---|---|
| Evidence record | `EVD-ENG2-RSK110-CLASSIFY` | `CAP-140` | Supports RSK-110 classification examination |
| Assessment result | `ASR-ENG2-RSK110` | `CAP-140` | Draft determination for RSK-110 |
| Finding (nested) | `FND-ENG2-RSK110-TRIGGER` | `CAP-140` | Open minor finding on trigger criteria |
| Evidence record | `EVD-SAMP2-DAT110-HANDLING` | `CAP-140` data path | Supports DAT-110 handling examination |
| Assessment result | `ASR-SAMP2-DAT110` | `CAP-140` data path | Draft determination for DAT-110 |

## Cross-reference rules (illustrative)

- Evidence `traceability.result_refs` points to assessment results that rely
  on the evidence; assessment `evidence_refs` points back without renaming
  ESAF-1500 fields.
- `assessment_scope.subject` names `CAP-140` by stable identifier rather than
  embedding capability attributes.
- Findings remain nested within assessment results; they are not exchanged as
  standalone top-level records.

## Exchange note

When sharing this fictional record set with an external reviewer, the exchange
should state scope, period, and purpose so the recipient does not infer broader
applicability than authorized — consistent with ESAF-1700 exchange guidance and
ESAF-1500 evidence `scope` and `period` contracts.

Filled JSON for the RSK-110 workbook trio appears under
[`assessment/workbook/examples/`](../../assessment/workbook/examples/). Catalog
examples for `procedure`, `log`, and `metric` evidence types appear under
[`assessment/evidence-catalog/examples/`](../../assessment/evidence-catalog/examples/).

## Nonclaims

Names, identifiers, and linkages in this example are fictional. Populating
these records does not constitute an ESAF-1000 conformance claim or an
ESAF-1500 final assessment result.
