---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-rm-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.RM-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Risk appetite and risk tolerance statements are established, communicated, and maintained"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.RM-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "RSK-100 requires rating criteria, residual risk, acceptance, and escalation in the approved AI risk methodology.",
      "conditions": [
        "Acceptance thresholds and rating criteria are treated as the AI expression of risk appetite and tolerance."
      ],
      "expected_evidence": [
        "Approved methodology sections on acceptance thresholds and escalation."
      ],
      "known_gaps": [
        "RSK-100 does not expressly require standalone enterprise risk-appetite and risk-tolerance statements for all cybersecurity domains."
      ]
    },
    {
      "esaf_control_id": "STR-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "STR-100 requires AI objectives and priorities that trace to organizational strategy and risk appetite.",
      "conditions": [
        "Documented risk appetite in AI strategy is communicated and maintained as an input to risk decisions."
      ],
      "expected_evidence": [
        "Approved AI strategy referencing risk appetite."
      ],
      "known_gaps": [
        "STR-100 risk appetite is strategic and may not specify operational cybersecurity tolerance thresholds."
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
      "change": "Created the draft NIST CSF 2.0 GV.RM-02 mapping record."
    }
  ]
}
---
# GV.RM-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
