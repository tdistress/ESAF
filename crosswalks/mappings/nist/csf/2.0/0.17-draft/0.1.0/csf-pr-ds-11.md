---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ds-11",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.DS-11",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Backups of data are created, protected, maintained, and tested • Platform Security (PR.PS): The hardware, software (e.g., firmware, operating systems, applications), and services of physical and virtual platforms are managed consistent with the organization's risk strategy to protect their confidentiality, integrity, and availability"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.DS-11"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "INF-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "INF-140 requires approved cryptography and key management for AI backups among other protected assets.",
      "conditions": [
        "Backups of AI data are protected using approved cryptographic and key-management controls."
      ],
      "expected_evidence": [
        "Backup encryption and key-management evidence for AI data."
      ],
      "known_gaps": [
        "INF-140 does not itself require creating, maintaining, and testing backups."
      ]
    },
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-130 requires continuity and recovery arrangements for AI including restoration capabilities.",
      "conditions": [
        "Backup/restore capabilities supporting AI recovery are created, maintained, and tested as part of continuity arrangements."
      ],
      "expected_evidence": [
        "Continuity plans, backup/restore test records for AI services."
      ],
      "known_gaps": [
        "OPS-130 does not prescribe enterprise backup schedules for all data types."
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
      "change": "Created the draft NIST CSF 2.0 PR.DS-11 mapping record."
    }
  ]
}
---
# PR.DS-11

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
