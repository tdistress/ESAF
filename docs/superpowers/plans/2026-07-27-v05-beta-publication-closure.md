# v0.5-beta publication closure implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish `v0.5-beta` as a validated Working Draft on one exact candidate while keeping all three UK mapping sets Draft and issue 55 open under the deferred owner-risk path.

**Architecture:** Keep the published v0.4 validator frozen. Add a v0.5-specific release controller and authenticated live GitHub evidence collector, land those capabilities in an evidence PR, then create a separate metadata-only closure candidate. Bind reviews and human decisions to that exact head, require tree equality after merge, validate merged `main`, create the annotated tag, and record durable publication evidence.

**Tech stack:** Python 3 standard library, PyYAML, `unittest`, Git, GitHub CLI, PowerShell, Mermaid CLI 11.16.0, Markdown and YAML front matter.

## Global constraints

- The binding design is `docs/superpowers/specs/2026-07-27-v05-beta-publication-closure-design.md`.
- The published `v0.4-alpha` validator, record, tag object, peeled commit, and issue 39 evidence shall remain valid and unchanged.
- `v0.5-beta` is a Working Draft publication. It shall not advance any control, architecture, profile, mapping set, or mapping record lifecycle state.
- All three UK mapping sets and all 404 records shall remain `draft`; reviewer metadata, review events, and lifecycle events shall remain unchanged under owner-risk acceptance.
- Use exactly one mapping basis across all three mapping sets: `qualified_approval` or `owner_risk_acceptance`.
- The deferred path shall enumerate exactly six missing human roles, retain issue 55, and preserve every required nonclaim and re-entry trigger.
- Standing repository authorization is not an exact-candidate owner-risk decision, scope approval, or Steering Committee approval.
- The owner-risk decision and scope approval shall be explicit and bound to the closure head. Governance approval shall be separate.
- Candidate, merged-main, and tag SHA domains shall remain distinct. The reviewed closure tree and merged tree shall be identical.
- Live evidence shall be fetched by the production collector through authenticated `gh api`; operational commands shall not accept caller-derived verdict, identity, check, merge, or tag objects.
- Live acquisition manifests expire after 15 minutes. Stale manifests shall be discarded and fetched again.
- Every Mermaid block shall be rendered with Mermaid CLI 11.16.0 and visually reviewed on the exact candidate.
- Set `PYTHONDONTWRITEBYTECODE=1` for every Python validation command and leave no `__pycache__` directories.
- Resolve all Critical and Important findings before merge or publication.
- Do not close issue 55.
- Do not create or push `v0.5-beta` until exact-head decisions, reviews, CI, clean merge state, post-merge validation, and taggable evidence all pass.
- The canonical SDD workspace for all nine tasks is the directory created from
  this plan in the evidence worktree. Record closure-worktree commits and
  reports in that ledger; do not initialize a second SDD workspace.
- Do not delete the canonical SDD workspace during a task. The
  subagent-driven-development workflow deletes it only after Task 9 completion
  and the final whole-plan review.

---

### Task 1: Add the v0.5 release-record contract

**Files:**
- Create: `tools/v05_beta_release_gates.py`
- Create: `tests/test_v05_beta_release_gates.py`
- Reference: `tools/release_gates.py`
- Reference: `tests/test_release_gates.py`

**Interfaces:**
- Consumes: tracked repository content and the v0.5 readiness Markdown front matter.
- Produces: `load_front_matter(path)`, `derive_scope(root)`, `validate_record(root, record)`, `validate_transition(previous, candidate)`, and CLI `python tools/v05_beta_release_gates.py --check [--baseline-ref REF]`.

- [ ] **Step 1: Write fail-first record and phase tests**

Build one `record_fixture(phase)` helper that returns the exact identity,
mapping set, scope count, publication, and gate fields specified below. Add
concrete assertions in this form:

```python
from tools.release_gates import (
    load_front_matter as load_v04_front_matter,
    validate_record as validate_v04_record,
)

class V05ReleaseRecordTests(unittest.TestCase):
    def test_v04_published_validator_remains_green(self) -> None:
        historical = load_v04_front_matter(V04_RECORD)
        self.assertEqual([], validate_v04_record(ROOT, historical))

    def test_v05_record_requires_fixed_release_identity(self) -> None:
        record = record_fixture("evidence_candidate")
        for field, value, diagnostic in (
            ("release", "0.4-alpha", "release shall equal 0.5-beta"),
            ("tag", "v0.4-alpha", "tag shall equal v0.5-beta"),
            ("issue", 39, "issue shall equal 59"),
        ):
            with self.subTest(field=field):
                candidate = deepcopy(record)
                candidate[field] = value
                self.assertIn(diagnostic, validate_record(ROOT, candidate))

    def test_phase_gate_state_matrix_is_exact(self) -> None:
        for phase, expected in PHASE_GATE_STATES.items():
            with self.subTest(phase=phase):
                record = record_fixture(phase)
                observed = {
                    gate: value["state"]
                    for gate, value in record["gates"].items()
                }
                self.assertEqual(expected, observed)
                self.assertEqual([], validate_record(ROOT, record))

    def test_scope_counts_are_derived_from_repository(self) -> None:
        self.assertEqual(EXPECTED_SCOPE, derive_scope(ROOT))

    def test_transition_rejects_published_to_candidate(self) -> None:
        previous = record_fixture("published")
        candidate = record_fixture("closure_candidate")
        self.assertIn(
            "published record shall not transition to a candidate phase",
            validate_transition(previous, candidate),
        )
```

Add table-driven mutations for every wrong phase state, missing or duplicate
mapping set, unsupported basis, stale scope count, missing assessment
foundation, wrong profile count, non-`HOLD` PCI disposition, and untracked
scope input. Each mutation shall assert one exact diagnostic.

For the CLI baseline test, create a temporary Git repository containing the
required tracked inputs and a closure-candidate record, run the tool without
`--baseline-ref`, and assert exit code 1 plus
`baseline-ref is required for closure candidate`.

Use these exact release constants:

```python
RELEASE = "0.5-beta"
TAG = "v0.5-beta"
ISSUE = 59
RECORD_RELATIVE = (
    "docs/superpowers/reviews/"
    "2026-07-27-v05-beta-publication-readiness.md"
)
REPOSITORY_SCOPE = "complete_git_tracked_repository"
PUBLICATION_CONDITION = "remote_annotated_tag_matches_exact_validated_commit"
MAPPING_DECISION_BASES = {"qualified_approval", "owner_risk_acceptance"}
```

The exact gate tuple is:

```python
GATE_IDS = (
    "scope",
    "technical",
    "editorial",
    "terminology",
    "cross_reference_rendering",
    "standards_mapping",
    "profile_scope",
    "release_metadata",
    "governance",
    "post_merge",
)
```

