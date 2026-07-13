"""JSON Schema loading and deterministic validation diagnostics."""

import json
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker


_FORMAT_CHECKER = FormatChecker()


@_FORMAT_CHECKER.checks("uri")
def _is_absolute_uri(value: object) -> bool:
    if not isinstance(value, str) or any(character.isspace() for character in value):
        return False
    try:
        parsed = urlsplit(value)
        return bool(parsed.scheme and (parsed.netloc or parsed.scheme not in {"http", "https"}))
    except ValueError:
        return False


def load_schemas(root: Path) -> dict[str, Draft202012Validator]:
    """Load every crosswalk schema beneath ``root`` keyed by artifact name."""
    schema_root = root / "crosswalks" / "schema"
    validators: dict[str, Draft202012Validator] = {}
    for path in sorted(schema_root.glob("*.schema.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(document)
        validators[path.name.removesuffix(".schema.json")] = Draft202012Validator(
            document, format_checker=_FORMAT_CHECKER
        )
    return validators


def schema_errors(
    validator: Draft202012Validator, value: object, relative_path: str
) -> list[str]:
    """Return stable, path-qualified validation errors for an artifact."""
    errors = []
    for item in sorted(validator.iter_errors(value), key=lambda error: list(error.absolute_path)):
        location = ".".join(str(part) for part in item.absolute_path) or "metadata"
        errors.append(f"{relative_path}: {location}: {item.message}")
    return errors
