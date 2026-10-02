---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-ma-05",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.MA-05",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The criteria for initiating incident recovery are applied • Incident Analysis (RS.AN): Investigations are conducted to ensure effective response and support forensics and recovery activities"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.MA-05"
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
      "rationale": "OPS-120 requires applying criteria for transitioning AI incidents into recovery as part of the incident lifecycle.",
      "conditions": [
        "Criteria for initiating incident recovery are applied for AI incidents."
      ],
      "expected_evidence": [
        "Incident records showing recovery-initiation criteria application."
      ],
      "known_gaps": [
        "OPS-120 does not define recovery criteria for all enterprise incident types outside AI."
      ]
    },
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-130 requires recovery arrangements that are initiated when recovery criteria are met.",
      "conditions": [
        "AI recovery arrangements are initiated according to defined criteria."
      ],
      "expected_evidence": [
        "Recovery initiation records for AI services."
      ],
      "known_gaps": [
        "OPS-130 focuses on continuity/recovery arrangements rather than incident-process criteria alone."
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
      "change": "Created the draft NIST CSF 2.0 RS.MA-05 mapping record."
    }
  ]
}
---
# RS.MA-05

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
