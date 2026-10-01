---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-1-5",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-1.5",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Organizational risk tolerances are determined and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-1.5"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "RSK-100 requires an approved AI risk methodology defining rating criteria, residual risk, treatment, acceptance, monitoring, reassessment, and escalation.",
      "conditions": [
        "Acceptance and rating criteria in the methodology are treated as the organization's documented AI risk tolerance expression."
      ],
      "expected_evidence": [
        "Approved AI risk methodology sections on acceptance thresholds and escalation."
      ],
      "known_gaps": [
        "RSK-100 does not expressly name or require a standalone 'risk tolerance' statement."
      ]
    },
    {
      "esaf_control_id": "STR-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "STR-100 requires AI objectives and investment priorities that trace to organizational strategy and risk appetite.",
      "conditions": [
        "Documented risk appetite in AI strategy is used as risk-tolerance input."
      ],
      "expected_evidence": [
        "Approved AI strategy referencing risk appetite."
      ],
      "known_gaps": [
        "STR-100 risk appetite is strategic and may not specify operational AI risk-tolerance thresholds."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-1.5 mapping record."
    }
  ]
}
---
# MAP-1.5

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
