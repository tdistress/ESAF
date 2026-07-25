# ESAF Licensing Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish ESAF standards content under CC BY 4.0 and implementation assets under Apache 2.0 with unambiguous path rules, attribution, third-party notices, trademark boundaries, and contribution terms.

**Architecture:** The unmodified CC BY 4.0 legal code remains at the repository root for GitHub detection. An exact Apache 2.0 text and a separate scope document apply Apache 2.0 to the named implementation paths; original ESAF material defaults to CC BY 4.0 everywhere else. Focused tests pin both official texts and the repository-facing license contract without changing normative or generated artifacts.

**Tech Stack:** Markdown, plain-text license files, Python `unittest`, SHA-256, and Git.

## Global Constraints

- Name `ESAF Project Maintainers` as the copyright holder.
- Do not name Hearst as a copyright holder, owner, sponsor, or endorser.
- Use the unmodified official English CC BY 4.0 legal code from `https://creativecommons.org/licenses/by/4.0/legalcode.txt`.
- Use the unmodified official Apache 2.0 text from `https://www.apache.org/licenses/LICENSE-2.0.txt`.
- Apply Apache 2.0 to `.github/`, `tools/`, `tests/`, `requirements-dev.txt`, `assessment/schema/`, `controls/schema/`, and `crosswalks/schema/`.
- Apply CC BY 4.0 to original ESAF material in every other path.
- A more specific path rule overrides a broader rule.
- Do not relicense third-party material.
- Do not create a certification scheme, registered-mark claim, copyright assignment, or new patent policy.
- Do not modify normative requirements, controls, mappings, schemas, generated catalogs, or mapping digests.

---

### Task 1: Add the executable licensing contract

**Files:**
- Create: `tests/test_license_metadata.py`
- Modify: `.gitattributes`
- Replace: `LICENSE`
- Create: `LICENSES/Apache-2.0.txt`
- Create: `LICENSE_SCOPE.md`
- Create: `NOTICE`
- Create: `THIRD_PARTY_NOTICES.md`
- Create: `TRADEMARKS.md`

**Interfaces:**
- Consumes: Official CC BY 4.0 and Apache 2.0 license texts and existing NCSC rights statements.
- Produces: A path-based license contract and a focused repository invariant test.

- [ ] **Step 1: Add the failing license metadata test**

Create `tests/test_license_metadata.py`:

```python
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CC_BY_4_SHA256 = (
    "9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411"
)
APACHE_2_SHA256 = (
    "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
)

APACHE_PATHS = (
    ".github/",
    "tools/",
    "tests/",
    "requirements-dev.txt",
    "assessment/schema/",
    "controls/schema/",
    "crosswalks/schema/",
)


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def normalized_sha256(relative_path: str) -> str:
    data = (ROOT / relative_path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


class LicenseMetadataTests(unittest.TestCase):
    def test_official_license_texts_are_complete_and_unmodified(self) -> None:
        self.assertEqual(CC_BY_4_SHA256, normalized_sha256("LICENSE"))
        self.assertEqual(
            APACHE_2_SHA256,
            normalized_sha256("LICENSES/Apache-2.0.txt"),
        )

    def test_scope_routes_implementation_assets_to_apache(self) -> None:
        scope = read_text("LICENSE_SCOPE.md")
        for path in APACHE_PATHS:
            with self.subTest(path=path):
                self.assertIn(f"`{path}`", scope)
        self.assertIn("Apache-2.0", scope)
        self.assertIn("CC-BY-4.0", scope)
        self.assertIn("A more specific path rule overrides a broader rule.", scope)
        self.assertIn(
            "Original ESAF material in every other path is licensed under "
            "CC BY 4.0.",
            scope,
        )
        self.assertIn("does not relicense third-party material", scope)

    def test_notice_has_exact_holder_and_nonendorsement_boundary(self) -> None:
        notice = read_text("NOTICE")
        self.assertIn("Copyright 2026 ESAF Project Maintainers", notice)
        self.assertIn("Enterprise Secure AI Framework (ESAF)", notice)
        self.assertIn("licensed under CC BY 4.0", notice)
        self.assertIn("does not imply endorsement", notice)
        self.assertNotIn("Hearst", notice)

    def test_third_party_notice_preserves_ncsc_terms(self) -> None:
        notice = read_text("THIRD_PARTY_NOTICES.md")
        self.assertIn("National Cyber Security Centre", notice)
        self.assertIn("Open Government Licence v3.0", notice)
        self.assertIn(
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            notice,
        )
        self.assertIn("do not relicense", notice)
        self.assertIn("mapping-level rights statements", notice)

    def test_trademark_policy_does_not_create_certification_or_registration(self) -> None:
        policy = read_text("TRADEMARKS.md")
        self.assertIn("truthful references", policy)
        self.assertIn("modified works", policy)
        self.assertIn("official ESAF publication", policy)
        self.assertIn("does not create a certification program", policy)
        self.assertIn("does not claim that any ESAF mark is registered", policy)
        for prohibited_claim in ("sponsored by", "endorsed by", "certified by"):
            with self.subTest(prohibited_claim=prohibited_claim):
                self.assertIn(prohibited_claim, policy)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and confirm the red state**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_license_metadata -v
```

