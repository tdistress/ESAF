---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-1-7",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-1.7",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Processes decommission and phase out AI systems safely in a manner that reduces risks."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-1.7"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "OPS-150 requires retiring an AI capability through an approved process addressing users, dependencies, access, models, data, agents, interfaces, suppliers, contracts, records, communications, continuity, and verification of decommissioning.",
      "conditions": [
        "The AI system being phased out is an in-scope AI capability under OPS-150."
      ],
      "expected_evidence": [
        "Approved capability-retirement record with decommissioning verification."
      ],
      "known_gaps": [
        "OPS-150 is capability retirement; it does not use NIST 'phase out' phrasing for every AI system form."
      ]
    },
    {
      "esaf_control_id": "MOD-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-150 requires authorized model retirement that removes deployment and access, preserves required evidence, disposes of artifacts and data, updates dependencies, and verifies prohibited use cannot continue.",
      "conditions": [
        "Material models supporting the decommissioned system are retired or detached under MOD-150."
      ],
      "expected_evidence": [
        "Model-retirement records showing access removal and dependency updates."
      ],
      "known_gaps": [
        "MOD-150 alone does not retire the broader AI system or service."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-1.7 mapping record."
    }
  ]
}
---
# GOVERN-1.7

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
