---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-ae-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.AE-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The estimated impact and scope of adverse events are understood"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.AE-04"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-140 requires prioritizing and triaging AI alerts, which includes understanding estimated impact and scope.",
      "conditions": [
        "Estimated impact and scope of adverse AI events are understood during triage."
      ],
      "expected_evidence": [
        "Triage records documenting estimated impact/scope of AI adverse events."
      ],
      "known_gaps": [
        "MON-140 does not estimate impact/scope for all enterprise adverse events."
      ]
    },
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-120 requires AI incident management including assessment of incidents once declared.",
      "conditions": [
        "Impact and scope are understood when adverse AI events become incidents."
      ],
      "expected_evidence": [
        "Incident assessment records documenting impact/scope."
      ],
      "known_gaps": [
        "OPS-120 applies after incident criteria are met."
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
      "change": "Created the draft NIST CSF 2.0 DE.AE-04 mapping record."
    }
  ]
}
---
# DE.AE-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
