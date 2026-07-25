# UK Pilot Profile Whole-Branch Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve every whole-branch review finding so the reusable ESAF-1800 validator fails closed, the Draft UK pilot uses exact factual applicability, and four independent reviewers can approve one exact candidate.

**Architecture:** Separate reusable profile validation from a profile-scoped UK pilot policy. Harden inventory, identity, formats, external-reference lifecycle resolution, source authority, and assertion detection in the generic layer; then align the normative documents and UK traceability graph without changing the three strategic ESAF pillars or importing external outcomes.

**Tech Stack:** Markdown; JSON Schema Draft 2020-12; Python 3.13; `jsonschema`; Python `unittest`; GitHub Actions; Git.

## Global Constraints

- Canonical pilot identifier remains `uk--jurisdiction-profile--0.1.0`.
- The pilot lifecycle remains `draft` and targets `v0.5-beta`.
- Generic validation shall not require future profiles to cite UK Cyber Essentials mappings.
- The UK pilot shall retain exactly its three pinned Draft lifecycle references.
- Every one of the 91 authoritative controls shall remain present exactly once.
- Component paths are package-relative; `$schema` values are document-relative.
- Mapping editorial state shall not be inferred solely from an empty event array.
- Risks and overlays shall be original ESAF synthesis.
- Do not import mapping relationships, external outcomes, or external evidence.
- Do not claim legal sufficiency, compliance, certification, equivalence, endorsement, external approval, Cyber Essentials implementation, or production readiness.
- Use test-driven development for every behavioral correction.
- Set `PYTHONDONTWRITEBYTECODE=1`; do not commit caches or generated build output.
- After any candidate change, all four whole-branch reviews shall run again on the same exact full SHA.

---

## File map

**Primary implementation**

- `tools/validate_profiles.py` — generic inventory, package loading, schema, semantic, source, lifecycle, assertion, and exit behavior.
- `profiles/schema/profile.schema.json` — reusable profile identity/version/date contract.
- `profiles/schema/control-selections.schema.json` — reusable component version contract.
- `profiles/schema/risk-overlays.schema.json` — reusable component version and source-basis contract.
- `profiles/schema/evidence-expectations.schema.json` — reusable component version contract.
- `profiles/schema/external-references.schema.json` — reusable component version and external-reference contract.
- `tests/profile_fixture.py` — valid generic and UK package fixtures.
- `tests/test_validate_profiles.py` — negative and operational validator coverage.
- `tests/test_profile_foundation.py` — normative, schema, UK content, graph, and workflow invariants.

**Normative and companion alignment**

- `profiles/ESAF-1800.md`
- `docs/superpowers/specs/2026-07-24-uk-pilot-profile-design.md`
- `docs/superpowers/plans/2026-07-24-uk-pilot-profile.md`
- `profiles/README.md`
- `CONTRIBUTING.md`
- `tools/README.md`

**UK package correction**

- `profiles/uk/0.1.0/README.md`
- `profiles/uk/0.1.0/profile.json`
- `profiles/uk/0.1.0/control-selections.json`
- `profiles/uk/0.1.0/risk-overlays.json`
- `profiles/uk/0.1.0/evidence-expectations.json`
- `profiles/uk/0.1.0/external-references.json`

**Review records**

- `docs/superpowers/reviews/2026-07-24-uk-pilot-profile-technical-review.md`
- `docs/superpowers/reviews/2026-07-24-uk-pilot-profile-editorial-review.md`
- `docs/superpowers/reviews/2026-07-24-uk-pilot-profile-scope-review.md`
- `docs/superpowers/reviews/2026-07-24-uk-pilot-profile-overclaiming-review.md`

---

### Task 1: Fail-closed inventory, identity, formats, and operational errors

