---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-6-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-6.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Contingency processes handle failures or incidents related to third-party data or AI systems deemed high-risk."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-6.2"
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
      "rationale": "OPS-120 requires preparing for, identifying, triaging, containing, investigating, recovering from, communicating, reporting, and learning from AI incidents using procedures integrated with enterprise incident management.",
      "conditions": [
        "Incidents involving third-party data or AI systems are handled under OPS-120."
      ],
      "expected_evidence": [
        "AI incident procedures and records covering third-party supplier or data failures."
      ],
      "known_gaps": [
        "OPS-120 does not uniquely define high-risk third-party contingency playbooks."
      ]
    },
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-130 requires risk-proportionate continuity, fallback, safe-state, recovery, dependency, data-restoration, and provider-failure arrangements for AI capabilities.",
      "conditions": [
        "High-risk third-party AI or data dependencies have continuity/provider-failure arrangements."
      ],
      "expected_evidence": [
        "Continuity and provider-failure plans for high-risk third-party dependencies."
      ],
      "known_gaps": [
        "OPS-130 is continuity/recovery, not the full incident-management response."
      ]
    },
    {
      "esaf_control_id": "API-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "API-140 requires enforcing incident, assurance, continuity, and exit requirements for external AI service integrations.",
      "conditions": [
        "The high-risk third party is an external AI service integration."
      ],
      "expected_evidence": [
        "External AI service continuity/incident/exit requirements and test evidence."
      ],
      "known_gaps": [
        "API-140 does not cover non-integrated third-party data sources."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-6.2 mapping record."
    }
  ]
}
---
# GOVERN-6.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
