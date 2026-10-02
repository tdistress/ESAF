---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-aa-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.AA-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Identities and credentials for authorized users, services, and hardware are managed by the organization"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.AA-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "IAM-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "IAM-100 requires uniquely identifying, inventorying, owning, and lifecycle-managing human, service, workload, API, and agent identities with AI access.",
      "conditions": [
        "Identities and credentials for authorized users, services, and AI-related workloads with AI access are managed by the organization."
      ],
      "expected_evidence": [
        "Identity inventory, ownership, and lifecycle records for AI-access identities."
      ],
      "known_gaps": [
        "IAM-100 does not manage identities for all enterprise hardware and non-AI systems."
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
      "change": "Created the draft NIST CSF 2.0 PR.AA-01 mapping record."
    }
  ]
}
---
# PR.AA-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
