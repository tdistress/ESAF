---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-4-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-4.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Post-deployment AI system monitoring plans are implemented, including consideration of AI system updates and user feedback."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-4.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "MON-120 requires monitoring production AI behavior against approved baselines and thresholds.",
      "conditions": [
        "A post-deployment monitoring plan implements MON-120 for the system."
      ],
      "expected_evidence": [
        "Production monitoring plan and baseline configuration."
      ],
      "known_gaps": [
        "MON-120 does not expressly require incorporating user feedback into the monitoring plan."
      ]
    },
    {
      "esaf_control_id": "OPS-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "OPS-100 requires approved objectives for monitoring, maintenance, support, and escalation for each production AI capability.",
      "conditions": [
        "Service objectives include post-deployment monitoring and maintenance."
      ],
      "expected_evidence": [
        "Service objectives documenting monitoring and maintenance expectations."
      ],
      "known_gaps": [
        "OPS-100 does not specify user-feedback integration mechanisms."
      ]
    },
    {
      "esaf_control_id": "OPS-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-110 requires controlled assessment, testing, approval, deployment, verification, and rollback for AI capability changes.",
      "conditions": [
        "Post-deployment updates are handled under change/release management connected to monitoring."
      ],
      "expected_evidence": [
        "Change records for post-deployment updates with verification."
      ],
      "known_gaps": [
        "OPS-110 manages updates but does not define the monitoring plan or user feedback loops."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-project-owner",
    "date": "2026-10-01"
  },
  "change_history": [
    {
      "version": "0.1.0",
      "date": "2026-10-01",
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-4.1 mapping record."
    }
  ]
}
---
# MANAGE-4.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
