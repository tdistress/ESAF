---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-sc-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.SC-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Cybersecurity supply chain risk management is integrated into cybersecurity and enterprise risk management, risk assessment, and improvement processes"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.SC-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "CMP-120 requires monitoring and enforcing third-party AI duties as part of ongoing compliance management.",
      "conditions": [
        "AI supply chain cybersecurity risk management is integrated into AI risk and improvement processes."
      ],
      "expected_evidence": [
        "Third-party monitoring results linked to AI risk and improvement records."
      ],
      "known_gaps": [
        "CMP-120 does not integrate C-SCRM into full enterprise ERM outside AI."
      ]
    },
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-100 requires AI risk methodology covering assessment and treatment that can include supplier-related AI risks.",
      "conditions": [
        "Supplier-related AI cybersecurity risks are assessed under the AI risk methodology."
      ],
      "expected_evidence": [
        "Risk assessments including third-party AI risk."
      ],
      "known_gaps": [
        "RSK-100 does not define a separate C-SCRM integration program."
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
      "change": "Created the draft NIST CSF 2.0 GV.SC-03 mapping record."
    }
  ]
}
---
# GV.SC-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
