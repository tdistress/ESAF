---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-4-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-4.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Measurement results regarding AI system trustworthiness in deployment settings inform AI risk-management approaches."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-4.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-100 requires monitoring, reassessment, and escalation using evidence within the AI risk methodology.",
      "conditions": [
        "Deployment measurement results are used as evidence for reassessment."
      ],
      "expected_evidence": [
        "Reassessment records citing production measurement/monitoring evidence."
      ],
      "known_gaps": [
        "RSK-100 does not specify trustworthiness measurement methods for deployment settings."
      ]
    },
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-120 requires monitoring production behavior for performance, safety, fairness, reliability, and related trustworthiness signals against baselines.",
      "conditions": [
        "Production monitoring results are available as trustworthiness measurement inputs."
      ],
      "expected_evidence": [
        "Production monitoring reports used in risk reviews."
      ],
      "known_gaps": [
        "MON-120 produces monitoring results; incorporation into risk management depends on RSK/AUD processes."
      ]
    },
    {
      "esaf_control_id": "AUD-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AUD-140 requires executive review using current risk, control-effectiveness, and assessment information with recorded decisions.",
      "conditions": [
        "Trustworthiness measurement results are included in management-review inputs."
      ],
      "expected_evidence": [
        "Management-review packs citing deployment trustworthiness measurements."
      ],
      "known_gaps": [
        "AUD-140 is periodic leadership review, not continuous risk-method updates."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-4.2 mapping record."
    }
  ]
}
---
# MEASURE-4.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
