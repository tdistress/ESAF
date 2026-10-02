---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rc-rp-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RC.RP-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Critical mission functions and cybersecurity risk management are considered to establish post-incident operational norms"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RC.RP-04"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-130 requires considering critical mission functions when establishing post-incident operational norms for AI recovery.",
      "conditions": [
        "Critical mission functions and AI cybersecurity risk management are considered to establish post-incident operational norms for AI."
      ],
      "expected_evidence": [
        "Post-incident operating norms and recovery objectives for AI services."
      ],
      "known_gaps": [
        "OPS-130 does not set post-incident norms for all enterprise functions outside AI."
      ]
    },
    {
      "esaf_control_id": "OPS-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-100 requires availability, security, and recovery objectives for AI services that inform post-incident norms.",
      "conditions": [
        "Service objectives inform post-incident operational norms for AI."
      ],
      "expected_evidence": [
        "Service objective records used in recovery planning."
      ],
      "known_gaps": [
        "OPS-100 does not itself declare post-incident norms."
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
      "change": "Created the draft NIST CSF 2.0 RC.RP-04 mapping record."
    }
  ]
}
---
# RC.RP-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
