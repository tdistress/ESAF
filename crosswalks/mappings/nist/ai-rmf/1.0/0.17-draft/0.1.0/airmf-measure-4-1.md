---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-4-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-4.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Measurement approaches for performance improvements and emergent risks are connected to AI system deployment and incident-response processes."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-4.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-120 requires AI incident procedures integrated with enterprise incident management, including identification, response, recovery, and learning.",
      "conditions": [
        "Measurement-derived risk signals can trigger or inform AI incident response."
      ],
      "expected_evidence": [
        "Incident procedures showing intake from monitoring/measurement signals."
      ],
      "known_gaps": [
        "OPS-120 does not define the measurement approaches themselves."
      ]
    },
    {
      "esaf_control_id": "OPS-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-110 requires classifying, assessing, testing, approving, deploying, verifying, and supporting rollback for AI capability changes according to impact and material-change triggers.",
      "conditions": [
        "Deployment/change processes receive measurement inputs affecting release decisions."
      ],
      "expected_evidence": [
        "Change records referencing measurement or monitoring results."
      ],
      "known_gaps": [
        "OPS-110 is change/release management, not measurement design."
      ]
    },
    {
      "esaf_control_id": "MON-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-140 requires triage, escalation, and containment for AI behavior and operational alerts.",
      "conditions": [
        "Measurement thresholds generate alerts routed into response processes."
      ],
      "expected_evidence": [
        "Alert response runbooks linking measurements to escalation/containment."
      ],
      "known_gaps": [
        "MON-140 covers alert response, not deployment authorization gates."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-4.1 mapping record."
    }
  ]
}
---
# MEASURE-4.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
