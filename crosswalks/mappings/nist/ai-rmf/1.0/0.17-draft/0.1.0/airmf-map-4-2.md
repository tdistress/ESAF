---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-4-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-4.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Internal risk controls for AI system components, including third-party AI technologies, are identified and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-4.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-120 requires documenting, approving, implementing, and monitoring treatments for identified AI risks.",
      "conditions": [
        "Treatments include controls applicable to AI system components."
      ],
      "expected_evidence": [
        "Documented risk treatments mapped to component risks."
      ],
      "known_gaps": [
        "RSK-120 does not require a component-level control inventory distinct from risk treatments."
      ]
    },
    {
      "esaf_control_id": "ARC-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "ARC-140 requires documenting and monitoring responsibility boundaries and inherited controls among providers and suppliers.",
      "conditions": [
        "Third-party AI technologies contribute inherited controls under shared responsibility."
      ],
      "expected_evidence": [
        "Shared-responsibility and inherited-control documentation."
      ],
      "known_gaps": [
        "ARC-140 documents inherited/shared controls, not all internal component controls."
      ]
    },
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "CMP-120 requires verifying and monitoring third-party AI obligations and related controls.",
      "conditions": [
        "Third-party AI technologies are covered by CMP-120 verification."
      ],
      "expected_evidence": [
        "Third-party verification/monitoring evidence for AI suppliers."
      ],
      "known_gaps": [
        "CMP-120 does not inventory internal non-third-party component controls."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-4.2 mapping record."
    }
  ]
}
---
# MAP-4.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
