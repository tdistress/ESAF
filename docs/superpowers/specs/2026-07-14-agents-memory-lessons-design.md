# ESAF AGENTS.md Durable-Lessons Update Design

## Purpose

Update `AGENTS.md` with durable working conventions learned while producing and publishing the UK Cyber Essentials v3.3 crosswalk. The update must help future framework-mapping work without turning project memory into a session log or a Cyber Essentials-specific procedure.

## Scope

The change will strengthen repository-wide validation guidance and add a focused crosswalk-development section. It will not restate the full crosswalk methodology, duplicate the style guide, or preserve task-specific commit identifiers, counts, branch names, or reviewer names.

## Repository-wide additions

- Require branch-wide whitespace validation with `git diff --check <merge-base>..HEAD`; working-tree-only and latest-commit checks are insufficient final gates.
- On Windows, use a short drive alias for deeply nested worktrees when paths approach platform limits. Run tests and tools through that alias and verify long tracked files are readable before diagnosing repository corruption.
- Keep review and traceability evidence synchronized with the exact candidate SHA and actual gate results.
- Keep task reports internally coherent; replace superseded totals or conclusions instead of leaving contradictory earlier statements followed by corrections.

## Crosswalk-development additions

- Pin authoritative sources by official URL, version, publication date, and checksum. Lock provision identifiers, summaries, and locators in a machine-readable oracle when feasible.
- Default to `no_direct_mapping` when ESAF does not expressly provide the external outcome. Mapping conditions may narrow or qualify an existing relationship but must not supply the missing outcome.
- Distinguish `prerequisite` from `partially_supports` using exact normative control text, not implementation guidance or adjacent capabilities.
- Treat whitespace-only record edits as snapshot changes when registries or catalogs depend on content digests; regenerate and validate derived artifacts.
- Derive published statistics from records and manifests. Keep pinned control population, relationship-leg count, distinct referenced-control count, and negative-disposition count separate.
- Keep adjacent assurance schemes independently sourced and mapped. Do not infer one scheme from another, such as Cyber Essentials Plus from the core requirements.
- Require two exact-SHA final reviews for substantial crosswalks: specification/inventory completeness and security/overclaiming semantics. Redispatch both after any candidate change.

## Existing guidance retained

The current rules for evidence-based mappings, exact reviewed SHA tracking, independent review, full-suite validation, generated-cache cleanup, merge-state checks, and autonomous repository authorization remain applicable and will not be duplicated unnecessarily.

## Validation

The implementation will be checked by:

1. Reviewing the complete `AGENTS.md` diff for duplication, contradictions, project-specific leakage, and ambiguous normative wording.
2. Scanning the changed files for placeholders and trailing whitespace.
3. Running `git diff --check <merge-base>..HEAD`.
4. Running the repository test suite through a short Windows drive alias to avoid deep-path false failures.

