# ESAF-1500 Minimum Assessment Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish and enforce the minimum shared ESAF-1500 evidence, assessment-result, and five-level maturity contracts required by crosswalks and the `v0.5-beta` pilot profile.

**Architecture:** Markdown remains the normative source in `assessment/ESAF-1500.md`. Three strict Draft 2020-12 JSON Schemas and three fictional cross-referenced examples provide reusable machine contracts, while `tools/validate_assessment.py` enforces duplicate-key rejection, reference integrity, final-state conditions, cumulative maturity, lowest-component roll-ups, and non-claim boundaries that JSON Schema cannot express safely. Focused tests lock the prose vocabulary and every validator invariant; repository links, contributor instructions, CI, and project records expose the foundation without creating a workbook or scoring product.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python 3.13+, `jsonschema`, `unittest`, GitHub Actions YAML.

## Global Constraints

- Follow the approved design at `docs/superpowers/specs/2026-07-24-esaf-1500-assessment-foundation-design.md`.
- Use `shall`, `should`, and `may` according to `STYLE_GUIDE.md`.
- Preserve the ESAF-1100 methods `Examine`, `Interview`, `Test`, and `Observe`.
- Preserve the determinations `satisfied`, `partially_satisfied`, `not_satisfied`, `not_applicable`, and `not_assessed`.
- Use exactly the maturity levels `M0` Ad hoc, `M1` Managed, `M2` Defined, `M3` Measured, and `M4` Adaptive.
- Keep maturity and conformance independent; prohibit numeric averaging and unsupported composite scores.
- Keep examples fictional and non-authoritative.
- Do not create a workbook, audit checklist, certification method, governance-template library, automated determination, or compliance score.
- Use test-driven development for every enforceable invariant.
- Set `PYTHONDONTWRITEBYTECODE=1` for Python validation and commit no `__pycache__` directories.

---

### Task 1: Publish the normative ESAF-1500 contract

**Files:**
- Create: `assessment/ESAF-1500.md`
- Create: `tests/test_assessment_foundation.py`

**Interfaces:**
- Consumes: ESAF-1100 methods, determinations, design/operating-effectiveness definitions, and evidence semantics.
- Produces: exact normative headings, vocabularies, maturity order, aggregation rules, and non-claims consumed by Tasks 2-4.

- [ ] **Step 1: Write the failing content-contract tests**

Create `tests/test_assessment_foundation.py` with repository-root discovery and
tests that read the normative document:

```python
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "assessment" / "ESAF-1500.md"

REQUIRED_HEADINGS = (
    "Purpose",
    "Scope",
    "Relationship to the ESAF library",
    "Assessment principles",
    "Evidence records",
    "Evidence quality",
    "Assessment scope and methods",
    "Assessment results",
    "Findings and dispositions",
    "Maturity model",
    "Conformance and maturity",
    "Aggregation",
    "Traceability and change control",
    "Implementation and validation",
)
QUALITY_ATTRIBUTES = (
    "relevance",
    "reliability",
    "completeness",
    "timeliness",
    "attribution",
    "integrity",
    "traceability",
)
METHODS = ("Examine", "Interview", "Test", "Observe")
DETERMINATIONS = (
    "satisfied",
    "partially_satisfied",
    "not_satisfied",
    "not_applicable",
    "not_assessed",
)
MATURITY_LEVELS = (
    ("M0", "Ad hoc"),
    ("M1", "Managed"),
    ("M2", "Defined"),
    ("M3", "Measured"),
    ("M4", "Adaptive"),
)


def text() -> str:
    return STANDARD.read_text(encoding="utf-8")


class AssessmentFoundationTests(unittest.TestCase):
    def test_normative_standard_exists_with_required_sections(self) -> None:
        document = text()
        for heading in REQUIRED_HEADINGS:
            with self.subTest(heading=heading):
                self.assertRegex(document, rf"(?m)^## {re.escape(heading)}$")

    def test_evidence_quality_vocabulary_is_exact(self) -> None:
        section = text().split("## Evidence quality", 1)[1].split("\n## ", 1)[0]
        for attribute in QUALITY_ATTRIBUTES:
            self.assertEqual(section.count(f"**{attribute}:**"), 1)
        for rating in ("adequate", "limited", "inadequate", "not_evaluated"):
            self.assertIn(f"`{rating}`", section)
        self.assertIn("shall not be calculated by averaging", section)

    def test_methods_and_determinations_reuse_esaf_1100(self) -> None:
        document = text()
        for method in METHODS:
            self.assertIn(f"`{method}`", document)
        for determination in DETERMINATIONS:
            self.assertIn(f"`{determination}`", document)
        self.assertIn("ESAF-1100", document)

    def test_maturity_levels_are_exact_ordered_and_cumulative(self) -> None:
        section = text().split("## Maturity model", 1)[1].split("\n## ", 1)[0]
        positions = []
        for level, name in MATURITY_LEVELS:
            marker = f"`{level}` | {name}"
            self.assertEqual(section.count(marker), 1)
            positions.append(section.index(marker))
        self.assertEqual(positions, sorted(positions))
        self.assertIn("levels are cumulative", section)

    def test_maturity_cannot_replace_conformance(self) -> None:
        document = text()
        for determination in ("not_assessed", "not_satisfied", "partially_satisfied"):
            self.assertIn(determination, document)
        for prohibited in (
            "compliance",
            "certification",
            "equivalence",
            "endorsement",
            "continuous assurance",
        ):
            self.assertIn(prohibited, document.casefold())

    def test_rollup_is_lowest_substantiated_level_without_averaging(self) -> None:
        section = text().split("## Aggregation", 1)[1].split("\n## ", 1)[0]
        self.assertIn("lowest substantiated applicable component level", section)
        self.assertIn("Numeric averaging", section)
        self.assertIn("not-assessed components", section)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_assessment_foundation -v
```

