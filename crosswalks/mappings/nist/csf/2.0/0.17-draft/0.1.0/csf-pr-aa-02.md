---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-aa-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.AA-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Identities are proofed and bound to credentials based on the context of interactions"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.AA-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "IAM-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "IAM-110 requires authenticating before access to non-public AI assets with strength proportionate to risk.",
      "conditions": [
        "Identity proofing and credential binding for AI access follows risk-proportionate authentication context."
      ],
      "expected_evidence": [
        "Authentication policy and enrollment records for AI-access identities."
      ],
      "known_gaps": [
        "IAM-110 does not expressly require formal identity proofing workflows for all identity types enterprise-wide."
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
      "change": "Created the draft NIST CSF 2.0 PR.AA-02 mapping record."
    }
  ]
}
---
# PR.AA-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
