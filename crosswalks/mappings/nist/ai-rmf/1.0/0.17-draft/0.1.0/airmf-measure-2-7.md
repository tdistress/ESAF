---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-measure-2-7",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MEASURE-2.7",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "AI system security and resilience identified during MAP are evaluated and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MEASURE-2.7"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MOD-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-120 requires validation against security and resilience criteria before authorization and after material change.",
      "conditions": [
        "Security and resilience are included in approved validation criteria."
      ],
      "expected_evidence": [
        "Model validation records covering security and resilience criteria."
      ],
      "known_gaps": [
        "MOD-120 is model-scoped and may not evaluate full system security/resilience."
      ]
    },
    {
      "esaf_control_id": "APP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "APP-100 requires design using documented threat and misuse cases, security requirements, and failure modes.",
      "conditions": [
        "Security requirements and failure modes are documented in application design."
      ],
      "expected_evidence": [
        "AI application threat/misuse and security-requirement design records."
      ],
      "known_gaps": [
        "APP-100 is design documentation, not ongoing security/resilience evaluation."
      ]
    },
    {
      "esaf_control_id": "ARC-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "ARC-130 requires designing AI capabilities for foreseeable component, model, data, provider, network, capacity, quality, and control failures using isolation, graceful degradation, safe state, fallback, reversibility, recovery, and tested resumption.",
      "conditions": [
        "Resilience design and tested resumption evidence are used for resilience evaluation."
      ],
      "expected_evidence": [
        "Resilience design and test evidence for failure modes."
      ],
      "known_gaps": [
        "ARC-130 is architecture/design resilience, not a complete security evaluation."
      ]
    },
    {
      "esaf_control_id": "MON-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-110 requires detecting and investigating risk-relevant AI security events.",
      "conditions": [
        "Security evaluation includes detection of security events in operation."
      ],
      "expected_evidence": [
        "Security detection use cases and investigation records."
      ],
      "known_gaps": [
        "MON-110 detects events; it does not perform comprehensive resilience evaluation."
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
      "change": "Created the draft NIST AI RMF 1.0 MEASURE-2.7 mapping record."
    }
  ]
}
---
# MEASURE-2.7

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
