---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-1-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-1.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Legal and regulatory requirements involving AI are understood, managed, and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-1.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "CMP-100 requires the organization to identify, interpret, record, assign, implement, monitor, and update legal, regulatory, contractual, policy, ethical, and sector obligations applicable to each AI capability and the enterprise AI management system.",
      "conditions": [
        "The AI RMF subcategory is evaluated for legal and regulatory obligation management covered by CMP-100."
      ],
      "expected_evidence": [
        "Obligation register covering legal and regulatory AI requirements with owners and monitoring status."
      ],
      "known_gaps": [
        "CMP-100 does not by itself require every AI-related legal topic to be framed as an AI RMF GOVERN process artifact."
      ]
    },
    {
      "esaf_control_id": "CMP-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "CMP-110 requires creation, protection, retention, disclosure, and submission of AI records, notices, registrations, reports, and evidence according to applicable requirements, supporting documentation of managed legal obligations.",
      "conditions": [
        "Applicable obligations require retained records, notices, or filings."
      ],
      "expected_evidence": [
        "Retained AI compliance records and submission evidence tied to identified obligations."
      ],
      "known_gaps": [
        "CMP-110 does not itself identify or interpret the legal requirements."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-1.1 mapping record."
    }
  ]
}
---
# GOVERN-1.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
