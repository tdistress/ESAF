---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-5",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.5",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The AI system to be deployed is demonstrated to be valid and reliable."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.5"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MOD-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "MOD-120 requires validating each model against approved criteria for intended performance, limitations, safety, security, robustness, and operating conditions before authorization.",
      "conditions": [
        "Deployment authorization depends on successful MOD-120 validation."
      ],
      "expected_evidence": [
        "Model validation and authorization records demonstrating intended performance and robustness."
      ],
      "known_gaps": [
        "MOD-120 validates models; full system validity/reliability may require additional application/service evidence."
      ]
    },
    {
      "esaf_control_id": "RSK-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-120 requires residual-risk acceptance from a commensurate authority before production authorization.",
      "conditions": [
        "Production authorization includes acceptance that residual validity/reliability risk is acceptable."
      ],
      "expected_evidence": [
        "Production authorization with residual-risk acceptance."
      ],
      "known_gaps": [
        "RSK-120 accepts residual risk; it does not itself demonstrate validity and reliability."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.5 mapping record."
    }
  ]
}
---
# MEASURE-2.5

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
