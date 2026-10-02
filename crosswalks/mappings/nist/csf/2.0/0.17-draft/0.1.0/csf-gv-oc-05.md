---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-oc-05",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.OC-05",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Outcomes, capabilities, and services that the organization depends on are understood and communicated • Risk Management Strategy (GV.RM): The organization's priorities, constraints, risk tolerance and appetite statements, and assumptions are established, communicated, and used to support operational risk decisions"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.OC-05"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "ARC-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "ARC-140 requires documenting, validating, and monitoring shared-responsibility boundaries with platforms, providers, and suppliers supporting AI capabilities.",
      "conditions": [
        "Dependencies on external outcomes, capabilities, and services for AI are recorded in shared-responsibility and dependency documentation."
      ],
      "expected_evidence": [
        "Shared-responsibility boundary documents and dependency inventories for AI platforms and suppliers."
      ],
      "known_gaps": [
        "ARC-140 does not inventory every organizational dependency outside AI delivery."
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
      "change": "Created the draft NIST CSF 2.0 GV.OC-05 mapping record."
    }
  ]
}
---
# GV.OC-05

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
