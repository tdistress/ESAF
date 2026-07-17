---
review_type: security-and-overclaiming
reviewer_id: codex-ce-plus-t5-overclaiming-reviewer
reviewer_authorized_source_access: true
review_date: 2026-07-17
base_sha: b3f25025e5f8334ba7a2557db9a8fe6a946cfefb
candidate_sha: f2242473a24e257400ee05224bff8fcecaa7224b
scope: CEPTS3.2-T5-001 through CEPTS3.2-T5-007
verdict: approved
critical_findings_remaining: 0
important_findings_remaining: 0
minor_findings_remaining: 0
---

# Cyber Essentials Plus v3.2 T5 security and overclaiming review

## Review identity and candidate binding

This immutable review binds only to candidate `f2242473a24e257400ee05224bff8fcecaa7224b` over base `b3f25025e5f8334ba7a2557db9a8fe6a946cfefb`. The reviewer is `codex-ce-plus-t5-overclaiming-reviewer` and had authorized source access. This identity is distinct from mapper `esaf-crosswalk-editorial-team`, mapping-rights reviewer `esaf-publication-rights-reviewer`, and normative-basis reviewer `codex-ce-plus-t5-normative-basis-reviewer`.

## Scope, method, and evidence

The review was read-only except for replacement of this report. It examined the Task 10 brief, updated implementation report, exact two-commit diff package, all seven candidate T5 records, locked oracle rows for `CEPTS3.2-T5-001` through `CEPTS3.2-T5-007`, pinned `0.4-alpha` IAM-120 and IAM-130 `## Requirement` text at baseline commit `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`, copy-guard implementation and caller coverage, the new regression, and feasibility material solely for independence comparison.

The audit covered source/version and actor boundaries, procedure/result separation, negative specificity, feasibility independence, conditions, gaps, evidence, prohibited inferences, consistency, and copied-source bypass risk. As a focused confirmation, the new copy-guard regression and completed-batch oracle/manifest fidelity test both passed at the exact candidate in 0.204 seconds. Broad suites were not rerun; their results were taken from the implementation report.

## Findings

### Critical

None.

### Important

None.

### Minor

None.

## Prior finding I-1 resolution

**Resolved.** The superseded candidate's globally consulted digest exemption for normalized text `test on every sampled device` and its unconditional skip have both been removed. The guard now applies the protected-source digest set uniformly to every narrative yielded by `record_narratives`: context summary, negative rationale, relationship rationale, conditions, expected evidence, known gaps, and prohibited inferences. The amended code contains no replacement record-wide, field-wide, or digest-specific bypass.

The regression `test_source_copy_guard_rejects_t5_003_derivative_window` directly supplies the formerly exempt protected digest and confirms that the surrounded five-word window raises. The completed-batch check also confirms all candidate narratives pass the unexempted source-window guard. The regression was reported RED on the vulnerable implementation and GREEN after removal; the focused re-review reproduced GREEN at candidate `f2242473a24e257400ee05224bff8fcecaa7224b`.

T5-003 preserves the exact locked oracle metadata and four-word context summary `Test every sampled device.` Its revised derivative rationale remains specific: ESAF does not require Assessor execution throughout the selected device sample and does not define or complete that assessment population. This preserves both complete sampled-device coverage and procedure-execution gaps without reproducing the protected five-word window. No new copy-guard bypass was introduced.

## T5-006 independent relationship determination

### IAM-120

Retain the IAM-120 leg as `partially_supports`, `narrow`, subject to its stated condition. The exact requirement mandates authorization of AI assets and actions by approved purpose, role, attributes, context, and least privilege, expressly including administration. When the process is an IAM-120 AI action and the ordinary user role is not approved for it, the requirement directly contributes to the restriction predicate represented by T5-006.

The leg does not create ordinary-credential semantics, separate-authentication behavior or the exact prompt, process selection or launch, credential entry, execution, device/process context, tested-population coverage, observation, a sub-test result, or an aggregate verdict. Its condition narrows support rather than supplying missing external mechanics. No removal, expansion, or additional IAM-120 relationship is warranted.

### IAM-130

Retain the IAM-130 leg as `partially_supports`, `narrow`, subject to its stated condition. The exact requirement independently mandates restriction and separate authentication for privileged access capable of changing one of its enumerated AI assets. When the process satisfies that scope predicate, IAM-130 directly contributes to the restriction and separate-authentication safeguards underlying T5-006.

The leg does not define ordinary credentials, require the exact additional-login request observable in this procedure, show credential entry or rejection during an attempt, select, launch, or execute the external process, establish device/process or population context, prove observation, or assign sub-test or aggregate verdicts. Its statement that IAM-130 contributes to both access predicates remains acceptable only with the existing condition, gaps, and prohibited-inference language; it is not evidence that the external result occurred. No removal, expansion, or additional IAM-130 relationship is warranted.

### Combined-leg determination

The legs stand independently and may coexist. IAM-120 supplies a role/least-privilege authorization contribution; IAM-130 supplies an independently scoped privileged-access restriction and separate-authentication contribution. Their combination still does not manufacture ordinary credentials, the exact prompt, external process selection/launch/execution, device/process context, tested population, observed attempt or result, sub-test disposition, or aggregate verdict. It does not establish test execution, pass/fail, certification, compliance, equivalence, endorsement, current-scheme completeness, full-population assurance, or continuous assurance.

## Preserved gaps and procedure/result separation

T5-001 through T5-005 and T5-007 correctly remain `no_direct_mapping`. Their rationales identify the missing external applicability, account-state procedure, complete sample coverage, operating-system-specific observed attempt, repetition, and aggregate result-chain outcomes. They do not convert access-control safeguards into proof that an Assessor acted, covered a population, observed a result, or assigned a verdict.

T5-006 preserves ordinary-credential meaning, the exact separate-authentication prompt, external procedure selection/launch/execution, device/process context, tested-population coverage, observed attempt/result, and sub-test/aggregate-verdict gaps. Its expected evidence concerns implementation of the cited ESAF safeguard, not execution or passage of the external test. Across the batch, no execution, result, coverage, pass/fail, certification, compliance, equivalence, endorsement, current-scheme completeness, full-population assurance, or continuous assurance is inferred.

## Feasibility independence and consistency

The amended commit changes no T5-006 relationship content. The record contains no feasibility identifiers or feasibility-disposition markers; its two rationales remain requirement-specific rather than copied feasibility prose. Independent comparison to the pinned requirements continues to support both retained legs, and the feasibility seed supplies no additional relationship, condition, or outcome.

All seven records remain draft, preserve the Assessor actor and exact source version/locator metadata from the locked oracle, and use only `esaf_to_external`. The batch remains internally consistent as six negative records and one mapped record with two separately justified legs.

## Copy-guard verdict

Pass. I-1 is closed for all narrative fields and records. The vulnerable global digest exemption and skip are absent; the formerly exempt source window is explicitly rejected; all completed candidate narratives pass the unexempted guard; and T5-003 preserves precise, source-faithful negative semantics without copied protected prose.

## Verdict

`APPROVED`. No Critical, Important, or Minor findings remain. The T5 dispositions, both narrow T5-006 legs, preserved gaps, feasibility independence, procedure/result boundary, and copied-source controls satisfy the Task 10 security and overclaiming requirements at exact candidate `f2242473a24e257400ee05224bff8fcecaa7224b`.
