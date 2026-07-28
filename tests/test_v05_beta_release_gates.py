from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tools.release_gates import (
    load_front_matter as load_v04_front_matter,
    validate_record as validate_v04_record,
)
from tools.build_mapping_review_bundle import (
    PROFILES,
    GitReader,
    assemble_package,
    parse_front_matter_bytes,
)
from tools.crosswalks.qualified_review_evidence import (
    build_campaign_archive,
    build_seal_record,
    canonical_json_bytes as official_canonical_json_bytes,
)
from tools.validate_qualified_review_evidence import VALIDATOR_VERSION
from tests.test_validate_qualified_review_evidence import CampaignFixture
from tools import v05_beta_release_gates
from tools.v05_beta_release_gates import (
    PHASE_GATE_STATES,
    RECORD_RELATIVE,
    derive_scope,
    load_front_matter,
    validate_external_evidence,
    validate_record,
    validate_transition,
)


ROOT = Path(__file__).resolve().parents[1]
V04_RECORD = ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
V05_RECORD = ROOT / RECORD_RELATIVE
CANONICAL_READINESS_BODY = V05_RECORD.read_text(encoding="utf-8").split(
    "\n---\n",
    1,
)[1]
EXPECTED_SCOPE = {
    "controls": 91,
    "control_families": 16,
    "architecture_patterns": 7,
    "mapping_sets": 3,
    "mapping_provisions": 404,
    "relationship_legs": 81,
    "negative_dispositions": 325,
    "assessment_foundation": True,
    "draft_profiles": 1,
    "pci_dss_disposition": "HOLD",
}
EXPECTED_CLOSURE_ALLOWLIST = {
    "VERSION.md",
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "project/RELEASE_PLAN.md",
    RECORD_RELATIVE,
}


def readiness_document(
    record: dict[str, object],
    body: str = CANONICAL_READINESS_BODY,
) -> str:
    return "---\n" + json.dumps(record) + "\n---\n" + body
MAPPING_SETS = [
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
]
CLOSURE_SHA = "c" * 40
CLOSURE_BASE = "b" * 40
MERGE_SHA = "d" * 40
CLOSURE_TREE = "e" * 40
FIXED_NOW = datetime(2026, 7, 27, 12, 10, tzinfo=timezone.utc)
COMMAND_IDS = (
    "full_suite",
    "assessment",
    "profiles",
    "controls",
    "architectures",
    "migration",
    "crosswalk_current",
    "crosswalk_baseline",
    "pci_readiness",
    "links",
    "release_v04",
    "release_v05",
    "mermaid_inventory",
    "mermaid_rendering",
    "whole_range_diff",
    "cache_count",
    "clean_status",
)
MISSING_ROLES = (
    "specification_and_inventory",
    "security_and_overclaiming",
)
REENTRY_TRIGGERS = {
    "eligible_qualified_reviewer_available",
    "mapping_or_source_inventory_changes",
    "owner_decision_expires_withdrawn_edited_or_superseded",
    "accountable_owner_requires_earlier_completion",
    "closure_candidate_or_merged_tree_changes",
}
CLAIMS_NOT_MADE = {
    "qualified_review",
    "qualified_mapping_approval",
    "artifact_lifecycle_approval",
    "certification",
    "compliance",
    "equivalence",
    "endorsement",
    "external_scheme_approval",
    "production_readiness",
    "assurance",
    "implementation_assessment",
    "legal_sufficiency",
    "replacement_of_qualified_professional_judgment",
}
QUALIFIED_SCHEMA = (
    "https://esaf-standard.org/schemas/"
    "qualified-review-evidence.schema.json"
)


def record_fixture(phase: str) -> dict[str, object]:
    states = PHASE_GATE_STATES[phase]
    return {
        "release": "0.5-beta",
        "tag": "v0.5-beta",
        "issue": 59,
        "repository_scope": "complete_git_tracked_repository",
        "phase": phase,
        "mapping_decision_basis": "qualified_approval",
        "mapping_sets": MAPPING_SETS,
        "scope": deepcopy(EXPECTED_SCOPE),
        "publication": {
            "condition": "remote_annotated_tag_matches_exact_validated_commit",
            "date": "2026-07-27" if phase == "published" else None,
            "evidence": ["https://example.test/release-record"],
        },
        "gates": {
            gate: {
                "state": state,
                "evidence": [f"https://example.test/{gate}"]
                if state in {"ready", "closed"}
                else [],
            }
            for gate, state in states.items()
        },
    }


def source_fixture(resource_id: str) -> dict[str, object]:
    resource_path = f"repos/tdistress/ESAF/issues/comments/{resource_id}"
    return {
        "repository": "tdistress/ESAF",
        "resource_path": resource_path,
        "comment_url": (
            "https://github.com/tdistress/ESAF/issues/59"
            f"#issuecomment-{resource_id}"
        ),
        "comment_id": int(resource_id),
        "author_login": "reviewer",
        "author_user_id": 1000 + int(resource_id),
        "author_association": "COLLABORATOR",
        "created_at": "2026-07-27T12:00:00Z",
        "updated_at": "2026-07-27T12:00:00Z",
        "body_sha256": "a" * 64,
        "response_sha256": "b" * 64,
        "acquisition_resource_id": resource_path,
        "source_verified_at": "2026-07-27T12:05:00Z",
    }


def sourced_verdict(name: str, resource_id: str) -> dict[str, object]:
    return {
        "sha": CLOSURE_SHA,
        "reviewer": f"{name} reviewer",
        "role": f"{name} reviewer",
        "date": "2026-07-27",
        "disposition": "approved",
        "url": source_fixture(resource_id)["comment_url"],
        "critical": 0,
        "important": 0,
        "source": source_fixture(resource_id),
    }


def mermaid_result(*, taggable: bool = False) -> dict[str, object]:
    result: dict[str, object] = {
        "rendered_blocks": 23,
        "renderer": "@mermaid-js/mermaid-cli@11.16.0",
        "visual_review": "approved",
        "candidate_inventory_equal": True,
        "candidate_review_url": (
            "https://github.com/tdistress/ESAF/issues/59#issuecomment-14"
        ),
        "candidate_reviewer": "candidate rendering reviewer",
        "reviewed_at": "2026-07-27T12:05:00Z",
    }
    if taggable:
        result.update(
            {
                "merge_tree_equal": True,
                "post_merge_reviewer": "post-merge rendering reviewer",
            }
        )
    return result


def command_results(
    sha: str | None, *, taggable: bool = False
) -> list[dict[str, object]]:
    return [
        {
            "name": name,
            "exit_code": 0,
            "result": (
                mermaid_result(taggable=taggable)
                if name == "mermaid_rendering"
                else "passed"
            ),
            **({"sha": sha} if sha is not None else {}),
        }
        for name in COMMAND_IDS
    ]


def missing_roles() -> list[dict[str, str]]:
    return [
        {"mapping_set_id": mapping_set_id, "role": role}
        for mapping_set_id in MAPPING_SETS
        for role in MISSING_ROLES
    ]


def owner_decision(mapping_set_id: str) -> dict[str, object]:
    owner_source = source_fixture("20")
    owner_source["author_login"] = "tdistress"
    owner_source["author_association"] = "OWNER"
    return {
        "mapping_set_id": mapping_set_id,
        "mapping_decision_basis": "owner_risk_acceptance",
        "decision_type": "owner_risk_acceptance",
        "sha": CLOSURE_SHA,
        "disposition": "accepted_for_working_draft",
        "qualified_review_status": "deferred",
        "missing_qualified_roles": missing_roles(),
        "accountable_owner": "tdistress",
        "issue_55_status": "remains_open",
        "lifecycle": "draft",
        "claims_not_made": sorted(CLAIMS_NOT_MADE),
        "reentry_triggers": sorted(REENTRY_TRIGGERS),
        "url": owner_source["comment_url"],
        "source": owner_source,
    }


