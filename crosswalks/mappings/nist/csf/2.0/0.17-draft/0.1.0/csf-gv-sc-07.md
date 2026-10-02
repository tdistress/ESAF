---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-sc-07",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.SC-07",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The risks posed by a supplier, their products and services, and other third parties are understood, recorded, prioritized, assessed, responded to, and monitored over the course of the relationship"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.SC-07"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "CMP-120 requires understanding, recording, prioritizing, assessing, responding to, and monitoring risks from AI suppliers and their products/services.",
      "conditions": [
        "Risks posed by AI suppliers and other third parties supporting AI are understood, recorded, prioritized, assessed, and responded to over the relationship."
      ],
      "expected_evidence": [
        "Third-party AI risk records, assessments, responses, and monitoring evidence."
      ],
      "known_gaps": [
        "CMP-120 does not manage all non-AI supplier risks enterprise-wide."
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
      "change": "Created the draft NIST CSF 2.0 GV.SC-07 mapping record."
    }
  ]
}
---
# GV.SC-07

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
