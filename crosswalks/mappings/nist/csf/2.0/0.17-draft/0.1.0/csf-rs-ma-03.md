---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-ma-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.MA-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incidents are categorized and prioritized"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.MA-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-120 requires categorizing and prioritizing AI incidents as part of incident management.",
      "conditions": [
        "AI incidents are categorized and prioritized."
      ],
      "expected_evidence": [
        "Incident category and priority fields in incident records."
      ],
      "known_gaps": [
        "OPS-120 does not categorize all enterprise incidents outside AI."
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
      "change": "Created the draft NIST CSF 2.0 RS.MA-03 mapping record."
    }
  ]
}
---
# RS.MA-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
