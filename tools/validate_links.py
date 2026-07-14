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


LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
EXPLICIT_ID_RE = re.compile(r"\b(?:id|name)=[\"']([^\"']+)[\"']", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]*>")
PUNCTUATION_RE = re.compile(r"[^\w\- ]", re.UNICODE)


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
        yield number, re.sub(r"`[^`]*`", "", line)


def github_slug(heading: str) -> str:
    value = html.unescape(heading).lower()
    value = TAG_RE.sub("", value)
    value = re.sub(r"[\[\]_*~]", "", value)
    value = PUNCTUATION_RE.sub("", value)
    return re.sub(r"\s+", "-", value.strip())


def anchors(path: Path) -> set[str]:
    found: set[str] = set()
    counts: defaultdict[str, int] = defaultdict(int)
    text = path.read_text(encoding="utf-8")
    for _, line in visible_markdown_lines(text):
        heading = HEADING_RE.match(line)
        if heading:
            base = github_slug(heading.group(1))
            count = counts[base]
            found.add(base if count == 0 else f"{base}-{count}")
            counts[base] += 1
        found.update(unquote(value) for value in EXPLICIT_ID_RE.findall(line))
    return found


def local_parts(target: str):
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
        for line_number, line in visible_markdown_lines(text):
            for match in LINK_RE.finditer(line):
                target = match.group(1) or match.group(2)
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
