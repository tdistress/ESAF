# UK Mapping Qualified-Review Preparation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build reproducible, exact-commit review packages and durable human-review guidance for the three Draft UK Cyber Essentials mapping snapshots without changing their lifecycle state.

**Architecture:** A single standard-library Python tool reads tracked bytes from an allowlisted Git commit, verifies one mapping snapshot and its pinned dependencies, and writes a deterministic directory with a canonical SHA-256 manifest. Repository protocol and worksheet templates define the human review boundary; focused `unittest` modules enforce both documentation and generator invariants.

**Tech Stack:** Python 3 standard library, existing PyYAML/front-matter helpers in `tools.crosswalks.io`, Git CLI, Markdown, JSON, `unittest`.

## Global Constraints

- The only accepted mapping-set identifiers are the three exact identifiers in the approved design.
- Expected provision populations are Core `116`, Plus forward `144`, and Plus reverse `144`.
- All mapping sets and mapping records shall remain `draft`; this work shall add no `reviewer` metadata.
- Generated packages shall be written outside every Git worktree and shall not be committed.
- Package content shall come from a full 40-character commit SHA, never from working-tree bytes.
- External source documents shall not be downloaded, embedded, copied, or redistributed.
- Core, Plus forward, and Plus reverse shall have separate packages and conclusions.
- Two separately recorded review disciplines are required: specification/inventory and security/overclaiming.
- Critical and Important findings shall be resolved before a later `reviewed` transition.
- Use `PYTHONDONTWRITEBYTECODE=1` for every Python test and validation command.

## File structure

- `crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md`: durable reviewer eligibility, workflow, findings, lifecycle, and stop rules.
- `crosswalks/reviews/templates/REVIEWER_ATTESTATION.md`: per-person, per-role, per-mapping-set attestation.
- `crosswalks/reviews/templates/SPECIFICATION_INVENTORY_REVIEW.md`: structured source, rights, population, and catalog review worksheet.
- `crosswalks/reviews/templates/SECURITY_OVERCLAIMING_REVIEW.md`: structured relationship and negative-disposition review worksheet.
- `tools/build_mapping_review_bundle.py`: profiles, exact Git-object reads, population validation, package rendering, manifesting, and CLI.
- `tests/test_mapping_review_protocol.py`: documentation contracts and preparation-phase Draft invariants.
- `tests/test_build_mapping_review_bundle.py`: unit and end-to-end generator tests.
- `tools/README.md`: operator commands and package-integrity explanation.

---

### Task 1: Human-review protocol and templates

**Files:**
- Create: `crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md`
- Create: `crosswalks/reviews/templates/REVIEWER_ATTESTATION.md`
- Create: `crosswalks/reviews/templates/SPECIFICATION_INVENTORY_REVIEW.md`
- Create: `crosswalks/reviews/templates/SECURITY_OVERCLAIMING_REVIEW.md`
- Create: `tests/test_mapping_review_protocol.py`

**Interfaces:**
- Consumes: ESAF-1600, `crosswalks/schema/mapping-set.schema.json`, and `crosswalks/schema/mapping-record.schema.json`.
- Produces: four UTF-8/LF Markdown inputs copied verbatim into every generated package.

- [ ] **Step 1: Write failing protocol-contract tests**

Create `tests/test_mapping_review_protocol.py`:

```python
from __future__ import annotations

import unittest
from pathlib import Path

from tools.crosswalks.io import parse_front_matter


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md"
TEMPLATES = ROOT / "crosswalks/reviews/templates"
SET_IDS = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
)
SNAPSHOTS = (
    ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0",
    ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0",
    ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0",
)


class MappingReviewProtocolTests(unittest.TestCase):
    def test_protocol_defines_roles_exact_sha_and_stop_boundary(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        for phrase in (
            "Specification and inventory review",
            "Security and overclaiming review",
            "full 40-character Git commit SHA",
            "authorized source access",
            "different from the mapper",
            "Critical",
            "Important",
            "remains `draft`",
            "AI-produced review",
        ):
            self.assertIn(phrase, text)
        for mapping_set_id in SET_IDS:
            self.assertIn(mapping_set_id, text)

    def test_attestation_requires_identity_eligibility_and_nonclaims(self) -> None:
        text = (TEMPLATES / "REVIEWER_ATTESTATION.md").read_text(encoding="utf-8")
        for field in (
            "Reviewer identity",
            "Organization",
            "Verification locator",
            "Mapping-set identifier",
            "Candidate commit SHA",
            "Review role",
            "Scheme qualification",
            "ESAF or mapping qualification",
            "Authorized source access",
            "Independence from mapper",
            "Conflicts of interest",
            "certification",
            "equivalence",
            "Signature",
            "Date",
        ):
            self.assertIn(field, text)

    def test_review_worksheets_have_separate_scopes_and_findings(self) -> None:
        specification = (
            TEMPLATES / "SPECIFICATION_INVENTORY_REVIEW.md"
        ).read_text(encoding="utf-8")
        security = (
            TEMPLATES / "SECURITY_OVERCLAIMING_REVIEW.md"
        ).read_text(encoding="utf-8")
        for text in (specification, security):
            for field in (
                "Mapping-set identifier",
                "Candidate commit SHA",
                "Attestation locator",
                "Coverage",
                "Finding ID",
                "Affected record IDs",
                "Severity",
                "Evidence",
                "Required action",
                "Disposition",
                "Overall conclusion",
                "`pass`",
                "`pass_after_correction`",
                "`stop`",
            ):
                self.assertIn(field, text)
        self.assertIn("Provision population", specification)
        self.assertIn("Publication rights", specification)
        self.assertIn("no_direct_mapping", security)
        self.assertIn("prerequisite", security)
        self.assertIn("partially_supports", security)

    def test_preparation_does_not_transition_snapshots(self) -> None:
        for snapshot in SNAPSHOTS:
            set_metadata, _ = parse_front_matter(snapshot / "README.md")
            self.assertEqual(set_metadata["status"], "draft")
            self.assertNotIn("reviewer", set_metadata)
            records = [
                path for path in snapshot.glob("*.md")
                if path.name not in {"README.md", "PROVISION_INVENTORY.md"}
            ]
            for record in records:
                metadata, _ = parse_front_matter(record)
                self.assertEqual(metadata["status"], "draft")
                self.assertNotIn("reviewer", metadata)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and confirm the missing-artifact failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_mapping_review_protocol -v
```

