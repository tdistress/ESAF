---
review_type: security-and-overclaiming
reviewer_id: codex-ce-plus-c-overclaiming-reviewer
reviewer_authorized_source_access: true
review_date: 2026-07-17
base_sha: d77768feee5b75bf3a71a5b503729ffe5baf8119
candidate_sha: 39f9dfa3eafe358929dddd63106be502f924a879
scope: CEPTS3.2-C-001 through CEPTS3.2-C-013
verdict: approved
critical_findings_remaining: 0
important_findings_remaining: 0
minor_findings_remaining: 0
---

# Cyber Essentials Plus v3.2 C security and overclaiming review

## Review identity and candidate binding

This immutable review binds only to candidate `39f9dfa3eafe358929dddd63106be502f924a879` over base `d77768feee5b75bf3a71a5b503729ffe5baf8119`. The reviewer is `codex-ce-plus-c-overclaiming-reviewer`, had authorized source access, and is distinct from mapper `esaf-crosswalk-editorial-team`, mapping-rights reviewer `esaf-publication-rights-reviewer`, and specification reviewer `codex-ce-plus-c-specification-reviewer`.

## Scope, method, and evidence

The review was read-only except for creation of this report. It examined the Task 11 brief, implementation report, exact `d77768feee5b75bf3a71a5b503729ffe5baf8119..39f9dfa3eafe358929dddd63106be502f924a879` diff package, all thirteen candidate C records, locked oracle rows for `CEPTS3.2-C-001` through `CEPTS3.2-C-013`, and exact plausible ESAF `0.4-alpha` `## Requirement` text at baseline `b4529c05c440db2f94ec12db4f21e3d0af57a5fb`.

The audit covered source/version and actor boundaries, procedure/decision/result separation, external exception ownership, predicate conjunction, observation immutability, negative specificity, copied-source protection, aggregate and certificate actions, prohibited inferences, and batch consistency. The locked oracle checksum was independently confirmed as `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`, and candidate scope was confirmed as the reported 17 paths. Broad suites were not rerun; the passing 29-test focused module, crosswalk checks, baseline check, link check, diff check, full 324-test suite, and source-window guard results were taken from the implementation report as directed.

## Findings

### Critical

None.

### Important

None.

### Minor

None.

## Independent challenge to the all-negative disposition

The all-negative result is justified by exact normative scope, not merely by actor-name mismatch. The closest plausible ESAF requirements were challenged independently:

- `AUD-100` requires an organizational AI assessment program with methods, evidence, reporting, and follow-up, but does not require an Assessor to execute or conclude this external scheme, consult its Delivery Partner, or assign a Cyber Essentials Plus result.
- `AUD-120` requires sufficient evidence for each organizational AI assessment procedure and determination, but does not perform prescribed external tests, establish their population or observations, or supply any scheme determination.
- `AUD-130` requires organizational classification, remediation, escalation, retest, closure, and evidence for AI assessment findings. It neither classifies Cyber Essentials Plus deviations as marginal nor revises the Assessor's observation, applies the external less-than-five-percent threshold, or establishes absence of broader process failure.
- `CMP-110` governs organizational records, reports, and evidence according to applicable requirements, but does not itself impose the C-001 report-completion procedure or any Delivery Partner consultation, aggregate verdict, or certificate action.
- `GOV-140` governs ESAF exceptions through an organizational process. It cannot make or constrain the Delivery Partner's separate discretionary scheme exception, waive either external predicate, or authorize a Plus certificate.
- General ESAF escalation, continuity, remediation, exception, evidence, and decision requirements similarly remain internal implementation duties and cannot manufacture the missing external actor action, performed-test result, threshold classification, aggregate decision, or certification consequence.

Accordingly, conditions could not rescue a positive leg: there is no exact ESAF outcome to narrow. Adding a relationship would overstate adjacency as direct normative support. Each record correctly uses `no_direct_mapping`, has an empty relationship list, and names its missing outcome specifically.

## Per-record actor and outcome determination

