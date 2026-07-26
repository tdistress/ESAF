# PCI DSS source readiness implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record and enforce an evidenced `HOLD` on public PCI DSS v4.0.1
mapping until ESAF has authorized source bytes, a verified provision inventory,
written publication permission, and qualified independent reviewers.

**Architecture:** Add one authoritative Markdown readiness record with closed
YAML front matter, a reusable readiness schema and validator, two evidence
reviews, and focused tests. Keep readiness outside the ESAF-1600 mapping and
registry trees so a HOLD cannot appear in generated crosswalk catalogs or imply
that provisions were assessed.

**Tech Stack:** Markdown, YAML, JSON Schema Draft 2020-12, Python 3.13,
`jsonschema`, `unittest`, GitHub Actions, SHA-256, and Git.

## Global constraints

- The disposition is exactly `HOLD`; do not create a GO artifact.
- Do not accept the PCI SSC license agreement on behalf of any person or
  entity.
- Do not download or commit the access-controlled PCI DSS PDF.
- Do not reproduce PCI DSS requirement text, titles, close paraphrases, or a
  provision inventory.
- Do not create any PCI DSS entry under `crosswalks/mappings/`,
  `crosswalks/registry/`, `crosswalks/catalog.json`, or `crosswalks/CATALOG.md`.
- Treat the discovery-catalog digest as a time-stamped digest of mutable
  metadata, never as the PCI DSS v4.0.1 source digest.
- Keep the proposed first mapping direction `esaf_to_external`; exclude
  `external_to_esaf` until separately designed and approved.
- Require one blocker object per unresolved source, inventory, rights, mapper,
  or reviewer prerequisite.
- Preserve the ESAF-1600 nonclaim boundary and add PCI SSC authorization,
  endorsement, validation, and compliance claims to the prohibited set.
- Use test-driven development for validator behavior.
- Set `PYTHONDONTWRITEBYTECODE=1`; do not commit caches or downloaded source
  artifacts.
- Review the complete branch diff and rerun exact-SHA reviews after any
  candidate change.

---

### Task 1: Add the readiness record contract and fail-closed validator

**Files:**

- Create: `crosswalks/schema/readiness-record.schema.json`
- Create: `tools/crosswalks/readiness.py`
- Create: `tools/validate_crosswalk_readiness.py`
- Create: `tests/crosswalk_readiness_fixtures.py`
- Create: `tests/test_validate_crosswalk_readiness.py`

**Interfaces:**

- Produces:
  `inventory_readiness_records(root: Path) -> tuple[tuple[Path, ...], list[str]]`.
- Produces:
  `validate_readiness(root: Path = ROOT) -> list[str]`.
- Reuses:
  `tools.crosswalks.io.parse_front_matter` for UTF-8/LF and duplicate-key
  enforcement.
- CLI:
  `python tools/validate_crosswalk_readiness.py --check`, with exit `0` on
  success and `1` on content or contract errors.

- [ ] **Step 1: Add RED fixture and inventory tests**

Create a minimal temporary repository fixture containing the readiness schema,
one valid HOLD record, and empty mapping and registry directories. Add failing
tests for:

