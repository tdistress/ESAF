---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ds-10",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.DS-10",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The confidentiality, integrity, and availability of data-in-use are protected"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.DS-10"
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
      "rationale": "DAT-110 requires enforcing classified handling for AI data throughout processing, including data-in-use contexts.",
      "conditions": [
        "Confidentiality, integrity, and availability protections apply to AI data-in-use per handling rules."
      ],
      "expected_evidence": [
        "Handling controls and runtime protection evidence for AI data-in-use."
      ],
      "known_gaps": [
        "DAT-110 does not specify memory-encryption or TEE requirements for all enterprise data-in-use."
      ]
    },
    {
      "esaf_control_id": "APP-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "APP-130 requires isolating user/tenant/session/memory so identities get only authorized context and state.",
      "conditions": [
        "Data-in-use isolation protects confidentiality of AI session/memory state."
      ],
      "expected_evidence": [
        "Isolation design and test evidence for AI applications."
      ],
      "known_gaps": [
        "APP-130 is AI application isolation, not general OS data-in-use protection."
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
      "change": "Created the draft NIST CSF 2.0 PR.DS-10 mapping record."
    }
  ]
}
---
# PR.DS-10

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
