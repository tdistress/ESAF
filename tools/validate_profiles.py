#!/usr/bin/env python3
"""Fail-closed validation of versioned ESAF profile packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Sequence

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

if __package__:
    from .crosswalks.io import parse_front_matter
    from .validate_assessment import asserted_prohibited_phrases
else:
    from crosswalks.io import parse_front_matter
    from validate_assessment import asserted_prohibited_phrases


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
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
MAPPING_REFERENCES = {
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
    ("legal sufficiency", re.compile(r"\blegally sufficient\b", re.IGNORECASE)),
    (
        "external approval",
        re.compile(r"\b(?:has|have|had)\s+external approval\b", re.IGNORECASE),
    ),
    (
        "production readiness",
        re.compile(r"\bproduction[- ]ready\b", re.IGNORECASE),
    ),
    (
        "compliance",
        re.compile(r"\bcertif(?:y|ies|ied)\s+compliance\b", re.IGNORECASE),
    ),
)
WEAKENING_LANGUAGE = re.compile(
    r"\b(?:replace(?:s|d|ment)?|waiv(?:e|es|ed|er)|"
    r"weaken(?:s|ed|ing)?|narrow(?:s|ed|ing)?|inapplicable)\b",
    re.IGNORECASE,
)
CONTROL_LANGUAGE = re.compile(
    r"\b(?:core\s+)?controls?(?:\s+requirements?)?\b",
    re.IGNORECASE,
)
WEAKENING_NEGATION = re.compile(
    r"\b(?:cannot|does\s+not|must\s+not|never|not|shall\s+not)\b",
    re.IGNORECASE,
)


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
    packages: list[Path] = []
    for country in profiles.iterdir():
        if country.name == "schema" or not country.is_dir():
            continue
        for version in country.iterdir():
            if version.is_dir() and SEMVER.fullmatch(version.name):
                packages.append(version)
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


def safe_schema(root: Path, schema_name: str) -> Path | None:
    """Resolve a schema only when it is a real file under ``profiles/schema``."""
    schema_root = root / "profiles" / "schema"
    candidate = schema_root / schema_name
    if any(
        part.is_symlink()
        for part in (candidate, *candidate.parents)
        if part != root.parent
    ):
        return None
    try:
        root_resolved = root.resolve(strict=True)
        schema_root_resolved = schema_root.resolve(strict=True)
        schema_root_resolved.relative_to(root_resolved)
        candidate.resolve(strict=True).relative_to(schema_root_resolved)
    except (OSError, ValueError):
        return None
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
    actual_entries = {
        path.relative_to(directory).as_posix(): path for path in directory.rglob("*")
    }
    for filename in sorted(expected_files - actual_entries.keys()):
        diagnostics.append(f"{relative}: missing package file {filename}")
    for entry, path in sorted(actual_entries.items()):
        if entry in expected_files:
            continue
        kind = "entry" if path.is_dir() else "file"
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
    catalog = load_json(root / "controls" / "catalog.json")
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


def registry_metadata(path: Path) -> dict[str, object]:
    """Load lifecycle metadata and derive the mapping's current status."""
    metadata, _ = parse_front_matter(path)
    events = metadata.get("events")
    if not isinstance(events, list):
        raise ValueError("registry lifecycle events must be an array")
    if events:
        final = events[-1]
        if not isinstance(final, dict) or not isinstance(final.get("state"), str):
            raise ValueError("registry lifecycle event requires a string state")
        status = final["state"]
    else:
        status = "draft"
    return {**metadata, "status": status}


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
    for identifier in sorted(set(reference_ids) - MAPPING_REFERENCES.keys()):
        diagnostics.append(
            f"{package.relative}/external-references.json: "
            f"unexpected mapping reference {identifier}"
        )
    for identifier in sorted(MAPPING_REFERENCES.keys() - set(reference_ids)):
        diagnostics.append(
            f"{package.relative}/external-references.json: "
            f"missing mapping reference {identifier}"
        )
    if len(references) != len(MAPPING_REFERENCES):
        diagnostics.append(
            f"{package.relative}/external-references.json: expected exactly "
            f"{len(MAPPING_REFERENCES)} mapping references"
        )

    for reference in references:
        identifier = reference.get("mapping_set_id")
        if not isinstance(identifier, str) or identifier not in MAPPING_REFERENCES:
            continue
        expected_path = MAPPING_REFERENCES[identifier]
        observed_path = reference.get("registry_path")
        if observed_path != expected_path:
            diagnostics.append(
                f"{package.relative}/external-references.json: mapping "
                f"{identifier} registry path must be {expected_path!r}"
            )
            continue
        if reference.get("expected_status") != "draft":
            diagnostics.append(
                f"{package.relative}/external-references.json: mapping "
                f"{identifier} expected_status must be 'draft'"
            )
        if reference.get("non_import_statement") != NON_IMPORT_STATEMENT:
            diagnostics.append(
                f"{package.relative}/external-references.json: mapping "
                f"{identifier} non_import_statement must be "
                f"{NON_IMPORT_STATEMENT!r}"
            )
        path = root.joinpath(*PurePosixPath(expected_path).parts)
        try:
            metadata = registry_metadata(path)
        except (OSError, UnicodeError, ValueError) as exc:
            diagnostics.append(
                f"{expected_path}: cannot load registry metadata: {exc}"
            )
            continue
        if metadata.get("mapping_set_id") != identifier:
            diagnostics.append(
                f"{expected_path}: registry mapping_set_id does not match "
                f"{identifier}"
            )
        if metadata.get("status") != "draft":
            diagnostics.append(
                f"{expected_path}: registry lifecycle status is "
                f"{metadata.get('status')!r}; expected 'draft'"
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


def contains_affirmative_weakening(text: str) -> bool:
    """Recognize known control weakening language while allowing denials."""
    for clause in re.split(
        r"[.!?;\n]+|,\s*(?=(?:but|however|yet)\b)"
        r"|\b(?:but|however|yet)\b",
        text,
        flags=re.IGNORECASE,
    ):
        weakening = WEAKENING_LANGUAGE.search(clause)
        control = CONTROL_LANGUAGE.search(clause)
        if weakening is None or control is None:
            continue
        prefix = clause[: weakening.start()]
        if WEAKENING_NEGATION.search(prefix):
            continue
        return True
    return False


def asserted_profile_phrases(text: str) -> list[str]:
    """Reuse ESAF-1500 assertion context for profile-specific claim phrases."""
    assertions = list(asserted_prohibited_phrases(text))
    for label, pattern in PROFILE_ASSERTION_PATTERNS:
        for match in pattern.finditer(text):
            transformed = (
                text[: match.start()]
                + "establishes compliance"
                + text[match.end() :]
            )
            if list(asserted_prohibited_phrases(transformed)):
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
    readme = (package.directory / PACKAGE_FILES["readme"]).read_text(
        encoding="utf-8"
    )
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
    diagnostics: list[str] = []
    for directory in discover_profile_packages(root):
        package = load_package(root, directory, diagnostics)
        if package is None:
            continue
        diagnostics.extend(semantic_diagnostics(root, package))
        diagnostics.extend(traceability_diagnostics(package))
        diagnostics.extend(claim_diagnostics(package))
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
    except Exception as exc:
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
