---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ds-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.DS-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The confidentiality, integrity, and availability of data-at-rest are protected"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.DS-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "DAT-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "DAT-110 requires classifying AI data and enforcing handling across collection through disposal.",
      "conditions": [
        "Confidentiality, integrity, and availability protections for AI data-at-rest follow classification and handling rules."
      ],
      "expected_evidence": [
        "Data classification and handling evidence for AI data-at-rest."
      ],
      "known_gaps": [
        "DAT-110 does not protect all enterprise data-at-rest outside AI."
      ]
    },
    {
      "esaf_control_id": "INF-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "INF-140 requires using approved cryptography and key management for AI data, models, credentials, paths, and backups.",
      "conditions": [
        "Cryptographic protection is applied to AI data-at-rest as required by classification and policy."
      ],
      "expected_evidence": [
        "Crypto configurations and key-management evidence for AI data-at-rest."
      ],
      "known_gaps": [
        "INF-140 is AI-scoped cryptographic control."
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
      "change": "Created the draft NIST CSF 2.0 PR.DS-01 mapping record."
    }
  ]
}
---
# PR.DS-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
