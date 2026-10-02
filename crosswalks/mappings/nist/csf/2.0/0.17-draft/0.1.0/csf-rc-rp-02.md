---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rc-rp-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RC.RP-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Recovery actions are selected, scoped, prioritized, and performed"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RC.RP-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-130 requires selecting, scoping, prioritizing, and performing recovery actions for AI continuity and provider-failure scenarios.",
      "conditions": [
        "Recovery actions for AI are selected, scoped, prioritized, and performed."
      ],
      "expected_evidence": [
        "Recovery action plans and execution evidence for AI."
      ],
      "known_gaps": [
        "OPS-130 does not manage recovery actions for all enterprise assets outside AI."
      ]
    },
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-120 requires performing recovery actions within AI incident recovery.",
      "conditions": [
        "Incident-driven recovery actions for AI are performed."
      ],
      "expected_evidence": [
        "Incident recovery action records."
      ],
      "known_gaps": [
        "OPS-120 is incident-linked recovery."
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
      "change": "Created the draft NIST CSF 2.0 RC.RP-02 mapping record."
    }
  ]
}
---
# RC.RP-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
