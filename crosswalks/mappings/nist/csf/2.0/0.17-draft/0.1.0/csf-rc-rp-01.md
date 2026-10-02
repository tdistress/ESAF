---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rc-rp-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RC.RP-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The recovery portion of the incident response plan is executed once initiated from the incident response process"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RC.RP-01"
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
      "rationale": "OPS-120 requires executing recovery as part of the AI incident response plan once initiated from the incident response process.",
      "conditions": [
        "The recovery portion of the AI incident response plan is executed once initiated."
      ],
      "expected_evidence": [
        "Recovery execution records linked to AI incidents."
      ],
      "known_gaps": [
        "OPS-120 recovery is AI-incident scoped."
      ]
    },
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-130 requires implementing recovery arrangements for AI services.",
      "conditions": [
        "AI recovery arrangements are executed when recovery is initiated."
      ],
      "expected_evidence": [
        "Recovery runbook execution records for AI."
      ],
      "known_gaps": [
        "OPS-130 may also support non-incident continuity recovery."
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
      "change": "Created the draft NIST CSF 2.0 RC.RP-01 mapping record."
    }
  ]
}
---
# RC.RP-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
