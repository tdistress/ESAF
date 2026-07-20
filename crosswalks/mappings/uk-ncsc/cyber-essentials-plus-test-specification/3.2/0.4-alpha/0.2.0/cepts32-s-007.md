---
{
  "schema_version": "1.0.0",
  "record_id": "cepts32-s-007",
  "mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
  "status": "draft",
  "external_provision_id": "CEPTS3.2-S-007",
  "granularity": "requirement",
  "external_metadata": {
    "group": "S",
    "kind": "procedure_step",
    "actors": [
      "Assessor"
    ]
  },
  "context": {
    "mode": "paraphrase",
    "summary": "Verify that sample size was calculated correctly using the Delivery Partner's method."
  },
  "source_locator": {
    "official_url": "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf",
    "locator": "PDF page 10; printed page 9; Sample testing; sample-size verification item"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "AUD-120",
      "esaf_control_version": "0.1.0",
      "esaf_control_path": "AUD/AUD-120.md",
      "esaf_control_sha256": "f6aa7dda8b73ee22586eb9728e59d5ec19f357a5c10187cd6c6a1d2c28f34ac0",
      "esaf_requirement_locator": "controls/AUD/AUD-120.md#requirement",
      "relationship": "partially_supports",
      "direction": "external_to_esaf",
      "coverage": "narrow",
      "confidence": "high",
      "rationale": "External observation: the sampling workpaper records whether sample size was calculated correctly using the Delivery Partner method. Supported ESAF outcome: AUD-120 requires relevant, reliable, complete, timely, attributable, and integrity-protected evidence for each AI assessment procedure, determination, scope, and period. Conditions only narrow this supported claim; they do not create either outcome.",
      "conditions": [
        "{\"condition\":\"actor\",\"evidence_references\":[\"record:external_metadata\",\"relationship:expected_evidence\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"scope\",\"evidence_references\":[\"record:context\",\"manifest:AUD-120#requirement\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"population\",\"evidence_references\":[\"relationship:expected_evidence\",\"relationship:known_gaps:0\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"sample\",\"evidence_references\":[\"relationship:expected_evidence\",\"relationship:known_gaps:0\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"assessment_date\",\"evidence_references\":[\"relationship:expected_evidence\",\"record:source_locator\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"evidence_date\",\"evidence_references\":[\"relationship:expected_evidence\",\"record:source_locator\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"tool\",\"evidence_references\":[\"relationship:expected_evidence\",\"record:source_locator\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"provenance\",\"evidence_references\":[\"record:source_locator\",\"manifest:AUD-120#requirement\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"exception\",\"evidence_references\":[\"relationship:expected_evidence\",\"relationship:prohibited_inferences\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"delivery_partner_discretion\",\"evidence_references\":[\"relationship:expected_evidence\",\"relationship:prohibited_inferences\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"point_in_time_status\",\"evidence_references\":[\"relationship:expected_evidence\",\"relationship:known_gaps:0\"],\"status\":\"SATISFIED\"}"
      ],
      "expected_evidence": [
        "A dated attributable sampling workpaper identifies the Assessor, AI assessment scope, population and sample, approved calculation method, inputs, result, provenance, and any exception."
      ],
      "known_gaps": [
        "Calculation correctness under the named method does not establish method suitability, sample representativeness, other evidence properties, or later conditions."
      ],
      "prohibited_inferences": [
        "CEPTS3.2-S-007 | prohibit implementation: The observation does not establish control implementation.",
        "CEPTS3.2-S-007 | prohibit effectiveness: The observation does not establish control effectiveness.",
        "CEPTS3.2-S-007 | prohibit sufficiency: The observation is not sufficient evidence of the control outcome.",
        "CEPTS3.2-S-007 | prohibit compliance: The observation does not establish ESAF compliance.",
        "CEPTS3.2-S-007 | prohibit certification: The observation does not authorize or establish certification.",
        "CEPTS3.2-S-007 | prohibit equivalence: The external provision is not equivalent to the ESAF control.",
        "CEPTS3.2-S-007 | prohibit continuous_assurance: The point-in-time observation is not continuous assurance.",
        "CEPTS3.2-S-007 | prohibit population_wide_coverage: The sampled observation is not population-wide coverage.",
        "CEPTS3.2-S-007 | prohibit current_scheme_coverage: The public v3.2 evidence is not current-scheme coverage."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-crosswalk-editorial-team",
    "date": "2026-07-19",
    "authorized_source_access": true
  },
  "change_history": [
    {
      "version": "0.2.0",
      "date": "2026-07-19",
      "change": "Created the draft Cyber Essentials Plus v3.2 external-to-ESAF evidence record."
    }
  ]
}
---
# CEPTS3.2-S-007

Draft derivative external-to-ESAF evidence analysis for the cited Cyber Essentials Plus v3.2 provision.
