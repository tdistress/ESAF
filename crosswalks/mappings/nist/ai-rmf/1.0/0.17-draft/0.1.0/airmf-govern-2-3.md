---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-2-3",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-2.3",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Executive leadership takes responsibility for decisions about risks associated with AI system development and deployment."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-2.3"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "GOV-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "GOV-100 requires executive leadership to establish and maintain enterprise authority with documented accountability and decision rights for governing in-scope AI capabilities.",
      "conditions": [
        "Executive-established authority includes decisions about AI development and deployment risk."
      ],
      "expected_evidence": [
        "Governance authority charter issued by executive leadership."
      ],
      "known_gaps": [
        "GOV-100 establishes authority structure; individual risk-acceptance decisions may be delegated under other controls."
      ]
    },
    {
      "esaf_control_id": "RSK-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-120 requires documented treatment of identified AI risks and acceptance of residual risk from an authority commensurate with the risk before production authorization or continued operation.",
      "conditions": [
        "Residual-risk acceptance for development/deployment decisions uses a commensurate authority, including executive acceptance where risk requires it."
      ],
      "expected_evidence": [
        "Residual-risk acceptance records identifying accepting authority."
      ],
      "known_gaps": [
        "RSK-120 does not require executives to accept every AI risk personally."
      ]
    },
    {
      "esaf_control_id": "AUD-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AUD-140 requires executive leadership to review the AI management system at planned intervals using risk and related information and to record resulting decisions.",
      "conditions": [
        "Management review decisions include AI development/deployment risk posture."
      ],
      "expected_evidence": [
        "Executive management-review minutes with risk decisions."
      ],
      "known_gaps": [
        "AUD-140 is periodic review, not day-to-day deployment authorization."
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
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-2.3 mapping record."
    }
  ]
}
---
# GOVERN-2.3

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
