#!/usr/bin/env python3
"""Validate repository-local links in every Git-tracked Markdown file."""

from __future__ import annotations

import argparse
from collections import defaultdict
import html
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
REFERENCE_DEFINITION_RE = re.compile(r"^\s{0,3}\[(?P<label>[^\]]+)\]:\s*")
REFERENCE_USAGE_RE = re.compile(r"\[([^\]\n]+)\]\[([^\]\n]*)\]")
EXPLICIT_ID_RE = re.compile(r"\b(?:id|name)=[\"']([^\"']+)[\"']", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]*>")
PUNCTUATION_RE = re.compile(r"[^\w\- ]", re.UNICODE)
ESCAPABLE_RE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")


def git_output(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def repository_root() -> Path:
    return Path(git_output(Path.cwd(), "rev-parse", "--show-toplevel").strip()).resolve()


def tracked_markdown(root: Path) -> list[Path]:
    names = git_output(root, "ls-files", "--", "*.md").splitlines()
    return [root / name for name in sorted(names)]


def visible_markdown_lines(text: str):
    fenced = False
    fence_marker = ""
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        marker_match = re.match(r"(`{3,}|~{3,})", stripped)
        if marker_match:
            marker = marker_match.group(1)
            if not fenced:
                fenced = True
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                fenced = False
                fence_marker = ""
            yield number, ""
            continue
        if fenced:
            yield number, ""
            continue
        yield number, line


def replace_code_spans(line: str, preserve_content: bool) -> str:
    output: list[str] = []
    position = 0
    while position < len(line):
        if line[position] != "`":
            output.append(line[position])
            position += 1
            continue
        run_end = position
        while run_end < len(line) and line[run_end] == "`":
            run_end += 1
        marker = line[position:run_end]
        closing = line.find(marker, run_end)
        if closing < 0:
            output.append(marker)
            position = run_end
            continue
        content = line[run_end:closing]
        if preserve_content:
            normalized = re.sub(r"\s", " ", content)
            if normalized.startswith(" ") and normalized.endswith(" ") and normalized.strip():
                normalized = normalized[1:-1]
            output.append(normalized)
        else:
            output.append(" " * (closing + len(marker) - position))
        position = closing + len(marker)
    return "".join(output)


def parse_destination(line: str, start: int, closing_parenthesis: bool) -> tuple[str, int] | None:
    position = start
    while position < len(line) and line[position] in " \t":
        position += 1
    if position >= len(line):
        return None
    if line[position] == "<":
        end = position + 1
        while end < len(line):
            if line[end] == "\\":
                end += 2
                continue
            if line[end] == ">":
                return line[position + 1 : end], end + 1
            end += 1
        return None
    destination_start = position
    depth = 0
    while position < len(line):
        character = line[position]
        if character == "\\":
            position += 2
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            if depth == 0:
                if closing_parenthesis:
                    return line[destination_start:position], position + 1
                break
            depth -= 1
        elif character in " \t" and depth == 0:
            break
        position += 1
    if depth != 0 or position == destination_start:
        return None
    return line[destination_start:position], position


def inline_destinations(line: str):
    masked = replace_code_spans(line, preserve_content=False)
    position = 0
    while position < len(masked):
        opening = masked.find("[", position)
        if opening < 0:
            return
        closing = opening + 1
        bracket_depth = 0
        while closing < len(masked):
            if masked[closing] == "\\":
                closing += 2
                continue
            if masked[closing] == "[":
                bracket_depth += 1
            elif masked[closing] == "]":
                if bracket_depth == 0:
                    break
                bracket_depth -= 1
            closing += 1
        if closing >= len(masked) or closing + 1 >= len(masked) or masked[closing + 1] != "(":
            position = opening + 1
            continue
        parsed = parse_destination(line, closing + 2, closing_parenthesis=True)
        if parsed is None:
            position = closing + 2
            continue
        target, end = parsed
        yield target
        position = end


def normalize_reference_label(label: str) -> str:
    unescaped = ESCAPABLE_RE.sub(r"\1", html.unescape(label))
    return re.sub(r"\s+", " ", unescaped.strip()).casefold()


def reference_definition(line: str) -> tuple[str, str] | None:
    match = REFERENCE_DEFINITION_RE.match(line)
    if match is None:
        return None
    parsed = parse_destination(line, match.end(), closing_parenthesis=False)
    return (match.group("label"), parsed[0]) if parsed else None


def reference_usages(line: str):
    masked = replace_code_spans(line, preserve_content=False)
    for match in REFERENCE_USAGE_RE.finditer(masked):
        first = line[match.start(1) : match.end(1)]
        second = line[match.start(2) : match.end(2)]
        yield second or first


def github_slug(heading: str) -> str:
    value = html.unescape(heading).lower()
    value = TAG_RE.sub("", value)
    value = re.sub(r"[\[\]_*~]", "", value)
    value = PUNCTUATION_RE.sub("", value)
    return re.sub(r"\s", "-", value.strip())


def anchors(path: Path) -> set[str]:
    found: set[str] = set()
    counts: defaultdict[str, int] = defaultdict(int)
    text = path.read_text(encoding="utf-8")
    for _, line in visible_markdown_lines(text):
        heading = HEADING_RE.match(replace_code_spans(line, preserve_content=True))
        if heading:
            base = github_slug(heading.group(1))
            count = counts[base]
            found.add(base if count == 0 else f"{base}-{count}")
            counts[base] += 1
        found.update(unquote(value) for value in EXPLICIT_ID_RE.findall(line))
    return found


def local_parts(target: str):
    target = ESCAPABLE_RE.sub(r"\1", target)
    if target.startswith("//"):
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    return unquote(parsed.path), unquote(parsed.fragment)


def resolved_target(root: Path, source: Path, target_path: str) -> tuple[Path | None, str | None]:
    if not target_path:
        candidate = source
    elif target_path.startswith("/"):
        candidate = root / target_path.lstrip("/")
    else:
        candidate = source.parent / target_path
    candidate = candidate.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, "target escapes repository"
    if candidate.is_dir():
        candidate = candidate / "README.md"
    if not candidate.is_file():
        return None, "target does not exist"
    return candidate, None


def validate(root: Path) -> tuple[list[str], int]:
    files = tracked_markdown(root)
    diagnostics: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    for source in files:
        relative_source = source.relative_to(root).as_posix()
        text = source.read_text(encoding="utf-8")
        lines = list(visible_markdown_lines(text))
        definitions: set[str] = set()
        for _, line in lines:
            definition = reference_definition(line)
            if definition is not None:
                definitions.add(normalize_reference_label(definition[0]))
        for line_number, line in lines:
            targets = list(inline_destinations(line))
            definition = reference_definition(line)
            if definition is not None:
                targets.insert(0, definition[1])
            for target in targets:
                parts = local_parts(target)
                if parts is None:
                    continue
                target_path, fragment = parts
                destination, error = resolved_target(root, source, target_path)
                if error:
                    diagnostics.append(f"{relative_source}:{line_number}: {target}: {error}")
                    continue
                if fragment:
                    assert destination is not None
                    if destination.suffix.lower() != ".md":
                        diagnostics.append(
                            f"{relative_source}:{line_number}: {target}: "
                            "cannot validate anchor on non-Markdown target"
                        )
                        continue
                    available = anchor_cache.setdefault(destination, anchors(destination))
                    if fragment not in available:
                        diagnostics.append(
                            f"{relative_source}:{line_number}: {target}: anchor does not exist"
                        )
            for label in reference_usages(line):
                if normalize_reference_label(label) not in definitions:
                    diagnostics.append(
                        f"{relative_source}:{line_number}: [{label}]: "
                        "reference definition does not exist"
                    )
    return diagnostics, len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without modifying files")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        root = repository_root()
        diagnostics, file_count = validate(root)
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        print(f"link validation failed: {exc}")
        return 2
    for diagnostic in diagnostics:
        print(diagnostic)
    if diagnostics:
        print(f"found {len(diagnostics)} broken repository-local links")
        return 1
    print(f"validated {file_count} tracked Markdown files; all repository-local links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