Expected: failures for the placeholder root license and missing license-contract files.

- [ ] **Step 3: Import and pin the official license texts**

Run:

```powershell
$ccSource = Join-Path $env:TEMP 'esaf-cc-by-4.0-legalcode.txt'
$apacheSource = Join-Path $env:TEMP 'esaf-apache-2.0.txt'
Invoke-WebRequest -Uri 'https://creativecommons.org/licenses/by/4.0/legalcode.txt' -OutFile $ccSource
Invoke-WebRequest -Uri 'https://www.apache.org/licenses/LICENSE-2.0.txt' -OutFile $apacheSource
New-Item -ItemType Directory -Force LICENSES | Out-Null
Copy-Item -LiteralPath $ccSource -Destination LICENSE -Force
Copy-Item -LiteralPath $apacheSource -Destination LICENSES/Apache-2.0.txt -Force
```

Add these rules to `.gitattributes`:

```gitattributes
LICENSE text eol=lf
LICENSES/*.txt text eol=lf
```

Run:

```powershell
python -m unittest tests.test_license_metadata.LicenseMetadataTests.test_official_license_texts_are_complete_and_unmodified -v
```

Expected: PASS.

- [ ] **Step 4: Add the scope, notice, third-party, and trademark documents**

Create `LICENSE_SCOPE.md` with:

```markdown
# License scope

ESAF uses separate licenses for standards content and implementation assets.

## Apache License 2.0

The following paths are licensed under the Apache License, Version 2.0 (`Apache-2.0`):

- `.github/`
- `tools/`
- `tests/`
- `requirements-dev.txt`
- `assessment/schema/`
- `controls/schema/`
- `crosswalks/schema/`

The complete license text is in [LICENSES/Apache-2.0.txt](LICENSES/Apache-2.0.txt).

## Creative Commons Attribution 4.0

Original ESAF material in every other path is licensed under CC BY 4.0. The complete license text is in [LICENSE](LICENSE), and the canonical license page is <https://creativecommons.org/licenses/by/4.0/>.

A more specific path rule overrides a broader rule.

## Exclusions

This license allocation applies only to rights held by the ESAF Project Maintainers or submitted with authority to license. It does not relicense third-party material. Separately marked material remains under its stated terms. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

License texts are provided under their own terms and are not relicensed by this scope document.
```

Create `NOTICE` with:

```text
Enterprise Secure AI Framework (ESAF)
Copyright 2026 ESAF Project Maintainers

Standards content is licensed under the Creative Commons Attribution 4.0
International license. Software and implementation assets identified in
LICENSE_SCOPE.md are licensed under the Apache License, Version 2.0.

Preferred attribution for standards content:

Enterprise Secure AI Framework (ESAF), copyright 2026 ESAF Project
Maintainers, licensed under CC BY 4.0. Changes were made where applicable.
Use does not imply endorsement by the ESAF Project Maintainers.

This preferred wording is guidance and does not add to or modify either
license.
```

Create `THIRD_PARTY_NOTICES.md` with:

