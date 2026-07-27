# UK Qualified-Review Evidence Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Validate externally retained qualified-human review evidence for the three UK mapping sets and generate deterministic review packages from complete Draft or reviewed candidates without changing lifecycle state.

**Architecture:** Extend the existing package builder with an in-memory package assembly and explicit candidate-state contract. Add one strict external-evidence schema, a focused library for safe evidence I/O, Markdown parsing, signed digests, and deterministic sealing, then add a thin campaign validator CLI that binds those external bytes to an exact Git candidate and the reconstructed packages.

**Tech Stack:** Python 3.13+, standard library, `jsonschema`, existing ESAF crosswalk parsers and validators, `unittest`, Markdown and canonical JSON artifacts.

## Global Constraints

- Core, Plus forward, and Plus reverse remain three separate mapping sets.
- The required review disciplines are `specification_and_inventory` and `security_and_overclaiming`.
- AI output, automation, mapper self-review, and ordinary pull-request review do not satisfy qualified human review.
- The repository shall not contain completed attestations, signed worksheets, external source documents, or licensed source text.
- `draft_review` and `final_reviewed_confirmation` are separate preserved campaigns.
- A Draft campaign derives `evidence_valid` and `transition_ready`; a final confirmation derives `evidence_valid` and `merge_ready`.
- Valid `stop` evidence may record open Critical or Important findings but is never transition-ready or merge-ready.
- Reviewed candidates shall reject open or accepted Critical and Important findings.
- All evidence and package files shall be regular files with link count exactly one and shall remain outside every Git worktree.
- All repository-sourced bytes shall come from an exact Git commit, never mutable working-tree content.
- All three mapping sets and all 404 records remain `draft` during this implementation.
- No approval, publication, compliance, certification, equivalence, endorsement, or scheme assurance claim may be added.

---

### Task 1: Add candidate-state package assembly

**Files:**
- Modify: `tools/build_mapping_review_bundle.py`
- Modify: `tests/test_build_mapping_review_bundle.py`

**Interfaces:**
- Produces: `CandidateState = Literal["draft", "reviewed"]`
- Produces: `PackageAssembly(payloads: tuple[PackageFile, ...], manifest: dict[str, object], manifest_bytes: bytes)`
- Produces: `assemble_package(reader: GitReader, commit: str, profile: MappingProfile, candidate_state: CandidateState = "draft") -> PackageAssembly`
- Modifies: `write_package(..., candidate_state: CandidateState = "draft") -> dict[str, object]`
- CLI: optional `--candidate-state {draft,reviewed}`, default `draft`

- [ ] **Step 1: Write failing tests for the new state contract**

Add focused tests that prove the current Draft path remains the default and that
unknown states fail:

```python
default_result = bundle_builder.main([
    "--commit", self.head,
    "--mapping-set-id", CORE_ID,
    "--output", str(self.default_output),
])
self.assertEqual(default_result, 0)
self.assertEqual(
    json.loads((self.default_output / "PACKAGE_MANIFEST.json").read_bytes())[
        "candidate_state"
    ],
    "draft",
)

def test_cli_defaults_to_draft_and_rejects_unknown_candidate_state(self) -> None:
    parser_result = bundle_builder.main([
        "--commit", self.head,
        "--mapping-set-id", CORE_ID,
        "--output", str(self.output),
        "--candidate-state", "approved",
    ])
    self.assertEqual(parser_result, 2)
    self.assertFalse(self.output.exists())
```

Add an in-memory assembly test:

```python
assembly = assemble_package(self.reader, self.head, PROFILES[CORE_ID])
self.assertEqual(assembly.manifest["candidate_state"], "draft")
self.assertNotIn(
    "PACKAGE_MANIFEST.json",
    {item.path for item in assembly.payloads},
)
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest `
  tests.test_build_mapping_review_bundle.PackageWriterTests.test_cli_defaults_to_draft_and_rejects_unknown_candidate_state `
  tests.test_build_mapping_review_bundle.PackageWriterTests.test_assembly_is_in_memory_and_manifest_self_excludes -v
```

Expected: import or signature failures because `PackageAssembly`,
`assemble_package`, and `--candidate-state` do not exist.

- [ ] **Step 3: Extract deterministic in-memory assembly**

