---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ps-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.PS-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Configuration management practices are established and applied"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.PS-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "INF-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "INF-110 requires hardening AI compute, hosts, containers, networks, storage, runtimes, and management via approved baselines.",
      "conditions": [
        "Configuration management practices are established and applied to AI infrastructure."
      ],
      "expected_evidence": [
        "Hardening baselines and compliance evidence for AI infrastructure."
      ],
      "known_gaps": [
        "INF-110 does not establish enterprise configuration management for all non-AI assets."
      ]
    },
    {
      "esaf_control_id": "INF-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "INF-130 requires managing AI infrastructure as versioned, reviewed, tested, and approved configuration with rollback/recovery.",
      "conditions": [
        "AI infrastructure configuration is version-controlled and approved."
      ],
      "expected_evidence": [
        "Versioned infra-as-code or config records with review/approval."
      ],
      "known_gaps": [
        "INF-130 is AI infrastructure focused."
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
      "change": "Created the draft NIST CSF 2.0 PR.PS-01 mapping record."
    }
  ]
}
---
# PR.PS-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