**Files:**
- Modify: `tools/validate_profiles.py`
- Modify: `profiles/schema/profile.schema.json`
- Modify: `profiles/schema/control-selections.schema.json`
- Modify: `profiles/schema/risk-overlays.schema.json`
- Modify: `profiles/schema/evidence-expectations.schema.json`
- Modify: `profiles/schema/external-references.schema.json`
- Modify: `tests/profile_fixture.py`
- Modify: `tests/test_profile_foundation.py`
- Modify: `tests/test_validate_profiles.py`

**Interfaces:**
- Produces: `inventory_profile_packages(root: Path) -> tuple[tuple[Path, ...], list[str]]`.
- Produces: `OperationalProfileError`, carrying a repository-relative sanitized diagnostic.
- Preserves: `validate(root: Path = ROOT) -> list[str]` for content diagnostics.
- Preserves: CLI exit `0` success, `1` content failure, `2` operational failure.

- [ ] **Step 1: Add inventory, identity, date, and operational RED tests**

Add focused tests with these assertions:

```python
def test_zero_profile_packages_is_rejected(self) -> None:
    self.remove_valid_package()
    self.assertIn("profiles: no profile packages found", validate(self.root))

def test_invalid_profile_domain_version_entry_is_rejected(self) -> None:
    (self.root / "profiles" / "example" / "not-semver").mkdir(parents=True)
    self.assertTrue(any("invalid profile version directory" in item for item in validate(self.root)))

def test_profile_id_version_must_match_manifest_and_directory(self) -> None:
    self.rewrite_all_profile_ids("example--risk-profile--9.9.9")
    self.assertTrue(any("profile_id version 9.9.9 does not match profile_version 0.1.0" in item for item in validate(self.root)))

def test_invalid_calendar_date_is_rejected(self) -> None:
    self.manifest()["change_history"][0]["date"] = "2026-02-30"
    self.assertTrue(any("is not a 'date'" in item for item in validate(self.root)))

def test_component_permission_error_is_operational_and_sanitized(self) -> None:
    with mock.patch("tools.validate_profiles.load_json", side_effect=PermissionError(r"C:\secret\profile.json")):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(2, main(["--check"], root=self.root))
    self.assertNotIn(r"C:\secret", stderr.getvalue())
```

Also add schema tests proving a valid non-`0.1.0` semantic version is reusable when the identifier and directory agree.

- [ ] **Step 2: Run RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_validate_profiles tests.test_profile_foundation.ProfileSchemaTests -v
```

Expected: the new inventory, identity, format, reusable-version, and operational tests fail for the reproduced reasons.

- [ ] **Step 3: Implement fail-closed inventory and operational separation**

Introduce:

```python
class OperationalProfileError(RuntimeError):
    pass


def inventory_profile_packages(root: Path) -> tuple[tuple[Path, ...], list[str]]:
    packages: list[Path] = []
    diagnostics: list[str] = []
    # Inspect every non-schema profile-domain and version entry.
    # Append diagnostics for aliases, symlinks, malformed names, and missing manifests.
    # Require at least one package in this repository.
    return tuple(sorted(packages)), sorted(set(diagnostics))
