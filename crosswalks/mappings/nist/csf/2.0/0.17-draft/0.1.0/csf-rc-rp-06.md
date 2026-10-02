---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rc-rp-06",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RC.RP-06",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The end of incident recovery is declared based on criteria, and incident- related documentation is completed • Incident Recovery Communication (RC.CO): Restoration activities are coordinated with internal and external parties"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RC.RP-06"
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
      "rationale": "OPS-120 requires declaring the end of AI incident recovery based on criteria and completing incident-related documentation.",
      "conditions": [
        "The end of AI incident recovery is declared based on criteria, and incident-related documentation is completed."
      ],
      "expected_evidence": [
        "Recovery-closure criteria application and completed incident documentation."
      ],
      "known_gaps": [
        "OPS-120 closure is AI-incident scoped."
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
      "change": "Created the draft NIST CSF 2.0 RC.RP-06 mapping record."
    }
  ]
}
---
# RC.RP-06

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
