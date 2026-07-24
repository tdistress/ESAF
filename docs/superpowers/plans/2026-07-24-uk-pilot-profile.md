# ESAF-1800 United Kingdom Pilot Profile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish and enforce a reusable ESAF-1800 profile contract plus one Draft United Kingdom jurisdiction pilot covering the complete ESAF control catalog.

**Architecture:** Add one concise normative standard, five strict component schemas, and a modular versioned pilot package. A fail-closed Python validator will load package-local components, derive the authoritative control population, enforce closed traceability and lifecycle-aware external references, and reuse ESAF-1500 assertion-aware claim detection.

**Tech Stack:** Markdown; JSON Schema Draft 2020-12; Python 3.13 standard library; `jsonschema`; `unittest`; GitHub Actions.

## Global Constraints

- Canonical profile identifier: `uk--jurisdiction-profile--0.1.0`.
- Schema version and profile version: `0.1.0`.
- Profile lifecycle status: `draft`; target ESAF release: `v0.5-beta`.
- Applicability: AI systems deployed or operated in the United Kingdom, regardless of organizational domicile.
- Source boundary: ESAF and the three pinned UK Cyber Essentials mapping sets already present in the repository.
- Every one of the 91 authoritative controls appears exactly once as `required`, `conditional`, `recommended`, or `not_selected`.
- Referenced mappings remain Draft, reference-only, and separately qualified-review gated.
- Reuse ESAF-1500 assessment and maturity semantics; never define a profile-local maturity scale.
- Do not claim legal sufficiency, compliance, certification, equivalence, endorsement, external approval, or production readiness.
- Do not add dependencies or Mermaid diagrams.
- Set `PYTHONDONTWRITEBYTECODE=1` for validation and leave no generated caches.

---

## File map

**Create**

- `profiles/ESAF-1800.md` — normative reusable profile contract.
- `profiles/schema/profile.schema.json` — root identity, lifecycle, scope, condition catalog, and component-path contract.
- `profiles/schema/control-selections.schema.json` — complete control-ledger contract.
- `profiles/schema/risk-overlays.schema.json` — additional-risk and strengthening-overlay contract.
- `profiles/schema/evidence-expectations.schema.json` — ESAF-1500-bound evidence contract.
- `profiles/schema/external-references.schema.json` — immutable mapping-reference contract.
- `profiles/uk/0.1.0/README.md` — human publication and limitations.
- `profiles/uk/0.1.0/profile.json` — pilot root manifest.
- `profiles/uk/0.1.0/control-selections.json` — 91-control ledger.
- `profiles/uk/0.1.0/risk-overlays.json` — bounded technical risks and overlays.
- `profiles/uk/0.1.0/evidence-expectations.json` — profile evidence strengthening.
- `profiles/uk/0.1.0/external-references.json` — exact three Draft mapping references.
- `tools/validate_profiles.py` — package, schema, semantic, traceability, lifecycle, and claim validator.
- `tests/profile_fixture.py` — canonical synthetic valid-package builder for negative validator tests.
- `tests/test_profile_foundation.py` — normative, schema, package, and integration invariants.
- `tests/test_validate_profiles.py` — validator behavior and negative cases.
- `docs/superpowers/reviews/2026-07-24-uk-pilot-profile-technical-review.md` — exact-SHA technical disposition.
- `docs/superpowers/reviews/2026-07-24-uk-pilot-profile-editorial-review.md` — exact-SHA editorial disposition.
- `docs/superpowers/reviews/2026-07-24-uk-pilot-profile-scope-review.md` — exact-SHA scope disposition.
- `docs/superpowers/reviews/2026-07-24-uk-pilot-profile-overclaiming-review.md` — exact-SHA overclaiming disposition.

**Modify**

- `.github/workflows/catalog-validation.yml` — profile path filters and validation step.
- `README.md` — link ESAF-1800 and the pilot.
- `CONTRIBUTING.md` — profile authoring and validation commands.
- `framework/ESAF-1000.md` — link the concrete ESAF-1800 contract.
- `profiles/README.md` — replace introductory copy with contract and pilot indexes.
- `project/BACKLOG.md` — remove the completed pilot workstream only at publication readiness.
- `tools/README.md` — document `validate_profiles.py`.
- `tests/test_release_metadata.py` — enforce backlog and milestone integration.

---

### Task 1: Normative ESAF-1800 contract