Expected: errors naming the four missing files under `crosswalks/reviews/`.

- [ ] **Step 3: Write the protocol**

Create `crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md` with these exact
sections and rules:

```markdown
# Qualified Review Protocol for UK Mapping Snapshots

## Status and boundary

This protocol prepares Draft mappings for qualified independent human review
under ESAF-1600. Preparation, automation, mapper self-review, and AI-produced
review are not qualified review. Until every applicable condition is met, the
affected mapping set remains `draft`.

## In-scope snapshots

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
  — Core, 116 provisions.
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
  — Plus forward, 144 provisions.
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`
  — Plus reverse, 144 provisions.

Core, Plus forward, and Plus reverse require separate packages, findings, and
conclusions.

## Candidate integrity

Every review names one full 40-character Git commit SHA and one package
manifest digest. A changed candidate invalidates final review evidence.

## Reviewer eligibility

A named human records scheme qualification, ESAF or mapping qualification,
authorized source access, organization, verification locator, independence
from the mapper, and conflicts of interest. The project owner accepts or
rejects eligibility per mapping set and review role.

## Specification and inventory review

Verify official source identity/version/checksum/locators, publication rights,
provision population and hierarchy, record coverage, registry/catalog
consistency, and predecessor/change-history integrity.

## Security and overclaiming review

Verify each relationship and `no_direct_mapping` rationale against exact
normative source and ESAF text. Check direction, coverage, confidence,
conditions, evidence, gaps, `prerequisite` versus `partially_supports`, and
all certification, compliance, equivalence, endorsement, and assurance
nonclaims.

## Findings

Use Critical, Important, and Minor. Resolve Critical and Important findings
before `reviewed`. Only Minor may be accepted, with named acceptor, rationale,
and date. Record separate worksheets for both review disciplines.

## Lifecycle transition

This preparation does not add reviewer metadata or change lifecycle state.
A later transition updates every mapping record, mapping-set metadata,
registry state, catalogs, and digests together on an exact human-reviewed
head. `reviewed` is not `approved`.

## Stop conditions

Stop for missing eligibility, independence, source access, source/version or
digest mismatch, changed SHA, combined Core/Plus conclusions, external-source
redistribution, open Critical or Important findings, unresolved template
markers, or an AI-produced review. The affected mapping remains `draft`.
```

- [ ] **Step 4: Write the three templates**

Create `REVIEWER_ATTESTATION.md` with a warning that an unsigned blank form is
not review evidence and a two-column table containing every field asserted by
the test. Include explicit yes/no attestations for authorized source access,
independence, and conflicts; add this exact nonclaim:

```markdown
I understand that this review does not establish certification, compliance,
equivalence, endorsement, or assurance beyond the relationships expressly
recorded in the mapping snapshot.
```

Create both review worksheets with:

```markdown
## Review identification

| Field | Value |
|---|---|
| Mapping-set identifier | `[REQUIRED]` |
| Candidate commit SHA | `[REQUIRED: 40 lowercase hexadecimal characters]` |
| Package-manifest SHA-256 | `[REQUIRED]` |
| Reviewer identity | `[REQUIRED]` |
| Attestation locator | `[REQUIRED]` |
| Review date | `[REQUIRED: YYYY-MM-DD]` |
| Coverage | `[REQUIRED]` |

## Findings

| Finding ID | Affected record IDs | Severity | Description | Evidence | Required action | Status | Disposition |
|---|---|---|---|---|---|---|---|
| `[REQUIRED OR NONE]` |  | Critical / Important / Minor |  |  |  | open / resolved / accepted |  |

## Overall conclusion

Select exactly one: `pass`, `pass_after_correction`, or `stop`.
```

The specification worksheet shall additionally enumerate source identity,
version, checksum, official locator, publication rights, Provision population,
inventory order/hierarchy, record/catalog/registry agreement, and change
history. The security worksheet shall enumerate relationship direction/type,
coverage/confidence, conditions, expected evidence, known gaps,
`no_direct_mapping`, `prerequisite`, `partially_supports`, normative-text
basis, and nonclaims.

- [ ] **Step 5: Run the focused tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_mapping_review_protocol -v
```

Expected: `Ran 4 tests` and `OK`.

- [ ] **Step 6: Commit the protocol slice**

```powershell
git add -- crosswalks/reviews tests/test_mapping_review_protocol.py
git commit -m "docs: add qualified mapping review protocol"
```

Expected: one commit containing only the protocol, templates, and focused
contract test.

---

### Task 2: Exact-commit reader and allowlisted mapping profiles

**Files:**
- Create: `tools/build_mapping_review_bundle.py`
- Create: `tests/test_build_mapping_review_bundle.py`

