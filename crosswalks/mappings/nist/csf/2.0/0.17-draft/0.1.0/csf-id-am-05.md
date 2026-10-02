---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-am-05",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.AM-05",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Assets are prioritized based on classification, criticality, resources, and impact on the mission"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.AM-05"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-110 requires classifying each AI capability before use based on impact, autonomy, data, exposure, criticality, and related factors.",
      "conditions": [
        "AI assets are prioritized based on classification, criticality, resources, and mission impact through risk classification."
      ],
      "expected_evidence": [
        "AI capability risk classifications and prioritization records."
      ],
      "known_gaps": [
        "RSK-110 classifies AI capabilities, not all enterprise assets."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-project-owner",
    "date": "2026-10-02"
  },
  "change_history": [
    {
      "version": "0.1.0",
      "date": "2026-10-02",
      "change": "Created the draft NIST CSF 2.0 ID.AM-05 mapping record."
    }
  ]
}
---
# ID.AM-05

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
