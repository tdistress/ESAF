---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-ma-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.MA-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The incident response plan is executed in coordination with relevant third parties once an incident is declared"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.MA-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "OPS-120 requires executing the AI incident response plan in coordination with relevant third parties once an incident is declared.",
      "conditions": [
        "The AI incident response plan is executed in coordination with relevant third parties once an incident is declared."
      ],
      "expected_evidence": [
        "Executed incident response records naming third-party coordination."
      ],
      "known_gaps": [
        "OPS-120 coordination is AI-incident scoped."
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
      "change": "Created the draft NIST CSF 2.0 RS.MA-01 mapping record."
    }
  ]
}
---
# RS.MA-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
