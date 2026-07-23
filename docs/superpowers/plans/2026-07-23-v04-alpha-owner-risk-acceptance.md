# ESAF 0.4-Alpha Owner Risk-Acceptance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the `0.4-alpha` Working Draft publication workflow using one uniform, explicitly disclosed mapping-decision basis while preserving every remaining exact-SHA, governance, review, CI, post-merge, tag, and lifecycle gate.

**Architecture:** First merge a separate amendment PR that adds the versioned mapping-decision boundary, tested owner-evidence controller, durable two-basis metadata rules, backlog retention, and fully reconciled execution plan. Then create a fresh branch from the amended `main` for the original evidence-only closure PR, whose diff remains limited to the original five closure files. Live GitHub sources are fetched into temporary files, verified and assembled by the controller, and validated offline in both closure and taggable phases.

**Tech Stack:** Python 3 standard library, `unittest`, YAML front matter through PyYAML, Markdown, PowerShell, Git, GitHub CLI, Mermaid CLI 11.16.0.

## Global Constraints

- The binding design is `docs/superpowers/specs/2026-07-23-v04-alpha-owner-risk-acceptance-design.md`; it supersedes only the qualified-only clauses identified there.
- `mapping_decision_schema` shall equal `esaf-mapping-decisions-v1`.
- `mapping_decision_basis` shall be uniformly `qualified_approval` or uniformly `owner_risk_acceptance`; mixed bases shall fail.
- `mapping_decisions` shall contain exactly one decision for each member of `EXPECTED_MAPPING_SETS`.
- Every mapping decision and scope decision shall remain bound to `closure_head` in both `closure` and `taggable` phases.
- Only `merge_head` and `post_merge.sha` shall use the merged-main SHA; the enclosing `post_merge.sha` binds every command result.
- Every decision timestamp shall be RFC 3339, and its UTC date shall equal the tracked conditional publication date.
- Owner `decided_at` shall equal the verified source comment `created_at`.
- Owner evidence shall identify repository `tdistress/ESAF`, an immutable numeric GitHub comment and user ID, `OWNER` association, and the SHA-256 digest of the exact fetched UTF-8 comment body.
- The exact limitation set is `compliance`, `certification`, `equivalence`, `endorsement`, `external_scheme_approval`, `assurance`, and `production_readiness`; lifecycle shall remain `draft`.
- Owner risk acceptance shall retain qualified-review backlog coverage for all three exact mapping-set IDs.
- Qualified approval shall preserve reviewer, qualification, disposition, source, exact-SHA, timestamp, limitation, and completed-review checks.
- Steering Committee governance approval shall remain a separate comment and evidence object.
- All controls, architectures, and mappings shall remain Draft; no publication statement may imply external-scheme approval or qualified review when the selected basis is owner risk acceptance.
- The generic owner comment on merged PR A shall not be used as substantive mapping or scope evidence.
- External evidence JSON, fetched comments, render outputs, and reviewer scratch material shall remain outside the repository.
- Validator, automation, backlog, specification, and controller changes shall merge through an amendment PR before the evidence-only closure PR is created.
- The evidence-only closure PR shall modify only `CHANGELOG.md`, `project/RELEASE_PLAN.md`, `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md`, `tests/test_release_metadata.py`, and `tests/test_release_gates.py`.
- No tag may be created until every unchanged publication gate passes on the exact candidate and merged-main SHA domains.
- Set `PYTHONDONTWRITEBYTECODE=1` for validation and leave no `__pycache__` directory.

## File and interface map

- `tools/release_gates.py` owns offline schema, exact-SHA, timestamp, basis, scope, governance, CI, merge-state, and post-merge validation.
- `tools/owner_risk_evidence.py` owns deterministic parsing and verification of fetched owner comments and assembly of complete temporary external evidence from fetched inputs.
- `tests/test_owner_risk_evidence.py` owns fail-closed controller tests for source edits, identity, association, structured content, digest, SHA, scope, limitations, and evidence assembly.
- `tests/test_release_gates.py` owns synthetic evidence fixtures and the identical closure/taggable mutation matrix for both bases.
- `tests/test_release_metadata.py` owns conditional publication wording, readiness, release-plan, backlog, issue-evidence-template, and tag-message invariants.
- `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md` owns the tracked release state and selected-basis disclosure without storing commit SHAs.
- `project/RELEASE_PLAN.md` owns the durable two-basis gate rule and the selected `0.4-alpha` closure state.
- `project/BACKLOG.md` retains deferred qualified review for the three exact mapping-set IDs under owner risk acceptance.
- `CHANGELOG.md` records the conditional UTC publication date and Working Draft limitations.
- `docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md` remains the end-to-end publication controller and shall be revised throughout so no qualified-only conflict remains.
- GitHub PR B, issue #39, the owner decision comment, the separate Steering Committee comment, temporary external evidence, and annotated tag `v0.4-alpha` own non-self-referential execution evidence.

---

### Task 1: Implement the versioned two-basis evidence contract

**Files:**
- Modify: `tests/test_release_gates.py`
- Modify: `tools/release_gates.py`
- Create: `tests/test_owner_risk_evidence.py`
- Create: `tools/owner_risk_evidence.py`

**Interfaces:**
- Consumes: `record["publication"]["date"]`, `EXPECTED_MAPPING_SETS`, `closure_head`, `expected_head`, and external evidence JSON.
- Produces: `validate_external_evidence(record: dict[str, object], evidence: dict[str, object], expected_head: str, phase: str) -> list[str]` with both decision bases.
- Extends: `validate_record(root: Path, record: dict[str, object]) -> list[str]` so a closure candidate declares exactly one supported `mapping_decision_basis`.
- Produces: `_validate_mapping_decisions(errors: list[str], record: dict[str, object], evidence: dict[str, object], closure_head: object) -> None`.
- Produces: `_validate_scope_decision(errors: list[str], record: dict[str, object], value: object, closure_head: object, basis: object) -> None`.
- Produces: `parse_owner_decision(body: str) -> dict[str, object]`.
- Produces: `verify_owner_comment(comment: dict[str, object], expected_head: str, publication_date: str, verified_at: str) -> dict[str, object]`.
- Produces: `build_external_evidence(owner_source: dict[str, object], closure_head: str, verdict_comments: dict[str, dict[str, object]], pr_state: dict[str, object]) -> dict[str, object]`.
- Produces: `refresh_taggable_evidence(base_evidence: dict[str, object], owner_source: dict[str, object], merge_head: str, post_merge: dict[str, object]) -> dict[str, object]`.
- Produces CLI build mode: `python tools/owner_risk_evidence.py --comment-json PATH --technical-comment-json PATH --editorial-comment-json PATH --rendering-comment-json PATH --governance-comment-json PATH --pr-state-json PATH --expected-head SHA --publication-date YYYY-MM-DD --verified-at RFC3339 --output PATH`.
- Produces CLI taggable-refresh mode: the same command with `--base-evidence PATH --merge-head SHA --post-merge-json PATH` instead of `--inputs-json`.
- Preserves: existing technical, editorial, rendering, governance, GitHub-check, merge-state, and post-merge diagnostics.

- [ ] **Step 1: Replace the qualified-only fixture with explicit v1 fixtures**

In `tests/test_release_gates.py`, add constants and helpers with these exact fields:

```python
CLAIMS_NOT_MADE = {
    "compliance",
    "certification",
    "equivalence",
    "endorsement",
    "external_scheme_approval",
    "assurance",
    "production_readiness",
}


def publication_timestamp() -> str:
    return f"{datetime.now(timezone.utc).date().isoformat()}T12:00:00Z"


def owner_source(created_at: str) -> dict[str, object]:
    return {
        "repository": "tdistress/ESAF",
        "comment_url": "https://github.com/tdistress/ESAF/pull/51#issuecomment-1001",
        "comment_id": 1001,
        "author_login": "tdistress",
        "author_user_id": 2001,
        "author_association": "OWNER",
        "created_at": created_at,
        "updated_at": created_at,
        "body_sha256": "a" * 64,
        "source_verified_at": publication_timestamp(),
    }


def limitations() -> dict[str, object]:
    return {
        "lifecycle": "draft",
        "claims_not_made": sorted(CLAIMS_NOT_MADE),
    }


def mapping_decisions(
    closure: str, basis: str,
) -> list[dict[str, object]]:
    decided_at = publication_timestamp()
    if basis == "qualified_approval":
        return [
            {
                "mapping_set_id": mapping_set_id,
                "decision_type": basis,
                "sha": closure,
                "decided_at": decided_at,
                "url": f"https://github.com/tdistress/ESAF/pull/51#issuecomment-{1100 + index}",
                "reviewer": f"qualified-reviewer-{index}",
                "qualification": "documented scheme and ESAF qualification",
                "disposition": "approved",
                "qualified_review_status": "completed",
                "limitations": limitations(),
            }
            for index, mapping_set_id in enumerate(EXPECTED_MAPPING_SETS, start=1)
        ]
    source = owner_source(decided_at)
    return [
        {
            "mapping_set_id": mapping_set_id,
            "decision_type": basis,
            "sha": closure,
            "decided_at": decided_at,
            "url": source["comment_url"],
            "owner_login": source["author_login"],
            "owner_user_id": source["author_user_id"],
            "role": "repository_owner",
            "author_association": "OWNER",
            "disposition": "accepted_for_working_draft",
            "qualified_review_status": "deferred",
            "limitations": limitations(),
            "source": deepcopy(source),
        }
        for mapping_set_id in EXPECTED_MAPPING_SETS
    ]
```