Add:

```python
from typing import Literal, NamedTuple

CandidateState = Literal["draft", "reviewed"]

class PackageAssembly(NamedTuple):
    payloads: tuple[PackageFile, ...]
    manifest: dict[str, object]
    manifest_bytes: bytes
```

Move collection, `PACKAGE_INDEX.md` rendering, and manifest construction out of
`write_package` into `assemble_package`. Keep filesystem publication in
`write_package`. Add `candidate_state` to `PACKAGE_MANIFEST.json` and the package
index metadata table. Bump `GENERATOR_VERSION` to `1.2.0` and the package
manifest `schema_version` to `1.1.0`.

Make pure package assembly repository-injectable: use `reader.root` wherever a
candidate-sourced helper currently uses module `ROOT`. Keep execution-state
checks only in the writing CLI path, where `GitReader(ROOT)` remains the
production reader. Tests may therefore assemble from an isolated temporary Git
repository without weakening production publication checks.

- [ ] **Step 4: Add reviewed-candidate validation tests**

Build a temporary Git repository fixture from one mapping set. Mutate the
snapshot and all records to `reviewed`, add complete schema-valid reviewer
objects, refresh the registry snapshot digest and generated catalog, then assert
reviewed assembly succeeds.

Add separate mutations for:

- mixed Draft/reviewed records;
- missing snapshot reviewer;
- missing provision reviewer;
- `approved` snapshot or record;
- open Critical;
- accepted Critical;
- open Important;
- accepted Important; and
- nonempty lifecycle events.

Also mutate every required reviewer field and both candidate-sourced
`mapping-set.schema.json` and `mapping-record.schema.json` constraints. Each
mutation shall raise `ValueError` with a stable content-focused message.

- [ ] **Step 5: Implement reviewed-state validation**

Replace `_require_draft` with:

```python
def _require_candidate_state(
    metadata: dict[str, object],
    mapping_set_id: str,
    subject: str,
    candidate_state: CandidateState,
) -> None:
    if metadata.get("mapping_set_id") != mapping_set_id:
        raise ValueError(f"{subject} mapping-set identifier mismatch")
    if metadata.get("status") != candidate_state:
        raise ValueError(f"{subject} must be {candidate_state}")
    reviewer = metadata.get("reviewer")
    if candidate_state == "draft" and reviewer is not None:
        raise ValueError(f"{subject} Draft content cannot contain reviewer metadata")
    if candidate_state == "reviewed" and not isinstance(reviewer, dict):
        raise ValueError(f"{subject} reviewed content requires reviewer metadata")
```

Load and validate the candidate bytes against the candidate-sourced mapping-set
and mapping-record schemas before applying the state-specific checks. Use the
existing findings semantics to reject open or accepted Critical and Important
findings. Require the registry event array to remain empty for both accepted
states.

Render state-specific lifecycle prose. Draft output retains “remains Draft.”
Reviewed output states that the mapping is reviewed but is not approved,
published, certified, compliant, equivalent, endorsed, or assured.

- [ ] **Step 6: Run focused package tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest tests.test_build_mapping_review_bundle -v
```

Expected: all package tests pass, including unchanged Draft package behavior.

- [ ] **Step 7: Commit Task 1**

```powershell
git add tools/build_mapping_review_bundle.py tests/test_build_mapping_review_bundle.py
git commit -m "feat: support reviewed mapping review packages"
```

---

### Task 2: Define the external evidence contract

**Files:**
- Create: `crosswalks/schema/qualified-review-evidence.schema.json`
- Modify: `crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md`
- Modify: `crosswalks/reviews/templates/REVIEWER_ATTESTATION.md`
- Modify: `crosswalks/reviews/templates/SPECIFICATION_INVENTORY_REVIEW.md`
- Modify: `crosswalks/reviews/templates/SECURITY_OVERCLAIMING_REVIEW.md`
- Modify: `tests/test_mapping_review_protocol.py`
- Create: `tests/test_qualified_review_evidence_schema.py`

**Interfaces:**
- Produces schema ID: `https://esaf-standard.org/schemas/qualified-review-evidence.schema.json`
- Produces phases: `draft_review`, `final_reviewed_confirmation`
- Produces roles: `specification_and_inventory`, `security_and_overclaiming`
- Produces conclusions: `pass`, `pass_after_correction`, `stop`
- Produces canonical `CAMPAIGN_SEAL.json` contract version `1.0.0`

