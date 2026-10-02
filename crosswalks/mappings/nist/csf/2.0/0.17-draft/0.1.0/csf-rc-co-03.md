---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rc-co-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RC.CO-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Recovery activities and progress in restoring operational capabilities are communicated to designated internal and external stakeholders"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RC.CO-03"
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
      "rationale": "OPS-120 requires communicating recovery activities and progress to designated internal and external stakeholders for AI incidents.",
      "conditions": [
        "Recovery activities and progress restoring AI operational capabilities are communicated to designated stakeholders."
      ],
      "expected_evidence": [
        "Recovery progress communications for AI incidents."
      ],
      "known_gaps": [
        "OPS-120 communication is AI-incident stakeholder scoped."
      ]
    },
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-130 recovery arrangements include stakeholder communication expectations for AI continuity events.",
      "conditions": [
        "AI recovery progress is communicated per continuity/recovery plans."
      ],
      "expected_evidence": [
        "Continuity recovery communications for AI."
      ],
      "known_gaps": [
        "OPS-130 may not cover all public/external stakeholder channels."
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
      "change": "Created the draft NIST CSF 2.0 RC.CO-03 mapping record."
    }
  ]
}
---
# RC.CO-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
