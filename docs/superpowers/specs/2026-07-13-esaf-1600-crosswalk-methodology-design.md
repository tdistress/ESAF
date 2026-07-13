# ESAF-1600 Standards Crosswalk Methodology Design

**Status:** Approved

**Date:** 2026-07-13

**Target:** ESAF v0.5-beta foundation

## 1. Purpose

This design defines the foundation for ESAF-1600, the standards crosswalk system. ESAF-1600 will provide defensible, versioned, human-reviewable, and machine-validatable traceability between ESAF controls and external requirements without asserting equivalence, certification, compliance, or legal sufficiency.

The first substantive crosswalks will address PCI DSS, HITRUST CSF, and UK Cyber Essentials. This milestone establishes their shared method before any of those mappings are authored.

## 2. Goals

The methodology shall:

- preserve Markdown as the authoritative source;
- support requirement-level mappings with a controlled clause- or domain-level fallback;
- separate relationship, direction, coverage, and confidence;
- preserve concise rationale, expected evidence, conditions, and known gaps;
- record negative assessments instead of treating omitted mappings as conclusions;
- enforce independent review before approval;
- bind every mapping set to exact external, ESAF, and mapping-set versions;
- define a machine-checkable assessment universe so approved sets cannot silently omit in-scope provisions;
- prevent restricted external requirement text from becoming project content;
- resolve mapped ESAF controls against a release-pinned ESAF control manifest;
- generate deterministic human- and machine-readable catalog views; and
- fail closed when a record is incomplete, ambiguous, stale, or internally inconsistent.

## 3. Non-goals

This milestone will not:

- create substantive PCI DSS, HITRUST CSF, Cyber Essentials, or other external mappings;
- reproduce external requirement text;
- certify an organization or system;
- determine legal, regulatory, contractual, or audit sufficiency;
- calculate compliance percentages or composite compliance scores;
- replace qualified assessors, legal counsel, auditors, or source-authority guidance;
- add a web interface or interactive mapping application; or
- modify ESAF-1000 or ESAF-1200 requirements.

This milestone will make a narrowly scoped ESAF-1100 and control-template migration because ESAF-1100 currently defines a conflicting mapping taxonomy and locates external mapping metadata inside each control record. ESAF-1600 will become the authoritative mapping source; ESAF-1100 will retain only the obligation to use ESAF-1600 and expose catalog references.

## 4. Design decisions

### 4.1 Authoritative format

Mapping-set and provision records will be Markdown documents with YAML front matter. Markdown remains authoritative in accordance with `DEC-0001`. JSON and summary Markdown catalogs are generated outputs and shall not be edited directly.

ESAF-1600 is authoritative for external mapping assertions. Control records remain authoritative for control requirements and versions, but their `External mappings` sections shall reference ESAF-1600 rather than duplicate mapping rows. ESAF-1100 Section 14 and `CONTROL_TEMPLATE.md` will be migrated to this contract in the same milestone.

### 4.2 Mapping granularity

Mappings shall use individual external requirement identifiers whenever the source license and publication structure permit it. Clause- or domain-level records are permitted only when the mapper records a specific granularity exception explaining why requirement-level mapping is unavailable or inappropriate.

### 4.3 Mapping dimensions

Relationship, direction, coverage, and confidence are independent dimensions. No single strength score will collapse them.

### 4.4 Source handling

Records store permitted identifiers, permitted titles, concise original context summaries only when permitted, official source links, access classification, and original ESAF mapping rationale. `identifier_only` records omit provision paraphrase when identifiers and structural metadata may be published but paraphrase may not. Restricted or licensed requirement text shall not be committed.

### 4.5 Review and versioning

Reviewed provision records and reviewed or approved snapshots require a qualified reviewer who is different from the mapper. Draft mapping sets are mutable working sets. Reviewed sets must be inventory-complete. Approved sets are inventory-complete, content-immutable snapshots; a new external release, ESAF release, or approved mapping correction creates a new snapshot.

### 4.6 Completeness boundary

Every mapping set declares either a complete-publication scope or a declared-subset scope and carries an authoritative provision inventory. Draft records may incompletely implement that inventory but may not exceed it. Reviewed and approved sets shall match their inventories exactly. A subset mapping is never presented as publication-wide coverage.

