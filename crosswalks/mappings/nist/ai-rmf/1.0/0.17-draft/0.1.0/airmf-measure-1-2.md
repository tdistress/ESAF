---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-1-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-1.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Approaches for assessing AI trustworthiness characteristics and risk-management impacts are identified and evaluated for effectiveness in context."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-1.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MOD-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-120 requires validation against approved, risk-proportionate criteria for intended performance, limitations, safety, security, robustness, fairness, privacy, explainability, resilience, and operating conditions.",
      "conditions": [
        "Trustworthiness assessment approaches are expressed as MOD-120 validation criteria."
      ],
      "expected_evidence": [
        "Approved model validation criteria and results."
      ],
      "known_gaps": [
        "MOD-120 does not expressly require evaluating the effectiveness of the assessment approaches themselves over time."
      ]
    },
    {
      "esaf_control_id": "AUD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AUD-100 requires a risk-based assessment program defining scope, criteria, frequency, methods, and follow-up for assessing the AI management system, capabilities, and controls.",
      "conditions": [
        "Assessment program methods evaluate trustworthiness-related controls or impacts in context."
      ],
      "expected_evidence": [
        "Assessment program plan defining methods and criteria."
      ],
      "known_gaps": [
        "AUD-100 assesses management system/controls; it may not assess every trustworthiness characteristic of each model."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-1.2 mapping record."
    }
  ]
}
---
# MEASURE-1.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
