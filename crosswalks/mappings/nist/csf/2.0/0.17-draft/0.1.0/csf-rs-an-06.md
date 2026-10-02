---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-an-06",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.AN-06",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Actions performed during an investigation are recorded, and the records' integrity and provenance are preserved"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.AN-06"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-150 requires preserving protected audit trails for AI access, config, changes, privilege, agents, and incidents.",
      "conditions": [
        "Actions performed during an AI investigation are recorded with integrity and provenance preserved via protected audit trails."
      ],
      "expected_evidence": [
        "Protected investigation/audit-trail records for AI incidents."
      ],
      "known_gaps": [
        "MON-150 preserves trails but does not alone define investigative action logging procedures."
      ]
    },
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-120 requires documenting AI incident response actions.",
      "conditions": [
        "Investigative and response actions during AI incidents are recorded."
      ],
      "expected_evidence": [
        "Incident action logs."
      ],
      "known_gaps": [
        "OPS-120 does not specify cryptographic provenance for all investigation records."
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
      "change": "Created the draft NIST CSF 2.0 RS.AN-06 mapping record."
    }
  ]
}
---
# RS.AN-06

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
