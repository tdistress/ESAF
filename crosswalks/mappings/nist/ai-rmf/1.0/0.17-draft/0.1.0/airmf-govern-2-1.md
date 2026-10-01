---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-2-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-2.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Roles, responsibilities, and communication lines for mapping, measuring, and managing AI risks are documented and clear."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-2.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "GOV-100 requires documented accountability, membership, decision rights, escalation paths, and meeting cadence for governing in-scope AI capabilities.",
      "conditions": [
        "Governance authority decision rights cover AI risk mapping, measurement, and management oversight."
      ],
      "expected_evidence": [
        "Governance charter with accountability and escalation paths."
      ],
      "known_gaps": [
        "GOV-100 does not enumerate NIST MAP/MEASURE/MANAGE role matrices."
      ]
    },
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "GOV-130 requires assignment of accountable business and technical/service owners with documented authority for purpose, outcomes, risk, resources, operation, material change, and retirement.",
      "conditions": [
        "Capability owners are accountable for risk outcomes within their scope."
      ],
      "expected_evidence": [
        "Capability ownership records documenting risk authority."
      ],
      "known_gaps": [
        "GOV-130 does not document enterprise communication lines for all AI risk actors."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-2.1 mapping record."
    }
  ]
}
---
# GOVERN-2.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
