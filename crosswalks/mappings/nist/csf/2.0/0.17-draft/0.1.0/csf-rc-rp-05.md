---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rc-rp-05",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RC.RP-05",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The integrity of restored assets is verified, systems and services are restored, and normal operating status is confirmed"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RC.RP-05"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-130 requires verifying restored AI assets, restoring systems and services, and confirming normal operating status.",
      "conditions": [
        "Integrity of restored AI assets is verified, systems and services are restored, and normal operating status is confirmed."
      ],
      "expected_evidence": [
        "Restoration verification and service-restoration confirmation records for AI."
      ],
      "known_gaps": [
        "OPS-130 restoration is AI-service scoped."
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
      "change": "Created the draft NIST CSF 2.0 RC.RP-05 mapping record."
    }
  ]
}
---
# RC.RP-05

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
