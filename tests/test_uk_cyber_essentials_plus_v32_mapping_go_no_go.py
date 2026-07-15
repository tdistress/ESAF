from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RIGHTS = ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-rights-re-attestation.md"
MATRIX = ROOT / "docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json"
REVIEW = ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md"
ORACLE_SHA256 = "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc"
PRIOR_RIGHTS_COMMIT = "6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6"
REVIEW_IDENTIFIER = "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--mapping-feasibility--0.1.0"
FIELD_CLASSES = (
    "source_oracle_identity",
    "provision_identifiers_and_structural_classifications",
    "original_probe_selection_rationales",
    "derivative_mapping_analysis",
    "esaf_normative_citations",
    "assurance_and_overclaiming_analysis",
    "official_links",
    "directional_gate_and_decision_metadata",
)
DIRECTIONS = ("esaf_to_external", "external_to_esaf")
DISPOSITIONS = {"GO", "HOLD", "NO_GO"}
GATES = ("source", "rights", "semantic", "normative_basis", "schema", "overclaiming", "utility")
GATE_STATUSES = {"PASS", "BLOCKED", "FAIL"}
GROUPS = ("M", "T1", "S", "T2", "T3", "T4", "T5", "C", "A", "B")
KINDS = (
    "applicability", "prerequisite", "procedure_step", "decision_rule",
    "result_rule", "evidence_retention", "recommendation",
)
ACTORS = ("Assessor", "Applicant", "Certification Body", "Certifying Body", "Delivery Partner")
SCENARIOS = (
    "figure-1-decision-logic",
    "sampling-and-population-limits",
    "evidence-retention",
    "complete-assessment-file-coverage",
    "delivery-partner-discretionary-exception",
    "known-source-anomaly",
    "point-in-time-versus-continuous-assurance",
    "core-v3.3-versus-plus-v3.2-separation",
    "expected-no-direct-esaf-basis",
)
PROBE_CONCLUSIONS = {"POSITIVE_FEASIBILITY", "NO_POSITIVE_BASIS", "INDETERMINATE"}
CONDITION_STATUSES = {"SATISFIED", "NOT_APPLICABLE"}
EXTERNAL_TO_ESAF_CONDITIONS = (
    "actor", "scope", "population", "sample", "assessment_date", "evidence_date",
    "tool", "provenance", "exception", "delivery_partner_discretion",
    "point_in_time_status",
)
PROHIBITED_KEYS = {
    "relationship", "relationships", "coverage", "confidence", "mapping_disposition",
    "snapshot_digest", "lifecycle", "mapper", "approver",
}
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
UTC_ISO_8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
SCENARIO_EVIDENCE = {
    "figure-1-decision-logic": {
        "required": {"CEPTS3.2-T1-008"},
        "one_of": set(),
        "paths": set(),
    },
    "sampling-and-population-limits": {
        "required": set(),
        "one_of": {"CEPTS3.2-M-006", "CEPTS3.2-S-005", "CEPTS3.2-S-007", "CEPTS3.2-S-009"},
        "paths": {"assurance_limits.population_and_sample_boundary"},
    },
    "evidence-retention": {
        "required": set(),
        "one_of": {"CEPTS3.2-M-011", "CEPTS3.2-S-008"},
        "paths": {"assurance_limits.evidence_date_boundary"},
    },
    "complete-assessment-file-coverage": {
        "required": {"CEPTS3.2-B-001"},
        "one_of": {"CEPTS3.2-B-007", "CEPTS3.2-B-010", "CEPTS3.2-B-011", "CEPTS3.2-B-012"},
        "paths": set(),
    },
    "delivery-partner-discretionary-exception": {
        "required": {"CEPTS3.2-C-008", "CEPTS3.2-C-010", "CEPTS3.2-C-011"},
        "one_of": set(),
        "paths": {"assurance_limits.discretion_owner", "assurance_limits.discretionary_exception"},
    },
    "known-source-anomaly": {
        "required": set(),
        "one_of": set(),
        "paths": {"known_anomalies[0].anomaly_id", "known_anomalies[0].locator"},
    },
    "point-in-time-versus-continuous-assurance": {
        "required": set(),
        "one_of": set(),
        "paths": {
            "assurance_limits.assessment_date_boundary",
            "assurance_limits.evidence_date_boundary",
            "assurance_limits.point_in_time_boundary",
        },
    },
    "core-v3.3-versus-plus-v3.2-separation": {
        "required": set(),
        "one_of": set(),
        "paths": {"scope", "assurance_limits.scope_boundary"},
    },
    "expected-no-direct-esaf-basis": {
        "required": set(),
        "one_of": set(),
        "paths": set(),
    },
}


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def assert_exact_keys(
    test: unittest.TestCase,
    obj: dict,
    expected: set[str],
    context: str,
) -> None:
    test.assertEqual(expected, set(obj), context)