- [ ] **Step 2: Run the focused tests and verify fail-first behavior**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_v05_beta_release_gates -v
```

Expected: import failure for `tools.v05_beta_release_gates`. The frozen v0.4 test remains green when run separately.

- [ ] **Step 3: Implement the record parser and derived scope**

Implement `load_front_matter(path)`, `derive_scope(root)`,
`validate_record(root, record)`, `validate_transition(previous, candidate)`,
and `main(argv)` with the signatures and return types stated in the
Interfaces block.

`derive_scope` shall read authoritative catalogs and validators rather than
accept counts from the caller. It shall return these keys:

```python
{
    "controls": 91,
    "control_families": 16,
    "architecture_patterns": 7,
    "mapping_sets": 3,
    "mapping_provisions": 404,
    "relationship_legs": 81,
    "negative_dispositions": 325,
    "assessment_foundation": True,
    "draft_profiles": 1,
    "pci_dss_disposition": "HOLD",
}
```

The values shown are the expected starting values, not hard-coded approvals.
The implementation shall derive them and compare them with the readiness
record.

The phase-state matrix shall be exact:

```python
PHASE_GATE_STATES = {
    "evidence_candidate": {gate: "open" for gate in GATE_IDS},
    "closure_candidate": {
        **{gate: "ready" for gate in GATE_IDS if gate != "post_merge"},
        "post_merge": "open",
    },
    "published": {gate: "closed" for gate in GATE_IDS},
}
```

Reject unknown top-level keys, unknown gates, duplicate mapping sets,
self-referential SHA fields in candidate phases, non-HTTPS evidence locators,
untracked required scope inputs, and stale recorded counts.

- [ ] **Step 4: Run v0.5 and frozen v0.4 record tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_v05_beta_release_gates tests.test_release_gates -v
python tools/release_gates.py --check
```

Expected: all tests pass and the historical v0.4 release validator exits 0.

- [ ] **Step 5: Commit Task 1**

```powershell
git add -- tools/v05_beta_release_gates.py tests/test_v05_beta_release_gates.py
git diff --cached --check
git commit -m "feat: define v0.5-beta release contract"
```

### Task 2: Validate exact candidate and taggable evidence

**Files:**
- Modify: `tools/v05_beta_release_gates.py`
- Modify: `tests/test_v05_beta_release_gates.py`
- Reference: `tools/validate_qualified_review_evidence.py`
- Reference: `tools/crosswalks/qualified_review_evidence.py`

**Interfaces:**
- Consumes: v0.5 closure record, external evidence JSON, exact expected head, validation phase, and validation time.
- Produces: `validate_external_evidence(root, record, evidence, expected_head,
  phase, now=None, *, baseline_ref=None, git_runner=subprocess.run) ->
  list[str]`.

- [ ] **Step 1: Add fail-first exact-schema and SHA-domain tests**

Create `closure_evidence()` and `taggable_evidence()` helpers that return
complete valid objects. Add concrete mutations:

```python
class V05ExternalEvidenceTests(unittest.TestCase):
    def assert_rejected(
        self, evidence: dict[str, object], diagnostic: str, phase: str
    ) -> None:
        errors = validate_external_evidence(
            ROOT, record_fixture("closure_candidate"), evidence,
            MERGE_SHA if phase == "taggable" else CLOSURE_SHA,
            phase, FIXED_NOW,
        )
        self.assertIn(diagnostic, errors)

    def test_closure_evidence_rejects_extra_top_level_key(self) -> None:
        evidence = closure_evidence()
        evidence["untrusted"] = {}
        self.assert_rejected(
            evidence, "closure evidence has unknown keys: untrusted", "closure"
        )

    def test_taggable_evidence_rejects_changed_merge_tree(self) -> None:
        evidence = taggable_evidence()
        evidence["merge_tree"] = "f" * 40
        self.assert_rejected(
            evidence, "merged tree shall equal closure tree", "taggable"
        )

    def test_verdict_requires_body_digest(self) -> None:
        evidence = closure_evidence()
        del evidence["technical"]["source"]["body_sha256"]
        self.assert_rejected(
            evidence, "technical source keys are invalid", "closure"
        )

    def test_governance_requires_manual_authority_attestation(self) -> None:
        evidence = closure_evidence()
        evidence["governance"]["authority_attestation"] = False
        self.assert_rejected(
            evidence,
            "governance shall contain an express manual authority attestation",
            "closure",
        )
```

Use the same concrete mutation pattern for missing head/tree values, candidate
and post-merge command set differences, unsuccessful or wrong-SHA checks, and
non-clean or wrong-SHA merge state. Assert a specific diagnostic for each.

The `mermaid_rendering` command result shall be a JSON object, not a plain
success string. Add mutations requiring these exact fields and values:

```python
{
    "rendered_blocks": 23,
    "renderer": "@mermaid-js/mermaid-cli@11.16.0",
    "visual_review": "approved",
    "candidate_inventory_equal": True,
    "merge_tree_equal": True,
    "candidate_review_url": "https://github.com/tdistress/ESAF/...",
    "candidate_reviewer": "resolved nonblank identity",
    "post_merge_reviewer": "resolved nonblank identity",
    "reviewed_at": "resolved RFC 3339 UTC timestamp",
}
```

Reject a plain `"passed"` result, missing reviewer identity, a non-HTTPS
candidate review URL, any false equality flag, a renderer mismatch, or a block
count other than 23.

Use this candidate and post-merge command tuple:

```python
COMMAND_IDS = (
    "full_suite",
    "assessment",
    "profiles",
    "controls",
    "architectures",
    "migration",
    "crosswalk_current",
    "crosswalk_baseline",
    "pci_readiness",
    "links",
    "release_v04",
    "release_v05",
    "mermaid_inventory",
    "mermaid_rendering",
    "whole_range_diff",
    "cache_count",
    "clean_status",
)
```

- [ ] **Step 2: Add fail-first mapping-basis tests**

Owner-risk evidence shall require:

```python
OWNER_DECISION_SCHEMA = "esaf-v05-owner-decision-v1"
QUALIFIED_REVIEW_STATUS = "deferred"
OWNER_DISPOSITION = "accepted_for_working_draft"
MISSING_ROLES = (
    "specification_and_inventory",
    "security_and_overclaiming",
)
```

Add mutation tests for mixed bases, wrong mapping IDs, missing or duplicate
decisions, nonuniform owner sources, fewer or more than six missing-role
objects, wrong accountable owner, missing issue 55, missing re-entry triggers,
changed Draft state, and missing nonclaims.

The exact re-entry trigger set is:

```python
REENTRY_TRIGGERS = {
    "eligible_qualified_reviewer_available",
    "mapping_or_source_inventory_changes",
    "owner_decision_expires_withdrawn_edited_or_superseded",
    "accountable_owner_requires_earlier_completion",
    "closure_candidate_or_merged_tree_changes",
}
```

The exact claim set is:

```python
CLAIMS_NOT_MADE = {
    "qualified_review",
    "qualified_mapping_approval",
    "artifact_lifecycle_approval",
    "certification",
    "compliance",
    "equivalence",
    "endorsement",
    "external_scheme_approval",
    "production_readiness",
    "assurance",
    "implementation_assessment",
    "legal_sufficiency",
    "replacement_of_qualified_professional_judgment",
}
```

For qualified review, add tests requiring an exact-candidate validator report
with:

```python
{
    "evidence_valid": True,
    "readiness_name": "transition_ready",
    "candidate_state": "draft",
    "candidate_sha": closure_head,
}
```

The report shall cover the three exact mapping sets and both roles for each.
Reject `merge_ready`, a `reviewed` candidate, or synthetic three-decision
approval objects without the validated campaign result.

- [ ] **Step 3: Run fail-first evidence tests**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_v05_beta_release_gates -v
```

Expected: the new evidence tests fail because the validator does not yet
implement the contracts.

- [ ] **Step 4: Implement evidence validation**

Implement `validate_external_evidence(root, record, evidence, expected_head,
phase, now=None)` with the signature and return type in the Interfaces block.

Extend the v0.5 gate CLI with:

```text
--external-evidence PATH
--expected-head SHA
--phase closure|taggable
```

Require all three arguments together. Reject external evidence for an
`evidence_candidate` or `published` record.

Closure evidence shall use exact keys:

```python
{
    "schema",
    "release",
    "closure_head",
    "closure_tree",
    "scope",
    "technical",
    "editorial",
    "terminology",
    "rendering",
    "profile_scope",
    "security_overclaiming",
    "whole_range",
    "governance",
    "candidate_commands",
    "mapping_decision_schema",
    "mapping_decision_basis",
    "mapping_decisions",
    "github_checks",
    "merge_state",
    "issue_55",
    "acquisition",
}
```

Taggable evidence adds only `merge_head`, `merge_tree`, and `post_merge`.
Reject missing or extra keys.

Each sourced verdict shall contain:

```python
{
    "sha",
    "reviewer",
    "role",
    "date",
    "disposition",
    "url",
    "critical",
    "important",
    "source",
}
```

`source` shall contain repository, resource path, comment URL, numeric comment
ID, author login, immutable numeric author ID, author association, creation
and update timestamps, body SHA-256, acquisition resource ID, and source
verification timestamp.

The governance object adds:

```python
{
    "authority": "Steering Committee",
    "authority_attestation": True,
    "authority_verification": "manual",
    "authority_basis": "GOVERNANCE.md#21-steering-committee",
}
```

- [ ] **Step 5: Run focused evidence and historical regression tests**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_v05_beta_release_gates `
  tests.test_release_gates `
  tests.test_owner_risk_evidence `
  tests.test_validate_qualified_review_evidence -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit Task 2**

```powershell
git add -- tools/v05_beta_release_gates.py tests/test_v05_beta_release_gates.py
git diff --cached --check
git commit -m "feat: validate v0.5 release evidence"
```

### Task 3: Build authenticated live GitHub evidence

**Files:**
- Create: `tools/v05_beta_release_evidence.py`
- Create: `tests/test_v05_beta_release_evidence.py`
- Modify: `tools/v05_beta_release_gates.py`
- Modify: `tests/test_v05_beta_release_gates.py`

**Interfaces:**
- Consumes: authenticated `gh api`, fixed repository, exact PR number, exact
  comment IDs, expected closure head, and output path.
- Produces: validated closure or taggable evidence JSON outside Git.
- Comment-source boundary: `source_record(response, payload, *,
  expected_container_type, expected_container_number, verified_at)` shall bind
  both canonical comment URLs to the explicitly named PR or issue container.

- [ ] **Step 1: Write the fail-first acquisition-adapter tests**

Define:

```python
@dataclass(frozen=True)
class ApiResponse:
    requested_resource: str
    observed_request_uri: str
    redirect_count: int
    status: int
    headers: tuple[tuple[str, str], ...]
    raw_body: bytes
    retrieved_at: datetime

    def json_object(self) -> dict[str, object]:
        value = json.loads(self.raw_body)
        if not isinstance(value, dict):
            raise ValueError("GitHub API response shall be an object")
        return value

@dataclass(frozen=True)
class ApiPageSet:
    requested_resource: str
    pages: tuple[ApiResponse, ...]
    complete: bool

class ApiClient(Protocol):
    def auth_login(self) -> str:
        raise NotImplementedError

    def get(self, resource: str) -> ApiResponse:
        raise NotImplementedError

    def get_pages(self, resource: str) -> ApiPageSet:
        raise NotImplementedError

class GhApiClient:
    def auth_login(self) -> str:
        return self._run_json(["api", "user"])["login"]

    def get(self, resource: str) -> ApiResponse:
        return self._get_included_response(resource)

    def get_pages(self, resource: str) -> ApiPageSet:
        return self._get_all_pages(resource)
```

`GhApiClient` shall run `gh api` with `GH_DEBUG=api`, capture the exact response
body bytes from stdout, and parse the HTTP request and response boundaries from
the debug stream on stderr. It shall retain only the observed request URI,
response status, response headers, and redirect count; it shall never persist
the raw debug stream or request headers. The trace parser shall reject a
missing request boundary, more than one request/response pair, any 3xx status,
any `Location` header, or an observed request URI that differs from the exact
requested API path and query.

Explicit page requests shall follow `Link: rel="next"` until absent; page
numbers, Link headers, observed request URIs, and terminal-page status
determine `complete`. Tests shall use captured, secret-free `GH_DEBUG=api`
fixtures for `/user`, issue comments, pull requests, check runs, commits, and
Git references so the parser does not depend on payload `url` fields.

Add concrete tests with a `FakeClient` that stores `ApiResponse` envelopes:

