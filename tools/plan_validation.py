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


TIERS = ("quick", "standard", "publication")
COMMIT_ID = re.compile(r"^[0-9a-f]{40,64}$")
COMMAND_PLACEHOLDERS = {"{base}", "{candidate}"}


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
class ValidationPolicy:
    """Reviewed in-memory command catalog and routing rules."""

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
    if not isinstance(value, tuple) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"policy {field} commands must be a tuple of identifiers")
    if len(value) != len(set(value)):
        raise ValueError(f"policy {field} commands contain duplicate identifiers")
    unknown = sorted(set(value) - known)
    if unknown:
        raise ValueError("policy rule refers to unknown command: " + ", ".join(unknown))
    return tuple(value)


def validate_policy(policy: ValidationPolicy) -> ValidationManifest:
    """Validate reviewed policy records before they drive command selection."""
    if not isinstance(policy, ValidationPolicy):
        raise ValueError("validation policy is invalid")
    raw_commands = policy.commands
    if not isinstance(raw_commands, tuple) or not raw_commands:
        raise ValueError("policy commands must be a non-empty tuple")
    commands: list[ValidationCommand] = []
    identifiers: set[str] = set()
    for raw in raw_commands:
        if not isinstance(raw, ValidationCommand):
            raise ValueError("policy command record is invalid")
        identifier, argv, tier, duration = raw.identifier, raw.argv, raw.tier, raw.duration
        if not isinstance(identifier, str) or not identifier:
            raise ValueError("policy command id must be a non-empty string")
        if identifier in identifiers:
            raise ValueError(f"policy has duplicate command id {identifier!r}")
        if not isinstance(argv, tuple) or not argv or any(
            not isinstance(item, str) or not item for item in argv
        ):
            raise ValueError(f"policy command {identifier!r} argv must contain non-empty strings")
        if any(item.startswith("{") or item.endswith("}") for item in argv if item not in COMMAND_PLACEHOLDERS):
            raise ValueError(f"policy command {identifier!r} has an invalid argv placeholder")
        if tier not in TIERS or not isinstance(duration, str) or not duration:
            raise ValueError(f"policy command {identifier!r} has invalid tier or duration")
        identifiers.add(identifier)
        commands.append(raw)
    raw_rules = policy.rules
    if not isinstance(raw_rules, tuple) or not raw_rules:
        raise ValueError("policy rules must be a non-empty tuple")
    rules: list[ValidationRule] = []
    rule_ids: set[str] = set()
    exact_selectors: set[str] = set()
    for raw in raw_rules:
        if not isinstance(raw, ValidationRule):
            raise ValueError("policy rule record is invalid")
        identifier = raw.identifier
        if not isinstance(identifier, str) or not identifier:
            raise ValueError("policy rule id must be a non-empty string")
        if identifier in rule_ids:
            raise ValueError(f"policy has duplicate rule id {identifier!r}")
        selectors = raw.selectors
        if not isinstance(selectors, tuple) or not selectors:
            raise ValueError(f"policy rule {identifier!r} selectors must be non-empty")
        parsed: list[tuple[str, str]] = []
        for raw_selector in selectors:
            if not isinstance(raw_selector, tuple) or len(raw_selector) != 2:
                raise ValueError(f"policy rule {identifier!r} selector is invalid")
            kind, value = raw_selector
            if kind not in {"exact", "prefix"}:
                raise ValueError(f"policy rule {identifier!r} selector is invalid")
            path = _path(value, selector=kind)
            if kind == "exact":
                if path in exact_selectors:
                    raise ValueError(f"policy has ambiguous exact selector {path!r}")
                exact_selectors.add(path)
            parsed.append((kind, path))
        quick = _command_ids(raw.quick, field="quick", known=identifiers)
        standard = _command_ids(raw.standard, field="standard", known=identifiers)
        if not isinstance(raw.reason, str) or not raw.reason or not isinstance(raw.cross_cutting, bool):
            raise ValueError(f"policy rule {identifier!r} reason or cross_cutting is invalid")
        rule_ids.add(identifier)
        rules.append(ValidationRule(identifier, tuple(parsed), quick, standard, raw.reason, raw.cross_cutting))
    return ValidationManifest(tuple(commands), tuple(rules))


