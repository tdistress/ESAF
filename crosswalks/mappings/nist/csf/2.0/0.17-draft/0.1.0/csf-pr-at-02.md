---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-at-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.AT-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Individuals in specialized roles are provided with awareness and training so that they possess the knowledge and skills to perform relevant tasks with cybersecurity risks in mind • Data Security (PR.DS): Data are managed consistent with the organization's risk strategy to protect the confidentiality, integrity, and availability of information"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.AT-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "EDU-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "EDU-110 requires defining, assessing, and evidencing role-based AI competency for design through audit and use roles.",
      "conditions": [
        "Individuals in specialized AI roles receive awareness and training for relevant cybersecurity risk management tasks."
      ],
      "expected_evidence": [
        "Role-based curricula, competency assessments, and completion records."
      ],
      "known_gaps": [
        "EDU-110 does not train all specialized enterprise cybersecurity roles outside AI."
      ]
    },
    {
      "esaf_control_id": "EDU-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "EDU-130 requires current secure AI engineering training for builders and operators of AI systems.",
      "conditions": [
        "Specialized engineering/operator roles receive secure AI training relevant to cybersecurity."
      ],
      "expected_evidence": [
        "Secure AI engineering training records."
      ],
      "known_gaps": [
        "EDU-130 is AI engineering focused."
      ]
    },
    {
      "esaf_control_id": "EDU-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "EDU-140 requires educating executives, owners, acceptors, and auditors on AI duties, risk, evidence, and decision rights.",
      "conditions": [
        "Specialized governance and assurance roles receive AI risk and cybersecurity-relevant duty training."
      ],
      "expected_evidence": [
        "Executive/owner/auditor education records."
      ],
      "known_gaps": [
        "EDU-140 does not cover all specialized cyber roles (e.g., SOC analysts) outside AI duties."
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
      "change": "Created the draft NIST CSF 2.0 PR.AT-02 mapping record."
    }
  ]
}
---
# PR.AT-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
