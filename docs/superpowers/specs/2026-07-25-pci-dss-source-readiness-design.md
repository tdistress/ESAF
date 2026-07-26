# PCI DSS source readiness and mapping decision design

## Purpose

ESAF shall decide whether a public PCI DSS v4.0.1 mapping may proceed by using
an evidence-pinned, mechanically derived GO/HOLD method. The current evidence
produces `HOLD`: PCI DSS v4.0.1 is identifiable as the active version, but the
authorized source bytes, source checksum, publishable provision inventory,
publication permission, and qualified mapping reviewers are not available.

The HOLD shall preserve a precise reconsideration path without creating a
mapping snapshot, provision record, registry record, or substantive PCI DSS
mapping assertion.

## Repository architecture

The readiness decision shall reuse the established source-oracle,
feasibility-matrix, deterministic-renderer, review, and traceability pattern
under `docs/superpowers/`. It shall not create a parallel authoritative
registry under `crosswalks/`.

The deliverables are:

- `docs/superpowers/specs/2026-07-25-pci-dss-source-readiness-oracle.json`;
- `docs/superpowers/reviews/2026-07-25-pci-dss-publication-rights-review.md`;
- `docs/superpowers/specs/2026-07-25-pci-dss-mapping-readiness-matrix.json`;
- `tools/render_pci_dss_mapping_go_no_go.py`;
- `docs/superpowers/reviews/2026-07-25-pci-dss-mapping-go-no-go-review.md`;
- `docs/superpowers/reviews/2026-07-25-pci-dss-mapping-go-no-go-traceability.md`;
- focused source-readiness and renderer tests; and
- status updates to `crosswalks/pci-dss.md` and `project/BACKLOG.md`.

No file shall be created under `crosswalks/mappings/` or
`crosswalks/registry/`, and generated crosswalk catalog counts shall not change.

## Rights-review sequence

The publication-rights review shall be committed before the source-readiness
oracle, feasibility matrix, or derivative decision analysis. It shall use only
official PCI SSC rights sources available without accepting the protected
document license.

The review shall name a reviewer different from any future mapper, record the
review date, confirm authorized access to the reviewed public rights sources,
and record that the publication basis was reviewed. It shall partition these
six ESAF-1600 field classes exhaustively and without overlap:

- identifiers;
- titles;
- structural inventory;
- paraphrases;
- derivative mapping analysis; and
- official links.

For the current HOLD, only official links are permitted among those six mapping
field classes. "Identifiers" and "titles" mean PCI DSS provision identifiers
and provision titles, not the minimal public bibliographic metadata needed to
identify the publication. The review shall separately approve this closed
bibliographic set: publisher name, publication-family name, document reference,
version label, language, format, public catalog dates and status flags,
announcement/retirement/effective dates, retrieval metadata, and official
URLs. All PCI DSS provision identifiers, provision titles, structural
inventory, paraphrases, and derivative mapping analysis remain prohibited
pending case-specific written permission. This is a fail-closed
publication-control decision based on absence of affirmative permission, not
legal advice or a conclusion about statutory exceptions.

The review shall cite:

- PCI SSC Terms and Conditions;
- PCI SSC Intellectual Property Rights Policy;
- the protected document license interstitial; and
- the PCI SSC Materials License Agreement request path.

## Source-readiness oracle

The closed JSON oracle shall pin only public discovery facts available without
accepting the protected document license:

- publisher and publication-family identity;
- document-library and discovery-catalog URLs;
- exact UTC retrieval time, byte length, and SHA-256 of the retrieved mutable
  `doc_library.json`;
- selected catalog values for document reference, version, archived state,
  protected state, catalog `last_updated`, and canonical English access URL;
- official publication-announcement URL and date;
- predecessor retirement and future-dated-requirement effective dates;
- source-artifact state, access behavior, and null byte digest/count fields;
- publication-date precision and evidence boundary;
- normative/supporting-document boundary; and
- explicit inventory and mapping nonclaims.

The discovery-catalog digest shall be labeled as a time-stamped digest of
mutable discovery metadata, never as the PCI DSS v4.0.1 source digest.

The official facts that may be recorded are:

- current version label: `v4.0.1`;
- official publication announcement date: `2024-06-11`;
- source artifact publication date: `2024-06` at month precision unless the
  authorized artifact later supplies a more exact date;
