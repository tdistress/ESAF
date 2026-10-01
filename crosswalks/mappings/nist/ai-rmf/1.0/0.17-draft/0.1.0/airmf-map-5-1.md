---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-map-5-1",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MAP-5.1",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Likelihood and magnitude of each identified impact—beneficial and harmful—are identified and documented using expected use, similar contexts, incidents, feedback, or other data."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MAP-5.1"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "RSK-100 requires an AI risk methodology defining rating criteria for inherent and residual risk based on evidence.",
      "conditions": [
        "Impact likelihood and magnitude are rated using the approved methodology."
      ],
      "expected_evidence": [
        "Risk ratings with documented likelihood/impact criteria and evidence sources."
      ],
      "known_gaps": [
        "RSK-100 defines methodology; individual impact enumeration may also rely on RSK-130."
      ]
    },
    {
      "esaf_control_id": "RSK-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "RSK-130 requires assessing beneficial and adverse impacts for E2–E4 capabilities and documenting evidence, uncertainty, stakeholder input, mitigations, and unresolved impacts.",
      "conditions": [
        "The capability is E2–E4."
      ],
      "expected_evidence": [
        "Impact assessment enumerating beneficial and adverse impacts with supporting evidence."
      ],
      "known_gaps": [
        "RSK-130 does not expressly require quantitative likelihood and magnitude for every impact."
      ]
    },
    {
      "esaf_control_id": "RSK-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "RSK-110 requires classification using documented criteria for impact and likelihood among other factors before approved use.",
      "conditions": [
        "Capability classification reflects impact and likelihood judgment."
      ],
      "expected_evidence": [
        "Capability classification worksheet documenting impact and likelihood criteria."
      ],
      "known_gaps": [
        "RSK-110 classifies the capability overall, not each identified impact."
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
      "change": "Created the draft NIST AI RMF 1.0 MAP-5.1 mapping record."
    }
  ]
}
---
# MAP-5.1

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
