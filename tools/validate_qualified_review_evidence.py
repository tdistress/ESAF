"""Validate externally retained qualified-review campaign evidence."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Mapping
import unicodedata

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mapping_review_bundle import (
    PROFILES,
    GitReader,
    PackageAssembly,
    assemble_package,
    parse_front_matter_bytes,
)
from tools.crosswalks.qualified_review_evidence import (
    CampaignEvidence,
    EvidenceError,
    EvidenceOperationalError,
    MappingSetEvidence,
    ReviewFinding,
    RoleEvidence,
    build_campaign_archive,
    build_seal_record,
    canonical_json_bytes,
    parse_completed_attestation,
    parse_completed_worksheet,
    read_external_regular_file,
    require_locator_digest,
    signed_worksheet_sha256,
)


VALIDATOR_VERSION = "1.0.0"
_MANIFEST_PATH = "REVIEW_EVIDENCE.json"
_SCHEMA_PATH = "crosswalks/schema/qualified-review-evidence.schema.json"
_ROLES = {
    "specification_and_inventory": "Specification and inventory review",
    "security_and_overclaiming": "Security and overclaiming review",
}
_TABLE_ROW = re.compile(r"^\| ([^|\\]+) \| ([^|\\]*) \|$")
_RESOLVED_CONFLICT = re.compile(r"^Resolved: [^\r\n|]+$")
_SCHEMA_ID = (
    "https://esaf-standard.org/schemas/"
    "qualified-review-evidence.schema.json"
)
_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"
_CANDIDATE_CACHE: dict[
    tuple[str, str, str, str],
    _CandidateMapping,
] = {}


class _ValidationFailure(ValueError):
    """One sanitized content-validation failure."""


class OperationalEvidenceError(RuntimeError):
    """One sanitized operational failure suitable for CLI handling."""


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        del message
        raise OperationalEvidenceError("invalid command arguments")


@dataclass(frozen=True)
class ValidationReport:
    evidence_valid: bool
    readiness_name: str
    readiness_value: bool
    candidate_commit: str
    campaign_id: str
    errors: tuple[str, ...]

    def as_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "candidate_commit": self.candidate_commit,
            "errors": list(self.errors),
            "evidence_valid": self.evidence_valid,
            "readiness_name": self.readiness_name,
            "readiness_value": self.readiness_value,
        }


@dataclass(frozen=True)
class _CandidateMapping:
    assembly: PackageAssembly
    mapping_metadata: Mapping[str, object]
    mapping_body: str
    record_metadata: tuple[Mapping[str, object], ...]


@dataclass(frozen=True)
class _ValidationDetails:
    report: ValidationReport
    campaign: CampaignEvidence
    manifest_bytes: bytes
    allowlist: tuple[str, ...]
    archive_bytes: bytes


def _fail(message: str) -> None:
    raise _ValidationFailure(message)


def _read_external(
    root: Path,
    relative: str,
    worktrees: tuple[Path, ...],
    snapshot: dict[str, bytes] | None = None,
) -> bytes:
    content = read_external_regular_file(root, relative, worktrees)
    if snapshot is not None:
        prior = snapshot.setdefault(relative, content)
        if prior != content:
            _fail(f"{relative} changed between validated reads")
    return content


def _read_external_path(
    path: Path,
    worktrees: tuple[Path, ...],
) -> bytes:
    return read_external_regular_file(path.parent, path.name, worktrees)


def _load_campaign(
    reader: GitReader,
    candidate: str,
    evidence_root: Path,
    worktrees: tuple[Path, ...],
    snapshot: dict[str, bytes],
) -> tuple[CampaignEvidence, bytes]:
    schema_bytes = reader.read_bytes(candidate, _SCHEMA_PATH)
    try:
        schema = json.loads(schema_bytes)
        _require_local_schema(schema)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        SchemaError,
        ValueError,
    ) as error:
        raise _ValidationFailure("candidate evidence schema is invalid") from error

    manifest_bytes = _read_external(
        evidence_root,
        _MANIFEST_PATH,
        worktrees,
        snapshot,
    )
    try:
        manifest = json.loads(manifest_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise _ValidationFailure("REVIEW_EVIDENCE.json is invalid JSON") from error
    if canonical_json_bytes(manifest) != manifest_bytes:
        _fail("REVIEW_EVIDENCE.json is not canonical JSON")
    errors = sorted(
        validator.iter_errors(manifest),
        key=lambda error: (
            tuple(str(item) for item in error.absolute_path),
            error.message,
        ),
    )
    if errors:
        path = ".".join(str(item) for item in errors[0].absolute_path)
        subject = path or "campaign"
        _fail(f"{subject} does not satisfy the campaign schema")
    return CampaignEvidence.from_mapping(manifest), manifest_bytes


def _require_local_schema(schema: object) -> None:
    if not isinstance(schema, dict):
        _fail("candidate evidence schema is invalid")
    if (
        schema.get("$schema") != _SCHEMA_DIALECT
        or schema.get("$id") != _SCHEMA_ID
    ):
        _fail("candidate evidence schema identity is invalid")

    pending: list[tuple[object, bool]] = [(schema, True)]
    while pending:
        value, root = pending.pop()
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {"$ref", "$dynamicRef", "$recursiveRef"} and (
                    not isinstance(item, str) or not item.startswith("#/")
                ):
                    _fail("candidate evidence schema has an external reference")
                if not root and key in {"$schema", "$id"}:
                    _fail("candidate evidence schema has a nested schema identity")
                pending.append((item, False))
        elif isinstance(value, list):
            pending.extend((item, False) for item in value)


def _mapping_entries(
    campaign: CampaignEvidence,
) -> dict[str, MappingSetEvidence]:
    result: dict[str, MappingSetEvidence] = {}
    for mapping_set in campaign.mapping_sets:
        if mapping_set.mapping_set_id in result:
            _fail("campaign contains a duplicate mapping-set identifier")
        result[mapping_set.mapping_set_id] = mapping_set
        roles = [role.role for role in mapping_set.roles]
        if len(roles) != len(set(roles)):
            _fail(
                f"{mapping_set.mapping_set_id} contains a duplicate review role"
            )
        if set(roles) != set(_ROLES):
            _fail(
                f"{mapping_set.mapping_set_id} does not contain both review roles"
            )
    if set(result) != set(PROFILES):
        _fail("campaign does not contain the exact three mapping sets")
    return result


def _candidate_mapping(
    *,
    reader: GitReader,
    candidate: str,
    candidate_state: str,
    mapping_set: MappingSetEvidence,
) -> _CandidateMapping:
    key = (
        str(reader.root),
        candidate,
        candidate_state,
        mapping_set.mapping_set_id,
    )
    cached = _CANDIDATE_CACHE.get(key)
    if cached is not None:
        return cached
    profile = PROFILES[mapping_set.mapping_set_id]
    try:
        assembly = assemble_package(
            reader,
            candidate,
            profile,
            candidate_state,  # type: ignore[arg-type]
        )
    except ValueError as error:
        raise _ValidationFailure(
            f"{mapping_set.mapping_set_id} candidate package is invalid"
        ) from error
    mapping_payload = next(
        payload for payload in assembly.payloads
        if payload.purpose == "mapping set"
    )
    mapping_metadata, mapping_body = parse_front_matter_bytes(
        mapping_payload.content
    )
    record_metadata: list[Mapping[str, object]] = []
    for payload in assembly.payloads:
        if payload.purpose != "mapping record":
            continue
        metadata, _record_body = parse_front_matter_bytes(payload.content)
        record_metadata.append(metadata)
    result = _CandidateMapping(
        assembly=assembly,
        mapping_metadata=mapping_metadata,
        mapping_body=mapping_body,
        record_metadata=tuple(record_metadata),
    )
    _CANDIDATE_CACHE[key] = result
    return result


def _read_package(
    *,
    evidence_root: Path,
    worktrees: tuple[Path, ...],
    mapping_set: MappingSetEvidence,
    candidate_mapping: _CandidateMapping,
    allowlist: list[str],
    snapshot: dict[str, bytes],
) -> None:
    package = mapping_set.package
    expected_manifest_path = f"{package.root}/PACKAGE_MANIFEST.json"
    if package.manifest_path != expected_manifest_path:
        _fail(
            f"{mapping_set.mapping_set_id} package manifest path is not "
            "root/PACKAGE_MANIFEST.json"
        )
    assembly = candidate_mapping.assembly
    manifest_bytes = _read_external(
        evidence_root,
        package.manifest_path,
        worktrees,
        snapshot,
    )
    if hashlib.sha256(manifest_bytes).hexdigest() != package.manifest_sha256:
        _fail(
            f"{mapping_set.mapping_set_id} package manifest digest does not match"
        )
    try:
        require_locator_digest(
            package.immutable_locator,
            package.manifest_sha256,
            f"{mapping_set.mapping_set_id} package immutable locator",
        )
    except EvidenceError as error:
        raise _ValidationFailure(str(error)) from error
    if manifest_bytes != assembly.manifest_bytes:
        _fail(
            f"{mapping_set.mapping_set_id} package manifest differs from "
            "exact candidate reconstruction"
        )
    try:
        observed_manifest = json.loads(manifest_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise _ValidationFailure(
            f"{mapping_set.mapping_set_id} package manifest is invalid JSON"
        ) from error
    if observed_manifest != assembly.manifest:
        _fail(
            f"{mapping_set.mapping_set_id} package manifest semantics differ "
            "from exact candidate reconstruction"
        )

    allowlist.append(package.manifest_path)
    for payload in assembly.payloads:
        campaign_path = f"{package.root}/{payload.path}"
        observed = _read_external(
            evidence_root,
            campaign_path,
            worktrees,
            snapshot,
        )
        if observed != payload.content:
            _fail(
                f"{campaign_path} differs from exact candidate reconstruction"
            )
        allowlist.append(campaign_path)



def _markdown_fields(content: bytes) -> dict[str, str]:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise _ValidationFailure("worksheet is not UTF-8") from error
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = _TABLE_ROW.fullmatch(line)
        if match is None:
            continue
        label, value = match.groups()
        if label == "Field":
            continue
        if label in fields:
            _fail(f"worksheet repeats the {label} field")
        fields[label] = value
    return fields


def _campaign_finding(finding: ReviewFinding) -> tuple[object, ...]:
    return (
        finding.finding_id,
        finding.affected_record_ids,
        finding.severity,
        finding.status,
        finding.disposition,
        finding.resolver_or_acceptor,
        finding.disposition_date,
        finding.acceptance_rationale,
    )


def _authoritative_finding(finding: ReviewFinding) -> tuple[object, ...]:
    return (
        finding.finding_id,
        finding.affected_record_ids,
        finding.severity,
        finding.description,
        finding.status,
        finding.disposition,
        finding.resolver_or_acceptor,
        finding.disposition_date,
        finding.acceptance_rationale,
    )


def _candidate_finding(value: object) -> tuple[object, ...]:
    if not isinstance(value, dict):
        _fail("candidate mapping finding is not an object")
    return (
        value.get("finding_id"),
        tuple(value.get("affected_record_ids", ())),
        value.get("severity"),
        value.get("description"),
        value.get("status"),
        value.get("disposition"),
        value.get("resolver_or_acceptor", ""),
        value.get("disposition_date", ""),
        value.get("acceptance_rationale", ""),
    )


def _expected_publication(
    candidate_mapping: _CandidateMapping,
) -> dict[str, str]:
    metadata = candidate_mapping.mapping_metadata
    try:
        publication = metadata["publication"]
        source_version = metadata["source_version"]
        source = metadata["source"]
        rights = metadata["publication_rights"]
        assert isinstance(publication, dict)
        assert isinstance(source_version, dict)
        assert isinstance(source, dict)
        assert isinstance(rights, dict)
        prohibited = rights["prohibited_elements"]
        assert isinstance(prohibited, list)
        permitted = rights["permitted_elements"]
        assert isinstance(permitted, list)
        checksums: set[str] = set()
        locators: set[str] = set()
        for payload in candidate_mapping.assembly.payloads:
            if payload.purpose != "source evidence pin":
                continue
            evidence = json.loads(payload.content)
            assert isinstance(evidence, dict)
            evidence_source = evidence["source"]
            assert isinstance(evidence_source, dict)
            variants = evidence_source["variants"]
            assert isinstance(variants, list)
            for variant in variants:
                assert isinstance(variant, dict)
                checksum = variant["sha256"]
                locator = variant["url"]
                assert isinstance(checksum, str)
                assert re.fullmatch(r"[0-9a-f]{64}", checksum)
                assert isinstance(locator, str) and locator
                checksums.add(checksum)
                locators.add(locator)
        if not checksums and not locators:
            source_section = candidate_mapping.mapping_body.split(
                "## Source and publication rights\n",
                1,
            )
            if len(source_section) != 2:
                raise AssertionError("candidate has no source section")
            source_text = source_section[1].split("\n## ", 1)[0]
            pinned = set(
                re.findall(
                    r"SHA-256 `([0-9a-f]{64})`",
                    source_text,
                )
            )
            official_url = source.get("official_url")
            if len(pinned) != 1 or not isinstance(official_url, str):
                raise AssertionError("candidate source pin is ambiguous")
            checksums.update(pinned)
            locators.add(official_url)
        if not checksums or not locators:
            raise AssertionError("candidate has no unambiguous source set")
        return {
            "publication_identity": str(publication["name"]),
            "source_version": str(source_version["id"]),
            "official_url": str(source["official_url"]),
            "source_checksums": ", ".join(sorted(checksums)),
            "source_locators": ", ".join(sorted(locators)),
            "publication_rights_basis": str(rights["basis"]),
            "permitted_elements": ", ".join(str(item) for item in permitted),
            "prohibited_elements": (
                ", ".join(str(item) for item in prohibited)
                if prohibited
                else "None"
            ),
            "restrictions": str(rights["restrictions"]),
        }
    except (
        AssertionError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        UnicodeDecodeError,
    ) as error:
        raise _ValidationFailure(
            "candidate publication metadata cannot be derived"
        ) from error


def _require_equal(
    actual: object,
    expected: object,
    subject: str,
) -> None:
    if actual != expected:
        _fail(f"{subject} does not match the campaign")


def _validate_role_files(
    *,
    campaign: CampaignEvidence,
    mapping_set: MappingSetEvidence,
    role: RoleEvidence,
    candidate_mapping: _CandidateMapping,
    evidence_root: Path,
    worktrees: tuple[Path, ...],
    allowlist: list[str],
    snapshot: dict[str, bytes],
) -> tuple[ReviewFinding, ...]:
    attestation_bytes = _read_external(
        evidence_root,
        role.attestation.path,
        worktrees,
        snapshot,
    )
    if (
        hashlib.sha256(attestation_bytes).hexdigest()
        != role.attestation.sha256
    ):
        _fail(f"{role.attestation.path} digest does not match")
    try:
        require_locator_digest(
            role.attestation.immutable_locator,
            role.attestation.sha256,
            f"{role.attestation.path} immutable locator",
        )
    except EvidenceError as error:
        raise _ValidationFailure(str(error)) from error
    attestation = parse_completed_attestation(attestation_bytes)

    worksheet_bytes = _read_external(
        evidence_root,
        role.worksheet.path,
        worktrees,
        snapshot,
    )
    if hashlib.sha256(worksheet_bytes).hexdigest() != role.worksheet.sha256:
        _fail(f"{role.worksheet.path} digest does not match")
    try:
        require_locator_digest(
            role.worksheet.immutable_locator,
            role.worksheet.sha256,
            f"{role.worksheet.path} immutable locator",
        )
    except EvidenceError as error:
        raise _ValidationFailure(str(error)) from error
    worksheet = parse_completed_worksheet(worksheet_bytes, role.role)
    if (
        signed_worksheet_sha256(worksheet_bytes)
        != role.worksheet.signed_sha256
        or worksheet.signed_worksheet_sha256
        != role.worksheet.signed_sha256
    ):
        _fail(f"{role.worksheet.path} signed digest does not match")
    fields = _markdown_fields(worksheet_bytes)

    package = mapping_set.package
    reviewer = role.reviewer
    publication = _expected_publication(candidate_mapping)
    expected_attestation = {
        "reviewer_identity": reviewer.identity,
        "organization": reviewer.organization,
        "verification_locator": reviewer.verification_locator,
        "mapping_set_identifier": mapping_set.mapping_set_id,
        "candidate_commit_sha": campaign.candidate_commit,
        "package_root": package.root,
        "package_manifest_path": package.manifest_path,
        "package_manifest_sha256": package.manifest_sha256,
        "package_immutable_locator": package.immutable_locator,
        "package_retention_owner": package.retention_owner,
        "attestation_path": role.attestation.path,
        "attestation_immutable_locator": role.attestation.immutable_locator,
        "attestation_retention_owner": role.attestation.retention_owner,
        "review_role": _ROLES[role.role],
        "publication_identity": publication["publication_identity"],
        "exact_source_version": publication["source_version"],
        "official_url": publication["official_url"],
        "source_checksums": publication["source_checksums"],
        "source_locators": publication["source_locators"],
        "publication_rights_basis": publication[
            "publication_rights_basis"
        ],
        "permitted_elements": publication["permitted_elements"],
        "prohibited_elements": publication["prohibited_elements"],
        "restrictions": publication["restrictions"],
        "qualification": reviewer.qualification,
        "authorized_source_access": (
            "Yes" if reviewer.authorized_source_access else "No"
        ),
        "independence_from_mapper": (
            "Yes" if reviewer.independent else "No"
        ),
        "conflicts_of_interest": "Yes" if reviewer.conflicts else "No",
        "conflict_disposition": reviewer.conflict_disposition,
        "project_owner_eligibility_acceptance": (
            "Accepted" if role.owner_eligibility_accepted else "Rejected"
        ),
        "project_owner_dual_role_acceptance": (
            "Yes" if role.dual_role_accepted else "No"
        ),
        "source_content_exclusion": "Yes",
        "source_content_exclusion_date": role.worksheet.review_date,
    }
    for field, expected in expected_attestation.items():
        _require_equal(
            attestation.get(field),
            expected,
            f"{role.attestation.path} {field}",
        )

    expected_worksheet = {
        "Mapping-set identifier": mapping_set.mapping_set_id,
        "Candidate commit SHA": campaign.candidate_commit,
        "Package root": package.root,
        "Package manifest path": package.manifest_path,
        "Package-manifest SHA-256": package.manifest_sha256,
        "Package immutable locator": package.immutable_locator,
        "Package retention owner": package.retention_owner,
        "Reviewer identity": reviewer.identity,
        "Attestation path": role.attestation.path,
        "Attestation immutable locator": role.attestation.immutable_locator,
        "Attestation retention owner": role.attestation.retention_owner,
        "Attestation SHA-256": role.attestation.sha256,
        "Worksheet path": role.worksheet.path,
        "Worksheet immutable locator": role.worksheet.immutable_locator,
        "Worksheet retention owner": role.worksheet.retention_owner,
        "Review role": _ROLES[role.role],
        "Review date": role.worksheet.review_date,
    }
    for field, expected in expected_worksheet.items():
        _require_equal(
            fields.get(field),
            expected,
            f"{role.worksheet.path} {field}",
        )
    _require_equal(
        worksheet.reviewer_identity,
        reviewer.identity,
        f"{role.worksheet.path} reviewer identity",
    )
    _require_equal(
        worksheet.review_date,
        role.worksheet.review_date,
        f"{role.worksheet.path} review date",
    )
    _require_equal(
        worksheet.conclusion,
        role.worksheet.conclusion,
        f"{role.worksheet.path} conclusion",
    )
    _require_equal(
        worksheet.post_correction_candidate_sha,
        role.worksheet.post_correction_candidate_sha,
        f"{role.worksheet.path} post-correction candidate",
    )
    _require_equal(
        worksheet.findings_disposition,
        role.worksheet.findings_disposition,
        f"{role.worksheet.path} findings disposition",
    )
    _require_equal(
        worksheet.attestation_sha256,
        role.attestation.sha256,
        f"{role.worksheet.path} attestation digest",
    )
    if tuple(
        _campaign_finding(finding) for finding in worksheet.findings
    ) != tuple(
        _campaign_finding(finding) for finding in role.worksheet_findings
    ):
        _fail(f"{role.worksheet.path} findings do not match the campaign")

    allowlist.extend((role.attestation.path, role.worksheet.path))
    return worksheet.findings


def _derived_reviewer(role: RoleEvidence) -> dict[str, object]:
    return {
        "id": role.reviewer.identity,
        "date": role.worksheet.review_date,
        "qualification": role.reviewer.qualification,
        "authorized_source_access": role.reviewer.authorized_source_access,
        "findings_disposition": role.worksheet.findings_disposition,
    }


def _canonical_actor_identity(value: object) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return "".join(
        character
        for character in normalized
        if unicodedata.category(character)[0] in {"L", "N"}
    )


def _same_actor(first: RoleEvidence, second: RoleEvidence) -> bool:
    return (
        _canonical_actor_identity(first.reviewer.identity)
        == _canonical_actor_identity(second.reviewer.identity)
        or first.reviewer.verification_locator
        == second.reviewer.verification_locator
    )


def _validate_roles_and_readiness(
    *,
    campaign: CampaignEvidence,
    mapping_entries: dict[str, MappingSetEvidence],
    candidate_mappings: dict[str, _CandidateMapping],
    evidence_root: Path,
    worktrees: tuple[Path, ...],
    allowlist: list[str],
    snapshot: dict[str, bytes],
) -> bool:
    ready = True
    for mapping_set_id, mapping_set in mapping_entries.items():
        candidate_mapping = candidate_mappings[mapping_set_id]
        mapping_ready = True
        duplicate_identity = _same_actor(
            mapping_set.roles[0],
            mapping_set.roles[1],
        )
        mapper_ids: set[str] = set()
        mapper = candidate_mapping.mapping_metadata.get("mapper")
        if isinstance(mapper, dict):
            mapper_ids.add(_canonical_actor_identity(mapper.get("id")))
        for metadata in candidate_mapping.record_metadata:
            record_mapper = metadata.get("mapper")
            if isinstance(record_mapper, dict):
                mapper_ids.add(
                    _canonical_actor_identity(record_mapper.get("id"))
                )
        record_ids = {
            metadata.get("record_id")
            for metadata in candidate_mapping.record_metadata
        }
        observed_findings: dict[str, tuple[object, ...]] = {}
        for role in mapping_set.roles:
            if (
                not role.reviewer.authorized_source_access
                or not role.reviewer.independent
            ):
                _fail(
                    f"{mapping_set_id} {role.role} reviewer is not eligible"
                )
            if _canonical_actor_identity(role.reviewer.identity) in mapper_ids:
                _fail(
                    f"{mapping_set_id} {role.role} reviewer is also a mapper"
                )
            if role.reviewer.conflicts and _RESOLVED_CONFLICT.fullmatch(
                role.reviewer.conflict_disposition
            ) is None:
                _fail(
                    f"{mapping_set_id} {role.role} reviewer has an "
                    "unresolved conflict"
                )
            if not role.owner_eligibility_accepted:
                _fail(
                    f"{mapping_set_id} {role.role} reviewer eligibility "
                    "was rejected"
                )
            if duplicate_identity:
                if (
                    not role.dual_role_accepted
                    or not role.reviewer.qualification.strip()
                ):
                    _fail(
                        f"{mapping_set_id} duplicate reviewer lacks complete "
                        "dual-role acceptance and qualifications"
                    )
            elif role.dual_role_accepted:
                _fail(
                    f"{mapping_set_id} unique reviewer cannot claim a dual role"
                )
            findings = _validate_role_files(
                campaign=campaign,
                mapping_set=mapping_set,
                role=role,
                candidate_mapping=candidate_mapping,
                evidence_root=evidence_root,
                worktrees=worktrees,
                allowlist=allowlist,
                snapshot=snapshot,
            )
            conclusion = role.worksheet.conclusion
            if conclusion == "stop":
                mapping_ready = False
            elif (
                conclusion == "pass_after_correction"
                and role.worksheet.post_correction_candidate_sha
                != campaign.candidate_commit
            ):
                _fail(
                    f"{mapping_set_id} {role.role} post-correction "
                    "candidate is not the campaign candidate"
                )
            for finding in findings:
                if not set(finding.affected_record_ids) <= record_ids:
                    _fail(
                        f"{mapping_set_id} finding {finding.finding_id} "
                        "references an unknown record"
                    )
                if (
                    finding.status == "accepted"
                    and finding.severity in {"Critical", "Important"}
                ):
                    _fail(
                        f"{mapping_set_id} {finding.severity} finding "
                        "cannot be accepted"
                    )
                if conclusion != "stop" and finding.status == "open":
                    _fail(
                        f"{mapping_set_id} pass conclusion has an open finding"
                    )
                normalized = _authoritative_finding(finding)
                prior = observed_findings.get(finding.finding_id)
                if prior is not None and prior != normalized:
                    _fail(
                        f"{mapping_set_id} finding {finding.finding_id} "
                        "has conflicting role evidence"
                    )
                observed_findings[finding.finding_id] = normalized
        if mapping_ready:
            candidate_findings = candidate_mapping.mapping_metadata.get(
                "findings"
            )
            if not isinstance(candidate_findings, list):
                _fail(f"{mapping_set_id} candidate findings are invalid")
            candidate_finding_rows = tuple(
                _candidate_finding(finding)
                for finding in candidate_findings
            )
            candidate_ids = tuple(str(item[0]) for item in candidate_finding_rows)
            if len(candidate_ids) != len(set(candidate_ids)):
                _fail(
                    f"{mapping_set_id} candidate finding identifiers "
                    "are duplicated"
                )
            authoritative = dict(zip(
                candidate_ids,
                candidate_finding_rows,
                strict=True,
            ))
            if observed_findings != authoritative:
                _fail(
                    f"{mapping_set_id} findings do not equal authoritative "
                    "candidate findings"
                )
        if campaign.candidate_state == "reviewed":
            role_map = {role.role: role for role in mapping_set.roles}
            expected_snapshot_reviewer = _derived_reviewer(
                role_map["specification_and_inventory"]
            )
            if (
                candidate_mapping.mapping_metadata.get("reviewer")
                != expected_snapshot_reviewer
            ):
                _fail(
                    f"{mapping_set_id} mapping-set reviewer does not equal "
                    "the specification review evidence"
                )
            expected_record_reviewer = _derived_reviewer(
                role_map["security_and_overclaiming"]
            )
            if any(
                metadata.get("reviewer") != expected_record_reviewer
                for metadata in candidate_mapping.record_metadata
            ):
                _fail(
                    f"{mapping_set_id} record reviewer does not equal the "
                    "security review evidence"
                )
        ready = ready and mapping_ready
    return ready


def _exact_allowlist(allowlist: list[str]) -> tuple[str, ...]:
    if len(allowlist) != len(set(allowlist)):
        _fail("campaign paths are duplicated")
    seen_casefold: set[str] = set()
    for relative in allowlist:
        folded = relative.casefold()
        if folded in seen_casefold:
            _fail("campaign paths have a case-insensitive collision")
        seen_casefold.add(folded)
        if PurePosixPath(relative).suffix not in {".md", ".json"}:
            _fail(f"{relative} uses a forbidden campaign file extension")
    return tuple(sorted(allowlist))


def _validate_draft_reference(
    *,
    reader: GitReader,
    reviewed_campaign: CampaignEvidence,
    draft_evidence_root: Path,
    draft_seal_record: Path,
    draft_archive: Path,
    worktrees: tuple[Path, ...],
) -> None:
    reference = reviewed_campaign.draft_campaign_reference
    if reference is None:
        _fail("final campaign has no Draft campaign reference")
    if reference.candidate_commit == reviewed_campaign.candidate_commit:
        _fail("reviewed and Draft candidate commits must differ")
    draft_details = _validate_campaign_details(
        reader,
        reference.candidate_commit,
        draft_evidence_root,
    )
    if draft_details.campaign.phase != "draft_review":
        _fail("referenced campaign is not a Draft review campaign")
    if (
        not draft_details.report.evidence_valid
        or not draft_details.report.readiness_value
        or draft_details.report.readiness_name != "transition_ready"
    ):
        _fail("referenced Draft campaign is not transition-ready")
    if reference.campaign_id != draft_details.campaign.campaign_id:
        _fail("Draft campaign identifier does not match the reference")
    if reference.candidate_commit != draft_details.campaign.candidate_commit:
        _fail("Draft candidate commit does not match the reference")
    if (
        hashlib.sha256(draft_details.manifest_bytes).hexdigest()
        != reference.manifest_sha256
    ):
        _fail("Draft manifest digest does not match the reference")

    retained_archive = _read_external_path(draft_archive, worktrees)
    if retained_archive != draft_details.archive_bytes:
        _fail("retained Draft archive differs from deterministic reconstruction")
    seal_bytes = _read_external_path(draft_seal_record, worktrees)
    if hashlib.sha256(seal_bytes).hexdigest() != reference.seal_record_sha256:
        _fail("Draft seal-record digest does not match the reference")
    try:
        seal = json.loads(seal_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise _ValidationFailure("Draft seal record is invalid JSON") from error
    if canonical_json_bytes(seal) != seal_bytes or not isinstance(seal, dict):
        _fail("Draft seal record is not canonical JSON")
    archive_locator = seal.get("archive_locator")
    if not isinstance(archive_locator, str):
        _fail("Draft seal record archive locator is invalid")
    try:
        _expected_record, expected_seal_bytes = build_seal_record(
            manifest_bytes=draft_details.manifest_bytes,
            archive_bytes=draft_details.archive_bytes,
            archive_locator=archive_locator,
            campaign_id=draft_details.campaign.campaign_id,
            candidate_commit=draft_details.campaign.candidate_commit,
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            validator_version=VALIDATOR_VERSION,
        )
    except EvidenceError as error:
        raise _ValidationFailure("Draft seal record is invalid") from error
    if seal_bytes != expected_seal_bytes:
        _fail("Draft seal record differs from deterministic reconstruction")


def _validate_campaign_details(
    reader: GitReader,
    candidate: str,
    evidence_root: Path,
    draft_evidence_root: Path | None = None,
    draft_seal_record: Path | None = None,
    draft_archive: Path | None = None,
    report_context: dict[str, str] | None = None,
) -> _ValidationDetails:
    resolved_candidate = reader.resolve_commit(candidate)
    worktrees = reader.worktree_roots()
    snapshot: dict[str, bytes] = {}
    campaign, manifest_bytes = _load_campaign(
        reader,
        resolved_candidate,
        evidence_root,
        worktrees,
        snapshot,
    )
    if report_context is not None:
        report_context.update(
            {
                "campaign_id": campaign.campaign_id,
                "candidate_commit": resolved_candidate,
                "readiness_name": (
                    "merge_ready"
                    if campaign.phase == "final_reviewed_confirmation"
                    else "transition_ready"
                ),
            }
        )
    if campaign.candidate_commit != resolved_candidate:
        _fail("campaign candidate commit does not equal the supplied candidate")
    mapping_entries = _mapping_entries(campaign)
    allowlist = [_MANIFEST_PATH]
    candidate_mappings = {
        mapping_set_id: _candidate_mapping(
            reader=reader,
            candidate=resolved_candidate,
            candidate_state=campaign.candidate_state,
            mapping_set=mapping_set,
        )
        for mapping_set_id, mapping_set in mapping_entries.items()
    }
    ready = _validate_roles_and_readiness(
        campaign=campaign,
        mapping_entries=mapping_entries,
        candidate_mappings=candidate_mappings,
        evidence_root=evidence_root,
        worktrees=worktrees,
        allowlist=allowlist,
        snapshot=snapshot,
    )
    draft_inputs = (
        draft_evidence_root,
        draft_seal_record,
        draft_archive,
    )
    if campaign.phase == "final_reviewed_confirmation":
        if any(item is None for item in draft_inputs):
            _fail(
                "final campaign requires Draft evidence root, seal record, "
                "and archive"
            )
        assert draft_evidence_root is not None
        assert draft_seal_record is not None
        assert draft_archive is not None
        _validate_draft_reference(
            reader=reader,
            reviewed_campaign=campaign,
            draft_evidence_root=draft_evidence_root,
            draft_seal_record=draft_seal_record,
            draft_archive=draft_archive,
            worktrees=worktrees,
        )
    elif any(item is not None for item in draft_inputs):
        _fail("Draft campaign must not receive preserved Draft inputs")
    for mapping_set_id, mapping_set in mapping_entries.items():
        _read_package(
            evidence_root=evidence_root,
            worktrees=worktrees,
            mapping_set=mapping_set,
            candidate_mapping=candidate_mappings[mapping_set_id],
            allowlist=allowlist,
            snapshot=snapshot,
        )
    exact_allowlist = _exact_allowlist(allowlist)
    archive_bytes = build_campaign_archive(
        evidence_root,
        exact_allowlist,
        content_by_path=snapshot,
    )
    readiness_name = (
        "merge_ready"
        if campaign.phase == "final_reviewed_confirmation"
        else "transition_ready"
    )
    report = ValidationReport(
        evidence_valid=True,
        readiness_name=readiness_name,
        readiness_value=ready,
        candidate_commit=resolved_candidate,
        campaign_id=campaign.campaign_id,
        errors=(),
    )
    return _ValidationDetails(
        report=report,
        campaign=campaign,
        manifest_bytes=manifest_bytes,
        allowlist=exact_allowlist,
        archive_bytes=archive_bytes,
    )


def validate_campaign(
    reader: GitReader,
    candidate: str,
    evidence_root: Path,
    draft_evidence_root: Path | None = None,
    draft_seal_record: Path | None = None,
    draft_archive: Path | None = None,
) -> ValidationReport:
    """Validate one campaign without modifying repository or evidence bytes."""
    context = {
        "campaign_id": "",
        "candidate_commit": candidate,
        "readiness_name": "transition_ready",
    }
    try:
        details = _validate_campaign_details(
            reader,
            candidate,
            evidence_root,
            draft_evidence_root,
            draft_seal_record,
            draft_archive,
            context,
        )
        return details.report
    except EvidenceOperationalError:
        raise
    except UnicodeError:
        raise
    except (_ValidationFailure, EvidenceError, ValueError) as error:
        return ValidationReport(
            evidence_valid=False,
            readiness_name=context["readiness_name"],
            readiness_value=False,
            candidate_commit=context["candidate_commit"],
            campaign_id=context["campaign_id"],
            errors=(str(error),),
        )


def validate_retained_campaign(
    reader: GitReader,
    candidate: str,
    evidence_root: Path,
    seal_record: Path,
    archive: Path,
) -> ValidationReport:
    """Validate a Draft campaign and its exact externally retained seal bytes."""
    context = {
        "campaign_id": "",
        "candidate_commit": candidate,
        "readiness_name": "transition_ready",
    }
    try:
        details = _validate_campaign_details(
            reader,
            candidate,
            evidence_root,
            report_context=context,
        )
        if details.campaign.phase != "draft_review":
            _fail("retained campaign is not a Draft review campaign")
        worktrees = reader.worktree_roots()
        retained_archive = _read_external_path(archive, worktrees)
        if retained_archive != details.archive_bytes:
            _fail(
                "retained archive differs from deterministic reconstruction"
            )
        seal_bytes = _read_external_path(seal_record, worktrees)
        try:
            seal = json.loads(seal_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise _ValidationFailure(
                "retained seal record is invalid JSON"
            ) from error
        if canonical_json_bytes(seal) != seal_bytes or not isinstance(seal, dict):
            _fail("retained seal record is not canonical JSON")
        archive_locator = seal.get("archive_locator")
        if not isinstance(archive_locator, str):
            _fail("retained seal record archive locator is invalid")
        try:
            _expected_record, expected_seal_bytes = build_seal_record(
                manifest_bytes=details.manifest_bytes,
                archive_bytes=details.archive_bytes,
                archive_locator=archive_locator,
                campaign_id=details.campaign.campaign_id,
                candidate_commit=details.campaign.candidate_commit,
                evidence_valid=True,
                readiness_name="transition_ready",
                readiness_value=True,
                validator_version=VALIDATOR_VERSION,
            )
        except EvidenceError as error:
            raise _ValidationFailure(
                "retained seal record is invalid"
            ) from error
        if seal_bytes != expected_seal_bytes:
            _fail(
                "retained seal record differs from deterministic reconstruction"
            )
        return details.report
    except EvidenceOperationalError:
        raise
    except UnicodeError:
        raise
    except (_ValidationFailure, EvidenceError, ValueError) as error:
        return ValidationReport(
            evidence_valid=False,
            readiness_name=context["readiness_name"],
            readiness_value=False,
            candidate_commit=context["candidate_commit"],
            campaign_id=context["campaign_id"],
            errors=(str(error),),
        )


def main(
    argv: list[str] | None = None,
    *,
    root: Path = ROOT,
) -> int:
    """Run the read-only validator CLI."""
    parser = _ArgumentParser(add_help=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--draft-evidence-root", type=Path)
    parser.add_argument("--draft-seal-record", type=Path)
    parser.add_argument("--draft-archive", type=Path)
    parser.add_argument("--check", action="store_true", required=True)
    try:
        args = parser.parse_args(argv)
        draft_inputs = (
            args.draft_evidence_root,
            args.draft_seal_record,
            args.draft_archive,
        )
        if sum(item is not None for item in draft_inputs) not in {0, 3}:
            raise OperationalEvidenceError(
                "preserved Draft inputs must be supplied together"
            )
        try:
            root_mode = args.evidence_root.stat().st_mode
        except OSError as error:
            raise OperationalEvidenceError(
                "campaign root is unavailable"
            ) from error
        if not args.evidence_root.is_dir() or not root_mode:
            raise OperationalEvidenceError("campaign root is unavailable")
        reader = GitReader(root)
        candidate = reader.resolve_commit(args.candidate)
        report = validate_campaign(
            reader,
            candidate,
            args.evidence_root,
            args.draft_evidence_root,
            args.draft_seal_record,
            args.draft_archive,
        )
        print(
            canonical_json_bytes(report.as_mapping()).decode("utf-8"),
            end="",
        )
        return 0 if report.evidence_valid else 1
    except (
        EvidenceOperationalError,
        OperationalEvidenceError,
        OSError,
        subprocess.SubprocessError,
    ):
        print("qualified-review evidence operation failed", file=sys.stderr)
        return 2
    except ValueError:
        print("qualified-review evidence operation failed", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
