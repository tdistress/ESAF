---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-ra-10",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.RA-10",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Critical suppliers are assessed prior to acquisition • Improvement (ID.IM): Improvements to organizational cybersecurity risk management processes, procedures and activities are identified across all CSF Functions"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.RA-10"
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
      "rationale": "CMP-120 requires due diligence and verification of third-party AI security duties before and during relationships.",
      "conditions": [
        "Critical AI suppliers are assessed prior to acquisition."
      ],
      "expected_evidence": [
        "Pre-acquisition third-party AI due-diligence assessments."
      ],
      "known_gaps": [
        "CMP-120 does not assess all critical enterprise suppliers outside AI."
      ]
    },
    {
      "esaf_control_id": "MOD-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MOD-110 requires assessing model suppliers before use.",
      "conditions": [
        "Critical model suppliers are assessed prior to acquisition and use."
      ],
      "expected_evidence": [
        "Pre-use model supplier assessments."
      ],
      "known_gaps": [
        "MOD-110 covers model suppliers only."
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
      "change": "Created the draft NIST CSF 2.0 ID.RA-10 mapping record."
    }
  ]
}
---
# ID.RA-10

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