COMMAND_CATALOG = (
    ValidationCommand("preflight", ("git", "diff", "--check", "{base}", "{candidate}"), "quick", "under a minute"),
    ValidationCommand("test-shard-manifest", ("python", "tools/validate_test_shards.py", "--check"), "quick", "under a minute"),
    ValidationCommand("profile-shard", ("python", "tools/run_test_shards.py", "--shard", "profile_validation"), "standard", "under a minute"),
    ValidationCommand("qualified-review-shard", ("python", "tools/run_test_shards.py", "--shard", "qualified_review_evidence"), "standard", "about 5 to 10 minutes"),
    ValidationCommand("mapping-review-shard", ("python", "tools/run_test_shards.py", "--shard", "mapping_review_bundle"), "standard", "about 3 minutes"),
    ValidationCommand("remaining-shard", ("python", "tools/run_test_shards.py", "--shard", "remaining"), "standard", "about 3 minutes"),
    ValidationCommand("architectures", ("python", "tools/validate_architectures.py"), "standard", "about a minute"),
    ValidationCommand("assessment", ("python", "tools/validate_assessment.py", "--check"), "standard", "about a minute"),
    ValidationCommand("controls", ("python", "tools/validate_controls.py", "--check"), "standard", "about a minute"),
    ValidationCommand("crosswalks", ("python", "tools/validate_crosswalks.py", "--check", "--baseline-ref", "{base}"), "standard", "about a minute"),
    ValidationCommand("profiles", ("python", "tools/validate_profiles.py", "--check"), "standard", "about a minute"),
    ValidationCommand("full-discovery", ("python", "-B", "-m", "unittest", "discover", "-s", "tests", "-v"), "publication", "candidate freeze"),
    ValidationCommand("mermaid-record", ("python", "tools/mermaid_inventory.py", "--check-record", "docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md"), "publication", "candidate freeze"),
    ValidationCommand("links", ("python", "tools/validate_links.py", "--check"), "standard", "about a minute"),
    ValidationCommand("qualified-review-equivalence", ("python", "tools/verify_qualified_review_hot_path_equivalence.py", "--check", "--candidate-sha", "{candidate}"), "publication", "publication proof"),
    ValidationCommand("release-gates", ("python", "tools/release_gates.py", "--check", "--baseline-ref", "{base}"), "publication", "candidate freeze"),
    ValidationCommand("release-evidence", ("python", "tools/v05_beta_release_gates.py", "--check", "--baseline-ref", "{base}"), "publication", "candidate freeze"),
    ValidationCommand("pci-dss-mapping-go-no-go", ("python", "tools/render_pci_dss_mapping_go_no_go.py", "--check"), "publication", "candidate freeze"),
    ValidationCommand("nist-ai-rmf-mapping-go-no-go", ("python", "tools/render_nist_ai_rmf_mapping_go_no_go.py", "--check"), "publication", "candidate freeze"),
    ValidationCommand("v09-rc1-release-gates", ("python", "tools/v09_rc1_release_gates.py", "--check"), "publication", "candidate freeze"),
)