```python
class V05AcquisitionTests(unittest.TestCase):
    def test_collector_rejects_redirected_resource(self) -> None:
        client = valid_fake_client()
        response = client.responses[OWNER_RESOURCE]
        client.responses[OWNER_RESOURCE] = replace(
            response,
            observed_request_uri="/repos/other/project/issues/comments/7",
        )
        with self.assertRaisesRegex(ValueError, "GitHub request URI changed"):
            collect_closure_evidence(client, **valid_collection_args())

    def test_collector_rejects_incomplete_pagination(self) -> None:
        client = valid_fake_client()
        client.page_sets[CHECKS_RESOURCE] = replace(
            client.page_sets[CHECKS_RESOURCE], complete=False
        )
        with self.assertRaisesRegex(ValueError, "GitHub pagination is incomplete"):
            collect_closure_evidence(client, **valid_collection_args())

    def test_source_digest_uses_exact_raw_body(self) -> None:
        client = valid_fake_client()
        evidence = collect_closure_evidence(
            client, **valid_collection_args()
        )
        expected = sha256(
            client.responses[OWNER_RESOURCE].raw_body
        ).hexdigest()
        self.assertEqual(
            expected,
            evidence["mapping_decisions"][0]["source"]["response_sha256"],
        )

    def test_operational_cli_rejects_local_snapshot_switches(self) -> None:
        parser = build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["--comment-json", "fabricated.json"])
```

Add equivalent concrete assertions for wrong authenticated login, non-200
status, malformed headers, edited comments, a comment created before the
closure commit, an acquisition older than 15 minutes, mismatched canonical
HTML/API URLs, missing final page, and a raw-body digest mutation.

- [ ] **Step 2: Write fail-first structured-comment parsing tests**

Every source comment shall contain exactly one fenced JSON object.

Owner and scope comment schema:

```json
{
  "schema": "esaf-v05-owner-decision-v1",
  "release": "0.5-beta",
  "sha": "${closureHead}",
  "mapping_decision_basis": "owner_risk_acceptance",
  "decision_type": "owner_risk_acceptance",
  "disposition": "accepted_for_working_draft",
  "qualified_review_status": "deferred",
  "mapping_set_ids": [
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0"
  ],
  "missing_qualified_roles": [
    {"mapping_set_id": "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0", "role": "specification_and_inventory"},
    {"mapping_set_id": "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0", "role": "security_and_overclaiming"},
    {"mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0", "role": "specification_and_inventory"},
    {"mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0", "role": "security_and_overclaiming"},
    {"mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0", "role": "specification_and_inventory"},
    {"mapping_set_id": "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0", "role": "security_and_overclaiming"}
  ],
  "accountable_owner": "tdistress",
  "scope_approval": {
    "scope": "complete_git_tracked_repository",
    "milestone": "v0.5-beta",
    "disposition": "approved_for_working_draft_closure"
  },
  "issue_55_status": "remains_open",
  "lifecycle": "draft",
  "claims_not_made": [
    "artifact_lifecycle_approval",
    "assurance",
    "certification",
    "compliance",
    "endorsement",
    "equivalence",
    "external_scheme_approval",
    "implementation_assessment",
    "legal_sufficiency",
    "production_readiness",
    "qualified_mapping_approval",
    "qualified_review",
    "replacement_of_qualified_professional_judgment"
  ],
  "reentry_triggers": [
    "accountable_owner_requires_earlier_completion",
    "closure_candidate_or_merged_tree_changes",
    "eligible_qualified_reviewer_available",
    "mapping_or_source_inventory_changes",
    "owner_decision_expires_withdrawn_edited_or_superseded"
  ]
}
```

Verdict schema:

```json
{
  "schema": "esaf-v05-release-verdict-v1",
  "release": "0.5-beta",
  "sha": "${closureHead}",
  "kind": "technical",
  "reviewer": "${reviewerIdentity}",
  "role": "technical reviewer",
  "date": "${authenticatedCommentCreationDate}",
  "disposition": "approved",
  "critical": 0,
  "important": 0
}
```

Allow `kind` only from `technical`, `editorial`, `terminology`, `rendering`,
and `profile_scope`. The rendering verdict adds `rendered_blocks: 23`,
`renderer: "@mermaid-js/mermaid-cli@11.16.0"`, and
`visual_review: "approved"`.

Governance schema:

```json
{
  "schema": "esaf-v05-governance-verdict-v1",
  "release": "0.5-beta",
  "sha": "${closureHead}",
  "kind": "governance",
  "approver": "${governanceApprover}",
  "authority": "Steering Committee",
  "authority_attestation": true,
  "authority_verification": "manual",
  "authority_basis": "GOVERNANCE.md#21-steering-committee",
  "date": "${authenticatedCommentCreationDate}",
  "disposition": "approved_for_working_draft_publication",
  "critical": 0,
  "important": 0
}
```

- [ ] **Step 3: Run fail-first collector tests**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_v05_beta_release_evidence -v
```

Expected: import failure for `tools.v05_beta_release_evidence`.

- [ ] **Step 4: Implement the production collector**

Implement `parse_fenced_json`, `source_record`,
`collect_closure_evidence`, `refresh_taggable_evidence`, `build_parser`, and
`main` with the signatures in the Interfaces block and the `ApiResponse`
contract above.

The CLI shall accept resource identifiers and resolved execution values only:

```text
--pr-number
--expected-head
--owner-comment-id
--technical-comment-id
--editorial-comment-id
--terminology-comment-id
--rendering-comment-id
--profile-scope-comment-id
--governance-comment-id
--security-overclaiming-comment-id
--whole-range-comment-id
--output
```

Taggable mode additionally accepts `--base-evidence`, `--merge-head`, and
`--post-merge-rendering-comment-id`. It shall execute the 16 canonical
nonvisual commands in a detached, tree-verified merge-head worktree and fetch
the authenticated post-merge rendering comment. It shall construct post-merge
results itself. It shall not accept caller post-merge results, publication
dates, raw comment JSON, PR JSON, check JSON, merge-state JSON, author
identity, body digest, or derived verdict JSON.

The collector shall query:

```text
user
repos/tdistress/ESAF/commits/{sha}
repos/tdistress/ESAF/issues/comments/{id}
repos/tdistress/ESAF/pulls/{pr}
repos/tdistress/ESAF/commits/{sha}/check-runs
repos/tdistress/ESAF/actions/runs/{run_id}
repos/tdistress/ESAF/issues/55
repos/tdistress/ESAF/git/ref/tags/v0.5-beta
```

Use GraphQL only when REST does not return the clean merge-state value. Record
every queried resource in the acquisition manifest.

- [ ] **Step 5: Verify collector and gate integration**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_v05_beta_release_evidence `
  tests.test_v05_beta_release_gates -v
python -m tools.v05_beta_release_evidence --help
```

Expected: all tests pass and module help exits 0 without creating caches.

- [ ] **Step 6: Commit Task 3**

```powershell
git add -- `
  tools/v05_beta_release_evidence.py `
  tests/test_v05_beta_release_evidence.py `
  tools/v05_beta_release_gates.py `
  tests/test_v05_beta_release_gates.py
