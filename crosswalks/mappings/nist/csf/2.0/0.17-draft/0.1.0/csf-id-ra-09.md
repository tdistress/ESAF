---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-ra-09",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.RA-09",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "The authenticity and integrity of hardware and software are assessed prior to acquisition and use"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.RA-09"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "MOD-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "MOD-110 requires verifying model provenance, source, licensing, integrity, dependencies, and supplier terms before use.",
      "conditions": [
        "Authenticity and integrity of models (software) are assessed prior to acquisition and use."
      ],
      "expected_evidence": [
        "Model provenance, integrity verification, and supplier-term records."
      ],
      "known_gaps": [
        "MOD-110 does not assess authenticity/integrity of general enterprise hardware or non-model software."
      ]
    },
    {
      "esaf_control_id": "APP-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "APP-140 requires secure development including dependency and build controls for AI application artifacts.",
      "conditions": [
        "Integrity of AI application software dependencies is assessed in the secure development lifecycle."
      ],
      "expected_evidence": [
        "Dependency review and build integrity evidence for AI apps."
      ],
      "known_gaps": [
        "APP-140 does not cover hardware authenticity assessment."
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
      "change": "Created the draft NIST CSF 2.0 ID.RA-09 mapping record."
    }
  ]
}
---
# ID.RA-09

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
