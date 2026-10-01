---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-3-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-3.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Pre-trained models used for development are monitored as part of regular AI system monitoring and maintenance."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-3.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MOD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-100 requires registering every material model with owner, lifecycle state, validation status, deployment relationships, and review date before approved use.",
      "conditions": [
        "Pre-trained models used in development are material models under MOD-100."
      ],
      "expected_evidence": [
        "Model registry entries for pre-trained models with review dates and lifecycle state."
      ],
      "known_gaps": [
        "MOD-100 registers models; continuous runtime monitoring relies on MON/OPS controls."
      ]
    },
    {
      "esaf_control_id": "MOD-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MOD-110 requires verifying provenance, source, licensing, integrity, dependencies, known limitations, and supplier terms before approved use.",
      "conditions": [
        "Pre-trained model supply-chain attributes are established before use."
      ],
      "expected_evidence": [
        "Provenance/supply-chain verification records for pre-trained models."
      ],
      "known_gaps": [
        "MOD-110 is pre-use verification, not continuous monitoring."
      ]
    },
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-120 requires monitoring production AI behavior including performance and emerging limitations against baselines.",
      "conditions": [
        "Deployed systems using pre-trained models are monitored in production."
      ],
      "expected_evidence": [
        "Production monitoring covering models in deployment relationships."
      ],
      "known_gaps": [
        "MON-120 monitors production behavior; development-only pre-trained models may not be production-monitored."
      ]
    },
    {
      "esaf_control_id": "MOD-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MOD-130 requires uniquely versioning, authorizing, testing, deploying, monitoring, and supporting rollback for model and provider-version changes.",
      "conditions": [
        "Provider version changes to pre-trained models are monitored and controlled."
      ],
      "expected_evidence": [
        "Model change/version records including provider-version monitoring."
      ],
      "known_gaps": [
        "MOD-130 focuses on change control rather than continuous benefit/risk monitoring of third-party pre-trained models."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-3.2 mapping record."
    }
  ]
}
---
# MANAGE-3.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
