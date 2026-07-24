# Qualified Review Protocol for UK Mapping Snapshots

## Status and boundary

This protocol prepares Draft mappings for qualified independent human review
under ESAF-1600. Preparation, automation, mapper self-review, and AI-produced
review are not qualified review. Until every applicable condition is met, the
affected mapping set remains `draft`.

## In-scope snapshots

- `uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0`
  — Core, 116 provisions.
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0`
  — Plus forward, 144 provisions.
- `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0`
  — Plus reverse, 144 provisions.

Core, Plus forward, and Plus reverse require separate packages, findings, and
conclusions.

## Candidate integrity

Every review names one full 40-character Git commit SHA and one package
manifest digest. A changed candidate invalidates final review evidence.

## Reviewer eligibility

A named human records scheme qualification, ESAF or mapping qualification,
authorized source access, organization, verification locator, independence
from the mapper, and conflicts of interest. The project owner accepts or
rejects eligibility per mapping set and review role. The reviewer must be
different from the mapper.

## Specification and inventory review

Verify official source identity/version/checksum/locators, publication rights,
provision population and hierarchy, record coverage, registry/catalog
consistency, and predecessor/change-history integrity.

## Security and overclaiming review

Verify each relationship and `no_direct_mapping` rationale against exact
normative source and ESAF text. Check direction, coverage, confidence,
conditions, evidence, gaps, `prerequisite` versus `partially_supports`, and
all certification, compliance, equivalence, endorsement, and assurance
nonclaims.

## Findings

Use Critical, Important, and Minor. Resolve Critical and Important findings
before `reviewed`. Only Minor may be accepted, with named acceptor, rationale,
and date. Record separate worksheets for both review disciplines.

## Lifecycle transition

This preparation does not add reviewer metadata or change lifecycle state.
A later transition updates every mapping record, mapping-set metadata,
registry state, catalogs, and digests together on an exact human-reviewed
head. `reviewed` is not `approved`.

## Stop conditions

Stop for missing eligibility, independence, source access, source/version or
digest mismatch, changed SHA, combined Core/Plus conclusions, external-source
redistribution, open Critical or Important findings, unresolved template
markers, or an AI-produced review. The affected mapping remains `draft`.
