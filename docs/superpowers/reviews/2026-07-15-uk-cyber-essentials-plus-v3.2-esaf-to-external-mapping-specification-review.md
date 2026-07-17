# Cyber Essentials Plus v3.2 ESAF-to-external mapping specification review

review_date: 2026-07-17
reviewer_id: codex-ce-plus-final-specification-reviewer
reviewer_role: independent final specification and task-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 0d141a6d5fff01cfb218ba8ac4f3cdc565739cf3
reviewed_base_sha: b4529c05c440db2f94ec12db4f21e3d0af57a5fb
reviewed_range: b4529c05c440db2f94ec12db4f21e3d0af57a5fb..0d141a6d5fff01cfb218ba8ac4f3cdc565739cf3
specification_verdict: approved
task_quality_verdict: approved
critical_or_important_findings_remain: false

## Independence and review boundary

This review is bound only to immutable content candidate
`0d141a6d5fff01cfb218ba8ac4f3cdc565739cf3`, compared with immutable baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. The reviewer used authorized
access to the pinned public NCSC v3.2 source boundary, locked oracle, the
candidate records, and the exact ESAF baseline requirements. The identity is
distinct from mapper `esaf-crosswalk-editorial-team`, mapping-rights reviewer
`esaf-publication-rights-reviewer`, and final overclaiming reviewer
`codex-ce-plus-final-overclaiming-reviewer`.

The candidate itself correctly has no final-review artifacts: those are
reviewer-owned post-candidate documentation. This report does not change the
candidate content, candidate index, candidate HEAD, or branch.

## Evidence and method

I read Task 13's brief and implementation report, the candidate traceability
record, and the supplied whole-range diff. I reviewed the complete range, not
only the Task 13 commits. I independently parsed every one of the 144 record
front matters, compared each ID, group, kind, actors, original-paraphrase
summary, and rendered locator with the locked oracle, checked every relationship
against the committed 91-control manifest and exact `## Requirement` text, and
inspected source, rights, lifecycle, catalog, navigation, backlog, schema,
validator, and test changes.

The following candidate-bound checks passed:

- `python -m unittest tests.test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping -v` — 35 tests passed.
- `python tools/validate_crosswalks.py --check --baseline-ref b4529c05c440db2f94ec12db4f21e3d0af57a5fb` — valid; 2 mapping sets, 260 provisions, 49 relationships, and 213 negative dispositions.
- `python tools/validate_crosswalks.py --check` — the same valid derived totals.
- `git diff --check b4529c05c440db2f94ec12db4f21e3d0af57a5fb..0d141a6d5fff01cfb218ba8ac4f3cdc565739cf3` — passed.

## Specification assessment

### Oracle, inventory, records, and taxonomy

All 144 oracle provisions bind exactly once, with no extra, omitted, duplicate,
or reverse record. The complete-publication inventory is in oracle order and
the group counts are M 24, T1 16, S 11, T2 9, T3 37, T4 9, T5 7, C 13, A 4,
and B 14. Kind counts are 43 procedure steps, 21 decision rules, 21
applicability records, 20 result rules, 19 prerequisites, 18 recommendations,
and 2 evidence-retention records.

There are seven mapped provisions, 137 `no_direct_mapping` dispositions, and
eight relationship legs referencing seven distinct controls. Each positive leg
is forward-only `esaf_to_external`, `partially_supports`, and unique on
external provision/control/direction. Each no-direct rationale identifies the
missing external outcome rather than using a generic absence claim. Each leg
has nonempty rationale, conditions, expected evidence, known gaps, and
prohibited inferences. Conditions narrow a requirement's contribution and do
not supply an absent external outcome.

