from __future__ import annotations

import json
import re
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "profiles" / "ESAF-1800.md"
SCHEMA_ROOT = ROOT / "profiles" / "schema"
SCHEMA_NAMES = (
    "profile",
    "control-selections",
    "risk-overlays",
    "evidence-expectations",
    "external-references",
)

REQUIRED_HEADINGS = (
    "Purpose and scope",
    "Profile identity and lifecycle",
    "Applicability and system boundary",
    "Control selections",
    "Additional risks and overlays",
    "Evidence and assessment",
    "External references",
    "Traceability and validation",
    "Non-claim boundaries",
)
SELECTION_STATUSES = (
    "required",
    "conditional",
    "recommended",
    "not_selected",
)


def text() -> str:
    return STANDARD.read_text(encoding="utf-8")


class ProfileFoundationTests(unittest.TestCase):
    def test_normative_contract_exists_with_required_sections(self) -> None:
        document = text()
        for heading in REQUIRED_HEADINGS:
            with self.subTest(heading=heading):
                self.assertRegex(document, rf"(?m)^## {re.escape(heading)}$")

    def test_control_selection_vocabulary_is_closed(self) -> None:
        document = text()
        selection_section = document.split("## Control selections", 1)[1].split(
            "\n## ", 1
        )[0]
        defined_statuses = set(
            re.findall(r"(?m)^\| `([^`]+)` \|", selection_section)
        )
        self.assertSetEqual(defined_statuses, set(SELECTION_STATUSES))

    def test_non_selection_preserves_control_applicability(self) -> None:
        self.assertIn(
            "does not declare the underlying ESAF control inapplicable", text()
        )

    def test_assessment_reuses_esaf_1500(self) -> None:
        self.assertIn("[ESAF-1500](../assessment/ESAF-1500.md)", text())

    def test_profiles_cannot_replace_maturity_or_weaken_controls(self) -> None:
        document = text()
        self.assertIn(
            "shall not define a profile-local replacement maturity scale", document
        )
        self.assertIn("shall not alter or weaken a core control", document)


