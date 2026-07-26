from __future__ import annotations

from copy import deepcopy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    ROOT / "crosswalks/schema/qualified-review-evidence.schema.json"
)
CORE_ID = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure"
    "--3.3--esaf-0.4-alpha--0.1.0"
)
PLUS_FORWARD_ID = (
    "uk-ncsc--cyber-essentials-plus-test-specification"
    "--3.2--esaf-0.4-alpha--0.1.0"
)
PLUS_REVERSE_ID = (
    "uk-ncsc--cyber-essentials-plus-test-specification"
    "--3.2--esaf-0.4-alpha--0.2.0"
)


class QualifiedReviewEvidenceSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)
        cls.valid_draft_campaign = {
            "schema_version": "1.0.0",
            "campaign_id": "uk-qualified-review-draft-2026-07-25",
            "phase": "draft_review",
            "candidate_state": "draft",
            "candidate_commit": "1" * 40,
            "retention_owner": "ESAF project owner",
            "retention_commitment": "Retain while the mapping is supported.",
            "mapping_sets": [
                {
                    "mapping_set_id": CORE_ID,
                    "package": {
                        "root": f"packages/{CORE_ID}",
                        "manifest_path": (
                            f"packages/{CORE_ID}/PACKAGE_MANIFEST.json"
                        ),
                        "manifest_sha256": "2" * 64,
                        "immutable_locator": f"urn:sha256:{'2' * 64}",
                        "retention_owner": "ESAF project owner",
                    },
                    "roles": [
                        {
                            "role": "specification_and_inventory",
                            "reviewer": {
                                "identity": "Reviewer Core Specification",
                                "organization": "Independent Review Ltd",
                                "verification_locator": (
                                    "https://evidence.example/reviewers/"
                                    "core-spec?version=1"
                                ),
                                "qualification": (
                                    "UK scheme and mapping inventory reviewer"
                                ),
                                "authorized_source_access": True,
                                "independent": True,
                                "conflicts": False,
                                "conflict_disposition": "Not applicable",
                            },
                            "owner_eligibility_accepted": True,
                            "dual_role_accepted": False,
                            "attestation": {
                                "path": "attestations/core-specification.md",
                                "immutable_locator": f"urn:sha256:{'3' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "3" * 64,
                            },
                            "worksheet": {
                                "path": "worksheets/core-specification.md",
                                "immutable_locator": f"urn:sha256:{'4' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "4" * 64,
                                "signed_sha256": "5" * 64,
                                "review_date": "2026-07-25",
                                "conclusion": "pass",
                                "findings_disposition": "No findings.",
                                "findings": [],
                            },
                        },
                        {
                            "role": "security_and_overclaiming",
                            "reviewer": {
                                "identity": "Reviewer Core Security",
                                "organization": "Independent Review Ltd",
                                "verification_locator": (
                                    "https://evidence.example/reviewers/"
                                    "core-security?version=1"
                                ),
                                "qualification": (
                                    "UK scheme and security mapping reviewer"
                                ),
                                "authorized_source_access": True,
                                "independent": True,
                                "conflicts": False,
                                "conflict_disposition": "Not applicable",
                            },
                            "owner_eligibility_accepted": True,
                            "dual_role_accepted": False,
                            "attestation": {
                                "path": "attestations/core-security.md",
                                "immutable_locator": f"urn:sha256:{'6' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "6" * 64,
                            },
                            "worksheet": {
                                "path": "worksheets/core-security.md",
                                "immutable_locator": f"urn:sha256:{'7' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "7" * 64,
                                "signed_sha256": "8" * 64,
                                "review_date": "2026-07-25",
                                "conclusion": "pass",
                                "findings_disposition": "No findings.",
                                "findings": [],
                            },
                        },
                    ],
                },
                {
                    "mapping_set_id": PLUS_FORWARD_ID,
                    "package": {
                        "root": f"packages/{PLUS_FORWARD_ID}",
                        "manifest_path": (
                            f"packages/{PLUS_FORWARD_ID}/PACKAGE_MANIFEST.json"
                        ),
                        "manifest_sha256": "9" * 64,
                        "immutable_locator": f"urn:sha256:{'9' * 64}",
                        "retention_owner": "ESAF project owner",
                    },
                    "roles": [
                        {
                            "role": "specification_and_inventory",
                            "reviewer": {
                                "identity": "Reviewer Plus Forward Specification",
                                "organization": "Independent Review Ltd",
                                "verification_locator": (
                                    "https://evidence.example/reviewers/"
                                    "plus-forward-spec?version=1"
                                ),
                                "qualification": (
                                    "UK scheme and mapping inventory reviewer"
                                ),
                                "authorized_source_access": True,
                                "independent": True,
                                "conflicts": False,
                                "conflict_disposition": "Not applicable",
                            },
                            "owner_eligibility_accepted": True,
                            "dual_role_accepted": False,
                            "attestation": {
                                "path": (
                                    "attestations/plus-forward-specification.md"
                                ),
                                "immutable_locator": f"urn:sha256:{'a' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "a" * 64,
                            },
                            "worksheet": {
                                "path": (
                                    "worksheets/plus-forward-specification.md"
                                ),
                                "immutable_locator": f"urn:sha256:{'b' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "b" * 64,
                                "signed_sha256": "c" * 64,
                                "review_date": "2026-07-25",
                                "conclusion": "pass",
                                "findings_disposition": "No findings.",
                                "findings": [],
                            },
                        },
                        {
                            "role": "security_and_overclaiming",
                            "reviewer": {
                                "identity": "Reviewer Plus Forward Security",
                                "organization": "Independent Review Ltd",
                                "verification_locator": (
                                    "https://evidence.example/reviewers/"
                                    "plus-forward-security?version=1"
                                ),
                                "qualification": (
                                    "UK scheme and security mapping reviewer"
                                ),
                                "authorized_source_access": True,
                                "independent": True,
                                "conflicts": False,
                                "conflict_disposition": "Not applicable",
                            },
                            "owner_eligibility_accepted": True,
                            "dual_role_accepted": False,
                            "attestation": {
                                "path": (
                                    "attestations/plus-forward-security.md"
                                ),
                                "immutable_locator": f"urn:sha256:{'d' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "d" * 64,
                            },
                            "worksheet": {
                                "path": "worksheets/plus-forward-security.md",
                                "immutable_locator": f"urn:sha256:{'e' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "e" * 64,
                                "signed_sha256": "f" * 64,
                                "review_date": "2026-07-25",
                                "conclusion": "pass",
                                "findings_disposition": "No findings.",
                                "findings": [],
                            },
                        },
                    ],
                },
                {
                    "mapping_set_id": PLUS_REVERSE_ID,
                    "package": {
                        "root": f"packages/{PLUS_REVERSE_ID}",
                        "manifest_path": (
                            f"packages/{PLUS_REVERSE_ID}/PACKAGE_MANIFEST.json"
                        ),
                        "manifest_sha256": "0" * 64,
                        "immutable_locator": f"urn:sha256:{'0' * 64}",
                        "retention_owner": "ESAF project owner",
                    },
                    "roles": [
                        {
                            "role": "specification_and_inventory",
                            "reviewer": {
                                "identity": "Reviewer Plus Reverse Specification",
                                "organization": "Independent Review Ltd",
                                "verification_locator": (
                                    "https://evidence.example/reviewers/"
                                    "plus-reverse-spec?version=1"
                                ),
                                "qualification": (
                                    "UK scheme and mapping inventory reviewer"
                                ),
                                "authorized_source_access": True,
                                "independent": True,
                                "conflicts": False,
                                "conflict_disposition": "Not applicable",
                            },
                            "owner_eligibility_accepted": True,
                            "dual_role_accepted": False,
                            "attestation": {
                                "path": (
                                    "attestations/plus-reverse-specification.md"
                                ),
                                "immutable_locator": f"urn:sha256:{'1' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "1" * 64,
                            },
                            "worksheet": {
                                "path": (
                                    "worksheets/plus-reverse-specification.md"
                                ),
                                "immutable_locator": f"urn:sha256:{'2' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "2" * 64,
                                "signed_sha256": "3" * 64,
                                "review_date": "2026-07-25",
                                "conclusion": "pass",
                                "findings_disposition": "No findings.",
                                "findings": [],
                            },
                        },
                        {
                            "role": "security_and_overclaiming",
                            "reviewer": {
                                "identity": "Reviewer Plus Reverse Security",
                                "organization": "Independent Review Ltd",
                                "verification_locator": (
                                    "https://evidence.example/reviewers/"
                                    "plus-reverse-security?version=1"
                                ),
                                "qualification": (
                                    "UK scheme and security mapping reviewer"
                                ),
                                "authorized_source_access": True,
                                "independent": True,
                                "conflicts": False,
                                "conflict_disposition": "Not applicable",
                            },
                            "owner_eligibility_accepted": True,
                            "dual_role_accepted": False,
                            "attestation": {
                                "path": (
                                    "attestations/plus-reverse-security.md"
                                ),
                                "immutable_locator": f"urn:sha256:{'4' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "4" * 64,
                            },
                            "worksheet": {
                                "path": "worksheets/plus-reverse-security.md",
                                "immutable_locator": f"urn:sha256:{'5' * 64}",
                                "retention_owner": "ESAF project owner",
                                "sha256": "5" * 64,
                                "signed_sha256": "6" * 64,
                                "review_date": "2026-07-25",
                                "conclusion": "pass",
                                "findings_disposition": "No findings.",
                                "findings": [],
                            },
                        },
                    ],
                },
            ],
        }

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_literal_six_role_draft_campaign_is_valid(self) -> None:
        self.validator.validate(self.valid_draft_campaign)

    def test_rejects_unknown_campaign_property(self) -> None:
        invalid = deepcopy(self.valid_draft_campaign)
        invalid["unexpected"] = "not allowed"
        self.assertFalse(self.validator.is_valid(invalid))

    def test_rejects_missing_role_record(self) -> None:
        invalid = deepcopy(self.valid_draft_campaign)
        invalid["mapping_sets"][0]["roles"].pop()
        self.assertFalse(self.validator.is_valid(invalid))

    def test_rejects_duplicate_mapping_set_entry(self) -> None:
        invalid = deepcopy(self.valid_draft_campaign)
        invalid["mapping_sets"][1] = deepcopy(invalid["mapping_sets"][0])
        self.assertFalse(self.validator.is_valid(invalid))

    def test_rejects_malformed_candidate_sha(self) -> None:
        invalid = deepcopy(self.valid_draft_campaign)
        invalid["candidate_commit"] = "A" * 40
        self.assertFalse(self.validator.is_valid(invalid))

    def test_rejects_unsafe_local_path(self) -> None:
        invalid = deepcopy(self.valid_draft_campaign)
        invalid["mapping_sets"][0]["roles"][0]["worksheet"]["path"] = (
            "../outside.md"
        )
        self.assertFalse(self.validator.is_valid(invalid))

    def test_rejects_invalid_immutable_locator(self) -> None:
        invalid = deepcopy(self.valid_draft_campaign)
        invalid["mapping_sets"][0]["package"]["immutable_locator"] = (
            "file:///local/package"
        )
        self.assertFalse(self.validator.is_valid(invalid))

    def test_rejects_missing_nested_retention_owner(self) -> None:
        invalid = deepcopy(self.valid_draft_campaign)
        del invalid["mapping_sets"][0]["roles"][0]["attestation"][
            "retention_owner"
        ]
        self.assertFalse(self.validator.is_valid(invalid))

    def test_rejects_final_campaign_without_draft_campaign_reference(
        self,
    ) -> None:
        invalid = deepcopy(self.valid_draft_campaign)
        invalid["phase"] = "final_reviewed_confirmation"
        invalid["candidate_state"] = "reviewed"
        self.assertFalse(self.validator.is_valid(invalid))

    def test_final_campaign_requires_exact_draft_reference_shape(self) -> None:
        valid = deepcopy(self.valid_draft_campaign)
        valid["phase"] = "final_reviewed_confirmation"
        valid["candidate_state"] = "reviewed"
        valid["candidate_commit"] = "7" * 40
        valid["draft_campaign_reference"] = {
            "campaign_id": "uk-qualified-review-draft-2026-07-25",
            "candidate_commit": "1" * 40,
            "manifest_sha256": "8" * 64,
            "seal_record_sha256": "9" * 64,
        }
        self.validator.validate(valid)

    def test_rejects_accepted_critical_or_important_finding(self) -> None:
        for severity in ("Critical", "Important"):
            with self.subTest(severity=severity):
                invalid = deepcopy(self.valid_draft_campaign)
                invalid["mapping_sets"][0]["roles"][0]["worksheet"][
                    "findings"
                ] = [
                    {
                        "finding_id": "finding-001",
                        "affected_record_ids": ["CE-001"],
                        "severity": severity,
                        "status": "accepted",
                        "disposition": "Accepted risk.",
                        "resolver_or_acceptor": "Project owner",
                        "disposition_date": "2026-07-25",
                        "acceptance_rationale": "Risk accepted.",
                    }
                ]
                self.assertFalse(self.validator.is_valid(invalid))

    def test_accepts_minor_finding_with_named_acceptance_evidence(self) -> None:
        valid = deepcopy(self.valid_draft_campaign)
        valid["mapping_sets"][0]["roles"][0]["worksheet"]["conclusion"] = (
            "stop"
        )
        valid["mapping_sets"][0]["roles"][0]["worksheet"]["findings"] = [
            {
                "finding_id": "finding-001",
                "affected_record_ids": ["CE-001"],
                "severity": "Minor",
                "status": "accepted",
                "disposition": "Accepted for this release.",
                "resolver_or_acceptor": "Project owner",
                "disposition_date": "2026-07-25",
                "acceptance_rationale": "No material mapping effect.",
            }
        ]
        self.validator.validate(valid)

    def test_conflict_disposition_tracks_conflict_declaration(self) -> None:
        invalid_without_conflict = deepcopy(self.valid_draft_campaign)
        invalid_without_conflict["mapping_sets"][0]["roles"][0]["reviewer"][
            "conflict_disposition"
        ] = "Owner reviewed the conflict."
        self.assertFalse(self.validator.is_valid(invalid_without_conflict))

        invalid_with_conflict = deepcopy(self.valid_draft_campaign)
        reviewer = invalid_with_conflict["mapping_sets"][0]["roles"][0][
            "reviewer"
        ]
        reviewer["conflicts"] = True
        reviewer["conflict_disposition"] = ""
        self.assertFalse(self.validator.is_valid(invalid_with_conflict))

    def test_post_correction_sha_is_conditional_on_conclusion(self) -> None:
        corrected = deepcopy(self.valid_draft_campaign)
        worksheet = corrected["mapping_sets"][0]["roles"][0]["worksheet"]
        worksheet["conclusion"] = "pass_after_correction"
        worksheet["post_correction_candidate_sha"] = "1" * 40
        self.validator.validate(corrected)

        missing = deepcopy(corrected)
        del missing["mapping_sets"][0]["roles"][0]["worksheet"][
            "post_correction_candidate_sha"
        ]
        self.assertFalse(self.validator.is_valid(missing))

        unexpected = deepcopy(self.valid_draft_campaign)
        unexpected["mapping_sets"][0]["roles"][0]["worksheet"][
            "post_correction_candidate_sha"
        ] = "1" * 40
        self.assertFalse(self.validator.is_valid(unexpected))


if __name__ == "__main__":
    unittest.main()
