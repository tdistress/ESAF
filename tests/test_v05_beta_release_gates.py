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

    def test_transition_requires_a_v05_evidence_baseline_for_closure(self) -> None:
        candidate = record_fixture("closure_candidate")
        mutations = (
            (
                "wrong release",
                lambda value: value.update(release="0.4-alpha"),
                "baseline release shall equal 0.5-beta",
            ),
            (
                "wrong repository scope",
                lambda value: value.update(repository_scope="partial"),
                "baseline repository scope shall equal complete_git_tracked_repository",
            ),
            (
                "skipped evidence phase",
                lambda value: value.update(phase="closure_candidate"),
                "closure_candidate shall transition only from evidence_candidate",
            ),
            (
                "phase regression",
                lambda value: value.update(phase="published"),
                "closure_candidate shall transition only from evidence_candidate",
            ),
        )
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                previous = record_fixture("evidence_candidate")
                mutate(previous)
                self.assertIn(diagnostic, validate_transition(previous, candidate))

    def test_transition_requires_a_closure_baseline_for_publication(self) -> None:
        self.assertIn(
            "published shall transition only from closure_candidate",
            validate_transition(
                record_fixture("evidence_candidate"), record_fixture("published")
            ),
        )

    def test_transition_rejects_any_predecessor_for_evidence_candidate(self) -> None:
        for phase in ("closure_candidate", "published"):
            with self.subTest(phase=phase):
                self.assertIn(
                    "evidence_candidate shall not have a predecessor",
                    validate_transition(
                        record_fixture(phase), record_fixture("evidence_candidate")
                    ),
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

    def test_contract_rejects_scope_input_overrides(self) -> None:
        for scope_inputs in ([], ["controls/catalog.json"]):
            with self.subTest(scope_inputs=scope_inputs):
                record = record_fixture("evidence_candidate")
                record["scope_inputs"] = scope_inputs
                self.assertIn(
                    "scope_inputs shall not override fixed authoritative scope inputs",
                    validate_record(ROOT, record),
                )

    def test_contract_rejects_unknown_nested_fields_and_nested_sha_keys(self) -> None:
        mutations = (
            (
                "publication field",
                lambda value: value["publication"].update(unexpected=True),
                "unknown publication key unexpected",
            ),
            (
                "gate field",
                lambda value: value["gates"]["scope"].update(unexpected=True),
                "scope: unknown gate key unexpected",
            ),
            (
                "nested SHA field",
                lambda value: value["publication"].update(commit_sha={}),
                "candidate phases shall not contain SHA fields",
            ),
        )
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                record = record_fixture("evidence_candidate")
                mutate(record)
                self.assertIn(diagnostic, validate_record(ROOT, record))

    def test_contract_enforces_publication_date_lifecycle(self) -> None:
        candidate = record_fixture("closure_candidate")
        candidate["publication"]["date"] = "2026-07-27"
        self.assertIn(
            "candidate publication date shall be null",
            validate_record(ROOT, candidate),
        )
        published = record_fixture("published")
        published["publication"]["date"] = None
        self.assertIn(
            "published publication date shall be an ISO date",
            validate_record(ROOT, published),
        )

    def test_contract_rejects_non_draft_mapping_catalog_entries(self) -> None:
        for mutation in ("catalog entry", "mapping record"):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    catalog_path = root / "crosswalks/catalog.json"
                    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
                    relative_record = catalog["mapping_sets"][0]["provisions"][0]["path"]
                    if mutation == "mapping record":
                        record_path = root / relative_record
                        record_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(ROOT / relative_record, record_path)
                    self._initialize_repository(root)
                    if mutation == "catalog entry":
                        catalog["mapping_sets"][0]["metadata"]["status"] = "published"
                        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
                    else:
                        record_path = root / relative_record
                        text = record_path.read_text(encoding="utf-8")
                        if text.lstrip().startswith("{"):
                            record = json.loads(text)
                            record["status"] = "published"
                            record_path.write_text(json.dumps(record), encoding="utf-8")
                        else:
                            record_path.write_text(
                                text.replace('"status":"draft"', '"status":"published"', 1)
                                if '"status":"draft"' in text
                                else text.replace("status: draft", "status: published", 1),
                                encoding="utf-8",
                            )
                    self.assertIn(
                        "tracked mapping sets shall remain draft",
                        validate_record(root, record_fixture("evidence_candidate")),
                    )

    def test_contract_requires_catalog_mapping_sources_to_exist_and_be_tracked(self) -> None:
        for mutation, diagnostic in (
            ("missing", "catalog-declared mapping source is missing"),
            ("untracked", "catalog-declared mapping source shall be Git-tracked"),
        ):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    catalog = json.loads((root / "crosswalks/catalog.json").read_text())
                    relative = catalog["mapping_sets"][0]["provisions"][0]["path"]
                    self._initialize_repository(root)
                    if mutation == "untracked":
                        target = root / relative
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(ROOT / relative, target)
                    self.assertIn(
                        diagnostic,
                        validate_record(root, record_fixture("evidence_candidate")),
                    )

    def test_contract_rejects_untracked_pattern_and_profile_scope_files(self) -> None:
        for relative, source in (
            ("architectures/patterns/ARC-P999.md", "architectures/patterns/ARC-P100.md"),
            ("profiles/example/0.1.0/profile.json", "profiles/uk/0.1.0/profile.json"),
        ):
            with self.subTest(relative=relative):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    self._initialize_repository(root)
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / source, target)
                    self.assertIn(
                        "scope inputs shall not contain untracked files",
                        validate_record(root, record_fixture("evidence_candidate")),
                    )

    def test_contract_returns_diagnostic_for_malformed_crosswalk_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            self._initialize_repository(root)
            (root / "crosswalks/catalog.json").write_text("{", encoding="utf-8")
            self.assertIn(
                "crosswalk catalog cannot be parsed",
                validate_record(root, record_fixture("evidence_candidate")),
            )

    def test_contract_rejects_untracked_scope_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            self._initialize_repository(root)
            shutil.copy2(
                ROOT / "architectures/patterns/ARC-P100.md",
                root / "architectures/patterns/ARC-P999.md",
            )
            self.assertIn(
                "scope inputs shall not contain untracked files",
                validate_record(root, record_fixture("evidence_candidate")),
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

    def test_cli_requires_baseline_for_published_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "---\n" + json.dumps(record_fixture("published")) + "\n---\n",
                encoding="utf-8",
            )
            (root / "tools").mkdir()
            shutil.copy2(ROOT / "tools/v05_beta_release_gates.py", root / "tools/v05_beta_release_gates.py")
            self._initialize_repository(root)
            result = subprocess.run(
                [sys.executable, "tools/v05_beta_release_gates.py", "--check"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("baseline-ref is required for published", result.stdout)

    def test_cli_rejects_wrong_release_and_invalid_phase_baselines(self) -> None:
        for name, baseline, diagnostic in (
            (
                "wrong release",
                {"release": "0.4-alpha"},
                "baseline release shall equal 0.5-beta",
            ),
            (
                "invalid phase",
                {"phase": "closure_candidate"},
                "closure_candidate shall transition only from evidence_candidate",
            ),
        ):
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    (root / "tools").mkdir()
                    shutil.copy2(
                        ROOT / "tools/v05_beta_release_gates.py",
                        root / "tools/v05_beta_release_gates.py",
                    )
                    record_path = root / RECORD_RELATIVE
                    record_path.parent.mkdir(parents=True)
                    previous = record_fixture("evidence_candidate")
                    previous.update(baseline)
                    record_path.write_text(
                        "---\n" + json.dumps(previous) + "\n---\n",
                        encoding="utf-8",
                    )
                    self._initialize_repository(root, commit=True)
                    record_path.write_text(
                        "---\n" + json.dumps(record_fixture("closure_candidate")) + "\n---\n",
                        encoding="utf-8",
                    )
                    result = subprocess.run(
                        [
                            sys.executable,
                            "tools/v05_beta_release_gates.py",
                            "--check",
                            "--baseline-ref",
                            "HEAD",
                        ],
                        cwd=root,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(1, result.returncode)
                    self.assertIn(diagnostic, result.stdout)

    def test_cli_validates_baseline_against_its_git_ref(self) -> None:
        for mutation, diagnostic in (
            ("scope", "baseline record: scope shall equal the derived repository scope"),
            ("mapping", "baseline record: tracked mapping sets shall remain draft"),
        ):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    self._reduce_catalog_mapping_sources(root)
                    (root / "tools").mkdir()
                    shutil.copy2(
                        ROOT / "tools/v05_beta_release_gates.py",
                        root / "tools/v05_beta_release_gates.py",
                    )
                    record_path = root / RECORD_RELATIVE
                    record_path.parent.mkdir(parents=True)
                    record_path.write_text(
                        "---\n" + json.dumps(record_fixture("evidence_candidate")) + "\n---\n",
                        encoding="utf-8",
                    )
                    if mutation == "scope":
                        controls_path = root / "controls/catalog.json"
                        controls = json.loads(controls_path.read_text(encoding="utf-8"))
                        controls["control_count"] = 92
                        controls_path.write_text(json.dumps(controls), encoding="utf-8")
                    else:
                        catalog_path = root / "crosswalks/catalog.json"
                        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
                        catalog["mapping_sets"][0]["metadata"]["status"] = "published"
                        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
                    self._initialize_repository(root, commit=True)
                    if mutation == "scope":
                        shutil.copy2(ROOT / "controls/catalog.json", root / "controls/catalog.json")
                    else:
                        shutil.copy2(ROOT / "crosswalks/catalog.json", root / "crosswalks/catalog.json")
                    record_path.write_text(
                        "---\n" + json.dumps(record_fixture("closure_candidate")) + "\n---\n",
                        encoding="utf-8",
                    )
                    result = subprocess.run(
                        [
                            sys.executable,
                            "tools/v05_beta_release_gates.py",
                            "--check",
                            "--baseline-ref",
                            "HEAD",
                        ],
                        cwd=root,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(1, result.returncode)
                    self.assertIn(diagnostic, result.stdout)

    def test_cli_accepts_valid_baseline_when_current_scope_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            self._reduce_catalog_mapping_sources(root)
            (root / "tools").mkdir()
            shutil.copy2(
                ROOT / "tools/v05_beta_release_gates.py",
                root / "tools/v05_beta_release_gates.py",
            )
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "---\n" + json.dumps(record_fixture("evidence_candidate")) + "\n---\n",
                encoding="utf-8",
            )
            self._initialize_repository(root, commit=True)
            controls_path = root / "controls/catalog.json"
            controls = json.loads(controls_path.read_text(encoding="utf-8"))
            controls["control_count"] = 92
            controls_path.write_text(json.dumps(controls), encoding="utf-8")
            candidate = record_fixture("closure_candidate")
            candidate["scope"] = derive_scope(root)
            record_path.write_text(
                "---\n" + json.dumps(candidate) + "\n---\n", encoding="utf-8"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/v05_beta_release_gates.py",
                    "--check",
                    "--baseline-ref",
                    "HEAD",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stdout)

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

    def _initialize_repository(self, root: Path, *, commit: bool = False) -> None:
        subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
        subprocess.run(
            ["git", "-c", "core.autocrlf=false", "add", "."],
            cwd=root,
            check=True,
        )
        if commit:
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test User",
                    "-c",
                    "user.email=test@example.test",
                    "commit",
                    "--quiet",
                    "-m",
                    "baseline",
                ],
                cwd=root,
                check=True,
            )

    def _reduce_catalog_mapping_sources(self, root: Path) -> None:
        source = (
            ROOT
            / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/"
            "3.3/0.4-alpha/0.1.0/README.md"
        )
        target = root / "crosswalks/mappings/source.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        catalog_path = root / "crosswalks/catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for mapping_set in catalog["mapping_sets"]:
            mapping_set["path"] = "crosswalks/mappings/source.md"
            mapping_set["provisions"] = []
        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
