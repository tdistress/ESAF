---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ps-05",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.PS-05",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Installation and execution of unauthorized software are prevented"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.PS-05"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "API-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "API-120 requires inventorying, approving, authenticating, authorizing, constraining, monitoring, and retiring every tool/plugin an AI can invoke.",
      "conditions": [
        "Installation and execution of unauthorized AI tools/plugins are prevented through approval and enforcement."
      ],
      "expected_evidence": [
        "Approved tool/plugin allowlists and enforcement evidence."
      ],
      "known_gaps": [
        "API-120 does not prevent unauthorized software installation on all enterprise endpoints."
      ]
    },
    {
      "esaf_control_id": "INF-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "INF-110 requires hardening baselines for AI compute and runtimes that can constrain unauthorized software execution in AI environments.",
      "conditions": [
        "Hardening baselines for AI hosts/runtimes prevent unauthorized software where configured."
      ],
      "expected_evidence": [
        "Hardening baseline settings restricting unauthorized execution in AI environments."
      ],
      "known_gaps": [
        "INF-110 does not establish enterprise application-control for all endpoints."
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
      "change": "Created the draft NIST CSF 2.0 PR.PS-05 mapping record."
    }
  ]
}
---
# PR.PS-05

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
