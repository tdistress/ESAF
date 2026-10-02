---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rc-rp-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RC.RP-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The integrity of backups and other restoration assets is verified before using them for restoration"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RC.RP-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-130 requires recovery arrangements that include verifying integrity of restoration assets before use where applicable to AI services.",
      "conditions": [
        "Integrity of backups and other restoration assets for AI is verified before using them for restoration."
      ],
      "expected_evidence": [
        "Backup/restoration integrity verification records for AI."
      ],
      "known_gaps": [
        "OPS-130 does not verify integrity of all enterprise backups outside AI recovery arrangements."
      ]
    },
    {
      "esaf_control_id": "INF-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "INF-140 requires cryptographic protection for AI backups supporting integrity verification.",
      "conditions": [
        "Cryptographic controls support integrity verification of AI restoration assets."
      ],
      "expected_evidence": [
        "Crypto/key evidence for AI backup integrity."
      ],
      "known_gaps": [
        "INF-140 provides protection mechanisms but not the recovery verification procedure alone."
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
      "change": "Created the draft NIST CSF 2.0 RC.RP-03 mapping record."
    }
  ]
}
---
# RC.RP-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
