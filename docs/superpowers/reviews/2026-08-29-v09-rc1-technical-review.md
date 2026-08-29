# v0.9-rc1 Independent Technical Review

## Review identity and scope

- Reviewer: `Codex ESAF Technical Publication Reviewer`
- Review date: 2026-08-29
- Exact candidate SHA: `3af9a6a7ada9a809dbe9422e83109bc7c566cb95`
- Scope: the Issue #95 `evidence_candidate` package and its prerequisites at
  the exact candidate SHA.
- Independence: the reviewer did not implement the reviewed validator or
  readiness record and made no tracked changes to the candidate.

The review covered the `tools/v09_rc1_release_gates.py` validator contract,
the recorded prerequisite dispositions (Phase 2 hosted-timing `DEFER`,
ESAF-1300/1400/1700 Working Drafts, and the NIST AI RMF crosswalk `HOLD`), the
derived-scope computation in `derive_scope`, and the `.github/workflows/catalog-validation.yml`
wiring that runs the validator on pull requests and pushes to `main`.

## Findings

The validator's front-matter contract, gate-state machine, and prerequisite
evidence-marker checks correctly bind the `evidence_candidate` phase to `open`
gates, null tag/date/evidence publication fields, and existing prerequisite
evidence files. `derive_scope` reads exclusively from live, Git-tracked
catalogs (`controls/catalog.json`, `crosswalks/catalog.json`, architecture
pattern files, the assessment foundation, the draft profile, and the PCI
DSS/NIST AI RMF readiness matrices), so the recorded `scope` block cannot
silently drift from the repository. CI wiring runs
`python tools/v09_rc1_release_gates.py --check` on the paths that can affect
the record or the validator, and `pytest`/`unittest` coverage of
`tools/v09_rc1_release_gates.py` exercises the happy path, phase-string
rejection, gate-state rejection, prerequisite-marker rejection, and scope-drift
rejection.

No unresolved Critical or Important finding was identified in the validator
contract, the prerequisite evidence, the scope derivation, or the CI wiring at
the exact candidate SHA.

- Open Critical: 0
- Open Important: 0
- Verdict: Approve for advancing to `closure_candidate`

## Nonclaims

This is a Working Draft release-candidate technical review only. It does not
close Issue [#55](https://github.com/tdistress/ESAF/issues/55) or Issue
[#60](https://github.com/tdistress/ESAF/issues/60). It establishes no
certification, compliance, equivalence, endorsement, assurance, or production
readiness, and it does not itself advance the readiness record's `phase` or
approve publication.

## Limitations

This review is not editorial, governance, or publication approval. Final
readiness still requires exact-head review of every required gate, external
approvals, merge validation, and the verified annotated-tag condition before
any `published` phase transition.
