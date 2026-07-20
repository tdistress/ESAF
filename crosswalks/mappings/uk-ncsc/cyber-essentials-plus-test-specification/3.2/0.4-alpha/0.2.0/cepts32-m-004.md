---
{
  "schema_version": "1.0.0",
  "record_id": "cepts32-m-004",
  "mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
  "status": "draft",
  "external_provision_id": "CEPTS3.2-M-004",
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
    "summary": "Technically verify that the Plus boundary corresponds to the assessed environment."
  },
  "source_locator": {
    "official_url": "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf",
    "locator": "PDF page 5; printed page 4; Before you begin; pre-test list, technical scope item"
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
      "rationale": "External observation: {\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}. Supported ESAF outcome: AUD-120 requires relevant, reliable, complete, timely, attributable, and integrity-protected evidence for each AI assessment scope and period. Conditions only narrow this supported claim; they do not create either outcome.",
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
        "actor evidence: CEPTS3.2-M-004 identifies the Assessor responsible for the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\".",
        "scope evidence: CEPTS3.2-M-004 identifies the in-scope AI subject for the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\": Technically verify that the Plus boundary corresponds to the assessed environment.",
        "population evidence: CEPTS3.2-M-004 defines the applicable population boundary for the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\" within that scope.",
        "sample evidence: CEPTS3.2-M-004 identifies the sample selected from that defined population and the selection basis for the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\", or confirms that all population members were assessed.",
        "assessment_date evidence: CEPTS3.2-M-004 records the assessment date, time, and timezone for the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\".",
        "evidence_date evidence: CEPTS3.2-M-004 records the evidence-collection date, time, and timezone separately from the assessment date for the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\".",
        "tool evidence: CEPTS3.2-M-004 names the tool and version or documented manual method used to produce the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\".",
        "provenance evidence: CEPTS3.2-M-004 links source artifacts, the source locator, and the cited ESAF requirement for the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\". Provision-specific record set: A dated and attributable technical comparison identifies the Assessor, declared boundary, assessed environment, population and sample, method, source artifacts, result, and any exception.",
        "exception evidence: CEPTS3.2-M-004 records that no exception affected the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\", or identifies the exception approval and disposition.",
        "delivery_partner_discretion evidence: CEPTS3.2-M-004 records whether Delivery Partner discretion affected the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\", identifying the applicable choice, method, or approval, or the basis for none.",
        "point_in_time_status evidence: CEPTS3.2-M-004 limits the observed result \"a dated technical comparison recorded whether the declared Plus boundary corresponded to the assessed environment\" to the assessment and evidence dates, defined population, and selected sample; later state is excluded."
      ],
      "known_gaps": [
        "The comparison does not establish evidence quality for unexamined environments, other assessment procedures, or later conditions."
      ],
      "prohibited_inferences": [
        "CEPTS3.2-M-004 | prohibit implementation: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" does not establish control implementation for the cited AUD-120 outcome.",
        "CEPTS3.2-M-004 | prohibit effectiveness: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" does not establish control effectiveness for the cited AUD-120 outcome.",
        "CEPTS3.2-M-004 | prohibit sufficiency: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" is not sufficient evidence for the cited AUD-120 outcome.",
        "CEPTS3.2-M-004 | prohibit compliance: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" does not establish ESAF compliance for the cited AUD-120 outcome.",
        "CEPTS3.2-M-004 | prohibit certification: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" does not authorize or establish certification for the cited AUD-120 outcome.",
        "CEPTS3.2-M-004 | prohibit equivalence: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" is not equivalent for the cited AUD-120 outcome.",
        "CEPTS3.2-M-004 | prohibit continuous_assurance: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" does not provide continuous assurance for the cited AUD-120 outcome.",
        "CEPTS3.2-M-004 | prohibit population_wide_coverage: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" does not establish population-wide coverage for the cited AUD-120 outcome.",
        "CEPTS3.2-M-004 | prohibit current_scheme_coverage: The observed result \"{\"assessment_date_boundary\":\"assessment_date_required\",\"control_id\":\"AUD-120\",\"evidence_date_boundary\":\"evidence_date_required\",\"predicate\":\"scope_correspondence_status\",\"provision_id\":\"CEPTS3.2-M-004\",\"result_kind\":\"assessment_scope\",\"result_type\":\"recorded_comparison\",\"subject\":\"declared_assessment_boundary\"}\" does not establish current-scheme coverage for the cited AUD-120 outcome."
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
# CEPTS3.2-M-004

Draft derivative external-to-ESAF evidence analysis for the cited Cyber Essentials Plus v3.2 provision.
