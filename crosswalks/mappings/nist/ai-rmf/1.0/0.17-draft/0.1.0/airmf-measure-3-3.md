---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-3-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-3.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Feedback processes for end users and impacted communities to report problems and appeal system outcomes are established and integrated into AI evaluation and monitoring."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-3.3"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AGT-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "AGT-120 requires risk-proportionate human challenge and appeal for agent decisions and actions.",
      "conditions": [
        "The system uses agents whose outcomes are subject to challenge/appeal under AGT-120."
      ],
      "expected_evidence": [
        "Agent appeal/challenge procedures and records."
      ],
      "known_gaps": [
        "AGT-120 provides agent appeal, not general end-user/community feedback channels for all AI systems."
      ]
    },
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-120 requires identifying, communicating, reporting, and learning from AI incidents.",
      "conditions": [
        "User-reported problems that meet incident criteria are handled under OPS-120."
      ],
      "expected_evidence": [
        "AI incident intake and learning records from reported problems."
      ],
      "known_gaps": [
        "OPS-120 is incident management, not a dedicated community feedback and appeal process integrated into evaluation."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-3.3 mapping record."
    }
  ]
}
---
# MEASURE-3.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
