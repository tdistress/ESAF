from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.render_pci_dss_mapping_go_no_go import (
    derive_decision,
    render,
    validate_matrix,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-07-25-pci-dss-mapping-readiness-matrix.json"
)
ORACLE = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-07-25-pci-dss-source-readiness-oracle.json"
)
REVIEW = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-07-25-pci-dss-mapping-go-no-go-review.md"
)
TOOL = ROOT / "tools" / "render_pci_dss_mapping_go_no_go.py"

GATES = (
    "source_identity_and_drift",
    "authorized_source_artifact",
    "publication_rights",
    "provision_inventory",
    "semantic_and_normative_feasibility",
    "esaf_1600_and_schema_fit",
    "mapper_and_reviewer_readiness",
    "overclaiming_controls",
)
EXPECTED_STATUSES = {
    "source_identity_and_drift": "PASS",
    "authorized_source_artifact": "BLOCKED",
    "publication_rights": "BLOCKED",
    "provision_inventory": "BLOCKED",
    "semantic_and_normative_feasibility": "BLOCKED",
    "esaf_1600_and_schema_fit": "PASS",
    "mapper_and_reviewer_readiness": "BLOCKED",
    "overclaiming_controls": "PASS",
}
QUESTION = (
    "Does exact normative ESAF control requirement text directly support, "
    "partially support, or establish a prerequisite for the outcome required by "
    "one authorized, publishable PCI DSS v4.0.1 numbered requirement or "
    "sub-requirement, with each relationship's conditions, expected evidence, "
    "and known gaps recorded independently, without implying PCI DSS compliance, "
    "assessment, equivalence, certification, authorization, or endorsement?"
)


class PciDssMappingGoNoGoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix_bytes = MATRIX.read_bytes()
        self.matrix = json.loads(self.matrix_bytes)

    def test_matrix_is_canonical_one_line_lf_json(self) -> None:
        expected = (
            json.dumps(
                self.matrix,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
            + b"\n"
        )
        self.assertEqual(self.matrix_bytes, expected)
        self.assertNotIn(b"\r", self.matrix_bytes)
        self.assertEqual(self.matrix_bytes.count(b"\n"), 1)

    def test_matrix_contract_is_closed_and_source_digest_is_live(self) -> None:
        self.assertEqual(
            set(self.matrix),
            {
                "blockers",
                "gates",
                "mapping_contract",
                "nonclaims",
                "reconsideration_sequence",
                "recorded_decision",
                "review_findings",
                "review_identifier",
                "reviewer_contract",
                "rights_review",
                "schema_version",
                "source_oracle",
            },
        )
        self.assertEqual(
            set(self.matrix["source_oracle"]),
            {"path", "sha256"},
        )
        self.assertEqual(
            self.matrix["source_oracle"]["path"],
            "docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json",
        )
        self.assertEqual(
            self.matrix["source_oracle"]["sha256"],
            hashlib.sha256(ORACLE.read_bytes()).hexdigest(),
        )
        validate_matrix(self.matrix)

    def test_gate_order_statuses_evidence_and_blocker_coverage_are_exact(self) -> None:
        self.assertEqual([gate["gate"] for gate in self.matrix["gates"]], list(GATES))
        self.assertEqual(
            {gate["gate"]: gate["status"] for gate in self.matrix["gates"]},
            EXPECTED_STATUSES,
        )
        blockers = {item["blocker_id"]: item for item in self.matrix["blockers"]}
        self.assertEqual(len(blockers), len(self.matrix["blockers"]))
        for gate in self.matrix["gates"]:
            self.assertEqual(
                set(gate),
                {"blocker_ids", "evidence_references", "gate", "rationale", "status"},
            )
            self.assertIn(gate["status"], {"PASS", "BLOCKED"})
            self.assertTrue(gate["rationale"].strip())
            self.assertTrue(gate["evidence_references"])
            self.assertTrue(all(reference.strip() for reference in gate["evidence_references"]))
            if gate["status"] == "PASS":
                self.assertEqual(gate["blocker_ids"], [])
            else:
                self.assertTrue(gate["blocker_ids"])
                for blocker_id in gate["blocker_ids"]:
                    self.assertEqual(blockers[blocker_id]["gate"], gate["gate"])

        for blocker in self.matrix["blockers"]:
            self.assertEqual(
                set(blocker),
                {
                    "blocker_id",
                    "category",
                    "gate",
                    "missing_evidence",
                    "owner",
                    "reconsideration_trigger",
                    "reentry_test",
                },
            )
            self.assertTrue(all(str(value).strip() for value in blocker.values()))
            self.assertIn(
                "ESAF Project Maintainer",
                blocker["owner"],
            )

    def test_matrix_binds_direction_scope_granularity_and_question(self) -> None:
        contract = self.matrix["mapping_contract"]
        self.assertEqual(
            set(contract),
            {
                "direction",
                "directional_question",
                "excluded_direction",
                "granularity",
                "positive_feasibility_probe",
                "scope",
            },
        )
        self.assertEqual(contract["direction"], "esaf_to_external")
        self.assertEqual(contract["excluded_direction"], "external_to_esaf")
        self.assertEqual(contract["scope"], "complete_publication")
        self.assertEqual(
            contract["granularity"],
            "finest_authorized_publishable_numbered_requirement_or_sub_requirement_identifier",
        )
        self.assertEqual(contract["directional_question"], QUESTION)
        self.assertIs(contract["positive_feasibility_probe"], False)

    def test_reviewer_contract_requires_qualified_independent_exact_sha_reviews(self) -> None:
        contract = self.matrix["reviewer_contract"]
        self.assertEqual(
            set(contract),
            {
                "approver",
                "candidate_change_requires_redispatch",
                "dual_role_requires_owner_approval",
                "mapper",
                "review_record_requirements",
                "reviewers",
                "separate_exact_candidate_reviews",
            },
        )
        self.assertEqual(
            contract["mapper"],
            {
                "authorized_source_access_required": True,
                "experience_required": ["PCI DSS v4.0.1", "ESAF-1600"],
                "named_person_required": True,
                "self_review_prohibited": True,
            },
        )
        reviewers = {reviewer["role"]: reviewer for reviewer in contract["reviewers"]}
        self.assertEqual(
            set(reviewers),
            {
                "pci_subject_matter",
                "esaf_specification_and_mapping",
                "publication_rights",
                "security_and_overclaiming",
            },
        )
        self.assertEqual(
            reviewers["pci_subject_matter"]["qualification"],
            "current QSA or owner-approved equivalent PCI reviewer",
        )
        for reviewer in reviewers.values():
            self.assertTrue(reviewer["independent_from_mapper"])
        self.assertEqual(
            set(contract["review_record_requirements"]),
            {
                "identity",
                "role",
                "qualification_or_relevant_experience",
                "authorized_source_access_attestation",
                "attributable_attestation",
                "review_date",
                "exact_candidate_sha",
                "artifact_digests",
                "findings",
                "findings_disposition",
            },
        )
        self.assertEqual(
            contract["separate_exact_candidate_reviews"],
            ["inventory_and_specification", "security_and_overclaiming"],
        )
        self.assertIs(contract["candidate_change_requires_redispatch"], True)

    def test_decision_is_derived_and_inconsistent_matrices_fail_closed(self) -> None:
        self.assertEqual(derive_decision(self.matrix), "HOLD")
        self.assertEqual(self.matrix["recorded_decision"], "HOLD")

        ready = copy.deepcopy(self.matrix)
        ready["gates"] = [
            {**gate, "status": "PASS", "blocker_ids": []}
            for gate in ready["gates"]
        ]
        ready["blockers"] = []
        ready["mapping_contract"]["positive_feasibility_probe"] = True
        ready["recorded_decision"] = "GO"
        validate_matrix(ready, verify_source_digest=False)
        self.assertEqual(derive_decision(ready), "GO")

        mutations = []
        invalid_status = copy.deepcopy(self.matrix)
        invalid_status["gates"][0]["status"] = "UNKNOWN"
        mutations.append(invalid_status)

        unknown_key = copy.deepcopy(self.matrix)
        unknown_key["unexpected"] = True
        mutations.append(unknown_key)

        duplicate_blocker = copy.deepcopy(self.matrix)
        duplicate_blocker["blockers"].append(copy.deepcopy(duplicate_blocker["blockers"][0]))
        mutations.append(duplicate_blocker)

        incomplete_blocker = copy.deepcopy(self.matrix)
        incomplete_blocker["blockers"][0]["missing_evidence"] = ""
        mutations.append(incomplete_blocker)

        incomplete_evidence = copy.deepcopy(self.matrix)
        incomplete_evidence["gates"][0]["evidence_references"] = []
        mutations.append(incomplete_evidence)

        uncovered_gate = copy.deepcopy(self.matrix)
        uncovered_gate["gates"][1]["blocker_ids"] = []
        mutations.append(uncovered_gate)

        contradictory_decision = copy.deepcopy(self.matrix)
        contradictory_decision["recorded_decision"] = "GO"
        mutations.append(contradictory_decision)

        malformed_decision = copy.deepcopy(self.matrix)
        malformed_decision["recorded_decision"] = "NO_GO"
        mutations.append(malformed_decision)

        no_positive_probe = copy.deepcopy(ready)
        no_positive_probe["mapping_contract"]["positive_feasibility_probe"] = False
        mutations.append(no_positive_probe)

        open_important = copy.deepcopy(ready)
        open_important["review_findings"]["open_important"] = 1
        mutations.append(open_important)

        for mutation in mutations:
            with self.subTest(mutation=mutations.index(mutation)):
                with self.assertRaises(ValueError):
                    validate_matrix(mutation, verify_source_digest=False)

        stale_digest = copy.deepcopy(self.matrix)
        stale_digest["source_oracle"]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            validate_matrix(stale_digest)

    def test_render_is_deterministic_and_covers_hold_contract(self) -> None:
        rendered = render(self.matrix)
        self.assertEqual(rendered, render(copy.deepcopy(self.matrix)))
        self.assertEqual(REVIEW.read_text(encoding="utf-8"), rendered)
        self.assertIn("# PCI DSS mapping readiness decision", rendered)
        self.assertIn("**Decision:** `HOLD`", rendered)
        self.assertIn("## Exact directional question", rendered)
        self.assertIn("## Source boundary", rendered)
        self.assertIn("## Gate results", rendered)
        self.assertIn("## Blockers", rendered)
        self.assertIn("## Future mapper and reviewer requirements", rendered)
        self.assertIn("## Reconsideration sequence", rendered)
        self.assertIn("## Nonclaims", rendered)
        self.assertIn("`external_to_esaf` is excluded", rendered)
        for gate in GATES:
            self.assertIn(f"| `{gate}` |", rendered)
        for blocker in self.matrix["blockers"]:
            self.assertIn(f"| `{blocker['blocker_id']}` |", rendered)

    def test_cli_write_check_and_operational_errors(self) -> None:
        check = subprocess.run(
            [sys.executable, str(TOOL), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(check.returncode, 0, check.stderr)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "review.md"
            write = subprocess.run(
                [sys.executable, str(TOOL), "--write", "--output", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(write.returncode, 0, write.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), render(self.matrix))

            missing = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "--check",
                    "--matrix",
                    str(Path(directory) / "missing.json"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(missing.returncode, 2)
            self.assertIn("error:", missing.stderr)


if __name__ == "__main__":
    unittest.main()
