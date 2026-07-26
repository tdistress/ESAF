# PCI DSS source readiness implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record and enforce an evidenced `HOLD` on public PCI DSS v4.0.1
mapping until ESAF has authorized source bytes, a verified complete provision
inventory, written publication permission, and qualified independent reviewers.

**Architecture:** Reuse ESAF's existing source-oracle, feasibility-matrix,
deterministic-renderer, review, and traceability pattern under
`docs/superpowers/`. Keep the decision outside the ESAF-1600 mapping and
registry trees so HOLD cannot appear in generated catalogs or imply that any
PCI DSS provision was assessed.

**Tech stack:** Markdown, canonical JSON, Python 3.13, `unittest`, SHA-256,
GitHub Actions, and Git.

## Global constraints

- Disposition is mechanically derived as `HOLD`; do not create a GO artifact.
- Do not accept the PCI SSC protected-document license agreement.
- Do not download or commit the protected PCI DSS PDF.
- Do not reproduce PCI DSS requirement text, titles, close paraphrases, or a
  provision inventory.
- Create no PCI DSS mapping, registry, or generated catalog record.
- Treat the discovery-catalog digest as mutable public metadata, never as the
  standard's digest.
- Scope only `esaf_to_external`; exclude `external_to_esaf`.
- Proposed scope is complete publication at the finest authorized publishable
  numbered requirement or sub-requirement identifier.
- Use test-driven development for every enforceable invariant.
- Set `PYTHONDONTWRITEBYTECODE=1`; do not commit caches or downloaded artifacts.
- After any candidate change, rerun both independent exact-SHA reviews.

---

### Task 1: Commit the fail-closed publication-rights boundary

**Files:**

- Create:
  `docs/superpowers/reviews/2026-07-25-pci-dss-publication-rights-review.md`
- Create: `tests/test_pci_dss_source_readiness.py`

- [ ] **Step 1: Add RED rights-contract tests**

Require the rights review to contain:

- named reviewer, review date, reviewed public source URLs, and exact review
  disposition;
- reviewer independence from any future mapper;
- authorized access to the reviewed public rights sources and a
  publication-basis-reviewed attestation;
- an exhaustive, disjoint partition of identifiers, titles,
  structural_inventory, paraphrases, derivative_mapping_analysis, and
  official_links;
- only `official_links` permitted and all other classes prohibited;
- case-specific Materials License Agreement trigger; and
- the non-legal-advice and no-statutory-exception-decision boundaries.

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_pci_dss_source_readiness -v
```

Expected: RED because the review does not exist.

- [ ] **Step 2: Write the rights review using official PCI SSC evidence**

Use only:

- `https://www.pcisecuritystandards.org/terms_and_conditions/`;
- `https://www.pcisecuritystandards.org/about_us/policies/`;
- the protected document's official access interstitial; and
- `https://programs.pcissc.org/mla_registration.aspx`.

Record HOLD as a fail-closed absence-of-permission decision. Do not conclude
that statutory exceptions are unavailable.

- [ ] **Step 3: Validate and commit rights before derivative evidence**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_pci_dss_source_readiness -v
git diff --check
git add docs/superpowers/reviews/2026-07-25-pci-dss-publication-rights-review.md `
  tests/test_pci_dss_source_readiness.py
git commit -m "docs: review PCI DSS publication rights"
```

Record this commit SHA for the oracle and matrix ancestry tests.

---

### Task 2: Pin the public source-readiness oracle

**Files:**

- Create:
  `docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json`
- Modify: `tests/test_pci_dss_source_readiness.py`

**Official source interfaces:**

- Document Library:
  `https://www.pcisecuritystandards.org/document_library/`
- Public discovery catalog:
  `https://docs-pub.pcisecuritystandards.org/doc_library.json`
- Protected English document URL:
  `https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf`
- Publication announcement:
  `https://blog.pcisecuritystandards.org/just-published-pci-dss-v4-0-1`

- [ ] **Step 1: Independently retrieve and hash public discovery metadata**

Retrieve `doc_library.json` without accepting the protected license. Record UTC
retrieval time, final URL, byte length, and lowercase SHA-256. Select only:

- document reference `pci_dss`;
- version `v4.0.1`;
- catalog `last_updated`;
- `archived: false`;
- `protected: yes`; and
- canonical English protected-document URL.

Do not commit the mutable one-megabyte catalog.

- [ ] **Step 2: Add RED closed-oracle tests**

Require exact nested key sets and values for:

- publisher, publication, version, language, and format;
- discovery and access URLs;
- retrieval timestamp, byte length, and digest;
- selected discovery values;
- source artifact state and null digest/count fields;
- artifact publication date `2024-06` with `month` precision, separately from
  announcement date `2024-06-11`, catalog update time, predecessor retirement,
  and future-dated requirement effective date;
- normative/supporting boundary;
- protected access behavior; and
- inventory, mapping, compliance, and checksum nonclaims.

- [ ] **Step 3: Create canonical oracle JSON**

Write one-line, UTF-8/LF, key-sorted canonical JSON. Store the rights review
path and rights-review commit SHA. Keep source byte length, source SHA-256, page
count, provision count, and inventory digest null.

- [ ] **Step 4: Make source tests GREEN and commit**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_pci_dss_source_readiness -v
git diff --check
git add docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json `
  tests/test_pci_dss_source_readiness.py
git commit -m "docs: pin PCI DSS public source readiness"
```

---

### Task 3: Implement the mechanical GO/HOLD decision

**Files:**

- Create:
  `docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json`
- Create: `tools/render_pci_dss_mapping_go_no_go.py`
- Create: `tests/test_render_pci_dss_mapping_go_no_go.py`
- Modify: `tests/test_pci_dss_source_readiness.py`

- [ ] **Step 1: Add RED matrix and renderer tests**

Require exact gate order:

```text
source_identity_and_drift
authorized_source_artifact
publication_rights
provision_inventory
semantic_and_normative_feasibility
esaf_1600_and_schema_fit
mapper_and_reviewer_readiness
overclaiming_controls
```

Test that:

- statuses are only `PASS` or `BLOCKED`;
- each gate has rationale and evidence references;
- each blocked gate has complete, uniquely identified blockers;
- GO requires all PASS, zero blockers, positive feasibility, and no open
  Critical/Important findings;
- HOLD requires at least one BLOCKED gate and blocker coverage;
- the matrix binds the exact directional question, complete-publication scope,
  finest authorized publishable requirement/sub-requirement granularity, and
  excluded reverse direction;
- renderer output is deterministic and derives rather than trusts decision;
- `--write` and `--check` work and operational errors exit `2`; and
- malformed decisions, stale digests, unknown keys, duplicate blocker IDs, and
  incomplete evidence fail closed.

- [ ] **Step 2: Create the closed readiness matrix**

Use expected statuses:

- PASS: source identity/drift, ESAF-1600/schema fit, overclaiming controls.
- BLOCKED: authorized source artifact, publication rights, provision inventory,
  semantic/normative feasibility, mapper/reviewer readiness.

Every blocker shall name `ESAF Project Maintainer` or a more specific owner and
record missing evidence, reconsideration trigger, and deterministic re-entry
test.

The reviewer contract shall require:

- named authorized mapper;
- independent current QSA or owner-approved equivalent PCI reviewer;
- independent ESAF specification/mapping reviewer;
- independent rights reviewer;
- independent security/overclaiming reviewer;
- exact candidate SHA and artifact digests;
- attributable attestation and findings disposition; and
- separate inventory/specification and security/overclaiming reviews, with
  redispatch after any candidate change.

- [ ] **Step 3: Implement deterministic renderer**

Expose:

```python
def validate_matrix(matrix: dict[str, object]) -> None: ...
def derive_decision(matrix: dict[str, object]) -> str: ...
def render(matrix: dict[str, object]) -> str: ...
```

The Markdown review shall show decision, exact question, source boundary, gate
table, blocker table, reviewer requirements, excluded direction,
reconsideration sequence, and nonclaims.

- [ ] **Step 4: Generate the review and make tests GREEN**

The output path is:

`docs/superpowers/reviews/2026-07-25-pci-dss-mapping-go-no-go-review.md`

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_pci_dss_source_readiness -v
python -m unittest tests.test_render_pci_dss_mapping_go_no_go -v
python tools/render_pci_dss_mapping_go_no_go.py --write
python tools/render_pci_dss_mapping_go_no_go.py --check
```

- [ ] **Step 5: Commit matrix, renderer, tests, and generated review**

```powershell
git add docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json `
  tools/render_pci_dss_mapping_go_no_go.py `
  tests/test_pci_dss_source_readiness.py `
  tests/test_render_pci_dss_mapping_go_no_go.py `
  docs/superpowers/reviews/2026-07-25-pci-dss-mapping-go-no-go-review.md