```python
def test_missing_readiness_directory_is_rejected(self) -> None: ...
def test_unexpected_readiness_entry_is_rejected(self) -> None: ...
def test_duplicate_yaml_key_is_rejected(self) -> None: ...
def test_invalid_utf8_or_crlf_is_rejected(self) -> None: ...
```

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_crosswalk_readiness -v
```

Expected: RED because the validator and schema do not exist.

- [ ] **Step 2: Add RED schema and HOLD-invariant tests**

Cover at minimum:

```python
def test_hold_requires_complete_blocker_contract(self) -> None: ...
def test_hold_rejects_available_source_without_digest(self) -> None: ...
def test_hold_rejects_source_digest_when_source_is_unavailable(self) -> None: ...
def test_hold_rejects_inventory_digest_when_inventory_is_unavailable(self) -> None: ...
def test_hold_requires_blocked_or_unreviewed_rights(self) -> None: ...
def test_hold_requires_prohibited_claims(self) -> None: ...
def test_hold_rejects_go_language(self) -> None: ...
def test_record_identity_and_version_must_agree(self) -> None: ...
def test_pci_mapping_snapshot_is_rejected_during_hold(self) -> None: ...
def test_pci_registry_record_is_rejected_during_hold(self) -> None: ...
def test_valid_hold_record_passes(self) -> None: ...
```

Expected: RED for the missing behavior.

- [ ] **Step 3: Implement the closed schema**

Use JSON Schema Draft 2020-12 with `additionalProperties: false` at every object
layer. Require:

- `schema_version`, `record_id`, `decision`, `decision_date`, and `owner`;
- source identity and public official URLs;
- discovery metadata and normative artifact states;
- provision-inventory and publication-rights states;
- proposed mapping scope and excluded direction;
- mapper and reviewer requirements;
- prohibited claims;
- blockers with stable IDs, categories, owners, evidence gaps, triggers, and
  re-entry tests; and
- change history.

Restrict decision to `GO` or `HOLD`, but implement only the fail-closed HOLD
semantic contract in this change. A future GO must not validate accidentally
without a separately implemented complete GO contract.

- [ ] **Step 4: Implement discovery and semantic validation**

Discover only direct `*.md` children of `crosswalks/readiness/`. Reject
directories, symlinks, unsupported files, empty inventory, duplicate record
IDs, parse errors, schema errors, and identity/path disagreement.

For HOLD records:

- require unavailable artifact and inventory states to carry null digest/count
  fields and explicit reasons;
- require rights to be `blocked` or `unreviewed`;
- require all blocker fields and unique blocker IDs;
- require `external_to_esaf` to be excluded in the PCI record;
- scan `crosswalks/mappings/` and `crosswalks/registry/` for a matching
  authority/publication identity and reject any PCI DSS mapping artifact; and
- reject `decision: GO`, `Disposition: GO`, or equivalent promotion language in
  the Markdown body.

Keep diagnostics repository-relative and deterministic.

- [ ] **Step 5: Make the focused tests GREEN**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_crosswalk_readiness -v
python tools/validate_crosswalk_readiness.py --check
```

Expected: tests pass; the CLI continues to fail until the authoritative record
is added in Task 2.

- [ ] **Step 6: Commit the contract**

```powershell
git add crosswalks/schema/readiness-record.schema.json `
  tools/crosswalks/readiness.py tools/validate_crosswalk_readiness.py `
  tests/crosswalk_readiness_fixtures.py `
  tests/test_validate_crosswalk_readiness.py
git commit -m "feat: validate crosswalk readiness holds"
```

---

### Task 2: Pin the public source evidence and record the HOLD

**Files:**

- Create: `crosswalks/readiness/pci-dss-v4.0.1.md`
- Create:
  `docs/superpowers/reviews/2026-07-25-pci-dss-publication-rights-review.md`
- Create:
  `docs/superpowers/reviews/2026-07-25-pci-dss-source-readiness-review.md`
- Modify: `tests/test_validate_crosswalk_readiness.py`

**Official sources:**

- `https://www.pcisecuritystandards.org/document_library/`
- `https://docs-pub.pcisecuritystandards.org/doc_library.json`
- `https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf`
- `https://blog.pcisecuritystandards.org/just-published-pci-dss-v4-0-1`
- `https://www.pcisecuritystandards.org/terms_and_conditions/`
- `https://www.pcisecuritystandards.org/about_us/policies/`
- `https://programs.pcissc.org/mla_registration.aspx`

- [ ] **Step 1: Independently retrieve and hash public discovery metadata**

