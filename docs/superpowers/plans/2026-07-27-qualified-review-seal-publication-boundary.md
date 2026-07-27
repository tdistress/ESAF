# Qualified-review seal publication boundary implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the normative qualified-review protocol and operator guidance with the approved distinction between local archive-and-seal materialization and external seal publication.

**Architecture:** Keep the existing offline sealing CLI and its atomic no-clobber materialization to a local external directory. Clarify that CLI success creates a local archive-and-seal pair only. The operator must upload and verify the exact archive before publishing or relying on the seal.

**Tech Stack:** Markdown, Python 3.13+, `unittest`

## Global constraints

- Markdown remains the authoritative source.
- The sealing CLI shall continue to atomically materialize `CAMPAIGN_ARCHIVE.zip` and `CAMPAIGN_SEAL.json` together in one new external output directory.
- The sealing CLI shall not access private external evidence systems or claim that an archive was uploaded, retained, or externally verified.
- A seal shall not be published or relied upon until the exact archive has been uploaded and its SHA-256 and byte length have been verified against the seal.
- Upload failure, absence, or mismatch shall leave the local seal unpublished and unusable.
- A changed archive byte or reserved locator shall require a new archive and seal in a new output directory.
- Source documents and completed human evidence shall remain outside Git.
- Automation shall not claim human identity, qualification, authorization, signature effect, retention truth, or external-object availability.

---

### Task 1: Align protocol, operator guidance, and contract tests

**Files:**
- Modify: `crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md`
- Modify: `tools/README.md`
- Modify: `tests/test_mapping_review_protocol.py`

**Interfaces:**
- Consumes: the approved design in `docs/superpowers/specs/2026-07-25-uk-qualified-review-evidence-gate-design.md`
- Preserves: `python tools/seal_qualified_review_campaign.py --candidate ... --evidence-root ... --output-directory ... --archive-locator ...`
- Produces: one consistent normative and operator sequence for local materialization, archive upload verification, and external seal publication

- [ ] **Step 1: Strengthen the protocol contract test**

Update `MappingReviewProtocolTests.test_protocol_defines_qualified_review_evidence_campaign` in `tests/test_mapping_review_protocol.py`.

Remove the assertion that requires this obsolete sequence:

```text
create and hash the deterministic archive, upload the archive to its immutable locator, then write `CAMPAIGN_SEAL.json`
```

Require the protocol section to state these observable contracts:

```text
local materialization
external publication
CLI success
does not establish upload
upload the exact archive bytes
SHA-256 and byte length
publish or rely on the seal
unpublished and unusable
new output directory
```

Keep the existing assertions for the seal filename, exact key set, canonical JSON, deterministic archive, external evidence record, and no lifecycle transition.

- [ ] **Step 2: Add an operator-guidance contract**

Extend `MappingReviewProtocolTests.test_tools_readme_documents_qualified_review_evidence_commands` so the qualified-review section requires these operator outcomes:

```text
locally materialized
does not establish upload
publish or rely on the seal
unpublished and unusable
new output directory
```

The test shall continue to require the exact Draft, reviewed, validation, sealing, and final-confirmation command tokens from the existing Task 5 brief.

- [ ] **Step 3: Run the focused contract tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest `
  tests.test_mapping_review_protocol.MappingReviewProtocolTests.test_protocol_defines_qualified_review_evidence_campaign `
  tests.test_mapping_review_protocol.MappingReviewProtocolTests.test_tools_readme_documents_qualified_review_evidence_commands -v
```

Expected: both tests fail because the normative protocol and README do not yet state the complete approved materialization and publication contract.

- [ ] **Step 4: Amend the normative protocol**

Rewrite `## External sealing sequence` in `crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md` to specify:

1. reserve a syntactically valid immutable locator;
2. validate one exact campaign snapshot;
3. atomically materialize the deterministic archive and canonical seal from that same snapshot in one new external output directory;
4. treat CLI success as local materialization only;
5. upload the exact archive bytes to the reserved locator;
6. verify the durable object's SHA-256 and byte length against the seal;
7. publish or rely on the seal only after successful verification; and
8. record the seal-record SHA-256, durable locator, and completion of archive upload verification in the external issue or pull-request evidence record.

State that upload failure, absence, or mismatch leaves the local seal unpublished and unusable. A changed archive byte or locator requires a newly materialized pair in a new output directory. Offline validation does not establish remote availability or external verification.

Preserve the exact `1.0.0` seal key set and deterministic archive requirements.

- [ ] **Step 5: Align the operator README**

Update `### Seal the Draft campaign` in `tools/README.md` without changing the command.

Use `materialize` for the CLI's local operation. State directly that:

- success creates the local pair but does not establish upload;
- the operator uploads the exact archive and verifies digest and length;
- the seal remains unpublished and unusable on upload failure, absence, or mismatch;
- the operator may publish or rely on the seal only after verification; and
- a changed archive byte or locator requires a new output directory and newly materialized pair.

Keep the external-storage prohibition, human-only boundary, and final-confirmation command unchanged.

- [ ] **Step 6: Run the focused contract tests and verify GREEN**

Run the Step 3 command.

Expected: both tests pass.

- [ ] **Step 7: Run the Task 5 integration gate**

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

Expected: all tests pass, with only documented platform capability skips.

- [ ] **Step 8: Review and commit**

Run:

```powershell
git diff --check
git status --short
```

Verify that no `__pycache__` directory or external evidence artifact is present.

Commit:

```powershell
git add crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md `
  tools/README.md `
  tests/test_mapping_review_protocol.py
git commit -m "docs: align qualified-review seal publication"
```
