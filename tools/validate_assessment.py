#!/usr/bin/env python3
"""Validate the ESAF-1500 assessment contracts and tracked examples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import TypeAlias

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_NAMES = ("evidence-record", "assessment-result", "maturity-assessment")
LEVELS = ("M0", "M1", "M2", "M3", "M4")
SCHEMA_LOCATORS = {
    f"../schema/{name}.schema.json": name for name in SCHEMA_NAMES
}
IDENTIFIER_FIELDS = {
    "evidence-record": "evidence_id",
    "assessment-result": "result_id",
    "maturity-assessment": "maturity_id",
}
IDENTIFIER_LABELS = {
    "evidence-record": "evidence",
    "assessment-result": "result",
    "maturity-assessment": "maturity",
}
PROHIBITED_ASSERTIONS = (
    "establishes compliance",
    "establishes certification",
    "establishes equivalence",
    "establishes endorsement",
    "provides continuous assurance",
)
NEGATED_ASSERTION_SUBJECT = re.compile(
    r"(?:\bnothing|\bno\s+(?:maturity\s+)?"
    r"(?:result|assessment|record|level|claim))\s*$",
    re.IGNORECASE,
)
PLACEHOLDER_WORD = re.compile(r"\b(?:TBD|TODO|FIXME)\b", re.IGNORECASE)
BRACKETED_PLACEHOLDER = re.compile(
    r"\[[^\]]*(?:TBD|TODO|FIXME|INSERT|PLACEHOLDER)\b[^\]]*\]",
    re.IGNORECASE,
)

JsonObject: TypeAlias = dict[str, object]
Record: TypeAlias = tuple[str, str, JsonObject]


def reject_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key {key!r}")
        value[key] = item
    return value


def load_json(path: Path) -> object:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )


def schema_diagnostics(
    validator: Draft202012Validator,
    value: object,
    relative: str,
) -> list[str]:
    diagnostics = []
    errors = sorted(
        validator.iter_errors(value),
        key=lambda item: (
            tuple(str(part) for part in item.absolute_path),
            item.message,
        ),
    )
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path)
        location = location or "document"
        diagnostics.append(f"{relative}: {location}: {error.message}")
    return diagnostics


def artifact_id(name: str, value: dict[str, object]) -> str:
    return str(value[IDENTIFIER_FIELDS[name]])


def expected_levels(level: str) -> list[str]:
    return list(LEVELS[: LEVELS.index(level) + 1])


def relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def load_document(path: Path, relative: str, diagnostics: list[str]) -> object | None:
    try:
        return load_json(path)
    except json.JSONDecodeError:
        diagnostics.append(f"{relative}: invalid JSON")
    except ValueError as error:
        diagnostics.append(f"{relative}: invalid JSON: {error}")
    except OSError as error:
        diagnostics.append(
            f"{relative}: unable to read file ({type(error).__name__})"
        )
    return None


def strings_in(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings_in(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings_in(child)


def list_of_strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def list_of_objects(value: object) -> list[JsonObject]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def asserted_prohibited_phrases(text: str):
    folded = text.casefold()
    for phrase in PROHIBITED_ASSERTIONS:
        offset = 0
        while True:
            index = folded.find(phrase, offset)
            if index < 0:
                break
            clause_start = max(
                folded.rfind(delimiter, 0, index)
                for delimiter in ".!?;:"
            )
            prefix = folded[clause_start + 1 : index]
            if not NEGATED_ASSERTION_SUBJECT.search(prefix):
                yield phrase
            offset = index + len(phrase)


def duplicate_finding_diagnostics(
    records: list[Record],
    validated_records: list[Record],
) -> list[str]:
    diagnostics: list[str] = []
    for name, relative, value in records:
        if name != "assessment-result":
            continue
        local_seen: set[str] = set()
        for finding in list_of_objects(value.get("findings")):
            finding_id = finding.get("finding_id")
            if not isinstance(finding_id, str):
                continue
            if finding_id in local_seen:
                diagnostics.append(
                    f"{relative}: duplicate finding identifier {finding_id}"
                )
            else:
                local_seen.add(finding_id)
    global_seen: dict[str, str] = {}
    for name, relative, value in validated_records:
        if name != "assessment-result":
            continue
        for finding in list_of_objects(value.get("findings")):
            finding_id = finding.get("finding_id")
            if not isinstance(finding_id, str):
                continue
            previous = global_seen.get(finding_id)
            if previous is not None and previous != relative:
                diagnostics.append(
                    f"{relative}: duplicate finding identifier {finding_id}"
                )
            else:
                global_seen[finding_id] = relative
    return diagnostics


def result_local_diagnostics(
    records: list[Record],
) -> list[str]:
    diagnostics: list[str] = []
    for name, relative, result in records:
        if name != "assessment-result":
            continue
        result_id = result.get("result_id", "<unknown>")
        if result.get("status") == "final":
            if result.get("determination") != "not_assessed":
                if not list_of_objects(result.get("methods")):
                    diagnostics.append(
                        f"{relative}: final result requires a method"
                    )
                if not list_of_strings(result.get("evidence_refs")):
                    diagnostics.append(
                        f"{relative}: final result requires evidence"
                    )
            for finding in list_of_objects(result.get("findings")):
                if finding.get("status") == "open":
                    diagnostics.append(
                        f"{relative}: final result contains open finding "
                        f"{finding.get('finding_id', '<unknown>')}"
                    )
            if any(
                PLACEHOLDER_WORD.search(text)
                or BRACKETED_PLACEHOLDER.search(text)
                for text in strings_in(result)
            ):
                diagnostics.append(
                    f"{relative}: final result {result_id} contains "
                    "unresolved placeholder language"
                )
    return diagnostics


def result_reference_diagnostics(
    records: list[Record],
    evidence_ids: set[str],
) -> list[str]:
    diagnostics: list[str] = []
    for name, relative, result in records:
        if name != "assessment-result":
            continue
        for evidence_ref in list_of_strings(result.get("evidence_refs")):
            if evidence_ref not in evidence_ids:
                diagnostics.append(
                    f"{relative}: unresolved evidence reference {evidence_ref}"
                )
        for finding in list_of_objects(result.get("findings")):
            finding_id = finding.get("finding_id", "<unknown>")
            for evidence_ref in list_of_strings(finding.get("evidence_refs")):
                if evidence_ref not in evidence_ids:
                    diagnostics.append(
                        f"{relative}: finding {finding_id} unresolved "
                        f"evidence reference {evidence_ref}"
                    )
    return diagnostics


def evidence_reference_diagnostics(
    records: list[Record],
    result_ids: set[str],
) -> list[str]:
    diagnostics: list[str] = []
    for name, relative, evidence in records:
        if name != "evidence-record":
            continue
        traceability = evidence.get("traceability")
        if not isinstance(traceability, dict):
            continue
        for result_ref in list_of_strings(traceability.get("result_refs")):
            if result_ref not in result_ids:
                diagnostics.append(
                    f"{relative}: unresolved result reference {result_ref}"
                )
    return diagnostics


def maturity_local_diagnostics(
    records: list[Record],
) -> list[str]:
    diagnostics: list[str] = []
    for name, relative, maturity in records:
        if name != "maturity-assessment":
            continue

        level = maturity.get("level")
        criteria = list_of_objects(maturity.get("criteria"))
        status = maturity.get("status")
        if status == "final" and isinstance(level, str) and level in LEVELS:
            actual_levels = [
                criterion.get("level")
                for criterion in criteria
                if isinstance(criterion.get("level"), str)
            ]
            required_levels = expected_levels(level)
            if actual_levels != required_levels:
                diagnostics.append(
                    f"{relative}: criteria levels must equal M0 through {level}"
                )
            for criterion in criteria:
                criterion_level = criterion.get("level", "<unknown>")
                if criterion.get("met") is False:
                    diagnostics.append(
                        f"{relative}: unmet prerequisite {criterion_level}"
                    )
                criterion_basis = list_of_strings(
                    criterion.get("basis_refs")
                )
                if not criterion_basis:
                    diagnostics.append(
                            f"{relative}: criterion {criterion_level} "
                            "basis_refs must not be empty"
                        )

        for criterion in criteria:
            rationale = criterion.get("rationale")
            if isinstance(rationale, str):
                for assertion in asserted_prohibited_phrases(rationale):
                    diagnostics.append(
                        f"{relative}: prohibited conformance assertion "
                        f"{assertion!r}"
                    )
        for limitation in list_of_strings(maturity.get("limitations")):
            for assertion in asserted_prohibited_phrases(limitation):
                diagnostics.append(
                    f"{relative}: prohibited conformance assertion "
                    f"{assertion!r}"
                )

        for component in list_of_objects(maturity.get("component_results")):
            applicability = component.get("applicability")
            if applicability == "not_applicable":
                rationale = component.get("rationale")
                if not isinstance(rationale, str) or not rationale:
                    diagnostics.append(
                        f"{relative}: not_applicable component requires rationale"
                    )
                continue
            if applicability == "not_assessed":
                if status == "final":
                    diagnostics.append(
                        f"{relative}: final roll-up contains not_assessed "
                        "component"
                    )
    return diagnostics


def maturity_reference_diagnostics(
    records: list[Record],
    basis_ids: set[str],
    maturity_records: dict[str, Record],
) -> list[str]:
    diagnostics: list[str] = []
    for name, relative, maturity in records:
        if name != "maturity-assessment":
            continue

        for basis_ref in list_of_strings(maturity.get("basis_refs")):
            if basis_ref not in basis_ids:
                diagnostics.append(
                    f"{relative}: unresolved basis reference {basis_ref}"
                )
        for criterion in list_of_objects(maturity.get("criteria")):
            criterion_level = criterion.get("level", "<unknown>")
            for basis_ref in list_of_strings(criterion.get("basis_refs")):
                if basis_ref not in basis_ids:
                    diagnostics.append(
                        f"{relative}: criterion {criterion_level} "
                        f"unresolved basis reference {basis_ref}"
                    )

        status = maturity.get("status")
        level = maturity.get("level")
        applicable_levels: list[str] = []
        for component in list_of_objects(maturity.get("component_results")):
            maturity_ref = component.get("maturity_ref")
            component_level = component.get("level")
            applicability = component.get("applicability")
            if not isinstance(maturity_ref, str):
                continue
            if maturity_ref == maturity.get("maturity_id"):
                diagnostics.append(
                    f"{relative}: self-referencing component {maturity_ref}"
                )
                continue
            resolved = maturity_records.get(maturity_ref)
            if resolved is None:
                diagnostics.append(
                    f"{relative}: unresolved component maturity reference "
                    f"{maturity_ref}"
                )
                continue
            resolved_value = resolved[2]
            resolved_level = resolved_value.get("level")
            if (
                isinstance(component_level, str)
                and isinstance(resolved_level, str)
                and component_level != resolved_level
            ):
                diagnostics.append(
                    f"{relative}: component {maturity_ref} declares "
                    f"{component_level} but resolved record declares "
                    f"{resolved_level}"
                )
            if status == "final" and resolved_value.get("status") != "final":
                diagnostics.append(
                    f"{relative}: {applicability} component {maturity_ref} "
                    "must be final"
                )
                continue
            if applicability != "applicable":
                continue
            if isinstance(resolved_level, str):
                applicable_levels.append(resolved_level)

        if (
            status == "final"
            and isinstance(level, str)
            and level in LEVELS
            and applicable_levels
        ):
            lowest = min(applicable_levels, key=LEVELS.index)
            if LEVELS.index(level) > LEVELS.index(lowest):
                diagnostics.append(
                    f"{relative}: claimed level {level} exceeds lowest "
                    f"applicable component {lowest}"
                )
    return diagnostics


def validate(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    diagnostics: list[str] = []
    validators: dict[str, Draft202012Validator] = {}

    for name in SCHEMA_NAMES:
        path = root / "assessment" / "schema" / f"{name}.schema.json"
        relative = relative_path(root, path)
        if not path.is_file():
            diagnostics.append(f"{relative}: required file is missing")
            continue
        schema = load_document(path, relative, diagnostics)
        if schema is None:
            continue
        if not isinstance(schema, dict):
            diagnostics.append(f"{relative}: schema document must be an object")
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as error:
            diagnostics.append(f"{relative}: invalid schema: {error.message}")
            continue
        validators[name] = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )

    canonical_examples = {
        root / "assessment" / "examples" / f"{name}.example.json"
        for name in SCHEMA_NAMES
    }
    for path in sorted(canonical_examples):
        if not path.is_file():
            diagnostics.append(
                f"{relative_path(root, path)}: required file is missing"
            )

    example_root = root / "assessment" / "examples"
    records: list[Record] = []
    validated_records: list[Record] = []
    paths = sorted(example_root.glob("*.example.json")) if example_root.is_dir() else []
    for path in paths:
        relative = relative_path(root, path)
        document = load_document(path, relative, diagnostics)
        if document is None:
            continue
        if not isinstance(document, dict):
            diagnostics.append(f"{relative}: document must be an object")
            continue
        locator = document.get("$schema")
        name = SCHEMA_LOCATORS.get(locator) if isinstance(locator, str) else None
        if name is None:
            diagnostics.append(
                f"{relative}: unsupported schema locator {locator!r}"
            )
            continue
        record = (name, relative, document)
        records.append(record)
        validator = validators.get(name)
        if validator is None:
            diagnostics.append(
                f"{relative}: required {name} schema is unavailable"
            )
            continue
        try:
            schema_errors = schema_diagnostics(validator, document, relative)
        except Exception as error:
            diagnostics.append(
                f"{relative}: schema validation failed "
                f"({type(error).__name__})"
            )
            continue
        diagnostics.extend(schema_errors)
        if not schema_errors:
            validated_records.append(record)

    records_by_type: dict[str, dict[str, Record]] = {
        name: {} for name in SCHEMA_NAMES
    }
    for name, relative, document in validated_records:
        identifier = artifact_id(name, document)
        existing = records_by_type[name].get(identifier)
        if existing is not None:
            label = IDENTIFIER_LABELS[name]
            diagnostics.append(
                f"{relative}: duplicate {label} identifier {identifier}"
            )
            continue
        records_by_type[name][identifier] = (name, relative, document)

    evidence_ids = set(records_by_type["evidence-record"])
    result_ids = set(records_by_type["assessment-result"])
    maturity_records = records_by_type["maturity-assessment"]
    diagnostics.extend(
        duplicate_finding_diagnostics(records, validated_records)
    )
    diagnostics.extend(
        evidence_reference_diagnostics(validated_records, result_ids)
    )
    diagnostics.extend(result_local_diagnostics(records))
    diagnostics.extend(
        result_reference_diagnostics(validated_records, evidence_ids)
    )
    diagnostics.extend(maturity_local_diagnostics(records))
    diagnostics.extend(
        maturity_reference_diagnostics(
            validated_records,
            evidence_ids | result_ids,
            maturity_records,
        )
    )
    return sorted(diagnostics)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    errors = validate(ROOT)
    if errors:
        print(
            f"Assessment validation failed with {len(errors)} error(s):",
            file=sys.stderr,
        )
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Successfully validated 3 assessment schemas and 3 tracked examples.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