git commit -m "feat: derive PCI DSS readiness hold"
```

---

### Task 4: Publish traceability and project status

**Files:**

- Create:
  `docs/superpowers/reviews/2026-07-25-pci-dss-mapping-go-no-go-traceability.md`
- Modify: `crosswalks/pci-dss.md`
- Modify: `project/BACKLOG.md`
- Modify: `tools/README.md`
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tests/test_pci_dss_source_readiness.py`

- [ ] **Step 1: Add RED traceability and presentation tests**

Require:

- traceability from every issue #58 acceptance item to exact evidence;
- the oracle, rights review, matrix, generated review, tests, and review protocol
  linked from `crosswalks/pci-dss.md`;
- status exactly `Readiness HOLD`;
- active backlog no longer lists PCI readiness as incomplete and a completed
  workstream records issue 58 as closed through evidenced HOLD;
- CI path filters cover all PCI readiness inputs; and
- CI runs both focused test modules and renderer `--check`.

- [ ] **Step 2: Add traceability and presentation**

State blocker owners and triggers, zero mapping artifacts, unchanged crosswalk
catalog counts, exact nonclaims, and the GO closure rule: a future readiness GO
does not close issue 58 until the approved Draft mapping scope is completed
under ESAF-1600.

- [ ] **Step 3: Wire and document CI validation**

Add the oracle, matrix, review, renderer, tests, PCI landing page, and backlog
paths to pull-request and push filters. Add renderer `--check` after ordinary
crosswalk validation. Document the command in `tools/README.md`.

- [ ] **Step 4: Validate and commit**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_pci_dss_source_readiness -v
python -m unittest tests.test_render_pci_dss_mapping_go_no_go -v
python tools/render_pci_dss_mapping_go_no_go.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
git diff --check
git add docs/superpowers/reviews/2026-07-25-pci-dss-mapping-go-no-go-traceability.md `
  crosswalks/pci-dss.md project/BACKLOG.md tools/README.md `
  .github/workflows/catalog-validation.yml tests/test_pci_dss_source_readiness.py
git commit -m "docs: publish PCI DSS readiness hold"
```

---

### Task 5: Independently review the exact candidate

**Files:**

- Create:
  `docs/superpowers/reviews/2026-07-25-pci-dss-exact-sha-source-inventory-review.md`
- Create:
  `docs/superpowers/reviews/2026-07-25-pci-dss-exact-sha-rights-overclaiming-review.md`
- Modify other files only to resolve findings test-first.

- [ ] **Step 1: Freeze clean candidate SHA and full diff**

```powershell
git status --short
git rev-parse HEAD
git diff --check origin/main..HEAD
```

- [ ] **Step 2: Dispatch independent source/inventory review**

Verify current version, URLs, public discovery digest, date precision, protected
access behavior, absent PDF checksum, absent provision inventory, blocker
coverage, and zero PCI mapping/registry/catalog artifacts.

- [ ] **Step 3: Dispatch independent rights/overclaiming review**

Verify public terms/IPR/permission path, six-field rights partition,
independence/access attestations, reviewer contract, prohibited claims, and no
implied PCI SSC authorization, compliance, equivalence, coverage, or
certification.

- [ ] **Step 4: Resolve Critical and Important findings**

Add focused regression tests before practical fixes. After any candidate
change, commit, record the new SHA, and redispatch both reviews.

- [ ] **Step 5: Commit exact-SHA review records**

Record reviewed SHA, commands/evidence, findings, and disposition. The review
commit may add only review records; any substantive candidate change requires a
new reviewed SHA.

---

### Task 6: Run publication gates, publish, merge, and clean up

- [ ] **Step 1: Run focused and full validation**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_pci_dss_source_readiness -v
python -m unittest tests.test_render_pci_dss_mapping_go_no_go -v
python -m unittest discover -s tests -v
python tools/render_pci_dss_mapping_go_no_go.py --check
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

- [ ] **Step 2: Review the complete branch diff**

Confirm no PCI source content, inventory, mapping, registry record, generated
catalog change, cache, or build output exists.

- [ ] **Step 3: Push and open a ready PR**

Include decision, blockers/re-entry tests, source and rights evidence, unchanged
catalog counts, exact reviewed head SHA, validation results, and `Closes #58`.

- [ ] **Step 4: Verify and merge**

Require passing GitHub checks, clean merge state, and PR head equality with the
reviewed SHA before merge.

- [ ] **Step 5: Validate and clean main**

Update local `main`, rerun proportional validation, verify a clean worktree,
and remove this temporary branch/worktree without disturbing unrelated
historical worktree metadata.
