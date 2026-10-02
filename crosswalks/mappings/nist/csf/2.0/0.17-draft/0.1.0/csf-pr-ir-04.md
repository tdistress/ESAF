---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ir-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.IR-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Adequate resource capacity to ensure availability is maintained DETECT (DE): Possible cybersecurity attacks and compromises are found and analyzed • Continuous Monitoring (DE.CM): Assets are monitored to find anomalies, indicators of compromise, and other potentially adverse events"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.IR-04"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "INF-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "INF-150 requires enforcing capacity, quota, isolation, and shutdown to prevent exhaustion and harmful contention for AI infrastructure.",
      "conditions": [
        "Adequate resource capacity to ensure AI availability is maintained through capacity and quota controls."
      ],
      "expected_evidence": [
        "Capacity/quota configurations and availability evidence for AI infrastructure."
      ],
      "known_gaps": [
        "INF-150 does not manage capacity for all enterprise services outside AI."
      ]
    },
    {
      "esaf_control_id": "OPS-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-100 requires service owner and objectives for availability, security, recovery, monitoring, and escalation for AI services.",
      "conditions": [
        "Availability objectives drive capacity management for AI services."
      ],
      "expected_evidence": [
        "Service objectives and capacity-related operating records for AI."
      ],
      "known_gaps": [
        "OPS-100 does not itself provision capacity."
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
      "change": "Created the draft NIST CSF 2.0 PR.IR-04 mapping record."
    }
  ]
}
---
# PR.IR-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
