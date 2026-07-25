# UK Pilot Profile Whole-Branch Remediation Design

**Date:** 2026-07-24  
**Issue:** #57  
**Reviewed candidate:** `bdfa078a890c6bf7fba5d06eeda6701ac2c67c4e`  
**Merge base:** `9715ddcd59eac0a92c72cf748db869e50f39359b`

## 1. Purpose

This design resolves the Important and Minor findings from the four independent
whole-branch reviews of the Draft United Kingdom profile. It preserves the
approved profile architecture while making the reusable contract fail closed,
separating generic validation from pilot-specific policy, aligning exact
applicability facts with control selections, and strengthening the normative
source and non-claim boundaries.

No remediation may claim legal compliance, Cyber Essentials implementation or
certification, equivalence, endorsement, external approval, or production
readiness. The United Kingdom package remains Draft.

## 2. Selected architecture

Validation shall use two explicit layers:

1. A reusable profile core shall validate inventory, package structure,
   identity and version coupling, schema formats, declared external references,
   traceability, source bases, control preservation, and non-claim semantics.
2. A United Kingdom pilot policy shall require the exact pilot identity,
   complete 91-control population, and three pinned Draft mapping references.

The generic layer shall not require a future profile to cite United Kingdom
Cyber Essentials mappings. The pilot policy shall not weaken the generic layer.

A separate United Kingdom-only validator is rejected because it would fragment
the contract. Self-declared policy that can relax validator invariants is
rejected because a profile could weaken its own gate.

## 3. Fail-closed inventory and identity

The loader shall inspect every entry beneath `profiles/`, except the documented
contract, schema directory, and allowed index files. It shall reject:

- a missing profile root or zero profile packages in this repository;
- malformed profile-domain or version directory names;
- unexpected files or directories;
- symlinked inventory entries;
- missing manifests; and
- package entries that are silently skipped.

Generic terminology shall use **profile domain**, not country or jurisdiction,
because the framework supports jurisdiction, industry, sector, and risk
profiles.

The semantic validator shall require:

- the version suffix of `profile_id` to equal `profile_version`;
- `profile_version` to equal the package version directory;
- every component identity and version to equal the manifest; and
- semantic versions to use the established repository format.

## 4. Schema and operational behavior

JSON Schema validation shall use a format checker so calendar dates are real
dates. Reusable component schemas shall accept valid semantic profile versions
rather than pin every future package to the pilot version.

Malformed content shall remain a content failure. Filesystem, permission,
schema-loading, and registry-reading failures shall be sanitized, shall not
disclose host paths, and shall produce the operational-failure exit class.

Component paths are **package-relative paths** resolved beneath the package
root. `$schema` values are document-relative schema locators. The approved
design, plan, normative contract, schema descriptions, and contributor guidance
shall use those terms consistently.

## 5. External-reference and lifecycle semantics

The generic external-reference schema shall permit an empty reference array.
Each declared nonempty reference shall:

- identify a normalized repository-relative lifecycle-record path;
- resolve to the declared mapping-set identifier;
- resolve to the authoritative mapping snapshot;
- compare `expected_status` to the snapshot editorial status; and
- validate the lifecycle record consistently with that editorial status.

`expected_status` shall support the mapping editorial sequence `draft`,
`reviewed`, and `approved`, plus later governed lifecycle states where the
existing contract requires them. Draft and reviewed snapshots shall retain
empty event arrays. Approved or later states shall be established by governed
registry events. Empty events shall not, by themselves, be interpreted as
Draft.

The United Kingdom pilot policy shall independently require its exact three
mapping identifiers, exact lifecycle-record paths, expected Draft editorial
status, lifecycle-reference-only use, qualified review, and explicit non-import
statements.

A referenced artifact transition shall require an explicit profile update
before the new state is relied upon. It shall not silently change the profile
lifecycle. Neither the profile nor the referenced artifact may be represented
beyond its independently governed recorded state.

## 6. Source and authority boundaries

ESAF-1800 shall normatively require each profile to identify permitted and
excluded sources and to distinguish original ESAF synthesis from legal,
regulatory, or external-scheme assertions. Additional risks and overlays shall
be original ESAF synthesis.

