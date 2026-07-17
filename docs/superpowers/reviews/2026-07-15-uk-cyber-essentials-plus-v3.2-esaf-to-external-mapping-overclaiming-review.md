# Cyber Essentials Plus v3.2 ESAF-to-external mapping overclaiming review

reviewer_id: codex-ce-plus-final-overclaiming-reviewer
reviewer_authorized_source_access: true
reviewed_baseline_sha: b4529c05c440db2f94ec12db4f21e3d0af57a5fb
reviewed_candidate_sha: 0d141a6d5fff01cfb218ba8ac4f3cdc565739cf3
review_scope: complete candidate delta over the immutable baseline, including all 144 forward-mapping records and publication metadata
disposition: approved for the stated draft boundary

## Verdict

No Critical, Important, or Minor overclaiming findings remain unresolved. This review is limited to the immutable candidate SHA above; it is not a scheme assessment, certification decision, lifecycle transition, or approval of the current operational Cyber Essentials Plus scheme.

## Independent review performed

- Reviewed the complete `b4529c0..0d141a6` candidate delta, required implementation and traceability records, rights attestation, snapshot README, landing-page context, and all 144 provision records.
- Verified source-copy protection across every record narrative using the locked five-word source-window guard; no copied-source window was found. The records use the permitted identifiers, locators, structural metadata, original paraphrases, and derivative analysis only. The snapshot preserves the IASME partition and excludes marks, imagery, and third-party material.
- Verified source pins and boundaries: the public NCSC v3.2 canonical PDF identity, legacy-PDF distinction, oracle digest, OGL v3.0 attribution, rights-attestation ancestry, and explicit exclusion of later/current operational-scheme or nonpublic Delivery Partner methods.
- Reviewed all 137 `no_direct_mapping` dispositions. Each states a provision-specific missing outcome, has no relationship leg, and does not use generic rationale. They do not manufacture coverage, testing execution, observation, aggregate sufficiency, certification, compliance, equivalence, endorsement, or any external verdict.
- Reviewed all 8 positive legs in 7 records. Each is forward-only `partially_supports`, has a narrow condition tied to its exact normative ESAF safeguard, and retains expected evidence, known gaps, and prohibited inferences. Conditions narrow scope rather than create an absent procedure, result, observation, population, or outcome.
- Independently reassessed `CEPTS3.2-T5-006`. `IAM-120` is bounded to approved-role authorization of an in-scope administrative AI action; `IAM-130` is bounded to separately authenticated privileged access for an enumerated AI asset. Neither leg claims credential entry, prompt observation, attempted execution, device or population coverage, observed result, aggregate verdict, or any assurance outcome. The record does not reuse the feasibility probe text.
- Verified procedure/result separation in the mapped and negative records, including that evidence retention or access-control contributions do not imply procedure execution, observed results, or aggregate pass/fail determinations.
- Verified Delivery Partner discretion is not inferred: Appendix A authorization/scoping remains procedural; Appendix B tailoring and complete-file responsibilities remain unmapped; C-008 through C-011 retain Delivery Partner ownership, the less-than-five-percent and no-broader-failure conjunction, and the prohibition on waiving predicates, revising observations, or deciding an overall pass from ESAF controls.
- Verified navigation and traceability language retains feasibility-time historical context, distinguishes the separate core v3.3 and Plus v3.2 artifacts, preserves `external_to_esaf` as unimplemented, and describes complete-publication as pinned-source inventory coverage only. Derived totals are stated as 144 records, 8 legs, 7 distinct controls, and 137 negative dispositions, with no aggregate or coverage claim.

## Evidence

`python -m unittest tests.test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping -v` passed: 35 tests. The focused suite exercises all-record oracle and narrative checks, source-window protection, negative-disposition specificity, condition boundaries, T5-006 feasibility-text separation, Delivery Partner boundaries, draft/current-scheme language, identity separation, and mutation failures for the relevant prohibited changes. `git diff --check b4529c05c440db2f94ec12db4f21e3d0af57a5fb..0d141a6d5fff01cfb218ba8ac4f3cdc565739cf3` also passed.

## Findings

| Severity | Count | Unresolved |
|---|---:|---:|
| Critical | 0 | 0 |
| Important | 0 | 0 |
| Minor | 0 | 0 |
