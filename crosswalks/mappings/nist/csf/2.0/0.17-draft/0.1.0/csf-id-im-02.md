---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-im-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.IM-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Improvements are identified from security tests and exercises, including those done in coordination with suppliers and relevant third parties"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.IM-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AUD-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "AUD-100 requires a risk-based assessment program for AI management system, capabilities, and controls.",
      "conditions": [
        "Improvements are identified from security tests and exercises within the AI assessment program, including those coordinated with suppliers when in scope."
      ],
      "expected_evidence": [
        "Assessment/test reports and resulting improvement actions."
      ],
      "known_gaps": [
        "AUD-100 does not mandate enterprise-wide red-team exercises beyond AI assessment scope."
      ]
    },
    {
      "esaf_control_id": "OPS-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-130 requires defining, implementing, and testing continuity, fallback, safe-state, recovery, and provider-failure arrangements for AI.",
      "conditions": [
        "Improvements are identified from continuity and recovery tests involving AI providers when executed."
      ],
      "expected_evidence": [
        "Continuity/recovery test results and improvement actions."
      ],
      "known_gaps": [
        "OPS-130 testing is continuity-focused, not a full security exercise program."
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
      "change": "Created the draft NIST CSF 2.0 ID.IM-02 mapping record."
    }
  ]
}
---
# ID.IM-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
