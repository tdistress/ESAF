---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-3-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-3.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Targeted application scope is specified and documented based on system capability, established context, and AI system categorization."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-3.3"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-110 requires classifying each in-scope AI capability before approved use using documented criteria including impact, autonomy, data sensitivity, affected parties, external exposure, and criticality.",
      "conditions": [
        "Capability classification informs approved application scope."
      ],
      "expected_evidence": [
        "Capability risk-classification record used before approved use."
      ],
      "known_gaps": [
        "RSK-110 classifies risk; it does not alone specify functional application-scope boundaries."
      ]
    },
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "GOV-130 requires documented owner authority for purpose and outcomes of each AI capability.",
      "conditions": [
        "Approved purpose is used as the documented application-scope baseline."
      ],
      "expected_evidence": [
        "Capability purpose statement approved by accountable owners."
      ],
      "known_gaps": [
        "GOV-130 does not require scope specification from categorization taxonomies beyond purpose/outcomes."
      ]
    },
    {
      "esaf_control_id": "MOD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MOD-100 requires registering approved purpose, risk classification, and deployment relationships before approved model use.",
      "conditions": [
        "Material models declare approved purpose and deployment relationships within scope."
      ],
      "expected_evidence": [
        "Model registry entries with approved purpose and deployment relationships."
      ],
      "known_gaps": [
        "MOD-100 scopes models, not the full AI system application boundary."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-3.3 mapping record."
    }
  ]
}
---
# MAP-3.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
