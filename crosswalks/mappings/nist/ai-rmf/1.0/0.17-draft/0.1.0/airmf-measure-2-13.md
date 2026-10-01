---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-13",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.13",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Effectiveness of employed TEVV metrics and processes in measuring risk inputs and outcomes is evaluated and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.13"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AUD-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AUD-140 requires executive review of the AI management system using current information on control effectiveness, assessments, and improvement needs, with recorded decisions.",
      "conditions": [
        "Management review includes effectiveness of AI assessment/measurement controls used for risk inputs and outcomes."
      ],
      "expected_evidence": [
        "Management-review records addressing assessment/control effectiveness and improvements."
      ],
      "known_gaps": [
        "AUD-140 does not expressly evaluate TEVV metrics and processes as a named effectiveness review."
      ]
    },
    {
      "esaf_control_id": "AUD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "AUD-100 requires a risk-based assessment program defining methods, criteria, frequency, and follow-up for assessing AI capabilities and controls.",
      "conditions": [
        "Assessment program methods are periodically adjusted based on follow-up findings."
      ],
      "expected_evidence": [
        "Assessment program plans and follow-up records."
      ],
      "known_gaps": [
        "AUD-100 establishes the program; it does not require meta-evaluation of TEVV metric effectiveness."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.13 mapping record."
    }
  ]
}
---
# MEASURE-2.13

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
