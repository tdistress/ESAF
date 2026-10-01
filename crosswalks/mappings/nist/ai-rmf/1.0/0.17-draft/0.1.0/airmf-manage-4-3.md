---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-4-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-4.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incidents and errors are communicated to relevant AI actors, including affected communities and users, and processes for tracking, responding, and recovering are followed and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-4.3"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "OPS-120 requires preparing for, identifying, triaging, containing, investigating, eradicating, recovering from, communicating, reporting, and learning from AI incidents using criteria and procedures integrated with enterprise incident management.",
      "conditions": [
        "AI incidents and material errors are handled under OPS-120."
      ],
      "expected_evidence": [
        "AI incident records showing communication, response, recovery, and learning."
      ],
      "known_gaps": [
        "OPS-120 requires communication and reporting but does not expressly require notifying affected communities in all cases."
      ]
    },
    {
      "esaf_control_id": "CMP-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "CMP-110 requires creating and disclosing AI records, notices, and reports according to applicable audience and timing requirements.",
      "conditions": [
        "Applicable obligations require incident or error notices to defined audiences."
      ],
      "expected_evidence": [
        "Obligation-driven incident/error notices and submission evidence."
      ],
      "known_gaps": [
        "CMP-110 is obligation-driven disclosure, not a universal affected-community communication process."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-4.3 mapping record."
    }
  ]
}
---
# MANAGE-4.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
