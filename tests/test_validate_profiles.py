from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from dataclasses import replace
from itertools import product
from pathlib import Path
from unittest import mock

from tests import profile_fixture, profile_language_cases
from tools import validate_profiles, verify_profile_hot_path_equivalence


ACTIVE_ASPECT_FORMS = (
    ("{present}", "does not {base}"),
    ("{past}", "did not {base}"),
    ("has {participle}", "has not {participle}"),
    ("had {participle}", "had not {participle}"),
    ("is {progressive}", "is not {progressive}"),
    ("was {progressive}", "was not {progressive}"),
    ("has been {progressive}", "has not been {progressive}"),
    ("had been {progressive}", "had not been {progressive}"),
)
PASSIVE_ASPECT_FORMS = (
    ("is {participle}", "is not {participle}"),
    ("was {participle}", "was not {participle}"),
    ("has been {participle}", "has not been {participle}"),
    ("had been {participle}", "had not been {participle}"),
    ("is being {participle}", "is not being {participle}"),
    ("was being {participle}", "was not being {participle}"),
)


def aspect_forms(
    *,
    base: str,
    present: str,
    past: str,
    participle: str,
    progressive: str,
    voice: str,
) -> tuple[tuple[str, str], ...]:
    templates = (
        ACTIVE_ASPECT_FORMS if voice == "active" else PASSIVE_ASPECT_FORMS
    )
    values = {
        "base": base,
        "present": present,
        "past": past,
        "participle": participle,
        "progressive": progressive,
    }
    return tuple(
        (
            affirmative.format(**values),
            denial.format(**values),
        )
        for affirmative, denial in templates
    )


class ProfileFixtureWriterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.package = profile_fixture.write_valid_profile_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_write_profile_readme_returns_and_writes_exact_content(self) -> None:
        content = profile_fixture.write_profile_readme(
            self.package, "This profile establishes compliance."
        )

        self.assertEqual(
            content,
            "# Synthetic profile\n\nThis profile establishes compliance.\n",
        )
        self.assertEqual(
            (self.package / "README.md").read_text(encoding="utf-8"),
            "# Synthetic profile\n\nThis profile establishes compliance.\n",
        )

    def test_write_component_synchronizes_json_and_authoritative_source(
        self,
    ) -> None:
        profile_path = self.package / "profile.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        profile["source_boundary"]["excluded_sources"] = ["Acme Code"]

        profile_fixture.write_component(self.package, "profile.json", profile)

        expected = json.dumps(profile, indent=2) + "\n"
        self.assertEqual(profile_path.read_text(encoding="utf-8"), expected)
        self.assertTrue(profile_path.read_bytes().endswith(b"\n"))
        self.assertFalse(profile_path.read_bytes().endswith(b"\n\n"))
        self.assertIn(
            '    "excluded_sources": [\n      "Acme Code"\n    ]',
            (self.package / "PROFILE.md").read_text(encoding="utf-8"),
        )

        profile["source_boundary"]["excluded_sources"] = []
        profile_fixture.write_component(self.package, "profile.json", profile)

        self.assertNotIn("Acme Code", profile_path.read_text(encoding="utf-8"))
        self.assertNotIn(
            "Acme Code",
            (self.package / "PROFILE.md").read_text(encoding="utf-8"),
        )


class ProfileTextDiagnosticBoundaryTests(unittest.TestCase):
    LOCATION = "profiles/uk/0.1.0/README.md"

    def test_claim_boundary_returns_exact_diagnostics(self) -> None:
        cases = (
            (
                "This profile makes GOV-100 optional.",
                [
                    f"{self.LOCATION}: prohibited control weakening language"
                ],
            ),
            (
                "This profile establishes compliance. "
                "This profile establishes certification eligibility.",
                [
                    f"{self.LOCATION}: prohibited assertion "
                    "'establishes certification'",
                    f"{self.LOCATION}: prohibited assertion "
                    "'establishes compliance'",
                ],
            ),
            ("This profile does not ensure legal compliance.", []),
            (
                'The prohibited assertion "This profile ensures legal '
                'compliance." is quoted for review.',
                [],
            ),
            (
                "The prohibited assertion that this profile ensures legal "
                "compliance is discussed here.",
                [],
            ),
        )
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(
                    validate_profiles.claim_text_diagnostics(
                        text, self.LOCATION
                    ),
                    expected,
                )

    def test_claim_boundary_deduplicates_repeated_diagnostics(self) -> None:
        text = (
            "This profile establishes compliance. "
            "This profile establishes compliance."
        )

        self.assertEqual(
            validate_profiles.claim_text_diagnostics(text, self.LOCATION),
            [
                f"{self.LOCATION}: prohibited assertion "
                "'establishes compliance'"
            ],
        )

    def test_source_authority_boundary_returns_exact_diagnostics(self) -> None:
        cases = (
            (
                "Acme Code governs this profile selection.",
                ("Acme Code",),
                [
                    f"{self.LOCATION}: prohibited source authority language"
                ],
            ),
            (
                "Acme Code does not govern this profile selection.",
                ("Acme Code",),
                [],
            ),
            (
                "Acme Code governs this profile selection.",
                (),
                [],
            ),
        )
        for text, excluded_sources, expected in cases:
            with self.subTest(
                text=text, excluded_sources=excluded_sources
            ):
                self.assertEqual(
                    validate_profiles.source_authority_text_diagnostics(
                        text, self.LOCATION, excluded_sources
                    ),
                    expected,
                )

    def test_source_authority_boundary_snapshots_excluded_sources(self) -> None:
        excluded_sources = ["Acme Code"]
        with mock.patch.object(
            validate_profiles,
            "contains_affirmative_source_authority",
            return_value=True,
        ) as classifier:
            diagnostics = (
                validate_profiles.source_authority_text_diagnostics(
                    "Acme Code governs this profile selection.",
                    self.LOCATION,
                    excluded_sources,
                )
            )
            excluded_sources.append("Later mutation")
        classifier.assert_called_once_with(
            "Acme Code governs this profile selection.", ("Acme Code",)
        )
        self.assertEqual(
            diagnostics,
            [f"{self.LOCATION}: prohibited source authority language"],
        )

    def test_text_boundaries_do_not_access_the_repository(self) -> None:
        repository_access = AssertionError(
            "text diagnostic boundaries shall not access the repository"
        )
        with (
            mock.patch.object(Path, "read_text", side_effect=repository_access),
            mock.patch.object(
                validate_profiles,
                "discover_profile_packages",
                side_effect=repository_access,
            ),
            mock.patch.object(
                validate_profiles, "load_json", side_effect=repository_access
            ),
            mock.patch.object(
                validate_profiles,
                "load_schema",
                side_effect=repository_access,
            ),
        ):
            self.assertEqual(
                validate_profiles.claim_text_diagnostics(
                    "This profile establishes compliance.", self.LOCATION
                ),
                [
                    f"{self.LOCATION}: prohibited assertion "
                    "'establishes compliance'"
                ],
            )
            self.assertEqual(
                validate_profiles.source_authority_text_diagnostics(
                    "Acme Code governs this profile selection.",
                    self.LOCATION,
                    ("Acme Code",),
                ),
                [
                    f"{self.LOCATION}: prohibited source authority language"
                ],
            )


