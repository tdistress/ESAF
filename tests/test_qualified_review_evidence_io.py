from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
import zipfile

from tools.crosswalks.qualified_review_evidence import (
    AttestationEvidence,
    build_campaign_archive,
    build_seal_record,
    canonical_json_bytes,
    CampaignEvidence,
    CompletedWorksheet,
    EvidenceError,
    MappingSetEvidence,
    ReviewerEvidence,
    ReviewFinding,
    RoleEvidence,
    parse_completed_attestation,
    parse_completed_worksheet,
    resolve_external_regular_file,
    signed_worksheet_sha256,
)


ROOT = Path(__file__).resolve().parents[1]
MAPPING_SET_ID = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3"
    "--esaf-0.4-alpha--0.1.0"
)
SHA = "a" * 40
DIGEST = "b" * 64
LOCATOR = f"urn:sha256:{DIGEST}"

COMPLETED_ATTESTATION = f"""# Qualified Reviewer Attestation

An unsigned blank form is not review evidence.

| Field | Value |
|---|---|
| Reviewer identity | Alice Reviewer |
| Organization | Example Assurance Ltd |
| Verification locator | {LOCATOR} |
| Mapping-set identifier | {MAPPING_SET_ID} |
| Candidate commit SHA | {SHA} |
| Package root | packages/core |
| Package manifest path | packages/core/PACKAGE_MANIFEST.json |
| Package-manifest SHA-256 | {DIGEST} |
| Package immutable locator | {LOCATOR} |
| Package retention owner | Records Owner |
| Attestation path | attestations/core-specification.md |
| Attestation immutable locator | {LOCATOR} |
| Attestation retention owner | Records Owner |
| Review role | Specification and inventory review |
| Publication identity | Cyber Essentials requirements |
| Exact source version | 3.3 |
| Official URL | https://example.invalid/publication |
| Source checksum(s) | {DIGEST} |
| Source locator(s) | https://example.invalid/source?version=3.3 |
| Publication-rights basis | Licensed reviewer access |
| Permitted elements | Review and citation |
| Prohibited elements | Redistribution |
| Restrictions | No source redistribution |
| Qualification | Scheme qualification and ESAF mapping qualification |
| Authorized source access | Yes |
| Independence from mapper | Yes |
| Conflicts of interest | No |
| Conflict disposition | Not applicable |
| Project-owner eligibility acceptance | Accepted |
| Project-owner dual-role acceptance | No |
| Project-owner identity | Project Owner |
| Project-owner signature | Project Owner / signed |
| Project-owner acceptance date | 2026-07-25 |
| Signature | Alice Reviewer / signed |
| Date | 2026-07-25 |

Every table value shall be single-line text without an unescaped pipe
character. Do not add, remove, duplicate, or reorder rows.

I attest that I had authorized access to the exact publication identity,
source version, official URL, source checksum(s), and source locator(s)
recorded above: Yes.

I attest that my access and use comply with the recorded publication-rights
basis, permitted elements, prohibited elements, and restrictions: Yes.

I attest that I am independent from the mapper: Yes.

I attest that conflicts of interest and their disposition have been fully
disclosed: Yes.

I understand that this review does not establish certification, compliance,
equivalence, endorsement, or assurance beyond the relationships expressly
recorded in the mapping snapshot.
"""

