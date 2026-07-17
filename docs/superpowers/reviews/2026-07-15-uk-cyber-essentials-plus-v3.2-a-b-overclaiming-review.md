# Cyber Essentials Plus v3.2 A-B Security and Overclaiming Review

review_date: 2026-07-17
reviewer_id: codex-ce-plus-ab-overclaiming-reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: e88e7756d78fa6bc7c94bb7ba8aa6be96e976ca6
reviewed_base_sha: d98581d2a9f8b411f3ad698838f237a082fe20f0
reviewed_range: d98581d2a9f8b411f3ad698838f237a082fe20f0..e88e7756d78fa6bc7c94bb7ba8aa6be96e976ca6
review_disposition: approved
critical_or_important_findings_remain: false

## Scope and independence

This independent read-only security and overclaiming review covers the exact
Task 12 candidate range above: `CEPTS3.2-A-001` through `CEPTS3.2-A-004`,
`CEPTS3.2-B-001` through `CEPTS3.2-B-014`, the focused test changes,
lifecycle digest, and generated catalogs.

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
rights reviewer `esaf-publication-rights-reviewer`, and specification reviewer
`codex-ce-plus-ab-specification-reviewer`. This review used authorized source
access and did not modify the candidate, index, or HEAD. The only file created
is this designated immutable report.

## Method and evidence

- Verified HEAD as exact candidate
  `e88e7756d78fa6bc7c94bb7ba8aa6be96e976ca6` over exact base
  `d98581d2a9f8b411f3ad698838f237a082fe20f0`. Reviewed the binding brief,
  implementation report, and complete supplied exact-range package
  `.superpowers/sdd/review-d98581d..e88e775.diff` before inspecting the
  candidate files directly.
