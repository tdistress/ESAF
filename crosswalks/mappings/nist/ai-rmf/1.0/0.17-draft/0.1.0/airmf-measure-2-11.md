---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-11",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.11",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Fairness and bias identified during MAP are evaluated and results are documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.11"
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
      "rationale": "MOD-120 requires validation against fairness criteria before authorization and after material change.",
      "conditions": [
        "Fairness/bias evaluation is included in approved validation criteria."
      ],
      "expected_evidence": [
        "Model validation results documenting fairness evaluation."
      ],
      "known_gaps": [
        "MOD-120 does not prescribe specific bias metrics or demographic parity tests."
      ]
    },
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-120 requires monitoring production AI behavior for fairness against approved baselines and thresholds.",
      "conditions": [
        "The system is in production and fairness monitoring is configured."
      ],
      "expected_evidence": [
        "Fairness monitoring baselines and resulting alerts/investigations."
      ],
      "known_gaps": [
        "MON-120 monitors drift against baselines; it may not perform comprehensive bias audits."
      ]
    },
    {
      "esaf_control_id": "DAT-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "DAT-120 requires monitoring representativeness and fitness of data used by an AI capability.",
      "conditions": [
        "Data representativeness issues relevant to bias are monitored."
      ],
      "expected_evidence": [
        "Data suitability monitoring evidence for representativeness."
      ],
      "known_gaps": [
        "DAT-120 is data fitness, not a complete fairness evaluation of system outcomes."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.11 mapping record."
    }
  ]
}
---
# MEASURE-2.11

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