SPECIFICATION_WORKSHEET = f"""# Specification and Inventory Review Worksheet

## Review identification

| Field | Value |
|---|---|
| Mapping-set identifier | {MAPPING_SET_ID} |
| Candidate commit SHA | {SHA} |
| Package root | packages/core |
| Package manifest path | packages/core/PACKAGE_MANIFEST.json |
| Package-manifest SHA-256 | {DIGEST} |
| Package immutable locator | {LOCATOR} |
| Package retention owner | Records Owner |
| Reviewer identity | Alice Reviewer |
| Attestation path | attestations/core-specification.md |
| Attestation immutable locator | {LOCATOR} |
| Attestation retention owner | Records Owner |
| Attestation SHA-256 | {DIGEST} |
| Worksheet path | worksheets/core-specification.md |
| Worksheet immutable locator | {LOCATOR} |
| Worksheet retention owner | Records Owner |
| Review role | Specification and inventory review |
| Review date | 2026-07-25 |
| Coverage summary | All 116 provisions and mapping records |
| Review method | Requirement-level inspection |
| Provision coverage | 116 provisions |
| Mapping-record coverage | 116 mapping records |

Every table value shall be single-line text without an unescaped pipe
character. Do not add, remove, duplicate, or reorder rows.

## Review scope

Make and record an explicit determination for each of:

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
- change history.

## Findings

Critical and Important findings cannot be accepted and must be resolved.
Only Minor findings may be accepted, with a named acceptor, acceptance
rationale, and disposition date.

| Finding ID | Affected record IDs | Severity | Description | Evidence | Required action | Status | Disposition | Resolver or acceptor | Disposition date | Acceptance rationale |
|---|---|---|---|---|---|---|---|---|---|---|
| NONE |  |  |  |  |  |  |  |  |  |  |

## Overall conclusion

| Field | Value |
|---|---|
| Overall conclusion | pass |
| Post-correction candidate SHA | Not applicable |
| Reviewer metadata findings disposition | No findings |

## Worksheet signature

| Field | Value |
|---|---|
| Reviewer signature | Alice Reviewer / signed |
| Signature date | 2026-07-25 |
| Signed worksheet SHA-256 | {DIGEST} |

Digest procedure: encode the completed worksheet as UTF-8 without BOM and LF
line endings after all other fields, including the reviewer signature and
signature date, are final. For the digest calculation, remove the entire
`| Signed worksheet SHA-256 |` table row, including its terminating LF, and
hash every remaining byte with SHA-256. Record the lowercase hexadecimal
digest in that row; verification repeats the same exclusion. No non-excluded
byte may change after the digest is recorded.
"""

SECURITY_WORKSHEET = f"""# Security and Overclaiming Review Worksheet

## Review identification

| Field | Value |
|---|---|
| Mapping-set identifier | {MAPPING_SET_ID} |
| Candidate commit SHA | {SHA} |
| Package root | packages/core |
| Package manifest path | packages/core/PACKAGE_MANIFEST.json |
| Package-manifest SHA-256 | {DIGEST} |
| Package immutable locator | {LOCATOR} |
| Package retention owner | Records Owner |
| Reviewer identity | Bob Reviewer |
| Attestation path | attestations/core-security.md |
| Attestation immutable locator | {LOCATOR} |
| Attestation retention owner | Records Owner |
| Attestation SHA-256 | {DIGEST} |
| Worksheet path | worksheets/core-security.md |
| Worksheet immutable locator | {LOCATOR} |
| Worksheet retention owner | Records Owner |
| Review role | Security and overclaiming review |
| Review date | 2026-07-25 |
| Coverage summary | All 116 relationships |
| Review method | Normative-text comparison |
| Provision coverage | 116 provisions |
| Mapping-record coverage | 116 mapping records |

Every table value shall be single-line text without an unescaped pipe
character. Do not add, remove, duplicate, or reorder rows.

## Review scope

Verify:

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
  and assurance.

## Findings

Critical and Important findings cannot be accepted and must be resolved.
Only Minor findings may be accepted, with a named acceptor, acceptance
rationale, and disposition date.

| Finding ID | Affected record IDs | Severity | Description | Evidence | Required action | Status | Disposition | Resolver or acceptor | Disposition date | Acceptance rationale |
|---|---|---|---|---|---|---|---|---|---|---|
| SEC-001 | ce-m-001, ce-m-002 | Minor | Ambiguous wording | Record text | Clarify rationale | accepted | Accepted for this release | Project Owner | 2026-07-25 | No material mapping effect |
| SEC-002 | ce-m-003 | Important | Unsupported outcome | Source text | Correct relationship | resolved | Corrected | Alice Mapper | 2026-07-25 | Not applicable |

## Overall conclusion

| Field | Value |
|---|---|
| Overall conclusion | pass_after_correction |
| Post-correction candidate SHA | {SHA} |
| Reviewer metadata findings disposition | All findings reconciled |

## Worksheet signature

| Field | Value |
|---|---|
| Reviewer signature | Bob Reviewer / signed |
| Signature date | 2026-07-25 |
| Signed worksheet SHA-256 | {DIGEST} |

Digest procedure: encode the completed worksheet as UTF-8 without BOM and LF
line endings after all other fields, including the reviewer signature and
signature date, are final. For the digest calculation, remove the entire
`| Signed worksheet SHA-256 |` table row, including its terminating LF, and
hash every remaining byte with SHA-256. Record the lowercase hexadecimal
digest in that row; verification repeats the same exclusion. No non-excluded
byte may change after the digest is recorded.
"""


