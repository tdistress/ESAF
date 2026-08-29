from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import unittest

from tools.v09_rc1_release_gates import (
    GATE_IDS,
    RECORD_RELATIVE,
    derive_scope,
    load_readiness_document,
    validate_readiness_body,
    validate_record,
)


ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / RECORD_RELATIVE


class V09RC1ReleaseGatesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record, self.body = load_readiness_document(RECORD_PATH)

    def test_check_passes_on_current_repo_record(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/v09_rc1_release_gates.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            0,
            result.returncode,
            msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
        )

    def test_happy_path_record_has_no_errors(self) -> None:
        errors = [
            *validate_record(ROOT, deepcopy(self.record)),
            *validate_readiness_body(self.body),
        ]
        self.assertEqual([], errors)

    def test_derived_scope_matches_recorded_scope(self) -> None:
        self.assertEqual(derive_scope(ROOT), self.record["scope"])

    def test_rejects_wrong_phase_string(self) -> None:
        record = deepcopy(self.record)
        record["phase"] = "closure_candidate_typo"
        errors = validate_record(ROOT, record)
        self.assertTrue(
            any("phase shall be evidence_candidate" in error for error in errors)
        )

    def test_rejects_wrong_gate_state_for_evidence_candidate(self) -> None:
        for gate in GATE_IDS:
            with self.subTest(gate=gate):
                record = deepcopy(self.record)
                record["gates"][gate]["state"] = "ready"
                errors = validate_record(ROOT, record)
                self.assertTrue(
                    any(
                        f"evidence_candidate phase shall set {gate} gate to 'open'"
                        in error
                        for error in errors
                    )
                )

    def test_rejects_missing_prerequisite_path(self) -> None:
        path_keys = (
            "phase2_evidence",
            "esaf_1300_path",
            "esaf_1400_path",
            "esaf_1700_path",
            "nist_ai_rmf_path",
        )
        for path_key in path_keys:
            with self.subTest(path_key=path_key):
                record = deepcopy(self.record)
                record["prerequisite_dispositions"][path_key] = (
                    "docs/superpowers/reviews/does-not-exist.md"
                )
                errors = validate_record(ROOT, record)
                self.assertTrue(
                    any(
                        f"prerequisite_dispositions.{path_key} does not exist"
                        in error
                        for error in errors
                    )
                )

    def test_rejects_prerequisite_disposition_value_drift(self) -> None:
        drifted = deepcopy(self.record)
        drifted["prerequisite_dispositions"]["nist_ai_rmf"] = "GO"
        errors = validate_record(ROOT, drifted)
        self.assertTrue(
            any(
                "prerequisite_dispositions.nist_ai_rmf shall equal 'HOLD'" in error
                for error in errors
            )
        )

    def test_rejects_prerequisite_missing_disposition_marker(self) -> None:
        record = deepcopy(self.record)
        record["prerequisite_dispositions"]["esaf_1300_path"] = (
            "docs/superpowers/reviews/2026-08-29-phase2-hosted-timing-deferral.md"
        )
        errors = validate_record(ROOT, record)
        self.assertTrue(
            any(
                "esaf_1300_path is missing a required disposition marker"
                in error
                for error in errors
            )
        )

    def test_rejects_scope_drift(self) -> None:
        for field, value in (
            ("controls", 999),
            ("control_families", 1),
            ("architecture_patterns", 0),
            ("mapping_sets", 1),
            ("mapping_provisions", 1),
            ("relationship_legs", 1),
            ("negative_dispositions", 1),
            ("assessment_foundation", False),
            ("draft_profiles", 0),
            ("pci_dss_disposition", "GO"),
            ("nist_ai_rmf_disposition", "GO"),
        ):
            with self.subTest(field=field):
                record = deepcopy(self.record)
                record["scope"][field] = value
                errors = validate_record(ROOT, record)
                self.assertIn(
                    "scope shall equal the derived repository scope", errors
                )

    def test_rejects_unknown_top_level_key(self) -> None:
        record = deepcopy(self.record)
        record["unexpected"] = True
        errors = validate_record(ROOT, record)
        self.assertIn("unknown top-level key unexpected", errors)

    def test_rejects_nonnull_publication_identity_for_evidence_candidate(self) -> None:
        record = deepcopy(self.record)
        record["publication"]["tag_object"] = "a" * 40
        errors = validate_record(ROOT, record)
        self.assertTrue(
            any("tag_object shall be null" in error for error in errors)
        )

    def test_rejects_missing_readiness_body_heading(self) -> None:
        body = self.body.replace("## Nonclaims", "## Renamed Section")
        errors = validate_readiness_body(body)
        self.assertTrue(
            any(
                "missing required heading: ## Nonclaims" in error
                for error in errors
            )
        )

    def test_evidence_candidate_rejects_baseline_ref(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "tools/v09_rc1_release_gates.py",
                "--check",
                "--baseline-ref",
                "HEAD",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn(
            "evidence_candidate shall not have a baseline-ref", result.stderr
        )


if __name__ == "__main__":
    unittest.main()