```

Use `jsonschema.FormatChecker()` with `Draft202012Validator`. Parse the
`profile_id` suffix with the existing identifier pattern and compare it to both
`profile_version` and `package.name`. Sanitize `OSError` and `PermissionError`
without embedding the exception path; propagate them as
`OperationalProfileError` so `main()` returns `2`.

Change every component schema `profile_version` from a pilot-only `const` to the
same semantic-version pattern used by the identifier suffix.

- [ ] **Step 4: Run GREEN and regression gates**

Run:

```powershell
python -m unittest tests.test_validate_profiles tests.test_profile_foundation.ProfileSchemaTests -v
python tools/validate_profiles.py --check
git diff --check
```

Expected: focused tests pass with only documented symlink skips; one repository
package validates; diff check is clean.

- [ ] **Step 5: Commit**

```powershell
git add tools/validate_profiles.py profiles/schema tests/profile_fixture.py tests/test_validate_profiles.py tests/test_profile_foundation.py
git diff --cached --check
git commit -m "fix: fail closed on profile inventory and identity"
```

---

### Task 2: Reusable external references and mapping lifecycle separation

**Files:**
- Modify: `tools/validate_profiles.py`
- Modify: `profiles/schema/external-references.schema.json`
- Modify: `tests/profile_fixture.py`
- Modify: `tests/test_validate_profiles.py`
- Modify: `tests/test_profile_foundation.py`

**Interfaces:**
- Produces: generic declared-reference validation from `crosswalks/catalog.json`.
- Produces: `mapping_reference_metadata(root: Path, mapping_set_id: str, registry_path: str) -> dict[str, object]`.
- Produces: profile-scoped UK invariant keyed by `uk--jurisdiction-profile--0.1.0`.

- [ ] **Step 1: Add external-reference RED tests**

Add tests proving:

```python
def test_generic_profile_may_have_no_external_references(self) -> None:
    package = self.generic_package(external_references=[])
    self.assertEqual([], semantic_diagnostics(package, self.root))

def test_future_profile_is_not_forced_to_use_uk_mappings(self) -> None:
    package = self.generic_package(profile_id="example--sector-profile--1.2.3", external_references=[])
    self.assertFalse(any("UK pilot mapping references" in item for item in semantic_diagnostics(package, self.root)))

def test_uk_pilot_still_requires_exact_three_references(self) -> None:
    self.external_references().pop()
    self.assertTrue(any("exactly three" in item for item in validate(self.root)))

def test_reviewed_snapshot_is_not_inferred_as_draft_from_empty_events(self) -> None:
    self.set_catalog_editorial_status("reviewed")
    self.set_expected_status("draft")
    self.assertTrue(any("expected editorial status draft; found reviewed" in item for item in validate(self.root)))

def test_reviewed_snapshot_with_empty_events_is_valid(self) -> None:
    self.set_catalog_editorial_status("reviewed")
    self.set_expected_status("reviewed")
    self.assertFalse(any("lifecycle" in item for item in validate(self.root)))
```

Add drift tests for reviewed-to-approved and approved registry-event state, plus
path, identifier, and symlink failures for a generic declared reference.

- [ ] **Step 2: Run RED**

Run:

```powershell
python -m unittest tests.test_validate_profiles.ProfileValidationTests.test_generic_profile_may_have_no_external_references tests.test_validate_profiles.ProfileValidationTests.test_future_profile_is_not_forced_to_use_uk_mappings tests.test_validate_profiles.ProfileValidationTests.test_reviewed_snapshot_is_not_inferred_as_draft_from_empty_events -v
```

Expected: generic packages are incorrectly forced to use UK references and
reviewed empty-event state is incorrectly treated as Draft.

- [ ] **Step 3: Implement layered reference validation**

Use `crosswalks/catalog.json` as the generic authoritative index:

```python
UK_PILOT_PROFILE_ID = "uk--jurisdiction-profile--0.1.0"
UK_PILOT_MAPPING_REFERENCES = frozenset({
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
})


def mapping_reference_metadata(root: Path, mapping_set_id: str, registry_path: str) -> dict[str, object]:
    registry_file = safe_repository_file(root, registry_path, expected_root="crosswalks/registry")
    registry, _ = parse_front_matter(registry_file)
    catalog = load_json(root / "crosswalks" / "catalog.json")
    matches = [
        record
        for record in catalog["mapping_sets"]
        if record["metadata"]["mapping_set_id"] == mapping_set_id
    ]
    if len(matches) != 1:
        raise ValueError(f"mapping set {mapping_set_id} does not resolve exactly once")
    record = matches[0]
    return {
        "mapping_set_id": mapping_set_id,
        "editorial_status": record["metadata"]["status"],
        "snapshot_path": record["path"],
        "registry_events": registry["events"],
    }
