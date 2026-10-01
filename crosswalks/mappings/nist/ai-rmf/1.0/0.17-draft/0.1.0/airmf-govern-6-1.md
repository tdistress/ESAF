---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-6-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-6.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Policies and procedures address AI risks associated with third-party entities, including third-party AI systems or data."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-6.1"
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
      "rationale": "CMP-120 requires establishing, contractually assigning, verifying, monitoring, and enforcing third-party AI obligations for security, privacy, data use, intellectual property, transparency, change, incidents, assurance, continuity, subcontractors, and exit.",
      "conditions": [
        "Third-party AI systems or data providers are in scope for CMP-120."
      ],
      "expected_evidence": [
        "Third-party AI obligation schedules, contracts, and monitoring evidence."
      ],
      "known_gaps": [
        "CMP-120 focuses on obligation assignment and enforcement, not a full third-party AI risk taxonomy."
      ]
    },
    {
      "esaf_control_id": "API-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "API-140 requires defining and enforcing security, privacy, data use, retention, training, residency, availability, change, incident, assurance, continuity, and exit requirements for external AI service integrations.",
      "conditions": [
        "Third-party AI is consumed via external AI service integration."
      ],
      "expected_evidence": [
        "External AI service integration requirements and enforcement evidence."
      ],
      "known_gaps": [
        "API-140 addresses integrated external AI services, not every third-party data source."
      ]
    },
    {
      "esaf_control_id": "ARC-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "ARC-140 requires documenting, approving, validating, and monitoring responsibility boundaries and inherited controls among capability owners, shared platforms, model providers, cloud services, data owners, tool providers, and other suppliers.",
      "conditions": [
        "Shared-responsibility boundaries with third parties are relevant to the AI system."
      ],
      "expected_evidence": [
        "Approved shared-responsibility documentation for suppliers and providers."
      ],
      "known_gaps": [
        "ARC-140 does not alone create third-party risk policies."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-6.1 mapping record."
    }
  ]
}
---
# GOVERN-6.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
