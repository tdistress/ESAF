"""Authoritative profile-language validation case inventory."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from collections.abc import Sequence
from contextlib import nullcontext
from dataclasses import dataclass
from itertools import product
from typing import Literal


DiagnosticFamily = Literal["claim", "source_authority"]
LOCATION = "profiles/uk/0.1.0/README.md"
EXPECTED_POPULATION_SHA256 = "8caf46a8e85121e53598cf17b9c04577bd9e1df3270cf08b5331bef73bf53735"
EXPECTED_SOURCE_DISTRIBUTION = {
    (): 772,
    ("UK GDPR",): 87,
    ("Acme Code",): 28,
    ("UK GDPR", "Cyber Essentials"): 13,
    ("UK GDPR", "NCSC", "Cyber Essentials"): 8,
}


@dataclass(frozen=True)
class ProfileLanguageCase:
    method_name: str
    case_id: str
    text: str
    location: str
    diagnostic_families: tuple[DiagnosticFamily, ...]
    excluded_sources: tuple[str, ...]
    expected_diagnostics: tuple[str, ...]


@dataclass(frozen=True)
class MethodBaseline:
    method_name: str
    validate_calls: int
    successful_subtests: int


@dataclass(frozen=True)
class ExcludedMethodBaseline:
    method_name: str
    validate_calls: int
    successful_subtests: int
    rationale: str


@dataclass(frozen=True)
class ProfileLanguageInventory:
    cases: tuple[ProfileLanguageCase, ...]
    methods: tuple[MethodBaseline, ...]
    exclusions: tuple[ExcludedMethodBaseline, ...]
    population_sha256: str

    def cases_for_method(self, method_name: str) -> tuple[ProfileLanguageCase, ...]:
        return tuple(case for case in self.cases if case.method_name == method_name)


METHOD_BASELINES = tuple(MethodBaseline(*values) for values in (('test_additional_assurance_claim_forms_are_rejected', 5, 5),
 ('test_additional_assurance_denials_and_discussion_are_allowed', 6, 6),
 ('test_additional_control_weakening_forms_are_rejected', 6, 6),
 ('test_additional_weakening_denials_and_discussion_are_allowed', 5, 5),
 ('test_affirmative_claim_after_denied_clause_is_rejected', 2, 2),
 ('test_affirmative_weakening_after_denial_is_rejected', 2, 2),
 ('test_approval_subject_voice_and_aspect_cross_product', 24, 24),
 ('test_assurance_voice_tense_and_aspect_grammar_matrix', 20, 20),
 ('test_bounded_adverb_slots_cross_product', 35, 35),
 ('test_common_affirmative_control_weakening_is_rejected', 16, 16),
 ('test_common_affirmative_profile_claim_variants_are_rejected', 30, 30),
 ('test_contrast_clause_boundaries_do_not_mask_prohibited_language', 18, 18),
 ('test_declared_generic_authority_passive_aspect_cross_product', 9, 8),
 ('test_direct_weakening_object_and_complement_are_bounded', 2, 2),
 ('test_dynamic_authority_bounded_adverb_cross_product', 19, 19),
 ('test_establishes_profile_claim_denials_are_allowed', 3, 3),
 ('test_establishes_profile_claim_quotations_are_allowed', 3, 3),
 ('test_establishes_profile_claim_variants_are_rejected', 3, 3),
 ('test_excluded_source_supply_and_derivation_are_rejected', 8, 8),
 ('test_excluded_source_supply_and_derivation_polarity_pairs', 20, 20),
 ('test_explicit_control_weakening_denials_are_allowed', 18, 18),
 ('test_extended_polarity_and_metalinguistic_matrix', 11, 11),
 ('test_final_review_claim_assertions_are_rejected', 9, 9),
 ('test_final_review_claim_polarity_and_clause_pairs', 28, 28),
 ('test_identified_excluded_source_supply_forms_are_rejected', 2, 2),
 ('test_identified_excluded_source_supply_polarity_pairs', 8, 8),
 ('test_later_metalinguistic_discussion_does_not_mask_assertions', 3, 3),
 ('test_mapping_direction_and_authority_grammar_matrix', 13, 13),
 ('test_mapping_direction_form_and_aspect_cross_product', 38, 38),
 ('test_metalinguistic_context_is_bounded_to_the_assertion', 4, 4),
 ('test_natural_perfect_mandatory_denial_and_discussion_pairs', 18, 18),
 ('test_natural_perfect_mandatory_placement_cross_product', 4, 4),
 ('test_negated_rejection_head_cross_product', 12, 12),
 ('test_negation_binding_complement_and_insertion_cross_product', 7, 7),
 ('test_negative_modifiers_remain_polarity_cross_product', 9, 9),
 ('test_new_control_weakening_quotations_are_allowed', 12, 12),
 ('test_new_profile_claim_denials_are_allowed', 18, 18),
 ('test_new_profile_claim_quotations_and_discussion_are_allowed', 44, 22),
 ('test_omit_skip_and_reduce_control_forms_are_rejected', 11, 11),
 ('test_omit_skip_and_reduce_polarity_pairs', 15, 15),
 ('test_passive_affirmative_control_weakening_is_rejected', 8, 8),
 ('test_passive_control_weakening_denials_are_allowed', 8, 8),
 ('test_passive_control_weakening_quotations_are_allowed', 8, 8),
 ('test_polarity_is_bound_to_the_assertion_head', 2, 0),
 ('test_postposed_denial_agent_vs_rhetorical_cross_product', 9, 9),
 ('test_postposed_denial_and_rejection_polarity_cross_product', 17, 17),
 ('test_postposed_denial_complement_boundary_cross_product', 30, 30),
 ('test_postposed_possessive_rhetorical_suffix_cross_product', 16, 16),
 ('test_postposed_terminal_and_qualified_denial_cross_product', 12, 12),
 ('test_profile_specific_claim_denials_are_allowed', 7, 7),
 ('test_profile_specific_claim_quotations_are_allowed', 8, 8),
 ('test_profile_specific_positive_claims_are_rejected', 4, 4),
 ('test_readiness_confirmation_requires_positive_establishment', 2, 2),
 ('test_reordered_mapping_and_general_authority_are_rejected', 4, 4),
 ('test_reordered_mapping_and_general_authority_denials_are_allowed', 4, 4),
 ('test_second_review_claim_word_order_polarity_pairs', 16, 16),
 ('test_second_review_claim_word_orders_are_rejected', 4, 4),
 ('test_second_review_direct_weakening_forms_are_rejected', 2, 2),
 ('test_second_review_direct_weakening_polarity_pairs', 8, 8),
 ('test_source_authority_after_denied_clause_is_rejected', 2, 0),
 ('test_source_authority_denials_and_discussion_are_allowed', 4, 4),
 ('test_source_boundary_rejects_excluded_authority_claims', 2, 2),
 ('test_third_review_bounded_nonweakening_semantic_variations', 4, 4),
 ('test_third_review_excluded_source_supply_aspect_and_voice', 20, 20),
 ('test_third_review_passive_aspect_claim_families', 30, 30),
 ('test_third_review_progressive_direct_weakening_forms', 20, 20),
 ('test_third_review_readiness_explicit_denial_family', 11, 10),
 ('test_unrelated_denial_does_not_mask_later_control_weakening', 2, 2),
 ('test_weakening_aspect_and_state_cross_product', 24, 24),
 ('test_weakening_aspect_denial_and_metalinguistic_pairs', 13, 13),
 ('test_weakening_cross_product_denials_and_claim_frames', 17, 17),
 ('test_weakening_state_grammar_matrix', 24, 24),
 ('test_weakening_subject_modal_and_state_cross_product', 46, 46)))
EXCLUDED_METHOD_BASELINES = tuple(
    ExcludedMethodBaseline(*values) for values in (('test_recommended_selection_rejects_mandatory_synonyms',
  3,
  3,
  'Tests structured control-selection rationale modality, not a claim, weakening, or '
  'source-authority classifier.'),
 ('test_risk_source_basis_must_resolve',
  2,
  2,
  'Tests risk source_basis reference resolution and integrity, which remain in the source-boundary '
  'wrapper.'),
 ('test_risk_source_basis_accepts_controls_and_permitted_sources',
  2,
  2,
  'Tests the risk source_basis allowlist and reference behavior, not narrative source-authority '
  'language.'),
 ('test_malformed_control_catalog_is_a_sanitized_content_failure',
  6,
  6,
  'Tests malformed catalog parsing, CLI content-failure behavior, and path sanitization.'),
 ('test_cli_reports_unresolvable_schema_reference_with_exit_two',
  2,
  0,
  'Tests schema reference resolution, operational-error sanitization, and CLI exit code 2.'))
)


AFFIRMATIVE_CLAIMS = (('This profile satisfies Cyber Essentials requirements.', 'scheme satisfaction'), ('This profile ensures legal compliance.', 'compliance'), ('This profile confers certification eligibility.', 'certification eligibility'), ('This profile has NCSC approval.', 'named-authority approval'), ('Cyber Essentials provision A maps to GOV-100 and supplies its external outcome.', 'imported mapping relationship'), ('Legal compliance is ensured by this profile.', 'compliance'), ('Certification eligibility is conferred by this profile.', 'certification eligibility'), ('NCSC approval is held by this profile.', 'named-authority approval'), ('GOV-100 is mapped from Cyber Essentials provision A and the external outcome is imported.', 'imported mapping relationship'), ('GOV-100 supports Cyber Essentials provision A.', 'imported mapping relationship'), ('GOV-100 satisfies Cyber Essentials provision A.', 'imported mapping relationship'), ('Cyber Essentials provision A is supported by GOV-100.', 'imported mapping relationship'), ('Cyber Essentials provision A is satisfied by GOV-100.', 'imported mapping relationship'), ('Cyber Essentials provision A supports GOV-100.', 'imported mapping relationship'), ('Cyber Essentials provision A satisfies GOV-100.', 'imported mapping relationship'), ('GOV-100 is supported by Cyber Essentials provision A.', 'imported mapping relationship'), ('GOV-100 is satisfied by Cyber Essentials provision A.', 'imported mapping relationship'), ('This profile meets Cyber Essentials requirements.', 'scheme satisfaction'), ('This profile complies with Cyber Essentials.', 'compliance'), ('This profile qualifies the organization for certification.', 'certification eligibility'), ('This profile is approved by NCSC.', 'named-authority approval'), ('NCSC approves this profile.', 'named-authority approval'))


AFFIRMATIVE_WEAKENING = ('This profile makes optional core controls.', 'This profile marks inapplicable core controls.', 'GOV-100 need not be applied.', 'This profile supersedes GOV-100.', 'The organization is exempt from GOV-100.', 'This profile lowers core control requirements.', 'GOV-100 is superseded by this profile.', 'GOV-100 is inapplicable under this profile.', 'Core control requirements are lowered by this profile.', 'This profile renders GOV-100 optional.', 'GOV-100 no longer applies.', 'GOV-100 does not apply under this profile.')


ACTIVE_ASPECT_FORMS = (('{present}', 'does not {base}'), ('{past}', 'did not {base}'), ('has {participle}', 'has not {participle}'), ('had {participle}', 'had not {participle}'), ('is {progressive}', 'is not {progressive}'), ('was {progressive}', 'was not {progressive}'), ('has been {progressive}', 'has not been {progressive}'), ('had been {progressive}', 'had not been {progressive}'))


PASSIVE_ASPECT_FORMS = (('is {participle}', 'is not {participle}'), ('was {participle}', 'was not {participle}'), ('has been {participle}', 'has not been {participle}'), ('had been {participle}', 'had not been {participle}'), ('is being {participle}', 'is not being {participle}'), ('was being {participle}', 'was not being {participle}'))


def aspect_forms(*, base: str, present: str, past: str, participle: str, progressive: str, voice: str) -> tuple[tuple[str, str], ...]:
    templates = ACTIVE_ASPECT_FORMS if voice == 'active' else PASSIVE_ASPECT_FORMS
    values = {'base': base, 'present': present, 'past': past, 'participle': participle, 'progressive': progressive}
    return tuple(((affirmative.format(**values), denial.format(**values)) for affirmative, denial in templates))


class _CaseBuilder:
    def __init__(self) -> None:
        self._profile = {"source_boundary": {"excluded_sources": []}}
        self._text: str | None = None
        self.records: list[tuple[str, tuple[str, ...]]] = []

    def write_readme(self, text: str) -> None:
        self._text = text

    def write_profile_readme_content(self, content: str) -> None:
        prefix = "# Synthetic profile\n\n"
        if not content.startswith(prefix) or not content.endswith("\n"):
            raise ValueError("profile-language builder produced an invalid README")
        self._text = content[len(prefix):-1]

    def load_component(self, filename: str) -> dict[str, object]:
        if filename != "profile.json":
            raise ValueError(f"unsupported profile-language component: {filename}")
        return copy.deepcopy(self._profile)

    def write_component(self, filename: str, document: dict[str, object]) -> None:
        if filename != "profile.json":
            raise ValueError(f"unsupported profile-language component: {filename}")
        self._profile = copy.deepcopy(document)

    def record_case(self) -> None:
        if self._text is None:
            raise ValueError("profile-language builder recorded a case without text")
        boundary = self._profile["source_boundary"]
        assert isinstance(boundary, dict)
        excluded = boundary["excluded_sources"]
        assert isinstance(excluded, list)
        self.records.append((self._text, tuple(str(item) for item in excluded)))


def _build_additional_assurance_claim_forms_are_rejected(builder):
    for text, expected in (('This profile guarantees legal compliance.', 'compliance'), ('This profile makes the organization eligible for certification.', 'certification eligibility'), ('This profile certifies the organization.', 'certification'), ('This profile has received NCSC approval.', 'named-authority approval'), ('NCSC has approved this profile.', 'named-authority approval')):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_additional_assurance_denials_and_discussion_are_allowed(builder):
    for text in ('This profile does not guarantee legal compliance.', 'This profile does not make the organization eligible for certification.', 'This profile does not certify the organization.', 'This profile has not received NCSC approval.', 'NCSC has not approved this profile.', 'The phrase "This profile guarantees legal compliance" is prohibited.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_additional_control_weakening_forms_are_rejected(builder):
    for text in ('GOV-100 is optional under this profile.', 'Core controls are optional under this profile.', 'GOV-100 shall not apply under this profile.', 'GOV-100 is not required under this profile.', 'This profile makes GOV-100 not required.', 'Under this profile, optional controls include GOV-100.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_additional_weakening_denials_and_discussion_are_allowed(builder):
    for text in ('GOV-100 is not optional under this profile.', 'Core controls are not optional under this profile.', 'GOV-100 shall apply under this profile.', 'The phrase "GOV-100 is not required" is prohibited.', 'The claim that GOV-100 is not required is discussed and rejected.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_affirmative_claim_after_denied_clause_is_rejected(builder):
    for text, expected in (('This profile does not ensure legal compliance, but it confers certification eligibility.', 'certification eligibility'), ('Cyber Essentials provision A does not map to GOV-100, yet it supplies its external outcome.', 'external outcome import')):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_affirmative_weakening_after_denial_is_rejected(builder):
    for text in ('This profile does not supersede GOV-100, but it lowers GOV-100.', 'Core controls are not marked inapplicable, yet GOV-100 need not be applied.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_approval_subject_voice_and_aspect_cross_product(builder):
    aspects = ('present', 'past', 'perfect', 'past-perfect')
    constructions = (('NCSC {verb} this profile', {'present': ('approves', 'does not approve'), 'past': ('approved', 'did not approve'), 'perfect': ('has approved', 'has not approved'), 'past-perfect': ('had approved', 'had not approved')}), ('This profile {verb} NCSC approval', {'present': ('receives', 'does not receive'), 'past': ('received', 'did not receive'), 'perfect': ('has received', 'has not received'), 'past-perfect': ('had received', 'had not received')}), ('This profile {verb} by NCSC', {'present': ('is approved', 'is not approved'), 'past': ('was approved', 'was not approved'), 'perfect': ('has been approved', 'has not been approved'), 'past-perfect': ('had been approved', 'had not been approved')}))
    for (template, forms), aspect in product(constructions, aspects):
        affirmative, denied = forms[aspect]
        with nullcontext():
            builder.write_readme(f'{template.format(verb=affirmative)}.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{template.format(verb=denied)}.')
            builder.record_case()


def _build_assurance_voice_tense_and_aspect_grammar_matrix(builder):
    cases = (('This profile guarantees legal compliance.', 'compliance'), ('This profile guaranteed legal compliance.', 'compliance'), ('This profile has guaranteed legal compliance.', 'compliance'), ('This profile proves legal compliance.', 'compliance'), ('This profile proved legal compliance.', 'compliance'), ('This profile has proven legal compliance.', 'compliance'), ('Legal compliance is ensured by this profile.', 'compliance'), ('Legal compliance was proven by this profile.', 'compliance'), ('Legal compliance has been guaranteed by this profile.', 'compliance'), ('This profile certified the organization.', 'certification'), ('This profile has certified the organization.', 'certification'), ('The organization was certified by this profile.', 'certification'), ('The organization has been certified by this profile.', 'certification'), ('This profile made the organization eligible for certification.', 'certification eligibility'), ('The organization has been made eligible for certification by this profile.', 'certification eligibility'), ('NCSC approved this profile.', 'named-authority approval'), ('NCSC has approved this profile.', 'named-authority approval'), ('This profile was approved by NCSC.', 'named-authority approval'), ('This profile has been approved by NCSC.', 'named-authority approval'), ('This profile received NCSC approval.', 'named-authority approval'))
    for text, label in cases:
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_bounded_adverb_slots_cross_product(builder):
    adverbs = ('formally', 'explicitly', 'directly', 'expressly', 'carefully')
    templates = (('NCSC has {adverb} approved this profile.', "prohibited assertion 'named-authority approval'"), ('This profile had {adverb} received NCSC approval.', "prohibited assertion 'named-authority approval'"), ('This profile has been {adverb} approved by NCSC.', "prohibited assertion 'named-authority approval'"), ('Cyber Essentials provision A has {adverb} mapped to GOV-100.', "prohibited assertion 'imported mapping relationship'"), ('Cyber Essentials provision A has been {adverb} mapped to GOV-100.', "prohibited assertion 'imported mapping relationship'"), ('GOV-100 had {adverb} mapped from Cyber Essentials provision A.', "prohibited assertion 'imported mapping relationship'"), ('GOV-100 had been {adverb} mapped from Cyber Essentials provision A.', "prohibited assertion 'imported mapping relationship'"))
    for (template, expected), adverb in product(templates, adverbs):
        with nullcontext():
            builder.write_readme(template.format(adverb=adverb))
            builder.record_case()


def _build_common_affirmative_control_weakening_is_rejected(builder):
    for text in ('This profile replaces core controls.', 'This profile alters core controls.', 'This profile relaxes core control requirements.', 'This profile makes core controls optional.', *AFFIRMATIVE_WEAKENING):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_common_affirmative_profile_claim_variants_are_rejected(builder):
    for text, expected in (('This profile provides legal sufficiency.', 'legal sufficiency'), ('This profile is externally approved.', 'external approval'), ('This profile demonstrates production readiness.', 'production readiness'), ('This profile is ready for production.', 'production readiness'), ('This profile is compliant.', 'compliance'), ('This profile is certified.', 'certification'), ('This profile is equivalent.', 'equivalence'), ('This profile is endorsed.', 'endorsement'), *AFFIRMATIVE_CLAIMS):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_contrast_clause_boundaries_do_not_mask_prohibited_language(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    cases = (('This profile guarantees legal compliance.', "assertion 'compliance'"), ('This profile supersedes GOV-100.', 'control weakening language'), ('UK GDPR governs this profile.', 'source authority language'))
    for conjunction in ('while', 'whereas', 'although', 'though', 'even though', 'however'):
        for assertion, expected in cases:
            text = f'The document discusses and rejects that claim {conjunction} {assertion}'
            with nullcontext():
                builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
                builder.record_case()


def _build_declared_generic_authority_passive_aspect_cross_product(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['Acme Code']
    builder.write_component('profile.json', profile)
    for auxiliary in ('is', 'was', 'has been', 'had been'):
        with nullcontext():
            builder.write_readme(f'This profile {auxiliary} governed by Acme Code.')
            builder.record_case()
    for auxiliary in ('is not', 'was not', 'has not been', 'had not been'):
        with nullcontext():
            builder.write_readme(f'This profile {auxiliary} governed by Acme Code.')
            builder.record_case()
    builder.write_readme('This profile is governed by Other Code.')
    builder.record_case()


def _build_direct_weakening_object_and_complement_are_bounded(builder):
    for statement in ('This profile reduces GOV-100 implementation risk while preserving every requirement.', 'This profile omits GOV-100 from this illustrative list while retaining it in the complete selection ledger.'):
        with nullcontext():
            builder.write_readme(statement)
            builder.record_case()


def _build_dynamic_authority_bounded_adverb_cross_product(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['Acme Code']
    builder.write_component('profile.json', profile)
    for auxiliary, adverb in product(('is', 'was', 'has been', 'had been'), ('formally', 'explicitly', 'directly', 'carefully')):
        with nullcontext():
            builder.write_readme(f'This profile {auxiliary} {adverb} governed by Acme Code.')
            builder.record_case()
    for modifier in ('not', 'never', 'by no means'):
        with nullcontext():
            builder.write_readme(f'This profile has {modifier} been governed by Acme Code.')
            builder.record_case()


def _build_establishes_profile_claim_denials_are_allowed(builder):
    for outcome in ('legal sufficiency', 'external approval', 'production readiness'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\nThis profile does not establish {outcome}.\n')
            builder.record_case()


def _build_establishes_profile_claim_quotations_are_allowed(builder):
    for phrase in ('establishes legal sufficiency', 'establishes external approval', 'establishes production readiness'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\nThe phrase "{phrase}" is prohibited.\n')
            builder.record_case()


def _build_establishes_profile_claim_variants_are_rejected(builder):
    for text, expected in (('This profile establishes legal sufficiency.', 'legal sufficiency'), ('This profile establishes external approval.', 'external approval'), ('This profile establishes production readiness.', 'production readiness')):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_excluded_source_supply_and_derivation_are_rejected(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    assertions = ('UK GDPR supplies this profile selection.', 'This profile selection is supplied by UK GDPR.', 'UK GDPR is the source for this profile requirement.', 'UK GDPR provides this profile requirement.', 'This profile requirement is provided by UK GDPR.', 'This profile selection derives from UK GDPR.', 'This profile selection is derived from UK GDPR.', 'This profile requirement is based on UK GDPR.')
    for assertion in assertions:
        with nullcontext():
            builder.write_readme(assertion)
            builder.record_case()


def _build_excluded_source_supply_and_derivation_polarity_pairs(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    pairs = (('UK GDPR supplies this profile selection', 'UK GDPR does not supply this profile selection.'), ('This profile selection is supplied by UK GDPR', 'This profile selection is not supplied by UK GDPR.'), ('UK GDPR is the source for this profile requirement', 'UK GDPR is not the source for this profile requirement.'), ('This profile selection derives from UK GDPR', 'This profile selection does not derive from UK GDPR.'), ('This profile requirement is based on UK GDPR', 'This profile requirement is not based on UK GDPR.'))
    for assertion, denial in pairs:
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{assertion}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that {assertion} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, {assertion}.')
            builder.record_case()


def _build_explicit_control_weakening_denials_are_allowed(builder):
    for text in ('This profile does not replace core controls.', 'No profile alters core controls.', 'This profile does not relax or make core controls optional.', 'This profile replaces no core controls.', 'This profile replaces neither core control.', 'This profile does not make optional core controls.', 'This profile does not mark inapplicable core controls.', 'GOV-100 must be applied.', 'This profile does not supersede GOV-100.', 'The organization is not exempt from GOV-100.', 'This profile does not lower core control requirements.', 'GOV-100 is not superseded by this profile.', 'GOV-100 is not inapplicable under this profile.', 'Core control requirements are not lowered by this profile.', 'This profile does not render GOV-100 optional.', 'GOV-100 remains applicable.', 'This profile renders GOV-100 mandatory.', 'GOV-100 applies under this profile.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_extended_polarity_and_metalinguistic_matrix(builder):
    allowed = ('This profile does not under any circumstances guarantee legal compliance.', 'GOV-100 is superseded by neither this profile nor any overlay.', 'The claim that GOV-100 is optional is false.', 'The claim that this profile guarantees legal compliance is false.', 'The claim that GOV-100 shall be optional is rejected.', 'The assertion that this profile has guaranteed legal compliance is denied.', 'Legal compliance has not been guaranteed by this profile.', 'Legal compliance is guaranteed by no profile.', 'Legal compliance is guaranteed by neither this profile nor any overlay.', 'NCSC did not approve this profile.', 'The phrase "This profile proved legal compliance" is prohibited.')
    for text in allowed:
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_final_review_claim_assertions_are_rejected(builder):
    cases = (('This profile guarantees compliance with Cyber Essentials.', "prohibited assertion 'compliance'"), ('NCSC endorses this profile.', "prohibited assertion 'endorsement'"), ('This profile confirms production readiness.', "prohibited assertion 'production readiness'"), ('The organization is eligible for certification under this profile.', "prohibited assertion 'certification eligibility'"), ('This profile has obtained NCSC approval.', "prohibited assertion 'named-authority approval'"), ('Cyber Essentials provision A.1 corresponds to GOV-100.', "prohibited assertion 'imported mapping relationship'"), ('Cyber Essentials provision A.1 provides evidence for GOV-100.', "prohibited assertion 'imported mapping relationship'"), ('GOV-100 corresponds to Cyber Essentials provision A.1.', "prohibited assertion 'imported mapping relationship'"), ('GOV-100 provides evidence for Cyber Essentials provision A.1.', "prohibited assertion 'imported mapping relationship'"))
    for assertion, expected in cases:
        with nullcontext():
            builder.write_readme(assertion)
            builder.record_case()


def _build_final_review_claim_polarity_and_clause_pairs(builder):
    cases = (('This profile guarantees compliance with Cyber Essentials', 'This profile does not guarantee compliance with Cyber Essentials.', 'compliance'), ('NCSC endorses this profile', 'NCSC does not endorse this profile.', 'endorsement'), ('This profile confirms production readiness', 'This profile does not confirm production readiness.', 'production readiness'), ('The organization is eligible for certification under this profile', 'The organization is not eligible for certification under this profile.', 'certification eligibility'), ('This profile has obtained NCSC approval', 'This profile has not obtained NCSC approval.', 'named-authority approval'), ('Cyber Essentials provision A.1 corresponds to GOV-100', 'Cyber Essentials provision A.1 does not correspond to GOV-100.', 'imported mapping relationship'), ('Cyber Essentials provision A.1 provides evidence for GOV-100', 'Cyber Essentials provision A.1 does not provide evidence for GOV-100.', 'imported mapping relationship'))
    for assertion, denial, expected in cases:
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{assertion}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that {assertion} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, {assertion}.')
            builder.record_case()


def _build_identified_excluded_source_supply_forms_are_rejected(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    for assertion in ('UK GDPR supplies the GOV-100 profile selection', 'This profile selection for GOV-100 is supplied by UK GDPR'):
        with nullcontext():
            builder.write_readme(f'{assertion}.')
            builder.record_case()


def _build_identified_excluded_source_supply_polarity_pairs(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    pairs = (('UK GDPR supplies the GOV-100 profile selection', 'UK GDPR does not supply the GOV-100 profile selection.'), ('This profile selection for GOV-100 is supplied by UK GDPR', 'This profile selection for GOV-100 is not supplied by UK GDPR.'))
    for assertion, denial in pairs:
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{assertion}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that {assertion} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, {assertion}.')
            builder.record_case()


def _build_later_metalinguistic_discussion_does_not_mask_assertions(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    for text, expected in (('This profile ensures legal compliance, and the document discusses that claim.', "prohibited assertion 'compliance'"), ('This profile supersedes GOV-100, and the document discusses that statement.', 'prohibited control weakening language'), ('UK GDPR is the authority for this profile selection, and the document discusses that claim.', 'prohibited source authority language')):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_mapping_direction_and_authority_grammar_matrix(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR', 'Cyber Essentials']
    builder.write_component('profile.json', profile)
    for text in ('Cyber Essentials provision A maps to GOV-100.', 'Cyber Essentials provision A mapped to GOV-100.', 'Cyber Essentials provision A has a mapping to GOV-100.', 'Cyber Essentials provision A is mapped to GOV-100.', 'GOV-100 is mapped from Cyber Essentials provision A.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()
    for text in ('This profile is governed by UK GDPR.', 'This profile was governed by UK GDPR.', 'UK GDPR governs this profile.', 'UK GDPR governed this profile.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()
    for text in ('Cyber Essentials provision A is not mapped to GOV-100.', 'The claim that Cyber Essentials provision A is mapped to GOV-100 is false.', 'This profile is not governed by UK GDPR.', 'The claim that this profile is governed by UK GDPR is rejected.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_mapping_direction_form_and_aspect_cross_product(builder):
    external = 'Cyber Essentials provision A'
    control = 'GOV-100'
    directions = ((external, 'to', control), (control, 'from', external))
    affirmative_forms = ('{subject} maps {preposition} {object}', '{subject} mapped {preposition} {object}', '{subject} has mapped {preposition} {object}', '{subject} had mapped {preposition} {object}', '{subject} is mapped {preposition} {object}', '{subject} was mapped {preposition} {object}', '{subject} has been mapped {preposition} {object}', '{subject} had been mapped {preposition} {object}', '{subject} has a mapping {preposition} {object}', '{subject} had a mapping {preposition} {object}')
    for direction, form in product(directions, affirmative_forms):
        subject, preposition, object_ = direction
        assertion = form.format(subject=subject, preposition=preposition, object=object_)
        with nullcontext():
            builder.write_readme(f'{assertion}.')
            builder.record_case()
    denied_forms = ('{subject} does not map {preposition} {object}', '{subject} did not map {preposition} {object}', '{subject} has not mapped {preposition} {object}', '{subject} had not mapped {preposition} {object}', '{subject} is not mapped {preposition} {object}', '{subject} has not been mapped {preposition} {object}', '{subject} had not been mapped {preposition} {object}', '{subject} has no mapping {preposition} {object}', '{subject} had no mapping {preposition} {object}')
    for direction, form in product(directions, denied_forms):
        subject, preposition, object_ = direction
        assertion = form.format(subject=subject, preposition=preposition, object=object_)
        with nullcontext():
            builder.write_readme(f'{assertion}.')
            builder.record_case()


def _build_metalinguistic_context_is_bounded_to_the_assertion(builder):
    for text in ('The claim that this profile ensures legal compliance is prohibited.', 'This text discusses without asserting that this profile ensures legal compliance.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()
    for text, expected in (('The prohibited statement is discussed here, but this profile ensures legal compliance.', "prohibited assertion 'compliance'"), ('The prohibited statement is discussed here, but this profile supersedes GOV-100.', 'prohibited control weakening language')):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_natural_perfect_mandatory_denial_and_discussion_pairs(builder):
    for subject, auxiliary in (('GOV-100', 'has'), ('Core controls', 'have'), ('GOV-100', 'had')):
        for negator in ('not', 'never'):
            with nullcontext():
                builder.write_readme(f'{subject} {auxiliary} {negator} ceased to be mandatory.')
                builder.record_case()
    claims = ('GOV-100 has no longer been mandatory', 'Core controls have no longer been mandatory', 'GOV-100 had no longer been mandatory')
    for claim, frame in product(claims, ('is false', 'is rejected', 'was denied')):
        with nullcontext():
            builder.write_readme(f'The claim that {claim} {frame}.')
            builder.record_case()
    for claim in claims:
        with nullcontext():
            builder.write_readme(f'The phrase "{claim}" is prohibited.')
            builder.record_case()


def _build_natural_perfect_mandatory_placement_cross_product(builder):
    subjects = (('GOV-100', 'has'), ('Core controls', 'have'))
    for (subject, present_perfect), auxiliary in product(subjects, ('present', 'past')):
        verb = present_perfect if auxiliary == 'present' else 'had'
        with nullcontext():
            builder.write_readme(f'{subject} {verb} no longer been mandatory.')
            builder.record_case()


def _build_negated_rejection_head_cross_product(builder):
    claims = (('this profile guarantees legal compliance', "prohibited assertion 'compliance'"), ('GOV-100 is optional', 'prohibited control weakening language'))
    frames = ('is never false', 'was by no means rejected', 'has never been denied', 'cannot be rejected', "can't be denied", 'is neither false nor rejected')
    for (claim, expected), frame in product(claims, frames):
        with nullcontext():
            builder.write_readme(f'The claim that {claim} {frame}.')
            builder.record_case()


def _build_negation_binding_complement_and_insertion_cross_product(builder):
    embedded = ('It is not surprising to see this profile guarantee legal compliance.', 'It is not unusual to observe this profile guarantee legal compliance.', 'It is not unexpected that this profile guarantees legal compliance.', 'A reviewer who did not object saw this profile guarantee legal compliance.')
    for text in embedded:
        with nullcontext():
            builder.write_readme(text)
            builder.record_case()
    insertions = ('as reviewers who assessed it confirmed', 'according to reviewers', 'despite what reviewers expected')
    for insertion in insertions:
        with nullcontext():
            builder.write_readme(f'This profile does not, {insertion}, guarantee legal compliance.')
            builder.record_case()


def _build_negative_modifiers_remain_polarity_cross_product(builder):
    templates = ('NCSC has {modifier} approved this profile.', 'Cyber Essentials provision A has {modifier} mapped to GOV-100.', 'GOV-100 has {modifier} mapped from Cyber Essentials provision A.')
    for template, modifier in product(templates, ('not', 'never', 'by no means')):
        with nullcontext():
            builder.write_readme(template.format(modifier=modifier))
            builder.record_case()


def _build_new_control_weakening_quotations_are_allowed(builder):
    for phrase in AFFIRMATIVE_WEAKENING:
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\nThe prohibited statement "{phrase}" is quoted for review.\n')
            builder.record_case()


def _build_new_profile_claim_denials_are_allowed(builder):
    for text in ('This profile does not satisfy Cyber Essentials requirements.', 'This profile does not ensure legal compliance.', 'This profile does not confer certification eligibility.', 'This profile does not have NCSC approval.', 'Legal compliance is not ensured by this profile.', 'Certification eligibility is not conferred by this profile.', 'NCSC approval is not held by this profile.', 'Cyber Essentials provision A does not map to GOV-100 or supply its external outcome.', 'GOV-100 is not mapped from Cyber Essentials provision A and the external outcome is not imported.', 'GOV-100 does not support or satisfy Cyber Essentials provision A.', 'Cyber Essentials provision A is not supported or satisfied by GOV-100.', 'Cyber Essentials provision A does not support or satisfy GOV-100.', 'GOV-100 is not supported or satisfied by Cyber Essentials provision A.', 'This profile does not meet Cyber Essentials requirements.', 'This profile does not comply with Cyber Essentials.', 'This profile does not qualify the organization for certification.', 'This profile is not approved by NCSC.', 'NCSC does not approve this profile.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_new_profile_claim_quotations_and_discussion_are_allowed(builder):
    for text, _ in AFFIRMATIVE_CLAIMS:
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\nThe prohibited assertion "{text}" is quoted for review.\n')
            builder.record_case()
            builder.write_profile_readme_content(f"# Synthetic profile\n\nThe prohibited assertion that {text.rstrip('.')} is discussed here.\n")
            builder.record_case()


def _build_omit_skip_and_reduce_control_forms_are_rejected(builder):
    affirmative = ('This profile omits GOV-100.', 'GOV-100 is omitted by this profile.', 'GOV-100 may be omitted.', 'This profile skips GOV-100.', 'GOV-100 is skipped by this profile.', 'GOV-100 may be skipped.', 'This profile reduces GOV-100.', 'GOV-100 is reduced by this profile.', 'GOV-100 may be reduced.', 'GOV-100 has become optional under this profile.', 'GOV-100 remains optional under this profile.')
    for assertion in affirmative:
        with nullcontext():
            builder.write_readme(assertion)
            builder.record_case()


def _build_omit_skip_and_reduce_polarity_pairs(builder):
    for verb, present, participle in (('omit', 'omits', 'omitted'), ('skip', 'skips', 'skipped'), ('reduce', 'reduces', 'reduced')):
        denial = f'This profile does not {verb} GOV-100.'
        claim = f'This profile {present} GOV-100'
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme('GOV-100 does not remain optional.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{claim}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that GOV-100 may be {participle} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, GOV-100 may be {participle}.')
            builder.record_case()


def _build_passive_affirmative_control_weakening_is_rejected(builder):
    for text in ('Core controls are replaced by this profile.', 'Core control requirements are waived by this profile.', 'Core controls are made optional by this profile.', 'Core controls are altered by this profile.', 'Core controls are relaxed by this profile.', 'Core controls are weakened by this profile.', 'Core controls are narrowed by this profile.', 'Core controls are marked inapplicable by this profile.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_passive_control_weakening_denials_are_allowed(builder):
    for text in ('Core controls are not replaced by this profile.', 'Core control requirements are not waived by this profile.', 'Core controls are not made optional by this profile.', 'Core controls are not altered by this profile.', 'Core controls are not relaxed by this profile.', 'Core controls are not weakened by this profile.', 'Core controls are not narrowed by this profile.', 'Core controls are not marked inapplicable by this profile.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_passive_control_weakening_quotations_are_allowed(builder):
    for phrase in ('Core controls are replaced by this profile', 'Core control requirements are waived by this profile', 'Core controls are made optional by this profile', 'Core controls are altered by this profile', 'Core controls are relaxed by this profile', 'Core controls are weakened by this profile', 'Core controls are narrowed by this profile', 'Core controls are marked inapplicable by this profile'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\nThe phrase "{phrase}" is prohibited.\n')
            builder.record_case()


def _build_polarity_is_bound_to_the_assertion_head(builder):
    builder.write_profile_readme_content('# Synthetic profile\n\nIt is not surprising that this profile ensures legal compliance.\n')
    builder.record_case()
    builder.write_profile_readme_content('# Synthetic profile\n\nGOV-100 is superseded by no profile.\n')
    builder.record_case()


def _build_postposed_denial_agent_vs_rhetorical_cross_product(builder):
    rhetorical = ("This profile guarantees legal compliance to no one's surprise.", 'This profile proves legal compliance by no small margin.', 'GOV-100 is superseded by no small margin.', 'Core controls are discontinued by no surprising mechanism.')
    for text in rhetorical:
        with nullcontext():
            builder.write_readme(text)
            expected = 'prohibited control weakening language' if 'GOV-100' in text or 'Core controls' in text else "prohibited assertion 'compliance'"
            builder.record_case()
    genuine_denials = ('Legal compliance is guaranteed by no profile.', 'Legal compliance was proven by no authority.', 'GOV-100 is superseded by no profile.', 'Core controls are discontinued by no authority.', 'GOV-100 is superseded by neither this profile nor any overlay.')
    for text in genuine_denials:
        with nullcontext():
            builder.write_readme(text)
            builder.record_case()


def _build_postposed_denial_and_rejection_polarity_cross_product(builder):
    for boundary in ('while', 'whereas', 'although'):
        with nullcontext():
            builder.write_readme(f'This profile guarantees legal compliance {boundary} certification is granted by no authority.')
            builder.record_case()
    claims = ('this profile guarantees legal compliance', 'GOV-100 is optional')
    affirmative_frames = ('is false', 'is rejected', 'was denied')
    negated_frames = ('is not false', 'is not rejected', 'was not denied', 'has not been rejected')
    for claim, frame in product(claims, affirmative_frames):
        with nullcontext():
            builder.write_readme(f'The claim that {claim} {frame}.')
            builder.record_case()
    for claim, frame in product(claims, negated_frames):
        with nullcontext():
            builder.write_readme(f'The claim that {claim} {frame}.')
            expected = "prohibited assertion 'compliance'" if 'guarantees' in claim else 'prohibited control weakening language'
            builder.record_case()


def _build_postposed_denial_complement_boundary_cross_product(builder):
    constructions = ('Legal compliance is guaranteed {complement}{boundary}.', 'GOV-100 is superseded {complement}{boundary}.')
    complements = ('by no profile', 'by no authority under this profile', 'by neither this profile nor any overlay')
    boundaries = ('', ', and this document explains the scope', ' while this document explains the scope', ' whereas this document explains the scope', ', but this document explains the scope')
    for construction, complement, boundary in product(constructions, complements, boundaries):
        with nullcontext():
            builder.write_readme(construction.format(complement=complement, boundary=boundary))
            builder.record_case()


def _build_postposed_possessive_rhetorical_suffix_cross_product(builder):
    closed_nouns = ('profile', 'authority', 'source', 'body', 'organization', 'agency', 'overlay')
    for noun, apostrophe in product(closed_nouns, ("'s", '’s')):
        with nullcontext():
            builder.write_readme(f'This profile proves legal compliance by no {noun}{apostrophe} surprise.')
            builder.record_case()
    for text in ('This profile proves legal compliance by no organization’s surprise.', "This profile proves legal compliance by no authority's measure."):
        with nullcontext():
            builder.write_readme(text)
            builder.record_case()


def _build_postposed_terminal_and_qualified_denial_cross_product(builder):
    closed_nouns = ('profile', 'authority', 'source', 'body', 'organization', 'agency', 'overlay')
    for noun in closed_nouns:
        with nullcontext():
            builder.write_readme(f'Legal compliance was proven by no {noun}.')
            builder.record_case()
    for qualifier in ('under this profile', 'within the scheme', 'in this document'):
        with nullcontext():
            builder.write_readme(f'Legal compliance was proven by no authority {qualifier}.')
            builder.record_case()
    for text in ('GOV-100 is superseded by neither this profile nor any overlay.', 'GOV-100 is superseded by neither this profile nor any overlay under this profile.'):
        with nullcontext():
            builder.write_readme(text)
            builder.record_case()


def _build_profile_specific_claim_denials_are_allowed(builder):
    for text in ('This profile is not legally sufficient.', 'This profile does not have external approval.', 'This profile is not production ready.', 'This profile does not certify compliance.', 'This profile is not certified.', 'This profile is not equivalent.', 'This profile is not endorsed.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_profile_specific_claim_quotations_are_allowed(builder):
    for phrase in ('legally sufficient', 'has external approval', 'production ready', 'certifies compliance', 'is compliant', 'is certified', 'is equivalent', 'is endorsed'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\nThe phrase "{phrase}" is prohibited.\n')
            builder.record_case()


def _build_profile_specific_positive_claims_are_rejected(builder):
    for text, expected in (('This profile is legally sufficient.', 'legal sufficiency'), ('This profile has external approval.', 'external approval'), ('This profile is production ready.', 'production readiness'), ('This profile certifies compliance.', 'compliance')):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_readiness_confirmation_requires_positive_establishment(builder):
    for statement in ('This profile confirms production readiness gaps remain unresolved.', 'This profile confirms production readiness is not established.'):
        with nullcontext():
            builder.write_readme(statement)
            builder.record_case()


def _build_reordered_mapping_and_general_authority_are_rejected(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR', 'NCSC', 'Cyber Essentials']
    builder.write_component('profile.json', profile)
    for text, expected in (('Requirement A of Cyber Essentials maps to GOV-100.', "prohibited assertion 'imported mapping relationship'"), ('Cyber Essentials provision A has a mapping to GOV-100.', "prohibited assertion 'imported mapping relationship'"), ('NCSC provision A maps to GOV-100.', "prohibited assertion 'imported mapping relationship'"), ('UK GDPR governs this profile.', 'prohibited source authority language')):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_reordered_mapping_and_general_authority_denials_are_allowed(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR', 'NCSC', 'Cyber Essentials']
    builder.write_component('profile.json', profile)
    for text in ('Requirement A of Cyber Essentials does not map to GOV-100.', 'Cyber Essentials provision A has no mapping to GOV-100.', 'NCSC provision A does not map to GOV-100.', 'UK GDPR does not govern this profile.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_second_review_claim_word_order_polarity_pairs(builder):
    cases = (('This profile guarantees Cyber Essentials compliance', 'This profile does not guarantee Cyber Essentials compliance.', 'compliance'), ('Compliance with Cyber Essentials is guaranteed by this profile', 'Compliance with Cyber Essentials is not guaranteed by this profile.', 'compliance'), ('Production readiness is confirmed by this profile', 'Production readiness is not confirmed by this profile.', 'production readiness'), ('Evidence for GOV-100 is provided by Cyber Essentials provision A.1', 'Evidence for GOV-100 is not provided by Cyber Essentials provision A.1.', 'imported mapping relationship'))
    for assertion, denial, expected in cases:
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{assertion}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that {assertion} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, {assertion}.')
            builder.record_case()


def _build_second_review_claim_word_orders_are_rejected(builder):
    cases = (('This profile guarantees Cyber Essentials compliance', 'compliance'), ('Compliance with Cyber Essentials is guaranteed by this profile', 'compliance'), ('Production readiness is confirmed by this profile', 'production readiness'), ('Evidence for GOV-100 is provided by Cyber Essentials provision A.1', 'imported mapping relationship'))
    for assertion, expected in cases:
        with nullcontext():
            builder.write_readme(f'{assertion}.')
            builder.record_case()


def _build_second_review_direct_weakening_forms_are_rejected(builder):
    for assertion in ('This profile omits the GOV-100 control.', 'This profile has omitted GOV-100.'):
        with nullcontext():
            builder.write_readme(assertion)
            builder.record_case()


def _build_second_review_direct_weakening_polarity_pairs(builder):
    pairs = (('This profile omits the GOV-100 control', 'This profile does not omit the GOV-100 control.'), ('This profile has omitted GOV-100', 'This profile has not omitted GOV-100.'))
    for assertion, denial in pairs:
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{assertion}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that {assertion} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, {assertion}.')
            builder.record_case()


def _build_source_authority_after_denied_clause_is_rejected(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    builder.write_profile_readme_content('# Synthetic profile\n\nUK GDPR is not the authority for this profile title, but it is the authority for this profile selection.\n')
    builder.record_case()
    builder.write_profile_readme_content('# Synthetic profile\n\nThe prohibited statement is discussed here, but UK GDPR is the authority for this profile selection.\n')
    builder.record_case()


def _build_source_authority_denials_and_discussion_are_allowed(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    for text in ('UK GDPR is not the authority for this profile selection.', 'This profile selection is not governed by UK GDPR.', 'The prohibited assertion "UK GDPR is the authority for this profile selection" is quoted for review.', 'The assertion that UK GDPR is the authority for this profile selection is prohibited and discussed here.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_source_boundary_rejects_excluded_authority_claims(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    for text in ('UK GDPR is the authority for this profile selection.', 'This profile selection is governed by UK GDPR.'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
            builder.record_case()


def _build_third_review_bounded_nonweakening_semantic_variations(builder):
    statements = ('This profile reduces GOV-100 implementation risks while preserving all requirements.', 'This profile reduced the GOV-100 control implementation risk while preserving every requirement.', 'This profile omits GOV-100 from an illustrative list while retaining it in the complete selection ledger.', 'This profile omitted the GOV-100 control from this illustrative list while retaining it in the complete selection ledger.')
    for statement in statements:
        with nullcontext():
            builder.write_readme(statement)
            builder.record_case()


def _build_third_review_excluded_source_supply_aspect_and_voice(builder):
    profile = builder.load_component('profile.json')
    profile['source_boundary']['excluded_sources'] = ['UK GDPR']
    builder.write_component('profile.json', profile)
    cases = (('UK GDPR has supplied the GOV-100 profile selection', 'UK GDPR has not supplied the GOV-100 profile selection.'), ('UK GDPR had supplied the GOV-100 profile selection', 'UK GDPR had not supplied the GOV-100 profile selection.'), ('The GOV-100 profile selection has been supplied by UK GDPR', 'The GOV-100 profile selection has not been supplied by UK GDPR.'), ('The GOV-100 profile selection had been supplied by UK GDPR', 'The GOV-100 profile selection had not been supplied by UK GDPR.'))
    for assertion, denial in cases:
        with nullcontext():
            builder.write_readme(f'{assertion}.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{assertion}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that {assertion} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, {assertion}.')
            builder.record_case()


def _build_third_review_passive_aspect_claim_families(builder):
    cases = (('Compliance with Cyber Essentials has been guaranteed by this profile', 'Compliance with Cyber Essentials has not been guaranteed by this profile.', 'compliance'), ('Compliance with Cyber Essentials had been guaranteed by this profile', 'Compliance with Cyber Essentials had not been guaranteed by this profile.', 'compliance'), ('Production readiness has been confirmed by this profile', 'Production readiness has not been confirmed by this profile.', 'production readiness'), ('Production readiness had been confirmed by this profile', 'Production readiness had not been confirmed by this profile.', 'production readiness'), ('Evidence for GOV-100 has been provided by Cyber Essentials provision A.1', 'Evidence for GOV-100 has not been provided by Cyber Essentials provision A.1.', 'imported mapping relationship'), ('Evidence for GOV-100 had been provided by Cyber Essentials provision A.1', 'Evidence for GOV-100 had not been provided by Cyber Essentials provision A.1.', 'imported mapping relationship'))
    for assertion, denial, expected in cases:
        with nullcontext():
            builder.write_readme(f'{assertion}.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{assertion}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that {assertion} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, {assertion}.')
            builder.record_case()


def _build_third_review_progressive_direct_weakening_forms(builder):
    cases = (('This profile is omitting the GOV-100 control', 'This profile is not omitting the GOV-100 control.'), ('This profile was skipping GOV-100', 'This profile was not skipping GOV-100.'), ('This profile has been omitting GOV-100', 'This profile has not been omitting GOV-100.'), ('This profile had been skipping the GOV-100 control', 'This profile had not been skipping the GOV-100 control.'))
    for assertion, denial in cases:
        with nullcontext():
            builder.write_readme(f'{assertion}.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(denial)
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The phrase "{assertion}" is prohibited.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'The claim that {assertion} is rejected.')
            builder.record_case()
        with nullcontext():
            builder.write_readme(f'{denial} However, {assertion}.')
            builder.record_case()


def _build_third_review_readiness_explicit_denial_family(builder):
    safe_statements = ('This profile confirms production readiness gaps remain unresolved.', 'This profile confirmed production readiness is not established.', 'This profile confirms production readiness has not been established.', 'This profile confirmed production readiness had not been established.', 'This profile confirms production readiness remains unestablished.', 'This profile confirmed production readiness is unestablished.', 'This profile confirms production readiness remained unestablished.')
    for statement in safe_statements:
        with nullcontext():
            builder.write_readme(statement)
            builder.record_case()
    for assertion in ('This profile confirms production readiness is established.', 'This profile confirms production readiness has been established.', 'This profile confirms production readiness remains established.'):
        with nullcontext():
            builder.write_readme(assertion)
            builder.record_case()
    builder.write_readme('This profile confirms production readiness remains unestablished. However, this profile confirms production readiness is established.')
    builder.record_case()


def _build_unrelated_denial_does_not_mask_later_control_weakening(builder):
    for conjunction in ('and', ', and'):
        with nullcontext():
            builder.write_profile_readme_content(f'# Synthetic profile\n\nThis profile does not replace its title {conjunction} replaces core controls.\n')
            builder.record_case()


def _build_weakening_aspect_and_state_cross_product(builder):
    subjects = (('GOV-100', 'has', 'is', 'was'), ('Core controls', 'have', 'are', 'were'))
    active_aspects = ('{perfect} ceased to apply', 'had ceased to apply', '{perfect} discontinued applying', 'had discontinued applying')
    passive_aspects = ('{present} discontinued', '{past} discontinued', '{perfect} been discontinued', 'had been discontinued')
    mandatory_aspects = ('{present} no longer mandatory', '{past} no longer mandatory', '{perfect} been no longer mandatory', 'had been no longer mandatory')
    for subject, perfect, present, past in subjects:
        values = {'perfect': perfect, 'present': present, 'past': past}
        for family, forms in (('active', active_aspects), ('passive', passive_aspects), ('mandatory', mandatory_aspects)):
            for form in forms:
                predicate = form.format(**values)
                with nullcontext():
                    builder.write_readme(f'{subject} {predicate}.')
                    builder.record_case()


def _build_weakening_aspect_denial_and_metalinguistic_pairs(builder):
    denied = ('GOV-100 has not ceased to apply.', 'Core controls have never discontinued applying.', 'GOV-100 has not been discontinued.', 'Core controls had never been discontinued.')
    claims = ('GOV-100 has ceased to apply', 'Core controls had been discontinued', 'GOV-100 has been no longer mandatory')
    for text in denied:
        with nullcontext():
            builder.write_readme(text)
            builder.record_case()
    for claim, frame in product(claims, ('is false', 'is rejected', 'was denied')):
        with nullcontext():
            builder.write_readme(f'The claim that {claim} {frame}.')
            builder.record_case()


def _build_weakening_cross_product_denials_and_claim_frames(builder):
    denied = ('GOV-100 is not optional.', 'Core controls are not inapplicable.', 'GOV-100 is mandatory.', 'GOV-100 does not cease to apply.', 'Core controls do not discontinue applying.', 'GOV-100 is not discontinued.', 'Core controls are still applied.', 'GOV-100 may not be optional.')
    frames = ('is false', 'is rejected', 'was denied')
    claims = ('GOV-100 is not mandatory', 'Core controls may be optional', 'GOV-100 shall cease to apply')
    for text in denied:
        with nullcontext():
            builder.write_readme(text)
            builder.record_case()
    for claim, frame in product(claims, frames):
        with nullcontext():
            builder.write_readme(f'The claim that {claim} {frame}.')
            builder.record_case()


def _build_weakening_state_grammar_matrix(builder):
    singular_predicates = ('must not apply', 'shall not apply', 'need not apply', 'no longer applies', 'is no longer required', 'shall be optional', 'must be optional', 'is optional', 'shall be inapplicable', 'must be inapplicable', 'is inapplicable', 'is not required')
    plural_predicates = ('must not apply', 'shall not apply', 'need not apply', 'no longer apply', 'are no longer required', 'shall be optional', 'must be optional', 'are optional', 'shall be inapplicable', 'must be inapplicable', 'are inapplicable', 'are not required')
    for subject, predicates in (('GOV-100', singular_predicates), ('Core controls', plural_predicates)):
        for predicate in predicates:
            text = f'{subject} {predicate} under this profile.'
            with nullcontext():
                builder.write_profile_readme_content(f'# Synthetic profile\n\n{text}\n')
                builder.record_case()


def _build_weakening_subject_modal_and_state_cross_product(builder):
    subjects = (('GOV-100', 'is', 'applies', 'ceases', 'discontinues'), ('Core controls', 'are', 'apply', 'cease', 'discontinue'))
    states = ('optional', 'inapplicable', 'not mandatory')
    for (subject, copula, _, _, _), state in product(subjects, states):
        modal_states = (f'{modal} not be mandatory' if state == 'not mandatory' else f'{modal} be {state}' for modal in ('shall', 'must', 'may'))
        for predicate in (f'{copula} {state}', *modal_states):
            with nullcontext():
                builder.write_readme(f'{subject} {predicate}.')
                builder.record_case()
    for subject, copula, applies, ceases, discontinues in subjects:
        transitions = (f'no longer {applies}', f'{copula} no longer applied', f'{copula} discontinued', f'{ceases} to apply', f'{discontinues} applying', *(f'{modal} {verb}' for modal, verb in product(('shall', 'must', 'may'), ('cease to apply', 'discontinue applying'))))
        for predicate in transitions:
            with nullcontext():
                builder.write_readme(f'{subject} {predicate}.')
                builder.record_case()


_CASE_BUILDERS = (('test_additional_assurance_claim_forms_are_rejected',
  '_build_additional_assurance_claim_forms_are_rejected'),
 ('test_additional_assurance_denials_and_discussion_are_allowed',
  '_build_additional_assurance_denials_and_discussion_are_allowed'),
 ('test_additional_control_weakening_forms_are_rejected',
  '_build_additional_control_weakening_forms_are_rejected'),
 ('test_additional_weakening_denials_and_discussion_are_allowed',
  '_build_additional_weakening_denials_and_discussion_are_allowed'),
 ('test_affirmative_claim_after_denied_clause_is_rejected',
  '_build_affirmative_claim_after_denied_clause_is_rejected'),
 ('test_affirmative_weakening_after_denial_is_rejected',
  '_build_affirmative_weakening_after_denial_is_rejected'),
 ('test_approval_subject_voice_and_aspect_cross_product',
  '_build_approval_subject_voice_and_aspect_cross_product'),
 ('test_assurance_voice_tense_and_aspect_grammar_matrix',
  '_build_assurance_voice_tense_and_aspect_grammar_matrix'),
 ('test_bounded_adverb_slots_cross_product', '_build_bounded_adverb_slots_cross_product'),
 ('test_common_affirmative_control_weakening_is_rejected',
  '_build_common_affirmative_control_weakening_is_rejected'),
 ('test_common_affirmative_profile_claim_variants_are_rejected',
  '_build_common_affirmative_profile_claim_variants_are_rejected'),
 ('test_contrast_clause_boundaries_do_not_mask_prohibited_language',
  '_build_contrast_clause_boundaries_do_not_mask_prohibited_language'),
 ('test_declared_generic_authority_passive_aspect_cross_product',
  '_build_declared_generic_authority_passive_aspect_cross_product'),
 ('test_direct_weakening_object_and_complement_are_bounded',
  '_build_direct_weakening_object_and_complement_are_bounded'),
 ('test_dynamic_authority_bounded_adverb_cross_product',
  '_build_dynamic_authority_bounded_adverb_cross_product'),
 ('test_establishes_profile_claim_denials_are_allowed',
  '_build_establishes_profile_claim_denials_are_allowed'),
 ('test_establishes_profile_claim_quotations_are_allowed',
  '_build_establishes_profile_claim_quotations_are_allowed'),
 ('test_establishes_profile_claim_variants_are_rejected',
  '_build_establishes_profile_claim_variants_are_rejected'),
 ('test_excluded_source_supply_and_derivation_are_rejected',
  '_build_excluded_source_supply_and_derivation_are_rejected'),
 ('test_excluded_source_supply_and_derivation_polarity_pairs',
  '_build_excluded_source_supply_and_derivation_polarity_pairs'),
 ('test_explicit_control_weakening_denials_are_allowed',
  '_build_explicit_control_weakening_denials_are_allowed'),
 ('test_extended_polarity_and_metalinguistic_matrix',
  '_build_extended_polarity_and_metalinguistic_matrix'),
 ('test_final_review_claim_assertions_are_rejected',
  '_build_final_review_claim_assertions_are_rejected'),
 ('test_final_review_claim_polarity_and_clause_pairs',
  '_build_final_review_claim_polarity_and_clause_pairs'),
 ('test_identified_excluded_source_supply_forms_are_rejected',
  '_build_identified_excluded_source_supply_forms_are_rejected'),
 ('test_identified_excluded_source_supply_polarity_pairs',
  '_build_identified_excluded_source_supply_polarity_pairs'),
 ('test_later_metalinguistic_discussion_does_not_mask_assertions',
  '_build_later_metalinguistic_discussion_does_not_mask_assertions'),
 ('test_mapping_direction_and_authority_grammar_matrix',
  '_build_mapping_direction_and_authority_grammar_matrix'),
 ('test_mapping_direction_form_and_aspect_cross_product',
  '_build_mapping_direction_form_and_aspect_cross_product'),
 ('test_metalinguistic_context_is_bounded_to_the_assertion',
  '_build_metalinguistic_context_is_bounded_to_the_assertion'),
 ('test_natural_perfect_mandatory_denial_and_discussion_pairs',
  '_build_natural_perfect_mandatory_denial_and_discussion_pairs'),
 ('test_natural_perfect_mandatory_placement_cross_product',
  '_build_natural_perfect_mandatory_placement_cross_product'),
 ('test_negated_rejection_head_cross_product', '_build_negated_rejection_head_cross_product'),
 ('test_negation_binding_complement_and_insertion_cross_product',
  '_build_negation_binding_complement_and_insertion_cross_product'),
 ('test_negative_modifiers_remain_polarity_cross_product',
  '_build_negative_modifiers_remain_polarity_cross_product'),
 ('test_new_control_weakening_quotations_are_allowed',
  '_build_new_control_weakening_quotations_are_allowed'),
 ('test_new_profile_claim_denials_are_allowed', '_build_new_profile_claim_denials_are_allowed'),
 ('test_new_profile_claim_quotations_and_discussion_are_allowed',
  '_build_new_profile_claim_quotations_and_discussion_are_allowed'),
 ('test_omit_skip_and_reduce_control_forms_are_rejected',
  '_build_omit_skip_and_reduce_control_forms_are_rejected'),
 ('test_omit_skip_and_reduce_polarity_pairs', '_build_omit_skip_and_reduce_polarity_pairs'),
 ('test_passive_affirmative_control_weakening_is_rejected',
  '_build_passive_affirmative_control_weakening_is_rejected'),
 ('test_passive_control_weakening_denials_are_allowed',
  '_build_passive_control_weakening_denials_are_allowed'),
 ('test_passive_control_weakening_quotations_are_allowed',
  '_build_passive_control_weakening_quotations_are_allowed'),
 ('test_polarity_is_bound_to_the_assertion_head', '_build_polarity_is_bound_to_the_assertion_head'),
 ('test_postposed_denial_agent_vs_rhetorical_cross_product',
  '_build_postposed_denial_agent_vs_rhetorical_cross_product'),
 ('test_postposed_denial_and_rejection_polarity_cross_product',
  '_build_postposed_denial_and_rejection_polarity_cross_product'),
 ('test_postposed_denial_complement_boundary_cross_product',
  '_build_postposed_denial_complement_boundary_cross_product'),
 ('test_postposed_possessive_rhetorical_suffix_cross_product',
  '_build_postposed_possessive_rhetorical_suffix_cross_product'),
 ('test_postposed_terminal_and_qualified_denial_cross_product',
  '_build_postposed_terminal_and_qualified_denial_cross_product'),
 ('test_profile_specific_claim_denials_are_allowed',
  '_build_profile_specific_claim_denials_are_allowed'),
 ('test_profile_specific_claim_quotations_are_allowed',
  '_build_profile_specific_claim_quotations_are_allowed'),
 ('test_profile_specific_positive_claims_are_rejected',
  '_build_profile_specific_positive_claims_are_rejected'),
 ('test_readiness_confirmation_requires_positive_establishment',
  '_build_readiness_confirmation_requires_positive_establishment'),
 ('test_reordered_mapping_and_general_authority_are_rejected',
  '_build_reordered_mapping_and_general_authority_are_rejected'),
 ('test_reordered_mapping_and_general_authority_denials_are_allowed',
  '_build_reordered_mapping_and_general_authority_denials_are_allowed'),
 ('test_second_review_claim_word_order_polarity_pairs',
  '_build_second_review_claim_word_order_polarity_pairs'),
 ('test_second_review_claim_word_orders_are_rejected',
  '_build_second_review_claim_word_orders_are_rejected'),
 ('test_second_review_direct_weakening_forms_are_rejected',
  '_build_second_review_direct_weakening_forms_are_rejected'),
 ('test_second_review_direct_weakening_polarity_pairs',
  '_build_second_review_direct_weakening_polarity_pairs'),
 ('test_source_authority_after_denied_clause_is_rejected',
  '_build_source_authority_after_denied_clause_is_rejected'),
 ('test_source_authority_denials_and_discussion_are_allowed',
  '_build_source_authority_denials_and_discussion_are_allowed'),
 ('test_source_boundary_rejects_excluded_authority_claims',
  '_build_source_boundary_rejects_excluded_authority_claims'),
 ('test_third_review_bounded_nonweakening_semantic_variations',
  '_build_third_review_bounded_nonweakening_semantic_variations'),
 ('test_third_review_excluded_source_supply_aspect_and_voice',
  '_build_third_review_excluded_source_supply_aspect_and_voice'),
 ('test_third_review_passive_aspect_claim_families',
  '_build_third_review_passive_aspect_claim_families'),
 ('test_third_review_progressive_direct_weakening_forms',
  '_build_third_review_progressive_direct_weakening_forms'),
 ('test_third_review_readiness_explicit_denial_family',
  '_build_third_review_readiness_explicit_denial_family'),
 ('test_unrelated_denial_does_not_mask_later_control_weakening',
  '_build_unrelated_denial_does_not_mask_later_control_weakening'),
 ('test_weakening_aspect_and_state_cross_product',
  '_build_weakening_aspect_and_state_cross_product'),
 ('test_weakening_aspect_denial_and_metalinguistic_pairs',
  '_build_weakening_aspect_denial_and_metalinguistic_pairs'),
 ('test_weakening_cross_product_denials_and_claim_frames',
  '_build_weakening_cross_product_denials_and_claim_frames'),
 ('test_weakening_state_grammar_matrix', '_build_weakening_state_grammar_matrix'),
 ('test_weakening_subject_modal_and_state_cross_product',
  '_build_weakening_subject_modal_and_state_cross_product'))
_EXPECTED_DIAGNOSTICS = {'test_additional_assurance_claim_forms_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'compliance'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'certification "
                                                         "eligibility'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'certification'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'named-authority approval'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'named-authority "
                                                         "approval'",)),
 'test_additional_assurance_denials_and_discussion_are_allowed': ((),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  ()),
 'test_additional_control_weakening_forms_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',)),
 'test_additional_weakening_denials_and_discussion_are_allowed': ((), (), (), (), ()),
 'test_affirmative_claim_after_denied_clause_is_rejected': (('profiles/uk/0.1.0/README.md: '
                                                             'prohibited assertion '
                                                             "'certification "
                                                             "eligibility'",),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited assertion '
                                                             "'external outcome "
                                                             "import'",)),
 'test_affirmative_weakening_after_denial_is_rejected': (('profiles/uk/0.1.0/README.md: '
                                                          'prohibited control '
                                                          'weakening language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited control '
                                                          'weakening language',)),
 'test_approval_subject_voice_and_aspect_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          ()),
 'test_assurance_voice_tense_and_aspect_grammar_matrix': (('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'compliance'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'certification'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'certification'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'certification'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'certification'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'certification "
                                                           "eligibility'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'certification "
                                                           "eligibility'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'named-authority "
                                                           "approval'",)),
 'test_bounded_adverb_slots_cross_product': (('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'named-authority approval'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",),
                                             ('profiles/uk/0.1.0/README.md: prohibited '
                                              "assertion 'imported mapping "
                                              "relationship'",)),
 'test_common_affirmative_control_weakening_is_rejected': (('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited control '
                                                            'weakening language',)),
 'test_common_affirmative_profile_claim_variants_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'legal "
                                                                  "sufficiency'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'external "
                                                                  "approval'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'production "
                                                                  "readiness'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'production "
                                                                  "readiness'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'compliance'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'certification'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'equivalence'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'endorsement'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'scheme "
                                                                  "satisfaction'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'compliance'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'certification "
                                                                  "eligibility'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'named-authority "
                                                                  "approval'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'external "
                                                                  "outcome import'",
                                                                  'profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'"),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'compliance'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'certification "
                                                                  "eligibility'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'named-authority "
                                                                  "approval'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'external "
                                                                  "outcome import'",
                                                                  'profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'"),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'imported "
                                                                  'mapping '
                                                                  "relationship'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  "assertion 'scheme "
                                                                  "satisfaction'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'compliance'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'certification "
                                                                  "eligibility'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'named-authority "
                                                                  "approval'",),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited '
                                                                  'assertion '
                                                                  "'named-authority "
                                                                  "approval'",)),
 'test_contrast_clause_boundaries_do_not_mask_prohibited_language': (('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'assertion '
                                                                      "'compliance'",),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'control '
                                                                      'weakening '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'source '
                                                                      'authority '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'assertion '
                                                                      "'compliance'",),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'control '
                                                                      'weakening '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'source '
                                                                      'authority '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'assertion '
                                                                      "'compliance'",),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'control '
                                                                      'weakening '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'source '
                                                                      'authority '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'assertion '
                                                                      "'compliance'",),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'control '
                                                                      'weakening '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'source '
                                                                      'authority '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'assertion '
                                                                      "'compliance'",),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'control '
                                                                      'weakening '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'source '
                                                                      'authority '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'assertion '
                                                                      "'compliance'",),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'control '
                                                                      'weakening '
                                                                      'language',),
                                                                     ('profiles/uk/0.1.0/README.md: '
                                                                      'prohibited '
                                                                      'source '
                                                                      'authority '
                                                                      'language',)),
 'test_declared_generic_authority_passive_aspect_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                                   'prohibited source '
                                                                   'authority '
                                                                   'language',),
                                                                  ('profiles/uk/0.1.0/README.md: '
                                                                   'prohibited source '
                                                                   'authority '
                                                                   'language',),
                                                                  ('profiles/uk/0.1.0/README.md: '
                                                                   'prohibited source '
                                                                   'authority '
                                                                   'language',),
                                                                  ('profiles/uk/0.1.0/README.md: '
                                                                   'prohibited source '
                                                                   'authority '
                                                                   'language',),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  ()),
 'test_direct_weakening_object_and_complement_are_bounded': ((), ()),
 'test_dynamic_authority_bounded_adverb_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         (),
                                                         (),
                                                         ()),
 'test_establishes_profile_claim_denials_are_allowed': ((), (), ()),
 'test_establishes_profile_claim_quotations_are_allowed': ((), (), ()),
 'test_establishes_profile_claim_variants_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'legal sufficiency'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'external approval'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'production readiness'",)),
 'test_excluded_source_supply_and_derivation_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                              'prohibited source '
                                                              'authority language',),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited source '
                                                              'authority language',),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited source '
                                                              'authority language',),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited source '
                                                              'authority language',),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited source '
                                                              'authority language',),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited source '
                                                              'authority language',),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited source '
                                                              'authority language',),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited source '
                                                              'authority language',)),
 'test_excluded_source_supply_and_derivation_polarity_pairs': ((),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               (),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               (),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               (),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               (),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',)),
 'test_explicit_control_weakening_denials_are_allowed': ((),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         (),
                                                         ()),
 'test_extended_polarity_and_metalinguistic_matrix': ((),
                                                      (),
                                                      (),
                                                      (),
                                                      (),
                                                      (),
                                                      (),
                                                      (),
                                                      (),
                                                      (),
                                                      ()),
 'test_final_review_claim_assertions_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'compliance'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'endorsement'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'production readiness'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'certification eligibility'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'named-authority approval'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      "prohibited assertion 'imported "
                                                      "mapping relationship'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      "prohibited assertion 'imported "
                                                      "mapping relationship'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      "prohibited assertion 'imported "
                                                      "mapping relationship'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      "prohibited assertion 'imported "
                                                      "mapping relationship'",)),
 'test_final_review_claim_polarity_and_clause_pairs': ((),
                                                       (),
                                                       (),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'compliance'",),
                                                       (),
                                                       (),
                                                       (),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'endorsement'",),
                                                       (),
                                                       (),
                                                       (),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'production readiness'",),
                                                       (),
                                                       (),
                                                       (),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'certification eligibility'",),
                                                       (),
                                                       (),
                                                       (),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'named-authority approval'",),
                                                       (),
                                                       (),
                                                       (),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'imported mapping "
                                                        "relationship'",),
                                                       (),
                                                       (),
                                                       (),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'imported mapping "
                                                        "relationship'",)),
 'test_identified_excluded_source_supply_forms_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',)),
 'test_identified_excluded_source_supply_polarity_pairs': ((),
                                                           (),
                                                           (),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited source '
                                                            'authority language',),
                                                           (),
                                                           (),
                                                           (),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited source '
                                                            'authority language',)),
 'test_later_metalinguistic_discussion_does_not_mask_assertions': (('profiles/uk/0.1.0/README.md: '
                                                                    'prohibited '
                                                                    'assertion '
                                                                    "'compliance'",),
                                                                   ('profiles/uk/0.1.0/README.md: '
                                                                    'prohibited '
                                                                    'control weakening '
                                                                    'language',),
                                                                   ('profiles/uk/0.1.0/README.md: '
                                                                    'prohibited source '
                                                                    'authority '
                                                                    'language',)),
 'test_mapping_direction_and_authority_grammar_matrix': (('profiles/uk/0.1.0/README.md: '
                                                          'prohibited assertion '
                                                          "'imported mapping "
                                                          "relationship'",),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited assertion '
                                                          "'imported mapping "
                                                          "relationship'",),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited assertion '
                                                          "'imported mapping "
                                                          "relationship'",),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited assertion '
                                                          "'imported mapping "
                                                          "relationship'",),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited assertion '
                                                          "'imported mapping "
                                                          "relationship'",),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         ('profiles/uk/0.1.0/README.md: '
                                                          'prohibited source authority '
                                                          'language',),
                                                         (),
                                                         (),
                                                         (),
                                                         ()),
 'test_mapping_direction_form_and_aspect_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited assertion '
                                                           "'imported mapping "
                                                           "relationship'",),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          (),
                                                          ()),
 'test_metalinguistic_context_is_bounded_to_the_assertion': ((),
                                                             (),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited assertion '
                                                              "'compliance'",),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited control '
                                                              'weakening language',)),
 'test_natural_perfect_mandatory_denial_and_discussion_pairs': ((),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                ()),
 'test_natural_perfect_mandatory_placement_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',)),
 'test_negated_rejection_head_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                "prohibited assertion 'compliance'",),
                                               ('profiles/uk/0.1.0/README.md: '
                                                "prohibited assertion 'compliance'",),
                                               ('profiles/uk/0.1.0/README.md: '
                                                "prohibited assertion 'compliance'",),
                                               ('profiles/uk/0.1.0/README.md: '
                                                "prohibited assertion 'compliance'",),
                                               ('profiles/uk/0.1.0/README.md: '
                                                "prohibited assertion 'compliance'",),
                                               ('profiles/uk/0.1.0/README.md: '
                                                "prohibited assertion 'compliance'",),
                                               ('profiles/uk/0.1.0/README.md: '
                                                'prohibited control weakening '
                                                'language',),
                                               ('profiles/uk/0.1.0/README.md: '
                                                'prohibited control weakening '
                                                'language',),
                                               ('profiles/uk/0.1.0/README.md: '
                                                'prohibited control weakening '
                                                'language',),
                                               ('profiles/uk/0.1.0/README.md: '
                                                'prohibited control weakening '
                                                'language',),
                                               ('profiles/uk/0.1.0/README.md: '
                                                'prohibited control weakening '
                                                'language',),
                                               ('profiles/uk/0.1.0/README.md: '
                                                'prohibited control weakening '
                                                'language',)),
 'test_negation_binding_complement_and_insertion_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                                   'prohibited '
                                                                   'assertion '
                                                                   "'compliance'",),
                                                                  ('profiles/uk/0.1.0/README.md: '
                                                                   'prohibited '
                                                                   'assertion '
                                                                   "'compliance'",),
                                                                  ('profiles/uk/0.1.0/README.md: '
                                                                   'prohibited '
                                                                   'assertion '
                                                                   "'compliance'",),
                                                                  ('profiles/uk/0.1.0/README.md: '
                                                                   'prohibited '
                                                                   'assertion '
                                                                   "'compliance'",),
                                                                  (),
                                                                  (),
                                                                  ()),
 'test_negative_modifiers_remain_polarity_cross_product': ((),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           ()),
 'test_new_control_weakening_quotations_are_allowed': ((),
                                                       (),
                                                       (),
                                                       (),
                                                       (),
                                                       (),
                                                       (),
                                                       (),
                                                       (),
                                                       (),
                                                       (),
                                                       ()),
 'test_new_profile_claim_denials_are_allowed': ((),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                (),
                                                ()),
 'test_new_profile_claim_quotations_and_discussion_are_allowed': ((),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  (),
                                                                  ()),
 'test_omit_skip_and_reduce_control_forms_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',)),
 'test_omit_skip_and_reduce_polarity_pairs': ((),
                                              (),
                                              (),
                                              (),
                                              ('profiles/uk/0.1.0/README.md: '
                                               'prohibited control weakening '
                                               'language',),
                                              (),
                                              (),
                                              (),
                                              (),
                                              ('profiles/uk/0.1.0/README.md: '
                                               'prohibited control weakening '
                                               'language',),
                                              (),
                                              (),
                                              (),
                                              (),
                                              ('profiles/uk/0.1.0/README.md: '
                                               'prohibited control weakening '
                                               'language',)),
 'test_passive_affirmative_control_weakening_is_rejected': (('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',)),
 'test_passive_control_weakening_denials_are_allowed': ((), (), (), (), (), (), (), ()),
 'test_passive_control_weakening_quotations_are_allowed': ((),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           ()),
 'test_polarity_is_bound_to_the_assertion_head': (('profiles/uk/0.1.0/README.md: '
                                                   'prohibited assertion '
                                                   "'compliance'",),
                                                  ()),
 'test_postposed_denial_agent_vs_rhetorical_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                              'prohibited assertion '
                                                              "'compliance'",),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited assertion '
                                                              "'compliance'",),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited control '
                                                              'weakening language',),
                                                             ('profiles/uk/0.1.0/README.md: '
                                                              'prohibited control '
                                                              'weakening language',),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             ()),
 'test_postposed_denial_and_rejection_polarity_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited assertion '
                                                                 "'compliance'",),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited assertion '
                                                                 "'compliance'",),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited assertion '
                                                                 "'compliance'",),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited assertion '
                                                                 "'compliance'",),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited assertion '
                                                                 "'compliance'",),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited assertion '
                                                                 "'compliance'",),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited assertion '
                                                                 "'compliance'",),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited control '
                                                                 'weakening language',),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited control '
                                                                 'weakening language',),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited control '
                                                                 'weakening language',),
                                                                ('profiles/uk/0.1.0/README.md: '
                                                                 'prohibited control '
                                                                 'weakening '
                                                                 'language',)),
 'test_postposed_denial_complement_boundary_cross_product': ((),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             (),
                                                             ()),
 'test_postposed_possessive_rhetorical_suffix_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'compliance'",)),
 'test_postposed_terminal_and_qualified_denial_cross_product': ((),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                (),
                                                                ()),
 'test_profile_specific_claim_denials_are_allowed': ((), (), (), (), (), (), ()),
 'test_profile_specific_claim_quotations_are_allowed': ((), (), (), (), (), (), (), ()),
 'test_profile_specific_positive_claims_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                         "prohibited assertion 'legal "
                                                         "sufficiency'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'external approval'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'production readiness'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'compliance'",)),
 'test_readiness_confirmation_requires_positive_establishment': ((), ()),
 'test_reordered_mapping_and_general_authority_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'imported mapping "
                                                                "relationship'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'imported mapping "
                                                                "relationship'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited assertion '
                                                                "'imported mapping "
                                                                "relationship'",),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',)),
 'test_reordered_mapping_and_general_authority_denials_are_allowed': ((), (), (), ()),
 'test_second_review_claim_word_order_polarity_pairs': ((),
                                                        (),
                                                        (),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'compliance'",),
                                                        (),
                                                        (),
                                                        (),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'compliance'",),
                                                        (),
                                                        (),
                                                        (),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'production readiness'",),
                                                        (),
                                                        (),
                                                        (),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'imported mapping "
                                                         "relationship'",)),
 'test_second_review_claim_word_orders_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'compliance'",),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'compliance'",),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'production readiness'",),
                                                       ('profiles/uk/0.1.0/README.md: '
                                                        'prohibited assertion '
                                                        "'imported mapping "
                                                        "relationship'",)),
 'test_second_review_direct_weakening_forms_are_rejected': (('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited control '
                                                             'weakening language',)),
 'test_second_review_direct_weakening_polarity_pairs': ((),
                                                        (),
                                                        (),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited control weakening '
                                                         'language',),
                                                        (),
                                                        (),
                                                        (),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited control weakening '
                                                         'language',)),
 'test_source_authority_after_denied_clause_is_rejected': (('profiles/uk/0.1.0/README.md: '
                                                            'prohibited source '
                                                            'authority language',),
                                                           ('profiles/uk/0.1.0/README.md: '
                                                            'prohibited source '
                                                            'authority language',)),
 'test_source_authority_denials_and_discussion_are_allowed': ((), (), (), ()),
 'test_source_boundary_rejects_excluded_authority_claims': (('profiles/uk/0.1.0/README.md: '
                                                             'prohibited source '
                                                             'authority language',),
                                                            ('profiles/uk/0.1.0/README.md: '
                                                             'prohibited source '
                                                             'authority language',)),
 'test_third_review_bounded_nonweakening_semantic_variations': ((), (), (), ()),
 'test_third_review_excluded_source_supply_aspect_and_voice': (('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               (),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               (),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               (),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',),
                                                               (),
                                                               (),
                                                               (),
                                                               ('profiles/uk/0.1.0/README.md: '
                                                                'prohibited source '
                                                                'authority language',)),
 'test_third_review_passive_aspect_claim_families': (('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'compliance'",),
                                                     (),
                                                     (),
                                                     (),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'compliance'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'compliance'",),
                                                     (),
                                                     (),
                                                     (),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'compliance'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'production readiness'",),
                                                     (),
                                                     (),
                                                     (),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'production readiness'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'production readiness'",),
                                                     (),
                                                     (),
                                                     (),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      'prohibited assertion '
                                                      "'production readiness'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      "prohibited assertion 'imported "
                                                      "mapping relationship'",),
                                                     (),
                                                     (),
                                                     (),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      "prohibited assertion 'imported "
                                                      "mapping relationship'",),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      "prohibited assertion 'imported "
                                                      "mapping relationship'",),
                                                     (),
                                                     (),
                                                     (),
                                                     ('profiles/uk/0.1.0/README.md: '
                                                      "prohibited assertion 'imported "
                                                      "mapping relationship'",)),
 'test_third_review_progressive_direct_weakening_forms': (('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          (),
                                                          (),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          (),
                                                          (),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          (),
                                                          (),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          (),
                                                          (),
                                                          (),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',)),
 'test_third_review_readiness_explicit_denial_family': ((),
                                                        (),
                                                        (),
                                                        (),
                                                        (),
                                                        (),
                                                        (),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'production readiness'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'production readiness'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'production readiness'",),
                                                        ('profiles/uk/0.1.0/README.md: '
                                                         'prohibited assertion '
                                                         "'production readiness'",)),
 'test_unrelated_denial_does_not_mask_later_control_weakening': (('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited control '
                                                                  'weakening '
                                                                  'language',),
                                                                 ('profiles/uk/0.1.0/README.md: '
                                                                  'prohibited control '
                                                                  'weakening '
                                                                  'language',)),
 'test_weakening_aspect_and_state_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',),
                                                   ('profiles/uk/0.1.0/README.md: '
                                                    'prohibited control weakening '
                                                    'language',)),
 'test_weakening_aspect_denial_and_metalinguistic_pairs': ((),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           ()),
 'test_weakening_cross_product_denials_and_claim_frames': ((),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           (),
                                                           ()),
 'test_weakening_state_grammar_matrix': (('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',),
                                         ('profiles/uk/0.1.0/README.md: prohibited '
                                          'control weakening language',)),
 'test_weakening_subject_modal_and_state_cross_product': (('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',),
                                                          ('profiles/uk/0.1.0/README.md: '
                                                           'prohibited control '
                                                           'weakening language',))}
_DIAGNOSTIC_FAMILIES = {'test_additional_assurance_claim_forms_are_rejected': (('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',)),
 'test_additional_assurance_denials_and_discussion_are_allowed': (('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',)),
 'test_additional_control_weakening_forms_are_rejected': (('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',)),
 'test_additional_weakening_denials_and_discussion_are_allowed': (('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',)),
 'test_affirmative_claim_after_denied_clause_is_rejected': (('claim',), ('claim',)),
 'test_affirmative_weakening_after_denial_is_rejected': (('claim',), ('claim',)),
 'test_approval_subject_voice_and_aspect_cross_product': (('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',)),
 'test_assurance_voice_tense_and_aspect_grammar_matrix': (('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',)),
 'test_bounded_adverb_slots_cross_product': (('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',),
                                             ('claim',)),
 'test_common_affirmative_control_weakening_is_rejected': (('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',)),
 'test_common_affirmative_profile_claim_variants_are_rejected': (('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',),
                                                                 ('claim',)),
 'test_contrast_clause_boundaries_do_not_mask_prohibited_language': (('claim',),
                                                                     ('claim',),
                                                                     ('source_authority',),
                                                                     ('claim',),
                                                                     ('claim',),
                                                                     ('source_authority',),
                                                                     ('claim',),
                                                                     ('claim',),
                                                                     ('source_authority',),
                                                                     ('claim',),
                                                                     ('claim',),
                                                                     ('source_authority',),
                                                                     ('claim',),
                                                                     ('claim',),
                                                                     ('source_authority',),
                                                                     ('claim',),
                                                                     ('claim',),
                                                                     ('source_authority',)),
 'test_declared_generic_authority_passive_aspect_cross_product': (('source_authority',),
                                                                  ('source_authority',),
                                                                  ('source_authority',),
                                                                  ('source_authority',),
                                                                  ('source_authority',),
                                                                  ('source_authority',),
                                                                  ('source_authority',),
                                                                  ('source_authority',),
                                                                  ('source_authority',)),
 'test_direct_weakening_object_and_complement_are_bounded': (('claim',), ('claim',)),
 'test_dynamic_authority_bounded_adverb_cross_product': (('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',)),
 'test_establishes_profile_claim_denials_are_allowed': (('claim',),
                                                        ('claim',),
                                                        ('claim',)),
 'test_establishes_profile_claim_quotations_are_allowed': (('claim',),
                                                           ('claim',),
                                                           ('claim',)),
 'test_establishes_profile_claim_variants_are_rejected': (('claim',),
                                                          ('claim',),
                                                          ('claim',)),
 'test_excluded_source_supply_and_derivation_are_rejected': (('source_authority',),
                                                             ('source_authority',),
                                                             ('source_authority',),
                                                             ('source_authority',),
                                                             ('source_authority',),
                                                             ('source_authority',),
                                                             ('source_authority',),
                                                             ('source_authority',)),
 'test_excluded_source_supply_and_derivation_polarity_pairs': (('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',)),
 'test_explicit_control_weakening_denials_are_allowed': (('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',)),
 'test_extended_polarity_and_metalinguistic_matrix': (('claim',),
                                                      ('claim',),
                                                      ('claim',),
                                                      ('claim',),
                                                      ('claim',),
                                                      ('claim',),
                                                      ('claim',),
                                                      ('claim',),
                                                      ('claim',),
                                                      ('claim',),
                                                      ('claim',)),
 'test_final_review_claim_assertions_are_rejected': (('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',)),
 'test_final_review_claim_polarity_and_clause_pairs': (('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',)),
 'test_identified_excluded_source_supply_forms_are_rejected': (('source_authority',),
                                                               ('source_authority',)),
 'test_identified_excluded_source_supply_polarity_pairs': (('source_authority',),
                                                           ('source_authority',),
                                                           ('source_authority',),
                                                           ('source_authority',),
                                                           ('source_authority',),
                                                           ('source_authority',),
                                                           ('source_authority',),
                                                           ('source_authority',)),
 'test_later_metalinguistic_discussion_does_not_mask_assertions': (('claim',),
                                                                   ('claim',),
                                                                   ('source_authority',)),
 'test_mapping_direction_and_authority_grammar_matrix': (('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('source_authority',),
                                                         ('claim',),
                                                         ('claim',),
                                                         ('source_authority',),
                                                         ('source_authority',)),
 'test_mapping_direction_form_and_aspect_cross_product': (('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',)),
 'test_metalinguistic_context_is_bounded_to_the_assertion': (('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',)),
 'test_natural_perfect_mandatory_denial_and_discussion_pairs': (('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',)),
 'test_natural_perfect_mandatory_placement_cross_product': (('claim',),
                                                            ('claim',),
                                                            ('claim',),
                                                            ('claim',)),
 'test_negated_rejection_head_cross_product': (('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',),
                                               ('claim',)),
 'test_negation_binding_complement_and_insertion_cross_product': (('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',)),
 'test_negative_modifiers_remain_polarity_cross_product': (('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',)),
 'test_new_control_weakening_quotations_are_allowed': (('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',)),
 'test_new_profile_claim_denials_are_allowed': (('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',),
                                                ('claim',)),
 'test_new_profile_claim_quotations_and_discussion_are_allowed': (('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',),
                                                                  ('claim',)),
 'test_omit_skip_and_reduce_control_forms_are_rejected': (('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',)),
 'test_omit_skip_and_reduce_polarity_pairs': (('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',),
                                              ('claim',)),
 'test_passive_affirmative_control_weakening_is_rejected': (('claim',),
                                                            ('claim',),
                                                            ('claim',),
                                                            ('claim',),
                                                            ('claim',),
                                                            ('claim',),
                                                            ('claim',),
                                                            ('claim',)),
 'test_passive_control_weakening_denials_are_allowed': (('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',)),
 'test_passive_control_weakening_quotations_are_allowed': (('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',)),
 'test_polarity_is_bound_to_the_assertion_head': (('claim',), ('claim',)),
 'test_postposed_denial_agent_vs_rhetorical_cross_product': (('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',)),
 'test_postposed_denial_and_rejection_polarity_cross_product': (('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',)),
 'test_postposed_denial_complement_boundary_cross_product': (('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',),
                                                             ('claim',)),
 'test_postposed_possessive_rhetorical_suffix_cross_product': (('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('claim',)),
 'test_postposed_terminal_and_qualified_denial_cross_product': (('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',)),
 'test_profile_specific_claim_denials_are_allowed': (('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',)),
 'test_profile_specific_claim_quotations_are_allowed': (('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',)),
 'test_profile_specific_positive_claims_are_rejected': (('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',)),
 'test_readiness_confirmation_requires_positive_establishment': (('claim',),
                                                                 ('claim',)),
 'test_reordered_mapping_and_general_authority_are_rejected': (('claim',),
                                                               ('claim',),
                                                               ('claim',),
                                                               ('source_authority',)),
 'test_reordered_mapping_and_general_authority_denials_are_allowed': (('claim',),
                                                                      ('claim',),
                                                                      ('claim',),
                                                                      ('source_authority',)),
 'test_second_review_claim_word_order_polarity_pairs': (('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',)),
 'test_second_review_claim_word_orders_are_rejected': (('claim',),
                                                       ('claim',),
                                                       ('claim',),
                                                       ('claim',)),
 'test_second_review_direct_weakening_forms_are_rejected': (('claim',), ('claim',)),
 'test_second_review_direct_weakening_polarity_pairs': (('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',)),
 'test_source_authority_after_denied_clause_is_rejected': (('source_authority',),
                                                           ('source_authority',)),
 'test_source_authority_denials_and_discussion_are_allowed': (('source_authority',),
                                                              ('source_authority',),
                                                              ('source_authority',),
                                                              ('source_authority',)),
 'test_source_boundary_rejects_excluded_authority_claims': (('source_authority',),
                                                            ('source_authority',)),
 'test_third_review_bounded_nonweakening_semantic_variations': (('claim',),
                                                                ('claim',),
                                                                ('claim',),
                                                                ('claim',)),
 'test_third_review_excluded_source_supply_aspect_and_voice': (('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',),
                                                               ('source_authority',)),
 'test_third_review_passive_aspect_claim_families': (('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',),
                                                     ('claim',)),
 'test_third_review_progressive_direct_weakening_forms': (('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',)),
 'test_third_review_readiness_explicit_denial_family': (('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',),
                                                        ('claim',)),
 'test_unrelated_denial_does_not_mask_later_control_weakening': (('claim',),
                                                                 ('claim',)),
 'test_weakening_aspect_and_state_cross_product': (('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',),
                                                   ('claim',)),
 'test_weakening_aspect_denial_and_metalinguistic_pairs': (('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',)),
 'test_weakening_cross_product_denials_and_claim_frames': (('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',),
                                                           ('claim',)),
 'test_weakening_state_grammar_matrix': (('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',),
                                         ('claim',)),
 'test_weakening_subject_modal_and_state_cross_product': (('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',),
                                                          ('claim',))}


def _build_profile_language_cases() -> tuple[ProfileLanguageCase, ...]:
    cases: list[ProfileLanguageCase] = []
    for method_name, builder_name in _CASE_BUILDERS:
        builder = _CaseBuilder()
        globals()[builder_name](builder)
        expected = _EXPECTED_DIAGNOSTICS[method_name]
        families = _DIAGNOSTIC_FAMILIES[method_name]
        if len(builder.records) != len(expected) or len(expected) != len(families):
            raise ValueError(f"builder metadata mismatch for {method_name}")
        identifier_prefix = method_name.removeprefix("test_")
        for index, ((text, excluded), diagnostics, diagnostic_families) in enumerate(
            zip(builder.records, expected, families), start=1
        ):
            cases.append(
                ProfileLanguageCase(
                    method_name=method_name,
                    case_id=f"{identifier_prefix}-{index:03d}",
                    text=text,
                    location=LOCATION,
                    diagnostic_families=diagnostic_families,
                    excluded_sources=excluded,
                    expected_diagnostics=diagnostics,
                )
            )
    return tuple(cases)


PROFILE_LANGUAGE_CASES = _build_profile_language_cases()


def profile_language_population_sha256(
    cases: Sequence[ProfileLanguageCase],
) -> str:
    payload = [
        {
            "method_name": case.method_name,
            "case_id": case.case_id,
            "text": case.text,
            "location": case.location,
            "diagnostic_families": case.diagnostic_families,
            "excluded_sources": case.excluded_sources,
            "expected_diagnostics": case.expected_diagnostics,
        }
        for case in cases
    ]
    canonical = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_profile_language_inventory(
    cases: Sequence[ProfileLanguageCase],
    methods: Sequence[MethodBaseline],
    exclusions: Sequence[ExcludedMethodBaseline],
    expected_sha256: str,
) -> ProfileLanguageInventory:
    case_tuple = tuple(cases)
    method_tuple = tuple(methods)
    exclusion_tuple = tuple(exclusions)

    method_names = [item.method_name for item in method_tuple]
    duplicates = [name for name, count in Counter(method_names).items() if count > 1]
    if duplicates:
        raise ValueError(f"duplicate method baseline: {duplicates[0]}")
    expected_names = [item.method_name for item in METHOD_BASELINES]
    missing = [name for name in expected_names if name not in method_names]
    if missing:
        raise ValueError(f"missing method baseline: {missing[0]}")
    extra = [name for name in method_names if name not in expected_names]
    if extra:
        raise ValueError(f"unexpected method baseline: {extra[0]}")

    identifiers: set[str] = set()
    counts = Counter(case.method_name for case in case_tuple)
    for case in case_tuple:
        if case.case_id in identifiers:
            raise ValueError(f"duplicate case identifier: {case.case_id}")
        identifiers.add(case.case_id)
        if case.method_name not in expected_names:
            raise ValueError(f"case references unknown method: {case.method_name}")
        if case.location != LOCATION:
            raise ValueError(f"invalid location for case {case.case_id}")
        if case.diagnostic_families not in (
            ("claim",),
            ("source_authority",),
            ("claim", "source_authority"),
        ):
            raise ValueError(
                f"invalid diagnostic families for case {case.case_id}: "
                f"{case.diagnostic_families!r}"
            )
        if not isinstance(case.excluded_sources, tuple):
            raise ValueError(
                f"excluded_sources must be a tuple for case {case.case_id}"
            )
        if not isinstance(case.expected_diagnostics, tuple):
            raise ValueError(
                f"expected_diagnostics must be a tuple for case {case.case_id}"
            )
        if len(set(case.expected_diagnostics)) != len(case.expected_diagnostics):
            raise ValueError(
                f"duplicate expected diagnostic for case {case.case_id}"
            )
        if case.expected_diagnostics != tuple(sorted(case.expected_diagnostics)):
            raise ValueError(
                f"expected diagnostics must be sorted for case {case.case_id}"
            )

    for baseline in method_tuple:
        actual = counts[baseline.method_name]
        if actual != baseline.validate_calls:
            raise ValueError(
                f"case count mismatch for {baseline.method_name}: "
                f"expected {baseline.validate_calls}, got {actual}"
            )
    if method_tuple != METHOD_BASELINES:
        raise ValueError("method baseline ledger mismatch")
    if len(case_tuple) != 908:
        raise ValueError(f"profile-language case total mismatch: {len(case_tuple)}")
    if sum(item.validate_calls for item in method_tuple) != 908:
        raise ValueError("selected validate-call total mismatch")
    if sum(item.successful_subtests for item in method_tuple) != 880:
        raise ValueError("selected successful-subtest total mismatch")
    if exclusion_tuple != EXCLUDED_METHOD_BASELINES:
        raise ValueError("excluded method baseline ledger mismatch")
    if sum(item.validate_calls for item in exclusion_tuple) != 15:
        raise ValueError("excluded validate-call total mismatch")
    if sum(item.successful_subtests for item in exclusion_tuple) != 13:
        raise ValueError("excluded successful-subtest total mismatch")
    if (
        sum(item.validate_calls for item in method_tuple)
        + sum(item.validate_calls for item in exclusion_tuple)
        != 923
    ):
        raise ValueError("repeated-call validate total mismatch")
    if (
        sum(item.successful_subtests for item in method_tuple)
        + sum(item.successful_subtests for item in exclusion_tuple)
        != 893
    ):
        raise ValueError("repeated-call successful-subtest total mismatch")
    distribution = Counter(case.excluded_sources for case in case_tuple)
    if dict(distribution) != EXPECTED_SOURCE_DISTRIBUTION:
        raise ValueError("excluded-source distribution mismatch")
    digest = profile_language_population_sha256(case_tuple)
    if digest != expected_sha256:
        raise ValueError("population digest mismatch")
    return ProfileLanguageInventory(
        cases=case_tuple,
        methods=method_tuple,
        exclusions=exclusion_tuple,
        population_sha256=digest,
    )


def profile_language_inventory() -> ProfileLanguageInventory:
    return validate_profile_language_inventory(
        PROFILE_LANGUAGE_CASES,
        METHOD_BASELINES,
        EXCLUDED_METHOD_BASELINES,
        EXPECTED_POPULATION_SHA256,
    )
