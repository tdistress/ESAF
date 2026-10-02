---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-oc-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.OC-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Critical objectives, capabilities, and services that external stakeholders depend on or expect from the organization are understood and communicated"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.OC-04"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-130 requires accountable business and technical/service owners with documented authority for purpose and outcomes of each in-scope AI capability.",
      "conditions": [
        "Critical objectives and services that external stakeholders depend on are reflected in documented AI capability purposes and outcomes where AI provides those services."
      ],
      "expected_evidence": [
        "Capability ownership records stating purpose and outcomes for stakeholder-facing AI services."
      ],
      "known_gaps": [
        "GOV-130 does not maintain an enterprise catalog of all critical services independent of AI capabilities."
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
      "change": "Created the draft NIST CSF 2.0 GV.OC-04 mapping record."
    }
  ]
}
---
# GV.OC-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
