---
{
  "schema_version": "1.0.0",
  "record_id": "cepts32-m-011",
  "mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
  "status": "draft",
  "external_provision_id": "CEPTS3.2-M-011",
  "granularity": "requirement",
  "external_metadata": {
    "group": "M",
    "kind": "evidence_retention",
    "actors": [
      "Certifying Body"
    ]
  },
  "context": {
    "mode": "paraphrase",
    "summary": "Retain all evidence from the pre-test verifications for at least the certificate's lifetime."
  },
  "source_locator": {
    "official_url": "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf",
    "locator": "PDF page 5; printed page 4; Before you begin; closing retention paragraph"
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
      "rationale": "External observation: {\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}. Supported ESAF outcome: AUD-120 requires relevant, reliable, complete, timely, attributable, and integrity-protected evidence to be obtained and retained for each AI assessment procedure, determination, scope, and period. Conditions only narrow this supported claim; they do not create either outcome.",
      "conditions": [
        "{\"condition\":\"actor\",\"evidence_references\":[\"relationship:expected_evidence:0\",\"record:external_metadata\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"scope\",\"evidence_references\":[\"relationship:expected_evidence:1\",\"record:context\",\"manifest:AUD-120#requirement\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"population\",\"evidence_references\":[\"relationship:expected_evidence:2\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"sample\",\"evidence_references\":[\"relationship:expected_evidence:3\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"assessment_date\",\"evidence_references\":[\"relationship:expected_evidence:4\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"evidence_date\",\"evidence_references\":[\"relationship:expected_evidence:5\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"tool\",\"evidence_references\":[\"relationship:expected_evidence:6\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"provenance\",\"evidence_references\":[\"relationship:expected_evidence:7\",\"record:source_locator\",\"manifest:AUD-120#requirement\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"exception\",\"evidence_references\":[\"relationship:expected_evidence:8\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"delivery_partner_discretion\",\"evidence_references\":[\"relationship:expected_evidence:9\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"point_in_time_status\",\"evidence_references\":[\"relationship:expected_evidence:10\",\"relationship:known_gaps:0\"],\"status\":\"SATISFIED\"}"
      ],
      "expected_evidence": [
        "actor evidence: CEPTS3.2-M-011 identifies the Assessor responsible for the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\".",
        "scope evidence: CEPTS3.2-M-011 identifies the in-scope AI subject for the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\": Retain all evidence from the pre-test verifications for at least the certificate's lifetime.",
        "population evidence: CEPTS3.2-M-011 defines the applicable population boundary for the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\" within that scope.",
        "sample evidence: CEPTS3.2-M-011 identifies the sample selected from that defined population and the selection basis for the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\", or confirms that all population members were assessed.",
        "assessment_date evidence: CEPTS3.2-M-011 records the assessment date, time, and timezone for the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\".",
        "evidence_date evidence: CEPTS3.2-M-011 records the evidence-collection date, time, and timezone separately from the assessment date for the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\".",
        "tool evidence: CEPTS3.2-M-011 names the tool and version or documented manual method used to produce the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\".",
        "provenance evidence: CEPTS3.2-M-011 links source artifacts, the source locator, and the cited ESAF requirement for the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\". Provision-specific record set: A dated integrity-protected evidence index identifies the Certifying Body, AI assessment scope, population and sample, verification artifacts, collection method, provenance, retention period, and any exception.",
        "exception evidence: CEPTS3.2-M-011 records that no exception affected the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\", or identifies the exception approval and disposition.",
        "delivery_partner_discretion evidence: CEPTS3.2-M-011 records whether Delivery Partner discretion affected the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\", identifying the applicable choice, method, or approval, or the basis for none.",
        "point_in_time_status evidence: CEPTS3.2-M-011 limits the observed result \"the dated retention record shows that all evidence from the pre-test verifications was retained for at least the certificate lifetime\" to the assessment and evidence dates, defined population, and selected sample; later state is excluded."
      ],
      "known_gaps": [
        "Retention does not establish the quality of each artifact, coverage beyond the recorded assessment, or conditions after the evidence period."
      ],
      "prohibited_inferences": [
        "CEPTS3.2-M-011 | prohibit implementation: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" does not establish control implementation for the cited AUD-120 outcome.",
        "CEPTS3.2-M-011 | prohibit effectiveness: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" does not establish control effectiveness for the cited AUD-120 outcome.",
        "CEPTS3.2-M-011 | prohibit sufficiency: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" is not sufficient evidence for the cited AUD-120 outcome.",
        "CEPTS3.2-M-011 | prohibit compliance: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" does not establish ESAF compliance for the cited AUD-120 outcome.",
        "CEPTS3.2-M-011 | prohibit certification: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" does not authorize or establish certification for the cited AUD-120 outcome.",
        "CEPTS3.2-M-011 | prohibit equivalence: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" is not equivalent for the cited AUD-120 outcome.",
        "CEPTS3.2-M-011 | prohibit continuous_assurance: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" does not provide continuous assurance for the cited AUD-120 outcome.",
        "CEPTS3.2-M-011 | prohibit population_wide_coverage: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" does not establish population-wide coverage for the cited AUD-120 outcome.",
        "CEPTS3.2-M-011 | prohibit current_scheme_coverage: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"retention_duration\",\"provision_id\":\"CEPTS3.2-M-011\",\"result_kind\":\"evidence_retention\",\"result_type\":\"recorded_duration\",\"subject\":\"pre_test_verification_evidence\"}\" does not establish current-scheme coverage for the cited AUD-120 outcome."
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
# CEPTS3.2-M-011

Draft derivative external-to-ESAF evidence analysis for the cited Cyber Essentials Plus v3.2 provision.
