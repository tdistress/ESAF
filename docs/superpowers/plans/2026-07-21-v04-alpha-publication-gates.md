# ESAF 0.4-Alpha Publication-Gate Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish an immutable `v0.4-alpha` Working Draft only after two exact-head pull requests, exhaustive renderer and review evidence, authorized governance approval, and post-merge validation close issue #39 without promoting any Draft artifact.

**Architecture:** The first pull request builds and reviews the substantive evidence candidate. After that merge is validated, a second evidence-only pull request establishes a conditional release record whose publication date becomes effective only when remote annotated tag `v0.4-alpha` resolves to the exact validated closure merge. Tracked Markdown remains authoritative; exact candidate, merge, approval, check, and tag SHAs live in GitHub evidence and the annotated tag so no commit claims to contain its own hash.

**Tech Stack:** Markdown, YAML front matter parsed with PyYAML, Python 3.13 `unittest`, Git, GitHub CLI, PowerShell, pnpm, and `@mermaid-js/mermaid-cli@11.16.0`.

## Global Constraints

- Preserve Protect AI, Utilize AI, and Govern AI and every existing Draft lifecycle state.
- Publish the complete tracked repository at the frozen evidence-candidate head; do not narrow release scope to the current branch diff.
- Treat Cyber Essentials core v3.3, Cyber Essentials Plus v3.2 `esaf_to_external`, and Cyber Essentials Plus v3.2 `external_to_esaf` as three separate Draft mapping snapshots.
- Do not claim compliance, certification, equivalence, endorsement, external-scheme approval, or production readiness.
- Use `shall`, `should`, and `may` according to `STYLE_GUIDE.md` in normative prose.
- Set `PYTHONDONTWRITEBYTECODE=1` for every Python gate and leave no `__pycache__`, renderer output, or scratch evidence in the repository.
- Pin Mermaid rendering to exactly `@mermaid-js/mermaid-cli@11.16.0` and render all 23 baseline blocks; any added block increases that exact candidate count.
- Store renderer outputs and external evidence JSON beneath a verified system temporary directory outside the repository.
- Do not treat repository ownership as governance authority. Publication approval shall identify the Steering Committee role assigned by `GOVERNANCE.md`.
- Mapping decisions shall use exactly one uniform basis for all three snapshots: `qualified_approval` or `owner_risk_acceptance`. Qualified approval identifies reviewer, qualification, scope, exact closure SHA, date, and disposition; owner-risk acceptance is a disclosed Working Draft risk acceptance that defers, rather than completes, qualified review.
- Any tracked candidate change invalidates affected exact-head results and requires the specified reviews and gates to be rerun.
- Resolve every Critical and Important finding before merge. Record accepted Minor findings with owner and rationale.
- No tag shall be created or pushed until the closure merge commit passes every post-merge gate and the conditional publication date is the current UTC date.

### Task 2 amendment precedence: two-basis publication controller

This amendment controls every conflicting clause below. The external-evidence schema is `mapping_decision_schema: esaf-mapping-decisions-v1`; it shall contain `mapping_decision_basis` and exactly three `mapping_decisions`, all using one basis. `qualified_approval` records independently qualified approval. `owner_risk_acceptance` records the repository owner's disclosed Working Draft acceptance and `qualified_review_status: deferred`; it never represents completed qualified review. A separate Steering Committee approval remains mandatory governance evidence.

For owner-risk acceptance, construct evidence with `tools/owner_risk_evidence.py` from temporary fetched JSON inputs and a new closure-head owner comment. Fetch and verify the GitHub source immediately before construction, immediately before merge, and immediately before tag; require a SHA-256 body comparison each time. The controller shall require owner, technical, editorial, rendering, governance, CI, merge-state, and post-merge evidence with the exact fields enforced by `tools/release_gates.py`. The technical, editorial, and rendering evidence shall be exact-head technical, editorial, and rendering verdicts with HTTPS locators.

Retain the exact three-ID deferred-review backlog item for every owner-risk decision: `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`, `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`, and `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`. Task 5 shall create a fresh closure branch from amended `main` and retain the original five-file evidence-only closure allowlist.

The following controller helpers are executable PowerShell contracts. Each
qualified input file is assembled from the freshly fetched exact-head
scope/technical/editorial/rendering/governance/reviewer/check/merge-state
sources before this helper runs; it is temporary and outside the repository.

```powershell
function Assert-OwnerSourceUnchanged($PriorSource, $FetchedComment) {
  $bodyBytes = [Text.Encoding]::UTF8.GetBytes([string]$FetchedComment.body)
  $digest = ([Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bodyBytes))).ToLowerInvariant()
  if ($digest -ne [string]$PriorSource.body_sha256) { throw 'Owner source digest differs from the prior validated source' }
  if ($FetchedComment.id -ne $PriorSource.comment_id -or $FetchedComment.html_url -ne $PriorSource.comment_url) { throw 'Owner source comment identity differs from the prior validated source' }
  if ($FetchedComment.user.login -ne $PriorSource.author_login -or $FetchedComment.user.id -ne $PriorSource.author_user_id -or $FetchedComment.author_association -ne 'OWNER') { throw 'Owner source author identity differs from the prior validated source' }
  if ($FetchedComment.created_at -ne $PriorSource.created_at -or $FetchedComment.updated_at -ne $PriorSource.updated_at) { throw 'Owner source timestamps differ from the prior validated source' }
  return $digest
}

function Get-StructuredCommentBody($Path, $Name) {
  $comment = Get-Content -Raw -LiteralPath $Path | ConvertFrom-Json
  # A qualified decision comment shall contain a JSON object; prose is not evidence.
  try { $body = [string]$comment.body | ConvertFrom-Json }
  catch { throw "$Name comment shall contain a JSON object" }
  if ($comment.id -isnot [long] -or $comment.html_url -notmatch '^https://') {
    throw "$Name comment identity is invalid"
  }
  return [ordered]@{ comment=$comment; body=$body }
}

function New-QualifiedInputFromSources($QualifiedFetchedPaths, $ExpectedCommentIds, $ClosureHead, $PublicationDate, $ScopePath, $TechnicalPath, $EditorialPath, $RenderingPath, $GovernancePath, $PrStatePath, $BaseEvidence = $null) {
  $expectedMappingIds = @(
    'uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0',
    'uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0',
    'uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0'
  )
  $expectedClaims = @('compliance','certification','equivalence','endorsement','external_scheme_approval','assurance','production_readiness')
  if (@($QualifiedFetchedPaths).Count -ne 3 -or @($ExpectedCommentIds).Count -ne 3 -or @($ExpectedCommentIds | Select-Object -Unique).Count -ne 3) {
    throw 'Qualified evidence shall use exactly three fixed qualified comment IDs'
  }
  $qualifiedReviews = @($QualifiedFetchedPaths | ForEach-Object {
    $source = Get-StructuredCommentBody $_ 'qualified decision'
    $comment = $source.comment
    $body = $source.body
    if ([long]$comment.id -notin @($ExpectedCommentIds | ForEach-Object { [long]$_ })) { throw 'Qualified decision comment ID is not one of the fixed response IDs' }
    if ($body.mapping_set_id -notin $expectedMappingIds -or $body.decision_type -ne 'qualified_approval' -or $body.sha -ne $ClosureHead) {
      throw 'Qualified decision mapping ID, type, or closure SHA is invalid'
    }
    if ($body.decided_at -notmatch '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$') {
      throw 'Qualified decision decided_at shall be RFC3339'
    }
    if ([DateTimeOffset]::Parse([string]$body.decided_at).ToUniversalTime().ToString('yyyy-MM-dd') -ne $PublicationDate) {
      throw 'Qualified decision date shall equal the current publication date'
    }
    if ([string]::IsNullOrWhiteSpace([string]$body.reviewer) -or [string]::IsNullOrWhiteSpace([string]$body.qualification) -or $body.disposition -ne 'approved' -or $body.qualified_review_status -ne 'completed') {
      throw 'Qualified decision reviewer, qualification, disposition, or completion status is invalid'
    }
    if ($body.url -ne $comment.html_url -or $body.url -notmatch '^https://') { throw 'Qualified decision evidence URL shall equal fetched comment URL' }
    if ($body.limitations.lifecycle -ne 'draft' -or (($body.limitations.claims_not_made -join ',') -ne ($expectedClaims -join ','))) {
      throw 'Qualified decision limitations shall be the exact Draft claims_not_made set'
    }
    [ordered]@{ mapping_set_id=$body.mapping_set_id; decision_type='qualified_approval'; sha=$body.sha; decided_at=$body.decided_at; reviewer=$body.reviewer; qualification=$body.qualification; disposition=$body.disposition; qualified_review_status=$body.qualified_review_status; url=$body.url; source=[ordered]@{comment_id=[long]$comment.id; comment_url=$comment.html_url} }
  })
  $actualMappingIds = @($qualifiedReviews.mapping_set_id | Sort-Object) -join ','
  $expectedMappingIdList = @($expectedMappingIds | Sort-Object) -join ','
  if ($actualMappingIds -ne $expectedMappingIdList) { throw 'Qualified decisions shall contain exactly the three expected mapping-set IDs' }
  if ($null -ne $BaseEvidence) {
    if ($BaseEvidence.closure_head -ne $ClosureHead) { throw 'Taggable qualified evidence closure head differs from retained closure evidence' }
    $scope = $BaseEvidence.scope; $technical = $BaseEvidence.technical; $editorial = $BaseEvidence.editorial
    $rendering = $BaseEvidence.rendering; $governance = $BaseEvidence.governance
    $githubChecks = $BaseEvidence.github_checks; $mergeState = $BaseEvidence.merge_state
  } else {
    $scope = (Get-StructuredCommentBody $ScopePath 'scope').body
    $technical = (Get-StructuredCommentBody $TechnicalPath 'technical').body
    $editorial = (Get-StructuredCommentBody $EditorialPath 'editorial').body
    $rendering = (Get-StructuredCommentBody $RenderingPath 'rendering').body
    $governance = (Get-StructuredCommentBody $GovernancePath 'governance').body
    $state = Get-Content -Raw -LiteralPath $PrStatePath | ConvertFrom-Json
    if ($state.headRefOid -ne $ClosureHead) { throw 'Qualified evidence PR state is not bound to closure head' }
    $githubChecks = [ordered]@{ expected=@('Validate ESAF sources'); observed=@($state.statusCheckRollup | ForEach-Object { [ordered]@{name=$_.name; sha=$ClosureHead; conclusion=([string]$_.conclusion).ToLowerInvariant(); url=$_.detailsUrl} }) }
    $mergeState = [ordered]@{sha=$ClosureHead; mergeable=($state.mergeable -eq 'MERGEABLE'); state=([string]$state.mergeStateStatus).ToLowerInvariant()}
  }
  return [ordered]@{
    qualified_reviews=$qualifiedReviews; scope=$scope; technical=$technical; editorial=$editorial; rendering=$rendering; governance=$governance
    github_checks=$githubChecks; merge_state=$mergeState
  }
}

function New-QualifiedClosureEvidence($InputPath, $ClosureHead) {
  $input = Get-Content -Raw -LiteralPath $InputPath | ConvertFrom-Json
  $expectedMappingIds = @(
    'uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0',
    'uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0',
    'uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0'
  )
  $limitations = [ordered]@{
    lifecycle = 'draft'
    claims_not_made = @('compliance','certification','equivalence','endorsement','external_scheme_approval','assurance','production_readiness')
  }
  $qualifiedDecisions = @($input.qualified_reviews | ForEach-Object {
    if ($_.mapping_set_id -notin $expectedMappingIds -or $_.sha -ne $ClosureHead -or $_.decision_type -ne 'qualified_approval' -or $_.disposition -ne 'approved' -or $_.qualified_review_status -ne 'completed' -or $_.url -notmatch '^https://' -or [string]::IsNullOrWhiteSpace([string]$_.reviewer) -or [string]::IsNullOrWhiteSpace([string]$_.qualification)) { throw 'Qualified mapping decision is incomplete or not bound to closure head' }
    if ($_.decided_at -notmatch '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$') { throw 'Qualified mapping decision decided_at shall be RFC3339' }
    if ($_.source.comment_id -isnot [long] -or $_.source.comment_url -ne $_.url) { throw 'Qualified mapping decision source is incomplete' }
    [ordered]@{ mapping_set_id=$_.mapping_set_id; decision_type='qualified_approval'; sha=$ClosureHead; decided_at=$_.decided_at; reviewer=$_.reviewer; qualification=$_.qualification; disposition='approved'; qualified_review_status='completed'; url=$_.url; limitations=$limitations; source=$_.source }
  })
  if ($qualifiedDecisions.Count -ne 3) { throw 'Qualified evidence shall contain exactly three mapping decisions' }
  if ((@($qualifiedDecisions.mapping_set_id | Sort-Object) -join ',') -ne (@($expectedMappingIds | Sort-Object) -join ',')) { throw 'Qualified mapping decisions shall contain exactly the three expected mapping-set IDs' }
  $qualifiedScope = [ordered]@{ sha=$ClosureHead; approver=$input.scope.approver; role='release-scope approver'; date=$input.scope.date; disposition='approved'; url=$input.scope.url }
  return [ordered]@{
    closure_head=$ClosureHead; scope=$qualifiedScope; technical=$input.technical; editorial=$input.editorial; rendering=$input.rendering; governance=$input.governance
    mapping_decision_schema = 'esaf-mapping-decisions-v1'; mapping_decision_basis='qualified_approval'; mapping_decisions = $qualifiedDecisions
    github_checks=$input.github_checks; merge_state=$input.merge_state
  }
}

function New-QualifiedTaggableEvidence($InputPath, $ClosureHead, $MergeHead, $PostMergePath) {
  $evidence = New-QualifiedClosureEvidence $InputPath $ClosureHead
  $evidence.merge_head = $MergeHead
  $evidence.post_merge = Get-Content -Raw -LiteralPath $PostMergePath | ConvertFrom-Json
  if ($evidence.post_merge.sha -ne $MergeHead) { throw 'Qualified post-merge evidence is not bound to merged main' }
  return $evidence
}
```