- [ ] **Step 1: Write failing schema and protocol tests**

Create a literal valid campaign fixture with the exact three mapping-set IDs and
six role records. Test:

```python
Draft202012Validator.check_schema(self.schema)
self.validator.validate(self.valid_draft_campaign)
```

Add literal negative fixtures for an extra property, missing role, duplicate
mapping set, malformed SHA, unsafe local path, invalid locator, missing
retention owner, and a final campaign without a Draft campaign reference.

Update protocol tests to require:

- the two campaign phases;
- `evidence_valid`, `transition_ready`, and `merge_ready`;
- valid `stop` evidence;
- the external seal sequence;
- the exact reviewer-field binding rule; and
- the prohibition on lifecycle transition by this preparation.

- [ ] **Step 2: Run schema and protocol tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest `
  tests.test_mapping_review_protocol `
  tests.test_qualified_review_evidence_schema -v
```

Expected: missing schema and missing protocol/template fields.

- [ ] **Step 3: Add the strict JSON Schema**

Use Draft 2020-12, `additionalProperties: false` at every object boundary, exact
enums, full lowercase SHA patterns, canonical relative-path patterns, and
conditional requirements:

```json
{
  "if": {"properties": {"phase": {"const": "final_reviewed_confirmation"}}},
  "then": {
    "properties": {"candidate_state": {"const": "reviewed"}},
    "required": ["draft_campaign_reference"]
  },
  "else": {
    "properties": {"candidate_state": {"const": "draft"}},
    "not": {"required": ["draft_campaign_reference"]}
  }
}
```

Require exactly three mapping-set entries and exactly two role records per
entry. Semantic uniqueness remains a validator responsibility in Task 4.

Use this closed object model, with no additional properties:

```text
Campaign
  schema_version, campaign_id, phase, candidate_state, candidate_commit
  retention_owner, retention_commitment, mapping_sets[]
  draft_campaign_reference?  # final phase only
DraftCampaignReference
  campaign_id, candidate_commit, manifest_sha256, seal_record_sha256
MappingSetEvidence
  mapping_set_id, package, roles[2]
PackageEvidence
  root, manifest_path, manifest_sha256, immutable_locator, retention_owner
RoleEvidence
  role, reviewer, owner_eligibility_accepted, dual_role_accepted
  attestation, worksheet
ReviewerEvidence
  identity, organization, verification_locator, qualification
  authorized_source_access, independent, conflicts, conflict_disposition
AttestationEvidence
  path, immutable_locator, retention_owner, sha256
WorksheetEvidence
  path, immutable_locator, retention_owner, sha256, signed_sha256
  review_date, conclusion, post_correction_candidate_sha?
  findings_disposition, findings[]
FindingEvidence
  finding_id, affected_record_ids, severity, status, disposition
  resolver_or_acceptor, disposition_date, acceptance_rationale
```

Define exact scalar formats and enums in `$defs`. Use booleans for affirmative
acceptances and access/independence, require `conflict_disposition` to be
`Not applicable` when no conflict is declared, and require a nonempty
disposition otherwise. `dual_role_accepted` is false for a unique reviewer and
must be true on both role records when the same identity fills both disciplines.
The schema fixture in Step 1 shall spell out every object and field rather than
using a fixture builder.

- [ ] **Step 4: Close the Markdown template grammar**

Convert the worksheet conclusion into a fixed table:

```markdown
| Overall conclusion | `[REQUIRED: pass / pass_after_correction / stop]` |
| Post-correction candidate SHA | `[REQUIRED for pass_after_correction; otherwise Not applicable]` |
| Reviewer metadata findings disposition | `[REQUIRED: concise disposition of all findings]` |
```

Add exact immutable-locator, retention-owner, attestation digest, and package
digest rows required by the schema. Keep all values single-line and retain the
signed-worksheet digest row-exclusion rule.

- [ ] **Step 5: Update the qualified-review protocol**

Document the two-stage campaign, external evidence boundary, valid-stop versus
readiness distinction, reviewer-object mapping, final reviewed-head
confirmation, sealing sequence, and stop conditions. State that automation
checks consistency but cannot establish human identity, qualification, source
authorization, signature effect, or non-infringement.

- [ ] **Step 6: Run contract tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest `
  tests.test_mapping_review_protocol `
  tests.test_qualified_review_evidence_schema -v
```

