from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import unittest

from tools.v09_rc1_release_gates import (
    GATE_IDS,
    PHASE_GATE_STATES,
    PREVIOUS_PHASE,
    RECORD_RELATIVE,
    derive_scope,
    load_readiness_document,
    validate_readiness_body,
    validate_record,
)


ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / RECORD_RELATIVE


def _evidence_candidate_record(source: dict) -> dict:
    record = deepcopy(source)
    record["phase"] = "evidence_candidate"
    record["publication"] = {
        "date": None,
        "condition": record["publication"]["condition"],
        "evidence": [],
        "tag_object": None,
        "tagged_commit": None,
        "issue_evidence_url": None,
    }
    record["gates"] = {
        gate: {"state": "open", "evidence": []} for gate in GATE_IDS
    }
    return record


def _closure_candidate_record(source: dict) -> dict:
    record = deepcopy(source)
    record["phase"] = "closure_candidate"
    record["publication"] = {
        "date": None,
        "condition": record["publication"]["condition"],
        "evidence": [],
        "tag_object": None,
        "tagged_commit": None,
        "issue_evidence_url": None,
    }
    record["gates"] = {
        gate: {
            "state": PHASE_GATE_STATES["closure_candidate"][gate],
            "evidence": (
                []
                if gate == "post_merge"
                else ["https://github.com/tdistress/ESAF/pull/101"]
            ),
        }
        for gate in GATE_IDS
    }
    return record


def _previous_phase_ref(phase: object) -> str:
    from tools.v09_rc1_release_gates import CLOSURE_ALLOWLIST, changed_paths_since

    expected = PREVIOUS_PHASE[phase]  # type: ignore[index]
    # Prefer nearby ancestors first so a stacked allowlist commit validates
    # against its immediate evidence parent rather than a lagging origin/main.
    for ref in ("HEAD~1", "HEAD~2", "HEAD~3", "origin/main"):
        result = subprocess.run(
            ["git", "show", f"{ref}:{RECORD_RELATIVE}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            continue
        text = result.stdout
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            continue
        boundary = text.index("\n---\n", 4)
        import yaml

        value = yaml.safe_load(text[4:boundary])
        if not isinstance(value, dict) or value.get("phase") != expected:
            continue
        if phase == "closure_candidate":
            disallowed = sorted(
                changed_paths_since(ROOT, ref) - set(CLOSURE_ALLOWLIST)
            )
            if disallowed:
                continue
        return ref
    raise AssertionError(
        f"no git ref found with readiness phase {expected!r} for {phase!r}"
    )


class V09RC1ReleaseGatesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record, self.body = load_readiness_document(RECORD_PATH)

    def test_check_passes_on_current_repo_record(self) -> None:
        command = [sys.executable, "tools/v09_rc1_release_gates.py", "--check"]
        phase = self.record.get("phase")
        if phase in PREVIOUS_PHASE:
            command.extend(["--baseline-ref", _previous_phase_ref(phase)])
        result = subprocess.run(
            command,
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
                record = _evidence_candidate_record(self.record)
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

    def test_rejects_nonnull_publication_identity_for_candidate_phases(self) -> None:
        record = deepcopy(self.record)
        if record["phase"] == "published":
            record = _evidence_candidate_record(record)
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

    def test_evidence_candidate_ignores_baseline_ref(self) -> None:
        from unittest.mock import patch

        from tools.v09_rc1_release_gates import main

        evidence = _evidence_candidate_record(self.record)
        with patch(
            "tools.v09_rc1_release_gates.load_readiness_document",
            return_value=(evidence, self.body),
        ):
            with patch("sys.stderr", new_callable=lambda: __import__("io").StringIO()) as err:
                code = main(["--check", "--baseline-ref", "HEAD"])
                stderr = err.getvalue()
        self.assertEqual(0, code, msg=stderr)

    def test_closure_candidate_cli_requires_baseline_ref(self) -> None:
        from unittest.mock import patch

        from tools.v09_rc1_release_gates import main

        record = _closure_candidate_record(self.record)
        with patch(
            "tools.v09_rc1_release_gates.load_readiness_document",
            return_value=(record, self.body),
        ):
            with patch("sys.stderr", new_callable=lambda: __import__("io").StringIO()) as err:
                code = main(["--check"])
                stderr = err.getvalue()
        self.assertEqual(1, code)
        self.assertIn("baseline-ref is required for closure candidate", stderr)

    def test_closure_candidate_requires_ready_gates_with_https_evidence(self) -> None:
        record = _closure_candidate_record(self.record)
        record["publication"]["date"] = "2026-08-29"
        self.assertEqual([], validate_record(ROOT, record))

    def test_closure_candidate_rejects_missing_gate_evidence(self) -> None:
        record = _closure_candidate_record(self.record)
        for gate in GATE_IDS:
            record["gates"][gate]["evidence"] = []
        errors = validate_record(ROOT, record)
        self.assertTrue(any("evidence is required" in error for error in errors))

    def test_published_requires_tag_identity(self) -> None:
        record = _closure_candidate_record(self.record)
        record["phase"] = "published"
        record["publication"] = {
            "date": "2026-08-29",
            "condition": record["publication"]["condition"],
            "evidence": ["https://github.com/tdistress/ESAF/issues/95#issuecomment-1"],
            "tag_object": None,
            "tagged_commit": None,
            "issue_evidence_url": "https://github.com/tdistress/ESAF/issues/95#issuecomment-1",
        }
        record["gates"] = {
            gate: {
                "state": "closed",
                "evidence": ["https://github.com/tdistress/ESAF/issues/95#issuecomment-1"],
            }
            for gate in PHASE_GATE_STATES["published"]
        }
        errors = validate_record(ROOT, record)
        self.assertTrue(
            any("published tag object shall be a 40-character SHA" in e for e in errors)
        )

    def test_allowlist_helper_reports_disallowed_paths(self) -> None:
        from tools.v09_rc1_release_gates import CLOSURE_ALLOWLIST

        changed = {"VERSION.md", "tools/v09_rc1_release_gates.py", RECORD_RELATIVE}
        disallowed = sorted(changed - set(CLOSURE_ALLOWLIST))
        self.assertEqual(["tools/v09_rc1_release_gates.py"], disallowed)


if __name__ == "__main__":
    unittest.main()
