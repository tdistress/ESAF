# Cyber Essentials Plus v3.2 T3-020-037 Security and Overclaiming Review

review_date: 2026-07-16
reviewer_id: codex-ce-plus-t3-020-037-overclaiming-reviewer
reviewer_authorized_source_access: true
reviewed_candidate_sha: fa3c8c8bef60b0f779849797f348701e900a22fd
reviewed_base_sha: e35ae8f49172139890aea83224a5cec1f16a0616
reviewed_range: e35ae8f49172139890aea83224a5cec1f16a0616..fa3c8c8bef60b0f779849797f348701e900a22fd
review_disposition: approved
critical_or_important_findings_remain: false

## Scope and independence

This independent read-only security and overclaiming review covers the sealed
Task 8 candidate range above: the eighteen new records `CEPTS3.2-T3-020`
through `CEPTS3.2-T3-037`, the focused test changes, lifecycle digest, and
generated catalogs. It also covers the required cross-cutting consistency
review of the complete 37-record T3 group, with direct inspection of unchanged
`T3-001` through `T3-019` where needed for population, procedure, result,
recommendation, and sole-positive comparisons.

The reviewer identity is distinct from mapper `esaf-crosswalk-editorial-team`,
rights reviewer `esaf-publication-rights-reviewer`, and the independently
assigned T3-020-037 specification-reviewer role. This review used authorized
source access and did not mutate the candidate, index, or HEAD. The only file
created is this designated immutable report.

## Method and evidence

- Verified HEAD as exact candidate
  `fa3c8c8bef60b0f779849797f348701e900a22fd` and reviewed the exact supplied
  diff package `.superpowers/sdd/review-e35ae8f..fa3c8c8.diff` together with
  `.superpowers/sdd/task-8-brief.md` and `.superpowers/sdd/task-8-report.md`.
- Used the locked 144-provision oracle at
  `docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json`.
  Its independently checked SHA-256 is
  `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`.
  The source boundary is the pinned public NCSC Cyber Essentials Plus Test
  Specification v3.2, canonical SHA-256
  `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`.
- Compared all 18 new records in oracle order for identity, actor, kind,
  original-paraphrase summary, locator, disposition, and specifically named
  missing outcome. Reviewed all 37 T3 records together for cross-half
  contradictions and templated rationales that could conceal a different
  external outcome.