Expected: all tests pass.

- [ ] **Step 7: Add the evidence contract to generated packages**

Add the schema to every generated package, assert its exact manifest purpose
and candidate-sourced bytes, and rerun:

```powershell
python -m unittest tests.test_build_mapping_review_bundle -v
```

- [ ] **Step 8: Commit Task 2**

```powershell
git add crosswalks/schema/qualified-review-evidence.schema.json `
  crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md `
  crosswalks/reviews/templates `
  tests/test_mapping_review_protocol.py `
  tests/test_qualified_review_evidence_schema.py `
  tools/build_mapping_review_bundle.py `
  tests/test_build_mapping_review_bundle.py
git commit -m "docs: define qualified-review evidence contract"
```

---

### Task 3: Implement safe evidence I/O, Markdown parsing, and sealing

**Files:**
- Create: `tools/crosswalks/qualified_review_evidence.py`
- Create: `tests/test_qualified_review_evidence_io.py`

**Interfaces:**
- Produces immutable dataclasses: `ReviewerEvidence`, `AttestationEvidence`,
  `ReviewFinding`, `CompletedWorksheet`, `RoleEvidence`,
  `MappingSetEvidence`, and `CampaignEvidence`
- Produces: `resolve_external_regular_file(root: Path, relative: str, worktrees: tuple[Path, ...]) -> Path`
- Produces: `parse_completed_attestation(content: bytes) -> dict[str, str]`
- Produces: `parse_completed_worksheet(content: bytes, role: str) -> CompletedWorksheet`
- Produces: `signed_worksheet_sha256(content: bytes) -> str`
- Produces: `canonical_json_bytes(value: object) -> bytes`
- Produces: `build_campaign_archive(root: Path, allowlist: tuple[str, ...]) -> bytes`
- Produces: `build_seal_record(...) -> tuple[dict[str, object], bytes]`

`CompletedWorksheet` shall contain `role`, `reviewer_identity`, `review_date`,
`conclusion`, optional `post_correction_candidate_sha`,
`findings_disposition`, `findings`, and the declared full-file and
signed-worksheet digests. The remaining dataclasses shall mirror the exact
closed schema objects from Task 2; conversion from validated JSON into these
types shall reject missing, unknown, or incorrectly typed fields.

- [ ] **Step 1: Write failing path-safety tests**

Use real temporary files and assert rejection of:

- absolute and parent-traversal paths;
- Windows drive and UNC paths;
- case-insensitive collisions;
- paths inside any Git worktree;
- symbolic links;
- directory junctions when supported;
- hard links with `st_nlink > 1`;
- directories, devices, and missing files; and
- platforms where reliable link-count inspection is unavailable.

The positive case shall resolve one single-link regular file beneath an external
temporary root.

- [ ] **Step 2: Run the path tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest tests.test_qualified_review_evidence_io.ExternalPathTests -v
```

Expected: import failure because the evidence module does not exist.

- [ ] **Step 3: Implement canonical path and regular-file checks**

Use lexical path validation before resolution, then `lstat`, ancestor
reparse-point checks, containment, and:

```python
stat_result = path.stat(follow_symlinks=False)
if not stat.S_ISREG(stat_result.st_mode):
    raise EvidenceError(f"{subject} must be a regular file")
if not hasattr(stat_result, "st_nlink") or stat_result.st_nlink != 1:
    raise EvidenceError(f"{subject} must have exactly one filesystem link")
