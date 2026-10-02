---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-am-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.AM-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Inventories of software, services, and systems managed by the organization are maintained"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.AM-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "GOV-120 requires portfolio oversight that maintains an inventory of in-scope AI capabilities with owners, risk classification, and lifecycle state.",
      "conditions": [
        "Inventories of AI software, services, and systems managed by the organization are maintained through the AI portfolio."
      ],
      "expected_evidence": [
        "AI portfolio inventory with owners, risk classification, and lifecycle state."
      ],
      "known_gaps": [
        "GOV-120 does not inventory non-AI enterprise software, services, and systems."
      ]
    },
    {
      "esaf_control_id": "MOD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-100 requires registering every material model with identity, owner, purpose, version, risk, validation, and deployment before use.",
      "conditions": [
        "Material models used as software/services are inventoried in the model register."
      ],
      "expected_evidence": [
        "Model registry entries for material models."
      ],
      "known_gaps": [
        "MOD-100 covers models, not all enterprise software."
      ]
    },
    {
      "esaf_control_id": "API-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "API-120 requires inventorying tools and plugins an AI can invoke.",
      "conditions": [
        "AI-invocable tools/plugins are inventoried as software/services in scope."
      ],
      "expected_evidence": [
        "Approved tool/plugin inventory for AI systems."
      ],
      "known_gaps": [
        "API-120 does not inventory general enterprise software."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-project-owner",
    "date": "2026-10-02"
  },
  "change_history": [
    {
      "version": "0.1.0",
      "date": "2026-10-02",
      "change": "Created the draft NIST CSF 2.0 ID.AM-02 mapping record."
    }
  ]
}
---
# ID.AM-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