**Files:**
- Create: `tests/test_profile_foundation.py`
- Create: `profiles/ESAF-1800.md`

**Interfaces:**
- Consumes: ESAF normative-language conventions; `assessment/ESAF-1500.md`; `controls/ESAF-1100.md`.
- Produces: headings and exact selection vocabulary consumed by schemas, validator tests, and pilot content.

- [ ] **Step 1: Write failing normative-contract tests**

Create `tests/test_profile_foundation.py` with:

```python
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "profiles" / "ESAF-1800.md"


class ProfileFoundationTests(unittest.TestCase):
    def test_normative_contract_has_required_sections(self) -> None:
        text = STANDARD.read_text(encoding="utf-8")
        for heading in (
            "## Purpose and scope",
            "## Profile identity and lifecycle",
            "## Applicability and system boundary",
            "## Control selections",
            "## Additional risks and overlays",
            "## Evidence and assessment",
            "## External references",
            "## Traceability and validation",
            "## Non-claim boundaries",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_selection_vocabulary_is_closed_and_explained(self) -> None:
        text = STANDARD.read_text(encoding="utf-8")
        for value in ("`required`", "`conditional`", "`recommended`", "`not_selected`"):
            self.assertIn(value, text)
        self.assertIn("does not declare the underlying ESAF control inapplicable", text)

    def test_contract_reuses_assessment_semantics_and_preserves_controls(self) -> None:
        text = STANDARD.read_text(encoding="utf-8")
        self.assertIn("[ESAF-1500](../assessment/ESAF-1500.md)", text)
        self.assertIn("shall not define a profile-local replacement maturity scale", text)
        self.assertIn("shall not alter or weaken a core control", text)
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_profile_foundation -v
```

Expected: errors because `profiles/ESAF-1800.md` does not exist.

- [ ] **Step 3: Write the normative contract**

Create `profiles/ESAF-1800.md` using the tested headings. Include exact `shall` requirements for versioned package identity, applicability evidence, complete control selection, condition activation, closed traceability, ESAF-1500 reuse, lifecycle-aware external references, and all non-claims from the approved design. State that `recommended` uses `should` and cannot affect ESAF conformance.

- [ ] **Step 4: Run the focused tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_profile_foundation -v
python tools/validate_links.py --check
```

Expected: all profile-foundation tests pass and all links resolve.

- [ ] **Step 5: Commit**

```powershell
git add profiles/ESAF-1800.md tests/test_profile_foundation.py
git diff --cached --check
git commit -m "docs: define ESAF-1800 profile contract"
```

---

### Task 2: Strict component schemas

**Files:**
- Create: `profiles/schema/profile.schema.json`
- Create: `profiles/schema/control-selections.schema.json`
- Create: `profiles/schema/risk-overlays.schema.json`
- Create: `profiles/schema/evidence-expectations.schema.json`
- Create: `profiles/schema/external-references.schema.json`
- Modify: `tests/test_profile_foundation.py`

**Interfaces:**
- Consumes: selection vocabulary and component responsibilities from Task 1.
- Produces: five schema documents loaded by `validate_profiles.schema_diagnostics()` in Task 3.

- [ ] **Step 1: Add failing schema-contract tests**

Add:

```python
import json
from jsonschema import Draft202012Validator

SCHEMA_ROOT = ROOT / "profiles" / "schema"
SCHEMA_NAMES = (
    "profile",
    "control-selections",
    "risk-overlays",
    "evidence-expectations",
    "external-references",
)