## File and interface map

- `tools/release_gates.py` — parse the authoritative publication-readiness Markdown front matter, validate scope/gates/transitions, reject self-referential SHA fields, and validate external exact-SHA evidence before merge or tag.
- `tools/owner_risk_evidence.py` — verify the fetched repository-owner comment and construct the two-basis external-evidence object without committing temporary source JSON.
- `tests/test_release_gates.py` — unit and mutation tests for release record parsing, four-state transitions, scope, Draft preservation, external approval binding, and tag prohibition.
- `tools/mermaid_inventory.py` — discover every Git-tracked Markdown Mermaid block in deterministic order and emit source digests plus temporary render inputs.
- `tests/test_mermaid_inventory.py` — inventory ordering, digest, fence parsing, mutation, and repository-count tests without invoking the external renderer.
- `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md` — authoritative Markdown release scope and gate record with machine-readable YAML front matter and concise human interpretation.
- `docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md` — exhaustive 23-row renderer/readability ledger owned by the rendering review.
- `docs/superpowers/reviews/2026-07-21-v04-alpha-technical-review.md` — normative and technical exact-head review.
- `docs/superpowers/reviews/2026-07-21-v04-alpha-editorial-review.md` — editorial, terminology, link, and cross-reference exact-head review.
- `tests/test_release_metadata.py` — repository metadata, conditional changelog, backlog, and release-state invariants.
- `CHANGELOG.md`, `project/RELEASE_PLAN.md`, `project/BACKLOG.md`, `VERSION.md`, and `ROADMAP.md` — synchronized publication metadata; only the files proven stale by tests may change.
- `.github/workflows/catalog-validation.yml` — run release and link validation when release, project, documentation, test, or tool paths change.
- `tools/README.md` — document release and Mermaid validation commands.
- GitHub PRs, issue #39, temporary external-evidence JSON, and annotated tag `v0.4-alpha` — non-self-referential exact-SHA evidence; no external-evidence JSON is committed.

---

### Task 1: Implement the authoritative release-gate contract

**Files:**
- Create: `tools/release_gates.py`
- Create: `tests/test_release_gates.py`
- Create: `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md`
- Modify: `tools/README.md`

**Interfaces:**
- Consumes: `VERSION.md`, `project/RELEASE_PLAN.md`, `crosswalks/catalog.json`, Git-tracked files, and optional external evidence JSON.
- Produces: `load_front_matter(path: Path) -> dict[str, object]`.
- Produces: `validate_record(root: Path, record: dict[str, object]) -> list[str]`.
- Produces: `validate_transition(previous: dict[str, object], candidate: dict[str, object]) -> list[str]`.
- Produces: `validate_external_evidence(record: dict[str, object], evidence: dict[str, object], expected_head: str, phase: str) -> list[str]`.
- Produces CLI: `python tools/release_gates.py --check [--baseline-ref REF] [--external-evidence PATH --expected-head SHA --phase closure|taggable]`.

- [ ] **Step 1: Write fail-first parser, schema, scope, transition, and external-evidence tests**

Create `tests/test_release_gates.py` with synthetic fixtures and repository assertions. The core test structures shall be:

```python
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest

from tools.release_gates import (
    EXPECTED_MAPPING_SETS,
    GATE_IDS,
    load_front_matter,
    validate_external_evidence,
    validate_record,
    validate_transition,
)

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"


def valid_record() -> dict[str, object]:
    return {
        "release": "0.4-alpha",
        "phase": "evidence_candidate",
        "tag": "v0.4-alpha",
        "issue": 39,
        "publication": {
            "date": None,
            "condition": "remote_annotated_tag_matches_exact_validated_commit",
        },
        "mapping_sets": [
            "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
            "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
            "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
        ],
        "gates": {gate: {"state": "open", "evidence": []} for gate in GATE_IDS},
    }


def closure_record() -> dict[str, object]:
    record = valid_record()
    record["phase"] = "closure_candidate"
    record["publication"] = {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "condition": "remote_annotated_tag_matches_exact_validated_commit",
    }
    record["gates"] = {
        gate: {
            "state": "ready",
            "evidence": ["https://github.com/tdistress/ESAF/issues/39"],
        }
        for gate in GATE_IDS
    }
    return record


def approved_external_evidence(closure: str, merge: str | None = None) -> dict[str, object]:
    date = datetime.now(timezone.utc).date().isoformat()
    verdict = lambda role, suffix: {
        "sha": closure,
        "reviewer": role,
        "date": date,
        "disposition": "approved",
        "url": f"https://github.com/tdistress/ESAF/pull/50#issuecomment-{suffix}",
        "critical": 0,
        "important": 0,
    }
    evidence: dict[str, object] = {
        "closure_head": closure,
        "scope": {**verdict("scope-approver", 1), "role": "release-scope approver"},
        "technical": verdict("technical-reviewer", 2),
        "editorial": verdict("editorial-reviewer", 3),
        "rendering": verdict("rendering-reviewer", 4),
        "governance": {**verdict("governance-approver", 5), "authority": "Steering Committee"},
        "mapping_decision_schema": "esaf-mapping-decisions-v1",
        "mapping_decision_basis": "qualified_approval",
        "mapping_decisions": [
            {
                "decision_type": "qualified_approval",
                "mapping_set_id": mapping_set_id,
                "sha": closure,
                "reviewer": f"qualified-reviewer-{index}",
                "qualification": "documented scheme and ESAF qualification",
                "date": date,
                "disposition": "approved",
                "url": f"https://github.com/tdistress/ESAF/pull/50#issuecomment-{index + 10}",
            }
            for index, mapping_set_id in enumerate(EXPECTED_MAPPING_SETS, start=1)
        ],
        "github_checks": {
            "expected": ["Validate ESAF sources"],
            "observed": [{
                "name": "Validate ESAF sources",
                "sha": closure,
                "conclusion": "success",
                "url": "https://github.com/tdistress/ESAF/actions/runs/1",
            }],
        },
        "merge_state": {"sha": closure, "mergeable": True, "state": "clean"},
    }
    if merge is not None:
        command_names = (
            "full_suite", "controls", "architectures", "migration",
            "crosswalk_current", "crosswalk_baseline", "links", "release_record",
            "mermaid_inventory", "whole_range_diff", "cache_count", "clean_status",
        )
        evidence["merge_head"] = merge
        evidence["post_merge"] = {
            "sha": merge,
            "commands": [
                {"name": name, "exit_code": 0, "result": "passed"}
                for name in command_names
            ],
        }
    return evidence


class ReleaseGateTests(unittest.TestCase):
    def test_authoritative_record_is_valid(self) -> None:
        self.assertEqual(validate_record(ROOT, load_front_matter(RECORD)), [])

    def test_record_rejects_self_referential_sha_fields_and_values(self) -> None:
        for key, value in (
            ("candidate_sha", "a" * 40),
            ("reviewed_commit", "b" * 40),
            ("evidence", ["c" * 40]),
        ):
            with self.subTest(key=key):
                record = valid_record()
                record[key] = value
                self.assertTrue(validate_record(ROOT, record))

    def test_closed_gate_requires_nonempty_stable_evidence_locator(self) -> None:
        record = valid_record()
        record["gates"]["technical"] = {"state": "closed", "evidence": []}
        self.assertIn("technical: closed gate requires evidence", validate_record(ROOT, record))

    def test_transition_rejects_open_directly_to_closed(self) -> None:
        previous = valid_record()
        candidate = deepcopy(previous)
        candidate["gates"]["technical"]["state"] = "closed"
        candidate["gates"]["technical"]["evidence"] = ["https://github.com/tdistress/ESAF/issues/39"]
        self.assertIn("technical: illegal transition open -> closed", validate_transition(previous, candidate))

    def test_repository_scope_locks_three_draft_mapping_sets(self) -> None:
        record = load_front_matter(RECORD)
        self.assertEqual(validate_record(ROOT, record), [])
        self.assertEqual(len(record["mapping_sets"]), 3)

    def test_taggable_phase_rejects_missing_or_wrong_sha_approval(self) -> None:
        record = closure_record()
        closure = "d" * 40
        expected_merge = "f" * 40
        evidence = approved_external_evidence(closure, expected_merge)
        evidence["governance"]["sha"] = "e" * 40
        evidence["mapping_decisions"] = []
        errors = validate_external_evidence(record, evidence, expected_merge, "taggable")
        self.assertIn("governance approval is not bound to closure head", errors)
        self.assertIn("mapping decisions shall contain each expected mapping set exactly once", errors)

    def test_taggable_phase_preserves_distinct_candidate_and_merge_domains(self) -> None:
        record = closure_record()
        closure = "d" * 40
        merge = "f" * 40
        evidence = approved_external_evidence(closure, merge)
        self.assertEqual(validate_external_evidence(record, evidence, merge, "taggable"), [])

    def test_closure_phase_requires_every_approval_check_and_clean_merge_state(self) -> None:
        closure = "d" * 40
        record = closure_record()
        for key in ("scope", "technical", "editorial", "rendering", "governance", "github_checks", "merge_state"):
            with self.subTest(key=key):
                evidence = approved_external_evidence(closure)
                del evidence[key]
                self.assertTrue(validate_external_evidence(record, evidence, closure, "closure"))

    def test_external_validation_requires_true_ready_closure_record(self) -> None:
        closure = "d" * 40
        for name, mutate, diagnostic in (
            ("phase", lambda r: r.__setitem__("phase", "evidence_candidate"), "record phase shall be closure_candidate"),
            ("altered_condition", lambda r: r["publication"].__setitem__("condition", "tag_exists"), "publication condition is invalid"),
            ("missing_condition", lambda r: r["publication"].pop("condition"), "publication condition is invalid"),
            ("missing_date", lambda r: r["publication"].__setitem__("date", None), "conditional publication date shall equal current UTC date"),
            ("open", lambda r: r["gates"]["technical"].__setitem__("state", "open"), "technical gate is not ready for closure"),
            ("in_review", lambda r: r["gates"]["editorial"].__setitem__("state", "in_review"), "editorial gate is not ready for closure"),
        ):
            with self.subTest(name=name):
                record = closure_record()
                mutate(record)
                self.assertIn(diagnostic, validate_external_evidence(record, approved_external_evidence(closure), closure, "closure"))

    def test_taggable_evidence_mutation_matrix(self) -> None:
        closure = "d" * 40
        merge = "f" * 40
        mutations = (
            ("disposition", lambda e: e["technical"].__setitem__("disposition", "rejected"), "technical disposition shall be approved"),
            ("url", lambda e: e["editorial"].__setitem__("url", "http://example.invalid"), "editorial URL shall use HTTPS"),
            ("findings", lambda e: e["rendering"].__setitem__("important", 1), "rendering Important findings shall be zero"),
            ("duplicate_mapping", lambda e: e["mapping_decisions"].append(deepcopy(e["mapping_decisions"][0])), "mapping decisions shall contain each expected mapping set exactly once"),
            ("duplicate_check", lambda e: e["github_checks"]["observed"].append(deepcopy(e["github_checks"]["observed"][0])), "observed GitHub checks shall exactly match expected checks"),
            ("exit_code", lambda e: e["post_merge"]["commands"][0].__setitem__("exit_code", 1), "full_suite command failed"),
            ("authority", lambda e: e["governance"].__setitem__("authority", "repository owner"), "governance authority is not authorized"),
            ("merge_state", lambda e: e["merge_state"].__setitem__("state", "dirty"), "merge state shall be clean"),
            ("candidate_sha", lambda e: e["scope"].__setitem__("sha", "a" * 40), "scope approval is not bound to closure head"),
            ("merge_sha", lambda e: e["post_merge"].__setitem__("sha", "a" * 40), "post-merge evidence is not bound to merge head"),
        )
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                evidence = approved_external_evidence(closure, merge)
                mutate(evidence)
                self.assertIn(diagnostic, validate_external_evidence(closure_record(), evidence, merge, "taggable"))
```

