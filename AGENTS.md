# Codex Working Memory for ESAF

These instructions preserve durable project conventions for future Codex development sessions in this repository.

## Project intent

- ESAF is a vendor-neutral, implementation-focused enterprise AI standard, not a marketing document or a collection of disconnected guidance.
- Preserve the three strategic pillars: Protect AI, Utilize AI, and Govern AI.
- Organize requirements around the enterprise AI lifecycle and maintain traceability from business purpose through risk, architecture, controls, evidence, assessment, and continuous improvement.
- Treat Markdown as the authoritative source. Generated websites, PDFs, Word documents, diagrams, and workbooks are downstream artifacts.
- Keep normative standard content concise. Put examples, optional implementation detail, and industry-specific elaboration in companion material.

## Editorial and architecture conventions

- Use `shall` for mandatory requirements, `should` for recommendations, and `may` for optional capabilities.
- Follow the repository style guide, templates, identifiers, and registries rather than inventing parallel structures.
- Preserve the established control families, control-objective layer, evidence model, maturity model, and architecture-pattern taxonomy.
- Keep framework mappings evidence-based. Do not claim equivalence or compliance without a verified requirement-level mapping.
- Treat diagrams as publication content: number them, keep labels readable, and validate every Mermaid block with the current Mermaid CLI before publication.
- Mermaid sequence-diagram messages must avoid semicolons because Mermaid treats them as statement delimiters.

## Development workflow

1. Start from an up-to-date, clean `main` branch.
2. Use a short-lived `agent/<scope>` branch and an isolated worktree for substantive work.
3. For substantial additions, progress through design, implementation plan, implementation, independent review, publication validation, and a reviewable pull request.
4. Use test-driven development for validators, automation, and enforceable document invariants.
5. Review the complete branch diff, not only the latest commit.
6. Record the reviewed head SHA in the pull-request description and ensure it still matches the PR head before merge.
7. Require passing GitHub checks and a clean merge state before merging.
8. After merge, update local `main`, rerun proportional validation, verify a clean worktree, then remove the temporary branch and worktree.
9. For short work sessions, start with `python tools/plan_validation.py --base origin/main --candidate HEAD` and use the route selected for the current candidate. The planner's catalog and routing policy are static reviewed Python records, and its diagnostic output JSON-quotes paths, reasons, and command arguments. Treat duration labels as estimates, not deadlines. Unknown, renamed, deleted, workflow, and validation-tool paths shall use the publication tier. A publication route cannot be reduced to quick or standard. Full cleanliness is required only when exact-SHA proof is selected; ordinary routes may have unrelated untracked artifacts. Required CI and publication gates remain authoritative, and every earlier validation result expires when the candidate SHA changes.
10. Use `python tools/run_test_shards.py --all --parallel --durations 50` when concurrent local shard feedback is useful. Retain sequential `--all` mode when ordered diagnostics are needed; parallel execution shall collect every selected shard result.

## Required validation habits

- Run focused tests for the artifact being changed.
- Run the full test suite with `python -m unittest discover -s tests -v`.
- Run `python tools/validate_assessment.py --check` when assessment content,
  schemas, examples, or their references may be affected.
- Run `python tools/validate_controls.py --check` when controls or their references may be affected.
- Run `python tools/validate_architectures.py` when architecture content or links may be affected.
- Run ordinary working-tree checks such as `git diff --check` during development, then run `git diff --check <merge-base>..HEAD` for final whole-branch review; ensure generated caches or build outputs are not committed.
- Render every Mermaid diagram, not merely count fenced blocks. A syntactically valid Markdown file can still contain a Mermaid parse failure.
- For a timed-out Mermaid renderer, make a bounded best-effort attempt to terminate only its process tree and clean up partial output. Treat a failed termination, drain, or cleanup as a validation failure.
- Do not claim success from prior evidence after the branch head changes; rerun the affected gates.

## Review discipline

- Use independent subagents when tasks can be safely separated, particularly for architecture options, threat review, specification review, and final whole-branch review.
- Resolve Critical and Important findings before publication. Record why any lower-severity finding is accepted or deferred.
- When a publication gate discovers a defect, add a focused regression test before fixing it when practical.
- Preserve unrelated user changes and avoid destructive Git operations.
- Keep traceability statements synchronized with the exact candidate SHA and the actual results of every required gate.
- In task reports, replace superseded totals or conclusions rather than retaining contradictory earlier statements followed by corrections.

## Crosswalk development lessons

- Pin authoritative external sources by official URL, version, publication date, and checksum. Lock provision identifiers, summaries, and locators in a machine-readable oracle when feasible.
- Default to `no_direct_mapping` when ESAF does not expressly provide the external outcome. Conditions may narrow or qualify an existing relationship, but they must not supply a missing external outcome.
- Distinguish `prerequisite` from `partially_supports` using exact normative control text; implementation guidance and adjacent capabilities are insufficient by themselves.
- Treat whitespace-only mapping-record edits as snapshot changes when registries or catalogs use content digests. Regenerate and validate every dependent artifact.
- Derive published statistics from records and manifests. Keep the pinned control population, relationship-leg count, distinct referenced-control count, and negative-disposition count separate.
- Keep adjacent assurance schemes independently sourced and mapped; do not infer one scheme's requirements or assurance from another.
- For substantial crosswalks, require separate specification/inventory and security/overclaiming reviews on the exact final SHA. Redispatch both reviews after any candidate change.

## Collaboration preferences

