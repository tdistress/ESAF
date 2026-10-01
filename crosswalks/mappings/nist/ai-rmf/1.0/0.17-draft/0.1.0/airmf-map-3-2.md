---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-3-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-3.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Potential costs, including non-monetary costs from AI errors or trustworthiness shortfalls, are examined and documented relative to risk tolerance."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-3.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-130 requires assessing adverse impacts and documenting uncertainty, mitigations, and unresolved impacts before authorization for E2–E4 capabilities.",
      "conditions": [
        "Adverse impact examination includes non-monetary harms relevant to errors or trustworthiness."
      ],
      "expected_evidence": [
        "Impact assessment documenting adverse impacts and unresolved impacts."
      ],
      "known_gaps": [
        "RSK-130 does not expressly require a cost ledger of monetary and non-monetary error costs."
      ]
    },
    {
      "esaf_control_id": "STR-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "STR-110 requires evaluating costs and material adverse effects alongside intended outcomes and continuation criteria.",
      "conditions": [
        "Production capability evaluation includes costs and material adverse effects."
      ],
      "expected_evidence": [
        "Value-realization evaluation records covering costs and adverse effects."
      ],
      "known_gaps": [
        "STR-110 does not explicitly tie cost examination to organizational risk-tolerance thresholds."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-3.2 mapping record."
    }
  ]
}
---
# MAP-3.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
