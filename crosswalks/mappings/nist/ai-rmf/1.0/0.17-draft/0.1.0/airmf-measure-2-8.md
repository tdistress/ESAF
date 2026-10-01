---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-8",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.8",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Risks associated with transparency and accountability identified during MAP are examined and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.8"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MOD-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MOD-120 requires validation against explainability criteria among approved trustworthiness criteria.",
      "conditions": [
        "Explainability validation is treated as partial examination of transparency-related risk."
      ],
      "expected_evidence": [
        "Model validation records covering explainability."
      ],
      "known_gaps": [
        "MOD-120 explainability does not expressly examine accountability risks or broader transparency risk."
      ]
    },
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-130 requires assignment of accountable owners with documented authority for purpose, outcomes, risk, operation, and retirement.",
      "conditions": [
        "Documented accountability ownership is examined as part of accountability risk context."
      ],
      "expected_evidence": [
        "Capability ownership records establishing accountability."
      ],
      "known_gaps": [
        "GOV-130 assigns accountability; it does not examine transparency/accountability risks as a measurement activity."
      ]
    },
    {
      "esaf_control_id": "MON-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "MON-150 requires preserving protected attributable audit trails for material AI access, approvals, configuration, model and data changes, policy decisions, privileged activity, agent actions, incidents, and governance decisions.",
      "conditions": [
        "Audit trails are used as evidence supporting accountability examination."
      ],
      "expected_evidence": [
        "Preserved AI audit trails for material decisions and actions."
      ],
      "known_gaps": [
        "MON-150 preserves trails; it does not itself examine transparency and accountability risks."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.8 mapping record."
    }
  ]
}
---
# MEASURE-2.8

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
