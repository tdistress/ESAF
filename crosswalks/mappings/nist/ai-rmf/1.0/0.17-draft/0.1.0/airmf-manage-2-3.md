---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-2-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-2.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Procedures are followed to respond to and recover from a previously unknown risk when it is identified."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-2.3"
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
      "rationale": "OPS-120 requires preparing for, identifying, triaging, containing, investigating, eradicating, recovering from, communicating, reporting, and learning from AI incidents.",
      "conditions": [
        "Previously unknown risks that manifest as AI incidents are handled under OPS-120."
      ],
      "expected_evidence": [
        "AI incident records showing response and recovery for newly identified risk events."
      ],
      "known_gaps": [
        "OPS-120 covers incidents; not every newly identified risk is an incident."
      ]
    },
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-100 requires escalation and reassessment within the AI risk methodology when risk information changes.",
      "conditions": [
        "Newly identified risks are entered into methodology-driven reassessment and escalation."
      ],
      "expected_evidence": [
        "Risk register updates and escalation records for newly identified risks."
      ],
      "known_gaps": [
        "RSK-100 does not itself perform operational recovery."
      ]
    },
    {
      "esaf_control_id": "RSK-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-140 requires reassessment, revalidation, and reauthorization before material changes that could alter purpose, performance, or control effectiveness.",
      "conditions": [
        "Response to a newly identified risk requires material change to the capability."
      ],
      "expected_evidence": [
        "Material-change risk review triggered by newly identified risk."
      ],
      "known_gaps": [
        "RSK-140 is change-triggered reauthorization, not general unknown-risk recovery procedures."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-2.3 mapping record."
    }
  ]
}
---
# MANAGE-2.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
