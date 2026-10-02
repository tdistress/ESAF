---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-sc-06",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.SC-06",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Planning and due diligence are performed to reduce risks before entering into formal supplier or other third-party relationships"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.SC-06"
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
      "rationale": "CMP-120 requires due diligence through verification of third-party AI duties before and during relationships.",
      "conditions": [
        "Planning and due diligence are performed to reduce AI supplier risks before formal relationships."
      ],
      "expected_evidence": [
        "Due-diligence assessments and onboarding records for AI suppliers."
      ],
      "known_gaps": [
        "CMP-120 does not define enterprise procurement due diligence outside AI."
      ]
    },
    {
      "esaf_control_id": "MOD-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MOD-110 requires assessing authenticity, integrity, licensing, and supplier terms before model use.",
      "conditions": [
        "Pre-use assessment of model suppliers reduces acquisition risk."
      ],
      "expected_evidence": [
        "Pre-use model supply-chain assessment records."
      ],
      "known_gaps": [
        "MOD-110 applies to models, not all third-party relationship types."
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
      "change": "Created the draft NIST CSF 2.0 GV.SC-06 mapping record."
    }
  ]
}
---
# GV.SC-06

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