Change `approved_external_evidence` to accept `basis: str = "qualified_approval"`, emit:

```python
"mapping_decision_schema": "esaf-mapping-decisions-v1",
"mapping_decision_basis": basis,
"mapping_decisions": mapping_decisions(closure, basis),
```

For qualified scope, retain the current approved scope fixture. For owner-risk scope, emit:

```python
{
    "approval_basis": "owner_risk_acceptance",
    "sha": closure,
    "owner_login": source["author_login"],
    "owner_user_id": source["author_user_id"],
    "role": "repository_owner",
    "author_association": "OWNER",
    "decided_at": source["created_at"],
    "scope": "complete_git_tracked_repository",
    "limitations": limitations(),
    "source": deepcopy(source),
}
```

- [ ] **Step 2: Write fail-first acceptance and uniformity tests**

Add tests that run both bases in both phases:

```python
def test_both_uniform_mapping_decision_bases_pass_closure_and_taggable(self) -> None:
    closure = "d" * 40
    merge = "f" * 40
    for basis in ("qualified_approval", "owner_risk_acceptance"):
        with self.subTest(basis=basis, phase="closure"):
            evidence = approved_external_evidence(closure, basis=basis)
            self.assertEqual(
                validate_external_evidence(
                    closure_record(basis), evidence, closure, "closure"
                ),
                [],
            )
        with self.subTest(basis=basis, phase="taggable"):
            evidence = approved_external_evidence(closure, merge, basis=basis)
            self.assertEqual(
                validate_external_evidence(
                    closure_record(basis), evidence, merge, "taggable"
                ),
                [],
            )


def test_mapping_decisions_require_v1_schema_and_uniform_basis(self) -> None:
    closure = "d" * 40
    cases = (
        (
            "schema",
            lambda e: e.__setitem__("mapping_decision_schema", "legacy"),
            "mapping decision schema shall equal esaf-mapping-decisions-v1",
        ),
        (
            "mixed",
            lambda e: e["mapping_decisions"][0].__setitem__(
                "decision_type", "owner_risk_acceptance"
            ),
            "mapping decisions shall uniformly match mapping_decision_basis",
        ),
        (
            "duplicate",
            lambda e: e["mapping_decisions"].append(
                deepcopy(e["mapping_decisions"][0])
            ),
            "mapping decisions shall contain each expected mapping set exactly once",
        ),
    )
    for name, mutate, diagnostic in cases:
        with self.subTest(name=name):
            evidence = approved_external_evidence(closure)
            mutate(evidence)
            self.assertIn(
                diagnostic,
                validate_external_evidence(closure_record(), evidence, closure, "closure"),
            )
```

Add a tracked-record binding test:

```python
def test_closure_record_and_external_evidence_require_the_same_basis(self) -> None:
    closure = "d" * 40
    record = closure_record()
    record["mapping_decision_basis"] = "owner_risk_acceptance"
    evidence = approved_external_evidence(closure, basis="qualified_approval")
    self.assertIn(
        "external mapping decision basis shall match the closure record",
        validate_external_evidence(record, evidence, closure, "closure"),
    )
```

Update `closure_record()` to accept `basis: str = "qualified_approval"` and set
`record["mapping_decision_basis"] = basis`. Add `validate_record` cases proving
that a closure candidate rejects a missing or unsupported basis, while the
already-merged `evidence_candidate` record may omit it.

- [ ] **Step 3: Write the identical global mutation matrix for both bases and phases**

Refactor the existing mutation cases into a helper that applies each global mutation to `qualified_approval` and `owner_risk_acceptance` evidence in both `closure` and `taggable`. Include exact cases for:

```python
GLOBAL_MUTATIONS = (
    ("missing_check", lambda e: e.pop("github_checks"), "GitHub checks are required"),
    (
        "failed_check",
        lambda e: e["github_checks"]["observed"][0].__setitem__("conclusion", "failure"),
        "GitHub check conclusion shall be success",
    ),
    (
        "dirty_merge",
        lambda e: e["merge_state"].__setitem__("state", "dirty"),
        "merge state shall be clean",
    ),
    (
        "unmergeable",
        lambda e: e["merge_state"].__setitem__("mergeable", False),
        "merge state shall be mergeable",
    ),
    (
        "governance_authority",
        lambda e: e["governance"].__setitem__("authority", "repository owner"),
        "governance authority is not authorized",
    ),
    (
        "stale_closure_sha",
        lambda e: e["mapping_decisions"][0].__setitem__("sha", "a" * 40),
        "mapping decision is not bound to closure head",
    ),
)
```

For taggable evidence also retain failed/missing post-merge command, wrong `merge_head`, and wrong `post_merge.sha` mutations. Assert the same diagnostic for both bases.

- [ ] **Step 4: Write fail-first qualified-approval branch tests**

For qualified evidence, independently mutate `reviewer`, `qualification`, `disposition`, `qualified_review_status`, `decided_at`, `url`, `limitations.lifecycle`, and every member of `limitations.claims_not_made`. Assert exact diagnostics, including:

```python
"qualified mapping reviewer shall be named"
"qualified mapping reviewer shall be qualified"
"qualified mapping disposition shall be approved"
"qualified review status shall be completed"
"mapping decision timestamp shall be RFC 3339"
"mapping decision UTC date shall equal conditional publication date"
"mapping decision URL shall use HTTPS"
"mapping decision lifecycle shall equal draft"
"mapping decision prohibited claims shall equal the required set"
```

Add cross-basis wording fields to synthetic evidence and prove qualified approval rejects `owner_risk_acceptance`, `deferred`, or repository-owner-publication-basis claims.

- [ ] **Step 5: Write fail-first owner-risk branch and owner-scope tests**

Use `closure_record("owner_risk_acceptance")` for every owner branch case. Mutate owner evidence through non-owner association, blank login, nonnumeric immutable user ID, wrong role, wrong disposition, completed review status, mismatched `decided_at`, stale timestamp, wrong repository, nonnumeric comment ID, non-HTTPS comment URL, a decision URL that differs from `source.comment_url`, edited body digest, invalid `source_verified_at`, identity/source mismatch, an owner-scope source that differs from the mapping-decision source, incomplete scope, and wrong limitation set. Assert precise diagnostics.

Include this explicit PR-A replay rejection:

```python
def test_owner_risk_rejects_pr_a_head_rebinding_in_both_phases(self) -> None:
    closure = "d" * 40
    merge = "f" * 40
    old_pr_a_head = "a" * 40
    for phase, expected in (("closure", closure), ("taggable", merge)):
        with self.subTest(phase=phase):
            evidence = approved_external_evidence(
                closure,
                merge if phase == "taggable" else None,
                basis="owner_risk_acceptance",
            )
            evidence["scope"]["sha"] = old_pr_a_head
            for decision in evidence["mapping_decisions"]:
                decision["sha"] = old_pr_a_head
            errors = validate_external_evidence(
                closure_record("owner_risk_acceptance"), evidence, expected, phase
            )
            self.assertIn("scope approval is not bound to closure head", errors)
            self.assertIn("mapping decision is not bound to closure head", errors)
```

Add an owner-risk wording field containing completed-qualified-review language and prove it fails.

- [ ] **Step 6: Write fail-first owner-evidence controller tests**

Create `tests/test_owner_risk_evidence.py`. Use a GitHub issue-comment fixture
whose body contains exactly one fenced `json` object followed by explanatory
prose. Test `parse_owner_decision`, `verify_owner_comment`, and
`build_external_evidence`. The valid structured object shall be:

```python
{
    "decision_type": "owner_risk_acceptance",
    "sha": "d" * 40,
    "mapping_set_ids": list(EXPECTED_MAPPING_SETS),
    "disposition": "accepted_for_working_draft",
    "qualified_review_status": "deferred",
    "scope": "complete_git_tracked_repository",
    "lifecycle": "draft",
    "claims_not_made": sorted(CLAIMS_NOT_MADE),
}
```

Write one mutation case for each of: missing/deleted input, more than one JSON
block, malformed JSON, wrong SHA, missing/duplicate/extra mapping-set ID, wrong
scope, wrong lifecycle, incomplete/extra prohibited claim, wrong decision type,
wrong disposition, completed review status, wrong repository URL, nonnumeric or
boolean comment/user ID, wrong login, non-`OWNER` association, invalid
timestamps, publication-date mismatch, body digest mismatch after an edit, and
an assembly input whose technical/editorial/rendering/governance comment or PR
check/merge field is absent.

Prove that `build_external_evidence` emits the complete v1 top level, three
owner decisions, owner scope, exact fetched source copied identically into all
four owner objects, and every supplied non-owner verdict. Prove
`refresh_taggable_evidence` preserves all closure-head objects, replaces only
the refreshed owner source, and adds exact `merge_head`/`post_merge` evidence.

- [ ] **Step 7: Run the focused tests and confirm RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_gates tests.test_owner_risk_evidence -v
```

Expected: new tests fail because the validator still requires `mapping_reviews`
and the controller module does not exist.

- [ ] **Step 8: Implement strict shared validators and basis dispatch**

In `tools/release_gates.py`, add:

```python
MAPPING_DECISION_SCHEMA = "esaf-mapping-decisions-v1"
MAPPING_DECISION_BASES = {"qualified_approval", "owner_risk_acceptance"}
CLAIMS_NOT_MADE = {
    "compliance",
    "certification",
    "equivalence",
    "endorsement",
    "external_scheme_approval",
    "assurance",
    "production_readiness",
}
OWNER_REPOSITORY = "tdistress/ESAF"
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


def _rfc3339(value: object) -> datetime | None:
    if not isinstance(value, str) or not RFC3339_RE.fullmatch(value):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else None
    except ValueError:
        return None


def _publication_date(record: dict[str, object]) -> str | None:
    publication = record.get("publication")
    if not isinstance(publication, dict):
        return None
    return _date_text(publication.get("date"))
```

In `validate_record`, require `mapping_decision_basis` to be a member of
`MAPPING_DECISION_BASES` when `phase == "closure_candidate"`. In
`validate_external_evidence`, require the external top-level basis to equal the
tracked closure record basis before dispatching mapping or scope validation.

Add focused helpers for limitations, source, qualified decisions, owner decisions, and scope. Each helper shall validate only its named responsibility and append deterministic diagnostics. Compare `claims_not_made` as a set while also requiring a list of seven unique strings. Require the owner-source body digest to match `[0-9a-f]{64}`, not a particular synthetic value.

Compare timestamp dates with
`timestamp.astimezone(timezone.utc).date().isoformat()`. Add a crossing-midnight
offset test such as `2026-07-23T23:30:00-02:00`, whose UTC date is
`2026-07-24`. Numeric GitHub IDs shall satisfy
`isinstance(value, int) and not isinstance(value, bool)`.

Replace the `mapping_reviews` block with `mapping_decision_schema`, `mapping_decision_basis`, and `mapping_decisions` validation. Require exactly one object for each expected ID, and dispatch every object only through the top-level basis. Do not accept legacy `mapping_reviews`.

Dispatch scope validation:

```python
basis = evidence.get("mapping_decision_basis")
if isinstance(evidence.get("scope"), dict) and evidence["scope"].get(
    "approval_basis"
) == "owner_risk_acceptance":
    _validate_owner_scope(errors, record, evidence["scope"], closure_head, basis)
else:
    _candidate_verdict(
        errors, "scope", evidence.get("scope"), closure_head, scope=True
    )
```

Do not alter `_candidate_verdict` for technical, editorial, rendering, or governance. Preserve the exact `authority == "Steering Committee"` check.

- [ ] **Step 9: Implement the deterministic owner-evidence controller**

In `tools/owner_risk_evidence.py`, parse exactly one fenced JSON object. Reject
text with zero or multiple JSON blocks. Verify the object against the exact
values in Step 6. Derive `comment_url`, numeric `comment_id`, author fields,
`created_at`, `updated_at`, and SHA-256 from the fetched GitHub JSON; never
accept those source fields from the structured body.

The CLI build mode shall read the fetched owner and four verdict-comment JSON
files plus `gh pr view` state JSON. Every verdict body shall contain exactly one
fenced JSON object whose SHA, date, disposition, findings, role/authority, and
method/result match its evidence type. Derive the comment URL from the fetched
GitHub response and the check URL/conclusion, exact head, mergeability, and
merge-state fields from PR state. Refuse an output path whose resolved path
lies within the repository root, then write the complete external evidence with
`json.dumps(..., indent=2, sort_keys=True)` and a trailing newline.

Taggable-refresh mode shall require the prior validated closure evidence,
refetched owner JSON, merge head, and post-merge results. It shall refuse to
alter any non-owner closure-head object and shall refresh the identical owner
source in the three decisions and scope before adding merge evidence.

Use `argparse` required arguments exactly as declared in the Task 1 interface.
Return nonzero with one deterministic diagnostic per failed invariant. Do not
make network calls from this helper; the controller plan owns live `gh api`
fetch timing.

- [ ] **Step 10: Run focused tests and inspect the full implementation diff**

Run:

```powershell
python -m unittest tests.test_release_gates tests.test_owner_risk_evidence -v
git diff --check
git diff -- tools/release_gates.py tests/test_release_gates.py `
  tools/owner_risk_evidence.py tests/test_owner_risk_evidence.py
```

Expected: focused tests pass; the diff contains no weakening of technical, editorial, rendering, governance, CI, merge-state, or post-merge gates.

- [ ] **Step 11: Commit the evidence-contract implementation**

Run:

```powershell
git add -- tools/release_gates.py tests/test_release_gates.py `
  tools/owner_risk_evidence.py tests/test_owner_risk_evidence.py
git commit -m "Support explicit mapping decision bases"
```

Expected: one focused commit containing the red-green validator boundary.

---

### Task 2: Reconcile durable metadata and the end-to-end controller

**Files:**
- Modify: `tests/test_release_metadata.py`
- Modify: `project/RELEASE_PLAN.md`
- Modify: `project/BACKLOG.md`
- Modify: `docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md`

**Interfaces:**
- Consumes: Task 1's v1 schema and the amendment precedence rules.
- Produces: durable two-basis release language and exact three-set deferred-review backlog coverage.
- Produces: a fully reconciled publication controller with no conflicting qualified-only clause.
- Preserves: the evidence-candidate readiness record and Unreleased changelog until the separate closure PR.

- [ ] **Step 1: Write fail-first durable metadata tests**

Add constants for the exact mapping IDs and prohibited claims. Assert that the
release plan permits exactly one uniform `qualified_approval` or
`owner_risk_acceptance` basis, says owner acceptance defers rather than
completes qualified review, and keeps governance separate.

Add:

```python
def test_owner_risk_acceptance_retains_exact_mapping_review_backlog(self) -> None:
    backlog = read_repository_file("project/BACKLOG.md")
    item = next(
        value for value in markdown_list_items(backlog)
        if "Complete deferred qualified review for the 0.4-alpha mapping snapshots" in value
    )
    for mapping_set_id in EXPECTED_MAPPING_SET_IDS:
        self.assertIn(mapping_set_id, item)
