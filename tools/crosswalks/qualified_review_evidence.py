"""Safe I/O primitives for external qualified-review evidence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
from typing import ClassVar
from urllib.parse import parse_qsl, urlsplit
import zipfile


class EvidenceError(ValueError):
    """A sanitized qualified-review evidence validation failure."""


_COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_HTTPS_LOCATOR = re.compile(
    r"^https://"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)"
    r"(?:\.(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?))*"
    r"(?::[1-9][0-9]{0,4})?"
    r"(?:/(?:[A-Za-z0-9._~!$&'()*+,;=:@-]|%[0-9A-Fa-f]{2})*)*"
    r"\?(?:[A-Za-z0-9._~!$&'()*+,;=:@/?-]|%[0-9A-Fa-f]{2})*"
    r"(?:#(?:[A-Za-z0-9._~!$&'()*+,;=:@/?-]|%[0-9A-Fa-f]{2})*)?$"
)
_ROLES = {
    "specification_and_inventory": "Specification and inventory review",
    "security_and_overclaiming": "Security and overclaiming review",
}
_ATTESTATION_ROWS = (
    "Reviewer identity",
    "Organization",
    "Verification locator",
    "Mapping-set identifier",
    "Candidate commit SHA",
    "Package root",
    "Package manifest path",
    "Package-manifest SHA-256",
    "Package immutable locator",
    "Package retention owner",
    "Attestation path",
    "Attestation immutable locator",
    "Attestation retention owner",
    "Review role",
    "Publication identity",
    "Exact source version",
    "Official URL",
    "Source checksum(s)",
    "Source locator(s)",
    "Publication-rights basis",
    "Permitted elements",
    "Prohibited elements",
    "Restrictions",
    "Qualification",
    "Authorized source access",
    "Independence from mapper",
    "Conflicts of interest",
    "Conflict disposition",
    "Project-owner eligibility acceptance",
    "Project-owner dual-role acceptance",
    "Project-owner identity",
    "Project-owner signature",
    "Project-owner acceptance date",
    "Signature",
    "Date",
)
_WORKSHEET_IDENTIFICATION_ROWS = (
    "Mapping-set identifier",
    "Candidate commit SHA",
    "Package root",
    "Package manifest path",
    "Package-manifest SHA-256",
    "Package immutable locator",
    "Package retention owner",
    "Reviewer identity",
    "Attestation path",
    "Attestation immutable locator",
    "Attestation retention owner",
    "Attestation SHA-256",
    "Worksheet path",
    "Worksheet immutable locator",
    "Worksheet retention owner",
    "Review role",
    "Review date",
    "Coverage summary",
    "Review method",
    "Provision coverage",
    "Mapping-record coverage",
)
_CONCLUSION_ROWS = (
    "Overall conclusion",
    "Post-correction candidate SHA",
    "Reviewer metadata findings disposition",
)
_SIGNATURE_ROWS = (
    "Reviewer signature",
    "Signature date",
    "Signed worksheet SHA-256",
)
_FINDING_COLUMNS = (
    "Finding ID",
    "Affected record IDs",
    "Severity",
    "Description",
    "Evidence",
    "Required action",
    "Status",
    "Disposition",
    "Resolver or acceptor",
    "Disposition date",
    "Acceptance rationale",
)


def _mapping(
    value: object,
    subject: str,
    required: tuple[str, ...],
    optional: tuple[str, ...] = (),
) -> dict[str, object]:
    if type(value) is not dict:
        raise EvidenceError(f"{subject} must be an object")
    result = value
    assert isinstance(result, dict)
    keys = set(result)
    expected = set(required)
    allowed = expected | set(optional)
    missing = expected - keys
    unknown = keys - allowed
    if missing:
        raise EvidenceError(f"{subject} is missing required fields")
    if unknown:
        raise EvidenceError(f"{subject} contains unknown fields")
    return result


def _string(value: object, subject: str) -> str:
    if type(value) is not str:
        raise EvidenceError(f"{subject} must be a string")
    return value


def _boolean(value: object, subject: str) -> bool:
    if type(value) is not bool:
        raise EvidenceError(f"{subject} must be a Boolean")
    return value


def _sequence(value: object, subject: str) -> list[object]:
    if type(value) is not list:
        raise EvidenceError(f"{subject} must be an array")
    return value


@dataclass(frozen=True)
class ReviewerEvidence:
    identity: str
    organization: str
    verification_locator: str
    qualification: str
    authorized_source_access: bool
    independent: bool
    conflicts: bool
    conflict_disposition: str

    @classmethod
    def from_mapping(cls, value: object) -> ReviewerEvidence:
        fields = (
            "identity",
            "organization",
            "verification_locator",
            "qualification",
            "authorized_source_access",
            "independent",
            "conflicts",
            "conflict_disposition",
        )
        item = _mapping(value, "reviewer evidence", fields)
        return cls(
            identity=_string(item["identity"], "reviewer identity"),
            organization=_string(item["organization"], "reviewer organization"),
            verification_locator=_string(
                item["verification_locator"],
                "reviewer verification locator",
            ),
            qualification=_string(
                item["qualification"],
                "reviewer qualification",
            ),
            authorized_source_access=_boolean(
                item["authorized_source_access"],
                "authorized source access",
            ),
            independent=_boolean(item["independent"], "reviewer independence"),
            conflicts=_boolean(item["conflicts"], "reviewer conflicts"),
            conflict_disposition=_string(
                item["conflict_disposition"],
                "conflict disposition",
            ),
        )


@dataclass(frozen=True)
class AttestationEvidence:
    path: str
    immutable_locator: str
    retention_owner: str
    sha256: str

    @classmethod
    def from_mapping(cls, value: object) -> AttestationEvidence:
        fields = ("path", "immutable_locator", "retention_owner", "sha256")
        item = _mapping(value, "attestation evidence", fields)
        return cls(
            path=_string(item["path"], "attestation path"),
            immutable_locator=_string(
                item["immutable_locator"],
                "attestation immutable locator",
            ),
            retention_owner=_string(
                item["retention_owner"],
                "attestation retention owner",
            ),
            sha256=_string(item["sha256"], "attestation SHA-256"),
        )


@dataclass(frozen=True)
class ReviewFinding:
    finding_id: str
    affected_record_ids: tuple[str, ...]
    severity: str
    description: str
    evidence: str
    required_action: str
    status: str
    disposition: str
    resolver_or_acceptor: str
    disposition_date: str
    acceptance_rationale: str

    @classmethod
    def from_mapping(cls, value: object) -> ReviewFinding:
        fields = (
            "finding_id",
            "affected_record_ids",
            "severity",
            "status",
            "disposition",
            "resolver_or_acceptor",
            "disposition_date",
            "acceptance_rationale",
        )
        item = _mapping(value, "finding evidence", fields)
        affected = tuple(
            _string(record_id, "affected record identifier")
            for record_id in _sequence(
                item["affected_record_ids"],
                "affected record identifiers",
            )
        )
        return cls(
            finding_id=_string(item["finding_id"], "finding identifier"),
            affected_record_ids=affected,
            severity=_string(item["severity"], "finding severity"),
            description="",
            evidence="",
            required_action="",
            status=_string(item["status"], "finding status"),
            disposition=_string(item["disposition"], "finding disposition"),
            resolver_or_acceptor=_string(
                item["resolver_or_acceptor"],
                "finding resolver or acceptor",
            ),
            disposition_date=_string(
                item["disposition_date"],
                "finding disposition date",
            ),
            acceptance_rationale=_string(
                item["acceptance_rationale"],
                "finding acceptance rationale",
            ),
        )


@dataclass(frozen=True)
class CompletedWorksheet:
    role: str
    reviewer_identity: str
    review_date: str
    conclusion: str
    post_correction_candidate_sha: str | None
    findings_disposition: str
    findings: tuple[ReviewFinding, ...]
    attestation_sha256: str
    signed_worksheet_sha256: str


@dataclass(frozen=True)
class _WorksheetEvidence:
    path: str
    immutable_locator: str
    retention_owner: str
    sha256: str
    signed_sha256: str
    review_date: str
    conclusion: str
    post_correction_candidate_sha: str | None
    findings_disposition: str
    findings: tuple[ReviewFinding, ...]

    @classmethod
    def from_mapping(cls, value: object) -> _WorksheetEvidence:
        required = (
            "path",
            "immutable_locator",
            "retention_owner",
            "sha256",
            "signed_sha256",
            "review_date",
            "conclusion",
            "findings_disposition",
            "findings",
        )
        item = _mapping(
            value,
            "worksheet evidence",
            required,
            ("post_correction_candidate_sha",),
        )
        conclusion = _string(item["conclusion"], "worksheet conclusion")
        post_correction = item.get("post_correction_candidate_sha")
        if (conclusion == "pass_after_correction") != (
            post_correction is not None
        ):
            raise EvidenceError(
                "worksheet post-correction candidate does not match conclusion"
            )
        return cls(
            path=_string(item["path"], "worksheet path"),
            immutable_locator=_string(
                item["immutable_locator"],
                "worksheet immutable locator",
            ),
            retention_owner=_string(
                item["retention_owner"],
                "worksheet retention owner",
            ),
            sha256=_string(item["sha256"], "worksheet SHA-256"),
            signed_sha256=_string(
                item["signed_sha256"],
                "signed worksheet SHA-256",
            ),
            review_date=_string(item["review_date"], "worksheet review date"),
            conclusion=conclusion,
            post_correction_candidate_sha=(
                _string(post_correction, "post-correction candidate")
                if post_correction is not None
                else None
            ),
            findings_disposition=_string(
                item["findings_disposition"],
                "worksheet findings disposition",
            ),
            findings=tuple(
                ReviewFinding.from_mapping(finding)
                for finding in _sequence(item["findings"], "worksheet findings")
            ),
        )


@dataclass(frozen=True)
class RoleEvidence:
    role: str
    reviewer: ReviewerEvidence
    owner_eligibility_accepted: bool
    dual_role_accepted: bool
    attestation: AttestationEvidence
    worksheet: _WorksheetEvidence

    @property
    def worksheet_findings(self) -> tuple[ReviewFinding, ...]:
        return self.worksheet.findings

    @classmethod
    def from_mapping(cls, value: object) -> RoleEvidence:
        fields = (
            "role",
            "reviewer",
            "owner_eligibility_accepted",
            "dual_role_accepted",
            "attestation",
            "worksheet",
        )
        item = _mapping(value, "role evidence", fields)
        return cls(
            role=_string(item["role"], "review role"),
            reviewer=ReviewerEvidence.from_mapping(item["reviewer"]),
            owner_eligibility_accepted=_boolean(
                item["owner_eligibility_accepted"],
                "owner eligibility acceptance",
            ),
            dual_role_accepted=_boolean(
                item["dual_role_accepted"],
                "dual-role acceptance",
            ),
            attestation=AttestationEvidence.from_mapping(item["attestation"]),
            worksheet=_WorksheetEvidence.from_mapping(item["worksheet"]),
        )


@dataclass(frozen=True)
class _PackageEvidence:
    root: str
    manifest_path: str
    manifest_sha256: str
    immutable_locator: str
    retention_owner: str

    @classmethod
    def from_mapping(cls, value: object) -> _PackageEvidence:
        fields = (
            "root",
            "manifest_path",
            "manifest_sha256",
            "immutable_locator",
            "retention_owner",
        )
        item = _mapping(value, "package evidence", fields)
        return cls(
            root=_string(item["root"], "package root"),
            manifest_path=_string(
                item["manifest_path"],
                "package manifest path",
            ),
            manifest_sha256=_string(
                item["manifest_sha256"],
                "package manifest SHA-256",
            ),
            immutable_locator=_string(
                item["immutable_locator"],
                "package immutable locator",
            ),
            retention_owner=_string(
                item["retention_owner"],
                "package retention owner",
            ),
        )


@dataclass(frozen=True)
class MappingSetEvidence:
    mapping_set_id: str
    package: _PackageEvidence
    roles: tuple[RoleEvidence, ...]

    @classmethod
    def from_mapping(cls, value: object) -> MappingSetEvidence:
        item = _mapping(
            value,
            "mapping-set evidence",
            ("mapping_set_id", "package", "roles"),
        )
        return cls(
            mapping_set_id=_string(
                item["mapping_set_id"],
                "mapping-set identifier",
            ),
            package=_PackageEvidence.from_mapping(item["package"]),
            roles=tuple(
                RoleEvidence.from_mapping(role)
                for role in _sequence(item["roles"], "mapping-set roles")
            ),
        )


@dataclass(frozen=True)
class _DraftCampaignReference:
    campaign_id: str
    candidate_commit: str
    manifest_sha256: str
    seal_record_sha256: str

    @classmethod
    def from_mapping(cls, value: object) -> _DraftCampaignReference:
        fields = (
            "campaign_id",
            "candidate_commit",
            "manifest_sha256",
            "seal_record_sha256",
        )
        item = _mapping(value, "Draft campaign reference", fields)
        return cls(
            campaign_id=_string(item["campaign_id"], "Draft campaign ID"),
            candidate_commit=_string(
                item["candidate_commit"],
                "Draft candidate commit",
            ),
            manifest_sha256=_string(
                item["manifest_sha256"],
                "Draft manifest SHA-256",
            ),
            seal_record_sha256=_string(
                item["seal_record_sha256"],
                "Draft seal-record SHA-256",
            ),
        )


@dataclass(frozen=True)
class CampaignEvidence:
    schema_version: str
    campaign_id: str
    phase: str
    candidate_state: str
    candidate_commit: str
    retention_owner: str
    retention_commitment: str
    mapping_sets: tuple[MappingSetEvidence, ...]
    draft_campaign_reference: _DraftCampaignReference | None

    _REQUIRED: ClassVar[tuple[str, ...]] = (
        "schema_version",
        "campaign_id",
        "phase",
        "candidate_state",
        "candidate_commit",
        "retention_owner",
        "retention_commitment",
        "mapping_sets",
    )

    @classmethod
    def from_mapping(cls, value: object) -> CampaignEvidence:
        item = _mapping(
            value,
            "campaign evidence",
            cls._REQUIRED,
            ("draft_campaign_reference",),
        )
        draft_reference = item.get("draft_campaign_reference")
        return cls(
            schema_version=_string(
                item["schema_version"],
                "campaign schema version",
            ),
            campaign_id=_string(item["campaign_id"], "campaign identifier"),
            phase=_string(item["phase"], "campaign phase"),
            candidate_state=_string(
                item["candidate_state"],
                "campaign candidate state",
            ),
            candidate_commit=_string(
                item["candidate_commit"],
                "campaign candidate commit",
            ),
            retention_owner=_string(
                item["retention_owner"],
                "campaign retention owner",
            ),
            retention_commitment=_string(
                item["retention_commitment"],
                "campaign retention commitment",
            ),
            mapping_sets=tuple(
                MappingSetEvidence.from_mapping(mapping_set)
                for mapping_set in _sequence(
                    item["mapping_sets"],
                    "campaign mapping sets",
                )
            ),
            draft_campaign_reference=(
                _DraftCampaignReference.from_mapping(draft_reference)
                if draft_reference is not None
                else None
            ),
        )


def _decode_markdown(content: bytes, subject: str) -> str:
    if (
        content.startswith(b"\xef\xbb\xbf")
        or b"\r" in content
        or not content.endswith(b"\n")
    ):
        raise EvidenceError(f"{subject} must use canonical UTF-8/LF")
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise EvidenceError(f"{subject} must use canonical UTF-8/LF") from error
    if "\\|" in text:
        raise EvidenceError(f"{subject} contains escaped-pipe ambiguity")
    if "[REQUIRED" in text:
        raise EvidenceError(f"{subject} contains an unresolved template marker")
    return text


def _require_headings(text: str, expected: tuple[str, ...]) -> None:
    headings = tuple(
        line for line in text.splitlines() if line.startswith("#")
    )
    if headings != expected:
        raise EvidenceError("Markdown heading order is invalid")


def _parse_two_column_tables(
    text: str,
    expected_rows: tuple[tuple[str, ...], ...],
) -> tuple[dict[str, str], ...]:
    lines = text.splitlines()
    starts = tuple(
        index
        for index, line in enumerate(lines)
        if line == "| Field | Value |"
    )
    if len(starts) != len(expected_rows):
        raise EvidenceError("Markdown table row structure is invalid")
    tables: list[dict[str, str]] = []
    for start, row_order in zip(starts, expected_rows, strict=True):
        if start + 1 >= len(lines) or lines[start + 1] != "|---|---|":
            raise EvidenceError("Markdown table row structure is invalid")
        rows: dict[str, str] = {}
        cursor = start + 2
        for expected_label in row_order:
            if cursor >= len(lines):
                raise EvidenceError("Markdown table row is missing")
            line = lines[cursor]
            match = re.fullmatch(r"\| ([^|\\]*) \| ([^|\\]*) \|", line)
            if match is None:
                raise EvidenceError("Markdown table row or pipe syntax is invalid")
            label, value = match.groups()
            if label != expected_label:
                raise EvidenceError("Markdown table row order is invalid")
            if not value or value != value.strip():
                raise EvidenceError(f"{label} must be nonempty canonical text")
            rows[label] = value
            cursor += 1
        if cursor < len(lines) and lines[cursor].startswith("|"):
            raise EvidenceError("Markdown table contains an unknown row")
        tables.append(rows)
    return tuple(tables)


def _snake_case(label: str) -> str:
    value = label.casefold()
    value = value.replace("sha-256", "sha256")
    value = value.replace("source checksum(s)", "source checksums")
    value = value.replace("source locator(s)", "source locators")
    value = value.replace("project-owner", "project owner")
    value = value.replace("publication-rights", "publication rights")
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def _require_date(value: str, subject: str) -> None:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise EvidenceError(f"{subject} must be an exact date")
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise EvidenceError(f"{subject} must be an exact date") from error


def _require_digest(value: str, subject: str) -> None:
    if _SHA256.fullmatch(value) is None:
        raise EvidenceError(f"{subject} must be a lowercase SHA-256")


def _require_commit(value: str, subject: str) -> None:
    if _COMMIT_SHA.fullmatch(value) is None:
        raise EvidenceError(f"{subject} must be a full lowercase Git SHA")


def parse_completed_attestation(content: bytes) -> dict[str, str]:
    """Parse one completed attestation using the closed Task 2 grammar."""
    text = _decode_markdown(content, "attestation")
    _require_headings(text, ("# Qualified Reviewer Attestation",))
    (rows,) = _parse_two_column_tables(text, (_ATTESTATION_ROWS,))
    if sum(line.startswith("|") for line in text.splitlines()) != (
        len(_ATTESTATION_ROWS) + 2
    ):
        raise EvidenceError("attestation contains an unknown table row")
    for label in (
        "Authorized source access",
        "Independence from mapper",
        "Conflicts of interest",
        "Project-owner dual-role acceptance",
    ):
        if rows[label] not in {"Yes", "No"}:
            raise EvidenceError(f"{label} has an invalid exact enum")
    if rows["Project-owner eligibility acceptance"] not in {
        "Accepted",
        "Rejected",
    }:
        raise EvidenceError(
            "Project-owner eligibility acceptance has an invalid exact enum"
        )
    if rows["Review role"] not in set(_ROLES.values()):
        raise EvidenceError("review role has an invalid exact enum")
    _require_commit(rows["Candidate commit SHA"], "candidate commit")
    _require_digest(
        rows["Package-manifest SHA-256"],
        "package-manifest digest",
    )
    _require_date(
        rows["Project-owner acceptance date"],
        "project-owner acceptance date",
    )
    _require_date(rows["Date"], "attestation date")

    expected_body = (
        "I attest that I had authorized access to the exact publication "
        "identity,\nsource version, official URL, source checksum(s), and "
        "source locator(s)\nrecorded above: "
        f"{rows['Authorized source access']}.\n\n"
        "I attest that my access and use comply with the recorded "
        "publication-rights\nbasis, permitted elements, prohibited elements, "
        "and restrictions: Yes.\n\n"
        "I attest that I am independent from the mapper: "
        f"{rows['Independence from mapper']}.\n\n"
        "I attest that conflicts of interest and their disposition have been "
        "fully\ndisclosed: Yes.\n\n"
        "I understand that this review does not establish certification, "
        "compliance,\nequivalence, endorsement, or assurance beyond the "
        "relationships expressly\nrecorded in the mapping snapshot.\n"
    )
    if not text.endswith(expected_body):
        raise EvidenceError("attestation body statements do not match the table")
    return {_snake_case(label): value for label, value in rows.items()}


def _parse_findings(text: str) -> tuple[ReviewFinding, ...]:
    lines = text.splitlines()
    header = "| " + " | ".join(_FINDING_COLUMNS) + " |"
    try:
        start = lines.index(header)
    except ValueError as error:
        raise EvidenceError("findings table header is invalid") from error
    separator = "|" + "|".join("---" for _ in _FINDING_COLUMNS) + "|"
    if start + 1 >= len(lines) or lines[start + 1] != separator:
        raise EvidenceError("findings table header is invalid")
    raw_rows: list[tuple[str, ...]] = []
    cursor = start + 2
    while cursor < len(lines) and lines[cursor].startswith("|"):
        line = lines[cursor]
        if not line.startswith("| ") or not line.endswith(" |"):
            raise EvidenceError("findings row or pipe syntax is invalid")
        cells = tuple(line[2:-2].split(" | "))
        if len(cells) != len(_FINDING_COLUMNS):
            raise EvidenceError("findings row or pipe syntax is invalid")
        if any(cell != cell.strip() for cell in cells):
            raise EvidenceError("findings cells must use canonical whitespace")
        raw_rows.append(cells)
        cursor += 1
    if not raw_rows:
        raise EvidenceError("findings table requires a NONE or finding row")
    none_rows = tuple(row for row in raw_rows if row[0] == "NONE")
    if none_rows:
        if len(raw_rows) != 1 or any(none_rows[0][1:]):
            raise EvidenceError("NONE cannot be combined with findings")
        return ()

    findings: list[ReviewFinding] = []
    seen_ids: set[str] = set()
    for row in raw_rows:
        if any(not cell for cell in row):
            raise EvidenceError("finding rows require every cell")
        (
            finding_id,
            affected_text,
            severity,
            description,
            evidence,
            required_action,
            status_value,
            disposition,
            resolver,
            disposition_date,
            rationale,
        ) = row
        affected = tuple(affected_text.split(", "))
        if (
            _IDENTIFIER.fullmatch(finding_id) is None
            or finding_id in seen_ids
            or not affected
            or len(set(affected)) != len(affected)
            or any(_IDENTIFIER.fullmatch(item) is None for item in affected)
        ):
            raise EvidenceError("finding identifiers are invalid or duplicate")
        if severity not in {"Critical", "Important", "Minor"}:
            raise EvidenceError("finding severity has an invalid exact enum")
        if status_value not in {"open", "resolved", "accepted"}:
            raise EvidenceError("finding status has an invalid exact enum")
        if status_value == "accepted" and severity != "Minor":
            raise EvidenceError("only Minor findings may be accepted")
        _require_date(disposition_date, "finding disposition date")
        seen_ids.add(finding_id)
        findings.append(
            ReviewFinding(
                finding_id=finding_id,
                affected_record_ids=affected,
                severity=severity,
                description=description,
                evidence=evidence,
                required_action=required_action,
                status=status_value,
                disposition=disposition,
                resolver_or_acceptor=resolver,
                disposition_date=disposition_date,
                acceptance_rationale=rationale,
            )
        )
    return tuple(findings)


def parse_completed_worksheet(
    content: bytes,
    role: str,
) -> CompletedWorksheet:
    """Parse a completed role worksheet using the closed Task 2 grammar."""
    if role not in _ROLES:
        raise EvidenceError("review role is unsupported")
    text = _decode_markdown(content, "worksheet")
    title = (
        "# Specification and Inventory Review Worksheet"
        if role == "specification_and_inventory"
        else "# Security and Overclaiming Review Worksheet"
    )
    _require_headings(
        text,
        (
            title,
            "## Review identification",
            "## Review scope",
            "## Findings",
            "## Overall conclusion",
            "## Worksheet signature",
        ),
    )
    identification, conclusion_rows, signature = _parse_two_column_tables(
        text,
        (
            _WORKSHEET_IDENTIFICATION_ROWS,
            _CONCLUSION_ROWS,
            _SIGNATURE_ROWS,
        ),
    )
    if identification["Review role"] != _ROLES[role]:
        raise EvidenceError("review role does not match worksheet")
    _require_commit(
        identification["Candidate commit SHA"],
        "candidate commit",
    )
    _require_digest(
        identification["Package-manifest SHA-256"],
        "package-manifest digest",
    )
    _require_digest(
        identification["Attestation SHA-256"],
        "attestation digest",
    )
    _require_date(identification["Review date"], "review date")
    _require_date(signature["Signature date"], "signature date")
    _require_digest(
        signature["Signed worksheet SHA-256"],
        "signed worksheet digest",
    )
    conclusion = conclusion_rows["Overall conclusion"]
    if conclusion not in {"pass", "pass_after_correction", "stop"}:
        raise EvidenceError("worksheet conclusion has an invalid exact enum")
    post_correction_text = conclusion_rows["Post-correction candidate SHA"]
    if conclusion == "pass_after_correction":
        _require_commit(post_correction_text, "post-correction candidate")
        post_correction: str | None = post_correction_text
    elif post_correction_text == "Not applicable":
        post_correction = None
    else:
        raise EvidenceError(
            "post-correction candidate does not match conclusion"
        )
    findings = _parse_findings(text)
    expected_pipe_lines = (
        len(_WORKSHEET_IDENTIFICATION_ROWS)
        + len(_CONCLUSION_ROWS)
        + len(_SIGNATURE_ROWS)
        + 8
        + (len(findings) or 1)
    )
    if sum(line.startswith("|") for line in text.splitlines()) != (
        expected_pipe_lines
    ):
        raise EvidenceError("worksheet contains an unknown table row")
    return CompletedWorksheet(
        role=role,
        reviewer_identity=identification["Reviewer identity"],
        review_date=identification["Review date"],
        conclusion=conclusion,
        post_correction_candidate_sha=post_correction,
        findings_disposition=conclusion_rows[
            "Reviewer metadata findings disposition"
        ],
        findings=findings,
        attestation_sha256=identification["Attestation SHA-256"],
        signed_worksheet_sha256=signature["Signed worksheet SHA-256"],
    )


def signed_worksheet_sha256(content: bytes) -> str:
    """Hash a canonical worksheet after excluding its one signed-digest row."""
    _decode_markdown(content, "worksheet")
    row_pattern = re.compile(
        rb"^\| Signed worksheet SHA-256 \| [^|\r\n]+ \|\n$"
    )
    rows = tuple(
        line
        for line in content.splitlines(keepends=True)
        if row_pattern.fullmatch(line)
    )
    if len(rows) != 1:
        raise EvidenceError(
            "worksheet must contain exactly one signed worksheet digest row"
        )
    return hashlib.sha256(content.replace(rows[0], b"", 1)).hexdigest()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _canonical_relative_path(value: str, subject: str) -> PurePosixPath:
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if (
        not value
        or "\\" in value
        or posix.is_absolute()
        or windows.is_absolute()
        or bool(windows.drive)
        or any(part in {"", ".", ".."} for part in value.split("/"))
        or any(
            re.fullmatch(r"[A-Za-z0-9._-]+", part) is None
            for part in value.split("/")
        )
        or posix.as_posix() != value
    ):
        raise EvidenceError(f"{subject} is not a canonical relative path")
    return posix


def _is_alias(path: Path, mode: int) -> bool:
    if stat.S_ISLNK(mode):
        return True
    file_attributes = getattr(path.lstat(), "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if reparse_flag and file_attributes & reparse_flag:
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction is not None and is_junction())


def _inspect_lexical_entry(path: Path, subject: str) -> int:
    try:
        result = path.lstat()
        if _is_alias(path, result.st_mode):
            raise EvidenceError(f"{subject} must not use a filesystem alias")
        return result.st_mode
    except EvidenceError:
        raise
    except FileNotFoundError as error:
        raise EvidenceError(f"{subject} is missing") from error
    except OSError as error:
        raise EvidenceError(f"{subject} cannot be inspected") from error


def _require_canonical_case(root: Path, relative: PurePosixPath) -> None:
    current = root
    accumulated: list[str] = []
    for part in relative.parts:
        accumulated.append(part)
        subject = "/".join(accumulated)
        try:
            matches = tuple(
                entry.name
                for entry in current.iterdir()
                if entry.name.casefold() == part.casefold()
            )
        except OSError as error:
            raise EvidenceError(f"{subject} cannot be inspected") from error
        if len(matches) > 1:
            raise EvidenceError(
                f"{subject} has a case-insensitive path collision"
            )
        if matches and matches[0] != part:
            raise EvidenceError(f"{subject} does not use canonical casing")
        current = current / part


def resolve_external_regular_file(
    root: Path,
    relative: str,
    worktrees: tuple[Path, ...],
) -> Path:
    """Resolve one canonical, unaliased, single-link external regular file."""
    canonical = _canonical_relative_path(relative, "evidence path")
    _inspect_lexical_entry(root, "campaign root")
    _require_canonical_case(root, canonical)

    candidate = root.joinpath(*canonical.parts)
    current = root
    for index, part in enumerate(canonical.parts):
        current /= part
        subject = "/".join(canonical.parts[: index + 1])
        _inspect_lexical_entry(current, subject)

    try:
        resolved_root = root.resolve(strict=True)
        resolved = candidate.resolve(strict=True)
        resolved_worktrees = tuple(
            worktree.resolve(strict=True) for worktree in worktrees
        )
    except (OSError, RuntimeError) as error:
        raise EvidenceError(f"{relative} cannot be resolved") from error

    if not _is_within(resolved, resolved_root):
        raise EvidenceError(f"{relative} escapes the campaign root")
    if any(_is_within(resolved, worktree) for worktree in resolved_worktrees):
        raise EvidenceError(
            f"{relative} must be outside every Git worktree"
        )

    try:
        stat_result = candidate.stat(follow_symlinks=False)
    except FileNotFoundError as error:
        raise EvidenceError(f"{relative} is missing") from error
    except OSError as error:
        raise EvidenceError(f"{relative} cannot be inspected") from error
    if not stat.S_ISREG(stat_result.st_mode):
        raise EvidenceError(f"{relative} must be a regular file")
    if (
        not hasattr(stat_result, "st_nlink")
        or stat_result.st_nlink != 1
    ):
        raise EvidenceError(
            f"{relative} must have exactly one filesystem link"
        )
    return resolved


def canonical_json_bytes(value: object) -> bytes:
    """Serialize canonical one-line sorted JSON with a terminating LF."""
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise EvidenceError("value is not canonical JSON data") from error
    return (text + "\n").encode("utf-8")


def _campaign_tree_entries(
    root: Path,
    expected_directories: set[str],
) -> tuple[str, ...]:
    _inspect_lexical_entry(root, "campaign root")
    try:
        root_mode = root.stat(follow_symlinks=False).st_mode
    except OSError as error:
        raise EvidenceError("campaign root cannot be inspected") from error
    if not stat.S_ISDIR(root_mode):
        raise EvidenceError("campaign root must be a directory")

    files: list[str] = []
    pending: list[tuple[Path, str]] = [(root, "")]
    seen_casefold: dict[str, str] = {}
    while pending:
        directory, prefix = pending.pop()
        try:
            entries = tuple(os.scandir(directory))
        except OSError as error:
            subject = prefix or "campaign root"
            raise EvidenceError(f"{subject} cannot be inspected") from error
        component_names: dict[str, str] = {}
        for entry in entries:
            folded_name = entry.name.casefold()
            if (
                folded_name in component_names
                and component_names[folded_name] != entry.name
            ):
                raise EvidenceError(
                    f"{prefix or 'campaign root'} has a "
                    "case-insensitive path collision"
                )
            component_names[folded_name] = entry.name
        for entry in entries:
            relative = f"{prefix}/{entry.name}" if prefix else entry.name
            canonical = _canonical_relative_path(relative, "campaign entry")
            if canonical.as_posix() != relative:
                raise EvidenceError(f"{relative} is not a canonical path")
            folded = relative.casefold()
            prior = seen_casefold.get(folded)
            if prior is not None and prior != relative:
                raise EvidenceError(
                    f"{relative} has a case-insensitive path collision"
                )
            seen_casefold[folded] = relative
            path = Path(entry.path)
            mode = _inspect_lexical_entry(path, relative)
            if stat.S_ISDIR(mode):
                if relative not in expected_directories:
                    raise EvidenceError(
                        f"{relative} is outside the campaign allowlist"
                    )
                pending.append((path, relative))
            else:
                files.append(relative)
    return tuple(files)


def build_campaign_archive(
    root: Path,
    allowlist: tuple[str, ...],
) -> bytes:
    """Build a deterministic ZIP containing exactly the safe allowlisted files."""
    canonical_paths: list[str] = []
    seen: set[str] = set()
    for relative in allowlist:
        canonical = _canonical_relative_path(relative, "archive entry")
        normalized = canonical.as_posix()
        folded = normalized.casefold()
        if folded in seen:
            raise EvidenceError(
                "archive allowlist has a duplicate case-insensitive path"
            )
        if canonical.name == "CAMPAIGN_SEAL.json":
            raise EvidenceError("campaign seal must remain outside the archive")
        seen.add(folded)
        canonical_paths.append(normalized)
    expected_files = set(canonical_paths)
    expected_directories = {
        "/".join(PurePosixPath(relative).parts[:index])
        for relative in canonical_paths
        for index in range(1, len(PurePosixPath(relative).parts))
    }
    actual_files = set(_campaign_tree_entries(root, expected_directories))
    if actual_files != expected_files:
        raise EvidenceError("campaign tree does not match the exact allowlist")

    payloads: list[tuple[str, bytes]] = []
    for relative in sorted(canonical_paths):
        resolved = resolve_external_regular_file(root, relative, ())
        try:
            content = resolved.read_bytes()
        except OSError as error:
            raise EvidenceError(f"{relative} cannot be read") from error
        payloads.append((relative, content))

    output = io.BytesIO()
    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_STORED,
        strict_timestamps=True,
    ) as archive:
        for relative, content in payloads:
            info = zipfile.ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.internal_attr = 0
            info.extra = b""
            info.comment = b""
            archive.writestr(info, content)
    return output.getvalue()


def _require_immutable_locator(value: str, subject: str) -> None:
    if re.fullmatch(r"urn:sha256:[0-9a-f]{64}", value):
        return
    if _HTTPS_LOCATOR.fullmatch(value) is None:
        raise EvidenceError(f"{subject} is not an immutable locator")
    try:
        parsed = urlsplit(value)
        query = parse_qsl(parsed.query, keep_blank_values=True)
        port = parsed.port
    except ValueError as error:
        raise EvidenceError(f"{subject} is not an immutable locator") from error
    immutable_keys = {"version", "versionId", "generation", "rev", "sha256"}
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or port is not None and not 1 <= port <= 65535
        or not any(key in immutable_keys and value for key, value in query)
        or any(character in value for character in "\r\n")
    ):
        raise EvidenceError(f"{subject} is not an immutable locator")


def build_seal_record(
    *,
    manifest_bytes: bytes,
    archive_bytes: bytes,
    archive_locator: str,
    campaign_id: str,
    candidate_commit: str,
    evidence_valid: bool,
    readiness_name: str,
    readiness_value: bool,
    validator_version: str,
) -> tuple[dict[str, object], bytes]:
    """Build the exact external, non-self-referential 1.0.0 seal record."""
    if type(manifest_bytes) is not bytes or type(archive_bytes) is not bytes:
        raise EvidenceError("manifest and archive inputs must be bytes")
    for value, subject in (
        (archive_locator, "archive locator"),
        (campaign_id, "campaign identifier"),
        (candidate_commit, "candidate commit"),
        (readiness_name, "readiness name"),
        (validator_version, "validator version"),
    ):
        if type(value) is not str:
            raise EvidenceError(f"{subject} must be a string")
    if type(evidence_valid) is not bool or type(readiness_value) is not bool:
        raise EvidenceError("validation and readiness values must be Boolean")
    _require_commit(candidate_commit, "candidate commit")
    _require_immutable_locator(archive_locator, "archive locator")
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", campaign_id) is None:
        raise EvidenceError("campaign identifier is invalid")
    if readiness_name not in {"transition_ready", "merge_ready"}:
        raise EvidenceError("readiness name is invalid")
    if (
        not validator_version
        or validator_version != validator_version.strip()
        or "\r" in validator_version
        or "\n" in validator_version
    ):
        raise EvidenceError("validator version is invalid")

    record: dict[str, object] = {
        "archive_byte_length": len(archive_bytes),
        "archive_format": "zip",
        "archive_locator": archive_locator,
        "archive_media_type": "application/zip",
        "archive_sha256": hashlib.sha256(archive_bytes).hexdigest(),
        "campaign_id": campaign_id,
        "candidate_commit": candidate_commit,
        "evidence_valid": evidence_valid,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "readiness_name": readiness_name,
        "readiness_value": readiness_value,
        "schema_version": "1.0.0",
        "validator_version": validator_version,
    }
    return record, canonical_json_bytes(record)