ROUTING_RULES = (
    ValidationRule("documentation", (("prefix", "docs/"),), ("preflight", "test-shard-manifest"), ("remaining-shard", "links"), "documentation change", False),
    ValidationRule("architectures", (("prefix", "architectures/"),), ("preflight", "test-shard-manifest"), ("architectures", "remaining-shard"), "architecture change", False),
    ValidationRule("assessment", (("prefix", "assessment/"),), ("preflight", "test-shard-manifest"), ("assessment", "remaining-shard"), "assessment change", False),
    ValidationRule("controls", (("prefix", "controls/"),), ("preflight", "test-shard-manifest"), ("controls", "remaining-shard"), "controls change", False),
    ValidationRule("crosswalks", (("prefix", "crosswalks/"),), ("preflight", "test-shard-manifest"), ("crosswalks", "mapping-review-shard"), "crosswalk change", False),
    ValidationRule("profiles", (("prefix", "profiles/"),), ("preflight", "test-shard-manifest"), ("profiles", "profile-shard"), "profile change", False),
    ValidationRule("qualified-review", (("prefix", "crosswalks/qualified-review/"),), ("preflight", "test-shard-manifest"), ("qualified-review-shard",), "qualified-review change", False),
    ValidationRule("mapping-review", (("prefix", "crosswalks/mapping-review/"),), ("preflight", "test-shard-manifest"), ("mapping-review-shard",), "mapping-review change", False),
    ValidationRule("workflow", (("prefix", ".github/workflows/"), ("exact", "AGENTS.md")), ("preflight",), (), "workflow change", True),
    ValidationRule("publication-evidence", (("prefix", "docs/superpowers/reviews/"), ("exact", "VERSION.md")), ("preflight",), (), "publication evidence or release metadata change", True),
    ValidationRule("release-metadata", (("exact", "README.md"), ("exact", "CHANGELOG.md"), ("exact", "ROADMAP.md"), ("exact", "project/BACKLOG.md"), ("exact", "project/MILESTONES.md"), ("exact", "project/RELEASE_PLAN.md")), ("preflight",), (), "release metadata change", True),
    ValidationRule("validation-tools", (("prefix", "tools/"), ("prefix", "tests/")), ("preflight",), (), "validation-tool change", True),
)

PUBLICATION_COMMAND_IDS = (
    "preflight", "test-shard-manifest", "profile-shard", "qualified-review-shard",
    "mapping-review-shard", "remaining-shard", "architectures", "assessment", "controls",
    "crosswalks", "profiles", "full-discovery", "mermaid-record", "links",
    "qualified-review-equivalence", "release-gates", "release-evidence",
    "pci-dss-mapping-go-no-go", "nist-ai-rmf-mapping-go-no-go",
    "v09-rc1-release-gates",
)
PROOF_COMMAND_IDS = ("qualified-review-equivalence",)
REVIEWED_POLICY = ValidationPolicy(COMMAND_CATALOG, ROUTING_RULES)


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


