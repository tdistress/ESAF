---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-co-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.CO-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Internal and external stakeholders are notified of incidents"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.CO-02"
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
      "rationale": "OPS-120 requires notifying internal and external stakeholders of AI incidents as part of incident management.",
      "conditions": [
        "Internal and external stakeholders are notified of AI incidents."
      ],
      "expected_evidence": [
        "Incident notification records to designated stakeholders."
      ],
      "known_gaps": [
        "OPS-120 notification scope is AI-incident stakeholders, not all enterprise notification matrices."
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
      "change": "Created the draft NIST CSF 2.0 RS.CO-02 mapping record."
    }
  ]
}
---
# RS.CO-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
