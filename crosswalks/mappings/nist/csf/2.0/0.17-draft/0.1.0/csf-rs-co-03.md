---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-co-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.CO-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Information is shared with designated internal and external stakeholders • Incident Mitigation (RS.MI): Activities are performed to prevent expansion of an event and mitigate its effects"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.CO-03"
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
      "rationale": "OPS-120 requires sharing information with designated internal and external stakeholders during AI incident response.",
      "conditions": [
        "Information is shared with designated internal and external stakeholders for AI incidents."
      ],
      "expected_evidence": [
        "Incident information-sharing records."
      ],
      "known_gaps": [
        "OPS-120 does not define sharing for all enterprise incident types outside AI."
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
      "change": "Created the draft NIST CSF 2.0 RS.CO-03 mapping record."
    }
  ]
}
---
# RS.CO-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
