---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-ae-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.AE-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Potentially adverse events are analyzed to better understand associated activities"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.AE-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-110 requires detecting and investigating AI security events to better understand associated activities.",
      "conditions": [
        "Potentially adverse AI events are analyzed to understand associated activities."
      ],
      "expected_evidence": [
        "Investigation records analyzing adverse AI security events."
      ],
      "known_gaps": [
        "MON-110 analysis is AI-security focused, not enterprise-wide adverse-event analysis."
      ]
    },
    {
      "esaf_control_id": "MON-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-140 requires owning, prioritizing, triaging, escalating, and containing AI security, behavior, ops, and compliance alerts.",
      "conditions": [
        "Triage analysis of adverse AI events improves understanding of associated activities."
      ],
      "expected_evidence": [
        "Triage and escalation records for AI alerts."
      ],
      "known_gaps": [
        "MON-140 is triage/containment oriented rather than deep forensic analysis alone."
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
      "change": "Created the draft NIST CSF 2.0 DE.AE-02 mapping record."
    }
  ]
}
---
# DE.AE-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
