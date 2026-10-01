---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-1-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-1.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Trustworthy-AI characteristics are integrated into organizational policies, processes, procedures, and practices."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-1.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "GOV-110 requires an approved enterprise AI policy that defines scope, principles, acceptable and prohibited use, lifecycle obligations, accountability, risk expectations, exception handling, enforcement, and review requirements.",
      "conditions": [
        "Enterprise AI policy principles are treated as the organization's expression of trustworthy-AI characteristics."
      ],
      "expected_evidence": [
        "Approved enterprise AI policy stating principles and lifecycle obligations."
      ],
      "known_gaps": [
        "GOV-110 does not enumerate NIST trustworthy-AI characteristics or require their explicit integration into every process and practice."
      ]
    },
    {
      "esaf_control_id": "GOV-100",
      "esaf_control_version": "0.1.0",
      "relationship": "prerequisite",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-100 requires executive leadership to establish enterprise authority with documented accountability and decision rights for governing in-scope AI capabilities, which is a prerequisite for policy-governed integration of trustworthy-AI expectations.",
      "conditions": [
        "An enterprise AI governance authority exists and owns policy approval."
      ],
      "expected_evidence": [
        "Governance-authority charter showing policy and principle decision rights."
      ],
      "known_gaps": [
        "GOV-100 alone does not integrate trustworthy-AI characteristics into operational practices."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-project-owner",
    "date": "2026-10-01"
  },
  "change_history": [
    {
      "version": "0.1.0",
      "date": "2026-10-01",
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-1.2 mapping record."
    }
  ]
}
---
# GOVERN-1.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
