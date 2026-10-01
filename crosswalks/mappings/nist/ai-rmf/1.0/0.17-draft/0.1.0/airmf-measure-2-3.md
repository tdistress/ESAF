---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "AI system performance or assurance criteria are measured and demonstrated for conditions similar to deployment settings."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.3"
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
      "rationale": "MOD-120 requires validating each model against approved criteria for intended performance and operating conditions before authorization and after material change.",
      "conditions": [
        "Validation includes operating conditions representative of deployment settings."
      ],
      "expected_evidence": [
        "Model validation results demonstrating performance under stated operating conditions."
      ],
      "known_gaps": [
        "MOD-120 does not expressly require production-identical environment demonstration for every criterion."
      ]
    },
    {
      "esaf_control_id": "APP-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "APP-140 requires controlled testing practices for AI application code, prompts, workflows, configurations, and AI-generated artifacts.",
      "conditions": [
        "Application-level assurance testing supplements model validation for deployment-like conditions."
      ],
      "expected_evidence": [
        "AI application test records for release/assurance criteria."
      ],
      "known_gaps": [
        "APP-140 is software assurance testing, not full system trustworthiness measurement in production settings."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.3 mapping record."
    }
  ]
}
---
# MEASURE-2.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
