---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-10",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.10",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Privacy risk of the AI system identified during MAP is examined and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.10"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "DAT-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "DAT-140 requires identifying and implementing privacy requirements for personal data processed by AI, including minimization, transparency, lawful basis, purpose limitation, retention, security, individual rights, automated-decision obligations, and cross-border transfer where applicable.",
      "conditions": [
        "The AI system processes personal data subject to DAT-140."
      ],
      "expected_evidence": [
        "Privacy requirements analysis and implementation evidence for the AI capability."
      ],
      "known_gaps": [
        "DAT-140 implements privacy requirements; it may not produce a standalone privacy-risk measurement report in AI RMF terms."
      ]
    },
    {
      "esaf_control_id": "MOD-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-120 requires validation against privacy criteria before authorization and after material change.",
      "conditions": [
        "Privacy is included in approved model validation criteria."
      ],
      "expected_evidence": [
        "Model validation results covering privacy criteria."
      ],
      "known_gaps": [
        "MOD-120 privacy validation is model-scoped, not a full system privacy-risk examination."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.10 mapping record."
    }
  ]
}
---
# MEASURE-2.10

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
