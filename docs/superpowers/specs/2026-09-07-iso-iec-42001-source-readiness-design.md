# ISO/IEC 42001:2023 source readiness and mapping decision design

## Purpose

ESAF shall decide whether a public ISO/IEC 42001:2023 mapping may proceed by
using an evidence-pinned, mechanically derived GO/HOLD method shaped like the
PCI DSS readiness package. The current evidence produces `HOLD`: ISO/IEC
42001:2023 is identifiable as the target publication, but the authorized source
bytes, source checksum, publishable provision inventory, publication
permission, and qualified mapping reviewers are not available.

This package intentionally does **not** follow the NIST AI RMF readiness shape.
ISO copyright typically prohibits republishing provision content, so no
provision-inventory JSON and no mapping artifacts are created under HOLD.

## Deliverables

- `docs/superpowers/specs/2026-09-07-iso-iec-42001-source-readiness-oracle.json`
- `docs/superpowers/reviews/2026-09-07-iso-iec-42001-publication-rights-review.md`
- `docs/superpowers/specs/2026-09-07-iso-iec-42001-mapping-readiness-matrix.json`
- `tools/render_iso_iec_42001_mapping_go_no_go.py`
- `docs/superpowers/reviews/2026-09-07-iso-iec-42001-2023-mapping-go-no-go-review.md`
- `docs/superpowers/reviews/2026-09-07-iso-iec-42001-2023-mapping-go-no-go-traceability.md`
- focused source-readiness and renderer tests
- `crosswalks/iso-iec-42001.md` landing page

No file shall be created under `crosswalks/mappings/` or
`crosswalks/registry/`. No ISO/IEC 42001 provision inventory JSON shall exist.
Generated crosswalk catalog counts shall not change.

## Rights-review sequence

The publication-rights review shall be committed before the source-readiness
oracle, feasibility matrix, or derivative decision analysis. It shall use only
official ISO public rights and discovery links available without accepting
commercial purchase terms. Only `official_links` is permitted among the six
ESAF-1600 mapping field classes. Minimal bibliographic source-identity metadata
is a separate closed allowance, matching the PCI pattern.

## Source-readiness oracle

The closed JSON oracle shall pin public bibliographic identity and discovery
URLs without accepting purchase terms or retaining protected PDF bytes:

- publisher, publication-family, document reference, edition/year, language,
  format, and full bibliographic title;
- official product page, copyright policy, and Online Browsing Platform landing;
- protected-access state with `license_accepted: false`;
- null source-artifact byte, digest, page-count, provision-count, and inventory
  fields; and
- explicit inventory and mapping nonclaims.

Public product-page retrieval may return an access challenge rather than
catalog HTML. Any retained challenge response is not the normative standard and
shall not be treated as a source-artifact digest.

## Exact proposed mapping contract

Direction: `esaf_to_external`. `external_to_esaf` is excluded.

Scope: `complete_publication` at
`finest_authorized_publishable_clause_or_control_outcome_identifier`.

Exact directional question:

> Does exact normative ESAF control requirement text directly support,
> partially support, or establish a prerequisite for the outcome required by
> one authorized, publishable ISO/IEC 42001:2023 clause or control outcome,
> with each relationship's conditions, expected evidence, and known gaps
> recorded independently, without implying ISO/IEC 42001 compliance,
> assessment, equivalence, certification, authorization, or endorsement?

## Mechanical GO/HOLD method

The closed readiness matrix uses the same eight ordered gates as PCI DSS:

1. `source_identity_and_drift`
2. `authorized_source_artifact`
3. `publication_rights`
4. `provision_inventory`
5. `semantic_and_normative_feasibility`
6. `esaf_1600_and_schema_fit`
7. `mapper_and_reviewer_readiness`
8. `overclaiming_controls`

Blockers `ISO-IEC-42001-READINESS-B001` through `B005` mirror the PCI
categories. `GO` requires all gates `PASS`, zero blockers, a positive
feasibility probe, and no open Critical or Important findings. Otherwise
`HOLD` when any gate is `BLOCKED`.

## Mapper and qualified-review contract

A future GO requires a named mapper with ISO/IEC 42001:2023 and ESAF-1600
experience, plus independent reviewers for `iso_iec_42001_subject_matter`,
ESAF specification and mapping, publication rights, and security/overclaiming,
with exact-SHA dual reviews and owner-authorized approval.

## HOLD boundary and reconsideration

HOLD prohibits clause/control identifiers and titles, structural inventory,
paraphrases, derivative mapping analysis, mapping artifacts, coverage
statistics, and claims of ISO/IEC authorization, compliance, equivalence, or
certification. Reconsideration requires written ISO/IEC permission (or
equivalent licensing), authorized artifact acquisition, reconciled inventory,
named qualified people, and a refreshed feasibility probe.

## Validation and presentation

Focused tests shall enforce the closed oracle and matrix contracts, rights
ancestry, zero mapping artifacts, unchanged catalog counts (3 / 404 / 81 /
325), renderer `--check`, landing `Readiness HOLD`, CI/tools wiring, and
`I143-*` traceability. `crosswalks/iso-iec-42001.md` shall publish the HOLD
status and evidence links without asserting compliance or endorsement.
