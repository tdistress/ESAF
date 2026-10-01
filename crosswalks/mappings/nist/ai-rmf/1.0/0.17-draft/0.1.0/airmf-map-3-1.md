---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-3-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-3.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Potential benefits of intended AI system functionality and performance are examined and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-3.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-130 requires assessing reasonably foreseeable beneficial and adverse impacts of E2–E4 AI capabilities and documenting evidence before authorization.",
      "conditions": [
        "The capability is E2–E4."
      ],
      "expected_evidence": [
        "Impact assessment documenting beneficial impacts of intended functionality."
      ],
      "known_gaps": [
        "RSK-130 does not apply to E1 capabilities."
      ]
    },
    {
      "esaf_control_id": "STR-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "STR-110 requires defining and periodically evaluating intended outcomes of each production AI capability using approved measures.",
      "conditions": [
        "Intended beneficial outcomes are defined as STR-110 measures for production capabilities."
      ],
      "expected_evidence": [
        "Approved intended-outcome measures for the capability."
      ],
      "known_gaps": [
        "STR-110 focuses on value realization for production systems, not all pre-production benefit examinations."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-3.1 mapping record."
    }
  ]
}
---
# MAP-3.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
