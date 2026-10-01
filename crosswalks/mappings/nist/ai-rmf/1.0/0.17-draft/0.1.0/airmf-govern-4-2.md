---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-4-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-4.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Teams document AI risks and potential impacts and communicate about those impacts more broadly."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-4.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-130 requires assessment of reasonably foreseeable beneficial and adverse impacts of E2 through E4 AI capabilities on the organization, individuals, affected groups, society, and the environment where relevant, documenting evidence, uncertainty, stakeholder input, mitigations, and unresolved impacts before authorization.",
      "conditions": [
        "The AI system is classified E2, E3, or E4 so RSK-130 applies."
      ],
      "expected_evidence": [
        "Completed AI impact assessment with documented impacts and stakeholder input."
      ],
      "known_gaps": [
        "RSK-130 does not apply to E1 capabilities and does not require broad external communication beyond documented stakeholder input."
      ]
    },
    {
      "esaf_control_id": "RSK-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-120 requires documenting, approving, implementing, and monitoring treatments for identified AI risks and accepting residual risk before production authorization or continued operation.",
      "conditions": [
        "Identified risks and treatments are documented for the capability."
      ],
      "expected_evidence": [
        "Risk-treatment and residual-risk acceptance records."
      ],
      "known_gaps": [
        "RSK-120 does not require communicating impacts more broadly outside risk-acceptance channels."
      ]
    },
    {
      "esaf_control_id": "CMP-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "CMP-110 requires creating and disclosing AI records, notices, and reports according to applicable audience and accessibility requirements when obligations require communication.",
      "conditions": [
        "Applicable obligations require impact-related notices or reports."
      ],
      "expected_evidence": [
        "Submitted or published AI notices/reports required by obligations."
      ],
      "known_gaps": [
        "CMP-110 is obligation-driven disclosure, not a general impact-communication practice."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-4.2 mapping record."
    }
  ]
}
---
# GOVERN-4.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