class ProfileSchemaTests(unittest.TestCase):
    def test_schemas_are_strict_draft_2020_12(self) -> None:
        for name in SCHEMA_NAMES:
            schema = json.loads(
                (SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8")
            )
            Draft202012Validator.check_schema(schema)
            self.assertEqual(
                schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
            )
            self.assertFalse(schema["additionalProperties"])

    def test_control_status_and_profile_lifecycle_are_closed(self) -> None:
        selections = json.loads(
            (SCHEMA_ROOT / "control-selections.schema.json").read_text(
                encoding="utf-8"
            )
        )
        status = selections["$defs"]["selection"]["properties"]["status"]["enum"]
        self.assertEqual(
            status, ["required", "conditional", "recommended", "not_selected"]
        )
        profile = json.loads(
            (SCHEMA_ROOT / "profile.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            profile["properties"]["status"]["enum"],
            ["proposed", "draft", "approved", "published", "deprecated", "retired"],
        )

    def test_component_schemas_accept_reusable_identifiers_and_lifecycle_states(
        self,
    ) -> None:
        schemas = {
            name: json.loads(
                (SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8")
            )
            for name in SCHEMA_NAMES
        }
        identity = {
            "schema_version": "0.1.0",
            "profile_id": "example-sector--general-profile--1.2.3",
            "profile_version": "0.1.0",
        }
        documents = {
            "control-selections": {
                **identity,
                "$schema": "../../schema/control-selections.schema.json",
                "selections": [
                    {
                        "control_id": "GOV-100",
                        "status": "not_selected",
                        "rationale": "The generic fixture adds no selection.",
                    }
                ],
            },
            "risk-overlays": {
                **identity,
                "$schema": "../../schema/risk-overlays.schema.json",
                "risks": [],
                "overlays": [],
            },
            "evidence-expectations": {
                **identity,
                "$schema": "../../schema/evidence-expectations.schema.json",
                "expectations": [],
            },
            "external-references": {
                **identity,
                "$schema": "../../schema/external-references.schema.json",
                "external_references": [
                    {
                        "mapping_set_id": "example--mapping-set--0.1.0",
                        "registry_path": "crosswalks/registry/example.md",
                        "expected_status": "draft",
                        "reference_use": "lifecycle_reference_only",
                        "qualified_review_required": True,
                        "non_import_statement": "Relationships and evidence are not imported.",
                    }
                ],
            },
        }
        for status in (
            "proposed",
            "draft",
            "approved",
            "published",
            "deprecated",
            "retired",
        ):
            with self.subTest(status=status):
                Draft202012Validator(schemas["profile"]).validate(
                    {
                        **identity,
                        "$schema": "../../schema/profile.schema.json",
                        "status": status,
                        "title": "Generic profile",
                        "scope": "A reusable profile scope.",
                        "applicability_conditions": [],
                        "source_boundary": {
                            "statement": "A bounded source set.",
                            "permitted_sources": ["ESAF"],
                            "excluded_sources": [],
                        },
                        "components": {
                            "readme": "README.md",
                            "control_selections": "control-selections.json",
                            "risk_overlays": "risk-overlays.json",
                            "evidence_expectations": "evidence-expectations.json",
                            "external_references": "external-references.json",
                        },
                        "change_history": [
                            {
                                "version": "0.1.0",
                                "date": "2026-07-24",
                                "author": "ESAF",
                                "description": "Initial profile version.",
                            }
                        ],
                    }
                )
        for name, document in documents.items():
            with self.subTest(component=name):
                Draft202012Validator(schemas[name]).validate(document)

    def test_component_schema_locators_resolve_from_a_profile_package(self) -> None:
        component_directory = ROOT / "profiles" / "example" / "0.1.0"
        for name in SCHEMA_NAMES:
            with self.subTest(component=name):
                schema = json.loads(
                    (SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8")
                )
                locator = schema["properties"]["$schema"]["const"]
                self.assertEqual(
                    (component_directory / PurePosixPath(locator)).resolve(),
                    (SCHEMA_ROOT / f"{name}.schema.json").resolve(),
                )

    def test_repository_paths_are_normalized_posix_paths(self) -> None:
        definitions = (
            ("profile", "relativePath"),
            ("external-references", "relativePath"),
        )
        invalid_paths = (
            "nested//component.json",
            "nested/./component.json",
            "nested/../component.json",
            r"nested\component.json",
            "/absolute/component.json",
        )
        for schema_name, definition in definitions:
            schema = json.loads(
                (SCHEMA_ROOT / f"{schema_name}.schema.json").read_text(
                    encoding="utf-8"
                )
            )
            validator = Draft202012Validator(schema["$defs"][definition])
            with self.subTest(schema=schema_name, path="nested/component.json"):
                self.assertFalse(
                    list(validator.iter_errors("nested/component.json"))
                )
            for path in invalid_paths:
                with self.subTest(schema=schema_name, path=path):
                    self.assertTrue(list(validator.iter_errors(path)))

    def test_nested_schema_objects_reject_unknown_properties(self) -> None:
        nested_records = (
            (
                "profile",
                "applicabilityCondition",
                {
                    "condition_id": "DEPLOYMENT-FACT",
                    "question": "Is the factual condition true?",
                    "answer_type": "boolean",
                    "activates_when": True,
                    "resolution_evidence": "Recorded deployment evidence.",
                },
            ),
            (
                "control-selections",
                "selection",
                {
                    "control_id": "GOV-100",
                    "status": "required",
                    "rationale": "A focused schema test.",
                },
            ),
            (
                "risk-overlays",
                "risk",
                {
                    "risk_id": "EXPOSURE-RISK",
                    "statement": "A bounded risk statement.",
                    "circumstances": "An in-scope circumstance.",
                    "source_basis": ["ESAF"],
                    "affected_controls": ["GOV-100"],
                    "overlay_ids": ["EXPOSURE-OVERLAY"],
                },
            ),
            (
                "evidence-expectations",
                "evidenceExpectation",
                {
                    "expectation_id": "EXPOSURE-EVIDENCE",
                    "purpose": "Demonstrate the expected evidence.",
                    "artifact_class": "Record",
                    "control_ids": ["GOV-100"],
                    "quality_attributes": ["relevance"],
                },
            ),
            (
                "external-references",
                "externalReference",
                {
                    "mapping_set_id": "example--mapping-set--0.1.0",
                    "registry_path": "crosswalks/registry/example.md",
                    "expected_status": "draft",
                    "reference_use": "lifecycle_reference_only",
                    "qualified_review_required": True,
                    "non_import_statement": "Relationships and evidence are not imported.",
                },
            ),
        )
        for schema_name, definition, record in nested_records:
            with self.subTest(schema=schema_name, definition=definition):
                schema = json.loads(
                    (SCHEMA_ROOT / f"{schema_name}.schema.json").read_text(
                        encoding="utf-8"
                    )
                )
                validator = Draft202012Validator(
                    {
                        "$schema": schema["$schema"],
                        "$defs": schema["$defs"],
                        "$ref": f"#/$defs/{definition}",
                    }
                )
                self.assertTrue(
                    list(validator.iter_errors({**record, "unexpected": True}))
                )


if __name__ == "__main__":
    unittest.main()
