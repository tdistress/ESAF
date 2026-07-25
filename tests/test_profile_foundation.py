from __future__ import annotations

import json
import hashlib
import re
import unittest
from pathlib import Path, PurePosixPath

import yaml
from jsonschema import Draft202012Validator
from tools import validate_profiles


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "profiles" / "ESAF-1800.md"
DESIGN = ROOT / "docs" / "superpowers" / "specs" / "2026-07-24-uk-pilot-profile-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-07-24-uk-pilot-profile.md"
PROFILE_README = ROOT / "profiles" / "README.md"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
TOOLS_README = ROOT / "tools" / "README.md"
VALIDATOR_TESTS = ROOT / "tests" / "test_validate_profiles.py"
WORKFLOW = ROOT / ".github" / "workflows" / "catalog-validation.yml"
SCHEMA_ROOT = ROOT / "profiles" / "schema"
UK_PROFILE_ROOT = ROOT / "profiles" / "uk" / "0.1.0"
UK_PROFILE_SOURCE = UK_PROFILE_ROOT / "PROFILE.md"
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
    "Source and authority boundaries",
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
    "source": "PROFILE.md",
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

    def test_normative_contract_defines_source_and_authority_boundaries(self) -> None:
        contract = text()
        self.assertIn("## Source and authority boundaries", contract)
        self.assertIn("shall identify permitted and excluded sources", contract)
        self.assertIn("shall be original ESAF synthesis", contract)

    def test_referenced_artifact_transition_preserves_independent_lifecycles(
        self,
    ) -> None:
        normalized = re.sub(r"\s+", " ", text())
        self.assertIn(
            "A referenced artifact lifecycle transition shall require an explicit "
            "profile update before the new state is relied upon. The transition "
            "shall not change the profile lifecycle automatically, and neither "
            "artifact shall be represented beyond its independently governed "
            "recorded state.",
            normalized,
        )

    def test_reusable_contract_contains_no_uk_pilot_instance_facts(self) -> None:
        contract = text()
        for instance_fact in (
            "United Kingdom",
            "uk--jurisdiction-profile--0.1.0",
            "v0.5-beta",
            "its lifecycle is `draft`",
            "profile version and schema version are `0.1.0`",
        ):
            with self.subTest(instance_fact=instance_fact):
                self.assertNotIn(instance_fact, contract)
        normalized = re.sub(r"\s+", " ", contract)
        self.assertIn(
            "Each profile manifest shall declare its profile identifier, "
            "profile version, schema version, lifecycle state, target "
            "ESAF release",
            normalized,
        )
        self.assertIn(
            "Each profile shall state factual applicability conditions",
            contract,
        )

    def test_mapping_editorial_status_and_registry_lifecycle_are_distinct(
        self,
    ) -> None:
        for path in (STANDARD, DESIGN, UK_PROFILE_ROOT / "README.md"):
            normalized = re.sub(
                r"\s+", " ", path.read_text(encoding="utf-8")
            ).lower()
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("mapping snapshot editorial status", normalized)
                self.assertIn("registry lifecycle", normalized)
        for path in (STANDARD, DESIGN):
            normalized = re.sub(
                r"\s+", " ", path.read_text(encoding="utf-8")
            ).lower()
            with self.subTest(path=path.relative_to(ROOT), drift=True):
                self.assertIn("identifier/path drift", normalized)
                self.assertIn("editorial status drift", normalized)
                self.assertIn("registry lifecycle-event drift", normalized)
                self.assertNotIn("approved mapping-set identifiers", normalized)

        schema = json.loads(
            (SCHEMA_ROOT / "external-references.schema.json").read_text(
                encoding="utf-8"
            )
        )
        reference = schema["$defs"]["externalReference"]
        self.assertIn(
            "mapping snapshot editorial status",
            reference["properties"]["expected_status"]["description"].lower(),
        )
        self.assertIn("registry lifecycle", reference["description"].lower())

    def test_expected_status_has_composite_normative_semantics(self) -> None:
        contract = re.sub(r"\s+", " ", text())
        self.assertIn(
            "`expected_status` shall mean the expected mapping snapshot "
            "editorial status before approval or the relied-upon governed "
            "registry state after approval.",
            contract,
        )
        self.assertIn(
            "Draft and Reviewed mapping snapshots shall have no registry "
            "lifecycle events.",
            contract,
        )
        self.assertIn(
            "Approved mapping snapshots and later governed registry states "
            "shall have the applicable governed registry lifecycle events.",
            contract,
        )

    def test_original_design_uses_editorial_and_lifecycle_terms_consistently(
        self,
    ) -> None:
        design = re.sub(r"\s+", " ", DESIGN.read_text(encoding="utf-8"))
        self.assertNotIn("three separate Draft United Kingdom mapping sets", design)
        self.assertNotIn("Those mapping sets remain Draft", design)
        self.assertNotIn(
            "three Draft mapping sets and their lifecycle states",
            design,
        )
        self.assertIn("three separate United Kingdom mapping snapshots", design)
        self.assertIn("retain Draft editorial status", design)
        self.assertIn("governed registry records", design)

    def test_design_risk_lenses_do_not_claim_external_evidentiary_support(
        self,
    ) -> None:
        design = re.sub(r"\s+", " ", DESIGN.read_text(encoding="utf-8"))
        self.assertIn(
            "supported by ESAF within the lifecycle-only external-reference "
            "boundary",
            design,
        )
        self.assertIn(
            "does not treat lifecycle metadata as substantive external "
            "evidentiary support",
            design,
        )
        self.assertNotIn(
            "supported by ESAF and the pinned Cyber Essentials source boundary",
            design,
        )

    def test_original_design_and_plan_pin_lifecycle_only_source_boundary(
        self,
    ) -> None:
        expected_boundary = (
            "ESAF plus pinned lifecycle metadata only from the exact three "
            "mapping snapshots"
        )
        expected_exclusion = (
            "Substantive mapping content, relationships, external outcomes, "
            "evidence, and interpretations are excluded."
        )
        for path in (DESIGN, PLAN):
            document = re.sub(
                r"\s+",
                " ",
                path.read_text(encoding="utf-8"),
            )
            with self.subTest(path=path.name):
                self.assertIn(expected_boundary, document)
                self.assertIn(expected_exclusion, document)

    def test_rsk_100_rationale_does_not_pin_a_stale_risk_count(self) -> None:
        selections = json.loads(
            (UK_PROFILE_ROOT / "control-selections.json").read_text(
                encoding="utf-8"
            )
        )["selections"]
        rationale = next(
            item["rationale"]
            for item in selections
            if item["control_id"] == "RSK-100"
        )
        self.assertNotRegex(
            rationale,
            r"(?i)\b(?:six|6)\s+additional risk lenses\b",
        )
        self.assertIn("profile risk", rationale.lower())

    def test_validator_tests_use_profile_domain_taxonomy(self) -> None:
        tests = VALIDATOR_TESTS.read_text(encoding="utf-8")
        self.assertNotRegex(tests, r"\b(?:outside_)?country\b")
        self.assertNotIn("_profile_country", tests)


