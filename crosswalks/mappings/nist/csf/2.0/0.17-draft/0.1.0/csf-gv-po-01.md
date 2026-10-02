---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-po-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.PO-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Policy for managing cybersecurity risks is established based on organizational context, cybersecurity strategy, and priorities and is communicated and enforced"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.PO-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "GOV-110 requires an approved enterprise AI policy set defining mandatory requirements for governing, protecting, and utilizing in-scope AI capabilities, including scope, acceptable use, lifecycle, risk, exceptions, and enforcement.",
      "conditions": [
        "Policy for managing AI cybersecurity risks is established from organizational context, strategy, and priorities and communicated as part of the AI policy set."
      ],
      "expected_evidence": [
        "Approved AI policy set, acknowledgements, and communication records."
      ],
      "known_gaps": [
        "GOV-110 is AI policy and does not establish the full enterprise cybersecurity policy suite."
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
      "change": "Created the draft NIST CSF 2.0 GV.PO-01 mapping record."
    }
  ]
}
---
# GV.PO-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