### 4.7 Historical ESAF provenance

Each mapping set pins a mandatory full ESAF commit SHA, an optional tag display alias that resolves to that commit, the control-catalog digest, and per-control identifiers, versions, and record digests used by the analysis. Historical mappings validate against that frozen manifest rather than the current working control catalog.

## 5. Repository architecture

```text
crosswalks/
├── README.md
├── ESAF-1600.md
├── MAPPING_SET_TEMPLATE.md
├── PROVISION_INVENTORY_TEMPLATE.md
├── CROSSWALK_TEMPLATE.md
├── LIFECYCLE_RECORD_TEMPLATE.md
├── CATALOG.md
├── catalog.json
├── schema/
│   ├── mapping-set.schema.json
│   ├── provision-inventory.schema.json
│   ├── mapping-record.schema.json
│   ├── lifecycle-record.schema.json
│   └── esaf-control-manifest.schema.json
├── registry/
│   └── <mapping-set-id>.md
└── mappings/
    └── <authority-id>/
        └── <source-version>/
            └── <esaf-release>/
                └── <mapping-set-version>/
                    ├── README.md
                    ├── PROVISION_INVENTORY.md
                    ├── ESAF_CONTROL_MANIFEST.json
                    └── <record-id>.md
```

The existing `pci-dss.md`, `hitrust-csf.md`, and `uk-cyber-essentials.md` files remain concise landing pages. They will link to ESAF-1600 and, in later milestones, to their versioned mapping sets.

## 6. Processing flow

```text
Authoritative external source
        ↓
Declared scope + authoritative provision inventory
        ↓
Versioned snapshot + release-pinned ESAF control manifest
        ↓
Provision records and directional mapping legs
        ↓
JSON Schema validation
        ↓
Semantic and catalog-reference validation
        ↓
Deterministic JSON and Markdown catalogs
        ↓
Continuous-integration freshness check
```

Lifecycle changes after snapshot approval are recorded in `crosswalks/registry/` and do not mutate the approved snapshot.

`tools/validate_crosswalks.py` will expose the same operational contract as the control validator:

- `--write` validates authoritative records and rewrites generated outputs; and
- `--check` validates authoritative records and fails when generated outputs are missing or stale.

## 7. Mapping-set snapshot model

Each snapshot `README.md` will contain YAML metadata validated by `mapping-set.schema.json`.

Required metadata includes:

- mapping-set identifier;
- authority identifier and name;
- publication identifier and name;
- filesystem-safe source-version identifier and exact display label;
- filesystem-safe ESAF-release identifier and exact display label;
- mapping-set three-part release version (`MAJOR.MINOR.PATCH`);
- editorial status: `draft`, `reviewed`, or `approved`;
- official source URL;
- source publication date when available;
- access class: `public`, `restricted`, or `licensed`;
- licensing note;
- approved publication-rights basis, permitted metadata and analysis elements, restrictions, rights reviewer, and review date;
- scope type: `complete_publication` or `declared_subset`;
- scope statement and inventory count;
- default mapping granularity;
- mapper identifier, qualification statement, and mapping date;
- reviewer identifier, qualification statement, review date, and findings disposition when reviewed;
- approver identifier and approval date when approved;
- structured review findings with identifiers, severity, status, disposition, and resolution metadata;
- predecessor identifier when applicable;
- mandatory full ESAF source commit SHA, optional release-tag display alias, control-catalog SHA-256 digest, and control-manifest path; and
- change history.

The snapshot path components shall exactly match its authority identifier, source-version identifier, ESAF-release identifier, and mapping-set version metadata.

### 7.1 Snapshot identity

Identifiers used in paths are author-supplied canonical slugs constrained to lowercase ASCII letters and digits separated by single hyphens; version identifiers may additionally contain periods. Display labels preserve the authoritative punctuation and casing.

Mapping-set versions use SemVer core only: three nonnegative numeric components `MAJOR.MINOR.PATCH`. Prerelease and build metadata are intentionally unsupported so the value is also the canonical filesystem component; this constrained form is documented as a three-part release version rather than full SemVer.

The mapping-set identifier is exactly:

```text
<authority-id>--<publication-id>--<source-version-id>--esaf-<esaf-release-id>--<mapping-set-version>
```

