from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tools.release_gates import (
    load_front_matter as load_v04_front_matter,
    validate_record as validate_v04_record,
)
from tools.v05_beta_release_gates import (
    PHASE_GATE_STATES,
    RECORD_RELATIVE,
    derive_scope,
    load_front_matter,
    validate_record,
    validate_transition,
)


ROOT = Path(__file__).resolve().parents[1]
V04_RECORD = ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
EXPECTED_SCOPE = {
    "controls": 91,
    "control_families": 16,
    "architecture_patterns": 7,
    "mapping_sets": 3,
    "mapping_provisions": 404,
    "relationship_legs": 81,
    "negative_dispositions": 325,
    "assessment_foundation": True,
    "draft_profiles": 1,
    "pci_dss_disposition": "HOLD",
}
MAPPING_SETS = [
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
]


def record_fixture(phase: str) -> dict[str, object]:
    states = PHASE_GATE_STATES[phase]
    return {
        "release": "0.5-beta",
        "tag": "v0.5-beta",
        "issue": 59,
        "repository_scope": "complete_git_tracked_repository",
        "phase": phase,
        "mapping_decision_basis": "qualified_approval",
        "mapping_sets": MAPPING_SETS,
        "scope": deepcopy(EXPECTED_SCOPE),
        "publication": {
            "condition": "remote_annotated_tag_matches_exact_validated_commit",
            "date": "2026-07-27" if phase == "published" else None,
            "evidence": ["https://example.test/release-record"],
        },
        "gates": {
            gate: {
                "state": state,
                "evidence": [f"https://example.test/{gate}"]
                if state in {"ready", "closed"}
                else [],
            }
            for gate, state in states.items()
        },
    }


class V05ReleaseRecordTests(unittest.TestCase):
    def test_v04_published_validator_remains_green(self) -> None:
        historical = load_v04_front_matter(V04_RECORD)
        self.assertEqual([], validate_v04_record(ROOT, historical))

    def test_v05_record_requires_fixed_release_identity(self) -> None:
        record = record_fixture("evidence_candidate")
        for field, value, diagnostic in (
            ("release", "0.4-alpha", "release shall equal 0.5-beta"),
            ("tag", "v0.4-alpha", "tag shall equal v0.5-beta"),
            ("issue", 39, "issue shall equal 59"),
        ):
            with self.subTest(field=field):
                candidate = deepcopy(record)
                candidate[field] = value
                self.assertIn(diagnostic, validate_record(ROOT, candidate))

    def test_phase_gate_state_matrix_is_exact(self) -> None:
        for phase, expected in PHASE_GATE_STATES.items():
            with self.subTest(phase=phase):
                record = record_fixture(phase)
                observed = {
                    gate: value["state"]
                    for gate, value in record["gates"].items()
                }
                self.assertEqual(expected, observed)
                self.assertEqual([], validate_record(ROOT, record))

    def test_scope_counts_are_derived_from_repository(self) -> None:
        self.assertEqual(EXPECTED_SCOPE, derive_scope(ROOT))

    def test_transition_rejects_published_to_candidate(self) -> None:
        previous = record_fixture("published")
        candidate = record_fixture("closure_candidate")
        self.assertIn(
            "published record shall not transition to a candidate phase",
            validate_transition(previous, candidate),
        )

    def test_contract_rejects_each_wrong_phase_gate_state(self) -> None:
        for phase, gates in PHASE_GATE_STATES.items():
            for gate, expected in gates.items():
                for wrong_state in {"open", "in_review", "ready", "closed"} - {expected}:
                    with self.subTest(phase=phase, gate=gate, wrong_state=wrong_state):
                        record = record_fixture(phase)
                        record["gates"][gate]["state"] = wrong_state
                        self.assertIn(
                            f"{phase} phase shall set {gate} gate to {expected}",
                            validate_record(ROOT, record),
                        )

    def test_contract_rejects_each_invalid_record_mutation(self) -> None:
        record = record_fixture("closure_candidate")
        mutations = (
            (
                "wrong phase state",
                lambda value: value["gates"]["scope"].update(state="open"),
                "closure_candidate phase shall set scope gate to ready",
            ),
            (
                "missing mapping set",
                lambda value: value.update(mapping_sets=value["mapping_sets"][:-1]),
                "mapping_sets shall equal the tracked catalog mapping sets",
            ),
            (
                "duplicate mapping set",
                lambda value: value.update(mapping_sets=[*value["mapping_sets"], value["mapping_sets"][0]]),
                "mapping_sets shall not contain duplicates",
            ),
            (
                "unsupported decision basis",
                lambda value: value.update(mapping_decision_basis="unreviewed"),
                "mapping_decision_basis shall be supported",
            ),
            (
                "stale scope count",
                lambda value: value["scope"].update(controls=90),
                "scope shall equal the derived repository scope",
            ),
            (
                "missing assessment foundation",
                lambda value: value["scope"].update(assessment_foundation=False),
                "scope shall equal the derived repository scope",
            ),
            (
                "wrong profile count",
                lambda value: value["scope"].update(draft_profiles=2),
                "scope shall equal the derived repository scope",
            ),
            (
                "non-HOLD PCI disposition",
                lambda value: value["scope"].update(pci_dss_disposition="GO"),
                "scope shall equal the derived repository scope",
            ),
            (
                "non-HTTPS evidence",
                lambda value: value["gates"]["scope"].update(evidence=["http://example.test/scope"]),
                "scope: evidence shall use HTTPS locators",
            ),
            (
                "candidate SHA field",
                lambda value: value.update(validated_sha="a" * 40),
                "candidate phases shall not contain SHA fields",
            ),
            (
                "unknown top-level field",
                lambda value: value.update(unexpected=True),
                "unknown top-level key unexpected",
            ),
            (
                "unknown gate",
                lambda value: value["gates"].update(unexpected={"state": "ready", "evidence": ["https://example.test/unexpected"]}),
                "unknown gate unexpected",
            ),
        )
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                candidate = deepcopy(record)
                mutate(candidate)
                self.assertIn(diagnostic, validate_record(ROOT, candidate))

    def test_contract_rejects_untracked_scope_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "core.autocrlf=false", "add", "."],
                cwd=root,
                check=True,
            )
            (root / "untracked-input.txt").write_text("untracked\n", encoding="utf-8")
            record = record_fixture("evidence_candidate")
            record["scope_inputs"] = ["untracked-input.txt"]
            self.assertIn(
                "required scope inputs shall be Git-tracked",
                validate_record(root, record),
            )

    def test_cli_requires_baseline_for_closure_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "---\n" + json.dumps(record_fixture("closure_candidate")) + "\n---\n",
                encoding="utf-8",
            )
            (root / "tools").mkdir()
            shutil.copy2(ROOT / "tools/v05_beta_release_gates.py", root / "tools/v05_beta_release_gates.py")
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "core.autocrlf=false", "add", "."],
                cwd=root,
                check=True,
            )
            result = subprocess.run(
                [sys.executable, "tools/v05_beta_release_gates.py", "--check"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("baseline-ref is required for closure candidate", result.stdout)

    def _copy_scope_inputs(self, destination: Path) -> None:
        for relative in (
            "controls/catalog.json",
            "architectures/patterns",
            "crosswalks/catalog.json",
            "assessment/ESAF-1500.md",
            "profiles/uk/0.1.0/profile.json",
            "docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json",
        ):
            source = ROOT / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)


if __name__ == "__main__":
    unittest.main()