```

Return diagnostics containing only the field name and campaign-relative path.

- [ ] **Step 4: Write failing strict Markdown parser tests**

Use completed literal copies of all three templates. Test exact heading order,
exact ordered table rows, unique fields, one-line cells, exact enums, matching
body attestations, `NONE` findings, multiple finding rows, escaped-pipe
rejection, duplicate row rejection, template-marker rejection, and malformed
UTF-8/CR rejection.

- [ ] **Step 5: Implement the strict Markdown parsers**

Define immutable row-order tuples and return normalized values without silently
rewriting case or whitespace. Parse findings into:

```python
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
```

- [ ] **Step 6: Write and implement signed-digest tests**

Prove the digest removes exactly one complete
`| Signed worksheet SHA-256 |` row including its LF. Reject missing or duplicate
digest rows. Mutating any other byte shall change the result.

- [ ] **Step 7: Write failing deterministic archive tests**

Create the same allowlisted campaign tree twice with different creation order
and filesystem timestamps. Assert identical ZIP bytes and inspect every entry:

```python
self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
self.assertEqual((info.external_attr >> 16) & 0o170000, stat.S_IFREG)
```

Reject extra files, duplicate case-folded names, aliases, links, and unsafe
archive entries.

- [ ] **Step 8: Implement canonical sealing**

Build sorted `ZIP_STORED` entries with fixed metadata and implicit directories.
Build the exact `1.0.0` seal record from the design, serialize it as one-line
sorted canonical JSON plus LF, and keep the seal outside the archive.

- [ ] **Step 9: Run Task 3 tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest tests.test_qualified_review_evidence_io -v
```

Expected: all tests pass with platform-specific link/junction tests skipped only
when the platform cannot create the test fixture. Production validation still
fails closed if it cannot inspect link counts.

- [ ] **Step 10: Commit Task 3**

```powershell
git add tools/crosswalks/qualified_review_evidence.py `
  tests/test_qualified_review_evidence_io.py
git commit -m "feat: validate and seal external review evidence"
```

---

### Task 4: Validate complete campaigns against exact Git candidates

**Files:**
- Create: `tools/validate_qualified_review_evidence.py`
- Create: `tools/seal_qualified_review_campaign.py`
- Create: `tests/test_validate_qualified_review_evidence.py`
- Modify: `tools/crosswalks/qualified_review_evidence.py`

**Interfaces:**
- Produces: `ValidationReport(evidence_valid: bool, readiness_name: str, readiness_value: bool, candidate_commit: str, campaign_id: str, errors: tuple[str, ...])`
- Produces: `validate_campaign(reader: GitReader, candidate: str, evidence_root: Path, draft_evidence_root: Path | None = None, draft_seal_record: Path | None = None, draft_archive: Path | None = None) -> ValidationReport`
- CLI exit codes: `0` valid evidence, `1` content-invalid evidence, `2` operational error
- Seal CLI: validates a campaign, atomically publishes one new directory
  containing deterministic `CAMPAIGN_ARCHIVE.zip` and canonical
  `CAMPAIGN_SEAL.json`, and refuses an existing destination

- [ ] **Step 1: Write a valid end-to-end Draft campaign fixture**

Generate the three packages from a temporary clean checkout of the exact test
candidate. Create six completed role records, attestations, and worksheets with
correct digests. Assert:

```python
report = validate_campaign(self.reader, self.candidate, self.campaign_root)
self.assertTrue(report.evidence_valid)
self.assertEqual(report.readiness_name, "transition_ready")
self.assertTrue(report.readiness_value)
```

- [ ] **Step 2: Run the valid-campaign test and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest `
  tests.test_validate_qualified_review_evidence.CampaignValidationTests.test_valid_draft_campaign_is_transition_ready -v
