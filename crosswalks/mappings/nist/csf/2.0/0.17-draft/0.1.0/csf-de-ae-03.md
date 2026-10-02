---
{
  "schema_version": "1.0.0",
  "record_id": "csf-de-ae-03",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "DE.AE-03",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Information is correlated from multiple sources"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory DE.AE-03"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MON-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "MON-110 requires investigating AI security events using available telemetry sources.",
      "conditions": [
        "Information from multiple AI telemetry sources is correlated during investigation of adverse events."
      ],
      "expected_evidence": [
        "Investigation records showing multi-source correlation for AI events."
      ],
      "known_gaps": [
        "MON-110 does not require a general SIEM correlation platform for all enterprise sources."
      ]
    },
    {
      "esaf_control_id": "MON-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "MON-100 requires multi-facet telemetry (identity, input, model, output, tool, config, policy) enabling correlation.",
      "conditions": [
        "Multiple AI telemetry facets are available to correlate for adverse-event analysis."
      ],
      "expected_evidence": [
        "Multi-facet AI telemetry available to investigators."
      ],
      "known_gaps": [
        "MON-100 collects telemetry but does not itself perform correlation."
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
      "change": "Created the draft NIST CSF 2.0 DE.AE-03 mapping record."
    }
  ]
}
---
# DE.AE-03

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
