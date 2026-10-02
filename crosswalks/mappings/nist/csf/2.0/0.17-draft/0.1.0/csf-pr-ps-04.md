---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ps-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.PS-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Log records are generated and made available for continuous monitoring"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.PS-04"
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
      "rationale": "MON-100 requires collecting attributable, protected telemetry for identity, input, model, output, tool, config, and policy events for AI.",
      "conditions": [
        "Log records are generated and made available for continuous monitoring of AI systems."
      ],
      "expected_evidence": [
        "Telemetry/logging configurations and protected log availability for AI."
      ],
      "known_gaps": [
        "MON-100 does not generate logs for all enterprise systems outside AI."
      ]
    },
    {
      "esaf_control_id": "MON-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MON-150 requires preserving protected audit trails for access, config, model/data changes, privilege, agents, and incidents.",
      "conditions": [
        "Audit log records for AI are generated and preserved for monitoring and investigation."
      ],
      "expected_evidence": [
        "Protected audit-trail evidence for AI events."
      ],
      "known_gaps": [
        "MON-150 is AI audit-trail focused."
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
      "change": "Created the draft NIST CSF 2.0 PR.PS-04 mapping record."
    }
  ]
}
---
# PR.PS-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
