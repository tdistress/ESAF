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

## Required validation habits

- Run focused tests for the artifact being changed.
- Run the full test suite with `python -m unittest discover -s tests -v`.
- Run `python tools/validate_controls.py --check` when controls or their references may be affected.
- Run `python tools/validate_architectures.py` when architecture content or links may be affected.
- Run ordinary working-tree checks such as `git diff --check` during development, then run `git diff --check <merge-base>..HEAD` for final whole-branch review; ensure generated caches or build outputs are not committed.
- Render every Mermaid diagram, not merely count fenced blocks. A syntactically valid Markdown file can still contain a Mermaid parse failure.
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
- The owner has authorized safe and relevant use of subagents.
- Do not extend this authorization to other repositories, accounts, publishing destinations, permissions, credentials, or materially broader project scope.
- When the owner asks to pause, leave the repository in a clean, recoverable state and stop new milestone work.

## Durable implementation lessons

- Content-level regression tests are valuable but do not replace renderer validation.
- Local browser sessions may not be authenticated for private GitHub repositories even when `gh` is authenticated; distinguish GitHub visual verification from local renderer verification accurately.
- PowerShell command substitution can collapse multiline PR descriptions. Use a literal here-string or a purpose-built GitHub tool when updating multiline bodies.
- `gh pr merge --delete-branch` can merge successfully and then fail during local branch deletion when another worktree owns the base branch. Verify PR state before retrying, then clean branches and worktrees separately.
- Set `PYTHONDONTWRITEBYTECODE=1` during Python validation and verify that no `__pycache__` directories remain before declaring the checkout clean.
- On Windows, deeply nested project-local worktrees can make tracked files unreadable to Python or PowerShell even when Git reports a clean checkout. Use a short drive alias, run tests and tools through it, and verify the longest tracked paths before diagnosing missing repository content.
