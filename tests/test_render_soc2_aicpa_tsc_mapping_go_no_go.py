from __future__ import annotations

import copy
import unittest

from tools.render_soc2_aicpa_tsc_mapping_go_no_go import derive_decision, validate_matrix


GATES = (
    "source_identity_and_drift", "authorized_source_artifact", "publication_rights",
    "provision_inventory", "semantic_and_normative_feasibility",
    "esaf_1600_and_schema_fit", "mapper_and_reviewer_readiness", "overclaiming_controls",
)


def matrix(statuses=None, blockers=None, positive=True, findings=None):
    statuses = statuses or {name: "PASS" for name in GATES}
    blockers = blockers or []
    return {
        "blockers": blockers,
        "gates": [{"blocker_ids": [b["blocker_id"] for b in blockers if b["gate"] == name],
                   "evidence_references": ["symbolic:fixture"], "gate": name,
                   "rationale": "Reviewed", "status": statuses[name]} for name in GATES],
        "mapping_contract": {"direction": "esaf_to_external", "excluded_direction": "external_to_esaf",
            "directional_question": "Question", "granularity": "requirement", "positive_feasibility_probe": positive,
            "scope": "complete_publication"},
        "nonclaims": ["No compliance claim"], "reconsideration_sequence": ["Reassess evidence"],
        "recorded_decision": "GO", "review_findings": findings or {"open_critical": 0, "open_important": 0},
        "review_identifier": "review-1", "reviewer_contract": {"fixture": True}, "rights_review": {"commit": "a"*40, "path": "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md", "sha256": "b"*64},
        "schema_version": "1.0.0", "source_oracle": {"path": "docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-source-readiness-oracle.json", "sha256": "2de8f16cb962a8f5edd3c4e77d6745360ba44cc5d33106a45cad0d46c5a8ac4f"},
    }


def blocker(identifier, gate, remediation):
    return {"blocker_id": identifier, "category": "evidence", "gate": gate,
        "missing_evidence": "Evidence", "owner": "Owner", "reconsideration_trigger": "Trigger",
        "reentry_test": "Test", "remediation": remediation}


class Soc2ReadinessTests(unittest.TestCase):
    def test_go_is_rejected_without_affirmative_source_rights_and_inventory_evidence(self):
        # The matrix can claim every gate passed, but it cannot override the
        # pinned source oracle and rights review's actual HOLD state.
        with self.assertRaisesRegex(ValueError, "source artifact retrieval"):
            derive_decision(matrix(), verify_source_digest=False)

    def test_go_still_requires_positive_probe_and_no_open_findings(self):
        m = matrix(positive=False)
        m["recorded_decision"] = "HOLD"
        with self.assertRaises(ValueError):
            validate_matrix(m, verify_source_digest=False)

    def test_hold_requires_reconsiderable_blocker_covering_each_blocked_gate(self):
        gate = GATES[1]
        b = blocker("B1", gate, "reconsiderable")
        m = matrix({**{g: "PASS" for g in GATES}, gate: "BLOCKED"}, [b])
        m["recorded_decision"] = "HOLD"
        self.assertEqual(derive_decision(m, verify_source_digest=False), "HOLD")
        m["blockers"][0]["remediation"] = "terminal"
        with self.assertRaisesRegex(ValueError, "NO_GO"):
            validate_matrix(m, verify_source_digest=False)

    def test_no_go_requires_terminal_blocker_and_all_blocked_gates_covered(self):
        gate = GATES[2]
        b = blocker("B1", gate, "terminal")
        m = matrix({**{g: "PASS" for g in GATES}, gate: "BLOCKED"}, [b])
        m["recorded_decision"] = "NO_GO"
        self.assertEqual(derive_decision(m, verify_source_digest=False), "NO_GO")
        m["blockers"][0]["remediation"] = "reconsiderable"
        with self.assertRaises(ValueError):
            validate_matrix(m, verify_source_digest=False)

    def test_rejects_orphan_blocker_and_unknown_keys(self):
        m = matrix()
        m["blockers"] = [blocker("B1", GATES[0], "reconsiderable")]
        with self.assertRaises(ValueError):
            validate_matrix(m, verify_source_digest=False)
        m = matrix()
        m["surprise"] = True
        with self.assertRaises(ValueError):
            validate_matrix(m, verify_source_digest=False)