- [ ] **Step 2: Run the new tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_gates -v
```

Expected: import failure for `tools.release_gates`; no unrelated test is executed.

- [ ] **Step 3: Implement the minimal release-gate validator**

Create `tools/release_gates.py` with these exact constants and validation boundaries:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

import yaml

GATE_IDS = (
    "scope",
    "technical",
    "editorial",
    "cross_reference_rendering",
    "standards_mapping",
    "release_metadata",
    "governance",
    "post_merge",
)
STATES = {"open", "in_review", "ready", "closed"}
ALLOWED_TRANSITIONS = {
    "open": {"open", "in_review", "ready"},
    "in_review": {"open", "in_review", "ready"},
    "ready": {"open", "in_review", "ready", "closed"},
    "closed": {"open", "in_review", "closed"},
}
EXPECTED_MAPPING_SETS = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
)
PUBLICATION_CONDITION = "remote_annotated_tag_matches_exact_validated_commit"
SHA_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", re.IGNORECASE)


def load_front_matter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path}: YAML front matter is required")
    payload = text[4:text.index("\n---\n", 4)]
    value = yaml.safe_load(payload)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: front matter shall be a mapping")
    return value


def flattened_items(value: object, prefix: str = ""):
    if prefix:
        yield prefix, value
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            yield from flattened_items(child, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from flattened_items(child, f"{prefix}[{index}]")


def validate_record(root: Path, record: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if record.get("release") != "0.4-alpha":
        errors.append("release shall equal 0.4-alpha")
    if record.get("tag") != "v0.4-alpha":
        errors.append("tag shall equal v0.4-alpha")
    if record.get("issue") != 39:
        errors.append("issue shall equal 39")
    if record.get("phase") not in {"evidence_candidate", "closure_candidate"}:
        errors.append("phase shall be evidence_candidate or closure_candidate")
    publication = record.get("publication")
    if not isinstance(publication, dict) or publication.get("condition") != PUBLICATION_CONDITION:
        errors.append("publication condition is invalid")
    elif record.get("phase") == "evidence_candidate" and publication.get("date") is not None:
        errors.append("evidence candidate shall not have a publication date")
    elif record.get("phase") == "closure_candidate" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(publication.get("date", ""))):
        errors.append("closure candidate shall have an ISO publication date")
    if tuple(sorted(record.get("mapping_sets", []))) != tuple(sorted(EXPECTED_MAPPING_SETS)):
        errors.append("mapping_sets shall equal the three unique Draft snapshots")
    gates = record.get("gates")
    if not isinstance(gates, dict) or tuple(gates) != GATE_IDS:
        errors.append("gates shall contain the exact ordered gate identifiers")
    else:
        for gate_id, gate in gates.items():
            if not isinstance(gate, dict) or gate.get("state") not in STATES:
                errors.append(f"{gate_id}: invalid gate state")
                continue
            evidence = gate.get("evidence")
            if not isinstance(evidence, list):
                errors.append(f"{gate_id}: evidence shall be a list")
            elif gate["state"] in {"ready", "closed"} and not evidence:
                errors.append(f"{gate_id}: {gate['state']} gate requires evidence")
    for path, value in flattened_items(record):
        if "sha" in path.casefold() or "commit" in path.casefold():
            errors.append(f"{path}: tracked record shall not contain SHA fields")
        if isinstance(value, str) and SHA_RE.search(value):
            errors.append(f"{path}: tracked record shall not contain a 40-character SHA")
    catalog = json.loads((root / "crosswalks/catalog.json").read_text(encoding="utf-8"))
    identifiers = tuple(item["metadata"]["mapping_set_id"] for item in catalog["mapping_sets"])
    if tuple(sorted(identifiers)) != tuple(sorted(EXPECTED_MAPPING_SETS)):
        errors.append("catalog mapping sets differ from the release scope")
    if any(item["metadata"]["status"] != "draft" for item in catalog["mapping_sets"]):
        errors.append("every in-scope mapping set shall remain draft")
    return errors


def validate_transition(previous: dict[str, object], candidate: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for gate_id in GATE_IDS:
        before = previous["gates"][gate_id]["state"]
        after = candidate["gates"][gate_id]["state"]
        if after not in ALLOWED_TRANSITIONS[before]:
            errors.append(f"{gate_id}: illegal transition {before} -> {after}")
    return errors
```

Implement `validate_external_evidence` directly below it with two explicit SHA domains and the complete evidence contract below.

Candidate-bound evidence shall contain:

- `closure_head`;
- `scope` with `sha`, named approver, role, UTC date, `disposition: approved`, and HTTPS URL;
- `technical`, `editorial`, and `rendering` objects with `sha`, reviewer, UTC date, `disposition: approved`, HTTPS URL, `critical: 0`, and `important: 0`;
- `governance` with `sha`, named approver, UTC date, `disposition: approved`, and HTTPS URL; `authority` shall equal `Steering Committee` as assigned by `GOVERNANCE.md`;
- `mapping_decision_schema: esaf-mapping-decisions-v1`, one `mapping_decision_basis`, and exactly three `mapping_decisions`, one per `EXPECTED_MAPPING_SETS`; every decision shall match that one basis. Qualified decisions carry candidate SHA, reviewer, qualification, UTC date, `disposition: approved`, and HTTPS URL. Owner-risk decisions carry candidate SHA, owner identity and association, `accepted_for_working_draft`, `qualified_review_status: deferred`, limitations, and the verified fetched-comment source;
- `github_checks.expected` equal to `['Validate ESAF sources']` and `github_checks.observed` containing exactly that named check with candidate SHA, `conclusion: success`, and HTTPS URL; and
- `merge_state` with candidate SHA, `mergeable: true`, and `state: clean`.

For both external phases, the tracked record shall have `phase: closure_candidate`, publication condition exactly `remote_annotated_tag_matches_exact_validated_commit`, a current ISO UTC publication date, and every gate in `ready` or `closed`; any `open` or `in_review` gate blocks closure and tagging.

In phase `closure`, `expected_head == closure_head` and every candidate-bound SHA shall equal it; `merge_head` and `post_merge` shall be absent. In phase `taggable`, the same candidate-bound objects shall remain bound to the separately recorded `closure_head`, while `expected_head == merge_head == post_merge.sha`. The taggable `post_merge.commands` shall contain exactly one successful entry for each of `full_suite`, `controls`, `architectures`, `migration`, `crosswalk_current`, `crosswalk_baseline`, `links`, `release_record`, `mermaid_inventory`, `whole_range_diff`, `cache_count`, and `clean_status`; every exit code shall be 0 and every result shall be nonempty. Missing fields, extra or duplicate mapping sets/checks/commands, non-HTTPS URLs, non-approved dispositions, nonzero findings/exit codes, invalid decision basis, unauthorized governance, non-clean merge state, and any SHA-domain mismatch shall each produce the exact diagnostics asserted by the mutation tests above.

The CLI shall load the tracked record, run `validate_record`, optionally load its baseline form with `git show "$baselineRef:docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"` and run `validate_transition`, optionally load external JSON and run `validate_external_evidence`, print one diagnostic per line, and return 0 only when no diagnostic exists. A missing baseline record is allowed only when the current record phase is `evidence_candidate`; closure and taggable phases shall fail if the baseline record cannot be loaded.

- [ ] **Step 4: Add the initial authoritative readiness record**

Create `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md` with this front matter and concise sections for scope, lifecycle limitations, evidence ownership, invalidation, and current state:

```yaml
---
release: 0.4-alpha
phase: evidence_candidate
tag: v0.4-alpha
issue: 39
publication:
  date: null
  condition: remote_annotated_tag_matches_exact_validated_commit
mapping_sets:
  - uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0
  - uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0
gates:
  scope: {state: in_review, evidence: []}
  technical: {state: open, evidence: []}
  editorial: {state: open, evidence: []}
  cross_reference_rendering: {state: open, evidence: []}
  standards_mapping: {state: open, evidence: []}
  release_metadata: {state: in_review, evidence: []}
  governance: {state: open, evidence: []}
  post_merge: {state: open, evidence: []}
---
```

The prose shall state the derived baseline totals: 91 controls, 16 families, 7 Draft architecture patterns, 3 Draft mapping sets, 404 provisions, 81 relationship legs, and 325 negative dispositions. It shall not include a candidate, reviewed, merge, or tag commit ID.

- [ ] **Step 5: Document the validator and run GREEN**

Add to `tools/README.md`:

```markdown
## Release-gate validation

Validate the authoritative 0.4-alpha readiness record without changing files:

```shell
python tools/release_gates.py --check
```

Exact candidate, approval, merge, and tag SHAs remain in GitHub evidence and an
external temporary JSON file; they are never written into the tracked record.
```

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_gates -v
python tools/release_gates.py --check
git diff --check
```

Expected: all release-gate tests pass, the validator reports no diagnostics, and the diff check exits 0.

- [ ] **Step 6: Commit the release-gate contract**

```powershell
git add -- tools/release_gates.py tests/test_release_gates.py tools/README.md docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md
git commit -m "Define 0.4-alpha release gate contract"
```

### Task 2: Build deterministic Mermaid inventory and render inputs

**Files:**
- Create: `tools/mermaid_inventory.py`
- Create: `tests/test_mermaid_inventory.py`
- Create: `docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md`
- Modify: `tools/README.md`

**Interfaces:**
- Consumes: all Git-tracked `*.md` files returned by `git ls-files`.
- Produces: immutable `MermaidBlock(path: str, index: int, digest: str, diagram_type: str, source: str)`.
- Produces: `discover(root: Path) -> list[MermaidBlock]` sorted by path then block index.
- Produces: `write_render_inputs(blocks: list[MermaidBlock], output_dir: Path) -> Path` with one `.mmd` per block and `inventory.json`.
- Produces CLI: `python tools/mermaid_inventory.py --output-dir DIR --write` and `--check-record PATH`.

- [ ] **Step 1: Write fail-first inventory tests**

Create `tests/test_mermaid_inventory.py` with these cases:

```python
from hashlib import sha256
from pathlib import Path
import tempfile
import unittest

from tools.mermaid_inventory import discover, extract_blocks, write_render_inputs

ROOT = Path(__file__).resolve().parents[1]


class MermaidInventoryTests(unittest.TestCase):
    def test_extract_blocks_accepts_lf_and_crlf_fences(self) -> None:
        text = "```mermaid\r\ngraph TD\r\nA-->B\r\n```\r\n\n```mermaid\nsequenceDiagram\nA->>B: ok\n```\n"
        self.assertEqual(extract_blocks(text), ["graph TD\nA-->B", "sequenceDiagram\nA->>B: ok"])

    def test_repository_inventory_is_complete_and_deterministic(self) -> None:
        first = discover(ROOT)
        second = discover(ROOT)
        self.assertEqual(first, second)
        self.assertEqual(23, len(first))
        self.assertEqual([(item.path, item.index) for item in first], sorted((item.path, item.index) for item in first))
        for item in first:
            self.assertEqual(item.digest, sha256(item.source.encode("utf-8")).hexdigest())

    def test_render_inputs_are_outside_repository_and_exact(self) -> None:
        blocks = discover(ROOT)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve()
            inventory = write_render_inputs(blocks, output)
            self.assertFalse(output.is_relative_to(ROOT.resolve()))
            self.assertTrue(inventory.is_file())
            self.assertEqual(len(blocks), len(list(output.glob("*.mmd"))))
```

- [ ] **Step 2: Run the tests and verify RED**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_mermaid_inventory -v
```

Expected: import failure for `tools.mermaid_inventory`.

- [ ] **Step 3: Implement deterministic discovery and temporary input writing**

Create `tools/mermaid_inventory.py` around this complete data contract:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys

MERMAID_RE = re.compile(r"```mermaid\r?\n(.*?)\r?\n```", re.DOTALL)


@dataclass(frozen=True)
class MermaidBlock:
    path: str
    index: int
    digest: str
    diagram_type: str
    source: str


def extract_blocks(text: str) -> list[str]:
    return [match.group(1).replace("\r\n", "\n") for match in MERMAID_RE.finditer(text)]


def diagram_type(source: str) -> str:
    for line in source.splitlines():
        candidate = line.strip()
        if candidate and not candidate.startswith("%%"):
            return candidate.split(maxsplit=1)[0]
    raise ValueError("Mermaid block does not declare a diagram type")


