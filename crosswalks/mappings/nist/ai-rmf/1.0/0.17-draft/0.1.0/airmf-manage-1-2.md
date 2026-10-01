---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-1-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-1.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Treatment of documented AI risks is prioritized based on impact, likelihood, and available resources or methods."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-1.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-120 requires documenting, approving, implementing, and monitoring treatments for identified AI risks.",
      "conditions": [
        "Documented AI risks have approved treatments."
      ],
      "expected_evidence": [
        "Risk-treatment plans with approval and implementation status."
      ],
      "known_gaps": [
        "RSK-120 does not expressly require prioritization formulas using resources/methods availability."
      ]
    },
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-100 requires rating criteria, treatment, acceptance, and escalation within an approved methodology.",
      "conditions": [
        "Prioritization uses methodology rating criteria for impact and likelihood."
      ],
      "expected_evidence": [
        "Methodology rating criteria and prioritized treatment queue."
      ],
      "known_gaps": [
        "RSK-100 may not explicitly incorporate resource availability into prioritization."
      ]
    },
    {
      "esaf_control_id": "STR-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "STR-130 requires identifying and approving resources required to maintain controls throughout the lifecycle.",
      "conditions": [
        "Available resources constrain feasible treatments."
      ],
      "expected_evidence": [
        "Approved resource plans covering risk-treatment capacity."
      ],
      "known_gaps": [
        "STR-130 plans resources; it does not prioritize individual risk treatments."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-1.2 mapping record."
    }
  ]
}
---
# MANAGE-1.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