class ProfileDiagnosticWrapperRoutingTests(unittest.TestCase):
    PROFILE_MARKER = "Profile JSON marker"
    RISK_MARKER = "Risk overlay JSON marker"
    README_MARKER = "README marker"
    SOURCE_MARKER = "PROFILE prose marker"
    EXCLUDED_SOURCES = ("Acme Code", "UK GDPR")

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.package = profile_fixture.write_valid_profile_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def loaded_marked_package(self) -> validate_profiles.ProfilePackage:
        profile_path = self.package / "profile.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        profile["scope"] = self.PROFILE_MARKER
        profile["source_boundary"]["excluded_sources"] = list(
            self.EXCLUDED_SOURCES
        )
        profile_fixture.write_component(self.package, "profile.json", profile)

        risk_path = self.package / "risk-overlays.json"
        risk_overlays = json.loads(risk_path.read_text(encoding="utf-8"))
        risk_overlays["risks"] = [
            {
                "risk_id": "RISK-MARKER",
                "statement": self.RISK_MARKER,
                "circumstances": "Synthetic marker circumstances.",
                "source_basis": ["ESAF"],
                "affected_controls": ["GOV-100"],
                "overlay_ids": ["OVERLAY-MARKER"],
            }
        ]
        profile_fixture.write_component(
            self.package, "risk-overlays.json", risk_overlays
        )
        (self.package / "README.md").write_text(
            self.README_MARKER, encoding="utf-8"
        )
        source = self.package / "PROFILE.md"
        source.write_text(
            source.read_text(encoding="utf-8")
            + f"\n{self.SOURCE_MARKER}\n",
            encoding="utf-8",
        )

        diagnostics: list[str] = []
        package = validate_profiles.load_package(
            self.root, self.package, diagnostics
        )
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(package)
        assert package is not None
        return package

    def expected_text_calls(
        self,
        package: validate_profiles.ProfilePackage,
        excluded_sources: tuple[str, ...] | None = None,
    ) -> list[mock._Call]:
        calls: list[mock._Call] = []
        for component, document in sorted(package.documents.items()):
            filename = validate_profiles.PACKAGE_FILES[component]
            relative = f"{package.relative}/{filename}"
            for location, _, value in validate_profiles.walk_json(document):
                if not isinstance(value, str):
                    continue
                complete_location = f"{relative}: {location}"
                if excluded_sources is None:
                    calls.append(mock.call(value, complete_location))
                else:
                    calls.append(
                        mock.call(
                            value, complete_location, excluded_sources
                        )
                    )

        for component in ("readme", "source"):
            filename = validate_profiles.PACKAGE_FILES[component]
            relative = f"{package.relative}/{filename}"
            text = (package.directory / filename).read_text(encoding="utf-8")
            if component == "source":
                text = validate_profiles.AUTHORITATIVE_JSON_BLOCK.sub("", text)
            if excluded_sources is None:
                calls.append(mock.call(text, relative))
            else:
                calls.append(mock.call(text, relative, excluded_sources))
        return calls

    def test_source_wrapper_routes_text_with_locations_and_exclusions(
        self,
    ) -> None:
        package = self.loaded_marked_package()
        sentinels = ["source-z", "source-a", "source-z"]
        with mock.patch.object(
            validate_profiles,
            "source_authority_text_diagnostics",
            return_value=sentinels,
        ) as boundary:
            diagnostics = validate_profiles.source_boundary_diagnostics(
                package, set()
            )

        self.assertEqual(diagnostics, ["source-a", "source-z"])
        calls = boundary.call_args_list
        self.assertEqual(
            calls,
            self.expected_text_calls(package, self.EXCLUDED_SOURCES),
        )
        self.assertIn(
            mock.call(
                self.PROFILE_MARKER,
                "profiles/uk/0.1.0/profile.json: document.scope",
                self.EXCLUDED_SOURCES,
            ),
            calls,
        )
        self.assertIn(
            mock.call(
                self.RISK_MARKER,
                "profiles/uk/0.1.0/risk-overlays.json: "
                "document.risks[0].statement",
                self.EXCLUDED_SOURCES,
            ),
            calls,
        )
        self.assertIn(
            mock.call(
                self.README_MARKER,
                "profiles/uk/0.1.0/README.md",
                self.EXCLUDED_SOURCES,
            ),
            calls,
        )
        source_calls = [
            boundary_call
            for boundary_call in calls
            if boundary_call.args[1] == "profiles/uk/0.1.0/PROFILE.md"
        ]
        self.assertEqual(len(source_calls), 1)
        source_text = source_calls[0].args[0]
        self.assertIn(self.SOURCE_MARKER, source_text)
        self.assertNotIn(self.PROFILE_MARKER, source_text)
        self.assertNotIn(self.RISK_MARKER, source_text)

    def test_claim_wrapper_routes_text_with_complete_locations(self) -> None:
        package = self.loaded_marked_package()
        sentinels = ["claim-z", "claim-a", "claim-z"]
        with mock.patch.object(
            validate_profiles,
            "claim_text_diagnostics",
            return_value=sentinels,
        ) as boundary:
            diagnostics = validate_profiles.claim_diagnostics(package)

        self.assertEqual(diagnostics, ["claim-a", "claim-z"])
        calls = boundary.call_args_list
        self.assertEqual(calls, self.expected_text_calls(package))
        self.assertIn(
            mock.call(
                self.PROFILE_MARKER,
                "profiles/uk/0.1.0/profile.json: document.scope",
            ),
            calls,
        )
        self.assertIn(
            mock.call(
                self.RISK_MARKER,
                "profiles/uk/0.1.0/risk-overlays.json: "
                "document.risks[0].statement",
            ),
            calls,
        )
        self.assertIn(
            mock.call(
                self.README_MARKER,
                "profiles/uk/0.1.0/README.md",
            ),
            calls,
        )
        source_calls = [
            boundary_call
            for boundary_call in calls
            if boundary_call.args[1] == "profiles/uk/0.1.0/PROFILE.md"
        ]
        self.assertEqual(len(source_calls), 1)
        source_text = source_calls[0].args[0]
        self.assertIn(self.SOURCE_MARKER, source_text)
        self.assertNotIn(self.PROFILE_MARKER, source_text)
        self.assertNotIn(self.RISK_MARKER, source_text)

    def test_source_wrapper_keeps_unresolved_risk_basis_checks(self) -> None:
        package = self.loaded_marked_package()
        package.documents["risk_overlays"]["risks"] = [
            {"source_basis": ["Outside source"]}
        ]
        with mock.patch.object(
            validate_profiles,
            "source_authority_text_diagnostics",
            return_value=[],
        ):
            diagnostics = validate_profiles.source_boundary_diagnostics(
                package, set()
            )

        self.assertEqual(
            diagnostics,
            [
                "profiles/uk/0.1.0/risk-overlays.json: "
                "document.risks[0].source_basis[0]: unresolved risk "
                "source basis 'Outside source'"
            ],
        )

    def test_claim_wrapper_keeps_prohibited_structural_field_checks(
        self,
    ) -> None:
        package = self.loaded_marked_package()
        package.documents["profile"]["nested"] = {
            "maturity_scale": ["local-one"]
        }
        package.documents["external_references"]["nested"] = {
            "supported-outcome": {"relationships": []}
        }
        with mock.patch.object(
            validate_profiles, "claim_text_diagnostics", return_value=[]
        ):
            diagnostics = validate_profiles.claim_diagnostics(package)

        self.assertEqual(
            diagnostics,
            [
                "profiles/uk/0.1.0/external-references.json: "
                "document.nested.supported-outcome.relationships: prohibited "
                "external-reference field 'relationships'",
                "profiles/uk/0.1.0/external-references.json: "
                "document.nested.supported-outcome: prohibited "
                "external-reference field 'supported-outcome'",
                "profiles/uk/0.1.0/profile.json: "
                "document.nested.maturity_scale: prohibited profile-local "
                "maturity field 'maturity_scale'",
            ],
        )


