---
{
  "schema_version": "1.0.0",
  "record_id": "cepts32-m-010",
  "mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
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
      "direction": "external_to_esaf",
      "coverage": "narrow",
      "confidence": "high",
      "rationale": "External observation: the dated pre-test record shows that issues found during the listed checks were resolved before testing began. Supported ESAF outcome: AUD-130 requires AI assessment findings to be documented, classified, assigned, prioritized, remediated, escalated, retested, closed, and retained according to the named governance factors. Conditions only narrow this supported claim; they do not create either outcome.",
      "conditions": [
        "{\"condition\":\"actor\",\"evidence_references\":[\"relationship:expected_evidence:0\",\"record:external_metadata\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"scope\",\"evidence_references\":[\"relationship:expected_evidence:1\",\"record:context\",\"manifest:AUD-130#requirement\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"population\",\"evidence_references\":[\"relationship:expected_evidence:2\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"sample\",\"evidence_references\":[\"relationship:expected_evidence:3\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"assessment_date\",\"evidence_references\":[\"relationship:expected_evidence:4\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"evidence_date\",\"evidence_references\":[\"relationship:expected_evidence:5\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"tool\",\"evidence_references\":[\"relationship:expected_evidence:6\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"provenance\",\"evidence_references\":[\"relationship:expected_evidence:7\",\"record:source_locator\",\"manifest:AUD-130#requirement\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"exception\",\"evidence_references\":[\"relationship:expected_evidence:8\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"delivery_partner_discretion\",\"evidence_references\":[\"relationship:expected_evidence:9\"],\"status\":\"SATISFIED\"}",
        "{\"condition\":\"point_in_time_status\",\"evidence_references\":[\"relationship:expected_evidence:10\",\"relationship:known_gaps:0\"],\"status\":\"SATISFIED\"}"
      ],
      "expected_evidence": [
        "actor evidence: CEPTS3.2-M-010 identifies the Assessor responsible for the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\".",
        "scope evidence: CEPTS3.2-M-010 identifies the in-scope AI subject for the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\": Resolve issues found during the listed pre-test checks before Plus testing commences.",
        "population evidence: CEPTS3.2-M-010 defines the applicable population boundary for the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" within that scope.",
        "sample evidence: CEPTS3.2-M-010 identifies the sample selected from that defined population and the selection basis for the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\", or confirms that all population members were assessed.",
        "assessment_date evidence: CEPTS3.2-M-010 records the assessment date, time, and timezone for the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\".",
        "evidence_date evidence: CEPTS3.2-M-010 records the evidence-collection date, time, and timezone separately from the assessment date for the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\".",
        "tool evidence: CEPTS3.2-M-010 names the tool and version or documented manual method used to produce the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\".",
        "provenance evidence: CEPTS3.2-M-010 links source artifacts, the source locator, and the cited ESAF requirement for the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\". Provision-specific record set: A dated finding record identifies the Assessor, affected AI assessment scope and population, issue, owner, action, retest, closure, source artifacts, and any exception.",
        "exception evidence: CEPTS3.2-M-010 records that no exception affected the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\", or identifies the exception approval and disposition.",
        "delivery_partner_discretion evidence: CEPTS3.2-M-010 records whether Delivery Partner discretion affected the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\", identifying the applicable choice, method, or approval, or the basis for none.",
        "point_in_time_status evidence: CEPTS3.2-M-010 limits the observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" to the assessment and evidence dates, defined population, and selected sample; later state is excluded."
      ],
      "known_gaps": [
        "Issue resolution alone does not establish every required finding activity, risk factor, root-cause analysis, or later state."
      ],
      "prohibited_inferences": [
        "CEPTS3.2-M-010 | prohibit implementation: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" does not establish control implementation for the cited AUD-130 outcome.",
        "CEPTS3.2-M-010 | prohibit effectiveness: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" does not establish control effectiveness for the cited AUD-130 outcome.",
        "CEPTS3.2-M-010 | prohibit sufficiency: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" is not sufficient evidence for the cited AUD-130 outcome.",
        "CEPTS3.2-M-010 | prohibit compliance: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" does not establish ESAF compliance for the cited AUD-130 outcome.",
        "CEPTS3.2-M-010 | prohibit certification: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" does not authorize or establish certification for the cited AUD-130 outcome.",
        "CEPTS3.2-M-010 | prohibit equivalence: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" is not equivalent for the cited AUD-130 outcome.",
        "CEPTS3.2-M-010 | prohibit continuous_assurance: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" does not provide continuous assurance for the cited AUD-130 outcome.",
        "CEPTS3.2-M-010 | prohibit population_wide_coverage: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" does not establish population-wide coverage for the cited AUD-130 outcome.",
        "CEPTS3.2-M-010 | prohibit current_scheme_coverage: The observed result \"the dated pre-test record shows that issues found during the listed checks were resolved before testing began\" does not establish current-scheme coverage for the cited AUD-130 outcome."
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
# CEPTS3.2-M-010

Draft derivative external-to-ESAF evidence analysis for the cited Cyber Essentials Plus v3.2 provision.