git diff --cached --check
git commit -m "feat: collect authenticated v0.5 evidence"
```

### Task 4: Publish the evidence-candidate records and CI gates

**Files:**
- Create: `docs/superpowers/reviews/2026-07-27-v05-beta-publication-readiness.md`
- Create: `docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md`
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tools/README.md`
- Modify: `CHANGELOG.md`
- Modify: `tests/test_release_metadata.py`
- Modify: `tests/test_v05_beta_release_gates.py`
- Modify: `tools/mermaid_inventory.py`
- Create: `tools/mermaid-render-config.json`
- Modify: `tests/test_mermaid_inventory.py`

**Interfaces:**
- Consumes: Task 1 record contract and Task 3 module CLI.
- Produces: valid evidence-candidate records and CI enforcement for both release generations.

- [ ] **Step 1: Add fail-first repository integration tests**

Add concrete repository assertions:

```python
class V05RepositoryIntegrationTests(unittest.TestCase):
    def test_v05_readiness_record_matches_its_phase(self) -> None:
        record = load_front_matter(V05_RECORD)
        self.assertIn(
            record["phase"],
            {"evidence_candidate", "closure_candidate", "published"},
        )
        self.assertEqual(
            PHASE_GATE_STATES[record["phase"]],
            {gate: value["state"] for gate, value in record["gates"].items()},
        )
        self.assertEqual([], validate_record(ROOT, record))

    def test_workflow_runs_both_release_validators(self) -> None:
        workflow = (ROOT / ".github/workflows/catalog-validation.yml").read_text()
        self.assertIn("python tools/release_gates.py --check", workflow)
        self.assertIn(
            "python tools/v05_beta_release_gates.py --check", workflow
        )

    def test_tools_readme_uses_module_invocation(self) -> None:
        readme = (ROOT / "tools/README.md").read_text(encoding="utf-8")
        self.assertIn("python -m tools.v05_beta_release_evidence", readme)

    def test_version_matches_release_record_phase(self) -> None:
        record = load_front_matter(V05_RECORD)
        version = (ROOT / "VERSION.md").read_text(encoding="utf-8")
        expected = (
            "Current Version: **0.4-alpha**"
            if record["phase"] == "evidence_candidate"
            else "Current Version: **0.5-beta**"
        )
        self.assertIn(expected, version)
        if record["phase"] == "closure_candidate":
            self.assertIn("conditional", version.casefold())
            self.assertNotIn("tag condition was satisfied", version.casefold())
```

Add exact path-trigger assertions for both new tools, both new test files, and
both new review records. Assert the changelog contains
`## 0.5-beta - Unreleased` and the required Working Draft nonclaims.

Add synthetic closure-record and allowlist tests here, before the closure
branch exists:

```python
CLOSURE_ALLOWLIST = {
    "VERSION.md",
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "project/RELEASE_PLAN.md",
    "docs/superpowers/reviews/2026-07-27-v05-beta-publication-readiness.md",
}

class V05ClosureInvariantTests(unittest.TestCase):
    def test_closure_candidate_fixture_uses_exact_gate_matrix(self) -> None:
        record = record_fixture("closure_candidate")
        self.assertEqual([], validate_record(ROOT, record))
        self.assertEqual("open", record["gates"]["post_merge"]["state"])

    def test_closure_allowlist_is_exact(self) -> None:
        self.assertEqual(
            CLOSURE_ALLOWLIST,
            set(v05_beta_release_gates.CLOSURE_ALLOWLIST),
        )
```

Add a repository test that enumerates all three mapping-set registries and all
mapping records, asserting `status == "draft"`, empty review-event arrays, and
absence of reviewer and approval metadata.

Extend `tests/test_mermaid_inventory.py` with:

```python
def test_v05_baseline_record_is_allowed_but_not_candidate_approval() -> None:
    failures = check_record(
        discover(ROOT),
        V05_LEDGER,
        expected_status=V05_BASELINE_STATUS,
    )
    self.assertEqual([], failures)
    self.assertNotEqual(APPROVED_STATUS, V05_BASELINE_STATUS)

def test_cli_rejects_unregistered_ledger_path() -> None:
    with tempfile.TemporaryDirectory() as directory:
        unregistered = Path(directory) / "untracked.md"
        unregistered.write_text("# not a release ledger\n", encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--check-record",
                str(unregistered),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
    self.assertEqual(2, result.returncode)
    self.assertIn("registered release ledger", result.stderr)
```

- [ ] **Step 2: Run fail-first integration tests**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_release_metadata `
  tests.test_v05_beta_release_gates `
  tests.test_mermaid_inventory -v
```

Expected: failures for the missing records, workflow steps, documentation, and
changelog section.

- [ ] **Step 3: Add the evidence-candidate readiness record**

Create YAML front matter with:

```yaml
release: 0.5-beta
phase: evidence_candidate
tag: v0.5-beta
issue: 59
repository_scope: complete_git_tracked_repository
publication:
  date: null
  condition: remote_annotated_tag_matches_exact_validated_commit
mapping_sets:
  - uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0
mapping_decision_basis: owner_risk_acceptance
scope_counts:
  controls: 91
  control_families: 16
  architecture_patterns: 7
  mapping_sets: 3
  mapping_provisions: 404
  relationship_legs: 81
  negative_dispositions: 325
  assessment_foundation: true
  draft_profiles: 1
  pci_dss_disposition: HOLD
gates:
  scope: {state: open, evidence: []}
  technical: {state: open, evidence: []}
  editorial: {state: open, evidence: []}
  terminology: {state: open, evidence: []}
  cross_reference_rendering: {state: open, evidence: []}
  standards_mapping: {state: open, evidence: []}
  profile_scope: {state: open, evidence: []}
  release_metadata: {state: open, evidence: []}
  governance: {state: open, evidence: []}
  post_merge: {state: open, evidence: []}
```

The Markdown body shall describe the complete tracked scope, all Draft
limitations, the two mapping-assurance paths, the PCI `HOLD`, issue 55
retention, and the conditional publication boundary.

- [ ] **Step 4: Add the baseline Mermaid record**

Generate the exact inventory for the Task 4 head, render all 23 blocks with
Mermaid CLI 11.16.0, and visually inspect every PNG. Record path, diagram
ordinal, source SHA-256, render-contract SHA-256, renderer version, render
profile, visual-review result, and reviewer.

The render contract is canonical JSON over the exact Mermaid source, source
digest, path, block ordinal, diagram type, pinned renderer and Node versions,
render options, and the complete checked-in render configuration. Prefix the
canonical bytes with `ESAF-MERMAID-RENDER-CONTRACT-V1\0` before hashing. The
operational ledger check shall render every block into a temporary directory
and fail closed if the pinned renderer is missing or any render fails. PNG byte
hashes are not durable evidence because browser rasterization is
nondeterministic. Visual review remains a separate named human attestation.

The record shall say:

```text
This record proves renderer capability and establishes a baseline inventory.
It is not v0.5-beta closure-candidate approval. The exact closure head requires
fresh rendering, digest comparison, and visual review evidence.
```

Update `tools/mermaid_inventory.py` to register exactly two tracked ledgers:

```python
V05_BASELINE_STATUS = (
    "Baseline renderer capability verified; not closure candidate approval"
)
RELEASE_LEDGERS = {
    Path("docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md"):
        APPROVED_STATUS,
    Path("docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md"):
        V05_BASELINE_STATUS,
}
```

Change `check_record` to receive `expected_status`; preserve the v0.4 status
and renderer behavior byte-for-byte. The CLI shall accept only an exact
tracked path in `RELEASE_LEDGERS`.

- [ ] **Step 5: Wire CI and document operator commands**

Add workflow path triggers for both new tools, both new tests, and both new
records. Add these validation steps:

```yaml
- name: Validate historical release record
  run: python tools/release_gates.py --check