```

Assert that the current readiness record remains `evidence_candidate` and
`CHANGELOG.md` remains Unreleased in this amendment PR.

- [ ] **Step 2: Write fail-first controller consistency tests**

Read `docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md` and
assert:

```python
self.assertIn("mapping_decision_schema: esaf-mapping-decisions-v1", plan)
self.assertIn("mapping_decision_basis", plan)
self.assertIn("owner_risk_acceptance", plan)
self.assertIn("qualified_approval", plan)
self.assertNotIn("three qualified mapping reaffirmations", plan)
self.assertNotIn("Pending: qualified mapping-set and scope approvals", plan)
self.assertNotIn("mapping_reviews", plan)
```

Also assert exact instructions for a new closure-head owner comment; fetched
GitHub source before construction, immediately before merge, and immediately
before tag; SHA-256 body comparison; separate Steering Committee approval;
exact-head technical, editorial, and rendering verdicts with HTTPS locators;
basis-specific tag/issue wording; exact three-ID backlog retention; and the
original five-file closure allowlist.

- [ ] **Step 3: Run focused tests and confirm RED**

Run:

```powershell
python -m unittest tests.test_release_metadata -v
```

Expected: failures identify qualified-only durable wording, missing exact
deferred-review backlog coverage, and conflicting controller clauses.

- [ ] **Step 4: Update durable release plan and backlog**

Change the durable gate list and 0.4-alpha mapping row so the mapping gate uses
exactly one uniform basis: completed qualified approval or disclosed
repository-owner risk acceptance for a Working Draft. State that owner
acceptance defers qualified review and does not supply qualification. Keep
Steering Committee governance separate.

Add exactly:

```markdown
- Complete deferred qualified review for the 0.4-alpha mapping snapshots: `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`, `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`, and `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`.
```

- [ ] **Step 5: Reconcile every conflicting original-plan clause**

Update the original plan's file map, Task 1 fixtures/schema prose, Task 4
interfaces and PR-A wording, Tasks 5-7 interfaces and templates,
external-evidence construction, final issue evidence, tag message, and stop
conditions. Preserve the original evidence-only closure allowlist and require a
fresh closure branch from amended `main`.

The controller shall use `tools/owner_risk_evidence.py` and temporary fetched
JSON inputs. It shall require owner, technical, editorial, rendering,
governance, CI, merge-state, and post-merge evidence with the exact fields
enforced by `tools/release_gates.py`.

- [ ] **Step 6: Run focused tests and legacy-clause scan**

Run:

```powershell
python -m unittest tests.test_release_metadata tests.test_release_gates `
  tests.test_owner_risk_evidence -v
rg -n "mapping_reviews|three qualified mapping|Pending: qualified mapping-set|qualified mapping reaffirmations" `
  docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md
git diff --check
```

Expected: tests pass and the scan returns no conflicting legacy clause.

- [ ] **Step 7: Commit durable metadata and controller reconciliation**

Run:

```powershell
git add -- project/RELEASE_PLAN.md project/BACKLOG.md `
  docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md `
  tests/test_release_metadata.py
git commit -m "Reconcile owner risk publication workflow"
```

---

### Task 3: Review, publish, and merge the amendment PR

**Files:**
- No additional planned tracked changes.
- Create outside repository: amendment PR body and reviewer scratch files.

**Interfaces:**
- Consumes: Tasks 1-2 on the amendment branch.
- Produces: independently approved, merged amendment PR and an amended clean `main`.

- [ ] **Step 1: Run the complete amendment validation suite**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$amendmentBase = (git merge-base HEAD origin/main).Trim()
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref $amendmentBase
python tools/validate_links.py --check
python tools/release_gates.py --check
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md
git diff --check "$amendmentBase..HEAD"
$cacheDirs = @(Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue)
if ($cacheDirs.Count -ne 0) { throw "Cache directories found: $($cacheDirs.Count)" }
```

Expected: all tests and validators pass, mapping totals remain 3 sets / 404
provisions / 81 relationship legs / 325 negative dispositions, Mermaid
inventory remains 23 blocks, and no cache exists.

- [ ] **Step 2: Obtain independent exact-head amendment reviews**

Dispatch separate specification/security and implementation reviewers. They
shall inspect the complete branch diff and exact head, both-basis parity,
owner-source fail-closed behavior, unmodified global gates, durable wording,
backlog retention, original-plan reconciliation, and confirmation that the
future closure PR remains evidence-only.

Resolve every Critical and Important finding with a focused red-green cycle,
rerun affected gates, and redispatch both reviews on the new head.

- [ ] **Step 3: Rename the local branch, push, and open the amendment PR**

```powershell
git branch -m agent/v04-alpha-owner-risk-acceptance
$amendmentHead = (git rev-parse HEAD).Trim()
git push -u origin agent/v04-alpha-owner-risk-acceptance
$amendmentBody = @"
Amends the 0.4-alpha publication evidence model after merged PR #50.

Head: $amendmentHead
Adds two uniform mapping-decision bases without treating repository-owner risk
acceptance as qualified review. Adds deterministic source verification,
preserves Steering Committee governance and every exact-SHA/global gate, and
retains deferred qualified-review backlog coverage for all three exact mapping
sets.

This PR does not close publication gates or authorize tag v0.4-alpha.
"@
gh pr create --repo tdistress/ESAF --base main `
  --head agent/v04-alpha-owner-risk-acceptance `
  --title "Add owner risk acceptance publication evidence" `
  --body $amendmentBody
```

- [ ] **Step 4: Verify and merge the amendment PR**

Run:

```powershell
function Assert-NativeSuccess([string]$operation) {
  if ($LASTEXITCODE -ne 0) { throw "$operation failed with exit $LASTEXITCODE" }
}
$amendmentPr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-owner-risk-acceptance --json number --jq '.number'
Assert-NativeSuccess 'Resolve amendment PR'
gh pr checks --repo tdistress/ESAF $amendmentPr
Assert-NativeSuccess 'Amendment required checks'
$amendmentHead = (git rev-parse HEAD).Trim()
Assert-NativeSuccess 'Resolve reviewed amendment head'
$amendmentState = gh pr view --repo tdistress/ESAF $amendmentPr `
  --json headRefOid,mergeable,mergeStateStatus,statusCheckRollup |
  ConvertFrom-Json
Assert-NativeSuccess 'Fetch amendment PR state'
if ($amendmentState.headRefOid -ne $amendmentHead) {
  throw 'Amendment PR head differs from reviewed local head'
}
if ($amendmentState.mergeable -ne 'MERGEABLE' -or `
    $amendmentState.mergeStateStatus -ne 'CLEAN') {
  throw 'Amendment PR is not cleanly mergeable'
}
if (@(git status --porcelain).Count -ne 0) {
  throw 'Amendment worktree changed after review'
}
gh pr merge --repo tdistress/ESAF $amendmentPr --merge
Assert-NativeSuccess 'Merge amendment PR'
gh pr view --repo tdistress/ESAF $amendmentPr `
  --json state,mergedAt,mergeCommit,headRefOid
Assert-NativeSuccess 'Verify amendment merge'
```

Expected: required checks pass, head equals reviewed `$amendmentHead`, mergeable
state is clean, and PR state becomes `MERGED`.

- [ ] **Step 5: Fast-forward and validate amended main**

From the main worktree, pull with `--ff-only`, rerun the full suite and all
validators, verify clean status, and capture `$amendmentMerge`. Only after this
passes may Task 4 create a fresh closure branch and worktree.

```powershell
git pull --ff-only origin main
$env:PYTHONDONTWRITEBYTECODE='1'
$amendmentMerge = (git rev-parse HEAD).Trim()
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python tools/release_gates.py --check
git diff --check
if (@(git status --porcelain).Count -ne 0) {
  throw 'Amended main is not clean'
}
```

- [ ] **Step 6: Remove the merged amendment worktree**

From the main worktree, resolve
`.worktrees/agent-v04-alpha-publication-gates-closure`, prove its absolute path
is below the main repository's `.worktrees` directory, and remove it with
`git worktree remove`. Prune registrations, delete merged local branch
`agent/v04-alpha-owner-risk-acceptance`, and delete its remote branch. This
releases the closure worktree path for Task 4.

