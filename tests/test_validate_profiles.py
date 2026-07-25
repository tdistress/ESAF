from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from itertools import product
from pathlib import Path
from unittest import mock

from tests import profile_fixture
from tools import validate_profiles


AFFIRMATIVE_CLAIMS = (
    ("This profile satisfies Cyber Essentials requirements.", "scheme satisfaction"),
    ("This profile ensures legal compliance.", "compliance"),
    (
        "This profile confers certification eligibility.",
        "certification eligibility",
    ),
    ("This profile has NCSC approval.", "named-authority approval"),
    (
        "Cyber Essentials provision A maps to GOV-100 and supplies its "
        "external outcome.",
        "imported mapping relationship",
    ),
    (
        "Legal compliance is ensured by this profile.",
        "compliance",
    ),
    (
        "Certification eligibility is conferred by this profile.",
        "certification eligibility",
    ),
    (
        "NCSC approval is held by this profile.",
        "named-authority approval",
    ),
    (
        "GOV-100 is mapped from Cyber Essentials provision A and the external "
        "outcome is imported.",
        "imported mapping relationship",
    ),
    (
        "GOV-100 supports Cyber Essentials provision A.",
        "imported mapping relationship",
    ),
    (
        "GOV-100 satisfies Cyber Essentials provision A.",
        "imported mapping relationship",
    ),
    (
        "Cyber Essentials provision A is supported by GOV-100.",
        "imported mapping relationship",
    ),
    (
        "Cyber Essentials provision A is satisfied by GOV-100.",
        "imported mapping relationship",
    ),
    (
        "Cyber Essentials provision A supports GOV-100.",
        "imported mapping relationship",
    ),
    (
        "Cyber Essentials provision A satisfies GOV-100.",
        "imported mapping relationship",
    ),
    (
        "GOV-100 is supported by Cyber Essentials provision A.",
        "imported mapping relationship",
    ),
    (
        "GOV-100 is satisfied by Cyber Essentials provision A.",
        "imported mapping relationship",
    ),
    (
        "This profile meets Cyber Essentials requirements.",
        "scheme satisfaction",
    ),
    (
        "This profile complies with Cyber Essentials.",
        "compliance",
    ),
    (
        "This profile qualifies the organization for certification.",
        "certification eligibility",
    ),
    (
        "This profile is approved by NCSC.",
        "named-authority approval",
    ),
    (
        "NCSC approves this profile.",
        "named-authority approval",
    ),
)