def recursive_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            key
            for child in value.values()
            for key in recursive_keys(child)
        }
    if isinstance(value, list):
        return {
            key
            for child in value
            for key in recursive_keys(child)
        }
    return set()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def direction_content_sha256(matrix: dict, direction: str) -> str:
    assessment = next(
        item for item in matrix["direction_assessments"]
        if item["direction"] == direction
    )
    value = {
        "direction_assessment": assessment,
        "probes": [
            probe for probe in matrix["probes"]
            if probe["direction"] == direction
        ],
    }
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def submission_payload_sha256(matrix: dict, direction: str) -> str:
    submission = next(
        item for item in matrix["analysis_provenance"]["submissions"]
        if item["direction"] == direction
    )
    assessment = next(
        item for item in matrix["direction_assessments"]
        if item["direction"] == direction
    )
    payload = {
        "direction": direction,
        "analyst": submission["analyst"],
        "direction_assessment": assessment,
        "probes": [p for p in matrix["probes"] if p["direction"] == direction],
        "no_output_file_attestation": True,
        "no_sibling_content_attestation": True,
    }
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def derive_coverage(matrix: dict, direction: str) -> dict[str, set[str]]:
    selected = [probe for probe in matrix["probes"] if probe["direction"] == direction]
    return {
        "groups": {value for probe in selected for value in probe["groups"]},
        "kinds": {value for probe in selected for value in probe["kinds"]},
        "actors": {value for probe in selected for value in probe["actors"]},
        "special_scenarios": {
            binding["scenario_id"]
            for probe in selected
            for binding in probe["special_scenario_bindings"]
        },
    }


def expected_disposition(
    assessment: dict,
    probes_by_id: dict[str, dict],
) -> str:
    statuses = {gate["status"] for gate in assessment["gate_results"]}
    derived_positive = [
        probe_id
        for probe_id, probe in probes_by_id.items()
        if probe["direction"] == assessment["direction"]
        and probe["conclusion"] == "POSITIVE_FEASIBILITY"
    ]
    if derived_positive != assessment["positive_probe_identifiers"]:
        raise ValueError("positive_probe_identifiers do not equal derived positive probes")
    if "FAIL" in statuses:
        return "NO_GO"
    if "BLOCKED" in statuses:
        return "HOLD"
    return "GO" if derived_positive else "NO_GO"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def resolve_oracle_path(oracle: dict, path: str) -> object:
    if path == "scope":
        return oracle["scope"]
    provision = re.fullmatch(r"provisions\[([^]]+)\]\.(external_provision_id|summary|locator)", path)
    if provision:
        item = next(
            entry for entry in oracle["provisions"]
            if entry["external_provision_id"] == provision.group(1)
        )
        return item[provision.group(2)]
    anomaly = re.fullmatch(r"known_anomalies\[0\]\.(anomaly_id|locator)", path)
    if anomaly:
        return oracle["known_anomalies"][0][anomaly.group(1)]
    assurance = re.fullmatch(r"assurance_limits\.([a-z_]+)", path)
    if assurance and assurance.group(1) in oracle["assurance_limits"]:
        return oracle["assurance_limits"][assurance.group(1)]
    raise KeyError(path)


