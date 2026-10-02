---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-rm-05",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.RM-05",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Lines of communication across the organization are established for cybersecurity risks, including risks from suppliers and other third parties"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.RM-05"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "GOV-100 requires enterprise AI governance authority with accountability, decision rights, escalation, and cadence.",
      "conditions": [
        "Lines of communication for AI cybersecurity risks, including supplier-related risks, use governance escalation paths."
      ],
      "expected_evidence": [
        "Governance charter, escalation paths, and communication records."
      ],
      "known_gaps": [
        "GOV-100 does not establish all enterprise cybersecurity risk communication channels outside AI governance."
      ]
    },
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "CMP-120 requires contractual assignment, verification, monitoring, and enforcement of third-party AI security, privacy, incident, and exit duties.",
      "conditions": [
        "Supplier and third-party AI cybersecurity risks are communicated through third-party management channels."
      ],
      "expected_evidence": [
        "Third-party risk communications and monitoring records."
      ],
      "known_gaps": [
        "CMP-120 is third-party AI compliance focused rather than a general risk-communication program."
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
      "change": "Created the draft NIST CSF 2.0 GV.RM-05 mapping record."
    }
  ]
}
---
# GV.RM-05

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
