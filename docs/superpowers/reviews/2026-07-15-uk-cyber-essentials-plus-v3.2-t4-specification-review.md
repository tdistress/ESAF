# Cyber Essentials Plus v3.2 `T4` specification review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t4-specification-reviewer
reviewer_role: independent specification and task-quality reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: ce5a88e94a6a505a2f27c25a4967e57db4860cf2
reviewed_base_sha: 6458359e7b9fdc10bd57b695c220a1d24d816cf2
reviewed_range: 6458359e7b9fdc10bd57b695c220a1d24d816cf2..ce5a88e94a6a505a2f27c25a4967e57db4860cf2
specification_verdict: approved
task_quality_verdict: approved
all_negative_determination: correct
critical_or_important_findings_remain: false

## Independence and authority

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
rights reviewer `esaf-publication-rights-reviewer`, and the independently
assigned T4 security and overclaiming reviewer. This review used authorized
access to the pinned public NCSC Cyber Essentials Plus Test Specification
v3.2, the locked 144-row provision oracle, and exact normative ESAF
`## Requirement` text at immutable baseline
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`. Implementation guidance,
assessment procedures, evidence examples, metrics, topic similarity, and
adjacent capabilities were not accepted as positive mapping bases.

## Scope, method, and evidence

The review covered `.superpowers/sdd/task-9-brief.md`,
`.superpowers/sdd/task-9-report.md`, the supplied exact package
`.superpowers/sdd/review-6458359..ce5a88e.diff`, the exact Git range bound
above, all nine T4 records, the focused Plus mapping test, lifecycle registry,
both generated catalogs, locked oracle, and committed ESAF control manifest.
HEAD was verified as exact candidate
`ce5a88e94a6a505a2f27c25a4967e57db4860cf2`, whose sole parent is the
required base and whose commit subject is `Map Cyber Essentials Plus
user-access tests`. After line-ending normalization, the package's embedded
ten-context-line diff matches the exact Git range.

The candidate contains exactly 13 authorized paths: nine new records
`cepts32-t4-001.md` through `cepts32-t4-009.md`, the focused mapping test, the
Plus lifecycle registry, and generated `crosswalks/catalog.json` and
`crosswalks/CATALOG.md`. It does not modify prior records, the locked oracle,
committed ESAF manifest, inventory, schemas, validators, rights artifacts, or
other publication content, and it does not create either Task 9 review
report.

The oracle SHA-256 was independently verified as
`8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
The committed manifest remains ESAF release `0.4-alpha`, source commit
`b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, with exactly 91 controls. All
nine records were compared in oracle order for record and external IDs,
group, kind, actors, original-paraphrase summary, official URL, and rendered
dual-coordinate locator; no mismatch was found. The implementer supplied
per-provision RED/GREEN evidence, a passing 23-test focused suite, a fresh
passing 318-test full suite with 3 expected skips, ordinary and pinned-baseline
crosswalk validation, link validation, and exact-range diff checks. No broad
suite was rerun for this task-scoped review. Read-only focused checks confirmed
the candidate identity and scope, oracle checksum, manifest binding, catalog
totals, exact package equality, clean range diff, and snapshot digest.

## Specification assessment

The candidate implements exactly `CEPTS3.2-T4-001` through
`CEPTS3.2-T4-009` and adds `T4` to `COMPLETED_GROUPS`. The shared completed-
batch fidelity assertion consequently requires the complete nine-row T4
oracle group, while the focused batch test fixes the result at zero mapped
records, zero relationship legs, and nine `no_direct_mapping` records.

Every record uses schema version `1.0.0`, requirement granularity, `draft`
status, the required mapping-set ID, paraphrase mode, approved mapper identity
and date, exact oracle-derived metadata and locator, and an empty relationship
array. Every negative rationale begins `Missing outcome:` and identifies the
specific absent assessment population, sampled-user sign-in exercise,
normal-user and administrator coverage rule, shared-authentication repetition
boundary, observation method, fallback method, authentication-service
repetition procedure, observed MFA result rule, or aggregate verdict. No
condition or adjacent control capability is used to create a missing external
outcome.

The records preserve the Assessor actor boundary. They do not infer tool or
procedure execution, assessor-account or test-account use, authentication
attempts, privilege checks, observations, cloud or sampled-device population
coverage, MFA form, or pass/fail rules from implemented access controls. They
also do not imply an executed procedure, observed result, certification,
compliance, equivalence, endorsement, current-scheme completeness,
full-population assurance, or continuous assurance.

## All-negative determination

The all-negative result is correct. Exact pinned `IAM-110` requires the
organization to authenticate identities before access to non-public AI assets
using mechanisms proportionate to risk. Exact pinned `IAM-120` requires
purpose-, role-, attribute-, context-, and least-privilege-based authorization
for AI assets and actions. Exact pinned `IAM-130` requires restriction and
separate authentication of privileged access capable of changing enumerated
AI assets. These requirements do not assign the external Assessor, select the
T4 cloud-service or role population, require sampled users to attempt access,
prescribe the observation environment, group or repeat tests by authentication
service, or create a Cyber Essentials Plus result.

`T4-008` does not receive a positive relationship merely because MFA is
topically adjacent. The word `multifactor` appears only in IAM-110
implementation guidance, not its normative requirement. IAM-110's requirement
does not prescribe an MFA form, a first prompt before cloud access, both
ordinary-user and administrator coverage, observation of that prompt, or an
Assessor pass/fail verdict. IAM-130's normative phrase `separately
authenticate` applies only to privileged access capable of changing specified
AI assets and likewise does not prescribe the observed MFA form or external
verdict. A condition could narrow a real authentication duty but could not
supply those missing population, observation, form, and result outcomes.

Exact pinned `ARC-140` requires documented and validated responsibility
boundaries among capability parties and cloud services; it does not establish
the T4 cloud population or repetition boundary. Exact pinned `AUD-100`
requires a risk-based AI assessment program, and `AUD-120` requires sufficient
evidence for AI assessment procedures and determinations; neither requires
this external procedure to be executed nor its observations or verdicts to
exist. No other concretely plausible pinned normative requirement supplies
the exact T4 actor, object, procedure, population, observation, MFA-form, or
result outcomes.

## Lifecycle, catalog, provenance, and tests

The lifecycle remains `draft`, its `events` array remains empty, and snapshot
digest `6bf590bf6c82f883b9b12276eb60b46f2dce79506befc6e60363868819bb80ff`
was independently recomputed from the 106-record snapshot. The generated
catalogs consistently derive repository totals of 2 mapping sets, 222
provisions, 47 directional relationships, and 176 negative dispositions. T4
contributes exactly nine records, zero relationship legs, zero distinct
referenced ESAF controls, and nine negative dispositions.

The focused tests enforce completed-group path equality, oracle identities and
metadata, original-paraphrase source-copy protection, manifest provenance,
draft status, exact T4 disposition and relationship counts, lifecycle digest,
catalog totals, and paired closure reports with authorized and pairwise-
distinct mapper, rights, specification, and overclaiming reviewer identities.
The test changes are focused and proportionate to the batch contract.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

No Critical or Important finding remains unresolved.

## Verdicts

Specification verdict: **approved**. Exact candidate
`ce5a88e94a6a505a2f27c25a4967e57db4860cf2` satisfies the binding Task 9
contract: exact nine-row oracle fidelity, complete T4 group enforcement,
normative-only mapping analysis, nine provision-specific negative
dispositions, no relationship legs, original paraphrases, correct provenance,
draft lifecycle with empty events, and deterministic catalog derivation.

Task-quality verdict: **approved**. The implementation is tightly scoped,
test-first, complete, and supported by credible candidate-bound validation
evidence. The all-negative determination is independently confirmed, including
the absence of exact normative support for T4-008's observed MFA-form result.
