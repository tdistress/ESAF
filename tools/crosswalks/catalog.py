"""Deterministic generated views of validated crosswalk records."""

from __future__ import annotations

import copy
import json
import re
from collections import Counter
from pathlib import Path, PurePosixPath

from tools.crosswalks.schemas import load_schemas, schema_errors
from tools.crosswalks.validation import ValidationResult


CATALOG_JSON = "crosswalks/catalog.json"
CATALOG_MARKDOWN = "crosswalks/CATALOG.md"
GENERATED_FROM = "crosswalks/mappings/** and crosswalks/registry/*.md"
COUNT_DIMENSIONS = (
    "by_snapshot_status",
    "by_lifecycle_state",
    "by_provision_status",
    "by_authority",
    "by_publication",
    "by_source_version",
    "by_esaf_release",
    "by_disposition",
    "by_relationship",
    "by_direction",
    "by_coverage",
    "by_confidence",
)
SCHEMA_ROOT = Path(__file__).parents[2]


def _repository_path(
    value: object,
    location: str,
    expected_prefix: tuple[str, ...],
    errors: list[str],
) -> PurePosixPath | None:
    """Validate one canonical POSIX repository-relative path."""
    if not isinstance(value, str) or not value:
        errors.append(f"{location}: path must be a nonempty string")
        return None
    path = PurePosixPath(value)
    if (
        "\\" in value
        or path.is_absolute()
        or any(part in {".", ".."} for part in path.parts)
        or path.as_posix() != value
    ):
        errors.append(f"{location}: path must be canonical POSIX repository-relative")
        return None
    if path.parts[: len(expected_prefix)] != expected_prefix:
        errors.append(
            f"{location}: path must be within {'/'.join(expected_prefix)}/"
        )
        return None
    return path


def _schema_model_errors(
    schema_name: str,
    value: object,
    location: str,
    validators: dict[str, object],
) -> list[str]:
    if not isinstance(value, dict):
        return [f"{location}: metadata must be a mapping"]
    return schema_errors(
        validators[schema_name], value, location  # type: ignore[arg-type]
    )