```

Expected: import failure because the validator does not exist.

- [ ] **Step 3: Implement schema loading and exact candidate binding**

Load the tracked schema from the exact candidate through `GitReader`, validate
the manifest, resolve the full SHA, and confirm the three mapping-set IDs and
candidate state. Do not read repository working-tree bytes.

- [ ] **Step 4: Implement full campaign-tree and package verification**

Build one exact allowlist from the campaign manifest, attestations, worksheets,
package manifests, package payloads, and package-manifest files. Reject every
unlisted entry and every extension outside `.md` and `.json`.

Reconstruct each expected package through `assemble_package`, then compare:

- package manifest bytes and digest;
- candidate, state, ID, direction, and expected count;
- ordered manifest entry path, purpose, bytes, and SHA-256; and
- every payload byte.

- [ ] **Step 5: Add mutation tests for role and reviewer eligibility**

Test missing/duplicate roles, mismatched set IDs, unauthorized source access,
mapper self-review, unresolved conflicts, rejected owner eligibility, duplicate
human identities without dual-role acceptance, and duplicate identities with
incomplete dual qualifications.

- [ ] **Step 6: Implement six-role and dual-role semantics**

Use exact `(mapping_set_id, role)` keys. Derive the reviewer metadata expected
by reviewed content:

```python
{
    "id": role.reviewer.identity,
    "date": role.worksheet.review_date,
    "qualification": role.reviewer.qualification,
    "authorized_source_access": role.reviewer.authorized_source_access,
    "findings_disposition": role.worksheet.findings_disposition,
}
```

Require semantic equality with the mapping-set reviewer for
`specification_and_inventory` and with every record reviewer for
`security_and_overclaiming`.

- [ ] **Step 7: Add finding and readiness mutation tests**

Cover:

- `stop` plus open Critical is evidence-valid and not transition-ready;
- `stop` plus open Important is evidence-valid and not transition-ready;
- accepted Critical or Important makes the campaign evidence-invalid;
- accepted Minor requires acceptor, rationale, and date;
- `pass` rejects unresolved findings;
- `pass_after_correction` requires the exact post-correction campaign candidate
  SHA, whether the campaign phase is Draft or reviewed;
- orphan affected-record IDs fail;
- transition-ready findings equal authoritative candidate findings; and
- a reviewed final campaign derives `merge_ready`.

- [ ] **Step 8: Implement findings reconciliation and phase outcomes**

Resolve every affected record ID within its mapping set. Compare normalized
worksheet findings with authoritative snapshot findings only when the campaign
claims readiness. Preserve valid `stop` evidence without pretending the new
finding already existed in the reviewed candidate.

- [ ] **Step 9: Add final-confirmation recursion and seal tests**

Create a preserved valid Draft campaign and seal, then a reviewed fixture and
final campaign. Assert recursive Draft validation, manifest/seal digest
agreement, different exact SHAs, deterministic archive reconstruction, and
`merge_ready: true`.

Mutate each reference field, archive byte, seal field, validator version, and
Draft campaign byte. Each mutation shall fail.

- [ ] **Step 10: Implement final-confirmation recursion**

Require `--draft-evidence-root`, `--draft-seal-record`, and `--draft-archive`
only for `final_reviewed_confirmation`. Recursively validate the Draft campaign,
rebuild its archive, compare it byte-for-byte with the retained archive,
validate the exact seal, then validate reviewed candidate metadata and both
role confirmations.

- [ ] **Step 11: Add CLI and sanitized-error tests**

Test exit codes, canonical one-line JSON report output, missing paths,
permission failures, malformed evidence, all-or-none
`--draft-evidence-root`/`--draft-seal-record`/`--draft-archive` arguments, and
no host-path disclosure.

- [ ] **Step 12: Implement the CLI**

The CLI shall require `--check`; it shall never write evidence or mapping
content. Print one canonical JSON report on stdout for valid or content-invalid
evidence and one concise sanitized line on stderr for operational errors.

- [ ] **Step 13: Write and implement seal CLI tests**

Test that sealing refuses invalid or non-ready campaigns, an existing output
directory, output inside a worktree, unsafe archive locators, and
execution-state drift. A valid ready campaign shall produce the exact
deterministic ZIP and canonical seal bytes returned by the Task 3 library.
Revalidation shall reconstruct and compare those bytes.

Create both files in a new sibling staging directory on the destination
filesystem, fsync the complete files where supported, repeat the candidate
execution-state check, and atomically rename that staging directory to the new
destination. The destination parent must already exist and be external to every
worktree; arbitrary split destinations and cross-filesystem publication are not
supported.

Implement:

```powershell
$candidateSha = git rev-parse HEAD
$campaignRoot = "D:\ESAF-review-evidence\issue-55\draft"
$sealedOutput = "D:\ESAF-review-evidence\issue-55\sealed-draft"
$archiveLocator = "https://evidence.example.invalid/esaf/issue-55/draft-campaign.zip"

python tools/seal_qualified_review_campaign.py `
  --candidate $candidateSha `
  --evidence-root $campaignRoot `
  --output-directory $sealedOutput `
  --archive-locator $archiveLocator
