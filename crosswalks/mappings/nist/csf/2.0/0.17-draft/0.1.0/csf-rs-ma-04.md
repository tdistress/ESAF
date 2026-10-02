---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-ma-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.MA-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incidents are escalated or elevated as needed"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.MA-04"
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
      "rationale": "OPS-120 requires escalating AI incidents as needed within integrated enterprise incident management.",
      "conditions": [
        "AI incidents are escalated or elevated as needed."
      ],
      "expected_evidence": [
        "Escalation records for AI incidents."
      ],
      "known_gaps": [
        "OPS-120 escalation is AI-incident scoped."
      ]
    },
    {
      "esaf_control_id": "MON-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-140 requires escalating AI alerts as needed.",
      "conditions": [
        "Pre-incident AI alerts are escalated when triage requires elevation."
      ],
      "expected_evidence": [
        "Alert escalation records."
      ],
      "known_gaps": [
        "MON-140 is alert escalation, not full incident elevation governance."
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
      "change": "Created the draft NIST CSF 2.0 RS.MA-04 mapping record."
    }
  ]
}
---
# RS.MA-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
