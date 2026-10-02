---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-cm-06",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.CM-06",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "External service provider activities and services are monitored to find potentially adverse events"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.CM-06"
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
      "rationale": "CMP-120 requires monitoring third-party AI security, privacy, incident, and exit duties.",
      "conditions": [
        "External AI service provider activities and services are monitored to find potentially adverse events."
      ],
      "expected_evidence": [
        "Third-party AI monitoring records and adverse-event findings."
      ],
      "known_gaps": [
        "CMP-120 does not monitor all external service providers enterprise-wide."
      ]
    },
    {
      "esaf_control_id": "MON-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-110 requires detecting AI security events that may originate from or involve external providers.",
      "conditions": [
        "Adverse events involving external AI providers are detected when visible in AI telemetry."
      ],
      "expected_evidence": [
        "Detection records implicating external AI provider activity."
      ],
      "known_gaps": [
        "MON-110 depends on telemetry visibility into provider activity."
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
      "change": "Created the draft NIST CSF 2.0 DE.CM-06 mapping record."
    }
  ]
}
---
# DE.CM-06

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
