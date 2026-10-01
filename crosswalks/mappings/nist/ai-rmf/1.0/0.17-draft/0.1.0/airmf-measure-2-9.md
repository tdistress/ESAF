---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-9",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.9",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The AI model is explained, validated, and documented, and AI system output is interpreted within its context to inform risk-management decisions."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.9"
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
      "rationale": "MOD-120 requires validation against explainability and intended-performance criteria and documentation of validation before authorization and after material change.",
      "conditions": [
        "Explainability and validation results are available for risk-management decisions."
      ],
      "expected_evidence": [
        "Model validation documentation covering explainability and performance."
      ],
      "known_gaps": [
        "MOD-120 does not require operational interpretation of every system output in context."
      ]
    },
    {
      "esaf_control_id": "APP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "APP-120 requires validating, constraining, encoding, labeling, and authorizing AI output before presentation, execution, persistence, or downstream use according to content, destination, intended action, uncertainty, and impact.",
      "conditions": [
        "Output handling considers uncertainty and impact before use."
      ],
      "expected_evidence": [
        "Output validation/labeling controls and authorization rules."
      ],
      "known_gaps": [
        "APP-120 governs safe output consumption, not model explanation documentation."
      ]
    },
    {
      "esaf_control_id": "DAT-160",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "DAT-160 requires classifying, validating, and labeling AI outputs according to content, source data, intended use, reliability, and downstream impact.",
      "conditions": [
        "Output labeling/reliability metadata supports contextual interpretation."
      ],
      "expected_evidence": [
        "Output classification and reliability labeling records."
      ],
      "known_gaps": [
        "DAT-160 does not explain the model or validate it."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.9 mapping record."
    }
  ]
}
---
# MEASURE-2.9

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
