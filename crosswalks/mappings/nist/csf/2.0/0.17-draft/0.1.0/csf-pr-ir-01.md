---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ir-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.IR-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Networks and environments are protected from unauthorized logical access and usage"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.IR-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "INF-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "INF-110 requires hardening AI networks among other infrastructure components via approved baselines.",
      "conditions": [
        "Networks and environments hosting AI are protected from unauthorized logical access and usage via hardening baselines."
      ],
      "expected_evidence": [
        "Network hardening baselines and access-control evidence for AI environments."
      ],
      "known_gaps": [
        "INF-110 does not protect all enterprise networks outside AI hosting."
      ]
    },
    {
      "esaf_control_id": "API-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "API-100 requires routing production AI access through policy enforcement including identity, authorization, logging, limits, and kill capability.",
      "conditions": [
        "Logical access to production AI is constrained through a policy enforcement point."
      ],
      "expected_evidence": [
        "Policy-enforcement gateway configurations for production AI access."
      ],
      "known_gaps": [
        "API-100 does not segment or protect all enterprise network environments."
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
      "change": "Created the draft NIST CSF 2.0 PR.IR-01 mapping record."
    }
  ]
}
---
# PR.IR-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