class ProfileSchemaTests(unittest.TestCase):
    def test_schemas_are_strict_draft_2020_12(self) -> None:
        for name in SCHEMA_NAMES:
            schema = json.loads(
                (SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8")
            )
            Draft202012Validator.check_schema(schema)
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertFalse(schema["additionalProperties"])

    def test_control_status_and_profile_lifecycle_are_closed(self) -> None:
        selections = json.loads(
            (SCHEMA_ROOT / "control-selections.schema.json").read_text(encoding="utf-8")
        )
        status = selections["$defs"]["selection"]["properties"]["status"]["enum"]
        self.assertEqual(status, ["required", "conditional", "recommended", "not_selected"])
        profile = json.loads((SCHEMA_ROOT / "profile.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["properties"]["status"]["const"], "draft")
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m unittest tests.test_profile_foundation.ProfileSchemaTests -v`

Expected: errors for five missing schemas.

- [ ] **Step 3: Implement all five schemas**

Use this common root shape in every schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://esaf.dev/schema/profiles/<component>/0.1.0",
  "type": "object",
  "additionalProperties": false,
  "required": ["$schema", "schema_version", "profile_id", "profile_version"],
  "properties": {
    "$schema": {"const": "../../../schema/<component>.schema.json"},
    "schema_version": {"const": "0.1.0"},
    "profile_id": {"const": "uk--jurisdiction-profile--0.1.0"},
    "profile_version": {"const": "0.1.0"}
  }
}
```

Extend each schema with the exact fields in the design. Define reusable `$defs` for identifiers, non-empty strings, repository-relative paths, selection records, risks, overlays, evidence expectations, and external references. Every nested object sets `additionalProperties: false`.

`profile.schema.json` shall require boolean applicability conditions with `activates_when` and `resolution_evidence`. `external-references.schema.json` shall close `reference_use` to `lifecycle_reference_only` and require `qualified_review_required` to be `true`.
The reusable component schemas shall allow empty risk, overlay, and evidence
arrays; Task 5 foundation tests, rather than the generic schemas, shall require
the UK pilot to publish the approved non-empty content.

- [ ] **Step 4: Run schema tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_profile_foundation.ProfileSchemaTests -v
python -m unittest tests.test_assessment_foundation -v
```

Expected: both modules pass.

- [ ] **Step 5: Commit**

```powershell
git add profiles/schema tests/test_profile_foundation.py
git diff --cached --check
git commit -m "feat: define strict ESAF profile schemas"
```

---

### Task 3: Fail-closed package loader

**Files:**
- Create: `tools/validate_profiles.py`
- Create: `tests/profile_fixture.py`
- Create: `tests/test_validate_profiles.py`

**Interfaces:**
- Produces:
  - `ProfilePackage` dataclass with `directory: Path`, `relative: str`, and `documents: dict[str, dict[str, object]]`.
  - `load_json(path: Path) -> object`.
  - `schema_diagnostics(schema: dict[str, object], document: object, relative: str) -> list[str]`.
  - `discover_profile_packages(root: Path) -> tuple[Path, ...]`.
  - `load_package(root: Path, directory: Path, diagnostics: list[str]) -> ProfilePackage | None`.
  - `validate(root: Path = ROOT) -> list[str]`.
  - `main(argv: Sequence[str] | None = None, *, root: Path | None = None) -> int`.
  - `tests.profile_fixture.write_valid_profile_fixture(root: Path) -> Path`.

- [ ] **Step 1: Write failing loader and CLI tests**

Create `tests/profile_fixture.py`. Its `write_valid_profile_fixture()` shall
copy `profiles/schema`, `controls/catalog.json`, and `crosswalks/registry`,
then write a synthetic `profiles/uk/0.1.0` package that conforms to the five
schemas. It shall derive selection records from the copied control catalog,
classify them `not_selected` with the rationale `Synthetic validator fixture;
the profile adds no selection`, define one inactive boolean condition, use
empty risk/overlay/evidence arrays, and write
the exact three lifecycle-only mapping references. This is test data, not
published pilot content.

Use that builder in each test:

Use:

```python
class ProfileValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.package = write_valid_profile_fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_population_has_no_errors(self) -> None:
        self.assertEqual(validate_profiles.validate(self.root), [])

    def test_duplicate_json_key_is_rejected(self) -> None:
        path = self.root / "profiles/uk/0.1.0/profile.json"
        text = path.read_text(encoding="utf-8").replace(
            '"profile_version":', '"profile_version": "duplicate",\n"profile_version":', 1
        )
        path.write_text(text, encoding="utf-8")
        self.assertTrue(any("duplicate JSON key" in e for e in validate_profiles.validate(self.root)))
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m unittest tests.test_validate_profiles -v`

Expected: import error because `tools/validate_profiles.py` does not exist.

- [ ] **Step 3: Implement the loader and CLI**

Implement duplicate-key rejection with `json.load(..., object_pairs_hook=reject_duplicate_keys)`. Discover only `profiles/<country>/<semver>/profile.json`, excluding `profiles/schema`. Require the exact six package files from the design and reject every other file.

For every candidate path:

```python
def safe_component(package: Path, relative: str) -> Path | None:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        return None
    candidate = package.joinpath(*pure.parts)
    if any(part.is_symlink() for part in (candidate, *candidate.parents) if part != package.parent):
        return None
    try:
        candidate.resolve(strict=True).relative_to(package.resolve(strict=True))
    except (OSError, ValueError):
        return None
    return candidate
```

Validate schema shape before adding a document to `ProfilePackage.documents`. Sort and deduplicate diagnostics before returning. `main()` requires `--check`, prints one success summary, returns `1` for content errors, and catches operational failures to return `2`.

- [ ] **Step 4: Run and verify GREEN**

Run: `python -m unittest tests.test_validate_profiles -v`

Expected: loader, schema, and CLI tests pass.

- [ ] **Step 5: Commit**

```powershell
git add tools/validate_profiles.py tests/profile_fixture.py tests/test_validate_profiles.py
git diff --cached --check
git commit -m "feat: add fail-closed profile package loader"
```

---

### Task 4: Semantic, traceability, lifecycle, and claim validation

**Files:**
- Modify: `tools/validate_profiles.py`
- Modify: `tests/test_validate_profiles.py`
- Modify: `tests/test_validate_assessment.py`

**Interfaces:**
- Consumes: `tools.validate_assessment.asserted_prohibited_phrases`.
- Produces:
  - `control_population(root: Path) -> set[str]`.
  - `registry_metadata(path: Path) -> dict[str, object]`.
  - `semantic_diagnostics(root: Path, package: ProfilePackage) -> list[str]`.
  - `traceability_diagnostics(package: ProfilePackage) -> list[str]`.
  - `claim_diagnostics(package: ProfilePackage) -> list[str]`.

- [ ] **Step 1: Add failing semantic tests**

Add one test per invariant: missing and duplicate controls, invalid condition usage, unresolved risks/overlays/evidence, asymmetric reciprocal links, wrong registry path/status, fourth mapping, imported relationship fields, replacement/waiver language, local maturity scale, positive prohibited claim, explicit denial, quotation, and stable diagnostic ordering.

Pin existing claim behavior before reuse:

```python
def test_profile_reuse_does_not_change_assessment_claim_classifier(self) -> None:
    self.assertEqual(
        list(asserted_prohibited_phrases("This result does not establish compliance.")),
        [],
    )
    self.assertEqual(
        list(asserted_prohibited_phrases("This result establishes compliance.")),
        ["compliance"],
    )
```

- [ ] **Step 2: Run and verify RED**

Run:

```powershell
python -m unittest tests.test_validate_profiles tests.test_validate_assessment -v
```

Expected: new profile semantic tests fail while existing assessment tests remain green.

- [ ] **Step 3: Implement semantic validation**

Load control IDs from `controls/catalog.json["controls"][*]["id"]` and require set equality plus record-count equality. Enforce status/condition rules. Build identifier maps before resolving links. Require reciprocal overlay/evidence links to agree.

Import assertion logic without changing `validate_assessment.py`:

```python
if __package__:
    from .validate_assessment import asserted_prohibited_phrases
else:
    from validate_assessment import asserted_prohibited_phrases
```

Scan narrative JSON fields and the package README. Report only affirmative prohibited assertions. Parse registry front matter and require exact identifier, path, and `draft` status for the three allowlisted mapping sets. Reject relationship, disposition, supported-outcome, equivalence, or evidence-import fields anywhere in external references.

- [ ] **Step 4: Run and verify GREEN**

Run:

```powershell
python -m unittest tests.test_validate_profiles tests.test_validate_assessment -v
python tools/validate_profiles.py --check
python tools/validate_assessment.py --check
```

Expected: both test modules and both validators pass.

- [ ] **Step 5: Commit**

```powershell
git add tools/validate_profiles.py tests/test_validate_profiles.py tests/test_validate_assessment.py
git diff --cached --check
git commit -m "feat: enforce profile semantic invariants"
```

---

### Task 5: Author the Draft UK pilot package

**Files:**
- Create: `profiles/uk/0.1.0/README.md`
- Create: `profiles/uk/0.1.0/profile.json`
- Create: `profiles/uk/0.1.0/control-selections.json`
- Create: `profiles/uk/0.1.0/risk-overlays.json`
- Create: `profiles/uk/0.1.0/evidence-expectations.json`
- Create: `profiles/uk/0.1.0/external-references.json`
- Modify: `tests/test_profile_foundation.py`

**Interfaces:**
- Consumes: all schemas and validator interfaces from Tasks 2–4.
- Produces: the only conforming Draft profile package for `v0.5-beta`.

- [ ] **Step 1: Add failing content tests**

Test the exact profile ID, Draft status, UK operating applicability, exact component list, complete 91-control population, at least one of every selection status, exact three mapping identifiers, `lifecycle_reference_only`, and explicit non-claims.

- [ ] **Step 2: Run and verify RED**

Run: `python -m unittest tests.test_profile_foundation -v`

Expected: pilot-package assertions fail until all content is authored.

- [ ] **Step 3: Author `profile.json` and `README.md`**

Define boolean condition records for the bounded facts actually used by selections and overlays, including internet exposure, external provider use, third-party administration, untrusted software intake, and unsupported-component presence. Each question identifies resolution evidence. State that scope does not equal a Cyber Essentials or legal scope.

- [ ] **Step 4: Author the 91-control ledger**

Generate the initial ordered record skeleton from `controls/catalog.json`, then inspect the exact normative text of every control before classifying it. For every record, write an original profile rationale. Use `required` only for universal UK operating-scope relevance, `conditional` only with defined condition IDs, `recommended` only as non-conformance guidance, and `not_selected` only to mean no additional profile selection.

Run after each control family:

```powershell
python tools/validate_profiles.py --check
python -m unittest tests.test_profile_foundation tests.test_validate_profiles -v
```

Expected: diagnostics decrease without introducing duplicate or missing controls.

- [ ] **Step 5: Author risks, overlays, and evidence expectations**

Create bounded records for exposed infrastructure, insecure configuration and privileged access, vulnerable or unsupported components, malware and untrusted software paths, cloud and third-party responsibility gaps, and incomplete scope/asset/evidence coverage. Close every risk → overlay → control/evidence link and every reciprocal overlay/evidence link. Reuse ESAF-1500 quality names verbatim.

- [ ] **Step 6: Author exact external references**

Add only the three identifiers in the design. Each record uses its actual registry path, `expected_status: "draft"`, `reference_use: "lifecycle_reference_only"`, and `qualified_review_required: true`. Include no relationship or evidence fields.

- [ ] **Step 7: Run and verify GREEN**

Run:

```powershell
python -m unittest tests.test_profile_foundation tests.test_validate_profiles -v
python tools/validate_profiles.py --check
python tools/validate_controls.py --check
python tools/validate_crosswalks.py --check
```

Expected: focused tests pass; profile summary reports one Draft package and 91 selections; affected validators pass.

- [ ] **Step 8: Commit**

```powershell
git add profiles/uk tests/test_profile_foundation.py
git diff --cached --check
git commit -m "feat: publish Draft UK pilot profile"
```

---

### Task 6: Repository, CI, and release integration

**Files:**
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `framework/ESAF-1000.md`
- Modify: `profiles/README.md`
- Modify: `project/BACKLOG.md`
- Modify: `tools/README.md`
- Modify: `tests/test_profile_foundation.py`
- Modify: `tests/test_release_metadata.py`

**Interfaces:**
- Consumes: `python tools/validate_profiles.py --check`.
- Produces: discoverable publication, CI enforcement, and completed-workstream metadata.

- [ ] **Step 1: Add failing integration tests**

Require links from the root/framework/profile indexes, validator documentation, CI path filters for `profiles/**` and `tools/validate_profiles.py`, a `Validate profiles` workflow step, and removal of the completed pilot backlog line while preserving qualified-review and PCI DSS work.

- [ ] **Step 2: Run and verify RED**

Run:

```powershell
python -m unittest tests.test_profile_foundation tests.test_release_metadata -v
```

Expected: new integration assertions fail.

- [ ] **Step 3: Update indexes and contributor documentation**

Link `profiles/ESAF-1800.md` and `profiles/uk/0.1.0/README.md`. Document package editing rules, mandatory Draft/non-claim language, and the exact validator command.

- [ ] **Step 4: Update CI and backlog**

Add `profiles/**` and the profile validator to pull-request and push path filters. Add:

```yaml
      - name: Validate profiles
        run: python tools/validate_profiles.py --check
```

Remove only the completed pilot bullet from `project/BACKLOG.md`.

- [ ] **Step 5: Run and verify GREEN**

Run:

```powershell
python -m unittest tests.test_profile_foundation tests.test_release_metadata -v
python tools/validate_profiles.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
```

Expected: all commands pass.

- [ ] **Step 6: Commit**

```powershell
git add .github/workflows/catalog-validation.yml README.md CONTRIBUTING.md framework/ESAF-1000.md profiles/README.md project/BACKLOG.md tools/README.md tests/test_profile_foundation.py tests/test_release_metadata.py
git diff --cached --check
git commit -m "docs: integrate UK pilot profile"
```

---

### Task 7: Whole-branch review and remediation

**Files:**
- Create: the four review records listed in the file map.
- Modify: any candidate file required to resolve a finding.

**Interfaces:**
- Consumes: exact candidate SHA and `git diff $(git merge-base main HEAD)..HEAD`.
- Produces: four exact-SHA review dispositions with severity, evidence, and resolution.

- [ ] **Step 1: Stabilize a review candidate**

Run all focused tests and validators from Task 8 except the full suite. Record:

```powershell
$base=git merge-base main HEAD
$candidate=git rev-parse HEAD
git diff --check "$base..$candidate"
```

- [ ] **Step 2: Dispatch independent exact-SHA reviews**

Use separate reviewers for:

1. technical/schema/validator correctness;
2. normative/editorial consistency;
3. profile applicability, control selection, and source boundary;
4. overclaiming, mapping leakage, and lifecycle separation.

Each reviewer shall inspect the complete merge-base range and report Critical, Important, and Minor findings with exact paths. Record “no findings” explicitly when applicable.

- [ ] **Step 3: Resolve findings with focused regression tests**

For each Critical or Important defect, add a failing test first, implement the smallest correction, rerun affected tests, and commit. Resolve or explicitly disposition Minor findings.

- [ ] **Step 4: Re-dispatch reviews after candidate changes**

If any candidate content changes, obtain all four reviews again on the new exact head. Do not carry prior approval forward.

- [ ] **Step 5: Commit review records**

```powershell
git add docs/superpowers/reviews
git diff --cached --check
git commit -m "docs: record UK pilot profile reviews"
```

The review-record commit changes the head. These records preserve the detailed
content review, but they are not the final exact-head approval. Task 8 obtains
fresh confirmations on the pushed final SHA and records them externally
without changing the branch.

---

### Task 8: Exact-candidate publication validation and pull request

**Files:**
- Modify: PR description and issue `#57` evidence only after local gates pass.

**Interfaces:**
- Consumes: final reviewed branch.
- Produces: reviewable Draft PR with exact-SHA evidence; issue closes only after merge.

- [ ] **Step 1: Run the full exact-candidate gate**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -v
python tools/validate_profiles.py --check
python tools/validate_assessment.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
$base=git merge-base main HEAD
git diff --check "$base..HEAD"
```

Expected: 0 failures, only documented Windows symlink skips, all validators successful, and no diff errors.

- [ ] **Step 2: Verify repository hygiene**

```powershell
git status --porcelain
rg --files -g '**/__pycache__/**'
git diff --name-only "$(git merge-base main HEAD)..HEAD"
```

Expected: clean status, no cache files, and only issue-`#57` scope.

- [ ] **Step 3: Push and open a Draft PR**

```powershell
git push -u origin agent/uk-pilot-profile
```

The PR body shall include `Closes #57`, the exact head and merge-base SHAs, derived selection-status counts, exact validation results, four review dispositions, and all Draft/non-claim boundaries.

- [ ] **Step 4: Require GitHub validation and clean merge state**

Verify the PR head still equals the reviewed SHA, `Validate ESAF sources` passes, and GitHub reports a clean mergeable state. If the head changes, rerun every affected local and independent-review gate.

- [ ] **Step 5: Obtain final exact-head review confirmations**

Dispatch the four independent reviewers against the pushed PR head, including
the committed review records. Record each confirmation as immutable PR or
issue evidence naming the exact full SHA. Do not modify the branch afterward.
All four confirmations must report no unresolved Critical or Important
findings; otherwise return to Task 7 and repeat the affected gates.

- [ ] **Step 6: Merge only after explicit completion authorization**

After merge, fast-forward local `main`, run focused profile tests and validators on the merge commit, add exact evidence to issue `#57`, and remove only `agent/uk-pilot-profile` and its owned worktree.
