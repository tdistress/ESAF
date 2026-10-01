---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-3-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-3.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Policies and procedures define and differentiate roles and responsibilities for human-AI configurations and oversight of AI systems."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-3.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AGT-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "AGT-120 requires risk-proportionate human approval, supervision, intervention, challenge, and appeal for agent decisions and actions, including conditions that prohibit autonomous execution.",
      "conditions": [
        "The AI system uses agents or autonomous action paths subject to AGT-120."
      ],
      "expected_evidence": [
        "Documented human-oversight procedures and autonomy prohibition conditions for agents."
      ],
      "known_gaps": [
        "AGT-120 applies to agents; it does not cover every non-agent human-AI configuration."
      ]
    },
    {
      "esaf_control_id": "APP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "APP-100 requires AI application design using documented trust boundaries, failure modes, human-oversight points, and risk-proportionate validation criteria.",
      "conditions": [
        "The AI system is delivered as an AI application with documented human-oversight points."
      ],
      "expected_evidence": [
        "Design records showing human-oversight points and trust boundaries."
      ],
      "known_gaps": [
        "APP-100 requires design documentation of oversight points but not a complete role/responsibility policy for all human-AI configurations."
      ]
    },
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-130 assigns accountable business and technical owners with authority for operation and risk of each AI capability.",
      "conditions": [
        "Capability owners are accountable for oversight configuration decisions."
      ],
      "expected_evidence": [
        "Ownership records assigning operational and risk authority."
      ],
      "known_gaps": [
        "GOV-130 does not differentiate human versus AI role configurations in detail."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-3.2 mapping record."
    }
  ]
}
---
# GOVERN-3.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
