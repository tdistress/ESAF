---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-2-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-2.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "AI system knowledge limits, human utilization and oversight of outputs, and assumptions about limitations are documented and used to inform development and deployment."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-2.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MOD-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-110 requires establishing and verifying known limitations, provenance, usage rights, and related attributes for each model before approved use.",
      "conditions": [
        "Material models have documented known limitations used in development/deployment decisions."
      ],
      "expected_evidence": [
        "Model provenance records including known limitations."
      ],
      "known_gaps": [
        "MOD-110 covers model limitations, not full system knowledge-bound documentation or human oversight procedures."
      ]
    },
    {
      "esaf_control_id": "MOD-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-120 requires validation against criteria for intended performance, limitations, explainability, and operating conditions before authorization and after material change.",
      "conditions": [
        "Validation results documenting limitations inform authorization and deployment."
      ],
      "expected_evidence": [
        "Model validation records covering limitations and operating conditions."
      ],
      "known_gaps": [
        "MOD-120 does not alone define how humans utilize and oversee outputs in operations."
      ]
    },
    {
      "esaf_control_id": "AGT-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AGT-120 requires human approval, supervision, intervention, challenge, and appeal for agent decisions and actions.",
      "conditions": [
        "Human oversight of agent outputs/actions is in scope."
      ],
      "expected_evidence": [
        "Agent oversight procedures defining supervision and intervention."
      ],
      "known_gaps": [
        "AGT-120 is agent-scoped and does not document model knowledge limits."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-2.2 mapping record."
    }
  ]
}
---
# MAP-2.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
