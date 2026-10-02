---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-ov-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.OV-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Organizational cybersecurity risk management performance is evaluated and reviewed for adjustments needed • Cybersecurity Supply Chain Risk Management (GV.SC): Cyber supply chain risk management processes are identified, established, managed, monitored, and improved by organizational stakeholders"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.OV-03"
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
      "rationale": "AUD-140 requires evaluating AI management-system performance including risk and controls for adjustments needed.",
      "conditions": [
        "Organizational AI cybersecurity risk management performance is evaluated and reviewed for adjustments."
      ],
      "expected_evidence": [
        "Performance metrics or assurance reports in management review and resulting actions."
      ],
      "known_gaps": [
        "AUD-140 does not define enterprise cybersecurity performance KPIs outside AI."
      ]
    },
    {
      "esaf_control_id": "AUD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AUD-100 requires a risk-based assessment program for the AI management system, capabilities, and controls.",
      "conditions": [
        "Assessment results inform evaluation of AI cybersecurity risk management performance."
      ],
      "expected_evidence": [
        "Assessment program plans and reports."
      ],
      "known_gaps": [
        "AUD-100 does not itself set strategy performance targets."
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
      "change": "Created the draft NIST CSF 2.0 GV.OV-03 mapping record."
    }
  ]
}
---
# GV.OV-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