The double-hyphen delimiter is reserved and prohibited inside components. The validator recomputes the identifier, rejects collisions, and requires directory and metadata agreement.

### 7.2 Snapshot immutability

An approved snapshot is content-immutable. Corrections create a new mapping-set version. A new external or ESAF release creates a new path. At approval, the validator computes a deterministic snapshot digest and records it in the lifecycle registry. Later publication, deprecation, retirement, and successor events update only the append-only lifecycle record.

Snapshot digest construction is fixed:

1. permit only regular files directly within the snapshot directory: `README.md`, `PROVISION_INVENTORY.md`, `ESAF_CONTROL_MANIFEST.json`, and provision Markdown records whose filenames match their record identifiers;
2. reject subdirectories, symbolic links, and every other directory entry, including unrecognized auxiliary files;
3. include the entire permitted file set in the digest;
4. require UTF-8 without a byte-order mark and LF line endings;
5. sort files by repository-relative POSIX path;
6. compute SHA-256 for each exact file byte sequence;
7. serialize one line per file as `<lowercase-sha256><two spaces><relative-posix-path>\n`; and
8. compute the snapshot SHA-256 over the UTF-8 bytes of that manifest.

Internal digest agreement is not treated as sufficient proof of immutability. Pull-request and protected-branch validation shall fetch full Git history and compare the candidate tree with a trusted baseline commit:

- snapshots already approved in the baseline must be byte-identical in the candidate;
- existing lifecycle event arrays must remain an exact prefix of the candidate event arrays; and
- only valid successor lifecycle events may be appended.

The baseline is the pull request's protected target-branch head during review and the pre-push protected-branch commit during post-merge validation. `tools/validate_crosswalks.py --check` performs current-tree checks; `--baseline-ref <commit>` additionally enforces immutability and append-only history. CI requires `--baseline-ref` whenever an event provides a trusted comparison commit.

### 7.3 Provision inventory

`PROVISION_INVENTORY.md` defines the machine-checkable assessment universe. It records scope type, scope statement, source basis, expected count, and the ordered external provision identifiers expected in the snapshot.

- A `complete_publication` inventory shall enumerate every provision in the publication at the declared granularity, including provisions ultimately assessed as out of scope.
- A `declared_subset` inventory shall enumerate every provision in the stated subset and shall disclose that it is not publication-wide coverage.
- Every provision record shall resolve to exactly one inventory identifier in every editorial state. Every inventory identifier shall have exactly one provision record when the snapshot is reviewed or approved; draft snapshots may leave inventory identifiers unimplemented but may not add records outside the inventory.
- A reviewed or approved snapshot is prohibited when inventory counts, identifiers, and records differ.

### 7.4 ESAF control manifest

`ESAF_CONTROL_MANIFEST.json` freezes the ESAF source used by the mapping. It records the ESAF release, mandatory 40-character source commit SHA, optional release-tag display alias, catalog digest, and each eligible control ID, control version, status, path, and control-record digest. Relationship assertions resolve against this manifest rather than the current `controls/catalog.json`.

The validator obtains the pinned commit from full Git history, reads `VERSION.md`, `controls/catalog.json`, and each referenced control file from that exact Git object, and deterministically regenerates the manifest. `VERSION.md` at the pinned commit shall match the declared ESAF release. An optional tag alias shall resolve to the same mandatory commit SHA but is never the trust anchor.

Eligible controls are exactly the control records present in the generated catalog at the pinned commit. Their editorial status is retained in the manifest so consumers can distinguish mappings to working-draft controls from mappings to published controls. The validator compares the committed manifest byte-for-byte with regenerated output and validates it against `esaf-control-manifest.schema.json`. CI uses full-history checkout so historical commits are available. This preserves historical validation when current control versions later change.

## 8. Provision record model

Each provision record represents one inventoried external provision at the finest permitted granularity. Its filename shall match its stable `record_id`; the exact external provision identifier remains separately recorded.

`record_id` is a mapping-set-local canonical slug constrained to lowercase ASCII letters and digits separated by single hyphens. Its globally unique key is `<mapping-set-id>/<record-id>`. The mapper selects and preserves the slug; the validator rejects duplicates and does not infer identity from punctuation-sensitive external identifiers.

