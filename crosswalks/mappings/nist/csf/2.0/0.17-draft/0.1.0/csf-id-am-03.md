---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-am-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.AM-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Representations of the organization's authorized network communication and internal and external network data flows are maintained"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.AM-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "ARC-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "ARC-110 requires documenting AI components, actors, identities, data and control flows, trust levels, dependencies, and boundaries.",
      "conditions": [
        "Representations of authorized network communication and internal/external data flows for AI systems are maintained in architecture documentation."
      ],
      "expected_evidence": [
        "AI architecture diagrams documenting data and control flows and trust boundaries."
      ],
      "known_gaps": [
        "ARC-110 does not maintain enterprise-wide network flow representations outside AI systems."
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
      "change": "Created the draft NIST CSF 2.0 ID.AM-03 mapping record."
    }
  ]
}
---
# ID.AM-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
