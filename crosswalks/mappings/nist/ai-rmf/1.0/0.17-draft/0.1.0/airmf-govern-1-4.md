---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-1-4",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-1.4",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The AI risk-management process and outcomes are established through transparent policies and controls based on organizational risk priorities."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-1.4"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-100 requires consistent application of an approved AI risk methodology covering treatment, acceptance, monitoring, reassessment, and escalation.",
      "conditions": [
        "The approved methodology is published as organizational policy or controlled procedure."
      ],
      "expected_evidence": [
        "Approved AI risk methodology and evidence of consistent application."
      ],
      "known_gaps": [
        "Transparency to external stakeholders is not expressly required by RSK-100."
      ]
    },
    {
      "esaf_control_id": "GOV-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "GOV-110 requires enterprise AI policy that defines risk expectations, accountability, enforcement, and review requirements.",
      "conditions": [
        "Enterprise AI policy includes risk expectations aligned to organizational priorities."
      ],
      "expected_evidence": [
        "Approved enterprise AI policy sections on risk expectations and review."
      ],
      "known_gaps": [
        "GOV-110 does not specify the detailed risk-management process outcomes."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-1.4 mapping record."
    }
  ]
}
---
# GOVERN-1.4

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
