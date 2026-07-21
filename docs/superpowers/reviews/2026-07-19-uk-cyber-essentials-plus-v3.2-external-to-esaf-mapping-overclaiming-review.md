# Cyber Essentials Plus v3.2 external-to-ESAF mapping security and overclaiming review

reviewer_id: codex-ce-plus-reverse-final-overclaiming-reviewer
reviewer_authorized_source_access: true
review_date: 2026-07-19
reviewed_base_sha: e4de0a5d3801431d96e49a746069834fa0b4d370
reviewed_candidate_sha: 969854ac58138bb58b8555687d30c64f12e78ed7
reviewed_esaf_baseline_sha: 7461d7137e3faf36b2b73a15f71100fa4ce11159
review_package_sha256: 54550d2d350eb44f39604ecc1e33f73525a31e93cca4a53108af3ef3be18f0a7
review_scope: complete merge-base range, all 144 external-to-ESAF records, validation profile, traceability, and publication metadata
disposition: approved for the stated unqualified technical-draft boundary

## Security and overclaiming verdict

PASS. No Critical, Important, or Minor security or overclaiming finding remains unresolved in the exact candidate above. The prior Important I-1 concerning missing candidate-owned traceability is resolved by the committed traceability record and an unconditional focused regression.

This is an independent technical-draft review, not qualified Cyber Essentials SME approval, scheme or certification approval, a compliance or equivalence determination, evidence of implementation or effectiveness, or an ESAF lifecycle transition. It does not approve the current operational Cyber Essentials Plus scheme or extend the pinned public v3.2 source boundary.

## Independent review performed

- Verified that the supplied 1,594,985-byte review package is bound to `e4de0a5d3801431d96e49a746069834fa0b4d370..969854ac58138bb58b8555687d30c64f12e78ed7`; its embedded 166-file patch byte-matches `git diff -U10` for that exact range.
- Re-reviewed the complete range and the new candidate-owned traceability record. The only candidate change after the first content review is the traceability record and its focused regression; the 144 mapping records, reverse profile, manifest, README, lifecycle, catalogs, navigation, and backlog are unchanged from the previously inspected content.
- Reconciled all 144 records to the locked oracle in oracle order: M 24, T1 16, S 11, T2 9, T3 37, T4 9, T5 7, C 13, A 4, and B 14. There are 32 mapped provisions with 32 reverse-only `external_to_esaf` / `partially_supports` legs referencing 10 distinct controls, plus 112 unique, relationship-free `no_direct_mapping` dispositions.
- Reassessed every positive leg against the exact immutable ESAF requirement. Each leg describes a bounded result rather than tool use, authorization, assessor activity, procedure execution, a file, a score alone, or an adjacent capability. Its ordered 11-condition contract narrows actor, scope, population, sample, dates, method, provenance, exceptions, Delivery Partner discretion, and point-in-time status; it does not create a missing external result or ESAF outcome.
- Reassessed every negative disposition. Scanner authorization and execution, sampling instructions, file supply and retention duties without their own mapped result, recommendations, case-level aggregation, certification actions, and Delivery Partner consultation or discretion remain negative. Each negative names its own external result and missing ESAF outcome; no rationale is generic or repeated.
- Reassessed the positive sub-test result rules, including T3-017, T3-029, and T3-036. Their legs are limited to the recorded branch or configuration-check result and do not infer the parent test-case result, overall assessment, aggregate sufficiency, implementation, effectiveness, or population-wide state.
- Independently reassessed T5-006. Its single IAM-130 leg is limited to a dated observation of restriction and separate authentication for an AI-changing privileged workflow. It excludes other privileged workflows, unsampled devices, later state, time-bounding, monitoring, periodic review, aggregate assessment, and certificate outcome. T5-001 through T5-005 and T5-007 remain negative.
- Verified Delivery Partner boundaries across all records. The condition requires recording any applicable choice, method, approval, or basis for none; it does not infer private methodology or allow discretion to create support. Appendix A authorization, Appendix B selection and file duties, and C-002 through C-013 consultation, exception, aggregate, and certification actions remain relationship-free.
- Verified release provenance. All 32 legs resolve exact control version, path, digest, and `## Requirement` locator through the deterministic 91-control manifest pinned to ESAF commit `7461d7137e3faf36b2b73a15f71100fa4ce11159`; no stale or adjacent-control binding was found.
- Verified source and rights boundaries against the pinned 424,226-byte canonical NCSC PDF with SHA-256 `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`. The focused five-word guard passed for all record narratives. An independent five-word scan of the new traceability record found only the permitted publication title. No copied requirement passage, IASME-derived structure, mark, imagery, source download, or unlicensed third-party material is introduced. OGL v3.0 attribution and the current-scheme exclusion remain explicit.
- Checked the README, lifecycle registry, generated catalog, UK landing page, backlog, and traceability together. Counts are derived consistently; lifecycle remains draft with `events: []`; feasibility statements are explicitly historical; the separate forward and reverse snapshots are not combined; and no narrative asserts certification, compliance, equivalence, endorsement, implementation, effectiveness, sufficiency, full-population coverage, or continuous assurance.

## Commands and results

- `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_uk_cyber_essentials_plus_v32_external_to_esaf_mapping -v` — PASS; 63 tests ran in 59.570 seconds with `OK`.
- `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/validate_crosswalks.py --check` — PASS; `Crosswalk catalog valid: 3 mapping sets, 404 provisions, 81 relationships, and 325 negative dispositions.`
- `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/validate_crosswalks.py --check --baseline-ref e4de0a5d3801431d96e49a746069834fa0b4d370` — PASS with the same derived totals.
- `git diff --check e4de0a5d3801431d96e49a746069834fa0b4d370..969854ac58138bb58b8555687d30c64f12e78ed7` — PASS; exit code 0 with no output.

## Findings

| Severity | Count | Unresolved |
|---|---:|---:|
| Critical | 0 | 0 |
| Important | 0 | 0 |
| Minor | 0 | 0 |