- PCI SSC catalog `last_updated`: `2024-06-11T07:00:00+00:00`;
- predecessor v4.0 retirement date: `2024-12-31`;
- previously future-dated requirements effective date: `2025-03-31`; and
- current v4.0.1 retirement date: not announced.

The effective date shall not be mislabeled as the publication date, and the
announcement date shall not be silently substituted for an unverified exact
artifact publication date.

The normative PCI DSS PDF shall remain `unavailable` with null byte length,
SHA-256, page count, provision count, and inventory digest. The oracle shall
record that direct HTTP retrieval returned an access response rather than PDF
bytes and that browser navigation displayed a license agreement requiring
acceptance. No one acting in this workstream shall accept that agreement.

## Exact proposed mapping contract

The first mapping direction is exactly `esaf_to_external`.
`external_to_esaf` is excluded and would require a separate approved design.

The proposed scope is `complete_publication` at the finest authorized,
publishable numbered PCI DSS requirement or sub-requirement identifier.
If written permission later narrows the available population or granularity,
the scope shall be redesigned and reapproved before GO rather than silently
converted to a subset.

The exact directional question is:

> Does exact normative ESAF control requirement text directly support,
> partially support, or establish a prerequisite for the outcome required by
> one authorized, publishable PCI DSS v4.0.1 numbered requirement or
> sub-requirement, with each relationship's conditions, expected evidence, and
> known gaps recorded independently, without implying PCI DSS compliance,
> assessment, equivalence, certification, authorization, or endorsement?

Conditions may narrow an existing relationship but shall not supply a missing
PCI DSS outcome. Adjacency, implementation guidance, source titles, assessment
procedures, or compliance-reporting forms shall not establish a positive
mapping basis.

## Mechanical GO/HOLD method

The closed readiness matrix shall contain these ordered gates:

1. `source_identity_and_drift`;
2. `authorized_source_artifact`;
3. `publication_rights`;
4. `provision_inventory`;
5. `semantic_and_normative_feasibility`;
6. `esaf_1600_and_schema_fit`;
7. `mapper_and_reviewer_readiness`; and
8. `overclaiming_controls`.

Each gate status shall be exactly `PASS` or `BLOCKED` and shall include a
rationale plus one or more evidence references. Every `BLOCKED` gate shall
include one or more blockers. Every blocker shall contain:

- a stable blocker ID;
- category;
- accountable owner;
- missing evidence;
- reconsideration trigger; and
- deterministic re-entry test.

The matrix decision shall be derived, not asserted:

- `GO` requires all eight gates to be `PASS`, zero blockers, a positive
  feasibility probe for the exact directional question, and no unresolved
  Critical or Important findings.
- `HOLD` requires one or more `BLOCKED` gates and at least one complete blocker
  for each blocked gate.

The renderer shall reject any inconsistent matrix and deterministically derive
the Markdown review. A HOLD review shall show all gates, blockers, owners,
evidence gaps, triggers, re-entry tests, excluded direction, and nonclaims.

The current expected gate results are:

| Gate | Status | Basis |
|---|---|---|
| Source identity and drift | `PASS` | Public PCI SSC discovery metadata identifies v4.0.1 |
| Authorized source artifact | `BLOCKED` | Protected PDF bytes and SHA-256 are unavailable |
| Publication rights | `BLOCKED` | No case-specific written permission covers ESAF publication |
| Provision inventory | `BLOCKED` | No authorized exact source or reconciled provision population |
| Semantic and normative feasibility | `BLOCKED` | Exact PCI outcomes cannot be assessed without authorized source access |
| ESAF-1600 and schema fit | `PASS` | Existing direction, relationship, disposition, rights, and lifecycle controls are sufficient |
| Mapper and reviewer readiness | `BLOCKED` | Named qualified humans with authorized source access are not evidenced |
| Overclaiming controls | `PASS` | The HOLD nonclaims and future analytical boundaries can be enforced |

## Mapper and qualified-review contract

A future GO requires:

- a named mapper with PCI DSS v4.0.1 and ESAF-1600 experience and authorized
  source access;
- an independent PCI DSS subject-matter reviewer, different from the mapper,
  with current QSA or owner-approved equivalent credentials and authorized
  source access;
- an independent ESAF mapping/specification reviewer;
- a publication-rights reviewer different from the mapper;
- a security/overclaiming reviewer; and
- an approver authorized by the ESAF project owner.