class ExternalPathTests(unittest.TestCase):
    def test_resolves_single_link_regular_file_beneath_external_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "evidence" / "worksheet.md"
            evidence.parent.mkdir()
            evidence.write_bytes(b"evidence\n")

            resolved = resolve_external_regular_file(
                root,
                "evidence/worksheet.md",
                (ROOT,),
            )

            self.assertEqual(resolved, evidence.resolve())

    def test_rejects_lexically_unsafe_paths_before_resolution(self) -> None:
        unsafe_paths = (
            "",
            "/absolute.md",
            "../parent.md",
            "nested/../alias.md",
            "./alias.md",
            "nested//alias.md",
            r"nested\alias.md",
            r"C:\absolute.md",
            "C:drive-relative.md",
            r"\\server\share\evidence.md",
            "//server/share/evidence.md",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in unsafe_paths:
                with self.subTest(relative=relative):
                    with mock.patch.object(
                        Path,
                        "resolve",
                        side_effect=AssertionError(
                            "resolution occurred before lexical rejection"
                        ),
                    ):
                        with self.assertRaises(EvidenceError):
                            resolve_external_regular_file(root, relative, ())

    def test_rejects_case_insensitive_path_alias(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "Evidence.md"
            evidence.write_bytes(b"evidence\n")

            with self.assertRaisesRegex(EvidenceError, "canonical casing"):
                resolve_external_regular_file(root, "evidence.md", ())

    def test_rejects_casefold_collisions_in_campaign_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upper = root / "Evidence.md"
            lower = root / "evidence.md"
            upper.write_bytes(b"upper\n")
            try:
                lower.write_bytes(b"lower\n")
            except OSError as error:
                self.skipTest(
                    f"case-sensitive temporary directory unavailable: {error}"
                )
            if len(tuple(root.iterdir())) != 2:
                self.skipTest("case-sensitive temporary directory unavailable")

            with self.assertRaisesRegex(
                EvidenceError,
                "case-insensitive path collision",
            ):
                resolve_external_regular_file(root, "Evidence.md", ())

    def test_rejects_file_inside_git_worktree(self) -> None:
        with self.assertRaisesRegex(EvidenceError, "outside every Git worktree"):
            resolve_external_regular_file(
                ROOT,
                "AGENTS.md",
                (ROOT,),
            )

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable")
    def test_rejects_symbolic_link_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.md"
            target.write_bytes(b"target\n")
            alias = root / "alias.md"
            try:
                os.symlink(target, alias)
            except OSError as error:
                self.skipTest(f"symbolic-link creation unavailable: {error}")

            with self.assertRaisesRegex(EvidenceError, "alias"):
                resolve_external_regular_file(root, "alias.md", ())

    def test_rejects_directory_junction_ancestor_when_supported(self) -> None:
        if os.name != "nt":
            self.skipTest("Windows directory junction fixture")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "evidence.md").write_bytes(b"evidence\n")
            junction = root / "junction"
            result = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(junction), str(target)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                self.skipTest(
                    f"directory junction creation unavailable: {result.stderr}"
                )
            try:
                with self.assertRaisesRegex(EvidenceError, "alias"):
                    resolve_external_regular_file(
                        root,
                        "junction/evidence.md",
                        (),
                    )
            finally:
                os.rmdir(junction)

    def test_rejects_hard_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.md"
            target.write_bytes(b"evidence\n")
            alias = root / "alias.md"
            try:
                os.link(target, alias)
            except OSError as error:
                self.skipTest(f"hard-link creation unavailable: {error}")

            with self.assertRaisesRegex(
                EvidenceError,
                "exactly one filesystem link",
            ):
                resolve_external_regular_file(root, "target.md", ())

    def test_rejects_directory_and_missing_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "directory").mkdir()

            with self.assertRaisesRegex(EvidenceError, "regular file"):
                resolve_external_regular_file(root, "directory", ())
            with self.assertRaisesRegex(EvidenceError, "missing"):
                resolve_external_regular_file(root, "missing.md", ())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO fixture is unavailable")
    def test_rejects_device_or_other_special_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            special = root / "special"
            try:
                os.mkfifo(special)
            except OSError as error:
                self.skipTest(f"special-file creation unavailable: {error}")

            with self.assertRaisesRegex(EvidenceError, "regular file"):
                resolve_external_regular_file(root, "special", ())

    def test_fails_closed_when_link_count_cannot_be_inspected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "evidence.md"
            evidence.write_bytes(b"evidence\n")
            real_stat = Path.stat

            def stat_without_link_count(
                path: Path,
                *,
                follow_symlinks: bool = True,
            ) -> object:
                result = real_stat(path, follow_symlinks=follow_symlinks)
                if path == evidence:
                    return SimpleNamespace(st_mode=result.st_mode)
                return result

            with mock.patch.object(Path, "stat", stat_without_link_count):
                with self.assertRaisesRegex(
                    EvidenceError,
                    "exactly one filesystem link",
                ):
                    resolve_external_regular_file(
                        root,
                        "evidence.md",
                        (),
                    )

    def test_operational_diagnostics_do_not_expose_host_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "evidence.md"
            evidence.write_bytes(b"evidence\n")
            with mock.patch.object(
                Path,
                "stat",
                side_effect=PermissionError(str(root / "host-secret")),
            ):
                with self.assertRaises(EvidenceError) as raised:
                    resolve_external_regular_file(
                        root,
                        "evidence.md",
                        (),
                    )

            diagnostic = str(raised.exception)
            self.assertIn("evidence.md", diagnostic)
            self.assertNotIn(str(root), diagnostic)
            self.assertNotIn("host-secret", diagnostic)


