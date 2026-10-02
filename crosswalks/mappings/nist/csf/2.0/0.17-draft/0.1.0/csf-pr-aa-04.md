---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-aa-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.AA-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Identity assertions are protected, conveyed, and verified"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.AA-04"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "IAM-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "IAM-110 requires authentication strength proportionate to risk for access to non-public AI assets.",
      "conditions": [
        "Identity assertions used for AI access are protected, conveyed, and verified as part of authentication."
      ],
      "expected_evidence": [
        "Authentication protocol configurations and assertion verification evidence for AI access."
      ],
      "known_gaps": [
        "IAM-110 does not specify federation assertion protections for all enterprise identity systems."
      ]
    },
    {
      "esaf_control_id": "API-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "API-110 requires authenticating, authorizing, and protecting AI-related APIs.",
      "conditions": [
        "API identity assertions for AI integrations are protected and verified."
      ],
      "expected_evidence": [
        "API authN configurations for AI-related APIs."
      ],
      "known_gaps": [
        "API-110 is API-scoped rather than a general identity-assertion control."
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
      "change": "Created the draft NIST CSF 2.0 PR.AA-04 mapping record."
    }
  ]
}
---
# PR.AA-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