```

Permit `external_references: []` generically. Compare `expected_status` to
catalog snapshot `metadata.status`; validate empty events for `draft` and
`reviewed`, and governed event prefixes for `approved` or later. Apply the
exact-three identifier/path/Draft rule only when `profile_id` equals the UK
pilot identifier.

- [ ] **Step 4: Run GREEN**

Run:

```powershell
python -m unittest tests.test_validate_profiles tests.test_profile_foundation.ProfileSchemaTests tests.test_profile_foundation.UKPilotProfileTests.test_external_references_are_exactly_the_three_lifecycle_pins -v
python tools/validate_profiles.py --check
python tools/validate_crosswalks.py --check
git diff --check
```

Expected: generic and pilot reference tests pass; profile and crosswalk
validators pass.

- [ ] **Step 5: Commit**

```powershell
git add tools/validate_profiles.py profiles/schema/external-references.schema.json tests/profile_fixture.py tests/test_validate_profiles.py tests/test_profile_foundation.py
git diff --cached --check
git commit -m "fix: separate profile mapping policy and lifecycle"
```

---

### Task 3: Source authority, mapping leakage, claims, and weakening

**Files:**
- Modify: `tools/validate_profiles.py`
- Modify: `profiles/schema/risk-overlays.schema.json`
- Modify: `tests/test_validate_profiles.py`
- Modify: `tests/test_profile_foundation.py`

**Interfaces:**
- Produces: `source_boundary_diagnostics(package: ProfilePackage, controls: set[str]) -> list[str]`.
- Extends: `claim_diagnostics(package: ProfilePackage) -> list[str]`.
- Preserves assertion-aware denial, quotation, metalinguistic, and coordinated-clause behavior.

- [ ] **Step 1: Add source and assertion RED tests**

Cover each family with affirmative and allowed denial/quotation cases:

```python
AFFIRMATIVE_CLAIMS = (
    "This profile satisfies Cyber Essentials requirements.",
    "This profile ensures legal compliance.",
    "This profile confers certification eligibility.",
    "This profile has NCSC approval.",
    "Cyber Essentials provision A maps to GOV-100 and supplies its external outcome.",
)

AFFIRMATIVE_WEAKENING = (
    "This profile makes optional core controls.",
    "This profile marks inapplicable core controls.",
    "GOV-100 need not be applied.",
    "This profile supersedes GOV-100.",
    "The organization is exempt from GOV-100.",
    "This profile lowers core control requirements.",
)
```

Add a source test that rejects `"UK GDPR is the authority for this profile
selection"` and a risk `source_basis` test that rejects any value not equal to
an authoritative control ID or a permitted manifest source identifier. Add
paired explicit denials, quotations, metalinguistic discussion, passive forms,
and affirmative second clauses after a denial.

- [ ] **Step 2: Run RED**

Run:

```powershell
python -m unittest tests.test_validate_profiles.ProfileValidationTests.test_common_affirmative_profile_claim_variants_are_rejected tests.test_validate_profiles.ProfileValidationTests.test_common_affirmative_control_weakening_is_rejected tests.test_validate_profiles.ProfileValidationTests.test_source_boundary_rejects_excluded_authority_claims tests.test_validate_profiles.ProfileValidationTests.test_risk_source_basis_must_resolve -v
```

Expected: the new affirmative probes pass validation incorrectly.

- [ ] **Step 3: Implement bounded source and assertion enforcement**

Validate every risk `source_basis` token against:

```python
allowed_source_basis = control_population(root) | set(manifest["source_boundary"]["permitted_sources"])
```

Reject unresolved tokens. Extend assertion-aware clause analysis to recognize
control IDs and weakening synonyms in either word order. Extend prohibited
claim families for satisfaction, compliance, certification eligibility,
certified state, and named-authority approval. Detect affirmative mapping
relationship and external-outcome import language across every string returned
by `walk_json(package.documents)`.

The implementation shall segment contrasting/coordinated clauses before
deciding whether a predicate is negated or quoted.

- [ ] **Step 4: Run GREEN**