class MarkdownParserTests(unittest.TestCase):
    def test_parses_completed_attestation_with_exact_body_bindings(self) -> None:
        result = parse_completed_attestation(
            COMPLETED_ATTESTATION.encode("utf-8")
        )

        self.assertEqual(result["reviewer_identity"], "Alice Reviewer")
        self.assertEqual(
            result["review_role"],
            "Specification and inventory review",
        )
        self.assertEqual(result["authorized_source_access"], "Yes")
        self.assertEqual(result["independence_from_mapper"], "Yes")
        self.assertEqual(result["conflicts_of_interest"], "No")
        self.assertEqual(result["project_owner_dual_role_acceptance"], "No")

    def test_parses_none_findings_specification_worksheet(self) -> None:
        worksheet = parse_completed_worksheet(
            SPECIFICATION_WORKSHEET.encode("utf-8"),
            "specification_and_inventory",
        )

        self.assertIsInstance(worksheet, CompletedWorksheet)
        self.assertEqual(worksheet.role, "specification_and_inventory")
        self.assertEqual(worksheet.reviewer_identity, "Alice Reviewer")
        self.assertEqual(worksheet.review_date, "2026-07-25")
        self.assertEqual(worksheet.conclusion, "pass")
        self.assertIsNone(worksheet.post_correction_candidate_sha)
        self.assertEqual(worksheet.findings_disposition, "No findings")
        self.assertEqual(worksheet.findings, ())
        self.assertEqual(worksheet.attestation_sha256, DIGEST)
        self.assertEqual(worksheet.signed_worksheet_sha256, DIGEST)

    def test_parses_multiple_findings_security_worksheet(self) -> None:
        worksheet = parse_completed_worksheet(
            SECURITY_WORKSHEET.encode("utf-8"),
            "security_and_overclaiming",
        )

        self.assertEqual(worksheet.conclusion, "pass_after_correction")
        self.assertEqual(worksheet.post_correction_candidate_sha, SHA)
        self.assertEqual(
            worksheet.findings,
            (
                ReviewFinding(
                    finding_id="SEC-001",
                    affected_record_ids=("ce-m-001", "ce-m-002"),
                    severity="Minor",
                    description="Ambiguous wording",
                    evidence="Record text",
                    required_action="Clarify rationale",
                    status="accepted",
                    disposition="Accepted for this release",
                    resolver_or_acceptor="Project Owner",
                    disposition_date="2026-07-25",
                    acceptance_rationale="No material mapping effect",
                ),
                ReviewFinding(
                    finding_id="SEC-002",
                    affected_record_ids=("ce-m-003",),
                    severity="Important",
                    description="Unsupported outcome",
                    evidence="Source text",
                    required_action="Correct relationship",
                    status="resolved",
                    disposition="Corrected",
                    resolver_or_acceptor="Alice Mapper",
                    disposition_date="2026-07-25",
                    acceptance_rationale="Not applicable",
                ),
            ),
        )

    def test_rejects_unknown_role_and_role_text_mismatch(self) -> None:
        with self.assertRaisesRegex(EvidenceError, "review role"):
            parse_completed_worksheet(
                SPECIFICATION_WORKSHEET.encode("utf-8"),
                "unknown",
            )
        with self.assertRaisesRegex(EvidenceError, "heading|review role"):
            parse_completed_worksheet(
                SPECIFICATION_WORKSHEET.encode("utf-8"),
                "security_and_overclaiming",
            )

    def test_rejects_duplicate_reordered_unknown_and_missing_rows(self) -> None:
        row = f"| Candidate commit SHA | {SHA} |\n"
        mutations = (
            COMPLETED_ATTESTATION.replace(row, row + row, 1),
            COMPLETED_ATTESTATION.replace(
                "| Reviewer identity | Alice Reviewer |\n"
                "| Organization | Example Assurance Ltd |\n",
                "| Organization | Example Assurance Ltd |\n"
                "| Reviewer identity | Alice Reviewer |\n",
                1,
            ),
            COMPLETED_ATTESTATION.replace(
                row,
                row + "| Unknown field | unexpected |\n",
                1,
            ),
            COMPLETED_ATTESTATION.replace(row, "", 1),
        )
        for content in mutations:
            with self.subTest(content=content[:80]):
                with self.assertRaisesRegex(EvidenceError, "row"):
                    parse_completed_attestation(content.encode("utf-8"))

    def test_rejects_duplicate_reordered_and_unknown_headings(self) -> None:
        mutations = (
            SPECIFICATION_WORKSHEET.replace(
                "## Review scope\n",
                "## Review scope\n\n## Review scope\n",
                1,
            ),
            SPECIFICATION_WORKSHEET.replace(
                "## Review scope",
                "## Unknown scope",
                1,
            ),
            SPECIFICATION_WORKSHEET.replace(
                "## Review scope",
                "## Overall conclusion",
                1,
            ),
        )
        for content in mutations:
            with self.subTest(content=content[:80]):
                with self.assertRaisesRegex(EvidenceError, "heading"):
                    parse_completed_worksheet(
                        content.encode("utf-8"),
                        "specification_and_inventory",
                    )

    def test_rejects_an_added_unknown_table(self) -> None:
        content = SPECIFICATION_WORKSHEET.replace(
            "## Review scope\n",
            "## Review scope\n\n| Unexpected | Table |\n|---|---|\n"
            "| Unknown | value |\n",
            1,
        )
        with self.assertRaisesRegex(EvidenceError, "unknown"):
            parse_completed_worksheet(
                content.encode("utf-8"),
                "specification_and_inventory",
            )

    def test_rejects_unescaped_or_escaped_pipe_ambiguity(self) -> None:
        for ambiguous in ("Alice | Reviewer", r"Alice \| Reviewer"):
            content = COMPLETED_ATTESTATION.replace(
                "Alice Reviewer",
                ambiguous,
                1,
            )
            with self.subTest(ambiguous=ambiguous):
                with self.assertRaisesRegex(EvidenceError, "pipe"):
                    parse_completed_attestation(content.encode("utf-8"))

    def test_rejects_template_markers_and_noncanonical_cell_whitespace(
        self,
    ) -> None:
        mutations = (
            COMPLETED_ATTESTATION.replace(
                "Alice Reviewer",
                "`[REQUIRED]`",
                1,
            ),
            COMPLETED_ATTESTATION.replace(
                "| Reviewer identity | Alice Reviewer |",
                "| Reviewer identity |  Alice Reviewer |",
                1,
            ),
        )
        for content in mutations:
            with self.subTest(content=content[:80]):
                with self.assertRaises(EvidenceError):
                    parse_completed_attestation(content.encode("utf-8"))

    def test_rejects_malformed_utf8_bom_cr_and_missing_final_lf(self) -> None:
        mutations = (
            b"\xff" + COMPLETED_ATTESTATION.encode("utf-8"),
            b"\xef\xbb\xbf" + COMPLETED_ATTESTATION.encode("utf-8"),
            COMPLETED_ATTESTATION.replace("\n", "\r\n").encode("utf-8"),
            COMPLETED_ATTESTATION[:-1].encode("utf-8"),
        )
        for content in mutations:
            with self.subTest(content=content[:20]):
                with self.assertRaisesRegex(EvidenceError, "UTF-8/LF"):
                    parse_completed_attestation(content)

    def test_rejects_attestation_body_answers_that_do_not_match(self) -> None:
        mutations = (
            COMPLETED_ATTESTATION.replace(
                "recorded above: Yes.",
                "recorded above: No.",
                1,
            ),
            COMPLETED_ATTESTATION.replace(
                "independent from the mapper: Yes.",
                "independent from the mapper: No.",
                1,
            ),
            COMPLETED_ATTESTATION.replace(
                "restrictions: Yes.",
                "restrictions: No.",
                1,
            ),
            COMPLETED_ATTESTATION.replace(
                "fully\ndisclosed: Yes.",
                "fully\ndisclosed: No.",
                1,
            ),
        )
        for content in mutations:
            with self.subTest(content=content[-500:]):
                with self.assertRaisesRegex(EvidenceError, "attestation"):
                    parse_completed_attestation(content.encode("utf-8"))

    def test_rejects_invalid_exact_enums_and_none_mixed_with_findings(
        self,
    ) -> None:
        invalid_enum = SECURITY_WORKSHEET.replace(
            "| SEC-001 | ce-m-001, ce-m-002 | Minor |",
            "| SEC-001 | ce-m-001, ce-m-002 | minor |",
            1,
        )
        mixed = SECURITY_WORKSHEET.replace(
            "| SEC-001 |",
            "| NONE |  |  |  |  |  |  |  |  |  |  |\n| SEC-001 |",
            1,
        )
        for content in (invalid_enum, mixed):
            with self.subTest(content=content[:80]):
                with self.assertRaises(EvidenceError):
                    parse_completed_worksheet(
                        content.encode("utf-8"),
                        "security_and_overclaiming",
                    )

    def test_completed_worksheet_is_immutable(self) -> None:
        worksheet = parse_completed_worksheet(
            SPECIFICATION_WORKSHEET.encode("utf-8"),
            "specification_and_inventory",
        )
        with self.assertRaises(AttributeError):
            worksheet.conclusion = "stop"  # type: ignore[misc]


