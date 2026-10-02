---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-am-08",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.AM-08",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Systems, hardware, software, services, and data are managed throughout their life cycles • Risk Assessment (ID.RA): The cybersecurity risk to the organization, assets, and individuals is understood by the organization"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.AM-08"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "GOV-120 requires lifecycle-state oversight including retirement for AI capabilities.",
      "conditions": [
        "AI systems, services, and related assets are managed throughout their life cycles via portfolio oversight."
      ],
      "expected_evidence": [
        "Portfolio lifecycle-state records and retirement decisions."
      ],
      "known_gaps": [
        "GOV-120 does not lifecycle-manage non-AI hardware/software enterprise-wide."
      ]
    },
    {
      "esaf_control_id": "ARC-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "ARC-150 requires governing adoption, currency, deprecation, and retirement of AI technologies and architecture components.",
      "conditions": [
        "AI technologies and architecture components are managed across adoption through retirement."
      ],
      "expected_evidence": [
        "Technology adoption/deprecation/retirement records for AI components."
      ],
      "known_gaps": [
        "ARC-150 is AI technology/architecture focused."
      ]
    },
    {
      "esaf_control_id": "OPS-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-150 requires controlled retirement of AI capabilities including data, model, access, and residual-risk handling.",
      "conditions": [
        "End-of-life management for AI capabilities is controlled."
      ],
      "expected_evidence": [
        "Retirement plans and execution records."
      ],
      "known_gaps": [
        "OPS-150 covers retirement, not the full earlier lifecycle phases alone."
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
      "change": "Created the draft NIST CSF 2.0 ID.AM-08 mapping record."
    }
  ]
}
---
# ID.AM-08

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
