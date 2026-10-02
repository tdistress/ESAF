---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-ra-08",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.RA-08",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Processes for receiving, analyzing, and responding to vulnerability disclosures are established"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.RA-08"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "INF-120",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "INF-120 requires identifying, assessing, prioritizing, remediating, or accepting vulnerabilities in AI infrastructure and dependencies.",
      "conditions": [
        "Processes for receiving, analyzing, and responding to vulnerability disclosures affecting AI infrastructure and dependencies are established as part of vulnerability management."
      ],
      "expected_evidence": [
        "Vulnerability disclosure intake, analysis, and response records for AI infra/dependencies."
      ],
      "known_gaps": [
        "INF-120 does not establish an organization-wide vulnerability disclosure program for all products/services."
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
      "change": "Created the draft NIST CSF 2.0 ID.RA-08 mapping record."
    }
  ]
}
---
# ID.RA-08

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