Expected: FAIL because `assessment/ESAF-1500.md` does not exist.

- [ ] **Step 3: Write the normative assessment standard**

Create `assessment/ESAF-1500.md`. Use the headings locked by the test and
implement these exact contracts:

```markdown
# ESAF-1500 Assessment Guide

**Status:** Working Draft
**Version:** 0.1.0

## Purpose

ESAF-1500 defines the shared evidence, assessment-result, and maturity
semantics used by ESAF assessments, crosswalks, and profiles.

## Scope

This guide applies to assessments of ESAF requirements, controls, capabilities,
profiles, and mapped outcomes. It does not define a certification scheme,
automate professional judgment, or establish external-framework compliance.
```

Author the remaining required sections using the approved design Sections 4-9
as the controlling requirements. The document shall include:

- one required-field table for evidence records using the exact field names
  from design Section 5;
- one table containing the seven quality attributes and their meanings;
- the exact quality ratings and explicit sufficiency values;
- one required-field table for assessment results using the exact field names
  from design Section 6;
- one finding/disposition table using design Section 7;
- the exact five-row maturity table from design Section 8;
- cumulative prerequisite, basis-reference, and component-roll-up rules;
- the exact conformance and aggregation prohibitions from design Section 9;
  and
- the repository-relative paths of the three schemas and three examples in
  code formatting, plus the future validator command. Add clickable links in
  Task 2 only after every target exists.

Use machine values in backticks and human-readable labels in prose. State that
ESAF-1100 remains authoritative for control requirements and assessment
procedure definitions, while ESAF-1500 is authoritative for shared assessment
records and maturity semantics.

- [ ] **Step 4: Run the content tests and link validator**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_assessment_foundation -v
python tools/validate_links.py --check
```

Expected: PASS. The normative document shall not contain a broken link to a
future artifact.

- [ ] **Step 5: Commit the normative contract**

```powershell
git add assessment/ESAF-1500.md tests/test_assessment_foundation.py
git diff --cached --check
python tools/validate_links.py --check
git commit -m "docs: define ESAF-1500 assessment semantics"
```

---

### Task 2: Define strict schemas and cross-referenced examples

**Files:**
- Create: `assessment/schema/evidence-record.schema.json`
- Create: `assessment/schema/assessment-result.schema.json`
- Create: `assessment/schema/maturity-assessment.schema.json`
- Create: `assessment/examples/evidence-record.example.json`
- Create: `assessment/examples/assessment-result.example.json`
- Create: `assessment/examples/maturity-assessment.example.json`
- Modify: `tests/test_assessment_foundation.py`

**Interfaces:**
- Consumes: exact field names and closed vocabularies from Task 1.
- Produces: Draft 2020-12 schemas and a valid in-repository example graph consumed by Task 3.

- [ ] **Step 1: Add failing schema-contract tests**

Extend `tests/test_assessment_foundation.py`:

```python
import json

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_ROOT = ROOT / "assessment" / "schema"
EXAMPLE_ROOT = ROOT / "assessment" / "examples"
SCHEMA_NAMES = (
    "evidence-record",
    "assessment-result",
    "maturity-assessment",
)


class AssessmentSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = {
            name: json.loads(
                (SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8")
            )
            for name in SCHEMA_NAMES
        }
        self.examples = {
            name: json.loads(
                (EXAMPLE_ROOT / f"{name}.example.json").read_text(encoding="utf-8")
            )
            for name in SCHEMA_NAMES
        }

