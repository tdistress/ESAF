#!/usr/bin/env python3
"""Validate the complete ESAF unit-test shard manifest."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.test_shards import tracked_test_modules, validate_manifest


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    """Run test-shard validation in check mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    arguments = parser.parse_args(argv)
    if not arguments.check:
        return 2
    try:
        shards = validate_manifest(ROOT)
        total = len(tracked_test_modules(ROOT))
    except ValueError as error:
        print(f"Test shard validation failed: {error}", file=sys.stderr)
        return 1
    for shard in shards:
        print(f"{shard.identifier}: {len(shard.modules)}")
    print(f"total tracked: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