Machine enforcement shall:

- require every risk `source_basis` value to resolve to an authoritative ESAF
  control or a permitted source identifier;
- reject unresolved or excluded source bases;
- detect affirmative narrative claims that an excluded authority governs or
  supplies a profile selection;
- detect imported mapping relationships or external outcomes across every
  narrative field; and
- preserve explicit denial, quotation, and metalinguistic discussion.

The validator is not expected to prove the origin of arbitrary prose. Its
bounded source-reference and assertion checks shall fail closed for declared
sources and common authority/import claims, while independent review remains
mandatory for semantic originality.

## 7. Assertion and control-preservation enforcement

Assertion-aware checks shall cover:

- weakening predicates before or after control language;
- explicit control identifiers as well as generic control terms;
- `supersede`, `lower`, `exempt`, `need not apply`, `no longer applies`,
  `render optional`, and standalone inapplicability forms;
- common affirmative compliance, certification, legal-sufficiency, scheme
  satisfaction, eligibility, and named-authority approval forms; and
- affirmative mapping-support, mapping-satisfaction, and external-outcome
  import forms.

Each family shall have affirmative, denial, quotation, metalinguistic, and
coordinated-clause regression coverage. A denial in one clause shall not mask
an affirmative assertion in another.

## 8. UK applicability corrections

The package shall add or revise bounded boolean conditions so:

- `APP-150` activates only when an internet-reachable AI application interface
  or privileged application workflow exists;
- `API-140` activates only when an external AI service integration exists; and
- `API-150` activates on the factual presence of an E1–E4 capability with a
  material provider or platform dependency, without asking whether an exit
  obligation has already been decided.

The affected selections, risks, overlays, evidence expectations, README
instructions, and reciprocal links shall move together. Counterexample tests
shall cover:

- an internet-reachable administration console without an exposed AI
  application interface;
- a downloaded external model without an external service integration; and
- a material E1–E4 dependency without a pre-existing exit decision.

Every overlay control shall appear in at least one linked risk's source basis
or affected-control set. Authenticated-administration language shall either
trace to the applicable IAM controls and evidence or defer explicitly to the
universal privileged-configuration chain.

## 9. Editorial corrections

`not_selected` rationales shall be descriptive applicability analysis and shall
not contain `shall`, `should`, or `must`.

Generic profile documentation shall use neutral profile-domain terminology.
Lifecycle guidance shall say a profile shall not advance beyond Draft until
required review and publication gates are complete, preserving `proposed` as a
valid earlier state.

The pilot shall contain one consolidated pre-publication `0.1.0` change-history
entry. Workflow integration tests shall inspect the pull-request path block,
push path block, and validation-job steps rather than relying on whole-file
string counts.

## 10. Test and review strategy

Every behavioral correction shall begin with a focused failing regression test.
Implementation shall proceed in three sequential clusters:

1. reusable validator, schema, source, mapping-lifecycle, and assertion gates;
2. normative and editorial contract alignment; and
3. UK condition and traceability corrections.

After each cluster, affected focused tests and validators shall pass. After all
clusters, the candidate shall pass every Task 7 preflight gate except the
repository-wide suite, which remains part of Task 8.

Because the candidate head changes, all four independent whole-branch reviews
shall be redispatched against the same new full SHA:

1. technical/schema/validator correctness;
2. normative/editorial consistency;
3. profile applicability, control selection, and source boundary; and
4. overclaiming, mapping leakage, and lifecycle separation.

All Critical and Important findings shall be resolved before review records are
committed. Minor findings shall be resolved or explicitly dispositioned with
evidence.

## 11. Acceptance criteria

The remediation is complete when:

- generic validation is reusable and fail closed;
- the United Kingdom exact-reference policy is profile scoped;
- mapping editorial and registry lifecycle states cannot be conflated;
- all source, non-claim, and control-preservation regressions pass;
- all three corrected control triggers are purely factual and exact;
- the risk, overlay, evidence, condition, and control graph is reciprocal and
  semantically aligned;
- normative and companion documents contain no identified contradictions;
- focused tests and all Task 7 preflight validators pass on the exact candidate;
  and
- all four independent whole-branch reviews report no unresolved Critical or
  Important findings.
