# ESAF-1400 capability-control mapping example (informative)

This sample is non-normative enablement for
[ESAF-1400](../../implementation/ESAF-1400.md) mapping practice. Using it
does not establish certification, compliance, or control satisfaction.

All organizations, capabilities, classifications, ownership assignments, and
records below are fictional. The rows are illustrative subsets, not complete
control determinations.

## Fictional capability mapping

| Capability | Risk classification | Architecture pattern and tailoring | Illustrative control points | Control owner | Evidence source |
|---|---|---|---|---|---|
| `CAP-140` workforce research assistant | Tier 2; reclassify for new audiences, data, memory, or actions | `ARC-P110` with `ARC-P100` and `ARC-P160`; retrieval and durable memory disabled | `GOV-130`, `RSK-110`, `ARC-120`, `IAM-120`, `DAT-110`, `APP-110`, `MON-100` | Workplace AI service owner; identity, data, application-security, and monitoring operators retain their assigned controls | `INV-CAP-140`, `RISK-140-02`, `ADR-140-01`, access-policy export, validation results, and monitoring baseline |
| `CAP-241` customer-support knowledge assistant | Tier 3; reclassify for automated decisions or write actions | `ARC-P120` with `ARC-P100` and `ARC-P160`; retrieval limited to approved support articles and authorization-aware sources | `RSK-110`, `ARC-110`, `IAM-120`, `DAT-130`, `DAT-150`, `APP-110`, `APP-120`, `MON-100` | Customer Support product owner; enterprise search owner operates retrieval controls | `INV-CAP-241`, `RISK-241-04`, `ADR-241-06`, source-authorization tests, citation evaluation, and retrieval audit trail |
| `CAP-318` invoice-field extraction service | Tier 2; reclassify if outputs initiate payment or affect supplier eligibility | `ARC-P150` with `ARC-P100` and `ARC-P160`; output remains a draft for human verification | `DAT-100`, `DAT-110`, `DAT-130`, `APP-120`, `API-110`, `MOD-120`, `OPS-110`, `MON-100` | Finance automation service owner; data and model owners operate their respective controls | `INV-CAP-318`, `RISK-318-03`, `ADR-318-02`, interface contract, model-validation report, release record, and telemetry sample |

## How a reviewer could use the mapping

1. Start with the inventory identifier and confirm that purpose, owner, and
   classification are current.
2. Follow the architecture decision to the selected pattern, supporting
   patterns, tailoring choices, and recorded deviations.
3. Compare the mapped control points with the classification and pattern
   rather than assuming that this illustrative subset is sufficient.
4. Confirm that each control has an accountable operator and that the evidence
   source resolves to the deployed version and assessment period.
5. Route evidence to an ESAF-1500 assessment without treating the mapping
   itself as a control record or result.

## Stale-mapping scenario

Suppose `CAP-241` enables a write connector but `MAP-241-02` still describes a
read-only retrieval assistant. The mismatch may first appear as a deployment
version newer than the architecture decision, an unlisted API permission, or
action telemetry with no mapped owner. The capability owner should pause use
of the unreviewed function, update classification and architecture analysis,
identify additional control points such as tool authorization and agent
monitoring where applicable, reconnect owners and evidence sources, and record
the mapping review triggered by the material change.

A mapping review should compare inventory, classification, architecture
decision, deployed configuration, release history, control assignments, and
evidence locations. A recurring review may supplement this event-driven check,
but it should not replace review after a material change.

This worksheet is informative working material, not conformance evidence or
an assessment result.
