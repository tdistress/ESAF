#!/usr/bin/env python3
"""Fail-closed validation of versioned ESAF profile packages."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Sequence

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_FILES = {
    "profile": "profile.json",
    "readme": "README.md",
    "control_selections": "control-selections.json",
    "risk_overlays": "risk-overlays.json",
    "evidence_expectations": "evidence-expectations.json",
    "external_references": "external-references.json",
}
DOCUMENT_SCHEMAS = {
    "profile": "profile.schema.json",
    "control_selections": "control-selections.schema.json",
    "risk_overlays": "risk-overlays.schema.json",
    "evidence_expectations": "evidence-expectations.schema.json",
    "external_references": "external-references.schema.json",
}


@dataclass(frozen=True)
class ProfilePackage:
    """A schema-valid profile package ready for semantic validation."""

    directory: Path
    relative: str
    documents: dict[str, dict[str, object]]


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build a JSON object while refusing duplicate keys."""
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError(f"duplicate JSON key {key!r}")
        document[key] = value
    return document


def load_json(path: Path) -> object:
    """Load JSON without accepting a lossy duplicate-key overwrite."""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def schema_diagnostics(
    schema: dict[str, object], document: object, relative: str
) -> list[str]:
    """Return deterministic Draft 2020-12 diagnostics for one document."""
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
    except SchemaError as exc:
        return [f"{relative}: invalid validation schema: {exc.message}"]

    diagnostics: list[str] = []
    for error in sorted(
        validator.iter_errors(document),
        key=lambda item: (tuple(str(part) for part in item.path), item.message),
    ):
        location = ".".join(str(part) for part in error.path) or "document"
        diagnostics.append(f"{relative}: {location}: {error.message}")
    return diagnostics


def discover_profile_packages(root: Path) -> tuple[Path, ...]:
    """Find only conventional ``profiles/<country>/<semver>`` packages."""
    profiles = root / "profiles"
    if not profiles.is_dir():
        return ()
    packages = [
        candidate.parent
        for candidate in profiles.glob("*/*/profile.json")
        if candidate.parent.parent.parent == profiles
        and candidate.parent.name.count(".") == 2
        and all(part.isdigit() for part in candidate.parent.name.split("."))
    ]
    return tuple(sorted(packages, key=lambda item: item.relative_to(root).as_posix()))


def safe_component(package: Path, relative: str) -> Path | None:
    """Resolve a normalized POSIX component path only within its package."""
    pure = PurePosixPath(relative)
    if (
        not relative
        or pure.is_absolute()
        or ".." in pure.parts
        or "\\" in relative
        or ":" in relative
        or pure.as_posix() != relative
        or not pure.parts
    ):
        return None
    candidate = package.joinpath(*pure.parts)
    if any(
        part.is_symlink()
        for part in (candidate, *candidate.parents)
        if part != package.parent
    ):
        return None
    try:
        candidate.resolve(strict=True).relative_to(package.resolve(strict=True))
    except (OSError, ValueError):
        return None
    return candidate


def package_relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def load_schema(root: Path, schema_name: str, diagnostics: list[str]) -> dict[str, object] | None:
    path = root / "profiles" / "schema" / schema_name
    relative = package_relative(root, path)
    try:
        schema = load_json(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        diagnostics.append(f"{relative}: cannot load schema: {exc}")
        return None
    if not isinstance(schema, dict):
        diagnostics.append(f"{relative}: schema root must be an object")
        return None
    return schema


def load_document(
    root: Path,
    package: Path,
    component: str,
    diagnostics: list[str],
) -> dict[str, object] | None:
    filename = PACKAGE_FILES[component]
    path = safe_component(package, filename)
    relative = package_relative(root, package / filename)
    if path is None:
        diagnostics.append(f"{relative}: unsafe or missing package component")
        return None
    try:
        document = load_json(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        diagnostics.append(f"{relative}: cannot load JSON: {exc}")
        return None
    if not isinstance(document, dict):
        diagnostics.append(f"{relative}: document root must be an object")
        return None
    schema = load_schema(root, DOCUMENT_SCHEMAS[component], diagnostics)
    if schema is None:
        return None
    diagnostics.extend(schema_diagnostics(schema, document, relative))
    if any(error.startswith(f"{relative}:") for error in diagnostics):
        return None
    return document


def load_package(
    root: Path, directory: Path, diagnostics: list[str]
) -> ProfilePackage | None:
    """Load one complete, schema-valid package without following aliases."""
    start = len(diagnostics)
    relative = package_relative(root, directory)
    if any(
        path.is_symlink()
        for path in (directory, *directory.parents)
        if path != root.parent
    ):
        diagnostics.append(f"{relative}: package directory must not be a symlink")
        return None

    expected_files = set(PACKAGE_FILES.values())
    actual_files = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    for filename in sorted(expected_files - actual_files):
        diagnostics.append(f"{relative}: missing package file {filename}")
    for filename in sorted(actual_files - expected_files):
        diagnostics.append(f"{relative}: unlisted package file {filename}")

    documents: dict[str, dict[str, object]] = {}
    profile = load_document(root, directory, "profile", diagnostics)
    if profile is None:
        return None
    documents["profile"] = profile

    components = profile.get("components")
    if not isinstance(components, dict):
        diagnostics.append(f"{relative}/profile.json: components must be an object")
    else:
        for component, filename in PACKAGE_FILES.items():
            if component == "profile":
                continue
            declared = components.get(component)
            if declared != filename:
                diagnostics.append(
                    f"{relative}/profile.json: component {component!r} must be {filename!r}"
                )
            elif safe_component(directory, declared) is None:
                diagnostics.append(
                    f"{relative}/profile.json: unsafe component path {declared!r}"
                )

    for component in DOCUMENT_SCHEMAS:
        if component == "profile":
            continue
        document = load_document(root, directory, component, diagnostics)
        if document is not None:
            documents[component] = document

    if len(diagnostics) != start:
        return None
    return ProfilePackage(directory=directory, relative=relative, documents=documents)


def validate(root: Path = ROOT) -> list[str]:
    """Return all deterministic content diagnostics for discovered packages."""
    diagnostics: list[str] = []
    for directory in discover_profile_packages(root):
        load_package(root, directory, diagnostics)
    return sorted(set(diagnostics))


def main(argv: Sequence[str] | None = None, *, root: Path | None = None) -> int:
    """Run profile validation in check mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    try:
        arguments = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    if not arguments.check:
        return 2

    try:
        validation_root = root if root is not None else ROOT
        diagnostics = validate(validation_root)
        package_count = len(discover_profile_packages(validation_root))
    except OSError as exc:
        print(f"Profile validation could not run: {exc}", file=sys.stderr)
        return 2
    if diagnostics:
        print(
            f"Profile validation failed with {len(diagnostics)} error(s):",
            file=sys.stderr,
        )
        for diagnostic in diagnostics:
            print(f"- {diagnostic}", file=sys.stderr)
        return 1
    print(f"Successfully validated {package_count} profile package(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
