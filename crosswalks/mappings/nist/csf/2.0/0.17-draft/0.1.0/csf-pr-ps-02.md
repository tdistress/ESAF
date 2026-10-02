---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ps-02",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.PS-02",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Software is maintained, replaced, and removed commensurate with risk"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.PS-02"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "ARC-150",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "medium",
      "rationale": "ARC-150 requires governing adoption, currency, deprecation, and retirement of AI technologies and architecture components.",
      "conditions": [
        "AI software technologies are maintained, replaced, and removed commensurate with risk."
      ],
      "expected_evidence": [
        "Technology currency and deprecation/retirement records for AI software components."
      ],
      "known_gaps": [
        "ARC-150 does not maintain all enterprise software outside AI technologies."
      ]
    },
    {
      "esaf_control_id": "APP-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "APP-140 requires secure development including dependency, build, release, and vulnerability practices for AI app artifacts.",
      "conditions": [
        "AI application software is maintained through secure development and release practices commensurate with risk."
      ],
      "expected_evidence": [
        "Release and dependency maintenance records for AI apps."
      ],
      "known_gaps": [
        "APP-140 covers AI application artifacts, not all enterprise software."
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
      "change": "Created the draft NIST CSF 2.0 PR.PS-02 mapping record."
    }
  ]
}
---
# PR.PS-02

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