- Compared the most plausible adjacent controls against exact normative
  `## Requirement` text from the pinned 91-control ESAF `0.4-alpha` baseline
  `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, including `INF-110`,
  `INF-120`, `INF-140`, `APP-140`, `MON-100`, `AUD-100`, and `AUD-120`.
  Implementation guidance, assessment procedures, evidence examples, and
  subject similarity were not accepted as mapping bases.
- Audited source/version, actor/procedure/result, population, aggregation,
  certification, and assurance boundaries. Conditions were evaluated only as
  narrowing devices and were not permitted to create absent external actor,
  procedure, observation, coverage, or verdict outcomes.
- Examined copied-source protection across the completed group, including the
  corrected T3-030 wording. A fresh read-only run of the single completed-batch
  oracle/manifest fidelity test passed on the exact candidate; that assertion
  applies the frozen normalized five-word source-window guard to every record
  narrative. No broad suite was rerun. The implementer evidence records 21
  focused tests passing, the full 316-test suite passing with 3 skipped,
  ordinary and pinned-baseline crosswalk validation passing at `213/47/167`,
  426 tracked Markdown links resolving, and clean diff checks.

## T3-027 through T3-035 adjacency determination

No direct ESAF support was omitted from `T3-027` through `T3-035`; all nine
negative dispositions correctly reject adjacency:

- `T3-027` requires the Assessor to use logs to confirm an anti-malware
  installation is operating. `MON-100` requires risk-proportionate AI
  telemetry, while `AUD-120` requires sufficient evidence for AI assessment
  procedures and determinations. Neither requires logs, the anti-malware
  product check, the confirmation outcome, or the external Assessor action.
- `T3-028` requires Assessor verification of anti-malware updates against the
  vendor's configuration instructions. `INF-110` approved baselines and
  `INF-120` vulnerability treatment do not prescribe that vendor-specific
  update criterion or manual verification procedure.
- `T3-029` is a conjunctive external pass/fail rule. `AUD-100` assessment
  criteria and `AUD-120` evidence sufficiency do not establish the two checks,
  observed results, or aggregate verdict.
- `T3-030` defines full sampled-device applicability for the certificate-based
  allow-listing sub-test. `INF-110`, `INF-140`, and `AUD-100` do not define
  that product class, sample, per-device coverage, or sub-test execution.
- `T3-031` requires an Assessor comparison against an operating-system
  manufacturer's trusted-root set. `INF-140` requires approved cryptographic
  protection for specified AI assets and paths, not that root-set baseline or
  comparison procedure.
- `T3-032` requires Assessor verification of explicit Applicant agreement for
  each additional root. General approval and controlled-configuration duties
  do not supply the certificate-specific object, Applicant actor, per-root
  coverage, or external verification.
- `T3-033` and `T3-034` require observed device-execution outcomes for unsigned
  and untrusted-chain executables. `INF-110` hardening, `INF-140`
  cryptographic protection, and `APP-140` controlled secure-development and
  build practices do not require these external execution tests or establish
  that either executable cannot run. `APP-140` guidance mentioning code
  signing is non-normative and cannot manufacture support.
- `T3-035` requires Assessor verification that operating-system policy covers
  every applicable executable format. `INF-110` and `APP-140` do not require
  that operating-system code-signing policy, every-format population, or
  external check.

Each rationale expressly names the absent procedure, product-specific check,
population, observed outcome, coverage, or aggregate verdict. The records do
not turn configuration recommendations, vendor mechanics, test mechanics, or
neighboring control capabilities into direct support.

## Full-T3 consistency and T3-014 determination

The complete T3 group is internally consistent. `T3-001`, `T3-004`,
`T3-007`, `T3-018`, `T3-026`, and `T3-030` all reject conversion of ESAF
scope, audit sampling, or control duties into the external assessment
population. Email failure rules `T3-015` and `T3-016` are treated consistently
with parallel browser failure rules `T3-024` and `T3-025`. Aggregate rules
`T3-017`, `T3-029`, `T3-036`, and `T3-037` consistently remain negative;
ESAF evidence or validation duties do not supply scheme-specific pass/fail
logic. `T3-019` remains a negative recommendation and is not promoted into a
mandatory ESAF outcome.

`T3-014 -> AUD-120` remains the sole justified T3 positive. The exact
normative `AUD-120` duty to obtain and retain attributable,
integrity-protected evidence sufficient to support each AI assessment
procedure and determination directly contributes to recording an attempted
attachment-opening outcome when that attempt is an ESAF-governed assessment
procedure and the outcome is necessary evidence. Its condition narrows an
existing evidence duty; it does not create the attempt, procedure, Assessor
assignment, observed result, or per-attachment coverage. Its rationale,
expected evidence, known gaps, and prohibited inferences preserve those
limits.

The negatives in `T3-027` and `T3-029` do not contradict `T3-014`.
`T3-014` is the external evidence-recording outcome itself. `T3-027` instead
requires a particular evidence source and product-specific confirmation
procedure, and `T3-029` requires an aggregate scheme verdict. AUD-120 supplies
neither. No other T3 provision has the same narrow recording outcome backed by
exact normative ESAF text.

## Source protection and overclaiming verdict

The 18 new records stay within the pinned public v3.2 source boundary, use
approved oracle structure and original paraphrases, reproduce no prohibited
source passage or IASME-derived structure, and do not imply that this pinned
publication is the complete current operational scheme. T3-030's corrected
negative rationale no longer reproduces the prohibited five-word source
window and passed the frozen copy guard.

All 37 records remain draft and forward-only `esaf_to_external`. No record or
leg implies procedure execution, observed results, device, sample, attachment,
or population coverage, aggregate pass/fail, certification, compliance,
equivalence, endorsement, current-scheme completeness, full-population
assurance, or continuous assurance.

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

## Disposition

Approved. Exact candidate
`fa3c8c8bef60b0f779849797f348701e900a22fd` is approved for Task 8
T3-020-037 technical closure from the security and overclaiming perspective,
including the required complete-T3 consistency review. No Critical or
Important findings remain. This approval does not promote the draft snapshot
or establish procedure execution, an observed result, device or population
coverage, aggregate pass/fail status, certification, compliance, equivalence,
endorsement, current-scheme completeness, full-population assurance, or
continuous assurance.