def tracked_markdown(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--", "*.md"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return sorted(result.stdout.splitlines())


def discover(root: Path) -> list[MermaidBlock]:
    blocks: list[MermaidBlock] = []
    for relative in tracked_markdown(root):
        text = (root / relative).read_text(encoding="utf-8")
        for index, source in enumerate(extract_blocks(text), start=1):
            blocks.append(MermaidBlock(relative.replace("\\", "/"), index, sha256(source.encode("utf-8")).hexdigest(), diagram_type(source), source))
    return blocks


def write_render_inputs(blocks: list[MermaidBlock], output_dir: Path) -> Path:
    output_dir = output_dir.resolve()
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()).resolve()
    if output_dir == root or output_dir.is_relative_to(root):
        raise ValueError("renderer output shall be outside the repository")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for ordinal, block in enumerate(blocks, start=1):
        name = f"{ordinal:03d}-{Path(block.path).stem}-{block.index}.mmd"
        (output_dir / name).write_text(block.source + "\n", encoding="utf-8", newline="\n")
        rows.append({**asdict(block), "source": None, "input": name})
    inventory = output_dir / "inventory.json"
    inventory.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8", newline="\n")
    return inventory
```

The CLI shall require `--write`, reject a pre-existing nonempty output directory, call `discover`, call `write_render_inputs`, and print the derived block count with the resolved output directory. `--check-record` shall parse the tracked Markdown ledger table and require exact `(path, index, digest, diagram type)` equality, the approved candidate-content status, the pinned renderer version, a non-placeholder reviewer identity, `Render == Pass`, and `Readability == Pass` for every current block.

- [ ] **Step 4: Create the pending exhaustive rendering ledger**

Create `docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md` with status `Pending exact-head rendering review`, renderer version `11.16.0`, and one row per discovered block:

```markdown
| Path | Block | SHA-256 | Diagram type | Render | Readability | Reviewer |
|---|---:|---|---|---|---|---|
| `architectures/patterns/ARC-P110.md` | 1 | `c0806f3c6906762383359c293f8eaf34ef4f8c3b13950bc1addbc20a2b670322` | flowchart | Pending | Pending | Pending |
```

Generate the 23 exact rows mechanically from `discover(ROOT)`; do not hand-copy paths or digests. The implementation may add a `--record-template` CLI argument that emits those rows, but it shall not overwrite any non-Pending human disposition.

- [ ] **Step 5: Run GREEN and document the pinned renderer command**

Add to `tools/README.md`:

```markdown
## Mermaid publication rendering

Inventory every tracked Mermaid block and write temporary renderer inputs outside the repository:

```shell
python tools/mermaid_inventory.py --output-dir /tmp/esaf-v04-mermaid --write
```

Render each input with `@mermaid-js/mermaid-cli@11.16.0`, then record parse and readability dispositions in the tracked release ledger. Parser success does not replace visual review.
```

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_mermaid_inventory -v
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md
git diff --check
```

Expected: unit tests pass; `--check-record` fails only because the exact 23 human dispositions remain Pending.

- [ ] **Step 6: Commit the inventory contract and pending ledger**

```powershell
git add -- tools/mermaid_inventory.py tests/test_mermaid_inventory.py tools/README.md docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md
git commit -m "Add exhaustive Mermaid release inventory"
```

### Task 3: Reconcile the evidence candidate and CI gates

**Files:**
- Modify: `tests/test_release_metadata.py`
- Modify: `CHANGELOG.md`
- Modify only if a failing invariant proves drift: `VERSION.md`, `ROADMAP.md`, `project/BACKLOG.md`, `project/RELEASE_PLAN.md`
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md`

**Interfaces:**
- Consumes: Task 1 release record and Task 2 Mermaid inventory.
- Produces: an internally coherent `evidence_candidate` with no publication date and all review-dependent gates Open or In review.
- Produces: CI coverage for release validation and repository-local links.

- [ ] **Step 1: Add fail-first release-scope and CI assertions**

Extend `tests/test_release_metadata.py` with:

```python
def test_current_changelog_names_all_three_draft_mapping_snapshots(self) -> None:
    section = current_changelog_section(current_version())
    required = (
        "Cyber Essentials v3.3",
        "Cyber Essentials Plus v3.2 `esaf_to_external`",
        "Cyber Essentials Plus v3.2 `external_to_esaf`",
    )
    for label in required:
        with self.subTest(label=label):
            self.assertIn(label, section)

def test_evidence_candidate_remains_unreleased_and_untagged(self) -> None:
    record = load_front_matter(ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md")
    self.assertEqual("evidence_candidate", record["phase"])
    self.assertIsNone(record["publication"]["date"])
    changelog = read_repository_file("CHANGELOG.md")
    self.assertEqual(1, changelog.count(f"## {current_version()} - Unreleased"))

def test_repository_workflow_runs_release_and_link_validation(self) -> None:
    workflow = read_repository_file(".github/workflows/catalog-validation.yml")
    self.assertIn("python tools/release_gates.py --check", workflow)
    self.assertIn("python tools/validate_links.py --check", workflow)
```

Import `load_front_matter` from `tools.release_gates` at module top.

- [ ] **Step 2: Run focused tests and verify RED only for missing reconciliation**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata tests.test_release_gates tests.test_mermaid_inventory -v
```

Expected: failures for missing two Cyber Essentials Plus changelog entries and missing workflow commands; all Task 1 and Task 2 contract tests pass.

- [ ] **Step 3: Apply the minimal metadata reconciliation**

Under `CHANGELOG.md` 0.4-alpha Added, add exactly:

```markdown
- Added the Draft Cyber Essentials Plus v3.2 `esaf_to_external` snapshot with 144 records and 8 forward-only relationship legs.
- Added the separate Draft Cyber Essentials Plus v3.2 `external_to_esaf` snapshot with 144 records, 32 reverse-only relationship legs, and 112 specific no-direct-mapping dispositions.
```

Derive every count again from the validators before committing. If an existing authoritative count differs, use the validator-derived value and update the focused expectation in the same red-green cycle. Do not alter `VERSION.md`, `ROADMAP.md`, `project/BACKLOG.md`, or `project/RELEASE_PLAN.md` unless its exact focused assertion fails.

- [ ] **Step 4: Extend CI path coverage and validation**

In `.github/workflows/catalog-validation.yml`, add these pull-request and push paths:

```yaml
      - "CHANGELOG.md"
      - "VERSION.md"
      - "ROADMAP.md"
      - "project/**"
      - "docs/superpowers/reviews/**"
      - "tools/release_gates.py"
      - "tools/mermaid_inventory.py"
      - "tools/validate_links.py"
```

After the crosswalk steps add:

```yaml
      - name: Validate release gate record
        run: python tools/release_gates.py --check
      - name: Validate repository-local links
        run: python tools/validate_links.py --check
```

- [ ] **Step 5: Run focused, validator, and workflow syntax gates**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata tests.test_release_gates tests.test_mermaid_inventory -v
python tools/release_gates.py --check
python tools/validate_crosswalks.py --check
python tools/validate_links.py --check
python -c "import yaml; yaml.safe_load(open('.github/workflows/catalog-validation.yml', encoding='utf-8')); print('workflow YAML valid')"
git diff --check
```

Expected: all focused tests and validators pass; workflow YAML parses; 3 mapping sets, 404 provisions, 81 relationship legs, and 325 negative dispositions remain unchanged.

- [ ] **Step 6: Commit the evidence-candidate reconciliation**

```powershell
git add -- tests/test_release_metadata.py CHANGELOG.md .github/workflows/catalog-validation.yml docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md
git add -- VERSION.md ROADMAP.md project/BACKLOG.md project/RELEASE_PLAN.md
git diff --cached --check
git commit -m "Reconcile 0.4-alpha evidence candidate"
```

Before committing, unstage any of the four conditional metadata files whose bytes did not need to change.

### Task 4: Render, review, freeze, and publish evidence candidate PR A

**Files:**
- Modify: `docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md`
- Create: `docs/superpowers/reviews/2026-07-21-v04-alpha-technical-review.md`
- Create: `docs/superpowers/reviews/2026-07-21-v04-alpha-editorial-review.md`
- Modify: `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md`
- Create outside repository: Mermaid `.mmd` and `.svg` files, `inventory.json`, `external-evidence.json`, and reviewer scratch notes.

**Interfaces:**
- Consumes: Tasks 1–3 candidate, pinned renderer, all 23 discovered blocks, and full release scope.
- Produces: immutable evidence-candidate head, complete rendering ledger, two independent tracked review reports, two-basis mapping-decision evidence in GitHub, and draft PR A linked to issue #39.

- [ ] **Step 1: Create a verified temporary rendering directory and render all blocks**

```powershell
$renderRoot = Join-Path ([IO.Path]::GetTempPath()) ("esaf-v04-mermaid-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $renderRoot | Out-Null
$resolvedRenderRoot = (Resolve-Path -LiteralPath $renderRoot).Path
$repositoryRoot = (git rev-parse --show-toplevel).Trim()
if ($resolvedRenderRoot.StartsWith($repositoryRoot, [StringComparison]::OrdinalIgnoreCase)) { throw 'Renderer output is inside repository' }
python tools/mermaid_inventory.py --output-dir $resolvedRenderRoot --write
$pnpm = 'C:\Users\phrea\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd'
$inputs = Get-ChildItem -LiteralPath $resolvedRenderRoot -Filter '*.mmd' | Sort-Object Name
foreach ($input in $inputs) {
    $svg = [IO.Path]::ChangeExtension($input.FullName, '.svg')
    & $pnpm dlx '@mermaid-js/mermaid-cli@11.16.0' -i $input.FullName -o $svg
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $svg)) { throw "Mermaid render failed: $($input.Name)" }
}
Write-Output "RENDERED=$($inputs.Count)"
```

Expected: `RENDERED=23` unless the exact candidate deliberately added blocks, in which case the repository-count test and ledger shall be updated to the new derived count before review.

- [ ] **Step 2: Perform exhaustive readability review and close the ledger**

Inspect every SVG at full resolution. For each ledger row record `Render = Pass`, `Readability = Pass`, and the reviewer identity only after confirming no clipped label, unreadable density, missing node/edge, unsafe contrast, or mismatch with its numbered figure/prose. Any failure returns to the relevant source task; add a focused regression when practical, correct the source, regenerate the entire inventory, rerender every changed block, and restart affected exact-head review.

Update the record status to `Approved on candidate content; pending final exact-head recheck`. Then run:

```powershell
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md
```

Expected: exact 23-row inventory and all dispositions pass.

- [ ] **Step 3: Obtain independent normative/technical and editorial reviews**

Dispatch two distinct reviewers who did not implement Tasks 1–3. Technical review shall cover the complete branch range from merge base through all normative content, controls, architecture, mapping boundaries, validators, and release logic. Editorial review shall cover terminology, `shall`/`should`/`may`, numbering, links, cross-references, changelog, roadmap, version, backlog, release plan, generated catalogs, and all renderer-to-prose pairings.

Each tracked report shall contain scope, merge base, candidate content commit before report creation, methods, exact derived counts, findings, dispositions, reviewer identity, independence statement, and explicit limitation that technical review is neither governance nor a mapping decision. Resolve Critical and Important findings, commit corrections, and redispatch both reviewers after any candidate change.

- [ ] **Step 4: Commit reports, then run exact-head read-only re-reviews**

```powershell
git add -- docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md docs/superpowers/reviews/2026-07-21-v04-alpha-technical-review.md docs/superpowers/reviews/2026-07-21-v04-alpha-editorial-review.md docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md
git commit -m "Review 0.4-alpha evidence candidate"
$candidateSha = (git rev-parse HEAD).Trim()
```

Both reviewers shall re-review the complete branch range at `$candidateSha` and return zero unresolved Critical or Important findings without editing tracked files. Record these exact-head verdicts externally.

- [ ] **Step 5: Run every exact-head candidate gate**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$mergeBase = (git merge-base HEAD main).Trim()
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref $mergeBase
python tools/validate_links.py --check
python tools/release_gates.py --check --baseline-ref $mergeBase
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md
git diff --check "$mergeBase..HEAD"
if (rg -n -i '^\s*(TBD|TODO|PLACEHOLDER|lorem ipsum)\s*$' README.md VERSION.md ROADMAP.md CHANGELOG.md project docs/superpowers/reviews) { throw 'Standalone drafting marker found' }
$cacheDirs = @(Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue)
if ($cacheDirs.Count -ne 0) { throw "Cache directories found: $($cacheDirs.Count)" }
if (@(git status --porcelain).Count -ne 0) { throw 'Candidate worktree is not clean' }
```

Expected: full suite passes; controls report 91/91/16; architectures report 10 foundation files and 7 patterns; migration reports 91 sections and 0 changed; crosswalks report 3/404/81/325 in both modes; all links, release gates, Mermaid ledger, diff, marker, cache, and status checks pass.

- [ ] **Step 6: Push and open draft evidence candidate PR A**