Run:

```powershell
python -m unittest tests.test_validate_profiles -v
python tools/validate_profiles.py --check
git diff --check
```

Expected: all assertion/source tests pass with only documented symlink skips;
the current pilot remains valid.

- [ ] **Step 5: Commit**

```powershell
git add tools/validate_profiles.py profiles/schema/risk-overlays.schema.json tests/test_validate_profiles.py tests/test_profile_foundation.py
git diff --cached --check
git commit -m "fix: enforce profile source and non-claim boundaries"
```

---

### Task 4: Normative and editorial contract alignment

**Files:**
- Modify: `profiles/ESAF-1800.md`
- Modify: `docs/superpowers/specs/2026-07-24-uk-pilot-profile-design.md`
- Modify: `docs/superpowers/plans/2026-07-24-uk-pilot-profile.md`
- Modify: `profiles/README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `tools/README.md`
- Modify: `profiles/uk/0.1.0/profile.json`
- Modify: `profiles/uk/0.1.0/control-selections.json`
- Modify: `tests/test_profile_foundation.py`

**Interfaces:**
- Consumes: package-relative component behavior from Task 1.
- Consumes: editorial/lifecycle behavior from Task 2.
- Produces: one contradiction-free normative and authoring contract.

- [ ] **Step 1: Add editorial RED tests**

Add tests requiring:

```python
def test_normative_contract_defines_source_and_authority_boundaries(self) -> None:
    contract = ESAF_1800.read_text(encoding="utf-8")
    self.assertIn("## Source and authority boundaries", contract)
    self.assertIn("shall identify permitted and excluded sources", contract)
    self.assertIn("shall be original ESAF synthesis", contract)

def test_not_selected_rationales_are_non_normative(self) -> None:
    for record in self.selections:
        if record["status"] == "not_selected":
            self.assertNotRegex(record["rationale"], r"(?i)\b(shall|should|must)\b")

def test_component_path_language_is_package_relative(self) -> None:
    for path in (DESIGN, PLAN, ESAF_1800, PROFILE_README, CONTRIBUTING):
        self.assertNotIn("repository-relative component path", path.read_text(encoding="utf-8"))

def test_workflow_assertions_are_structurally_scoped(self) -> None:
    workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    self.assertIn("profiles/**", workflow["on"]["pull_request"]["paths"])
    self.assertIn("profiles/**", workflow["on"]["push"]["paths"])
    steps = workflow["jobs"]["validate"]["steps"]
    self.assertTrue(any(
        step.get("name") == "Validate profiles"
        and step.get("run") == "python tools/validate_profiles.py --check"
        for step in steps
    ))