def _require_checked_out_candidate(
    root: Path, candidate: str, runner: Callable[..., object]
) -> None:
    """Require the requested candidate to be the clean checked-out commit."""
    head = _resolve(root, "HEAD", runner)
    if head != candidate:
        raise ValueError("resolved candidate does not match checkout HEAD")
    result = runner(
        ["git", "status", "--porcelain=v1", "--untracked-files=no"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    output = getattr(result, "stdout", None)
    if getattr(result, "returncode", None) != 0 or not isinstance(output, bytes):
        raise ValueError("could not inspect tracked checkout changes")
    if output:
        raise ValueError("checkout contains tracked changes")


def _require_no_untracked_files(root: Path, runner: Callable[..., object]) -> None:
    """Require a proof-bearing publication plan to start from an empty checkout."""
    result = runner(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    output = getattr(result, "stdout", None)
    if getattr(result, "returncode", None) != 0 or not isinstance(output, bytes):
        raise ValueError("could not inspect checkout untracked files")
    if output:
        raise ValueError("checkout contains untracked files for publication proof")


def _require_base_ancestor(
    root: Path, base: str, candidate: str, runner: Callable[..., object]
) -> None:
    """Require the validation comparison to advance from its declared base."""
    result = runner(
        ["git", "merge-base", "--is-ancestor", base, candidate],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if getattr(result, "returncode", None) != 0:
        raise ValueError("resolved base is not an ancestor of resolved candidate")


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


def _bind_commands(
    commands: tuple[ValidationCommand, ...], *, base: str, candidate: str
) -> tuple[ValidationCommand, ...]:
    """Bind the only supported comparison placeholders in fixed catalog argv."""
    bindings = {"{base}": base, "{candidate}": candidate}
    return tuple(
        ValidationCommand(
            command.identifier,
            tuple(bindings.get(argument, argument) for argument in command.argv),
            command.tier,
            command.duration,
        )
        for command in commands
    )


def _publication_commands(manifest: ValidationManifest) -> tuple[ValidationCommand, ...]:
    commands = {command.identifier: command for command in manifest.commands}
    try:
        return tuple(commands[identifier] for identifier in PUBLICATION_COMMAND_IDS)
    except KeyError as error:
        raise ValueError(f"policy publication command is missing: {error.args[0]}") from error


def plan_validation(root: Path, *, base: str, candidate: str, git_runner: Callable[..., object] | None = None) -> ValidationPlan:
    """Return the conservative validation plan for the resolved Git comparison."""
    manifest = validate_policy(REVIEWED_POLICY)
    runner = git_runner if git_runner is not None else subprocess.run
    resolved_base = _resolve(root, base, runner)
    resolved_candidate = _resolve(root, candidate, runner)
    _require_checked_out_candidate(root, resolved_candidate, runner)
    _require_base_ancestor(root, resolved_base, resolved_candidate, runner)
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
    if escalation:
        commands = _bind_commands(
            _publication_commands(manifest), base=resolved_base, candidate=resolved_candidate
        )
        tiers = ("publication",)
        selected_reasons = tuple(dict.fromkeys(escalation))
    else:
        selected = set(command_ids)
        commands = _bind_commands(
            tuple(command for command in manifest.commands if command.identifier in selected),
            base=resolved_base,
            candidate=resolved_candidate,
        )
        tiers = tuple(tier for tier in TIERS if any(command.tier == tier for command in commands))
        if not commands:
            raise ValueError("manifest rules selected no validation commands")
        selected_reasons = tuple(dict.fromkeys(reasons))
    if set(PROOF_COMMAND_IDS).intersection(command.identifier for command in commands):
        _require_no_untracked_files(root, runner)
    return ValidationPlan(resolved_base, resolved_candidate, changed_paths, tiers, commands, selected_reasons)


def render_text(plan: ValidationPlan) -> str:
    quote = json.dumps
    lines = [
        f"Base: {quote(plan.base)}",
        f"Candidate: {quote(plan.candidate)}",
        "Selected tiers: " + ", ".join(quote(tier) for tier in plan.selected_tiers),
        "Changed paths:",
    ]
    lines.extend(f"- {quote(path)}" for path in plan.changed_paths)
    lines.append("Reasons:")
    lines.extend(f"- {quote(reason)}" for reason in plan.reasons)
    lines.append("Commands:")
    lines.extend(
        f"- {quote(command.identifier)} [{quote(command.tier)}; {quote(command.duration)}]: "
        + " ".join(quote(argument) for argument in command.argv)
        for command in plan.commands
    )
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
            if plan.selected_tiers == ("publication",) and arguments.tier != "publication":
                raise ValueError("publication validation route cannot be down-tiered")
            if arguments.tier == "publication":
                manifest = validate_policy(REVIEWED_POLICY)
                commands = _bind_commands(
                    _publication_commands(manifest), base=plan.base, candidate=plan.candidate
                )
                if plan.selected_tiers != ("publication",):
                    _require_no_untracked_files(root or Path.cwd(), git_runner or subprocess.run)
            else:
                commands = tuple(command for command in plan.commands if command.tier == arguments.tier)
            plan = ValidationPlan(
                plan.base,
                plan.candidate,
                plan.changed_paths,
                (arguments.tier,) if commands else (),
                commands,
                plan.reasons,
            )
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(render_json(plan) if arguments.format == "json" else render_text(plan), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
