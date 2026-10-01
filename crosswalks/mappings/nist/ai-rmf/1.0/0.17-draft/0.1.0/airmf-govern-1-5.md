---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-1-5",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-1.5",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Ongoing monitoring and periodic review of the AI risk-management process are planned, with roles and review frequency defined."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-1.5"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-100 requires the AI risk methodology to include monitoring, reassessment, and escalation.",
      "conditions": [
        "Monitoring and reassessment cadence is defined in the approved methodology."
      ],
      "expected_evidence": [
        "Methodology clauses defining monitoring and reassessment frequency and escalation paths."
      ],
      "known_gaps": [
        "RSK-100 does not alone assign all organizational roles for periodic review of the process itself."
      ]
    },
    {
      "esaf_control_id": "AUD-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "AUD-140 requires executive leadership to review the AI management system at planned intervals using current information on risk, control effectiveness, assessments, and improvement needs and to record decisions.",
      "conditions": [
        "Management review includes the AI risk-management process and outcomes."
      ],
      "expected_evidence": [
        "Management-review records showing planned interval, risk inputs, and decisions."
      ],
      "known_gaps": [
        "AUD-140 is enterprise management review, not a dedicated RMF-process audit schedule."
      ]
    },
    {
      "esaf_control_id": "GOV-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-100 requires documented accountability, membership, decision rights, escalation paths, and meeting cadence for the enterprise AI governance authority.",
      "conditions": [
        "Governance authority owns periodic review of AI risk management."
      ],
      "expected_evidence": [
        "Governance charter defining meeting cadence and risk-review decision rights."
      ],
      "known_gaps": [
        "GOV-100 does not prescribe risk-methodology monitoring metrics."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-1.5 mapping record."
    }
  ]
}
---
# GOVERN-1.5

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
