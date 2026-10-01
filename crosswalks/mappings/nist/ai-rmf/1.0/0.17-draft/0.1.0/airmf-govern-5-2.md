---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-5-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-5.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Mechanisms enable the developing/deploying team to review and incorporate feedback about potential individual and societal AI impacts."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-5.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-130 requires documenting stakeholder input, mitigations, and unresolved impacts before authorization, which provides a mechanism to review and incorporate impact feedback for E2–E4 capabilities.",
      "conditions": [
        "Impact feedback is captured within RSK-130 assessments for E2–E4 capabilities."
      ],
      "expected_evidence": [
        "Impact assessment showing feedback reviewed and mitigations or unresolved impacts recorded."
      ],
      "known_gaps": [
        "RSK-130 does not require ongoing post-deployment feedback incorporation mechanisms for the developing team."
      ]
    },
    {
      "esaf_control_id": "AUD-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "low",
      "rationale": "AUD-140 requires executive review using current information including improvement needs and recording resulting decisions, which may incorporate escalated impact feedback.",
      "conditions": [
        "Impact feedback is escalated into management-review inputs."
      ],
      "expected_evidence": [
        "Management-review inputs and decisions referencing impact feedback."
      ],
      "known_gaps": [
        "AUD-140 is leadership review, not a team-level feedback incorporation mechanism."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-5.2 mapping record."
    }
  ]
}
---
# GOVERN-5.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