```markdown
# Third-party notices

The ESAF licenses apply only to original ESAF material and other material that the ESAF Project Maintainers have authority to license. They do not relicense third-party material.

## UK National Cyber Security Centre

Identified National Cyber Security Centre material is Crown copyright and is reused under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

Existing mapping-level rights statements define the exact source, version, permitted elements, prohibited elements, attribution, and publication basis for each affected mapping set. Those statements remain controlling for the third-party material they identify.

NCSC and government logos, third-party material, and excluded source text are not covered by the ESAF licenses. Reuse does not imply NCSC endorsement, certification, or official status.
```

Create `TRADEMARKS.md` with:

```markdown
# ESAF name and marks

The copyright licenses do not grant trademark rights or permission to imply project approval.

Truthful references to ESAF and unmodified ESAF publications are permitted. For example, a product or document may state that it implements, references, or is based on a specified ESAF publication and version when that statement is accurate.

Modified works shall identify their changes and shall not present themselves as an official ESAF publication. Without written authorization, a person or organization shall not claim that a work, product, service, assessment, or organization is:

- sponsored by the ESAF Project Maintainers;
- endorsed by the ESAF Project Maintainers;
- certified by the ESAF Project Maintainers;
- an official ESAF publication; or
- ESAF conformant.

This policy does not create a certification program and does not claim that any ESAF mark is registered.
```

- [ ] **Step 5: Run the focused contract test**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_license_metadata -v
```

Expected: all tests in `tests.test_license_metadata` pass.

- [ ] **Step 6: Commit the executable licensing contract**

Run:

```powershell
git add .gitattributes LICENSE LICENSES/Apache-2.0.txt LICENSE_SCOPE.md NOTICE THIRD_PARTY_NOTICES.md TRADEMARKS.md tests/test_license_metadata.py
git commit -m "legal: establish ESAF dual-license scope"
```

Expected: one commit containing only the license contract, official texts, and focused tests.

### Task 2: Publish the licensing model to contributors and readers

**Files:**
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tests/test_esaf_1600_foundation.py`
- Modify: `tests/test_license_metadata.py`

**Interfaces:**
- Consumes: `LICENSE_SCOPE.md`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, and `TRADEMARKS.md`.
- Produces: Reader-facing and contributor-facing licensing instructions enforced by the focused test.

- [ ] **Step 1: Extend the focused test for README and contribution terms**

Add these methods to `LicenseMetadataTests`:

```python
    def test_readme_publishes_the_dual_license_model(self) -> None:
        readme = read_text("README.md")
        self.assertNotIn("Licensing is not yet finalized", readme)
        self.assertIn("CC BY 4.0", readme)
        self.assertIn("Apache License 2.0", readme)
        for target in (
            "LICENSE",
            "LICENSE_SCOPE.md",
            "NOTICE",
            "THIRD_PARTY_NOTICES.md",
            "TRADEMARKS.md",
        ):
            with self.subTest(target=target):
                self.assertIn(f"]({target})", readme)

    def test_contributions_follow_target_path_license_and_require_authority(self) -> None:
        contributing = read_text("CONTRIBUTING.md")
        self.assertIn("license applicable to the target path", contributing)
        self.assertIn("authority to submit the contribution", contributing)
        self.assertIn("does not transfer copyright ownership", contributing)
        self.assertIn("Not a Contribution", contributing)
        self.assertIn("third-party material", contributing)
        self.assertIn("LICENSE_SCOPE.md", contributing)
```

- [ ] **Step 2: Run the new tests and confirm the red state**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_license_metadata.LicenseMetadataTests.test_readme_publishes_the_dual_license_model `
  tests.test_license_metadata.LicenseMetadataTests.test_contributions_follow_target_path_license_and_require_authority `
  -v
```

Expected: both tests fail because README still says licensing is not finalized and CONTRIBUTING lacks target-path contribution terms.

- [ ] **Step 3: Replace the README license section**

Replace the existing `## License` section with:

```markdown
## License

Original ESAF standards content is licensed under [Creative Commons Attribution 4.0 International](LICENSE). Software and implementation assets identified in [LICENSE_SCOPE.md](LICENSE_SCOPE.md) are licensed under the [Apache License 2.0](LICENSES/Apache-2.0.txt).

See the [copyright and attribution notice](NOTICE), [third-party notices](THIRD_PARTY_NOTICES.md), and [ESAF name and marks policy](TRADEMARKS.md). Separately identified third-party material remains under its stated terms.
```

