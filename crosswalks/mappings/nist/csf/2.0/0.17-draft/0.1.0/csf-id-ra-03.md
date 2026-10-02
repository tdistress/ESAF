---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-ra-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.RA-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Internal and external threats to the organization are identified and recorded"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.RA-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "APP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "APP-100 requires designing AI applications with documented threat and misuse cases.",
      "conditions": [
        "Internal and external threats to AI applications are identified and recorded in design threat models."
      ],
      "expected_evidence": [
        "Threat and misuse-case documentation for AI applications."
      ],
      "known_gaps": [
        "APP-100 does not identify all organizational threats outside AI applications."
      ]
    },
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-100 requires AI risk methodology that includes identifying threats as part of assessment.",
      "conditions": [
        "Threat identification is recorded in AI risk assessments."
      ],
      "expected_evidence": [
        "AI risk assessments documenting identified threats."
      ],
      "known_gaps": [
        "RSK-100 does not create an enterprise threat catalog."
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
      "change": "Created the draft NIST CSF 2.0 ID.RA-03 mapping record."
    }
  ]
}
---
# ID.RA-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
