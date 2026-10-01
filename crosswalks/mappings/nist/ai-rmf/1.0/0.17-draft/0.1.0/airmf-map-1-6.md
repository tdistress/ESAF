---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-1-6",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-1.6",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "System requirements are elicited from relevant AI actors, and design decisions account for socio-technical implications to address AI risks."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-1.6"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "APP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "APP-100 requires designing each AI application using documented trust boundaries, data and control flows, threat and misuse cases, security requirements, failure modes, human-oversight points, and risk-proportionate validation criteria.",
      "conditions": [
        "The AI system is delivered as an AI application subject to APP-100 design requirements."
      ],
      "expected_evidence": [
        "Design documentation covering trust boundaries, misuse cases, oversight points, and validation criteria."
      ],
      "known_gaps": [
        "APP-100 does not expressly require eliciting requirements from all relevant AI actors or documenting socio-technical implications as a named analysis."
      ]
    },
    {
      "esaf_control_id": "RSK-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-130 requires assessing impacts on individuals, affected groups, and society for E2–E4 capabilities before authorization.",
      "conditions": [
        "The capability is E2–E4 and socio-technical implications are captured in impact assessment."
      ],
      "expected_evidence": [
        "Impact assessment documenting affected parties and societal implications."
      ],
      "known_gaps": [
        "RSK-130 is authorization-time impact assessment, not full requirements elicitation."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-1.6 mapping record."
    }
  ]
}
---
# MAP-1.6

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
