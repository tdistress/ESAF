# UK Cyber Essentials v3.3 Crosswalk Design

**Status:** Approved for implementation planning

**Date:** 2026-07-13

**Target:** ESAF-1600 validated draft mapping set

## 1. Purpose

This design defines the first substantive ESAF-1600 mapping set: a complete-publication, atomic crosswalk from the ESAF 0.4-alpha control catalog to the UK National Cyber Security Centre (NCSC) *Cyber Essentials: Requirements for IT Infrastructure v3.3*.

The mapping set answers one analytical question: how does an ESAF control contribute to an individual Cyber Essentials v3.3 provision? It does not assess an adopter's implementation, calculate a compliance percentage, establish equivalence, or demonstrate Cyber Essentials certification.

Cyber Essentials Plus is excluded from this mapping set. The Plus test specification shall receive a separate source-versioned mapping set because it has a distinct assurance purpose and currently published source version.

## 2. Source and baseline

### 2.1 External source

- Authority: UK National Cyber Security Centre
- Authority identifier: `uk-ncsc`
- Publication: *Cyber Essentials: Requirements for IT Infrastructure*
- Publication identifier: `cyber-essentials-requirements-for-it-infrastructure`
- Source version: `3.3`
- Publication/effective date: `2026-04-27`
- Official URL: `https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf`
- Source access date: `2026-07-13`
- PDF SHA-256: `e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923`

The source PDF is not committed. The official URL, digest, publication metadata, access date, and attribution are recorded in the mapping-set narrative and UK Cyber Essentials landing page.

### 2.2 ESAF source baseline

- ESAF release identifier: `0.4-alpha`
- ESAF label: `ESAF 0.4-alpha`
- Source commit: `5de9ff356ddad1e193444cd7308eff16ed83e811`
- Control count: 91
- Control status and version: all controls are `draft`, version `0.1.0`

`ESAF_CONTROL_MANIFEST.json` and the control-catalog SHA-256 shall be regenerated from the immutable source commit using the existing ESAF-1600 manifest tooling. Relationship legs shall resolve only to that manifest.

## 3. Publication rights

The source is public Crown copyright content. The NCSC terms state that website content may be reused under the Open Government Licence v3.0 unless otherwise indicated. The mapping set shall attribute the NCSC, link to the OGL v3.0, and avoid any implication of NCSC endorsement.

Publication-rights metadata shall use:

- mapper ID: `esaf-crosswalk-editorial-team`
- rights reviewer ID: `esaf-project-owner`
- access class: `public`
- permitted elements: `identifiers`, `titles`, `structural_inventory`, `paraphrases`, `derivative_mapping_analysis`, and `official_links`
- prohibited elements: an empty array
- restrictions: acknowledge NCSC Crown copyright and OGL v3.0; do not use NCSC or government logos; do not reproduce third-party material; do not imply endorsement, certification, or official status; prefer original paraphrases over copied requirement text

The six publication-rights elements are an exhaustive, disjoint partition as required by ESAF-1600. The mapping records shall contain original ESAF paraphrases, not copied requirement text.

## 4. Mapping-set identity and repository layout

The authoritative mapping-set identifier is:

`uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`

The authoritative snapshot root is:

`crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/`

It contains exactly:

- `README.md`
- `PROVISION_INVENTORY.md`
- `ESAF_CONTROL_MANIFEST.json`
- 116 direct-child provision records

No subdirectory, symbolic link, source PDF, scratch file, or auxiliary data file is permitted beneath the snapshot root.

The lifecycle record is:

`crosswalks/registry/uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0.md`

The mapping set and all provision records remain `draft`. The lifecycle record has an empty event array. Qualified review and approval are separate future governance actions.

## 5. Complete-publication provision inventory

The inventory contains every independently testable prescriptive provision in section D, Scope, and section E, Requirements by technical control theme. It excludes definitions, aims, examples, explanatory introductions, information boxes, section C backup guidance, section F zero-trust guidance, and statements expressly identified as non-mandatory guidance.