- The repository owner prefers autonomous progress with concise commentary updates and outcome-focused handoffs.
- For work scoped to `tdistress/ESAF`, the owner has authorized Codex to create branches and worktrees, edit files, commit, push, open and update pull requests, merge passing PRs, and clean up temporary branches and worktrees.
- Within the approved task scope, Codex may choose and execute its recommended design and implementation approach without requesting intermediate approval. Ask only when a decision requires new authority, materially broadens scope, or carries significant external risk.
- Use subagents whenever they add useful parallelism or independent review. Codex does not need separate approval to dispatch them for in-scope work.
- Do not extend this authorization to other repositories, accounts, publishing destinations, permissions, credentials, or materially broader project scope.
- When the owner asks to pause, leave the repository in a clean, recoverable state and stop new milestone work.

## Durable implementation lessons

- Content-level regression tests are valuable but do not replace renderer validation.
- Local browser sessions may not be authenticated for private GitHub repositories even when `gh` is authenticated; distinguish GitHub visual verification from local renderer verification accurately.
- PowerShell command substitution can collapse multiline PR descriptions. Use a literal here-string or a purpose-built GitHub tool when updating multiline bodies.
- `gh pr merge --delete-branch` can merge successfully and then fail during local branch deletion when another worktree owns the base branch. Verify PR state before retrying, then clean branches and worktrees separately.
- Set `PYTHONDONTWRITEBYTECODE=1` during Python validation and verify that no `__pycache__` directories remain before declaring the checkout clean.
- On Windows, deeply nested project-local worktrees can make tracked files unreadable to Python or PowerShell even when Git reports a clean checkout. Use a short drive alias, run tests and tools through it, and verify the longest tracked paths before diagnosing missing repository content.
- Before advancing a release record into a one-way gated phase, land prerequisite fixes first. Once the repository is in a closure phase, an otherwise valid standalone repair may fail the required transition or exact changed-path gate. Use only the gate's documented recovery or next-transition path, satisfy that transition's prerequisites independently, and treat the repaired head as a new exact-SHA candidate requiring complete affected-gate validation and review.
- Tests that depend on mutable repository state such as tags, refs, branches, or worktrees must inject deterministic fixtures for the intended state and retain explicit negative tests for fail-closed behavior. Never assume a release tag is absent merely because it did not exist when the test was written.
- Treat authenticated API responses and transport caches used as release evidence as acquisition-scoped. Consume or clear cached responses before reacquisition, reacquire external evidence after intervening validation, and fail closed if the refreshed head, base, or source identity drifts.
- A publication-phase transition must synchronize every public status surface, including `README.md`, `VERSION.md`, the changelog, roadmap, release plan, backlog, milestones, and the authoritative readiness record. Phase-aware regression tests should reject stale prior-phase wording and obsolete active/completed tracker placement.
- Git operations can succeed while maintenance or pruning emits a warning about an inaccessible unrelated worktree. Verify the exit code and the intended refs or worktree metadata, as applicable, before retrying; do not modify the unrelated worktree to silence the warning.
- For staged equivalence migrations, record the sealed proof SHA, case-population digest, and hashes of proof-critical files. After sealing the proof, limit changes to the explicit migration path set. Any proof-critical change starts a new proof and exact-SHA review cycle.
- Fetch `origin/main` immediately before publishing a pull request and record the validation merge base. If the base has advanced, integrate the change and rerun every affected validation and exact-head review before opening or merging the pull request.
- When a validator binds its result to a candidate SHA, rerun it on the merged `main` commit after the pull request merges. The pull-request head and merge commit are different candidates even when their tree content is identical.
- Do not recursively remove a pnpm-managed temporary directory solely because the task created it. Remove only components proved private to the task. If pnpm links, protected entries, or shared-store ownership make that unsafe, leave the remainder in place and report its exact path.

## Cursor Cloud specific instructions

These notes apply to Cloud Agent VMs for this repository. They capture non-obvious environment behavior discovered while provisioning the toolchain; they do not change any normative content or validation policy.

- Toolchain parity with CI: the environment provides Python `3.13` (as bare `python`/`python3`), Node `22.23.1` (the nvm default, matching the pinned Mermaid renderer), npm, and `@mermaid-js/mermaid-cli@11.16.0` (`mmdc`). Refresh Python dependencies idempotently with `python -m pip install --requirement requirements-dev.txt`. Keep `PYTHONDONTWRITEBYTECODE=1` set during validation and confirm no `__pycache__` remains.
- Mermaid node resolution: the agent shell wrapper prepends an older `/exec-daemon/node` (v22.14.0) to `PATH`, which shadows the pinned Node in agent-run commands even though login shells and terminals resolve Node `22.23.1` correctly. `tools/mermaid_inventory.py` requires exactly `22.23.1`. When invoking it from an agent command, prefix `PATH=/usr/local/bin:$PATH` (or run it inside a login shell) so `node` and `mmdc` resolve to `22.23.1`, and set `ESAF_MERMAID_PUPPETEER_CONFIG=tools/mermaid-puppeteer-ci.json`.
- Fast fixture-heavy test runs: many tests (qualified-review evidence, crosswalk baselines, release gates, mapping bundles) create real Git commits. The Cloud VM's Git config enables SSH commit signing, so each fixture commit spawns `ssh-keygen -Y sign` and slows the suite substantially. For local test runs only, disable signing per-invocation with `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`; this injects config into the tests' Git subprocesses without altering the agent's real signing configuration used for your own commits.
- Known overlayfs-only test-order sensitivity: `tests/test_validate_qualified_review_evidence.py::CampaignValidationTests.test_attestation_source_sets_are_exactly_candidate_bound` reads an attestation via an unsorted `Path.glob("*.md")` whose readdir order differs on the Cloud VM's overlayfs rootfs from CI's ext4. It passes in GitHub CI and on ext4-ordered checkouts but can fail on overlayfs. The method is AST-frozen by the qualified-review equivalence proof (`RETAINED_AST_SHA256`), so do not edit it to work around the local ordering; treat this specific failure as an environment artifact, not a regression.
