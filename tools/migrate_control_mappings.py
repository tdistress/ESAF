#!/usr/bin/env python3
"""Migrate control External mappings sections to the ESAF-1600 catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROLS = ROOT / "controls"
CANONICAL_EXTERNAL_MAPPING = (
    "Authoritative external mappings are maintained in the "
    "[ESAF-1600 generated catalog](../../crosswalks/CATALOG.md)."
)
EXTERNAL_MAPPING_SECTION = re.compile(
    r"^## External mappings\r?$\n(?P<section>.*?)(?=^## [^\r\n]+\r?$|\Z)",
    flags=re.MULTILINE | re.DOTALL,
)


def split_external_mapping(text: str) -> tuple[str, str, str]:
    """Return the exact prefix, stripped section content, and exact suffix."""
    matches = list(EXTERNAL_MAPPING_SECTION.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one '## External mappings' section; found {len(matches)}")
    match = matches[0]
    return text[: match.start()], match.group("section").strip(), text[match.end() :]


def replace_external_mapping(text: str, replacement: str) -> str:
    """Replace only the External mappings heading and content."""
    prefix, _section, suffix = split_external_mapping(text)
    return prefix + f"## External mappings\n\n{replacement.strip()}\n\n" + suffix


def control_record_paths(root: Path = ROOT) -> list[Path]:
    """Return control record paths declared by the generated control catalog."""
    catalog = json.loads((root / "controls" / "catalog.json").read_text(encoding="utf-8"))
    return [root / "controls" / record["path"] for record in catalog["controls"]]


def read_exact_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_exact_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="confirm all catalog controls delegate to ESAF-1600")
    mode.add_argument("--write", action="store_true", help="update all catalog controls to delegate to ESAF-1600")
    args = parser.parse_args()

    errors: list[str] = []
    changed = 0
    paths = control_record_paths()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        try:
            text = read_exact_text(path)
            _prefix, section, _suffix = split_external_mapping(text)
        except (OSError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
            continue
        if section == CANONICAL_EXTERNAL_MAPPING:
            continue
        if args.check:
            errors.append(f"{relative}: External mappings must delegate to ESAF-1600")
            continue
        write_exact_text(path, replace_external_mapping(text, CANONICAL_EXTERNAL_MAPPING))
        changed += 1

    if errors:
        print(f"Control mapping migration check failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    action = "updated" if args.write else "validated"
    print(f"Successfully {action} {len(paths)} catalog-derived control mapping sections ({changed} changed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