| Group | Record range | Count |
|---|---|---:|
| D. Scope | `ce33-d-001` through `ce33-d-044` | 44 |
| E.1 Firewalls | `ce33-e1-001` through `ce33-e1-012` | 12 |
| E.2 Secure Configuration | `ce33-e2-001` through `ce33-e2-012` | 12 |
| E.3 Security Update Management | `ce33-e3-001` through `ce33-e3-007` | 7 |
| E.4 User Access Control | `ce33-e4-001` through `ce33-e4-029` | 29 |
| E.5 Malware Protection | `ce33-e5-001` through `ce33-e5-012` | 12 |
| **Total** |  | **116** |

### 5.1 Identity convention

Each record uses a lowercase stable `record_id`, such as `ce33-e4-010`, and a corresponding inventory/external locator ID, such as `CE3.3-E4-010`. These are ESAF-assigned citation identifiers, not identifiers printed or endorsed by the NCSC. The mapping-set narrative and landing page shall make this distinction prominent.

Every record also preserves an exact human-readable locator containing the source section, subsection or table, page number, and paragraph, bullet, sub-bullet, or table-cell ordinal. The official PDF URL is repeated in `source_locator.official_url`.

### 5.2 Atomization rules

- Include explicit `must`, imperative, `need to`, and independently testable prescriptive `should` statements.
- Include declarative scope classifications such as `in scope` and `out of scope`.
- Split conjunctive outcomes when each outcome can fail independently.
- Split independently applicable triggers, including the three 14-day update conditions.
- Preserve mutually exclusive implementation alternatives in one record when no branch is independently mandatory.
- Do not duplicate an umbrella statement when immediately following provisions fully operationalize it.
- Do not count a repeated clarification as a second provision.
- Include meaningful scope-table classifications; omit `N/A` cells and duplicate classifications already expressed by a general rule.

The inventory is `complete_publication` at atomic requirement granularity. Informative material is documented as excluded context, not converted into artificial `out_of_scope` provision records.

## 6. Provision record contract

Every provision record shall:

- use schema version `1.0.0`;
- use status `draft`;
- use granularity `requirement`;
- match exactly one inventory identifier;
- include an original, neutral paraphrase that preserves the source's mandatory or recommended strength;
- include an exact source locator and official URL;
- identify mapper `esaf-crosswalk-editorial-team` with authorized public-source access;
- include a `0.1.0` change-history entry dated on the authoring date;
- use exactly one disposition: `mapped` or `no_direct_mapping`;
- omit `reviewer` until qualified review occurs;
- avoid `out_of_scope` because the inventory contains prescriptive provisions only.

## 7. Mapping analysis

### 7.1 Direction and taxonomy

The initial snapshot contains only `esaf_to_external` relationship legs. Reverse-direction analysis is a later independently assessed extension and shall not be inferred from the forward mapping.

Relationship, coverage, and confidence remain independent:

- use `supports` where the ESAF control directly contributes to the external outcome;
- use `partially_supports` where coverage is incomplete;
- use `complements` or `informs` only when the adjacent contribution is analytically useful;
- use `substantial` coverage and `high` confidence only with explicit control-text evidence;
- never use a weak relationship merely to avoid a negative disposition.

Every relationship leg shall record nonempty rationale, conditions, expected evidence, and known gaps. Several partial legs shall not be presented as collectively sufficient.

### 7.2 Negative dispositions

Use `no_direct_mapping` when ESAF lacks a sufficiently direct requirement. Each negative rationale shall identify the missing outcome rather than making a generic scope statement.

Known areas requiring especially conservative treatment include:

- whole-enterprise technology scope outside AI systems;
- mandatory firewall deployment and default-deny behavior;
- exact password, throttling, and lockout thresholds;
- the fixed 14-day update deadline and exact severity triggers;
- endpoint anti-malware behavior and application allowlisting.

### 7.3 Likely ESAF coverage

Candidate controls include, subject to provision-level analysis:

