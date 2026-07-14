"""Validate authoritative crosswalk records and write or check generated catalogs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).absolute().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.crosswalks.catalog import (
    build_catalog,
    check_outputs,
    render_json,
    render_markdown,
)
from tools.crosswalks.validation import validate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--baseline-ref")
    return parser


def _diagnostic(error: str) -> str:
    if "; required:" in error:
        return error
    if ": " in error:
        path, observed = error.split(": ", 1)
    else:
        path, observed = "crosswalks", error
    return (
        f"{path}: validation: {observed}; required: correct the authoritative "
        "crosswalk source and rerun validation"
    )


def _print_errors(errors: list[str]) -> None:
    for error in sorted({_diagnostic(item) for item in errors}):
        print(f"- {error}")


def _summary(catalog: dict[str, object]) -> str:
    counts = catalog["counts"]
    assert isinstance(counts, dict)
    return (
        f"{counts['mapping_sets']} mapping sets, {counts['provisions']} provisions, "
        f"{counts['relationships']} relationships, and "
        f"{counts['negative_dispositions']} negative dispositions"
    )


def main(
    argv: Sequence[str] | None = None, *, root: Path | None = None
) -> int:
    arguments = _parser().parse_args(argv)
    repository = root if root is not None else ROOT
    result = validate(repository, baseline_ref=arguments.baseline_ref)
    if result.errors:
        _print_errors(result.errors)
        return 1

    catalog = build_catalog(result)
    if arguments.check:
        errors = check_outputs(repository, catalog)
        if errors:
            _print_errors(errors)
            return 1
    else:
        crosswalks = repository / "crosswalks"
        crosswalks.mkdir(parents=True, exist_ok=True)
        (crosswalks / "catalog.json").write_text(
            render_json(catalog), encoding="utf-8", newline="\n"
        )
        (crosswalks / "CATALOG.md").write_text(
            render_markdown(catalog), encoding="utf-8", newline="\n"
        )
    print(f"Crosswalk catalog valid: {_summary(catalog)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