- [ ] **Step 4: Add contribution licensing terms**

Add this section after `## Contribution Principles` in `CONTRIBUTING.md`:

```markdown
## Contribution licensing

Unless the contributor and the ESAF Project Maintainers agree otherwise in writing, each contribution is submitted under the license applicable to the target path in [LICENSE_SCOPE.md](LICENSE_SCOPE.md). A contribution to an Apache-licensed path is submitted under Apache 2.0. A contribution to a CC BY 4.0 path is submitted under CC BY 4.0.

By submitting a contribution, the contributor confirms that they have authority to submit the contribution under the applicable license. This submission does not transfer copyright ownership.

Material conspicuously marked `Not a Contribution` is excluded from submission under these terms. Third-party material shall be identified and shall not be submitted unless its terms permit inclusion and the project accepts it through the applicable rights-review process.
```

- [ ] **Step 5: Extend the repository-validation path filters**

Add these entries after `"CHANGELOG.md"` in both
`.github/workflows/catalog-validation.yml` path lists:

```yaml
      - "CONTRIBUTING.md"
      - "LICENSE"
      - "LICENSES/**"
      - "LICENSE_SCOPE.md"
      - "NOTICE"
      - "README.md"
      - "THIRD_PARTY_NOTICES.md"
      - "TRADEMARKS.md"
```

Add the same entries after `"CHANGELOG.md"` in the `expected_paths` list in
`tests/test_esaf_1600_foundation.py`:

```python
            "CONTRIBUTING.md",
            "LICENSE",
            "LICENSES/**",
            "LICENSE_SCOPE.md",
            "NOTICE",
            "README.md",
            "THIRD_PARTY_NOTICES.md",
            "TRADEMARKS.md",
```

- [ ] **Step 6: Run the complete focused tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_license_metadata -v
python -m unittest `
  tests.test_esaf_1600_foundation.Esaf1600FoundationTests.test_ci_fetches_history_and_runs_crosswalk_validation `
  -v
```

Expected: all licensing metadata tests and the CI path-filter contract test pass.

- [ ] **Step 7: Commit the reader, contributor, and CI documentation**

Run:

```powershell
git add README.md CONTRIBUTING.md .github/workflows/catalog-validation.yml tests/test_esaf_1600_foundation.py tests/test_license_metadata.py
git commit -m "docs: publish ESAF licensing and contribution terms"
```

Expected: one commit containing the README, contribution terms, CI path filters, and their tests.

### Task 3: Validate the complete licensing branch

**Files:**
- Verify only: all files changed from the merge base through `HEAD`

**Interfaces:**
- Consumes: The two implementation commits and the approved design.
- Produces: Evidence that license texts, path rules, documentation, and repository invariants are complete and clean.

- [ ] **Step 1: Verify exact branch scope and official text hashes**

Run:

```powershell
$mergeBase = git merge-base main HEAD
git diff --name-only "$mergeBase..HEAD"
git diff --check "$mergeBase..HEAD"
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_license_metadata -v
```

Expected: only the design, plan, license contract, focused tests, CI path filters, README, and CONTRIBUTING files changed; no whitespace errors; all focused tests pass.

- [ ] **Step 2: Verify authoritative artifacts are unchanged**

Run:

```powershell
$mergeBase = git merge-base main HEAD
$protected = git diff --name-only "$mergeBase..HEAD" -- framework controls architectures assessment crosswalks governance implementation data-model profiles templates examples diagrams
if ($protected) { throw "Unexpected authoritative artifact changes: $protected" }
Write-Output 'Authoritative and generated artifacts are unchanged.'
```

Expected: `Authoritative and generated artifacts are unchanged.`

- [ ] **Step 3: Run the full repository test suite**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -v
```

Expected: all tests pass, with only documented Windows symlink skips.

- [ ] **Step 4: Verify the worktree is clean and cache-free**

Run:

```powershell
git status --short
$cacheDirs = Get-ChildItem -Directory -Recurse -Filter __pycache__ -ErrorAction SilentlyContinue
if ($cacheDirs) { $cacheDirs.FullName; throw '__pycache__ directories found' }
```

Expected: no output from `git status --short` and no cache directories.