Required record metadata includes:

- record identifier and mapping-set identifier;
- record editorial status: `draft` or `reviewed`;
- external provision identifier;
- granularity: `requirement`, `clause`, or `domain`;
- permitted title when available;
- context mode: `paraphrase` or `identifier_only`;
- concise original context summary when context mode is `paraphrase`, or a rights-based omission rationale when it is `identifier_only`;
- provision-specific official source URL or locator;
- granularity-exception rationale when granularity is not `requirement`;
- disposition;
- zero or more relationship assertions as permitted by the disposition;
- mapper identifier and mapping date;
- independent reviewer identifier, review date, and findings disposition when reviewed;
- predecessor record when applicable; and
- change history.

### 8.1 Provision disposition

Every provision record declares exactly one disposition:

- `mapped`: one or more ESAF-control relationships are required;
- `no_direct_mapping`: relationships must be empty and a gap rationale is required; or
- `out_of_scope`: relationships must be empty and a scope rationale is required.

Negative dispositions are first-class assessment results. An omitted provision is not interpreted as a negative disposition.

## 9. Relationship taxonomy

Every relationship assertion records one directed analytical leg between one external provision and one ESAF control version from the snapshot manifest.

### 9.1 Relationship

- `supports`: the source contributes directly to the target outcome or evidence but is not independently sufficient;
- `partially_supports`: the source addresses only a defined subset of the target outcome;
- `complements`: the source addresses an adjacent outcome that is useful with the target;
- `prerequisite`: the source establishes a condition needed before the target can operate as intended; or
- `informs`: the source provides interpretive or contextual guidance without claiming coverage.

`equivalent`, `satisfies`, `certifies`, and compliance-conclusion relationships are prohibited.

### 9.2 Direction

- `esaf_to_external`: the assertion analyzes how an ESAF control contributes to the external provision;
- `external_to_esaf`: the assertion analyzes how the external provision contributes to an ESAF control.

Bidirectional analysis is represented by two separate legs with opposite directions. Each leg carries its own relationship, coverage, confidence, rationale, conditions, expected evidence, and known gaps. The validator rejects duplicate same-direction legs but permits one leg in each direction for the same provision/control pair.

### 9.3 Coverage

- `substantial`: the relationship addresses most of the stated outcome within its declared conditions;
- `partial`: the relationship addresses a material subset;
- `narrow`: the relationship addresses a limited element; or
- `contextual`: the relationship provides context rather than direct outcome coverage.

Coverage does not express compliance sufficiency.

### 9.4 Confidence

- `high`: authoritative source language and ESAF requirements make the asserted relationship direct and unambiguous;
- `medium`: the relationship is well supported but depends on declared interpretation or implementation conditions; or
- `low`: the relationship is plausible but materially dependent on assumptions that require validation.

Confidence expresses confidence in the mapping analysis, not confidence in an implementation.

### 9.5 Required assertion fields

Every relationship assertion includes:

- ESAF control ID and version;
- relationship;
- direction;
- coverage;
- confidence;
- rationale for that direction;
- conditions and scope assumptions;
- expected evidence; and
- known gaps.

## 10. Review and publication workflow

Snapshot editorial states are:

```text
draft → reviewed → approved
```

Provision records use `draft → reviewed`. Mapping-set approval approves the reviewed records as one immutable snapshot; provision records do not carry an independent approved state.

The external lifecycle registry then tracks:

```text
approved → published → deprecated → retired
```

This split aligns crosswalk editorial review with the project publication lifecycle while keeping post-approval lifecycle changes outside immutable snapshot content. `reviewed` means the required technical and editorial mapping reviews are complete.

### 10.1 Draft

Draft content requires a mapper, mapping date, source identification, and complete analytical fields. Draft records are not authoritative mappings.

### 10.2 Reviewed

Reviewed records and snapshots require:

- a reviewer different from the mapper;
- reviewer qualification and authorized source access;
- review date;
- structured findings with no open Critical or Important item; and
- successful schema, semantic, reference, and freshness validation.

