from __future__ import annotations

import copy
import hashlib
import io
import json
import posixpath
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from tools import render_soc2_aicpa_tsc_mapping_go_no_go as renderer
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
        with self.assertRaisesRegex(ValueError, "evidence manifest"):
            derive_decision(matrix(), verify_source_digest=False)

    def test_go_requires_supported_feasibility_and_exact_candidate_attestations(self):
        with tempfile.TemporaryDirectory() as directory:
            oracle_path = Path(directory) / "oracle.json"
            rights_path = Path(directory) / "rights.md"
            oracle_path.write_text(json.dumps({
                "source_artifact": {"state": "retrieved", "sha256": "a" * 64, "byte_length": 12},
                "access": {"source_bytes_retrieved": True},
                "inventory": {"created": True, "inventory_sha256": "b" * 64},
                "boundary": {"document_specific_notice_inspected": True},
            }), encoding="utf-8")
            rights_path.write_text("**Disposition:** `PASS`\n", encoding="utf-8")
            source_ref = matrix()["source_oracle"]["path"]
            resolver = lambda value, _label: oracle_path if value == source_ref else rights_path
            with patch("tools.render_soc2_aicpa_tsc_mapping_go_no_go._repo_path", side_effect=resolver):
                with self.assertRaisesRegex(ValueError, "evidence manifest"):
                    derive_decision(matrix(), verify_source_digest=False)

    def test_go_still_requires_positive_probe_and_no_open_findings(self):
        m = matrix(positive=False)
        m["recorded_decision"] = "HOLD"
        with self.assertRaises(ValueError):
            validate_matrix(m, verify_source_digest=False)


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _subject_digest(feasibility, inputs):
    """Canonical digest: UTF-8 JSON, sorted keys, compact separators, no reviews."""
    pairs = [{"path": posixpath.normpath(item["path"]), "sha256": item["sha256"]} for item in inputs]
    pairs.sort(key=lambda item: item["path"])
    subject = {"feasibility": feasibility, "inputs": pairs}
    encoded = json.dumps(subject, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class SyntheticManifestFixture:
    """Temporary repository containing only synthetic contract evidence."""

    def __init__(self, root, *, positive=True, ready_sources=False):
        self.root = Path(root)
        for relative, payload in {
            "source/oracle.json": b'{"synthetic": "oracle"}\n',
            "inventory/inventory.json": b'{"synthetic": "inventory"}\n',
            "probe/probe.json": b'{"synthetic": "probe"}\n',
        }.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        self.inputs = [
            {"category": category, "path": relative, "sha256": _sha256(self.root / relative)}
            for category, relative in (
                ("source", "source/oracle.json"),
                ("inventory", "inventory/inventory.json"),
                ("probe", "probe/probe.json"),
            )
        ] if positive else []
        self.feasibility = {
            "blocker_ids": [] if positive else ["SOC2-TSC-READINESS-B004"],
            "method": "Synthetic bounded feasibility probe",
            "rationale": "Synthetic evidence supports the declared feasibility state.",
            "scope": "synthetic fixture only",
            "status": "positive" if positive else "not_evidenced",
        }
        self.manifest = {
            "schema_version": "1.0.0",
            "feasibility": copy.deepcopy(self.feasibility),
            "evidence_inputs": copy.deepcopy(self.inputs),
            "evidence_subject_sha256": _subject_digest(self.feasibility, self.inputs),
            "review": {
                "status": "complete" if positive else "not_completed",
                "rationale": "Two independent synthetic reviews completed." if positive else "No qualified reviewers are evidenced.",
                "blocker_ids": [] if positive else ["SOC2-TSC-READINESS-B005"],
                "attestations": [],
            },
        }
        if positive:
            self.manifest["review"]["attestations"] = [self._attestation(role, identity) for role, identity in (
                ("inventory_and_specification", "reviewer-spec"),
                ("security_and_overclaiming", "reviewer-security"),
            )]
        self.manifest_path = self.root / "evidence/manifest.json"
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.write_manifest()
        self.matrix = self._matrix()
        oracle_path = self.root / "docs/superpowers/specs/2026-10-02-soc2-aica-tsc-source-readiness-oracle.json"
        oracle_path.parent.mkdir(parents=True, exist_ok=True)
        oracle_path.write_text(json.dumps({"source_artifact": ({"state": "retrieved", "sha256": "a" * 64,
                                                                  "byte_length": 12} if ready_sources else {"state": "not_retrieved"}),
                                           "access": {"source_bytes_retrieved": ready_sources},
                                           "inventory": ({"created": True, "inventory_sha256": "b" * 64} if ready_sources else {"created": False}),
                                           "boundary": {"document_specific_notice_inspected": ready_sources}}), encoding="utf-8")
        rights_path = self.root / "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md"
        rights_path.parent.mkdir(parents=True, exist_ok=True)
        rights_path.write_text("**Disposition:** `PASS`\n" if ready_sources else "**Disposition:** `HOLD`\n", encoding="utf-8")
        self.matrix["source_oracle"] = {"path": oracle_path.relative_to(self.root).as_posix(), "sha256": _sha256(oracle_path)}
        self.matrix["rights_review"]["sha256"] = _sha256(rights_path)

    def _attestation(self, role, identity):
        return {
            "identity": identity,
            "role": role,
            "qualification": "Qualified for synthetic contract review",
            "authorized_source_access": True,
            "independence": True,
            "conflict_disposition": "none",
            "review_date": "2026-10-05",
            "disposition": "PASS",
            "evidence_subject_sha256": self.manifest["evidence_subject_sha256"],
            "findings": {"open_critical": 0, "open_important": 0},
        }

    def write_manifest(self):
        self.manifest_path.write_text(json.dumps(self.manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    def _matrix(self):
        statuses = {name: "PASS" for name in GATES}
        blockers = []
        if not self.inputs:
            for gate, identifier in (("semantic_and_normative_feasibility", "SOC2-TSC-READINESS-B004"),
                                     ("mapper_and_reviewer_readiness", "SOC2-TSC-READINESS-B005")):
                statuses[gate] = "BLOCKED"
                blockers.append(blocker(identifier, gate, "reconsiderable"))
        m = matrix(statuses, blockers, positive=False if not self.inputs else True)
        m["recorded_decision"] = "HOLD" if blockers else "GO"
        m["mapping_contract"].pop("positive_feasibility_probe")
        m["mapping_contract"]["evidence_manifest"] = {
            "path": "evidence/manifest.json", "sha256": _sha256(self.manifest_path),
        }
        m["mapping_contract"]["mapper_identity"] = "mapper-1"
        return m


class Soc2EvidenceManifestContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.fixture = SyntheticManifestFixture(self.temp.name)
        self.root_patch = patch.object(renderer, "ROOT", Path(self.temp.name))
        self.root_patch.start()

    def tearDown(self):
        self.root_patch.stop()
        self.temp.cleanup()

    def validate_manifest(self, manifest=None, matrix_value=None, *, refresh_subject=True):
        candidate = manifest or self.fixture.manifest
        matrix_candidate = copy.deepcopy(matrix_value or self.fixture.matrix)
        if manifest is not None:
            if refresh_subject:
                subject = _subject_digest(candidate["feasibility"], candidate["evidence_inputs"])
                candidate["evidence_subject_sha256"] = subject
                for attestation in candidate["review"]["attestations"]:
                    attestation["evidence_subject_sha256"] = subject
            self.fixture.manifest_path.write_text(json.dumps(candidate, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            matrix_candidate["mapping_contract"]["evidence_manifest"]["sha256"] = _sha256(self.fixture.manifest_path)
        return renderer.validate_manifest(
            candidate,
            matrix_candidate,
            repository_root=self.fixture.root,
            mapper_identity="mapper-1",
        )

    def run_cli(self, matrix_value):
        matrix_path = self.fixture.root / "matrix.json"
        matrix_path.write_text(json.dumps(matrix_value), encoding="utf-8")
        error = io.StringIO()
        with redirect_stderr(error):
            status = renderer.main(["--matrix", str(matrix_path), "--output", str(self.fixture.root / "out.md")])
        return status, error.getvalue()

    def assert_cli_validation_error(self, matrix_value, message):
        status, error = self.run_cli(matrix_value)
        self.assertEqual(status, 2)
        self.assertTrue(error.startswith("error:"), error)
        self.assertNotIn("Traceback", error)
        self.assertIn(message, error)

    def test_cli_reports_wrong_type_manifest_category_without_traceback(self):
        self.fixture.manifest["evidence_inputs"][0]["category"] = ["source"]
        self.fixture.write_manifest()
        self.fixture.matrix["mapping_contract"]["evidence_manifest"]["sha256"] = _sha256(self.fixture.manifest_path)
        self.assert_cli_validation_error(self.fixture.matrix, "category allowlist")

    def test_cli_reports_wrong_type_reviewer_role_without_traceback(self):
        self.fixture.manifest["review"]["attestations"][0]["role"] = ["inventory_and_specification"]
        self.fixture.write_manifest()
        self.fixture.matrix["mapping_contract"]["evidence_manifest"]["sha256"] = _sha256(self.fixture.manifest_path)
        self.assert_cli_validation_error(self.fixture.matrix, "reviewer roles")

    def test_cli_reports_wrong_type_manifest_reference_without_traceback(self):
        self.fixture.matrix["mapping_contract"]["evidence_manifest"]["path"] = ["evidence/manifest.json"]
        self.assert_cli_validation_error(self.fixture.matrix, "evidence manifest path")

    def test_cli_reports_wrong_type_gate_collection_without_traceback(self):
        self.fixture = SyntheticManifestFixture(self.temp.name, positive=False)
        self.fixture.matrix["gates"] = {"gate": "semantic_and_normative_feasibility"}
        self.assert_cli_validation_error(self.fixture.matrix, "gate")

    def test_complete_not_evidenced_manifest_is_valid_and_keeps_hold(self):
        fixture = SyntheticManifestFixture(self.temp.name, positive=False)
        self.fixture = fixture
        self.assertEqual(fixture.manifest["feasibility"]["status"], "not_evidenced")
        self.assertTrue(fixture.manifest["feasibility"]["rationale"])
        self.assertEqual(fixture.manifest["review"]["status"], "not_completed")
        self.assertTrue(fixture.manifest["review"]["rationale"])
        self.assertEqual(fixture.manifest["evidence_inputs"], [])
        self.assertEqual(fixture.manifest["review"]["attestations"], [])
        self.assertEqual(fixture.manifest["feasibility"]["blocker_ids"], ["SOC2-TSC-READINESS-B004"])
        self.assertEqual(fixture.manifest["review"]["blocker_ids"], ["SOC2-TSC-READINESS-B005"])
        matrix_blockers = {gate["gate"]: gate["blocker_ids"] for gate in fixture.matrix["gates"]}
        self.assertEqual(fixture.manifest["feasibility"]["blocker_ids"], matrix_blockers["semantic_and_normative_feasibility"])
        self.assertEqual(fixture.manifest["review"]["blocker_ids"], matrix_blockers["mapper_and_reviewer_readiness"])
        self.assertEqual(self.validate_manifest(), "not_evidenced")
        self.assertEqual(renderer.derive_decision(
            fixture.matrix, manifest=fixture.manifest, repository_root=fixture.root,
            verify_source_digest=False), "HOLD")
        self.assertEqual(renderer.derive_decision(
            fixture.matrix, repository_root=fixture.root, verify_source_digest=False), "HOLD")

    def test_positive_manifest_digest_and_two_distinct_roles_validate(self):
        result = self.validate_manifest()
        self.assertEqual(result, "positive")
        roles = [a["role"] for a in self.fixture.manifest["review"]["attestations"]]
        self.assertEqual(roles, ["inventory_and_specification", "security_and_overclaiming"])
        self.assertEqual(len({a["identity"] for a in self.fixture.manifest["review"]["attestations"]}), 2)

    def test_changed_input_bytes_fail_digest_validation(self):
        (self.fixture.root / self.fixture.inputs[0]["path"]).write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "input.*digest|digest.*input"):
            self.validate_manifest()

    def test_input_category_cannot_reference_another_category_root(self):
        generic = self.fixture.root / "inputs/inventory.json"
        generic.parent.mkdir(parents=True, exist_ok=True)
        generic.write_bytes((self.fixture.root / "inventory/inventory.json").read_bytes())
        bad = copy.deepcopy(self.fixture.manifest)
        bad["evidence_inputs"][0]["path"] = "inputs/inventory.json"
        bad["evidence_inputs"][0]["sha256"] = _sha256(generic)
        bad["evidence_inputs"].pop(1)
        with self.assertRaisesRegex(ValueError, "category allowlist"):
            self.validate_manifest(bad)

    def test_symlink_cannot_alias_another_input_category(self):
        alias = self.fixture.root / "source/inventory-alias.json"
        alias.symlink_to(self.fixture.root / "inventory/inventory.json")
        bad = copy.deepcopy(self.fixture.manifest)
        bad["evidence_inputs"][0]["path"] = "source/inventory-alias.json"
        bad["evidence_inputs"][0]["sha256"] = _sha256(alias)
        with self.assertRaisesRegex(ValueError, "category|allowlist"):
            self.validate_manifest(bad)

    def test_cyclic_evidence_symlink_is_a_validation_error(self):
        cycle = self.fixture.root / "source/cycle.json"
        cycle.symlink_to(cycle.name)
        bad = copy.deepcopy(self.fixture.manifest)
        bad["evidence_inputs"][0]["path"] = "source/cycle.json"
        with self.assertRaisesRegex(ValueError, "symlink|path"):
            self.validate_manifest(bad)

    def test_stale_matrix_pinned_manifest_digest_fails(self):
        self.fixture.matrix["mapping_contract"]["evidence_manifest"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "manifest.*digest|digest.*manifest"):
            self.validate_manifest()

    def test_manifest_schema_is_closed_and_input_object_is_pinned(self):
        bad = copy.deepcopy(self.fixture.manifest)
        bad["unexpected"] = True
        with self.assertRaisesRegex(ValueError, "exactly"):
            self.validate_manifest(bad)
        unpinned = copy.deepcopy(self.fixture.manifest)
        unpinned["review"]["rationale"] = "Different object than the pinned bytes."
        with self.assertRaisesRegex(ValueError, "object differs|manifest.*digest"):
            renderer.validate_manifest(unpinned, self.fixture.matrix,
                                       repository_root=self.fixture.root, mapper_identity="mapper-1")

    def test_malformed_digest_fails(self):
        bad = copy.deepcopy(self.fixture.manifest)
        bad["evidence_inputs"][0]["sha256"] = "not-a-digest"
        with self.assertRaisesRegex(ValueError, "digest|SHA-256"):
            self.validate_manifest(bad)

    def test_duplicate_normalized_paths_fail(self):
        self.fixture.manifest["evidence_inputs"].append({**self.fixture.inputs[0], "path": "source/./oracle.json"})
        with self.assertRaisesRegex(ValueError, "duplicate|normalized"):
            self.validate_manifest()

    def test_path_outside_repository_fails(self):
        bad = copy.deepcopy(self.fixture.manifest)
        bad["evidence_inputs"][0]["path"] = "../outside.json"
        with self.assertRaisesRegex(ValueError, "repository|path"):
            self.validate_manifest(bad)

    def test_matrix_manifest_and_generated_review_cannot_be_inputs(self):
        for forbidden in ("matrix.json", "evidence/manifest.json", "generated/review.md"):
            with self.subTest(path=forbidden):
                bad = copy.deepcopy(self.fixture.manifest)
                bad["evidence_inputs"][0]["path"] = forbidden
                with self.assertRaisesRegex(ValueError, "forbidden|dependency|path"):
                    self.validate_manifest(bad)

    def test_missing_or_duplicate_review_roles_fail(self):
        for attestations in ([], [self.fixture.manifest["review"]["attestations"][0]],
                             self.fixture.manifest["review"]["attestations"] * 2):
            with self.subTest(count=len(attestations)):
                bad = copy.deepcopy(self.fixture.manifest)
                bad["review"]["attestations"] = attestations
                with self.assertRaises(ValueError):
                    self.validate_manifest(bad)

    def test_same_reviewer_identity_across_roles_fails(self):
        bad = copy.deepcopy(self.fixture.manifest)
        bad["review"]["attestations"][1]["identity"] = bad["review"]["attestations"][0]["identity"]
        with self.assertRaisesRegex(ValueError, "distinct|independent|identity"):
            self.validate_manifest(bad)

    def test_mapper_self_review_fails(self):
        bad = copy.deepcopy(self.fixture.manifest)
        bad["review"]["attestations"][0]["identity"] = "mapper-1"
        with self.assertRaisesRegex(ValueError, "mapper|self.review|independent"):
            self.validate_manifest(bad)

    def test_missing_qualification_access_independence_or_conflict_disposition_fails(self):
        for key in ("qualification", "authorized_source_access", "independence", "conflict_disposition"):
            with self.subTest(key=key):
                bad = copy.deepcopy(self.fixture.manifest)
                del bad["review"]["attestations"][0][key]
                with self.assertRaises(ValueError):
                    self.validate_manifest(bad)

    def test_pending_or_open_conflict_disposition_fails(self):
        for value in ("pending", "open"):
            with self.subTest(value=value):
                bad = copy.deepcopy(self.fixture.manifest)
                bad["review"]["attestations"][0]["conflict_disposition"] = value
                with self.assertRaisesRegex(ValueError, "conflict disposition"):
                    self.validate_manifest(bad)
        inadequate_values = (
            ("qualification", "   "),
            ("authorized_source_access", False),
            ("independence", False),
            ("conflict_disposition", "unresolved"),
        )
        for key, value in inadequate_values:
            with self.subTest(key=key, value=value):
                bad = copy.deepcopy(self.fixture.manifest)
                bad["review"]["attestations"][0][key] = value
                with self.assertRaises(ValueError):
                    self.validate_manifest(bad)

    def test_invalid_review_date_or_disposition_fails(self):
        for key, value in (("review_date", "not-a-date"), ("disposition", "MAYBE")):
            bad = copy.deepcopy(self.fixture.manifest)
            bad["review"]["attestations"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate_manifest(bad)

    def test_unsupported_reviewer_disposition_fails(self):
        bad = copy.deepcopy(self.fixture.manifest)
        bad["review"]["attestations"][0]["disposition"] = "APPROVE_WITHOUT_REVIEW"
        with self.assertRaisesRegex(ValueError, "disposition"):
            self.validate_manifest(bad)

    def test_stale_subject_digest_fails(self):
        bad = copy.deepcopy(self.fixture.manifest)
        bad["review"]["attestations"][0]["evidence_subject_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "subject|attestation|digest"):
            self.validate_manifest(bad, refresh_subject=False)

    def test_open_critical_or_important_findings_fail(self):
        for finding in ("open_critical", "open_important"):
            bad = copy.deepcopy(self.fixture.manifest)
            bad["review"]["attestations"][0]["findings"][finding] = 1
            with self.subTest(finding=finding), self.assertRaises(ValueError):
                self.validate_manifest(bad)

    def test_matrix_labels_cannot_override_missing_feasibility_or_review_evidence(self):
        fixture = SyntheticManifestFixture(self.temp.name, positive=False)
        fixture.matrix["gates"][4]["status"] = "PASS"
        fixture.matrix["gates"][4]["blocker_ids"] = []
        fixture.matrix["gates"][6]["status"] = "PASS"
        fixture.matrix["gates"][6]["blocker_ids"] = []
        fixture.matrix["blockers"] = []
        fixture.matrix["recorded_decision"] = "GO"
        with self.assertRaises(ValueError):
            renderer.derive_decision(fixture.matrix, manifest=fixture.manifest,
                                     repository_root=fixture.root, verify_source_digest=False)

    def test_current_source_rights_and_inventory_evidence_cannot_derive_go(self):
        fixture = SyntheticManifestFixture(self.temp.name)
        with self.assertRaisesRegex(ValueError, "source artifact retrieval|inventory|rights|disabled"):
            renderer.derive_decision(fixture.matrix, manifest=fixture.manifest,
                                     repository_root=fixture.root, verify_source_digest=False)

    def test_hold_and_no_go_blocker_rules_remain_in_force(self):
        self.fixture = SyntheticManifestFixture(self.temp.name, positive=False)
        hold = copy.deepcopy(self.fixture.matrix)
        self.assertEqual(renderer.derive_decision(hold, manifest=self.fixture.manifest,
                         repository_root=self.fixture.root, verify_source_digest=False), "HOLD")
        no_go = copy.deepcopy(hold)
        no_go["recorded_decision"] = "NO_GO"
        no_go["blockers"][0]["remediation"] = "terminal"
        self.assertEqual(renderer.derive_decision(no_go, manifest=self.fixture.manifest,
                         repository_root=self.fixture.root, verify_source_digest=False), "NO_GO")
        no_go["blockers"][0]["remediation"] = "reconsiderable"
        with self.assertRaisesRegex(ValueError, "NO_GO|recorded_decision"):
            renderer.derive_decision(no_go, manifest=self.fixture.manifest,
                                     repository_root=self.fixture.root, verify_source_digest=False)

    def test_high_level_derivation_requires_manifest_pin_even_for_hold(self):
        fixture = SyntheticManifestFixture(self.temp.name, positive=False)
        fixture.matrix["mapping_contract"].pop("evidence_manifest")
        with self.assertRaisesRegex(ValueError, "evidence manifest"):
            renderer.derive_decision(fixture.matrix, repository_root=fixture.root,
                                     verify_source_digest=False)

    def test_all_positive_case_requires_every_independent_prerequisite(self):
        fixture = SyntheticManifestFixture(self.temp.name, ready_sources=True)
        self.assertEqual(renderer.derive_decision(fixture.matrix, manifest=fixture.manifest,
                         repository_root=fixture.root, verify_source_digest=False), "GO")


class Soc2ReadinessBlockerRuleTests(unittest.TestCase):

    def test_hold_requires_reconsiderable_blocker_covering_each_blocked_gate(self):
        gate = GATES[1]
        b = blocker("B1", gate, "reconsiderable")
        m = matrix({**{g: "PASS" for g in GATES}, gate: "BLOCKED"}, [b])
        m["recorded_decision"] = "HOLD"
        validate_matrix(m, verify_source_digest=False)
        self.assertEqual(m["recorded_decision"], "HOLD")
        m["blockers"][0]["remediation"] = "terminal"
        with self.assertRaisesRegex(ValueError, "NO_GO"):
            validate_matrix(m, verify_source_digest=False)

    def test_no_go_requires_terminal_blocker_and_all_blocked_gates_covered(self):
        gate = GATES[2]
        b = blocker("B1", gate, "terminal")
        m = matrix({**{g: "PASS" for g in GATES}, gate: "BLOCKED"}, [b])
        m["recorded_decision"] = "NO_GO"
        validate_matrix(m, verify_source_digest=False)
        self.assertEqual(m["recorded_decision"], "NO_GO")
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