- Independently verified the locked 144-provision oracle SHA-256 as
  `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
  Retrieved the pinned public NCSC Cyber Essentials Plus Test Specification
  v3.2 and verified its canonical SHA-256 as
  `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`
  before inspecting PDF pages 21 through 23.
- Compared all 18 A/B records in oracle order for identity, group, actor,
  kind, approved original-paraphrase summary, locator, disposition, and
  specifically stated missing outcome. No candidate positive leg was assumed
  correct or required merely because adjacent subject matter exists.
- Compared plausible controls against exact normative `## Requirement` text
  from the pinned 91-control ESAF `0.4-alpha` baseline
  `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, especially `APP-140`,
  `INF-120`, `AUD-100`, `AUD-120`, `DAT-120`, `INF-110`, and `ARC-140`.
  Implementation guidance, evidence examples, generic capability adjacency,
  and assessment mechanics were not accepted as mapping bases.
- Audited the public-source, copied-source, IASME, actor, authorization,
  execution, observation, population, result, certification, and assurance
  boundaries. Conditions were treated only as narrowing devices and were not
  allowed to create an absent tool, actor, target population, test-material,
  procedure, observed result, or scheme verdict.
- Fresh read-only verification on the exact candidate passed the full focused
  32-test mapping module, including the frozen normalized five-word
  copied-source guard, A/B boundary assertions, exact oracle/manifest
  fidelity, and final counts. Pinned-baseline crosswalk validation passed at
  260 provisions, 49 relationships, and 213 negative dispositions. Exact-range
  `git diff --check` passed and the worktree was clean before report creation.

## Appendix A determination

All four A dispositions are correctly `no_direct_mapping` with no relationship
legs.

- `A-001` authorizes the scanner class for this external assessment. Neither
  `APP-140` nor `INF-120` requires Delivery Partner authorization of an
  Assessor's scanner, and authorization does not establish scanner execution,
  output, or an observed result.
- `A-002` defines every-associated-address coverage. `INF-120` requires
  risk-based vulnerability identification and treatment for AI infrastructure
  and dependencies, but it does not require this external scan, Assessor
  execution, every Applicant-associated IP address, or any resulting
  observation. A condition could not manufacture those missing outcomes.
- `A-003` defines a Delivery Partner-scoped limited-port alternative.
  Vulnerability-management and secure-testing duties do not supply that
  permission, port population, ownership boundary, or external procedure.
- `A-004` recommends that the Delivery Partner provide the Assessor a TCP/UDP
  port inventory. ESAF inventory, evidence, and assessment duties do not assign
  that scheme-specific inventory to the Delivery Partner or require its supply
  to an Assessor. A setup input is not scanner execution, scanner output, or
  implementation evidence.

The four records therefore preserve tool authorization versus execution and
result, address coverage, port coverage, and port-inventory ownership without
turning any of them into proof of an ESAF safeguard.

## Appendix B determination

All fourteen B dispositions are correctly `no_direct_mapping` with no
relationship legs.

- `B-001` requires complete assessment-file supply, while `B-007` requires an
  advance representative set. `B-010` through `B-012` define mandatory
  container, executable, and routinely received file-type categories for the
  full set. `AUD-100` and `AUD-120` do not assign this file-set ownership,
  composition, or delivery to the external actors. Test inputs are not
  evidence that a safeguard was implemented or tested.
- `B-002` and `B-003` assign Applicant-specific subset definition and hosting
  to the Certification Body. `B-008` and `B-009` address encouragement and
  tailoring for the Applicant's applications and platforms. ESAF assessment
  scope, sampling, evidence, data representativeness, and responsibility
  controls do not prescribe this external subset, hosting arrangement,
  actor assignment, or file-selection method. Conditions cannot supply those
  missing particulars.
- `B-004` is a prospective correct-file confirmation. It establishes neither
  file delivery nor test execution, observation, or implementation evidence.
- `B-005` and `B-006` state expected anti-malware and executable-file
  reactions. ESAF has no exact normative endpoint anti-malware, user-access
  blocking, warning, or execution-choice requirement, and an expected external
  reaction is not an observed reaction or result.
- `B-013` concerns conspicuous executable-test-artifact behavior, and `B-014`
  concerns selection of generally detectable inert malware samples.
  `APP-140` secure-development and testing practices do not require these
  external Delivery Partner artifact-design or sample-selection outcomes.

The records preserve complete-file supply, representative-set coverage,
subset definition, hosting, Applicant-specific tailoring, expected reactions,
container and file-type applicability, and test-artifact design and selection
without converting any of those assessment mechanics into normative ESAF
implementation evidence.

## Source protection and assurance boundaries

The candidate stays within the pinned public NCSC v3.2 publication and locked
oracle. It uses authorized structural metadata, approved original paraphrases,
derivative missing-outcome analysis, and official links. It reproduces no
prohibited requirement or passage text, imports no IASME-derived structure,
and does not infer requirements from a current operational scheme or adjacent
assurance source.

The exact candidate completes the snapshot at 144 records with group counts
`24/16/11/9/37/9/7/13/4/14` for `M/T1/S/T2/T3/T4/T5/C/A/B`.
The A/B batch contains 18 negative dispositions, zero mapped dispositions,
zero relationship legs, and zero referenced ESAF controls. Snapshot and
records remain draft, lifecycle events remain empty, and direction remains
exclusively `esaf_to_external`.

No A/B record or candidate-generated artifact claims or implies procedure
execution, an observed result, address, port, file, device, sample, or
population coverage, pass/fail, certification, compliance, equivalence,
endorsement, current-scheme completeness, full-population assurance, or
continuous assurance.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

## Disposition

Approved. Exact candidate
`e88e7756d78fa6bc7c94bb7ba8aa6be96e976ca6` is approved for Task 12 A/B
technical closure from the security and overclaiming perspective. No Critical,
Important, or Minor findings remain unresolved. This approval does not promote
the draft snapshot or establish procedure execution, observed results,
population coverage, pass/fail, certification, compliance, equivalence,
endorsement, current-scheme completeness, full-population assurance, or
continuous assurance.