| Record | Independent determination |
|---|---|
| C-001 | Negative retained. Organizational evidence or reporting duties do not require the Assessor to compile the external report after completion of every prescribed test and do not prove completion. |
| C-002 | Negative retained. ESAF escalation governance does not require consultation with the Delivery Partner when the appointed-day assessment remains unfinished. |
| C-003 | Negative retained. No ESAF requirement grants the Delivery Partner authority to defer unfinished scheme tests. |
| C-004 | Negative retained. ESAF remediation or exception timing does not supply the Delivery Partner's scheme-specific one-month deferral recommendation. |
| C-005 | Negative retained. ESAF cannot establish that every performed scheme case passed or require the Assessor to assign the resulting aggregate pass. |
| C-006 | Negative retained. ESAF neither establishes the prerequisite normal overall pass nor instructs the Assessor to award the Plus certificate. |
| C-007 | Negative retained. ESAF cannot classify external failures as only a few minor issues or perform the resulting Assessor-to-Delivery-Partner consultation. |
| C-008 | Negative retained. The discretionary overall-pass decision belongs solely to the Delivery Partner and requires both C-010 and C-011; no control may make the decision, waive a predicate, revise an observation, or convert implementation into the verdict. |
| C-009 | Negative retained. ESAF neither creates the Delivery Partner exception outcome nor authorizes the Assessor's consequent Plus certificate award. |
| C-010 | Negative retained. No ESAF requirement counts performed external tests or establishes the Delivery Partner's marginal-deviation threshold of less than five percent; C-011 remains independently necessary. |
| C-011 | Negative retained. No ESAF requirement establishes the Delivery Partner's absence-of-broader-process-failure predicate; C-010 remains independently necessary. |
| C-012 | Negative retained. ESAF cannot evaluate both pass routes over the external results or require the Assessor to assign the residual aggregate failure. |
| C-013 | Negative retained. ESAF neither establishes the prerequisite residual failure nor instructs the Assessor to withhold the Plus certificate. |

## Conjunction, exception ownership, and observation immutability

C-008, C-010, and C-011 correctly preserve one conjunctive external decision boundary. C-010 is the Delivery Partner's first predicate: marginal deviations in less than five percent of performed tests. C-011 is its second, distinct predicate: no evidence of broader failure in the Applicant's cybersecurity processes. Both predicates are necessary, neither is sufficient, and C-008 remains discretionary even when both hold.

The records do not let an ESAF control count tests, classify the deviation threshold, establish an absence of broader process failure, revise an Assessor observation, waive either predicate, or make the exceptional pass decision. The rationales expressly preserve the other predicate and the overall-pass gap. This is the required separation between technical implementation, immutable external observations, predicate evaluation, and Delivery Partner discretion.

## Aggregate and certificate determinations

C-005 and C-012 correctly remain negative result rules. Their outcomes depend on the complete performed-case result set and branching logic, which ESAF controls do not execute, observe, aggregate, or adjudicate. Internal testing, evidence, findings, or control status cannot become an external overall pass or residual failure.

C-006, C-009, and C-013 correctly remain negative certificate actions. Each certificate action depends on a prior scheme outcome that ESAF cannot establish: the normal pass for C-006, the Delivery Partner exception pass for C-009, and the residual failure for C-013. ESAF neither awards nor withholds Cyber Essentials Plus certification and supplies no authority to the Assessor for those actions.

No record infers procedure execution, observation, population coverage, pass/fail, certification, compliance, equivalence, endorsement, current-scheme completeness, full-population assurance, or continuous assurance.

## Source, copy protection, and consistency verdict

All thirteen records preserve the locked v3.2 oracle identifiers, groups, kinds, actors, official URL, page/section locators, and original paraphrase mode. Actor ownership is consistent: Assessor for C-001, C-002, C-005 through C-007, C-009, C-012, and C-013; Delivery Partner for C-003, C-004, C-008, C-010, and C-011. The narratives do not introduce copied-source or IASME-derived structures. The reported source-window guard covered candidate narrative fields and passed; no candidate change adds a copy-protection exemption or bypass.

The batch is internally consistent as thirteen draft negative records, zero relationships, zero referenced controls, forward-only `esaf_to_external`, an unchanged empty lifecycle event array, and generated counts of 126 snapshot provisions, 242 repository provisions, 49 relationships, and 195 negative dispositions.

## Verdict

`APPROVED`. No Critical, Important, or Minor findings remain. The thirteen negative dispositions preserve source and actor boundaries, the C-008/C-010/C-011 predicate conjunction and Delivery Partner discretion, observation immutability, aggregate-result and certificate separation, specific missing outcomes, and the prohibition on unsupported assurance or scheme claims at exact candidate `39f9dfa3eafe358929dddd63106be502f924a879`.
