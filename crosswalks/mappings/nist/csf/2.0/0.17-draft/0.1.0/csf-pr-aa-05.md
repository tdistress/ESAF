---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-aa-05",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.AA-05",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.AA-05"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "IAM-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "IAM-120 requires authorizing AI assets and actions by purpose, role, attributes, context, and least privilege.",
      "conditions": [
        "Access permissions, entitlements, and authorizations for AI are defined in policy, managed, enforced, and reviewed with least privilege."
      ],
      "expected_evidence": [
        "Authorization policies, entitlement reviews, and enforcement evidence for AI access."
      ],
      "known_gaps": [
        "IAM-120 does not manage entitlements for all non-AI enterprise systems."
      ]
    },
    {
      "esaf_control_id": "IAM-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "IAM-150 requires reviewing AI access at risk-defined frequency and revoking or adjusting on role/scope/need change.",
      "conditions": [
        "AI access authorizations are reviewed and adjusted."
      ],
      "expected_evidence": [
        "Access review records and revocation evidence."
      ],
      "known_gaps": [
        "IAM-150 is AI-access review, not enterprise-wide IAM review."
      ]
    },
    {
      "esaf_control_id": "IAM-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "IAM-130 requires restricting, separately authenticating, time-bounding, monitoring, and reviewing privileged AI-changing access.",
      "conditions": [
        "Privileged entitlements for AI-changing access incorporate least privilege and review."
      ],
      "expected_evidence": [
        "Privileged access records and reviews for AI."
      ],
      "known_gaps": [
        "IAM-130 covers privileged AI-changing access only."
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
      "change": "Created the draft NIST CSF 2.0 PR.AA-05 mapping record."
    }
  ]
}
---
# PR.AA-05

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
