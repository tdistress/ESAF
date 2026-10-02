---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-an-08",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.AN-08",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "An incident's magnitude is estimated and validated • Incident Response Reporting and Communication (RS.CO): Response activities are coordinated with internal and external stakeholders as required by laws, regulations, or policies"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.AN-08"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-120 requires estimating and validating AI incident magnitude as part of incident assessment.",
      "conditions": [
        "An AI incident's magnitude is estimated and validated."
      ],
      "expected_evidence": [
        "Incident magnitude estimation and validation records."
      ],
      "known_gaps": [
        "OPS-120 does not estimate magnitude for all enterprise incidents outside AI."
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
      "change": "Created the draft NIST CSF 2.0 RS.AN-08 mapping record."
    }
  ]
}
---
# RS.AN-08

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
