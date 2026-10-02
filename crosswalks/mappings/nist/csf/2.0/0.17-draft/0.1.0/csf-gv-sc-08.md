---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-sc-08",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.SC-08",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Relevant suppliers and other third parties are included in incident planning, response, and recovery activities"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.SC-08"
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
      "rationale": "OPS-120 requires preparing for and running AI incident lifecycle integrated with enterprise incident management, including third-party-affecting incidents.",
      "conditions": [
        "Relevant AI suppliers and third parties are included in incident planning, response, and recovery activities for in-scope AI."
      ],
      "expected_evidence": [
        "Incident plans naming third parties, joint response records, and recovery coordination evidence."
      ],
      "known_gaps": [
        "OPS-120 does not include all enterprise suppliers in cyber incident planning outside AI."
      ]
    },
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "CMP-120 requires contractual incident duties for AI third parties.",
      "conditions": [
        "Incident roles for AI suppliers are established in contracts and exercised when needed."
      ],
      "expected_evidence": [
        "Contractual incident clauses and exercise/activation records."
      ],
      "known_gaps": [
        "CMP-120 does not itself run joint incident response."
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
      "change": "Created the draft NIST CSF 2.0 GV.SC-08 mapping record."
    }
  ]
}
---
# GV.SC-08

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
