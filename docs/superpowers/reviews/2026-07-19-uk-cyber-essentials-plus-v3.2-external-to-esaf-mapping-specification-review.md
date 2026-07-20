# Cyber Essentials Plus v3.2 external-to-ESAF mapping specification review

review_date: 2026-07-19
reviewer_id: codex-ce-plus-reverse-final-specification-reviewer
reviewer_role: independent final specification, inventory, and task-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: 969854ac58138bb58b8555687d30c64f12e78ed7
reviewed_base_sha: e4de0a5d3801431d96e49a746069834fa0b4d370
reviewed_range: e4de0a5d3801431d96e49a746069834fa0b4d370..969854ac58138bb58b8555687d30c64f12e78ed7
immutable_esaf_baseline_sha: 7461d7137e3faf36b2b73a15f71100fa4ce11159
specification_verdict: approved
task_quality_verdict: approved
critical_or_important_findings_remain: false

## Independence and review boundary

This review is bound only to immutable content candidate
`969854ac58138bb58b8555687d30c64f12e78ed7`, compared with merge-base
`e4de0a5d3801431d96e49a746069834fa0b4d370`, and to the candidate's immutable
ESAF control baseline `7461d7137e3faf36b2b73a15f71100fa4ce11159`.
The reviewer used authorized access to the pinned public NCSC v3.2 source
boundary, locked oracle, candidate records, and exact ESAF baseline
requirements.

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
rights reviewer `esaf-reverse-mapping-rights-reviewer`, and the separately
dispatched final security/overclaiming reviewer. This is an independent
technical-draft review. It is not qualified Cyber Essentials SME approval,
lifecycle approval, certification approval, a compliance determination, or an
authorization to promote any record or mapping-set status.

The report is reviewer-owned post-candidate documentation. It does not modify
the reviewed candidate SHA, its index, HEAD, mapping records, generated
artifacts, or lifecycle state.

## Evidence and method

I read the exact Task 6 brief, the complete supplied review package, both
reverse-mapping designs and implementation plans, the source-rights
attestation, the candidate-owned traceability record, the snapshot metadata,
the lifecycle record, generated catalogs, UK navigation, backlog change,
source-versioned observation registry, production validation changes, and the
focused regression suite. The supplied package contained the same 166 changed
paths as Git's complete merge-base range, with no missing or extra packaged
path.

I independently parsed all 144 provision records and compared each record's
identifier, group, kind, actors, approved paraphrase, and rendered locator with
the locked oracle. I compared all positive relationships with the committed
91-control manifest and exact baseline `## Requirement` text, reviewed all 32
registered observation profiles and all 112 negative rationales, and checked
publication, rights, lifecycle, catalog, navigation, backlog, and traceability
synchronization.

The following candidate-bound commands passed with
`PYTHONDONTWRITEBYTECODE=1` for Python commands:

- `python -m unittest tests.test_uk_cyber_essentials_plus_v32_external_to_esaf_mapping -v` - 63 tests passed in 62.148 seconds.
- `python tools/validate_crosswalks.py --check` - valid; 3 mapping sets, 404 provisions, 81 relationships, and 325 negative dispositions.
- `python tools/validate_crosswalks.py --check --baseline-ref e4de0a5d3801431d96e49a746069834fa0b4d370` - valid with the same derived totals.
- `git diff --check e4de0a5d3801431d96e49a746069834fa0b4d370..969854ac58138bb58b8555687d30c64f12e78ed7` - passed with no output.

A separate read-only audit reported 144 records, 32 mapped provisions, 112
no-direct-mapping dispositions, 32 legs, 10 distinct controls, zero oracle
fidelity errors, zero condition-order or evidence-reference errors, zero
registry omissions or orphans, 112 unique negative rationales, and zero
negative records with relationships. It reproduced snapshot digest
`460b14fafb2dd8b2ac041cba5a2ec5216cb6fec4fae14ec7b6e3ee89416c2599`.