def closure_evidence() -> dict[str, object]:
    governance = sourced_verdict("governance", "16")
    governance["reviewer"] = "governance-approver"
    governance["role"] = "Steering Committee approver"
    governance["source"]["author_login"] = "governance-approver"
    governance.update(
        {
            "disposition": "approved_for_working_draft_publication",
            "authority": "Steering Committee",
            "authority_attestation": True,
            "authority_verification": "manual",
            "authority_basis": "GOVERNANCE.md#21-steering-committee",
        }
    )
    scope = sourced_verdict("scope", "10")
    owner_source = source_fixture("20")
    owner_source["author_login"] = "tdistress"
    owner_source["author_association"] = "OWNER"
    scope["reviewer"] = "tdistress"
    scope["role"] = "repository owner"
    scope["url"] = owner_source["comment_url"]
    scope["source"] = owner_source
    scope.update(
        {
            "disposition": "approved_for_working_draft_closure",
            "scope": "complete_git_tracked_repository",
            "milestone": "v0.5-beta",
        }
    )
    return {
        "schema": "esaf-v05-release-evidence-v1",
        "release": "0.5-beta",
        "closure_base": CLOSURE_BASE,
        "closure_head": CLOSURE_SHA,
        "closure_tree": CLOSURE_TREE,
        "scope": scope,
        "technical": sourced_verdict("technical", "11"),
        "editorial": sourced_verdict("editorial", "12"),
        "terminology": sourced_verdict("terminology", "13"),
        "rendering": sourced_verdict("rendering", "14"),
        "profile_scope": sourced_verdict("profile scope", "15"),
        "governance": governance,
        "candidate_commands": command_results(CLOSURE_SHA),
        "mapping_decision_schema": "esaf-v05-owner-decision-v1",
        "mapping_decision_basis": "owner_risk_acceptance",
        "mapping_decisions": [
            owner_decision(mapping_set_id) for mapping_set_id in MAPPING_SETS
        ],
        "github_checks": {
            "expected": ["Validate ESAF sources"],
            "observed": [
                {
                    "name": "Validate ESAF sources",
                    "sha": CLOSURE_SHA,
                    "conclusion": "success",
                    "url": "https://github.com/tdistress/ESAF/actions/runs/1",
                }
            ],
        },
        "merge_state": {
            "sha": CLOSURE_SHA,
            "mergeable": True,
            "state": "clean",
        },
        "tag_state": {
            "resource": "repos/tdistress/ESAF/git/ref/tags/v0.5-beta",
            "exists": False,
            "status": 404,
            "response_sha256": "c" * 64,
        },
        "acquisition": {
            "schema": "esaf-v05-acquisition-v1",
            "repository": "tdistress/ESAF",
            "authenticated_login": "tdistress",
            "retrieved_at": "2026-07-27T12:05:00Z",
            "complete": True,
            "resources": [
                {
                    "resource_id": source_fixture(identifier)["resource_path"],
                    "observed_canonical_url": source_fixture(identifier)[
                        "comment_url"
                    ],
                    "page_count": 1,
                    "response_sha256": source_fixture(identifier)[
                        "response_sha256"
                    ],
                }
                for identifier in (
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "20",
                    "21",
                )
            ]
            + [
                {
                    "resource_id": "user",
                    "observed_canonical_url": (
                        "https://github.com/tdistress"
                    ),
                    "page_count": 1,
                    "response_sha256": "d" * 64,
                },
                {
                    "resource_id": (
                        f"repos/tdistress/ESAF/commits/{CLOSURE_SHA}"
                    ),
                    "observed_canonical_url": (
                        "https://github.com/tdistress/ESAF/commit/"
                        f"{CLOSURE_SHA}"
                    ),
                    "page_count": 1,
                    "response_sha256": "e" * 64,
                },
                {
                    "resource_id": "repos/tdistress/ESAF/pulls/59",
                    "observed_canonical_url": (
                        "https://github.com/tdistress/ESAF/pull/59"
                    ),
                    "page_count": 1,
                    "response_sha256": "f" * 64,
                },
                {
                    "resource_id": (
                        f"repos/tdistress/ESAF/commits/{CLOSURE_SHA}/"
                        "check-runs"
                    ),
                    "observed_canonical_url": (
                        "https://github.com/tdistress/ESAF/actions/runs/1"
                    ),
                    "page_count": 1,
                    "response_sha256": "0" * 64,
                },
                {
                    "resource_id": (
                        "repos/tdistress/ESAF/git/ref/tags/v0.5-beta"
                    ),
                    "observed_canonical_url": (
                        "https://api.github.com/repos/tdistress/ESAF/"
                        "git/ref/tags/v0.5-beta"
                    ),
                    "page_count": 1,
                    "response_sha256": "c" * 64,
                }
            ],
        },
    }


def taggable_evidence() -> dict[str, object]:
    evidence = closure_evidence()
    evidence["acquisition"]["resources"].append(
        {
            "resource_id": f"repos/tdistress/ESAF/commits/{MERGE_SHA}",
            "observed_canonical_url": (
                "https://github.com/tdistress/ESAF/commit/"
                f"{MERGE_SHA}"
            ),
            "page_count": 1,
            "response_sha256": "1" * 64,
        }
    )
    evidence.update(
        {
            "merge_head": MERGE_SHA,
            "merge_tree": CLOSURE_TREE,
            "post_merge": {
                "schema": "esaf-v05-post-merge-results-v1",
                "sha": MERGE_SHA,
                "tree": CLOSURE_TREE,
                "commands": command_results(None, taggable=True),
            },
        }
    )
    return evidence


def bind_closure_head(evidence: dict[str, object], sha: str) -> None:
    previous = evidence["closure_head"]
    evidence["closure_head"] = sha
    for name in (
        "scope",
        "technical",
        "editorial",
        "terminology",
        "rendering",
        "profile_scope",
        "governance",
    ):
        evidence[name]["sha"] = sha
    for command in evidence["candidate_commands"]:
        command["sha"] = sha
    evidence["github_checks"]["observed"][0]["sha"] = sha
    evidence["merge_state"]["sha"] = sha
    for resource in evidence["acquisition"]["resources"]:
        if resource["resource_id"] == (
            f"repos/tdistress/ESAF/commits/{previous}"
        ):
            resource["resource_id"] = (
                f"repos/tdistress/ESAF/commits/{sha}"
            )
            resource["observed_canonical_url"] = (
                f"https://github.com/tdistress/ESAF/commit/{sha}"
            )
        elif resource["resource_id"] == (
            f"repos/tdistress/ESAF/commits/{previous}/check-runs"
        ):
            resource["resource_id"] = (
                f"repos/tdistress/ESAF/commits/{sha}/check-runs"
            )


