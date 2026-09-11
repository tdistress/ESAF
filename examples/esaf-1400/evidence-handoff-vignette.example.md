# Evidence handoff vignette (informative)

Non-normative example supporting
[ESAF-1400](../../implementation/ESAF-1400.md) Section 9 evidence handoff.
Completing this material does not establish certification, compliance, or
control satisfaction.

This fictional vignette shows how an implementation team prepares ESAF-1500
evidence during a CAP-140 release without treating draft assessment results
as final determinations.

## Scenario

Fictional Summit Analytics completes a September 2026 release of the
workforce-research assistant. The implementation team captures evidence at
the point of release and routes it to the control owners identified in the
capability-to-control mapping.

## Capture-at-source checklist

| Capture step | Fictional artifact | ESAF-1500 fields recorded |
|---|---|---|
| Export approved configuration | Gateway allowlist export | source, custodian, collection method, scope, period |
| Retain immutable test output | Classification regression harness | source, period, integrity digest |
| Record assessor-facing limitation | Staging-only trace note | limitations array on evidence record |
| Link to control mapping | `MAP-140-03` row for `RSK-110`, `DAT-110` | traceability requirement and procedure refs |

## Handoff records

| Record type | Fictional ID | Routed to | Status |
|---|---|---|---|
| Evidence record | `EVD-ENG2-RSK110-CLASSIFY` | Enterprise risk analyst (RSK-110 owner) | Ready for assessor review |
| Evidence record | `EVD-SAMP2-DAT110-HANDLING` | Data owner (DAT-110 owner) | Ready for assessor review |
| Assessment result | `ASR-ENG2-RSK110` | Independent assessor | `draft` — open finding on trigger criteria |
| Assessment result | `ASR-SAMP2-DAT110` | Independent assessor | `draft` — staging trace limitation |

Filled JSON examples for the RSK-110 workbook engagement appear in
[`assessment/workbook/examples/engagement2-evidence-record.example.json`](../../assessment/workbook/examples/engagement2-evidence-record.example.json)
and siblings. The second audit-checklist sampling vignette at
[`assessment/audit-checklist/sampling2-vignette.example.md`](../../assessment/audit-checklist/sampling2-vignette.example.md)
shows how an assessor records determinations from similar evidence.

## Known gaps (explicit)

- RSK-110 audience-expansion trigger criteria remain incomplete; result stays
  `draft`.
- DAT-110 trace used staging, not production; assessor must accept limitation
  or re-run before any final determination.
- Implementation notes remain separate from finished evidence records.

## Nonclaims

Names, identifiers, dates, and routing decisions in this vignette are
fictional. This example does not determine control satisfaction, design or
operating effectiveness, or maturity level — those remain assessor
determinations under ESAF-1500.
