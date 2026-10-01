---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-1-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-1.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Approaches and metrics for measuring AI risks enumerated during MAP—including residual risks after treatment—are identified."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-1.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-100 requires an AI risk methodology defining rating criteria, residual risk, monitoring, reassessment, and escalation.",
      "conditions": [
        "Residual-risk measurement approaches are defined in the approved methodology."
      ],
      "expected_evidence": [
        "Approved methodology describing residual-risk rating and monitoring measures."
      ],
      "known_gaps": [
        "RSK-100 does not require metrics specifically enumerated against each MAP-identified risk artifact."
      ]
    },
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-120 requires monitoring production AI behavior for performance, quality, drift, safety, fairness, reliability, policy, uncertainty, and emerging limitations against approved baselines and thresholds.",
      "conditions": [
        "Production monitoring metrics are used as risk-measurement approaches for deployed systems."
      ],
      "expected_evidence": [
        "Approved monitoring baselines/thresholds and measurement results."
      ],
      "known_gaps": [
        "MON-120 measures runtime behavior, not all residual risks identified in MAP."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-1.1 mapping record."
    }
  ]
}
---
# MEASURE-1.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