**Interfaces:**
- Produces:
  - `MappingProfile(mapping_set_id: str, snapshot_path: str, label: str, direction: str, expected_count: int)`.
  - `GitReader.resolve_commit(revision: str) -> str`.
  - `GitReader.read_bytes(commit: str, path: str) -> bytes`.
  - `GitReader.list_files(commit: str, path: str) -> tuple[str, ...]`.
  - `GitReader.worktree_roots() -> tuple[Path, ...]`.
- Consumes: only Git CLI output and repository-relative POSIX paths.

- [ ] **Step 1: Write failing reader/profile tests**

Start `tests/test_build_mapping_review_bundle.py` with:

```python
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.build_mapping_review_bundle import (
    PROFILES,
    GitReader,
    MappingProfile,
)


ROOT = Path(__file__).resolve().parents[1]


class GitReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = GitReader(ROOT)
        self.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()

    def test_profiles_are_exact_and_separate(self) -> None:
        self.assertEqual(
            {profile.expected_count for profile in PROFILES.values()},
            {116, 144},
        )
        self.assertEqual(len(PROFILES), 3)
        self.assertEqual(
            {profile.direction for profile in PROFILES.values()},
            {"external_to_esaf", "esaf_to_external"},
        )
        self.assertEqual(
            {profile.label for profile in PROFILES.values()},
            {"Core", "Plus forward", "Plus reverse"},
        )

    def test_resolve_commit_requires_full_exact_sha(self) -> None:
        self.assertEqual(self.reader.resolve_commit(self.head), self.head)
        for invalid in ("HEAD", self.head[:12], "g" * 40, "0" * 40):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    self.reader.resolve_commit(invalid)

    def test_reads_blob_and_lists_tree_from_commit(self) -> None:
        data = self.reader.read_bytes(self.head, "crosswalks/ESAF-1600.md")
        self.assertTrue(data.startswith(b"---\n"))
        paths = self.reader.list_files(self.head, "crosswalks/schema")
        self.assertIn("crosswalks/schema/mapping-set.schema.json", paths)
        self.assertEqual(paths, tuple(sorted(paths)))

    def test_reports_all_worktree_roots_as_resolved_paths(self) -> None:
        roots = self.reader.worktree_roots()
        self.assertIn(ROOT.resolve(), roots)
        self.assertTrue(all(path.is_absolute() for path in roots))
```

- [ ] **Step 2: Run the tests and confirm import failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle.GitReaderTests -v
```

Expected: import error because `tools/build_mapping_review_bundle.py` does not
exist.

- [ ] **Step 3: Implement profiles and exact Git reads**

Create `tools/build_mapping_review_bundle.py` with these definitions:

```python
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
GENERATOR_VERSION = "1.0.0"


@dataclass(frozen=True)
class MappingProfile:
    mapping_set_id: str
    snapshot_path: str
    label: str
    direction: str
    expected_count: int


_PROFILE_ROWS = (
    (
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0",
        "Core", "external_to_esaf", 116,
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0",
        "Plus forward", "esaf_to_external", 144,
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0",
        "Plus reverse", "external_to_esaf", 144,
    ),
)
PROFILES = {
    row[0]: MappingProfile(*row)
    for row in _PROFILE_ROWS
}


class GitReader:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def _run(self, *arguments: str, text: bool = False) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True, capture_output=True, text=text,
        )

    def resolve_commit(self, revision: str) -> str:
        if not FULL_SHA.fullmatch(revision):
            raise ValueError("candidate must be a full lowercase 40-character Git SHA")
        try:
            resolved = self._run("rev-parse", "--verify", f"{revision}^{{commit}}", text=True).stdout.strip()
        except subprocess.CalledProcessError as error:
            raise ValueError("candidate is not an available commit") from error
        if resolved != revision:
            raise ValueError("candidate does not resolve to the exact commit")
        return resolved

    def read_bytes(self, commit: str, path: str) -> bytes:
        if path.startswith("/") or ".." in Path(path).parts or "\\" in path:
            raise ValueError(f"unsafe repository path: {path}")
        try:
            return self._run("show", f"{commit}:{path}").stdout
        except subprocess.CalledProcessError as error:
            raise ValueError(f"missing tracked file at candidate: {path}") from error

    def list_files(self, commit: str, path: str) -> tuple[str, ...]:
        result = self._run(
            "ls-tree", "-r", "--name-only", "-z", commit, "--", path
        ).stdout
        names = tuple(
            item.decode("utf-8")
            for item in result.split(b"\0")
            if item
        )
        return tuple(sorted(names))

    def worktree_roots(self) -> tuple[Path, ...]:
        output = self._run("worktree", "list", "--porcelain", "-z").stdout
        roots = []
        for field in output.split(b"\0"):
            if field.startswith(b"worktree "):
                roots.append(Path(field[9:].decode("utf-8")).resolve())
        return tuple(roots)
```

Keep lines within the repository's normal readable width when implementing;
the snippets show exact behavior, not a license to collapse production code.

- [ ] **Step 4: Run the focused reader tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle.GitReaderTests -v
```

Expected: `Ran 4 tests` and `OK`.

- [ ] **Step 5: Commit the exact-reader slice**

```powershell
git add -- tools/build_mapping_review_bundle.py tests/test_build_mapping_review_bundle.py
git commit -m "feat: add exact-commit mapping review reader"
```

---

### Task 3: Snapshot population and dependency validation

**Files:**
- Modify: `tools/build_mapping_review_bundle.py`
- Modify: `tests/test_build_mapping_review_bundle.py`

