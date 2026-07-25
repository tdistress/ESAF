#!/usr/bin/env python3
"""Fail-closed validation of versioned ESAF profile packages."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Sequence

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing.exceptions import Unresolvable

if __package__:
    from .crosswalks.io import parse_front_matter
    from .validate_assessment import (
        DIRECT_NEGATED_PROPOSITION,
        PROPOSITION_BOUNDARY,
        asserted_prohibited_phrases,
        quoted_occurrence_is_metalinguistic,
    )
else:
    from crosswalks.io import parse_front_matter
    from validate_assessment import (
        DIRECT_NEGATED_PROPOSITION,
        PROPOSITION_BOUNDARY,
        asserted_prohibited_phrases,
        quoted_occurrence_is_metalinguistic,
    )


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
SEMVER_PATTERN = r"[0-9]+\.[0-9]+\.[0-9]+"
SEMVER = re.compile(rf"^{SEMVER_PATTERN}$")
PROFILE_DOMAIN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROFILE_IDENTIFIER = re.compile(
    rf"^[a-z0-9]+(?:-[a-z0-9]+)*--"
    rf"[a-z0-9]+(?:-[a-z0-9]+)*--(?P<version>{SEMVER_PATTERN})$"
)
PROFILE_ROOT_FILES = frozenset({"ESAF-1800.md", "README.md"})
PROFILE_PROPOSITION_BOUNDARY = re.compile(
    rf"(?:{PROPOSITION_BOUNDARY.pattern})|[\r\n]",
    PROPOSITION_BOUNDARY.flags,
)
UK_PILOT_PROFILE_ID = "uk--jurisdiction-profile--0.1.0"
UK_PILOT_REGISTRY_PATHS = {
    (
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3"
        "--esaf-0.4-alpha--0.1.0"
    ): (
        "crosswalks/registry/"
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3"
        "--esaf-0.4-alpha--0.1.0.md"
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
        "--esaf-0.4-alpha--0.1.0"
    ): (
        "crosswalks/registry/"
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
        "--esaf-0.4-alpha--0.1.0.md"
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
        "--esaf-0.4-alpha--0.2.0"
    ): (
        "crosswalks/registry/"
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
        "--esaf-0.4-alpha--0.2.0.md"
    ),
}
UK_PILOT_MAPPING_REFERENCES = frozenset(UK_PILOT_REGISTRY_PATHS)
MAPPING_LIFECYCLE_STATES = ("approved", "published", "deprecated", "retired")
EXTERNAL_IMPORT_FIELDS = frozenset(
    {
        "relationship",
        "relationships",
        "disposition",
        "dispositions",
        "supported-outcome",
        "supported-outcomes",
        "equivalence",
        "evidence-import",
        "evidence-imports",
    }
)
LOCAL_MATURITY_FIELDS = frozenset(
    {
        "local-maturity-scale",
        "maturity-levels",
        "maturity-model",
        "maturity-scale",
    }
)
NON_IMPORT_STATEMENT = (
    "Relationships, external outcomes, and evidence are not imported."
)
PROFILE_ASSERTION_PATTERNS = (
    (
        "legal sufficiency",
        re.compile(
            r"\bestablish(?:es|ed|ing)?\s+(?:no\s+)?"
            r"(?P<outcome>legal sufficiency)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "external approval",
        re.compile(
            r"\bestablish(?:es|ed|ing)?\s+(?:no\s+)?"
            r"(?P<outcome>external approval)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production readiness",
        re.compile(
            r"\bestablish(?:es|ed|ing)?\s+(?:no\s+)?"
            r"(?P<outcome>production readiness)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "legal sufficiency",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>legally sufficient)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "legal sufficiency",
        re.compile(
            r"\b(?:provides?|demonstrates?)\s+(?:no\s+)?"
            r"(?P<outcome>legal sufficiency)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "external approval",
        re.compile(
            r"\b(?:has|have|had)\s+(?:no\s+)?"
            r"(?P<outcome>external approval)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "external approval",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>externally approved)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production readiness",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>production[- ]ready|ready for production)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production readiness",
        re.compile(
            r"\b(?:demonstrates?|provides?)\s+(?:no\s+)?"
            r"(?P<outcome>production readiness)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "compliance",
        re.compile(
            r"\bcertif(?:y|ies|ied)\s+(?:no\s+)?"
            r"(?P<outcome>compliance)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "compliance",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>compliant)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "certification",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>certified)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "equivalence",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>equivalent)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "endorsement",
        re.compile(
            r"\b(?:is|are|was|were)\s+(?:not\s+)?"
            r"(?P<outcome>endorsed)\b",
            re.IGNORECASE,
        ),
    ),
)
WEAKENING_PREDICATE = re.compile(
    r"\b(?:replace(?:s|d|ing)?|alter(?:s|ed|ing)?|relax(?:es|ed|ing)?"
    r"|waiv(?:e|es|ed|ing)|weaken(?:s|ed|ing)?|narrow(?:s|ed|ing)?"
    r"|mark(?:s|ed|ing)?|mak(?:e|es|ing))\b",
    re.IGNORECASE,
)
PASSIVE_WEAKENING = re.compile(
    r"\b(?P<control>(?:core\s+)?controls?(?:\s+requirements?)?)\s+"
    r"(?:is|are|was|were)\s+(?:not\s+)?"
    r"(?P<predicate>replaced|waived|made\s+optional|altered|relaxed|weakened|"
    r"narrowed|marked\s+inapplicable)\b",
    re.IGNORECASE,
)
CONTROL_LANGUAGE = re.compile(
    r"\b(?:core\s+)?controls?(?:\s+requirements?)?\b",
    re.IGNORECASE,
)
PREDICATE_NEGATION = re.compile(
    r"\b(?:cannot|can['’]t|doesn['’]t|isn['’]t|must\s+not|never|not"
    r"|shall\s+not|wasn['’]t|weren['’]t)\b",
    re.IGNORECASE,
)
POST_PREDICATE_NEGATION = re.compile(
    r"\b(?:no|neither)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ProfilePackage:
    """A schema-valid profile package ready for semantic validation."""

    directory: Path
    relative: str
    documents: dict[str, dict[str, object]]


class OperationalProfileError(RuntimeError):
    """A sanitized repository-relative operational validation failure."""


def lstat_mode(path: Path, diagnostic: str) -> int | None:
    """Return an entry mode without suppressing operational stat failures."""
    try:
        return path.lstat().st_mode
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise OperationalProfileError(diagnostic) from exc


def bounded_paths(path: Path, boundary: Path) -> tuple[Path, ...]:
    """Return ``path`` and lexical parents only through ``boundary``."""
    try:
        path.relative_to(boundary)
    except ValueError:
        return ()
    result: list[Path] = []
    current = path
    while True:
        result.append(current)
        if current == boundary:
            return tuple(result)
        current = current.parent


def entry_is_alias(
    path: Path, diagnostic: str, mode: int | None = None
) -> bool:
    """Inspect a path for aliasing while preserving operational failures."""
    observed_mode = mode if mode is not None else lstat_mode(path, diagnostic)
    if observed_mode is None:
        return False
    if stat.S_ISLNK(observed_mode):
        return True
    try:
        return path.is_junction()
    except OSError as exc:
        raise OperationalProfileError(diagnostic) from exc


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
        validator = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )
    except SchemaError as exc:
        return [f"{relative}: invalid validation schema: {exc.message}"]

    try:
        errors = sorted(
            validator.iter_errors(document),
            key=lambda item: (
                tuple(str(part) for part in item.path),
                item.message,
            ),
        )
    except Unresolvable as exc:
        raise OperationalProfileError(
            f"{relative}: cannot resolve validation schema"
        ) from exc

    diagnostics: list[str] = []
    for error in errors:
        location = ".".join(str(part) for part in error.path) or "document"
        diagnostics.append(f"{relative}: {location}: {error.message}")
    return diagnostics


def inventory_profile_packages(
    root: Path,
) -> tuple[tuple[Path, ...], list[str]]:
    """Inventory every profile-domain entry without silently skipping content."""
    profiles = root / "profiles"
    packages: list[Path] = []
    diagnostics: list[str] = []
    try:
        profiles_mode = lstat_mode(
            profiles, "profiles: cannot inspect profile root"
        )
        if profiles_mode is None:
            diagnostics.append("profiles: profile root is missing")
        elif entry_is_alias(
            profiles, "profiles: cannot inspect profile root", profiles_mode
        ):
            diagnostics.append(
                "profiles: profile root must not be a symlink or junction alias"
            )
        elif not stat.S_ISDIR(profiles_mode):
            diagnostics.append("profiles: profile root must be a directory")
        else:
            for domain in sorted(profiles.iterdir(), key=lambda item: item.name):
                relative = domain.relative_to(root).as_posix()
                domain_mode = lstat_mode(
                    domain, f"{relative}: cannot inspect profile inventory entry"
                )
                if domain_mode is None:
                    raise OperationalProfileError(
                        f"{relative}: profile inventory entry disappeared"
                    )
                if entry_is_alias(
                    domain,
                    f"{relative}: cannot inspect profile inventory entry",
                    domain_mode,
                ):
                    if domain.name == "schema":
                        diagnostics.append(
                            f"{relative}: schema root or file must not be a "
                            "symlink or junction alias"
                        )
                    else:
                        diagnostics.append(
                            f"{relative}: profile inventory entry must not be a "
                            "symlink or junction alias"
                        )
                    continue
                if domain.name in PROFILE_ROOT_FILES:
                    if not stat.S_ISREG(domain_mode):
                        diagnostics.append(
                            f"{relative}: profile index entry must be a file"
                        )
                    continue
                if domain.name == "schema":
                    if not stat.S_ISDIR(domain_mode):
                        diagnostics.append(
                            f"{relative}: schema entry must be a directory"
                        )
                    continue
                if not stat.S_ISDIR(domain_mode):
                    diagnostics.append(
                        f"{relative}: unexpected profile inventory entry"
                    )
                    continue
                if not PROFILE_DOMAIN.fullmatch(domain.name):
                    diagnostics.append(
                        f"{relative}: invalid profile domain directory"
                    )
                    continue

                version_entries = tuple(
                    sorted(domain.iterdir(), key=lambda item: item.name)
                )
                if not version_entries:
                    diagnostics.append(
                        f"{relative}: profile domain contains no version entries"
                    )
                for version in version_entries:
                    version_relative = version.relative_to(root).as_posix()
                    version_mode = lstat_mode(
                        version,
                        f"{version_relative}: cannot inspect profile version entry",
                    )
                    if version_mode is None:
                        raise OperationalProfileError(
                            f"{version_relative}: profile version entry disappeared"
                        )
                    if entry_is_alias(
                        version,
                        f"{version_relative}: cannot inspect profile version entry",
                        version_mode,
                    ):
                        diagnostics.append(
                            f"{version_relative}: profile version directory "
                            "must not be a symlink or junction alias"
                        )
                        continue
                    if not stat.S_ISDIR(version_mode):
                        diagnostics.append(
                            f"{version_relative}: unexpected profile version entry"
                        )
                        continue
                    if not SEMVER.fullmatch(version.name):
                        diagnostics.append(
                            f"{version_relative}: invalid profile version directory"
                        )
                        continue
                    manifest = version / PACKAGE_FILES["profile"]
                    manifest_relative = manifest.relative_to(root).as_posix()
                    manifest_mode = lstat_mode(
                        manifest,
                        f"{manifest_relative}: cannot inspect profile manifest",
                    )
                    if manifest_mode is None:
                        diagnostics.append(
                            f"{version_relative}: missing profile manifest "
                            f"{PACKAGE_FILES['profile']}"
                        )
                    elif entry_is_alias(
                        manifest,
                        f"{manifest_relative}: cannot inspect profile manifest",
                        manifest_mode,
                    ):
                        diagnostics.append(
                            f"{manifest_relative}: "
                            "profile manifest must not be a symlink or junction alias"
                        )
                    elif not stat.S_ISREG(manifest_mode):
                        diagnostics.append(
                            f"{manifest_relative}: profile manifest must be a "
                            "regular file"
                        )
                    packages.append(version)
    except OSError as exc:
        raise OperationalProfileError(
            "profiles: cannot inventory profile packages"
        ) from exc

    if not packages:
        diagnostics.append("profiles: no profile packages found")
    return tuple(sorted(packages)), sorted(set(diagnostics))


def discover_profile_packages(root: Path) -> tuple[Path, ...]:
    """Return conventional packages from the fail-closed inventory."""
    return inventory_profile_packages(root)[0]


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
        entry_is_alias(
            part, "profile package: cannot inspect package component path"
        )
        for part in bounded_paths(candidate, package)
    ):
        return None
    candidate_mode = lstat_mode(
        candidate, "profile package: cannot inspect package component"
    )
    if candidate_mode is None or not stat.S_ISREG(candidate_mode):
        return None
    try:
        candidate.resolve(strict=True).relative_to(package.resolve(strict=True))
    except (FileNotFoundError, ValueError):
        return None
    except OSError as exc:
        raise OperationalProfileError(
            "profile package: cannot resolve package component"
        ) from exc
    return candidate


def package_relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def safe_schema(root: Path, schema_name: str) -> Path | None:
    """Resolve a schema only when it is a real file under ``profiles/schema``."""
    schema_root = root / "profiles" / "schema"
    candidate = schema_root / schema_name
    if any(
        entry_is_alias(
            part, "profiles/schema: cannot inspect validation schema path"
        )
        for part in bounded_paths(candidate, root)
    ):
        return None
    candidate_mode = lstat_mode(
        candidate, "profiles/schema: cannot inspect validation schema"
    )
    if candidate_mode is None or not stat.S_ISREG(candidate_mode):
        return None
    try:
        root_resolved = root.resolve(strict=True)
        schema_root_resolved = schema_root.resolve(strict=True)
        schema_root_resolved.relative_to(root_resolved)
        candidate.resolve(strict=True).relative_to(schema_root_resolved)
    except (FileNotFoundError, ValueError):
        return None
    except OSError as exc:
        raise OperationalProfileError(
            "profiles/schema: cannot resolve validation schema"
        ) from exc
    return candidate


def safe_repository_file(
    root: Path, relative: str, *, expected_root: str
) -> Path:
    """Resolve one normalized regular file beneath a repository subdirectory."""
    pure = PurePosixPath(relative)
    expected = PurePosixPath(expected_root)
    reference_kind = (
        "registry"
        if expected_root == "crosswalks/registry"
        else "snapshot"
    )
    if (
        not relative
        or pure.is_absolute()
        or ".." in pure.parts
        or "\\" in relative
        or ":" in relative
        or pure.as_posix() != relative
        or pure.parts[: len(expected.parts)] != expected.parts
    ):
        raise ValueError(
            f"unsafe or missing {reference_kind} path {relative!r}"
        )
    candidate = root.joinpath(*pure.parts)
    if any(
        entry_is_alias(
            part, f"{expected_root}: cannot inspect repository reference path"
        )
        for part in bounded_paths(candidate, root)
    ):
        raise ValueError(
            f"unsafe or missing {reference_kind} path {relative!r}"
        )
    candidate_mode = lstat_mode(
        candidate, f"{expected_root}: cannot inspect repository reference"
    )
    if candidate_mode is None or not stat.S_ISREG(candidate_mode):
        raise ValueError(
            f"unsafe or missing {reference_kind} path {relative!r}"
        )
    try:
        expected_directory = root.joinpath(*expected.parts).resolve(strict=True)
        candidate.resolve(strict=True).relative_to(expected_directory)
    except (FileNotFoundError, ValueError) as exc:
        raise ValueError(
            f"unsafe or missing {reference_kind} path {relative!r}"
        ) from exc
    except OSError as exc:
        raise OperationalProfileError(
            f"{expected_root}: cannot resolve repository reference"
        ) from exc
    return candidate


def load_schema(root: Path, schema_name: str, diagnostics: list[str]) -> dict[str, object] | None:
    nominal_path = root / "profiles" / "schema" / schema_name
    relative = package_relative(root, nominal_path)
    path = safe_schema(root, schema_name)
    if path is None:
        diagnostics.append(
            f"{relative}: schema root or file is missing, symlinked, or outside profiles/schema"
        )
        return None
    try:
        schema = load_json(path)
    except OSError as exc:
        raise OperationalProfileError(
            f"{relative}: cannot read validation schema"
        ) from exc
    except (json.JSONDecodeError, ValueError) as exc:
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
    except OSError as exc:
        raise OperationalProfileError(
            f"{relative}: cannot read package component"
        ) from exc
    except (json.JSONDecodeError, ValueError) as exc:
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
        entry_is_alias(
            path, f"{relative}: cannot inspect package directory path"
        )
        for path in bounded_paths(directory, root)
    ):
        diagnostics.append(f"{relative}: package directory must not be a symlink")
        return None

    expected_files = set(PACKAGE_FILES.values())
    try:
        actual_entries = {
            path.name: path for path in directory.iterdir()
        }
    except OSError as exc:
        raise OperationalProfileError(
            f"{relative}: cannot inventory package contents"
        ) from exc
    for filename in sorted(expected_files):
        path = actual_entries.get(filename)
        component_relative = f"{relative}/{filename}"
        if path is None:
            diagnostics.append(f"{relative}: missing package file {filename}")
            continue
        mode = lstat_mode(
            path, f"{component_relative}: cannot inspect package component"
        )
        if mode is None:
            diagnostics.append(f"{relative}: missing package file {filename}")
        elif entry_is_alias(
            path,
            f"{component_relative}: cannot inspect package component",
            mode,
        ):
            diagnostics.append(
                f"{component_relative}: package component must not be a "
                "symlink or junction alias"
            )
        elif not stat.S_ISREG(mode):
            diagnostics.append(
                f"{component_relative}: package component must be a regular file"
            )
    for entry, path in sorted(actual_entries.items()):
        if entry in expected_files:
            continue
        entry_relative = f"{relative}/{entry}"
        mode = lstat_mode(
            path, f"{entry_relative}: cannot inspect unlisted package entry"
        )
        if mode is None:
            raise OperationalProfileError(
                f"{entry_relative}: unlisted package entry disappeared"
            )
        if entry_is_alias(
            path,
            f"{entry_relative}: cannot inspect unlisted package entry",
            mode,
        ):
            kind = "symlink or junction alias"
        elif stat.S_ISDIR(mode):
            kind = "entry"
        else:
            kind = "file"
        diagnostics.append(f"{relative}: unlisted package {kind} {entry}")

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


def control_population(root: Path) -> set[str]:
    """Load the authoritative ESAF control identifiers."""
    try:
        catalog = load_json(root / "controls" / "catalog.json")
    except OSError as exc:
        raise OperationalProfileError(
            "controls/catalog.json: cannot read control catalog"
        ) from exc
    if not isinstance(catalog, dict):
        raise ValueError("controls/catalog.json root must be an object")
    controls = catalog.get("controls")
    if not isinstance(controls, list):
        raise ValueError("controls/catalog.json controls must be an array")
    identifiers: list[str] = []
    for index, record in enumerate(controls):
        if not isinstance(record, dict) or not isinstance(record.get("id"), str):
            raise ValueError(
                f"controls/catalog.json controls[{index}] requires a string id"
            )
        identifiers.append(record["id"])
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("controls/catalog.json contains duplicate control ids")
    return set(identifiers)


def mapping_reference_metadata(
    root: Path, mapping_set_id: str, registry_path: str
) -> dict[str, object]:
    """Resolve declared mapping metadata without conflating editorial state."""
    canonical_registry_path = (
        f"crosswalks/registry/{mapping_set_id}.md"
    )
    if registry_path != canonical_registry_path:
        raise ValueError(
            "registry path must be canonical "
            f"{canonical_registry_path!r}"
        )
    registry_file = safe_repository_file(
        root, registry_path, expected_root="crosswalks/registry"
    )
    try:
        registry, _ = parse_front_matter(registry_file)
    except yaml.YAMLError as exc:
        raise ValueError("cannot parse registry front matter") from exc
    except (UnicodeError, ValueError) as exc:
        raise ValueError(
            f"cannot load registry front matter: {exc}"
        ) from exc
    events = registry.get("events")
    if not isinstance(events, list):
        raise ValueError("registry lifecycle events must be an array")
    catalog = load_json(root / "crosswalks" / "catalog.json")
    if not isinstance(catalog, dict):
        raise ValueError("crosswalks/catalog.json root must be an object")
    mapping_sets = catalog.get("mapping_sets")
    if not isinstance(mapping_sets, list):
        raise ValueError(
            "crosswalks/catalog.json mapping_sets must be an array"
        )
    matches = [
        record
        for record in mapping_sets
        if isinstance(record, dict)
        and isinstance(record.get("metadata"), dict)
        and record["metadata"].get("mapping_set_id") == mapping_set_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"mapping set {mapping_set_id} does not resolve exactly once"
        )
    record = matches[0]
    metadata = record["metadata"]
    editorial_status = metadata.get("status")
    snapshot_path = record.get("path")
    if not isinstance(editorial_status, str):
        raise ValueError(
            f"mapping set {mapping_set_id} has no editorial status"
        )
    if not isinstance(snapshot_path, str):
        raise ValueError(f"mapping set {mapping_set_id} has no snapshot path")
    snapshot_file = safe_repository_file(
        root, snapshot_path, expected_root="crosswalks/mappings"
    )
    try:
        snapshot, _ = parse_front_matter(snapshot_file)
    except yaml.YAMLError as exc:
        raise ValueError("cannot parse snapshot front matter") from exc
    except (UnicodeError, ValueError) as exc:
        raise ValueError(
            f"cannot load snapshot front matter: {exc}"
        ) from exc
    if registry.get("mapping_set_id") != mapping_set_id:
        raise ValueError(
            f"registry mapping_set_id does not match {mapping_set_id}"
        )
    if snapshot.get("mapping_set_id") != mapping_set_id:
        raise ValueError(
            f"snapshot mapping_set_id does not match {mapping_set_id}"
        )
    snapshot_status = snapshot.get("status")
    if snapshot_status != editorial_status:
        raise ValueError(
            f"snapshot editorial status {snapshot_status} does not match "
            f"catalog {editorial_status}"
        )
    return {
        "mapping_set_id": mapping_set_id,
        "editorial_status": editorial_status,
        "snapshot_path": snapshot_path,
        "registry_events": events,
    }


def mapping_lifecycle_diagnostics(
    metadata: dict[str, object], expected_status: str
) -> list[str]:
    """Validate snapshot editorial state and governed lifecycle separately."""
    diagnostics: list[str] = []
    editorial_status = metadata.get("editorial_status")
    events = metadata.get("registry_events")
    if not isinstance(events, list):
        return ["registry lifecycle events must be an array"]

    expected_editorial = (
        expected_status
        if expected_status in {"draft", "reviewed", "approved"}
        else "approved"
    )
    if editorial_status != expected_editorial:
        diagnostics.append(
            f"expected editorial status {expected_editorial}; "
            f"found {editorial_status}"
        )

    states = [
        event.get("state") if isinstance(event, dict) else None
        for event in events
    ]
    if editorial_status in {"draft", "reviewed"}:
        if events:
            diagnostics.append(
                f"{editorial_status} mapping snapshot requires empty "
                "registry lifecycle events"
            )
        return diagnostics

    if editorial_status == "approved":
        if not events:
            diagnostics.append(
                "approved mapping snapshot requires governed registry "
                "lifecycle events"
            )
            return diagnostics
        if states != list(MAPPING_LIFECYCLE_STATES[: len(states)]):
            diagnostics.append("invalid governed registry lifecycle event prefix")
            return diagnostics
        observed_status = states[-1]
        if observed_status != expected_status:
            diagnostics.append(
                f"expected lifecycle status {expected_status}; "
                f"found {observed_status}"
            )
    return diagnostics


def objects(value: object) -> list[dict[str, object]]:
    """Return the object members of a schema-validated array."""
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def strings(value: object) -> list[str]:
    """Return the string members of a schema-validated array."""
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def duplicate_identifiers(
    records: list[dict[str, object]], field: str
) -> set[str]:
    identifiers = [
        value
        for record in records
        if isinstance((value := record.get(field)), str)
    ]
    return {
        identifier
        for identifier in identifiers
        if identifiers.count(identifier) > 1
    }


def semantic_diagnostics(
    root: Path, package: ProfilePackage
) -> list[str]:
    """Validate catalog coverage, condition use, identity, and lifecycle pins."""
    diagnostics: list[str] = []
    profile = package.documents["profile"]
    selections_document = package.documents["control_selections"]
    risk_document = package.documents["risk_overlays"]
    evidence_document = package.documents["evidence_expectations"]
    reference_document = package.documents["external_references"]

    expected_profile_id = profile.get("profile_id")
    expected_profile_version = profile.get("profile_version")
    identifier_match = (
        PROFILE_IDENTIFIER.fullmatch(expected_profile_id)
        if isinstance(expected_profile_id, str)
        else None
    )
    if identifier_match is not None and isinstance(
        expected_profile_version, str
    ):
        identifier_version = identifier_match.group("version")
        if identifier_version != expected_profile_version:
            diagnostics.append(
                f"{package.relative}/profile.json: profile_id version "
                f"{identifier_version} does not match profile_version "
                f"{expected_profile_version}"
            )
        if expected_profile_version != package.directory.name:
            diagnostics.append(
                f"{package.relative}/profile.json: profile_version "
                f"{expected_profile_version} does not match profile version "
                f"directory {package.directory.name}"
            )
    for component, document in sorted(package.documents.items()):
        if component == "profile":
            continue
        relative = f"{package.relative}/{PACKAGE_FILES[component]}"
        if document.get("profile_id") != expected_profile_id:
            diagnostics.append(
                f"{relative}: profile_id does not match profile.json"
            )
        if document.get("profile_version") != expected_profile_version:
            diagnostics.append(
                f"{relative}: profile_version does not match profile.json"
            )

    conditions = objects(profile.get("applicability_conditions"))
    risks = objects(risk_document.get("risks"))
    overlays = objects(risk_document.get("overlays"))
    expectations = objects(evidence_document.get("expectations"))
    selections = objects(selections_document.get("selections"))
    duplicate_sets = (
        (
            conditions,
            "condition_id",
            "applicability condition",
            "profile.json",
        ),
        (risks, "risk_id", "risk", "risk-overlays.json"),
        (overlays, "overlay_id", "overlay", "risk-overlays.json"),
        (
            expectations,
            "expectation_id",
            "evidence expectation",
            "evidence-expectations.json",
        ),
    )
    for records, field, label, filename in duplicate_sets:
        for identifier in sorted(duplicate_identifiers(records, field)):
            diagnostics.append(
                f"{package.relative}/{filename}: duplicate {label} {identifier}"
            )

    population = control_population(root)
    selection_ids = [
        value
        for selection in selections
        if isinstance((value := selection.get("control_id")), str)
    ]
    for identifier in sorted(set(selection_ids) - population):
        diagnostics.append(
            f"{package.relative}/control-selections.json: "
            f"unknown control selection {identifier}"
        )
    for identifier in sorted(population - set(selection_ids)):
        diagnostics.append(
            f"{package.relative}/control-selections.json: "
            f"missing control selection {identifier}"
        )
    for identifier in sorted(
        identifier
        for identifier in set(selection_ids)
        if selection_ids.count(identifier) > 1
    ):
        diagnostics.append(
            f"{package.relative}/control-selections.json: "
            f"duplicate control selection {identifier}"
        )
    if len(selection_ids) != len(population):
        diagnostics.append(
            f"{package.relative}/control-selections.json: "
            f"selection record count {len(selection_ids)} does not match "
            f"control population {len(population)}"
        )

    condition_ids = {
        value
        for condition in conditions
        if isinstance((value := condition.get("condition_id")), str)
    }
    condition_users = [
        ("control-selections.json", selection)
        for selection in selections
    ]
    condition_users.extend(
        ("risk-overlays.json", overlay) for overlay in overlays
    )
    condition_users.extend(
        ("evidence-expectations.json", expectation)
        for expectation in expectations
    )
    for filename, record in condition_users:
        for identifier in strings(record.get("activation_conditions")):
            if identifier not in condition_ids:
                diagnostics.append(
                    f"{package.relative}/{filename}: unresolved "
                    f"applicability condition {identifier}"
                )

    for selection in selections:
        status = selection.get("status")
        activation_conditions = strings(
            selection.get("activation_conditions")
        )
        if status == "conditional" and not activation_conditions:
            diagnostics.append(
                f"{package.relative}/control-selections.json: conditional "
                "selection requires activation conditions"
            )
        if status != "conditional" and activation_conditions:
            diagnostics.append(
                f"{package.relative}/control-selections.json: only conditional "
                "selections may use activation conditions"
            )
    for overlay in overlays:
        applicability = overlay.get("applicability")
        activation_conditions = strings(overlay.get("activation_conditions"))
        if applicability == "conditional" and not activation_conditions:
            diagnostics.append(
                f"{package.relative}/risk-overlays.json: conditional overlay "
                "requires activation conditions"
            )
        if applicability != "conditional" and activation_conditions:
            diagnostics.append(
                f"{package.relative}/risk-overlays.json: only conditional "
                "overlays may use activation conditions"
            )

    references = objects(reference_document.get("external_references"))
    reference_ids = [
        value
        for reference in references
        if isinstance((value := reference.get("mapping_set_id")), str)
    ]
    for identifier in sorted(
        identifier
        for identifier in set(reference_ids)
        if reference_ids.count(identifier) > 1
    ):
        diagnostics.append(
            f"{package.relative}/external-references.json: "
            f"duplicate mapping reference {identifier}"
        )

    for reference in references:
        identifier = reference.get("mapping_set_id")
        observed_path = reference.get("registry_path")
        expected_status = reference.get("expected_status")
        if (
            not isinstance(identifier, str)
            or not isinstance(observed_path, str)
            or not isinstance(expected_status, str)
        ):
            continue
        try:
            metadata = mapping_reference_metadata(
                root, identifier, observed_path
            )
        except OSError as exc:
            raise OperationalProfileError(
                f"{observed_path}: cannot read mapping reference metadata"
            ) from exc
        except (UnicodeError, ValueError) as exc:
            diagnostics.append(
                f"{package.relative}/external-references.json: mapping "
                f"{identifier}: {exc}"
            )
            continue
        if metadata.get("mapping_set_id") != identifier:
            diagnostics.append(
                f"{observed_path}: registry mapping_set_id does not match "
                f"{identifier}"
            )
        for lifecycle_diagnostic in mapping_lifecycle_diagnostics(
            metadata, expected_status
        ):
            diagnostics.append(
                f"{observed_path}: {lifecycle_diagnostic}"
            )

    if expected_profile_id == UK_PILOT_PROFILE_ID:
        for identifier in sorted(
            set(reference_ids) - UK_PILOT_MAPPING_REFERENCES
        ):
            diagnostics.append(
                f"{package.relative}/external-references.json: unexpected "
                f"UK pilot mapping reference {identifier}"
            )
        for identifier in sorted(
            UK_PILOT_MAPPING_REFERENCES - set(reference_ids)
        ):
            diagnostics.append(
                f"{package.relative}/external-references.json: missing "
                f"UK pilot mapping reference {identifier}"
            )
        if (
            len(references) != 3
            or set(reference_ids) != UK_PILOT_MAPPING_REFERENCES
        ):
            diagnostics.append(
                f"{package.relative}/external-references.json: UK pilot "
                "mapping references must contain exactly three references"
            )
        for reference in references:
            identifier = reference.get("mapping_set_id")
            if (
                not isinstance(identifier, str)
                or identifier not in UK_PILOT_REGISTRY_PATHS
            ):
                continue
            expected_path = UK_PILOT_REGISTRY_PATHS[identifier]
            if reference.get("registry_path") != expected_path:
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} registry path must be {expected_path!r}"
                )
            if reference.get("expected_status") != "draft":
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} expected_status must be 'draft'"
                )
            if reference.get("reference_use") != "lifecycle_reference_only":
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} reference_use must be "
                    "'lifecycle_reference_only'"
                )
            if reference.get("qualified_review_required") is not True:
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} requires qualified review"
                )
            if reference.get("non_import_statement") != NON_IMPORT_STATEMENT:
                diagnostics.append(
                    f"{package.relative}/external-references.json: mapping "
                    f"{identifier} non_import_statement must be "
                    f"{NON_IMPORT_STATEMENT!r}"
                )
    return sorted(set(diagnostics))


def traceability_diagnostics(package: ProfilePackage) -> list[str]:
    """Validate the closed risk, overlay, and evidence reference graph."""
    diagnostics: list[str] = []
    risk_document = package.documents["risk_overlays"]
    evidence_document = package.documents["evidence_expectations"]
    risks = objects(risk_document.get("risks"))
    overlays = objects(risk_document.get("overlays"))
    expectations = objects(evidence_document.get("expectations"))
    risk_map = {
        record["risk_id"]: record
        for record in risks
        if isinstance(record.get("risk_id"), str)
    }
    overlay_map = {
        record["overlay_id"]: record
        for record in overlays
        if isinstance(record.get("overlay_id"), str)
    }
    evidence_map = {
        record["expectation_id"]: record
        for record in expectations
        if isinstance(record.get("expectation_id"), str)
    }
    population = {
        selection["control_id"]
        for selection in objects(
            package.documents["control_selections"].get("selections")
        )
        if isinstance(selection.get("control_id"), str)
    }

    def check_controls(filename: str, record: dict[str, object]) -> None:
        for identifier in strings(
            record.get("affected_controls", record.get("control_ids"))
        ):
            if identifier not in population:
                diagnostics.append(
                    f"{package.relative}/{filename}: unresolved control "
                    f"reference {identifier}"
                )

    for risk in risks:
        check_controls("risk-overlays.json", risk)
        risk_id = risk.get("risk_id")
        for overlay_id in strings(risk.get("overlay_ids")):
            overlay = overlay_map.get(overlay_id)
            if overlay is None:
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: unresolved "
                    f"overlay reference {overlay_id}"
                )
            elif isinstance(risk_id, str) and risk_id not in strings(
                overlay.get("risk_ids")
            ):
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: risk {risk_id} "
                    f"and overlay {overlay_id} must reference each other"
                )

    for overlay in overlays:
        check_controls("risk-overlays.json", overlay)
        overlay_id = overlay.get("overlay_id")
        for risk_id in strings(overlay.get("risk_ids")):
            risk = risk_map.get(risk_id)
            if risk is None:
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: unresolved risk "
                    f"reference {risk_id}"
                )
            elif isinstance(overlay_id, str) and overlay_id not in strings(
                risk.get("overlay_ids")
            ):
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: risk {risk_id} "
                    f"and overlay {overlay_id} must reference each other"
                )
        for expectation_id in strings(
            overlay.get("evidence_expectation_ids")
        ):
            expectation = evidence_map.get(expectation_id)
            if expectation is None:
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: unresolved "
                    "evidence expectation reference "
                    f"{expectation_id}"
                )
            elif isinstance(overlay_id, str) and overlay_id not in strings(
                expectation.get("overlay_ids")
            ):
                diagnostics.append(
                    f"{package.relative}/risk-overlays.json: overlay "
                    f"{overlay_id} and evidence expectation {expectation_id} "
                    "must reference each other"
                )

    for expectation in expectations:
        check_controls("evidence-expectations.json", expectation)
        expectation_id = expectation.get("expectation_id")
        for overlay_id in strings(expectation.get("overlay_ids")):
            overlay = overlay_map.get(overlay_id)
            if overlay is None:
                diagnostics.append(
                    f"{package.relative}/evidence-expectations.json: "
                    f"unresolved overlay reference {overlay_id}"
                )
            elif isinstance(
                expectation_id, str
            ) and expectation_id not in strings(
                overlay.get("evidence_expectation_ids")
            ):
                diagnostics.append(
                    f"{package.relative}/evidence-expectations.json: overlay "
                    f"{overlay_id} and evidence expectation {expectation_id} "
                    "must reference each other"
                )
    return sorted(set(diagnostics))


def walk_json(
    value: object, location: str = "document"
) -> list[tuple[str, str | None, object]]:
    """Flatten JSON values with deterministic dotted locations."""
    found: list[tuple[str, str | None, object]] = []
    if isinstance(value, dict):
        for key in sorted(value):
            child_location = f"{location}.{key}"
            child = value[key]
            found.append((child_location, key, child))
            found.extend(walk_json(child, child_location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_location = f"{location}[{index}]"
            found.append((child_location, None, child))
            found.extend(walk_json(child, child_location))
    return found


def proposition_bounds(
    text: str, index: int
) -> tuple[int, int, list[re.Match[str]]]:
    """Return the proposition containing ``index`` and preceding boundaries."""
    preceding = list(PROFILE_PROPOSITION_BOUNDARY.finditer(text, 0, index))
    start = preceding[-1].end() if preceding else 0
    following = PROFILE_PROPOSITION_BOUNDARY.search(text, index)
    end = following.start() if following else len(text)
    return start, end, preceding


def predicate_is_negated(prefix: str) -> bool:
    """Return whether a proposition prefix directly negates its predicate."""
    return bool(
        DIRECT_NEGATED_PROPOSITION.search(prefix)
        or PREDICATE_NEGATION.search(prefix)
    )


def coordinated_weakening_is_negated(
    text: str, preceding: list[re.Match[str]]
) -> bool:
    """Propagate a weakening denial only across an adjacent ``or``/``nor``."""
    if not preceding or preceding[-1].group(0).casefold() not in {"or", "nor"}:
        return False
    previous_end = preceding[-1].start()
    previous_start = preceding[-2].end() if len(preceding) > 1 else 0
    previous = text[previous_start:previous_end]
    weakening = WEAKENING_PREDICATE.search(previous)
    if weakening is None:
        return False
    return predicate_is_negated(previous[: weakening.start()])


def contains_affirmative_weakening(text: str) -> bool:
    """Recognize weakening predicates with assertion-aware polarity."""
    for weakening in WEAKENING_PREDICATE.finditer(text):
        start, end, preceding = proposition_bounds(text, weakening.start())
        proposition = text[start:end]
        relative_predicate = weakening.start() - start
        prefix = proposition[:relative_predicate]
        suffix = proposition[relative_predicate:]
        control = CONTROL_LANGUAGE.search(suffix)
        if control is None:
            continue
        word = weakening.group(0).casefold()
        after_control = suffix[control.end() :]
        if word.startswith("mak") and not re.search(
            r"\boptional\b", after_control, re.IGNORECASE
        ):
            continue
        if word.startswith("mark") and not re.search(
            r"\binapplicable\b", after_control, re.IGNORECASE
        ):
            continue
        between = suffix[weakening.end() - weakening.start() : control.start()]
        if (
            predicate_is_negated(prefix)
            or POST_PREDICATE_NEGATION.search(between)
            or coordinated_weakening_is_negated(text, preceding)
        ):
            continue
        if quoted_occurrence_is_metalinguistic(
            text, weakening.start(), weakening.start() + control.end()
        ):
            continue
        return True
    for weakening in PASSIVE_WEAKENING.finditer(text):
        predicate_start = weakening.start("predicate")
        start, _, _ = proposition_bounds(text, predicate_start)
        if predicate_is_negated(text[start:predicate_start]):
            continue
        if quoted_occurrence_is_metalinguistic(
            text, weakening.start(), weakening.end()
        ):
            continue
        return True
    return False


def asserted_profile_phrases(text: str) -> list[str]:
    """Reuse ESAF-1500 assertion context for profile-specific claim phrases."""
    assertions = list(asserted_prohibited_phrases(text))
    for label, pattern in PROFILE_ASSERTION_PATTERNS:
        for match in pattern.finditer(text):
            outcome_start = match.start("outcome")
            start, _, _ = proposition_bounds(text, outcome_start)
            if predicate_is_negated(text[start:outcome_start]):
                continue
            if quoted_occurrence_is_metalinguistic(
                text, match.start(), match.end()
            ):
                continue
            assertions.append(label)
    return assertions


def claim_diagnostics(package: ProfilePackage) -> list[str]:
    """Reject imported outcomes, local scales, weakening, and positive claims."""
    diagnostics: list[str] = []
    for component, document in sorted(package.documents.items()):
        filename = PACKAGE_FILES[component]
        relative = f"{package.relative}/{filename}"
        for location, key, value in walk_json(document):
            normalized = (
                key.casefold().replace("_", "-")
                if isinstance(key, str)
                else None
            )
            if (
                component == "external_references"
                and normalized in EXTERNAL_IMPORT_FIELDS
            ):
                diagnostics.append(
                    f"{relative}: {location}: prohibited "
                    f"external-reference field {key!r}"
                )
            if normalized in LOCAL_MATURITY_FIELDS:
                diagnostics.append(
                    f"{relative}: {location}: prohibited profile-local "
                    f"maturity field {key!r}"
                )
            if not isinstance(value, str):
                continue
            if contains_affirmative_weakening(value):
                diagnostics.append(
                    f"{relative}: {location}: prohibited control weakening "
                    "language"
                )
            for phrase in asserted_profile_phrases(value):
                diagnostics.append(
                    f"{relative}: {location}: prohibited assertion "
                    f"{phrase!r}"
                )

    readme_relative = f"{package.relative}/{PACKAGE_FILES['readme']}"
    try:
        readme = (package.directory / PACKAGE_FILES["readme"]).read_text(
            encoding="utf-8"
        )
    except UnicodeError:
        diagnostics.append(
            f"{readme_relative}: cannot decode UTF-8 content"
        )
        return sorted(set(diagnostics))
    if contains_affirmative_weakening(readme):
        diagnostics.append(
            f"{readme_relative}: prohibited control weakening language"
        )
    for phrase in asserted_profile_phrases(readme):
        diagnostics.append(
            f"{readme_relative}: prohibited assertion {phrase!r}"
        )
    return sorted(set(diagnostics))


def validate(root: Path = ROOT) -> list[str]:
    """Return all deterministic content diagnostics for discovered packages."""
    try:
        packages, diagnostics = inventory_profile_packages(root)
        for directory in packages:
            package = load_package(root, directory, diagnostics)
            if package is None:
                continue
            diagnostics.extend(semantic_diagnostics(root, package))
            diagnostics.extend(traceability_diagnostics(package))
            diagnostics.extend(claim_diagnostics(package))
        return sorted(set(diagnostics))
    except OperationalProfileError:
        raise
    except OSError as exc:
        raise OperationalProfileError(
            "profiles: repository content could not be read"
        ) from exc


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
    except OperationalProfileError as exc:
        print(f"Profile validation could not run: {exc}", file=sys.stderr)
        return 2
    except Exception:
        print(
            "Profile validation could not run: unexpected operational error",
            file=sys.stderr,
        )
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
