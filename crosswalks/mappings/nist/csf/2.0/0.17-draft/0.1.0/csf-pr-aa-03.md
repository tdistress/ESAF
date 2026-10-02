---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-aa-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.AA-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Users, services, and hardware are authenticated"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.AA-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "IAM-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "IAM-110 requires authenticating users and services before access to non-public AI assets.",
      "conditions": [
        "Users, services, and workloads accessing AI assets are authenticated."
      ],
      "expected_evidence": [
        "Authentication configurations and access logs for AI assets."
      ],
      "known_gaps": [
        "IAM-110 does not authenticate access to all non-AI enterprise hardware/services."
      ]
    },
    {
      "esaf_control_id": "API-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "API-110 requires authenticating AI-related APIs.",
      "conditions": [
        "AI-related API clients and services are authenticated."
      ],
      "expected_evidence": [
        "API authentication configurations and logs."
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
      "change": "Created the draft NIST CSF 2.0 PR.AA-03 mapping record."
    }
  ]
}
---
# PR.AA-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
