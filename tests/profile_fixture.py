"""Synthetic profile packages for validator tests."""

from __future__ import annotations

import json
import hashlib
import shutil
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
PROFILE_ID = "uk--jurisdiction-profile--0.1.0"
PROFILE_VERSION = "0.1.0"
PACKAGE_RELATIVE = Path("profiles/uk/0.1.0")
AUTHORITATIVE_COMPONENTS = (
    "profile.json",
    "control-selections.json",
    "risk-overlays.json",
    "evidence-expectations.json",
    "external-references.json",
)
MAPPING_REFERENCES = (
    (
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
        "crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md",
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
        "crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0.md",
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
        "crosswalks/registry/uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0.md",
    ),
)


def write_json(path: Path, document: object) -> None:
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def write_authoritative_source(package: Path) -> None:
    """Render the Markdown source blocks from the fixture's JSON records."""
    lines = [
        "# Synthetic Authoritative Profile Records",
        "",
        "> JSON files in this fixture are derived from these Markdown blocks.",
        "",
    ]
    for filename in AUTHORITATIVE_COMPONENTS:
        lines.extend(
            [
                f"## {filename}",
                "",
                "```json",
                (package / filename).read_text(encoding="utf-8").rstrip(),
                "```",
                "",
            ]
        )
    (package / "PROFILE.md").write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )


def profile_readme_content(text: str) -> str:
    return f"# Synthetic profile\n\n{text}\n"


def write_profile_readme(package: Path, text: str) -> str:
    content = profile_readme_content(text)
    (package / "README.md").write_text(content, encoding="utf-8")
    return content


def write_component(package: Path, filename: str, document: object) -> None:
    write_json(package / filename, document)
    write_authoritative_source(package)


def write_valid_profile_fixture(root: Path) -> Path:
    """Create a schema-conforming profile package without published content."""
    shutil.copytree(SOURCE_ROOT / "profiles/schema", root / "profiles/schema")
    shutil.copytree(SOURCE_ROOT / "controls", root / "controls")
    shutil.copytree(SOURCE_ROOT / "crosswalks/registry", root / "crosswalks/registry")
    shutil.copy2(SOURCE_ROOT / "crosswalks/catalog.json", root / "crosswalks/catalog.json")
    crosswalk_catalog = json.loads(
        (SOURCE_ROOT / "crosswalks/catalog.json").read_text(encoding="utf-8")
    )
    for record in crosswalk_catalog["mapping_sets"]:
        snapshot = root / record["path"]
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE_ROOT / record["path"], snapshot)

    package = root / PACKAGE_RELATIVE
    package.mkdir(parents=True)
    catalog = json.loads((root / "controls/catalog.json").read_text(encoding="utf-8"))
    catalog_digest = hashlib.sha256(
        (root / "controls/catalog.json").read_bytes()
    ).hexdigest()
    selections = [
        {
            "control_id": record["id"],
            "status": "not_selected",
            "rationale": "Synthetic validator fixture; the profile adds no selection",
        }
        for record in catalog["controls"]
    ]

    write_json(
        package / "profile.json",
        {
            "$schema": "../../schema/profile.schema.json",
            "schema_version": PROFILE_VERSION,
            "profile_id": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "status": "draft",
            "target_esaf_release": "v0.5-beta",
            "control_catalog": {
                "path": "controls/catalog.json",
                "schema_version": str(catalog["schema_version"]),
                "sha256": catalog_digest,
                "records": [
                    {
                        "id": record["id"],
                        "version": record["version"],
                        "status": record["status"],
                        "path": record["path"],
                        "record_sha256": hashlib.sha256(
                            (root / "controls" / record["path"]).read_bytes()
                        ).hexdigest(),
                    }
                    for record in catalog["controls"]
                ],
            },
            "title": "Synthetic validator profile",
            "scope": "Synthetic loader validation only.",
            "applicability_conditions": [
                {
                    "condition_id": "INACTIVE-FACT",
                    "question": "Is the synthetic condition active?",
                    "answer_type": "boolean",
                    "activates_when": False,
                    "resolution_evidence": "Synthetic fixture evidence.",
                }
            ],
            "source_boundary": {
                "statement": "Synthetic validator fixture source boundary.",
                "permitted_sources": ["ESAF"],
                "excluded_sources": [],
            },
            "components": {
                "source": "PROFILE.md",
                "readme": "README.md",
                "control_selections": "control-selections.json",
                "risk_overlays": "risk-overlays.json",
                "evidence_expectations": "evidence-expectations.json",
                "external_references": "external-references.json",
            },
            "change_history": [
                {
                    "version": PROFILE_VERSION,
                    "date": "2026-07-24",
                    "author": "ESAF",
                    "description": "Synthetic validator fixture.",
                }
            ],
        },
    )
    (package / "README.md").write_text(
        "# Synthetic validator profile\n", encoding="utf-8"
    )
    write_json(
        package / "control-selections.json",
        {
            "$schema": "../../schema/control-selections.schema.json",
            "schema_version": PROFILE_VERSION,
            "profile_id": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "selections": selections,
        },
    )
    write_json(
        package / "risk-overlays.json",
        {
            "$schema": "../../schema/risk-overlays.schema.json",
            "schema_version": PROFILE_VERSION,
            "profile_id": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "risks": [],
            "overlays": [],
        },
    )
    write_json(
        package / "evidence-expectations.json",
        {
            "$schema": "../../schema/evidence-expectations.schema.json",
            "schema_version": PROFILE_VERSION,
            "profile_id": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "expectations": [],
        },
    )
    write_json(
        package / "external-references.json",
        {
            "$schema": "../../schema/external-references.schema.json",
            "schema_version": PROFILE_VERSION,
            "profile_id": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "external_references": [
                {
                    "mapping_set_id": mapping_set_id,
                    "registry_path": registry_path,
                    "expected_status": "draft",
                    "reference_use": "lifecycle_reference_only",
                    "qualified_review_required": True,
                    "non_import_statement": "Relationships, external outcomes, and evidence are not imported.",
                }
                for mapping_set_id, registry_path in MAPPING_REFERENCES
            ],
        },
    )
    write_authoritative_source(package)
    return package


def rewrite_profile_version(package: Path, version: str) -> Path:
    """Rewrite every package identity and move it to the matching version path."""
    profile_path = package / "profile.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile_id = str(profile["profile_id"]).rsplit("--", 1)[0] + f"--{version}"
    profile["profile_id"] = profile_id
    profile["profile_version"] = version
    for change in profile["change_history"]:
        change["version"] = version
    write_json(profile_path, profile)

    for filename in (
        "control-selections.json",
        "risk-overlays.json",
        "evidence-expectations.json",
        "external-references.json",
    ):
        path = package / filename
        document = json.loads(path.read_text(encoding="utf-8"))
        document["profile_id"] = profile_id
        document["profile_version"] = version
        write_json(path, document)

    destination = package.parent / version
    package.rename(destination)
    write_authoritative_source(destination)
    return destination
