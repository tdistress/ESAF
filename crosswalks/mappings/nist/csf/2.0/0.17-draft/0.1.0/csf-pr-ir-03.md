---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ir-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.IR-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Mechanisms are implemented to achieve resilience requirements in normal and adverse situations"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.IR-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "ARC-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "ARC-130 requires designing for foreseeable failures with isolation, degradation, safe state, fallback, and recovery.",
      "conditions": [
        "Mechanisms are implemented to achieve resilience requirements for AI in normal and adverse situations."
      ],
      "expected_evidence": [
        "Resilience design documentation and test evidence for AI systems."
      ],
      "known_gaps": [
        "ARC-130 is AI architecture resilience, not enterprise facility/tech resilience broadly."
      ]
    },
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-130 requires continuity, fallback, safe-state, recovery, and provider-failure arrangements for AI.",
      "conditions": [
        "Operational resilience mechanisms for AI are implemented and tested."
      ],
      "expected_evidence": [
        "Continuity/fallback/recovery arrangements and tests for AI."
      ],
      "known_gaps": [
        "OPS-130 does not implement resilience for all enterprise technology assets."
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
      "change": "Created the draft NIST CSF 2.0 PR.IR-03 mapping record."
    }
  ]
}
---
# PR.IR-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
