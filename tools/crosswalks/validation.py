"""Repository-aware semantic validation for crosswalk snapshots."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.manifest import build_control_manifest, render_manifest
from tools.crosswalks.schemas import load_schemas, schema_errors


@dataclass
class ValidationResult:
    errors: list[str]
    mapping_sets: list[dict[str, object]]
    lifecycle_records: list[dict[str, object]]


def snapshot_directories(root: Path) -> list[Path]:
    """Return snapshot directories in deterministic repository order."""
    base = root / "crosswalks" / "mappings"
    return sorted(path.parent for path in base.rglob("README.md")) if base.exists() else []


def validate(root: Path, baseline_ref: str | None = None) -> ValidationResult:
    """Validate all crosswalk mapping snapshots below ``root``."""
    del baseline_ref  # Lifecycle comparison is added by a later implementation task.
    errors: list[str] = []
    mapping_sets: list[dict[str, object]] = []
    seen_mapping_set_ids: set[str] = set()
    schema_root = root if (root / "crosswalks" / "schema").exists() else Path(__file__).parents[2]
    validators = load_schemas(schema_root)

    for snapshot in snapshot_directories(root):
        relative = snapshot.relative_to(root).as_posix()
        try:
            metadata, _ = parse_front_matter(snapshot / "README.md")
        except yaml.YAMLError as error:
            errors.append(f"{relative}/README.md: invalid YAML: {error}")
            continue
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{relative}/README.md: {error}")
            continue
        snapshot_errors, model = _validate_snapshot(
            root, snapshot, metadata, seen_mapping_set_ids, validators
        )
        errors.extend(snapshot_errors)
        mapping_sets.append(model)
    return ValidationResult(sorted(set(errors)), mapping_sets, [])


def load_snapshot_model(
    root: Path, snapshot: Path, metadata: dict[str, object]
) -> dict[str, object]:
    """Load a valid snapshot into the stable model consumed by generators."""
    inventory, _ = parse_front_matter(snapshot / "PROVISION_INVENTORY.md")
    manifest = json.loads(
        (snapshot / "ESAF_CONTROL_MANIFEST.json").read_text(encoding="utf-8")
    )
    provisions: list[dict[str, object]] = []
    for path in sorted(snapshot.glob("*.md")):
        if path.name in {"README.md", "PROVISION_INVENTORY.md"} or path.is_symlink():
            continue
        record, body = parse_front_matter(path)
        provisions.append(
            {
                "path": path.relative_to(root).as_posix(),
                "metadata": record,
                "body": body,
            }
        )
    return _snapshot_model(root, snapshot, metadata, inventory, manifest, provisions)


def _validate_snapshot(
    root: Path,
    snapshot: Path,
    mapping_set: dict[str, object],
    seen_mapping_set_ids: set[str],
    validators: dict[str, object],
) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    relative = snapshot.relative_to(root).as_posix()
    errors.extend(schema_errors(validators["mapping-set"], mapping_set, f"{relative}/README.md"))  # type: ignore[arg-type]
    errors.extend(_validate_mapping_set(mapping_set, relative))
    errors.extend(
        _validate_reviewed_text(
            snapshot / "README.md", mapping_set.get("status"), f"{relative}/README.md"
        )
    )

    mapping_set_id = mapping_set.get("mapping_set_id")
    if isinstance(mapping_set_id, str):
        if mapping_set_id in seen_mapping_set_ids:
            errors.append(f"{relative}: duplicate mapping-set id {mapping_set_id}")
        seen_mapping_set_ids.add(mapping_set_id)

    expected_id = _mapping_set_id(mapping_set)
    if expected_id and mapping_set_id != expected_id:
        errors.append(f"{relative}: mapping-set id disagrees with metadata")
    expected_path = _snapshot_path(mapping_set)
    if expected_path and relative != expected_path:
        errors.append(f"{relative}: snapshot path disagrees with metadata")

    allowed_names = {"README.md", "PROVISION_INVENTORY.md", "ESAF_CONTROL_MANIFEST.json"}
    record_paths: list[Path] = []
    try:
        entries = sorted(snapshot.iterdir(), key=lambda path: path.name)
    except OSError as error:
        return [f"{relative}: cannot inspect snapshot: {error}"], {"metadata": mapping_set}
    for entry in entries:
        if entry.is_symlink() or not entry.is_file():
            errors.append(f"{relative}/{entry.name}: unexpected snapshot entry")
        elif entry.name in allowed_names:
            continue
        elif entry.suffix == ".md":
            record_paths.append(entry)
        else:
            errors.append(f"{relative}/{entry.name}: unexpected snapshot entry")

    inventory_document = _read_front_matter(
        snapshot / "PROVISION_INVENTORY.md", relative, "provision inventory", errors
    )
    inventory, inventory_body = (
        inventory_document if inventory_document is not None else (None, "")
    )
    manifest = _read_json(snapshot / "ESAF_CONTROL_MANIFEST.json", relative, errors)
    if inventory is not None:
        errors.extend(
            schema_errors(
                validators["provision-inventory"],  # type: ignore[arg-type]
                inventory,
                f"{relative}/PROVISION_INVENTORY.md",
            )
        )
        errors.extend(
            _validate_reviewed_text(
                snapshot / "PROVISION_INVENTORY.md",
                mapping_set.get("status"),
                f"{relative}/PROVISION_INVENTORY.md",
                inventory_body,
            )
        )
    if manifest is not None:
        errors.extend(
            schema_errors(
                validators["esaf-control-manifest"],  # type: ignore[arg-type]
                manifest,
                f"{relative}/ESAF_CONTROL_MANIFEST.json",
            )
        )
    records: list[dict[str, object]] = []
    provisions: list[dict[str, object]] = []
    seen_record_ids: set[str] = set()
    seen_external_ids: set[str] = set()
    inventory_values = inventory.get("provision_ids", []) if inventory else []
    inventory_ids = (
        {item for item in inventory_values if isinstance(item, str)}
        if isinstance(inventory_values, list)
        else set()
    )
    for path in record_paths:
        record_document = _read_front_matter(path, relative, "provision record", errors)
        if record_document is None:
            continue
        record, body = record_document
        records.append(record)
        record_relative = path.relative_to(root).as_posix()
        provisions.append({"path": record_relative, "metadata": record, "body": body})
        errors.extend(
            schema_errors(validators["mapping-record"], record, record_relative)  # type: ignore[arg-type]
        )
        record_id = record.get("record_id")
        external_id = record.get("external_provision_id")
        if isinstance(record_id, str):
            if record_id in seen_record_ids:
                errors.append(f"{record_relative}: duplicate record id {record_id}")
            seen_record_ids.add(record_id)
            if path.name != f"{record_id}.md":
                errors.append(f"{record_relative}: record filename disagrees with record id")
        if isinstance(external_id, str):
            if external_id in seen_external_ids:
                errors.append(
                    f"{record_relative}: duplicate external provision identifier {external_id}"
                )
            seen_external_ids.add(external_id)
            if external_id not in inventory_ids:
                errors.append(
                    f"{record_relative}: provision {external_id} not present in provision inventory"
                )
        if record.get("mapping_set_id") != mapping_set_id:
            errors.append(f"{record_relative}: record mapping-set id disagrees with snapshot")
        errors.extend(_validate_status(record, mapping_set, record_relative))
        errors.extend(
            f"{record_relative}: {message}"
            for message in validate_record(record, mapping_set)
        )
        errors.extend(_validate_reviewed_text(path, record.get("status"), record_relative))

    if manifest is not None:
        errors.extend(
            _validate_control_manifest(root, snapshot, mapping_set, manifest, records)
        )

    if inventory is not None:
        errors.extend(_validate_inventory(relative, mapping_set, inventory, seen_external_ids))
    if mapping_set.get("status") == "approved" and not records:
        errors.append(f"{relative}: approved snapshot requires at least one provision")

    model = _snapshot_model(
        root, snapshot, mapping_set, inventory or {}, manifest or {}, provisions
    )
    return errors, model


def _validate_control_manifest(
    root: Path,
    snapshot: Path,
    mapping_set: dict[str, object],
    manifest: dict[str, object],
    records: list[dict[str, object]] | None,
) -> list[str]:
    """Validate manifest provenance and provision control references."""
    errors: list[str] = []
    relative = snapshot.relative_to(root).as_posix()
    release = mapping_set.get("esaf_release")
    if not isinstance(release, dict):
        return errors
    commit = release.get("source_commit_sha")
    release_id = release.get("id")
    tag_alias = release.get("tag_alias")
    if not isinstance(commit, str) or not isinstance(release_id, str):
        return errors
    if tag_alias is not None and not isinstance(tag_alias, str):
        return errors

    if manifest.get("source_commit_sha") != commit:
        errors.append(f"{relative}: manifest source commit disagrees with snapshot")
    if manifest.get("esaf_release") != release_id:
        errors.append(f"{relative}: manifest ESAF release disagrees with snapshot")
    if manifest.get("tag_alias") != tag_alias:
        errors.append(f"{relative}: manifest tag alias disagrees with snapshot")
    if manifest.get("control_catalog_sha256") != release.get("control_catalog_sha256"):
        errors.append(f"{relative}: control catalog digest mismatch")

    try:
        regenerated = build_control_manifest(root, commit, release_id, tag_alias)
    except ValueError as error:
        errors.append(f"{relative}: {error}")
        return errors

    expected_catalog_digest = regenerated.get("control_catalog_sha256")
    if release.get("control_catalog_sha256") != expected_catalog_digest:
        errors.append(f"{relative}: control catalog digest mismatch")

    expected_controls = {
        item.get("id"): item
        for item in regenerated.get("controls", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    manifest_controls = manifest.get("controls", [])
    if not isinstance(manifest_controls, list):
        manifest_controls = []
    actual_controls = {
        item.get("id"): item
        for item in manifest_controls
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for control_id in sorted(expected_controls.keys() & actual_controls.keys()):
        if actual_controls[control_id].get("record_sha256") != expected_controls[
            control_id
        ].get("record_sha256"):
            errors.append(f"{relative}: control record digest mismatch for {control_id}")

    manifest_path = snapshot / "ESAF_CONTROL_MANIFEST.json"
    try:
        committed_bytes = manifest_path.read_bytes()
    except OSError:
        committed_bytes = b""
    expected_bytes = render_manifest(regenerated).encode("utf-8")
    if committed_bytes != expected_bytes:
        errors.append(f"{relative}: manifest differs from regeneration at pinned commit")

    if records is None:
        return errors
    for record in records:
        relationships = record.get("relationships", [])
        if not isinstance(relationships, list):
            continue
        for relationship in relationships:
            if not isinstance(relationship, dict):
                continue
            control_id = relationship.get("esaf_control_id")
            control_version = relationship.get("esaf_control_version")
            control = expected_controls.get(control_id)
            if control is None:
                errors.append(
                    f"{relative}: unresolved ESAF control identifier {control_id}"
                )
            elif control.get("version") != control_version:
                errors.append(
                    f"{relative}: ESAF control version mismatch for {control_id}"
                )
    return errors


def _snapshot_model(
    root: Path,
    snapshot: Path,
    mapping_set: dict[str, object],
    inventory: dict[str, object],
    manifest: dict[str, object],
    provisions: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "path": (snapshot / "README.md").relative_to(root).as_posix(),
        "metadata": mapping_set,
        "inventory": {
            "path": (snapshot / "PROVISION_INVENTORY.md").relative_to(root).as_posix(),
            "metadata": inventory,
        },
        "control_manifest": {
            "path": (snapshot / "ESAF_CONTROL_MANIFEST.json").relative_to(root).as_posix(),
            "metadata": manifest,
        },
        "provisions": provisions,
    }


def _validate_inventory(
    relative: str,
    mapping_set: dict[str, object],
    inventory: dict[str, object],
    record_external_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    scope = mapping_set.get("scope", {})
    if not isinstance(scope, dict):
        return errors
    if inventory.get("mapping_set_id") != mapping_set.get("mapping_set_id"):
        errors.append(f"{relative}: inventory mapping-set id disagrees with snapshot")
    if scope.get("type") != inventory.get("scope_type"):
        errors.append(f"{relative}: mapping-set scope type disagrees with provision inventory")
    if scope.get("statement") != inventory.get("scope_statement"):
        errors.append(f"{relative}: mapping-set scope statement disagrees with provision inventory")
    if scope.get("inventory_count") != inventory.get("expected_count"):
        errors.append(f"{relative}: mapping-set inventory count disagrees with provision inventory")
    provision_ids = inventory.get("provision_ids", [])
    if not isinstance(provision_ids, list):
        provision_ids = []
    if isinstance(provision_ids, list) and inventory.get("expected_count") != len(provision_ids):
        errors.append(f"{relative}: inventory expected count disagrees with provision identifiers")
    inventory_ids = {item for item in provision_ids if isinstance(item, str)}
    status = mapping_set.get("status")
    if isinstance(status, str) and status in {"reviewed", "approved"}:
        for missing in sorted(inventory_ids - record_external_ids):
            errors.append(f"{relative}: missing provision record for inventory identifier {missing}")
    return errors


def _validate_status(
    record: dict[str, object], mapping_set: dict[str, object], relative: str
) -> list[str]:
    allowed = {
        "draft": {"draft", "reviewed"},
        "reviewed": {"reviewed"},
        "approved": {"reviewed"},
    }
    snapshot_status = mapping_set.get("status")
    accepted = allowed.get(snapshot_status, set()) if isinstance(snapshot_status, str) else set()
    record_status = record.get("status")
    if not isinstance(record_status, str) or record_status not in accepted:
        return [f"{relative}: invalid snapshot/provision status combination"]
    return []


def _validate_mapping_set(mapping_set: dict[str, object], relative: str) -> list[str]:
    errors: list[str] = []
    components: list[object] = []
    for parent, child in (
        ("authority", "id"),
        ("publication", "id"),
        ("source_version", "id"),
        ("esaf_release", "id"),
    ):
        value = mapping_set.get(parent)
        components.append(value.get(child) if isinstance(value, dict) else None)
    components.append(mapping_set.get("mapping_set_version"))
    if any(isinstance(value, str) and "--" in value for value in components):
        errors.append(f"{relative}: mapping-set id component contains double hyphens")

    mapper = mapping_set.get("mapper")
    reviewer = mapping_set.get("reviewer")
    rights = mapping_set.get("publication_rights")
    mapper_id = mapper.get("id") if isinstance(mapper, dict) else None
    mapping_status = mapping_set.get("status")
    if isinstance(mapping_status, str) and mapping_status in {"reviewed", "approved"}:
        if not _complete_reviewer(reviewer):
            errors.append(f"{relative}: reviewed content requires review metadata")
        elif reviewer.get("id") == mapper_id:  # type: ignore[union-attr]
            errors.append(f"{relative}: reviewer must differ from mapper")
    if not isinstance(rights, dict) or rights.get("approved") is not True:
        errors.append(f"{relative}: publication-rights approval is required")
    elif rights.get("reviewer_id") == mapper_id:
        errors.append(f"{relative}: publication-rights reviewer must differ from mapper")

    if mapping_set.get("status") == "approved":
        findings = mapping_set.get("findings", [])
        if isinstance(findings, list):
            for finding in findings:
                if not isinstance(finding, dict):
                    continue
                severity = finding.get("severity")
                status = finding.get("status")
                if status == "open":
                    errors.append(f"{relative}: open review finding blocks approval")
                if (
                    isinstance(severity, str)
                    and severity in {"Critical", "Important"}
                    and status != "resolved"
                ):
                    errors.append(f"{relative}: {severity} findings must be resolved")
                if severity == "Minor" and status not in {"resolved", "accepted"}:
                    errors.append(
                        f"{relative}: Minor findings must be resolved or formally accepted"
                    )
    return errors


def validate_record(
    record: dict[str, object], mapping_set: dict[str, object]
) -> list[str]:
    """Return semantic diagnostics for one provision record."""
    errors: list[str] = []
    relationships = record.get("relationships", [])
    if not isinstance(relationships, list):
        relationships = []
    disposition = record.get("disposition")
    if disposition == "mapped" and not relationships:
        errors.append("mapped record requires at least one relationship")
    if disposition != "mapped" and relationships:
        errors.append(f"{disposition} record must not contain relationships")
    if disposition != "mapped" and not record.get("negative_rationale"):
        errors.append("negative disposition requires negative_rationale")
    if record.get("granularity") != "requirement" and not record.get("granularity_exception"):
        errors.append("non-requirement granularity requires granularity_exception")

    seen_legs: set[tuple[object, object]] = set()
    for leg in relationships:
        if not isinstance(leg, dict):
            continue
        key = (leg.get("esaf_control_id"), leg.get("direction"))
        if not all(isinstance(value, str) for value in key):
            continue
        if key in seen_legs:
            errors.append(f"duplicate relationship leg {key[0]}/{key[1]}")
        seen_legs.add(key)

    mapper = record.get("mapper")
    reviewer = record.get("reviewer")
    if record.get("status") == "reviewed":
        if not _complete_reviewer(reviewer):
            errors.append("reviewed content requires review metadata")
        elif isinstance(mapper, dict) and reviewer.get("id") == mapper.get("id"):  # type: ignore[union-attr]
            errors.append("reviewer must differ from mapper")

    context = record.get("context")
    rights = mapping_set.get("publication_rights")
    if isinstance(context, dict) and isinstance(rights, dict):
        permitted = rights.get("permitted_elements", [])
        mode = context.get("mode")
        required_element = "paraphrases" if mode == "paraphrase" else "identifiers"
        if not isinstance(permitted, list) or required_element not in permitted:
            errors.append("context exceeds permitted publication elements")
    return errors


def _complete_reviewer(value: object) -> bool:
    required = {
        "id",
        "qualification",
        "date",
        "authorized_source_access",
        "findings_disposition",
    }
    return (
        isinstance(value, dict)
        and required.issubset(value)
        and bool(value.get("id"))
        and bool(value.get("qualification"))
        and bool(value.get("date"))
        and value.get("authorized_source_access") is True
        and bool(value.get("findings_disposition"))
    )


_MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
_DRAFTING_MARKER = re.compile(r"(?im)(?:^|\b)(?:TODO|TBD|FIXME|PLACEHOLDER)(?:\b|$)")
_CORRUPTION_SIGNATURES = ("Ã", "Â", "â€", "â€™", "ï»¿", "�")


def _validate_reviewed_text(
    path: Path, status: object, relative: str, text: str | None = None
) -> list[str]:
    if not isinstance(status, str) or status not in {"reviewed", "approved"}:
        return []
    if text is None:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return []
    errors: list[str] = []
    if any(signature in text for signature in _CORRUPTION_SIGNATURES):
        errors.append(f"{relative}: possible text-encoding corruption")
    if _DRAFTING_MARKER.search(text):
        errors.append(f"{relative}: unresolved drafting marker")
    for match in _MARKDOWN_LINK.finditer(text):
        raw_target = match.group(1).strip()
        if raw_target.startswith("<") and ">" in raw_target:
            raw_target = raw_target[1 : raw_target.index(">")]
        else:
            raw_target = raw_target.split(maxsplit=1)[0]
        try:
            parsed = urlsplit(raw_target)
        except ValueError:
            errors.append(f"{relative}: broken local link {raw_target}")
            continue
        if parsed.scheme or parsed.netloc or raw_target.startswith("#"):
            continue
        target = unquote(parsed.path)
        if target and not (path.parent / target).resolve().exists():
            errors.append(f"{relative}: broken local link {raw_target}")
    return errors


def _mapping_set_id(mapping_set: dict[str, object]) -> str | None:
    try:
        authority = mapping_set["authority"]
        publication = mapping_set["publication"]
        source_version = mapping_set["source_version"]
        esaf_release = mapping_set["esaf_release"]
        components = (
            authority["id"],  # type: ignore[index]
            publication["id"],  # type: ignore[index]
            source_version["id"],  # type: ignore[index]
            esaf_release["id"],  # type: ignore[index]
            mapping_set["mapping_set_version"],
        )
        if not all(isinstance(component, str) for component in components):
            return None
        return f"{components[0]}--{components[1]}--{components[2]}--esaf-{components[3]}--{components[4]}"
    except (KeyError, TypeError):
        return None


def _snapshot_path(mapping_set: dict[str, object]) -> str | None:
    try:
        return (
            "crosswalks/mappings/"
            f"{mapping_set['authority']['id']}/"  # type: ignore[index]
            f"{mapping_set['source_version']['id']}/"  # type: ignore[index]
            f"{mapping_set['esaf_release']['id']}/"  # type: ignore[index]
            f"{mapping_set['mapping_set_version']}"
        )
    except (KeyError, TypeError):
        return None


def _read_front_matter(
    path: Path, relative: str, label: str, errors: list[str]
) -> tuple[dict[str, object], str] | None:
    if not path.is_file():
        errors.append(f"{relative}: missing {label} {path.name}")
        return None
    try:
        return parse_front_matter(path)
    except yaml.YAMLError as error:
        errors.append(f"{relative}/{path.name}: invalid YAML: {error}")
        return None
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"{relative}/{path.name}: {error}")
        return None


def _read_json(path: Path, relative: str, errors: list[str]) -> dict[str, object] | None:
    if not path.is_file():
        errors.append(f"{relative}: missing ESAF control manifest")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"{relative}/{path.name}: {error}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{relative}/{path.name}: JSON document must be an object")
        return None
    return value