class DataclassConversionTests(unittest.TestCase):
    def _campaign(self) -> dict[str, object]:
        finding = {
            "finding_id": "F-001",
            "affected_record_ids": ["ce-m-001"],
            "severity": "Minor",
            "status": "accepted",
            "disposition": "Accepted",
            "resolver_or_acceptor": "Project Owner",
            "disposition_date": "2026-07-25",
            "acceptance_rationale": "No material effect",
        }
        role = {
            "role": "specification_and_inventory",
            "reviewer": {
                "identity": "Alice Reviewer",
                "organization": "Example Assurance Ltd",
                "verification_locator": LOCATOR,
                "qualification": "Qualified reviewer",
                "authorized_source_access": True,
                "independent": True,
                "conflicts": False,
                "conflict_disposition": "Not applicable",
            },
            "owner_eligibility_accepted": True,
            "dual_role_accepted": False,
            "attestation": {
                "path": "attestations/core.md",
                "immutable_locator": LOCATOR,
                "retention_owner": "Records Owner",
                "sha256": DIGEST,
            },
            "worksheet": {
                "path": "worksheets/core.md",
                "immutable_locator": LOCATOR,
                "retention_owner": "Records Owner",
                "sha256": DIGEST,
                "signed_sha256": DIGEST,
                "review_date": "2026-07-25",
                "conclusion": "pass",
                "findings_disposition": "All findings reconciled",
                "findings": [finding],
            },
        }
        return {
            "schema_version": "1.0.0",
            "campaign_id": "draft-review-2026",
            "phase": "draft_review",
            "candidate_state": "draft",
            "candidate_commit": SHA,
            "retention_owner": "Records Owner",
            "retention_commitment": "Retain for the project lifetime",
            "mapping_sets": [
                {
                    "mapping_set_id": MAPPING_SET_ID,
                    "package": {
                        "root": "packages/core",
                        "manifest_path": (
                            "packages/core/PACKAGE_MANIFEST.json"
                        ),
                        "manifest_sha256": DIGEST,
                        "immutable_locator": LOCATOR,
                        "retention_owner": "Records Owner",
                    },
                    "roles": [role],
                }
            ],
        }

    def test_converts_closed_validated_mapping_to_nested_immutable_types(
        self,
    ) -> None:
        campaign = CampaignEvidence.from_mapping(self._campaign())

        self.assertIsInstance(campaign, CampaignEvidence)
        self.assertIsInstance(campaign.mapping_sets[0], MappingSetEvidence)
        role = campaign.mapping_sets[0].roles[0]
        self.assertIsInstance(role, RoleEvidence)
        self.assertIsInstance(role.reviewer, ReviewerEvidence)
        self.assertIsInstance(role.attestation, AttestationEvidence)
        self.assertEqual(role.worksheet_findings[0].finding_id, "F-001")
        with self.assertRaises(AttributeError):
            role.role = "security_and_overclaiming"  # type: ignore[misc]

    def test_conversion_rejects_non_object_missing_unknown_and_wrong_types(
        self,
    ) -> None:
        campaign = self._campaign()
        invalid_values: list[object] = [
            [],
            {key: value for key, value in campaign.items() if key != "phase"},
            {**campaign, "unknown": "field"},
            {**campaign, "candidate_commit": 123},
        ]
        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(EvidenceError):
                    CampaignEvidence.from_mapping(value)

    def test_nested_conversion_rejects_unknown_and_wrongly_typed_fields(
        self,
    ) -> None:
        campaign = self._campaign()
        mapping_set = campaign["mapping_sets"][0]  # type: ignore[index]
        role = mapping_set["roles"][0]  # type: ignore[index]
        reviewer = role["reviewer"]  # type: ignore[index]
        reviewer["unknown"] = "field"  # type: ignore[index]
        with self.assertRaises(EvidenceError):
            CampaignEvidence.from_mapping(campaign)

        campaign = self._campaign()
        mapping_set = campaign["mapping_sets"][0]  # type: ignore[index]
        role = mapping_set["roles"][0]  # type: ignore[index]
        role["dual_role_accepted"] = "false"  # type: ignore[index]
        with self.assertRaises(EvidenceError):
            CampaignEvidence.from_mapping(campaign)


