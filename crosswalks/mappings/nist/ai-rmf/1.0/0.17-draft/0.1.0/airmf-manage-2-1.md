---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-2-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-2.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Resources required to manage AI risks—and viable alternatives—are considered when making AI system go/no-go decisions."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-2.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "STR-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "STR-130 requires identifying, approving, and periodically reviewing people, competencies, funding, data, platforms, assurance, operational capacity, and supplier resources required to achieve AI objectives and maintain controls.",
      "conditions": [
        "Go/no-go decisions consider whether required risk-management resources are approved."
      ],
      "expected_evidence": [
        "Approved resource plans tied to capability authorization decisions."
      ],
      "known_gaps": [
        "STR-130 does not expressly require documenting viable alternatives in go/no-go records."
      ]
    },
    {
      "esaf_control_id": "RSK-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-120 requires residual-risk acceptance before production authorization or continued operation.",
      "conditions": [
        "Authorization considers whether treatments and residual risk are acceptable given available methods/resources."
      ],
      "expected_evidence": [
        "Authorization records referencing treatment feasibility and residual risk."
      ],
      "known_gaps": [
        "RSK-120 does not require an alternatives analysis for resource-constrained go/no-go decisions."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-2.1 mapping record."
    }
  ]
}
---
# MANAGE-2.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
