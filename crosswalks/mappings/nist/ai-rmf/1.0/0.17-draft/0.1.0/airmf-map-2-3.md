---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-2-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-2.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Scientific integrity and TEVV considerations—including experimental design, data collection and selection, trustworthiness, and bias—are identified and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-2.3"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "DAT-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "DAT-120 requires defining, validating, and monitoring risk-proportionate criteria for accuracy, completeness, timeliness, relevance, representativeness, consistency, and fitness of data used by an AI capability.",
      "conditions": [
        "Data selection and suitability criteria are documented for the AI system."
      ],
      "expected_evidence": [
        "Data quality/suitability criteria and validation evidence."
      ],
      "known_gaps": [
        "DAT-120 does not require experimental-design documentation or full TEVV scientific-integrity controls."
      ]
    },
    {
      "esaf_control_id": "MOD-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-120 requires validation against criteria including fairness, safety, security, robustness, privacy, explainability, and operating conditions.",
      "conditions": [
        "Trustworthiness and bias-related validation criteria are identified before authorization."
      ],
      "expected_evidence": [
        "Model validation plan and results covering fairness and related trustworthiness criteria."
      ],
      "known_gaps": [
        "MOD-120 does not expressly require documenting experimental design or TEVV toolchains as scientific-integrity artifacts."
      ]
    },
    {
      "esaf_control_id": "STR-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "STR-120 requires authorizing AI experiments through a documented, time-bounded process with hypothesis, boundary, monitoring, and closure or lifecycle promotion.",
      "conditions": [
        "Experimental or evaluative work is conducted under STR-120."
      ],
      "expected_evidence": [
        "Experiment authorization records defining hypothesis and boundary."
      ],
      "known_gaps": [
        "STR-120 governs experiments; it does not establish full TEVV scientific-integrity requirements."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-2.3 mapping record."
    }
  ]
}
---
# MAP-2.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
