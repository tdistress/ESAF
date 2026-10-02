---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-am-04",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.AM-04",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Inventories of services provided by suppliers are maintained"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.AM-04"
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
      "rationale": "API-140 requires managing external AI integrations with security, privacy, continuity, and exit requirements.",
      "conditions": [
        "Inventories of AI services provided by suppliers are maintained for in-scope integrations."
      ],
      "expected_evidence": [
        "External AI integration inventory."
      ],
      "known_gaps": [
        "API-140 does not inventory all supplier services enterprise-wide."
      ]
    },
    {
      "esaf_control_id": "ARC-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "ARC-140 requires documenting shared-responsibility boundaries with platforms, providers, and suppliers.",
      "conditions": [
        "Supplier-provided AI platform/services are recorded in shared-responsibility documentation."
      ],
      "expected_evidence": [
        "Shared-responsibility records naming supplier services."
      ],
      "known_gaps": [
        "ARC-140 is boundary documentation, not a complete supplier-service CMDB."
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
      "change": "Created the draft NIST CSF 2.0 ID.AM-04 mapping record."
    }
  ]
}
---
# ID.AM-04

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