```

Also test neutral profile-domain terminology, “shall not advance beyond Draft,”
correct referenced-artifact transition wording, and one `0.1.0` change-history
entry.

- [ ] **Step 2: Run RED**

Run:

```powershell
python -m unittest tests.test_profile_foundation -v
```

Expected: source-boundary, component terminology, rationale, lifecycle,
change-history, and structured-workflow tests fail.

- [ ] **Step 3: Align normative and companion content**

Add a concise ESAF-1800 source/authority section using `shall`. Change original
risk/overlay synthesis from `should` to `shall`. Replace component terminology
with package-relative paths and describe `$schema` separately as
document-relative. Replace contradictory transition language with:

```text
A referenced artifact lifecycle transition shall require an explicit profile
update before the new state is relied upon. The transition shall not change the
profile lifecycle automatically, and neither artifact shall be represented
beyond its independently governed recorded state.
```

Rewrite `not_selected` rationales as descriptive analysis without normative
verbs. Use profile-domain terminology, preserve `proposed`, consolidate the
pilot change history, and parse the workflow structure in the test rather than
counting strings.

- [ ] **Step 4: Run GREEN**

Run:

```powershell
python -m unittest tests.test_profile_foundation tests.test_release_metadata -v
python tools/validate_profiles.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
git diff --check
```

Expected: focused tests and publication/document validators pass.

- [ ] **Step 5: Commit**

```powershell
git add profiles/ESAF-1800.md docs/superpowers/specs/2026-07-24-uk-pilot-profile-design.md docs/superpowers/plans/2026-07-24-uk-pilot-profile.md profiles/README.md CONTRIBUTING.md tools/README.md profiles/uk/0.1.0/profile.json profiles/uk/0.1.0/control-selections.json tests/test_profile_foundation.py
git diff --cached --check
git commit -m "docs: align profile authority and lifecycle contract"
```

---

### Task 5: Correct UK applicability and traceability

**Files:**
- Modify: `profiles/uk/0.1.0/README.md`
- Modify: `profiles/uk/0.1.0/profile.json`
- Modify: `profiles/uk/0.1.0/control-selections.json`
- Modify: `profiles/uk/0.1.0/risk-overlays.json`
- Modify: `profiles/uk/0.1.0/evidence-expectations.json`
- Modify: `tests/test_profile_foundation.py`

**Interfaces:**
- Produces: `INTERNET-REACHABLE-AI-APPLICATION-INTERFACE`.
- Produces: `EXTERNAL-AI-SERVICE-INTEGRATION`.
- Refines: `MATERIAL-EXTERNAL-PROVIDER-DEPENDENCY` to a purely factual E1–E4 question.

- [ ] **Step 1: Add applicability RED tests**

Add exact truth-table counterexamples:

```python
def test_admin_console_only_does_not_activate_app_150(self) -> None:
    self.assertEqual(
        ["INTERNET-REACHABLE-AI-APPLICATION-INTERFACE"],
        self.selection("APP-150")["activation_conditions"],
    )

def test_downloaded_external_model_does_not_activate_api_140(self) -> None:
    self.assertEqual(
        ["EXTERNAL-AI-SERVICE-INTEGRATION"],
        self.selection("API-140")["activation_conditions"],
    )

def test_api_150_material_dependency_condition_is_purely_factual(self) -> None:
    question = self.condition("MATERIAL-EXTERNAL-PROVIDER-DEPENDENCY")["question"]
    self.assertIn("E1 through E4", question)
    self.assertIn("material provider or platform dependency", question)
    self.assertNotRegex(question, r"(?i)\b(must|should|addressed|replacement decision)\b")
```

Add graph tests requiring each conditional overlay/evidence record to use the
same single condition as its affected conditional controls. Add a risk-source
coverage assertion for every overlay control. Pin IAM-140 and authenticated
administration to a coherent linked risk/evidence path.

- [ ] **Step 2: Run RED**

Run:

```powershell
python -m unittest tests.test_profile_foundation.UKPilotProfileTests -v
```

Expected: the three trigger tests and graph-alignment assertions fail.

- [ ] **Step 3: Update the package as one reciprocal graph**

Create the two new boolean conditions with resolution evidence. Move APP-150
and API-140 selections to their exact conditions. Split or rename affected
overlays/evidence records when a shared record cannot express one factual
trigger. Update both sides of every risk/overlay and overlay/evidence link.

For API-150, use this factual question:

```text
Is the assessed capability classified E1 through E4 and materially dependent
on an external provider or platform?
```

Add IAM-140 to an appropriate linked risk source/affected set. Either trace
authenticated administration to IAM-110/IAM-130 and evidence or state that the
universal privileged-configuration chain supplies that requirement.

- [ ] **Step 4: Run GREEN**

Run:

```powershell
python -m unittest tests.test_profile_foundation tests.test_validate_profiles -v
python tools/validate_profiles.py --check
python tools/validate_controls.py --check
python tools/validate_crosswalks.py --check
git diff --check
```

Expected: the exact counterexamples pass; one Draft package with 91 ordered
selections validates; all affected validators pass.

- [ ] **Step 5: Commit**

```powershell
git add profiles/uk/0.1.0 tests/test_profile_foundation.py
git diff --cached --check
git commit -m "fix: align UK profile applicability and traceability"
```

---

### Task 6: Stabilize and redispatch all four whole-branch reviews

**Files:**
- Create: the four review records listed in the file map.
- Modify: any candidate file required by a new Critical or Important finding.

**Interfaces:**
- Consumes: exact merge base and exact remediated candidate SHA.
- Produces: four exact-SHA review records with finding dispositions.

- [ ] **Step 1: Run the Task 7 preflight**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_profile_foundation tests.test_validate_profiles tests.test_release_metadata -v
python tools/validate_profiles.py --check
python tools/validate_assessment.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
$base=(git merge-base main HEAD).Trim()
$candidate=(git rev-parse HEAD).Trim()
git diff --check "$base..$candidate"
git status --short
```

