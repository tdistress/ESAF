#!/usr/bin/env python3
"""Validate the structural contract for the ESAF-1200 foundation."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "architectures/README.md",
    "architectures/ESAF-1200.md",
    "architectures/ARCHITECTURE_TEMPLATE.md",
    "architectures/PRINCIPLES.md",
    "architectures/TRUST_ZONES.md",
    "architectures/PATTERN_SELECTION.md",
    "architectures/overlays/README.md",
    "architectures/patterns/README.md",
    "architectures/decisions/README.md",
    "architectures/decisions/ADR_TEMPLATE.md",
)
RESERVED_PATTERNS = (
    "ARC-P100",
    "ARC-P110",
    "ARC-P120",
    "ARC-P130",
    "ARC-P140",
    "ARC-P150",
    "ARC-P160",
)
REQUIRED_TEMPLATE_HEADINGS = (
    "Metadata",
    "Purpose",
    "Problem statement",
    "Intended outcomes",
    "Non-goals",
    "Applicability",
    "Assumptions and prerequisites",
    "Prohibited uses",
    "Architecture views",
    "Actors and identities",
    "Data and instruction flows",
    "Trust boundaries",
    "Components and responsibilities",
    "Required controls",
    "Control points and overlays",
    "Architecture decisions and parameters",
    "Failure modes and abuse cases",
    "Fallback recovery and retirement",
    "Evidence and assessment",
    "Variants and alternatives",
    "Anti-patterns",
    "Related patterns",
    "Change history",
)
PATTERN_STATES = {"proposed", "draft", "approved", "published", "deprecated", "retired"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CONTROL_FAMILY = re.compile(r"`([A-Z]{3})`")
PATTERN_ROW = re.compile(
    r"^\|\s*(?:\[)?(ARC-P[1-9][0-9]{2})(?:\]\([^)]+\))?\s*\|.*?\|\s*([A-Za-z]+)\s*\|\s*$",
    re.MULTILINE,
)
PATTERN_METADATA = {
    "Pattern ID": re.compile(r"^\*\*Pattern ID:\*\*\s*(ARC-P[1-9][0-9]{2})\s*$", re.MULTILINE),
    "Status": re.compile(r"^\*\*Status:\*\*\s*([A-Za-z]+)\s*$", re.MULTILINE),
    "Version": re.compile(r"^\*\*Version:\*\*\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.MULTILINE),
}
CONTROL_ID = re.compile(r"`([A-Z]{3}-[1-9][0-9]{2})`")
PLACEHOLDER = re.compile(r"\b(?:TBD|TODO|FIXME)\b", re.IGNORECASE)


def architecture_markdown(root: Path) -> list[Path]:
    directory = root / "architectures"
    return sorted(directory.rglob("*.md")) if directory.exists() else []


def valid_control_families(root: Path) -> set[str]:
    schema_path = root / "controls/schema/control.schema.json"
    if not schema_path.exists():
        return set()
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        return set(schema["properties"]["family"]["enum"])
    except (OSError, ValueError, KeyError, TypeError):
        return set()


def validate_links(root: Path, path: Path, text: str) -> list[str]:
    errors: list[str] = []
    relative = path.relative_to(root).as_posix()
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        file_target = unquote(target.split("#", 1)[0])
        if file_target and not (path.parent / file_target).resolve().exists():
            errors.append(f"{relative}: broken local link '{target}'")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"{relative}: required foundation file is missing")

    template_path = root / "architectures/ARCHITECTURE_TEMPLATE.md"
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
        for heading in REQUIRED_TEMPLATE_HEADINGS:
            if not re.search(rf"^## {re.escape(heading)}\s*$", template, re.MULTILINE):
                errors.append(f"architectures/ARCHITECTURE_TEMPLATE.md: missing heading '## {heading}'")

    registry_path = root / "architectures/patterns/README.md"
    if registry_path.exists():
        registry = registry_path.read_text(encoding="utf-8")
        rows = PATTERN_ROW.findall(registry)
        row_ids = [identifier for identifier, _state in rows]
        for identifier in RESERVED_PATTERNS:
            count = row_ids.count(identifier)
            if count != 1:
                errors.append(f"architectures/patterns/README.md: {identifier} occurs {count} times; expected 1")
        for identifier in sorted(set(row_ids) - set(RESERVED_PATTERNS)):
            errors.append(f"architectures/patterns/README.md: unreserved pattern identifier {identifier}")
        for identifier, state in rows:
            if state.lower() not in PATTERN_STATES:
                errors.append(f"architectures/patterns/README.md: {identifier} has invalid state {state!r}")

        for pattern_path in sorted((root / "architectures/patterns").glob("ARC-P[1-9][0-9][0-9].md")):
            relative = pattern_path.relative_to(root).as_posix()
            text = pattern_path.read_text(encoding="utf-8")
            filename_id = pattern_path.stem
            metadata: dict[str, str] = {}
            for field, expression in PATTERN_METADATA.items():
                match = expression.search(text)
                if not match:
                    errors.append(f"{relative}: missing or invalid {field} metadata")
                else:
                    metadata[field] = match.group(1)
            pattern_id = metadata.get("Pattern ID")
            if pattern_id and pattern_id != filename_id:
                errors.append(f"{relative}: Pattern ID {pattern_id} does not match filename {filename_id}")
            status = metadata.get("Status", "").lower()
            if status and status not in PATTERN_STATES:
                errors.append(f"{relative}: invalid pattern status {metadata['Status']!r}")
            for heading in REQUIRED_TEMPLATE_HEADINGS:
                if not re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE):
                    errors.append(f"{relative}: missing heading '## {heading}'")
            for control_id in sorted(set(CONTROL_ID.findall(text))):
                family = control_id.split("-", 1)[0]
                if not (root / "controls" / family / f"{control_id}.md").is_file():
                    errors.append(f"{relative}: unresolved control reference {control_id}")
            if f"[{filename_id}]({filename_id}.md)" not in registry:
                errors.append(f"architectures/patterns/README.md: {filename_id} record is not linked as '{filename_id}.md'")
            registry_state = next((state for identifier, state in rows if identifier == filename_id), "")
            if status and registry_state and status != registry_state.lower():
                errors.append(
                    f"architectures/patterns/README.md: {filename_id} registry state {registry_state!r} "
                    f"does not match record status {metadata['Status']!r}"
                )

    families = valid_control_families(root)
    for path in architecture_markdown(root):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        errors.extend(validate_links(root, path, text))
        if PLACEHOLDER.search(text):
            errors.append(f"{relative}: unresolved placeholder marker")
        if "�" in text or "â€" in text or "â†" in text:
            errors.append(f"{relative}: possible text-encoding corruption")
        for family in CONTROL_FAMILY.findall(text):
            if families and family not in families:
                errors.append(f"{relative}: unknown ESAF control family {family}")
    return sorted(set(errors))


def main() -> int:
    errors = validate(ROOT)
    if errors:
        print(f"Architecture validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Successfully validated {len(REQUIRED_FILES)} foundation files and {len(RESERVED_PATTERNS)} reserved patterns.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
