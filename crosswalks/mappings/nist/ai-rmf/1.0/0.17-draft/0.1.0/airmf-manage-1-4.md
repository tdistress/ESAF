---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-1-4",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-1.4",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Negative residual risks after AI risk treatment are documented, monitored, and managed."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-1.4"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-120 requires documenting and monitoring treatments and obtaining acceptance of residual risk from a commensurate authority before production authorization or continued operation.",
      "conditions": [
        "Residual risks are accepted and monitored after treatment."
      ],
      "expected_evidence": [
        "Residual-risk acceptance records and monitoring of accepted residuals."
      ],
      "known_gaps": [
        "RSK-120 accepts residual risk; continuous management may also rely on RSK-100 monitoring."
      ]
    },
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-100 requires residual risk, monitoring, reassessment, and escalation within the approved methodology.",
      "conditions": [
        "Residual risks remain under methodology monitoring and reassessment."
      ],
      "expected_evidence": [
        "Risk methodology and register entries for residual risks with monitoring status."
      ],
      "known_gaps": [
        "RSK-100 defines methodology; operational residual-risk handling is evidenced via treatments and monitoring records."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-1.4 mapping record."
    }
  ]
}
---
# MANAGE-1.4

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
