---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-3-5",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-3.5",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Processes for human oversight are defined, assessed, and documented, including people responsible for overseeing deployed AI systems."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-3.5"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AGT-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "AGT-120 requires defining and implementing risk-proportionate human approval, supervision, intervention, challenge, and appeal for agent decisions and actions.",
      "conditions": [
        "The system includes agent/autonomous paths requiring human oversight."
      ],
      "expected_evidence": [
        "Documented oversight procedures identifying responsible supervisors and intervention conditions."
      ],
      "known_gaps": [
        "AGT-120 is agent-scoped; non-agent oversight may need adjacent controls."
      ]
    },
    {
      "esaf_control_id": "APP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "APP-100 requires documented human-oversight points in AI application design.",
      "conditions": [
        "AI application design identifies oversight points and responsible roles."
      ],
      "expected_evidence": [
        "Design documentation listing human-oversight points."
      ],
      "known_gaps": [
        "APP-100 is design-time and does not alone assess ongoing oversight effectiveness."
      ]
    },
    {
      "esaf_control_id": "GOV-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "GOV-130 assigns accountable owners with authority for operation and risk of each AI capability.",
      "conditions": [
        "Accountable owners are identified as responsible for oversight accountability."
      ],
      "expected_evidence": [
        "Ownership records assigning operational authority."
      ],
      "known_gaps": [
        "GOV-130 does not define detailed human-oversight operating procedures."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-3.5 mapping record."
    }
  ]
}
---
# MAP-3.5

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
