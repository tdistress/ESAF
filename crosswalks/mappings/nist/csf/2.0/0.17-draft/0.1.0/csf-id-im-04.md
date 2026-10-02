---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-im-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.IM-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incident response plans and other cybersecurity plans that affect operations are established, communicated, maintained, and improved PROTECT (PR): Safeguards to manage the organization's cybersecurity risks are used • Identity Management, Authentication, and Access Control (PR.AA): Access to physical and logical assets is limited to authorized users, services, and hardware and managed commensurate with the assessed risk of unauthorized access"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.IM-04"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-120 requires preparing for and running AI incident response integrated with enterprise incident management.",
      "conditions": [
        "Incident response plans affecting AI operations are established, communicated, maintained, and improved."
      ],
      "expected_evidence": [
        "AI incident response plans, communications, and improvement records."
      ],
      "known_gaps": [
        "OPS-120 does not establish all enterprise cybersecurity plans outside AI incident management."
      ]
    },
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-130 requires continuity and recovery arrangements for AI that are maintained and tested.",
      "conditions": [
        "Recovery and continuity plans affecting AI operations are established and maintained."
      ],
      "expected_evidence": [
        "Continuity/recovery plans and maintenance records for AI."
      ],
      "known_gaps": [
        "OPS-130 does not cover every cybersecurity plan type beyond continuity/recovery."
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
      "change": "Created the draft NIST CSF 2.0 ID.IM-04 mapping record."
    }
  ]
}
---
# ID.IM-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
