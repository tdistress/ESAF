---
{
  "schema_version": "1.0.0",
  "record_id": "csf-pr-ps-06",
  "mapping_set_id": "nist--csf--2.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "PR.PS-06",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Secure software development practices are integrated, and their performance is monitored throughout the software development life cycle • Technology Infrastructure Resilience (PR.IR): Security architectures are managed with the organization's risk strategy to protect asset confidentiality, integrity, and availability, and organizational resilience"
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "locator": "NIST CSF 2.0, subcategory PR.PS-06"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "APP-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "APP-140 requires applying secure development, review, test, dependency, build, release, vulnerability, and change practices to AI application artifacts and monitoring their performance through the lifecycle.",
      "conditions": [
        "Secure software development practices are integrated and monitored for AI applications."
      ],
      "expected_evidence": [
        "Secure SDLC evidence, reviews, tests, and monitoring for AI app development."
      ],
      "known_gaps": [
        "APP-140 covers AI application development, not all enterprise software development."
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
      "change": "Created the draft NIST CSF 2.0 PR.PS-06 mapping record."
    }
  ]
}
---
# PR.PS-06

Draft derivative mapping analysis for the cited NIST CSF 2.0 subcategory.
