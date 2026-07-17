---
{
  "schema_version": "1.0.0", "record_id": "cepts32-s-008", "mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0", "status": "draft",
  "external_provision_id": "CEPTS3.2-S-008", "granularity": "requirement",
  "external_metadata": {"group": "S", "kind": "evidence_retention", "actors": ["Certifying Body"]},
  "context": {"mode": "paraphrase", "summary": "Retain evidence of the sample-size calculation for at least the certificate's lifetime."},
  "source_locator": {"official_url": "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf", "locator": "PDF page 10; printed page 9; Sample testing; sample-calculation evidence sentence"},
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-110",
      "esaf_control_version": "0.1.0",
      "esaf_control_path": "CMP/CMP-110.md",
      "esaf_control_sha256": "b02bad69b329e16ff1ac0becf9ff7eddfe9a0cdf6033f43045b03359a1aeed68",
      "esaf_requirement_locator": "controls/CMP/CMP-110.md#requirement",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "high",
      "rationale": "CMP-110 directly requires retention of AI evidence according to applicable content and retention requirements, supporting preservation of a qualifying sampling-calculation record for its applicable period.",
      "conditions": [
        "The calculation evidence is an AI record governed by CMP-110, and the certificate-lifetime period is an applicable retention requirement."
      ],
      "expected_evidence": [
        "A retention schedule and protected record show preservation of the qualifying calculation evidence for the applicable certificate period."
      ],
      "known_gaps": [
        "CMP-110 does not require creation or correctness of the sample-size calculation, prescribe the Delivery Partner's method, or assign the Certifying Body's role.",
        "CMP-110 does not establish that any sample was selected, tested, representative, or sufficient for its population."
      ],
      "prohibited_inferences": [
        "No inference that the calculation exists, is correct, or was verified against the external method.",
        "No inference of sample or population coverage, procedure execution, observed results, certification, compliance, equivalence, or endorsement."
      ]
    }
  ],
  "mapper": {"id": "esaf-crosswalk-editorial-team", "date": "2026-07-16", "authorized_source_access": true},
  "change_history": [{"version": "0.1.0", "date": "2026-07-16", "change": "Created the draft Cyber Essentials Plus v3.2 methodology mapping record."}]
}
---
# CEPTS3.2-S-008

Draft derivative mapping analysis for the cited Cyber Essentials Plus v3.2 methodology provision.
