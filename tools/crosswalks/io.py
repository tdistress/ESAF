"""Strict input helpers for authoritative crosswalk Markdown."""

from pathlib import Path

import yaml


def parse_front_matter(path: Path) -> tuple[dict[str, object], str]:
    """Return YAML metadata and Markdown body from a canonical UTF-8/LF file."""
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 byte-order mark is prohibited")
    if b"\r" in raw:
        raise ValueError("CR or CRLF line endings are prohibited")
    text = raw.decode("utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("malformed YAML front matter")
    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict):
        raise ValueError("front matter must be a mapping")
    return metadata, parts[2]
