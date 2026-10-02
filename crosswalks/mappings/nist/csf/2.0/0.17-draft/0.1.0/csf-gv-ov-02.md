---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-ov-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.OV-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The cybersecurity risk management strategy is reviewed and adjusted to ensure coverage of organizational requirements and risks"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.OV-02"
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
      "rationale": "AUD-140 requires executive review that can identify coverage gaps against organizational requirements and risks for AI.",
      "conditions": [
        "AI cybersecurity risk management strategy is reviewed and adjusted for coverage of organizational requirements and risks within AI scope."
      ],
      "expected_evidence": [
        "Management-review findings and strategy adjustment records."
      ],
      "known_gaps": [
        "AUD-140 does not review enterprise cybersecurity strategy outside AI."
      ]
    },
    {
      "esaf_control_id": "GOV-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-120 requires periodic AI portfolio review of ownership, risk, incidents, dependencies, cost, and retirement.",
      "conditions": [
        "Portfolio review informs whether AI risk-management coverage remains adequate."
      ],
      "expected_evidence": [
        "Portfolio review records and resulting adjustments."
      ],
      "known_gaps": [
        "GOV-120 is portfolio oversight, not a full strategy coverage audit."
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
      "change": "Created the draft NIST CSF 2.0 GV.OV-02 mapping record."
    }
  ]
}
---
# GV.OV-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