class ProfileSchemaTests(unittest.TestCase):
    def test_manifest_requires_target_release_and_control_catalog_pin(
        self,
    ) -> None:
        schema = json.loads(
            (SCHEMA_ROOT / "profile.schema.json").read_text(encoding="utf-8")
        )
        self.assertIn("target_esaf_release", schema["required"])
        self.assertIn("control_catalog", schema["required"])

    def test_evidence_expectations_use_esaf_1500_evidence_types(self) -> None:
        schema = json.loads(
            (SCHEMA_ROOT / "evidence-expectations.schema.json").read_text(
                encoding="utf-8"
            )
        )
        expectation = schema["$defs"]["evidenceExpectation"]
        self.assertIn("evidence_types", expectation["required"])
        self.assertNotIn("artifact_class", expectation["properties"])
        self.assertEqual(
            set(
                expectation["properties"]["evidence_types"]["items"]["enum"]
            ),
            {
                "policy",
                "procedure",
                "record",
                "configuration",
                "log",
                "technical_test",
                "observation",
                "interview",
                "metric",
                "contract",
                "external_assurance",
                "other",
            },
        )

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

    def test_risk_source_basis_schema_declares_closed_reference_semantics(
        self,
    ) -> None:
        schema = json.loads(
            (SCHEMA_ROOT / "risk-overlays.schema.json").read_text(
                encoding="utf-8"
            )
        )
        source_basis = schema["$defs"]["risk"]["properties"]["source_basis"]
        self.assertEqual(
            source_basis["items"]["$ref"],
            "#/$defs/sourceBasisReference",
        )
        description = schema["$defs"]["sourceBasisReference"]["description"]
        self.assertIn("authoritative ESAF control identifier", description)
        self.assertIn("manifest permitted source identifier", description)

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
            "profile_version": "1.2.3",
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
                        "target_esaf_release": "v1.2.3",
                        "control_catalog": {
                            "path": "controls/catalog.json",
                            "schema_version": "1.0.0",
                            "sha256": "0" * 64,
                            "records": [
                                {
                                    "id": "GOV-100",
                                    "version": "1.0.0",
                                    "status": "published",
                                    "path": "GOV/GOV-100.md",
                                    "record_sha256": "0" * 64,
                                }
                            ],
                        },
                        "title": "Generic profile",
                        "scope": "A reusable profile scope.",
                        "applicability_conditions": [],
                        "source_boundary": {
                            "statement": "A bounded source set.",
                            "permitted_sources": ["ESAF"],
                            "excluded_sources": [],
                        },
                        "components": {
                            "source": "PROFILE.md",
                            "readme": "README.md",
                            "control_selections": "control-selections.json",
                            "risk_overlays": "risk-overlays.json",
                            "evidence_expectations": "evidence-expectations.json",
                            "external_references": "external-references.json",
                        },
                        "change_history": [
                            {
                                "version": "1.2.3",
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

    def test_external_reference_schema_permits_empty_and_reviewed_references(
        self,
    ) -> None:
        schema = json.loads(
            (SCHEMA_ROOT / "external-references.schema.json").read_text(
                encoding="utf-8"
            )
        )
        identity = {
            "$schema": "../../schema/external-references.schema.json",
            "schema_version": "0.1.0",
            "profile_id": "example--sector-profile--1.2.3",
            "profile_version": "1.2.3",
        }
        validator = Draft202012Validator(schema)
        validator.validate({**identity, "external_references": []})
        reference = {
            "mapping_set_id": "example--mapping-set--0.1.0",
            "registry_path": "crosswalks/registry/example.md",
            "expected_status": "reviewed",
            "reference_use": "lifecycle_reference_only",
            "qualified_review_required": True,
            "non_import_statement": "Relationships and evidence are not imported.",
        }
        validator.validate({**identity, "external_references": [reference]})

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
                    "evidence_types": ["record"],
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


class ProfileRepositoryIntegrationTests(unittest.TestCase):
    def test_repository_contains_exactly_one_draft_pilot_package(self) -> None:
        self.assertEqual(
            validate_profiles.discover_profile_packages(ROOT),
            (UK_PROFILE_ROOT,),
        )

    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_publication_indexes_link_contract_and_draft_uk_pilot(self) -> None:
        expected_links = {
            "README.md": (
                "profiles/ESAF-1800.md",
                "profiles/uk/0.1.0/README.md",
            ),
            "framework/ESAF-1000.md": (
                "../profiles/ESAF-1800.md",
                "../profiles/uk/0.1.0/README.md",
            ),
            "profiles/README.md": (
                "ESAF-1800.md",
                "uk/0.1.0/README.md",
            ),
        }
        for path, links in expected_links.items():
            document = self.read(path)
            for link in links:
                with self.subTest(path=path, link=link):
                    self.assertRegex(
                        document,
                        rf"\[[^\]]+\]\({re.escape(link)}\)",
                    )

    def test_profile_authoring_guidance_is_draft_non_claim_and_validated(
        self,
    ) -> None:
        for path in ("CONTRIBUTING.md", "profiles/README.md"):
            document = self.read(path)
            normalized = re.sub(r"\s+", " ", document)
            with self.subTest(path=path, requirement="editing"):
                self.assertIn("profiles/<profile-domain>/<version>/", document)
            with self.subTest(path=path, requirement="draft"):
                self.assertIn("shall not advance beyond Draft", normalized)
                self.assertNotIn("shall remain Draft", document)
            with self.subTest(path=path, requirement="non-claim"):
                self.assertIn(
                    "shall not claim compliance, certification, equivalence, "
                    "endorsement, legal sufficiency, external approval, or "
                    "production readiness",
                    normalized,
                )
            with self.subTest(path=path, requirement="validation"):
                self.assertIn(
                    "python tools/validate_profiles.py --check",
                    document,
                )

    def test_tools_readme_documents_profile_validation(self) -> None:
        document = self.read("tools/README.md")
        self.assertIn("## Profile validation", document)
        self.assertIn("python tools/validate_profiles.py --check", document)
        self.assertIn("Draft profile packages", document)

    def test_component_path_language_is_package_relative(self) -> None:
        for path in (
            DESIGN,
            PLAN,
            STANDARD,
            PROFILE_README,
            CONTRIBUTING,
            TOOLS_README,
        ):
            document = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("repository-relative component path", document)
                self.assertIn("package-relative component", document)
                self.assertIn("document-relative", document)

    def test_generic_authoring_guidance_uses_profile_domain_terminology(
        self,
    ) -> None:
        for path in (
            STANDARD,
            DESIGN,
            PLAN,
            PROFILE_README,
            CONTRIBUTING,
            TOOLS_README,
        ):
            document = path.read_text(encoding="utf-8")
            normalized = re.sub(r"\s+", " ", document)
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("profile domain", normalized.lower())
                self.assertNotIn("<jurisdiction-or-sector>", document)
                self.assertNotIn("profiles/<jurisdiction>/<version>/", document)
                self.assertNotIn("profiles/<country>/<semver>/", document)

    def test_workflow_assertions_are_structurally_scoped(self) -> None:
        workflow = yaml.load(
            WORKFLOW.read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        self.assertIn("profiles/**", workflow["on"]["pull_request"]["paths"])
        self.assertIn("profiles/**", workflow["on"]["push"]["paths"])
        steps = workflow["jobs"]["validate"]["steps"]
        self.assertTrue(
            any(
                step.get("name") == "Validate profiles"
                and step.get("run") == "python tools/validate_profiles.py --check"
                for step in steps
            )
        )


class UKPilotProfileTests(unittest.TestCase):
    def test_markdown_source_contains_every_authoritative_profile_record(
        self,
    ) -> None:
        source = UK_PROFILE_SOURCE.read_text(encoding="utf-8")
        for filename in (
            "profile.json",
            "control-selections.json",
            "risk-overlays.json",
            "evidence-expectations.json",
            "external-references.json",
        ):
            with self.subTest(filename=filename):
                self.assertIn(f"## {filename}\n\n```json\n", source)

    def test_control_catalog_pin_matches_authoritative_catalog(self) -> None:
        profile = json.loads(
            (UK_PROFILE_ROOT / "profile.json").read_text(encoding="utf-8")
        )
        catalog_path = ROOT / profile["control_catalog"]["path"]
        self.assertEqual(
            profile["control_catalog"]["sha256"],
            hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
        )
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["control_catalog"]["schema_version"],
            catalog["schema_version"],
        )
        records = {
            record["id"]: record
            for record in profile["control_catalog"]["records"]
        }
        self.assertEqual(records.keys(), {record["id"] for record in catalog["controls"]})
        for catalog_record in catalog["controls"]:
            record = records[catalog_record["id"]]
            self.assertEqual(record["version"], catalog_record["version"])
            self.assertEqual(record["status"], catalog_record["status"])
            self.assertEqual(record["path"], catalog_record["path"])
            self.assertEqual(
                record["record_sha256"],
                hashlib.sha256(
                    (ROOT / "controls" / record["path"]).read_bytes()
                ).hexdigest(),
            )

    def load(self, filename: str) -> dict[str, object]:
        path = UK_PROFILE_ROOT / filename
        self.assertTrue(path.is_file(), f"missing UK pilot artifact {filename}")
        return json.loads(path.read_text(encoding="utf-8"))

    def condition(self, condition_id: str) -> dict[str, object]:
        return self.records_by_id(
            "profile.json", "applicability_conditions", "condition_id"
        )[condition_id]

    def selection(self, control_id: str) -> dict[str, object]:
        return self.records_by_id(
            "control-selections.json", "selections", "control_id"
        )[control_id]

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
                "INTERNET-REACHABLE-API",
                "INTERNET-REACHABLE-AI-APPLICATION-INTERFACE",
                "EXTERNAL-PROVIDER-USE",
                "EXTERNAL-AI-SERVICE-INTEGRATION",
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

    def test_applicability_contract_pins_positive_and_negative_semantics(
        self,
    ) -> None:
        overlays = self.records_by_id(
            "risk-overlays.json", "overlays", "overlay_id"
        )
        expectations = self.records_by_id(
            "evidence-expectations.json", "expectations", "expectation_id"
        )
        readme = (UK_PROFILE_ROOT / "README.md").read_text(encoding="utf-8")
        contracts = (
            {
                "control_id": "APP-150",
                "condition_id": (
                    "INTERNET-REACHABLE-AI-APPLICATION-INTERFACE"
                ),
                "overlay_id": "AI-APPLICATION-INTERFACE-OVERLAY",
                "expectation_id": "AI-APPLICATION-INTERFACE-EVIDENCE",
                "records": (
                    (
                        "condition question",
                        (
                            "user or automated client",
                            "invokes or interacts with the assessed ai "
                            "capability",
                            "privileged ai-use workflow",
                            "excluding a console or path used only to "
                            "administer supporting systems",
                        ),
                    ),
                    (
                        "resolution evidence",
                        (
                            "ai-use",
                            "privileged",
                            "administration-only consoles or paths",
                            "excluded",
                        ),
                    ),
                    (
                        "selection rationale",
                        (
                            "user or automated client",
                            "invokes or interacts with the assessed ai "
                            "capability",
                            "administration-only console or path is excluded "
                            "from this condition",
                        ),
                    ),
                    (
                        "overlay statement",
                        (
                            "user or automated client",
                            "invokes or interacts with the assessed ai "
                            "capability",
                            "privileged ai-use workflow",
                        ),
                    ),
                    (
                        "overlay strengthening",
                        (
                            "administration-only console or path is excluded "
                            "from this condition",
                        ),
                    ),
                    (
                        "evidence purpose",
                        (
                            "ai-use interfaces and workflows",
                            "user or automated client",
                            "invoked or interacted with the assessed ai "
                            "capability",
                        ),
                    ),
                    (
                        "evidence strengthening",
                        (
                            "administration-only consoles or paths",
                            "excluded",
                        ),
                    ),
                    (
                        "readme",
                        (
                            "administration-only console or path does not "
                            "satisfy the internet-reachable ai "
                            "application-interface condition",
                        ),
                    ),
                ),
            },
            {
                "control_id": "API-140",
                "condition_id": "EXTERNAL-AI-SERVICE-INTEGRATION",
                "overlay_id": "EXTERNAL-AI-SERVICE-INTEGRATION-OVERLAY",
                "expectation_id": (
                    "EXTERNAL-AI-SERVICE-INTEGRATION-EVIDENCE"
                ),
                "records": (
                    (
                        "condition question",
                        ("live external ai service integration",),
                    ),
                    (
                        "resolution evidence",
                        (
                            "downloaded or otherwise acquired external "
                            "model artifact",
                            "without a live service boundary",
                            "excluded",
                        ),
                    ),
                    (
                        "selection rationale",
                        (
                            "live external ai service integration",
                            "downloaded or otherwise acquired external "
                            "model artifact without a live service boundary "
                            "is excluded from this condition",
                        ),
                    ),
                    (
                        "overlay statement",
                        ("live external ai service integration",),
                    ),
                    (
                        "overlay strengthening",
                        (
                            "downloaded or otherwise acquired external "
                            "model artifact without a live service boundary "
                            "is excluded from this condition",
                        ),
                    ),
                    (
                        "evidence purpose",
                        ("live external ai service integration",),
                    ),
                    (
                        "evidence strengthening",
                        (
                            "downloaded or otherwise acquired external "
                            "model artifacts without a live service boundary",
                            "excluded",
                        ),
                    ),
                    (
                        "readme",
                        (
                            "downloaded or otherwise acquired external model "
                            "without a live service integration does not "
                            "satisfy the external ai service-integration "
                            "condition",
                        ),
                    ),
                ),
            },
        )

        for contract in contracts:
            condition = self.condition(contract["condition_id"])
            selection = self.selection(contract["control_id"])
            overlay = overlays[contract["overlay_id"]]
            expectation = expectations[contract["expectation_id"]]
            texts = {
                "condition question": condition["question"],
                "resolution evidence": condition["resolution_evidence"],
                "selection rationale": selection["rationale"],
                "overlay statement": overlay["statement"],
                "overlay strengthening": overlay["strengthening_rationale"],
                "evidence purpose": expectation["purpose"],
                "evidence strengthening": expectation["strengthening"],
                "readme": readme,
            }
            with self.subTest(
                control=contract["control_id"],
                assertion="condition identifier",
            ):
                self.assertEqual(
                    selection["activation_conditions"],
                    [contract["condition_id"]],
                )
                self.assertEqual(
                    overlay["activation_conditions"],
                    [contract["condition_id"]],
                )
                self.assertEqual(
                    expectation["activation_conditions"],
                    [contract["condition_id"]],
                )
            for record_name, phrases in contract["records"]:
                for phrase in phrases:
                    with self.subTest(
                        control=contract["control_id"],
                        record=record_name,
                        phrase=phrase,
                    ):
                        self.assertIn(
                            phrase,
                            " ".join(
                                texts[record_name].lower().split()
                            ),
                        )

    def test_api_150_material_dependency_condition_is_purely_factual(
        self,
    ) -> None:
        question = self.condition(
            "MATERIAL-EXTERNAL-PROVIDER-DEPENDENCY"
        )["question"]
        self.assertEqual(
            question,
            "Is the assessed capability classified E1 through E4 and "
            "materially dependent on an external provider or platform?",
        )
        self.assertNotRegex(
            question,
            r"(?i)\b(must|should|addressed|replacement decision)\b",
        )

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
            "APP-150": [
                "INTERNET-REACHABLE-AI-APPLICATION-INTERFACE"
            ],
            "API-110": ["INTERNET-REACHABLE-API"],
            "API-120": ["CALLABLE-TOOL-OR-PLUGIN-USE"],
            "API-140": ["EXTERNAL-AI-SERVICE-INTEGRATION"],
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

    def test_conditional_overlay_and_evidence_truth_table_is_machine_resolvable(
        self,
    ) -> None:
        expected = {
            "EXPOSED-BOUNDARY-OVERLAY": (
                "INTERNET-EXPOSURE",
                {
                    "IAM-110",
                    "IAM-130",
                    "INF-110",
                    "INF-120",
                    "INF-140",
                    "INF-150",
                    "MON-110",
                },
                "BOUNDARY-EXPOSURE-EVIDENCE",
            ),
            "AI-APPLICATION-INTERFACE-OVERLAY": (
                "INTERNET-REACHABLE-AI-APPLICATION-INTERFACE",
                {"APP-150"},
                "AI-APPLICATION-INTERFACE-EVIDENCE",
            ),
            "INTERNET-REACHABLE-API-OVERLAY": (
                "INTERNET-REACHABLE-API",
                {"API-110"},
                "INTERNET-REACHABLE-API-EVIDENCE",
            ),
            "MODEL-INTAKE-OVERLAY": (
                "UNTRUSTED-MODEL-INTAKE",
                {"MOD-110"},
                "MODEL-INTAKE-EVIDENCE",
            ),
            "APPLICATION-ARTIFACT-INTAKE-OVERLAY": (
                "UNTRUSTED-APPLICATION-ARTIFACT-INTAKE",
                {"APP-140"},
                "APPLICATION-ARTIFACT-INTAKE-EVIDENCE",
            ),
            "CALLABLE-TOOL-OVERLAY": (
                "CALLABLE-TOOL-OR-PLUGIN-USE",
                {"API-120"},
                "CALLABLE-TOOL-EVIDENCE",
            ),
            "INFRASTRUCTURE-DEPENDENCY-INTAKE-OVERLAY": (
                "UNTRUSTED-INFRASTRUCTURE-DEPENDENCY-INTAKE",
                {"INF-120"},
                "INFRASTRUCTURE-DEPENDENCY-INTAKE-EVIDENCE",
            ),
            "MODEL-RETIREMENT-OVERLAY": (
                "UNSUPPORTED-MODEL-PRESENCE",
                {"MOD-150"},
                "MODEL-RETIREMENT-EVIDENCE",
            ),
            "UNSUPPORTED-INFRASTRUCTURE-OVERLAY": (
                "UNSUPPORTED-INFRASTRUCTURE-COMPONENT-PRESENCE",
                {"INF-120"},
                "UNSUPPORTED-INFRASTRUCTURE-EVIDENCE",
            ),
            "UNSUPPORTED-TECHNOLOGY-OVERLAY": (
                "UNSUPPORTED-TECHNOLOGY-COMPONENT-PRESENCE",
                {"ARC-150"},
                "UNSUPPORTED-TECHNOLOGY-EVIDENCE",
            ),
            "EXTERNAL-RESPONSIBILITY-OVERLAY": (
                "EXTERNAL-PROVIDER-USE",
                {"CMP-120", "ARC-140"},
                "EXTERNAL-RESPONSIBILITY-EVIDENCE",
            ),
            "EXTERNAL-AI-SERVICE-INTEGRATION-OVERLAY": (
                "EXTERNAL-AI-SERVICE-INTEGRATION",
                {"API-140"},
                "EXTERNAL-AI-SERVICE-INTEGRATION-EVIDENCE",
            ),
            "MATERIAL-DEPENDENCY-OVERLAY": (
                "MATERIAL-EXTERNAL-PROVIDER-DEPENDENCY",
                {"API-150"},
                "MATERIAL-DEPENDENCY-EVIDENCE",
            ),
            "THIRD-PARTY-ADMINISTRATION-OVERLAY": (
                "THIRD-PARTY-ADMINISTRATION",
                {
                    "IAM-130",
                    "IAM-140",
                    "IAM-150",
                    "INF-130",
                    "CMP-120",
                    "ARC-140",
                },
                "THIRD-PARTY-ADMINISTRATION-EVIDENCE",
            ),
        }
        risk_document = self.load("risk-overlays.json")
        risks = {
            risk["risk_id"]: risk for risk in risk_document["risks"]
        }
        overlays = {
            overlay["overlay_id"]: overlay for overlay in risk_document["overlays"]
        }
        expectations = self.records_by_id(
            "evidence-expectations.json", "expectations", "expectation_id"
        )
        selections = self.records_by_id(
            "control-selections.json", "selections", "control_id"
        )
        conditional_overlays = {
            overlay_id: overlay
            for overlay_id, overlay in overlays.items()
            if overlay["applicability"] == "conditional"
        }
        self.assertEqual(set(conditional_overlays), set(expected))
        self.assertEqual(
            {
                expectation_id
                for expectation_id, expectation in expectations.items()
                if expectation.get("activation_conditions")
            },
            {expectation_id for _, _, expectation_id in expected.values()},
        )
        for overlay_id, (
            condition_id,
            control_ids,
            expectation_id,
        ) in expected.items():
            with self.subTest(overlay=overlay_id):
                overlay = overlays[overlay_id]
                self.assertEqual(overlay["activation_conditions"], [condition_id])
                self.assertEqual(set(overlay["affected_controls"]), control_ids)
                self.assertEqual(
                    overlay["evidence_expectation_ids"], [expectation_id]
                )
                expectation = expectations[expectation_id]
                self.assertEqual(
                    expectation["activation_conditions"], [condition_id]
                )
                self.assertEqual(set(expectation["control_ids"]), control_ids)
                self.assertEqual(expectation["overlay_ids"], [overlay_id])
                for risk_id in overlay["risk_ids"]:
                    self.assertIn(overlay_id, risks[risk_id]["overlay_ids"])
                for control_id in control_ids:
                    selection = selections[control_id]
                    self.assertTrue(
                        selection["status"] == "required"
                        or (
                            selection["status"] == "conditional"
                            and condition_id
                            in selection.get("activation_conditions", [])
                        ),
                        f"{control_id} is not applicable under {condition_id}",
                    )
                    if (
                        selection["status"] == "conditional"
                        and len(selection["activation_conditions"]) == 1
                    ):
                        self.assertEqual(
                            selection["activation_conditions"],
                            [condition_id],
                            f"{control_id} and {overlay_id} use different "
                            "single-condition applicability",
                        )

    def test_every_overlay_control_is_covered_by_a_linked_risk(self) -> None:
        risk_document = self.load("risk-overlays.json")
        risks = {
            risk["risk_id"]: risk for risk in risk_document["risks"]
        }
        for overlay in risk_document["overlays"]:
            linked_risks = [
                risks[risk_id] for risk_id in overlay["risk_ids"]
            ]
            for control_id in overlay["affected_controls"]:
                with self.subTest(
                    overlay=overlay["overlay_id"],
                    control=control_id,
                ):
                    self.assertTrue(
                        any(
                            control_id
                            in {
                                *risk["source_basis"],
                                *risk["affected_controls"],
                            }
                            for risk in linked_risks
                        ),
                        f"{control_id} has no source or affected-control "
                        f"coverage in risks linked to {overlay['overlay_id']}",
                    )

    def test_iam_140_and_authenticated_administration_are_fully_linked(
        self,
    ) -> None:
        risks = self.records_by_id("risk-overlays.json", "risks", "risk_id")
        overlays = self.records_by_id(
            "risk-overlays.json", "overlays", "overlay_id"
        )
        expectations = self.records_by_id(
            "evidence-expectations.json", "expectations", "expectation_id"
        )

        privileged_risk = risks["PRIVILEGED-CONFIGURATION-RISK"]
        self.assertIn("IAM-140", privileged_risk["source_basis"])
        self.assertIn("IAM-140", privileged_risk["affected_controls"])

        third_party_overlay = overlays["THIRD-PARTY-ADMINISTRATION-OVERLAY"]
        third_party_evidence = expectations[
            "THIRD-PARTY-ADMINISTRATION-EVIDENCE"
        ]
        self.assertIn("IAM-140", third_party_overlay["affected_controls"])
        self.assertIn("IAM-140", third_party_evidence["control_ids"])

        exposure_overlay = overlays["EXPOSED-BOUNDARY-OVERLAY"]
        exposure_evidence = expectations["BOUNDARY-EXPOSURE-EVIDENCE"]
        exposed_risk = risks["EXPOSED-INFRASTRUCTURE-RISK"]
        self.assertIn(
            "authenticated administration",
            exposure_overlay["statement"].lower(),
        )
        for control_id in ("IAM-110", "IAM-130"):
            with self.subTest(control=control_id):
                self.assertIn(
                    control_id, exposure_overlay["affected_controls"]
                )
                self.assertIn(control_id, exposure_evidence["control_ids"])
                self.assertIn(control_id, exposed_risk["source_basis"])
                self.assertIn(control_id, exposed_risk["affected_controls"])

    def test_external_responsibility_chain_is_generic_but_api_150_is_material(
        self,
    ) -> None:
        risks = self.records_by_id("risk-overlays.json", "risks", "risk_id")
        overlays = self.records_by_id(
            "risk-overlays.json", "overlays", "overlay_id"
        )
        expectations = self.records_by_id(
            "evidence-expectations.json", "expectations", "expectation_id"
        )
        conditions = {
            condition["condition_id"]: condition
            for condition in self.load("profile.json")["applicability_conditions"]
        }
        generic_chain = " ".join(
            (
                conditions["EXTERNAL-PROVIDER-USE"]["question"],
                risks["EXTERNAL-RESPONSIBILITY-RISK"]["statement"],
                risks["EXTERNAL-RESPONSIBILITY-RISK"]["circumstances"],
                overlays["EXTERNAL-RESPONSIBILITY-OVERLAY"]["statement"],
                overlays["EXTERNAL-RESPONSIBILITY-OVERLAY"][
                    "strengthening_rationale"
                ],
                expectations["EXTERNAL-RESPONSIBILITY-EVIDENCE"]["purpose"],
                expectations["EXTERNAL-RESPONSIBILITY-EVIDENCE"]["strengthening"],
            )
        ).lower()
        self.assertNotRegex(
            generic_chain,
            r"\bmaterial (?:external )?(?:provider|service|operation)\b",
        )
        selections = self.records_by_id(
            "control-selections.json", "selections", "control_id"
        )
        self.assertEqual(
            selections["API-150"]["activation_conditions"],
            ["MATERIAL-EXTERNAL-PROVIDER-DEPENDENCY"],
        )

    def test_model_retirement_chain_covers_every_mod_150_state(self) -> None:
        states = (
            "end-of-life",
            "replaced",
            "unsupported",
            "compromised",
            "nonconforming",
            "expired",
            "abandoned",
        )
        conditions = {
            condition["condition_id"]: condition
            for condition in self.load("profile.json")["applicability_conditions"]
        }
        risk_document = self.load("risk-overlays.json")
        risks = {
            risk["risk_id"]: risk for risk in risk_document["risks"]
        }
        overlay = next(
            record
            for record in risk_document["overlays"]
            if record.get("activation_conditions")
            == ["UNSUPPORTED-MODEL-PRESENCE"]
            and record["affected_controls"] == ["MOD-150"]
        )
        self.assertEqual(len(overlay["risk_ids"]), 1)
        risk = risks[overlay["risk_ids"][0]]
        expectations = self.records_by_id(
            "evidence-expectations.json", "expectations", "expectation_id"
        )
        self.assertEqual(len(overlay["evidence_expectation_ids"]), 1)
        expectation = expectations[overlay["evidence_expectation_ids"][0]]

        for record_name, text in (
            (
                "condition question",
                conditions["UNSUPPORTED-MODEL-PRESENCE"]["question"],
            ),
            ("risk circumstances", risk["circumstances"]),
            ("overlay statement", overlay["statement"]),
            ("overlay strengthening", overlay["strengthening_rationale"]),
            ("evidence purpose", expectation["purpose"]),
            ("evidence strengthening", expectation["strengthening"]),
        ):
            for state in states:
                with self.subTest(record=record_name, state=state):
                    self.assertIn(state, text.lower())

        with self.subTest(record="risk identifier"):
            self.assertEqual(risk["risk_id"], "LIFECYCLE-DISPOSITION-RISK")
        with self.subTest(record="overlay identifier"):
            self.assertEqual(
                overlay["overlay_id"], "MODEL-RETIREMENT-OVERLAY"
            )
        with self.subTest(record="evidence identifier"):
            self.assertEqual(
                expectation["expectation_id"],
                "MODEL-RETIREMENT-EVIDENCE",
            )
        self.assertIn(
            "unsupported or end-of-life infrastructure",
            risk["circumstances"].lower(),
        )
        self.assertIn(
            "unsupported, end-of-life, or out-of-window ai technology",
            risk["circumstances"].lower(),
        )
        self.assertIn("MOD-150", " ".join(risk["source_basis"]))

    def test_risk_source_basis_uses_only_closed_source_references(self) -> None:
        expected = {
            "EXPOSED-INFRASTRUCTURE-RISK": {
                "APP-150",
                "API-110",
                "IAM-110",
                "IAM-130",
                "INF-110",
                "INF-120",
                "INF-140",
                "INF-150",
                "MON-110",
            },
            "PRIVILEGED-CONFIGURATION-RISK": {
                "IAM-120",
                "IAM-130",
                "IAM-140",
                "IAM-150",
                "INF-110",
                "INF-130",
                "MON-150",
            },
            "LIFECYCLE-DISPOSITION-RISK": {
                "MOD-150",
                "INF-120",
                "ARC-150",
            },
            "UNTRUSTED-SOFTWARE-RISK": {
                "MOD-110",
                "APP-140",
                "API-120",
                "INF-120",
            },
            "EXTERNAL-RESPONSIBILITY-RISK": {
                "API-140",
                "CMP-120",
                "ARC-140",
                "IAM-130",
                "IAM-150",
            },
            "MATERIAL-DEPENDENCY-RISK": {"API-150"},
            "INCOMPLETE-SCOPE-EVIDENCE-RISK": {
                "GOV-130",
                "RSK-110",
                "IAM-100",
                "MOD-100",
                "INF-100",
                "AUD-120",
                "ARC-110",
                "ESAF",
            },
        }
        risks = self.records_by_id("risk-overlays.json", "risks", "risk_id")
        self.assertEqual(set(risks), set(expected))
        for risk_id, source_basis in expected.items():
            with self.subTest(risk=risk_id):
                self.assertEqual(set(risks[risk_id]["source_basis"]), source_basis)

    def test_selection_rationales_do_not_embed_stale_condition_counts(self) -> None:
        selections = self.load("control-selections.json")["selections"]
        for selection in selections:
            with self.subTest(control=selection["control_id"]):
                self.assertNotRegex(
                    selection["rationale"].lower(),
                    r"\b(?:five|5)\b[^.]{0,80}\bconditions?\b",
                )
        by_id = {
            selection["control_id"]: selection for selection in selections
        }
        for control_id in ("STR-130", "APP-110", "AGT-100"):
            self.assertIn(
                "bounded profile conditions",
                by_id[control_id]["rationale"].lower(),
            )

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

    def test_not_selected_rationales_are_non_normative(self) -> None:
        selections = self.load("control-selections.json")["selections"]
        for record in selections:
            if record["status"] == "not_selected":
                with self.subTest(control=record["control_id"]):
                    self.assertNotRegex(
                        record["rationale"],
                        r"(?i)\b(shall|should|must)\b",
                    )

    def test_change_history_has_one_consolidated_0_1_0_entry(self) -> None:
        history = self.load("profile.json")["change_history"]
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["version"], "0.1.0")
        description = history[0]["description"]
        for phrase in (
            "Initial Draft United Kingdom pilot profile",
            "mapping-source boundaries",
            "normalized conditional overlays",
            "internet-reachable API condition",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, description)

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
                    reference["registry_path"],
                    f"crosswalks/registry/{reference['mapping_set_id']}.md",
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
