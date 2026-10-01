---
{
  "schema_version": "1.0.0",
  "record_id": "airmf-manage-2-2",
  "mapping_set_id": "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0",
  "status": "draft",
  "external_provision_id": "MANAGE-2.2",
  "granularity": "requirement",
  "context": {
    "mode": "paraphrase",
    "summary": "Mechanisms are in place and applied to sustain the value of deployed AI systems."
  },
  "source_locator": {
    "official_url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "locator": "NIST AI RMF 1.0 Core, subcategory MANAGE-2.2"
  },
  "disposition": "mapped",
  "relationships": [
    {
      "esaf_control_id": "STR-110",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "substantial",
      "confidence": "high",
      "rationale": "STR-110 requires periodically evaluating intended outcomes, costs, material adverse effects, and continuation criteria for each production AI capability.",
      "conditions": [
        "The AI system is a production capability under STR-110."
      ],
      "expected_evidence": [
        "Periodic value-realization evaluations and continuation decisions."
      ],
      "known_gaps": [
        "STR-110 evaluates value; operational sustainment depends on OPS controls."
      ]
    },
    {
      "esaf_control_id": "OPS-100",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "partial",
      "confidence": "high",
      "rationale": "OPS-100 requires assigning a service owner and approved objectives for availability, performance, quality, support, security, recovery, cost, monitoring, escalation, and maintenance.",
      "conditions": [
        "Service objectives sustain operational value of the deployed AI system."
      ],
      "expected_evidence": [
        "Service ownership and approved operational objectives."
      ],
      "known_gaps": [
        "OPS-100 sets operational objectives; it does not measure business value realization."
      ]
    },
    {
      "esaf_control_id": "OPS-140",
      "esaf_control_version": "0.1.0",
      "relationship": "partially_supports",
      "direction": "esaf_to_external",
      "coverage": "narrow",
      "confidence": "medium",
      "rationale": "OPS-140 requires monitoring and managing AI availability, latency, throughput, quality, capacity, utilization, demand, cost, and dependency performance against approved objectives.",
      "conditions": [
        "Operational performance management sustains deployed-system value."
      ],
      "expected_evidence": [
        "Performance/capacity management records against objectives."
      ],
      "known_gaps": [
        "OPS-140 is operational performance, not full value sustainment including business outcomes."
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
      "change": "Created the draft NIST AI RMF 1.0 MANAGE-2.2 mapping record."
    }
  ]
}
---
# MANAGE-2.2

Draft derivative mapping analysis for the cited NIST AI RMF 1.0 Core subcategory.