```powershell
$candidateSha = (git rev-parse HEAD).Trim()
git push -u origin agent/v04-alpha-publication-gates-design
$prBody = @"
Closes #39 only after the separate closure PR, post-merge validation, and verified annotated tag.

Evidence candidate: $candidateSha
Release status: Unreleased 0.4-alpha Working Draft
Scope: complete tracked repository, including 91 controls, 7 Draft architecture patterns, and 3 Draft mapping sets.
Renderer: all 23 Mermaid blocks rendered with @mermaid-js/mermaid-cli@11.16.0 and passed readability review.
Validation: include the exact Task 4 Step 5 command outputs and counts in this paragraph before submitting.
Reviews: include the exact technical, editorial, and renderer reviewer identities and dispositions before submitting.
Pending: one uniform mapping-decision basis and scope evidence on this exact head.

This PR does not authorize publication or tag creation. Draft artifacts remain Draft, with no compliance, certification, equivalence, endorsement, or production-readiness claim.
"@
gh pr create --repo tdistress/ESAF --base main --head agent/v04-alpha-publication-gates-design --draft --title "Prepare 0.4-alpha publication evidence candidate" --body $prBody
$prNumber = gh pr view --repo tdistress/ESAF agent/v04-alpha-publication-gates-design --json number --jq '.number'
```

The PR body file shall identify issue #39, exact `$candidateSha`, full scope, lifecycle limitations, every command/result, renderer 23/23 result, reviewer identities/dispositions, and the pending uniform mapping-decision/scope evidence. It shall state that no release or tag is authorized by PR A.

- [ ] **Step 7: Obtain one uniform mapping decision and scope evidence on exact PR A head**

Choose exactly one uniform basis for all mapping snapshots. For `qualified_approval`, require qualified contributor comments with reviewer identity, qualification, exact `$candidateSha`, mapping-set ID, date, disposition, and limitations. For `owner_risk_acceptance`, obtain a repository-owner comment with the three exact mapping IDs, exact `$candidateSha`, Working Draft limitations, deferred qualified-review status, and all prohibited claims; never treat it as governance. In either case, obtain exact-head scope evidence. Do not infer mapping qualification from repository ownership.

After approvals, verify:

```powershell
$candidateSha = (git rev-parse HEAD).Trim()
$prNumber = gh pr view --repo tdistress/ESAF agent/v04-alpha-publication-gates-design --json number --jq '.number'
gh pr checks --repo tdistress/ESAF $prNumber
gh pr view --repo tdistress/ESAF $prNumber --json state,isDraft,mergeable,headRefOid,statusCheckRollup
```

Expected: head equals `$candidateSha`, all required checks pass, PR is mergeable, and no tracked byte changed after approvals.

### Task 5: Merge PR A, validate merged main, and build evidence-only closure PR B

**Files in closure branch:**
- Modify: `tests/test_release_metadata.py`
- Modify: `tests/test_release_gates.py`
- Modify: `CHANGELOG.md`
- Modify: `project/RELEASE_PLAN.md`
- Modify: `docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md`
- No other tracked path is allowed unless a failing closure-contract test proves it necessary and the design is amended and reapproved first.

**Interfaces:**
- Consumes: merged PR A, exact PR A merge SHA, external PR A evidence, and byte-identical mapping/Mermaid inventories.
- Produces: a fresh `agent/v04-alpha-publication-gates-closure` branch from amended, validated `main`, conditional changelog state for the UTC date observed when the closure candidate is created, and closure PR B whose diff is evidence-only.

- [ ] **Step 1: Merge approved PR A and validate exact resulting main**

Promote PR A from draft only after all Task 4 gates pass. Merge with the repository's normal merge-commit strategy, update local `main`, and bind `$evidenceMerge` to both local and remote main:

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
$prNumber = gh pr view --repo tdistress/ESAF agent/v04-alpha-publication-gates-design --json number --jq '.number'
gh pr ready --repo tdistress/ESAF $prNumber
gh pr merge --repo tdistress/ESAF $prNumber --merge
git -C $mainRoot pull --ff-only origin main
$evidenceMerge = (git -C $mainRoot rev-parse HEAD).Trim()
if ($evidenceMerge -ne (git -C $mainRoot rev-parse origin/main).Trim()) { throw 'Local and remote main differ' }
Set-Location -LiteralPath $mainRoot
if ((git branch --show-current).Trim() -ne 'main') { throw 'Post-merge validation is not on main' }
if ((git rev-parse HEAD).Trim() -ne $evidenceMerge) { throw 'Post-merge checkout differs from the captured merge' }
```

Run the complete post-merge set from that exact main checkout, using the first parent as the crosswalk baseline:

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
Set-Location -LiteralPath $mainRoot
$env:PYTHONDONTWRITEBYTECODE='1'
$evidenceMerge = (git rev-parse HEAD).Trim()
$evidenceParent = (git rev-parse 'HEAD^1').Trim()
if ((git branch --show-current).Trim() -ne 'main') { throw 'Post-merge validation is not on main' }
if ($evidenceMerge -ne (git rev-parse origin/main).Trim()) { throw 'Post-merge main differs from origin/main' }
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref $evidenceParent
python tools/validate_links.py --check
python tools/release_gates.py --check --baseline-ref $evidenceParent
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md
git diff --check "$evidenceParent..HEAD"
$cacheDirs = @(Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue)
if ($cacheDirs.Count -ne 0) { throw "Cache directories found: $($cacheDirs.Count)" }
if (@(git status --porcelain).Count -ne 0) { throw 'Merged evidence main is not clean' }
```

Post the exact results to PR A and issue #39. Do not create the closure branch until all commands pass.

- [ ] **Step 2: Create the fresh isolated closure worktree from amended, validated main**

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
git -C $mainRoot check-ignore -q .worktrees
if ($LASTEXITCODE -ne 0) { throw '.worktrees is not ignored' }
$closurePath = "$mainRoot\.worktrees\agent-v04-alpha-publication-gates-closure"
git -C $mainRoot worktree add $closurePath -b agent/v04-alpha-publication-gates-closure main
Set-Location -LiteralPath $closurePath
if ((git branch --show-current).Trim() -ne 'agent/v04-alpha-publication-gates-closure') { throw 'Wrong closure branch' }
if ((git rev-parse HEAD).Trim() -ne (git -C $mainRoot rev-parse main).Trim()) { throw 'Closure branch did not start from validated main' }
```

Verify `.worktrees` is ignored before this command, verify `main` contains the two-basis amendment, and run the full baseline suite in the new worktree with bytecode disabled.

- [ ] **Step 3: Write fail-first conditional-publication and allowlist tests**

Resolve `$mainRoot` from the common Git directory, set `$closurePath`, switch to it, and assert branch `agent/v04-alpha-publication-gates-closure` immediately before editing. Every `apply_patch` target in Steps 3–5 shall be an absolute path beneath that resolved closure worktree.

Add `from datetime import datetime, timezone` and `import subprocess` to `tests/test_release_metadata.py`. Replace `current_changelog_section` with the conditional-aware helper below so all existing architecture and mapping assertions continue to inspect the current section:

```python
def current_changelog_section(version: str) -> str:
    changelog = read_repository_file("CHANGELOG.md")
    heading_pattern = re.compile(
        rf"^## {re.escape(version)} - (?:Unreleased|\d{{4}}-\d{{2}}-\d{{2}} "
        rf"\(effective only when remote annotated tag v0\.4-alpha resolves to this commit\))$",
        re.MULTILINE,
    )
    heading_matches = list(heading_pattern.finditer(changelog))
    if len(heading_matches) != 1:
        raise AssertionError(f"CHANGELOG.md must contain exactly one current {version} heading")
    section_start = heading_matches[0].end()
    next_release = re.search(r"^## .+$", changelog[section_start:], re.MULTILINE)
    section_end = section_start + next_release.start() if next_release else len(changelog)
    return changelog[section_start:section_end]
