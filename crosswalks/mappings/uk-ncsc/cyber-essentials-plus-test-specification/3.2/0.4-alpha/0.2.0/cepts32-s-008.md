---
{
  "schema_version": "1.0.0",
  "record_id": "cepts32-s-008",
  "mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
  "status": "draft",
  "external_provision_id": "CEPTS3.2-S-008",
  "granularity": "requirement",
  "external_metadata": {
    "group": "S",
    "kind": "evidence_retention",
    "actors": [
      "Certifying Body"
    ]
  },
  "context": {
    "mode": "paraphrase",
    "summary": "Retain evidence of the sample-size calculation for at least the certificate's lifetime."
  },
  "source_locator": {
    "official_url": "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf",
    "locator": "PDF page 10; printed page 9; Sample testing; sample-calculation evidence sentence"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "CMP-110",
      "esaf_control_version": "0.1.0",
      "esaf_control_path": "CMP/CMP-110.md",
      "esaf_control_sha256": "b02bad69b329e16ff1ac0becf9ff7eddfe9a0cdf6033f43045b03359a1aeed68",
      "esaf_requirement_locator": "controls/CMP/CMP-110.md#requirement",
      "relationship": "partially_supports",
      "direction": "external_to_esaf",
      "coverage": "narrow",
      "confidence": "high",
      "rationale": "External observation: the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime. Supported ESAF outcome: CMP-110 requires AI records, notices, registrations, reports, and evidence to be created, protected, retained, disclosed, submitted, and disposed of according to applicable record requirements. Conditions only narrow this supported claim; they do not create either outcome.",
      "conditions": [
        "{\"condition\":\"actor\",\"evidence_references\":[\"relationship:expected_evidence:0\",\"record:external_metadata\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"scope\",\"evidence_references\":[\"relationship:expected_evidence:1\",\"record:context\",\"manifest:CMP-110#requirement\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"population\",\"evidence_references\":[\"relationship:expected_evidence:2\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"sample\",\"evidence_references\":[\"relationship:expected_evidence:3\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"assessment_date\",\"evidence_references\":[\"relationship:expected_evidence:4\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"evidence_date\",\"evidence_references\":[\"relationship:expected_evidence:5\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"tool\",\"evidence_references\":[\"relationship:expected_evidence:6\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"provenance\",\"evidence_references\":[\"relationship:expected_evidence:7\",\"record:source_locator\",\"manifest:CMP-110#requirement\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"exception\",\"evidence_references\":[\"relationship:expected_evidence:8\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"delivery_partner_discretion\",\"evidence_references\":[\"relationship:expected_evidence:9\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"point_in_time_status\",\"evidence_references\":[\"relationship:expected_evidence:10\",\"relationship:known_gaps:0\"],\"status\":\"SATISFIED\"}"
      ],
      "expected_evidence": [
        "actor evidence: CEPTS3.2-S-008 identifies the Assessor responsible for the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\".",
        "scope evidence: CEPTS3.2-S-008 identifies the in-scope AI subject for the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\": Retain evidence of the sample-size calculation for at least the certificate's lifetime.",
        "population evidence: CEPTS3.2-S-008 defines the applicable population boundary for the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" within that scope.",
        "sample evidence: CEPTS3.2-S-008 identifies the sample selected from that defined population and the selection basis for the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\", or confirms that all population members were assessed.",
        "assessment_date evidence: CEPTS3.2-S-008 records the assessment date, time, and timezone for the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\".",
        "evidence_date evidence: CEPTS3.2-S-008 records the evidence-collection date, time, and timezone separately from the assessment date for the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\".",
        "tool evidence: CEPTS3.2-S-008 names the tool and version or documented manual method used to produce the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\".",
        "provenance evidence: CEPTS3.2-S-008 links source artifacts, the source locator, and the cited ESAF requirement for the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\". Provision-specific record set: A dated integrity-protected retention index identifies the Certifying Body, AI assessment scope, population and sample, calculation record, source, retention period, provenance, and any exception.",
        "exception evidence: CEPTS3.2-S-008 records that no exception affected the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\", or identifies the exception approval and disposition.",
        "delivery_partner_discretion evidence: CEPTS3.2-S-008 records whether Delivery Partner discretion affected the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\", identifying the applicable choice, method, or approval, or the basis for none.",
        "point_in_time_status evidence: CEPTS3.2-S-008 limits the observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" to the assessment and evidence dates, defined population, and selected sample; later state is excluded."
      ],
      "known_gaps": [
        "Retention of the calculation record does not establish its creation or accuracy, protection beyond the recorded controls, other record duties, or later conditions."
      ],
      "prohibited_inferences": [
        "CEPTS3.2-S-008 | prohibit implementation: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" does not establish control implementation for the cited CMP-110 outcome.",
        "CEPTS3.2-S-008 | prohibit effectiveness: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" does not establish control effectiveness for the cited CMP-110 outcome.",
        "CEPTS3.2-S-008 | prohibit sufficiency: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" is not sufficient evidence for the cited CMP-110 outcome.",
        "CEPTS3.2-S-008 | prohibit compliance: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" does not establish ESAF compliance for the cited CMP-110 outcome.",
        "CEPTS3.2-S-008 | prohibit certification: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" does not authorize or establish certification for the cited CMP-110 outcome.",
        "CEPTS3.2-S-008 | prohibit equivalence: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" is not equivalent for the cited CMP-110 outcome.",
        "CEPTS3.2-S-008 | prohibit continuous_assurance: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" does not provide continuous assurance for the cited CMP-110 outcome.",
        "CEPTS3.2-S-008 | prohibit population_wide_coverage: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" does not establish population-wide coverage for the cited CMP-110 outcome.",
        "CEPTS3.2-S-008 | prohibit current_scheme_coverage: The observed result \"the dated retention record shows that sample-size calculation evidence was retained for at least the certificate lifetime\" does not establish current-scheme coverage for the cited CMP-110 outcome."
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
# CEPTS3.2-S-008

Draft derivative external-to-ESAF evidence analysis for the cited Cyber Essentials Plus v3.2 provision.
