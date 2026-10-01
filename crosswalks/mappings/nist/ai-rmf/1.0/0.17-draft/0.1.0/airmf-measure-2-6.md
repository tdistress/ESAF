---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-6",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.6",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The AI system is evaluated regularly for safety risks identified during MAP."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.6"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-120 requires monitoring production AI behavior for safety against approved baselines and thresholds.",
      "conditions": [
        "Safety risks identified for the system are reflected in monitoring baselines."
      ],
      "expected_evidence": [
        "Safety monitoring baselines and alert/investigation records."
      ],
      "known_gaps": [
        "MON-120 is continuous monitoring, not a complete periodic safety evaluation program for all MAP safety risks."
      ]
    },
    {
      "esaf_control_id": "MOD-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MOD-120 requires safety validation before authorization and after material change.",
      "conditions": [
        "Safety revalidation occurs after material changes under MOD-120."
      ],
      "expected_evidence": [
        "Safety validation results at authorization and after material change."
      ],
      "known_gaps": [
        "MOD-120 does not require regular safety evaluation on a fixed calendar independent of material change."
      ]
    },
    {
      "esaf_control_id": "RSK-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-140 requires reassessment, revalidation, and reauthorization before material changes that could alter performance or control effectiveness.",
      "conditions": [
        "Material changes trigger safety-related reassessment."
      ],
      "expected_evidence": [
        "Material-change risk review records."
      ],
      "known_gaps": [
        "RSK-140 is change-triggered, not periodic safety evaluation alone."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.6 mapping record."
    }
  ]
}
---
# MEASURE-2.6

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
