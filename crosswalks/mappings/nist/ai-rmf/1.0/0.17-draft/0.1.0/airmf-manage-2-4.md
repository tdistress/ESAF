---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-2-4",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-2.4",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Mechanisms exist to supersede, disengage, or deactivate AI systems with performance or outcomes inconsistent with intended use, with assigned and understood responsibilities."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-2.4"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AGT-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "AGT-150 requires providing, protecting, monitoring, and testing mechanisms to pause, restrict, isolate, terminate, roll back, recover, and safely resume agent operation according to defined triggers and authority.",
      "conditions": [
        "The system includes agents that can be paused/terminated when outcomes are inconsistent with intended use."
      ],
      "expected_evidence": [
        "Agent intervention mechanisms, triggers, authority, and test evidence."
      ],
      "known_gaps": [
        "AGT-150 is agent-scoped and does not deactivate all AI system types."
      ]
    },
    {
      "esaf_control_id": "OPS-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-150 requires an approved retirement process addressing users, dependencies, access, models, data, agents, interfaces, suppliers, contracts, records, communications, continuity, and decommissioning verification.",
      "conditions": [
        "Deactivation/retirement is used when performance remains inconsistent with intended use."
      ],
      "expected_evidence": [
        "Approved capability retirement/decommissioning records with named owners."
      ],
      "known_gaps": [
        "OPS-150 is full retirement, not temporary disengage/supersede mechanisms."
      ]
    },
    {
      "esaf_control_id": "ARC-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "ARC-130 requires designing safe state, fallback, reversibility, recovery, and tested resumption for foreseeable failures.",
      "conditions": [
        "Safe-state/fallback design supports disengage behavior when outcomes are inconsistent."
      ],
      "expected_evidence": [
        "Resilience design and test evidence for safe-state/fallback."
      ],
      "known_gaps": [
        "ARC-130 is design/resilience, not assigned operational deactivation responsibility alone."
      ]
    },
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-130 assigns accountable owners with authority for operation, material change, and retirement.",
      "conditions": [
        "Accountable owners hold deactivation/retirement decision authority."
      ],
      "expected_evidence": [
        "Ownership records documenting retirement/operation authority."
      ],
      "known_gaps": [
        "GOV-130 assigns accountability but does not implement technical deactivation mechanisms."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-2.4 mapping record."
    }
  ]
}
---
# MANAGE-2.4

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
