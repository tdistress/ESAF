from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys


DIRECTIONS = ("esaf_to_external", "external_to_esaf")


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def direction_content_sha256(matrix: dict, direction: str) -> str:
    assessment = next(
        item for item in matrix["direction_assessments"]
        if item["direction"] == direction
    )
    content = {
        "direction_assessment": assessment,
        "probes": [p for p in matrix["probes"] if p["direction"] == direction],
    }
    return hashlib.sha256(canonical_json_bytes(content)).hexdigest()


def render(matrix: dict) -> str:
    assessments = matrix["direction_assessments"]
    if tuple(item["direction"] for item in assessments) != DIRECTIONS:
        raise ValueError("unexpected direction order")
    provenance = matrix["analysis_provenance"]
    reconciliation = provenance["reconciliation"]
    if (
        reconciliation["packaging_disposition"] != "accepted"
        or any(item["status"] != "ACCEPTED" for item in reconciliation["direction_validations"])
    ):
        raise ValueError("unaccepted reconciliation")
    recorded = {
        item["direction"]: item["sha256"]
        for item in provenance["direction_content_digests"]
    }
    if any(recorded.get(direction) != direction_content_sha256(matrix, direction) for direction in DIRECTIONS):
        raise ValueError("direction content digest mismatch")
    probes = matrix["probes"]
    lines = [
        "# Cyber Essentials Plus v3.2 Mapping Go/No-Go Review",
        "",
        "**Boundary:** No mapping snapshot exists. A GO authorizes design only.",
        "",
    ]
    for assessment in assessments:
        direction = assessment["direction"]
        selected = [probe for probe in probes if probe["direction"] == direction]
        counts = Counter(probe["conclusion"] for probe in selected)
        coverage = {
            "Groups": {value for probe in selected for value in probe["groups"]},
            "Kinds": {value for probe in selected for value in probe["kinds"]},
            "Actors": {value for probe in selected for value in probe["actors"]},
            "Special scenarios": {
                binding["scenario_id"]
                for probe in selected
                for binding in probe["special_scenario_bindings"]
            },
        }
        lines.extend([
            f"## {direction}",
            "",
            f"**Disposition:** {assessment['disposition']}",
            "",
            assessment["decision_rationale"],
            "",
            "| Gate | Status |",
            "|---|---|",
            *[f"| `{gate['gate']}` | `{gate['status']}` |" for gate in assessment["gate_results"]],
            "",
            f"Probes: {len(selected)}; positive: {counts['POSITIVE_FEASIBILITY']}; "
            f"no positive basis: {counts['NO_POSITIVE_BASIS']}; indeterminate: {counts['INDETERMINATE']}.",
            "",
            "| Coverage axis | Derived total |",
            "|---|---:|",
            *[f"| {label} | {len(values)} |" for label, values in coverage.items()],
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    try:
        matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
        rendered = render(matrix).encode("utf-8")
        if args.write:
            args.output.write_bytes(rendered)
            return 0
        return 0 if args.output.read_bytes() == rendered else 1
    except Exception as error:
        print(error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