Retrieve `doc_library.json` without accepting the PCI SSC document license.
Record UTC retrieval time, final URL, byte length, and lowercase SHA-256.
Extract only the selected metadata necessary to confirm:

- document reference `pci_dss`;
- version `v4.0.1`;
- `last_updated` value;
- `archived: false`;
- `protected: yes`; and
- canonical English PDF URL.

Do not commit the mutable one-megabyte catalog or any protected document.

- [ ] **Step 2: Add the publication-rights review**

Record exact official-source evidence and distinguish:

- internal study permission;
- prohibited or ungranted public distribution and derivative uses;
- the case-specific Materials License Agreement path;
- unknown version-specific terms beyond the observed access interstitial; and
- the fact that this is a conservative publication-control decision, not legal
  advice.

The review shall conclude `HOLD` for public mapping and specify the exact
permission scope needed for reconsideration.

- [ ] **Step 3: Add the authoritative readiness record**

Populate the contract with:

- current source identity and public discovery digest;
- source artifact, checksum, page count, provision count, and inventory digest
  marked unavailable;
- publication rights marked blocked;
- proposed future `esaf_to_external` scope only;
- required mapper, PCI DSS/QSA subject-matter reviewer, ESAF mapping reviewer,
  rights reviewer, and overclaiming reviewer qualifications;
- distinct blockers for source bytes, inventory, publication permission,
  mapper availability, and independent reviewers;
- accountable owner `ESAF Project Maintainer`;
- precise trigger and re-entry test for each blocker; and
- the full nonclaim boundary.

- [ ] **Step 4: Add the source-readiness review**

Document the official version/date/status evidence, public discovery digest,
protected access behavior, missing source checksum, missing provision
inventory, reviewer requirements, and mechanical decision result. State that
no substantive mapping files exist and that the generated crosswalk counts are
unchanged.

- [ ] **Step 5: Pin committed content with focused assertions**

Add tests that load the actual repository record and assert the exact decision,
version, URLs, unavailable fields, blockers, excluded direction, prohibited
claims, and linked review files.

- [ ] **Step 6: Validate and commit the evidence**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_crosswalk_readiness -v
python tools/validate_crosswalk_readiness.py --check
python tools/validate_crosswalks.py --check
git diff --check
git add crosswalks/readiness `
  docs/superpowers/reviews/2026-07-25-pci-dss-publication-rights-review.md `
  docs/superpowers/reviews/2026-07-25-pci-dss-source-readiness-review.md `
  tests/test_validate_crosswalk_readiness.py
git commit -m "docs: record PCI DSS mapping readiness hold"
```

Expected: readiness validation passes, ordinary crosswalk catalog counts remain
unchanged, and no protected source content is committed.

---

### Task 3: Publish the HOLD in project surfaces and continuous validation

**Files:**

- Modify: `crosswalks/pci-dss.md`
- Modify: `project/BACKLOG.md`
- Modify: `tools/README.md`
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tests/test_validate_crosswalk_readiness.py`

- [ ] **Step 1: Add RED presentation and workflow tests**

Require:

- `crosswalks/pci-dss.md` says `Readiness HOLD`, links the authoritative record
  and both reviews, and contains the nonclaim and reconsideration boundary;
- the active backlog no longer lists the PCI readiness workstream as
  incomplete and records issue 58 as completed through evidenced HOLD;
- the workflow path filters include readiness records, their schema, validator,
  and focused tests; and
- CI runs `python tools/validate_crosswalk_readiness.py --check`.

- [ ] **Step 2: Update repository presentation**

Replace the PCI placeholder with the exact status, blockers, owner,
reconsideration triggers, and nonclaim. Move the backlog item into a completed
workstream section without stating or implying that a PCI mapping exists.

- [ ] **Step 3: Wire continuous validation**

Document the command in `tools/README.md`. Update both pull-request and push
path filters in `catalog-validation.yml`, and add a dedicated readiness
validation step after the ordinary crosswalk check.

- [ ] **Step 4: Validate and commit presentation**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_crosswalk_readiness -v
python tools/validate_crosswalk_readiness.py --check
python tools/validate_links.py --check
git diff --check
git add crosswalks/pci-dss.md project/BACKLOG.md tools/README.md `
  .github/workflows/catalog-validation.yml `
  tests/test_validate_crosswalk_readiness.py
git commit -m "docs: publish PCI DSS readiness hold"
```

