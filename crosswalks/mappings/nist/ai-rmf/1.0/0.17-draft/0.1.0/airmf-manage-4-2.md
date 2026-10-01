---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-4-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-4.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Measurable continual-improvement activities are integrated into AI system updates and include regular engagement with interested parties."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-4.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AUD-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "AUD-140 requires executive review using improvement needs and recording resulting decisions at planned intervals.",
      "conditions": [
        "Improvement decisions from management review feed AI system updates."
      ],
      "expected_evidence": [
        "Management-review decisions and resulting improvement actions."
      ],
      "known_gaps": [
        "AUD-140 does not expressly require regular engagement with external interested parties or communities."
      ]
    },
    {
      "esaf_control_id": "OPS-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-110 requires controlled deployment of changes to AI capabilities according to impact and risk.",
      "conditions": [
        "Continual-improvement changes are implemented through controlled updates."
      ],
      "expected_evidence": [
        "Change records implementing improvement actions."
      ],
      "known_gaps": [
        "OPS-110 does not define continual-improvement measurement or interested-party engagement."
      ]
    },
    {
      "esaf_control_id": "STR-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "STR-110 requires periodic evaluation of intended outcomes, costs, adverse effects, and continuation criteria.",
      "conditions": [
        "Periodic value evaluation identifies improvement or continuation actions."
      ],
      "expected_evidence": [
        "Periodic evaluation records leading to update actions."
      ],
      "known_gaps": [
        "STR-110 does not require engagement with interested parties as part of continual improvement."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-4.2 mapping record."
    }
  ]
}
---
# MANAGE-4.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
