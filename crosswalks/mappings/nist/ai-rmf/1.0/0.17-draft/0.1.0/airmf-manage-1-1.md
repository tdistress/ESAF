---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-1-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-1.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "A determination is made whether the AI system achieves intended purposes and objectives and whether development or deployment should proceed."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-1.1"
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
      "rationale": "RSK-120 requires residual-risk acceptance from a commensurate authority before production authorization or continued operation.",
      "conditions": [
        "Go/no-go for deployment is expressed through residual-risk acceptance before production authorization."
      ],
      "expected_evidence": [
        "Production authorization / residual-risk acceptance decision record."
      ],
      "known_gaps": [
        "RSK-120 accepts residual risk; it does not alone evaluate achievement of intended purposes."
      ]
    },
    {
      "esaf_control_id": "STR-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "STR-110 requires defining and periodically evaluating intended outcomes and continuation criteria for production AI capabilities.",
      "conditions": [
        "Continuation/go criteria include whether intended outcomes are being achieved."
      ],
      "expected_evidence": [
        "Value-realization evaluation against continuation criteria."
      ],
      "known_gaps": [
        "STR-110 applies to production capabilities and continuation, not all early development go/no-go gates."
      ]
    },
    {
      "esaf_control_id": "GOV-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-120 requires portfolio review using value, risk, and related information at defined frequency.",
      "conditions": [
        "Portfolio oversight includes proceed/continue decisions for capabilities."
      ],
      "expected_evidence": [
        "Portfolio review records with proceed/continue/retire decisions."
      ],
      "known_gaps": [
        "GOV-120 is periodic portfolio review, not system-specific development gate determination."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-1.1 mapping record."
    }
  ]
}
---
# MANAGE-1.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
