---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-3-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-3.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Risk-tracking approaches identify and monitor existing, emergent, and previously unidentified AI risks."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-3.2"
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
      "rationale": "RSK-100 requires monitoring, reassessment, and escalation as part of consistent AI risk methodology application.",
      "conditions": [
        "Tracking of existing and newly identified risks follows the approved methodology."
      ],
      "expected_evidence": [
        "Risk register/reassessment records showing monitoring of known and newly identified risks."
      ],
      "known_gaps": [
        "RSK-100 does not prescribe a specific emergent-risk sensing method beyond methodology requirements."
      ]
    },
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-120 requires monitoring for emerging limitations and related behavioral risk signals in production.",
      "conditions": [
        "Behavioral monitoring contributes to identification of previously unidentified risks."
      ],
      "expected_evidence": [
        "Monitoring evidence of emergent limitation detection."
      ],
      "known_gaps": [
        "MON-120 is production behavior monitoring, not a complete enterprise risk-tracking system."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-3.2 mapping record."
    }
  ]
}
---
# MEASURE-3.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
