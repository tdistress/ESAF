# ESAF-1400 adoption vignette example (informative)

This sample is non-normative enablement for the
[ESAF-1400](../../implementation/ESAF-1400.md) adoption sequence. Following
it does not establish certification, compliance, or control satisfaction.

All organizations, capabilities, identifiers, decisions, and records below
are fictional.

## Fictional context

Northstar Services proposes `CAP-140`, a workforce research assistant that
summarizes employee-selected public and internal documents. It cannot take
actions, write to systems of record, or search repositories a user cannot
already access. The walkthrough shows how one team could apply ESAF-1400
Section 5 without treating the sequence as an approval checklist.

## Steps 1–9

| Step | Fictional walkthrough | Resulting implementation record |
|---|---|---|
| **1. Confirm management-system scope** | The governance team records `CAP-140` as an in-scope workforce capability because it processes internal information and produces work output. The approved purpose covers research and drafting, and excludes employment decisions and autonomous action. | Inventory entry `INV-CAP-140`, purpose statement, and scope rationale |
| **2. Confirm accountability** | The Director of Knowledge Services accepts business ownership, and the Workplace AI service owner accepts technical ownership. Security, privacy, data, records, accessibility, and operations roles are named as contributors. | Ownership acceptance `OWN-140-01` and responsibility assignments |
| **3. Classify risk early** | Reviewers classify the capability as fictional Tier 2 after considering internal data, workforce use, non-consequential outputs, human review, and the absence of write actions. They identify reclassification triggers for new data types, audiences, memory, or actions. | Classification `RISK-140-02` with rationale and change triggers |
| **4. Select and tailor an architecture pattern** | The architecture team selects `ARC-P110` with `ARC-P100` for governed model access and `ARC-P160` for evidence and monitoring. Retrieval remains disabled until a separate `ARC-P120` review. The design removes durable memory and connector write access. | Architecture decision `ADR-140-01`, data-flow view, and tailoring record |
| **5. Select applicable controls** | The team maps the classification and pattern control points to `GOV-130`, `RSK-110`, `ARC-120`, `IAM-120`, `DAT-110`, `APP-110`, and `MON-100`, while recording ownership and evidence sources for each. | Capability-control mapping `MAP-140-03` |
| **6. Implement and configure** | Engineers configure managed identity, least-privilege access, approved model routing, input protections, output notices, restricted retention, and telemetry. Product names and versions remain in a local configuration baseline rather than the ESAF-facing mapping. | Versioned baseline `CFG-140-07`, build record, and AI Bill of Materials entry |
| **7. Validate before production** | Independent reviewers test access boundaries, prompt-injection handling, output notices, logging, safe failure, and the prohibited-use restrictions. One missing log field is corrected and retested before the production request proceeds. | Validation plan `VAL-140-01`, corrected log-field defect, retest result, and production decision reference |
| **8. Assess and evidence** | The deployment pipeline captures the approved configuration, test result, commit identifier, collector identity, and timestamp. The control owner adds review evidence and hands the staged records to an assessor using ESAF-1500 semantics. | Evidence records `EVD-140-001` through `EVD-140-009` and draft Assessment Result `ASR-140-01` |
| **9. Operate and improve** | Operations monitors access failures, unsafe-input detections, user feedback, quality measures, incidents, and material changes. A rise in unsupported citations leads to a revised evaluation set and configuration update through Steps 4–8. | Monitoring review `MONREV-140-02`, improvement item `IMP-140-05`, and linked change record |

## Reader checks

- The approved purpose, exclusions, owners, classification, pattern, controls,
  evidence, and operating feedback remain traceable to `CAP-140`.
- Classification precedes pattern selection, and validation precedes the
  fictional production decision.
- Product detail stays in the implementation-local configuration baseline.
- The assessment remains a separate determination performed under ESAF-1500.
- Operating feedback starts another iteration instead of ending the sequence.

This vignette is informative working material, not conformance evidence or a
production authorization.
