---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-ra-05",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.RA-05",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent risk and inform risk response prioritization"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.RA-05"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-100 requires using methodology outputs to understand inherent risk and inform risk response prioritization.",
      "conditions": [
        "Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent AI risk and prioritize responses."
      ],
      "expected_evidence": [
        "Inherent-risk ratings and prioritization records from AI assessments."
      ],
      "known_gaps": [
        "RSK-100 does not compute inherent risk for non-AI enterprise assets."
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
      "change": "Created the draft NIST CSF 2.0 ID.RA-05 mapping record."
    }
  ]
}
---
# ID.RA-05

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
