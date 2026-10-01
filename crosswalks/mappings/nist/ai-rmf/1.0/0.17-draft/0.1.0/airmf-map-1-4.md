---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-1-4",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-1.4",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Business value or context of business use is clearly defined or re-evaluated for existing AI systems."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-1.4"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "STR-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "STR-110 requires the accountable business owner to define, measure, and periodically evaluate each production AI capability's intended outcomes, costs, material adverse effects, and continuation criteria using approved measures established before production authorization.",
      "conditions": [
        "The AI system is a production capability under STR-110, or is being re-evaluated for continuation."
      ],
      "expected_evidence": [
        "Value-realization measures and periodic evaluation records for intended outcomes and continuation."
      ],
      "known_gaps": [
        "STR-110 applies to production capabilities; pre-production business-case definition may rely on adjacent controls."
      ]
    },
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-130 requires documented owner authority for purpose and outcomes of each in-scope AI capability.",
      "conditions": [
        "Business-use context is captured in the capability purpose/outcomes statement."
      ],
      "expected_evidence": [
        "Capability ownership record stating purpose and outcomes."
      ],
      "known_gaps": [
        "GOV-130 does not require periodic business-value re-evaluation metrics."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-1.4 mapping record."
    }
  ]
}
---
# MAP-1.4

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
