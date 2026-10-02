---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-cm-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.CM-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Personnel activity and technology usage are monitored to find potentially adverse events"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.CM-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-100 requires telemetry for identity, input, model, output, tool, config, and policy events enabling monitoring of personnel activity and technology usage for AI.",
      "conditions": [
        "Personnel activity and technology usage related to AI are monitored to find potentially adverse events."
      ],
      "expected_evidence": [
        "AI telemetry and monitoring views covering user/service activity."
      ],
      "known_gaps": [
        "MON-100 does not monitor all enterprise personnel activity and technology usage outside AI."
      ]
    },
    {
      "esaf_control_id": "MON-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-110 requires detecting AI security events such as unauthorized access, prompt/context attacks, exposure, and abuse.",
      "conditions": [
        "Adverse personnel/technology-usage events affecting AI security are detected."
      ],
      "expected_evidence": [
        "Detection and investigation records for AI security events."
      ],
      "known_gaps": [
        "MON-110 does not cover general insider-threat monitoring outside AI."
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
      "change": "Created the draft NIST CSF 2.0 DE.CM-03 mapping record."
    }
  ]
}
---
# DE.CM-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