def _catalog_model_errors(result: ValidationResult) -> list[str]:
    """Validate the complete generator model before sorting or rendering it."""
    errors: list[str] = []
    validators = load_schemas(SCHEMA_ROOT)
    if not isinstance(result.mapping_sets, list):
        errors.append("mapping_sets: generator collection must be an array")
        mapping_sets: list[object] = []
    else:
        mapping_sets = result.mapping_sets
    if not isinstance(result.lifecycle_records, list):
        errors.append("lifecycle_records: generator collection must be an array")
        lifecycle_records: list[object] = []
    else:
        lifecycle_records = result.lifecycle_records

    lifecycle_by_id: dict[str, dict[str, object]] = {}
    for index, lifecycle_model in enumerate(lifecycle_records):
        location = f"lifecycle_records.{index}"
        if not isinstance(lifecycle_model, dict):
            errors.append(f"{location}: lifecycle model must be a mapping")
            continue
        path = _repository_path(
            lifecycle_model.get("path"),
            f"{location}.path",
            ("crosswalks", "registry"),
            errors,
        )
        if path is not None and (
            len(path.parts) != 3 or path.suffix != ".md" or path.name == ".gitkeep"
        ):
            errors.append(f"{location}.path: lifecycle path must name one registry Markdown record")
        metadata = lifecycle_model.get("metadata")
        errors.extend(
            _schema_model_errors(
                "lifecycle-record", metadata, f"{location}.metadata", validators
            )
        )
        if not isinstance(metadata, dict):
            continue
        mapping_set_id = metadata.get("mapping_set_id")
        if isinstance(mapping_set_id, str):
            if mapping_set_id in lifecycle_by_id:
                errors.append(
                    f"{location}.metadata.mapping_set_id: duplicate lifecycle model"
                )
            else:
                lifecycle_by_id[mapping_set_id] = metadata
            if path is not None and path.name != f"{mapping_set_id}.md":
                errors.append(
                    f"{location}.path: lifecycle filename must match mapping-set id"
                )

    seen_mapping_set_ids: set[str] = set()
    for index, model in enumerate(mapping_sets):
        location = f"mapping_sets.{index}"
        if not isinstance(model, dict):
            errors.append(f"{location}: mapping-set model must be a mapping")
            continue
        metadata = model.get("metadata")
        errors.extend(
            _schema_model_errors(
                "mapping-set", metadata, f"{location}.metadata", validators
            )
        )
        mapping_set_id = (
            metadata.get("mapping_set_id") if isinstance(metadata, dict) else None
        )
        if isinstance(mapping_set_id, str):
            if mapping_set_id in seen_mapping_set_ids:
                errors.append(f"{location}.metadata.mapping_set_id: duplicate mapping set")
            seen_mapping_set_ids.add(mapping_set_id)

        snapshot_path = _repository_path(
            model.get("path"),
            f"{location}.path",
            ("crosswalks", "mappings"),
            errors,
        )
        if snapshot_path is not None and (
            len(snapshot_path.parts) != 7 or snapshot_path.name != "README.md"
        ):
            errors.append(
                f"{location}.path: snapshot path must name a versioned mapping README.md"
            )
        if snapshot_path is not None and isinstance(metadata, dict):
            authority = metadata.get("authority")
            source_version = metadata.get("source_version")
            esaf_release = metadata.get("esaf_release")
            components = (
                authority.get("id") if isinstance(authority, dict) else None,
                source_version.get("id") if isinstance(source_version, dict) else None,
                esaf_release.get("id") if isinstance(esaf_release, dict) else None,
                metadata.get("mapping_set_version"),
            )
            if all(isinstance(item, str) for item in components):
                expected = PurePosixPath(
                    "crosswalks", "mappings", *components, "README.md"  # type: ignore[arg-type]
                )
                if snapshot_path != expected:
                    errors.append(
                        f"{location}.path: snapshot path must match mapping-set metadata"
                    )

        inventory_model = model.get("inventory")
        if not isinstance(inventory_model, dict):
            errors.append(f"{location}.inventory: inventory model must be a mapping")
        else:
            inventory_path = _repository_path(
                inventory_model.get("path"),
                f"{location}.inventory.path",
                ("crosswalks", "mappings"),
                errors,
            )
            if snapshot_path is not None and inventory_path != snapshot_path.with_name(
                "PROVISION_INVENTORY.md"
            ):
                errors.append(
                    f"{location}.inventory.path: inventory must belong to the mapping-set snapshot"
                )
            errors.extend(
                _schema_model_errors(
                    "provision-inventory",
                    inventory_model.get("metadata"),
                    f"{location}.inventory.metadata",
                    validators,
                )
            )

        lifecycle = model.get("lifecycle")
        errors.extend(
            _schema_model_errors(
                "lifecycle-record", lifecycle, f"{location}.lifecycle", validators
            )
        )
        if isinstance(mapping_set_id, str):
            registry_lifecycle = lifecycle_by_id.get(mapping_set_id)
            if registry_lifecycle is None:
                errors.append(
                    f"{location}.lifecycle: mapping set requires one registry lifecycle model"
                )
            elif lifecycle != registry_lifecycle:
                errors.append(
                    f"{location}.lifecycle: attached lifecycle must exactly match registry metadata"
                )

        provisions = model.get("provisions")
        if not isinstance(provisions, list):
            errors.append(f"{location}.provisions: provisions must be an array")
            continue
        for provision_index, provision in enumerate(provisions):
            provision_location = f"{location}.provisions.{provision_index}"
            if not isinstance(provision, dict):
                errors.append(
                    f"{provision_location}: provision model must be a mapping"
                )
                continue
            provision_metadata = provision.get("metadata")
            errors.extend(
                _schema_model_errors(
                    "mapping-record",
                    provision_metadata,
                    f"{provision_location}.metadata",
                    validators,
                )
            )
            provision_path = _repository_path(
                provision.get("path"),
                f"{provision_location}.path",
                ("crosswalks", "mappings"),
                errors,
            )
            if snapshot_path is not None and provision_path is not None:
                if provision_path.parent != snapshot_path.parent:
                    errors.append(
                        f"{provision_location}.path: provision must belong to the mapping-set snapshot"
                    )
                record_id = (
                    provision_metadata.get("record_id")
                    if isinstance(provision_metadata, dict)
                    else None
                )
                if isinstance(record_id, str) and provision_path.name != f"{record_id}.md":
                    errors.append(
                        f"{provision_location}.path: provision filename must match record id"
                    )

    orphan_ids = sorted(set(lifecycle_by_id) - seen_mapping_set_ids)
    for mapping_set_id in orphan_ids:
        errors.append(
            f"lifecycle_records: lifecycle model has no mapping set {mapping_set_id}"
        )
    return sorted(set(errors))


