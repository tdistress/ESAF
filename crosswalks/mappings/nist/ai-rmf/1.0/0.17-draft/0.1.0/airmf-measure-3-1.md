---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-3-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-3.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Approaches, personnel, and documentation regularly identify and track existing, unanticipated, and emergent AI risks based on application, deployment environment, and context."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-3.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-120 requires monitoring for emerging limitations against approved baselines and thresholds in production.",
      "conditions": [
        "Production monitoring is used to identify emergent behavioral risks."
      ],
      "expected_evidence": [
        "Monitoring baselines and records of emerging-limitation detections."
      ],
      "known_gaps": [
        "MON-120 does not alone assign personnel or full risk-tracking documentation for all unanticipated risks."
      ]
    },
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-100 requires monitoring, reassessment, and escalation within the approved AI risk methodology.",
      "conditions": [
        "Risk methodology defines how newly identified risks are tracked and escalated."
      ],
      "expected_evidence": [
        "Methodology clauses and risk-register entries for newly identified risks."
      ],
      "known_gaps": [
        "RSK-100 is methodological; operational detection depends on monitoring controls."
      ]
    },
    {
      "esaf_control_id": "MON-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-140 requires assigned ownership, triage, investigation, escalation, and documentation for AI security, behavior, operational, and compliance alerts.",
      "conditions": [
        "Alert response personnel track and escalate emergent risk indications."
      ],
      "expected_evidence": [
        "Alert ownership and escalation records."
      ],
      "known_gaps": [
        "MON-140 handles alerts; it does not identify all emergent risks outside alerting."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-project-owner",
    "date": "2026-10-01"
  },
  "change_history": [
    {
      "version": "0.1.0",
      "date": "2026-10-01",
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-3.1 mapping record."
    }
  ]
}
---
# MEASURE-3.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