Each structured finding records a stable finding ID, affected record IDs, severity, status (`open`, `resolved`, or `accepted`), description, disposition, resolver or risk acceptor, and disposition date. `accepted` findings require a named approval authority and rationale and are permitted only for Minor findings. Approval is blocked by every open finding and by every Critical or Important finding that is not resolved.

### 10.3 Approved

An approved mapping set requires:

- every inventoried provision to have exactly one reviewed record;
- no unresolved review findings;
- an identified approver and approval date;
- an approved publication-rights analysis;
- an exact, valid ESAF control manifest;
- current generated catalogs; and
- successful repository validation.

An approved snapshot containing zero provision records is prohibited. The methodology foundation may generate an empty project catalog while no snapshot claims approved status.

The permitted parent/child combinations are:

| Snapshot state | Permitted provision-record states |
|---|---|
| Draft | Draft or Reviewed |
| Reviewed | Reviewed only |
| Approved | Reviewed only; frozen by snapshot approval |

A draft snapshot may be incomplete. Reviewed and approved snapshots shall exactly match their inventories.

### 10.4 Deprecated and retired

Each mapping set has one lifecycle record in `crosswalks/registry/`. The record contains the immutable snapshot digest and an append-only event list with event ID, state, date, actor, reason, predecessor/successor linkage, approval reference, previous-event digest, and event digest.

For event hashing, the first event uses 64 lowercase zeroes as `previous_event_digest`. The digest input contains only string values for these fields, in this fixed order: `event_id`, `state`, `date`, `actor`, `reason`, `predecessor_id`, `successor_id`, `approval_reference`, and `previous_event_digest`. An absent optional value is represented by the empty string. Every value is normalized to Unicode NFC and encoded as UTF-8. For each field, the serializer emits the ASCII field name, a colon, the base-10 byte length of the UTF-8 value without leading zeroes, a colon, the exact UTF-8 value bytes, and one LF byte. Concatenating those field encodings in the stated order produces the canonical byte sequence; `event_digest` is the lowercase SHA-256 of that sequence. Each later event names the preceding event digest. Current-tree validation recomputes the chain; baseline validation proves the trusted event sequence is an unchanged prefix, which prevents a coordinated rewrite from passing the publication gate.

Published records identify the approved snapshot exposed as an active release. Deprecated lifecycle records name a successor or explain why none exists. Retired content remains available in historical views but is excluded from current views. Lifecycle events may not rewrite snapshot content or reuse identifiers.

For a given authority, publication, external source version, and ESAF release, at most one mapping-set version may be `published` without being deprecated. Multiple historical versions remain valid and queryable.

## 11. Source and licensing governance

The public repository shall not contain restricted or licensed external requirement text.

Before any source-derived mapping-set, inventory, or provision content enters this repository, its publication-rights analysis shall be approved by a named rights reviewer different from the mapper. Source analysis may be prepared in a private working environment, but a public contribution may not be used as the venue for initial rights review.

Each mapping set committed to the repository shall:

- identify the authoritative source and exact version;
- classify source access;
- provide a licensing note;
- record the permission basis for publishing identifiers, titles, structural inventories, paraphrases, and derivative mapping analysis;
- enumerate which source-derived elements are permitted and which are prohibited;
- identify official source links;
- attest that mapper and reviewer used the identified authoritative source, were authorized to access it, and reviewed the documented publication basis; and
- use original paraphrase and rationale rather than copied source text.

Provision context is required only to the extent permitted by the documented publication basis. A complete-publication mapping may use `identifier_only` records when complete identifiers and structural inventory may be published but paraphrases may not. The mapping set shall use a declared subset or shall not enter the repository only when the identifiers or inventory needed to substantiate its claimed completeness boundary cannot be published. Public-source quotations are exceptional, must be demonstrably permitted, and are not needed by the base schema. The base record model intentionally has no `source_text` or `verbatim_requirement` field.

Automated validation cannot prove copyright or license compliance. Schema design, publication-rights metadata, required attestations, independent review, and contribution policy provide layered controls for that risk. This milestone will update `CONTRIBUTING.md` to require source-rights provenance and an intellectual-property attestation for external mapping contributions.

## 12. Validation rules

The validator will combine JSON Schema validation with repository-aware semantic checks.

It shall reject:

- malformed front matter or schema violations;
- duplicate mapping-set or record identifiers;
- snapshot paths that disagree with metadata;
- unexpected snapshot files, directories, symbolic links, or other directory entries;
- record-to-snapshot identifier mismatches;
- duplicate or extra provision records relative to the authoritative inventory in every state;
- missing provision records relative to the authoritative inventory when a snapshot is reviewed or approved;
- inventory counts that disagree with inventory identifiers;
- duplicate external provision identifiers within a snapshot;
- duplicate provision/control/direction legs;
- unresolved ESAF control identifiers in the pinned control manifest;
- ESAF control versions that disagree with the pinned control manifest;
- invalid control-manifest schema, catalog digest, or provenance metadata;
- a missing/unreachable pinned commit, ESAF release mismatch at that commit, optional tag alias resolving elsewhere, or manifest output differing from regeneration at the pinned commit;
- unsupported relationship, direction, coverage, confidence, disposition, status, access, or granularity values;
- missing rationale, evidence, conditions, known-gap, or review fields;
- non-requirement granularity without a specific exception rationale;
- `mapped` records without relationships;
- negative dispositions with relationships;
- negative dispositions without their required rationale;
- an attempt to encode bidirectionality in one leg instead of two independently assessed legs;
- identical mapper and reviewer identities in reviewed or approved content;
- reviewed provision records or reviewed/approved snapshots without completed review metadata;
- invalid snapshot/provision status combinations;
- approved snapshots without approval metadata, rights approval, complete inventory coverage, or eligible records;
- open review findings, unresolved Critical or Important findings, or accepted Critical/Important findings at approval;
- published lifecycle records without an approved snapshot and matching snapshot digest;
- lifecycle transitions that are missing, reordered, duplicated, or inconsistent;
- baseline-approved snapshot bytes that changed or baseline lifecycle events that are not an exact candidate prefix;
- multiple active published versions for the same authority/publication/source-version/ESAF-release tuple;
- deprecated lifecycle records without a successor or explanation;
- source-rights metadata that does not state the publication basis and permitted elements;
- publication-rights approval whose rights reviewer is missing or identical to the mapper;
- any repository mapping snapshot whose publication-rights review is not already approved, regardless of editorial state;
- provision context mode or content that exceeds the mapping set's recorded permitted elements;
- broken local links;
- unresolved drafting markers in reviewed or approved content;
- generated catalogs that are missing or stale; and
- text-encoding corruption detected by existing repository conventions.

Validation errors will name the file, field or rule, observed problem, and required correction. Results will be sorted deterministically.

The methodology uses three distinct version conditions:

- `inconsistent` is invalid: path, metadata, manifest, digest, or referenced version values disagree;
- `superseded` is valid historical state: a newer lifecycle record exists and the older set is deprecated or retired; and
- `generated_stale` is invalid: generated output differs from authoritative source records.

Older exact source versions are not invalid merely because a newer publication exists.

## 13. Generated catalogs

### 13.1 Machine-readable catalog

`crosswalks/catalog.json` will include:

- catalog schema version;
- generated-source declaration;
- mapping-set, provision, relationship, and negative-disposition counts;
- separate counts by snapshot editorial state, lifecycle state, provision-record state, authority, publication, source version, ESAF release, disposition, relationship, direction, coverage, and confidence;
- complete mapping-set metadata, inventory metadata, every provision including negative dispositions, every directional relationship leg, and lifecycle linkage needed for forward and reverse queries; and
- explicit status and historical linkage.

Machine output is sorted by authority ID, publication ID, normalized source version, normalized ESAF release, semantic mapping-set version, external provision ID, record ID, ESAF control ID, and direction.

### 13.2 Human-readable catalog

`crosswalks/CATALOG.md` will provide:

- a generated-content warning;
- active published mapping sets;
- reviewed and draft work in progress;
- deprecated and retired historical sets;
- coverage and gap summaries; and
- links to authoritative mapping-set and provision records.

An active mapping set is a registry record in `published` state that is not deprecated or retired. The validator permits only one active mapping-set version for an exact authority/publication/source-version/ESAF-release tuple. Different external source versions may remain active simultaneously and are labeled explicitly; the catalog does not infer one globally preferred source version.

The initial catalog will deterministically report zero mapping sets, provisions, relationships, and negative dispositions. It will not imply that external standards were assessed.

