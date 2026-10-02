---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-cm-09",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.CM-09",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events • Adverse Event Analysis (DE.AE): Anomalies, indicators of compromise, and other potentially adverse events are analyzed to characterize the events and detect cybersecurity incidents"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.CM-09"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "MON-100 requires collecting telemetry for AI compute-relevant identity, input, model, output, tool, config, and policy events.",
      "conditions": [
        "Computing hardware and software, runtime environments, and their data for AI are monitored to find potentially adverse events via AI telemetry."
      ],
      "expected_evidence": [
        "AI telemetry configurations covering runtimes, models, and data-path events."
      ],
      "known_gaps": [
        "MON-100 does not monitor all enterprise compute/hardware/software outside AI."
      ]
    },
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-120 requires monitoring AI behavior and drift for in-scope production AI capabilities.",
      "conditions": [
        "Runtime behavior of AI software/environments is monitored for adverse conditions."
      ],
      "expected_evidence": [
        "Behavior/drift monitoring configurations and alerts."
      ],
      "known_gaps": [
        "MON-120 is behavior/drift focused rather than full host/hardware monitoring."
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
      "change": "Created the draft NIST CSF 2.0 DE.CM-09 mapping record."
    }
  ]
}
---
# DE.CM-09

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
