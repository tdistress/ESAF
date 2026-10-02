---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ds-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.DS-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The confidentiality, integrity, and availability of data-in-transit are protected"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.DS-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "INF-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "INF-140 requires approved cryptography for AI data paths including transit protections where applicable.",
      "conditions": [
        "Confidentiality, integrity, and availability of AI data-in-transit are protected using approved cryptography."
      ],
      "expected_evidence": [
        "Transit encryption configurations for AI data paths."
      ],
      "known_gaps": [
        "INF-140 does not protect all enterprise data-in-transit outside AI paths."
      ]
    },
    {
      "esaf_control_id": "API-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "API-110 requires encrypting AI-related APIs among other API security controls.",
      "conditions": [
        "AI-related API data-in-transit is protected."
      ],
      "expected_evidence": [
        "API TLS/encryption configurations for AI APIs."
      ],
      "known_gaps": [
        "API-110 covers AI-related APIs only."
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
      "change": "Created the draft NIST CSF 2.0 PR.DS-02 mapping record."
    }
  ]
}
---
# PR.DS-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