- name: Validate v0.5-beta release record
  run: python tools/v05_beta_release_gates.py --check
```

Document:

```powershell
python tools/v05_beta_release_gates.py --check
python -m tools.v05_beta_release_evidence --help
```

Add `## 0.5-beta - Unreleased` to `CHANGELOG.md`. Describe the assessment
foundation, Draft UK profile, PCI DSS `HOLD`, deferred UK mapping assurance,
and release tooling without claiming publication.

- [ ] **Step 6: Run focused and repository validators**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_release_metadata `
  tests.test_v05_beta_release_gates `
  tests.test_v05_beta_release_evidence `
  tests.test_release_gates `
  tests.test_owner_risk_evidence `
  tests.test_mermaid_inventory -v
python tools/release_gates.py --check
python tools/v05_beta_release_gates.py --check
python tools/validate_links.py --check
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 7: Commit Task 4**

```powershell
git add -- `
  .github/workflows/catalog-validation.yml `
  CHANGELOG.md `
  tools/README.md `
  docs/superpowers/reviews/2026-07-27-v05-beta-publication-readiness.md `
  docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md `
  tests/test_release_metadata.py `
  tests/test_v05_beta_release_gates.py `
  tools/mermaid-render-config.json `
  tools/mermaid_inventory.py `
  tests/test_mermaid_inventory.py
git diff --cached --check
git commit -m "docs: establish v0.5 evidence candidate"
```

### Task 5: Review and merge the evidence capability

**Files:**
- Review: complete branch diff from `b9a6e63993bf9cf546e5d716d41c037c3eeb26db`
- External: GitHub pull request and checks

**Interfaces:**
- Consumes: Tasks 1 through 4.
- Produces: merged evidence capability on clean `main`.

- [ ] **Step 1: Run complete exact-head validation**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -v
python tools/validate_assessment.py --check
python tools/validate_profiles.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref b9a6e63993bf9cf546e5d716d41c037c3eeb26db
python tools/render_pci_dss_mapping_go_no_go.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
python tools/v05_beta_release_gates.py --check
git diff --check b9a6e63993bf9cf546e5d716d41c037c3eeb26db..HEAD
```

Render all Mermaid blocks with `@mermaid-js/mermaid-cli@11.16.0`, visually
inspect every result, verify zero Python caches, and verify clean status.

- [ ] **Step 2: Dispatch exact-head independent reviews**

Require separate reviewers for:

- release contract and test quality;
- security, source acquisition, and overclaiming;
- complete branch diff and publication boundary.

Each review shall name the exact head SHA and report Critical, Important, and
Minor findings. Fix all Critical and Important findings, rerun affected gates,
and redispatch exact-head review after any change.

- [ ] **Step 3: Push and open the evidence pull request**

```powershell
git push -u origin agent/v05-beta-publication-closure
gh pr create `
  --repo tdistress/ESAF `
  --base main `
  --head agent/v05-beta-publication-closure `
  --title "Prepare v0.5-beta publication evidence" `
  --body-file .superpowers/sdd/2026-07-27-v05-beta-publication-closure/pr-body.md
```

The PR body shall record the reviewed head, exact commands and results, all
review verdicts, the non-release boundary, and the human decisions still
required.

- [ ] **Step 4: Verify and merge**

Verify the live PR head equals the reviewed SHA, `Validate ESAF sources`
succeeds on that SHA, the merge state is clean, and no review has unresolved
Critical or Important findings. Merge the PR, update local `main`, rerun
proportional validation, and retain this plan's evidence worktree and ignored
SDD ledger until Task 9. Do not delete the recovery ledger between the evidence
PR and closure PR.

### Task 6: Create the exact metadata-only closure candidate

**Files:**
- Modify: `VERSION.md`
- Modify: `README.md`
- Modify: `ROADMAP.md`
- Modify: `CHANGELOG.md`
- Modify: `project/RELEASE_PLAN.md`
- Modify: `docs/superpowers/reviews/2026-07-27-v05-beta-publication-readiness.md`

**Interfaces:**
- Consumes: merged Task 5 evidence capability.
- Produces: one immutable closure-head commit and tree.

- [ ] **Step 1: Create a fresh isolated closure branch**

Create `agent/v05-beta-publication-closure-candidate` from clean updated
`main`. Record `$closureBase = git rev-parse HEAD`.

- [ ] **Step 2: Verify the prewritten phase and closure invariants**

Run the Stage 1 tests against the unmodified closure branch:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest `
  tests.test_release_metadata `
  tests.test_v05_beta_release_gates -v
```

Expected: the phase-aware repository tests pass for the current
`evidence_candidate`; the synthetic closure allowlist and gate-matrix tests
also pass. These tests were written and reviewed in Stage 1, so the closure
branch changes only the six permitted metadata files. Do not edit tests on
this branch.

- [ ] **Step 3: Update conditional release metadata**

Set:

```text
Current Version: 0.5-beta
Status: Working Draft
Release Stage: Priority Crosswalk and Draft Profile Beta
```

Every metadata surface shall say publication is conditional on the remote
annotated `v0.5-beta` tag resolving to the exact validated merge. Do not state
that the tag exists.

Change the readiness record to `closure_candidate`, keep the publication date
null, set all non-post-merge gates to `ready`, leave `post_merge` `open`, and
add only stable HTTPS evidence locators that actually exist. Candidate records
shall not contain tag objects, tagged commits, or issue-publication evidence
identity.

Replace exactly these three normalized paragraphs in their existing ordered
positions in the readiness body:

```text
This closure candidate covers the complete Git-tracked repository. Its derived inventory contains 91 controls in 16 families, 7 architecture patterns, 3 mapping sets, and 404 mapping provisions. The mappings contain 81 relationship legs and 325 negative dispositions.

The current ESAF version is `0.5-beta`. The non-post-merge v0.5 gates are ready, the post-merge gate is open, and the `v0.5-beta` tag has not been created. The `v0.5-beta` release status is Working Draft. This closure candidate does not approve publication.

Publication remains conditional on the remote annotated `v0.5-beta` tag resolving to the exact validated merged commit. This closure candidate requires its own exact-head reviews, rendering evidence, owner and scope decision, governance decision, successful checks, and clean merge state. The post-merge gate remains open until merged-main validation and remote tag verification are complete.
```

Retain every other heading and paragraph exactly, allowing only paragraph line
wrapping and whitespace normalization. Do not add the optional
evidence-candidate discussion paragraph or any other block. The phase-aware
prose validator accepts this exact ordered closure form without changes to the
validator or its tests.

- [ ] **Step 4: Commit the six-file candidate, then validate and freeze**

Verify the complete branch path set equals the six-path
`CLOSURE_ALLOWLIST`. Commit:

```powershell
git add -- `
  VERSION.md README.md ROADMAP.md CHANGELOG.md project/RELEASE_PLAN.md `
  docs/superpowers/reviews/2026-07-27-v05-beta-publication-readiness.md
git diff --cached --check
git commit -m "release: prepare v0.5-beta closure candidate"
```

Set:

```powershell
$closureHead = (git rev-parse HEAD).Trim()
$closureTree = (git rev-parse "$closureHead^{tree}").Trim()
```

Run the complete Task 5 Step 1 command set with
`--baseline-ref $closureBase` on `$closureHead`. Render and visually review all
Mermaid blocks, run whole-range diff, cache, and clean-status gates, and record
all results against `$closureHead`.

No tracked change may follow. A validation failure requires a fix commit, a new
closure head, and complete revalidation. Do not claim the prior SHA's results
for the new head.

### Task 7: Acquire exact-head reviews and non-delegable decisions

**Files:**
- External only: closure PR, GitHub comments, temporary evidence directory
- Do not modify tracked files

**Interfaces:**
- Consumes: frozen closure head and tree.
- Produces: exact-head review comments, owner/scope decision, governance decision, successful CI, and closure evidence.

- [ ] **Step 1: Push the closure candidate and open the PR**

Push `agent/v05-beta-publication-closure-candidate` and open a ready PR. Record
the PR number and confirm its `headRefOid` equals `$closureHead`.

- [ ] **Step 2: Dispatch exact-head reviews**

Dispatch independent technical, editorial, terminology, rendering, profile
scope, security/overclaiming, and whole-range reviews. Reviewers shall inspect
the exact closure range and name `$closureHead`. Rendering review shall render
all 23 Mermaid blocks with CLI 11.16.0 and record visual approval.

Post one structured verdict comment for each required `kind`. Do not label
subagent review as human qualified mapping review.

- [ ] **Step 3: Prepare the exact owner and governance decision text**

Resolve `$closureHead` and the six exact missing-role objects into the Task 3
schemas. Each review and governance verdict date shall be the UTC calendar
date of its own authenticated comment creation. Present the complete
owner/scope JSON and
governance JSON to the repository owner and the actual governance approver,
respectively.

STOP until the owner expressly approves the exact owner-risk and scope
decision for `$closureHead`. Separately, STOP until the actual governance
approver expressly attests in their own decision that they are authorized to
act for the Steering Committee and approves Working Draft publication for the
same `$closureHead`. If the repository owner and governance approver are the
same person, they shall still make two separate substantive decisions and the
governance comment shall state the separate authority being exercised.
Standing repository authorization does not satisfy either decision.

- [ ] **Step 4: Record and fetch the decisions**

After each decision maker expressly approves their own exact text, record each
decision through that decision maker's authenticated GitHub identity without
changing its semantic content. Automation shall not post a governance decision
under a different person's identity. Record the numeric comment IDs and fetch
each independently with:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m tools.v05_beta_release_evidence `
  --pr-number $prNumber `
  --expected-head $closureHead `
  --owner-comment-id $ownerCommentId `
  --technical-comment-id $technicalCommentId `
  --editorial-comment-id $editorialCommentId `
  --terminology-comment-id $terminologyCommentId `
  --rendering-comment-id $renderingCommentId `
  --profile-scope-comment-id $profileScopeCommentId `
  --governance-comment-id $governanceCommentId `
  --security-overclaiming-comment-id $securityOverclaimingCommentId `
  --whole-range-comment-id $wholeRangeCommentId `
  --output $closureEvidence
```

Validate:

```powershell
python tools/v05_beta_release_gates.py --check `
  --baseline-ref $closureBase `
  --external-evidence $closureEvidence `
  --expected-head $closureHead `
  --phase closure
```

- [ ] **Step 5: Re-fetch immediately before merge**

Require successful `Validate ESAF sources` on `$closureHead`, clean merge
state, no pending checks, and unchanged comment IDs, identities, timestamps,
bodies, and digests. Rebuild closure evidence within 15 minutes of the merge
attempt and validate it again.

### Task 8: Merge, validate merged main, and create the tag

**Files:**
- External only until the durable publication record task

**Interfaces:**
- Consumes: validated closure evidence and clean exact-head PR.
- Produces: validated merge commit, taggable evidence, remote annotated tag, and issue 59 publication evidence.

- [ ] **Step 1: Merge and verify tree equality**

Merge the closure PR without squashing content changes into a different tree.
Fetch merged `main` and set:

```powershell
$mergeHead = (git rev-parse origin/main).Trim()
$mergeTree = (git rev-parse "$mergeHead^{tree}").Trim()
if ($mergeTree -ne $closureTree) { throw "Merged tree differs from closure tree" }
```

If the trees differ, do not tag. Create a new closure candidate and return to
Task 7.

- [ ] **Step 2: Authenticate the post-merge visual review**

Create a separate issue 59 comment after the merge that records the authenticated
post-merge Mermaid review. The comment shall use the
`esaf-v05-post-merge-rendering-verdict-v1` schema and bind the merge commit,
merge tree, 23/23 disposition, exact Mermaid renderer, reviewer identity, and
review time.
The collector shall fetch this comment directly and shall not accept any
caller-provided command or rendering result file.

The authenticated reviewer shall open every generated SVG before posting the
comment. If any diagram is unreadable, do not post an approved disposition and
do not tag.

- [ ] **Step 3: Build and validate fresh taggable evidence**

Fully re-fetch the user, closure and merge commits, PR, issue 55, every comment,
check-run page, canonical Actions run, and tag resources. Give every acquired
resource its own retrieval time and reject any resource older than the
15-minute freshness window. Run:

```powershell
python -m tools.v05_beta_release_evidence `
  --base-evidence $closureEvidence `
  --merge-head $mergeHead `
  --post-merge-rendering-comment-id $postMergeRenderingCommentId `
  --pr-number $prNumber `
  --expected-head $closureHead `
  --owner-comment-id $ownerCommentId `
  --technical-comment-id $technicalCommentId `
  --editorial-comment-id $editorialCommentId `
  --terminology-comment-id $terminologyCommentId `
  --rendering-comment-id $renderingCommentId `
  --profile-scope-comment-id $profileScopeCommentId `
  --governance-comment-id $governanceCommentId `
  --security-overclaiming-comment-id $securityOverclaimingCommentId `
  --whole-range-comment-id $wholeRangeCommentId `
  --output $taggableEvidence

python tools/v05_beta_release_gates.py --check `
  --baseline-ref $closureBase `
  --external-evidence $taggableEvidence `
  --expected-head $mergeHead `
  --phase taggable
```

