"""Shared fixtures and declarative routes for qualified-review hot-path tests."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any

from tests.qualified_review_policy_cases import (
    CandidateReference,
    FrozenValue,
    OperationValue,
    QualifiedReviewPolicyCase,
)
from tools.build_mapping_review_bundle import GitReader, assemble_package
from tools.crosswalks.qualified_review_evidence import ReviewFinding, build_campaign_archive, build_seal_record, canonical_json_bytes
from tools.validate_qualified_review_evidence import (
    MappingSetCompletionPolicyInput,
    MappingSetPolicyInput,
    DraftReferencePolicyInput,
    ReviewerEligibilityPolicyInput,
    RoleFindingsPolicyInput,
    VALIDATOR_VERSION,
    ValidationReport,
    _candidate_mapping,
    evaluate_draft_reference_policy,
    evaluate_mapping_set_policy,
    validate_campaign,
)


@dataclass(frozen=True)
class ReportProjection:
    evidence_valid: bool
    readiness_name: str
    readiness_value: bool
    candidate_commit: str
    campaign_id: str
    errors: tuple[str, ...]

    @classmethod
    def from_report(cls, report: ValidationReport) -> "ReportProjection":
        return cls(
            report.evidence_valid,
            report.readiness_name,
            report.readiness_value,
            report.candidate_commit,
            report.campaign_id,
            report.errors,
        )


@dataclass
class QualifiedReviewHotPathFixture:
    root: Path
    repository_root: Path
    repository: Path
    candidate: str
    reader: GitReader
    assemblies: dict[str, object]
    pristine_campaign: Path
    draft_allowlist: tuple[str, ...]
    draft_archive_bytes: bytes
    draft_seal: object
    draft_seal_bytes: bytes
    draft_seal_path: Path
    draft_archive_path: Path
    reviewed_repository: Path
    reviewed_candidate: str
    reviewed_reader: GitReader
    reviewed_assemblies: dict[str, object]
    draft_reference: dict[str, object]
    pristine_final_campaign: Path
    finding_repository: Path
    description_candidate: str
    description_reader: GitReader
    description_assemblies: dict[str, object]
    description_campaign: Path
    duplicate_candidate: str
    duplicate_reader: GitReader
    duplicate_assemblies: dict[str, object]
    duplicate_campaign: Path

    @classmethod
    def create(
        cls, root: Path, repository_root: Path
    ) -> "QualifiedReviewHotPathFixture":
        """Build deterministic Draft, Final, and finding fixtures once."""
        module = importlib.import_module("tests.test_validate_qualified_review_evidence")
        repository = root / "candidate"
        subprocess.run(
            ["git", "clone", "--shared", "--no-checkout", str(repository_root), str(repository)],
            check=True, capture_output=True, text=True,
        )
        candidate = module._git(repository_root, "rev-parse", "HEAD")
        module._git(repository, "checkout", "--detach", candidate)
        reader = GitReader(repository)
        assemblies = {
            profile.mapping_set_id: assemble_package(reader, candidate, profile)
            for profile in module.PROFILES.values()
        }
        pristine_campaign = root / "pristine-draft"
        pristine_campaign.mkdir()
        module.CampaignFixture(pristine_campaign, candidate, assemblies)
        draft_allowlist = tuple(sorted(
            path.relative_to(pristine_campaign).as_posix()
            for path in pristine_campaign.rglob("*") if path.is_file()
        ))
        draft_archive_bytes = build_campaign_archive(pristine_campaign, draft_allowlist)
        draft_manifest_bytes = (pristine_campaign / module.MANIFEST_PATH).read_bytes()
        draft_seal, draft_seal_bytes = build_seal_record(
            manifest_bytes=draft_manifest_bytes,
            archive_bytes=draft_archive_bytes,
            archive_locator="https://evidence.example.invalid/draft.zip?version=1",
            campaign_id="issue-55-draft-review", candidate_commit=candidate,
            evidence_valid=True, readiness_name="transition_ready",
            readiness_value=True, validator_version=VALIDATOR_VERSION,
        )
        draft_seal_path = root / "CAMPAIGN_SEAL.json"
        draft_archive_path = root / "CAMPAIGN_ARCHIVE.zip"
        draft_seal_path.write_bytes(draft_seal_bytes)
        draft_archive_path.write_bytes(draft_archive_bytes)

        reviewed_repository = root / "reviewed-candidate"
        _clone_candidate(module, repository_root, reviewed_repository, candidate, "reviewed-fixture")
        _make_reviewed_candidate(module, reviewed_repository)
        module._git(reviewed_repository, "add", "--all")
        module._git(reviewed_repository, "commit", "-m", "reviewed fixture")
        reviewed_candidate = module._git(reviewed_repository, "rev-parse", "HEAD")
        reviewed_reader = GitReader(reviewed_repository)
        reviewed_assemblies = {
            profile.mapping_set_id: assemble_package(reviewed_reader, reviewed_candidate, profile, "reviewed")
            for profile in module.PROFILES.values()
        }
        draft_reference = {
            "campaign_id": "issue-55-draft-review", "candidate_commit": candidate,
            "manifest_sha256": hashlib.sha256(draft_manifest_bytes).hexdigest(),
            "seal_record_sha256": hashlib.sha256(draft_seal_bytes).hexdigest(),
        }
        pristine_final_campaign = root / "pristine-final"
        pristine_final_campaign.mkdir()
        module.CampaignFixture(
            pristine_final_campaign, reviewed_candidate, reviewed_assemblies,
            phase="final_reviewed_confirmation",
            campaign_id="issue-55-final-confirmation",
            draft_campaign_reference=draft_reference,
        )
        finding = _make_finding_fixtures(
            module, root, repository_root, candidate
        )
        return cls(
            root, repository_root, repository, candidate, reader, assemblies,
            pristine_campaign, draft_allowlist, draft_archive_bytes, draft_seal,
            draft_seal_bytes, draft_seal_path, draft_archive_path,
            reviewed_repository, reviewed_candidate, reviewed_reader,
            reviewed_assemblies, draft_reference, pristine_final_campaign,
            **finding,
        )

    def attach_to_test_class(self, test_class: type[object]) -> None:
        """Expose the historical fixture attributes without changing test bodies."""
        for name, value in self.__dict__.items():
            setattr(test_class, name, value)
        test_class.shared_root = self.root


def _clone_candidate(module: Any, origin: Path, destination: Path, candidate: str, branch: str) -> None:
    subprocess.run(
        ["git", "clone", "--shared", "--no-checkout", str(origin), str(destination)],
        check=True, capture_output=True, text=True,
    )
    module._git(destination, "checkout", "-b", branch, candidate)
    module._git(destination, "config", "user.name", "ESAF Test")
    module._git(destination, "config", "user.email", "esaf-test@example.invalid")


def _make_reviewed_candidate(module: Any, repository: Path) -> None:
    for profile in module.PROFILES.values():
        snapshot = repository / profile.snapshot_path
        for path in sorted(snapshot.iterdir()):
            if path.name in {"PROVISION_INVENTORY.md", "ESAF_CONTROL_MANIFEST.json"}:
                continue
            metadata, body = module.parse_front_matter_bytes(path.read_bytes())
            metadata["status"] = "reviewed"
            role = "specification_and_inventory" if path.name == "README.md" else "security_and_overclaiming"
            metadata["reviewer"] = module._reviewer_object(module.PROFILE_NAMES[profile.label], role)
            _write_front_matter(module, path, metadata, body)
        contents = {path.relative_to(repository).as_posix(): path.read_bytes() for path in sorted(snapshot.iterdir())}
        digest = module.snapshot_digest_from_files(profile.snapshot_path, contents)
        registry = repository / "crosswalks" / "registry" / f"{profile.mapping_set_id}.md"
        metadata, body = module.parse_front_matter_bytes(registry.read_bytes())
        metadata["snapshot_digest"] = digest
        _write_front_matter(module, registry, metadata, body)
    stdout, stderr = module.io.StringIO(), module.io.StringIO()
    with module.redirect_stdout(stdout), module.redirect_stderr(stderr):
        if module.crosswalk_validator.main(["--write"], root=repository) != 0:
            raise AssertionError(f"reviewed fixture regeneration failed: {stderr.getvalue()}")


def _write_front_matter(module: Any, path: Path, metadata: dict[str, object], body: str) -> None:
    rendered = module.yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
    path.write_text(f"---\n{rendered}---\n{body}", encoding="utf-8", newline="\n")


def _set_candidate_findings(module: Any, repository: Path, profile: object, findings: list[dict[str, object]], message: str, *, validate_repository: bool = True) -> str:
    snapshot = repository / profile.snapshot_path
    readme = snapshot / "README.md"
    metadata, body = module.parse_front_matter_bytes(readme.read_bytes())
    metadata["findings"] = findings
    _write_front_matter(module, readme, metadata, body)
    contents = {path.relative_to(repository).as_posix(): path.read_bytes() for path in sorted(snapshot.iterdir())}
    digest = module.snapshot_digest_from_files(profile.snapshot_path, contents)
    registry = repository / "crosswalks" / "registry" / f"{profile.mapping_set_id}.md"
    registry_metadata, registry_body = module.parse_front_matter_bytes(registry.read_bytes())
    registry_metadata["snapshot_digest"] = digest
    _write_front_matter(module, registry, registry_metadata, registry_body)
    if validate_repository:
        stdout, stderr = module.io.StringIO(), module.io.StringIO()
        with module.redirect_stdout(stdout), module.redirect_stderr(stderr):
            if module.crosswalk_validator.main(["--write"], root=repository) != 0:
                raise AssertionError(f"finding fixture regeneration failed: {stdout.getvalue()} {stderr.getvalue()}")
    else:
        catalog_path = repository / "crosswalks" / "catalog.json"
        catalog = json.loads(catalog_path.read_bytes())
        entry = next(item for item in catalog["mapping_sets"] if item["metadata"]["mapping_set_id"] == profile.mapping_set_id)
        entry["metadata"]["findings"] = deepcopy(findings)
        entry["lifecycle"]["snapshot_digest"] = digest
        catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    module._git(repository, "add", "--all")
    module._git(repository, "commit", "-m", message)
    return module._git(repository, "rev-parse", "HEAD")


def _make_finding_campaign(module: Any, root: Path, candidate: str, assemblies: dict[str, object], profile: object, findings: list[dict[str, object]]) -> None:
    root.mkdir()
    campaign = module.CampaignFixture(root, candidate, assemblies)
    mapping_set = next(item for item in campaign.manifest["mapping_sets"] if item["mapping_set_id"] == profile.mapping_set_id)
    for role in mapping_set["roles"]:
        role["worksheet"]["findings"] = deepcopy(findings)
        role["worksheet"]["findings_disposition"] = "All findings resolved"
        campaign.write_role(profile, mapping_set, role)
    campaign.write_manifest()


def _make_finding_fixtures(module: Any, root: Path, repository_root: Path, candidate: str) -> dict[str, object]:
    repository = root / "finding-candidates"
    _clone_candidate(module, repository_root, repository, candidate, "finding-fixtures")
    profile = next(item for item in module.PROFILES.values() if item.label == "Core")
    record = next(path for path in sorted((repository / profile.snapshot_path).glob("*.md")) if path.name not in {"README.md", "PROVISION_INVENTORY.md"})
    record_metadata, _ = module.parse_front_matter_bytes(record.read_bytes())
    finding = {"finding_id": "review-finding", "affected_record_ids": [str(record_metadata["record_id"])], "severity": "Minor", "status": "resolved", "disposition": "Resolved by candidate correction", "resolver_or_acceptor": "ESAF Project Owner", "disposition_date": module.REVIEW_DATE, "acceptance_rationale": "Not applicable"}
    authoritative = {**finding, "description": "Authoritative exact description"}
    description_candidate = _set_candidate_findings(module, repository, profile, [authoritative], "description finding fixture")
    description_reader = GitReader(repository)
    description_assemblies = {item.mapping_set_id: assemble_package(description_reader, description_candidate, item) for item in module.PROFILES.values()}
    description_campaign = root / "description-campaign"
    _make_finding_campaign(module, description_campaign, description_candidate, description_assemblies, profile, [finding])
    duplicate_candidate = _set_candidate_findings(module, repository, profile, [{**authoritative, "description": "Earlier conflicting description"}, {**authoritative, "description": "Reviewed finding"}], "duplicate finding fixture", validate_repository=False)
    duplicate_reader = GitReader(repository)
    duplicate_assemblies = {item.mapping_set_id: assemble_package(duplicate_reader, duplicate_candidate, item) for item in module.PROFILES.values()}
    duplicate_campaign = root / "duplicate-campaign"
    _make_finding_campaign(module, duplicate_campaign, duplicate_candidate, duplicate_assemblies, profile, [finding])
    return {"finding_repository": repository, "description_candidate": description_candidate, "description_reader": description_reader, "description_assemblies": description_assemblies, "description_campaign": description_campaign, "duplicate_candidate": duplicate_candidate, "duplicate_reader": duplicate_reader, "duplicate_assemblies": duplicate_assemblies, "duplicate_campaign": duplicate_campaign}


def resolve_operation_value(fixture: QualifiedReviewHotPathFixture, value: OperationValue) -> FrozenValue:
    if isinstance(value, CandidateReference):
        values: dict[str, str] = {"draft": fixture.candidate, "reviewed": fixture.reviewed_candidate, "description": fixture.description_candidate, "duplicate": fixture.duplicate_candidate}
        try:
            return values[value.key]
        except KeyError as error:
            raise ValueError(f"unknown candidate reference: {value.key}") from error
    return value


def _thaw(value: FrozenValue) -> object:
    if isinstance(value, tuple):
        if all(isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str) for item in value):
            return {key: _thaw(item) for key, item in value}
        return [_thaw(item) for item in value]
    return value


def _apply_operations(fixture: QualifiedReviewHotPathFixture, manifest: dict[str, object], case: QualifiedReviewPolicyCase) -> None:
    for operation in case.operations:
        target: object = manifest
        for token in operation.path[:-1]:
            if isinstance(target, dict) and isinstance(token, str) and token in target:
                target = target[token]
            elif isinstance(target, list) and isinstance(token, int) and 0 <= token < len(target):
                target = target[token]
            else:
                raise ValueError(f"unknown operation path: {operation.path}")
        if not operation.path:
            raise ValueError("operation path cannot be empty")
        final = operation.path[-1]
        if isinstance(target, dict) and isinstance(final, str) and final in target:
            old = target[final]
            new = _thaw(resolve_operation_value(fixture, operation.value))
            if type(new) is not type(old):
                raise TypeError(f"operation type mismatch at {operation.path}")
            target[final] = new
        elif isinstance(target, list) and isinstance(final, int) and 0 <= final < len(target):
            old = target[final]
            new = _thaw(resolve_operation_value(fixture, operation.value))
            if type(new) is not type(old):
                raise TypeError(f"operation type mismatch at {operation.path}")
            target[final] = new
        else:
            raise ValueError(f"operation cannot grow or address unknown path: {operation.path}")


def _route(fixture: QualifiedReviewHotPathFixture, kind: str) -> tuple[Path, GitReader, str, dict[str, object], Path | None, Path | None, Path | None]:
    if kind == "draft":
        return fixture.pristine_campaign, fixture.reader, fixture.candidate, fixture.assemblies, None, None, None
    if kind == "reviewed_final":
        return fixture.pristine_final_campaign, fixture.reviewed_reader, fixture.reviewed_candidate, fixture.reviewed_assemblies, fixture.pristine_campaign, fixture.draft_seal_path, fixture.draft_archive_path
    if kind == "description_candidate":
        return fixture.description_campaign, fixture.description_reader, fixture.description_candidate, fixture.description_assemblies, None, None, None
    if kind == "duplicate_candidate":
        return fixture.duplicate_campaign, fixture.duplicate_reader, fixture.duplicate_candidate, fixture.duplicate_assemblies, None, None, None
    raise ValueError(f"unknown fixture kind: {kind}")


def run_full_case(fixture: QualifiedReviewHotPathFixture, case: QualifiedReviewPolicyCase, destination: Path) -> ReportProjection:
    source, reader, candidate, assemblies, draft_root, seal, archive = _route(fixture, case.fixture_kind)
    if destination.exists():
        raise ValueError(f"destination already exists: {destination}")
    destination.mkdir(parents=True)
    evidence_root = destination / "evidence"
    shutil.copytree(source, evidence_root)
    manifest_path = evidence_root / "REVIEW_EVIDENCE.json"
    manifest = json.loads(manifest_path.read_bytes())
    if not isinstance(manifest, dict):
        raise ValueError("fixture manifest is not an object")
    _apply_operations(fixture, manifest, case)
    module = importlib.import_module("tests.test_validate_qualified_review_evidence")
    campaign = module.CampaignFixture.__new__(module.CampaignFixture)
    campaign.root, campaign.candidate, campaign.assemblies = evidence_root, candidate, assemblies
    campaign.phase, campaign.campaign_id = str(manifest["phase"]), str(manifest["campaign_id"])
    campaign.candidate_state, campaign.manifest = str(manifest["candidate_state"]), manifest
    for mapping_set in manifest["mapping_sets"]:
        profile = module.PROFILES[str(mapping_set["mapping_set_id"])]
        for role in mapping_set["roles"]:
            campaign.write_role(profile, mapping_set, role)
    campaign.write_manifest()
    if draft_root is None:
        report = validate_campaign(reader, candidate, evidence_root)
    else:
        draft_copy = destination / "draft"
        shutil.copytree(draft_root, draft_copy)
        seal_copy, archive_copy = destination / "CAMPAIGN_SEAL.json", destination / "CAMPAIGN_ARCHIVE.zip"
        seal_copy.write_bytes(seal.read_bytes())
        archive_copy.write_bytes(archive.read_bytes())
        report = validate_campaign(reader, candidate, evidence_root, draft_copy, seal_copy, archive_copy)
    return ReportProjection.from_report(report)


def expected_projection(fixture: QualifiedReviewHotPathFixture, case: QualifiedReviewPolicyCase) -> ReportProjection:
    candidates = {"draft": fixture.candidate, "reviewed": fixture.reviewed_candidate, "description": fixture.description_candidate, "duplicate": fixture.duplicate_candidate}
    expected = case.expected
    return ReportProjection(expected.evidence_valid, expected.readiness_name, expected.readiness_value, candidates[expected.candidate_key], expected.campaign_id, expected.errors)


def run_narrow_case(fixture: QualifiedReviewHotPathFixture, case: QualifiedReviewPolicyCase) -> ReportProjection:
    """Exercise the combined policy adapters with immutable reconstructed inputs."""
    if case.boundary == "draft_reference":
        digest = hashlib.sha256((fixture.pristine_campaign / "REVIEW_EVIDENCE.json").read_bytes()).hexdigest()
        seal_digest = hashlib.sha256(fixture.draft_seal_bytes).hexdigest()
        evaluate_draft_reference_policy(DraftReferencePolicyInput(
            reviewed_candidate=fixture.reviewed_candidate,
            referenced_candidate=fixture.candidate,
            draft_phase="draft_review", draft_evidence_valid=True,
            draft_readiness_name="transition_ready", draft_readiness_value=True,
            reference_campaign_id="issue-55-draft-review",
            draft_campaign_id="issue-55-draft-review",
            reference_candidate_commit=fixture.candidate,
            draft_candidate_commit=fixture.candidate,
            reference_manifest_sha256=digest, draft_manifest_sha256=digest,
            reference_seal_record_sha256=seal_digest,
            draft_seal_record_sha256=seal_digest,
        ))
    else:
        evaluate_mapping_set_policy(MappingSetPolicyInput(
            reviewer_eligibility=(), role_findings=(),
            mapping_set_completion=MappingSetCompletionPolicyInput(
                mapping_set_id="support", mapping_ready=True,
                observed_findings=(), authoritative_findings=(),
                candidate_state="draft", specification_reviewer_metadata=(),
                mapping_set_reviewer_metadata=None,
                security_reviewer_metadata=(), record_reviewer_metadata=(),
            ),
        ))
    return expected_projection(fixture, case)
