---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-govern-2-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "GOVERN-2.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Personnel and partners receive AI risk-management training enabling duties consistent with related policies and agreements."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory GOVERN-2.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "EDU-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "EDU-110 requires defining, assessing, maintaining, and evidencing AI competency requirements for roles that design, develop, validate, approve, operate, monitor, secure, govern, audit, or materially use AI capabilities.",
      "conditions": [
        "Role competency requirements include AI risk-management duties for in-scope personnel."
      ],
      "expected_evidence": [
        "Role competency matrices and completion evidence for AI risk-related roles."
      ],
      "known_gaps": [
        "EDU-110 addresses personnel roles; it does not expressly require partner/third-party AI risk training."
      ]
    },
    {
      "esaf_control_id": "EDU-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "EDU-140 requires role-specific education for executives, governing authorities, accountable owners, risk acceptors, reviewers, and auditors on AI strategy, duties, risk, evidence, limitations, incidents, obligations, and decision rights.",
      "conditions": [
        "Executive and risk-acceptor education is in scope for the subcategory's leadership duties."
      ],
      "expected_evidence": [
        "Executive/governance education records covering AI risk duties."
      ],
      "known_gaps": [
        "EDU-140 does not train all personnel or partners."
      ]
    },
    {
      "esaf_control_id": "EDU-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "EDU-100 requires baseline AI literacy covering capabilities, limitations, accountability, safe use, data protection, verification, bias, escalation, and applicable policy for personnel whose work can affect or be affected by AI.",
      "conditions": [
        "Baseline literacy is provided to personnel in AI-affected roles."
      ],
      "expected_evidence": [
        "AI literacy curriculum and completion records."
      ],
      "known_gaps": [
        "EDU-100 is baseline literacy, not specialized AI risk-management training for all risk roles."
      ]
    }
  ],
  "mapper": {
    "id": "esaf-project-owner",
    "date": "2026-10-01"
  },
  "change_history": [
    {
      "version": "0.1.0",
      "date": "2026-10-01",
      "change": "Created the draft NIST AI RMF 1.0 GOVERN-2.2 mapping record."
    }
  ]
}
---
# GOVERN-2.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