- Scope and responsibility: `ARC-110`, `ARC-140`, `CMP-120`, `AUD-120`, `INF-100`, and `GOV-130`
- Firewalls: `INF-110`, `INF-130`, `IAM-110`, `IAM-130`, and `ARC-110`
- Secure configuration: `INF-110`, `INF-130`, `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, and `IAM-150`
- Security updates: `INF-120`, `ARC-150`, `OPS-110`, `INF-130`, and `APP-140`
- User access: `IAM-100`, `IAM-110`, `IAM-120`, `IAM-130`, `IAM-150`, and `MON-150`
- Malware protection: primarily negative dispositions; `INF-110`, `APP-140`, and `API-120` may be contextual only where their exact requirements justify a leg

These candidates are starting points, not preapproved relationships.

## 8. Generated and narrative outputs

Implementation shall update:

- `crosswalks/uk-cyber-essentials.md` with the source version, draft status, OGL attribution, inventory counts, scope rules, prominent coverage gaps, and links to the authoritative snapshot;
- `crosswalks/CATALOG.md` through deterministic generation;
- `crosswalks/catalog.json` through deterministic generation.

The landing page shall state that all referenced ESAF controls are draft and that the crosswalk does not establish certification, compliance, equivalence, or legal sufficiency. It shall identify Cyber Essentials Plus as a separate future mapping set.

## 9. Validation and failure behavior

Add focused regression coverage in `tests/test_uk_cyber_essentials_v33_crosswalk.py`. Tests shall verify:

- the exact mapping-set ID and repository path;
- the exact official source URL, version, date, access class, and ESAF source commit;
- the source digest and OGL attribution in narrative content;
- exactly 116 records with grouped counts `44/12/12/7/29/12`;
- contiguous record and inventory ID ranges with no duplicates;
- exact inventory-to-record agreement;
- mapper-assigned identifier disclosure and nonempty precise source locators;
- draft-only snapshot, record, and lifecycle states;
- an empty lifecycle event array;
- forward-only `esaf_to_external` relationship legs;
- zero `out_of_scope` dispositions;
- nonempty, specific negative rationales;
- relationship control/version resolution against the pinned manifest;
- required conditions, expected evidence, and known gaps for every leg;
- absence of equivalence, certification, compliance-percentage, or endorsement claims;
- current deterministic catalogs and valid local links.

The implementation shall fail closed on count drift, orphaned records, malformed metadata, unknown controls, copied baseline mismatch, stale catalogs, broken links, rights inconsistencies, or prohibited claims. Tests shall be written before enforceable implementation changes when a validator or repository invariant is added.

Required final gates are:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_uk_cyber_essentials_v33_crosswalk -v
python -m unittest discover -s tests -v
python tools/validate_crosswalks.py --write
python tools/migrate_control_mappings.py --check
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/validate_crosswalks.py --check
python tools/validate_crosswalks.py --check --baseline-ref 5de9ff356ddad1e193444cd7308eff16ed83e811
git diff --check
```

## 10. Review and publication

The complete branch receives independent specification and security/overclaiming reviews. Critical and Important findings shall be resolved before the pull request is made ready. Approved lower-severity findings shall be recorded with rationale or fixed with regression coverage.

Independent Codex review may establish technical closure for the pull request but shall not populate the schema `reviewer` or `approver` fields and shall not advance the snapshot beyond `draft`. Promotion to `reviewed` requires a qualified Cyber Essentials SME. Promotion to `approved` requires a separate governance decision and a valid lifecycle transition.

The pull-request head shall equal the independently reviewed SHA, required GitHub checks shall pass, and merge state shall be clean before merge.

## 11. Acceptance criteria

The milestone is complete when:

1. The source and rights evidence are fixed and attributed.
2. All 116 prescriptive provisions are inventoried and represented exactly once.
3. Every provision has either defensible forward mapping legs or a specific negative rationale.
4. The pinned ESAF manifest resolves every relationship.
5. The landing page and generated catalogs accurately expose draft status, counts, and gaps.
6. Focused, full-suite, crosswalk, migration, control, architecture, baseline, link, and diff checks pass.
7. Two independent reviewers report no unresolved Critical or Important findings.
8. The merged protected-branch workflow passes.
9. The snapshot remains `draft` pending qualified human review.