## 14. Templates

`MAPPING_SET_TEMPLATE.md` will demonstrate all snapshot metadata and required narrative sections without representing an approved mapping set.

`PROVISION_INVENTORY_TEMPLATE.md` will demonstrate complete-publication and declared-subset boundaries, source basis, rights constraints, expected counts, and exact provision identifiers.

`CROSSWALK_TEMPLATE.md` will demonstrate:

- a requirement-level mapped provision;
- asymmetric bidirectional analysis using two independent directional legs;
- a controlled granularity exception; and
- negative-disposition rules.

`LIFECYCLE_RECORD_TEMPLATE.md` will demonstrate the append-only approval, publication, deprecation, and retirement event model plus snapshot-digest protection.

Examples in templates are non-normative placeholders and will remain outside `crosswalks/mappings/` so they cannot enter generated catalogs.

## 15. Testing strategy

`tests/test_validate_crosswalks.py` will use temporary repositories and fixtures to cover:

- valid empty-foundation generation;
- valid draft, reviewed, and approved snapshots plus published, deprecated, and retired lifecycle records;
- valid complete-publication and declared-subset inventories;
- valid incomplete draft snapshots and invalid incomplete reviewed/approved snapshots;
- valid mapped, no-direct-mapping, and out-of-scope provisions;
- every schema enum and required-field boundary;
- snapshot-path and metadata agreement;
- rejection of unrecognized auxiliary files, nested directories, symbolic links, and other unexpected snapshot entries;
- unique identifiers and relationships;
- exact inventory-to-record completeness;
- control resolution against fixture manifests and the generated control-manifest contract, without hardcoding the current catalog count;
- control-version and record-digest agreement with the pinned manifest;
- manifest regeneration from an immutable commit, VERSION agreement, and optional tag-alias resolution;
- disposition and relationship cardinality;
- granularity-exception enforcement;
- asymmetric two-leg bidirectional analysis;
- independent mapper/reviewer enforcement;
- structured review findings and approval eligibility;
- snapshot/provision status compatibility;
- source-rights metadata and approval;
- identifier-only and paraphrase context modes against permitted publication elements;
- lifecycle-transition, active-version uniqueness, and snapshot-digest enforcement;
- language-independent event-digest test vectors, including Unicode NFC and empty optional fields;
- trusted-baseline rejection of coordinated snapshot/digest rewrites and lifecycle-prefix rewrites;
- deprecation and retirement linkage;
- deterministic JSON and Markdown rendering;
- generated-output freshness checking;
- broken links, drafting markers, and encoding checks; and
- actionable, stable error messages.

Mutation tests will demonstrate rejection of:

- identical mapper and reviewer identities;
- inconsistent path, manifest, digest, and version metadata while preserving valid superseded history;
- incomplete inventories and duplicate provision/control/direction legs;
- missing rationale, evidence, conditions, or known gaps;
- relationships added to negative dispositions;
- omitted negative-disposition rationale;
- unsupported fallback granularity;
- collapsing two directional legs into one bidirectional assertion;
- unsafe snapshot/provision state combinations;
- open findings, missing rights approval, and mutated approved snapshots;
- accepted Critical/Important findings and unapproved source-derived drafts;
- auxiliary files, nested directories, and symbolic links introduced into snapshots; and
- stale generated output.

The complete repository suite will continue to run control and architecture validation.

## 16. Continuous integration

`.github/workflows/catalog-validation.yml` will be extended to:

- trigger on `crosswalks/**` and `tools/validate_crosswalks.py` changes;
- check out full Git history (`fetch-depth: 0`) so pinned commits and trusted baselines are available;
- run all repository unit tests;
- run `python tools/validate_crosswalks.py --check` for current-tree validation;
- run `python tools/validate_crosswalks.py --check --baseline-ref <trusted-commit>` for pull requests and protected-branch updates;
- retain the existing control and architecture validation steps.

For pull requests, the trusted commit is the fetched protected target-branch head. For protected-branch pushes, it is the event's pre-push commit. A missing or shallow baseline is a validation error when approved or lifecycle-managed snapshots exist.

The crosswalk validator shall use only dependencies already declared in `requirements-dev.txt` unless the implementation plan demonstrates a necessary addition.

