---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-1-6",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-1.6",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Mechanisms inventory AI systems and are resourced according to organizational risk priorities."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-1.6"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "GOV-120 requires review of the enterprise AI portfolio at an organization-defined frequency using current information on ownership, lifecycle state, value, risk, incidents, exceptions, obligations, dependencies, concentration, cost, and retirement.",
      "conditions": [
        "Portfolio review is treated as the inventory and prioritization mechanism for AI systems/capabilities."
      ],
      "expected_evidence": [
        "Current AI portfolio inventory with ownership, lifecycle state, and risk fields."
      ],
      "known_gaps": [
        "GOV-120 reviews the portfolio; it does not expressly require a continuously maintained system inventory independent of review cadence."
      ]
    },
    {
      "esaf_control_id": "MOD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MOD-100 requires registration of every material model with identifier, owner, purpose, lifecycle state, risk classification, and deployment relationships before approved use.",
      "conditions": [
        "Material models used by inventoried AI systems are registered."
      ],
      "expected_evidence": [
        "Model registry entries linked to deploying capabilities."
      ],
      "known_gaps": [
        "MOD-100 inventories models, not complete AI systems or non-model AI capabilities."
      ]
    },
    {
      "esaf_control_id": "STR-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "STR-130 requires identification, approval, and periodic review of people, competencies, funding, platforms, assurance, and supplier resources required to achieve AI objectives and maintain controls.",
      "conditions": [
        "Resource planning is aligned to portfolio risk priorities."
      ],
      "expected_evidence": [
        "Approved AI resource plan tied to high-priority capabilities."
      ],
      "known_gaps": [
        "STR-130 does not itself create the AI system inventory."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-1.6 mapping record."
    }
  ]
}
---
# GOVERN-1.6

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
