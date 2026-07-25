from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests import profile_fixture
from tools import validate_profiles


class ProfileValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.package = profile_fixture.write_valid_profile_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def load_component(self, filename: str) -> dict[str, object]:
        return json.loads((self.package / filename).read_text(encoding="utf-8"))

    def write_component(
        self, filename: str, document: dict[str, object]
    ) -> None:
        (self.package / filename).write_text(
            json.dumps(document, indent=2) + "\n",
            encoding="utf-8",
        )

    def assert_has_error(self, expected: str) -> None:
        diagnostics = validate_profiles.validate(self.root)
        self.assertTrue(
            any(expected in error for error in diagnostics),
            f"missing {expected!r} in diagnostics:\n"
            + "\n".join(diagnostics),
        )

    def loaded_package(self) -> validate_profiles.ProfilePackage:
        diagnostics: list[str] = []
        package = validate_profiles.load_package(
            self.root, self.package, diagnostics
        )
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(package)
        assert package is not None
        return package

    def write_closed_trace_fixture(self) -> str:
        selections = self.load_component("control-selections.json")
        control_id = selections["selections"][0]["control_id"]
        self.write_component(
            "risk-overlays.json",
            {
                "$schema": "../../schema/risk-overlays.schema.json",
                "schema_version": profile_fixture.PROFILE_VERSION,
                "profile_id": profile_fixture.PROFILE_ID,
                "profile_version": profile_fixture.PROFILE_VERSION,
                "risks": [
                    {
                        "risk_id": "RISK-A",
                        "statement": "Synthetic risk.",
                        "circumstances": "Synthetic circumstances.",
                        "source_basis": ["ESAF"],
                        "affected_controls": [control_id],
                        "overlay_ids": ["OVERLAY-A"],
                    }
                ],
                "overlays": [
                    {
                        "overlay_id": "OVERLAY-A",
                        "statement": "Synthetic strengthening.",
                        "applicability": "universal",
                        "affected_controls": [control_id],
                        "risk_ids": ["RISK-A"],
                        "evidence_expectation_ids": ["EVIDENCE-A"],
                        "strengthening_rationale": "Preserves core meaning.",
                    }
                ],
            },
        )
        self.write_component(
            "evidence-expectations.json",
            {
                "$schema": "../../schema/evidence-expectations.schema.json",
                "schema_version": profile_fixture.PROFILE_VERSION,
                "profile_id": profile_fixture.PROFILE_ID,
                "profile_version": profile_fixture.PROFILE_VERSION,
                "expectations": [
                    {
                        "expectation_id": "EVIDENCE-A",
                        "purpose": "Synthetic evidence purpose.",
                        "artifact_class": "Synthetic artifact.",
                        "overlay_ids": ["OVERLAY-A"],
                        "quality_attributes": ["relevance"],
                    }
                ],
            },
        )
        return control_id

    def test_valid_population_has_no_errors(self) -> None:
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_control_population_is_loaded_from_authoritative_catalog(self) -> None:
        catalog = json.loads(
            (self.root / "controls/catalog.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            validate_profiles.control_population(self.root),
            {record["id"] for record in catalog["controls"]},
        )

    def test_missing_control_selection_is_rejected(self) -> None:
        document = self.load_component("control-selections.json")
        missing = document["selections"].pop()["control_id"]
        self.write_component("control-selections.json", document)
        self.assert_has_error(f"missing control selection {missing}")

    def test_duplicate_control_selection_is_rejected(self) -> None:
        document = self.load_component("control-selections.json")
        duplicate = dict(document["selections"][0])
        duplicate["rationale"] = "A second record with the same identifier."
        document["selections"].append(duplicate)
        self.write_component("control-selections.json", document)
        self.assert_has_error(
            f"duplicate control selection {duplicate['control_id']}"
        )

    def test_duplicate_condition_identifier_is_rejected(self) -> None:
        document = self.load_component("profile.json")
        duplicate = dict(document["applicability_conditions"][0])
        duplicate["question"] = "A different question with the same identifier?"
        document["applicability_conditions"].append(duplicate)
        self.write_component("profile.json", document)
        self.assert_has_error("duplicate applicability condition INACTIVE-FACT")

    def test_duplicate_risk_identifier_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("risk-overlays.json")
        duplicate = dict(document["risks"][0])
        duplicate["statement"] = "A second risk with the same identifier."
        document["risks"].append(duplicate)
        self.write_component("risk-overlays.json", document)
        self.assert_has_error("duplicate risk RISK-A")

    def test_duplicate_overlay_identifier_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("risk-overlays.json")
        duplicate = dict(document["overlays"][0])
        duplicate["statement"] = "A second overlay with the same identifier."
        document["overlays"].append(duplicate)
        self.write_component("risk-overlays.json", document)
        self.assert_has_error("duplicate overlay OVERLAY-A")

    def test_duplicate_evidence_identifier_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("evidence-expectations.json")
        duplicate = dict(document["expectations"][0])
        duplicate["purpose"] = "A second purpose with the same identifier."
        document["expectations"].append(duplicate)
        self.write_component("evidence-expectations.json", document)
        self.assert_has_error("duplicate evidence expectation EVIDENCE-A")

    def test_undefined_selection_condition_is_rejected(self) -> None:
        document = self.load_component("control-selections.json")
        document["selections"][0]["status"] = "conditional"
        document["selections"][0]["activation_conditions"] = ["UNKNOWN-FACT"]
        self.write_component("control-selections.json", document)
        self.assert_has_error("unresolved applicability condition UNKNOWN-FACT")

    def test_undefined_overlay_condition_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("risk-overlays.json")
        document["overlays"][0]["applicability"] = "conditional"
        document["overlays"][0]["activation_conditions"] = ["UNKNOWN-FACT"]
        self.write_component("risk-overlays.json", document)
        self.assert_has_error("unresolved applicability condition UNKNOWN-FACT")

    def test_unresolved_risk_overlay_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("risk-overlays.json")
        document["risks"][0]["overlay_ids"] = ["OVERLAY-MISSING"]
        self.write_component("risk-overlays.json", document)
        self.assert_has_error("unresolved overlay reference OVERLAY-MISSING")

    def test_unresolved_overlay_risk_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("risk-overlays.json")
        document["overlays"][0]["risk_ids"] = ["RISK-MISSING"]
        self.write_component("risk-overlays.json", document)
        self.assert_has_error("unresolved risk reference RISK-MISSING")

    def test_unresolved_overlay_evidence_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("risk-overlays.json")
        document["overlays"][0]["evidence_expectation_ids"] = [
            "EVIDENCE-MISSING"
        ]
        self.write_component("risk-overlays.json", document)
        self.assert_has_error(
            "unresolved evidence expectation reference EVIDENCE-MISSING"
        )

    def test_unresolved_evidence_overlay_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("evidence-expectations.json")
        document["expectations"][0]["overlay_ids"] = ["OVERLAY-MISSING"]
        self.write_component("evidence-expectations.json", document)
        self.assert_has_error("unresolved overlay reference OVERLAY-MISSING")

    def test_unknown_traceability_control_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("risk-overlays.json")
        document["risks"][0]["affected_controls"] = ["UNKNOWN-999"]
        self.write_component("risk-overlays.json", document)
        self.assert_has_error("unresolved control reference UNKNOWN-999")

    def test_asymmetric_overlay_evidence_link_is_rejected(self) -> None:
        control_id = self.write_closed_trace_fixture()
        document = self.load_component("evidence-expectations.json")
        document["expectations"][0]["control_ids"] = [control_id]
        del document["expectations"][0]["overlay_ids"]
        self.write_component("evidence-expectations.json", document)
        self.assert_has_error(
            "overlay OVERLAY-A and evidence expectation EVIDENCE-A "
            "must reference each other"
        )

    def test_asymmetric_risk_overlay_link_is_rejected(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("risk-overlays.json")
        document["overlays"][0]["risk_ids"] = ["RISK-MISSING"]
        self.write_component("risk-overlays.json", document)
        self.assert_has_error(
            "risk RISK-A and overlay OVERLAY-A must reference each other"
        )

    def test_exact_registry_metadata_is_loaded_as_draft(self) -> None:
        mapping_set_id, registry_path = profile_fixture.MAPPING_REFERENCES[0]
        metadata = validate_profiles.registry_metadata(
            self.root / registry_path
        )
        self.assertEqual(metadata["mapping_set_id"], mapping_set_id)
        self.assertEqual(metadata["status"], "draft")

    def test_wrong_mapping_registry_path_is_rejected(self) -> None:
        document = self.load_component("external-references.json")
        document["external_references"][0]["registry_path"] = (
            "crosswalks/registry/wrong.md"
        )
        self.write_component("external-references.json", document)
        self.assert_has_error("registry path must be")

    def test_non_draft_mapping_expectation_is_rejected(self) -> None:
        document = self.load_component("external-references.json")
        document["external_references"][0]["expected_status"] = "approved"
        self.write_component("external-references.json", document)
        self.assert_has_error("expected_status must be 'draft'")

    def test_mapping_reference_must_deny_imported_outcomes(self) -> None:
        document = self.load_component("external-references.json")
        document["external_references"][0]["non_import_statement"] = (
            "Relationships, external outcomes, and evidence are imported."
        )
        self.write_component("external-references.json", document)
        self.assert_has_error("non_import_statement must be")

    def test_mapping_registry_lifecycle_drift_is_rejected(self) -> None:
        _, registry_path = profile_fixture.MAPPING_REFERENCES[0]
        path = self.root / registry_path
        text = path.read_text(encoding="utf-8").replace(
            "events: []",
            "events:\n  - state: approved",
            1,
        )
        path.write_text(text, encoding="utf-8", newline="\n")
        self.assert_has_error("registry lifecycle status is 'approved'")

    def test_registry_os_error_does_not_disclose_host_path(self) -> None:
        with mock.patch.object(
            validate_profiles,
            "registry_metadata",
            side_effect=OSError(f"cannot read {self.root}"),
        ):
            diagnostics = validate_profiles.validate(self.root)
        matching = [
            error
            for error in diagnostics
            if "cannot load registry metadata" in error
        ]
        self.assertTrue(matching, diagnostics)
        self.assertTrue(
            all(str(self.root) not in error for error in matching),
            matching,
        )

    def test_fourth_mapping_reference_is_rejected(self) -> None:
        document = self.load_component("external-references.json")
        extra = dict(document["external_references"][0])
        extra["mapping_set_id"] = (
            "uk-ncsc--unapproved-mapping--1.0--esaf-0.4-alpha--0.1.0"
        )
        extra["registry_path"] = "crosswalks/registry/unapproved.md"
        document["external_references"].append(extra)
        self.write_component("external-references.json", document)
        self.assert_has_error("unexpected mapping reference")

    def test_imported_relationship_fields_are_rejected_at_any_depth(self) -> None:
        package = self.loaded_package()
        references = package.documents["external_references"][
            "external_references"
        ]
        references[0]["nested_import"] = {
            "supported-outcome": {"relationships": []}
        }
        diagnostics = validate_profiles.claim_diagnostics(package)
        self.assertTrue(
            any(
                "prohibited external-reference field 'supported-outcome'"
                in error
                for error in diagnostics
            ),
            diagnostics,
        )
        self.assertTrue(
            any(
                "prohibited external-reference field 'relationships'"
                in error
                for error in diagnostics
            ),
            diagnostics,
        )

    def test_core_control_replacement_or_waiver_language_is_rejected(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile replaces core control requirements and waives them.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited control weakening language")

    def test_core_control_inapplicable_language_is_rejected(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile marks a core control inapplicable.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited control weakening language")

    def test_contrast_does_not_mask_affirmative_control_weakening(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile does not preserve core controls, "
            "but replaces core controls.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited control weakening language")

    def test_unrelated_denial_does_not_mask_later_control_weakening(self) -> None:
        for conjunction in ("and", ", and"):
            with self.subTest(conjunction=conjunction):
                (self.package / "README.md").write_text(
                    "# Synthetic profile\n\n"
                    "This profile does not replace its title "
                    f"{conjunction} replaces core controls.\n",
                    encoding="utf-8",
                )
                self.assert_has_error("prohibited control weakening language")

    def test_common_affirmative_control_weakening_is_rejected(self) -> None:
        for text in (
            "This profile replaces core controls.",
            "This profile alters core controls.",
            "This profile relaxes core control requirements.",
            "This profile makes core controls optional.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error("prohibited control weakening language")

    def test_passive_affirmative_control_weakening_is_rejected(self) -> None:
        for text in (
            "Core controls are replaced by this profile.",
            "Core control requirements are waived by this profile.",
            "Core controls are made optional by this profile.",
            "Core controls are altered by this profile.",
            "Core controls are relaxed by this profile.",
            "Core controls are weakened by this profile.",
            "Core controls are narrowed by this profile.",
            "Core controls are marked inapplicable by this profile.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error("prohibited control weakening language")

    def test_passive_control_weakening_denials_are_allowed(self) -> None:
        for text in (
            "Core controls are not replaced by this profile.",
            "Core control requirements are not waived by this profile.",
            "Core controls are not made optional by this profile.",
            "Core controls are not altered by this profile.",
            "Core controls are not relaxed by this profile.",
            "Core controls are not weakened by this profile.",
            "Core controls are not narrowed by this profile.",
            "Core controls are not marked inapplicable by this profile.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_passive_control_weakening_quotations_are_allowed(self) -> None:
        for phrase in (
            "Core controls are replaced by this profile",
            "Core control requirements are waived by this profile",
            "Core controls are made optional by this profile",
            "Core controls are altered by this profile",
            "Core controls are relaxed by this profile",
            "Core controls are weakened by this profile",
            "Core controls are narrowed by this profile",
            "Core controls are marked inapplicable by this profile",
        ):
            with self.subTest(phrase=phrase):
                (self.package / "README.md").write_text(
                    "# Synthetic profile\n\n"
                    f'The phrase "{phrase}" is prohibited.\n',
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_explicit_control_weakening_denials_are_allowed(self) -> None:
        for text in (
            "This profile does not replace core controls.",
            "No profile alters core controls.",
            "This profile does not relax or make core controls optional.",
            "This profile replaces no core controls.",
            "This profile replaces neither core control.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_profile_local_maturity_scale_is_rejected(self) -> None:
        package = self.loaded_package()
        package.documents["profile"]["nested"] = {
            "maturity_scale": ["local-one", "local-two"]
        }
        diagnostics = validate_profiles.claim_diagnostics(package)
        self.assertTrue(
            any("profile-local maturity field" in error for error in diagnostics),
            diagnostics,
        )

    def test_positive_prohibited_claim_is_rejected(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\nThis profile establishes compliance.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited assertion 'establishes compliance'")

    def test_profile_specific_positive_claims_are_rejected(self) -> None:
        for text, expected in (
            ("This profile is legally sufficient.", "legal sufficiency"),
            ("This profile has external approval.", "external approval"),
            ("This profile is production ready.", "production readiness"),
            ("This profile certifies compliance.", "compliance"),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error(f"prohibited assertion '{expected}'")

    def test_common_affirmative_profile_claim_variants_are_rejected(self) -> None:
        for text, expected in (
            ("This profile provides legal sufficiency.", "legal sufficiency"),
            ("This profile is externally approved.", "external approval"),
            (
                "This profile demonstrates production readiness.",
                "production readiness",
            ),
            ("This profile is ready for production.", "production readiness"),
            ("This profile is compliant.", "compliance"),
            ("This profile is certified.", "certification"),
            ("This profile is equivalent.", "equivalence"),
            ("This profile is endorsed.", "endorsement"),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error(f"prohibited assertion '{expected}'")

    def test_establishes_profile_claim_variants_are_rejected(self) -> None:
        for text, expected in (
            (
                "This profile establishes legal sufficiency.",
                "legal sufficiency",
            ),
            (
                "This profile establishes external approval.",
                "external approval",
            ),
            (
                "This profile establishes production readiness.",
                "production readiness",
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error(f"prohibited assertion '{expected}'")

    def test_establishes_profile_claim_denials_are_allowed(self) -> None:
        for outcome in (
            "legal sufficiency",
            "external approval",
            "production readiness",
        ):
            with self.subTest(outcome=outcome):
                (self.package / "README.md").write_text(
                    "# Synthetic profile\n\n"
                    f"This profile does not establish {outcome}.\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_establishes_profile_claim_quotations_are_allowed(self) -> None:
        for phrase in (
            "establishes legal sufficiency",
            "establishes external approval",
            "establishes production readiness",
        ):
            with self.subTest(phrase=phrase):
                (self.package / "README.md").write_text(
                    "# Synthetic profile\n\n"
                    f'The phrase "{phrase}" is prohibited.\n',
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_explicit_claim_denial_is_allowed(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile does not establish compliance.\n",
            encoding="utf-8",
        )
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_profile_specific_claim_denials_are_allowed(self) -> None:
        for text in (
            "This profile is not legally sufficient.",
            "This profile does not have external approval.",
            "This profile is not production ready.",
            "This profile does not certify compliance.",
            "This profile is not certified.",
            "This profile is not equivalent.",
            "This profile is not endorsed.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_metalinguistic_claim_quotation_is_allowed(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            'The phrase "establishes compliance" is prohibited.\n',
            encoding="utf-8",
        )
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_profile_specific_claim_quotations_are_allowed(self) -> None:
        for phrase in (
            "legally sufficient",
            "has external approval",
            "production ready",
            "certifies compliance",
            "is compliant",
            "is certified",
            "is equivalent",
            "is endorsed",
        ):
            with self.subTest(phrase=phrase):
                (self.package / "README.md").write_text(
                    "# Synthetic profile\n\n"
                    f'The phrase "{phrase}" is prohibited.\n',
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_semantic_diagnostic_ordering_is_stable(self) -> None:
        selections = self.load_component("control-selections.json")
        duplicate = dict(selections["selections"][0])
        duplicate["rationale"] = "Duplicate."
        selections["selections"].append(duplicate)
        selections["selections"].pop(1)
        self.write_component("control-selections.json", selections)
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\nThis profile establishes equivalence.\n",
            encoding="utf-8",
        )
        diagnostics = validate_profiles.validate(self.root)
        self.assertEqual(diagnostics, sorted(set(diagnostics)))

    def test_duplicate_json_key_is_rejected(self) -> None:
        path = self.package / "profile.json"
        text = path.read_text(encoding="utf-8").replace(
            '"profile_version":',
            '"profile_version": "duplicate",\n"profile_version":',
            1,
        )
        path.write_text(text, encoding="utf-8")
        self.assertTrue(
            any("duplicate JSON key" in error for error in validate_profiles.validate(self.root))
        )

    def test_malformed_json_syntax_is_rejected_directly(self) -> None:
        path = self.package / "risk-overlays.json"
        path.write_text('{"risks": [}\n', encoding="utf-8")
        self.assert_has_error("cannot load JSON")

    def test_unlisted_package_file_is_rejected(self) -> None:
        (self.package / "unlisted.json").write_text("{}\n", encoding="utf-8")
        self.assertTrue(
            any("unlisted package file" in error for error in validate_profiles.validate(self.root))
        )

    def test_rogue_package_directory_is_rejected(self) -> None:
        (self.package / "rogue").mkdir()
        self.assertTrue(
            any("unlisted package entry rogue" in error for error in validate_profiles.validate(self.root))
        )

    def test_missing_profile_manifest_is_rejected(self) -> None:
        (self.package / "profile.json").unlink()
        self.assertTrue(
            any("missing package file profile.json" in error for error in validate_profiles.validate(self.root))
        )

    def test_missing_component_is_rejected(self) -> None:
        (self.package / "evidence-expectations.json").unlink()
        self.assertTrue(
            any(
                "missing package file evidence-expectations.json" in error
                for error in validate_profiles.validate(self.root)
            )
        )

    def test_schema_directory_is_not_a_profile_country(self) -> None:
        false_package = self.root / "profiles" / "schema" / "0.1.0"
        false_package.mkdir()
        (false_package / "profile.json").write_text("{}\n", encoding="utf-8")
        self.assertEqual(
            validate_profiles.discover_profile_packages(self.root), (self.package,)
        )

    def test_safe_component_rejects_path_aliases(self) -> None:
        for relative in (
            "nested/./component.json",
            "nested//component.json",
            "nested/../component.json",
            r"nested\component.json",
            "/absolute/component.json",
            "component.json/",
        ):
            with self.subTest(relative=relative):
                self.assertIsNone(validate_profiles.safe_component(self.package, relative))

    def test_diagnostics_are_deterministic_and_repository_relative(self) -> None:
        additional = self.root / "profiles" / "aa" / "0.1.0"
        shutil.copytree(self.package, additional)
        (self.package / "z.txt").write_text("fixture\n", encoding="utf-8")
        (additional / "a.txt").write_text("fixture\n", encoding="utf-8")
        diagnostics = validate_profiles.validate(self.root)
        self.assertEqual(diagnostics, sorted(diagnostics))
        self.assertTrue(all(str(self.root) not in error for error in diagnostics))

    def test_symlinked_country_directory_is_rejected(self) -> None:
        country = self.package.parent
        outside_country = self.root / "outside" / country.name
        outside_country.parent.mkdir()
        shutil.move(str(country), outside_country)
        try:
            os.symlink(outside_country, country, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symlink creation is unavailable: {exc}")
        self.assertTrue(
            any("symlink" in error for error in validate_profiles.validate(self.root))
        )

    def test_symlinked_schema_file_is_rejected(self) -> None:
        schema = self.root / "profiles/schema/profile.schema.json"
        target = self.root / "profile.schema.target.json"
        shutil.move(schema, target)
        try:
            os.symlink(target, schema)
        except OSError as exc:
            self.skipTest(f"symlink creation is unavailable: {exc}")
        self.assertTrue(
            any("schema root or file" in error for error in validate_profiles.validate(self.root))
        )

    def test_symlinked_schema_directory_is_rejected(self) -> None:
        schema_root = self.root / "profiles/schema"
        target = self.root / "schema-target"
        shutil.move(schema_root, target)
        try:
            os.symlink(target, schema_root, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symlink creation is unavailable: {exc}")
        self.assertTrue(
            any("schema root or file" in error for error in validate_profiles.validate(self.root))
        )

    def test_invalid_component_schema_does_not_load_package(self) -> None:
        path = self.package / "risk-overlays.json"
        path.write_text("[]\n", encoding="utf-8")
        diagnostics: list[str] = []
        package = validate_profiles.load_package(self.root, self.package, diagnostics)
        self.assertIsNone(package)
        self.assertTrue(any("risk-overlays.json" in error for error in diagnostics))

    def test_cli_requires_check_and_reports_success(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 0)
        self.assertIn("Successfully validated 1 profile package", output.getvalue())

    def test_cli_requires_check(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = validate_profiles.main([], root=self.root)
        self.assertEqual(result, 2)
        self.assertIn("--check", output.getvalue())

    def test_cli_reports_content_errors_with_exit_one(self) -> None:
        (self.package / "unexpected.txt").write_text("fixture\n", encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 1)
        self.assertIn("unexpected.txt", output.getvalue())

    def test_cli_reports_unresolvable_schema_reference_with_exit_two(self) -> None:
        path = self.root / "profiles/schema/profile.schema.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["allOf"] = [{"$ref": "missing.schema.json"}]
        path.write_text(json.dumps(schema), encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 2)
        self.assertIn("could not run", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
