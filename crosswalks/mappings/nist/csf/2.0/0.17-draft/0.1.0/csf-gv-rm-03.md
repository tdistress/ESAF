---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-rm-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.RM-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Cybersecurity risk management activities and outcomes are included in enterprise risk management processes"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.RM-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "RSK-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "RSK-100 requires AI risk methodology application including treatment, acceptance, monitoring, and escalation that can feed enterprise risk processes.",
      "conditions": [
        "AI cybersecurity risk activities and outcomes are included in enterprise risk management where the organization integrates AI risk into ERM."
      ],
      "expected_evidence": [
        "AI risk assessments and escalation records linked to enterprise risk reporting."
      ],
      "known_gaps": [
        "RSK-100 does not mandate that enterprise ERM include cybersecurity risk management as a named process."
      ]
    },
    {
      "esaf_control_id": "AUD-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "AUD-140 requires executive review of the AI management system including risk, incidents, controls, suppliers, and improvement.",
      "conditions": [
        "Executive review outputs inform enterprise risk discussions for AI cybersecurity risk."
      ],
      "expected_evidence": [
        "Management-review packs including AI risk outcomes."
      ],
      "known_gaps": [
        "AUD-140 is AI management-system review, not a full ERM integration control."
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
      "change": "Created the draft NIST CSF 2.0 GV.RM-03 mapping record."
    }
  ]
}
---
# GV.RM-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