    def test_schemas_are_strict_draft_2020_12_documents(self) -> None:
        for name, schema in self.schemas.items():
            with self.subTest(name=name):
                self.assertEqual(
                    schema["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )
                Draft202012Validator.check_schema(schema)
                self.assertFalse(schema["additionalProperties"])

    def test_examples_validate_against_their_schemas(self) -> None:
        for name in SCHEMA_NAMES:
            with self.subTest(name=name):
                errors = list(
                    Draft202012Validator(
                        self.schemas[name],
                        format_checker=FormatChecker(),
                    ).iter_errors(self.examples[name])
                )
                self.assertEqual(errors, [])

    def test_examples_are_explicitly_fictional_and_non_authoritative(self) -> None:
        notice = (
            "Fictional non-authoritative example; no organization, ESAF control, "
            "profile, or external framework has been assessed."
        )
        for name, example in self.examples.items():
            with self.subTest(name=name):
                self.assertEqual(example["example_notice"], notice)

    def test_evidence_schema_requires_every_quality_attribute(self) -> None:
        required = set(
            self.schemas["evidence-record"]["properties"]["quality"]["required"]
        )
        self.assertTrue(set(QUALITY_ATTRIBUTES).issubset(required))

    def test_schema_enumerations_match_the_normative_contract(self) -> None:
        evidence = self.schemas["evidence-record"]
        result = self.schemas["assessment-result"]
        maturity = self.schemas["maturity-assessment"]
        self.assertEqual(
            evidence["$defs"]["qualityRating"]["enum"],
            ["adequate", "limited", "inadequate", "not_evaluated"],
        )
        self.assertEqual(
            result["properties"]["determination"]["enum"],
            list(DETERMINATIONS),
        )
        self.assertEqual(
            maturity["properties"]["level"]["enum"],
            [level for level, _name in MATURITY_LEVELS],
        )

    def test_every_object_boundary_rejects_extra_properties(self) -> None:
        def walk(value: object, path: tuple[object, ...] = ()):
            if isinstance(value, dict):
                yield path
                for key, child in value.items():
                    yield from walk(child, (*path, key))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    yield from walk(child, (*path, index))

        for name, example in self.examples.items():
            validator = Draft202012Validator(
                self.schemas[name], format_checker=FormatChecker()
            )
            for path in walk(example):
                mutated = json.loads(json.dumps(example))
                target = mutated
                for part in path:
                    target = target[part]
                target["unexpected"] = True
                with self.subTest(name=name, path=path):
                    self.assertTrue(list(validator.iter_errors(mutated)))
```

- [ ] **Step 2: Run the schema tests and verify they fail**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_assessment_foundation.AssessmentSchemaTests -v
```

Expected: FAIL because the schemas and examples do not exist.

- [ ] **Step 3: Create the evidence-record schema**

Create a strict Draft 2020-12 schema with:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://esaf.dev/schema/assessment/evidence-record.schema.json",
  "title": "ESAF evidence record",
  "type": "object",
  "additionalProperties": false
}
```

Require every top-level field in design Section 5. Define:

- identifier pattern `^EVD-[A-Z0-9][A-Z0-9-]*$`;
- the exact twelve `evidence_type` values;
- conditional `other_type_description` for `evidence_type: other`;
- mutually exclusive point-in-time and inclusive-period shapes;
- population with `description`, `sample`, and `selection_rationale`;
- one required object per quality attribute;
- rating enum `adequate`, `limited`, `inadequate`, `not_evaluated`;
- sufficiency enum `sufficient`, `limited`, `insufficient`;
- RFC 3339 `date-time` formats;
- SHA-256 digest pattern `^[0-9a-f]{64}$`;
- non-empty unique arrays where references or requirements are mandatory; and
- `additionalProperties: false` at every object boundary.

- [ ] **Step 4: Create the assessment-result schema**

Create a strict Draft 2020-12 schema with:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://esaf.dev/schema/assessment/assessment-result.schema.json",
  "title": "ESAF assessment result",
  "type": "object",
  "additionalProperties": false
}
```

Require every field in design Section 6. Define exact closed enums for status,
methods, determinations, effectiveness, severity, and finding status. Add
schema conditionals:

- `not_applicable` requires `applicability_rationale` and
  `applicability_approver`;
- `not_assessed` requires `scope_exclusion_rationale`;
- other determinations prohibit those conditional fields;
- `resolved` findings require `disposition_at`;
- `accepted` findings require `disposition_at`, `acceptance_authority`,
  `acceptance_rationale`, `review_at`, and `residual_risk`; and
- final records require at least one change-history entry.

Use `additionalProperties: false` at every object boundary.

- [ ] **Step 5: Create the maturity-assessment schema**

Create a strict Draft 2020-12 schema with:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://esaf.dev/schema/assessment/maturity-assessment.schema.json",
  "title": "ESAF maturity assessment",
  "type": "object",
  "additionalProperties": false
}
```

Require every field in design Section 8. Define:

- `level` enum `M0` through `M4`;
- criterion level using the same enum;
- criterion fields `criterion_id`, `statement`, `met`, `rationale`, and
  `basis_refs`;
- basis references matching `^(?:EVD|ASR)-[A-Z0-9][A-Z0-9-]*$`;
- component records with `maturity_ref`, `level`, and `applicability`;
- no numeric `score`, `average`, or extensible property bag; and
- `additionalProperties: false` at every object boundary.

Leave cumulative ordering and lowest-component behavior to Task 3.

- [ ] **Step 6: Create one fictional cross-referenced example graph**

Use these stable identities:

```text
EVD-EXAMPLE-CHANGE-LOG
ASR-EXAMPLE-CHANGE-CONTROL
FND-EXAMPLE-CHANGE-REVIEW
MAT-EXAMPLE-CHANGE-MANAGEMENT
```

The evidence example shall evaluate all seven attributes, use a fictional
change log, and reference `ASR-EXAMPLE-CHANGE-CONTROL`. The result example
shall reference the evidence, contain one resolved Minor finding, use
`partially_satisfied`, and avoid any compliance claim. The maturity example
shall claim `M1`, include met `M0` and `M1` criteria in order, and reference
both the evidence and assessment result. Each example shall contain:

```json
"example_notice": "Fictional non-authoritative example; no organization, ESAF control, profile, or external framework has been assessed."
```

Define `example_notice` as an optional property with that exact constant in
each schema. Require it in the tracked examples through
`tests/test_assessment_foundation.py`; do not make it mandatory for production
records.

Use these exact instance schema locators:

```text
evidence-record.example.json: "$schema": "../schema/evidence-record.schema.json"
assessment-result.example.json: "$schema": "../schema/assessment-result.schema.json"
maturity-assessment.example.json: "$schema": "../schema/maturity-assessment.schema.json"
```

After all six targets exist, replace the code-formatted artifact paths in
`assessment/ESAF-1500.md` with repository-local Markdown links.

- [ ] **Step 7: Run focused schema and content tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_assessment_foundation -v
python tools/validate_links.py --check
```

Expected: PASS.

- [ ] **Step 8: Commit schemas and examples**

```powershell
git add assessment/ESAF-1500.md assessment/schema assessment/examples tests/test_assessment_foundation.py
git diff --cached --check
git commit -m "feat: add assessment record schemas"
```

---

### Task 3: Implement fail-closed assessment validation

**Files:**
- Create: `tools/validate_assessment.py`
- Create: `tests/test_validate_assessment.py`

**Interfaces:**
- Consumes: three schema files and three example documents from Task 2.
- Produces: `validate(root: Path = ROOT) -> list[str]` and CLI
  `python tools/validate_assessment.py --check`.

- [ ] **Step 1: Write a valid temporary-foundation fixture**

Create `tests/test_validate_assessment.py`. Copy the three schemas and examples
from the repository into a `TemporaryDirectory` in `setUp`, and expose:

```python
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.validate_assessment import validate


REPO = Path(__file__).resolve().parents[1]


class AssessmentValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(REPO / "assessment" / "schema", self.root / "assessment" / "schema")
        shutil.copytree(REPO / "assessment" / "examples", self.root / "assessment" / "examples")

    def load(self, name: str) -> dict[str, object]:
        path = self.root / "assessment" / "examples" / f"{name}.example.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def write(self, name: str, value: dict[str, object]) -> None:
        path = self.root / "assessment" / "examples" / f"{name}.example.json"
        path.write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def test_valid_foundation_has_no_errors(self) -> None:
        self.assertEqual(validate(self.root), [])
```

- [ ] **Step 2: Add failing mutation tests**

Add independent tests that assert stable diagnostic substrings for:

```python
    def test_duplicate_json_key_is_rejected(self) -> None:
        path = self.root / "assessment/examples/evidence-record.example.json"
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace('"title":', '"title": "duplicate",\n  "title":', 1), encoding="utf-8")
        self.assertTrue(any("duplicate JSON key 'title'" in error for error in validate(self.root)))

    def test_unresolved_evidence_reference_is_rejected(self) -> None:
        result = self.load("assessment-result")
        result["evidence_refs"] = ["EVD-MISSING"]
        self.write("assessment-result", result)
        self.assertTrue(any("unresolved evidence reference EVD-MISSING" in error for error in validate(self.root)))

    def test_duplicate_finding_identifiers_are_rejected(self) -> None:
        result = self.load("assessment-result")
        result["findings"].append(json.loads(json.dumps(result["findings"][0])))
        self.write("assessment-result", result)
        self.assertTrue(any("duplicate finding identifier" in error for error in validate(self.root)))

    def test_final_result_requires_evidence_unless_not_assessed(self) -> None:
        result = self.load("assessment-result")
        result["status"] = "final"
        result["evidence_refs"] = []
        self.write("assessment-result", result)
        self.assertTrue(any("final result requires evidence" in error for error in validate(self.root)))

    def test_final_result_rejects_open_finding(self) -> None:
        result = self.load("assessment-result")
        result["status"] = "final"
        result["findings"][0]["status"] = "open"
        self.write("assessment-result", result)
        self.assertTrue(any("final result contains open finding" in error for error in validate(self.root)))

    def test_maturity_requires_every_prerequisite_level_in_order(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["level"] = "M2"
        self.write("maturity-assessment", maturity)
        self.assertTrue(any("criteria levels must equal M0 through M2" in error for error in validate(self.root)))

    def test_maturity_rejects_unmet_prerequisite(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][0]["met"] = False
        self.write("maturity-assessment", maturity)
        self.assertTrue(any("unmet prerequisite M0" in error for error in validate(self.root)))

    def test_rollup_cannot_exceed_lowest_applicable_component(self) -> None:
        component = self.load("maturity-assessment")
        component["maturity_id"] = "MAT-COMPONENT-A"
        component["level"] = "M0"
        component["criteria"] = component["criteria"][:1]
        component_path = (
            self.root / "assessment/examples/maturity-component.example.json"
        )
        component_path.write_text(
            json.dumps(component, indent=2) + "\n", encoding="utf-8"
        )
        maturity = self.load("maturity-assessment")
        maturity["component_results"] = [
            {"maturity_ref": "MAT-COMPONENT-A", "level": "M0", "applicability": "applicable"}
        ]
        self.write("maturity-assessment", maturity)
        self.assertTrue(any("exceeds lowest applicable component M0" in error for error in validate(self.root)))

    def test_numeric_average_field_is_rejected(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["average"] = 2.5
        self.write("maturity-assessment", maturity)
        errors = validate(self.root)
        self.assertTrue(any("average" in error and "unexpected" in error for error in errors))

    def test_conformance_overclaiming_field_is_rejected(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["compliance_status"] = "compliant"
        self.write("maturity-assessment", maturity)
        errors = validate(self.root)
        self.assertTrue(any("compliance_status" in error and "unexpected" in error for error in errors))

    def test_maturity_rationale_cannot_assert_compliance(self) -> None:
        maturity = self.load("maturity-assessment")
        maturity["criteria"][-1]["rationale"] = (
            "This maturity result establishes compliance."
        )
        self.write("maturity-assessment", maturity)
        self.assertTrue(
            any("prohibited conformance assertion" in error for error in validate(self.root))
        )
```

Add tests for every remaining design mutation: missing quality attributes,
unresolved result and finding references, duplicate finding IDs, invalid
`not_applicable`, invalid `not_assessed`, unresolved basis references, skipped
levels, duplicate levels, out-of-order levels, empty criterion basis, excluded
components being ignored in roll-up, missing files, invalid schemas, malformed
JSON, and stable repository-relative ordering.

- [ ] **Step 3: Run validator tests and verify they fail**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_assessment -v
```

Expected: FAIL because `tools/validate_assessment.py` does not exist.

- [ ] **Step 4: Implement deterministic loading and schema validation**

Create `tools/validate_assessment.py` with:

```python
#!/usr/bin/env python3
"""Validate the ESAF-1500 assessment contracts and tracked examples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_NAMES = ("evidence-record", "assessment-result", "maturity-assessment")
LEVELS = ("M0", "M1", "M2", "M3", "M4")


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
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
        key=lambda item: (list(item.absolute_path), item.message),
    )
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "document"
        diagnostics.append(f"{relative}: {location}: {error.message}")
    return diagnostics
```

Load all three required schemas, call
`Draft202012Validator.check_schema(document)`, use `FormatChecker`, and convert
all operational failures into stable diagnostics rather than tracebacks.

- [ ] **Step 5: Implement reference and identifier validation**

Implement small focused functions:

```python
def artifact_id(name: str, value: dict[str, object]) -> str:
    return str(value[{
        "evidence-record": "evidence_id",
        "assessment-result": "result_id",
        "maturity-assessment": "maturity_id",
    }[name]])


def expected_levels(level: str) -> list[str]:
    return list(LEVELS[: LEVELS.index(level) + 1])
```

Scan sorted `assessment/examples/*.example.json` files and dispatch each
document by its declared repository-relative schema locator. Build sets for
evidence, result, finding, and maturity IDs only after schema validation
succeeds for the applicable record. Reject duplicates globally.
Resolve:

- evidence result references;
- result evidence references;
- finding evidence references;
- maturity `basis_refs`; and
- every component maturity reference.

Every component reference shall resolve to another validated maturity record.
The tracked repository contains one maturity example with no component
roll-up; temporary tests create additional component records to exercise
roll-up behavior. Each component entry's declared `level` shall equal the
resolved component record's level.

- [ ] **Step 6: Implement final-state and maturity semantics**

For final assessment results:

- require one method and one evidence reference unless determination is
  `not_assessed`;
- reject open findings;
- reject `TBD`, `TODO`, `FIXME`, and bracketed placeholder markers in
  user-authored strings; and
- retain accepted findings without changing the determination.

For final maturity assessments:

- require criterion levels to equal `M0` through the claimed level exactly;
- require every prerequisite criterion to be met;
- require every criterion basis reference to resolve;
- require top-level basis references to resolve;
- compute the minimum ordinal level across applicable components;
- reject a claim above that minimum;
- ignore components explicitly marked `not_applicable` only when they include
  a rationale; and
- never calculate or emit a score.

Inspect maturity criterion rationales and limitations for the explicit
assertions `establishes compliance`, `establishes certification`,
`establishes equivalence`, `establishes endorsement`, and
`provides continuous assurance`. Reject those phrases with a stable
`prohibited conformance assertion` diagnostic. Do not use a broad keyword
blacklist that would reject legitimate non-claim language.

- [ ] **Step 7: Implement the CLI**

Use a required `--check` flag:

```python
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    errors = validate(ROOT)
    if errors:
        print(f"Assessment validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Successfully validated 3 assessment schemas and 3 tracked examples.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 8: Run focused validator and content tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_assessment -v
python -m unittest tests.test_assessment_foundation -v
python tools/validate_assessment.py --check
```

Expected: PASS.

- [ ] **Step 9: Commit the validator**

```powershell
git add tools/validate_assessment.py tests/test_validate_assessment.py assessment/schema/maturity-assessment.schema.json
git diff --cached --check
git commit -m "feat: validate ESAF assessment contracts"
```

---

### Task 4: Integrate ESAF-1500 into repository navigation and CI

**Files:**
- Modify: `assessment/README.md`
- Modify: `README.md`
- Modify: `framework/ESAF-1000.md`
- Modify: `controls/ESAF-1100.md`
- Modify: `profiles/README.md`
- Modify: `tools/README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `AGENTS.md`
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `project/BACKLOG.md`
- Modify: `tests/test_assessment_foundation.py`

**Interfaces:**
- Consumes: normative guide and validator command from Tasks 1-3.
- Produces: discoverable repository links, contribution rules, durable CI enforcement, and a backlog that no longer lists merged work as pending.

- [ ] **Step 1: Add failing integration tests**

Extend `tests/test_assessment_foundation.py`:

```python
    def test_repository_indexes_link_the_normative_guide(self) -> None:
        expected = {
            "README.md": "[ESAF-1500](assessment/ESAF-1500.md)",
            "assessment/README.md": "[ESAF-1500](ESAF-1500.md)",
            "framework/ESAF-1000.md": "[ESAF-1500](../assessment/ESAF-1500.md)",
            "controls/ESAF-1100.md": "[ESAF-1500](../assessment/ESAF-1500.md)",
            "profiles/README.md": "[ESAF-1500](../assessment/ESAF-1500.md)",
        }
        for relative, marker in expected.items():
            with self.subTest(relative=relative):
                self.assertIn(marker, (ROOT / relative).read_text(encoding="utf-8"))

    def test_tools_and_contributing_document_the_validator(self) -> None:
        for relative in ("tools/README.md", "CONTRIBUTING.md", "AGENTS.md"):
            with self.subTest(relative=relative):
                self.assertIn(
                    "python tools/validate_assessment.py --check",
                    (ROOT / relative).read_text(encoding="utf-8"),
                )

    def test_ci_runs_assessment_validation_for_assessment_changes(self) -> None:
        workflow = (ROOT / ".github/workflows/catalog-validation.yml").read_text(encoding="utf-8")
        self.assertEqual(workflow.count('- "assessment/**"'), 2)
        self.assertEqual(workflow.count('- "tools/validate_assessment.py"'), 2)
        self.assertIn("run: python tools/validate_assessment.py --check", workflow)

    def test_profile_contract_cannot_define_local_maturity_scale(self) -> None:
        profile = (ROOT / "profiles/README.md").read_text(encoding="utf-8")
        self.assertIn("shall reuse", profile)
        self.assertIn("shall not define a profile-local replacement maturity scale", profile)

    def test_completed_foundation_is_removed_from_backlog(self) -> None:
        backlog = (ROOT / "project/BACKLOG.md").read_text(encoding="utf-8")
        self.assertNotIn("Define the minimum ESAF-1500 assessment foundation", backlog)
```

- [ ] **Step 2: Run the integration tests and verify they fail**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_assessment_foundation -v
```

Expected: FAIL on the new navigation, CI, and backlog assertions.

- [ ] **Step 3: Update assessment and publication indexes**

Replace the placeholder `assessment/README.md` with links to:

- `ESAF-1500.md`;
- all three schemas;
- all three fictional examples; and
- `python tools/validate_assessment.py --check`.

In `README.md`, change the ESAF-1500 publication location from inline code to:

```markdown
| ESAF-1500 | Assessment Guide | [assessment/ESAF-1500.md](assessment/ESAF-1500.md) |
```

In `framework/ESAF-1000.md`, link the companion publication:

```markdown
| [ESAF-1500](../assessment/ESAF-1500.md) | Assessment methodology and maturity model |
```

In `controls/ESAF-1100.md`, add after the evidence model:

```markdown
[ESAF-1500](../assessment/ESAF-1500.md) is authoritative for shared
evidence-record, assessment-result, and maturity semantics. ESAF-1100 remains
authoritative for control requirements and assessment procedures.
```

Do not duplicate the full ESAF-1500 model in ESAF-1100.

- [ ] **Step 4: Bind profiles to the shared semantics**

Add to `profiles/README.md`:

```markdown
## Shared assessment semantics

Each profile shall reuse the determinations, evidence-quality attributes,
assessment-result contract, and maturity levels defined by
[ESAF-1500](../assessment/ESAF-1500.md). A profile may add stricter evidence
or maturity criteria, but shall not weaken cumulative prerequisites, treat
maturity as conformance, or define a profile-local replacement maturity scale.
```

- [ ] **Step 5: Document contributor and operator validation**

Add an `Assessment validation` section to `tools/README.md` with:

```text
python tools/validate_assessment.py --check
```

State that it validates the three schemas, tracked examples, references, final
states, maturity prerequisites, component roll-ups, and non-claim boundaries;
it does not score organizations.

Add the same command to `CONTRIBUTING.md` for assessment changes and to the
required validation habits in `AGENTS.md`.

- [ ] **Step 6: Add the assessment gate to CI**

In both pull-request and push path lists in
`.github/workflows/catalog-validation.yml`, add:

```yaml
      - "assessment/**"
      - "tools/validate_assessment.py"
```

After unit tests, add:

```yaml
      - name: Validate assessment foundation
        run: python tools/validate_assessment.py --check
```

- [ ] **Step 7: Reconcile the high-level backlog**

Remove only the completed ESAF-1500 assessment-foundation bullet from
`project/BACKLOG.md`. Preserve:

- qualified UK review;
- the pilot profile, including its assessment-foundation dependency;
- PCI DSS readiness;
- release closure; and
- HITRUST readiness.

Do not change the `v0.5-beta` milestone exit criterion in
`project/MILESTONES.md`; it remains the historical release requirement until
the milestone closes.

- [ ] **Step 8: Run focused integration validation**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_assessment_foundation -v
python -m unittest tests.test_validate_assessment -v
python tools/validate_assessment.py --check
python tools/validate_links.py --check
git diff --check
```

Expected: PASS.

- [ ] **Step 9: Commit repository integration**

```powershell
git add .github/workflows/catalog-validation.yml AGENTS.md CONTRIBUTING.md README.md assessment/README.md controls/ESAF-1100.md framework/ESAF-1000.md profiles/README.md project/BACKLOG.md tools/README.md tests/test_assessment_foundation.py
git diff --cached --check
git commit -m "docs: integrate ESAF-1500 foundation"
```

---

### Task 5: Review and validate the complete branch

**Files:**
- Review: every file changed from the merge base
- Create if needed: `docs/superpowers/reviews/2026-07-24-esaf-1500-assessment-foundation-review.md`
- Modify only when findings require correction: affected implementation and regression-test files

**Interfaces:**
- Consumes: the complete implementation from Tasks 1-4.
- Produces: one exact reviewed SHA, resolved Critical/Important findings, complete validation evidence, and a reviewable PR candidate.

- [ ] **Step 1: Inspect the whole branch**

Run:

```powershell
$base=(git merge-base main HEAD).Trim()
git diff --stat "$base..HEAD"
git diff --check "$base..HEAD"
git status --short --branch
```

Review all changes, not only the latest commit. Confirm no generated caches,
temporary examples, real organization data, or unrelated edits are present.

- [ ] **Step 2: Dispatch independent exact-head reviews**

Record:

```powershell
$candidate=(git rev-parse HEAD).Trim()
```

Obtain three independent reviews on `$candidate`:

1. technical/schema/validator correctness;
2. editorial/normative consistency; and
3. maturity, aggregation, conformance, and external-assurance overclaiming.

Each reviewer shall inspect the complete `$base..$candidate` diff and report
Critical, Important, and Minor findings. Resolve all Critical and Important
findings. Record the disposition of each Minor finding.

- [ ] **Step 3: Add regression tests before review-driven fixes**

For each reproducible defect, first add the smallest failing focused test,
verify the failure, implement the fix, and rerun the focused tests. Commit
review fixes with a descriptive message. Because the head changed, redispatch
all affected review disciplines on the new exact SHA.

- [ ] **Step 4: Run the complete validation set on the final reviewed SHA**

Use a short drive alias if the OneDrive-backed worktree causes path or
performance failures. Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_assessment_foundation -v
python -m unittest tests.test_validate_assessment -v
python -m unittest discover -s tests -v
python tools/validate_assessment.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
$base=(git merge-base main HEAD).Trim()
git diff --check "$base..HEAD"
```

Verify:

```powershell
$caches=@(Get-ChildItem -Path . -Directory -Filter '__pycache__' -Recurse -Force -ErrorAction SilentlyContinue)
if($caches.Count -ne 0){throw "Found $($caches.Count) __pycache__ directories"}
if(@(git status --porcelain).Count -ne 0){throw 'Worktree is not clean'}
```

Expected:

- every focused and full-suite test passes;
- all validators pass;
- only documented platform skips occur;
- no cache directories exist; and
- the worktree is clean.

- [ ] **Step 5: Prepare the exact-head PR evidence**

The PR description shall record:

- issue `#56`;
- design and implementation-plan paths;
- exact reviewed head SHA;
- files and contracts added;
- exact focused/full test counts and expected skips;
- each validator result;
- independent reviewer identities and dispositions;
- explicit non-claims;
- accepted Minor findings, if any; and
- confirmation that the PR head equals the reviewed SHA.

- [ ] **Step 6: Publish, verify, merge, and close**

Use `superpowers:finishing-a-development-branch` and `github:yeet`:

1. push `agent/esaf-1500-foundation`;
2. open a reviewable PR linked to issue `#56`;
3. verify the remote head equals the reviewed SHA;
4. wait for GitHub checks;
5. require a clean merge state;
6. merge only after all gates pass;
7. update local `main`;
8. rerun proportional post-merge validation;
9. close issue `#56` with the merged SHA, PR, tests, validators, review
   dispositions, and non-claims; and
10. remove only the owned branch and
    `.worktrees/agent-esaf-1500-foundation` worktree.

Do not close issue `#55`, select the pilot profile for issue `#57`, or advance
any Draft artifact lifecycle state as part of this work.

## Execution stop conditions

Stop and preserve a clean, recoverable state if:

- the normative vocabulary conflicts with ESAF-1100;
- a schema permits undeclared fields at an object boundary;
- a final result can omit required evidence without `not_assessed`;
- a maturity claim can skip or fail a prerequisite;
- a roll-up can exceed its lowest substantiated applicable component;
- maturity can imply control satisfaction, compliance, certification,
  equivalence, endorsement, external approval, or continuous assurance;
- a Critical or Important review finding remains unresolved;
- any focused test, full suite, validator, link check, diff check, or cache
  check fails;
- the branch head changes after review without affected re-review;
- the PR head differs from the reviewed SHA;
- GitHub checks fail or the PR is not cleanly mergeable; or
- cleanup cannot prove that the target is the owned branch or worktree.

Do not weaken schemas, tests, validation, normative boundaries, or repository
history to bypass a stop condition.
