---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-1-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-1.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Internal expertise independent of front-line developers and/or independent external evaluators are available to assist in evaluating AI trustworthiness and risk-management impacts."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-1.3"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AUD-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "AUD-110 requires assigning AI assessments to personnel with documented competence and independence proportionate to the subject, method, complexity, and risk being evaluated.",
      "conditions": [
        "AI trustworthiness or risk-management impact evaluations are performed as AI assessments under AUD-110."
      ],
      "expected_evidence": [
        "Assessor competence and independence records for AI assessments."
      ],
      "known_gaps": [
        "AUD-110 covers assessment assignments; it does not require standing external evaluators for every system."
      ]
    },
    {
      "esaf_control_id": "AUD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "prerequisite",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AUD-100 requires a risk-based AI assessment program defining responsibilities and independence expectations, establishing the program context in which independent evaluators operate.",
      "conditions": [
        "An AI assessment program exists under which independent evaluators are assigned."
      ],
      "expected_evidence": [
        "Assessment program documentation defining independence responsibilities."
      ],
      "known_gaps": [
        "AUD-100 alone does not staff independent evaluators."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-1.3 mapping record."
    }
  ]
}
---
# MEASURE-1.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
