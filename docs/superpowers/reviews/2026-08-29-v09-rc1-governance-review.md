# v0.9-rc1 Independent Governance Review

## Review identity and scope

- Reviewer: `Codex ESAF Governance Publication Reviewer`
- Review date: 2026-08-29
- Exact candidate SHA: `3af9a6a7ada9a809dbe9422e83109bc7c566cb95`
- Scope: the Issue #95 `evidence_candidate` package and its prerequisites at
  the exact candidate SHA.
- Independence: the reviewer did not implement the reviewed validator or
  readiness record and made no tracked changes to the candidate.

The review covered the `evidence_candidate` -> `closure_candidate` ->
`published` phase machine in `tools/v09_rc1_release_gates.py`
(`PHASE_GATE_STATES`, `PREVIOUS_PHASE`), the `CLOSURE_ALLOWLIST` discipline
that will bound closure- and published-phase diffs against the recorded
baseline, alignment with the `project/RELEASE_PLAN.md` milestone exit
criteria for prior releases, and the tag-after-post-merge rule that keeps
`publication.tag_object`/`tagged_commit` null until after the exact validated
commit is merged and tagged.

## Findings

The phase machine requires every gate `open` at `evidence_candidate`, every
gate but `post_merge` `ready` at `closure_candidate`, and every gate `closed`
only at `published`, matching the milestone exit-criteria pattern used for
`0.4-alpha` and `0.5-beta` in `project/RELEASE_PLAN.md`. `CLOSURE_ALLOWLIST`
restricts closure- and published-phase changes to `VERSION.md`, `README.md`,
`ROADMAP.md`, `CHANGELOG.md`, `project/RELEASE_PLAN.md`, and the readiness
record itself, which is consistent with the repository's established
publication-surface discipline. `_validate_publication` keeps
`tag_object`, `tagged_commit`, and `issue_evidence_url` null through both
candidate phases and requires 40-character SHAs only once `phase` is
`published`, preserving the rule that the annotated tag is created only after
merge to `main` on the exact validated commit. The readiness record at the
exact candidate SHA still records `phase: evidence_candidate`, so this
governance review authorizes no phase advance by itself.

No unresolved Critical or Important finding was identified in the phase
machine, the allowlist discipline, the milestone exit-criteria alignment, or
the tag-after-post-merge rule at the exact candidate SHA.

- Open Critical: 0
- Open Important: 0
- Verdict: Approve for advancing to `closure_candidate`

## Nonclaims

This is a Working Draft release-candidate governance review only. It does not
close Issue [#55](https://github.com/tdistress/ESAF/issues/55) or Issue
[#60](https://github.com/tdistress/ESAF/issues/60). It establishes no
certification, compliance, equivalence, endorsement, assurance, or production
readiness. It does not itself advance the readiness record's `phase`, bump
`VERSION.md`, or approve publication.

## Limitations

This review is not technical, editorial, or publication approval. Final
readiness still requires exact-head review of every required gate, external
approvals, merge validation, and the verified annotated-tag condition before
any `published` phase transition.