```

The command shall use exclusive writes and publish neither output unless both
bytes are complete and the execution state still matches the candidate.

- [ ] **Step 14: Run Task 4 tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest `
  tests.test_qualified_review_evidence_schema `
  tests.test_qualified_review_evidence_io `
  tests.test_validate_qualified_review_evidence -v
```

Expected: all tests pass.

- [ ] **Step 15: Commit Task 4**

```powershell
git add tools/validate_qualified_review_evidence.py `
  tools/seal_qualified_review_campaign.py `
  tools/crosswalks/qualified_review_evidence.py `
  tests/test_validate_qualified_review_evidence.py
git commit -m "feat: validate qualified-review campaigns"
```

---

### Task 5: Document and integrate the capability

**Files:**
- Modify: `tools/README.md`
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tests/test_mapping_review_protocol.py`
- Modify: `tests/test_release_metadata.py`
- Modify: `project/BACKLOG.md` only if wording must distinguish mechanical readiness from completed human review

**Interfaces:**
- Documents exact Draft package command, reviewed package command, evidence
  validation commands, final confirmation inputs, sealing output, and human-only
  stop conditions.
- CI path filters include the new validator and evidence library.

- [ ] **Step 1: Write failing documentation and workflow contract tests**

Require the README to contain these commands:

```text
python tools/build_mapping_review_bundle.py --candidate-state draft
python tools/build_mapping_review_bundle.py --candidate-state reviewed
python tools/validate_qualified_review_evidence.py --check
python tools/seal_qualified_review_campaign.py
--draft-evidence-root
--draft-seal-record
--draft-archive
```

Require workflow path filters for:

- `tools/build_mapping_review_bundle.py`;
- `tools/validate_qualified_review_evidence.py`;
- `tools/seal_qualified_review_campaign.py`; and
- `tools/crosswalks/qualified_review_evidence.py`.

Do not add a CI execution step that needs private external evidence.

- [ ] **Step 2: Run the contract tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest `
  tests.test_mapping_review_protocol `
  tests.test_release_metadata -v
```

Expected: missing command and path-filter assertions fail.

- [ ] **Step 3: Update operator documentation**

Document:

- campaign directory layout;
- safe external location requirements;
- Draft validation and `transition_ready`;
- valid `stop` handling;
- deterministic sealing and external evidence record;
- reviewed package generation;
- final recursive confirmation and `merge_ready`;
- evidence that automation cannot establish; and
- the prohibition on storing source documents or completed human evidence in
  Git.

- [ ] **Step 4: Update workflow path filters**

Add the three exact tool paths to both pull-request and `main` push filters.
The full unit suite exercises the validator with fictional external fixtures.

- [ ] **Step 5: Run focused integration tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest `
  tests.test_mapping_review_protocol `
  tests.test_build_mapping_review_bundle `
  tests.test_qualified_review_evidence_schema `
  tests.test_qualified_review_evidence_io `
  tests.test_validate_qualified_review_evidence `
  tests.test_release_metadata -v
```

- [ ] **Step 6: Commit Task 5**

```powershell
git add tools/README.md .github/workflows/catalog-validation.yml `
  tests/test_mapping_review_protocol.py tests/test_release_metadata.py
# Add project/BACKLOG.md only when Step 3 changed it.
git commit -m "docs: integrate qualified-review evidence validation"
```

---

### Task 6: Review, validate, and publish the engineering capability

**Files:**
- Review: complete diff from the computed merge base through `HEAD`
- Create after exact-SHA review if required by repository convention:
  `docs/superpowers/reviews/2026-07-25-uk-qualified-review-evidence-gate-review.md`

**Interfaces:**
- Produces one exact reviewed PR head with no unresolved Critical or Important
  findings.

- [ ] **Step 1: Run focused validation**

Run the Task 5 focused command and:

```powershell
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref origin/main
python tools/validate_links.py --check
$mergeBase = git merge-base origin/main HEAD
git diff --check "$mergeBase..HEAD"
```

