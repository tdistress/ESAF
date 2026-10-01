---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-1-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-1.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Processes determine the needed level of AI risk-management activity based on organizational risk tolerance."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-1.3"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-100 requires an approved AI risk methodology defining scope, risk dimensions, rating criteria, inherent and residual risk, treatment, acceptance, monitoring, reassessment, and escalation.",
      "conditions": [
        "The methodology's rating and acceptance criteria are used to scale risk-management activity."
      ],
      "expected_evidence": [
        "Approved AI risk methodology documenting how risk level drives treatment and oversight intensity."
      ],
      "known_gaps": [
        "RSK-100 does not use the NIST phrase 'risk tolerance' as a named artifact."
      ]
    },
    {
      "esaf_control_id": "RSK-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-110 requires classification of each in-scope AI capability before approved use using documented impact, likelihood, uncertainty, autonomy, data sensitivity, affected parties, and related criteria.",
      "conditions": [
        "Capability classification is used to determine proportionate risk-management activities."
      ],
      "expected_evidence": [
        "Capability risk-classification records linked to required control intensity."
      ],
      "known_gaps": [
        "RSK-110 classifies capabilities; it does not alone set enterprise risk-tolerance statements."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-1.3 mapping record."
    }
  ]
}
---
# GOVERN-1.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
