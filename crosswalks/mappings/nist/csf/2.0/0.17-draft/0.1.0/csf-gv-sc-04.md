---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-sc-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.SC-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Suppliers are known and prioritized by criticality"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.SC-04"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "API-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "API-140 requires enforcing security, privacy, data-use, continuity, and exit requirements per external AI integration.",
      "conditions": [
        "External AI suppliers and integrations are known and can be prioritized by criticality for in-scope AI."
      ],
      "expected_evidence": [
        "External AI integration inventory with criticality or risk classification."
      ],
      "known_gaps": [
        "API-140 does not maintain an enterprise supplier inventory outside AI integrations."
      ]
    },
    {
      "esaf_control_id": "MOD-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MOD-110 requires verifying model provenance, source, licensing, integrity, dependencies, and supplier terms before use.",
      "conditions": [
        "Model suppliers are known before acquisition and use."
      ],
      "expected_evidence": [
        "Model provenance and supplier-term records."
      ],
      "known_gaps": [
        "MOD-110 covers model suppliers, not all organizational suppliers."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-project-owner",
    "date": "2026-10-02"
  },
  "change_history": [
    {
      "version": "0.1.0",
      "date": "2026-10-02",
      "change": "Created the draft NIST CSF 2.0 GV.SC-04 mapping record."
    }
  ]
}
---
# GV.SC-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