- [ ] **Step 2: Run the full suite**

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest discover -s tests -v
```

Expected: all tests pass, with only documented platform skips.

- [ ] **Step 3: Freeze the substantive candidate**

Record:

- full candidate SHA;
- evidence schema SHA-256;
- validator and package-builder SHA-256;
- focused and full-suite results; and
- catalog counts.

- [ ] **Step 4: Dispatch independent exact-SHA reviews**

Require separate:

1. specification and implementation review of the evidence model, campaign
   phases, package reconstruction, and human-only boundaries;
2. security review of path handling, links, sealing, archive construction,
   source protection, findings, and overclaiming.

Resolve every Critical and Important finding test-first. Any candidate mutation
requires both reviews again.

- [ ] **Step 5: Push and open a ready pull request**

The PR shall link issue 55 but shall not close it. Record the exact reviewed
head, validation results, boundaries, and the remaining named-human blocker.

- [ ] **Step 6: Merge only after GitHub checks pass**

Verify the PR head equals the independently reviewed SHA and merge state is
clean. Merge using the repository's normal merge-commit strategy.

- [ ] **Step 7: Validate updated main**

Switch to the primary checkout, update local `main`, rerun focused
validator/package tests and proportional standalone validators, and verify a
clean primary worktree. Retain the feature worktree until Task 7 completes.

---

### Task 7: Refresh exact-SHA Draft packages and update issue 55

**Files:**
- External outputs only: three new package directories outside every worktree
- GitHub issue update: issue `tdistress/ESAF#55`
- No repository file changes

**Interfaces:**
- Produces three deterministic Draft packages from one clean merged `main` SHA.
- Produces one issue comment with candidate SHA, package digests, directions,
  payload counts, validation, and the remaining human-only blocker.

- [ ] **Step 1: Freeze clean merged main**

```powershell
git checkout main
git pull --ff-only origin main
$candidate = git rev-parse HEAD
git status --short
```

Require an empty status and a full 40-character SHA.

- [ ] **Step 2: Generate the three external Draft packages**

Use three new output directories beneath one newly created temporary campaign
parent outside every worktree:

```powershell
$campaignParent = Join-Path $env:TEMP ("esaf-issue55-" + [guid]::NewGuid())
$coreOutput = Join-Path $campaignParent "core"
$plusForwardOutput = Join-Path $campaignParent "plus-forward"
$plusReverseOutput = Join-Path $campaignParent "plus-reverse"
New-Item -ItemType Directory -Path $campaignParent | Out-Null

python tools/build_mapping_review_bundle.py `
  --commit $candidate `
  --mapping-set-id "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0" `
  --candidate-state draft `
  --output $coreOutput

python tools/build_mapping_review_bundle.py `
  --commit $candidate `
  --mapping-set-id "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0" `
  --candidate-state draft `
  --output $plusForwardOutput

python tools/build_mapping_review_bundle.py `
  --commit $candidate `
  --mapping-set-id "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0" `
  --candidate-state draft `
  --output $plusReverseOutput
```

Run once for each exact mapping-set ID. Preserve each JSON report.

- [ ] **Step 3: Independently regenerate and compare**

Generate a second set in a different external parent. Compare every file path
and byte, including each `PACKAGE_MANIFEST.json`. Require byte-identical output.

- [ ] **Step 4: Validate package boundaries**

Confirm:

- Core direction `esaf_to_external`, 116 provisions;
- Plus forward direction `esaf_to_external`, 144 provisions;
- Plus reverse direction `external_to_esaf`, 144 provisions;
- no external source document;
- no completed attestation or worksheet;
- candidate state `draft`; and
- manifest payload counts and digests agree.

- [ ] **Step 5: Update issue 55**

Post one concise issue comment with:

- exact merged candidate SHA;
- all three mapping-set IDs and directions;
- package-manifest SHA-256 values and payload counts;
- commands and validation results;
- the new evidence-gate PR link; and
- the explicit remaining requirement for named qualified humans and six
  separately recorded role dispositions.

State that the packages remain Draft preparation and do not establish review,
approval, certification, compliance, equivalence, endorsement, or assurance.

- [ ] **Step 6: Stop at the human boundary**

Do not populate reviewer fields or transition lifecycle state. Issue 55 remains
open pending eligible humans and signed exact-SHA evidence.

- [ ] **Step 7: Clean up the completed feature branch**

After the issue comment succeeds and the primary checkout remains clean, remove
the feature worktree, local feature branch, and remote feature branch. Confirm
that local `main` still equals the merged remote head.
