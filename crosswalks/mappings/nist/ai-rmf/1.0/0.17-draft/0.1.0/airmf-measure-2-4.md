---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-4",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.4",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Functionality and behavior of the AI system and its components are monitored when in production."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.4"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "MON-120 requires monitoring production AI behavior for performance, quality, data and concept drift, safety, fairness, reliability, policy, uncertainty, and emerging limitations against approved baselines and thresholds.",
      "conditions": [
        "The AI system is in production."
      ],
      "expected_evidence": [
        "Production monitoring dashboards/alerts against approved baselines."
      ],
      "known_gaps": [
        "MON-120 may not monitor every MAP-identified component equally."
      ]
    },
    {
      "esaf_control_id": "MON-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-100 requires collecting attributable, protected, risk-proportionate telemetry sufficient to monitor AI identity, input, context, retrieval, model, output, tool, action, configuration, performance, cost, and policy events.",
      "conditions": [
        "Telemetry collection supports production functionality/behavior monitoring."
      ],
      "expected_evidence": [
        "Telemetry configuration covering model/output/performance events."
      ],
      "known_gaps": [
        "MON-100 collects telemetry; analysis and threshold response are covered by adjacent monitoring controls."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.4 mapping record."
    }
  ]
}
---
# MEASURE-2.4

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