class V05ExternalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.qualified_template_temporary = tempfile.TemporaryDirectory()
        cls.qualified_template_root = (
            Path(cls.qualified_template_temporary.name) / "retained"
        )
        campaign_root = cls.qualified_template_root / "campaign"
        sealed_root = cls.qualified_template_root / "sealed"
        campaign_root.mkdir(parents=True)
        sealed_root.mkdir()
        cls.qualified_candidate = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        cls.qualified_reader = GitReader(ROOT)
        cls.qualified_assemblies = {
            profile.mapping_set_id: assemble_package(
                cls.qualified_reader,
                cls.qualified_candidate,
                profile,
            )
            for profile in PROFILES.values()
        }
        CampaignFixture(
            campaign_root,
            cls.qualified_candidate,
            cls.qualified_assemblies,
        )
        allowlist = tuple(
            sorted(
                path.relative_to(campaign_root).as_posix()
                for path in campaign_root.rglob("*")
                if path.is_file()
            )
        )
        archive_bytes = build_campaign_archive(campaign_root, allowlist)
        manifest_bytes = (campaign_root / "REVIEW_EVIDENCE.json").read_bytes()
        _seal_record, seal_bytes = build_seal_record(
            manifest_bytes=manifest_bytes,
            archive_bytes=archive_bytes,
            archive_locator=(
                "https://evidence.example.invalid/campaign.zip?version=1"
            ),
            campaign_id="issue-55-draft-review",
            candidate_commit=cls.qualified_candidate,
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            validator_version=VALIDATOR_VERSION,
        )
        (sealed_root / "CAMPAIGN_ARCHIVE.zip").write_bytes(archive_bytes)
        (sealed_root / "CAMPAIGN_SEAL.json").write_bytes(seal_bytes)
        cls.qualified_affected_record_id = ""
        for assembly in cls.qualified_assemblies.values():
            for payload in assembly.payloads:
                if payload.purpose == "mapping record":
                    metadata, _body = parse_front_matter_bytes(payload.content)
                    cls.qualified_affected_record_id = str(metadata["record_id"])
                    break
            if cls.qualified_affected_record_id:
                break

    @classmethod
    def tearDownClass(cls) -> None:
        cls.qualified_template_temporary.cleanup()

    def official_qualified_evidence(self) -> dict[str, object]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        retained_root = Path(temporary.name) / "retained"
        shutil.copytree(self.qualified_template_root, retained_root)
        evidence = closure_evidence()
        bind_closure_head(evidence, self.qualified_candidate)
        evidence["mapping_decision_schema"] = QUALIFIED_SCHEMA
        evidence["mapping_decision_basis"] = "qualified_approval"
        evidence["mapping_decisions"] = [
            {
                "retained_root": str(retained_root),
                "campaign_path": "campaign",
                "archive_path": "sealed/CAMPAIGN_ARCHIVE.zip",
                "seal_path": "sealed/CAMPAIGN_SEAL.json",
                "source": source_fixture("21"),
            }
        ]
        return evidence

    def official_qualified_paths(
        self, evidence: dict[str, object]
    ) -> tuple[Path, Path, Path]:
        decision = evidence["mapping_decisions"][0]
        retained_root = Path(decision["retained_root"])
        return (
            retained_root / decision["campaign_path"],
            retained_root / decision["archive_path"],
            retained_root / decision["seal_path"],
        )

    def rewrite_official_role(
        self,
        evidence: dict[str, object],
        mutate: object,
    ) -> None:
        campaign_root, _archive_path, _seal_path = (
            self.official_qualified_paths(evidence)
        )
        manifest_path = campaign_root / "REVIEW_EVIDENCE.json"
        manifest = json.loads(manifest_path.read_bytes())
        mapping_set = manifest["mapping_sets"][0]
        role = mapping_set["roles"][0]
        mutate(role)
        fixture = CampaignFixture.__new__(CampaignFixture)
        fixture.root = campaign_root
        fixture.candidate = self.qualified_candidate
        fixture.assemblies = self.qualified_assemblies
        fixture.phase = "draft_review"
        fixture.campaign_id = "issue-55-draft-review"
        fixture.candidate_state = "draft"
        fixture.manifest = manifest
        profile = PROFILES[str(mapping_set["mapping_set_id"])]
        fixture.write_role(profile, mapping_set, role)
        fixture.write_manifest()

    def reseal_official_campaign(
        self, evidence: dict[str, object]
    ) -> None:
        campaign_root, archive_path, seal_path = self.official_qualified_paths(
            evidence
        )
        allowlist = tuple(
            sorted(
                path.relative_to(campaign_root).as_posix()
                for path in campaign_root.rglob("*")
                if path.is_file()
            )
        )
        archive_bytes = build_campaign_archive(campaign_root, allowlist)
        manifest_bytes = (campaign_root / "REVIEW_EVIDENCE.json").read_bytes()
        _seal_record, seal_bytes = build_seal_record(
            manifest_bytes=manifest_bytes,
            archive_bytes=archive_bytes,
            archive_locator=(
                "https://evidence.example.invalid/campaign.zip?version=1"
            ),
            campaign_id="issue-55-draft-review",
            candidate_commit=self.qualified_candidate,
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            validator_version=VALIDATOR_VERSION,
        )
        archive_path.write_bytes(archive_bytes)
        seal_path.write_bytes(seal_bytes)

    def assert_rejected(
        self, evidence: dict[str, object], diagnostic: str, phase: str
    ) -> None:
        errors = validate_external_evidence(
            ROOT,
            record_fixture("closure_candidate"),
            evidence,
            MERGE_SHA if phase == "taggable" else CLOSURE_SHA,
            phase,
            FIXED_NOW,
        )
        self.assertIn(diagnostic, errors)

    def test_complete_closure_and_taggable_evidence_are_accepted(self) -> None:
        owner_record = record_fixture("closure_candidate")
        owner_record["mapping_decision_basis"] = "owner_risk_acceptance"
        self.assertEqual(
            [],
            validate_external_evidence(
                ROOT,
                owner_record,
                closure_evidence(),
                CLOSURE_SHA,
                "closure",
                FIXED_NOW,
            ),
        )
        self.assertEqual(
            [],
            validate_external_evidence(
                ROOT,
                owner_record,
                taggable_evidence(),
                MERGE_SHA,
                "taggable",
                FIXED_NOW,
            ),
        )

    def test_closure_evidence_rejects_extra_top_level_key(self) -> None:
        evidence = closure_evidence()
        evidence["untrusted"] = {}
        self.assert_rejected(
            evidence, "closure evidence has unknown keys: untrusted", "closure"
        )

    def test_tag_state_requires_exact_live_absence_proof(self) -> None:
        for field, value in (
            ("resource", "repos/other/project/git/ref/tags/v0.5-beta"),
            ("exists", True),
            ("status", 200),
            ("response_sha256", "not-a-digest"),
        ):
            with self.subTest(field=field):
                evidence = closure_evidence()
                evidence["tag_state"][field] = value
                self.assert_rejected(
                    evidence,
                    "remote tag state shall prove exact v0.5-beta absence",
                    "closure",
                )

    def test_acquisition_resource_requires_page_count_and_response_digest(
        self,
    ) -> None:
        for field in ("page_count", "response_sha256"):
            with self.subTest(field=field):
                evidence = closure_evidence()
                del evidence["acquisition"]["resources"][0][field]
                self.assert_rejected(
                    evidence,
                    "acquisition resource identifiers are invalid",
                    "closure",
                )

    def test_source_and_tag_digests_match_their_acquired_responses(
        self,
    ) -> None:
        evidence = closure_evidence()
        evidence["technical"]["source"]["response_sha256"] = "d" * 64
        self.assert_rejected(
            evidence,
            "technical source response digest shall equal acquired response",
            "closure",
        )

    def test_acquisition_manifest_covers_user_commit_pr_checks_and_tag(
        self,
    ) -> None:
        required = (
            "user",
            f"repos/tdistress/ESAF/commits/{CLOSURE_SHA}",
            "repos/tdistress/ESAF/pulls/59",
            f"repos/tdistress/ESAF/commits/{CLOSURE_SHA}/check-runs",
            "repos/tdistress/ESAF/git/ref/tags/v0.5-beta",
        )
        for resource in required:
            with self.subTest(resource=resource):
                evidence = closure_evidence()
                evidence["acquisition"]["resources"] = [
                    item
                    for item in evidence["acquisition"]["resources"]
                    if item["resource_id"] != resource
                ]
                self.assert_rejected(
                    evidence,
                    "acquisition manifest is missing required resources",
                    "closure",
                )
        evidence = closure_evidence()
        evidence["tag_state"]["response_sha256"] = "d" * 64
        self.assert_rejected(
            evidence,
            "remote tag state shall bind the acquired tag response",
            "closure",
        )

    def test_exact_schema_requires_all_phase_keys(self) -> None:
        for phase, field, diagnostic in (
            ("closure", "closure_base", "closure evidence is missing keys: closure_base"),
            ("closure", "closure_head", "closure evidence is missing keys: closure_head"),
            ("closure", "closure_tree", "closure evidence is missing keys: closure_tree"),
            ("taggable", "merge_head", "taggable evidence is missing keys: merge_head"),
            ("taggable", "merge_tree", "taggable evidence is missing keys: merge_tree"),
            ("taggable", "post_merge", "taggable evidence is missing keys: post_merge"),
        ):
            with self.subTest(phase=phase, field=field):
                evidence = (
                    taggable_evidence() if phase == "taggable" else closure_evidence()
                )
                evidence.pop(field)
                self.assert_rejected(evidence, diagnostic, phase)

    def test_sha_domains_and_tree_equality_are_exact(self) -> None:
        cases = (
            (
                "closure head",
                "closure",
                lambda value: value.__setitem__("closure_head", "a" * 40),
                "closure head shall equal expected head",
            ),
            (
                "taggable merge head",
                "taggable",
                lambda value: value.__setitem__("merge_head", "a" * 40),
                "merge head shall equal expected head",
            ),
            (
                "changed merge tree",
                "taggable",
                lambda value: value.__setitem__("merge_tree", "f" * 40),
                "merged tree shall equal closure tree",
            ),
            (
                "post-merge tree",
                "taggable",
                lambda value: value["post_merge"].__setitem__("tree", "f" * 40),
                "post-merge tree shall equal merged tree",
            ),
        )
        for name, phase, mutate, diagnostic in cases:
            with self.subTest(name=name):
                evidence = (
                    taggable_evidence() if phase == "taggable" else closure_evidence()
                )
                mutate(evidence)
                self.assert_rejected(evidence, diagnostic, phase)

    def test_verdict_requires_body_digest(self) -> None:
        evidence = closure_evidence()
        del evidence["technical"]["source"]["body_sha256"]
        self.assert_rejected(
            evidence, "technical source keys are invalid", "closure"
        )

    def test_sourced_verdicts_require_exact_candidate_and_clean_findings(self) -> None:
        cases = (
            (
                "missing reviewer",
                lambda value: value["editorial"].__setitem__("reviewer", " "),
                "editorial reviewer shall be named",
            ),
            (
                "wrong SHA",
                lambda value: value["terminology"].__setitem__("sha", "a" * 40),
                "terminology verdict shall be bound to closure head",
            ),
            (
                "wrong disposition",
                lambda value: value["profile_scope"].__setitem__(
                    "disposition", "pending"
                ),
                "profile_scope verdict disposition is invalid",
            ),
            (
                "important finding",
                lambda value: value["rendering"].__setitem__("important", 1),
                "rendering verdict findings shall be zero",
            ),
        )
        for name, mutate, diagnostic in cases:
            with self.subTest(name=name):
                evidence = closure_evidence()
                mutate(evidence)
                self.assert_rejected(evidence, diagnostic, "closure")

    def test_governance_requires_manual_authority_attestation(self) -> None:
        evidence = closure_evidence()
        evidence["governance"]["authority_attestation"] = False
        self.assert_rejected(
            evidence,
            "governance shall contain an express manual authority attestation",
            "closure",
        )

    def test_candidate_and_post_merge_command_sets_are_exact(self) -> None:
        for phase, container, mutation, diagnostic in (
            (
                "closure",
                "candidate_commands",
                "missing",
                "candidate commands shall contain each required command exactly once",
            ),
            (
                "closure",
                "candidate_commands",
                "duplicate",
                "candidate commands shall contain each required command exactly once",
            ),
            (
                "closure",
                "candidate_commands",
                "extra",
                "candidate commands shall contain each required command exactly once",
            ),
            (
                "taggable",
                "post_merge",
                "missing",
                "post-merge commands shall contain each required command exactly once",
            ),
        ):
            with self.subTest(phase=phase, mutation=mutation):
                evidence = (
                    taggable_evidence() if phase == "taggable" else closure_evidence()
                )
                commands = (
                    evidence[container]["commands"]
                    if container == "post_merge"
                    else evidence[container]
                )
                if mutation == "missing":
                    commands.pop()
                elif mutation == "duplicate":
                    commands.append(deepcopy(commands[0]))
                else:
                    commands[-1]["name"] = "untrusted"
                self.assert_rejected(evidence, diagnostic, phase)

    def test_commands_reject_failure_or_wrong_sha(self) -> None:
        for phase, command_path, field, value, diagnostic in (
            (
                "closure",
                "candidate",
                "exit_code",
                1,
                "full_suite candidate command shall succeed",
            ),
            (
                "closure",
                "candidate",
                "sha",
                "a" * 40,
                "full_suite candidate command shall be bound to closure head",
            ),
            (
                "taggable",
                "post_merge",
                "exit_code",
                1,
                "full_suite post-merge command shall succeed",
            ),
        ):
            with self.subTest(phase=phase, field=field):
                evidence = (
                    taggable_evidence() if phase == "taggable" else closure_evidence()
                )
                commands = (
                    evidence["post_merge"]["commands"]
                    if command_path == "post_merge"
                    else evidence["candidate_commands"]
                )
                commands[0][field] = value
                self.assert_rejected(evidence, diagnostic, phase)

    def test_taggable_accepts_exact_task8_post_merge_results_shape(self) -> None:
        evidence = taggable_evidence()
        evidence["post_merge"] = {
            "schema": "esaf-v05-post-merge-results-v1",
            "sha": MERGE_SHA,
            "tree": CLOSURE_TREE,
            "commands": [
                {"name": "full_suite", "exit_code": 0, "result": "passed"},
                {"name": "assessment", "exit_code": 0, "result": "passed"},
                {"name": "profiles", "exit_code": 0, "result": "passed"},
                {"name": "controls", "exit_code": 0, "result": "passed"},
                {"name": "architectures", "exit_code": 0, "result": "passed"},
                {"name": "migration", "exit_code": 0, "result": "passed"},
                {"name": "crosswalk_current", "exit_code": 0, "result": "passed"},
                {"name": "crosswalk_baseline", "exit_code": 0, "result": "passed"},
                {"name": "pci_readiness", "exit_code": 0, "result": "passed"},
                {"name": "links", "exit_code": 0, "result": "passed"},
                {"name": "release_v04", "exit_code": 0, "result": "passed"},
                {"name": "release_v05", "exit_code": 0, "result": "passed"},
                {"name": "mermaid_inventory", "exit_code": 0, "result": "passed"},
                {
                    "name": "mermaid_rendering",
                    "exit_code": 0,
                    "result": {
                        "rendered_blocks": 23,
                        "renderer": "@mermaid-js/mermaid-cli@11.16.0",
                        "visual_review": "approved",
                        "candidate_inventory_equal": True,
                        "merge_tree_equal": True,
                        "candidate_review_url": (
                            "https://github.com/tdistress/ESAF/issues/59"
                            "#issuecomment-14"
                        ),
                        "candidate_reviewer": "candidate rendering reviewer",
                        "post_merge_reviewer": "post-merge rendering reviewer",
                        "reviewed_at": "2026-07-27T12:05:00Z",
                    },
                },
                {"name": "whole_range_diff", "exit_code": 0, "result": "passed"},
                {
                    "name": "cache_count",
                    "exit_code": 0,
                    "result": "0 __pycache__ directories",
                },
                {"name": "clean_status", "exit_code": 0, "result": "clean"},
            ],
        }
        owner_record = record_fixture("closure_candidate")
        owner_record["mapping_decision_basis"] = "owner_risk_acceptance"
        self.assertEqual(
            [],
            validate_external_evidence(
                ROOT,
                owner_record,
                evidence,
                MERGE_SHA,
                "taggable",
                FIXED_NOW,
            ),
        )

    def test_closure_mermaid_requires_candidate_review_only(self) -> None:
        evidence = closure_evidence()
        command = next(
            item
            for item in evidence["candidate_commands"]
            if item["name"] == "mermaid_rendering"
        )
        self.assertNotIn("post_merge_reviewer", command["result"])
        self.assertNotIn("merge_tree_equal", command["result"])
        owner_record = record_fixture("closure_candidate")
        owner_record["mapping_decision_basis"] = "owner_risk_acceptance"
        self.assertEqual(
            [],
            validate_external_evidence(
                ROOT,
                owner_record,
                evidence,
                CLOSURE_SHA,
                "closure",
                FIXED_NOW,
            ),
        )

    def test_taggable_mermaid_requires_postmerge_review_and_tree_equality(
        self,
    ) -> None:
        for field in ("post_merge_reviewer", "merge_tree_equal"):
            with self.subTest(field=field):
                evidence = taggable_evidence()
                command = next(
                    item
                    for item in evidence["post_merge"]["commands"]
                    if item["name"] == "mermaid_rendering"
                )
                command["result"].pop(field)
                self.assert_rejected(
                    evidence,
                    "mermaid_rendering result shall be a structured visual review",
                    "taggable",
                )

    def test_mermaid_rendering_result_is_structured_and_exact(self) -> None:
        cases = (
            (
                "plain result",
                lambda result: "passed",
                "mermaid_rendering result shall be a structured visual review",
            ),
            (
                "reviewer",
                lambda result: {**result, "post_merge_reviewer": " "},
                "mermaid_rendering reviewer identities shall be named",
            ),
            (
                "URL",
                lambda result: {**result, "candidate_review_url": "http://example.test"},
                "mermaid_rendering candidate review URL shall use HTTPS",
            ),
            (
                "inventory equality",
                lambda result: {**result, "candidate_inventory_equal": False},
                "mermaid_rendering equality flags shall be true",
            ),
            (
                "tree equality",
                lambda result: {**result, "merge_tree_equal": False},
                "mermaid_rendering equality flags shall be true",
            ),
            (
                "renderer",
                lambda result: {**result, "renderer": "mermaid-cli@latest"},
                "mermaid_rendering renderer is invalid",
            ),
            (
                "count",
                lambda result: {**result, "rendered_blocks": 22},
                "mermaid_rendering shall cover exactly 23 blocks",
            ),
        )
        for name, mutate, diagnostic in cases:
            with self.subTest(name=name):
                evidence = taggable_evidence()
                command = next(
                    item
                    for item in evidence["post_merge"]["commands"]
                    if item["name"] == "mermaid_rendering"
                )
                command["result"] = mutate(command["result"])
                self.assert_rejected(evidence, diagnostic, "taggable")

    def test_github_check_and_merge_state_are_exact(self) -> None:
        cases = (
            (
                lambda value: value["github_checks"]["observed"][0].__setitem__(
                    "conclusion", "pending"
                ),
                "GitHub check shall be successful",
            ),
            (
                lambda value: value["github_checks"]["observed"][0].__setitem__(
                    "sha", "a" * 40
                ),
                "GitHub check shall be bound to closure head",
            ),
            (
                lambda value: value["merge_state"].__setitem__("state", "blocked"),
                "merge state shall be clean",
            ),
            (
                lambda value: value["merge_state"].__setitem__("sha", "a" * 40),
                "merge state shall be bound to closure head",
            ),
        )
        for mutate, diagnostic in cases:
            with self.subTest(diagnostic=diagnostic):
                evidence = closure_evidence()
                mutate(evidence)
                self.assert_rejected(evidence, diagnostic, "closure")

    def test_taggable_rejects_merge_head_equal_to_closure_head(self) -> None:
        evidence = taggable_evidence()
        evidence["merge_head"] = CLOSURE_SHA
        evidence["post_merge"]["sha"] = CLOSURE_SHA
        self.assert_rejected(
            evidence,
            "merge head shall differ from closure head",
            "taggable",
        )

    def test_owner_risk_scope_requires_authenticated_owner_source(self) -> None:
        for field, value in (
            ("author_association", "COLLABORATOR"),
            ("author_login", "other"),
        ):
            with self.subTest(field=field):
                evidence = closure_evidence()
                evidence["scope"]["source"][field] = value
                self.assert_rejected(
                    evidence,
                    "scope approval shall use its authenticated OWNER source",
                    "closure",
                )

    def test_governance_approver_matches_authenticated_source(self) -> None:
        evidence = closure_evidence()
        evidence["governance"]["reviewer"] = "different-approver"
        self.assert_rejected(
            evidence,
            "governance approver shall match its authenticated source author",
            "closure",
        )

    def test_governance_source_is_distinct_from_owner_scope_source(self) -> None:
        evidence = closure_evidence()
        evidence["governance"]["source"] = deepcopy(evidence["scope"]["source"])
        evidence["governance"]["reviewer"] = "tdistress"
        evidence["governance"]["url"] = evidence["scope"]["url"]
        self.assert_rejected(
            evidence,
            "governance source shall be distinct from owner and scope source",
            "closure",
        )

    def test_source_path_comment_id_url_and_acquisition_id_are_consistent(
        self,
    ) -> None:
        cases = (
            (
                "resource path",
                lambda source: source.__setitem__(
                    "resource_path",
                    "repos/tdistress/ESAF/issues/comments/999",
                ),
            ),
            (
                "comment URL",
                lambda source: source.__setitem__(
                    "comment_url",
                    "https://github.com/tdistress/ESAF/issues/59"
                    "#issuecomment-999",
                ),
            ),
            (
                "acquisition resource",
                lambda source: source.__setitem__(
                    "acquisition_resource_id",
                    "repos/tdistress/ESAF/issues/comments/999",
                ),
            ),
        )
        for name, mutate in cases:
            with self.subTest(name=name):
                evidence = closure_evidence()
                mutate(evidence["technical"]["source"])
                self.assert_rejected(
                    evidence,
                    "technical source identity is inconsistent",
                    "closure",
                )

    def test_source_comment_url_matches_sourced_verdict_url(self) -> None:
        evidence = closure_evidence()
        evidence["technical"]["url"] = (
            "https://github.com/tdistress/ESAF/issues/55#issuecomment-12"
        )
        self.assert_rejected(
            evidence,
            "technical verdict URL shall equal source comment URL",
            "closure",
        )

    def test_sourced_verdict_requires_exact_calendar_date(self) -> None:
        for invalid in ("20260727", "2026-W31-1", "2026-7-27"):
            with self.subTest(invalid=invalid):
                evidence = closure_evidence()
                evidence["technical"]["date"] = invalid
                self.assert_rejected(
                    evidence,
                    "technical verdict date shall be YYYY-MM-DD",
                    "closure",
                )

    def test_source_comment_url_matches_canonical_url_from_acquired_response(
        self,
    ) -> None:
        evidence = closure_evidence()
        alternate = (
            "https://github.com/tdistress/ESAF/issues/55#issuecomment-12"
        )
        evidence["technical"]["source"]["comment_url"] = alternate
        evidence["technical"]["url"] = alternate
        self.assert_rejected(
            evidence,
            "technical source canonical URL shall equal acquired response",
            "closure",
        )

    def test_nested_evidence_objects_reject_unknown_keys(self) -> None:
        cases = (
            (
                "candidate command",
                "closure",
                lambda value: value["candidate_commands"][0].__setitem__(
                    "untrusted", True
                ),
                "candidate command keys are invalid",
            ),
            (
                "owner decision",
                "closure",
                lambda value: value["mapping_decisions"][0].__setitem__(
                    "untrusted", True
                ),
                "owner-risk decision keys are invalid",
            ),
            (
                "owner missing role",
                "closure",
                lambda value: value["mapping_decisions"][0][
                    "missing_qualified_roles"
                ][0].__setitem__("untrusted", True),
                "owner-risk missing-role keys are invalid",
            ),
            (
                "GitHub checks",
                "closure",
                lambda value: value["github_checks"].__setitem__(
                    "untrusted", True
                ),
                "GitHub checks keys are invalid",
            ),
            (
                "GitHub check",
                "closure",
                lambda value: value["github_checks"]["observed"][0].__setitem__(
                    "untrusted", True
                ),
                "GitHub check keys are invalid",
            ),
            (
                "merge state",
                "closure",
                lambda value: value["merge_state"].__setitem__(
                    "untrusted", True
                ),
                "merge state keys are invalid",
            ),
            (
                "post-merge evidence",
                "taggable",
                lambda value: value["post_merge"].__setitem__(
                    "untrusted", True
                ),
                "post-merge evidence keys are invalid",
            ),
            (
                "post-merge command",
                "taggable",
                lambda value: value["post_merge"]["commands"][0].__setitem__(
                    "untrusted", True
                ),
                "post-merge command keys are invalid",
            ),
        )
        for name, phase, mutate, diagnostic in cases:
            with self.subTest(name=name):
                evidence = (
                    taggable_evidence() if phase == "taggable" else closure_evidence()
                )
                mutate(evidence)
                self.assert_rejected(evidence, diagnostic, phase)

    def test_owner_risk_basis_is_uniform_and_complete(self) -> None:
        cases = (
            (
                lambda value: value["mapping_decisions"][0].__setitem__(
                    "mapping_decision_basis", "qualified_approval"
                ),
                "mapping decisions shall use one uniform basis",
            ),
            (
                lambda value: value["mapping_decisions"][0].__setitem__(
                    "mapping_set_id", "wrong"
                ),
                "owner-risk decisions shall contain each mapping set exactly once",
            ),
            (
                lambda value: value["mapping_decisions"].pop(),
                "owner-risk evidence shall contain exactly three decisions",
            ),
            (
                lambda value: value["mapping_decisions"].append(
                    deepcopy(value["mapping_decisions"][0])
                ),
                "owner-risk evidence shall contain exactly three decisions",
            ),
            (
                lambda value: value["mapping_decisions"][1]["source"].__setitem__(
                    "body_sha256", "f" * 64
                ),
                "owner-risk decisions shall use one unchanged source",
            ),
        )
        for mutate, diagnostic in cases:
            with self.subTest(diagnostic=diagnostic):
                evidence = closure_evidence()
                mutate(evidence)
                self.assert_rejected(evidence, diagnostic, "closure")

    def test_owner_risk_decision_requires_an_acquired_source_body_digest(self) -> None:
        evidence = closure_evidence()
        for decision in evidence["mapping_decisions"]:
            decision["source"].pop("body_sha256")
        self.assert_rejected(
            evidence, "owner-risk source keys are invalid", "closure"
        )

    def test_owner_risk_decision_requires_six_roles_and_working_draft_limits(
        self,
    ) -> None:
        cases = (
            (
                lambda decision: decision["missing_qualified_roles"].pop(),
                "owner-risk decision shall contain exactly six missing roles",
            ),
            (
                lambda decision: decision["missing_qualified_roles"].append(
                    deepcopy(decision["missing_qualified_roles"][0])
                ),
                "owner-risk decision shall contain exactly six missing roles",
            ),
            (
                lambda decision: decision.__setitem__("accountable_owner", "other"),
                "owner-risk accountable owner shall match authenticated author",
            ),
            (
                lambda decision: decision.__setitem__("issue_55_status", "closed"),
                "owner-risk decision shall leave issue 55 open",
            ),
            (
                lambda decision: decision["reentry_triggers"].pop(),
                "owner-risk re-entry triggers shall equal the required set",
            ),
            (
                lambda decision: decision.__setitem__("lifecycle", "reviewed"),
                "owner-risk decision lifecycle shall remain draft",
            ),
            (
                lambda decision: decision["claims_not_made"].pop(),
                "owner-risk nonclaims shall equal the required set",
            ),
        )
        for mutate, diagnostic in cases:
            with self.subTest(diagnostic=diagnostic):
                evidence = closure_evidence()
                mutate(evidence["mapping_decisions"][0])
                self.assert_rejected(evidence, diagnostic, "closure")

    def test_qualified_manifest_must_pass_tracked_official_schema(self) -> None:
        evidence = self.official_qualified_evidence()
        self.assertEqual(
            [],
            validate_external_evidence(
                ROOT,
                record_fixture("closure_candidate"),
                evidence,
                self.qualified_candidate,
                "closure",
                FIXED_NOW,
            ),
        )
        campaign_root, _archive_path, _seal_path = (
            self.official_qualified_paths(evidence)
        )
        manifest_path = campaign_root / "REVIEW_EVIDENCE.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["untrusted"] = True
        manifest_path.write_bytes(official_canonical_json_bytes(manifest))
        self.reseal_official_campaign(evidence)
        self.assertIn(
            "qualified campaign shall pass the tracked official validator",
            validate_external_evidence(
                ROOT,
                record_fixture("closure_candidate"),
                evidence,
                self.qualified_candidate,
                "closure",
                FIXED_NOW,
            ),
        )

    def test_qualified_campaign_must_be_verified_by_official_validator(
        self,
    ) -> None:
        evidence = self.official_qualified_evidence()
        campaign_root, _archive_path, _seal_path = (
            self.official_qualified_paths(evidence)
        )
        manifest = json.loads(
            (campaign_root / "REVIEW_EVIDENCE.json").read_bytes()
        )
        attestation_path = manifest["mapping_sets"][0]["roles"][0][
            "attestation"
        ]["path"]
        (campaign_root / attestation_path).write_bytes(b"forged attestation\n")
        self.reseal_official_campaign(evidence)
        self.assertIn(
            "qualified campaign shall pass the tracked official validator",
            validate_external_evidence(
                ROOT,
                record_fixture("closure_candidate"),
                evidence,
                self.qualified_candidate,
                "closure",
                FIXED_NOW,
            ),
        )

    def test_qualified_seal_requires_retained_archive_and_exact_bytes(
        self,
    ) -> None:
        evidence = self.official_qualified_evidence()
        _campaign_root, archive_path, _seal_path = (
            self.official_qualified_paths(evidence)
        )
        archive_path.write_bytes(archive_path.read_bytes() + b"forged")
        self.assertIn(
            "qualified retained archive and seal shall match exact campaign bytes",
            validate_external_evidence(
                ROOT,
                record_fixture("closure_candidate"),
                evidence,
                self.qualified_candidate,
                "closure",
                FIXED_NOW,
            ),
        )

        escaped_evidence = self.official_qualified_evidence()
        escaped_evidence["mapping_decisions"][0]["archive_path"] = (
            "../outside.zip"
        )
        self.assertIn(
            "qualified retained evidence locators shall remain within one external root",
            validate_external_evidence(
                ROOT,
                record_fixture("closure_candidate"),
                escaped_evidence,
                self.qualified_candidate,
                "closure",
                FIXED_NOW,
            ),
        )

        seal_evidence = self.official_qualified_evidence()
        _campaign_root, _archive_path, seal_path = (
            self.official_qualified_paths(seal_evidence)
        )
        seal_record = json.loads(seal_path.read_bytes())
        seal_record["untrusted"] = True
        seal_path.write_bytes(official_canonical_json_bytes(seal_record))
        self.assertIn(
            "qualified retained archive and seal shall match exact campaign bytes",
            validate_external_evidence(
                ROOT,
                record_fixture("closure_candidate"),
                seal_evidence,
                self.qualified_candidate,
                "closure",
                FIXED_NOW,
            ),
        )

    def test_qualified_campaign_rejects_accepted_critical_or_important_findings(
        self,
    ) -> None:
        for severity in ("Critical", "Important"):
            with self.subTest(severity=severity):
                evidence = self.official_qualified_evidence()

                def accept_high_severity(role: dict[str, object]) -> None:
                    worksheet = role["worksheet"]
                    worksheet["findings_disposition"] = "Accepted finding"
                    worksheet["findings"] = [
                        {
                            "finding_id": f"release-{severity.lower()}",
                            "affected_record_ids": [
                                self.qualified_affected_record_id
                            ],
                            "severity": severity,
                            "status": "accepted",
                            "disposition": "Accepted risk",
                            "resolver_or_acceptor": "ESAF Project Owner",
                            "disposition_date": "2026-07-27",
                            "acceptance_rationale": (
                                "Accepted only to exercise the release gate."
                            ),
                        }
                    ]

                self.rewrite_official_role(evidence, accept_high_severity)
                self.reseal_official_campaign(evidence)
                self.assertIn(
                    "qualified campaign shall pass the tracked official validator",
                    validate_external_evidence(
                        ROOT,
                        record_fixture("closure_candidate"),
                        evidence,
                        self.qualified_candidate,
                        "closure",
                        FIXED_NOW,
                    ),
                )

    def test_qualified_basis_rejects_synthetic_approval_decisions(self) -> None:
        evidence = closure_evidence()
        evidence["mapping_decision_schema"] = QUALIFIED_SCHEMA
        evidence["mapping_decision_basis"] = "qualified_approval"
        evidence["mapping_decisions"] = [
            {
                "mapping_set_id": mapping_set_id,
                "disposition": "approved",
                "sha": CLOSURE_SHA,
            }
            for mapping_set_id in MAPPING_SETS
        ]
        self.assert_rejected(
            evidence,
            "qualified approval requires a valid exact-candidate six-role Draft campaign",
            "closure",
        )

    def test_external_evidence_rejects_nonclosure_record_phases(self) -> None:
        for record_phase in ("evidence_candidate", "published"):
            with self.subTest(record_phase=record_phase):
                self.assertIn(
                    "external evidence requires a closure_candidate record",
                    validate_external_evidence(
                        ROOT,
                        record_fixture(record_phase),
                        closure_evidence(),
                        CLOSURE_SHA,
                        "closure",
                        FIXED_NOW,
                    ),
                )

    def test_cli_requires_all_external_evidence_arguments_together(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in (
                "controls/catalog.json",
                "architectures/patterns",
                "crosswalks",
                "assessment/ESAF-1500.md",
                "profiles/uk/0.1.0/profile.json",
                "docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json",
            ):
                source = ROOT / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    shutil.copy2(source, target)
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "---\n"
                + json.dumps(record_fixture("evidence_candidate"))
                + "\n---\n",
                encoding="utf-8",
            )
            (root / "tools").mkdir()
            shutil.copy2(
                ROOT / "tools/v05_beta_release_gates.py",
                root / "tools/v05_beta_release_gates.py",
            )
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "core.autocrlf=false", "add", "."],
                cwd=root,
                check=True,
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/v05_beta_release_gates.py",
                    "--check",
                    "--external-evidence",
                    "missing.json",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn(
                "external-evidence, expected-head, and phase shall be supplied together",
                result.stdout,
            )

    def test_closure_base_is_exact_distinct_sha(self) -> None:
        for phase, fixture in (
            ("closure", closure_evidence),
            ("taggable", taggable_evidence),
        ):
            evidence = fixture()
            record = record_fixture("closure_candidate")
            record["mapping_decision_basis"] = "owner_risk_acceptance"
            self.assertNotIn(
                "closure base shall be a distinct 40-character SHA",
                validate_external_evidence(
                    ROOT,
                    record,
                    evidence,
                    CLOSURE_SHA if phase == "closure" else MERGE_SHA,
                    phase,
                    FIXED_NOW,
                ),
            )
            for invalid in ("not-a-sha", CLOSURE_SHA):
                with self.subTest(phase=phase, invalid=invalid):
                    changed = deepcopy(evidence)
                    changed["closure_base"] = invalid
                    self.assert_rejected(
                        changed,
                        "closure base shall be a distinct 40-character SHA",
                        phase,
                    )