**Interfaces:**
- Produces:
  - `PackageFile(path: str, content: bytes, purpose: str)`.
  - `parse_front_matter_bytes(content: bytes) -> tuple[dict[str, object], str]`.
  - `collect_package_files(reader: GitReader, commit: str, profile: MappingProfile) -> tuple[PackageFile, ...]`.
- Consumes: `GitReader`, `MappingProfile`, the snapshot manifest, registry, catalog, ESAF-1600, schemas, protocol, and templates.

- [ ] **Step 1: Add failing population tests**

Append a `PackagePopulationTests` class:

```python
class PackagePopulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reader = GitReader(ROOT)
        cls.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()

    def test_every_profile_collects_exact_population_and_dependencies(self) -> None:
        for profile in PROFILES.values():
            with self.subTest(profile=profile.label):
                files = collect_package_files(self.reader, self.head, profile)
                paths = {item.path for item in files}
                record_prefix = f"{profile.snapshot_path}/"
                record_paths = {
                    path for path in paths
                    if path.startswith(record_prefix)
                    and path.endswith(".md")
                    and not path.endswith("/README.md")
                    and not path.endswith("/PROVISION_INVENTORY.md")
                }
                self.assertEqual(len(record_paths), profile.expected_count)
                for required in (
                    f"{profile.snapshot_path}/README.md",
                    f"{profile.snapshot_path}/PROVISION_INVENTORY.md",
                    f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json",
                    f"crosswalks/registry/{profile.mapping_set_id}.md",
                    "crosswalks/ESAF-1600.md",
                    "crosswalks/schema/mapping-set.schema.json",
                    "crosswalks/schema/mapping-record.schema.json",
                    "crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md",
                    "crosswalks/reviews/templates/REVIEWER_ATTESTATION.md",
                    "review-metadata/catalog-entry.json",
                ):
                    self.assertIn(required, paths)

    def test_collected_controls_match_manifest_paths_and_digests(self) -> None:
        for profile in PROFILES.values():
            files = collect_package_files(self.reader, self.head, profile)
            by_path = {item.path: item.content for item in files}
            manifest = json.loads(
                by_path[f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"]
            )
            for control in manifest["controls"]:
                packaged_path = f"controls/{control['path']}"
                self.assertEqual(
                    hashlib.sha256(by_path[packaged_path]).hexdigest(),
                    control["record_sha256"],
                )

    def test_collector_rejects_population_or_status_drift(self) -> None:
        profile = next(iter(PROFILES.values()))
        base = self.reader

        class MutatingReader:
            def read_bytes(self, commit: str, path: str) -> bytes:
                content = base.read_bytes(commit, path)
                if path.endswith("/README.md"):
                    return content.replace(b"status: draft", b"status: reviewed", 1)
                return content

            def list_files(self, commit: str, path: str) -> tuple[str, ...]:
                return base.list_files(commit, path)

        with self.assertRaisesRegex(ValueError, "must remain draft"):
            collect_package_files(MutatingReader(), self.head, profile)
```

Add imports for `hashlib`, `json`, and `collect_package_files`.

- [ ] **Step 2: Run the population tests and confirm missing-symbol failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle.PackagePopulationTests -v
```

Expected: import failure for `collect_package_files`.

- [ ] **Step 3: Implement strict front-matter parsing and package-file types**

Add:

```python
from tools.crosswalks.io import load_yaml_mapping


@dataclass(frozen=True)
class PackageFile:
    path: str
    content: bytes
    purpose: str


