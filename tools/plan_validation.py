"""Fail-closed planning of ESAF validation commands from a Git comparison."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
import sys
from collections.abc import Callable, Sequence


MANIFEST_PATH = Path("tools/validation-plans.json")
SCHEMA = "esaf-validation-plans-v1"
TIERS = ("quick", "standard", "publication")
COMMIT_ID = re.compile(r"^[0-9a-f]{40,64}$")


@dataclass(frozen=True)
class ValidationCommand:
    identifier: str
    argv: tuple[str, ...]
    tier: str
    duration: str


@dataclass(frozen=True)
class ValidationRule:
    identifier: str
    selectors: tuple[tuple[str, str], ...]
    quick: tuple[str, ...]
    standard: tuple[str, ...]
    reason: str
    cross_cutting: bool


@dataclass(frozen=True)
class ValidationManifest:
    commands: tuple[ValidationCommand, ...]
    rules: tuple[ValidationRule, ...]


@dataclass(frozen=True)
class ValidationPlan:
    base: str
    candidate: str
    changed_paths: tuple[str, ...]
    selected_tiers: tuple[str, ...]
    commands: tuple[ValidationCommand, ...]
    reasons: tuple[str, ...]


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build a JSON object while rejecting repeated keys."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"manifest has duplicate key {key!r}")
        result[key] = value
    return result


def _path(value: object, *, selector: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or value.startswith("/"):
        raise ValueError(f"manifest {selector} selector is invalid")
    if selector == "prefix":
        if not value.endswith("/"):
            raise ValueError("manifest prefix selector must end with a slash")
        value = value[:-1]
    parts = value.split("/")
    if any(not part or part in {".", ".."} for part in parts):
        raise ValueError(f"manifest {selector} selector is invalid")
    return value + "/" if selector == "prefix" else value


def _command_ids(value: object, *, field: str, known: set[str]) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"manifest {field} commands must be a list of identifiers")
    if len(value) != len(set(value)):
        raise ValueError(f"manifest {field} commands contain duplicate identifiers")
    unknown = sorted(set(value) - known)
    if unknown:
        raise ValueError("manifest rule refers to unknown command: " + ", ".join(unknown))
    return tuple(value)


def load_manifest(root: Path) -> ValidationManifest:
    """Load and strictly validate the validation routing manifest."""
    try:
        document = json.loads(
            (root / MANIFEST_PATH).read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except json.JSONDecodeError as error:
        raise ValueError("validation plan manifest is not valid JSON") from error
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError("validation plan manifest could not be read") from error
    if not isinstance(document, dict) or set(document) != {"schema", "commands", "rules"}:
        raise ValueError("manifest top-level keys must be schema, commands, and rules")
    if document["schema"] != SCHEMA:
        raise ValueError(f"manifest schema must be {SCHEMA!r}")
    raw_commands = document["commands"]
    if not isinstance(raw_commands, list) or not raw_commands:
        raise ValueError("manifest commands must be a non-empty list")
    commands: list[ValidationCommand] = []
    identifiers: set[str] = set()
    for raw in raw_commands:
        if not isinstance(raw, dict) or set(raw) != {"id", "argv", "tier", "duration"}:
            raise ValueError("manifest command keys must be id, argv, tier, and duration")
        identifier, argv, tier, duration = raw["id"], raw["argv"], raw["tier"], raw["duration"]
        if not isinstance(identifier, str) or not identifier:
            raise ValueError("manifest command id must be a non-empty string")
        if identifier in identifiers:
            raise ValueError(f"manifest has duplicate command id {identifier!r}")
        if not isinstance(argv, list) or not argv or any(not isinstance(item, str) or not item for item in argv):
            raise ValueError(f"manifest command {identifier!r} argv must contain non-empty strings")
        if tier not in TIERS or not isinstance(duration, str) or not duration:
            raise ValueError(f"manifest command {identifier!r} has invalid tier or duration")
        identifiers.add(identifier)
        commands.append(ValidationCommand(identifier, tuple(argv), tier, duration))
    raw_rules = document["rules"]
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ValueError("manifest rules must be a non-empty list")
    rules: list[ValidationRule] = []
    rule_ids: set[str] = set()
    exact_selectors: set[str] = set()
    required = {"id", "selectors", "quick", "standard", "reason", "cross_cutting"}
    for raw in raw_rules:
        if not isinstance(raw, dict) or set(raw) != required:
            raise ValueError("manifest rule has invalid keys")
        identifier = raw["id"]
        if not isinstance(identifier, str) or not identifier:
            raise ValueError("manifest rule id must be a non-empty string")
        if identifier in rule_ids:
            raise ValueError(f"manifest has duplicate rule id {identifier!r}")
        selectors = raw["selectors"]
        if not isinstance(selectors, list) or not selectors:
            raise ValueError(f"manifest rule {identifier!r} selectors must be non-empty")
        parsed: list[tuple[str, str]] = []
        for raw_selector in selectors:
            if not isinstance(raw_selector, dict) or len(raw_selector) != 1:
                raise ValueError(f"manifest rule {identifier!r} selector is invalid")
            kind, value = next(iter(raw_selector.items()))
            if kind not in {"exact", "prefix"}:
                raise ValueError(f"manifest rule {identifier!r} selector is invalid")
            path = _path(value, selector=kind)
            if kind == "exact":
                if path in exact_selectors:
                    raise ValueError(f"manifest has ambiguous exact selector {path!r}")
                exact_selectors.add(path)
            parsed.append((kind, path))
        quick = _command_ids(raw["quick"], field="quick", known=identifiers)
        standard = _command_ids(raw["standard"], field="standard", known=identifiers)
        if not isinstance(raw["reason"], str) or not raw["reason"] or not isinstance(raw["cross_cutting"], bool):
            raise ValueError(f"manifest rule {identifier!r} reason or cross_cutting is invalid")
        rule_ids.add(identifier)
        rules.append(ValidationRule(identifier, tuple(parsed), quick, standard, raw["reason"], raw["cross_cutting"]))
    return ValidationManifest(tuple(commands), tuple(rules))


def _resolve(root: Path, ref: str, runner: Callable[..., object]) -> str:
    result = runner(["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], cwd=root, check=False, capture_output=True)
    output = getattr(result, "stdout", None)
    if getattr(result, "returncode", None) != 0 or not isinstance(output, bytes):
        raise ValueError(f"could not resolve Git reference {ref!r}")
    try:
        resolved = output.decode("ascii", errors="strict").strip()
    except UnicodeDecodeError as error:
        raise ValueError(f"could not resolve Git reference {ref!r}") from error
    if not COMMIT_ID.fullmatch(resolved):
        raise ValueError(f"could not resolve Git reference {ref!r}")
    return resolved


def _diff_paths(root: Path, base: str, candidate: str, runner: Callable[..., object]) -> tuple[tuple[str, str], ...]:
    result = runner(["git", "diff", "--name-status", "-z", base, candidate], cwd=root, check=False, capture_output=True)
    output = getattr(result, "stdout", None)
    if getattr(result, "returncode", None) != 0 or not isinstance(output, bytes):
        raise ValueError("could not produce Git name-status diff")
    try:
        fields = output.decode("utf-8", errors="strict").split("\0")
    except UnicodeDecodeError as error:
        raise ValueError("Git name-status diff is not valid UTF-8") from error
    if not fields or fields[-1] != "":
        raise ValueError("Git name-status diff is malformed")
    fields.pop()
    if not fields:
        raise ValueError("Git name-status diff contains no paths")
    changes: list[tuple[str, str]] = []
    position = 0
    while position < len(fields):
        status = fields[position]
        position += 1
        if status in {"A", "M", "D"}:
            if position >= len(fields) or not fields[position]:
                raise ValueError("Git name-status diff is malformed")
            changes.append((status, fields[position]))
            position += 1
        elif re.fullmatch(r"R\d{1,3}", status):
            if position + 1 >= len(fields) or not fields[position] or not fields[position + 1]:
                raise ValueError("Git name-status diff is malformed")
            changes.append(("R", fields[position + 1]))
            position += 2
        else:
            raise ValueError("Git name-status diff is malformed")
    return tuple(changes)


def _matches(rule: ValidationRule, path: str) -> bool:
    return any((kind == "exact" and path == selector) or (kind == "prefix" and path.startswith(selector)) for kind, selector in rule.selectors)


def plan_validation(root: Path, *, base: str, candidate: str, git_runner: Callable[..., object] | None = None) -> ValidationPlan:
    """Return the conservative validation plan for the resolved Git comparison."""
    manifest = load_manifest(root)
    runner = git_runner if git_runner is not None else subprocess.run
    resolved_base = _resolve(root, base, runner)
    resolved_candidate = _resolve(root, candidate, runner)
    changes = _diff_paths(root, resolved_base, resolved_candidate, runner)
    changed_paths = tuple(path for _, path in changes)
    escalation: list[str] = []
    command_ids: list[str] = []
    reasons: list[str] = []
    for status, path in changes:
        if status == "D":
            escalation.append(f"deleted path: {path}")
            continue
        if status == "R":
            escalation.append(f"renamed path: {path}")
            continue
        matched = [rule for rule in manifest.rules if _matches(rule, path)]
        if not matched:
            escalation.append(f"unclassified path: {path}")
            continue
        if any(rule.cross_cutting for rule in matched):
            escalation.extend(rule.reason for rule in matched if rule.cross_cutting)
            continue
        for rule in matched:
            reasons.append(rule.reason)
            command_ids.extend(rule.quick)
            command_ids.extend(rule.standard)
    catalog = {command.identifier: command for command in manifest.commands}
    if escalation:
        commands = tuple(command for command in manifest.commands if command.tier == "publication")
        return ValidationPlan(resolved_base, resolved_candidate, changed_paths, ("publication",), commands, tuple(dict.fromkeys(escalation)))
    selected = set(command_ids)
    commands = tuple(command for command in manifest.commands if command.identifier in selected)
    tiers = tuple(tier for tier in TIERS if any(command.tier == tier for command in commands))
    if not commands:
        raise ValueError("manifest rules selected no validation commands")
    return ValidationPlan(resolved_base, resolved_candidate, changed_paths, tiers, commands, tuple(dict.fromkeys(reasons)))


def render_text(plan: ValidationPlan) -> str:
    lines = [f"Base: {plan.base}", f"Candidate: {plan.candidate}", "Selected tiers: " + ", ".join(plan.selected_tiers), "Changed paths:"]
    lines.extend(f"- {path}" for path in plan.changed_paths)
    lines.append("Reasons:")
    lines.extend(f"- {reason}" for reason in plan.reasons)
    lines.append("Commands:")
    lines.extend(f"- {command.identifier} [{command.tier}; {command.duration}]: {' '.join(command.argv)}" for command in plan.commands)
    return "\n".join(lines) + "\n"


def render_json(plan: ValidationPlan) -> str:
    value = {"base": plan.base, "candidate": plan.candidate, "changed_paths": list(plan.changed_paths), "selected_tiers": list(plan.selected_tiers), "commands": [{"id": command.identifier, "argv": list(command.argv), "tier": command.tier, "duration": command.duration} for command in plan.commands], "reasons": list(plan.reasons)}
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main(argv: Sequence[str] | None = None, *, root: Path | None = None, git_runner: Callable[..., object] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--tier", choices=TIERS)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    arguments = parser.parse_args(argv)
    try:
        plan = plan_validation(root or Path.cwd(), base=arguments.base, candidate=arguments.candidate, git_runner=git_runner)
        if arguments.tier:
            commands = tuple(command for command in plan.commands if command.tier == arguments.tier)
            plan = ValidationPlan(plan.base, plan.candidate, plan.changed_paths, (arguments.tier,) if commands else (), commands, plan.reasons)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(render_json(plan) if arguments.format == "json" else render_text(plan), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