def _numeric_key(value: object) -> tuple[tuple[int, object], ...]:
    """Order identifiers by case-folded text and embedded integer components."""
    return tuple(
        (0, int(part)) if part.isdigit() else (1, part.casefold())
        for part in re.split(r"(\d+)", str(value))
        if part
    )


def _semver_key(value: object) -> tuple[int, int, int]:
    parts = str(value).split(".")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def _nested_id(metadata: dict[str, object], field: str) -> str:
    value = metadata.get(field)
    nested = value.get("id") if isinstance(value, dict) else None
    return nested if isinstance(nested, str) else ""


def _mapping_set_key(model: dict[str, object]) -> tuple[object, ...]:
    metadata = model.get("metadata")
    if not isinstance(metadata, dict):
        return ((), (), (), (), (0, 0, 0))
    return (
        _numeric_key(_nested_id(metadata, "authority")),
        _numeric_key(_nested_id(metadata, "publication")),
        _numeric_key(_nested_id(metadata, "source_version")),
        _numeric_key(_nested_id(metadata, "esaf_release")),
        _semver_key(metadata.get("mapping_set_version", "0.0.0")),
    )


def _provision_key(model: dict[str, object]) -> tuple[object, ...]:
    metadata = model.get("metadata")
    if not isinstance(metadata, dict):
        return ((), ())
    return (
        _numeric_key(metadata.get("external_provision_id", "")),
        _numeric_key(metadata.get("record_id", "")),
    )


def _relationship_key(leg: object) -> tuple[object, ...]:
    if not isinstance(leg, dict):
        return ((), ())
    return (
        _numeric_key(leg.get("esaf_control_id", "")),
        _numeric_key(leg.get("direction", "")),
    )


def _increment(counter: Counter[str], value: object) -> None:
    if isinstance(value, str):
        counter[value] += 1


