# Validation workflow security hardening implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make validation planning fail closed, bind emitted commands to the reviewed candidate, and reliably contain timed-out Mermaid renderer processes.

**Architecture:** The reviewed Python module owns all executable commands and routing rules. The planner computes a natural route before applying optional tiers, rejects attempted down-tiering of publication work, and adds full cleanliness only when exact proof is selected. Mermaid rendering owns a bounded, platform-aware process-tree helper.

**Tech Stack:** Python 3.13, `unittest`, Git, GitHub Actions YAML, Windows `taskkill`, POSIX process groups.

## Global constraints

- Do not load executable command definitions or route policy from candidate-controlled JSON.
- Keep CI concurrency, four-shard matrix, `fail-fast: false`, and aggregate check unchanged.
- Keep Node 22.23.1, Mermaid CLI 11.16.0, and the tracked Puppeteer configuration unchanged.
- Unknown, deleted, renamed, review-evidence, release-metadata, workflow, tool, test, and planner-policy changes are publication work.
- A publication plan cannot be reduced to quick or standard.
- Never terminate global browser processes. Target only the renderer child tree.
- Use humanizer for every human-facing documentation edit.

---

### Task 1: Move planner policy into reviewed code

**Files:**

- Delete: `tools/validation-plans.json`
- Modify: `tools/plan_validation.py`
- Modify: `tests/test_plan_validation.py`

**Interfaces:**

- Produces immutable `COMMAND_CATALOG`, `ROUTING_RULES`, `PUBLICATION_COMMAND_IDS`, and `PROOF_COMMAND_IDS`.
- Replaces `load_manifest(root)` with policy validation over supplied immutable records.

- [ ] Write failing tests that reject invalid in-memory policies and assert the committed catalog’s exact identifiers, ordered publication sequence, and argv templates.
- [ ] Run `python -B -m unittest tests/test_plan_validation.py -v` and observe failure because the JSON loader still defines policy.
- [ ] Define frozen reviewed policy records in `tools/plan_validation.py`; bind link validation to `--check`, preflight to `git diff --check {base} {candidate}`, and proof to `--check --candidate-sha {candidate}`.
- [ ] Exclude commands that require human evidence, stateful output, or arbitrary input parameters.
- [ ] Delete the JSON policy file and update tests to construct synthetic `ValidationPolicy` records directly.
- [ ] Run focused planner tests and `python tools/validate_test_shards.py --check`.
- [ ] Commit: `refactor: keep validation policy in reviewed code`.

### Task 2: Enforce candidate state, escalation, and safe rendering

**Files:**

- Modify: `tools/plan_validation.py`
- Modify: `tests/test_plan_validation.py`

**Interfaces:**

- `plan_validation(...)` returns an immutable natural plan before CLI tier filtering.
- `main()` rejects `--tier quick|standard` for a publication natural plan.

- [ ] Write failing tests for publication down-tier rejection; exact publication catalog on `--tier publication`; base ancestry; candidate equals HEAD; tracked-clean checkout; proof-bearing all-file cleanliness; and ordinary plans with unrelated untracked files.
- [ ] Add failing route tests for review evidence, `VERSION.md`, release metadata, policy source, workflow, tools, tests, deleted/renamed/unknown paths, and ordinary docs/qualified-review paths.
- [ ] Add failing text-output tests containing newline, ANSI, quote, and control characters in changed paths and reasons.
- [ ] Run the focused suite and observe the expected failures.
- [ ] Implement natural-route selection, non-bypassable publication semantics, proof-aware full status check, and JSON-quoted text fields and argv tokens.
- [ ] Run focused planner tests and representative text/JSON planner commands.
- [ ] Commit: `fix: harden validation plan candidate binding`.

### Task 3: Make Mermaid process cleanup platform-aware and verifiable

**Files:**

- Modify: `tools/mermaid_inventory.py`
- Modify: `tests/test_mermaid_inventory.py`

**Interfaces:**

- `_run_renderer(...)` starts a dedicated POSIX session and bounded renderer process.
- `_terminate_timed_out_renderer(...)` targets only the timed-out renderer tree and returns bounded cleanup disposition.

- [ ] Write failing Windows and POSIX tests for process-tree termination, bounded drain, partial-output cleanup, and stable block-specific errors when tree termination or cleanup fails.
- [ ] Run the focused Mermaid module and observe failure before changing production code.
- [ ] Use `taskkill /PID <pid> /T /F` on Windows and `os.killpg(pid, signal.SIGKILL)` for a dedicated POSIX session. Keep all waits bounded.
- [ ] Report inability to terminate or clean up as a stable validation failure without claiming successful deletion or termination.
- [ ] Run `python -B -m unittest tests/test_mermaid_inventory.py -v` and the private pinned Mermaid record gate.
- [ ] Commit: `fix: verify timed-out Mermaid cleanup`.

### Task 4: Update documentation, CI trigger coverage, and candidate evidence

**Files:**

- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tests/test_validation_shards.py`
- Modify: `tests/test_esaf_1600_foundation.py`
- Modify: `tools/README.md`
- Modify: `AGENTS.md`

- [ ] Write failing workflow tests that remove the deleted JSON policy path and retain the Python policy source, concurrency, matrix, `fail-fast: false`, operational gates, and aggregate job.
- [ ] Run focused workflow tests and observe the expected path-list failure.
- [ ] Update trigger lists and expected-path tests.
- [ ] Humanize the contributor guidance: static policy, non-bypassable publication routes, proof-only full cleanliness, quoted output, and best-effort renderer cleanup.
- [ ] Run focused planner, Mermaid, shard, workflow, and foundation suites; manifest validation; private pinned Mermaid record gate; and whole-branch diff checks.
- [ ] Create a fresh detached worktree at the candidate and run full discovery there.
- [ ] Commit: `docs: explain hardened validation workflow`.

## Plan self-review

- The four tasks cover every final-review blocker and preserve required CI behavior.
- Static policy and planner enforcement are isolated from renderer cleanup.
- Every changed production behavior begins with a focused failing test.
- Final validation requires a clean detached worktree and redispatched security and specification reviews on the final SHA.
