---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-4-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-4.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Practices enable AI testing, identification of unexpected functionality and behavior, and human override of AI system performance when needed."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-4.3"
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
      "rationale": "MOD-120 requires validating each model against approved criteria for intended performance, limitations, safety, security, robustness, fairness, privacy, explainability, resilience, and operating conditions before authorization and after material change.",
      "conditions": [
        "Model validation is used to detect unexpected or out-of-limit behavior before authorization."
      ],
      "expected_evidence": [
        "Model validation records covering performance, limitations, and safety criteria."
      ],
      "known_gaps": [
        "MOD-120 does not expressly require runtime human override mechanisms."
      ]
    },
    {
      "esaf_control_id": "AGT-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "AGT-120 requires human approval, supervision, intervention, challenge, and appeal, including conditions that prohibit autonomous execution.",
      "conditions": [
        "The system includes agent or autonomous paths where override/intervention applies."
      ],
      "expected_evidence": [
        "Oversight procedures defining intervention and prohibition-of-autonomy conditions."
      ],
      "known_gaps": [
        "AGT-120 is agent-scoped and does not cover all AI system override paths."
      ]
    },
    {
      "esaf_control_id": "APP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "APP-100 requires design documentation of threat and misuse cases, failure modes, human-oversight points, and risk-proportionate validation criteria.",
      "conditions": [
        "Application design includes oversight and validation against unexpected behavior."
      ],
      "expected_evidence": [
        "Design documentation listing failure modes and human-oversight points."
      ],
      "known_gaps": [
        "APP-100 is design-time; it does not alone operate production override controls."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-4.3 mapping record."
    }
  ]
}
---
# GOVERN-4.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