```powershell
$mainRoot = (Get-Location).Path
$worktreeRoot = [IO.Path]::GetFullPath(
  (Join-Path $mainRoot '.worktrees')
) + [IO.Path]::DirectorySeparatorChar
$amendmentWorktree = [IO.Path]::GetFullPath(
  (Join-Path $mainRoot '.worktrees\agent-v04-alpha-publication-gates-closure')
)
if (-not $amendmentWorktree.StartsWith(
  $worktreeRoot, [StringComparison]::OrdinalIgnoreCase
)) { throw 'Amendment worktree resolved outside .worktrees' }
git -C $mainRoot worktree remove $amendmentWorktree
git -C $mainRoot worktree prune
git -C $mainRoot branch -d agent/v04-alpha-owner-risk-acceptance
if (git -C $mainRoot ls-remote --heads origin `
  agent/v04-alpha-owner-risk-acceptance) {
  git -C $mainRoot push origin --delete agent/v04-alpha-owner-risk-acceptance
}
```

---

### Task 4: Build, approve, and merge the evidence-only closure PR

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `project/RELEASE_PLAN.md`
- Modify: `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md`
- Modify: `tests/test_release_metadata.py`
- Modify: `tests/test_release_gates.py`
- Create outside repository: fetched comment/verdict JSON, controller inputs JSON, and external evidence JSON.

**Interfaces:**
- Consumes: amended clean `main`, merged PR A, and the five-file closure allowlist.
- Produces: exact-head technical, editorial, rendering, owner mapping/scope, and Steering Committee evidence plus merged closure PR B.

- [ ] **Step 1: Create a fresh isolated closure worktree**

Use required sub-skill `superpowers:using-git-worktrees`. From clean amended
`main`, create branch `agent/v04-alpha-publication-gates-closure` in
`.worktrees/agent-v04-alpha-publication-gates-closure`. Confirm its merge base
equals `$amendmentMerge` and its status is clean.

- [ ] **Step 2: Write fail-first closure-state tests**

In the two allowed focused test modules, assert the readiness record becomes
`closure_candidate`, declares `mapping_decision_basis:
owner_risk_acceptance`, uses the current UTC conditional date, has all gates
`ready` with HTTPS evidence, and contains all owner-risk/deferred/Draft
limitations. Generalize the changelog parser to accept the conditional dated
heading. Assert the changelog and release-plan closure wording contain no
completed-qualified-review claim.

Run the two focused modules and confirm failures against amended main.

- [ ] **Step 3: Apply the five-file closure state and commit**

Capture `$publicationDate = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')`
once. Use `apply_patch` to insert that exact captured value into the readiness
front matter and changelog heading. Move all eight tracked gates to `ready`
with stable HTTPS PR/issue/review locators. Add the complete owner-risk
disclosure and limitations. Do not store a commit SHA in tracked content.

Run focused tests, `python tools/release_gates.py --check --baseline-ref
origin/main`, and `git diff --check`. Verify the diff contains exactly the five
declared paths, then commit with message `Close 0.4-alpha gates conditionally`.

- [ ] **Step 4: Push and open draft closure PR B**

Resolve all values in this block:

```powershell
$closureHead = (git rev-parse HEAD).Trim()
git push -u origin agent/v04-alpha-publication-gates-closure
$closureBody = @"
Continues #39 after merged evidence PR #50 and the mapping-decision amendment.

Closure candidate: $closureHead
Mapping decision basis: owner_risk_acceptance.
Qualified mapping review is deferred; repository-owner risk acceptance is the
proposed Working Draft publication basis. All mapping snapshots remain Draft.
No compliance, certification, equivalence, endorsement, external-scheme
approval, assurance, production-readiness, or qualified-review claim is made.
"@
gh pr create --repo tdistress/ESAF --base main `
  --head agent/v04-alpha-publication-gates-closure `
  --title "Close 0.4-alpha publication gates conditionally" `
  --body $closureBody --draft
```

- [ ] **Step 5: Obtain and publish three exact-head independent verdicts**

Dispatch distinct technical, editorial, and rendering reviewers on the exact
PR head. Rendering shall re-run the digest-bound 23-block inventory, verify it
matches the PR-A ledger, render all blocks with Mermaid CLI 11.16.0, and record
readability. Each verdict shall contain reviewer identity, exact SHA, current
UTC date, `disposition: approved`, Critical 0, Important 0, method/result, and
inventory digest where applicable.

Each posted verdict shall contain exactly one fenced JSON object. Technical and
editorial objects use keys `sha`, `reviewer`, `date`, `disposition`,
`critical`, `important`, and `result`. Rendering adds `inventory_digest`,
`rendered_blocks: 23`, and `mermaid_cli: 11.16.0`.

Post each final verdict to PR B with `gh api -X POST
repos/tdistress/ESAF/issues/$closurePr/comments -F "body=@$verdictPath"` and
save returned JSON at fixed temporary names
`esaf-v04-technical-response.json`, `esaf-v04-editorial-response.json`, and
`esaf-v04-rendering-response.json`. Capture each numeric comment ID and
immutable HTTPS URL. Any tracked correction invalidates all three verdicts and
requires redispatch.

```powershell
$closurePr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-publication-gates-closure --json number --jq '.number'
$temp = [IO.Path]::GetTempPath()
$technicalVerdictPath = Join-Path $temp 'esaf-v04-technical-verdict.md'
$editorialVerdictPath = Join-Path $temp 'esaf-v04-editorial-verdict.md'
$renderingVerdictPath = Join-Path $temp 'esaf-v04-rendering-verdict.md'
$verdicts = @(
  @{name='technical'; path=$technicalVerdictPath},
  @{name='editorial'; path=$editorialVerdictPath},
  @{name='rendering'; path=$renderingVerdictPath}
)
foreach ($verdict in $verdicts) {
  $response = gh api -X POST `
    "repos/tdistress/ESAF/issues/$closurePr/comments" `
    -F "body=@$($verdict.path)"
  $responsePath = Join-Path ([IO.Path]::GetTempPath()) `
    "esaf-v04-$($verdict.name)-response.json"
  $response | Set-Content -LiteralPath $responsePath -Encoding utf8
  $comment = $response | ConvertFrom-Json
  if ($comment.id -isnot [long] -and $comment.id -isnot [int]) {
    throw "$($verdict.name) comment ID is not numeric"
  }
  if (-not ([string]$comment.html_url).StartsWith('https://')) {
    throw "$($verdict.name) comment URL is not HTTPS"
  }
}
```

- [ ] **Step 6: Post and capture the structured owner decision**

Resolve `$closurePr` and `$closureHead` anew. Build a temporary body containing
one fenced JSON object with the exact Task 1 Step 6 structure and literal
closure SHA, followed by the explicit residual-risk acceptance sentence. Post
from the authenticated repository-owner account:

````powershell
$closurePr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-publication-gates-closure --json number --jq '.number'
$closureHead = gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid --jq '.headRefOid'
$ownerCommentPath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-owner-comment.md'
$ownerCommentBody = @"
ESAF 0.4-alpha Working Draft mapping and scope decision

```json
{
  "decision_type": "owner_risk_acceptance",
  "sha": "$closureHead",
  "mapping_set_ids": [
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0"
  ],
  "disposition": "accepted_for_working_draft",
  "qualified_review_status": "deferred",
  "scope": "complete_git_tracked_repository",
  "lifecycle": "draft",
  "claims_not_made": [
    "assurance",
    "certification",
    "compliance",
    "endorsement",
    "equivalence",
    "external_scheme_approval",
    "production_readiness"
  ]
}
```

As repository owner, I accept the residual risk from unavailable qualified
mapping review for this Working Draft only. This is not qualified review,
external-scheme approval, assurance, compliance, certification, equivalence,
endorsement, or production readiness.
"@
$ownerCommentBody | Set-Content -LiteralPath $ownerCommentPath -Encoding utf8
$ownerResponsePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-owner-response.json'
$ownerResponse = gh api -X POST `
  "repos/tdistress/ESAF/issues/$closurePr/comments" `
  -F "body=@$ownerCommentPath"
$ownerResponse | Set-Content -LiteralPath $ownerResponsePath -Encoding utf8
$ownerCommentId = ($ownerResponse | ConvertFrom-Json).id
if ($ownerCommentId -isnot [long] -and $ownerCommentId -isnot [int]) {
  throw 'Owner comment ID is not numeric'
}
````

Do not reuse the generic PR-A comment.

- [ ] **Step 7: Wait for CI and fetch exact live PR state**

Resolve `$closurePr` and immutable local head anew, mark the draft ready, wait
for required checks, and fetch:

```powershell
function Assert-NativeSuccess([string]$operation) {
  if ($LASTEXITCODE -ne 0) { throw "$operation failed with exit $LASTEXITCODE" }
}
$closurePr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-publication-gates-closure --json number --jq '.number'
Assert-NativeSuccess 'Resolve closure PR'
$closureHead = (git rev-parse HEAD).Trim()
Assert-NativeSuccess 'Resolve immutable closure head'
gh pr ready --repo tdistress/ESAF $closurePr
Assert-NativeSuccess 'Mark closure PR ready'
gh pr checks --repo tdistress/ESAF $closurePr --watch
Assert-NativeSuccess 'Closure required checks'
$prState = gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid,mergeable,mergeStateStatus,statusCheckRollup,isDraft |
  ConvertFrom-Json
Assert-NativeSuccess 'Fetch closure PR state'
if ($prState.isDraft -ne $false) { throw 'Closure PR is still draft' }
if ($prState.headRefOid -ne $closureHead) { throw 'Closure PR head changed' }
if ($prState.mergeable -ne 'MERGEABLE' -or `
    $prState.mergeStateStatus -ne 'CLEAN') {
  throw 'Closure PR is not cleanly mergeable'
}
```

Require exact head, successful required check URL, `mergeable: MERGEABLE`, and
`mergeStateStatus: CLEAN`.

- [ ] **Step 8: Obtain Steering Committee approval last**

After reviews, owner source, CI, and clean merge state pass, obtain a separate
Steering Committee comment containing approver, authority, exact closure SHA,
current UTC date, `disposition: approved`, conditional tag rule, and Draft
limitations. Post through `gh api` and save the returned JSON/URL outside the
repository as `esaf-v04-governance-response.json`. It shall not be the owner
mapping/scope comment.

Its fenced JSON object shall use keys `sha`, `approver`, `authority` with exact
value `Steering Committee`, `date`, `disposition`, and `condition` with exact
value `remote_annotated_tag_matches_exact_validated_commit`.

```powershell
$closurePr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-publication-gates-closure --json number --jq '.number'
$governanceVerdictPath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-governance-verdict.md'
$governanceResponse = gh api -X POST `
  "repos/tdistress/ESAF/issues/$closurePr/comments" `
  -F "body=@$governanceVerdictPath"
$governanceResponsePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-governance-response.json'
$governanceResponse |
  Set-Content -LiteralPath $governanceResponsePath -Encoding utf8
```

- [ ] **Step 9: Fetch sources and build complete closure evidence**

Re-resolve PR number/head and fetch every comment by numeric ID with `gh api
repos/tdistress/ESAF/issues/comments/{id}` into fixed temporary JSON paths.
Fetch PR state to a fixed temporary JSON path. Then run:

```powershell
$closurePr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-publication-gates-closure --json number --jq '.number'
$closureHead = gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid --jq '.headRefOid'
$ownerResponsePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-owner-response.json'
$ownerCommentId = [long](
  Get-Content -Raw -LiteralPath $ownerResponsePath | ConvertFrom-Json
).id
$ownerFetchedPath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-owner-fetched.json'
gh api "repos/tdistress/ESAF/issues/comments/$ownerCommentId" |
  Set-Content -LiteralPath $ownerFetchedPath -Encoding utf8
$technicalFetchedPath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-technical-fetched.json'
$editorialFetchedPath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-editorial-fetched.json'
$renderingFetchedPath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-rendering-fetched.json'
$governanceFetchedPath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-governance-fetched.json'
$technicalResponsePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-technical-response.json'
$editorialResponsePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-editorial-response.json'
$renderingResponsePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-rendering-response.json'
$governanceResponsePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-governance-response.json'
$technicalCommentId = [long](
  Get-Content -Raw -LiteralPath $technicalResponsePath | ConvertFrom-Json
).id
$editorialCommentId = [long](
  Get-Content -Raw -LiteralPath $editorialResponsePath | ConvertFrom-Json
).id
$renderingCommentId = [long](
  Get-Content -Raw -LiteralPath $renderingResponsePath | ConvertFrom-Json
).id
$governanceCommentId = [long](
  Get-Content -Raw -LiteralPath $governanceResponsePath | ConvertFrom-Json
).id
gh api "repos/tdistress/ESAF/issues/comments/$technicalCommentId" |
  Set-Content -LiteralPath $technicalFetchedPath -Encoding utf8
gh api "repos/tdistress/ESAF/issues/comments/$editorialCommentId" |
  Set-Content -LiteralPath $editorialFetchedPath -Encoding utf8
gh api "repos/tdistress/ESAF/issues/comments/$renderingCommentId" |
  Set-Content -LiteralPath $renderingFetchedPath -Encoding utf8
gh api "repos/tdistress/ESAF/issues/comments/$governanceCommentId" |
  Set-Content -LiteralPath $governanceFetchedPath -Encoding utf8
$prStatePath = Join-Path ([IO.Path]::GetTempPath()) 'esaf-v04-pr-state.json'
gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid,mergeable,mergeStateStatus,statusCheckRollup |
  Set-Content -LiteralPath $prStatePath -Encoding utf8
$publicationDate = python -c "from pathlib import Path; from tools.release_gates import load_front_matter; print(load_front_matter(Path('docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md'))['publication']['date'])"
$verifiedAt = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$externalEvidence = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-closure-external-evidence.json'
python tools/owner_risk_evidence.py --comment-json $ownerFetchedPath `
  --technical-comment-json $technicalFetchedPath `
  --editorial-comment-json $editorialFetchedPath `
  --rendering-comment-json $renderingFetchedPath `
  --governance-comment-json $governanceFetchedPath `
  --pr-state-json $prStatePath --expected-head $closureHead `
  --publication-date $publicationDate --verified-at $verifiedAt `
  --output $externalEvidence
$closureBase = (git merge-base HEAD origin/main).Trim()
python tools/release_gates.py --check --baseline-ref $closureBase `
  --external-evidence $externalEvidence --expected-head $closureHead `
  --phase closure
```

- [ ] **Step 10: Immediately refresh every live source and merge**

In one uninterrupted controller block, re-resolve PR number/head; re-fetch the
owner, technical, editorial, rendering, and governance comments; refetch check
rollup, `mergeable`, and `mergeStateStatus`; rebuild inputs/evidence with a new
`verifiedAt`; rerun offline closure validation; confirm clean local status; and
merge without another PR-state mutation:

```powershell
function Assert-NativeSuccess([string]$operation) {
  if ($LASTEXITCODE -ne 0) { throw "$operation failed with exit $LASTEXITCODE" }
}
$closurePr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-publication-gates-closure --json number --jq '.number'
Assert-NativeSuccess 'Resolve closure PR before merge'
$localClosureHead = (git rev-parse HEAD).Trim()
Assert-NativeSuccess 'Resolve immutable local closure head'
$closureHead = gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid --jq '.headRefOid'
Assert-NativeSuccess 'Resolve remote closure head'
if ($closureHead -ne $localClosureHead) { throw 'PR head differs from reviewed head' }
$temp = [IO.Path]::GetTempPath()
$responseNames = @('owner','technical','editorial','rendering','governance')
$fetched = @{}
foreach ($name in $responseNames) {
  $responsePath = Join-Path $temp "esaf-v04-$name-response.json"
  $commentId = [long](
    Get-Content -Raw -LiteralPath $responsePath | ConvertFrom-Json
  ).id
  $fetchedPath = Join-Path $temp "esaf-v04-$name-prefetch-merge.json"
  gh api "repos/tdistress/ESAF/issues/comments/$commentId" |
    Set-Content -LiteralPath $fetchedPath -Encoding utf8
  Assert-NativeSuccess "Refetch $name comment"
  $fetched[$name] = $fetchedPath
}
$prStatePath = Join-Path $temp 'esaf-v04-pr-state-prefetch-merge.json'
gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid,mergeable,mergeStateStatus,statusCheckRollup |
  Set-Content -LiteralPath $prStatePath -Encoding utf8
Assert-NativeSuccess 'Refetch closure PR state'
$state = Get-Content -Raw -LiteralPath $prStatePath | ConvertFrom-Json
if ($state.headRefOid -ne $closureHead) { throw 'PR head changed' }
if ($state.mergeable -ne 'MERGEABLE') { throw 'PR is not mergeable' }
if ($state.mergeStateStatus -ne 'CLEAN') { throw 'PR merge state is not clean' }
$publicationDate = python -c "from pathlib import Path; from tools.release_gates import load_front_matter; print(load_front_matter(Path('docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md'))['publication']['date'])"
Assert-NativeSuccess 'Read conditional publication date'
$verifiedAt = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$externalEvidence = Join-Path $temp 'esaf-v04-closure-external-evidence.json'
if (Test-Path -LiteralPath $externalEvidence) {
  Remove-Item -LiteralPath $externalEvidence
}
python tools/owner_risk_evidence.py --comment-json $fetched.owner `
  --technical-comment-json $fetched.technical `
  --editorial-comment-json $fetched.editorial `
  --rendering-comment-json $fetched.rendering `
  --governance-comment-json $fetched.governance `
  --pr-state-json $prStatePath --expected-head $closureHead `
  --publication-date $publicationDate --verified-at $verifiedAt `
  --output $externalEvidence
Assert-NativeSuccess 'Rebuild closure evidence'
$closureBase = (git merge-base HEAD origin/main).Trim()
Assert-NativeSuccess 'Resolve closure baseline'
python tools/release_gates.py --check --baseline-ref $closureBase `
  --external-evidence $externalEvidence --expected-head $closureHead `
  --phase closure
