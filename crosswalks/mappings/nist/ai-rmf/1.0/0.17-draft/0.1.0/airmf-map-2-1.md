---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-2-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-2.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Specific tasks and methods used to implement AI capabilities that each system component will provide are defined."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-2.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "ARC-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "ARC-110 requires documenting and maintaining AI components, actors, identities, data and control flows, trust levels, entry and exit points, external dependencies, administrative paths, and enforcement boundaries.",
      "conditions": [
        "Component roles within the AI system are documented under ARC-110 architecture views."
      ],
      "expected_evidence": [
        "Current AI component and data/control-flow documentation."
      ],
      "known_gaps": [
        "ARC-110 documents components and flows but does not expressly require defining tasks and methods each component uses to implement AI capabilities."
      ]
    },
    {
      "esaf_control_id": "APP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "APP-100 requires documented data and control flows, trust boundaries, and validation criteria for AI application design.",
      "conditions": [
        "Application design documents component responsibilities relevant to AI capability delivery."
      ],
      "expected_evidence": [
        "AI application design records describing component responsibilities."
      ],
      "known_gaps": [
        "APP-100 does not require a complete task/method specification per AI component."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-2.1 mapping record."
    }
  ]
}
---
# MAP-2.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
