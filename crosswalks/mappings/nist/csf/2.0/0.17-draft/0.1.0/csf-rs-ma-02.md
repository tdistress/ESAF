---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-ma-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.MA-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incident reports are triaged and validated"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.MA-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-140 requires triaging AI alerts before escalation and containment.",
      "conditions": [
        "Incident reports/alerts for AI are triaged and validated."
      ],
      "expected_evidence": [
        "Triage and validation records for AI incident reports/alerts."
      ],
      "known_gaps": [
        "MON-140 triage precedes full incident declaration in many cases."
      ]
    },
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-120 requires AI incident management including validation of incident reports.",
      "conditions": [
        "AI incident reports are triaged and validated within the incident process."
      ],
      "expected_evidence": [
        "Incident triage/validation records."
      ],
      "known_gaps": [
        "OPS-120 does not triage all enterprise incident reports outside AI."
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
      "change": "Created the draft NIST CSF 2.0 RS.MA-02 mapping record."
    }
  ]
}
---
# RS.MA-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
