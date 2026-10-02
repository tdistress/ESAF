---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-sc-09",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.SC-09",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Supply chain security practices are integrated into cybersecurity and enterprise risk management programs, and their performance is monitored throughout the technology product and service life cycle"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.SC-09"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "CMP-120 requires monitoring performance of third-party AI security and related duties.",
      "conditions": [
        "Supply chain security practices for AI are integrated into AI risk management and their performance is monitored."
      ],
      "expected_evidence": [
        "Third-party monitoring metrics and performance reviews for AI suppliers."
      ],
      "known_gaps": [
        "CMP-120 does not integrate supply-chain security into full enterprise ERM outside AI."
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
      "change": "Created the draft NIST CSF 2.0 GV.SC-09 mapping record."
    }
  ]
}
---
# GV.SC-09

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
