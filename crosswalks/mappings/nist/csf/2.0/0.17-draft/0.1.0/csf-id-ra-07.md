---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-ra-07",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.RA-07",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Changes and exceptions are managed, assessed for risk impact, recorded, and tracked"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.RA-07"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-140 requires defining material-change triggers and reassessing, revalidating, and reauthorizing before material change.",
      "conditions": [
        "Changes and exceptions affecting AI risk are managed, assessed for risk impact, recorded, and tracked."
      ],
      "expected_evidence": [
        "Material-change reviews, reassessment records, and related exception links."
      ],
      "known_gaps": [
        "RSK-140 is material-change focused for AI and does not manage all enterprise change tickets."
      ]
    },
    {
      "esaf_control_id": "GOV-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "GOV-140 requires authorizing time-bounded exceptions with risk, compensating measures, monitoring, and expiry.",
      "conditions": [
        "Exceptions are assessed for risk impact and tracked to expiry."
      ],
      "expected_evidence": [
        "Exception authorizations with risk and compensating measures."
      ],
      "known_gaps": [
        "GOV-140 does not assess routine non-exception changes."
      ]
    },
    {
      "esaf_control_id": "OPS-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-110 requires classifying, assessing, testing, approving, deploying, verifying, and rolling back AI changes by impact.",
      "conditions": [
        "AI operational changes are assessed for risk impact before deployment."
      ],
      "expected_evidence": [
        "Change records with impact classification and approvals."
      ],
      "known_gaps": [
        "OPS-110 is AI change management, not enterprise CAB for all changes."
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
      "change": "Created the draft NIST CSF 2.0 ID.RA-07 mapping record."
    }
  ]
}
---
# ID.RA-07

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
