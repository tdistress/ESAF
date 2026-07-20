"""Repository-aware semantic validation for crosswalk snapshots."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

from tools.crosswalks.io import load_yaml_mapping, parse_front_matter
from tools.crosswalks.digests import event_digest, snapshot_digest
from tools.crosswalks.manifest import build_control_manifest, render_manifest
from tools.crosswalks.schemas import load_schemas, schema_errors
import tools.crosswalks.uk_ce_plus_v32_reverse_profile as uk_ce_plus_v32_reverse_profile


_UK_CE_PLUS_V32_REVERSE_PROFILE_ID = (
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--"
    "esaf-0.4-alpha--0.2.0"
)

_OUTCOME_AUD_SCOPE = (
    "requires relevant, reliable, complete, timely, attributable, and "
    "integrity-protected evidence for each AI assessment scope and period."
)
_OUTCOME_AUD_FINDINGS = (
    "requires AI assessment findings to be documented, classified, assigned, "
    "prioritized, remediated, escalated, retested, closed, and retained according "
    "to the named governance factors."
)
_OUTCOME_AUD_RETAINED_PROCEDURE = (
    "requires relevant, reliable, complete, timely, attributable, and "
    "integrity-protected evidence to be obtained and retained for each AI "
    "assessment procedure, determination, scope, and period."
)
_OUTCOME_AUD_PROCEDURE = (
    "requires relevant, reliable, complete, timely, attributable, and "
    "integrity-protected evidence for each AI assessment procedure, determination, "
    "scope, and period."
)
_OUTCOME_RECORDS = (
    "requires AI records, notices, registrations, reports, and evidence to be "
    "created, protected, retained, disclosed, submitted, and disposed of according "
    "to applicable record requirements."
)
_OUTCOME_VULNERABILITIES = (
    "requires vulnerabilities affecting AI infrastructure and dependencies to be "
    "identified, assessed, prioritized, remediated, mitigated, or accepted according "
    "to the named risk factors."
)
_OUTCOME_AUTHENTICATION = (
    "requires identities to be authenticated before access to non-public AI assets "
    "using mechanisms whose strength, context, and resistance are proportionate to "
    "risk."
)
_OUTCOME_CREDENTIALS = (
    "requires credentials used by AI capabilities to be generated, stored, "
    "distributed, used, rotated, revoked, and monitored through approved "
    "secrets-management mechanisms."
)
_OUTCOME_APPLICATION_MISUSE = (
    "requires AI application misuse, adversarial behavior, automated abuse, denial "
    "of service, excessive consumption, repeated policy evasion, and out-of-purpose "
    "use to be detected, constrained, and responded to."
)
_OUTCOME_INFRASTRUCTURE_HARDENING = (
    "requires AI compute, hosts, networks, images, runtimes, and management "
    "interfaces to be hardened using approved, versioned, and risk-proportionate "
    "configuration baselines."
)
_OUTCOME_CONFIGURATION_CHANGE = (
    "requires infrastructure affecting AI workloads to be controlled, versioned, "
    "reviewed, tested, approved, reproducible, and monitored configuration with "
    "rollback or recovery."
)
_OUTCOME_REPLAY_RESISTANT_AUTHENTICATION = (
    "requires identities to be authenticated before access to non-public AI assets "
    "using mechanisms whose strength, context, and resistance to replay or credential "
    "theft are proportionate to risk."
)

# Source-versioned prose is deliberately independent of authored Markdown at runtime.
_UK_CE_PLUS_V32_SUPPORTED_OUTCOME_TEXTS = {
    ("CEPTS3.2-M-004", "AUD-120"): _OUTCOME_AUD_SCOPE,
    ("CEPTS3.2-M-010", "AUD-130"): _OUTCOME_AUD_FINDINGS,
    ("CEPTS3.2-M-011", "AUD-120"): _OUTCOME_AUD_RETAINED_PROCEDURE,
    ("CEPTS3.2-S-007", "AUD-120"): _OUTCOME_AUD_PROCEDURE,
    ("CEPTS3.2-S-008", "CMP-110"): _OUTCOME_RECORDS,
    ("CEPTS3.2-T1-009", "INF-120"): _OUTCOME_VULNERABILITIES,
    ("CEPTS3.2-T1-011", "IAM-110"): _OUTCOME_AUTHENTICATION,
    ("CEPTS3.2-T1-012", "IAM-110"): _OUTCOME_AUTHENTICATION,
    ("CEPTS3.2-T1-013", "IAM-140"): _OUTCOME_CREDENTIALS,
    ("CEPTS3.2-T1-014", "APP-150"): _OUTCOME_APPLICATION_MISUSE,
    ("CEPTS3.2-T1-015", "APP-150"): _OUTCOME_APPLICATION_MISUSE,
    ("CEPTS3.2-T2-007", "INF-120"): _OUTCOME_VULNERABILITIES,
    ("CEPTS3.2-T3-005", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-015", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-016", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-017", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-021", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-022", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-023", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-024", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-025", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-027", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-028", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-029", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-031", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-032", "INF-130"): _OUTCOME_CONFIGURATION_CHANGE,
    ("CEPTS3.2-T3-033", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-034", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-035", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T3-036", "INF-110"): _OUTCOME_INFRASTRUCTURE_HARDENING,
    ("CEPTS3.2-T4-008", "IAM-110"): _OUTCOME_REPLAY_RESISTANT_AUTHENTICATION,
}

_REVERSE_NARROWING_STATEMENT = (
    "Conditions only narrow this supported claim; they do not create either outcome."
)
_REVERSE_PROHIBITION_CATEGORIES = (
    "implementation",
    "effectiveness",
    "sufficiency",
    "compliance",
    "certification",
    "equivalence",
    "continuous_assurance",
    "population_wide_coverage",
    "current_scheme_coverage",
)
_REVERSE_PROHIBITION_DENIALS = {
    "implementation": "does not establish control implementation",
    "effectiveness": "does not establish control effectiveness",
    "sufficiency": "is not sufficient evidence",
    "compliance": "does not establish ESAF compliance",
    "certification": "does not authorize or establish certification",
    "equivalence": "is not equivalent",
    "continuous_assurance": "does not provide continuous assurance",
    "population_wide_coverage": "does not establish population-wide coverage",
    "current_scheme_coverage": "does not establish current-scheme coverage",
}


@dataclass
class ValidationResult:
    errors: list[str]
    mapping_sets: list[dict[str, object]]
    lifecycle_records: list[dict[str, object]]


def snapshot_directories(root: Path) -> list[Path]:
    """Return snapshot directories in deterministic repository order."""
    base = root / "crosswalks" / "mappings"
    if base.is_symlink():
        return []
    return sorted(path.parent for path in base.rglob("README.md")) if base.exists() else []


def _validate_mappings_tree(root: Path) -> list[str]:
    """Reject every mappings-tree entry that is not part of a valid snapshot path."""
    base = root / "crosswalks" / "mappings"
    if base.is_symlink():
        return ["crosswalks/mappings: unexpected mappings-tree entry"]
    if not base.exists():
        return []
    errors: list[str] = []
    try:
        entries = sorted(base.rglob("*"), key=lambda path: path.as_posix())
    except OSError as error:
        return [f"crosswalks/mappings: cannot inspect mappings tree: {error}"]
    snapshots = {
        path.parent
        for path in entries
        if path.name == "README.md"
        and path.is_file()
        and not path.is_symlink()
        and len(path.parent.relative_to(base).parts) in {4, 5}
    }
    ancestors = {
        ancestor
        for snapshot in snapshots
        for ancestor in snapshot.parents
        if ancestor != base and base in ancestor.parents
    }
    allowed_files = {"README.md", "PROVISION_INVENTORY.md", "ESAF_CONTROL_MANIFEST.json"}
    record_name = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
    for entry in entries:
        relative = entry.relative_to(root).as_posix()
        valid = False
        if entry.is_symlink():
            valid = False
        elif entry.is_dir():
            valid = entry in snapshots or entry in ancestors
        elif entry.is_file():
            if entry.parent == base and entry.name == ".gitkeep":
                valid = True
            elif entry.parent in snapshots:
                valid = entry.name in allowed_files or bool(record_name.fullmatch(entry.name))
        if not valid:
            errors.append(f"{relative}: unexpected mappings-tree entry")
    return errors


def validate(root: Path, baseline_ref: str | None = None) -> ValidationResult:
    """Validate all crosswalk mapping snapshots below ``root``."""
    errors: list[str] = []
    mapping_sets: list[dict[str, object]] = []
    lifecycle_records: list[dict[str, object]] = []
    seen_mapping_set_ids: set[str] = set()
    schema_root = root if (root / "crosswalks" / "schema").exists() else Path(__file__).parents[2]
    validators = load_schemas(schema_root)
    errors.extend(_validate_mappings_tree(root))

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
    lifecycle_errors, lifecycle_records = _load_lifecycle_records(root, validators)
    errors.extend(lifecycle_errors)
    errors.extend(validate_lifecycle(lifecycle_records))
    errors.extend(_validate_lifecycle_links(root, mapping_sets, lifecycle_records))
    _attach_lifecycle_records(mapping_sets, lifecycle_records)
    result = ValidationResult(sorted(set(errors)), mapping_sets, lifecycle_records)
    if baseline_ref is not None:
        result.errors.extend(validate_baseline(root, baseline_ref, result))
        result.errors = sorted(set(result.errors))
    return result


def _attach_lifecycle_records(
    mapping_sets: list[dict[str, object]],
    lifecycle_records: list[dict[str, object]],
) -> None:
    """Attach lifecycle metadata to the generator model after validation."""
    lifecycle_by_id = {
        metadata["mapping_set_id"]: metadata
        for record in lifecycle_records
        if isinstance((metadata := record.get("metadata")), dict)
        and isinstance(metadata.get("mapping_set_id"), str)
    }
    for model in mapping_sets:
        metadata = model.get("metadata")
        mapping_set_id = (
            metadata.get("mapping_set_id") if isinstance(metadata, dict) else None
        )
        model["lifecycle"] = lifecycle_by_id.get(mapping_set_id)


def validate_lifecycle(records: list[dict[str, object]]) -> list[str]:
    """Validate lifecycle state order, identifiers, and digest chains."""
    errors: list[str] = []
    expected_states = ("approved", "published", "deprecated", "retired")
    seen_mapping_sets: set[str] = set()
    for model in records:
        record = model.get("metadata", model)
        path = str(model.get("path", "lifecycle record"))
        if not isinstance(record, dict):
            continue
        mapping_set_id = record.get("mapping_set_id")
        if isinstance(mapping_set_id, str):
            if mapping_set_id in seen_mapping_sets:
                errors.append(
                    f"{path}: duplicate lifecycle record for mapping set {mapping_set_id}"
                )
            seen_mapping_sets.add(mapping_set_id)
        events = record.get("events")
        if not isinstance(events, list):
            continue
        states = [event.get("state") for event in events if isinstance(event, dict)]
        if states != list(expected_states[: len(states)]):
            errors.append(f"{path}: invalid lifecycle transition")
        seen_event_ids: set[object] = set()
        previous = "0" * 64
        previous_date: date | None = None
        for event in events:
            if not isinstance(event, dict):
                continue
            event_id = event.get("event_id")
            if isinstance(event_id, str):
                if event_id in seen_event_ids:
                    errors.append(f"{path}: duplicate lifecycle event {event_id}")
                seen_event_ids.add(event_id)
            if event.get("previous_event_digest") != previous:
                errors.append(f"{path}: invalid previous lifecycle event digest")
            canonical = {
                field: value
                for field, value in event.items()
                if field != "event_digest" and isinstance(value, str)
            }
            calculated = event_digest(canonical)
            if event.get("event_digest") != calculated:
                errors.append(f"{path}: lifecycle event digest mismatch")
            previous = str(event.get("event_digest", ""))
            event_date = event.get("date")
            if isinstance(event_date, str):
                try:
                    parsed_date = date.fromisoformat(event_date)
                except ValueError:
                    parsed_date = None
                if parsed_date is not None:
                    if previous_date is not None and parsed_date < previous_date:
                        errors.append(f"{path}: lifecycle event dates must be nondecreasing")
                    previous_date = parsed_date
            if (
                event.get("state") == "deprecated"
                and not event.get("successor_id")
                and not event.get("reason")
            ):
                errors.append(
                    f"{path}: deprecated lifecycle requires successor or explanation"
                )
    return errors


def validate_baseline(
    root: Path, baseline_ref: str, current: ValidationResult
) -> list[str]:
    """Compare protected candidate content with an immutable Git baseline."""
    protected = any(
        isinstance(model.get("metadata"), dict)
        and model["metadata"].get("status") == "approved"  # type: ignore[index]
        for model in current.mapping_sets
    ) or bool(current.lifecycle_records)
    commit = _resolve_commit(root, baseline_ref)
    if commit is None:
        return (
            ["trusted baseline is unavailable for protected crosswalk content"]
            if protected
            else []
        )

    errors: list[str] = []
    schema_root = (
        root
        if (root / "crosswalks" / "schema").exists()
        else Path(__file__).parents[2]
    )
    validators = load_schemas(schema_root)
    baseline_paths = _git_tree_paths(root, commit, "crosswalks/mappings")
    baseline_approved_ids: set[str] = set()
    for readme in (path for path in baseline_paths if path.endswith("/README.md")):
        try:
            metadata = _front_matter_bytes(_git_show(root, commit, readme))
        except ValueError as error:
            errors.append(
                f"{readme}: trusted baseline snapshot metadata is malformed: {error}"
            )
            continue
        if not isinstance(metadata, dict) or schema_errors(
            validators["mapping-set"], metadata, readme  # type: ignore[arg-type]
        ):
            errors.append(
                f"{readme}: trusted baseline snapshot metadata is malformed"
            )
            continue
        status = metadata.get("status")
        if status != "approved":
            continue
        mapping_set_id = metadata.get("mapping_set_id")
        if isinstance(mapping_set_id, str):
            baseline_approved_ids.add(mapping_set_id)
        directory = readme.rsplit("/", 1)[0]
        baseline_files = sorted(
            path for path in baseline_paths if path.startswith(directory + "/")
        )
        candidate = root / directory
        candidate_files = (
            sorted(
                path.relative_to(root).as_posix()
                for path in candidate.rglob("*")
                if path.is_file() and not path.is_symlink()
            )
            if candidate.exists()
            else []
        )
        differs = baseline_files != candidate_files
        if not differs:
            for path in baseline_files:
                try:
                    if (root / path).read_bytes() != _git_show(root, commit, path):
                        differs = True
                        break
                except OSError:
                    differs = True
                    break
        if differs:
            errors.append(f"{directory}: approved snapshot differs from trusted baseline")

    current_lifecycle = {}
    for model in current.lifecycle_records:
        metadata = model.get("metadata")
        mapping_set_id = (
            metadata.get("mapping_set_id") if isinstance(metadata, dict) else None
        )
        if isinstance(mapping_set_id, str):
            current_lifecycle[mapping_set_id] = metadata
    for path in _git_tree_paths(root, commit, "crosswalks/registry"):
        if not path.endswith(".md"):
            continue
        try:
            baseline = _front_matter_bytes(_git_show(root, commit, path))
        except ValueError as error:
            errors.append(
                f"{path}: trusted baseline lifecycle metadata is malformed: {error}"
            )
            continue
        if not isinstance(baseline, dict) or schema_errors(
            validators["lifecycle-record"], baseline, path  # type: ignore[arg-type]
        ):
            errors.append(
                f"{path}: trusted baseline lifecycle metadata is malformed"
            )
            continue
        mapping_set_id = baseline.get("mapping_set_id")
        if not isinstance(mapping_set_id, str):
            errors.append(
                f"{path}: trusted baseline lifecycle metadata is malformed: "
                "mapping_set_id must be a string"
            )
            continue
        baseline_events = baseline.get("events")
        if not isinstance(baseline_events, list):
            errors.append(
                f"{path}: trusted baseline lifecycle metadata is malformed: "
                "events must be an array"
            )
            continue
        if mapping_set_id in baseline_approved_ids and not baseline_events:
            errors.append(
                f"{path}: trusted baseline lifecycle metadata is malformed"
            )
            continue
        candidate = current_lifecycle.get(mapping_set_id)
        candidate_events = candidate.get("events") if isinstance(candidate, dict) else None
        if (
            not isinstance(candidate_events, list)
            or candidate_events[: len(baseline_events)] != baseline_events
        ):
            errors.append(f"{path}: baseline lifecycle events are not an exact prefix")
    return errors


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


def _load_lifecycle_records(
    root: Path, validators: dict[str, object]
) -> tuple[list[str], list[dict[str, object]]]:
    errors: list[str] = []
    records: list[dict[str, object]] = []
    registry = root / "crosswalks" / "registry"
    if not registry.exists():
        return errors, records
    try:
        entries = sorted(registry.iterdir(), key=lambda path: path.name)
    except OSError as error:
        return [f"crosswalks/registry: cannot inspect lifecycle registry: {error}"], records
    for path in entries:
        relative = path.relative_to(root).as_posix()
        if path.name == ".gitkeep" and path.is_file() and not path.is_symlink():
            continue
        if path.is_symlink() or not path.is_file() or path.suffix != ".md":
            errors.append(f"{relative}: unexpected lifecycle registry entry")
            continue
        try:
            metadata, body = parse_front_matter(path)
        except yaml.YAMLError as error:
            errors.append(f"{relative}: invalid YAML: {error}")
            continue
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{relative}: {error}")
            continue
        errors.extend(
            schema_errors(
                validators["lifecycle-record"], metadata, relative  # type: ignore[arg-type]
            )
        )
        mapping_set_id = metadata.get("mapping_set_id")
        if isinstance(mapping_set_id, str) and path.name != f"{mapping_set_id}.md":
            errors.append(f"{relative}: lifecycle filename disagrees with mapping-set id")
        records.append({"path": relative, "metadata": metadata, "body": body})
    return errors, records


def _validate_lifecycle_links(
    root: Path,
    mapping_sets: list[dict[str, object]],
    lifecycle_records: list[dict[str, object]],
) -> list[str]:
    errors: list[str] = []
    snapshots = {}
    for model in mapping_sets:
        metadata = model.get("metadata")
        mapping_set_id = (
            metadata.get("mapping_set_id") if isinstance(metadata, dict) else None
        )
        if isinstance(mapping_set_id, str):
            snapshots[mapping_set_id] = model
    lifecycle_counts: dict[str, int] = {}
    lifecycle_by_id: dict[str, dict[str, object]] = {}
    active: dict[tuple[object, object, object, object], str] = {}
    for lifecycle_model in lifecycle_records:
        lifecycle = lifecycle_model.get("metadata")
        relative = str(lifecycle_model.get("path", "lifecycle record"))
        if not isinstance(lifecycle, dict):
            continue
        mapping_set_id = lifecycle.get("mapping_set_id")
        if not isinstance(mapping_set_id, str):
            continue
        lifecycle_counts[mapping_set_id] = lifecycle_counts.get(mapping_set_id, 0) + 1
        lifecycle_by_id[mapping_set_id] = lifecycle
        snapshot_model = snapshots.get(mapping_set_id)
        if not isinstance(snapshot_model, dict):
            errors.append(f"{relative}: lifecycle record has no mapping-set snapshot")
            continue
        metadata = snapshot_model.get("metadata")
        readme_path = snapshot_model.get("path")
        if not isinstance(metadata, dict) or not isinstance(readme_path, str):
            continue
        snapshot = (root / readme_path).parent
        try:
            digest = snapshot_digest(root, snapshot)
        except ValueError as error:
            errors.append(f"{relative}: cannot compute lifecycle snapshot digest: {error}")
        else:
            if lifecycle.get("snapshot_digest") != digest:
                errors.append(f"{relative}: lifecycle snapshot digest mismatch")
        events = lifecycle.get("events")
        states = (
            [event.get("state") for event in events if isinstance(event, dict)]
            if isinstance(events, list)
            else []
        )
        snapshot_status = metadata.get("status")
        if isinstance(snapshot_status, str) and snapshot_status in {"draft", "reviewed"} and states:
            errors.append(
                f"{relative}: {snapshot_status} mapping set requires empty lifecycle events"
            )
        if snapshot_status == "approved" and not states:
            errors.append(
                f"{relative}: approved mapping set requires an approval lifecycle event"
            )
        if "published" in states and metadata.get("status") != "approved":
            errors.append(f"{relative}: published lifecycle requires approved snapshot")
        if states and states[-1] == "published":
            authority = metadata.get("authority")
            publication = metadata.get("publication")
            source_version = metadata.get("source_version")
            esaf_release = metadata.get("esaf_release")
            key = (
                authority.get("id") if isinstance(authority, dict) else None,
                publication.get("id") if isinstance(publication, dict) else None,
                source_version.get("id") if isinstance(source_version, dict) else None,
                esaf_release.get("id") if isinstance(esaf_release, dict) else None,
            )
            if not all(isinstance(value, str) for value in key):
                continue
            prior = active.get(key)
            if prior is not None and prior != mapping_set_id:
                errors.append(
                    f"{relative}: multiple active published mapping sets for {key}"
                )
            active[key] = str(mapping_set_id)
    for mapping_set_id, snapshot_model in sorted(snapshots.items()):
        if lifecycle_counts.get(mapping_set_id, 0) != 1:
            relative = str(snapshot_model.get("path", mapping_set_id))
            errors.append(
                f"{relative}: mapping set requires lifecycle record "
                f"(found {lifecycle_counts.get(mapping_set_id, 0)})"
            )

    def event_links(lifecycle: dict[str, object], field: str) -> set[str]:
        events = lifecycle.get("events", [])
        if not isinstance(events, list):
            return set()
        return {
            value
            for event in events
            if isinstance(event, dict)
            and isinstance((value := event.get(field)), str)
            and value
        }

    for mapping_set_id, snapshot_model in sorted(snapshots.items()):
        metadata = snapshot_model.get("metadata")
        lifecycle = lifecycle_by_id.get(mapping_set_id, {})
        if not isinstance(metadata, dict):
            continue
        predecessor_values = event_links(lifecycle, "predecessor_id")
        declared_predecessor = metadata.get("predecessor_id")
        if isinstance(declared_predecessor, str) and declared_predecessor:
            predecessor_values.add(declared_predecessor)
        successor_values = event_links(lifecycle, "successor_id")
        relative = str(snapshot_model.get("path", mapping_set_id))
        if len(predecessor_values) > 1:
            errors.append(f"{relative}: conflicting predecessor mapping-set links")
        if len(successor_values) > 1:
            errors.append(f"{relative}: conflicting successor mapping-set links")
        for field, values in (("predecessor", predecessor_values), ("successor", successor_values)):
            for linked_id in sorted(values):
                if linked_id == mapping_set_id:
                    errors.append(f"{relative}: lifecycle link must not reference itself")
                elif linked_id not in snapshots:
                    errors.append(f"{relative}: {field} mapping set does not exist: {linked_id}")
        for successor_id in sorted(successor_values & snapshots.keys()):
            target_metadata = snapshots[successor_id].get("metadata")
            if not isinstance(target_metadata, dict) or target_metadata.get("predecessor_id") != mapping_set_id:
                errors.append(f"{relative}: successor link is not reciprocated by target predecessor_id")
        for predecessor_id in sorted(predecessor_values & snapshots.keys()):
            predecessor_lifecycle = lifecycle_by_id.get(predecessor_id, {})
            if mapping_set_id not in event_links(predecessor_lifecycle, "successor_id"):
                errors.append(f"{relative}: predecessor link is not reciprocated by predecessor lifecycle")
    return errors


def _resolve_commit(root: Path, reference: str) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--verify", "--quiet", f"{reference}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def _git_tree_paths(root: Path, commit: str, prefix: str) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only", "-z", commit, "--", prefix],
        check=True,
        capture_output=True,
    )
    return sorted(
        path.decode("utf-8")
        for path in completed.stdout.split(b"\0")
        if path
    )


def _git_show(root: Path, commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(root), "show", f"{commit}:{path}"],
        check=True,
        capture_output=True,
    ).stdout


def _front_matter_bytes(raw: bytes) -> dict[str, object] | None:
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        return None
    try:
        text = raw.decode("utf-8")
        if not text.startswith("---\n"):
            return None
        parts = text.split("---\n", 2)
        if len(parts) != 3:
            return None
        value = load_yaml_mapping(parts[1])
    except ValueError:
        raise
    except (UnicodeError, yaml.YAMLError, IndexError):
        return None
    return value


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
            root, snapshot / "README.md", mapping_set.get("status"), f"{relative}/README.md"
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
    expected_paths = _snapshot_paths(mapping_set)
    if expected_paths and relative not in expected_paths:
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
                root,
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
        if record.get("status") == "reviewed":
            errors.extend(
                _validate_reviewed_findings(
                    mapping_set.get("findings"), record_relative, record_id
                )
            )
        errors.extend(_validate_reviewed_text(root, path, record.get("status"), record_relative))

    errors.extend(_validate_finding_targets(mapping_set, seen_record_ids, relative))
    errors.extend(_validate_publication_rights(mapping_set, records, relative))

    if manifest is not None:
        errors.extend(
            _validate_control_manifest(root, snapshot, mapping_set, manifest, provisions)
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
    provisions: list[dict[str, object]],
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

    for provision in provisions:
        record = provision.get("metadata")
        record_path = provision.get("path")
        if not isinstance(record, dict) or not isinstance(record_path, str):
            continue
        errors.extend(
            f"{record_path}: {message}"
            for message in validate_reverse_evidence_record(
                record, mapping_set, expected_controls
            )
        )
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
                    f"{record_path}: unresolved ESAF control identifier {control_id}"
                )
            elif control.get("version") != control_version:
                errors.append(
                    f"{record_path}: ESAF control version mismatch for {control_id}"
                )
            if control is None:
                continue
            provenance_fields = (
                "esaf_control_path",
                "esaf_control_sha256",
                "esaf_requirement_locator",
            )
            present = [field for field in provenance_fields if field in relationship]
            if present and len(present) != len(provenance_fields):
                errors.append(
                    f"{record_path}: incomplete provenance triplet for {control_id}"
                )
                continue
            if not present:
                continue
            expected_path = control.get("path")
            expected_digest = control.get("record_sha256")
            expected_locator = f"controls/{expected_path}#requirement"
            expected = {
                "esaf_control_path": expected_path,
                "esaf_control_sha256": expected_digest,
                "esaf_requirement_locator": expected_locator,
            }
            for field, expected_value in expected.items():
                if relationship.get(field) != expected_value:
                    errors.append(f"{record_path}: {field} mismatch for {control_id}")
    if mapping_set.get("mapping_set_id") == _UK_CE_PLUS_V32_REVERSE_PROFILE_ID:
        mapped_pairs: list[tuple[str, str]] = []
        for provision in provisions:
            record = provision.get("metadata")
            if not isinstance(record, dict) or record.get("disposition") != "mapped":
                continue
            provision_id = record.get("external_provision_id")
            relationships = record.get("relationships", [])
            if not isinstance(provision_id, str) or not isinstance(relationships, list):
                continue
            for relationship in relationships:
                if not isinstance(relationship, dict):
                    continue
                control_id = relationship.get("esaf_control_id")
                if isinstance(control_id, str):
                    mapped_pairs.append((provision_id, control_id))
        errors.extend(
            f"{relative}: {message}"
            for message in uk_ce_plus_v32_reverse_profile.validate_observation_registry(
                mapped_pairs,
                uk_ce_plus_v32_reverse_profile.OBSERVATION_PROFILE_ENTRIES,
            )
        )
        errors.extend(
            f"{relative}: {message}"
            for message in _reverse_supported_outcome_registry_errors(
                uk_ce_plus_v32_reverse_profile.OBSERVATION_PROFILE_ENTRIES
            )
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
    if isinstance(rights, dict):
        universe = {
            "identifiers", "titles", "structural_inventory", "paraphrases",
            "derivative_mapping_analysis", "official_links",
        }
        permitted_values = rights.get("permitted_elements", [])
        prohibited_values = rights.get("prohibited_elements", [])
        permitted = {
            item for item in permitted_values if isinstance(item, str)
        } if isinstance(permitted_values, list) else set()
        prohibited = {
            item for item in prohibited_values if isinstance(item, str)
        } if isinstance(prohibited_values, list) else set()
        if permitted & prohibited:
            errors.append(f"{relative}: publication-rights elements must be disjoint")
        if permitted | prohibited != universe:
            errors.append(f"{relative}: publication-rights elements must exhaustively partition the schema elements")

    findings = mapping_set.get("findings", [])
    if isinstance(findings, list):
        seen_finding_ids: set[str] = set()
        for finding in findings:
            finding_id = finding.get("finding_id") if isinstance(finding, dict) else None
            if not isinstance(finding_id, str):
                continue
            if finding_id in seen_finding_ids:
                errors.append(f"{relative}: duplicate finding id {finding_id}")
            seen_finding_ids.add(finding_id)
    if mapping_status == "reviewed":
        errors.extend(_validate_reviewed_findings(findings, relative))
    if mapping_status == "approved":
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
                if severity == "Minor" and (
                    not isinstance(status, str)
                    or status not in {"resolved", "accepted"}
                ):
                    errors.append(
                        f"{relative}: Minor findings must be resolved or formally accepted"
                    )
    return errors


def _validate_finding_targets(
    mapping_set: dict[str, object], record_ids: set[str], relative: str
) -> list[str]:
    errors: list[str] = []
    findings = mapping_set.get("findings", [])
    if not isinstance(findings, list):
        return errors
    for finding in findings:
        affected = finding.get("affected_record_ids") if isinstance(finding, dict) else None
        if not isinstance(affected, list):
            continue
        for record_id in affected:
            if isinstance(record_id, str) and record_id not in record_ids:
                errors.append(f"{relative}: finding target {record_id} does not resolve")
    return errors


def _validate_publication_rights(
    mapping_set: dict[str, object], records: list[dict[str, object]], relative: str
) -> list[str]:
    rights = mapping_set.get("publication_rights")
    if not isinstance(rights, dict):
        return []
    permitted = rights.get("permitted_elements", [])
    prohibited = rights.get("prohibited_elements", [])
    if not isinstance(permitted, list) or not isinstance(prohibited, list):
        return []
    committed = {"identifiers", "structural_inventory", "official_links"}
    if records:
        committed.add("derivative_mapping_analysis")
    for record in records:
        if record.get("title"):
            committed.add("titles")
        context = record.get("context")
        if isinstance(context, dict) and context.get("mode") == "paraphrase":
            committed.add("paraphrases")
    errors = []
    for element in sorted(committed):
        if element not in permitted or element in prohibited:
            errors.append(f"{relative}: committed element {element} is not permitted by publication rights")
    return errors


def _validate_reviewed_findings(
    findings: object, relative: str, record_id: object | None = None
) -> list[str]:
    """Return entity-specific reviewed-finding diagnostics."""
    if not isinstance(findings, list):
        return []
    errors: list[str] = []
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        affected = finding.get("affected_record_ids")
        if not isinstance(affected, list):
            continue
        targets_entity = (
            not affected
            if record_id is None
            else isinstance(record_id, str)
            and any(
                isinstance(affected_id, str) and affected_id == record_id
                for affected_id in affected
            )
        )
        if not targets_entity:
            continue
        severity = finding.get("severity")
        status = finding.get("status")
        if (
            isinstance(severity, str)
            and severity in {"Critical", "Important"}
            and isinstance(status, str)
            and status in {"open", "accepted"}
        ):
            errors.append(
                f"{relative}: {status} {severity} review finding blocks reviewed content"
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


def validate_reverse_evidence_record(
    record: dict[str, object],
    mapping_set: dict[str, object],
    manifest_controls: dict[str, dict[str, object]],
) -> list[str]:
    """Validate a source-versioned reverse-evidence authoring profile."""
    if mapping_set.get("mapping_set_id") != _UK_CE_PLUS_V32_REVERSE_PROFILE_ID:
        return []

    errors: list[str] = []
    external_id = record.get("external_provision_id")
    relationships = record.get("relationships", [])
    if not isinstance(relationships, list):
        relationships = []
    disposition = record.get("disposition")

    if disposition == "no_direct_mapping":
        rationale = record.get("negative_rationale")
        specific_pattern = re.compile(
            rf"^Missing outcome: {re.escape(str(external_id))} - "
            r"external result '(?P<external_result>[^']{10,})' does not evidence "
            r"ESAF outcome '(?P<esaf_outcome>[^']{10,})'\.$"
        )
        match = (
            specific_pattern.fullmatch(rationale)
            if isinstance(rationale, str)
            else None
        )
        context = record.get("context")
        context_summary = context.get("summary") if isinstance(context, dict) else None
        if (
            not isinstance(external_id, str)
            or match is None
            or not isinstance(context_summary, str)
            or match.group("external_result").lower() not in context_summary.lower()
            or "generic" in match.group("esaf_outcome").lower()
            or "direct mapping" in match.group("esaf_outcome").lower()
            or _reverse_outcome_is_semantic_placeholder(
                match.group("esaf_outcome")
            )
        ):
            errors.append(
                "no_direct_mapping rationale must name a paraphrase-bound external "
                "result and specific ESAF outcome using "
                f"'Missing outcome: {external_id} - external result <result> does "
                "not evidence ESAF outcome <outcome>'"
            )
        if relationships:
            errors.append("negative reverse-evidence record must have no relationships")
        return errors
    if disposition == "out_of_scope":
        errors.append("complete-publication reverse profile does not permit out_of_scope")
        return errors
    if disposition != "mapped":
        return errors
    if not relationships:
        errors.append(
            "mapped reverse-evidence record requires at least one relationship"
        )
        return errors

    condition_order = (
        "actor",
        "scope",
        "population",
        "sample",
        "assessment_date",
        "evidence_date",
        "tool",
        "provenance",
        "exception",
        "delivery_partner_discretion",
        "point_in_time_status",
    )
    seen_legs: set[tuple[object, object]] = set()
    for leg_index, leg in enumerate(relationships):
        if not isinstance(leg, dict):
            continue
        control_id = leg.get("esaf_control_id")
        direction = leg.get("direction")
        leg_label = f"relationship {leg_index + 1}"
        if direction != "external_to_esaf":
            errors.append(f"{leg_label} must use direction external_to_esaf")
        duplicate_key = (control_id, direction)
        if duplicate_key in seen_legs:
            errors.append(f"duplicate reverse-evidence relationship leg for {control_id}")
        seen_legs.add(duplicate_key)

        control = manifest_controls.get(control_id) if isinstance(control_id, str) else None
        if control is None:
            errors.append(f"{leg_label} references unresolved manifest control {control_id}")
        else:
            expected = {
                "esaf_control_version": control.get("version"),
                "esaf_control_path": control.get("path"),
                "esaf_control_sha256": control.get("record_sha256"),
                "esaf_requirement_locator": (
                    f"controls/{control.get('path')}#requirement"
                ),
            }
            for field, expected_value in expected.items():
                if leg.get(field) != expected_value:
                    errors.append(
                        f"{leg_label} {field} must exactly match pinned manifest "
                        f"control {control_id}"
                    )

        rationale = leg.get("rationale")
        exact_outcome_marker = f"Supported ESAF outcome: {control_id} "
        narrowing_statement = _REVERSE_NARROWING_STATEMENT
        if not isinstance(rationale, str):
            rationale = ""
        if "External observation: " not in rationale:
            errors.append(f"{leg_label} must state an external observation independently")
            observation = ""
        else:
            observation_segment = rationale.split("External observation: ", 1)[1].split(
                "Supported ESAF outcome:", 1
            )[0].strip()
            has_one_terminal_period = observation_segment.endswith(".") and not (
                observation_segment.endswith("..")
            )
            if not has_one_terminal_period:
                errors.append(
                    f"{leg_label} observation contract: external observation must be "
                    "one canonical JSON object followed by one terminal period"
                )
            observation = (
                observation_segment[:-1]
                if observation_segment.endswith(".")
                else observation_segment
            )
            errors.extend(
                f"{leg_label} observation contract: {message}"
                for message in uk_ce_plus_v32_reverse_profile.validate_observation_claim(
                    observation, external_id, control_id
                )
            )
        supported_outcome_text = (
            _UK_CE_PLUS_V32_SUPPORTED_OUTCOME_TEXTS.get((external_id, control_id))
            if isinstance(external_id, str) and isinstance(control_id, str)
            else None
        )
        if supported_outcome_text is None:
            errors.append(
                f"{leg_label} requires source-versioned supported-outcome text for "
                "the exact provision/control pair"
            )
        else:
            canonical_rationale = (
                f"External observation: {observation}. Supported ESAF outcome: "
                f"{control_id} {supported_outcome_text} {narrowing_statement}"
            )
            if rationale != canonical_rationale:
                errors.append(
                    f"{leg_label} rationale must equal the exact canonical "
                    "reverse-evidence template"
                )
        if exact_outcome_marker not in rationale:
            errors.append(f"{leg_label} must state the exact supported ESAF outcome")
        if narrowing_statement not in rationale:
            errors.append(f"{leg_label} must state that conditions only narrow support")
        if re.search(
            r"(?is)\bconditions?\b\s+(?:alone\s+)?"
            r"(?:supply|create|establish|provide)\b",
            rationale,
        ) or re.search(
            r"(?is)\b(?:outcome|observation|result|support)\b\s+(?:is|are)\s+"
            r"(?:supplied|created|established|provided)\s+by\s+conditions?\b",
            rationale,
        ):
            errors.append(f"{leg_label} conditions must not create an outcome")
        prohibited_claim = re.compile(
            r"(?i)\b(?:implementation|implemented|effectiveness|effective|"
            r"sufficiency|sufficient|compliance|compliant|certification|certified|"
            r"equivalence|equivalent|continuous[- ]assurance|"
            r"population[- ]wide(?:\s+coverage)?|"
            r"current[- ]scheme(?:\s+coverage)?)\b"
        )
        if prohibited_claim.search(rationale):
            errors.append(f"{leg_label} rationale contains prohibited assurance claim")

        expected_evidence = leg.get("expected_evidence")
        evidence_text = (
            " ".join(expected_evidence).lower()
            if isinstance(expected_evidence, list)
            and all(isinstance(item, str) for item in expected_evidence)
            else ""
        )
        selection_text = f"{observation} {evidence_text}"
        if re.search(
            r"\b(?:sample|sampled|sampling|select|selected|selection)\w*\b",
            selection_text,
        ) and not _reverse_evidence_has_population_boundary(evidence_text):
            errors.append(
                f"{leg_label} selection or sampling evidence requires an explicit "
                "population boundary"
            )

        prohibited_inferences = leg.get("prohibited_inferences")
        if not _reverse_prohibitions_have_required_categories(
            prohibited_inferences, external_id
        ):
            errors.append(
                f"{leg_label} requires provision-specific prohibited_inferences "
                "for every binding assurance prohibition"
            )
        elif not _reverse_prohibitions_bind_observation_and_outcome(
            prohibited_inferences, external_id, observation, control_id
        ):
            errors.append(
                f"{leg_label} must bind every prohibited inference to the observed "
                "result and cited ESAF outcome"
            )

        raw_conditions = leg.get("conditions")
        parsed_conditions: list[dict[str, object]] = []
        if isinstance(raw_conditions, list):
            for condition_index, raw_condition in enumerate(raw_conditions):
                try:
                    condition = (
                        json.loads(raw_condition)
                        if isinstance(raw_condition, str)
                        else None
                    )
                except json.JSONDecodeError:
                    condition = None
                if not isinstance(condition, dict) or set(condition) != {
                    "condition",
                    "status",
                    "evidence_references",
                }:
                    errors.append(
                        f"{leg_label} condition {condition_index + 1} must be a canonical "
                        "condition/status/evidence_references JSON string"
                    )
                    continue
                if raw_condition != json.dumps(
                    condition, separators=(",", ":"), sort_keys=True
                ):
                    errors.append(
                        f"{leg_label} condition {condition_index + 1} must be a canonical "
                        "condition/status/evidence_references JSON string"
                    )
                parsed_conditions.append(condition)
        else:
            errors.append(f"{leg_label} conditions must be a list")

        actual_order = [item.get("condition") for item in parsed_conditions]
        if actual_order != list(condition_order):
            errors.append(f"{leg_label} conditions must use the exact ordered checklist")
        for condition in parsed_conditions:
            name = condition.get("condition")
            status = condition.get("status")
            references = condition.get("evidence_references")
            if status not in {"SATISFIED", "NOT_APPLICABLE"}:
                errors.append(f"{leg_label} condition {name} has invalid status")
            if (
                not isinstance(references, list)
                or not references
                or any(not isinstance(item, str) or not item.strip() for item in references)
            ):
                errors.append(f"{leg_label} condition {name} requires evidence references")
                continue
            if len(set(references)) != len(references):
                errors.append(
                    f"{leg_label} condition {name} requires distinct evidence references"
                )
            for reference in references:
                if not _reverse_evidence_reference_resolves(
                    reference, record, leg, manifest_controls
                ):
                    errors.append(
                        f"{leg_label} condition {name} has unresolved evidence "
                        f"reference {reference}"
                    )
            if status == "NOT_APPLICABLE":
                if len(set(references)) < 2 or not any(
                    isinstance(reference, str)
                    and not reference.startswith("relationship:known_gaps:")
                    for reference in references
                ):
                    errors.append(
                        f"{leg_label} condition {name} NOT_APPLICABLE requires "
                        "distinct evidence references and a separate corroborating reference"
                    )
                elif not _has_evidence_based_na(name, references, leg):
                    errors.append(
                        f"{leg_label} condition {name} NOT_APPLICABLE requires an "
                        "explicit condition-specific known-gap justification and "
                        "corroborating reference"
                    )
            elif status == "SATISFIED" and not _reverse_condition_is_substantiated(
                name, references, external_id, leg
            ):
                errors.append(
                    f"{leg_label} condition {name} requires provision-specific "
                    f"evidence for {name}"
                )
    return errors


def _reverse_supported_outcome_registry_errors(
    profile_entries: object,
) -> list[str]:
    """Require exact pair coverage between semantic and supported-outcome registries."""
    if not isinstance(profile_entries, (list, tuple)):
        return ["observation profile declarations must be an ordered sequence"]
    profile_pairs = {
        (entry[0], entry[1])
        for entry in profile_entries
        if isinstance(entry, (list, tuple))
        and len(entry) == 6
        and isinstance(entry[0], str)
        and isinstance(entry[1], str)
    }
    supported_pairs = set(_UK_CE_PLUS_V32_SUPPORTED_OUTCOME_TEXTS)
    errors = [
        f"missing supported-outcome text for observation profile pair: {pair[0]}/{pair[1]}"
        for pair in sorted(profile_pairs - supported_pairs)
    ]
    errors.extend(
        f"orphan supported-outcome text pair: {pair[0]}/{pair[1]}"
        for pair in sorted(supported_pairs - profile_pairs)
    )
    return errors


def _reverse_evidence_has_population_boundary(evidence_text: str) -> bool:
    """Require selected or sampled evidence to name its bounded population."""
    return bool(
        re.search(r"\bpopulation\b", evidence_text)
        and re.search(
            r"(?i)\b(?:in-scope|scope|applicable|affected|declared|defined|"
            r"enumerated|inventory|universe|total|all)\b",
            evidence_text,
        )
    )


def _reverse_prohibitions_have_required_categories(
    prohibited_inferences: object, external_id: object
) -> bool:
    """Require one provision-bound entry for each canonical assurance category."""
    if not isinstance(external_id, str) or not isinstance(prohibited_inferences, list):
        return False
    if len(prohibited_inferences) != len(_REVERSE_PROHIBITION_CATEGORIES):
        return False
    return all(
        isinstance(entry, str)
        and entry.startswith(f"{external_id} | prohibit {category}: ")
        for category, entry in zip(
            _REVERSE_PROHIBITION_CATEGORIES, prohibited_inferences, strict=True
        )
    )


def _reverse_prohibitions_bind_observation_and_outcome(
    prohibited_inferences: object,
    external_id: object,
    observation: str,
    control_id: object,
) -> bool:
    """Require all nine exact observation- and control-bound prohibition strings."""
    if not _reverse_prohibitions_have_required_categories(
        prohibited_inferences, external_id
    ) or not isinstance(control_id, str):
        return False
    normalized_observation = observation.rstrip(". ").strip()
    if not normalized_observation:
        return False
    expected = [
        f'{external_id} | prohibit {category}: The observed result '
        f'"{normalized_observation}" {_REVERSE_PROHIBITION_DENIALS[category]} '
        f"for the cited {control_id} outcome."
        for category in _REVERSE_PROHIBITION_CATEGORIES
    ]
    return prohibited_inferences == expected


def _reverse_condition_is_substantiated(
    condition: object,
    references: list[object],
    external_id: object,
    leg: dict[str, object],
) -> bool:
    """Require a labeled evidence item that substantively addresses the condition."""
    if not isinstance(condition, str) or not isinstance(external_id, str):
        return False
    expected_evidence = leg.get("expected_evidence")
    if not isinstance(expected_evidence, list):
        return False
    semantic_patterns = {
        "actor": (
            r"\b(?:assessor|actor)\b",
            r"\b(?:responsible|performed|record)\w*\b",
        ),
        "scope": (r"\b(?:in-scope|scope)\b", r"\bAI\b"),
        "population": (
            r"\bpopulation\b",
            r"\b(?:applicable|defined|enumerated|inventory|universe|all)\b",
        ),
        "sample": (
            r"\bsample\b",
            r"\b(?:selected|selection|basis)\b",
            r"\bpopulation\b",
        ),
        "assessment_date": (
            r"\bassessment date\b",
            r"\b(?:date|time|timezone)\b",
        ),
        "evidence_date": (
            r"\bevidence(?:-collection)? date\b",
            r"\b(?:separate|separately)\b",
        ),
        "tool": (r"\b(?:tool|manual)\b", r"\b(?:version|method)\b"),
        "provenance": (
            r"\b(?:provenance|source artifacts?|source locator)\b",
            r"\b(?:cited|manifest|requirement)\b",
        ),
        "exception": (r"\bexception\b", r"\b(?:no|approval|disposition)\b"),
        "delivery_partner_discretion": (
            r"\bdelivery partner\b",
            r"\b(?:discretion|choice|method|approval)\b",
            r"\b(?:basis|affect)\w*\b",
        ),
        "point_in_time_status": (
            r"\b(?:point-in-time|assessment and evidence dates)\b",
            r"\b(?:later state|excluded)\b",
        ),
    }
    patterns = semantic_patterns.get(condition)
    if patterns is None:
        return False
    control_id = leg.get("esaf_control_id")
    allowed_auxiliary_references = {
        "actor": {"record:external_metadata"},
        "scope": {
            "record:context",
            f"manifest:{control_id}#requirement",
        },
        "provenance": {
            "record:source_locator",
            f"manifest:{control_id}#requirement",
        },
    }
    prefix = f"{condition} evidence: {external_id} "
    found_labeled_evidence = False
    for reference in references:
        if not isinstance(reference, str):
            return False
        match = re.fullmatch(r"relationship:expected_evidence:([0-9]+)", reference)
        if match is None:
            if (
                reference.startswith("relationship:known_gaps:")
                and condition == "point_in_time_status"
            ):
                continue
            if reference not in allowed_auxiliary_references.get(condition, set()):
                return False
            continue
        index = int(match.group(1))
        if index >= len(expected_evidence) or not isinstance(expected_evidence[index], str):
            return False
        evidence = expected_evidence[index]
        if not evidence.startswith(prefix) or not all(
            re.search(pattern, evidence, re.IGNORECASE) for pattern in patterns
        ):
            return False
        found_labeled_evidence = True
    return found_labeled_evidence


def _reverse_outcome_is_semantic_placeholder(outcome: str) -> bool:
    """Reject abstract labels that do not identify a concrete ESAF outcome."""
    semantic_scaffolding = {
        "a",
        "an",
        "and",
        "ai",
        "assessed",
        "condition",
        "control",
        "defined",
        "documented",
        "esaf",
        "evidence",
        "exact",
        "for",
        "implementation",
        "in",
        "named",
        "normative",
        "observed",
        "of",
        "on",
        "or",
        "outcome",
        "relevant",
        "requirement",
        "result",
        "safeguard",
        "specific",
        "state",
        "technical",
        "the",
        "to",
        "verified",
    }
    outcome_without_control_ids = re.sub(
        r"\b[a-z]{3}(?:[-_ ./]?\d{3})\b", " ", outcome.lower()
    )
    concrete_terms = {
        token
        for token in re.findall(r"[a-z0-9]+", outcome_without_control_ids)
        if token not in semantic_scaffolding and not token.isdigit()
    }
    return len(concrete_terms) < 2


def _reverse_evidence_reference_resolves(
    reference: str,
    record: dict[str, object],
    leg: dict[str, object],
    manifest_controls: dict[str, dict[str, object]],
) -> bool:
    """Resolve closed reverse-profile evidence references without external I/O."""
    record_fields = {
        "record:context": "context",
        "record:source_locator": "source_locator",
        "record:external_metadata": "external_metadata",
    }
    if reference in record_fields:
        return bool(record.get(record_fields[reference]))
    relationship_fields = {
        "relationship:rationale": "rationale",
        "relationship:expected_evidence": "expected_evidence",
        "relationship:prohibited_inferences": "prohibited_inferences",
    }
    if reference in relationship_fields:
        return bool(leg.get(relationship_fields[reference]))
    expected_evidence = re.fullmatch(
        r"relationship:expected_evidence:([0-9]+)", reference
    )
    if expected_evidence:
        values = leg.get("expected_evidence")
        index = int(expected_evidence.group(1))
        return isinstance(values, list) and index < len(values) and bool(values[index])
    known_gap = re.fullmatch(r"relationship:known_gaps:([0-9]+)", reference)
    if known_gap:
        values = leg.get("known_gaps")
        index = int(known_gap.group(1))
        return isinstance(values, list) and index < len(values) and bool(values[index])
    manifest = re.fullmatch(r"manifest:([A-Z]{3}-[0-9]{3})#requirement", reference)
    if manifest:
        return (
            manifest.group(1) == leg.get("esaf_control_id")
            and manifest.group(1) in manifest_controls
        )
    return False


def _has_evidence_based_na(
    condition: object, references: list[object], leg: dict[str, object]
) -> bool:
    if not isinstance(condition, str) or len(references) < 2:
        return False
    gaps = leg.get("known_gaps")
    if not isinstance(gaps, list):
        return False
    prefix = f"{condition} not applicable because "
    for reference in references:
        if not isinstance(reference, str):
            continue
        match = re.fullmatch(r"relationship:known_gaps:([0-9]+)", reference)
        if not match:
            continue
        index = int(match.group(1))
        if index < len(gaps) and isinstance(gaps[index], str):
            remainder = gaps[index].removeprefix(prefix)
            if gaps[index].startswith(prefix) and len(remainder.strip()) >= 20:
                return True
    return False


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
_CORRUPTION_SIGNATURES = (
    "\u00c3\u0192\u00c2",
    "\u00c3\u00a9",
    "\u00c3\u00a7",
    "\u00c3\u00b1",
    "\u00e2\u20ac\u02dc",
    "\u00e2\u20ac\u00a6",
    "\u00e2\u20ac\u2122",
    "\u00e2\u20ac\u201c",
    "\u00e2\u20ac\u201d",
    "\u00ef\u00bb\u00bf",
    "\ufffd",
)


def _validate_reviewed_text(
    root: Path, path: Path, status: object, relative: str, text: str | None = None
) -> list[str]:
    if text is None:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return []
    errors: list[str] = []
    if any(signature in text for signature in _CORRUPTION_SIGNATURES):
        errors.append(f"{relative}: possible text-encoding corruption")
    if isinstance(status, str) and status in {"reviewed", "approved"} and _DRAFTING_MARKER.search(text):
        errors.append(f"{relative}: unresolved drafting marker")
    for match in _MARKDOWN_LINK.finditer(text):
        raw_target = match.group(1).strip()
        if raw_target.startswith("<") and ">" in raw_target:
            raw_target = raw_target[1 : raw_target.index(">")]
        else:
            raw_target = raw_target.split(maxsplit=1)[0]
        if re.match(r"^[A-Za-z]:[\\/]", raw_target) or raw_target.startswith(("/", "\\")):
            errors.append(f"{relative}: local link escapes repository {raw_target}")
            continue
        try:
            parsed = urlsplit(raw_target)
        except ValueError:
            errors.append(f"{relative}: broken local link {raw_target}")
            continue
        if parsed.scheme or parsed.netloc or raw_target.startswith("#"):
            continue
        target = unquote(parsed.path)
        if target:
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{relative}: local link escapes repository {raw_target}")
                continue
            if not resolved.exists():
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


def _snapshot_paths(mapping_set: dict[str, object]) -> set[str]:
    try:
        authority = mapping_set["authority"]["id"]  # type: ignore[index]
        publication = mapping_set["publication"]["id"]  # type: ignore[index]
        source_version = mapping_set["source_version"]["id"]  # type: ignore[index]
        esaf_release = mapping_set["esaf_release"]["id"]  # type: ignore[index]
        mapping_version = mapping_set["mapping_set_version"]
        base = f"crosswalks/mappings/{authority}"
        suffix = f"{source_version}/{esaf_release}/{mapping_version}"
        return {f"{base}/{suffix}", f"{base}/{publication}/{suffix}"}
    except (KeyError, TypeError):
        return set()


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
