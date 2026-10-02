---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-sc-10",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.SC-10",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Cybersecurity supply chain risk management plans include provisions for activities that occur after the conclusion of a partnership or service agreement IDENTIFY (ID): The organization's current cybersecurity risks are understood • Asset Management (ID.AM): Assets (e.g., data, hardware, software, systems, facilities, services, people) that enable the organization to achieve business purposes are identified and managed consistent with their relative importance to organizational objectives and the organization's risk strategy"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.SC-10"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "CMP-120 requires exit duties in AI third-party agreements.",
      "conditions": [
        "AI supply chain risk management plans include provisions for activities after partnership or service conclusion."
      ],
      "expected_evidence": [
        "Exit/transition clauses and post-termination activity records for AI suppliers."
      ],
      "known_gaps": [
        "CMP-120 does not define post-relationship activities for all enterprise suppliers."
      ]
    },
    {
      "esaf_control_id": "API-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "API-150 requires documenting and testing interfaces and exit criteria to replace or isolate material AI providers.",
      "conditions": [
        "Exit criteria and replacement planning exist for material AI providers."
      ],
      "expected_evidence": [
        "Exit criteria documentation and isolation/replacement test records."
      ],
      "known_gaps": [
        "API-150 is integration-exit focused, not a full post-partnership C-SCRM plan."
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
      "change": "Created the draft NIST CSF 2.0 GV.SC-10 mapping record."
    }
  ]
}
---
# GV.SC-10

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
