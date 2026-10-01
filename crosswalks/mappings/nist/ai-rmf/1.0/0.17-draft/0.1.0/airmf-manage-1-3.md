---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-1-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-1.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Responses to high-priority AI risks are developed, planned, and documented, including strategies to maximize benefits and minimize negative impacts."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-1.3"
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
      "rationale": "RSK-120 requires documenting, approving, implementing, and monitoring treatments for identified AI risks before production authorization or continued operation.",
      "conditions": [
        "High-priority risks have documented treatments."
      ],
      "expected_evidence": [
        "Approved treatment plans for high-priority AI risks."
      ],
      "known_gaps": [
        "RSK-120 focuses on risk treatment and residual acceptance, not expressly on maximizing AI benefits."
      ]
    },
    {
      "esaf_control_id": "RSK-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "RSK-130 requires documenting mitigations and unresolved impacts for beneficial and adverse impacts of E2–E4 capabilities before authorization.",
      "conditions": [
        "The capability is E2–E4 and impact mitigations address high-priority negative impacts."
      ],
      "expected_evidence": [
        "Impact assessment mitigations for high-priority adverse impacts."
      ],
      "known_gaps": [
        "RSK-130 is pre-authorization impact assessment, not ongoing high-priority risk-response planning for all risks."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-1.3 mapping record."
    }
  ]
}
---
# MANAGE-1.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