def _sorted_counts(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def build_catalog(result: ValidationResult) -> dict[str, object]:
    """Build the complete catalog view from a successful validation result."""
    if result.errors:
        raise ValueError("cannot build a catalog from invalid authoritative records")
    model_errors = _catalog_model_errors(result)
    if model_errors:
        raise ValueError(
            "invalid catalog model:\n" + "\n".join(f"- {error}" for error in model_errors)
        )

    dimensions = {name: Counter() for name in COUNT_DIMENSIONS}
    mapping_set_views: list[dict[str, object]] = []
    provision_count = relationship_count = negative_count = 0

    for source_model in sorted(result.mapping_sets, key=_mapping_set_key):
        metadata = copy.deepcopy(source_model.get("metadata", {}))
        inventory_model = source_model.get("inventory", {})
        inventory = copy.deepcopy(
            inventory_model.get("metadata", {})
            if isinstance(inventory_model, dict)
            else {}
        )
        lifecycle = copy.deepcopy(source_model.get("lifecycle"))
        provisions: list[dict[str, object]] = []

        if isinstance(metadata, dict):
            _increment(dimensions["by_snapshot_status"], metadata.get("status"))
            _increment(dimensions["by_authority"], _nested_id(metadata, "authority"))
            _increment(dimensions["by_publication"], _nested_id(metadata, "publication"))
            _increment(dimensions["by_source_version"], _nested_id(metadata, "source_version"))
            _increment(dimensions["by_esaf_release"], _nested_id(metadata, "esaf_release"))
        if isinstance(lifecycle, dict):
            events = lifecycle.get("events")
            if isinstance(events, list) and events and isinstance(events[-1], dict):
                _increment(dimensions["by_lifecycle_state"], events[-1].get("state"))

        source_provisions = source_model.get("provisions", [])
        if not isinstance(source_provisions, list):
            source_provisions = []
        for source_provision in sorted(source_provisions, key=_provision_key):
            if not isinstance(source_provision, dict):
                continue
            provision_metadata = copy.deepcopy(source_provision.get("metadata", {}))
            if not isinstance(provision_metadata, dict):
                continue
            relationships = provision_metadata.get("relationships", [])
            if isinstance(relationships, list):
                relationships.sort(key=_relationship_key)
            else:
                relationships = []
                provision_metadata["relationships"] = relationships
            provision_count += 1
            relationship_count += len(relationships)
            disposition = provision_metadata.get("disposition")
            if disposition in {"no_direct_mapping", "out_of_scope"}:
                negative_count += 1
            _increment(dimensions["by_provision_status"], provision_metadata.get("status"))
            _increment(dimensions["by_disposition"], disposition)
            for leg in relationships:
                if not isinstance(leg, dict):
                    continue
                _increment(dimensions["by_relationship"], leg.get("relationship"))
                _increment(dimensions["by_direction"], leg.get("direction"))
                _increment(dimensions["by_coverage"], leg.get("coverage"))
                _increment(dimensions["by_confidence"], leg.get("confidence"))
            provisions.append(
                {
                    "path": source_provision.get("path", ""),
                    "metadata": provision_metadata,
                }
            )

        mapping_set_views.append(
            {
                "path": source_model.get("path", ""),
                "metadata": metadata,
                "inventory": inventory,
                "lifecycle": lifecycle,
                "provisions": provisions,
            }
        )

    counts: dict[str, object] = {
        "mapping_sets": len(mapping_set_views),
        "provisions": provision_count,
        "relationships": relationship_count,
        "negative_dispositions": negative_count,
    }
    counts.update(
        {name: _sorted_counts(dimensions[name]) for name in COUNT_DIMENSIONS}
    )
    return {
        "schema_version": "1.0.0",
        "generated_from": GENERATED_FROM,
        "counts": counts,
        "mapping_sets": mapping_set_views,
    }


def render_json(catalog: dict[str, object]) -> str:
    """Render stable UTF-8 JSON text."""
    return json.dumps(catalog, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def _markdown_path(repository_path: object) -> str:
    path = str(repository_path)
    return path.removeprefix("crosswalks/")


def _mapping_set_row(item: dict[str, object]) -> str:
    metadata = item["metadata"]
    assert isinstance(metadata, dict)
    mapping_set_id = str(metadata.get("mapping_set_id", ""))
    source_version = _nested_id(metadata, "source_version")
    esaf_release = _nested_id(metadata, "esaf_release")
    status = str(metadata.get("status", ""))
    lifecycle = item.get("lifecycle")
    events = lifecycle.get("events", []) if isinstance(lifecycle, dict) else []
    state = (
        str(events[-1].get("state", ""))
        if isinstance(events, list) and events and isinstance(events[-1], dict)
        else ""
    )
    return (
        f"| [{mapping_set_id}]({_markdown_path(item['path'])}) | "
        f"{source_version} | {esaf_release} | {status} | {state} |"
    )


def _mapping_set_table(items: list[dict[str, object]]) -> list[str]:
    lines = [
        "| Mapping set | Source version | ESAF release | Editorial status | Lifecycle state |",
        "|---|---|---|---|---|",
    ]
    if items:
        lines.extend(_mapping_set_row(item) for item in items)
    else:
        lines.append("| None | Not applicable | Not applicable | Not applicable | Not applicable |")
    return lines + [""]


def render_markdown(catalog: dict[str, object]) -> str:
    """Render the fixed-order human-readable catalog."""
    counts = catalog["counts"]
    mapping_sets = catalog["mapping_sets"]
    assert isinstance(counts, dict) and isinstance(mapping_sets, list)
    lines = [
        "# ESAF Standards Crosswalk Catalog",
        "",
        "> Generated by `tools/validate_crosswalks.py`. Do not edit directly.",
        "",
    ]
    if counts["mapping_sets"] == 0:
        lines.extend(
            [
                "No mapping sets have been assessed or approved. This empty catalog makes no claim about any external standard.",
                "",
            ]
        )

    active: list[dict[str, object]] = []
    work: list[dict[str, object]] = []
    history: list[dict[str, object]] = []
    for item in mapping_sets:
        if not isinstance(item, dict):
            continue
        metadata = item.get("metadata")
        lifecycle = item.get("lifecycle")
        events = lifecycle.get("events", []) if isinstance(lifecycle, dict) else []
        state = (
            events[-1].get("state")
            if isinstance(events, list) and events and isinstance(events[-1], dict)
            else None
        )
        if state == "published":
            active.append(item)
        elif state in {"deprecated", "retired"}:
            history.append(item)
        elif isinstance(metadata, dict):
            work.append(item)

    lines.extend(["## Active published mapping sets", ""])
    lines.extend(_mapping_set_table(active))
    lines.extend(["## Reviewed and draft work", ""])
    lines.extend(_mapping_set_table(work))
    lines.extend(["## Deprecated and retired history", ""])
    lines.extend(_mapping_set_table(history))
    lines.extend(["## Coverage and gaps", ""])
    lines.extend(
        [
            f"Mapping sets: {counts['mapping_sets']}; provisions: {counts['provisions']}; directional relationships: {counts['relationships']}; negative dispositions: {counts['negative_dispositions']}.",
            "",
            "| Provision record | Disposition | Relationships |",
            "|---|---|---:|",
        ]
    )
    provision_rows = 0
    for item in mapping_sets:
        if not isinstance(item, dict):
            continue
        provisions = item.get("provisions", [])
        if not isinstance(provisions, list):
            continue
        for provision in provisions:
            if not isinstance(provision, dict):
                continue
            metadata = provision.get("metadata")
            if not isinstance(metadata, dict):
                continue
            relationships = metadata.get("relationships", [])
            relationship_total = len(relationships) if isinstance(relationships, list) else 0
            record_id = str(metadata.get("record_id", ""))
            lines.append(
                f"| [{record_id}]({_markdown_path(provision.get('path', ''))}) | "
                f"{metadata.get('disposition', '')} | {relationship_total} |"
            )
            provision_rows += 1
    if not provision_rows:
        lines.append("| None assessed | Not applicable | 0 |")
    return "\n".join(lines).rstrip() + "\n"


def check_outputs(root: Path, catalog: dict[str, object]) -> list[str]:
    """Compare generated files with their exact expected UTF-8 bytes."""
    expected = {
        CATALOG_JSON: render_json(catalog).encode("utf-8"),
        CATALOG_MARKDOWN: render_markdown(catalog).encode("utf-8"),
    }
    errors = []
    for relative, expected_bytes in expected.items():
        path = root / relative
        try:
            actual = path.read_bytes()
        except OSError:
            actual = None
        if actual != expected_bytes:
            errors.append(
                f"{relative}: freshness: generated output is missing or stale; "
                "required: run python tools/validate_crosswalks.py --write"
            )
    return sorted(errors)