def parse_front_matter_bytes(content: bytes) -> tuple[dict[str, object], str]:
    if content.startswith(b"\xef\xbb\xbf") or b"\r" in content:
        raise ValueError("package Markdown must be canonical UTF-8/LF")
    text = content.decode("utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("malformed YAML front matter")
    return load_yaml_mapping(parts[1]), parts[2]
```

- [ ] **Step 4: Implement collection and validation**

Implement these helpers and `collect_package_files`:

```python
def _package_file(
    reader: GitReader,
    commit: str,
    path: str,
    purpose: str,
) -> PackageFile:
    return PackageFile(path, reader.read_bytes(commit, path), purpose)


def _require_draft(
    metadata: dict[str, object],
    mapping_set_id: str,
    subject: str,
) -> None:
    if metadata.get("mapping_set_id") != mapping_set_id:
        raise ValueError(f"{subject} mapping-set identifier mismatch")
    if metadata.get("status") != "draft" or "reviewer" in metadata:
        raise ValueError(f"{subject} must remain draft without reviewer metadata")


def collect_package_files(
    reader: GitReader,
    commit: str,
    profile: MappingProfile,
) -> tuple[PackageFile, ...]:
    snapshot_paths = reader.list_files(commit, profile.snapshot_path)
    required = {
        f"{profile.snapshot_path}/README.md",
        f"{profile.snapshot_path}/PROVISION_INVENTORY.md",
        f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json",
    }
    if not required.issubset(snapshot_paths):
        raise ValueError("snapshot is missing required artifacts")
    record_paths = tuple(
        path for path in snapshot_paths
        if path.endswith(".md") and path not in required
    )
    if len(record_paths) != profile.expected_count:
        raise ValueError("mapping-record population mismatch")

    files: list[PackageFile] = []
    readme_path = f"{profile.snapshot_path}/README.md"
    readme = _package_file(reader, commit, readme_path, "mapping set")
    set_metadata, _ = parse_front_matter_bytes(readme.content)
    _require_draft(set_metadata, profile.mapping_set_id, "mapping set")
    scope = set_metadata.get("scope")
    if not isinstance(scope, dict) or scope.get("inventory_count") != profile.expected_count:
        raise ValueError("mapping-set inventory count mismatch")
    files.append(readme)

    inventory_path = f"{profile.snapshot_path}/PROVISION_INVENTORY.md"
    inventory = _package_file(
        reader, commit, inventory_path, "provision inventory"
    )
    inventory_metadata, _ = parse_front_matter_bytes(inventory.content)
    if inventory_metadata.get("mapping_set_id") != profile.mapping_set_id:
        raise ValueError("inventory mapping-set identifier mismatch")
    provision_ids = inventory_metadata.get("provision_ids")
    if (
        inventory_metadata.get("expected_count") != profile.expected_count
        or not isinstance(provision_ids, list)
        or len(provision_ids) != profile.expected_count
        or len(set(provision_ids)) != profile.expected_count
    ):
        raise ValueError("provision inventory population mismatch")
    files.append(inventory)

    record_ids: set[str] = set()
    record_provisions: set[str] = set()
    for path in record_paths:
        record = _package_file(reader, commit, path, "mapping record")
        metadata, _ = parse_front_matter_bytes(record.content)
        _require_draft(metadata, profile.mapping_set_id, f"record {path}")
        record_id = metadata.get("record_id")
        provision_id = metadata.get("external_provision_id")
        if not isinstance(record_id, str) or record_id in record_ids:
            raise ValueError("duplicate or invalid mapping-record identifier")
        if not isinstance(provision_id, str) or provision_id in record_provisions:
            raise ValueError("duplicate or invalid external provision identifier")
        record_ids.add(record_id)
        record_provisions.add(provision_id)
        files.append(record)
    if record_provisions != set(provision_ids):
        raise ValueError("mapping records do not match provision inventory")

    manifest_path = f"{profile.snapshot_path}/ESAF_CONTROL_MANIFEST.json"
    manifest_file = _package_file(
        reader, commit, manifest_path, "control manifest"
    )
    manifest = json.loads(manifest_file.content)
    if manifest.get("esaf_release") != set_metadata["esaf_release"]["id"]:
        raise ValueError("control manifest ESAF release mismatch")
    controls = manifest.get("controls")
    if not isinstance(controls, list) or not controls:
        raise ValueError("control manifest has no controls")
    files.append(manifest_file)
    seen_controls: set[str] = set()
    for control in controls:
        control_path = f"controls/{control['path']}"
        if control_path in seen_controls:
            raise ValueError("duplicate control manifest path")
        seen_controls.add(control_path)
        control_file = _package_file(
            reader, commit, control_path, "referenced ESAF control"
        )
        if hashlib.sha256(control_file.content).hexdigest() != control["record_sha256"]:
            raise ValueError(f"control digest mismatch: {control_path}")
        files.append(control_file)

    registry_path = f"crosswalks/registry/{profile.mapping_set_id}.md"
    registry = _package_file(
        reader, commit, registry_path, "lifecycle registry"
    )
    registry_metadata, registry_body = parse_front_matter_bytes(registry.content)
    if (
        registry_metadata.get("mapping_set_id") != profile.mapping_set_id
        or registry_metadata.get("events") != []
        or "state: draft" not in registry_body
    ):
        raise ValueError("registry must remain Draft with no lifecycle events")
    files.append(registry)

    catalog = json.loads(reader.read_bytes(commit, "crosswalks/catalog.json"))
    matches = [
        item for item in catalog["mapping_sets"]
        if item["metadata"]["mapping_set_id"] == profile.mapping_set_id
    ]
    if len(matches) != 1 or len(matches[0]["provisions"]) != profile.expected_count:
        raise ValueError("catalog entry population mismatch")
    catalog_bytes = (
        json.dumps(
            {
                "schema_version": catalog["schema_version"],
                "generated_from": catalog["generated_from"],
                "mapping_set": matches[0],
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    files.append(
        PackageFile(
            "review-metadata/catalog-entry.json",
            catalog_bytes,
            "catalog entry",
        )
    )

    fixed_paths = {
        "crosswalks/ESAF-1600.md": "ESAF-1600 method",
        "crosswalks/schema/esaf-control-manifest.schema.json": "crosswalk schema",
        "crosswalks/schema/lifecycle-record.schema.json": "crosswalk schema",
        "crosswalks/schema/mapping-record.schema.json": "crosswalk schema",
        "crosswalks/schema/mapping-set.schema.json": "crosswalk schema",
        "crosswalks/schema/provision-inventory.schema.json": "crosswalk schema",
        "crosswalks/reviews/QUALIFIED_REVIEW_PROTOCOL.md": "review protocol",
        "crosswalks/reviews/templates/REVIEWER_ATTESTATION.md": "blank review template",
        "crosswalks/reviews/templates/SPECIFICATION_INVENTORY_REVIEW.md": "blank review template",
        "crosswalks/reviews/templates/SECURITY_OVERCLAIMING_REVIEW.md": "blank review template",
    }
    files.extend(
        _package_file(reader, commit, path, purpose)
        for path, purpose in fixed_paths.items()
    )
    paths = [item.path for item in files]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate package path")
    return tuple(sorted(files, key=lambda item: item.path))
```

Use these purposes: `mapping set`, `provision inventory`, `mapping record`,
`control manifest`, `referenced ESAF control`, `lifecycle registry`,
`catalog entry`, `ESAF-1600 method`, `crosswalk schema`, `review protocol`,
and `blank review template`.

- [ ] **Step 5: Run all generator tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle -v
```

Expected: `Ran 7 tests` and `OK`.

- [ ] **Step 6: Commit the verified-population slice**

```powershell
git add -- tools/build_mapping_review_bundle.py tests/test_build_mapping_review_bundle.py
git commit -m "feat: verify mapping review package population"
```

---

### Task 4: Deterministic package output and safe CLI

**Files:**
- Modify: `tools/build_mapping_review_bundle.py`
- Modify: `tests/test_build_mapping_review_bundle.py`

**Interfaces:**
- Produces:
  - `canonical_json_bytes(value: object) -> bytes`.
  - `validate_output_directory(output: Path, worktrees: tuple[Path, ...]) -> Path`.
  - `write_package(reader: GitReader, commit: str, profile: MappingProfile, output: Path) -> dict[str, object]`.
  - CLI: `python tools/build_mapping_review_bundle.py --commit <sha> --mapping-set-id <id> --output <outside-path>`.
- Consumes: the sorted `PackageFile` tuple from Task 3.

- [ ] **Step 1: Add failing deterministic-output and safety tests**

Append:

```python
class PackageWriterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reader = GitReader(ROOT)
        cls.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
        cls.profile = PROFILES[
            "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0"
        ]

    def test_two_runs_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            first_manifest = write_package(
                self.reader, self.head, self.profile, first
            )
            second_manifest = write_package(
                self.reader, self.head, self.profile, second
            )
            self.assertEqual(first_manifest, second_manifest)
            first_files = {
                path.relative_to(first).as_posix(): path.read_bytes()
                for path in first.rglob("*") if path.is_file()
            }
            second_files = {
                path.relative_to(second).as_posix(): path.read_bytes()
                for path in second.rglob("*") if path.is_file()
            }
            self.assertEqual(first_files, second_files)
            self.assertIn("PACKAGE_INDEX.md", first_files)
            self.assertIn("PACKAGE_MANIFEST.json", first_files)

    def test_manifest_covers_every_payload_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            manifest = write_package(
                self.reader, self.head, self.profile, output
            )
            listed = {item["path"] for item in manifest["files"]}
            actual_payload = {
                path.relative_to(output).as_posix()
                for path in output.rglob("*")
                if path.is_file() and path.name != "PACKAGE_MANIFEST.json"
            }
            self.assertEqual(listed, actual_payload)
            for item in manifest["files"]:
                content = (output / item["path"]).read_bytes()
                self.assertEqual(item["bytes"], len(content))
                self.assertEqual(
                    item["sha256"], hashlib.sha256(content).hexdigest()
                )

    def test_rejects_worktree_and_nonempty_output(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside every Git worktree"):
            validate_output_directory(
                ROOT / "review-output",
                self.reader.worktree_roots(),
            )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "existing"
            output.mkdir()
            (output / "keep.txt").write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty"):
                validate_output_directory(output, ())

    def test_cli_writes_one_allowlisted_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package"
            result = subprocess.run(
                [
                    "python", str(ROOT / "tools/build_mapping_review_bundle.py"),
                    "--commit", self.head,
                    "--mapping-set-id", self.profile.mapping_set_id,
                    "--output", str(output),
                ],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["candidate_commit"], self.head)
            self.assertEqual(report["mapping_set_id"], self.profile.mapping_set_id)
            self.assertEqual(len(report["manifest_sha256"]), 64)

    def test_cli_rejects_unknown_mapping_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    "python", str(ROOT / "tools/build_mapping_review_bundle.py"),
                    "--commit", self.head,
                    "--mapping-set-id", "unknown",
                    "--output", str(Path(directory) / "package"),
                ],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsupported mapping-set identifier", result.stderr)
```

Import `validate_output_directory` and `write_package`.

- [ ] **Step 2: Run writer tests and confirm missing-symbol failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle.PackageWriterTests -v
```

Expected: import failure for the writer symbols.

- [ ] **Step 3: Implement output validation and canonical serialization**

Add:

```python
def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_output_directory(
    output: Path, worktrees: tuple[Path, ...]
) -> Path:
    resolved = output.resolve()
    if any(_is_within(resolved, root) for root in worktrees):
        raise ValueError("output must be outside every Git worktree")
    if resolved.exists() and any(resolved.iterdir()):
        raise ValueError("existing output directory must be empty")
    return resolved
```

- [ ] **Step 4: Implement index, manifest, and writer**

Add this index renderer:

```python
def render_package_index(
    profile: MappingProfile,
    commit: str,
    mapping_set_content: bytes,
) -> bytes:
    metadata, _ = parse_front_matter_bytes(mapping_set_content)
    source = metadata["source"]
    rights = metadata["publication_rights"]
    source_version = metadata["source_version"]
    text = f"""# {profile.label} Qualified-Review Package

| Field | Value |
|---|---|
| Mapping-set identifier | `{profile.mapping_set_id}` |
| Direction | `{profile.direction}` |
| Candidate commit | `{commit}` |
| Expected provisions | {profile.expected_count} |
| Source version | `{source_version["id"]}` ({source_version["label"]}) |
| Official URL | {source["official_url"]} |
| Access class | `{source["access_class"]}` |

## Publication-rights boundary

**Basis:** {rights["basis"]}

**Restrictions:** {rights["restrictions"]}

External source documents are not included. The reviewer must independently
obtain authorized access to the exact source and attest to that access.

## Lifecycle and assurance boundary

This package does not establish qualified review, certification, compliance,
equivalence, endorsement, approval, or assurance. The mapping remains Draft.
"""
    return text.encode("utf-8")
```

This names the label, direction, mapping-set ID, exact commit, provision
count, official URL, source version, access class, publication-rights basis,
restrictions, and required boundaries:

```markdown
External source documents are not included. The reviewer must independently
obtain authorized access to the exact source and attest to that access.

This package does not establish qualified review, certification, compliance,
equivalence, endorsement, approval, or assurance. The mapping remains Draft.
```

Implement the writer:

```python
def write_package(
    reader: GitReader,
    commit: str,
    profile: MappingProfile,
    output: Path,
) -> dict[str, object]:
    destination = validate_output_directory(output, reader.worktree_roots())
    collected = list(collect_package_files(reader, commit, profile))
    mapping_set_path = f"{profile.snapshot_path}/README.md"
    mapping_set_content = next(
        item.content for item in collected
        if item.path == mapping_set_path
    )
    collected.append(
        PackageFile(
            "PACKAGE_INDEX.md",
            render_package_index(profile, commit, mapping_set_content),
            "package index",
        )
    )
    collected.sort(key=lambda item: item.path)
    destination.mkdir(parents=True, exist_ok=True)
    manifest_files: list[dict[str, object]] = []
    for item in collected:
        relative = Path(item.path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"unsafe package path: {item.path}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(item.content)
        manifest_files.append(
            {
                "path": item.path,
                "purpose": item.purpose,
                "bytes": len(item.content),
                "sha256": hashlib.sha256(item.content).hexdigest(),
            }
        )
    manifest: dict[str, object] = {
        "schema_version": "1.0.0",
        "generator_version": GENERATOR_VERSION,
        "mapping_set_id": profile.mapping_set_id,
        "package_label": profile.label,
        "direction": profile.direction,
        "expected_provision_count": profile.expected_count,
        "candidate_commit": commit,
        "files": manifest_files,
    }
    (destination / "PACKAGE_MANIFEST.json").write_bytes(
        canonical_json_bytes(manifest)
    )
    return manifest
```

The manifest digest printed by the CLI is:

```python
manifest_sha256 = hashlib.sha256(
    (output / "PACKAGE_MANIFEST.json").read_bytes()
).hexdigest()
```

- [ ] **Step 5: Implement the CLI**

Add:

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True)
    parser.add_argument("--mapping-set-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        root = Path(
            subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                check=True, capture_output=True, text=True,
            ).stdout.strip()
        )
        reader = GitReader(root)
        commit = reader.resolve_commit(args.commit)
        try:
            profile = PROFILES[args.mapping_set_id]
        except KeyError as error:
            raise ValueError("unsupported mapping-set identifier") from error
        output = validate_output_directory(
            args.output, reader.worktree_roots()
        )
        write_package(reader, commit, profile, output)
        report = {
            "candidate_commit": commit,
            "mapping_set_id": profile.mapping_set_id,
            "output": str(output),
            "manifest_sha256": hashlib.sha256(
                (output / "PACKAGE_MANIFEST.json").read_bytes()
            ).hexdigest(),
        }
        print(json.dumps(report, sort_keys=True))
        return 0
    except Exception as error:
        print(error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Run all focused tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle -v
python -m unittest tests.test_mapping_review_protocol -v
```

Expected: `Ran 12 tests` for the generator, `Ran 4 tests` for the protocol,
and both commands end in `OK`.

- [ ] **Step 7: Commit the deterministic-writer slice**

```powershell
git add -- tools/build_mapping_review_bundle.py tests/test_build_mapping_review_bundle.py
git commit -m "feat: build deterministic mapping review packages"
```

---

### Task 5: Operator documentation and three-package integration proof

**Files:**
- Modify: `tools/README.md`
- Modify: `tests/test_build_mapping_review_bundle.py`

**Interfaces:**
- Consumes: the completed CLI.
- Produces: documented commands and an end-to-end test proving all three
  packages stay separate and exclude external binary source files.

- [ ] **Step 1: Add failing integration/documentation tests**

Append:

```python
class PackageIntegrationTests(unittest.TestCase):
    def test_all_packages_are_separate_complete_and_source_safe(self) -> None:
        reader = GitReader(ROOT)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
        with tempfile.TemporaryDirectory() as directory:
            manifests = {}
            for profile in PROFILES.values():
                output = Path(directory) / profile.label.replace(" ", "-").lower()
                manifests[profile.label] = write_package(
                    reader, head, profile, output
                )
                names = {
                    path.relative_to(output).as_posix()
                    for path in output.rglob("*") if path.is_file()
                }
                self.assertFalse(
                    any(name.lower().endswith((".pdf", ".doc", ".docx")) for name in names)
                )
                index = (output / "PACKAGE_INDEX.md").read_text(encoding="utf-8")
                self.assertIn(profile.label, index)
                self.assertIn(profile.direction, index)
                self.assertIn("remains Draft", index)
            self.assertEqual(set(manifests), {"Core", "Plus forward", "Plus reverse"})
            self.assertEqual(
                {item["mapping_set_id"] for item in manifests.values()},
                set(PROFILES),
            )

    def test_tools_readme_documents_exact_safe_command(self) -> None:
        text = (ROOT / "tools/README.md").read_text(encoding="utf-8")
        self.assertIn("## Qualified mapping review packages", text)
        self.assertIn("build_mapping_review_bundle.py", text)
        self.assertIn("--commit", text)
        self.assertIn("--mapping-set-id", text)
        self.assertIn("--output", text)
        self.assertIn("outside every Git worktree", text)
        self.assertIn("does not include the external source document", text)
```

- [ ] **Step 2: Run the integration tests and confirm documentation failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle.PackageIntegrationTests -v
```

Expected: the package test passes and the README test fails because the new
section is absent.

- [ ] **Step 3: Document package generation**

Append this section to `tools/README.md`:

````markdown
## Qualified mapping review packages

Generate one reviewer package from an exact commit into an empty directory
outside every Git worktree:

```powershell
$candidate = git rev-parse HEAD
$output = Join-Path ([System.IO.Path]::GetTempPath()) "esaf-uk-review-core"
python tools/build_mapping_review_bundle.py `
  --commit $candidate `
  --mapping-set-id uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0 `
  --output $output
```

Repeat with each allowlisted mapping-set identifier and a distinct empty
output directory. Preserve the exact commit and printed manifest SHA-256 in
the review record.

The package contains tracked ESAF mapping evidence, referenced controls,
schemas, protocol, and blank worksheets. It does not include the external
source document. Reviewers obtain authorized access independently. Package
generation does not change Draft lifecycle state or constitute qualified
review.
````

- [ ] **Step 4: Run all focused tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_build_mapping_review_bundle -v
python -m unittest tests.test_mapping_review_protocol -v
```

Expected: `Ran 14 tests` and `Ran 4 tests`; both commands end in `OK`.

- [ ] **Step 5: Generate every package twice and compare**

Use two system-temporary roots outside all worktrees:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$candidate = git rev-parse HEAD
$runA = Join-Path ([System.IO.Path]::GetTempPath()) "esaf-uk-review-run-a"
$runB = Join-Path ([System.IO.Path]::GetTempPath()) "esaf-uk-review-run-b"
```

Ensure those exact directories do not exist or are empty. For each identifier
in `PROFILES`, invoke the CLI once beneath `$runA` and once beneath `$runB`.
Compare matching `PACKAGE_MANIFEST.json` bytes and recursively compare the
SHA-256 of every file. Expected: three matching package pairs and no PDF,
Word, cache, or repository modification.

- [ ] **Step 6: Commit the integration/documentation slice**

```powershell
git add -- tools/README.md tests/test_build_mapping_review_bundle.py
git commit -m "docs: document qualified review package workflow"
```

---

### Task 6: Whole-branch review, validation, and pull request

**Files:**
- Review: every file changed from `git merge-base main HEAD` through `HEAD`.
- Do not modify mapping snapshots unless a verified defect is found; any such
  change requires both a regression test and a new exact-head review cycle.

**Interfaces:**
- Consumes: the complete implementation branch.
- Produces: exact-SHA review evidence, a passing pull request, and a merged
  preparation capability; it does not produce qualified mapping-review
  evidence.

- [ ] **Step 1: Run focused and full validation**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_mapping_review_protocol -v
python -m unittest tests.test_build_mapping_review_bundle -v
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
$base = git merge-base main HEAD
git diff --check "$base..HEAD"
```

Expected: every command exits `0`; the suite retains only the established
Windows symlink skips; all three mapping sets and 404 records remain Draft.

- [ ] **Step 2: Verify repository hygiene**

```powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__
git status --short
git diff --name-only "$base..HEAD" | Select-String -Pattern '\.(pdf|docx?|zip)$'
```

Expected: no cache directories, clean status, and no generated/source/archive
artifacts in the branch diff.

- [ ] **Step 3: Dispatch independent reviews on the exact head**

Record `git rev-parse HEAD`, then obtain:

1. specification review against
   `docs/superpowers/specs/2026-07-23-uk-qualified-review-preparation-design.md`;
2. security/overclaiming review of package boundaries, path handling,
   source-rights protection, lifecycle nonclaims, and test coverage; and
3. final whole-branch review.

Resolve every Critical and Important finding. Add a focused regression test
before fixing publication-gate defects when practical. If `HEAD` changes,
rerun affected validations and all three reviews on the new exact SHA.

- [ ] **Step 4: Push and open a reviewable pull request**

Push `agent/uk-qualified-review-preparation` and open a pull request linked to
issue `#55`. Its body shall include:

- the exact reviewed head SHA;
- the design and plan locators;
- focused/full validation commands and exact results;
- independent review identities or agent task names and dispositions;
- confirmation that all three mapping sets and all 404 records remain Draft;
- confirmation that no external source document is packaged;
- confirmation that no qualified human reviewer has yet been identified; and
- `Preparation only: does not close #55 and does not establish qualified review.`

- [ ] **Step 5: Verify checks, head identity, and merge state**

Require passing GitHub checks and a clean merge state. Compare the PR head to
the reviewed SHA immediately before merge. If they differ, do not merge;
repeat the exact-head gates.

- [ ] **Step 6: Merge and validate main proportionally**

After merge, update local `main`, run the two focused modules,
`validate_crosswalks.py --check`, `validate_links.py --check`, and
`git status --short`. Expected: all pass and local `main` is clean.

- [ ] **Step 7: Generate merged-SHA packages and recruit reviewers**

From the exact merged `main` SHA, generate Core, Plus forward, and Plus reverse
packages into distinct system-temporary directories. Post one issue `#55`
comment containing:

- merged candidate SHA;
- three mapping-set IDs, labels, directions, and manifest SHA-256 values;
- protocol and generator locators;
- specification/inventory and security/overclaiming role requirements;
- qualification, independence, conflict, and authorized-access criteria;
- a request to express interest without posting sensitive or licensed
  material publicly; and
- `All three mappings remain Draft. This comment recruits reviewers; it does
  not record or imply qualified review.`

Do not close the issue, assign an unverified reviewer, or change mapping
lifecycle metadata.

- [ ] **Step 8: Clean only owned temporary state**

Remove the three temporary package directories after their manifest values
and issue-comment evidence are recorded. Remove only the owned worktree and
local/remote feature branch after verifying merge. Do not alter unrelated
branches, worktrees, or stale worktree metadata.