The I-1 regression was also exercised with `TRACEABILITY` patched to a
nonexistent path. The targeted publication-metadata test ran once and failed
once at the required traceability assertion, with no error, proving that the
candidate no longer silently accepts missing candidate-owned traceability.

The public source pins reproduced without a local source download: the
424,226-byte canonical PDF hashes to
`2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`,
the 419,191-byte legacy official PDF hashes to
`d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694`,
and the locked oracle hashes to
`8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
Visual inspection of the source flow diagram confirmed that T1-009 is an
applied service result for a vulnerability scoring 7.0 or more, while the
adjacent T2-005 provision is only a generic qualifying criterion; their
different dispositions are therefore not contradictory.

## Specification assessment

### Oracle, inventory, taxonomy, and records

All 144 oracle provisions bind exactly once, with no omitted, added, duplicate,
or non-oracle record. The inventory preserves oracle order and group counts M
24, T1 16, S 11, T2 9, T3 37, T4 9, T5 7, C 13, A 4, and B 14. The kind counts
are 43 procedure steps, 21 decision rules, 21 applicability records, 20 result
rules, 19 prerequisites, 18 recommendations, and 2 evidence-retention records.
Every record remains `draft`, uses requirement granularity, and exactly matches
its oracle metadata, original paraphrase, and official locator.

The snapshot derives 32 mapped provisions and 112 `no_direct_mapping`
dispositions. The 112 negatives are unique, relationship-free, and each names
both the provision-bound external result and a specific missing ESAF outcome.
Administrative prerequisites, mere assessor or tool activity, recommendations,
aggregate rules, file supply, certification decisions, and adjacent procedures
remain negative unless the provision independently yields a defined result that
bears on an exact ESAF requirement.

### Positive registry, taxonomy, and exact support

The exact positive pair registry contains 32 unique provision/control pairs and
equals the authoritative Markdown leg set with no missing or orphan key:

- `CEPTS3.2-M-004/AUD-120`, `M-010/AUD-130`, `M-011/AUD-120`,
  `S-007/AUD-120`, and `S-008/CMP-110`;
- `T1-009/INF-120`, `T1-011/IAM-110`, `T1-012/IAM-110`,
  `T1-013/IAM-140`, `T1-014/APP-150`, `T1-015/APP-150`, and
  `T2-007/INF-120`;
- `T3-005/INF-110`, `T3-015/INF-110`, `T3-016/INF-110`,
  `T3-017/INF-110`, `T3-021/INF-110`, `T3-022/INF-110`,
  `T3-023/INF-110`, `T3-024/INF-110`, `T3-025/INF-110`,
  `T3-027/INF-110`, `T3-028/INF-110`, `T3-029/INF-110`,
  `T3-031/INF-110`, `T3-032/INF-130`, `T3-033/INF-110`,
  `T3-034/INF-110`, `T3-035/INF-110`, and `T3-036/INF-110`;
- `T4-008/IAM-110` and `T5-006/IAM-130`.

Every leg is unique, reverse-only `external_to_esaf`, and uses
`partially_supports`, narrow coverage, and high confidence. Each leg resolves
the exact control version, path, digest, and
`controls/<manifest-path>#requirement` locator. No condition or adjacent
capability creates a missing observation or ESAF outcome.

The structured observation language is closed, canonical, outcome-neutral,
pair-bound, and date-bound. Each positive has the exact ordered 11-condition
contract for actor, scope, population, sample, assessment date, evidence date,
tool, provenance, exception, Delivery Partner discretion, and point-in-time
status. Every condition has resolved, provision-specific evidence references;
expected evidence has one entry per condition; known gaps are nonempty; and all
nine prohibited-inference categories bind the exact observation and control.

The candidate keeps narrow boundaries for sample and population, assessment and
evidence dates, later state, unobserved safeguards, full requirement scope,
aggregate outcomes, and source-version limitations. T1-009 records a dated
severity measurement but not AI-specific prioritization or disposition.
T5-006 records restriction and separate authentication only for an in-scope
AI-changing privileged workflow; it does not establish time-bounding,
monitoring, review, other workflows, unsampled devices, or later state.

