---
{
  "schema_version": "1.0.0",
  "record_id": "cepts32-m-010",
  "mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
  "status": "draft",
  "external_provision_id": "CEPTS3.2-M-010",
  "granularity": "requirement",
  "external_metadata": {
    "group": "M",
    "kind": "prerequisite",
    "actors": [
      "Assessor"
    ]
  },
  "context": {
    "mode": "paraphrase",
    "summary": "Resolve issues found during the listed pre-test checks before Plus testing commences."
  },
  "source_locator": {
    "official_url": "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf",
    "locator": "PDF page 5; printed page 4; Before you begin; paragraph following pre-test list"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AUD-130",
      "esaf_control_version": "0.1.0",
      "esaf_control_path": "AUD/AUD-130.md",
      "esaf_control_sha256": "cecd8e3e917827670267476d7c35d15b46a51eca4878eff2b5d13f7cdf13eca5",
      "esaf_requirement_locator": "controls/AUD/AUD-130.md#requirement",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "high",
      "rationale": "AUD-130 directly requires remediation and closure of AI assessment findings, contributing to resolution of a preliminary issue when that issue is governed as such a finding.",
      "conditions": [
        "The preliminary issue is formally governed as an AI assessment finding under ESAF and falls within the organization's remediation responsibility."
      ],
      "expected_evidence": [
        "A finding record identifies the issue, responsible owner, risk basis, remediation, retest, closure, and retained evidence."
      ],
      "known_gaps": [
        "AUD-130 does not require every preliminary issue to be cleared.",
        "AUD-130 does not impose closure ahead of the external test sequence.",
        "AUD-130 does not assign issue resolution to the Assessor.",
        "AUD-130 does not establish execution or results for any Cyber Essentials Plus procedure."
      ],
      "prohibited_inferences": [
        "No inference that preliminary Cyber Essentials Plus checks were executed or produced results.",
        "No inference that every issue was cleared before testing.",
        "No inference of testing completion, certification, compliance, equivalence, or endorsement."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-crosswalk-editorial-team",
    "date": "2026-07-16",
    "authorized_source_access": true
  },
  "change_history": [
    {
      "version": "0.1.0",
      "date": "2026-07-16",
      "change": "Created the draft Cyber Essentials Plus v3.2 methodology mapping record."
    }
  ]
}
---
# CEPTS3.2-M-010

Draft derivative mapping analysis for the cited Cyber Essentials Plus v3.2 methodology provision.
