---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-cm-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.CM-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Networks and network services are monitored to find potentially adverse events"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.CM-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-100 requires collecting attributable telemetry for AI including network-relevant identity, input, tool, and policy events where applicable.",
      "conditions": [
        "Networks and network services supporting AI are monitored via AI telemetry to find potentially adverse events."
      ],
      "expected_evidence": [
        "AI telemetry covering network-relevant AI access and tool events."
      ],
      "known_gaps": [
        "MON-100 does not provide general enterprise network IDS/monitoring outside AI telemetry scope."
      ]
    },
    {
      "esaf_control_id": "MON-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-110 requires detecting and investigating AI security events including unauthorized access and abuse.",
      "conditions": [
        "Potentially adverse network-related AI security events are detected."
      ],
      "expected_evidence": [
        "Detection rules and investigation records for AI security events with network indicators."
      ],
      "known_gaps": [
        "MON-110 is AI security-event detection, not full network service monitoring."
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
      "change": "Created the draft NIST CSF 2.0 DE.CM-01 mapping record."
    }
  ]
}
---
# DE.CM-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
