---
{
  "schema_version": "1.0.0",
  "record_id": "csf-gv-oc-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GV.OC-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Legal, regulatory, and contractual requirements regarding cybersecurity — including privacy and civil liberties obligations — are understood and managed"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory GV.OC-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "CMP-100 requires the organization to identify, interpret, record, assign, implement, monitor, and update legal, regulatory, contractual, policy, ethical, and sector obligations applicable to each AI capability and the enterprise AI management system.",
      "conditions": [
        "Cybersecurity, privacy, and civil-liberties obligations applicable to in-scope AI are treated as CMP-100 obligations."
      ],
      "expected_evidence": [
        "Obligation register covering legal, regulatory, contractual, and privacy obligations with owners and status."
      ],
      "known_gaps": [
        "CMP-100 is AI-scoped and does not by itself establish the full enterprise cybersecurity legal register outside AI."
      ]
    },
    {
      "esaf_control_id": "DAT-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "DAT-140 requires implementing privacy requirements including minimization, individual rights, transfers, and automated-decision duties for AI data.",
      "conditions": [
        "Privacy and civil-liberties obligations for AI data processing are in scope."
      ],
      "expected_evidence": [
        "Privacy requirement implementations and rights-handling records for AI data."
      ],
      "known_gaps": [
        "DAT-140 does not cover non-privacy cybersecurity legal obligations."
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
      "change": "Created the draft NIST CSF 2.0 GV.OC-03 mapping record."
    }
  ]
}
---
# GV.OC-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