The eight legs are limited to the exact normative support available from
AUD-130 (M-010), AUD-120 (M-011 and T3-014), CMP-110 (S-008), IAM-110
(T1-011), IAM-140 (T1-013), and IAM-120/IAM-130 (T5-006). The corresponding
requirements respectively mandate assessment-finding remediation and closure,
assessment evidence retention, governed-record retention, authentication of
non-public AI assets, credential rotation, authorization/least privilege, and
restriction with separate authentication of enumerated privileged access. The
records correctly retain narrow gaps for external procedure execution,
assessor/Certifying Body roles, observed results, device and population
coverage, and aggregate outcomes. No relationship is elevated from direct
normative support to equivalence, completion, or result assurance.

### Baseline, manifest, schema, lifecycle, and catalog

The oracle digest is `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
The manifest is deterministically derived from the stated immutable ESAF
baseline `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, release `0.4-alpha`,
and contains 91 controls. Every leg's version, path, record SHA-256, and
`controls/<path>#requirement` locator match that manifest.

The schema extension supplies structured external metadata, authorized mapper
access, relationship provenance, and prohibited-inference fields; the validator
fails closed for incomplete or mismatched manifest provenance. The snapshot and
lifecycle state remain `draft`, lifecycle `events` is `[]`, and the regenerated
snapshot digest is `284daa76427b88b11a8db0d317ba443061693b52efdb7999a3b928207c0a04b6`.
Both catalog formats derive the same two-set totals: 260 provisions, 49 legs,
and 213 negatives. The candidate neither treats complete-publication inventory
as approval nor supplies a lifecycle transition.

### Rights, navigation, history, and traceability

The candidate preserves the mapping-rights attestation, its feasibility-rights
ancestry `4207e1c1e8ff9f743274ebb4b626210cca053458`, the pinned public v3.2
oracle and canonical-PDF identity, OGL v3.0 attribution, copied-passage
prohibition, IASME-structure partition, and exclusion of marks, imagery, and
third-party material. Its narrative checks and mutation coverage guard against
copied source windows, T5-006 feasibility-text reuse, generic negatives,
conditions that manufacture an outcome, stale provenance, stale catalog data,
wrong taxonomy, and reverse legs.

The README, UK landing page, registry, catalogs, and traceability record agree
on draft status, 144/8/7/137 totals, source-version boundary, and the limits on
certification, compliance, equivalence, qualified review, current-scheme
completeness, full-population assurance, and continuous assurance. The landing
page's two "no mapping" statements are explicitly feasibility-time historical
statements, immediately separated from the current-draft description; they are
not current-state claims. The authorized forward-design backlog item is removed
while the distinct `external_to_esaf` design item remains.

The traceability record accurately identifies the content candidate, derived
digest, two complete gate passes, batch-review closure, and the pre-review
status. It does not claim qualified review or approval. The only Task 13 scope
exception is the necessary `tests/test_release_metadata.py` change, which
updates its former backlog assertion to the separately authorized completed
forward design state. The historical inventory contract and its digest-locked
feasibility evidence remain preserved rather than rewritten.

## Task-quality assessment

The implementation supplies a whole-snapshot reconciliation contract and a
meaningful mutation matrix for missing/extra records, metadata changes, stale
control digest and requirement locator, reverse direction, relationship
taxonomy, empty gaps, condition-created outcomes, generic negative rationale,
copied source window, T5-006 reuse, and stale catalog. It includes the focused
validator regression for manifest-provenance triplets. The implementation report
records the initial reconciliation RED/GREEN and the corrected candidate gate
evidence; the traceability record captures the two complete gate runs and
explicitly scopes the release-metadata exception. Navigation and backlog changes
are synchronized with that evidence.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

No Critical or Important finding remains.

## Verdicts

Specification verdict: **approved**. The exact candidate satisfies the
complete-publication draft contract with exact oracle fidelity, defensible
normative-only positive relationships, specific negative dispositions, manifest
provenance, draft governance, and generated catalog/lifecycle integrity.

Task-quality verdict: **approved**. The full-range implementation is
traceable, fail-closed where required, and supports the stated candidate-bound
publication state without overextending historical feasibility statements or
the sole authorized release-metadata test scope exception.
