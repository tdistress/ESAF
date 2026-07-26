# PCI DSS source readiness and mapping decision design

## Purpose

ESAF shall close the PCI DSS v4.0.1 readiness workstream with a formally
evidenced `HOLD`. The decision shall preserve a precise path to reconsideration
without creating a mapping snapshot, provision inventory, registry record, or
substantive PCI DSS mapping assertion.

PCI DSS v4.0.1 is the current active PCI DSS version. Its official PDF is
access-controlled by a PCI Security Standards Council license agreement, and
the public PCI SSC terms do not grant ESAF a general right to publish,
distribute, or prepare derivative works from Council content. The exact PDF
bytes, PDF checksum, and independently verified provision population are
therefore unavailable for an authorized public mapping at this time.

## Decision

The readiness disposition is `HOLD`.

`HOLD` means:

- no directory shall be created under `crosswalks/mappings/` for PCI DSS;
- no PCI DSS lifecycle record shall be created under `crosswalks/registry/`;
- no PCI DSS provision title, requirement text, close paraphrase, inventory, or
  mapping relationship shall enter the repository;
- no PCI DSS compliance, equivalence, coverage, certification, authorization,
  endorsement, or legal-sufficiency claim shall be made; and
- the workstream may be reconsidered only after every recorded blocker passes
  its re-entry test.

Internal study permitted by the PCI SSC license is outside the public
repository boundary and does not authorize an ESAF mapping.

## Authoritative readiness record

The authoritative record shall be
`crosswalks/readiness/pci-dss-v4.0.1.md`. YAML front matter shall conform to a
closed JSON Schema and shall contain:

- stable record identity, decision, decision date, and accountable owner;
- PCI SSC authority, publication family, exact version, language, and status;
- the official Document Library, access-controlled PDF, discovery catalog,
  publication announcement, terms, IPR policy, and permission-request URLs;
- the retrieval timestamp, byte length, and SHA-256 digest of the mutable
  discovery catalog, explicitly distinguished from the unavailable PDF digest;
- exact source-artifact, provision-inventory, and publication-rights states;
- the proposed mapping direction and boundaries;
- mapper and independent-review qualification requirements;
- overclaiming prohibitions;
- one blocker object per missing prerequisite, including owner, missing
  evidence, reconsideration trigger, and deterministic re-entry test; and
- change history.

The Markdown body shall explain the evidence, decision, nonclaim boundary,
reconsideration sequence, and adoption disclaimer. It shall contain no
source-derived PCI DSS requirement content.

## Source pinning boundary

The readiness record may pin public discovery metadata that PCI SSC exposes
without accepting the document license. It shall record the official
`doc_library.json` bytes observed on 2026-07-25 by URL, retrieval timestamp,
byte length, and SHA-256, together with the selected catalog facts used to
identify PCI DSS v4.0.1. The mutable discovery-catalog digest shall not be
presented as the standard's digest.

The normative source artifact shall remain `unavailable` with null byte length,
SHA-256, page count, and inventory digest. A future authorized acquisition
shall create a new readiness-record version or documented change that pins the
exact English PDF bytes and independently reconciles the provision inventory
before any mapping snapshot exists.

The official version facts are:

- publication: PCI Data Security Standard;
- version: v4.0.1;
- publication announcement date: 2024-06-11;
- predecessor v4.0 retirement date: 2024-12-31;
- previously future-dated requirements effective date: 2025-03-31; and
- current v4.0.1 retirement date: not announced.

The effective date shall not be mislabeled as the v4.0.1 publication date.

## Publication-rights boundary

A named, independent rights review shall record the public evidence:

- PCI SSC owns the copyright in its standards and work product;
- ordinary study rights are limited to internal copying and employee sharing;
- public distribution, derivative works, and non-personal use are not generally
  authorized without a separate written agreement; and
- PCI SSC provides a case-specific Materials License Agreement request path.

The readiness record shall mark publication rights `blocked`, not infer that
identifiers, titles, paraphrases, inventories, or mapping analysis are safe to
publish, and require a written PCI SSC permission or license covering the exact
ESAF artifact and distribution channels before reconsideration.

## Proposed future mapping scope

If every blocker is later resolved, the first candidate mapping scope should be
`esaf_to_external` only because the published ESAF PCI DSS landing page promises
to map applicable ESAF controls to PCI DSS. `external_to_esaf` shall remain
explicitly excluded until separately designed and approved.

A future GO decision shall freeze:

- exact authorized source bytes and checksum;
- complete-publication or declared-subset scope;
- publishable provision identifiers and granularity;
- permitted field classes;
- exact directional question;
- mapper and independent qualified reviewers with authorized source access;
- adversarial positive and negative feasibility probes; and
- every ESAF-1600 overclaiming and lifecycle control.

GO shall require every gate to pass. It shall authorize a separate substantive
mapping change and shall not itself create or imply PCI DSS coverage.

## Validation

`tools/validate_crosswalk_readiness.py` shall discover direct Markdown children
of `crosswalks/readiness/`, reject unexpected entries and duplicate YAML keys,
validate the front matter against
`crosswalks/schema/readiness-record.schema.json`, and enforce semantic
conditions that JSON Schema alone cannot safely express.

For a `HOLD` record, validation shall require:

- at least one blocker with nonempty owner, evidence gap, trigger, and re-entry
  test;
- null artifact and inventory digests when their states are unavailable;
- a blocked or unreviewed publication-rights state;
- a nonempty prohibited-claims list;
- no PCI DSS mapping or registry record anywhere in the repository;
- no language that promotes the decision to GO; and
- internal agreement among record identity, version, source URLs, and status.

Focused tests shall begin red and cover malformed records, incomplete blockers,
false source pins, prohibited PCI mapping artifacts, duplicate keys,
unauthorized decision transitions, and successful validation of the committed
HOLD record. The full test suite, crosswalk validator, link validator, relevant
repository validators, and whole-branch whitespace checks shall pass on the
exact final candidate.

## Repository presentation

`crosswalks/pci-dss.md` shall change from `Planned` to `Readiness HOLD`, link to
the authoritative readiness record and reviews, state the blockers and
nonclaims, and explain the reconsideration boundary.

`project/BACKLOG.md` shall mark issue 58 complete through the evidenced-HOLD
path without implying that a PCI DSS mapping exists. Generated crosswalk
catalog counts shall remain unchanged.

## Independent review

The exact candidate SHA shall receive:

- a source and inventory review that confirms the official-version facts,
  discovery digest, unavailable PDF checksum, and absence of an invented
  provision population; and
- a publication-rights and overclaiming review that confirms the HOLD boundary,
  permission trigger, reviewer requirements, and prohibited claims.

Critical and Important findings shall be resolved before publication. Any
candidate change shall invalidate prior exact-SHA review evidence and require
both reviews to be rerun.

## Non-goals

This change does not:

- accept the PCI SSC license agreement on behalf of Eric Amos, Hearst, ESAF, or
  any other entity;
- provide legal advice or decide copyright exceptions;
- download, commit, reproduce, paraphrase, or redistribute PCI DSS;
- create a provision inventory, mapping record, mapping snapshot, registry
  event, or generated catalog entry;
- claim PCI SSC authorization, validation, endorsement, certification,
  compliance, equivalence, coverage, or legal sufficiency; or
- correct the pre-existing ESAF-1600 snapshot-path wording discrepancy, which
  is irrelevant until a separate authorized mapping snapshot is designed.
