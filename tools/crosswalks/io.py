"""Strict input helpers for authoritative crosswalk Markdown."""

from pathlib import Path

import yaml


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys at every depth."""


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[object, object]:
    loader.flatten_mapping(node)
    result: dict[object, object] = {}
    for key_node, value_node in node.value:
        if not isinstance(key_node, yaml.ScalarNode):
            raise ValueError("YAML mapping keys must be scalar and hashable")
        key = loader.construct_object(key_node, deep=deep)
        try:
            hash(key)
        except TypeError as error:
            raise ValueError("YAML mapping keys must be scalar and hashable") from error
        if key in result:
            raise ValueError(f"duplicate YAML key {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def load_yaml_mapping(text: str) -> dict[str, object]:
    """Load one YAML mapping safely while rejecting duplicate keys."""
    value = yaml.load(text, Loader=_UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError("front matter must be a mapping")
    return value


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
    metadata = load_yaml_mapping(parts[1])
    return metadata, parts[2]
