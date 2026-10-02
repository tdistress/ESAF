---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-an-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.AN-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Analysis is performed to establish what has taken place during an incident and the root cause of the incident"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.AN-03"
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
      "rationale": "OPS-120 requires analysis within AI incident management to establish what took place and root cause.",
      "conditions": [
        "Analysis establishes what took place during an AI incident and the root cause."
      ],
      "expected_evidence": [
        "Incident analysis and root-cause records."
      ],
      "known_gaps": [
        "OPS-120 analysis is AI-incident scoped."
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
      "change": "Created the draft NIST CSF 2.0 RS.AN-03 mapping record."
    }
  ]
}
---
# RS.AN-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