AFFIRMATIVE_WEAKENING = (
    "This profile makes optional core controls.",
    "This profile marks inapplicable core controls.",
    "GOV-100 need not be applied.",
    "This profile supersedes GOV-100.",
    "The organization is exempt from GOV-100.",
    "This profile lowers core control requirements.",
    "GOV-100 is superseded by this profile.",
    "GOV-100 is inapplicable under this profile.",
    "Core control requirements are lowered by this profile.",
    "This profile renders GOV-100 optional.",
    "GOV-100 no longer applies.",
    "GOV-100 does not apply under this profile.",
)


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

    def write_readme(self, text: str) -> None:
        (self.package / "README.md").write_text(
            f"# Synthetic profile\n\n{text}\n",
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

    def generic_package(
        self,
        *,
        profile_id: str = "example--sector-profile--0.1.0",
        external_references: list[dict[str, object]] | None = None,
    ) -> validate_profiles.ProfilePackage:
        package = self.loaded_package()
        for document in package.documents.values():
            document["profile_id"] = profile_id
        if external_references is not None:
            package.documents["external_references"]["external_references"] = (
                external_references
            )
        return package

    def external_references(self) -> list[dict[str, object]]:
        document = self.load_component("external-references.json")
        references = document["external_references"]
        assert isinstance(references, list)
        return references

    def set_catalog_editorial_status(
        self, status: str, reference_index: int = 0
    ) -> None:
        mapping_set_id = profile_fixture.MAPPING_REFERENCES[reference_index][0]
        path = self.root / "crosswalks/catalog.json"
        catalog = json.loads(path.read_text(encoding="utf-8"))
        record = next(
            record
            for record in catalog["mapping_sets"]
            if record["metadata"]["mapping_set_id"] == mapping_set_id
        )
        record["metadata"]["status"] = status
        profile_fixture.write_json(path, catalog)

    def snapshot_path(self, reference_index: int = 0) -> Path:
        mapping_set_id = profile_fixture.MAPPING_REFERENCES[reference_index][0]
        catalog = json.loads(
            (self.root / "crosswalks/catalog.json").read_text(encoding="utf-8")
        )
        record = next(
            record
            for record in catalog["mapping_sets"]
            if record["metadata"]["mapping_set_id"] == mapping_set_id
        )
        return self.root / record["path"]

    def set_snapshot_editorial_status(
        self, status: str, reference_index: int = 0
    ) -> None:
        path = self.snapshot_path(reference_index)
        text = path.read_text(encoding="utf-8")
        for current in ("draft", "reviewed", "approved"):
            marker = f"status: {current}"
            if marker in text:
                path.write_text(
                    text.replace(marker, f"status: {status}", 1),
                    encoding="utf-8",
                    newline="\n",
                )
                return
        self.fail("snapshot has no editable editorial status")

    def set_editorial_status(
        self, status: str, reference_index: int = 0
    ) -> None:
        self.set_catalog_editorial_status(status, reference_index)
        self.set_snapshot_editorial_status(status, reference_index)

    def set_expected_status(
        self, status: str, reference_index: int = 0
    ) -> None:
        document = self.load_component("external-references.json")
        document["external_references"][reference_index]["expected_status"] = status
        self.write_component("external-references.json", document)

    def set_registry_events(
        self, states: list[str], reference_index: int = 0
    ) -> None:
        registry_path = profile_fixture.MAPPING_REFERENCES[reference_index][1]
        path = self.root / registry_path
        events = "\n".join(f"  - state: {state}" for state in states)
        replacement = f"events:\n{events}" if events else "events: []"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "events: []", replacement, 1
            ),
            encoding="utf-8",
            newline="\n",
        )

    def remove_valid_package(self) -> None:
        shutil.rmtree(self.package)

    def rewrite_all_profile_ids(self, profile_id: str) -> None:
        for filename in (
            "profile.json",
            "control-selections.json",
            "risk-overlays.json",
            "evidence-expectations.json",
            "external-references.json",
        ):
            document = self.load_component(filename)
            document["profile_id"] = profile_id
            self.write_component(filename, document)

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

    def test_zero_profile_packages_is_rejected(self) -> None:
        self.remove_valid_package()
        self.assertIn(
            "profiles: no profile packages found",
            validate_profiles.validate(self.root),
        )

    def test_invalid_profile_domain_version_entry_is_rejected(self) -> None:
        (self.root / "profiles" / "example" / "not-semver").mkdir(parents=True)
        self.assertTrue(
            any(
                "invalid profile version directory" in item
                for item in validate_profiles.validate(self.root)
            )
        )

    def test_invalid_profile_domain_directory_is_rejected(self) -> None:
        (self.root / "profiles" / "Invalid-Domain").mkdir()
        self.assert_has_error("invalid profile domain directory")

    def test_unexpected_profile_root_entry_is_rejected(self) -> None:
        (self.root / "profiles" / "unexpected.txt").write_text(
            "unexpected\n", encoding="utf-8"
        )
        self.assert_has_error("unexpected profile inventory entry")

    def test_missing_profile_root_is_rejected(self) -> None:
        shutil.rmtree(self.root / "profiles")
        diagnostics = validate_profiles.validate(self.root)
        self.assertIn("profiles: profile root is missing", diagnostics)
        self.assertIn("profiles: no profile packages found", diagnostics)

    def test_empty_profile_domain_is_rejected(self) -> None:
        (self.root / "profiles" / "empty-domain").mkdir()
        self.assert_has_error("profile domain contains no version entries")

    def test_profile_id_version_must_match_manifest_and_directory(self) -> None:
        self.rewrite_all_profile_ids("example--risk-profile--9.9.9")
        self.assertTrue(
            any(
                "profile_id version 9.9.9 does not match profile_version 0.1.0"
                in item
                for item in validate_profiles.validate(self.root)
            )
        )

    def test_non_pilot_semantic_version_is_valid_when_identity_and_directory_agree(
        self,
    ) -> None:
        self.package = profile_fixture.rewrite_profile_version(
            self.package, "1.2.3"
        )
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_invalid_calendar_date_is_rejected(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["change_history"][0]["date"] = "2026-02-30"
        self.write_component("profile.json", manifest)
        self.assertTrue(
            any(
                "is not a 'date'" in item
                for item in validate_profiles.validate(self.root)
            )
        )

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

    def test_exact_mapping_reference_metadata_uses_catalog_editorial_status(
        self,
    ) -> None:
        mapping_set_id, registry_path = profile_fixture.MAPPING_REFERENCES[0]
        metadata = validate_profiles.mapping_reference_metadata(
            self.root, mapping_set_id, registry_path
        )
        self.assertEqual(metadata["mapping_set_id"], mapping_set_id)
        self.assertEqual(metadata["editorial_status"], "draft")
        self.assertEqual(metadata["registry_events"], [])

    def test_generic_profile_may_have_no_external_references(self) -> None:
        package = self.generic_package(external_references=[])
        self.assertEqual(
            [],
            validate_profiles.semantic_diagnostics(self.root, package),
        )

    def test_future_profile_is_not_forced_to_use_uk_mappings(self) -> None:
        package = self.generic_package(
            profile_id="example--sector-profile--1.2.3",
            external_references=[],
        )
        diagnostics = validate_profiles.semantic_diagnostics(self.root, package)
        self.assertFalse(
            any("UK pilot mapping references" in item for item in diagnostics)
        )
        self.assertFalse(
            any("mapping reference" in item for item in diagnostics),
            diagnostics,
        )

    def test_generic_profile_may_declare_one_catalog_reference(self) -> None:
        reference = self.external_references()[0]
        package = self.generic_package(external_references=[reference])
        self.assertEqual(
            [],
            validate_profiles.semantic_diagnostics(self.root, package),
        )

    def test_uk_pilot_still_requires_exact_three_references(self) -> None:
        document = self.load_component("external-references.json")
        document["external_references"].pop()
        self.write_component("external-references.json", document)
        self.assertTrue(
            any(
                "exactly three" in item
                for item in validate_profiles.validate(self.root)
            )
        )

    def test_reviewed_snapshot_is_not_inferred_as_draft_from_empty_events(
        self,
    ) -> None:
        self.set_editorial_status("reviewed")
        package = self.generic_package(
            external_references=[self.external_references()[0]]
        )
        self.assertTrue(
            any(
                "expected editorial status draft; found reviewed" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_reviewed_snapshot_with_empty_events_is_valid(self) -> None:
        self.set_editorial_status("reviewed")
        self.set_expected_status("reviewed")
        package = self.generic_package(
            external_references=[self.external_references()[0]]
        )
        self.assertFalse(
            any(
                "lifecycle" in item or "editorial status" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_reviewed_snapshot_rejects_approved_registry_event(self) -> None:
        self.set_editorial_status("reviewed")
        self.set_expected_status("reviewed")
        self.set_registry_events(["approved"])
        package = self.generic_package(
            external_references=[self.external_references()[0]]
        )
        self.assertTrue(
            any(
                "reviewed mapping snapshot requires empty registry lifecycle events"
                in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_approved_snapshot_requires_approved_registry_event(self) -> None:
        self.set_editorial_status("approved")
        self.set_expected_status("approved")
        package = self.generic_package(
            external_references=[self.external_references()[0]]
        )
        self.assertTrue(
            any(
                "approved mapping snapshot requires governed registry lifecycle events"
                in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_approved_snapshot_with_approved_registry_event_is_valid(self) -> None:
        self.set_editorial_status("approved")
        self.set_expected_status("approved")
        self.set_registry_events(["approved"])
        package = self.generic_package(
            external_references=[self.external_references()[0]]
        )
        self.assertFalse(
            any(
                "lifecycle" in item or "editorial status" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_generic_reference_path_must_be_safe_and_present(self) -> None:
        reference = self.external_references()[0]
        (self.root / str(reference["registry_path"])).unlink()
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "unsafe or missing registry path" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_generic_reference_identifier_must_resolve_in_catalog(self) -> None:
        reference = self.external_references()[0]
        source = self.root / str(reference["registry_path"])
        reference["mapping_set_id"] = "example--mapping-set--0.1.0"
        reference["registry_path"] = (
            "crosswalks/registry/example--mapping-set--0.1.0.md"
        )
        shutil.copy2(source, self.root / str(reference["registry_path"]))
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "does not resolve exactly once" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_generic_reference_requires_canonical_registry_path(self) -> None:
        reference = self.external_references()[0]
        canonical = self.root / str(reference["registry_path"])
        alternate = canonical.with_name("alternate-lifecycle-record.md")
        shutil.copy2(canonical, alternate)
        reference["registry_path"] = alternate.relative_to(self.root).as_posix()
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "registry path must be canonical" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_missing_catalog_snapshot_is_rejected(self) -> None:
        self.snapshot_path().unlink()
        reference = self.external_references()[0]
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "unsafe or missing snapshot path" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_catalog_snapshot_mapping_identifier_drift_is_rejected(self) -> None:
        path = self.snapshot_path()
        mapping_set_id = profile_fixture.MAPPING_REFERENCES[0][0]
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                f"mapping_set_id: {mapping_set_id}",
                "mapping_set_id: example--wrong-mapping--0.1.0",
                1,
            ),
            encoding="utf-8",
            newline="\n",
        )
        reference = self.external_references()[0]
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "snapshot mapping_set_id does not match" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_snapshot_and_catalog_editorial_status_drift_is_rejected(self) -> None:
        self.set_snapshot_editorial_status("reviewed")
        reference = self.external_references()[0]
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "snapshot editorial status reviewed does not match catalog draft"
                in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_catalog_snapshot_escape_is_rejected(self) -> None:
        catalog_path = self.root / "crosswalks/catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        mapping_set_id = profile_fixture.MAPPING_REFERENCES[0][0]
        record = next(
            record
            for record in catalog["mapping_sets"]
            if record["metadata"]["mapping_set_id"] == mapping_set_id
        )
        record["path"] = "../outside-snapshot.md"
        profile_fixture.write_json(catalog_path, catalog)
        reference = self.external_references()[0]
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "unsafe or missing snapshot path" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_catalog_snapshot_must_be_a_regular_file(self) -> None:
        catalog_path = self.root / "crosswalks/catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        mapping_set_id = profile_fixture.MAPPING_REFERENCES[0][0]
        record = next(
            record
            for record in catalog["mapping_sets"]
            if record["metadata"]["mapping_set_id"] == mapping_set_id
        )
        record["path"] = "crosswalks/mappings"
        profile_fixture.write_json(catalog_path, catalog)
        reference = self.external_references()[0]
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "unsafe or missing snapshot path" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_generic_snapshot_symlink_is_rejected(self) -> None:
        path = self.snapshot_path()
        target = path.with_name("snapshot-target.md")
        path.rename(target)
        try:
            path.symlink_to(target)
        except OSError as error:
            target.rename(path)
            self.skipTest(f"symlink creation is unavailable: {error}")
        try:
            reference = self.external_references()[0]
            package = self.generic_package(external_references=[reference])
            self.assertTrue(
                any(
                    "unsafe or missing snapshot path" in item
                    for item in validate_profiles.semantic_diagnostics(
                        self.root, package
                    )
                )
            )
        finally:
            path.unlink()
            target.rename(path)

    @unittest.skipUnless(os.name == "nt", "Windows junction regression")
    def test_generic_snapshot_junction_is_rejected(self) -> None:
        snapshot_directory = self.snapshot_path().parent
        outside = self.root / "outside-snapshot"
        snapshot_directory.rename(outside)
        junction = subprocess.run(
            [
                "cmd",
                "/c",
                "mklink",
                "/J",
                str(snapshot_directory),
                str(outside),
            ],
            capture_output=True,
            text=True,
        )
        if junction.returncode != 0:
            outside.rename(snapshot_directory)
            self.skipTest(f"junction creation is unavailable: {junction.stderr}")
        try:
            reference = self.external_references()[0]
            package = self.generic_package(external_references=[reference])
            self.assertTrue(
                any(
                    "unsafe or missing snapshot path" in item
                    for item in validate_profiles.semantic_diagnostics(
                        self.root, package
                    )
                )
            )
        finally:
            os.rmdir(snapshot_directory)
            outside.rename(snapshot_directory)

    def test_generic_reference_registry_symlink_is_rejected(self) -> None:
        reference = self.external_references()[0]
        path = self.root / str(reference["registry_path"])
        target = path.with_name("registry-target.md")
        path.rename(target)
        try:
            path.symlink_to(target)
        except OSError as error:
            target.rename(path)
            self.skipTest(f"symlink creation is unavailable: {error}")
        package = self.generic_package(external_references=[reference])
        self.assertTrue(
            any(
                "unsafe or missing registry path" in item
                for item in validate_profiles.semantic_diagnostics(
                    self.root, package
                )
            )
        )

    def test_malformed_registry_front_matter_is_content_failure(self) -> None:
        registry_path = profile_fixture.MAPPING_REFERENCES[0][1]
        (self.root / registry_path).write_text(
            "---\nmapping_set_id: [\n---\n# Broken registry\n",
            encoding="utf-8",
            newline="\n",
        )
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 1)
        self.assertIn("cannot parse registry front matter", stderr.getvalue())
        self.assertNotIn(str(self.root), stderr.getvalue())

    def test_malformed_snapshot_front_matter_is_content_failure(self) -> None:
        self.snapshot_path().write_text(
            "---\nmapping_set_id: [\n---\n# Broken snapshot\n",
            encoding="utf-8",
            newline="\n",
        )
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 1)
        self.assertIn("cannot parse snapshot front matter", stderr.getvalue())
        self.assertNotIn(str(self.root), stderr.getvalue())

    def test_valid_governed_mapping_lifecycle_prefixes(self) -> None:
        valid_cases = (
            (["approved"], "approved"),
            (["approved", "published"], "published"),
            (["approved", "published", "deprecated"], "deprecated"),
            (
                ["approved", "published", "deprecated", "retired"],
                "retired",
            ),
        )
        for states, expected_status in valid_cases:
            with self.subTest(states=states):
                metadata = {
                    "editorial_status": "approved",
                    "registry_events": [
                        {"state": state} for state in states
                    ],
                }
                self.assertEqual(
                    [],
                    validate_profiles.mapping_lifecycle_diagnostics(
                        metadata, expected_status
                    ),
                )

    def test_invalid_governed_mapping_lifecycle_transitions(self) -> None:
        invalid_cases = (
            ["approved", "deprecated"],
            ["approved", "approved"],
            ["published", "approved"],
            [
                "approved",
                "published",
                "deprecated",
                "retired",
                "retired",
            ],
        )
        for states in invalid_cases:
            with self.subTest(states=states):
                metadata = {
                    "editorial_status": "approved",
                    "registry_events": [
                        {"state": state} for state in states
                    ],
                }
                self.assertIn(
                    "invalid governed registry lifecycle event prefix",
                    validate_profiles.mapping_lifecycle_diagnostics(
                        metadata, states[-1]
                    ),
                )

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
        self.assert_has_error(
            "draft mapping snapshot requires empty registry lifecycle events"
        )

    def test_registry_os_error_is_operational_and_does_not_disclose_host_path(
        self,
    ) -> None:
        with mock.patch.object(
            validate_profiles,
            "mapping_reference_metadata",
            side_effect=OSError(f"cannot read {self.root}"),
        ):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(
                    2,
                    validate_profiles.main(["--check"], root=self.root),
                )
        self.assertNotIn(str(self.root), stderr.getvalue())

    def test_fourth_mapping_reference_is_rejected(self) -> None:
        document = self.load_component("external-references.json")
        extra = dict(document["external_references"][0])
        extra["mapping_set_id"] = (
            "uk-ncsc--unapproved-mapping--1.0--esaf-0.4-alpha--0.1.0"
        )
        extra["registry_path"] = "crosswalks/registry/unapproved.md"
        document["external_references"].append(extra)
        self.write_component("external-references.json", document)
        self.assert_has_error("unexpected UK pilot mapping reference")

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
            *AFFIRMATIVE_WEAKENING,
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
            "This profile does not make optional core controls.",
            "This profile does not mark inapplicable core controls.",
            "GOV-100 must be applied.",
            "This profile does not supersede GOV-100.",
            "The organization is not exempt from GOV-100.",
            "This profile does not lower core control requirements.",
            "GOV-100 is not superseded by this profile.",
            "GOV-100 is not inapplicable under this profile.",
            "Core control requirements are not lowered by this profile.",
            "This profile does not render GOV-100 optional.",
            "GOV-100 remains applicable.",
            "This profile renders GOV-100 mandatory.",
            "GOV-100 applies under this profile.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_new_control_weakening_quotations_are_allowed(self) -> None:
        for phrase in AFFIRMATIVE_WEAKENING:
            with self.subTest(phrase=phrase):
                (self.package / "README.md").write_text(
                    "# Synthetic profile\n\n"
                    f'The prohibited statement "{phrase}" is quoted for review.\n',
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_affirmative_weakening_after_denial_is_rejected(self) -> None:
        for text in (
            "This profile does not supersede GOV-100, but it lowers GOV-100.",
            (
                "Core controls are not marked inapplicable, yet GOV-100 need "
                "not be applied."
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error("prohibited control weakening language")

    def test_non_negating_not_only_does_not_mask_weakening(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile not only supersedes GOV-100.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited control weakening language")

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
            *AFFIRMATIVE_CLAIMS,
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

    def test_new_profile_claim_denials_are_allowed(self) -> None:
        for text in (
            "This profile does not satisfy Cyber Essentials requirements.",
            "This profile does not ensure legal compliance.",
            "This profile does not confer certification eligibility.",
            "This profile does not have NCSC approval.",
            "Legal compliance is not ensured by this profile.",
            "Certification eligibility is not conferred by this profile.",
            "NCSC approval is not held by this profile.",
            (
                "Cyber Essentials provision A does not map to GOV-100 or "
                "supply its external outcome."
            ),
            (
                "GOV-100 is not mapped from Cyber Essentials provision A and "
                "the external outcome is not imported."
            ),
            (
                "GOV-100 does not support or satisfy Cyber Essentials "
                "provision A."
            ),
            (
                "Cyber Essentials provision A is not supported or satisfied "
                "by GOV-100."
            ),
            (
                "Cyber Essentials provision A does not support or satisfy "
                "GOV-100."
            ),
            (
                "GOV-100 is not supported or satisfied by Cyber Essentials "
                "provision A."
            ),
            "This profile does not meet Cyber Essentials requirements.",
            "This profile does not comply with Cyber Essentials.",
            (
                "This profile does not qualify the organization for "
                "certification."
            ),
            "This profile is not approved by NCSC.",
            "NCSC does not approve this profile.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_new_profile_claim_quotations_and_discussion_are_allowed(self) -> None:
        for text, _ in AFFIRMATIVE_CLAIMS:
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    "# Synthetic profile\n\n"
                    f'The prohibited assertion "{text}" is quoted for review.\n',
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])
                (self.package / "README.md").write_text(
                    "# Synthetic profile\n\n"
                    "The prohibited assertion that "
                    f"{text.rstrip('.')} is discussed here.\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_metalinguistic_context_is_bounded_to_the_assertion(self) -> None:
        for text in (
            (
                "The claim that this profile ensures legal compliance is "
                "prohibited."
            ),
            (
                "This text discusses without asserting that this profile "
                "ensures legal compliance."
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])
        for text, expected in (
            (
                (
                    "The prohibited statement is discussed here, but this "
                    "profile ensures legal compliance."
                ),
                "prohibited assertion 'compliance'",
            ),
            (
                (
                    "The prohibited statement is discussed here, but this "
                    "profile supersedes GOV-100."
                ),
                "prohibited control weakening language",
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error(expected)

    def test_repeated_subject_after_or_is_not_inherited_denial(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile does not ensure legal compliance or this profile "
            "confers certification eligibility.\n",
            encoding="utf-8",
        )
        self.assert_has_error(
            "prohibited assertion 'certification eligibility'"
        )

    def test_affirmative_claim_after_denied_clause_is_rejected(self) -> None:
        for text, expected in (
            (
                (
                    "This profile does not ensure legal compliance, but it "
                    "confers certification eligibility."
                ),
                "certification eligibility",
            ),
            (
                (
                    "Cyber Essentials provision A does not map to GOV-100, "
                    "yet it supplies its external outcome."
                ),
                "external outcome import",
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error(f"prohibited assertion '{expected}'")

    def test_non_negating_not_only_does_not_mask_claim(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile not only satisfies Cyber Essentials requirements.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited assertion 'scheme satisfaction'")

    def test_mapping_leakage_is_checked_in_every_json_narrative(self) -> None:
        package = self.loaded_package()
        package.documents["profile"]["nested"] = {
            "arbitrary_narrative": (
                "Cyber Essentials provision A maps to GOV-100 and imports "
                "its external outcome."
            )
        }
        diagnostics = validate_profiles.claim_diagnostics(package)
        self.assertTrue(
            any(
                "prohibited assertion 'imported mapping relationship'" in item
                for item in diagnostics
            ),
            diagnostics,
        )
        self.assertTrue(
            any(
                "prohibited assertion 'external outcome import'" in item
                for item in diagnostics
            ),
            diagnostics,
        )

    def test_source_boundary_rejects_excluded_authority_claims(self) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["UK GDPR"]
        self.write_component("profile.json", profile)
        for text in (
            "UK GDPR is the authority for this profile selection.",
            "This profile selection is governed by UK GDPR.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assert_has_error("prohibited source authority language")

    def test_source_boundary_uses_declared_generic_excluded_source(self) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["Acme Code"]
        self.write_component("profile.json", profile)
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "Acme Code is the authority for this profile selection.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited source authority language")

    def test_source_authority_denials_and_discussion_are_allowed(self) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["UK GDPR"]
        self.write_component("profile.json", profile)
        for text in (
            "UK GDPR is not the authority for this profile selection.",
            "This profile selection is not governed by UK GDPR.",
            (
                'The prohibited assertion "UK GDPR is the authority for this '
                'profile selection" is quoted for review.'
            ),
            (
                "The assertion that UK GDPR is the authority for this profile "
                "selection is prohibited and discussed here."
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_source_authority_after_denied_clause_is_rejected(self) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["UK GDPR"]
        self.write_component("profile.json", profile)
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "UK GDPR is not the authority for this profile title, but it is "
            "the authority for this profile selection.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited source authority language")
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "The prohibited statement is discussed here, but UK GDPR is the "
            "authority for this profile selection.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited source authority language")

    def test_unrelated_claim_denial_does_not_mask_source_authority(self) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["UK GDPR"]
        self.write_component("profile.json", profile)
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile does not ensure legal compliance or UK GDPR is the "
            "authority for this profile selection.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited source authority language")

    def test_risk_source_basis_must_resolve(self) -> None:
        self.write_closed_trace_fixture()
        for source_basis in ("UK GDPR", "ESAF-1100 controls GOV-100"):
            with self.subTest(source_basis=source_basis):
                document = self.load_component("risk-overlays.json")
                document["risks"][0]["source_basis"] = [source_basis]
                self.write_component("risk-overlays.json", document)
                self.assert_has_error(
                    f"unresolved risk source basis {source_basis!r}"
                )

    def test_risk_source_basis_accepts_controls_and_permitted_sources(
        self,
    ) -> None:
        control_id = self.write_closed_trace_fixture()
        for source_basis in (control_id, "ESAF"):
            with self.subTest(source_basis=source_basis):
                document = self.load_component("risk-overlays.json")
                document["risks"][0]["source_basis"] = [source_basis]
                self.write_component("risk-overlays.json", document)
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_later_metalinguistic_discussion_does_not_mask_assertions(
        self,
    ) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["UK GDPR"]
        self.write_component("profile.json", profile)
        for text, expected in (
            (
                (
                    "This profile ensures legal compliance, and the document "
                    "discusses that claim."
                ),
                "prohibited assertion 'compliance'",
            ),
            (
                (
                    "This profile supersedes GOV-100, and the document "
                    "discusses that statement."
                ),
                "prohibited control weakening language",
            ),
            (
                (
                    "UK GDPR is the authority for this profile selection, and "
                    "the document discusses that claim."
                ),
                "prohibited source authority language",
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assert_has_error(expected)

    def test_additional_control_weakening_forms_are_rejected(self) -> None:
        for text in (
            "GOV-100 is optional under this profile.",
            "Core controls are optional under this profile.",
            "GOV-100 shall not apply under this profile.",
            "GOV-100 is not required under this profile.",
            "This profile makes GOV-100 not required.",
            "Under this profile, optional controls include GOV-100.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assert_has_error("prohibited control weakening language")

    def test_additional_weakening_denials_and_discussion_are_allowed(self) -> None:
        for text in (
            "GOV-100 is not optional under this profile.",
            "Core controls are not optional under this profile.",
            "GOV-100 shall apply under this profile.",
            'The phrase "GOV-100 is not required" is prohibited.',
            (
                "The claim that GOV-100 is not required is discussed and "
                "rejected."
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_additional_assurance_claim_forms_are_rejected(self) -> None:
        for text, expected in (
            ("This profile guarantees legal compliance.", "compliance"),
            (
                "This profile makes the organization eligible for certification.",
                "certification eligibility",
            ),
            ("This profile certifies the organization.", "certification"),
            (
                "This profile has received NCSC approval.",
                "named-authority approval",
            ),
            (
                "NCSC has approved this profile.",
                "named-authority approval",
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assert_has_error(f"prohibited assertion '{expected}'")

    def test_additional_assurance_denials_and_discussion_are_allowed(self) -> None:
        for text in (
            "This profile does not guarantee legal compliance.",
            (
                "This profile does not make the organization eligible for "
                "certification."
            ),
            "This profile does not certify the organization.",
            "This profile has not received NCSC approval.",
            "NCSC has not approved this profile.",
            (
                'The phrase "This profile guarantees legal compliance" is '
                "prohibited."
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_reordered_mapping_and_general_authority_are_rejected(self) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = [
            "UK GDPR",
            "NCSC",
            "Cyber Essentials",
        ]
        self.write_component("profile.json", profile)
        for text, expected in (
            (
                "Requirement A of Cyber Essentials maps to GOV-100.",
                "prohibited assertion 'imported mapping relationship'",
            ),
            (
                "Cyber Essentials provision A has a mapping to GOV-100.",
                "prohibited assertion 'imported mapping relationship'",
            ),
            (
                "NCSC provision A maps to GOV-100.",
                "prohibited assertion 'imported mapping relationship'",
            ),
            (
                "UK GDPR governs this profile.",
                "prohibited source authority language",
            ),
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assert_has_error(expected)

    def test_reordered_mapping_and_general_authority_denials_are_allowed(
        self,
    ) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = [
            "UK GDPR",
            "NCSC",
            "Cyber Essentials",
        ]
        self.write_component("profile.json", profile)
        for text in (
            "Requirement A of Cyber Essentials does not map to GOV-100.",
            "Cyber Essentials provision A has no mapping to GOV-100.",
            "NCSC provision A does not map to GOV-100.",
            "UK GDPR does not govern this profile.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_polarity_is_bound_to_the_assertion_head(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "It is not surprising that this profile ensures legal compliance.\n",
            encoding="utf-8",
        )
        self.assert_has_error("prohibited assertion 'compliance'")
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "GOV-100 is superseded by no profile.\n",
            encoding="utf-8",
        )
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_contrast_clause_boundaries_do_not_mask_prohibited_language(
        self,
    ) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["UK GDPR"]
        self.write_component("profile.json", profile)
        cases = (
            ("This profile guarantees legal compliance.", "assertion 'compliance'"),
            ("This profile supersedes GOV-100.", "control weakening language"),
            (
                "UK GDPR governs this profile.",
                "source authority language",
            ),
        )
        for conjunction in (
            "while",
            "whereas",
            "although",
            "though",
            "even though",
            "however",
        ):
            for assertion, expected in cases:
                text = (
                    "The document discusses and rejects that claim "
                    f"{conjunction} {assertion}"
                )
                with self.subTest(conjunction=conjunction, assertion=assertion):
                    (self.package / "README.md").write_text(
                        f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                    )
                    self.assert_has_error(f"prohibited {expected}")

    def test_weakening_state_grammar_matrix(self) -> None:
        singular_predicates = (
            "must not apply",
            "shall not apply",
            "need not apply",
            "no longer applies",
            "is no longer required",
            "shall be optional",
            "must be optional",
            "is optional",
            "shall be inapplicable",
            "must be inapplicable",
            "is inapplicable",
            "is not required",
        )
        plural_predicates = (
            "must not apply",
            "shall not apply",
            "need not apply",
            "no longer apply",
            "are no longer required",
            "shall be optional",
            "must be optional",
            "are optional",
            "shall be inapplicable",
            "must be inapplicable",
            "are inapplicable",
            "are not required",
        )
        for subject, predicates in (
            ("GOV-100", singular_predicates),
            ("Core controls", plural_predicates),
        ):
            for predicate in predicates:
                text = f"{subject} {predicate} under this profile."
                with self.subTest(subject=subject, predicate=predicate):
                    (self.package / "README.md").write_text(
                        f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                    )
                    self.assert_has_error(
                        "prohibited control weakening language"
                    )

    def test_assurance_voice_tense_and_aspect_grammar_matrix(self) -> None:
        cases = (
            ("This profile guarantees legal compliance.", "compliance"),
            ("This profile guaranteed legal compliance.", "compliance"),
            ("This profile has guaranteed legal compliance.", "compliance"),
            ("This profile proves legal compliance.", "compliance"),
            ("This profile proved legal compliance.", "compliance"),
            ("This profile has proven legal compliance.", "compliance"),
            ("Legal compliance is ensured by this profile.", "compliance"),
            ("Legal compliance was proven by this profile.", "compliance"),
            ("Legal compliance has been guaranteed by this profile.", "compliance"),
            ("This profile certified the organization.", "certification"),
            ("This profile has certified the organization.", "certification"),
            ("The organization was certified by this profile.", "certification"),
            ("The organization has been certified by this profile.", "certification"),
            (
                "This profile made the organization eligible for certification.",
                "certification eligibility",
            ),
            (
                "The organization has been made eligible for certification by "
                "this profile.",
                "certification eligibility",
            ),
            ("NCSC approved this profile.", "named-authority approval"),
            ("NCSC has approved this profile.", "named-authority approval"),
            ("This profile was approved by NCSC.", "named-authority approval"),
            ("This profile has been approved by NCSC.", "named-authority approval"),
            ("This profile received NCSC approval.", "named-authority approval"),
        )
        for text, label in cases:
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assert_has_error(f"prohibited assertion '{label}'")

    def test_mapping_direction_and_authority_grammar_matrix(self) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = [
            "UK GDPR",
            "Cyber Essentials",
        ]
        self.write_component("profile.json", profile)
        for text in (
            "Cyber Essentials provision A maps to GOV-100.",
            "Cyber Essentials provision A mapped to GOV-100.",
            "Cyber Essentials provision A has a mapping to GOV-100.",
            "Cyber Essentials provision A is mapped to GOV-100.",
            "GOV-100 is mapped from Cyber Essentials provision A.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assert_has_error(
                    "prohibited assertion 'imported mapping relationship'"
                )
        for text in (
            "This profile is governed by UK GDPR.",
            "This profile was governed by UK GDPR.",
            "UK GDPR governs this profile.",
            "UK GDPR governed this profile.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assert_has_error("prohibited source authority language")
        for text in (
            "Cyber Essentials provision A is not mapped to GOV-100.",
            (
                "The claim that Cyber Essentials provision A is mapped to "
                "GOV-100 is false."
            ),
            "This profile is not governed by UK GDPR.",
            "The claim that this profile is governed by UK GDPR is rejected.",
        ):
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_extended_polarity_and_metalinguistic_matrix(self) -> None:
        allowed = (
            (
                "This profile does not under any circumstances guarantee "
                "legal compliance."
            ),
            "GOV-100 is superseded by neither this profile nor any overlay.",
            "The claim that GOV-100 is optional is false.",
            (
                "The claim that this profile guarantees legal compliance is "
                "false."
            ),
            "The claim that GOV-100 shall be optional is rejected.",
            (
                "The assertion that this profile has guaranteed legal "
                "compliance is denied."
            ),
            "Legal compliance has not been guaranteed by this profile.",
            "Legal compliance is guaranteed by no profile.",
            (
                "Legal compliance is guaranteed by neither this profile nor "
                "any overlay."
            ),
            "NCSC did not approve this profile.",
            'The phrase "This profile proved legal compliance" is prohibited.',
        )
        for text in allowed:
            with self.subTest(text=text):
                (self.package / "README.md").write_text(
                    f"# Synthetic profile\n\n{text}\n", encoding="utf-8"
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_weakening_subject_modal_and_state_cross_product(self) -> None:
        subjects = (
            ("GOV-100", "is", "applies", "ceases", "discontinues"),
            ("Core controls", "are", "apply", "cease", "discontinue"),
        )
        states = ("optional", "inapplicable", "not mandatory")
        for (subject, copula, _, _, _), state in product(subjects, states):
            modal_states = (
                (
                    f"{modal} not be mandatory"
                    if state == "not mandatory"
                    else f"{modal} be {state}"
                )
                for modal in ("shall", "must", "may")
            )
            for predicate in (
                f"{copula} {state}",
                *modal_states,
            ):
                with self.subTest(subject=subject, predicate=predicate):
                    self.write_readme(f"{subject} {predicate}.")
                    self.assert_has_error(
                        "prohibited control weakening language"
                    )
        for subject, copula, applies, ceases, discontinues in subjects:
            transitions = (
                f"no longer {applies}",
                f"{copula} no longer applied",
                f"{copula} discontinued",
                f"{ceases} to apply",
                f"{discontinues} applying",
                *(
                    f"{modal} {verb}"
                    for modal, verb in product(
                        ("shall", "must", "may"),
                        ("cease to apply", "discontinue applying"),
                    )
                ),
            )
            for predicate in transitions:
                with self.subTest(subject=subject, predicate=predicate):
                    self.write_readme(f"{subject} {predicate}.")
                    self.assert_has_error(
                        "prohibited control weakening language"
                    )

    def test_weakening_cross_product_denials_and_claim_frames(self) -> None:
        denied = (
            "GOV-100 is not optional.",
            "Core controls are not inapplicable.",
            "GOV-100 is mandatory.",
            "GOV-100 does not cease to apply.",
            "Core controls do not discontinue applying.",
            "GOV-100 is not discontinued.",
            "Core controls are still applied.",
            "GOV-100 may not be optional.",
        )
        frames = ("is false", "is rejected", "was denied")
        claims = (
            "GOV-100 is not mandatory",
            "Core controls may be optional",
            "GOV-100 shall cease to apply",
        )
        for text in denied:
            with self.subTest(text=text):
                self.write_readme(text)
                self.assertEqual(validate_profiles.validate(self.root), [])
        for claim, frame in product(claims, frames):
            with self.subTest(claim=claim, frame=frame):
                self.write_readme(f"The claim that {claim} {frame}.")
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_approval_subject_voice_and_aspect_cross_product(self) -> None:
        aspects = ("present", "past", "perfect", "past-perfect")
        constructions = (
            (
                "NCSC {verb} this profile",
                {
                    "present": ("approves", "does not approve"),
                    "past": ("approved", "did not approve"),
                    "perfect": ("has approved", "has not approved"),
                    "past-perfect": ("had approved", "had not approved"),
                },
            ),
            (
                "This profile {verb} NCSC approval",
                {
                    "present": ("receives", "does not receive"),
                    "past": ("received", "did not receive"),
                    "perfect": ("has received", "has not received"),
                    "past-perfect": ("had received", "had not received"),
                },
            ),
            (
                "This profile {verb} by NCSC",
                {
                    "present": ("is approved", "is not approved"),
                    "past": ("was approved", "was not approved"),
                    "perfect": ("has been approved", "has not been approved"),
                    "past-perfect": (
                        "had been approved",
                        "had not been approved",
                    ),
                },
            ),
        )
        for (template, forms), aspect in product(constructions, aspects):
            affirmative, denied = forms[aspect]
            with self.subTest(template=template, aspect=aspect, polarity=True):
                self.write_readme(f"{template.format(verb=affirmative)}.")
                self.assert_has_error(
                    "prohibited assertion 'named-authority approval'"
                )
            with self.subTest(template=template, aspect=aspect, polarity=False):
                self.write_readme(f"{template.format(verb=denied)}.")
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_mapping_direction_form_and_aspect_cross_product(self) -> None:
        external = "Cyber Essentials provision A"
        control = "GOV-100"
        directions = (
            (external, "to", control),
            (control, "from", external),
        )
        affirmative_forms = (
            "{subject} maps {preposition} {object}",
            "{subject} mapped {preposition} {object}",
            "{subject} has mapped {preposition} {object}",
            "{subject} had mapped {preposition} {object}",
            "{subject} is mapped {preposition} {object}",
            "{subject} was mapped {preposition} {object}",
            "{subject} has been mapped {preposition} {object}",
            "{subject} had been mapped {preposition} {object}",
            "{subject} has a mapping {preposition} {object}",
            "{subject} had a mapping {preposition} {object}",
        )
        for direction, form in product(directions, affirmative_forms):
            subject, preposition, object_ = direction
            assertion = form.format(
                subject=subject,
                preposition=preposition,
                object=object_,
            )
            with self.subTest(direction=direction, form=form):
                self.write_readme(f"{assertion}.")
                self.assert_has_error(
                    "prohibited assertion 'imported mapping relationship'"
                )
        denied_forms = (
            "{subject} does not map {preposition} {object}",
            "{subject} did not map {preposition} {object}",
            "{subject} has not mapped {preposition} {object}",
            "{subject} had not mapped {preposition} {object}",
            "{subject} is not mapped {preposition} {object}",
            "{subject} has not been mapped {preposition} {object}",
            "{subject} had not been mapped {preposition} {object}",
            "{subject} has no mapping {preposition} {object}",
            "{subject} had no mapping {preposition} {object}",
        )
        for direction, form in product(directions, denied_forms):
            subject, preposition, object_ = direction
            assertion = form.format(
                subject=subject,
                preposition=preposition,
                object=object_,
            )
            with self.subTest(direction=direction, form=form):
                self.write_readme(f"{assertion}.")
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_declared_generic_authority_passive_aspect_cross_product(
        self,
    ) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["Acme Code"]
        self.write_component("profile.json", profile)
        for auxiliary in ("is", "was", "has been", "had been"):
            with self.subTest(auxiliary=auxiliary):
                self.write_readme(
                    f"This profile {auxiliary} governed by Acme Code."
                )
                self.assert_has_error("prohibited source authority language")
        for auxiliary in ("is not", "was not", "has not been", "had not been"):
            with self.subTest(auxiliary=auxiliary):
                self.write_readme(
                    f"This profile {auxiliary} governed by Acme Code."
                )
                self.assertEqual(validate_profiles.validate(self.root), [])
        self.write_readme("This profile is governed by Other Code.")
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_negation_binding_complement_and_insertion_cross_product(
        self,
    ) -> None:
        embedded = (
            "It is not surprising to see this profile guarantee legal compliance.",
            "It is not unusual to observe this profile guarantee legal compliance.",
            "It is not unexpected that this profile guarantees legal compliance.",
            (
                "A reviewer who did not object saw this profile guarantee "
                "legal compliance."
            ),
        )
        for text in embedded:
            with self.subTest(text=text):
                self.write_readme(text)
                self.assert_has_error("prohibited assertion 'compliance'")
        insertions = (
            "as reviewers who assessed it confirmed",
            "according to reviewers",
            "despite what reviewers expected",
        )
        for insertion in insertions:
            with self.subTest(insertion=insertion):
                self.write_readme(
                    "This profile does not, "
                    f"{insertion}, guarantee legal compliance."
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_postposed_denial_and_rejection_polarity_cross_product(
        self,
    ) -> None:
        for boundary in ("while", "whereas", "although"):
            with self.subTest(boundary=boundary):
                self.write_readme(
                    "This profile guarantees legal compliance "
                    f"{boundary} certification is granted by no authority."
                )
                self.assert_has_error("prohibited assertion 'compliance'")
        claims = (
            "this profile guarantees legal compliance",
            "GOV-100 is optional",
        )
        affirmative_frames = ("is false", "is rejected", "was denied")
        negated_frames = (
            "is not false",
            "is not rejected",
            "was not denied",
            "has not been rejected",
        )
        for claim, frame in product(claims, affirmative_frames):
            with self.subTest(claim=claim, frame=frame):
                self.write_readme(f"The claim that {claim} {frame}.")
                self.assertEqual(validate_profiles.validate(self.root), [])
        for claim, frame in product(claims, negated_frames):
            with self.subTest(claim=claim, frame=frame):
                self.write_readme(f"The claim that {claim} {frame}.")
                expected = (
                    "prohibited assertion 'compliance'"
                    if "guarantees" in claim
                    else "prohibited control weakening language"
                )
                self.assert_has_error(expected)

    def test_weakening_aspect_and_state_cross_product(self) -> None:
        subjects = (
            ("GOV-100", "has", "is", "was"),
            ("Core controls", "have", "are", "were"),
        )
        active_aspects = (
            "{perfect} ceased to apply",
            "had ceased to apply",
            "{perfect} discontinued applying",
            "had discontinued applying",
        )
        passive_aspects = (
            "{present} discontinued",
            "{past} discontinued",
            "{perfect} been discontinued",
            "had been discontinued",
        )
        mandatory_aspects = (
            "{present} no longer mandatory",
            "{past} no longer mandatory",
            "{perfect} been no longer mandatory",
            "had been no longer mandatory",
        )
        for subject, perfect, present, past in subjects:
            values = {
                "perfect": perfect,
                "present": present,
                "past": past,
            }
            for family, forms in (
                ("active", active_aspects),
                ("passive", passive_aspects),
                ("mandatory", mandatory_aspects),
            ):
                for form in forms:
                    predicate = form.format(**values)
                    with self.subTest(
                        subject=subject,
                        family=family,
                        predicate=predicate,
                    ):
                        self.write_readme(f"{subject} {predicate}.")
                        self.assert_has_error(
                            "prohibited control weakening language"
                        )

    def test_weakening_aspect_denial_and_metalinguistic_pairs(self) -> None:
        denied = (
            "GOV-100 has not ceased to apply.",
            "Core controls have never discontinued applying.",
            "GOV-100 has not been discontinued.",
            "Core controls had never been discontinued.",
        )
        claims = (
            "GOV-100 has ceased to apply",
            "Core controls had been discontinued",
            "GOV-100 has been no longer mandatory",
        )
        for text in denied:
            with self.subTest(text=text):
                self.write_readme(text)
                self.assertEqual(validate_profiles.validate(self.root), [])
        for claim, frame in product(
            claims,
            ("is false", "is rejected", "was denied"),
        ):
            with self.subTest(claim=claim, frame=frame):
                self.write_readme(f"The claim that {claim} {frame}.")
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_bounded_adverb_slots_cross_product(self) -> None:
        adverbs = (
            "formally",
            "explicitly",
            "directly",
            "expressly",
            "carefully",
        )
        templates = (
            (
                "NCSC has {adverb} approved this profile.",
                "prohibited assertion 'named-authority approval'",
            ),
            (
                "This profile had {adverb} received NCSC approval.",
                "prohibited assertion 'named-authority approval'",
            ),
            (
                "This profile has been {adverb} approved by NCSC.",
                "prohibited assertion 'named-authority approval'",
            ),
            (
                "Cyber Essentials provision A has {adverb} mapped to GOV-100.",
                "prohibited assertion 'imported mapping relationship'",
            ),
            (
                "Cyber Essentials provision A has been {adverb} mapped to "
                "GOV-100.",
                "prohibited assertion 'imported mapping relationship'",
            ),
            (
                "GOV-100 had {adverb} mapped from Cyber Essentials provision A.",
                "prohibited assertion 'imported mapping relationship'",
            ),
            (
                "GOV-100 had been {adverb} mapped from Cyber Essentials "
                "provision A.",
                "prohibited assertion 'imported mapping relationship'",
            ),
        )
        for (template, expected), adverb in product(templates, adverbs):
            with self.subTest(template=template, adverb=adverb):
                self.write_readme(template.format(adverb=adverb))
                self.assert_has_error(expected)

    def test_dynamic_authority_bounded_adverb_cross_product(self) -> None:
        profile = self.load_component("profile.json")
        profile["source_boundary"]["excluded_sources"] = ["Acme Code"]
        self.write_component("profile.json", profile)
        for auxiliary, adverb in product(
            ("is", "was", "has been", "had been"),
            ("formally", "explicitly", "directly", "carefully"),
        ):
            with self.subTest(auxiliary=auxiliary, adverb=adverb):
                self.write_readme(
                    f"This profile {auxiliary} {adverb} governed by Acme Code."
                )
                self.assert_has_error("prohibited source authority language")
        for modifier in ("not", "never", "by no means"):
            with self.subTest(modifier=modifier):
                self.write_readme(
                    f"This profile has {modifier} been governed by Acme Code."
                )
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_negative_modifiers_remain_polarity_cross_product(self) -> None:
        templates = (
            "NCSC has {modifier} approved this profile.",
            (
                "Cyber Essentials provision A has {modifier} mapped to "
                "GOV-100."
            ),
            (
                "GOV-100 has {modifier} mapped from Cyber Essentials "
                "provision A."
            ),
        )
        for template, modifier in product(
            templates,
            ("not", "never", "by no means"),
        ):
            with self.subTest(template=template, modifier=modifier):
                self.write_readme(template.format(modifier=modifier))
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_postposed_denial_agent_vs_rhetorical_cross_product(self) -> None:
        rhetorical = (
            "This profile guarantees legal compliance to no one's surprise.",
            "This profile proves legal compliance by no small margin.",
            "GOV-100 is superseded by no small margin.",
            "Core controls are discontinued by no surprising mechanism.",
        )
        for text in rhetorical:
            with self.subTest(text=text):
                self.write_readme(text)
                expected = (
                    "prohibited control weakening language"
                    if "GOV-100" in text or "Core controls" in text
                    else "prohibited assertion 'compliance'"
                )
                self.assert_has_error(expected)
        genuine_denials = (
            "Legal compliance is guaranteed by no profile.",
            "Legal compliance was proven by no authority.",
            "GOV-100 is superseded by no profile.",
            "Core controls are discontinued by no authority.",
            (
                "GOV-100 is superseded by neither this profile nor any "
                "overlay."
            ),
        )
        for text in genuine_denials:
            with self.subTest(text=text):
                self.write_readme(text)
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_negated_rejection_head_cross_product(self) -> None:
        claims = (
            (
                "this profile guarantees legal compliance",
                "prohibited assertion 'compliance'",
            ),
            (
                "GOV-100 is optional",
                "prohibited control weakening language",
            ),
        )
        frames = (
            "is never false",
            "was by no means rejected",
            "has never been denied",
            "cannot be rejected",
            "can't be denied",
            "is neither false nor rejected",
        )
        for (claim, expected), frame in product(claims, frames):
            with self.subTest(claim=claim, frame=frame):
                self.write_readme(f"The claim that {claim} {frame}.")
                self.assert_has_error(expected)

    def test_natural_perfect_mandatory_placement_cross_product(self) -> None:
        subjects = (
            ("GOV-100", "has"),
            ("Core controls", "have"),
        )
        for (subject, present_perfect), auxiliary in product(
            subjects,
            ("present", "past"),
        ):
            verb = present_perfect if auxiliary == "present" else "had"
            with self.subTest(subject=subject, auxiliary=verb):
                self.write_readme(
                    f"{subject} {verb} no longer been mandatory."
                )
                self.assert_has_error(
                    "prohibited control weakening language"
                )

    def test_natural_perfect_mandatory_denial_and_discussion_pairs(
        self,
    ) -> None:
        for subject, auxiliary in (
            ("GOV-100", "has"),
            ("Core controls", "have"),
            ("GOV-100", "had"),
        ):
            for negator in ("not", "never"):
                with self.subTest(
                    subject=subject,
                    auxiliary=auxiliary,
                    negator=negator,
                ):
                    self.write_readme(
                        f"{subject} {auxiliary} {negator} ceased to be "
                        "mandatory."
                    )
                    self.assertEqual(validate_profiles.validate(self.root), [])
        claims = (
            "GOV-100 has no longer been mandatory",
            "Core controls have no longer been mandatory",
            "GOV-100 had no longer been mandatory",
        )
        for claim, frame in product(
            claims,
            ("is false", "is rejected", "was denied"),
        ):
            with self.subTest(claim=claim, frame=frame):
                self.write_readme(f"The claim that {claim} {frame}.")
                self.assertEqual(validate_profiles.validate(self.root), [])
        for claim in claims:
            with self.subTest(claim=claim, frame="quotation"):
                self.write_readme(f'The phrase "{claim}" is prohibited.')
                self.assertEqual(validate_profiles.validate(self.root), [])

    def test_postposed_possessive_rhetorical_suffix_cross_product(
        self,
    ) -> None:
        closed_nouns = (
            "profile",
            "authority",
            "source",
            "body",
            "organization",
            "agency",
            "overlay",
        )
        for noun, apostrophe in product(closed_nouns, ("'s", "’s")):
            with self.subTest(noun=noun, apostrophe=apostrophe):
                self.write_readme(
                    "This profile proves legal compliance by no "
                    f"{noun}{apostrophe} surprise."
                )
                self.assert_has_error("prohibited assertion 'compliance'")
        for text in (
            "This profile proves legal compliance by no organization’s surprise.",
            "This profile proves legal compliance by no authority's measure.",
        ):
            with self.subTest(text=text):
                self.write_readme(text)
                self.assert_has_error("prohibited assertion 'compliance'")

    def test_postposed_terminal_and_qualified_denial_cross_product(
        self,
    ) -> None:
        closed_nouns = (
            "profile",
            "authority",
            "source",
            "body",
            "organization",
            "agency",
            "overlay",
        )
        for noun in closed_nouns:
            with self.subTest(noun=noun, qualification="terminal"):
                self.write_readme(
                    f"Legal compliance was proven by no {noun}."
                )
                self.assertEqual(validate_profiles.validate(self.root), [])
        for qualifier in (
            "under this profile",
            "within the scheme",
            "in this document",
        ):
            with self.subTest(qualifier=qualifier):
                self.write_readme(
                    "Legal compliance was proven by no authority "
                    f"{qualifier}."
                )
                self.assertEqual(validate_profiles.validate(self.root), [])
        for text in (
            (
                "GOV-100 is superseded by neither this profile nor any "
                "overlay."
            ),
            (
                "GOV-100 is superseded by neither this profile nor any "
                "overlay under this profile."
            ),
        ):
            with self.subTest(text=text):
                self.write_readme(text)
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

    def test_malformed_readme_encoding_is_a_content_failure(self) -> None:
        (self.package / "README.md").write_bytes(b"\xff\xfe")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 1)
        self.assertIn("README.md: cannot decode UTF-8 content", stderr.getvalue())

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

    def test_package_alias_is_rejected_without_traversing_it(self) -> None:
        outside = self.root / "outside-package"
        outside.mkdir()
        (outside / "nested.txt").write_text("outside\n", encoding="utf-8")
        alias = self.package / "rogue"
        try:
            alias.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            if os.name != "nt":
                self.skipTest(f"directory symlinks unavailable: {exc}")
            junction = subprocess.run(
                [
                    "cmd",
                    "/c",
                    "mklink",
                    "/J",
                    str(alias),
                    str(outside),
                ],
                capture_output=True,
                text=True,
            )
            if junction.returncode != 0:
                self.skipTest(
                    f"directory aliases are unavailable: {exc}; "
                    f"{junction.stderr}"
                )
        try:
            diagnostics = validate_profiles.validate(self.root)
            self.assertTrue(
                any(
                    "unlisted package symlink or junction alias rogue" in item
                    for item in diagnostics
                ),
                diagnostics,
            )
            self.assertFalse(
                any("nested.txt" in item for item in diagnostics),
                diagnostics,
            )
        finally:
            if alias.is_symlink():
                alias.unlink()
            elif alias.is_junction():
                os.rmdir(alias)

    def test_missing_profile_manifest_is_rejected(self) -> None:
        (self.package / "profile.json").unlink()
        self.assertTrue(
            any("missing package file profile.json" in error for error in validate_profiles.validate(self.root))
        )

    def test_directory_profile_manifest_is_a_content_failure(self) -> None:
        manifest = self.package / "profile.json"
        manifest.unlink()
        manifest.mkdir()
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 1)
        self.assertIn("regular file", stderr.getvalue())

    def test_missing_component_is_rejected(self) -> None:
        (self.package / "evidence-expectations.json").unlink()
        self.assertTrue(
            any(
                "missing package file evidence-expectations.json" in error
                for error in validate_profiles.validate(self.root)
            )
        )

    def test_directory_component_is_a_content_failure(self) -> None:
        component = self.package / "risk-overlays.json"
        component.unlink()
        component.mkdir()
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 1)
        self.assertIn("regular file", stderr.getvalue())

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

    def test_symlink_check_does_not_inspect_ancestors_above_repository(
        self,
    ) -> None:
        outside_ancestor = self.root.parent.parent
        original_is_symlink = Path.is_symlink

        def simulated_ancestor_symlink(path: Path) -> bool:
            return path == outside_ancestor or original_is_symlink(path)

        with mock.patch.object(
            Path,
            "is_symlink",
            autospec=True,
            side_effect=simulated_ancestor_symlink,
        ):
            self.assertEqual(validate_profiles.validate(self.root), [])

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
            if os.name != "nt":
                self.skipTest(f"symlink creation is unavailable: {exc}")
            junction = subprocess.run(
                [
                    "cmd",
                    "/c",
                    "mklink",
                    "/J",
                    str(country),
                    str(outside_country),
                ],
                capture_output=True,
                text=True,
            )
            if junction.returncode != 0:
                self.skipTest(
                    f"directory aliases are unavailable: {exc}; "
                    f"{junction.stderr}"
                )
        try:
            self.assertTrue(
                any(
                    "symlink" in error
                    for error in validate_profiles.validate(self.root)
                )
            )
        finally:
            if country.is_symlink():
                country.unlink()
            elif country.is_junction():
                os.rmdir(country)
            if not country.exists():
                shutil.move(str(outside_country), country)

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

    def test_component_permission_error_is_operational_and_sanitized(self) -> None:
        with mock.patch(
            "tools.validate_profiles.load_json",
            side_effect=PermissionError(r"C:\secret\profile.json"),
        ):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(
                    2,
                    validate_profiles.main(["--check"], root=self.root),
                )
        self.assertNotIn(r"C:\secret", stderr.getvalue())

    def test_component_resolution_error_is_operational_and_sanitized(self) -> None:
        with mock.patch.object(
            Path,
            "resolve",
            side_effect=PermissionError(r"C:\secret\profile.json"),
        ):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(
                    2,
                    validate_profiles.main(["--check"], root=self.root),
                )
        self.assertNotIn(r"C:\secret", stderr.getvalue())

    def test_inventory_permission_error_is_operational_and_sanitized(self) -> None:
        with mock.patch.object(
            Path,
            "lstat",
            side_effect=PermissionError(r"C:\secret\profiles"),
        ):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(
                    2,
                    validate_profiles.main(["--check"], root=self.root),
                )
        self.assertNotIn(r"C:\secret", stderr.getvalue())

    def test_cli_reports_unresolvable_schema_reference_with_exit_two(self) -> None:
        path = self.root / "profiles/schema/profile.schema.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["allOf"] = [{"$ref": "missing.schema.json"}]
        path.write_text(json.dumps(schema), encoding="utf-8")
        with self.assertRaises(
            validate_profiles.OperationalProfileError
        ) as caught:
            validate_profiles.validate(self.root)
        self.assertNotIn(str(self.root), str(caught.exception))
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = validate_profiles.main(["--check"], root=self.root)
        self.assertEqual(result, 2)
        self.assertIn("could not run", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
