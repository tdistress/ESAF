---
{
  "schema_version": "1.0.0",
  "record_id": "csf-rs-mi-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "RS.MI-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Incidents are eradicated RECOVER (RC): Assets and operations affected by a cybersecurity incident are restored • Incident Recovery Plan Execution (RC.RP): Restoration activities are performed to ensure operational availability of systems and services affected by cybersecurity incidents"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory RS.MI-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "OPS-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-120 requires eradicating AI incidents as part of the incident lifecycle.",
      "conditions": [
        "AI incidents are eradicated."
      ],
      "expected_evidence": [
        "Eradication actions and evidence in incident records."
      ],
      "known_gaps": [
        "OPS-120 eradication is AI-incident scoped."
      ]
    },
    {
      "esaf_control_id": "AUD-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AUD-130 requires remediating and closing findings by risk, which can include eradication follow-through after incidents.",
      "conditions": [
        "Eradication-related corrective actions are tracked to closure when captured as findings."
      ],
      "expected_evidence": [
        "Finding remediation and closure evidence tied to incident eradication."
      ],
      "known_gaps": [
        "AUD-130 is finding remediation, not real-time incident eradication."
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
      "change": "Created the draft NIST CSF 2.0 RS.MI-02 mapping record."
    }
  ]
}
---
# RS.MI-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