Assert-NativeSuccess 'Validate refreshed closure evidence'
if (@(git status --porcelain).Count -ne 0) {
  throw 'Closure worktree changed after approval'
}
gh pr merge --repo tdistress/ESAF $closurePr --merge
Assert-NativeSuccess 'Merge closure PR'
$mergedState = gh pr view --repo tdistress/ESAF $closurePr `
  --json state,mergedAt,mergeCommit,headRefOid | ConvertFrom-Json
Assert-NativeSuccess 'Verify closure merge'
if ($mergedState.state -ne 'MERGED') { throw 'Closure PR did not merge' }
```

Any source edit/deletion, digest mismatch, head change, check regression,
non-clean merge state, or local tracked change stops the block before merge.

---

### Task 5: Validate merged main, publish the tag, close issue #39, and clean up

**Files:**
- No tracked file changes.
- Modify outside repository: `esaf-v04-closure-external-evidence.json`.

**Interfaces:**
- Consumes: merged PR B, exact `$closureMerge`, immutable owner source, conditional UTC publication date, and every post-merge result.
- Produces: validated taggable evidence, remote annotated `v0.4-alpha` tag, consolidated issue evidence, closed issue #39, and clean `main`.

- [ ] **Step 1: Update local main and verify exact merge identity**

Run:

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
git -C $mainRoot pull --ff-only origin main
Set-Location -LiteralPath $mainRoot
$closureMerge = (git rev-parse HEAD).Trim()
$remoteMain = (git rev-parse origin/main).Trim()
if ($closureMerge -ne $remoteMain) { throw 'Local main and origin/main differ' }
$publicationDate = python -c "from pathlib import Path; from tools.release_gates import load_front_matter; print(load_front_matter(Path('docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md'))['publication']['date'])"
if ((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd') -ne $publicationDate.Trim()) {
  throw 'Conditional publication date expired; create and review a new closure candidate'
}
```

- [ ] **Step 2: Run every post-merge gate on unchanged merged main**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$closureMerge = (git rev-parse HEAD).Trim()
$evidenceMerge = (git rev-parse 'HEAD^1').Trim()
function Invoke-RecordedGate {
  param([string]$Name, [string]$Executable, [string[]]$Arguments)
  $output = @(& $Executable @Arguments 2>&1)
  $output | ForEach-Object { Write-Host $_ }
  if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit $LASTEXITCODE" }
  $summary = ($output | Where-Object {
    -not [string]::IsNullOrWhiteSpace([string]$_)
  } | Select-Object -Last 1)
  if ([string]::IsNullOrWhiteSpace([string]$summary)) {
    $summary = "$Name passed"
  }
  return @{name = $Name; exit_code = 0; result = [string]$summary}
}
$commands = @()
$commands += Invoke-RecordedGate 'full_suite' 'python' `
  @('-m','unittest','discover','-s','tests','-v')
$commands += Invoke-RecordedGate 'controls' 'python' `
  @('tools/validate_controls.py','--check')
$commands += Invoke-RecordedGate 'architectures' 'python' `
  @('tools/validate_architectures.py')
$commands += Invoke-RecordedGate 'migration' 'python' `
  @('tools/migrate_control_mappings.py','--check')
$commands += Invoke-RecordedGate 'crosswalk_current' 'python' `
  @('tools/validate_crosswalks.py','--check')
$commands += Invoke-RecordedGate 'crosswalk_baseline' 'python' `
  @('tools/validate_crosswalks.py','--check','--baseline-ref',$evidenceMerge)
$commands += Invoke-RecordedGate 'links' 'python' `
  @('tools/validate_links.py','--check')
$commands += Invoke-RecordedGate 'release_record' 'python' `
  @('tools/release_gates.py','--check','--baseline-ref',$evidenceMerge)
$commands += Invoke-RecordedGate 'mermaid_inventory' 'python' `
  @('tools/mermaid_inventory.py','--check-record',
    'docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md')
$commands += Invoke-RecordedGate 'whole_range_diff' 'git' `
  @('diff','--check',"$evidenceMerge..HEAD")
$cacheDirs = @(Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue)
if ($cacheDirs.Count -ne 0) { throw "Cache directories found: $($cacheDirs.Count)" }
$commands += @{name='cache_count'; exit_code=0; result='0 cache directories'}
if (@(git status --porcelain).Count -ne 0) { throw 'Merged main is not clean' }
$commands += @{name='clean_status'; exit_code=0; result='clean working tree'}
$postMergePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-post-merge.json'
@{sha=$closureMerge; commands=$commands} | ConvertTo-Json -Depth 6 |
  Set-Content -LiteralPath $postMergePath -Encoding utf8
```

Expected: every command succeeds on `$closureMerge`.

- [ ] **Step 3: Add post-merge evidence and validate the two SHA domains**

Resolve `$closureMerge` and create a temporary post-merge JSON object with
`sha: $closureMerge` and exactly one successful nonempty result for
`full_suite`, `controls`, `architectures`, `migration`, `crosswalk_current`,
`crosswalk_baseline`, `links`, `release_record`, `mermaid_inventory`,
`whole_range_diff`, `cache_count`, and `clean_status`. Use the exact observed
results from Step 2, not predicted totals.

Do not mutate the validated closure evidence yet.

- [ ] **Step 4: Atomically refresh, validate, create, and push the tag**

Run one uninterrupted guarded PowerShell block that resolves every variable
inside the block:

```powershell
function Assert-NativeSuccess([string]$operation) {
  if ($LASTEXITCODE -ne 0) { throw "$operation failed with exit $LASTEXITCODE" }
}
$externalEvidence = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-closure-external-evidence.json'
$taggableEvidence = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-taggable-external-evidence.json'
$postMergePath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-post-merge.json'
$baseEvidence = Get-Content -Raw -LiteralPath $externalEvidence | ConvertFrom-Json
$closureHead = [string]$baseEvidence.closure_head
$ownerCommentId = [long]$baseEvidence.mapping_decisions[0].source.comment_id
$ownerFetchedPath = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-owner-prefetch-tag.json'
gh api "repos/tdistress/ESAF/issues/comments/$ownerCommentId" |
  Set-Content -LiteralPath $ownerFetchedPath -Encoding utf8
Assert-NativeSuccess 'Refetch owner source before tag'
$closureMerge = (git rev-parse HEAD).Trim()
Assert-NativeSuccess 'Resolve closure merge before tag'
$evidenceMerge = (git rev-parse 'HEAD^1').Trim()
Assert-NativeSuccess 'Resolve evidence baseline before tag'
$publicationDate = python -c "from pathlib import Path; from tools.release_gates import load_front_matter; print(load_front_matter(Path('docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md'))['publication']['date'])"
Assert-NativeSuccess 'Read publication date before tag'
$verifiedAt = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
if (Test-Path -LiteralPath $taggableEvidence) {
  Remove-Item -LiteralPath $taggableEvidence
}
python tools/owner_risk_evidence.py --comment-json $ownerFetchedPath `
  --base-evidence $externalEvidence --expected-head $closureHead `
  --publication-date $publicationDate --verified-at $verifiedAt `
  --merge-head $closureMerge --post-merge-json $postMergePath `
  --output $taggableEvidence
Assert-NativeSuccess 'Build refreshed taggable evidence'
python tools/release_gates.py --check --baseline-ref $evidenceMerge `
  --external-evidence $taggableEvidence --expected-head $closureMerge `
  --phase taggable
Assert-NativeSuccess 'Validate refreshed taggable evidence'
git fetch origin main
Assert-NativeSuccess 'Fetch origin main before tag'
$currentMain = (git rev-parse HEAD).Trim()
Assert-NativeSuccess 'Resolve local main before tag'
$remoteMain = (git rev-parse origin/main).Trim()
Assert-NativeSuccess 'Resolve remote main before tag'
$validatedMerge = [string](
  Get-Content -Raw -LiteralPath $taggableEvidence | ConvertFrom-Json
).merge_head
if ($currentMain -ne $validatedMerge -or $remoteMain -ne $validatedMerge) {
  throw 'HEAD, origin/main, and validated merge differ'
}
if (@(git status --porcelain).Count -ne 0) { throw 'Main worktree is not clean' }
if ((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd') -ne $publicationDate.Trim()) {
  throw 'Conditional publication date expired'
}
if (@(git tag --list 'v0.4-alpha').Count -ne 0) {
  throw 'Local v0.4-alpha already exists'
}
if (@(git ls-remote --tags origin 'refs/tags/v0.4-alpha').Count -ne 0) {
  throw 'Remote v0.4-alpha already exists'
}
$tagMessage = @"
ESAF 0.4-alpha Working Draft

Validated commit: $validatedMerge
Evidence: https://github.com/tdistress/ESAF/issues/39
Mapping decision basis: repository-owner risk acceptance.
Qualified mapping review was deferred; all mapping snapshots remain Draft.
This Working Draft publication makes no compliance, certification, equivalence,
endorsement, external-scheme approval, assurance, production-readiness, or
qualified-review claim.
"@
git tag -a v0.4-alpha $validatedMerge -m $tagMessage
Assert-NativeSuccess 'Create annotated v0.4-alpha tag'
git push origin refs/tags/v0.4-alpha
Assert-NativeSuccess 'Push annotated v0.4-alpha tag'
```

Do not move or recreate the tag if push verification fails.

- [ ] **Step 5: Resolve the remote annotated tag**

Run:

```powershell
function Assert-NativeSuccess([string]$operation) {
  if ($LASTEXITCODE -ne 0) { throw "$operation failed with exit $LASTEXITCODE" }
}
git fetch origin tag v0.4-alpha --force
Assert-NativeSuccess 'Fetch published v0.4-alpha tag'
$validatedMerge = (git rev-parse HEAD).Trim()
Assert-NativeSuccess 'Resolve validated main'
$localPeeled = (git rev-parse 'v0.4-alpha^{commit}').Trim()
Assert-NativeSuccess 'Peel local v0.4-alpha tag'
$remoteRows = @(git ls-remote --tags origin `
  'refs/tags/v0.4-alpha' 'refs/tags/v0.4-alpha^{}')
