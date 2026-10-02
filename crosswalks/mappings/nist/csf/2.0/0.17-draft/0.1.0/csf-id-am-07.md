---
{
  "schema_version": "1.0.0",
  "record_id": "csf-id-am-07",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "ID.AM-07",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Inventories of data and corresponding metadata for designated data types are maintained"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory ID.AM-07"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "DAT-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "DAT-100 requires approving owner, authority, purpose, users, sharing, retention, and prohibited uses for AI data.",
      "conditions": [
        "Inventories of designated AI data types and corresponding metadata are maintained through data-purpose and ownership records."
      ],
      "expected_evidence": [
        "Approved AI data-purpose and ownership records for designated data types."
      ],
      "known_gaps": [
        "DAT-100 does not maintain enterprise data inventories outside AI."
      ]
    },
    {
      "esaf_control_id": "DAT-130",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "DAT-130 requires maintaining provenance and lineage for material AI data end-to-end.",
      "conditions": [
        "Metadata for material AI data types includes provenance/lineage."
      ],
      "expected_evidence": [
        "Provenance and lineage records for material AI data."
      ],
      "known_gaps": [
        "DAT-130 covers material AI data, not all designated enterprise data types."
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
      "change": "Created the draft NIST CSF 2.0 ID.AM-07 mapping record."
    }
  ]
}
---
# ID.AM-07

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
