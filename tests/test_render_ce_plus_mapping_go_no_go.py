from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.render_ce_plus_mapping_go_no_go import render


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "tools/render_ce_plus_mapping_go_no_go.py"
DIRECTIONS = ("esaf_to_external", "external_to_esaf")


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def content_sha256(matrix: dict, direction: str) -> str:
    assessment = next(
        item for item in matrix["direction_assessments"]
        if item["direction"] == direction
    )
    content = {
        "direction_assessment": assessment,
        "probes": [
            probe for probe in matrix["probes"]
            if probe["direction"] == direction
        ],
    }
    return hashlib.sha256(canonical_json_bytes(content)).hexdigest()


class RenderMappingGoNoGoTests(unittest.TestCase):
    def fixture(self) -> dict:
        matrix = {
            "analysis_provenance": {
                "reconciliation": {
                    "packaging_disposition": "accepted",
                    "direction_validations": [
                        {"direction": direction, "status": "ACCEPTED"}
                        for direction in DIRECTIONS
                    ],
                },
                "direction_content_digests": [],
            },
            "direction_assessments": [
                {
                    "direction": direction,
                    "disposition": "GO",
                    "decision_rationale": f"Bounded feasibility exists for {direction}.",
                    "gate_results": [
                        {"gate": "source", "status": "PASS"},
                        {"gate": "rights", "status": "PASS"},
                    ],
                }
                for direction in DIRECTIONS
            ],
            "probes": [
                {
                    "probe_id": "etoe-1",
                    "direction": "esaf_to_external",
                    "groups": ["M", "T1"],
                    "kinds": ["prerequisite"],
                    "actors": ["Assessor"],
                    "special_scenario_bindings": [
                        {"scenario_id": "sampling-and-population-limits"}
                    ],
                    "conclusion": "POSITIVE_FEASIBILITY",
                },
                {
                    "probe_id": "etoe-2",
                    "direction": "external_to_esaf",
                    "groups": ["S"],
                    "kinds": ["procedure_step", "evidence_retention"],
                    "actors": ["Assessor", "Certifying Body"],
                    "special_scenario_bindings": [
                        {"scenario_id": "evidence-retention"},
                        {"scenario_id": "point-in-time-versus-continuous-assurance"},
                    ],
                    "conclusion": "NO_POSITIVE_BASIS",
                },
            ],
        }
        matrix["analysis_provenance"]["direction_content_digests"] = [
            {"direction": direction, "sha256": content_sha256(matrix, direction)}
            for direction in DIRECTIONS
        ]
        return matrix

    def test_render_is_deterministic_and_derived(self) -> None:
        first = render(self.fixture())
        second = render(self.fixture())
        self.assertEqual(first, second)
        self.assertIn("No mapping snapshot exists", first)
        self.assertIn("design only", first)
        for label in ("Groups", "Kinds", "Actors", "Special scenarios"):
            self.assertIn(label, first)
        for direction in DIRECTIONS:
            selected = [p for p in self.fixture()["probes"] if p["direction"] == direction]
            expected = {
                "Groups": len({v for p in selected for v in p["groups"]}),
                "Kinds": len({v for p in selected for v in p["kinds"]}),
                "Actors": len({v for p in selected for v in p["actors"]}),
                "Special scenarios": len({
                    b["scenario_id"] for p in selected
                    for b in p["special_scenario_bindings"]
                }),
            }
            section = first.split(f"## {direction}", 1)[1].split("## ", 1)[0]
            for label, total in expected.items():
                self.assertIn(f"| {label} | {total} |", section)

    def test_render_rejects_unknown_direction(self) -> None:
        fixture = self.fixture()
        fixture["direction_assessments"][0]["direction"] = "bidirectional"
        with self.assertRaisesRegex(ValueError, "unexpected direction order"):
            render(fixture)

    def test_render_rejects_unaccepted_or_digest_drifted_packaging(self) -> None:
        fixture = self.fixture()
        fixture["analysis_provenance"]["reconciliation"]["packaging_disposition"] = "rejected"
        with self.assertRaisesRegex(ValueError, "unaccepted reconciliation"):
            render(fixture)
        fixture = self.fixture()
        fixture["direction_assessments"][0]["decision_rationale"] += " changed"
        with self.assertRaisesRegex(ValueError, "direction content digest mismatch"):
            render(fixture)

    def test_render_requires_exact_direction_ordered_validations(self) -> None:
        invalid_arrays = (
            [],
            [{"direction": "esaf_to_external", "status": "ACCEPTED"}],
            [
                {"direction": "esaf_to_external", "status": "ACCEPTED"},
                {"direction": "esaf_to_external", "status": "ACCEPTED"},
            ],
            [
                {"direction": "external_to_esaf", "status": "ACCEPTED"},
                {"direction": "esaf_to_external", "status": "ACCEPTED"},
            ],
        )
        for validations in invalid_arrays:
            with self.subTest(validations=validations):
                fixture = self.fixture()
                fixture["analysis_provenance"]["reconciliation"]["direction_validations"] = validations
                with self.assertRaisesRegex(ValueError, "unaccepted reconciliation"):
                    render(fixture)
        fixture = self.fixture()
        del fixture["analysis_provenance"]["reconciliation"]["direction_validations"]
        with self.assertRaisesRegex(ValueError, "unaccepted reconciliation"):
            render(fixture)

    def test_cli_writes_checks_and_reports_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            matrix_path = root / "matrix.json"
            output_path = root / "review.md"
            matrix_path.write_text(json.dumps(self.fixture()), encoding="utf-8")
            write = subprocess.run(
                ["python", str(RENDERER), "--matrix", str(matrix_path),
                 "--output", str(output_path), "--write"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(write.returncode, 0, write.stderr)
            self.assertEqual(output_path.read_text(encoding="utf-8"), render(self.fixture()))
            check = subprocess.run(
                ["python", str(RENDERER), "--matrix", str(matrix_path),
                 "--output", str(output_path), "--check"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(check.returncode, 0, check.stderr)
            output_path.write_text("drift\n", encoding="utf-8")
            drift = subprocess.run(
                ["python", str(RENDERER), "--matrix", str(matrix_path),
                 "--output", str(output_path), "--check"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(drift.returncode, 1)

    def test_cli_operational_errors_exit_two(self) -> None:
        result = subprocess.run(
            ["python", str(RENDERER), "--matrix", "missing.json",
             "--output", "missing.md", "--check"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
