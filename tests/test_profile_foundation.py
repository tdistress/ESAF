from __future__ import annotations

import json
import re
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator
from tools import validate_profiles


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "profiles" / "ESAF-1800.md"
SCHEMA_ROOT = ROOT / "profiles" / "schema"
UK_PROFILE_ROOT = ROOT / "profiles" / "uk" / "0.1.0"
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
UK_PROFILE_ID = "uk--jurisdiction-profile--0.1.0"
UK_COMPONENTS = {
    "readme": "README.md",
    "control_selections": "control-selections.json",
    "risk_overlays": "risk-overlays.json",
    "evidence_expectations": "evidence-expectations.json",
    "external_references": "external-references.json",
}
UK_MAPPING_IDS = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3"
    "--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
    "--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2"
    "--esaf-0.4-alpha--0.2.0",
)
ESAF_1500_QUALITY_ATTRIBUTES = {
    "relevance",
    "reliability",
    "completeness",
    "timeliness",
    "attribution",
    "integrity",
    "traceability",
}


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


class UKPilotProfileTests(unittest.TestCase):
    def load(self, filename: str) -> dict[str, object]:
        path = UK_PROFILE_ROOT / filename
        self.assertTrue(path.is_file(), f"missing UK pilot artifact {filename}")
        return json.loads(path.read_text(encoding="utf-8"))

    def records_by_id(
        self, filename: str, collection: str, identifier: str
    ) -> dict[str, dict[str, object]]:
        return {
            record[identifier]: record
            for record in self.load(filename)[collection]
        }

    def test_package_has_exact_identity_lifecycle_scope_and_components(self) -> None:
        manifest = self.load("profile.json")
        self.assertEqual(manifest["profile_id"], UK_PROFILE_ID)
        self.assertEqual(manifest["profile_version"], "0.1.0")
        self.assertEqual(manifest["status"], "draft")
        self.assertEqual(manifest["target_esaf_release"], "v0.5-beta")
        self.assertIn("deployed or operated in the United Kingdom", manifest["scope"])
        self.assertIn("regardless of organizational domicile", manifest["scope"])
        self.assertEqual(manifest["components"], UK_COMPONENTS)
        self.assertEqual(
            {path.name for path in UK_PROFILE_ROOT.iterdir()},
            {"profile.json", *UK_COMPONENTS.values()},
        )

    def test_conditions_are_bounded_booleans_with_resolution_evidence(self) -> None:
        manifest = self.load("profile.json")
        conditions = manifest["applicability_conditions"]
        self.assertEqual(
            {condition["condition_id"] for condition in conditions},
            {
                "INTERNET-EXPOSURE",
                "EXTERNAL-PROVIDER-USE",
                "MATERIAL-EXTERNAL-PROVIDER-DEPENDENCY",
                "THIRD-PARTY-ADMINISTRATION",
                "UNTRUSTED-MODEL-INTAKE",
                "UNTRUSTED-APPLICATION-ARTIFACT-INTAKE",
                "CALLABLE-TOOL-OR-PLUGIN-USE",
                "UNTRUSTED-INFRASTRUCTURE-DEPENDENCY-INTAKE",
                "UNSUPPORTED-TECHNOLOGY-COMPONENT-PRESENCE",
                "UNSUPPORTED-MODEL-PRESENCE",
                "UNSUPPORTED-INFRASTRUCTURE-COMPONENT-PRESENCE",
                "CAPABILITY-RETIREMENT-REQUIRED",
            },
        )
        for condition in conditions:
            with self.subTest(condition=condition["condition_id"]):
                self.assertEqual(condition["answer_type"], "boolean")
                self.assertIs(condition["activates_when"], True)
                self.assertTrue(condition["question"].strip())
                self.assertTrue(condition["resolution_evidence"].strip())

    def test_every_condition_is_used_by_a_selection_or_overlay(self) -> None:
        condition_ids = {
            condition["condition_id"]
            for condition in self.load("profile.json")["applicability_conditions"]
        }
        selections = self.load("control-selections.json")["selections"]
        overlays = self.load("risk-overlays.json")["overlays"]
        used = {
            condition_id
            for record in [*selections, *overlays]
            for condition_id in record.get("activation_conditions", [])
        }
        self.assertEqual(used, condition_ids)

    def test_conditional_selections_use_exact_factual_triggers(self) -> None:
        expected = {
            "IAM-140": ["THIRD-PARTY-ADMINISTRATION"],
            "MOD-110": ["UNTRUSTED-MODEL-INTAKE"],
            "MOD-150": ["UNSUPPORTED-MODEL-PRESENCE"],
            "APP-140": ["UNTRUSTED-APPLICATION-ARTIFACT-INTAKE"],
            "APP-150": ["INTERNET-EXPOSURE"],
            "API-110": ["INTERNET-EXPOSURE"],
            "API-120": ["CALLABLE-TOOL-OR-PLUGIN-USE"],
            "API-140": ["EXTERNAL-PROVIDER-USE"],
            "API-150": ["MATERIAL-EXTERNAL-PROVIDER-DEPENDENCY"],
            "INF-120": [
                "INTERNET-EXPOSURE",
                "UNTRUSTED-INFRASTRUCTURE-DEPENDENCY-INTAKE",
                "UNSUPPORTED-INFRASTRUCTURE-COMPONENT-PRESENCE",
            ],
            "INF-140": ["INTERNET-EXPOSURE"],
            "INF-150": ["INTERNET-EXPOSURE"],
            "OPS-150": ["CAPABILITY-RETIREMENT-REQUIRED"],
            "MON-110": ["INTERNET-EXPOSURE"],
            "CMP-120": [
                "EXTERNAL-PROVIDER-USE",
                "THIRD-PARTY-ADMINISTRATION",
            ],
            "ARC-140": [
                "EXTERNAL-PROVIDER-USE",
                "THIRD-PARTY-ADMINISTRATION",
            ],
            "ARC-150": ["UNSUPPORTED-TECHNOLOGY-COMPONENT-PRESENCE"],
        }
        observed = {
            selection["control_id"]: selection["activation_conditions"]
            for selection in self.load("control-selections.json")["selections"]
            if selection["status"] == "conditional"
        }
        self.assertEqual(observed, expected)

    def test_internet_exposure_traces_infrastructure_resource_safeguards(
        self,
    ) -> None:
        selections = self.records_by_id(
            "control-selections.json", "selections", "control_id"
        )
        risks = self.records_by_id("risk-overlays.json", "risks", "risk_id")
        overlays = self.records_by_id(
            "risk-overlays.json", "overlays", "overlay_id"
        )
        expectations = self.records_by_id(
            "evidence-expectations.json", "expectations", "expectation_id"
        )
        selection = selections["INF-150"]
        risk = risks["EXPOSED-INFRASTRUCTURE-RISK"]
        overlay = overlays["EXPOSED-BOUNDARY-OVERLAY"]
        evidence = expectations["BOUNDARY-EXPOSURE-EVIDENCE"]
        self.assertEqual(selection["status"], "conditional")
        self.assertEqual(selection["activation_conditions"], ["INTERNET-EXPOSURE"])
        self.assertIn("INF-150", risk["affected_controls"])
        self.assertIn("INF-150", overlay["affected_controls"])
        self.assertIn("INF-150", evidence["control_ids"])
        self.assertIn(overlay["overlay_id"], risk["overlay_ids"])
        self.assertIn(evidence["expectation_id"], overlay["evidence_expectation_ids"])
        self.assertIn(overlay["overlay_id"], evidence["overlay_ids"])
        for safeguard in (
            "capacity",
            "quota",
            "budget",
            "concurrency",
            "isolation",
            "scaling",
            "shutdown",
        ):
            with self.subTest(safeguard=safeguard):
                self.assertIn(safeguard, overlay["statement"].lower())
        self.assertIn("risk-proportionate", overlay["statement"].lower())
        self.assertIn(
            "without fixed profile thresholds", overlay["statement"].lower()
        )

    def test_control_ledger_matches_catalog_order_and_status_invariants(self) -> None:
        catalog = json.loads(
            (ROOT / "controls" / "catalog.json").read_text(encoding="utf-8")
        )
        selections = self.load("control-selections.json")["selections"]
        expected = [record["id"] for record in catalog["controls"]]
        observed = [record["control_id"] for record in selections]
        self.assertEqual(len(selections), 91)
        self.assertEqual(observed, expected)
        self.assertEqual(len(observed), len(set(observed)))
        self.assertEqual(len({record["rationale"] for record in selections}), 91)
        for selection in selections:
            with self.subTest(control=selection["control_id"]):
                self.assertIn(selection["status"], SELECTION_STATUSES)
                self.assertGreaterEqual(len(selection["rationale"].split()), 8)
                if selection["status"] == "conditional":
                    self.assertTrue(selection["activation_conditions"])
                else:
                    self.assertNotIn("activation_conditions", selection)

    def test_risks_overlays_and_evidence_are_non_empty_and_reuse_esaf_1500(self) -> None:
        risk_document = self.load("risk-overlays.json")
        evidence_document = self.load("evidence-expectations.json")
        self.assertGreaterEqual(len(risk_document["risks"]), 6)
        self.assertGreaterEqual(len(risk_document["overlays"]), 6)
        self.assertTrue(evidence_document["expectations"])
        used_attributes = set()
        for expectation in evidence_document["expectations"]:
            used_attributes.update(expectation["quality_attributes"])
        self.assertTrue(used_attributes)
        self.assertLessEqual(used_attributes, ESAF_1500_QUALITY_ATTRIBUTES)

    def test_evidence_emphases_preserve_all_seven_esaf_1500_evaluations(
        self,
    ) -> None:
        required_statement = (
            "All seven ESAF-1500 evidence-quality attributes remain required; "
            "the listed attributes are profile-specific emphases."
        )
        for expectation in self.load("evidence-expectations.json")["expectations"]:
            with self.subTest(expectation=expectation["expectation_id"]):
                self.assertIn(required_statement, expectation["strengthening"])

    def test_external_references_are_exactly_the_three_lifecycle_pins(self) -> None:
        references = self.load("external-references.json")["external_references"]
        self.assertEqual(
            tuple(reference["mapping_set_id"] for reference in references),
            UK_MAPPING_IDS,
        )
        for reference in references:
            with self.subTest(mapping=reference["mapping_set_id"]):
                self.assertEqual(reference["expected_status"], "draft")
                self.assertEqual(
                    reference["reference_use"], "lifecycle_reference_only"
                )
                self.assertIs(reference["qualified_review_required"], True)
                self.assertEqual(
                    reference["non_import_statement"],
                    "Relationships, external outcomes, and evidence are not imported.",
                )
                self.assertEqual(
                    set(reference),
                    {
                        "mapping_set_id",
                        "registry_path",
                        "expected_status",
                        "reference_use",
                        "qualified_review_required",
                        "non_import_statement",
                    },
                )

    def test_source_boundary_and_readme_state_explicit_non_claims(self) -> None:
        manifest = self.load("profile.json")
        boundary = manifest["source_boundary"]
        self.assertEqual(
            boundary["permitted_sources"],
            [
                "ESAF",
                *[
                    f"Pinned lifecycle metadata only: {mapping_id}"
                    for mapping_id in UK_MAPPING_IDS
                ],
            ],
        )
        excluded = " ".join(boundary["excluded_sources"]).lower()
        self.assertIn("laws", excluded)
        self.assertIn("substantive content", excluded)
        self.assertIn("other or unpinned external mappings", excluded)
        self.assertNotIn("unreviewed", excluded)
        self.assertTrue(
            all(mapping_id not in excluded for mapping_id in UK_MAPPING_IDS)
        )
        self.assertIn(
            "Relationships, external outcomes, and evidence are not imported",
            boundary["statement"],
        )
        readme = (UK_PROFILE_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("pinned lifecycle metadata only", readme.lower())
        self.assertIn("substantive mapping content remains excluded", readme.lower())
        for statement in (
            "does not establish legal sufficiency",
            "does not establish compliance",
            "does not establish certification",
            "does not establish equivalence",
            "does not establish endorsement",
            "does not establish external approval",
            "does not establish production readiness",
            "does not define the scope of Cyber Essentials",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement, readme)

    def test_published_pilot_passes_profile_validation(self) -> None:
        self.assertEqual(validate_profiles.validate(ROOT), [])


if __name__ == "__main__":
    unittest.main()
