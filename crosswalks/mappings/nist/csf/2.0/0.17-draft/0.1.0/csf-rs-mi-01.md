---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-mi-01",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.MI-01",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incidents are contained"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.MI-01"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-120 requires containing AI incidents as part of the incident lifecycle.",
      "conditions": [
        "AI incidents are contained."
      ],
      "expected_evidence": [
        "Containment actions and evidence in incident records."
      ],
      "known_gaps": [
        "OPS-120 containment is AI-incident scoped."
      ]
    },
    {
      "esaf_control_id": "AGT-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AGT-150 requires pause, restrict, isolate, and terminate capabilities for agents.",
      "conditions": [
        "Agent-related incidents can be contained via pause/restrict/isolate/terminate."
      ],
      "expected_evidence": [
        "Agent containment action records."
      ],
      "known_gaps": [
        "AGT-150 covers agents only."
      ]
    },
    {
      "esaf_control_id": "MON-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-140 requires containing AI security, behavior, ops, and compliance alerts when appropriate.",
      "conditions": [
        "Containment begins at alert handling for AI adverse events."
      ],
      "expected_evidence": [
        "Containment actions on AI alerts."
      ],
      "known_gaps": [
        "MON-140 containment is alert-level and may precede formal incident containment."
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
      "change": "Created the draft NIST CSF 2.0 RS.MI-01 mapping record."
    }
  ]
}
---
# RS.MI-01

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