Expected: all focused tests pass with only documented Windows symlink skips;
all validators exit `0`; worktree is clean.

- [ ] **Step 2: Dispatch four independent exact-SHA reviews**

Use separate read-only reviewers for:

1. technical/schema/validator correctness;
2. normative/editorial consistency;
3. applicability/control selection/source boundary; and
4. overclaiming/mapping leakage/lifecycle separation.

Each reviewer shall read the complete `git diff "$base..$candidate"`, identify
Critical, Important, and Minor findings with exact evidence, and explicitly
record “no findings” when applicable.

- [ ] **Step 3: Resolve any remaining Critical or Important finding test-first**

For each accepted finding:

```powershell
python -m unittest tests.test_profile_foundation tests.test_validate_profiles -v  # RED
# Apply the smallest correction.
python -m unittest tests.test_profile_foundation tests.test_validate_profiles -v  # GREEN
git add tools/validate_profiles.py profiles tests/test_profile_foundation.py tests/test_validate_profiles.py
git diff --cached --check
git commit -m "fix: resolve UK profile review finding"
```

If the candidate changes, rerun Step 1 and all four reviews. Prior approvals do
not carry forward.

- [ ] **Step 4: Write the four review records**

Each record shall name:

- exact merge base and reviewed full SHA;
- review lens and inspected scope;
- Critical, Important, and Minor findings;
- resolution or accepted-Minor rationale;
- focused probes and validator evidence; and
- final verdict.

- [ ] **Step 5: Commit review records**

```powershell
git add docs/superpowers/reviews
git diff --cached --check
git commit -m "docs: record UK pilot profile reviews"
```

The review-record commit changes the head. Task 8 shall obtain fresh external
confirmations on the pushed final SHA without modifying the branch.

---

### Task 7: Exact-candidate publication handoff

**Files:**
- Modify externally: Draft pull-request description and issue `#57` evidence.

**Interfaces:**
- Consumes: final reviewed branch including review records.
- Produces: pushed Draft PR and GitHub validation evidence.

- [ ] **Step 1: Run the complete Task 8 gate**

Run:

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
$base=(git merge-base main HEAD).Trim()
git diff --check "$base..HEAD"
git status --porcelain
rg --files -g '**/__pycache__/**'
```

Expected: no failures, only documented Windows symlink skips, every validator
passes, no diff errors, clean status, and no caches.

- [ ] **Step 2: Push and create the Draft PR**

Push `agent/uk-pilot-profile`. The PR body shall include `Closes #57`, exact
head and merge-base SHAs, derived selection counts, exact gate results, four
review dispositions, Draft status, and every non-claim boundary.

- [ ] **Step 3: Require GitHub checks and final exact-head confirmations**

Confirm the remote PR head equals the locally gated SHA, `Validate ESAF
sources` passes, and mergeability is clean. Dispatch the same four independent
review lenses on that pushed SHA including the committed review records. Record
confirmations externally without modifying the branch.

- [ ] **Step 4: Stop at the merge authorization gate**

Do not merge until the repository owner explicitly authorizes completion after
reviewing the Draft PR and exact-head evidence.