- [ ] **Step 4: Create and verify the annotated tag**

Verify neither local nor remote `v0.5-beta` exists. Create an annotated tag
whose message states Working Draft status, the owner-risk basis, deferred
qualified review, issue 55 retention, and every required nonclaim.

Push only the tag. Fetch it back and verify:

```powershell
$tagObject = (git rev-parse 'v0.5-beta^{tag}').Trim()
$peeled = (git rev-parse 'v0.5-beta^{}').Trim()
if ($peeled -ne $mergeHead) { throw "Remote tag does not peel to validated merge" }
```

- [ ] **Step 5: Post consolidated evidence and close issue 59**

Post one issue 59 comment containing the evidence PR and closure PR heads and
merges, remote tag object and peeled commit, every derived count, all command
results, all exact-head verdict locators, owner/scope and governance locators,
mapping basis and three exact mapping IDs, issue 55 retention, tree equality,
zero Critical/Important findings, and Working Draft nonclaims.

Fetch the comment back, compare its SHA-256, verify the remote tag again, then
close issue 59. Leave issue 55 open.

### Task 9: Record durable publication truth and clean up

**Files:**
- Modify: `docs/superpowers/reviews/2026-07-27-v05-beta-publication-readiness.md`
- Modify: `project/RELEASE_PLAN.md`
- Modify: `project/BACKLOG.md`
- Modify: `project/MILESTONES.md`
- Modify: `ROADMAP.md`
- Modify: `CHANGELOG.md`
- Modify: `tests/test_release_metadata.py`
- Modify: `tests/test_v05_beta_release_gates.py`

**Interfaces:**
- Consumes: verified tag object, peeled merge commit, and issue 59 evidence URL.
- Produces: immutable published record validated without live network access.

- [ ] **Step 1: Write fail-first published-record tests**

Require the exact fixed publication date, tag object, tagged commit, evidence
URL, owner-risk basis, closed gate matrix, issue 55 open state, and local
annotated-tag resolution. Reject external closure evidence as a substitute for
the published record. Permit a `published` record to be checked against a
`published` baseline only when the complete gate matrix and all publication
identity fields are unchanged; reject every published-to-candidate transition.

- [ ] **Step 2: Update the durable record and planning truth**

Set the readiness record phase to `published`, every gate to `closed`, and add
the UTC calendar date derived from the annotated tag operation, resolved tag
object, tagged commit, and issue evidence URL. Set
`mapping_decision_basis` explicitly to `owner_risk_acceptance`; the published
body below is valid only for that basis. A future `qualified_approval`
publication path requires separately reviewed prose and an explicit issue 55
lifecycle decision rather than reuse of this template. Update release plan,
backlog, milestone, roadmap, and changelog to describe the published Working
Draft without changing any artifact lifecycle state or closing issue 55.

Use this complete exact readiness body, allowing only paragraph line wrapping
and whitespace normalization:

```markdown
# v0.5-beta publication readiness

## Scope

This published record covers the complete Git-tracked repository. Its derived
inventory contains 91 controls in 16 families, 7 architecture patterns, 3
mapping sets, and 404 mapping provisions. The mappings contain 81 relationship
legs and 325 negative dispositions.

The scope includes the ESAF-1500 assessment foundation and one Draft UK pilot
profile under the reusable profile contract. The PCI DSS readiness record has
the approved `HOLD` disposition. That disposition does not establish a PCI DSS
mapping, assessment, certification, compliance, equivalence, endorsement, or
legal conclusion.

## Lifecycle boundary

The current ESAF version is `0.5-beta`. The `v0.5-beta` Working Draft is
published. Publication is limited to the repository Working Draft and does not
change any artifact lifecycle state.

All controls, architecture patterns, the pilot profile, mapping sets, and
mapping records remain Draft. The three mapping lifecycle records have empty
event arrays. This publication does not add reviewer metadata, approval
metadata, or lifecycle events to those artifacts.

## Mapping assurance

This published Working Draft uses the owner-risk-acceptance mapping basis
recorded in front matter. Qualified approval remains deferred and requires a
validated six-role Draft campaign bound to the exact published commit. The
owner-risk decision permits only Working Draft publication; it does not
approve mappings or change artifact lifecycle state.

Issue 55 remains open for qualified review. Owner-risk acceptance does not
complete qualified review or approve the mappings. It does not establish
qualified mapping approval, artifact lifecycle approval, certification,
compliance, equivalence, endorsement, external scheme approval, production
readiness, assurance, implementation assessment, legal sufficiency, or
replacement of qualified professional judgment.

## Publication evidence

The exact annotated `v0.5-beta` tag object, tagged commit, publication date,
and issue 59 evidence URL are recorded in this record's front matter. This
body does not independently identify or replace that durable publication
evidence.
```

Do not add the evidence-candidate optional paragraph or any other block.

- [ ] **Step 3: Validate and independently review the publication record**

Run the full suite, all validators, both release validators, local tag
resolution, link validation, whole-range diff checks, zero-cache check, and
clean status. Dispatch exact-head metadata and overclaiming reviews. Resolve
all Critical and Important findings.

- [ ] **Step 4: Publish the record PR**

Commit, push, open a PR, wait for successful CI and clean merge state, merge,
update local `main`, and rerun proportional validation.

- [ ] **Step 5: Final external and repository verification**

Verify:

- remote `v0.5-beta` tag object and peeled commit match the durable record;
- issue 59 is closed and its evidence comment digest matches;
- issue 55 remains open;
- all three mapping sets and records remain Draft without reviewer or lifecycle
  metadata changes;
- `main` is clean and equals `origin/main`; and
- no temporary evidence, caches, branches, or plan-owned worktrees remain.

Remove completed temporary branches and worktrees while preserving the
canonical SDD workspace, unrelated worktrees, and user changes. After Task 9
is recorded complete and the final whole-plan review passes, let the
subagent-driven-development workflow delete only this plan's SDD workspace.
