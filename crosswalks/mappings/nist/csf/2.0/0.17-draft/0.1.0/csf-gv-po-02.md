---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-po-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.PO-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Policy for managing cybersecurity risks is reviewed, updated, communicated, and enforced to reflect changes in requirements, threats, technology, and organizational mission • Oversight (GV.OV): Results of organization-wide cybersecurity risk management activities and performance are used to inform, improve, and adjust the risk management strategy"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.PO-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "GOV-110 requires maintaining an approved enterprise AI policy set with enforcement and exception handling.",
      "conditions": [
        "AI cybersecurity risk policy is reviewed, updated, communicated, and enforced to reflect changes in requirements, threats, technology, and mission."
      ],
      "expected_evidence": [
        "Policy revision history, communications, and enforcement/exception records."
      ],
      "known_gaps": [
        "GOV-110 does not cover non-AI cybersecurity policy maintenance."
      ]
    },
    {
      "esaf_control_id": "GOV-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-140 requires authorizing time-bounded exceptions with risk, compensating measures, monitoring, and expiry.",
      "conditions": [
        "Policy exceptions for AI cybersecurity requirements are managed under GOV-140."
      ],
      "expected_evidence": [
        "Exception records with compensating measures and expiry."
      ],
      "known_gaps": [
        "GOV-140 does not itself perform periodic policy content review."
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
      "change": "Created the draft NIST CSF 2.0 GV.PO-02 mapping record."
    }
  ]
}
---
# GV.PO-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
