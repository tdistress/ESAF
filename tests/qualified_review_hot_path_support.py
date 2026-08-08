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
from tools.crosswalks.qualified_review_evidence import CampaignEvidence, ReviewFinding, build_campaign_archive, build_seal_record, canonical_json_bytes
from tools.validate_qualified_review_evidence import (
    MappingSetCompletionPolicyInput,
    MappingSetPolicyInput,
    DraftReferencePolicyInput,
    ReviewerEligibilityPolicyInput,
    RoleFindingsPolicyInput,
    VALIDATOR_VERSION,
    ValidationReport,
    _ValidationFailure,
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


ReviewerMetadata = tuple[tuple[str, object], ...]


@dataclass(frozen=True)
class NarrowMappingSetFacts:
    mapping_set_id: str
    mapper_identities: frozenset[str]
    record_ids: frozenset[str]
    authoritative_findings: tuple[tuple[object, ...], ...] | None
    mapping_set_reviewer_metadata: ReviewerMetadata | None
    record_reviewer_metadata: tuple[ReviewerMetadata | None, ...]


@dataclass(frozen=True)
class NarrowDraftFacts:
    phase: str
    evidence_valid: bool
    readiness_name: str
    readiness_value: bool
    campaign_id: str
    candidate_commit: str
    manifest_sha256: str
    seal_record_sha256: str


@dataclass(frozen=True)
class NarrowFixtureFacts:
    fixture_kind: str
    campaign_json: str
    candidate_references: tuple[tuple[str, str], ...]
    mapping_sets: tuple[NarrowMappingSetFacts, ...]
    draft: NarrowDraftFacts | None


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
    narrow_facts: tuple[NarrowFixtureFacts, ...]

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
        draft_manifest_sha256 = hashlib.sha256(draft_manifest_bytes).hexdigest()
        draft_seal_record_sha256 = hashlib.sha256(draft_seal_bytes).hexdigest()
        draft_reference = {
            "campaign_id": "issue-55-draft-review", "candidate_commit": candidate,
            "manifest_sha256": draft_manifest_sha256,
            "seal_record_sha256": draft_seal_record_sha256,
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
        candidate_references = (
            ("draft", candidate),
            ("reviewed", reviewed_candidate),
            ("description", str(finding["description_candidate"])),
            ("duplicate", str(finding["duplicate_candidate"])),
        )
        draft_facts = NarrowDraftFacts(
            phase="draft_review",
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            campaign_id="issue-55-draft-review",
            candidate_commit=candidate,
            manifest_sha256=draft_manifest_sha256,
            seal_record_sha256=draft_seal_record_sha256,
        )
        narrow_facts = (
            _capture_narrow_fixture(
                module,
                "draft",
                pristine_campaign,
                assemblies,
                candidate_references,
            ),
            _capture_narrow_fixture(
                module,
                "reviewed_final",
                pristine_final_campaign,
                reviewed_assemblies,
                candidate_references,
                draft=draft_facts,
            ),
            _capture_narrow_fixture(
                module,
                "description_candidate",
                finding["description_campaign"],
                finding["description_assemblies"],
                candidate_references,
            ),
            _capture_narrow_fixture(
                module,
                "duplicate_candidate",
                finding["duplicate_campaign"],
                finding["duplicate_assemblies"],
                candidate_references,
            ),
        )
        return cls(
            root, repository_root, repository, candidate, reader, assemblies,
            pristine_campaign, draft_allowlist, draft_archive_bytes, draft_seal,
            draft_seal_bytes, draft_seal_path, draft_archive_path,
            reviewed_repository, reviewed_candidate, reviewed_reader,
            reviewed_assemblies, draft_reference, pristine_final_campaign,
            **finding, narrow_facts=narrow_facts,
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


def _review_finding_mapping(finding: ReviewFinding) -> dict[str, object]:
    return {
        "finding_id": finding.finding_id,
        "affected_record_ids": list(finding.affected_record_ids),
        "severity": finding.severity,
        "status": finding.status,
        "disposition": finding.disposition,
        "resolver_or_acceptor": finding.resolver_or_acceptor,
        "disposition_date": finding.disposition_date,
        "acceptance_rationale": finding.acceptance_rationale,
    }


def _campaign_policy_mapping(campaign: CampaignEvidence) -> dict[str, object]:
    draft_reference = campaign.draft_campaign_reference
    result: dict[str, object] = {
        "campaign_id": campaign.campaign_id,
        "phase": campaign.phase,
        "candidate_state": campaign.candidate_state,
        "candidate_commit": campaign.candidate_commit,
        "mapping_sets": [],
    }
    if draft_reference is not None:
        result["draft_campaign_reference"] = {
            "campaign_id": draft_reference.campaign_id,
            "candidate_commit": draft_reference.candidate_commit,
            "manifest_sha256": draft_reference.manifest_sha256,
            "seal_record_sha256": draft_reference.seal_record_sha256,
        }
    mapping_sets = result["mapping_sets"]
    assert isinstance(mapping_sets, list)
    for mapping_set in campaign.mapping_sets:
        roles: list[dict[str, object]] = []
        for role in mapping_set.roles:
            reviewer = role.reviewer
            worksheet = role.worksheet
            roles.append(
                {
                    "role": role.role,
                    "reviewer": {
                        "identity": reviewer.identity,
                        "organization": reviewer.organization,
                        "verification_locator": reviewer.verification_locator,
                        "qualification": reviewer.qualification,
                        "authorized_source_access": reviewer.authorized_source_access,
                        "independent": reviewer.independent,
                        "conflicts": reviewer.conflicts,
                        "conflict_disposition": reviewer.conflict_disposition,
                    },
                    "owner_eligibility_accepted": role.owner_eligibility_accepted,
                    "dual_role_accepted": role.dual_role_accepted,
                    "review_date": worksheet.review_date,
                    "conclusion": worksheet.conclusion,
                    "post_correction_candidate_sha": (
                        worksheet.post_correction_candidate_sha
                    ),
                    "findings_disposition": worksheet.findings_disposition,
                    "findings": [
                        _review_finding_mapping(finding)
                        for finding in role.worksheet_findings
                    ],
                }
            )
        mapping_sets.append(
            {"mapping_set_id": mapping_set.mapping_set_id, "roles": roles}
        )
    return result


def _candidate_finding_tuple(value: object) -> tuple[object, ...]:
    if not isinstance(value, dict):
        raise ValueError("candidate mapping finding is not an object")
    affected = value.get("affected_record_ids", ())
    if not isinstance(affected, (list, tuple)):
        raise ValueError("candidate mapping finding record identifiers are invalid")
    return (
        value.get("finding_id"),
        tuple(affected),
        value.get("severity"),
        value.get("description"),
        value.get("status"),
        value.get("disposition"),
        value.get("resolver_or_acceptor", ""),
        value.get("disposition_date", ""),
        value.get("acceptance_rationale", ""),
    )


def _reviewer_metadata(value: object) -> ReviewerMetadata | None:
    if not isinstance(value, dict):
        return None
    return tuple(value.items())


def _capture_mapping_set_facts(
    module: Any,
    mapping_set_id: str,
    assembly: object,
) -> NarrowMappingSetFacts:
    payloads = getattr(assembly, "payloads")
    mapping_payload = next(
        payload for payload in payloads if payload.purpose == "mapping set"
    )
    mapping_metadata, _mapping_body = module.parse_front_matter_bytes(
        mapping_payload.content
    )
    record_metadata = tuple(
        module.parse_front_matter_bytes(payload.content)[0]
        for payload in payloads
        if payload.purpose == "mapping record"
    )
    mapper_identities: set[str] = set()
    mapper = mapping_metadata.get("mapper")
    if isinstance(mapper, dict):
        mapper_identities.add(str(mapper.get("id", "")))
    for metadata in record_metadata:
        record_mapper = metadata.get("mapper")
        if isinstance(record_mapper, dict):
            mapper_identities.add(str(record_mapper.get("id", "")))
    findings = mapping_metadata.get("findings")
    authoritative = (
        tuple(_candidate_finding_tuple(finding) for finding in findings)
        if isinstance(findings, list)
        else None
    )
    return NarrowMappingSetFacts(
        mapping_set_id=mapping_set_id,
        mapper_identities=frozenset(mapper_identities),
        record_ids=frozenset(
            str(metadata.get("record_id")) for metadata in record_metadata
        ),
        authoritative_findings=authoritative,
        mapping_set_reviewer_metadata=_reviewer_metadata(
            mapping_metadata.get("reviewer")
        ),
        record_reviewer_metadata=tuple(
            _reviewer_metadata(metadata.get("reviewer"))
            for metadata in record_metadata
        ),
    )


def _capture_narrow_fixture(
    module: Any,
    fixture_kind: str,
    campaign_root: object,
    assemblies: object,
    candidate_references: tuple[tuple[str, str], ...],
    *,
    draft: NarrowDraftFacts | None = None,
) -> NarrowFixtureFacts:
    if not isinstance(campaign_root, Path) or not isinstance(assemblies, dict):
        raise TypeError("narrow fixture acquisition inputs are invalid")
    manifest = json.loads((campaign_root / "REVIEW_EVIDENCE.json").read_bytes())
    campaign = CampaignEvidence.from_mapping(manifest)
    return NarrowFixtureFacts(
        fixture_kind=fixture_kind,
        campaign_json=json.dumps(
            _campaign_policy_mapping(campaign),
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        candidate_references=candidate_references,
        mapping_sets=tuple(
            _capture_mapping_set_facts(
                module,
                mapping_set.mapping_set_id,
                assemblies[mapping_set.mapping_set_id],
            )
            for mapping_set in campaign.mapping_sets
        ),
        draft=draft,
    )


def resolve_operation_value(fixture: QualifiedReviewHotPathFixture, value: OperationValue) -> FrozenValue:
    return _resolve_operation_value(
        (
            ("draft", fixture.candidate),
            ("reviewed", fixture.reviewed_candidate),
            ("description", fixture.description_candidate),
            ("duplicate", fixture.duplicate_candidate),
        ),
        value,
    )


def _resolve_operation_value(
    candidate_references: tuple[tuple[str, str], ...],
    value: OperationValue,
) -> FrozenValue:
    if isinstance(value, CandidateReference):
        values = dict(candidate_references)
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


def _apply_operations_with_references(
    candidate_references: tuple[tuple[str, str], ...],
    manifest: dict[str, object],
    case: QualifiedReviewPolicyCase,
) -> None:
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
        if (
            isinstance(target, dict)
            and isinstance(final, str)
            and final not in target
            and isinstance(target.get("worksheet"), dict)
            and (
                final in target["worksheet"]
                or final == "post_correction_candidate_sha"
            )
        ):
            target = target["worksheet"]
        if isinstance(target, dict) and isinstance(final, str) and final in target:
            old = target[final]
            new = _thaw(
                _resolve_operation_value(candidate_references, operation.value)
            )
            if type(new) is not type(old) and not (
                final == "post_correction_candidate_sha"
                and old is None
                and isinstance(new, str)
            ):
                raise TypeError(f"operation type mismatch at {operation.path}")
            target[final] = new
        elif (
            isinstance(target, dict)
            and final == "post_correction_candidate_sha"
            and isinstance(operation.value, (str, CandidateReference))
        ):
            target[final] = _thaw(
                _resolve_operation_value(candidate_references, operation.value)
            )
        elif isinstance(target, list) and isinstance(final, int) and 0 <= final < len(target):
            old = target[final]
            new = _thaw(
                _resolve_operation_value(candidate_references, operation.value)
            )
            if type(new) is not type(old):
                raise TypeError(f"operation type mismatch at {operation.path}")
            target[final] = new
        else:
            raise ValueError(f"operation cannot grow or address unknown path: {operation.path}")


def _apply_operations(
    fixture: QualifiedReviewHotPathFixture,
    manifest: dict[str, object],
    case: QualifiedReviewPolicyCase,
) -> None:
    _apply_operations_with_references(
        (
            ("draft", fixture.candidate),
            ("reviewed", fixture.reviewed_candidate),
            ("description", fixture.description_candidate),
            ("duplicate", fixture.duplicate_candidate),
        ),
        manifest,
        case,
    )


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


def _narrow_fixture_facts(
    fixture: QualifiedReviewHotPathFixture,
    fixture_kind: str,
) -> NarrowFixtureFacts:
    for facts in fixture.narrow_facts:
        if facts.fixture_kind == fixture_kind:
            return facts
    raise ValueError(f"unknown fixture kind: {fixture_kind}")


def _mapping(value: object, subject: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{subject} is not an object")
    return value


def _sequence(value: object, subject: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{subject} is not an array")
    return value


def _string(value: object, subject: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{subject} is not a string")
    return value


def _boolean(value: object, subject: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{subject} is not a boolean")
    return value


def _derived_reviewer_metadata(role: dict[str, object]) -> ReviewerMetadata:
    reviewer = _mapping(role.get("reviewer"), "reviewer")
    return (
        ("id", _string(reviewer.get("identity"), "reviewer identity")),
        ("date", _string(role.get("review_date"), "review date")),
        (
            "qualification",
            _string(reviewer.get("qualification"), "reviewer qualification"),
        ),
        (
            "authorized_source_access",
            _boolean(
                reviewer.get("authorized_source_access"),
                "authorized source access",
            ),
        ),
        (
            "findings_disposition",
            _string(role.get("findings_disposition"), "findings disposition"),
        ),
    )


def _mapping_set_policy_input(
    campaign: dict[str, object],
    mapping_set: dict[str, object],
    facts: NarrowMappingSetFacts,
) -> MappingSetPolicyInput:
    mapping_set_id = _string(
        mapping_set.get("mapping_set_id"), "mapping-set identifier"
    )
    roles = tuple(
        _mapping(role, "review role")
        for role in _sequence(mapping_set.get("roles"), "review roles")
    )
    if len(roles) != 2:
        raise ValueError("narrow fixture does not contain both review roles")
    eligibility: list[ReviewerEligibilityPolicyInput] = []
    findings: list[RoleFindingsPolicyInput] = []
    for index, role in enumerate(roles):
        reviewer = _mapping(role.get("reviewer"), "reviewer")
        other_reviewer = _mapping(
            roles[1 - index].get("reviewer"), "other reviewer"
        )
        eligibility.append(
            ReviewerEligibilityPolicyInput(
                mapping_set_id=mapping_set_id,
                role=_string(role.get("role"), "review role"),
                reviewer_identity=_string(
                    reviewer.get("identity"), "reviewer identity"
                ),
                reviewer_verification_locator=_string(
                    reviewer.get("verification_locator"),
                    "reviewer verification locator",
                ),
                other_reviewer_identity=_string(
                    other_reviewer.get("identity"), "other reviewer identity"
                ),
                other_reviewer_verification_locator=_string(
                    other_reviewer.get("verification_locator"),
                    "other reviewer verification locator",
                ),
                authorized_source_access=_boolean(
                    reviewer.get("authorized_source_access"),
                    "authorized source access",
                ),
                independent=_boolean(
                    reviewer.get("independent"), "reviewer independence"
                ),
                conflicts=_boolean(
                    reviewer.get("conflicts"), "reviewer conflicts"
                ),
                conflict_disposition=_string(
                    reviewer.get("conflict_disposition"),
                    "conflict disposition",
                ),
                owner_eligibility_accepted=_boolean(
                    role.get("owner_eligibility_accepted"),
                    "owner eligibility acceptance",
                ),
                dual_role_accepted=_boolean(
                    role.get("dual_role_accepted"), "dual-role acceptance"
                ),
                qualification=_string(
                    reviewer.get("qualification"), "reviewer qualification"
                ),
                mapper_identities=facts.mapper_identities,
            )
        )
        findings.append(
            RoleFindingsPolicyInput(
                mapping_set_id=mapping_set_id,
                role=_string(role.get("role"), "review role"),
                conclusion=_string(role.get("conclusion"), "review conclusion"),
                post_correction_candidate_sha=(
                    _string(
                        role["post_correction_candidate_sha"],
                        "post-correction candidate",
                    )
                    if role.get("post_correction_candidate_sha") is not None
                    else None
                ),
                candidate_commit=_string(
                    campaign.get("candidate_commit"), "campaign candidate"
                ),
                record_ids=facts.record_ids,
                findings=tuple(
                    ReviewFinding.from_mapping(finding)
                    for finding in _sequence(
                        role.get("findings"), "review findings"
                    )
                ),
                mapping_ready=True,
                observed_findings=(),
            )
        )
    role_map = {
        _string(role.get("role"), "review role"): role for role in roles
    }
    return MappingSetPolicyInput(
        reviewer_eligibility=tuple(eligibility),
        role_findings=tuple(findings),
        mapping_set_completion=MappingSetCompletionPolicyInput(
            mapping_set_id=mapping_set_id,
            mapping_ready=True,
            observed_findings=(),
            authoritative_findings=facts.authoritative_findings,
            candidate_state=_string(
                campaign.get("candidate_state"), "campaign candidate state"
            ),
            specification_reviewer_metadata=_derived_reviewer_metadata(
                role_map["specification_and_inventory"]
            ),
            mapping_set_reviewer_metadata=(
                facts.mapping_set_reviewer_metadata
            ),
            security_reviewer_metadata=_derived_reviewer_metadata(
                role_map["security_and_overclaiming"]
            ),
            record_reviewer_metadata=facts.record_reviewer_metadata,
        ),
    )


def _draft_reference_policy_input(
    campaign: dict[str, object],
    facts: NarrowFixtureFacts,
) -> DraftReferencePolicyInput:
    reference = _mapping(
        campaign.get("draft_campaign_reference"), "Draft campaign reference"
    )
    draft = facts.draft
    if draft is None:
        raise ValueError("final fixture has no Draft input facts")
    referenced_candidate = _string(
        reference.get("candidate_commit"), "referenced candidate"
    )
    return DraftReferencePolicyInput(
        reviewed_candidate=_string(
            campaign.get("candidate_commit"), "reviewed candidate"
        ),
        referenced_candidate=referenced_candidate,
        draft_phase=draft.phase,
        draft_evidence_valid=draft.evidence_valid,
        draft_readiness_name=draft.readiness_name,
        draft_readiness_value=draft.readiness_value,
        reference_campaign_id=_string(
            reference.get("campaign_id"), "referenced campaign identifier"
        ),
        draft_campaign_id=draft.campaign_id,
        reference_candidate_commit=referenced_candidate,
        draft_candidate_commit=draft.candidate_commit,
        reference_manifest_sha256=_string(
            reference.get("manifest_sha256"), "referenced manifest digest"
        ),
        draft_manifest_sha256=draft.manifest_sha256,
        reference_seal_record_sha256=_string(
            reference.get("seal_record_sha256"), "referenced seal digest"
        ),
        draft_seal_record_sha256=draft.seal_record_sha256,
    )


def run_narrow_case(
    fixture: QualifiedReviewHotPathFixture,
    case: QualifiedReviewPolicyCase,
) -> ReportProjection:
    """Reconstruct and evaluate one case from immutable in-memory inputs."""
    facts = _narrow_fixture_facts(fixture, case.fixture_kind)
    campaign = json.loads(facts.campaign_json)
    if not isinstance(campaign, dict):
        raise ValueError("frozen narrow campaign is not an object")
    _apply_operations_with_references(
        facts.candidate_references,
        campaign,
        case,
    )
    phase = _string(campaign.get("phase"), "campaign phase")
    readiness_name = (
        "merge_ready"
        if phase == "final_reviewed_confirmation"
        else "transition_ready"
    )
    candidate = _string(
        campaign.get("candidate_commit"), "campaign candidate"
    )
    campaign_id = _string(
        campaign.get("campaign_id"), "campaign identifier"
    )
    try:
        if case.boundary == "draft_reference":
            evaluate_draft_reference_policy(
                _draft_reference_policy_input(campaign, facts)
            )
            ready = True
        elif case.boundary == "role_readiness":
            fact_by_id = {
                mapping_set.mapping_set_id: mapping_set
                for mapping_set in facts.mapping_sets
            }
            ready = True
            for value in _sequence(
                campaign.get("mapping_sets"), "campaign mapping sets"
            ):
                mapping_set = _mapping(value, "campaign mapping set")
                mapping_set_id = _string(
                    mapping_set.get("mapping_set_id"),
                    "mapping-set identifier",
                )
                try:
                    mapping_facts = fact_by_id[mapping_set_id]
                except KeyError as error:
                    raise ValueError(
                        f"unknown narrow mapping set: {mapping_set_id}"
                    ) from error
                ready = (
                    evaluate_mapping_set_policy(
                        _mapping_set_policy_input(
                            campaign,
                            mapping_set,
                            mapping_facts,
                        )
                    )
                    and ready
                )
        else:
            raise ValueError(f"unknown policy boundary: {case.boundary}")
        return ReportProjection(
            True,
            readiness_name,
            ready,
            candidate,
            campaign_id,
            (),
        )
    except _ValidationFailure as error:
        return ReportProjection(
            False,
            readiness_name,
            False,
            candidate,
            campaign_id,
            (str(error),),
        )
