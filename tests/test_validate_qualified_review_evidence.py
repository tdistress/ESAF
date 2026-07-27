from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile

import yaml

import tools.validate_crosswalks as crosswalk_validator
import tools.seal_qualified_review_campaign as seal_module
from tools.build_mapping_review_bundle import (
    PROFILES,
    GitReader,
    PackageAssembly,
    assemble_package,
    parse_front_matter_bytes,
)
from tools.crosswalks.digests import snapshot_digest_from_files
from tools.crosswalks.qualified_review_evidence import (
    build_campaign_archive,
    build_seal_record,
    canonical_json_bytes,
    signed_worksheet_sha256,
)
from tools.seal_qualified_review_campaign import main as seal_main
from tools.validate_qualified_review_evidence import (
    VALIDATOR_VERSION,
    ValidationReport,
    main,
    validate_campaign,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = "REVIEW_EVIDENCE.json"
ROLES = (
    "specification_and_inventory",
    "security_and_overclaiming",
)
ROLE_LABELS = {
    "specification_and_inventory": "Specification and inventory review",
    "security_and_overclaiming": "Security and overclaiming review",
}
PROFILE_NAMES = {
    "Core": "core",
    "Plus forward": "plus-forward",
    "Plus reverse": "plus-reverse",
}
LOCATOR = f"urn:sha256:{'b' * 64}"
REVIEW_DATE = "2026-07-25"


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _table(rows: tuple[tuple[str, str], ...]) -> str:
    return "\n".join(
        (
            "| Field | Value |",
            "|---|---|",
            *(f"| {label} | {value} |" for label, value in rows),
        )
    )


def _reviewer(profile_name: str, role: str) -> dict[str, object]:
    discipline = (
        "inventory"
        if role == "specification_and_inventory"
        else "security"
    )
    return {
        "identity": f"{profile_name} {discipline} reviewer",
        "organization": "Example Assurance Ltd",
        "verification_locator": (
            "https://identity.example.invalid/reviewer"
            f"?version={profile_name}-{discipline}"
        ),
        "qualification": f"Qualified {discipline} mapping reviewer",
        "authorized_source_access": True,
        "independent": True,
        "conflicts": False,
        "conflict_disposition": "Not applicable",
    }


def _reviewer_object(profile_name: str, role: str) -> dict[str, object]:
    reviewer = _reviewer(profile_name, role)
    return {
        "id": reviewer["identity"],
        "date": REVIEW_DATE,
        "qualification": reviewer["qualification"],
        "authorized_source_access": True,
        "findings_disposition": "No findings",
    }


def _attestation_text(
    *,
    mapping_set_id: str,
    candidate: str,
    package: dict[str, object],
    role: dict[str, object],
    publication: dict[str, object],
) -> bytes:
    reviewer = role["reviewer"]
    attestation = role["attestation"]
    assert isinstance(reviewer, dict)
    assert isinstance(attestation, dict)
    conflicts = "Yes" if reviewer["conflicts"] else "No"
    authorized = "Yes" if reviewer["authorized_source_access"] else "No"
    independent = "Yes" if reviewer["independent"] else "No"
    dual_role = "Yes" if role["dual_role_accepted"] else "No"
    eligibility = (
        "Accepted" if role["owner_eligibility_accepted"] else "Rejected"
    )
    rows = (
        ("Reviewer identity", str(reviewer["identity"])),
        ("Organization", str(reviewer["organization"])),
        ("Verification locator", str(reviewer["verification_locator"])),
        ("Mapping-set identifier", mapping_set_id),
        ("Candidate commit SHA", candidate),
        ("Package root", str(package["root"])),
        ("Package manifest path", str(package["manifest_path"])),
        ("Package-manifest SHA-256", str(package["manifest_sha256"])),
        ("Package immutable locator", str(package["immutable_locator"])),
        ("Package retention owner", str(package["retention_owner"])),
        ("Attestation path", str(attestation["path"])),
        (
            "Attestation immutable locator",
            str(attestation["immutable_locator"]),
        ),
        ("Attestation retention owner", str(attestation["retention_owner"])),
        ("Review role", ROLE_LABELS[str(role["role"])]),
        ("Publication identity", str(publication["publication_identity"])),
        ("Exact source version", str(publication["source_version"])),
        ("Official URL", str(publication["official_url"])),
        ("Source checksum(s)", str(publication["source_checksums"])),
        ("Source locator(s)", str(publication["source_locators"])),
        (
            "Publication-rights basis",
            str(publication["publication_rights_basis"]),
        ),
        ("Permitted elements", str(publication["permitted_elements"])),
        ("Prohibited elements", str(publication["prohibited_elements"])),
        ("Restrictions", str(publication["restrictions"])),
        ("Qualification", str(reviewer["qualification"])),
        ("Authorized source access", authorized),
        ("Independence from mapper", independent),
        ("Conflicts of interest", conflicts),
        ("Conflict disposition", str(reviewer["conflict_disposition"])),
        ("Project-owner eligibility acceptance", eligibility),
        ("Project-owner dual-role acceptance", dual_role),
        ("Project-owner identity", "Project Owner"),
        ("Project-owner signature", "Project Owner / signed"),
        ("Project-owner acceptance date", REVIEW_DATE),
        ("Source-content exclusion", "Yes"),
        (
            "Source-content exclusion signature",
            f"{reviewer['identity']} / separately signed",
        ),
        ("Source-content exclusion date", REVIEW_DATE),
        ("Signature", f"{reviewer['identity']} / signed"),
        ("Date", REVIEW_DATE),
    )
    return (
        "# Qualified Reviewer Attestation\n\n"
        "An unsigned blank form is not review evidence.\n\n"
        f"{_table(rows)}\n\n"
        "Every table value shall be single-line text without an unescaped pipe\n"
        "character. Do not add, remove, duplicate, or reorder rows.\n\n"
        "I attest that I had authorized access to the exact publication identity,\n"
        "source version, official URL, source checksum(s), and source locator(s)\n"
        f"recorded above: {authorized}.\n\n"
        "I attest that my access and use comply with the recorded publication-rights\n"
        "basis, permitted elements, prohibited elements, and restrictions: Yes.\n\n"
        f"I attest that I am independent from the mapper: {independent}.\n\n"
        "I attest that conflicts of interest and their disposition have been fully\n"
        "disclosed: Yes.\n\n"
        "I separately attest that the reviewer-authored attestation and worksheet\n"
        "contain no copied or close-paraphrased source passage or other licensed "
        "source\n"
        "text, and use source material only through the recorded identifiers, "
        "checksums,\n"
        "locators, and concise reviewer analysis: Yes.\n\n"
        "I understand that this review does not establish certification, compliance,\n"
        "equivalence, endorsement, or assurance beyond the relationships expressly\n"
        "recorded in the mapping snapshot.\n"
    ).encode("utf-8")


def _findings_table(findings: list[dict[str, object]]) -> str:
    header = (
        "| Finding ID | Affected record IDs | Severity | Description | "
        "Evidence | Required action | Status | Disposition | "
        "Resolver or acceptor | Disposition date | Acceptance rationale |"
    )
    separator = "|" + "|".join("---" for _ in range(11)) + "|"
    if not findings:
        rows = ("| NONE |  |  |  |  |  |  |  |  |  |  |",)
    else:
        rows = tuple(
            "| "
            + " | ".join(
                (
                    str(finding["finding_id"]),
                    ", ".join(finding["affected_record_ids"]),
                    str(finding["severity"]),
                    str(finding.get("description", "Reviewed finding")),
                    str(finding.get("evidence", "Signed review evidence")),
                    str(finding.get("required_action", "Apply disposition")),
                    str(finding["status"]),
                    str(finding["disposition"]),
                    str(finding["resolver_or_acceptor"]),
                    str(finding["disposition_date"]),
                    str(finding["acceptance_rationale"]),
                )
            )
            + " |"
            for finding in findings
        )
    return "\n".join((header, separator, *rows))


def _worksheet_text(
    *,
    mapping_set_id: str,
    candidate: str,
    package: dict[str, object],
    role: dict[str, object],
    expected_count: int,
) -> bytes:
    reviewer = role["reviewer"]
    attestation = role["attestation"]
    worksheet = role["worksheet"]
    assert isinstance(reviewer, dict)
    assert isinstance(attestation, dict)
    assert isinstance(worksheet, dict)
    role_name = str(role["role"])
    specification = role_name == "specification_and_inventory"
    title = (
        "# Specification and Inventory Review Worksheet"
        if specification
        else "# Security and Overclaiming Review Worksheet"
    )
    coverage = (
        f"All {expected_count} provisions and mapping records"
        if specification
        else f"All {expected_count} relationships"
    )
    method = (
        "Requirement-level inspection"
        if specification
        else "Normative-text comparison"
    )
    identification = (
        ("Mapping-set identifier", mapping_set_id),
        ("Candidate commit SHA", candidate),
        ("Package root", str(package["root"])),
        ("Package manifest path", str(package["manifest_path"])),
        ("Package-manifest SHA-256", str(package["manifest_sha256"])),
        ("Package immutable locator", str(package["immutable_locator"])),
        ("Package retention owner", str(package["retention_owner"])),
        ("Reviewer identity", str(reviewer["identity"])),
        ("Attestation path", str(attestation["path"])),
        (
            "Attestation immutable locator",
            str(attestation["immutable_locator"]),
        ),
        ("Attestation retention owner", str(attestation["retention_owner"])),
        ("Attestation SHA-256", str(attestation["sha256"])),
        ("Worksheet path", str(worksheet["path"])),
        ("Worksheet immutable locator", str(worksheet["immutable_locator"])),
        ("Worksheet retention owner", str(worksheet["retention_owner"])),
        ("Review role", ROLE_LABELS[role_name]),
        ("Review date", str(worksheet["review_date"])),
        ("Coverage summary", coverage),
        ("Review method", method),
        ("Provision coverage", f"{expected_count} provisions"),
        ("Mapping-record coverage", f"{expected_count} mapping records"),
    )
    if specification:
        scope = """Make and record an explicit determination for each of:

- source identity, version, checksum, and official locator;
- Publication rights;
- Provision population;
- provision identifiers;
- provision hierarchy;
- provision granularity;
- provision coverage;
- predecessor integrity;
- absence of omitted, duplicated, invented, or wrong-version provisions;
- record, catalog, and registry agreement; and
- change history."""
    else:
        scope = """Verify:

- relationship direction and type;
- coverage and confidence;
- conditions;
- expected evidence;
- known gaps;
- `no_direct_mapping`;
- `prerequisite`;
- `partially_supports`;
- normative-text basis; and
- that conditions cannot create a missing external outcome;
- that implementation guidance or adjacent capabilities cannot replace
  normative requirements; and
- nonclaims, including certification, compliance, equivalence, endorsement,
  and assurance."""
    post_correction = worksheet.get(
        "post_correction_candidate_sha",
        "Not applicable",
    )
    conclusion = (
        ("Overall conclusion", str(worksheet["conclusion"])),
        ("Post-correction candidate SHA", str(post_correction)),
        (
            "Reviewer metadata findings disposition",
            str(worksheet["findings_disposition"]),
        ),
    )
    signature = (
        ("Reviewer signature", f"{reviewer['identity']} / signed"),
        ("Signature date", str(worksheet["review_date"])),
        ("Signed worksheet SHA-256", "0" * 64),
    )
    text = (
        f"{title}\n\n"
        "## Review identification\n\n"
        f"{_table(identification)}\n\n"
        "Every table value shall be single-line text without an unescaped pipe\n"
        "character. Do not add, remove, duplicate, or reorder rows.\n\n"
        "## Review scope\n\n"
        f"{scope}\n\n"
        "## Findings\n\n"
        "Critical and Important findings cannot be accepted and must be resolved.\n"
        "Only Minor findings may be accepted, with a named acceptor, acceptance\n"
        "rationale, and disposition date.\n\n"
        f"{_findings_table(worksheet['findings'])}\n\n"
        "## Overall conclusion\n\n"
        f"{_table(conclusion)}\n\n"
        "## Worksheet signature\n\n"
        f"{_table(signature)}\n\n"
        "Digest procedure: encode the completed worksheet as UTF-8 without BOM and LF\n"
        "line endings after all other fields, including the reviewer signature and\n"
        "signature date, are final. For the digest calculation, remove the entire\n"
        "`| Signed worksheet SHA-256 |` table row, including its terminating LF, and\n"
        "hash every remaining byte with SHA-256. Record the lowercase hexadecimal\n"
        "digest in that row; verification repeats the same exclusion. No non-excluded\n"
        "byte may change after the digest is recorded.\n"
    ).encode("utf-8")
    digest = signed_worksheet_sha256(text)
    return text.replace(b"0" * 64, digest.encode("ascii"), 1)


class CampaignFixture:
    def __init__(
        self,
        root: Path,
        candidate: str,
        assemblies: dict[str, PackageAssembly],
        *,
        phase: str = "draft_review",
        campaign_id: str = "issue-55-draft-review",
        draft_campaign_reference: dict[str, object] | None = None,
    ) -> None:
        self.root = root
        self.candidate = candidate
        self.assemblies = assemblies
        self.phase = phase
        self.campaign_id = campaign_id
        self.candidate_state = (
            "reviewed"
            if phase == "final_reviewed_confirmation"
            else "draft"
        )
        self.manifest: dict[str, object] = {
            "schema_version": "1.0.0",
            "campaign_id": campaign_id,
            "phase": phase,
            "candidate_state": self.candidate_state,
            "candidate_commit": candidate,
            "retention_owner": "ESAF Project Owner",
            "retention_commitment": "Retain every sealed campaign byte.",
            "mapping_sets": [],
        }
        if draft_campaign_reference is not None:
            self.manifest["draft_campaign_reference"] = (
                draft_campaign_reference
            )
        self._write_packages_and_roles()
        self.write_manifest()

    def _write_packages_and_roles(self) -> None:
        mapping_sets = self.manifest["mapping_sets"]
        assert isinstance(mapping_sets, list)
        for profile in PROFILES.values():
            assembly = self.assemblies[profile.mapping_set_id]
            profile_name = PROFILE_NAMES[profile.label]
            package_root = f"packages/{profile_name}"
            for payload in assembly.payloads:
                self.write(f"{package_root}/{payload.path}", payload.content)
            manifest_path = f"{package_root}/PACKAGE_MANIFEST.json"
            self.write(manifest_path, assembly.manifest_bytes)
            package = {
                "root": package_root,
                "manifest_path": manifest_path,
                "manifest_sha256": hashlib.sha256(
                    assembly.manifest_bytes
                ).hexdigest(),
                "immutable_locator": (
                    "https://evidence.example.invalid/package"
                    f"?version={profile_name}"
                ),
                "retention_owner": "Records Owner",
            }
            mapping_set = {
                "mapping_set_id": profile.mapping_set_id,
                "package": package,
                "roles": [],
            }
            mapping_sets.append(mapping_set)
            for role_name in ROLES:
                role = {
                    "role": role_name,
                    "reviewer": _reviewer(profile_name, role_name),
                    "owner_eligibility_accepted": True,
                    "dual_role_accepted": False,
                    "attestation": {
                        "path": f"attestations/{profile_name}-{role_name}.md",
                        "immutable_locator": (
                            "https://evidence.example.invalid/attestation"
                            f"?version={profile_name}-{role_name}"
                        ),
                        "retention_owner": "Records Owner",
                        "sha256": "0" * 64,
                    },
                    "worksheet": {
                        "path": f"worksheets/{profile_name}-{role_name}.md",
                        "immutable_locator": (
                            "https://evidence.example.invalid/worksheet"
                            f"?version={profile_name}-{role_name}"
                        ),
                        "retention_owner": "Records Owner",
                        "sha256": "0" * 64,
                        "signed_sha256": "0" * 64,
                        "review_date": REVIEW_DATE,
                        "conclusion": "pass",
                        "findings_disposition": "No findings",
                        "findings": [],
                    },
                }
                mapping_set["roles"].append(role)
                self.write_role(profile, mapping_set, role)

    def _publication(
        self,
        profile_id: str,
    ) -> dict[str, object]:
        assembly = self.assemblies[profile_id]
        mapping_file = next(
            payload for payload in assembly.payloads
            if payload.purpose == "mapping set"
        )
        metadata, _body = parse_front_matter_bytes(mapping_file.content)
        rights = metadata["publication_rights"]
        assert isinstance(rights, dict)
        prohibited = rights["prohibited_elements"]
        assert isinstance(prohibited, list)
        variants: list[dict[str, object]] = []
        for payload in assembly.payloads:
            if payload.purpose != "source evidence pin":
                continue
            evidence = json.loads(payload.content)
            source = evidence["source"]
            assert isinstance(source, dict)
            payload_variants = source["variants"]
            assert isinstance(payload_variants, list)
            variants.extend(
                variant
                for variant in payload_variants
                if isinstance(variant, dict)
            )
        if variants:
            source_checksums = ", ".join(
                sorted({str(variant["sha256"]) for variant in variants})
            )
            source_locators = ", ".join(
                sorted({str(variant["url"]) for variant in variants})
            )
        else:
            source_section = _body.split(
                "## Source and publication rights\n",
                1,
            )[1].split("\n## ", 1)[0]
            pinned = re.findall(
                r"SHA-256 `([0-9a-f]{64})`",
                source_section,
            )
            assert len(pinned) == 1
            source_checksums = pinned[0]
            source_locators = str(metadata["source"]["official_url"])
        return {
            "publication_identity": metadata["publication"]["name"],
            "source_version": metadata["source_version"]["id"],
            "official_url": metadata["source"]["official_url"],
            "source_checksums": source_checksums,
            "source_locators": source_locators,
            "publication_rights_basis": rights["basis"],
            "permitted_elements": ", ".join(rights["permitted_elements"]),
            "prohibited_elements": (
                ", ".join(prohibited) if prohibited else "None"
            ),
            "restrictions": rights["restrictions"],
        }

    def write_role(
        self,
        profile: object,
        mapping_set: dict[str, object],
        role: dict[str, object],
    ) -> None:
        package = mapping_set["package"]
        attestation = role["attestation"]
        worksheet = role["worksheet"]
        assert isinstance(package, dict)
        assert isinstance(attestation, dict)
        assert isinstance(worksheet, dict)
        attestation_content = _attestation_text(
            mapping_set_id=str(mapping_set["mapping_set_id"]),
            candidate=self.candidate,
            package=package,
            role=role,
            publication=self._publication(str(mapping_set["mapping_set_id"])),
        )
        attestation["sha256"] = hashlib.sha256(
            attestation_content
        ).hexdigest()
        self.write(str(attestation["path"]), attestation_content)
        worksheet_content = _worksheet_text(
            mapping_set_id=str(mapping_set["mapping_set_id"]),
            candidate=self.candidate,
            package=package,
            role=role,
            expected_count=profile.expected_count,
        )
        worksheet["signed_sha256"] = signed_worksheet_sha256(
            worksheet_content
        )
        worksheet["sha256"] = hashlib.sha256(worksheet_content).hexdigest()
        self.write(str(worksheet["path"]), worksheet_content)

    def write_manifest(self) -> None:
        self.write(MANIFEST_PATH, canonical_json_bytes(self.manifest))

    def write(self, relative: str, content: bytes) -> None:
        path = self.root.joinpath(*relative.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


class CampaignValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.shared_temporary = tempfile.TemporaryDirectory()
        cls.shared_root = Path(cls.shared_temporary.name)
        cls.repository = cls.shared_root / "candidate"
        subprocess.run(
            [
                "git",
                "clone",
                "--shared",
                "--no-checkout",
                str(ROOT),
                str(cls.repository),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.candidate = _git(ROOT, "rev-parse", "HEAD")
        _git(cls.repository, "checkout", "--detach", cls.candidate)
        cls.reader = GitReader(cls.repository)
        cls.assemblies = {
            profile.mapping_set_id: assemble_package(
                cls.reader,
                cls.candidate,
                profile,
            )
            for profile in PROFILES.values()
        }
        cls.pristine_campaign = cls.shared_root / "pristine-draft"
        cls.pristine_campaign.mkdir()
        CampaignFixture(
            cls.pristine_campaign,
            cls.candidate,
            cls.assemblies,
        )
        cls.draft_allowlist = tuple(
            sorted(
                path.relative_to(cls.pristine_campaign).as_posix()
                for path in cls.pristine_campaign.rglob("*")
                if path.is_file()
            )
        )
        cls.draft_archive_bytes = build_campaign_archive(
            cls.pristine_campaign,
            cls.draft_allowlist,
        )
        draft_manifest_bytes = (
            cls.pristine_campaign / MANIFEST_PATH
        ).read_bytes()
        (
            cls.draft_seal,
            cls.draft_seal_bytes,
        ) = build_seal_record(
            manifest_bytes=draft_manifest_bytes,
            archive_bytes=cls.draft_archive_bytes,
            archive_locator=(
                "https://evidence.example.invalid/draft.zip?version=1"
            ),
            campaign_id="issue-55-draft-review",
            candidate_commit=cls.candidate,
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            validator_version=VALIDATOR_VERSION,
        )
        cls.draft_seal_path = cls.shared_root / "CAMPAIGN_SEAL.json"
        cls.draft_archive_path = cls.shared_root / "CAMPAIGN_ARCHIVE.zip"
        cls.draft_seal_path.write_bytes(cls.draft_seal_bytes)
        cls.draft_archive_path.write_bytes(cls.draft_archive_bytes)

        cls.reviewed_repository = cls.shared_root / "reviewed-candidate"
        subprocess.run(
            [
                "git",
                "clone",
                "--shared",
                "--no-checkout",
                str(ROOT),
                str(cls.reviewed_repository),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        _git(
            cls.reviewed_repository,
            "checkout",
            "-b",
            "reviewed-fixture",
            cls.candidate,
        )
        _git(cls.reviewed_repository, "config", "user.name", "ESAF Test")
        _git(
            cls.reviewed_repository,
            "config",
            "user.email",
            "esaf-test@example.invalid",
        )
        cls._make_reviewed_candidate()
        _git(cls.reviewed_repository, "add", "--all")
        _git(
            cls.reviewed_repository,
            "commit",
            "-m",
            "reviewed fixture",
        )
        cls.reviewed_candidate = _git(
            cls.reviewed_repository,
            "rev-parse",
            "HEAD",
        )
        cls.reviewed_reader = GitReader(cls.reviewed_repository)
        cls.reviewed_assemblies = {
            profile.mapping_set_id: assemble_package(
                cls.reviewed_reader,
                cls.reviewed_candidate,
                profile,
                "reviewed",
            )
            for profile in PROFILES.values()
        }
        cls.draft_reference = {
            "campaign_id": "issue-55-draft-review",
            "candidate_commit": cls.candidate,
            "manifest_sha256": hashlib.sha256(
                draft_manifest_bytes
            ).hexdigest(),
            "seal_record_sha256": hashlib.sha256(
                cls.draft_seal_bytes
            ).hexdigest(),
        }
        cls.pristine_final_campaign = cls.shared_root / "pristine-final"
        cls.pristine_final_campaign.mkdir()
        CampaignFixture(
            cls.pristine_final_campaign,
            cls.reviewed_candidate,
            cls.reviewed_assemblies,
            phase="final_reviewed_confirmation",
            campaign_id="issue-55-final-confirmation",
            draft_campaign_reference=cls.draft_reference,
        )
        cls._make_finding_candidates()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.shared_temporary.cleanup()

    @classmethod
    def _write_front_matter(
        cls,
        path: Path,
        metadata: dict[str, object],
        body: str,
    ) -> None:
        rendered = yaml.safe_dump(
            metadata,
            allow_unicode=True,
            sort_keys=False,
        )
        path.write_text(
            f"---\n{rendered}---\n{body}",
            encoding="utf-8",
            newline="\n",
        )

    @classmethod
    def _make_reviewed_candidate(cls) -> None:
        for profile in PROFILES.values():
            snapshot = cls.reviewed_repository / profile.snapshot_path
            for path in sorted(snapshot.iterdir()):
                if path.name in {
                    "PROVISION_INVENTORY.md",
                    "ESAF_CONTROL_MANIFEST.json",
                }:
                    continue
                metadata, body = parse_front_matter_bytes(path.read_bytes())
                metadata["status"] = "reviewed"
                role = (
                    "specification_and_inventory"
                    if path.name == "README.md"
                    else "security_and_overclaiming"
                )
                metadata["reviewer"] = _reviewer_object(
                    PROFILE_NAMES[profile.label],
                    role,
                )
                cls._write_front_matter(path, metadata, body)
            snapshot_contents = {
                path.relative_to(cls.reviewed_repository).as_posix(): (
                    path.read_bytes()
                )
                for path in sorted(snapshot.iterdir())
            }
            digest = snapshot_digest_from_files(
                profile.snapshot_path,
                snapshot_contents,
            )
            registry = (
                cls.reviewed_repository
                / "crosswalks"
                / "registry"
                / f"{profile.mapping_set_id}.md"
            )
            metadata, body = parse_front_matter_bytes(registry.read_bytes())
            metadata["snapshot_digest"] = digest
            cls._write_front_matter(registry, metadata, body)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = crosswalk_validator.main(
                ["--write"],
                root=cls.reviewed_repository,
            )
        if result != 0:
            raise AssertionError(
                f"reviewed fixture regeneration failed: {stderr.getvalue()}"
            )

    @classmethod
    def _set_candidate_findings(
        cls,
        repository: Path,
        profile: object,
        findings: list[dict[str, object]],
        message: str,
        *,
        validate_repository: bool = True,
    ) -> str:
        snapshot = repository / profile.snapshot_path
        readme = snapshot / "README.md"
        metadata, body = parse_front_matter_bytes(readme.read_bytes())
        metadata["findings"] = findings
        cls._write_front_matter(readme, metadata, body)
        snapshot_contents = {
            path.relative_to(repository).as_posix(): path.read_bytes()
            for path in sorted(snapshot.iterdir())
        }
        digest = snapshot_digest_from_files(
            profile.snapshot_path,
            snapshot_contents,
        )
        registry = (
            repository
            / "crosswalks"
            / "registry"
            / f"{profile.mapping_set_id}.md"
        )
        registry_metadata, registry_body = parse_front_matter_bytes(
            registry.read_bytes()
        )
        registry_metadata["snapshot_digest"] = digest
        cls._write_front_matter(
            registry,
            registry_metadata,
            registry_body,
        )
        if validate_repository:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = crosswalk_validator.main(
                    ["--write"],
                    root=repository,
                )
            if result != 0:
                raise AssertionError(
                    "finding fixture regeneration failed: "
                    f"{stdout.getvalue()} {stderr.getvalue()}"
                )
        else:
            catalog_path = repository / "crosswalks" / "catalog.json"
            catalog = json.loads(catalog_path.read_bytes())
            catalog_sets = catalog["mapping_sets"]
            assert isinstance(catalog_sets, list)
            catalog_entry = next(
                item
                for item in catalog_sets
                if item["metadata"]["mapping_set_id"]
                == profile.mapping_set_id
            )
            catalog_entry["metadata"]["findings"] = deepcopy(findings)
            catalog_entry["lifecycle"]["snapshot_digest"] = digest
            catalog_path.write_text(
                json.dumps(
                    catalog,
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
        _git(repository, "add", "--all")
        _git(repository, "commit", "-m", message)
        return _git(repository, "rev-parse", "HEAD")

    @classmethod
    def _make_finding_campaign(
        cls,
        root: Path,
        candidate: str,
        assemblies: dict[str, PackageAssembly],
        profile: object,
        worksheet_findings: list[dict[str, object]],
    ) -> None:
        root.mkdir()
        fixture = CampaignFixture(root, candidate, assemblies)
        mapping_sets = fixture.manifest["mapping_sets"]
        assert isinstance(mapping_sets, list)
        mapping_set = next(
            item
            for item in mapping_sets
            if item["mapping_set_id"] == profile.mapping_set_id
        )
        roles = mapping_set["roles"]
        assert isinstance(roles, list)
        for role in roles:
            worksheet = role["worksheet"]
            assert isinstance(worksheet, dict)
            worksheet["findings"] = deepcopy(worksheet_findings)
            worksheet["findings_disposition"] = "All findings resolved"
            fixture.write_role(profile, mapping_set, role)
        fixture.write_manifest()

    @classmethod
    def _make_finding_candidates(cls) -> None:
        cls.finding_repository = cls.shared_root / "finding-candidates"
        subprocess.run(
            [
                "git",
                "clone",
                "--shared",
                "--no-checkout",
                str(ROOT),
                str(cls.finding_repository),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        _git(
            cls.finding_repository,
            "checkout",
            "-b",
            "finding-fixtures",
            cls.candidate,
        )
        _git(cls.finding_repository, "config", "user.name", "ESAF Test")
        _git(
            cls.finding_repository,
            "config",
            "user.email",
            "esaf-test@example.invalid",
        )
        profile = next(
            item for item in PROFILES.values() if item.label == "Core"
        )
        record = next(
            path
            for path in sorted(
                (cls.finding_repository / profile.snapshot_path).glob("*.md")
            )
            if path.name not in {"README.md", "PROVISION_INVENTORY.md"}
        )
        record_metadata, _body = parse_front_matter_bytes(record.read_bytes())
        affected = [str(record_metadata["record_id"])]
        evidence_finding = {
            "finding_id": "review-finding",
            "affected_record_ids": affected,
            "severity": "Minor",
            "status": "resolved",
            "disposition": "Resolved by candidate correction",
            "resolver_or_acceptor": "ESAF Project Owner",
            "disposition_date": REVIEW_DATE,
            "acceptance_rationale": "Not applicable",
        }
        authoritative = {
            **evidence_finding,
            "description": "Authoritative exact description",
        }
        cls.description_candidate = cls._set_candidate_findings(
            cls.finding_repository,
            profile,
            [authoritative],
            "description finding fixture",
        )
        cls.description_reader = GitReader(cls.finding_repository)
        cls.description_assemblies = {
            item.mapping_set_id: assemble_package(
                cls.description_reader,
                cls.description_candidate,
                item,
            )
            for item in PROFILES.values()
        }
        cls.description_campaign = cls.shared_root / "description-campaign"
        cls._make_finding_campaign(
            cls.description_campaign,
            cls.description_candidate,
            cls.description_assemblies,
            profile,
            [evidence_finding],
        )

        duplicate_last = {
            **authoritative,
            "description": "Reviewed finding",
        }
        duplicate_first = {
            **authoritative,
            "description": "Earlier conflicting description",
        }
        cls.duplicate_candidate = cls._set_candidate_findings(
            cls.finding_repository,
            profile,
            [duplicate_first, duplicate_last],
            "duplicate finding fixture",
            validate_repository=False,
        )
        cls.duplicate_reader = GitReader(cls.finding_repository)
        cls.duplicate_assemblies = {
            item.mapping_set_id: assemble_package(
                cls.duplicate_reader,
                cls.duplicate_candidate,
                item,
            )
            for item in PROFILES.values()
        }
        cls.duplicate_campaign = cls.shared_root / "duplicate-campaign"
        cls._make_finding_campaign(
            cls.duplicate_campaign,
            cls.duplicate_candidate,
            cls.duplicate_assemblies,
            profile,
            [evidence_finding],
        )

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.campaign_root = Path(self.temporary.name) / "campaign"
        shutil.copytree(self.pristine_campaign, self.campaign_root)

    def _manifest(self) -> dict[str, object]:
        value = json.loads(
            (self.campaign_root / MANIFEST_PATH).read_bytes()
        )
        self.assertIsInstance(value, dict)
        return value

    def _write_manifest(self, manifest: dict[str, object]) -> None:
        (self.campaign_root / MANIFEST_PATH).write_bytes(
            canonical_json_bytes(manifest)
        )

    def _rewrite_role(
        self,
        manifest: dict[str, object],
        mapping_index: int,
        role_index: int,
    ) -> None:
        mapping_sets = manifest["mapping_sets"]
        assert isinstance(mapping_sets, list)
        mapping_set = mapping_sets[mapping_index]
        assert isinstance(mapping_set, dict)
        roles = mapping_set["roles"]
        package = mapping_set["package"]
        assert isinstance(roles, list)
        assert isinstance(package, dict)
        role = roles[role_index]
        assert isinstance(role, dict)
        mapping_set_id = str(mapping_set["mapping_set_id"])
        profile = PROFILES[mapping_set_id]
        attestation = role["attestation"]
        worksheet = role["worksheet"]
        assert isinstance(attestation, dict)
        assert isinstance(worksheet, dict)
        fixture = CampaignFixture.__new__(CampaignFixture)
        fixture.root = self.campaign_root
        fixture.candidate = str(manifest["candidate_commit"])
        fixture.assemblies = self.assemblies
        fixture.phase = str(manifest["phase"])
        fixture.campaign_id = str(manifest["campaign_id"])
        fixture.candidate_state = str(manifest["candidate_state"])
        fixture.manifest = manifest
        fixture.write_role(profile, mapping_set, role)
        self._write_manifest(manifest)

    def _report(self) -> ValidationReport:
        return validate_campaign(
            self.reader,
            self.candidate,
            self.campaign_root,
        )

    def _replace_attestation_text(
        self,
        old: str,
        new: str,
        *,
        mapping_index: int = 0,
        role_index: int = 0,
    ) -> None:
        manifest = self._manifest()
        mapping_sets = manifest["mapping_sets"]
        assert isinstance(mapping_sets, list)
        mapping_set = mapping_sets[mapping_index]
        assert isinstance(mapping_set, dict)
        roles = mapping_set["roles"]
        assert isinstance(roles, list)
        role = roles[role_index]
        assert isinstance(role, dict)
        attestation = role["attestation"]
        worksheet = role["worksheet"]
        assert isinstance(attestation, dict)
        assert isinstance(worksheet, dict)
        attestation_path = self.campaign_root.joinpath(
            *str(attestation["path"]).split("/")
        )
        prior_digest = str(attestation["sha256"])
        content = attestation_path.read_text(encoding="utf-8")
        self.assertIn(old, content)
        revised = content.replace(old, new, 1).encode("utf-8")
        attestation_path.write_bytes(revised)
        current_digest = hashlib.sha256(revised).hexdigest()
        attestation["sha256"] = current_digest

        worksheet_path = self.campaign_root.joinpath(
            *str(worksheet["path"]).split("/")
        )
        worksheet_bytes = worksheet_path.read_bytes().replace(
            prior_digest.encode("ascii"),
            current_digest.encode("ascii"),
            1,
        )
        previous_signed = str(worksheet["signed_sha256"]).encode("ascii")
        current_signed = signed_worksheet_sha256(worksheet_bytes)
        worksheet_bytes = worksheet_bytes.replace(
            previous_signed,
            current_signed.encode("ascii"),
            1,
        )
        worksheet_path.write_bytes(worksheet_bytes)
        worksheet["signed_sha256"] = current_signed
        worksheet["sha256"] = hashlib.sha256(worksheet_bytes).hexdigest()
        self._write_manifest(manifest)

    def _candidate_mapper_id(self, mapping_index: int) -> str:
        profile = tuple(PROFILES.values())[mapping_index]
        mapping_file = next(
            payload
            for payload in self.assemblies[profile.mapping_set_id].payloads
            if payload.purpose == "mapping set"
        )
        metadata, _body = parse_front_matter_bytes(mapping_file.content)
        mapper = metadata["mapper"]
        assert isinstance(mapper, dict)
        return str(mapper["id"])

    def _record_id(self, mapping_index: int) -> str:
        profile = tuple(PROFILES.values())[mapping_index]
        record = next(
            payload
            for payload in self.assemblies[profile.mapping_set_id].payloads
            if payload.purpose == "mapping record"
        )
        metadata, _body = parse_front_matter_bytes(record.content)
        return str(metadata["record_id"])

    def _finding(
        self,
        *,
        severity: str = "Minor",
        status: str = "resolved",
        record_id: str | None = None,
    ) -> dict[str, object]:
        return {
            "finding_id": "review-finding-1",
            "affected_record_ids": [record_id or self._record_id(0)],
            "severity": severity,
            "status": status,
            "disposition": (
                "Accepted for this release"
                if status == "accepted"
                else "Resolved in candidate"
            ),
            "resolver_or_acceptor": "Project Owner",
            "disposition_date": REVIEW_DATE,
            "acceptance_rationale": (
                "No material mapping effect"
                if status == "accepted"
                else "Not applicable"
            ),
        }

    def _mutate_worksheet(
        self,
        mutate: object,
        *,
        mapping_index: int = 0,
        role_index: int = 0,
    ) -> None:
        manifest = self._manifest()
        mapping_sets = manifest["mapping_sets"]
        assert isinstance(mapping_sets, list)
        mapping_set = mapping_sets[mapping_index]
        assert isinstance(mapping_set, dict)
        roles = mapping_set["roles"]
        assert isinstance(roles, list)
        role = roles[role_index]
        assert isinstance(role, dict)
        worksheet = role["worksheet"]
        assert isinstance(worksheet, dict)
        mutate(worksheet)
        self._rewrite_role(
            manifest,
            mapping_index,
            role_index,
        )

    def _final_inputs(
        self,
        name: str,
    ) -> tuple[Path, Path, Path, Path]:
        base = Path(self.temporary.name) / name
        base.mkdir()
        final_root = base / "final"
        draft_root = base / "draft"
        shutil.copytree(self.pristine_final_campaign, final_root)
        shutil.copytree(self.pristine_campaign, draft_root)
        seal_path = base / "CAMPAIGN_SEAL.json"
        archive_path = base / "CAMPAIGN_ARCHIVE.zip"
        seal_path.write_bytes(self.draft_seal_bytes)
        archive_path.write_bytes(self.draft_archive_bytes)
        return final_root, draft_root, seal_path, archive_path

    def _final_report(
        self,
        final_root: Path,
        draft_root: Path | None,
        seal_path: Path | None,
        archive_path: Path | None,
    ) -> ValidationReport:
        return validate_campaign(
            self.reviewed_reader,
            self.reviewed_candidate,
            final_root,
            draft_root,
            seal_path,
            archive_path,
        )

    def test_valid_draft_campaign_is_transition_ready(self) -> None:
        report = validate_campaign(
            self.reader,
            self.candidate,
            self.campaign_root,
        )

        self.assertIsInstance(report, ValidationReport)
        self.assertTrue(report.evidence_valid, report.errors)
        self.assertEqual(report.readiness_name, "transition_ready")
        self.assertTrue(report.readiness_value)
        self.assertEqual(report.candidate_commit, self.candidate)
        self.assertEqual(report.campaign_id, "issue-55-draft-review")
        self.assertEqual(report.errors, ())

    def test_rejects_missing_duplicate_and_mismatched_role_keys(self) -> None:
        mutations = []

        missing = self._manifest()
        missing_sets = missing["mapping_sets"]
        assert isinstance(missing_sets, list)
        missing_mapping = missing_sets[0]
        assert isinstance(missing_mapping, dict)
        missing_roles = missing_mapping["roles"]
        assert isinstance(missing_roles, list)
        missing_roles.pop()
        mutations.append(("missing role", missing))

        duplicate = self._manifest()
        duplicate_sets = duplicate["mapping_sets"]
        assert isinstance(duplicate_sets, list)
        duplicate_mapping = duplicate_sets[0]
        assert isinstance(duplicate_mapping, dict)
        duplicate_roles = duplicate_mapping["roles"]
        assert isinstance(duplicate_roles, list)
        duplicate_second = duplicate_roles[1]
        assert isinstance(duplicate_second, dict)
        duplicate_second["role"] = "specification_and_inventory"
        mutations.append(("duplicate role", duplicate))

        mismatched = self._manifest()
        mismatched_sets = mismatched["mapping_sets"]
        assert isinstance(mismatched_sets, list)
        first_mapping = mismatched_sets[0]
        second_mapping = mismatched_sets[1]
        assert isinstance(first_mapping, dict)
        assert isinstance(second_mapping, dict)
        second_mapping["mapping_set_id"] = first_mapping["mapping_set_id"]
        mutations.append(("duplicate mapping set", mismatched))

        for label, manifest in mutations:
            with self.subTest(label=label):
                isolated = Path(self.temporary.name) / label.replace(" ", "-")
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    if label == "duplicate role":
                        self._rewrite_role(manifest, 0, 1)
                    else:
                        self._write_manifest(manifest)
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_rejects_ineligible_reviewer_evidence(self) -> None:
        cases = (
            (
                "unauthorized source access",
                lambda role: role["reviewer"].__setitem__(
                    "authorized_source_access",
                    False,
                ),
            ),
            (
                "mapper self-review",
                lambda role: role["reviewer"].__setitem__(
                    "identity",
                    self._candidate_mapper_id(0),
                ),
            ),
            (
                "unresolved conflict",
                lambda role: (
                    role["reviewer"].__setitem__("conflicts", True),
                    role["reviewer"].__setitem__(
                        "conflict_disposition",
                        "Unresolved",
                    ),
                ),
            ),
            (
                "pending conflict variant",
                lambda role: (
                    role["reviewer"].__setitem__("conflicts", True),
                    role["reviewer"].__setitem__(
                        "conflict_disposition",
                        "Resolution pending",
                    ),
                ),
            ),
            (
                "rejected owner eligibility",
                lambda role: role.__setitem__(
                    "owner_eligibility_accepted",
                    False,
                ),
            ),
        )
        for label, mutate in cases:
            with self.subTest(label=label):
                isolated = Path(self.temporary.name) / label.replace(" ", "-")
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    manifest = self._manifest()
                    mapping_sets = manifest["mapping_sets"]
                    assert isinstance(mapping_sets, list)
                    mapping_set = mapping_sets[0]
                    assert isinstance(mapping_set, dict)
                    roles = mapping_set["roles"]
                    assert isinstance(roles, list)
                    role = roles[0]
                    assert isinstance(role, dict)
                    mutate(role)
                    self._rewrite_role(manifest, 0, 0)
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_actor_aliases_and_shared_locator_cannot_bypass_role_rules(
        self,
    ) -> None:
        aliases = (
            ("case", None, lambda value: value.swapcase(), False),
            (
                "punctuation",
                None,
                lambda value: value.replace(" ", "-"),
                False,
            ),
            (
                "unicode",
                "Jos\u00e9 Reviewer",
                lambda _value: "Jose\u0301 Reviewer",
                False,
            ),
            (
                "shared-locator",
                None,
                lambda _value: "Different Display Name",
                True,
            ),
        )
        for label, first_name, alias, share_locator in aliases:
            with self.subTest(alias=label):
                isolated = Path(self.temporary.name) / f"actor-alias-{label}"
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    manifest = self._manifest()
                    mapping_sets = manifest["mapping_sets"]
                    assert isinstance(mapping_sets, list)
                    mapping_set = mapping_sets[0]
                    assert isinstance(mapping_set, dict)
                    roles = mapping_set["roles"]
                    assert isinstance(roles, list)
                    first, second = roles
                    assert isinstance(first, dict)
                    assert isinstance(second, dict)
                    first_reviewer = first["reviewer"]
                    second_reviewer = second["reviewer"]
                    assert isinstance(first_reviewer, dict)
                    assert isinstance(second_reviewer, dict)
                    if first_name is not None:
                        first_reviewer["identity"] = first_name
                    second_reviewer["identity"] = alias(
                        str(first_reviewer["identity"])
                    )
                    if share_locator:
                        second_reviewer["verification_locator"] = (
                            first_reviewer["verification_locator"]
                        )
                    self._rewrite_role(manifest, 0, 0)
                    self._rewrite_role(manifest, 0, 1)
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_actor_alias_cannot_bypass_mapper_independence(self) -> None:
        manifest = self._manifest()
        mapping_sets = manifest["mapping_sets"]
        assert isinstance(mapping_sets, list)
        mapping_set = mapping_sets[0]
        assert isinstance(mapping_set, dict)
        roles = mapping_set["roles"]
        assert isinstance(roles, list)
        role = roles[0]
        assert isinstance(role, dict)
        reviewer = role["reviewer"]
        assert isinstance(reviewer, dict)
        reviewer["identity"] = self._candidate_mapper_id(0).swapcase()
        self._rewrite_role(manifest, 0, 0)
        self.assertFalse(self._report().evidence_valid)

    def test_sha_locators_bind_package_attestation_and_worksheet_bytes(
        self,
    ) -> None:
        for locator_class in ("package", "attestation", "worksheet"):
            with self.subTest(locator_class=locator_class):
                isolated = Path(self.temporary.name) / locator_class
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    manifest = self._manifest()
                    mapping_sets = manifest["mapping_sets"]
                    assert isinstance(mapping_sets, list)
                    mapping_set = mapping_sets[0]
                    assert isinstance(mapping_set, dict)
                    roles = mapping_set["roles"]
                    assert isinstance(roles, list)
                    if locator_class == "package":
                        package = mapping_set["package"]
                        assert isinstance(package, dict)
                        package["immutable_locator"] = (
                            f"urn:sha256:{'0' * 64}"
                        )
                        self._rewrite_role(manifest, 0, 0)
                        self._rewrite_role(manifest, 0, 1)
                    else:
                        role = roles[0]
                        assert isinstance(role, dict)
                        record = role[locator_class]
                        assert isinstance(record, dict)
                        record["immutable_locator"] = (
                            f"urn:sha256:{'0' * 64}"
                        )
                        self._rewrite_role(manifest, 0, 0)
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_attestation_source_sets_are_exactly_candidate_bound(self) -> None:
        attestation_path = next(
            (self.campaign_root / "attestations").glob("*.md")
        )
        text = attestation_path.read_text(encoding="utf-8")
        checksum_line = next(
            line
            for line in text.splitlines()
            if line.startswith("| Source checksum(s) | ")
        )
        locator_line = next(
            line
            for line in text.splitlines()
            if line.startswith("| Source locator(s) | ")
        )
        checksum_set = checksum_line.removeprefix(
            "| Source checksum(s) | "
        ).removesuffix(" |")
        locator_set = locator_line.removeprefix(
            "| Source locator(s) | "
        ).removesuffix(" |")
        cases = (
            (checksum_set, "0" * 64),
            (checksum_set, checksum_set + ", " + "0" * 64),
            (
                checksum_set,
                ", ".join(checksum_set.split(", ")[:-1]) or "0" * 64,
            ),
            (
                locator_set,
                locator_set + ", https://wrong.invalid/source?version=1",
            ),
            (
                locator_set,
                ", ".join(locator_set.split(", ")[:-1])
                or "https://wrong.invalid/source?version=1",
            ),
            ("| Exact source version | 3.3 |", "| Exact source version | 3.2 |"),
        )
        for index, (old, new) in enumerate(cases):
            with self.subTest(case=index):
                isolated = Path(self.temporary.name) / f"source-set-{index}"
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    self._replace_attestation_text(old, new)
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_explicitly_resolved_conflict_is_eligible(self) -> None:
        manifest = self._manifest()
        mapping_sets = manifest["mapping_sets"]
        assert isinstance(mapping_sets, list)
        mapping_set = mapping_sets[0]
        assert isinstance(mapping_set, dict)
        roles = mapping_set["roles"]
        assert isinstance(roles, list)
        role = roles[0]
        assert isinstance(role, dict)
        reviewer = role["reviewer"]
        assert isinstance(reviewer, dict)
        reviewer["conflicts"] = True
        reviewer["conflict_disposition"] = (
            "Resolved: reviewer recused from all mapping decisions"
        )
        self._rewrite_role(manifest, 0, 0)

        report = self._report()

        self.assertTrue(report.evidence_valid, report.errors)
        self.assertTrue(report.readiness_value)

    def test_duplicate_human_requires_dual_acceptance_and_both_qualifications(
        self,
    ) -> None:
        cases = ("without acceptance", "incomplete qualifications")
        for label in cases:
            with self.subTest(label=label):
                isolated = Path(self.temporary.name) / label.replace(" ", "-")
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    manifest = self._manifest()
                    mapping_sets = manifest["mapping_sets"]
                    assert isinstance(mapping_sets, list)
                    mapping_set = mapping_sets[0]
                    assert isinstance(mapping_set, dict)
                    roles = mapping_set["roles"]
                    assert isinstance(roles, list)
                    first = roles[0]
                    second = roles[1]
                    assert isinstance(first, dict)
                    assert isinstance(second, dict)
                    first_reviewer = first["reviewer"]
                    second_reviewer = second["reviewer"]
                    assert isinstance(first_reviewer, dict)
                    assert isinstance(second_reviewer, dict)
                    second_reviewer["identity"] = first_reviewer["identity"]
                    if label == "incomplete qualifications":
                        first["dual_role_accepted"] = True
                        second["dual_role_accepted"] = True
                        second_reviewer["qualification"] = " "
                    self._rewrite_role(manifest, 0, 0)
                    self._rewrite_role(manifest, 0, 1)
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_stop_with_open_high_severity_is_valid_but_not_ready(self) -> None:
        for severity in ("Critical", "Important"):
            with self.subTest(severity=severity):
                isolated = Path(self.temporary.name) / severity.casefold()
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    finding = self._finding(
                        severity=severity,
                        status="open",
                    )
                    self._mutate_worksheet(
                        lambda worksheet: (
                            worksheet.__setitem__("conclusion", "stop"),
                            worksheet.__setitem__("findings", [finding]),
                            worksheet.__setitem__(
                                "findings_disposition",
                                f"Open {severity} finding stops transition",
                            ),
                        )
                    )
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertTrue(report.evidence_valid, report.errors)
                self.assertEqual(report.readiness_name, "transition_ready")
                self.assertFalse(report.readiness_value)

    def test_accepted_critical_or_important_is_evidence_invalid(self) -> None:
        for severity in ("Critical", "Important"):
            with self.subTest(severity=severity):
                isolated = (
                    Path(self.temporary.name)
                    / f"accepted-{severity.casefold()}"
                )
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    finding = self._finding(
                        severity=severity,
                        status="accepted",
                    )
                    self._mutate_worksheet(
                        lambda worksheet: worksheet.__setitem__(
                            "findings",
                            [finding],
                        )
                    )
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_accepted_minor_requires_named_acceptance_evidence(self) -> None:
        for field in (
            "resolver_or_acceptor",
            "acceptance_rationale",
            "disposition_date",
        ):
            with self.subTest(field=field):
                isolated = Path(self.temporary.name) / f"minor-{field}"
                shutil.copytree(self.pristine_campaign, isolated)
                original = self.campaign_root
                self.campaign_root = isolated
                try:
                    finding = self._finding(status="accepted")
                    finding[field] = ""
                    self._mutate_worksheet(
                        lambda worksheet: worksheet.__setitem__(
                            "findings",
                            [finding],
                        )
                    )
                    report = self._report()
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_pass_rejects_open_findings(self) -> None:
        finding = self._finding(status="open")
        self._mutate_worksheet(
            lambda worksheet: worksheet.__setitem__("findings", [finding])
        )

        report = self._report()

        self.assertFalse(report.evidence_valid, report)

    def test_pass_after_correction_binds_exact_campaign_candidate(self) -> None:
        def mutate(worksheet: dict[str, object]) -> None:
            worksheet["conclusion"] = "pass_after_correction"
            worksheet["post_correction_candidate_sha"] = "a" * 40

        self._mutate_worksheet(mutate)
        report = self._report()
        self.assertFalse(report.evidence_valid, report)

        shutil.rmtree(self.campaign_root)
        shutil.copytree(self.pristine_campaign, self.campaign_root)

        def bind_exact(worksheet: dict[str, object]) -> None:
            worksheet["conclusion"] = "pass_after_correction"
            worksheet["post_correction_candidate_sha"] = self.candidate

        self._mutate_worksheet(bind_exact)
        exact = self._report()
        self.assertTrue(exact.evidence_valid, exact.errors)
        self.assertTrue(exact.readiness_value)

    def test_orphan_affected_record_identifier_is_invalid_even_for_stop(
        self,
    ) -> None:
        finding = self._finding(
            status="open",
            record_id="orphan-record",
        )
        self._mutate_worksheet(
            lambda worksheet: (
                worksheet.__setitem__("conclusion", "stop"),
                worksheet.__setitem__("findings", [finding]),
            )
        )

        report = self._report()

        self.assertFalse(report.evidence_valid, report)

    def test_ready_findings_must_equal_authoritative_candidate_findings(
        self,
    ) -> None:
        finding = self._finding(status="resolved")
        self._mutate_worksheet(
            lambda worksheet: worksheet.__setitem__("findings", [finding])
        )

        report = self._report()

        self.assertFalse(report.evidence_valid, report)

    def test_ready_findings_bind_authoritative_description(self) -> None:
        report = validate_campaign(
            self.description_reader,
            self.description_candidate,
            self.description_campaign,
        )

        self.assertFalse(report.evidence_valid, report)

    def test_duplicate_authoritative_finding_identifiers_are_invalid(
        self,
    ) -> None:
        report = validate_campaign(
            self.duplicate_reader,
            self.duplicate_candidate,
            self.duplicate_campaign,
        )

        self.assertFalse(report.evidence_valid, report)

    def test_campaign_tree_and_package_bytes_are_exact(self) -> None:
        for mutation in ("extra source", "manifest byte", "payload byte"):
            with self.subTest(mutation=mutation):
                isolated = (
                    Path(self.temporary.name)
                    / mutation.replace(" ", "-")
                )
                shutil.copytree(self.pristine_campaign, isolated)
                if mutation == "extra source":
                    (isolated / "licensed-source.pdf").write_bytes(
                        b"not allowlisted"
                    )
                else:
                    manifest = json.loads(
                        (isolated / MANIFEST_PATH).read_bytes()
                    )
                    mapping_sets = manifest["mapping_sets"]
                    assert isinstance(mapping_sets, list)
                    mapping_set = mapping_sets[0]
                    assert isinstance(mapping_set, dict)
                    package = mapping_set["package"]
                    assert isinstance(package, dict)
                    if mutation == "manifest byte":
                        target = isolated.joinpath(
                            *str(package["manifest_path"]).split("/")
                        )
                    else:
                        assembly = self.assemblies[
                            str(mapping_set["mapping_set_id"])
                        ]
                        payload = next(
                            item
                            for item in assembly.payloads
                            if item.path.endswith(".md")
                        )
                        target = isolated.joinpath(
                            *(
                                f"{package['root']}/{payload.path}"
                            ).split("/")
                        )
                    target.write_bytes(target.read_bytes() + b"mutated")
                report = validate_campaign(
                    self.reader,
                    self.candidate,
                    isolated,
                )
                self.assertFalse(report.evidence_valid, report)

    def test_candidate_schema_cannot_retrieve_external_references(self) -> None:
        malicious_schema = canonical_json_bytes(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": (
                    "https://esaf-standard.org/schemas/"
                    "qualified-review-evidence.schema.json"
                ),
                "$ref": "https://attacker.example.invalid/schema.json",
            }
        )
        original_read = self.reader.read_bytes

        def read_candidate(commit: str, path: str) -> bytes:
            if path == "crosswalks/schema/qualified-review-evidence.schema.json":
                return malicious_schema
            return original_read(commit, path)

        with (
            mock.patch.object(
                self.reader,
                "read_bytes",
                side_effect=read_candidate,
            ),
            mock.patch(
                "urllib.request.urlopen",
                side_effect=AssertionError("network retrieval attempted"),
            ) as urlopen,
        ):
            report = self._report()

        self.assertFalse(report.evidence_valid, report)
        urlopen.assert_not_called()

    def test_valid_final_campaign_is_recursively_merge_ready(self) -> None:
        final_root, draft_root, seal_path, archive_path = self._final_inputs(
            "valid-final"
        )

        report = self._final_report(
            final_root,
            draft_root,
            seal_path,
            archive_path,
        )

        self.assertTrue(report.evidence_valid, report.errors)
        self.assertEqual(report.readiness_name, "merge_ready")
        self.assertTrue(report.readiness_value)
        self.assertEqual(report.candidate_commit, self.reviewed_candidate)
        self.assertEqual(report.campaign_id, "issue-55-final-confirmation")

    def test_invalid_report_preserves_parsed_final_campaign_context(self) -> None:
        final_root, draft_root, seal_path, archive_path = self._final_inputs(
            "invalid-final-context"
        )
        manifest = json.loads((final_root / MANIFEST_PATH).read_bytes())
        mapping_sets = manifest["mapping_sets"]
        assert isinstance(mapping_sets, list)
        mapping_set = mapping_sets[0]
        assert isinstance(mapping_set, dict)
        package = mapping_set["package"]
        assert isinstance(package, dict)
        assembly = self.reviewed_assemblies[
            str(mapping_set["mapping_set_id"])
        ]
        payload = next(
            item for item in assembly.payloads if item.path.endswith(".md")
        )
        payload_path = final_root.joinpath(
            *(f"{package['root']}/{payload.path}").split("/")
        )
        payload_path.write_bytes(payload_path.read_bytes() + b"mutated")

        report = self._final_report(
            final_root,
            draft_root,
            seal_path,
            archive_path,
        )

        self.assertFalse(report.evidence_valid, report)
        self.assertEqual(report.readiness_name, "merge_ready")
        self.assertEqual(report.campaign_id, "issue-55-final-confirmation")
        self.assertEqual(report.candidate_commit, self.reviewed_candidate)

    def test_final_campaign_requires_all_preserved_draft_inputs(self) -> None:
        final_root, draft_root, seal_path, archive_path = self._final_inputs(
            "missing-inputs"
        )
        cases = (
            (None, seal_path, archive_path),
            (draft_root, None, archive_path),
            (draft_root, seal_path, None),
        )
        for supplied in cases:
            with self.subTest(supplied=supplied):
                report = self._final_report(final_root, *supplied)
                self.assertFalse(report.evidence_valid, report)

    def test_final_campaign_binds_every_draft_reference_field(self) -> None:
        changes = (
            ("campaign_id", "another-draft-campaign"),
            ("candidate_commit", self.reviewed_candidate),
            ("manifest_sha256", "a" * 64),
            ("seal_record_sha256", "a" * 64),
        )
        for field, value in changes:
            with self.subTest(field=field):
                (
                    final_root,
                    draft_root,
                    seal_path,
                    archive_path,
                ) = self._final_inputs(f"reference-{field}")
                manifest = json.loads(
                    (final_root / MANIFEST_PATH).read_bytes()
                )
                reference = manifest["draft_campaign_reference"]
                assert isinstance(reference, dict)
                reference[field] = value
                (final_root / MANIFEST_PATH).write_bytes(
                    canonical_json_bytes(manifest)
                )
                report = self._final_report(
                    final_root,
                    draft_root,
                    seal_path,
                    archive_path,
                )
                self.assertFalse(report.evidence_valid, report)

    def test_final_campaign_rejects_archive_seal_or_draft_byte_mutation(
        self,
    ) -> None:
        for mutation in ("archive", "seal-version", "seal-field", "draft"):
            with self.subTest(mutation=mutation):
                (
                    final_root,
                    draft_root,
                    seal_path,
                    archive_path,
                ) = self._final_inputs(f"mutated-{mutation}")
                if mutation == "archive":
                    archive_path.write_bytes(
                        archive_path.read_bytes() + b"mutated"
                    )
                elif mutation in {"seal-version", "seal-field"}:
                    seal = json.loads(seal_path.read_bytes())
                    if mutation == "seal-version":
                        seal["validator_version"] = "0.0.0"
                    else:
                        seal["archive_sha256"] = "a" * 64
                    mutated_seal = canonical_json_bytes(seal)
                    seal_path.write_bytes(mutated_seal)
                    final_manifest = json.loads(
                        (final_root / MANIFEST_PATH).read_bytes()
                    )
                    reference = final_manifest["draft_campaign_reference"]
                    assert isinstance(reference, dict)
                    reference["seal_record_sha256"] = hashlib.sha256(
                        mutated_seal
                    ).hexdigest()
                    (final_root / MANIFEST_PATH).write_bytes(
                        canonical_json_bytes(final_manifest)
                    )
                else:
                    manifest = json.loads(
                        (draft_root / MANIFEST_PATH).read_bytes()
                    )
                    manifest["retention_commitment"] = (
                        "Mutated after sealing."
                    )
                    (draft_root / MANIFEST_PATH).write_bytes(
                        canonical_json_bytes(manifest)
                    )
                report = self._final_report(
                    final_root,
                    draft_root,
                    seal_path,
                    archive_path,
                )
                self.assertFalse(report.evidence_valid, report)

    def test_retained_draft_revalidation_rejects_mismatched_archive_urn(
        self,
    ) -> None:
        final_root, draft_root, seal_path, archive_path = self._final_inputs(
            "draft-archive-urn-mismatch"
        )
        seal = json.loads(seal_path.read_bytes())
        seal["archive_locator"] = f"urn:sha256:{'0' * 64}"
        revised_seal = canonical_json_bytes(seal)
        seal_path.write_bytes(revised_seal)
        final_manifest = json.loads(
            (final_root / MANIFEST_PATH).read_bytes()
        )
        reference = final_manifest["draft_campaign_reference"]
        assert isinstance(reference, dict)
        reference["seal_record_sha256"] = hashlib.sha256(
            revised_seal
        ).hexdigest()
        (final_root / MANIFEST_PATH).write_bytes(
            canonical_json_bytes(final_manifest)
        )

        report = self._final_report(
            final_root,
            draft_root,
            seal_path,
            archive_path,
        )

        self.assertFalse(report.evidence_valid, report)

    def test_reviewed_candidate_requires_exact_nested_reviewer_objects(
        self,
    ) -> None:
        for role_index in (0, 1):
            with self.subTest(role=ROLES[role_index]):
                (
                    final_root,
                    draft_root,
                    seal_path,
                    archive_path,
                ) = self._final_inputs(f"reviewer-{role_index}")
                original = self.campaign_root
                self.campaign_root = final_root
                try:
                    manifest = self._manifest()
                    mapping_sets = manifest["mapping_sets"]
                    assert isinstance(mapping_sets, list)
                    mapping_set = mapping_sets[0]
                    assert isinstance(mapping_set, dict)
                    roles = mapping_set["roles"]
                    assert isinstance(roles, list)
                    role = roles[role_index]
                    assert isinstance(role, dict)
                    reviewer = role["reviewer"]
                    assert isinstance(reviewer, dict)
                    reviewer["qualification"] = (
                        "Different signed qualification"
                    )
                    self._rewrite_role(manifest, 0, role_index)
                    report = self._final_report(
                        final_root,
                        draft_root,
                        seal_path,
                        archive_path,
                    )
                finally:
                    self.campaign_root = original
                self.assertFalse(report.evidence_valid, report)

    def test_final_pass_after_correction_binds_reviewed_candidate(self) -> None:
        final_root, draft_root, seal_path, archive_path = self._final_inputs(
            "final-correction"
        )
        original = self.campaign_root
        self.campaign_root = final_root
        try:
            self._mutate_worksheet(
                lambda worksheet: (
                    worksheet.__setitem__(
                        "conclusion",
                        "pass_after_correction",
                    ),
                    worksheet.__setitem__(
                        "post_correction_candidate_sha",
                        self.candidate,
                    ),
                )
            )
            report = self._final_report(
                final_root,
                draft_root,
                seal_path,
                archive_path,
            )
        finally:
            self.campaign_root = original
        self.assertFalse(report.evidence_valid, report)

    def _run_validator_cli(
        self,
        arguments: list[str],
    ) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = main(arguments, root=self.repository)
        return result, stdout.getvalue(), stderr.getvalue()

    def test_validator_cli_emits_canonical_reports_and_exit_codes(self) -> None:
        arguments = [
            "--candidate",
            self.candidate,
            "--evidence-root",
            str(self.campaign_root),
            "--check",
        ]
        result, stdout, stderr = self._run_validator_cli(arguments)
        expected = ValidationReport(
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            candidate_commit=self.candidate,
            campaign_id="issue-55-draft-review",
            errors=(),
        )
        self.assertEqual(result, 0, stderr)
        self.assertEqual(
            stdout.encode("utf-8"),
            canonical_json_bytes(expected.as_mapping()),
        )
        self.assertEqual(stderr, "")

        (self.campaign_root / MANIFEST_PATH).write_bytes(b"{malformed\n")
        invalid_result, invalid_stdout, invalid_stderr = (
            self._run_validator_cli(arguments)
        )
        self.assertEqual(invalid_result, 1)
        invalid_report = json.loads(invalid_stdout)
        self.assertFalse(invalid_report["evidence_valid"])
        self.assertEqual(
            invalid_stdout.encode("utf-8"),
            canonical_json_bytes(invalid_report),
        )
        self.assertEqual(invalid_stderr, "")

    def test_validator_cli_requires_check_and_all_or_none_draft_inputs(
        self,
    ) -> None:
        base = [
            "--candidate",
            self.candidate,
            "--evidence-root",
            str(self.campaign_root),
        ]
        cases = (
            base,
            [
                *base,
                "--check",
                "--draft-evidence-root",
                str(self.pristine_campaign),
            ],
            [
                *base,
                "--check",
                "--draft-seal-record",
                str(self.draft_seal_path),
            ],
            [
                *base,
                "--check",
                "--draft-archive",
                str(self.draft_archive_path),
            ],
        )
        for arguments in cases:
            with self.subTest(arguments=arguments[-2:]):
                result, stdout, stderr = self._run_validator_cli(arguments)
                self.assertEqual(result, 2)
                self.assertEqual(stdout, "")
                self.assertEqual(len(stderr.splitlines()), 1)

    def test_validator_cli_sanitizes_missing_and_permission_failures(
        self,
    ) -> None:
        missing_root = (
            Path(self.temporary.name)
            / "host-secret-campaign-does-not-exist"
        )
        arguments = [
            "--candidate",
            self.candidate,
            "--evidence-root",
            str(missing_root),
            "--check",
        ]
        result, stdout, stderr = self._run_validator_cli(arguments)
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertNotIn(str(missing_root), stderr)
        self.assertNotIn("host-secret", stderr)

        with mock.patch(
            "tools.crosswalks.qualified_review_evidence._open_final_file",
            side_effect=PermissionError("host-secret permission denied"),
        ):
            result, stdout, stderr = self._run_validator_cli(
                [
                    "--candidate",
                    self.candidate,
                    "--evidence-root",
                    str(self.campaign_root),
                    "--check",
                ]
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertNotIn("host-secret", stderr)

    def test_validator_cli_classifies_preopen_permissions_as_operational(
        self,
    ) -> None:
        arguments = [
            "--candidate",
            self.candidate,
            "--evidence-root",
            str(self.campaign_root),
            "--check",
        ]
        original_resolve = Path.resolve
        original_stat = Path.stat
        manifest_path = self.campaign_root / MANIFEST_PATH

        def deny_campaign_resolve(
            path: Path,
            *args: object,
            **kwargs: object,
        ) -> Path:
            if path == self.campaign_root:
                raise PermissionError("host-secret resolve denied")
            return original_resolve(path, *args, **kwargs)

        def deny_manifest_stat(
            path: Path,
            *args: object,
            **kwargs: object,
        ) -> object:
            if (
                path == manifest_path
                and kwargs.get("follow_symlinks") is False
            ):
                raise PermissionError("host-secret stat denied")
            return original_stat(path, *args, **kwargs)

        cases = (
            (
                "lstat",
                mock.patch.object(
                    Path,
                    "lstat",
                    autospec=True,
                    side_effect=PermissionError("host-secret lstat denied"),
                ),
            ),
            (
                "iterdir",
                mock.patch.object(
                    Path,
                    "iterdir",
                    autospec=True,
                    side_effect=PermissionError("host-secret iterdir denied"),
                ),
            ),
            (
                "resolve",
                mock.patch.object(
                    Path,
                    "resolve",
                    autospec=True,
                    side_effect=deny_campaign_resolve,
                ),
            ),
            (
                "stat",
                mock.patch.object(
                    Path,
                    "stat",
                    autospec=True,
                    side_effect=deny_manifest_stat,
                ),
            ),
        )
        for boundary, patcher in cases:
            with self.subTest(boundary=boundary), patcher:
                result, stdout, stderr = self._run_validator_cli(arguments)
                self.assertEqual(result, 2)
                self.assertEqual(stdout, "")
                self.assertEqual(len(stderr.splitlines()), 1)
                self.assertNotIn("host-secret", stderr)

    def test_clis_sanitize_git_operational_failures(self) -> None:
        git_failure = subprocess.CalledProcessError(128, ["git"])
        validator_arguments = [
            "--candidate",
            self.candidate,
            "--evidence-root",
            str(self.campaign_root),
            "--check",
        ]
        with mock.patch(
            "tools.build_mapping_review_bundle.GitReader.worktree_roots",
            autospec=True,
            side_effect=git_failure,
        ):
            result, stdout, stderr = self._run_validator_cli(
                validator_arguments
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertNotIn(str(self.repository), stderr)

        decode_failure = UnicodeDecodeError(
            "utf-8",
            b"\xff",
            0,
            1,
            "invalid Git output",
        )
        with mock.patch(
            "tools.build_mapping_review_bundle.GitReader.worktree_roots",
            autospec=True,
            side_effect=decode_failure,
        ):
            result, stdout, stderr = self._run_validator_cli(
                validator_arguments
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)

        output = Path(self.temporary.name) / "git-failure-output"
        with mock.patch(
            "tools.build_mapping_review_bundle.GitReader.worktree_roots",
            autospec=True,
            side_effect=git_failure,
        ):
            result, stdout, stderr = self._run_seal_cli(
                self._seal_arguments(output)
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertFalse(output.exists())

    def test_validator_cli_keeps_post_blob_git_show_failure_operational(
        self,
    ) -> None:
        original_run = GitReader._run

        def fail_show(
            reader: GitReader,
            *arguments: str,
            text: bool = False,
        ) -> subprocess.CompletedProcess:
            if arguments and arguments[0] == "show":
                raise subprocess.CalledProcessError(
                    128,
                    ["git", "show", "host-secret"],
                    stderr=b"host-secret object failure",
                )
            return original_run(reader, *arguments, text=text)

        with mock.patch.object(
            GitReader,
            "_run",
            autospec=True,
            side_effect=fail_show,
        ):
            result, stdout, stderr = self._run_validator_cli(
                [
                    "--candidate",
                    self.candidate,
                    "--evidence-root",
                    str(self.campaign_root),
                    "--check",
                ]
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertNotIn("host-secret", stderr)

    def _run_seal_cli(
        self,
        arguments: list[str],
    ) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = seal_main(arguments, root=self.repository)
        return result, stdout.getvalue(), stderr.getvalue()

    def _seal_arguments(
        self,
        output: Path,
        *,
        evidence_root: Path | None = None,
        archive_locator: str = (
            "https://evidence.example.invalid/draft.zip?version=1"
        ),
    ) -> list[str]:
        return [
            "--candidate",
            self.candidate,
            "--evidence-root",
            str(evidence_root or self.campaign_root),
            "--output-directory",
            str(output),
            "--archive-locator",
            archive_locator,
        ]

    def test_seal_cli_atomically_publishes_exact_archive_and_seal(self) -> None:
        output = Path(self.temporary.name) / "sealed"

        result, stdout, stderr = self._run_seal_cli(
            self._seal_arguments(output)
        )

        self.assertEqual(result, 0, stderr)
        self.assertEqual(stderr, "")
        self.assertEqual(
            (output / "CAMPAIGN_ARCHIVE.zip").read_bytes(),
            self.draft_archive_bytes,
        )
        expected_record, expected_seal = build_seal_record(
            manifest_bytes=(
                self.campaign_root / MANIFEST_PATH
            ).read_bytes(),
            archive_bytes=self.draft_archive_bytes,
            archive_locator=(
                "https://evidence.example.invalid/draft.zip?version=1"
            ),
            campaign_id="issue-55-draft-review",
            candidate_commit=self.candidate,
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            validator_version=VALIDATOR_VERSION,
        )
        self.assertEqual(
            (output / "CAMPAIGN_SEAL.json").read_bytes(),
            expected_seal,
        )
        self.assertEqual(json.loads(stdout), expected_record)
        self.assertEqual(
            stdout.encode("utf-8"),
            canonical_json_bytes(expected_record),
        )

    def test_seal_cli_refuses_invalid_or_nonready_campaign(self) -> None:
        invalid_root = Path(self.temporary.name) / "invalid"
        shutil.copytree(self.pristine_campaign, invalid_root)
        (invalid_root / MANIFEST_PATH).write_bytes(b"{malformed\n")
        invalid_output = Path(self.temporary.name) / "invalid-output"
        result, _stdout, _stderr = self._run_seal_cli(
            self._seal_arguments(
                invalid_output,
                evidence_root=invalid_root,
            )
        )
        self.assertEqual(result, 1)
        self.assertFalse(invalid_output.exists())

        stop_root = Path(self.temporary.name) / "stop"
        shutil.copytree(self.pristine_campaign, stop_root)
        original = self.campaign_root
        self.campaign_root = stop_root
        try:
            finding = self._finding(severity="Critical", status="open")
            self._mutate_worksheet(
                lambda worksheet: (
                    worksheet.__setitem__("conclusion", "stop"),
                    worksheet.__setitem__("findings", [finding]),
                )
            )
        finally:
            self.campaign_root = original
        stop_output = Path(self.temporary.name) / "stop-output"
        result, _stdout, _stderr = self._run_seal_cli(
            self._seal_arguments(
                stop_output,
                evidence_root=stop_root,
            )
        )
        self.assertEqual(result, 1)
        self.assertFalse(stop_output.exists())

    def test_seal_cli_refuses_existing_worktree_and_unsafe_destinations(
        self,
    ) -> None:
        existing = Path(self.temporary.name) / "existing"
        existing.mkdir()
        marker = existing / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        result, _stdout, _stderr = self._run_seal_cli(
            self._seal_arguments(existing)
        )
        self.assertEqual(result, 2)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

        worktree_output = self.repository / "sealed-output"
        result, _stdout, _stderr = self._run_seal_cli(
            self._seal_arguments(worktree_output)
        )
        self.assertEqual(result, 2)
        self.assertFalse(worktree_output.exists())

        missing_parent = (
            Path(self.temporary.name)
            / "missing-parent"
            / "sealed-output"
        )
        result, _stdout, _stderr = self._run_seal_cli(
            self._seal_arguments(missing_parent)
        )
        self.assertEqual(result, 2)
        self.assertFalse(missing_parent.exists())

        unsafe_output = Path(self.temporary.name) / "unsafe-locator"
        result, _stdout, _stderr = self._run_seal_cli(
            self._seal_arguments(
                unsafe_output,
                archive_locator=(
                    "https://evidence.example.invalid/draft.zip"
                ),
            )
        )
        self.assertEqual(result, 2)
        self.assertFalse(unsafe_output.exists())

    def test_seal_cli_publishes_nothing_after_execution_state_drift(
        self,
    ) -> None:
        output = Path(self.temporary.name) / "drift-output"
        with mock.patch(
            "tools.seal_qualified_review_campaign."
            "GitReader.require_candidate_execution_state",
            autospec=True,
            side_effect=(None, ValueError("repository became dirty")),
        ) as require_state:
            result, stdout, stderr = self._run_seal_cli(
                self._seal_arguments(output)
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertEqual(require_state.call_count, 2)
        self.assertFalse(output.exists())

    def test_seal_cli_preserves_competing_output_and_cleans_partial_staging(
        self,
    ) -> None:
        output = Path(self.temporary.name) / "competing-output"
        original_rename = seal_module._rename_directory_no_replace

        def publish_competitor(
            source: Path,
            destination: Path,
            *dir_fds: int | None,
        ) -> None:
            destination.mkdir()
            (destination / "competitor.txt").write_text(
                "keep",
                encoding="utf-8",
            )
            original_rename(source, destination, *dir_fds)

        with mock.patch(
            "tools.seal_qualified_review_campaign."
            "_rename_directory_no_replace",
            side_effect=publish_competitor,
        ):
            result, stdout, stderr = self._run_seal_cli(
                self._seal_arguments(output)
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertEqual(
            (output / "competitor.txt").read_text(encoding="utf-8"),
            "keep",
        )
        self.assertEqual(
            tuple(output.parent.glob(f".{output.name}.staging-*")),
            (),
        )

        partial_output = Path(self.temporary.name) / "partial-output"
        original_write = seal_module._write_exclusive_fsync

        def fail_seal_write(path: Path, content: bytes) -> None:
            if path.name == "CAMPAIGN_SEAL.json":
                raise OSError("simulated partial publication failure")
            original_write(path, content)

        with mock.patch(
            "tools.seal_qualified_review_campaign._write_exclusive_fsync",
            side_effect=fail_seal_write,
        ):
            result, stdout, stderr = self._run_seal_cli(
                self._seal_arguments(partial_output)
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertFalse(partial_output.exists())
        self.assertEqual(
            tuple(
                partial_output.parent.glob(
                    f".{partial_output.name}.staging-*"
                )
            ),
            (),
        )

    def test_seal_fails_closed_when_parent_or_ancestor_is_swapped(
        self,
    ) -> None:
        for boundary in ("parent", "ancestor"):
            with self.subTest(boundary=boundary):
                base = Path(self.temporary.name) / f"swap-{boundary}"
                parent = base / "ancestor" / "parent"
                parent.mkdir(parents=True)
                output = parent / "sealed"
                swap_target = parent if boundary == "parent" else parent.parent
                moved = swap_target.with_name(swap_target.name + "-moved")
                original_validate = seal_module._validate_campaign_details

                def swap_after_validation(
                    *args: object,
                    **kwargs: object,
                ) -> object:
                    details = original_validate(*args, **kwargs)
                    swap_target.rename(moved)
                    swap_target.mkdir(parents=True)
                    return details

                with mock.patch(
                    "tools.seal_qualified_review_campaign."
                    "_validate_campaign_details",
                    side_effect=swap_after_validation,
                ):
                    result, stdout, stderr = self._run_seal_cli(
                        self._seal_arguments(output)
                    )
                self.assertEqual(result, 2)
                self.assertEqual(stdout, "")
                self.assertEqual(len(stderr.splitlines()), 1)
                self.assertFalse(output.exists())
                moved_output = (
                    moved / "sealed"
                    if boundary == "parent"
                    else moved / "parent" / "sealed"
                )
                self.assertFalse(moved_output.exists())

    def test_seal_archives_the_exact_validated_byte_snapshot(self) -> None:
        output = Path(self.temporary.name) / "snapshot-output"
        manifest_path = self.campaign_root / MANIFEST_PATH
        validated_manifest = manifest_path.read_bytes()
        original_builder = build_campaign_archive

        def mutate_then_build(
            root: Path,
            allowlist: tuple[str, ...],
            **kwargs: object,
        ) -> bytes:
            manifest_path.write_bytes(validated_manifest + b" ")
            return original_builder(root, allowlist, **kwargs)

        with mock.patch(
            "tools.validate_qualified_review_evidence."
            "build_campaign_archive",
            side_effect=mutate_then_build,
        ):
            result, stdout, stderr = self._run_seal_cli(
                self._seal_arguments(output)
            )

        self.assertEqual(result, 0, stderr)
        self.assertNotEqual(manifest_path.read_bytes(), validated_manifest)
        with zipfile.ZipFile(output / "CAMPAIGN_ARCHIVE.zip") as archive:
            archived_manifest = archive.read(MANIFEST_PATH)
        self.assertEqual(archived_manifest, validated_manifest)
        seal = json.loads((output / "CAMPAIGN_SEAL.json").read_bytes())
        self.assertEqual(
            seal["manifest_sha256"],
            hashlib.sha256(validated_manifest).hexdigest(),
        )
        self.assertEqual(json.loads(stdout), seal)


if __name__ == "__main__":
    unittest.main()