class SignedWorksheetDigestTests(unittest.TestCase):
    def test_removes_exactly_one_complete_digest_row_including_lf(self) -> None:
        content = SPECIFICATION_WORKSHEET.encode("utf-8")
        excluded = (
            f"| Signed worksheet SHA-256 | {DIGEST} |\n"
        ).encode("utf-8")
        expected = hashlib.sha256(content.replace(excluded, b"", 1)).hexdigest()

        self.assertEqual(signed_worksheet_sha256(content), expected)

    def test_rejects_missing_or_duplicate_digest_row(self) -> None:
        row = f"| Signed worksheet SHA-256 | {DIGEST} |\n"
        for content in (
            SPECIFICATION_WORKSHEET.replace(row, "", 1),
            SPECIFICATION_WORKSHEET.replace(row, row + row, 1),
        ):
            with self.subTest(content=content[-500:]):
                with self.assertRaisesRegex(
                    EvidenceError,
                    "exactly one signed worksheet",
                ):
                    signed_worksheet_sha256(content.encode("utf-8"))

    def test_mutating_any_nonexcluded_byte_changes_digest(self) -> None:
        original = SPECIFICATION_WORKSHEET.encode("utf-8")
        mutated = SPECIFICATION_WORKSHEET.replace(
            "No findings",
            "No findings recorded",
            1,
        ).encode("utf-8")

        self.assertNotEqual(
            signed_worksheet_sha256(original),
            signed_worksheet_sha256(mutated),
        )


