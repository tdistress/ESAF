---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-at-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.AT-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.AT-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "EDU-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "EDU-100 requires providing and refreshing baseline AI literacy covering limits, safe use, data protection, escalation, and policy.",
      "conditions": [
        "Personnel are provided awareness and training so they can perform general AI-related tasks with cybersecurity risk implications."
      ],
      "expected_evidence": [
        "Baseline AI literacy curricula and completion records."
      ],
      "known_gaps": [
        "EDU-100 is AI literacy and does not provide enterprise-wide general cybersecurity awareness for all personnel roles."
      ]
    },
    {
      "esaf_control_id": "EDU-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "EDU-120 requires educating users on approved services, acceptable use, data boundaries, verification, and incident reporting.",
      "conditions": [
        "Users receive awareness enabling cybersecurity-relevant safe use of AI services."
      ],
      "expected_evidence": [
        "User education materials and completion evidence."
      ],
      "known_gaps": [
        "EDU-120 does not replace organization-wide cyber awareness training."
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
      "change": "Created the draft NIST CSF 2.0 PR.AT-01 mapping record."
    }
  ]
}
---
# PR.AT-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