```

Replace the evidence-candidate unreleased assertion with:

```python
def test_closure_candidate_uses_conditional_publication_heading(self) -> None:
    record = load_front_matter(ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md")
    self.assertEqual("closure_candidate", record["phase"])
    publication_date = str(record["publication"]["date"])
    self.assertEqual(datetime.now(timezone.utc).date().isoformat(), publication_date)
    changelog = read_repository_file("CHANGELOG.md")
    heading = f"## 0.4-alpha - {publication_date} (effective only when remote annotated tag v0.4-alpha resolves to this commit)"
    self.assertEqual(1, changelog.count(heading))
    self.assertIn("The dated 0.4-alpha heading is not effective until the named remote annotated tag resolves to that exact commit.", changelog)

def test_closure_branch_changes_only_evidence_paths(self) -> None:
    allowed = {
        "CHANGELOG.md",
        "project/RELEASE_PLAN.md",
        "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md",
        "tests/test_release_metadata.py",
        "tests/test_release_gates.py",
    }
    base = subprocess.run(["git", "merge-base", "HEAD", "main"], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()
    changed = set(subprocess.run(["git", "diff", "--name-only", f"{base}..HEAD"], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.splitlines())
    self.assertEqual(changed, allowed)
```

During the red-green cycle, the allowlist test shall accept working-tree paths using `git diff --name-only HEAD` until the closure commit exists, then switch to the exact branch-range assertion above.

- [ ] **Step 4: Run focused closure tests and verify RED**

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
$closurePath = "$mainRoot\.worktrees\agent-v04-alpha-publication-gates-closure"
Set-Location -LiteralPath $closurePath
if ((git branch --show-current).Trim() -ne 'agent/v04-alpha-publication-gates-closure') { throw 'Focused closure tests are not in the closure worktree' }
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_release_metadata tests.test_release_gates -v
```

Expected: failures for evidence-candidate phase, Unreleased heading, Open readiness states, missing conditional convention, and closure allowlist content.

- [ ] **Step 5: Apply the conditional closure metadata**

At the start of this step, compute and print the exact heading:

```powershell
$publicationDate = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')
$heading = "## 0.4-alpha - $publicationDate (effective only when remote annotated tag v0.4-alpha resolves to this commit)"
Write-Output $heading
```

Use `apply_patch` to replace the Unreleased heading with that exact printed line; do not write a symbolic token into `CHANGELOG.md`.

Add this authoritative convention near the top of `CHANGELOG.md`:

```markdown
The dated 0.4-alpha heading is not effective until the named remote annotated tag resolves to that exact commit. Before that condition is satisfied, 0.4-alpha remains an unreleased Working Draft.
```

Update readiness record front matter to `phase: closure_candidate`, set `publication.date` to the same exact `$publicationDate`, and move gates with complete PR A evidence to `ready`; use stable PR/issue/report URLs in `evidence`. Keep governance and post-merge `ready`, not `closed`, because their exact external events have not occurred. Update `project/RELEASE_PLAN.md` prose to explain the conditional tag model and external exact-SHA closure without inserting any SHA.

- [ ] **Step 6: Run closure GREEN and commit**

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
$closurePath = "$mainRoot\.worktrees\agent-v04-alpha-publication-gates-closure"
Set-Location -LiteralPath $closurePath
if ((git branch --show-current).Trim() -ne 'agent/v04-alpha-publication-gates-closure') { throw 'Closure commit is not in the closure worktree' }
$env:PYTHONDONTWRITEBYTECODE='1'
$closureBase = (git merge-base HEAD main).Trim()
python -m unittest tests.test_release_metadata tests.test_release_gates -v
python tools/release_gates.py --check --baseline-ref $closureBase
python tools/validate_links.py --check
git diff --check
git add -- CHANGELOG.md project/RELEASE_PLAN.md docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md tests/test_release_metadata.py tests/test_release_gates.py
git commit -m "Prepare conditional 0.4-alpha closure candidate"
```

Expected: focused tests and validators pass; commit contains exactly the five allowed paths.

### Task 6: Review, approve, and merge exact closure PR B

**Files:**
- No new tracked file after Task 5 closure commit unless a review defect requires a new red-green correction cycle.
- Create outside repository: `closure-external-evidence.json`.

**Interfaces:**
- Consumes: exact closure head, PR A evidence, mapping-controlled and Mermaid digests, authorized reviewers, and GitHub checks.
- Produces: exact-head scope/technical/editorial/rendering verdicts, one uniform three-snapshot mapping-decision record, separate Steering Committee approval, passing CI, clean merge state, and merged PR B.

- [ ] **Step 1: Prove closure diff and controlled-content digest identity**

```powershell
$closureHead = (git rev-parse HEAD).Trim()
$closureBase = (git merge-base HEAD main).Trim()
git diff --name-only "$closureBase..$closureHead"
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md
python tools/validate_crosswalks.py --check --baseline-ref $closureBase
```

Expected: exactly the five allowed evidence paths changed; all Mermaid and mapping-controlled digests are identical; crosswalk totals remain 3/404/81/325.

- [ ] **Step 2: Run full closure gates and independent exact-head reviews**

Run the complete Task 4 Step 5 command set on `$closureHead`. Redispatch the scope approver plus technical, editorial, and rendering reviewers to the complete closure range. For `qualified_approval`, the scope approver shall state that the complete tracked release scope, three distinct Draft mapping snapshots, lifecycle limitations, and conditional publication boundary remain approved on exact `$closureHead`; record the approver's name, role, date, disposition, and stable comment URL. For `owner_risk_acceptance`, the verified owner source supplies the source-bound owner scope required by `tools/release_gates.py`. The rendering reviewer may use exact inventory digest equality because no Mermaid source changed. All verdicts shall name `$closureHead` externally, use HTTPS locators, and report zero unresolved Critical or Important findings.

- [ ] **Step 3: Construct one uniform mapping-decision record on `$closureHead`**

Use exactly one basis for the three mapping snapshots. A `qualified_approval` basis requires qualified reviewers to state that mapping-controlled digests are identical to approved PR A content and state their exact-head dispositions. An `owner_risk_acceptance` basis requires a new closure-head owner comment that accepts the disclosed Working Draft risk, defers qualified review, includes all three mapping IDs and limitations, and does not claim qualification. Construct either set of three decision objects with resolved execution values:

```powershell
$publicationDate = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')
$closureHead = (git rev-parse HEAD).Trim()
$mappingDecision = [ordered]@{
    decision_type = $mappingDecisionBasis
    mapping_set_id = 'uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0'
    sha = $closureHead
    reviewer = $resolvedReviewerName
    qualification = $resolvedQualification
    date = $publicationDate
    disposition = 'approved'
    url = $resolvedCommentUrl
}
```

The controller shall supply the basis-specific resolved identity and HTTPS locator from the actual GitHub source. Repeat the object for the other two exact mapping-set IDs. For owner risk, use `tools/owner_risk_evidence.py` with a freshly fetched comment JSON source and do not commit any temporary JSON. Governance remains a separate Steering Committee approval.

For `qualified_approval`, acquire the three reviewer decisions as structured
JSON, not prose. Each reviewer comment body shall be exactly one JSON object
with `mapping_set_id`, `decision_type: qualified_approval`, exact
`$closureHead`, RFC3339 `decided_at`, nonempty `reviewer` and
`qualification`, `disposition: approved`,
`qualified_review_status: completed`, an HTTPS `url` equal to that
fetched comment's `html_url`, and limitations exactly
`lifecycle: draft` plus the seven `claims_not_made` values enforced by
the controller helper. Capture qualified decision comment IDs in fixed
temporary response files; later controller steps shall fetch those numeric IDs
again and reject any changed or incomplete source.

```powershell
function Assert-NativeSuccess([string]$operation) {
  if ($LASTEXITCODE -ne 0) { throw "$operation failed with exit $LASTEXITCODE" }
}
$temp = [IO.Path]::GetTempPath()
$closurePr = gh pr view --repo tdistress/ESAF agent/v04-alpha-publication-gates-closure --json number --jq '.number'
Assert-NativeSuccess 'Resolve closure PR for qualified decision acquisition'
$closureHead = gh pr view --repo tdistress/ESAF $closurePr --json headRefOid --jq '.headRefOid'
Assert-NativeSuccess 'Resolve closure head for qualified decision acquisition'
$publicationDate = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')
$expectedMappingIds = @(
  'uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0',
  'uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0',
  'uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0'
)
$expectedClaims = @('compliance','certification','equivalence','endorsement','external_scheme_approval','assurance','production_readiness')
$commentFeedPath = Join-Path $temp 'esaf-v04-qualified-comment-feed.json'
gh api "repos/tdistress/ESAF/issues/$closurePr/comments?per_page=100" |
  Set-Content -LiteralPath $commentFeedPath -Encoding utf8
Assert-NativeSuccess 'Fetch qualified decision comments'
$commentFeed = Get-Content -Raw -LiteralPath $commentFeedPath | ConvertFrom-Json
for ($index = 0; $index -lt $expectedMappingIds.Count; $index++) {
  $mappingSetId = $expectedMappingIds[$index]
  $matches = @($commentFeed | Where-Object {
    try {
      $decision = [string]$_.body | ConvertFrom-Json
        $decision.mapping_set_id -eq $mappingSetId -and
        $decision.decision_type -eq 'qualified_approval' -and
        $decision.sha -eq $closureHead -and
        $decision.decided_at -match '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$' -and
        [DateTimeOffset]::Parse([string]$decision.decided_at).ToUniversalTime().ToString('yyyy-MM-dd') -eq $publicationDate -and
        -not [string]::IsNullOrWhiteSpace([string]$decision.reviewer) -and
        -not [string]::IsNullOrWhiteSpace([string]$decision.qualification) -and
        $decision.disposition -eq 'approved' -and
        $decision.qualified_review_status -eq 'completed' -and
        $decision.url -eq $_.html_url -and
        $decision.url -match '^https://' -and
        $decision.limitations.lifecycle -eq 'draft' -and
        ($decision.limitations.claims_not_made -join ',') -eq ($expectedClaims -join ',')
    } catch { $false }
  })
  if ($matches.Count -ne 1) { throw "Expected one structured qualified decision for $mappingSetId" }
  $responsePath = Join-Path $temp "esaf-v04-qualified-$index-response.json"
  [ordered]@{id=[long]$matches[0].id; url=$matches[0].html_url; mapping_set_id=$mappingSetId} |
    ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $responsePath -Encoding utf8
}
```

- [ ] **Step 4: Push and open closure PR B, then obtain governance approval**

```powershell
$closureHead = (git rev-parse HEAD).Trim()
git push -u origin agent/v04-alpha-publication-gates-closure
$closureBody = @"
Continues #39 after the validated evidence-candidate merge.

Closure candidate: $closureHead
Diff boundary: CHANGELOG.md, project/RELEASE_PLAN.md, the publication-readiness record, and two focused test modules only.
Publication condition: the recorded UTC date becomes effective only when remote annotated tag v0.4-alpha resolves to the exact post-merge validated commit.
Validation and reviews: include the exact Task 6 Step 2 outputs, reviewer identities, and dispositions before submitting.
Pending: exact-head scope evidence, the chosen uniform mapping-decision basis, and separate authorized governance approval on this exact head.

Draft artifacts remain Draft, with no compliance, certification, equivalence, endorsement, or production-readiness claim.
"@
gh pr create --repo tdistress/ESAF --base main --head agent/v04-alpha-publication-gates-closure --title "Close 0.4-alpha publication gates conditionally" --body $closureBody
$closurePr = gh pr view --repo tdistress/ESAF agent/v04-alpha-publication-gates-closure --json number --jq '.number'
```

The authorized Steering Committee approver shall comment with role/authority, exact `$closureHead`, the current UTC date, disposition `approved`, the condition that publication remains contingent on the remote annotated tag and post-merge gates, and limitations. Repository ownership without the governance role is insufficient.

- [ ] **Step 5: Fetch sources and build complete closure evidence before merge**

For `owner_risk_acceptance`, run this self-contained block immediately before
initial closure validation. It fetches immutable comment sources by numeric ID,
removes stale output, rebuilds evidence, and validates the rebuilt file. The
qualified branch below fetches and produces its own complete input before use.

```powershell
function Assert-NativeSuccess([string]$operation) {
  if ($LASTEXITCODE -ne 0) { throw "$operation failed with exit $LASTEXITCODE" }
}
$temp = [IO.Path]::GetTempPath()
$closurePr = gh pr view --repo tdistress/ESAF `
  agent/v04-alpha-publication-gates-closure --json number --jq '.number'
Assert-NativeSuccess 'Resolve closure PR for evidence construction'
$closureHead = gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid --jq '.headRefOid'
Assert-NativeSuccess 'Resolve closure head for evidence construction'
$responseNames = @('owner','scope','technical','editorial','rendering','governance')
$fetched = @{}
foreach ($name in $responseNames) {
  $responsePath = Join-Path $temp "esaf-v04-$name-response.json"
  $commentId = [long](Get-Content -Raw -LiteralPath $responsePath | ConvertFrom-Json).id
  $suffix = if ($name -eq 'owner') { 'owner-fetched' } else { "$name-fetched" }
  $fetchedPath = Join-Path $temp "esaf-v04-$suffix.json"
  gh api "repos/tdistress/ESAF/issues/comments/$commentId" |
    Set-Content -LiteralPath $fetchedPath -Encoding utf8
  Assert-NativeSuccess "Fetch $name comment for closure evidence"
  $fetched[$name] = $fetchedPath
}
$ownerFetchedPath = $fetched.owner
$technicalFetchedPath = $fetched.technical
$editorialFetchedPath = $fetched.editorial
$renderingFetchedPath = $fetched.rendering
$governanceFetchedPath = $fetched.governance
$prStatePath = Join-Path $temp 'esaf-v04-pr-state.json'
gh pr view --repo tdistress/ESAF $closurePr `
  --json headRefOid,mergeable,mergeStateStatus,statusCheckRollup |
  Set-Content -LiteralPath $prStatePath -Encoding utf8
Assert-NativeSuccess 'Fetch closure PR state for evidence construction'
$state = Get-Content -Raw -LiteralPath $prStatePath | ConvertFrom-Json
if ($state.headRefOid -ne $closureHead) { throw 'PR head changed during evidence construction' }
$publicationDate = python -c "from pathlib import Path; from tools.release_gates import load_front_matter; print(load_front_matter(Path('docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md'))['publication']['date'])"
Assert-NativeSuccess 'Read conditional publication date'
$verifiedAt = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$externalEvidence = Join-Path $temp 'esaf-v04-closure-external-evidence.json'
if (Test-Path -LiteralPath $externalEvidence) { Remove-Item -LiteralPath $externalEvidence }
$mappingDecisionBasis = python -c "from pathlib import Path; from tools.release_gates import load_front_matter; print(load_front_matter(Path('docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md'))['mapping_decision_basis'])"
Assert-NativeSuccess 'Resolve closure mapping decision basis'
if ($mappingDecisionBasis -eq 'owner_risk_acceptance') {
  $ownerFetched = Get-Content -Raw -LiteralPath $ownerFetchedPath | ConvertFrom-Json
  $ownerDigest = ([Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes([string]$ownerFetched.body)))).ToLowerInvariant()
  python tools/owner_risk_evidence.py --comment-json $ownerFetchedPath `
    --technical-comment-json $technicalFetchedPath `
    --editorial-comment-json $editorialFetchedPath `
    --rendering-comment-json $renderingFetchedPath `
    --governance-comment-json $governanceFetchedPath `
    --pr-state-json $prStatePath --expected-head $closureHead `
    --publication-date $publicationDate --verified-at $verifiedAt --output $externalEvidence
  Assert-NativeSuccess 'Build owner-risk closure evidence'
  $builtEvidence = Get-Content -Raw -LiteralPath $externalEvidence | ConvertFrom-Json
  if ($builtEvidence.mapping_decisions[0].source.body_sha256 -ne $ownerDigest) { throw 'Built owner evidence digest does not match fetched UTF-8 body' }
} elseif ($mappingDecisionBasis -eq 'qualified_approval') {
  $qualifiedInputsPath = Join-Path $temp 'esaf-v04-qualified-closure-input.json'
  $qualifiedResponsePaths = @(0..2 | ForEach-Object { Join-Path $temp "esaf-v04-qualified-$_-response.json" })
  $qualifiedCommentIds = @($qualifiedResponsePaths | ForEach-Object { [long](Get-Content -Raw -LiteralPath $_ | ConvertFrom-Json).id })
  if ($qualifiedCommentIds.Count -ne 3 -or @($qualifiedCommentIds | Select-Object -Unique).Count -ne 3) { throw 'Qualified closure input shall use exactly three fixed qualified comment IDs' }
  $qualifiedFetchedPaths = @()
  for ($index = 0; $index -lt $qualifiedCommentIds.Count; $index++) {
    $qualifiedCommentId = $qualifiedCommentIds[$index]
    $qualifiedFetchedPath = Join-Path $temp "esaf-v04-qualified-$index-fetched.json"
    gh api "repos/tdistress/ESAF/issues/comments/$qualifiedCommentId" |
      Set-Content -LiteralPath $qualifiedFetchedPath -Encoding utf8
    Assert-NativeSuccess "Fetch qualified decision $index for closure evidence"
    $qualifiedFetchedPaths += $qualifiedFetchedPath
  }
  $qualifiedInput = New-QualifiedInputFromSources $qualifiedFetchedPaths $qualifiedCommentIds $closureHead $publicationDate $fetched.scope $fetched.technical $fetched.editorial $fetched.rendering $fetched.governance $prStatePath
  $qualifiedInput | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $qualifiedInputsPath -Encoding utf8
  $qualifiedEvidence = New-QualifiedClosureEvidence $qualifiedInputsPath $closureHead
  $qualifiedEvidence | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $externalEvidence -Encoding utf8
} else { throw "Unsupported mapping decision basis: $mappingDecisionBasis" }
Assert-NativeSuccess 'Build closure evidence'
$closureBase = (git merge-base HEAD origin/main).Trim()
Assert-NativeSuccess 'Resolve closure baseline'
python tools/release_gates.py --check --baseline-ref $closureBase `
  --external-evidence $externalEvidence --expected-head $closureHead --phase closure
Assert-NativeSuccess 'Validate closure evidence'
```

Expected: release validator passes, GitHub checks pass, PR head equals `$closureHead`, PR is mergeable, and no tracked byte changed after approval.

- [ ] **Step 6: Immediately refresh every live source and merge PR B**

Run this uninterrupted fail-closed block. It refetches owner, technical,
editorial, rendering, governance, CI, and merge-state sources before rebuild
and merge; any changed source or failed validation stops before merge.

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
$responseNames = @('owner','scope','technical','editorial','rendering','governance')
$fetched = @{}
foreach ($name in $responseNames) {
  $responsePath = Join-Path $temp "esaf-v04-$name-response.json"
  $commentId = [long](Get-Content -Raw -LiteralPath $responsePath | ConvertFrom-Json).id
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
$priorEvidence = Get-Content -Raw -LiteralPath $externalEvidence | ConvertFrom-Json
$mappingDecisionBasis = [string]$priorEvidence.mapping_decision_basis
if (Test-Path -LiteralPath $externalEvidence) { Remove-Item -LiteralPath $externalEvidence }
if ($mappingDecisionBasis -eq 'owner_risk_acceptance') {
  $ownerFetched = Get-Content -Raw -LiteralPath $fetched.owner | ConvertFrom-Json
  $fetchedOwnerDigest = ([Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes([string]$ownerFetched.body)))).ToLowerInvariant()
  $ownerDigest = Assert-OwnerSourceUnchanged $priorEvidence.mapping_decisions[0].source $ownerFetched
  if ($ownerDigest -ne $fetchedOwnerDigest) { throw 'Owner source digest differs from the prior validated source' }
  python tools/owner_risk_evidence.py --comment-json $fetched.owner `
    --technical-comment-json $fetched.technical `
    --editorial-comment-json $fetched.editorial `
    --rendering-comment-json $fetched.rendering `
    --governance-comment-json $fetched.governance `
    --pr-state-json $prStatePath --expected-head $closureHead `
    --publication-date $publicationDate --verified-at $verifiedAt --output $externalEvidence
  Assert-NativeSuccess 'Rebuild owner-risk closure evidence'
  $rebuiltEvidence = Get-Content -Raw -LiteralPath $externalEvidence | ConvertFrom-Json
  if ($rebuiltEvidence.mapping_decisions[0].source.body_sha256 -ne $ownerDigest) { throw 'Rebuilt owner evidence digest differs from live source' }
} elseif ($mappingDecisionBasis -eq 'qualified_approval') {
  $qualifiedInputsPath = Join-Path $temp 'esaf-v04-qualified-prefetch-merge-input.json'
  $qualifiedCommentIds = @($priorEvidence.mapping_decisions.source.comment_id | ForEach-Object { [long]$_ })
  if ($qualifiedCommentIds.Count -ne 3 -or @($qualifiedCommentIds | Select-Object -Unique).Count -ne 3) { throw 'Qualified pre-merge input shall use exactly three fixed qualified comment IDs' }
  $qualifiedFetchedPaths = @()
  for ($index = 0; $index -lt $qualifiedCommentIds.Count; $index++) {
    $qualifiedCommentId = $qualifiedCommentIds[$index]
    $qualifiedFetchedPath = Join-Path $temp "esaf-v04-qualified-$index-prefetch-merge.json"
    gh api "repos/tdistress/ESAF/issues/comments/$qualifiedCommentId" |
      Set-Content -LiteralPath $qualifiedFetchedPath -Encoding utf8
    Assert-NativeSuccess "Refetch qualified decision $index before merge"
    $qualifiedFetchedPaths += $qualifiedFetchedPath
  }
  $qualifiedInput = New-QualifiedInputFromSources $qualifiedFetchedPaths $qualifiedCommentIds $closureHead $publicationDate $fetched.scope $fetched.technical $fetched.editorial $fetched.rendering $fetched.governance $prStatePath
  $qualifiedInput | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $qualifiedInputsPath -Encoding utf8
  $qualifiedEvidence = New-QualifiedClosureEvidence $qualifiedInputsPath $closureHead
  $qualifiedEvidence | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $externalEvidence -Encoding utf8
} else { throw "Unsupported mapping decision basis: $mappingDecisionBasis" }
Assert-NativeSuccess 'Rebuild closure evidence'
$closureBase = (git merge-base HEAD origin/main).Trim()
Assert-NativeSuccess 'Resolve closure baseline'
python tools/release_gates.py --check --baseline-ref $closureBase `
  --external-evidence $externalEvidence --expected-head $closureHead --phase closure
Assert-NativeSuccess 'Validate refreshed closure evidence'
if (@(git status --porcelain).Count -ne 0) { throw 'Closure worktree changed after approval' }
gh pr merge --repo tdistress/ESAF $closurePr --merge
Assert-NativeSuccess 'Merge closure PR'
$mergedState = gh pr view --repo tdistress/ESAF $closurePr `
  --json state,mergedAt,mergeCommit,headRefOid | ConvertFrom-Json
Assert-NativeSuccess 'Verify closure merge'
if ($mergedState.state -ne 'MERGED') { throw 'Closure PR did not merge' }
```

Expected: PR state `MERGED`; capture the exact merge commit as `$closureMerge`. Do not create the tag yet.

### Task 7: Validate merged main, publish the annotated tag, close issue #39, and clean up

**Files:**
- No tracked file changes.
- Modify outside repository: `closure-external-evidence.json` with exact merge and post-merge results.

**Interfaces:**
- Consumes: merged PR B, exact `$closureMerge`, the conditional UTC date stored in the readiness record, passing post-merge gates, external approvals, and issue #39.
- Produces: remote annotated tag `v0.4-alpha` peeled to `$closureMerge`, complete issue evidence, closed issue #39, updated clean `main`, and removed owned release branches/worktrees.

- [ ] **Step 1: Update local main and verify exact merge identity**

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
git -C $mainRoot pull --ff-only origin main
Set-Location -LiteralPath $mainRoot
$closureMerge = (git -C $mainRoot rev-parse HEAD).Trim()
$remoteMain = (git -C $mainRoot rev-parse origin/main).Trim()
if ($closureMerge -ne $remoteMain) { throw 'Local main and origin/main differ' }
$publicationDate = python -c "from pathlib import Path; from tools.release_gates import load_front_matter; print(load_front_matter(Path('docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md'))['publication']['date'])"
if ((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd') -ne $publicationDate.Trim()) { throw 'Conditional publication date expired; create and review a new closure candidate' }
```

- [ ] **Step 2: Run every post-merge gate on unchanged `$closureMerge`**

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
Set-Location -LiteralPath $mainRoot
$env:PYTHONDONTWRITEBYTECODE='1'
$closureMerge = (git rev-parse HEAD).Trim()
$evidenceMerge = (git rev-parse 'HEAD^1').Trim()
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/migrate_control_mappings.py --check
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref $evidenceMerge
python tools/validate_links.py --check
python tools/release_gates.py --check --baseline-ref $evidenceMerge
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md
git diff --check "$evidenceMerge..HEAD"
$cacheDirs = @(Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue)
if ($cacheDirs.Count -ne 0) { throw "Cache directories found: $($cacheDirs.Count)" }
if (@(git status --porcelain).Count -ne 0) { throw 'Merged main is not clean' }
```

Rerender all Mermaid blocks only if the inventory digest differs from the exact reviewed closure inventory. Because Task 5's allowlist forbids Mermaid changes, digest identity is the expected result; any difference blocks publication.

- [ ] **Step 3: Complete external taggable evidence and validate it**

Create the post-merge JSON from the exact Task 7 Step 2 results. Do not mutate
the validated closure evidence; the next step rebuilds a separate taggable
evidence file from a fresh fetched owner source.

Run:

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
Set-Location -LiteralPath $mainRoot
$currentMain = (git rev-parse HEAD).Trim()
$postMergePath = Join-Path ([IO.Path]::GetTempPath()) 'esaf-v04-post-merge.json'
@{sha=$currentMain; commands=$commands} | ConvertTo-Json -Depth 6 |
  Set-Content -LiteralPath $postMergePath -Encoding utf8
```

Expected: the post-merge input is ready for the fresh taggable-evidence rebuild.

- [ ] **Step 4: Create and push the annotated tag atomically after validation**

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
$mappingDecisionBasis = [string]$baseEvidence.mapping_decision_basis
$closureMerge = (git rev-parse HEAD).Trim()
Assert-NativeSuccess 'Resolve closure merge before tag'
$evidenceMerge = (git rev-parse 'HEAD^1').Trim()
Assert-NativeSuccess 'Resolve evidence baseline before tag'
$publicationDate = python -c "from pathlib import Path; from tools.release_gates import load_front_matter; print(load_front_matter(Path('docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md'))['publication']['date'])"
Assert-NativeSuccess 'Read publication date before tag'
$verifiedAt = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
if (Test-Path -LiteralPath $taggableEvidence) { Remove-Item -LiteralPath $taggableEvidence }
if ($mappingDecisionBasis -eq 'owner_risk_acceptance') {
  $ownerCommentId = [long]$baseEvidence.mapping_decisions[0].source.comment_id
  $ownerFetchedPath = Join-Path ([IO.Path]::GetTempPath()) 'esaf-v04-owner-prefetch-tag.json'
  gh api "repos/tdistress/ESAF/issues/comments/$ownerCommentId" |
    Set-Content -LiteralPath $ownerFetchedPath -Encoding utf8
  Assert-NativeSuccess 'Refetch owner source before tag'
  $ownerFetched = Get-Content -Raw -LiteralPath $ownerFetchedPath | ConvertFrom-Json
  $fetchedOwnerDigest = ([Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes([string]$ownerFetched.body)))).ToLowerInvariant()
  $ownerDigest = Assert-OwnerSourceUnchanged $baseEvidence.mapping_decisions[0].source $ownerFetched
  if ($ownerDigest -ne $fetchedOwnerDigest) { throw 'Owner source digest differs from the prior validated source' }
  python tools/owner_risk_evidence.py --comment-json $ownerFetchedPath `
    --base-evidence $externalEvidence --expected-head $closureHead `
    --publication-date $publicationDate --verified-at $verifiedAt `
    --merge-head $closureMerge --post-merge-json $postMergePath --output $taggableEvidence
  Assert-NativeSuccess 'Build refreshed owner-risk taggable evidence'
  $rebuiltEvidence = Get-Content -Raw -LiteralPath $taggableEvidence | ConvertFrom-Json
  if ($rebuiltEvidence.mapping_decisions[0].source.body_sha256 -ne $ownerDigest) { throw 'Taggable owner evidence digest differs from live source' }
} elseif ($mappingDecisionBasis -eq 'qualified_approval') {
  $qualifiedInputsPath = Join-Path ([IO.Path]::GetTempPath()) 'esaf-v04-qualified-taggable-input.json'
  $qualifiedCommentIds = @($baseEvidence.mapping_decisions.source.comment_id | ForEach-Object { [long]$_ })
  if ($qualifiedCommentIds.Count -ne 3 -or @($qualifiedCommentIds | Select-Object -Unique).Count -ne 3) { throw 'Qualified taggable input shall use exactly three fixed qualified comment IDs' }
  $qualifiedFetchedPaths = @()
  for ($index = 0; $index -lt $qualifiedCommentIds.Count; $index++) {
    $qualifiedCommentId = $qualifiedCommentIds[$index]
    $qualifiedFetchedPath = Join-Path ([IO.Path]::GetTempPath()) "esaf-v04-qualified-$index-prefetch-tag.json"
    gh api "repos/tdistress/ESAF/issues/comments/$qualifiedCommentId" |
      Set-Content -LiteralPath $qualifiedFetchedPath -Encoding utf8
    Assert-NativeSuccess "Refetch qualified decision $index before tag"
    $qualifiedFetchedPaths += $qualifiedFetchedPath
  }
  $qualifiedInput = New-QualifiedInputFromSources -QualifiedFetchedPaths $qualifiedFetchedPaths -ExpectedCommentIds $qualifiedCommentIds -ClosureHead $closureHead -PublicationDate $publicationDate -BaseEvidence $baseEvidence
  $qualifiedInput | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $qualifiedInputsPath -Encoding utf8
  $qualifiedEvidence = New-QualifiedTaggableEvidence $qualifiedInputsPath $closureHead $closureMerge $postMergePath
  $qualifiedEvidence | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $taggableEvidence -Encoding utf8
} else { throw "Unsupported mapping decision basis: $mappingDecisionBasis" }
Assert-NativeSuccess 'Build refreshed taggable evidence'
python tools/release_gates.py --check --baseline-ref $evidenceMerge --external-evidence $taggableEvidence --expected-head $closureMerge --phase taggable
Assert-NativeSuccess 'Validate refreshed taggable evidence'
$validatedEvidence = Get-Content -Raw -LiteralPath $taggableEvidence | ConvertFrom-Json
$validatedMerge = [string]$validatedEvidence.merge_head
$mappingDecisionBasis = [string]$validatedEvidence.mapping_decision_basis
$mappingIds = ($validatedEvidence.mapping_decisions.mapping_set_id -join ', ')
if ($mappingDecisionBasis -eq 'owner_risk_acceptance') {
  $mappingDecisionSummary = "Repository-owner risk acceptance for $mappingIds; qualified review is deferred and backlog retention covers all three mapping-set IDs."
  $owner = $validatedEvidence.mapping_decisions[0].source
  $ownerComparison = 'passed: live fetched comment matched the validated ID, URL, author, association, timestamps, and SHA-256 body digest'
  $ownerDetail = "Owner source: $($owner.comment_url); comment $($owner.comment_id); body SHA-256 $($owner.body_sha256)."
} elseif ($mappingDecisionBasis -eq 'qualified_approval') {
  $mappingDecisionSummary = "Qualified approval is completed for $mappingIds."
  $ownerComparison = 'not applicable: qualified approval basis'
  $ownerDetail = 'Owner source: not applicable for qualified approval.'
} else { throw "Unsupported mapping decision basis: $mappingDecisionBasis" }
git fetch origin main
Assert-NativeSuccess 'Fetch origin main before tag'
$currentMain = (git rev-parse HEAD).Trim()
Assert-NativeSuccess 'Resolve local main before tag'
$remoteMain = (git rev-parse origin/main).Trim()
Assert-NativeSuccess 'Resolve remote main before tag'
if ($currentMain -ne $validatedMerge -or $remoteMain -ne $validatedMerge) { throw 'HEAD, origin/main, and validated merge differ' }
if (@(git status --porcelain).Count -ne 0) { throw 'Main worktree is not clean' }
if ((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd') -ne $publicationDate.Trim()) { throw 'Conditional publication date expired' }
if (@(git tag --list 'v0.4-alpha').Count -ne 0) { throw 'Local v0.4-alpha already exists' }
if (@(git ls-remote --tags origin 'refs/tags/v0.4-alpha').Count -ne 0) { throw 'Remote v0.4-alpha already exists' }
python tools/release_gates.py --check --baseline-ref $evidenceMerge --external-evidence $taggableEvidence --expected-head $closureMerge --phase taggable
Assert-NativeSuccess 'Revalidate refreshed taggable evidence before tag'
$tagMessage = @"
ESAF 0.4-alpha Working Draft

Validated commit: $validatedMerge
Evidence: https://github.com/tdistress/ESAF/issues/39
Mapping decision basis: $mappingDecisionBasis. $mappingDecisionSummary
Lifecycle boundary: Draft artifacts remain Draft; this tag does not claim compliance, certification, equivalence, endorsement, or production readiness.
"@
git tag -a v0.4-alpha $validatedMerge -m $tagMessage
Assert-NativeSuccess 'Create annotated v0.4-alpha tag'
git push origin refs/tags/v0.4-alpha
Assert-NativeSuccess 'Push annotated v0.4-alpha tag'
```

Do not move or recreate the tag if push verification fails. Diagnose the exact remote state first.

- [ ] **Step 5: Resolve the remote annotated tag to the exact commit**

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
Set-Location -LiteralPath $mainRoot
$taggableEvidence = Join-Path ([IO.Path]::GetTempPath()) 'esaf-v04-taggable-external-evidence.json'
$evidence = Get-Content -Raw -LiteralPath $taggableEvidence | ConvertFrom-Json
$validatedMerge = [string]$evidence.merge_head
git fetch origin tag v0.4-alpha --force
$localPeeled = (git rev-parse 'v0.4-alpha^{commit}').Trim()
$remoteRows = @(git ls-remote --tags origin 'refs/tags/v0.4-alpha' 'refs/tags/v0.4-alpha^{}')
$remotePeeled = (($remoteRows | Where-Object { $_ -match '\^\{\}$' }) -split '\s+')[0]
if ($localPeeled -ne $validatedMerge -or $remotePeeled -ne $validatedMerge) { throw 'Published tag does not peel to validated closure merge' }
```

- [ ] **Step 6: Record publication evidence and close issue #39**

Post one consolidated issue comment containing PR A head/merge, PR B head/merge, tag object and peeled commit, every command/count, 23/23 renderer result, technical/editorial/rendering verdicts, the uniform mapping decision basis and three exact decisions, separate governance approval, GitHub check URLs, clean merge state, lifecycle limitations, and zero unresolved Critical/Important findings. When the basis is owner risk, include the deferred-review backlog IDs and fetched-comment SHA-256 body comparison. Replace any superseded result rather than appending contradictory totals.

The controller shall supply `$finalGateSummary` from the exact Task 7 Steps 2–3 outputs and `$finalReviewSummary` from the approved external-evidence objects. Use those resolved values to post the consolidated comment, then close the issue:

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
Set-Location -LiteralPath $mainRoot
$taggableEvidence = Join-Path ([IO.Path]::GetTempPath()) 'esaf-v04-taggable-external-evidence.json'
$evidence = Get-Content -Raw -LiteralPath $taggableEvidence | ConvertFrom-Json
$validatedMerge = [string]$evidence.merge_head
$mappingDecisionBasis = [string]$evidence.mapping_decision_basis
$mappingIds = ($evidence.mapping_decisions.mapping_set_id -join ', ')
if ($mappingDecisionBasis -eq 'owner_risk_acceptance') {
  $mappingDecisionSummary = "Repository-owner risk acceptance for $mappingIds; qualified review is deferred and backlog retention covers all three mapping-set IDs."
  $owner = $evidence.mapping_decisions[0].source
  $ownerComparison = 'passed: live fetched comment matched the validated ID, URL, author, association, timestamps, and SHA-256 body digest'
  $ownerDetail = "Owner source: $($owner.comment_url); comment $($owner.comment_id); body SHA-256 $($owner.body_sha256)."
} elseif ($mappingDecisionBasis -eq 'qualified_approval') {
  $mappingDecisionSummary = "Qualified approval is completed for $mappingIds."
  $ownerComparison = 'not applicable: qualified approval basis'
  $ownerDetail = 'Owner source: not applicable for qualified approval.'
} else { throw "Unsupported mapping decision basis: $mappingDecisionBasis" }
$finalGateSummary = ($evidence.post_merge.commands | ForEach-Object {
  "$($_.name): $($_.result)"
}) -join '; '
$finalReviewSummary = "technical $($evidence.technical.url); editorial $($evidence.editorial.url); rendering $($evidence.rendering.url); governance $($evidence.governance.url)"
$closurePr = gh pr view --repo tdistress/ESAF agent/v04-alpha-publication-gates-closure --json number --jq '.number'
$closureHead = gh pr view --repo tdistress/ESAF $closurePr --json headRefOid --jq '.headRefOid'
$evidencePr = gh pr view --repo tdistress/ESAF agent/v04-alpha-publication-gates-design --json number --jq '.number'
$evidenceHead = gh pr view --repo tdistress/ESAF $evidencePr --json headRefOid --jq '.headRefOid'
$evidenceMerge = gh pr view --repo tdistress/ESAF $evidencePr --json mergeCommit --jq '.mergeCommit.oid'
$tagObject = (git rev-parse v0.4-alpha).Trim()
if ([string]::IsNullOrWhiteSpace($finalGateSummary)) { throw 'Controller did not supply the exact Task 7 gate summary' }
if ([string]::IsNullOrWhiteSpace($finalReviewSummary)) { throw 'Controller did not supply the exact approved-review summary' }
$evidenceComment = @"
0.4-alpha publication evidence

- Evidence PR: #$evidencePr; reviewed head $evidenceHead; merge $evidenceMerge.
- Closure PR: #$closurePr; reviewed head $closureHead; merge $validatedMerge.
- Annotated tag: object $tagObject; peeled commit $validatedMerge.
- Renderer: 23/23 Mermaid blocks parsed and passed readability review with @mermaid-js/mermaid-cli@11.16.0.
- Repository gates: $finalGateSummary
- Reviews: $finalReviewSummary
- Mapping decision: $mappingDecisionBasis; $mappingDecisionSummary
- $ownerDetail
- Owner source live comparison: $ownerComparison
- Findings: Critical 0; Important 0; every accepted Minor includes its owner and rationale.
- Lifecycle: all architecture, control, and mapping artifacts retain their existing Draft state. Publication claims no compliance, certification, equivalence, endorsement, external-scheme approval, or production readiness.
"@
gh issue comment 39 --repo tdistress/ESAF --body $evidenceComment
gh issue close 39 --repo tdistress/ESAF --comment "0.4-alpha publication gates are closed. Basis: $mappingDecisionBasis. Remote annotated tag v0.4-alpha resolves to validated commit $validatedMerge. See the preceding consolidated evidence comment for exact results, deferred-review status where applicable, and lifecycle limitations."
```

- [ ] **Step 7: Clean branches/worktrees and verify final repository state**

From `$mainRoot`, verify the exact owned worktree paths lie under `.worktrees`, remove them, prune registrations, delete merged local branches, and delete their remote branches. Do not touch the unrelated `agent/task2-mapping-set-counts` or `agent/task2-validation` worktrees.

```powershell
$gitCommon = (git rev-parse --path-format=absolute --git-common-dir).Trim()
$mainRoot = Split-Path -Parent $gitCommon
$externalEvidence = Join-Path ([IO.Path]::GetTempPath()) 'esaf-v04-closure-external-evidence.json'
$validatedMerge = ((Get-Content -Raw -LiteralPath $externalEvidence | ConvertFrom-Json).merge_head).Trim()
$ownedWorktrees = @(
    (Join-Path $mainRoot '.worktrees\agent-v04-alpha-publication-gates-design'),
    (Join-Path $mainRoot '.worktrees\agent-v04-alpha-publication-gates-closure')
)
$worktreeRoot = [IO.Path]::GetFullPath((Join-Path $mainRoot '.worktrees')) + [IO.Path]::DirectorySeparatorChar
git -C $mainRoot worktree list --porcelain
foreach ($ownedWorktree in $ownedWorktrees) {
    $resolvedWorktree = [IO.Path]::GetFullPath($ownedWorktree)
    if (-not $resolvedWorktree.StartsWith($worktreeRoot, [StringComparison]::OrdinalIgnoreCase)) { throw "Refusing to remove out-of-scope worktree: $resolvedWorktree" }
    if (Test-Path -LiteralPath $resolvedWorktree) { git -C $mainRoot worktree remove $resolvedWorktree }
}
git -C $mainRoot worktree prune
git -C $mainRoot branch -d agent/v04-alpha-publication-gates-design
git -C $mainRoot branch -d agent/v04-alpha-publication-gates-closure
if (git -C $mainRoot ls-remote --heads origin agent/v04-alpha-publication-gates-design) { git -C $mainRoot push origin --delete agent/v04-alpha-publication-gates-design }
if (git -C $mainRoot ls-remote --heads origin agent/v04-alpha-publication-gates-closure) { git -C $mainRoot push origin --delete agent/v04-alpha-publication-gates-closure }
git -C $mainRoot status --short --branch
git -C $mainRoot rev-parse HEAD
git -C $mainRoot rev-parse origin/main
git -C $mainRoot rev-parse 'v0.4-alpha^{commit}'
```

Expected: clean `main`; local main, origin/main, and peeled tag all equal `$validatedMerge`; issue #39 is closed; only unrelated pre-existing worktrees remain.

## Execution stop conditions

Stop immediately and preserve a clean, recoverable state when any of these occurs:

- a Critical or Important finding remains unresolved;
- a reviewer lacks the required independence, mapping qualification, or governance authority;
- any exact candidate SHA changes after approval without complete affected re-review;
- any Mermaid block fails to parse or readability review;
- any validator, full suite, link, diff, cache, or cleanliness gate fails;
- GitHub checks are pending or failing, the PR is not mergeable, or the observed PR head differs from the reviewed head;
- the closure diff contains a path outside the five-file allowlist;
- the current UTC date differs from the conditional publication date;
- local main, origin/main, closure merge, or tag targets disagree; or
- `v0.4-alpha` already exists locally or remotely.

Do not weaken a validator, broaden an allowlist, change a lifecycle state, or rewrite a tag to bypass a stop condition. Add a focused regression for any discovered defect when practical, correct the source, create a new candidate, and rerun the invalidated gates.
