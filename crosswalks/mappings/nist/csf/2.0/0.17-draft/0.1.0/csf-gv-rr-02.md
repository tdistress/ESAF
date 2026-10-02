---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-rr-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.RR-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Roles, responsibilities, and authorities related to cybersecurity risk management are established, communicated, understood, and enforced"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.RR-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "GOV-100 requires documented accountability, membership, decision rights, and escalation paths for AI governance.",
      "conditions": [
        "Roles, responsibilities, and authorities for AI cybersecurity risk management are established and communicated through the governance charter."
      ],
      "expected_evidence": [
        "Governance charter, role definitions, and escalation paths."
      ],
      "known_gaps": [
        "GOV-100 does not define all enterprise cybersecurity roles outside AI."
      ]
    },
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "GOV-130 requires assigning accountable business and technical/service owners per AI capability.",
      "conditions": [
        "Capability-level cybersecurity risk roles are assigned to named owners."
      ],
      "expected_evidence": [
        "Capability ownership records with accountable owners."
      ],
      "known_gaps": [
        "GOV-130 is capability-owner focused, not a full RACI for all cybersecurity functions."
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
      "change": "Created the draft NIST CSF 2.0 GV.RR-02 mapping record."
    }
  ]
}
---
# GV.RR-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