### Baseline, manifest, source, and rights

The manifest is deterministic for ESAF release `0.4-alpha` at immutable commit
`7461d7137e3faf36b2b73a15f71100fa4ce11159`, contains 91 controls, and has
catalog digest
`70bbd955a65969d2843b60220ad0aad2850f36ec6d189ecd32c40431b848b398`.
Every positive provenance triplet matches that manifest.

The snapshot preserves the NCSC/Crown attribution, Open Government Licence
v3.0 basis, feasibility-rights ancestry
`4207e1c1e8ff9f743274ebb4b626210cca053458`, copied-passage prohibition,
IASME-structure partition, marks and imagery exclusion, both official PDF byte
identities, and the public-v3.2/current-operational-scheme boundary. I found no
copied five-word source window or source-identity drift.

### Lifecycle, catalog, navigation, backlog, and traceability

The snapshot README, lifecycle registry, both generated catalogs, UK landing
page, backlog, and candidate traceability agree on 144 records, 32 mapped
provisions, 32 reverse legs, 10 distinct referenced controls, 112 negatives,
and repository totals of 3 mapping sets, 404 provisions, 81 relationships, and
325 negative dispositions. The snapshot and all records remain draft;
lifecycle `events` is `[]`; and the lifecycle digest equals the regenerated
snapshot digest.

The landing page separates feasibility-time historical statements from the two
subsequently implemented draft directions. Only the completed
external-to-ESAF design backlog item is removed. The traceability record binds
the exact oracle, source pins, immutable ESAF baseline, snapshot digest, derived
counts, draft boundary, pre-review content commit, merge-base, prior I-1, and
recorded pre-review gates. It does not claim qualified review or promote the
lifecycle.

## Task-quality assessment

The implementation has meaningful whole-snapshot and mutation coverage for
identity, oracle fidelity, counts, kind taxonomy, exact targets, direction,
relationship taxonomy, manifest provenance, condition order and resolution,
population/sample boundaries, tool-only observations, condition-created
support, supported-outcome drift, structured-observation grammar, registry
duplicates/missing/orphans, generic negative language, copied-source windows,
assurance smuggling, catalog synchronization, navigation, backlog scope, and
reviewer independence.

Important I-1 from the first exact-SHA review is resolved. The test now requires
candidate-owned traceability unconditionally while continuing to permit the two
reviewer-owned final reports to be absent from the content candidate. The
traceability file exists at the required path and contains the exact baseline,
snapshot digest, derived totals, lifecycle boundary, command family, and
technical-review limitations. The patched-path exercise proves that removing
it fails the focused contract.

The complete review package matches the Git range, generated artifacts reproduce
from authoritative content, and the required focused, ordinary crosswalk,
baseline crosswalk, and exact-range whitespace gates pass on the new immutable
candidate. No lower-severity issue is accepted or deferred.

## Findings by severity

- Critical: none.
- Important: none. Prior Important I-1 is resolved in candidate
  `969854ac58138bb58b8555687d30c64f12e78ed7` by an enforcing regression and
  candidate-owned traceability.
- Minor: none.

No Critical, Important, or Minor finding remains.

## Verdicts

Specification verdict: **approved**. The exact candidate satisfies the
complete-publication external-to-ESAF technical-draft contract with exact
oracle fidelity, defensible provision-first relationships, specific negative
dispositions, deterministic manifest provenance, synchronized draft
publication metadata, and no condition-created support or unsupported
adjacency.

Task-quality verdict: **approved**. The complete range is traceable, the I-1
regression fails on the original omission, the candidate-owned traceability is
reviewable, and the focused and repository-aware gates provide proportionate
fail-closed coverage. This approval is technical only and does not replace
qualified SME review, lifecycle governance, certification, or compliance
determination.