---

### Task 4: Independently review the exact candidate

**Files:**

- Create:
  `docs/superpowers/reviews/2026-07-25-pci-dss-exact-sha-source-review.md`
- Create:
  `docs/superpowers/reviews/2026-07-25-pci-dss-exact-sha-rights-overclaiming-review.md`
- Modify as findings require: files from Tasks 1–3

- [ ] **Step 1: Freeze the candidate SHA**

```powershell
git status --short
git rev-parse HEAD
git diff --check origin/main..HEAD
```

Expected: clean worktree and one 40-character candidate SHA.

- [ ] **Step 2: Dispatch independent source/inventory review**

The reviewer shall independently verify, on the exact SHA:

- current PCI DSS version and official URLs;
- discovery-catalog digest and selected facts;
- correct distinction between public metadata and protected PDF bytes;
- absent PDF checksum and absent provision inventory;
- complete blocker and re-entry contracts; and
- zero PCI mapping, registry, or generated catalog artifacts.

- [ ] **Step 3: Dispatch independent rights/overclaiming review**

The reviewer shall independently verify, on the same exact SHA:

- public terms, IPR ownership, and Materials License Agreement path;
- conservative treatment of identifiers, summaries, and derivative analysis;
- mapper/reviewer independence and authorized-access requirements;
- prohibited claims and adoption disclaimer; and
- no implied PCI SSC authorization, compliance, equivalence, coverage, or
  certification.

- [ ] **Step 4: Resolve findings test-first**

Add a focused regression test before correcting each practical Critical or
Important defect. After any change, commit it, record the new SHA, and
redispatch both exact-SHA reviews.

- [ ] **Step 5: Commit review records**

Review records shall name the exact reviewed SHA, commands/evidence, finding
counts, and disposition. Do not claim exact-SHA approval if the commit
containing review records changes substantive candidate files.

---

### Task 5: Run publication gates and publish the branch

**Files:** Whole branch.

- [ ] **Step 1: Run the focused and full validation suite**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_crosswalk_readiness -v
python -m unittest discover -s tests -v
python tools/validate_crosswalk_readiness.py --check
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref origin/main
python tools/validate_assessment.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/validate_profiles.py --check
python tools/validate_links.py --check
git diff --check origin/main..HEAD
git status --short
```

Expected: all gates pass, no cache directories or generated output are present,
and the worktree is clean.

- [ ] **Step 2: Review the complete branch diff**

```powershell
git diff --stat origin/main..HEAD
git diff origin/main..HEAD
git log --oneline origin/main..HEAD
```

Confirm that no PCI DSS source material, provision inventory, mapping snapshot,
registry record, or generated catalog change is present.

- [ ] **Step 3: Push and open a reviewable PR**

Push `agent/pci-dss-readiness`, open a ready pull request linked to issue 58,
and include:

- decision and rationale;
- exact blocker/re-entry summary;
- source and rights evidence;
- unchanged crosswalk catalog counts;
- exact reviewed head SHA;
- full validation results; and
- `Closes #58`.

- [ ] **Step 4: Verify and merge**

Require passing GitHub checks, clean merge state, and PR head equality with the
reviewed SHA before merge. Merge only when all are satisfied.

- [ ] **Step 5: Validate and clean main**

Update local `main`, rerun proportional readiness/crosswalk/link/full-suite
validation, verify a clean worktree, and remove the temporary branch and
worktree. Do not disturb unrelated historical worktree metadata.
