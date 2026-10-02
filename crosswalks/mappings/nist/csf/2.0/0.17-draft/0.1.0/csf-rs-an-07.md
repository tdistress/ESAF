---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-an-07",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.AN-07",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incident data and metadata are collected, and their integrity and provenance are preserved"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.AN-07"
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
      "rationale": "MON-150 requires preserving protected audit trails including integrity for AI incident-related data.",
      "conditions": [
        "AI incident data and metadata are collected and their integrity and provenance are preserved."
      ],
      "expected_evidence": [
        "Protected incident data/metadata with integrity controls."
      ],
      "known_gaps": [
        "MON-150 does not collect all enterprise incident forensic artifacts outside AI."
      ]
    },
    {
      "esaf_control_id": "AGT-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AGT-140 requires recording attributable agent instructions, tools, approvals, actions, and outcomes for investigation.",
      "conditions": [
        "Agent-related incident data is collected with attribution for investigation."
      ],
      "expected_evidence": [
        "Agent action records used in investigations."
      ],
      "known_gaps": [
        "AGT-140 covers agents only."
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
      "change": "Created the draft NIST CSF 2.0 RS.AN-07 mapping record."
    }
  ]
}
---
# RS.AN-07

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