class ProfileLanguageInventoryTests(unittest.TestCase):
    EXPECTED_METHOD_LEDGER = (
        ("test_additional_assurance_claim_forms_are_rejected", 5, 5),
        ("test_additional_assurance_denials_and_discussion_are_allowed", 6, 6),
        ("test_additional_control_weakening_forms_are_rejected", 6, 6),
        ("test_additional_weakening_denials_and_discussion_are_allowed", 5, 5),
        ("test_affirmative_claim_after_denied_clause_is_rejected", 2, 2),
        ("test_affirmative_weakening_after_denial_is_rejected", 2, 2),
        ("test_approval_subject_voice_and_aspect_cross_product", 24, 24),
        ("test_assurance_voice_tense_and_aspect_grammar_matrix", 20, 20),
        ("test_bounded_adverb_slots_cross_product", 35, 35),
        ("test_common_affirmative_control_weakening_is_rejected", 16, 16),
        ("test_common_affirmative_profile_claim_variants_are_rejected", 30, 30),
        ("test_contrast_clause_boundaries_do_not_mask_prohibited_language", 18, 18),
        ("test_declared_generic_authority_passive_aspect_cross_product", 9, 8),
        ("test_direct_weakening_object_and_complement_are_bounded", 2, 2),
        ("test_dynamic_authority_bounded_adverb_cross_product", 19, 19),
        ("test_establishes_profile_claim_denials_are_allowed", 3, 3),
        ("test_establishes_profile_claim_quotations_are_allowed", 3, 3),
        ("test_establishes_profile_claim_variants_are_rejected", 3, 3),
        ("test_excluded_source_supply_and_derivation_are_rejected", 8, 8),
        ("test_excluded_source_supply_and_derivation_polarity_pairs", 20, 20),
        ("test_explicit_control_weakening_denials_are_allowed", 18, 18),
        ("test_extended_polarity_and_metalinguistic_matrix", 11, 11),
        ("test_final_review_claim_assertions_are_rejected", 9, 9),
        ("test_final_review_claim_polarity_and_clause_pairs", 28, 28),
        ("test_identified_excluded_source_supply_forms_are_rejected", 2, 2),
        ("test_identified_excluded_source_supply_polarity_pairs", 8, 8),
        ("test_later_metalinguistic_discussion_does_not_mask_assertions", 3, 3),
        ("test_mapping_direction_and_authority_grammar_matrix", 13, 13),
        ("test_mapping_direction_form_and_aspect_cross_product", 38, 38),
        ("test_metalinguistic_context_is_bounded_to_the_assertion", 4, 4),
        ("test_natural_perfect_mandatory_denial_and_discussion_pairs", 18, 18),
        ("test_natural_perfect_mandatory_placement_cross_product", 4, 4),
        ("test_negated_rejection_head_cross_product", 12, 12),
        ("test_negation_binding_complement_and_insertion_cross_product", 7, 7),
        ("test_negative_modifiers_remain_polarity_cross_product", 9, 9),
        ("test_new_control_weakening_quotations_are_allowed", 12, 12),
        ("test_new_profile_claim_denials_are_allowed", 18, 18),
        ("test_new_profile_claim_quotations_and_discussion_are_allowed", 44, 22),
        ("test_omit_skip_and_reduce_control_forms_are_rejected", 11, 11),
        ("test_omit_skip_and_reduce_polarity_pairs", 15, 15),
        ("test_passive_affirmative_control_weakening_is_rejected", 8, 8),
        ("test_passive_control_weakening_denials_are_allowed", 8, 8),
        ("test_passive_control_weakening_quotations_are_allowed", 8, 8),
        ("test_polarity_is_bound_to_the_assertion_head", 2, 0),
        ("test_postposed_denial_agent_vs_rhetorical_cross_product", 9, 9),
        ("test_postposed_denial_and_rejection_polarity_cross_product", 17, 17),
        ("test_postposed_denial_complement_boundary_cross_product", 30, 30),
        ("test_postposed_possessive_rhetorical_suffix_cross_product", 16, 16),
        ("test_postposed_terminal_and_qualified_denial_cross_product", 12, 12),
        ("test_profile_specific_claim_denials_are_allowed", 7, 7),
        ("test_profile_specific_claim_quotations_are_allowed", 8, 8),
        ("test_profile_specific_positive_claims_are_rejected", 4, 4),
        ("test_readiness_confirmation_requires_positive_establishment", 2, 2),
        ("test_reordered_mapping_and_general_authority_are_rejected", 4, 4),
        ("test_reordered_mapping_and_general_authority_denials_are_allowed", 4, 4),
        ("test_second_review_claim_word_order_polarity_pairs", 16, 16),
        ("test_second_review_claim_word_orders_are_rejected", 4, 4),
        ("test_second_review_direct_weakening_forms_are_rejected", 2, 2),
        ("test_second_review_direct_weakening_polarity_pairs", 8, 8),
        ("test_source_authority_after_denied_clause_is_rejected", 2, 0),
        ("test_source_authority_denials_and_discussion_are_allowed", 4, 4),
        ("test_source_boundary_rejects_excluded_authority_claims", 2, 2),
        ("test_third_review_bounded_nonweakening_semantic_variations", 4, 4),
        ("test_third_review_excluded_source_supply_aspect_and_voice", 20, 20),
        ("test_third_review_passive_aspect_claim_families", 30, 30),
        ("test_third_review_progressive_direct_weakening_forms", 20, 20),
        ("test_third_review_readiness_explicit_denial_family", 11, 10),
        ("test_unrelated_denial_does_not_mask_later_control_weakening", 2, 2),
        ("test_weakening_aspect_and_state_cross_product", 24, 24),
        ("test_weakening_aspect_denial_and_metalinguistic_pairs", 13, 13),
        ("test_weakening_cross_product_denials_and_claim_frames", 17, 17),
        ("test_weakening_state_grammar_matrix", 24, 24),
        ("test_weakening_subject_modal_and_state_cross_product", 46, 46),
    )
    EXPECTED_SOURCE_DISTRIBUTION = {
        (): 772,
        ("UK GDPR",): 87,
        ("Acme Code",): 28,
        ("UK GDPR", "Cyber Essentials"): 13,
        ("UK GDPR", "NCSC", "Cyber Essentials"): 8,
    }

    def setUp(self) -> None:
        self.inventory = profile_language_cases.profile_language_inventory()

    def validate(
        self,
        *,
        cases: object | None = None,
        methods: object | None = None,
        exclusions: object | None = None,
        expected_sha256: str | None = None,
    ) -> profile_language_cases.ProfileLanguageInventory:
        return profile_language_cases.validate_profile_language_inventory(
            self.inventory.cases if cases is None else cases,
            self.inventory.methods if methods is None else methods,
            self.inventory.exclusions if exclusions is None else exclusions,
            (
                profile_language_cases.EXPECTED_POPULATION_SHA256
                if expected_sha256 is None
                else expected_sha256
            ),
        )

    def test_inventory_matches_authoritative_population(self) -> None:
        self.assertEqual(
            tuple(
                (
                    baseline.method_name,
                    baseline.validate_calls,
                    baseline.successful_subtests,
                )
                for baseline in self.inventory.methods
            ),
            self.EXPECTED_METHOD_LEDGER,
        )
        self.assertEqual(len(self.inventory.methods), 73)
        self.assertEqual(len(self.inventory.cases), 908)
        self.assertEqual(
            len({case.case_id for case in self.inventory.cases}), 908
        )
        distribution = {
            sources: sum(
                case.excluded_sources == sources
                for case in self.inventory.cases
            )
            for sources in self.EXPECTED_SOURCE_DISTRIBUTION
        }
        self.assertEqual(distribution, self.EXPECTED_SOURCE_DISTRIBUTION)

    def test_inventory_case_shape_is_immutable_and_canonical(self) -> None:
        allowed_families = (
            ("claim",),
            ("source_authority",),
            ("claim", "source_authority"),
        )
        for case in self.inventory.cases:
            with self.subTest(case_id=case.case_id):
                self.assertEqual(
                    case.location, "profiles/uk/0.1.0/README.md"
                )
                self.assertIsInstance(case.diagnostic_families, tuple)
                self.assertIn(case.diagnostic_families, allowed_families)
                self.assertTrue(
                    all(
                        family in ("claim", "source_authority")
                        for family in case.diagnostic_families
                    )
                )
                self.assertIsInstance(case.excluded_sources, tuple)
                self.assertIsInstance(case.expected_diagnostics, tuple)
                self.assertEqual(
                    case.expected_diagnostics,
                    tuple(sorted(set(case.expected_diagnostics))),
                )

    def test_inventory_exclusion_ledger_is_exact(self) -> None:
        self.assertEqual(
            self.inventory.exclusions,
            (
                profile_language_cases.ExcludedMethodBaseline(
                    "test_recommended_selection_rejects_mandatory_synonyms",
                    3,
                    3,
                    "Tests structured control-selection rationale modality, not a claim, weakening, or source-authority classifier.",
                ),
                profile_language_cases.ExcludedMethodBaseline(
                    "test_risk_source_basis_must_resolve",
                    2,
                    2,
                    "Tests risk source_basis reference resolution and integrity, which remain in the source-boundary wrapper.",
                ),
                profile_language_cases.ExcludedMethodBaseline(
                    "test_risk_source_basis_accepts_controls_and_permitted_sources",
                    2,
                    2,
                    "Tests the risk source_basis allowlist and reference behavior, not narrative source-authority language.",
                ),
                profile_language_cases.ExcludedMethodBaseline(
                    "test_malformed_control_catalog_is_a_sanitized_content_failure",
                    6,
                    6,
                    "Tests malformed catalog parsing, CLI content-failure behavior, and path sanitization.",
                ),
                profile_language_cases.ExcludedMethodBaseline(
                    "test_cli_reports_unresolvable_schema_reference_with_exit_two",
                    2,
                    0,
                    "Tests schema reference resolution, operational-error sanitization, and CLI exit code 2.",
                ),
            ),
        )

    def assert_invalid(
        self,
        message: str,
        *,
        cases: object | None = None,
        methods: object | None = None,
        exclusions: object | None = None,
    ) -> None:
        with self.assertRaises(ValueError) as captured:
            self.validate(cases=cases, methods=methods, exclusions=exclusions)
        self.assertEqual(str(captured.exception), message)

    def test_inventory_rejects_missing_method(self) -> None:
        method = self.inventory.methods[-1].method_name
        self.assert_invalid(
            f"missing method baseline: {method}",
            methods=self.inventory.methods[:-1],
        )

    def test_inventory_rejects_extra_method(self) -> None:
        extra = profile_language_cases.MethodBaseline(
            "test_extra_method", 0, 0
        )
        self.assert_invalid(
            "unexpected method baseline: test_extra_method",
            methods=(*self.inventory.methods, extra),
        )

    def test_inventory_rejects_wrong_per_method_count(self) -> None:
        baseline = self.inventory.methods[0]
        methods = (
            replace(baseline, validate_calls=baseline.validate_calls + 1),
            *self.inventory.methods[1:],
        )
        self.assert_invalid(
            (
                f"case count mismatch for {baseline.method_name}: "
                f"expected {baseline.validate_calls + 1}, "
                f"got {baseline.validate_calls}"
            ),
            methods=methods,
        )

    def test_inventory_rejects_duplicate_ledger_method(self) -> None:
        method = self.inventory.methods[0].method_name
        self.assert_invalid(
            f"duplicate method baseline: {method}",
            methods=(*self.inventory.methods, self.inventory.methods[0]),
        )

    def test_inventory_rejects_duplicate_case_identifier(self) -> None:
        duplicate = replace(
            self.inventory.cases[1],
            case_id=self.inventory.cases[0].case_id,
        )
        self.assert_invalid(
            f"duplicate case identifier: {duplicate.case_id}",
            cases=(self.inventory.cases[0], duplicate, *self.inventory.cases[2:]),
        )

    def test_inventory_rejects_invalid_family_tuples(self) -> None:
        case = self.inventory.cases[0]
        for families in (
            (),
            ("claim", "claim"),
            ("source_authority", "claim"),
            ("unknown",),
        ):
            with self.subTest(families=families):
                self.assert_invalid(
                    (
                        f"invalid diagnostic families for case "
                        f"{case.case_id}: {families!r}"
                    ),
                    cases=(
                        replace(case, diagnostic_families=families),
                        *self.inventory.cases[1:],
                    ),
                )

    def test_inventory_rejects_mutable_excluded_sources(self) -> None:
        case = self.inventory.cases[0]
        self.assert_invalid(
            f"excluded_sources must be a tuple for case {case.case_id}",
            cases=(
                replace(case, excluded_sources=[]),
                *self.inventory.cases[1:],
            ),
        )

    def test_inventory_rejects_unsorted_expected_diagnostics(self) -> None:
        index, case = next(
            (index, case)
            for index, case in enumerate(self.inventory.cases)
            if len(case.expected_diagnostics) > 1
        )
        cases = list(self.inventory.cases)
        cases[index] = replace(
            case, expected_diagnostics=tuple(reversed(case.expected_diagnostics))
        )
        self.assert_invalid(
            f"expected diagnostics must be sorted for case {case.case_id}",
            cases=tuple(cases),
        )

    def test_inventory_rejects_duplicate_expected_diagnostics(self) -> None:
        index, case = next(
            (index, case)
            for index, case in enumerate(self.inventory.cases)
            if case.expected_diagnostics
        )
        cases = list(self.inventory.cases)
        cases[index] = replace(
            case,
            expected_diagnostics=(
                *case.expected_diagnostics,
                case.expected_diagnostics[0],
            ),
        )
        self.assert_invalid(
            f"duplicate expected diagnostic for case {case.case_id}",
            cases=tuple(cases),
        )

    def test_inventory_rejects_wrong_source_distribution(self) -> None:
        case = self.inventory.cases[0]
        self.assertEqual(case.excluded_sources, ())
        self.assert_invalid(
            "excluded-source distribution mismatch",
            cases=(
                replace(case, excluded_sources=("UK GDPR",)),
                *self.inventory.cases[1:],
            ),
        )

    def test_inventory_rejects_stale_digest(self) -> None:
        case = self.inventory.cases[0]
        self.assert_invalid(
            "population digest mismatch",
            cases=(
                replace(case, text=case.text + "x"),
                *self.inventory.cases[1:],
            ),
        )


