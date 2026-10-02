---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-ae-08",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.AE-08",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incidents are declared when adverse events meet the defined incident criteria RESPOND (RS): Actions regarding a detected cybersecurity incident are taken • Incident Management (RS.MA): Responses to detected cybersecurity incidents are managed"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.AE-08"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "OPS-120 requires preparing for and running AI incident lifecycle including declaration when adverse events meet defined incident criteria, integrated with enterprise incident management.",
      "conditions": [
        "Incidents are declared when adverse AI events meet defined incident criteria."
      ],
      "expected_evidence": [
        "Incident declaration criteria and declaration records for AI events."
      ],
      "known_gaps": [
        "OPS-120 does not define incident criteria for all enterprise cybersecurity events outside AI."
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
      "change": "Created the draft NIST CSF 2.0 DE.AE-08 mapping record."
    }
  ]
}
---
# DE.AE-08

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
