# Validation workflow security hardening design

**Date:** 2026-08-09
**Status:** Approved design
**Parent design:** `docs/superpowers/specs/2026-08-08-validation-time-budgeted-workflow-design.md`
**Baseline candidate:** `4193c4ab09abc4939198630925a8227a9a24fe34`

## Purpose

Harden the time-budgeted validation workflow after final review found that candidate-controlled routing data, optional-tier filtering, and renderer cleanup could weaken or misstate publication validation. The repair shall preserve short-session feedback for ordinary changes while making publication plans complete, executable, and unambiguous.

## Scope

This design changes the planner trust boundary and Mermaid timeout cleanup. It does not change required GitHub checks, the test population, the pinned Node or Mermaid versions, the tracked Puppeteer configuration, or the meaning of a release gate.

## Planner policy

The planner shall define its executable command catalog, route rules, ordered publication command identifiers, and proof-bearing command identifiers in reviewed Python code. It shall not load executable commands or routing policy from a candidate-controlled JSON file.

The static policy shall contain immutable records for commands and routes. A command shall contain a stable identifier, a fixed argv template, a tier, and a duration range. A route shall contain reviewed path selectors, command identifiers, a cross-cutting flag, and a reason. The implementation shall reject an invalid in-memory policy before planning.

The repository shall remove `tools/validation-plans.json`. Workflow path filters, documentation, and tests shall no longer reference it.

## Candidate binding and escalation

The planner shall resolve a base and candidate commit, require the candidate to equal checked-out `HEAD`, and require the base to be an ancestor of the candidate. It shall reject tracked changes for every plan.

The planner shall select its natural route before processing `--tier`. If the natural route is publication, `--tier quick` and `--tier standard` shall fail. `--tier publication` shall return the complete ordered publication catalog. An ordinary quick or standard route may still be filtered to a requested tier.

Unknown, deleted, renamed, workflow, validation-tool, policy-source, generated-review-evidence, and release-metadata paths shall select publication. The publication command sequence shall be a separately declared invariant, not an outcome derived from path rules.

When a selected plan contains a proof-bearing command, the planner shall require `git status --porcelain=v1 --untracked-files=all` to be empty. Ordinary quick and standard plans may allow unrelated untracked files. Documentation shall describe this distinction plainly.

## Executable output

Every emitted command shall have fixed argv defined by the reviewed policy. The branch whitespace command shall compare the resolved base and candidate. Link validation shall include `--check`. The exact qualified-review verifier shall include `--check --candidate-sha <candidate>`. Commands that require human evidence, stateful inputs, or an output path shall not be generic planner commands.

Text output shall JSON-quote changed paths, reasons, duration labels, identifiers, and each argv token. This prevents terminal-control or prompt-spoofing output from Git-derived names. JSON remains the machine-readable interface.

## Mermaid timeout cleanup

Each Mermaid block render shall run through a bounded helper. On timeout, Windows shall terminate only the timed-out renderer tree with `taskkill /PID <pid> /T /F`; POSIX shall create and terminate a dedicated process group. The helper shall use a short bounded drain after termination.

If tree termination or cleanup cannot complete, the renderer shall return a stable, block-specific validation error. It shall not claim that partial-output deletion or descendant termination succeeded when that work was best effort. It shall not change the pinned renderer versions, launch arguments, or Puppeteer configuration.

## Verification

Tests shall cover:

- the exact static command catalog and publication sequence;
- candidate binding, base ancestry, tracked and proof-bearing full cleanliness;
- non-bypassable publication filtering;
- known ordinary routes and every publication escalation family;
- executable argv and safe text encoding of hostile path strings;
- bounded Mermaid timeout cleanup on Windows and POSIX abstractions, including termination, drain, output-removal, and cleanup failures;
- preserved CI matrix, `fail-fast: false`, aggregate job, and trigger coverage.

Final validation shall run focused suites, the full test suite from a clean detached worktree, the private pinned Mermaid record gate, whole-branch whitespace checks, final independent specification and security reviews, and the normal pull-request checks.

## Non-goals

- Trusting a candidate-executed local planner as a complete defense against a malicious candidate that also edits the planner.
- Adding GPU flags, retry loops, or alternative renderer versions.
- Making generated review evidence optional for publication.
- Replacing required CI with the local planner.