Assert-NativeSuccess 'Resolve remote v0.4-alpha tag'
$remotePeeled = (($remoteRows | Where-Object { $_ -match '\^\{\}$' }) -split '\s+')[0]
if ($localPeeled -ne $validatedMerge -or $remotePeeled -ne $validatedMerge) {
  throw 'Published tag does not peel to validated closure merge'
}
```

- [ ] **Step 6: Post consolidated evidence and close issue #39**

Build the final comment directly from taggable evidence:

```powershell
function Assert-NativeSuccess([string]$operation) {
  if ($LASTEXITCODE -ne 0) { throw "$operation failed with exit $LASTEXITCODE" }
}
$taggableEvidence = Join-Path ([IO.Path]::GetTempPath()) `
  'esaf-v04-taggable-external-evidence.json'
$evidence = Get-Content -Raw -LiteralPath $taggableEvidence | ConvertFrom-Json
$closurePr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-publication-gates-closure --json number --jq '.number'
Assert-NativeSuccess 'Resolve closure PR for final evidence'
$closure = gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid,mergeCommit | ConvertFrom-Json
Assert-NativeSuccess 'Fetch closure PR identity'
$evidencePr = gh pr view --repo tdistress/ESAF 50 `
  --json headRefOid,mergeCommit | ConvertFrom-Json
Assert-NativeSuccess 'Fetch evidence PR identity'
$tagObject = (git rev-parse v0.4-alpha).Trim()
Assert-NativeSuccess 'Resolve tag object'
$peeled = (git rev-parse 'v0.4-alpha^{commit}').Trim()
Assert-NativeSuccess 'Resolve peeled publication commit'
$commandSummary = ($evidence.post_merge.commands | ForEach-Object {
  "$($_.name): $($_.result)"
}) -join '; '
$owner = $evidence.mapping_decisions[0].source
$mappingIds = ($evidence.mapping_decisions.mapping_set_id -join ', ')
$body = @"
0.4-alpha publication evidence

- Evidence PR #50: head $($evidencePr.headRefOid); merge $($evidencePr.mergeCommit.oid).
- Closure PR #$closurePr: head $($closure.headRefOid); merge $($closure.mergeCommit.oid).
- Tag object $tagObject; peeled commit $peeled.
- Gates: $commandSummary
- Renderer: 23/23 blocks approved on exact closure head; Critical 0; Important 0.
- Mapping decision basis: owner_risk_acceptance; qualified mapping review was deferred.
- Mapping sets: $mappingIds
- Owner source: $($owner.comment_url); comment $($owner.comment_id); body SHA-256 $($owner.body_sha256).
- Governance: separate Steering Committee approval at $($evidence.governance.url).
- Backlog: deferred qualified review retained for all three exact mapping-set IDs.
- Lifecycle: all mappings, architectures, and controls remain Draft. Publication makes no compliance, certification, equivalence, endorsement, external-scheme approval, assurance, production-readiness, or qualified-review claim.
- Findings: Critical 0; Important 0.
"@
gh issue comment 39 --repo tdistress/ESAF --body $body
Assert-NativeSuccess 'Post consolidated issue evidence'
gh issue close 39 --repo tdistress/ESAF --comment `
  "0.4-alpha publication gates are closed; remote annotated tag v0.4-alpha resolves to $peeled."
Assert-NativeSuccess 'Close issue 39'
$issueState = gh issue view 39 --repo tdistress/ESAF --json state |
  ConvertFrom-Json
Assert-NativeSuccess 'Verify issue 39 state'
if ($issueState.state -ne 'CLOSED') { throw 'Issue 39 did not close' }
```

Replace superseded totals or conclusions; do not append contradictory results.

- [ ] **Step 7: Clean owned branches/worktrees and verify final state**

From the main worktree, validate both owned absolute worktree paths before
removal:

```powershell
$mainRoot = (Get-Location).Path
$worktreeRoot = [IO.Path]::GetFullPath(
  (Join-Path $mainRoot '.worktrees')
) + [IO.Path]::DirectorySeparatorChar
$owned = @(
  (Join-Path $mainRoot '.worktrees\agent-v04-alpha-publication-gates-closure')
)
foreach ($path in $owned) {
  $resolved = [IO.Path]::GetFullPath($path)
  if (-not $resolved.StartsWith(
    $worktreeRoot, [StringComparison]::OrdinalIgnoreCase
  )) { throw "Refusing out-of-scope worktree removal: $resolved" }
  if (Test-Path -LiteralPath $resolved) {
    git -C $mainRoot worktree remove $resolved
  }
}
git -C $mainRoot worktree prune
git -C $mainRoot branch -d agent/v04-alpha-publication-gates-closure
if (git -C $mainRoot ls-remote --heads origin `
  agent/v04-alpha-publication-gates-closure) {
  git -C $mainRoot push origin --delete `
    agent/v04-alpha-publication-gates-closure
}
$head = (git -C $mainRoot rev-parse HEAD).Trim()
$remote = (git -C $mainRoot rev-parse origin/main).Trim()
$tagged = (git -C $mainRoot rev-parse 'v0.4-alpha^{commit}').Trim()
if ($head -ne $remote -or $head -ne $tagged) {
  throw 'Final main/tag identities differ'
}
if (@(git -C $mainRoot status --porcelain).Count -ne 0) {
  throw 'Final main is not clean'
}
gh issue view 39 --repo tdistress/ESAF --json state
```

Expected: issue closed; clean main; local main, origin/main, and peeled tag equal;
only unrelated worktrees remain.

## Execution stop conditions

Stop and preserve a clean, recoverable state if:

- any Critical or Important finding remains unresolved;
- any selected-basis statement contradicts the external evidence;
- decision bases are mixed or any expected mapping-set decision is missing, duplicated, or extra;
- the owner comment is missing, edited, deleted, not authored with `OWNER` association, not bound to exact closure head, or differs from its recorded digest or structured content;
- the generic PR-A comment is proposed as substantive mapping or scope evidence;
- Steering Committee governance approval is absent or combined with the owner mapping/scope decision;
- any exact candidate SHA changes after approval without complete affected re-review;
- any Mermaid block fails renderer or readability review;
- any validator, full suite, link, diff, cache, cleanliness, GitHub-check, mergeability, post-merge, publication-date, or tag-identity gate fails;
- any mapping, architecture, or control lifecycle state changes from Draft;
- owner-risk publication wording implies qualified review, scheme approval, compliance, certification, equivalence, endorsement, assurance, or production readiness;
- qualified-review backlog coverage omits any of the three exact mapping-set IDs;
- the amendment diff includes closure-state files, or the closure diff includes
  any path outside its original five-file allowlist;
- external evidence is written inside the repository; or
- the remote tag exists before final validation or does not peel to the exact validated merged-main commit.