class DeterministicArchiveTests(unittest.TestCase):
    ALLOWLIST = (
        "REVIEW_EVIDENCE.json",
        "attestations/core.md",
        "packages/core/PACKAGE_MANIFEST.json",
        "worksheets/core.md",
    )
    CONTENTS = {
        "REVIEW_EVIDENCE.json": b'{"schema_version":"1.0.0"}\n',
        "attestations/core.md": b"attestation\n",
        "packages/core/PACKAGE_MANIFEST.json": b'{"files":[]}\n',
        "worksheets/core.md": b"worksheet\n",
    }

    def _write_tree(
        self,
        root: Path,
        order: tuple[str, ...],
        timestamp: int,
    ) -> None:
        for relative in order:
            path = root.joinpath(*relative.split("/"))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(self.CONTENTS[relative])
            os.utime(path, (timestamp, timestamp))

    def test_archive_bytes_ignore_creation_order_and_filesystem_timestamps(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            first = base / "first"
            second = base / "second"
            first.mkdir()
            second.mkdir()
            self._write_tree(first, self.ALLOWLIST, 1_600_000_000)
            self._write_tree(second, tuple(reversed(self.ALLOWLIST)), 1_700_000_000)

            first_archive = build_campaign_archive(first, self.ALLOWLIST)
            second_archive = build_campaign_archive(second, self.ALLOWLIST)

            self.assertEqual(first_archive, second_archive)
            with zipfile.ZipFile(io.BytesIO(first_archive)) as archive:
                self.assertEqual(archive.namelist(), sorted(self.ALLOWLIST))
                for info in archive.infolist():
                    self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                    self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                    self.assertEqual(
                        (info.external_attr >> 16) & 0o170000,
                        stat.S_IFREG,
                    )
                    self.assertEqual(
                        (info.external_attr >> 16) & 0o777,
                        0o644,
                    )
                    self.assertEqual(
                        archive.read(info.filename),
                        self.CONTENTS[info.filename],
                    )

    def test_archive_rejects_extra_or_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_tree(root, self.ALLOWLIST, 1_600_000_000)
            (root / "extra.txt").write_bytes(b"extra\n")
            with self.assertRaisesRegex(EvidenceError, "allowlist"):
                build_campaign_archive(root, self.ALLOWLIST)

            (root / "extra.txt").unlink()
            (root / "worksheets/core.md").unlink()
            with self.assertRaisesRegex(EvidenceError, "allowlist|missing"):
                build_campaign_archive(root, self.ALLOWLIST)

    def test_archive_rejects_unsafe_alias_and_casefold_allowlist_entries(
        self,
    ) -> None:
        unsafe_allowlists = (
            ("../escape.md",),
            ("/absolute.md",),
            (r"attestations\core.md",),
            ("attestations/./core.md",),
            ("attestations/core.md", "attestations/CORE.md"),
            ("attestations/core.md", "attestations/core.md"),
            ("CAMPAIGN_SEAL.json",),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for allowlist in unsafe_allowlists:
                with self.subTest(allowlist=allowlist):
                    with self.assertRaises(EvidenceError):
                        build_campaign_archive(root, allowlist)

    def test_archive_rejects_hard_links_and_symbolic_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.md"
            target.write_bytes(b"target\n")
            hardlink = root / "hardlink.md"
            try:
                os.link(target, hardlink)
            except OSError as error:
                self.skipTest(f"hard-link creation unavailable: {error}")
            with self.assertRaisesRegex(
                EvidenceError,
                "exactly one filesystem link",
            ):
                build_campaign_archive(root, ("target.md", "hardlink.md"))

        if not hasattr(os, "symlink"):
            return
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.md"
            target.write_bytes(b"target\n")
            alias = root / "alias.md"
            try:
                os.symlink(target, alias)
            except OSError:
                return
            with self.assertRaisesRegex(EvidenceError, "alias"):
                build_campaign_archive(root, ("target.md", "alias.md"))


class CanonicalSealTests(unittest.TestCase):
    def test_canonical_json_is_one_line_sorted_utf8_with_lf(self) -> None:
        self.assertEqual(
            canonical_json_bytes({"z": "é", "a": [True, 2]}),
            '{"a":[true,2],"z":"é"}\n'.encode("utf-8"),
        )
        with self.assertRaises((EvidenceError, ValueError)):
            canonical_json_bytes({"invalid": float("nan")})

    def test_builds_exact_external_non_self_referential_seal(self) -> None:
        manifest = b'{"schema_version":"1.0.0"}\n'
        archive = b"deterministic archive bytes"
        record, content = build_seal_record(
            manifest_bytes=manifest,
            archive_bytes=archive,
            archive_locator=LOCATOR,
            campaign_id="draft-review-2026",
            candidate_commit=SHA,
            evidence_valid=True,
            readiness_name="transition_ready",
            readiness_value=True,
            validator_version="1.0.0",
        )

        self.assertEqual(
            set(record),
            {
                "archive_byte_length",
                "archive_format",
                "archive_locator",
                "archive_media_type",
                "archive_sha256",
                "campaign_id",
                "candidate_commit",
                "evidence_valid",
                "manifest_sha256",
                "readiness_name",
                "readiness_value",
                "schema_version",
                "validator_version",
            },
        )
        self.assertEqual(record["archive_byte_length"], len(archive))
        self.assertEqual(
            record["archive_sha256"],
            hashlib.sha256(archive).hexdigest(),
        )
        self.assertEqual(
            record["manifest_sha256"],
            hashlib.sha256(manifest).hexdigest(),
        )
        self.assertEqual(record["archive_format"], "zip")
        self.assertEqual(record["archive_media_type"], "application/zip")
        self.assertEqual(content, canonical_json_bytes(record))
        self.assertEqual(json.loads(content), record)
        self.assertNotIn("seal", b"deterministic archive bytes".decode())

    def test_seal_rejects_invalid_sha_locator_and_value_types(self) -> None:
        valid = {
            "manifest_bytes": b"manifest\n",
            "archive_bytes": b"archive",
            "archive_locator": LOCATOR,
            "campaign_id": "draft-review-2026",
            "candidate_commit": SHA,
            "evidence_valid": True,
            "readiness_name": "transition_ready",
            "readiness_value": True,
            "validator_version": "1.0.0",
        }
        invalid_changes = (
            {"candidate_commit": "ABC"},
            {"archive_locator": "https://example.invalid/archive.zip"},
            {
                "archive_locator": (
                    "https://example.invalid/archive.zip?version=bad|value"
                )
            },
            {"evidence_valid": 1},
            {"readiness_name": 1},
            {"readiness_value": "true"},
        )
        for change in invalid_changes:
            with self.subTest(change=change):
                with self.assertRaises(EvidenceError):
                    build_seal_record(**{**valid, **change})  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
