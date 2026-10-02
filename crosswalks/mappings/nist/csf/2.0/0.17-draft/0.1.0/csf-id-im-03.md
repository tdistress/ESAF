---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-im-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.IM-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Improvements are identified from execution of operational processes, procedures, and activities"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.IM-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AUD-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "AUD-140 requires management review including incidents, controls, and improvement for the AI management system.",
      "conditions": [
        "Improvements are identified from execution of AI operational processes, procedures, and activities as reviewed by management."
      ],
      "expected_evidence": [
        "Management-review actions arising from operational performance and incidents."
      ],
      "known_gaps": [
        "AUD-140 does not capture every operational lesson outside management review inputs."
      ]
    },
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-120 requires AI incident lifecycle including post-incident learning integrated with enterprise incident management.",
      "conditions": [
        "Improvements are identified from AI incident operational execution."
      ],
      "expected_evidence": [
        "Post-incident review actions."
      ],
      "known_gaps": [
        "OPS-120 is incident-centric rather than all operational processes."
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
      "change": "Created the draft NIST CSF 2.0 ID.IM-03 mapping record."
    }
  ]
}
---
# ID.IM-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