class V05ReleaseRecordTests(unittest.TestCase):
    def test_v05_readiness_record_matches_its_phase(self) -> None:
        record = load_front_matter(V05_RECORD)
        self.assertIn(
            record["phase"],
            {"evidence_candidate", "closure_candidate", "published"},
        )
        self.assertEqual(
            PHASE_GATE_STATES[record["phase"]],
            {
                gate: value["state"]
                for gate, value in record["gates"].items()
            },
        )
        self.assertEqual([], validate_record(ROOT, record))

    def test_closure_candidate_fixture_uses_exact_gate_matrix(self) -> None:
        record = record_fixture("closure_candidate")
        self.assertEqual([], validate_record(ROOT, record))
        self.assertEqual("open", record["gates"]["post_merge"]["state"])

    def test_closure_allowlist_is_exact(self) -> None:
        self.assertEqual(
            EXPECTED_CLOSURE_ALLOWLIST,
            set(v05_beta_release_gates.CLOSURE_ALLOWLIST),
        )

    def test_readiness_loader_rejects_duplicate_yaml_keys(self) -> None:
        source = V05_RECORD.read_text(encoding="utf-8")
        mutations = (
            source.replace(
                "phase: evidence_candidate",
                "phase: evidence_candidate\nphase: published",
                1,
            ),
            source.replace(
                "  controls: 91",
                "  controls: 91\n  controls: 92",
                1,
            ),
            source.replace(
                "  scope: {state: open, evidence: []}",
                (
                    "  scope: {state: open, evidence: []}\n"
                    "  scope: {state: closed, evidence: []}"
                ),
                1,
            ),
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "readiness.md"
            for index, mutation in enumerate(mutations):
                with self.subTest(index=index):
                    path.write_text(mutation, encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "duplicate YAML key"):
                        load_front_matter(path)

    def test_readiness_body_rejects_publication_or_approval_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._prepare_cli_root(root)
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                readiness_document(record_fixture("evidence_candidate")),
                encoding="utf-8",
            )
            self._initialize_repository(root)
            canonical = subprocess.run(
                [
                    sys.executable,
                    "tools/v05_beta_release_gates.py",
                    "--check",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, canonical.returncode, canonical.stdout)

            mutations = (
                CANONICAL_READINESS_BODY.replace(
                    "This\nrecord does not approve publication.",
                    "This record approves publication.",
                    1,
                ),
                (
                    CANONICAL_READINESS_BODY
                    + "\nQualified review is complete and the mappings are approved.\n"
                ),
            )
            for body in mutations:
                with self.subTest(body=body[-90:]):
                    record_path.write_text(
                        readiness_document(
                            record_fixture("evidence_candidate"),
                            body,
                        ),
                        encoding="utf-8",
                    )
                    result = subprocess.run(
                        [
                            sys.executable,
                            "tools/v05_beta_release_gates.py",
                            "--check",
                        ],
                        cwd=root,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(1, result.returncode)
                    self.assertIn("readiness body", result.stdout)

    def test_cli_accepts_event_baseline_for_evidence_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._prepare_cli_root(root)
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                readiness_document(record_fixture("evidence_candidate")),
                encoding="utf-8",
            )
            self._initialize_repository(root, commit=True)
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/v05_beta_release_gates.py",
                    "--check",
                    "--baseline-ref",
                    "HEAD",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stdout)

    def test_cli_rejects_closure_candidate_when_range_exceeds_exact_allowlist(
        self,
    ) -> None:
        for name, changes in (
            ("extra", {*EXPECTED_CLOSURE_ALLOWLIST, "unexpected.md"}),
            (
                "missing",
                EXPECTED_CLOSURE_ALLOWLIST - {"ROADMAP.md"},
            ),
        ):
            with self.subTest(name=name):
                result = self._run_closure_candidate(changes)
                self.assertEqual(1, result.returncode)
                self.assertIn(
                    "closure candidate changed paths shall equal the exact allowlist",
                    result.stdout,
                )

    def test_cli_accepts_closure_candidate_with_exact_allowlist(self) -> None:
        result = self._run_closure_candidate(EXPECTED_CLOSURE_ALLOWLIST)
        self.assertEqual(0, result.returncode, result.stdout)

    def test_uk_mapping_sets_and_records_remain_unreviewed_drafts(self) -> None:
        catalog = json.loads(
            (ROOT / "crosswalks/catalog.json").read_text(encoding="utf-8")
        )
        mapping_sets = catalog["mapping_sets"]
        self.assertEqual(3, len(mapping_sets))
        self.assertEqual(set(MAPPING_SETS), {
            item["metadata"]["mapping_set_id"]
            for item in mapping_sets
        })
        provision_count = 0
        for mapping_set in mapping_sets:
            with self.subTest(mapping_set=mapping_set["path"]):
                self.assertEqual("draft", mapping_set["metadata"]["status"])
                registry = load_front_matter(
                    ROOT
                    / "crosswalks/registry"
                    / f"{mapping_set['metadata']['mapping_set_id']}.md"
                )
                self.assertEqual([], registry["events"])
                self.assertNotIn("reviewer", registry)
                self.assertNotIn("approver", registry)
                self.assertNotIn("approval", registry)
                for provision in mapping_set["provisions"]:
                    provision_count += 1
                    record = load_front_matter(ROOT / provision["path"])
                    self.assertEqual("draft", record["status"])
                    self.assertNotIn("reviewer", record)
                    self.assertNotIn("approver", record)
                    self.assertNotIn("approval", record)
        self.assertEqual(404, provision_count)

    def test_v04_published_validator_remains_green(self) -> None:
        historical = load_v04_front_matter(V04_RECORD)
        self.assertEqual([], validate_v04_record(ROOT, historical))

    def test_v05_record_requires_fixed_release_identity(self) -> None:
        record = record_fixture("evidence_candidate")
        for field, value, diagnostic in (
            ("release", "0.4-alpha", "release shall equal 0.5-beta"),
            ("tag", "v0.4-alpha", "tag shall equal v0.5-beta"),
            ("issue", 39, "issue shall equal 59"),
        ):
            with self.subTest(field=field):
                candidate = deepcopy(record)
                candidate[field] = value
                self.assertIn(diagnostic, validate_record(ROOT, candidate))

    def test_phase_gate_state_matrix_is_exact(self) -> None:
        for phase, expected in PHASE_GATE_STATES.items():
            with self.subTest(phase=phase):
                record = record_fixture(phase)
                observed = {
                    gate: value["state"]
                    for gate, value in record["gates"].items()
                }
                self.assertEqual(expected, observed)
                self.assertEqual([], validate_record(ROOT, record))

    def test_scope_counts_are_derived_from_repository(self) -> None:
        self.assertEqual(EXPECTED_SCOPE, derive_scope(ROOT))

    def test_transition_rejects_published_to_candidate(self) -> None:
        previous = record_fixture("published")
        candidate = record_fixture("closure_candidate")
        self.assertIn(
            "published record shall not transition to a candidate phase",
            validate_transition(previous, candidate),
        )

    def test_transition_requires_a_v05_evidence_baseline_for_closure(self) -> None:
        candidate = record_fixture("closure_candidate")
        mutations = (
            (
                "wrong release",
                lambda value: value.update(release="0.4-alpha"),
                "baseline release shall equal 0.5-beta",
            ),
            (
                "wrong repository scope",
                lambda value: value.update(repository_scope="partial"),
                "baseline repository scope shall equal complete_git_tracked_repository",
            ),
            (
                "skipped evidence phase",
                lambda value: value.update(phase="closure_candidate"),
                "closure_candidate shall transition only from evidence_candidate",
            ),
            (
                "phase regression",
                lambda value: value.update(phase="published"),
                "closure_candidate shall transition only from evidence_candidate",
            ),
        )
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                previous = record_fixture("evidence_candidate")
                mutate(previous)
                self.assertIn(diagnostic, validate_transition(previous, candidate))

    def test_transition_requires_a_closure_baseline_for_publication(self) -> None:
        self.assertIn(
            "published shall transition only from closure_candidate",
            validate_transition(
                record_fixture("evidence_candidate"), record_fixture("published")
            ),
        )

    def test_transition_rejects_any_predecessor_for_evidence_candidate(self) -> None:
        for phase in ("closure_candidate", "published"):
            with self.subTest(phase=phase):
                self.assertIn(
                    "evidence_candidate shall not have a predecessor",
                    validate_transition(
                        record_fixture(phase), record_fixture("evidence_candidate")
                    ),
                )

    def test_contract_rejects_each_wrong_phase_gate_state(self) -> None:
        for phase, gates in PHASE_GATE_STATES.items():
            for gate, expected in gates.items():
                for wrong_state in {"open", "in_review", "ready", "closed"} - {expected}:
                    with self.subTest(phase=phase, gate=gate, wrong_state=wrong_state):
                        record = record_fixture(phase)
                        record["gates"][gate]["state"] = wrong_state
                        self.assertIn(
                            f"{phase} phase shall set {gate} gate to {expected}",
                            validate_record(ROOT, record),
                        )

    def test_contract_rejects_each_invalid_record_mutation(self) -> None:
        record = record_fixture("closure_candidate")
        mutations = (
            (
                "wrong phase state",
                lambda value: value["gates"]["scope"].update(state="open"),
                "closure_candidate phase shall set scope gate to ready",
            ),
            (
                "missing mapping set",
                lambda value: value.update(mapping_sets=value["mapping_sets"][:-1]),
                "mapping_sets shall equal the tracked catalog mapping sets",
            ),
            (
                "duplicate mapping set",
                lambda value: value.update(mapping_sets=[*value["mapping_sets"], value["mapping_sets"][0]]),
                "mapping_sets shall not contain duplicates",
            ),
            (
                "unsupported decision basis",
                lambda value: value.update(mapping_decision_basis="unreviewed"),
                "mapping_decision_basis shall be supported",
            ),
            (
                "stale scope count",
                lambda value: value["scope"].update(controls=90),
                "scope shall equal the derived repository scope",
            ),
            (
                "missing assessment foundation",
                lambda value: value["scope"].update(assessment_foundation=False),
                "scope shall equal the derived repository scope",
            ),
            (
                "wrong profile count",
                lambda value: value["scope"].update(draft_profiles=2),
                "scope shall equal the derived repository scope",
            ),
            (
                "non-HOLD PCI disposition",
                lambda value: value["scope"].update(pci_dss_disposition="GO"),
                "scope shall equal the derived repository scope",
            ),
            (
                "non-HTTPS evidence",
                lambda value: value["gates"]["scope"].update(evidence=["http://example.test/scope"]),
                "scope: evidence shall use HTTPS locators",
            ),
            (
                "candidate SHA field",
                lambda value: value.update(validated_sha="a" * 40),
                "candidate phases shall not contain SHA fields",
            ),
            (
                "unknown top-level field",
                lambda value: value.update(unexpected=True),
                "unknown top-level key unexpected",
            ),
            (
                "unknown gate",
                lambda value: value["gates"].update(unexpected={"state": "ready", "evidence": ["https://example.test/unexpected"]}),
                "unknown gate unexpected",
            ),
        )
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                candidate = deepcopy(record)
                mutate(candidate)
                self.assertIn(diagnostic, validate_record(ROOT, candidate))

    def test_contract_rejects_scope_input_overrides(self) -> None:
        for scope_inputs in ([], ["controls/catalog.json"]):
            with self.subTest(scope_inputs=scope_inputs):
                record = record_fixture("evidence_candidate")
                record["scope_inputs"] = scope_inputs
                self.assertIn(
                    "scope_inputs shall not override fixed authoritative scope inputs",
                    validate_record(ROOT, record),
                )

    def test_contract_rejects_unknown_nested_fields_and_nested_sha_keys(self) -> None:
        mutations = (
            (
                "publication field",
                lambda value: value["publication"].update(unexpected=True),
                "unknown publication key unexpected",
            ),
            (
                "gate field",
                lambda value: value["gates"]["scope"].update(unexpected=True),
                "scope: unknown gate key unexpected",
            ),
            (
                "nested SHA field",
                lambda value: value["publication"].update(commit_sha={}),
                "candidate phases shall not contain SHA fields",
            ),
        )
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                record = record_fixture("evidence_candidate")
                mutate(record)
                self.assertIn(diagnostic, validate_record(ROOT, record))

    def test_contract_enforces_publication_date_lifecycle(self) -> None:
        candidate = record_fixture("closure_candidate")
        candidate["publication"]["date"] = "2026-07-27"
        self.assertIn(
            "candidate publication date shall be null",
            validate_record(ROOT, candidate),
        )
        published = record_fixture("published")
        published["publication"]["date"] = None
        self.assertIn(
            "published publication date shall be an ISO date",
            validate_record(ROOT, published),
        )

    def test_contract_rejects_non_draft_mapping_catalog_entries(self) -> None:
        for mutation in ("catalog entry", "mapping record"):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    catalog_path = root / "crosswalks/catalog.json"
                    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
                    relative_record = catalog["mapping_sets"][0]["provisions"][0]["path"]
                    if mutation == "mapping record":
                        record_path = root / relative_record
                        record_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(ROOT / relative_record, record_path)
                    self._initialize_repository(root)
                    if mutation == "catalog entry":
                        catalog["mapping_sets"][0]["metadata"]["status"] = "published"
                        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
                    else:
                        record_path = root / relative_record
                        text = record_path.read_text(encoding="utf-8")
                        if text.lstrip().startswith("{"):
                            record = json.loads(text)
                            record["status"] = "published"
                            record_path.write_text(json.dumps(record), encoding="utf-8")
                        else:
                            record_path.write_text(
                                text.replace('"status":"draft"', '"status":"published"', 1)
                                if '"status":"draft"' in text
                                else text.replace("status: draft", "status: published", 1),
                                encoding="utf-8",
                            )
                    self.assertIn(
                        "tracked mapping sets shall remain draft",
                        validate_record(root, record_fixture("evidence_candidate")),
                    )

    def test_contract_requires_catalog_mapping_sources_to_exist_and_be_tracked(self) -> None:
        for mutation, diagnostic in (
            ("missing", "catalog-declared mapping source is missing"),
            ("untracked", "catalog-declared mapping source shall be Git-tracked"),
        ):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    catalog = json.loads((root / "crosswalks/catalog.json").read_text())
                    relative = catalog["mapping_sets"][0]["provisions"][0]["path"]
                    self._initialize_repository(root)
                    if mutation == "untracked":
                        target = root / relative
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(ROOT / relative, target)
                    self.assertIn(
                        diagnostic,
                        validate_record(root, record_fixture("evidence_candidate")),
                    )

    def test_contract_rejects_untracked_pattern_and_profile_scope_files(self) -> None:
        for relative, source in (
            ("architectures/patterns/ARC-P999.md", "architectures/patterns/ARC-P100.md"),
            ("profiles/example/0.1.0/profile.json", "profiles/uk/0.1.0/profile.json"),
        ):
            with self.subTest(relative=relative):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    self._initialize_repository(root)
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / source, target)
                    self.assertIn(
                        "scope inputs shall not contain untracked files",
                        validate_record(root, record_fixture("evidence_candidate")),
                    )

    def test_contract_returns_diagnostic_for_malformed_crosswalk_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            self._initialize_repository(root)
            (root / "crosswalks/catalog.json").write_text("{", encoding="utf-8")
            self.assertIn(
                "crosswalk catalog cannot be parsed",
                validate_record(root, record_fixture("evidence_candidate")),
            )

    def test_contract_rejects_untracked_scope_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            self._initialize_repository(root)
            shutil.copy2(
                ROOT / "architectures/patterns/ARC-P100.md",
                root / "architectures/patterns/ARC-P999.md",
            )
            self.assertIn(
                "scope inputs shall not contain untracked files",
                validate_record(root, record_fixture("evidence_candidate")),
            )

    def test_cli_requires_baseline_for_closure_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "---\n" + json.dumps(record_fixture("closure_candidate")) + "\n---\n",
                encoding="utf-8",
            )
            (root / "tools").mkdir()
            shutil.copy2(ROOT / "tools/v05_beta_release_gates.py", root / "tools/v05_beta_release_gates.py")
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "core.autocrlf=false", "add", "."],
                cwd=root,
                check=True,
            )
            result = subprocess.run(
                [sys.executable, "tools/v05_beta_release_gates.py", "--check"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("baseline-ref is required for closure candidate", result.stdout)

    def test_cli_requires_baseline_for_published_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "---\n" + json.dumps(record_fixture("published")) + "\n---\n",
                encoding="utf-8",
            )
            (root / "tools").mkdir()
            shutil.copy2(ROOT / "tools/v05_beta_release_gates.py", root / "tools/v05_beta_release_gates.py")
            self._initialize_repository(root)
            result = subprocess.run(
                [sys.executable, "tools/v05_beta_release_gates.py", "--check"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("baseline-ref is required for published", result.stdout)

    def test_cli_rejects_wrong_release_and_invalid_phase_baselines(self) -> None:
        for name, baseline, diagnostic in (
            (
                "wrong release",
                {"release": "0.4-alpha"},
                "baseline release shall equal 0.5-beta",
            ),
            (
                "invalid phase",
                {"phase": "closure_candidate"},
                "closure_candidate shall transition only from evidence_candidate",
            ),
        ):
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    (root / "tools").mkdir()
                    shutil.copy2(
                        ROOT / "tools/v05_beta_release_gates.py",
                        root / "tools/v05_beta_release_gates.py",
                    )
                    record_path = root / RECORD_RELATIVE
                    record_path.parent.mkdir(parents=True)
                    previous = record_fixture("evidence_candidate")
                    previous.update(baseline)
                    record_path.write_text(
                        "---\n" + json.dumps(previous) + "\n---\n",
                        encoding="utf-8",
                    )
                    self._initialize_repository(root, commit=True)
                    record_path.write_text(
                        "---\n" + json.dumps(record_fixture("closure_candidate")) + "\n---\n",
                        encoding="utf-8",
                    )
                    result = subprocess.run(
                        [
                            sys.executable,
                            "tools/v05_beta_release_gates.py",
                            "--check",
                            "--baseline-ref",
                            "HEAD",
                        ],
                        cwd=root,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(1, result.returncode)
                    self.assertIn(diagnostic, result.stdout)

    def test_cli_validates_baseline_against_its_git_ref(self) -> None:
        for mutation, diagnostic in (
            ("scope", "baseline record: scope shall equal the derived repository scope"),
            ("mapping", "baseline record: tracked mapping sets shall remain draft"),
        ):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self._copy_scope_inputs(root)
                    self._reduce_catalog_mapping_sources(root)
                    (root / "tools").mkdir()
                    shutil.copy2(
                        ROOT / "tools/v05_beta_release_gates.py",
                        root / "tools/v05_beta_release_gates.py",
                    )
                    record_path = root / RECORD_RELATIVE
                    record_path.parent.mkdir(parents=True)
                    record_path.write_text(
                        "---\n" + json.dumps(record_fixture("evidence_candidate")) + "\n---\n",
                        encoding="utf-8",
                    )
                    if mutation == "scope":
                        controls_path = root / "controls/catalog.json"
                        controls = json.loads(controls_path.read_text(encoding="utf-8"))
                        controls["control_count"] = 92
                        controls_path.write_text(json.dumps(controls), encoding="utf-8")
                    else:
                        catalog_path = root / "crosswalks/catalog.json"
                        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
                        catalog["mapping_sets"][0]["metadata"]["status"] = "published"
                        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
                    self._initialize_repository(root, commit=True)
                    if mutation == "scope":
                        shutil.copy2(ROOT / "controls/catalog.json", root / "controls/catalog.json")
                    else:
                        shutil.copy2(ROOT / "crosswalks/catalog.json", root / "crosswalks/catalog.json")
                    record_path.write_text(
                        "---\n" + json.dumps(record_fixture("closure_candidate")) + "\n---\n",
                        encoding="utf-8",
                    )
                    result = subprocess.run(
                        [
                            sys.executable,
                            "tools/v05_beta_release_gates.py",
                            "--check",
                            "--baseline-ref",
                            "HEAD",
                        ],
                        cwd=root,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(1, result.returncode)
                    self.assertIn(diagnostic, result.stdout)

    def test_cli_rejects_scope_change_outside_closure_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_scope_inputs(root)
            self._reduce_catalog_mapping_sources(root)
            (root / "tools").mkdir()
            shutil.copy2(
                ROOT / "tools/v05_beta_release_gates.py",
                root / "tools/v05_beta_release_gates.py",
            )
            record_path = root / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                "---\n" + json.dumps(record_fixture("evidence_candidate")) + "\n---\n",
                encoding="utf-8",
            )
            self._initialize_repository(root, commit=True)
            controls_path = root / "controls/catalog.json"
            controls = json.loads(controls_path.read_text(encoding="utf-8"))
            controls["control_count"] = 92
            controls_path.write_text(json.dumps(controls), encoding="utf-8")
            candidate = record_fixture("closure_candidate")
            candidate["scope"] = derive_scope(root)
            record_path.write_text(
                "---\n" + json.dumps(candidate) + "\n---\n", encoding="utf-8"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/v05_beta_release_gates.py",
                    "--check",
                    "--baseline-ref",
                    "HEAD",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn(
                "closure candidate changed paths shall equal the exact allowlist",
                result.stdout,
            )

    def _prepare_cli_root(self, root: Path) -> None:
        self._copy_scope_inputs(root)
        self._reduce_catalog_mapping_sources(root)
        (root / "tools").mkdir()
        shutil.copy2(
            ROOT / "tools/v05_beta_release_gates.py",
            root / "tools/v05_beta_release_gates.py",
        )

    def _run_closure_candidate(
        self,
        changed_paths: set[str],
    ) -> subprocess.CompletedProcess[str]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self._prepare_cli_root(root)
        record_path = root / RECORD_RELATIVE
        record_path.parent.mkdir(parents=True)
        record_path.write_text(
            readiness_document(record_fixture("evidence_candidate")),
            encoding="utf-8",
        )
        for relative in EXPECTED_CLOSURE_ALLOWLIST - {RECORD_RELATIVE}:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"baseline {relative}\n", encoding="utf-8")
        self._initialize_repository(root, commit=True)

        for relative in changed_paths:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if relative == RECORD_RELATIVE:
                path.write_text(
                    readiness_document(record_fixture("closure_candidate")),
                    encoding="utf-8",
                )
            else:
                path.write_text(f"closure {relative}\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", "--all"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Test User",
                "-c",
                "user.email=test@example.test",
                "commit",
                "--quiet",
                "-m",
                "closure",
            ],
            cwd=root,
            check=True,
        )
        return subprocess.run(
            [
                sys.executable,
                "tools/v05_beta_release_gates.py",
                "--check",
                "--baseline-ref",
                "HEAD^",
            ],
            cwd=root,
            capture_output=True,
            text=True,
        )

    def _copy_scope_inputs(self, destination: Path) -> None:
        for relative in (
            "controls/catalog.json",
            "architectures/patterns",
            "crosswalks/catalog.json",
            "assessment/ESAF-1500.md",
            "profiles/uk/0.1.0/profile.json",
            "docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json",
        ):
            source = ROOT / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)

    def _initialize_repository(self, root: Path, *, commit: bool = False) -> None:
        subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
        subprocess.run(
            ["git", "-c", "core.autocrlf=false", "add", "."],
            cwd=root,
            check=True,
        )
        if commit:
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test User",
                    "-c",
                    "user.email=test@example.test",
                    "commit",
                    "--quiet",
                    "-m",
                    "baseline",
                ],
                cwd=root,
                check=True,
            )

    def _reduce_catalog_mapping_sources(self, root: Path) -> None:
        source = (
            ROOT
            / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/"
            "3.3/0.4-alpha/0.1.0/README.md"
        )
        target = root / "crosswalks/mappings/source.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        catalog_path = root / "crosswalks/catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for mapping_set in catalog["mapping_sets"]:
            mapping_set["path"] = "crosswalks/mappings/source.md"
            mapping_set["provisions"] = []
        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