class ProfileHotPathEquivalenceCommandTests(unittest.TestCase):
    CANDIDATE = "1" * 40
    OTHER_CANDIDATE = "2" * 40

    def setUp(self) -> None:
        self.root = Path("C:/private/injected-checkout")

    @staticmethod
    def completed(
        stdout: bytes = b"",
        *,
        returncode: int = 0,
        stderr: bytes = b"",
    ) -> subprocess.CompletedProcess[bytes]:
        return subprocess.CompletedProcess(
            args=["git"],
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
        )

    def runner_for(
        self, *results: subprocess.CompletedProcess[bytes]
    ) -> mock.Mock:
        return mock.Mock(side_effect=results)

    def assert_safe_error(
        self,
        runner: mock.Mock,
        *,
        candidate: str | None = None,
    ) -> None:
        with self.assertRaises(
            verify_profile_hot_path_equivalence.ProfileHotPathEquivalenceError
        ) as captured:
            verify_profile_hot_path_equivalence.require_exact_candidate(
                self.root,
                self.CANDIDATE if candidate is None else candidate,
                runner=runner,
            )
        message = str(captured.exception)
        self.assertNotIn(str(self.root), message)
        self.assertNotIn("injected child stderr", message)
        self.assertNotIn("secret-change.txt", message)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(
            verify_profile_hot_path_equivalence,
            "verify_profile_hot_path_equivalence",
            side_effect=captured.exception,
        ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = verify_profile_hot_path_equivalence.main(
                [
                    "--check",
                    "--candidate-sha",
                    self.CANDIDATE if candidate is None else candidate,
                ],
                root=self.root,
            )
        self.assertEqual(result, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(len(stderr.getvalue().splitlines()), 1)
        self.assertNotIn(str(self.root), stderr.getvalue())
        self.assertNotIn("injected child stderr", stderr.getvalue())
        self.assertNotIn("secret-change.txt", stderr.getvalue())

    def test_candidate_must_be_an_available_lowercase_full_sha(self) -> None:
        for candidate in ("A" * 40, "1" * 12, "0" * 40):
            with self.subTest(candidate=candidate):
                runner = mock.Mock()
                self.assert_safe_error(runner, candidate=candidate)
                runner.assert_not_called()

    def test_candidate_must_match_a_clean_checkout(self) -> None:
        failures = (
            (
                self.completed((self.OTHER_CANDIDATE + "\n").encode()),
            ),
            (
                self.completed(returncode=1),
            ),
            (
                self.completed(
                    (self.CANDIDATE + "\n").encode(),
                    stderr=b"injected child stderr",
                ),
            ),
            (
                self.completed((self.CANDIDATE + "\n").encode()),
                self.completed(b" M tracked.txt\n"),
            ),
            (
                self.completed((self.CANDIDATE + "\n").encode()),
                self.completed(b"?? secret-change.txt\n"),
            ),
            (
                self.completed((self.CANDIDATE + "\n").encode()),
                self.completed(returncode=1),
            ),
            (
                self.completed((self.CANDIDATE + "\n").encode()),
                self.completed(stderr=b"injected child stderr"),
            ),
        )
        for results in failures:
            with self.subTest(results=results):
                self.assert_safe_error(self.runner_for(*results))

    def test_clean_matching_detached_checkout_is_accepted(self) -> None:
        runner = self.runner_for(
            self.completed((self.CANDIDATE + "\n").encode()),
            self.completed(),
        )

        verify_profile_hot_path_equivalence.require_exact_candidate(
            self.root, self.CANDIDATE, runner=runner
        )

        self.assertEqual(
            runner.call_args_list,
            [
                mock.call(
                    ["git", "rev-parse", "--verify", "HEAD"],
                    cwd=self.root,
                    shell=False,
                    capture_output=True,
                ),
                mock.call(
                    [
                        "git",
                        "status",
                        "--porcelain=v1",
                        "--untracked-files=all",
                    ],
                    cwd=self.root,
                    shell=False,
                    capture_output=True,
                ),
            ],
        )

    def test_main_failure_is_nonzero_and_sanitized(self) -> None:
        unsafe_path = str(self.root)

        def fail_candidate_check(*_args: object, **_kwargs: object) -> object:
            runner = self.runner_for(
                self.completed((self.CANDIDATE + "\n").encode()),
                self.completed(
                    b"?? secret-change.txt\n",
                    stderr=b"injected child stderr",
                ),
            )
            return verify_profile_hot_path_equivalence.require_exact_candidate(
                self.root, self.CANDIDATE, runner=runner
            )

        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(
            verify_profile_hot_path_equivalence,
            "verify_profile_hot_path_equivalence",
            side_effect=fail_candidate_check,
        ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = verify_profile_hot_path_equivalence.main(
                ["--check", "--candidate-sha", self.CANDIDATE],
                root=self.root,
            )

        self.assertEqual(result, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(len(stderr.getvalue().splitlines()), 1)
        self.assertNotIn(unsafe_path, stderr.getvalue())
        self.assertNotIn("injected child stderr", stderr.getvalue())
        self.assertNotIn("secret-change.txt", stderr.getvalue())

    def test_main_prints_the_exact_pass_record(self) -> None:
        expected = verify_profile_hot_path_equivalence.EquivalenceResult(
            candidate_sha=self.CANDIDATE,
            method_count=73,
            population_count=908,
            population_sha256="a" * 64,
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(
            verify_profile_hot_path_equivalence,
            "verify_profile_hot_path_equivalence",
            return_value=expected,
        ) as verify, contextlib.redirect_stdout(
            stdout
        ), contextlib.redirect_stderr(stderr):
            result = verify_profile_hot_path_equivalence.main(
                ["--check", "--candidate-sha", self.CANDIDATE],
                root=self.root,
            )

        self.assertEqual(result, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(
            stdout.getvalue(),
            "candidate_sha=1111111111111111111111111111111111111111\n"
            "method_count=73\n"
            "population_count=908\n"
            "population_sha256="
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
            "equivalence=PASS\n",
        )
        verify.assert_called_once_with(self.root, self.CANDIDATE)


class ProfileHotPathEquivalenceComparisonTests(unittest.TestCase):
    CANDIDATE = "1" * 40
    OTHER_CANDIDATE = "2" * 40
    LOCATION = "profiles/uk/0.1.0/README.md"
    CLAIM_DIAGNOSTIC = f"{LOCATION}: claim problem"
    SOURCE_DIAGNOSTIC = f"{LOCATION}: source problem"

    def setUp(self) -> None:
        self.root = Path("C:/private/injected-checkout")
        self.real_temporary_directory = tempfile.TemporaryDirectory
        self.real_json_loads = json.loads
        self.events: list[tuple[object, ...]] = []
        self.fixture_roots: list[Path] = []
        self.component_exclusions: list[list[str]] = []
        self.readme_text: dict[str, str] = {}
        self.inventory = profile_language_cases.ProfileLanguageInventory(
            cases=(
                self.case(
                    "method_one",
                    "case-claim-001",
                    "Claim text",
                    ("claim",),
                    (),
                    (self.CLAIM_DIAGNOSTIC,),
                ),
                self.case(
                    "method_one",
                    "case_source",
                    "Source text",
                    ("source_authority",),
                    ("Acme Code",),
                    (self.SOURCE_DIAGNOSTIC,),
                ),
                self.case(
                    "method_two",
                    "case_empty_reset",
                    "Neutral text",
                    ("claim", "source_authority"),
                    (),
                    (),
                ),
            ),
            methods=(
                profile_language_cases.MethodBaseline("method_one", 2, 2),
                profile_language_cases.MethodBaseline("method_two", 1, 1),
            ),
            exclusions=(),
            population_sha256="d" * 64,
        )
        self.full_outputs = {
            "Claim text": [self.CLAIM_DIAGNOSTIC],
            "Source text": [self.SOURCE_DIAGNOSTIC],
            "Neutral text": [],
        }
        self.claim_outputs = {
            "Claim text": [self.CLAIM_DIAGNOSTIC],
            "Neutral text": [],
        }
        self.source_outputs = {
            "Source text": [self.SOURCE_DIAGNOSTIC],
            "Neutral text": [],
        }

    @classmethod
    def case(
        cls,
        method_name: str,
        case_id: str,
        text: str,
        families: tuple[profile_language_cases.DiagnosticFamily, ...],
        excluded_sources: tuple[str, ...],
        expected: tuple[str, ...],
    ) -> profile_language_cases.ProfileLanguageCase:
        return profile_language_cases.ProfileLanguageCase(
            method_name=method_name,
            case_id=case_id,
            text=text,
            location=cls.LOCATION,
            diagnostic_families=families,
            excluded_sources=excluded_sources,
            expected_diagnostics=expected,
        )

    @staticmethod
    def completed(
        stdout: bytes = b"",
        *,
        returncode: int = 0,
        stderr: bytes = b"",
    ) -> subprocess.CompletedProcess[bytes]:
        return subprocess.CompletedProcess(
            args=["git"],
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
        )

    def run_comparison(
        self,
        *,
        inventory: profile_language_cases.ProfileLanguageInventory | None = None,
        runner_results: tuple[subprocess.CompletedProcess[bytes], ...]
        | None = None,
        full_outputs: dict[str, list[str]] | None = None,
        claim_outputs: dict[str, list[str]] | None = None,
        source_outputs: dict[str, list[str]] | None = None,
        full_output_factory: object | None = None,
    ) -> verify_profile_hot_path_equivalence.EquivalenceResult:
        selected_inventory = self.inventory if inventory is None else inventory
        selected_full = self.full_outputs if full_outputs is None else full_outputs
        selected_claim = (
            self.claim_outputs if claim_outputs is None else claim_outputs
        )
        selected_source = (
            self.source_outputs if source_outputs is None else source_outputs
        )
        results = list(
            runner_results
            if runner_results is not None
            else (
                self.completed((self.CANDIDATE + "\n").encode()),
                self.completed(),
                self.completed((self.CANDIDATE + "\n").encode()),
                self.completed(),
            )
        )

        def run_git(*args: object, **kwargs: object) -> object:
            self.events.append(("git", tuple(args[0])))
            if not results:
                raise AssertionError("the verifier made an extra Git call")
            return results.pop(0)

        def new_temporary_directory() -> tempfile.TemporaryDirectory[str]:
            self.events.append(("temporary_directory",))
            return self.real_temporary_directory()

        def write_fixture(fixture_root: Path) -> Path:
            self.events.append(("fixture", str(fixture_root)))
            self.fixture_roots.append(fixture_root)
            package = fixture_root / "profiles/uk/0.1.0"
            package.mkdir(parents=True)
            (package / "profile.json").write_text(
                json.dumps(
                    {"source_boundary": {"excluded_sources": ["stale"]}}
                )
                + "\n",
                encoding="utf-8",
            )
            return package

        def write_readme(package: Path, text: str) -> str:
            self.events.append(("readme", text))
            content = f"# Synthetic profile\n\n{text}\n"
            (package / "README.md").write_text(content, encoding="utf-8")
            self.readme_text[content] = text
            return content

        def load_json(value: str) -> object:
            self.events.append(("json_read",))
            return self.real_json_loads(value)

        def write_component(
            package: Path, filename: str, document: object
        ) -> None:
            profile = document
            if not isinstance(profile, dict):
                raise AssertionError("the profile record must be a dictionary")
            boundary = profile["source_boundary"]
            if not isinstance(boundary, dict):
                raise AssertionError("the source boundary must be a dictionary")
            excluded_sources = boundary["excluded_sources"]
            self.assertIsInstance(excluded_sources, list)
            self.component_exclusions.append(excluded_sources)
            self.events.append(
                ("component", filename, tuple(excluded_sources))
            )
            (package / filename).write_text(
                json.dumps(profile) + "\n", encoding="utf-8"
            )
            self.events.append(("authoritative_source",))
            (package / "PROFILE.md").write_text(
                json.dumps(profile) + "\n", encoding="utf-8"
            )

        def full_validate(fixture_root: Path) -> list[str]:
            package = fixture_root / "profiles/uk/0.1.0"
            readme = (package / "README.md").read_text(encoding="utf-8")
            text = self.readme_text[readme]
            profile = self.real_json_loads(
                (package / "profile.json").read_text(encoding="utf-8")
            )
            self.events.append(
                (
                    "full",
                    text,
                    tuple(profile["source_boundary"]["excluded_sources"]),
                    (package / "PROFILE.md").exists(),
                )
            )
            if full_output_factory is not None:
                return full_output_factory(fixture_root, text)
            return list(selected_full[text])

        def claim_boundary(readme: str, location: str) -> list[str]:
            text = self.readme_text[readme]
            self.events.append(("claim", text, location))
            return list(selected_claim[text])

        def source_boundary(
            readme: str, location: str, excluded_sources: tuple[str, ...]
        ) -> list[str]:
            text = self.readme_text[readme]
            self.events.append(
                ("source_authority", text, location, excluded_sources)
            )
            return list(selected_source[text])

        runner = mock.Mock(side_effect=run_git)
        temporary_directory = mock.Mock(side_effect=new_temporary_directory)
        inventory_accessor = mock.Mock(return_value=selected_inventory)
        fixture_writer = mock.Mock(side_effect=write_fixture)
        readme_writer = mock.Mock(side_effect=write_readme)
        component_writer = mock.Mock(side_effect=write_component)
        full_validator = mock.Mock(side_effect=full_validate)
        claim_validator = mock.Mock(side_effect=claim_boundary)
        source_validator = mock.Mock(side_effect=source_boundary)
        self.last_runner = runner
        self.last_temporary_directory = temporary_directory
        self.last_inventory_accessor = inventory_accessor
        self.last_fixture_writer = fixture_writer
        self.last_readme_writer = readme_writer
        self.last_component_writer = component_writer
        self.last_full_validator = full_validator
        self.last_claim_validator = claim_validator
        self.last_source_validator = source_validator

        with mock.patch.object(
            verify_profile_hot_path_equivalence.profile_language_cases,
            "profile_language_inventory",
            inventory_accessor,
        ), mock.patch.object(
            verify_profile_hot_path_equivalence.tempfile,
            "TemporaryDirectory",
            temporary_directory,
        ), mock.patch.object(
            verify_profile_hot_path_equivalence.profile_fixture,
            "write_valid_profile_fixture",
            fixture_writer,
        ), mock.patch.object(
            verify_profile_hot_path_equivalence.profile_fixture,
            "write_profile_readme",
            readme_writer,
        ), mock.patch.object(
            verify_profile_hot_path_equivalence.json,
            "loads",
            side_effect=load_json,
        ), mock.patch.object(
            verify_profile_hot_path_equivalence.profile_fixture,
            "write_component",
            component_writer,
        ), mock.patch.object(
            verify_profile_hot_path_equivalence.validate_profiles,
            "validate",
            full_validator,
        ), mock.patch.object(
            verify_profile_hot_path_equivalence.validate_profiles,
            "claim_text_diagnostics",
            claim_validator,
        ), mock.patch.object(
            verify_profile_hot_path_equivalence.validate_profiles,
            "source_authority_text_diagnostics",
            source_validator,
        ):
            result = (
                verify_profile_hot_path_equivalence.verify_profile_hot_path_equivalence(
                    self.root, self.CANDIDATE, runner=runner
                )
            )
        self.assertEqual(results, [])
        return result

    def assert_main_rejects(
        self,
        error: verify_profile_hot_path_equivalence.ProfileHotPathEquivalenceError,
    ) -> str:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(
            verify_profile_hot_path_equivalence,
            "verify_profile_hot_path_equivalence",
            side_effect=error,
        ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = verify_profile_hot_path_equivalence.main(
                ["--check", "--candidate-sha", self.CANDIDATE],
                root=self.root,
            )
        self.assertEqual(result, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertNotIn("equivalence=PASS", stderr.getvalue())
        self.assertEqual(len(stderr.getvalue().splitlines()), 1)
        return stderr.getvalue()

    def assert_comparison_failure(
        self,
        expected_relation: str,
        **kwargs: object,
    ) -> None:
        with self.assertRaises(
            verify_profile_hot_path_equivalence.ProfileHotPathEquivalenceError
        ) as captured:
            self.run_comparison(**kwargs)
        message = str(captured.exception)
        self.assertTrue(
            message.startswith("method_one/case-claim-001: "), message
        )
        self.assertIn(expected_relation, message)
        stderr = self.assert_main_rejects(captured.exception)
        for unsafe in (
            str(self.root),
            *(str(root) for root in self.fixture_roots),
        ):
            self.assertNotIn(unsafe, message)
            self.assertNotIn(unsafe, stderr)

    def test_every_case_uses_fresh_and_fully_reset_state(self) -> None:
        result = self.run_comparison()

        self.assertEqual(
            result,
            verify_profile_hot_path_equivalence.EquivalenceResult(
                candidate_sha=self.CANDIDATE,
                method_count=2,
                population_count=3,
                population_sha256="d" * 64,
            ),
        )
        self.last_inventory_accessor.assert_called_once_with()
        self.assertEqual(self.last_temporary_directory.call_count, 2)
        self.assertEqual(self.last_fixture_writer.call_count, 2)
        self.assertEqual(len({str(root) for root in self.fixture_roots}), 2)
        self.assertEqual(self.last_readme_writer.call_count, 3)
        self.assertEqual(self.last_component_writer.call_count, 3)
        self.assertEqual(self.component_exclusions, [[], ["Acme Code"], []])
        self.assertEqual(len({id(value) for value in self.component_exclusions}), 3)
        self.assertEqual(self.last_full_validator.call_count, 3)
        self.assertEqual(self.last_claim_validator.call_count, 2)
        self.assertEqual(self.last_source_validator.call_count, 2)
        self.assertEqual(
            self.events,
            [
                ("git", ("git", "rev-parse", "--verify", "HEAD")),
                (
                    "git",
                    (
                        "git",
                        "status",
                        "--porcelain=v1",
                        "--untracked-files=all",
                    ),
                ),
                ("temporary_directory",),
                ("fixture", str(self.fixture_roots[0])),
                ("readme", "Claim text"),
                ("json_read",),
                ("component", "profile.json", ()),
                ("authoritative_source",),
                ("full", "Claim text", (), True),
                ("claim", "Claim text", self.LOCATION),
                ("readme", "Source text"),
                ("json_read",),
                ("component", "profile.json", ("Acme Code",)),
                ("authoritative_source",),
                ("full", "Source text", ("Acme Code",), True),
                (
                    "source_authority",
                    "Source text",
                    self.LOCATION,
                    ("Acme Code",),
                ),
                ("temporary_directory",),
                ("fixture", str(self.fixture_roots[1])),
                ("readme", "Neutral text"),
                ("json_read",),
                ("component", "profile.json", ()),
                ("authoritative_source",),
                ("full", "Neutral text", (), True),
                ("claim", "Neutral text", self.LOCATION),
                (
                    "source_authority",
                    "Neutral text",
                    self.LOCATION,
                    (),
                ),
                ("git", ("git", "rev-parse", "--verify", "HEAD")),
                (
                    "git",
                    (
                        "git",
                        "status",
                        "--porcelain=v1",
                        "--untracked-files=all",
                    ),
                ),
            ],
        )
        expected_git_calls = [
            mock.call(
                ["git", "rev-parse", "--verify", "HEAD"],
                cwd=self.root,
                shell=False,
                capture_output=True,
            ),
            mock.call(
                [
                    "git",
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                ],
                cwd=self.root,
                shell=False,
                capture_output=True,
            ),
        ]
        self.assertEqual(
            self.last_runner.call_args_list,
            [*expected_git_calls, *expected_git_calls],
        )

    def test_complete_and_narrow_mismatch_is_rejected(self) -> None:
        outputs = dict(self.claim_outputs)
        outputs["Claim text"] = [self.SOURCE_DIAGNOSTIC]
        self.assert_comparison_failure(
            "complete/narrow", claim_outputs=outputs
        )

    def test_complete_and_expected_mismatch_is_rejected(self) -> None:
        first = replace(
            self.inventory.cases[0],
            expected_diagnostics=(self.SOURCE_DIAGNOSTIC,),
        )
        inventory = replace(
            self.inventory, cases=(first, *self.inventory.cases[1:])
        )
        self.assert_comparison_failure(
            "complete/expected", inventory=inventory
        )

    def test_narrow_and_expected_mismatch_is_rejected(self) -> None:
        first = replace(
            self.inventory.cases[0],
            expected_diagnostics=(self.SOURCE_DIAGNOSTIC,),
        )
        inventory = replace(
            self.inventory, cases=(first, *self.inventory.cases[1:])
        )
        outputs = dict(self.full_outputs)
        outputs["Claim text"] = [self.SOURCE_DIAGNOSTIC]
        self.assert_comparison_failure(
            "narrow/expected", inventory=inventory, full_outputs=outputs
        )

    def test_wrong_diagnostic_order_is_rejected(self) -> None:
        first = replace(
            self.inventory.cases[0],
            expected_diagnostics=(
                self.SOURCE_DIAGNOSTIC,
                self.CLAIM_DIAGNOSTIC,
            ),
        )
        inventory = replace(
            self.inventory, cases=(first, *self.inventory.cases[1:])
        )
        full_outputs = dict(self.full_outputs)
        full_outputs["Claim text"] = [
            self.CLAIM_DIAGNOSTIC,
            self.SOURCE_DIAGNOSTIC,
        ]
        claim_outputs = dict(self.claim_outputs)
        claim_outputs["Claim text"] = [
            self.CLAIM_DIAGNOSTIC,
            self.SOURCE_DIAGNOSTIC,
        ]
        self.assert_comparison_failure(
            "complete/expected",
            inventory=inventory,
            full_outputs=full_outputs,
            claim_outputs=claim_outputs,
        )

    def test_duplicate_diagnostic_is_rejected(self) -> None:
        outputs = dict(self.full_outputs)
        outputs["Claim text"] = [
            self.CLAIM_DIAGNOSTIC,
            self.CLAIM_DIAGNOSTIC,
        ]
        self.assert_comparison_failure(
            "complete/narrow", full_outputs=outputs
        )

    def test_temporary_path_in_diagnostic_is_rejected_without_leaking(self) -> None:
        def leaked_output(fixture_root: Path, _text: str) -> list[str]:
            return [f"{fixture_root.resolve()}/secret"]

        self.assert_comparison_failure(
            "temporary fixture path", full_output_factory=leaked_output
        )

    def test_postflight_head_drift_fails_after_all_comparisons(self) -> None:
        results = (
            self.completed((self.CANDIDATE + "\n").encode()),
            self.completed(),
            self.completed((self.OTHER_CANDIDATE + "\n").encode()),
        )
        with self.assertRaises(
            verify_profile_hot_path_equivalence.ProfileHotPathEquivalenceError
        ) as captured:
            self.run_comparison(runner_results=results)
        self.assertEqual(self.last_full_validator.call_count, 3)
        self.assertNotIn(str(self.root), str(captured.exception))
        stderr = self.assert_main_rejects(captured.exception)
        self.assertNotIn("equivalence=PASS", stderr)

    def test_postflight_dirty_state_fails_after_all_comparisons(self) -> None:
        dirty = b"?? injected-postflight-secret.txt\n"
        results = (
            self.completed((self.CANDIDATE + "\n").encode()),
            self.completed(),
            self.completed((self.CANDIDATE + "\n").encode()),
            self.completed(dirty),
        )
        with self.assertRaises(
            verify_profile_hot_path_equivalence.ProfileHotPathEquivalenceError
        ) as captured:
            self.run_comparison(runner_results=results)
        self.assertEqual(self.last_full_validator.call_count, 3)
        self.assertNotIn(str(self.root), str(captured.exception))
        self.assertNotIn(dirty.decode().strip(), str(captured.exception))
        stderr = self.assert_main_rejects(captured.exception)
        self.assertNotIn(dirty.decode().strip(), stderr)
        self.assertNotIn("equivalence=PASS", stderr)


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
        profile_fixture.write_component(self.package, filename, document)

    def write_readme(self, text: str) -> None:
        profile_fixture.write_profile_readme(self.package, text)

    def _assert_language_cases_through_full_validate(
        self, method_name: str
    ) -> None:
        inventory = profile_language_cases.profile_language_inventory()
        cases = inventory.cases_for_method(method_name)
        self.assertEqual(
            len(cases),
            next(
                item.validate_calls
                for item in inventory.methods
                if item.method_name == method_name
            ),
        )
        for case in cases:
            with self.subTest(case_id=case.case_id):
                profile_fixture.write_profile_readme(self.package, case.text)
                profile = self.load_component("profile.json")
                profile["source_boundary"]["excluded_sources"] = list(
                    case.excluded_sources
                )
                profile_fixture.write_component(
                    self.package, "profile.json", profile
                )
                self.assertEqual(
                    validate_profiles.validate(self.root),
                    list(case.expected_diagnostics),
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
        profile_domain, _, profile_version = profile_id.split("--")
        directory = (
            self.root / "profiles" / profile_domain / profile_version
        )
        return validate_profiles.ProfilePackage(
            directory=directory,
            relative=directory.relative_to(self.root).as_posix(),
            documents=package.documents,
        )

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
                        "evidence_types": ["record"],
                        "overlay_ids": ["OVERLAY-A"],
                        "quality_attributes": ["relevance"],
                    }
                ],
            },
        )
        return control_id

    def test_valid_population_has_no_errors(self) -> None:
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_derived_json_must_match_authoritative_markdown(self) -> None:
        path = self.package / "control-selections.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        document["selections"][0]["rationale"] = "Drifted derived record."
        profile_fixture.write_json(path, document)
        self.assert_has_error(
            "derived control-selections.json does not match authoritative "
            "Markdown block"
        )

    def test_authoritative_markdown_prose_is_claim_scanned(self) -> None:
        source = self.package / "PROFILE.md"
        source.write_text(
            source.read_text(encoding="utf-8")
            + "\nThis profile establishes compliance.\n",
            encoding="utf-8",
        )
        self.assert_has_error(
            "PROFILE.md: prohibited assertion 'establishes compliance'"
        )

    def test_authoritative_markdown_prose_respects_source_boundary(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["source_boundary"]["excluded_sources"] = ["UK GDPR"]
        self.write_component("profile.json", manifest)
        source = self.package / "PROFILE.md"
        source.write_text(
            source.read_text(encoding="utf-8")
            + "\nUK GDPR governs this profile selection.\n",
            encoding="utf-8",
        )
        self.assert_has_error(
            "PROFILE.md: prohibited source authority language"
        )

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

    def test_profile_id_domain_must_match_package_domain(self) -> None:
        package = self.loaded_package()
        for document in package.documents.values():
            document["profile_id"] = "example--jurisdiction-profile--0.1.0"
        diagnostics = validate_profiles.semantic_diagnostics(self.root, package)
        self.assertTrue(
            any(
                "profile_id domain example does not match profile domain "
                "directory uk" in item
                for item in diagnostics
            ),
            diagnostics,
        )

    def test_duplicate_profile_ids_across_packages_are_rejected(self) -> None:
        duplicate = self.root / "profiles" / "example" / "0.1.0"
        duplicate.parent.mkdir()
        shutil.copytree(self.package, duplicate)
        self.assert_has_error(
            "duplicate profile_id uk--jurisdiction-profile--0.1.0"
        )

    def test_change_history_must_include_current_profile_version(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["change_history"][0]["version"] = "9.9.9"
        self.write_component("profile.json", manifest)
        self.assert_has_error(
            "change history does not include current profile_version 0.1.0"
        )

    def test_change_history_versions_must_be_unique(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["change_history"].append(
            {
                **manifest["change_history"][0],
                "date": "2026-07-25",
            }
        )
        self.write_component("profile.json", manifest)
        self.assert_has_error("duplicate change history version 0.1.0")

    def test_change_history_versions_must_be_semver(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["change_history"][0]["version"] = "not-semver"
        self.write_component("profile.json", manifest)
        self.assert_has_error("'not-semver' does not match")

    def test_change_history_must_be_chronological(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["change_history"].append(
            {
                **manifest["change_history"][0],
                "version": "0.0.9",
                "date": "2026-07-23",
            }
        )
        self.write_component("profile.json", manifest)
        self.assert_has_error(
            "change history must be ordered by date and semantic version"
        )

    def test_control_catalog_digest_drift_is_rejected(self) -> None:
        catalog_path = self.root / "controls" / "catalog.json"
        catalog_path.write_text(
            catalog_path.read_text(encoding="utf-8") + " ",
            encoding="utf-8",
        )
        self.assert_has_error("control catalog digest does not match")

    def test_control_catalog_schema_version_drift_is_rejected(self) -> None:
        catalog_path = self.root / "controls" / "catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog["schema_version"] = "9.9.9"
        profile_fixture.write_json(catalog_path, catalog)
        self.assert_has_error("control catalog schema_version 9.9.9 does not match")

    def test_control_record_digest_drift_is_rejected(self) -> None:
        control_path = self.root / "controls" / "GOV" / "GOV-100.md"
        control_path.write_text(
            control_path.read_text(encoding="utf-8")
            + "\nUnversioned meaning change.\n",
            encoding="utf-8",
        )
        self.assert_has_error("control GOV-100 record digest does not match")

    def test_missing_control_record_pin_is_rejected(self) -> None:
        manifest = self.load_component("profile.json")
        missing = manifest["control_catalog"]["records"].pop()["id"]
        self.write_component("profile.json", manifest)
        self.assert_has_error(f"missing pinned control record {missing}")

    def test_unknown_control_record_pin_is_rejected(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["control_catalog"]["records"][0]["id"] = "GOV-999"
        manifest["control_catalog"]["records"][0]["path"] = "GOV/GOV-999.md"
        self.write_component("profile.json", manifest)
        self.assert_has_error("unknown pinned control record GOV-999")

    def test_duplicate_control_record_pin_is_rejected(self) -> None:
        manifest = self.load_component("profile.json")
        duplicate = dict(manifest["control_catalog"]["records"][0])
        duplicate["record_sha256"] = "0" * 64
        manifest["control_catalog"]["records"].append(duplicate)
        self.write_component("profile.json", manifest)
        self.assert_has_error("duplicate pinned control record GOV-100")

    def test_control_record_version_drift_is_rejected(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["control_catalog"]["records"][0]["version"] = "9.9.9"
        self.write_component("profile.json", manifest)
        self.assert_has_error(
            "control GOV-100 version does not match controls/catalog.json"
        )

    def test_control_record_status_drift_is_rejected(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["control_catalog"]["records"][0]["status"] = "retired"
        self.write_component("profile.json", manifest)
        self.assert_has_error(
            "control GOV-100 status does not match controls/catalog.json"
        )

    def test_control_record_path_drift_is_rejected(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["control_catalog"]["records"][0]["path"] = "GOV/GOV-110.md"
        self.write_component("profile.json", manifest)
        self.assert_has_error(
            "control GOV-100 path does not match controls/catalog.json"
        )

    def test_control_record_path_traversal_is_rejected_by_schema(self) -> None:
        manifest = self.load_component("profile.json")
        manifest["control_catalog"]["records"][0]["path"] = "../GOV-100.md"
        self.write_component("profile.json", manifest)
        self.assert_has_error("'../GOV-100.md' does not match")

    def test_missing_control_record_file_is_rejected(self) -> None:
        (self.root / "controls/GOV/GOV-100.md").unlink()
        self.assert_has_error(
            "unsafe or missing control path 'controls/GOV/GOV-100.md'"
        )

    def test_control_record_directory_substitution_is_rejected(self) -> None:
        path = self.root / "controls/GOV/GOV-100.md"
        path.unlink()
        path.mkdir()
        self.assert_has_error(
            "unsafe or missing control path 'controls/GOV/GOV-100.md'"
        )

    def test_control_record_symlink_substitution_is_rejected(self) -> None:
        path = self.root / "controls/GOV/GOV-100.md"
        target = self.root / "control-target.md"
        target.write_bytes(path.read_bytes())
        path.unlink()
        try:
            os.symlink(target, path)
        except OSError as error:
            self.skipTest(f"symlink creation is unavailable: {error}")
        self.assert_has_error(
            "unsafe or missing control path 'controls/GOV/GOV-100.md'"
        )

    def test_control_record_read_error_is_operational_and_sanitized(self) -> None:
        control_path = self.root / "controls/GOV/GOV-100.md"
        original_read_bytes = Path.read_bytes

        def read_bytes(path: Path) -> bytes:
            if path == control_path:
                raise PermissionError(r"C:\secret\GOV-100.md")
            return original_read_bytes(path)

        with mock.patch.object(Path, "read_bytes", new=read_bytes):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(
                    2,
                    validate_profiles.main(["--check"], root=self.root),
                )
        self.assertNotIn(r"C:\secret", stderr.getvalue())

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

    def test_recommended_selection_requires_should_modality(self) -> None:
        document = self.load_component("control-selections.json")
        document["selections"][0]["status"] = "recommended"
        document["selections"][0]["rationale"] = (
            "The organization should adopt this control because "
            "implementation is required."
        )
        self.write_component("control-selections.json", document)
        self.assert_has_error(
            "recommended selection rationale must use should and must not "
            "use shall or must"
        )

    def test_recommended_selection_rejects_mandatory_synonyms(self) -> None:
        rationales = (
            "The organization should implement this control because it is compulsory.",
            "The organization should implement this control and has to maintain it.",
            "The organization should implement this control; implementation is a requirement.",
        )
        for rationale in rationales:
            with self.subTest(rationale=rationale):
                document = self.load_component("control-selections.json")
                document["selections"][0]["status"] = "recommended"
                document["selections"][0]["rationale"] = rationale
                self.write_component("control-selections.json", document)
                self.assert_has_error(
                    "recommended selection rationale must use should and "
                    "must not use shall or must"
                )

    def test_other_evidence_type_requires_description(self) -> None:
        self.write_closed_trace_fixture()
        document = self.load_component("evidence-expectations.json")
        document["expectations"][0]["evidence_types"] = ["other"]
        self.write_component("evidence-expectations.json", document)
        self.assert_has_error("'other_type_description' is a required property")

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

    def test_generic_reference_requires_complete_non_import_statement(
        self,
    ) -> None:
        reference = self.external_references()[0]
        reference["non_import_statement"] = "Evidence is not imported."
        package = self.generic_package(external_references=[reference])
        diagnostics = validate_profiles.semantic_diagnostics(self.root, package)
        self.assertTrue(
            any("non_import_statement must be" in item for item in diagnostics),
            diagnostics,
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
        self._assert_language_cases_through_full_validate(
            'test_unrelated_denial_does_not_mask_later_control_weakening'
        )

    def test_common_affirmative_control_weakening_is_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_common_affirmative_control_weakening_is_rejected'
        )

    def test_passive_affirmative_control_weakening_is_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_passive_affirmative_control_weakening_is_rejected'
        )

    def test_passive_control_weakening_denials_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_passive_control_weakening_denials_are_allowed'
        )

    def test_passive_control_weakening_quotations_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_passive_control_weakening_quotations_are_allowed'
        )

    def test_explicit_control_weakening_denials_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_explicit_control_weakening_denials_are_allowed'
        )

    def test_new_control_weakening_quotations_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_new_control_weakening_quotations_are_allowed'
        )

    def test_affirmative_weakening_after_denial_is_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_affirmative_weakening_after_denial_is_rejected'
        )

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
        self._assert_language_cases_through_full_validate(
            'test_profile_specific_positive_claims_are_rejected'
        )

    def test_common_affirmative_profile_claim_variants_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_common_affirmative_profile_claim_variants_are_rejected'
        )

    def test_final_review_claim_assertions_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_final_review_claim_assertions_are_rejected'
        )

    def test_final_review_claim_polarity_and_clause_pairs(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_final_review_claim_polarity_and_clause_pairs'
        )

    def test_second_review_claim_word_orders_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_second_review_claim_word_orders_are_rejected'
        )

    def test_second_review_claim_word_order_polarity_pairs(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_second_review_claim_word_order_polarity_pairs'
        )

    def test_third_review_passive_aspect_claim_families(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_third_review_passive_aspect_claim_families'
        )

    def test_fourth_review_claim_and_import_auxiliary_matrix(self) -> None:
        families = (
            (
                "compliance",
                "This profile {verb} Cyber Essentials compliance",
                "Cyber Essentials compliance {verb} by this profile",
                {
                    "base": "guarantee",
                    "present": "guarantees",
                    "past": "guaranteed",
                    "participle": "guaranteed",
                    "progressive": "guaranteeing",
                },
            ),
            (
                "production readiness",
                "This profile {verb} production readiness",
                "Production readiness {verb} by this profile",
                {
                    "base": "confirm",
                    "present": "confirms",
                    "past": "confirmed",
                    "participle": "confirmed",
                    "progressive": "confirming",
                },
            ),
            (
                "imported mapping relationship",
                (
                    "Cyber Essentials provision A.1 {verb} evidence for "
                    "GOV-100"
                ),
                (
                    "Evidence for GOV-100 {verb} by Cyber Essentials "
                    "provision A.1"
                ),
                {
                    "base": "provide",
                    "present": "provides",
                    "past": "provided",
                    "participle": "provided",
                    "progressive": "providing",
                },
            ),
            (
                "imported mapping relationship",
                (
                    "This profile {verb} evidence from Cyber Essentials "
                    "provision A.1"
                ),
                (
                    "Evidence from Cyber Essentials provision A.1 {verb} by "
                    "this profile"
                ),
                {
                    "base": "import",
                    "present": "imports",
                    "past": "imported",
                    "participle": "imported",
                    "progressive": "importing",
                },
            ),
        )
        for label, active, passive, forms in families:
            for voice, template in (("active", active), ("passive", passive)):
                for affirmative_verb, denial_verb in aspect_forms(
                    **forms,
                    voice=voice,
                ):
                    assertion = template.format(verb=affirmative_verb)
                    denial = template.format(verb=denial_verb)
                    with self.subTest(
                        label=label,
                        voice=voice,
                        assertion=assertion,
                        form="affirmative",
                    ):
                        self.assertIn(
                            label,
                            validate_profiles.asserted_profile_phrases(
                                assertion
                            ),
                        )
                    with self.subTest(
                        label=label,
                        voice=voice,
                        assertion=assertion,
                        form="denial",
                    ):
                        self.assertNotIn(
                            label,
                            validate_profiles.asserted_profile_phrases(denial),
                        )
                    for form, text in (
                        ("quotation", f'The phrase "{assertion}" is prohibited.'),
                        (
                            "discussion",
                            f"The claim that {assertion} is rejected.",
                        ),
                    ):
                        with self.subTest(
                            label=label,
                            voice=voice,
                            assertion=assertion,
                            form=form,
                        ):
                            self.assertNotIn(
                                label,
                                validate_profiles.asserted_profile_phrases(
                                    text
                                ),
                            )
                    with self.subTest(
                        label=label,
                        voice=voice,
                        assertion=assertion,
                        form="coordinated",
                    ):
                        self.assertIn(
                            label,
                            validate_profiles.asserted_profile_phrases(
                                f"{denial}. However, {assertion}."
                            ),
                        )

    def test_establishes_profile_claim_variants_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_establishes_profile_claim_variants_are_rejected'
        )

    def test_establishes_profile_claim_denials_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_establishes_profile_claim_denials_are_allowed'
        )

    def test_establishes_profile_claim_quotations_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_establishes_profile_claim_quotations_are_allowed'
        )

    def test_explicit_claim_denial_is_allowed(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            "This profile does not establish compliance.\n",
            encoding="utf-8",
        )
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_profile_specific_claim_denials_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_profile_specific_claim_denials_are_allowed'
        )

    def test_metalinguistic_claim_quotation_is_allowed(self) -> None:
        (self.package / "README.md").write_text(
            "# Synthetic profile\n\n"
            'The phrase "establishes compliance" is prohibited.\n',
            encoding="utf-8",
        )
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_profile_specific_claim_quotations_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_profile_specific_claim_quotations_are_allowed'
        )

    def test_new_profile_claim_denials_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_new_profile_claim_denials_are_allowed'
        )

    def test_new_profile_claim_quotations_and_discussion_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_new_profile_claim_quotations_and_discussion_are_allowed'
        )

    def test_metalinguistic_context_is_bounded_to_the_assertion(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_metalinguistic_context_is_bounded_to_the_assertion'
        )

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
        self._assert_language_cases_through_full_validate(
            'test_affirmative_claim_after_denied_clause_is_rejected'
        )

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
        self._assert_language_cases_through_full_validate(
            'test_source_boundary_rejects_excluded_authority_claims'
        )

    def test_excluded_source_supply_and_derivation_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_excluded_source_supply_and_derivation_are_rejected'
        )

    def test_excluded_source_supply_and_derivation_polarity_pairs(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_excluded_source_supply_and_derivation_polarity_pairs'
        )

    def test_identified_excluded_source_supply_forms_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_identified_excluded_source_supply_forms_are_rejected'
        )

    def test_identified_excluded_source_supply_polarity_pairs(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_identified_excluded_source_supply_polarity_pairs'
        )

    def test_third_review_excluded_source_supply_aspect_and_voice(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_third_review_excluded_source_supply_aspect_and_voice'
        )

    def test_fourth_review_excluded_source_auxiliary_matrix(self) -> None:
        for forms in (
            {
                "base": "supply",
                "present": "supplies",
                "past": "supplied",
                "participle": "supplied",
                "progressive": "supplying",
            },
            {
                "base": "provide",
                "present": "provides",
                "past": "provided",
                "participle": "provided",
                "progressive": "providing",
            },
        ):
            for voice, template in (
                (
                    "active",
                    "UK GDPR {verb} the GOV-100 profile selection",
                ),
                (
                    "passive",
                    "The GOV-100 profile selection {verb} by UK GDPR",
                ),
            ):
                for affirmative_verb, denial_verb in aspect_forms(
                    **forms,
                    voice=voice,
                ):
                    assertion = template.format(verb=affirmative_verb)
                    denial = template.format(verb=denial_verb)
                    with self.subTest(
                        voice=voice,
                        assertion=assertion,
                        form="affirmative",
                    ):
                        self.assertTrue(
                            validate_profiles.contains_affirmative_source_authority(
                                assertion,
                                ["UK GDPR"],
                            )
                        )
                    with self.subTest(
                        voice=voice,
                        assertion=assertion,
                        form="denial",
                    ):
                        self.assertFalse(
                            validate_profiles.contains_affirmative_source_authority(
                                denial,
                                ["UK GDPR"],
                            )
                        )
                    for form, text in (
                        ("quotation", f'The phrase "{assertion}" is prohibited.'),
                        (
                            "discussion",
                            f"The claim that {assertion} is rejected.",
                        ),
                    ):
                        with self.subTest(
                            voice=voice,
                            assertion=assertion,
                            form=form,
                        ):
                            self.assertFalse(
                                validate_profiles.contains_affirmative_source_authority(
                                    text,
                                    ["UK GDPR"],
                                )
                            )
                    with self.subTest(
                        voice=voice,
                        assertion=assertion,
                        form="coordinated",
                    ):
                        self.assertTrue(
                            validate_profiles.contains_affirmative_source_authority(
                                f"{denial}. However, {assertion}.",
                                ["UK GDPR"],
                            )
                        )

    def test_fourth_review_excluded_source_perfect_derivation(self) -> None:
        pairs = (
            (
                "The GOV-100 profile selection has been derived from UK GDPR",
                "The GOV-100 profile selection has not been derived from UK GDPR",
            ),
            (
                "The GOV-100 profile selection had been derived from UK GDPR",
                "The GOV-100 profile selection had not been derived from UK GDPR",
            ),
            (
                "The GOV-100 profile selection has been based on UK GDPR",
                "The GOV-100 profile selection has not been based on UK GDPR",
            ),
            (
                "The GOV-100 profile selection had been based on UK GDPR",
                "The GOV-100 profile selection had not been based on UK GDPR",
            ),
            (
                "UK GDPR has been the source for the GOV-100 profile selection",
                "UK GDPR has not been the source for the GOV-100 profile selection",
            ),
            (
                "UK GDPR had been the source for the GOV-100 profile selection",
                "UK GDPR had not been the source for the GOV-100 profile selection",
            ),
        )
        for assertion, denial in pairs:
            with self.subTest(assertion=assertion, form="affirmative"):
                self.assertTrue(
                    validate_profiles.contains_affirmative_source_authority(
                        assertion,
                        ["UK GDPR"],
                    )
                )
            with self.subTest(assertion=assertion, form="denial"):
                self.assertFalse(
                    validate_profiles.contains_affirmative_source_authority(
                        denial,
                        ["UK GDPR"],
                    )
                )
            for form, text in (
                ("quotation", f'The phrase "{assertion}" is prohibited.'),
                ("discussion", f"The claim that {assertion} is rejected."),
            ):
                with self.subTest(assertion=assertion, form=form):
                    self.assertFalse(
                        validate_profiles.contains_affirmative_source_authority(
                            text,
                            ["UK GDPR"],
                        )
                    )
            with self.subTest(assertion=assertion, form="coordinated"):
                self.assertTrue(
                    validate_profiles.contains_affirmative_source_authority(
                        f"{denial}. However, {assertion}.",
                        ["UK GDPR"],
                    )
                )

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
        self._assert_language_cases_through_full_validate(
            'test_source_authority_denials_and_discussion_are_allowed'
        )

    def test_source_authority_after_denied_clause_is_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_source_authority_after_denied_clause_is_rejected'
        )

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

    def test_later_metalinguistic_discussion_does_not_mask_assertions(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_later_metalinguistic_discussion_does_not_mask_assertions'
        )

    def test_additional_control_weakening_forms_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_additional_control_weakening_forms_are_rejected'
        )

    def test_omit_skip_and_reduce_control_forms_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_omit_skip_and_reduce_control_forms_are_rejected'
        )

    def test_omit_skip_and_reduce_polarity_pairs(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_omit_skip_and_reduce_polarity_pairs'
        )

    def test_second_review_direct_weakening_forms_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_second_review_direct_weakening_forms_are_rejected'
        )

    def test_second_review_direct_weakening_polarity_pairs(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_second_review_direct_weakening_polarity_pairs'
        )

    def test_third_review_progressive_direct_weakening_forms(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_third_review_progressive_direct_weakening_forms'
        )

    def test_fourth_review_direct_weakening_auxiliary_matrix(self) -> None:
        for forms in (
            {
                "base": "omit",
                "present": "omits",
                "past": "omitted",
                "participle": "omitted",
                "progressive": "omitting",
            },
            {
                "base": "skip",
                "present": "skips",
                "past": "skipped",
                "participle": "skipped",
                "progressive": "skipping",
            },
            {
                "base": "reduce",
                "present": "reduces",
                "past": "reduced",
                "participle": "reduced",
                "progressive": "reducing",
            },
        ):
            for voice, template in (
                ("active", "This profile {verb} the GOV-100 control"),
                ("passive", "GOV-100 {verb} by this profile"),
            ):
                for affirmative_verb, denial_verb in aspect_forms(
                    **forms,
                    voice=voice,
                ):
                    assertion = template.format(verb=affirmative_verb)
                    denial = template.format(verb=denial_verb)
                    with self.subTest(
                        voice=voice,
                        assertion=assertion,
                        form="affirmative",
                    ):
                        self.assertTrue(
                            validate_profiles.contains_affirmative_weakening(
                                assertion
                            )
                        )
                    with self.subTest(
                        voice=voice,
                        assertion=assertion,
                        form="denial",
                    ):
                        self.assertFalse(
                            validate_profiles.contains_affirmative_weakening(
                                denial
                            )
                        )
                    for form, text in (
                        ("quotation", f'The phrase "{assertion}" is prohibited.'),
                        (
                            "discussion",
                            f"The claim that {assertion} is rejected.",
                        ),
                    ):
                        with self.subTest(
                            voice=voice,
                            assertion=assertion,
                            form=form,
                        ):
                            self.assertFalse(
                                validate_profiles.contains_affirmative_weakening(
                                    text
                                )
                            )
                    with self.subTest(
                        voice=voice,
                        assertion=assertion,
                        form="coordinated",
                    ):
                        self.assertTrue(
                            validate_profiles.contains_affirmative_weakening(
                                f"{denial}. However, {assertion}."
                            )
                        )

    def test_direct_weakening_object_and_complement_are_bounded(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_direct_weakening_object_and_complement_are_bounded'
        )

    def test_readiness_confirmation_requires_positive_establishment(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_readiness_confirmation_requires_positive_establishment'
        )

    def test_third_review_bounded_nonweakening_semantic_variations(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_third_review_bounded_nonweakening_semantic_variations'
        )

    def test_third_review_readiness_explicit_denial_family(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_third_review_readiness_explicit_denial_family'
        )

    def test_fourth_review_safe_complement_grammar_variations(self) -> None:
        safe_weakening = (
            "This profile reduces GOV-100-related implementation risk, while preserving every requirement.",
            "This profile reduced GOV-100-related implementation risks while preserving all requirements.",
            "This profile omits GOV-100 from this illustrative list while retaining it in the complete selection ledger.",
            "This profile omitted GOV-100 from an illustrative list, while retaining it in the complete selection ledger.",
            "This profile omits GOV-100 from the illustrative list while retaining it in the complete selection ledger.",
        )
        for statement in safe_weakening:
            with self.subTest(statement=statement):
                self.assertFalse(
                    validate_profiles.contains_affirmative_weakening(statement)
                )
        safe_readiness = (
            "This profile confirms production readiness is still not established.",
            "This profile confirms production readiness has never been established.",
            "This profile confirms production readiness had never been established.",
            "This profile confirms production readiness has yet to be established.",
            "This profile confirms production readiness had yet to be established.",
        )
        for statement in safe_readiness:
            with self.subTest(statement=statement):
                self.assertNotIn(
                    "production readiness",
                    validate_profiles.asserted_profile_phrases(statement),
                )
        self.assertIn(
            "production readiness",
            validate_profiles.asserted_profile_phrases(
                "This profile confirms production readiness has never been "
                "established. However, this profile confirms production "
                "readiness is established."
            ),
        )

    def test_additional_weakening_denials_and_discussion_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_additional_weakening_denials_and_discussion_are_allowed'
        )

    def test_additional_assurance_claim_forms_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_additional_assurance_claim_forms_are_rejected'
        )

    def test_additional_assurance_denials_and_discussion_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_additional_assurance_denials_and_discussion_are_allowed'
        )

    def test_reordered_mapping_and_general_authority_are_rejected(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_reordered_mapping_and_general_authority_are_rejected'
        )

    def test_reordered_mapping_and_general_authority_denials_are_allowed(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_reordered_mapping_and_general_authority_denials_are_allowed'
        )

    def test_polarity_is_bound_to_the_assertion_head(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_polarity_is_bound_to_the_assertion_head'
        )

    def test_contrast_clause_boundaries_do_not_mask_prohibited_language(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_contrast_clause_boundaries_do_not_mask_prohibited_language'
        )

    def test_weakening_state_grammar_matrix(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_weakening_state_grammar_matrix'
        )

    def test_assurance_voice_tense_and_aspect_grammar_matrix(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_assurance_voice_tense_and_aspect_grammar_matrix'
        )

    def test_mapping_direction_and_authority_grammar_matrix(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_mapping_direction_and_authority_grammar_matrix'
        )

    def test_extended_polarity_and_metalinguistic_matrix(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_extended_polarity_and_metalinguistic_matrix'
        )

    def test_weakening_subject_modal_and_state_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_weakening_subject_modal_and_state_cross_product'
        )

    def test_weakening_cross_product_denials_and_claim_frames(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_weakening_cross_product_denials_and_claim_frames'
        )

    def test_approval_subject_voice_and_aspect_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_approval_subject_voice_and_aspect_cross_product'
        )

    def test_mapping_direction_form_and_aspect_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_mapping_direction_form_and_aspect_cross_product'
        )

    def test_declared_generic_authority_passive_aspect_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_declared_generic_authority_passive_aspect_cross_product'
        )

    def test_negation_binding_complement_and_insertion_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_negation_binding_complement_and_insertion_cross_product'
        )

    def test_postposed_denial_and_rejection_polarity_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_postposed_denial_and_rejection_polarity_cross_product'
        )

    def test_weakening_aspect_and_state_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_weakening_aspect_and_state_cross_product'
        )

    def test_weakening_aspect_denial_and_metalinguistic_pairs(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_weakening_aspect_denial_and_metalinguistic_pairs'
        )

    def test_bounded_adverb_slots_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_bounded_adverb_slots_cross_product'
        )

    def test_dynamic_authority_bounded_adverb_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_dynamic_authority_bounded_adverb_cross_product'
        )

    def test_negative_modifiers_remain_polarity_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_negative_modifiers_remain_polarity_cross_product'
        )

    def test_postposed_denial_agent_vs_rhetorical_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_postposed_denial_agent_vs_rhetorical_cross_product'
        )

    def test_negated_rejection_head_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_negated_rejection_head_cross_product'
        )

    def test_natural_perfect_mandatory_placement_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_natural_perfect_mandatory_placement_cross_product'
        )

    def test_natural_perfect_mandatory_denial_and_discussion_pairs(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_natural_perfect_mandatory_denial_and_discussion_pairs'
        )

    def test_postposed_possessive_rhetorical_suffix_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_postposed_possessive_rhetorical_suffix_cross_product'
        )

    def test_postposed_terminal_and_qualified_denial_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_postposed_terminal_and_qualified_denial_cross_product'
        )

    def test_postposed_denial_complement_boundary_cross_product(self) -> None:
        self._assert_language_cases_through_full_validate(
            'test_postposed_denial_complement_boundary_cross_product'
        )

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

    def test_malformed_control_catalog_is_a_sanitized_content_failure(self) -> None:
        path = self.root / "controls" / "catalog.json"
        cases = (
            ("{", "cannot load JSON"),
            ("[]", "root must be an object"),
            ("{}", "controls must be an array"),
            ('{"controls": {}}', "controls must be an array"),
            ('{"controls": [null]}', "controls[0] requires a string id"),
            ('{"controls": [{"id": 42}]}', "controls[0] requires a string id"),
        )
        for content, expected in cases:
            with self.subTest(content=content):
                path.write_text(content + "\n", encoding="utf-8")
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    result = validate_profiles.main(
                        ["--check"], root=self.root
                    )
                output = stderr.getvalue()
                self.assertEqual(result, 1, output)
                self.assertIn(f"controls/catalog.json: {expected}", output)
                self.assertNotIn(str(self.root), output)
                self.assertNotIn("unexpected operational error", output)

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

    def test_schema_directory_is_not_a_profile_domain(self) -> None:
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

    def test_symlinked_profile_domain_directory_is_rejected(self) -> None:
        profile_domain = self.package.parent
        outside_profile_domain = self.root / "outside" / profile_domain.name
        outside_profile_domain.parent.mkdir()
        shutil.move(str(profile_domain), outside_profile_domain)
        try:
            os.symlink(
                outside_profile_domain,
                profile_domain,
                target_is_directory=True,
            )
        except OSError as exc:
            if os.name != "nt":
                self.skipTest(f"symlink creation is unavailable: {exc}")
            junction = subprocess.run(
                [
                    "cmd",
                    "/c",
                    "mklink",
                    "/J",
                    str(profile_domain),
                    str(outside_profile_domain),
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
            if profile_domain.is_symlink():
                profile_domain.unlink()
            elif profile_domain.is_junction():
                os.rmdir(profile_domain)
            if not profile_domain.exists():
                shutil.move(str(outside_profile_domain), profile_domain)

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