## 17. Existing landing pages

`crosswalks/pci-dss.md`, `crosswalks/hitrust-csf.md`, and `crosswalks/uk-cyber-essentials.md` will remain `Planned`. This milestone will update them only to link to ESAF-1600 and explain that no substantive mapping has yet been approved.

`crosswalks/README.md` will replace its collapsed `strength` terminology with the approved relationship, direction, coverage, and confidence dimensions.

`controls/ESAF-1100.md` Section 14 will be revised to designate ESAF-1600 records as authoritative, remove the conflicting `equivalent`, `broader`, `narrower`, `intersects`, and `related` taxonomy, and require control-level views to resolve from ESAF-1600. `controls/CONTROL_TEMPLATE.md` and the `External mappings` section of every existing control record will replace release-specific absence assertions and embedded tables with a durable link to the ESAF-1600 generated catalog. This mechanical migration prevents control text from becoming false when a later mapping set is approved and does not add substantive external mappings.

`CONTRIBUTING.md` will add source-rights provenance, publication-basis, authorized-access, and intellectual-property attestation requirements for external mapping contributions.

No external publication version will be selected in this methodology milestone. Each later crosswalk design will verify and approve its authoritative source version before creating a mapping-set snapshot.

## 18. Decision log updates

The implementation will add decisions establishing that:

- provision Markdown is the authoritative crosswalk source;
- generated crosswalk catalogs are deterministic derivative outputs;
- relationship, direction, coverage, and confidence are independent dimensions;
- negative dispositions are explicit records;
- independent review is required before approval;
- approved mapping snapshots are immutable and version-bound, while draft snapshots remain mutable working sets;
- lifecycle changes use an external append-only registry;
- assessment completeness is bounded by an authoritative provision inventory;
- historical mappings resolve against a release-pinned ESAF control manifest;
- ESAF-1600 supersedes the prior ESAF-1100 mapping taxonomy; and
- restricted external requirement text is excluded and publication rights are recorded.

## 19. Acceptance criteria

The methodology milestone is complete when:

1. ESAF-1600 normatively defines scope, semantics, lifecycle, versioning, review, source governance, and disclaimers.
2. Mapping-set, provision-inventory, mapping-record, lifecycle-record, and ESAF-control-manifest schemas validate their intended artifacts.
3. Templates demonstrate the complete snapshot, inventory, record, and lifecycle contracts without entering generated catalogs.
4. The validator enforces every rule in Section 12 and produces deterministic errors.
5. Reviewed and approved snapshots cannot omit or add a provision relative to their declared inventories.
6. Historical control references resolve against manifests regenerated from mandatory immutable source commits rather than mutable current-state metadata.
7. Approved snapshots remain digest-protected while publication, deprecation, and retirement occur through lifecycle records, and trusted-baseline validation rejects coordinated snapshot or event-history rewrites.
8. Empty initial catalogs generate deterministically and state that no mapping sets were assessed.
9. All focused schema, semantic, resolution, mutation, lifecycle, and freshness tests pass.
10. The existing full repository test suite passes.
11. Control, architecture, and crosswalk validators pass in local and CI checks.
12. ESAF-1100, its control template, all existing control `External mappings` sections, and the crosswalk README use the ESAF-1600 source-of-truth and taxonomy contract.
13. `CONTRIBUTING.md` requires source-rights provenance and publication attestation before source-derived mapping content enters the repository.
14. The three priority landing pages link to the methodology without claiming completed mappings.
15. The repository contains no external requirement text or substantive external mapping assertions.
16. No content claims equivalence, certification, compliance, or legal sufficiency.
17. An independent whole-branch review has no unresolved Critical or Important findings.

## 20. Follow-on sequence

After this methodology is approved and merged, each substantive crosswalk will receive its own design, implementation plan, mapping branch, independent review, and approval gate. The recommended order is:

1. PCI DSS;
2. UK Cyber Essentials and Cyber Essentials Plus; and
3. HITRUST CSF.

PCI DSS provides the first broad technical and governance pilot. Cyber Essentials tests a smaller foundational-hygiene scheme. HITRUST follows after the public-repository licensing workflow has been exercised with an explicitly licensed source.
