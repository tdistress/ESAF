---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-ae-06",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.AE-06",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Information on adverse events is provided to authorized staff and tools"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.AE-06"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-140 requires escalating AI alerts to authorized staff and enabling response tooling paths.",
      "conditions": [
        "Information on adverse AI events is provided to authorized staff and tools through alert ownership and escalation."
      ],
      "expected_evidence": [
        "Escalation records and tool integrations for AI alerts."
      ],
      "known_gaps": [
        "MON-140 does not distribute adverse-event information enterprise-wide outside AI alert channels."
      ]
    },
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-120 requires communicating AI incident information to relevant stakeholders within incident management.",
      "conditions": [
        "Incident-level adverse-event information is provided to authorized staff."
      ],
      "expected_evidence": [
        "Incident communication records."
      ],
      "known_gaps": [
        "OPS-120 is incident-centric."
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
      "change": "Created the draft NIST CSF 2.0 DE.AE-06 mapping record."
    }
  ]
}
---
# DE.AE-06

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