class MappingGoNoGoTests(unittest.TestCase):
    def test_oracle_digest_is_locked(self) -> None:
        self.assertEqual(normalized_sha256(ORACLE), ORACLE_SHA256)

    def test_rights_re_attestation_exists_before_analysis(self) -> None:
        self.assertTrue(RIGHTS.is_file())

    def test_rights_re_attestation_contract_is_exact(self) -> None:
        text = RIGHTS.read_text(encoding="utf-8")
        self.assertIn(f"`{ORACLE_SHA256}`", text)
        self.assertIn(f"`{PRIOR_RIGHTS_COMMIT}`", text)
        self.assertIn("**Disposition:** Approved", text)
        for field_class in FIELD_CLASSES:
            self.assertIn(f"`{field_class}`", text)
        self.assertIn("**IASME partition preserved:** yes", text)
        self.assertIn("**Copied-source prohibition preserved:** yes", text)

    def test_matrix_and_rendered_review_exist(self) -> None:
        missing = [str(path.relative_to(ROOT)) for path in (MATRIX, REVIEW) if not path.is_file()]
        self.assertEqual([], missing)


@unittest.skipUnless(MATRIX.is_file() and REVIEW.is_file(), "Task 4 artifacts are absent")
class MatrixClosedContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        cls.review = REVIEW.read_text(encoding="utf-8")
        cls.provisions = {
            item["external_provision_id"]: item for item in cls.oracle["provisions"]
        }
        cls.probes = {item["probe_id"]: item for item in cls.matrix["probes"]}

    def assert_nonempty_string(self, value: object, context: str) -> None:
        self.assertIsInstance(value, str, context)
        self.assertTrue(value.strip(), context)

    def assert_evidence_reference(self, reference: str) -> None:
        if reference in self.probes or reference.startswith("https://"):
            return
        path_text, separator, locator = reference.partition("#")
        self.assertTrue(separator and locator, reference)
        self.assertTrue((ROOT / path_text).is_file(), reference)

    def test_top_level_source_rights_roles_and_coverage_are_closed(self) -> None:
        assert_exact_keys(self, self.matrix, {
            "schema_version", "review_identifier", "source_oracle",
            "rights_re_attestation", "roles", "coverage_contract",
            "analysis_provenance", "direction_assessments", "probes",
        }, "matrix")
        self.assertEqual(self.matrix["schema_version"], "1.0.0")
        self.assertEqual(self.matrix["review_identifier"], REVIEW_IDENTIFIER)
        source = self.matrix["source_oracle"]
        assert_exact_keys(self, source, {
            "path", "sha256", "source_version", "expected_provision_count",
            "atomization_rule_version", "scope_statement",
        }, "source_oracle")
        self.assertEqual(source["path"], ORACLE.relative_to(ROOT).as_posix())
        self.assertEqual(source["sha256"], ORACLE_SHA256)
        self.assertEqual(source["source_version"], "3.2")
        self.assertEqual(source["expected_provision_count"], 144)
        self.assertEqual(source["atomization_rule_version"], "1.0.0")
        self.assertEqual(source["scope_statement"], self.oracle["scope"]["statement"])
        rights = self.matrix["rights_re_attestation"]
        assert_exact_keys(self, rights, {
            "record_path", "record_commit", "reviewer", "review_date",
            "prior_rights_commit", "oracle_sha256", "publication_basis_covered",
            "iasme_partition_preserved", "copied_source_prohibition_preserved",
            "field_classes_reviewed", "disposition",
        }, "rights_re_attestation")
        self.assertEqual(rights["record_path"], RIGHTS.relative_to(ROOT).as_posix())
        self.assertEqual(rights["prior_rights_commit"], PRIOR_RIGHTS_COMMIT)
        self.assertEqual(rights["oracle_sha256"], ORACLE_SHA256)
        self.assertEqual(rights["field_classes_reviewed"], list(FIELD_CLASSES))
        for key in ("publication_basis_covered", "iasme_partition_preserved", "copied_source_prohibition_preserved"):
            self.assertIs(rights[key], True)
        self.assertEqual(rights["disposition"], "approved")
        assert_exact_keys(self, self.matrix["roles"], {
            "esaf_to_external_analyst", "external_to_esaf_analyst", "reconciler",
        }, "roles")
        roles = self.matrix["roles"]
        self.assertEqual(len(set(roles.values())), 3)
        self.assertNotIn(rights["reviewer"], roles.values())
        coverage = self.matrix["coverage_contract"]
        assert_exact_keys(self, coverage, {"groups", "kinds", "actors", "special_scenarios"}, "coverage_contract")
        self.assertEqual(coverage, {
            "groups": list(GROUPS), "kinds": list(KINDS), "actors": list(ACTORS),
            "special_scenarios": list(SCENARIOS),
        })

    def test_rights_commit_is_rights_only_and_precedes_analysis(self) -> None:
        commit = self.matrix["rights_re_attestation"]["record_commit"]
        self.assertRegex(commit, r"^[0-9a-f]{40}$")
        self.assertEqual(git("diff-tree", "--no-commit-id", "--name-only", "-r", commit), RIGHTS.relative_to(ROOT).as_posix())
        self.assertEqual(subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ROOT
        ).returncode, 0)
        first_probe_commit = git("log", "--diff-filter=A", "--format=%H", "--reverse", "--", MATRIX.relative_to(ROOT).as_posix())
        if first_probe_commit:
            self.assertEqual(subprocess.run(
                ["git", "merge-base", "--is-ancestor", commit, first_probe_commit.splitlines()[0]], cwd=ROOT
            ).returncode, 0)

    def test_provenance_is_closed_immutable_and_digest_bound(self) -> None:
        provenance = self.matrix["analysis_provenance"]
        assert_exact_keys(self, provenance, {
            "broker_protocol", "prompt_digests", "common_input_sha256",
            "submissions", "direction_content_digests", "reconciliation",
        }, "analysis_provenance")
        broker = provenance["broker_protocol"]
        assert_exact_keys(self, broker, {
            "dispatch_mode", "fork_turns", "concurrent", "analyst_output_channel",
            "no_output_files", "controller_withholding_attestation",
            "sibling_mailbox_inaccessible_attestation", "fail_closed_fallback",
        }, "broker_protocol")
        self.assertEqual(broker, {
            "dispatch_mode": "codex_sibling_agents", "fork_turns": "none",
            "concurrent": True, "analyst_output_channel": "controller_mailbox_final_response",
            "no_output_files": True, "controller_withholding_attestation": True,
            "sibling_mailbox_inaccessible_attestation": True,
            "fail_closed_fallback": "separate_principals_or_containers_else_stop",
        })
        prompts = provenance["prompt_digests"]
        self.assertEqual([item["direction"] for item in prompts], list(DIRECTIONS))
        for item in prompts:
            assert_exact_keys(self, item, {"direction", "sha256"}, "prompt_digest")
            self.assertRegex(item["sha256"], HEX_SHA256)
        self.assertEqual(len({item["sha256"] for item in prompts}), 2)
        self.assertRegex(provenance["common_input_sha256"], HEX_SHA256)
        submissions = provenance["submissions"]
        self.assertEqual([item["direction"] for item in submissions], list(DIRECTIONS))
        self.assertEqual([item["analyst"] for item in submissions], [
            self.matrix["roles"]["esaf_to_external_analyst"],
            self.matrix["roles"]["external_to_esaf_analyst"],
        ])
        for item in submissions:
            assert_exact_keys(self, item, {
                "direction", "analyst", "received_at_utc", "payload_sha256",
                "digest_reference", "no_output_file_attestation",
                "no_sibling_content_attestation",
            }, "submission")
            self.assertRegex(item["received_at_utc"], UTC_ISO_8601)
            self.assertRegex(item["payload_sha256"], HEX_SHA256)
            self.assertEqual(item["payload_sha256"], submission_payload_sha256(self.matrix, item["direction"]))
            self.assertIs(item["no_output_file_attestation"], True)
            self.assertIs(item["no_sibling_content_attestation"], True)
        self.assertEqual(len({item["payload_sha256"] for item in submissions}), 2)
        self.assertEqual(len({item["digest_reference"] for item in submissions}), 2)
        digests = provenance["direction_content_digests"]
        self.assertEqual([item["direction"] for item in digests], list(DIRECTIONS))
        for item in digests:
            assert_exact_keys(self, item, {"direction", "sha256"}, "direction_content_digest")
            self.assertEqual(item["sha256"], direction_content_sha256(self.matrix, item["direction"]))
        reconciliation = provenance["reconciliation"]
        assert_exact_keys(self, reconciliation, {
            "reconciler", "submission_digest_references", "direction_validations",
            "post_seal_changes_prohibited", "packaging_disposition",
        }, "reconciliation")
        self.assertEqual(reconciliation["reconciler"], self.matrix["roles"]["reconciler"])
        self.assertEqual(reconciliation["submission_digest_references"], [item["digest_reference"] for item in submissions])
        self.assertIs(reconciliation["post_seal_changes_prohibited"], True)
        self.assertEqual(reconciliation["packaging_disposition"], "accepted")
        validations = reconciliation["direction_validations"]
        self.assertEqual([item["direction"] for item in validations], list(DIRECTIONS))
        for item in validations:
            assert_exact_keys(self, item, {"direction", "status", "evidence_references"}, "direction_validation")
            self.assertEqual(item["status"], "ACCEPTED")
            self.assertTrue(item["evidence_references"])
            for reference in item["evidence_references"]:
                self.assert_evidence_reference(reference)
        keys = recursive_keys(self.matrix)
        self.assertFalse({
            key for key in keys
            if "correction" in key.lower() or "supersession" in key.lower()
            or key == "supersedes_digest_reference"
        })

    def test_assessments_gates_and_dispositions_are_mechanical(self) -> None:
        assessments = self.matrix["direction_assessments"]
        self.assertEqual([item["direction"] for item in assessments], list(DIRECTIONS))
        for assessment in assessments:
            assert_exact_keys(self, assessment, {
                "direction", "analyst", "question", "gate_results",
                "positive_probe_identifiers", "disposition", "decision_rationale",
                "prerequisites", "reconsideration_triggers",
            }, "direction_assessment")
            role = self.matrix["roles"][f"{assessment['direction']}_analyst"]
            self.assertEqual(assessment["analyst"], role)
            self.assertEqual([gate["gate"] for gate in assessment["gate_results"]], list(GATES))
            self.assertEqual(assessment["disposition"], expected_disposition(assessment, self.probes))
            self.assertIn(assessment["disposition"], DISPOSITIONS)
            for gate in assessment["gate_results"]:
                assert_exact_keys(self, gate, {"gate", "status", "rationale", "evidence_references"}, "gate")
                self.assertIn(gate["status"], GATE_STATUSES)
                self.assert_nonempty_string(gate["rationale"], "gate rationale")
                self.assertTrue(gate["evidence_references"])
                for reference in gate["evidence_references"]:
                    self.assert_evidence_reference(reference)
            for prerequisite in assessment["prerequisites"]:
                assert_exact_keys(self, prerequisite, {"prerequisite", "required_evidence", "reentry_test"}, "prerequisite")
                for value in prerequisite.values():
                    self.assert_nonempty_string(value, "prerequisite value")
            for trigger in assessment["reconsideration_triggers"]:
                assert_exact_keys(self, trigger, {"change", "required_evidence"}, "reconsideration trigger")
                for value in trigger.values():
                    self.assert_nonempty_string(value, "trigger value")
            if assessment["disposition"] == "GO":
                self.assertEqual(assessment["prerequisites"], [])
                self.assertEqual(assessment["reconsideration_triggers"], [])
            elif assessment["disposition"] == "HOLD":
                self.assertIn("BLOCKED", {g["status"] for g in assessment["gate_results"]})
                self.assertTrue(assessment["prerequisites"])
                self.assertEqual(assessment["reconsideration_triggers"], [])
            else:
                self.assertEqual(assessment["prerequisites"], [])
                self.assertTrue(assessment["reconsideration_triggers"])

    def test_probe_contract_oracle_derivation_and_conditions_are_exact(self) -> None:
        self.assertEqual(len(self.probes), len(self.matrix["probes"]))
        for probe in self.matrix["probes"]:
            assert_exact_keys(self, probe, {
                "probe_id", "direction", "provision_ids", "selection_basis", "groups",
                "kinds", "actors", "special_scenarios", "special_scenario_bindings",
                "condition_checklist", "esaf_normative_bases", "semantic_fit_analysis",
                "assurance_and_overclaiming_risks", "source_rights_and_operational_limits",
                "conclusion", "rationale",
            }, "probe")
            self.assertIn(probe["direction"], DIRECTIONS)
            self.assertIn(probe["conclusion"], PROBE_CONCLUSIONS)
            self.assertTrue(probe["provision_ids"])
            selected = [self.provisions[item] for item in probe["provision_ids"]]
            self.assertEqual(probe["groups"], list(dict.fromkeys(item["group"] for item in selected)))
            self.assertEqual(probe["kinds"], list(dict.fromkeys(item["kind"] for item in selected)))
            self.assertEqual(probe["actors"], list(dict.fromkeys(actor for item in selected for actor in item["actors"])))
            expected_conditions = (
                probe["direction"] == "external_to_esaf"
                and probe["conclusion"] == "POSITIVE_FEASIBILITY"
            )
            if expected_conditions:
                self.assertEqual([entry["condition"] for entry in probe["condition_checklist"]], list(EXTERNAL_TO_ESAF_CONDITIONS))
                for entry in probe["condition_checklist"]:
                    assert_exact_keys(self, entry, {"condition", "status", "evidence_references"}, "condition")
                    self.assertIn(entry["status"], CONDITION_STATUSES)
                    self.assertTrue(entry["evidence_references"])
                    for reference in entry["evidence_references"]:
                        self.assert_evidence_reference(reference)
            else:
                self.assertEqual(probe["condition_checklist"], [])
            if probe["conclusion"] == "POSITIVE_FEASIBILITY":
                self.assertTrue(probe["esaf_normative_bases"])
            if probe["conclusion"] == "NO_POSITIVE_BASIS":
                self.assertRegex(probe["rationale"], r"(?i)missing|does not (?:supply|provide|require|establish)")
            if probe["conclusion"] == "INDETERMINATE":
                assessment = next(item for item in self.matrix["direction_assessments"] if item["direction"] == probe["direction"])
                self.assertTrue(assessment["prerequisites"])
                self.assertTrue(any(item["prerequisite"] in probe["rationale"] for item in assessment["prerequisites"]))
            for basis in probe["esaf_normative_bases"]:
                assert_exact_keys(self, basis, {"control_id", "requirement_locator", "relevance_analysis"}, "normative basis")
                control = ROOT / "controls" / basis["control_id"].split("-", 1)[0] / f"{basis['control_id']}.md"
                self.assertTrue(control.is_file(), basis["control_id"])
                self.assertEqual(basis["requirement_locator"], f"{control.relative_to(ROOT).as_posix()}#requirement")
                requirement = control.read_text(encoding="utf-8").split("## Requirement", 1)[1].split("## ", 1)[0]
                self.assertRegex(requirement, r"\bshall\b")
                self.assert_nonempty_string(basis["relevance_analysis"], "relevance analysis")

    def test_direction_local_coverage_and_scenario_bindings_are_complete(self) -> None:
        for direction in DIRECTIONS:
            coverage = derive_coverage(self.matrix, direction)
            self.assertEqual(coverage, {
                "groups": set(GROUPS), "kinds": set(KINDS), "actors": set(ACTORS),
                "special_scenarios": set(SCENARIOS),
            })
            selected = [probe for probe in self.matrix["probes"] if probe["direction"] == direction]
            for probe in selected:
                self.assertEqual(probe["special_scenarios"], [item["scenario_id"] for item in probe["special_scenario_bindings"]])
                self.assertEqual(len(set(probe["special_scenarios"])), len(probe["special_scenarios"]))
                for binding in probe["special_scenario_bindings"]:
                    assert_exact_keys(self, binding, {"scenario_id", "provision_ids", "oracle_paths"}, "scenario binding")
                    self.assertTrue(binding["provision_ids"])
                    self.assertTrue(set(binding["provision_ids"]) <= set(probe["provision_ids"]))
                    self.assertTrue(binding["oracle_paths"])
                    for path in binding["oracle_paths"]:
                        resolve_oracle_path(self.oracle, path)
                        match = re.match(r"provisions\[([^]]+)\]", path)
                        if match:
                            self.assertIn(match.group(1), binding["provision_ids"])
            for scenario, contract in SCENARIO_EVIDENCE.items():
                probe, binding = next(
                    (probe, binding)
                    for probe in selected
                    for binding in probe["special_scenario_bindings"]
                    if binding["scenario_id"] == scenario
                )
                ids = set(binding["provision_ids"])
                self.assertTrue(contract["required"] <= ids, scenario)
                if contract["one_of"]:
                    self.assertTrue(contract["one_of"] & ids, scenario)
                self.assertTrue(contract["paths"] <= set(binding["oracle_paths"]), scenario)
                if scenario == "figure-1-decision-logic":
                    self.assertTrue({f"CEPTS3.2-T1-{number:03d}" for number in range(9, 17)} <= ids)
                elif scenario == "known-source-anomaly":
                    self.assertEqual(resolve_oracle_path(self.oracle, "known_anomalies[0].anomaly_id"), "cepts32-anomaly-001")
                elif scenario == "expected-no-direct-esaf-basis":
                    self.assertEqual(probe["conclusion"], "NO_POSITIVE_BASIS")
                    for provision_id in ids:
                        self.assertIn(f"provisions[{provision_id}].summary", binding["oracle_paths"])
                        self.assertIn(f"provisions[{provision_id}].locator", binding["oracle_paths"])
                elif scenario in {"point-in-time-versus-continuous-assurance", "core-v3.3-versus-plus-v3.2-separation", "known-source-anomaly"}:
                    self.assertTrue(ids)

    def test_prohibited_fields_claims_literals_and_mapping_tree_changes_are_absent(self) -> None:
        self.assertEqual(PROHIBITED_KEYS & recursive_keys(self.matrix), set())
        combined = MATRIX.read_text(encoding="utf-8") + "\n" + self.review
        self.assertNotIn(self.oracle["known_anomalies"][0]["source_literal"], combined)
        for pattern in (
            r"(?i)\bequivalent to\b", r"(?i)\bensures compliance\b",
            r"(?i)\bcertified by\b", r"(?i)\bNCSC endorses\b",
            r"(?i)\bproves (?:continuous|full.population) assurance\b",
        ):
            self.assertNotRegex(combined, pattern)
        base = git("merge-base", "HEAD", "origin/main")
        changed = git("diff", "--name-only", base, "--", "crosswalks/mappings", "crosswalks/registry")
        self.assertEqual(changed, "")

    def test_rendered_review_is_derived_from_matrix(self) -> None:
        self.assertIn("No mapping snapshot exists", self.review)
        self.assertIn("design only", self.review)
        for assessment in self.matrix["direction_assessments"]:
            direction = assessment["direction"]
            section = self.review.split(f"## {direction}", 1)[1].split("## ", 1)[0]
            self.assertIn(f"**Disposition:** {assessment['disposition']}", section)
            for gate in assessment["gate_results"]:
                self.assertIn(f"| `{gate['gate']}` | `{gate['status']}` |", section)
            selected = [probe for probe in self.matrix["probes"] if probe["direction"] == direction]
            conclusions = {value: sum(p["conclusion"] == value for p in selected) for value in PROBE_CONCLUSIONS}
            self.assertIn(
                f"Probes: {len(selected)}; positive: {conclusions['POSITIVE_FEASIBILITY']}; "
                f"no positive basis: {conclusions['NO_POSITIVE_BASIS']}; "
                f"indeterminate: {conclusions['INDETERMINATE']}.", section,
            )
            coverage = derive_coverage(self.matrix, direction)
            for label, key in (("Groups", "groups"), ("Kinds", "kinds"), ("Actors", "actors"), ("Special scenarios", "special_scenarios")):
                self.assertIn(f"| {label} | {len(coverage[key])} |", section)
