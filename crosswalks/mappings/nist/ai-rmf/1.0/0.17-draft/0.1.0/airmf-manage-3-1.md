---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-3-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-3.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "AI risks and benefits from third-party resources are regularly monitored, and risk controls are applied and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-3.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "CMP-120 requires verifying, monitoring, and enforcing third-party AI obligations for security, privacy, data use, intellectual property, transparency, change, incidents, assurance, continuity, subcontractors, and exit.",
      "conditions": [
        "Third-party resources providing AI systems or data are under CMP-120."
      ],
      "expected_evidence": [
        "Third-party monitoring and enforcement evidence for AI suppliers."
      ],
      "known_gaps": [
        "CMP-120 monitors obligations/controls; it does not expressly monitor third-party benefits."
      ]
    },
    {
      "esaf_control_id": "API-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "API-140 requires enforcing change, incident, assurance, continuity, and related requirements for external AI service integrations.",
      "conditions": [
        "Third-party AI is consumed via external service integration."
      ],
      "expected_evidence": [
        "External AI service monitoring and assurance evidence."
      ],
      "known_gaps": [
        "API-140 covers integrated external AI services, not all third-party resources."
      ]
    },
    {
      "esaf_control_id": "ARC-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "ARC-140 requires monitoring responsibility boundaries and inherited controls among suppliers and providers.",
      "conditions": [
        "Inherited third-party controls are monitored."
      ],
      "expected_evidence": [
        "Shared-responsibility monitoring records."
      ],
      "known_gaps": [
        "ARC-140 does not monitor third-party benefits."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-3.1 mapping record."
    }
  ]
}
---
# MANAGE-3.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