One person may fill more than one independent review discipline only through an
explicit owner-approved dual-role decision that records why independence
remains adequate. The mapper shall never review their own work.

Each qualified review shall record identity, role, qualification or relevant
experience, authorized-source-access attestation, signed or attributable
attestation, review date, exact candidate SHA and artifact digests, findings,
and disposition. Specification/inventory and security/overclaiming reviews
shall run separately on the same exact candidate. Any candidate change shall
invalidate both reviews and require redispatch.

## HOLD boundary and reconsideration

HOLD prohibits:

- PCI DSS source text, titles, close paraphrases, or structural inventory;
- provision records, mapping legs, negative dispositions, snapshots, registry
  records, and generated catalog entries;
- coverage statistics or percentages; and
- claims of PCI SSC authorization, validation, endorsement, assessment,
  compliance, equivalence, certification, coverage, or legal sufficiency.

Reconsideration requires all of the following:

1. case-specific written PCI SSC permission that covers the exact field
   classes, repository, website, generated publications, license, and
   downstream redistribution model;
2. acquisition by an authorized person of the exact English PCI DSS v4.0.1 PDF
   through the intended flow, with final URL, filename, byte length, SHA-256,
   PDF metadata, page count, and acquisition time recorded;
3. an independently reconciled complete provision inventory at the authorized
   granularity, with count and digest;
4. availability of the named mapper and qualified independent reviewers; and
5. a refreshed current-version and source-drift check.

Each satisfied trigger shall update the evidence and matrix. GO shall not be
recorded until all gates pass mechanically.

## GO closure semantics

A readiness GO may authorize a separate substantive mapping pull request, but
it does not by itself close issue 58 or the `v0.5-beta` PCI workstream. Under
the GO path, closure requires the approved Draft mapping scope to be completed
under ESAF-1600, including the source-pinned snapshot, provision inventory,
control manifest, provision records and negative dispositions, lifecycle
record, generated catalogs, exact-SHA qualified reviews, and traceability.

The evidenced HOLD path may close issue 58 and satisfy the corresponding
milestone workstream when this decision package passes all review and
publication gates.

## Validation

Focused tests shall begin red and shall enforce:

- exact closed oracle and matrix key sets;
- source identity, URL, date-precision, protected-access, and null-artifact
  invariants;
- the canonical rights-review path, commit ancestry, exact committed and live
  byte equality, SHA-256 binding, six-element provision-field
  partition, separately approved closed bibliographic set, independence,
  access, and publication-basis attestations;
- exact gate order, status vocabulary, evidence references, blocker coverage,
  and mechanical GO/HOLD derivation;
- exact directional question, complete-publication scope, granularity, and
  excluded reverse direction;
- mapper/reviewer qualification and independence requirements;
- prohibited claims and reconsideration triggers;
- deterministic renderer output and `--check` drift detection;
- zero PCI DSS mapping, registry, or generated catalog artifacts; and
- unchanged ordinary crosswalk catalog counts.

The full test suite, crosswalk validator with protected baseline, link
validator, relevant repository validators, and whole-branch whitespace checks
shall pass on the exact candidate. In-repository review records shall review the
substantive candidate SHA. After those review-only records are committed, fresh
independent source/inventory and rights/overclaiming reviews shall approve the
final PR head without another repository mutation; their final-head SHA,
results, and evidence shall be recorded in the PR description or external check
evidence. No open Critical or Important findings may remain.

## Repository presentation

`crosswalks/pci-dss.md` shall change from `Planned` to `Readiness HOLD`, link to
the oracle, rights review, matrix, generated review, and traceability record,
and state the blockers, owner, reconsideration conditions, and nonclaims.

`project/BACKLOG.md` shall record issue 58 as completed through the
evidenced-HOLD path without implying that a PCI DSS mapping exists.

## Non-goals

This change does not:

- accept the PCI SSC license agreement on behalf of Eric Amos, Hearst, ESAF, or
  another entity;
- provide legal advice or decide copyright exceptions;
- download, commit, reproduce, paraphrase, or redistribute PCI DSS;
- create a provision inventory, mapping record, mapping snapshot, registry
  event, or generated catalog entry;
- claim PCI SSC authorization, validation, endorsement, certification,
  compliance, equivalence, coverage, or legal sufficiency; or
- correct the pre-existing ESAF-1600 snapshot-path wording discrepancy, which
  is irrelevant until a separate authorized mapping snapshot is designed.
