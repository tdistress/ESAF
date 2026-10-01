---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-4-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-4.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Approaches for mapping AI technology and legal risks of components—including third-party AI and intellectual-property or other rights infringement—are in place, followed, and documented."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-4.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "CMP-140 requires identifying, approving, complying with, and retaining evidence of intellectual-property ownership, license, attribution, usage, distribution, training, output, indemnity, and restriction requirements for AI data, models, code, prompts, tools, and generated content.",
      "conditions": [
        "IP and licensing risks of AI components are in scope."
      ],
      "expected_evidence": [
        "IP/licensing approval and evidence records for AI components."
      ],
      "known_gaps": [
        "CMP-140 addresses IP/licensing obligations, not all technology risk mapping methods."
      ]
    },
    {
      "esaf_control_id": "CMP-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "CMP-120 requires establishing and monitoring third-party AI obligations including intellectual property, security, privacy, and related domains.",
      "conditions": [
        "Third-party AI technologies are used as components."
      ],
      "expected_evidence": [
        "Third-party AI obligation and monitoring records."
      ],
      "known_gaps": [
        "CMP-120 is obligation-centric rather than a full technology-risk mapping method."
      ]
    },
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-100 requires consistent application of an AI risk methodology covering scope, dimensions, rating, treatment, and reassessment.",
      "conditions": [
        "Component and legal risks are assessed using the approved methodology."
      ],
      "expected_evidence": [
        "Risk assessments covering AI technology components and legal risk dimensions."
      ],
      "known_gaps": [
        "RSK-100 does not expressly require IP-infringement risk mapping as a distinct approach."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-4.1 mapping record."
    }
  ]
}
---
# MAP-4.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
