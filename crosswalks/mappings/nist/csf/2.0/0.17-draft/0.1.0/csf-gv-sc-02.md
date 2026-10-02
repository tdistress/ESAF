---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-sc-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.SC-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Cybersecurity roles and responsibilities for suppliers, customers, and partners are established, communicated, and coordinated internally and externally"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.SC-02"
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
      "rationale": "CMP-120 requires establishing and coordinating third-party AI security, privacy, incident, and exit duties in contracts and monitoring.",
      "conditions": [
        "Cybersecurity roles and responsibilities for AI suppliers and partners are established, communicated, and coordinated."
      ],
      "expected_evidence": [
        "Contractual role clauses and coordination records with AI suppliers/partners."
      ],
      "known_gaps": [
        "CMP-120 does not define customer-facing cybersecurity roles outside AI supplier relationships."
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
      "change": "Created the draft NIST CSF 2.0 GV.SC-02 mapping record."
    }
  ]
}
---
# GV.SC-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
